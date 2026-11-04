---
name: lot-sizing
description: When the user wants to model and solve dynamic lot-sizing problems, from uncapacitated single-item lot sizing to multi-item capacitated lot sizing (CLSP) with setup times, covering Wagner-Whitin DP, facility-location reformulation, (l,S) valid inequalities, big-bucket vs small-bucket models, and fix-and-optimize. Also use when the user mentions "lot sizing," "Wagner-Whitin," "setup costs," "CLSP," "production planning periods," or a setup-vs-holding cost trade-off over a discrete horizon. For DP recursion design, see dynamic-programming; for MIP-based improvement loops, see matheuristics.
---

# Lot Sizing

You are an expert in dynamic lot-sizing models for production planning. This skill covers the uncapacitated single-item problem (ULS) solved exactly by the Wagner-Whitin dynamic program, the multi-item capacitated lot-sizing problem (CLSP) with setup costs and setup times, strong reformulations (facility-location, (l,S) valid inequalities), the big-bucket vs small-bucket model families, and fix-and-optimize matheuristics for large instances. Use the framework below to classify the variant, pick the right formulation strength, and deliver a validated production plan with a defensible optimality gap.

## Initial Assessment

Establish these facts before formulating anything:

- **Capacity.** Is per-period production capacity binding? Uncapacitated single-item problems are polynomially solvable; capacity makes even the single-item case NP-hard.
- **Number of items and periods.** N items × T periods sets the binary count (N·T setup variables). N·T ≤ a few thousand is comfortable MIP territory; beyond that plan for matheuristics.
- **Bucket size.** Are periods long (weeks/months, many setups per period — big bucket) or short (shifts/hours, at most one or two products per period — small bucket)? This decides the model family before any code is written.
- **Setup structure.** Setup costs only, or also setup times that consume capacity? Setup times change the complexity class of the feasibility question. Ask about setup carryover across periods and sequence-dependent setups.
- **Cost structure.** Time-varying or constant setup/holding/production costs? Constant unit production cost can be dropped from the objective (total production equals total demand when backlog is forbidden).
- **Backlogging and lost sales.** Hard demand satisfaction, backlog at a cost, or lost sales? This changes the flow-balance constraints and the validity of zero-inventory-ordering arguments.
- **Lot-size restrictions.** Minimum lot sizes, batch multiples, or all-or-nothing production invalidate the Wagner-Whitin structure and need extra integer variables.
- **Demand certainty.** Deterministic forecast, or stochastic demand needing safety stock / scenario models? A deterministic model re-solved in a rolling horizon is the common practical pattern.
- **Horizon usage.** One-shot plan or rolling horizon? Rolling horizons need end-of-horizon inventory rules and frozen periods to control nervousness.
- **Quality requirement and time budget.** Proven optimality (MIP with strong formulation), small gap in minutes (matheuristic), or instant answer (DP / construction heuristic)?
- **Solver availability.** Gurobi license, or open-source only? The DP and the metaheuristic below need only numpy; the MIP sections need a MILP solver.
- **Data format.** Demand matrix orientation (items × periods), units of capacity (hours vs pieces), and whether quantities must be integral (usually production quantities may stay continuous).

## Problem Variants and Formulations

### Notation

Items $i = 1,\dots,N$; periods $t = 1,\dots,T$. Data: demand $d_{it} \ge 0$, setup cost $f_i$, holding cost $h_i$ per unit per period, processing time $a_i$ capacity units per unit, setup time $st_i$, capacity $C_t$. Variables: production $x_{it} \ge 0$, end-of-period inventory $s_{it} \ge 0$ (with $s_{i0} = 0$), setup indicator $y_{it} \in \{0,1\}$.

### ULS — uncapacitated single-item lot sizing

$$
\min \sum_{t=1}^{T} \big( f_t\, y_t + h_t\, s_t \big)
\quad \text{s.t.} \quad
s_{t-1} + x_t = d_t + s_t,\qquad
x_t \le \Big(\sum_{u=t}^{T} d_u\Big)\, y_t,\qquad
x_t, s_t \ge 0,\; y_t \in \{0,1\}.
$$

**Zero-inventory ordering (ZIO).** Wagner & Whitin (1958) proved an optimal solution exists with $s_{t-1}\, x_t = 0$ for all $t$: you never produce while still holding stock. So each demand $d_u$ is produced entirely in one period $t \le u$, and the horizon splits into regeneration intervals. This yields an $O(T^2)$ dynamic program; refinements reach $O(T \log T)$ (Federgruen & Tzur 1991; Wagelmans, van Hoesel & Kolen 1992; Aggarwal & Park 1993). ULS is the textbook entry point of **dynamic-programming** for planning problems.

### CLSP — capacitated multi-item, big bucket

$$
\min \sum_{i=1}^{N}\sum_{t=1}^{T} \big( f_i\, y_{it} + h_i\, s_{it} \big)
$$

$$
s_{i,t-1} + x_{it} = d_{it} + s_{it} \;\;\forall i,t; \qquad
\sum_{i=1}^{N} \big( a_i\, x_{it} + st_i\, y_{it} \big) \le C_t \;\;\forall t; \qquad
x_{it} \le M_{it}\, y_{it} \;\;\forall i,t,
$$

with the tightest valid big-M $M_{it} = \min\big( \sum_{u \ge t} d_{iu},\; (C_t - st_i)/a_i \big)$.

**Complexity.** Single-item lot sizing with general time-varying capacities is NP-hard (Florian, Lenstra & Rinnooy Kan 1980; Bitran & Yanasse 1982); with constant capacity and integer data it admits an $O(T^4)$ DP (Florian & Klein 1971). For the multi-item CLSP with positive setup times, even deciding feasibility is NP-complete (Maes, McClain & Van Wassenhove 1991) — that is why practical codes add overtime variables.

### Big-bucket vs small-bucket model families

| Model | Bucket | Per-period structure | Sequencing | Key reference |
|-------|--------|----------------------|------------|---------------|
| CLSP | big | many items, one setup each | none inside period | Trigeiro, Thomas & McClain (1989) |
| CLSPL | big | CLSP + setup carryover between periods | first/last item only | Suerie & Stadtler (2003) |
| DLSP | small | ≤1 item, all-or-nothing at full capacity | implicit | Fleischmann (1990) |
| CSLP | small | ≤1 item, any quantity up to capacity | implicit | Karmarkar & Schrage (1985) |
| PLSP | small | ≤1 setup change, so up to 2 items | implicit | Drexl & Haase (1995) |
| GLSP | hybrid | macro-period capacity, micro-period sequence | full | Fleischmann & Meyr (1997) |

Use big-bucket models when periods are weeks or months and shop-floor sequencing is decided downstream. Switch to small-bucket or GLSP models when setups carry over between short periods or are sequence-dependent — there, lot sizing and scheduling cannot be separated.

### Strong reformulations

The big-M linking constraint makes the standard LP relaxation notoriously weak. Two classical repairs, both from the single-item polyhedron, also tighten every item's substructure inside the CLSP (Pochet & Wolsey 2006, *Production Planning by Mixed Integer Programming*):

**Facility-location reformulation** (Krarup & Bilde 1977). Disaggregate production: $w_{itu}$ = quantity produced in period $t$ to serve demand $d_{iu}$, $t \le u$:

$$
\min \sum_{i,t} f_i\, y_{it} + \sum_{i,\, t \le u} h_i (u-t)\, w_{itu}
\quad \text{s.t.} \quad
\sum_{t \le u} w_{itu} = d_{iu} \;\;\forall i,u; \qquad
w_{itu} \le d_{iu}\, y_{it}.
$$

For uncapacitated single-item instances, its LP relaxation has an integral optimal $y$ — it describes the convex hull. Cost: $O(N T^2 / 2)$ variables.

**(l,S) valid inequalities** (Barany, Van Roy & Wolsey 1984). For each $l \in \{1,\dots,T\}$ and each $S \subseteq \{1,\dots,l\}$:

$$
\sum_{t \in S} x_t \;\le\; s_l + \sum_{t \in S} d_{t,l}\; y_t,
\qquad d_{t,l} = \sum_{u=t}^{l} d_u .
$$

Together with the trivial inequalities these give the full convex hull of ULS solutions. There are exponentially many, but exact separation is $O(T^2)$ per item: given an LP point $(x^*, y^*, s^*)$, the most violated set is $S^* = \{ t \le l : x^*_t > d_{t,l}\, y^*_t \}$. So the small standard model plus a cut loop reaches the same bound as the large FL model.

### Method selection

| Situation | Method |
|-----------|--------|
| Single item, no capacity | Wagner-Whitin DP, exact in $O(T^2)$ |
| Single item, constant capacity, integer data | Florian-Klein DP, $O(T^4)$ |
| CLSP, up to a few thousand setup binaries | MIP with FL reformulation or (l,S) cut loop |
| Large CLSP, setup times, overtime | fix-and-optimize / relax-and-fix (see **matheuristics**) |
| Setup carryover or sequence-dependent setups | CLSPL / GLSP models, metaheuristics |
| Stochastic demand | static-dynamic strategies, two-stage scenario models |

## Instance Generation and Validation

Build these two functions first: every later section reuses the instance container and reports through the independent validator. The generator follows the design of the classic Trigeiro, Thomas & McClain (1989) CLSP test bed: setup costs are derived from a target time-between-orders (TBO) via the EOQ relation $TBO = \sqrt{2 f / (h \bar d)}$, and capacity is set from a target utilization.

```python
from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class ClspInstance:
    """Multi-item big-bucket CLSP data. Shapes: demand (N, T); item arrays (N,); capacity (T,)."""
    demand: np.ndarray        # d[i, t] >= 0
    setup_cost: np.ndarray    # f[i]
    holding_cost: np.ndarray  # h[i] per unit per period
    prod_time: np.ndarray     # a[i] capacity units per produced unit
    setup_time: np.ndarray    # st[i] capacity units per setup
    capacity: np.ndarray      # C[t]


def generate_clsp_instance(n_items: int, n_periods: int, seed: int,
                           tbo: float = 2.0, utilization: float = 0.85,
                           demand_cv: float = 0.35) -> ClspInstance:
    """Trigeiro-style CLSP generator: TBO sets setup costs, utilization sets capacity tightness."""
    rng = np.random.default_rng(seed)
    mean_demand = rng.uniform(50.0, 150.0, n_items)
    demand = rng.normal(mean_demand[:, None], demand_cv * mean_demand[:, None],
                        (n_items, n_periods))
    demand = np.clip(np.rint(demand), 0.0, None)
    holding_cost = rng.uniform(0.5, 1.5, n_items)
    setup_cost = 0.5 * tbo ** 2 * holding_cost * demand.mean(axis=1)  # EOQ-derived
    prod_time = np.ones(n_items)
    setup_time = rng.uniform(10.0, 50.0, n_items)
    mean_load = (prod_time[:, None] * demand).sum(axis=0).mean()
    capacity_value = (mean_load + setup_time.sum() / tbo) / utilization
    capacity = np.full(n_periods, capacity_value)
    return ClspInstance(demand, setup_cost, holding_cost, prod_time, setup_time, capacity)


inst = generate_clsp_instance(n_items=4, n_periods=8, seed=42)
print(inst.demand.shape, float(inst.demand.sum()), round(float(inst.capacity[0]), 1))
# Expected: (4, 8) 3870.0 646.4 — identical numbers on every rerun with seed 42.
```

Raise `utilization` toward 1.0 and `tbo` above 3 to create hard instances; setup-time-heavy, tightly capacitated instances are the hardest in the Trigeiro set. The validator below recomputes everything from raw data — never trust the model's own bookkeeping when reporting results:

```python
import numpy as np


def validate_clsp_solution(inst: ClspInstance, x: np.ndarray, y: np.ndarray,
                           tol: float = 1e-6) -> tuple[bool, float, list[str]]:
    """Independent feasibility check and objective recomputation; no solver objects involved."""
    violations: list[str] = []
    inventory = np.cumsum(x - inst.demand, axis=1)
    if (x < -tol).any():
        violations.append("negative production quantity")
    if (inventory < -tol).any():
        i, t = map(int, np.argwhere(inventory < -tol)[0])
        violations.append(f"unmet demand: item {i}, period {t}")
    if ((x > tol) & (y < 0.5)).any():
        i, t = map(int, np.argwhere((x > tol) & (y < 0.5))[0])
        violations.append(f"production without setup: item {i}, period {t}")
    load = (inst.prod_time[:, None] * x + inst.setup_time[:, None] * y).sum(axis=0)
    if (load > inst.capacity + tol).any():
        t = int(np.argwhere(load > inst.capacity + tol)[0][0])
        violations.append(f"capacity exceeded in period {t}")
    objective = float((inst.setup_cost[:, None] * y).sum()
                      + (inst.holding_cost[:, None] * np.clip(inventory, 0.0, None)).sum())
    return (not violations, objective, violations)


inst = generate_clsp_instance(n_items=4, n_periods=8, seed=42)
x_lfl = inst.demand.astype(float)              # lot-for-lot plan
y_lfl = (inst.demand > 0).astype(float)
ok, obj, viol = validate_clsp_solution(inst, x_lfl, y_lfl)
print(ok, round(obj, 1), viol)
# Expected: False 6802.5 ['capacity exceeded in period 2'] — lot-for-lot pays a setup
# for every item in every period, and the setup hours overload the tight periods.
```

## Wagner-Whitin Dynamic Program

The exact ULS solver. State: $F(t)$ = minimum cost of satisfying demands $1..t$, with $F(0) = 0$. By ZIO, the last regeneration interval is produced entirely in some period $j$:

$$
F(t) = \min_{1 \le j \le t} \Big\{ F(j-1) + f_j + \sum_{u=j}^{t} \Big( \sum_{v=j}^{u-1} h_v \Big) d_u \Big\}.
$$

Prefix sums make each candidate cost $O(1)$, so the whole DP is $O(T^2)$ — instant for any practical horizon. The implementation supports time-varying setup and holding costs and skips the setup charge on zero-demand intervals:

```python
import numpy as np


def wagner_whitin(demand: np.ndarray, setup_cost: np.ndarray,
                  holding_cost: np.ndarray) -> tuple[float, list[int]]:
    """O(T^2) DP for single-item uncapacitated lot sizing (Wagner & Whitin 1958).

    Returns (optimal cost, 0-indexed setup periods). Supports time-varying f_t, h_t.
    """
    T = len(demand)
    cum_h = np.concatenate(([0.0], np.cumsum(holding_cost)))        # sum h[0..t-1]
    cum_d = np.concatenate(([0.0], np.cumsum(demand)))
    cum_hd = np.concatenate(([0.0], np.cumsum(cum_h[:T] * demand)))
    F = np.full(T + 1, np.inf)
    F[0] = 0.0
    pred = np.zeros(T + 1, dtype=int)
    for t in range(T):
        j = np.arange(t + 1)
        interval_demand = cum_d[t + 1] - cum_d[j]
        produce_cost = setup_cost[j] + (cum_hd[t + 1] - cum_hd[j]) - cum_h[j] * interval_demand
        produce_cost = np.where(interval_demand > 0, produce_cost, 0.0)  # no demand, no setup
        total = F[j] + produce_cost
        k = int(np.argmin(total))
        F[t + 1] = total[k]
        pred[t + 1] = k
    setups, t = [], T
    while t > 0:
        j = pred[t]
        if cum_d[t] - cum_d[j] > 0:
            setups.append(int(j))
        t = j
    return float(F[T]), setups[::-1]


cost, setups = wagner_whitin(np.array([10.0, 20.0, 30.0]),
                             np.array([40.0, 40.0, 40.0]),
                             np.array([1.0, 1.0, 1.0]))
print(cost, setups)
# Expected: 100.0 [0, 2] — produce 30 units in period 0 (holding d_2 one period costs 20)
# and 30 units in period 2; all four ZIO plans cost 120/110/100/120.
```

Use Wagner-Whitin three ways inside capacitated work: as the exact solver when capacity never binds, as a per-item lower-bounding and seeding device (solve each item alone, ignore capacity), and as the subproblem inside Lagrangian or column-generation schemes for the CLSP. The $O(T \log T)$ refinements matter only when ULS is called millions of times inside such loops. For deeper recursion-design guidance see **dynamic-programming**.

## Exact MIP Models in gurobipy

### Standard CLSP with constraint-builder functions

Each constraint family lives in its own builder so it can be unit-tested and reused by the reformulation and the matheuristic. Note `model.update()` at the end of the builder: gurobipy's lazy updates otherwise leave `relax()` and `getVars()` looking at an empty model.

```python
import gurobipy as gp
import numpy as np
from gurobipy import GRB


def add_flow_balance_constraints(model: gp.Model, v: dict, data: ClspInstance) -> None:
    """Inventory balance s[i,t-1] + x[i,t] == d[i,t] + s[i,t], with s[i,-1] = 0."""
    N, T = data.demand.shape
    x, s = v["x"], v["s"]
    for i in range(N):
        for t in range(T):
            prev = s[i, t - 1] if t > 0 else 0.0
            model.addConstr(prev + x[i, t] == data.demand[i, t] + s[i, t],
                            name=f"flow[{i},{t}]")


def add_setup_linking_constraints(model: gp.Model, v: dict, data: ClspInstance) -> None:
    """x[i,t] <= M[i,t] y[i,t] with the tightest valid big-M (remaining demand vs capacity)."""
    N, T = data.demand.shape
    x, y = v["x"], v["y"]
    remaining = data.demand[:, ::-1].cumsum(axis=1)[:, ::-1]
    for i in range(N):
        for t in range(T):
            cap_bound = (data.capacity[t] - data.setup_time[i]) / data.prod_time[i]
            big_m = min(remaining[i, t], max(cap_bound, 0.0))
            model.addConstr(x[i, t] <= big_m * y[i, t], name=f"link[{i},{t}]")


def add_capacity_constraints(model: gp.Model, v: dict, data: ClspInstance) -> None:
    """Production plus setup time within period capacity: sum_i a_i x[i,t] + st_i y[i,t] <= C_t."""
    N, T = data.demand.shape
    x, y = v["x"], v["y"]
    for t in range(T):
        model.addConstr(
            gp.quicksum(data.prod_time[i] * x[i, t] + data.setup_time[i] * y[i, t]
                        for i in range(N)) <= data.capacity[t],
            name=f"cap[{t}]")


def build_clsp_model(data: ClspInstance) -> tuple[gp.Model, dict]:
    """Standard inventory-and-setup CLSP MIP."""
    N, T = data.demand.shape
    model = gp.Model("clsp")
    model.Params.OutputFlag = 0
    v = {"x": model.addVars(N, T, lb=0.0, name="x"),
         "s": model.addVars(N, T, lb=0.0, name="s"),
         "y": model.addVars(N, T, vtype=GRB.BINARY, name="y")}
    add_flow_balance_constraints(model, v, data)
    add_setup_linking_constraints(model, v, data)
    add_capacity_constraints(model, v, data)
    model.setObjective(
        gp.quicksum(data.setup_cost[i] * v["y"][i, t] + data.holding_cost[i] * v["s"][i, t]
                    for i in range(N) for t in range(T)),
        GRB.MINIMIZE)
    model.update()
    return model, v


def solve_clsp(data: ClspInstance, time_limit: float = 60.0) -> tuple[float, np.ndarray, np.ndarray]:
    """Solve the CLSP and return (objective, production matrix, setup matrix)."""
    model, v = build_clsp_model(data)
    model.Params.TimeLimit = time_limit
    model.Params.MIPGap = 1e-6
    model.optimize()
    assert model.Status == GRB.OPTIMAL or (model.Status == GRB.TIME_LIMIT and model.SolCount > 0)
    N, T = data.demand.shape
    x = np.array([[v["x"][i, t].X for t in range(T)] for i in range(N)])
    y = np.array([[round(v["y"][i, t].X) for t in range(T)] for i in range(N)])
    return model.ObjVal, x, y


inst = generate_clsp_instance(n_items=4, n_periods=8, seed=42)
obj_mip, x_mip, y_mip = solve_clsp(inst)
print(round(obj_mip, 1), validate_clsp_solution(inst, x_mip, y_mip)[:2])
# Expected: 5571.5 (True, 5571.501...) — optimal in well under a second; the independent
# validator reproduces the solver objective exactly.
```

For general gurobipy patterns (parameters, statuses, infeasibility diagnosis) see **milp-modeling-gurobi**.

### Facility-location reformulation

Same optimum, far stronger LP relaxation. The price is $O(N T^2/2)$ `w` variables — worth paying up to horizons of 50-100 periods. The holding coefficient $h_i(u-t)$ assumes item-constant holding cost; with time-varying $h_{it}$ replace it by the cumulative sum between $t$ and $u$.

```python
import gurobipy as gp
import numpy as np
from gurobipy import GRB


def build_clsp_fl_model(data: ClspInstance) -> tuple[gp.Model, dict]:
    """Facility-location reformulation (Krarup & Bilde 1977): w[i,t,u] serves demand (i,u) from t."""
    N, T = data.demand.shape
    model = gp.Model("clsp_fl")
    model.Params.OutputFlag = 0
    triples = [(i, t, u) for i in range(N) for u in range(T)
               if data.demand[i, u] > 0 for t in range(u + 1)]
    w = model.addVars(triples, lb=0.0, name="w")
    y = model.addVars(N, T, vtype=GRB.BINARY, name="y")
    for i in range(N):
        for u in range(T):
            if data.demand[i, u] > 0:
                model.addConstr(gp.quicksum(w[i, t, u] for t in range(u + 1))
                                == data.demand[i, u], name=f"demand[{i},{u}]")
    for (i, t, u) in triples:
        model.addConstr(w[i, t, u] <= data.demand[i, u] * y[i, t], name=f"open[{i},{t},{u}]")
    by_period: dict[int, list[tuple[int, int]]] = {t: [] for t in range(T)}
    for (i, t, u) in triples:
        by_period[t].append((i, u))
    for t in range(T):
        model.addConstr(
            gp.quicksum(data.prod_time[i] * w[i, t, u] for (i, u) in by_period[t])
            + gp.quicksum(data.setup_time[i] * y[i, t] for i in range(N))
            <= data.capacity[t], name=f"cap[{t}]")
    model.setObjective(
        gp.quicksum(data.setup_cost[i] * y[i, t] for i in range(N) for t in range(T))
        + gp.quicksum(data.holding_cost[i] * (u - t) * w[i, t, u] for (i, t, u) in triples),
        GRB.MINIMIZE)
    model.update()
    return model, {"w": w, "y": y}


def lp_bound(model: gp.Model) -> float:
    """LP-relaxation bound of a built MIP model."""
    relaxed = model.relax()
    relaxed.Params.OutputFlag = 0
    relaxed.optimize()
    assert relaxed.Status == GRB.OPTIMAL
    return relaxed.ObjVal


inst = generate_clsp_instance(n_items=4, n_periods=8, seed=42)
m_std, _ = build_clsp_model(inst)
m_fl, _ = build_clsp_fl_model(inst)
print(round(lp_bound(m_std), 1), round(lp_bound(m_fl), 1))
# Expected: 2414.6 5397.3 — the standard LP bound is 57% below the MIP optimum 5571.5,
# the FL relaxation closes about 94% of that gap. The FL MIP optimum is also 5571.5.
```

### (l,S) valid inequalities with exact separation

The same bound as the FL model, obtained on the small standard model by a cutting-plane loop. `separate_ls_inequalities` is the exact $O(N T^2)$ separation; the loop strengthens the root LP. Inside a branch-and-bound run you would add the same cuts through a user-cut callback — the callback machinery is covered in **cutting-planes-valid-inequalities**.

```python
import gurobipy as gp
import numpy as np
from gurobipy import GRB


def separate_ls_inequalities(data: ClspInstance, x_val: np.ndarray, y_val: np.ndarray,
                             s_val: np.ndarray, eps: float = 1e-4) -> list[tuple[int, int, list[int]]]:
    """Exact separation of (l,S) inequalities (Barany, Van Roy & Wolsey 1984).

    For each item i and end period l, the most violated set is
    S* = {t <= l : x*[t] > d[t..l] * y*[t]}. Returns violated (i, l, S*) triples.
    """
    cuts = []
    N, T = data.demand.shape
    for i in range(N):
        for l in range(T):
            d_tl = np.cumsum(data.demand[i, :l + 1][::-1])[::-1]   # d_tl[t] = d[i, t..l]
            margin = x_val[i, :l + 1] - d_tl * y_val[i, :l + 1]
            S = np.nonzero(margin > eps)[0]
            if margin[S].sum() - s_val[i, l] > eps:
                cuts.append((i, l, S.tolist()))
    return cuts


def clsp_root_cut_loop(data: ClspInstance, max_rounds: int = 50) -> tuple[float, float, int]:
    """Strengthen the root LP with (l,S) cuts; returns (lp_before, lp_after, n_cuts)."""
    model, v = build_clsp_model(data)
    for var in model.getVars():
        var.VType = GRB.CONTINUOUS          # binaries keep their [0,1] bounds
    model.optimize()
    lp0 = model.ObjVal
    N, T = data.demand.shape
    n_cuts = 0
    for _ in range(max_rounds):
        x_val = np.array([[v["x"][i, t].X for t in range(T)] for i in range(N)])
        y_val = np.array([[v["y"][i, t].X for t in range(T)] for i in range(N)])
        s_val = np.array([[v["s"][i, t].X for t in range(T)] for i in range(N)])
        cuts = separate_ls_inequalities(data, x_val, y_val, s_val)
        if not cuts:
            break
        for (i, l, S) in cuts:
            d_tl = np.cumsum(data.demand[i, :l + 1][::-1])[::-1]
            model.addConstr(
                gp.quicksum(v["x"][i, t] for t in S)
                <= v["s"][i, l] + gp.quicksum(d_tl[t] * v["y"][i, t] for t in S),
                name=f"ls[{i},{l},{n_cuts}]")
            n_cuts += 1
        model.optimize()
    return lp0, model.ObjVal, n_cuts


inst = generate_clsp_instance(n_items=4, n_periods=8, seed=42)
lp0, lp_cut, n_cuts = clsp_root_cut_loop(inst)
print(round(lp0, 1), round(lp_cut, 1), n_cuts)
# Expected: 2414.6 5397.3 93 — 93 cuts close 94.5% of the LP gap and reach exactly the
# FL-reformulation bound, as the convex-hull theory predicts.
```

The residual 5397.3 → 5571.5 gap comes from the capacity coupling between items — no single-item polyhedral result can close it. That part is left to branching.

## Metaheuristic: Setup-Pattern GA with ZIO Decoder

For instances beyond MIP reach (hundreds of items, long horizons), search over the binary setup patterns only and let a decoder set the quantities. Given a setup pattern, ZIO assigns every demand to the most recent open setup — optimal per item up to capacity, which is handled by a penalty. The whole population decodes in a few vectorized numpy operations; one well-matched method is enough here, and operator variants (selection, crossover, mutation-rate control) are covered in **genetic-algorithms**.

```python
import numpy as np


def decode_zio(setups: np.ndarray, data: ClspInstance,
               penalty: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Vectorized ZIO decoder: setup patterns (P,N,T) -> plans, effective setups, fitness."""
    P, N, T = setups.shape
    d = data.demand
    first = np.argmax(d > 0, axis=1)                     # earliest positive demand per item
    Y = setups.astype(bool).copy()
    Y[:, np.arange(N), first] = True                     # repair: earliest demand is covered
    src = np.maximum.accumulate(np.where(Y, np.arange(T), -1), axis=2)
    flat_src = np.where(d > 0, src, 0).reshape(P * N, T)  # safe index where demand is zero
    qty = np.broadcast_to(np.where(d > 0, d, 0.0), (P, N, T)).reshape(P * N, T)
    x = np.zeros((P * N, T))
    np.add.at(x, (np.arange(P * N)[:, None], flat_src), qty)
    x = x.reshape(P, N, T)
    y_eff = x > 1e-9                                     # drop setups that produce nothing
    inv = np.cumsum(x - d, axis=2)                       # >= 0 by construction
    cost = (data.setup_cost[None, :, None] * y_eff).sum(axis=(1, 2)) \
        + (data.holding_cost[None, :, None] * inv).sum(axis=(1, 2))
    load = (data.prod_time[None, :, None] * x
            + data.setup_time[None, :, None] * y_eff).sum(axis=1)
    overload = np.clip(load - data.capacity[None, :], 0.0, None).sum(axis=1)
    return x, y_eff.astype(float), cost + penalty * overload


def ga_clsp(data: ClspInstance, pop_size: int = 200, generations: int = 300,
            setup_prob: float = 0.5, mut_rate: float = 0.02, penalty: float = 100.0,
            elite_frac: float = 0.1, seed: int = 0) -> tuple[float, np.ndarray, np.ndarray]:
    """Binary GA over setup patterns; ZIO decoder sets quantities, penalty handles capacity."""
    rng = np.random.default_rng(seed)
    N, T = data.demand.shape
    pop = rng.random((pop_size, N, T)) < setup_prob
    n_elite = max(1, int(elite_frac * pop_size))
    n_child = pop_size - n_elite
    best_fit, best_x, best_y = np.inf, None, None
    for _ in range(generations):
        x, y, fit = decode_zio(pop, data, penalty)
        order = np.argsort(fit)
        if fit[order[0]] < best_fit:
            b = order[0]
            best_fit, best_x, best_y = float(fit[b]), x[b].copy(), y[b].copy()
        cand = rng.integers(0, pop_size, (2, 2 * n_child))        # size-2 tournaments
        winners = np.where(fit[cand[0]] <= fit[cand[1]], cand[0], cand[1])
        pa, pb = winners[:n_child], winners[n_child:]
        mask = rng.random((n_child, N, T)) < 0.5                  # uniform crossover
        children = np.where(mask, pop[pa], pop[pb])
        children ^= rng.random((n_child, N, T)) < mut_rate        # bit-flip mutation
        pop = np.concatenate([pop[order[:n_elite]], children])
    return best_fit, best_x, best_y


inst = generate_clsp_instance(n_items=4, n_periods=8, seed=42)
ga_fit, ga_x, ga_y = ga_clsp(inst, seed=3)
ok, ga_obj, viol = validate_clsp_solution(inst, ga_x, ga_y)
print(round(ga_fit, 1), ok, viol)
# Expected: 5657.4 True [] — capacity-feasible (zero penalty active) and 1.54% above
# the MIP optimum 5571.5; a few seconds for 200 x 300 decoded individuals.
```

Set `setup_prob` near `1/tbo` so the initial population starts at sensible setup densities, and scale `penalty` so one unit of overload costs more than the largest setup saving (here capacity units are comparable to holding-cost units, so 100 is safely dominant). If the best individual still carries overload, the validator will say so — report that, never silently accept it.

## Advanced Techniques

### Fix-and-optimize

The standard matheuristic for large lot-sizing models (Helber & Sahling 2010): keep the full MIP, but free only the setup binaries inside a sliding time window and fix the rest to the incumbent. Each subproblem is small and solves in seconds; the incumbent is always feasible for the next window, so the objective decreases monotonically. Start it from any feasible setup matrix — the GA result is a good seed.

```python
import gurobipy as gp
import numpy as np
from gurobipy import GRB


def fix_and_optimize(data: ClspInstance, y_start: np.ndarray, window: int = 4, step: int = 2,
                     mip_seconds: float = 5.0, passes: int = 2) -> tuple[float, np.ndarray, np.ndarray]:
    """Time-window fix-and-optimize (Helber & Sahling 2010). y_start must be capacity-feasible."""
    model, v = build_clsp_model(data)
    model.Params.TimeLimit = mip_seconds
    N, T = data.demand.shape
    y_inc = np.rint(y_start).astype(float)
    best = np.inf
    for _ in range(passes):
        for w0 in range(0, T, step):
            w1 = min(w0 + window, T)
            for i in range(N):
                for t in range(T):
                    free = w0 <= t < w1
                    v["y"][i, t].LB = 0.0 if free else y_inc[i, t]
                    v["y"][i, t].UB = 1.0 if free else y_inc[i, t]
            model.optimize()
            if model.SolCount > 0 and model.ObjVal < best - 1e-9:
                best = model.ObjVal
                y_inc = np.array([[round(v["y"][i, t].X) for t in range(T)]
                                  for i in range(N)], dtype=float)
    for i in range(N):                       # recover x under the final setup pattern
        for t in range(T):
            v["y"][i, t].LB = y_inc[i, t]
            v["y"][i, t].UB = y_inc[i, t]
    model.optimize()
    x = np.array([[v["x"][i, t].X for t in range(T)] for i in range(N)])
    return model.ObjVal, x, y_inc


inst = generate_clsp_instance(n_items=4, n_periods=8, seed=42)
_, _, y_seed = ga_clsp(inst, seed=3)
fo_obj, fo_x, fo_y = fix_and_optimize(inst, y_seed)
print(round(fo_obj, 1), validate_clsp_solution(inst, fo_x, fo_y)[0])
# Expected: 5571.5 True — fix-and-optimize repairs the 1.54% GA gap to the exact optimum.
# On a 10-item, 12-period instance (seed 1) the same pipeline gives GA 22830.9 ->
# fix-and-optimize 22232.2 vs MIP optimum 22210.0 (0.1% gap).
```

Window decompositions other than time work too: free all periods of an item subset, or all binaries of one resource. Rotate decompositions when a pass stops improving. Variants, acceptance rules, and budgeting of the inner MIP calls are treated in **matheuristics**.

### Relax-and-fix construction

When no feasible start exists, build one forward in time: in iteration $k$, keep the binaries of window $k$ integral, fix the already-decided earlier windows, and relax all later binaries to $[0,1]$. The relaxed tail approximates future setup costs well because the per-item polyhedron is tight there if you use the FL or (l,S)-strengthened model. With positive setup times, add overtime variables with a high cost so every iteration stays feasible; drive overtime to zero in a second fix-and-optimize phase.

### Setup carryover and small-bucket refinements

CLSPL adds binary carryover variables $z_{it}$ ("the machine is still configured for $i$ when period $t$ starts"), with constraints $z_{it} \le y_{i,t-1} + z_{i,t-1}$, $\sum_i z_{it} \le 1$, and a relaxed linking constraint $x_{it} \le M_{it}(y_{it} + z_{it})$ (Suerie & Stadtler 2003 give a tight formulation). Carryover typically saves 3-10% setup time in tightly loaded plans. If setups are sequence-dependent inside periods, move to GLSP-style micro-period models — at that point lot sizing has become lot sizing *and* scheduling, and metaheuristics or decomposition take over from monolithic MIP.

### Rolling horizons and end-of-horizon control

Production plans are re-solved every period with a shifted window. Two standing problems: the model drains inventory to zero at the horizon end (underproduction late in the window), and re-planning flips earlier decisions (nervousness). Standard fixes: impose terminal inventory lower bounds or a salvage value on $s_{iT}$, freeze the first 1-3 periods of each re-plan, and overlap windows so only frozen decisions are executed. Evaluate a rolling policy by simulation over the full demand realization, not by the single-window objective.

### Stochastic demand

Under demand uncertainty, classify the policy first (Bookbinder & Tan 1988): *static* (setup periods and quantities fixed now), *static-dynamic* (setup periods fixed, quantities decided as demand reveals — the practical favorite, since plan stability is preserved), or *dynamic* (everything recourse). The static-dynamic strategy becomes a two-stage program: first-stage $y$, second-stage quantities per scenario, solvable in extensive form for moderate scenario counts. Scenario generation, sample-average approximation, and L-shaped decomposition for larger trees are covered in **stochastic-optimization**.

## Practical Challenges

**The MIP gap stalls because the LP relaxation is far below any feasible cost.** The big-M linking constraints are the cause; on the demo instance the standard LP bound is 57% below the optimum. Use the tightest $M_{it}$ (remaining demand capped by capacity), then either switch to the facility-location reformulation or run an (l,S) cut loop — both closed ~94% of the gap above. Only then increase solver effort.

**The solver reports infeasible as soon as setup times are included.** Feasibility with setup times is NP-complete (Maes, McClain & Van Wassenhove 1991), and real data is often genuinely overloaded in peak periods. Add overtime variables $o_t$ to the capacity constraints with an explicit, documented cost; a plan that says "12 overtime hours in period 7" is more useful than `GRB.INFEASIBLE`.

**Wagner-Whitin output is used as the production plan although capacity binds.** ZIO plans concentrate production and routinely violate tight capacities. Use WW per item only as a seed or bound; let the CLSP model or the fix-and-optimize loop produce the executable plan, and always run the independent validator on whatever is shipped.

**Minimum lot sizes or batch multiples quietly invalidate the model.** ZIO and the (l,S) hull arguments assume freely divisible lots. Model minimum lots as $x_{it} \ge L_i y_{it}$ (this alone keeps the structure), batch multiples with integer batch-count variables $x_{it} = B_i q_{it}$ — and stop using the WW DP as an exact oracle in either case.

**Rolling-horizon re-planning flips last week's decisions.** Freeze the first periods, penalize deviations from the previous plan, and set terminal inventory targets. Measure nervousness explicitly (count of changed setups between consecutive plans) — otherwise the planning department will measure it for you.

**The FL reformulation runs out of memory on long horizons.** It carries $O(NT^2/2)$ variables; at $N = 200$, $T = 100$ that is a million `w` variables before presolve. Prefer the (l,S) cut loop on the standard model, restrict $w_{itu}$ to $u - t \le$ a max holding span, or aggregate periods.

**The GA returns a plan that the validator rejects on capacity.** The penalty weight is too small relative to setup savings, so infeasible individuals win tournaments. Raise the penalty, or make it adaptive (multiply by 2 whenever the generation best is infeasible); keep the validator as the final referee and report its verdict, not the fitness value.

**Two formulations disagree on the optimal cost.** Almost always an objective mismatch, not a solver bug: the inventory model charges $h_i s_{it}$ on end-of-period stock, the FL model charges $h_i (u-t)$ per unit — these coincide only with item-constant holding costs and zero initial inventory. Reconcile conventions (initial stock, end-of-horizon stock, time-varying $h$) and re-derive one objective from the other before suspecting anything else.

## Tools & Libraries

| Library | When to use | Note |
|---------|-------------|------|
| gurobipy | CLSP MIPs, cut loops, fix-and-optimize | Fastest path to proven gaps; license required |
| HiGHS (highspy) | Same models without a commercial license | Good MIP performance; expect longer runtimes on hard CLSP |
| PuLP / Pyomo | Solver-agnostic model definition | Useful when the solver must be swappable; slower model build |
| OR-Tools CP-SAT | Lot sizing fused with detailed sequencing | Integer quantities only; shines on GLSP-like scheduling parts |
| numpy | WW DP, decoder, GA, validator | Everything in this skill except the MIPs runs on numpy alone |
| pandas | Result/experiment tables | One row per (instance, seed, method, objective, time, gap) |

## Output Format

A complete lot-sizing answer contains:

1. **Variant classification.** One sentence: which model family (ULS / CLSP / CLSPL / small-bucket) and why, with the key data facts (N, T, utilization, setup times present or not).
2. **Model summary table.** Variables, constraint families with counts, objective terms, and which reformulation/cuts are active.

| Component | Count | Notes |
|-----------|-------|-------|
| x, s continuous | 2·N·T | production, inventory |
| y binary | N·T | setups |
| flow / link / cap constraints | N·T + N·T + T | named per family |
| (l,S) cuts added | as separated | root LP: before → after |

3. **Bound and gap report.** Standard LP bound, strengthened bound, best incumbent, proven gap, and runtime — e.g. "LP 2414.6 → +(l,S) 5397.3 → optimum 5571.5, 0.4 s".
4. **The plan itself.** Per item: setup periods, lot sizes, end inventories; per period: capacity used vs available (flag periods above 95%).
5. **Validator verdict.** Output of `validate_clsp_solution` — feasibility flag, recomputed objective matching the reported one, and the violation list (empty).
6. **For heuristic runs.** Seeds, population/iteration budget, best/mean over ≥10 seeds, and gap to the best known bound — never a single-run number.
7. **Reproducibility artifacts.** Instance generator parameters (seed, TBO, utilization), solver parameters changed from defaults, and library versions.

## Questions to Ask

- Is per-period capacity binding, and do setups consume capacity time as well as money?
- How many items and periods, and are periods big buckets (weeks) or small buckets (shifts)?
- Can setups carry over between adjacent periods? Are changeovers sequence-dependent?
- Is backlogging or lost sales allowed, and at what cost?
- Are there minimum lot sizes, batch multiples, or shelf-life limits on inventory?
- Are costs time-varying, and is there nonzero initial inventory?
- Is demand a firm forecast, or should the plan hedge against uncertainty?
- Will the plan be executed once or re-solved in a rolling horizon — and how many periods are frozen?
- What runtime is acceptable, and is a proven optimality gap required?
- Is a Gurobi license available, or must everything run on open-source solvers?

## Related Skills

- **dynamic-programming** — for the recursion design behind Wagner-Whitin, the Florian-Klein capacitated DP, and state-space tricks when lot sizing appears as a subproblem.
- **cutting-planes-valid-inequalities** — for separation machinery and user-cut callbacks when (l,S)-style cuts must run inside branch and bound instead of a root loop.
- **matheuristics** — for fix-and-optimize, relax-and-fix, local branching, and how to budget MIP calls inside a heuristic loop on large CLSP instances.
- **milp-modeling-gurobi** — for the gurobipy idioms used by every model here: constraint builders, parameter setting, status handling, and solution extraction.
- **stochastic-optimization** — for lot sizing under demand uncertainty: scenario generation, two-stage extensive forms, and the L-shaped method behind static-dynamic strategies.
