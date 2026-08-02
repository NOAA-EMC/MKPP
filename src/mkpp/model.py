from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum

class PhaseMode(Enum):
    GAS = "gas"
    AEROSOL = "aerosol"
    AQUEOUS = "aqueous"
    MIXED = "mixed"

class SolverMode(Enum):
    IMPLICIT = "implicit"
    EXPLICIT = "explicit"
    COUPLED = "coupled"

class AerosolRepresentation(Enum):
    BULK = "bulk"
    MODAL = "modal"
    SECTIONAL = "sectional"

class ReactionType(Enum):
    ARRHENIUS = "ARRHENIUS"
    TROE = "TROE"
    PHOTOLYSIS = "PHOTOLYSIS"
    HETEROGENEOUS = "HETEROGENEOUS"
    TUNNELING = "TUNNELING"
    CONDENSATION = "CONDENSATION"
    PHASE_CHANGE = "PHASE_CHANGE"
    UNKNOWN = "UNKNOWN"

@dataclass
class SpeciesDefinition:
    name: str
    phase: PhaseMode
    elements: Dict[str, int] = field(default_factory=dict)
    role: Optional[str] = None

@dataclass
class PhaseDefinition:
    name: str
    solver_mode: SolverMode
    transport_model: Optional[str] = None
    continuity_model: Optional[str] = None

@dataclass
class ReactionDefinition:
    reaction_type: str  # e.g., ARRHENIUS, PHOTOLYSIS, TROE, EP2, EP3
    reactants: Dict[str, float]
    products: Dict[str, float]
    rate_expression: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    unit_policy: str = "canonical"
    stiff: bool = False
    continuous_transition: bool = False

@dataclass
class ArrayDefinition:
    name: str
    rank: int
    layout: str = "LayoutLeft" # Default to Fortran-compatible column-major
    extent: Optional[List[int]] = None
    unit: str = "unknown"
    ownership: str = "host" # 'host' or 'device'

@dataclass
class HostInterfaceSchema:
    arrays: List[ArrayDefinition] = field(default_factory=list)

@dataclass
class MechanismDefinition:
    name: str
    description: str
    aerosol_representation: AerosolRepresentation
    species: List[SpeciesDefinition]
    phases: List[PhaseDefinition]
    reactions: List[ReactionDefinition]
    host_interface: Optional['HostInterfaceSchema'] = None
    units: str = "canonical"
    metadata: Dict[str, str] = field(default_factory=dict)

@dataclass
class TestEnvironmentDefinition:
    name: str
    initial_conditions: Dict[str, float]
    meteorology: Dict[str, float]
    photolysis: Dict[str, float]
    cloud_liquid_water: float
    bounds: Dict[str, Dict[str, float]]
    expected_outputs: Optional[Dict[str, float]] = None

@dataclass
class GeneratedArtifact:
    kind: str
    path: str
    dependencies: List[str]
    checksum: Optional[str] = None
