# Feature Specification: MKPP Standard Mechanisms Validation

**Feature Branch**: `feature/016-mkpp-standard-mechanisms`
**Created**: 2026-08-01
**Status**: Draft

**Input**: User description: "Convert standard KPP mechanisms (small_strato, carbon, saprc99, saprcnov) into OpenAtmos format inside a new mechanisms directory. Create a parameterized E2E validation pipeline that tests these MKPP generated headers and solvers against the legacy KPP output for full numerical parity."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Mechanism Translation Utility (Priority: P1)
As an atmospheric scientist migrating from legacy KPP, I want a utility that automatically translates legacy KPP `.eqn` and `.spc` files into compliant OpenAtmos (MICM) YAML format, so that I can easily port my existing chemical mechanisms without manual error-prone translation.

**Acceptance Scenarios**:
1. **Given** the standard `saprc99.eqn` and `saprc99.spc` files, **When** processed by the translator utility, **Then** a valid `saprc99.yaml` is produced that successfully parses through `mkpp compile` without schema errors.
2. **Given** any rate expression containing arbitrary Arrhenius coefficients or photolysis rates, **When** translated, **Then** the parameters map correctly to the OpenAtmos `parameters` dictionary.

### User Story 2 - Standard Mechanisms Library (Priority: P1)
As a project maintainer, I want all standard KPP models (`small_strato`, `carbon`, `saprc99`, `saprcnov`) available as OpenAtmos YAML files within a central `mechanisms/` directory, so they can be easily distributed and used as benchmark cases.

**Acceptance Scenarios**:
1. **Given** the `mechanisms/` repository directory, **When** inspected, **Then** it contains the OpenAtmos versions of the target legacy mechanisms.

### User Story 3 - Parameterized E2E Parity Testing (Priority: P1)
As an HPC operations engineer, I want the E2E validation suite to automatically loop over all mechanisms in the `mechanisms/` directory, so that I have guaranteed proof that MKPP achieves 100% numerical parity (Jacobian values and ROS2 integration) against legacy KPP across highly stiff, large-scale systems (like SAPRC99).

**Acceptance Scenarios**:
1. **Given** the E2E CTest suite, **When** `ctest -R E2E_Mechanisms` is executed, **Then** the suite iteratively compiles MKPP headers for each mechanism, evaluates the built-in solvers, and asserts RMSE < 1e-6 against automatically generated legacy KPP baseline data.

## Requirements *(mandatory)*
- **FR-001**: A Python script (`utils/kpp2openatmos.py`) MUST be created to parse KPP syntax and emit MICM/OpenAtmos YAML.
- **FR-002**: The MKPP repository MUST include a `mechanisms/` directory hosting the translated mechanisms.
- **FR-003**: The E2E GoogleTest and CMake configuration MUST be refactored to support parameterized test generation or looping over the mechanisms directory.
- **FR-004**: An automated baseline generator script MUST execute the legacy KPP binary to generate the `.csv` truth data for each test mechanism dynamically or during CI setup.

## Success Criteria *(mandatory)*
- **SC-001**: `saprc99.yaml`, `saprcnov.yaml`, `carbon.yaml`, and `small_strato.yaml` successfully pass MKPP strict validation.
- **SC-002**: The integration suite proves exact Jacobian sparsity mapping, Jacobian value parity (ATOL 1e-12), and ROS2 final concentration parity (RTOL 1e-6) for all listed mechanisms simultaneously.
