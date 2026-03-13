---
name: cobrapy
description: Constraints-Based Reconstruction and Analysis for Python. Used for modeling large-scale metabolic networks in microorganisms.
version: 0.29
license: LGPL-2.1
---

# COBRApy - Metabolic Modeling

Models the "metabolism" of a cell as a linear optimization problem. Used to predict bacterial growth under different conditions or design GMO strains.

## When to Use

- Predicting microbial growth rates under different nutrient conditions.
- Designing metabolic engineering strategies (knockouts, additions).
- Understanding metabolic flux distributions.
- Comparing metabolic capabilities across organisms.
- Identifying essential genes and reactions.

## Core Principles

### Flux Balance Analysis (FBA)

Optimizes metabolic fluxes to maximize biomass production (or other objectives) subject to stoichiometric constraints.

### Gene-Protein-Reaction (GPR)

Genes encode proteins (enzymes) that catalyze reactions. Knockouts affect reaction availability.

### Constraints

Reaction bounds (lower/upper limits) represent enzyme capacity or nutrient availability.

## Quick Reference

### Standard Imports

```python
import cobra
from cobra.io import load_model, save_model
```

### Basic Patterns

```python
# 1. Load model (e.g., E. coli)
model = cobra.io.load_model("iJO1366")
# Or: model = cobra.io.read_sbml_model("model.xml")

# 2. Run Flux Balance Analysis (FBA)
solution = model.optimize()
print(f"Growth rate: {solution.objective_value:.4f}")
print(f"Status: {solution.status}")

# 3. Knockout simulation (Gene essentiality)
with model:
    model.genes.get_by_id("b0002").knock_out()
    print(f"Growth after knockout: {model.optimize().objective_value:.4f}")

# 4. Change medium (nutrient availability)
model.medium = {
    'EX_glc__D_e': 10.0,  # Glucose uptake
    'EX_o2_e': 1000.0     # Oxygen
}
solution = model.optimize()
```

## Critical Rules

### ✅ DO

- **Check solution status** - Ensure status is 'optimal' before using results.
- **Use context managers** - Wrap modifications in `with model:` to avoid permanent changes.
- **Set appropriate bounds** - Reaction bounds should reflect biological reality.
- **Validate model** - Use `model.validate()` to check for common issues.

### ❌ DON'T

- **Don't ignore infeasible solutions** - If optimization fails, check constraints and bounds.
- **Don't modify model in place** - Use context managers or copy the model first.
- **Don't assume all reactions are active** - Many reactions have zero flux in optimal solution.

## Advanced Patterns

### Flux Variability Analysis (FVA)

```python
from cobra.flux_analysis import flux_variability_analysis

# Find range of possible fluxes for each reaction
fva_result = flux_variability_analysis(model, model.reactions)
```

### Gene Essentiality Analysis

```python
# Test which genes are essential for growth
from cobra.flux_analysis import single_gene_deletion

deletion_results = single_gene_deletion(model)
essential_genes = deletion_results[deletion_results['growth'] < 0.01]
```

### Adding Custom Reactions

```python
# Add a new reaction to the model
new_reaction = cobra.Reaction("NEW_RXN")
new_reaction.add_metabolites({
    model.metabolites.get_by_id("glc__D_c"): -1,
    model.metabolites.get_by_id("atp_c"): -1,
    model.metabolites.get_by_id("adp_c"): 1,
})
new_reaction.lower_bound = 0
new_reaction.upper_bound = 1000
model.add_reactions([new_reaction])
```

COBRApy transforms metabolic networks into computable models, enabling researchers to predict and engineer cellular behavior at the systems level.
