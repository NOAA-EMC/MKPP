import json
import yaml
from pathlib import Path
from typing import Dict, Any

from .model import (
    MechanismDefinition, SpeciesDefinition, PhaseDefinition,
    ReactionDefinition, PhaseMode, SolverMode, AerosolRepresentation
)

def parse_mechanism_micm(name: str, data: Dict[str, Any]) -> MechanismDefinition:
    """Parse MICM/OpenAtmos standard dictionary into internal model."""
    if "species" not in data or not data["species"]:
        raise ValueError("MICM data must define at least one species")
        
    species = []
    for s in data.get("species", []):
        sp_name = s.get("name")
        if not sp_name:
            raise ValueError("Species must have a name")
        # Default to GAS if not specified in basic MICM
        phase = PhaseMode.GAS 
        species.append(SpeciesDefinition(name=sp_name, phase=phase))
        
    phases = []
    for p in data.get("phases", []):
        phases.append(PhaseDefinition(
            name=p.get("name"),
            solver_mode=SolverMode.IMPLICIT
        ))
        
    reactions = []
    for r in data.get("reactions", []):
        rtype = r.get("type", "UNKNOWN")
        reactants = list(r.get("reactants", {}).keys())
        products = list(r.get("products", {}).keys())
        reactions.append(ReactionDefinition(
            reaction_type=rtype,
            reactants=reactants,
            products=products,
            rate_expression=str(r.get("A", "")) # Simplify base expression for MVP
        ))
        
    return MechanismDefinition(
        name=name,
        description=data.get("description", ""),
        aerosol_representation=AerosolRepresentation.BULK,
        species=species,
        phases=phases,
        reactions=reactions
    )

def load_mechanism(path: str) -> MechanismDefinition:
    p = Path(path)
    with open(p, 'r') as f:
        if p.suffix in ['.yaml', '.yml']:
            data = yaml.safe_load(f)
        else:
            data = json.load(f)
    return parse_mechanism_micm(p.stem, data)
