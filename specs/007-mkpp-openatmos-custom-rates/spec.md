# Feature Specification: MKPP OpenAtmos Custom Rate Support (FALL, EP2, EP3)

**Feature Branch**: `feature/017-mkpp-openatmos-custom-rates`
**Created**: 2026-08-01
**Status**: Draft

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Standardized Falloff Reaction Types (Priority: P1)
As a mechanism developer, I want to use standard OpenAtmos (MICM) `TROE` or `TERNARY` reaction types instead of arbitrary `FALL()` macros in the YAML configuration, so that MKPP can parse them canonically and evaluate their partial derivatives in SymPy mathematically correctly.

**Acceptance Scenarios**:
1. **Given** a KPP `FALL` rate in `saprc99.eqn`, **When** the `kpp2openatmos.py` translator runs, **Then** it translates the reaction to a `type: TROE` (or `type: FALLOFF`) reaction in the YAML, mapping `A0, B0, C0, A1, B1, C1, CF` correctly into the `parameters` dictionary.
2. **Given** the translated `saprc99.yaml`, **When** `mkpp compile` runs, **Then** the SymPy lowering step natively handles the `TROE` parameterization, generating the accurate Jacobian entries for all connected species without generating `FALL(...)` text strings.

### User Story 2 - Custom Reaction Type Support (Priority: P2)
As a modeler, I want to define custom reaction types (like `EP2` and `EP3` used by SAPRC) in the OpenAtmos YAML using explicit mathematical expressions or custom type identifiers, so that MKPP can parse and analytically differentiate them without crashing.

**Acceptance Scenarios**:
1. **Given** an `EP2` rate in `saprcnov.eqn`, **When** translated, **Then** it is structured in the YAML either as an explicit mathematical string or a mapped type `CUSTOM_EP2`.
2. **Given** the parsed AST, **When** MKPP calculates the Unified Jacobian, **Then** the SymPy engine analytically applies the chain rule across the custom expression with respect to Temperature and `M_density`.

## Requirements *(mandatory)*
- **FR-001**: The `kpp2openatmos.py` translator MUST identify `FALL(...)` syntax and extract the 7 constituent parameters into a structured OpenAtmos `TROE` definition.
- **FR-002**: The `kpp2openatmos.py` translator MUST identify `EP2(...)` and `EP3(...)` syntax and extract their parameters into a structured OpenAtmos custom formulation.
- **FR-003**: The MKPP lowering engine (`src/mkpp/lowering.py`) MUST implement native SymPy formulation for `TROE` reactions.
- **FR-004**: The MKPP lowering engine MUST implement native SymPy formulation for `EP2` and `EP3` reactions (or allow arbitrary mathematical string evaluation).

## Success Criteria *(mandatory)*
- **SC-001**: `saprc99.yaml` and `saprcnov.yaml` compile via MKPP successfully.
- **SC-002**: The E2E validation pipeline runs on the generated `saprc99.hpp` and exactly matches the legacy KPP analytical outputs within $10^{-12}$ Absolute Tolerance.
