# How-To Guide: Compile and Run Adjoint & Tangent-Linear Model (TLM) Solvers

This guide explains how to compile chemical mechanisms with discrete Adjoint and Tangent-Linear Model (TLM) support in MKPP and integrate them into 4D-Var Data Assimilation frameworks (such as JEDI).

---

## Overview

For 4D-Var Data Assimilation and sensitivity analysis, atmospheric models require adjoint models that efficiently compute gradients of cost functions with respect to initial chemical species concentrations ($\frac{\partial J_{\text{cost}}}{\partial \mathbf{y}_0}$).

MKPP generates analytical transposed Jacobians ($J^T$) and discrete adjoint integrators at build time, eliminating manual derivation and runtime automatic differentiation overhead.

---

## 1. Compile Mechanism with Adjoint Support

Pass the `--adjoint` flag to `mkpp compile` when generating C++ headers:

```bash
# Compile SAPRC-99 mechanism with ROS-3 solver and Adjoint/TLM support
mkpp compile mechanisms/openatmos/saprc99/mechanism.json \
  --test-env example_env.yaml \V
  --out mkpp-generated \
  --solver ros3 \
  --adjoint
```

When `--adjoint` is enabled, the generated header (`mkpp-generated/saprc99.hpp`) includes:

- `CheckpointBuffer`: Struct for saving forward trajectory state vectors at each accepted timestep.
- `integrate_fwd_checkpoint`: Forward integration kernel that records checkpoints during integration.
- `integrate_adj`: Discrete adjoint backward integration kernel that walks backward through saved checkpoints, accumulating adjoint variables ($\lambda$).
- `compute_adjoint`: Function that evaluates the transposed analytical Jacobian $J^T$.

---

## 2. Using Checkpoint Buffers in Forward Solvers

In a 4D-Var assimilation window, the forward solver runs first and records trajectory checkpoints:

```cpp
#include <Kokkos_Core.hpp>
#include "saprc99.hpp"

int main(int argc, char* argv[]) {
    Kokkos::initialize(argc, argv);
    {
        const int num_cells = 100;
        const double t_start = 0.0;
        const double t_end = 3600.0; // 1 hour

        // Allocate state view and checkpoint buffers
        Kokkos::View<double**, Kokkos::LayoutLeft> state("state", num_cells, saprc99::NUM_SPECIES);
        saprc99::CheckpointBuffer checkpoint_buf(num_cells, 500); // 500 max steps

        // Environmental drivers
        double temp = 298.15;
        double press = 101325.0;

        // Run forward integration with trajectory checkpointing
        Kokkos::parallel_for("Forward_Checkpoint", num_cells, KOKKOS_LAMBDA(const int i) {
            auto cell_state = Kokkos::subview(state, i, Kokkos::ALL());
            saprc99::integrate_fwd_checkpoint(
                cell_state, temp, press, t_start, t_end, checkpoint_buf, i
            );
        });
        Kokkos::fence();
    }
    Kokkos::finalize();
    return 0;
}
```

---

## 3. Running Discrete Adjoint Backward Integration

After the forward trajectory is recorded, the discrete adjoint solver executes backward from $t_{\text{end}}$ to $t_{\text{start}}$, propagating sensitivity vector $\lambda$:

```cpp
// Allocate adjoint variable vector (lambda), initialized with cost function gradient dJ/dy_tf
Kokkos::View<double**, Kokkos::LayoutLeft> lambda("lambda", num_cells, saprc99::NUM_SPECIES);

// Run backward discrete adjoint integration
Kokkos::parallel_for("Adjoint_Backward", num_cells, KOKKOS_LAMBDA(const int i) {
    auto cell_lambda = Kokkos::subview(lambda, i, Kokkos::ALL());
    saprc99::integrate_adj(
        cell_lambda, temp, press, t_start, t_end, checkpoint_buf, i
    );
});
Kokkos::fence();

// lambda(i, species) now contains dJ / d(y_0) sensitivity gradient for initial conditions
```

---

## 4. Evaluating Transposed Analytical Jacobians ($J^T$)

If your data assimilation framework requires direct evaluation of $J^T$ at a given state:

```cpp
Kokkos::View<double*, Kokkos::LayoutLeft> cell_state("state", saprc99::NUM_SPECIES);
Kokkos::View<double**, Kokkos::LayoutLeft> J_adj("J_adj", saprc99::NUM_SPECIES, saprc99::NUM_SPECIES);

// Compute J^T into J_adj
saprc99::compute_adjoint(cell_state, J_adj, temp, press, cair);
```

---

## 5. Verification & Taylor Series Sensitivity Check

To verify the correctness of generated adjoint gradients against finite difference perturbations:

$$\lim_{\epsilon \to 0} \frac{J(\mathbf{y}_0 + \epsilon \mathbf{\delta y}) - J(\mathbf{y}_0)}{\epsilon} = \mathbf{\lambda}^T \mathbf{\delta y}$$

1. Run the forward model with state $\mathbf{y}_0$ and compute cost function value $J_0$.
2. Compute adjoint sensitivity vector $\mathbf{\lambda}$ via `integrate_adj`.
3. Apply a small perturbation $\epsilon \mathbf{\delta y}$ to species $k$ and re-run forward model to get $J_{\text{pert}}$.
4. Confirm that $\frac{J_{\text{pert}} - J_0}{\epsilon}$ matches $\lambda_k$ within relative error $< 10^{-5}$.

---

## Related Documents

- [AOT Solver C++ & CLI API Reference](../reference/aot-solver-api.md)
- [Reaction Kinetics, Multiphase Aerosols, and Unified Jacobian Explanation](../explanation/unified-jacobian-and-reaction-kinetics.md)
- [AOT Solver Quickstart Tutorial](../tutorials/aot-solver-quickstart.md)
