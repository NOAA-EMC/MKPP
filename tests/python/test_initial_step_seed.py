"""Tests for the configurable Rosenbrock initial-step seed.

The generated implicit solver ramps its first internal substep from
``dt = dt_total * seed``.  Historically that seed was hardcoded to ``1.0e-6``
to match MICM's default, which forces ~ceil(log6(1e6)) >= 9 mandatory growth
substeps per host step regardless of tolerance -- a fixed floor on per-cell
cost.  This knob lets a mechanism author raise the seed (fewer ramp substeps)
or keep it tight, without touching generated C++ by hand.

Guarantees exercised here:
  * unset  -> the committed ``1.0e-6`` literal is emitted byte-for-byte, so the
    default artifact stays reproducible;
  * set    -> the value flows env YAML -> EnvironmentDefinition -> mechanism
    metadata -> template context -> generated header;
  * invalid -> fail loudly at context build (never emit a seed that can stall
    the integrator).
"""

import tempfile
from pathlib import Path

import pytest
from mkpp.codegen import generate_headers
from mkpp.model import AerosolRepresentation, MechanismDefinition, PhaseMode, SpeciesDefinition
from mkpp.parser import load_environment
from mkpp.template_context import build_template_context


def _minimal_mechanism() -> MechanismDefinition:
    """A single-species mechanism sufficient to render the integrate kernel."""
    mech = MechanismDefinition(
        name="seed_test",
        description="Minimal mechanism for initial-step seed tests",
        aerosol_representation=AerosolRepresentation.BULK,
        species=[SpeciesDefinition(name="O3", phase=PhaseMode.GAS)],
        phases=[],
        reactions=[],
    )
    return mech


def _rendered_seed_member(header_text: str) -> str:
    """Extract the baked token from the ``double initial_step_seed = <tok>;`` member.

    The seed is emitted as a public member of the solver struct so a host can
    override it at runtime without regenerating; the member's initializer is
    the compile-time value.  integrate() reads the member, so this is the only
    place the literal appears on the primary path.
    """
    prefix = "double initial_step_seed ="
    for line in header_text.splitlines():
        stripped = line.strip()
        if stripped.startswith(prefix):
            return stripped[len(prefix) :].rstrip(";").strip()
    raise AssertionError("no 'double initial_step_seed = <token>;' member found in header")


class TestParserReadsSeed:
    def test_seed_absent_is_none(self, tmp_path: Path):
        env_file = tmp_path / "env.yaml"
        env_file.write_text("solver: {rtol: 1.0e-6, atol: 1.0e-3}\n")
        env = load_environment(env_file)
        assert env.solver_initial_step_seed is None

    def test_seed_read_from_solver_block(self, tmp_path: Path):
        env_file = tmp_path / "env.yaml"
        env_file.write_text("solver: {initial_step_seed: 0.01}\n")
        env = load_environment(env_file)
        assert env.solver_initial_step_seed == pytest.approx(0.01)

    def test_seed_without_solver_block_is_none(self, tmp_path: Path):
        env_file = tmp_path / "env.yaml"
        env_file.write_text("environment: {temperature: 298.15}\n")
        env = load_environment(env_file)
        assert env.solver_initial_step_seed is None


class TestContextSeed:
    def test_default_context_seed_is_committed_literal(self):
        mech = _minimal_mechanism()
        context = build_template_context(mech, solver_name="ros3")
        # Byte-identity anchor: the default must be the exact committed token.
        assert context["initial_step_seed"] == "1.0e-6"

    def test_metadata_seed_overrides_context(self):
        mech = _minimal_mechanism()
        mech.metadata = {"initial_step_seed": 0.01}
        context = build_template_context(mech, solver_name="ros3")
        assert context["initial_step_seed"] == "0.01"

    @pytest.mark.parametrize("bad", [0.0, -1.0, float("nan"), float("inf")])
    def test_invalid_seed_fails_loudly(self, bad):
        mech = _minimal_mechanism()
        mech.metadata = {"initial_step_seed": bad}
        with pytest.raises(ValueError):
            build_template_context(mech, solver_name="ros3")


class TestHeaderSeed:
    def test_default_header_is_byte_identical_seed(self):
        mech = _minimal_mechanism()
        with tempfile.TemporaryDirectory() as tmpdir:
            results = generate_headers(mech, out_dir=tmpdir, solver_name="ros3")
            header_text = Path(results["header"]).read_text()
        assert _rendered_seed_member(header_text) == "1.0e-6"

    def test_override_header_uses_seed(self):
        mech = _minimal_mechanism()
        mech.metadata = {"initial_step_seed": 0.01}
        with tempfile.TemporaryDirectory() as tmpdir:
            results = generate_headers(mech, out_dir=tmpdir, solver_name="ros3")
            header_text = Path(results["header"]).read_text()
        assert _rendered_seed_member(header_text) == "0.01"


class TestRuntimeSeedMember:
    """The baked seed doubles as a public member initializer so a host can
    override it per solve without regenerating the artifact."""

    def _header(self, metadata=None) -> str:
        mech = _minimal_mechanism()
        if metadata:
            mech.metadata = metadata
        with tempfile.TemporaryDirectory() as tmpdir:
            results = generate_headers(mech, out_dir=tmpdir, solver_name="ros3")
            return Path(results["header"]).read_text()

    def test_default_header_declares_member_with_baked_literal(self):
        assert "double initial_step_seed = 1.0e-6;" in self._header()

    def test_override_header_bakes_configured_value(self):
        assert "double initial_step_seed = 0.01;" in self._header({"initial_step_seed": 0.01})

    def test_integrate_reads_the_member_not_a_literal(self):
        # integrate() must consume the member so a runtime override takes
        # effect; the literal may appear ONLY in the member initializer.
        text = self._header()
        assert "double dt = dt_total * initial_step_seed;" in text
        assert "double dt = dt_total * 1.0e-6;" not in text
