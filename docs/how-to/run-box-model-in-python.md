---
type: howto
category: how_to
tags: [box-model, python, scipy, zero-dimensional, photolysis, chemistry, runtime]
---

# How-To: Run a Chemical Box Model in Python with MKPP

This guide shows how to integrate an OpenAtmos mechanism as a **zero-dimensional
(0-D) chemical box model directly in Python**, with **no C++ compilation step**.
The box model reuses the same SymPy lowering pipeline that produces the Kokkos
AOT solvers (the Unified Jacobian and rate vector), then numerically integrates
the ODE system with SciPy.

Use the box model when you want to:

- Explore or debug a new mechanism quickly from a Python REPL, notebook, or script.
- Generate reference trajectories to validate the compiled AOT solver.
- Run single-grid-cell chemistry studies (e.g. a parcel, a chamber, one model column).

For production grid-cell swarms on CPU/GPU, compile the AOT Kokkos solver instead
(see [AOT Solver Quickstart](../tutorials/aot-solver-quickstart.md) and
[Host Model Integration](host_model_integration.md)).

---

## 1. Prerequisites

Install MKPP in editable mode (the box model pulls in `numpy` and `scipy`):

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
```

Verify the entry point is available:

```bash
mkpp-box --help
```

---

## 2. Quick Start (Chapman Ozone Chemistry)

The shortest working example loads a bundled mechanism, sets initial
concentrations and photolysis rates, and integrates for one hour.

```python
from mkpp.box import BoxModel

box = BoxModel("mechanisms/openatmos/chapman/mechanism.json")
box.set_initial_concentrations({"O": 1.0e10, "O2": 2.0e10, "O3": 3.0e10, "M": 4.0e10})
box.set_photolysis({0: 2.0e-5, 1: 1.0e-3})   # J_0 (O2), J_1 (O3) in s^-1

result = box.simulate(t_end=3600.0, dt_out=60.0)

print(result.final["O3"])            # final ozone concentration
print(result.concentrations["O3"])   # full O3 time series (numpy array)
```

`result` is a `BoxModelResult` carrying the output time grid (`result.t`), the
`(n_species, n_times)` concentration array (`result.y`), and convenience views
`result.concentrations` (dict of time series) and `result.final` (dict of final
values).

### Accuracy

This exact setup reproduces the committed SciPy Radau reference used by the C++
end-to-end validation suite
(`tests/integration/e2e_validation/data/chapman_reference.json`) to a maximum
relative error of about **5e-12**. The box model and the compiled AOT solver are
driven by the *same* lowered SymPy expressions, so they agree to solver tolerance.

---

## 3. Setting Photolysis Rates

Photolysis frequencies (`J`-values, s^-1) can be keyed three ways. All are
equivalent for the Chapman mechanism:

```python
# By photolysis index (declaration order in the mechanism)
box.set_photolysis({0: 2.0e-5, 1: 1.0e-3})

# By "J_<n>" string
box.set_photolysis({"J_0": 2.0e-5, "J_1": 1.0e-3})

# By the name of the photolyzed reactant species
box.set_photolysis({"O2": 2.0e-5, "O3": 1.0e-3})
```

If a species photolyzes in more than one reaction, the name-keyed form raises a
`KeyError` and you must select by `J_<n>` index instead.

---

## 4. Environmental Conditions

Temperature, relative humidity, air density, and pressure are substituted into
the rate laws at construction time (isothermal, constant-pressure box):

```python
box = BoxModel(
    "mechanisms/openatmos/ts1/mechanism.json",
    temperature=298.15,      # K   -> substituted into Arrhenius/Troe rates
    relative_humidity=0.5,   # 0-1 -> substituted into RH (equilibrium systems)
    air_density=2.46e19,     # molec cm^-3 -> M_density fallback third body
    pressure=101325.0,       # Pa
)
```

Species named `M` or `AIR` are treated as fixed background (their tendency is
zero); `air_density` is only used when a mechanism references the generic
`M_density` symbol instead.

---

## 5. Emissions, Deposition, and External Rates

Add simple physical forcing on top of the chemistry without editing the
mechanism:

```python
# Constant emission tendency (molec cm^-3 s^-1)
box.set_emissions({"NO": 1.0e6})

# First-order wall / dry-deposition loss (s^-1): dC/dt -= k * C
box.set_first_order_loss({"O3": 1.0e-4})

# Externally supplied Rate_<n> for PHASE_CHANGE / TUNNELING reactions
# (e.g. a deposition or photostationary flux provided by a host driver)
box.set_external_rate(reaction_index=3, rate=2.5e-2)
```

Emissions and losses are validated against the mechanism's species list and
raise `KeyError` for unknown names.

---

## 6. Choosing an Integrator and Tolerances

`simulate()` forwards to `scipy.integrate.solve_ivp`. Stiff atmospheric chemistry
needs an implicit method; the analytical Jacobian from the Unified Jacobian is
supplied automatically for `Radau` and `BDF`.

```python
result = box.simulate(
    t_end=86400.0,        # one day (s)
    dt_out=3600.0,        # hourly output
    method="Radau",       # Radau (default), BDF, LSODA, or RK45
    rtol=1.0e-8,
    atol=1.0e-10,
)
```

- **`Radau`** (default): robust L-stable choice for stiff mechanisms.
- **`BDF`**: alternative stiff method, also receives the analytical Jacobian.
- **`LSODA` / `RK45`**: for non-stiff or exploratory runs; no Jacobian passed.

You can also pass an explicit output grid with `t_eval=np.array([...])`.

### Working with the result

```python
import matplotlib.pyplot as plt

df = result.to_dataframe()          # requires pandas (optional)
plt.semilogy(result.t / 3600.0, result.concentrations["O3"])
plt.xlabel("time (h)"); plt.ylabel("[O3] (molec cm$^{-3}$)")
plt.show()
```

---

## 7. Running from the Command Line

The `mkpp-box` command runs a mechanism as a box model and prints (or saves) the
trajectory as CSV:

```bash
mkpp-box mechanisms/openatmos/chapman/mechanism.json \
    --t-end 3600 --dt-out 1800 \
    --temp 298.15 --rh 0.5 \
    --conc O=1e10 --conc O2=2e10 --conc O3=3e10 --conc M=4e10 \
    --jval O2=2e-5 --jval O3=1e-3 \
    --method Radau --out chapman_box.csv
```

```text
time_s,O,O2,O3,M
0.000,1.000000e+10,2.000000e+10,3.000000e+10,4.000000e+10
1800.000,1.543013e+09,6.921839e+10,6.735043e+06,4.000000e+10
3600.000,6.433164e+09,6.678342e+10,1.965767e-01,4.000000e+10
```

| Flag | Meaning |
| :--- | :--- |
| `mechanism` | Path to an OpenAtmos YAML/JSON mechanism (positional). |
| `--t-end` | Simulation length in seconds (required). |
| `--dt-out` | Output sampling interval in seconds. |
| `--temp`, `--rh`, `--air-density` | Environmental constants. |
| `--conc SPECIES=VALUE` | Initial concentration (repeatable). |
| `--jval SPECIES_OR_INDEX=VALUE` | Photolysis rate in s^-1 (repeatable). |
| `--method` | `solve_ivp` method (default `Radau`). |
| `--out PATH` | Optional CSV output path. |

---

## 8. Scaling Notes

The box model builds the **full symbolic Jacobian** and lambdifies only its
structurally non-zero entries, so per-step cost scales with Jacobian sparsity,
not density.

- Small mechanisms (Chapman, `small_strato`): build in well under a second,
  integrate a day in a fraction of a second.
- Large mechanisms (TS1, 210 species / 155 runtime parameters): construction
  takes on the order of **10-15 s** (SymPy Jacobian derivation), and stiff
  integration is comparatively slow because the SciPy linear algebra is dense.
  For large mechanisms run over many grid cells or long durations, prefer the
  compiled AOT Kokkos solver.

---

## 9. Troubleshooting

| Symptom | Cause / Fix |
| :--- | :--- |
| `Box model cannot resolve symbol 'X'` | The mechanism references a symbol the box model does not substitute. Supported: `C_<species>`, `J_<n>`, `Rate_<n>`, `Temp`, `RH`, `M_density`, `Press`, `S_a`, `v_gas`. |
| `No initial concentration set for species: [...]` | Every species needs an initial value; pass them all to `set_initial_concentrations`. |
| `KeyError: 'Unknown species'` | A forcing/initial key is not in the mechanism; inspect `box.species`. |
| Integration raises `RuntimeError: ... failed` | Loosen `rtol`/`atol`, reduce `t_end`, switch `method`, or set `max_step`. |
| Slow on a large mechanism | Expected — see [Section 8](#8-scaling-notes); use the compiled AOT solver. |

---

## See Also

- [AOT Solver Quickstart](../tutorials/aot-solver-quickstart.md) — compile and run the Kokkos solver.
- [Create Custom Reactions](create-custom-reactions.md) — author the mechanisms the box model runs.
- [Box Model Python API Reference](../reference/api/box.md) — full `mkpp.box` signatures.
- [Reaction Kinetics & Unified Jacobian](../explanation/unified-jacobian-and-reaction-kinetics.md) — the math the box model evaluates.
