---
name: milp-modeling-gurobi
description: When the user wants to build, solve, and debug mixed-integer linear programs in Python with Gurobi — creating variables, writing constraint-builder functions, setting objectives and parameters, handling solver status, and extracting solutions safely. Also use when the user mentions "gurobipy," "build a MIP model," "mixed-integer program," "addVar," "addConstr," "tupledict," or asks why reading .X fails after optimize. For products of variables, big-M choices, and piecewise-linear terms, see linearization-techniques; for callbacks, IIS deep-dives, and solution pools, see gurobi-advanced-features.
---

# MILP Modeling with Gurobi

You are an expert in mathematical optimization and the gurobipy API. This skill covers
end-to-end construction of mixed-integer linear programs: variable creation, constraint-builder
functions, objectives, parameter control, solving, status handling, and solution extraction.
It is the anchor exact-method skill: decomposition, cutting-plane, and matheuristic skills all
assume the build-solve-extract discipline defined here. Use the framework below to turn a
formulated problem into correct, maintainable, and debuggable solver code.

## Initial Assessment

Establish these facts before writing any model code:

- **Problem class and formulation status.** Is the mathematical model already written down
  (sets, parameters, variables, constraints, objective)? If not, formulate first — see
  problem-formulation. Never start typing `addVar` against a vague word problem.
- **Instance size.** Count variables and constraints as functions of the data
  (e.g., GAP has `m*n` binaries, `n + m` rows). Estimate nonzeros. Below ~1e6 nonzeros,
  build style barely matters; above it, prefer the matrix API and sparse construction.
- **Integrality.** Which decisions are truly discrete? Every avoidable integer variable
  costs branching effort. Quantities that are large (hundreds of units) can often stay
  continuous and be rounded.
- **Hard vs soft constraints.** Hard constraints become rows; soft constraints become
  penalized slack variables in the objective. Confirm the classification with the user
  before coding — it changes the model skeleton.
- **License and solver availability.** Gurobi requires a license (free academic licenses
  exist; the `pip` install ships a size-limited trial). If there is no license, switch to
  open-source-solvers before investing in gurobipy-specific code.
- **Time budget and quality target.** Proven optimality, 1% gap, or "best in 60 seconds"?
  This sets `MIPGap` and `TimeLimit` up front and decides whether a heuristic is the better
  tool entirely.
- **Data format and units.** Where do coefficients come from (CSV, database, generated)?
  Check unit consistency: mixing cents with millions of dollars creates the numerical
  pathologies described under Practical Challenges.
- **Re-solve pattern.** One-shot solve, or repeated solves with changing data
  (rolling horizon, decomposition loop)? Repeated solves favor model modification over
  rebuild and explicit `Seed`/`Threads` control for reproducibility.
- **Deliverable.** A solution table, a reusable module, or an experiment harness?
  This determines how much of the Output Format section applies.

## Model Anatomy

The object of study is the mixed-integer linear program

$$
\min_{x,\,y} \; c^{\top} x + d^{\top} y
\quad \text{s.t.} \quad
A x + G y \le b, \qquad
x \in \mathbb{Z}^{n}_{\ge 0}, \quad
y \in \mathbb{R}^{m}_{\ge 0}.
$$

Dropping integrality gives the LP relaxation, solvable in polynomial time; the integrality
restriction makes MILP NP-hard, and branch-and-bound explores a worst-case exponential tree.
In practice difficulty is governed less by size than by the tightness of the LP relaxation:
a 1e6-variable model with a tight relaxation can solve in minutes while a 500-variable model
with loose big-M constraints stalls for hours (Wolsey (1998), *Integer Programming*;
Klotz & Newman (2013), *Practical guidelines for solving difficult mixed integer linear
programs*). Formulation strength is covered in integer-programming-techniques; this skill
makes sure the model you build is the model you meant.

### The gurobipy object model

| Object | Created by | Role |
|---|---|---|
| `gp.Env` | implicit, or `gp.Env()` explicitly | license session; create explicitly in services so it can be disposed cleanly |
| `gp.Model` | `gp.Model("name")` | owns variables, constraints, objective, parameters, attributes |
| `gp.Var` | `model.addVar(...)` | single decision variable with `lb`, `ub`, `vtype`, `obj`, `name` |
| `gp.tupledict` of `Var` | `model.addVars(...)` | indexed variable family; supports `.sum(...)`, `.select(...)`, `.items()` |
| `gp.LinExpr` | arithmetic, `gp.quicksum` | linear expression; `quicksum` is the fast accumulator |
| `gp.Constr` | `model.addConstr(s)(...)` | named linear row; query `Pi`, `Slack`, `RHS` after solve |
| `gp.MVar` / matrix constraints | `model.addMVar`, `A @ x <= b` | numpy-style blocks for large regular structure |

### Variable types

| `vtype` | Use for | Watch out |
|---|---|---|
| `GRB.CONTINUOUS` | quantities, flows, slacks | default `lb` is `0.0`; free variables need `lb=-GRB.INFINITY` |
| `GRB.BINARY` | on/off, assignment, setup decisions | solution values are floats near 0/1; test with `> 0.5`, never `== 1` |
| `GRB.INTEGER` | counts, lot sizes | always set a finite, data-derived `ub`; loose bounds weaken the relaxation |
| `GRB.SEMICONT` / `GRB.SEMIINT` | value is 0 or in `[lb, ub]` | replaces an explicit binary + big-M link; solver branches on the disjunction |

### Lifecycle rules

- **Lazy updates.** gurobipy batches `addVar`/`addConstr` calls; the model is synchronized at
  `optimize()` or an explicit `model.update()`. Querying an attribute of a just-added object
  before an update raises an error — this is the classic first-session surprise.
- **Attributes are phase-dependent.** `var.X`, `model.ObjVal`, `constr.Pi` exist only after a
  solve that produced what you are asking for. Gate every read on `model.Status` and
  `model.SolCount` as in the harness below.
- **Name everything.** Named variables and constraints make `model.write("model.lp")` readable.
  Writing the LP file and reading it line by line is the single most effective model-debugging
  technique: you see the model the solver sees, after your indexing bugs.
- **Modify, don't rebuild.** `constr.RHS`, `var.Obj`, `var.LB/UB`, and `model.chgCoeff` support
  re-solve loops; Gurobi reuses the LP basis or MIP incumbent where possible.

### When MILP is the right hammer

- Objective and constraints are linear, or linearizable at acceptable cost
  (products, absolute values, piecewise terms — see linearization-techniques).
- Proven bounds or optimality certificates matter (publication, money, safety).
- Instance sizes are moderate, or the relaxation is known to be strong.
- Prefer CP-SAT for deeply disjunctive scheduling, and metaheuristics when the evaluation
  budget is tiny or constraints resist linearization; the triage logic lives in
  problem-formulation.

## A Reusable Build-Solve-Extract Skeleton

Every model in this repository follows one skeleton. Constraint families get one builder
function each — this keeps the formulation reviewable (each function maps to one block of
math), unit-testable, and reusable across model variants.

```text
BUILD-SOLVE-EXTRACT(data):
1. model <- Model(name); set Params explicitly (TimeLimit, MIPGap, Seed, Threads)
2. vars  <- add_variables(model, data)          # vtype, lb, ub fixed at creation time
3. for each constraint family F in the formulation:
       add_F_constraints(model, vars, data)     # one function per family, named rows
4. set_objective(model, vars, data)
5. model.optimize()
6. case model.Status of
       OPTIMAL                      -> extract ObjVal, var.X, ObjBound, MIPGap
       TIME_LIMIT and SolCount > 0  -> extract incumbent, report remaining gap
       TIME_LIMIT and SolCount == 0 -> report bound only; consider MIPFocus=1 rerun
       INFEASIBLE                   -> computeIIS(); inspect conflicting rows/bounds
       INF_OR_UNBD                  -> set DualReductions=0, re-optimize to disambiguate
       UNBOUNDED                    -> missing constraint or sign error in the objective
7. validate the extracted solution with code that never touches the model
```

Construction idioms first — `addVars` index sets, `tupledict.sum`, generator-based
`addConstrs` with named families, `quicksum` objectives — on a small transportation model:

```python
"""Core gurobipy construction idioms on a tiny transportation model."""
import gurobipy as gp
from gurobipy import GRB

plants = ["p1", "p2"]
markets = ["m1", "m2", "m3"]
supply = {"p1": 30.0, "p2": 25.0}
demand = {"m1": 15.0, "m2": 20.0, "m3": 18.0}
cost = {
    ("p1", "m1"): 4.0, ("p1", "m2"): 6.0, ("p1", "m3"): 9.0,
    ("p2", "m1"): 5.0, ("p2", "m2"): 3.0, ("p2", "m3"): 7.0,
}

model = gp.Model("transport_idioms")
model.Params.OutputFlag = 0

# addVars over two index sets -> tupledict keyed by (plant, market) tuples.
ship = model.addVars(plants, markets, lb=0.0, name="ship")

# tupledict.sum with wildcards replaces hand-written quicksum for pure sums.
model.addConstrs((ship.sum(i, "*") <= supply[i] for i in plants), name="supply")
model.addConstrs((ship.sum("*", j) >= demand[j] for j in markets), name="demand")

model.setObjective(
    gp.quicksum(cost[i, j] * ship[i, j] for i in plants for j in markets),
    GRB.MINIMIZE,
)
model.optimize()

if model.Status == GRB.OPTIMAL:
    flows = {key: var.X for key, var in ship.items() if var.X > 1e-6}
    print(f"cost={model.ObjVal:.1f}")
    print(flows)
# Expected: cost=272.0 — p2 serves all of m2 (its comparative advantage), the
# remainder of p2 goes to m3, and p1 covers m1 plus the rest of m3.
```

The reusable harness wraps steps 5-7. It is solver-status-complete: it never reads `.X`
without a usable incumbent, it disambiguates `INF_OR_UNBD`, and it returns a plain dataclass
so downstream code (validators, result tables, plots) never holds gurobipy objects.

```python
"""Reusable solve-and-extract harness with explicit status handling."""
from dataclasses import dataclass, field
from typing import Any

import gurobipy as gp
from gurobipy import GRB

STATUS_NAMES: dict[int, str] = {
    GRB.OPTIMAL: "OPTIMAL",
    GRB.INFEASIBLE: "INFEASIBLE",
    GRB.UNBOUNDED: "UNBOUNDED",
    GRB.INF_OR_UNBD: "INF_OR_UNBD",
    GRB.TIME_LIMIT: "TIME_LIMIT",
    GRB.INTERRUPTED: "INTERRUPTED",
}


@dataclass
class SolveResult:
    """Everything worth keeping from one solve, decoupled from gurobipy objects."""

    status_name: str
    objective: float | None
    best_bound: float | None
    mip_gap: float | None
    runtime_s: float
    solution: dict[str, dict[Any, float]] = field(default_factory=dict)

    @property
    def has_solution(self) -> bool:
        """True when objective and variable values are safe to use."""
        return self.objective is not None


def solve_and_extract(
    model: gp.Model,
    var_groups: dict[str, gp.tupledict],
    time_limit_s: float = 60.0,
    mip_gap: float = 1e-4,
    seed: int = 0,
) -> SolveResult:
    """Set parameters explicitly, optimize, extract values only if an incumbent exists."""
    model.Params.TimeLimit = time_limit_s
    model.Params.MIPGap = mip_gap
    model.Params.Seed = seed
    model.optimize()

    if model.Status == GRB.INF_OR_UNBD:
        # Presolve could not separate the two cases; rerun without dual reductions.
        model.Params.DualReductions = 0
        model.optimize()

    status_name = STATUS_NAMES.get(model.Status, f"STATUS_{model.Status}")
    usable = model.Status == GRB.OPTIMAL or (
        model.Status in (GRB.TIME_LIMIT, GRB.INTERRUPTED) and model.SolCount > 0
    )
    if not usable:
        return SolveResult(status_name, None, None, None, model.Runtime)

    is_mip = model.IsMIP == 1
    return SolveResult(
        status_name=status_name,
        objective=model.ObjVal,
        best_bound=model.ObjBound if is_mip else model.ObjVal,
        mip_gap=model.MIPGap if is_mip else 0.0,
        runtime_s=model.Runtime,
        solution={
            group: {key: var.X for key, var in tdict.items()}
            for group, tdict in var_groups.items()
        },
    )


# Tiny demo: a three-item 0-1 knapsack.
demo = gp.Model("harness_demo")
demo.Params.OutputFlag = 0
items = [0, 1, 2]
value = {0: 8.0, 1: 11.0, 2: 6.0}
weight = {0: 5.0, 1: 7.0, 2: 4.0}
pick = demo.addVars(items, vtype=GRB.BINARY, name="pick")
demo.addConstr(gp.quicksum(weight[i] * pick[i] for i in items) <= 10.0, name="budget")
demo.setObjective(gp.quicksum(value[i] * pick[i] for i in items), GRB.MAXIMIZE)

result = solve_and_extract(demo, {"pick": pick})
print(result.status_name, result.objective, result.solution["pick"])
# Expected: OPTIMAL 14.0 — items 0 and 2 chosen (weight 9 <= 10); item 1 alone gives only 11.
```

## Worked Example 1: Production Mix — LP to MIP

The canonical walkthrough: start with the continuous production-mix LP, read its full dual
story, then watch integrality and fixed charges change the answer. Products $j$ with unit
profit $p_j$ compete for resources $r$ with capacity $b_r$, consuming $a_{rj}$ per unit:

$$
\max \sum_{j} p_j x_j
\quad \text{s.t.} \quad
\sum_{j} a_{rj}\, x_j \le b_r \;\; \forall r, \qquad x_j \ge 0.
$$

The LP's dual values price the resources: $\pi_r$ is the marginal profit of one extra unit of
resource $r$ (valid within the RHS sensitivity range), and a nonbasic product's reduced cost
says how far its profit must rise before producing it becomes attractive.

```python
"""Production-mix LP with full dual analysis: shadow prices, reduced costs, ranges."""
import gurobipy as gp
from gurobipy import GRB

PRODUCTS = ["chair", "table", "desk"]
RESOURCES = ["wood", "labor"]
PROFIT = {"chair": 45.0, "table": 80.0, "desk": 110.0}
CAPACITY = {"wood": 400.0, "labor": 450.0}
USAGE = {  # (resource, product) -> units consumed per unit produced
    ("wood", "chair"): 5.0, ("wood", "table"): 20.0, ("wood", "desk"): 25.0,
    ("labor", "chair"): 10.0, ("labor", "table"): 15.0, ("labor", "desk"): 20.0,
}


def build_production_lp() -> tuple[gp.Model, gp.tupledict]:
    """Continuous production mix: max p'x subject to Ax <= b, x >= 0."""
    model = gp.Model("production_mix_lp")
    model.Params.OutputFlag = 0
    x = model.addVars(PRODUCTS, lb=0.0, name="x")
    model.addConstrs(
        (
            gp.quicksum(USAGE[r, p] * x[p] for p in PRODUCTS) <= CAPACITY[r]
            for r in RESOURCES
        ),
        name="capacity",
    )
    model.setObjective(gp.quicksum(PROFIT[p] * x[p] for p in PRODUCTS), GRB.MAXIMIZE)
    return model, x


model, x = build_production_lp()
model.optimize()
assert model.Status == GRB.OPTIMAL

print(f"objective = {model.ObjVal:.2f}")
for p in PRODUCTS:
    print(f"  x[{p}] = {x[p].X:7.3f}   reduced cost = {x[p].RC:7.3f}")
for r in RESOURCES:
    row = model.getConstrByName(f"capacity[{r}]")
    print(
        f"  {r}: shadow price = {row.Pi:.4f}, slack = {row.Slack:.2f}, "
        f"RHS valid in [{row.SARHSLow:.1f}, {row.SARHSUp:.1f}]"
    )
# Expected: objective = 2258.33 with x = (chair 21.667, table 0, desk 11.667).
# Table's reduced cost is -4.167: its profit must rise above 84.17 to enter the mix.
# Shadow prices: wood 1.3333, labor 3.8333 — labor is the more valuable bottleneck.
```

Now the MIP step. Real production runs in integer lots, a production line incurs a fixed
setup cost $f_j$ when used, and a used line must produce at least a minimum lot $\ell_j$.
Introduce binaries $y_j \in \{0,1\}$ and link them to the quantities:

$$
\max \sum_j \left( p_j x_j - f_j y_j \right)
\quad \text{s.t.} \quad
\sum_j a_{rj} x_j \le b_r \;\forall r, \qquad
\ell_j\, y_j \le x_j \le u_j\, y_j \;\forall j, \qquad
x_j \in \mathbb{Z}_{\ge 0},\; y_j \in \{0,1\}.
$$

The linking coefficient $u_j$ is the big-M, and it must be tight: the best data-derived bound
is $u_j = \min_r \lfloor b_r / a_{rj} \rfloor$, the most production any single resource allows.
A lazy `1e6` here would weaken the relaxation and slow branching for no benefit.

```python
"""Production mix as a MIP: integer lots, fixed setup charges, minimum lot sizes."""
import math

import gurobipy as gp
from gurobipy import GRB

PRODUCTS = ["chair", "table", "desk"]
RESOURCES = ["wood", "labor"]
PROFIT = {"chair": 45.0, "table": 80.0, "desk": 110.0}
CAPACITY = {"wood": 400.0, "labor": 450.0}
USAGE = {
    ("wood", "chair"): 5.0, ("wood", "table"): 20.0, ("wood", "desk"): 25.0,
    ("labor", "chair"): 10.0, ("labor", "table"): 15.0, ("labor", "desk"): 20.0,
}
SETUP_COST = {"chair": 200.0, "table": 150.0, "desk": 300.0}
MIN_LOT = {"chair": 5, "table": 5, "desk": 5}


def build_production_mip() -> tuple[gp.Model, gp.tupledict, gp.tupledict]:
    """Integer lots with fixed charges; big-M values derived from data, never guessed."""
    model = gp.Model("production_mix_mip")
    # Tightest valid upper bound on x[p]: the most any single resource allows.
    max_lot = {
        p: math.floor(min(CAPACITY[r] / USAGE[r, p] for r in RESOURCES))
        for p in PRODUCTS
    }
    x = model.addVars(
        PRODUCTS, vtype=GRB.INTEGER, lb=0,
        ub=[max_lot[p] for p in PRODUCTS], name="x",
    )
    y = model.addVars(PRODUCTS, vtype=GRB.BINARY, name="y")

    model.addConstrs(
        (
            gp.quicksum(USAGE[r, p] * x[p] for p in PRODUCTS) <= CAPACITY[r]
            for r in RESOURCES
        ),
        name="capacity",
    )
    model.addConstrs((x[p] <= max_lot[p] * y[p] for p in PRODUCTS), name="setup_link")
    model.addConstrs((x[p] >= MIN_LOT[p] * y[p] for p in PRODUCTS), name="min_lot")

    model.setObjective(
        gp.quicksum(PROFIT[p] * x[p] - SETUP_COST[p] * y[p] for p in PRODUCTS),
        GRB.MAXIMIZE,
    )
    return model, x, y


model, x, y = build_production_mip()
model.Params.OutputFlag = 0
model.Params.MIPGap = 1e-9  # prove optimality on this tiny instance
model.optimize()
assert model.Status == GRB.OPTIMAL

plan = {p: round(x[p].X) for p in PRODUCTS}
setups = {p: round(y[p].X) for p in PRODUCTS}
print(f"objective = {model.ObjVal:.1f}  plan = {plan}  setups = {setups}")
# Expected: objective = 1850.0 with plan chair=24, table=14, desk=0.
# The LP loved desks; the 300 setup charge flips the optimal mix to chairs + tables —
# integrality and fixed costs change structure, not just round the LP answer.
```

The qualitative lesson generalizes: never present a rounded LP solution as "near-optimal" when
fixed charges or logical constraints are present. Here rounding the LP would keep desks open
and lose 105 profit versus the true optimum, and on larger instances rounding is often
infeasible outright.

## Worked Example 2: Generalized Assignment Problem

GAP assigns each job $j$ to exactly one machine $i$, paying cost $c_{ij}$ and consuming
capacity $a_{ij}$ of machine $i$'s budget $b_i$ (Ross & Soland (1975); Martello & Toth (1990),
*Knapsack Problems*):

$$
\min \sum_{i}\sum_{j} c_{ij} x_{ij}
\quad \text{s.t.} \quad
\sum_{i} x_{ij} = 1 \;\; \forall j, \qquad
\sum_{j} a_{ij} x_{ij} \le b_i \;\; \forall i, \qquad
x_{ij} \in \{0,1\}.
$$

The two constraint families have different characters — partitioning rows and knapsack rows —
so they get one builder function each. This is exactly the structure that Lagrangian and
column-generation methods later exploit; building it cleanly now pays off when the model
becomes a subproblem.

```python
"""Generalized assignment problem: min-cost job-to-machine assignment under capacities."""
from dataclasses import dataclass

import gurobipy as gp
from gurobipy import GRB


@dataclass(frozen=True)
class GapInstance:
    """GAP data: cost[i][j] and usage[i][j] for machine i and job j; capacity[i]."""

    cost: tuple[tuple[float, ...], ...]
    usage: tuple[tuple[float, ...], ...]
    capacity: tuple[float, ...]

    @property
    def machines(self) -> range:
        """Machine index set."""
        return range(len(self.capacity))

    @property
    def jobs(self) -> range:
        """Job index set."""
        return range(len(self.cost[0]))


def add_assignment_constraints(model: gp.Model, x: gp.tupledict, inst: GapInstance) -> None:
    """Each job goes to exactly one machine (set-partitioning rows)."""
    model.addConstrs(
        (gp.quicksum(x[i, j] for i in inst.machines) == 1 for j in inst.jobs),
        name="assign",
    )


def add_capacity_constraints(model: gp.Model, x: gp.tupledict, inst: GapInstance) -> None:
    """Per-machine resource budget (knapsack rows)."""
    model.addConstrs(
        (
            gp.quicksum(inst.usage[i][j] * x[i, j] for j in inst.jobs)
            <= inst.capacity[i]
            for i in inst.machines
        ),
        name="capacity",
    )


def build_gap_model(inst: GapInstance) -> tuple[gp.Model, gp.tupledict]:
    """Assemble the GAP MIP: one builder function per constraint family."""
    model = gp.Model("gap")
    x = model.addVars(inst.machines, inst.jobs, vtype=GRB.BINARY, name="x")
    add_assignment_constraints(model, x, inst)
    add_capacity_constraints(model, x, inst)
    model.setObjective(
        gp.quicksum(
            inst.cost[i][j] * x[i, j] for i in inst.machines for j in inst.jobs
        ),
        GRB.MINIMIZE,
    )
    return model, x


def solve_gap(inst: GapInstance, time_limit_s: float = 30.0) -> dict[int, int] | None:
    """Solve and return job -> machine, or None when no incumbent exists."""
    model, x = build_gap_model(inst)
    model.Params.OutputFlag = 0
    model.Params.TimeLimit = time_limit_s
    model.Params.MIPGap = 1e-9
    model.optimize()
    usable = model.Status == GRB.OPTIMAL or (
        model.Status == GRB.TIME_LIMIT and model.SolCount > 0
    )
    if not usable:
        return None
    print(f"objective = {model.ObjVal:.1f}  gap = {model.MIPGap:.2%}")
    return {j: i for i in inst.machines for j in inst.jobs if x[i, j].X > 0.5}


INST = GapInstance(
    cost=((6.0, 9.0, 4.0, 8.0), (5.0, 3.0, 8.0, 6.0)),
    usage=((3.0, 4.0, 2.0, 5.0), (4.0, 2.0, 5.0, 3.0)),
    capacity=(8.0, 8.0),
)
print(solve_gap(INST))
# Expected: objective = 19.0, assignment {0: 0, 1: 1, 2: 0, 3: 1}.
# Cheapest row-wise assignment costs 18 but overloads machine 1 (load 9 > 8);
# moving job 0 to machine 0 is the cheapest repair (+1).
```

Every model deserves an independent validator: a function that recomputes feasibility and the
objective from raw data and a plain solution, importing nothing from the solver. It catches
indexing bugs, wrong-direction inequalities, and silent unit errors that the solver cannot see
(it faithfully optimizes whatever wrong model you gave it).

```python
"""Independent feasibility and objective check for a GAP solution (no solver involved)."""


def validate_gap_solution(
    assignment: dict[int, int],
    cost: list[list[float]],
    usage: list[list[float]],
    capacity: list[float],
    tol: float = 1e-6,
) -> tuple[float, list[str]]:
    """Recompute objective and collect violations; an empty list means feasible."""
    n_machines, n_jobs = len(capacity), len(cost[0])
    violations: list[str] = []
    if sorted(assignment) != list(range(n_jobs)):
        violations.append("not every job is assigned exactly once")
    total = 0.0
    load = [0.0] * n_machines
    for job, machine in assignment.items():
        total += cost[machine][job]
        load[machine] += usage[machine][job]
    for i in range(n_machines):
        if load[i] > capacity[i] + tol:
            violations.append(f"machine {i} overloaded: {load[i]} > {capacity[i]}")
    return total, violations


obj, errors = validate_gap_solution(
    {0: 0, 1: 1, 2: 0, 3: 1},
    cost=[[6.0, 9.0, 4.0, 8.0], [5.0, 3.0, 8.0, 6.0]],
    usage=[[3.0, 4.0, 2.0, 5.0], [4.0, 2.0, 5.0, 3.0]],
    capacity=[8.0, 8.0],
)
print(obj, errors)
# Expected: 19.0 [] — matches the solver's objective with zero violations.
```

Cross-check the validator's objective against `model.ObjVal` on every run; a mismatch larger
than `1e-6 * |ObjVal|` means the model and your intent have diverged.

## Advanced Techniques

### Matrix API for large, regular structure

When the model is naturally expressed with arrays — knapsacks, assignment blocks, flow
balances over dense index grids — `addMVar` plus `@` builds it one or two orders of magnitude
faster than per-variable loops, because construction happens in C on whole arrays.

```python
"""Matrix API: build a model from numpy arrays with addMVar."""
import numpy as np

import gurobipy as gp
from gurobipy import GRB

value = np.array([8.0, 11.0, 6.0, 4.0])
weight = np.array([5.0, 7.0, 4.0, 3.0])
budget = 10.0

model = gp.Model("knapsack_matrix")
model.Params.OutputFlag = 0
x = model.addMVar(value.size, vtype=GRB.BINARY, name="x")
model.addConstr(weight @ x <= budget, name="budget")
model.setObjective(value @ x, GRB.MAXIMIZE)
model.optimize()

assert model.Status == GRB.OPTIMAL
chosen = np.flatnonzero(x.X > 0.5)
print(f"objective = {model.ObjVal:.1f}  chosen = {chosen.tolist()}")
# Expected: objective = 15.0, chosen = [1, 3] (weights 7 + 3 = 10, exactly the budget).
```

For block-structured constraints pass a `scipy.sparse` matrix to `model.addMConstr` or use
`A @ x <= b` directly with sparse `A`. Mixing styles is fine: use `addMVar` for the bulk
arrays and `addConstrs` generators for the irregular side constraints.

### Parameter strategy by situation

Set parameters explicitly and record them; defaults change between Gurobi versions, and an
unrecorded parameter is an unreproducible experiment.

```python
"""Named parameter profiles: explicit, recorded, reusable."""
import gurobipy as gp

PROFILES: dict[str, dict[str, float | int]] = {
    "prove_optimality": {"MIPGap": 1e-9, "MIPFocus": 2},
    "good_solution_fast": {"MIPGap": 0.01, "MIPFocus": 1, "Heuristics": 0.2, "TimeLimit": 60},
    "hard_root_lp": {"Method": 2, "Crossover": 0},  # barrier, skip crossover
    "reproducible_run": {"Seed": 42, "Threads": 1},
    "numerically_fragile": {"NumericFocus": 2, "IntFeasTol": 1e-7},
}


def apply_profile(model: gp.Model, profile: str) -> None:
    """Apply a named parameter bundle to a model."""
    for param, value in PROFILES[profile].items():
        model.setParam(param, value)


demo = gp.Model("profile_demo")
demo.Params.OutputFlag = 0
apply_profile(demo, "good_solution_fast")
print(demo.Params.MIPGap, demo.Params.TimeLimit)
# Expected: 0.01 60.0
```

| Situation | Parameters that matter |
|---|---|
| Need any good solution quickly | `MIPFocus=1`, `Heuristics=0.2`, modest `MIPGap` (1-5%) |
| Bound moves too slowly | `MIPFocus=3`, `Cuts=2` |
| Proving optimality at the end | `MIPFocus=2`, tight `MIPGap` |
| Root LP dominates runtime | `Method=2` (barrier), `Crossover=0` if a basis is not needed |
| Benchmarking / experiments | `Seed`, `Threads=1`, fixed `TimeLimit` — see the run protocol in your experiment harness |
| Memory pressure on big trees | `NodefileStart=0.5` to spill nodes to disk |

### Diagnosing infeasibility with an IIS

An Irreducible Inconsistent Subsystem is a minimal set of constraints and bounds that is
infeasible together — removing any one member makes it feasible. It turns "model infeasible"
into a short, readable list of suspects. Named constraints make the output meaningful.

```python
"""Infeasibility diagnosis: compute and print an IIS."""
import gurobipy as gp
from gurobipy import GRB

model = gp.Model("infeasible_demo")
model.Params.OutputFlag = 0
x = model.addVar(lb=0.0, name="x")
y = model.addVar(lb=0.0, name="y")
model.addConstr(x + y >= 10.0, name="demand")
model.addConstr(x <= 3.0, name="cap_x")
model.addConstr(y <= 4.0, name="cap_y")
model.optimize()

if model.Status == GRB.INFEASIBLE:
    model.computeIIS()
    members = [c.ConstrName for c in model.getConstrs() if c.IISConstr]
    print("IIS:", members)
# Expected: IIS: ['demand', 'cap_x', 'cap_y'] — max supply 3 + 4 = 7 < 10 demanded;
# dropping any one of the three rows restores feasibility.
```

For "which constraints should I relax and by how much," `model.feasRelax` finds a minimal
weighted relaxation. Both tools, plus callbacks and the solution pool, are covered in depth in
gurobi-advanced-features.

### Numerical hygiene

Keep all matrix coefficients within roughly six orders of magnitude (ideally `1e-3` to `1e6`),
rescale units rather than fight tolerances, and derive every big-M from data as in the
production MIP. Symptoms of trouble: warnings about large coefficient ranges, "solutions" that
your independent validator rejects, and binaries at 0.5 after "optimal" termination. Klotz &
Newman (2013) is the standard practical reference. `IntFeasTol` (default `1e-5`) means a
binary can legitimately return 0.99999 — always extract with `> 0.5`, and tighten the
tolerance rather than post-round when downstream logic is sensitive.

### Warm starts and re-solve loops

Set `var.Start = value` before `optimize()` to inject a known feasible solution; Gurobi
repairs partial starts. In rolling-horizon or decomposition loops, modify `RHS`/`Obj`/bounds
in place instead of rebuilding — the retained basis or incumbent typically cuts re-solve time
substantially. Feed heuristic solutions in as MIP starts whenever you have them; a good
incumbent at the root prunes the tree from the first node.

## Practical Challenges

**Model construction takes longer than the solve.** Python-side expression building is the
usual culprit: `sum(...)` over `LinExpr` objects is quadratic, one `addConstr` call per row
inside nested loops pays call overhead millions of times. Use `gp.quicksum`, generator-based
`addConstrs`, and the matrix API for the dense blocks. Profile build time separately from
`model.Runtime` — they are different problems with different fixes.

**`AttributeError` (unable to retrieve attribute `X`).** You read a solution that does not
exist: before `optimize()`, after `INFEASIBLE`, or after `TIME_LIMIT` with `SolCount == 0`.
Gate every extraction on status as in the harness; never wrap the read in a bare `try/except`
that hides which case occurred.

**Binaries come back as 0.9999999 or 1e-9.** Integrality is enforced only to `IntFeasTol`.
Test binaries with `> 0.5`, recover integer counts with `round(var.X)`, and never use
equality comparisons on solution values. If downstream feasibility is sensitive to the
residue, tighten `IntFeasTol` to `1e-7` and re-solve.

**The model is infeasible but the data "looks fine."** Compute an IIS and read the named
members. The most common root causes, in order: an inequality written in the wrong direction,
a variable's default `lb=0` clashing with a constraint that needs it negative, unit
mismatches between two data sources, and over-tight bounds copied from another instance.
`model.write("model.lp")` and reading the rows around the IIS members settles it quickly.

**Big-M chosen as 1e6 "to be safe."** Oversized big-M weakens the LP relaxation (the solver
branches far more) and creates numerical traps: with `FeasibilityTol = 1e-6`, a big-M of
`1e6` lets `y = 1e-12` "switch off" a constraint while the incumbent quietly violates your
intent. Derive each big-M from capacities and bounds, per entity, as in the production MIP;
if no finite bound exists, reconsider the formulation (indicator constraints are the
fallback — see linearization-techniques).

**The solver says optimal but the answer is wrong in the real world.** The solver proved
optimality of the model you wrote, not the problem you meant. Run the independent validator,
recompute the objective from raw data, and compare term by term. Divergence localizes the bug
to a constraint family or a cost term; this is why builders are separate functions you can
test one at a time.

**The MIP gap stalls for hours.** This is usually formulation weakness or symmetry, not a
parameter issue: identical machines, interchangeable bins, or loose linking constraints leave
the solver enumerating permutations of the same solution. Tighten the relaxation, add
symmetry-breaking, or reformulate — the diagnosis-and-repair playbook is
integer-programming-techniques. Parameter nudges (`MIPFocus`, `Cuts`) buy at most a constant
factor.

**Every data change triggers a full model rebuild.** For re-solve loops, mutate the model:
`constr.RHS = new_value`, `var.Obj = new_cost`, `var.UB = 0.0` to forbid, `model.chgCoeff`
for matrix entries. Rebuild only when the sparsity pattern itself changes. This preserves
warm-start information and often turns minutes per iteration into seconds.

## Tools & Libraries

| Library | When to use | Note |
|---|---|---|
| `gurobipy` | The subject of this skill | Commercial license required; free academic licenses; `pip` install includes a size-limited trial |
| `numpy` | Data prep and the matrix API | `addMVar` + `@` is the fast path for dense regular blocks |
| `scipy.sparse` | Constraint matrices for `addMConstr` | Build COO/CSR once; avoid dense matrices above ~1e4 columns |
| `pandas` | Solution and experiment tables | Convert `SolveResult` objects to tidy one-row-per-run tables |
| `PuLP` / `Pyomo` / `python-mip` | Solver-agnostic modeling layers | Trade API expressiveness for portability — see open-source-solvers |
| HiGHS / SCIP / CBC | No Gurobi license available | Selection and migration guidance in open-source-solvers |
| OR-Tools CP-SAT | Disjunctive scheduling, heavy logical structure | Different modeling paradigm; triage in problem-formulation |

## Output Format

A complete MILP modeling deliverable contains, in order:

1. **Formulation.** Sets, parameters, decision variables (with types and bounds), constraints,
   and objective in mathematical notation — before any code. Every constraint family in the
   code must point back to a numbered line here.
2. **Model summary table.** What was actually built:

   | Component | Count | Detail |
   |---|---|---|
   | Binary variables | m·n | `x[i,j]` assignment |
   | Integer variables | n | `x[p]`, ub from capacity |
   | Constraint family `assign` | n | partitioning rows |
   | Constraint family `capacity` | m | knapsack rows |

3. **Solver configuration.** Gurobi version, every parameter changed from default, seed,
   thread count, hardware if runtimes are reported.
4. **Solution-quality report.** Status, incumbent objective, best bound, relative gap,
   runtime, node count. For `TIME_LIMIT` results, state the gap explicitly — "best found
   1850 (gap 2.3% after 600 s)" — never present an incumbent as optimal.
5. **Decision tables.** Nonzero decisions only (`var.X > 0.5` for binaries,
   `> 1e-6` for continuous), in domain terms ("job 3 on machine 1"), not raw variable dumps.
6. **Validation statement.** Output of the independent checker: recomputed objective, maximum
   constraint violation, and confirmation that it matches `ObjVal` within tolerance.
7. **Artifacts when useful.** `model.write("model.lp")` for review on small instances,
   `model.write("model.mps")` plus the data seed for reproducible bug reports,
   solution JSON/CSV for downstream consumers.

## Questions to Ask

- Is the mathematical formulation written down, or are we starting from a word problem?
- How large is a realistic instance — how many variables and constraints as a function of the data?
- Which constraints are hard, and which are preferences that can be violated at a price?
- Is a Gurobi license available (academic or commercial), or should this target an open-source solver?
- What is the time budget per solve, and is proven optimality required or is a small gap acceptable?
- Will the model be solved once, or repeatedly with changing data (rolling horizon, decomposition loop)?
- Where do the coefficients come from, and are units consistent across data sources?
- Are there quantities currently modeled as integer that could safely be continuous?
- What should the deliverable look like — a solution table, a reusable module, or an experiment harness?

## Related Skills

- **linearization-techniques** — when the formulation contains products of variables, absolute
  values, min/max terms, piecewise-linear costs, or logical implications that must become
  linear before this skill's machinery applies.
- **integer-programming-techniques** — when the model is correct but slow: relaxation
  strength, symmetry breaking, big-M vs indicator trade-offs, and MIP gap interpretation.
- **gurobi-advanced-features** — when you need callbacks (lazy constraints, user cuts,
  heuristic injection), IIS workflows, the solution pool, multi-objective API, or the
  parameter tuning tool.
- **problem-formulation** — when decisions, objective, and constraints are not yet pinned
  down, or when it is unclear whether MILP is the right model class at all.
- **open-source-solvers** — when no Gurobi license is available and the model should be built
  for or migrated to HiGHS, SCIP, CBC, or OR-Tools.
