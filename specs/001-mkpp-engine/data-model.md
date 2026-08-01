# Data Model: MKPP Engine

## Entities

### MechanismDefinition

Represents the author-authored chemistry mechanism input.

| Field | Type | Notes |
|---|---|---|
| name | string | Human-readable mechanism identifier. |
| description | string | Freeform summary of the chemistry set. |
| aerosol_representation | AerosolRepresentation | Defines bulk/bin/modal/sectional lowering behavior. |
| species | list[SpeciesDefinition] | All gas, aerosol, and aqueous species. |
| phases | list[PhaseDefinition] | Phase membership and solver ownership. |
| reactions | list[ReactionDefinition] | All kinetic, photolysis, heterogeneous, and aqueous reactions. |
| units | UnitSystem | Canonical units or conversion mode. |
| metadata | map[string, string] | Optional provenance and comments. |

### TestEnvironmentDefinition

Represents the structured validation environment that accompanies a mechanism.

| Field | Type | Notes |
|---|---|---|
| name | string | Identifier for the validation case. |
| initial_conditions | map[string, number] | Species concentrations and state variables. |
| meteorology | map[string, number] | Temperature, pressure, humidity, and related forcing. |
| photolysis | map[string, number] | J-rates or slope-based forcing inputs. |
| cloud_liquid_water | number or array | Required for cloud coupling validation. |
| bounds | map[string, range] | Physical and numerical guardrails. |
| expected_outputs | map[string, number] | Optional validation targets or tolerances. |

### SpeciesDefinition

| Field | Type | Notes |
|---|---|---|
| name | string | Unique species name. |
| phase | string | gas, aerosol, aqueous, or mixed. |
| elements | map[string, integer] | Stoichiometric elemental counts. |
| role | string | Optional solver role such as radical, precursor, or tracer. |

### PhaseDefinition

| Field | Type | Notes |
|---|---|---|
| name | string | Phase identifier. |
| solver_mode | string | implicit, explicit, or coupled. |
| transport_model | string | Optional representation-specific transport behavior. |
| continuity_model | string | Continuous transition law for hysteresis or phase change. |

### ReactionDefinition

| Field | Type | Notes |
|---|---|---|
| type | string | kinetic, photolysis, heterogeneous, aqueous, condensation, or projection. |
| reactants | list[string] | Species identifiers consumed by the reaction. |
| products | list[string] | Species identifiers produced by the reaction. |
| rate_expression | string | Symbolic or numeric expression for the rate. |
| unit_policy | string | Canonical unit handling for the rate law. |
| stiff | boolean | Marks reactions that belong in the implicit block. |
| continuous_transition | boolean | Marks reactions modeled with smooth transition functions. |

### GeneratedArtifact

| Field | Type | Notes |
|---|---|---|
| kind | string | header, manifest, diagnostics, or report. |
| path | string | Relative output path. |
| checksum | string | Optional deterministic artifact fingerprint. |
| dependencies | list[string] | Inputs used to produce the artifact. |

## Relationships

- A `MechanismDefinition` owns many `SpeciesDefinition`, `PhaseDefinition`, and `ReactionDefinition` records.
- A `TestEnvironmentDefinition` is validated against exactly one `MechanismDefinition` per compilation run.
- A compilation run produces one or more `GeneratedArtifact` records, including runtime headers and machine-readable manifests.
- The lowering pipeline partitions `ReactionDefinition` entries into deterministic solver blocks before code generation.

## Validation Rules

- Mechanism names must be non-empty and filesystem-safe when mapped into output paths.
- Species names must be unique within a mechanism.
- Reaction references must point only to declared species.
- Every phase-specific species must belong to a declared phase.
- The test-environment file must provide the fields required by the mechanism’s active reaction types, especially photolysis and cloud-coupling inputs when those reactions exist.
- Any unsupported or unresolvable stiffness case must terminate compilation with a non-zero exit code and a diagnostic message on stderr.

## State Transitions

1. **Loaded**: raw YAML/JSON has been read from disk.
2. **Parsed**: raw data has been converted into typed in-memory entities.
3. **Validated**: schema, reference, and physical checks have passed.
4. **Lowered**: the mechanism has been partitioned into solver blocks and symbolic forms.
5. **Generated**: headers, manifests, and reports have been written to disk.
6. **Failed**: validation or lowering terminated the run early with diagnostics.