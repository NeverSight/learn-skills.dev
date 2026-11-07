---
name: gurobi-advanced-features
description: When the user wants to use Gurobi beyond plain model building — callbacks for lazy constraints, user cuts, heuristic solution injection, and early termination; IIS computation for diagnosing an infeasible model; the solution pool; the multi-objective API; the matrix API (addMVar/addMConstr); MIP starts; and parameter tuning with the built-in tuning tool. Also use when the user mentions "Gurobi callback," "lazy constraints," "IIS," "solution pool," "Gurobi parameters," "infeasible model," or "MIP start." For core model construction, see milp-modeling-gurobi; for cut families and separation theory, see cutting-planes-valid-inequalities.
---

# Gurobi Advanced Features

You are an expert in the advanced layer of the Gurobi Python API: callbacks, infeasibility
diagnosis, solution pools, multi-objective solves, matrix-based model construction, MIP starts,
and parameter tuning. This skill is a pattern catalog. Each pattern gives the motivation, a
complete implementation, and the pitfall that most often breaks it in practice. Use the framework
below to pick the right feature for the symptom, then adapt the matching pattern.

## Initial Assessment

Establish the following before recommending any advanced feature:

- **Symptom first.** Is the problem (a) the formulation needs exponentially many constraints,
  (b) the model is infeasible, (c) the solve is too slow, (d) one optimum is not enough,
  (e) several objectives compete, or (f) model build time dominates solve time? Each maps to a
  different feature; do not reach for callbacks when a parameter fixes it.
- **Gurobi version and license.** Callbacks, IIS, pools, and multi-objective all work on a full
  license. The size-limited (free/pip) license caps model size at 2000 variables / 2000
  constraints; tuning long runs on it is pointless.
- **Model scale.** Variables, constraints, nonzeros. Matrix API pays off above roughly 10^5
  nonzeros of build work; IIS cost grows quickly with model size.
- **Where time goes.** Ask for the log. Split time into model build, root relaxation, cut loop,
  and tree search before touching parameters. `m.printStats()` gives coefficient ranges.
- **Determinism requirements.** Experiments for a paper need fixed `Seed`, fixed `Threads`, and a
  recorded parameter file; interactive use does not.
- **Is the exponential family separable?** Lazy constraints need a separation routine: given a
  candidate solution, find a violated constraint or certify none exists. If separation is itself
  hard, reconsider the formulation.
- **Hard vs soft infeasibility.** If the model is infeasible, decide whether the user needs the
  cause (IIS) or a least-violating solution (feasRelax). These are different deliverables.
- **Incumbent source.** If a good feasible solution exists from a heuristic, plan for a MIP start
  or callback injection before tuning anything else.
- **Time budget for tuning.** The tuning tool needs at least 5-10 solves' worth of wall-clock
  time to say anything; with a 2-hour model, plan tuning as an overnight batch job.

## Feature Map and Decision Guidance

Match the symptom to the feature, not the other way around:

| Symptom | Feature | Pattern below |
|---|---|---|
| Constraint family too large to enumerate | Lazy constraints (`cbLazy`) | Callback 1 |
| Root gap large, valid inequalities known | User cuts (`cbCut`) | Callback 2 |
| Solver struggles to find incumbents | Heuristic injection (`cbSetSolution`) / MIP start | Callback 3, Starts |
| Solve must stop on a custom criterion | `terminate()` in a callback | Callback 4 |
| `Status == GRB.INFEASIBLE` | IIS (`computeIIS`) | Diagnosis 1 |
| Need a least-violation repair | `feasRelax` | Diagnosis 2 |
| Need K best / diverse solutions | Solution pool | Pool |
| Several objectives with priorities | Multi-objective API (`setObjectiveN`) | Multi-objective |
| Model build slower than solve | Matrix API (`addMVar`, `addMConstr`) | Matrix |
| Defaults underperform systematically | Parameter tuning (`tune()`, `grbtune`) | Tuning |

**The lazy-constraint setting, formally.** Many strong formulations have the shape

$$\min \; c^\top x \quad \text{s.t.} \quad x \in P, \qquad a_k^\top x \le b_k \;\; \forall k \in K,$$

where $|K|$ is exponential (subtour elimination over all vertex subsets, Benders cuts over all
dual extreme points). Branch-and-cut handles this with a *separation oracle*: given a candidate
$x^*$, either return some $k \in K$ with $a_k^\top x^* > b_k$, or certify that none exists.
Gurobi exposes the oracle hook through callbacks. The distinction that matters:

- **Lazy constraints** are part of the model definition. Omitting one makes "feasible" solutions
  wrong. They must be checked at every `MIPSOL`. Requires `Params.LazyConstraints = 1`.
- **User cuts** only tighten the LP relaxation. The model is correct without them. They may be
  added at `MIPNODE` and Gurobi is free to discard them. Requires `Params.PreCrush = 1`.

**Callback `where` map.** A callback is a single function `cb(model, where)` passed to
`optimize()`. The `where` code tells you what is legal:

| `where` | Fires when | Can query | Can do |
|---|---|---|---|
| `GRB.Callback.MIPSOL` | New integer-feasible solution | `cbGetSolution`, `MIPSOL_OBJ`, `MIPSOL_OBJBND` | `cbLazy`, `terminate` |
| `GRB.Callback.MIPNODE` | Node explored | `cbGetNodeRel` (only if `MIPNODE_STATUS == GRB.OPTIMAL`), node counts | `cbCut`, `cbLazy`, `cbSetSolution`/`cbUseSolution`, `terminate` |
| `GRB.Callback.MIP` | Periodic tree progress | `MIP_OBJBST`, `MIP_OBJBND`, `MIP_NODCNT`, `RUNTIME` | `terminate` |
| `GRB.Callback.SIMPLEX` / `BARRIER` | Per LP iteration | objective, infeasibilities | `terminate` |
| `GRB.Callback.MESSAGE` | Each log line | `MSG_STRING` | custom logging |
| `GRB.Callback.MULTIOBJ` | Each objective pass | `MULTIOBJ_OBJCNT`, `MULTIOBJ_SOLCNT` | `terminate` (current pass) |

Complexity note: the callback runs inside the branch-and-bound loop, possibly thousands of times.
Keep `MIPNODE` work near O(separation) and avoid Python-level loops over all variables when a
vectorized or incremental check exists. A separation routine that takes 50 ms at every node of a
10^5-node tree adds 80+ minutes.

Decision rules of thumb:

- Use **lazy constraints** when enumeration is impossible; use a full formulation plus solver
  defaults when the family is small (a few thousand constraints enumerate fine).
- Use **user cuts** only with evidence: solve the root, measure the integrality gap, and add cuts
  that demonstrably close part of it. Otherwise let Gurobi's 20+ internal cut families work.
- Prefer a **MIP start** over `cbSetSolution` when the heuristic runs before the solve; use the
  callback only when the heuristic needs node LP information.
- Prefer **parameters** (`BestObjStop`, `BestBdStop`, `MIPGap`, `TimeLimit`, `Cutoff`) over a
  termination callback when the stopping rule is expressible as a threshold.

## Callback Patterns

### Pattern: lazy subtour elimination (branch-and-cut)

The canonical lazy-constraint application, following Padberg & Rinaldi (1991): solve symmetric
TSP with degree constraints only, and add Dantzig-Fulkerson-Johnson subtour cuts when an
integer-feasible candidate contains a short cycle. The same skeleton carries Benders optimality
cuts (see **benders-decomposition**) and any row-generation scheme.

```python
import itertools
import math

import gurobipy as gp
from gurobipy import GRB


def shortest_cycle(edges: list[tuple[int, int]], n: int) -> list[int]:
    """Return the shortest cycle in the graph induced by the selected edges."""
    adj: dict[int, list[int]] = {i: [] for i in range(n)}
    for i, j in edges:
        adj[i].append(j)
        adj[j].append(i)
    unvisited = set(range(n))
    best = list(range(n))
    while unvisited:
        cycle = []
        node = next(iter(unvisited))
        while node in unvisited:
            unvisited.remove(node)
            cycle.append(node)
            node = next((k for k in adj[node] if k in unvisited), cycle[0])
        if len(cycle) < len(best):
            best = cycle
    return best


def solve_tsp_lazy(dist: dict[tuple[int, int], float], n: int) -> tuple[list[int], float]:
    """Solve the symmetric TSP with DFJ subtour cuts added lazily."""
    m = gp.Model("tsp_dfj")
    m.Params.OutputFlag = 0
    m.Params.LazyConstraints = 1  # mandatory before any cbLazy call
    x = m.addVars(dist.keys(), vtype=GRB.BINARY, name="x")
    for i, j in list(dist):
        x[j, i] = x[i, j]  # symmetric access, same variable object
    m.addConstrs((x.sum(i, "*") == 2 for i in range(n)), name="degree")
    m.setObjective(gp.quicksum(dist[e] * x[e] for e in dist), GRB.MINIMIZE)
    m._x, m._edges, m._n = x, list(dist.keys()), n

    def cb(model: gp.Model, where: int) -> None:
        if where != GRB.Callback.MIPSOL:
            return
        vals = model.cbGetSolution(model._x)
        chosen = [e for e in model._edges if vals[e] > 0.5]
        cycle = shortest_cycle(chosen, model._n)
        if len(cycle) < model._n:
            model.cbLazy(
                gp.quicksum(model._x[i, j] for i, j in itertools.combinations(cycle, 2))
                <= len(cycle) - 1
            )

    m.optimize(cb)
    assert m.Status == GRB.OPTIMAL
    tour_edges = [e for e in m._edges if x[e].X > 0.5]
    return shortest_cycle(tour_edges, n), m.ObjVal


# Tiny instance: 6 points on the unit circle; the optimal tour is the circle order.
pts = [(math.cos(2 * math.pi * k / 6), math.sin(2 * math.pi * k / 6)) for k in range(6)]
dist = {(i, j): math.dist(pts[i], pts[j]) for i in range(6) for j in range(i + 1, 6)}
tour, length = solve_tsp_lazy(dist, 6)
print(sorted(tour), round(length, 4))
# Expected: all 6 nodes in one cycle, length 6.0 (six unit-length chords)
```

**Pitfall:** every `MIPSOL` candidate must be checked, including incumbents produced by Gurobi's
own internal heuristics — they have *not* seen your lazy constraints. Skipping the check (for
example, returning early "because the root was already cut") silently returns infeasible
"optimal" tours. Also note `LazyConstraints = 1` disables dual presolve reductions, so expect a
mild slowdown even when no cut is ever added; never leave it on for models without lazy cuts.

### Pattern: user cuts at the root (`cbCut`)

User cuts tighten the relaxation but are optional for correctness. The example separates cover
inequalities for a knapsack constraint with a greedy heuristic (see
**cutting-planes-valid-inequalities** for the cut families and exact separation).

```python
import gurobipy as gp
from gurobipy import GRB


def solve_knapsack_with_cover_cuts(
    profit: list[float], weight: list[float], cap: float
) -> tuple[list[int], float]:
    """0-1 knapsack with greedy cover-cut separation injected at the root node."""
    n = len(profit)
    m = gp.Model("knapsack_cover")
    m.Params.OutputFlag = 0
    m.Params.PreCrush = 1  # required: lets presolve translate user cuts onto the presolved model
    m.Params.Cuts = 0      # silence built-in cuts so the user cuts are attributable in the log
    x = m.addVars(n, vtype=GRB.BINARY, name="x")
    m.addConstr(gp.quicksum(weight[i] * x[i] for i in range(n)) <= cap, name="cap")
    m.setObjective(gp.quicksum(profit[i] * x[i] for i in range(n)), GRB.MAXIMIZE)

    def cb(model: gp.Model, where: int) -> None:
        if where != GRB.Callback.MIPNODE:
            return
        if model.cbGet(GRB.Callback.MIPNODE_STATUS) != GRB.OPTIMAL:
            return  # node relaxation not solved to optimality: cbGetNodeRel would raise
        if model.cbGet(GRB.Callback.MIPNODE_NODCNT) > 0:
            return  # separate at the root only
        xval = model.cbGetNodeRel(x)
        order = sorted(range(n), key=lambda i: -xval[i])
        cover: list[int] = []
        load = 0.0
        for i in order:
            cover.append(i)
            load += weight[i]
            if load > cap:
                break
        if load > cap and sum(xval[i] for i in cover) > len(cover) - 1 + 1e-6:
            model.cbCut(gp.quicksum(x[i] for i in cover) <= len(cover) - 1)

    m.optimize(cb)
    assert m.Status == GRB.OPTIMAL
    return [i for i in range(n) if x[i].X > 0.5], m.ObjVal


items, value = solve_knapsack_with_cover_cuts(
    profit=[10.0, 10.0, 10.0], weight=[4.0, 4.0, 4.0], cap=6.0
)
print(items, value)
# Expected: a single item, value 10.0; root LP is 15.0 and cover cuts (x_i + x_j <= 1) close it
```

**Pitfall:** a user cut must be valid for *every* integer-feasible solution. If your separation
routine has a sign error and cuts off a feasible point, Gurobi will not warn you — it simply
returns a wrong "optimum". Test separation by re-solving without callbacks and comparing
objectives on a batch of small instances. Forgetting `PreCrush = 1` raises a runtime error on
the first `cbCut` call; setting it without using cuts costs presolve strength for nothing.

### Pattern: heuristic solution injection (`cbSetSolution`)

When a problem-specific heuristic can exploit the node LP relaxation (rounding, repair, local
search around the fractional point), inject its output as an incumbent. This is the hook that
**matheuristics** use to combine MIP search with heuristics that run *during* the solve.

```python
import numpy as np
import gurobipy as gp
from gurobipy import GRB


def solve_with_injection(profit: np.ndarray, weight: np.ndarray, cap: float) -> float:
    """Knapsack solve that injects a greedy rounding of the node LP as an incumbent."""
    n = len(profit)
    m = gp.Model("knapsack_inject")
    m.Params.OutputFlag = 0
    m.Params.Heuristics = 0.0  # disable built-ins so injected incumbents are attributable
    x = m.addVars(n, vtype=GRB.BINARY, name="x")
    m.addConstr(gp.quicksum(float(weight[i]) * x[i] for i in range(n)) <= cap, name="cap")
    m.setObjective(gp.quicksum(float(profit[i]) * x[i] for i in range(n)), GRB.MAXIMIZE)
    m._accepted = []

    def cb(model: gp.Model, where: int) -> None:
        if where != GRB.Callback.MIPNODE:
            return
        if model.cbGet(GRB.Callback.MIPNODE_STATUS) != GRB.OPTIMAL:
            return
        rel = model.cbGetNodeRel(x)
        order = sorted(range(n), key=lambda i: -(rel[i] + 1e-9) * profit[i] / weight[i])
        load, plan = 0.0, np.zeros(n)
        for i in order:
            if load + weight[i] <= cap:
                load += weight[i]
                plan[i] = 1.0
        model.cbSetSolution([x[i] for i in range(n)], plan.tolist())
        obj = model.cbUseSolution()  # returns GRB.INFINITY if the vector was rejected
        if obj < GRB.INFINITY:
            model._accepted.append(obj)

    m.optimize(cb)
    assert m.Status == GRB.OPTIMAL
    return m.ObjVal


rng = np.random.default_rng(7)
w = rng.uniform(1.0, 10.0, size=25)
p = w * rng.uniform(0.8, 1.2, size=25)
best = solve_with_injection(p, w, cap=float(w.sum()) * 0.3)
print(round(best, 3))
# Expected: the optimal value; the LP-guided greedy supplies the first incumbent at the root
```

**Pitfall:** `cbSetSolution` is only legal in `MIPNODE`, not in `MIPSOL`. A partial vector
(only some variables set) triggers a completion sub-MIP, which can be slow if called at every
node — either provide complete vectors or rate-limit the injection (for example, only when
`MIPNODE_NODCNT` is a multiple of 100). Call `cbUseSolution()` to get immediate accept/reject
feedback; without it the solution is only applied after the callback returns and you cannot tell
whether it helped.

### Pattern: custom termination

Stop the solve when the incumbent stagnates — a budget rule no built-in parameter expresses.
For plain thresholds prefer `TimeLimit`, `MIPGap`, `BestObjStop`, `BestBdStop`, or `Cutoff`.

```python
from collections.abc import Callable

import numpy as np
import gurobipy as gp
from gurobipy import GRB


def make_stagnation_callback(stall_seconds: float) -> Callable[[gp.Model, int], None]:
    """Stop a minimization solve once the incumbent stops improving for stall_seconds."""

    def cb(model: gp.Model, where: int) -> None:
        if where != GRB.Callback.MIP:
            return
        best = model.cbGet(GRB.Callback.MIP_OBJBST)
        now = model.cbGet(GRB.Callback.RUNTIME)
        if best < model._incumbent - 1e-6 * (1.0 + abs(best)):
            model._incumbent = best
            model._last_improve = now
        elif best < GRB.INFINITY and now - model._last_improve > stall_seconds:
            model.terminate()

    return cb


rng = np.random.default_rng(3)
A = (rng.random((40, 120)) < 0.08).astype(float)
A[np.arange(40), rng.integers(0, 120, size=40)] = 1.0  # guarantee feasibility
cost = rng.uniform(1.0, 5.0, size=120)
m = gp.Model("set_cover_stall")
m.Params.OutputFlag = 0
m._incumbent, m._last_improve = GRB.INFINITY, 0.0
x = m.addVars(120, vtype=GRB.BINARY, name="x")
m.addConstrs(
    (gp.quicksum(A[r, j] * x[j] for j in range(120) if A[r, j] > 0) >= 1 for r in range(40)),
    name="cover",
)
m.setObjective(gp.quicksum(cost[j] * x[j] for j in range(120)), GRB.MINIMIZE)
m.optimize(make_stagnation_callback(stall_seconds=5.0))
usable = m.Status == GRB.OPTIMAL or (m.Status == GRB.INTERRUPTED and m.SolCount > 0)
print(usable, round(m.ObjVal, 2) if m.SolCount > 0 else None)
# Expected: True and a feasible cover cost; this small instance finishes OPTIMAL before stalling
```

**Pitfall:** `terminate()` is a request, not an abort — the solver stops at the next safe point
and returns `Status == GRB.INTERRUPTED`. Always gate attribute reads on `SolCount > 0`; reading
`.X` after an interrupted solve with no incumbent raises an `AttributeError`-style Gurobi error.
The comparison direction above assumes minimization; for maximization flip the improvement test
or read `ModelSense`.

## Infeasibility Diagnosis

### Pattern: IIS — find the conflicting core

An IIS (Irreducible Inconsistent Subsystem) is a subset of constraints and bounds that is
infeasible but becomes feasible if any single member is removed (Chinneck (2008), *Feasibility
and Infeasibility in Optimization*). It turns "model infeasible" into a short, reviewable list.

```python
import gurobipy as gp
from gurobipy import GRB


def diagnose_infeasibility(m: gp.Model) -> tuple[list[str], list[str]]:
    """Compute an IIS; return the constraint names and variable bounds that conflict."""
    m.optimize()
    if m.Status == GRB.INF_OR_UNBD:
        m.Params.DualReductions = 0  # disambiguate INFEASIBLE vs UNBOUNDED
        m.optimize()
    if m.Status != GRB.INFEASIBLE:
        return [], []
    m.computeIIS()
    bad_constrs = [c.ConstrName for c in m.getConstrs() if c.IISConstr]
    bad_bounds = [v.VarName for v in m.getVars() if v.IISLB or v.IISUB]
    m.write("infeasible_core.ilp")  # human-readable IIS file for the report
    return bad_constrs, bad_bounds


m = gp.Model("infeasible_demo")
m.Params.OutputFlag = 0
x = m.addVar(name="x")
y = m.addVar(name="y")
m.addConstr(x + y <= 1, name="budget")
m.addConstr(x >= 1, name="x_min")
m.addConstr(y >= 1, name="y_min")
constrs, bounds = diagnose_infeasibility(m)
print(sorted(constrs), bounds)
# Expected: ['budget', 'x_min', 'y_min'] [] — removing any one of the three restores feasibility
```

**Pitfall:** an IIS is irreducible, not minimum — Gurobi returns *one* small conflicting core,
not the smallest one, and a model can contain several independent conflicts. After fixing the
reported core, re-solve; if still infeasible, compute the next IIS. On large MIPs `computeIIS`
can cost more than the solve: set `IISMethod = 0` for speed (larger IIS) or run the IIS on the
LP relaxation first. Name every constraint at build time, otherwise the IIS output is unreadable
(`R0`, `R1`, ...).

### Pattern: feasRelax — quantify the minimal violation

When the answer to "why infeasible" is "the data is over-constrained and we must ship anyway",
relax constraints with penalties and report the smallest violation that restores feasibility.

```python
import gurobipy as gp
from gurobipy import GRB


def minimal_relaxation(m: gp.Model) -> dict[str, float]:
    """Relax all constraints with unit penalties; return the positive violations by name."""
    relaxed = m.copy()  # feasRelax rewrites the model in place; keep the original intact
    relaxed.Params.OutputFlag = 0
    cons = relaxed.getConstrs()
    # args: relaxobjtype (0 = min weighted sum of violations), minrelax,
    #       vars/lbpen/ubpen (None = keep bounds hard), constrs, rhspen
    relaxed.feasRelax(0, False, None, None, None, cons, [1.0] * len(cons))
    relaxed.optimize()
    assert relaxed.Status == GRB.OPTIMAL
    return {
        v.VarName: v.X
        for v in relaxed.getVars()
        if v.VarName.startswith(("ArtP_", "ArtN_")) and v.X > 1e-6
    }


m = gp.Model("relax_demo")
m.Params.OutputFlag = 0
x = m.addVar(name="x")
y = m.addVar(name="y")
m.addConstr(x + y <= 1, name="budget")
m.addConstr(x >= 1, name="x_min")
m.addConstr(y >= 1, name="y_min")
violations = minimal_relaxation(m)
print(violations, round(sum(violations.values()), 4))
# Expected: total violation 1.0, e.g. {'ArtP_budget': 1.0} (ties exist: relaxing x_min also works)
```

**Pitfall:** `feasRelax` *replaces* the model's objective with the violation objective and adds
artificial `ArtP_`/`ArtN_` variables — always run it on `m.copy()`. Unit penalties answer "what
is the smallest total violation", which is rarely the business question; weight the penalties by
the real cost of breaking each constraint family (overtime cost, late-delivery cost) or the
relaxation will concentrate all violation on the cheapest-to-break constraint. The convenience
wrapper `feasRelaxS(relaxobjtype, minrelax, vrelax, crelax)` relaxes everything uniformly and is
fine for a first look.

## Solution Pool, Multi-Objective API, and MIP Starts

### Pattern: solution pool — K best solutions in one solve

Decision support often needs alternatives, not one optimum (Danna, Fennell & Rothberg (2007),
generating multiple solutions for MIPs). `PoolSearchMode = 2` makes Gurobi prove it found the
`PoolSolutions` best solutions within `PoolGap` of the optimum.

```python
import gurobipy as gp
from gurobipy import GRB


def knapsack_pool(
    profit: list[float], weight: list[float], cap: float, keep: int, rel_gap: float
) -> list[tuple[float, list[int]]]:
    """Collect the `keep` best knapsack solutions within rel_gap of the optimum."""
    n = len(profit)
    m = gp.Model("pool")
    m.Params.OutputFlag = 0
    m.Params.PoolSearchMode = 2   # 0: incidental pool, 1: best effort, 2: K best with proof
    m.Params.PoolSolutions = keep
    m.Params.PoolGap = rel_gap    # drop pool members more than rel_gap worse than the optimum
    x = m.addVars(n, vtype=GRB.BINARY, name="x")
    m.addConstr(gp.quicksum(weight[i] * x[i] for i in range(n)) <= cap, name="cap")
    m.setObjective(gp.quicksum(profit[i] * x[i] for i in range(n)), GRB.MAXIMIZE)
    m.optimize()
    assert m.Status == GRB.OPTIMAL
    pool: list[tuple[float, list[int]]] = []
    for k in range(m.SolCount):
        m.Params.SolutionNumber = k  # selects which solution Xn refers to
        pool.append((m.PoolObjVal, [i for i in range(n) if x[i].Xn > 0.5]))
    return pool


sols = knapsack_pool([10.0, 9.0, 8.0, 7.0], [4.0, 4.0, 4.0, 4.0], cap=8.0, keep=4, rel_gap=0.25)
for obj, items in sols:
    print(obj, items)
# Expected: 19.0 [0, 1]; 18.0 [0, 2]; 17.0 [0, 3] and/or [1, 2]; 16.0 ... — best first
```

**Pitfall:** read pool members through `.Xn` after setting `Params.SolutionNumber`; `.X` always
returns the incumbent (solution 0). With `PoolSearchMode = 0` (default) the pool merely records
incumbents found on the way and proves nothing about the K-best claim. Solutions that differ only
in continuous variables count as distinct, so a pool over a mixed model can be full of integer
duplicates — deduplicate on the integer projection. Symmetric models fill the pool with permuted
copies of one design; add symmetry breaking first if diversity is the goal.

### Pattern: multi-objective API — hierarchical and blended

`setObjectiveN` runs lexicographic passes (by `priority`) or blends objectives at equal priority
(by `weight`). Degradation tolerances (`reltol`/`abstol`) allow lower-priority objectives to
trade away a controlled amount of higher-priority quality.

```python
import gurobipy as gp
from gurobipy import GRB


def lexicographic_knapsack(
    profit: list[float], weight: list[float], cap: float, slack: float
) -> tuple[float, float]:
    """Maximize profit first, then minimize weight, allowing slack relative profit loss."""
    n = len(profit)
    m = gp.Model("multiobj")
    m.Params.OutputFlag = 0
    m.ModelSense = GRB.MAXIMIZE  # all objectives share one sense; negate those to minimize
    x = m.addVars(n, vtype=GRB.BINARY, name="x")
    m.addConstr(gp.quicksum(weight[i] * x[i] for i in range(n)) <= cap, name="cap")
    m.setObjectiveN(
        gp.quicksum(profit[i] * x[i] for i in range(n)),
        index=0, priority=2, reltol=slack, name="profit",
    )
    m.setObjectiveN(
        -gp.quicksum(weight[i] * x[i] for i in range(n)),
        index=1, priority=1, name="light",
    )
    m.optimize()
    assert m.Status == GRB.OPTIMAL
    m.Params.ObjNumber = 0
    best_profit = m.ObjNVal
    m.Params.ObjNumber = 1
    total_weight = -m.ObjNVal
    return best_profit, total_weight


p, w = lexicographic_knapsack([6.0, 5.0, 5.0], [3.0, 2.0, 1.0], cap=5.0, slack=0.0)
print(p, w)
# Expected: profit 11.0 at weight 4.0 — the profit tie {0,1} vs {0,2} breaks toward lighter {0,2}
```

**Pitfall:** all objectives must be linear, and they all share `ModelSense` — minimize a
secondary objective in a maximize model by negating it (and negate `ObjNVal` back when
reporting). In multi-objective mode several familiar attributes change meaning: query per-
objective values via `Params.ObjNumber` + `ObjNVal`, and remember `reltol` on objective $k$
states how much *that* objective may degrade in later passes, not a tolerance on the later ones.
Hierarchical solves cost roughly one MIP per priority level; for a true Pareto frontier use
epsilon-constraint loops instead (the multi-objective API returns one point, not a front).

### Pattern: MIP starts — seed the solver with known solutions

Feed solutions from heuristics, previous runs, or relaxations as starting incumbents. An accepted
start gives an immediate upper bound (minimization), enables stronger pruning, and lets reduced-
cost fixing bite from node 0. Construction heuristics that produce good starts are covered in
**warm-starts-and-initial-solutions**.

```python
import gurobipy as gp
from gurobipy import GRB


def solve_with_two_starts(
    profit: list[float], weight: list[float], cap: float
) -> tuple[float, int]:
    """Knapsack with two MIP starts: profit-greedy and density-greedy packs."""
    n = len(profit)
    m = gp.Model("starts")
    m.Params.OutputFlag = 0
    x = m.addVars(n, vtype=GRB.BINARY, name="x")
    m.addConstr(gp.quicksum(weight[i] * x[i] for i in range(n)) <= cap, name="cap")
    m.setObjective(gp.quicksum(profit[i] * x[i] for i in range(n)), GRB.MAXIMIZE)

    def greedy(order: list[int]) -> list[float]:
        load, plan = 0.0, [0.0] * n
        for i in order:
            if load + weight[i] <= cap:
                load += weight[i]
                plan[i] = 1.0
        return plan

    orders = [
        sorted(range(n), key=lambda i: -profit[i]),
        sorted(range(n), key=lambda i: -profit[i] / weight[i]),
    ]
    m.NumStart = len(orders)
    for s, order in enumerate(orders):
        m.Params.StartNumber = s  # selects which start vector the Start attribute writes to
        plan = greedy(order)
        for i in range(n):
            x[i].Start = plan[i]
    m.optimize()
    assert m.Status == GRB.OPTIMAL
    return m.ObjVal, m.SolCount


obj, n_sols = solve_with_two_starts(
    profit=[15.0, 10.0, 9.0, 5.0], weight=[8.0, 5.0, 5.0, 3.0], cap=10.0
)
print(obj, n_sols)
# Expected: 19.0 (items 1 and 2); both starts are accepted as incumbents, SolCount >= 2
```

**Pitfall:** watch the log for `User MIP start did not produce a new incumbent` — a rejected
start usually means the heuristic solution violates a constraint by more than the tolerances, or
a partial start could not be completed within `StartNodeLimit`. Debug by fixing all variables to
the start values (`lb = ub = start`) and calling `computeIIS()` on the fixed model; the IIS names
the violated constraint. When the start quality is doubtful, use `VarHintVal` instead of `Start`:
hints bias search without claiming feasibility, so a wrong hint cannot poison the incumbent.

## Matrix API and Parameter Tuning

### Pattern: matrix API — build models at numpy speed

When build time dominates (many similar constraints, data already in arrays), `addMVar` plus
`addMConstr`/operator syntax replaces Python loops with one vectorized call. Typical speedups on
10^5+ nonzero models are 10-100x in build time.

```python
import numpy as np
import scipy.sparse as sp
import gurobipy as gp
from gurobipy import GRB


def solve_mdknapsack_matrix(
    c: np.ndarray, A: sp.csr_matrix, b: np.ndarray
) -> tuple[np.ndarray, float]:
    """Multidimensional knapsack via the matrix API: one addMVar, one addMConstr."""
    n = c.shape[0]
    m = gp.Model("mdk_matrix")
    m.Params.OutputFlag = 0
    x = m.addMVar(n, vtype=GRB.BINARY, name="x")
    m.addMConstr(A, x, GRB.LESS_EQUAL, b, name="capacity")
    m.setObjective(c @ x, GRB.MAXIMIZE)
    m.optimize()
    assert m.Status == GRB.OPTIMAL
    return x.X.round().astype(int), m.ObjVal


rng = np.random.default_rng(42)
n_items, n_dims = 30, 5
c = rng.integers(10, 100, size=n_items).astype(float)
A = sp.csr_matrix(rng.integers(1, 20, size=(n_dims, n_items)).astype(float))
b = 0.4 * np.asarray(A.sum(axis=1)).ravel()
sol, obj = solve_mdknapsack_matrix(c, A, b)
print(int(sol.sum()), round(obj, 1))
# Expected: a feasible selection of roughly 10-15 items at the optimal profit for seed 42
```

**Pitfall:** pass `A` as `scipy.sparse` — a dense numpy matrix for a 10^5 x 10^5 system
allocates terabytes before Gurobi sees it. MVar slicing (`x[5:20]`) and `A @ x` expressions are
convenient but each creates temporary objects; build constraint blocks once rather than slicing
inside loops. Named matrix constraints get index suffixes (`capacity[0]`, `capacity[1]`); keep a
row-index-to-meaning map, because IIS output and shadow-price reports will refer to these names.

### Pattern: parameter tuning — the tool and the manual order

Gurobi exposes 100+ parameters; Klotz & Newman (2013), practical guidelines for difficult MIPs,
recommend changing them only with log evidence. The built-in tuner automates the search.

| Parameter | Default | Controls | Try when |
|---|---|---|---|
| `MIPFocus` | 0 | 1 feasibility, 2 optimality proof, 3 bound | no incumbents / gap stalls |
| `Heuristics` | 0.05 | share of effort on primal heuristics | raise to 0.2+ for hard feasibility |
| `Cuts` | -1 | global cut aggressiveness 0-3 | root gap large → 2-3; cut loop slow → 0-1 |
| `Presolve` | -1 | 0 off, 1 mild, 2 aggressive | presolve slow or destroys structure |
| `Method` | -1 | root LP: 0 primal, 1 dual, 2 barrier | huge root LPs → 2 |
| `Threads` | 0 (all) | parallelism | reproducibility, memory pressure |
| `Seed` | 0 | random perturbations | variability testing (3+ seeds) |
| `MIPGap` | 1e-4 | relative stop gap | heuristic use → 0.005-0.02 |
| `TimeLimit` | inf | wall clock | always set in experiments |
| `NodefileStart` | inf | spill tree to disk after N GB | memory blowups → 0.5 |
| `NumericFocus` | 0 | numerical care 0-3 | warnings, wrong answers near tolerances |
| `IntFeasTol` | 1e-5 | integrality tolerance | big-M models leaking flow → 1e-7 |

```python
import numpy as np
import gurobipy as gp
from gurobipy import GRB


def tune_and_save(m: gp.Model, tune_seconds: float, prm_path: str) -> dict[str, float]:
    """Run the built-in tuner, load the best setting, persist it as a .prm file."""
    m.Params.TuneTimeLimit = tune_seconds
    m.Params.TuneTrials = 2   # repeat each setting with perturbed seeds to dampen variability
    m.Params.TuneOutput = 1   # one summary line per completed trial
    m.tune()
    if m.TuneResultCount == 0:
        return {}
    m.getTuneResult(0)        # index 0 = best parameter set; loads it into the model
    m.write(prm_path)
    settings: dict[str, float] = {}
    with open(prm_path, encoding="utf-8") as fh:
        for line in fh:
            parts = line.split()
            if len(parts) == 2 and not line.startswith("#"):
                settings[parts[0]] = float(parts[1])
    return settings


rng = np.random.default_rng(11)
A = (rng.random((60, 200)) < 0.06).astype(float)
A[np.arange(60), rng.integers(0, 200, size=60)] = 1.0
cost = rng.uniform(1.0, 5.0, size=200)
model = gp.Model("tune_demo")
x = model.addVars(200, vtype=GRB.BINARY, name="x")
model.addConstrs(
    (gp.quicksum(A[r, j] * x[j] for j in range(200) if A[r, j] > 0) >= 1 for r in range(60)),
    name="cover",
)
model.setObjective(gp.quicksum(cost[j] * x[j] for j in range(200)), GRB.MINIMIZE)
found = tune_and_save(model, tune_seconds=60.0, prm_path="tuned_settings.prm")
print(found)
# Expected: a small dict such as {'Heuristics': 0.0, 'Cuts': 1.0} — whatever beat the defaults
```

**Pitfall:** tuning a single instance with a single seed mostly fits noise — MIP performance
variability from permutation/seed changes alone routinely exceeds 25% (Lodi & Tramontani (2013),
performance variability in MIP). Tune on a representative instance *set* (the `grbtune` command-
line tool accepts multiple model files), keep `TuneTrials >= 2`, and validate the winning `.prm`
on held-out instances and 3 fresh seeds before adopting it. Re-tune after any formulation change;
tuned parameters are formulation-specific.

## Advanced Techniques

### Callback state and thread discipline

Gurobi serializes callback invocations even in multi-threaded solves, so a Python callback never
runs concurrently with itself — plain attributes are safe for state. Use the `model._name`
convention (a leading underscore avoids collisions with Gurobi attributes) or closures to carry
data; never call `getAttr`/`setAttr`, `addConstr`, or `optimize` on the model inside a callback —
the only legal mutations are `cbLazy`, `cbCut`, `cbSetSolution`, `cbStopOneMultiObj`, and
`terminate`. Exceptions raised inside a callback abort the solve with a generic callback error;
wrap risky separation code, store the traceback on `model._cb_error`, call `model.terminate()`,
and re-raise after `optimize()` returns so failures are visible instead of swallowed.

### Performance variability and seed protocols

Before crediting any parameter or cut with a speedup, measure the noise floor: run the unchanged
model with `Seed` in {0, 1, 2} and record the spread of solve times. A change is real only if it
beats the spread on multiple instances. Report the full protocol (Gurobi version, parameter file,
seeds, time limit, hardware) with results; see Klotz & Newman (2013) for reporting practice. For
paper experiments fix `Threads` explicitly — "all cores" makes results machine-dependent, and
deterministic work units (`WorkLimit`) travel across machines better than `TimeLimit`.

### Numerical health checks

Advanced features amplify numerical issues: lazy constraints with loose big-M values let
heuristic incumbents pass `IntFeasTol` while violating the intended logic, and user cuts derived
from a near-singular basis can be invalid. Check `m.KappaExact` (basis condition number) when
answers look wrong: above 1e10 is concerning, above 1e14 results are unreliable. Inspect
coefficient ranges with `m.printStats()`; aim for at most 1e6-1e9 spread between the smallest and
largest matrix coefficients. Remedies in order: rescale units in the data, tighten big-M values
(see linearization guidance in **milp-modeling-gurobi**'s neighborhood), then `NumericFocus = 2`
or 3, then `IntFeasTol`/`FeasibilityTol` tightening as a last resort.

### Memory control on large trees

A branch-and-bound tree on a hard instance can exhaust RAM long before the time limit. Set
`NodefileStart = 0.5` (gigabytes of in-memory nodes before spilling to disk) and `NodefileDir`
to a fast scratch disk; the slowdown is modest and far better than the OS killing the process.
Reducing `Threads` cuts memory roughly linearly because each thread keeps node working sets.
`MemLimit` turns out-of-memory into a clean `MEM_LIMIT` status you can handle in the experiment
driver; pool memory scales with `PoolSolutions` times the variable count.

### Combining features safely

Common stacks and their interaction rules: lazy constraints + MIP starts require the start to
satisfy *all* lazy constraints, including ones not yet generated — Gurobi checks starts against
the explicit model only, so validate starts with your own separation routine first. Solution pool
+ multi-objective fills the pool during the final priority pass only. Callbacks + tuning: the
tuner ignores callback effects entirely, so models whose performance depends on lazy cuts must be
tuned manually. IIS + lazy formulations: `computeIIS` sees only the constraints currently in the
model, so an "IIS-clean" master can still be infeasible against the full lazy family.

## Practical Challenges

**The solver returns an "optimal" solution that violates a lazy constraint.** Some `MIPSOL`
candidate slipped through unseparated — usually an early-return bug or a tolerance mismatch
(your check uses 1e-9 while the candidate is integral only to 1e-5). Validate every incumbent
with an independent feasibility checker after the solve; treat `vals[e] > 0.5`, not `== 1.0`,
as "selected".

**Callback slows the solve to a crawl.** Profile the callback alone: log entry counts per
`where` code and cumulative time. Typical fixes: skip `MIPNODE` separation except every k-th
node, separate only the most violated constraint instead of all violated ones, and replace
Python-loop scans with numpy operations over a cached coefficient array.

**`cbGetNodeRel` raises an error.** It is only valid when
`cbGet(GRB.Callback.MIPNODE_STATUS) == GRB.OPTIMAL`; nodes can be infeasible, cut off, or
unsolved. Always check the status first — this is the single most common callback crash.

**User cuts seem ignored.** Check `PreCrush = 1`, and remember Gurobi may judge your cuts
unhelpful and drop them — verify in the log (`User: n` in the cut summary). If they truly
help, add the strongest ones as regular constraints before the solve instead.

**MIP start silently rejected.** The log says the start produced no incumbent. Fix all integer
variables to start values, solve; if infeasible, `computeIIS` names the broken constraint. If
the fixed model is feasible, the start was only partial and completion failed — raise
`StartNodeLimit` or provide values for all integer variables.

**The IIS has 400 members and helps nobody.** Large IISes usually mean the real conflict is an
aggregate (total capacity vs total demand) expressed through many rows. Try `IISMethod = 1` for
a smaller IIS, group constraints by family name prefix in the report, and run feasRelax with
family-level penalties to localize which family must give.

**`INF_OR_UNBD` instead of a clear status.** Presolve's dual reductions cannot distinguish the
two. Re-solve with `DualReductions = 0` to get a definite `INFEASIBLE` or `UNBOUNDED`; if
unbounded, an objective coefficient or a missing bound is the usual cause.

**Solution pool full of near-identical solutions.** With symmetric formulations the K best
solutions are permutations of one design. Add symmetry-breaking constraints, deduplicate on a
canonical form of the integer solution, or post-filter the pool by minimum Hamming distance
before presenting alternatives.

**Tuned parameters help on the tuning instance, hurt in production.** Classic overtuning. Split
instances into tune/validate sets (as in **algorithm-benchmarking-statistics** protocols), tune
on one, accept the `.prm` only if it wins on the other across 3 seeds; otherwise keep defaults.

**Multi-objective solve ends with a working incumbent but odd attributes.** `ObjVal` reflects
the last pass; per-objective values need `Params.ObjNumber`. If a time limit hits mid-hierarchy,
earlier priorities are solved and later ones are not — monitor via the `MULTIOBJ` callback.

## Tools & Libraries

| Tool | When to use | Note |
|---|---|---|
| `gurobipy` | All patterns here | Python API; matrix API needs numpy, sparse input needs scipy |
| `grbtune` (CLI) | Tuning over instance sets | Accepts many `.mps`/`.lp` files; writes ranked `.prm` files |
| `gurobi_cl` (CLI) | Quick solves, parameter experiments | `gurobi_cl ResultFile=sol.sol model.mps` without Python |
| `scipy.sparse` | Constraint matrices for `addMConstr` | Use CSR for row-wise families; never densify |
| `numpy` | Data prep, callback-side separation math | Vectorize separation checks over cached arrays |
| `.prm` / `.mps` / `.ilp` files | Reproducibility artifacts | Commit the `.prm`; `.ilp` holds the IIS for reports |
| OR-Tools / SCIP / HiGHS | No Gurobi license available | Callback and IIS support differs widely; port patterns, not code |

## Output Format

Deliverables for advanced-feature work are configuration plus evidence. Use these templates.

**Callback deployment checklist:**

```text
[ ] Params.LazyConstraints = 1 set (lazy) / Params.PreCrush = 1 set (user cuts)
[ ] MIPNODE_STATUS == GRB.OPTIMAL checked before every cbGetNodeRel
[ ] Every MIPSOL candidate separated; no early-return path skips the check
[ ] Callback exceptions captured and re-raised after optimize()
[ ] Independent post-solve feasibility validation of the final incumbent
[ ] Callback time share measured (target < 20% of total solve time)
[ ] Status handling covers OPTIMAL, TIME_LIMIT/INTERRUPTED with SolCount > 0, INFEASIBLE
```

**Infeasibility triage report (one per infeasible model):**

```text
Model: <file/build id>      Gurobi: <version>      DualReductions checked: yes/no
IIS size: <k constraints, b bounds>   IIS file: infeasible_core.ilp
Conflicting families: <names, counts>
Root cause hypothesis: <one sentence>
Repair options: (1) data fix <which>, (2) constraint relaxation <which, penalty>,
                (3) feasRelax minimal violation = <value> concentrated on <family>
Decision and owner: <chosen option>
```

**Parameter file convention (`.prm`, committed next to results):**

```text
# tuned_settings.prm — tuned on instances {a,b,c}, validated on {d,e}, seeds 0-2
# Gurobi 12.0, 8 threads, TimeLimit 600
MIPFocus  1
Heuristics  0.2
Cuts  2
Seed  0
Threads  8
```

**Tuning/experiment report checklist:** instance set and split, baseline vs tuned times per
seed, variability spread, win/loss per instance, the adopted `.prm`, and the Gurobi version.

## Questions to Ask

- What does the log show — where does time go: presolve, root LP, cut loop, or tree search?
- Is the model infeasible, slow, or wrong? Which status code and final gap do you see?
- Can your constraint family be enumerated (thousands) or only separated (exponential)?
- Do you have a feasible solution from any heuristic or a previous run to warm-start from?
- One optimum, K alternatives, or a trade-off curve — what does the decision-maker actually need?
- Which Gurobi version and license size; how many threads and how much RAM on the target machine?
- How many tuning instances exist, can some be held out, and must results be reproducible?

## Related Skills

- **milp-modeling-gurobi** — when the question is building the model itself: variables,
  constraint builders, objectives, and basic solve/status handling.
- **cutting-planes-valid-inequalities** — when you need the cut families and separation theory
  behind `cbLazy`/`cbCut`: covers, cliques, MIR, Gomory, subtour elimination.
- **benders-decomposition** — when lazy-constraint callbacks implement Benders optimality and
  feasibility cuts for decomposable or two-stage models.
- **warm-starts-and-initial-solutions** — when the focus is producing good starting solutions:
  construction heuristics, partial fixing, and hint strategies feeding MIP starts.
- **matheuristics** — when solver features are embedded in a heuristic loop: fix-and-optimize,
  local branching, and MIP-based repair with budgeted solver calls.
