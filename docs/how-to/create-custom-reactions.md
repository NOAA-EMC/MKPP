# How-To Guide: Create Custom Reactions in MKPP

This guide explains how to define custom reactions in mechanism YAML files, configure custom rate expressions, and extend the MKPP Python lowering engine for new reaction rate laws.

---

## 1. Defining Reactions in an OpenAtmos Mechanism

All chemical mechanisms in MKPP are declared as OpenAtmos JSON documents under `mechanisms/openatmos/` (for example, `mechanisms/openatmos/saprc99/mechanism.json`).

### Basic Reaction Structure

```yaml
reactions:
  - type: ARRHENIUS
    reactants:
      NO: 1.0
      O3: 1.0
    products:
      NO2: 1.0
      O2: 1.0
    parameters:
      A: 1.8e-12
      B: 0.0
      C: -1370.0
```

---

## 2. Using Custom SymPy Rate Expressions

For reaction kinetics that do not match standard Arrhenius or Troe rate laws, you can define custom rate expressions directly in YAML using SymPy-parseable math strings.

### Example: Custom Temperature-Dependent Expression

```yaml
reactions:
  - type: CUSTOM
    reactants:
      OH: 1.0
      CO: 1.0
    products:
      HO2: 1.0
      CO2: 1.0
    parameters:
      rate_expression: "1.5e-13 * (1.0 + 0.6 * Press / 101325.0)"
```

Available environmental driver symbols in custom rate expressions:

- `Temp`: Temperature $[K]$.
- `Press`: Pressure $[Pa]$.
- `M_density` / `cair`: Air density $[\text{molec/cm}^3]$.
- `S_a`: Aerosol surface area density $[m^2/m^3]$.
- `v_gas`: Thermal velocity $[m/s]$.

---

## 3. Creating Multiphase Aerosol Condensation Reactions

To create phase-transfer reactions that move mass between gas and aerosol phases, set reactant/product species with matching phase declarations:

```yaml
species:
  - name: HNO3
    phase: gas
  - name: NO3_aero
    phase: aerosol

reactions:
  - type: HETEROGENEOUS
    reactants:
      HNO3: 1.0
    products:
      NO3_aero: 1.0
    parameters:
      gamma: 0.1
```

*Note*: Heterogeneous phase reactions automatically couple gas-phase loss ($\frac{d[\text{HNO3}]}{dt} = -k_{\text{het}} [\text{HNO3}]$) and aerosol production ($\frac{d[\text{NO3\_aero}]}{dt} = +k_{\text{het}} [\text{HNO3}]$) in the Unified Jacobian state vector without requiring operator splitting.

---

## 4. Extending the Python Lowering Engine for New Reaction Types

If you are developing a new chemical rate law (e.g. specialized photolysis parameterization or surface reaction model), follow these steps to add native AOT compiler support in Python:

### Step 1: Add Reaction Type in `src/mkpp/model.py`

Update `ReactionDefinition` or enumerations if necessary:

```python
# src/mkpp/model.py
class ReactionDefinition:
    reaction_type: str  # e.g., ARRHENIUS, PHOTOLYSIS, TROE, MY_CUSTOM_TYPE
```

### Step 2: Implement Rate Symbolic Translation in `src/mkpp/lowering.py`

Open `src/mkpp/lowering.py` and locate `prepare_unified_jacobian()`. Add a new `elif` branch for your reaction type:

```python
# src/mkpp/lowering.py
elif rtype == "MY_CUSTOM_TYPE":
    # Parse parameters from YAML dictionary p = r.parameters
    A = parse_sym_or_val(p["A"])
    beta = parse_sym_or_val(p.get("beta", 1.0))

    # Form SymPy symbolic rate expression
    flux = A * (Temp / 300.0)**beta
```

### Step 3: Add Validation Rules in `src/mkpp/validation.py`

Ensure required parameters are checked during mechanism compilation:

```python
# src/mkpp/validation.py
if r.reaction_type.upper() == "MY_CUSTOM_TYPE":
    if "A" not in r.parameters:
        raise ValueError(f"MY_CUSTOM_TYPE reaction requires 'A' parameter.")
```

### Step 4: Recompile Mechanism & Verify

Test your new reaction type by compiling a mechanism header:

```bash
python -m mkpp.cli compile mechanisms/openatmos/my_mechanism/mechanism.json --out mkpp-generated/
```

Verify that `mkpp-generated/my_mechanism.hpp` contains the unrolled C++ rate and Jacobian expressions.

---

## Related Documents

- [Reaction Kinetics & Unified Jacobian Explanation](../explanation/unified-jacobian-and-reaction-kinetics.md)
- [Reaction Types & YAML Schema Reference](../reference/reaction-types-and-yaml-schema.md)
- [AOT Solver C++ & CLI API Reference](../reference/aot-solver-api.md)
- [How-To: Compile & Run Adjoint and TLM Solvers](compile-adjoint-and-tlm-solvers.md)
- [MKPP Documentation Index](../README.md)
