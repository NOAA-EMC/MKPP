"""Structural tests for the device-callable generated solver path.

These assert the *structural* guarantees that make the generated solver path
callable from a device execution space:

  * every ``detail::`` helper invoked from a ``KOKKOS_INLINE_FUNCTION`` method
    has an inline **definition** visible at the point of kernel instantiation
    -- a declaration-only boundary compiled by a host-only unit is not
    enough for a device compiler;
  * the runtime photolysis input ``jvals`` is bound as a memory-space
    ``Kokkos::View`` rather than a raw host pointer.

Host and device must share one source of truth: the same inline definitions
live in a generated implementation header that both the public header and the
compiled translation units include.

**Validates: Requirements 2.1, 2.2, 3.1.**
"""

import re
from pathlib import Path

import pytest
from mkpp.codegen import generate_headers
from mkpp.parser import load_mechanism

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CHAPMAN = PROJECT_ROOT / "mechanisms/openatmos/chapman/mechanism.json"


@pytest.fixture(scope="module")
def chapman_artifacts(tmp_path_factory):
    if not CHAPMAN.exists():
        pytest.skip(f"chapman mechanism file not found at {CHAPMAN}")
    mech = load_mechanism(str(CHAPMAN))
    out_dir = tmp_path_factory.mktemp("chapman_gen")
    results = generate_headers(mech, out_dir=str(out_dir), solver_name="ros3", emit_reference_backend=True)
    header = Path(results["header"]).read_text()
    impl_dir = Path(results["header"]).parent / "chapman"
    fragments = {p.name: p.read_text() for p in sorted(impl_dir.glob("*.hpp"))}
    return {"header": header, "fragments": fragments, "results": results, "out_dir": out_dir}


# ---------------------------------------------------------------------------
# Inline device-callable helper definitions
# ---------------------------------------------------------------------------


def test_detail_helpers_have_inline_definitions(chapman_artifacts):
    """The detail:: helpers must be emitted as KOKKOS_INLINE_FUNCTION definitions."""
    fragments = chapman_artifacts["fragments"]
    assert fragments, "expected generated device-callable implementation fragments with inline detail:: definitions"
    all_impl = "\n".join(fragments.values())

    for symbol in ("compute_rates_chunk_0", "compute_jacobian_chunk_0", "factorize_plan", "solve_plan"):
        pattern = rf"KOKKOS_INLINE_FUNCTION\s+void\s+{symbol}\b"
        assert re.search(pattern, all_impl), f"detail::{symbol} is not emitted as a KOKKOS_INLINE_FUNCTION definition"


def test_header_no_longer_declares_only_helpers(chapman_artifacts):
    """The public header must not keep a declaration-only detail:: boundary."""
    header = chapman_artifacts["header"]
    # A bare 'void compute_rates_chunk_0(' declaration (no KOKKOS_INLINE_FUNCTION,
    # no body) is exactly the host-only boundary that breaks device callability.
    bare_decl = re.search(r"(?<!KOKKOS_INLINE_FUNCTION\s)void\s+compute_rates_chunk_\d+\s*\(", header)
    assert bare_decl is None, "public header still carries a declaration-only detail:: helper"


def test_single_source_of_truth_via_include(chapman_artifacts):
    """The public header includes the fragments; the .cpp TUs include them too."""
    header = chapman_artifacts["header"]
    for fragment in ("rates", "jacobian", "supernodal_factorize", "supernodal_solve", "factorize", "solve"):
        assert re.search(
            rf'#include\s+"[^"]*{fragment}\.hpp"', header
        ), f"header.j2 must include the {fragment} implementation fragment"

    results = chapman_artifacts["results"]
    compiled = {Path(p).name: Path(p).read_text() for p in results["compiled_sources"]}
    assert compiled, "expected compiled sources to still be emitted"
    for name, text in compiled.items():
        stem = name.removesuffix(".cpp")
        assert re.search(rf'#include\s+"{stem}\.hpp"', text), f"{name} must include the shared fragment, not redefine the algebra"


def test_inline_definitions_are_namespace_scoped(chapman_artifacts):
    """Each fragment is self-contained: it opens the mechanism detail namespace."""
    all_impl = "\n".join(chapman_artifacts["fragments"].values())
    assert (
        "namespace mkpp::generated::chapman::detail" in all_impl
    ), "fragments must define helpers inside the mechanism detail namespace"
    assert "#include <Kokkos_Core.hpp>" in all_impl, "fragments must include Kokkos for KOKKOS_INLINE_FUNCTION"


# ---------------------------------------------------------------------------
# Memory-space jvals binding
# ---------------------------------------------------------------------------


def test_kernel_entrypoints_take_view_jvals(chapman_artifacts):
    """integrate/compute_rates/compute_jacobian must bind jvals as a Kokkos::View."""
    header = chapman_artifacts["header"]
    view_jval = re.compile(r"Kokkos::View<const double\s*\*,\s*memory_space>\s+jvals")
    assert view_jval.search(header), "generated entry points must take jvals as a memory-space Kokkos::View"


def test_no_raw_pointer_jvals_in_entry_points(chapman_artifacts):
    """The device-reachable entry points must not take a raw host double* jvals."""
    header = chapman_artifacts["header"]
    # Look only at the KOKKOS_INLINE_FUNCTION method signatures, not the detail
    # chunk definitions (which legitimately take a device-accessible raw pointer).
    raw = re.search(
        r"KOKKOS_INLINE_FUNCTION\s+void\s+(?:integrate|compute_rates|compute_jacobian)\b[^;{]*const double\s*\*\s*jvals", header
    )
    assert raw is None, "entry point still accepts a raw host pointer for jvals"
