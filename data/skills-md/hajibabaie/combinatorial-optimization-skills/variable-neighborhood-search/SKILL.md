---
name: variable-neighborhood-search
description: When the user wants to design or implement variable neighborhood search and its family — VND, basic VNS, general VNS, and skewed VNS — choosing and ordering neighborhoods, designing shaking moves, and deciding when systematic neighborhood change beats a single neighborhood. Also use when the user mentions "variable neighborhood search," "VNS," "VND," "shaking," "neighborhood change," or when a local search keeps returning to the same local optimum. For move design and delta evaluation, see local-search-and-neighborhoods; for perturbation-restart loops, see iterated-local-search.
---

# Variable Neighborhood Search

You are an expert in variable neighborhood search (VNS), the metaheuristic family built on systematic change of neighborhood structures: variable neighborhood descent (VND), reduced VNS (RVNS), basic VNS (BVNS), general VNS (GVNS), skewed VNS (SVNS), and variable neighborhood decomposition search (VNDS). This skill covers neighborhood ordering, shaking design, neighborhood-change rules, and complete worked implementations on the p-median problem and the capacitated vehicle routing problem (CVRP). Use the framework below to pick the right family member, assemble it from reusable components, and validate the result.

## Initial Assessment

Establish the following before designing or coding any VNS:

- **Representation.** Permutation, subset selection, partition into routes, or assignment? The representation fixes which neighborhood structures exist at all. If the representation itself is open, settle it first (see **solution-encodings** in this repository's operator skills).
- **Move inventory.** List every candidate move type (swap, relocate, 2-opt, k-interchange, segment exchange), its neighborhood size, and the cost of evaluating one move. VNS pays off only when at least two genuinely different move types are available; with a single strong move type, **iterated-local-search** is the simpler design.
- **Delta evaluation.** Determine for each move whether the objective change is computable in O(1) or O(n) without re-evaluating the whole solution. A VND scanning O(n^2) moves with full O(n) re-evaluation per move is unusable beyond toy sizes; see **local-search-and-neighborhoods** for delta-evaluation patterns.
- **Constraint structure.** Which constraints are hard? Can shaking and descent stay feasible by construction (capacity-checked insertions), or is a repair step or penalty needed? Feasible-by-construction is strongly preferred inside VNS because the neighborhood-change logic assumes comparable objective values.
- **Instance size and time budget.** Number of decision elements (clients, customers, jobs), wall-clock budget per run, and number of runs (tuning plus final experiments). This decides best- vs first-improvement, candidate lists, and whether VNDS is needed.
- **Quality target.** Gap to best-known solutions, gap to an exact bound, or simply "beat the current heuristic under equal budget"? The target determines how much engineering (candidate lists, caching) is justified.
- **Baseline.** Confirm what already exists: a construction heuristic, a plain local search, an ILS. VNS must be compared against the strongest of these under the same time budget, with the same underlying moves.
- **Exact reference for validation.** On small instances, an exact model (Gurobi, HiGHS) or exhaustive enumeration should confirm that the VNS reaches the optimum. Plan this check before scaling up.
- **Reproducibility requirements.** Seeded `np.random.default_rng`, and a stopping rule that is reproducible (shake budget) versus one that is fair across machines (wall clock). Decide which the deliverable needs; record both.
- **Data format.** Coordinates versus explicit distance matrix; symmetric or asymmetric costs; integer or float objective (sets the improvement tolerance).
- **Output expectations.** One good solution, or a statistical comparison across seeds and instances with convergence evidence? This changes how much instrumentation the implementation needs from the start.

## The VNS Family: Anatomy and Variants

VNS solves

$$
\min_{x \in S} f(x)
$$

using a finite set of neighborhood structures $N_1, N_2, \dots, N_{k_{\max}}$ with $N_k(x) \subseteq S$. A solution $x$ is a *local optimum with respect to* $N_k$ if $f(x) \le f(y)$ for all $y \in N_k(x)$. The method rests on three empirical observations (Mladenović & Hansen 1997, "Variable neighborhood search"):

1. A local optimum with respect to one neighborhood structure is not necessarily a local optimum with respect to another.
2. A global optimum is a local optimum with respect to every possible neighborhood structure.
3. In many problems, local optima with respect to one or several neighborhoods are relatively close to each other and to the global optimum.

Observation 1 motivates VND: keep descending as long as *any* neighborhood in a list contains an improving move. Observation 2 makes the VND stopping condition meaningful: the output is locally optimal for the whole list, a much stronger condition than single-neighborhood local optimality. Observation 3 motivates recentering: after every improvement, shake again from the new incumbent rather than restarting from scratch.

Every family member shares one control mechanism, the **neighborhood change step** applied after a trial solution $x''$ is produced from the incumbent $x$:

$$
\text{if } f(x'') < f(x): \quad x \leftarrow x'',\; k \leftarrow 1 \qquad \text{else: } \quad k \leftarrow k + 1
$$

Keep two neighborhood lists conceptually separate — conflating them is the most common VNS design error:

- the **shaking list** $N_1, \dots, N_{k_{\max}}$: sampled *randomly*, usually nested ($N_k \subset N_{k+1}$) or parameterized by strength $k$, so that $k$ escalates perturbation size;
- the **descent list** $M_1, \dots, M_{\ell_{\max}}$ inside VND: scanned *deterministically* for the best (or first) improving move, usually consisting of complementary move types rather than nested sets.

| Variant | Shaking | Improvement step | Acceptance | Use when |
|---|---|---|---|---|
| VND | none (deterministic) | best-improvement scan of $M_1 \dots M_{\ell_{\max}}$ | improving only | as the local search inside GVNS, or alone when the budget allows a single descent |
| RVNS (reduced) | random $x' \in N_k(x)$ | none | improving only | evaluation is cheap but any full descent is too expensive (very large instances) |
| BVNS (basic) | random $x' \in N_k(x)$ | one local search, single neighborhood | improving only | the default first design: one strong move type plus an escalating shake |
| GVNS (general) | random $x' \in N_k(x)$ | full VND over $M_1 \dots M_{\ell_{\max}}$ | improving only | several complementary move types exist (the usual case in routing and scheduling) |
| SVNS (skewed) | random $x' \in N_k(x)$ | local search or VND | $f(x'') - \alpha\,\rho(x, x'') < f(x)$ | good local optima sit in valleys far apart; improving-only acceptance stalls |
| VNDS (decomposition) | select a size-$k$ subproblem | optimize the subproblem, rest fixed | improving only | instances too large to improve as a whole |

### Neighborhood ordering

- Order the **descent list** by increasing scan cost (neighborhood size times per-move evaluation cost). A cheap neighborhood run to local optimality first removes most defects before any expensive scan starts.
- When improvement statistics are available, place neighborhoods with a higher empirical probability of improving first. Re-measure after design changes; orderings are problem- and instance-class-specific.
- Make the **shaking list** nested or strength-parameterized: $N_k$ = "apply $k$ elementary random moves" is the standard construction and gives a clean escalation semantics.
- The scan discipline within VND also matters: sequential (restart at $M_1$ after every improvement, used below), pipe (stay in the improving neighborhood), and cyclic variants trade scan overhead against descent steepness. Mjirda et al. (2017), "Sequential variable neighborhood descent variants: an empirical study on the traveling salesman problem," compare these systematically; sequential with cheapest-first ordering is the robust default.

### When systematic neighborhood change beats a single neighborhood

- Different move types repair different defect classes. In routing, relocate fixes wrong customer-to-route assignment, while 2-opt fixes wrong sequencing within a route; no amount of 2-opt repairs an assignment defect.
- A VND local optimum is locally optimal for *all* listed neighborhoods simultaneously. The set of such points is much smaller, and empirically much better, than the set of single-neighborhood local optima.
- Escalating shake strength ($k = 1, 2, \dots, k_{\max}$) replaces the perturbation-strength tuning of ILS with a built-in adaptive scheme: the search applies the smallest perturbation that escapes the current basin.
- Do **not** reach for VNS when one neighborhood dominates and a single well-tuned kick suffices — that is ILS territory and the simpler code wins. For tightly constrained problems where most neighbors are infeasible, destroy-and-repair (large neighborhood search) is usually the better fit than any move-based VND.

### Complexity

One VND pass costs $O\!\left(\sum_{\ell} |M_\ell| \cdot c_\ell\right)$ where $c_\ell$ is the per-move delta-evaluation cost; with the usual $|M_\ell| = O(n^2)$ neighborhoods and $c_\ell = O(1)$ deltas, a descent step is $O(n^2)$ and a full descent is $O(n^2)$ times the number of improving steps. Shaking is $O(k)$. Memory is dominated by the $O(n^2)$ distance matrix. Beyond roughly $n = 1000$, restrict scans with candidate lists (k-nearest-neighbor moves only) or switch to VNDS.

## Generic Implementation

The skeleton below is the whole method. Everything problem-specific enters through three callables: `objective`, `shake`, and `local_search`.

```text
BVNS(x0, {N_1..N_kmax}, LocalSearch, budget)
  x <- LocalSearch(x0)
  repeat until budget exhausted:
    k <- 1
    while k <= kmax and budget remains:
      x'  <- Shake(x, k)            # RANDOM point of N_k(x)
      x'' <- LocalSearch(x')        # descend; plain LS -> BVNS, VND -> GVNS
      if f(x'') < f(x):             # NeighborhoodChange
        x <- x'';  k <- 1           # recenter on improvement, reset shake
      else:
        k <- k + 1                  # same center, stronger shake
  return x

VND(x, {M_1..M_lmax})               # deterministic multi-neighborhood descent
  l <- 1
  while l <= lmax:
    x' <- best improving neighbor in M_l(x)   (None if no improvement)
    if x' exists:  x <- x';  l <- 1
    else:          l <- l + 1
  return x                          # local optimum w.r.t. ALL M_l
```

VND first. Each descent neighborhood is a *step function*: it returns a strictly improving neighbor or `None`. This keeps the VND loop problem-agnostic and makes each neighborhood independently testable.

```python
from collections.abc import Callable, Sequence
from typing import TypeVar

S = TypeVar("S")


def vnd(solution: S, neighborhoods: Sequence[Callable[[S], S | None]]) -> S:
    """Sequential variable neighborhood descent.

    Each entry of `neighborhoods` is a best-improvement step function: it
    returns a strictly improving neighbor, or None when the solution is
    locally optimal for that neighborhood. The returned solution is locally
    optimal with respect to EVERY neighborhood in the list.
    """
    k = 0
    while k < len(neighborhoods):
        improved = neighborhoods[k](solution)
        if improved is None:
            k += 1        # locally optimal here -> try the next neighborhood
        else:
            solution = improved
            k = 0         # improvement found -> restart from the cheapest
    return solution
```

The outer VNS loop. Passing a plain single-neighborhood local search yields BVNS; passing `lambda x: vnd(x, descent_list)` yields GVNS — the loop itself does not change.

```python
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Generic, TypeVar

import numpy as np

S = TypeVar("S")


@dataclass
class VNSResult(Generic[S]):
    """Best solution found plus search statistics."""

    best: S
    best_obj: float
    shakes: int = 0
    improvements: int = 0
    history: list[float] = field(default_factory=list)


def basic_vns(
    initial: S,
    objective: Callable[[S], float],
    shake: Callable[[S, int, np.random.Generator], S],
    local_search: Callable[[S], S],
    k_max: int,
    max_shakes: int = 1_000,
    time_limit: float = 60.0,
    seed: int = 0,
) -> VNSResult:
    """Basic VNS (Mladenovic & Hansen 1997) for minimization.

    Pass a VND as `local_search` to obtain General VNS. `shake(x, k, rng)`
    must return a RANDOM point of N_k(x): sampling the best point of N_k(x)
    instead makes shaking deterministic and the search cycles.
    """
    rng = np.random.default_rng(seed)
    best = local_search(initial)
    best_obj = objective(best)
    res = VNSResult(best=best, best_obj=best_obj, history=[best_obj])
    start = time.perf_counter()

    def budget_left() -> bool:
        return res.shakes < max_shakes and time.perf_counter() - start < time_limit

    while budget_left():
        k = 1
        while k <= k_max and budget_left():
            trial = local_search(shake(best, k, rng))   # shake, then descend
            trial_obj = objective(trial)
            res.shakes += 1
            if trial_obj < best_obj - 1e-9:             # neighborhood change
                best, best_obj = trial, trial_obj
                res.improvements += 1
                res.history.append(best_obj)
                k = 1                                   # recenter, smallest shake
            else:
                k += 1                                  # same center, larger shake
    res.best, res.best_obj = best, best_obj
    return res
```

Two implementation details carry most of the practical weight. First, the improvement test uses a tolerance (`1e-9`) — with float objectives, accepting ties reintroduces cycling. Second, the budget check sits in *both* loops, so a long VND cannot overshoot the time limit by a full $k$-cycle.

### Parameter guidance

| Parameter | Typical range | What it trades off |
|---|---|---|
| `k_max` (shake levels) | 3–10 generally; ≤ `p` for p-median; ≤ n/5 for routing | higher gives stronger escapes per cycle but wastes descents far from good basins |
| shake strength at level k | k elementary random moves; or nested $N_k \subset N_{k+1}$ | too weak: descent undoes the shake; too strong: degenerates into random restart |
| VND ordering | cheapest scan first | a wrong order burns expensive scans on defects a cheap move would fix |
| improvement rule | best-improvement up to ~10^4 moves/scan; first-improvement beyond | best = steeper descent, fewer steps; first = cheaper steps, more of them |
| acceptance | improving-only (BVNS/GVNS); skewed with $\alpha$ ≈ 0.01–0.1 of typical $f$ per unit distance | improving-only intensifies; skewed crosses wide valleys but needs a solution-distance function |
| stopping | wall clock; or shake budget; or 5–20 full k-cycles without improvement | wall clock is fair across methods; shake budget is exactly reproducible |
| restarts | none by default; new construction after 3–5 fruitless full cycles | helps when good local optima cluster in separate regions of $S$ |

Shake and descent operators themselves (segment relocations, double bridge, k-exchange) are cataloged in **mutation-and-perturbation-operators** and **local-search-and-neighborhoods**; this skill treats them as plug-ins.

## Worked Application 1: p-Median with Basic VNS

The p-median problem: given a set $V$ of $n$ sites with distances $d_{ij}$, open a subset $M \subseteq V$ with $|M| = p$ minimizing total client-to-nearest-median distance

$$
\min_{|M| = p} \; \sum_{i \in V} \min_{j \in M} d_{ij}.
$$

This was the first large-scale VNS application (Hansen & Mladenović 1997, "Variable neighborhood search for the p-median"). The natural design: descent in the 1-interchange neighborhood (swap one open median for one closed site), shaking in the k-interchange neighborhoods — perfectly nested, so $k$ directly measures perturbation strength. For exact formulations and Lagrangian bounds on this problem, see **facility-location-problem**.

```python
import numpy as np


def euclidean_pmedian_instance(n: int, seed: int = 0) -> np.ndarray:
    """n random points in [0,100]^2; every point is both client and site.

    Returns the n-by-n Euclidean distance matrix.
    """
    rng = np.random.default_rng(seed)
    pts = rng.uniform(0.0, 100.0, size=(n, 2))
    diff = pts[:, None, :] - pts[None, :, :]
    return np.sqrt((diff ** 2).sum(axis=2))


def pmedian_cost(dist: np.ndarray, medians: np.ndarray) -> float:
    """Sum over clients of the distance to the closest open median."""
    return float(dist[:, medians].min(axis=1).sum())
```

The local search is a best-improvement 1-interchange, fully vectorized over all (insert, drop) pairs using the closest/second-closest decomposition of Whitaker (1983), "A fast algorithm for the greedy interchange for large-scale clustering and median location problems" (see also Resende & Werneck 2007, "A fast swap-based local search procedure for location problems"). For a swap that inserts site $f$ and drops median $m$, each client $i$ contributes

$$
\Delta_i(f, m) =
\begin{cases}
\min(d_{1i}, d_{if}) - d_{1i} & \text{if } m \text{ is not } i\text{'s closest median},\\
\min(d_{2i}, d_{if}) - d_{1i} & \text{if } m \text{ is } i\text{'s closest median},
\end{cases}
$$

where $d_{1i}, d_{2i}$ are the distances to $i$'s closest and second-closest open medians. Splitting the second case into the first case plus a correction term lets numpy build the entire $(p \times (n-p))$ delta matrix with one matrix product.

```python
import numpy as np


def best_interchange(
    dist: np.ndarray, medians: np.ndarray
) -> tuple[np.ndarray, float] | None:
    """Best-improvement 1-interchange step, fully vectorized (requires p >= 2).

    Builds the complete (drop m, insert f) delta matrix from the closest /
    second-closest decomposition. Returns (new_medians, delta), or None when
    no swap improves.
    """
    n, p = dist.shape[0], len(medians)
    med_dist = dist[:, medians]                       # (n, p)
    order = np.argsort(med_dist, axis=1)
    rows = np.arange(n)
    d1 = med_dist[rows, order[:, 0]]                  # closest open median
    d2 = med_dist[rows, order[:, 1]]                  # second closest
    closest_pos = order[:, 0]                         # column index in `medians`

    out = np.setdiff1d(np.arange(n), medians)         # closed sites, (c,)
    cand = dist[:, out]                               # (n, c)

    # Gain of inserting f (no drop yet): clients move to f when it is closer.
    gain = np.minimum(cand, d1[:, None]) - d1[:, None]            # (n, c) <= 0
    total_gain = gain.sum(axis=0)                                 # (c,)

    # Correction when the dropped median was client i's closest:
    # i is re-served at min(d2_i, d_if) instead of min(d1_i, d_if).
    corr = np.minimum(cand, d2[:, None]) - np.minimum(cand, d1[:, None])
    onehot = np.zeros((n, p))
    onehot[rows, closest_pos] = 1.0
    loss = onehot.T @ corr                                        # (p, c)

    delta = total_gain[None, :] + loss                            # (p, c)
    m_pos, f_pos = np.unravel_index(np.argmin(delta), delta.shape)
    if delta[m_pos, f_pos] >= -1e-9:
        return None
    new_medians = medians.copy()
    new_medians[m_pos] = out[f_pos]
    return new_medians, float(delta[m_pos, f_pos])


def interchange_descent(dist: np.ndarray, medians: np.ndarray) -> np.ndarray:
    """Repeat best-improvement swaps until 1-interchange locally optimal."""
    while (step := best_interchange(dist, medians)) is not None:
        medians = step[0]
    return medians
```

Shaking replaces $k$ random open medians with $k$ random closed sites — a uniform random point of the k-interchange neighborhood, exactly as the skeleton requires.

```python
import numpy as np


def pmedian_shake(
    dist: np.ndarray, medians: np.ndarray, k: int, rng: np.random.Generator
) -> np.ndarray:
    """N_k shake: swap k random open medians for k random closed sites."""
    out = np.setdiff1d(np.arange(dist.shape[0]), medians)
    new = medians.copy()
    drop = rng.choice(len(medians), size=k, replace=False)
    new[drop] = rng.choice(out, size=k, replace=False)
    return new


def pmedian_vns(
    dist: np.ndarray, p: int, k_max: int, max_shakes: int = 400, seed: int = 0
) -> VNSResult:
    """Basic VNS for p-median: random start, interchange descent, k-swap shake."""
    rng = np.random.default_rng(seed)
    start = rng.choice(dist.shape[0], size=p, replace=False)
    return basic_vns(
        initial=start,
        objective=lambda m: pmedian_cost(dist, m),
        shake=lambda m, k, g: pmedian_shake(dist, m, k, g),
        local_search=lambda m: interchange_descent(dist, m),
        k_max=min(k_max, p),
        max_shakes=max_shakes,
        time_limit=30.0,
        seed=seed,
    )


dist = euclidean_pmedian_instance(n=80, seed=42)
res = pmedian_vns(dist, p=6, k_max=4, max_shakes=400, seed=1)
print(sorted(res.best.tolist()), round(res.best_obj, 1))
# Expected: prints "[4, 10, 47, 55, 58, 65] 1057.5". Seeds 1-5 all reach this
# same set, and an exact MIP confirms 1057.5 is the optimum of this instance.
# Runs in well under one second (400 shakes, vectorized descent).
```

Note the division of labor: `basic_vns` is reused verbatim from the generic section; only ~60 problem-specific lines (objective, descent step, shake) were added. That ratio is the hallmark of a clean VNS implementation.

## Worked Application 2: Capacitated VRP with General VNS

CVRP: serve customers $1..n$ from depot $0$ with vehicles of capacity $Q$; each customer $i$ has demand $q_i$ and must be visited exactly once; minimize total travel distance over all routes, where each route starts and ends at the depot and its total demand respects $\sum_{i \in r} q_i \le Q$. The CVRP is the canonical GVNS showcase because it naturally offers several complementary neighborhoods (Kytöjoki et al. 2007, "An efficient variable neighborhood search heuristic for very large scale vehicle routing problems"). For the full problem family — time windows, heterogeneous fleets, ALNS, OR-Tools — see **vehicle-routing-problem**.

Solution representation: a list of routes, each a list of customer indices (depot implicit). The instance generator, evaluator, independent feasibility checker, and a capacity-aware nearest-neighbor construction:

```python
import numpy as np


def cvrp_instance(
    n_customers: int, capacity: int, seed: int = 0
) -> tuple[np.ndarray, np.ndarray, int]:
    """Random Euclidean CVRP; node 0 is the depot at the center.

    Returns (distance matrix, integer demands with demand[0] = 0, capacity).
    """
    rng = np.random.default_rng(seed)
    pts = rng.uniform(0.0, 100.0, size=(n_customers + 1, 2))
    pts[0] = (50.0, 50.0)
    diff = pts[:, None, :] - pts[None, :, :]
    dist = np.sqrt((diff ** 2).sum(axis=2))
    demand = np.zeros(n_customers + 1, dtype=np.int64)
    demand[1:] = rng.integers(1, 10, size=n_customers, endpoint=True)
    return dist, demand, capacity


def route_cost(route: list[int], dist: np.ndarray) -> float:
    """Cost of depot -> route -> depot; an empty route costs 0."""
    if not route:
        return 0.0
    idx = np.array([0, *route, 0])
    return float(dist[idx[:-1], idx[1:]].sum())


def total_cost(routes: list[list[int]], dist: np.ndarray) -> float:
    """Total distance over all routes."""
    return sum(route_cost(r, dist) for r in routes)


def check_cvrp(routes: list[list[int]], demand: np.ndarray, capacity: int) -> None:
    """Independent feasibility check: visit-once and capacity."""
    visited = sorted(c for r in routes for c in r)
    assert visited == list(range(1, len(demand))), "each customer exactly once"
    assert all(int(demand[r].sum()) <= capacity for r in routes if r), "capacity"


def greedy_start(
    dist: np.ndarray, demand: np.ndarray, capacity: int
) -> list[list[int]]:
    """Capacity-aware nearest-neighbor construction."""
    unvisited = set(range(1, len(demand)))
    routes: list[list[int]] = []
    while unvisited:
        route: list[int] = []
        load, cur = 0, 0
        while True:
            feasible = [c for c in unvisited if load + demand[c] <= capacity]
            if not feasible:
                break
            nxt = min(feasible, key=lambda c: dist[cur, c])
            route.append(nxt)
            unvisited.discard(nxt)
            load += int(demand[nxt])
            cur = nxt
        routes.append(route)
    return routes
```

Three descent neighborhoods, each written as a best-improvement step function compatible with the generic `vnd`. All three use O(1) edge-based delta evaluation. Ordering follows the cheapest-first rule: relocate (assignment defects, also the cheapest scan), then inter-route swap, then intra-route 2-opt (sequencing defects).

```python
import numpy as np


def best_relocate(
    routes: list[list[int]], dist: np.ndarray, demand: np.ndarray, capacity: int
) -> list[list[int]] | None:
    """Best-improvement relocate: move one customer to any other position."""
    loads = [int(demand[r].sum()) for r in routes]
    best_delta, best_move = -1e-9, None
    for r1, route1 in enumerate(routes):
        for i, c in enumerate(route1):
            prev1 = route1[i - 1] if i > 0 else 0
            next1 = route1[i + 1] if i + 1 < len(route1) else 0
            remove = dist[prev1, next1] - dist[prev1, c] - dist[c, next1]
            for r2, route2 in enumerate(routes):
                if r2 != r1 and loads[r2] + demand[c] > capacity:
                    continue
                for j in range(len(route2) + 1):
                    if r2 == r1 and j in (i, i + 1):
                        continue          # no-op positions
                    a = route2[j - 1] if j > 0 else 0
                    b = route2[j] if j < len(route2) else 0
                    delta = remove + dist[a, c] + dist[c, b] - dist[a, b]
                    if delta < best_delta:
                        best_delta, best_move = delta, (r1, i, r2, j)
    if best_move is None:
        return None
    r1, i, r2, j = best_move
    new = [r[:] for r in routes]
    c = new[r1].pop(i)
    if r1 == r2 and j > i:
        j -= 1
    new[r2].insert(j, c)
    return new


def best_swap(
    routes: list[list[int]], dist: np.ndarray, demand: np.ndarray, capacity: int
) -> list[list[int]] | None:
    """Best-improvement inter-route swap of two customers."""
    loads = [int(demand[r].sum()) for r in routes]
    best_delta, best_move = -1e-9, None
    for r1 in range(len(routes)):
        for r2 in range(r1 + 1, len(routes)):
            for i, c1 in enumerate(routes[r1]):
                for j, c2 in enumerate(routes[r2]):
                    if loads[r1] - demand[c1] + demand[c2] > capacity:
                        continue
                    if loads[r2] - demand[c2] + demand[c1] > capacity:
                        continue
                    p1 = routes[r1][i - 1] if i > 0 else 0
                    n1 = routes[r1][i + 1] if i + 1 < len(routes[r1]) else 0
                    p2 = routes[r2][j - 1] if j > 0 else 0
                    n2 = routes[r2][j + 1] if j + 1 < len(routes[r2]) else 0
                    delta = (
                        dist[p1, c2] + dist[c2, n1] - dist[p1, c1] - dist[c1, n1]
                        + dist[p2, c1] + dist[c1, n2] - dist[p2, c2] - dist[c2, n2]
                    )
                    if delta < best_delta:
                        best_delta, best_move = delta, (r1, i, r2, j)
    if best_move is None:
        return None
    r1, i, r2, j = best_move
    new = [r[:] for r in routes]
    new[r1][i], new[r2][j] = new[r2][j], new[r1][i]
    return new


def best_two_opt(
    routes: list[list[int]], dist: np.ndarray
) -> list[list[int]] | None:
    """Best-improvement intra-route 2-opt (segment reversal)."""
    best_delta, best_move = -1e-9, None
    for r, route in enumerate(routes):
        path = [0, *route, 0]
        for i in range(len(path) - 2):
            for j in range(i + 2, len(path) - 1):
                delta = (
                    dist[path[i], path[j]] + dist[path[i + 1], path[j + 1]]
                    - dist[path[i], path[i + 1]] - dist[path[j], path[j + 1]]
                )
                if delta < best_delta:
                    best_delta, best_move = delta, (r, i, j)
    if best_move is None:
        return None
    r, i, j = best_move
    new = [rt[:] for rt in routes]
    new[r][i:j] = reversed(new[r][i:j])   # path slots i+1..j = route slots i..j-1
    return new
```

Wiring it together: VND over the three neighborhoods as local search, shaking by $k$ random feasible relocations (ejection plus capacity-checked reinsertion). One spare empty route is appended to the start solution so relocate can open a new route when that pays off.

```python
import numpy as np


def cvrp_vnd(
    routes: list[list[int]], dist: np.ndarray, demand: np.ndarray, capacity: int
) -> list[list[int]]:
    """VND over relocate -> inter-route swap -> intra-route 2-opt."""
    return vnd(
        routes,
        [
            lambda s: best_relocate(s, dist, demand, capacity),
            lambda s: best_swap(s, dist, demand, capacity),
            lambda s: best_two_opt(s, dist),
        ],
    )


def cvrp_shake(
    routes: list[list[int]],
    k: int,
    rng: np.random.Generator,
    demand: np.ndarray,
    capacity: int,
) -> list[list[int]]:
    """N_k shake: k random relocations to random capacity-feasible positions."""
    new = [r[:] for r in routes]
    for _ in range(k):
        nonempty = [i for i, r in enumerate(new) if r]
        r1 = int(rng.choice(nonempty))
        c = new[r1].pop(int(rng.integers(len(new[r1]))))
        feasible = [
            i for i, r in enumerate(new)
            if int(demand[r].sum()) + int(demand[c]) <= capacity
        ]
        r2 = int(rng.choice(feasible))   # r1 is always feasible again
        new[r2].insert(int(rng.integers(len(new[r2]) + 1)), c)
    return new


dist, demand, capacity = cvrp_instance(n_customers=25, capacity=40, seed=7)
start = greedy_start(dist, demand, capacity) + [[]]   # spare empty route
res = basic_vns(
    initial=start,
    objective=lambda s: total_cost(s, dist),
    shake=lambda s, k, g: cvrp_shake(s, k, g, demand, capacity),
    local_search=lambda s: cvrp_vnd(s, dist, demand, capacity),
    k_max=5,
    max_shakes=100,
    time_limit=120.0,
    seed=3,
)
final = [r for r in res.best if r]
check_cvrp(final, demand, capacity)
print(len(final), round(total_cost(start, dist), 1), round(res.best_obj, 1))
# Expected: prints "4 913.9 612.7" — 4 routes, greedy start 913.9 improved
# to 612.7 (about 33%); the feasibility check passes. Deterministic for the
# given seeds because stopping is by shake budget; runs in under a second.
```

The same GVNS becomes a different algorithm by editing only the descent list — add Or-opt or cross-exchange step functions and `cvrp_vnd` picks them up. That modularity, not any single neighborhood, is the reason to structure VRP heuristics this way.

## Advanced Techniques

### Skewed VNS

When good local optima sit in distant valleys, improving-only acceptance keeps the search trapped near the incumbent: every shake either falls back or lands in a worse valley and is rejected. SVNS (Hansen & Mladenović 2001, "Variable neighborhood search: principles and applications") accepts a slightly worse $x''$ when it is *far* from the incumbent, using a solution-distance function $\rho$:

```python
import time
from collections.abc import Callable
from typing import TypeVar

import numpy as np

S = TypeVar("S")


def skewed_vns(
    initial: S,
    objective: Callable[[S], float],
    shake: Callable[[S, int, np.random.Generator], S],
    local_search: Callable[[S], S],
    distance: Callable[[S, S], float],
    alpha: float,
    k_max: int,
    max_shakes: int = 1_000,
    time_limit: float = 60.0,
    seed: int = 0,
) -> tuple[S, float]:
    """Skewed VNS: recenter when f(x'') - alpha * rho(x, x'') < f(x).

    The search center may drift to non-improving solutions; the best solution
    is tracked separately and returned.
    """
    rng = np.random.default_rng(seed)
    cur = local_search(initial)
    cur_obj = objective(cur)
    best, best_obj = cur, cur_obj
    shakes = 0
    start = time.perf_counter()
    while shakes < max_shakes and time.perf_counter() - start < time_limit:
        k = 1
        while k <= k_max and shakes < max_shakes:
            trial = local_search(shake(cur, k, rng))
            trial_obj = objective(trial)
            shakes += 1
            if trial_obj < best_obj:
                best, best_obj = trial, trial_obj
            if trial_obj - alpha * distance(cur, trial) < cur_obj:
                cur, cur_obj = trial, trial_obj   # skewed neighborhood change
                k = 1
            else:
                k += 1
    return best, best_obj


def median_set_distance(a: np.ndarray, b: np.ndarray) -> float:
    """p-median solution distance: number of medians not shared."""
    return float(np.setdiff1d(a, b).size)
```

Calibrate $\alpha$ so that $\alpha \cdot \rho$ for a typical shake distance is 1–10% of the objective; $\alpha = 0$ recovers BVNS, large $\alpha$ degenerates into a random walk. Distances must be cheap: symmetric difference for subsets, number of differing edges for tours, Hamming distance for assignments.

### Reduced VNS

RVNS drops the local search entirely: shake, evaluate, neighborhood-change. It is the right regime when single evaluations are cheap but any descent scan is prohibitive (millions of elements), and it doubles as a cheap diagnostic — if RVNS already matches your BVNS, the local search is adding nothing and its neighborhoods need rethinking.

### Variable Neighborhood Decomposition Search

VNDS (Hansen, Mladenović & Perez-Brito 2001, "Variable neighborhood decomposition search") shakes by selecting a size-$k$ subproblem — e.g., $k$ customers and their routes, or $k$ medians and their allocated clients — and runs the full VNS only on that subproblem with the remainder frozen. The neighborhood-change step then operates on subproblem size $k$. This is the VNS-native version of fix-and-optimize and the standard route once instances outgrow whole-solution descents.

### Adaptive neighborhood ordering

Track, per descent neighborhood, the count of scans and improvements; periodically reorder the VND list by empirical improvement rate divided by scan cost. Keep the reorder period long (hundreds of descents) — orderings measured on a handful of scans are noise. The same statistics tell you when a neighborhood earns its place at all: a neighborhood that improves in under 1% of scans and costs 50% of descent time should be dropped or demoted to a periodic deep-clean role.

### Hybridization with exact methods

VNS combines naturally with MIP machinery: use a solver to optimize the subproblems of VNDS, or define shaking in the space of MIP solutions by bounding the Hamming distance to the incumbent — VNS branching (Hansen, Mladenović & Urošević 2006, "Variable neighborhood search and local branching"). The neighborhood-change logic is unchanged; only the descent step becomes a budgeted solver call. Budget each call strictly (node or time limits), since one runaway subproblem can consume the entire heuristic budget.

## Practical Challenges

**Shaking keeps falling back into the same local optimum.** The shake at level $k$ is too weak relative to the basin of attraction, so the descent undoes it. Increase the per-level strength (apply $2k$ elementary moves at level $k$), use a *different* move type for shaking than for descent (segment relocations against an edge-based descent), or grow $k$ in larger steps. Diagnose by logging the fraction of shakes that return exactly the previous solution; above ~50% at $k = 1$ is normal, above ~50% at $k = k_{\max}$ means the whole shake ladder is too weak.

**GVNS spends almost all its time inside the first VND call.** The construction is far from local optimality, so the first descent does the work of a full local-search run. That is expected; if it dominates the budget, run the cheapest neighborhood alone to local optimality before entering the full VND, or use a stronger construction so descents start closer.

**VND oscillates between two neighborhoods without terminating.** Equal-cost moves are being accepted somewhere. Enforce strict improvement with an explicit tolerance everywhere (`delta < -1e-9`); with integer objectives use `delta < 0`. Cycling is impossible under strict improvement because the objective strictly decreases at every accepted move.

**The search stalls after exhausting $k = 1 \dots k_{\max}$ with no improvement.** By design the outer loop restarts at $k = 1$ and tries a fresh random shake; randomness alone often breaks the stall. If whole cycles repeatedly pass without improvement, stop (the cheap option), switch acceptance to skewed, or restart from a new construction while keeping the global best.

**Most shaken solutions are infeasible under hard constraints.** Build feasibility into the shake (the CVRP shake above only inserts where capacity allows) instead of penalizing violations: the neighborhood-change comparison silently assumes both solutions are feasible, and penalty mistuning corrupts it. If feasible-by-construction is impossible, add a repair step between shake and descent.

**Unclear whether to use ILS or VNS.** They share a skeleton; BVNS is essentially ILS with an escalating perturbation and improving-only acceptance. If you already know a good fixed perturbation strength, ILS is the simpler, equally strong choice — see **iterated-local-search**. If perturbation strength is unknown or instance-dependent, the $k$-escalation of VNS removes that tuning dimension.

**Runtime explodes with instance size because every scan is $O(n^2)$.** Restrict moves to candidate lists (each customer's 10–20 nearest neighbors), add don't-look bits, and cache route loads incrementally instead of recomputing — the standard arsenal in **local-search-and-neighborhoods**. Past the point where even restricted descents are too slow, switch to VNDS subproblems.

**Results are not reproducible between runs.** Wall-clock stopping plus a shared `rng` makes every run unique. For experiments, stop on a shake budget (as both demos do), pass explicit seeds, and report the wall-clock time separately; for deployment, wall-clock stopping is fine.

## Tools & Libraries

| Library / tool | When to use | Note |
|---|---|---|
| numpy | always — distance matrices, vectorized delta scans, shaking | use `np.random.default_rng(seed)` for all randomness |
| numba | pure-Python descent loops become the bottleneck | `@njit` the move scans; keep solutions as arrays, not lists of lists |
| scipy.spatial | building distance structures and candidate lists | `cKDTree` k-nearest queries restrict $O(n^2)$ scans to $O(n \cdot k)$ |
| OR-Tools routing | independent VRP baseline to compare against | its guided local search gives a strong reference cost in minutes |
| gurobipy / HiGHS | exact reference on small instances; VNDS subproblem solver | confirm VNS reaches optimality where the MIP is tractable |
| pandas | experiment result tables | one row per (instance, seed, configuration) run |
| matplotlib | convergence plots from `VNSResult.history` | best-so-far curves with a band over seeds |

There is no dominant off-the-shelf VNS library in Python; the method is ~60 lines (above) and the value is in problem-specific neighborhoods, so implementing it directly is the norm in both research and practice.

## Output Format

A complete VNS deliverable contains five parts.

**1. Algorithm card** — one table that fully specifies the configuration:

| Item | Example entry |
|---|---|
| Variant | GVNS |
| Descent neighborhoods (VND order) | relocate → inter-route swap → intra-route 2-opt |
| Improvement rule | best improvement, tolerance 1e-9 |
| Shake | k random capacity-feasible relocations, k = 1..5 |
| Acceptance | improving only |
| Stopping | 100 shakes (reproducible) or 120 s, whichever first |
| Construction | capacity-aware nearest neighbor + one empty route |
| Seeds | 10 seeds, reported individually |

**2. Per-run results table** — one row per instance × seed:

```text
instance      seed  initial    final     gap%   shakes  improv  t_best  t_total
cvrp-n25-s7      3    913.9    612.7     0.02     100       2    0.1s    0.2s
cvrp-n25-s7      4    913.9    612.6     0.00     100       3    0.1s    0.2s
```

where `gap%` is measured against the best known value or an exact bound, `t_best` is time-to-best, and `improv` counts accepted neighborhood changes.

**3. Aggregate statistics** per instance: best, mean, standard deviation over seeds, and the success rate of reaching the target value. Single-seed results are anecdotes, not evidence.

**4. Validation statement** — output of an independent feasibility checker plus objective recomputation (like `check_cvrp` and `total_cost` above) executed on the final solutions, stated explicitly: "all 10 final solutions pass visit-once and capacity checks; recomputed objectives match reported values."

**5. Convergence evidence** — `VNSResult.history` per run, plotted as best-so-far curves or tabulated at checkpoints, so reviewers can see whether the budget was binding or the search had flattened.

## Questions to Ask

- What is the problem class, the representation, and the instance size range?
- Which move types are available, and does each have O(1) or O(n) delta evaluation?
- Are there at least two genuinely different neighborhoods, or would ILS be simpler?
- Which constraints are hard, and can shaking stay feasible by construction?
- What is the time budget per run, and how many runs does the experiment need?
- Is reproducibility required (seeded, budget-stopped) or is wall-clock stopping acceptable?
- Are best-known solutions or exact bounds available for gap reporting?
- Is the deliverable one good solution, or a statistical comparison against a baseline?

## Related Skills

- **local-search-and-neighborhoods** — when the work is designing the individual moves, delta evaluation, and scan order that VND and VNS consume as building blocks.
- **iterated-local-search** — when one neighborhood plus a tuned perturbation suffices; the simpler baseline every VNS must beat under equal budget.
- **facility-location-problem** — when the p-median application needs exact formulations, Lagrangian bounds, or alternative heuristics beyond the VNS shown here.
- **vehicle-routing-problem** — when the CVRP application needs full variant coverage (time windows, fleets), ALNS, or OR-Tools routing baselines.
