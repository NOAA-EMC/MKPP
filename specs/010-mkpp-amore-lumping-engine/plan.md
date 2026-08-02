# Implementation Plan: MKPP AMORE Lumping Engine

**Branch**: `010-mkpp-amore-lumping-engine` | **Date**: 2026-08-02 | **Spec**: specs/010-mkpp-amore-lumping-engine/spec.md
**Input**: Feature specification from `specs/010-mkpp-amore-lumping-engine/spec.md`

## Summary

Implement the AMORE lumping engine to automatically map explicit VOCs to surrogate classes, collapse redundant reactions, and enforce carbon/mass conservation by generating stoichiometric product multipliers.

## Technical Context

**Language/Version**: Python 3.14 (engine), C++23 (generated headers)
**Primary Dependencies**: SymPy, PyYAML
**Storage**: N/A
**Testing**: pytest (Python), Googletest (C++)
**Target Platform**: HPC (WCOSS, Linux)
**Project Type**: CLI Compiler Module
**Performance Goals**: Generated Kokkos C++ headers must be block-sparse and GPU optimized
**Constraints**: Algebraic mass/carbon conservation is mandatory; fail-fast on errors

## Constitution Check

*GATE: Must pass before proceeding. Re-check after design phase.*

| Principle | Status | Notes |
|-----------|--------|-------|
| Clarity Over Cleverness | PASS | The lumping rules YAML is explicit and readable. |
| Defensive Programming | PASS | The engine validates species existence and weights before proceeding. |
| Fail Fast, Fail Loudly | PASS | CLI will exit immediately if lumping rules are invalid or carbon scaling fails. |
| Algebraic Mass Conservation | PASS | Engine explicitly calculates and applies carbon scaling factors. |
| CI/CD & EE2 Compliance | PASS | E2E integration test ensures solver correctness. |

## Project Structure

### Documentation (this feature)

```text
specs/010-mkpp-amore-lumping-engine/
├── spec.md              # Feature specification
├── plan.md              # This file
├── tasks.md             # Task breakdown
├── research.md          # Research findings
├── data-model.md        # Entities and validation
├── quickstart.md        # Validation guide
└── contracts/
    └── lumping_rules.schema.yaml
```

### Source Code (repository root)

```text
src/
└── mkpp/
    ├── amore.py             # New lumping engine
    ├── cli.py               # CLI modifications for --lump
    └── parser.py            # Hook to inject AMORE before DRGEP

tests/
├── python/
│   └── test_amore.py        # Unit tests for AST collapsing
└── integration/
    └── test_e2e_mechanisms.cpp # E2E Kokkos solver tests
```

**Structure Decision**: The AMORE engine is decoupled into its own module (`amore.py`) to keep the AST transformation logic separate from standard parsing, while CLI modifications provide an explicit entry point.

## Execution Strategy

### TDD Requirements

- [x] `src/mkpp/amore.py`: Complex AST manipulation and reaction collapsing logic requires strict TDD to ensure no equations are malformed and rates are correctly weighted.
- [x] Mass Conservation scaling: Requires tests to prove the C_explicit / C_surrogate scaling factor is accurately computed and injected.

### Parallel Execution Opportunities

- [x] CLI flag parsing and `lumping_rules.yaml` schema validation can be developed independently from the SymPy AST node collapsing logic.

### Human Checkpoints

1. After foundational setup — verify `lumping_rules.yaml` schema and CLI integration.
2. After implementing AST collapsing — verify the generated SymPy AST has correctly merged equations.
3. After mass conservation logic — verify the C++ solver headers are perfectly conservative.
4. Before merge — final review against spec.

### Review Gates

- [x] Lumping rule parsing and validation logic: Review before integrating into the main compilation pipeline.
- [x] AST Collapsing & Rate Averaging: Review by an atmospheric physicist/developer to ensure scientific validity of $A_{eff}$.

