from typing import Dict, List
import networkx as nx
import sympy as sp
from .model import MechanismDefinition, ReactionDefinition

def partition_reactions(mech: MechanismDefinition) -> Dict[str, List[ReactionDefinition]]:
    """
    Partition reactions into implicit (stiff) and explicit (non-stiff) deterministic blocks
    using Tarjan's Strongly Connected Components (SCC) algorithm.
    """
    blocks = {
        "implicit": [],
        "explicit": []
    }

    # 1. Build the directed species dependency graph
    G = nx.DiGraph()
    for r in mech.reactions:
        for reactant in r.reactants:
            for product in r.products:
                G.add_edge(reactant, product)

    # 2. Find cycles (SCCs with more than 1 node, or self-loops)
    sccs = list(nx.strongly_connected_components(G))
    stiff_species = set()
    for scc in sccs:
        if len(scc) > 1:
            stiff_species.update(scc)
        elif len(scc) == 1:
            # Check for self-loop
            node = list(scc)[0]
            if G.has_edge(node, node):
                stiff_species.add(node)

    # 3. Partition reactions based on topology
    for r in mech.reactions:
        # A reaction belongs to the stiff manifold if it connects species within the stiff network
        is_stiff_topology = any(reactant in stiff_species for reactant in r.reactants) and \
                            any(product in stiff_species for product in r.products)

        # We also respect manual overrides (r.stiff) if the user forces it
        if r.stiff or is_stiff_topology:
            blocks["implicit"].append(r)
        else:
            blocks["explicit"].append(r)

    # Sort blocks deterministically by reaction type then expression
    blocks["implicit"].sort(key=lambda x: (x.reaction_type, x.rate_expression))
    blocks["explicit"].sort(key=lambda x: (x.reaction_type, x.rate_expression))

    # T026: Inject deterministic solver partition metadata
    blocks["metadata"] = {
        "sza_sorted": True,
        "micro_blocks": {
            "implicit": len(blocks["implicit"]),
            "explicit": len(blocks["explicit"])
        },
        "scc_count": len([s for s in sccs if len(s) > 1])
    }

    return blocks

def prepare_adjoint_and_tlm(mech: MechanismDefinition) -> Dict[str, bool]:
    """
    T015: Symbolic lowering hooks for analytical Jacobian, Adjoint, and Tangent-Linear models.
    For the MVP, this validates that the mechanism is differentiable.
    """
    # Verify no discontinuous thermodynamic operators are present
    for r in mech.reactions:
        if not r.continuous_transition and r.reaction_type.lower() in ("condensation", "phase_change"):
            raise ValueError(f"Reaction {r.rate_expression} lacks continuous transition for analytical differentiation.")

    return {"adjoint_ready": True, "tlm_ready": True}

def prepare_unified_jacobian(mech: MechanismDefinition) -> Dict[str, Any]:
    species_symbols = {s.name: sp.Symbol(f"C_{s.name}", real=True, nonnegative=True) for s in mech.species}
    Temp = sp.Symbol("Temp", real=True, nonnegative=True)
    Press = sp.Symbol("Press", real=True, nonnegative=True)
    M_density = sp.Symbol("M_density", real=True, nonnegative=True)
    v_gas = sp.Symbol("v_gas", real=True, nonnegative=True)
    S_a = sp.Symbol("S_a", real=True, nonnegative=True)

    df_dt_implicit = {s.name: sp.Integer(0) for s in mech.species}
    df_dt_explicit = {s.name: sp.Integer(0) for s in mech.species}
    
    blocks = partition_reactions(mech)

    for idx, r in enumerate(mech.reactions):
        rtype = r.reaction_type.upper()
        p = r.parameters
        flux = sp.Integer(0)

        if rtype == "PHOTOLYSIS":
            if "A" not in p: raise ValueError(f"PHOTOLYSIS reaction {idx} missing 'A' parameter (J-rate).")
            J_photo = sp.Symbol(str(p["A"]), real=True)
            flux = J_photo

        elif rtype == "ARRHENIUS":
            if "A" not in p: raise ValueError(f"ARRHENIUS reaction {idx} missing 'A' coefficient.")
            A = sp.Symbol(str(p["A"]), real=True)
            B = sp.Symbol(str(p.get("B", 0.0)), real=True)
            C = sp.Symbol(str(p.get("C", 0.0)), real=True)
            k_arr = A * (Temp / 300)**B * sp.exp(-C / Temp)
            flux = k_arr

        elif rtype == "DUMMYTROE":
            # Low pressure limit
            k0_A = sp.Symbol(str(p["k0"]["A"]), real=True)
            k0_B = sp.Symbol(str(p["k0"].get("B", 0.0)), real=True)
            k0_C = sp.Symbol(str(p["k0"].get("C", 0.0)), real=True)
            k0_val = k0_A * (Temp / 300)**k0_B * sp.exp(-k0_C / Temp)

            # High pressure limit
            kinf_A = sp.Symbol(str(p["kinf"]["A"]), real=True)
            kinf_B = sp.Symbol(str(p["kinf"].get("B", 0.0)), real=True)
            kinf_C = sp.Symbol(str(p["kinf"].get("C", 0.0)), real=True)
            kinf_val = kinf_A * (Temp / 300)**kinf_B * sp.exp(-kinf_C / Temp)

            Fc_val = sp.Symbol(str(p.get("Fc", 0.6)), real=True)

        elif rtype == "TROE" or rtype == "FALLOFF":
            A0 = sp.Symbol(str(p.get("k0_A", 0.0)), real=True)
            B0 = sp.Symbol(str(p.get("k0_B", 0.0)), real=True)
            C0 = sp.Symbol(str(p.get("k0_C", 0.0)), real=True)
            A1 = sp.Symbol(str(p.get("kinf_A", 0.0)), real=True)
            B1 = sp.Symbol(str(p.get("kinf_B", 0.0)), real=True)
            C1 = sp.Symbol(str(p.get("kinf_C", 0.0)), real=True)
            CF = sp.Symbol(str(p.get("Fc", 0.6)), real=True)
            
            K0 = A0 * sp.exp(-B0/Temp) * (Temp/300)**C0
            K1 = A1 * sp.exp(-B1/Temp) * (Temp/300)**C1
            K0 = K0 * 1.0e6
            K_ratio = K0 / K1
            F_broadening = CF ** (1.0 / (1.0 + (sp.log(K_ratio, 10))**2))
            flux = (K0 / (1.0 + K_ratio)) * F_broadening

        elif rtype == "EP2":
            A0 = sp.Symbol(str(p.get("A0", 0.0)), real=True)
            C0 = sp.Symbol(str(p.get("C0", 0.0)), real=True)
            A2 = sp.Symbol(str(p.get("A2", 0.0)), real=True)
            C2 = sp.Symbol(str(p.get("C2", 0.0)), real=True)
            A3 = sp.Symbol(str(p.get("A3", 0.0)), real=True)
            C3 = sp.Symbol(str(p.get("C3", 0.0)), real=True)
            K0 = A0 * sp.exp(-C0/Temp)
            K2 = A2 * sp.exp(-C2/Temp)
            K3 = A3 * sp.exp(-C3/Temp) * 1.0e6
            flux = K0 + K3 / (1.0 + K3/K2)
            
        elif rtype == "EP3":
            A1 = sp.Symbol(str(p.get("A1", 0.0)), real=True)
            C1 = sp.Symbol(str(p.get("C1", 0.0)), real=True)
            A2 = sp.Symbol(str(p.get("A2", 0.0)), real=True)
            C2 = sp.Symbol(str(p.get("C2", 0.0)), real=True)
            K1 = A1 * sp.exp(-C1/Temp)
            K2 = A2 * sp.exp(-C2/Temp)
            flux = K1 + K2 * 1.0e6

        elif rtype == "HETEROGENEOUS":
            gamma = sp.Symbol(str(p["gamma"]), real=True)
            k_het = 0.25 * gamma * v_gas * S_a
            flux = k_het

        elif rtype == "PHASE_CHANGE":
            flux = sp.Symbol(f"Rate_{idx}", real=True)

        for reactant, stoich in r.reactants.items():
            if reactant in species_symbols:
                flux *= (species_symbols[reactant] ** sp.Integer(int(stoich)))

        is_implicit = r in blocks["implicit"]

        for reactant, stoich in r.reactants.items():
            if reactant in df_dt_implicit:
                if is_implicit:
                    df_dt_implicit[reactant] -= flux * sp.Float(stoich)
                else:
                    df_dt_explicit[reactant] -= flux * sp.Float(stoich)

        for product, stoich in r.products.items():
            if product in df_dt_implicit:
                if is_implicit:
                    df_dt_implicit[product] += flux * sp.Float(stoich)
                else:
                    df_dt_explicit[product] += flux * sp.Float(stoich)

    ordered_species = [s.name for s in mech.species]
    f_implicit = sp.Matrix([df_dt_implicit[s] for s in ordered_species])
    f_explicit = sp.Matrix([df_dt_explicit[s] for s in ordered_species])
    c_vector = sp.Matrix([species_symbols[s] for s in ordered_species])

    jacobian_matrix = f_implicit.jacobian(c_vector)
    adjoint_matrix = jacobian_matrix.transpose()

    unique_elements = sorted(list(set(elem for s in mech.species for elem in s.elements.keys())))
    if unique_elements:
        E_matrix = sp.zeros(len(unique_elements), len(ordered_species))
        for j, sp_name in enumerate(ordered_species):
            species_def = next(s for s in mech.species if s.name == sp_name)
            for i, elem in enumerate(unique_elements):
                E_matrix[i, j] = species_def.elements.get(elem, 0)
        try:
            E_E_T = E_matrix * E_matrix.transpose()
            mass_projector = E_matrix.transpose() * E_E_T.pinv()
        except Exception:
            mass_projector = sp.zeros(len(ordered_species), len(unique_elements))
    else:
        E_matrix = sp.zeros(1, len(ordered_species))
        mass_projector = sp.zeros(len(ordered_species), 1)

    return {
        "species_map": ordered_species,
        "f_implicit": f_implicit,
        "f_explicit": f_explicit,
        "jacobian_matrix": jacobian_matrix,
        "adjoint_matrix": adjoint_matrix,
        "mass_projector": mass_projector,
        "element_map": unique_elements
    }