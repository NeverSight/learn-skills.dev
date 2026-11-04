---
name: network-flow-optimization
description: When the user wants to solve flow problems on a network - max-flow/min-cut, min-cost flow, multicommodity flow, or shortest paths via Dijkstra, Bellman-Ford, and label-correcting methods - using networkx, gurobipy, or specialized algorithms, including when total unimodularity makes LP solutions integral for free. Also use when the user mentions "network flow," "min-cost flow," "max flow," "multicommodity," "shortest path," "flow conservation," or when the constraints have flow-balance structure on a graph. For one-to-one matching, see assignment-problems; for duality and sensitivity background, see linear-programming-fundamentals.
---

# Network Flow Optimization

You are an expert in network flow optimization: shortest paths, maximum flow,
minimum-cost flow, and multicommodity flow. This skill covers the LP/MIP view
(total unimodularity, when integrality is free, when it is lost), dedicated
combinatorial algorithms, and networkx + gurobipy implementations, plus
instance generation and independent validation. Use the framework below to
classify the problem, pick the cheapest adequate method, and verify the result.

## Initial Assessment

Establish these points before formulating or recommending a method:

- **Which flow problem is it, exactly?** Shortest path, max flow, min-cost
  flow, transshipment, or multicommodity? Many word problems hide a pure flow
  structure; finding it replaces a MIP solve with a polynomial algorithm.
- **Single commodity or several?** One commodity keeps total unimodularity
  and free integrality. Commodities that share arc capacities destroy both;
  the splittable version is still an LP, the unsplittable version is NP-hard.
- **Side constraints.** Fixed charges for opening arcs, logical conditions,
  budget constraints, or arc-flow lower bounds tied to binaries all break the
  network structure. Plan for a MIP the moment one appears.
- **Sizes.** Nodes n, arcs m, commodities K. networkx handles m up to ~10^5
  comfortably; OR-Tools' C++ flow solvers handle 10^6-10^7 arcs; the LP/MIP
  route in Gurobi handles n_vars = m·K, so estimate that product early.
- **Sign of arc costs.** Negative costs rule out plain Dijkstra. Check for
  negative cycles: with them, min-cost flow needs care and shortest path
  becomes NP-hard (it turns into longest path).
- **Directed or undirected.** Most algorithms and all formulations below
  assume directed arcs. Undirected edges with nonnegative cost become two
  opposite arcs; with negative cost they do not, so flag that case.
- **Data type.** Integral capacities/demands enable the integrality theorem
  and networkx's `min_cost_flow` (which requires integers). Float data must
  be scaled, or you must use the LP route.
- **Balance check.** Do supplies equal demands (sum of b_i = 0)? If not,
  decide where the slack goes (dummy node, inequality balances).
- **Solve count.** One-off solve, or thousands of shortest-path calls inside
  a pricing loop or heuristic? Embedded use changes tooling (reusable arrays,
  scipy.csgraph, warm potentials).
- **Solver availability.** Gurobi licensed? If not, networkx + OR-Tools +
  scipy cover everything here; the LP/MIP models run on HiGHS.
- **Deliverable.** Flow values only, or also duals/potentials, the min cut,
  and a sensitivity story? This decides LP route vs pure algorithm.
- **Validation path.** Agree up front that every reported flow passes the
  independent feasibility and objective check provided below.

## Problem Classes and Formulations

Let G = (N, A) be a directed graph with n = |N| nodes and m = |A| arcs. Arc
(i, j) has capacity u_ij > 0 and unit cost c_ij. Node i has balance b_i
(supply if b_i > 0, demand if b_i < 0, transshipment if b_i = 0), with
sum_i b_i = 0. Decision variable x_ij is the flow on arc (i, j).

### Minimum-cost flow — the master problem

$$
\min_{x} \; \sum_{(i,j) \in A} c_{ij}\, x_{ij}
$$

$$
\sum_{j:(i,j) \in A} x_{ij} \;-\; \sum_{j:(j,i) \in A} x_{ji} \;=\; b_i
\quad \forall i \in N \qquad \text{(flow conservation)}
$$

$$
0 \;\le\; x_{ij} \;\le\; u_{ij} \quad \forall (i,j) \in A .
$$

Every other single-commodity problem is a special case:

| Problem | Specialization of min-cost flow |
|---|---|
| Shortest s-t path | b_s = 1, b_t = -1, all other b_i = 0, u = infinity |
| Max s-t flow | b = 0, add arc (t, s) with cost -1, u_ts = infinity, all other costs 0 |
| Transportation | Bipartite N = sources + sinks, arcs only across |
| Assignment | Transportation with all supplies and demands equal to 1 |

### Total unimodularity and free integrality

The conservation constraint matrix is the node-arc incidence matrix of a
directed graph: each column has exactly one +1 and one -1. Such matrices are
**totally unimodular** (every square submatrix has determinant in {-1, 0, +1}).
By Hoffman & Kruskal (1956), a TU matrix with integral right-hand side and
integral bounds defines a polyhedron with only integral vertices. Practical
consequences:

- Solve the LP relaxation with simplex/barrier; any basic optimal solution is
  automatically an integer flow when b and u are integral. Never declare flow
  variables binary or integer for a pure flow problem — it only slows presolve.
- The LP duals are meaningful: the dual pi_i of node i's conservation
  constraint is its **node potential**; the reduced cost of arc (i, j) is
  c_ij - pi_i + pi_j. Optimality means no nonsaturated arc has negative
  reduced cost (Ahuja, Magnanti & Orlin 1993, *Network Flows*).
- Max-flow min-cut (Ford & Fulkerson 1956) is LP duality plus TU: the maximum
  s-t flow equals the minimum capacity over s-t cuts, and the optimal dual is
  the indicator of the min-cut node set.

### Multicommodity flow — where integrality dies

Commodities k = 1..K, each with source s_k, sink t_k, demand d_k, and its own
flow variables x^k_ij. Conservation holds per commodity; capacities couple them:

$$
\min \sum_{k} \sum_{(i,j) \in A} c_{ij}\, x^{k}_{ij}
\qquad \text{s.t.} \qquad
\sum_{j} x^{k}_{ij} - \sum_{j} x^{k}_{ji} = b^{k}_{i} \;\; \forall i, k,
\qquad
\sum_{k} x^{k}_{ij} \le u_{ij} \;\; \forall (i,j),
\qquad x \ge 0 .
$$

The joint-capacity rows break total unimodularity. The splittable version is
a (possibly fractional) LP. The **unsplittable** version — each commodity on a
single path — is NP-hard already for two commodities with integral flows
(Even, Itai & Shamir 1976). Expect a real integrality gap; the worked example
below exhibits one (LP 11 vs unsplittable 14).

### Algorithm selection

| Problem | Method | Complexity | Use it when |
|---|---|---|---|
| Shortest path, c >= 0 | Dijkstra, binary heap | O((n+m) log n) | Always, for nonnegative costs |
| Shortest path, some c < 0 | Bellman-Ford-Moore (label-correcting) | O(nm) | Negative arcs or cycle detection needed |
| All-pairs shortest paths | Johnson (one BF reweight + n Dijkstras) | O(nm + n^2 log n) | Sparse graphs; else Floyd-Warshall O(n^3) |
| Max flow | Preflow-push (Goldberg & Tarjan 1988); Dinic (1970) | O(n^2 sqrt(m)); O(n^2 m) | Pure max flow / min cut |
| Min-cost flow | Network simplex; successive shortest path; cost scaling (Goldberg & Tarjan 1990) | Fast in practice; O(m log U) Dijkstra calls; O(nm log(nC)) | Pure MCF; networkx and OR-Tools provide these |
| Multicommodity, splittable | LP (arc-based) or column generation (path-based) | Polynomial via LP | K and m moderate; CG when m·K explodes |
| Multicommodity, unsplittable | MIP, or metaheuristic over path choices | NP-hard | Exact for small K·m; heuristic beyond |

Decision rule: use the dedicated algorithm while the problem stays pure;
switch to the LP/MIP the moment a side constraint appears, and say explicitly
in the deliverable that integrality is no longer free.

## Exact Models in Gurobi

Build models with explicit constraint-builder functions: one function per
constraint family, named constraints, no anonymous loops in the main routine.
This makes each family unit-testable and the duals retrievable by name.

### Min-cost flow LP

```python
import gurobipy as gp
from gurobipy import GRB


def add_flow_conservation_constraints(
    model: gp.Model, x: gp.tupledict, data: dict
) -> None:
    """Add one flow-balance equality per node: outflow - inflow = balance."""
    arcs = data["arcs"]
    for i in data["nodes"]:
        out_expr = gp.quicksum(x[a] for a in arcs if a[0] == i)
        in_expr = gp.quicksum(x[a] for a in arcs if a[1] == i)
        model.addConstr(out_expr - in_expr == data["balance"][i],
                        name=f"balance[{i}]")


def add_capacity_constraints(model: gp.Model, x: gp.tupledict, data: dict) -> None:
    """Add x_a <= u_a as named constraints (instead of variable bounds) so the
    capacity dual prices are retrievable per arc."""
    for a in data["arcs"]:
        model.addConstr(x[a] <= data["capacity"][a], name=f"cap[{a[0]},{a[1]}]")


def solve_min_cost_flow(data: dict, integer: bool = False) -> dict | None:
    """Solve min-cost flow as LP (default) or IP; return flows and duals.

    integer=True is never needed for integral data (total unimodularity);
    it exists only to demonstrate that both give the same answer.
    """
    model = gp.Model("min_cost_flow")
    model.Params.OutputFlag = 0
    vtype = GRB.INTEGER if integer else GRB.CONTINUOUS
    x = model.addVars(data["arcs"], lb=0.0, vtype=vtype, name="x")
    add_flow_conservation_constraints(model, x, data)
    add_capacity_constraints(model, x, data)
    model.setObjective(
        gp.quicksum(data["cost"][a] * x[a] for a in data["arcs"]), GRB.MINIMIZE
    )
    model.optimize()
    if model.Status != GRB.OPTIMAL:
        return None
    result: dict = {
        "objective": model.ObjVal,
        "flow": {a: x[a].X for a in data["arcs"]},
    }
    if not integer:  # node potentials = duals of the conservation rows
        result["potential"] = {
            i: model.getConstrByName(f"balance[{i}]").Pi for i in data["nodes"]
        }
    return result


data = {
    "nodes": [0, 1, 2, 3],
    "arcs": [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)],
    "balance": {0: 4, 1: 0, 2: 0, 3: -4},
    "capacity": {(0, 1): 3, (0, 2): 2, (1, 2): 2, (1, 3): 2, (2, 3): 3},
    "cost": {(0, 1): 2, (0, 2): 4, (1, 2): 1, (1, 3): 6, (2, 3): 3},
}
result = solve_min_cost_flow(data)
print(result["objective"], result["flow"])
# Expected: objective 27.0 with integral flows even though the model is an LP:
# x[0,1]=3, x[0,2]=1, x[1,2]=2, x[1,3]=1, x[2,3]=3 (total unimodularity).
```

Read the node potentials from `result["potential"]` and verify reduced-cost
optimality by hand on small instances: every arc with flow strictly between
0 and u must satisfy c_ij - pi_i + pi_j = 0; every empty arc must have
nonnegative reduced cost. This is the single most useful debugging check for
flow LPs.

### Multicommodity flow: splittable LP and unsplittable MIP

The same builder pattern, with one conservation family per (commodity, node)
and one coupling family per arc. The `unsplittable` flag swaps continuous
per-commodity flows for binary arc-usage variables scaled by demand, which
forces each commodity onto a single path.

```python
import gurobipy as gp
from gurobipy import GRB


def add_commodity_conservation_constraints(
    model: gp.Model, x: dict, data: dict
) -> None:
    """Flow balance per (commodity, node): each commodity routes its demand."""
    for k, (s_k, t_k, d_k) in enumerate(data["commodities"]):
        for i in data["nodes"]:
            rhs = d_k if i == s_k else (-d_k if i == t_k else 0.0)
            out_expr = gp.quicksum(x[k, a] for a in data["arcs"] if a[0] == i)
            in_expr = gp.quicksum(x[k, a] for a in data["arcs"] if a[1] == i)
            model.addConstr(out_expr - in_expr == rhs, name=f"bal[{k},{i}]")


def add_joint_capacity_constraints(model: gp.Model, x: dict, data: dict) -> None:
    """Couple commodities: total flow on each arc at most its capacity.
    These are the rows that destroy total unimodularity."""
    n_k = len(data["commodities"])
    for a in data["arcs"]:
        model.addConstr(
            gp.quicksum(x[k, a] for k in range(n_k)) <= data["capacity"][a],
            name=f"cap[{a[0]},{a[1]}]",
        )


def solve_multicommodity(data: dict, unsplittable: bool = False,
                         time_limit: float = 60.0) -> dict | None:
    """Arc-based multicommodity flow: LP if splittable, binary MIP if not."""
    model = gp.Model("multicommodity")
    model.Params.OutputFlag = 0
    model.Params.TimeLimit = time_limit
    n_k = len(data["commodities"])
    keys = [(k, a) for k in range(n_k) for a in data["arcs"]]
    if unsplittable:
        y = model.addVars(keys, vtype=GRB.BINARY, name="y")
        # x[k,a] = d_k * y[k,a]: commodity k uses arc a fully or not at all.
        x = {(k, a): data["commodities"][k][2] * y[k, a] for (k, a) in keys}
    else:
        x = model.addVars(keys, lb=0.0, name="x")
    add_commodity_conservation_constraints(model, x, data)
    add_joint_capacity_constraints(model, x, data)
    model.setObjective(
        gp.quicksum(data["cost"][a] * x[k, a] for (k, a) in keys), GRB.MINIMIZE
    )
    model.optimize()
    ok = model.Status == GRB.OPTIMAL or (
        model.Status == GRB.TIME_LIMIT and model.SolCount > 0
    )
    if not ok:
        return None
    if unsplittable:
        flow = {ka: data["commodities"][ka[0]][2] * y[ka].X for ka in keys}
    else:
        flow = {ka: x[ka].X for ka in keys}
    return {"objective": model.ObjVal, "flow": flow, "gap": model.MIPGap
            if unsplittable else 0.0}


data = {
    "nodes": [0, 1, 2, 3],
    "arcs": [(0, 2), (1, 2), (2, 3), (0, 3), (1, 3)],
    "capacity": {(0, 2): 3, (1, 2): 3, (2, 3): 3, (0, 3): 3, (1, 3): 3},
    "cost": {(0, 2): 1, (1, 2): 1, (2, 3): 1, (0, 3): 5, (1, 3): 5},
    "commodities": [(0, 3, 2.0), (1, 3, 2.0)],  # (source, sink, demand)
}
lp = solve_multicommodity(data)
ip = solve_multicommodity(data, unsplittable=True)
print(lp["objective"], ip["objective"])
# Expected: splittable LP objective 11.0 (3 units share the cheap hub arc
# (2,3), 1 unit takes a direct arc); unsplittable objective 14.0 (one
# commodity hub, one direct). The gap exists because the joint-capacity
# matrix is not totally unimodular.
```

For large instances the arc-based LP has m·K variables and grows fast; switch
to the path-based formulation with column generation (see Advanced
Techniques) before fighting the LP size.

## Dedicated Algorithms: Shortest Paths and networkx

Use these when the problem is pure. They are 10-1000x faster than the LP
route and need no license.

### Dijkstra — label-setting, nonnegative costs only

Dijkstra (1959) permanently settles nodes in order of distance. Correctness
relies on c >= 0: once a node leaves the heap with its final label, no later
path can improve it. With a binary heap and lazy deletion it runs in
O((n + m) log n).

```python
import heapq


def dijkstra(
    adj: dict[int, list[tuple[int, float]]], source: int
) -> tuple[dict[int, float], dict[int, int]]:
    """Label-setting shortest paths from source; requires c >= 0 on all arcs.

    adj[i] = list of (j, cost_ij). Returns (distance, predecessor) maps.
    Lazy deletion: stale heap entries are skipped via the settled set.
    """
    dist: dict[int, float] = {source: 0.0}
    pred: dict[int, int] = {}
    heap: list[tuple[float, int]] = [(0.0, source)]
    settled: set[int] = set()
    while heap:
        d_i, i = heapq.heappop(heap)
        if i in settled:
            continue
        settled.add(i)
        for j, c_ij in adj.get(i, []):
            d_j = d_i + c_ij
            if d_j < dist.get(j, float("inf")):
                dist[j] = d_j
                pred[j] = i
                heapq.heappush(heap, (d_j, j))
    return dist, pred


adj = {0: [(1, 2.0), (2, 4.0)], 1: [(2, 1.0), (3, 6.0)], 2: [(3, 3.0)]}
dist, pred = dijkstra(adj, 0)
print(dist[3], pred)
# Expected: dist[3] == 6.0 along 0 -> 1 -> 2 -> 3; pred == {1: 0, 2: 1, 3: 2}.
```

### Bellman-Ford-Moore — label-correcting, handles negative costs

The queue-based form below is the classic label-correcting method (Bellman
1958; Ford 1956; Moore 1959): node labels stay tentative and may improve many
times. It tolerates negative arc costs and proves negative cycles. Variants
differ only in queue discipline — FIFO here; deque insertion (d'Esopo-Pape,
Pape 1974) and small-label-first are drop-in replacements that often run
faster on road-like networks but have bad worst cases.

```python
from collections import deque


def bellman_ford(
    arcs: list[tuple[int, int, float]], n_nodes: int, source: int
) -> tuple[list[float], list[int], bool]:
    """FIFO label-correcting shortest paths; allows negative arc costs.

    Returns (dist, pred, has_negative_cycle). A node dequeued more than
    n_nodes times proves a negative cycle reachable from the source.
    O(n*m) worst case; close to O(m) on sparse practical graphs.
    """
    inf = float("inf")
    dist = [inf] * n_nodes
    pred = [-1] * n_nodes
    dist[source] = 0.0
    out: dict[int, list[tuple[int, float]]] = {}
    for i, j, c in arcs:
        out.setdefault(i, []).append((j, c))
    in_queue = [False] * n_nodes
    dequeues = [0] * n_nodes
    queue: deque[int] = deque([source])
    in_queue[source] = True
    while queue:
        i = queue.popleft()
        in_queue[i] = False
        dequeues[i] += 1
        if dequeues[i] > n_nodes:
            return dist, pred, True
        for j, c in out.get(i, []):
            if dist[i] + c < dist[j] - 1e-12:
                dist[j] = dist[i] + c
                pred[j] = i
                if not in_queue[j]:
                    queue.append(j)
                    in_queue[j] = True
    return dist, pred, False


arcs = [(0, 1, 4.0), (0, 2, 2.0), (2, 1, -3.0), (1, 3, 2.0), (2, 3, 4.0)]
dist, pred, neg = bellman_ford(arcs, 4, 0)
print(dist[3], neg)
# Expected: dist[3] == 1.0 via 0 -> 2 -> 1 -> 3 (2 - 3 + 2); neg == False.
```

For repeated shortest-path calls on a graph with some negative costs, run
Bellman-Ford once, reweight every arc to c_ij - pi_i + pi_j >= 0 with the
resulting potentials, then use Dijkstra for all later queries (Johnson 1977).
This is exactly how successive-shortest-path min-cost flow stays fast.

### networkx for max flow, min cut, and min-cost flow

```python
import networkx as nx


def networkx_flows() -> None:
    """Reference solves: max-flow/min-cut and min-cost flow with networkx."""
    # Max flow / min cut (preflow-push is the default algorithm).
    g = nx.DiGraph()
    for (i, j), u in {(0, 1): 3, (0, 2): 2, (1, 2): 1,
                      (1, 3): 2, (2, 3): 3}.items():
        g.add_edge(i, j, capacity=u)
    value, flow = nx.maximum_flow(g, 0, 3)
    cut_value, (side_s, side_t) = nx.minimum_cut(g, 0, 3)
    print(value, cut_value, sorted(side_s))
    # Expected: value == 5, cut_value == 5, side_s == [0]
    # (the min cut is {(0,1),(0,2)} with capacity 3 + 2 = 5).

    # Min-cost flow via network simplex. Convention: node attribute
    # 'demand' is negative for supply. Data must be integral.
    h = nx.DiGraph()
    h.add_node(0, demand=-4)
    h.add_node(3, demand=4)
    arc_data = {(0, 1): (3, 2), (0, 2): (2, 4), (1, 2): (2, 1),
                (1, 3): (2, 6), (2, 3): (3, 3)}
    for (i, j), (u, c) in arc_data.items():
        h.add_edge(i, j, capacity=u, weight=c)
    flow_dict = nx.min_cost_flow(h)
    print(nx.cost_of_flow(h, flow_dict))
    # Expected: 27 — identical to the Gurobi LP on the same instance.


networkx_flows()
```

networkx is the right prototyping tool up to roughly 10^5 arcs. Beyond that,
use OR-Tools (`ortools.graph.python.min_cost_flow` and `max_flow`), which
wrap C++ cost-scaling and push-relabel implementations (Goldberg 1997, "An
efficient implementation of a scaling minimum-cost flow algorithm").

## Metaheuristic: GA for Unsplittable Multicommodity Flow

Pure single-commodity flow problems never need a metaheuristic — the
polynomial algorithms above are exact and fast. The NP-hard member of this
family is unsplittable multicommodity flow, and a genetic algorithm over
**path-index chromosomes** matches it well: precompute a small candidate-path
set per commodity (k-shortest paths via `networkx.shortest_simple_paths`, or
repeated Dijkstra with perturbed arc costs), then search over the index
vector that picks one path per commodity. Capacity violations are handled by
a static penalty. Operator and parameter details are covered in the
genetic-algorithms and constraint-handling-techniques skills; the encoding
here keeps everything vectorizable.

```python
import numpy as np


def path_arc_matrices(
    candidates: list[list[list[tuple[int, int]]]],
    arcs: list[tuple[int, int]],
    demands: np.ndarray,
    costs: dict[tuple[int, int], float],
) -> tuple[np.ndarray, np.ndarray]:
    """Build load tensor L[k,p,a] (= d_k if commodity k's path p uses arc a)
    and path-cost matrix C[k,p]; unused path slots get cost +inf."""
    n_k, n_p = len(candidates), max(len(c) for c in candidates)
    arc_idx = {a: t for t, a in enumerate(arcs)}
    load = np.zeros((n_k, n_p, len(arcs)))
    cost = np.full((n_k, n_p), np.inf)
    for k, paths in enumerate(candidates):
        for p, path in enumerate(paths):
            load[k, p, [arc_idx[a] for a in path]] = demands[k]
            cost[k, p] = demands[k] * sum(costs[a] for a in path)
    return load, cost


def ga_unsplittable_mcf(
    load: np.ndarray, path_cost: np.ndarray, capacity: np.ndarray,
    n_paths: np.ndarray, penalty: float = 1_000.0, pop: int = 60,
    gens: int = 200, seed: int = 0,
) -> tuple[np.ndarray, float]:
    """Vectorized GA over path-index chromosomes (one gene per commodity).
    See the genetic-algorithms skill for operator design rationale."""
    rng = np.random.default_rng(seed)
    n_k = load.shape[0]
    k_idx = np.arange(n_k)

    def fitness(pop_mat: np.ndarray) -> np.ndarray:
        arc_load = load[k_idx, pop_mat, :].sum(axis=1)        # (pop, arcs)
        excess = np.maximum(arc_load - capacity, 0.0).sum(axis=1)
        return path_cost[k_idx, pop_mat].sum(axis=1) + penalty * excess

    P = rng.integers(0, n_paths, size=(pop, n_k))
    fit = fitness(P)
    for _ in range(gens):
        a = rng.integers(0, pop, (2, pop))                    # tournaments
        b = rng.integers(0, pop, (2, pop))
        pa = np.where(fit[a[0]] < fit[a[1]], a[0], a[1])
        pb = np.where(fit[b[0]] < fit[b[1]], b[0], b[1])
        mask = rng.random((pop, n_k)) < 0.5                   # uniform xover
        children = np.where(mask, P[pa], P[pb])
        mut = rng.random((pop, n_k)) < 1.0 / n_k              # random reset
        children = np.where(mut, rng.integers(0, n_paths, (pop, n_k)), children)
        merged = np.vstack([P, children])                     # (mu + lambda)
        merged_fit = np.concatenate([fit, fitness(children)])
        keep = np.argpartition(merged_fit, pop - 1)[:pop]
        P, fit = merged[keep], merged_fit[keep]
    best = int(np.argmin(fit))
    return P[best], float(fit[best])


arcs = [(0, 2), (1, 2), (2, 3), (0, 3), (1, 3)]
costs = {(0, 2): 1.0, (1, 2): 1.0, (2, 3): 1.0, (0, 3): 5.0, (1, 3): 5.0}
capacity = np.array([3.0, 3.0, 3.0, 3.0, 3.0])
demands = np.array([2.0, 2.0])
candidates = [
    [[(0, 2), (2, 3)], [(0, 3)]],   # commodity 0: hub path or direct arc
    [[(1, 2), (2, 3)], [(1, 3)]],   # commodity 1: hub path or direct arc
]
load, path_cost = path_arc_matrices(candidates, arcs, demands, costs)
chrom, best_fit = ga_unsplittable_mcf(load, path_cost, capacity,
                                      np.array([2, 2]), seed=1)
print(chrom, best_fit)
# Expected: best_fit == 14.0 — one commodity through the hub, the other
# direct; equals the unsplittable Gurobi optimum on the same instance.
```

Two design notes. First, the candidate-path set bounds solution quality: if
the optimal path of some commodity is missing, the GA cannot find it, so
generate 5-20 diverse candidates per commodity and report which were used.
Second, always benchmark the GA against the splittable LP value — it is a
valid lower bound, and `(GA - LP) / LP` is an honest quality gap even when
the MIP is too large to solve.

## Instance Generation and Validation

### Seeded generators (feasible by construction)

Random balances with random capacities are usually infeasible. Generate
instances by routing a known flow first and sizing capacities to cover it:
feasibility is then guaranteed, and the routed flow gives a built-in upper
bound on the optimal cost.

```python
import numpy as np


def generate_mcf_instance(
    n_nodes: int, arc_density: float, n_supply: int, seed: int
) -> dict:
    """Random feasible min-cost flow instance.

    Builds a DAG skeleton (arcs i -> j only for i < j) including the chain
    0 -> 1 -> ... -> n-1 for connectivity, routes random supplies to the last
    node along node-increasing walks, then sets capacities to cover the
    routed flow plus slack. Feasible by construction.
    """
    rng = np.random.default_rng(seed)
    nodes = list(range(n_nodes))
    arc_set = {(i, i + 1) for i in range(n_nodes - 1)}
    for i in range(n_nodes):
        for j in range(i + 2, n_nodes):
            if rng.random() < arc_density:
                arc_set.add((i, j))
    arcs = sorted(arc_set)
    out: dict[int, list[int]] = {}
    for i, j in arcs:
        out.setdefault(i, []).append(j)
    used = {a: 0.0 for a in arcs}
    balance = {i: 0.0 for i in nodes}
    sink = n_nodes - 1
    for _ in range(n_supply):
        amount = float(rng.integers(1, 10))
        i = int(rng.integers(0, sink))
        balance[i] += amount
        while i != sink:                      # node-increasing walk to sink
            j = int(rng.choice(out[i]))
            used[(i, j)] += amount
            i = j
        balance[sink] -= amount
    capacity = {a: used[a] + float(rng.integers(0, 8)) for a in arcs}
    cost = {a: float(rng.integers(1, 20)) for a in arcs}
    return {"nodes": nodes, "arcs": arcs, "balance": balance,
            "capacity": capacity, "cost": cost}


def generate_multicommodity_instance(
    n_nodes: int, arc_density: float, n_commodities: int, seed: int
) -> dict:
    """Feasible multicommodity instance on the same DAG skeleton: each
    commodity gets a routed witness path; joint capacities cover the sum."""
    rng = np.random.default_rng(seed)
    base = generate_mcf_instance(n_nodes, arc_density, n_supply=1, seed=seed)
    arcs, out = base["arcs"], {}
    for i, j in arcs:
        out.setdefault(i, []).append(j)
    used = {a: 0.0 for a in arcs}
    commodities: list[tuple[int, int, float]] = []
    for _ in range(n_commodities):
        s = int(rng.integers(0, n_nodes - 1))
        d = float(rng.integers(1, 6))
        i = s
        while i != n_nodes - 1:
            j = int(rng.choice(out[i]))
            used[(i, j)] += d
            i = j
        commodities.append((s, n_nodes - 1, d))
    capacity = {a: used[a] + float(rng.integers(0, 5)) for a in arcs}
    return {"nodes": base["nodes"], "arcs": arcs, "capacity": capacity,
            "cost": base["cost"], "commodities": commodities}


inst = generate_mcf_instance(n_nodes=8, arc_density=0.3, n_supply=5, seed=42)
print(len(inst["arcs"]), sum(inst["balance"].values()))
# Expected: a connected DAG with the printed arc count for seed 42, and
# balances summing to exactly 0.0 (feasible by construction).
```

Report the generator parameters (n_nodes, density, seed) with every
experiment so instances are reproducible; vary seeds, never instances by hand.

### Independent validator

Never trust the model that produced the solution. The validator recomputes
feasibility and objective from raw instance data only.

```python
def validate_flow(
    data: dict, flow: dict, tol: float = 1e-6
) -> tuple[bool, float, list[str]]:
    """Independent check of a single-commodity flow: sign, capacity,
    conservation at every node, and recomputed objective."""
    errors: list[str] = []
    for a in data["arcs"]:
        f = flow.get(a, 0.0)
        if f < -tol:
            errors.append(f"negative flow {f:.6g} on arc {a}")
        if f > data["capacity"][a] + tol:
            errors.append(
                f"capacity exceeded on {a}: {f:.6g} > {data['capacity'][a]}")
    for i in data["nodes"]:
        net = (sum(flow.get(a, 0.0) for a in data["arcs"] if a[0] == i)
               - sum(flow.get(a, 0.0) for a in data["arcs"] if a[1] == i))
        if abs(net - data["balance"][i]) > tol:
            errors.append(
                f"conservation violated at node {i}: "
                f"net {net:.6g} != balance {data['balance'][i]}")
    objective = sum(data["cost"][a] * flow.get(a, 0.0) for a in data["arcs"])
    return len(errors) == 0, objective, errors


def validate_multicommodity(
    data: dict, flow: dict, tol: float = 1e-6
) -> tuple[bool, float, list[str]]:
    """Check per-commodity conservation plus joint capacities; recompute cost.
    flow is keyed by (k, arc)."""
    errors: list[str] = []
    n_k = len(data["commodities"])
    for k, (s_k, t_k, d_k) in enumerate(data["commodities"]):
        for i in data["nodes"]:
            rhs = d_k if i == s_k else (-d_k if i == t_k else 0.0)
            net = (sum(flow.get((k, a), 0.0)
                       for a in data["arcs"] if a[0] == i)
                   - sum(flow.get((k, a), 0.0)
                         for a in data["arcs"] if a[1] == i))
            if abs(net - rhs) > tol:
                errors.append(f"commodity {k} conservation broken at node {i}")
    for a in data["arcs"]:
        total = sum(flow.get((k, a), 0.0) for k in range(n_k))
        if total > data["capacity"][a] + tol:
            errors.append(f"joint capacity exceeded on arc {a}: {total:.6g}")
    objective = sum(data["cost"][a] * flow.get((k, a), 0.0)
                    for k in range(n_k) for a in data["arcs"])
    return len(errors) == 0, objective, errors


data = {
    "nodes": [0, 1, 2, 3],
    "arcs": [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)],
    "balance": {0: 4, 1: 0, 2: 0, 3: -4},
    "capacity": {(0, 1): 3, (0, 2): 2, (1, 2): 2, (1, 3): 2, (2, 3): 3},
    "cost": {(0, 1): 2, (0, 2): 4, (1, 2): 1, (1, 3): 6, (2, 3): 3},
}
flow = {(0, 1): 3.0, (0, 2): 1.0, (1, 2): 2.0, (1, 3): 1.0, (2, 3): 3.0}
print(validate_flow(data, flow))
# Expected: (True, 27.0, []) — confirms the Gurobi and networkx results.
```

Wire the validator into every solve path: exact, heuristic, and any solution
read back from a file. Cross-check exact vs heuristic on small instances —
on the multicommodity example above, the validator must report 14.0 for both
the MIP solution and the GA solution.

## Advanced Techniques

### Node potentials, reduced costs, and warm-started pricing

The dual pi_i of node i turns arc costs into reduced costs
c^pi_ij = c_ij - pi_i + pi_j. Successive-shortest-path min-cost flow keeps
all reduced costs nonnegative, so each augmentation step is a Dijkstra call
even when original costs are negative (Ahuja, Magnanti & Orlin 1993, ch. 9).
When flow problems sit inside a loop — column-generation pricing, Benders
subproblems, rolling-horizon resolves — keep the potentials from the previous
solve as the starting reweighting: the first Dijkstra after a small data
change then touches only the affected region of the graph.

### Scaling algorithms for large instances

Successive shortest path alone is pseudo-polynomial (one augmentation per
unit of flow in the worst case). Capacity scaling fixes this by augmenting
only along paths with residual capacity at least Delta, halving Delta over
O(log U) phases, giving O(m log U) Dijkstra calls. Cost scaling
(Goldberg & Tarjan 1990) refines an epsilon-optimality condition on reduced
costs and runs in O(n m log(nC)); it is the algorithm behind OR-Tools'
min-cost flow. Network simplex — simplex specialized to spanning-tree bases
with O(1) pivot pricing per arc — is exponential in theory but typically the
fastest exact method in practice, and Orlin (1997) gives a polynomial
variant. Practical order of attack: network simplex (networkx, Gurobi
`Method=0` on the LP) first, cost scaling (OR-Tools) when m exceeds ~10^5.

### Lagrangian relaxation of joint capacities

For multicommodity flow, dualize the joint-capacity rows with multipliers
w_ij >= 0. The Lagrangian subproblem separates into K independent shortest
paths under costs c_ij + w_ij — each solved by Dijkstra in milliseconds.
Update w by subgradient steps on the capacity violations. Because the
subproblems have the integrality property, the best Lagrangian bound equals
the LP relaxation value (Geoffrion 1974, "Lagrangean relaxation for integer
programming") — you gain speed and a primal heuristic (route commodities
greedily under the final w), not a tighter bound.

### Path-based formulation and column generation

Replace arc variables with path variables f_p >= 0 for p in P_k, the set of
s_k-t_k paths. The master LP has one convexity row per commodity and one
capacity row per arc; the pricing problem for commodity k is a shortest path
under reduced costs c_ij - w_ij (w = capacity duals), so new columns come
from Dijkstra. This scales far beyond the arc formulation when K is large
and is the standard route to exact unsplittable solutions via
branch-and-price (Barnhart, Hane & Vance 2000, "Using branch-and-price-and-
cut to solve origin-destination integer multicommodity flow problems").

### Graph transformations catalog

Reduce nonstandard features to the standard model instead of writing new
algorithms:

| Feature | Transformation |
|---|---|
| Node capacity / node cost at i | Split i into i_in, i_out joined by one arc carrying the capacity/cost |
| Arc lower bound l_ij > 0 | Send l_ij permanently: set u' = u - l, add l_ij to b_j, subtract from b_i |
| Undirected edge, c >= 0 | Two antiparallel arcs with the same capacity and cost |
| Multiple sources/sinks (max flow) | Super-source/super-sink with infinite-capacity arcs |
| Max flow as min-cost flow | Zero costs, add arc (t, s) with cost -1 and infinite capacity |
| Unbalanced supply/demand | Dummy node absorbing the surplus via zero-cost arcs |

## Practical Challenges

**Supplies and demands do not balance.** `nx.min_cost_flow` raises
`NetworkXUnfeasible` and the Gurobi LP reports infeasible when
sum b_i != 0. Decide what surplus means in the application — lost sales,
inventory, overtime — and add a dummy node that absorbs it through arcs whose
cost prices that interpretation. A zero-cost dummy silently hides modeling
errors; give it a visible cost.

**networkx min-cost flow with float data.** `nx.min_cost_flow` and
`nx.network_simplex` assume integer capacities, demands, and weights; float
input can produce wrong answers or non-termination. Scale to integers
(multiply by 10^k, round, record k) or use the Gurobi/HiGHS LP, which is
float-native.

**Dijkstra silently wrong with negative arcs.** Dijkstra never revisits a
settled node, so one negative arc can make it return a non-shortest path with
no error raised. Scan `min(c)` at the boundary of your code; dispatch to
Bellman-Ford or Johnson reweighting when it is negative. Add a regression
test with a known negative-arc instance.

**Infeasible instance with no explanation.** Conservation infeasibility is a
cut problem: build the super-source/super-sink max-flow instance; if the max
flow is less than total supply, the min cut returned by `nx.minimum_cut`
names exactly the bottleneck arc set separating supply from demand. Report
that cut, not just "infeasible". On the LP route, `model.computeIIS()` gives
the conflicting constraint set.

**Parallel arcs disappear.** `nx.DiGraph` keeps one edge per node pair, so
two cables between the same substations merge silently. Use `nx.MultiDiGraph`
(flow functions accept it) or key arcs as (i, j, idx) in your own models and
generators.

**Side constraints quietly destroy integrality.** Adding a budget row, fixed
charges, or arc-choice binaries to a flow LP breaks total unimodularity;
solutions may turn fractional and rounding them violates conservation.
The moment a non-network row enters, declare the integer variables integer,
treat the model as a true MIP, and re-estimate solve time — see
milp-modeling-gurobi.

**Python loops too slow on large graphs.** Dict-based Dijkstra at 10^6 arcs
costs seconds per call; inside a pricing loop that is fatal. Move to
`scipy.sparse.csgraph` (CSR adjacency, C speed) or OR-Tools. Keep the pure-
Python version as the reference implementation for tests.

**Degenerate duals confuse sensitivity stories.** Flow LPs are massively
degenerate; potentials are not unique, and two solvers can return different
pi vectors for the same optimum. Only reduced-cost signs and objective
ranges are reliable claims; never report a single dual vector as "the"
marginal prices without checking uniqueness on a perturbed instance.

## Tools & Libraries

| Library | When to use | Note |
|---|---|---|
| networkx | Prototyping, graphs up to ~10^5 arcs | `maximum_flow`, `minimum_cut`, `min_cost_flow`, `network_simplex`; integer data required for MCF |
| gurobipy | Flow + side constraints, multicommodity, duals needed | LP/MIP route; TU gives integral LP solutions for pure flow |
| OR-Tools graph | Production scale, 10^6+ arcs, no license | `min_cost_flow` (cost scaling), `max_flow` (push-relabel); C++ speed, integer data |
| scipy.sparse.csgraph | Many shortest-path calls on a fixed graph | `dijkstra`, `bellman_ford`, `johnson`, plus `maximum_flow` in scipy.sparse |
| HiGHS (via scipy.optimize.linprog or highspy) | LP route without a Gurobi license | Handles the arc-based formulations in this skill |
| igraph / graph-tool | Very large graphs, analysis-heavy workflows | C-backed; fewer flow-specific APIs than OR-Tools |

## Output Format

A complete network-flow deliverable contains:

1. **Problem classification.** One line: which flow problem, single or
   multicommodity, pure or with side constraints, and the chosen method with
   the reason ("pure MCF, integral data -> network simplex via networkx").
2. **Model summary table.**

   | Item | Value |
   |---|---|
   | Nodes / arcs / commodities | n, m, K |
   | Variables / constraints (LP or MIP route) | counts |
   | Integrality | free (TU) or enforced (MIP) |
   | Solver and algorithm | e.g. Gurobi LP dual simplex; OR-Tools cost scaling |

3. **Solution report.** Objective value; table of nonzero arc flows
   (arc, flow, capacity, cost, reduced cost); node potentials when the LP
   route was used; the min-cut arc set when max flow was solved; for MIPs,
   the bound and final gap; runtime and seed.
4. **Validation line.** Output of the independent validator on the reported
   flow: `feasible=True, objective=..., 0 violations`. A deliverable without
   this line is incomplete.
5. **Heuristic extras (when a metaheuristic was used).** Candidate-set size
   per commodity, generations, population, penalty value, best/mean over
   seeds, and the gap to the splittable-LP lower bound.
6. **Artifacts.** `solution.csv` (columns: commodity, tail, head, flow),
   `instance.json` (generator name + parameters + seed), and the run log.

## Questions to Ask

- Is this a pure flow problem, or are there side constraints (fixed charges,
  budgets, logical rules) that break the network structure?
- One commodity or several? If several: may a commodity split across paths?
- Are capacities, demands, and costs integral, or floats that need scaling?
- Any negative arc costs — and could there be a negative cycle?
- Directed arcs, undirected edges, or a mix?
- How large: nodes, arcs, commodities? One solve or thousands in a loop?
- Do supplies and demands balance, and what should happen to any surplus?
- Are duals, sensitivity ranges, or a min-cut certificate part of the
  deliverable, or only the flow itself?
- Is a Gurobi license available, or should everything run on open tools?
- What time budget separates "exact MIP" from "heuristic with LP bound"?

## Related Skills

- **linear-programming-fundamentals** — when you need the duality, reduced-
  cost, and sensitivity background behind node potentials and total
  unimodularity.
- **assignment-problems** — when the network is bipartite with unit supplies
  and demands; assignment is the min-cost flow special case with dedicated
  algorithms.
- **milp-modeling-gurobi** — when side constraints break the network
  structure and a general MIP must be built and solved properly.
- **dynamic-programming** — when shortest paths carry resource constraints;
  labeling algorithms are DP over the node-resource state space and feed
  pricing loops.
