"""
Property-based test for context completeness under StrictUndefined (Property 2).

# Feature: jinja2-codegen-templates, Property 2: Context completeness under StrictUndefined

For any valid MechanismDefinition and solver configuration,
`build_template_context` + `render("header.j2", context)` must complete
without `UndefinedError`.

Verify all required keys present, blocks list present when block structure
exists, transpose steps present when adjoint enabled.

**Validates: Requirements 2.1, 2.2, 2.3, 2.4, 6.4**
"""

from hypothesis import given, settings
from hypothesis import strategies as st
from jinja2 import UndefinedError
from mkpp.lowering import compute_symbolic_lu_decomposition, prepare_unified_jacobian
from mkpp.model import (
    AerosolRepresentation,
    MechanismDefinition,
    PhaseMode,
    ReactionDefinition,
    SpeciesDefinition,
)
from mkpp.rosenbrock import SOLVER_COEFFICIENTS
from mkpp.template_context import build_template_context
from mkpp.template_engine import TemplateEngine

# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

SOLVER_NAMES = list(SOLVER_COEFFICIENTS.keys())


@st.composite
def mechanism_strategy(draw):
    """Generate a valid MechanismDefinition with 2-6 species and plausible reactions.

    Builds:
    - N species with unique names
    - 1-3 ARRHENIUS reactions referencing valid species
    - Optionally includes a PHOTOLYSIS reaction
    - Random solver name from available solvers
    - Random adjoint flag
    """
    # Number of species
    n = draw(st.integers(min_value=2, max_value=6))

    # Generate unique species names
    species_names = [f"SP{i}" for i in range(n)]
    species_list = [SpeciesDefinition(name=name, phase=PhaseMode.GAS) for name in species_names]

    # Generate reactions: 1-3 ARRHENIUS reactions
    num_reactions = draw(st.integers(min_value=1, max_value=min(3, n - 1)))
    reactions = []
    for r_idx in range(num_reactions):
        # Pick a reactant and product from available species (different ones)
        reactant_idx = draw(st.integers(min_value=0, max_value=n - 1))
        product_idx = draw(st.integers(min_value=0, max_value=n - 1).filter(lambda x, ri=reactant_idx: x != ri))
        reactant_name = species_names[reactant_idx]
        product_name = species_names[product_idx]

        reactions.append(
            ReactionDefinition(
                reaction_type="ARRHENIUS",
                reactants={reactant_name: 1.0},
                products={product_name: 1.0},
                rate_expression=f"k{r_idx}*{reactant_name}",
                parameters={"A": 1e-3, "B": 0.0, "C": 0.0},
                stiff=True,
            )
        )

    # Optionally add a photolysis reaction
    has_photolysis = draw(st.booleans())
    if has_photolysis and n >= 2:
        photo_reactant_idx = draw(st.integers(min_value=0, max_value=n - 1))
        photo_product_idx = draw(st.integers(min_value=0, max_value=n - 1).filter(lambda x, ri=photo_reactant_idx: x != ri))
        reactions.append(
            ReactionDefinition(
                reaction_type="PHOTOLYSIS",
                reactants={species_names[photo_reactant_idx]: 1.0},
                products={species_names[photo_product_idx]: 1.0},
                rate_expression=f"J1*{species_names[photo_reactant_idx]}",
                parameters={"A": "J1"},
                stiff=True,
            )
        )

    # Solver name
    solver_name = draw(st.sampled_from(SOLVER_NAMES))

    # Adjoint flag
    adjoint = draw(st.booleans())

    mech = MechanismDefinition(
        name=f"prop2_test_{n}sp",
        description="Property 2 test mechanism",
        aerosol_representation=AerosolRepresentation.BULK,
        species=species_list,
        phases=[],
        reactions=reactions,
    )

    return mech, solver_name, adjoint


@st.composite
def mechanism_with_blocks_strategy(draw):
    """Generate a mechanism that produces block-diagonal LU structure.

    Creates two independent reaction chains (A->B and C->D) so the
    Jacobian is block-diagonal.
    """
    # Always 4 species in 2 blocks
    species_list = [
        SpeciesDefinition(name="A", phase=PhaseMode.GAS),
        SpeciesDefinition(name="B", phase=PhaseMode.GAS),
        SpeciesDefinition(name="C", phase=PhaseMode.GAS),
        SpeciesDefinition(name="D", phase=PhaseMode.GAS),
    ]

    reactions = [
        ReactionDefinition(
            reaction_type="ARRHENIUS",
            reactants={"A": 1.0},
            products={"B": 1.0},
            rate_expression="k1*A",
            parameters={"A": 1e-3, "B": 0.0, "C": 0.0},
            stiff=True,
        ),
        ReactionDefinition(
            reaction_type="ARRHENIUS",
            reactants={"C": 1.0},
            products={"D": 1.0},
            rate_expression="k2*C",
            parameters={"A": 2e-3, "B": 0.0, "C": 0.0},
            stiff=True,
        ),
    ]

    solver_name = draw(st.sampled_from(SOLVER_NAMES))
    adjoint = draw(st.booleans())

    mech = MechanismDefinition(
        name="prop2_block_test",
        description="Block-diagonal mechanism for Property 2",
        aerosol_representation=AerosolRepresentation.BULK,
        species=species_list,
        phases=[],
        reactions=reactions,
    )

    return mech, solver_name, adjoint


# ---------------------------------------------------------------------------
# Required context keys (from Requirement 2.2)
# ---------------------------------------------------------------------------

REQUIRED_KEYS = [
    "mechanism_name",
    "species",
    "num_species",
    "tableau",
    "jacobian_entries",
    "permutation",
    "adjoint_enabled",
    "has_equilibrium",
    "has_cloud_gated",
    "has_photolysis",
    "num_photolysis",
    "tolerance_arrays",
]


# ---------------------------------------------------------------------------
# Property 2: Context completeness under StrictUndefined
# **Validates: Requirements 2.1, 2.2, 2.3, 2.4, 6.4**
# ---------------------------------------------------------------------------


@given(data=mechanism_strategy())
@settings(deadline=None)
def test_property_2_context_completeness_no_undefined_error(data):
    """
    For any valid MechanismDefinition and solver configuration,
    `build_template_context` + `render("header.j2", context)` must complete
    without raising `UndefinedError`.

    This confirms the context produced by build_template_context is always
    sufficient for the header.j2 template under StrictUndefined.

    **Validates: Requirements 2.1, 2.2, 2.3, 2.4, 6.4**
    """
    mech, solver_name, adjoint = data

    # Build the template context from the mechanism
    lowering_data = prepare_unified_jacobian(mech)
    lu_plan = compute_symbolic_lu_decomposition(
        lowering_data["jacobian_matrix"],
        lowering_data["species_map"],
    )

    context = build_template_context(
        mech,
        solver_name=solver_name,
        lu_plan=lu_plan,
        sympy_meta=lowering_data,
        adjoint=adjoint,
    )

    # Verify all required keys are present
    for key in REQUIRED_KEYS:
        assert key in context, (
            f"Required key '{key}' missing from context.\n"
            f"Mechanism: {mech.name}, solver={solver_name}, adjoint={adjoint}\n"
            f"Context keys: {sorted(context.keys())}"
        )

    # When adjoint is enabled, verify transpose steps are present
    if adjoint:
        assert "transpose_forward_sub_steps" in context, "transpose_forward_sub_steps missing when adjoint=True"
        assert "transpose_backward_sub_steps" in context, "transpose_backward_sub_steps missing when adjoint=True"
        assert context["transpose_forward_sub_steps"] is not None, "transpose_forward_sub_steps is None when adjoint=True"
        assert context["transpose_backward_sub_steps"] is not None, "transpose_backward_sub_steps is None when adjoint=True"

    # Render header.j2 - must not raise UndefinedError
    engine = TemplateEngine()
    try:
        rendered = engine.render("header.j2", context)
    except UndefinedError as e:
        raise AssertionError(
            f"UndefinedError during header.j2 rendering: {e}\n"
            f"Mechanism: {mech.name}, solver={solver_name}, adjoint={adjoint}\n"
            f"num_species={len(mech.species)}, "
            f"has_photolysis={context.get('has_photolysis')}, "
            f"has_equilibrium={context.get('has_equilibrium')}\n"
            f"Context keys: {sorted(context.keys())}"
        ) from e

    # Rendered output should be non-empty valid C++ text
    assert len(rendered) > 0, "Rendered header is empty"
    assert "#pragma once" in rendered or "namespace" in rendered, "Rendered header does not contain expected C++ markers"


@given(data=mechanism_with_blocks_strategy())
@settings(deadline=None)
def test_property_2_blocks_present_when_block_structure_exists(data):
    """
    When the LU plan contains block structure (multiple independent blocks),
    the context SHALL contain a `blocks` list with species-name annotations.

    This verifies Requirement 2.3: WHEN the LU_Plan contains block structure,
    THE Template_Context SHALL include a `blocks` list.

    **Validates: Requirements 2.1, 2.2, 2.3, 2.4, 6.4**
    """
    mech, solver_name, adjoint = data

    # Build context with a mechanism known to produce block-diagonal structure
    lowering_data = prepare_unified_jacobian(mech)
    lu_plan = compute_symbolic_lu_decomposition(
        lowering_data["jacobian_matrix"],
        lowering_data["species_map"],
    )

    # Force multi-block structure if lowering didn't detect it
    # (the A->B, C->D mechanism should produce blocks [[0,1],[2,3]])
    if lu_plan.blocks is None or len(lu_plan.blocks) <= 1:
        lu_plan.blocks = [[0, 1], [2, 3]]

    context = build_template_context(
        mech,
        solver_name=solver_name,
        lu_plan=lu_plan,
        sympy_meta=lowering_data,
        adjoint=adjoint,
    )

    # Verify blocks is present and has correct structure
    assert context["blocks"] is not None, "blocks should be non-None when LU plan has multi-block structure"
    assert len(context["blocks"]) == 2, f"Expected 2 blocks, got {len(context['blocks'])}"
    # Each block should have indices and species_names
    for block in context["blocks"]:
        assert "indices" in block, "Block missing 'indices' key"
        assert "species_names" in block, "Block missing 'species_names' key"
        assert len(block["indices"]) > 0, "Block has empty indices"
        assert len(block["species_names"]) == len(block["indices"]), "Block species_names length doesn't match indices length"

    # Rendering with blocks should also succeed without UndefinedError
    engine = TemplateEngine()
    try:
        rendered = engine.render("header.j2", context)
    except UndefinedError as e:
        raise AssertionError(
            f"UndefinedError during header.j2 rendering with blocks: {e}\n"
            f"Mechanism: {mech.name}, solver={solver_name}, adjoint={adjoint}\n"
            f"blocks={context['blocks']}\n"
            f"Context keys: {sorted(context.keys())}"
        ) from e

    assert len(rendered) > 0, "Rendered header with blocks is empty"
