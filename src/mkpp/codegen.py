"""MKPP Code Generation Orchestrator.

This module provides the top-level `generate_headers` function that emits
Kokkos C++ solver headers from a parsed mechanism definition. It delegates
to the Jinja2 template engine for C++ emission and to focused submodules
for tableau definitions and expression formatting.

Public API (backward-compatible):
    - generate_headers
    - generate_host_api_headers
    - SOLVER_COEFFICIENTS
    - RosenbrockTableau
    - format_eqn
    - get_A, get_C
"""

import hashlib
import json
from pathlib import Path

from .format_eqn import format_eqn
from .model import MechanismDefinition
from .rosenbrock import SOLVER_COEFFICIENTS, RosenbrockTableau, get_A, get_C
from .template_context import build_template_context
from .template_engine import TemplateEngine

# Re-export public API for backward compatibility
__all__ = [
    "generate_headers",
    "generate_host_api_headers",
    "SOLVER_COEFFICIENTS",
    "RosenbrockTableau",
    "format_eqn",
    "get_A",
    "get_C",
]


def generate_host_api_headers(
    mech: MechanismDefinition,
    out_dir: str = "src/solvers",
    solver_name: str = "ros3",
) -> dict[str, str]:
    """Emit the C, C++, and Fortran host API headers and wrappers for a mechanism."""
    if not mech or not mech.species:
        raise ValueError("Cannot generate host API headers for empty mechanism")

    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    context = build_template_context(mech, solver_name=solver_name)
    engine = TemplateEngine()

    rendered = {
        "c_header": ("mkpp.h", engine.render("host_api/mkpp.h.j2", context)),
        "fortran_module": ("mkpp_mod.f90", engine.render("host_api/mkpp_mod.f90.j2", context)),
        "cpp_header": ("mkpp.hpp", engine.render("host_api/mkpp.hpp.j2", context)),
        "c_api_source": ("mkpp_c_api.cpp", engine.render("host_api/mkpp_c_api.cpp.j2", context)),
    }

    results = {}
    for key, (filename, content) in rendered.items():
        file_path = out_path / filename
        with open(file_path, "w") as f:
            f.write(content)
        results[key] = str(file_path)

    return results


def generate_headers(
    mech: MechanismDefinition,
    out_dir: str = "src/solvers",
    suffix: str = "",
    solver_name: str = "ros3",
    adjoint: bool = False,
    generate_host_api: bool = False,
    simd_backend: str = "native",
    emit_reference_backend: bool = False,
) -> dict[str, str]:
    """Emit the Kokkos headers and manifest artifact."""
    if not mech or not mech.species:
        raise ValueError("Cannot generate headers for empty mechanism")

    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    # Sensitivity code is always emitted into the generated header, guarded by
    # MKPP_ENABLE_ADJOINT.  That keeps a mechanism's chemistry artifact stable
    # while allowing CMake to preprocess adjoint/TLM code away in forward-only
    # builds.  ``adjoint`` remains accepted for CLI/API compatibility.
    context = build_template_context(mech, solver_name, adjoint=True, simd_backend=simd_backend)
    # Add suffix to context for filename generation
    context["suffix"] = suffix
    # The public header includes the reference factorization fragment only when
    # the unrolled-reference backend is emitted, keeping the default artifact
    # set free of the benchmark-only algebra.
    context["emit_reference_backend"] = emit_reference_backend

    # 2. Render the header via Jinja2 template engine
    engine = TemplateEngine()
    header_text = engine.render("header.j2", context)

    # 3. Write rendered output to the same file path as before
    header_path = out_path / f"{mech.name}{suffix}.hpp"
    with open(header_path, "w") as f:
        f.write(header_text)

    compiled_sources = []
    # Keep the public include at the output root while grouping its compiled
    # implementation units under a mechanism-specific directory.
    compiled_path = out_path / f"{mech.name}{suffix}"
    compiled_path.mkdir(parents=True, exist_ok=True)
    # The algebra for every detail:: helper is emitted ONCE as a
    # KOKKOS_INLINE_FUNCTION definition fragment under the mechanism directory.
    # The public header includes the fragments (so a device instantiation sees
    # inline bodies for the whole call chain) and each compiled translation unit
    # includes only its own fragment (so per-TU compile cost stays bounded and
    # the static-library pathway keeps working). Host and device therefore
    # share a single source of truth with no forked chemistry algebra.
    for kernel in ("rates", "jacobian"):
        fragment_path = compiled_path / f"{kernel}.hpp"
        with open(fragment_path, "w") as f:
            f.write(engine.render(f"device_impl/{kernel}.hpp.j2", context))
        source_path = compiled_path / f"{kernel}.cpp"
        with open(source_path, "w") as f:
            f.write(engine.render(f"compiled_{kernel}.cpp.j2", context))
        for stale_path in compiled_path.glob(f"{kernel}_*.cpp"):
            stale_path.unlink()
        compiled_sources.append(str(source_path))

    if emit_reference_backend:
        fragment_path = compiled_path / "factorize.hpp"
        with open(fragment_path, "w") as f:
            f.write(engine.render("device_impl/factorize.hpp.j2", context))
        source_path = compiled_path / "factorize.cpp"
        with open(source_path, "w") as f:
            f.write(engine.render("compiled_factorize.cpp.j2", context))
        compiled_sources.append(str(source_path))
    else:
        for source_path in compiled_path.glob("factorize*.*"):
            source_path.unlink()

    fragment_path = compiled_path / "solve.hpp"
    with open(fragment_path, "w") as f:
        f.write(engine.render("device_impl/solve.hpp.j2", context))
    source_path = compiled_path / "solve.cpp"
    with open(source_path, "w") as f:
        f.write(engine.render("compiled_solve.cpp.j2", context))
    compiled_sources.append(str(source_path))

    for kernel in ("supernodal_factorize", "supernodal_solve"):
        fragment_path = compiled_path / f"{kernel}.hpp"
        with open(fragment_path, "w") as f:
            f.write(engine.render(f"device_impl/{kernel}.hpp.j2", context))
        source_path = compiled_path / f"{kernel}.cpp"
        with open(source_path, "w") as f:
            f.write(engine.render(f"{kernel}.cpp.j2", context))
        compiled_sources.append(str(source_path))

    results = {"header": str(header_path), "compiled_sources": compiled_sources}

    if generate_host_api:
        api_results = generate_host_api_headers(mech, out_dir=out_dir, solver_name=solver_name)
        results.update(api_results)

    # 4. Manifest metadata emission (unchanged logic)
    manifest = {
        "mechanism": mech.name,
        "aerosol_representation": mech.aerosol_representation.value,
        "simd_backend": simd_backend,
        "checksum": hashlib.sha256(mech.name.encode()).hexdigest(),
        "artifacts": [
            {"kind": "header", "file": header_path.name},
            *({"kind": "compiled_kernel_source", "file": str(Path(source).relative_to(out_path))} for source in compiled_sources),
            {"kind": "adjoint_tlm_record", "differentiable": True},
        ],
    }

    if getattr(mech, "host_interface", None) and mech.host_interface.arrays:
        manifest["host_interface"] = {
            arr.name: {
                "rank": arr.rank,
                "layout": arr.layout,
                "lifetime": "unmanaged_borrowed_from_host" if arr.ownership == "host" else "device_owned",
            }
            for arr in mech.host_interface.arrays
        }

    partition_meta = getattr(mech, "partition_metadata", None)
    if partition_meta:
        manifest["solver_partition"] = partition_meta

    manifest_path = out_path / f"{mech.name}_manifest.json"
    plan_json_path = compiled_path / "factorization_plan.json"
    plan_markdown_path = compiled_path / "factorization_plan.md"
    plan_json_path.write_text(engine.render("factorization_plan.json.j2", context), encoding="utf-8")
    plan_markdown_path.write_text(engine.render("factorization_plan.md.j2", context), encoding="utf-8")
    manifest["factorization_plan"] = {
        "json": str(plan_json_path.relative_to(out_path)),
        "markdown": str(plan_markdown_path.relative_to(out_path)),
    }
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    results["manifest"] = str(manifest_path)
    results["factorization_plan"] = str(plan_json_path)
    results["factorization_plan_markdown"] = str(plan_markdown_path)
    return results
