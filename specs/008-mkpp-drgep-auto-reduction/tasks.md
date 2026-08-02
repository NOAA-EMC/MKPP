---
description: "Task list for MKPP DRGEP Auto-Reduction"
---

# Tasks: MKPP DRGEP Auto-Reduction

## Phase 1: CLI and Framework
- [x] T001 [US2] Update `src/mkpp/cli.py` to add `--enable-drgep` (boolean flag) and `--drgep-threshold` (float, default 0.05).
- [x] T002 [US2] Update `src/mkpp/codegen.py` to optionally append `_full` or `_reduced` to the output file names based on a `suffix` parameter in `generate_headers(mech, out_dir, suffix="")`.

## Phase 2: DRGEP Logic
- [x] T003 [US1] Create `src/mkpp/reduction.py` and implement `reduce_mechanism_drgep(mech, threshold)` using `networkx` to build a directed graph between species based on reaction connectivity.
- [x] T004 [US1] Implement graph pruning in `reduce_mechanism_drgep`: Remove species with 0 out-degree or below-threshold connectivity weights.
- [x] T005 [US1] Implement reaction pruning in `reduce_mechanism_drgep`: Drop any reaction from `mech.reactions` where all participating species were pruned.

## Phase 3: Integration
- [x] T006 [US2] Update `src/mkpp/cli.py` `run_compiler` to execute the dual-pipeline if `--enable-drgep` is True.
- [x] T007 Run `.venv/bin/mkpp compile mechanisms/saprc99.yaml --test-env tests/integration/e2e_validation/data/env.yaml --out build/mkpp-generated --enable-drgep` and verify two differing headers are generated!
