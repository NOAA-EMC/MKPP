# MKPP Quickstart

## Prerequisites

- Python 3.11 environment configured for the repository.
- A CMake/Ninja toolchain available for the native runtime subproject under `src/exaero/`.
- A mechanism file and matching test-environment file that conform to the contracts in `contracts/cli.md` and `contracts/test-environment-schema.md`.

## Validation Workflow

1. Run the compiler against a mechanism and test environment that satisfy the published contract.

```bash
python -m mkpp compile <mechanism.{yaml,yml,json}> --test-env <environment.{yaml,yml,json}> --out build/mkpp-generated --emit-manifest
```

Expected outcome:

- The command exits with status `0`.
- Generated Kokkos C++ headers appear in `build/mkpp-generated/`.
- A manifest file records the emitted artifacts and their source inputs.

2. Build the native runtime consumer that will include the generated headers.

```bash
cmake -S src/exaero -B build/exaero -G Ninja
cmake --build build/exaero
```

Expected outcome:

- The native runtime configuration succeeds with Kokkos available.
- The build completes without requiring compiler-specific pragmas in generated headers.

3. Run the native test suite.

```bash
ctest --test-dir build/exaero --output-on-failure
```

Expected outcome:

- The unit, fuzz, and Fortran interoperability tests pass.
- Any invalid mechanism or unsupported stiffness case fails loudly with stderr diagnostics rather than producing silent fallback behavior.

## What to Verify

- The generated headers are deterministic when the same mechanism and environment inputs are compiled twice.
- The compiler rejects invalid or incomplete test-environment files before writing output.
- The runtime consumer can ingest the emitted headers without additional manual patching.