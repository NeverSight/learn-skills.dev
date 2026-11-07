---
name: tabu-search
description: When the user wants to design or implement tabu search — tabu lists and tenure, move attributes, aspiration criteria, frequency-based diversification, candidate list strategies, and elite-restart intensification. Also use when the user mentions "tabu search," "tabu list," "tabu tenure," "aspiration criterion," "candidate list," or when a local search keeps cycling back into the same local optima. For neighborhood design and delta evaluation, see local-search-and-neighborhoods; for incremental objective updates and solution hashing, see fitness-evaluation-and-caching.
---

# Tabu Search

You are an expert in metaheuristic optimization, specifically in designing and implementing tabu search (Glover 1986, "Future paths for integer programming and links to artificial intelligence"; Glover & Laguna 1997, *Tabu Search*). This skill covers the memory structures that make tabu search work — tabu lists and tenure, move attributes, aspiration criteria, frequency-based long-term memory, candidate list strategies, and elite-based intensification — plus two reference implementations: Taillard's robust tabu search for the QAP and a critical-path tabu search for job-shop scheduling. Use the framework below to pick each memory component deliberately, implement against the verified code, and validate results against exact baselines on small instances.

## Initial Assessment

Establish the following before writing any tabu search code. Each answer changes a design decision downstream.

- **Problem class and representation.** Permutation, binary vector, assignment, sequencing per machine? The representation fixes which neighborhoods and which move attributes are available. See solution-representation guidance in local-search-and-neighborhoods before adding memory on top.
- **Neighborhood and its size.** Tabu search scans many moves per iteration (often the whole neighborhood). An O(n²) swap neighborhood with O(1) delta lookup is the sweet spot; an O(n²) neighborhood with O(n) evaluation each already costs O(n³) per iteration and needs candidate lists.
- **Delta evaluation cost.** Tabu search is only competitive when move evaluation is incremental. If each move needs a full objective recomputation, fix that first (fitness-evaluation-and-caching) — memory structures cannot compensate for a slow scan.
- **What should be forbidden?** Decide the move attribute: the exact inverse move, an element-position assignment, a destroyed arc/edge. This is the single most important design choice (see the granularity table below).
- **Tenure regime.** Fixed, randomized per move, or reactive? Randomized tenure (Taillard 1991) is the robust default; fixed tenure needs per-instance tuning.
- **Evaluation budget and time limit.** Iterations × (scan cost) must fit the budget. Tabu search has no natural stopping point; pick max iterations, max iterations without improvement, or wall-clock time explicitly.
- **Deterministic or stochastic runs?** Tabu search with fixed tenure and deterministic tie-breaking is deterministic given the start. With randomized tenure/tie-breaking, plan a multi-seed protocol for reporting.
- **Feasibility handling.** Will the search stay inside the feasible region (feasibility-preserving moves), or oscillate across the boundary with penalties? Strategic oscillation needs a penalty schedule.
- **Known optima or best-known values.** For QAPLIB, Taillard, OR-Library instances, best-known values exist — report gaps against them. For new problems, build a small-instance exact baseline (MIP/CP) first.
- **Cycling risk indicators.** Plateaus and symmetric solutions raise cycling risk; plan solution hashing for cycle detection and a diversification mechanism from the start, not as an afterthought.
- **Single long run vs restarts.** Decide whether the budget goes into one long run with diversification phases or several restarts from elite solutions; both need the elite pool machinery below.
- **Comparison baselines.** At minimum: best-improvement local search with random restarts, and one alternative metaheuristic (e.g., simulated annealing). A tabu list must demonstrably beat memoryless descent on your instances.

## Algorithm Anatomy

Tabu search is best-improvement local search plus memory. At iteration $t$, with current solution $x_t$, neighborhood $\mathcal{N}(x_t)$, active tabu attribute set $T_t$, and incumbent $x^*$:

$$
x_{t+1} = \operatorname*{argmin}_{y \in \mathcal{N}(x_t)} \left\{ f(y) \;:\; \text{attr}(x_t \to y) \notin T_t \;\text{ or }\; f(y) < f(x^*) \right\}
$$

The move is executed **even if $f(x_{t+1}) > f(x_t)$** — tabu search climbs out of local optima deterministically, unlike simulated annealing's probabilistic acceptance. The tabu list then forbids reversing recent moves for *tenure* $\tau$ iterations, so the search cannot fall straight back into the optimum it just left. The condition $f(y) < f(x^*)$ is the standard *improved-best aspiration*: a tabu status is overridden whenever the move reaches a new global best, because the tabu list exists to prevent cycling, and a strictly better solution cannot be a repeat.

### The three memories

| Memory | Time scale | Stores | Drives |
|---|---|---|---|
| Recency (short-term) | last $\tau$ iterations | move/solution attributes recently changed | cycle avoidance — the tabu list itself |
| Frequency (long-term) | whole run | transition counts (how often each move fired), residence counts (how long each attribute was present) | diversification: penalize over-used moves, force rarely-used assignments |
| Quality (medium-term) | whole run | elite solutions and their common features | intensification: restart from elites, fix shared attributes |

A minimal tabu search uses only recency memory. A production tabu search uses all three: recency every iteration, frequency when the search stagnates, quality when the budget allows restarts. Glover & Laguna (1997) treat this layering as the defining feature of the method.

### Move attributes: what exactly becomes tabu

The tabu list stores *attributes* of executed moves, not full solutions. The attribute granularity sets how aggressively the list prunes:

| Attribute recorded | A later move is tabu if it ... | Restrictiveness | Typical use |
|---|---|---|---|
| Full solution hash | recreates an exact previous solution | weakest — blocks only exact revisits | cycle *detection*, not prevention (hashing via fitness-evaluation-and-caching) |
| Exact inverse move, e.g. "swap positions (i, j)" | applies the inverse move | weak — the same solution can be rebuilt by other move sequences | very large neighborhoods where stronger attributes over-restrict |
| Element-position pair, e.g. "unit $r$ returns to location $\ell$" | restores a recently destroyed assignment | medium — the Ro-TS choice for QAP | assignment and permutation problems |
| Element only, e.g. "element $r$ moves at all" | touches a recently moved element | strong — freezes elements | scheduling moves with many positions per element |
| Solution feature, e.g. "arc $u \to v$ re-enters the tour/sequence" | re-creates a recently removed feature | strong, feature-aligned | TSP edges, JSP disjunctive arcs |

Rule of thumb: pick the attribute that matches what the *objective* depends on (edges for tours, assignments for QAP, arcs for schedules). Too-fine attributes let the search cycle through near-duplicates; too-coarse attributes forbid large unexplored regions and force constant aspiration overrides.

### Tenure

Tenure $\tau$ is how long an attribute stays tabu, in iterations. The classic guidance:

- **Fixed:** $\tau = 7$ was Glover's early constant; $\tau \approx \sqrt{|\mathcal{N}|}$ or $\tau \in [0.5\sqrt{n}, 2\sqrt{n}]$ are common starting points. Fixed tenure is fragile — one value rarely fits all instances.
- **Randomized per move:** draw $\tau \sim U[\tau_{\min}, \tau_{\max}]$ each time an attribute is recorded. Taillard (1991, "Robust taboo search for the quadratic assignment problem") uses $U[0.9n,\,1.1n]$ for QAP and shows the randomization itself prevents cycles that any fixed value permits. This is the recommended default.
- **Reactive:** adapt $\tau$ from observed solution repetitions (Battiti & Tecchiolli 1994, "The reactive tabu search") — see Advanced Techniques.

Symptoms: tenure too short → the search returns to the same local optimum every few iterations (detect by hashing solutions); tenure too long → objective trace shows long flat ramps because most of the neighborhood is forbidden, and the all-tabu fallback fires often.

### Aspiration criteria

1. **Improved-best (always implement):** override tabu if the move yields $f < f(x^*)$.
2. **Default / least-tabu (always implement):** if every move is tabu and none aspirates, execute the move whose tabu status expires earliest (or the best tabu move). Never skip an iteration — a frozen search wastes the remaining budget.
3. **Forced long-term aspiration (Ro-TS):** execute a move regardless of its value if it creates an assignment not seen for $A$ iterations (e.g., $A = 5n^2$). This is diversification built into the aspiration test.
4. **Regional aspiration:** override tabu if the move improves on the best solution *within the current search region* (requires defining regions; rarely worth it before the first three).

### When to choose tabu search

| Situation | Verdict |
|---|---|
| Cheap O(1)–O(n) delta evaluation, moderate neighborhood (≤ ~10⁵ moves) | Tabu search is a top contender — full-scan best-improvement exploits the delta structure SA wastes |
| QAP, job-shop, graph coloring (tabucol, Hertz & de Werra 1987), vehicle routing intra-route | Tabu search variants are or were state of the art; start here |
| Very expensive evaluation, no delta structure | Prefer methods that evaluate few candidates per iteration (ILS, SA) or fix the evaluation first |
| Huge neighborhoods (ruin-and-recreate scale) | Use large neighborhood search; tabu memory can still guard the repair |
| Highly constrained, hard-to-stay-feasible problems | Consider strategic oscillation or decoder-based methods before plain tabu search |

Per-iteration complexity = (number of candidate moves scanned) × (delta lookup cost) + (memory update cost). The QAP implementation below achieves O(n²) per iteration: O(n²) scan with O(1) lookups plus O(n²) delta-matrix maintenance.

## Generic Tabu Search Framework

The skeleton every variant shares:

```text
TABU SEARCH (minimization)
Input: initial solution x0, neighborhood N(.), tenure rule tau(.),
       aspiration test A(.), iteration budget T
x <- x0;  x_best <- x0
tabu <- empty map {attribute -> iteration until which it is active}
for t = 1 .. T:
    C <- candidate moves from N(x)              # full scan or candidate list
    admissible <- { m in C : tabu[attr_check(m)] < t  or  A(m) holds }
    if admissible is empty:
        m* <- move in C whose tabu status expires earliest   # default aspiration
    else:
        m* <- argmin_{m in admissible} f(x (+) m)   # best admissible, even uphill
    x <- x (+) m*
    tabu[attr_record(m*)] <- t + tau(t)         # forbid reversal for tau iterations
    if f(x) < f(x_best): x_best <- x
    # optional: update frequency memory; trigger diversification/intensification
return x_best
```

The generic engine below separates the four problem-specific callables (objective, move enumeration, move execution, tenure rule) from the memory logic. Use it to prototype; the two worked applications then show why production implementations specialize the scan and the delta bookkeeping for speed.

```python
import numpy as np
from dataclasses import dataclass
from collections.abc import Callable, Hashable, Iterable
from typing import Any

@dataclass(frozen=True)
class Move:
    """One candidate move: payload to execute, objective change, tabu attributes."""
    payload: Any
    delta: float
    check_key: Hashable    # move is tabu while this attribute is active
    record_key: Hashable   # attribute activated when the move is executed

def tabu_search(
    initial: Any,
    objective: Callable[[Any], float],
    enumerate_moves: Callable[[Any], Iterable[Move]],
    execute: Callable[[Any, Any], Any],
    tenure: Callable[[np.random.Generator], int],
    n_iters: int,
    seed: int = 0,
) -> tuple[Any, float, list[float]]:
    """Attribute-based best-improvement tabu search (minimization).

    Returns (best solution, best value, best-so-far trace per iteration)."""
    rng = np.random.default_rng(seed)
    current, cur_val = initial, objective(initial)
    best, best_val = current, cur_val
    tabu_until: dict[Hashable, int] = {}
    trace = [best_val]
    for t in range(1, n_iters + 1):
        chosen, chosen_val = None, np.inf
        fallback, fallback_exp = None, np.inf   # least-tabu default aspiration
        for mv in enumerate_moves(current):
            new_val = cur_val + mv.delta
            if tabu_until.get(mv.check_key, 0) >= t and new_val >= best_val:
                if tabu_until[mv.check_key] < fallback_exp:
                    fallback, fallback_exp = mv, tabu_until[mv.check_key]
                continue
            if new_val < chosen_val:
                chosen, chosen_val = mv, new_val
        if chosen is None:                      # every move tabu, none aspired
            if fallback is None:
                break                           # neighborhood empty: stop
            chosen, chosen_val = fallback, cur_val + fallback.delta
        current = execute(current, chosen.payload)
        cur_val = chosen_val
        tabu_until[chosen.record_key] = t + tenure(rng)
        if cur_val < best_val:
            best, best_val = current, cur_val
        trace.append(best_val)
    return best, best_val, trace

# Demo: QUBO  min x^T Q x  with bit-flip moves and O(n) vectorized deltas.
def qubo_flip_deltas(Q: np.ndarray, x: np.ndarray) -> np.ndarray:
    """Objective change of flipping each bit of x (Q symmetric)."""
    s, dg = Q @ x, np.diag(Q)
    return (1 - 2 * x) * (dg + 2 * (s - dg * x))

rng = np.random.default_rng(7)
n = 14
Q = rng.integers(-10, 11, (n, n))
Q = (Q + Q.T) // 2

def moves(x: np.ndarray) -> list[Move]:
    """All bit flips; attribute = flipped index (element attribute)."""
    d = qubo_flip_deltas(Q, x)
    return [Move(payload=i, delta=float(d[i]), check_key=i, record_key=i)
            for i in range(n)]

def do_flip(x: np.ndarray, i: int) -> np.ndarray:
    """Return a copy of x with bit i flipped."""
    y = x.copy()
    y[i] = 1 - y[i]
    return y

x0 = rng.integers(0, 2, n)
best, best_val, trace = tabu_search(
    x0, lambda x: float(x @ Q @ x), moves, do_flip,
    tenure=lambda g: int(g.integers(5, 9)), n_iters=200, seed=1)
bits = ((np.arange(2 ** n)[:, None] >> np.arange(n)) & 1).astype(np.int64)
exact = int(np.einsum("bi,ij,bj->b", bits, Q, bits).min())
print(best_val, exact)
# Expected: tabu search reaches -143.0, equal to the brute-force optimum -143
```

### Parameter guidance

| Parameter | Typical range | Trades off |
|---|---|---|
| Tenure $\tau$ | $U[0.9n, 1.1n]$ (QAP swaps); 8–14 (JSP arcs); $\sqrt{|\mathcal{N}|}$ as generic start | short = cycling risk; long = over-restriction, frequent fallbacks |
| Tenure regime | randomized > reactive > fixed (in robustness order) | randomized needs a range, not a value; reactive adds two meta-parameters |
| Iteration budget | $10^3$–$10^6$; or $50n$–$1000n$ without improvement | solution quality vs wall-clock time |
| Aspiration | improved-best + least-tabu fallback always; forced after $A = 5n^2$ idle | larger $A$ = less forced diversification |
| Candidate list size | 5–20 % of $\mathcal{N}$ when full scan is too slow | scan speed vs move quality per iteration |
| Diversification trigger | $0.5n$–$5n$ iterations without incumbent improvement | too eager destroys convergence; too lazy wastes budget |
| Elite pool size | 5–20 distinct solutions | memory + restart variety vs dilution with mediocre elites |
| Frequency penalty weight | scale to the median \|delta\| of accepted moves | too small = no effect; too large = frequency dictates the search |

Operator-level details (swap vs insertion neighborhoods, delta derivations per move type, perturbation design) belong to local-search-and-neighborhoods and fitness-evaluation-and-caching — this skill assumes a working neighborhood and adds memory on top.

## Worked Application 1: Robust Tabu Search for the QAP

The quadratic assignment problem: given flow matrix $F \in \mathbb{Z}^{n \times n}$ and distance matrix $D \in \mathbb{Z}^{n \times n}$, find a permutation $\pi$ (unit $u$ placed at location $\pi(u)$) minimizing

$$
C(\pi) = \sum_{u=1}^{n} \sum_{v=1}^{n} F_{uv} \, D_{\pi(u)\pi(v)}.
$$

Exact methods stall around $n \approx 30$; Taillard's robust tabu search (Ro-TS) remains the reference heuristic and the standard baseline on QAPLIB (see quadratic-assignment-problem for the problem-side view). The swap move exchanges the locations of units $r$ and $s$. With $p = \pi(r)$, $q = \pi(s)$, the cost change is computable in O(n):

$$
\Delta(\pi, r, s) = F_{rr}(D_{qq}{-}D_{pp}) + F_{rs}(D_{qp}{-}D_{pq}) + F_{sr}(D_{pq}{-}D_{qp}) + F_{ss}(D_{pp}{-}D_{qq}) + \sum_{k \neq r,s} \big[ F_{kr}(D_{\pi(k)q}{-}D_{\pi(k)p}) + F_{ks}(D_{\pi(k)p}{-}D_{\pi(k)q}) + F_{rk}(D_{q\pi(k)}{-}D_{p\pi(k)}) + F_{sk}(D_{p\pi(k)}{-}D_{q\pi(k)}) \big]
$$

Ro-TS maintains the full $\Delta$ matrix. After executing swap $(r, s)$, every pair $\{u, v\}$ disjoint from $\{r, s\}$ updates in O(1) (Taillard 1991), with $\pi$ taken *before* the swap:

$$
\Delta'(u,v) = \Delta(u,v) + (F_{ru}{-}F_{rv}{+}F_{sv}{-}F_{su})(D_{\pi(r)\pi(u)}{-}D_{\pi(r)\pi(v)}{+}D_{\pi(s)\pi(v)}{-}D_{\pi(s)\pi(u)}) + (F_{ur}{-}F_{vr}{+}F_{vs}{-}F_{us})(D_{\pi(u)\pi(r)}{-}D_{\pi(v)\pi(r)}{+}D_{\pi(v)\pi(s)}{-}D_{\pi(u)\pi(s)})
$$

Only the 2n−3 pairs touching $r$ or $s$ need the O(n) formula again, so one iteration costs O(n²) total — scan, choice, and maintenance included — versus O(n³) for naive re-evaluation. Both formulas below handle general (asymmetric) matrices and are verified against brute-force recomputation.

```python
import numpy as np

def qap_cost(F: np.ndarray, D: np.ndarray, perm: np.ndarray) -> int:
    """Full objective: sum_{u,v} F[u,v] * D[perm[u], perm[v]]."""
    return int(np.sum(F * D[np.ix_(perm, perm)]))

def swap_delta(F: np.ndarray, D: np.ndarray, perm: np.ndarray,
               r: int, s: int) -> int:
    """O(n) cost change of swapping perm[r] and perm[s] (general matrices)."""
    pr, ps = perm[r], perm[s]
    d = (F[r, r] * (D[ps, ps] - D[pr, pr])
         + F[r, s] * (D[ps, pr] - D[pr, ps])
         + F[s, r] * (D[pr, ps] - D[ps, pr])
         + F[s, s] * (D[pr, pr] - D[ps, ps]))
    idx = np.arange(len(perm))
    k = np.flatnonzero((idx != r) & (idx != s))
    pk = perm[k]
    d += int(np.sum(F[k, r] * (D[pk, ps] - D[pk, pr])
                    + F[k, s] * (D[pk, pr] - D[pk, ps])
                    + F[r, k] * (D[ps, pk] - D[pr, pk])
                    + F[s, k] * (D[pr, pk] - D[ps, pk])))
    return int(d)

def full_delta_matrix(F: np.ndarray, D: np.ndarray,
                      perm: np.ndarray) -> np.ndarray:
    """All swap deltas; O(n^3) but computed once at the start of the search."""
    n = len(perm)
    delta = np.zeros((n, n), dtype=np.int64)
    for r in range(n - 1):
        for s in range(r + 1, n):
            delta[r, s] = swap_delta(F, D, perm, r, s)
            delta[s, r] = delta[r, s]
    return delta
```

The search itself. Tabu attribute = (unit, location) pair: after moving unit $r$ away from location $\pi(r)$, the assignment "$r$ back at $\pi(r)$" is tabu for a tenure drawn uniformly from $[0.9n, 1.1n]$ — redrawn for every recording, which is what makes the method *robust* to instance-specific tuning. A swap is tabu only if **both** units would re-enter recently-left locations. Two aspiration tests: improved-best, and the forced long-term test (an assignment absent for $5n^2$ iterations forces the move) — the latter is Ro-TS's built-in frequency-style diversification.

```python
import numpy as np
# Continues the same module: uses qap_cost, swap_delta, full_delta_matrix
# from the previous block.

def robust_tabu_search(F: np.ndarray, D: np.ndarray, n_iters: int = 10_000,
                       seed: int = 0,
                       tenure: tuple[int, int] | None = None,
                       aspiration: int | None = None) -> tuple[np.ndarray, int]:
    """Taillard (1991) robust tabu search for the QAP; O(n^2) per iteration.

    Returns (best permutation, best cost)."""
    n = F.shape[0]
    rng = np.random.default_rng(seed)
    t_lo, t_hi = tenure if tenure else (int(0.9 * n), int(np.ceil(1.1 * n)))
    asp = aspiration if aspiration else 5 * n * n
    perm = rng.permutation(n)
    cost = qap_cost(F, D, perm)
    best_perm, best_cost = perm.copy(), cost
    delta = full_delta_matrix(F, D, perm)
    tabu_until = np.zeros((n, n), dtype=np.int64)      # [unit, location]
    iu, ju = np.triu_indices(n, 1)                     # all swaps, vectorized
    for t in range(1, n_iters + 1):
        d = delta[iu, ju]
        ti = tabu_until[iu, perm[ju]]   # unit iu entering location perm[ju]
        tj = tabu_until[ju, perm[iu]]   # unit ju entering location perm[iu]
        tabu = (ti >= t) & (tj >= t)    # tabu only if BOTH re-entries are recent
        aspired = (cost + d < best_cost) | (ti < t - asp) | (tj < t - asp)
        admissible = ~tabu | aspired
        if admissible.any():
            cand = np.flatnonzero(admissible)
            k = int(cand[np.argmin(d[cand])])
        else:
            k = int(np.argmin(d))       # all moves tabu: take the best anyway
        r, s = int(iu[k]), int(ju[k])
        cost += int(delta[r, s])
        a = F[r, :] - F[s, :]           # O(1)-per-pair update, pre-swap perm
        b = D[perm[r], perm] - D[perm[s], perm]
        c = F[:, r] - F[:, s]
        e = D[perm, perm[r]] - D[perm, perm[s]]
        delta += (np.subtract.outer(a, a) * np.subtract.outer(b, b)
                  + np.subtract.outer(c, c) * np.subtract.outer(e, e))
        tabu_until[r, perm[r]] = t + rng.integers(t_lo, t_hi + 1)
        tabu_until[s, perm[s]] = t + rng.integers(t_lo, t_hi + 1)
        perm[r], perm[s] = perm[s], perm[r]
        for u in range(n):              # exact O(n) refresh of pairs touching r, s
            for v in (r, s):
                if u != v:
                    dv = swap_delta(F, D, perm, u, v)
                    delta[u, v] = dv
                    delta[v, u] = dv
        if cost < best_cost:
            best_cost, best_perm = cost, perm.copy()
    return best_perm, best_cost

# Tiny synthetic instance, checked against brute force.
from itertools import permutations
rng = np.random.default_rng(42)
n = 8
F = rng.integers(0, 10, (n, n)); np.fill_diagonal(F, 0)
D = rng.integers(1, 10, (n, n)); np.fill_diagonal(D, 0)
opt = min(qap_cost(F, D, np.array(p)) for p in permutations(range(n)))
best_perm, best_cost = robust_tabu_search(F, D, n_iters=2000, seed=1)
print(opt, best_cost, qap_cost(F, D, best_perm))
# Expected: 1155 1155 1155 — Ro-TS matches the brute-force optimum, and the
# independently recomputed cost confirms the incremental bookkeeping.
```

Implementation notes that matter in practice:

- The incremental `cost` must be advanced with `delta[r, s]` **before** the outer-product update touches the matrix, and the update term must use the **pre-swap** permutation. Both orderings are easy to get wrong; the final `qap_cost` recomputation in the demo is the regression check that catches them.
- The "both re-entries recent" tabu test (logical AND) is deliberately weaker than OR. With OR, after a few iterations almost every swap is tabu and the search runs on aspiration overrides alone.
- For symmetric instances with zero diagonals the delta formula collapses to $2\sum_{k\neq r,s}(F_{sk}-F_{rk})(D_{\pi(r)\pi(k)}-D_{\pi(s)\pi(k)})$; keep the general form unless profiling says otherwise.

## Worked Application 2: Job-Shop Scheduling with a Critical-Path Neighborhood

The job-shop problem (JSP): $n$ jobs, each a fixed sequence of operations over $m$ machines, one operation per machine per job; minimize makespan $C_{\max}$. A solution is an operation order for each machine. In the disjunctive-graph view, fixing all machine orders turns the schedule into a longest-path computation: each operation's start time is the longest path from the source, and $C_{\max}$ is the longest path overall. A **critical path** is a chain of operations realizing $C_{\max}$, linked by job-precedence or machine-precedence arcs.

Two classic results make the neighborhood (van Laarhoven, Aarts & Lenstra 1992, "Job shop scheduling by simulated annealing"):

1. Swapping two **adjacent critical** operations on the same machine never creates a cycle — every such move is feasible without checking.
2. Swapping adjacent operations that are **not** both critical can never reduce the makespan — so restricting moves to critical machine-arcs loses nothing. This is a candidate list strategy that is *exact*, not approximate.

The tabu attribute is the destroyed disjunctive arc: after swapping $u$ before $v$ into $v$ before $u$ on machine $M$, re-creating arc $u \to v$ on $M$ is tabu. This is the attribute family behind the best JSP tabu searches (Taillard 1994, "Parallel taboo search techniques for the job shop scheduling problem"; Nowicki & Smutnicki 1996, "A fast taboo search algorithm for the job shop problem"). Graph machinery first:

```python
import numpy as np

def makespan(machines: np.ndarray, ptimes: np.ndarray,
             seq: list[list[int]]) -> tuple[int, np.ndarray, np.ndarray,
                                            np.ndarray, np.ndarray] | None:
    """Longest-path schedule for fixed machine sequences.

    machines[j, k] / ptimes[j, k]: machine and duration of job j's k-th op.
    seq[m]: job order on machine m. Operation id = j * n_mach + k.
    Returns (cmax, start, completion, job_pred, mach_pred); None if the
    sequences induce a cycle (only possible for externally supplied seq)."""
    n_jobs, n_mach = machines.shape
    n_ops = n_jobs * n_mach
    op_of = np.zeros((n_jobs, n_mach), dtype=np.int64)   # (job, machine) -> op
    for j in range(n_jobs):
        for k in range(n_mach):
            op_of[j, machines[j, k]] = j * n_mach + k
    p = ptimes.ravel()
    job_pred = np.full(n_ops, -1, dtype=np.int64)
    for j in range(n_jobs):
        job_pred[j * n_mach + 1: (j + 1) * n_mach] = \
            np.arange(j * n_mach, (j + 1) * n_mach - 1)
    mach_pred = np.full(n_ops, -1, dtype=np.int64)
    for m in range(n_mach):
        ops = op_of[seq[m], m]
        mach_pred[ops[1:]] = ops[:-1]
    succ_job = np.full(n_ops, -1, dtype=np.int64)
    succ_mach = np.full(n_ops, -1, dtype=np.int64)
    for o in range(n_ops):
        if job_pred[o] >= 0:
            succ_job[job_pred[o]] = o
        if mach_pred[o] >= 0:
            succ_mach[mach_pred[o]] = o
    indeg = (job_pred >= 0).astype(np.int64) + (mach_pred >= 0).astype(np.int64)
    start = np.zeros(n_ops, dtype=np.int64)
    comp = np.zeros(n_ops, dtype=np.int64)
    stack, seen = list(np.flatnonzero(indeg == 0)), 0
    while stack:                       # topological longest-path pass
        o = stack.pop()
        seen += 1
        st = 0
        if job_pred[o] >= 0:
            st = max(st, comp[job_pred[o]])
        if mach_pred[o] >= 0:
            st = max(st, comp[mach_pred[o]])
        start[o], comp[o] = st, st + p[o]
        for nx in (succ_job[o], succ_mach[o]):
            if nx >= 0:
                indeg[nx] -= 1
                if indeg[nx] == 0:
                    stack.append(nx)
    if seen < n_ops:
        return None
    return int(comp.max()), start, comp, job_pred, mach_pred

def critical_path(machines: np.ndarray, ptimes: np.ndarray,
                  seq: list[list[int]]) -> tuple[int, list[int], np.ndarray]:
    """One critical path (source to sink) and the machine-predecessor array."""
    res = makespan(machines, ptimes, seq)
    if res is None:
        raise ValueError("machine sequences induce a cycle")
    cmax, start, comp, job_pred, mach_pred = res
    o = int(np.argmax(comp))
    path = [o]
    while True:
        o = path[-1]
        if mach_pred[o] >= 0 and comp[mach_pred[o]] == start[o]:
            path.append(int(mach_pred[o]))
        elif job_pred[o] >= 0 and comp[job_pred[o]] == start[o]:
            path.append(int(job_pred[o]))
        else:
            break
    path.reverse()
    return cmax, path, mach_pred

def critical_machine_pairs(machines: np.ndarray, path: list[int],
                           mach_pred: np.ndarray) -> list[tuple[int, int, int]]:
    """Adjacent same-machine critical pairs as (machine, first_job, second_job)."""
    n_mach = machines.shape[1]
    pairs = []
    for a, b in zip(path[:-1], path[1:]):
        if mach_pred[b] == a:
            ja, jb = a // n_mach, b // n_mach
            pairs.append((int(machines[ja, a % n_mach]), int(ja), int(jb)))
    return pairs
```

The tabu search. Initial solution: order jobs on every machine by the operation's position inside its job (ties by job id) — this "level order" is provably acyclic and needs no scheduler. Tenure is randomized on a small range; the JSP arc attribute is much stronger than the QAP assignment attribute, so tenures of 8–14 work where QAP needs ~$n$. Each candidate move is evaluated by a full O(|ops|) recomputation, which is honest and simple; Taillard (1994) shows how head/tail values give an O(1) makespan *lower bound* per move when the scan itself becomes the bottleneck — see job-shop-scheduling for that refinement and for the Nowicki–Smutnicki block neighborhood.

```python
import numpy as np
# Continues the same module: uses makespan, critical_path,
# critical_machine_pairs from the previous block.

def initial_sequences(machines: np.ndarray) -> list[list[int]]:
    """Acyclic start: order jobs on each machine by op position in the job."""
    n_jobs, n_mach = machines.shape
    pos = np.zeros((n_jobs, n_mach), dtype=np.int64)
    for j in range(n_jobs):
        for k in range(n_mach):
            pos[j, machines[j, k]] = k
    return [list(np.lexsort((np.arange(n_jobs), pos[:, m])))
            for m in range(n_mach)]

def apply_swap(seq: list[list[int]], m: int, ja: int, jb: int) -> list[list[int]]:
    """Copy of seq with jobs ja, jb (adjacent on machine m, ja first) swapped."""
    new = [list(s) for s in seq]
    i = new[m].index(ja)
    new[m][i], new[m][i + 1] = jb, ja
    return new

def jsp_tabu_search(machines: np.ndarray, ptimes: np.ndarray,
                    n_iters: int = 500, tenure: tuple[int, int] = (8, 14),
                    seed: int = 0) -> tuple[list[list[int]], int]:
    """Critical-path tabu search for the JSP (N1 neighborhood).

    Tabu attribute: the destroyed machine arc (machine, first_job, second_job).
    Returns (best machine sequences, best makespan)."""
    rng = np.random.default_rng(seed)
    seq = initial_sequences(machines)
    cmax, path, mach_pred = critical_path(machines, ptimes, seq)
    best_seq, best_cmax = [list(s) for s in seq], cmax
    tabu: dict[tuple[int, int, int], int] = {}
    for t in range(1, n_iters + 1):
        pairs = critical_machine_pairs(machines, path, mach_pred)
        if not pairs:
            break                                  # cmax = max job length: optimal
        chosen, chosen_val = None, None            # (move, seq, schedule result)
        fallback, fallback_exp = None, None
        for m, ja, jb in pairs:
            cand_seq = apply_swap(seq, m, ja, jb)  # feasible by construction
            res = critical_path(machines, ptimes, cand_seq)
            val = res[0]
            if tabu.get((m, jb, ja), 0) >= t and val >= best_cmax:
                exp = tabu[(m, jb, ja)]            # tabu, no aspiration
                if fallback_exp is None or exp < fallback_exp:
                    fallback, fallback_exp = ((m, ja, jb), cand_seq, res), exp
                continue
            if chosen_val is None or val < chosen_val:
                chosen, chosen_val = ((m, ja, jb), cand_seq, res), val
        if chosen is None:                         # all tabu: least-tabu fallback
            chosen = fallback
        (m, ja, jb), seq, (cmax, path, mach_pred) = chosen
        tabu[(m, ja, jb)] = t + int(rng.integers(tenure[0], tenure[1] + 1))
        if cmax < best_cmax:
            best_cmax, best_seq = cmax, [list(s) for s in seq]
    return best_seq, best_cmax

# ft06 (Fisher & Thompson 1963), 6 jobs x 6 machines, known optimum 55.
machines = np.array([[2, 0, 1, 3, 5, 4], [1, 2, 4, 5, 0, 3],
                     [2, 3, 5, 0, 1, 4], [1, 0, 2, 3, 4, 5],
                     [2, 1, 4, 5, 0, 3], [1, 3, 5, 0, 4, 2]])
ptimes = np.array([[1, 3, 6, 7, 3, 6], [8, 5, 10, 10, 10, 4],
                   [5, 4, 8, 9, 1, 7], [5, 5, 5, 3, 8, 9],
                   [9, 3, 5, 4, 3, 1], [3, 3, 9, 10, 4, 1]])
start_cmax = critical_path(machines, ptimes, initial_sequences(machines))[0]
best_seq, best_cmax = jsp_tabu_search(machines, ptimes, n_iters=500, seed=0)
print(start_cmax, best_cmax)
# Expected: 60 55 — from the level-order start (makespan 60) the critical-path
# tabu search reaches 55, the proven optimum of ft06, within 500 iterations.
```

Two observations worth internalizing. First, the neighborhood here *is* the candidate list: instead of all O(n·m) adjacent swaps, only critical-arc swaps are scanned (typically 3–10 on ft06-sized instances), and result 2 above guarantees this filter discards no improving move. Second, the uphill steps are essential: from many schedules every critical swap increases the makespan, and a memoryless descent stops exactly there; the tabu list is what lets the search traverse those ridges without immediately undoing them.

## Advanced Techniques

### Reactive tenure

Battiti & Tecchiolli (1994) replace tenure tuning with feedback: hash every visited solution; if a solution repeats within a window, the search is cycling — increase tenure multiplicatively. If no repetition occurs for a long stretch, decay tenure so the search is no more restricted than necessary. Canonical hashing of solutions is covered in fitness-evaluation-and-caching.

```python
import numpy as np

class ReactiveTenure:
    """Battiti & Tecchiolli (1994): adapt tenure from solution repetitions."""

    def __init__(self, start: int, cap: int, window: int = 50,
                 up: float = 1.1, down: float = 0.9) -> None:
        self.tenure, self.cap, self.window = start, cap, window
        self.up, self.down = up, down
        self.seen: dict[int, int] = {}     # solution hash -> last iteration
        self.last_change = 0

    def update(self, solution_hash: int, t: int) -> int:
        """Call once per iteration with the current solution's hash."""
        last = self.seen.get(solution_hash)
        self.seen[solution_hash] = t
        if last is not None and t - last < self.window:        # cycling
            self.tenure = min(self.cap, max(self.tenure + 1,
                                            int(self.tenure * self.up)))
            self.last_change = t
        elif t - self.last_change > self.window:               # quiet: relax
            self.tenure = max(1, int(self.tenure * self.down))
            self.last_change = t
        return self.tenure

rt = ReactiveTenure(start=8, cap=40)
perm = np.array([3, 1, 0, 2])
h = hash(tuple(perm))
print(rt.update(h, t=1), rt.update(h, t=5))
# Expected: 8 9 — the repeat at t=5 (within the window) raises the tenure.
```

### Frequency-based long-term memory and diversification

Recency memory forgets after $\tau$ iterations; frequency memory never forgets. Track *transition* counts (how often each move attribute fired) and *residence* counts (how long each attribute stayed in the solution). When the incumbent stalls, enter a diversification phase: add a penalty $w \cdot \text{freq}(m)/t$ to each move's delta so the scan prefers rarely used moves, or force the least-used assignment outright (the Ro-TS forced aspiration is exactly this, embedded in the aspiration test). Scale $w$ to the median |delta| of recently accepted moves so the penalty competes with, but does not drown, the objective.

```python
import numpy as np

class FrequencyMemory:
    """Long-term transition/residence counts for a permutation problem."""

    def __init__(self, n: int) -> None:
        self.transition = np.zeros((n, n), dtype=np.int64)   # swap (i, j) count
        self.residence = np.zeros((n, n), dtype=np.int64)    # iters of i at pos
        self.iters = 0

    def record(self, perm: np.ndarray, r: int, s: int) -> None:
        """Call once per iteration, after executing swap (r, s)."""
        self.transition[r, s] += 1
        self.transition[s, r] += 1
        self.residence[np.arange(len(perm)), perm] += 1
        self.iters += 1

    def penalties(self, weight: float) -> np.ndarray:
        """Penalty matrix to ADD to the delta matrix while diversifying."""
        if self.iters == 0:
            return np.zeros_like(self.transition, dtype=np.float64)
        return weight * self.transition / self.iters

mem = FrequencyMemory(5)
perm = np.array([2, 0, 1, 4, 3])
mem.record(perm, 0, 1)
mem.record(perm, 0, 1)
mem.record(perm, 2, 3)
print(round(mem.penalties(10.0)[0, 1], 2), round(mem.penalties(10.0)[2, 3], 2))
# Expected: 6.67 3.33 — the over-used swap (0, 1) is penalized twice as hard.
```

### Intensification by restarting from elite solutions

Quality memory: keep a bounded pool of the best *distinct* solutions seen. When diversification has not produced a new incumbent for a long phase, restart the search from a random elite with a cleared (or shortened) tabu list and a fresh tenure draw — the second visit explores different uphill exits because the randomized tenure changes which reversals are forbidden. Nowicki & Smutnicki's TSAB owes much of its strength to exactly this back-jump-to-elite mechanism. A stronger variant fixes the attributes shared by all elites (common assignments, common arcs) and searches only the residual problem; path relinking between elites is the systematic version of that idea. Restart policy comparisons and diversity measurement belong to diversity-and-population-management.

```python
import numpy as np

class ElitePool:
    """Bounded pool of best distinct solutions for intensification restarts."""

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.pool: list[tuple[float, tuple[int, ...]]] = []

    def offer(self, value: float, solution: np.ndarray) -> None:
        """Insert unless duplicate; keep the `capacity` best by value."""
        key = tuple(int(v) for v in solution)
        if any(k == key for _, k in self.pool):
            return
        self.pool.append((value, key))
        self.pool.sort(key=lambda e: e[0])
        del self.pool[self.capacity:]

    def restart_from(self, rng: np.random.Generator) -> np.ndarray:
        """Pick an elite uniformly at random as the new current solution."""
        _, sol = self.pool[rng.integers(len(self.pool))]
        return np.array(sol)

pool = ElitePool(capacity=3)
for v, p in [(10, [0, 1, 2]), (8, [1, 0, 2]), (12, [2, 1, 0]),
             (8, [1, 0, 2]), (7, [2, 0, 1])]:
    pool.offer(float(v), np.array(p))
print([v for v, _ in pool.pool])
# Expected: [7.0, 8.0, 10.0] — duplicate rejected, worst (12) evicted.
```

### Candidate list strategies

When the full neighborhood scan is too slow, scan a subset — but choose the subset with structure, not blindly (Glover & Laguna 1997, ch. 3):

- **Exact filters:** problem theory proves some moves cannot improve — the JSP critical-arc restriction above is the model case. Always look for one first.
- **Elite candidate list:** scan the full neighborhood occasionally, keep the best $k$ moves; in between, scan only that list, refreshing it when its best move degrades below a threshold.
- **Successive filtering:** cheap test first (e.g., lower bound on delta), exact evaluation only for survivors.
- **Random sampling:** evaluate a random fraction per iteration; simplest, weakest, but unbiased — combine with first-improvement-style early exit.
- **Neighborhood decomposition:** partition moves (by region, machine, vehicle) and rotate through partitions; pairs naturally with frequency memory to decide which partition deserves attention.

### Strategic oscillation

For tightly constrained problems, let the search cross the feasibility boundary on purpose: allow infeasible moves with a violation penalty, increase the penalty while infeasible and decrease it while feasible (multiplicative factors ~1.2/0.85 every few iterations work as a start), and record boundary crossings in the tabu list so the oscillation does not thrash on one constraint. This turns the boundary region — where optima of capacity-style problems live — into the most-searched region instead of a wall.

## Practical Challenges

**The search still cycles despite the tabu list.** The attribute is too fine (inverse-move attributes let other move orders rebuild the same solution) or the tenure too short. Diagnose by hashing visited solutions and logging repeats (fitness-evaluation-and-caching); fix by widening the attribute (element-position or feature level), randomizing tenure over a range, or switching to reactive tenure. Cycling with period $p$ needs tenure comfortably above $p$.

**Every move is tabu and the search freezes.** Tenure is too long relative to the number of distinct attributes (a tenure of $n$ with only $2n$ attributes freezes half the neighborhood), or the attribute is too coarse. Always implement the least-tabu fallback so an iteration executes something; if the fallback fires more than a few percent of iterations, shorten tenure or refine the attribute.

**Incremental deltas drift away from the true objective.** Order-of-update bugs (cost updated after the delta matrix, update term computed with the post-swap permutation) corrupt the search silently — it still runs, just on wrong numbers. In tests, recompute the objective from scratch every $k$ iterations and compare exactly; the worked examples above end with exactly this check. Keep the independent recomputation function separate from the incremental code path.

**The neighborhood scan dominates runtime.** Profile before optimizing: if delta lookup is O(1) but the scan is a Python loop, vectorize the scan over index arrays as in the Ro-TS implementation (mask + argmin over `np.triu_indices`). If evaluation itself is the cost, install candidate lists, preferring exact filters. Only then consider numba on the inner loop.

**Aspiration never fires, or fires constantly.** Never fires: the improved-best test is too strict for long runs on large instances — fine, that is its job; check the least-tabu fallback instead. Fires constantly: tenure or attribute is over-restrictive and aspiration has become the de-facto selection rule, which silently degrades the method to plain best-improvement; fix the memory, do not loosen the aspiration further.

**Strong basins recapture the search after every escape.** The tabu list handles small basins; deep, wide basins need long-term memory. Trigger a diversification phase after $0.5n$–$5n$ improvement-free iterations: frequency-penalized selection, a forced sequence of least-used moves, or a restart from an elite plus a perturbation. If diversification phases dominate the run, the neighborhood itself is too myopic — revisit local-search-and-neighborhoods before adding more memory.

**Results are not reproducible or vary wildly across seeds.** Pass explicit `np.random.default_rng(seed)` generators everywhere (tenure draws, tie-breaking, restarts); never use global random state. Report best/mean/worst over ≥10 seeds with fixed budgets. If the across-seed spread is large, the search is start-sensitive: strengthen diversification or lengthen runs rather than cherry-picking the best seed.

**Tenure tuning consumes the project.** Stop tuning constants. Adopt randomized tenure on a range tied to instance size ($[0.9n, 1.1n]$ for QAP-like attributes, small constants for strong arc attributes), or reactive tenure. Tune the *range*, not a point value, and only on a training split of instances.

## Tools & Libraries

| Library / resource | When to use | Note |
|---|---|---|
| numpy | always — delta matrices, vectorized scans, RNG | `default_rng(seed)`; vectorize the scan before reaching for compilation |
| numba | inner move loops that resist vectorization (JSP graph passes) | `@njit` the longest-path evaluation; keep a pure-Python reference for tests |
| networkx | independent validation of longest-path / DAG claims in scheduling | use `dag_longest_path_length` as the slow oracle in unit tests |
| OR-Tools CP-SAT | exact baselines for JSP/timetabling on small-medium instances | confirms optima your tabu search should hit on test instances |
| gurobipy | exact MIP baselines; linearized QAP for tiny instances | exact methods stall ~n=30 on QAP — small instances only |
| QAPLIB / OR-Library / Taillard sets | standard benchmark instances with best-known values | report gaps to best-known, not just raw objectives |
| Optuna | tuning tenure ranges, diversification triggers, penalty weights | tune on a training instance split; hold out test instances |
| pandas | run logs and result tables (one row per run) | aggregate per instance × seed; feed statistical comparison |

## Output Format

A complete tabu search deliverable contains:

1. **Design summary table** — every memory decision made explicit:

| Component | Choice |
|---|---|
| Neighborhood | all pairwise swaps, \|N\| = n(n−1)/2, O(1) delta lookup |
| Tabu attribute | (unit, location) assignments destroyed by the move |
| Tabu test | both re-entries recent (AND) |
| Tenure | uniform on [0.9n, 1.1n], redrawn per recording |
| Aspiration | improved-best; forced after 5n² absent iterations; least-tabu fallback |
| Long-term memory | transition frequencies; diversification after 2n idle iterations |
| Intensification | elite pool of 10; restart on diversification failure |
| Budget / stopping | 10⁵ iterations or 60 s, whichever first |

2. **Run report** — one row per (instance, seed): instance name, $n$, seed, best objective, best-known value, gap %, iteration of last improvement, total iterations, wall-clock seconds. Aggregate per instance: best/mean/worst over seeds.

3. **Convergence evidence** — best-so-far trace per run (the `trace` list in the generic engine); plot mean ± range over seeds. Flag the fraction of budget after the last improvement: above ~50 % suggests the budget is wasted or diversification is broken.

4. **Validation statement** — best solutions re-checked by an independent objective recomputation (never the incremental value), feasibility verified by a separate checker, and agreement with exact baselines on all small test instances (as in both worked examples above).

5. **Artifacts** — solutions as plain arrays/JSON with instance and seed metadata; traces as CSV (iteration, current, best); the exact config (all parameters + git hash) embedded in the result file.

## Questions to Ask

- What problem and representation — permutation, assignment, sequences per machine, binary vector? Is a neighborhood with cheap delta evaluation already available?
- What instance sizes now, and at the target scale? What per-run time budget?
- Is there a known-optimum or best-known reference set for validation and gap reporting?
- Must the search stay feasible at all times, or is controlled infeasibility (penalties, oscillation) acceptable?
- Is there an existing local search to upgrade — or are we choosing among metaheuristics, in which case why tabu search over SA/ILS for this problem?
- What should be reported: single best solution, or a statistical comparison across seeds and instances?
- Any symmetry in solutions (relabeling, rotations) that makes attribute design and cycle detection harder?
- Will the implementation later need parallel runs or hybridization (e.g., tabu search inside a memetic loop) that constrain the code structure?

## Related Skills

- **local-search-and-neighborhoods** — when the neighborhood, move data structures, or delta evaluation needs design work before any memory is added; tabu search inherits all of it.
- **fitness-evaluation-and-caching** — when move evaluation is the bottleneck or cycling must be detected: O(n) QAP swap updates, canonical solution hashing, memoized evaluators.
- **quadratic-assignment-problem** — when the user works on QAP itself: formulations, linearizations, QAPLIB benchmarks, and why robust tabu search is the method of choice.
- **job-shop-scheduling** — when the user needs the full JSP toolbox: disjunctive MIP, CP-SAT interval models, Nowicki–Smutnicki block neighborhoods, shifting bottleneck.
- **diversity-and-population-management** — when stagnation persists and restart policies, diversity measurement, or population-level memory need more machinery than frequency penalties.
