# Feature Specification: MKPP AMORE Lumping Engine

**Feature Branch**: `feature/020-mkpp-amore-lumping-engine`
**Created**: 2026-08-02
**Status**: Draft

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Mechanism Surrogating & Reaction Merging (Priority: P1)
As a mechanism developer handling the Master Chemical Mechanism (MCM), I want MKPP to ingest a `lumping_rules.yaml` file defining how explicit VOCs map to surrogate classes (e.g., `ALK1 = Ethane + Propane`), so that the compiler automatically collapses redundant explicit reactions into a single flux-weighted proxy reaction.

**Acceptance Scenarios**:
1. **Given** an explicit mechanism and a lumping specification mapping 5 explicit alkanes to `ALK_SURR`, **When** the compiler runs, **Then** the emitted `_reduced.yaml` contains only `ALK_SURR` and collapses all $OH$ abstraction reactions into a single equation.
2. **Given** the collapsed reaction, **When** evaluated, **Then** the surrogate reaction rate $k_{surr}$ is the concentration-weighted average of the explicit Arrhenius rate constants.

### User Story 2 - Automated Carbon & Mass Conservation (Priority: P1)
As an atmospheric physicist, I want the lumping engine to automatically generate stoichiometric product multipliers to ensure that collapsing heavy explicit species into lighter surrogates does not violate algebraic carbon or oxygen mass conservation within the solver.

**Acceptance Scenarios**:
1. **Given** a lumping from an explicit $C_5$ species to a $C_3$ surrogate, **When** the products are emitted, **Then** a carbon-scaling factor (e.g., $5/3$) is automatically appended to the surrogate product yield.

### User Story 3 - Replacement of Destructive DRGEP (Priority: P1)
As a user of MKPP, I want to use the `--lump` flag in the CLI to trigger AMORE-style safe reduction instead of relying on the destructive `--enable-drgep` flag which dangerously drops boundary species like `SO2` and `ISOPRENE`.

**Acceptance Scenarios**:
1. **Given** the CLI command `mkpp compile --lump rules.yaml`, **When** executed, **Then** MKPP bypasses DRGEP degree-pruning and applies AMORE graph lumping instead.

## Requirements *(mandatory)*
- **FR-001**: A new `src/mkpp/amore.py` module MUST be created to perform Abstract Syntax Tree (AST) node collapsing based on a YAML definition file.
- **FR-002**: The engine MUST parse a `lumping_rules.yaml` that specifies `Target_Surrogate: [Explicit_1, Explicit_2, ...]`.
- **FR-003**: The engine MUST iterate through all mechanism reactions, substituting explicit species with their surrogate targets.
- **FR-004**: If multiple reactions collapse into the exact same reactant/product signature after substitution, the engine MUST merge them and compute a new effective rate expression $A_{eff}$.
- **FR-005**: The engine MUST execute before `prepare_unified_jacobian()` so the SymPy AST natively inherits the lumped system.

## Success Criteria *(mandatory)*
- **SC-001**: Running the AMORE engine on an explicit test mechanism successfully emits a structurally smaller but chemically conservative mechanism representation.
- **SC-002**: The generated `_lumped.hpp` C++ headers successfully compile with `test_e2e_mechanisms.cpp` and evaluate with zero unmapped variables.
