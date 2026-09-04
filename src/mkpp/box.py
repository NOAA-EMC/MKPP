"""Zero-dimensional chemical box model driven by the MKPP symbolic lowering engine.

This module reuses the same SymPy lowering pipeline that generates the Kokkos
C++ solvers (:func:`mkpp.lowering.prepare_unified_jacobian`) but evaluates the
Unified Jacobian and rate vector numerically in Python. The resulting ODE
system is integrated with SciPy (``solve_ivp``), which makes it possible to
run a mechanism as a box model without compiling any C++ code.

Typical usage::

    from mkpp.box import BoxModel

    box = BoxModel("mechanisms/openatmos/chapman/mechanism.json")
    box.set_initial_concentrations({"O": 1.0e10, "O2": 2.0e10, "O3": 3.0e10, "M": 4.0e10})
    box.set_photolysis({0: 2.0e-5, 1: 1.0e-3})
    result = box.simulate(t_end=3600.0, dt_out=60.0)
    print(result.concentrations["O3"][-1])

Units follow the MKPP canonical policy (molecules cm^-3, s, K).
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import sympy as sp

from .lowering import prepare_unified_jacobian
from .model import MechanismDefinition
from .parser import load_mechanism

__all__ = ["BoxModel", "BoxModelResult"]

_STATE_RE = re.compile(r"^C_(?P<name>\w+)$")
_PARAM_RE = re.compile(r"^(?:J|Rate)_(?P<idx>\d+)$")

# Environmental symbols substituted with scalar constants at construction time.
_ENV_SYMBOL_NAMES = ("Temp", "RH", "M_density", "Press")


@dataclass
class BoxModelResult:
    """Container for a completed box-model integration.

    Attributes:
        t: 1-D array of output times (s).
        y: 2-D array of concentrations with shape ``(n_species, n_times)``.
        species: Ordered species names matching the rows of :attr:`y`.
        method: Integrator method that produced the result.
        scipy_message: Status message reported by ``scipy.integrate.solve_ivp``.
    """

    t: np.ndarray
    y: np.ndarray
    species: list[str]
    method: str = "Radau"
    scipy_message: str = ""

    @property
    def concentrations(self) -> dict[str, np.ndarray]:
        """Time series keyed by species name."""
        return {name: self.y[i] for i, name in enumerate(self.species)}

    @property
    def final(self) -> dict[str, float]:
        """Final concentration of every species."""
        return {name: float(self.y[i, -1]) for i, name in enumerate(self.species)}

    def to_dataframe(self):
        """Return a ``pandas.DataFrame`` of the trajectory (requires pandas)."""
        import pandas as pd

        data = {"time_s": self.t}
        data.update({name: self.y[i] for i, name in enumerate(self.species)})
        return pd.DataFrame(data)


class BoxModel:
    """0-D chemical box model built from the MKPP symbolic lowering engine.

    The mechanism's Unified Jacobian and rate vector are lowered once with
    :func:`mkpp.lowering.prepare_unified_jacobian`, then numerically lambdified
    against a flat concentration vector and a flat parameter vector containing
    photolysis frequencies (``J_<n>``) and externally supplied reaction rates
    (``Rate_<n>`` from PHASE_CHANGE/TUNNELING reactions).

    Args:
        mechanism: Path to an OpenAtmos YAML/JSON mechanism, a YAML/JSON dict,
            or an already-parsed :class:`mkpp.model.MechanismDefinition`.
        temperature: Temperature in K (substituted into Arrhenius/Troe rates).
        relative_humidity: Relative humidity (0-1) substituted into ``RH``.
        air_density: Air number density (molecules cm^-3) substituted into
            ``M_density`` when a mechanism has no explicit ``M``/``AIR`` species.
        pressure: Pressure in Pa substituted into ``Press`` if referenced.
    """

    def __init__(
        self,
        mechanism: str | Path | dict[str, Any] | MechanismDefinition,
        *,
        temperature: float = 298.15,
        relative_humidity: float = 0.5,
        air_density: float = 2.46e19,
        pressure: float = 101325.0,
    ) -> None:
        if isinstance(mechanism, MechanismDefinition):
            self.mech = mechanism
        elif isinstance(mechanism, dict):
            from .parser import parse_mechanism_micm

            self.mech = parse_mechanism_micm(str(mechanism.get("name", "box")), mechanism)
        else:
            self.mech = load_mechanism(mechanism)

        self.temperature = float(temperature)
        self.relative_humidity = float(relative_humidity)
        self.air_density = float(air_density)
        self.pressure = float(pressure)

        self._initial: dict[str, float] = {}
        self._emissions: dict[str, float] = {}
        self._deposition: dict[str, float] = {}
        self._jvals: dict[int, float] = {}
        self._external_rates: dict[int, float] = {}

        lowered = prepare_unified_jacobian(self.mech)
        self.species: list[str] = list(lowered["species_map"])
        self._c_vector: sp.Matrix = sp.Matrix([sp.Symbol(f"C_{n}") for n in self.species])

        # Symbols created by the lowering engine carry assumptions
        # (real=True, nonnegative=True), so they must be matched by name from
        # the expressions' own free-symbol sets rather than by freshly built
        # symbols.
        f_total = lowered["f_implicit"] + lowered["f_explicit"]
        jacobian = lowered["jacobian_matrix"]
        free_syms: dict[str, sp.Symbol] = {}
        for expr in list(f_total) + list(jacobian):
            for sym in expr.free_symbols:
                free_syms.setdefault(str(sym), sym)

        env_values = {
            "Temp": self.temperature,
            "RH": self.relative_humidity,
            "M_density": self.air_density,
            "Press": self.pressure,
            # Aerosol surface area / gas-phase volume factors default to unity,
            # matching the codegen emission defaults in ``format_eqn``.
            "S_a": 1.0,
            "v_gas": 1.0,
        }
        env_subs = {free_syms[k]: sp.Float(v) for k, v in env_values.items() if k in free_syms}

        # ``subs`` is cheap and preserves the expressions the lowering engine
        # already produced; a full ``simplify`` pass on the Jacobian is
        # prohibitively slow beyond a handful of species.
        f_total = f_total.subs(env_subs, simultaneous=True)
        jacobian = jacobian.subs(env_subs, simultaneous=True)

        # Collect the remaining free symbols: species (C_X) and runtime
        # parameters (J_<n>, Rate_<n>). Anything else is an unsupported symbol.
        param_syms: dict[str, sp.Symbol] = {}
        for expr in list(f_total) + list(jacobian):
            for sym in expr.free_symbols:
                name = str(sym)
                if _STATE_RE.match(name):
                    continue
                if _PARAM_RE.match(name):
                    param_syms[name] = sym
                    continue
                raise ValueError(
                    f"Box model cannot resolve symbol '{name}' in mechanism "
                    f"'{self.mech.name}'. Only C_<species>, J_<n>, Rate_<n>, "
                    f"and {_ENV_SYMBOL_NAMES} are supported."
                )

        self._param_names = sorted(param_syms, key=lambda n: (n.split("_")[0], int(n.split("_")[1])))
        self._param_syms = [param_syms[n] for n in self._param_names]
        self._param_index = {n: i for i, n in enumerate(self._param_names)}
        self._n = len(self.species)

        self._rhs = sp.lambdify((self._c_vector, sp.Matrix(self._param_syms)), f_total, modules="numpy")

        # The Unified Jacobian is block-sparse; for large mechanisms a dense
        # lambdify evaluates thousands of identically-zero entries per step.
        # Lambdify only the structurally non-zero entries and scatter them into
        # a dense buffer (SciPy's Radau/BDF accept a dense Jacobian callable).
        self._jac_rows: list[int] = []
        self._jac_cols: list[int] = []
        nz_exprs: list[sp.Basic] = []
        for i in range(self._n):
            for j in range(self._n):
                entry = jacobian[i, j]
                if entry != 0:
                    self._jac_rows.append(i)
                    self._jac_cols.append(j)
                    nz_exprs.append(entry)
        self._jac_nz = sp.lambdify((self._c_vector, sp.Matrix(self._param_syms)), nz_exprs, modules="numpy") if nz_exprs else None

    # ------------------------------------------------------------------
    # Configuration API
    # ------------------------------------------------------------------
    def set_initial_concentrations(self, concentrations: dict[str, float]) -> BoxModel:
        """Set initial concentrations (molecules cm^-3) keyed by species name."""
        for name in concentrations:
            if name not in self.species:
                raise KeyError(f"Unknown species '{name}'. Mechanism species: {self.species}")
        self._initial.update({k: float(v) for k, v in concentrations.items()})
        return self

    def set_photolysis(self, jvals: dict[int | str, float]) -> BoxModel:
        """Set photolysis frequencies (s^-1).

        Keys are either the photolysis index ``J_<n>`` (int or ``"J_0"``) or the
        name of the photolyzed reactant species (e.g. ``"O3"``).
        """
        for key, value in jvals.items():
            idx = self._resolve_photolysis_index(key)
            self._jvals[idx] = float(value)
        return self

    def set_external_rate(self, reaction_index: int, rate: float) -> BoxModel:
        """Set an externally supplied ``Rate_<n>`` tendency (e.g. PHASE_CHANGE)."""
        self._external_rates[int(reaction_index)] = float(rate)
        return self

    def set_emissions(self, emissions: dict[str, float]) -> BoxModel:
        """Set constant emission tendencies (molecules cm^-3 s^-1) per species."""
        for name in emissions:
            if name not in self.species:
                raise KeyError(f"Unknown species '{name}'. Mechanism species: {self.species}")
        self._emissions.update({k: float(v) for k, v in emissions.items()})
        return self

    def set_first_order_loss(self, losses: dict[str, float]) -> BoxModel:
        """Set first-order wall/dry-deposition loss frequencies (s^-1) per species."""
        for name in losses:
            if name not in self.species:
                raise KeyError(f"Unknown species '{name}'. Mechanism species: {self.species}")
        self._deposition.update({k: float(v) for k, v in losses.items()})
        return self

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _resolve_photolysis_index(self, key: int | str) -> int:
        """Map a J-index, ``"J_<n>"`` string, or photolyzed species name to ``<n>``.

        Photolysis indices are assigned in mechanism-declaration order by
        :func:`mkpp.lowering._evaluate_reaction_fluxes`, so the same traversal
        is repeated here to resolve a species name back to its ``J_<n>`` symbol.
        """
        if isinstance(key, int):
            return key
        m = re.match(r"^J_(\d+)$", str(key))
        if m:
            return int(m.group(1))
        photo_idx = 0
        matches: list[int] = []
        for r in self.mech.reactions:
            if r.reaction_type.upper() == "PHOTOLYSIS":
                if any(reactant == str(key) for reactant in r.reactants):
                    matches.append(photo_idx)
                photo_idx += 1
        if not matches:
            raise KeyError(f"No PHOTOLYSIS reaction found for species '{key}' in mechanism '{self.mech.name}'.")
        if len(matches) > 1:
            raise KeyError(
                f"Species '{key}' photolyzes in multiple reactions {matches}; select by J-index (e.g. J_{matches[0]}) instead."
            )
        return matches[0]

    def _param_vector(self) -> np.ndarray:
        vec = np.zeros(len(self._param_names))
        for idx, value in self._jvals.items():
            name = f"J_{idx}"
            if name in self._param_index:
                vec[self._param_index[name]] = value
        for idx, value in self._external_rates.items():
            name = f"Rate_{idx}"
            if name in self._param_index:
                vec[self._param_index[name]] = value
        return vec

    def _y0(self) -> np.ndarray:
        missing = [n for n in self.species if n not in self._initial]
        if missing:
            raise ValueError(f"No initial concentration set for species: {missing}")
        return np.array([self._initial[n] for n in self.species], dtype=float)

    def _rhs_callable(self, t: float, y: np.ndarray, p: np.ndarray) -> np.ndarray:
        dydt = np.asarray(self._rhs(y, p), dtype=float).reshape(-1)
        for name, rate in self._emissions.items():
            dydt[self.species.index(name)] += rate
        for name, kloss in self._deposition.items():
            dydt[self.species.index(name)] -= kloss * y[self.species.index(name)]
        return dydt

    def _jac_callable(self, t: float, y: np.ndarray, p: np.ndarray) -> np.ndarray:
        J = np.zeros((self._n, self._n))
        if self._jac_nz is not None:
            values = np.asarray(self._jac_nz(y, p), dtype=float).reshape(-1)
            J[np.asarray(self._jac_rows), np.asarray(self._jac_cols)] = values
        for name, kloss in self._deposition.items():
            J[self.species.index(name), self.species.index(name)] -= kloss
        return J

    # ------------------------------------------------------------------
    # Integration
    # ------------------------------------------------------------------
    def simulate(
        self,
        t_end: float,
        *,
        dt_out: float | None = None,
        t_eval: np.ndarray | None = None,
        method: str = "Radau",
        rtol: float = 1.0e-10,
        atol: float = 1.0e-12,
        max_step: float = np.inf,
    ) -> BoxModelResult:
        """Integrate the box chemistry from t=0 to ``t_end`` seconds.

        Args:
            t_end: Simulation length (s). Must be positive.
            dt_out: Output sampling interval (s). Ignored when ``t_eval`` is given.
            t_eval: Explicit output time grid (s). Defaults to 101 uniform points.
            method: ``scipy.integrate.solve_ivp`` method. ``"Radau"`` (default),
                ``"BDF"``, ``"LSODA"`` or ``"RK45"``.
            rtol: Relative solver tolerance.
            atol: Absolute solver tolerance.
            max_step: Maximum internal step (s).

        Returns:
            A :class:`BoxModelResult` with the sampled trajectory.
        """
        from scipy.integrate import solve_ivp

        if t_end <= 0:
            raise ValueError(f"t_end must be positive, got {t_end}")

        y0 = self._y0()
        p = self._param_vector()

        if t_eval is None:
            n_out = max(int(round(t_end / dt_out)) + 1, 2) if dt_out else 101
            t_eval = np.linspace(0.0, t_end, n_out)

        sol = solve_ivp(
            fun=lambda t, y: self._rhs_callable(t, y, p),
            t_span=(0.0, float(t_end)),
            y0=y0,
            method=method,
            t_eval=t_eval,
            jac=lambda t, y: self._jac_callable(t, y, p) if method in ("Radau", "BDF") else None,
            rtol=rtol,
            atol=atol,
            max_step=max_step,
        )
        if not sol.success:
            raise RuntimeError(f"Box model integration failed: {sol.message}")

        return BoxModelResult(
            t=np.asarray(sol.t),
            y=np.asarray(sol.y),
            species=list(self.species),
            method=method,
            scipy_message=str(sol.message),
        )


# ----------------------------------------------------------------------
# Command-line entry point: mkpp-box
# ----------------------------------------------------------------------
def _parse_env_overrides(pairs: list[str]) -> dict[str, float]:
    out: dict[str, float] = {}
    for item in pairs:
        if "=" not in item:
            raise SystemExit(f"FATAL ERROR: bad override '{item}', expected NAME=VALUE")
        name, value = item.split("=", 1)
        out[name.strip()] = float(value)
    return out


def main(argv: list[str] | None = None) -> int:
    """CLI wrapper that runs a mechanism as a Python box model."""
    ap = argparse.ArgumentParser(prog="mkpp-box", description="Run an MKPP mechanism as a 0-D box model (SciPy).")
    ap.add_argument("mechanism", help="Path to OpenAtmos YAML/JSON mechanism")
    ap.add_argument("--t-end", type=float, required=True, help="Simulation length in seconds")
    ap.add_argument("--dt-out", type=float, default=None, help="Output interval in seconds")
    ap.add_argument("--temp", type=float, default=298.15, help="Temperature (K)")
    ap.add_argument("--rh", type=float, default=0.5, help="Relative humidity (0-1)")
    ap.add_argument("--air-density", type=float, default=2.46e19, help="Air number density (molec cm-3)")
    ap.add_argument("--conc", action="append", default=[], metavar="SPECIES=VALUE", help="Initial concentration")
    ap.add_argument("--jval", action="append", default=[], metavar="SPECIES_OR_INDEX=VALUE", help="Photolysis rate (s-1)")
    ap.add_argument("--method", default="Radau", help="solve_ivp method (Radau, BDF, LSODA, RK45)")
    ap.add_argument("--out", default=None, help="Optional CSV output path")
    args = ap.parse_args(argv)

    box = BoxModel(
        args.mechanism,
        temperature=args.temp,
        relative_humidity=args.rh,
        air_density=args.air_density,
    )
    box.set_initial_concentrations(_parse_env_overrides(args.conc))
    for item in args.jval:
        name, value = item.split("=", 1)
        key: int | str = int(name) if name.isdigit() else name
        box.set_photolysis({key: float(value)})

    result = box.simulate(args.t_end, dt_out=args.dt_out, method=args.method)

    header = "time_s," + ",".join(result.species)
    print(header)
    for k in range(len(result.t)):
        row = ",".join(f"{v:.6e}" for v in result.y[:, k])
        print(f"{result.t[k]:.3f},{row}")

    if args.out:
        path = Path(args.out)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as fh:
            fh.write(header + "\n")
            for k in range(len(result.t)):
                row = ",".join(f"{v:.6e}" for v in result.y[:, k])
                fh.write(f"{result.t[k]:.3f},{row}\n")
        print(f"[mkpp-box] wrote {path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
