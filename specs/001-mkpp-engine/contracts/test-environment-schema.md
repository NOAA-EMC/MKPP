# Test Environment Contract

## Purpose

The test-environment file provides the compiler with the initial conditions and forcing data required to validate a mechanism during AOT compilation.

## Accepted Formats

- YAML: `.yaml` or `.yml`
- JSON: `.json`

## Required Fields

| Field | Type | Notes |
|---|---|---|
| name | string | Human-readable identifier for the validation case. |
| initial_conditions | object | Species concentrations and state variables. |
| meteorology | object | Temperature, pressure, humidity, and similar fields. |
| photolysis | object | J-rate inputs or slopes for time interpolation. |
| cloud_liquid_water | number or array | Required for cloud-coupling cases. |

## Optional Fields

| Field | Type | Notes |
|---|---|---|
| bounds | object | Physical or numerical limits used during validation. |
| expected_outputs | object | Optional tolerance-based checks. |
| metadata | object | Provenance or scenario comments. |

## Validation Rules

- All numeric values must be finite.
- Species names in `initial_conditions` must match names declared in the mechanism.
- Array dimensions must be consistent with the mechanism’s solver layout.
- Missing required fields must terminate the compile run before code generation starts.
- Environment files must not require any secrets or private infrastructure identifiers.
### MPI Distribution Rules
In accordance with EE2 HPC constraints (CON-003), the compiler enforcing mechanism validation against host states requires that `gather_to_root` operations are explicitly prohibited to prevent single-node out-of-memory (OOM) failures.

```yaml
mpi:
  gather_to_root: false # MUST ALWAYS BE FALSE
```
