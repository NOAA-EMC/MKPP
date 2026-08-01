# MKPP Engine Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a standalone MKPP compiler CLI that ingests representation-agnostic mechanism definitions plus a standardized test-environment file, validates them deterministically, and emits Kokkos-based C++ headers plus adjoint/TLM artifacts for downstream host integration.

**Architecture:** The new compiler frontend lives in a dedicated Python package under `src/mkpp/` and owns parsing, validation, lowering, and code generation. It emits stable header artifacts that are consumed by the existing C++/Fortran runtime areas under `src/exaero/`, while the validation story is split between Python unit tests and the existing CMake/CTest integration surface.

**Tech Stack:** Python 3.11, YAML/JSON parsing, SymPy, Jinja2 or structured text emission, C++20, Kokkos, CMake 3.24, Ninja, pytest, ctest.

## Global Constraints

- `System MUST ensure path sanitization and avoid hardcoded secrets.`
- `System MUST guarantee scientific determinism (no unseeded randoms).`
- `System MUST NOT gather multidimensional grid data onto a single root rank.`
- `System MUST evaluate kinetics without operator splitting (Unified formulation).`
- `System MUST provide an ahead-of-time compiler via a standalone CLI tool to process representation-agnostic mechanism definitions.`
- `System MUST generate optimized solvers utilizing pure Kokkos block-sparse operations (no raw OpenMP/OpenACC pragmas).`
- `System MUST generate analytical Adjoint and Tangent Linear Models for Data Assimilation.`
- `System MUST implement a bidirectional interface to translate chemical state arrays into physical/optical diagnostics.`
- `System MUST provide a zero-copy interoperability wrapper for the host model.`
- `System MUST enforce elemental mass conservation via a proportional algebraic projection step.`
- `System MUST replace rigid thermodynamic thresholds with continuous differentiable transition curves.`
- `System MUST fail compilation (non-zero exit code and stderr log) if the Extreme Environment Fuzzer detects unresolvable stiffness.`
- `System MUST accept a standardized JSON/YAML file containing test environments alongside the mechanism definition for AOT validation.`

## Summary

MKPP is implemented as a compile-time pipeline: parse the mechanism and test-environment inputs, build an internal reaction/species graph, partition the solver into deterministic blocks, and emit Kokkos-friendly C++ headers plus the validation metadata needed by host models and downstream tests. The runtime-facing integration remains isolated in the existing C++/Fortran surfaces so the compiler can evolve independently while still producing artifacts those surfaces can consume.

## Technical Context

**Language/Version**: Python 3.11 for the compiler frontend; C++20 for generated/runtime integration; Fortran remains part of the surrounding runtime test surface.
**Primary Dependencies**: SymPy for symbolic lowering, YAML/JSON parsing for mechanism and test-environment files, Kokkos for generated solver backends, CMake/Ninja for native builds.
**Storage**: File-based inputs and outputs only; mechanism definitions, test-environment definitions, generated headers, and reports are all filesystem artifacts.
**Testing**: pytest for compiler behavior and schema validation; ctest for C++/Fortran integration in the runtime subproject.
**Target Platform**: Linux HPC targets for runtime, with macOS developer support already present in the workspace; compiler and docs must stay portable.
**Project Type**: Mixed CLI compiler plus native library/runtime integration.
**Performance Goals**: Deterministic builds, zero-copy host integration, no root-rank aggregation, and generated kernels that stay within Kokkos/device register constraints.
**Constraints**: No operator splitting, pure Kokkos abstractions only in generated code, strict path sanitization, non-zero exit on stiffness failure, and stable CLI outputs suitable for automation.

## Constitution Check

*GATE: Must pass before proceeding. Re-check after design phase.*

| Principle | Status | Notes |
|-----------|--------|-------|
| Clarity Over Cleverness | PASS | The plan uses a dedicated compiler package, explicit contracts, and separate validation artifacts instead of a monolith. |
| Defensive Programming | PASS | Input validation, schema checks, and deterministic failure handling are first-class tasks. |
| Fail Fast, Fail Loudly | PASS | The fuzzer path and CLI validation are specified to fail with non-zero exit codes and stderr diagnostics. |
| High-Performance HPC & MPI | PASS | The plan preserves distributed-friendly constraints and avoids root-rank aggregation. |
| GPU Acceleration & Kokkos | PASS | Generated code is constrained to pure Kokkos abstractions and block-sparse lowering. |
| Zero-Copy Data Interoperability | PASS | The runtime contract preserves layout and unmanaged view semantics for host integration. |
| Scientific Hygiene & Determinism | PASS | The compiler output and validation path are specified to be deterministic and branch-stable. |

## Project Structure

### Documentation (this feature)

```text
specs/001-mkpp-engine/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
└── contracts/
    ├── cli.md
    └── test-environment-schema.md
```

### Source Code (repository root)

```text
src/
├── mkpp/
│   ├── __init__.py
│   ├── cli.py
│   ├── parser.py
│   ├── model.py
│   ├── validation.py
│   ├── lowering.py
│   └── codegen.py
└── exaero/
    ├── src/
    └── tests/

tests/
└── python/
    ├── test_cli.py
    ├── test_validation.py
    └── test_codegen.py
```

**Structure Decision**: Keep the compiler frontend in a standalone Python package under `src/mkpp/` so parsing and code generation can move quickly without disturbing the native runtime. Preserve `src/exaero/` as the downstream consumer of generated artifacts, because that is already the repository’s closest native integration surface and already carries CMake/CTest scaffolding.

## Execution Strategy

### TDD Requirements (MANDATORY)

*Per Constitution EE2 Compliance, these test gates MUST pass before implementation is considered complete.*

- [ ] `src/mkpp/parser.py` and `src/mkpp/validation.py`: strict schema parsing and failure modes need red-green coverage because malformed inputs must fail deterministically.
- [ ] `src/mkpp/codegen.py`: emitted header text and metadata must be asserted byte-for-byte or structure-for-structure to prevent accidental drift.
- [ ] `src/mkpp/cli.py`: command-line behavior, exit codes, and stderr text need coverage because the CLI is the user entrypoint.

### Parallel Execution Opportunities

- [ ] Input schema validation and code generation can proceed in parallel once the shared dataclasses in `src/mkpp/model.py` are defined.
- [ ] CLI wiring and quickstart/documentation updates can proceed in parallel after the contract files stabilize.
- [ ] Runtime integration checks under `src/exaero/tests/` can be prepared independently of the Python package internals once the generated artifact layout is fixed.

### Human Checkpoints

1. After the parser and schema contract are defined, verify the accepted mechanism/test-environment formats against the spec.
2. After lowering and code generation are defined, verify the emitted artifact layout is compatible with the native runtime consumer.
3. After the validation strategy is defined, verify the failure modes are explicit and deterministic.
4. Before implementation begins, confirm the quickstart commands reflect the actual build and test entrypoints.

### Review Gates

- [ ] `src/mkpp/cli.py` and `contracts/cli.md`: review before any downstream consumer code is written.
- [ ] `src/mkpp/model.py` and `data-model.md`: review before lowering logic is implemented.
- [ ] `src/mkpp/codegen.py` and `contracts/test-environment-schema.md`: review before any runtime integration or test harness wiring.

## Complexity Tracking

> No constitution violations are expected for this plan, so no complexity exceptions are required.
