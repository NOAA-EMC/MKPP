---
type: explanation
category: mechanisms
tags: [cracmm2, cmaq, aerosol, catchem, ufs-chem]
---

# CRACMM2 Port: Limitations and Integration TODOs

## Scope and status

MKPP imports a pinned [EPA CRACMM2](https://usepa.github.io/CRACMM/chemistry/README.html)
species and reaction catalog and emits an ahead-of-time solver. This is not yet a
CMAQ-equivalent multiphase implementation or a CAT-Chem/UFS-Chem integration.
CRACMM describes linked gas and particle chemistry, but CMAQ also supplies
thermodynamics, aerosol processes, photolysis, and environment-dependent uptake
rates. A unified kinetic Jacobian does not automatically include processes that
are calculated outside that Jacobian.

The current [importer](../../scripts/import_cracmm2.py) produces 271 species and
531 reactions: 454 ARRHENIUS, 64 UNKNOWN, 11 HETEROGENEOUS, and 2 PHOTOLYSIS.
The catalog has 32 variable aerosol species, but species membership alone does
not establish working gas-particle exchange. The source is pinned as described
in [Compile CRACMM2](../how-to/compile-cracmm2.md). These counts describe the
current imported snapshot, not the full set of CMAQ aerosol processes.

## Immediate correctness blockers

1. **Separate and validate external kinetic rates.** The 64 UNKNOWN and 11
   HETEROGENEOUS entries have named coefficients requiring host calculations.
   [Lowering](../../src/mkpp/lowering.py) creates `Rate_<reaction_index>` for
   them, and [expression formatting](../../src/mkpp/format_eqn.py) maps that
   symbol to `jvals[reaction_index]`. The generated CRACMM2 kernel therefore
   accesses slots such as `jvals[395]`, whereas the
   [host API](../../src/mkpp/templates/host_api/mkpp_c_api.cpp.j2) allocates the
   input using *photolysis count* (2 for this catalog). This can read outside
   the supplied array. Give external rates a distinct, sized, named per-cell
   interface; reject missing or non-finite coefficients before integration.
   Keep photolysis indices separate from reaction indices and document units.

2. **Resolve particle products and CMAQ tracking intermediates.** When a
   reaction references a name missing from the species table, the
   [importer](../../scripts/import_cracmm2.py) adds it as a fixed gas species.
   Thus `AGLYJ`, `AISO3NOSJ`, `ASO4J`, and similar heterogeneous products in
   [the canonical catalog](../../mechanisms/openatmos/cracmm2/mechanism.json)
   are fixed gas entries. [Lowering](../../src/mkpp/lowering.py) does not
   evolve fixed-species products. Define whether each name is a real state,
   a CMAQ bookkeeping intermediate, or a transfer into an aerosol mode; verify
   both reactant loss and particle production, including C/N/S conservation.

3. **Replace the shared CRACMM2 test setup with a mechanism-specific case.**
   The [end-to-end runner](../../tests/integration/e2e_validation/test_e2e_mechanisms.cpp)
   initializes large mechanisms with SAPRC-99-specific species indices and uses
   a 64-element `jvals` buffer. That cannot validate CRACMM2 chemistry and is
   too small for its generated external-rate indices. The
   [catalog test](../../tests/integration/solver_benchmark/test_extended_mechanisms.py)
   checks provenance and counts, not physical rates or aerosol outcomes. Fix
   the rate contract first, then test CRACMM2 with named species and reference
   values from an independently configured CMAQ box case.

## Missing or unconnected physical processes

4. **Inorganic aerosol thermodynamics.** CMAQ CRACMM uses ISORROPIA II for
   equilibrium among sulfate, nitrate, ammonium, chloride, sodium, potassium,
   calcium, magnesium, and aerosol water. The MKPP
   [equilibrium registry](../../src/mkpp/equilibrium/registry.py) has a
   simplified NH4/NO3/SO4 model, not the full
   [ISORROPIA II system](https://acp.copernicus.org/articles/7/4639/2007/).
   The CRACMM2 catalog declares no EQUILIBRIUM reactions invoking even that
   simplified model. Choose a validated CAT-Chem thermodynamics provider or
   extend and validate MKPP's model across composition, RH, and phase regimes;
   reconcile gas and modal aerosol totals without duplicate partitioning.

5. **Condensation, evaporation, and nucleation.** CRACMM's condensable
   precursors and particle species do not implement CMAQ's inorganic
   condensation/nucleation or equilibrium absorptive partitioning of
   semivolatile organics. Specify which CAT-Chem aerosol process owns each
   transfer and returns the updated gas and particle states. Do not apply a
   CMAQ-like partitioning process twice when an uptake reaction already
   consumes the same precursor. The [EPA chemistry documentation](https://usepa.github.io/CRACMM/chemistry/README.html)
   states that organic absorptive partitioning is outside the kinetic reaction
   listing.

6. **Heterogeneous and aqueous rate drivers.** The 11 `HET_*` reactions retain
   their stoichiometry but not CMAQ's calculated uptake coefficients. N2O5,
   NO2, glyoxal, and IEPOX pathways depend on such inputs as aerosol surface
   area and size, gas diffusivity, composition, liquid water, acidity, sulfate,
   temperature, and RH. Supply and validate their per-cell rates and particle
   products, including organosulfate consumption, against CMAQ. Do not infer
   that a `HETEROGENEOUS` label alone implements reactive uptake.

7. **Other named rates and photolysis.** Importing an UNKNOWN expression
   preserves its EPA source string rather than its executable CMAQ rate law;
   some include photolysis and specialized temperature/pressure dependencies.
   Inventory every named forcing, implement or provide its correct calculation,
   and compare values over day/night and relevant meteorological ranges. Do
   not substitute zero, guessed constants, or unrelated photolysis slots.

## CAT-Chem and UFS-Chem integration

8. **Define state ownership and scheduling.** Map CRACMM2 gas, aerosol, and
   bookkeeping species into CAT-Chem's state with explicit units, modal mapping,
   emissions, deposition, and restart behavior. Connect meteorology,
   photolysis, inorganic thermodynamics, aerosol microphysics, and MKPP through
   CAT-Chem's process interfaces. Specify when each process updates rates and
   state relative to the kinetic step; external operator-split processes do not
   become fully implicit merely by compiling the reactions into MKPP. CAT-Chem
   [documents a process-based architecture](https://catchem.readthedocs.io/en/latest/)
   and [UFS-Chem configurations](https://catchem.readthedocs.io/en/latest/ufschem/),
   but MKPP does not currently contain a CRACMM2-specific CAT-Chem adapter.

9. **Set scientific acceptance gates before deployment.** Compare MKPP and
   reference CMAQ box simulations for O3/NOx/HOx, inorganic gas-particle
   partitioning, aerosol water, SOA, and heterogeneous products under dry/wet,
   acidic/neutralized, dusty/marine, low/high organic loading, and day/night
   conditions. Check elemental and charge budgets, positivity, finite rates,
   mass transfers between gas and particle states, and timestep sensitivity.
   Then verify CAT-Chem/UFS-Chem interface units, restart reproducibility,
   multi-cell behavior, and operational performance. Passing compilation or
   species-count checks alone does not establish scientific equivalence.

## References

- [EPA CRACMM chemistry and CMAQ-ready mechanism](https://usepa.github.io/CRACMM/chemistry/README.html)
- [Pye et al. (2023), CRACMM multiphase chemistry and CMAQ aerosol coupling](https://acp.copernicus.org/articles/23/5043/2023/)
- [Fountoukis and Nenes (2007), ISORROPIA II](https://acp.copernicus.org/articles/7/4639/2007/)
- [CAT-Chem](https://github.com/ufs-community/CATChem)
