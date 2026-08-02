# Phase 1: Data Model & Interfaces

## 1. LumpingRule (Entity)
Represents a single surrogate mapping from the `lumping_rules.yaml`.

**Fields**:
- `surrogate_name` (String): The target lumped species (e.g., `ALK_SURR`).
- `explicit_species` (List[String]): The explicit species to collapse.
- `weights` (Dict[String, Float]): Reference concentration weights for the explicit species used for rate averaging.

**Validation Rules**:
- Explicit species must exist in the base mechanism.
- Weights must be positive floats.
- The surrogate species must be defined or automatically injectable into the species dictionary.

## 2. CollapsedReaction (Entity)
Represents the result of merging multiple explicit reactions.

**Fields**:
- `reactants` (Dict[String, Float]): Stoichiometry of reactants.
- `products` (Dict[String, Float]): Stoichiometry of products, including carbon-scaling factors.
- `effective_rate` (Expression): The SymPy AST expression representing the concentration-weighted $A_{eff}$.

**Validation Rules**:
- Algebraic carbon and mass conservation must be maintained across the reaction.
- Product multipliers must strictly account for the `C_explicit / C_surrogate` ratio.
