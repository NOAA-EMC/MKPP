#pragma once
#include <Kokkos_Core.hpp>

#include <string>

namespace mkpp {
namespace host {

enum CellErrorCode : int {
    SUCCESS = 0,
    ERR_SINGULAR_MATRIX = 1,
    ERR_NON_FINITE_STATE = 2,
    ERR_CONVERGENCE_FAILURE = 3,
    ERR_NUMERICAL_FAILURE = 4
};

/// @brief Runtime execution parameters for host integration dispatch.
struct HostExecutionParams {
    double dt{60.0};              ///< Integration timestep size in seconds
    const double* jvals{nullptr}; ///< Pointer to Cloud-J photolysis rate array
    double temp{288.15};          ///< Temperature in Kelvin (used for mechanisms like GOCART)
    double rh{0.5};               ///< Relative humidity fraction (used for mechanisms like GOCART)
    double clw{0.0};              ///< Cloud liquid water fraction (used by cloud-gated mechanisms)
    int steps{1};                 ///< Number of integration timesteps
};

/// @brief Helper trait function invoking solver integration with matching argument signature.
template <typename SolverKernelsType, typename SubStateView>
KOKKOS_INLINE_FUNCTION void integrate_cell(SolverKernelsType& solver,
                                           const HostExecutionParams& params,
                                           SubStateView sub_state) {
    static const double default_jvals[512] = {0.0};
    const double* jvals_ptr = params.jvals ? params.jvals : default_jvals;

    if constexpr (requires { solver.integrate(params.dt, sub_state, jvals_ptr, params.temp, params.rh, params.clw); }) {
        solver.integrate(params.dt, sub_state, jvals_ptr, params.temp, params.rh, params.clw);
    } else if constexpr (requires { solver.integrate(params.dt, sub_state, jvals_ptr, params.temp, params.rh); }) {
        solver.integrate(params.dt, sub_state, jvals_ptr, params.temp, params.rh);
    } else {
        solver.integrate(params.dt, sub_state, jvals_ptr);
    }
}

template <typename MemorySpace = Kokkos::DefaultExecutionSpace::memory_space>
struct BatchErrorStatus {
    using memory_space = MemorySpace;
    Kokkos::View<int*, MemorySpace> status;

    BatchErrorStatus() = default;
    explicit BatchErrorStatus(size_t num_cells)
        : status("BatchErrorStatus", num_cells) {}
    explicit BatchErrorStatus(Kokkos::View<int*, MemorySpace> s)
        : status(s) {}

    KOKKOS_INLINE_FUNCTION
    void set_error(size_t cell_idx, CellErrorCode code) const {
        status(cell_idx) = static_cast<int>(code);
    }

    KOKKOS_INLINE_FUNCTION
    int get_error(size_t cell_idx) const {
        return status(cell_idx);
    }
};

/// @brief Serial host integrator for single-thread CPU benchmark parity.
/// @tparam SolverKernelsType Generated solver kernel type callable on host.
/// @tparam StateViewType Kokkos view type containing cell-major concentrations.
/// @param state Four-dimensional concentration view with cell extent in dimension 0.
/// @param dt Integration timestep in seconds.
/// @param steps Number of timesteps to integrate per cell.
/// @param jvals Pointer to Cloud-J photolysis rate array (may be nullptr if no photolysis).
template <typename SolverKernelsType, typename StateViewType>
void execute_mechanism_serial_steps(StateViewType state, const double dt, const int steps,
                                    const double* jvals = nullptr) {
    const int num_cells = state.extent(0);

    for (int cell_idx = 0; cell_idx < num_cells; ++cell_idx) {
        SolverKernelsType solver;
        auto sub_state = Kokkos::subview(state, cell_idx, Kokkos::ALL(), 0, 0);
        for (int step = 0; step < steps; ++step) { solver.integrate(dt, sub_state, jvals); }
    }
}

/// @brief Serial host integrator for a single timestep.
/// @tparam SolverKernelsType Generated solver kernel type callable on host.
/// @tparam StateViewType Kokkos view type containing cell-major concentrations.
/// @param state Four-dimensional concentration view with cell extent in dimension 0.
/// @param dt Integration timestep in seconds.
/// @param jvals Pointer to Cloud-J photolysis rate array (may be nullptr if no photolysis).
template <typename SolverKernelsType, typename StateViewType>
void execute_mechanism_serial(StateViewType state, const double dt, const double* jvals = nullptr) {
    execute_mechanism_serial_steps<SolverKernelsType>(state, dt, 1, jvals);
}

template <typename SolverKernelsType, typename StateViewType>
struct TiledCellIntegrator {
    StateViewType m_state;
    double m_dt;
    const double* m_jvals;

    TiledCellIntegrator(StateViewType s, double dt, const double* jvals = nullptr)
        : m_state(s), m_dt(dt), m_jvals(jvals) {}

    KOKKOS_INLINE_FUNCTION
    void operator()(const int cell_idx) const {
        SolverKernelsType solver;
        auto sub_state = Kokkos::subview(m_state, cell_idx, Kokkos::ALL(), 0, 0);
        solver.integrate(m_dt, sub_state, m_jvals);
    }
};

template <typename SolverKernelsType, typename StateViewType>
struct TiledCellTimeIntegrator {
    StateViewType m_state;
    double m_dt;
    int m_steps;
    const double* m_jvals;

    TiledCellTimeIntegrator(StateViewType s, double dt, int steps, const double* jvals = nullptr)
        : m_state(s), m_dt(dt), m_steps(steps), m_jvals(jvals) {}

    KOKKOS_INLINE_FUNCTION
    void operator()(const int cell_idx) const {
        SolverKernelsType solver;
        auto sub_state = Kokkos::subview(m_state, cell_idx, Kokkos::ALL(), 0, 0);
        for (int step = 0; step < m_steps; ++step) { solver.integrate(m_dt, sub_state, m_jvals); }
    }
};

template <typename SolverKernelsType, typename StateViewType>
struct ParamsTiledCellIntegrator {
    StateViewType m_state;
    HostExecutionParams m_params;

    ParamsTiledCellIntegrator(StateViewType s, const HostExecutionParams& params)
        : m_state(s), m_params(params) {}

    KOKKOS_INLINE_FUNCTION
    void operator()(const int cell_idx) const {
        SolverKernelsType solver;
        if constexpr (StateViewType::rank() == 4) {
            auto sub_state = Kokkos::subview(m_state, cell_idx, Kokkos::ALL(), 0, 0);
            for (int step = 0; step < m_params.steps; ++step) {
                integrate_cell(solver, m_params, sub_state);
            }
        } else {
            auto sub_state = Kokkos::subview(m_state, cell_idx, Kokkos::ALL());
            for (int step = 0; step < m_params.steps; ++step) {
                integrate_cell(solver, m_params, sub_state);
            }
        }
    }
};

template <typename SolverKernelsType, typename StateViewType, typename ErrorViewType>
struct BatchedTeamCellIntegrator {
    StateViewType m_state;
    double m_dt;
    int m_steps;
    const double* m_jvals;
    ErrorViewType m_error_status;

    using ScratchViewType = Kokkos::View<double*, Kokkos::DefaultExecutionSpace::scratch_memory_space, Kokkos::MemoryUnmanaged>;

    BatchedTeamCellIntegrator(StateViewType s, double dt, int steps, const double* jvals, ErrorViewType err)
        : m_state(s), m_dt(dt), m_steps(steps), m_jvals(jvals), m_error_status(err) {}

    KOKKOS_INLINE_FUNCTION
    void operator()(const typename Kokkos::TeamPolicy<Kokkos::DefaultExecutionSpace>::member_type& member) const {
        const int num_cells = static_cast<int>(m_state.extent(0));
        const int num_species = static_cast<int>(m_state.extent(1));

        const int team_rank = member.league_rank();
        const int num_teams = member.league_size();
        const int cells_per_team = (num_cells + num_teams - 1) / num_teams;
        const int begin_cell = team_rank * cells_per_team;
        const int end_cell = (begin_cell + cells_per_team < num_cells) ? (begin_cell + cells_per_team) : num_cells;

        // Team-level scratch space allocation
        ScratchViewType scratch_species(member.team_scratch(0), num_species * (end_cell - begin_cell));

        auto state = m_state;
        auto steps = m_steps;
        auto dt = m_dt;
        auto jvals = m_jvals;
        auto err = m_error_status;

        Kokkos::parallel_for(Kokkos::TeamThreadRange(member, begin_cell, end_cell), [=](const int cell_idx) {
            auto sub_state = Kokkos::subview(state, cell_idx, Kokkos::ALL(), 0, 0);

            // Pre-kernel non-finite boundary check
            bool has_non_finite = false;
            for (int sp = 0; sp < num_species; ++sp) {
                if (!Kokkos::isfinite(sub_state(sp))) {
                    has_non_finite = true;
                    break;
                }
            }

            if (has_non_finite) {
                if constexpr (requires { err.set_error(cell_idx, ERR_NON_FINITE_STATE); }) {
                    err.set_error(cell_idx, ERR_NON_FINITE_STATE);
                } else {
                    err(cell_idx) = static_cast<int>(ERR_NON_FINITE_STATE);
                }
                Kokkos::printf("FATAL ERROR: Non-finite concentration detected at pre-kernel boundary for cell %d\n", cell_idx);
                return;
            }

            SolverKernelsType solver;
            for (int step = 0; step < steps; ++step) {
                solver.integrate(dt, sub_state, jvals);
            }
        });
    }
};

/// @brief Batched host integrator using hierarchical Kokkos::TeamPolicy
template <typename SolverKernelsType, typename StateViewType, typename ErrorViewType>
void execute_mechanism_steps_batched(const std::string& name, StateViewType state, const double dt,
                                     const int steps, const double* jvals, ErrorViewType error_status,
                                     int team_size = 64) {
    using ExecSpace = Kokkos::DefaultExecutionSpace;
    using TeamPolicy = Kokkos::TeamPolicy<ExecSpace>;
    using ScratchViewType = Kokkos::View<double*, ExecSpace::scratch_memory_space, Kokkos::MemoryUnmanaged>;

    const int num_cells = static_cast<int>(state.extent(0));
    const int num_species = static_cast<int>(state.extent(1));
    const int num_teams = (num_cells + team_size - 1) / team_size;

    size_t scratch_bytes = ScratchViewType::shmem_size(num_species * team_size);

    TeamPolicy policy(num_teams, Kokkos::AUTO);
    policy.set_scratch_size(0, Kokkos::PerTeam(scratch_bytes));

    Kokkos::parallel_for(
        "MKPP_Batched_Team_Dispatch_" + name,
        policy,
        BatchedTeamCellIntegrator<SolverKernelsType, StateViewType, ErrorViewType>(
            state, dt, steps, jvals, error_status));
}

/// @brief Integrate all requested timesteps with a single Kokkos launch.
/// @tparam SolverKernelsType Generated solver kernel type callable in the active execution space.
/// @tparam StateViewType Kokkos view type containing cell-major concentrations.
/// @param name Mechanism name used for Kokkos profiling labels.
/// @param state Four-dimensional concentration view with cell extent in dimension 0.
/// @param dt Integration timestep in seconds.
/// @param steps Number of timesteps to integrate per cell.
/// @param jvals Pointer to Cloud-J photolysis rate array (may be nullptr if no photolysis).
template <typename SolverKernelsType, typename StateViewType>
void execute_mechanism_steps(const std::string& name, StateViewType state, const double dt,
                             const int steps, const double* jvals = nullptr) {
    using ExecSpace = Kokkos::DefaultExecutionSpace;
    const int num_cells = state.extent(0);

    Kokkos::parallel_for(
        "MKPP_Grid_Dispatch_" + name,
        Kokkos::RangePolicy<ExecSpace>(0, num_cells, Kokkos::ChunkSize(64)),
        TiledCellTimeIntegrator<SolverKernelsType, StateViewType>(state, dt, steps, jvals));
}

template <typename SolverKernelsType, typename StateViewType>
void execute_mechanism(const std::string& name, StateViewType state, double dt,
                       const double* jvals = nullptr) {
    execute_mechanism_steps<SolverKernelsType>(name, state, dt, 1, jvals);
}

}  // namespace host

/// @brief Core handle implementation structure for MKPP Host Model API C ABI wrappers.
struct mkpp_handle_impl {
    std::size_t num_cells{0};
    std::size_t num_species{0};
    std::size_t num_reactions{0};
    std::size_t num_photolysis{0};
    bool is_initialized{false};

    // Unmanaged 2D view over host model species concentrations (num_cells, num_species)
    Kokkos::View<double**, Kokkos::LayoutLeft, Kokkos::HostSpace, Kokkos::MemoryUnmanaged> species_conc;

    // Unmanaged 1D views over host model meteorology & aerosol drivers (num_cells)
    Kokkos::View<double*, Kokkos::LayoutLeft, Kokkos::HostSpace, Kokkos::MemoryUnmanaged> temperature;
    Kokkos::View<double*, Kokkos::LayoutLeft, Kokkos::HostSpace, Kokkos::MemoryUnmanaged> pressure;
    Kokkos::View<double*, Kokkos::LayoutLeft, Kokkos::HostSpace, Kokkos::MemoryUnmanaged> air_density;
    Kokkos::View<double*, Kokkos::LayoutLeft, Kokkos::HostSpace, Kokkos::MemoryUnmanaged> relative_humidity;
    Kokkos::View<double*, Kokkos::LayoutLeft, Kokkos::HostSpace, Kokkos::MemoryUnmanaged> aerosol_surface_area;

    // Unmanaged 2D view over host model photolysis rates (num_cells, num_photolysis)
    Kokkos::View<double**, Kokkos::LayoutLeft, Kokkos::HostSpace, Kokkos::MemoryUnmanaged> photolysis_rates;

    // Allocated scratch workspace memory for internal solver calculations
    Kokkos::View<double**, Kokkos::LayoutLeft> workspace_scratch;

    // Human-readable error diagnostic message for last failure
    std::string last_error_msg;

    void set_error(const std::string& msg) {
        last_error_msg = msg;
    }
};

}  // namespace mkpp
