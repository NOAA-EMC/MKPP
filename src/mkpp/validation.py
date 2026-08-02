import os
from .model import MechanismDefinition

def sanitize_path(path: str) -> str:
    """Ensure path does not traverse directories upwards or access unauthorized roots."""
    if ".." in path:
        raise ValueError("Directory traversal detected in path")
    if path.startswith("/") and not path.startswith(os.getcwd()):
        raise ValueError("Directory traversal: Absolute paths must be within current workspace")
    return path

def validate_mechanism(mech: MechanismDefinition, strict: bool = False):
    """Validate mechanism references and schema deterministic rules."""
    if not mech or not mech.species:
        raise ValueError("Mechanism cannot be empty")

    if strict and not mech.description:
        raise ValueError("Strict mode requires a mechanism description")

    species_names = {s.name for s in mech.species}

    for idx, r in enumerate(mech.reactions):
        for reactant in r.reactants:
            if reactant not in species_names:
                raise ValueError(f"Unknown reactant '{reactant}' in reaction {idx}")
        for product in r.products:
            if product not in species_names:
                raise ValueError(f"Unknown product '{product}' in reaction {idx}")

import sys
from typing import Dict, Any

def validate_fuzzer_stiffness(max_condition_number: float, threshold: float = 1e12):
    """Extreme Environment Fuzzer compile gate (T042)."""
    if max_condition_number > threshold:
        print(f"FATAL ERROR: Unresolvable stiffness detected. Condition number {max_condition_number} exceeds threshold {threshold}.", file=sys.stderr)
        sys.exit(1)

def validate_mpi_safety(environment_config: Dict[str, Any]) -> bool:
    """Explicit no-root-rank aggregation validation (T043)."""
    mpi_config = environment_config.get("mpi", {})
    if mpi_config.get("gather_to_root", False):
        raise ValueError("Root-rank aggregation is strictly forbidden by EE2 standards.")
    return True

def validate_host_interface(mech: MechanismDefinition):
    """T022: Validate the zero-copy host interface schema."""
    if not getattr(mech, "host_interface", None) or not mech.host_interface.arrays:
        raise ValueError("Host interface schema is missing required arrays")

    for arr in mech.host_interface.arrays:
        if not arr.extent:
            raise ValueError(f"Host interface array '{arr.name}' must define extent vector matching rank {arr.rank}")
        if len(arr.extent) != arr.rank:
            raise ValueError(f"Extent length {len(arr.extent)} does not match rank {arr.rank} for array '{arr.name}'")
        if arr.ownership not in ("host", "device"):
            raise ValueError(f"Ownership must be 'host' or 'device', got {arr.ownership}")
        if not arr.unit or arr.unit == "unknown":
            raise ValueError(f"Host interface array '{arr.name}' must define a known physical unit for C-compatible translation")
    return True

def validate_terminator_safety(mech: MechanismDefinition) -> bool:
    """T028: Prevent abrupt photolysis changes from crashing explicit blocks."""
    for r in mech.reactions:
        if r.reaction_type.upper() == "PHOTOLYSIS" and not r.continuous_transition:
            raise ValueError("PHOTOLYSIS reactions must be marked with continuous_transition to safely navigate the terminator")
    return True

def validate_mass_conservation(mech: MechanismDefinition) -> bool:
    """T032, T034: Validate elemental mass balance for every reaction."""
    species_dict = {s.name: s.elements for s in mech.species}

    for idx, r in enumerate(mech.reactions):
        lhs_elements = {}
        rhs_elements = {}

        # Accumulate reactant elements
        for reactant in r.reactants:
            elements = species_dict.get(reactant, {})
            for elem, count in elements.items():
                lhs_elements[elem] = lhs_elements.get(elem, 0) + count

        # Accumulate product elements
        for product in r.products:
            elements = species_dict.get(product, {})
            for elem, count in elements.items():
                rhs_elements[elem] = rhs_elements.get(elem, 0) + count

        # Compare
        if lhs_elements != rhs_elements:
            raise ValueError(f"Elemental mass imbalance detected in reaction {idx}: {r.reactants} -> {r.products} ({lhs_elements} != {rhs_elements})")

    return True
