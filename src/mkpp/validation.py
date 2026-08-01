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
