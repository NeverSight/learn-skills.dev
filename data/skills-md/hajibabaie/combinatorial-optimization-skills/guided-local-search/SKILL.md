---
name: guided-local-search
description: When the user wants to escape local optima by penalizing solution features and re-optimizing an augmented objective — guided local search (GLS) design, implementation, lambda calibration, penalty decay, and pairing with fast local search. Also use when the user mentions "guided local search," "GLS," "feature penalties," "augmented objective," "penalty decay," "escape local optimum," or OR-Tools' GUIDED_LOCAL_SEARCH routing metaheuristic. For neighborhood and delta-evaluation design, see local-search-and-neighborhoods; for memory-based escape via move attributes, see tabu-search.
---

# Guided Local Search

You are an expert in guided local search (GLS) for combinatorial optimization. This skill covers feature-based penalties, the utility function, the augmented objective, calibration of the penalty weight λ, penalty decay, and the coupling of GLS with fast local search (activation bits), including its production incarnation as the GLS metaheuristic in OR-Tools routing. Use the framework below to take a user from "my 2-opt/relocate descent is stuck in a local optimum" to a calibrated GLS implementation whose escape mechanism is deterministic, cheap, and explainable feature by feature.

## Initial Assessment

Establish these facts before writing any GLS code:

- **Underlying local search.** GLS does not replace a descent; it steers one. Identify the neighborhood (2-opt, relocate, exchange, flip) and whether move deltas are O(1)/O(n). If the descent does not exist yet, design it first (see local-search-and-neighborhoods) — GLS amplifies a good descent and cannot rescue a bad one.
- **Feature set.** What solution components can carry penalties? Edges/arcs for routing, pair assignments for QAP-like problems, item-bin memberships for packing, soft-constraint violations for timetabling. A feature must be a cheap-to-test boolean property of a solution.
- **Feature costs.** Do candidate features have meaningfully different costs (edge lengths, violation degrees)? The utility function needs cost differentiation; with uniform costs GLS degrades to uniform feature rotation.
- **Objective scale.** λ has the units of the objective divided by a feature count. Record the typical objective value of a local optimum and how many features a solution exhibits — both feed the standard λ calibration.
- **Instance size and memory.** Arc features on n nodes imply an O(n²) penalty store. Decide now between a dense matrix (n up to a few thousand) and a sparse map of penalized features only.
- **Hard vs soft constraints.** Keep hard feasibility inside the move set or the construction. GLS penalties are a diversification device, not a constraint-handling device; mixing the two in one penalty term makes λ impossible to calibrate.
- **Time budget and anytime needs.** GLS is naturally anytime: every round ends at a local optimum of the augmented objective and the incumbent is always feasible. Fix the round budget or wall-clock limit up front.
- **Determinism requirements.** Given the starting solution, plain GLS is fully deterministic — useful for debugging and exact reproducibility. Randomness enters only through construction (and optional random moves in extended variants).
- **Existing tooling.** If the problem is a routing problem and OR-Tools is in the stack, the built-in `GUIDED_LOCAL_SEARCH` metaheuristic may already be the right answer; custom GLS is for problems or move sets OR-Tools does not cover.
- **Baselines and quality target.** Always measure against the construction heuristic and the plain descent. Decide whether the goal is "clearly better than descent" or "within x% of best-known on benchmarks" — the second needs multi-seed runs and a tuned λ.
- **Reporting protocol.** Seeds per instance, best/mean/std, and whether results feed a statistical comparison against ILS or tabu search.

## Algorithm Anatomy

### Features, penalties, and the augmented objective

GLS comes from Voudouris & Tsang (1999), "Guided local search and its application to the travelling salesman problem," which grew out of the GENET network for constraint satisfaction. Choose a feature set $\{1, \dots, M\}$. Feature $i$ has an indicator $I_i(s) \in \{0, 1\}$ (does solution $s$ exhibit it?), a cost $c_i \ge 0$, and an integer penalty counter $p_i$ initialized to 0. The local search minimizes the augmented objective

$$
h(s) = g(s) + \lambda \sum_{i=1}^{M} p_i \, I_i(s),
$$

where $g$ is the true objective. Penalties deform the landscape so that the current local optimum stops being one; the incumbent is always tracked on the true cost $g$, never on $h$.

### The penalization step

When the descent reaches a local optimum $s^\*$ of $h$, GLS increments the penalty of the feature(s) present in $s^\*$ that maximize the utility

$$
\mathrm{util}(s^\*, i) = I_i(s^\*) \cdot \frac{c_i}{1 + p_i}.
$$

The rationale has two halves. The numerator says: expensive features are the most suspect parts of a stuck solution, so remove those first. The denominator says: a feature already penalized many times yields diminishing information, so rotate attention across features instead of hammering one. All maximizers are penalized (ties included). After the increment, $s^\*$ is usually no longer a local optimum of $h$, and the descent resumes from it — GLS never restarts from scratch, which is what makes it cheap.

### Calibrating λ

λ is the single substantive parameter. The standard rule computes it once, at the first local optimum $s^\*_1$:

$$
\lambda = \alpha \cdot \frac{g(s^\*_1)}{\big|\{\, i : I_i(s^\*_1) = 1 \,\}\big|}.
$$

The fraction is the average cost share of one feature in a typical local optimum, so a unit penalty then "weighs" about α times an average feature. Reference values for α:

| Problem / feature set | α range | Source |
|---|---|---|
| TSP, edges under 2-opt | 1/8 – 1/2 | Voudouris & Tsang (1999) |
| VRP, arcs under relocate/exchange | 0.1 – 0.3 | Kilby, Prosser & Shaw (1999); OR-Tools default coefficient 0.1 |
| QAP, location-assignment pairs | 0.5 – 1.0 | Mills, Tsang & Ford (2003), extended GLS studies |
| Weighted constraint violations | often λ = 1 with $c_i$ = violation cost | Mills & Tsang (2000) on MAX-SAT |

The response to α is flat-bottomed: an order-of-magnitude error matters, a factor of 2 usually does not. The sensitivity sweep in Advanced Techniques makes this measurable per problem.

### Fast local search coupling

Re-running a full descent after every penalization wastes effort: the augmented matrix changed only on the penalized features. Fast local search (FLS) — the activation-bit idea of Bentley (1992), "Fast algorithms for geometric traveling salesman problems," generalized by Voudouris & Tsang — partitions the neighborhood into sub-neighborhoods (one per city, per customer, per variable), keeps an activation bit for each, scans only active ones, deactivates a sub-neighborhood after a fruitless scan, and reactivates the sub-neighborhoods touched by an applied move or by a penalization. Because penalties only *increase* arc costs, a move that does not remove a penalized feature can only have become less attractive; therefore waking just the penalized features' endpoints is sufficient to find every newly improving move. GLS + FLS descents after the first are localized and typically orders of magnitude cheaper than the initial descent.

### When GLS is the right escape mechanism

- **Use GLS when** a fast delta-evaluated descent exists, features with non-uniform costs capture "what is bad" about a solution, you want few parameters (one α) and deterministic, explainable behavior, and anytime feasibility matters.
- **Prefer tabu search when** cycling is driven by move attributes rather than by identifiable costly features, or when you need aspiration logic and frequency memory (see tabu-search).
- **Prefer ILS or large kicks when** local optima are separated by wide valleys that single-feature penalties cross too slowly — or hybridize: GLS penalties plus occasional perturbations (Extended GLS, Mills & Tsang 2000).
- **Complexity per round:** penalization is O(F) for F features present in the solution; the descent cost is dominated by the reactivated sub-neighborhoods. Memory is O(M) penalty counters — O(n²) for arc features, which is the binding constraint on very large instances.

### Parameter guidance

| Parameter | Typical range | Increasing it buys | At the cost of |
|---|---|---|---|
| α (sets λ) | 0.1 – 0.5 (see table above) | Faster escapes, broader exploration | True-cost distortion; search chases penalties |
| Penalty increment | 1 (fixed) | Larger steps diversify faster | Coarser, less informative memory |
| Decay factor ρ (per K rounds) | 0.8 – 1.0 (1.0 = off) | Forgets stale penalties, restores late-run mobility | May revisit already-explored optima |
| Decay period K | 50 – 500 rounds | Smoother forgetting | More bookkeeping, full FLS reactivation |
| Patience (rounds without new best) | 10² – 10³ | Fewer premature stops | Wasted budget on exhausted runs |
| FLS activation scope | Endpoints of penalized features | Minimal-cost descents | None for pure penalization (see argument above); decay needs full reactivation |

Tune α first; everything else is secondary. For operator-level choices inside the descent (neighborhood order, first vs best improvement, candidate lists), see local-search-and-neighborhoods rather than re-deriving them here.

## Reusable GLS Engine

The loop is problem-independent; all problem knowledge sits in the objective, the feature extraction, and the descent.

```text
GUIDED-LOCAL-SEARCH(s0)
  p_i <- 0 for every feature i                   // penalty counters
  s   <- LOCAL-SEARCH(s0 ; g)                    // first descent on the TRUE cost
  s*, g* <- s, g(s)
  lambda <- alpha * g(s) / #features-present(s)  // one-time calibration
  repeat
      U <- { i : I_i(s) = 1 }                    // features of this local optimum
      util_i <- c_i / (1 + p_i)        for i in U
      for every i in U maximizing util_i:  p_i <- p_i + 1
      reactivate sub-neighborhoods touching penalized features    // FLS
      s <- LOCAL-SEARCH(s ; h),  h = g + lambda * sum_i p_i I_i   // resume, no restart
      if g(s) < g*:  s*, g* <- s, g(s)           // incumbent on TRUE cost only
  until round budget exhausted, or no new incumbent for `patience` rounds
  return s*, g*
```

A generic driver with flat feature ids. It treats solutions as opaque objects and is handy for problems whose features map naturally to one integer range (columns, items, violations):

```python
import copy
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

import numpy as np


@dataclass
class GLSResult:
    """Best-found solution plus run diagnostics for reporting."""
    best: Any
    best_cost: float
    lam: float
    rounds: int
    history: list[float] = field(default_factory=list)


def guided_local_search(
    initial: Any,
    objective: Callable[[Any], float],
    features_of: Callable[[Any], np.ndarray],
    feature_cost: np.ndarray,
    local_search: Callable[[Any, np.ndarray, float], Any],
    alpha: float = 0.3,
    lam: float | None = None,
    max_rounds: int = 1000,
    patience: int = 0,
    decay: float = 1.0,
    decay_every: int = 0,
    snapshot: Callable[[Any], Any] = copy.deepcopy,
) -> GLSResult:
    """Problem-independent GLS driver.

    `local_search(s, penalties, lam)` must return a local optimum of the
    augmented objective g(s) + lam * penalties[features_of(s)].sum(); it may
    mutate `s` in place. `features_of(s)` returns the integer ids of the
    features present in `s`; `feature_cost[i]` is the utility numerator c_i.
    The incumbent is tracked on the TRUE objective, never the augmented one.
    """
    penalties = np.zeros(feature_cost.shape[0])
    s = local_search(initial, penalties, 0.0)        # first descent: true cost
    best, best_cost = snapshot(s), objective(s)
    if lam is None:
        lam = alpha * best_cost / max(features_of(s).size, 1)
    history = [best_cost]
    since_best = 0
    rounds = 0
    for rounds in range(1, max_rounds + 1):
        present = features_of(s)
        util = feature_cost[present] / (1.0 + penalties[present])
        top = present[util >= util.max() - 1e-12]    # penalize ALL maximizers
        penalties[top] += 1.0
        if decay_every and rounds % decay_every == 0:
            penalties *= decay                       # multiplicative forgetting
        s = local_search(s, penalties, lam)
        cost = objective(s)
        history.append(cost)
        if cost < best_cost - 1e-9:
            best, best_cost = snapshot(s), cost
            since_best = 0
        else:
            since_best += 1
            if patience and since_best >= patience:
                break
    return GLSResult(best, best_cost, lam, rounds, history)
```

The two worked examples below specialize this loop instead of calling it: with arc features, a penalty *matrix* indexed by `(i, j)` plus an incrementally maintained augmented matrix is both faster and clearer than flattening n² arcs into one id range, so the (short) loop is repeated with matrix bookkeeping.

## Worked Example: TSP with Edge-Feature Penalties

The original GLS showcase. Features are tour edges: feature {i, j} has cost $c_{ij} = d_{ij}$ and indicator "the tour uses edge {i, j}". The descent is 2-opt on the augmented matrix $\hat d = d + \lambda P$, with FLS activation bits per city. Instance helpers first:

```python
import numpy as np


def random_euclidean_instance(n: int, seed: int = 0) -> tuple[np.ndarray, np.ndarray]:
    """Random points in the unit square and their distance matrix."""
    rng = np.random.default_rng(seed)
    pts = rng.random((n, 2))
    dist = np.linalg.norm(pts[:, None, :] - pts[None, :, :], axis=2)
    return pts, dist


def tour_length(tour: np.ndarray, dist: np.ndarray) -> float:
    """True (unpenalized) tour length."""
    return float(dist[tour, np.roll(tour, -1)].sum())


def nearest_neighbor_tour(dist: np.ndarray, start: int = 0) -> np.ndarray:
    """Greedy nearest-neighbor construction."""
    n = dist.shape[0]
    unvisited = np.ones(n, dtype=bool)
    unvisited[start] = False
    tour = [start]
    for _ in range(n - 1):
        cur = tour[-1]
        masked = np.where(unvisited, dist[cur], np.inf)
        nxt = int(np.argmin(masked))
        unvisited[nxt] = False
        tour.append(nxt)
    return np.array(tour)
```

The descent. A 2-opt move is an unordered pair of tour rows $(k, j)$ with $k + 2 \le j$ and $(k, j) \ne (0, n-1)$; applying it reverses `tour[k+1 .. j]`. For each active city, both of its incident tour edges are scanned against all partner edges in one vectorized pass — O(n) per scan:

```python
import numpy as np


def _best_move_for_edge(r: int, tour: np.ndarray, aug: np.ndarray) -> tuple[float, int, int]:
    """Best 2-opt move removing tour edge r = (tour[r], tour[(r+1) % n]).

    Returns (delta, k, j) for reversing tour[k+1 .. j]; delta = +inf when the
    edge admits no move. One vectorized O(n) scan over all partner edges.
    """
    n = tour.shape[0]
    succ = np.roll(tour, -1)
    ks = np.arange(0 if r < n - 1 else 1, r - 1)      # r as the larger row
    js = np.arange(r + 2, n - 1 if r == 0 else n)     # r as the smaller row
    cand_k = np.concatenate([ks, np.full(js.shape, r)])
    cand_j = np.concatenate([np.full(ks.shape, r), js])
    if cand_k.size == 0:
        return np.inf, -1, -1
    t1, t2 = tour[cand_k], succ[cand_k]               # first removed edge
    t3, t4 = tour[cand_j], succ[cand_j]               # second removed edge
    delta = aug[t1, t3] + aug[t2, t4] - aug[t1, t2] - aug[t3, t4]
    m = int(np.argmin(delta))
    return float(delta[m]), int(cand_k[m]), int(cand_j[m])


def two_opt_descent(tour: np.ndarray, aug: np.ndarray, active: np.ndarray) -> np.ndarray:
    """Fast-local-search 2-opt descent (don't-look bits, Bentley 1992).

    Only cities with active[city] == True are scanned; a city is deactivated
    after a fruitless scan of its two incident edges and reactivated whenever
    one of its tour edges changes. GLS wakes just the endpoints of penalized
    edges, so every descent after the first is localized. Mutates `tour`.
    """
    n = tour.shape[0]
    pos = np.empty(n, dtype=np.int64)
    pos[tour] = np.arange(n)
    while True:
        scan = tour[active[tour]]                     # active cities, tour order
        if scan.size == 0:
            return tour
        for a in scan:
            if not active[a]:
                continue
            moved = True
            while moved:                              # exhaust moves around a
                moved = False
                i = int(pos[a])
                for r in ((i - 1) % n, i):            # a's two incident edges
                    delta, k, j = _best_move_for_edge(r, tour, aug)
                    if delta < -1e-10:
                        ends = [tour[k], tour[(k + 1) % n], tour[j], tour[(j + 1) % n]]
                        tour[k + 1 : j + 1] = tour[k + 1 : j + 1][::-1]
                        pos[tour[k + 1 : j + 1]] = np.arange(k + 1, j + 1)
                        active[ends] = True           # wake all four endpoints
                        moved = True
                        break
            active[a] = False
```

The GLS driver. Penalties live in a symmetric matrix; the augmented matrix is maintained incrementally (only penalized entries change, by exactly λ):

```python
import numpy as np


def gls_tsp(
    dist: np.ndarray,
    alpha: float = 0.3,
    max_rounds: int = 1000,
    patience: int = 250,
    seed: int = 0,
) -> tuple[np.ndarray, float, list[float]]:
    """Guided local search for the symmetric TSP with edges as features.

    Utility of edge (i, j) in the current tour: d[i, j] / (1 + pen[i, j]).
    The incumbent is tracked on the TRUE tour length. Uses two_opt_descent,
    nearest_neighbor_tour, and tour_length defined above.
    """
    n = dist.shape[0]
    rng = np.random.default_rng(seed)
    tour = nearest_neighbor_tour(dist, start=int(rng.integers(n)))
    pen = np.zeros_like(dist)
    aug = dist.copy()
    active = np.ones(n, dtype=bool)
    tour = two_opt_descent(tour, aug, active)         # first descent: true cost
    best, best_len = tour.copy(), tour_length(tour, dist)
    lam = alpha * best_len / n                        # n features in any tour
    history = [best_len]
    since_best = 0
    for _ in range(max_rounds):
        u, v = tour, np.roll(tour, -1)
        util = dist[u, v] / (1.0 + pen[u, v])
        top = np.flatnonzero(util >= util.max() - 1e-12)
        pen[u[top], v[top]] += 1.0                    # symmetric edge penalty
        pen[v[top], u[top]] += 1.0
        aug[u[top], v[top]] += lam                    # incremental augmentation
        aug[v[top], u[top]] += lam
        active[u[top]] = True                         # FLS: wake only endpoints
        active[v[top]] = True
        tour = two_opt_descent(tour, aug, active)
        length = tour_length(tour, dist)
        history.append(length)
        if length < best_len - 1e-9:
            best, best_len = tour.copy(), length
            since_best = 0
        else:
            since_best += 1
            if patience and since_best >= patience:
                break
    return best, best_len, history
```

Demonstration on two tiny synthetic instances — one with a known optimum, one harder:

```python
import numpy as np

# Sanity instance: points on a circle. The optimal tour is the convex hull.
n = 32
ang = np.linspace(0.0, 2.0 * np.pi, n, endpoint=False)
pts = np.column_stack([np.cos(ang), np.sin(ang)])
dist = np.linalg.norm(pts[:, None, :] - pts[None, :, :], axis=2)
optimum = n * 2.0 * np.sin(np.pi / n)                 # regular n-gon perimeter
best, best_len, _ = gls_tsp(dist, alpha=0.3, max_rounds=200, seed=0)
print(f"circle: optimum {optimum:.6f}   GLS {best_len:.6f}")

# Harder instance: uniform random points.
pts, dist = random_euclidean_instance(80, seed=42)
nn_len = tour_length(nearest_neighbor_tour(dist), dist)
best, best_len, hist = gls_tsp(dist, alpha=0.3, max_rounds=800, seed=42)
print(f"random: NN {nn_len:.4f} -> GLS {best_len:.4f} in {len(hist) - 1} rounds")
# Expected: the circle case matches the optimum to ~1e-9; on the random
# instance GLS beats nearest-neighbor by roughly 15-25% and lands within a
# few percent of optimal — typical for 2-opt-based GLS at this size.
```

## Worked Example: CVRP with GLS over Relocate and Exchange

Kilby, Prosser & Shaw (1999), "Guided local search for the vehicle routing problem with time windows," established arc penalties as the standard GLS feature set for routing; OR-Tools routing implements exactly this scheme. Features are the arcs used by the solution (depot arcs included), with cost equal to arc length. The descent combines relocate (move one customer anywhere, intra- or inter-route) and inter-route exchange (swap two customers), both with O(1) augmented-arc deltas. Node 0 is the depot; customers are 1..n.

```python
import numpy as np


def route_cost(route: list[int], dist: np.ndarray) -> float:
    """Cost of depot -> route -> depot under the given arc-cost matrix."""
    if not route:
        return 0.0
    path = np.array([0, *route, 0])
    return float(dist[path[:-1], path[1:]].sum())


def solution_cost(routes: list[list[int]], dist: np.ndarray) -> float:
    """Total true cost over all routes."""
    return sum(route_cost(r, dist) for r in routes)


def check_cvrp(routes: list[list[int]], demand: np.ndarray,
               capacity: float, n_customers: int) -> None:
    """Independent feasibility check: visit-once and capacity."""
    visited = sorted(c for r in routes for c in r)
    assert visited == list(range(1, n_customers + 1)), "visit-once violated"
    for r in routes:
        assert sum(demand[c] for c in r) <= capacity + 1e-9, "capacity violated"


def greedy_routes(dist: np.ndarray, demand: np.ndarray,
                  capacity: float) -> list[list[int]]:
    """Nearest-neighbor construction; opens a new route when nothing fits."""
    n = dist.shape[0] - 1
    unrouted = set(range(1, n + 1))
    routes: list[list[int]] = []
    while unrouted:
        cur, load, route = 0, 0.0, []
        while True:
            feasible = [c for c in unrouted if load + demand[c] <= capacity]
            if not feasible:
                break
            nxt = min(feasible, key=lambda c: dist[cur, c])
            route.append(nxt)
            unrouted.remove(nxt)
            load += float(demand[nxt])
            cur = nxt
        routes.append(route)
    return routes
```

The descent is best-improvement over both neighborhoods. The move scan is loop-based on purpose: capacity feasibility and variable-length routes break clean broadcasting, and at demonstration sizes clarity wins. For larger instances, restrict relocate candidates to the k nearest neighbors of each customer (granular search, Toth & Vigo 2003) and add per-customer activation bits exactly as in the TSP example.

```python
import numpy as np


def cvrp_descent(
    routes: list[list[int]],
    aug: np.ndarray,
    demand: np.ndarray,
    capacity: float,
) -> list[list[int]]:
    """Best-improvement descent over relocate and inter-route exchange on the
    augmented arc-cost matrix. Every move delta is O(1) arc arithmetic.
    Returns the improved solution; emptied routes are dropped."""
    routes = [r[:] for r in routes if r]
    while True:
        loads = [float(sum(demand[c] for c in r)) for r in routes]
        padded = [[0, *r, 0] for r in routes]
        best_delta = -1e-10
        best_move: tuple | None = None

        # Relocate: move customer p[k] from (route i) to (route j, slot m).
        for i, p in enumerate(padded):
            for k in range(1, len(p) - 1):
                c = p[k]
                gain = aug[p[k - 1], c] + aug[c, p[k + 1]] - aug[p[k - 1], p[k + 1]]
                for j, q in enumerate(padded):
                    if j != i and loads[j] + demand[c] > capacity:
                        continue
                    for m in range(len(q) - 1):
                        if j == i and m in (k - 1, k):
                            continue                  # reinserts in place
                        delta = (aug[q[m], c] + aug[c, q[m + 1]]
                                 - aug[q[m], q[m + 1]] - gain)
                        if delta < best_delta:
                            best_delta = delta
                            best_move = ("relocate", i, k - 1, j, m)

        # Exchange: swap customer p[k] (route i) with q[m] (route j > i).
        for i, p in enumerate(padded):
            for j in range(i + 1, len(padded)):
                q = padded[j]
                for k in range(1, len(p) - 1):
                    c1 = p[k]
                    for m in range(1, len(q) - 1):
                        c2 = q[m]
                        if (loads[i] - demand[c1] + demand[c2] > capacity
                                or loads[j] - demand[c2] + demand[c1] > capacity):
                            continue
                        delta = (
                            aug[p[k - 1], c2] + aug[c2, p[k + 1]]
                            - aug[p[k - 1], c1] - aug[c1, p[k + 1]]
                            + aug[q[m - 1], c1] + aug[c1, q[m + 1]]
                            - aug[q[m - 1], c2] - aug[c2, q[m + 1]]
                        )
                        if delta < best_delta:
                            best_delta = delta
                            best_move = ("exchange", i, k - 1, j, m - 1)

        if best_move is None:
            return [r for r in routes if r]
        kind, i, k, j, m = best_move
        if kind == "relocate":
            c = routes[i].pop(k)
            if j == i and m > k:
                m -= 1                                # indices shift after pop
            routes[j].insert(m, c)
            routes = [r for r in routes if r]
        else:
            routes[i][k], routes[j][m] = routes[j][m], routes[i][k]
```

The GLS driver mirrors the TSP one; only the feature extraction (arcs of all routes) and the λ denominator (number of arcs, which is `n_customers + n_routes`) differ:

```python
import numpy as np


def gls_cvrp(
    dist: np.ndarray,
    demand: np.ndarray,
    capacity: float,
    alpha: float = 0.2,
    max_rounds: int = 400,
    patience: int = 120,
) -> tuple[list[list[int]], float, list[float]]:
    """GLS for the CVRP with arcs as features (Kilby-Prosser-Shaw scheme).

    Uses greedy_routes, cvrp_descent, and solution_cost defined above.
    Penalties are symmetric so the augmented matrix stays a single lookup.
    """
    routes = greedy_routes(dist, demand, capacity)
    pen = np.zeros_like(dist)
    aug = dist.copy()
    routes = cvrp_descent(routes, aug, demand, capacity)
    best = [r[:] for r in routes]
    best_cost = solution_cost(routes, dist)
    n_arcs = sum(len(r) + 1 for r in routes)
    lam = alpha * best_cost / n_arcs
    history = [best_cost]
    since_best = 0
    for _ in range(max_rounds):
        arcs = np.array([(u, v) for r in routes
                         for u, v in zip([0, *r], [*r, 0])])
        u, v = arcs[:, 0], arcs[:, 1]
        util = dist[u, v] / (1.0 + pen[u, v])
        top = np.flatnonzero(util >= util.max() - 1e-12)
        pen[u[top], v[top]] += 1.0
        pen[v[top], u[top]] += 1.0
        aug[u[top], v[top]] += lam
        aug[v[top], u[top]] += lam
        routes = cvrp_descent(routes, aug, demand, capacity)
        cost = solution_cost(routes, dist)
        history.append(cost)
        if cost < best_cost - 1e-9:
            best, best_cost = [r[:] for r in routes], cost
            since_best = 0
        else:
            since_best += 1
            if patience and since_best >= patience:
                break
    return best, best_cost, history
```

Demonstration on a tiny synthetic instance, with the independent validator:

```python
import numpy as np

rng = np.random.default_rng(7)
n = 16
pts = np.vstack([np.array([[0.5, 0.5]]), rng.random((n, 2))])  # row 0 = depot
dist = np.linalg.norm(pts[:, None, :] - pts[None, :, :], axis=2)
demand = np.concatenate([[0.0], rng.integers(1, 10, size=n).astype(float)])
capacity = 25.0

start_cost = solution_cost(greedy_routes(dist, demand, capacity), dist)
routes, cost, hist = gls_cvrp(dist, demand, capacity, alpha=0.2, max_rounds=200)
check_cvrp(routes, demand, capacity, n)
print(f"greedy {start_cost:.4f} -> GLS {cost:.4f} with {len(routes)} routes")
# Expected: the feasibility check passes and GLS finishes 15-30% below the
# greedy construction; at 16 customers the result is usually optimal or
# within ~1% of it.
```

## Advanced Techniques

### Penalty decay and resets

Penalties are memory, and memory goes stale: after thousands of rounds the augmented landscape no longer resembles the true one, and the search loses its sense of direction near good solutions. Two standard fixes. Multiplicative decay `p *= rho` (ρ ≈ 0.8–0.99) every K rounds, as implemented in the generic driver above — smooth forgetting that keeps relative penalty order. Or full resets when no incumbent improvement for a long stretch, which behaves like a soft restart from the current solution. Both interact with FLS: decay changes augmented costs *downward*, so the "wake only penalized endpoints" argument breaks and all activation bits must be set after a decay step (and the augmented matrix rebuilt as `dist + lam * pen`). OR-Tools resets penalties when a new overall best is found, a pragmatic variant of the same idea.

### Aspiration and random moves (Extended GLS)

Mills & Tsang (2000), "Guided local search for solving SAT and weighted MAX-SAT problems," add two ingredients. Aspiration: accept any move that improves the *true* incumbent even if the augmented delta is non-improving — penalties should never block a new best solution. Random moves: with small probability (≈1/n per step) apply a random neighbor instead of the best one, injecting cheap diversity. Both reduce λ sensitivity substantially, which is the main practical reason to use them: when a clean α sweep is unaffordable, Extended GLS is more forgiving of a mis-set λ.

### Measuring λ sensitivity

Because the α response is flat-bottomed, a coarse logarithmic sweep is enough to locate the plateau, and it doubles as evidence in a methods section:

```python
import numpy as np

pts, dist = random_euclidean_instance(80, seed=3)   # helper defined above
for alpha in (0.05, 0.125, 0.25, 0.5, 1.0):
    _, best_len, hist = gls_tsp(dist, alpha=alpha, max_rounds=400, seed=3)
    print(f"alpha={alpha:<6} best={best_len:.4f} rounds={len(hist) - 1}")
# Expected: a flat-bottomed response — alpha in [0.125, 1.0] gives
# near-identical tour lengths, while alpha=0.05 under-penalizes (slow escape)
# and is visibly worse; pushing alpha well above 1 eventually degrades true
# cost as the search chases penalty relief instead of tour length.
```

### Relation to OR-Tools routing GLS

The OR-Tools routing library ships GLS as its strongest default metaheuristic for vehicle routing: features are solution arcs, the penalized term is added to the arc-cost evaluator, and `guided_local_search_lambda_coefficient` is exactly the α of this skill (default 0.1). Use it when the problem fits the routing model (capacities, time windows, pickup-delivery); write custom GLS when the move set or feature set does not:

```python
from ortools.constraint_solver import pywrapcp, routing_enums_pb2


def solve_cvrp_ortools_gls(
    dist_int: list[list[int]],
    demand: list[int],
    capacity: int,
    n_vehicles: int,
    seconds: int = 10,
) -> pywrapcp.Assignment | None:
    """CVRP via OR-Tools routing with the built-in GLS metaheuristic.

    Costs must be integers; scale float distances by e.g. 1000 and round.
    """
    manager = pywrapcp.RoutingIndexManager(len(dist_int), n_vehicles, 0)
    routing = pywrapcp.RoutingModel(manager)

    def arc_cost(i: int, j: int) -> int:
        return dist_int[manager.IndexToNode(i)][manager.IndexToNode(j)]

    def demand_cb(i: int) -> int:
        return demand[manager.IndexToNode(i)]

    transit = routing.RegisterTransitCallback(arc_cost)
    routing.SetArcCostEvaluatorOfAllVehicles(transit)
    dem = routing.RegisterUnaryTransitCallback(demand_cb)
    routing.AddDimensionWithVehicleCapacity(
        dem, 0, [capacity] * n_vehicles, True, "Load")
    params = pywrapcp.DefaultRoutingSearchParameters()
    params.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    params.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    params.guided_local_search_lambda_coefficient = 0.1
    params.time_limit.FromSeconds(seconds)
    return routing.SolveWithParameters(params)
# Expected: on small CVRPs this matches or beats the custom GLS above within
# a few seconds; GLS requires a time limit because it never proves optimality.
```

### Feature design beyond arcs

Arcs are not the only option. For QAP-style problems, penalize location-assignment pairs (facility f at site s) with cost equal to that pair's contribution to the objective. For timetabling, penalize individual soft-constraint violations with cost equal to the violation weight — GLS then concentrates repair effort on the most expensive violations first. For packing/selection problems, penalize item-container memberships. Two design rules carry across domains: a feature must be removable by the move set (penalizing something the neighborhood cannot change just distorts the landscape), and feature costs should reflect each feature's marginal contribution to $g$ so the utility numerator means something. When two feature families have different cost scales, give each its own λ calibrated separately.

## Practical Challenges

**The search never escapes, or escapes and never returns to good regions.** Both are λ symptoms. Too small: the augmented descent re-derives the same local optimum for many consecutive rounds (watch for repeated identical costs in the history). Too large: the true cost of visited optima drifts steadily upward because the search optimizes penalty relief, not the objective. Run the logarithmic α sweep, pick the plateau, and prefer the plateau's lower edge — under-penalizing wastes rounds, over-penalizing destroys solution quality.

**The reported "best" was read off the augmented objective.** A classic bug: tracking the incumbent inside the descent, which sees only `aug`. The incumbent must be updated from the true objective after each round, and the final solution re-evaluated with an independent cost function (as `tour_length`/`solution_cost` do here) before any number is reported.

**Penalties accumulate until the landscape is unrecognizable.** After many rounds, large swaths of the instance carry penalties and descents wander. Apply multiplicative decay every K rounds, reset on new incumbents (the OR-Tools convention), or cap individual penalty counters. Remember that any downward penalty change requires waking all FLS activation bits.

**Uniform feature costs make the utility function useless.** With identical $c_i$, utility reduces to $1/(1+p_i)$ and GLS rotates through features in round-robin order — legal, but no smarter than uniform perturbation. Recover differentiation by using violation magnitudes, regret values, or marginal objective contributions as costs; if genuinely no differentiation exists, consider tabu search instead, whose memory does not depend on feature costs.

**The O(n²) penalty matrix does not fit in memory.** Only features that have actually been penalized need storage — at most (rounds × ties) of them. Replace the matrix with a dict keyed by arc, and compute augmented costs as `dist[i, j] + lam * pen.get((i, j), 0)` inside the delta evaluation. The asymmetric-instance case needs no symmetrization, halving entries again.

**Every descent rescans the whole neighborhood.** Without FLS, GLS loses its main speed advantage and benchmark comparisons become unfair to it (Voudouris & Tsang's TSP results rely on fast local search). Penalization only increases costs of moves that keep the penalized feature, so waking just the penalized features' sub-neighborhoods provably suffices — implement activation bits as in `two_opt_descent` above.

**Delta evaluation silently breaks after augmentation.** If the descent computes deltas from `dist` but acceptance uses `aug` (or vice versa), the search loops or stalls. Keep one matrix — the augmented one — as the only lookup inside the descent, maintain it incrementally when penalties change, and never mix true and augmented arithmetic in a single delta.

**GLS loses to ILS or tabu search in a fair benchmark.** First check the descent itself: GLS amplifies a descent, so a weak neighborhood (e.g., 2-opt without candidate lists on large TSPs) caps what any penalty scheme can do. Then check λ and FLS. If GLS is still behind, hybridize — penalties plus occasional double-bridge-style kicks is a strong combination — or accept the verdict: on problems where cycling is attribute-driven rather than cost-driven, tabu search is structurally better suited.

## Tools & Libraries

| Library / tool | When to use | Note |
|---|---|---|
| numpy | All custom GLS implementations here | Penalty matrices, vectorized edge scans, `np.random.default_rng(seed)` for construction |
| OR-Tools routing (`pywrapcp`) | Production TSP/VRP variants | `GUIDED_LOCAL_SEARCH` metaheuristic; `guided_local_search_lambda_coefficient` = α, default 0.1; needs a time limit |
| tsplib95 | TSP benchmark instances | Parses TSPLIB; feeds the edge-penalty example directly |
| vrplib | CVRPLIB / Solomon instances | Instance parsing plus best-known solutions for gap reporting |
| pyvrp | Strong VRP baseline (HGS) | Compare custom GLS against the state of the art before claiming quality |
| pandas | Experiment result tables | One row per (instance, seed, α, rounds, best, time) |
| matplotlib | Diagnostics | Plot true vs augmented cost per round; penalty heatmaps reveal where the search focuses |

## Output Format

A complete GLS deliverable contains, in order:

1. **Configuration summary** — a table of every choice that affects results:

```text
Instance            : random Euclidean TSP, n=80, seed 42
Construction        : nearest neighbor (random start)
Local search        : 2-opt, best-improvement per edge, FLS activation bits
Features / costs    : tour edges / edge length
alpha (lambda rule) : 0.3  ->  lambda = 0.00321 (calibrated at first optimum)
Penalty increment   : 1; decay: off; patience: 250 rounds; budget: 800 rounds
```

2. **Convergence report** — rounds executed, round at which the incumbent was last improved, number of penalization events, share of distinct features ever penalized, and the best-so-far curve (true cost only). A flat tail longer than `patience` justifies the stop.
3. **Solution quality** — best/mean/std of the true objective over at least 10 seeds per instance, gap to the optimum or best-known solution where available, and the same statistics for the plain descent baseline so the GLS contribution is isolated.
4. **Validation statement** — the final solution re-checked by an independent evaluator (feasibility plus objective recomputation, as in `check_cvrp`), with the checked value matching the reported one.
5. **Artifacts** — per-round history CSV (round, true cost, incumbent, penalized features), the best solution in a problem-native format (tour order, route lists), and optionally a route/tour plot and a penalty heatmap.

Never report the augmented objective as a result; it is an internal control signal. When comparing against other metaheuristics, equalize the evaluation budget (moves or wall-clock, not rounds — GLS rounds are much cheaper than ILS iterations under FLS).

## Questions to Ask

- What local search and neighborhood already exist, and are move deltas O(1)?
- What are the candidate features, and do their costs differ meaningfully?
- How large are instances — does an O(n²) penalty matrix fit, or is a sparse map needed?
- Is the problem a routing problem where OR-Tools' built-in GLS would do, or is custom code required?
- How are hard constraints handled — feasibility-preserving moves, or a separate penalty term (kept apart from GLS penalties)?
- What is the time budget per run, and is anytime behavior required?
- What baseline must GLS beat — plain descent, ILS, tabu search, best-known solutions?
- How many seeds and instances will the evaluation use, and what statistics are expected?
- Should the run be fully deterministic for reproducibility, or is randomized construction acceptable?

## Related Skills

- **local-search-and-neighborhoods** — design the underlying descent: neighborhood structure, scanning order, and O(1)/O(n) delta evaluation that GLS amplifies.
- **tabu-search** — the other principal escape mechanism; choose attribute-based memory when cycling rather than feature cost is the obstacle, or hybridize it with GLS penalties.
- **traveling-salesman-problem** — formulations, construction heuristics, and benchmark handling behind the edge-penalty worked example.
- **vehicle-routing-problem** — CVRP variants, MIP models, and the ALNS/OR-Tools context in which routing GLS competes.
