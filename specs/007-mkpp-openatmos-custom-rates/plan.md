# Implementation Plan: MKPP OpenAtmos Custom Rate Support

## Summary
To achieve full parity across the complex SAPRC mechanisms, we must extend MKPP's parsing and SymPy evaluation layers to natively support non-Arrhenius reactions (Troe falloff curves `FALL`, and empirical fits `EP2`/`EP3`). We will update the KPP translator to map these onto specialized YAML definitions, then inject SymPy symbolic algebra for those explicit definitions so the AOT compiler derives the Jacobian correctly.

## Execution Strategy
1. **Translator Update (`utils/kpp2openatmos.py`)**: Parse `FALL`, `EP2`, and `EP3` and emit `type: TROE`, `type: EP2`, and `type: EP3` respectively.
2. **Schema Update (`src/mkpp/model.py`)**: Register these new types.
3. **AST Expansion (`src/mkpp/lowering.py`)**: Define the exact explicit mathematical formulas using `sp.Symbol` and `sp.exp` for these reaction types so `f_vector.jacobian(c_vector)` expands correctly.
4. **Validation**: Re-run the CMake integration loop.
