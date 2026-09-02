---
type: reference
category: reference
tags: [python, api, box-model, scipy, mkpp.box]
---

# Box Model Python API Reference (`mkpp.box`)

The `mkpp.box` module provides a zero-dimensional chemical box model built on the
same SymPy lowering pipeline as the AOT Kokkos code generator. It numerically
lambdifies the Unified Jacobian and rate vector and integrates them with SciPy.

For a task-oriented walkthrough, see
[How-To: Run a Chemical Box Model in Python](../../how-to/run-box-model-in-python.md).

## `BoxModel`

::: mkpp.box.BoxModel
    options:
        members:
            - set_initial_concentrations
            - set_photolysis
            - set_external_rate
            - set_emissions
            - set_first_order_loss
            - simulate
        show_root_heading: true

## `BoxModelResult`

::: mkpp.box.BoxModelResult
    options:
        members:
            - concentrations
            - final
            - to_dataframe
        show_root_heading: true
