# Phase 0: Research & Clarifications

## 1. Effective Rate Expression Weighting ($A_{eff}$)
- **Context**: User Story 1 requires collapsing explicit reactions into a single equation and computing a concentration-weighted average of the Arrhenius rate constants.
- **Decision**: The `lumping_rules.yaml` must specify steady-state or reference concentrations (or weights) for the explicit VOCs being lumped. Alternatively, weights can be parsed from a standard atmospheric reference state profile. For this iteration, we will require explicit weights in the `lumping_rules.yaml`.
- **Rationale**: Atmospheric mechanism reduction (like AMORE) relies on expected partitioning among explicit species (e.g., Ethane vs Propane in an urban environment). Without reference weights, an average is scientifically invalid.
- **Alternatives considered**: Unweighted averaging (rejected due to violation of scientific hygiene / physical accuracy constraints).

## 2. Automatic Carbon & Mass Conservation (Scaling Factors)
- **Context**: User Story 2 requires automatically appending a carbon-scaling factor to surrogate product yields.
- **Decision**: The engine will parse the number of Carbon atoms from the species definitions (e.g., `species_saprc99.yaml` or whatever is loaded by the compiler). If the species formula isn't available, the engine will fail fast. The factor will be computed as `C_explicit / C_surrogate`.
- **Rationale**: Ensures algebraic mass conservation (a strict requirement in the master guidelines).
- **Alternatives considered**: Requiring manual scaling factors in the YAML (rejected because User Story 2 explicitly requests "automated" generation).

## 3. CLI Integration of `--lump` Flag
- **Context**: User Story 3 requires `--lump rules.yaml` to trigger AMORE instead of DRGEP.
- **Decision**: Modify the compiler entry point (e.g., `src/mkpp/__main__.py` or CLI module) to accept `--lump <filepath>`. When this is present, it will initialize the AMORE engine and bypass the DRGEP auto-reduction module. 
- **Rationale**: Clean separation of concerns; provides an explicit opt-in for graph lumping.
- **Alternatives considered**: Implicit lumping if the file exists (rejected due to "Fail Fast, Fail Loudly" and explicitness principles).
