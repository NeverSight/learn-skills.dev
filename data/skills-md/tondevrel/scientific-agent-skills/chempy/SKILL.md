---
name: chempy
description: A Python package useful for chemistry (mainly physical/analytical/inorganic chemistry). Features include balancing chemical reactions, chemical kinetics (ODE integration), chemical equilibria, ionic strength calculations, and unit handling. Use when working with chemical equations, reaction balancing, kinetic modeling, equilibrium calculations, speciation, pH calculations, ionic strength, activity coefficients, or chemical formula parsing.
version: 0.8
license: BSD-3-Clause
---

# ChemPy - Physical and Analytical Chemistry

ChemPy provides a systematic way to handle chemical entities and reactions. It can automatically balance complex redox reactions, solve systems of ordinary differential equations (ODEs) for kinetics, and calculate species distribution in equilibria.

## When to Use

- Balancing chemical equations (including ionic and redox reactions).
- Simulating chemical kinetics (concentration vs. time) using ODE solvers.
- Calculating chemical equilibria and speciation (e.g., pH of a buffer).
- Handling physical constants and units in chemical calculations.
- Modeling ionic strength and activity coefficients (Debye-Hückel).
- Parsing chemical formulas and calculating molar masses.
- Generating LaTeX or HTML representations of chemical reactions.

## Reference Documentation

**Official docs**: https://bjodah.github.io/chempy/  
**GitHub**: https://github.com/bjodah/chempy  
**Search patterns**: `chempy.Reaction`, `chempy.ReactionSystem`, `chempy.balance_stoichiometry`, `chempy.kinetics`

## Core Principles

### Chemical Entities
Represented as strings ('H2O', 'Fe+3') or Substance objects. ChemPy can parse these to determine composition and charge.

### Reaction Systems
A collection of Reaction objects. This system can be converted into a mathematical model (ODE) where the rates are defined by mass-action kinetics or custom rate laws.

### Units
ChemPy integrates with quantities or pint to ensure dimensional correctness, which is vital for calculating rates (e.g., M⁻¹s⁻¹).

## Quick Reference

### Installation

```bash
pip install chempy
```

### Standard Imports

```python
import numpy as np
import matplotlib.pyplot as plt
from chempy import Reaction, ReactionSystem, Substance
from chempy.util.parsing import formula_to_composition
```

### Basic Pattern - Balancing a Reaction

```python
from chempy import balance_stoichiometry

# 1. Define reactants and products
reac, prod = balance_stoichiometry({'H2', 'O2'}, {'H2O'})

# 2. Output coefficients
print(reac) # {'H2': 2, 'O2': 1}
print(prod) # {'H2O': 2}
```

## Critical Rules

### ✅ DO

- **Use Standard Notation** - Follow standard chemical notation for formulas ('H2SO4', 'Fe+3') for reliable parsing.
- **Define a ReactionSystem** - For any complex network, wrap reactions in a ReactionSystem to manage substances and rates together.
- **Check Mass/Charge Balance** - Always verify that your reactions are balanced before running kinetic simulations.
- **Use Units** - Whenever possible, use a units library to avoid errors in time scales or concentration units.
- **Specify Rate Laws** - Be explicit about whether a reaction is elementary (mass-action) or follows a custom rate law.
- **Vectorize Concentrations** - Use NumPy arrays when providing initial concentrations to solvers.

### ❌ DON'T

- **Manually Balance Complex Equations** - Let balance_stoichiometry handle it, especially for redox reactions.
- **Ignore Ionic Strength** - In analytical chemistry, remember that activity coefficients change with ionic strength (use chempy.einstein).
- **Assume Fast Equilibria** - In kinetic models, ensure your rate constants for "instantaneous" steps are high enough but don't cause numerical stiffness.
- **Hardcode Molar Masses** - Use Substance.from_formula('H2O').mass to ensure precision.

## Anti-Patterns (NEVER)

```python
from chempy import balance_stoichiometry

# ❌ BAD: Manual string parsing to find mass
# mass = 1.008 * 2 + 16.00 # Fragile and tedious

# ✅ GOOD: Use Substance properties
from chempy import Substance
water = Substance.from_formula('H2O')
print(water.mass)

# ❌ BAD: Hardcoding ODEs for kinetics
# def dc_dt(c, t): return [-k*c[0]*c[1], ...] # Error-prone

# ✅ GOOD: Generate ODE from ReactionSystem
from chempy.kinetics.ode import get_odesys
rsys = ReactionSystem.from_string("A + B -> C; k")
odesys, extra = get_odesys(rsys)
# This handles all derivatives automatically
```

## Stoichiometry and Formulas

### Advanced Balancing (Redox)

```python
from chempy import balance_stoichiometry

# Balancing KMn04 + HCl reaction
reactants = {'KMnO4', 'HCl'}
products = {'KCl', 'MnCl2', 'H2O', 'Cl2'}
reac, prod = balance_stoichiometry(reactants, products)

print(f"Balanced: 2 KMnO4 + 16 HCl -> 2 KCl + 2 MnCl2 + 8 H2O + 5 Cl2")
```

### Substance Properties

```python
from chempy import Substance

# Create substance with metadata
ferric = Substance('Fe+3', name='Iron(III) ion', latex='Fe^{3+}')
print(ferric.composition) # {26: 1} - Atomic number 26
print(ferric.charge)      # 3
```

## Chemical Kinetics (chempy.kinetics)

### Simulating Concentration over Time

```python
from chempy import ReactionSystem
from chempy.kinetics.ode import get_odesys
import numpy as np

# 1. Define the system: 2A -> B (rate constant k=0.5)
rsys = ReactionSystem.from_string("2 A -> B; 0.5")

# 2. Get the ODE system
odesys, extra = get_odesys(rsys)

# 3. Integrate
tout = np.linspace(0, 10, 50)
c0 = {'A': 1.0, 'B': 0.0}
result = odesys.integrate(tout, c0)

# 4. Plot
plt.plot(result.tout, result.cout)
plt.legend(rsys.substances.keys())
```

## Chemical Equilibria

### Calculating Speciation

```python
from chempy.equilibria import EqSystem

# Define equilibria: H2O <-> H+ + OH- (Kw = 1e-14)
# and acetic acid dissociation
eqsys = EqSystem.from_string("""
H2O <-> H+ + OH-; 1e-14
CH3COOH <-> CH3COO- + H+; 1.75e-5
""")

# Calculate concentrations given initial state
init_conc = {'H2O': 55.5, 'CH3COOH': 0.1, 'H+': 1e-7, 'OH-': 1e-7, 'CH3COO-': 0}
final_conc, info = eqsys.root(init_conc)

print(f"pH: {-np.log10(final_conc[eqsys.substances.index('H+')]):.2f}")
```

## Physical Chemistry Utilities

### Ionic Strength and Activity

```python
from chempy.electrolytes import ion_strength, davies_activity_coefficient

# Calculate ionic strength of 0.1M Na2SO4
molalities = {'Na+': 0.2, 'SO4-2': 0.1}
I = ion_strength(molalities)

# Davies activity coefficient (extension of Debye-Hückel)
gamma = davies_activity_coefficient(I, z=2, eps=78.3, T=298.15)
print(f"Activity coefficient for SO4-2: {gamma:.3f}")
```

## Practical Workflows

### 1. Titration Curve Simulation

```python
def simulate_titration(acid_conc, base_concs):
    """Calculates pH as base is added to an acid."""
    results = []
    for cb in base_concs:
        # Define complex equilibrium system for each step
        eqsys = EqSystem.from_string(f"HA <-> H+ + A-; 1e-5\nH2O <-> H+ + OH-; 1e-14")
        # Solve for H+ concentration
        ...
    return results
```

### 2. Enzyme Kinetics (Michaelis-Menten ODE)

```python
def enzyme_kinetics():
    # E + S <-> ES -> E + P
    rsys = ReactionSystem.from_string("""
    E + S <-> ES; 1e6, 1e2
    ES -> E + P; 1e3
    """)
    odesys, _ = get_odesys(rsys)
    # Integrate to see substrate depletion and product formation
    ...
```

### 3. Atmospheric Chemistry Model

```python
def ozone_cycle():
    # Simple Chapman Cycle
    reactions = """
    O2 -> 2 O; k1
    O + O2 -> O3; k2
    O3 -> O + O2; k3
    O + O3 -> 2 O2; k4
    """
    rsys = ReactionSystem.from_string(reactions)
    # Solve for steady-state ozone concentration
    ...
```

## Performance Optimization

### Symbolic Derivation
ChemPy uses SymPy under the hood to derive the Jacobian of the ODE system. This makes integration significantly faster and more stable than numerical Jacobian estimation.

### Native Code Generation
For very large systems, ChemPy can use pyodesys to generate C++ or Fortran code from your chemical reaction network, which is then compiled and called from Python.

## Common Pitfalls and Solutions

### The "Stiff System" Problem
Chemical systems often have reactions with widely different time scales (fast proton transfer vs. slow combustion).

```python
# ✅ Solution: Use a stiff-capable solver (like 'cvode' or 'lsoda')
result = odesys.integrate(tout, c0, integrator='lsoda')
```

### Formula Parsing Ambiguity
'Co' could be Cobalt or Carbon + Oxygen.

```python
# ❌ Problem: formula_to_composition('Co') -> {27: 1} (Cobalt)
# ✅ Solution: Use Substance objects to be explicit
sub = Substance('CO', name='Carbon Monoxide')
```

### Units and Floating Point
Equilibrium constants (K) can span 50 orders of magnitude (10⁻⁵⁰ to 10²⁰).

```python
# ❌ Problem: Standard root finders might fail on small values
# ✅ Solution: Solve in log-space (log-concentrations)
final_conc, info = eqsys.root(init_conc, use_log=True)
```

ChemPy brings the precision of physical chemistry to the Python world. By automating the transition from chemical notation to mathematical models, it allows researchers to focus on the chemistry rather than the underlying differential equations.
