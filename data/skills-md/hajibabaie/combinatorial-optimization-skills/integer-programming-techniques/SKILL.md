---
name: integer-programming-techniques
description: When the user wants to diagnose and fix slow MIP solves — branch-and-bound mechanics inside modern solvers, LP relaxation strength, MIP gap interpretation, formulation tightening, symmetry breaking, big-M versus indicator constraints, and presolve effects. Also use when the user mentions "branch and bound," "MIP gap," "LP relaxation," "symmetry breaking," "tighten formulation," "big-M," or when the dual bound stalls while the incumbent stops improving. For building gurobipy models from scratch, see milp-modeling-gurobi; for implementing a custom search tree, see branch-and-bound.
---

# Integer Programming Techniques

You are an expert in computational integer programming: what a modern MIP solver
does with a model between `optimize()` and `OPTIMAL`, and how to change the model
so the solver finishes sooner. This skill covers branch-and-bound mechanics,
LP relaxation strength, MIP gap interpretation, formulation tightening,
symmetry breaking, big-M versus indicator constraints, and presolve effects.
Use the framework below to diagnose a slow solve first, then apply the one or
two levers the diagnosis actually points to.

## Initial Assessment

Establish the following before recommending any change:

- **The symptom, precisely.** "Slow" is not a diagnosis. Distinguish: (a) no
  incumbent found, (b) incumbent good but dual bound stalls, (c) both move but
  too slowly, (d) root LP itself is slow, (e) numerical warnings in the log.
- **The solve log.** Ask for it or reproduce it. The root relaxation value, the
  cut summary, the node throughput, and the gap trajectory carry most of the
  diagnostic signal. Never tune blind.
- **Problem size.** Variables (how many integer/binary), constraints, nonzeros
  — before and after presolve. A model with 10^7 nonzeros has different
  bottlenecks than one with 10^4.
- **Instance scaling.** One instance or a family? Does difficulty explode at a
  specific size? Collect 3–5 representative instances for any comparison.
- **Solver and license.** Gurobi version and parameter defaults matter;
  conclusions below assume a recent Gurobi but transfer to CPLEX/SCIP/HiGHS.
- **Time budget and gap target.** Proving optimality to 0.01% and reaching 1%
  feasible-with-certificate are different projects. Get the real requirement.
- **Hard vs soft constraints.** Soft constraints moved into the objective with
  penalty weights change relaxation strength; note which constraints are
  negotiable before tightening anything.
- **Data magnitudes.** Largest and smallest objective and constraint
  coefficients. Ratios above ~1e6 within a row or column predict numerical
  trouble and weak big-M relaxations.
- **Structural symmetry.** Identical machines, vehicles, bins, shifts, or
  facilities with equal data are a red flag for symmetric search trees.
- **Exact-vs-heuristic need.** If a proof of optimality is not required and the
  gap target is loose, a matheuristic or a warm-started truncated solve may
  beat months of formulation work; confirm the deliverable first.
- **Data format and reproducibility.** Fixed random seed, fixed `Threads`, and
  pinned solver version for any before/after claim.

## How Branch-and-Bound Actually Runs Your Model

Modern solvers run LP-based branch-and-cut (Land & Doig (1960), "An automatic
method of solving discrete programming problems"; Achterberg & Wunderling
(2013), "Mixed integer programming: Analyzing 12 years of progress"):

```text
BRANCH-AND-CUT (minimization)
  presolve the model                      # tighten bounds, drop rows/cols, probe
  L <- {root};  z_P <- +inf               # open nodes, primal bound (incumbent)
  while L not empty:
      select node k from L                # best-bound / depth-first mix
      solve LP relaxation of k  -> z_k, x_k
      if LP infeasible or z_k >= z_P:  prune k; continue
      if x_k integral:                 z_P <- z_k; update incumbent; continue
      try cutting planes at k (root: aggressively); resolve LP
      run primal heuristics from x_k      # rounding, diving, RINS, ...
      pick fractional variable x_j        # pseudocost / reliability branching
      add children k1: x_j <= floor(x_jk), k2: x_j >= ceil(x_jk) to L
  z_D <- min over open nodes of z_k       # global dual bound at any time
```

**Bounds and the MIP gap.** For a minimization MIP with feasible set
$X = P \cap (\mathbb{Z}^p \times \mathbb{R}^{n-p})$ and LP relaxation over the
polyhedron $P$:

$$ z_{LP} \;=\; \min\{c^\top x : x \in P\} \;\le\; z_D \;\le\; z^* \;\le\; z_P $$

The solver reports `ObjVal` ($z_P$, incumbent), `ObjBound` ($z_D$, proven dual
bound), and

$$ \text{MIPGap} \;=\; \frac{|z_P - z_D|}{|z_P|}. $$

Gurobi stops at MIPGap ≤ 1e-4 by default. A 1% gap means the incumbent is
*proven* within 1% of optimal — it says nothing about which side is weak. The
log tells you: if the incumbent column froze long ago, the dual bound is the
laggard (formulation problem); if the bound is near-final but the incumbent is
poor, it is a primal-heuristic problem (see **warm-starts-and-initial-solutions**).

**Formulation strength.** Two formulations with polyhedra $P_1, P_2$ and the
same integer feasible set $X$ are ranked by inclusion. The ideal formulation is
$\operatorname{conv}(X)$, where the LP optimum is already integral:

$$ \operatorname{conv}(X) \;\subseteq\; P_1 \;\subseteq\; P_2
   \;\Longrightarrow\; z_{LP}(P_1) \;\ge\; z_{LP}(P_2) \quad (\text{minimization}). $$

A node is pruned as soon as its LP bound reaches $z_P$; a tighter $P$ raises
every node bound, so the pruned region of the tree grows. This is why
formulation strength, not constraint count, predicts solve time (Wolsey (1998),
*Integer Programming*; Vielma (2015), "Mixed integer linear programming
formulation techniques").

**The levers and what each one moves:**

| Lever | Raises root bound | Shrinks tree | Main cost |
|---|---|---|---|
| Disaggregate implications | yes | yes | more rows, slower node LP |
| Tight big-M from data | yes | yes | bound analysis per constraint |
| Valid inequalities / cuts | yes | yes | separation effort |
| Symmetry breaking | rarely | yes, on symmetric trees | can clash with heuristics |
| Branching priorities | no | often | needs domain insight |
| MIP start / better heuristics | no (primal side) | yes, earlier pruning | cheap |
| Presolve level (0/1/2) | sometimes | usually | rarely hurts; test it |

**Decision guidance:**

- Use **disaggregation** when one aggregated row encodes many independent
  implications (the facility-location example below is the canonical case).
- Use a **tight big-M** when a valid $M$ follows from variable bounds or data
  (remaining demand, capacity); use an **indicator constraint** when no
  reasonable $M$ exists or when $M \ge 10^6$ forces numerical trouble.
- Use **symmetry breaking** only after confirming symmetry (equal-data
  resources) and only one scheme at a time; benchmark against the solver's own
  `Symmetry=2` handling.
- Treat **presolve** as part of the formulation: always compare formulations
  both with `Presolve=0` (raw strength) and default (what the solver sees).

## Diagnostic Toolkit: Measure Before You Tighten

The reusable workflow. Every tightening claim must be backed by these numbers,
not by intuition:

```text
TIGHTEN-AND-DIAGNOSE WORKFLOW (minimization)
1. Solve the pure LP relaxation (model.relax())            -> z_LP
2. Solve the MIP with a short time limit                   -> z_P, z_D, gap, nodes
3. LP integrality gap = (z_P - z_LP) / z_P
   - large (> ~5%): the formulation is the problem ->
       disaggregate, shrink big-M, add valid inequalities
   - small, but the tree is huge: suspect symmetry or weak branching ->
       break symmetry, set branching priorities
   - small and tree small, but nodes are slow: node LP cost is the problem ->
       prefer the smaller formulation, move dense rows to lazy constraints
4. Re-run with fixed Seed; repeat on >= 3 instances and >= 3 seeds
   before declaring a winner (performance variability is real).
```

```python
import gurobipy as gp
from gurobipy import GRB


def lp_relaxation_bound(model: gp.Model) -> float:
    """Solve the pure LP relaxation of a MIP and return its objective value.

    Caveat: Model.relax() drops integrality AND general constraints
    (indicator, SOS, min/max). For indicator-based models measure the root
    bound from the solve log instead.
    """
    relaxed = model.relax()
    relaxed.Params.OutputFlag = 0
    relaxed.optimize()
    if relaxed.Status != GRB.OPTIMAL:
        raise RuntimeError(f"LP relaxation ended with status {relaxed.Status}")
    return relaxed.ObjVal


def solve_and_report(model: gp.Model, time_limit: float = 60.0) -> dict[str, float]:
    """Solve a MIP and report the numbers that matter for formulation diagnosis."""
    z_lp = lp_relaxation_bound(model)
    model.Params.OutputFlag = 0
    model.Params.TimeLimit = time_limit
    model.Params.Seed = 0  # fix the seed whenever you compare formulations
    model.optimize()
    usable = model.Status == GRB.OPTIMAL or (
        model.Status == GRB.TIME_LIMIT and model.SolCount > 0
    )
    if not usable:
        raise RuntimeError(f"no usable solution: status {model.Status}")
    z_inc = model.ObjVal      # primal bound (incumbent)
    z_dual = model.ObjBound   # dual bound (proven)
    return {
        "lp_relaxation": z_lp,
        "incumbent": z_inc,
        "dual_bound": z_dual,
        "mip_gap": model.MIPGap,
        "lp_integrality_gap": abs(z_inc - z_lp) / max(abs(z_inc), 1e-9),
        "nodes": model.NodeCount,
        "runtime_s": model.Runtime,
    }


# Tiny demo: a 4-item 0-1 knapsack whose LP optimum is fractional.
demo = gp.Model("knapsack_demo")
x = demo.addVars(4, vtype=GRB.BINARY, name="pick")
value = [8.0, 11.0, 6.0, 4.0]
weight = [5.0, 7.0, 4.0, 3.0]
demo.addConstr(gp.quicksum(weight[i] * x[i] for i in range(4)) <= 14, name="cap")
demo.setObjective(gp.quicksum(value[i] * x[i] for i in range(4)), GRB.MAXIMIZE)
print({k: round(v, 4) for k, v in solve_and_report(demo).items()})
# Expected: lp_relaxation 22.0, incumbent 21.0 (items 2,3,4), mip_gap 0.0,
# lp_integrality_gap ~0.0476 -- a 4.8% root gap that branching must close.
```

The comparison harness solves the same instance under several formulations and
returns one tidy row per model:

```python
from collections.abc import Callable

import gurobipy as gp
import pandas as pd
from gurobipy import GRB


def compare_formulations(
    builders: dict[str, Callable[[], gp.Model]],
    time_limit: float = 120.0,
    presolve: int = -1,
) -> pd.DataFrame:
    """Solve one instance under several formulations; one result row per model.

    presolve=0 exposes raw formulation strength; presolve=-1 (solver default)
    shows what branch-and-bound actually works with. Report both.
    """
    rows = []
    for label, build in builders.items():
        mip = build()
        relaxed = mip.relax()
        relaxed.Params.OutputFlag = 0
        relaxed.optimize()
        z_lp = relaxed.ObjVal if relaxed.Status == GRB.OPTIMAL else float("nan")

        mip.Params.OutputFlag = 0
        mip.Params.TimeLimit = time_limit
        mip.Params.Presolve = presolve
        mip.Params.Seed = 0
        mip.optimize()
        has_sol = mip.SolCount > 0
        rows.append(
            {
                "formulation": label,
                "rows": mip.NumConstrs,
                "lp_bound": round(z_lp, 2),
                "objective": round(mip.ObjVal, 2) if has_sol else float("nan"),
                "dual_bound": round(mip.ObjBound, 2),
                "mip_gap_pct": round(100 * mip.MIPGap, 3) if has_sol else float("inf"),
                "nodes": int(mip.NodeCount),
                "runtime_s": round(mip.Runtime, 2),
            }
        )
    return pd.DataFrame(rows).set_index("formulation")
```

## Worked Example 1: Facility Location, Weak vs Strong Linking

The uncapacitated facility location problem (UFLP) is the canonical
demonstration that two formulations with identical integer solutions can have
wildly different LP relaxations (Cornuéjols, Nemhauser & Wolsey (1990), "The
uncapacitated facility location problem").

Customers $i \in I$ ($|I| = m$), candidate sites $j \in J$ ($|J| = n$), fixed
opening cost $f_j$, assignment cost $c_{ij}$:

$$ \min \sum_{j} f_j y_j + \sum_{i}\sum_{j} c_{ij} x_{ij}
   \quad \text{s.t.} \quad \sum_j x_{ij} = 1 \;\; \forall i, \qquad
   y_j \in \{0,1\}, \; x_{ij} \in [0,1] $$

($x$ may stay continuous: once the open set is fixed, assigning each customer
to its cheapest open site is automatically integral.) The linking constraints
come in two algebraically equivalent flavors:

- **Weak (aggregated), $n$ rows:** $\sum_i x_{ij} \le m \, y_j \;\; \forall j$
- **Strong (disaggregated), $mn$ rows:** $x_{ij} \le y_j \;\; \forall i, j$

Summing the strong rows over $i$ yields the weak row, so
$P_{\text{strong}} \subseteq P_{\text{weak}}$. The converse fails badly: the
weak LP sets $y_j = \frac{1}{m}\sum_i x_{ij}$, opening every attractive site at
level $\approx 1/m$ and paying almost no fixed cost. Its bound collapses toward
the pure assignment cost. The strong LP forces $y_j \ge \max_i x_{ij}$ and is
frequently integral or near-integral in practice.

```python
import gurobipy as gp
import numpy as np
from gurobipy import GRB


def make_uflp_instance(n_customers: int, n_sites: int, seed: int = 0) -> dict:
    """Random UFLP on a 100x100 square: Euclidean assignment costs, fixed costs."""
    rng = np.random.default_rng(seed)
    customers = rng.uniform(0.0, 100.0, size=(n_customers, 2))
    sites = rng.uniform(0.0, 100.0, size=(n_sites, 2))
    c = np.linalg.norm(customers[:, None, :] - sites[None, :, :], axis=2)
    f = rng.uniform(400.0, 900.0, size=n_sites)
    return {"c": c, "f": f, "m": n_customers, "n": n_sites}


def build_uflp(data: dict, linking: str) -> gp.Model:
    """UFLP MIP. linking='weak' aggregates one row per site; 'strong' disaggregates."""
    m, n, c, f = data["m"], data["n"], data["c"], data["f"]
    model = gp.Model(f"uflp_{linking}")
    y = model.addVars(n, vtype=GRB.BINARY, name="open")
    x = model.addVars(m, n, lb=0.0, ub=1.0, name="assign")
    model.addConstrs((x.sum(i, "*") == 1 for i in range(m)), name="serve")
    if linking == "weak":
        model.addConstrs(
            (gp.quicksum(x[i, j] for i in range(m)) <= m * y[j] for j in range(n)),
            name="link_agg",
        )
    elif linking == "strong":
        model.addConstrs(
            (x[i, j] <= y[j] for i in range(m) for j in range(n)),
            name="link_dis",
        )
    else:
        raise ValueError(f"unknown linking mode {linking!r}")
    model.setObjective(
        gp.quicksum(f[j] * y[j] for j in range(n))
        + gp.quicksum(c[i, j] * x[i, j] for i in range(m) for j in range(n)),
        GRB.MINIMIZE,
    )
    return model
```

Run the comparison twice — once with presolve off to see raw strength, once
with defaults to see how much presolve repairs:

```python
# make_uflp_instance, build_uflp: defined in the block above.
# compare_formulations: defined in the diagnostic-toolkit section.
data = make_uflp_instance(n_customers=40, n_sites=15, seed=7)
for presolve in (0, -1):
    table = compare_formulations(
        {
            "weak_aggregated": lambda: build_uflp(data, "weak"),
            "strong_disaggregated": lambda: build_uflp(data, "strong"),
        },
        time_limit=120.0,
        presolve=presolve,
    )
    print(f"\nPresolve={presolve}")
    print(table)
# Expected: identical 'objective' in both rows (same integer optimum). With
# Presolve=0 the strong LP bound lands within ~1-2% of the optimum while the
# weak LP bound is far lower (the LP opens sites at y_j ~ 1/40 and pays almost
# no fixed cost); the weak model needs orders of magnitude more nodes. With
# default presolve the difference shrinks (probing derives some x<=y
# implications) but the strong model still dominates.
```

The general lesson: whenever one row says "if the aggregate is positive then
the switch is on," ask whether it is really $m$ separate implications
"$x_{ij} > 0 \Rightarrow y_j = 1$" — and write those directly. The strong model
pays with $mn$ rows; for very large instances add the disaggregated rows as
lazy constraints or user cuts instead (see
**cutting-planes-valid-inequalities**).

## Worked Example 2: Symmetry-Broken Parallel-Machine Scheduling

Makespan minimization on identical parallel machines ($P||C_{\max}$): jobs
$j = 1..n$ with processing times $p_j$, machines $k = 1..K$ with no
distinguishing data.

$$ \min \; C_{\max} \quad \text{s.t.} \quad
   \sum_{k} x_{jk} = 1 \;\forall j, \qquad
   \sum_{j} p_j x_{jk} \le C_{\max} \;\forall k, \qquad
   x_{jk} \in \{0,1\} $$

Any permutation of the machine indices maps a feasible solution to another one
with the same makespan: the symmetry group is $S_K$, so every solution lives in
an orbit of up to $K!$ copies. Plain branch-and-bound re-proves the same dual
bound in each copy's subtree (Margot (2010), "Symmetry in integer linear
programming"; Sherali & Smith (2001), "Improving discrete model representations
via symmetry considerations"). Two valid single-scheme remedies:

- **Load ordering:** $\sum_j p_j x_{j,k} \ge \sum_j p_j x_{j,k+1}$ for
  $k = 1..K{-}1$. Valid because every solution has a machine-sorted
  representative.
- **Job-index rule:** $x_{jk} = 0$ for all $k > j$ (jobs indexed from 1).
  Valid because machines can be relabeled in order of the smallest job index
  they host: job 1's machine becomes machine 1, the machine of the smallest
  job not on machine 1 becomes machine 2, and so on. Implement by fixing
  variable bounds, not by adding rows — presolve then deletes the variables.

Symmetry breaking barely moves the root bound — the LP already splits jobs
fractionally and achieves $z_{LP} = \max\{\sum_j p_j / K,\; \max_j p_j\}$ once
the valid inequality $C_{\max} \ge \max_j p_j$ is added (valid because some
machine carries that job entirely; not implied by the rest of the LP). The
payoff is a smaller tree, not a better bound.

```python
import gurobipy as gp
import numpy as np
from gurobipy import GRB


def make_pmcmax_instance(n_jobs: int, n_machines: int, seed: int = 0) -> dict:
    """Random identical-parallel-machine instance with integer processing times."""
    rng = np.random.default_rng(seed)
    p = rng.integers(5, 50, size=n_jobs).astype(float)
    return {"p": p, "n": n_jobs, "k": n_machines}


def build_pmcmax(data: dict, symmetry: str) -> gp.Model:
    """P||Cmax assignment model. symmetry in {'none', 'load_order', 'job_index'}."""
    n, k, p = data["n"], data["k"], data["p"]
    model = gp.Model(f"pmcmax_{symmetry}")
    x = model.addVars(n, k, vtype=GRB.BINARY, name="assign")
    cmax = model.addVar(lb=0.0, name="makespan")
    model.addConstrs((x.sum(j, "*") == 1 for j in range(n)), name="one_machine")
    load = {h: gp.quicksum(p[j] * x[j, h] for j in range(n)) for h in range(k)}
    model.addConstrs((load[h] <= cmax for h in range(k)), name="makespan_def")
    model.addConstr(cmax >= float(p.max()), name="longest_job")  # free tightening
    if symmetry == "load_order":
        model.addConstrs(
            (load[h] >= load[h + 1] for h in range(k - 1)), name="sym_load"
        )
    elif symmetry == "job_index":
        for j in range(k - 1):           # job j may only use machines 0..j
            for h in range(j + 1, k):
                x[j, h].UB = 0.0         # fix the bound; do not add a row
    elif symmetry != "none":
        raise ValueError(f"unknown symmetry mode {symmetry!r}")
    model.setObjective(cmax, GRB.MINIMIZE)
    return model
```

Benchmark the schemes against each other *and* against the solver's internal
symmetry detection. Turn the internal handling off (`Symmetry=0`) to measure
what your constraints contribute, then let `Symmetry=2` compete:

```python
# make_pmcmax_instance, build_pmcmax: defined in the block above.
data = make_pmcmax_instance(n_jobs=15, n_machines=5, seed=4)

configs = [
    ("none + solver sym off", "none", 0),
    ("load_order + solver sym off", "load_order", 0),
    ("job_index + solver sym off", "job_index", 0),
    ("none + solver sym aggressive", "none", 2),
]
for label, mode, sym_param in configs:
    model = build_pmcmax(data, mode)
    model.Params.OutputFlag = 0
    model.Params.TimeLimit = 60
    model.Params.Symmetry = sym_param
    model.Params.Seed = 0
    model.optimize()
    if model.Status not in (GRB.OPTIMAL, GRB.TIME_LIMIT) or model.SolCount == 0:
        raise RuntimeError(f"{label}: status {model.Status}")
    print(
        f"{label:30s} makespan={model.ObjVal:6.1f} "
        f"nodes={int(model.NodeCount):8d} time={model.Runtime:6.2f}s"
    )
# Expected: all four configurations agree on the optimal makespan. With the
# solver's symmetry handling off, 'none' explores the largest tree; both
# breaking schemes cut node counts substantially (often 5-50x on this size).
# 'none + Symmetry=2' is usually competitive with the hand-written schemes --
# always measure before shipping symmetry constraints.
```

The same pattern applies to identical bins, vehicles, shifts, and any model
with interchangeable resource indices. The constraints must select exactly one
representative per orbit; selecting zero (over-breaking) makes the model
infeasible or suboptimal — see Practical Challenges for the classic mistake of
stacking two schemes.

## Big-M versus Indicator Constraints

The implication $y = 0 \Rightarrow x = 0$ with $x \in [0, U]$ is usually
written $x \le M y$. In the LP relaxation this permits $y = x / M$, so the
fixed cost attached to $y$ enters the bound at the rate $f/M$ per unit of $x$ —
the bound deteriorates linearly as $M$ grows (Camm, Raturi & Tsubakitani
(1990), "Cutting big M down to size"). Two distinct failure modes:

1. **Weak relaxation:** $M \gg U$ makes the root bound useless.
2. **Trickle flow:** with the default integrality tolerance `IntFeasTol=1e-5`,
   $y = 10^{-5}$ counts as integral 0, yet allows $x \le M \cdot 10^{-5}$ — with
   $M = 10^6$ that is 10 "free" units. The solver returns an incumbent that
   violates the business logic (Klotz & Newman (2013), "Practical guidelines
   for solving difficult mixed integer linear programs").

The fixes, in order of preference: derive the tightest valid $M$ from data
(here: remaining demand), or hand the implication to the solver as an
indicator constraint and let it derive its own reformulation. Indicators add
no relaxation strength of their own — `Model.relax()` deletes them entirely —
but they are numerically safe when no reasonable $M$ exists.

```python
import gurobipy as gp
import numpy as np
from gurobipy import GRB


def build_fixed_charge(d: list[float], mode: str) -> gp.Model:
    """Single-item fixed-charge production model; mode in {'loose','tight','indicator'}."""
    T = len(d)
    setup_cost, unit_cost, hold_cost = 90.0, 1.0, 2.0
    model = gp.Model(f"fixed_charge_{mode}")
    x = model.addVars(T, lb=0.0, name="produce")
    s = model.addVars(T, lb=0.0, name="stock")
    y = model.addVars(T, vtype=GRB.BINARY, name="setup")
    model.addConstrs(
        ((s[t - 1] if t else 0.0) + x[t] == d[t] + s[t] for t in range(T)),
        name="balance",
    )
    if mode == "loose":
        model.addConstrs((x[t] <= 1e6 * y[t] for t in range(T)), name="link")
    elif mode == "tight":
        rem = np.cumsum(np.asarray(d)[::-1])[::-1]  # demand from t to horizon end
        model.addConstrs((x[t] <= float(rem[t]) * y[t] for t in range(T)), name="link")
    elif mode == "indicator":
        for t in range(T):
            model.addGenConstrIndicator(y[t], 0, x[t] == 0.0, name=f"link[{t}]")
    else:
        raise ValueError(f"unknown mode {mode!r}")
    model.setObjective(
        gp.quicksum(setup_cost * y[t] + unit_cost * x[t] + hold_cost * s[t]
                    for t in range(T)),
        GRB.MINIMIZE,
    )
    return model


d = [40.0, 0.0, 70.0, 10.0, 0.0, 60.0, 30.0, 0.0, 25.0, 50.0]
for mode in ("loose", "tight", "indicator"):
    mip = build_fixed_charge(d, mode)
    relaxed = mip.relax()
    relaxed.Params.OutputFlag = 0
    relaxed.optimize()
    mip.Params.OutputFlag = 0
    mip.optimize()
    if mip.Status != GRB.OPTIMAL:
        raise RuntimeError(f"{mode}: status {mip.Status}")
    print(
        f"{mode:9s} lp_bound={relaxed.ObjVal:8.1f} "
        f"optimum={mip.ObjVal:8.1f} nodes={int(mip.NodeCount)}"
    )
# Expected: all three modes report the same optimal cost. 'tight' shows the
# highest LP bound; 'loose' pays almost no setup cost in the LP (y_t ~ 1e-7).
# 'indicator' looks weakest here only because relax() deletes general
# constraints -- judge indicator models by the root bound in the solve log.
```

Rule of thumb: if you can state a valid $M$ at most one or two orders of
magnitude above the variable's realistic range, the tight big-M wins (cuts and
MIR procedures exploit it). If $M$ would exceed ~$10^6$ relative to row
coefficients, switch to indicators or rescale units. For products of variables
and other constructs that *generate* big-M rows, see
**linearization-techniques**.

## Advanced Techniques

### Reading the log: which side of the gap is stuck

Open the node log and track three columns over time: incumbent, best bound,
gap. Compute where the gap would be if only the bound had improved, and where
if only the incumbent had. The stalled side gets the work. Bound stalls with
fractional LPs at deep nodes point to formulation strength (this skill); bound
stalls with near-integral LPs point to symmetry or degeneracy; incumbent stalls
call for MIP starts and heuristic emphasis (`Heuristics`, `RINS`) — see
**warm-starts-and-initial-solutions**. Also watch the cut summary at the root:
if Gurobi adds hundreds of implied-bound or flow-cover cuts, it is mechanically
disaggregating what the model could have stated directly.

### Presolve forensics

Presolve performs bound strengthening, coefficient reduction, probing, clique
merging, substitution, and more (Achterberg, Bixby, Gu, Rothberg & Weninger
(2020), "Presolve reductions in mixed integer programming"). Inspect what it
does to your model rather than guessing:

```python
import gurobipy as gp
from gurobipy import GRB

# make_uflp_instance, build_uflp: defined in the facility-location example.
data = make_uflp_instance(n_customers=40, n_sites=15, seed=7)

weak = build_uflp(data, "weak")
weak.Params.OutputFlag = 0
pre = weak.presolve()
print(f"original : {weak.NumVars} vars, {weak.NumConstrs} rows, {weak.NumNZs} nz")
print(f"presolved: {pre.NumVars} vars, {pre.NumConstrs} rows, {pre.NumNZs} nz")

for level in (0, 1, 2):
    model = build_uflp(data, "weak")
    model.Params.OutputFlag = 0
    model.Params.Presolve = level
    model.Params.TimeLimit = 60
    model.optimize()
    print(
        f"Presolve={level}: nodes={int(model.NodeCount):8d} "
        f"gap={100 * model.MIPGap:.3f}% time={model.Runtime:.1f}s"
    )
# Expected: presolve shrinks the model and recovers part of the weak/strong
# difference via probing, but the explicitly strong formulation still wins.
# Never rely on presolve to repair a weak model you could have written tightly.
```

When a model is reported infeasible only with presolve on (or vice versa),
set `DualReductions=0` to separate INFEASIBLE from UNBOUNDED, then bisect with
`Presolve=0/1/2` — and suspect your own big-M values before suspecting the solver.

### Branching priorities and strategic variables

Solvers pick branching variables by pseudocost and reliability estimates
(Achterberg, Koch & Martin (2005), "Branching rules revisited"), which need
history to become good. When the model has a clear design/operations split —
open facilities then assign customers, buy machines then schedule jobs — tell
the solver to decide the design first:

```python
import gurobipy as gp


def prioritize(model: gp.Model, prefix: str, priority: int = 10) -> int:
    """Raise BranchPriority for every variable whose name starts with prefix."""
    touched = 0
    for v in model.getVars():
        if v.VarName.startswith(prefix):
            v.BranchPriority = priority
            touched += 1
    return touched


# make_uflp_instance, build_uflp: defined in the facility-location example.
model = build_uflp(make_uflp_instance(40, 15, seed=7), "strong")
n_set = prioritize(model, "open")  # branch on facility-open before assignment
model.Params.OutputFlag = 0
model.optimize()
print(n_set, int(model.NodeCount))
# Expected: 15 variables prioritized. Fixing the y_j design variables first
# typically shrinks the tree: once the open set is decided, the assignment
# subproblem is an easy (often integral) LP.
```

### Constraint-based vs solver-internal symmetry handling

Hand-written symmetry constraints are static; solver-internal techniques —
orbital fixing and orbital branching (Ostrowski, Linderoth, Rossi & Smriglio
(2011), "Orbital branching") — act dynamically on the symmetry group that
survives at each node and never remove the orbit representative the heuristics
would have found. In Gurobi this is `Symmetry` (-1 auto, 0 off, 2 aggressive).
Practical protocol: detect symmetry structurally (equal-data resources),
benchmark `{no constraints, scheme A, scheme B} × {Symmetry=0, default, 2}`,
and keep the cheapest winner. Hand-written schemes tend to win when the
symmetry is total and known (identical machines); the solver tends to win on
partial or hidden symmetry. Never ship both a strong hand-written scheme and
`Symmetry=2` without testing — they can interact badly with MIP starts, which
must satisfy the symmetry-breaking rows to be accepted.

## Practical Challenges

**The gap stalls at 2% for hours.** Read the log before touching anything. If
`ObjBound` froze: compute the LP integrality gap with `model.relax()`; if it is
large, the formulation is weak — disaggregate, tighten big-M, add valid
inequalities. If the pure LP bound is already close to the incumbent but nodes
keep multiplying, suspect symmetry or massive dual degeneracy instead. If
`ObjVal` froze: feed a MIP start, raise `Heuristics`, or accept the gap.

**Symmetry constraints made the solve slower.** Common and well documented.
The constraints may fight the solver's internal orbital methods, cut off the
representative its heuristics find first, or reject your MIP start. Re-test
with `Symmetry=0` to isolate the constraints' true effect, and keep exactly
one mechanism — yours or the solver's.

**Two stacked symmetry-breaking schemes cut off every optimum.** Each scheme
selects one representative per orbit, but different schemes select *different*
representatives; their intersection can be empty. Concrete failure on
$P||C_{\max}$ with $K=2$, $p=(1,5)$: the job-index rule forces job 1 onto
machine 1, load ordering forces machine 1 to carry at least as much load —
together they only admit both jobs on machine 1, makespan 6 instead of the
optimal 5. Never combine schemes without a proof that one representative
satisfies both.

**Trickle flow: setups are off but flow is positive.** A binary at $10^{-5}$
passes `IntFeasTol` as 0, and $x \le M y$ with huge $M$ then admits real flow.
Detect it by validating incumbents with an independent checker; fix it by
tightening $M$, lowering `IntFeasTol`, or moving to indicator constraints.

**Presolve masks the formulation comparison.** With default settings, probing
can partially disaggregate a weak model, so two formulations look closer than
they are; conclusions then silently depend on the solver version. Always report
strength comparisons at `Presolve=0` *and* default, and state the version.

**The strong formulation is too big to build.** $mn$ disaggregated rows at
$m = n = 5000$ is $2.5 \times 10^7$ rows. Options: add them lazily via a
callback when violated (see **cutting-planes-valid-inequalities**), keep the
weak rows and let cut separation work, or build the strong model only for the
subproblems of a decomposition.

**Run-to-run variance swamps the measured improvement.** MIP performance is
chaotic: changing `Seed` alone can shift runtime by 2-5x. Declare a formulation
better only after multiple seeds and instances — paired comparisons,
geometric-mean speedups, and the protocols of Achterberg & Wunderling (2013).

**The model is infeasible and nobody knows why.** Compute an irreducible
infeasible subsystem (`model.computeIIS()`), write it out, and read the
conflicting named constraints. Constraint names from disciplined builders (one
name per family, indexed) turn the IIS from noise into a diagnosis. Suspect
over-tight big-M values and over-aggressive symmetry rows first.

## Tools & Libraries

| Library / tool | When to use | Note |
|---|---|---|
| gurobipy | Primary modeling and solving layer assumed throughout this skill | Attributes `ObjBound`, `MIPGap`, `NodeCount` drive every diagnosis |
| PySCIPOpt (SCIP) | Research access to B&B internals: custom branching rules, event handlers, separators | Free for academic use; the reference open branch-and-cut framework |
| HiGHS (`highspy`) | License-free LP/MIP for relaxation-strength studies and CI tests | Strong LP performance; MIP solid but behind Gurobi on hard instances |
| OR-Tools CP-SAT | When the MIP gap will not close and the model is scheduling- or feasibility-heavy | Different proof system; often wins on disjunctive scheduling |
| MIPLIB 2017 | Reference instance set for benchmarking and regression-testing solver settings | Use the curated "benchmark" subset; report shifted geometric means |
| `grbtune` (Gurobi tuning tool) | Parameter search after formulation work is finished, never before | Tune on several instances; beware overfitting to one seed |
| pandas | Result tables for formulation comparisons (one row per model/seed/instance) | Pairs with the `compare_formulations` harness above |

## Output Format

A complete formulation-diagnosis deliverable contains:

1. **Symptom statement and log evidence.** One paragraph: which bound stalled,
   root relaxation value, cut summary, node throughput.
2. **Model summary table.** Per formulation: binaries, continuous variables,
   rows, nonzeros — before and after presolve.
3. **Strength comparison table** (the harness output), at `Presolve=0` and
   default, with fixed `Seed` and identical `TimeLimit`:

   | formulation | rows | lp_bound | objective | dual_bound | mip_gap_pct | nodes | runtime_s |
   |---|---|---|---|---|---|---|---|
   | weak_aggregated | 55 | 9166.2 | 11423.7 | 11423.7 | 0.0 | 38114 | 41.20 |
   | strong_disaggregated | 640 | 11298.5 | 11423.7 | 11423.7 | 0.0 | 87 | 1.95 |

4. **Cross-seed robustness.** The same comparison over >= 3 seeds and >= 3
   instances; report geometric-mean runtime ratio and worst case, not a single
   lucky run.
5. **Recommendation list, ordered by expected payoff.** Each item names the
   lever (disaggregation, big-M tightening, symmetry scheme, branching
   priority, parameter), the evidence row that justifies it, and its cost.
6. **Reproducibility block.** Solver version, `Seed`, `Threads`, `TimeLimit`,
   `MIPGap` target, hardware, instance files or generator seeds.
7. **Validation note.** Confirmation that an independent feasibility checker
   accepts the incumbent of every formulation variant (this catches trickle
   flow and over-broken symmetry immediately).

## Questions to Ask

- Can you share the solve log, or at least the root relaxation value and the
  final incumbent/bound pair?
- Which side stopped moving first — the incumbent or the best bound?
- How large is the model before and after presolve (variables, rows, nonzeros)?
- Are there interchangeable resources (identical machines, vehicles, bins,
  shifts) anywhere in the model?
- Where do the big-M constants come from, and what is the largest one relative
  to typical variable values?
- What gap is actually acceptable for the decision being made, and what is the
  wall-clock budget?
- Is this a one-off solve or a recurring production run (how much engineering
  is a 10x speedup worth)?
- Do results need to be reproducible across solver versions and seeds for a
  paper or audit?

## Related Skills

Hand off when the question shifts from tightening an existing model:

- **milp-modeling-gurobi** — when the model itself still needs to be built or
  restructured in gurobipy; this skill assumes a working model and makes it solve faster.
- **branch-and-bound** — when a custom tree search outside a MIP solver is the
  right tool: problem-specific bounds, dominance rules, or no solver license.
- **cutting-planes-valid-inequalities** — when tightening should come from added
  inequalities: cover, clique, MIR, subtour cuts, and separation via callbacks.
- **linearization-techniques** — when nonlinear constructs (products, absolute
  values, piecewise costs) must become linear before any tightening question arises.
- **warm-starts-and-initial-solutions** — when the primal side is the bottleneck:
  MIP starts and construction heuristics so the incumbent stops being the weak end of the gap.
