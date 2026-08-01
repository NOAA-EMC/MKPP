# Research Notes: MKPP Engine

## Decision 1: Compiler frontend stays in Python 3.11

- **Decision:** Implement the AOT compiler as a Python 3.11 CLI package under `src/mkpp/`.
- **Rationale:** The spec already describes an AOT Python frontend, and the repository root already carries Python tooling via `pyproject.toml` and `environment.yml`. Keeping the compiler in Python makes symbolic lowering, YAML/JSON parsing, and deterministic validation easier to evolve than a native-only implementation.
- **Alternatives considered:** A native C++ compiler frontend would reduce language count but would duplicate symbolic and schema-heavy logic in a harder-to-maintain layer. A notebook or script-only prototype would be too brittle for the CLI contract the spec requires.

## Decision 2: YAML remains the canonical mechanism input

- **Decision:** Accept YAML as the primary mechanism authoring format, while also accepting JSON where needed for automation and the test-environment contract.
- **Rationale:** The spec repeatedly names YAML for mechanism definitions and JSON/YAML for test environments. YAML is the better authoring format for domain scientists, and JSON compatibility keeps automated environments simple.
- **Alternatives considered:** JSON-only input would simplify parsing but would be less ergonomic for large chemical mechanisms. A custom DSL would be more expressive but would create an unnecessary grammar and parser burden.

## Decision 3: Generated runtime code remains pure Kokkos C++

- **Decision:** Emit C++ headers that use only Kokkos abstractions and normal CMake backend flags; do not emit compiler-specific pragmas.
- **Rationale:** The spec explicitly requires pure Kokkos abstractions and the repository already uses Kokkos in native code. Keeping the generated code portable protects downstream builds and avoids backend-specific source divergence.
- **Alternatives considered:** Emitting OpenMP/OpenACC pragmas would make the code more directly tied to some compilers but would violate the architectural constraint and complicate portability.

## Decision 4: Validation is split between pytest and ctest

- **Decision:** Use pytest for the compiler frontend and ctest for the native runtime integration surface.
- **Rationale:** The compiler’s logic is data-shaping and schema-heavy, which is well suited to Python unit tests. The runtime consumer already has CMake and CTest scaffolding, so end-to-end checks belong there.
- **Alternatives considered:** A single test framework for everything would be simpler on paper but would either ignore the native runtime or force Python into the CMake test path unnecessarily.

## Decision 5: The test-environment contract is a first-class artifact

- **Decision:** Treat the standardized JSON/YAML test-environment file as a documented contract, not an ad hoc CLI argument bag.
- **Rationale:** The spec requires the compiler to accept test environments alongside the mechanism definition, and the data needed for validation is structured. A contract document keeps that structure explicit and stable.
- **Alternatives considered:** Passing environment values as CLI flags would be simpler for a prototype but would not scale to realistic atmospheric cases or preserve reproducibility.