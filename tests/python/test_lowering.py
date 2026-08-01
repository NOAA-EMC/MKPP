import pytest
from mkpp.model import MechanismDefinition, ReactionDefinition, AerosolRepresentation
from mkpp.lowering import partition_reactions

def test_partition_reactions():
    mech = MechanismDefinition(
        name="test_mech",
        description="Test",
        aerosol_representation=AerosolRepresentation.BULK,
        species=[],
        phases=[],
        reactions=[
            ReactionDefinition(reaction_type="ARRHENIUS", reactants=[], products=[], rate_expression="", stiff=True),
            ReactionDefinition(reaction_type="PHOTOLYSIS", reactants=[], products=[], rate_expression="", stiff=False),
        ]
    )
    blocks = partition_reactions(mech)
    assert "implicit" in blocks
    assert "explicit" in blocks
    assert len(blocks["implicit"]) == 1
    assert len(blocks["explicit"]) == 1

from mkpp.lowering import prepare_adjoint_and_tlm
import pytest

def test_prepare_adjoint_and_tlm_success():
    mech = MechanismDefinition(
        name="test_mech", description="Test",
        aerosol_representation=AerosolRepresentation.BULK,
        species=[], phases=[],
        reactions=[
            ReactionDefinition(reaction_type="condensation", reactants=[], products=[], rate_expression="", continuous_transition=True)
        ]
    )
    result = prepare_adjoint_and_tlm(mech)
    assert result["adjoint_ready"] is True
    assert result["tlm_ready"] is True

def test_prepare_adjoint_and_tlm_failure():
    mech = MechanismDefinition(
        name="test_mech", description="Test",
        aerosol_representation=AerosolRepresentation.BULK,
        species=[], phases=[],
        reactions=[
            ReactionDefinition(reaction_type="condensation", reactants=[], products=[], rate_expression="", continuous_transition=False)
        ]
    )
    with pytest.raises(ValueError, match="lacks continuous transition"):
        prepare_adjoint_and_tlm(mech)
