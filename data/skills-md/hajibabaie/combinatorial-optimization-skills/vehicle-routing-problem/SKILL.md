---
name: vehicle-routing-problem
description: When the user wants to model and solve vehicle routing problems — the capacitated VRP and its main variants (time windows, multi-depot, heterogeneous fleet, pickup-and-delivery) — via two- and three-index MIP formulations, savings and sweep construction, ALNS improvement, and OR-Tools routing. Also use when the user mentions "vehicle routing," "VRP," "CVRP," "time windows," "fleet," "delivery routes," or "Solomon instances," or when several capacity-limited routes must start and end at a depot. For single-vehicle tours, see traveling-salesman-problem; for destroy-repair design in depth, see large-neighborhood-search.
---

# Vehicle Routing Problem

You are an expert in vehicle routing: the capacitated VRP (CVRP) and its main variants — time windows (VRPTW), multi-depot (MDVRP), heterogeneous fleet (HFVRP), and pickup-and-delivery (PDPTW). This skill covers two- and three-index MIP formulations in gurobipy with explicit constraint builders, reproducible instance generation, independent solution validation, classic construction heuristics (Clarke-Wright savings, sweep), a compact ALNS, and the OR-Tools routing layer. Use the framework below to pick the right variant model and the right solution method for the instance size and time budget, and to deliver solutions whose feasibility and objective are verified independently of the solver.

## Initial Assessment

Establish these facts before writing any model or heuristic:

- **Variant.** Which side constraints exist — capacity only, time windows, multiple depots, mixed fleet, paired pickups and deliveries, open routes (no return)? Map the problem onto the variant table below before choosing a formulation.
- **Objective.** Pure travel distance/time, fixed cost per vehicle used, or a hierarchy (minimize vehicles first, then distance)? Hierarchies change acceptance rules in heuristics and need either lexicographic solving or a large vehicle cost in MIPs.
- **Fleet.** Is the number of vehicles K a hard limit, a decision to minimize, or effectively unlimited? Is the fleet homogeneous? Heterogeneous fleets push you toward three-index models or set partitioning.
- **Instance size.** Customer count is the method gate: a two-index MIP in a general solver proves optimality up to roughly 30-50 customers; branch-cut-and-price codes reach 200-1000 (Pecin et al. 2017, "Improved branch-cut-and-price for capacitated vehicle routing"); beyond that, heuristics only.
- **Distance data.** Euclidean coordinates or a road-network matrix? Symmetric or asymmetric? What rounding convention applies — CVRPLIB rounds Euclidean distances to the nearest integer, and mixing conventions silently corrupts gap reports.
- **Time data (if windows).** Are travel times equal to distances? Service durations per stop? Planning horizon and depot closing time? Is waiting before a window allowed (standard) or penalized?
- **Demand structure.** Deterministic integer demands? Any single demand close to the vehicle capacity Q makes packing tight and construction heuristics fragile.
- **Split deliveries.** Exactly one visit per customer (the standard assumption everywhere below), or may a customer's demand be split across vehicles? Split delivery (SDVRP) changes the model class — settle this before formulating anything.
- **Route limits.** Maximum route duration, length, or stop count? Driver breaks? These become extra dimensions in OR-Tools and extra resources in labeling-based pricing, and they bloat two-index MIPs.
- **Re-planning cadence.** One-shot strategic plan or daily operational re-solve? Repeated solving rewards warm starts from the previous plan and route-stability penalties, not just raw cost per day.
- **Solver availability.** Gurobi license for exact work? OR-Tools acceptable as a dependency? PyVRP available when benchmark-quality heuristic results are wanted with no tuning?
- **Time budget.** Seconds per instance (operational dispatch), minutes (planning), or hours (benchmarking)? The budget decides between OR-Tools defaults, a tuned ALNS, and exact methods.
- **Quality requirement.** Proof of optimality, within ~1% of best known, or "a feasible plan now"? Only the first forces exact machinery.
- **Feasibility risk.** Can demand exceed total fleet capacity, or can windows be impossible to meet? Decide upfront whether unassigned customers are allowed at a penalty (a request bank) or must be impossible.
- **Benchmarks.** Will results be compared on CVRPLIB / Uchoa X-instances / Solomon / Gehring-Homberger sets, or only on private data? Benchmark conventions fix rounding, fleet limits, and objective definitions.
- **Validation plan.** Insist on an independent feasibility checker and objective recomputation that share no code with the model or heuristic (provided below).
- **Reproducibility.** Fixed seeds for instance generation and for every stochastic method; one results row per (instance, algorithm, seed) run.

## Problem Variants and Formulations

### Formal definition (CVRP)

Given a complete directed graph $G=(V,A)$ with $V=\{0,1,\dots,n\}$, depot $0$, customer set $N=\{1,\dots,n\}$, demands $q_i>0$, identical vehicles of capacity $Q$, fleet size $K$, and arc costs $c_{ij}$: find at most $K$ circuits through the depot such that every customer lies on exactly one circuit, the demand on each circuit is at most $Q$, and total arc cost is minimal. The problem was introduced by Dantzig & Ramser (1959), "The Truck Dispatching Problem." With $K=1$ and $Q=\infty$ it reduces to the TSP, so CVRP is NP-hard; with fixed $K$, even deciding feasibility embeds bin packing.

The two-index formulation uses binary arc variables $x_{ij}$:

$$
\min \sum_{(i,j)\in A} c_{ij}\, x_{ij}
$$

$$
\sum_{j \neq i} x_{ij} = 1, \qquad \sum_{j \neq i} x_{ji} = 1 \qquad \forall i \in N
$$

$$
\sum_{j \in N} x_{0j} \le K
$$

$$
\sum_{i \in S}\sum_{j \notin S} x_{ij} \;\ge\; \left\lceil \frac{\sum_{i\in S} q_i}{Q} \right\rceil \qquad \forall\, S \subseteq N,\; S \neq \emptyset
$$

The last family — the rounded capacity inequalities — both eliminates subtours and enforces capacity, but it is exponential in size and must be separated dynamically (see Advanced Techniques). The compact alternative adds load variables $u_i$ in MTZ style (Miller, Tucker & Zemlin 1960):

$$
u_j \ge u_i + q_j - Q\,(1 - x_{ij}) \quad \forall\, i \neq j \in N, \qquad q_i \le u_i \le Q .
$$

Load strictly increases along arcs between customers, so no subtour disconnected from the depot can exist, and the bound $u_i \le Q$ enforces capacity. The price is a weak LP relaxation: expect large root gaps compared with the cut-based model.

For VRPTW, add service-start variables $t_i \in [a_i, b_i]$ with service times $s_i$ and travel times $\tau_{ij}$:

$$
t_j \ge t_i + s_i + \tau_{ij} - M_{ij}\,(1 - x_{ij}), \qquad M_{ij} = \max(0,\; b_i + s_i + \tau_{ij} - a_j).
$$

The per-arc constant $M_{ij}$ is the tightest valid big-M; never use one global constant. Time propagation also eliminates subtours, so the load constraints are then needed only for capacity.

### Variant taxonomy

| Variant | Extra data | Model change | Practical method of choice |
|---|---|---|---|
| CVRP | $q_i$, $Q$, $K$ | base model above | HGS or ALNS heuristic; branch-cut-and-price exact |
| VRPTW | $[a_i,b_i]$, $s_i$, $\tau_{ij}$ | time variables + per-arc big-M | ALNS; insertion (Solomon 1987) to construct |
| MDVRP | depot set $D$ | three-index, or assignment + one CVRP per depot | ALNS with depot-reassignment removal |
| HFVRP | types with $Q_k$, fixed cost $f_k$ | three-index $x_{ijk}$, fleet-mix objective | ALNS / set partitioning over routes |
| PDPTW | pickup-delivery pairs $(p,d)$ | same-route pairing + precedence $t_p \le t_d$ | ALNS (Ropke & Pisinger 2006) |
| OVRP | no depot return | drop return arcs or zero their cost | same as CVRP |

### Two-index vs three-index vs set partitioning

- **Two-index** ($x_{ij}$): smallest model, vehicles anonymous. Correct default for homogeneous fleets. Cannot express per-vehicle attributes.
- **Three-index** ($x_{ijk}$, plus visit variables $y_{ik}$): needed when vehicles differ (capacity, cost, depot, allowed customers). Identical vehicles create severe symmetry — break it (e.g., force vehicle $k$ to be used only if $k-1$ is used, or assign the lowest-index customer of each route to the lowest free vehicle index) or the branch-and-bound tree explodes; see the symmetry discussion in integer-programming-techniques-style references (Toth & Vigo 2014, "Vehicle Routing: Problems, Methods, and Applications").
- **Set partitioning**: one binary per feasible route, partitioning constraints over customers. Exponentially many columns, solved by column generation with shortest-path pricing — the backbone of every modern exact VRP code (Pessoa et al. 2020, "A generic exact solver for vehicle routing and related problems"). See column-generation.

### Decision guidance

- **Use the two-index MIP** when $n \le 50$, the fleet is homogeneous, and an optimality certificate matters. Add lazy rounded-capacity cuts when the MTZ-load gap stalls.
- **Use OR-Tools routing** when you need a good feasible plan in seconds-to-minutes with many side constraints and no appetite for custom code; its default improvement metaheuristic is guided local search — see guided-local-search.
- **Use ALNS** (or PyVRP's hybrid genetic search) when instances exceed exact reach or run repeatedly in production; ALNS handles tight windows and heterogeneous constraints gracefully because repair rebuilds feasibility — see large-neighborhood-search.
- **Use column generation / branch-and-price** when you need bounds or exactness past $n \approx 50$ and can invest in a pricing labeling algorithm.
- **Intra-route improvement is TSP machinery** (2-opt, Or-opt, 3-opt on each route); reuse it from traveling-salesman-problem rather than reinventing it.

## Exact MIP Models in Gurobi

Build every constraint family in its own named function. This makes formulations swappable (MTZ-load vs lazy cuts), testable in isolation, and reusable across variants.

### CVRP, two-index with MTZ-load capacity

```python
import math
import gurobipy as gp
from gurobipy import GRB


def add_degree_constraints(model: gp.Model, x: gp.tupledict, data: dict) -> None:
    """One arc in and one arc out per customer; at most K vehicles leave the depot."""
    n, K = data["n"], data["K"]
    nodes = range(n + 1)
    for i in range(1, n + 1):
        model.addConstr(gp.quicksum(x[i, j] for j in nodes if j != i) == 1, name=f"out[{i}]")
        model.addConstr(gp.quicksum(x[j, i] for j in nodes if j != i) == 1, name=f"in[{i}]")
    model.addConstr(gp.quicksum(x[0, j] for j in range(1, n + 1)) <= K, name="fleet")


def add_capacity_constraints(model: gp.Model, x: gp.tupledict, u: gp.tupledict, data: dict) -> None:
    """MTZ-style load propagation: u[j] is the vehicle load right after serving j.

    Load strictly increases along customer-to-customer arcs, which kills subtours;
    the variable bounds q_i <= u_i <= Q enforce capacity.
    """
    n, Q, q = data["n"], data["Q"], data["q"]
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if i != j:
                model.addConstr(u[j] >= u[i] + q[j] - Q * (1 - x[i, j]), name=f"load[{i},{j}]")


def build_cvrp_two_index(data: dict) -> tuple[gp.Model, gp.tupledict]:
    """Two-index CVRP. data keys: n, K, Q, q (length n+1, q[0]=0), c (cost matrix)."""
    n, Q, q, c = data["n"], data["Q"], data["q"], data["c"]
    nodes = range(n + 1)
    arcs = [(i, j) for i in nodes for j in nodes if i != j]
    model = gp.Model("cvrp_two_index")
    x = model.addVars(arcs, vtype=GRB.BINARY, name="x")
    u = model.addVars(range(1, n + 1), lb=[q[i] for i in range(1, n + 1)], ub=Q, name="u")
    model.setObjective(gp.quicksum(c[i][j] * x[i, j] for i, j in arcs), GRB.MINIMIZE)
    add_degree_constraints(model, x, data)
    add_capacity_constraints(model, x, u, data)
    return model, x


def extract_routes(x: gp.tupledict) -> list[list[int]]:
    """Recover routes by following selected arcs from the depot."""
    succ = {i: j for (i, j), var in x.items() if i != 0 and var.X > 0.5}
    starts = [j for (i, j), var in x.items() if i == 0 and var.X > 0.5]
    routes = []
    for s in starts:
        route, v = [], s
        while v != 0:
            route.append(v)
            v = succ[v]
        routes.append(route)
    return routes


# Tiny instance: depot at origin, three customers on the x-axis, two on the y-axis.
pts = [(0, 0), (1, 0), (2, 0), (3, 0), (0, 2), (0, 4)]
c = [[math.dist(a, b) for b in pts] for a in pts]
data = {"n": 5, "K": 2, "Q": 10, "q": [0, 3, 3, 3, 5, 5], "c": c}
model, x = build_cvrp_two_index(data)
model.Params.OutputFlag = 0
model.Params.TimeLimit = 30
model.optimize()
if model.Status == GRB.OPTIMAL or (model.Status == GRB.TIME_LIMIT and model.SolCount > 0):
    print(round(model.ObjVal, 2), extract_routes(x))
# Expected: 14.0 with routes [1, 2, 3] and [4, 5], possibly direction-reversed
# (costs are symmetric): out-and-back along each axis
```

Always check `model.Status` before touching `.X`; with a time limit, additionally require `model.SolCount > 0`. Report `model.MIPGap` alongside the objective — on MTZ-load models the gap, not the incumbent, is usually the bottleneck.

### VRPTW, two-index with time propagation

Time variables make the load constraints redundant for subtour elimination, but capacity still needs them. The per-arc big-M below is the tightest valid constant; with a global big-M the root relaxation collapses toward the assignment bound.

```python
import math
import gurobipy as gp
from gurobipy import GRB


def add_degree_constraints(model: gp.Model, x: gp.tupledict, data: dict) -> None:
    """One arc in and one arc out per customer; at most K vehicles leave the depot."""
    n, K = data["n"], data["K"]
    nodes = range(n + 1)
    for i in range(1, n + 1):
        model.addConstr(gp.quicksum(x[i, j] for j in nodes if j != i) == 1, name=f"out[{i}]")
        model.addConstr(gp.quicksum(x[j, i] for j in nodes if j != i) == 1, name=f"in[{i}]")
    model.addConstr(gp.quicksum(x[0, j] for j in range(1, n + 1)) <= K, name="fleet")


def add_load_constraints(model: gp.Model, x: gp.tupledict, u: gp.tupledict, data: dict) -> None:
    """Capacity via load propagation (subtours are already cut by the time variables)."""
    n, Q, q = data["n"], data["Q"], data["q"]
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if i != j:
                model.addConstr(u[j] >= u[i] + q[j] - Q * (1 - x[i, j]), name=f"load[{i},{j}]")


def add_time_window_constraints(model: gp.Model, x: gp.tupledict, t: gp.tupledict, data: dict) -> None:
    """Service-start propagation with the tightest valid per-arc big-M."""
    n, a, b, s, tau = data["n"], data["a"], data["b"], data["s"], data["tau"]
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if i != j:
                m_ij = max(0.0, b[i] + s[i] + tau[i][j] - a[j])
                model.addConstr(
                    t[j] >= t[i] + s[i] + tau[i][j] - m_ij * (1 - x[i, j]),
                    name=f"time[{i},{j}]",
                )
    for j in range(1, n + 1):
        model.addConstr(t[j] >= tau[0][j] * x[0, j], name=f"depart[{j}]")
        m_j0 = max(0.0, b[j] + s[j] + tau[j][0] - b[0])
        model.addConstr(
            t[j] + s[j] + tau[j][0] <= b[0] + m_j0 * (1 - x[j, 0]), name=f"return[{j}]"
        )


def build_vrptw(data: dict) -> tuple[gp.Model, gp.tupledict, gp.tupledict]:
    """Two-index VRPTW. data adds a, b (windows), s (service), tau (travel) to CVRP data."""
    n, q, Q, c, a, b = data["n"], data["q"], data["Q"], data["c"], data["a"], data["b"]
    nodes = range(n + 1)
    arcs = [(i, j) for i in nodes for j in nodes if i != j]
    model = gp.Model("vrptw_two_index")
    x = model.addVars(arcs, vtype=GRB.BINARY, name="x")
    u = model.addVars(range(1, n + 1), lb=[q[i] for i in range(1, n + 1)], ub=Q, name="u")
    t = model.addVars(range(1, n + 1), lb=[a[i] for i in range(1, n + 1)],
                      ub=[b[i] for i in range(1, n + 1)], name="t")
    model.setObjective(gp.quicksum(c[i][j] * x[i, j] for i, j in arcs), GRB.MINIMIZE)
    add_degree_constraints(model, x, data)
    add_load_constraints(model, x, u, data)
    add_time_window_constraints(model, x, t, data)
    return model, x, t


# Tiny instance: customer 1 must be served early, customer 2 only after time 3.
pts = [(0, 0), (1, 0), (2, 0), (0, 2)]
c = [[math.dist(p1, p2) for p2 in pts] for p1 in pts]
data = {
    "n": 3, "K": 2, "Q": 8, "q": [0, 4, 4, 4], "c": c, "tau": c,
    "a": [0.0, 0.0, 3.0, 0.0], "b": [100.0, 2.0, 10.0, 10.0],
    "s": [0.0, 0.5, 0.5, 0.5],
}
model, x, t = build_vrptw(data)
model.Params.OutputFlag = 0
model.optimize()
if model.Status == GRB.OPTIMAL:
    arcs_used = sorted((i, j) for (i, j), v in x.items() if v.X > 0.5)
    print(round(model.ObjVal, 2), arcs_used)
# Expected: 8.0 with arcs [(0, 1), (0, 3), (1, 2), (2, 0), (3, 0)];
# the vehicle waits at customer 2 until its window opens (t[2] = 3.0)
```

For multi-depot or heterogeneous fleets, switch to three-index variables and write one builder per family (`add_assignment_constraints` linking $y_{ik}$ to $x_{ijk}$, `add_vehicle_capacity_constraints` with per-type $Q_k$), and add symmetry-breaking constraints among identical vehicles before anything else.

## Instances and Independent Validation

Treat validation as non-negotiable: every solver result is checked by code that shares nothing with the model. The generator is seeded and parameterized so experiments are reproducible; the validator recomputes feasibility and objective from raw data.

### Seeded instance generator

```python
import numpy as np


def generate_cvrp_instance(
    n: int,
    seed: int,
    clustered: bool = False,
    demand_low: int = 1,
    demand_high: int = 9,
    avg_route_size: float = 8.0,
    fleet_slack: float = 1.3,
) -> dict:
    """Synthetic CVRP instance in the spirit of Uchoa et al. (2017) X-instances.

    Returns n, coords ((n+1) x 2, depot first), c (Euclidean matrix),
    q (demands, q[0] = 0), capacity Q, fleet size K.
    """
    rng = np.random.default_rng(seed)
    if clustered:
        n_centers = max(2, n // 25)
        centers = rng.uniform(10.0, 90.0, size=(n_centers, 2))
        which = rng.integers(0, n_centers, size=n)
        coords = np.clip(centers[which] + rng.normal(0.0, 6.0, size=(n, 2)), 0.0, 100.0)
    else:
        coords = rng.uniform(0.0, 100.0, size=(n, 2))
    coords = np.vstack([[50.0, 50.0], coords])
    diff = coords[:, None, :] - coords[None, :, :]
    c = np.sqrt((diff ** 2).sum(axis=2))
    q = np.concatenate([[0], rng.integers(demand_low, demand_high + 1, size=n)])
    Q = int(np.ceil(avg_route_size * q[1:].mean()))
    K = int(np.ceil(fleet_slack * q[1:].sum() / Q))
    return {"n": n, "coords": coords, "c": c, "q": q, "Q": Q, "K": K}


def add_time_windows(
    data: dict, seed: int, horizon: float = 1000.0, width: float = 60.0, service: float = 10.0
) -> dict:
    """Solomon-style windows: each window is placed so the customer is reachable
    from the depot and the vehicle can still return before the horizon."""
    rng = np.random.default_rng(seed)
    n, c = data["n"], data["c"]
    slack = np.maximum(1.0, horizon - 2.0 * c[0, 1:] - width - service)
    center = c[0, 1:] + rng.uniform(0.0, 1.0, size=n) * slack
    a = np.concatenate([[0.0], np.maximum(center - width / 2.0, c[0, 1:])])
    b = np.concatenate([[horizon], center + width / 2.0])
    out = dict(data)
    out.update({"a": a, "b": b, "s": np.concatenate([[0.0], np.full(n, service)]),
                "tau": data["c"]})
    return out


inst = generate_cvrp_instance(n=30, seed=42, clustered=True)
print(inst["Q"], inst["K"], inst["q"][1:6].tolist())
# Expected: deterministic for seed 42 — Q = 38, K = 5, demands [4, 4, 4, 8, 3];
# rerunning with the same seed reproduces identical values
```

Uniform vs clustered customer placement changes which heuristics shine: sweep degrades on clustered data with the depot inside a cluster, and related removal in ALNS gains value. Generate both when benchmarking. For standard benchmark files (CVRPLIB, Solomon) and their exact rounding conventions, see instance-generation-and-benchmarks.

### Independent feasibility and objective validator

```python
import numpy as np


def validate_cvrp(routes: list[list[int]], data: dict) -> tuple[bool, float, list[str]]:
    """Independent check of a CVRP/VRPTW solution. Shares no code with any solver.

    Verifies visit-exactly-once, no depot inside routes, per-route capacity,
    fleet size, and (if windows are present) time feasibility with waiting.
    Returns (feasible, recomputed_cost, error_messages).
    """
    n, Q, K = data["n"], data["Q"], data["K"]
    q = np.asarray(data["q"], dtype=float)
    c = np.asarray(data["c"], dtype=float)
    errors: list[str] = []
    visited = sorted(v for r in routes for v in r)
    if visited != list(range(1, n + 1)):
        errors.append("customer set mismatch: every customer 1..n must appear exactly once")
    if len(routes) > K:
        errors.append(f"{len(routes)} routes exceed fleet size K={K}")
    cost = 0.0
    for idx, r in enumerate(routes):
        if not r or 0 in r:
            errors.append(f"route {idx} is empty or contains the depot")
            continue
        load = float(q[r].sum())
        if load > Q + 1e-9:
            errors.append(f"route {idx} load {load:.1f} exceeds capacity {Q}")
        path = np.array([0] + list(r) + [0])
        cost += float(c[path[:-1], path[1:]].sum())
    if "a" in data:
        a, b, s, tau = data["a"], data["b"], data["s"], data["tau"]
        for idx, r in enumerate(routes):
            t, prev = 0.0, 0
            for v in r:
                t = max(a[v], t + s[prev] + tau[prev][v])
                if t > b[v] + 1e-9:
                    errors.append(f"route {idx}: window missed at {v} (t={t:.2f} > b={b[v]:.2f})")
                prev = v
            if t + s[prev] + tau[prev][0] > b[0] + 1e-9:
                errors.append(f"route {idx} returns to the depot after the horizon")
    return (not errors), cost, errors


data = {"n": 4, "q": [0, 3, 3, 3, 3], "Q": 6, "K": 2,
        "c": [[0, 1, 2, 2, 1], [1, 0, 1, 3, 2], [2, 1, 0, 3, 3],
              [2, 3, 3, 0, 1], [1, 2, 3, 1, 0]]}
print(validate_cvrp([[1, 2], [3, 4]], data))
print(validate_cvrp([[1, 2, 3], [4]], data)[2])
# Expected: (True, 8.0, []) for the first call;
# the second reports a capacity violation on route 0 (load 9 > 6)
```

Run the validator on every solution any method returns, including the MIP's — it catches model bugs (a missing degree constraint produces "optimal" solutions that skip customers) and convention mismatches (service time counted in one place but not the other).

## Construction Heuristics

Construction gives the MIP a warm start, the ALNS an initial solution, and dispatchers a sane fallback. Savings is the robust default; sweep needs planar coordinates and a depot that is not inside a dense cluster.

### Clarke-Wright savings

Merging two out-and-back routes that end at $i$ and start at $j$ saves $s_{ij} = c_{0i} + c_{0j} - c_{ij} \ge 0$ (triangle inequality). The parallel variant (Clarke & Wright 1964, "Scheduling of Vehicles from a Central Depot to a Number of Delivery Points") sorts all savings once and merges greedily at route endpoints. Complexity is $O(n^2 \log n)$ for the sort; quality is typically 5-10% above optimal on Euclidean instances.

```python
import numpy as np


def clarke_wright(c: np.ndarray, q: np.ndarray, Q: float) -> list[list[int]]:
    """Parallel Clarke-Wright savings for the CVRP.

    Starts from one out-and-back route per customer and merges endpoint pairs
    in order of decreasing savings s_ij = c_0i + c_0j - c_ij, respecting capacity.
    """
    n = len(q) - 1
    routes: dict[int, list[int]] = {i: [i] for i in range(1, n + 1)}
    load: dict[int, float] = {i: float(q[i]) for i in range(1, n + 1)}
    of: dict[int, int] = {i: i for i in range(1, n + 1)}  # customer -> route id
    sav = c[0][:, None] + c[0][None, :] - c               # vectorized savings matrix
    iu, ju = np.triu_indices(n + 1, k=1)
    keep = iu >= 1                                        # customer pairs only
    iu, ju = iu[keep], ju[keep]
    for k in np.argsort(-sav[iu, ju]):
        i, j = int(iu[k]), int(ju[k])
        ri, rj = of[i], of[j]
        if ri == rj or load[ri] + load[rj] > Q:
            continue
        ra, rb = routes[ri], routes[rj]
        if ra[-1] == i and rb[0] == j:
            merged = ra + rb
        elif rb[-1] == j and ra[0] == i:
            merged = rb + ra
        elif ra[0] == i and rb[0] == j:
            merged = ra[::-1] + rb
        elif ra[-1] == i and rb[-1] == j:
            merged = ra + rb[::-1]
        else:
            continue                                      # i or j is interior: skip
        routes[ri] = merged
        load[ri] += load[rj]
        del routes[rj], load[rj]
        for v in merged:
            of[v] = ri
    return list(routes.values())


pts = np.array([(0, 0), (1, 0), (2, 0), (3, 0), (0, 2), (0, 4)], dtype=float)
c = np.sqrt(((pts[:, None] - pts[None, :]) ** 2).sum(axis=2))
q = np.array([0, 3, 3, 3, 5, 5], dtype=float)
print(clarke_wright(c, q, Q=10.0))
# Expected: [[1, 2, 3], [4, 5]] — cost 14.0, the MIP optimum on this instance
```

### Sweep

Sweep (Gillett & Miller 1974, "A Heuristic Algorithm for the Vehicle-Dispatch Problem") clusters first and routes second: sort customers by polar angle around the depot, cut the circular order into capacity-feasible sectors, then sequence each sector as a small TSP. Run it from several start angles and keep the best.

```python
import math
import numpy as np


def sweep(coords: np.ndarray, q: np.ndarray, Q: float, start_angle: float = 0.0) -> list[list[int]]:
    """Sweep construction: angular clusters cut at capacity, nearest-neighbor sequencing.

    coords[0] is the depot. Replace the nearest-neighbor step with 2-opt
    (see traveling-salesman-problem) for a few percent extra quality.
    """
    n = len(q) - 1
    rel = coords[1:] - coords[0]
    angles = (np.arctan2(rel[:, 1], rel[:, 0]) - start_angle) % (2.0 * math.pi)
    order = (np.argsort(angles) + 1).tolist()
    clusters: list[list[int]] = []
    cur: list[int] = []
    load = 0.0
    for v in order:
        if cur and load + q[v] > Q:
            clusters.append(cur)
            cur, load = [], 0.0
        cur.append(v)
        load += float(q[v])
    if cur:
        clusters.append(cur)
    dist = np.sqrt(((coords[:, None, :] - coords[None, :, :]) ** 2).sum(axis=2))
    routes = []
    for cl in clusters:
        rest, here, route = set(cl), 0, []
        while rest:
            nxt = min(rest, key=lambda v: dist[here, v])
            route.append(nxt)
            rest.remove(nxt)
            here = nxt
        routes.append(route)
    return routes


pts = np.array([(0, 0), (1, 0), (2, 0), (3, 0), (0, 2), (0, 4)], dtype=float)
q = np.array([0, 3, 3, 3, 5, 5], dtype=float)
print(sweep(pts, q, Q=10.0))
# Expected: [[1, 2, 3], [4, 5]] — the angular order groups the x-axis customers,
# then the y-axis customers, and capacity cuts exactly between the groups
```

For VRPTW, the standard construction is Solomon's I1 insertion (Solomon 1987, "Algorithms for the Vehicle Routing and Scheduling Problems with Time Window Constraints"): seed each route with the farthest or most time-critical customer, then repeatedly insert the customer with the best weighted distance-and-delay score at its cheapest feasible position. Its insertion-cost machinery is exactly the repair operator of the ALNS below, so implement it once.

## ALNS and OR-Tools Routing

### Compact ALNS for the CVRP

ALNS (Ropke & Pisinger 2006, "An Adaptive Large Neighborhood Search Heuristic for the Pickup and Delivery Problem with Time Windows"; generalized in Pisinger & Ropke 2007, "A general heuristic for vehicle routing problems") is the method of choice when you write a VRP heuristic yourself: destroy operators remove customers, repair operators reinsert them, simulated-annealing acceptance keeps the walk moving, and operator weights adapt per segment. The version below is intentionally compact — two removal operators, greedy insertion with vectorized position costs, fleet treated as open (the validator checks K afterwards). For regret-k repair, noise, route-removal operators, and acceptance alternatives, use the full engine in large-neighborhood-search.

```python
import math
import numpy as np

def total_cost(c: np.ndarray, routes: list[list[int]]) -> float:
    """Recompute the objective from the distance matrix."""
    cost = 0.0
    for r in routes:
        path = np.array([0] + r + [0])
        cost += float(c[path[:-1], path[1:]].sum())
    return cost

def greedy_insert(c: np.ndarray, q: np.ndarray, Q: float, routes: list[list[int]],
                  removed: list[int], rng: np.random.Generator) -> list[list[int]]:
    """Reinsert removed customers at their cheapest feasible position (vectorized per route)."""
    loads = [float(q[r].sum()) for r in routes]
    for cust in rng.permutation(removed).tolist():
        best, where = math.inf, None
        for ri, r in enumerate(routes):
            if loads[ri] + q[cust] > Q:
                continue
            seq = np.array([0] + r + [0])
            delta = c[seq[:-1], cust] + c[cust, seq[1:]] - c[seq[:-1], seq[1:]]
            p = int(np.argmin(delta))
            if delta[p] < best:
                best, where = float(delta[p]), (ri, p)
        if where is None:
            routes.append([cust])
            loads.append(float(q[cust]))
        else:
            ri, p = where
            routes[ri].insert(p, cust)
            loads[ri] += float(q[cust])
    return routes

def alns_cvrp(c: np.ndarray, q: np.ndarray, Q: float, routes0: list[list[int]],
              iters: int = 20000, seed: int = 0) -> tuple[list[list[int]], float]:
    """Compact ALNS: random + related removal, greedy insertion, SA acceptance,
    segment-based adaptive operator weights. See large-neighborhood-search."""
    rng = np.random.default_rng(seed)
    n = len(q) - 1
    cur = [r[:] for r in routes0 if r]
    f_cur = total_cost(c, cur)
    best, f_best = [r[:] for r in cur], f_cur
    T = 0.05 * f_cur / math.log(2)                 # accept 5%-worse with prob 0.5
    cool = (1e-4) ** (1.0 / iters)
    w, pi, theta = np.ones(2), np.zeros(2), np.zeros(2)
    for it in range(iters):
        op = int(rng.choice(2, p=w / w.sum()))
        k = int(rng.integers(2, max(3, n // 4) + 1))
        if op == 0:                                # random removal
            removed = rng.choice(np.arange(1, n + 1), size=min(k, n), replace=False).tolist()
        else:                                      # related removal: a seed and its neighbors
            s = int(rng.integers(1, n + 1))
            removed = (np.argsort(c[s, 1:n + 1])[:min(k, n)] + 1).tolist()
        gone = set(removed)
        cand = [[v for v in r if v not in gone] for r in cur]
        cand = greedy_insert(c, q, Q, [r for r in cand if r], removed, rng)
        f_cand = total_cost(c, cand)
        score = 0.0
        if f_cand < f_best - 1e-9:
            best, f_best, score = [r[:] for r in cand], f_cand, 3.0
        if f_cand < f_cur or rng.random() < math.exp(-(f_cand - f_cur) / max(T, 1e-12)):
            cur, f_cur, score = cand, f_cand, max(score, 1.0)
        pi[op] += score
        theta[op] += 1.0
        T *= cool
        if (it + 1) % 100 == 0:                    # segment weight update
            used = theta > 0
            w[used] = 0.8 * w[used] + 0.2 * (pi[used] / theta[used] + 0.01)
            pi[:], theta[:] = 0.0, 0.0
    return best, f_best

rng = np.random.default_rng(7)
pts = np.vstack([[50.0, 50.0], rng.uniform(0, 100, size=(20, 2))])
c = np.sqrt(((pts[:, None] - pts[None, :]) ** 2).sum(axis=2))
q = np.concatenate([[0], rng.integers(1, 10, size=20)])
init = [[i] for i in range(1, 21)]                 # one out-and-back route per customer
routes, f = alns_cvrp(c, q, Q=40.0, routes0=init, iters=4000, seed=1)
print(round(f, 1), len(routes), round(total_cost(c, init), 1))
# Expected: cost 549.2 over 3 routes, down from 1580.2 for the one-customer-per-route start
```

Two implementation points carry most of the speed: the insertion deltas are computed with one vectorized expression per route instead of a Python loop over positions, and the candidate is rebuilt by filtering lists rather than deep-copying objects. For serious instances add: route-removal and worst-removal operators, regret-2 insertion, a granular neighbor list to restrict insertion positions, and intra-route 2-opt on improved solutions (from traveling-salesman-problem).

### OR-Tools routing layer

OR-Tools is the fastest path to a working VRP solver with side constraints: capacities, time windows, pickup-delivery pairs, and penalties for dropping visits are all built in. Costs must be integers — scale floats by 100 or 1000 and report the scale. The default improvement metaheuristic to request is guided local search (see guided-local-search for why it escapes local optima that plain local search cannot).

```python
import math
from ortools.constraint_solver import pywrapcp, routing_enums_pb2


def solve_cvrp_ortools(dist: list[list[int]], demands: list[int], Q: int, K: int,
                       seconds: int = 10) -> tuple[list[list[int]], int]:
    """CVRP with the OR-Tools routing layer: path-cheapest-arc start + guided local search.

    dist must contain integers (scale float distances before calling).
    Returns (routes, objective) or ([], -1) if no solution was found.
    """
    manager = pywrapcp.RoutingIndexManager(len(dist), K, 0)
    routing = pywrapcp.RoutingModel(manager)

    def arc_cb(i: int, j: int) -> int:
        return dist[manager.IndexToNode(i)][manager.IndexToNode(j)]

    transit = routing.RegisterTransitCallback(arc_cb)
    routing.SetArcCostEvaluatorOfAllVehicles(transit)

    def demand_cb(i: int) -> int:
        return demands[manager.IndexToNode(i)]

    dem = routing.RegisterUnaryTransitCallback(demand_cb)
    routing.AddDimensionWithVehicleCapacity(dem, 0, [Q] * K, True, "Load")
    params = pywrapcp.DefaultRoutingSearchParameters()
    params.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    params.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    params.time_limit.FromSeconds(seconds)
    sol = routing.SolveWithParameters(params)
    if sol is None:
        return [], -1
    routes = []
    for v in range(K):
        idx, route = routing.Start(v), []
        while not routing.IsEnd(idx):
            node = manager.IndexToNode(idx)
            if node != 0:
                route.append(node)
            idx = sol.Value(routing.NextVar(idx))
        if route:
            routes.append(route)
    return routes, sol.ObjectiveValue()


pts = [(0, 0), (1, 0), (2, 0), (3, 0), (0, 2), (0, 4)]
dist = [[int(round(100 * math.dist(a, b))) for b in pts] for a in pts]
routes, obj = solve_cvrp_ortools(dist, [0, 3, 3, 3, 5, 5], Q=10, K=2, seconds=2)
print(obj, routes)
# Expected: 1400 (distance 14.0 at scale 100) with routes [1, 2, 3] and [4, 5]
```

For time windows, add a second dimension with the travel-plus-service callback, then set `CumulVar(index).SetRange(a_i, b_i)` per customer and give vehicles slack for waiting (`AddDimension(transit_time_cb, waiting_slack, horizon, False, "Time")`). To allow dropping customers at a penalty (a request bank), call `routing.AddDisjunction([manager.NodeToIndex(i)], penalty)` per customer — essential when feasibility is not guaranteed.

## Advanced Techniques

### Rounded capacity cuts via lazy constraints

The MTZ-load model is compact but weak. The branch-and-cut alternative drops the load variables and separates the rounded capacity inequalities at integer candidates inside a Gurobi callback (`where == GRB.Callback.MIPSOL`): read the candidate arcs, build the support graph on customers only, find its connected components, and for each component $S$ that is disconnected from the depot or violates $\sum_{i \in S, j \notin S} x_{ij} \ge \lceil q(S)/Q \rceil$, add the cut with `model.cbLazy`. Set `model.Params.LazyConstraints = 1`. This connected-component separation is exact for integer points; fractional separation needs heuristics or the CVRPSEP routines of Lysgaard, Letchford & Eglese (2004), "A new branch-and-cut algorithm for the capacitated vehicle routing problem." The callback pattern is the same as TSP subtour elimination — reuse it from traveling-salesman-problem.

### Set partitioning and branch-cut-and-price

The strongest known bounds come from the set-partitioning view: minimize $\sum_r c_r \lambda_r$ over feasible routes $r$, subject to $\sum_r a_{ir} \lambda_r = 1$ per customer and $\sum_r \lambda_r \le K$. The LP is solved by column generation; pricing is an elementary shortest path with resource constraints (capacity, time) solved by a labeling algorithm. Modern codes add ng-route relaxations, rank-1 cuts, and route enumeration (Pecin et al. 2017; Pessoa et al. 2020, the VRPSolver framework). Build this only when bounds matter: the pricing labeling algorithm is the dominant engineering cost. The decomposition mechanics and stabilization live in column-generation.

### Granular neighborhoods

Local search and insertion over all $O(n^2)$ arcs wastes time on hopeless long arcs. Granular search (Toth & Vigo 2003, "The granular tabu search and its application to the vehicle-routing problem") restricts moves to a sparse arc set — typically each customer's 10-30 nearest neighbors plus depot arcs — cutting move evaluation by an order of magnitude with negligible quality loss. Apply the same neighbor lists inside ALNS repair (only test insertions adjacent to near neighbors) and related removal. This single change usually separates a toy VRP code from one that handles 1000 customers.

### Multi-depot and heterogeneous fleet

MDVRP: either a three-index model with depot-indexed vehicles, or — often better — cluster customers to depots first (assignment by distance with capacity budgets), then solve one CVRP per depot and let an improvement phase reassign border customers. In ALNS, add a removal operator that frees all customers of one depot's border region. HFVRP: three-index MIP with per-type capacity $Q_k$ and fixed cost $f_k$ in the objective; in heuristics, evaluate insertion against the cheapest feasible vehicle type and include fleet-mix moves (upgrade/downgrade a route's vehicle). Hybrid genetic search handles both variants well (Vidal et al. 2012, "A hybrid genetic algorithm for multidepot and periodic vehicle routing problems").

### Pickup-and-delivery overview

PDPTW couples requests: pickup $p$ and delivery $d$ must be on the same route with $t_p \le t_d$, and load now goes up and down along the route, so the running-load profile (not the total) must stay within $[0, Q]$. In MIPs this means pairing constraints and load propagation per arc; in ALNS, destroy/repair must remove and reinsert the pair as a unit — which is precisely the setting ALNS was invented for (Ropke & Pisinger 2006). Dial-a-ride adds ride-time limits per request. If a user describes "transport from A to B" requests rather than depot deliveries, route the discussion through this variant immediately; CVRP code does not adapt incrementally.

## Practical Challenges

**The two-index MIP stalls beyond ~40 customers.** This is expected, not a bug. Order the escalation: tighten the formulation (lazy rounded capacity cuts instead of MTZ-load), warm start with Clarke-Wright plus 2-opt via `var.Start`, give the solver a target gap (`model.Params.MIPGap = 0.01`) instead of demanding optimality, and past that switch to ALNS or PyVRP with the MIP retained only on small instances for validation.

**The LP gap looks terrible even on small instances.** The MTZ-load relaxation is structurally weak — root gaps of 20-40% are normal. Do not conclude the instance is hard. Compare against the cut-based bound before judging; if the cut model's root gap is also large, demands are probably tight relative to Q (bin-packing hardness), and a packing-aware construction matters more than the solver.

**The heuristic uses more vehicles than the fleet owns.** Open-fleet heuristics (including the compact ALNS above) may return more than K routes. Either add a high fixed cost per route to the objective so route count is squeezed first, or run a route-elimination phase (remove the route with least demand, reinsert its customers, accept if feasible), or hand minimum-vehicle solutions to OR-Tools with K fixed. Always re-check K with the validator.

**Objectives disagree between your code and the benchmark's best known.** Almost always a rounding convention: CVRPLIB instances use integer-rounded Euclidean distances, Solomon VRPTW uses truncated-to-one-decimal travel times in much of the literature. Fix one convention in the instance data itself (round the matrix once, at load time), never inside objective functions, and document it in the results table.

**Construction fails on tight time windows.** Savings and sweep ignore windows; naive insertion dead-ends with unplaceable customers. Use Solomon I1 with time-feasibility checks, keep a request bank for the leftovers, and let ALNS reinsert them at a decreasing penalty. If even that fails, check whether windows are satisfiable at all: solve a one-customer-per-route feasibility check first — if customer i cannot be reached inside its window even alone, the instance is infeasible, not the algorithm wrong.

**Asymmetric road-network travel times break Euclidean assumptions.** One-way streets make $\tau_{ij} \neq \tau_{ji}$; sweep and savings quality degrades and 2-opt's reversal moves change cost in non-obvious ways (a reversed segment costs differently). Use the directed formulations given above (they never assumed symmetry), prefer Or-opt (segment relocation without reversal) over 2-opt, and get the matrix from a routing engine rather than haversine distance — duty-time legality often depends on it.

**Per-iteration cost explodes with instance size.** Profile before optimizing, but the usual fixes are: distance matrix precomputed once as a numpy array (never recompute coordinates-to-distance in the loop), granular neighbor lists for insertion candidates, incremental route loads (maintained, not re-summed), and route-level cost deltas instead of full-solution recomputation. The compact ALNS above recomputes full cost for clarity; replacing `total_cost` with delta bookkeeping is the first scaling step.

**Stochastic results are not reproducible.** Every run must record (instance id, seed, algorithm, parameters, time limit, objective, vehicles). Use `np.random.default_rng(seed)` exclusively — no global `np.random` state — and validate every reported solution with `validate_cvrp` before it enters a results table.

## Tools & Libraries

| Library | When to use | Note |
|---|---|---|
| gurobipy | Exact two-/three-index MIPs, lazy-cut branch-and-cut, warm starts | Commercial license; the reference for optimality proofs up to ~50 customers |
| OR-Tools routing | Production VRP with windows, capacities, drops, pickup-delivery | Integer costs only; GLS default; strong out of the box, limited bound information |
| PyVRP | Benchmark-quality heuristics for CVRP/VRPTW with zero tuning | Open-source hybrid genetic search (Vidal 2022 lineage); Python interface, C++ core |
| vrplib | Reading CVRPLIB/Solomon instance and solution files | Handles the rounding conventions for you; pairs with instance-generation-and-benchmarks |
| VRPSolver (BaPCod) | Research-grade exact branch-cut-and-price | Pessoa et al. (2020); steep setup, state-of-the-art exact results |
| LKH-3 | Heuristic for many VRP variants via transformation | Helsgaun's extension of Lin-Kernighan; external binary, excellent on large CVRP |
| networkx | Graph utilities, quick shortest paths for road-network preprocessing | Not a VRP solver; use for data preparation only |
| numpy | Distance matrices, vectorized insertion deltas, ALNS internals | The implementation substrate for everything heuristic in this skill |

## Output Format

A complete VRP deliverable contains:

1. **Problem and model summary.**

| Item | Value |
|---|---|
| Variant | CVRP (capacity only), directed |
| Customers / fleet | n = 100, K = 12, Q = 180 |
| Formulation | two-index, MTZ-load capacity, lazy RC cuts off |
| Distance convention | Euclidean, rounded to integer (CVRPLIB) |
| Method | Clarke-Wright start + ALNS (20k iterations, seed 17) |

2. **Solution-quality report.** Objective as recomputed by the independent validator (never the solver's internal number alone), vehicles used vs available, gap to best known or to the MIP bound where one exists, wall-clock time, and seed. For stochastic methods: best/mean/std over at least 10 seeds.

3. **Per-route table.**

| Route | Sequence | Load/Q | Distance |
|---|---|---|---|
| 1 | 0-14-7-23-0 | 162/180 | 1043 |
| 2 | 0-3-91-44-60-0 | 175/180 | 1188 |

4. **Validation line.** Explicit statement: `validate_cvrp: feasible=True, cost=10412, errors=[]` — the recomputed cost must equal the reported objective to within rounding tolerance, and any mismatch is a finding, not a footnote.

5. **Reproducibility block.** Instance file or generator call with seed, full parameter set, library versions, and time limits, sufficient for a third party to regenerate every number.

6. **File artifacts when requested.** Solution in CVRPLIB `.sol` format (one `Route #k:` line per route plus `Cost`), results CSV with one row per run, and a route plot (depot starred, one color per route) if visualization is wanted.

## Questions to Ask

- Which constraints exist besides capacity — time windows, multiple depots, different vehicle types, pickups with deliveries, maximum route duration?
- Is the number of vehicles fixed, to be minimized, or effectively unlimited?
- How large are the instances (customers, vehicles), and how many must be solved how often?
- Where do distances come from — coordinates or a road-network matrix — and is travel asymmetric?
- What is the time budget per instance, and is a proof of optimality required or just a good plan?
- Is a Gurobi license available, or should everything run on open-source tools?
- Can customers ever be left unserved at a penalty, or is full coverage a hard requirement?
- Are there established benchmark instances or best-known values this work must be compared against?
- What objective exactly — distance, time, vehicle fixed costs, or a hierarchy of these?

## Related Skills

- **traveling-salesman-problem** — when there is a single vehicle, or for the intra-route machinery every VRP method reuses: 2-opt/Or-opt, nearest-neighbor construction, and subtour-elimination callbacks.
- **large-neighborhood-search** — when the compact ALNS here needs the full engine: more destroy/repair operators, regret insertion, adaptive weights, acceptance calibration, and noise.
- **column-generation** — when bounds or exact solutions are needed beyond MIP reach: set partitioning over routes with shortest-path pricing and branch-and-price.
- **vehicle-platooning-optimization** — when vehicles coordinate to share road segments rather than serve capacitated delivery demands; routing structure overlaps, objectives differ.
- **guided-local-search** — when using OR-Tools routing (GLS is its workhorse metaheuristic) or building penalty-based escapes over relocate/exchange neighborhoods.
- **instance-generation-and-benchmarks** — when parsing CVRPLIB/Solomon files, choosing benchmark subsets, or designing synthetic instance families beyond the generator in this skill.
