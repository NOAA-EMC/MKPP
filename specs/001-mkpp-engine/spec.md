# Feature Specification: Multiphase KPP (MKPP) Engine

**Feature Branch**: `001-mkpp-engine`

**Created**: 2026-07-31

**Status**: Draft

**Input**: User description: "Implement the feature specification based on the updated constitution. I want to make a phased building of Project Plan: Next-Gen Multiphase Atmospheric Chemistry Solver (Futuristic KPP) V8.md"

## Clarifications
### Session 2026-07-31
- Q: How should the ahead-of-time (AOT) compiler be executed by users or host models? → A: As a standalone CLI tool (e.g., `mkpp compile mech.yaml`) that can be invoked by scientists and build systems.
- Q: How should the Extreme Environment Fuzzer report failures or stiffness during the AOT compilation step? → A: Fail the build with a non-zero exit code and detailed stderr logs.
- Q: How should the host model feed initial condition data and meteorological forcing inputs into the standalone AOT compiler for validation during the build step? → A: Accept a standardized JSON/YAML file containing test environments alongside the mechanism definition.
- Q: How should the auto-generated C++ code handle compiler-specific pragmas or directives that might conflict with Kokkos abstractions? → A: Emit pure Kokkos abstractions and rely entirely on CMake for backend flags.
- Q: To ensure robust testability and independent story delivery, should the standalone AOT CLI tool generate a standalone runner/test-harness along with the C++ headers? → A: Do not generate a test harness; require users to provide their own main application to link the headers.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ahead-Of-Time Mechanism Compilation & Adjoint Generation (Priority: P1)

As a domain atmospheric scientist, I want to define chemical mechanisms in a representation-agnostic format so that the system can automatically generate the optimized solver and necessary adjoint models for data assimilation without requiring me to write manual derivatives.

**Why this priority**: The ahead-of-time compiler is the fundamental engine that shifts overhead from runtime to build-time. All subsequent runtime features depend on the generated solver code.

**Independent Test**: Can be tested by running the compiler CLI on a test mechanism and verifying the generated files (Adjoint/TLM) match expected mathematical precision against finite difference perturbations using an external test application.

**Acceptance Scenarios**:
1. **Given** a mechanism file with gas and aerosol species, **When** passed through the ahead-of-time compiler CLI, **Then** it generates optimized block-sparse solver components using pure Kokkos abstractions.
2. **Given** the generated components, **When** evaluated using Taylor series tests in a host application, **Then** the tangent linear and adjoint models show exact mathematical precision agreement against finite difference perturbations.

---

### User Story 2 - Bidirectional Host Interface & Cloud Coupling (Priority: P1)

As a model developer, I want a bidirectional interface so that the chemical solver can ingest cloud liquid water from the host microphysics module and output optical diagnostics without breaking encapsulation or requiring memory copies.

**Why this priority**: Establishes the core data exchange interface with the host model, which is required for actual runtime integration.

**Independent Test**: Can be tested by compiling the interface and verifying that it successfully translates a dummy chemical state array into valid optical depth values.

**Acceptance Scenarios**:
1. **Given** a chemical state, **When** the optical depth query is called, **Then** it returns the correct optical depth based on the chemical state.
2. **Given** host model arrays, **When** passed through the zero-copy wrapper, **Then** data is accessed without allocating new memory (verified by memory profiling).

---

### User Story 3 - Hierarchical Multi-Rate Solver & Workload Sorting (Priority: P2)

As a performance engineer, I want the host driver to sort grid cells by computational intensity (e.g., Solar Zenith Angle) and partition species into implicit and explicit solvers so that execution threads stay perfectly balanced across day/night boundaries without execution divergence.

**Why this priority**: Solves the critical terminator problem and is necessary for extreme scale performance.

**Independent Test**: Measure wall-clock execution block times comparing sorted vs. unsorted grid cells to verify nighttime idle starvation is reduced by at least 90%.

**Acceptance Scenarios**:
1. **Given** a 3D domain spanning the dawn terminator, **When** the solver integrates the chemistry, **Then** the execution blocks remain load-balanced without starvation.
2. **Given** dynamic photolysis rates, **When** passing through sunrise, **Then** the solver curves gracefully without numerical crashes.

---

### User Story 4 - Aerosol Math & Algebraic Mass Conservation (Priority: P2)

As a scientist, I want the solver to strictly enforce proportional elemental mass conservation and handle prognostic thermodynamics (hysteresis) without rigid conditional branches so that the model maintains long-term stability and continuous differentiability.

**Why this priority**: Ensures scientific hygiene, numerical stability, and strict elemental conservation as demanded by the Constitution.

**Independent Test**: Track physical size distribution during heavy condensation events and verify mass successfully transitions across physical boundaries without trapped mass.

**Acceptance Scenarios**:
1. **Given** a chemical reaction micro-block solve, **When** it completes, **Then** a zero-overhead algebraic projection step strictly enforces elemental mass conservation.
2. **Given** thermodynamic hysteresis (e.g., phase changes), **When** integrated, **Then** the prognostic state variables evolve smoothly without triggering execution divergence.

---

### Edge Cases

- What happens when extremely stiff atmospheric events (like smoke plumes) cause the explicit solver to crash? (Extreme Environment Fuzzer handles this ahead-of-time, failing the build and emitting stderr logs).
- What happens when photolysis rates spike abruptly at sunrise? (Interpolated photolysis forcing curves gracefully).

## Requirements *(mandatory)*

### Core Constitution Constraints

- **CON-001**: System MUST ensure path sanitization and avoid hardcoded secrets.
- **CON-002**: System MUST guarantee scientific determinism (no unseeded randoms).
- **CON-003**: System MUST NOT gather multidimensional grid data onto a single root rank.
- **CON-004**: System MUST evaluate kinetics without operator splitting (Unified formulation).

### Functional Requirements

- **FR-001**: System MUST provide an ahead-of-time compiler via a standalone CLI tool to process representation-agnostic mechanism definitions.
- **FR-002**: System MUST generate optimized solvers utilizing pure Kokkos block-sparse operations (no raw OpenMP/OpenACC pragmas).
- **FR-003**: System MUST generate analytical Adjoint and Tangent Linear Models for Data Assimilation.
- **FR-004**: System MUST implement a bidirectional interface to translate chemical state arrays into physical/optical diagnostics.
- **FR-005**: System MUST provide a zero-copy interoperability wrapper for the host model.
- **FR-006**: System MUST enforce elemental mass conservation via a proportional algebraic projection step.
- **FR-007**: System MUST replace rigid thermodynamic thresholds with continuous differentiable transition curves.
- **FR-008**: System MUST fail compilation (non-zero exit code and stderr log) if the Extreme Environment Fuzzer detects unresolvable stiffness.
- **FR-009**: System MUST accept a standardized JSON/YAML file containing test environments alongside the mechanism definition for AOT validation.

### Key Entities

- **Mechanism Definition**: The human-readable and representation-agnostic definition of chemical species, phases, and reactions.
- **Test Environment Definition**: A standardized JSON/YAML file containing initial conditions and meteorological forcing inputs for AOT validation.
- **Unified Solver**: The single, branchless integration matrix fusing gas kinetics, photolysis, and aerosol phase-transfers.
- **Bidirectional Interface**: The API that connects chemistry arrays with host model physics (cloud liquid water and optical diagnostics).
- **Zero-Copy Wrapper**: The interface that maps host memory arrays into the solver without copying.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Adjoint/TLM Validity: Tangent linear and adjoint models demonstrate agreement against finite difference perturbations with absolute error <= 1e-12 and relative error <= 1e-8 over the validation state vector.
- **SC-002**: Dawn Accuracy: Max Relative Error < 0.1% and zero negative radical concentrations when compared to baseline solvers across the dawn terminator.
- **SC-003**: Aerosol Growth Spectrum: Mass successfully transitions across representation boundaries with zero trapped mass.
- **SC-004**: Hardware Limits: Profiling of the solver using NVIDIA Nsight Compute (ncu) shows the core integration kernel operates with <= 64 registers per thread and zero local memory spilling.
- **SC-005**: Memory Efficiency: Memory layout performance achieves > 80% utilization of theoretical device memory bandwidth.
- **SC-006**: Terminator Load Balance: Nighttime idle starvation is reduced by ≥ 90% via workload sorting.

## Assumptions

- Assumes the host environment provides the required meteorology and cloud liquid water arrays.
- Assumes the host model is capable of calling C-compatible interfaces.
- Assumes target hardware is available and appropriately configured in the build environment.
