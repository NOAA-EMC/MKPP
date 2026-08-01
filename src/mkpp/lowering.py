from typing import Dict, List
from .model import MechanismDefinition, ReactionDefinition

def partition_reactions(mech: MechanismDefinition) -> Dict[str, List[ReactionDefinition]]:
    """Partition reactions into implicit (stiff) and explicit (non-stiff) deterministic blocks."""
    blocks = {
        "implicit": [],
        "explicit": []
    }
    
    for r in mech.reactions:
        if r.stiff:
            blocks["implicit"].append(r)
        else:
            blocks["explicit"].append(r)
            
    # Sort blocks deterministically by reaction type then expression
    blocks["implicit"].sort(key=lambda x: (x.reaction_type, x.rate_expression))
    blocks["explicit"].sort(key=lambda x: (x.reaction_type, x.rate_expression))
    
    return blocks

def prepare_adjoint_and_tlm(mech: MechanismDefinition) -> Dict[str, bool]:
    """
    T015: Symbolic lowering hooks for analytical Jacobian, Adjoint, and Tangent-Linear models.
    For the MVP, this validates that the mechanism is differentiable.
    """
    # Verify no discontinuous thermodynamic operators are present 
    for r in mech.reactions:
        if not r.continuous_transition and r.reaction_type in ("condensation", "phase_change"):
            raise ValueError(f"Reaction {r.rate_expression} lacks continuous transition for analytical differentiation.")
            
    return {"adjoint_ready": True, "tlm_ready": True}
