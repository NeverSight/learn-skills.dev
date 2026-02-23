---
name: ortools
description: Google Optimization Tools. An open-source software suite for optimization, specialized in vehicle routing, flows, integer and linear programming, and constraint programming. Features the world-class CP-SAT solver. Use for vehicle routing problems (VRP), scheduling, bin packing, knapsack problems, linear programming (LP), integer programming (MIP), network flows, constraint programming, combinatorial optimization, resource allocation, shift scheduling, job-shop scheduling, and discrete optimization problems.
version: 9.8
license: Apache-2.0
---

# Google OR-Tools - Combinatorial Optimization

OR-Tools provides specialized solvers for hard combinatorial problems. Its crown jewel is the CP-SAT solver, which uses Constraint Programming and Satisfiability techniques to find optimal solutions for scheduling and resource allocation problems that are impossible for standard linear solvers.

## When to Use

- **Vehicle Routing (VRP)**: Finding the best paths for a fleet of vehicles to deliver goods.
- **Scheduling**: Creating shift rosters, project timelines, or job-shop schedules.
- **Bin Packing**: Fitting objects of different sizes into a finite number of bins.
- **Knapsack Problem**: Selecting items to maximize value within a weight limit.
- **Linear Programming (LP)**: Standard resource allocation with continuous variables.
- **Integer Programming (MIP)**: Optimization where variables must be whole numbers (e.g., "number of machines to buy").
- **Network Flows**: Calculating max flow or min cost in a graph.

## Reference Documentation

**Official docs**: https://developers.google.com/optimization  
**GitHub**: https://github.com/google/or-tools  
**Search patterns**: `cp_model.CpModel`, `pywraplp.Solver`, `routing_enums_pb2`, `AddConstraint`

## Core Principles

### Modeling vs. Solving

OR-Tools separates the **Definition** of the problem (Variables, Constraints, Objective) from the **Solver** engine. You build a model, then pass it to a solver instance.

### CP-SAT (Constraint Programming)

The most modern and recommended solver for discrete problems. **Critical Note**: CP-SAT works with integers only. If you have floating-point numbers (like `0.5`), you must scale them (e.g., multiply by 100 and work with integers).

### Status Codes

After solving, always check the status. It can be `OPTIMAL`, `FEASIBLE` (a solution found, but maybe not the best), `INFEASIBLE` (impossible to solve), or `LIMIT_REACHED`.

## Quick Reference

### Installation

```bash
pip install ortools
```

### Standard Imports

```python
from ortools.sat.python import cp_model
from ortools.linear_solver import pywraplp
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
```

### Basic Pattern - CP-SAT Solver (Integer Logic)

```python
from ortools.sat.python import cp_model

# 1. Create the model
model = cp_model.CpModel()

# 2. Define variables: NewIntVar(lower_bound, upper_bound, name)
x = model.NewIntVar(0, 10, 'x')
y = model.NewIntVar(0, 10, 'y')

# 3. Add constraints
model.Add(x + y <= 8)
model.Add(x > 2)

# 4. Define Objective
model.Maximize(x + 2 * y)

# 5. Solve
solver = cp_model.CpSolver()
status = solver.Solve(model)

if status == cp_model.OPTIMAL:
    print(f'x = {solver.Value(x)}, y = {solver.Value(y)}')
```

## Critical Rules

### ✅ DO

- **Use CP-SAT for Discrete Tasks** - It is significantly faster than MIP solvers for scheduling and logic-heavy problems.
- **Scale your Floats** - Since CP-SAT is an integer solver, convert `1.25` to `125` and adjust the logic.
- **Check Status First** - Never access variable values if the status is `INFEASIBLE`.
- **Use AddElement for indexing** - To use a variable as an index in an array, use the specialized constraint `model.AddElement`.
- **Set a Time Limit** - For complex problems, use `solver.parameters.max_time_in_seconds = 60.0` to get the best possible solution within a minute.
- **Verify with Value()** - Access results using `solver.Value(var)`, not the variable object itself.

### ❌ DON'T

- **Don't use Python if in Constraints** - You cannot use `if x > 5: model.Add(...)`. Use boolean implications (`OnlyEnforceIf`).
- **Don't use non-linear math** - CP-SAT and LP solvers don't support `x * y` (where both are variables) or `sin(x)`. For `x * y`, you need specialized linearization or piecewise approximations.
- **Avoid huge domains** - Defining a variable with a range of 0 to 1,000,000,000 can slow down the solver. Narrow the bounds as much as possible.

## Anti-Patterns (NEVER)

```python
from ortools.sat.python import cp_model

# ❌ BAD: Using standard Python logic inside the model
# if solver.Value(x) > 5: # ❌ Value() is not available during modeling!
#     model.Add(y == 1)

# ✅ GOOD: Conditional constraints (Logical Implication)
b = model.NewBoolVar('b')
model.Add(x > 5).OnlyEnforceIf(b)
model.Add(x <= 5).OnlyEnforceIf(b.Not())
model.Add(y == 1).OnlyEnforceIf(b)

# ❌ BAD: Floating point variables in CP-SAT
# x = model.NewIntVar(0, 1.5, 'x') # ❌ Error!

# ✅ GOOD: Scaling
# x_scaled = model.NewIntVar(0, 150, 'x_scaled') # 150 represents 1.50
```

## Linear Programming (pywraplp)

### Resource Allocation (Continuous Variables)

```python
from ortools.linear_solver import pywraplp

# Create solver with GLOP backend (Google Linear Optimization Package)
solver = pywraplp.Solver.CreateSolver('GLOP')

# Define continuous variables
x = solver.NumVar(0, solver.infinity(), 'x')
y = solver.NumVar(0, solver.infinity(), 'y')

# Constraint: x + 2y <= 14
ct = solver.Constraint(-solver.infinity(), 14)
ct.SetCoefficient(x, 1)
ct.SetCoefficient(y, 2)

# Objective: Maximize 3x + 4y
objective = solver.Objective()
objective.SetCoefficient(x, 3)
objective.SetCoefficient(y, 4)
objective.SetMaximization()

solver.Solve()
print(f'Solution: x={x.solution_value()}, y={y.solution_value()}')
```

## Vehicle Routing (VRP)

### The Logistics Engine

```python
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def solve_vrp():
    # 1. Distance Matrix (distance between locations)
    data = {'distance_matrix': [[0, 10, 20], [10, 0, 15], [20, 15, 0]],
            'num_vehicles': 1, 'depot': 0}
    
    # 2. Setup Index Manager and Routing Model
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])
    routing = pywrapcp.RoutingModel(manager)
    
    # 3. Create Distance Callback
    def distance_callback(from_index, to_index):
        return data['distance_matrix'][manager.IndexToNode(from_index)][manager.IndexToNode(to_index)]
    
    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    
    # 4. Solve
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    
    solution = routing.SolveWithParameters(search_parameters)
    return solution
```

## Constraint Programming: Scheduling

### Job-Shop Example (Tasks with dependencies)

```python
model = cp_model.CpModel()

# Define an Interval Variable (Start, Duration, End)
duration = 10
start_var = model.NewIntVar(0, 100, 'start')
end_var = model.NewIntVar(0, 100, 'end')
interval_var = model.NewIntervalVar(start_var, duration, end_var, 'interval')

# No-overlap constraint (Machines can only do one task at a time)
model.AddNoOverlap([interval_var1, interval_var2, interval_var3])
```

## Practical Workflows

### 1. Employee Shift Scheduling

```python
def solve_shifts(num_employees, num_days, shifts_per_day):
    model = cp_model.CpModel()
    shifts = {}
    for e in range(num_employees):
        for d in range(num_days):
            for s in range(shifts_per_day):
                shifts[(e, d, s)] = model.NewBoolVar(f'shift_e{e}d{d}s{s}')
                
    # Constraint: Each shift is assigned to exactly one employee
    for d in range(num_days):
        for s in range(shifts_per_day):
            model.Add(sum(shifts[(e, d, s)] for e in range(num_employees)) == 1)
            
    # Constraint: Each employee works at most one shift per day
    for e in range(num_employees):
        for d in range(num_days):
            model.Add(sum(shifts[(e, d, s)] for s in range(shifts_per_day)) <= 1)
            
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    return shifts, solver
```

### 2. Multi-Knapsack (Packing items into bins)

```python
def bin_packing(items, bin_capacities):
    model = cp_model.CpModel()
    # x[i, j] = 1 if item i is in bin j
    x = {}
    for i in range(len(items)):
        for j in range(len(bin_capacities)):
            x[i, j] = model.NewBoolVar(f'x_{i}_{j}')
            
    # Each item in exactly one bin
    for i in range(len(items)):
        model.Add(sum(x[i, j] for j in range(len(bin_capacities))) == 1)
        
    # Bin capacity constraint
    for j in range(len(bin_capacities)):
        model.Add(sum(x[i, j] * items[i] for i in range(len(items))) <= bin_capacities[j])
```

## Performance Optimization

### Hinting (Warm Start)

If you have a good initial guess, provide it to the solver to speed up search.

```python
model.AddHint(x, 5)
model.AddHint(y, 2)
```

### Parallel Solving

CP-SAT can use multiple threads to explore different parts of the search tree.

```python
solver = cp_model.CpSolver()
solver.parameters.num_search_workers = 8 # Use 8 CPU cores
```

## Common Pitfalls and Solutions

### Floating Point Math Errors

As mentioned, OR-Tools CP-SAT is strictly integer.

```python
# ❌ Problem: model.Add(x * 0.1 <= 5)
# ✅ Solution: 
model.Add(x <= 50) # Multiply both sides by 10
```

### Infeasible Models

If `solver.Solve(model)` returns `INFEASIBLE`, it means your constraints are contradictory.

```python
# ✅ Solution: Use 'Sufficient Assmptions' or 'Constraint Relaxation'
# to identify which constraint is causing the conflict.
```

### Symmetry

If items A and B are identical, the solver will waste time checking both "A in Bin 1, B in Bin 2" and "B in Bin 1, A in Bin 2".

```python
# ✅ Solution: Add symmetry-breaking constraints
# model.Add(x_A <= x_B) # Force an ordering
```

## Best Practices

1. **Always check solver status** before accessing variable values
2. **Scale floating-point values** to integers when using CP-SAT
3. **Set time limits** for complex problems to get feasible solutions quickly
4. **Use appropriate solver** - CP-SAT for discrete, GLOP for continuous LP
5. **Break symmetry** in models with identical variables to speed up solving
6. **Narrow variable domains** as much as possible for better performance
7. **Use hints** when you have good initial guesses
8. **Enable parallel solving** for large problems when available
9. **Verify solutions** by checking constraints are satisfied
10. **Document your model** - variable names and constraint logic

Google OR-Tools is the heavy machinery of the optimization world. It solves the discrete puzzles that power global logistics, airline scheduling, and manufacturing, turning impossible "Trial and Error" into mathematical certainty.
