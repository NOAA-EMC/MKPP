"""Unit tests for TemplateEngine and build_template_context.

Task 1.4 - Tests cover:
1. TemplateEngine error paths: TemplateNotFound for nonexistent template,
   UndefinedError when context is missing required keys
2. build_template_context: produces all required keys for the Chapman mechanism,
   includes `blocks` when LU plan has block structure, includes transposed steps
   when adjoint=True, raises ValueError for empty mechanism

Requirements: 1.2, 2.1, 2.2, 2.3, 2.4, 6.3, 6.4
"""

import pytest
from jinja2 import UndefinedError
from jinja2.exceptions import TemplateNotFound
from mkpp.lowering import (
    compute_symbolic_lu_decomposition,
    prepare_unified_jacobian,
)
from mkpp.model import (
    AerosolRepresentation,
    MechanismDefinition,
    PhaseMode,
    ReactionDefinition,
    SpeciesDefinition,
    SymbolicLUPlan,
)
from mkpp.template_context import build_template_context
from mkpp.template_engine import TemplateEngine

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def chapman_mechanism():
    """3-species Chapman-like mechanism (O, O3, O1D) with non-trivial coupling."""
    sp_o = SpeciesDefinition(name="O", phase=PhaseMode.GAS)
    sp_o3 = SpeciesDefinition(name="O3", phase=PhaseMode.GAS)
    sp_o1d = SpeciesDefinition(name="O1D", phase=PhaseMode.GAS)

    r1 = ReactionDefinition(
        reaction_type="PHOTOLYSIS",
        reactants={"O3": 1.0},
        products={"O1D": 1.0, "O": 1.0},
        rate_expression="J1*O3",
        parameters={"A": "J1"},
        stiff=True,
    )
    r2 = ReactionDefinition(
        reaction_type="ARRHENIUS",
        reactants={"O": 1.0, "O3": 1.0},
        products={"O": 2.0},
        rate_expression="k2*O*O3",
        parameters={"A": 1e-15, "B": 0.0, "C": 0.0},
        stiff=True,
    )
    return MechanismDefinition(
        name="chapman_test",
        description="Chapman mechanism for template engine tests",
        aerosol_representation=AerosolRepresentation.BULK,
        species=[sp_o, sp_o3, sp_o1d],
        phases=[],
        reactions=[r1, r2],
    )


@pytest.fixture
def chapman_with_lu(chapman_mechanism):
    """Chapman mechanism with pre-computed LU plan attached."""
    lowering_data = prepare_unified_jacobian(chapman_mechanism)
    lu_plan = compute_symbolic_lu_decomposition(
        lowering_data["jacobian_matrix"],
        lowering_data["species_map"],
    )
    chapman_mechanism.metadata["sympy_metadata"] = lowering_data
    chapman_mechanism.metadata["symbolic_lu_plan"] = lu_plan
    return chapman_mechanism, lu_plan, lowering_data


# ---------------------------------------------------------------------------
# TemplateEngine tests
# ---------------------------------------------------------------------------


class TestTemplateEngineErrors:
    """Tests for TemplateEngine error paths (Requirements 1.2, 6.3, 6.4)."""

    def test_raises_template_not_found_for_missing_template(self):
        """TemplateEngine.render raises TemplateNotFound for a nonexistent template."""
        engine = TemplateEngine()
        with pytest.raises(TemplateNotFound):
            engine.render("nonexistent_template_xyz.j2", {})

    def test_raises_undefined_error_for_missing_context_keys(self, tmp_path):
        """TemplateEngine raises UndefinedError when template uses a missing variable."""
        # Create a minimal template that references a variable
        template_dir = tmp_path / "templates"
        template_dir.mkdir()
        (template_dir / "test.j2").write_text("Hello {{ name }}!")

        engine = TemplateEngine(template_dir=template_dir)
        with pytest.raises(UndefinedError):
            engine.render("test.j2", {})

    def test_template_not_found_contains_template_name(self):
        """The TemplateNotFound exception contains the name of the missing template."""
        engine = TemplateEngine()
        with pytest.raises(TemplateNotFound, match="missing_abc_xyz.j2"):
            engine.render("missing_abc_xyz.j2", {})

    def test_undefined_error_contains_variable_name(self, tmp_path):
        """The UndefinedError exception contains the name of the undefined variable."""
        template_dir = tmp_path / "templates"
        template_dir.mkdir()
        (template_dir / "test.j2").write_text("{{ some_variable }}")

        engine = TemplateEngine(template_dir=template_dir)
        with pytest.raises(UndefinedError, match="some_variable"):
            engine.render("test.j2", {})


# ---------------------------------------------------------------------------
# build_template_context tests
# ---------------------------------------------------------------------------


class TestBuildTemplateContextChapman:
    """Tests for build_template_context producing correct keys (Requirements 2.1, 2.2)."""

    def test_produces_all_required_keys(self, chapman_with_lu):
        """build_template_context returns dict with all required keys for Chapman."""
        mech, lu_plan, lowering_data = chapman_with_lu
        ctx = build_template_context(mech, solver_name="ros3", lu_plan=lu_plan, sympy_meta=lowering_data)

        # All required keys from Requirement 2.1
        required_keys = [
            "mechanism_name",
            "species",
            "num_species",
            "tableau",
            "lu_expressions",
            "forward_sub_steps",
            "backward_sub_steps",
            "needed_w",
            "non_zero_jac_set",
            "jacobian_entries",
            "f_exprs",
            "permutation",
            "adjoint_enabled",
            "has_equilibrium",
            "has_cloud_gated",
            "has_photolysis",
            "num_photolysis",
            "tolerance_arrays",
        ]
        for key in required_keys:
            assert key in ctx, f"Missing required key: {key}"

    def test_mechanism_name_matches(self, chapman_with_lu):
        """Context mechanism_name matches the input mechanism name."""
        mech, lu_plan, lowering_data = chapman_with_lu
        ctx = build_template_context(mech, solver_name="ros3", lu_plan=lu_plan, sympy_meta=lowering_data)
        assert ctx["mechanism_name"] == "chapman_test"

    def test_species_count_matches(self, chapman_with_lu):
        """Context num_species matches the mechanism's species count."""
        mech, lu_plan, lowering_data = chapman_with_lu
        ctx = build_template_context(mech, solver_name="ros3", lu_plan=lu_plan, sympy_meta=lowering_data)
        assert ctx["num_species"] == 3
        assert len(ctx["species"]) == 3

    def test_species_have_correct_structure(self, chapman_with_lu):
        """Each species entry has name, index, and elements."""
        mech, lu_plan, lowering_data = chapman_with_lu
        ctx = build_template_context(mech, solver_name="ros3", lu_plan=lu_plan, sympy_meta=lowering_data)
        for idx, sp in enumerate(ctx["species"]):
            assert "name" in sp
            assert "index" in sp
            assert "elements" in sp
            assert sp["index"] == idx

    def test_tableau_contains_required_fields(self, chapman_with_lu):
        """Tableau dictionary has all required solver coefficient fields."""
        mech, lu_plan, lowering_data = chapman_with_lu
        ctx = build_template_context(mech, solver_name="ros3", lu_plan=lu_plan, sympy_meta=lowering_data)
        tableau = ctx["tableau"]
        required_tableau_keys = [
            "name",
            "stages",
            "ELO",
            "Gamma",
            "M",
            "E",
            "Alpha",
            "NewF",
            "A_matrix",
            "C_matrix",
        ]
        for key in required_tableau_keys:
            assert key in tableau, f"Missing tableau key: {key}"
        assert tableau["name"] == "ROS-3"
        assert tableau["stages"] == 3

    def test_lu_expressions_are_present(self, chapman_with_lu):
        """LU expressions list is non-empty for Chapman mechanism."""
        mech, lu_plan, lowering_data = chapman_with_lu
        ctx = build_template_context(mech, solver_name="ros3", lu_plan=lu_plan, sympy_meta=lowering_data)
        assert len(ctx["lu_expressions"]) > 0
        # Each expression should have kind, i, j, expr
        for expr in ctx["lu_expressions"]:
            assert "kind" in expr
            assert "i" in expr
            assert "j" in expr
            assert "expr" in expr
            assert expr["kind"] in ("L", "U")

    def test_forward_backward_sub_steps_present(self, chapman_with_lu):
        """Forward and backward substitution steps are present and non-empty."""
        mech, lu_plan, lowering_data = chapman_with_lu
        ctx = build_template_context(mech, solver_name="ros3", lu_plan=lu_plan, sympy_meta=lowering_data)
        assert len(ctx["forward_sub_steps"]) == 3
        assert len(ctx["backward_sub_steps"]) == 3
        for step in ctx["forward_sub_steps"]:
            assert "i" in step
            assert "raw_expr" in step

    def test_needed_w_includes_diagonal(self, chapman_with_lu):
        """needed_w always includes diagonal entries for each species."""
        mech, lu_plan, lowering_data = chapman_with_lu
        ctx = build_template_context(mech, solver_name="ros3", lu_plan=lu_plan, sympy_meta=lowering_data)
        for i in range(ctx["num_species"]):
            assert (i, i) in ctx["needed_w"]

    def test_photolysis_detected(self, chapman_with_lu):
        """Chapman mechanism has photolysis reactions detected."""
        mech, lu_plan, lowering_data = chapman_with_lu
        ctx = build_template_context(mech, solver_name="ros3", lu_plan=lu_plan, sympy_meta=lowering_data)
        assert ctx["has_photolysis"] is True
        assert ctx["num_photolysis"] > 0

    def test_tolerance_arrays_correct_length(self, chapman_with_lu):
        """Tolerance arrays have correct length (one per species)."""
        mech, lu_plan, lowering_data = chapman_with_lu
        ctx = build_template_context(mech, solver_name="ros3", lu_plan=lu_plan, sympy_meta=lowering_data)
        assert len(ctx["tolerance_arrays"]["atol"]) == 3
        assert len(ctx["tolerance_arrays"]["rtol"]) == 3


class TestBuildTemplateContextBlocks:
    """Tests for build_template_context block structure (Requirement 2.3)."""

    def test_includes_blocks_when_lu_plan_has_block_structure(self):
        """Context includes `blocks` when LU plan has multi-block structure."""
        # Create a mechanism with a block-diagonal LU plan
        sp_a = SpeciesDefinition(name="A", phase=PhaseMode.GAS)
        sp_b = SpeciesDefinition(name="B", phase=PhaseMode.GAS)
        sp_c = SpeciesDefinition(name="C", phase=PhaseMode.GAS)
        sp_d = SpeciesDefinition(name="D", phase=PhaseMode.GAS)

        rxn1 = ReactionDefinition(
            reaction_type="ARRHENIUS",
            reactants={"A": 1.0},
            products={"B": 1.0},
            rate_expression="k1*A",
            parameters={"A": 1e-3, "B": 0.0, "C": 0.0},
            stiff=True,
        )
        rxn2 = ReactionDefinition(
            reaction_type="ARRHENIUS",
            reactants={"C": 1.0},
            products={"D": 1.0},
            rate_expression="k2*C",
            parameters={"A": 2e-3, "B": 0.0, "C": 0.0},
            stiff=True,
        )
        mech = MechanismDefinition(
            name="block_test",
            description="Mechanism with block-diagonal structure",
            aerosol_representation=AerosolRepresentation.BULK,
            species=[sp_a, sp_b, sp_c, sp_d],
            phases=[],
            reactions=[rxn1, rxn2],
        )

        # Create a mock LU plan with explicit block structure
        lu_plan = SymbolicLUPlan(
            num_species=4,
            species_map=["A", "B", "C", "D"],
            non_zero_jacobian=[
                (0, 0, "-k1"),
                (1, 0, "k1"),
                (2, 2, "-k2"),
                (3, 2, "k2"),
            ],
            lu_expressions_ordered=[
                ("U", 0, 0, "W_0_0"),
                ("U", 1, 1, "W_1_1"),
                ("U", 2, 2, "W_2_2"),
                ("U", 3, 3, "W_3_3"),
            ],
            forward_sub_steps=[
                (0, "b_0"),
                (1, "b_1"),
                (2, "b_2"),
                (3, "b_3"),
            ],
            backward_sub_steps=[
                (3, "y_3 / U_3_3"),
                (2, "y_2 / U_2_2"),
                (1, "y_1 / U_1_1"),
                (0, "y_0 / U_0_0"),
            ],
            blocks=[[0, 1], [2, 3]],  # Two separate blocks
        )

        lowering_data = prepare_unified_jacobian(mech)
        ctx = build_template_context(mech, solver_name="ros3", lu_plan=lu_plan, sympy_meta=lowering_data)

        assert ctx["blocks"] is not None
        assert len(ctx["blocks"]) == 2
        assert ctx["blocks"][0]["indices"] == [0, 1]
        assert ctx["blocks"][0]["species_names"] == ["A", "B"]
        assert ctx["blocks"][1]["indices"] == [2, 3]
        assert ctx["blocks"][1]["species_names"] == ["C", "D"]

    def test_blocks_is_none_when_single_block(self, chapman_with_lu):
        """Context blocks is None when LU plan has only a single block."""
        mech, lu_plan, lowering_data = chapman_with_lu
        # Single block means all species in one block - treated as no block structure
        lu_plan.blocks = [[0, 1, 2]]

        ctx = build_template_context(mech, solver_name="ros3", lu_plan=lu_plan, sympy_meta=lowering_data)
        # Single block is treated as no meaningful block structure
        assert ctx["blocks"] is None


class TestBuildTemplateContextAdjoint:
    """Tests for build_template_context adjoint mode (Requirement 2.4)."""

    def test_includes_transposed_steps_when_adjoint_true(self, chapman_with_lu):
        """Context includes transpose steps when adjoint=True."""
        mech, lu_plan, lowering_data = chapman_with_lu

        ctx = build_template_context(
            mech,
            solver_name="ros3",
            lu_plan=lu_plan,
            sympy_meta=lowering_data,
            adjoint=True,
        )

        assert ctx["adjoint_enabled"] is True
        assert "transpose_forward_sub_steps" in ctx
        assert "transpose_backward_sub_steps" in ctx
        assert ctx["transpose_forward_sub_steps"] is not None
        assert ctx["transpose_backward_sub_steps"] is not None
        # Should have same number of steps as regular substitution
        assert len(ctx["transpose_forward_sub_steps"]) == 3
        assert len(ctx["transpose_backward_sub_steps"]) == 3

    def test_transposed_steps_have_correct_structure(self, chapman_with_lu):
        """Transposed substitution steps have i and raw_expr fields."""
        mech, lu_plan, lowering_data = chapman_with_lu

        ctx = build_template_context(
            mech,
            solver_name="ros3",
            lu_plan=lu_plan,
            sympy_meta=lowering_data,
            adjoint=True,
        )

        for step in ctx["transpose_forward_sub_steps"]:
            assert "i" in step
            assert "raw_expr" in step
        for step in ctx["transpose_backward_sub_steps"]:
            assert "i" in step
            assert "raw_expr" in step

    def test_adjoint_disabled_by_default(self, chapman_with_lu):
        """When adjoint=False, transposed steps are not in context."""
        mech, lu_plan, lowering_data = chapman_with_lu

        ctx = build_template_context(mech, solver_name="ros3", lu_plan=lu_plan, sympy_meta=lowering_data)

        assert ctx["adjoint_enabled"] is False
        assert "transpose_forward_sub_steps" not in ctx
        assert "transpose_backward_sub_steps" not in ctx


class TestBuildTemplateContextErrors:
    """Tests for build_template_context error cases (Requirements 2.1, 6.4)."""

    def test_raises_value_error_for_empty_mechanism(self):
        """build_template_context raises ValueError for mechanism with no species."""
        mech = MechanismDefinition(
            name="empty_mech",
            description="Empty mechanism",
            aerosol_representation=AerosolRepresentation.BULK,
            species=[],
            phases=[],
            reactions=[],
        )
        with pytest.raises(ValueError, match="empty mechanism"):
            build_template_context(mech)

    def test_raises_value_error_for_none_mechanism(self):
        """build_template_context raises ValueError for None mechanism."""
        with pytest.raises((ValueError, TypeError, AttributeError)):
            build_template_context(None)

    def test_raises_key_error_for_invalid_solver(self, chapman_with_lu):
        """build_template_context raises KeyError for invalid solver name."""
        mech, lu_plan, lowering_data = chapman_with_lu
        with pytest.raises(KeyError):
            build_template_context(
                mech,
                solver_name="nonexistent_solver_xyz",
                lu_plan=lu_plan,
                sympy_meta=lowering_data,
            )


# ---------------------------------------------------------------------------
# sub_prefixes filter tests (Task 1.3, Requirements 3.3, 3.4)
# ---------------------------------------------------------------------------


class TestSubPrefixesFilter:
    """Tests for the sub_prefixes Jinja2 custom filter."""

    def test_replaces_b_prefix_with_rhs(self):
        """b_<digits> is replaced with the rhs prefix."""
        from mkpp.template_engine import _sub_prefixes

        assert _sub_prefixes("b_0", rhs="F1", y="y1", x="K1") == "F1_0"
        assert _sub_prefixes("b_12", rhs="rhs3", y="y3", x="K3") == "rhs3_12"

    def test_replaces_y_prefix(self):
        """y_<digits> is replaced with the y prefix."""
        from mkpp.template_engine import _sub_prefixes

        assert _sub_prefixes("y_2 / U_2_2", rhs="rhs1", y="y1", x="K1") == "y1_2 / U_2_2"

    def test_replaces_x_prefix(self):
        """x_<digits> is replaced with the x prefix."""
        from mkpp.template_engine import _sub_prefixes

        assert _sub_prefixes("x_0 + x_1", rhs="rhs1", y="y1", x="K1") == "K1_0 + K1_1"

    def test_combined_forward_sub_pattern(self):
        """Forward substitution: b_i and y_i replaced simultaneously."""
        from mkpp.template_engine import _sub_prefixes

        result = _sub_prefixes("b_0 - L_1_0 * y_0", rhs="F1", y="y1", x="K1")
        assert result == "F1_0 - L_1_0 * y1_0"

    def test_combined_backward_sub_pattern(self):
        """Backward substitution: y_i and x_i replaced simultaneously."""
        from mkpp.template_engine import _sub_prefixes

        result = _sub_prefixes("y_1 - U_1_0 * x_0", rhs="v1", y="yt1", x="u1")
        assert result == "yt1_1 - U_1_0 * u1_0"

    def test_does_not_replace_non_matching_prefixes(self):
        """L_, U_, W_ prefixes are NOT substituted."""
        from mkpp.template_engine import _sub_prefixes

        expr = "L_1_0 * W_0_0 + U_2_2"
        assert _sub_prefixes(expr, rhs="F1", y="y1", x="K1") == expr

    def test_word_boundary_prevents_partial_match(self):
        """Word boundaries prevent replacing digits within L_1_0 style tokens."""
        from mkpp.template_engine import _sub_prefixes

        # "b_0" inside a larger identifier shouldn't match
        # But "b_0" as a standalone word should
        assert _sub_prefixes("ab_0", rhs="F1", y="y1", x="K1") == "ab_0"
        assert _sub_prefixes("b_0a", rhs="F1", y="y1", x="K1") == "b_0a"

    def test_multi_digit_indices(self):
        """Multi-digit indices are handled correctly."""
        from mkpp.template_engine import _sub_prefixes

        result = _sub_prefixes("b_12 + y_34 - x_56", rhs="F1", y="y1", x="K1")
        assert result == "F1_12 + y1_34 - K1_56"

    def test_filter_registered_on_engine(self, tmp_path):
        """sub_prefixes filter is available in templates rendered by TemplateEngine."""
        template_dir = tmp_path / "templates"
        template_dir.mkdir()
        (template_dir / "test.j2").write_text("{{ expr | sub_prefixes(rhs=rhs_prefix, y=y_prefix, x=x_prefix) }}")

        engine = TemplateEngine(template_dir=template_dir)
        result = engine.render(
            "test.j2",
            {
                "expr": "b_0 - L_1_0 * y_0",
                "rhs_prefix": "F1",
                "y_prefix": "y1",
                "x_prefix": "K1",
            },
        )
        assert result == "F1_0 - L_1_0 * y1_0"

    def test_filter_with_partial_args(self, tmp_path):
        """sub_prefixes filter works with only some prefixes specified."""
        template_dir = tmp_path / "templates"
        template_dir.mkdir()
        (template_dir / "test.j2").write_text("{{ expr | sub_prefixes(rhs=rhs_prefix) }}")

        engine = TemplateEngine(template_dir=template_dir)
        result = engine.render(
            "test.j2",
            {
                "expr": "b_0 + y_1",
                "rhs_prefix": "F1",
            },
        )
        # b_0 gets replaced, y_1 uses default (y) so stays as y_1
        assert result == "F1_0 + y_1"
