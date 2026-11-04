---
name: warm-starts-and-initial-solutions
description: When the user wants to construct an initial solution and feed it into a solver — construction heuristics by problem class, MIP starts and variable hints in Gurobi, partial fixing, and seeding metaheuristic populations from exact solution pools. Also use when the user mentions "warm start," "MIP start," "initial solution," "construction heuristic," "seed the population," "variable hints," or when the solver struggles to find any feasible solution. For callback injection and solution pools, see gurobi-advanced-features; for fix-and-optimize hybrids built on partial fixing, see matheuristics.
---

# Warm Starts and Initial Solutions

You are an expert in initial-solution engineering for combinatorial optimization: building good starting solutions cheaply, injecting them into exact solvers (MIP starts, variable hints, partial fixing, basis reuse), and moving solutions the other way — from exact solvers into metaheuristic populations. Use the framework below to decide which mechanism fits, to run the injection protocol end to end, and to measure whether the warm start actually paid for itself. This is a methodology skill: the protocols matter as much as the code.

## Initial Assessment

Establish these facts before touching any `Start` attribute. Most failed warm starts trace back to a skipped item here.

- **Direction of transfer.** Heuristic solution into an exact solver, exact solution into a metaheuristic, or solver-to-solver across a reoptimization sequence? Each direction has its own mechanism and its own failure modes.
- **Source of the start.** A construction heuristic, a previous solve on slightly different data, a rounded LP relaxation, or a human-made plan? The source determines how much of it you can trust and whether it is feasible for the current model.
- **Complete or partial values.** Does the candidate cover every variable family, or only the "important" ones (e.g., the binaries)? Partial starts and complete starts go through different mechanisms.
- **Feasibility for THIS model.** A solution feasible for last week's data, or for a model variant without one constraint family, is not a MIP start — it is a hint at best. Verify against the current model before injecting.
- **Where the pain is.** Time to first feasible solution, incumbent quality at the time limit, or proving optimality? Warm starts improve only the primal side; if the dual bound is the bottleneck, a warm start will not close the gap.
- **Solver and API.** Gurobi (`Start`, `VarHintVal`, `NumStart`, basis attributes), OR-Tools CP-SAT (`AddHint`), HiGHS, PuLP/Pyomo passthrough? The mechanism names and semantics differ.
- **Model identity across runs.** Is the model object kept alive, or rebuilt from scratch each run? Rebuilt models need name-based variable mapping; object references die with the old model.
- **Is this a one-off solve or a sequence?** Rolling horizons, branch-and-price iterations, and parameter sweeps re-solve near-identical models; there the start should come from the previous solution, not from a constructor.
- **Cost of constructing the start.** A constructor that takes 30 s to save 10 s of solver time is a net loss. Budget construction time against expected savings.
- **Metaheuristic side: population size and seed fraction.** How many seeds are available, how diverse are they, and what fraction of the population should they occupy? Seeding 100% of a population with near-identical elites kills diversity on arrival.
- **Measurement plan.** Same time limit, with/without comparison, several seeds for randomized components. Decide the protocol before running, or the result will be an anecdote.
- **Tolerances.** `IntFeasTol` and feasibility tolerances decide whether a numerically noisy start is accepted. Values like 0.9999999 must be rounded before injection, not after rejection.

## Warm-Start Decision Framework

### Why warm starts work — and what they cannot do

Branch-and-bound for a minimization MIP keeps an incumbent value $\bar z$ and prunes every node whose relaxation bound already matches it:

$$
\text{prune node } k \iff z_{LP}^{(k)} \;\ge\; \bar z - \varepsilon
$$

A good incumbent supplied at time zero prunes from the first node onward, shrinks the tree, and lets reduced-cost fixing remove variables early. The reported gap is

$$
\text{gap} = \frac{\bar z - z_{\text{dual}}}{|\bar z|},
$$

and a warm start moves only $\bar z$. The dual bound $z_{\text{dual}}$ follows its own trajectory, untouched by the start. Consequences: warm starts shine when feasible solutions are hard to find (tight rostering, big-M models where solver heuristics flounder) or when the run is killed by a time limit while the incumbent is still poor; they do little on instances the solver cracks at the root, and nothing for a gap that is stuck because the dual bound will not move. Modern solvers also run strong internal primal heuristics — RINS, feasibility pump, polishing (Danna, Rothberg & Le Pape 2005, "Exploring relaxation induced neighborhoods to improve MIP solutions"; Berthold 2006, "Primal Heuristics for Mixed Integer Programs") — so the bar your start must beat is "what Gurobi finds in the first seconds anyway," not zero.

### Mechanism taxonomy

| Mechanism | Gurobi handle | What the solver does | Use when | Main risk |
|---|---|---|---|---|
| Complete MIP start | `var.Start` on all variables | Checks feasibility, installs as incumbent before B&B | You hold a full feasible solution for this exact model | Silently rejected if infeasible or off-tolerance |
| Partial MIP start | `var.Start` on a subset, rest `GRB.UNDEFINED` | Runs a completion heuristic / sub-MIP to fill the gaps | You trust the binaries but not the continuous part | Completion fails; raise `StartNodeLimit` or complete it yourself |
| Multiple starts | `NumStart` attr + `Params.StartNumber` | Evaluates each start, keeps the best feasible ones | Several candidate solutions of unknown relative quality | Costs root time per start; keep the list short |
| Variable hints | `var.VarHintVal` (+ `VarHintPri`) | Biases branching and heuristics toward the hinted values | Values are educated guesses, joint feasibility unsure | Bad hints steer the whole search into a poor region |
| Branching priority | `var.BranchPriority` | Branches on high-priority variables first | You know which decisions dominate the structure | Changes the tree, not the incumbent; not a start at all |
| Partial fixing | `var.LB = var.UB = value` | Restricts the feasible set to the fixed sub-space | Inside fix-and-optimize / LNS loops (see matheuristics) | Optimal solution may be cut off; this is not a suggestion |
| Callback injection | `cbSetSolution` + `cbUseSolution` in `MIPNODE` | Installs solutions found by an external heuristic mid-run | A heuristic keeps producing solutions while B&B runs | Overhead per callback; see gurobi-advanced-features |
| LP basis reuse | `VBasis` / `CBasis`, `Params.LPWarmStart` | Starts simplex from the given basis | Re-solving an LP after a small data change | Useless for barrier without crossover; basis must match dimensions |
| LP vector start | `PStart` / `DStart` | Starts from primal/dual vectors instead of a basis | Crossover-free pipelines, basis unavailable | Weaker than a basis for simplex |
| CP-SAT hint | `model.AddHint(vars, values)` | Seeds the feasibility search | OR-Tools CP-SAT models | One hint only; no feasibility guarantee needed |

### Decision tree

```text
Need a better primal side?
│
├─ Target is an EXACT solver (MIP / CP)
│   ├─ Complete feasible solution for THIS model in hand
│   │     → complete MIP start; verify acceptance in the log
│   ├─ Only part of the solution is trusted (e.g. the binaries)
│   │     ├─ values MUST hold        → partial fixing (LB = UB) inside a
│   │     │                            fix-and-optimize loop (matheuristics)
│   │     ├─ values are a proposal   → partial MIP start (rest UNDEFINED)
│   │     └─ joint feasibility unsure→ variable hints (VarHintVal)
│   ├─ Several candidate solutions
│   │     → multiple starts: NumStart + StartNumber loop
│   ├─ Solutions keep arriving DURING the solve (external heuristic)
│   │     → callback injection via cbSetSolution (gurobi-advanced-features)
│   └─ Pure LP re-solved after a small data change
│         → basis reuse (VBasis/CBasis) with LPWarmStart = 1
│
└─ Target is a METAHEURISTIC
    ├─ Single-solution method (SA, tabu, ILS)
    │     → best constructive solution, polished by local search first
    └─ Population method (GA, BRKGA, ALNS solution pool)
          → seed 5–20% of the population: elites + mutated copies
            + random fill; never seed 100%
```

### When to invest in the start

- **Invest** when instances time out with a weak incumbent, when feasibility itself is hard, when the same model is re-solved many times, or when a domain constructor encodes knowledge the solver cannot rediscover cheaply.
- **Do not invest** when the solver reaches near-optimality in seconds, when the gap is dual-bound-limited, or when the constructor costs more time than it saves. Measure with the protocol below instead of assuming.

## Construction Heuristics by Problem Class

A constructor should be cheap (at most a few seconds at production scale), deterministic given a seed, and honest — validated by an independent feasibility check before anyone calls it a solution. Three design rules cover most cases. First, greedy on the right marginal criterion: cost per unit of newly covered demand, value per unit of consumed capacity, regret between the best and second-best option. Second, randomize the greedy choice only when you need many diverse starts (restricted candidate lists — see grasp). Third, always polish with a few passes of local search before injection; 2-opt on a nearest-neighbor tour removes a third of its excess at trivial cost (see local-search-and-neighborhoods).

| Problem class | Constructor | Complexity | Typical quality | Reference |
|---|---|---|---|---|
| 0-1 / multidim. knapsack | value/weight ratio greedy | $O(n \log n)$ | 1–5% below optimum | Martello & Toth (1990), "Knapsack Problems" |
| TSP | nearest neighbor, greedy edge | $O(n^2)$ | 20–25% above optimum; $\Theta(\log n)$ worst case | Rosenkrantz, Stearns & Lewis (1977) |
| CVRP | Clarke–Wright savings | $O(n^2 \log n)$ | 5–10% above best known | Clarke & Wright (1964) |
| Permutation flow shop | NEH insertion | $O(n^2 m)$ with Taillard's acceleration | 2–5% above best known | Nawaz, Enscore & Ham (1983) |
| Set covering | greedy cost per newly covered row | $O(\text{rows} \cdot \text{cols})$ per pick | $\ln n$ approximation guarantee | Chvátal (1979) |
| Generalized assignment | regret-2 insertion | $O(n^2 m)$ | feasible on most instances, 5–15% | Martello & Toth (1981) |
| Graph coloring | DSATUR | $O(n^2)$ | near-optimal on sparse graphs | Brélaz (1979) |
| $P \,\|\, C_{\max}$ scheduling | LPT list scheduling | $O(n \log n)$ | $\le 4/3 - 1/(3m)$ of optimum | Graham (1969) |
| Facility location | open by cost/capacity ratio, assign nearest | $O(n \log n + nm)$ | 10–20% above optimum | folklore; polish with interchange |

Four of these, implementation-grade and independently checkable:

```python
import numpy as np


def greedy_knapsack(values: np.ndarray, weights: np.ndarray, capacity: float) -> np.ndarray:
    """0-1 knapsack greedy in Dantzig (value/weight) order. O(n log n)."""
    order = np.argsort(-values / weights)
    x = np.zeros(len(values), dtype=int)
    load = 0.0
    for i in order:
        if load + weights[i] <= capacity:
            x[i] = 1
            load += weights[i]
    return x


def nearest_neighbor_tour(dist: np.ndarray, start: int = 0) -> np.ndarray:
    """TSP nearest-neighbor construction. O(n^2). Always polish with 2-opt."""
    n = dist.shape[0]
    unvisited = np.ones(n, dtype=bool)
    unvisited[start] = False
    tour = [start]
    current = start
    for _ in range(n - 1):
        masked = np.where(unvisited, dist[current], np.inf)
        current = int(np.argmin(masked))
        unvisited[current] = False
        tour.append(current)
    return np.array(tour)


def greedy_set_cover(cover: np.ndarray, cost: np.ndarray) -> np.ndarray:
    """Greedy set cover: repeatedly pick the column with the lowest cost per
    newly covered row. ln(n) guarantee (Chvátal 1979)."""
    n_rows, n_cols = cover.shape
    uncovered = np.ones(n_rows, dtype=bool)
    chosen = np.zeros(n_cols, dtype=int)
    while uncovered.any():
        gain = cover[uncovered].sum(axis=0)
        score = np.where(gain > 0, cost / np.maximum(gain, 1), np.inf)
        j = int(np.argmin(score))
        chosen[j] = 1
        uncovered &= ~cover[:, j].astype(bool)
    return chosen


def regret2_gap_assignment(cost: np.ndarray, demand: np.ndarray,
                           capacity: np.ndarray) -> np.ndarray | None:
    """Generalized assignment by regret-2: always commit the task whose two
    cheapest feasible agents differ most. Returns agent per task, or None if
    the construction dead-ends (then fall back to a penalty/repair start)."""
    n_tasks, n_agents = cost.shape
    assign = -np.ones(n_tasks, dtype=int)
    load = np.zeros(n_agents)
    unassigned = set(range(n_tasks))
    while unassigned:
        best_task, best_regret, best_agent = -1, -1.0, -1
        for t in unassigned:
            feas = np.where(load + demand[t] <= capacity)[0]
            if feas.size == 0:
                return None
            c = np.sort(cost[t, feas])
            regret = float(c[1] - c[0]) if c.size > 1 else float("inf")
            if regret > best_regret:
                best_regret = regret
                best_task = t
                best_agent = int(feas[np.argmin(cost[t, feas])])
        assign[best_task] = best_agent
        load[best_agent] += demand[best_task]
        unassigned.remove(best_task)
    return assign


# Tiny synthetic checks, one per constructor.
v = np.array([10.0, 7.0, 4.0, 3.0])
w = np.array([5.0, 4.0, 3.0, 1.0])
print(greedy_knapsack(v, w, capacity=8.0))

D = np.array([[0, 1, 4, 3], [1, 0, 2, 5], [4, 2, 0, 1], [3, 5, 1, 0]], dtype=float)
tour = nearest_neighbor_tour(D)
print(tour, D[tour, np.roll(tour, -1)].sum())

cover = np.array([[1, 0, 0], [1, 1, 0], [0, 1, 1], [0, 0, 1]])
print(greedy_set_cover(cover, cost=np.array([2.0, 2.0, 3.0])))

gap_cost = np.array([[4.0, 9.0], [6.0, 7.0], [3.0, 8.0]])
a = regret2_gap_assignment(gap_cost, demand=np.array([3.0, 3.0, 3.0]),
                           capacity=np.array([6.0, 6.0]))
print(a, gap_cost[np.arange(3), a].sum())
# Expected: knapsack [1 0 0 1] (value 13 vs optimum 14 — greedy misses {0,2});
# tour [0 1 2 3] with length 7.0; cover [1 0 1] at cost 5.0;
# GAP assignment [0 1 0] at cost 14.0, capacities 6/6 respected.
```

The knapsack line is the standing reminder: constructors are starting points, not answers. Greedy returns 13 where the optimum is 14, and that 7% gap is exactly what the receiving solver or metaheuristic is for.

## End-to-End Protocol: Warm-Starting a MIP

Seven steps, in order. Skipping step 2 or step 5 is the source of most "the warm start did nothing" reports.

1. **Construct** a candidate with a problem-class constructor (previous section), or take the previous solve's solution in a reoptimization setting.
2. **Validate independently.** Recompute feasibility and objective with plain numpy against the instance data — never by trusting the constructor's own bookkeeping. If this check fails, fix the constructor, not the model.
3. **Build the model** exactly as you would for a cold solve (see milp-modeling-gurobi). Do not weaken constraints to admit the start.
4. **Inject** via `var.Start` (complete), or the partial mechanisms from the taxonomy if coverage is incomplete.
5. **Confirm acceptance.** With `OutputFlag = 1`, the log must show `User MIP start produced solution with objective ...`. The line `User MIP start did not produce a new incumbent` means rejected or dominated — diagnose before trusting any conclusions (see Practical Challenges).
6. **Measure** cold vs warm under the same time limit: time to first incumbent, incumbent at the limit, node count, final gap.
7. **Decide.** Keep the warm start only if step 6 shows a benefit on representative instances; otherwise delete the construction code path entirely.

The example below runs the full protocol on a single-source capacitated facility location problem — binaries for opening and for assignment, so a feasible start is genuinely informative.

```python
import gurobipy as gp
import numpy as np
from gurobipy import GRB


def make_cflp(n_fac: int, n_cust: int, seed: int) -> dict:
    """Random single-source CFLP; assignment costs are plane distances."""
    rng = np.random.default_rng(seed)
    fac = rng.uniform(0, 100, (n_fac, 2))
    cust = rng.uniform(0, 100, (n_cust, 2))
    c = np.linalg.norm(fac[:, None, :] - cust[None, :, :], axis=2)
    d = rng.integers(5, 20, n_cust).astype(float)
    u = np.full(n_fac, d.sum() * 1.18 / n_fac)   # tight: ~18% slack overall
    f = rng.uniform(300.0, 700.0, n_fac)
    return {"c": c, "d": d, "u": u, "f": f}


def greedy_cflp(inst: dict) -> tuple[np.ndarray, np.ndarray]:
    """Step 1 — construct: open facilities by opening-cost-per-capacity until
    5% spare capacity, then assign customers (largest demand first) to the
    cheapest open facility with residual room."""
    c, d, u, f = inst["c"], inst["d"], inst["u"], inst["f"]
    n_fac, n_cust = c.shape
    order = np.argsort(f / u)
    is_open = np.zeros(n_fac, dtype=int)
    next_to_open = 0
    cap = 0.0
    while cap < 1.05 * d.sum():
        is_open[order[next_to_open]] = 1
        cap += u[order[next_to_open]]
        next_to_open += 1
    x = np.zeros((n_fac, n_cust), dtype=int)
    residual = u * is_open
    for i in np.argsort(-d):
        feas = np.where(residual >= d[i])[0]
        if feas.size == 0:                      # dead end: open one more site
            j_new = order[next_to_open]
            is_open[j_new] = 1
            residual[j_new] = u[j_new]
            next_to_open += 1
            feas = np.array([j_new])
        j = feas[np.argmin(c[feas, i])]
        x[j, i] = 1
        residual[j] -= d[i]
    return is_open, x


def start_cost(inst: dict, is_open: np.ndarray, x: np.ndarray) -> float:
    """Step 2 — validate: independent feasibility check + objective recompute."""
    c, d, u, f = inst["c"], inst["d"], inst["u"], inst["f"]
    assert (x.sum(axis=0) == 1).all(), "every customer assigned exactly once"
    assert (x @ d <= u * is_open + 1e-9).all(), "capacity holds, closed sites unused"
    return float(f @ is_open + (c * x).sum())


def build_cflp(inst: dict) -> tuple[gp.Model, gp.tupledict, gp.tupledict]:
    """Step 3 — build: single-source CFLP with disaggregated linking."""
    c, d, u, f = inst["c"], inst["d"], inst["u"], inst["f"]
    n_fac, n_cust = c.shape
    m = gp.Model("cflp")
    m.Params.OutputFlag = 0      # set to 1 in step 5 to read acceptance lines
    y = m.addVars(n_fac, vtype=GRB.BINARY, name="open")
    x = m.addVars(n_fac, n_cust, vtype=GRB.BINARY, name="assign")
    m.addConstrs((x.sum("*", i) == 1 for i in range(n_cust)), name="serve")
    m.addConstrs(
        (gp.quicksum(d[i] * x[j, i] for i in range(n_cust)) <= u[j] * y[j]
         for j in range(n_fac)), name="capacity")
    m.addConstrs((x[j, i] <= y[j] for j in range(n_fac) for i in range(n_cust)),
                 name="link")
    m.setObjective(
        gp.quicksum(f[j] * y[j] for j in range(n_fac))
        + gp.quicksum(c[j, i] * x[j, i] for j in range(n_fac) for i in range(n_cust)),
        GRB.MINIMIZE)
    return m, y, x


def inject_start(y: gp.tupledict, x: gp.tupledict,
                 is_open: np.ndarray, x_start: np.ndarray) -> None:
    """Step 4 — inject: write a complete MIP start into the Start attribute."""
    n_fac, n_cust = x_start.shape
    for j in range(n_fac):
        y[j].Start = float(is_open[j])
        for i in range(n_cust):
            x[j, i].Start = float(x_start[j, i])


def solve(m: gp.Model, time_limit: float = 5.0) -> dict:
    """Step 6 — measure: solve and report the comparison quantities."""
    m.Params.TimeLimit = time_limit
    m.optimize()
    has_sol = m.Status == GRB.OPTIMAL or (m.Status == GRB.TIME_LIMIT and m.SolCount > 0)
    assert has_sol, f"no incumbent, status {m.Status}"
    return {"obj": m.ObjVal, "bound": m.ObjBound, "gap": m.MIPGap,
            "nodes": int(m.NodeCount), "time": round(m.Runtime, 2)}


inst = make_cflp(n_fac=20, n_cust=90, seed=42)
is_open, x_start = greedy_cflp(inst)
z_greedy = start_cost(inst, is_open, x_start)

m_cold, _, _ = build_cflp(inst)
cold = solve(m_cold)

m_warm, y, x = build_cflp(inst)
inject_start(y, x, is_open, x_start)
warm = solve(m_warm)

print(f"greedy start : {z_greedy:.1f}")
print(f"cold  5s     : obj={cold['obj']:.1f} nodes={cold['nodes']}")
print(f"warm  5s     : obj={warm['obj']:.1f} nodes={warm['nodes']}")
# Expected: greedy start 9420.2, which is 16% above the true optimum 8111.8.
# Under the shared 5 s limit one machine gave cold obj 8556.1 vs warm obj
# 8333.2 — the warm run spends its node budget improving a decent incumbent
# instead of hunting for a first one. Node counts and times vary by machine;
# with a long limit both runs prove 8111.8 optimal.
```

When the model is rebuilt between runs (typical in scripted experiments), variable objects from the old model are useless. Address starts by variable name instead, and the same helpers then cover multiple starts, hints, and hard fixing:

```python
import gurobipy as gp
from gurobipy import GRB


def set_mip_starts(model: gp.Model, starts: list[dict[str, float]]) -> None:
    """Load several MIP starts addressed by variable name. Variables a start
    does not mention stay GRB.UNDEFINED, so the solver completes them."""
    model.update()
    model.NumStart = len(starts)
    for k, start in enumerate(starts):
        model.Params.StartNumber = k
        for name, value in start.items():
            model.getVarByName(name).Start = value
    model.Params.StartNumber = 0


def set_hints(model: gp.Model, hints: dict[str, float], priority: int = 0) -> None:
    """Variable hints: bias heuristics and branching toward `hints` without
    requiring the values to be jointly feasible. Larger priority = more trust."""
    model.update()
    for name, value in hints.items():
        var = model.getVarByName(name)
        var.VarHintVal = value
        var.VarHintPri = priority


def fix_partial(model: gp.Model, fixed: dict[str, float]) -> None:
    """Hard-fix a trusted subset (LB = UB). This RESTRICTS the feasible set —
    it is a commitment, not a suggestion; use inside fix-and-optimize loops."""
    model.update()
    for name, value in fixed.items():
        var = model.getVarByName(name)
        var.LB = value
        var.UB = value


def tiny_knapsack() -> gp.Model:
    """4-item knapsack used as the shared demo model."""
    m = gp.Model("tiny")
    m.Params.OutputFlag = 0
    x = m.addVars(4, vtype=GRB.BINARY, name="x")
    m.addConstr(3 * x[0] + 5 * x[1] + 4 * x[2] + 2 * x[3] <= 9, name="cap")
    m.setObjective(8 * x[0] + 9 * x[1] + 6 * x[2] + 3 * x[3], GRB.MAXIMIZE)
    return m


m1 = tiny_knapsack()
set_mip_starts(m1, [{"x[0]": 1.0, "x[1]": 1.0}, {"x[2]": 1.0, "x[3]": 1.0}])
m1.optimize()

m2 = tiny_knapsack()
set_hints(m2, {"x[0]": 1.0, "x[1]": 1.0}, priority=5)
m2.optimize()

m3 = tiny_knapsack()
fix_partial(m3, {"x[1]": 0.0})
m3.optimize()
print(m1.ObjVal, m2.ObjVal, m3.ObjVal)
# Expected: 17.0 17.0 17.0 — both optima {x0,x1} and {x0,x2,x3} reach 17, so
# even fixing x1=0 loses nothing here. On real models the third call is the
# dangerous one: LB=UB can cut off the optimum, the first two cannot.
```

## End-to-End Protocol: Seeding a Metaheuristic from Exact Solutions

The reverse direction: a time-limited exact run produces a pool of good, distinct solutions, and the pool seeds a metaheuristic population for a longer or repeated search. This is the standard pattern when the MIP finds good incumbents on a truncated run but cannot close the gap, or when the production system must answer in milliseconds with a metaheuristic while an offline exact run supplies elite genes.

Protocol: (1) run the solver with `PoolSearchMode = 2` and a short time limit, harvesting up to `PoolSolutions` distinct feasible solutions; (2) deduplicate and sort by objective; (3) seed 5–20% of the population with these elites; (4) add mutated copies of the elites so their basin is sampled, not just their point; (5) fill the rest uniformly at random; (6) compare seeded vs unseeded under identical budgets and random seeds. The fraction matters: seed too much and the population converges on arrival — selection pressure amplifies near-identical elites within a few generations (see diversity discussion in the genetic-algorithms literature, e.g. Eiben & Smith 2015, "Introduction to Evolutionary Computing").

```python
import gurobipy as gp
import numpy as np
from gurobipy import GRB


def make_mkp(n_items: int, n_dims: int, seed: int) -> dict:
    """Random multidimensional knapsack with 40% capacity tightness."""
    rng = np.random.default_rng(seed)
    w = rng.integers(5, 30, (n_dims, n_items)).astype(float)
    v = rng.integers(10, 100, n_items).astype(float)
    b = 0.4 * w.sum(axis=1)
    return {"v": v, "w": w, "b": b}


def harvest_pool(inst: dict, time_limit: float, pool_size: int) -> np.ndarray:
    """Step 1 — short exact run returning a pool of distinct feasible solutions,
    best first (Gurobi orders the pool by objective)."""
    v, w, b = inst["v"], inst["w"], inst["b"]
    n = len(v)
    m = gp.Model("mkp_pool")
    m.Params.OutputFlag = 0
    m.Params.TimeLimit = time_limit
    m.Params.PoolSearchMode = 2      # actively collect the k best solutions
    m.Params.PoolSolutions = pool_size
    x = m.addVars(n, vtype=GRB.BINARY, name="x")
    m.addConstrs(
        (gp.quicksum(w[k, i] * x[i] for i in range(n)) <= b[k]
         for k in range(w.shape[0])), name="cap")
    m.setObjective(gp.quicksum(v[i] * x[i] for i in range(n)), GRB.MAXIMIZE)
    m.optimize()
    assert m.SolCount > 0, "no feasible solution within the time limit"
    sols = []
    for s in range(m.SolCount):
        m.Params.SolutionNumber = s
        sols.append([round(x[i].Xn) for i in range(n)])
    return np.array(sols, dtype=int)


def seeded_population(pool: np.ndarray, pop_size: int, n_items: int,
                      seed_frac: float, rng: np.random.Generator) -> np.ndarray:
    """Steps 3-5 — population = exact elites + mutated copies + random fill."""
    n_seed = min(len(pool), max(1, int(seed_frac * pop_size)))
    elites = pool[:n_seed]
    n_mut = min(pop_size - n_seed, n_seed)
    flips = (rng.random((n_mut, n_items)) < 0.05).astype(int)
    mutated = np.abs(elites[:n_mut] - flips)
    n_rand = pop_size - n_seed - n_mut
    randoms = (rng.random((n_rand, n_items)) < 0.5).astype(int)
    return np.vstack([elites, mutated, randoms])


def fitness(pop: np.ndarray, inst: dict) -> np.ndarray:
    """Penalized fitness: value minus a steep cost per unit of violation."""
    v, w, b = inst["v"], inst["w"], inst["b"]
    viol = np.maximum(pop @ w.T - b, 0.0).sum(axis=1)
    return pop @ v - 10.0 * v.max() * viol


def run_ga(pop: np.ndarray, inst: dict, n_gen: int,
           rng: np.random.Generator) -> float:
    """Compact (mu+lambda) binary GA: tournament selection, uniform crossover,
    bit-flip mutation, truncation replacement. All population-level numpy."""
    pop = pop.copy()
    fit = fitness(pop, inst)
    pop_size, n = pop.shape
    for _ in range(n_gen):
        a = rng.integers(0, pop_size, pop_size)
        c = rng.integers(0, pop_size, pop_size)
        parents = np.where((fit[a] >= fit[c])[:, None], pop[a], pop[c])
        partners = parents[rng.permutation(pop_size)]
        mask = rng.random((pop_size, n)) < 0.5
        children = np.where(mask, parents, partners)
        children ^= (rng.random((pop_size, n)) < 1.0 / n).astype(int)
        merged = np.vstack([pop, children])
        merged_fit = np.concatenate([fit, fitness(children, inst)])
        keep = np.argpartition(-merged_fit, pop_size - 1)[:pop_size]
        pop, fit = merged[keep], merged_fit[keep]
    return float(fit.max())


inst = make_mkp(n_items=120, n_dims=5, seed=3)
rng = np.random.default_rng(3)
pool = harvest_pool(inst, time_limit=2.0, pool_size=10)
print("pool:", len(pool), "best:", float(pool[0] @ inst["v"]))

pop_size, n_gen = 100, 150
seeded = seeded_population(pool, pop_size, 120, seed_frac=0.10, rng=rng)
random_pop = (rng.random((pop_size, 120)) < 0.5).astype(int)
print("seeded GA:", run_ga(seeded, inst, n_gen, np.random.default_rng(7)))
print("random GA:", run_ga(random_pop, inst, n_gen, np.random.default_rng(7)))
# Expected: pool of 10 with best 3693.0 (on this small demo the 2 s exact run
# already proves 3693 optimal). The seeded GA holds 3693.0 because the elite
# survives truncation replacement; the random-start GA stalls around 3641.0,
# about 1.4% short, under the identical budget. At real scale the exact run
# would stop far from optimality and the seeds are merely good, not optimal.
```

Two practical notes. First, deduplicate the pool before seeding — `PoolSearchMode = 2` returns distinct solutions, but pools merged across runs need `np.unique(pool, axis=0)`. Second, when the metaheuristic uses a different representation (a permutation, a key vector), convert through the decoder rather than seeding raw genotypes; an elite that decodes to a different phenotype than the exact solution is worse than no seed, because it carries unjustified fitness authority into selection.

## Advanced Techniques

### Completing and repairing partial starts

Gurobi completes partial starts with a restricted sub-MIP whose effort is capped by `StartNodeLimit`. When the completion keeps failing — common when the trusted variables interlock tightly with the undefined ones — do the completion yourself: fix the trusted subset, solve the remaining sub-MIP with a feasibility-focused configuration, and inject the resulting full solution as an ordinary complete start. The same function doubles as a repair operator for starts that are slightly infeasible after data changes: fix only the part that still validates.

```python
import gurobipy as gp
from gurobipy import GRB


def complete_partial_start(model: gp.Model, trusted: dict[str, float],
                           time_limit: float = 5.0) -> dict[str, float] | None:
    """Complete a partial assignment into a full feasible point by solving the
    sub-MIP with the trusted variables fixed. Returns {name: value} or None
    when the trusted part admits no completion (then shrink `trusted`)."""
    model.update()
    sub = model.copy()
    sub.update()
    for name, value in trusted.items():
        var = sub.getVarByName(name)
        var.LB = value
        var.UB = value
    sub.Params.OutputFlag = 0
    sub.Params.TimeLimit = time_limit
    sub.Params.MIPFocus = 1          # feasibility first; quality is secondary
    sub.optimize()
    if sub.SolCount == 0:
        return None
    return {var.VarName: round(var.X, 6) for var in sub.getVars()}


m = gp.Model("demo")
m.Params.OutputFlag = 0
x = m.addVars(4, vtype=GRB.BINARY, name="x")
m.addConstr(3 * x[0] + 5 * x[1] + 4 * x[2] + 2 * x[3] <= 9, name="cap")
m.setObjective(8 * x[0] + 9 * x[1] + 6 * x[2] + 3 * x[3], GRB.MAXIMIZE)

full = complete_partial_start(m, trusted={"x[0]": 1.0})
for name, value in full.items():
    m.getVarByName(name).Start = value
m.optimize()
print(full, m.ObjVal)
# Expected: {'x[0]': 1.0, 'x[1]': 0.0, 'x[2]': 1.0, 'x[3]': 1.0} and 17.0 —
# the completion picks the best fill {x2, x3} around the fixed x0, and the
# completed start is then accepted as a full incumbent at value 17.
```

### Variable hints versus MIP starts

The two mechanisms answer different questions. A MIP start says "this point is feasible — install it as the incumbent"; it must pass a feasibility check and contributes nothing if rejected. A hint says "I believe the optimal solution looks like this" — the solver biases branching directions and primal heuristics toward the hinted values, with no feasibility requirement, and the influence persists even when no single feasible point matches all hints. Prefer hints when the candidate comes from stale data (yesterday's plan after today's demand update), from a relaxation rounding, or from a structurally similar but not identical model. Set `VarHintPri` higher on values you trust more — for example, priority 10 on facility-open binaries from the previous planning round and priority 0 on the assignment binaries that churn. Hints and starts can be combined on one model; on rolling horizons the robust pattern is: previous solution as a partial start for the overlap window, hints for the freshly appended period.

### Warm starts across reoptimization sequences

Sequences of near-identical solves — rolling horizons, Benders master iterations, column-generation restricted masters, parameter sweeps — are where warm starting pays the most reliably, because the previous optimum is an excellent candidate by construction. For the LP case, carry the simplex basis: after a small right-hand-side or objective change the old basis is often optimal or near-optimal, and dual simplex re-converges in a handful of iterations.

```python
import gurobipy as gp
import numpy as np
from gurobipy import GRB


def copy_basis(src: gp.Model, dst: gp.Model) -> None:
    """Carry the optimal simplex basis between two same-shaped LPs."""
    dst.update()
    for vs, vd in zip(src.getVars(), dst.getVars()):
        vd.VBasis = vs.VBasis
    for cs, cd in zip(src.getConstrs(), dst.getConstrs()):
        cd.CBasis = cs.CBasis
    dst.Params.LPWarmStart = 1


def make_lp(rhs: float) -> gp.Model:
    """Dense random LP; only the shared RHS value changes between solves."""
    rng = np.random.default_rng(0)
    a = rng.uniform(1, 5, (40, 60))
    c = rng.uniform(1, 10, 60)
    m = gp.Model("lp")
    m.Params.OutputFlag = 0
    m.Params.Method = 1              # dual simplex, the natural re-solver
    x = m.addVars(60, ub=10.0, name="x")
    m.addConstrs((gp.quicksum(a[i, j] * x[j] for j in range(60)) <= rhs
                  for i in range(40)), name="row")
    m.setObjective(gp.quicksum(c[j] * x[j] for j in range(60)), GRB.MAXIMIZE)
    return m


lp1 = make_lp(rhs=100.0)
lp1.optimize()

lp_cold = make_lp(rhs=105.0)
lp_cold.optimize()

lp_warm = make_lp(rhs=105.0)
copy_basis(lp1, lp_warm)
lp_warm.optimize()
print(lp1.IterCount, lp_cold.IterCount, lp_warm.IterCount)
# Expected: 32.0 27.0 0.0 — after the small RHS change the copied basis is
# still optimal, so the warm LP re-solves in zero simplex iterations while
# the cold solve pays the full 27. On production-sized LPs this difference
# is the entire running time of a pricing or Benders loop.
```

Caveats: the basis is only meaningful for simplex — barrier without crossover produces no basis, so force `Method = 1` (dual simplex) or accept crossover cost; and the two models must have identical variable/constraint order, which the name-based mapping from the MIP helpers can restore when they do not. For MIP sequences, pass the previous incumbent as a (partial) start and keep hints for the changed region; do not fix, unless you are deliberately inside a fix-and-optimize scheme (see matheuristics).

### Injecting solutions during the run

When an external heuristic runs concurrently with the exact solve — an ALNS thread, a human planner, a stream of solutions from another machine — inject through a callback: in a `MIPNODE` callback, call `cbSetSolution(vars, values)` and then `cbUseSolution()` to hand Gurobi the candidate for feasibility checking and incumbent installation. This is the only mechanism that works after `optimize()` has started; `Start` attributes are read once, at the beginning. Budget the callback frequency — checking a candidate costs a sub-MIP-like effort, so inject only solutions that beat the current `cbGet(GRB.Callback.MIPNODE_OBJBST)`. Full callback mechanics, including the matching lazy-constraint patterns, are in gurobi-advanced-features.

### Warm-starting the start: chained constructors

Constructors compose. NEH already contains a greedy insertion inside a priority order; regret-2 GAP can take its agent order from a Lagrangian relaxation's reduced costs; a facility-location start improves measurably when the assignment step is re-run once after the open set stabilizes. The general pattern is constructor → cheap local search → injection, with the local-search budget capped at a fraction (10–20%) of the expected solver-time savings. Resist the temptation to grow this pipeline into a full metaheuristic: past that budget you are no longer warm-starting, you are competing with the solver, and the matheuristics skill covers that regime deliberately.

## Practical Challenges

**The log says "User MIP start did not produce a new incumbent."** Three causes, in observed frequency order: the start is infeasible for the current model; the start is feasible but worse than what presolve/heuristics already found; or rounding noise pushed an integer variable off-tolerance. Diagnose with the fixed-model trick: copy the model, set `LB = UB = start value` for every variable, and optimize. `INFEASIBLE` → run `computeIIS()` on the fixed copy and the IIS names exactly the constraints your start violates. Feasible with the expected objective → the start was merely dominated, which is fine.

**The start is feasible on paper but rejected numerically.** Constructors that work in floats produce binaries like 0.9999999. Round integer variables to exact integral values before injection, then recompute the dependent continuous variables from the rounded binaries rather than reusing their float values. If a model has genuinely tight tolerances, loosen nothing — fix the constructor's arithmetic instead.

**The warm start makes the solver slower.** It happens: a mediocre incumbent changes the pruning pattern and node order, and can suppress internal heuristics (RINS works relative to the incumbent). First check that the start beats what the solver finds unaided in the first seconds; if it does not, delete it. If it does and the slowdown persists, switch from start to hints, or start only the structural binaries and let completion rebuild the rest.

**Variable mapping breaks when the model is rebuilt.** Object references die with the model; positional indices silently shift when a constraint family is added. The only stable contract is the variable name — adopt a naming discipline (`open[3]`, `assign[3,17]`) at model-building time and address every start, hint, and fix by name, as the helpers above do.

**The seeded population converges in ten generations.** Classic seeding overdose: too many near-identical elites, amplified by selection. Cap the seed fraction at 5–20%, include mutated copies instead of more elites, and monitor population diversity (mean pairwise Hamming distance) for the first generations; if it collapses, lower the fraction or raise early mutation.

**The heuristic and the solver disagree on the start's objective.** Almost always a data or version mismatch — the constructor read a different cost matrix, an updated demand vector, or applied a rounding the model does not. Keep one independent evaluator (the `start_cost` pattern above) owned by neither the constructor nor the model code, and refuse to inject anything it does not certify.

**A partial start never completes.** Either the trusted set is too small to guide the sub-MIP or so large it strangles it. Raise `StartNodeLimit` first; if completion still fails, run your own completion with `complete_partial_start` and shrink `trusted` greedily (drop the least-certain 10% of variables per retry) until a completion exists.

**The constructor costs more than it saves.** A 60 s matheuristic-grade construction feeding a solver that needed 20 s cold is a net loss nobody notices because the two timers live in different scripts. Always report construction time and solver time in one row (format below) and compare against the cold baseline end to end, not solver-time to solver-time.

## Tools & Libraries

| Library | When to use | Note |
|---|---|---|
| gurobipy | MIP starts, hints, fixing, basis reuse | `Start`, `NumStart`/`StartNumber`, `VarHintVal`/`VarHintPri`, `LB=UB`, `VBasis`/`CBasis`, `PStart`/`DStart`, `cbSetSolution` |
| OR-Tools CP-SAT | Hinting CP models | `model.AddHint(variables, values)`; one hint per model, partial allowed |
| HiGHS (highspy) | Open-source MIP/LP warm starts | `Highs.setSolution` for MIP starts; basis via `setBasis` |
| PySCIPOpt | SCIP-based pipelines | `createPartialSol`/`addSol`; SCIP also accepts partial solutions |
| PuLP | Quick CBC models | `var.setInitialValue(v)` + solver flag `warmStart=True` |
| Pyomo | Solver-agnostic models | `solver.solve(model, warmstart=True)` with persistent Gurobi/CPLEX |
| numpy | Constructors, validators, population seeding | All constructors above are plain numpy; keep them solver-free |
| scipy.optimize | Assignment-based constructors | `linear_sum_assignment` builds strong starts for assignment-like cores |
| pandas | The cold/warm comparison table | One row per (instance, variant, seed); nothing else |

## Output Format

A complete warm-start deliverable reports four things: where the start came from, that it was independently validated, that the solver accepted it, and what it changed. Use this template:

```text
WARM-START REPORT — <model name>, <instance set>, <date>

START SOURCE   constructor: greedy_cflp (cost/capacity opening, regret assign)
               construction time: 0.04 s        validated by: start_cost()
               start objective (independent recompute): 9420.2

INJECTION      mechanism: complete MIP start (var.Start, by name)
               acceptance: "User MIP start produced solution with
               objective 9420.18" (root log line confirmed)

COMPARISON     protocol: identical TimeLimit=5 s, default params, 1 build each
               metric                      cold        warm
               time to first incumbent     0.8 s       0.0 s (start)
               incumbent @ limit           8556.1      8333.2
               final gap @ limit           5.2%        2.6%
               nodes explored              1335        1315
               construction + solve        5.0 s       5.1 s

DECISION       keep warm start: YES — better incumbent at equal budget on
               18/20 instances; revisit if instances shrink below 50 customers
```

Reporting rules. State the construction time next to the solver time, never apart. Quote the acceptance log line verbatim — it is the only proof the start was used. Report time-to-first-incumbent and incumbent-at-limit for both variants; node counts support the story but vary too much to carry it. For randomized constructors or seeded metaheuristics, repeat over at least 5 seeds and report median and range. Close with an explicit keep/drop decision and the condition that would reverse it.

## Questions to Ask

- Which direction is the transfer — heuristic into exact solver, exact into metaheuristic, or solve-to-solve in a sequence?
- Is there already a feasible solution available, and for exactly which model version and data was it feasible?
- Does the candidate cover all variables, or only some families — and which ones do you actually trust?
- What hurts today: time to first feasible, incumbent quality at the limit, or proving optimality?
- Which solver and API, and is the model object kept alive between solves or rebuilt?
- How often is the model re-solved with slightly changed data?
- How much time may the constructor itself spend, at production instance sizes?
- For population seeding: population size, available elites, and is there a decoder between genotype and solution?
- How will success be measured — same time limit, how many instances, how many seeds?
- What happened when you compared against the cold solver baseline — or has nobody run that comparison yet?

## Related Skills

- **gurobi-advanced-features** — when injection needs callbacks (`cbSetSolution`), the solution pool, MIP-start parameters like `StartNodeLimit`, or IIS-based diagnosis of rejected starts.
- **grasp** — when one deterministic constructor is not enough and you need many diverse randomized starts via restricted candidate lists.
- **matheuristics** — when partial fixing grows into fix-and-optimize, relax-and-fix, or local-branching loops that call the solver repeatedly.
- **milp-modeling-gurobi** — when the model receiving the start must first be built cleanly, with named variables and constraint-builder functions.
- **local-search-and-neighborhoods** — when constructed starts should be polished by 2-opt/insertion/exchange moves before injection or seeding.
