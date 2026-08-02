# Feature Specification: MKPP Diagnostic Reporting & Mechanism Graphs

**Feature Branch**: `feature/019-mkpp-diagnostic-reports`
**Created**: 2026-08-01
**Status**: Draft

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Visual Graph Generation (Priority: P1)
As a domain scientist, I want the compiler to generate visual network graphs (e.g., PNG/SVG) of the chemical mechanism, so that I can visually inspect the species reaction pathways and identify central hubs (like $OH$ or $O_3$).

**Acceptance Scenarios**:
1. **Given** a mechanism file, **When** compiled with the `--report` flag, **Then** MKPP outputs a `network_graph.png` highlighting species nodes and reaction edges.

### User Story 2 - Stiffness & Performance Diagnostics (Priority: P1)
As an HPC engineer, I want the compiler to automatically analyze the mechanism and output a list of potentially problematic reactions (e.g., highly stiff reactions, termolecular reactions, or those with extreme rate constants), so I can proactively tune the numerical integration tolerances.

**Acceptance Scenarios**:
1. **Given** the compile process, **When** `--report` is triggered, **Then** the generated report flags specific reactions that may slow down the GPU implicit solver (e.g., identifying the most dense rows in the Jacobian).

### User Story 3 - Comprehensive Markdown Report (Priority: P1)
As a project maintainer, I want a full-blown Markdown report generated alongside the C++ headers, summarizing the DRGEP reduction statistics, total species/reaction counts, and identified analytical mass conservation balances.

**Acceptance Scenarios**:
1. **Given** a successful compile, **When** `--report` is active, **Then** `report.md` is emitted in the output directory containing all diagnostics, graph links, and solver statistics.

## Requirements *(mandatory)*
- **FR-001**: MKPP must accept a `--report` CLI flag in `src/mkpp/cli.py`.
- **FR-002**: A `src/mkpp/reporting.py` module MUST be created to handle report generation.
- **FR-003**: The reporting module MUST use `networkx` and `matplotlib` to plot and save the reaction network graph.
- **FR-004**: The reporting module MUST analyze the Jacobian sparsity to identify the most heavily coupled species (densest rows/columns) and flag them.
- **FR-005**: A formatted `report.md` MUST be written to the output directory combining all insights.

## Success Criteria *(mandatory)*
- **SC-001**: Running `.venv/bin/mkpp compile mechanisms/chapman.yaml --out build/chapman --report` successfully writes `report.md` and `network.png`.
- **SC-002**: The markdown report explicitly identifies which species act as network hubs.
