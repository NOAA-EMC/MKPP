# Implementation Plan: MKPP Standard Mechanisms Validation

**Branch**: `feature/016-mkpp-standard-mechanisms` | **Date**: 2026-08-01 | **Spec**: [spec.md](spec.md)

## Summary
Develop a KPP-to-OpenAtmos translation utility to convert legacy `.eqn` and `.spc` files into the YAML configurations required by MKPP. Translate the standard atmospheric mechanisms (`small_strato`, `carbon`, `saprc99`, `saprcnov`) into a new `mechanisms/` library. Finally, upgrade the existing E2E validation pipeline to automatically parameterize and verify all translated mechanisms against legacy KPP execution baselines to guarantee 100% numerical parity across varying chemical stiffness levels.

## Technical Context
**Language/Version**: Python 3.14 (Translator, Baseline Gen, PyTest), C++23 (Harness)
**Primary Dependencies**: MKPP, GoogleTest, Legacy KPP Binary
**Project Type**: Translation Utility & Automated Benchmarking

## Constitution Check
| Principle | Status | Notes |
|-----------|--------|-------|
| Test-First | PASS | We are directly creating an automated benchmark framework to prevent mathematical regressions. |
| CON-001 / CON-002 | PASS | The parameterized test suite will reuse the Exaero-style 0-byte Kokkos layouts verified in the Chapman test. |

## Project Structure
```text
mechanisms/
├── carbon.yaml
├── saprc99.yaml
├── saprcnov.yaml
└── small_strato.yaml

utils/
└── kpp2openatmos.py

tests/integration/e2e_validation/
├── generate_baselines.py        # Automates calling legacy KPP
└── test_e2e_mechanisms.cpp      # Parameterized GTest runner
```

## Execution Strategy
### Human Checkpoints
1. After translation, visually verify `saprc99.yaml` correctly extracted rate equations.
2. Review the GoogleTest parameterized instantiation to ensure it correctly loops over mechanisms.
