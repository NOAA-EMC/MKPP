# Implementation Plan: MKPP Diagnostic Reporting

**Branch**: `feature/019-mkpp-diagnostic-reports` | **Date**: 2026-08-01 | **Spec**: [spec.md](spec.md)

## Summary
Add a `--report` capability to the MKPP compiler that performs offline, ahead-of-time topological and mathematical analysis on the provided chemical mechanism. It will utilize `matplotlib` and `networkx` to visualize the stiff species interactions, and output a comprehensive `report.md` outlining computational bottlenecks (dense Jacobian rows, highly stiff/termolecular equations) so that HPC engineers can tune their tolerances or mechanisms beforehand.

## Technical Context
**Language/Version**: Python 3.14
**Primary Dependencies**: `matplotlib` (NEW), `networkx`
**Output**: `report.md`, `network_graph.png`

## Project Structure
```text
src/
└── mkpp/
    ├── cli.py             # Add --report flag
    └── reporting.py       # NEW: Implements report generation
```

## Execution Strategy
1. **Dependency Addition**: Ensure `matplotlib` is added to the virtual environment for plotting.
2. **Analysis Pipeline**: Inside `reporting.py`, process the `Mech` object and `sympy_metadata` (the analytical Jacobian) to extract the most heavily coupled species.
3. **Graphing**: Plot the directed acyclic components using NetworkX's Spring or Kamada-Kawai layout to separate stiff from explicit clusters visually.
