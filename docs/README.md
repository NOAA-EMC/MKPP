# MKPP Documentation

Welcome to the documentation for the **Multiphase Kinetic PreProcessor (MKPP)**.

Our documentation follows the **Diátaxis framework**, organizing information into four distinct categories based on user needs:

```
                  LEARNING-ORIENTED
                          │
            Tutorials     │    Explanation
                          │
PRACTICAL ────────────────┼──────────────── THEORETICAL
                          │
          How-To Guides   │    Reference
                          │
                   WORK-ORIENTED
```

---

## 🎓 1. Tutorials (Learning-Oriented)
Step-by-step lessons for newcomers to learn MKPP through hands-on practice.

* **[AOT Solver Quickstart Tutorial](tutorials/aot-solver-quickstart.md)**
  * Learn how to generate, compile, and execute an Ahead-Of-Time (AOT) Kokkos chemical ODE solver header from a mechanism YAML file.

---

## 🛠️ 2. How-To Guides (Problem-Oriented)
Practical step-by-step guides for solving specific real-world tasks.

* **[Create Custom Reactions](how-to/create-custom-reactions.md)**
  * Define custom kinetics, SymPy math rate expressions, multiphase aerosol condensation, and extend the Python lowering engine.
* **[Run a Box Model in Python](how-to/run-box-model-in-python.md)**
  * Integrate any OpenAtmos mechanism as a 0-D chemical box model directly in Python with SciPy — no C++ compilation required.
* **[Solver Comparison Benchmarks](tutorials/benchmark-mkpp-vs-micm.md)**
  * Execute numerical accuracy verification against legacy Fortran KPP, run 24-hour diurnal cycle benchmarks, and profile GPU register usage.
* **[Compile & Run Adjoint and TLM Solvers](how-to/compile-adjoint-and-tlm-solvers.md)**
  * Generate discrete adjoint and Tangent-Linear Model (TLM) solvers using `--adjoint` for JEDI 4D-Var data assimilation workflows.

---

## 📖 3. Reference (Information-Oriented)
Technical descriptions of APIs, CLI flags, configuration schema, and data structures.

* **[AOT Kokkos Solver C++ & CLI API Reference](reference/aot-solver-api.md)**
  * Complete reference for `mkpp compile` CLI options, generated C++ solver signatures (`compute_rates`, `compute_jacobian`, `integrate`), and Adjoint/TLM interfaces (`CheckpointBuffer`, `integrate_adj`).
* **[Reaction Types, Parameters, and YAML Schema Reference](reference/reaction-types-and-yaml-schema.md)**
  * Detailed specification of YAML mechanism schema, species declarations, reaction types (`ARRHENIUS`, `TROE`, `PHOTOLYSIS`, `HETEROGENEOUS`, `EQUILIBRIUM`, `CUSTOM`), and CF metadata conventions.

---

## 💡 4. Explanation (Understanding-Oriented)
Deep-dive discussions on theoretical foundations, architectural design, and trade-offs.

* **[Complete End-to-End MKPP Architecture & Compiler Pipeline](explanation/mkpp-end-to-end-architecture.md)**
  * Comprehensive walkthrough of the 6-stage compiler pipeline, from mechanism ingestion to Kokkos HPC runtime execution.
* **[Ahead-Of-Time (AOT) Symbolic LU Solver Architecture](explanation/aot-symbolic-lu-architecture.md)**
  * Rationale behind zero-loop symbolic unrolling, RCM bandwidth reduction, pure scalar register mapping (0 bytes local stack), and stage loop fusion.
* **[Reaction Kinetics, Multiphase Aerosols, and Unified Jacobian](explanation/unified-jacobian-and-reaction-kinetics.md)**
  * Mathematical formulations of rate laws, operator-splitting elimination via unified state vectors, and SymPy analytical Jacobian and Adjoint derivations.
