# Tutorial: Quickstart with Ahead-Of-Time (AOT) Kokkos ODE Solvers

This tutorial guides you through generating, compiling, and executing an Ahead-Of-Time (AOT) Kokkos C++ chemical ODE solver in MKPP.

---

## Learning Objectives

By the end of this tutorial, you will be able to:

1. Generate C++ Kokkos ODE solver headers from a chemical mechanism specification using the MKPP Python AOT generator.
2. Integrate the generated Kokkos header into a C++ application.
3. Launch parallel ODE integration across grid cells using Kokkos views and execution spaces.

---

## Prerequisites

- **Python**: 3.10+ with SymPy and PyYAML installed.
- **C++ Compiler**: C++17 or C++20 compliant compiler (GCC 10+, Clang 12+, NVCC, or ROCm).
- **Kokkos Core**: Installed or available via CMake dependencies.

---

## Step 1: Generate the C++ Solver Header

MKPP provides AOT code generation scripts to convert mechanism declarations into header-only Kokkos ODE solvers.

To generate a solver header for a supported mechanism (e.g., SAPRC-99, Chapman, GOCART) with your choice of Rosenbrock solver tableau (`ros2`, `ros3`, `ros4`, `rodas3`, `rodas4`):

```bash
# Compile SAPRC-99 mechanism with ROS-3 (default 3-stage order 3) solver
mkpp compile mechanisms/openatmos/saprc99/mechanism.json --test-env example_env.yaml --out mkpp-generated --solver ros3

# Compile high-throughput ROS-2 (2-stage order 2) solver for 3D ESM runs
mkpp compile mechanisms/openatmos/saprc99/mechanism.json --test-env example_env.yaml --out mkpp-generated --solver ros2

# Compile high-accuracy ROS-4 (4-stage order 4) solver
mkpp compile mechanisms/openatmos/saprc99/mechanism.json --test-env example_env.yaml --out mkpp-generated --solver ros4

# Compile ROS-3 solver with discrete Adjoint / TLM support for JEDI 4D-Var
mkpp compile mechanisms/openatmos/saprc99/mechanism.json --test-env example_env.yaml --out mkpp-generated --solver ros3 --adjoint
```

The generated header (`mkpp-generated/saprc99.hpp`) contains:

- Flat scalar rate evaluations (`compute_rates`).
- Symbolic, unrolled Jacobian computation (`compute_jacobian`).
- RCM-permuted and block-sparse symbolic LU decomposition (`lu_decompose`).
- Straight-line forward and backward substitution (`lu_solve`).
- Rosenbrock integration kernels (`integrate` and `integrate_with_reduction`).

---

## Step 2: Write a C++ Integration Host Application

Create a minimal host driver `main.cpp` that initializes Kokkos, allocates state views, and invokes the generated solver:

```cpp
#include <Kokkos_Core.hpp>
#include <iostream>
#include "saprc99.hpp"

int main(int argc, char* argv[]) {
    Kokkos::initialize(argc, argv);
    {
        const int num_cells = 1000;
        const double t_start = 0.0;
        const double t_end = 3600.0; // 1 hour integration

        // Allocate 2D grid state view: (num_cells, NUM_SPECIES)
        Kokkos::View<double**, Kokkos::LayoutLeft> state("state", num_cells, saprc99::NUM_SPECIES);
        Kokkos::View<double*> temp("temperature", num_cells);
        Kokkos::View<double*> press("pressure", num_cells);

        // Initialize environmental conditions
        Kokkos::deep_copy(temp, 298.15);
        Kokkos::deep_copy(press, 101325.0);

        // Execute parallel ODE integration across grid cells
        Kokkos::parallel_for("MKPP_Integrate", num_cells, KOKKOS_LAMBDA(const int i) {
            auto cell_state = Kokkos::subview(state, i, Kokkos::ALL());
            saprc99::integrate(cell_state, temp(i), press(i), t_start, t_end);
        });

        Kokkos::fence();
        std::cout << "Successfully integrated " << num_cells << " grid cells over 1 hour." << std::endl;
    }
    Kokkos::finalize();
    return 0;
}
```

---

## Step 3: Build and Run

Compile your application with CMake:

```bash
mkdir -p build && cd build
cmake .. -DKokkos_ENABLE_CUDA=ON  # or -DKokkos_ENABLE_OPENMP=ON for CPU multi-threading
make -j
./mkpp_app
```

---

## Next Steps

- Learn how to define custom kinetics with the [How-To: Create Custom Reactions](../how-to/create-custom-reactions.md) guide.
- Learn how to compile and run discrete adjoint models with the [How-To: Compile & Run Adjoint and TLM Solvers](../how-to/compile-adjoint-and-tlm-solvers.md) guide.
- Review CLI options and function signatures in the [AOT Solver C++ & CLI API Reference](../reference/aot-solver-api.md).
- Review reaction rate laws and parameters in the [Reaction Types & YAML Schema Reference](../reference/reaction-types-and-yaml-schema.md).
- Explore the [Solver Comparison Benchmarks](benchmark-mkpp-vs-micm.md) guide to benchmark accuracy and performance.
- Read the [Complete End-to-End MKPP Architecture & Compiler Pipeline](../explanation/mkpp-end-to-end-architecture.md) for a complete system walkthrough.
- Visit the [MKPP Documentation Index](../README.md) to explore all Diátaxis documentation.
