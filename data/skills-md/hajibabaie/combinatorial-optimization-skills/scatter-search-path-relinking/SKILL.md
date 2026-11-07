---
name: scatter-search-path-relinking
description: When the user wants to implement scatter search (reference set management, diversification generation, subset combination, improvement method) or path relinking as intensification between elite solutions, standalone or inside GRASP. Also use when the user mentions "scatter search," "path relinking," "reference set," "RefSet," "elite solutions," "solution combination," "relinking," or when a small, explicitly managed elite population should replace a large stochastic one. For greedy randomized construction and multi-start, see grasp; for large-population recombination, see genetic-algorithms.
---

# Scatter Search and Path Relinking

You are an expert in memory-based metaheuristics, specializing in scatter search and
path relinking. This skill covers the five-method scatter search template —
diversification generation, improvement, reference set update, subset generation,
solution combination — and path relinking as an intensification mechanism between
elite solutions, both standalone and inside GRASP or tabu search. Use the framework
below to decide when these methods fit, implement them in clean numpy, and report
results that withstand reviewer scrutiny.

## Initial Assessment

Establish the following before proposing or writing any code:

- **Representation and distance.** What is a solution (binary vector, permutation,
  assignment), and what dissimilarity metric is natural (Hamming, swap distance)?
  Scatter search needs an explicit distance for the diversity half of the RefSet;
  path relinking needs a move that brings a solution one unit closer to a guiding
  solution — if no such move exists, the method does not apply.
- **Objective sense.** Minimization or maximization; fix one convention internally
  and convert at the boundary. Sign errors in admission rules are the most common
  scatter search bug.
- **Improvement method.** Which local search improves trial solutions, and what one
  descent costs — scatter search calls it on every combined trial; budget it. The
  QAP example below shows the delta-evaluation pattern.
- **Feasibility along paths.** Can intermediate solutions on a relinking path be
  infeasible? Decide up front: restrict moves to feasible ones, allow infeasible
  steps and record only feasible interiors, or repair every candidate.
- **Elite source.** Full scatter search, or path relinking bolted onto an existing
  method (GRASP, tabu search, a GA) that already collects elites? The second is far
  cheaper to add and often captures most of the benefit.
- **Instance size.** Solution length n, reference set size b, and pool size P
  determine the per-round cost: O(b^2) combinations, each followed by an
  improvement run.
- **Time budget, stopping rule, quality requirement.** Wall-clock or evaluation
  budget; how many rebuild rounds it allows; target gap to best-known values;
  single best solution or a distribution over seeds.
- **Exact-vs-heuristic need.** If a MIP solver closes the gap within the budget,
  solve exactly; use these methods for larger instances or as warm starts.
- **Baselines.** Plain multi-start with the same improvement method is the honest
  baseline; a GA at the same budget is the standard population comparison.
- **Reproducibility.** One `np.random.default_rng(seed)` per run; record seeds,
  reference set sizes, and admission rules in every result table.

## Algorithm Anatomy

Scatter search dates to Glover (1977, "Heuristics for integer programming using
surrogate constraints"); the modern template is Glover (1998, "A template for
scatter search and path relinking") and Glover, Laguna & Martí (2000, "Fundamentals
of scatter search and path relinking"), with the book-length treatment in Laguna &
Martí (2003, "Scatter Search: Methodology and Implementations in C"). Path
relinking originates in the tabu search literature (Glover & Laguna 1997, "Tabu
Search") and entered GRASP through Laguna & Martí (1999); the joint survey is
Resende, Ribeiro, Glover & Martí (2010, "Scatter search and path-relinking:
fundamentals, advances, and applications," Handbook of Metaheuristics).

**The five-method template.** Every scatter search instantiates:

1. **Diversification generation method** — builds a pool $P$ spread over the
   search space, using frequency memory or systematic construction, not uniform
   sampling.
2. **Improvement method** — a local search applied to pool members and to every
   combined trial solution.
3. **Reference set update method** — maintains the RefSet $R$ of $b = b_1 + b_2$
   solutions, $b_1$ by quality, $b_2$ by diversity; admission and replacement
   rules live here.
4. **Subset generation method** — selects subsets of $R$ to combine; in practice,
   all 2-element subsets containing at least one new member.
5. **Solution combination method** — maps a subset to trial solutions through
   structured combination (linear combinations, vote-merging, path relinking),
   not generic random crossover.

**Reference set construction.** From the improved pool, take the $b_1$ best by
cost; then fill the $b_2$ diversity slots greedily by max-min distance:

$$
x^{*} \;=\; \arg\max_{x \in P \setminus R} \; \min_{r \in R} \; d(x, r).
$$

Typical sizes: $b = 10$ with $b_1 = b_2 = 5$, pool $P$ of 50–100. The RefSet is
small and deterministic by design: scatter search replaces selection pressure
with explicit quality-plus-diversity membership, and random crossover with
purposeful combination — the defining contrast with genetic algorithms.

**The main loop.** Combine every subset with a new member, improve each trial,
and admit improving trials into $R$ (replace-worst, or a two-tier rule — see
Advanced Techniques). When a full pass admits nothing the RefSet has converged:
keep the $b_1$ best, refresh the diversity half from a fresh pool, and repeat.

**Path relinking.** Given an initiating solution $x_s$ and a guiding solution
$x_t$, relinking walks through the neighborhood graph using only moves that reduce
the distance to the guide:

$$
N_{\mathrm{PR}}(s, x_t) \;=\; \{\, s' \in N(s) \;:\; d(s', x_t) < d(s, x_t) \,\},
$$

choosing at each step the candidate with the best objective. A path from Hamming
distance $h$ has $h$ steps for bit-flip moves (at most $h - 1$ swaps for
permutations) and visits interior solutions sharing the common structure of both
endpoints — where good solutions cluster under the proximate-optimality
assumption. The best interior point is returned and usually polished with the
improvement method. Step $k$ evaluates $h - k + 1$ candidates, so a full relink
costs $O(h^2)$ candidate evaluations — use delta evaluation where it exists.

**Relinking variants** (Resende & Ribeiro 2005, "GRASP with path-relinking: recent
advances and applications"):

| Variant | Path | When to use |
|---|---|---|
| Forward | worse endpoint → better | Simplest baseline |
| Backward | better endpoint → worse | Default: early steps, where freedom is largest, happen near the good endpoint; empirically stronger |
| Back-and-forward | both directions | Doubles cost for a small extra gain |
| Mixed | alternate one step from each end | Explores both endpoint basins at the cost of one direction |
| Truncated | first 20–40% of the path | Improvements concentrate near the initiating endpoint |
| Greedy randomized | RCL step choice instead of argmin | When PR runs many times per search and needs diversity |
| Exterior | moves that increase distance beyond an endpoint | Extrapolation past the segment (Glover 2014, "Exterior path relinking for zero-one optimization") |
| Evolutionary | relink all elite pairs, repeat until no change | Post-processing intensification (Resende & Werneck 2004, "A hybrid heuristic for the p-median problem") |

**Decision guidance.**

- Use path relinking whenever a method already maintains elites: it converts any
  multi-start into a memory-based search for a few dozen lines of code. Inside
  GRASP it is the standard upgrade (see **grasp**).
- Use full scatter search when structured combination is meaningful for the
  representation (rounded linear combinations, vote-merging, relinking) and a
  small intensively-managed population fits the budget better than a large one.
- Prefer a GA when the representation has well-studied crossover operators and
  large-population diversity is easier to maintain than to engineer — see
  **genetic-algorithms**.
- Prefer plain multi-start when elites are so scattered that paths between them
  cross only poor regions; measure interior-improvement rates to check.

**Complexity.** One scatter search round combines $O(b^2)$ subsets; with $b = 10$
that is at most 45 relinks plus 45 improvement runs. The improvement method
dominates in practice. Path relinking itself is cheap: a trajectory scan, not a
second search.

## Scatter Search: Generic Framework

The skeleton shared by every scatter search:

```text
ScatterSearch(b1, b2, pool_size, max_rebuilds):
    P      <- pool_size solutions from DiversificationGeneration, each Improved
    RefSet <- b1 best of P  +  b2 max-min-diverse of P     # all marked new
    repeat max_rebuilds + 1 times:
        while RefSet has a new member:                     # combination phase
            Subsets <- all pairs with at least one new member; clear new flags
            for each (x, y) in Subsets:
                for t in Combine(x, y):
                    t <- Improve(t)
                    if cost(t) < worst RefSet cost and t not in RefSet:
                        replace worst member by t; mark t new
        keep b1 best of RefSet                             # rebuild
        refresh diversity half from a fresh improved pool
    return best solution seen
```

The framework below is problem-independent: the five methods arrive as callables,
so the same loop serves both worked examples.

```python
import numpy as np
from collections.abc import Callable


def select_refset(pool: list[np.ndarray], costs: np.ndarray,
                  distance: Callable[[np.ndarray, np.ndarray], float],
                  b1: int, b2: int) -> list[int]:
    """RefSet build: b1 best-cost pool indices + b2 by greedy max-min distance."""
    order = np.argsort(costs)
    chosen = [int(i) for i in order[:b1]]
    rest = [int(i) for i in order[b1:]]
    while len(chosen) < b1 + b2 and rest:
        dmin = np.array([min(distance(pool[i], pool[j]) for j in chosen)
                         for i in rest])
        chosen.append(rest.pop(int(np.argmax(dmin))))
    return chosen


def scatter_search(
    diversify: Callable[[np.random.Generator], np.ndarray],
    improve: Callable[[np.ndarray], np.ndarray],
    combine: Callable[[np.ndarray, np.ndarray, np.random.Generator],
                      list[np.ndarray]],
    cost: Callable[[np.ndarray], float],
    distance: Callable[[np.ndarray, np.ndarray], float],
    b1: int = 5, b2: int = 5, pool_size: int = 50,
    max_rebuilds: int = 3, seed: int = 0,
) -> tuple[np.ndarray, float]:
    """Scatter search template (Glover, Laguna & Marti 2000).

    The five methods are injected: diversify builds one diverse solution,
    improve is the local search, combine maps a RefSet pair to trial
    solutions, distance feeds the diversity half of the RefSet.
    """
    rng = np.random.default_rng(seed)
    pool = [improve(diversify(rng)) for _ in range(pool_size)]
    pool_costs = np.array([cost(x) for x in pool])
    idx = select_refset(pool, pool_costs, distance, b1, b2)
    refset = [pool[i].copy() for i in idx]
    ref_costs = [float(pool_costs[i]) for i in idx]
    is_new = [True] * len(refset)
    k = int(np.argmin(ref_costs))
    best, best_cost = refset[k].copy(), ref_costs[k]

    for rebuild in range(max_rebuilds + 1):
        while any(is_new):                       # combination phase
            pairs = [(refset[i].copy(), refset[j].copy())
                     for i in range(len(refset))
                     for j in range(i + 1, len(refset))
                     if is_new[i] or is_new[j]]
            is_new = [False] * len(refset)
            for x, y in pairs:
                for t in combine(x, y, rng):
                    t = improve(t)
                    ct = cost(t)
                    w = int(np.argmax(ref_costs))
                    if (ct < ref_costs[w] - 1e-12
                            and all(distance(t, r) > 1e-9 for r in refset)):
                        refset[w], ref_costs[w], is_new[w] = t.copy(), ct, True
                        if ct < best_cost:
                            best, best_cost = t.copy(), ct
        if rebuild == max_rebuilds:
            break
        order = np.argsort(ref_costs)[:b1]       # rebuild: keep quality half
        keep = [refset[i] for i in order]
        keep_costs = [ref_costs[i] for i in order]
        fresh = [improve(diversify(rng)) for _ in range(pool_size)]
        pool = keep + fresh
        pool_costs = np.array(keep_costs + [cost(x) for x in fresh])
        idx = select_refset(pool, pool_costs, distance, b1, b2)
        refset = [pool[i].copy() for i in idx]
        ref_costs = [float(pool_costs[i]) for i in idx]
        is_new = [i >= len(keep) for i in idx]   # fresh members drive new pairs
    return best, best_cost


# Tiny wiring check: recover a hidden binary target from Hamming-distance cost.
_target = np.array([1, 0, 1, 1, 0, 0, 1, 0, 1, 1], dtype=bool)

def _toy_improve(x: np.ndarray) -> np.ndarray:
    """Deliberately weak improvement: repair one disagreeing bit per call."""
    x = x.copy()
    wrong = np.flatnonzero(x != _target)
    if len(wrong):
        x[wrong[0]] = _target[wrong[0]]
    return x

def _toy_combine(x: np.ndarray, y: np.ndarray,
                 rng: np.random.Generator) -> list[np.ndarray]:
    """Keep agreements, randomize disagreements -- one trial per pair."""
    return [np.where(x == y, x, rng.random(len(x)) < 0.5).astype(bool)]

best, best_cost = scatter_search(
    diversify=lambda rng: rng.random(10) < 0.5,
    improve=_toy_improve,
    combine=_toy_combine,
    cost=lambda x: float(np.sum(x != _target)),
    distance=lambda a, b: float(np.sum(a != b)),
    b1=3, b2=3, pool_size=12, max_rebuilds=2, seed=0)
print(best_cost)
# Expected: 0.0 -- combination of agreeing bits plus the weak one-bit repair
# reconstructs the target; the check exercises every branch of the loop.
```

### Parameter guidance

| Parameter | Typical range | Trade-off |
|---|---|---|
| `b1` (quality slots) | 5–8 | More quality slots intensify; fewer leave room for diversity-driven combinations |
| `b2` (diversity slots) | 3–5 (b = b1+b2 ≈ 10, rarely > 20) | Larger b2 widens coverage but adds weak members to every combination round |
| `pool_size` | 5–10 × b (50–100) | Bigger pools give a better RefSet build at linear extra improvement cost |
| `max_rebuilds` | 3–10 or budget-driven | Each rebuild restarts exploration; returns diminish once elites stop changing |
| Subset type | All 2-element subsets | Triples and larger subsets (Glover 1998 types 2–4) rarely pay for their extra combinations |
| Trials per combination | 1–3 | More trials per pair deepen the scan of one pair at the cost of fewer pairs per budget |
| PR variant in combine | Backward, then try truncated | See the variants table above |
| Truncation fraction | 0.2–0.4 | Shorter scans cut cost; most interior improvements sit near the initiating endpoint |
| Improvement policy | Improve every trial; or only trials beating the worst RefSet cost before improvement | Full improvement is the quality driver and the runtime sink |
| Admission rule | Replace worst (quality-only) or two-tier | Two-tier keeps diversity alive; quality-only converges faster but risks clone collapse |

Distance metrics, duplicate detection, and diversity measurement are treated in
depth in **diversity-and-population-management**; combination operators for
specific encodings belong to the operator skills referenced there.

## Path Relinking: Generic Framework

```text
PathRelink(start, guide, truncate):
    s <- start;  best <- none
    while s differs from guide in more than one move:
        C <- all solutions one move closer to guide        # N_PR(s, guide)
        s <- argmin_{c in C} cost(c)                       # greedy step
        if s is interior (s != guide) and cost(s) < cost(best): best <- s
        stop early after truncate * initial_distance steps
    return best interior point                             # then Improve(best)
```

The driver below is representation-independent: a `steps_toward` callable
enumerates the one-move-closer candidates. Bit flips for binary vectors and
repairing swaps for permutations cover most combinatorial representations.

```python
import numpy as np
from collections.abc import Callable


def path_relink(start: np.ndarray, guide: np.ndarray,
                cost: Callable[[np.ndarray], float],
                steps_toward: Callable[[np.ndarray, np.ndarray],
                                       list[np.ndarray]],
                truncate: float = 1.0) -> tuple[np.ndarray | None, float]:
    """Greedy path relinking from start toward guide (minimization).

    steps_toward(s, guide) returns every solution one move closer to the
    guide. Returns the best strictly interior point and its cost, or
    (None, inf) when the path has no interior. Apply the improvement
    method to the returned point, not to every step.
    """
    s = start.copy()
    best, best_cost = None, np.inf
    cands = steps_toward(s, guide)
    h0, steps = len(cands), 0
    while cands and steps < truncate * h0:
        vals = [cost(c) for c in cands]
        k = int(np.argmin(vals))
        s = cands[k]
        steps += 1
        cands = steps_toward(s, guide)
        if cands and vals[k] < best_cost:        # interior points only
            best, best_cost = s.copy(), vals[k]
    return best, best_cost


def binary_steps(s: np.ndarray, guide: np.ndarray) -> list[np.ndarray]:
    """One-flip moves toward the guide: fix one disagreeing bit."""
    out = []
    for j in np.flatnonzero(s != guide):
        t = s.copy()
        t[j] = guide[j]
        out.append(t)
    return out


def perm_steps_toward(s: np.ndarray, guide: np.ndarray) -> list[np.ndarray]:
    """Repairing swaps toward the guide: put guide[a] into position a."""
    out = []
    for a in np.flatnonzero(s != guide):
        b = int(np.flatnonzero(s == guide[a])[0])
        t = s.copy()
        t[a], t[b] = t[b], t[a]
        out.append(t)
    return out


# Tiny check: walk from all-zeros to all-ones; cost is lowest with exactly
# two ones, so the best interior point must score 0.
start = np.zeros(6, dtype=bool)
guide = np.ones(6, dtype=bool)
best, c = path_relink(start, guide,
                      cost=lambda x: float(abs(int(x.sum()) - 2)),
                      steps_toward=binary_steps)
print(int(best.sum()), c)
# Expected: 2 0.0 -- the path adds one item per step and the relink keeps
# the interior point with two ones.
```

## Worked Example 1: QAP Scatter Search

The quadratic assignment problem (QAP): given a symmetric flow matrix $F$ and
distance matrix $D$ (zero diagonals), find a permutation $\pi$ (facility $\to$
location) minimizing

$$
\min_{\pi} \; \sum_{a=1}^{n} \sum_{b=1}^{n} F_{ab} \, D_{\pi(a)\pi(b)}.
$$

QAP was an early scatter search showcase (Cung, Mautor, Michelon & Tavares 1997,
"A scatter search based approach for the quadratic assignment problem"). For
models, bounds, and benchmark instances see **quadratic-assignment-problem**.
Base ingredients: instance generator, objective, the $O(n)$ swap delta, and a
best-improvement 2-exchange descent as the improvement method:

```python
import numpy as np


def generate_qap(n: int, seed: int) -> tuple[np.ndarray, np.ndarray]:
    """Symmetric random QAP: integer flows F, Euclidean distances D, zero diagonals."""
    rng = np.random.default_rng(seed)
    F = np.triu(rng.integers(0, 10, (n, n)), k=1).astype(float)
    F = F + F.T
    pts = rng.random((n, 2)) * 100.0
    D = np.hypot(pts[:, None, 0] - pts[None, :, 0],
                 pts[:, None, 1] - pts[None, :, 1])
    return F, D


def qap_cost(perm: np.ndarray, F: np.ndarray, D: np.ndarray) -> float:
    """sum_{a,b} F[a,b] * D[perm[a], perm[b]]  (perm maps facility -> location)."""
    return float((F * D[np.ix_(perm, perm)]).sum())


def swap_delta(perm: np.ndarray, F: np.ndarray, D: np.ndarray,
               a: int, b: int) -> float:
    """O(n) cost change for swapping the locations of facilities a and b."""
    mask = np.ones(len(perm), dtype=bool)
    mask[[a, b]] = False
    pk = perm[mask]
    u, v = perm[a], perm[b]
    return float(2.0 * ((F[a, mask] - F[b, mask]) * (D[v, pk] - D[u, pk])).sum())


def two_exchange(perm: np.ndarray, F: np.ndarray, D: np.ndarray) -> np.ndarray:
    """Best-improvement 2-exchange descent using O(n) swap deltas."""
    perm = perm.copy()
    n = len(perm)
    while True:
        best_d, best_pair = -1e-9, None
        for a in range(n - 1):
            for b in range(a + 1, n):
                d = swap_delta(perm, F, D, a, b)
                if d < best_d:
                    best_d, best_pair = d, (a, b)
        if best_pair is None:
            return perm
        a, b = best_pair
        perm[a], perm[b] = perm[b], perm[a]
```

Two scatter-search-specific pieces remain. The diversification generator uses
frequency memory — assignments used often in earlier pool members are avoided, a
direct application of Glover's diversification principle. The combination method
is backward path relinking with the swap delta, so each step costs $O(h \cdot n)$
instead of $O(h \cdot n^2)$:

```python
import numpy as np


class FrequencyDiversifier:
    """Frequency-memory diversification generator for permutations.

    counts[f, l] = how often facility f received location l in earlier
    generated solutions; each new solution prefers rarely used assignments.
    """

    def __init__(self, n: int) -> None:
        self.counts = np.zeros((n, n))

    def __call__(self, rng: np.random.Generator) -> np.ndarray:
        n = self.counts.shape[0]
        perm = np.full(n, -1, dtype=int)
        free = np.ones(n, dtype=bool)
        for f in rng.permutation(n):
            locs = np.flatnonzero(free)
            c = self.counts[f, locs]
            loc = int(rng.choice(locs[c == c.min()]))   # least-used, ties random
            perm[f] = loc
            free[loc] = False
        self.counts[np.arange(n), perm] += 1
        return perm


def qap_path_relink(start: np.ndarray, guide: np.ndarray, F: np.ndarray,
                    D: np.ndarray) -> tuple[np.ndarray | None, float]:
    """Greedy relinking via repairing swaps; returns best interior + cost."""
    s = start.copy()
    cur = qap_cost(s, F, D)
    best, best_cost = None, np.inf
    while True:
        diff = np.flatnonzero(s != guide)
        if len(diff) < 2:
            return best, best_cost
        moves = []
        for a in diff:
            b = int(np.flatnonzero(s == guide[a])[0])
            moves.append((swap_delta(s, F, D, a, b), a, b))
        d, a, b = min(moves)
        s[a], s[b] = s[b], s[a]
        cur += d
        if np.any(s != guide) and cur < best_cost:
            best, best_cost = s.copy(), cur


def combine_qap(x: np.ndarray, y: np.ndarray, F: np.ndarray,
                D: np.ndarray) -> list[np.ndarray]:
    """Backward PR: relink from the better endpoint toward the worse one."""
    if qap_cost(x, F, D) > qap_cost(y, F, D):
        x, y = y, x
    interior, _ = qap_path_relink(x, y, F, D)
    return [] if interior is None else [interior]


F, D = generate_qap(n=12, seed=3)
div = FrequencyDiversifier(12)
ss_best, ss_cost = scatter_search(
    diversify=div,
    improve=lambda p: two_exchange(p, F, D),
    combine=lambda x, y, rng: combine_qap(x, y, F, D),
    cost=lambda p: qap_cost(p, F, D),
    distance=lambda p, q: float(np.sum(p != q)),
    b1=5, b2=5, pool_size=30, max_rebuilds=3, seed=0)
assert sorted(ss_best.tolist()) == list(range(12))       # valid permutation
print(f"{ss_cost:.1f}")
# Expected: 24650.1. The multi-start baseline -- the best of the same 30
# improved pool members -- stops at 24662.7; the combination phase closes
# the difference, reaching the value a tuned GRASP+PR finds on this instance.
```

Notes. The combination is deterministic, so the `rng` argument of the framework's
`combine` goes unused; a greedy randomized PR step (RCL over the repairing swaps)
reintroduces randomness when rebuilds recombine the same pairs. The framework
improves the interior point returned by `combine_qap`, so relinking stays a cheap
scan and the descent runs once per pair.

## Worked Example 2: Path Relinking Between Knapsack Elites

Path relinking without the full scatter search machinery: take elites produced by
any method and relink them pairwise. The 0/1 knapsack problem — maximize
$\sum_j v_j x_j$ subject to $\sum_j w_j x_j \le W$, $x \in \{0,1\}^n$ — makes the
feasibility question explicit, because interior points on a path can overflow the
capacity. Strategy here: allow infeasible steps, record only feasible interiors,
and repair plus greedy-fill the returned point. An exact DP validator provides
the optimality reference; for the problem family see **knapsack-problems**.
Base ingredients:

```python
import numpy as np


def generate_knapsack(n: int, seed: int) -> tuple[np.ndarray, np.ndarray, float]:
    """Uncorrelated 0/1 knapsack: integer values/weights, capacity = half the total."""
    rng = np.random.default_rng(seed)
    values = rng.integers(10, 100, n).astype(float)
    weights = rng.integers(5, 50, n).astype(float)
    capacity = float(np.floor(0.5 * weights.sum()))
    return values, weights, capacity


def kp_is_feasible(x: np.ndarray, weights: np.ndarray, capacity: float) -> bool:
    """Independent feasibility check."""
    return bool(weights[x].sum() <= capacity + 1e-9)


def greedy_fill(x: np.ndarray, values: np.ndarray, weights: np.ndarray,
                capacity: float) -> np.ndarray:
    """Add items by value/weight ratio while they fit (deterministic)."""
    x = x.copy()
    slack = capacity - weights[x].sum()
    for j in np.argsort(-values / weights):
        if not x[j] and weights[j] <= slack:
            x[j] = True
            slack -= weights[j]
    return x


def repair_kp(x: np.ndarray, values: np.ndarray, weights: np.ndarray,
              capacity: float) -> np.ndarray:
    """Drop worst-ratio packed items until feasible, then greedy-fill the slack."""
    x = x.copy()
    while weights[x].sum() > capacity + 1e-9:
        packed = np.flatnonzero(x)
        x[packed[np.argmin(values[packed] / weights[packed])]] = False
    return greedy_fill(x, values, weights, capacity)


def build_elites(values: np.ndarray, weights: np.ndarray, capacity: float,
                 n_elites: int, alpha: float, seed: int) -> list[np.ndarray]:
    """GRASP-style greedy randomized constructions; keep the best distinct ones."""
    rng = np.random.default_rng(seed)
    n = len(values)
    ratio = values / weights
    pool: list[np.ndarray] = []
    for _ in range(20 * n_elites):
        x = np.zeros(n, dtype=bool)
        slack = capacity
        while True:
            cand = np.flatnonzero(~x & (weights <= slack))
            if len(cand) == 0:
                break
            r = ratio[cand]
            cutoff = r.max() - alpha * (r.max() - r.min())
            j = int(rng.choice(cand[r >= cutoff - 1e-12]))
            x[j] = True
            slack -= weights[j]
        pool.append(x)
    pool.sort(key=lambda s: -values[s].sum())
    elites: list[np.ndarray] = []
    for x in pool:
        if all(np.any(x != e) for e in elites):
            elites.append(x)
        if len(elites) == n_elites:
            break
    return elites
```

The relinking step picks, among all one-flip moves toward the guide, the best
feasible one — and when every move overflows, the one with least overflow, so the
walk always reaches the guide. Mixed relinking alternates the two endpoints. One
round of evolutionary path relinking relinks all elite pairs and admits improved,
repaired interiors back into the elite set:

```python
import numpy as np


def _kp_step(s: np.ndarray, guide: np.ndarray, values: np.ndarray,
             weights: np.ndarray, capacity: float) -> tuple[float, bool]:
    """Apply in place the best one-flip move of s toward guide.

    Feasible moves compete on value; if none is feasible, take the move
    with the least overflow. Returns (value after move, feasibility).
    """
    diff = np.flatnonzero(s != guide)
    delta_w = np.where(guide[diff], weights[diff], -weights[diff])
    delta_v = np.where(guide[diff], values[diff], -values[diff])
    loads = weights[s].sum() + delta_w
    vals = values[s].sum() + delta_v
    feas = loads <= capacity + 1e-9
    if feas.any():
        k = int(np.argmax(np.where(feas, vals, -np.inf)))
    else:
        k = int(np.argmin(loads - capacity))
    s[diff[k]] = guide[diff[k]]
    return float(vals[k]), bool(feas[k])


def kp_path_relink(start: np.ndarray, guide: np.ndarray, values: np.ndarray,
                   weights: np.ndarray, capacity: float,
                   truncate: float = 1.0) -> tuple[np.ndarray | None, float]:
    """Forward greedy PR; returns the best feasible interior and its value."""
    s = start.copy()
    best, best_val = None, -np.inf
    h0 = int(np.sum(start != guide))
    for _ in range(int(np.ceil(truncate * h0))):
        if np.sum(s != guide) <= 1:
            break
        val, feas = _kp_step(s, guide, values, weights, capacity)
        if feas and np.any(s != guide) and val > best_val:
            best, best_val = s.copy(), val
    return best, best_val


def kp_mixed_pr(x: np.ndarray, y: np.ndarray, values: np.ndarray,
                weights: np.ndarray, capacity: float
                ) -> tuple[np.ndarray | None, float]:
    """Mixed PR: alternate one step from each end until the ends meet."""
    a, b = x.copy(), y.copy()
    best, best_val = None, -np.inf
    while np.sum(a != b) > 1:
        val, feas = _kp_step(a, b, values, weights, capacity)
        if feas and np.any(a != b) and val > best_val:
            best, best_val = a.copy(), val
        a, b = b, a
    return best, best_val


def kp_dp_optimum(values: np.ndarray, weights: np.ndarray,
                  capacity: float) -> float:
    """Exact 0/1 knapsack DP over integer weights -- independent reference."""
    dp = np.zeros(int(capacity) + 1)
    for v, w in zip(values, weights.astype(int)):
        dp[w:] = np.maximum(dp[w:], dp[:-w] + v)   # RHS uses pre-update dp: 0/1
    return float(dp[-1])


values, weights, capacity = generate_knapsack(n=50, seed=6)
elites = build_elites(values, weights, capacity, n_elites=6, alpha=0.5, seed=2)
elite_vals = [float(values[e].sum()) for e in elites]
best_before = max(elite_vals)

improved = True                # one evolutionary-PR pass until no admission
while improved:
    improved = False
    for i in range(len(elites)):
        for j in range(len(elites)):
            if i == j:
                continue
            cand, _ = kp_path_relink(elites[i], elites[j],
                                     values, weights, capacity)
            if cand is None:
                continue
            cand = repair_kp(cand, values, weights, capacity)
            v = float(values[cand].sum())
            w = int(np.argmin(elite_vals))
            if v > elite_vals[w] + 1e-9 and all(np.any(cand != e)
                                                for e in elites):
                elites[w], elite_vals[w] = cand, v
                improved = True

best_after = max(elite_vals)
assert all(kp_is_feasible(e, weights, capacity) for e in elites)
print(f"{best_before:.0f} -> {best_after:.0f}  "
      f"(DP optimum {kp_dp_optimum(values, weights, capacity):.0f})")
# Expected: 2044 -> 2059  (DP optimum 2059) -- relinking the six elite
# constructions closes the full remaining gap to the exact optimum; the
# repair + greedy-fill step turns interiors into feasible, maximal packings.
```

Notes. Relinking is elite-to-elite here (evolutionary PR); the more common online
pattern relinks each new local optimum against one randomly chosen elite — that
variant lives inside the GRASP loop and is shown in **grasp**. For maximization,
keep the sign convention visible (`-np.inf` sentinels, `argmax`) rather than
negating values everywhere; sign bugs in admission tests are silent.

## Advanced Techniques

### Two-Tier Reference Set Update

Quality-only replacement lets the RefSet collapse into near-clones. The two-tier
rule keeps the diversity slots honest: a trial enters the quality tier only by
cost, and the diversity tier only if it is farther from the quality tier than the
least-diverse current member:

```python
import numpy as np
from collections.abc import Callable


def two_tier_update(refset: list[np.ndarray], ref_costs: list[float],
                    trial: np.ndarray, trial_cost: float,
                    distance: Callable[[np.ndarray, np.ndarray], float],
                    b1: int) -> bool:
    """Two-tier RefSet admission; mutates refset/ref_costs, returns True on entry.

    Quality tier = b1 lowest-cost members; diversity tier = the rest.
    """
    if any(distance(trial, r) <= 1e-9 for r in refset):
        return False                                   # duplicate guard
    order = np.argsort(ref_costs)
    quality, diversity = order[:b1], order[b1:]
    worst_q = int(quality[-1])
    if trial_cost < ref_costs[worst_q] - 1e-12:        # quality admission
        refset[worst_q], ref_costs[worst_q] = trial.copy(), trial_cost
        return True
    d_trial = min(distance(trial, refset[int(i)]) for i in quality)
    d_members = [min(distance(refset[int(i)], refset[int(j)]) for j in quality)
                 for i in diversity]
    k = int(np.argmin(d_members))
    if d_trial > d_members[k] + 1e-12:                 # diversity admission
        refset[int(diversity[k])] = trial.copy()
        ref_costs[int(diversity[k])] = trial_cost
        return True
    return False
```

Swap this rule into the framework's admission test when the mean pairwise RefSet
distance collapses within a few rounds — a diagnostic worth logging in every
experiment (see **diversity-and-population-management**).

### Truncated and Greedy Randomized Relinking

Profile where interior improvements occur along the path before paying for full
relinks: on most problems the histogram concentrates in the first third from the
initiating endpoint (Resende & Ribeiro 2005). Truncating at 20–40% then buys 2–3x
more relinks per budget at almost no quality loss — the `truncate` parameter in
both drivers above. Greedy randomized relinking replaces the argmin step choice
with an RCL draw among the best moves; use it when the same elite pairs are
relinked repeatedly (rebuilds, evolutionary PR rounds), so repeated scans take
different trajectories through the same segment.

### Evolutionary Path Relinking as Post-Processing

After any elite-collecting search finishes, run rounds of all-pairs relinking,
improve the interiors, and admit improvements until a round admits nothing
(Resende & Werneck 2004). It is the cheapest quality upgrade at the end of a run
because it reuses solutions already paid for. Skip pairs closer than a minimum
distance (no interior to find) and pairs already relinked with both endpoints
unchanged — keep a set of relinked pair hashes.

### Combination Beyond Relinking

Path relinking is one combination method, not the only one. Classic scatter
search on binary or integer vectors uses weighted linear combinations rounded to
feasibility — for a pair $(x, y)$ with costs $c_x \le c_y$, generate
$z = x + \lambda (y - x)$ for $\lambda \in \{-0.5, 0.5, 1.5\}$ (one exterior on
each side, one interior) and round; for permutations, vote-merging assigns each
position the value preferred by the better parent unless already used (Campos,
Glover, Laguna & Martí 2001, "An experimental evaluation of a scatter search for
the linear ordering problem"). Relinking wins when a strong move delta exists;
linear combination wins on vector spaces with cheap rounding repair.

## Practical Challenges

**The reference set collapses to near-duplicates within a few rounds.** Quality-
only replacement admits clones of the incumbent. Add the duplicate guard at
admission (minimum distance > 0 is not enough — use a threshold like n/20), switch
to the two-tier update, and log min/mean pairwise RefSet distance per round so the
collapse is visible instead of silent.

**Relinking returns nothing or only endpoint copies.** Endpoints too close (no
interior exists — skip pairs below a distance threshold) or too far (the path
crosses a poor region). Measure the interior-improvement rate against pair
distance; if mid-range distances also fail, the elites share no exploitable
structure and plain multi-start at the same budget is the honest alternative.

**Combined trials are infeasible.** Decide the policy once and document it:
restrict the step set to feasible moves (can disconnect the path), allow
infeasible steps but record only feasible interiors (the knapsack example), or
repair every returned point deterministically. Validate final solutions with an
independent feasibility check, never with the search's own bookkeeping.

**The improvement method consumes the entire budget.** With 45 pairs per round
and a full descent per trial, local search dominates. Improve only trials whose
unimproved cost already beats the worst RefSet member, use first-improvement
descent inside the loop and best-improvement only on the final incumbent, and
truncate relinks so fewer interior candidates reach the improvement stage.

**The search stagnates after the first rebuild.** Frequency memory in the
diversification generator must persist across rebuilds (the `FrequencyDiversifier`
above does) — a memoryless sampler regenerates the same pool. Raise b2, randomize
the relinking step choice, and try exterior relinking when interior paths are
exhausted.

**Scatter search underperforms a GA at equal budget.** Check the comparison
first: equal evaluation counts including improvement calls, same local search if
the GA is memetic, 10+ seeds, distributions not best values. If the gap is real,
the usual cause is a weak combination method; replace random crossover with
relinking or structured combination before abandoning the method.

**Path relinking added to GRASP shows no improvement.** The elite set is filled
by quality only and holds near-identical members, so relinks find nothing. Admit
elites with a distance rule, start relinking once the set holds 3+ distinct
members, and relink against a random elite rather than always the best.

## Tools & Libraries

| Library | When to use | Note |
|---|---|---|
| numpy | All framework, relinking, and improvement operations | `np.random.default_rng(seed)`; vectorize candidate evaluation per relink step |
| scipy.spatial.distance | RefSet diversity on large pools | `cdist` builds the full distance matrix for max-min selection in one call |
| numba | Swap-delta loops and 2-exchange descents at n ≥ 50 | `@njit` the delta and the descent; keep the template in plain Python |
| multiprocessing / joblib | Improvement of trial solutions in parallel | Trials within one round are independent; merge admissions after the batch |
| pandas | Experiment tables (instance, seed, b1, b2, variant, cost, time) | Aggregate over seeds before comparing variants |
| matplotlib | Best-so-far curves; RefSet diversity over rounds; improvement-position histograms along paths | The path-position histogram justifies the truncation fraction |
| Optuna / irace | Tuning b1, b2, pool size, truncation on training instances | Hold out test instances; defaults (5+5, pool 50) are robust starting points |

## Output Format

A complete scatter search / path relinking deliverable contains:

1. **Configuration summary** — one table naming all five methods concretely:

| Field | Value |
|---|---|
| Diversification generation | generator type (frequency memory, systematic), pool size |
| Improvement | neighborhood, first/best improvement, delta evaluation used |
| Reference set | b1 + b2, admission rule (replace-worst / two-tier), duplicate threshold |
| Subset generation | subset type (pairs with a new member), trials per subset |
| Combination | PR variant (direction, truncation) or structured combination rule |
| Budget | rebuild rounds or wall-clock limit, stopping rule |
| Seeds | list or range; one rng per run |

2. **Results table** — per instance: best cost, mean ± std over seeds, gap to
   best-known or exact value, time-to-best, and the multi-start baseline (same
   improvement method and budget) in its own column.
3. **Validation statement** — every reported solution passed an independent
   feasibility check and objective recomputation outside the algorithm code (the
   knapsack example validates against an exact DP).
4. **Convergence and diversity evidence** — best-so-far curve per rebuild round;
   min/mean pairwise RefSet distance per round; admissions per round.
5. **Relinking diagnostics** — fraction of relinks yielding an improving interior;
   histogram of improvement positions along the path (justifies truncation).
6. **Code artifacts** — instance generator with seeds, the five methods as
   separate functions, and the validator, so reviewers can rerun everything.

Report evaluation counts (including improvement-method calls) alongside
wall-clock time; comparisons under combination counts alone are meaningless.

## Questions to Ask

- What is the solution representation, and what distance metric matches it?
- Does a local search with cheap delta evaluation exist for the improvement method?
- Full scatter search, or path relinking added to an existing elite-collecting method?
- Minimization or maximization, and where is the sign converted?
- Can relinking-path intermediates be infeasible, and what is the repair policy?
- What budget per instance, and how many seeds for the final comparison?
- Are there benchmark instances with best-known values to report gaps against?
- What baselines must the comparison include, at what budgets and seed counts?
- Is deterministic reproducibility required, or is per-run variance acceptable?
- How will solutions be validated independently of the algorithm code?

## Related Skills

- **grasp** — when path relinking serves as the intensification layer of GRASP,
  or greedy randomized construction must produce the elite solutions to relink.
- **genetic-algorithms** — when a large stochastic population with generic
  crossover fits the problem better than a small, deterministically managed
  reference set.
- **diversity-and-population-management** — when RefSet admission needs distance
  metrics, duplicate detection, or diversity measurement and control in depth.
- **quadratic-assignment-problem** — when the QAP worked example becomes the real
  task: formulations, bounds, benchmark instances, and stronger neighborhoods.
