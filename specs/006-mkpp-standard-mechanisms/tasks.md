---
description: "Task list for Standard Mechanisms Validation"
---

# Tasks: Standard Mechanisms Validation

## Phase 1: Translation Utility

- [x] T001 [US1] Create `utils/kpp2openatmos.py` that parses KPP `.eqn` and `.spc` files using regex.
- [x] T002 [US1] Implement mapping logic in `utils/kpp2openatmos.py` to identify ARRHENIUS vs PHOTOLYSIS reactions and structure the output into MICM YAML.

## Phase 2: Generating the Mechanism Library

- [x] T003 [US2] Create the `mechanisms/` directory at the project root.
- [x] T004 [US2] Run `utils/kpp2openatmos.py` on `carbon`, `saprc99`, `saprcnov`, and `small_strato` from the `../KPP/models/` directory and save them to `mechanisms/`.

## Phase 3: Automated Baseline Generation

- [x] T005 [US3] Create `tests/integration/e2e_validation/generate_baselines.py` that wraps the legacy KPP binary, auto-generates a driver similar to the chapman test, compiles it, runs it, and extracts the `.csv` for a given mechanism.
- [x] T006 [US3] Run the baseline generator to create the ground truth data for all 4 mechanisms inside `tests/integration/e2e_validation/data/`.

## Phase 4: Parameterized C++ Testing

- [x] T007 [US3] Create `tests/integration/e2e_validation/test_e2e_mechanisms.cpp` using `testing::TestWithParam<std::string>` to iterate over mechanism names.
- [x] T008 [US3] Configure CMake to loop through the 4 mechanisms, call `mkpp compile` on each, and register the C++ tests and Python comparator tests for each.
