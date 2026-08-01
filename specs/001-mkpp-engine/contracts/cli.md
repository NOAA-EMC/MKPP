# MKPP CLI Contract

## Command

```text
mkpp compile <mechanism.{yaml,yml,json}> --test-env <environment.{yaml,yml,json}> --out <output-dir> [--strict] [--emit-manifest]
```

## Inputs

- `mechanism.{yaml,yml,json}`: the mechanism definition that declares species, phases, reactions, and units.
- `environment.{yaml,yml,json}`: the standardized test-environment file used for AOT validation.
- `--out <output-dir>`: writable directory where generated headers and reports are written.
- `--strict`: fail on unsupported or ambiguous schema features instead of trying to coerce them.
- `--emit-manifest`: write a machine-readable artifact manifest alongside generated headers.

## Outputs

- Generated C++ headers for the solver and adjoint/TLM artifacts.
- A deterministic manifest that records emitted artifact names and their source inputs.
- Stderr diagnostics for validation failures or stiffness detection.

## Exit Codes

- `0`: compilation and validation succeeded.
- `1`: validation failed, unsupported chemistry was detected, or stiffness could not be resolved.
- `2`: CLI usage error, missing path, or unreadable input file.

## Behavioral Guarantees

- The command must not mutate the input mechanism or test-environment files.
- The command must sanitize any path-derived output names before writing files.
- The command must produce deterministic output for identical inputs and configuration.
- The command must fail loudly with useful stderr output when the fuzzer or schema checks reject the input.