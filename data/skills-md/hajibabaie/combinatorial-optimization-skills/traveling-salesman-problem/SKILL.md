---
name: traveling-salesman-problem
description: When the user wants to model or solve the traveling salesman problem - exact MIP formulations (MTZ vs DFJ with lazy subtour-elimination cuts), construction heuristics (nearest neighbor, greedy edge, Christofides), 2-opt/3-opt/Or-opt improvement, and Lin-Kernighan-style moves. Also use when the user mentions "TSP," "traveling salesman," "subtour elimination," "tour," "2-opt," "TSPLIB," "Hamiltonian cycle," or when one vehicle must visit every node exactly once and return. For multiple vehicles, capacities, or time windows, see vehicle-routing-problem; for delta-evaluation engineering, see local-search-and-neighborhoods.
---

# Traveling Salesman Problem

You are an expert in the traveling salesman problem. This skill covers exact MIP
formulations (MTZ vs DFJ with lazy subtour cuts in Gurobi), construction heuristics
(nearest neighbor, greedy edge, Christofides), 2-opt/3-opt/Or-opt local search, the
Lin-Kernighan idea, TSPLIB conventions, instance generation, and independent solution
validation. Use the framework below to pick the method that fits the instance size and
quality target, and to deliver tours verified by code independent of their producer.

## Initial Assessment

Establish these facts before formulating or writing any code:

- **Instance size.** n ≤ 20: Held-Karp DP is exact and trivial (see
  **dynamic-programming**). n ≤ ~100: MTZ is acceptable, DFJ is better. n ≤ ~5,000: DFJ
  with lazy cuts (or Concorde) solves most Euclidean instances to optimality. Beyond
  that: heuristics with Held-Karp bound for the gap report, or LKH.
- **Symmetric or asymmetric?** c_ij = c_ji or not? This changes the formulation (edge vs
  arc variables), the valid local-search moves (2-opt deltas are wrong under asymmetry
  because segment reversal changes arc directions), and the available codes.
- **Metric or not?** Christofides' 3/2 guarantee needs the triangle inequality. Distances
  from road networks usually satisfy it; penalized or forbidden arcs may not.
- **Distance convention.** TSPLIB EUC_2D rounds each distance to the nearest integer.
  Comparing a float-distance tour length against published optima is the single most
  common TSP reporting error. Fix the convention before benchmarking.
- **Data format.** Coordinates (compute distances on the fly or once) vs explicit matrix.
  A float64 matrix needs 8n² bytes: 800 MB at n = 10,000. Above a few thousand cities,
  plan k-nearest-neighbor candidate lists instead of full matrices.
- **Exact or heuristic?** What gap is acceptable, and must it be proven? A proven 0% gap
  requires the MIP/Concorde route; "within ~1-2% almost surely" is cheap with 2-opt +
  Or-opt inside a metaheuristic.
- **Time budget.** Seconds, minutes, hours? DFJ with lazy cuts may need minutes at
  n = 1,000; a 2-opt descent takes milliseconds.
- **Solver availability.** Gurobi license present? If not, plan OR-Tools or HiGHS-based
  fallbacks (the formulations below transfer directly).
- **Is it really a TSP?** Multiple vehicles, capacities, time windows, or depots make it
  a VRP (see **vehicle-routing-problem**). An open path (no return), fixed endpoints, or
  precedence constraints change the model; see the transformations under Advanced
  Techniques.
- **Reproducibility.** Seed every random construction and perturbation
  (`np.random.default_rng(seed)`) and record solver parameter settings with results.

## Problem Definition and Formulations

Given a complete graph $K_n = (V, E)$ with $V = \{0, \dots, n-1\}$ and costs $c_{ij}$,
find a Hamiltonian cycle (a tour visiting every node exactly once) of minimum total cost:

$$
\min_{\pi \in \Pi_n} \; \sum_{k=0}^{n-1} c_{\pi_k \pi_{k+1 \bmod n}}
$$

where $\Pi_n$ is the set of cyclic permutations of $V$. The decision version is
NP-complete (Karp 1972, "Reducibility among combinatorial problems"). Euclidean TSP stays
NP-hard but admits a PTAS (Arora 1998). None of this stops exact solving in practice:
branch-and-cut codes built on the DFJ relaxation routinely prove optimality for instances
with tens of thousands of cities — pla85900 was solved exactly (Applegate, Bixby, Chvátal
& Cook 2006, "The Traveling Salesman Problem: A Computational Study").

### DFJ formulation (Dantzig, Fulkerson & Johnson 1954)

Symmetric form with one binary edge variable $x_{ij}$ per unordered pair $i<j$:

$$
\min \sum_{i<j} c_{ij} x_{ij}
\quad \text{s.t.} \quad
\sum_{j \ne i} x_{\min(i,j),\max(i,j)} = 2 \;\; \forall i \in V,
$$

$$
\sum_{i,j \in S,\, i<j} x_{ij} \le |S| - 1
\qquad \forall S \subset V, \; 2 \le |S| \le n-1 .
$$

The subtour-elimination constraints (SECs) are exponentially many, so they are separated:
start without them, and whenever an integer solution decomposes into cycles, add the SEC
of each short cycle as a lazy constraint. The LP relaxation with all SECs is the subtour
relaxation; its value equals the Held-Karp bound and is typically within 1-2% of the
optimum on Euclidean instances. This bound strength is why DFJ branch-and-cut dominates.

### MTZ formulation (Miller, Tucker & Zemlin 1960)

Directed form with arc variables $x_{ij}$ and continuous order variables $u_i$
($1 \le u_i \le n-1$ for $i \ge 1$, node 0 anchored as tour start). The lifted version
(Desrochers & Laporte 1991) is:

$$
u_i - u_j + (n-1)\,x_{ij} + (n-3)\,x_{ji} \le n-2
\qquad \forall i \ne j,\; i,j \ge 1 .
$$

If arc $(i,j)$ is used, then $u_j \ge u_i + 1$, so no cycle can avoid node 0. Only
$O(n^2)$ constraints, no callbacks — but the LP relaxation is weak (often 20%+ below the
optimum), so branch-and-bound trees explode beyond roughly 50-100 cities.

| | DFJ (lazy SECs) | MTZ (lifted) |
|---|---|---|
| Variables | n(n−1)/2 binary | n(n−1) binary + (n−1) continuous |
| Constraints | n degree + SECs on demand | 2n degree + O(n²) order |
| LP bound | Held-Karp strength, ~1-2% gap (Euclidean) | weak, often 20%+ gap |
| Practical reach | thousands of cities | ~50-100 cities |
| Use when | pure TSP must be solved exactly | tour structure embedded in a larger MIP where callbacks are awkward |

### Heuristic landscape

Average excess over the Held-Karp bound on random Euclidean instances (Johnson & McGeoch
1997, "The traveling salesman problem: a case study in local optimization"):

| Method | Excess over HK bound | Time (typical) |
|---|---|---|
| Nearest neighbor | ~25% | O(n²) |
| Greedy edge | ~15% | O(n² log n) |
| Christofides | ~10% (3/2 worst case) | O(n³) matching |
| 2-opt (from good start) | ~5% | seconds at n=10⁴ with candidate lists |
| 3-opt | ~3% | minutes at n=10⁴ |
| Lin-Kernighan | ~2% | engineered: seconds at n=10⁴ |
| Iterated LK / LKH | <1%, often optimal | longer runs |

Decision rule: construction + 2-opt + Or-opt inside an ILS wrapper is the strong simple
baseline; reach for LKH (Helsgaun 2000) when you need <1% at scale; reach for DFJ
branch-and-cut or Concorde when the gap must be proven zero.

## Exact Models in Gurobi

Build both models from explicit constraint-builder functions so each constraint family is
testable in isolation and reusable when the TSP sits inside a larger model.

### MTZ model

```python
import numpy as np
import gurobipy as gp
from gurobipy import GRB


def add_degree_constraints(model: gp.Model, x: gp.tupledict, n: int) -> None:
    """Each city has exactly one outgoing and one incoming arc (directed form)."""
    model.addConstrs(
        (gp.quicksum(x[i, j] for j in range(n) if j != i) == 1 for i in range(n)),
        name="out_degree",
    )
    model.addConstrs(
        (gp.quicksum(x[j, i] for j in range(n) if j != i) == 1 for i in range(n)),
        name="in_degree",
    )


def add_mtz_order_constraints(
    model: gp.Model, x: gp.tupledict, u: gp.tupledict, n: int
) -> None:
    """Lifted MTZ subtour elimination (Desrochers & Laporte 1991)."""
    model.addConstrs(
        (
            u[i] - u[j] + (n - 1) * x[i, j] + (n - 3) * x[j, i] <= n - 2
            for i in range(1, n)
            for j in range(1, n)
            if i != j
        ),
        name="mtz",
    )


def solve_tsp_mtz(dist: np.ndarray, time_limit: float = 60.0) -> tuple[list[int], float]:
    """Solve the (A)TSP with the lifted MTZ formulation. Returns (tour, length)."""
    n = dist.shape[0]
    model = gp.Model("tsp_mtz")
    model.Params.OutputFlag = 0
    model.Params.TimeLimit = time_limit
    arcs = [(i, j) for i in range(n) for j in range(n) if i != j]
    x = model.addVars(arcs, vtype=GRB.BINARY, name="x")
    u = model.addVars(range(1, n), lb=1.0, ub=n - 1, name="u")
    model.setObjective(
        gp.quicksum(dist[i, j] * x[i, j] for i, j in arcs), GRB.MINIMIZE
    )
    add_degree_constraints(model, x, n)
    add_mtz_order_constraints(model, x, u, n)
    model.optimize()
    if model.Status not in (GRB.OPTIMAL, GRB.TIME_LIMIT) or model.SolCount == 0:
        raise RuntimeError(f"no solution found, status {model.Status}")
    succ = {i: j for i, j in arcs if x[i, j].X > 0.5}
    tour, node = [0], succ[0]
    while node != 0:
        tour.append(node)
        node = succ[node]
    return tour, model.ObjVal


# Tiny instance: 5 cities on a line at x = 0, 1, 2, 3, 4.
xs = np.array([0.0, 1.0, 2.0, 3.0, 4.0])
dist = np.abs(np.subtract.outer(xs, xs))
tour, length = solve_tsp_mtz(dist)
print(tour, round(length, 1))
# Expected: length 8.0 = 2 * (max - min); any tour going out to x=4 and back is optimal.
```

MTZ is the right choice when the tour is one piece of a larger MIP (e.g., sequence-
dependent setups in scheduling) and callbacks are not worth it; for pure TSP, prefer DFJ.

### DFJ model with lazy subtour-elimination callbacks

Degree constraints are added up front; SECs are separated inside a `MIPSOL` callback.
Each integer-feasible candidate either is one Hamiltonian cycle (accepted) or decomposes
into k ≥ 2 cycles, each of which yields one violated SEC. For separation of *fractional*
subtours via min-cut (user cuts, much stronger pruning at the root), see
**cutting-planes-valid-inequalities**.

```python
import itertools
import numpy as np
import gurobipy as gp
from gurobipy import GRB


def add_two_degree_constraints(model: gp.Model, x: gp.tupledict, n: int) -> None:
    """Each city is incident to exactly two selected edges (symmetric form)."""
    model.addConstrs(
        (
            gp.quicksum(x[min(i, j), max(i, j)] for j in range(n) if j != i) == 2
            for i in range(n)
        ),
        name="degree",
    )


def find_cycles(edges: list[tuple[int, int]], n: int) -> list[list[int]]:
    """Decompose a degree-2 edge set into its cycles (lists of node ids)."""
    nbr: dict[int, list[int]] = {i: [] for i in range(n)}
    for i, j in edges:
        nbr[i].append(j)
        nbr[j].append(i)
    seen = [False] * n
    cycles: list[list[int]] = []
    for start in range(n):
        if seen[start]:
            continue
        cycle: list[int] = []
        prev, node = -1, start
        while not seen[node]:
            seen[node] = True
            cycle.append(node)
            nxt = nbr[node][0] if nbr[node][0] != prev else nbr[node][1]
            prev, node = node, nxt
        cycles.append(cycle)
    return cycles


def solve_tsp_dfj(dist: np.ndarray, time_limit: float = 300.0) -> tuple[list[int], float]:
    """Solve the symmetric TSP with DFJ subtour cuts added lazily."""
    n = dist.shape[0]
    model = gp.Model("tsp_dfj")
    model.Params.OutputFlag = 0
    model.Params.TimeLimit = time_limit
    model.Params.LazyConstraints = 1  # mandatory for cbLazy
    keys = [(i, j) for i in range(n) for j in range(i + 1, n)]
    x = model.addVars(keys, vtype=GRB.BINARY, name="x")
    model.setObjective(gp.quicksum(dist[i, j] * x[i, j] for i, j in keys), GRB.MINIMIZE)
    add_two_degree_constraints(model, x, n)

    def subtour_callback(m: gp.Model, where: int) -> None:
        """Add one SEC per short cycle in each integer candidate solution."""
        if where != GRB.Callback.MIPSOL:
            return
        vals = m.cbGetSolution(x)
        chosen = [(i, j) for (i, j) in keys if vals[i, j] > 0.5]
        for cycle in find_cycles(chosen, n):
            if len(cycle) < n:
                m.cbLazy(
                    gp.quicksum(
                        x[i, j] for i, j in itertools.combinations(sorted(cycle), 2)
                    )
                    <= len(cycle) - 1
                )

    model.optimize(subtour_callback)
    if model.Status not in (GRB.OPTIMAL, GRB.TIME_LIMIT) or model.SolCount == 0:
        raise RuntimeError(f"no solution found, status {model.Status}")
    chosen = [(i, j) for (i, j) in keys if x[i, j].X > 0.5]
    tour = find_cycles(chosen, n)[0]
    return tour, model.ObjVal


# Tiny instance: two clusters of 3 points; without SECs the optimum is two triangles,
# so the lazy callback must fire at least once.
pts = np.array([[0, 0], [1, 0], [0.5, 1], [10, 0], [11, 0], [10.5, 1]], dtype=float)
dist = np.linalg.norm(pts[:, None, :] - pts[None, :, :], axis=2)
tour, length = solve_tsp_dfj(dist)
print(sorted(tour), round(length, 2))
# Expected: one tour over all 6 nodes, optimal length 23.24
# (e.g. 0-1-3-4-5-2: 1 + 9 + 1 + 1.118 + 10 + 1.118).
```

Practical notes for the DFJ path: one SEC per short cycle is enough (its complement is
implied by the degree constraints), and adding every cycle found per candidate beats
one-at-a-time separation. Warm-start with a heuristic tour (`x[i, j].Start = 1` for tour
edges) so the first incumbent is good. At n in the thousands, restrict variables to a
k-nearest-neighbor candidate graph plus one spanning tour to keep the model small, and
re-solve with an enlarged graph if the optimal tour uses a near-boundary edge.

## Construction Heuristics

Constructions provide MIP warm starts and metaheuristic starting points. Quality numbers
are in the landscape table above; nearest neighbor and greedy edge run in well under a
second at n = 1,000, while Christofides pays an O(n³) matching.

### Nearest neighbor and greedy edge

```python
import numpy as np


def tour_length(dist: np.ndarray, tour: np.ndarray) -> float:
    """Closed-tour length under distance matrix `dist`."""
    return float(dist[tour, np.roll(tour, -1)].sum())


def nearest_neighbor_tour(dist: np.ndarray, start: int = 0) -> np.ndarray:
    """Nearest-neighbor construction; O(n^2) via one vectorized argmin per step."""
    n = dist.shape[0]
    visited = np.zeros(n, dtype=bool)
    tour = np.empty(n, dtype=np.int64)
    tour[0] = start
    visited[start] = True
    for k in range(1, n):
        row = np.where(visited, np.inf, dist[tour[k - 1]])
        tour[k] = np.argmin(row)
        visited[tour[k]] = True
    return tour


# Tiny instance: 8 points on the unit circle (regular octagon).
angles = 2.0 * np.pi * np.arange(8) / 8
pts = np.column_stack([np.cos(angles), np.sin(angles)])
d = np.linalg.norm(pts[:, None, :] - pts[None, :, :], axis=2)
t = nearest_neighbor_tour(d)
print(t, round(tour_length(d, t), 4))
# Expected: angular order [0 1 2 3 4 5 6 7], length 6.1229 (= 8 * 2 sin(pi/8)).
# NN is optimal here by luck; on random instances it averages ~25% above the HK bound
# and its last edge back to the start is notoriously long.
```

Greedy edge sorts all edges by cost and accepts an edge iff both endpoints have degree
< 2 and it does not close a cycle before all n edges are placed (union-find check):

```python
import numpy as np


def greedy_edge_tour(dist: np.ndarray) -> np.ndarray:
    """Greedy-edge construction: cheapest edges first, degree <= 2, no early cycle."""
    n = dist.shape[0]
    iu, ju = np.triu_indices(n, k=1)
    order = np.argsort(dist[iu, ju], kind="stable")
    degree = np.zeros(n, dtype=np.int64)
    parent = np.arange(n)

    def find(a: int) -> int:
        """Union-find root with path halving."""
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    adj: list[list[int]] = [[] for _ in range(n)]
    added = 0
    for k in order:
        i, j = int(iu[k]), int(ju[k])
        if degree[i] == 2 or degree[j] == 2:
            continue
        ri, rj = find(i), find(j)
        if ri == rj and added < n - 1:
            continue  # would close a subtour early
        parent[ri] = rj
        degree[i] += 1
        degree[j] += 1
        adj[i].append(j)
        adj[j].append(i)
        added += 1
        if added == n:
            break
    tour = [0]
    prev, node = -1, 0
    for _ in range(n - 1):
        nxt = adj[node][0] if adj[node][0] != prev else adj[node][1]
        prev, node = node, nxt
        tour.append(node)
    return np.array(tour, dtype=np.int64)


# Tiny instance: same regular octagon.
angles = 2.0 * np.pi * np.arange(8) / 8
pts = np.column_stack([np.cos(angles), np.sin(angles)])
d = np.linalg.norm(pts[:, None, :] - pts[None, :, :], axis=2)
t = greedy_edge_tour(d)
print(round(float(d[t, np.roll(t, -1)].sum()), 4))
# Expected: 6.1229 - the 8 hull edges are the 8 cheapest, so greedy selects exactly them.
```

### Christofides (sketch)

Christofides (1976) gives the classic 3/2-approximation for metric symmetric TSP:

```text
1. T  <- minimum spanning tree of (V, c)
2. O  <- nodes with odd degree in T            (|O| is even by handshake lemma)
3. M  <- minimum-weight perfect matching on O  (the expensive O(n^3) step)
4. G  <- multigraph T + M                      (every node now has even degree)
5. E  <- Eulerian circuit of G
6. tour <- shortcut E (skip repeated nodes; triangle inequality => no cost increase)
```

Cost analysis: c(T) ≤ OPT (delete one tour edge to get a spanning tree), and
c(M) ≤ OPT/2 (the optimal tour restricted to O splits into two perfect matchings), so
the shortcut tour costs ≤ 3/2 · OPT. networkx supplies every step —
`nx.minimum_spanning_tree`, `nx.min_weight_matching` on the odd-degree subgraph,
`nx.eulerian_circuit` on the merged multigraph, then a skip-repeats shortcut pass — and
`nx.approximation.christofides` packages the whole pipeline. In practice it lands ~10%
above the HK bound, worse than 2-opt from a greedy start, so its value is the worst-case
guarantee: use it when a proven factor matters, and only on metric instances.

## Local Search and Iterated Local Search

The TSP improvement stack is 2-opt (remove two edges, reconnect reversed), Or-opt
(relocate a segment of 1-3 cities without reversal), and 3-opt (remove three edges; 7
reconnections, of which pure-reversal cases collapse to 2-opt). Deltas are O(1) for
symmetric instances. Full move theory, scan orders, and candidate-list engineering live
in **local-search-and-neighborhoods**; here are TSP-ready implementations.

For positions $i < j$ in tour $\pi$, the 2-opt move reversing $\pi_{i+1} \dots \pi_j$
changes the length by

$$
\Delta_{ij} = d_{\pi_i \pi_j} + d_{\pi_{i+1} \pi_{j+1}}
            - d_{\pi_i \pi_{i+1}} - d_{\pi_j \pi_{j+1}} .
$$

All n(n−1)/2 deltas can be scored at once with broadcasting — the right tool up to a few
thousand cities, after which O(n²) memory per sweep forces candidate lists (Advanced
Techniques). The vectorized best-improvement descent is the `two_opt` function inside
the ILS implementation below; it requires a symmetric matrix, because the delta formula
assumes reversal-invariant edge costs. A useful test invariant: 2-opt local optima have
no crossing edges, so points in convex position must yield the hull tour.

Or-opt relocates short segments *without* reversing them, so it is also valid for
asymmetric instances and reaches solutions 2-opt cannot (the two neighborhoods'
local-optima sets differ — the basis for chaining them):

```python
import numpy as np


def or_opt_descent(dist: np.ndarray, tour: np.ndarray) -> np.ndarray:
    """First-improvement Or-opt: relocate segments of length 1-3, orientation kept."""
    t = [int(v) for v in tour]
    n = len(t)
    improved = True
    while improved:
        improved = False
        for seg_len in (1, 2, 3):
            for i in range(n):
                if i + seg_len >= n:
                    continue  # skip wrap-around segments for clarity
                a, b = t[i - 1], t[i]  # predecessor, segment head
                c, e = t[i + seg_len - 1], t[i + seg_len]  # segment tail, successor
                gain_remove = dist[a, b] + dist[c, e] - dist[a, e]
                for j in range(n):
                    if (j - i + 1) % n <= seg_len:
                        continue  # insertion inside / adjacent to the segment (cyclic)
                    p, q = t[j], t[(j + 1) % n]
                    delta = dist[p, b] + dist[c, q] - dist[p, q] - gain_remove
                    if delta < -1e-10:
                        seg = t[i : i + seg_len]
                        rest = t[:i] + t[i + seg_len :]
                        pos = rest.index(p) + 1
                        t = rest[:pos] + seg + rest[pos:]
                        improved = True
                        break
                if improved:
                    break
            if improved:
                break
    return np.array(t, dtype=np.int64)


# Tiny instance: octagon tour with city 3 displaced -> Or-opt relocates it home.
angles = 2.0 * np.pi * np.arange(8) / 8
pts = np.column_stack([np.cos(angles), np.sin(angles)])
d = np.linalg.norm(pts[:, None, :] - pts[None, :, :], axis=2)
t = or_opt_descent(d, np.array([0, 1, 2, 4, 5, 6, 3, 7]))
print(round(float(d[t, np.roll(t, -1)].sum()), 4))
# Expected: 6.1229 - the optimal octagon tour is restored.
```

### The metaheuristic of choice: ILS with double-bridge kicks

Iterated local search is the standard strong-and-simple TSP metaheuristic: descend to a
2-opt optimum, apply a double-bridge 4-opt kick (the canonical perturbation, because no
sequence of 2-opt moves undoes it cheaply), re-descend, keep the better tour. Design
options (acceptance rules, adaptive kick strength, restarts) are covered in
**iterated-local-search**; population-based constructive alternatives in
**ant-colony-optimization**.

```python
import numpy as np


def tour_length(dist: np.ndarray, tour: np.ndarray) -> float:
    """Closed-tour length."""
    return float(dist[tour, np.roll(tour, -1)].sum())


def two_opt(dist: np.ndarray, tour: np.ndarray) -> np.ndarray:
    """Vectorized best-improvement 2-opt descent (symmetric distances)."""
    tour = tour.copy()
    n = tour.size
    while True:
        nxt = np.roll(tour, -1)
        removed = dist[tour, nxt]
        delta = (
            dist[np.ix_(tour, tour)] + dist[np.ix_(nxt, nxt)]
            - removed[:, None] - removed[None, :]
        )
        delta = np.triu(delta, k=2)
        i, j = np.unravel_index(np.argmin(delta), delta.shape)
        if delta[i, j] > -1e-10:
            return tour
        tour[i + 1 : j + 1] = tour[i + 1 : j + 1][::-1]


def double_bridge(tour: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """4-opt double-bridge kick: cut the tour at 3 points, reorder the middle parts."""
    n = tour.size
    a, b, c = np.sort(rng.choice(np.arange(1, n), size=3, replace=False))
    return np.concatenate([tour[:a], tour[b:c], tour[a:b], tour[c:]])


def ils_tsp(dist: np.ndarray, n_kicks: int = 200, seed: int = 0) -> tuple[np.ndarray, float]:
    """Iterated local search: NN start, 2-opt descent, double-bridge perturbation."""
    rng = np.random.default_rng(seed)
    n = dist.shape[0]
    visited = np.zeros(n, dtype=bool)
    tour = np.empty(n, dtype=np.int64)
    tour[0] = 0
    visited[0] = True
    for k in range(1, n):  # nearest-neighbor start
        row = np.where(visited, np.inf, dist[tour[k - 1]])
        tour[k] = np.argmin(row)
        visited[tour[k]] = True
    cur = two_opt(dist, tour)
    cur_len = tour_length(dist, cur)
    best, best_len = cur, cur_len
    for _ in range(n_kicks):
        cand = two_opt(dist, double_bridge(cur, rng))
        cand_len = tour_length(dist, cand)
        if cand_len < cur_len:  # better-acceptance; see iterated-local-search
            cur, cur_len = cand, cand_len
        if cand_len < best_len:
            best, best_len = cand, cand_len
    return best, best_len


# Tiny instance: 12 random points in the unit square.
rng = np.random.default_rng(42)
pts = rng.random((12, 2))
d = np.linalg.norm(pts[:, None, :] - pts[None, :, :], axis=2)
tour, length = ils_tsp(d, n_kicks=100, seed=1)
print(round(length, 4))
# Expected: 2.9806 - the optimum of this 12-city instance (verified by Held-Karp DP);
# ILS with 100 kicks is essentially exact at this size.
```

Parameter guidance: `n_kicks` is the budget knob — quality saturates roughly
logarithmically in it. Add Or-opt after each descent for another ~1% at small cost; on
rugged clustered instances, restart from the best tour after ~50 non-improving kicks.

## Instances, TSPLIB, and Validation

### Instance generators (seeded)

Uniform-random and clustered Euclidean generators in the DIMACS TSP Challenge
portgen/portcgen styles. Clustered instances are systematically harder for local search
(kicks must cross low-density gaps), so report both families; benchmark protocol and
feature reporting live in **instance-generation-and-benchmarks**.

```python
import numpy as np


def euclidean_instance(
    n: int,
    seed: int,
    kind: str = "uniform",
    n_clusters: int = 5,
    tsplib_round: bool = False,
) -> tuple[np.ndarray, np.ndarray]:
    """Random Euclidean TSP instance. Returns (coords, dist).

    kind='uniform': points uniform in [0, 1000]^2 (portgen style).
    kind='clustered': Gaussian blobs around n_clusters random centers (portcgen style).
    tsplib_round=True applies TSPLIB EUC_2D rounding: d = floor(euclid + 0.5).
    """
    rng = np.random.default_rng(seed)
    if kind == "uniform":
        coords = rng.uniform(0.0, 1000.0, size=(n, 2))
    elif kind == "clustered":
        centers = rng.uniform(0.0, 1000.0, size=(n_clusters, 2))
        labels = rng.integers(0, n_clusters, size=n)
        coords = centers[labels] + rng.normal(0.0, 25.0, size=(n, 2))
    else:
        raise ValueError(f"unknown kind {kind!r}")
    diff = coords[:, None, :] - coords[None, :, :]
    dist = np.sqrt((diff**2).sum(axis=2))
    if tsplib_round:
        dist = np.floor(dist + 0.5)
    np.fill_diagonal(dist, 0.0)
    return coords, dist


coords, dist = euclidean_instance(100, seed=0)
print(coords.shape, dist.shape, round(float(dist.mean()), 2))
# Expected: (100, 2) (100, 100) 542.06 - identical on every run with seed=0.
```

### TSPLIB reader

TSPLIB (Reinelt 1991, "TSPLIB - A traveling salesman problem library") is the standard
benchmark set. The critical detail is the per-type rounding rule: published optima
(berlin52 = 7542, pr2392 = 378032) are integers under it; float evaluation will not match.

```python
import numpy as np


def read_tsplib(path: str) -> tuple[str, np.ndarray]:
    """Parse a TSPLIB file with NODE_COORD_SECTION (EUC_2D, CEIL_2D, or ATT).

    Returns (name, dist) using the official TSPLIB rounding, so tour lengths are
    directly comparable with published optima.
    """
    name, ewt = "", ""
    coords: list[tuple[float, float]] = []
    in_coords = False
    with open(path, encoding="utf-8") as fh:
        for raw in fh:
            token = raw.strip()
            if token.startswith("NAME"):
                name = token.split(":", 1)[1].strip()
            elif token.startswith("EDGE_WEIGHT_TYPE"):
                ewt = token.split(":", 1)[1].strip()
            elif token == "NODE_COORD_SECTION":
                in_coords = True
            elif token == "EOF" or token.endswith("_SECTION"):
                in_coords = False  # any later section ends the coordinate block
            elif token and in_coords:
                parts = token.split()
                coords.append((float(parts[1]), float(parts[2])))
    xy = np.asarray(coords)
    diff = xy[:, None, :] - xy[None, :, :]
    if ewt == "EUC_2D":
        dist = np.floor(np.sqrt((diff**2).sum(axis=2)) + 0.5)
    elif ewt == "CEIL_2D":
        dist = np.ceil(np.sqrt((diff**2).sum(axis=2)))
    elif ewt == "ATT":  # pseudo-Euclidean, used by att48/att532
        r = np.sqrt((diff**2).sum(axis=2) / 10.0)
        t = np.floor(r + 0.5)
        dist = np.where(t < r, t + 1.0, t)
    else:
        raise ValueError(f"unsupported EDGE_WEIGHT_TYPE {ewt!r}")
    np.fill_diagonal(dist, 0.0)
    return name, dist


# Tiny instance: write a 5-city TSPLIB file, parse it back.
import pathlib

text = (
    "NAME : tiny5\nTYPE : TSP\nDIMENSION : 5\nEDGE_WEIGHT_TYPE : EUC_2D\n"
    "NODE_COORD_SECTION\n1 0 0\n2 3 0\n3 3 4\n4 0 4\n5 1 1\nEOF\n"
)
p = pathlib.Path("tiny5.tsp")
p.write_text(text, encoding="utf-8")
name, dist = read_tsplib(str(p))
p.unlink()
print(name, dist[0, 1], dist[1, 2], dist[0, 2])
# Expected: tiny5 3.0 4.0 5.0 (the 3-4-5 triangle, integer-rounded).
```

### Independent validator

Never trust the producing code's own objective. The validator must share no code with the
solver or heuristic: it re-derives feasibility (permutation property) and length from the
distance matrix alone.

```python
import numpy as np


def validate_tour(
    dist: np.ndarray,
    tour: np.ndarray,
    claimed_length: float | None = None,
    tol: float = 1e-6,
) -> float:
    """Independent feasibility + objective check. Raises ValueError on violation.

    Checks: tour is a permutation of 0..n-1, every leg is finite (no forbidden arc),
    and the recomputed length matches `claimed_length` within relative tolerance.
    Returns the recomputed length.
    """
    n = dist.shape[0]
    t = np.asarray(tour, dtype=np.int64)
    if t.shape != (n,):
        raise ValueError(f"tour has shape {t.shape}, expected ({n},)")
    if not np.array_equal(np.sort(t), np.arange(n)):
        raise ValueError("tour is not a permutation of 0..n-1")
    legs = dist[t, np.roll(t, -1)]
    if not np.all(np.isfinite(legs)):
        raise ValueError("tour uses a forbidden (non-finite) arc")
    length = float(legs.sum())
    if claimed_length is not None:
        if abs(length - claimed_length) > tol * max(1.0, abs(length)):
            raise ValueError(f"recomputed {length} != claimed {claimed_length}")
    return length


# Tiny instance: validate a correct tour, then catch a corrupted one.
xs = np.array([0.0, 1.0, 2.0, 3.0])
dist = np.abs(np.subtract.outer(xs, xs))
print(validate_tour(dist, np.array([0, 1, 2, 3]), claimed_length=6.0))
try:
    validate_tour(dist, np.array([0, 1, 1, 3]))
except ValueError as exc:
    print(exc)
# Expected: 6.0, then "tour is not a permutation of 0..n-1".
```

Run the validator on every reported result and inside tests against known TSPLIB optima.

## Advanced Techniques

### Lin-Kernighan: sequential edge exchange

Lin & Kernighan (1973) generalize 2-opt/3-opt to variable-depth moves: starting from a
node, alternately remove a tour edge and add a cheaper non-tour edge, maintaining the
running gain $G_k = \sum_{m \le k} (c(\text{removed}_m) - c(\text{added}_m))$ and closing
the chain back to the start whenever the closed tour improves. The two design rules that
make it work: only extend while $G_k > 0$ (positive-gain criterion), and forbid re-adding
removed edges within one chain. LKH (Helsgaun 2000, "An effective implementation of the
Lin-Kernighan traveling salesman heuristic") adds α-nearness candidate lists derived
from 1-trees and 5-opt basic moves, and finds optima of most TSPLIB instances. Implement
LK yourself only as a learning exercise — use LKH (or `elkai`) in production.

### Candidate lists and don't-look bits

Improving moves almost always connect geometrically close cities. Restrict the search to
each city's k nearest neighbors (k = 8-16): build the lists once with a KD-tree
(`scipy.spatial.cKDTree`) in O(n log n), and scan moves only over `(city, neighbor)`
pairs. Add don't-look bits: when a scan from city v finds no improving move, mark v;
unmark only the endpoints of applied moves. Together these turn a quadratic 2-opt sweep
into near-linear work per pass and are what makes n = 10⁵ tractable (Bentley 1992, "Fast
algorithms for geometric traveling salesman problems").

### Held-Karp bound via 1-trees

A 1-tree is a spanning tree on $V \setminus \{0\}$ plus the two cheapest edges at node 0;
every tour is a 1-tree, so the cheapest 1-tree is a lower bound. Held & Karp (1970, 1971)
tighten it with node penalties $\pi$: under costs $c_{ij} + \pi_i + \pi_j$, the bound
$w(\pi) = \text{1tree}(\pi) - 2\sum_i \pi_i$ is maximized by subgradient ascent with
$\pi \leftarrow \pi + t \,(\deg_T - 2)$. The result equals the DFJ LP bound and reaches
~99% of the optimum on Euclidean instances — the standard denominator for heuristic gap
reporting when the optimum is unknown.

### ATSP and path-TSP transformations

Asymmetric instances: either solve the directed MTZ/DFJ model directly, or transform to a
symmetric instance by splitting each city into (in, out) copies joined by a large-negative
(or zero-cost, with offsets) edge (Jonker & Volgenant 1983), doubling n but unlocking
symmetric codes like LKH. Open-path TSP (no return): add a dummy node at distance 0 to
all cities; fixed start/end: dummy node at distance 0 to exactly those two. After
solving, cut the tour at the dummy. These transformations preserve optimality exactly —
prefer them over ad-hoc model surgery.

### Warm starts and fractional separation for DFJ

Give the MIP every advantage: set `x[i, j].Start = 1` on the edges of an ILS tour (a ~1%
solution collapses the primal side of the search immediately), and separate subtours on
*fractional* LP solutions at `MIPNODE` by computing a global minimum cut on the support
graph (Padberg & Rinaldi 1991) — if the min cut is < 2, the cut set yields a violated
SEC to add with `cbCut`. Integer-only separation (the code above) is correct but leaves
the root LP weak; fractional separation typically cuts node counts by an order of
magnitude at n ≥ 500. Implementation patterns for both callback types are in
**cutting-planes-valid-inequalities**.

## Practical Challenges

**The MTZ model stalls beyond ~80 cities.** Expected, not a bug: the MTZ LP relaxation
is far below the optimum, so branch-and-bound cannot prune. Switch to DFJ with lazy
SECs; keep MTZ only when the tour is embedded in a larger model.

**Gurobi raises an error or silently ignores `cbLazy`.** Set
`model.Params.LazyConstraints = 1` before `optimize(callback)`, and guard the callback
with `where == GRB.Callback.MIPSOL` before calling `cbGetSolution` — calling it in other
contexts errors out.

**The "optimal" solution visits only a subset of cities.** The model has degree
constraints but the SEC mechanism never fired: the callback was not passed to
`optimize()`, or the cycle-detection threshold used `> 0.5` on the wrong variable dict.
Run `validate_tour` on every extracted solution; it catches this class of bug instantly.

**Heuristic tour length does not match published TSPLIB optima.** Almost always the
rounding convention: EUC_2D rounds each leg to the nearest integer before summing. Parse
with the TSPLIB rules (reader above), recompute, and only then report gaps.

**2-opt is correct but too slow at n = 10,000.** The vectorized full-matrix sweep is
O(n²) time and memory per iteration — 100M deltas per sweep. Move to k-nearest-neighbor
candidate lists with don't-look bits (Advanced Techniques) and first-improvement
scanning; expect a ~100x speedup with no measurable quality loss.

**2-opt makes an asymmetric instance worse.** The O(1) 2-opt delta assumes
reversal-invariant edge costs; under asymmetry the reversed segment re-prices every
internal arc. Use orientation-preserving moves (Or-opt, 3-opt segment reinsertion) or
transform the instance to symmetric form first.

**Results differ between runs with "the same" setup.** Seed the construction and kick rng
(`np.random.default_rng(seed)`), fix `model.Params.Seed`, and pin `model.Params.Threads`
— Gurobi's parallel MIP is performance-nondeterministic across thread counts and even
across runs when racing is involved. Record all three with every result row.

**Out of memory building the distance matrix.** At n = 50,000, the float64 matrix is
20 GB. Keep coordinates only, compute candidate lists with a KD-tree, and evaluate edge
lengths on demand (cache the k-NN distances, which is all local search ever touches).

## Tools & Libraries

| Library / tool | When to use | Note |
|---|---|---|
| gurobipy | Exact DFJ/MTZ models, warm starts, callbacks | License required; the formulations port to any MIP API |
| Concorde | Proven-optimal symmetric TSP at scale | The reference exact code; CLI or via pyconcorde wrapper |
| LKH-3 | <1% (often optimal) heuristic tours, huge n, ATSP/variants | Helsgaun's code; `elkai` gives Python bindings |
| OR-Tools routing | Quick decent tours, free, many side constraints | GLS-based; weaker than LKH on pure TSP but very practical |
| networkx | MST, matching, Eulerian circuits (Christofides) | Fine to n ≈ 1,000; matching is the bottleneck |
| scipy.spatial | cKDTree for k-NN candidate lists; `distance.pdist` | Build neighbor lists in O(n log n) |
| tsplib95 | Parsing the full TSPLIB format zoo | Use when you need GEO, EXPLICIT, or display data |
| numpy | All heuristic code in this skill | Vectorized delta scoring; `np.random.default_rng(seed)` |

## Output Format

A complete TSP deliverable contains:

1. **Model/method summary.** Formulation chosen (DFJ lazy / MTZ / heuristic stack) with a
   one-line justification tied to instance size and proof requirement; variable and
   constraint counts for MIPs; neighborhood stack and kick type for heuristics.
2. **Solution-quality report.** One row per (instance, method, seed):

   | instance | n | method | length | bound (LB) | gap % | time s | seed |
   |---|---|---|---|---|---|---|---|
   | berlin52 | 52 | DFJ lazy | 7542 | 7542 | 0.00 | 0.4 | 0 |
   | rnd-u1000-s3 | 1000 | ILS (2opt+DB) | 23945871 | 23687014 (HK) | 1.09 | 12.1 | 3 |

   Gap is against the proven LB (MIP) or the Held-Karp bound (heuristics); state which.
3. **Validation line.** Explicit statement that `validate_tour` recomputed every reported
   length from the raw distance data, with the rounding convention named.
4. **Convergence summary** (heuristics). Best-so-far length vs kicks/time for at least 5
   seeds: median and range, not a single lucky run.
5. **Artifacts.** The tour as a 0-indexed permutation (one line, space-separated, plus
   the TSPLIB 1-indexed `.tour` file if benchmarking), the instance file or generator
   call with seed, and the exact solver parameters / heuristic settings used.
6. **Reproducibility block.** Package versions, Gurobi version and parameter overrides,
   all seeds, hardware, and time limits — enough to re-run every table row.

## Questions to Ask

- How many cities, and is that fixed or will instances grow?
- Are distances symmetric? Metric? Euclidean from coordinates, or an arbitrary matrix?
- Must optimality be proven, or is "within ~1% with high confidence" acceptable?
- What is the time budget per instance, and is this a one-off solve or a repeated batch?
- Is a Gurobi license available, or should everything run on open-source tools?
- Closed tour or open path? Fixed start/end points?
- Any side constraints (precedence, time windows, several vehicles)? Each leaves pure TSP.
- Which distance convention applies for reporting — TSPLIB integer rounding or float?
- Are there existing benchmark instances/optima to validate against?

## Related Skills

- **vehicle-routing-problem** — when there are multiple vehicles, capacities, depots, or
  time windows; the TSP is its single-route building block.
- **local-search-and-neighborhoods** — for delta-evaluation engineering, scan orders,
  candidate lists, and move data structures behind 2-opt/Or-opt.
- **cutting-planes-valid-inequalities** — for fractional subtour separation via min-cut,
  user cuts vs lazy constraints, and comb inequalities beyond basic SECs.
- **ant-colony-optimization** — pheromone-based constructive metaheuristic whose home
  benchmark is the TSP; pairs naturally with the 2-opt code here.
- **instance-generation-and-benchmarks** — TSPLIB/benchmark protocol, instance features,
  and train/test splits for tuning.
- **dynamic-programming** — Held-Karp O(n² 2ⁿ) exact DP for n ≤ ~20 and labeling
  techniques that reuse the same state-space ideas.
