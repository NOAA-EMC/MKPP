# Feature Specification: MKPP DRGEP Auto-Reduction

**Feature Branch**: `feature/018-mkpp-drgep-auto-reduction`
**Created**: 2026-08-01
**Status**: Draft

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Directed Graph Generation & Thresholding (Priority: P1)
As a computational chemist, I want MKPP to automatically generate a Direct Relation Graph (DRG) measuring the normalized production/destruction dependency weights between every species pair, so that it can identify which species are irrelevant to the core chemical evolution.

**Acceptance Scenarios**:
1. **Given** a heavily detailed mechanism (like SAPRC99 with 80+ species), **When** compiled with `--drgep-threshold 0.05`, **Then** the AOT compiler mathematically prunes species whose dependency weights fall below $5\%$.

### User Story 2 - Dual-Output Header Generation (Priority: P1)
As a systems engineer, I want the compiler to automatically emit both a `full` reference solver and a `reduced` highly pruned solver, so that I can benchmark the stripped mechanism without running two separate compilation pipelines.

**Acceptance Scenarios**:
1. **Given** the compile command, **When** `--enable-drgep` is provided, **Then** `codegen.py` writes `{mech.name}_full.hpp` and `{mech.name}_reduced.hpp`.
2. **Given** the generated headers, **When** evaluated, **Then** the `reduced` header contains a physically smaller State View extent, a smaller `NUM_SPECIES` parameter, and entirely omits pruned reactions from the Jacobian AST.

## Requirements *(mandatory)*
- **FR-001**: MKPP must accept `--enable-drgep` and `--drgep-threshold <float>` CLI arguments in `src/mkpp/cli.py`.
- **FR-002**: `src/mkpp/lowering.py` must contain a `reduce_mechanism()` function using `networkx` to calculate the DRGEP interaction coefficients $r_{AB}$.
- **FR-003**: The reduction step must prune reactions where all reactant species fall below the DRGEP threshold.
- **FR-004**: The code generator must loop twice when reduction is enabled, writing `_full` and `_reduced` variants.

## Success Criteria *(mandatory)*
- **SC-001**: A large mechanism (like `saprc99.yaml`) successfully produces two physically different C++ headers.
- **SC-002**: `saprc99_reduced.hpp` has fewer species (`NUM_SPECIES`) and smaller AST Jacobians than `saprc99_full.hpp`.
