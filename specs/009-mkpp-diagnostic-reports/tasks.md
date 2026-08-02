---
description: "Task list for MKPP Diagnostic Reporting"
---

# Tasks: MKPP Diagnostic Reporting

## Phase 1: Environment & Setup
- [x] T001 Add `matplotlib` to `pyproject.toml` and reinstall into the `.venv`.
- [x] T002 Update `src/mkpp/cli.py` to add `--report` flag.

## Phase 2: Graph Visualization
- [x] T003 Create `src/mkpp/reporting.py` with `generate_network_graph(mech, out_dir)` using `matplotlib` and `networkx`.

## Phase 3: Diagnostic Analytics
- [x] T004 Implement `analyze_stiffness(mech, sympy_meta)` in `reporting.py` to count non-zeros per row in the analytical Jacobian and flag the top 5 densest species.
- [x] T005 Implement markdown emission `write_report(mech, sympy_meta, out_dir)` combining the graph, reaction breakdown, and stiffness warnings.

## Phase 4: Integration
- [x] T006 Call `write_report` from `cli.py` when `--report` is passed.
- [x] T007 Run the compiler on `chapman.yaml` with `--report` and visually inspect the output directory.
