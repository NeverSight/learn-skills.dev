---
name: local-search-and-neighborhoods
description: When the user wants to design or implement neighborhood-based local search - choosing moves (swap, insertion, 2-opt, Or-opt, exchange), writing O(1)/O(n) delta evaluation, first vs best improvement, scan order, and move data structures. Also use when the user mentions "local search," "2-opt," "neighborhood," "delta evaluation," "hill climbing," "first improvement," or when a heuristic recomputes the full objective after every move. For accepting worsening moves to escape local optima, see simulated-annealing; for perturbation-and-restart wrappers, see iterated-local-search.
---

# Local Search and Neighborhoods

You are an expert in neighborhood-based search for combinatorial optimization. This skill
covers neighborhood design (swap, insertion, 2-opt, Or-opt, exchange), constant- and
linear-time delta evaluation, first- vs best-improvement pivoting, neighborhood scanning
order, move data structures, and the limits of plain hill climbing. Use the framework below
to build descent engines that are correct (deltas audited against full recomputation) and
fast (no full objective evaluation inside the move loop), and that drop in unchanged as the
inner loop of simulated annealing, tabu search, and iterated local search.

## Initial Assessment

Establish these facts before proposing a neighborhood or writing any move code:

- **Representation.** Permutation (tour, schedule), binary vector (selection), integer
  assignment array, or partition into sets (routes, machine loads)? The move catalog and
  the delta formulas depend entirely on this. See **solution-encodings**-style criteria:
  every move must map feasible representations to feasible representations, or you must
  plan a penalty scheme.
- **Objective structure.** Additive over solution elements (sum of edge lengths, sum of
  assignment costs, linear penalties)? Additive objectives almost always admit O(1) or
  O(n) deltas. Max-type / critical-path objectives (flow-shop or job-shop makespan) do
  not; plan for an acceleration scheme (Taillard heads/tails, critical-path filtering)
  instead of a true delta.
- **Hard vs soft constraints.** Decide per constraint: keep moves feasibility-preserving,
  or relax the constraint into the objective and evaluate the penalty change inside the
  delta. Mixing the two without a plan is the most common source of wrong deltas.
- **Instance size.** n ≤ 500: any O(n²) neighborhood with full sweeps is fine in plain
  Python. n in 10³–10⁴: you need candidate lists, don't-look bits, or vectorized move
  scoring. n above 10⁴: you also need O(1) position queries and careful apply costs
  (segment reversal is O(n) per move).
- **Evaluation cost.** Time one full objective evaluation and one delta evaluation early.
  If the delta is not at least ~n times cheaper than the full evaluation, the neighborhood
  implementation is wrong or the objective does not decompose.
- **Role of the local search.** Standalone descent, multistart, or inner loop of a
  metaheuristic? The wrapper changes the acceptance logic; the move/delta code should not
  change at all. Keep them in separate functions from day one.
- **Quality target.** 2-opt local optima on random Euclidean TSP sit roughly 5% above
  optimal from good starts (Johnson & McGeoch 1997, "The traveling salesman problem: a
  case study in local optimization"). If the target is tighter, plan a metaheuristic
  wrapper or a richer neighborhood, not more sweeps.
- **Data format.** Full distance matrix (O(n²) memory) vs coordinates plus k-nearest
  neighbors via a KD-tree? At n = 20,000, a float64 matrix is 3.2 GB — candidate lists are
  not optional there.
- **Determinism.** Seed every random scan order and tie-break (`np.random.default_rng`)
  so descents are reproducible run to run.
- **Validation plan.** An independent objective recompute and a delta audit (compare each
  claimed delta against a from-scratch evaluation on random moves) must exist before any
  performance tuning.

## Neighborhood Anatomy

A neighborhood is a function $N: S \to 2^S$ mapping each solution to the set of solutions
reachable by one move. Local search descends until it reaches a local optimum:

$$
s^\* \text{ is a local optimum of } f \text{ w.r.t. } N
\iff f(s^\*) \le f(s) \quad \forall s \in N(s^\*).
$$

A move $m$ applied to $s$ is written $s \oplus m$, and the entire craft of fast local
search is computing the delta

$$
\Delta(s, m) = f(s \oplus m) - f(s)
$$

without ever computing $f(s \oplus m)$ from scratch. Local optimality is always *relative
to N*: a 2-opt optimum is usually not an Or-opt optimum, which is the basis of compound
neighborhoods and variable neighborhood descent.

### Move catalog

| Move | Acts on | Neighborhood size | Delta cost | Notes |
|---|---|---|---|---|
| Swap (exchange two elements) | permutation, assignment array | n(n−1)/2 | O(1) for additive costs; O(n) for QAP | Weak on tours (touches 4 edges but rarely improving); strong on assignments |
| Insertion (shift one element) | permutation | (n−1)² | O(1) additive; O(nm) per job in flow shop via Taillard | The dominant scheduling neighborhood |
| 2-opt (reverse a segment) | tours | n(n−1)/2 | O(1) symmetric distances; **no O(1) delta if asymmetric** | Apply costs O(n) (reversal); Croes (1958) |
| Or-opt (relocate segment of 1–3) | tours | ≈ 3n² | O(1) | Orientation-preserving, so valid for asymmetric instances; Or (1976) |
| k-flip | binary vectors | C(n,k) | O(degree) per flip | Knapsack, max-cut, SAT-style problems |
| Inter-set exchange / relocate | partitions, routes | O(n²) | O(1)–O(route length) | CVRP inter-route moves; feasibility (load, time) checked in the delta |

### Delta evaluation

For the symmetric TSP, reversing positions $i{+}1 \dots j$ of tour $\pi$ removes two edges
and adds two edges; every interior edge keeps its (symmetric) length:

$$
\Delta_{\text{2opt}}(i, j) =
d_{\pi_i \pi_j} + d_{\pi_{i+1} \pi_{j+1}} - d_{\pi_i \pi_{i+1}} - d_{\pi_j \pi_{j+1}}.
$$

This O(1) formula is why 2-opt scans millions of moves per second. On *asymmetric*
instances the reversed segment changes direction, so the formula is invalid — use
orientation-preserving moves (Or-opt, 3-opt segment reinsertion) instead. The same
discipline applies everywhere: write the delta as (cost of edges/terms created) − (cost of
edges/terms destroyed), and prove to yourself that nothing else changes.

### First vs best improvement

- **Best improvement** scans the whole neighborhood, applies the steepest move. Fewer,
  larger steps; deterministic given the scan; pairs naturally with vectorized scoring of
  all moves at once.
- **First improvement** applies the first improving move found. Much cheaper sweeps early
  in the descent when improving moves are dense; final quality is usually on par with best
  improvement, sometimes better, especially from random starts (Hansen & Mladenović 2006,
  "First vs. best improvement: an empirical study").
- Practical default: first improvement with a *randomized scan order per sweep* (removes
  lexicographic bias), switching to best improvement only when moves are scored in bulk
  with numpy.
- The termination certificate is one full improving-move-free sweep. That last sweep costs
  |N| delta evaluations no matter what — pruning rules and candidate lists are the only
  way to shrink it.

### Scanning order and move data structures

Scan order matters because first improvement commits to whatever it sees first.
Lexicographic order biases the search toward low indices; a seeded random permutation per
sweep is the cheap fix. Queue-driven orders (re-examine elements whose surroundings just
changed) are the systematic version and lead directly to don't-look bits (Bentley 1992,
"Fast algorithms for geometric traveling salesman problems").

Keep these structures current under every apply:

- `pos` array with `pos[element] = position`, the inverse of the permutation — O(1) move
  legality and delta lookups, updated in O(segment) on reversal.
- Cached per-element quantities used by deltas (route load, completion times, gains), each
  with an O(1)/O(k) incremental update rule.
- For very large tours, array reversal is the bottleneck; doubly linked or two-level
  list representations bound the apply cost (Fredman, Johnson, McGeoch & Ostheimer 1995,
  "Data structures for traveling salesmen").

### Hill climbing and its limits

Plain hill climbing terminates at the first local optimum of $N$ — typically in O(n) to
O(n log n) accepted moves empirically, and there it stops. Larger neighborhoods give
better local optima at higher sweep cost; no fixed polynomial neighborhood removes local
optima for NP-hard problems. Escaping is the wrapper's job: probabilistic acceptance
(simulated annealing), memory (tabu search), perturbation and restarts (iterated local
search). Build the descent so those wrappers reuse the identical move and delta code.

## Generic Descent Engine

The reusable skeleton, independent of problem and move type:

```text
LOCAL-SEARCH(s, N, rule):
    f_s <- f(s)                                   # one full evaluation, ever
    repeat:
        scan (m, delta(s, m)) for m in N(s)       # deltas only, never full f
        if rule = BEST:   m* <- move with minimum delta
        if rule = FIRST:  m* <- first move with delta < -tol in scan order
        if no move has delta < -tol:
            return s                              # local optimum w.r.t. N
        s   <- s (+) m*                           # apply in place
        f_s <- f_s + delta(s, m*)                 # bookkeeping, audit periodically
    until move/time budget exhausted
```

The engine below realizes this with two problem-specific callbacks: a move enumerator that
yields `(move, delta)` pairs for the current solution, and an in-place apply. The demo is
weighted max-cut with a 1-flip neighborhood and an O(n) delta per vertex.

```python
import numpy as np
from collections.abc import Callable, Iterable
from typing import Any

Move = Any


def local_search(
    objective: float,
    enumerate_moves: Callable[[], Iterable[tuple[Move, float]]],
    apply_move: Callable[[Move], None],
    improvement: str = "best",
    tol: float = 1e-9,
    max_moves: int = 1_000_000,
) -> tuple[float, dict[str, int]]:
    """Generic descent. enumerate_moves() yields (move, delta) pairs for the
    CURRENT solution; apply_move mutates the solution in place."""
    stats = {"sweeps": 0, "moves": 0, "delta_evals": 0}
    while stats["moves"] < max_moves:
        stats["sweeps"] += 1
        best_move, best_delta = None, -tol
        for move, delta in enumerate_moves():
            stats["delta_evals"] += 1
            if delta < best_delta:
                best_move, best_delta = move, delta
                if improvement == "first":
                    break
        if best_move is None:
            break                                  # local optimum reached
        apply_move(best_move)
        objective += best_delta
        stats["moves"] += 1
    return objective, stats


def weighted_maxcut_demo(n: int = 40, seed: int = 0) -> None:
    """Hill climbing for weighted max-cut: flip one vertex side, O(n) delta."""
    rng = np.random.default_rng(seed)
    w = rng.uniform(0.0, 1.0, (n, n))
    w = np.triu(w, 1) + np.triu(w, 1).T            # symmetric, zero diagonal
    side = rng.integers(0, 2, n)

    def cut_value(s: np.ndarray) -> float:
        return float(w[s[:, None] != s[None, :]].sum() / 2.0)

    def enumerate_moves() -> Iterable[tuple[int, float]]:
        same = side[:, None] == side[None, :]
        gain = (w * same).sum(axis=1) - (w * ~same).sum(axis=1)
        for i in np.argsort(-gain):                # promising flips first
            yield int(i), -float(gain[i])          # we minimize -cut

    def apply_move(i: int) -> None:
        side[i] ^= 1

    obj, stats = local_search(-cut_value(side), enumerate_moves, apply_move,
                              improvement="first")
    assert abs(obj + cut_value(side)) < 1e-6       # deltas match full recompute
    print(f"cut={-obj:.3f} moves={stats['moves']} sweeps={stats['sweeps']}")


weighted_maxcut_demo()
# Expected: cut=230.250 moves=13 sweeps=14 -- a 1-flip local optimum; the
# assert proves the accumulated deltas equal an independent recompute.
```

The demo recomputes the full gain vector each sweep for clarity (O(n²) per sweep). A
production version maintains `gain` incrementally — after flipping vertex i, only
`gain[j]` for neighbors j of i change, an O(degree) update. That pattern, plus
memoization and batch evaluation, is covered in depth in **fitness-evaluation-and-caching**.

### Parameter guidance

| Parameter | Typical range / choice | Trade-off |
|---|---|---|
| Improvement rule | first (default), best with vectorized scoring | Sweep cost vs step quality; final quality usually similar |
| Scan order | seeded random permutation per sweep | Removes positional bias; costs one `rng.permutation` per sweep |
| Improvement tolerance `tol` | 1e-9 … 1e-6 (scale to objective) | Too small: float-noise cycling; too large: stops early |
| Candidate list size k | 5–20 nearest neighbors | Smaller: faster sweeps, weaker local optima; >20 rarely pays off |
| Or-opt segment lengths | 1–3 | Longer segments: bigger neighborhood, diminishing returns |
| Max sweeps / move budget | bound by time, not count, in experiments | A budget cap protects wrappers (ILS, SA) from runaway descents |
| Restarts (standalone use) | 5–50 seeded starts, keep best | Cheap variance reduction; superseded by ILS-style perturbation |
| Delta audit frequency | every run in tests; every ~10⁴ moves in production | Catches drift and wrong delta formulas at negligible cost |

## Worked Example: TSP 2-opt with O(1) Delta Evaluation

Tour as a numpy position array `tour` (city at each position). The move `(i, j)` reverses
`tour[i+1 : j+1]`; the delta is the four-edge formula above. First, the scalar
first-improvement descent with a randomized scan order:

```python
import numpy as np


def tour_length(tour: np.ndarray, dist: np.ndarray) -> float:
    """Length of the closed tour (array of city indices by position)."""
    return float(dist[tour, np.roll(tour, -1)].sum())


def two_opt_delta(tour: np.ndarray, dist: np.ndarray, i: int, j: int) -> float:
    """O(1) length change of reversing tour[i+1 : j+1], for positions i < j."""
    n = len(tour)
    a, b = tour[i], tour[i + 1]
    c, d = tour[j], tour[(j + 1) % n]
    return float(dist[a, c] + dist[b, d] - dist[a, b] - dist[c, d])


def two_opt_first(tour: np.ndarray, dist: np.ndarray, seed: int = 0,
                  tol: float = 1e-9) -> tuple[np.ndarray, float]:
    """First-improvement 2-opt descent with a randomized scan order per sweep."""
    rng = np.random.default_rng(seed)
    tour = tour.copy()
    n = len(tour)
    length = tour_length(tour, dist)
    improved = True
    while improved:
        improved = False
        for i in rng.permutation(n - 2):
            i = int(i)
            for j in range(i + 2, n - (i == 0)):   # skip the wrap pair (0, n-1)
                delta = two_opt_delta(tour, dist, i, j)
                if delta < -tol:
                    tour[i + 1 : j + 1] = tour[i + 1 : j + 1][::-1]
                    length += delta
                    improved = True
                    break                          # take it, continue with next i
    return tour, length


def circle_instance(n: int, seed: int = 0) -> tuple[np.ndarray, np.ndarray]:
    """n points on the unit circle; the optimal tour visits them in angular order."""
    rng = np.random.default_rng(seed)
    theta = np.sort(rng.uniform(0.0, 2.0 * np.pi, n))
    pts = np.column_stack([np.cos(theta), np.sin(theta)])
    dist = np.linalg.norm(pts[:, None] - pts[None, :], axis=2)
    return pts, dist


_, dist = circle_instance(12, seed=42)
start = np.random.default_rng(7).permutation(12)
tour, length = two_opt_first(start, dist)
print(f"start={tour_length(start, dist):.4f} final={length:.4f} "
      f"optimal={tour_length(np.arange(12), dist):.4f}")
# Expected: start=14.6762 final=5.9567 optimal=5.9567. For points in convex
# position every 2-opt local optimum is crossing-free, and the only
# crossing-free tour through points in convex position is the hull tour.
```

Best improvement becomes attractive once the whole delta matrix is computed in one shot.
With `succ = np.roll(tour, -1)` and `edge[i]` the cost of the edge leaving position i, the
n×n delta matrix is four broadcasts — one (n, n) temporary per sweep (n = 5,000 →
~200 MB, so this variant is for n up to a few thousand):

```python
import numpy as np


def two_opt_best_vectorized(tour: np.ndarray, dist: np.ndarray,
                            tol: float = 1e-9) -> tuple[np.ndarray, float]:
    """Best-improvement 2-opt; each sweep scores all O(n^2) moves at once."""
    tour = tour.copy()
    n = len(tour)
    length = float(dist[tour, np.roll(tour, -1)].sum())
    iu = np.triu_indices(n, k=2)                   # positions with j >= i+2
    while True:
        succ = np.roll(tour, -1)
        edge = dist[tour, succ]                    # cost of edge at each position
        delta = (dist[tour[:, None], tour[None, :]]
                 + dist[succ[:, None], succ[None, :]]
                 - edge[:, None] - edge[None, :])
        k = int(np.argmin(delta[iu]))
        i, j = int(iu[0][k]), int(iu[1][k])
        if delta[i, j] >= -tol:
            return tour, length
        tour[i + 1 : j + 1] = tour[i + 1 : j + 1][::-1]
        length += float(delta[i, j])


rng = np.random.default_rng(3)
pts = rng.random((100, 2))
dist = np.linalg.norm(pts[:, None] - pts[None, :], axis=2)
start = rng.permutation(100)
tour, length = two_opt_best_vectorized(start, dist)
print(f"start={float(dist[start, np.roll(start, -1)].sum()):.3f} final={length:.3f}")
# Expected: start=46.152 final=8.733 -- about 81% shorter; a best-improvement
# 2-opt local optimum for 100 uniform points (optimal is typically ~7.7-8.0,
# so this sits 5-12% above it, normal for 2-opt from a random start).
```

The wrap pair (i=0, j=n−1) stays in the index set because its delta is exactly zero
(reversing everything after position 0 re-traverses the same closed tour), so it can never
be selected as improving.

Every delta formula gets an audit before it gets trusted. This is non-negotiable: a wrong
delta produces a descent that silently reports objectives that are not the objective.

```python
import numpy as np


def audit_two_opt_deltas(n: int = 60, trials: int = 500, seed: int = 1) -> float:
    """Largest |claimed delta - true length change| over random 2-opt moves."""
    rng = np.random.default_rng(seed)
    pts = rng.random((n, 2))
    dist = np.linalg.norm(pts[:, None] - pts[None, :], axis=2)
    tour = rng.permutation(n)
    base = float(dist[tour, np.roll(tour, -1)].sum())
    worst = 0.0
    for _ in range(trials):
        i = int(rng.integers(0, n - 3))
        j = int(rng.integers(i + 2, n - (i == 0)))
        a, b, c, d = tour[i], tour[i + 1], tour[j], tour[(j + 1) % n]
        delta = float(dist[a, c] + dist[b, d] - dist[a, b] - dist[c, d])
        trial = tour.copy()
        trial[i + 1 : j + 1] = trial[i + 1 : j + 1][::-1]
        true_change = float(dist[trial, np.roll(trial, -1)].sum()) - base
        worst = max(worst, abs(true_change - delta))
    return worst


print(f"max |delta - true change| = {audit_two_opt_deltas():.2e}")
# Expected: below 1e-12 -- pure floating-point rounding; the formula is exact.
```

2-opt local optima still contain misplaced *chains* of cities that no segment reversal can
fix. Or-opt relocates segments of length 1–3 (optionally reversed) elsewhere in the tour —
an O(1) delta with three edges destroyed and three created, and since the segment keeps
its orientation, the formula is also valid for asymmetric instances:

```python
import numpy as np


def closed_tour_length(tour: list[int], dist: np.ndarray) -> float:
    """Length of a closed tour stored as a Python list of city indices."""
    n = len(tour)
    return float(sum(dist[tour[k], tour[(k + 1) % n]] for k in range(n)))


def first_or_opt_move(tour: list[int], dist: np.ndarray,
                      tol: float) -> tuple[list[int], float] | None:
    """First improving Or-opt relocation (segment lengths 1-3), else None."""
    n = len(tour)
    for seg_len in (1, 2, 3):
        for i in range(1, n - seg_len + 1):        # segment occupies i..i+seg_len-1
            prev, first = tour[i - 1], tour[i]
            last, nxt = tour[i + seg_len - 1], tour[(i + seg_len) % n]
            gap = float(dist[prev, nxt] - dist[prev, first] - dist[last, nxt])
            if gap >= -tol:
                continue        # metric pruning: reinsertion cost is >= 0, so the
                                # removal itself must save length (triangle inequality)
            for j in range(n):
                if i - 1 <= j <= i + seg_len - 1:
                    continue                       # identity or inside the segment
                u, v = tour[j], tour[(j + 1) % n]
                delta = gap + float(dist[u, first] + dist[last, v] - dist[u, v])
                if delta < -tol:
                    seg = tour[i : i + seg_len]
                    rest = tour[:i] + tour[i + seg_len :]
                    at = rest.index(u)
                    return rest[: at + 1] + seg + rest[at + 1 :], delta
    return None


def or_opt_descent(tour: list[int], dist: np.ndarray,
                   tol: float = 1e-9) -> tuple[list[int], float]:
    """First-improvement Or-opt descent (segment relocation; Or 1976)."""
    length = closed_tour_length(tour, dist)
    while (step := first_or_opt_move(tour, dist, tol)) is not None:
        tour, delta = step
        length += delta
    return tour, length


rng = np.random.default_rng(11)
pts = rng.random((60, 2))
dist = np.linalg.norm(pts[:, None] - pts[None, :], axis=2)
start = [int(c) for c in rng.permutation(60)]
tour, length = or_opt_descent(start, dist)
assert abs(length - closed_tour_length(tour, dist)) < 1e-6
print(f"start={closed_tour_length(start, dist):.3f} final={length:.3f}")
# Expected: start=34.147 final=7.261 -- Or-opt alone reaches a relocation
# optimum; interleave with 2-opt (compound neighborhood) to go further.
```

In production TSP code these two neighborhoods are interleaved: run 2-opt to a local
optimum, then Or-opt; any Or-opt move re-opens 2-opt moves and vice versa, so loop until
both are exhausted. The apply here is O(n) (list splicing) while the delta stays O(1) —
the standard trade for relocation moves on array representations.

## Worked Example: Flow-Shop Insertion Neighborhood

Permutation flow shop: n jobs through m machines in the same order; `p[j, k]` is the
processing time of job j on machine k; minimize makespan. Completion times follow the
recurrence $C_{i,k} = \max(C_{i-1,k},\, C_{i,k-1}) + p_{\pi_i,k}$. The makespan is a
critical-path objective, so **no O(1) delta exists** for insertion moves — this example
shows what to do when deltas are structurally unavailable. The naive descent re-evaluates
every insertion from scratch:

```python
import numpy as np


def makespan(perm: np.ndarray, p: np.ndarray) -> float:
    """Permutation flow-shop makespan; p[j, k] = time of job j on machine k."""
    c = np.zeros(p.shape[1])
    for job in perm:
        c[0] += p[job, 0]
        for k in range(1, p.shape[1]):
            c[k] = max(c[k], c[k - 1]) + p[job, k]
    return float(c[-1])


def naive_insertion_descent(perm: np.ndarray,
                            p: np.ndarray) -> tuple[np.ndarray, float]:
    """Best-position insertion descent that re-evaluates every insertion from
    scratch: O(n^3 m) per sweep. Correct, slow -- the baseline to beat."""
    seq = [int(x) for x in perm]
    best = makespan(np.array(seq), p)
    improved = True
    while improved:
        improved = False
        for k in range(len(seq)):
            job = seq[k]
            rest = seq[:k] + seq[k + 1 :]
            cands = [makespan(np.array(rest[:i] + [job] + rest[i:]), p)
                     for i in range(len(rest) + 1)]
            i = int(np.argmin(cands))
            if cands[i] < best - 1e-9:
                seq = rest[:i] + [job] + rest[i:]
                best = cands[i]
                improved = True
    return np.array(seq), best


rng = np.random.default_rng(5)
p = rng.integers(1, 20, (8, 4)).astype(float)
perm, cmax = naive_insertion_descent(np.arange(8), p)
print(f"start={makespan(np.arange(8), p):.0f} final={cmax:.0f}")
# Expected: start=134 final=103 -- an insertion local optimum for this instance.
```

Taillard (1990, "Some efficient heuristic methods for the flow shop sequencing problem")
removes a factor of n: with heads $e$, tails $q$, and the inserted job's relative
completion times $f$, all $k{+}1$ insertion positions of one job into a k-job sequence
$\sigma$ are evaluated in O(km) total:

$$
e_{i,k} = \max(e_{i,k-1},\, e_{i-1,k}) + p_{\sigma_i,k}, \qquad
q_{i,k} = \max(q_{i,k+1},\, q_{i+1,k}) + p_{\sigma_i,k},
$$

$$
f_{i,k} = \max(f_{i,k-1},\, e_{i,k}) + p_{r,k}, \qquad
C_{\max}(\text{insert } r \text{ at } i) = \max_k \,(f_{i,k} + q_{i,k}),
$$

with $e_{0,k} = 0$ and the tail boundary row $q$ equal to zero past the last job. The
recurrences are sequential in both indices, but $f$ vectorizes over all insertion
positions at once — one numpy `maximum` per machine:

```python
import numpy as np


def makespan(perm: np.ndarray, p: np.ndarray) -> float:
    """Permutation flow-shop makespan; p[j, k] = time of job j on machine k."""
    c = np.zeros(p.shape[1])
    for job in perm:
        c[0] += p[job, 0]
        for k in range(1, p.shape[1]):
            c[k] = max(c[k], c[k - 1]) + p[job, k]
    return float(c[-1])


def heads(seq: np.ndarray, p: np.ndarray) -> np.ndarray:
    """e[i, k] = completion time of the first i jobs of seq on machine k."""
    n_m = p.shape[1]
    e = np.zeros((len(seq) + 1, n_m))
    for i in range(1, len(seq) + 1):
        row, prev = e[i], e[i - 1]
        row[0] = prev[0] + p[seq[i - 1], 0]
        for k in range(1, n_m):
            row[k] = max(row[k - 1], prev[k]) + p[seq[i - 1], k]
    return e


def tails(seq: np.ndarray, p: np.ndarray) -> np.ndarray:
    """q[i, k] = time from start of seq[i] on machine k to the end of all work."""
    n_m = p.shape[1]
    q = np.zeros((len(seq) + 1, n_m))
    for i in range(len(seq) - 1, -1, -1):
        row, nxt = q[i], q[i + 1]
        row[n_m - 1] = nxt[n_m - 1] + p[seq[i], n_m - 1]
        for k in range(n_m - 2, -1, -1):
            row[k] = max(row[k + 1], nxt[k]) + p[seq[i], k]
    return q


def insertion_costs(seq: np.ndarray, job: int, p: np.ndarray) -> np.ndarray:
    """Makespans of inserting `job` at each of len(seq)+1 positions, O(len*m)
    total (Taillard 1990) instead of O(len^2 * m) naive re-evaluation."""
    e, q = heads(seq, p), tails(seq, p)
    f = np.empty((len(seq) + 1, p.shape[1]))
    f[:, 0] = e[:, 0] + p[job, 0]
    for k in range(1, p.shape[1]):
        f[:, k] = np.maximum(f[:, k - 1], e[:, k]) + p[job, k]
    return (f + q).max(axis=1)


def neh(p: np.ndarray) -> np.ndarray:
    """NEH construction (Nawaz, Enscore & Ham 1983) built on insertion_costs."""
    order = np.argsort(-p.sum(axis=1), kind="stable")
    seq: list[int] = [int(order[0])]
    for job in order[1:]:
        costs = insertion_costs(np.array(seq), int(job), p)
        seq.insert(int(np.argmin(costs)), int(job))
    return np.array(seq)


def insertion_descent(perm: np.ndarray, p: np.ndarray, seed: int = 0,
                      tol: float = 1e-9) -> tuple[np.ndarray, float]:
    """Best-position insertion local search with Taillard acceleration:
    O(n^2 m) per sweep -- a factor n cheaper than naive re-evaluation."""
    rng = np.random.default_rng(seed)
    seq = [int(x) for x in perm]
    best = makespan(np.array(seq), p)
    improved = True
    while improved:
        improved = False
        for job in rng.permutation(len(seq)):     # jobs are labeled 0..n-1
            job = int(job)
            k = seq.index(job)
            rest = np.array(seq[:k] + seq[k + 1 :])
            costs = insertion_costs(rest, job, p)
            i = int(np.argmin(costs))
            if costs[i] < best - tol:
                seq = [int(x) for x in rest[:i]] + [job] + [int(x) for x in rest[i:]]
                best = float(costs[i])
                improved = True
    return np.array(seq), best


rng = np.random.default_rng(3)
p = rng.integers(1, 100, (20, 5)).astype(float)

# Audit: accelerated insertion costs == naive re-evaluation, every position.
seq = rng.permutation(np.arange(19))
naive = [makespan(np.insert(seq, i, 19), p) for i in range(20)]
assert np.allclose(insertion_costs(seq, 19, p), naive)

start = neh(p)
final, cmax = insertion_descent(start, p)
print(f"random={makespan(np.arange(20), p):.0f} NEH={makespan(start, p):.0f} "
      f"NEH+descent={cmax:.0f}")
# Expected: random=1541 NEH=1294 NEH+descent=1261 -- NEH start plus insertion
# descent; the assert proves the acceleration is exact, not approximate.
```

The lesson generalizes: when the objective has no O(1) delta, look for shared
subcomputation across the whole neighborhood (heads/tails here, critical-path filtering in
job shop) and evaluate the neighborhood *as a batch*. This insertion descent seeded by NEH
is also exactly the inner loop of iterated greedy, the state of the art for permutation
flow shops.

## Scaling Up: Candidate Lists and Don't-Look Bits

Full 2-opt sweeps are O(n²) delta evaluations. Two classic devices (Bentley 1992) cut this
to near-linear per sweep with almost no quality loss on geometric instances:

- **Candidate lists.** Only consider moves that create an edge (a, c) where c is among the
  k nearest neighbors of a. Since candidates are sorted by distance, the scan for city a
  stops as soon as `dist[a, c]` is no shorter than both tour edges at a — no remaining
  candidate can yield an improving move from a.
- **Don't-look bits.** After city a yields no improving move, switch its bit off and skip
  it until a move changes one of its tour neighbors. Maintained with a queue, this focuses
  work where the tour just changed.

```python
import numpy as np
from collections import deque


def two_opt_candidate_lists(pts: np.ndarray, k: int = 8, seed: int = 0,
                            tol: float = 1e-9) -> tuple[np.ndarray, float, int]:
    """2-opt restricted to k-nearest-neighbor moves with don't-look bits
    (Bentley 1992). Returns (tour, length, number of delta evaluations)."""
    n = len(pts)
    dist = np.linalg.norm(pts[:, None] - pts[None, :], axis=2)
    cand = np.argsort(dist, axis=1)[:, 1 : k + 1]  # k nearest, sorted
    rng = np.random.default_rng(seed)
    tour = rng.permutation(n)
    pos = np.empty(n, dtype=np.int64)
    pos[tour] = np.arange(n)
    length = float(dist[tour, np.roll(tour, -1)].sum())
    evals = 0

    def apply(q1: int, q2: int) -> None:           # drop edges at positions q1, q2
        lo, hi = (q1, q2) if q1 < q2 else (q2, q1)
        tour[lo + 1 : hi + 1] = tour[lo + 1 : hi + 1][::-1]
        pos[tour[lo + 1 : hi + 1]] = np.arange(lo + 1, hi + 1)

    queue: deque[int] = deque(int(c) for c in rng.permutation(n))
    queued = np.ones(n, dtype=bool)
    while queue:
        a = queue.popleft()
        queued[a] = False
        pa = int(pos[a])
        succ_a, pred_a = int(tour[(pa + 1) % n]), int(tour[pa - 1])
        for c in cand[a]:
            c = int(c)
            evals += 1
            if dist[a, c] >= max(dist[a, succ_a], dist[pred_a, a]):
                break                              # sorted: no further gain possible
            pc = int(pos[c])
            succ_c, pred_c = int(tour[(pc + 1) % n]), int(tour[pc - 1])
            # forward: drop (a,succ_a),(c,succ_c); add (a,c),(succ_a,succ_c)
            d_fwd = (dist[a, c] + dist[succ_a, succ_c]
                     - dist[a, succ_a] - dist[c, succ_c])
            # backward: drop (pred_a,a),(pred_c,c); add (a,c),(pred_a,pred_c)
            d_bwd = (dist[a, c] + dist[pred_a, pred_c]
                     - dist[pred_a, a] - dist[pred_c, c])
            if min(d_fwd, d_bwd) >= -tol:
                continue
            if d_fwd <= d_bwd:
                touched = (a, succ_a, c, succ_c)
                apply(pa, pc)
                length += float(d_fwd)
            else:
                touched = (a, pred_a, c, pred_c)
                apply((pa - 1) % n, (pc - 1) % n)
                length += float(d_bwd)
            for t in touched:                      # wake the cities that moved
                if not queued[t]:
                    queue.append(t)
                    queued[t] = True
            break                                  # a re-enters via the queue
    return tour, length, evals


rng = np.random.default_rng(9)
pts = rng.random((400, 2))
tour, length, evals = two_opt_candidate_lists(pts, k=8, seed=9)
dist = np.linalg.norm(pts[:, None] - pts[None, :], axis=2)
assert abs(length - float(dist[tour, np.roll(tour, -1)].sum())) < 1e-6
print(f"length={length:.3f} evals={evals} "
      f"(one full-neighborhood sweep alone = {400 * 399 // 2} deltas)")
# Expected: length=17.200 evals=4925 -- the entire descent from a random tour
# (length 205.1) costs fewer delta evaluations than a tenth of ONE full sweep.
```

The local optimum is now relative to the *restricted* neighborhood: a small (usually <1%)
quality sacrifice on geometric instances for one to two orders of magnitude less work. For
coordinates without a precomputed matrix, build `cand` with `scipy.spatial.cKDTree` and
look distances up on demand; for n in the 10⁵ range, replace array reversal with a
two-level doubly linked tour so the apply cost stops dominating.

## Advanced Techniques

### Compound neighborhoods and descent ordering

Order neighborhoods cheap-to-expensive and let each restart the cheaper ones: 2-opt to a
local optimum, then Or-opt; any accepted Or-opt move re-enables 2-opt moves around the
touched edges, so alternate until no neighborhood improves. The result is a local optimum
with respect to the *union* of neighborhoods at far less cost than scanning the union
directly. This pipeline (variable neighborhood descent) typically beats deepening any
single neighborhood — going from 2-opt to full 3-opt costs O(n³) per sweep, while
2-opt + Or-opt covers most 3-opt gains in O(n²).

### Delta evaluation under side constraints

Constrained problems need the delta to price feasibility, not just cost. Maintain
auxiliary state with O(1) incremental updates per move: route load for capacity checks,
cumulative earliest/latest start times for time windows, machine completion times for
scheduling. The pattern: a move is scored as `delta_cost + delta_penalty`, both computed
from cached prefix/suffix quantities; the apply updates those caches incrementally. If a
constraint cannot be priced incrementally (for example, makespan-style coupling), batch
the neighborhood like the Taillard scheme above. Penalty weights that change *during*
search invalidate cached deltas — recompute or rescale caches whenever weights move.

### Plateaus and sideways moves

On objectives with many ties (set covering, satisfiability-style counts, makespan), strict
descent stalls on plateaus where all deltas are ≥ 0 and many are exactly 0. Allow sideways
moves (delta = 0) with a cap — a fixed number of consecutive non-improving accepted moves
— and break ties randomly to random-walk along the plateau until an exit appears. Track
visited move attributes to avoid 2-cycles between two equal-cost solutions. This is the
boundary where plain descent ends and tabu-style memory begins; if sideways caps keep
hitting, switch the wrapper rather than tuning the cap (Hoos & Stützle 2004, "Stochastic
Local Search: Foundations and Applications").

### Profiling the move loop

Measure, per sweep: delta evaluations, accepted moves, time in delta vs apply vs
bookkeeping. Healthy descents spend >80% of time in delta evaluation; if apply dominates,
the representation is wrong for the move (array reversal on huge tours, list splicing in
hot loops). If bookkeeping dominates, the scan-order machinery is too clever for the
instance size. These counters cost nothing and decide where candidate lists, numba, or a
data-structure change pays — before reaching for any of them, confirm with the audit
functions that correctness holds, then optimize.

## Practical Challenges

**The accumulated objective drifts away from the true value.** Thousands of `length +=
delta` operations accumulate float error, and a wrong delta formula hides inside plausible
numbers. Recompute the objective from scratch every ~10⁴ moves and assert agreement within
1e-6; run a delta audit (random moves, claimed delta vs recomputed change) in the test
suite for every move type. The audit above caught nothing because the formula is exact —
that is what the report should say, with evidence.

**2-opt deltas are wrong on asymmetric instances.** Segment reversal flips the direction
of every interior edge, so the four-edge formula silently undercounts. For asymmetric
costs use orientation-preserving moves: Or-opt relocation, 3-opt variants that reconnect
without reversal, or transform the instance to a symmetric one of twice the size.

**The descent cycles between equal-cost solutions.** Accepting `delta < 0` with `tol = 0`
lets float noise alternate two reversals forever. Use a scaled tolerance (`tol` around
1e-9 × objective magnitude), and if sideways moves are allowed, cap consecutive
non-improving acceptances and randomize tie-breaking.

**Correct but too slow beyond n ≈ 2,000.** Profile first: if the time is in delta
evaluation, add candidate lists and don't-look bits (above) or vectorize the scoring; if
it is in apply, change the move (Or-opt instead of long reversals) or the data structure.
A numba `@njit` on the scalar scan loop is often a 50–100× drop-in win once the algorithm
is final.

**Moves keep producing infeasible solutions.** Decide per constraint: restrict the
neighborhood so moves preserve feasibility (swap within a machine, relocate only if load
fits), or price violations in the delta with a penalty and let the wrapper manage weights.
Never mix silently — a "feasible-only" neighborhood with one unchecked corner case
produces infeasible incumbents that the objective bookkeeping cannot detect. Keep an
independent feasibility checker and run it on every reported incumbent.

**First improvement spends most of its time on the final, empty sweep.** The certificate
sweep costs |N| evaluations with zero improvements — for n = 1,000 2-opt, half a million
deltas just to stop. Pruning bounds (sorted candidates with early break) and don't-look
bits shrink exactly this cost; budget-based stopping inside a metaheuristic wrapper
removes it entirely at the price of not certifying local optimality.

**The same move code behaves differently inside SA or tabu search.** It should not: the
acceptance rule changes, the neighborhood and delta code stay identical. If results
diverge, the usual cause is hidden state in the move enumerator (stale caches after
non-improving accepted moves, which plain descent never makes). Keep move/delta/apply
pure with explicit cache-update functions, and test them under random accept/reject
sequences, not only descent traces.

**No O(1) delta exists for the objective.** Critical-path objectives (makespan), nested
max/min, or simulation-based costs do not decompose edge-wise. Use batch evaluation with
shared subcomputation (Taillard heads/tails), restrict moves to the critical path where
off-path moves provably cannot improve, or accept an O(n) delta and compensate with a
smaller, better-targeted neighborhood.

## Tools & Libraries

| Library / tool | When to use | Note |
|---|---|---|
| numpy | All matrix work, vectorized move scoring, batch deltas | `default_rng(seed)` everywhere; `argsort`/`argpartition` build candidate lists |
| scipy.spatial.cKDTree | k-nearest-neighbor candidate lists without an O(n²) matrix | `query(pts, k+1)` gives sorted neighbor lists directly |
| numba | Scalar move loops too slow in CPython after the algorithm is final | `@njit` the delta+scan loop; keep numpy types at the boundary |
| OR-Tools routing | Production VRP/TSP local search you should not rewrite | Built-in 2-opt, Or-opt, relocate, exchange plus guided local search |
| LKH-3 | Reference tours for calibrating your 2-opt/Or-opt gaps | Lin-Kernighan-Helsgaun; the quality yardstick for TSP-like problems |
| tsplib95 | Parsing TSPLIB benchmark instances | Standard EUC_2D / explicit-matrix handling |
| pytest | Delta audits and known-optimum regression tests in CI | Run `audit_*` functions as tests, not as one-off scripts |
| pandas | Result tables across instances, seeds, configurations | One row per run; aggregation for the report tables below |

## Output Format

A complete local-search deliverable contains:

1. **Neighborhood specification.** Move definition(s), neighborhood size as a function of
   n, delta formula with its cost (O(1)/O(n)/batched), apply cost, and which constraints
   moves preserve vs price. One paragraph or table — this is the part reviewers check.
2. **Engine configuration.** Improvement rule, scan order, tolerance, candidate list size,
   seeds, stopping condition. Every value that affects the trajectory must be stated and
   seeded.
3. **Correctness evidence.** Delta audit result (max |claimed − recomputed| over random
   moves), independent objective recompute at termination, and feasibility-checker pass on
   the final solution.
4. **Solution-quality report.** One row per (instance, seed):

   | instance | n | start obj | final obj | improv % | moves | delta evals | time (s) |
   |---|---|---|---|---|---|---|---|
   | rand-400 | 400 | 205.14 | 17.20 | 91.6 | 888 | 4,925 | 0.06 |
   | circle-12 | 12 | 14.68 | 5.96 | 59.4 | 17 | 198 | <0.001 |

   Report best/mean/worst over seeds when multistarting, plus the gap to a reference
   (optimal value, LKH tour, or best-known bound) where one exists.
5. **Convergence summary.** Objective vs accepted-move index (or time), noting where the
   descent flattened — this tells the reader whether a wrapper (restart, perturbation,
   annealing) would pay.
6. **File artifacts.** Final solution in a problem-standard format, run table as CSV (one
   row per run with instance, seed, config, objective, time), and the exact config used.

## Questions to Ask

- What representation does the current code use for a solution, and can I see one example?
- Is the objective a sum over solution elements, or does it involve max/min coupling like
  a makespan?
- Which constraints must every move preserve, and which may be temporarily violated?
- Are distances/costs symmetric? (This decides whether 2-opt-style reversal moves are
  usable.)
- What are the instance sizes now, and what sizes must this still handle next year?
- What is the time budget per run, and is this a standalone descent or the inner loop of a
  metaheuristic?
- Is there an existing evaluation function I should reuse and profile before writing
  deltas?
- How will solutions be validated independently of the search code?
- Is there a known optimum, best-known value, or reference solver output to calibrate
  against?

## Related Skills

- **fitness-evaluation-and-caching** — when the evaluation itself is the bottleneck:
  incremental gain structures, memoized evaluators, surrogate and batch evaluation beyond
  the per-move deltas shown here.
- **simulated-annealing** — when descent stalls in local optima and you want probabilistic
  acceptance of worsening moves over exactly these neighborhoods.
- **tabu-search** — when escaping local optima needs memory: tabu attributes, aspiration,
  and frequency-based diversification on top of the same move pool.
- **iterated-local-search** — when this descent is good but needs perturbation, restart,
  and acceptance logic wrapped around it to become a full metaheuristic.
- **traveling-salesman-problem** — when you need the full TSP toolbox around the 2-opt and
  Or-opt engines here: formulations, construction heuristics, and benchmark instances.
