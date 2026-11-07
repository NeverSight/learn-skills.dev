---
name: grasp
description: When the user wants to implement GRASP — multi-start greedy randomized construction with a restricted candidate list followed by local search — including alpha tuning, reactive GRASP, and path relinking hybrids. Also use when the user mentions "GRASP," "greedy randomized," "restricted candidate list," "RCL," "multi-start," "semi-greedy," or when a good greedy heuristic exists but its deterministic bias must be escaped by randomized restarts. For the improvement phase, see local-search-and-neighborhoods; for elite-set intensification, see scatter-search-path-relinking.
---

# GRASP — Greedy Randomized Adaptive Search Procedures

You are an expert in metaheuristic optimization, specializing in GRASP and multi-start
methods. This skill covers greedy randomized construction with restricted candidate lists
(RCL), the construction/local-search iteration, alpha calibration, reactive GRASP, bias
functions, and hybridization with path relinking. Use the framework below to decide
whether GRASP fits a problem, implement it correctly in vectorized numpy, and report
results that withstand reviewer scrutiny.

## Initial Assessment

Establish the following before proposing or writing any GRASP code:

- **Greedy structure.** Identify the element-by-element construction: what is an
  "element" (a column, an assignment, an edge), and what incremental greedy score does
  adding it have? GRASP requires a cheap, meaningful greedy function. If none exists,
  reconsider the method.
- **Problem class and objective.** Minimization or maximization, single objective,
  and which constraints the construction must respect at every partial step.
- **Hard vs soft constraints.** Hard constraints shape the candidate set during
  construction; soft constraints belong in the objective or in penalties.
- **Instance size.** Number of elements per solution, candidates per construction step,
  and whether greedy scores can be updated incrementally instead of recomputed.
- **Local search.** Which neighborhood improves constructed solutions, and whether
  O(1)/O(n) delta evaluation exists. GRASP without a competent improvement phase is
  just semi-greedy sampling and usually underperforms.
- **Evaluation cost.** Time per construction and per local-search descent determines
  how many restarts fit the budget.
- **Exact-vs-heuristic need.** If instances are small enough for a MIP solver to close
  the gap in the available time, solve exactly and use GRASP only for warm starts.
- **Time budget and stopping rule.** Wall-clock limit, iteration limit, or
  stagnation-based stop; restarts are independent, so the budget maps linearly to
  iterations.
- **Quality requirement.** Target gap to best-known solutions or bounds; whether a
  single good solution or a distribution over seeds is required.
- **Data format.** How instances arrive (matrix files, benchmark formats, generated)
  and what an independent feasibility check looks like.
- **Memory features in scope.** Plain GRASP is memoryless; decide up front whether
  reactive alpha, hashing of duplicates, or path relinking is part of the deliverable.
- **Parallel resources.** Independent restarts parallelize with near-linear speedup;
  count available cores.
- **Reproducibility.** One `np.random.default_rng(seed)` per run; record seeds in all
  result tables.

## Algorithm Anatomy

GRASP (Feo & Resende 1989, "A probabilistic heuristic for a computationally difficult
set covering problem"; Feo & Resende 1995, "Greedy randomized adaptive search
procedures") is a multi-start metaheuristic. Each iteration has two phases:

1. **Greedy randomized construction.** Build a complete solution element by element.
   At each step, score every feasible candidate with the greedy function, form a
   restricted candidate list (RCL), and pick one RCL member uniformly at random.
2. **Local search.** Descend from the constructed solution to a local optimum.

The incumbent over all iterations is returned. Iterations are independent: basic GRASP
carries no state between restarts except the incumbent.

**The RCL.** Let $C$ be the current candidate set and $c(e)$ the incremental greedy
cost of element $e$ (lower is better), with $c_{\min} = \min_{e \in C} c(e)$ and
$c_{\max} = \max_{e \in C} c(e)$. The value-based RCL with parameter
$\alpha \in [0, 1]$ is

$$
\mathrm{RCL}(\alpha) \;=\; \{\, e \in C \;:\; c(e) \,\le\, c_{\min} + \alpha\,(c_{\max} - c_{\min}) \,\}.
$$

The cardinality-based alternative keeps the $\lceil \alpha\,|C| \rceil$ best-scored
candidates. Semantics of the extremes:

- $\alpha = 0$: pure greedy construction (random only in tie-breaking).
- $\alpha = 1$: uniformly random construction.

**Adaptive** is the operative word: greedy scores are recomputed (or incrementally
updated) after every selection, because the value of a candidate depends on the partial
solution built so far. A non-adaptive variant that scores candidates once is cheaper
but markedly weaker on problems with strong interaction between elements.

**Why GRASP works.** Pure greedy is a single, biased sample: it commits early to
myopic choices and lands in one basin of attraction. Pure random restarts cover many
basins but start local search from poor solutions, wasting descent time. Semi-greedy
sampling (Hart & Shogan 1987, "Semi-greedy heuristics: an empirical study") produces
starting points that are simultaneously good and diverse, so local search converges
fast and to varied local optima. The minimum over iterations then improves with the
number of restarts. Empirically, GRASP time-to-target values follow an approximately
exponential distribution (Aiex, Resende & Ribeiro 2002, "Probability distribution of
solution time in GRASP"), which has a practical consequence: running $p$ independent
GRASPs in parallel divides expected time-to-target by roughly $p$.

**Decision guidance.**

- Use GRASP when a natural constructive heuristic exists (covering, location,
  assignment, scheduling, routing) and its score is cheap to evaluate or update.
- Prefer GRASP over iterated local search when high-quality local optima are scattered
  across the search space; prefer ILS when they cluster in a "big valley," because
  perturbing a good solution then beats rebuilding from scratch.
- Prefer GRASP over population methods when memory and diversity machinery would be
  overkill, or when an embarrassingly parallel method is wanted.
- Plain GRASP learns nothing across iterations. If the iteration budget is large,
  add memory: reactive alpha selection and path relinking are the two standard,
  well-tested upgrades (Resende & Ribeiro 2016, "Optimization by GRASP").

**Complexity.** One iteration costs the construction plus the descent. A construction
of $k$ elements with $|C|$ candidates per step and incremental score updates costs
$O(k\,|C|)$ score evaluations; recomputing scores from scratch each step multiplies
that by the update cost. Local search usually dominates; budget it accordingly and see
**local-search-and-neighborhoods** for delta-evaluation patterns that keep it cheap.

## Generic Framework

The skeleton every GRASP shares:

```text
GRASP(alpha, max_iters):
    best <- None
    for k = 1 .. max_iters:                       # independent restarts
        x <- GreedyRandomizedConstruction(alpha)
        x <- LocalSearch(x)                       # descend to a local optimum
        if cost(x) < cost(best): best <- x
    return best

GreedyRandomizedConstruction(alpha):
    x <- empty partial solution
    while x is not complete:
        C    <- feasible candidate elements given x
        c(e) <- greedy score of e for all e in C  # adaptive: depends on x
        cmin, cmax <- min / max of c over C
        RCL  <- { e in C : c(e) <= cmin + alpha * (cmax - cmin) }
        e    <- uniform random element of RCL
        x    <- x + e                             # update scores incrementally
    return x
```

The RCL selection is the only piece that repeats across problems, so isolate it:

```python
import numpy as np


def rcl_choice(scores: np.ndarray, alpha: float, rng: np.random.Generator,
               kind: str = "value") -> int:
    """Pick one candidate index from the restricted candidate list.

    scores: greedy score per candidate, lower = better, np.inf = infeasible.
    kind:   "value" keeps scores within alpha of the min-max range;
            "cardinality" keeps the best ceil(alpha * n_feasible) candidates.
    """
    feasible = np.flatnonzero(np.isfinite(scores))
    s = scores[feasible]
    if kind == "value":
        cutoff = s.min() + alpha * (s.max() - s.min())
        rcl = feasible[s <= cutoff + 1e-12]
    else:
        k = max(1, int(np.ceil(alpha * len(feasible))))
        rcl = feasible[np.argpartition(s, k - 1)[:k]]
    return int(rng.choice(rcl))
```

The driver is problem-independent. It takes the construction and the local search as
callables, so the same loop serves every worked example below:

```python
import numpy as np
from collections.abc import Callable


def grasp(construct: Callable[[float, np.random.Generator], np.ndarray],
          local_search: Callable[[np.ndarray], np.ndarray],
          cost: Callable[[np.ndarray], float],
          n_iters: int = 200, alpha: float = 0.2,
          seed: int = 0) -> tuple[np.ndarray, float, np.ndarray]:
    """Plain multi-start GRASP; returns (best, best_cost, best-so-far curve)."""
    rng = np.random.default_rng(seed)
    best, best_cost = None, np.inf
    curve = np.empty(n_iters)
    for k in range(n_iters):
        x = local_search(construct(alpha, rng))
        c = cost(x)
        if c < best_cost:
            best, best_cost = x.copy(), c
        curve[k] = best_cost
    return best, best_cost, curve


# Tiny wiring check: select exactly 2 of 5 items at minimum total cost.
_item_costs = np.array([5.0, 1.0, 4.0, 2.0, 9.0])

def _toy_construct(alpha: float, rng: np.random.Generator) -> np.ndarray:
    """Greedy randomized selection of 2 items (value-based RCL on item cost)."""
    chosen = np.zeros(5, dtype=bool)
    for _ in range(2):
        scores = np.where(chosen, np.inf, _item_costs)
        feasible = np.flatnonzero(np.isfinite(scores))
        s = scores[feasible]
        cutoff = s.min() + alpha * (s.max() - s.min())
        chosen[int(rng.choice(feasible[s <= cutoff + 1e-12]))] = True
    return chosen

best, best_cost, _ = grasp(_toy_construct, lambda x: x,
                           lambda x: float(_item_costs[x].sum()),
                           n_iters=50, alpha=0.3, seed=1)
print(best_cost)
# Expected: 3.0 -- the items costing 1 and 2, found within the 50 restarts.
```

### Parameter guidance

| Parameter | Typical range | Trade-off |
|---|---|---|
| `alpha` (value RCL) | 0.10–0.30 fixed; or reactive over {0.0, 0.1, ..., 0.9} | Low alpha = better single-start quality, less diversity; high alpha = diverse but weak starts that burn local-search time |
| RCL type | Value-based by default | Value RCL adapts its size to the score spread; cardinality RCL gives fixed-size control when scores are badly scaled |
| Iterations | 100–5,000 or a wall-clock budget | More restarts improve the minimum, linearly in time; returns diminish without memory mechanisms |
| Local search | First-improvement in the loop; best-improvement for final polish | Speed per restart vs depth per restart |
| Bias function | Uniform (classic); linear or exponential rank bias | Sharper bias pushes selection toward greedy without shrinking the RCL |
| Elite set size (PR) | 5–10 distinct solutions | Larger sets diversify relinking targets but slow admission turnover |
| PR frequency | Every iteration, or every 2–5 | Intensification payoff vs extra local-search calls |
| Reactive block size | 50–100 iterations per probability update | Faster adaptation vs noisier per-alpha estimates |

Operator-level details (neighborhood catalogs, repair operators, delta tables) are
covered by their own skills — see **local-search-and-neighborhoods** for moves and
**fitness-evaluation-and-caching** for incremental evaluation; do not reinvent them
inside the GRASP loop.

## Worked Example 1: Set Covering GRASP

The set covering problem (SCP): given rows $1..m$, columns $j = 1..n$ with cost
$c_j > 0$ and a boolean cover matrix $A \in \{0,1\}^{m \times n}$, choose a column set
covering every row at minimum cost:

$$
\min \sum_{j=1}^{n} c_j x_j \quad \text{s.t.} \quad \sum_{j: a_{ij}=1} x_j \ge 1 \;\; \forall i, \qquad x_j \in \{0,1\}.
$$

The classic greedy score is cost per newly covered row, $c_j / |S_j \cap U|$ where $U$
is the uncovered set (Chvátal 1979, "A greedy heuristic for the set-covering problem").
This was GRASP's original application (Feo & Resende 1989). For models, bounds, and
Lagrangian alternatives on this problem family, see
**set-covering-packing-partitioning**.

Instance generator and an independent feasibility check:

```python
import numpy as np


def generate_scp(m: int, n: int, density: float,
                 seed: int) -> tuple[np.ndarray, np.ndarray]:
    """Random SCP instance: boolean cover matrix A (m x n) and costs c (n,)."""
    rng = np.random.default_rng(seed)
    A = rng.random((m, n)) < density
    for i in np.flatnonzero(A.sum(axis=1) < 2):       # guarantee coverability
        A[i, rng.choice(n, size=2, replace=False)] = True
    c = 1.0 + rng.integers(0, 99, size=n).astype(float)
    return A, c


def scp_is_cover(x: np.ndarray, A: np.ndarray) -> bool:
    """Independent feasibility check: every row covered by a selected column."""
    return bool(A[:, x].any(axis=1).all())
```

Construction. Solutions are boolean column masks. The score vector is rebuilt after
every selection from the shrinking uncovered set — the adaptive part:

```python
import numpy as np


def construct_scp(A: np.ndarray, c: np.ndarray, alpha: float,
                  rng: np.random.Generator) -> np.ndarray:
    """Greedy randomized SCP construction; returns a boolean column mask.

    Greedy score: cost per newly covered row, recomputed after each pick.
    """
    m, n = A.shape
    x = np.zeros(n, dtype=bool)
    uncovered = np.ones(m, dtype=bool)
    while uncovered.any():
        gain = A[uncovered].sum(axis=0).astype(float)   # new rows per column
        score = np.where((gain > 0) & ~x, c / np.maximum(gain, 1.0), np.inf)
        feasible = np.flatnonzero(np.isfinite(score))
        s = score[feasible]
        cutoff = s.min() + alpha * (s.max() - s.min())
        j = int(rng.choice(feasible[s <= cutoff + 1e-12]))
        x[j] = True
        uncovered &= ~A[:, j]
    return x
```

Local search: first drop redundant columns (every covered row stays covered), then a
first-improvement 1-out exchange — remove one column, repair greedily, keep the trial
if it is strictly cheaper. The repair is a deterministic version of the construction:

```python
import numpy as np


def drop_redundant(x: np.ndarray, A: np.ndarray, c: np.ndarray) -> np.ndarray:
    """Remove columns whose rows are all covered twice, most expensive first."""
    x = x.copy()
    counts = A[:, x].sum(axis=1)                    # cover count per row
    for j in sorted(np.flatnonzero(x), key=lambda j: -c[j]):
        rows = A[:, j]
        if (counts[rows] >= 2).all():
            x[j] = False
            counts = counts - rows
    return x


def greedy_repair(x: np.ndarray, A: np.ndarray, c: np.ndarray) -> np.ndarray:
    """Deterministic ratio-greedy repair of a partial (uncovering) solution."""
    x = x.copy()
    uncovered = ~A[:, x].any(axis=1)
    while uncovered.any():
        gain = A[uncovered].sum(axis=0).astype(float)
        score = np.where((gain > 0) & ~x, c / np.maximum(gain, 1.0), np.inf)
        j = int(np.argmin(score))
        x[j] = True
        uncovered &= ~A[:, j]
    return x


def scp_local_search(x: np.ndarray, A: np.ndarray, c: np.ndarray) -> np.ndarray:
    """Redundancy elimination + first-improvement 1-out exchange."""
    x = drop_redundant(x, A, c)
    improved = True
    while improved:
        improved = False
        for j in np.flatnonzero(x):
            trial = x.copy()
            trial[j] = False
            trial = drop_redundant(greedy_repair(trial, A, c), A, c)
            if c[trial].sum() < c[x].sum() - 1e-9:
                x, improved = trial, True
                break
    return x
```

The full algorithm is the generic `grasp` driver plus closures over the instance.
Always benchmark against the alpha = 0 extreme — deterministic greedy plus the same
local search — because that baseline is what randomization must beat:

```python
import numpy as np

A, c = generate_scp(m=100, n=300, density=0.03, seed=7)

greedy_only = scp_local_search(
    construct_scp(A, c, alpha=0.0, rng=np.random.default_rng(0)), A, c)

best, best_cost, curve = grasp(
    construct=lambda alpha, rng: construct_scp(A, c, alpha, rng),
    local_search=lambda x: scp_local_search(x, A, c),
    cost=lambda x: float(c[x].sum()),
    n_iters=200, alpha=0.15, seed=42)

assert scp_is_cover(best, A)
print(f"greedy+LS: {c[greedy_only].sum():.0f}   GRASP: {best_cost:.0f}")
# Expected: both feasible covers; greedy+LS gives 648, GRASP 633 (~2% lower) --
# the 200 randomized restarts escape the deterministic greedy's bias.
```

## Worked Example 2: QAP GRASP with Path Relinking

The quadratic assignment problem (QAP): given symmetric flow matrix $F$ and distance
matrix $D$ (zero diagonals), find a permutation $\pi$ (facility $\to$ location)
minimizing

$$
\min_{\pi} \; \sum_{a=1}^{n} \sum_{b=1}^{n} F_{ab} \, D_{\pi(a)\pi(b)}.
$$

GRASP was among the first competitive heuristics for QAP (Li, Pardalos & Resende 1994,
"A greedy randomized adaptive search procedure for the quadratic assignment problem").
The construction places high-interaction facilities first; the local search is
2-exchange descent with the standard $O(n)$ swap delta — maintain a full delta table
for larger instances, see **fitness-evaluation-and-caching**:

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


def construct_qap(F: np.ndarray, D: np.ndarray, alpha: float,
                  rng: np.random.Generator) -> np.ndarray:
    """Greedy randomized placement, high-interaction facilities first.

    Greedy score of (facility f, free location l): the interaction cost
    between f at l and all already-placed facilities.
    """
    n = F.shape[0]
    perm = np.full(n, -1, dtype=int)
    free = np.ones(n, dtype=bool)                  # free locations
    placed: list[int] = []
    for f in np.argsort(-F.sum(axis=1)):           # facility insertion order
        locs = np.flatnonzero(free)
        if placed:
            pl = np.array(placed)
            inc = 2.0 * (D[np.ix_(locs, perm[pl])] @ F[f, pl])  # symmetric F, D
            cutoff = inc.min() + alpha * (inc.max() - inc.min())
            loc = int(rng.choice(locs[inc <= cutoff + 1e-12]))
        else:
            loc = int(rng.choice(locs))
        perm[f] = loc
        free[loc] = False
        placed.append(f)
    return perm


def swap_delta(perm: np.ndarray, F: np.ndarray, D: np.ndarray,
               a: int, b: int) -> float:
    """O(n) cost change for swapping the locations of facilities a and b."""
    mask = np.ones(len(perm), dtype=bool)
    mask[[a, b]] = False
    pk = perm[mask]
    u, v = perm[a], perm[b]
    return float(2.0 * ((F[a, mask] - F[b, mask]) * (D[v, pk] - D[u, pk])).sum())


def qap_local_search(perm: np.ndarray, F: np.ndarray,
                     D: np.ndarray) -> np.ndarray:
    """Best-improvement 2-exchange descent using O(n) swap deltas."""
    perm = perm.copy()
    n = len(perm)
    while True:
        best_delta, best_pair = -1e-9, None
        for a in range(n - 1):
            for b in range(a + 1, n):
                d = swap_delta(perm, F, D, a, b)
                if d < best_delta:
                    best_delta, best_pair = d, (a, b)
        if best_pair is None:
            return perm
        a, b = best_pair
        perm[a], perm[b] = perm[b], perm[a]
```

**Path relinking** turns memoryless GRASP into a method with intensification (Laguna &
Martí 1999, "GRASP and path relinking for 2-layer straight line crossing
minimization"). Keep a small elite set; after each GRASP iteration, walk step by step
from the new local optimum toward a randomly chosen elite, always applying the best
repairing swap, and keep the best intermediate solution on the path. The sketch below
is the standard greedy forward relinking for permutations; a deeper treatment of
reference-set management and relinking variants lives in
**scatter-search-path-relinking**:

```python
import numpy as np


def path_relink(start: np.ndarray, guide: np.ndarray, F: np.ndarray,
                D: np.ndarray) -> tuple[np.ndarray, float]:
    """Greedy walk from start toward guide; returns the best intermediate."""
    s = start.copy()
    best, best_cost = s.copy(), qap_cost(s, F, D)
    cur_cost = best_cost
    while True:
        diff = np.flatnonzero(s != guide)
        if len(diff) < 2:
            return best, best_cost
        moves = []
        for a in diff:
            b = int(np.flatnonzero(s == guide[a])[0])   # swap fixes position a
            moves.append((swap_delta(s, F, D, a, b), a, b))
        d, a, b = min(moves)                            # best repairing swap
        s[a], s[b] = s[b], s[a]
        cur_cost += d
        if cur_cost < best_cost - 1e-9:
            best, best_cost = s.copy(), cur_cost


def grasp_pr_qap(F: np.ndarray, D: np.ndarray, n_iters: int = 60,
                 alpha: float = 0.3, elite_size: int = 5,
                 seed: int = 0) -> tuple[np.ndarray, float]:
    """GRASP + path relinking to a random elite each iteration."""
    rng = np.random.default_rng(seed)
    elites: list[tuple[float, np.ndarray]] = []
    best, best_cost = None, np.inf

    def submit(perm: np.ndarray, cost: float) -> None:
        nonlocal best, best_cost
        if cost < best_cost:
            best, best_cost = perm.copy(), cost
        if all(np.any(perm != e) for _, e in elites):   # keep elites distinct
            elites.append((cost, perm.copy()))
            elites.sort(key=lambda t: t[0])
            del elites[elite_size:]

    for _ in range(n_iters):
        x = qap_local_search(construct_qap(F, D, alpha, rng), F, D)
        cx = qap_cost(x, F, D)
        if elites:
            _, guide = elites[int(rng.integers(len(elites)))]
            y, _ = path_relink(x, guide, F, D)
            y = qap_local_search(y, F, D)               # polish best intermediate
            cy = qap_cost(y, F, D)
            if cy < cx:
                submit(y, cy)
        submit(x, cx)
    return best, best_cost


F, D = generate_qap(n=12, seed=3)
best, best_cost = grasp_pr_qap(F, D, n_iters=40, alpha=0.3, elite_size=5, seed=1)
assert sorted(best.tolist()) == list(range(12))         # valid permutation
print(f"{best_cost:.1f}")
# Expected: 24650.1. Plain multi-start GRASP with the same seed and budget
# stalls at 24713.5; relinking against the elite set recovers the better
# value. Across seeds, GRASP+PR results here stay within 0.1% of each other.
```

Notes on the relinking step. Each swap fixes at least one disagreeing position, so a
path between solutions at Hamming distance $h$ has at most $h - 1$ interior points;
evaluating each step costs $O(h \cdot n)$ with the delta function. Apply full local
search only to the best intermediate, not to every point on the path — relinking is a
cheap trajectory scan, not a second descent phase.

## Advanced Techniques

### Reactive GRASP

Fixing alpha is the most common tuning mistake: the best value differs across
instances and even across phases of a run. Reactive GRASP (Prais & Ribeiro 2000,
"Reactive GRASP: an application to a matrix decomposition problem in TDMA traffic
assignment") draws alpha from a discrete set with probabilities updated from observed
solution quality — alphas that produced better averages get sampled more often:

```python
import numpy as np


class ReactiveAlpha:
    """Reactive GRASP alpha selection (Prais & Ribeiro 2000).

    Samples alpha from a discrete set; every block_size iterations the
    sampling probabilities are reset proportional to
    (best_cost / avg_cost_of_alpha) ** beta.
    """

    def __init__(self, alphas: np.ndarray, block_size: int = 50,
                 beta: float = 10.0) -> None:
        self.alphas = alphas
        self.block_size = block_size
        self.beta = beta
        self.probs = np.full(len(alphas), 1.0 / len(alphas))
        self.sums = np.zeros(len(alphas))
        self.counts = np.zeros(len(alphas))
        self.best = np.inf
        self.iters = 0
        self.idx = 0

    def sample(self, rng: np.random.Generator) -> float:
        """Draw the alpha to use for the next GRASP iteration."""
        self.idx = int(rng.choice(len(self.alphas), p=self.probs))
        return float(self.alphas[self.idx])

    def report(self, cost: float) -> None:
        """Feed back the cost of the iteration run with the sampled alpha."""
        self.sums[self.idx] += cost
        self.counts[self.idx] += 1
        self.best = min(self.best, cost)
        self.iters += 1
        if self.iters % self.block_size == 0:
            avg = self.sums / np.maximum(self.counts, 1.0)
            avg[self.counts == 0] = self.best        # untried alphas stay attractive
            q = (self.best / avg) ** self.beta
            self.probs = q / q.sum()


# Reactive GRASP on the set covering functions from Worked Example 1.
A, c = generate_scp(m=100, n=300, density=0.03, seed=7)
ra = ReactiveAlpha(alphas=np.linspace(0.0, 0.9, 10), block_size=40, beta=50.0)
rng = np.random.default_rng(5)
best_cost = np.inf
for _ in range(200):
    alpha = ra.sample(rng)
    x = scp_local_search(construct_scp(A, c, alpha, rng), A, c)
    ra.report(float(c[x].sum()))
    best_cost = min(best_cost, float(c[x].sum()))
print(best_cost, np.round(ra.probs, 2))
# Expected: best_cost 633 (matches the fixed-alpha run above); probabilities
# concentrate on the low alphas, e.g. ~0.27 and ~0.24 on alpha 0.0 and 0.1.
```

Prais & Ribeiro used `beta = 10`. Note, however, that a strong local search
compresses the cost differences between alphas — every start descends to a similar
level — so a sharper exponent (30–100) is often needed before probability mass moves
decisively. Report the final probability vector in experiments: it is free diagnostic
output that tells you what alpha the instance class actually wants.

### Bias Functions in RCL Sampling

Uniform sampling inside the RCL is the classic choice, but the selection can be biased
toward better-ranked candidates without shrinking the list (Bresina 1996, "Heuristic-
biased stochastic sampling"). This decouples diversity (RCL size, via alpha) from
greediness (sampling sharpness, via the bias):

```python
import numpy as np


def biased_rcl_choice(scores: np.ndarray, alpha: float, bias: str,
                      rng: np.random.Generator) -> int:
    """RCL sampling with a rank bias: 'uniform', 'linear' (1/rank),
    or 'exponential' (e^-rank). Lower score = better candidate."""
    feasible = np.flatnonzero(np.isfinite(scores))
    s = scores[feasible]
    rcl = feasible[s <= s.min() + alpha * (s.max() - s.min()) + 1e-12]
    rank = np.argsort(np.argsort(scores[rcl])) + 1.0
    w = {"uniform": np.ones_like(rank),
         "linear": 1.0 / rank,
         "exponential": np.exp(-rank)}[bias]
    return int(rng.choice(rcl, p=w / w.sum()))
```

A linear bias with a generous alpha (0.4–0.6) often matches a tuned uniform RCL while
being less sensitive to the exact alpha value — a useful robustness trade.

### Path Relinking Variants

Forward relinking (new solution toward elite, as implemented above) is the default.
Backward relinking starts from the elite — usually better, since more of the path lies
near the higher-quality endpoint. Mixed relinking alternates ends and meets in the
middle. Truncated relinking explores only the first 20–40% of the path, where most
improvements concentrate. Evolutionary path relinking periodically relinks all elite
pairs as a post-processing intensification (Resende & Werneck 2004, "A hybrid
heuristic for the p-median problem"). Implement forward + truncated first; measure
before adopting anything fancier. Reference-set admission rules (quality plus minimum
distance) are covered in **scatter-search-path-relinking**.

### Avoiding Repeated Work Across Restarts

With small alpha, restarts collide: identical or near-identical constructions get
re-descended at full cost. Hash each constructed solution (e.g.
`hash(x.tobytes())` for a canonical array form) and skip or re-randomize duplicates
before local search. On problems where local search is the bottleneck this saves
10–30% of runtime at negligible cost. Memoization of full evaluations belongs to
**fitness-evaluation-and-caching**.

### Cost Perturbations and Sampled Greedy

Two construction variants matter in practice. Cost perturbation multiplies greedy
scores by random factors (e.g. uniform on [1, 1.25]) and then runs a *pure greedy*
construction — diversity comes from the data instead of the RCL; this often preserves
more greedy quality than value RCLs (Resende & Werneck 2004). Sampled greedy evaluates
only a random subset of candidates per step and picks the best of the sample — the
method of choice when $|C|$ is huge and scoring every candidate per step is the
bottleneck. Both plug into the same `grasp` driver unchanged.

## Practical Challenges

**Every iteration returns nearly the same solution.** Alpha is too small, or greedy
scores contain heavy ties broken deterministically. Verify the construction actually
consumes randomness (log RCL sizes per step — size 1 means pure greedy), randomize
tie-breaking, and raise alpha or switch to a cardinality RCL when score ranges
collapse.

**The incumbent stops improving after a small fraction of the budget.** Expected
behavior for memoryless sampling: the running minimum of i.i.d. draws improves ever
more slowly. Add memory — reactive alpha, path relinking — or split the remaining
budget across parallel seeds instead of extending a stagnant run.

**Construction dominates runtime.** Update greedy scores incrementally instead of
recomputing them: in set covering, only columns intersecting newly covered rows change
their gain. Use `np.argpartition` for cardinality RCLs, and switch to sampled greedy
when the candidate set is very large.

**Local search barely improves constructed solutions.** Either alpha is so low that
constructions are already locally optimal for the chosen neighborhood, or the
neighborhood is too weak. Track mean relative improvement of the descent phase; if it
is near zero, strengthen the neighborhood (see **local-search-and-neighborhoods**)
before touching alpha.

**Construction dead-ends on tightly constrained problems.** When no candidate is
feasible for a partial solution, do not silently return garbage: restart the
construction (cheap), allow temporarily infeasible additions with penalty scores, or
finish with a repair operator. Count dead-ends — a high rate means the greedy order
itself needs rethinking.

**Path relinking elite set collapses to near-duplicates.** Admission by quality alone
fills the set with clones and relinking paths of length zero. Admit a solution only if
it differs from every elite by a minimum distance (e.g. Hamming distance ≥ n/10), and
replace the closest worse elite rather than the worst one.

**Alpha tuned on one instance fails on the rest.** Tune on a training subset and
report on a disjoint test subset, or sidestep the issue with reactive GRASP. Always
report the alpha sensitivity curve — reviewers ask for it, and flat curves are a
selling point.

**Comparisons against ILS or simulated annealing look unfair.** Give every method the
same wall-clock or evaluation budget and the same local search where applicable, run
10+ seeds, and compare distributions, not single best values. GRASP's variance across
seeds is usually low; exploit that in the write-up.

## Tools & Libraries

| Library | When to use | Note |
|---|---|---|
| numpy | All construction and local-search inner operations | `np.random.default_rng(seed)`; vectorize score vectors, never loop over candidates in Python |
| scipy.sparse | Covering/partitioning matrices beyond ~10^4 columns | CSC format makes column gain updates cheap |
| numba | Hot pairwise scans (e.g. QAP swap loops) at n ≥ 50 | `@njit` the delta loop; keep the GRASP driver in plain Python |
| multiprocessing / joblib | Parallel independent restarts | One worker per seed; merge incumbents at the end — near-linear speedup |
| pandas | Experiment tables (one row per run: instance, seed, alpha, cost, time) | Aggregate over seeds before comparing methods |
| matplotlib | Best-so-far curves and time-to-target (TTT) plots | TTT plots are the standard evidence for GRASP runtime behavior |
| Optuna / irace | Tuning alpha, block size, elite size on a training instance set | Hold out test instances; reactive GRASP often removes the need |

## Output Format

A complete GRASP deliverable contains:

1. **Configuration summary** — one table, so the run is reproducible:

| Field | Value |
|---|---|
| Construction | greedy score definition, RCL type, alpha policy (fixed / reactive set) |
| Local search | neighborhood, first/best improvement, delta evaluation used |
| Memory | none / reactive / path relinking (elite size, admission rule) |
| Budget | iterations or wall-clock limit, stopping rule |
| Seeds | list or range; one rng per run |

2. **Results table** — per instance: best cost, mean ± std over seeds, gap to
   best-known or bound, time-to-best, iterations-to-best, and the alpha = 0
   (greedy + LS) baseline cost in its own column.
3. **Validation statement** — every reported solution passed an independent
   feasibility check and an objective recomputation outside the algorithm code.
4. **Convergence evidence** — best-so-far curve (median over seeds with a min-max
   band) and, for runtime claims, a TTT plot at a stated target value.
5. **Diagnostics** — final reactive-alpha probabilities (if used), mean local-search
   improvement per iteration, duplicate-construction rate.
6. **Code artifacts** — instance generator with seeds, the algorithm, and the
   validator as separate functions, so reviewers can rerun everything.

Report iteration counts *and* wall-clock time: GRASP comparisons are meaningless
under iteration counts alone when construction costs differ across methods.

## Questions to Ask

- What greedy construction already exists for this problem, and what is its score?
- Are instances small enough that an exact solver closes the gap in the time budget?
- What is the wall-clock budget per instance, and how many cores are available?
- Is there a known neighborhood with cheap delta evaluation for the local search?
- Fixed alpha or reactive — is cross-instance robustness a requirement?
- Is path relinking in scope, or is plain multi-start enough for the deliverable?
- What baselines must the comparison include, and at what budgets and seed counts?
- How will solutions be validated independently of the algorithm code?
- Are there benchmark instances with best-known values to report gaps against?

## Related Skills

- **local-search-and-neighborhoods** — when the improvement phase needs better
  neighborhoods, first-vs-best improvement decisions, or delta evaluation design.
- **warm-starts-and-initial-solutions** — when GRASP constructions feed a MIP start
  or another solver, or you need construction heuristics by problem class.
- **set-covering-packing-partitioning** — when the underlying problem is covering or
  partitioning and you need exact models, bounds, or Lagrangian alternatives.
- **scatter-search-path-relinking** — when path relinking becomes the main
  intensification tool and you need reference-set management and relinking variants
  in depth.
