---
type: reference
category: reference
tags: [reactions, openatmos, schema, yaml, mkpp]
---

# Reference: Reaction Types, Parameters, and OpenAtmos YAML Schema

This document provides a reference for all reaction types, parameter definitions, OpenAtmos YAML schema rules, species phase modes, and host model coupling interfaces supported by the Multiphase Kinetic PreProcessor (MKPP).

---

## 1. Mechanism Specification YAML Schema

A mechanism YAML file consists of top-level metadata, species declarations, phase modes, reaction list definitions, and host interface configurations:

```yaml
name: mechanism_identifier
description: Detailed description of chemical mechanism
metadata:
  rate_units: kinetic # kinetic (default) | SI
species:
  - name: SpeciesName
    phase: gas # gas | aerosol | aqueous
    role: variable # variable | fixed
    elements:
      C: 2
      H: 6

phases:
  - name: gas
    solver_mode: explicit

reactions:
  - type: REACTION_TYPE
    reactants:
      SpeciesA: 1.0
      SpeciesB: 1.0
    products:
      SpeciesC: 1.0
    parameters:
      # Type-specific rate parameters
```

---

### Mechanism Rate Units

`metadata.rate_units` declares the source concentration units of stored mechanism rate coefficients. The accepted values are `kinetic` and `SI`, case-insensitively. If omitted, the mechanism uses `kinetic`, preserving the legacy convention. An SI declaration converts supported coefficients to the kinetic basis during parsing, before symbolic lowering; it does not change generated solver interfaces.

For an evaluated coefficient multiplying concentration order $m$, MKPP converts SI to kinetic units using:

$$
k_{\mathrm{kinetic}} = k_{\mathrm{SI}} \left(\frac{N_A}{10^6}\right)^{1-m},
\qquad \frac{N_A}{10^6} = 6.02214076 \times 10^{17}.
$$

| Rate family | Coefficient | Effective concentration order |
|---|---|---|
| `ARRHENIUS` | `A` | Sum of listed reactant exponents |
| `TROE` / `FALLOFF` | low-pressure `k0.A` | Listed reactant order plus one for `[M]` |
| `TROE` / `FALLOFF` | high-pressure `kinf.A` | Listed reactant order |
| `EP2` | `A0`, `A2` | Listed reactant order |
| `EP2` | `A3` | Listed reactant order plus one for `[M]` |
| `EP3` | `A1` | Listed reactant order |
| `EP3` | `A2` | Listed reactant order plus one for `[M]` |

Temperature parameters and falloff broadening factors are unchanged. SI conversion requires finite numeric coefficients and nonnegative integral reactant exponents. Unsupported rate forms, including `TUNNELING`, and symbolic coefficients whose units cannot be determined are rejected before code generation with reaction context; a mechanism is never partially converted.

Runtime concentrations, number densities (including `AIR`/`M`), emissions, temperature, photolysis values, and externally supplied `Rate_n` values remain in MKPP's existing kinetic basis. `PHOTOLYSIS`, `PHASE_CHANGE`, `USER_DEFINED`, and the current `SURFACE` lowering path use runtime forcings and are not coefficient-converted. `HETEROGENEOUS.gamma` is dimensionless and is not rescaled.

Example SI declaration:

```yaml
metadata:
  rate_units: SI
```

---

## 2. Species Declarations

Each species entry defines physical phase, solver variable mode, and elemental stoichiometry.

| Property | Type | Options | Description |
| :--- | :--- | :--- | :--- |
| `name` | string | Valid identifier (e.g., `O3`, `NO2`, `SO4_aero`) | Unique species identifier |
| `phase` | string | `gas`, `aerosol`, `aqueous` | Physical state phase for Unified Jacobian coupling |
| `role` | string | `variable` (default), `fixed` | `fixed` species have constant background concentration ($dC/dt = 0$) |
| `elements` | dict | `{ElementSymbol: integer}` | Elemental stoichiometry for mass balance verification (e.g. `{C: 2, H: 6}`) |

---

## 3. Supported Reaction Types & OpenAtmos YAML Examples

### 3.1 `ARRHENIUS`
Standard and modified Arrhenius reaction rate laws for gas-phase kinetics, aligned with MICM parameter sign conventions.

- **Formula**: $k(T) = A \cdot \left(\frac{T}{300}\right)^B \cdot \exp\left(\frac{C}{T}\right)$
- **Parameters**:
  - `A` (*float*, required): Pre-exponential factor $[\text{cm}^3/\text{molec/s}$ or $1/\text{s}]$.
  - `B` (*float*, optional, default `0.0`): Temperature exponent $n$.
  - `C` (*float*, optional, default `0.0`): Activation energy parameter $-E_a / R$ $[K]$ (matching MICM's sign convention).

#### OpenAtmos YAML Entry
```yaml
reactions:
  - type: ARRHENIUS
    reactants:
      DMS: 1.0
      OH: 1.0
    products:
      SO2: 1.0
    parameters:
      A: 1.2e-11
      B: 0.0
      C: -260.0
```

- **Explanation**: $A$ sets the collision frequency factor, $B$ accounts for non-exponential temperature scaling, and $C$ represents $-E_a / R$. MKPP lowers this to $k(T) = 1.2 \times 10^{-11} \cdot (T / 300)^0 \cdot \exp(-260 / T)$.

---

### 3.2 `TROE` / `FALLOFF`
Pressure-dependent termolecular association reactions with low and high pressure limit falloff parameterization.

- **Formula**:
  $$k_0(T) = A_0 \left(\frac{T}{300}\right)^{B_0} \exp\left(-\frac{C_0}{T}\right) \cdot [M]$$
  $$k_\infty(T) = A_\infty \left(\frac{T}{300}\right)^{B_\infty} \exp\left(-\frac{C_\infty}{T}\right)$$
  $$k(T, M) = \left(\frac{k_0}{1 + k_0/k_\infty}\right) \cdot F_c^{\frac{1}{1 + \left(\log_{10}(k_0/k_\infty)\right)^2}}$$
- **Parameters**:
  - `k0`: `{A: float, B: float, C: float}` (Low-pressure limit parameters)
  - `kinf`: `{A: float, B: float, C: float}` (High-pressure limit parameters)
  - `Fc` (*float*, optional, default `0.6`): Falloff broadening factor.

#### OpenAtmos YAML Entry
```yaml
reactions:
  - type: TROE
    reactants:
      NO2: 1.0
      NO3: 1.0
    products:
      N2O5: 1.0
    parameters:
      k0:
        A: 2.0e-30
        B: -3.0
        C: 0.0
      kinf:
        A: 1.4e-12
        B: 0.1
        C: 0.0
      Fc: 0.6
```

- **Explanation**: Models association reactions that exhibit unimolecular falloff behavior between low-density ($k_0$) and high-density ($k_\infty$) limits. $F_c$ accounts for collisional energy transfer efficiency. MKPP automatically multiplies $k_0$ by ambient air density $[M]$.

---

### 3.3 `PHOTOLYSIS`
Photolytic reaction rate laws driven by ambient solar irradiance.

- **Formula**: $R = J_{\text{photo}} \cdot \prod_{j} [C_j]^{s_{j}}$
- **Parameters**:
  - `A` (*float* or *string*, required): Base photolysis rate coefficient $J_0$ $[1/\text{s}]$ or photolysis reaction name identifier.

#### OpenAtmos YAML Entry
```yaml
reactions:
  - type: PHOTOLYSIS
    reactants:
      NO2: 1.0
    products:
      NO: 1.0
      O: 1.0
    parameters:
      A: J_NO2
    continuous_transition: true
```

- **Explanation**: Parameter `A` specifies a $J$-value identifier (`J_NO2`) dynamically populated at runtime by radiation models (e.g. Cloud-J / Fast-JX) or passed via the high-level host model API `mkpp_set_photolysis_ptrs`.

---

### 3.4 `EP2`
Specialized 3-parameter termolecular rate law.

- **Formula**: $k(T) = K_0 + \frac{K_3 \cdot [M]}{1 + K_3 \cdot [M] / K_2}$ where $K_i = A_i \exp(-C_i / T)$.
- **Parameters**: `A0`, `C0`, `A2`, `C2`, `A3`, `C3`.

#### OpenAtmos YAML Entry
```yaml
reactions:
  - type: EP2
    reactants:
      HNO3: 1.0
      OH: 1.0
    products:
      NO3: 1.0
      H2O: 1.0
    parameters:
      A0: 2.4e-14
      C0: -460.0
      A2: 2.7e-17
      C2: -2199.0
      A3: 6.5e-34
      C3: -1335.0
```

- **Explanation**: IUPAC/JPL rate law representing reactions (such as $\text{HNO}_3 + \text{OH}$) containing both direct bimolecular channels ($K_0$) and third-body energy-transfer association channels ($K_2, K_3$).

---

### 3.5 `EP3`
Specialized 2-parameter termolecular rate law with total air density dependence.

- **Formula**: $k(T, M) = K_1 + K_2 \cdot [M]$ where $K_i = A_i \exp(-C_i / T)$.
- **Parameters**: `A1`, `C1`, `A2`, `C2`.

#### OpenAtmos YAML Entry
```yaml
reactions:
  - type: EP3
    reactants:
      HO2: 1.0
      HO2: 1.0
    products:
      H2O2: 1.0
      O2: 1.0
    parameters:
      A1: 2.3e-13
      C1: -600.0
      A2: 1.7e-33
      C2: -1000.0
```

- **Explanation**: Used for radical self-reactions (such as $\text{HO}_2 + \text{HO}_2$) featuring a bimolecular channel ($K_1$) supplemented by a collisionally-assisted channel ($K_2 \cdot [M]$).

---

### 3.6 `HETEROGENEOUS`
Gas-to-aerosol particle surface uptake rate laws.

- **Formula**: $k_{\text{het}} = \frac{1}{4} \cdot \gamma \cdot v_{\text{gas}} \cdot S_a$
- **Parameters**:
  - `gamma` (*float*, required): Mass accommodation / surface reaction uptake coefficient $\gamma \in [0, 1]$.
  - `activation_trigger` (*string*, optional): Conditional meteorological trigger (e.g., `meteo.cloud_liquid_water > 1.0e-6`).

#### OpenAtmos YAML Entry
```yaml
reactions:
  - type: HETEROGENEOUS
    reactants:
      SO2: 1.0
      DUST1: 1.0
    products:
      SO4: 1.0
      DUST1: 1.0
    parameters:
      gamma: 0.0001
    activation_trigger: "meteo.cloud_liquid_water > 1.0e-6"
    continuous_transition: true
```

- **Explanation**: Represents gas molecule collisions and reaction on aerosol particle surface area density $S_a$. `gamma` ($\gamma$) is the uptake probability per surface collision.

---

### 3.7 `EQUILIBRIUM`
Inorganic aerosol thermodynamic equilibrium partitioning system (e.g. $\text{NH}_4/\text{NO}_3/\text{SO}_4$ gas-aerosol partitioning). Replaces deprecated discrete phase change blocks with smooth, C¹-continuous thermodynamic equilibrium curves.

- **Formula**:
  Evaluates temperature-dependent van 't Hoff equilibrium constants $K_p(T) = A \cdot \exp\left(-\frac{\Delta H}{R} \left(\frac{1}{T} - \frac{1}{T_{\text{ref}}}\right)\right)$ and applies continuous sigmoid regime blending across sulfate ratio regimes ($R = \frac{[\text{Total NH}_3]}{[\text{Total SO}_4]}$).

- **Parameters**:
  - `system` (*string*): Thermodynamic system identifier (e.g., `NH4_NO3_SO4`).
  - `total_species` (*dict*): Mapping of reduced nitrogen, oxidized nitrogen, and sulfate gas/aerosol species lists.
  - `regime_blending` (*string*): Blending function type (`sigmoid` or `hermite`).
  - `transition_width` (*float*): Blending transition width parameter (default: `0.05`).
  - `equilibrium_constants` (*dict*): Temperature dependence parameters (`A`, `dH`, `Tref`) for $K_p$ constants (`Kp_NH4NO3`, `Kp_NH4HSO4`, `Kp_NH42SO4`).

#### OpenAtmos YAML Entry
```yaml
reactions:
  - type: EQUILIBRIUM
    system: NH4_NO3_SO4
    total_species:
      reduced_nitrogen:
        gas: NH3
        aerosol: [NH4a]
      oxidized_nitrogen:
        gas: HNO3
        aerosol: [NO3an1, NO3an2, NO3an3]
      sulfate:
        gas: SO2
        aerosol: [SO4]
    regime_blending: sigmoid
    transition_width: 0.05
    equilibrium_constants:
      Kp_NH4NO3: { A: 4.39e-17, dH: -74735.0, Tref: 298.15 }
      Kp_NH4HSO4: { A: 1.086e-2, dH: -40000.0, Tref: 298.15 }
      Kp_NH42SO4: { A: 1.817e-25, dH: -160000.0, Tref: 298.15 }
```

- **Explanation**: Evaluates analytical equilibrium gas/aerosol distribution without discrete conditional branches, avoiding GPU thread divergence and gradient cliffs.

---

### 3.8 `PHASE_CHANGE` / `CONDENSATION` (Deprecated)
Direct kinetic phase transfer between gas, aerosol, and aqueous species.

- **Formula**: $R = k_{\text{cond}} \cdot (C_{\text{gas}} - C_{\text{sat}})$

#### OpenAtmos YAML Entry
```yaml
reactions:
  - type: PHASE_CHANGE
    reactants:
      NH3: 1.0
      HNO3: 1.0
    products:
      NH4NO3_aero: 1.0
    parameters:
      rate_expression: "1.0e-4 * (C_NH3 * C_HNO3 - Kp_NH4NO3)"
```

- **Explanation**: Legacy phase change rate specification. *Note*: Users should migrate inorganic gas-aerosol partitioning reactions to `EQUILIBRIUM` using `mkpp compile --migrate-equilibrium`.

---

### 3.9 `CUSTOM` / `TUNNELING`
User-defined SymPy math expressions for custom rate laws.

- **Parameters**:
  - `rate_expression` (*string*): Valid SymPy-parseable math string using variables `Temp`, `Press`, `M_density`, `cair`, `S_a`, `v_gas`.

#### OpenAtmos YAML Entry
```yaml
reactions:
  - type: CUSTOM
    reactants:
      O3: 1.0
      OH: 1.0
    products:
      HO2: 1.0
      O2: 1.0
    parameters:
      rate_expression: "1.6e-12 * exp(-940.0 / Temp)"
```

- **Explanation**: Allows arbitrary analytical rate laws referencing physical variables (`Temp`, `Press`, `M_density`, `cair`, `S_a`, `v_gas`).

---

## 4. CF Metadata for Multiphase States

Generated solvers emit variables conforming to standard Climate and Forecast (CF) metadata conventions:

| Variable Name | Standard Name | Long Name | Units | Phase |
| :--- | :--- | :--- | :--- | :--- |
| `C_gas` | `mole_fraction_of_gas_phase_species_in_air` | Gas Phase Concentration | $\text{molec/cm}^3$ | Gas |
| `C_aerosol` | `mass_concentration_of_aerosol_species_in_air` | Aerosol Particle Concentration | $\text{molec/cm}^3$ or $\mu\text{g/m}^3$ | Aerosol |
| `C_aqueous` | `mass_concentration_of_aqueous_species_in_cloud_water` | Aqueous Phase Concentration | $\text{molec/cm}^3$ | Aqueous |
| `temp` | `air_temperature` | Temperature | $K$ | Driver |
| `press` | `air_pressure` | Pressure | $Pa$ | Driver |
| `S_a` | `aerosol_surface_area_density` | Aerosol Surface Area | $m^2/m^3$ | Driver |

---

## 5. High-Level Host Model Integration

To generate C, C++, and Fortran host model interface headers alongside Kokkos C++ solvers, pass the `--host-api` flag to MKPP:

```bash
python -m mkpp generate --mechanism mechanism.yaml --out-dir src/solvers --host-api
```

For detailed multi-language host integration instructions, refer to [How-To: Host Model Integration](../how-to/host_model_integration.md).

---

## Related Documents

- [How-To: Host Model Integration](../how-to/host_model_integration.md)
- [AOT Solver C++ and Host API Reference](aot-solver-api.md)
- [Reaction Kinetics & Unified Jacobian Explanation](../explanation/unified-jacobian-and-reaction-kinetics.md)
- [How-To: Create Custom Reactions](../how-to/create-custom-reactions.md)
