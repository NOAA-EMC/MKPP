"""Tests for the pure-Python MKPP box model (``mkpp.box``).

The box model reuses the SymPy lowering pipeline (Unified Jacobian + rate
vector) and integrates with SciPy. Correctness is anchored against the
committed SciPy Radau reference used by the C++ e2e validation suite
(``tests/integration/e2e_validation/data/chapman_reference.json``).
"""

from pathlib import Path

import numpy as np
import pytest

from mkpp.box import BoxModel, BoxModelResult, main

REPO_ROOT = Path(__file__).resolve().parents[2]
CHAPMAN = REPO_ROOT / "mechanisms" / "openatmos" / "chapman" / "mechanism.json"
SMALL_STRATO = REPO_ROOT / "mechanisms" / "openatmos" / "small_strato" / "mechanism.json"
TS1 = REPO_ROOT / "mechanisms" / "openatmos" / "ts1" / "mechanism.json"
CHAPMAN_REFERENCE = REPO_ROOT / "tests" / "integration" / "e2e_validation" / "data" / "chapman_reference.json"


def make_chapman_box() -> BoxModel:
    box = BoxModel(CHAPMAN)
    box.set_initial_concentrations({"O": 1.0e10, "O2": 2.0e10, "O3": 3.0e10, "M": 4.0e10})
    box.set_photolysis({0: 2.0e-5, 1: 1.0e-3})
    return box


class TestChapmanAgainstSciPyReference:
    """The box model must reproduce the committed SciPy Radau reference."""

    def test_final_state_matches_reference(self):
        reference = np.array(__import__("json").load(open(CHAPMAN_REFERENCE))["expected_final"])
        result = make_chapman_box().simulate(t_end=3600.0, dt_out=600.0)
        np.testing.assert_allclose(result.y[:, -1], reference, rtol=1e-6)

    def test_fixed_species_is_conserved(self):
        result = make_chapman_box().simulate(t_end=3600.0, dt_out=600.0)
        m_row = result.y[result.species.index("M")]
        np.testing.assert_allclose(m_row, 4.0e10, rtol=0.0, atol=1e-3)

    def test_result_convenience_views(self):
        result = make_chapman_box().simulate(t_end=600.0, dt_out=60.0)
        assert isinstance(result, BoxModelResult)
        assert set(result.concentrations) == set(result.species)
        assert result.final["M"] == pytest.approx(4.0e10)
        assert result.t[0] == 0.0 and result.t[-1] == 600.0


class TestPhotolysisResolution:
    def test_species_name_keyed_equals_index_keyed(self):
        by_index = make_chapman_box().simulate(t_end=3600.0, dt_out=1800.0)
        box = BoxModel(CHAPMAN)
        box.set_initial_concentrations({"O": 1.0e10, "O2": 2.0e10, "O3": 3.0e10, "M": 4.0e10})
        box.set_photolysis({"O2": 2.0e-5, "O3": 1.0e-3})
        by_name = box.simulate(t_end=3600.0, dt_out=1800.0)
        np.testing.assert_allclose(by_index.y, by_name.y, rtol=1e-9)

    def test_unknown_photolysis_species_raises(self):
        with pytest.raises(KeyError, match="No PHOTOLYSIS reaction"):
            make_chapman_box().set_photolysis({"NOPE": 1e-3})


class TestForcing:
    def test_emission_and_first_order_loss_analytic(self):
        """With J=0 and zero reagents, M (fixed) evolves as dM/dt = E - k*M."""
        box = BoxModel(CHAPMAN)
        box.set_initial_concentrations({"O": 0.0, "O2": 0.0, "O3": 0.0, "M": 1.0e10})
        box.set_emissions({"M": 1.0e9})
        box.set_first_order_loss({"M": 0.01})
        result = box.simulate(t_end=100.0, dt_out=10.0)
        e, k, m0 = 1.0e9, 0.01, 1.0e10
        expected = e / k + (m0 - e / k) * np.exp(-k * result.t)
        m_row = result.y[result.species.index("M")]
        np.testing.assert_allclose(m_row, expected, rtol=1e-6)

    def test_unknown_species_in_forcing_raises(self):
        box = BoxModel(CHAPMAN)
        with pytest.raises(KeyError, match="Unknown species"):
            box.set_emissions({"FAKE": 1.0})


class TestValidation:
    def test_missing_initial_concentration_raises(self):
        box = BoxModel(CHAPMAN)
        box.set_initial_concentrations({"O": 1e10})
        with pytest.raises(ValueError, match="No initial concentration set"):
            box.simulate(t_end=10.0)

    def test_unknown_species_initial_raises(self):
        with pytest.raises(KeyError, match="Unknown species"):
            BoxModel(CHAPMAN).set_initial_concentrations({"XYZ": 1.0})

    def test_nonpositive_t_end_raises(self):
        with pytest.raises(ValueError, match="t_end must be positive"):
            make_chapman_box().simulate(t_end=0.0)


class TestOtherMechanisms:
    def test_small_strato_day(self):
        box = BoxModel(SMALL_STRATO)
        box.set_initial_concentrations({s: 1.0e12 for s in box.species})
        for name in box._param_index:  # noqa: SLF001 - test reaches into internals deliberately
            idx = int(name.split("_")[1])
            if name.startswith("J_"):
                box.set_photolysis({idx: 1.0e-3})
            else:
                box.set_external_rate(idx, 0.0)
        result = box.simulate(t_end=86400.0, dt_out=3600.0, rtol=1e-8, atol=1e-8)
        assert np.all(np.isfinite(result.y))
        assert np.all(result.y >= -1e-6)

    @pytest.mark.slow
    def test_ts1_builds_large_mechanism(self):
        """TS1 (210 species) exercises environment-symbol substitution at scale."""
        box = BoxModel(TS1)
        assert len(box.species) > 100
        assert any(n.startswith("J_") for n in box._param_index)


class TestCli:
    def test_cli_runs_and_writes_csv(self, tmp_path, capsys):
        out_csv = tmp_path / "traj.csv"
        rc = main(
            [
                str(CHAPMAN),
                "--t-end",
                "600",
                "--dt-out",
                "60",
                "--conc",
                "O=1e10",
                "--conc",
                "O2=2e10",
                "--conc",
                "O3=3e10",
                "--conc",
                "M=4e10",
                "--jval",
                "O2=2e-5",
                "--jval",
                "O3=1e-3",
                "--out",
                str(out_csv),
            ]
        )
        assert rc == 0
        header = capsys.readouterr().out.splitlines()[0]
        assert header == "time_s,O,O2,O3,M"
        assert out_csv.exists()
        data = np.loadtxt(out_csv, delimiter=",", skiprows=1)
        assert data[-1, 4] == pytest.approx(4.0e10)
