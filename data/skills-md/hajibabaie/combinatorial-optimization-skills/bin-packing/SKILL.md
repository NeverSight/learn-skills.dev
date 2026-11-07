---
name: bin-packing
description: When the user wants to pack items into the fewest capacitated bins, compare FFD/BFD heuristics against the L1/L2 lower bounds, or build exact compact MIP and arc-flow models, plus variants with variable bin sizes and item conflicts. Also use when the user mentions "bin packing," "first fit decreasing," "minimize bins," "packing items," "lower bound L2," or when indivisible items must be partitioned into identical capacity-limited containers. For repeated item sizes with large demands and trim loss, see cutting-stock; for the pattern set-covering route, see column-generation.
---

# Bin Packing

You are an expert in one-dimensional bin packing and its standard variants. This skill covers
construction heuristics with worst-case guarantees (FF, BF, FFD, BFD), the L1 and L2 lower
bounds, the compact assignment MIP with symmetry breaking, the arc-flow exact model, item
conflicts, variable bin sizes, and the relation to cutting stock. Use the framework below to
choose the right bound, heuristic, and exact model for the instance at hand, and to validate
every solution independently.

## Initial Assessment

Establish the following before proposing a method.

- **Instance size.** Get `n` (number of items), the capacity `C`, and the number of *distinct*
  item sizes `d`. If `d << n` (many duplicates), aggregate items into (size, demand) pairs and
  treat the problem as cutting stock — pattern-based models scale with `d`, not `n`.
- **Weight type.** Integer or fractional weights? Arc-flow and DP-based bounds need integer
  weights; fractional data must be scaled. Ask for the scaling precision the user accepts.
- **Sanity of the data.** Check `0 < w_i <= C` for every item. An item with `w_i > C` makes the
  instance infeasible; items with `w_i = 0` should be removed before modeling.
- **Variant detection.** Identical bins, or multiple bin types with different capacities and
  costs (variable-sized bin packing)? Are there incompatible item pairs that may not share a
  bin (bin packing with conflicts)? Cardinality limits per bin?
- **Objective check.** Confirm the goal is minimizing the number of bins. If the number of bins
  is fixed and the goal is balancing loads, that is multiprocessor scheduling (P||Cmax), a
  different problem with different methods.
- **Online vs offline.** Do all items arrive up front? Online arrival changes the achievable
  guarantees (no algorithm beats competitive ratio ~1.54) and rules out sorting-based methods.
- **Exactness need.** Is a provably optimal count required, or is "within one bin of a lower
  bound, certified" enough? FFD plus L2 often closes the gap without any solver.
- **Time budget and solver access.** Seconds or hours? Is a Gurobi license available, or should
  the model run on HiGHS / CP-SAT? Arc-flow models can be large: estimate `C * d` arcs first.
- **Solution artifact.** Does the user need only the bin count, or the explicit item-to-bin
  assignment? The assignment matters for downstream use and for validation.
- **Scale of repetition.** One instance, or thousands solved in a loop (e.g., inside a pricing
  or simulation routine)? Repetition pushes toward O(n log n) heuristics with cached bounds.

## Problem Definition, Bounds, and Model Choice

**Formal definition.** Given items `i in I = {1, ..., n}` with weights `w_i > 0` and identical
bins of capacity `C >= max_i w_i`, partition `I` into the minimum number of subsets (bins) such
that the total weight in each subset is at most `C`. The compact (Kantorovich) formulation over
a bin index set `B = {1, ..., U}` (U = any valid upper bound):

$$
\min \sum_{b \in B} y_b
\quad \text{s.t.} \quad
\sum_{b \in B} x_{ib} = 1 \;\; \forall i \in I, \qquad
\sum_{i \in I} w_i\, x_{ib} \le C\, y_b \;\; \forall b \in B, \qquad
x_{ib},\, y_b \in \{0, 1\}.
$$

The pattern (set-covering / Gilmore-Gomory) formulation uses the set `P` of all maximal feasible
packings of a single bin:

$$
\min \sum_{p \in P} \lambda_p
\quad \text{s.t.} \quad
\sum_{p \ni i} \lambda_p \ge 1 \;\; \forall i \in I, \qquad
\lambda_p \in \mathbb{Z}_{\ge 0}.
$$

Its LP relaxation `z_LP` is far stronger than the compact LP (which only gives the trivial
`L1` bound) and is solved by column generation with a knapsack pricing problem.

**Complexity.** Bin packing is strongly NP-hard (reduction from 3-Partition; Garey & Johnson
1979, "Computers and Intractability"). No polynomial algorithm approximates within a factor
below 3/2 unless P = NP (deciding 2 vs 3 bins encodes PARTITION). There is an APTAS (Fernandez
de la Vega & Lueker 1981) and an additive `OPT + O(log OPT)` algorithm via the pattern LP
(Hoberg & Rothvoss 2017). In practice, instances with thousands of items are routinely solved
to optimality by arc-flow or branch-and-price.

**Lower bounds.**

- `L1 = ceil(sum_i w_i / C)`: the continuous bound, equal to the compact LP relaxation. Can be
  as weak as OPT/2 (e.g., all items slightly larger than C/2).
- `L2` (Martello & Toth 1990, "Knapsack Problems"): for a threshold `alpha in [0, C/2]`, count
  items larger than `C - alpha` (one bin each) plus items in `(C/2, C - alpha]`, then charge
  the items in `[alpha, C/2]` against the residual space of the latter group. Maximize over
  `alpha`. Computable in O(n log n); worst-case ratio 2/3 of OPT, and frequently tight.
- `ceil(z_LP)` from the pattern LP: the strongest practical bound. The MIRUP conjecture
  (Scheithauer & Terno 1995) states `OPT <= ceil(z_LP) + 1`; no counterexample is known.

**Relation to cutting stock.** Bin packing is exactly cutting stock with all demands equal to 1.
When item sizes repeat, switch to the cutting-stock view: aggregate to `d` size classes and use
pattern-based or arc-flow models whose size depends on `d` and `C`, not on `n`.

**Method selection.**

| Situation | Recommended approach |
|---|---|
| Need a fast, good solution; any size | FFD or BFD, report gap vs L2 |
| FFD already matches L2 or `ceil(z_LP)` | Stop: optimality is certified without a solver |
| Integer weights, `C * d` up to ~10^6 | Arc-flow MIP (pseudo-polynomial, very strong LP) |
| Small `n` (<= ~100), awkward side constraints | Compact MIP + symmetry breaking, FFD upper bound |
| Many duplicates (`d << n`) | Cutting-stock pattern model + column generation |
| Conflicts between items | Compact MIP with conflict cuts, or conflict-aware FFD |
| Gap of 1 bin must be closed, large instance | Branch-and-price (see column-generation) |
| Heterogeneous instance stream, no single best rule | Heuristic pool / selection (see hyper-heuristics) |

## Construction Heuristics and Lower Bounds

First Fit (FF) places each item into the lowest-indexed bin with room; Best Fit (BF) into the
feasible bin with the least residual space. Sorting items by non-increasing weight first gives
FFD and BFD. Guarantees (asymptotic, all tight):

| Heuristic | Guarantee | Reference |
|---|---|---|
| FF | `FF(I) <= floor(1.7 * OPT(I))` | Dósa & Sgall (2013), "First Fit bin packing: a tight analysis" |
| BF | `BF(I) <= floor(1.7 * OPT(I))` | Dósa & Sgall (2014) |
| FFD | `FFD(I) <= 11/9 * OPT(I) + 6/9` | Dósa (2007), tight bound of FFD |
| BFD | `BFD(I) <= 11/9 * OPT(I) + 1` | Johnson (1973), worst-case ratio family |

The naive implementations below are O(n^2); for very large `n`, FF can run in O(n log n) with a
segment tree over bin residuals. In practice FFD/BFD land within 1-2 bins of optimal on most
random instances.

```python
from collections.abc import Sequence


def first_fit(weights: Sequence[float], capacity: float,
              order: Sequence[int] | None = None) -> list[list[int]]:
    """Pack items in `order` (default: input order), each into the first bin that fits."""
    idx = list(order) if order is not None else list(range(len(weights)))
    bins: list[list[int]] = []
    loads: list[float] = []
    for i in idx:
        for b, load in enumerate(loads):
            if load + weights[i] <= capacity:
                bins[b].append(i)
                loads[b] += weights[i]
                break
        else:
            bins.append([i])
            loads.append(weights[i])
    return bins


def best_fit(weights: Sequence[float], capacity: float,
             order: Sequence[int] | None = None) -> list[list[int]]:
    """Pack items in `order`, each into the feasible bin with least residual space."""
    idx = list(order) if order is not None else list(range(len(weights)))
    bins: list[list[int]] = []
    loads: list[float] = []
    for i in idx:
        best_b, best_resid = -1, float("inf")
        for b, load in enumerate(loads):
            resid = capacity - load - weights[i]
            if 0 <= resid < best_resid:
                best_b, best_resid = b, resid
        if best_b >= 0:
            bins[best_b].append(i)
            loads[best_b] += weights[i]
        else:
            bins.append([i])
            loads.append(weights[i])
    return bins


def decreasing_order(weights: Sequence[float]) -> list[int]:
    """Indices sorted by non-increasing weight (the 'D' in FFD/BFD)."""
    return sorted(range(len(weights)), key=lambda i: -weights[i])


weights = [7, 6, 5, 4, 3, 2, 1]
ffd_bins = first_fit(weights, capacity=10, order=decreasing_order(weights))
bfd_bins = best_fit(weights, capacity=10, order=decreasing_order(weights))
print(len(ffd_bins), ffd_bins)
# Expected: 3 [[0, 4], [1, 3], [2, 5, 6]] — loads 10, 10, 8; L1 = ceil(28/10) = 3,
# so FFD is provably optimal here without any solver.
```

Always compute both lower bounds before judging a heuristic solution. If the heuristic count
equals `max(L1, L2)`, you are done.

```python
import math

import numpy as np


def lower_bound_l1(weights: np.ndarray, capacity: int) -> int:
    """Continuous bound: ceil(total weight / capacity). Equals the compact LP bound."""
    return math.ceil(float(weights.sum()) / capacity)


def lower_bound_l2(weights: np.ndarray, capacity: int) -> int:
    """Martello-Toth L2 bound, O(n log n) over candidate thresholds.

    For threshold alpha: items > C - alpha each need their own bin (J1); items in
    (C/2, C - alpha] need their own bin too (J2) but keep usable residual space;
    items in [alpha, C/2] (J3) are charged against that residual space. It suffices
    to scan alpha over 0 and the distinct weights <= C/2 (Martello & Toth 1990).
    """
    w = np.asarray(weights)
    best = lower_bound_l1(w, capacity)
    alphas = np.unique(w[w <= capacity / 2])
    for alpha in np.concatenate(([0], alphas)):
        j1 = w[w > capacity - alpha]
        j2 = w[(w > capacity / 2) & (w <= capacity - alpha)]
        j3 = w[(w >= alpha) & (w <= capacity / 2)]
        free_in_j2_bins = len(j2) * capacity - float(j2.sum())
        extra = max(0, math.ceil((float(j3.sum()) - free_in_j2_bins) / capacity))
        best = max(best, len(j1) + len(j2) + extra)
    return int(best)


w = np.array([6, 6, 6, 5, 5, 5])
print(lower_bound_l1(w, 10), lower_bound_l2(w, 10))
# Expected: 4 5 — at alpha=5: three items of 6 need own bins, the three 5s need
# ceil(15/10)=2 more. Optimum is 5 (6|6|6|5+5|5), so L2 is tight and L1 is not.
```

Worst-case quality of the bounds themselves: `L1 >= OPT/2` and `L2 >= (2/3) OPT`
asymptotically (Martello & Toth 1990). When `L2 < FFD`, compute `ceil(z_LP)` from the pattern
LP before concluding that FFD is suboptimal — the gap is usually in the bound, not the packing.

## Exact Models in Gurobi

### Compact assignment MIP

The compact model is correct but symmetric: any permutation of bin indices gives an equivalent
solution, and the LP relaxation only yields `L1`. Two standard fixes are built in below:
(1) canonical assignment — item `i` may only use bins `0..i` (order bins by the smallest item
index they contain); (2) prefix bins — bin `b+1` can open only if bin `b` is open. Always pass
a heuristic upper bound (FFD count) as the number of candidate bins; this shrinks the model and
tightens the search. Conflicts (incompatible pairs) enter as pairwise constraints.

```python
import gurobipy as gp
import numpy as np
from gurobipy import GRB


def allowed_pairs(n_items: int, n_bins: int) -> list[tuple[int, int]]:
    """Canonical symmetry reduction: item i may only use bins 0..min(i, n_bins-1)."""
    return [(i, b) for i in range(n_items) for b in range(min(i + 1, n_bins))]


def add_assignment_constraints(model: gp.Model, x: gp.tupledict,
                               n_items: int, n_bins: int) -> None:
    """Each item is placed in exactly one of its allowed bins."""
    for i in range(n_items):
        model.addConstr(
            gp.quicksum(x[i, b] for b in range(min(i + 1, n_bins))) == 1,
            name=f"assign[{i}]")


def add_capacity_constraints(model: gp.Model, x: gp.tupledict, y: gp.tupledict,
                             weights: np.ndarray, capacity: float,
                             n_bins: int) -> None:
    """Bin load at most capacity, and only if the bin is open (links x to y)."""
    n_items = len(weights)
    for b in range(n_bins):
        model.addConstr(
            gp.quicksum(float(weights[i]) * x[i, b] for i in range(b, n_items))
            <= capacity * y[b],
            name=f"cap[{b}]")


def add_symmetry_breaking_constraints(model: gp.Model, y: gp.tupledict,
                                      n_bins: int) -> None:
    """Open bins form a prefix: bin b+1 may open only if bin b is open."""
    for b in range(n_bins - 1):
        model.addConstr(y[b] >= y[b + 1], name=f"prefix[{b}]")


def add_conflict_constraints(model: gp.Model, x: gp.tupledict,
                             conflicts: list[tuple[int, int]],
                             n_bins: int) -> None:
    """Conflicting items may not share a bin (only bins where both can appear)."""
    for i, j in conflicts:
        i, j = min(i, j), max(i, j)
        for b in range(min(i + 1, n_bins)):
            model.addConstr(x[i, b] + x[j, b] <= 1, name=f"conflict[{i},{j},{b}]")


def solve_bin_packing_mip(weights: np.ndarray, capacity: float,
                          conflicts: list[tuple[int, int]] | None = None,
                          n_bins: int | None = None,
                          time_limit: float = 60.0) -> tuple[list[list[int]], float]:
    """Compact assignment MIP. Pass n_bins = FFD count as the upper bound."""
    n_items = len(weights)
    if n_bins is None:
        n_bins = n_items
    model = gp.Model("bin_packing")
    model.Params.OutputFlag = 0
    model.Params.TimeLimit = time_limit
    x = model.addVars(allowed_pairs(n_items, n_bins), vtype=GRB.BINARY, name="x")
    y = model.addVars(n_bins, vtype=GRB.BINARY, name="y")
    add_assignment_constraints(model, x, n_items, n_bins)
    add_capacity_constraints(model, x, y, np.asarray(weights), capacity, n_bins)
    add_symmetry_breaking_constraints(model, y, n_bins)
    if conflicts:
        add_conflict_constraints(model, x, conflicts, n_bins)
    model.setObjective(y.sum(), GRB.MINIMIZE)
    model.optimize()
    if model.Status not in (GRB.OPTIMAL, GRB.TIME_LIMIT) or model.SolCount == 0:
        raise RuntimeError(f"no feasible solution found, status {model.Status}")
    bins = [[i for i in range(n_items) if (i, b) in x and x[i, b].X > 0.5]
            for b in range(n_bins)]
    return [items for items in bins if items], model.ObjBound


w = np.array([7, 6, 5, 4, 3, 2, 1])
bins, bound = solve_bin_packing_mip(w, capacity=10, n_bins=4)
print(len(bins), round(bound))
# Expected: 3 3 — three bins, and ObjBound = 3 proves optimality.
```

Expect the compact model to handle up to roughly 100-200 items with tight bounds; beyond that,
symmetry and the weak LP make it stall. Switch to arc-flow or column generation. For general
gurobipy modeling idioms (parameters, status handling, warm starts), see milp-modeling-gurobi.

### Arc-flow model

The arc-flow formulation (Valério de Carvalho 1999, "Exact solution of bin-packing problems
using column generation and branch-and-bound") models one bin as a path in a graph whose nodes
are partial loads `0..C`. An item arc `(u, u + w)` packs one item of size `w` on top of load
`u`; loss arcs `(u, u + 1)` absorb unused capacity. The total flow value equals the number of
bins, and demand constraints force each size class to be used the right number of times. Its LP
relaxation is *equal in strength* to the Gilmore-Gomory pattern LP, so the model usually solves
at the root node. Size is pseudo-polynomial — O(C·d) arcs — so it needs integer weights and a
moderate capacity. The version below restricts arc tails to subset-sum-reachable nodes, the
basic graph reduction; see Advanced Techniques for stronger reductions.

```python
from collections import defaultdict

import gurobipy as gp
import numpy as np
from gurobipy import GRB


def reachable_nodes(sizes: list[int], counts: list[int], capacity: int) -> list[int]:
    """Subset-sum DP respecting multiplicities: only these loads can be arc tails."""
    reach = np.zeros(capacity + 1, dtype=bool)
    reach[0] = True
    for w, c in zip(sizes, counts):
        for _ in range(c):
            new = reach.copy()
            new[w:] |= reach[:-w]
            if (new == reach).all():
                break
            reach = new
    return [u for u in range(capacity + 1) if reach[u]]


def solve_arc_flow(weights: np.ndarray, capacity: int,
                   time_limit: float = 60.0) -> int:
    """Arc-flow bin packing model; returns the optimal number of bins."""
    sizes_arr, counts_arr = np.unique(np.asarray(weights, dtype=int),
                                      return_counts=True)
    sizes = [int(s) for s in sizes_arr]
    counts = [int(c) for c in counts_arr]
    nodes = reachable_nodes(sizes, counts, capacity)
    item_arcs = [(u, u + w, w) for w in sizes for u in nodes if u + w <= capacity]
    arcs_out: dict[int, list[tuple[int, int, int]]] = defaultdict(list)
    arcs_in: dict[int, list[tuple[int, int, int]]] = defaultdict(list)
    for arc in item_arcs:
        arcs_out[arc[0]].append(arc)
        arcs_in[arc[1]].append(arc)
    model = gp.Model("arc_flow")
    model.Params.OutputFlag = 0
    model.Params.TimeLimit = time_limit
    f = model.addVars(item_arcs, vtype=GRB.INTEGER, name="f")
    loss = model.addVars(capacity, vtype=GRB.INTEGER, name="loss")  # arc (u, u+1)
    z = model.addVar(vtype=GRB.INTEGER, name="bins")
    for u in range(capacity + 1):
        inflow = gp.quicksum(f[a] for a in arcs_in[u]) \
            + (loss[u - 1] if u >= 1 else 0)
        outflow = gp.quicksum(f[a] for a in arcs_out[u]) \
            + (loss[u] if u < capacity else 0)
        if u == 0:
            model.addConstr(outflow - inflow == z, name="source")
        elif u == capacity:
            model.addConstr(inflow - outflow == z, name="sink")
        else:
            model.addConstr(inflow == outflow, name=f"balance[{u}]")
    for w, c in zip(sizes, counts):
        model.addConstr(gp.quicksum(f[a] for a in item_arcs if a[2] == w) == c,
                        name=f"demand[{w}]")
    model.setObjective(z, GRB.MINIMIZE)
    model.optimize()
    if model.Status != GRB.OPTIMAL and model.SolCount == 0:
        raise RuntimeError(f"no solution, status {model.Status}")
    return int(round(z.X))


w = np.array([7, 6, 5, 4, 3, 2, 1])
print(solve_arc_flow(w, capacity=10))
# Expected: 3 — same optimum as the compact MIP, but the LP relaxation already
# gives 2.8 -> ceil = 3, so the root node closes the instance.
```

Recovering the explicit packing from an arc-flow solution means decomposing the flow into
`z` source-to-sink paths (each path is one bin); do this greedily on the integer flow values.
For demand-aggregated data and trim-loss objectives, the same machinery is developed further in
cutting-stock; the pricing view of the same LP is in column-generation.

## Metaheuristic: Random-Key GA with First-Fit Decoder

When FFD leaves a gap of 2+ bins and exact models are too slow (huge `n`, fractional weights,
messy side constraints), a biased random-key GA over packing orders is a robust choice: keys in
`[0,1)^n` are decoded by sorting into an item order and packing with first fit. Every decoded
solution is feasible by construction, and the only problem-specific code is the decoder. The
fitness pairs the bin count with Falkenauer's fill measure `mean((load_b / C)^2)` (Falkenauer
1996, "A hybrid grouping genetic algorithm for bin packing") so that, among equal bin counts,
packings with fuller bins — which are closer to dropping a bin — rank higher. Population
operations are vectorized; see the biased-random-key-genetic-algorithm skill for the framework
details (elite/mutant partitioning, biased crossover) and hyper-heuristics for managing a pool
of packing rules instead of a single decoder.

```python
import numpy as np


def first_fit_decode(perm: np.ndarray, weights: np.ndarray,
                     capacity: float) -> tuple[int, float, list[list[int]]]:
    """Decode an item permutation with first fit.

    Returns (bin count, fill measure mean((load/C)^2), bins). The fill measure
    breaks ties between equal bin counts in favor of fuller bins.
    """
    bins: list[list[int]] = []
    loads: list[float] = []
    for i in perm:
        w = float(weights[i])
        for b, load in enumerate(loads):
            if load + w <= capacity:
                bins[b].append(int(i))
                loads[b] = load + w
                break
        else:
            bins.append([int(i)])
            loads.append(w)
    arr = np.asarray(loads)
    return len(bins), float(np.mean((arr / capacity) ** 2)), bins


def random_key_ga(weights: np.ndarray, capacity: float, pop_size: int = 80,
                  generations: int = 150, elite_frac: float = 0.2,
                  mutant_frac: float = 0.15, inherit_p: float = 0.7,
                  seed: int = 0) -> tuple[int, list[list[int]]]:
    """BRKGA-style random-key GA for bin packing; returns (bin count, bins)."""
    rng = np.random.default_rng(seed)
    n = len(weights)
    n_elite = max(1, int(elite_frac * pop_size))
    n_mut = max(1, int(mutant_frac * pop_size))
    n_off = pop_size - n_elite - n_mut
    pop = rng.random((pop_size, n))
    pop[0] = np.argsort(np.argsort(-np.asarray(weights, dtype=float))) / n  # FFD seed
    best_count, best_bins = n + 1, [[i] for i in range(n)]
    for _ in range(generations):
        perms = np.argsort(pop, axis=1)
        results = [first_fit_decode(p, weights, capacity) for p in perms]
        scores = np.array([(r[0], r[1]) for r in results])
        rank = np.lexsort((-scores[:, 1], scores[:, 0]))  # bins asc, fill desc
        if int(scores[rank[0], 0]) < best_count:
            best_count, best_bins = int(scores[rank[0], 0]), results[rank[0]][2]
        elite = pop[rank[:n_elite]]
        e_idx = rng.integers(0, n_elite, n_off)
        o_idx = rng.integers(n_elite, pop_size, n_off)
        mask = rng.random((n_off, n)) < inherit_p
        offspring = np.where(mask, elite[e_idx], pop[rank[o_idx]])
        pop = np.vstack([elite, offspring, rng.random((n_mut, n))])
    return best_count, best_bins


rng = np.random.default_rng(3)        # Falkenauer triplet instance, optimum = 20
cap = 1000
a = rng.integers(380, 491, size=20)
b = rng.integers(250, (cap - a) // 2 + 1)
w = np.concatenate([a, b, cap - a - b])
rng.shuffle(w)
n_bins, bins = random_key_ga(w, capacity=cap, generations=200, seed=3)
print(n_bins)
# Expected: 21 — the known optimum is 20 (every bin must hold a zero-slack triple)
# and FFD gives 24; the GA closes 3 of FFD's 4 extra bins in 200 generations.
```

Because the FFD order is injected as the first individual, the GA is guaranteed to be at least
as good as FFD. On Falkenauer triplet instances (below), where zero-slack triples defeat any
greedy fit and FFD sits 3-4 bins above the optimum, the GA recovers most of that gap within a
few hundred generations on a population of 80. If many structurally
different instance families must be handled by one solver, prefer a selection hyper-heuristic
over a pool of packing rules (FFD, BFD, worst-fit, random order) — see hyper-heuristics.

## Instance Generation and Validation

### Instance generators (seeded)

Two standard families: uniform weights in a fraction band of `C` (hardness peaks around
`[0.2, 0.8]`), and Falkenauer triplet instances where every optimal bin contains exactly three
items summing to exactly `C` — these have zero slack, defeat FFD reliably, and come with a
known optimum for regression testing.

```python
import numpy as np


def uniform_instance(n: int, capacity: int, lo: float, hi: float,
                     seed: int) -> np.ndarray:
    """Integer weights uniform in [lo*C, hi*C]. Classic hard band: lo=0.2, hi=0.8."""
    rng = np.random.default_rng(seed)
    low = max(1, int(round(lo * capacity)))
    high = max(low, int(round(hi * capacity)))
    return rng.integers(low, high + 1, size=n)


def triplet_instance(n_bins: int, capacity: int, seed: int) -> tuple[np.ndarray, int]:
    """Falkenauer-style triplet instance with known optimum = n_bins.

    Each generated bin holds items (a, b, c) with a + b + c = C exactly,
    a in [0.38C, 0.49C], b and c in [0.25C, 0.5C). Zero slack overall.
    """
    rng = np.random.default_rng(seed)
    a = rng.integers(int(0.38 * capacity), int(0.49 * capacity) + 1, size=n_bins)
    b = rng.integers(int(0.25 * capacity), (capacity - a) // 2 + 1)
    c = capacity - a - b
    weights = np.concatenate([a, b, c])
    rng.shuffle(weights)
    return weights, n_bins


def conflict_graph(n: int, density: float, seed: int) -> list[tuple[int, int]]:
    """Random conflict pairs (i < j) with the given edge density."""
    rng = np.random.default_rng(seed)
    iu, ju = np.triu_indices(n, k=1)
    mask = rng.random(iu.shape[0]) < density
    return [(int(i), int(j)) for i, j in zip(iu[mask], ju[mask])]


w, opt = triplet_instance(n_bins=20, capacity=1000, seed=3)
print(len(w), int(w.sum()) // 1000, opt)
# Expected: 60 20 20 — total weight is exactly 20 * 1000, optimum is 20 bins.
```

Report instance features alongside results: `n`, `C`, `d` (distinct sizes), mean weight as a
fraction of `C`, and the L1/L2 bounds. These features explain most performance differences
between methods.

### Independent validator

Never trust the solver's own bookkeeping. Validate every packing — heuristic, GA, or MIP —
with code that shares nothing with the solution method: check the partition property, the
capacity of every bin, and all conflict pairs, then recompute the objective.

```python
import numpy as np


def validate_packing(bins: list[list[int]], weights: np.ndarray, capacity: float,
                     conflicts: list[tuple[int, int]] | None = None,
                     tol: float = 1e-9) -> tuple[bool, list[str]]:
    """Independent feasibility check; shares no code with any solution method.

    Verifies: every item packed exactly once, every bin within capacity,
    no conflicting pair shares a bin. Returns (feasible, error messages).
    """
    errors: list[str] = []
    seen = np.zeros(len(weights), dtype=int)
    for b, items in enumerate(bins):
        if not items:
            errors.append(f"bin {b} is empty — drop empty bins before reporting")
            continue
        load = float(np.sum(weights[np.asarray(items, dtype=int)]))
        if load > capacity + tol:
            errors.append(f"bin {b} overloaded: load {load} > capacity {capacity}")
        for i in items:
            seen[i] += 1
    if (seen != 1).any():
        bad = np.flatnonzero(seen != 1)
        errors.append(f"items not packed exactly once: {bad.tolist()}")
    if conflicts:
        location = {i: b for b, items in enumerate(bins) for i in items}
        for i, j in conflicts:
            if i in location and location.get(i) == location.get(j):
                errors.append(f"conflict pair ({i},{j}) shares bin {location[i]}")
    return not errors, errors


def packing_objective(bins: list[list[int]]) -> int:
    """Objective recomputed independently: number of non-empty bins."""
    return sum(1 for items in bins if items)


w = np.array([7, 6, 5, 4, 3, 2, 1])
solution = [[0, 4], [1, 3], [2, 5, 6]]
ok, msgs = validate_packing(solution, w, capacity=10)
print(ok, packing_objective(solution))
# Expected: True 3
```

Use integer weights wherever possible so the capacity check is exact. If weights are floats,
fix one tolerance (`tol`) project-wide and use the same value in heuristics, models, and the
validator — mismatched tolerances are a classic source of "valid here, invalid there" bugs.

## Advanced Techniques

### Reductions and dominance before solving

Apply the Martello-Toth reduction procedure before any exact method. Two items with
`w_i + w_j = C` can be fixed into one bin and removed: some optimal solution packs them
together, because swapping any alternative partner of the larger item for the exact complement
never hurts. Any item with `w_i > C - min_j w_j` fits with nothing and gets a dedicated bin;
remove it and add 1 to the bound. More generally, if the largest unpacked item's best feasible
completion (found by a small subset-sum search over compatible items) is dominated by a single
exact partner, fix it. These reductions often shrink hard instances by 20-50% and, combined
with L2 on the reduced instance, yield the stronger L3 bound of Martello & Toth (1990).

### Item conflicts and the coloring connection

Bin packing with conflicts (BPPC) adds a graph `G = (I, E)` of incompatible pairs. BPPC
generalizes both pure bin packing (empty graph) and vertex coloring (all weights 0, or
`C = sum w_i`): each bin is an independent set with a knapsack constraint. Consequences:
(1) any clique in `G` gives a lower bound on the bin count — combine `max(L2, clique bound)`;
(2) conflict-aware FFD must scan bins for both residual capacity and conflicts, and a good item
order is by conflict degree first, weight second (Gendreau, Laporte & Semet 2004, "Heuristics
and lower bounds for the bin packing problem with conflicts"); (3) in branch-and-price, the
pricing problem becomes a knapsack with conflicts — still well-solved by DP over interval or
sparse conflict structures (see knapsack-problems). Dense conflict graphs push the problem
toward coloring methods; sparse ones stay packing-like.

### Variable bin sizes and costs

In variable-sized bin packing (VSBPP), bin types `k` have capacity `C_k` and cost `c_k`;
minimize total cost of used bins. The compact MIP changes little: `y_{bk}` selects a type per
candidate bin, capacity constraints read `sum_i w_i x_{ib} <= sum_k C_k y_{bk}`, and the
objective is `sum_{b,k} c_k y_{bk}`. The continuous bound becomes
`sum_i w_i * min_k (c_k / C_k)` — total weight priced at the cheapest cost per unit of
capacity. Adapt FFD by opening, when no open bin fits, the type minimizing `c_k / C_k` among
types with `C_k >=` the current item (Friesen & Langston 1986 analyze the asymptotic worst case
of such rules; Kang & Park 2003 give practical greedy variants). Arc-flow extends by giving
each bin type its own sink level, or one graph per type with a shared demand layer.

### Pattern LP, MIRUP, and closing the last bin

The practical exactness pipeline is: FFD upper bound -> L2 -> if gap > 0, solve the pattern LP
by column generation -> if `FFD = ceil(z_LP)`, certified optimal; if `FFD = ceil(z_LP) + 1`,
the MIRUP property (Scheithauer & Terno 1995) says you are at most one bin off, and only then
pay for an exact run: arc-flow if `C * d` is moderate, branch-and-price otherwise. Two modern
arc-flow upgrades matter at scale: graph compression, which merges equivalent nodes and prunes
arcs by the decreasing-size criterion (Brandão & Pedroso 2016, "Bin packing and related
problems: general arc-flow formulation with graph compression"), and the reflect formulation,
which folds the graph at `C/2` and roughly halves its size (Delorme & Iori 2020, "Enhanced
pseudo-polynomial formulations for bin packing and cutting stock"). The survey by Delorme, Iori
& Martello (2016, "Bin packing and cutting stock problems: mathematical models and exact
algorithms") is the standard map of this territory.

## Practical Challenges

**The compact MIP stalls on 150 items even with a tight time limit.** This is symmetry plus a
weak LP, not a solver tuning issue. Confirm the canonical `b <= i` variable restriction and the
prefix constraints are active, pass the FFD count as `n_bins` (not `n`), and give the model a
MIP start from FFD. If it still stalls, the answer is a stronger formulation — arc-flow or
column generation — not more parameters.

**L1 says 40 bins, the heuristic uses 44, and you cannot tell who is at fault.** Compute L2 and
then `ceil(z_LP)` from the pattern LP before blaming the heuristic. On instances with many items
just above `C/2`, L1 is off by nearly a factor of two while L2 is exact. Most "my heuristic has
a 10% gap" reports are actually "my bound has a 10% gap".

**Fractional weights break arc-flow and DP-based methods.** Scale to integers with a declared
precision (e.g., grams instead of kilograms). If rounding is unavoidable, round item weights up
and keep the capacity unchanged: any packing of the rounded instance is feasible for the
original, so the optimum you compute is a valid upper bound; solve the rounded-down version too
if you need a bound from below.

**FFD with conflicts returns infeasible bins.** A first-fit scan that checks only capacity will
co-locate conflicting items. The bin-feasibility test must check both the residual capacity and
the absence of conflicts with every item already in the bin; order items by conflict degree,
then weight. With dense graphs, expect many near-singleton bins — that is the coloring bound at
work, not a bug.

**The validator rejects solutions the model claims are feasible.** Almost always a tolerance
mismatch: Gurobi's default integer feasibility tolerance lets `x = 0.999...` round to 1 while
loads computed from `.X > 0.5` indicators are exact. Use integer weights, or align the
validator tolerance with the solver's `FeasibilityTol`, and always rebuild loads from the
extracted assignment rather than from solver expressions.

**A million items arrive but only 40 distinct sizes exist.** Stop treating items individually.
Aggregate to (size, demand) pairs, run FFD on the multiset in O(d log d) per bin-type decision,
and use the cutting-stock pattern model for exactness — its size is independent of `n`. The
bin-packing view wastes three orders of magnitude here.

**Stakeholders want "balanced" bins, not just few bins.** Minimizing bins and balancing loads
conflict: the optimal count packs some bins full and leaves one nearly empty. Solve
lexicographically — first minimize the bin count `B*`, then fix `B*` bins and minimize the
maximum load (or load spread) in a second model. Mixing both in one weighted objective produces
solutions that are good at neither.

## Tools & Libraries

| Library | When to use | Note |
|---|---|---|
| gurobipy | Compact MIP, arc-flow, conflict variants | Commercial; free academic licenses; best B&B engine |
| HiGHS (highspy, or via PuLP/python-mip) | Same models without a commercial license | Strong open-source MIP; arc-flow solves well on it |
| OR-Tools CP-SAT | Side constraints that are awkward in MIP (cardinality, logical) | Boolean assignment model + linear capacity; good with conflicts |
| VPSolver | Production-grade arc-flow with graph compression | Brandão & Pedroso's tool; handles cutting stock and variants |
| numpy | Heuristics, bounds, GA populations | `np.random.default_rng(seed)` everywhere; vectorize population ops |
| pandas | Result tables across instances, seeds, methods | One row per run: instance, seed, method, bins, bound, time |
| `binpacking` (PyPI) | Quick scripting only | Splits into a *fixed* number of balanced bins — a different problem; verify before use |

## Output Format

A complete bin-packing deliverable contains:

1. **Instance summary.** `n`, `C`, `d` distinct sizes, weight distribution (min / mean / max as
   fractions of `C`), conflict density if applicable, generator name and seed.
2. **Bound and solution table.** One row per method, always including the bounds:

   | Method | Bins | Best bound | Gap | Time (s) |
   |---|---|---|---|---|
   | L1 / L2 | — | 20 / 20 | — | 0.00 |
   | FFD | 22 | 20 | 2 | 0.01 |
   | Random-key GA (seed 7) | 21 | 20 | 1 | 1.8 |
   | Arc-flow MIP | 20 | 20 | 0 (optimal) | 4.2 |

3. **Optimality statement.** Explicit and honest: "proved optimal (incumbent = bound)",
   "certified within 1 bin of optimal (MIRUP)", or "best found in 60 s, gap 2 bins vs L2".
4. **Explicit packing artifact.** CSV or JSON mapping `bin_id -> [item ids]` with per-bin load
   and residual; never only the count, unless the user asked for the count alone.
5. **Validator confirmation.** The line `validate_packing(...) -> (True, [])` run on the final
   artifact, stated in the report. A solution that was not independently validated is a draft.
6. **Reproducibility block.** Seeds, solver version and parameters (`TimeLimit`, tolerances),
   and the exact command or script that regenerates the table.

When several methods were run, state which result is the recommendation and why (e.g., "FFD
suffices: it matches L2 on all 50 instances; the MIP added nothing but runtime").

## Questions to Ask

- How many items, what capacity, and how many *distinct* item sizes are there?
- Are weights integers, or can they be scaled to integers at an acceptable precision?
- Are all bins identical, or are there several bin types with different capacities/costs?
- Are there pairs of items that must not share a bin (conflicts)? How dense?
- Is a provably optimal bin count required, or is a certified small gap acceptable?
- What is the time budget per instance, and how many instances must be solved?
- Is a Gurobi license available, or must the solution run on open-source solvers?
- Do all items arrive up front (offline), or one by one with irrevocable decisions (online)?
- Is the real goal fewest bins, or balanced loads across a fixed number of bins?
- What artifact is needed downstream — just the count, or the explicit item-to-bin assignment?

## Related Skills

- **cutting-stock** — when item sizes repeat with large demands: pattern-based models,
  trim-loss objectives, and integer rounding for the aggregated (size, demand) view.
- **column-generation** — when the pattern set-covering LP and branch-and-price are the right
  exact route for large instances; bin packing's pricing problem is a knapsack.
- **knapsack-problems** — for the single-bin subproblem: pricing in column generation,
  subset-sum reductions, and DP machinery reused inside bounds and repairs.
- **hyper-heuristics** — when one packing rule is not robust across heterogeneous instance
  streams: selection over a pool of low-level heuristics (FFD, BFD, worst-fit, regret).
- **milp-modeling-gurobi** — for general gurobipy idioms behind the compact and arc-flow
  models: parameters, status handling, MIP starts, and constraint-builder structure.
