---
name: open-source-solvers
description: When the user wants to solve LPs, MIPs, or CP models without a commercial license — choosing among HiGHS, SCIP, CBC, OR-Tools (CP-SAT and MathOpt), PuLP, Pyomo, and python-mip, comparing licenses, setting realistic performance expectations versus Gurobi, and migrating gurobipy models to an open-source stack. Also use when the user mentions "open-source solver," "HiGHS," "SCIP," "PuLP," "Pyomo," "CBC," "free solver," or "no Gurobi license." For gurobipy model construction itself, see milp-modeling-gurobi; for deep CP-SAT modeling, see constraint-programming.
---

# Open-Source Solvers

You are an expert in the open-source optimization solver ecosystem: the solvers themselves
(HiGHS, SCIP, CBC, OR-Tools CP-SAT), the modeling layers that reach them (PuLP, Pyomo,
python-mip, OR-Tools MathOpt, scipy), their licenses, and their realistic performance relative
to Gurobi. This skill is a pattern catalog. Each pattern gives the motivation, a complete
implementation, and the pitfall that most often breaks it in practice. Use the selection
framework to pick a stack, then adapt the matching pattern.

## Initial Assessment

Establish the following before recommending a solver or writing any code:

- **Why no commercial solver?** License cost, deployment restrictions (cloud/container nodes
  each need a license), reproducibility for reviewers, or open-source policy. Academics often
  qualify for a free Gurobi license — check before migrating anything.
- **Problem class.** Pure LP, MILP, MIQP, convex MINLP, or feasibility-heavy combinatorial
  structure (scheduling, timetabling)? The last one usually wants CP-SAT, not a MIP solver.
- **Scale and hardness.** Variables, constraints, nonzeros, and integrality gap behavior. A MIP
  Gurobi solves in seconds is fine everywhere; a MIP Gurobi needs hours for may be out of reach
  for CBC entirely and marginal for HiGHS/SCIP.
- **Solve pattern.** One large solve, or thousands of small solves inside a matheuristic loop?
  Loops rule out file-based interfaces (PuLP `*_CMD` solvers) and favor in-memory APIs
  (highspy, PySCIPOpt, python-mip).
- **Needed solver features.** Duals and reduced costs (LP), lazy constraints/cuts via
  callbacks, MIP starts, solution pools, multi-objective. Feature coverage differs sharply
  across open solvers; list the must-haves first.
- **Data types.** CP-SAT accepts only integer coefficients. Float costs force a scaling
  decision before modeling starts.
- **License constraints of the *user's own* code.** GPL solvers (GLPK) impose copyleft on
  distributed binaries; MIT/Apache/EPL solvers do not. Ask whether the model ships inside a
  product.
- **Existing codebase.** A gurobipy codebase migrates most naturally to PySCIPOpt or python-mip
  (same imperative style); a from-scratch project may prefer a portable layer (MathOpt, Pyomo)
  so the solver stays swappable.
- **Time budget and quality target.** Required gap at termination, wall-clock limit, and
  whether a feasible-but-not-proven solution is acceptable. Open solvers prove optimality more
  slowly; often the right move is a fixed time limit plus gap reporting.
- **Environment.** OS, Python version, container or HPC cluster. All stacks below are
  pip-installable on Linux/macOS/Windows; HPC modules sometimes ship older system CBC/GLPK
  binaries that shadow pip versions.

## Solver Landscape and Selection

Two separate decisions: which **solver** does the work, and which **API layer** builds the
model. Conflating them is the most common beginner error ("PuLP is slow" usually means "CBC is
slow" or "the file round-trip is slow").

**Solvers:**

| Solver | Class | License | Python access | One-line judgment |
|---|---|---|---|---|
| HiGHS | LP, MIP, QP | MIT | highspy, scipy ≥ 1.9, PuLP, Pyomo, MathOpt | Fastest open LP; rapidly improving MIP; trivial `pip install highspy` |
| SCIP | MIP, MINLP framework | Apache 2.0 (since 8.0.3, Nov 2022) | PySCIPOpt, MathOpt (GSCIP) | Richest features: plugins, custom branching, separators, exotic constraints |
| CBC | MIP | EPL-2.0 | python-mip, PuLP (bundled), Pyomo | Mature but weakest performer; still fine for small/medium MIPs |
| OR-Tools CP-SAT | CP over integers | Apache 2.0 | ortools | Often beats every MIP solver on scheduling/feasibility-heavy problems |
| GLPK | LP, MIP | GPL-3 | swiglpk, PuLP, Pyomo | Legacy; slow MIP; copyleft — avoid for new work |

**API layers:**

| Layer | License | Reaches | Best for | Build overhead |
|---|---|---|---|---|
| highspy / PySCIPOpt (direct) | MIT / Apache 2.0 | one solver each | full control, re-solves in loops | lowest |
| python-mip | EPL-2.0 | CBC (bundled), Gurobi | fast builds, CBC cut callbacks | low (cffi) |
| OR-Tools MathOpt | Apache 2.0 | HiGHS, GSCIP, GLOP, CP-SAT, Gurobi | one API, swap solver by enum | low |
| PuLP | MIT | CBC (bundled), HiGHS, SCIP, Gurobi, CPLEX | quick models, teaching | medium + file I/O per solve |
| Pyomo | BSD | nearly everything, incl. NLP (Ipopt) | large projects, NLP/MINLP, suffixes | highest (rich objects) |
| scipy (`linprog`/`milp`) | BSD | HiGHS only | matrix-form models, no extra deps | lowest (arrays) |

**Performance expectations vs Gurobi.** Calibrate with the shifted geometric mean used in
solver benchmarking,

$$\mathrm{SGM}(t_1,\dots,t_n) = \exp\!\Big(\tfrac{1}{n}\sum_{i=1}^{n}\ln(t_i + s)\Big) - s,
\qquad s = 10\ \text{s},$$

the metric behind Mittelmann's public benchmarks and the MIPLIB 2017 collection (Gleixner et
al. (2021), "MIPLIB 2017"). Honest rules of thumb as of the mid-2020s:

- **LP:** HiGHS (Huangfu & Hall (2018), parallel dual simplex) is within a small constant
  factor of commercial solvers on most instances; for huge barrier-dominated LPs commercial
  codes still lead. For almost all research LP work, HiGHS is simply enough.
- **MIP:** on broad benchmark sets, Gurobi is typically 2-5× faster than SCIP and HiGHS in
  shifted geometric mean and solves more instances within a fixed time limit; the spread on
  individual hard instances can be 100× either way. CBC is roughly an order of magnitude
  behind SCIP and times out far more often.
- **CP-SAT:** on scheduling, timetabling, and packing-with-logic, CP-SAT regularly beats all
  MIP solvers including Gurobi (repeated MiniZinc Challenge gold medals). It is not a
  replacement for MIP on problems with meaningful LP relaxations and continuous variables.

**Decision guidance:**

- Use **HiGHS** by default for LP and "ordinary" MILP — pip install, MIT license, good speed.
- Use **SCIP** when you need solver internals: lazy constraints, custom branching/separation,
  nonconvex MINLP, or research on the solving process itself (Achterberg (2009), "SCIP:
  solving constraint integer programs").
- Use **CP-SAT** when the model is integer-only with heavy logical/disjunctive structure —
  see **constraint-programming** for modeling depth.
- Use **python-mip or direct APIs** inside matheuristic loops: thousands of solves cannot
  afford file round-trips or heavy object models.
- Use **MathOpt or Pyomo** when the solver must remain swappable (benchmarking, papers that
  report multiple solvers, uncertain deployment licenses).
- Use **scipy.optimize.milp** when the model is naturally matrix-form and you want zero extra
  dependencies — it is HiGHS underneath.
- For pure network problems (max-flow, min-cost flow, assignment), specialized algorithms beat
  general MIP solvers by orders of magnitude — see **network-flow-optimization**.

## Direct Solver APIs: HiGHS, scipy, SCIP

### Pattern: HiGHS via highspy

The lowest-friction high-performance stack: MIT license, one pip package, expression-based
model building, and full access to duals, ranging, and MIP statistics. The pythonic API below
suits small/medium models; very large models should use the array interface (see Pitfall).

```python
import highspy


def solve_production_mix(
    profit: list[float],
    machine_hours: list[list[float]],
    capacity: list[float],
    max_lots: list[int],
) -> dict[str, object]:
    """Solve an integer production-mix model with HiGHS via highspy."""
    h = highspy.Highs()
    h.silent()  # call before anything that logs
    n = len(profit)
    x = [h.addIntegral(lb=0, ub=max_lots[j], name=f"x{j}") for j in range(n)]
    for i, row in enumerate(machine_hours):
        h.addConstr(sum(row[j] * x[j] for j in range(n)) <= capacity[i], name=f"cap{i}")
    h.setOptionValue("time_limit", 60.0)
    h.setOptionValue("mip_rel_gap", 1e-6)
    h.maximize(sum(profit[j] * x[j] for j in range(n)))  # sets objective AND solves
    status = h.getModelStatus()
    if status != highspy.HighsModelStatus.kOptimal:
        raise RuntimeError(f"HiGHS status: {h.modelStatusToString(status)}")
    sol = h.getSolution()
    info = h.getInfo()
    return {
        "objective": info.objective_function_value,
        "x": [round(sol.col_value[j]) for j in range(n)],
        "mip_gap": info.mip_gap,
        "nodes": info.mip_node_count,
    }


profit = [12.0, 9.0, 15.0]
hours = [[2.0, 1.0, 3.0], [1.0, 2.0, 2.0]]
result = solve_production_mix(profit, hours, capacity=[10.0, 8.0], max_lots=[4, 4, 4])
print(result)
# Expected: objective 66.0 with x = [4, 2, 0]; both machine capacities tight.
```

**Pitfall:** `h.maximize(expr)` both sets the objective and runs the solve — calling `h.run()`
afterwards solves a second time. Building row by row through Python expressions is O(model) in
interpreter time; above roughly 10^5 nonzeros, assemble column-start/index/value arrays and call
`h.passModel` instead, or build with `scipy.sparse` and use the scipy interface. On a time-limit
exit the status is `kTimeLimit`, not an error: check `info.primal_solution_status` before
trusting `col_value`, and report `info.mip_dual_bound` with the incumbent.

### Pattern: matrix-form MILP with scipy.optimize.milp

When the model is already matrices (A, b, c), `scipy.optimize.milp` calls HiGHS with no
modeling-object overhead at all. Ideal for vectorized pipelines and teaching; deliberately
minimal otherwise.

```python
import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp


def solve_binary_milp(
    c: np.ndarray, a_ub: np.ndarray, b_ub: np.ndarray, time_limit: float = 60.0
) -> tuple[np.ndarray, float]:
    """Maximize c @ x over binary x subject to a_ub @ x <= b_ub (HiGHS backend)."""
    n = c.size
    res = milp(
        c=-c,  # scipy minimizes; negate to maximize
        constraints=LinearConstraint(a_ub, ub=b_ub),
        integrality=np.ones(n),
        bounds=Bounds(np.zeros(n), np.ones(n)),
        options={"time_limit": time_limit, "mip_rel_gap": 1e-6, "disp": False},
    )
    if res.status != 0:  # 0 optimal, 1 limit reached, 2 infeasible, 3 unbounded
        raise RuntimeError(f"milp failed (status {res.status}): {res.message}")
    x = np.round(res.x).astype(int)
    return x, float(-res.fun)


rng = np.random.default_rng(7)
values = rng.integers(5, 30, size=8).astype(float)
weights = rng.integers(1, 10, size=(2, 8)).astype(float)
caps = weights.sum(axis=1) * 0.4
x_opt, best = solve_binary_milp(values, weights, caps)
assert np.all(weights @ x_opt <= caps + 1e-9)
print(x_opt, best)
# Expected: a feasible 0-1 vector with objective values[x_opt == 1].sum(); both
# knapsack rows of weights @ x_opt are within caps.
```

**Pitfall:** `milp` is one-shot. No variable names, no warm starts, no callbacks, no
incremental re-solve, and no duals for MIPs (only `res.mip_dual_bound`). Equality constraints
are encoded as `LinearConstraint(A, lb=b, ub=b)`; mixing several constraint blocks means
passing a sequence of `LinearConstraint` objects whose column order must all match `c` exactly
— a silent source of wrong models when columns are reordered upstream.

### Pattern: SCIP via PySCIPOpt

SCIP is the open solver closest to Gurobi in capability: constraint handlers, custom branching
rules, separators, event handlers, and nonconvex MINLP. The imperative API maps almost
one-to-one from gurobipy (see the migration section).

```python
from pyscipopt import Model, quicksum


def solve_set_cover(
    costs: list[float], covers: list[set[int]], n_elements: int
) -> tuple[list[int], float]:
    """Solve min-cost set covering with SCIP via PySCIPOpt."""
    m = Model("setcover")
    m.hideOutput()
    n = len(costs)
    x = [m.addVar(vtype="B", name=f"x{j}") for j in range(n)]
    for e in range(n_elements):
        m.addCons(
            quicksum(x[j] for j in range(n) if e in covers[j]) >= 1, name=f"cover_{e}"
        )
    m.setObjective(quicksum(costs[j] * x[j] for j in range(n)), sense="minimize")
    m.setParam("limits/time", 60)
    m.setParam("limits/gap", 0.0)
    m.optimize()
    if m.getStatus() != "optimal":
        raise RuntimeError(f"SCIP status {m.getStatus()}, dual bound {m.getDualbound():.4f}")
    chosen = [j for j in range(n) if m.getVal(x[j]) > 0.5]
    return chosen, m.getObjVal()


costs = [3.0, 2.0, 4.0, 3.0, 2.0]
covers = [{0, 1, 2}, {0, 3}, {1, 2, 3, 4}, {2, 4}, {3, 4}]
chosen, total = solve_set_cover(costs, covers, n_elements=5)
print(chosen, total)
# Expected: chosen = [0, 4] with total cost 5.0 (sets {0,1,2} and {3,4} cover everything).
```

**Pitfall:** SCIP statuses are plain strings (`"optimal"`, `"timelimit"`, `"infeasible"`), not
enums — typos in comparisons fail silently. After `optimize()` the model is *transformed*; any
modification (adding a constraint, changing a bound) requires `m.freeTransform()` first or
PySCIPOpt raises. Parameters are hierarchical path strings (`"limits/time"`, not `TimeLimit`);
use `m.setEmphasis` / preset `.set` files rather than guessing names. Like all MIP solvers,
binary values return as 0.9999999 within `numerics/feastol = 1e-6` — threshold with `> 0.5`,
never `== 1`.

## Modeling Layers: PuLP, Pyomo, python-mip

### Pattern: PuLP with a swappable backend

PuLP is the lightest modeling layer: pure Python, MIT license, CBC bundled so models solve out
of the box. Its key feature is naming the backend at solve time, so the same code runs on CBC
today and HiGHS or Gurobi tomorrow.

```python
import pulp


def solve_transport(
    supply: list[float],
    demand: list[float],
    cost: list[list[float]],
    solver_name: str = "PULP_CBC_CMD",
) -> tuple[dict[tuple[int, int], float], float]:
    """Solve a transportation LP with PuLP; backend chosen by name at call time."""
    m, n = len(supply), len(demand)
    prob = pulp.LpProblem("transport", pulp.LpMinimize)
    keys = [(i, j) for i in range(m) for j in range(n)]
    x = pulp.LpVariable.dicts("x", keys, lowBound=0)
    prob += pulp.lpSum(cost[i][j] * x[i, j] for i, j in keys)
    for i in range(m):
        prob += pulp.lpSum(x[i, j] for j in range(n)) <= supply[i], f"supply_{i}"
    for j in range(n):
        prob += pulp.lpSum(x[i, j] for i in range(m)) >= demand[j], f"demand_{j}"
    solver = pulp.getSolver(solver_name, msg=False, timeLimit=60)
    prob.solve(solver)
    if pulp.LpStatus[prob.status] != "Optimal":
        raise RuntimeError(f"PuLP status: {pulp.LpStatus[prob.status]}")
    flows = {(i, j): x[i, j].value() for i, j in keys if x[i, j].value() > 1e-9}
    return flows, pulp.value(prob.objective)


supply = [20.0, 30.0]
demand = [15.0, 25.0, 10.0]
cost = [[4.0, 6.0, 9.0], [5.0, 4.0, 7.0]]
flows, total = solve_transport(supply, demand, cost)
print(flows, total)
# Expected: total cost 240.0 with x[0,0]=15, x[0,2]=5, x[1,1]=25, x[1,2]=5.
```

**Pitfall:** most PuLP backends are `*_CMD` solvers: PuLP writes an LP/MPS file to a temp
directory, shells out to a solver binary, and parses the solution file back. That round-trip
costs 0.1-1 s per solve regardless of model size — harmless for one solve, fatal inside a loop
calling the solver thousands of times. Run `pulp.listSolvers(onlyAvailable=True)` to see what
is actually installed; a request for an absent solver raises only at solve time. Variable and
constraint names are sanitized for the file format, so illegal characters get silently mangled
— keep names alphanumeric with underscores.

### Pattern: Pyomo with dual extraction

Pyomo (Hart et al. (2017), "Pyomo — Optimization Modeling in Python") is the heavyweight
layer: sets, parameters, blocks, NLP/MINLP support, and suffixes for duals and reduced costs.
The price is the slowest model build of all the stacks here. Use it for structured projects
and when sensitivity information from open LP solvers matters.

```python
import pyomo.environ as pyo


def solve_diet_lp(
    cost: dict[str, float],
    nutrient: dict[tuple[str, str], float],
    requirement: dict[str, float],
    solver: str = "highs",
) -> tuple[dict[str, float], dict[str, float], float]:
    """Solve a diet LP in Pyomo; return primal solution, constraint duals, objective."""
    foods = sorted(cost)
    nutrients = sorted(requirement)
    model = pyo.ConcreteModel()
    model.x = pyo.Var(foods, domain=pyo.NonNegativeReals)
    model.obj = pyo.Objective(
        expr=sum(cost[f] * model.x[f] for f in foods), sense=pyo.minimize
    )

    def meet_rule(m: pyo.ConcreteModel, nut: str) -> object:
        """Nutrient requirement row."""
        return sum(nutrient[f, nut] * m.x[f] for f in foods) >= requirement[nut]

    model.meet = pyo.Constraint(nutrients, rule=meet_rule)
    model.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)  # declare BEFORE solving
    result = pyo.SolverFactory(solver).solve(model, tee=False)
    pyo.assert_optimal_termination(result)
    primal = {f: pyo.value(model.x[f]) for f in foods}
    duals = {nut: model.dual[model.meet[nut]] for nut in nutrients}
    return primal, duals, pyo.value(model.obj)


cost = {"milk": 3.0, "oats": 2.0}
nutrient = {
    ("oats", "protein"): 4.0, ("oats", "iron"): 2.0,
    ("milk", "protein"): 8.0, ("milk", "iron"): 1.0,
}
requirement = {"protein": 16.0, "iron": 5.0}
primal, duals, total = solve_diet_lp(cost, nutrient, requirement)
print(primal, duals, total)
# Expected: oats = 2.0, milk = 1.0, cost 7.0; both duals equal 1/3 (each
# requirement is binding and priced).
```

**Pitfall:** the dual `Suffix` must exist before the solve, and only some interfaces export
duals — `SolverFactory("highs")` (the appsi interface over highspy) and `"cbc"` (needs the
`cbc` binary on PATH) do for LPs; for MIPs no solver returns duals because none exist. Reading
`pyo.value` on a variable when the solve failed raises a confusing "no value" error — always
gate on `assert_optimal_termination` or inspect
`result.solver.termination_condition`. For repeated solves, rebuild cost dominates: use the
persistent/appsi interfaces, which keep the model in solver memory and accept incremental
updates.

### Pattern: python-mip with a MIP start

python-mip (Santos & Toffolo (2020)) bundles CBC via cffi, so model build is C-fast and there
is no file round-trip. It is the best route to CBC for matheuristics, and it supports MIP
starts and cut/lazy-constraint generators on CBC — features PuLP does not expose.

```python
from mip import BINARY, Model, OptimizationStatus, maximize, xsum


def solve_gap(
    profit: list[list[float]],
    weight: list[list[float]],
    capacity: list[float],
    start: list[int] | None = None,
    max_seconds: float = 60.0,
) -> tuple[list[int], float]:
    """Solve the generalized assignment problem with CBC through python-mip."""
    n_agents, n_jobs = len(profit), len(profit[0])
    m = Model(solver_name="CBC")
    m.verbose = 0
    x = [
        [m.add_var(var_type=BINARY, name=f"x_{i}_{j}") for j in range(n_jobs)]
        for i in range(n_agents)
    ]
    for j in range(n_jobs):
        m += xsum(x[i][j] for i in range(n_agents)) == 1, f"assign_{j}"
    for i in range(n_agents):
        m += xsum(weight[i][j] * x[i][j] for j in range(n_jobs)) <= capacity[i], f"cap_{i}"
    m.objective = maximize(
        xsum(profit[i][j] * x[i][j] for i in range(n_agents) for j in range(n_jobs))
    )
    if start is not None:  # warm start from a heuristic assignment job -> agent
        m.start = [(x[start[j]][j], 1.0) for j in range(n_jobs)]
    m.max_mip_gap = 1e-6
    status = m.optimize(max_seconds=max_seconds)
    if status not in (OptimizationStatus.OPTIMAL, OptimizationStatus.FEASIBLE):
        raise RuntimeError(f"CBC status: {status}")
    assign = [
        next(i for i in range(n_agents) if x[i][j].x > 0.5) for j in range(n_jobs)
    ]
    return assign, m.objective_value


profit = [[9.0, 2.0, 8.0], [6.0, 7.0, 4.0]]
weight = [[3.0, 1.0, 4.0], [2.0, 3.0, 2.0]]
capacity = [7.0, 5.0]
assign, best = solve_gap(profit, weight, capacity, start=[1, 1, 0])
print(assign, best)
# Expected: assign = [0, 1, 0] with profit 24.0 (agent 0 carries jobs 0 and 2,
# load 7 <= 7; agent 1 carries job 1, load 3 <= 5).
```

**Pitfall:** `var.x` is `None` whenever no incumbent exists — reading it after an
`INFEASIBLE` or empty `NO_SOLUTION_FOUND` status throws `TypeError` deep in user code, so gate
on status first. A MIP start that CBC cannot complete to a feasible solution is silently
dropped (only a log line mentions it); validate starts with your own feasibility checker
before passing them. `m.optimize(max_seconds=...)` returning `FEASIBLE` means the time limit
hit — report `m.gap` and `m.objective_bound` alongside the incumbent, never just the objective.

## OR-Tools: CP-SAT and MathOpt

### Pattern: CP-SAT for integer combinatorial structure

CP-SAT is a lazy-clause-generation solver over integers. On models dominated by logical,
disjunctive, or scheduling structure it routinely outperforms MIP solvers — commercial ones
included. Model it natively (no big-M needed); see **constraint-programming** for interval
variables, `NoOverlap`, and `Cumulative`.

```python
from ortools.sat.python import cp_model


def solve_pmachines_makespan(
    durations: list[int], n_machines: int, time_limit_s: float = 30.0
) -> tuple[list[int], int]:
    """Minimize makespan on identical parallel machines with CP-SAT."""
    model = cp_model.CpModel()
    n = len(durations)
    horizon = sum(durations)
    assign = [
        [model.new_bool_var(f"a_{j}_{k}") for k in range(n_machines)] for j in range(n)
    ]
    load = [model.new_int_var(0, horizon, f"load_{k}") for k in range(n_machines)]
    makespan = model.new_int_var(0, horizon, "makespan")
    for j in range(n):
        model.add_exactly_one(assign[j])
    for k in range(n_machines):
        model.add(load[k] == sum(durations[j] * assign[j][k] for j in range(n)))
        model.add(load[k] <= makespan)
    for k in range(n_machines - 1):  # symmetry breaking: order machine loads
        model.add(load[k] >= load[k + 1])
    model.minimize(makespan)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit_s
    solver.parameters.num_workers = 8  # parallel portfolio is CP-SAT's main lever
    status = solver.solve(model)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        raise RuntimeError(solver.status_name(status))
    machine_of = [
        next(k for k in range(n_machines) if solver.value(assign[j][k])) for j in range(n)
    ]
    return machine_of, int(solver.value(makespan))


durations = [7, 5, 4, 3, 3, 2]
machine_of, cmax = solve_pmachines_makespan(durations, n_machines=2)
print(machine_of, cmax)
# Expected: makespan 12 — total work 24 splits evenly, e.g. {7, 5} vs {4, 3, 3, 2}.
```

**Pitfall:** CP-SAT accepts only integer coefficients and bounds. Float costs must be scaled
(e.g., cents instead of euros) and rounded; the scale factor becomes your effective optimality
tolerance, and inconsistent scaling between constraint and objective silently changes the
problem. Keep domains tight — a horizon of `sum(durations)` instead of `10**9` can change
solve time by orders of magnitude. `FEASIBLE` means the time limit hit with an incumbent:
report `solver.best_objective_bound` with the value, exactly as you would report a MIP gap.

### Pattern: MathOpt as a solver-portable MIP API

MathOpt (in `ortools.math_opt`) is a modern, typed, solver-agnostic model API. One model
object solves with HiGHS, SCIP (GSCIP), GLOP, CP-SAT, or a licensed Gurobi — the solver is a
function argument, which makes cross-solver experiments one-line cheap.

```python
import datetime

from ortools.math_opt.python import mathopt


def solve_knapsack_mathopt(
    values: list[float],
    weights: list[float],
    capacity: float,
    solver: mathopt.SolverType = mathopt.SolverType.HIGHS,
) -> tuple[list[int], float]:
    """Solve a 0-1 knapsack with OR-Tools MathOpt; swap solvers via the enum."""
    model = mathopt.Model(name="knapsack")
    x = [model.add_binary_variable(name=f"x{j}") for j in range(len(values))]
    model.add_linear_constraint(
        sum(w * xj for w, xj in zip(weights, x)) <= capacity, name="cap"
    )
    model.maximize(sum(v * xj for v, xj in zip(values, x)))
    params = mathopt.SolveParameters(
        time_limit=datetime.timedelta(seconds=60), relative_gap_tolerance=1e-6
    )
    result = mathopt.solve(model, solver, params=params)
    if result.termination.reason != mathopt.TerminationReason.OPTIMAL:
        raise RuntimeError(f"termination: {result.termination}")
    sol = result.variable_values()
    return [int(round(sol[xj])) for xj in x], result.objective_value()


values = [10.0, 13.0, 7.0, 11.0]
weights = [4.0, 6.0, 3.0, 5.0]
take, best = solve_knapsack_mathopt(values, weights, capacity=10.0)
print(take, best)
# Expected: take = [1, 1, 0, 0] with value 23.0 (weight exactly 10).
# The same call with solver=mathopt.SolverType.GSCIP returns the same optimum.
```

**Pitfall:** `time_limit` must be a `datetime.timedelta`, not a float — passing seconds raises
a type error only at solve time. Available `SolverType` values depend on the OR-Tools build
(`GUROBI` needs a licensed local Gurobi). When a limit stops the solve, the termination reason
is `FEASIBLE` with a populated `result.termination.limit`; code that accepts only `OPTIMAL`
(like the function above) will reject usable incumbents under time limits — relax the check
deliberately, not by accident. Solving CP_SAT through MathOpt inherits the integrality
restriction on coefficients.

## Migrating from gurobipy

Most migrations are mechanical: the imperative model-building style of gurobipy (see
**milp-modeling-gurobi**) maps almost one-to-one onto PySCIPOpt and python-mip. Translate with
this table, then verify objective parity on small instances.

| Concept | gurobipy | PySCIPOpt | python-mip |
|---|---|---|---|
| Model | `gp.Model("m")` | `Model("m")` | `Model(solver_name="CBC")` |
| Silence log | `Params.OutputFlag = 0` | `hideOutput()` | `verbose = 0` |
| Binary var | `addVar(vtype=GRB.BINARY)` | `addVar(vtype="B")` | `add_var(var_type=BINARY)` |
| Constraint | `addConstr(e <= b, name)` | `addCons(e <= b, name=...)` | `m += e <= b, name` |
| Sum | `gp.quicksum(...)` | `quicksum(...)` | `xsum(...)` |
| Objective | `setObjective(e, GRB.MAXIMIZE)` | `setObjective(e, sense="maximize")` | `objective = maximize(e)` |
| Time limit | `Params.TimeLimit = 60` | `setParam("limits/time", 60)` | `optimize(max_seconds=60)` |
| Gap limit | `Params.MIPGap` | `setParam("limits/gap", g)` | `max_mip_gap = g` |
| Optimality test | `Status == GRB.OPTIMAL` | `getStatus() == "optimal"` | `status == OptimizationStatus.OPTIMAL` |
| Value / objective | `v.X` / `m.ObjVal` | `getVal(v)` / `getObjVal()` | `v.x` / `objective_value` |
| Bound / gap | `ObjBound` / `MIPGap` | `getDualbound()` / `getGap()` | `objective_bound` / `gap` |
| MIP start | `v.Start = 1` | `createPartialSol` + `setSolVal` | `m.start = [(v, 1.0)]` |
| Lazy constraints | callback `cbLazy` | constraint handler (conshdlr) | `lazy_constrs_generator` |
| Write model | `m.write("m.mps")` | `writeProblem("m.mps")` | `m.write("m.mps")` |

### Pattern: side-by-side parity check

Migrate one model, keep both implementations temporarily, and assert objective parity on a
small instance suite before deleting the gurobipy version.

```python
import gurobipy as gp
from gurobipy import GRB
from pyscipopt import Model as ScipModel
from pyscipopt import quicksum as scip_sum


def gap_gurobi(profit: list[list[float]], weight: list[list[float]], cap: list[float]) -> float:
    """Reference gurobipy implementation of the generalized assignment problem."""
    n_a, n_j = len(profit), len(profit[0])
    m = gp.Model("gap")
    m.Params.OutputFlag = 0
    m.Params.TimeLimit = 60
    x = m.addVars(n_a, n_j, vtype=GRB.BINARY, name="x")
    m.addConstrs((x.sum("*", j) == 1 for j in range(n_j)), name="assign")
    m.addConstrs(
        (gp.quicksum(weight[i][j] * x[i, j] for j in range(n_j)) <= cap[i] for i in range(n_a)),
        name="cap",
    )
    m.setObjective(
        gp.quicksum(profit[i][j] * x[i, j] for i in range(n_a) for j in range(n_j)),
        GRB.MAXIMIZE,
    )
    m.optimize()
    assert m.Status == GRB.OPTIMAL
    return m.ObjVal


def gap_scip(profit: list[list[float]], weight: list[list[float]], cap: list[float]) -> float:
    """Line-for-line SCIP translation of gap_gurobi using the idiom table."""
    n_a, n_j = len(profit), len(profit[0])
    m = ScipModel("gap")
    m.hideOutput()                                # Params.OutputFlag = 0
    m.setParam("limits/time", 60)                 # Params.TimeLimit = 60
    x = {
        (i, j): m.addVar(vtype="B", name=f"x_{i}_{j}")
        for i in range(n_a) for j in range(n_j)
    }
    for j in range(n_j):                          # addConstrs generator -> explicit loop
        m.addCons(scip_sum(x[i, j] for i in range(n_a)) == 1, name=f"assign_{j}")
    for i in range(n_a):
        m.addCons(
            scip_sum(weight[i][j] * x[i, j] for j in range(n_j)) <= cap[i], name=f"cap_{i}"
        )
    m.setObjective(
        scip_sum(profit[i][j] * x[i, j] for i in range(n_a) for j in range(n_j)),
        sense="maximize",
    )
    m.optimize()
    assert m.getStatus() == "optimal"             # Status == GRB.OPTIMAL
    return m.getObjVal()                          # ObjVal


profit = [[9.0, 2.0, 8.0], [6.0, 7.0, 4.0]]
weight = [[3.0, 1.0, 4.0], [2.0, 3.0, 2.0]]
cap = [7.0, 5.0]
print(gap_gurobi(profit, weight, cap), gap_scip(profit, weight, cap))
# Expected: both print 24.0 — identical optimum from both stacks.
```

**Pitfall:** "objective parity" must respect tolerances. Two solvers reporting 1043.18 and
1043.21 may both be correct under their default relative gaps (Gurobi `MIPGap = 1e-4`, SCIP
`limits/gap = 0`, CBC `allowableGap` defaults differ) — compare against bounds, or tighten gaps
to 1e-6 for the parity tests only. Features without counterparts are the real migration cost:
Gurobi's solution pool, IIS, multi-objective API, and `cbLazy` one-liners need redesign (SCIP
constraint handlers are powerful but a different programming model; CBC lazy constraints exist
only through python-mip generators). Inventory those features *before* promising a timeline.

## Advanced Techniques

### Warm starts across stacks

Every open stack accepts initial solutions, with different ergonomics: python-mip
`m.start = [(var, val), ...]`; CP-SAT `model.add_hint(var, val)` per variable; PySCIPOpt
`s = m.createPartialSol()` then `m.setSolVal(s, var, val)`; highspy `h.setSolution` on a
`HighsSolution` object; PuLP forwards `warmStart=True` for some backends only. The payoff
profile mirrors Gurobi: strong incumbents prune the tree early and matter most when the solver
struggles to find feasibility on its own. Always check the log confirms acceptance — every
stack silently discards inconsistent starts.

### Extracting duals and reduced costs

For LPs: highspy exposes `getSolution().row_dual` and `.col_dual`; scipy's `linprog` returns
marginals in `res.ineqlin` / `res.eqlin`; Pyomo imports them through `Suffix` (pattern above);
PuLP exposes `constraint.pi` and `variable.dj` after a CBC solve. SCIP is the trap: it is a
branch-and-bound code first, and clean LP duals require solving as an LP (disable presolve and
heuristics, or use `m.optimize()` on a model with no integer variables and read
`m.getDualSolVal` per constraint). If sensitivity analysis is the deliverable, prefer HiGHS,
whose ranging information is a first-class API, and validate degenerate duals against a
re-solve with perturbed right-hand sides.

### Tuning open-source solvers

Tuning moves less than formulation strength, but the levers worth knowing: SCIP —
`setEmphasis(SCIP_PARAMEMPHASIS.FEASIBILITY)` or `OPTIMALITY`, `"limits/gap"`, aggressive
presolve settings; HiGHS — `"presolve"`, `"parallel"`, `"mip_heuristic_effort"` (0-1),
`"mip_rel_gap"`; CP-SAT — `num_workers` dominates everything (the parallel portfolio is the
engine), then `max_time_in_seconds` and `log_search_progress` for diagnosis; CBC — cut and
heuristic flags exist via python-mip's `m.emphasis`, with modest expectations. There is no
open equivalent of Gurobi's automated tuning tool, so tune like a metaheuristic experiment:
fixed instance set, fixed seeds, one parameter at a time, shifted-geometric-mean runtime.

### File-based interoperability

Every solver here reads MPS and LP formats, which makes files the universal escape hatch:
build once, `write("model.mps")`, and solve with any binary (`highs model.mps`,
`scip -f model.mps`, `cbc model.mps`). Use this for (a) reproducing a bug in a solver-neutral
artifact, (b) sending instances to colleagues without your Python stack, and (c) archiving the
exact models behind published tables. Beware: LP format truncates names and loses some
precision; prefer MPS (or the gzipped variant) for archival. Free-form MPS handling of ranges
and objective constants differs subtly across readers — round-trip and re-check the objective
after import.

### Cross-solver benchmarking harness

When a paper or a deployment decision needs evidence, run the same models across solvers under
identical limits and report status, objective, bound, and time per run — one tidy row each
(then analyze as in **optimization-project-structure** conventions).

```python
import datetime
from collections.abc import Callable

import pandas as pd
from ortools.math_opt.python import mathopt


def benchmark_solvers(
    build: Callable[[dict], mathopt.Model],
    instances: dict[str, dict],
    solvers: list[mathopt.SolverType],
    time_limit_s: float = 60.0,
) -> pd.DataFrame:
    """Solve every instance with every solver; one tidy row per (instance, solver)."""
    params = mathopt.SolveParameters(time_limit=datetime.timedelta(seconds=time_limit_s))
    rows: list[dict[str, object]] = []
    for name, data in instances.items():
        model = build(data)
        for solver in solvers:
            result = mathopt.solve(model, solver, params=params)
            ok = result.termination.reason in (
                mathopt.TerminationReason.OPTIMAL,
                mathopt.TerminationReason.FEASIBLE,
            )
            rows.append({
                "instance": name,
                "solver": solver.name,
                "status": result.termination.reason.name,
                "objective": result.objective_value() if ok else None,
                "bound": result.best_objective_bound() if ok else None,
                "time_s": result.solve_time().total_seconds(),
            })
    return pd.DataFrame(rows)


def build_knapsack(data: dict) -> mathopt.Model:
    """Build a 0-1 knapsack MathOpt model from an instance dict."""
    model = mathopt.Model(name="kp")
    x = [model.add_binary_variable(name=f"x{j}") for j in range(len(data["v"]))]
    model.add_linear_constraint(sum(w * xj for w, xj in zip(data["w"], x)) <= data["cap"])
    model.maximize(sum(v * xj for v, xj in zip(data["v"], x)))
    return model


instances = {"toy": {"v": [10.0, 13.0, 7.0], "w": [4.0, 6.0, 3.0], "cap": 9.0}}
df = benchmark_solvers(
    build_knapsack, instances, [mathopt.SolverType.HIGHS, mathopt.SolverType.GSCIP]
)
print(df)
# Expected: two rows, both status OPTIMAL with objective 20.0 (items 1 and 2:
# weight 9, value 20), differing only in time_s.
```

## Practical Challenges

**Two solvers report different "optimal" objectives on the same model.** Almost always
tolerance semantics, not a bug: each solver stops when its *relative gap* falls under its own
default, and integer feasibility tolerances differ (1e-5 vs 1e-6). Tighten gaps to 1e-9 on a
small instance, compare best bound against best objective across solvers, and run an
independent feasibility/objective validator on both solutions. If a genuinely infeasible
solution passes a solver, check for big-M values poisoning numerics.

**CBC needs hours on a model Gurobi solved in seconds.** Expected behavior on hard MIPs, not a
configuration error. In order of leverage: tighten the formulation (stronger LP relaxation
beats any solver switch), move to HiGHS or SCIP, feed a heuristic warm start, decompose, or
accept a time-limited gap and report bounds. Only then consider parameter tuning, which
rarely buys more than 2× on CBC.

**A tiny MIP inside a loop is slow under PuLP.** The model solves in milliseconds; the LP-file
write, process spawn, and solution-file parse cost a second. Switch to an in-memory API
(python-mip, highspy, PySCIPOpt) for anything called repeatedly — matheuristic loops see
100× wall-clock improvements from this change alone.

**CP-SAT seems to reject the model's float data.** It does, by design. Scale costs and
coefficients to integers (cents, grams, seconds) and document the scale factor next to the
model. Check that constraint and objective use the same scale, and that the scaled magnitudes
stay well below 2^62 after products with domain bounds.

**No duals come out of the MIP.** MIPs have no duals — that is mathematics, not a missing
feature. For prices, fix all integer variables at their optimal values, re-solve the remaining
LP, and read its duals (interpret with care: they price resources *given* the discrete
decisions). For sensitivity to RHS changes, re-solve with perturbed data; MIP value functions
are not differentiable.

**Pyomo's dual suffix comes back empty.** Three causes in practice: the `Suffix` was declared
after `solve()`; the chosen interface does not export duals (several CMD-style plugins drop
them); or the model is a MIP. Declare the suffix at build time, use the appsi/persistent
interfaces, and test dual extraction on a 3-variable LP before relying on it in a pipeline.

**Results change after moving between machines.** Different solver versions and threading make
runs non-reproducible. Pin exact versions (`highspy==…` in a lock file), set deterministic
options (`random_seed`, fixed thread counts; CP-SAT with `num_workers > 1` is a portfolio and
only seed-deterministic for a fixed worker count and version), and record solver name +
version + options in every result row.

**The system solver shadows the pip-installed one.** HPC modules and OS packages ship old
`cbc`/`glpsol` binaries on PATH; PuLP and Pyomo CMD interfaces may pick those instead of the
bundled or pip versions. Log the resolved executable path and version at startup; in Pyomo,
pass `executable=` explicitly to `SolverFactory` when in doubt.

**Choosing between a free academic Gurobi and an open solver for a paper.** Use both
deliberately: develop and debug on the open stack so any reader can reproduce the pipeline,
and report commercial-solver results separately if performance claims depend on them. State
solver versions and parameter files in the paper; "CBC could not solve X" is publishable only
with the version, limits, and gap at termination.

**Model build itself becomes the bottleneck at scale.** Object-per-constraint layers (Pyomo,
PuLP) spend minutes building what HiGHS solves in seconds. Restructure to array form: build
coefficient matrices with numpy/scipy.sparse and use `scipy.optimize.milp` or highspy's
`passModel`; or at least batch construction (gurobipy-style `addVars`-equivalents, python-mip
lists) instead of one Python call per scalar entry.

## Tools & Libraries

| Library | Use when | Note |
|---|---|---|
| highspy | Default open LP/MIP, duals, in-memory re-solves | MIT; `pip install highspy`; array API for big models |
| scipy.optimize (`milp`, `linprog`) | Matrix-form models, zero extra dependencies | HiGHS backend; one-shot, no warm starts or callbacks |
| PySCIPOpt | Callbacks, custom branching, MINLP, solver research | Apache 2.0 since SCIP 8.0.3; richest plugin system |
| python-mip | CBC with fast builds, MIP starts, cut generators | EPL-2.0; CBC bundled; best CBC route for loops |
| ortools (CP-SAT) | Integer feasibility-heavy combinatorics, scheduling | Apache 2.0; integer coefficients only; `num_workers` |
| ortools (MathOpt) | Solver-portable models, cross-solver benchmarks | One enum swaps HiGHS/GSCIP/GLOP/CP-SAT/Gurobi |
| PuLP | Quick one-off models, teaching, prototypes | MIT; CMD file round-trip per solve; CBC bundled |
| Pyomo | Large structured projects, NLP/MINLP, suffixes | BSD; heaviest build; persistent interfaces for loops |
| gurobipy (size-limited pip) | Sanity-checking small models against Gurobi | Free install caps ~2000 vars/constraints |
| GLPK / swiglpk | Legacy code only | GPL copyleft; outperformed by HiGHS everywhere |

## Output Format

A complete solver-selection or migration deliverable contains:

**Solver selection checklist:**

- [ ] Problem class identified (LP / MILP / MINLP / CP) and size estimated (vars, cons, nnz).
- [ ] Must-have features listed (duals, callbacks, MIP starts, pools) and mapped to stacks.
- [ ] License compatibility confirmed for the deployment (MIT/Apache/BSD/EPL vs GPL).
- [ ] Solve pattern classified: one-shot vs in-loop; file-based interfaces excluded for loops.
- [ ] Candidate stack benchmarked on 3-5 representative instances with fixed time limits.
- [ ] Status handling covers OPTIMAL, limit-with-incumbent, INFEASIBLE, UNBOUNDED.

**Migration checklist (gurobipy → open stack):**

- [ ] Feature inventory done: callbacks, IIS, pools, multi-objective flagged for redesign.
- [ ] Idiom table applied; constraint names preserved for debugging.
- [ ] Parity suite: both implementations agree on objective (gap ≤ 1e-6) on small instances.
- [ ] Independent validator re-checks feasibility and objective of migrated solutions.
- [ ] Tolerances aligned (`mip_rel_gap`, feasibility tolerance) and documented.
- [ ] gurobipy implementation deleted after parity holds (one-versioned codebase).

**Run-report template** (one per solve, machine-readable next to results):

```yaml
run_report:
  model: gap_n50_m10_seed3
  solver: {name: HiGHS, version: 1.7.2, interface: highspy}
  options: {time_limit: 600, mip_rel_gap: 1.0e-4, threads: 8, random_seed: 0}
  termination: {status: TIME_LIMIT, incumbent: true}
  objective: 10432.0
  best_bound: 10391.5
  gap: 0.0039
  wall_time_s: 600.2
  environment: {python: 3.12.4, os: linux-x86_64, pinned_in: requirements.lock}
```

Reports comparing solvers additionally include a tidy results table (instance × solver rows
with status/objective/bound/time) and shifted-geometric-mean runtimes per solver.

## Questions to Ask

- Why is Gurobi unavailable — cost, deployment licensing, or reproducibility? Could a free
  academic or size-limited license cover this case?
- What problem class and size: LP, MILP, MINLP, or feasibility-heavy integer structure?
- One big solve, or many solves inside a heuristic loop?
- Which solver features are non-negotiable: duals, lazy constraints, MIP starts, pools?
- Does the model's data contain floats that would need scaling for CP-SAT?
- Will the code ship inside a distributed product (license copyleft check)?
- Is there an existing gurobipy codebase to migrate, or is this greenfield?
- What time limit and gap are acceptable at termination, and must optimality be proven?
- Do results feed a publication that requires reproducibility across machines?

## Related Skills

- **milp-modeling-gurobi** — when the user has a Gurobi license and wants the reference
  gurobipy modeling workflow these open stacks are compared against and migrated from.
- **constraint-programming** — when the model is integer feasibility-heavy and CP-SAT
  modeling depth (intervals, NoOverlap, Cumulative, search strategies) is needed.
- **network-flow-optimization** — when the problem is a flow/assignment/shortest-path
  structure that specialized algorithms solve faster than any general MIP solver.
- **optimization-project-structure** — when solver choice must be wired into configs,
  factories, and reproducible experiment pipelines rather than hard-coded.
