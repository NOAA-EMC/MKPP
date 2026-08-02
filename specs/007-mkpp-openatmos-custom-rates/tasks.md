---
description: "Task list for MKPP OpenAtmos Custom Rate Support"
---

# Tasks: MKPP OpenAtmos Custom Rate Support

## Phase 1: Mechanism Translation
- [x] T001 Update `utils/kpp2openatmos.py` to parse `FALL(...)` and emit `type: TROE` with parameters `k0_A`, `k0_B`, `k0_C`, `kinf_A`, `kinf_B`, `kinf_C`, and `Fc`.
- [x] T002 Update `utils/kpp2openatmos.py` to parse `EP2(...)` and `EP3(...)` and emit corresponding types.
- [x] T003 Re-run the translator on `saprc99` and `saprcnov` to update `mechanisms/`.

## Phase 2: AST Mathematical Expansion
- [x] T004 Add new types (`TROE`, `EP2`, `EP3`) to validation schemas in `src/mkpp/model.py`.
- [x] T005 Implement the analytical mathematical definitions for `TROE`, `EP2`, and `EP3` in `src/mkpp/lowering.py` using SymPy so that the Jacobian derives cleanly.

## Phase 3: Parity Re-validation
- [x] T006 Recompile `saprc99.yaml` and `saprcnov.yaml` into headers.
- [x] T007 Add `saprc99` and `saprcnov` to the E2E parameter list in `tests/integration/e2e_validation/CMakeLists.txt`.
- [x] T008 Run `ninja e2e_saprc99_runner e2e_saprcnov_runner` and assert 1e-12 parity for their complex Jacobians.
