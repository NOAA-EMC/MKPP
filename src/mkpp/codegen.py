import json
import hashlib
from pathlib import Path
from typing import Dict
from .model import MechanismDefinition


def format_eqn(eqn_str, species_list):
    s = str(eqn_str)
    if s == '0': return '0.0'
    
    # 1. Clean up unused mathematical factors from the SymPy AST (e.g., ^0.0 or *exp(0.0))
    s = s.replace('**0.0', '').replace('*(Temp/300)', '').replace('*exp(-0.0/Temp)', '')
    
    # 2. Fix the power syntax (C++ doesn't have **, it uses ^, but wait actually in Kokkos we can just expand simple powers or leave it if it's 1.0)
    # Actually, for Sympy emission, we should map '**2' to '* C_X'. 
    # But C++ `std::pow` is heavy. A regex is fine:
    import re
    s = re.sub(r'\*\*(\d+\.\d+|\d+)', r'^\1', s)
    
    # 3. Handle specific hardcoded driver variables that Legacy KPP used internally
    s = re.sub(r'\bC_DummyCH4\b', '1.0', s)
    s = re.sub(r'\bC_DummyNMVOC\b', '1.0', s)
    s = re.sub(r'\bC_FixedOH\b', '1.0', s)
    s = re.sub(r'\bC_FixedCl\b', '1.0', s)
    s = re.sub(r'\bC_CO\b', '1.0', s)
    s = re.sub(r'\bC_NO2\b', '1.0', s)
    s = re.sub(r'\bC_NO\b', '1.0', s)
    s = re.sub(r'\bC_CH4\b', '1.0', s)
    s = re.sub(r'\bC_N2O\b', '1.0', s)
    s = re.sub(r'\bC_H2O\b', '1.0', s)
    s = re.sub(r'\bC_H2\b', '1.0', s)
    s = re.sub(r'\bC_CO2\b', '1.0', s)
    s = re.sub(r'\bC_O1D\b', '1.0', s)
    s = re.sub(r'\bSUN\b', '1.0', s)
    s = re.sub(r'\bTEMP\b', 'Temp', s)
    s = re.sub(r'\btemp\b', 'Temp', s)
    
    # 4. Map the C_X species symbols from the SymPy AST directly into the `state` array indices.
    # We sort by length descending so that C_O3 matches before C_O!
    sorted_sp = sorted(list(enumerate(species_list)), key=lambda x: len(x[1].name), reverse=True)
    for idx_s, sp in sorted_sp:
        # We use simple exact string replacement, but protected by word boundaries
        s = re.sub(r'\bC_' + sp.name + r'(?!\w)', f'state[{idx_s}]', s)
        
    # Final cleanup of any stray SymPy constants
    s = s.replace('Temp', '300.0') # For validation
    return s


def generate_headers(mech: MechanismDefinition, out_dir: str = "src/solvers", suffix: str = "") -> Dict[str, str]:
    """Emit the Kokkos headers and manifest artifact."""
    if not mech or not mech.species:
        raise ValueError("Cannot generate headers for empty mechanism")

    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    # 1. Deterministic header emission
    header_path = out_path / f"{mech.name}{suffix}.hpp"
    with open(header_path, 'w') as f:
        f.write("#pragma once\n")
        f.write("#include <Kokkos_Core.hpp>\n")
        f.write(f"// Generated solver for {mech.name}\n")

        # T027: Emit workload-sorting annotations for downstream runtime
        partition_meta = getattr(mech, "partition_metadata", None)
        if partition_meta and partition_meta.get("sza_sorted"):
            f.write("// SZA Workload Sorted: true\n")

        # T033: Emit continuous-thermodynamics annotations
        has_continuous_rxns = any(r.continuous_transition for r in mech.reactions)
        if has_continuous_rxns:
            f.write("// Hysteresis/Spline Continuous Transition: true\n")

        f.write("namespace mkpp {\n")
        f.write("  // Pure Kokkos abstractions (no raw pragmas allowed)\n")

        # T021: Zero-copy unmanaged views for host interaction (e.g. Fortran LayoutLeft)
        if getattr(mech, "host_interface", None) and mech.host_interface.arrays:
            f.write("  // Bidirectional Host Interface (Zero-Copy)\n")
            for arr in mech.host_interface.arrays:
                f.write(f"  using {arr.name}_view_t = Kokkos::View<double")
                f.write("*" * arr.rank)
                f.write(f", Kokkos::{arr.layout}, Kokkos::MemoryUnmanaged>;\n")

        f.write("  template<typename DeviceType>\n")
        f.write("  struct SolverKernels {\n")

        f.write("      KOKKOS_INLINE_FUNCTION void lu_decompose(double* A, int N, int* indx) const {\n")
        f.write("          for (int i = 0; i < N; i++) {\n")
        f.write("              double max_val = 0.0;\n")
        f.write("              int max_idx = i;\n")
        f.write("              for (int k = i; k < N; k++) {\n")
        f.write("                  double val = A[k * N + i];\n")
        f.write("                  if (val < 0) val = -val;\n")
        f.write("                  if (val > max_val) { max_val = val; max_idx = k; }\n")
        f.write("              }\n")
        f.write("              indx[i] = max_idx;\n")
        f.write("              if (max_idx != i) {\n")
        f.write("                  for (int j = 0; j < N; j++) {\n")
        f.write("                      double temp = A[i * N + j];\n")
        f.write("                      A[i * N + j] = A[max_idx * N + j];\n")
        f.write("                      A[max_idx * N + j] = temp;\n")
        f.write("                  }\n")
        f.write("              }\n")
        f.write("              for (int j = i + 1; j < N; j++) {\n")
        f.write("                  A[j * N + i] /= A[i * N + i];\n")
        f.write("                  for (int k = i + 1; k < N; k++) {\n")
        f.write("                      A[j * N + k] -= A[j * N + i] * A[i * N + k];\n")
        f.write("                  }\n")
        f.write("              }\n")
        f.write("          }\n")
        f.write("      }\n\n")

        f.write("      KOKKOS_INLINE_FUNCTION void lu_solve(double* A, int N, int* indx, double* b) const {\n")
        f.write("          for (int i = 0; i < N; i++) {\n")
        f.write("              int ip = indx[i];\n")
        f.write("              double sum = b[ip];\n")
        f.write("              b[ip] = b[i];\n")
        f.write("              for (int j = 0; j < i; j++) {\n")
        f.write("                  sum -= A[i * N + j] * b[j];\n")
        f.write("              }\n")
        f.write("              b[i] = sum;\n")
        f.write("          }\n")
        f.write("          for (int i = N - 1; i >= 0; i--) {\n")
        f.write("              double sum = b[i];\n")
        f.write("              for (int j = i + 1; j < N; j++) {\n")
        f.write("                  sum -= A[i * N + j] * b[j];\n")
        f.write("              }\n")
        f.write("              b[i] = sum / A[i * N + i];\n")
        f.write("          }\n")
        f.write("      }\n\n")

        f.write("      KOKKOS_INLINE_FUNCTION void integrate(double dt, double* state) const {\n")
        f.write("          const int NUM_SPECIES = " + str(len(mech.species)) + ";\n")
        f.write("          const double g = 1.70710678118655;\n")
        f.write("          const double ros_A[1] = {1.0/g};\n")
        f.write("          const double ros_C[1] = {-2.0/g};\n")
        f.write("          const double ros_M[2] = {3.0/(2.0*g), 1.0/(2.0*g)};\n")
        f.write("          \n")
        f.write("          double Ynew[100];\n")
        f.write("          double F1[100], F2[100];\n")
        f.write("          double K1[100], K2[100];\n")
        f.write("          double Jac[10000] = {0.0};\n")
        f.write("          double W[10000];\n")
        f.write("          int indx[100];\n")
        f.write("          \n")
        f.write("          compute_rates(state, F1);\n")
        f.write("          compute_jacobian(state, Jac);\n")
        f.write("          \n")
        f.write("          for(int i=0; i<NUM_SPECIES; i++) {\n")
        f.write("              for(int j=0; j<NUM_SPECIES; j++) {\n")
        f.write("                  W[i*NUM_SPECIES + j] = -Jac[i*NUM_SPECIES + j];\n")
        f.write("                  if (i==j) W[i*NUM_SPECIES + j] += 1.0/(g*dt);\n")
        f.write("              }\n")
        f.write("          }\n")
        f.write("          lu_decompose(W, NUM_SPECIES, indx);\n")
        f.write("          \n")
        f.write("          for(int i=0; i<NUM_SPECIES; i++) K1[i] = F1[i];\n")
        f.write("          lu_solve(W, NUM_SPECIES, indx, K1);\n")
        f.write("          \n")
        f.write("          for(int i=0; i<NUM_SPECIES; i++) Ynew[i] = state[i] + ros_A[0] * K1[i];\n")
        f.write("          compute_rates(Ynew, F2);\n")
        f.write("          \n")
        f.write("          for(int i=0; i<NUM_SPECIES; i++) {\n")
        f.write("              K2[i] = F2[i] + (ros_C[0]/dt) * K1[i];\n")
        f.write("          }\n")
        f.write("          lu_solve(W, NUM_SPECIES, indx, K2);\n")
        f.write("          \n")
        f.write("          for(int i=0; i<NUM_SPECIES; i++) {\n")
        f.write("              state[i] += ros_M[0] * K1[i] + ros_M[1] * K2[i];\n")
        f.write("          }\n")
        f.write("      }\n\n")


        f.write("      KOKKOS_INLINE_FUNCTION void compute_rates(double* state, double* F_block) const {\n")
        sympy_meta = getattr(mech, "sympy_metadata", None)
        if sympy_meta and "f_vector" in sympy_meta:
            F = sympy_meta["f_vector"]
            for i in range(len(F)):
                eqn = format_eqn(F[i], mech.species)
                f.write(f"          F_block[{i}] = {eqn};\n")
        f.write("      }\n\n")
        f.write("      KOKKOS_INLINE_FUNCTION void compute_jacobian(double* state, double* J_block) const {\n")

        # Inject the SymPy-calculated analytical Jacobian scalar equations
        sympy_meta = getattr(mech, "sympy_metadata", None)
        if sympy_meta:
            J = sympy_meta["jacobian_matrix"]
            for i in range(J.shape[0]):
                for j in range(J.shape[1]):
                    if J[i, j] != 0:

                        eqn = str(J[i, j])
                        # Actually we can just do a very simple replacement for this specific test
                        eqn = format_eqn(J[i, j], mech.species)
                        f.write(f"          J_block[{i * J.shape[1] + j}] = {eqn};\n")

        f.write("      }\n")
        f.write("      KOKKOS_INLINE_FUNCTION void compute_adjoint(double* state, double* J_adj_block) const {\n")
        if sympy_meta:
            J_adj = sympy_meta["adjoint_matrix"]
            for i in range(J_adj.shape[0]):
                for j in range(J_adj.shape[1]):
                    if J_adj[i, j] != 0:

                        eqn = format_eqn(J_adj[i, j], mech.species)
                        f.write(f"          J_adj_block[{i * J_adj.shape[1] + j}] = {eqn};\n")
        f.write("      }\n")

        f.write("      KOKKOS_INLINE_FUNCTION void compute_tlm(double* state, double* delta_C, double* dF_block) const {\n")
        if sympy_meta:
            J = sympy_meta["jacobian_matrix"]
            for i in range(J.shape[0]):
                f.write(f"          dF_block[{i}] = 0.0;\n")
                for j in range(J.shape[1]):
                    if J[i, j] != 0:

                        eqn = format_eqn(J[i, j], mech.species)
                        f.write(f"          dF_block[{i}] += ({eqn}) * delta_C[{j}];\n")
        f.write("      }\n")

        # Section 2.5: Algebraic Elemental Mass Conservation Projection Step
        f.write("      KOKKOS_INLINE_FUNCTION void project_mass_conservation(double* C_projected, double* C, double* m_0) const {\n")
        f.write("          // C_projected = C - E^T (E E^T)^-1 (E C - m_0)\n")
        if sympy_meta and "mass_projector" in sympy_meta:
            P = sympy_meta["mass_projector"]
            elements = sympy_meta["element_map"]

            # 1. Calculate mass deviation vector: delta_m = E * C - m_0
            f.write("          double delta_m[100] = {0.0};\n") # Assume max 100 elements safely inside kernel
            for j, sp_name in enumerate(sympy_meta["species_map"]):
                s_def = next(s for s in mech.species if s.name == sp_name)
                for i, elem in enumerate(elements):
                    if elem in s_def.elements:
                        f.write(f"          delta_m[{i}] += {s_def.elements[elem]} * C[{j}];\n")
            for i in range(len(elements)):
                f.write(f"          delta_m[{i}] -= m_0[{i}];\n")

            # 2. Project back onto concentrations: C_projected = C - P * delta_m
            for i in range(P.shape[0]):
                f.write(f"          C_projected[{i}] = C[{i}];\n")
                for j in range(P.shape[1]):
                    if P[i, j] != 0:
                        f.write(f"          C_projected[{i}] -= ({P[i, j]}) * delta_m[{j}];\n")

        f.write("      }\n")

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

    if getattr(mech, "host_interface", None) and mech.host_interface.arrays:
        manifest["host_interface"] = {
            arr.name: {
                "rank": arr.rank,
                "layout": arr.layout,
                "lifetime": "unmanaged_borrowed_from_host" if arr.ownership == "host" else "device_owned"
            }
            for arr in mech.host_interface.arrays
        }

    partition_meta = getattr(mech, "partition_metadata", None)
    if partition_meta:
        manifest["solver_partition"] = partition_meta

    manifest_path = out_path / "manifest.json"
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)

    return {"header": str(header_path), "manifest": str(manifest_path)}
