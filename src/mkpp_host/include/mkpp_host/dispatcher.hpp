#pragma once
#include <Kokkos_Core.hpp>
#include <string>

namespace mkpp {
namespace host {

// This will serve as the host execution loop for UFS/FV3
template <typename ExecSpace, typename SolverKernelsType, typename StateViewType>
struct GridDispatcher {
    using TeamPolicy = Kokkos::TeamPolicy<ExecSpace>;
    using MemberType = typename TeamPolicy::member_type;

    StateViewType state;
    double dt_phys;

    GridDispatcher(StateViewType s, double dt) : state(s), dt_phys(dt) {}

    KOKKOS_INLINE_FUNCTION
    void operator()(const MemberType& team_member) const {
        const int cell_idx = team_member.league_rank();
        
        Kokkos::parallel_for(Kokkos::TeamThreadRange(team_member, 1), [&](const int& s) {
            SolverKernelsType solver;
            
            // Extract the 1D chemical state for this specific grid cell
            // Assuming 2D state view: [cell, species]
            int n_spec = state.extent(1);
            
            // In an optimized production environment, we use scratch memory or direct pointers.
            // For safety, we pull into a thread-local flat state.
            double local_state[1000] = {0.0};
            for(int k=0; k<n_spec; k++) {
                local_state[k] = state(cell_idx, k, 0, 0);
            }
            
            // Execute the AOT generated math
            solver.integrate(dt_phys, local_state);
            
            // Write back to global memory
            for(int k=0; k<n_spec; k++) {
                state(cell_idx, k, 0, 0) = local_state[k];
            }
        });
    }
};

template <typename SolverKernelsType, typename StateViewType>
void execute_mechanism(const std::string& name, StateViewType state, double dt) {
    using ExecSpace = Kokkos::DefaultExecutionSpace;
    int num_cells = state.extent(0);
    
    Kokkos::parallel_for("MKPP_Grid_Dispatch_" + name,
        Kokkos::TeamPolicy<ExecSpace>(num_cells, Kokkos::AUTO),
        GridDispatcher<ExecSpace, SolverKernelsType, StateViewType>(state, dt)
    );
}

} // namespace host
} // namespace mkpp
