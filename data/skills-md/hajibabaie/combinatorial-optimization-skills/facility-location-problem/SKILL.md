---
name: facility-location-problem
description: When the user wants to choose facility sites and assign customers to them — UFLP, CFLP, p-median, or p-center — with strong MIP formulations, Benders or Lagrangian solution paths, and greedy, interchange, or VNS heuristics. Also use when the user mentions "facility location," "p-median," "p-center," "open facilities," "location-allocation," "UFLP," "warehouse location," or when fixed opening costs trade off against assignment or transport costs. For optimality-cut decomposition at scale, see benders-decomposition; for demand uncertainty, see stochastic-optimization.
---

# Facility Location Problems

You are an expert in discrete facility location, the open-sites-and-assign-customers structure that underlies supply chain design, public service siting, and clustering. This skill covers the uncapacitated and capacitated facility location problems (UFLP, CFLP), the p-median, and the p-center, with strong-vs-weak MIP formulations, Benders and Lagrangian solution paths, greedy and interchange heuristics, a VNS metaheuristic, and a stochastic-demand extension sketch. Use the framework below to identify the variant, choose the formulation whose LP relaxation is tight enough, and deliver a solution with an independently validated objective and a defensible optimality gap.

## Initial Assessment

Establish the following before formulating or coding anything:

- **Identify the variant.** Are fixed opening costs present (UFLP/CFLP) or is the number of facilities fixed at `p` (p-median/p-center)? Is the objective total cost (sum) or worst-case distance (max)? Are capacities binding? These four answers select the model.
- **Check the assignment regime.** May a customer's demand be split across facilities (multi-source), or must each customer be served by exactly one facility (single-source)? Single-source CFLP embeds a generalized assignment problem and is much harder — even finding a feasible assignment for fixed open sites is NP-hard.
- **Estimate size.** Record `n` customers and `m` candidate sites. The strong formulation has `n * m` linking constraints; at `n * m >= ~5e6` a direct MIP strains memory and you should plan for Benders, Lagrangian relaxation, or candidate reduction.
- **Audit the cost data.** Are assignment costs distances, distance × demand, or full freight quotes? Are fixed costs amortized to the same time horizon as the flow costs? Mixed units silently corrupt the trade-off the model is supposed to make.
- **Check the distance structure.** Euclidean/haversine from coordinates, or shortest paths on a road network? For p-center and covering arguments, confirm whether the triangle inequality holds — approximation guarantees depend on it.
- **Clarify exact-vs-heuristic requirements.** Strategic location decisions are solved rarely and justify exact MIP with a proven gap. Repeated tactical re-solves (e.g., location inside a larger loop) favor the interchange/VNS heuristics plus a Lagrangian bound.
- **Confirm solver availability.** Gurobi license present? If not, the models below port directly to HiGHS/SCIP via the same constraint families; the heuristics are pure numpy.
- **Ask about uncertainty.** Is demand known, or are there scenarios/forecast errors? Facilities are long-lived first-stage decisions; if demand is uncertain, a deterministic model with average demand can be badly wrong (see the stochastic extension sketch below).
- **Agree on deliverables.** Open-site list, assignment plan, objective split into fixed and service cost, capacity utilization, bound and gap, and an independent feasibility check.

## Problem Variants and Formulations

Notation: customers `j ∈ J` with `|J| = n`, candidate sites `i ∈ I` with `|I| = m`, fixed opening cost `f_i ≥ 0`, assignment cost `c_ji ≥ 0` for serving the *full* demand of `j` from `i`, demand `d_j > 0`, capacity `q_i > 0`, and `p` the number of facilities to open. Decision variables: `y_i ∈ {0,1}` (open site `i`), `x_ji ∈ [0,1]` (fraction of customer `j` served from `i`).

### UFLP — uncapacitated facility location

$$
\min \sum_{i} f_i y_i + \sum_{j}\sum_{i} c_{ji} x_{ji}
\quad \text{s.t.} \quad
\sum_{i} x_{ji} = 1 \;\; \forall j, \qquad
x_{ji} \le y_i \;\; \forall j,i, \qquad
x \ge 0, \; y \in \{0,1\}^m.
$$

Two classic formulations differ only in the linking constraints:

- **Strong (disaggregated):** `x_ji <= y_i` for every pair — `n * m` rows. The LP relaxation is tight; on many benchmark instances it is integral or nearly so (Cornuéjols, Nemhauser & Wolsey 1990, "The uncapacitated facility location problem", in *Discrete Location Theory*).
- **Weak (aggregated):** `sum_j x_ji <= n * y_i` — only `m` rows. Same integer optimum, but the LP bound is far weaker: the LP can open `y_i = 1/n` slivers of every facility, and branch-and-bound explodes.

Always start from the strong formulation. Modern solvers presolve and cut well, but no amount of cutting reliably recovers the strength you gave away by aggregating. With `y` integral, the assignment subproblem is trivial (serve each customer from the cheapest open site), so `x` may be declared continuous — the optimal `x` is automatically integral when assignment costs are nonnegative.

### CFLP — capacitated facility location

Add capacity rows and keep the disaggregated links as redundant-for-the-IP tightening:

$$
\sum_{j} d_j x_{ji} \le q_i y_i \;\; \forall i, \qquad
x_{ji} \le y_i \;\; \forall j,i.
$$

The capacity row already links `x` to `y`, so the `x_ji <= y_i` rows are logically redundant — but they substantially tighten the LP relaxation and are standard practice. A useful valid inequality is the total-capacity cover `sum_i q_i y_i >= sum_j d_j`. **Single-source CFLP** declares `x` binary; the assignment subproblem for fixed `y` becomes a generalized assignment problem (strongly NP-hard), and instance difficulty jumps accordingly.

### p-median and p-center

Both fix the number of open facilities and drop fixed costs (ReVelle & Swain 1970 for the p-median IP; Hakimi 1964, 1965 for the network versions):

$$
\text{p-median:} \;\; \min \sum_{j}\sum_{i} d_j \, t_{ji} \, x_{ji}
\qquad
\text{p-center:} \;\; \min z, \;\; \sum_{i} t_{ji} x_{ji} \le z \;\; \forall j,
$$

both subject to `sum_i x_ji = 1`, `x_ji <= y_i`, `sum_i y_i = p`, with `t_ji` the distance. The p-median minimizes demand-weighted average distance (efficiency); the p-center minimizes the worst customer distance (equity/emergency coverage). The p-center MIP has notoriously weak LP bounds because a single `z` aggregates everything; the practical exact method is bisection on the radius with set-covering feasibility subproblems (Daskin 1995, *Network and Discrete Location*), implemented below.

### Complexity and method selection

All four problems are NP-hard on general instances; the p-median is NP-hard even on planar graphs of maximum degree 3 (Kariv & Hakimi 1979). For metric UFLP the best known approximation factor is 1.488 (Li 2013) against a hardness floor of 1.463 (Guha & Khuller 1999); the p-center admits a tight 2-approximation (Gonzalez 1985; Hochbaum & Shmoys 1985). The p-median on trees is polynomial (Tamir 1996).

| Setting | Recommended route |
|---|---|
| UFLP, `n * m` up to ~1e6 links | strong MIP directly (this skill's `solve_uflp`) |
| UFLP, larger | Benders with closed-form cuts (Fischetti, Ljubić & Sinnl 2017) or Lagrangian/dual ascent |
| CFLP, multi-source | MIP with capacity + disaggregated links + total-capacity cover |
| CFLP, single-source, large | Lagrangian relaxation + repair heuristic, or LNS over assignments |
| p-median, `m <= ~1000` | MIP, or Lagrangian (Beasley 1993) for bound + heuristic |
| p-median, large | VNS / fast interchange (Hansen & Mladenović 1997; Resende & Werneck 2007) |
| p-center | bisection over the radius with covering MIPs (below) |
| Stochastic demand | two-stage scenario model; see the sketch below and stochastic-optimization |

## Instance Generation and Validation

Standard benchmarks: the OR-Library `cap*` UFLP/CFLP sets (Beasley 1990), the large Körkel-Ghosh UFLP instances, and the OR-Library p-median set. For controlled experiments, generate Euclidean instances with seeds so every run is reproducible.

```python
import numpy as np


def generate_instance(
    n_customers: int,
    n_facilities: int,
    seed: int,
    capacity_ratio: float | None = None,
    fixed_cost_range: tuple[float, float] = (100.0, 300.0),
) -> dict[str, np.ndarray]:
    """Generate a Euclidean facility-location instance with a fixed seed.

    Returns 'cust_xy', 'fac_xy', 'dist' (n x m Euclidean distances),
    'demand', 'cost' (demand-weighted distance, the UFLP/CFLP assignment
    cost), 'fixed_cost', and — when capacity_ratio is given — 'capacity'
    sized so total capacity = capacity_ratio * total demand.
    """
    rng = np.random.default_rng(seed)
    cust_xy = rng.uniform(0.0, 100.0, size=(n_customers, 2))
    fac_xy = rng.uniform(0.0, 100.0, size=(n_facilities, 2))
    dist = np.linalg.norm(cust_xy[:, None, :] - fac_xy[None, :, :], axis=2)
    demand = rng.integers(1, 20, size=n_customers).astype(np.float64)
    inst = {
        "cust_xy": cust_xy,
        "fac_xy": fac_xy,
        "dist": dist,
        "demand": demand,
        "cost": demand[:, None] * dist,
        "fixed_cost": rng.uniform(*fixed_cost_range, size=n_facilities),
    }
    if capacity_ratio is not None:
        total = float(demand.sum())
        inst["capacity"] = np.full(
            n_facilities, capacity_ratio * total / n_facilities
        )
    return inst


inst = generate_instance(n_customers=50, n_facilities=10, seed=42, capacity_ratio=2.0)
print(inst["dist"].shape, float(inst["demand"].sum()) > 0, inst["capacity"].shape)
# Expected: (50, 10) True (10,) — identical numbers on every rerun of seed 42.
```

Tune hardness through `capacity_ratio` (1.1–1.5 makes CFLP capacity-bound and hard; >= 3 makes it UFLP-like) and the ratio of fixed to assignment costs (high fixed costs → few facilities, long assignments, weaker LP bounds).

Every solution — exact or heuristic — must pass an independent validator that shares no code with the models. This is the second opinion that catches sign errors, transposed matrices, and constraints you forgot to add.

```python
import numpy as np


def validate_solution(
    open_mask: np.ndarray,
    assign: np.ndarray,
    fixed_cost: np.ndarray,
    cost: np.ndarray,
    demand: np.ndarray | None = None,
    capacity: np.ndarray | None = None,
    p: int | None = None,
    objective: str = "sum",
    tol: float = 1e-6,
) -> tuple[bool, float, list[str]]:
    """Independent feasibility check and objective recomputation.

    open_mask: (m,) boolean. assign: (n, m) with assign[j, i] = fraction of
    customer j served from site i. cost: (n, m) cost of serving ALL of j
    from i; pass demand-weighted distance for the p-median, raw distance
    with objective='max' for the p-center. Returns (feasible, objective,
    violation messages).
    """
    violations: list[str] = []
    row_sum = assign.sum(axis=1)
    unserved = np.flatnonzero(np.abs(row_sum - 1.0) > tol)
    if unserved.size:
        violations.append(f"customers not fully assigned: {unserved[:5].tolist()}")
    if float(assign.min()) < -tol:
        violations.append("negative assignment fractions")
    closed = assign[:, ~open_mask]
    if closed.size and float(closed.max()) > tol:
        violations.append("assignment to closed facilities")
    if capacity is not None and demand is not None:
        load = (demand[:, None] * assign).sum(axis=0)
        over = np.flatnonzero(load > capacity * (1.0 + tol) + tol)
        if over.size:
            violations.append(f"capacity exceeded at sites: {over.tolist()}")
    if p is not None and int(open_mask.sum()) != p:
        violations.append(f"{int(open_mask.sum())} sites open, expected p={p}")
    service = (cost * assign).sum(axis=1)
    if objective == "max":
        obj = float(service.max())
    else:
        obj = float(fixed_cost[open_mask].sum() + service.sum())
    return (not violations), obj, violations


fixed = np.array([4.0, 3.0, 4.0])
cost = np.array([[2.0, 6.0, 9.0], [5.0, 3.0, 8.0], [9.0, 7.0, 2.0], [8.0, 6.0, 3.0]])
open_mask = np.array([True, False, True])
assign = np.zeros((4, 3))
assign[[0, 1, 2, 3], [0, 0, 2, 2]] = 1.0
print(validate_solution(open_mask, assign, fixed, cost))
# Expected: (True, 20.0, []) — feasible, objective matches the UFLP optimum below.
```

## Exact MIP Models in gurobipy

State each model, then build it from named constraint-builder functions so every constraint family is testable in isolation. The 4-customer, 3-site instance used in the demos has known optima: UFLP 20.0, CFLP 20.0, p-median 12.0, p-center 5.0, all opening sites `{0, 2}`.

### UFLP with selectable formulation strength

```python
import gurobipy as gp
import numpy as np
from gurobipy import GRB


def add_assignment_constraints(
    model: gp.Model, x: gp.tupledict, n: int, m: int
) -> None:
    """Each customer is fully assigned: sum_i x[j,i] == 1."""
    for j in range(n):
        model.addConstr(
            gp.quicksum(x[j, i] for i in range(m)) == 1, name=f"assign[{j}]"
        )


def add_strong_linking_constraints(
    model: gp.Model, x: gp.tupledict, y: gp.tupledict, n: int, m: int
) -> None:
    """Disaggregated x[j,i] <= y[i]: n*m rows, tight LP relaxation."""
    for j in range(n):
        for i in range(m):
            model.addConstr(x[j, i] <= y[i], name=f"link[{j},{i}]")


def add_weak_linking_constraints(
    model: gp.Model, x: gp.tupledict, y: gp.tupledict, n: int, m: int
) -> None:
    """Aggregated sum_j x[j,i] <= n*y[i]: m rows, loose LP relaxation."""
    for i in range(m):
        model.addConstr(
            gp.quicksum(x[j, i] for j in range(n)) <= n * y[i],
            name=f"aglink[{i}]",
        )


def solve_uflp(
    fixed_cost: np.ndarray,
    cost: np.ndarray,
    strong: bool = True,
    time_limit: float = 120.0,
) -> tuple[float, np.ndarray, np.ndarray]:
    """Solve the UFLP. Returns (objective, open mask, assignment matrix)."""
    n, m = cost.shape
    model = gp.Model("uflp")
    model.Params.OutputFlag = 0
    model.Params.TimeLimit = time_limit
    y = model.addVars(m, vtype=GRB.BINARY, name="y")
    x = model.addVars(n, m, vtype=GRB.CONTINUOUS, lb=0.0, ub=1.0, name="x")
    add_assignment_constraints(model, x, n, m)
    if strong:
        add_strong_linking_constraints(model, x, y, n, m)
    else:
        add_weak_linking_constraints(model, x, y, n, m)
    model.setObjective(
        gp.quicksum(float(fixed_cost[i]) * y[i] for i in range(m))
        + gp.quicksum(
            float(cost[j, i]) * x[j, i] for j in range(n) for i in range(m)
        ),
        GRB.MINIMIZE,
    )
    model.optimize()
    if model.Status not in (GRB.OPTIMAL, GRB.TIME_LIMIT) or model.SolCount == 0:
        raise RuntimeError(f"no solution found (status {model.Status})")
    open_mask = np.array([y[i].X > 0.5 for i in range(m)])
    assign = np.array([[x[j, i].X for i in range(m)] for j in range(n)])
    return float(model.ObjVal), open_mask, assign


fixed = np.array([4.0, 3.0, 4.0])
cost = np.array([[2.0, 6.0, 9.0], [5.0, 3.0, 8.0], [9.0, 7.0, 2.0], [8.0, 6.0, 3.0]])
obj, open_mask, assign = solve_uflp(fixed, cost, strong=True)
print(round(obj, 2), np.flatnonzero(open_mask).tolist())
# Expected: 20.0 [0, 2] — open sites 0 and 2; customers 0,1 -> 0 and 2,3 -> 2.
```

To see the formulation gap, solve the LP relaxations of both variants on a generated instance: the weak LP bound is typically far below the strong one, while the strong LP is often integral. This comparison is the single most instructive experiment in MIP formulation strength.

### CFLP with capacities and single-source option

```python
import gurobipy as gp
import numpy as np
from gurobipy import GRB


def add_demand_constraints(
    model: gp.Model, x: gp.tupledict, n: int, m: int
) -> None:
    """Each customer's demand is fully served: sum_i x[j,i] == 1."""
    for j in range(n):
        model.addConstr(
            gp.quicksum(x[j, i] for i in range(m)) == 1, name=f"demand[{j}]"
        )


def add_capacity_constraints(
    model: gp.Model,
    x: gp.tupledict,
    y: gp.tupledict,
    demand: np.ndarray,
    capacity: np.ndarray,
) -> None:
    """Capacity with opening link: sum_j d_j x[j,i] <= q_i y[i]."""
    n, m = len(demand), len(capacity)
    for i in range(m):
        model.addConstr(
            gp.quicksum(float(demand[j]) * x[j, i] for j in range(n))
            <= float(capacity[i]) * y[i],
            name=f"capacity[{i}]",
        )


def add_linking_constraints(
    model: gp.Model, x: gp.tupledict, y: gp.tupledict, n: int, m: int
) -> None:
    """x[j,i] <= y[i]: redundant for the IP, tightens the LP substantially."""
    for j in range(n):
        for i in range(m):
            model.addConstr(x[j, i] <= y[i], name=f"link[{j},{i}]")


def solve_cflp(
    fixed_cost: np.ndarray,
    cost: np.ndarray,
    demand: np.ndarray,
    capacity: np.ndarray,
    single_source: bool = False,
    time_limit: float = 120.0,
) -> tuple[float, np.ndarray, np.ndarray]:
    """Solve the CFLP; x becomes binary when single_source=True."""
    n, m = cost.shape
    model = gp.Model("cflp")
    model.Params.OutputFlag = 0
    model.Params.TimeLimit = time_limit
    y = model.addVars(m, vtype=GRB.BINARY, name="y")
    xtype = GRB.BINARY if single_source else GRB.CONTINUOUS
    x = model.addVars(n, m, vtype=xtype, lb=0.0, ub=1.0, name="x")
    add_demand_constraints(model, x, n, m)
    add_capacity_constraints(model, x, y, demand, capacity)
    add_linking_constraints(model, x, y, n, m)
    model.addConstr(
        gp.quicksum(float(capacity[i]) * y[i] for i in range(m))
        >= float(demand.sum()),
        name="total_capacity",
    )
    model.setObjective(
        gp.quicksum(float(fixed_cost[i]) * y[i] for i in range(m))
        + gp.quicksum(
            float(cost[j, i]) * x[j, i] for j in range(n) for i in range(m)
        ),
        GRB.MINIMIZE,
    )
    model.optimize()
    if model.Status not in (GRB.OPTIMAL, GRB.TIME_LIMIT) or model.SolCount == 0:
        raise RuntimeError(f"no solution found (status {model.Status})")
    open_mask = np.array([y[i].X > 0.5 for i in range(m)])
    assign = np.array([[x[j, i].X for i in range(m)] for j in range(n)])
    return float(model.ObjVal), open_mask, assign


fixed = np.array([4.0, 3.0, 4.0])
cost = np.array([[2.0, 6.0, 9.0], [5.0, 3.0, 8.0], [9.0, 7.0, 2.0], [8.0, 6.0, 3.0]])
demand = np.array([4.0, 3.0, 5.0, 4.0])
capacity = np.array([9.0, 8.0, 9.0])
obj, open_mask, assign = solve_cflp(fixed, cost, demand, capacity)
print(round(obj, 2), np.flatnonzero(open_mask).tolist())
# Expected: 20.0 [0, 2] — capacities 9+9 cover total demand 16 with no split.
```

### p-median

```python
import gurobipy as gp
import numpy as np
from gurobipy import GRB


def add_assignment_constraints(
    model: gp.Model, x: gp.tupledict, n: int, m: int
) -> None:
    """Each customer is assigned: sum_i x[j,i] == 1."""
    for j in range(n):
        model.addConstr(
            gp.quicksum(x[j, i] for i in range(m)) == 1, name=f"assign[{j}]"
        )


def add_linking_constraints(
    model: gp.Model, x: gp.tupledict, y: gp.tupledict, n: int, m: int
) -> None:
    """Customers may only use open medians: x[j,i] <= y[i]."""
    for j in range(n):
        for i in range(m):
            model.addConstr(x[j, i] <= y[i], name=f"link[{j},{i}]")


def add_cardinality_constraint(model: gp.Model, y: gp.tupledict, p: int) -> None:
    """Open exactly p facilities: sum_i y[i] == p."""
    model.addConstr(y.sum() == p, name="cardinality")


def solve_pmedian(
    dist: np.ndarray, demand: np.ndarray, p: int, time_limit: float = 120.0
) -> tuple[float, np.ndarray, np.ndarray]:
    """Solve the p-median; objective is demand-weighted total distance."""
    n, m = dist.shape
    model = gp.Model("pmedian")
    model.Params.OutputFlag = 0
    model.Params.TimeLimit = time_limit
    y = model.addVars(m, vtype=GRB.BINARY, name="y")
    x = model.addVars(n, m, vtype=GRB.CONTINUOUS, lb=0.0, ub=1.0, name="x")
    add_assignment_constraints(model, x, n, m)
    add_linking_constraints(model, x, y, n, m)
    add_cardinality_constraint(model, y, p)
    model.setObjective(
        gp.quicksum(
            float(demand[j] * dist[j, i]) * x[j, i]
            for j in range(n)
            for i in range(m)
        ),
        GRB.MINIMIZE,
    )
    model.optimize()
    if model.Status not in (GRB.OPTIMAL, GRB.TIME_LIMIT) or model.SolCount == 0:
        raise RuntimeError(f"no solution found (status {model.Status})")
    open_mask = np.array([y[i].X > 0.5 for i in range(m)])
    assign = np.array([[x[j, i].X for i in range(m)] for j in range(n)])
    return float(model.ObjVal), open_mask, assign


dist = np.array([[2.0, 6.0, 9.0], [5.0, 3.0, 8.0], [9.0, 7.0, 2.0], [8.0, 6.0, 3.0]])
obj, open_mask, assign = solve_pmedian(dist, np.ones(4), p=2)
print(round(obj, 2), np.flatnonzero(open_mask).tolist())
# Expected: 12.0 [0, 2] — best pair of medians for unit demands.
```

### p-center: direct MIP and radius bisection

The direct MIP works but bounds poorly. The bisection method exploits that the optimal radius is one of the `n * m` distance values: binary-search the sorted unique distances, and at each candidate radius `r` ask the set-covering feasibility question "can `p` sites cover every customer within `r`?".

```python
import gurobipy as gp
import numpy as np
from gurobipy import GRB


def add_radius_constraints(
    model: gp.Model, x: gp.tupledict, z: gp.Var, dist: np.ndarray
) -> None:
    """Worst-case distance bound: sum_i t[j,i] x[j,i] <= z for every j."""
    n, m = dist.shape
    for j in range(n):
        model.addConstr(
            gp.quicksum(float(dist[j, i]) * x[j, i] for i in range(m)) <= z,
            name=f"radius[{j}]",
        )


def solve_pcenter_mip(
    dist: np.ndarray, p: int, time_limit: float = 120.0
) -> tuple[float, np.ndarray]:
    """Direct p-center MIP. Weak LP bound; fine for small instances."""
    n, m = dist.shape
    model = gp.Model("pcenter")
    model.Params.OutputFlag = 0
    model.Params.TimeLimit = time_limit
    y = model.addVars(m, vtype=GRB.BINARY, name="y")
    x = model.addVars(n, m, vtype=GRB.CONTINUOUS, lb=0.0, ub=1.0, name="x")
    z = model.addVar(lb=0.0, name="z")
    for j in range(n):
        model.addConstr(
            gp.quicksum(x[j, i] for i in range(m)) == 1, name=f"assign[{j}]"
        )
        for i in range(m):
            model.addConstr(x[j, i] <= y[i], name=f"link[{j},{i}]")
    model.addConstr(y.sum() == p, name="cardinality")
    add_radius_constraints(model, x, z, dist)
    model.setObjective(z, GRB.MINIMIZE)
    model.optimize()
    if model.Status not in (GRB.OPTIMAL, GRB.TIME_LIMIT) or model.SolCount == 0:
        raise RuntimeError(f"no solution found (status {model.Status})")
    return float(model.ObjVal), np.array([y[i].X > 0.5 for i in range(m)])


def solve_pcenter_bisection(dist: np.ndarray, p: int) -> tuple[float, np.ndarray]:
    """Exact p-center via binary search on the radius over unique distances.

    Each test solves a small covering MIP: choose <= p sites such that every
    customer has an open site within radius r (Daskin 1995).
    """
    n, m = dist.shape
    radii = np.unique(dist)
    lo, hi = 0, len(radii) - 1
    best_r, best_mask = float(radii[-1]), np.zeros(m, dtype=bool)
    while lo <= hi:
        mid = (lo + hi) // 2
        r = float(radii[mid])
        cover = dist <= r + 1e-9
        model = gp.Model("cover")
        model.Params.OutputFlag = 0
        y = model.addVars(m, vtype=GRB.BINARY, name="y")
        for j in range(n):
            model.addConstr(
                gp.quicksum(y[i] for i in range(m) if cover[j, i]) >= 1,
                name=f"cover[{j}]",
            )
        model.addConstr(y.sum() <= p, name="cardinality")
        model.setObjective(0, GRB.MINIMIZE)
        model.optimize()
        if model.Status == GRB.OPTIMAL:
            best_r = r
            best_mask = np.array([y[i].X > 0.5 for i in range(m)])
            hi = mid - 1
        else:
            lo = mid + 1
    return best_r, best_mask


dist = np.array([[2.0, 6.0, 9.0], [5.0, 3.0, 8.0], [9.0, 7.0, 2.0], [8.0, 6.0, 3.0]])
r, mask = solve_pcenter_bisection(dist, p=2)
print(round(r, 2), np.flatnonzero(mask).tolist())
# Expected: 5.0 [0, 2] — same optimum as solve_pcenter_mip on this instance.
```

The bisection solves `O(log(n*m))` covering MIPs, each of which is far easier than the monolithic p-center model. On instances where the direct MIP stalls with a 50% gap, the bisection typically finishes in seconds.

## Construction and Improvement Heuristics

The classic UFLP heuristics remain the right first move on large instances: greedy ADD (Kuehn & Hamburger 1963) for construction, then interchange (open/close/swap) improvement. With zero fixed costs and swap-only moves, the same interchange is the Teitz & Bart (1968) vertex-substitution heuristic for the p-median. The implementation below evaluates every move by full recomputation — `O(m^2)` trials of `O(n*m)` each per pass — which is simple and correct; production codes use Whitaker's (1983) fast-swap data structures, refined by Resende & Werneck (2007).

```python
import numpy as np


def uflp_total_cost(
    open_mask: np.ndarray, fixed_cost: np.ndarray, cost: np.ndarray
) -> float:
    """Fixed cost of the open set plus closest-open-site assignment cost."""
    if not open_mask.any():
        return float("inf")
    return float(fixed_cost[open_mask].sum() + cost[:, open_mask].min(axis=1).sum())


def greedy_add_uflp(fixed_cost: np.ndarray, cost: np.ndarray) -> np.ndarray:
    """Greedy ADD: repeatedly open the site with the largest total-cost drop."""
    n, m = cost.shape
    open_mask = np.zeros(m, dtype=bool)
    best_serve = np.full(n, np.inf)
    total = float("inf")
    while True:
        cand_assign = np.minimum(best_serve[:, None], cost).sum(axis=0)
        cand_total = fixed_cost[open_mask].sum() + fixed_cost + cand_assign
        cand_total[open_mask] = np.inf
        i = int(np.argmin(cand_total))
        if cand_total[i] >= total - 1e-9:
            return open_mask
        total = float(cand_total[i])
        open_mask[i] = True
        best_serve = np.minimum(best_serve, cost[:, i])


def interchange(
    open_mask: np.ndarray,
    fixed_cost: np.ndarray,
    cost: np.ndarray,
    swap_only: bool = False,
) -> tuple[np.ndarray, float]:
    """Best-improvement open/close/swap descent. With swap_only=True and zero
    fixed costs this is Teitz-Bart vertex substitution for the p-median."""
    mask = open_mask.copy()
    total = uflp_total_cost(mask, fixed_cost, cost)
    improved = True
    while improved:
        improved = False
        best_total, best_mask = total, mask
        open_idx = np.flatnonzero(mask)
        closed_idx = np.flatnonzero(~mask)
        moves = [(a, b) for a in open_idx for b in closed_idx]
        if not swap_only:
            moves += [(a, -1) for a in open_idx if len(open_idx) > 1]
            moves += [(-1, b) for b in closed_idx]
        for a, b in moves:
            trial = mask.copy()
            if a >= 0:
                trial[a] = False
            if b >= 0:
                trial[b] = True
            t = uflp_total_cost(trial, fixed_cost, cost)
            if t < best_total - 1e-9:
                best_total, best_mask, improved = t, trial, True
        mask, total = best_mask, best_total
    return mask, total


fixed = np.array([4.0, 3.0, 4.0])
cost = np.array([[2.0, 6.0, 9.0], [5.0, 3.0, 8.0], [9.0, 7.0, 2.0], [8.0, 6.0, 3.0]])
g = greedy_add_uflp(fixed, cost)
print(np.flatnonzero(g).tolist(), uflp_total_cost(g, fixed, cost))
final, total = interchange(g, fixed, cost)
print(np.flatnonzero(final).tolist(), total)
# Expected: greedy opens [1, 2] at 21.0; interchange swaps to [0, 2] at 20.0.
```

Note the instructive failure: greedy stops at `{1, 2}` (cost 21) because no single *addition* improves, yet the swap `1 -> 0` reaches the optimum 20. Greedy for UFLP has a worst-case guarantee only for the related maximization form (Cornuéjols, Fisher & Nemhauser 1977); always follow it with interchange.

## Metaheuristic: VNS for the p-median

Variable neighborhood search is the method of choice for large p-median instances (Hansen & Mladenović 1997): shake by replacing `k` medians at random, descend with vertex substitution, and grow `k` only when stuck. The local-search step below vectorizes the insertion scan over all candidate sites at once. For VNS design choices — neighborhood ordering, skewed acceptance, reduced VNS — see **variable-neighborhood-search**; this block keeps the algorithm minimal.

```python
import numpy as np


def pmedian_cost(dist: np.ndarray, demand: np.ndarray, medians: np.ndarray) -> float:
    """Demand-weighted cost of serving every customer from its closest median."""
    return float((demand * dist[:, medians].min(axis=1)).sum())


def interchange_step(
    dist: np.ndarray, demand: np.ndarray, medians: np.ndarray
) -> tuple[np.ndarray, float, bool]:
    """One best-improvement vertex-substitution pass, vectorized over insertions."""
    n, m = dist.shape
    cand = np.setdiff1d(np.arange(m), medians)
    cur = pmedian_cost(dist, demand, medians)
    best_cost, best_sol = cur, medians
    d_sel = dist[:, medians]
    for r in range(len(medians)):
        rest = np.delete(d_sel, r, axis=1)
        rest_min = rest.min(axis=1) if rest.shape[1] else np.full(n, np.inf)
        new_min = np.minimum(rest_min[:, None], dist[:, cand])
        costs = (demand[:, None] * new_min).sum(axis=0)
        k = int(np.argmin(costs))
        if costs[k] < best_cost - 1e-9:
            best_cost = float(costs[k])
            best_sol = medians.copy()
            best_sol[r] = cand[k]
    return best_sol, best_cost, best_cost < cur - 1e-9


def vns_pmedian(
    dist: np.ndarray,
    demand: np.ndarray,
    p: int,
    seed: int = 0,
    k_max: int = 3,
    max_no_improve: int = 30,
) -> tuple[np.ndarray, float]:
    """Basic VNS for the p-median: shake k medians, descend, move or grow k."""
    rng = np.random.default_rng(seed)
    m = dist.shape[1]
    sol = rng.choice(m, size=p, replace=False)
    improved = True
    while improved:
        sol, _, improved = interchange_step(dist, demand, sol)
    best_sol, best_cost = sol, pmedian_cost(dist, demand, sol)
    stall, k = 0, 1
    while stall < max_no_improve and m > p:
        kk = min(k, p, m - p)
        out = rng.choice(p, size=kk, replace=False)
        pool = np.setdiff1d(np.arange(m), best_sol)
        trial = best_sol.copy()
        trial[out] = rng.choice(pool, size=kk, replace=False)
        improved = True
        while improved:
            trial, _, improved = interchange_step(dist, demand, trial)
        cost = pmedian_cost(dist, demand, trial)
        if cost < best_cost - 1e-9:
            best_sol, best_cost, k, stall = trial, cost, 1, 0
        else:
            k, stall = k % k_max + 1, stall + 1
    return np.sort(best_sol), best_cost


dist = np.array([[2.0, 6.0, 9.0], [5.0, 3.0, 8.0], [9.0, 7.0, 2.0], [8.0, 6.0, 3.0]])
sol, cost = vns_pmedian(dist, np.ones(4), p=2, seed=7)
print(sol.tolist(), cost)
# Expected: [0, 2] 12.0 — matches the p-median MIP optimum on this instance.
```

On instances with `m <= ~2000`, VNS with these defaults reliably lands within 0–1% of the OR-Library optima in seconds. Always report the gap against the Lagrangian or LP bound, not just the best heuristic value.

## Advanced Techniques

### Lagrangian relaxation of the assignment constraints

Dualize `sum_i x_ji = 1` with multipliers `λ_j` (free sign). The relaxed problem separates by facility: each site `i` has reduced profit `ρ_i = f_i + sum_j min(0, c_ji - λ_j)` and opens exactly when `ρ_i < 0`, giving the bound

$$
L(\lambda) = \sum_j \lambda_j + \sum_i \min(0, \rho_i).
$$

The subproblem has the integrality property, so `max_λ L(λ)` equals the strong-formulation LP bound (Geoffrion 1974, "Lagrangean relaxation for integer programming") — you get the strong bound without ever forming the `n*m` constraint matrix. Maximize `L` by subgradient steps on `g_j = 1 - sum_i x_ji`; full subgradient loop, step-size rules, and the primal-recovery heuristic are in **lagrangian-relaxation** (its worked example is exactly this UFLP path).

```python
import numpy as np


def uflp_lagrangian_bound(
    fixed_cost: np.ndarray, cost: np.ndarray, lam: np.ndarray
) -> tuple[float, np.ndarray]:
    """Lagrangian lower bound for UFLP and the subgradient at lam."""
    slack = cost - lam[:, None]
    rho = fixed_cost + np.minimum(slack, 0.0).sum(axis=0)
    open_i = rho < 0.0
    x = (slack < 0.0) & open_i[None, :]
    bound = float(lam.sum() + rho[open_i].sum())
    return bound, 1.0 - x.sum(axis=1)


fixed = np.array([4.0, 3.0, 4.0])
cost = np.array([[2.0, 6.0, 9.0], [5.0, 3.0, 8.0], [9.0, 7.0, 2.0], [8.0, 6.0, 3.0]])
bound, subgrad = uflp_lagrangian_bound(fixed, cost, np.array([6.0, 5.0, 7.0, 6.0]))
print(bound)
# Expected: 20.0 — at these multipliers the bound already equals the optimum.
```

### Benders decomposition with closed-form cuts

Project out `x`: keep `y` and one epigraph variable `η_j` per customer in the master. For a master point `ŷ`, the customer-`j` subproblem is `min_i { c_ji : ŷ_i = 1 }`, whose dual solution is available in closed form. With `i*` the cheapest open site for `j`, the optimality cut is

$$
\eta_j \ge c_{j i^*} - \sum_{i:\, c_{ji} < c_{j i^*}} (c_{j i^*} - c_{ji}) \, y_i ,
$$

separable per customer and added lazily at integer master solutions. This is the engine behind the state-of-the-art exact UFLP results of Fischetti, Ljubić & Sinnl (2017), "Redesigning Benders decomposition for large-scale facility location". The full callback implementation (lazy constraints, root-node cut loop, normalization) is the UFLP worked example in **benders-decomposition** — use it when `n * m` links no longer fit in memory.

### Dual ascent and DUALOC

Erlenkotter (1978), "A dual-based procedure for uncapacitated facility location", ascends the strong-LP dual greedily: raise each customer's dual `v_j` until it hits the next assignment cost `c_ji`, keep facility slack complementary, and read off a primal solution from the tight constraints. DUALOC routinely closes UFLP instances without any LP solver and remains a strong warm-start generator: run dual ascent, take its primal solution as a MIP start, and its bound as the initial cutoff.

### Stochastic-demand extension (sketch)

Facilities are first-stage decisions; assignments can adapt after demand is revealed. With scenarios `s` of probability `π_s` and demands `d_j^s`, the two-stage model is

$$
\min \; \sum_i f_i y_i + \sum_s \pi_s \sum_j \sum_i c_{ji}^s \, x_{ji}^s
$$

subject to per-scenario assignment and capacity constraints, with the single `y` shared across scenarios. The extensive form is just the CFLP model above with `x` indexed by scenario — build it by calling the same constraint builders once per scenario. Uncertainty matters most when capacities bind: the deterministic average-demand solution can be infeasible in high-demand scenarios. For scenario generation, sample average approximation, EVPI/VSS, and the L-shaped method (which is exactly Benders applied to this structure), see **stochastic-optimization**; the survey of Snyder (2006), "Facility location under uncertainty: a review", maps the modeling choices.

### Candidate and variable reduction

For continental-scale instances, most `x_ji` pairs are absurd (customer in one region, site in another). Restrict each customer to its `k` nearest candidate sites (`k = 20–50`) before building the model; this shrinks the strong formulation from `n*m` to `n*k` links. The reduction is heuristic — verify it by checking that no customer's chosen site is its `k`-th nearest (if it is, increase `k` and re-solve), or make it exact by pricing the deleted variables' reduced costs after solving.

## Practical Challenges

**The strong formulation exhausts memory before the solver even starts.** At `n = m = 3000`, the disaggregated UFLP has 9M linking rows. Options in order of preference: candidate reduction to `k` nearest sites; Benders with closed-form cuts (no `x` in the master at all); Lagrangian relaxation (no constraint matrix at all). Do not fall back to the weak formulation — its LP bound makes branch-and-bound hopeless at this size.

**The CFLP LP relaxation is much weaker than the UFLP one.** Capacity rows let the LP open fractional facilities to "rent" capacity cheaply. Keep the disaggregated `x_ji <= y_i` links even though the capacity row already links `x` to `y`, add the total-capacity cover `sum q_i y_i >= sum d_j`, and consider flow-cover cuts (Gurobi separates these automatically when the model is written with explicit capacity structure).

**Single-source CFLP feasibility is itself hard.** With `x` binary, fixing `y` leaves a generalized assignment problem, so a heuristic that picks good sites can still die on the assignment. Solve the multi-source LP first to choose sites, then solve the single-source assignment as a separate MIP over the open sites only; or use Lagrangian relaxation of the assignment constraints with a knapsack-based repair.

**The p-center MIP stalls with a huge gap.** A single max-variable `z` gives the LP almost no information. Switch to the radius-bisection method above: `O(log(n*m))` covering problems, each tiny. If even those are slow, the 2-approximation of Gonzalez (1985) (iteratively pick the farthest customer as the next center) gives an instant upper bound and a starting interval for the bisection.

**The heuristic answer has no quality certificate.** Stakeholders deciding on warehouses will ask how far from optimal the plan is. Always pair a heuristic incumbent with a bound: the Lagrangian bound above costs milliseconds per evaluation, and 200 subgradient iterations typically land within 1–2% of the strong LP value. Report `gap = (UB - LB) / UB`.

**Identical candidate sites create symmetry.** Multiple sites with equal `(f_i, c_·i)` columns (e.g., generic lots in the same zone) make branch-and-bound enumerate permutations. Aggregate them into one site with an integer opening variable `y_i ∈ {0, ..., u}` and capacity `u * q`, or add lexicographic ordering constraints `y_i >= y_{i'}` within each identical group.

**Fixed and variable costs live on different time scales.** Fixed costs are capital expenditures; assignment costs are per-shipment. Amortize the fixed cost to the planning horizon (e.g., annualized capex against annual flow cost) before modeling. If the answer flips when the amortization period changes from 5 to 10 years, report both solutions — the model is telling you the decision is finance-driven, not logistics-driven.

**Distance ties make heuristic results unstable across seeds.** Grid-like coordinates produce many equal distances; argmin tie-breaking then differs across runs and platforms. Break ties deterministically (lowest index), run the metaheuristic over >= 10 seeds, and report best/mean/spread rather than a single run.

## Tools & Libraries

| Library | When to use | Note |
|---|---|---|
| gurobipy | exact UFLP/CFLP/p-median/p-center MIPs | the models in this skill; callbacks enable the Benders path |
| HiGHS / SCIP (via PuLP, Pyomo, python-mip) | no commercial license | same constraint families port directly; expect 2-10x slower on hard CFLP |
| OR-Tools CP-SAT | single-source CFLP with side constraints | strong on assignment-feasibility-dominated instances |
| numpy | heuristics, bounds, validators | greedy/interchange/VNS and the Lagrangian bound above |
| scipy.spatial.distance.cdist | building distance matrices | one call replaces nested loops; supports many metrics |
| networkx | road-network distances | multi-source Dijkstra from candidate sites, then matrix assembly |
| spopt (PySAL) | quick GIS-flavored location models | ready-made p-median/p-center/LSCP/MCLP wrappers over PuLP |

## Output Format

A complete facility-location deliverable contains:

1. **Model summary** — one table stating what was solved:

| Item | Value |
|---|---|
| Variant | CFLP, multi-source |
| Formulation | strong links + total-capacity cover |
| Size | n=500 customers, m=60 sites, 30,060 binaries/continuous |
| Solver, settings | Gurobi 12, TimeLimit=600, MIPGap=0.5% |

2. **Solution report** — open sites with their fixed costs; objective split into fixed vs. service cost; per-site utilization `load_i / q_i` for capacitated variants; the assignment plan as a CSV (`customer, site, fraction, cost`).
3. **Quality certificate** — best bound, incumbent, gap, and solve time for exact runs; for heuristics, the Lagrangian/LP bound, the gap against it, and best/mean/std over seeds.
4. **Validation line** — output of `validate_solution` on the reported plan: feasibility flag, recomputed objective, and confirmation that it matches the solver objective to tolerance. A deliverable without this line is not done.
5. **Sensitivity notes** — how the open set changes when fixed costs are amortized differently, when `p` varies by ±1, or across demand scenarios; location decisions are strategic, and the stability of the open set matters more than the third decimal of the objective.
6. **Artifacts** — instance file (or generator call with seed), solution CSV/JSON, and the exact solver log or heuristic convergence trace.

## Questions to Ask

- Are fixed opening costs known, or is the number of facilities fixed by policy (p-median/p-center)?
- Should the model minimize total cost or the worst customer's distance? Who is the worst-case constraint protecting?
- Can a customer's demand be split across facilities, or is single sourcing contractual?
- Do facilities have hard capacities? What happens to unmet demand — lost, penalized, or outsourced?
- How many customers and candidate sites? Is there a shortlist of candidates, or is every customer location also a candidate?
- Are distances Euclidean, road-network, or tariff-based? Do you have the matrix, or coordinates only?
- Is demand deterministic, or should the plan hedge across forecast scenarios?
- What time horizon amortizes the fixed costs, and is the demand figure for the same horizon?
- Is a proven optimum required for the investment decision, or is a bounded-gap heuristic acceptable?

## Related Skills

- **benders-decomposition** — when the strong UFLP/CFLP formulation no longer fits in memory; its worked example is UFLP with closed-form lazy cuts.
- **lagrangian-relaxation** — when you need the strong-LP bound and a primal heuristic without building the full model; its worked example dualizes the UFLP assignment constraints.
- **variable-neighborhood-search** — when instances outgrow exact methods; design details for the shaking and descent used in the p-median VNS above.
- **stochastic-optimization** — when demand is uncertain and facilities must be sited before it is revealed; two-stage scenario models and SAA.
- **milp-modeling-gurobi** — when you need the general gurobipy modeling workflow behind the constraint-builder pattern used in every model here.
