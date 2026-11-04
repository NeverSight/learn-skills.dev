---
name: fitness-evaluation-and-caching
description: When the user wants to speed up objective evaluation in a metaheuristic or local search — profiling, delta/incremental evaluation, memoization with solution hashing, surrogate, vectorized batch, and parallel evaluation. Also use when the user mentions "fitness evaluation," "delta evaluation," "incremental evaluation," "memoization," "expensive objective," or "evaluation bottleneck," or when most runtime goes to recomputing objectives from scratch. For move and neighborhood design, see local-search-and-neighborhoods; for array-level speedups, see numpy-vectorization-for-optimization.
---

# Fitness Evaluation and Caching

You are an expert in efficient objective-function evaluation for combinatorial optimization. A typical
metaheuristic spends 80-95% of its runtime evaluating candidate solutions, so the evaluator — not the
search logic — decides how many iterations fit in the time budget. This skill is a catalog of the
standard speedup components: profiling, delta/incremental evaluation, memoization with canonical
solution hashing, vectorized batch evaluation, surrogate evaluation, and parallel evaluation. Use the
framework below to pick the right component, implement it correctly, and prove that it computes the
same numbers as the naive evaluator.

## Initial Assessment

Establish these facts before recommending or writing any code:

- **Measured bottleneck.** Has the user profiled? Confirm with `cProfile` or timing counters that
  evaluation dominates runtime before optimizing it.
- **Cost of one evaluation.** Microseconds (array formula), milliseconds (LP solve, decoder), or
  seconds (simulation)? The band selects the technique: delta/vectorization for cheap objectives,
  parallelism and surrogates for expensive ones.
- **Evaluation budget.** Wall-clock budget and evaluation count: 10^8 evaluations forbid 1 ms each.
- **Search pattern.** Trajectory method scanning a neighborhood (delta evaluation applies),
  population method evaluating batches (vectorization/parallelism applies), or both (memetic)?
- **Move structure.** Which solution components does one move change? Delta evaluation only pays
  off when a move touches O(1) or O(n) of an O(n^2) objective.
- **Objective structure.** A sum of local terms gives cheap deltas; globally propagating
  quantities (e.g., makespan through a critical path) need auxiliary state or full recomputation.
- **Numerics and determinism.** Integer costs give exact deltas forever; floating-point deltas
  drift and need resynchronization. Stochastic objectives break naive memoization entirely.
- **Revisit rate.** Does the search re-evaluate previously seen solutions? Memoization is
  worthless at a 0% hit rate; measure before paying the memory.
- **Hardware and memory.** Cores available for parallel evaluation; RAM for caches and delta
  tables (an all-pairs delta table is O(n^2) floats).
- **Exactness requirement.** Are approximate fitness values acceptable during search (surrogates,
  sampling), provided final reporting re-evaluates exactly?

## The Evaluation Hierarchy

Total search effort factorizes as $T = N_{\text{evals}} \times C_{\text{eval}}$, and a
best-improvement local search performs $|N(s)|$ candidate evaluations per iteration. Every
technique in this skill attacks $C_{\text{eval}}$ (or hides it behind cores); neighborhood design
attacks $|N(s)|$ and belongs to **local-search-and-neighborhoods**.

The running worked example is the quadratic assignment problem (QAP). With flow matrix
$A=(a_{ij})$, distance matrix $B=(b_{k\ell})$, and permutation $\pi$ assigning facility $i$ to
location $\pi(i)$:

$$
f(\pi) \;=\; \sum_{i=1}^{n}\sum_{j=1}^{n} a_{ij}\, b_{\pi(i)\pi(j)},
\qquad
\Delta(\pi, r, s) \;=\; f(\pi \circ (r\,s)) - f(\pi),
$$

where $(r\,s)$ swaps positions $r$ and $s$. Full evaluation costs $O(n^2)$; the swap neighborhood
has $n(n-1)/2$ moves. The cost of one full best-improvement scan under each evaluation strategy:

| Strategy | Cost per scan of all swaps | Source of the saving |
|---|---|---|
| Full recomputation per candidate | $O(n^4)$ | none (baseline) |
| $O(n)$ swap delta per candidate | $O(n^3)$ | only changed terms recomputed |
| Delta table maintained across moves | $O(n^2)$ amortized | previous deltas updated in $O(1)$ each (Taillard 1991, robust taboo search) |

### Technique taxonomy

| Technique | Mechanism | Exact? | Use when | Typical gain |
|---|---|---|---|---|
| Delta evaluation | recompute only terms a move changes | exact | separable objective, small moves | factor $n$ to $n^2$ |
| Incremental auxiliary state | maintain running aggregates (loads, conflict counts) | exact | objective needs per-component aggregates | factor of structure size |
| Memoization | skip re-evaluation of seen solutions | exact | search revisits solutions (cycling, restarts into same basin) | proportional to hit rate |
| Vectorized batch evaluation | one array expression evaluates the whole population | exact | population/multi-start methods, cheap algebraic objective | 10-100x constant factor |
| Surrogate / sampled evaluation | cheap correlated proxy ranks candidates | approximate | evaluation dominated by simulation or heavy decoder | 10-1000x, costs accuracy |
| Parallel evaluation | distribute evaluations over cores | exact | per-evaluation cost far exceeds dispatch overhead | up to core count (wall clock only) |

### Delta evaluation across the problem catalog

| Problem | Move | Full eval | Delta cost | Auxiliary state |
|---|---|---|---|---|
| TSP (symmetric) | 2-opt, Or-opt relocation | $O(n)$ | $O(1)$ | none |
| QAP | swap | $O(n^2)$ | $O(n)$; $O(1)$ amortized with table | $O(n^2)$ delta matrix |
| Knapsack family | flip / exchange item | $O(n)$ | $O(1)$ | running weight and value |
| Graph coloring | recolor vertex $v$ | $O(|E|)$ | $O(1)$ query, $O(\deg v)$ apply | conflict counts per (vertex, color) |
| Max-SAT | flip variable $x$ | $O(\text{clauses})$ | $O(\text{occurrences of } x)$ | satisfied-literal count per clause |
| Permutation flow shop (makespan) | job insertion | $O(nm)$ per schedule | $O(nm)$ for **all** $n$ insertions of one job (Taillard 1990 acceleration) | head/tail completion matrices |
| Bin packing | move item between bins | $O(n)$ | $O(1)$ | per-bin loads |
| Set covering | add/drop column | $O(nm)$ | $O(\text{rows covered by column})$ | cover count per row |
| VRP | relocate / exchange between routes | $O(\text{route lengths})$ | $O(1)$ | per-route load, duration, distance |

### Order of attack

1. **Profile** — confirm evaluation dominates, and which part of it.
2. **Delta evaluation** — the largest asymptotic win for trajectory methods; required for
   competitive tabu search and simulated annealing on QAP-like problems.
3. **Vectorize batches** — for population methods, before any parallelism.
4. **Memoize** — only where a measured revisit rate exists; cheap to add, easy to waste memory on.
5. **Parallelize** — multiplies whatever per-evaluation cost remains; never fixes a slow evaluator.
6. **Surrogates** — last, because they trade exactness; reserve for evaluations above ~10 ms.

The gains multiply: an $O(n)$ delta inside a vectorized scan over 8 cores stacks all three factors.

## Profiling the Evaluation Bottleneck

**When to use.** Always first, and again after every change. **Complexity.** Negligible overhead
for counters; 2-5x slowdown while `cProfile` is attached. **Fits.** Every algorithm; wrap the
objective once and pass the wrapper everywhere.

A counting wrapper gives evaluations/second and best-so-far without touching the search code:

```python
import time
from collections.abc import Callable
from dataclasses import dataclass

import numpy as np


@dataclass
class EvalProfile:
    """Counts, times, and tracks the best value of every objective call."""
    fn: Callable[[np.ndarray], float]
    calls: int = 0
    total_s: float = 0.0
    best: float = float("inf")

    def __call__(self, x: np.ndarray) -> float:
        t0 = time.perf_counter()
        value = self.fn(x)
        self.total_s += time.perf_counter() - t0
        self.calls += 1
        self.best = min(self.best, value)
        return value

    def report(self) -> str:
        """One-line summary: calls, total time, mean microseconds per call."""
        mean_us = 1e6 * self.total_s / max(self.calls, 1)
        return f"{self.calls} evals, {self.total_s:.3f} s, {mean_us:.1f} us/eval, best {self.best:.1f}"


def qap_full(perm: np.ndarray, a: np.ndarray, b: np.ndarray) -> float:
    """Full QAP objective sum_ij a[i,j] * b[perm[i], perm[j]].  O(n^2)."""
    return float(np.sum(a * b[np.ix_(perm, perm)]))


rng = np.random.default_rng(0)
n = 30
a = rng.integers(0, 10, (n, n)).astype(float)
b = rng.integers(0, 10, (n, n)).astype(float)
profiled = EvalProfile(lambda p: qap_full(p, a, b))
for _ in range(1000):
    profiled(rng.permutation(n))
print(profiled.report())
# Expected: 1000 evals in well under a second, mean cost in the tens of
# microseconds; rerunning with n=100 shows ~10x cost per eval -- the O(n^2) wall.
```

When the evaluator is buried inside a larger search, attribute time to functions with
`cProfile.Profile()` around one neighborhood scan, then
`pstats.Stats(profiler).sort_stats("tottime").print_stats(10)`. The classic signature of a missing
delta evaluation is one cheap function called enormous numbers of times: profiling a
full-recomputation 2-opt scan at $n = 150$ shows ~11,000 calls to the $O(n)$ tour-length function
(plus 11,000 array copies) absorbing essentially all the runtime, while the search logic is
invisible. The matching anti-pattern and its $O(1)$ replacement appear in the TSP delta example
below. Re-profile after every change: once deltas land, the bottleneck typically migrates to
neighbor copying or move bookkeeping, which needs a different fix (apply/undo, see Practical
Challenges).

## Delta and Incremental Evaluation

**When to use.** Trajectory methods (tabu search, simulated annealing, ILS, VNS) and the local
search inside memetic algorithms — anywhere candidates differ from the current solution by a small
move. **Complexity.** Per-problem; see the catalog table above. **Fits.** Any objective that is a
sum of terms where a move changes few terms, or that admits auxiliary state updated locally.

Implement deltas against a fixed three-function contract: `full(s)` (ground truth, kept obviously
correct), `delta(s, move)` (cost change **without** applying), `apply(s, move)` (mutate solution
and auxiliary state). The golden invariant `delta(s, m) == full(apply(copy(s), m)) - full(s)` (to
FP tolerance) must hold for every move type; assert it on hundreds of random pairs in CI.

### QAP swap delta in O(n)

Swapping positions $r, s$ leaves all terms with $i, j \notin \{r, s\}$ unchanged; only the $O(n)$
terms in rows/columns $r$ and $s$ are recomputed (general, non-symmetric form):

```python
import numpy as np


def qap_full(perm: np.ndarray, a: np.ndarray, b: np.ndarray) -> float:
    """Full QAP objective sum_ij a[i,j] * b[perm[i], perm[j]].  O(n^2)."""
    return float(np.sum(a * b[np.ix_(perm, perm)]))


def qap_swap_delta(perm: np.ndarray, a: np.ndarray, b: np.ndarray, r: int, s: int) -> float:
    """Cost change of swapping perm[r] and perm[s].  O(n), exact.

    Standard swap delta for the general (non-symmetric) QAP; see
    Taillard (1991), robust taboo search."""
    pr, ps = perm[r], perm[s]
    d = ((a[r, r] - a[s, s]) * (b[ps, ps] - b[pr, pr])
         + (a[r, s] - a[s, r]) * (b[ps, pr] - b[pr, ps]))
    k = np.ones(len(perm), dtype=bool)
    k[[r, s]] = False
    pk = perm[k]
    d += float(np.sum((a[k, r] - a[k, s]) * (b[pk, ps] - b[pk, pr])
                      + (a[r, k] - a[s, k]) * (b[ps, pk] - b[pr, pk])))
    return float(d)


rng = np.random.default_rng(1)
n = 12
a = rng.integers(0, 20, (n, n)).astype(float)
b = rng.integers(0, 20, (n, n)).astype(float)
perm = rng.permutation(n)
for _ in range(200):
    r, s = (int(v) for v in rng.choice(n, size=2, replace=False))
    swapped = perm.copy()
    swapped[[r, s]] = swapped[[s, r]]
    assert abs(qap_swap_delta(perm, a, b, r, s)
               - (qap_full(swapped, a, b) - qap_full(perm, a, b))) < 1e-9
    perm = swapped
print("O(n) delta matches full recomputation on 200 random swaps")
# Expected: the assert holds on every trial -- one neighborhood scan drops
# from O(n^4) to O(n^3).
```

### QAP delta table: O(1) amortized per candidate

Best-improvement search needs **all** pair deltas every iteration. Keep them in a table: after
applying swap $(u, v)$, every delta $\Delta(r, s)$ with $\{r,s\} \cap \{u,v\} = \emptyset$ changes
by a closed-form $O(1)$ correction (Taillard 1991); only the $O(n)$ pairs touching $u$ or $v$ need
the $O(n)$ formula. One iteration then costs $O(n^2)$ instead of $O(n^3)$:

```python
import numpy as np


class QAPDeltaTable:
    """All-pairs swap deltas for the QAP, kept current in O(n^2) per move.

    Building the table costs O(n^3) once; each applied move refreshes it
    in O(n^2): a vectorized O(1)-per-entry correction for pairs disjoint
    from the swap, plus exact O(n) recomputation for pairs touching it.
    Best-improvement scans become an O(n^2) argmin over the table."""

    def __init__(self, a: np.ndarray, b: np.ndarray, perm: np.ndarray) -> None:
        self.a, self.b = a, b
        self.perm = perm.copy()
        self.n = len(perm)
        self.cost = float(np.sum(a * b[np.ix_(perm, perm)]))
        self.delta = np.zeros((self.n, self.n))
        for r in range(self.n):
            for s in range(r + 1, self.n):
                self.delta[r, s] = self.delta[s, r] = self._swap_delta(r, s)

    def _swap_delta(self, r: int, s: int) -> float:
        """Exact O(n) delta of swapping positions r and s."""
        a, b, p = self.a, self.b, self.perm
        pr, ps = p[r], p[s]
        d = ((a[r, r] - a[s, s]) * (b[ps, ps] - b[pr, pr])
             + (a[r, s] - a[s, r]) * (b[ps, pr] - b[pr, ps]))
        k = np.ones(self.n, dtype=bool)
        k[[r, s]] = False
        pk = p[k]
        d += float(np.sum((a[k, r] - a[k, s]) * (b[pk, ps] - b[pk, pr])
                          + (a[r, k] - a[s, k]) * (b[ps, pk] - b[pr, pk])))
        return float(d)

    def apply_swap(self, u: int, v: int) -> None:
        """Apply swap (u, v) and refresh the whole table in O(n^2)."""
        a, b, p = self.a, self.b, self.perm
        self.cost += float(self.delta[u, v])
        pu, pv = p[u], p[v]
        # O(1)-per-entry correction, valid for pairs disjoint from {u, v};
        # all quantities use the permutation BEFORE the swap.
        c1 = a[:, u] - a[:, v]
        c2 = a[u, :] - a[v, :]
        g = b[p, pv] - b[p, pu]
        h = b[pv, p] - b[pu, p]
        self.delta += ((c1[:, None] - c1[None, :]) * (g[None, :] - g[:, None])
                       + (c2[:, None] - c2[None, :]) * (h[None, :] - h[:, None]))
        p[[u, v]] = p[[v, u]]
        # Pairs touching u or v: exact O(n) recomputation.
        for r in (u, v):
            for s in range(self.n):
                if s != r:
                    d = self._swap_delta(min(r, s), max(r, s))
                    self.delta[r, s] = self.delta[s, r] = d
        np.fill_diagonal(self.delta, 0.0)


rng = np.random.default_rng(7)
n = 15
a = rng.integers(0, 20, (n, n)).astype(float)
b = rng.integers(0, 20, (n, n)).astype(float)
table = QAPDeltaTable(a, b, rng.permutation(n))
while True:  # best-improvement descent, O(n^2) per iteration
    u, v = (int(x) for x in np.unravel_index(np.argmin(table.delta), table.delta.shape))
    if table.delta[u, v] >= -1e-9:
        break
    table.apply_swap(u, v)
fresh = QAPDeltaTable(a, b, table.perm)
assert abs(table.cost - fresh.cost) < 1e-6
assert np.allclose(table.delta, fresh.delta, atol=1e-6)
print(f"local optimum cost {table.cost:.0f}; incremental table matches rebuilt table")
# Expected: descent reaches a local optimum and the incrementally maintained
# table agrees entry-by-entry with one rebuilt from scratch.
```

This structure is exactly what **tabu-search** consumes: the argmin scan becomes "best non-tabu
swap", and the table survives across iterations.

### TSP 2-opt delta in O(1)

```python
import numpy as np


def tour_length(tour: np.ndarray, d: np.ndarray) -> float:
    """Closed-tour length.  O(n)."""
    return float(d[tour, np.roll(tour, -1)].sum())


def two_opt_delta(tour: np.ndarray, d: np.ndarray, i: int, j: int) -> float:
    """Length change of reversing segment tour[i+1..j].  O(1).

    Removes edges (t[i], t[i+1]) and (t[j], t[j+1]); adds (t[i], t[j])
    and (t[i+1], t[j+1]). Requires a symmetric distance matrix -- for
    asymmetric TSP the reversed segment changes O(n) arc costs."""
    n = len(tour)
    p, q = tour[i], tour[(i + 1) % n]
    r, s = tour[j], tour[(j + 1) % n]
    return float(d[p, r] + d[q, s] - d[p, q] - d[r, s])


rng = np.random.default_rng(2)
n = 80
pts = rng.uniform(0.0, 100.0, (n, 2))
d = np.hypot(pts[:, None, 0] - pts[None, :, 0], pts[:, None, 1] - pts[None, :, 1])
tour = rng.permutation(n)
for _ in range(300):
    i = int(rng.integers(0, n - 3))
    j = int(rng.integers(i + 2, n - 1))
    cand = tour.copy()
    cand[i + 1:j + 1] = cand[i + 1:j + 1][::-1]
    assert abs(two_opt_delta(tour, d, i, j)
               - (tour_length(cand, d) - tour_length(tour, d))) < 1e-9
print("O(1) 2-opt delta verified on 300 random moves")
# Expected: all asserts pass; a full 2-opt scan costs O(n^2) with this delta
# versus O(n^3) with recomputation.
```

### Incremental auxiliary state: graph coloring conflicts

When the delta is not a closed form, maintain a data structure. For $k$-coloring with the
conflicting-edge objective, keep `counts[v, c]` = number of neighbors of `v` colored `c`. The delta
of a recolor is an $O(1)$ lookup; applying it updates only the neighbors. This is the engine of
TabuCol (Hertz & de Werra 1987, "Using tabu search techniques for graph coloring").

```python
import numpy as np


class ColoringConflicts:
    """Incremental conflict evaluation for k-coloring.

    State: counts[v, c] = neighbors of v currently colored c;
    total = number of conflicting edges. delta() is O(1); apply() is
    O(deg v); full evaluation is O(|E|). Fits tabu search and simulated
    annealing on graph coloring, timetabling, and frequency assignment."""

    def __init__(self, adj: list[np.ndarray], colors: np.ndarray, k: int) -> None:
        self.adj = adj
        self.colors = colors.copy()
        n = len(adj)
        self.counts = np.zeros((n, k), dtype=np.int64)
        for v in range(n):
            np.add.at(self.counts[v], self.colors[adj[v]], 1)
        self.total = int(sum(self.counts[v, self.colors[v]] for v in range(n))) // 2

    def delta(self, v: int, c: int) -> int:
        """Change in conflicting edges if v is recolored to c.  O(1)."""
        return int(self.counts[v, c] - self.counts[v, self.colors[v]])

    def apply(self, v: int, c: int) -> None:
        """Recolor v to c, updating neighbor counts.  O(deg v)."""
        self.total += self.delta(v, c)
        nbrs = self.adj[v]
        self.counts[nbrs, self.colors[v]] -= 1  # unique indices: safe fancy update
        self.counts[nbrs, c] += 1
        self.colors[v] = c


rng = np.random.default_rng(4)
n, k = 60, 4
edges = np.array([(i, j) for i in range(n) for j in range(i + 1, n)
                  if rng.random() < 0.15])
adj = [np.concatenate((edges[edges[:, 0] == v, 1], edges[edges[:, 1] == v, 0]))
       for v in range(n)]
state = ColoringConflicts(adj, rng.integers(0, k, n), k)
for _ in range(500):
    v, c = int(rng.integers(n)), int(rng.integers(k))
    if c != state.colors[v]:
        state.apply(v, c)
brute = int(np.sum(state.colors[edges[:, 0]] == state.colors[edges[:, 1]]))
assert state.total == brute
print(f"{state.total} conflicts; incremental count matches brute force")
# Expected: after 500 incremental recolors the maintained conflict count
# equals the O(|E|) recomputation exactly (integer arithmetic: no drift).
```

## Memoization and Solution Hashing

**When to use.** The objective is expensive (decoder, simulation, LP) **and** the search revisits
solutions: tabu search cycling near optima, ILS falling back into the same basin, GAs late in the
run when the population converges. **Complexity.** $O(\text{key})$ per lookup plus hashing; memory
bounded by the cache size. **Fits.** Any deterministic objective. Canonicalization is the part
people get wrong: hash a *canonical form*, not the raw array, whenever distinct encodings
represent the same solution:

| Encoding | Symmetries | Canonical key | Cost |
|---|---|---|---|
| Assignment permutation (QAP) | none | raw array bytes | $O(n)$ |
| Closed tour, symmetric TSP | $2n$ rotations/reflections | rotate city 0 first, fix direction | $O(n)$ |
| Binary subset (knapsack, SCP) | none | `np.packbits` bytes | $O(n)$ |
| Partition into unlabeled groups (coloring) | group relabeling | relabel groups by smallest member | $O(n \log n)$ |
| Multiset schedule with identical jobs | permuting identical jobs | sort within identical blocks | $O(n \log n)$ |

```python
import numpy as np
from collections import OrderedDict
from collections.abc import Callable


def canonical_tour_key(tour: np.ndarray) -> bytes:
    """Canonical key for a closed tour under rotation and reflection.

    Rotate city 0 to the front, then pick the direction whose second city
    has the smaller label: all 2n encodings map to one key.  O(n)."""
    start = int(np.argwhere(tour == 0)[0, 0])
    rot = np.roll(tour, -start)
    if rot[1] > rot[-1]:
        rot = np.concatenate((rot[:1], rot[1:][::-1]))
    return rot.astype(np.int32).tobytes()


class MemoizedEvaluator:
    """Bounded LRU memo around an expensive deterministic objective.

    Keyed by a canonical encoding so symmetric duplicates hit one entry;
    tracks hits/misses so the cache earns its memory or gets dropped."""

    def __init__(self, fn: Callable[[np.ndarray], float],
                 key_fn: Callable[[np.ndarray], bytes],
                 max_size: int = 100_000) -> None:
        self.fn, self.key_fn, self.max_size = fn, key_fn, max_size
        self.cache: OrderedDict[bytes, float] = OrderedDict()
        self.hits = 0
        self.misses = 0

    def __call__(self, x: np.ndarray) -> float:
        key = self.key_fn(x)
        if key in self.cache:
            self.cache.move_to_end(key)
            self.hits += 1
            return self.cache[key]
        value = self.fn(x)
        self.misses += 1
        self.cache[key] = value
        if len(self.cache) > self.max_size:
            self.cache.popitem(last=False)  # evict least recently used
        return value

    @property
    def hit_rate(self) -> float:
        """Fraction of calls answered from the cache."""
        total = self.hits + self.misses
        return self.hits / total if total else 0.0


rng = np.random.default_rng(5)
n = 50
pts = rng.uniform(0.0, 100.0, (n, 2))
d = np.hypot(pts[:, None, 0] - pts[None, :, 0], pts[:, None, 1] - pts[None, :, 1])


def tour_len(t: np.ndarray) -> float:
    """Closed-tour length.  O(n)."""
    return float(d[t, np.roll(t, -1)].sum())


memo = MemoizedEvaluator(tour_len, canonical_tour_key, max_size=10_000)
tour = rng.permutation(n)
v1 = memo(tour)
v2 = memo(np.roll(tour, 17))      # same tour, rotated start
v3 = memo(tour[::-1].copy())      # same tour, opposite direction
assert v1 == v2 == v3
print(f"hits={memo.hits} misses={memo.misses} hit_rate={memo.hit_rate:.2f}")
# Expected: hits=2 misses=1 hit_rate=0.67 -- all 2n encodings of one
# symmetric tour share a single cache entry.
```

### Zobrist hashing: O(1) incremental keys

Hashing the whole solution costs $O(n)$ per lookup — wasteful next to an $O(1)$ delta. Zobrist
hashing (Zobrist 1970, originally for game positions) XORs one random 64-bit code per
(position, value) pair, so one changed position updates the hash in $O(1)$, in lockstep with the
delta-updated solution; tabu search uses it for cycle detection, caches as the key.

```python
import numpy as np


class ZobristHash:
    """Incrementally updatable 64-bit hash for assignment-type solutions.

    h(x) = XOR_i Z[i, x[i]] with a fixed random table Z. update() is O(1)
    and self-inverse, so undoing a move restores the hash. Birthday bound:
    ~10^7 distinct solutions give collision probability near 3e-6 -- fine
    for caching and cycle detection, not for correctness proofs."""

    def __init__(self, n_positions: int, n_values: int, seed: int = 0) -> None:
        rng = np.random.default_rng(seed)
        self.table = rng.integers(0, 2**63, size=(n_positions, n_values), dtype=np.uint64)

    def full(self, x: np.ndarray) -> np.uint64:
        """Hash from scratch.  O(n)."""
        return np.bitwise_xor.reduce(self.table[np.arange(len(x)), x])

    def update(self, h: np.uint64, i: int, old: int, new: int) -> np.uint64:
        """Hash after position i changes old -> new.  O(1)."""
        return h ^ self.table[i, old] ^ self.table[i, new]


rng = np.random.default_rng(9)
n = 20
z = ZobristHash(n, n, seed=42)
p = rng.permutation(n)
h = z.full(p)
i, j = 3, 11
h2 = z.update(z.update(h, i, int(p[i]), int(p[j])), j, int(p[j]), int(p[i]))
q = p.copy()
q[[i, j]] = q[[j, i]]
assert h2 == z.full(q)
assert h == z.update(z.update(h2, i, int(q[i]), int(q[j])), j, int(q[j]), int(q[i]))
print(f"hash {int(h):#018x} -> {int(h2):#018x} via two O(1) updates")
# Expected: the incrementally updated hash equals the from-scratch hash of
# the swapped permutation, and undoing the swap restores the original hash.
```

## Batch, Surrogate, and Parallel Evaluation

### Vectorized batch evaluation

**When to use.** Population methods (GA, EDA, PSO-style discrete variants, multi-start) with an
algebraic objective. **Complexity.** Same asymptotics as the loop, but 10-100x smaller constants
via SIMD and no interpreter overhead. **Fits.** Knapsack-type linear objectives (one matrix
product), QAP (fancy indexing + `einsum`), distance-based objectives. See
**numpy-vectorization-for-optimization** for the underlying array techniques.

```python
import numpy as np


def qap_batch(perms: np.ndarray, a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Evaluate m QAP permutations at once.  O(m n^2) time AND memory.

    Fancy indexing builds b[perm[i], perm[j]] for every member; einsum
    contracts against the flow matrix. Memory check: m=512, n=100 already
    allocates 512*100*100*8 B = 41 MB -- chunk the population if needed."""
    bp = b[perms[:, :, None], perms[:, None, :]]          # (m, n, n)
    return np.einsum("ij,mij->m", a, bp)


def knapsack_batch(pop: np.ndarray, values: np.ndarray, weights: np.ndarray,
                   capacity: float, penalty: float) -> np.ndarray:
    """Penalized 0-1 knapsack fitness for a binary population.  O(m n).

    Two matrix-vector products evaluate the whole population; no Python
    loop. Fits genetic algorithms and EDAs on binary encodings."""
    value = pop @ values
    overload = np.maximum(pop @ weights - capacity, 0.0)
    return value - penalty * overload


rng = np.random.default_rng(6)
n, m = 40, 256
a = rng.integers(0, 10, (n, n)).astype(float)
b = rng.integers(0, 10, (n, n)).astype(float)
perms = rng.permuted(np.tile(np.arange(n), (m, 1)), axis=1)
batch = qap_batch(perms, a, b)
loop = np.array([float(np.sum(a * b[np.ix_(p, p)])) for p in perms])
assert np.allclose(batch, loop)
vals, wts = rng.uniform(1, 10, 80), rng.uniform(1, 10, 80)
pop = (rng.random((m, 80)) < 0.3).astype(float)
fit = knapsack_batch(pop, vals, wts, capacity=float(wts.sum()) * 0.25, penalty=50.0)
print(f"QAP batch matches loop; knapsack best penalized fitness {fit.max():.1f}")
# Expected: batch values equal the loop exactly; one einsum call replaces
# 256 full evaluations (typically 20-50x faster at this size).
```

### Surrogate and sampled (screening) evaluation

**When to use.** One exact evaluation costs ≳10 ms (simulation, heavy decoder, embedded solve) and
the search only needs *ranking* fidelity, not exact values, for most candidates. **Complexity.**
Proxy cost per candidate plus exact cost on the surviving fraction. **Fits.** Population methods
(screen each generation) and construction methods (screen candidate pools); see Jin (2005), "A
comprehensive survey of fitness approximation in evolutionary computation." The robust pattern is
*screening*: rank everyone with a cheap correlated proxy, evaluate the best fraction exactly, and
calibrate the rest so the two scales mix consistently.

```python
import numpy as np
from collections.abc import Callable


class ScreeningEvaluator:
    """Two-stage (multi-fidelity) evaluation for minimization.

    Stage 1 scores every candidate with a cheap proxy. Stage 2 evaluates
    the best keep_frac exactly; the others get the proxy mapped through
    a least-squares linear calibration fitted on the exact subset, so
    both scales mix. Re-evaluate any reported solution exactly."""

    def __init__(self, exact_fn: Callable[[np.ndarray], float],
                 proxy_fn: Callable[[np.ndarray], float],
                 keep_frac: float = 0.25) -> None:
        self.exact_fn, self.proxy_fn, self.keep_frac = exact_fn, proxy_fn, keep_frac
        self.exact_calls = 0
        self.proxy_calls = 0

    def evaluate_population(self, pop: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """Return (fitness, exact_mask) for the rows of pop."""
        m = len(pop)
        proxy = np.array([self.proxy_fn(x) for x in pop])
        self.proxy_calls += m
        n_exact = max(2, int(np.ceil(self.keep_frac * m)))
        elite = np.argsort(proxy)[:n_exact]
        exact_vals = np.array([self.exact_fn(pop[i]) for i in elite])
        self.exact_calls += n_exact
        slope, intercept = np.polyfit(proxy[elite], exact_vals, deg=1)
        fitness = slope * proxy + intercept
        fitness[elite] = exact_vals
        exact_mask = np.zeros(m, dtype=bool)
        exact_mask[elite] = True
        return fitness, exact_mask


rng = np.random.default_rng(8)
n, m = 40, 200
a = rng.integers(0, 10, (n, n)).astype(float)
b = rng.integers(0, 10, (n, n)).astype(float)
pop = rng.permuted(np.tile(np.arange(n), (m, 1)), axis=1)


def qap_exact(p: np.ndarray) -> float:
    """Full objective.  O(n^2)."""
    return float(np.sum(a * b[np.ix_(p, p)]))


def make_sampled_proxy(sub: np.ndarray) -> Callable[[np.ndarray], float]:
    """Proxy = objective restricted to index sample sub.  O(|S|^2) per call."""
    def proxy(p: np.ndarray) -> float:
        ps = p[sub]
        return float(np.sum(a[np.ix_(sub, sub)] * b[np.ix_(ps, ps)]))
    return proxy


def ranks(v: np.ndarray) -> np.ndarray:
    """Rank vector of v (0 = smallest)."""
    return np.argsort(np.argsort(v))


truth = np.array([qap_exact(p) for p in pop])     # for validation only
for size in (n // 3, n // 2, 3 * n // 4):         # ALWAYS audit proxy fidelity
    pv = np.array([make_sampled_proxy(rng.choice(n, size, replace=False))(p) for p in pop])
    rho = float(np.corrcoef(ranks(truth), ranks(pv))[0, 1])
    print(f"|S|={size}: proxy cost {size * size / (n * n):.0%} of exact, rank corr {rho:.2f}")
screener = ScreeningEvaluator(qap_exact, make_sampled_proxy(
    rng.choice(n, size=3 * n // 4, replace=False)), keep_frac=0.2)
fitness, exact_mask = screener.evaluate_population(pop)
overlap = len(set(np.argsort(truth)[:10].tolist()) & set(np.argsort(fitness)[:10].tolist()))
print(f"exact calls {screener.exact_calls}/{m}, top-10 overlap {overlap}/10")
# Expected: correlation improves with sample size but stays modest and
# seed-noisy (about 0.15 at 11% cost up to 0.35-0.5 at 56%): QAP values
# concentrate on random populations, so cheap samples rank weakly. The
# fidelity audit is the point -- pick the cheapest proxy whose correlation
# supports your keep_frac, raise keep_frac when it sags, and always re-rank
# reported elites exactly.
```

### Parallel evaluation

**When to use.** Per-evaluation cost is large relative to inter-process dispatch (~0.1-1 ms per
task after chunking) and evaluations are independent. **Complexity.** Wall-clock divided by up to
the core count; total CPU work unchanged. **Fits.** Population methods (embarrassingly parallel
generations), multi-start, parallel neighborhood scans. For parallelizing the *search* rather than
the evaluator — island models, cooperative threads — see **parallel-and-hybrid-metaheuristics**.

```python
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np


def expensive_objective(x: np.ndarray) -> float:
    """Stand-in for a costly black-box evaluation (~5 ms of work)."""
    deadline = time.perf_counter() + 0.005
    acc = 0.0
    while time.perf_counter() < deadline:
        acc += float(np.sum(np.sort(x))) * 1e-12
    return float(np.sum(x * x)) + acc


def evaluate_parallel(pop: np.ndarray, workers: int, chunk: int) -> np.ndarray:
    """Evaluate rows of pop in worker processes.

    chunksize amortizes pickling/dispatch overhead. On Windows/macOS the
    start method is 'spawn': the objective MUST be module-level and pool
    creation MUST sit under the __main__ guard. Ship large read-only
    instance data via an initializer or shared memory, never per task."""
    with ProcessPoolExecutor(max_workers=workers) as pool:
        results = pool.map(expensive_objective, pop, chunksize=chunk)
        return np.fromiter(results, dtype=float, count=len(pop))


if __name__ == "__main__":
    rng = np.random.default_rng(11)
    pop = rng.normal(size=(64, 50))
    t0 = time.perf_counter()
    serial = np.array([expensive_objective(x) for x in pop])
    t_serial = time.perf_counter() - t0
    t0 = time.perf_counter()
    parallel = evaluate_parallel(pop, workers=4, chunk=8)
    t_parallel = time.perf_counter() - t0
    assert np.allclose(serial, parallel, rtol=1e-6, atol=1e-6)
    print(f"serial {t_serial:.2f}s, parallel {t_parallel:.2f}s")
    # Expected: identical values; at this tiny scale pool startup (0.5-2 s on
    # spawn platforms) can erase the win -- the speedup approaches
    # min(workers, cores) only when per-eval cost x population size dwarfs it.
```

## Advanced Techniques

### Fitness inheritance and partial evaluation in population methods

Fitness inheritance (Smith, Dike & Stegmann 1995) assigns a fraction of offspring the weighted
average of parent fitnesses instead of an exact evaluation: 30-50% fewer evaluations, but biased
selection. Cap the inherited fraction near 0.5, evaluate elites exactly, and never report an
inherited value as a result. For decoder-based representations the sharper tool is *partial
re-decoding*: when a crossover preserves a segment, decode only the changed part and reuse cached
partial objective state — the decoder analogue of delta evaluation.

### Caching for stochastic objectives

A noisy objective makes a single cached sample a lie. Cache the *sufficient statistics* instead:
key → (mean, sample count, M2) updated with Welford's online algorithm; a cache hit then means
"add samples or reuse the mean" depending on the comparison at hand. Allocate re-sampling effort
where it changes decisions — candidates whose confidence intervals overlap the incumbent —
following optimal computing budget allocation (Chen, Lin, Yücesan & Chick 2000). Never mix values
with different sample counts in tournament selection without noting the variance difference.

### Cache policy and collision management

Unbounded caches leak memory at exactly the moment long runs need it. Use a bounded LRU (as in
`MemoizedEvaluator`) for trajectory methods, or generation-scoped clearing for GAs where revisits
concentrate within a few generations. Store fixed-size digests (Zobrist value, `blake2b` of the
canonical bytes) as keys rather than full solution arrays — at $n = 1000$ a raw-array key costs
8 kB per entry versus 16 B for a digest. With 64-bit keys, plan for collisions: store a second
independent checksum and verify on hit, or accept the ~$2^{-64}$ per-pair risk explicitly. For
population dedup, exact byte keys are safer — false merges silently shrink diversity.

### Surrogate management loops

A static surrogate goes stale as the search moves into new regions. Maintain an archive of
(solution, exact value) pairs, retrain every $g$ generations on the recent slice, and apply
*evolution control* (Jin 2005): individual-based (always evaluate the predicted-best $k$ exactly)
or generation-based (every $g$-th generation fully exact). Track the rank correlation between
surrogate and exact values on each exact batch; below ~0.5, raise the exact fraction. Screen with
an optimism margin — keep candidates within one surrogate standard error of the cutoff, not just
the point-estimate elite.

### Delta correctness under adaptive penalties

Guided local search (Voudouris & Tsang 1999) and adaptive constraint handling change penalty
weights *during* the run, silently invalidating every cached fitness and delta table built on the
weighted objective. Two safe designs: (1) store objectives as component vectors (raw cost, each
violation measure) and apply weights only at comparison time, so caches survive weight changes; or
(2) version the weights and flush/rebuild caches and tables on every update. Mixing stale and
fresh weighted values is the classic source of "the search accepts moves it should reject" bugs.

## Practical Challenges

**Delta and full evaluation drift apart after thousands of moves.** Floating-point deltas
accumulate rounding error. Resynchronize: every $K$ moves (e.g., 10^4) recompute the objective
from scratch, log the discrepancy, and alert above tolerance. With integer cost data, do all delta
arithmetic in `int64` — exact forever, no resync needed.

**Cache hit rate is near zero.** Diverse populations almost never revisit solutions, so a memo on
a GA's objective is pure overhead. Memoize where revisits actually happen: inside the local search
of a memetic algorithm, in tabu cycle detection, or at the decoder layer where many genotypes map
to one phenotype. Always measure `hit_rate` before keeping the cache.

**The cache eats all memory.** Full solutions stored as keys at scale pin gigabytes. Switch keys
to digests, bound the cache, and store scalars (objective, feasibility flag) rather than solution
copies; elite archives keep solutions once in a pool and reference by index.

**Parallel evaluation is slower than serial.** Causes, in order of likelihood: per-task cost below
dispatch overhead (fix with `chunksize` or batched tasks), instance data pickled into every task
(fix with a pool initializer or shared memory; fork on Linux shares read-only data for free), and
oversubscription against numpy's own threads (set `OMP_NUM_THREADS=1` in workers). Vectorize
before parallelizing — a 50x einsum beats 8 cores of slow loops.

**The surrogate misleads the search.** Symptom: exact re-evaluation of "improvements" shows none.
Monitor proxy-exact rank correlation on every exact batch; shrink the surrogate's responsibility
(higher keep_frac, more retraining) when it degrades, and re-rank final elites exactly.

**A new objective term silently breaks delta evaluation.** Someone adds a soft constraint to
`full()` but not to `delta()`; the search optimizes a ghost objective. Make the randomized
invariant `delta(s, m) == full(apply(s, m)) - full(s)` a CI test over every move type and commit.

**Profiling shows evaluation is not the bottleneck — copying is.** The
`cand = tour.copy()`-per-candidate pattern dominates once the evaluator is fast. Score moves from
`(s, move)` without materializing the neighbor, and use apply/undo: apply the move in place,
evaluate, undo (both $O(\text{move})$) when scoring genuinely requires the mutated state.

## Tools & Libraries

| Library / tool | When to use | Note |
|---|---|---|
| `cProfile` + `pstats` | first step on any "my search is slow" report | function-level attribution; sort by `tottime` |
| `line_profiler` | the hot function is known, the hot line is not | decorator-based, line-level timings |
| `numpy` | batch evaluation, delta tables, vectorized aggregates | the default substrate for everything here |
| `numba` (`@njit`) | per-move deltas with unavoidable Python loops | 10-100x on scalar loop code; JIT warmup applies |
| `functools.lru_cache` | quick memo on hashable-argument functions | needs tuple/bytes keys, no canonicalization or stats |
| `hashlib.blake2b` / `xxhash` | digest keys for large solutions | xxhash is fastest; blake2b ships with Python |
| `concurrent.futures` | process-parallel evaluation, standard library | `chunksize` matters; spawn semantics on Windows |
| `joblib.Parallel` | parallel sweeps with memory-mapped numpy arrays | also provides disk-backed `Memory` caching |
| `multiprocessing.shared_memory` | large read-only instance data across workers | avoids per-task pickling of matrices |
| `scikit-learn` | regression surrogates (RF, GP) over solution features | pair with an evolution-control loop |

## Output Format

A complete evaluation-speedup deliverable contains:

1. **Profiling evidence (before).** Where time went, from `cProfile` or counters:

   | Component | Share of runtime | Calls | Mean cost |
   |---|---|---|---|
   | objective evaluation | 91% | 2.1e6 | 38 us |
   | neighbor copying + search logic | 9% | 2.1e6 | 2.5 us |

2. **Technique decision.** Which hierarchy level was applied and why (move structure, objective
   separability, hardware), plus the techniques rejected and the reason.

3. **Correctness harness.** The randomized delta-vs-full invariant test for every move type, the
   FP tolerance, and the resynchronization policy (period, observed drift). For caches: the
   canonicalization rule and the collision policy.

4. **Speedup report (after).** Same workload, before vs after:

   | Variant | Evals/s | Time to target quality | Speedup |
   |---|---|---|---|
   | full recomputation | 2.6e4 | 312 s | 1.0x |
   | O(n) delta | 8.1e5 | 9.8 s | 32x |
   | delta table + tabu scan | 6.4e6 | 1.3 s | 240x |

5. **Cache statistics** when memoization is used: hits, misses, hit rate, entries, memory,
   eviction policy — and the recommendation to drop the cache below a ~5% hit rate.

6. **Exactness statement** when surrogates or sampling are used: which reported numbers are
   exact, the measured proxy-exact rank correlation, and confirmation that all final solutions
   were re-evaluated with the exact objective.

## Questions to Ask

- How long does one evaluation take now, and what is the total time budget for a run?
- What does the profiler say — is evaluation really the bottleneck, and which part of it?
- Which solution components does one move change? Is the objective a sum of local terms?
- Is the objective deterministic, or does it involve simulation noise?
- Are the cost data integers (exact deltas) or floats (drift and resync policy needed)?
- Does the search revisit solutions — what hit rate would a cache actually see?
- How much memory can caches and delta tables use at the target instance size?
- How many cores are available, and is the objective picklable / process-safe?
- Is approximate ranking acceptable during search if final results are re-evaluated exactly?
- Which encoding symmetries (rotations, reflections, relabelings) must a cache key canonicalize?

## Related Skills

- **local-search-and-neighborhoods** — when the question is which moves and neighborhoods to use
  rather than how to price them; delta evaluation is designed around the move set chosen there.
- **numpy-vectorization-for-optimization** — when batch evaluation needs array-level redesign:
  broadcasting, fancy indexing, einsum, and memory-layout tuning.
- **tabu-search** — the canonical consumer of delta tables and incremental hashing: best-improvement
  scans over all moves with attribute-based memory and aspiration checks.
- **parallel-and-hybrid-metaheuristics** — when speeding up one evaluator is not enough and the
  search itself should run in parallel (island models, cooperative searches, hybrid schemes).
