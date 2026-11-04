---
name: simulated-annealing
description: When the user wants to design, implement, or tune simulated annealing for combinatorial optimization, covering Metropolis acceptance, cooling schedules (geometric, Lundy-Mees, adaptive), initial temperature calibration, reheating, and restarts. Also use when the user mentions "simulated annealing," "cooling schedule," "acceptance probability," "initial temperature," "Metropolis criterion," or when a hill climber stalls in local optima and needs a randomized escape. For move and delta-evaluation design, see local-search-and-neighborhoods; for choosing among metaheuristics, see metaheuristic-design-principles.
---

# Simulated Annealing

You are an expert in simulated annealing (SA) for combinatorial optimization. This skill covers the Metropolis acceptance rule, cooling-schedule design (geometric, Lundy-Mees, logarithmic, adaptive), initial-temperature calibration, plateau lengths, stopping rules, reheating, and restart strategies, with implementation-grade Python. Use the framework below to take a user from "local search gets stuck" to a calibrated, reproducible SA implementation with a defensible parameter story.

## Initial Assessment

Establish these facts before writing any SA code:

- **Objective and move set.** What is minimized, and what is one elementary move (swap, recolor, flip, insertion)? SA is only as good as its neighborhood; if the move set is undecided, design it first (see local-search-and-neighborhoods).
- **Delta evaluation cost.** Can the objective change of a move be computed in O(1) or O(n) instead of recomputing from scratch? SA performs millions of evaluations; without cheap deltas it is rarely competitive.
- **Problem size and evaluation budget.** Instance size, time budget in seconds, and measured moves-per-second together fix the total move count. The cooling schedule must be derived from that count, not chosen in a vacuum.
- **Hard vs soft constraints.** Decide per constraint: keep it satisfied by construction (feasibility-preserving moves such as Kempe chains), or penalize violations in the objective. Penalty weights interact with temperature, so this choice shapes calibration.
- **Objective scale.** Temperature has the same units as the objective. Note the typical magnitude of a move's objective change; calibration depends on it, not on the absolute objective value.
- **Quality requirement.** Is the goal a quick 5%-gap solution, or near-best-known on benchmark instances? The first allows a fast schedule; the second needs long plateaus, slow cooling, and replications.
- **Baseline.** Is there an existing greedy/hill-climbing baseline to beat? Always run plain first-improvement descent first; if SA cannot beat it, the temperature schedule is broken.
- **Competing methods.** If a strong problem-specific local search exists, iterated local search or tabu search often beats SA (e.g., robust tabu search dominates SA on QAP). Choose SA when the landscape is rugged, deltas are cheap, and simplicity or anytime behavior matters.
- **Reproducibility needs.** Number of seeds per instance, reporting format (best/mean/std), and whether results feed a statistical comparison.
- **Termination contract.** Wall-clock limit, move limit, target objective, or stagnation rule — pick one primary criterion now, because the schedule is derived from it.

## Algorithm Anatomy

### Metropolis acceptance

SA is local search that accepts worsening moves with a temperature-controlled probability. For minimization, a move with objective change $\Delta = f(s') - f(s)$ is accepted with

$$
P(\text{accept}) =
\begin{cases}
1 & \Delta \le 0,\\[2pt]
e^{-\Delta / T} & \Delta > 0.
\end{cases}
$$

At fixed temperature $T$ the induced Markov chain has the Boltzmann stationary distribution

$$
\pi_T(s) = \frac{e^{-f(s)/T}}{\sum_{s'} e^{-f(s')/T}},
$$

which concentrates on global minima as $T \to 0$. Two readings of $T$ help intuition:

- A move worse by exactly $T$ is accepted with probability $1/e \approx 0.37$.
- A move worse by $3T$ is accepted with probability $\approx 0.05$ — effectively the acceptance horizon.

The method comes from Metropolis et al. (1953), "Equation of State Calculations by Fast Computing Machines," applied to optimization independently by Kirkpatrick, Gelatt & Vecchi (1983), "Optimization by Simulated Annealing," and Černý (1985).

### Cooling schedules

Hajek (1988), "Cooling Schedules for Optimal Annealing," proved convergence in probability to global optima for $T_k = c/\log(k+1)$ with $c$ at least the depth of the deepest non-global local optimum. That schedule is uselessly slow in practice; finite-time SA is a heuristic and the schedule is an engineering choice:

| Schedule | Update rule | Typical setting | Character |
|---|---|---|---|
| Geometric | $T \leftarrow \alpha T$ after $L$ moves | $\alpha \in [0.90, 0.99]$, $L$ = 1-10 neighborhood sweeps | Default workhorse; two intuitive knobs |
| Lundy-Mees | $T \leftarrow T/(1+\beta T)$ after each move | $\beta$ from the budget formula below | Smooth; one move per level; Lundy & Mees (1986) |
| Linear | $T \leftarrow T - \eta$ | rarely competitive | Spends too long at useless high temperatures |
| Logarithmic | $T_k = c/\log(k+1)$ | theory only | Convergence guarantee, hopeless runtime |
| Adaptive | $\alpha$ or step from acceptance ratio / cost spread | Huang et al. (1986) | Spends budget in the critical mid-temperature band |
| Constant | $T$ fixed | Connolly (1990) for QAP | Strong if the single temperature is well chosen |

Derive geometric parameters from the budget: with `total_moves` available and `L` moves per level, the number of levels is `total_moves / L` and

$$
\alpha = \left(\frac{T_{\min}}{T_0}\right)^{L/\text{total\_moves}}.
$$

For Lundy-Mees, $1/T$ increases by $\beta$ each move, so $\beta = (T_0 - T_{\min}) / (M\, T_0\, T_{\min})$ for a budget of $M$ moves.

### Initial and final temperature

- **Acceptance-ratio calibration (recommended).** Sample a few hundred random moves from random solutions, keep the uphill deltas $\Delta^+$, and choose $T_0$ so the empirical acceptance $\chi(T_0) = \overline{e^{-\Delta^+/T_0}}$ hits a target $\chi_0$. Johnson, Aragon, McGeoch & Schevon (1989) used $\chi_0 \approx 0.8$; use 0.5 for tight budgets. The closed form $T_0 = -\overline{\Delta^+}/\ln \chi_0$ is a good start; Ben-Ameur (2004) refines it by fixed-point iteration (implemented below).
- **Do not use** $T_0 = \max \Delta$ or a multiple of the objective value: both overshoot and waste a large share of the budget on a random walk.
- **Final temperature.** Stop when a typical uphill move is accepted with negligible probability, e.g. $T_{\min} = \overline{\Delta^+} / \ln(10^3)$, or simply $T_{\min} = 10^{-4}\, T_0$, combined with a stagnation rule (no new best for $K$ levels).

### Parameter guidance

| Parameter | Typical range | Increasing it buys | At the cost of |
|---|---|---|---|
| $\chi_0$ (sets $T_0$) | 0.5 - 0.9 | More early exploration, robustness to bad starts | Budget burned on near-random walking |
| $\alpha$ | 0.90 - 0.99 (0.999 for long runs) | Better expected quality | Linear growth in runtime |
| $L$ (moves per level) | 1 - 10 × neighborhood size | Better equilibration per temperature | Fewer distinct temperatures in budget |
| $T_{\min}/T_0$ | $10^{-3}$ - $10^{-5}$ | Deeper final descent | Long frozen tail with few acceptances |
| Stagnation limit $K$ | 10 - 50 levels | Fewer premature stops | Wasted frozen iterations |
| Reheat factor | 0.1 - 0.5 × $T_0$ | Escape from late-run traps | Re-randomizes part of the progress |

With a fixed total budget, $L$ and the number of levels trade off directly; tune $\alpha$ and $\chi_0$ first, they matter most.

## Reusable SA Engine

The engine below is problem-independent: it sees solutions as numpy arrays and moves through two callables, `propose` (returns a move and its exact delta, without modifying the solution) and `apply_move` (applies it in place). All problem knowledge lives in those two functions plus the objective used once at the start.

```text
SIMULATED-ANNEALING(instance, budget)
  s  <- initial solution                 // random or greedy construction
  f  <- objective(s);  s*, f* <- s, f
  T  <- T0 calibrated so uphill acceptance ~ chi0 (0.8)
  repeat                                 // one pass = one temperature level
      for L moves:                       // L ~ 1-10 neighborhood sweeps
          m, delta <- propose random neighbor move of s
          if delta <= 0 or rand() < exp(-delta / T):
              apply m to s;  f <- f + delta
              if f < f*:  s*, f* <- s, f
      record (T, acceptance ratio, f, f*)
      T <- alpha * T                     // geometric cooling
  until T < T_min  or  no new best for K levels
  return s*, f*
```

Calibration first — this function is reused by every example:

```python
import numpy as np


def calibrate_initial_temperature(
    move_deltas: np.ndarray,
    target_acceptance: float = 0.8,
    tol: float = 1e-3,
    max_iter: int = 100,
) -> float:
    """Find T0 whose empirical uphill acceptance ratio matches the target.

    move_deltas: objective changes of random moves sampled at random
    solutions (minimization convention; only positive deltas are used).
    Starts from the closed form T0 = -mean(delta)/ln(chi0), then applies
    the fixed-point refinement of Ben-Ameur (2004), 'Computing the initial
    temperature of simulated annealing'.
    """
    deltas = np.asarray(move_deltas, dtype=float)
    deltas = deltas[deltas > 0]
    if deltas.size == 0:
        raise ValueError("no uphill deltas in sample; enlarge the move sample")
    t = float(-deltas.mean() / np.log(target_acceptance))
    for _ in range(max_iter):
        chi = float(np.exp(-deltas / t).mean())
        if abs(chi - target_acceptance) <= tol:
            break
        t *= np.log(chi) / np.log(target_acceptance)
    return t


rng = np.random.default_rng(0)
sample = rng.uniform(5.0, 15.0, size=400)  # uphill deltas centered near 10
t0 = calibrate_initial_temperature(sample, target_acceptance=0.8)
print(round(t0, 2), round(float(np.exp(-sample / t0).mean()), 3))
# Expected: T0 ~ 45 (closed form -10/ln 0.8 = 44.8) and acceptance ratio 0.8.
```

The engine, plus a complete demo on number partitioning (split a set of numbers into two groups with equal sums — a classic SA test problem from Johnson et al. 1991):

```python
import numpy as np
from collections.abc import Callable
from dataclasses import dataclass


@dataclass
class SAResult:
    """Best solution, its objective, and one history row per temperature level."""
    best: np.ndarray
    best_obj: float
    history: list[tuple[int, float, float, float, float]]
    # history row: (cumulative moves, T, acceptance ratio, current f, best f)


def simulated_annealing(
    initial: np.ndarray,
    initial_obj: float,
    propose: Callable[[np.ndarray, np.random.Generator], tuple[object, float]],
    apply_move: Callable[[np.ndarray, object], None],
    t0: float,
    alpha: float = 0.95,
    moves_per_level: int = 2000,
    t_min_factor: float = 1e-4,
    stagnation_limit: int = 25,
    seed: int = 0,
) -> SAResult:
    """Minimize with geometric-cooling SA over an in-place move interface.

    propose(current, rng) returns (move, delta) and must not modify
    `current`; apply_move(current, move) applies the move in place. The
    objective is tracked incrementally from the deltas, so deltas must be
    exact (see local-search-and-neighborhoods for delta-evaluation design).
    """
    rng = np.random.default_rng(seed)
    current = initial.copy()
    current_obj = float(initial_obj)
    best = current.copy()
    best_obj = current_obj
    t = t0
    t_min = t0 * t_min_factor
    history: list[tuple[int, float, float, float, float]] = []
    moves = 0
    stagnant = 0
    while t > t_min and stagnant < stagnation_limit:
        accepted = 0
        level_improved = False
        for _ in range(moves_per_level):
            move, delta = propose(current, rng)
            if delta <= 0.0 or rng.random() < np.exp(-delta / t):
                apply_move(current, move)
                current_obj += delta
                accepted += 1
                if current_obj < best_obj - 1e-9:
                    best_obj = current_obj
                    best = current.copy()
                    level_improved = True
        moves += moves_per_level
        history.append((moves, t, accepted / moves_per_level, current_obj, best_obj))
        stagnant = 0 if level_improved else stagnant + 1
        t *= alpha
    return SAResult(best, best_obj, history)


# Demo: number partitioning. Solution = vector of +/-1 signs; objective =
# |sum(values * signs)|, i.e. the absolute difference of the two group sums.
rng = np.random.default_rng(42)
values = rng.integers(50, 500, size=40).astype(float)


def propose_flip(sol: np.ndarray, rng: np.random.Generator) -> tuple[int, float]:
    """Move = flip one sign; exact delta from the running signed sum."""
    i = int(rng.integers(sol.size))
    signed = float(values @ sol)
    return i, abs(signed - 2.0 * sol[i] * values[i]) - abs(signed)


def apply_flip(sol: np.ndarray, i: int) -> None:
    """Apply the sign flip in place."""
    sol[i] = -sol[i]


start = np.ones(values.size)
result = simulated_annealing(
    start, float(abs(values.sum())), propose_flip, apply_flip,
    t0=float(values.mean()), alpha=0.9, moves_per_level=400, seed=7,
)
print(int(result.best_obj))
# Expected: 1 -- provably optimal here: this instance's total sum is odd,
# so no partition can do better than a difference of 1.
```

Keep the engine and the problem adapter in separate modules in real projects; the adapter is the only part that changes between problems. For richer perturbation moves to anneal over (segment reversals, scrambles, destroy-style kicks), see mutation-and-perturbation-operators.

## Worked Example 1: QAP with a Swap Neighborhood

The quadratic assignment problem places $n$ facilities at $n$ locations. With flow matrix $F$ and distance matrix $D$, and $\pi(i)$ = location of facility $i$, minimize

$$
C(\pi) = \sum_{i=1}^{n} \sum_{j=1}^{n} F_{ij}\, D_{\pi(i)\pi(j)}.
$$

The natural neighborhood swaps the locations of two facilities $r, s$. For symmetric $F, D$ with zero diagonals the objective change is computable in $O(n)$:

$$
\Delta(\pi, r, s) = 2 \sum_{k \ne r,s} \big(F_{rk} - F_{sk}\big)\big(D_{\pi(s)\pi(k)} - D_{\pi(r)\pi(k)}\big).
$$

This is the same algebra used by Burkard & Rendl (1984) for SA on QAP and by Taillard (1991) in robust tabu search. SA with this neighborhood is the classic strong-and-simple QAP baseline; Connolly (1990), "An improved annealing scheme for the QAP," showed that a well-chosen near-constant temperature works remarkably well here. For QAP-specific structure, bounds, and QAPLIB, see quadratic-assignment-problem.

```python
import itertools
import numpy as np


def qap_objective(perm: np.ndarray, flow: np.ndarray, dist: np.ndarray) -> float:
    """Full objective sum_ij flow[i,j] * dist[perm[i], perm[j]] in O(n^2)."""
    return float((flow * dist[np.ix_(perm, perm)]).sum())


def swap_delta(perm: np.ndarray, flow: np.ndarray, dist: np.ndarray,
               r: int, s: int) -> float:
    """O(n) objective change for swapping perm[r] and perm[s].

    Valid for symmetric flow/dist with zero diagonals.
    """
    pr, ps = perm[r], perm[s]
    k = np.delete(np.arange(perm.size), [r, s])
    pk = perm[k]
    return float(2.0 * ((flow[r, k] - flow[s, k])
                        * (dist[ps, pk] - dist[pr, pk])).sum())


def qap_sa(
    flow: np.ndarray,
    dist: np.ndarray,
    alpha: float = 0.95,
    sweeps_per_level: float = 2.0,
    t_min_factor: float = 1e-4,
    stagnation_limit: int = 30,
    seed: int = 0,
) -> tuple[np.ndarray, float]:
    """Simulated annealing for the symmetric QAP with the swap neighborhood."""
    rng = np.random.default_rng(seed)
    n = flow.shape[0]
    perm = rng.permutation(n)
    current = qap_objective(perm, flow, dist)
    # T0 calibration: random swap deltas at the random start, chi0 = 0.8.
    pairs = rng.integers(0, n, size=(300, 2))
    pairs = pairs[pairs[:, 0] != pairs[:, 1]]
    deltas = np.array([swap_delta(perm, flow, dist, int(r), int(s))
                       for r, s in pairs])
    uphill = deltas[deltas > 0]
    t = float(-uphill.mean() / np.log(0.8))
    t_min = t * t_min_factor
    moves_per_level = int(sweeps_per_level * n * (n - 1) / 2)
    best = perm.copy()
    best_obj = current
    stagnant = 0
    while t > t_min and stagnant < stagnation_limit:
        level_improved = False
        for _ in range(moves_per_level):
            r, s = rng.choice(n, size=2, replace=False)
            delta = swap_delta(perm, flow, dist, int(r), int(s))
            if delta <= 0.0 or rng.random() < np.exp(-delta / t):
                perm[[r, s]] = perm[[s, r]]
                current += delta
                if current < best_obj - 1e-9:
                    best_obj = current
                    best = perm.copy()
                    level_improved = True
        stagnant = 0 if level_improved else stagnant + 1
        t *= alpha
    return best, best_obj


# Tiny synthetic symmetric instance (n=8): 2x4 grid Manhattan distances,
# random symmetric integer flows with zero diagonal.
rng = np.random.default_rng(3)
xy = np.array([(i, j) for i in range(2) for j in range(4)], dtype=float)
dist = np.abs(xy[:, None, :] - xy[None, :, :]).sum(axis=2)
upper = np.triu(rng.integers(0, 10, size=(8, 8)), 1)
flow = upper + upper.T

perm, obj = qap_sa(flow, dist, seed=11)
optimum = min(qap_objective(np.array(p), flow, dist)
              for p in itertools.permutations(range(8)))
print(int(obj), int(optimum))
# Expected: both numbers are equal -- SA reaches the brute-force optimum
# of this n=8 instance (8! = 40320 permutations enumerated for reference).
```

Implementation notes:

- **The delta is the whole game.** With the O(n) formula one level of $2\binom{n}{2}$ moves costs $O(n^3)$; with naive recomputation it would cost $O(n^4)$. On QAPLIB sizes (n = 20-100) that is the difference between thousands and dozens of temperature levels in the same budget.
- **Asymmetric instances** need the general delta with all four cross terms; keep a unit test comparing `swap_delta` against `qap_objective` differences on random swaps before trusting any run.
- **Reporting**: for QAPLIB instances report percentage gap to best known values over 10+ seeds, not a single best.

## Worked Example 2: Graph Coloring with Kempe-Chain Moves

Given graph $G=(V,E)$, color vertices so adjacent vertices differ, using few colors. The Kempe-chain SA of Johnson, Aragon, McGeoch & Schevon (1991), "Optimization by Simulated Annealing: An Experimental Evaluation; Part II, Graph Coloring and Number Partitioning," anneals over **proper colorings only**:

- A **Kempe chain** for vertex $v$ (color $a$) and color $b$ is the connected component containing $v$ in the subgraph induced by vertices colored $a$ or $b$. Swapping $a \leftrightarrow b$ inside the chain keeps a proper coloring proper, because every neighbor of the chain carries a color outside $\{a,b\}$ (otherwise it would belong to the chain).
- The cost function is $f = -\sum_i |C_i|^2$ over color classes $C_i$. Minimizing it concentrates vertices into few large classes; classes empty out and the number of used colors falls as a side effect. The move's delta is $O(1)$ from the class sizes once the chain is known.
- Whole-class swaps (the chain contains all of $C_a \cup C_b$) only relabel colors; skip them, they are no-ops with delta 0 that waste acceptance statistics.

This is a textbook case of **feasibility-preserving move design**: no penalty weights to tune, and the temperature only negotiates class-size trade-offs. For DSATUR, tabucol, bounds, and the full problem treatment, see graph-coloring.

```python
import numpy as np


def greedy_coloring(adj: list[list[int]], order: np.ndarray) -> np.ndarray:
    """Proper coloring by first-fit greedy in the given vertex order."""
    colors = np.full(len(adj), -1, dtype=int)
    for v in order:
        used = {int(colors[u]) for u in adj[v] if colors[u] >= 0}
        c = 0
        while c in used:
            c += 1
        colors[v] = c
    return colors


def kempe_chain(adj: list[list[int]], colors: np.ndarray,
                v: int, b: int) -> np.ndarray:
    """Component of v in the subgraph induced by colors {colors[v], b}."""
    a = int(colors[v])
    in_chain = {v}
    stack = [v]
    while stack:
        u = stack.pop()
        for w in adj[u]:
            if w not in in_chain and int(colors[w]) in (a, b):
                in_chain.add(w)
                stack.append(w)
    return np.fromiter(in_chain, dtype=int)


def count_conflicts(adj: list[list[int]], colors: np.ndarray) -> int:
    """Independent validator: number of monochromatic edges."""
    return sum(int(colors[u] == colors[w])
               for u in range(len(adj)) for w in adj[u]) // 2


def kempe_sa(
    adj: list[list[int]],
    colors0: np.ndarray,
    t0: float,
    alpha: float = 0.93,
    moves_per_level: int = 0,
    t_min_factor: float = 1e-3,
    stagnation_limit: int = 20,
    seed: int = 0,
) -> tuple[np.ndarray, int]:
    """Anneal proper colorings under Kempe-chain interchanges.

    Cost = -sum_i |C_i|^2 (Johnson et al. 1991, part II). Properness is
    invariant under Kempe interchanges, so no conflict penalty is needed.
    Returns (best coloring, number of colors it uses).
    """
    rng = np.random.default_rng(seed)
    n = len(adj)
    colors = colors0.copy()
    if moves_per_level == 0:
        moves_per_level = 8 * n
    sizes = np.bincount(colors, minlength=n)
    current = float(-(sizes.astype(float) ** 2).sum())
    best = colors.copy()
    best_cost = current
    t = t0
    t_min = t0 * t_min_factor
    stagnant = 0
    while t > t_min and stagnant < stagnation_limit:
        level_improved = False
        for _ in range(moves_per_level):
            v = int(rng.integers(n))
            a = int(colors[v])
            nonempty = np.flatnonzero(sizes)
            choices = nonempty[nonempty != a]
            if choices.size == 0:
                continue  # a single class colors the whole graph
            b = int(rng.choice(choices))
            chain = kempe_chain(adj, colors, v, b)
            c_a = int(np.count_nonzero(colors[chain] == a))
            c_b = chain.size - c_a
            if c_a == sizes[a] and c_b == sizes[b]:
                continue  # whole-class swap = pure relabeling, skip
            na, nb = int(sizes[a]), int(sizes[b])
            na2, nb2 = na - c_a + c_b, nb - c_b + c_a
            delta = float(na ** 2 + nb ** 2 - na2 ** 2 - nb2 ** 2)
            if delta <= 0.0 or rng.random() < np.exp(-delta / t):
                to_b = chain[colors[chain] == a]
                to_a = chain[colors[chain] == b]
                colors[to_b] = b
                colors[to_a] = a
                sizes[a], sizes[b] = na2, nb2
                current += delta
                if current < best_cost - 1e-9:
                    best_cost = current
                    best = colors.copy()
                    level_improved = True
        stagnant = 0 if level_improved else stagnant + 1
        t *= alpha
    return best, int(np.unique(best).size)


# Demo: crown graph (K_{8,8} minus a perfect matching). It is bipartite,
# so 2 colors suffice, but first-fit greedy in the interleaved order
# u0, v0, u1, v1, ... is fooled into using 8 colors.
n_side = 8
adj: list[list[int]] = [[] for _ in range(2 * n_side)]
for i in range(n_side):
    for j in range(n_side):
        if i != j:
            adj[i].append(n_side + j)
            adj[n_side + j].append(i)

order = np.arange(2 * n_side).reshape(2, n_side).T.ravel()
start = greedy_coloring(adj, order)
best, n_colors = kempe_sa(adj, start, t0=16.0, seed=5)
print(int(np.unique(start).size), n_colors, count_conflicts(adj, best))
# Expected: '8 2 0' -- greedy wastes 8 colors, SA collapses them to the
# bipartite optimum of 2, and the validator confirms zero conflicts.
```

Implementation notes:

- **Chain computation is the bottleneck** ($O(|C_a| + |C_b|)$ per move via DFS on the induced subgraph). On dense graphs, cache adjacency-into-class counts if profiling shows the chain walk dominating.
- **An alternative formulation** fixes $k$ colors, allows improper colorings, and minimizes conflicting edges (the "fixed-K" scheme of the same paper); it needs penalty-vs-temperature care but handles graphs where proper colorings are hard to find. Solve a sequence of fixed-K problems with decreasing $k$.
- **Always validate independently**: `count_conflicts` recomputes feasibility without touching the incremental state, exactly like the objective re-check in the QAP example.

## Advanced Techniques

### Adaptive cooling from run feedback

Fixed $\alpha$ ignores where the search actually is. Two proven feedback rules: cool slowly while the cost distribution at a level still has large spread (the "critical region" where ordering happens), and cool fast when acceptance is near 1 (random walk) or near 0 (frozen). Huang, Romeo & Sangiovanni-Vincentelli (1986) set the next temperature from the observed cost standard deviation.

```python
import numpy as np


def huang_step(t: float, level_cost_std: float, lam: float = 0.7) -> float:
    """Huang-Romeo-Sangiovanni-Vincentelli (1986) adaptive cooling step.

    Cools slowly while the observed cost spread at the current level is
    large, and quickly once the distribution has collapsed.
    """
    if level_cost_std <= 0.0:
        return 0.5 * t
    return t * float(np.exp(-lam * t / level_cost_std))


def acceptance_guided_alpha(accept_ratio: float) -> float:
    """Spend the cooling budget where it matters: slow in the mid band.

    Acceptance above 0.9 is near-random walking and below 0.05 is frozen;
    both regimes deserve fast cooling. The 0.1-0.9 band does the ordering.
    """
    return 0.999 if 0.1 <= accept_ratio <= 0.9 else 0.9


def lundy_mees_beta(t0: float, t_final: float, total_moves: int) -> float:
    """Beta for the Lundy-Mees schedule T <- T/(1 + beta*T), one move/level.

    1/T grows by beta per move, so beta = (t0 - t_final)/(M * t0 * t_final)
    lands exactly on t_final after M moves (Lundy & Mees 1986).
    """
    return (t0 - t_final) / (total_moves * t0 * t_final)


# Budget-to-schedule mapping for a 200k-move run from T0=100 to T=0.01:
t0, t_final, total_moves, moves_per_level = 100.0, 0.01, 200_000, 2_000
alpha = (t_final / t0) ** (moves_per_level / total_moves)
print(round(alpha, 4), format(lundy_mees_beta(t0, t_final, total_moves), ".2e"))
# Expected: alpha = 0.912 (100 levels) and beta = 5.00e-04.
```

### Reheating

Late in a run the temperature is too low to cross any barrier, and a stagnating search is stuck for good. Reheating resets $T$ to a fraction of $T_0$ (0.1-0.5) when no new best has appeared for $K$ levels, then resumes cooling. It is a cheap, bounded form of restart that keeps the current solution. Use few reheats (2-4); if every reheat finds the same basin, switch to full restarts instead.

```python
import numpy as np
from collections.abc import Callable


def sa_with_reheating(
    run_level: Callable[[float, np.random.Generator], tuple[float, bool]],
    t0: float,
    alpha: float = 0.95,
    t_min_factor: float = 1e-4,
    reheat_factor: float = 0.3,
    stagnation_trigger: int = 15,
    max_reheats: int = 3,
    seed: int = 0,
) -> list[float]:
    """Outer temperature controller with reheating on stagnation.

    run_level(t, rng) executes one temperature plateau on external search
    state and returns (best objective so far, improved flag). On
    stagnation the temperature jumps back to reheat_factor * t0; after
    max_reheats the run ends. Returns the per-level best-objective trace.
    """
    rng = np.random.default_rng(seed)
    t = t0
    t_min = t0 * t_min_factor
    stagnant = 0
    reheats = 0
    trace: list[float] = []
    while t > t_min:
        best, improved = run_level(t, rng)
        trace.append(best)
        stagnant = 0 if improved else stagnant + 1
        if stagnant >= stagnation_trigger:
            if reheats >= max_reheats:
                break
            t = reheat_factor * t0
            reheats += 1
            stagnant = 0
        else:
            t *= alpha
    return trace
```

### Restarts and elite reseeding

Independent restarts with fresh seeds are the honest baseline: $R$ restarts of budget $B/R$ vs one run of budget $B$ is an empirical question — answer it on training instances, not by intuition. Two refinements: (1) restart from the best-known solution with a reheated temperature (intensifying), and (2) restart from a perturbed elite — apply a strong kick from mutation-and-perturbation-operators to the incumbent, which is exactly the bridge from SA toward iterated local search. Keep per-restart seeds and traces separate so variance across restarts is reportable.

### Parallel tempering (replica exchange)

Run $R$ replicas at a fixed temperature ladder $T_1 < \dots < T_R$ and periodically propose to exchange solutions between adjacent temperatures. Cold replicas exploit; hot replicas explore and hand good basins down the ladder. Acceptance for swapping replicas $i, i{+}1$ preserves the joint Boltzmann distribution:

```python
import numpy as np


def tempering_swap_indices(
    objs: np.ndarray, temps: np.ndarray, rng: np.random.Generator
) -> list[tuple[int, int]]:
    """One replica-exchange sweep over adjacent temperature pairs.

    Swap replicas i and i+1 with probability
    min(1, exp((1/T_i - 1/T_{i+1}) * (f_i - f_{i+1}))). Returns the
    accepted index pairs; the caller swaps both the solution states and
    the objective entries. See Earl & Deem (2005) for a survey.
    """
    swaps: list[tuple[int, int]] = []
    for i in range(temps.size - 1):
        log_p = (1.0 / temps[i] - 1.0 / temps[i + 1]) * (objs[i] - objs[i + 1])
        if log_p >= 0.0 or rng.random() < np.exp(log_p):
            swaps.append((i, i + 1))
    return swaps
```

Geometric ladders ($T_{r+1}/T_r$ constant, 5-10 replicas) work well; tune the ratio so adjacent-pair swap acceptance sits near 20-40%. This is the SA-native form of parallelism and pairs naturally with one process per replica.

### Choosing the move mix

SA tolerates heterogeneous neighborhoods: draw each move from a small pool (e.g., 80% swaps, 20% segment reversals) with fixed probabilities. Calibrate $T_0$ on the pooled delta distribution. If the pool deserves adaptive weights, that is operator selection — at that point use the machinery in metaheuristic-design-principles rather than hand-tuned mixing inside SA.

## Practical Challenges

**The acceptance ratio stays above 0.9 for most of the run.** $T_0$ is too high or the schedule too slow for the budget; the search is a random walk that only starts optimizing in the last levels. Recalibrate $T_0$ from sampled deltas with $\chi_0 = 0.8$ (or 0.5), and derive $\alpha$ from the actual move budget with the formula in Algorithm Anatomy. Log the acceptance ratio per level — it is the single most diagnostic curve an SA run produces.

**SA performs no better than hill climbing.** The temperature is effectively zero from the start: $T_0$ calibrated on the wrong delta scale (e.g., after a penalty term changed the objective units), or an aggressive $\alpha$ with long levels. Check that the first level accepts 50-90% of uphill moves; if not, the Metropolis rule never fires and you paid SA's overhead for nothing.

**The incremental objective drifts away from the true objective.** A delta-evaluation bug compounds silently over millions of moves. During development, recompute the objective from scratch every level and assert agreement within 1e-6; in the QAP example, test `swap_delta` against `qap_objective` differences on hundreds of random swaps. Keep the validator (full recomputation, feasibility check) in the codebase permanently and run it on every reported solution.

**Penalty weights and temperature fight each other.** Both scale acceptance of constraint-violating moves: doubling a penalty weight halves the temperature's effective reach on those moves. Fix penalty weights before calibrating $T_0$, express them in objective units (cost of repairing one violation), and prefer feasibility-preserving neighborhoods (Kempe chains, capacity-respecting swaps) where they exist — they remove the interaction entirely.

**Equal-cost moves dominate late in the run.** On plateaus ($\Delta = 0$ accepted always), the chain drifts without progress and stagnation detection misfires. Options: accept zero-delta moves with probability 0.5, add a tiny lexicographic tie-breaker to the objective, or treat repeated zero-delta acceptance at low temperature as frozen and trigger the stopping rule.

**Results are irreproducible across runs.** Every random decision must flow from one `np.random.default_rng(seed)` instance per run; never touch the global numpy state. Store (instance, seed, parameters, best objective, time) for every run; report mean and std over 10+ seeds, not a single lucky best. This is the minimum for any comparison a reviewer will accept.

**The budget is wall-clock seconds but the schedule needs a move count.** Measure moves-per-second on the target instance in a 2-second probe, convert the time limit into `total_moves`, then derive $\alpha$ (or the Lundy-Mees $\beta$) from it. Re-derive when the instance size changes — schedules do not transfer across sizes because neighborhood size and delta cost both scale.

**Performance is poor and profiling shows evaluation dominates.** Vectorize the delta (as in `swap_delta`), or move the inner loop to numba; SA's sequential acceptance makes population-style vectorization impossible, so the delta is the only lever. If the objective is genuinely expensive (simulation-based), SA's million-move appetite is the wrong fit — reconsider the method choice in metaheuristic-design-principles.

## Tools & Libraries

| Library | When to use | Note |
|---|---|---|
| numpy | Always | The substrate for every implementation in this skill; vectorized deltas, `default_rng` |
| simanneal (PyPI) | Quick prototypes, small instances | Clean Annealer class, but deep-copies state per move — too slow for serious runs |
| scipy `dual_annealing` | Continuous box-constrained problems | Generalized SA + local refinement; not for combinatorial neighborhoods |
| numba | Hot inner loops after profiling | JIT the move/delta loop; keep the rng inside the jitted function |
| alns (PyPI) | Destroy/repair searches | Provides SA-style acceptance criteria inside an ALNS loop |
| Timefold (JVM) | Enterprise planning problems | Production solver whose acceptor menu includes simulated annealing |
| pandas / matplotlib | Experiment tables and convergence plots | One row per run; best-so-far curves with bands over seeds |

## Output Format

A complete SA deliverable contains:

1. **Configuration summary** — every number a reader needs to reproduce the schedule:

| Item | Value | How it was set |
|---|---|---|
| Neighborhood | facility swap | problem analysis |
| $T_0$ | 184.2 | $\chi_0 = 0.8$ on 300 sampled deltas (Ben-Ameur refinement) |
| Schedule | geometric, $\alpha = 0.95$ | derived from 5 s budget at 1.1M moves/s |
| Moves per level | $2 \binom{n}{2}$ | 2 neighborhood sweeps |
| Stop | $T < 10^{-4} T_0$ or 30 stagnant levels | default |
| Seeds | 0-9 | 10 replications |

2. **Convergence report** — per-level history table (moves, $T$, acceptance ratio, current, best) or a best-so-far plot with a band over seeds; the acceptance-ratio column doubles as the schedule diagnostic.
3. **Solution quality** — best/mean/std objective over seeds; gap to optimum, best-known value, or a lower bound where available; time to best.
4. **Validation statement** — the reported solution re-checked by an independent function: feasibility confirmed and objective recomputed from scratch (e.g., `count_conflicts(...) == 0`, `qap_objective(best, ...) == reported`).
5. **Artifacts** — the engine module, the problem adapter (propose/apply/objective), the run script with seeds, and the results table (one row per run) ready for statistical comparison.

State explicitly which parameters were tuned and on which instances, so tuned-on and reported-on instance sets are visibly separate.

## Questions to Ask

- What is one elementary move on your solution, and can its objective change be computed without full recomputation?
- What is the time budget per run, and on what hardware — i.e., how many moves can we afford?
- Which constraints must never be violated, and which can be penalized during the search?
- What is the typical objective change of a random move (rough order of magnitude)?
- Is there an existing greedy or local-search baseline, and what does it score?
- Do you need one good solution, or a distribution over many seeds for a paper-grade comparison?
- Are benchmark instances with best-known values available (e.g., QAPLIB, DIMACS coloring)?
- Should the final solution be polished by a deterministic local search after annealing ends?
- Is the objective deterministic? Noisy objectives change acceptance behavior and need re-evaluation strategies.

## Related Skills

- **local-search-and-neighborhoods** — when the move set, scanning order, or O(1)/O(n) delta evaluation needs design work; SA inherits all of it.
- **mutation-and-perturbation-operators** — for the catalog of moves to anneal over (swaps, insertions, inversions, destroy-style kicks) and perturbation-strength control.
- **metaheuristic-design-principles** — when choosing whether SA is the right method at all, and for constraint handling, stopping criteria, and evaluation budgeting.
- **graph-coloring** — for the full coloring problem treatment (DSATUR, tabucol, bounds, benchmarks) beyond the Kempe-chain example here.
- **quadratic-assignment-problem** — for QAP-specific structure, linearizations, robust tabu search, and QAPLIB benchmarking beyond the SA baseline here.
