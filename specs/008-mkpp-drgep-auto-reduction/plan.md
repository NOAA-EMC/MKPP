# Implementation Plan: MKPP DRGEP Auto-Reduction

**Branch**: `feature/018-mkpp-drgep-auto-reduction` | **Date**: 2026-08-01 | **Spec**: [spec.md](spec.md)

## Summary
Implement the Direct Relation Graph with Error Propagation (DRGEP) auto-reduction strategy natively inside MKPP's AST engine. Using `NetworkX` directed graphs, we will evaluate the inter-species reaction connectivity weights. Any species (and subsequently, any associated reactions) that fall below a user-provided interaction threshold will be mathematically pruned from the abstract syntax tree *before* C++ generation occurs.

## Technical Context
**Language/Version**: Python 3.14 (MKPP core), NetworkX (Graph Analysis)
**Constraints**: 
- **Constitution**: The reduced mechanism must be mathematically sound (will not break the `KOKKOS_INLINE_FUNCTION` syntax or the Mass Conservation projections).

## Project Structure
```text
src/
└── mkpp/
    ├── cli.py            # Add --enable-drgep and --drgep-threshold flags
    ├── reduction.py      # NEW: Implement `reduce_mechanism_drgep()` logic
    └── codegen.py        # Update loop to dump two headers
```

## Execution Strategy
1. Extend `cli.py` to parse the new optional arguments.
2. Build the DRGEP NetworkX graph builder in a new `reduction.py` module.
3. Update `cli.py` compilation orchestrator to conditionally branch: if reduction is enabled, compile the full mechanism, deepcopy it, run the reducer, then compile the reduced mechanism.
