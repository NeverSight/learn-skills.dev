---
name: iterated-local-search
description: When the user wants to design, implement, or tune iterated local search (ILS) — the local-search + perturbation + acceptance loop that is the strongest simple baseline for permutation and routing problems. Also use when the user mentions "iterated local search," "ILS," "perturbation," "kick move," "double-bridge," "iterated greedy," "restart strategy," or when a hill climber keeps returning the same local optimum and needs a principled escape mechanism. For neighborhood and delta-evaluation design, see local-search-and-neighborhoods; for randomized multi-start construction, see grasp.
---

# Iterated Local Search

You are an expert in iterated local search (ILS) and single-solution metaheuristics for
combinatorial optimization. This skill covers the ILS loop — embedded local search,
perturbation ("kick") design, and acceptance criteria — plus perturbation-strength tuning,
adaptive variants, and the use of ILS as the strong simple baseline that any proposed
metaheuristic must beat. Use the framework below to assemble an ILS from a problem-specific
descent and a well-matched kick, to tune its three or four parameters, and to diagnose
stagnation in an existing implementation.

## Initial Assessment

Establish the following before writing any code or recommending parameters:

- **Problem class and representation.** Permutation (tours, schedules), binary selection,
  assignment, or mixed? The representation fixes which local searches and kicks are available.
- **Existing local search.** Is there already a descent procedure? How long does one full
  descent take on a realistic instance? ILS runs the local search hundreds to thousands of
  times; a descent that takes minutes makes plain ILS impractical without truncation.
- **Evaluation cost.** Is the objective cheap to evaluate? Is delta (incremental) evaluation
  available for the neighborhood moves? Without delta evaluation, the embedded local search
  usually dominates runtime by 95%+.
- **Time budget.** Wall-clock seconds per run, and number of runs (seeds × instances).
  ILS parameters that win at 10 seconds differ from those that win at 10 minutes.
- **Quality requirement.** Gap to best-known solutions, "beat the current heuristic," or
  "good feasible fast"? This decides acceptance criterion aggressiveness and restart policy.
- **Hard vs soft constraints.** Must every visited solution stay feasible, or may a kick
  pass through infeasibility as long as the local search repairs it?
- **Role in the study.** Is ILS the proposed method or the baseline in a comparison? As a
  baseline it must be implemented competently (good kick, tuned strength), otherwise the
  comparison is meaningless.
- **Instance size now and later.** An O(n^2) neighborhood scan per descent is fine at
  n = 100 and hopeless at n = 100,000 without candidate lists.
- **Software context.** Pure numpy acceptable? Is numba/Cython available for inner loops?
  Reproducibility requirements (seed policy, deterministic ordering)?

## Algorithm Anatomy

ILS searches the set of local optima instead of the set of all solutions. The embedded
local search LS maps any solution to a local optimum, so the reachable set collapses to
$\mathcal{S}^* = \{\mathrm{LS}(s) : s \in \mathcal{S}\}$, which is dramatically smaller and
has much better average quality than $\mathcal{S}$. ILS is a biased walk on
$\mathcal{S}^*$ (Lourenço, Martin & Stützle 2003, "Iterated Local Search", Handbook of
Metaheuristics):

$$
s_0 = \mathrm{LS}(s_{\mathrm{init}}), \qquad
s'_t = \mathrm{LS}\big(\mathrm{Perturb}(s_t)\big), \qquad
s_{t+1} =
\begin{cases}
s'_t & \text{if } \mathrm{Accept}\big(f(s_t), f(s'_t)\big)\\[2pt]
s_t & \text{otherwise.}
\end{cases}
$$

Why this beats independent random restarts: in many landscapes good local optima cluster —
the "big valley" structure observed for the TSP by Boese, Kahng & Muddu (1994). A small kick
from a good optimum lands in a nearby basin whose optimum is correlated with (and often as
good as) the start, and the warm-started local search reaches it in a fraction of the moves
a cold start needs. Random restart throws both advantages away.

### The four components

| Component | Role | Typical choices |
|---|---|---|
| GenerateInitial | first local optimum | greedy construction (nearest neighbor, NEH); random permutation when no greedy exists |
| LocalSearch | defines $\mathcal{S}^*$; must be deterministic-ish and fast from a warm start | 2-opt, insertion descent, VND over 2-3 neighborhoods |
| Perturb | jumps to a nearby basin; must not be undoable by one local-search move | double-bridge, d random reinsertions, destroy-and-rebuild |
| Accept | bias of the walk over $\mathcal{S}^*$ | better-only, Metropolis at fixed T, epsilon-accept, restart |

### Acceptance criteria

- **Better:** accept iff $f(s') < f(s)$. Strong intensification; the default first try.
- **Random walk:** always accept. Maximal diversification; useful only with strong kicks.
- **Metropolis (fixed T):** accept with probability $\min\{1, e^{-(f(s') - f(s))/T}\}$.
  Unlike simulated annealing the temperature is constant — ILS needs no cooling schedule
  because the local search, not the temperature, provides intensification.
- **Epsilon-accept:** accept iff $f(s') \le (1+\varepsilon) f(s)$, $\varepsilon \approx$
  0.02–0.05. Deterministic mild diversification.
- **Restart:** after $L$ consecutive non-improving kicks, reset the current solution to the
  best-so-far (intensifying) or to a fresh construction (diversifying).

### When to choose ILS

- **Use ILS when** a strong, fast local search already exists for the problem. ILS adds
  roughly 20 lines on top of it and is the highest benefit-to-effort metaheuristic.
- **Use ILS as the baseline** in every metaheuristic study on permutation-like problems;
  iterated greedy (an ILS with construction-based kicks) is state of the art for the
  permutation flow shop (Ruiz & Stützle 2007).
- **Prefer tabu search** when the failure mode is cycling on plateaus inside one basin
  rather than basin escape.
- **Prefer GRASP** when randomized construction is more natural than perturbing a complete
  solution (e.g., set covering); GRASP is essentially restart-ILS with the randomness moved
  into construction.
- **Prefer LNS/ALNS** when tight constraints make small kicks useless and destroy-repair is
  the natural move (rich vehicle routing, complex scheduling).

### Cost model

Per iteration: one kick, O(strength), plus one warm-started descent. A warm 2-opt descent
after a double-bridge only needs to repair the region around the 4 changed edges — with
don't-look bits and neighbor lists this is near O(n) instead of the O(n^2) cold-start scan.
Total work = iterations × warm-descent cost; always report wall-clock alongside iteration
counts, because LS truncation trades quality-per-iteration for kicks-per-second.

### Parameter guidance

| Parameter | Typical range | What it trades off |
|---|---|---|
| Kick strength | 1–3 composite moves, or relocating 5–15% of solution components | too weak: the descent undoes the kick and returns the same optimum; too strong: behaves like random restart and loses big-valley correlation |
| Acceptance criterion | better → epsilon → Metropolis → always | intensification vs diversification; start with better-only, soften only on stagnation |
| Metropolis T | calibrate so 2–5% of typical worsening kicks pass; flow-shop rule of thumb $T = \tau \cdot \bar{p}/10$, $\tau \in [0.2, 0.7]$ | higher T → random walk over local optima |
| Restart threshold L | 20–100 non-improving iterations (≈ 5–20% of the budget) | small L: heavy intensification around the incumbent; large L: longer independent excursions |
| Local-search depth | full descent vs single first-improvement pass | quality per iteration vs number of iterations within the budget |
| Budget | fixed wall-clock per run; 10+ seeds | comparisons must use equal time, not equal iterations |

## Reference Implementation

The framework separates the problem-independent loop from the four problem-specific
callables. The incumbent update is deliberately independent of the acceptance decision:
the walk may accept worse solutions, but the best-so-far is never lost.

```text
ILS(construct, LocalSearch, Perturb, Accept, budget):
    s  <- LocalSearch(construct())        # initial local optimum
    s* <- s                               # incumbent
    while budget remains:
        s' <- Perturb(s)                  # kick: leave the current basin
        s' <- LocalSearch(s')             # descend into the neighboring basin
        if f(s') < f(s*):
            s* <- s'                      # incumbent update, independent of Accept
        if Accept(f(s), f(s')):
            s <- s'                       # walk step on the space of local optima
    return s*
```

Acceptance criteria as plain callables, so they can be swapped without touching the loop:

```python
"""Acceptance criteria for ILS: callables (current_cost, candidate_cost, rng) -> bool."""
import math
from typing import Callable

import numpy as np

AcceptFn = Callable[[float, float, np.random.Generator], bool]


def accept_better(current: float, candidate: float, rng: np.random.Generator) -> bool:
    """Accept only strict improvements: the classic, most exploitative choice."""
    return candidate < current


def accept_always(current: float, candidate: float, rng: np.random.Generator) -> bool:
    """Random-walk acceptance: maximal diversification, rarely good on its own."""
    return True


def make_metropolis(temperature: float) -> AcceptFn:
    """Metropolis acceptance at a fixed temperature: accept worse candidates with
    probability exp(-delta / T). Interpolates between accept_better (T -> 0)
    and accept_always (T -> infinity); no cooling schedule is needed in ILS."""
    def accept(current: float, candidate: float, rng: np.random.Generator) -> bool:
        if candidate <= current:
            return True
        return float(rng.random()) < math.exp(-(candidate - current) / temperature)
    return accept


def make_epsilon_accept(epsilon: float) -> AcceptFn:
    """Accept candidates at most a factor (1 + epsilon) worse than the current
    cost. Deterministic mild diversification; epsilon in [0.02, 0.05] is typical."""
    def accept(current: float, candidate: float, rng: np.random.Generator) -> bool:
        return candidate <= (1.0 + epsilon) * current
    return accept
```

The loop itself, with restart acceptance handled via `restart_after`, plus a complete
smoke test on number partitioning (a rugged landscape where plain hill climbing gets
trapped immediately):

```python
"""Problem-independent ILS loop. Plug in construct / local_search / perturb / accept.
Uses accept_better from the acceptance-criteria block above."""
from dataclasses import dataclass, field
from typing import Callable

import numpy as np


@dataclass
class ILSResult:
    """Best solution found plus the trace needed for convergence reporting."""
    best: np.ndarray
    best_cost: float
    n_iterations: int
    n_accepted: int
    history: list[tuple[int, float]] = field(default_factory=list)


def iterated_local_search(
    construct: Callable[[np.random.Generator], np.ndarray],
    local_search: Callable[[np.ndarray], tuple[np.ndarray, float]],
    perturb: Callable[[np.ndarray, np.random.Generator], np.ndarray],
    accept: Callable[[float, float, np.random.Generator], bool],
    n_iterations: int = 500,
    restart_after: int | None = None,
    seed: int = 0,
) -> ILSResult:
    """Run ILS for n_iterations kicks. `local_search` maps any solution to
    (local_optimum, cost). `restart_after` resets the current solution to the
    best-so-far after that many consecutive non-improving iterations."""
    rng = np.random.default_rng(seed)
    current, current_cost = local_search(construct(rng))
    best, best_cost = current.copy(), current_cost
    history = [(0, best_cost)]
    n_accepted, stall = 0, 0
    for it in range(1, n_iterations + 1):
        candidate, candidate_cost = local_search(perturb(current, rng))
        if accept(current_cost, candidate_cost, rng):
            current, current_cost = candidate, candidate_cost
            n_accepted += 1
        if candidate_cost < best_cost - 1e-12:
            best, best_cost = candidate.copy(), candidate_cost
            history.append((it, best_cost))
            stall = 0
        else:
            stall += 1
            if restart_after is not None and stall >= restart_after:
                current, current_cost = best.copy(), best_cost
                stall = 0
    return ILSResult(best, best_cost, n_iterations, n_accepted, history)


def make_partition_problem(weights: np.ndarray) -> tuple[Callable, Callable, Callable]:
    """Number partitioning: split items into two sets minimizing the absolute
    difference of their sums. Rugged landscape; a good ILS smoke test."""
    def construct(rng: np.random.Generator) -> np.ndarray:
        return rng.integers(0, 2, size=weights.size)

    def local_search(x: np.ndarray) -> tuple[np.ndarray, float]:
        x = x.copy()
        while True:
            s = float(weights @ (2 * x - 1))
            flip_costs = np.abs(s - 2 * (2 * x - 1) * weights)  # cost after each flip
            k = int(np.argmin(flip_costs))
            if flip_costs[k] < abs(s) - 1e-9:
                x[k] = 1 - x[k]
            else:
                return x, abs(s)

    def perturb(x: np.ndarray, rng: np.random.Generator) -> np.ndarray:
        y = x.copy()
        idx = rng.choice(x.size, size=3, replace=False)
        y[idx] = 1 - y[idx]
        return y

    return construct, local_search, perturb


rng = np.random.default_rng(7)
weights = rng.integers(1, 1000, size=24).astype(float)
construct, local_search, perturb = make_partition_problem(weights)
hill_cost = local_search(construct(np.random.default_rng(7)))[1]
result = iterated_local_search(construct, local_search, perturb, accept_better,
                               n_iterations=300, seed=7)
print(f"single descent: {hill_cost:.0f}   ILS best: {result.best_cost:.0f}")
# Expected: single descent: 2   ILS best: 0  (a perfect partition exists; ILS finds it)
```

Note the vectorized descent: all single-flip costs are computed in one numpy expression
per pass instead of an inner Python loop. For deeper delta-evaluation patterns see
**local-search-and-neighborhoods**.

## Worked Example 1: TSP with Double-Bridge Kicks

The canonical ILS. Local search is 2-opt; the kick is the **double-bridge**: cut the tour
into four segments A|B|C|D and reconnect them as A-C-B-D. This 4-opt move changes exactly
four edges, keeps every segment's orientation, and — the key property — cannot be reversed
by any single 2-opt move, so the descent cannot simply undo it. It was introduced as the
kick of the large-step Markov chain method of Martin, Otto & Felten (1991), the direct
ancestor of ILS.

Building blocks (instance, evaluation, construction, descent):

```python
"""TSP building blocks: instance, evaluation, construction, vectorized 2-opt."""
import numpy as np


def random_euclidean_tsp(n: int, seed: int) -> np.ndarray:
    """n points uniform in the unit square; returns the (n, n) distance matrix."""
    rng = np.random.default_rng(seed)
    pts = rng.random((n, 2))
    diff = pts[:, None, :] - pts[None, :, :]
    return np.sqrt((diff ** 2).sum(axis=2))


def tour_length(tour: np.ndarray, dist: np.ndarray) -> float:
    """Length of the closed tour visiting cities in `tour` order."""
    return float(dist[tour, np.roll(tour, -1)].sum())


def nearest_neighbor_tour(dist: np.ndarray, start: int = 0) -> np.ndarray:
    """Greedy nearest-neighbor construction starting from city `start`."""
    n = dist.shape[0]
    visited = np.zeros(n, dtype=bool)
    tour = np.empty(n, dtype=np.int64)
    tour[0] = start
    visited[start] = True
    for i in range(1, n):
        row = np.where(visited, np.inf, dist[tour[i - 1]])
        tour[i] = int(np.argmin(row))
        visited[tour[i]] = True
    return tour


def two_opt(tour: np.ndarray, dist: np.ndarray) -> tuple[np.ndarray, float]:
    """2-opt descent to a local optimum. For each first edge, the deltas of all
    compatible second edges are evaluated in one vectorized pass; the reversal
    applies the best one. See local-search-and-neighborhoods for O(1) delta
    derivations and candidate-list accelerations."""
    tour = tour.copy()
    n = tour.size
    improved = True
    while improved:
        improved = False
        for i in range(n - 2):
            a, b = tour[i], tour[i + 1]
            hi = n - 1 if i > 0 else n - 2      # skip the edge sharing city tour[0]
            js = np.arange(i + 2, hi + 1)
            if js.size == 0:
                continue
            c = tour[js]
            d = tour[(js + 1) % n]
            deltas = dist[a, c] + dist[b, d] - dist[a, b] - dist[c, d]
            k = int(np.argmin(deltas))
            if deltas[k] < -1e-10:
                j = int(js[k])
                tour[i + 1:j + 1] = tour[i + 1:j + 1][::-1]
                improved = True
    return tour, tour_length(tour, dist)
```

The kick and the assembled solver. With accept-better and double-bridge, this is the
textbook TSP ILS; for stronger machinery (Or-opt, Lin-Kernighan moves, TSPLIB instances)
see **traveling-salesman-problem**.

```python
"""Double-bridge kick and the assembled TSP ILS.
Uses iterated_local_search / accept_better (framework blocks) and
random_euclidean_tsp / nearest_neighbor_tour / two_opt (previous block)."""
import numpy as np


def double_bridge(tour: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Cut the tour into four segments A|B|C|D and reconnect as A-C-B-D.
    No single 2-opt move can reverse this kick (Martin, Otto & Felten 1991)."""
    n = tour.size
    i, j, k = np.sort(rng.choice(np.arange(1, n), size=3, replace=False))
    return np.concatenate([tour[:i], tour[j:k], tour[i:j], tour[k:]])


def solve_tsp_ils(dist: np.ndarray, n_iterations: int = 300, seed: int = 0) -> "ILSResult":
    """TSP ILS: nearest-neighbor start, 2-opt descent, double-bridge kicks,
    accept-better. The strong simple baseline for any TSP heuristic study."""
    return iterated_local_search(
        construct=lambda rng: nearest_neighbor_tour(dist, start=0),
        local_search=lambda t: two_opt(t, dist),
        perturb=double_bridge,
        accept=accept_better,
        n_iterations=n_iterations,
        seed=seed,
    )


dist = random_euclidean_tsp(n=60, seed=3)
start_cost = two_opt(nearest_neighbor_tour(dist), dist)[1]
result = solve_tsp_ils(dist, n_iterations=300, seed=3)
print(f"2-opt local optimum: {start_cost:.4f}   ILS best: {result.best_cost:.4f}")
# Expected: 2-opt local optimum: 6.2630   ILS best: 6.0728  (~3% gained by kicking)
```

A single double-bridge per iteration is the right default strength: it relocates two
segments while leaving most of the tour intact, so successive local optima stay correlated.
Stacking several double-bridges is the standard way to increase strength (used in the
adaptive variant under Advanced Techniques).

## Worked Example 2: Permutation Flow-Shop with NEH Start

In the permutation flow-shop problem (PFSP), n jobs visit M machines in the same machine
order, and all machines process jobs in the same job order, so a solution is one
permutation $\pi$. With processing times $p_{j,m}$, completion times follow

$$
C_{\pi(i),m} = \max\{C_{\pi(i-1),m},\; C_{\pi(i),m-1}\} + p_{\pi(i),m},
\qquad C_{\max}(\pi) = C_{\pi(n),M},
$$

with $C_{\pi(0),m} = C_{\pi(i),0} = 0$. The objective is to minimize the makespan
$C_{\max}$.

Three classic ingredients make the ILS strong here:

- **NEH construction** (Nawaz, Enscore & Ham 1983): sort jobs by decreasing total
  processing time, insert each at its best position in the partial sequence.
- **Taillard acceleration** (Taillard 1990): evaluating all $k{+}1$ insertion positions of
  one job into a length-$k$ sequence costs $O(kM)$ total — not $O(k^2 M)$ — using head
  matrix $e$ (prefix completion times), tail matrix $q$ (time from each job's start to the
  end of the schedule), and $f$ (completion times of the inserted job at every position):
  the makespan after inserting at position $i$ is $\max_m (f_{i,m} + q_{i,m})$.
- **Destruction-construction kick**: remove $d$ random jobs, greedily reinsert each at its
  best position. With this kick and a constant-temperature Metropolis acceptance, ILS *is*
  the iterated greedy (IG) algorithm of Ruiz & Stützle (2007) — still the reference method
  for the PFSP. The earlier ILS of Stützle (1998) used random insertion/swap kicks.

```python
"""Permutation flow-shop: makespan, Taillard-accelerated insertion, NEH."""
import numpy as np


def makespan(seq: np.ndarray, p: np.ndarray) -> float:
    """Cmax of job sequence `seq`; p has shape (n_jobs, n_machines)."""
    c = np.zeros(p.shape[1])
    for j in seq:
        c[0] += p[j, 0]
        for m in range(1, p.shape[1]):
            c[m] = max(c[m], c[m - 1]) + p[j, m]
    return float(c[-1])


def best_insertion(seq: np.ndarray, job: int, p: np.ndarray) -> tuple[int, float]:
    """Best position and resulting Cmax for inserting `job` into `seq`,
    evaluated for all |seq|+1 positions in O(|seq| * M) total (Taillard 1990)."""
    k, m = seq.size, p.shape[1]
    e = np.zeros((k + 1, m))            # e[i]: completion times of the i-th prefix job
    for i in range(1, k + 1):
        t = p[seq[i - 1]]
        e[i, 0] = e[i - 1, 0] + t[0]
        for mm in range(1, m):
            e[i, mm] = max(e[i, mm - 1], e[i - 1, mm]) + t[mm]
    q = np.zeros((k + 1, m))            # q[i]: tail of seq[i]; q[k] = 0 covers appending
    for i in range(k - 1, -1, -1):
        t = p[seq[i]]
        q[i, m - 1] = q[i + 1, m - 1] + t[m - 1]
        for mm in range(m - 2, -1, -1):
            q[i, mm] = max(q[i, mm + 1], q[i + 1, mm]) + t[mm]
    f = np.empty((k + 1, m))            # f[i]: completions of `job` inserted at i
    f[:, 0] = e[:, 0] + p[job, 0]
    for mm in range(1, m):              # vectorized over all k+1 positions at once
        f[:, mm] = np.maximum(f[:, mm - 1], e[:, mm]) + p[job, mm]
    cmax = (f + q).max(axis=1)
    pos = int(np.argmin(cmax))
    return pos, float(cmax[pos])


def neh(p: np.ndarray) -> np.ndarray:
    """NEH construction (Nawaz, Enscore & Ham 1983): insert jobs in order of
    decreasing total processing time, each at its best position."""
    order = np.argsort(-p.sum(axis=1), kind="stable")
    seq = order[:1].copy()
    for job in order[1:]:
        pos, _ = best_insertion(seq, int(job), p)
        seq = np.insert(seq, pos, job)
    return seq


def random_pfsp_instance(n_jobs: int, n_machines: int, seed: int) -> np.ndarray:
    """Taillard-style instance: processing times uniform on [1, 99]."""
    rng = np.random.default_rng(seed)
    return rng.integers(1, 100, size=(n_jobs, n_machines)).astype(float)


p = random_pfsp_instance(n_jobs=20, n_machines=10, seed=5)
print(f"NEH makespan: {makespan(neh(p), p):.0f}")
# Expected: NEH makespan: 1707
```

The local search is a best-insertion descent (remove each job, reinsert it at its best
position, repeat until no move improves), and the kick reuses `best_insertion` for greedy
repair. Acceptance follows the Ruiz–Stützle constant temperature
$T = \tau \cdot \bar{p}/10$ with $\tau = 0.4$.

```python
"""Insertion local search, destruction kick, and the assembled flow-shop ILS.
Uses iterated_local_search / make_metropolis (framework blocks) and
makespan / best_insertion / neh / random_pfsp_instance (previous block)."""
import numpy as np


def insertion_local_search(seq: np.ndarray, p: np.ndarray) -> tuple[np.ndarray, float]:
    """Best-insertion descent: remove each job, reinsert at its best position;
    repeat full passes until no single-job move improves the makespan."""
    seq = seq.copy()
    current = makespan(seq, p)
    improved = True
    while improved:
        improved = False
        for job in list(seq):
            partial = seq[seq != job]
            pos, new_cmax = best_insertion(partial, int(job), p)
            if new_cmax < current - 1e-9:
                seq = np.insert(partial, pos, job)
                current = new_cmax
                improved = True
    return seq, current


def make_destruction_kick(p: np.ndarray, d: int):
    """Kick: remove d random jobs, greedily reinsert each at its best position.
    This construction-based kick turns ILS into iterated greedy (Ruiz & Stützle 2007)."""
    def kick(seq: np.ndarray, rng: np.random.Generator) -> np.ndarray:
        removed = rng.choice(seq, size=d, replace=False)
        partial = seq[~np.isin(seq, removed)]
        for job in rng.permutation(removed):
            pos, _ = best_insertion(partial, int(job), p)
            partial = np.insert(partial, pos, job)
        return partial
    return kick


def solve_pfsp_ils(p: np.ndarray, n_iterations: int = 150, d: int = 4,
                   tau: float = 0.4, seed: int = 0) -> "ILSResult":
    """Flow-shop ILS: NEH start, insertion descent, destruction kicks,
    constant-temperature Metropolis acceptance."""
    temperature = tau * float(p.mean()) / 10.0
    return iterated_local_search(
        construct=lambda rng: neh(p),
        local_search=lambda s: insertion_local_search(s, p),
        perturb=make_destruction_kick(p, d),
        accept=make_metropolis(temperature),
        n_iterations=n_iterations,
        seed=seed,
    )


p = random_pfsp_instance(n_jobs=20, n_machines=10, seed=5)
neh_cost = makespan(neh(p), p)
result = solve_pfsp_ils(p, n_iterations=150, d=4, tau=0.4, seed=5)
print(f"NEH: {neh_cost:.0f}   ILS best: {result.best_cost:.0f}")
# Expected: NEH: 1707   ILS best: 1611  (about 5.6% below the NEH start)
```

Default `d = 4` removed jobs is robust across Taillard instance sizes from 20×5 to 500×20;
the Metropolis acceptance matters more than `d` once `d` is in the 2–8 range
(Ruiz & Stützle 2007). For NEH tie-breaking variants, IG refinements, and Taillard
benchmark protocol, see **flow-shop-scheduling**.

## Advanced Techniques

### Adaptive perturbation strength

Fixed-strength kicks are a compromise. The standard adaptive rule mirrors VNS shaking:
reset strength to the minimum whenever a new best is found, and grow it after every block
of non-improving iterations. This keeps kicks minimal inside a productive big-valley region
and escalates them only when the region is exhausted.

```python
"""ILS with stagnation-driven kick strength.
Uses accept_better plus the TSP blocks (random_euclidean_tsp, nearest_neighbor_tour,
two_opt, double_bridge) defined above."""
import numpy as np
from typing import Callable


def adaptive_ils(construct: Callable, local_search: Callable, perturb: Callable,
                 accept: Callable, n_iterations: int = 500, s_min: int = 1,
                 s_max: int = 8, grow_after: int = 15, seed: int = 0
                 ) -> tuple[np.ndarray, float]:
    """ILS where `perturb(solution, strength, rng)` takes an explicit strength:
    reset to s_min on a new best, grow by one every `grow_after` stalls."""
    rng = np.random.default_rng(seed)
    current, current_cost = local_search(construct(rng))
    best, best_cost = current.copy(), current_cost
    strength, stall = s_min, 0
    for _ in range(n_iterations):
        candidate, candidate_cost = local_search(perturb(current, strength, rng))
        if accept(current_cost, candidate_cost, rng):
            current, current_cost = candidate, candidate_cost
        if candidate_cost < best_cost - 1e-12:
            best, best_cost = candidate.copy(), candidate_cost
            strength, stall = s_min, 0
        else:
            stall += 1
            if stall % grow_after == 0:
                strength = min(strength + 1, s_max)
    return best, best_cost


def multi_bridge(tour: np.ndarray, strength: int, rng: np.random.Generator) -> np.ndarray:
    """Apply `strength` consecutive double-bridge kicks."""
    for _ in range(strength):
        tour = double_bridge(tour, rng)
    return tour


dist = random_euclidean_tsp(n=80, seed=5)
best, cost = adaptive_ils(
    construct=lambda rng: nearest_neighbor_tour(dist),
    local_search=lambda t: two_opt(t, dist),
    perturb=multi_bridge,
    accept=accept_better,
    n_iterations=400, seed=5,
)
print(f"adaptive ILS best: {cost:.4f}")
# Expected: adaptive ILS best: 7.1109  (ties fixed-strength ILS on this instance;
# the gain appears on instances where strength-1 kicks stagnate)
```

### Calibrating the Metropolis temperature

Do not guess T. Sample 50–200 kicks from a few local optima of a representative instance,
record the worsening deltas $\Delta > 0$ of the resulting local optima, and set
$T = -\Delta_{\mathrm{med}} / \ln(p_{\mathrm{acc}})$ for a target acceptance probability
$p_{\mathrm{acc}}$ of the median-worsening move (0.02–0.05 is a good target). This is the
same calibration logic used for initial temperatures in simulated annealing, applied once
to a constant T. Problem-normalized rules like $T = \tau\,\bar{p}/10$ for the PFSP encode
the same idea when the objective scale is known in advance.

### Restarts, multistart, and elite-guided kicks

Restart acceptance (jump back to the incumbent after L stalls) intensifies; restarting from
a fresh construction diversifies — combine both by alternating. Independent ILS runs are
embarrassingly parallel: one process per seed, keep the best. When single runs stagnate
early, maintain a small elite pool (5–10 best distinct solutions) and kick from a random
elite member instead of the current solution; this is the cheapest population-flavored
upgrade before moving to a full memetic algorithm. If construction-side randomness fits
the problem better than solution-side kicks, that design point is GRASP — see **grasp**.

### Truncated and time-boxed local search

Inside ILS the local search does not need to reach a true local optimum every iteration.
A single first-improvement pass, a descent capped at a move budget, or 2-opt restricted to
the neighborhood of the kicked components ("don't-look bits" set everywhere except the four
changed edges) often triples the number of iterations within the same wall-clock with
little quality loss per iteration. Tune the depth/iterations trade-off on a small instance
grid before the main experiments; for kick-operator design options beyond those used here,
see **mutation-and-perturbation-operators**.

## Practical Challenges

**The local search immediately undoes the kick.** Symptom: consecutive local optima are
identical. The kick lives inside the local search's own neighborhood (e.g., a single 2-opt
kick under a 2-opt descent). Use a structurally different move — double-bridge under 2-opt,
segment insertion under swap descent — or stack several moves. Measure it: hash each local
optimum and track the fraction of iterations returning the previous hash; above ~30%,
strengthen the kick.

**ILS behaves like random restart.** Symptom: quality no better than independent
multi-start under the same budget. The kick is too strong, destroying the correlation
between successive optima. Compare the average distance (e.g., differing edges or
positions) between consecutive local optima against the distance between independent ones;
consecutive should be markedly smaller. Reduce strength until it is.

**The embedded local search consumes the whole budget.** Profile first — the descent is
almost always >90% of runtime. Add delta evaluation, candidate lists, and don't-look bits;
re-optimize only the region the kick touched; or truncate the descent. Only then consider
numba/Cython for the scan loop.

**Accept-better stalls after a few hundred iterations.** The walk is stuck in one
big-valley region. Soften acceptance (epsilon or Metropolis), add `restart_after`, or
enable adaptive strength. If none of this helps, the landscape may lack global structure —
check fitness-distance correlation before investing more in ILS.

**Objective drift from incremental evaluation.** Delta-evaluated costs accumulate
floating-point error or hide bugs. Recompute the objective from scratch every few hundred
iterations and assert agreement within 1e-6 of the incremental value; on integer-valued
objectives demand exact equality.

**Large run-to-run variance.** Report at least 10 seeds per instance with mean, standard
deviation, and best; high variance usually means too-strong kicks or an acceptance
criterion close to random walk. Equal wall-clock budgets — never equal iteration counts —
are the only fair basis for comparing against other methods.

**Kicks break feasibility.** Three orderly options: design feasibility-preserving kicks
(relocate within feasible slots only); let the kick destroy and a greedy repair restore
feasibility, as in the flow-shop destruction kick; or accept transient infeasibility with a
penalty the local search can pay down. Pick one mechanism and validate every accepted
solution with an independent checker.

**"ILS is too simple to publish."** Simplicity is the point: Lourenço, Martin & Stützle
(2003) position ILS as the baseline every new method must beat, and a competently tuned IG
remains state of the art for the PFSP (Ruiz & Stützle 2007). A paper whose proposed method
loses to 60 lines of ILS under equal budget has its answer; include the comparison with
proper statistical testing.

## Tools & Libraries

| Library | When to use | Note |
|---|---|---|
| numpy | all kick and evaluation code in this skill | `np.random.default_rng(seed)` everywhere for reproducible kicks |
| numba | descent scan loops too slow in numpy | `@njit` the 2-opt/insertion inner loop for 10–100× speedups |
| multiprocessing / joblib | parallel independent ILS runs | one seed per worker; return (seed, best_cost, history) |
| tsplib95 | standard TSP benchmark instances | pairs with known optima for gap reporting |
| optuna | tuning kick strength d, temperature tau, restart L | tune on a training instance set, test on a held-out set |
| OR-Tools routing | production routing where building ILS is not worth it | ships guided local search; less control than your own loop |
| pandas | experiment tables across seeds and instances | one row per run: instance, seed, parameters, best, time |

## Output Format

A complete ILS deliverable contains:

1. **Configuration summary** — one table, so the run is reproducible from the report alone:

   | Component | Choice |
   |---|---|
   | Construction | NEH (total-processing-time order) |
   | Local search | best-insertion descent, full passes |
   | Kick | destruction-construction, d = 4 |
   | Acceptance | Metropolis, T = 0.4 · mean(p)/10 |
   | Budget | 150 iterations ≈ 2.1 s; seeds 0–9 |

2. **Convergence evidence** — the `history` trace (iteration, best cost) per seed, plotted
   as best-so-far curves with a min-max or quartile band across seeds.
3. **Solution quality table** — per instance: best, mean, standard deviation over seeds,
   and percentage gap to the best-known solution or to the construction heuristic when no
   reference value exists.
4. **Runtime breakdown** — share of time in the local search vs kicks vs evaluation, and
   iterations per second; this justifies (or motivates) truncation choices.
5. **Code artifacts** — the four callables plus the framework loop, an instance
   generator/parser with explicit seeds, and an independent feasibility-and-objective
   checker applied to every reported solution.
6. **Baseline comparison** — when ILS is the baseline: identical budgets, identical
   instances and seeds, and a paired statistical test on per-instance results.

## Questions to Ask

- What problem and representation — permutation, binary, assignment, something mixed?
- Does a local search already exist, and how long is one descent on a full-size instance?
- Is delta evaluation available for the neighborhood moves, or only full recomputation?
- What is the wall-clock budget per run, and how many runs are planned?
- What is the quality target — gap to best-known, beat a current heuristic, or feasible-fast?
- Must every visited solution be feasible, or may kicks pass through infeasibility?
- Is ILS the proposed method or the baseline, and what comparison protocol is required?
- How large are the instances now, and how large will they get in deployment?
- Are numba/Cython acceptable if the descent needs more speed than numpy gives?

## Related Skills

- **local-search-and-neighborhoods** — when the embedded descent needs better neighborhood
  design, delta evaluation, or scanning-order decisions.
- **mutation-and-perturbation-operators** — when designing or strengthening kick moves
  beyond double-bridge and destruction-reinsertion.
- **grasp** — when randomized construction restarts fit the problem better than perturbing
  one incumbent solution.
- **traveling-salesman-problem** — when the TSP application needs formulations, stronger
  local searches, or TSPLIB benchmark workflows.
- **flow-shop-scheduling** — when the flow-shop application needs NEH variants, iterated
  greedy refinements, or Taillard benchmark protocol.
