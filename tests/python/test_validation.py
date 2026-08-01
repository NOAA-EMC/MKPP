import pytest
import yaml
from mkpp.model import MechanismDefinition, PhaseMode, SolverMode, AerosolRepresentation
from mkpp.parser import parse_mechanism_micm
from mkpp.validation import validate_mechanism, sanitize_path

def test_sanitize_path_rejects_traversal():
    with pytest.raises(ValueError, match="Directory traversal"):
        sanitize_path("../secret/file.yaml")
    with pytest.raises(ValueError, match="Directory traversal"):
        sanitize_path("/absolute/unauthorized/path.yaml")
    assert sanitize_path("valid/path.yaml") == "valid/path.yaml"
    assert sanitize_path("./valid/path.yaml") == "./valid/path.yaml"

def test_parse_micm_mechanism():
    yaml_content = """
    species:
      - name: O3
        type: CHEM_SPEC
      - name: O2
        type: CHEM_SPEC
      - name: O
        type: CHEM_SPEC
    phases:
      - name: gas
        species: [O3, O2, O]
    reactions:
      - type: ARRHENIUS
        reactants:
          O: {}
          O2: {}
          M: {}
        products:
          O3: {}
          M: {}
        A: 6.0e-34
    """
    raw_data = yaml.safe_load(yaml_content)
    mech = parse_mechanism_micm("test_mech", raw_data)
    assert len(mech.species) == 3
    assert mech.species[0].name == "O3"
    assert len(mech.phases) == 1
    assert mech.phases[0].name == "gas"
    assert len(mech.reactions) == 1
    assert mech.reactions[0].reaction_type == "ARRHENIUS"
    assert "O2" in mech.reactions[0].reactants
    assert "O3" in mech.reactions[0].products

def test_validate_mechanism_missing_species():
    yaml_content = """
    species:
      - name: O2
        type: CHEM_SPEC
    phases: []
    reactions:
      - type: ARRHENIUS
        reactants:
          O: {}
          O2: {}
        products:
          O3: {}
        A: 1.0
    """
    raw_data = yaml.safe_load(yaml_content)
    mech = parse_mechanism_micm("bad_mech", raw_data)
    with pytest.raises(ValueError, match="Unknown reactant 'O' in reaction"):
        validate_mechanism(mech)

from mkpp.validation import validate_fuzzer_stiffness, validate_mpi_safety

def test_validate_fuzzer_stiffness():
    # Fuzzer stiffness exceeding threshold must exit with non-zero status (T042)
    with pytest.raises(SystemExit) as e:
        validate_fuzzer_stiffness(max_condition_number=1e15, threshold=1e12)
    assert e.value.code != 0

def test_validate_mpi_safety():
    # MPI Safety check must reject root-rank aggregation (T043)
    with pytest.raises(ValueError, match="Root-rank aggregation is strictly forbidden"):
        validate_mpi_safety({"mpi": {"gather_to_root": True}})
    
    assert validate_mpi_safety({"mpi": {"gather_to_root": False}}) is True

def test_validate_mechanism_strict():
    from mkpp.model import MechanismDefinition, AerosolRepresentation, SpeciesDefinition, PhaseMode
    
    # Valid but missing description
    mech = MechanismDefinition(
        name="test_mech",
        description="", # Empty description
        aerosol_representation=AerosolRepresentation.BULK,
        species=[SpeciesDefinition(name="O3", phase=PhaseMode.GAS)],
        phases=[],
        reactions=[]
    )
    
    # Should pass in non-strict mode
    validate_mechanism(mech, strict=False)
    
    # Should fail in strict mode
    with pytest.raises(ValueError, match="Strict mode requires a mechanism description"):
        validate_mechanism(mech, strict=True)
