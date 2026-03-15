---
name: pyomo
description: Python Optimization Modeling Objects. A high-level framework for formulating, solving, and analyzing optimization models. Supports Linear Programming (LP), Mixed-Integer Linear Programming (MILP), and Non-Linear Programming (NLP). Part of the COIN-OR project. Use for mathematical optimization, linear programming, mixed-integer programming, non-linear programming, strategic planning, process engineering, energy systems, supply chain optimization, stochastic programming, and solver integration with IPOPT, SCIP, Gurobi, CPLEX, or GLPK.
version: 6.7
license: BSD-3-Clause
---

# Pyomo - Mathematical Optimization Modeling

Pyomo allows you to define optimization problems using a natural mathematical syntax (Sets, Parameters, Variables, Constraints). It decouples the model from the solver, allowing the same model to be solved by different engines without code changes.

## FIRST: Verify Prerequisites

```bash
pip install pyomo
# Also install a solver (e.g., GLPK for linear/integer problems)
# Conda: conda install -c conda-forge glpk ipopt
```

## When to Use

- **Strategic Planning**: Long-term resource allocation or investment planning.
- **Process Engineering**: Optimizing chemical plants or refinery operations (Non-linear).
- **Energy Systems**: Power grid dispatch and unit commitment problems.
- **Supply Chain Optimization**: Multi-period, multi-commodity flow problems.
- **Non-Linear Programming (NLP)**: When your constraints or objectives involve smooth curves (e.g., x², log(x)).
- **Stochastic Programming**: Modeling uncertainty in optimization.
- **Custom Solver Integration**: When you need to use specific solvers like IPOPT, SCIP, or Baron.

## Reference Documentation

**Official docs**: http://www.pyomo.org/  
**GitHub**: https://github.com/Pyomo/pyomo  
**Search patterns**: `pyo.ConcreteModel`, `pyo.Constraint`, `pyo.Objective`, `pyo.SolverFactory`

## Core Principles

### Concrete vs. Abstract Models

- **ConcreteModel**: Data is defined at the time the model is built (most common in Python/Data Science).
- **AbstractModel**: The structure is defined first, and data is loaded later (standard for large-scale industrial models).

### Components

- **Var**: Unknowns the solver needs to find.
- **Set/Param**: Data that defines the problem instance.
- **Objective**: The function to minimize or maximize.
- **Constraint**: Rules the variables must follow.

### Solvers

Pyomo does not have its own solver. It requires external solvers (like glpk for LP/MIP or ipopt for NLP) installed on the system.

## Quick Reference

### Installation

```bash
pip install pyomo
# Also install a solver (e.g., GLPK for linear/integer problems)
# Conda: conda install -c conda-forge glpk ipopt
```

### Standard Imports

```python
import pyomo.environ as pyo
from pyomo.opt import SolverFactory
```

### Basic Pattern - Simple Linear Model (Concrete)

```python
import pyomo.environ as pyo

# 1. Create Model
model = pyo.ConcreteModel()

# 2. Define Variables
model.x = pyo.Var(within=pyo.NonNegativeReals)
model.y = pyo.Var(within=pyo.NonNegativeReals)

# 3. Define Objective (Minimize x + 2*y)
model.obj = pyo.Objective(expr=model.x + 2*model.y, sense=pyo.minimize)

# 4. Define Constraints
model.con1 = pyo.Constraint(expr=3*model.x + 4*model.y >= 12)
model.con2 = pyo.Constraint(expr=2*model.x + 5*model.y >= 10)

# 5. Solve
solver = pyo.SolverFactory('glpk')
results = solver.solve(model)

# 6. Access Results
print(f"x = {pyo.value(model.x)}, y = {pyo.value(model.y)}")
```

## Critical Rules

### ✅ DO

- **Scale your problem** - Like all optimization, Pyomo works best if variables and constraints are within a similar order of magnitude (e.g., 0.1 to 100).
- **Use pyo.value()** - Always wrap variables in `pyo.value(model.x)` to get their numerical result after solving.
- **Check Solver Status** - Verify the solver reached an optimal solution using `results.solver.termination_condition`.
- **Use pyo.Set and pyo.Param** - For complex models, organize data using these components rather than raw Python lists/dicts.
- **Specify Solver Options** - Use `solver.options['tm_limit'] = 60` (or similar depending on the solver) to manage execution time.
- **Use model.dual** - If the solver supports it, enable dual suffix to get shadow prices (important for economic analysis).

### ❌ DON'T

- **Don't use Python math functions** - Use `pyo.log()`, `pyo.exp()`, `pyo.sqrt()` instead of `math.log()` or `np.log()` inside expressions.
- **Don't use if statements in constraints** - Constraints must be algebraic. Use "Big-M" notation or logical reformulations for conditional logic.
- **Avoid "Hard" non-linearities** - Functions like `abs(x)` or `max(x, y)` are non-smooth and can break many solvers. Use reformulations.
- **Don't forget the Intercept/Constant** - Constraints like `x + y = 10` are fine, but ensure your units are consistent.

## Anti-Patterns (NEVER)

```python
import pyomo.environ as pyo
import numpy as np

# ❌ BAD: Using NumPy/Math functions in constraints
# model.con = pyo.Constraint(expr=np.sin(model.x) <= 0.5)

# ✅ GOOD: Use Pyomo-compatible functions
model.con = pyo.Constraint(expr=pyo.sin(model.x) <= 0.5)

# ❌ BAD: Using Python IF for conditional constraints
# if model.x > 10:
#     model.con = pyo.Constraint(expr=model.y <= 5)

# ✅ GOOD: Using Big-M notation (for binary variable z)
# y <= 5 + M * (1 - z)
# x >= 10 - M * (1 - z)

# ❌ BAD: Printing a variable directly
# print(model.x) # Returns a reference object, not a number!

# ✅ GOOD: Use value()
print(pyo.value(model.x))
```

## Modeling with Sets and Indices

### Large-Scale Model Construction

```python
model = pyo.ConcreteModel()

# Data
products = ['A', 'B', 'C']
profit = {'A': 10, 'B': 20, 'C': 15}
limit = 100

# Components
model.P = pyo.Set(initialize=products)
model.x = pyo.Var(model.P, within=pyo.NonNegativeReals)

# Indexed Objective
def obj_rule(model):
    return sum(profit[p] * model.x[p] for p in model.P)
model.obj = pyo.Objective(rule=obj_rule, sense=pyo.maximize)

# Indexed Constraint
def limit_rule(model):
    return sum(model.x[p] for p in model.P) <= limit
model.con = pyo.Constraint(rule=limit_rule)
```

## Non-Linear Programming (NLP)

### Using the IPOPT Solver

```python
# Solving: Minimize (x-2)^2 + (y-2)^2
model = pyo.ConcreteModel()
model.x = pyo.Var(initialize=0) # Initialization is CRUCIAL for NLP
model.y = pyo.Var(initialize=0)

model.obj = pyo.Objective(expr=(model.x - 2)**2 + (model.y - 2)**2)

# Constraint: x^2 + y <= 1
model.con = pyo.Constraint(expr=model.x**2 + model.y <= 1)

# Solve with IPOPT
solver = pyo.SolverFactory('ipopt')
solver.solve(model)
```

## Mixed-Integer Linear Programming (MILP)

### Discrete Decisions

```python
# Binary variable: 1 if we open a warehouse, 0 otherwise
model.use_warehouse = pyo.Var(within=pyo.Binary)

# Integer variable: Number of trucks to buy
model.num_trucks = pyo.Var(within=pyo.NonNegativeIntegers)

# Conditional logic: If warehouse is not used, trucks must be 0
# trucks <= Capacity * use_warehouse
model.cap_con = pyo.Constraint(expr=model.num_trucks <= 100 * model.use_warehouse)
```

## Practical Workflows

### 1. Diet Problem (Classic Linear Programming)

```python
def solve_diet(foods, nutrients, costs, requirements):
    model = pyo.ConcreteModel()
    model.F = pyo.Set(initialize=foods)
    model.N = pyo.Set(initialize=nutrients)
    
    model.x = pyo.Var(model.F, within=pyo.NonNegativeReals)
    
    # Minimize cost
    model.obj = pyo.Objective(expr=sum(costs[f] * model.x[f] for f in model.F))
    
    # Meet nutrient requirements
    def nutrient_rule(model, n):
        return sum(nutrients[f][n] * model.x[f] for f in model.F) >= requirements[n]
    model.con = pyo.Constraint(model.N, rule=nutrient_rule)
    
    pyo.SolverFactory('glpk').solve(model)
    return {f: pyo.value(model.x[f]) for f in model.F}
```

### 2. Blending Problem (Chemical/Process Engineering)

```python
# Balancing component fractions in a mixture
# Note: Often becomes non-linear (NLP) if both flow and fraction are variables
def blend_optimization(inputs, target_purity):
    model = pyo.ConcreteModel()
    # ... model setup ...
    # con: sum(flow[i] * purity[i]) / sum(flow[i]) == target_purity
    # becomes: sum(flow[i] * purity[i]) == target_purity * sum(flow[i]) (Linearized)
```

## Performance Optimization

### Solver Choice

- **GLPK/CBC**: Good for free/open-source LP/MIP.
- **Gurobi/CPLEX**: Industrial standards (extremely fast for large MIP).
- **IPOPT**: Best for smooth Non-linear (NLP).

### Warm Starts

For iterative optimizations, use the previous solution as a starting point.

```python
# For NLP solvers like IPOPT
model.x.set_value(prev_x_value)
solver.solve(model)
```

## Common Pitfalls and Solutions

### Termination Condition

Always check why the solver stopped.

```python
from pyomo.opt import TerminationCondition

results = solver.solve(model)
if results.solver.termination_condition == TerminationCondition.optimal:
    print("Success")
elif results.solver.termination_condition == TerminationCondition.infeasible:
    print("Check your constraints!")
```

### Non-Convexity in NLP

If your NLP model has multiple local minima, IPOPT might get stuck.

```python
# ✅ Solution: 
# 1. Provide multiple different initial guesses (multistart).
# 2. Use a global solver like BARON or SCIP.
```

### Indexing with Variables

`model.x[model.y]` where `y` is a `Var` is illegal.

```python
# ✅ Solution: Use model.AddElement or binary variable reformulations.
```

## Best Practices

1. Always scale your problem - variables and constraints should be within similar orders of magnitude
2. Use `pyo.value()` to extract numerical results from variables after solving
3. Check solver termination conditions to verify optimality or diagnose issues
4. Use `pyo.Set` and `pyo.Param` for organizing data in complex models
5. Initialize variables for NLP problems - good starting points are crucial
6. Use Pyomo-compatible functions (`pyo.log()`, `pyo.exp()`, etc.) instead of NumPy/math functions in expressions
7. Reformulate conditional logic using Big-M notation or binary variables
8. Avoid non-smooth functions like `abs()` or `max()` - use reformulations
9. Enable dual suffix for shadow prices when economic analysis is needed
10. Set solver time limits and options appropriately for your problem size

Pyomo is the ultimate tool for turning high-level mathematical abstractions into solved business and scientific problems. Its ability to bridge the gap between algebraic modeling and high-performance solvers makes it the foundation of modern prescriptive analytics.
