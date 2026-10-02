import copy
import json
import math
from pathlib import Path
from typing import Any

import yaml

from .model import (
    AerosolRepresentation,
    CompilationError,
    EnvironmentDefinition,
    EquilibriumDefinition,
    MechanismDefinition,
    PhaseDefinition,
    PhaseMode,
    ReactionDefinition,
    SolverMode,
    SpeciesDefinition,
)


def detect_config_format(source: str | Path) -> str:
    """Detect whether a configuration source is JSON or YAML.

    First checks file extension (.json -> json, .yaml/.yml -> yaml).
    If extension is missing or unrecognised, inspects leading content characters.
    """
    p = Path(source)
    if p.suffix.lower() == ".json":
        return "json"
    if p.suffix.lower() in (".yaml", ".yml"):
        return "yaml"

    try:
        if p.exists() and p.is_file():
            content = p.read_text(encoding="utf-8").strip()
        else:
            content = str(source).strip()
        if content.startswith("{") or content.startswith("["):
            return "json"
    except Exception:
        pass

    return "yaml"


def _normalize_species_dict(d: Any) -> dict[str, float]:
    """Normalize MICM/OpenAtmos reactant or product dictionary/list into species -> float yield."""
    if isinstance(d, list):
        result: dict[str, float] = {}
        for item in d:
            if isinstance(item, str):
                result[item] = 1.0
            elif isinstance(item, dict):
                name = item.get("species name", item.get("name"))
                if name:
                    result[str(name)] = float(item.get("coefficient", item.get("yield", 1.0)))
        return result
    if not isinstance(d, dict):
        return {}
    res = {}
    for sp, val in d.items():
        if isinstance(val, int | float):
            res[sp] = float(val)
        elif isinstance(val, dict):
            res[sp] = float(val.get("yield", 1.0))
        elif val is None:
            res[sp] = 1.0
        else:
            try:
                res[sp] = float(val)
            except (ValueError, TypeError):
                res[sp] = 1.0
    return res


def _normalize_si_rate_coefficients(reactions: list[ReactionDefinition]) -> list[ReactionDefinition]:
    """Convert supported SI rate coefficients to the kinetic concentration basis.

    Parameters
    ----------
    reactions : list[ReactionDefinition]
        Parsed reaction definitions containing SI-source coefficients.

    Returns
    -------
    list[ReactionDefinition]
        A deep-copied reaction list with supported coefficients converted.

    Raises
    ------
    CompilationError
        If any coefficient family, coefficient value, or reactant order cannot
        be converted safely.
    """
    molecules_per_mol_m3 = 6.02214076e17
    runtime_rate_types = {"PHOTOLYSIS", "PHASE_CHANGE", "USER_DEFINED", "SURFACE", "HETEROGENEOUS"}
    conversions: list[tuple[int, tuple[str, ...], float]] = []

    for reaction_index, reaction in enumerate(reactions):
        reaction_type = reaction.reaction_type.upper()
        if reaction_type in runtime_rate_types:
            continue

        reactant_order = 0
        for species_name, exponent in reaction.reactants.items():
            if not math.isfinite(exponent) or exponent < 0 or not exponent.is_integer():
                raise CompilationError(
                    stage="validation",
                    message=(
                        f"SI rate conversion does not support reactant exponent {exponent!r} "
                        f"for species '{species_name}' in {reaction_type}"
                    ),
                    reaction_index=reaction_index,
                )
            reactant_order += int(exponent)

        coefficient_paths: list[tuple[tuple[str, ...], int]] = []
        parameters = reaction.parameters
        if reaction_type == "ARRHENIUS":
            if "A" not in parameters:
                raise CompilationError(
                    stage="validation",
                    message="SI ARRHENIUS reaction is missing coefficient 'A'",
                    reaction_index=reaction_index,
                )
            coefficient_paths.append((("A",), reactant_order))
        elif reaction_type in {"TROE", "FALLOFF"}:
            for key in ("k0", "kinf"):
                if key in parameters and not isinstance(parameters[key], dict):
                    raise CompilationError(
                        stage="validation",
                        message=f"SI {reaction_type} coefficient group '{key}' must be a dictionary",
                        reaction_index=reaction_index,
                    )
            for key, order in (("k0", reactant_order + 1), ("kinf", reactant_order)):
                group = parameters.get(key)
                if isinstance(group, dict):
                    if "A" in group:
                        coefficient_paths.append(((key, "A"), order))
                elif f"{key}_A" in parameters:
                    coefficient_paths.append(((f"{key}_A",), order))
        elif reaction_type == "EP2":
            for key in ("A0", "A2"):
                if key in parameters:
                    coefficient_paths.append(((key,), reactant_order))
            if "A3" in parameters:
                coefficient_paths.append((("A3",), reactant_order + 1))
        elif reaction_type == "EP3":
            if "A1" in parameters:
                coefficient_paths.append((("A1",), reactant_order))
            if "A2" in parameters:
                coefficient_paths.append((("A2",), reactant_order + 1))
        else:
            raise CompilationError(
                stage="validation",
                message=f"SI rate conversion is unsupported for reaction type '{reaction_type}'",
                reaction_index=reaction_index,
            )

        for path, effective_order in coefficient_paths:
            value: Any = parameters
            for key in path:
                value = value[key]
            coefficient_name = ".".join(path)
            if isinstance(value, bool):
                numeric_value = math.nan
            else:
                try:
                    numeric_value = float(value)
                except (TypeError, ValueError):
                    numeric_value = math.nan
            if not math.isfinite(numeric_value):
                raise CompilationError(
                    stage="validation",
                    message=(
                        f"SI {reaction_type} coefficient '{coefficient_name}' must be a finite numeric value; " f"got {value!r}"
                    ),
                    reaction_index=reaction_index,
                )
            conversion_factor = molecules_per_mol_m3 ** (1 - effective_order)
            converted_value = numeric_value * conversion_factor
            if not math.isfinite(converted_value) or (numeric_value != 0.0 and converted_value == 0.0):
                raise CompilationError(
                    stage="validation",
                    message=f"SI {reaction_type} coefficient '{coefficient_name}' is outside the convertible numeric range",
                    reaction_index=reaction_index,
                )
            conversions.append((reaction_index, path, converted_value))

    normalized_reactions = copy.deepcopy(reactions)
    for reaction_index, path, converted_value in conversions:
        parameters = normalized_reactions[reaction_index].parameters
        for key in path[:-1]:
            parameters = parameters[key]
        parameters[path[-1]] = converted_value
    return normalized_reactions


def parse_mechanism_micm(
    name: str, data: dict[str, Any], *, convert_openatmos_activation_energy: bool = False
) -> MechanismDefinition:
    """Parse MICM/OpenAtmos standard dictionary into internal model."""
    if not isinstance(data, dict) or "species" not in data or not data["species"]:
        raise CompilationError(
            stage="parsing",
            message="OpenAtmos v1 data must define at least one species",
        )

    metadata = data.get("metadata", {})
    if not isinstance(metadata, dict):
        raise CompilationError(stage="parsing", message="Mechanism metadata must be a dictionary")
    raw_rate_units = metadata.get("rate_units", "kinetic")
    source_rate_units = str(raw_rate_units).strip().lower()
    if source_rate_units not in {"kinetic", "si"}:
        raise CompilationError(
            stage="parsing",
            message=f"Invalid metadata.rate_units '{raw_rate_units}'; accepted values are 'kinetic' and 'SI'",
        )
    if source_rate_units == "si":
        source_rate_units = "SI"

    species = []
    for s in data.get("species", []):
        if not isinstance(s, dict) or not s.get("name"):
            raise CompilationError(
                stage="parsing",
                message="Species in OpenAtmos v1 mechanism must have a name",
            )
        sp_name = s.get("name")
        # Default to GAS if not specified in basic MICM
        phase = PhaseMode.GAS
        sp_type = str(s.get("type", "")).lower()
        sp_role = str(s.get("role", "")).lower()
        # Only explicit OpenAtmos fixed roles and the conventional third-body
        # placeholders are non-evolving. Atmospheric species such as O2 and
        # H2O may look like background constituents, but TS1/MICM evolves them
        # and their tendency must therefore be part of the same ODE system.
        if sp_name in ("AIR", "M") or sp_type == "fixed" or sp_role == "fixed":
            role = "fixed"
        else:
            role = "variable"
        species.append(
            SpeciesDefinition(
                name=sp_name,
                phase=phase,
                role=role,
                solver_atol=s.get("_atol"),
                solver_rtol=s.get("_rtol"),
            )
        )

    phases = []
    for p in data.get("phases", []):
        phases.append(PhaseDefinition(name=p.get("name"), solver_mode=SolverMode.IMPLICIT))

    # Build species name set for validation
    species_names = {s.name for s in species}

    reactions = []
    equilibrium_reactions: list[EquilibriumDefinition] = []

    def micm_signed_parameters(raw: dict[str, Any]) -> dict[str, Any]:
        """Match musica/MICM's signed activation-energy representation.

        The OpenAtmos JSON serialisation carries positive activation energies;
        musica converts them to MICM's signed ``exp(C / T)`` convention when it
        constructs an Arrhenius or Troe object.  MKPP lowers the latter form,
        so apply the same conversion before symbolic rate/Jacobian generation.
        """
        converted = dict(raw)
        for key in ("C", "k0_C", "kinf_C", "C0", "C1", "C2", "C3"):
            value = converted.get(key)
            if isinstance(value, int | float):
                converted[key] = -float(value)
        for key in ("k0", "kinf"):
            value = converted.get(key)
            if isinstance(value, dict):
                nested = dict(value)
                if isinstance(nested.get("C"), int | float):
                    nested["C"] = -float(nested["C"])
                converted[key] = nested
        return converted

    for r in data.get("reactions", []):
        rtype = r.get("type", "UNKNOWN")

        if rtype == "EQUILIBRIUM":
            # Parse EQUILIBRIUM block into EquilibriumDefinition
            system = r.get("system", "")
            raw_total_species = r.get("total_species", {})
            regime_blending = r.get("regime_blending", "sigmoid")
            transition_width = r.get("transition_width", 0.05)
            activity_model = r.get("activity_model", "fixed")
            eq_constants = r.get("equilibrium_constants", {})
            continuous_transition = r.get("continuous_transition", True)

            # Flatten total_species: each element maps to [gas_species, *aerosol_species]
            total_species: dict[str, list[str]] = {}
            for element_name, element_data in raw_total_species.items():
                gas_sp = element_data.get("gas", "")
                aerosol_sp = element_data.get("aerosol", [])
                if isinstance(aerosol_sp, str):
                    aerosol_sp = [aerosol_sp]
                flat_list = [gas_sp] + aerosol_sp
                total_species[element_name] = flat_list

            # Validate all referenced species exist in the mechanism species list
            for element_name, sp_list in total_species.items():
                for sp_name in sp_list:
                    if sp_name not in species_names:
                        raise CompilationError(
                            stage="parsing",
                            message=f"EQUILIBRIUM references unknown species '{sp_name}' " f"in element '{element_name}'",
                            species_name=sp_name,
                        )

            # Validate equilibrium constants have required params (A, dH, Tref)
            for const_name, const_params in eq_constants.items():
                for required_field in ("A", "dH", "Tref"):
                    if required_field not in const_params:
                        raise CompilationError(
                            stage="validation",
                            message=f"Equilibrium constant '{const_name}' requires A, dH, Tref parameters",
                        )

            equilibrium_reactions.append(
                EquilibriumDefinition(
                    system=system,
                    total_species=total_species,
                    regime_blending=regime_blending,
                    transition_width=transition_width,
                    activity_model=activity_model,
                    equilibrium_constants=eq_constants,
                    continuous_transition=continuous_transition,
                    relaxation_timescale_inv=r.get("relaxation_timescale_inv", 1e6),
                )
            )
            # EQUILIBRIUM is not a kinetic reaction — do NOT add to reactions list
            continue

        # OpenAtmos surface uptake reactions encode their gas-phase side with
        # dedicated fields rather than the ordinary reactants/products maps.
        # Normalize them into the common representation so downstream
        # symbolic lowering applies both the concentration dependence and the
        # product stoichiometry.  This is format-level behaviour, not a
        # mechanism-specific convention.
        if rtype.upper() == "SURFACE":
            gas_species = r.get("gas-phase species")
            reactants = {str(gas_species): 1.0} if gas_species else {}
            products = _normalize_species_dict(r.get("gas-phase products", {}))
        else:
            reactants = _normalize_species_dict(r.get("reactants", {}))
            products = _normalize_species_dict(r.get("products", {}))

        # Extract all potential rate parameters instead of just A
        # For MICM compliance, parameters can include k0, kinf, Fc, gamma, etc.
        parameters = {}
        for k, v in r.items():
            if k not in ("type", "reactants", "products", "stiff", "continuous_transition"):
                parameters[k] = v
        if convert_openatmos_activation_energy:
            parameters = micm_signed_parameters(parameters)

        # Maintain backwards compat for the simple tests
        base_rate = str(r.get("A", ""))

        reactions.append(
            ReactionDefinition(
                reaction_type=rtype,
                reactants=reactants,
                products=products,
                rate_expression=base_rate,
                parameters=parameters,
                stiff=r.get("stiff", False),
                # OpenAtmos/MUSICA photolysis entries are continuous by definition;
                # older YAML mechanisms may opt out explicitly.
                continuous_transition=r.get("continuous_transition", rtype.upper() == "PHOTOLYSIS"),
            )
        )

    if source_rate_units == "SI":
        reactions = _normalize_si_rate_coefficients(reactions)

    # Detect PHASE_CHANGE / EQUILIBRIUM conflicts: collect species from each
    phase_change_species: set[str] = set()
    for rxn in reactions:
        if rxn.reaction_type == "PHASE_CHANGE":
            phase_change_species.update(rxn.reactants.keys())
            phase_change_species.update(rxn.products.keys())

    equilibrium_species: set[str] = set()
    for eq_def in equilibrium_reactions:
        for sp_list in eq_def.total_species.values():
            equilibrium_species.update(sp_list)

    overlap = phase_change_species & equilibrium_species
    if overlap:
        conflict_name = sorted(overlap)[0]
        raise CompilationError(
            stage="validation",
            message=f"Species '{conflict_name}' cannot have both " f"PHASE_CHANGE and EQUILIBRIUM declarations",
            species_name=conflict_name,
        )

    from .model import ArrayDefinition, HostInterfaceSchema

    host_interface = None
    if "host_interface" in data and "arrays" in data["host_interface"]:
        arrays = []
        for arr_data in data["host_interface"]["arrays"]:
            arrays.append(
                ArrayDefinition(
                    name=arr_data.get("name", "unknown"),
                    rank=arr_data.get("rank", 0),
                    layout=arr_data.get("layout", "LayoutLeft"),
                    extent=arr_data.get("extent"),
                    unit=arr_data.get("unit", "unknown"),
                    ownership=arr_data.get("ownership", "host"),
                )
            )
        host_interface = HostInterfaceSchema(arrays=arrays)

    # A kinetic reaction may declare an `activation_trigger` naming a runtime
    # meteorological quantity, e.g. "meteo.cloud_liquid_water > 1.0e-6". When
    # present, the reaction's rate is gated by a smooth indicator of that
    # quantity and the generated solver must accept it as an extra per-cell
    # equilibrium input. Only cloud liquid water is currently supported; an
    # unrecognized quantity is rejected rather than silently ignored, because a
    # dropped trigger would run ungated chemistry (the exact failure R1 guards).
    _TRIGGER_QUANTITIES = {"meteo.cloud_liquid_water": "cloud_liquid_water"}
    cloud_gated = False
    for rxn in reactions:
        trigger = rxn.parameters.get("activation_trigger")
        if trigger is None:
            continue
        quantity = str(trigger).split(">")[0].strip()
        if quantity not in _TRIGGER_QUANTITIES:
            raise CompilationError(
                stage="validation",
                message=(
                    f"reaction declares unsupported activation_trigger '{trigger}'; "
                    f"supported quantities: {sorted(_TRIGGER_QUANTITIES)}"
                ),
            )
        cloud_gated = True

    return MechanismDefinition(
        name=name,
        description=data.get("description", ""),
        aerosol_representation=AerosolRepresentation.BULK,
        species=species,
        phases=phases,
        reactions=reactions,
        host_interface=host_interface,
        equilibrium_reactions=equilibrium_reactions,
        metadata=metadata,
        source_rate_units=source_rate_units,
        has_cloud_gated_reaction=cloud_gated,
    )


def load_mechanism(path: str | Path) -> MechanismDefinition:
    """Load an OpenAtmos v1 chemical mechanism from a JSON or YAML file."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Mechanism configuration file not found: {p}")

    fmt = detect_config_format(p)
    try:
        with open(p, encoding="utf-8") as f:
            if fmt == "json":
                data = json.load(f)
            else:
                data = yaml.safe_load(f)
    except json.JSONDecodeError as e:
        raise CompilationError(
            stage="parsing",
            message=f"JSON syntax error in mechanism file '{p}': line {e.lineno}, column {e.colno} ({e.msg})",
            yaml_location=f"{p}:{e.lineno}:{e.colno}",
        ) from e
    except yaml.YAMLError as e:
        loc = str(p)
        if hasattr(e, "problem_mark") and e.problem_mark is not None:
            loc = f"{p}:{e.problem_mark.line + 1}:{e.problem_mark.column + 1}"
        raise CompilationError(
            stage="parsing",
            message=f"YAML syntax error in mechanism file '{p}': {e}",
            yaml_location=loc,
        ) from e

    if not isinstance(data, dict):
        raise CompilationError(
            stage="parsing",
            message=f"Mechanism configuration file '{p}' must contain a key-value dictionary",
            yaml_location=str(p),
        )

    # OpenAtmos/MUSICA and MICM both store Arrhenius activation terms in the
    # signed exp(C / T) convention.  Preserve the source value verbatim.
    # OpenAtmos catalog entries are conventionally named ``mechanism.json``.
    # The source document name describes the chemistry; an optional catalog
    # mechanism ID provides the stable host-facing artifact name.  This keeps
    # generated include paths stable without deriving identity from the shared
    # file stem.
    metadata = data.get("metadata", {})
    mechanism_id = metadata.get("mkpp_mechanism_id") if isinstance(metadata, dict) else None
    return parse_mechanism_micm(str(mechanism_id or data.get("name", p.stem)), data)


def load_environment(path: str | Path) -> EnvironmentDefinition:
    """Load an OpenAtmos v1 environmental configuration from a JSON or YAML file."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Environment configuration file not found: {p}")

    fmt = detect_config_format(p)
    try:
        with open(p, encoding="utf-8") as f:
            if fmt == "json":
                data = json.load(f)
            else:
                data = yaml.safe_load(f)
    except json.JSONDecodeError as e:
        raise CompilationError(
            stage="parsing",
            message=f"JSON syntax error in environment file '{p}': line {e.lineno}, column {e.colno} ({e.msg})",
            yaml_location=f"{p}:{e.lineno}:{e.colno}",
        ) from e
    except yaml.YAMLError as e:
        loc = str(p)
        if hasattr(e, "problem_mark") and e.problem_mark is not None:
            loc = f"{p}:{e.problem_mark.line + 1}:{e.problem_mark.column + 1}"
        raise CompilationError(
            stage="parsing",
            message=f"YAML syntax error in environment file '{p}': {e}",
            yaml_location=loc,
        ) from e

    if not isinstance(data, dict):
        raise CompilationError(
            stage="parsing",
            message=f"Environment configuration file '{p}' must contain a key-value dictionary",
            yaml_location=str(p),
        )

    env_block = data.get("environment", data.get("meteorology", data))

    temp = float(env_block.get("temperature", env_block.get("T", 298.15)))
    press = float(env_block.get("pressure", env_block.get("P", 101325.0)))
    air_dens = float(env_block.get("air_density", env_block.get("M", 2.46e19)))
    rh = float(env_block.get("relative_humidity", env_block.get("RH", 0.5)))
    solver_block = data.get("solver", {})
    if not isinstance(solver_block, dict):
        solver_block = {}
    solver_atol = solver_block.get("atol")
    solver_rtol = solver_block.get("rtol")
    solver_seed = solver_block.get("initial_step_seed")

    init_conc = data.get("initial_concentrations", data.get("initial_conditions", data.get("concentrations", {})))
    if not isinstance(init_conc, dict):
        init_conc = {}

    normalized_init = {str(k): float(v) for k, v in init_conc.items() if isinstance(v, int | float | str)}

    return EnvironmentDefinition(
        temperature=temp,
        pressure=press,
        air_density=air_dens,
        relative_humidity=rh,
        solver_atol=float(solver_atol) if solver_atol is not None else None,
        solver_rtol=float(solver_rtol) if solver_rtol is not None else None,
        solver_initial_step_seed=float(solver_seed) if solver_seed is not None else None,
        initial_concentrations=normalized_init,
    )
