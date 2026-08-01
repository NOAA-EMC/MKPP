import json
import hashlib
from pathlib import Path
from typing import Dict
from .model import MechanismDefinition

def generate_headers(mech: MechanismDefinition, out_dir: str = "build/mkpp-generated") -> Dict[str, str]:
    """Emit the Kokkos headers and manifest artifact."""
    if not mech or not mech.species:
        raise ValueError("Cannot generate headers for empty mechanism")
        
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    
    # 1. Deterministic header emission
    header_path = out_path / f"{mech.name}.hpp"
    with open(header_path, 'w') as f:
        f.write("#pragma once\n")
        f.write("#include <Kokkos_Core.hpp>\n")
        f.write("#include <KokkosBatched_LU_Decl.hpp>\n")
        f.write("#include <KokkosBatched_Trsv_Decl.hpp>\n\n")
        f.write(f"// Generated solver for {mech.name}\n")
        f.write("namespace mkpp {\n")
        f.write("  // Pure Kokkos abstractions (no raw pragmas allowed)\n")
        f.write("  template<typename DeviceType>\n")
        f.write("  struct SolverKernels {\n")
        f.write("      KOKKOS_INLINE_FUNCTION void integrate_forward() const {}\n")
        f.write("      KOKKOS_INLINE_FUNCTION void compute_adjoint() const {}\n")
        f.write("      KOKKOS_INLINE_FUNCTION void compute_tlm() const {}\n")
        f.write("  };\n")
        f.write("}\n")
        
    # 2. Manifest metadata emission (T008)
    manifest = {
        "mechanism": mech.name,
        "aerosol_representation": mech.aerosol_representation.value,
        "checksum": hashlib.sha256(mech.name.encode()).hexdigest(), # Simplified checksum for MVP
        "artifacts": [
            {"kind": "header", "file": header_path.name},
            {"kind": "adjoint_tlm_record", "differentiable": True}
        ]
    }
    
    manifest_path = out_path / "manifest.json"
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
        
    return {"header": str(header_path), "manifest": str(manifest_path)}
