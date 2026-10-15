"""Static checks for truthful Kokkos device-callability claims."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ISORROPIA = ROOT / "src" / "isorropialite"
EXAERO = ROOT / "src" / "exaero"


def _source_files(root: Path) -> list[Path]:
    return [*root.rglob("*.cpp"), *root.rglob("*.hpp"), *root.rglob("*.h")]


def _annotated_bodies(source: str) -> list[str]:
    bodies = []
    for match in re.finditer(r"KOKKOS_INLINE_FUNCTION\b", source):
        opening = source.find("{", match.end())
        if opening == -1:
            continue
        depth = 1
        cursor = opening + 1
        while depth and cursor < len(source):
            depth += (source[cursor] == "{") - (source[cursor] == "}")
            cursor += 1
        if depth == 0:
            bodies.append(source[opening + 1 : cursor - 1])
    return bodies


def test_no_fake_kokkos_inline_definition() -> None:
    definitions = []
    for path in _source_files(ISORROPIA) + _source_files(EXAERO):
        source = path.read_text()
        if re.search(r"^\s*#\s*define\s+KOKKOS_INLINE_FUNCTION\s+inline\b", source, re.MULTILINE):
            definitions.append(str(path.relative_to(ROOT)))

    assert definitions == []


def test_device_annotated_bodies_use_portable_math() -> None:
    forbidden = re.compile(r"\bstd::(?:log|exp|max|min|abs|pow|sqrt|fmax|fmin|cbrt)\s*\(")
    violations = []
    for path in _source_files(ISORROPIA) + _source_files(EXAERO):
        for body in _annotated_bodies(path.read_text()):
            if forbidden.search(body):
                violations.append(str(path.relative_to(ROOT)))

    assert violations == []


def test_auxiliary_call_chain_has_no_undefined_device_symbols() -> None:
    declarations = []
    for path in _source_files(EXAERO):
        source = path.read_text()
        if re.search(r"extern\s+\"C\"[^;]*\b\w+_device\s*\(", source, re.DOTALL):
            declarations.append(str(path.relative_to(ROOT)))

    assert declarations == []


def test_auxiliary_engines_are_not_computed_in_exaero() -> None:
    # Photolysis rates are an MKPP *input*, not computed by the aerosol module,
    # and the ISORROPIA coupling is host-confined. Ex-Aero must not advertise or
    # stub out auxiliary-engine compute entry points.
    offenders = []
    for path in _source_files(EXAERO):
        source = path.read_text()
        if re.search(r"\bAuxiliaryEngines\b|compute_photolysis|EXAERO_WITH_CLOUDJ|EXAERO_WITH_ISORROPIALITE", source):
            offenders.append(str(path.relative_to(ROOT)))

    assert offenders == []