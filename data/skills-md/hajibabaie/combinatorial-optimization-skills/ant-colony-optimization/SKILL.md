---
name: ant-colony-optimization
description: When the user wants to design, implement, or tune ant colony optimization for combinatorial problems, including pheromone model design, visibility heuristics, and choosing among Ant System, Ant Colony System, and MAX-MIN Ant System. Also use when the user mentions "ant colony," "ACO," "pheromone," "MMAS," "ant colony system," "pheromone evaporation," "pheromone trail," "construction graph," or when solutions are built component-by-component guided by learned trail values. For tour neighborhoods and 2-opt machinery, see local-search-and-neighborhoods; for TSP formulations and benchmarks, see traveling-salesman-problem.
---

# Ant Colony Optimization

You are an expert in ant colony optimization (ACO) for combinatorial optimization. This skill covers
pheromone models, visibility (heuristic) information, the main variants — Ant System, Ant Colony
System (ACS), and MAX-MIN Ant System (MMAS) — pheromone trail limits, hybridization with local
search, and the design of construction graphs for problems beyond routing. Use the framework below
to select a variant, build a correct and fast implementation, and diagnose convergence behavior.

## Initial Assessment

Establish the following before writing any code or recommending a configuration:

- **Problem class and construction graph.** Identify the sequential decisions an ant makes: edge
  pheromones for routing, (item, position) pairs for assignment, per-item trails for subset
  problems. If no natural sequential construction exists, ACO is a poor fit.
- **Instance size.** The pheromone matrix is O(n^2) memory and a naive construction step is O(n).
  For n above a few thousand, candidate lists and vectorized construction are mandatory.
- **Heuristic information.** Check whether a greedy desirability measure (eta) exists, e.g. inverse
  distance for TSP. Without one (QAP, much of scheduling), plan for beta = 0 and lean on local search.
- **Local search availability.** ACO without local search is rarely competitive on classic
  benchmarks (Dorigo & Stützle 2004, Ant Colony Optimization). Confirm a delta-evaluable
  improvement procedure exists before promising results.
- **Evaluation cost.** Count objective evaluations per iteration: ants × (construction + local
  search). If the objective is expensive, shrink the colony and deepen local search.
- **Time budget and termination.** Fix a wall-clock or iteration budget up front; ACO has no
  natural stopping point. Plan stagnation detection and restarts for long runs.
- **Quality target.** Determine whether the goal is "good feasible quickly" (favor ACS, high q0) or
  "near-optimal given hours" (favor MMAS with restarts and strong local search).
- **Constraint structure.** Decide whether construction can always stay feasible (visit-once
  constraints are free in permutation construction) or whether a repair/penalty layer is needed.
- **Baseline.** Multi-start local search at the same evaluation budget is the honest baseline;
  ACO must beat it to justify its complexity.
- **Reproducibility.** Require seeded runs (`np.random.default_rng(seed)`) and multiple seeds per instance.

## Algorithm Anatomy

### Construction graph and transition rule

ACO builds solutions component by component on a construction graph. Ant k at decision point i
chooses the next component j from the feasible neighborhood N_i^k with the **random proportional
rule** of Ant System (Dorigo, Maniezzo & Colorni 1996, Ant System):

$$
p_{ij}^{k} \;=\; \frac{\tau_{ij}^{\alpha}\,\eta_{ij}^{\beta}}
{\sum_{l \in N_i^{k}} \tau_{il}^{\alpha}\,\eta_{il}^{\beta}},
\qquad j \in N_i^{k},
$$

where tau is the learned pheromone trail and eta the static heuristic desirability (for TSP,
eta_ij = 1/d_ij). Alpha and beta weight learning against greediness.

### Pheromone update

After all m ants finish, Ant System evaporates and deposits:

$$
\tau_{ij} \;\leftarrow\; (1-\rho)\,\tau_{ij} \;+\; \sum_{k=1}^{m} \Delta\tau_{ij}^{k},
\qquad
\Delta\tau_{ij}^{k} =
\begin{cases}
1/C^{k} & \text{if ant } k \text{ used component } (i,j),\\
0 & \text{otherwise,}
\end{cases}
$$

with C^k the cost of ant k's solution. Evaporation rate rho in (0, 1] controls how fast the colony
forgets. The two strong modern variants change *who deposits* and *how trails are bounded*.

### Variant comparison

| Variant | Who deposits | Selection rule | Extra mechanics | Use when |
|---|---|---|---|---|
| Ant System (1996) | all ants | random proportional | none | teaching, baselines only |
| Elitist / Rank-based AS | best + top-ranked ants | random proportional | weighted deposits | mild upgrade of AS; mostly historical |
| ACS (Dorigo & Gambardella 1997) | best-so-far only | pseudorandom proportional (q0) | local evaporation during construction | small budgets, fast convergence, online/dynamic problems |
| MMAS (Stützle & Hoos 2000) | iteration-best / best-so-far schedule | random proportional | trail limits [tau_min, tau_max], restarts | robust default, best with local search |

**ACS mechanics.** With probability q0 the ant exploits: j = argmax over N of tau_il * eta_il^beta;
otherwise it samples with the random proportional rule. Each ant also applies a **local update**
while constructing, tau_ij <- (1 - xi) tau_ij + xi tau_0 with tau_0 = 1 / (n * C_nn), which makes
edges less attractive immediately after use and decorrelates ants within one iteration. The global
update evaporates and deposits only on the best-so-far solution's components.

**MMAS mechanics.** Only the iteration-best or best-so-far ant deposits. All trails are clamped to
[tau_min, tau_max] and initialized at tau_max, which forces early exploration and provably prevents
the probability of any component from reaching 0 or 1:

$$
\tau_{\max} = \frac{1}{\rho\,C^{bs}},
\qquad
\tau_{\min} = \tau_{\max}\cdot
\frac{1 - p_{\mathrm{best}}^{1/n}}{(\,n/2 - 1\,)\;p_{\mathrm{best}}^{1/n}},
$$

where p_best (e.g. 0.05) is the target probability of reconstructing the current best solution at
full convergence, and n/2 estimates the average number of choices per step. When trails stagnate,
MMAS resets all trails to tau_max (a restart).

### Pheromone models beyond routing

The pheromone must index the decision you want the colony to learn. Standard designs:

| Problem family | Pheromone index tau | Visibility eta | Deposit on |
|---|---|---|---|
| Routing (TSP, VRP) | edge (i, j) | 1/d_ij | edges of the tour/routes |
| Assignment (QAP, timetabling) | pair (item i, location/value k) | usually none (beta = 0) | chosen (item, location) pairs |
| Subset selection (knapsack, set covering) | item i | profit/weight or cover ratio | chosen items |
| Sequencing/scheduling (flow shop, RCPSP) | (job j, position p) | priority-rule value | chosen positions, read with the summation rule |

Design rules: (1) solution quality must map monotonically to deposit (use 1/C for minimization);
(2) the trail consulted at a decision must be conditionally meaningful — in position-based
scheduling models the raw trail tau[j, p] misleads, so the summation rule (Merkle, Middendorf &
Schmeck 2002) reads sum over q <= p of tau[j, q] instead; (3) keep the pheromone O(n^2) or smaller.

### Decision guidance

- Default to **MMAS + local search on every ant**: it is the most robust published configuration
  for TSP- and QAP-like problems.
- Choose **ACS** when the evaluation budget is small, you need good solutions within seconds, or
  the problem changes online (local evaporation adapts faster).
- Per-iteration cost is O(m·n^2) for full construction scans, O(m·n·cl) with candidate lists of
  size cl, plus local search. Memory is O(n^2) for tau (and eta if dense).
- Prefer a different metaheuristic when there is no sequential construction (pure binary flips),
  when the problem is continuous, or when evaluations are too expensive for population sampling.

## Generic MMAS Framework

The only problem-specific elements of ACO are the construction procedure, the evaluation, and the
mapping from a solution to the pheromone entries it used. The framework below owns everything
else: pheromone memory, trail limits, evaporation, deposit scheduling, best-so-far bookkeeping.
For the `improve` step see **local-search-and-neighborhoods**; for cheap `evaluate` see
**fitness-evaluation-and-caching**.

```text
MMAS skeleton
-------------
initialize tau[i][j] := tau_max estimated from a quick starting solution
repeat for n_iterations:
    for each of m ants:
        s := construct(tau, rng)            # problem-specific, random proportional rule
        s := improve(s)                     # optional local search
    update iteration-best and best-so-far
    recompute tau_max := 1 / (rho * C_best),  tau_min from p_best
    tau := (1 - rho) * tau                  # evaporation
    pick deposit solution: iteration-best, every gb_every-th iteration best-so-far
    tau[components of deposit solution] += 1 / C_deposit
    clip tau into [tau_min, tau_max]; (optionally) restart tau := tau_max on stagnation
return best-so-far
```

```python
"""Reusable MAX-MIN Ant System core: pheromone memory, trail limits, updates.

Problem-specific parts are injected as callables:
  construct(tau, rng) -> solution        build one solution from trail values
  evaluate(solution)  -> float           minimization objective
  deposit(solution)   -> (rows, cols)    pheromone entries the solution used
  improve(solution)   -> solution        optional local search
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np


@dataclass
class MMASConfig:
    """MMAS parameters (Stützle & Hoos 2000, MAX-MIN Ant System)."""

    n_ants: int = 25
    rho: float = 0.2          # evaporation rate in (0, 1]
    p_best: float = 0.05      # target probability of rebuilding the best solution
    n_iterations: int = 500
    gb_every: int = 25        # deposit best-so-far every gb_every iterations
    seed: int = 0


def trail_limits(best_cost: float, rho: float, p_best: float, n: int) -> tuple[float, float]:
    """Return (tau_min, tau_max): tau_max = 1/(rho*C_best), tau_min from p_best."""
    tau_max = 1.0 / (rho * best_cost)
    p = p_best ** (1.0 / n)
    tau_min = tau_max * (1.0 - p) / ((n / 2.0 - 1.0) * p)
    return min(tau_min, tau_max), tau_max


def run_mmas(
    n: int,
    construct: Callable[[np.ndarray, np.random.Generator], np.ndarray],
    evaluate: Callable[[np.ndarray], float],
    deposit: Callable[[np.ndarray], tuple[np.ndarray, np.ndarray]],
    cfg: MMASConfig,
    improve: Callable[[np.ndarray], np.ndarray] | None = None,
) -> tuple[np.ndarray, float, list[float]]:
    """Run MMAS; return (best solution, best cost, best-so-far history)."""
    rng = np.random.default_rng(cfg.seed)
    tau = np.full((n, n), 1.0)            # rescaled to tau_max after iteration 0
    best_sol = np.empty(0, dtype=np.int64)
    best_cost = float("inf")
    history: list[float] = []
    for it in range(cfg.n_iterations):
        iter_sol, iter_cost = best_sol, float("inf")
        for _ in range(cfg.n_ants):
            sol = construct(tau, rng)
            if improve is not None:
                sol = improve(sol)
            cost = evaluate(sol)
            if cost < iter_cost:
                iter_sol, iter_cost = sol, cost
        if iter_cost < best_cost:
            best_sol, best_cost = iter_sol.copy(), iter_cost
        tau_min, tau_max = trail_limits(best_cost, cfg.rho, cfg.p_best, n)
        if it == 0:
            tau.fill(tau_max)             # MMAS initialization at the upper limit
        tau *= 1.0 - cfg.rho
        use_gb = (it + 1) % cfg.gb_every == 0
        dep_sol, dep_cost = (best_sol, best_cost) if use_gb else (iter_sol, iter_cost)
        rows, cols = deposit(dep_sol)
        tau[rows, cols] += 1.0 / dep_cost
        np.clip(tau, tau_min, tau_max, out=tau)
        history.append(best_cost)
    return best_sol, best_cost, history


if __name__ == "__main__":
    # Tiny demo: 10-city Euclidean TSP wired into the framework via closures.
    rng0 = np.random.default_rng(42)
    pts = rng0.random((10, 2))
    dist = np.sqrt(((pts[:, None, :] - pts[None, :, :]) ** 2).sum(axis=2))
    eta_b = (1.0 / np.maximum(dist, 1e-9)) ** 2.0          # beta = 2 folded into eta

    def construct(tau: np.ndarray, rng: np.random.Generator) -> np.ndarray:
        n = tau.shape[0]
        tour = np.empty(n, dtype=np.int64)
        visited = np.zeros(n, dtype=bool)
        cur = int(rng.integers(n))
        tour[0] = cur
        visited[cur] = True
        for step in range(1, n):
            cand = np.flatnonzero(~visited)
            w = tau[cur, cand] * eta_b[cur, cand]          # alpha = 1
            cur = int(cand[rng.choice(cand.size, p=w / w.sum())])
            tour[step] = cur
            visited[cur] = True
        return tour

    def evaluate(tour: np.ndarray) -> float:
        return float(dist[tour, np.roll(tour, -1)].sum())

    def deposit(tour: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        nxt = np.roll(tour, -1)                            # symmetric deposit
        return np.concatenate([tour, nxt]), np.concatenate([nxt, tour])

    sol, cost, hist = run_mmas(
        10, construct, evaluate, deposit, MMASConfig(n_ants=10, n_iterations=120, seed=7)
    )
    print(f"10-city tour length: {cost:.4f}")
    # Expected: a valid 10-city tour; length typically 2.5-3.2 and equal to the
    # optimum for most seeds (10 uniform points; exhaustive check is feasible).
```

### Parameter guidance

| Parameter | Typical range | What it trades off |
|---|---|---|
| m (ants per iteration) | 10–50; with local search 10–25 | sampling breadth per iteration vs. iterations within the budget |
| alpha (trail weight) | 1.0, rarely tuned | >1 amplifies trail differences — faster convergence, higher stagnation risk |
| beta (visibility weight) | 2–5 (0 when no eta exists) | high beta = greedy and strong early; low beta lets learned trails dominate |
| rho (evaporation) | MMAS: 0.2 with local search, 0.02 without; ACS: 0.1 | fast forgetting adapts quickly but is unstable; slow forgetting learns slowly |
| q0 (ACS exploitation) | 0.7–0.95 | exploitation of the best-known components vs. exploration during construction |
| xi (ACS local update) | 0.1 | stronger local evaporation decorrelates ants inside one iteration |
| p_best (MMAS) | 0.005–0.05 | smaller value raises tau_min — more exploration, slower convergence |
| cl (candidate list size) | 10–30 | smaller is faster and usually better; too small can exclude needed edges |
| gb_every (deposit schedule) | start 25, decrease over the run | iteration-best favors exploration; best-so-far accelerates convergence |

## Worked Example 1: TSP with MMAS + 2-opt

The reference configuration from Stützle & Hoos (2000): MMAS with a nearest-neighbor candidate
list, 2-opt applied to every ant's tour, deposit alternating between iteration-best and
best-so-far. The 2-opt here is a compact best-improvement version with a vectorized move scan; for
don't-look bits, neighbor-list pruning, and Or-opt see **local-search-and-neighborhoods**.

```python
"""TSP utilities for the MMAS worked example: instance, 2-opt, candidate lists."""
from __future__ import annotations

import numpy as np


def euclidean_instance(n: int, seed: int) -> np.ndarray:
    """n random points in the unit square -> (n, n) Euclidean distance matrix."""
    rng = np.random.default_rng(seed)
    pts = rng.random((n, 2))
    diff = pts[:, None, :] - pts[None, :, :]
    return np.sqrt((diff * diff).sum(axis=2))


def tour_length(tour: np.ndarray, dist: np.ndarray) -> float:
    """Cyclic tour length."""
    return float(dist[tour, np.roll(tour, -1)].sum())


def two_opt(tour: np.ndarray, dist: np.ndarray) -> np.ndarray:
    """Best-improvement 2-opt with a vectorized move scan per anchor edge."""
    tour = tour.copy()
    n = tour.size
    improved = True
    while improved:
        improved = False
        succ = np.roll(tour, -1)
        d_cur = dist[tour, succ]
        for i in range(n - 2):
            a, b = tour[i], tour[i + 1]
            j_hi = n - 1 if i == 0 else n      # skip the move that flips the whole tour
            js = np.arange(i + 2, j_hi)
            if js.size == 0:
                continue
            c, d = tour[js], succ[js]
            delta = dist[a, c] + dist[b, d] - d_cur[i] - d_cur[js]
            k = int(np.argmin(delta))
            if delta[k] < -1e-12:
                j = int(js[k])
                tour[i + 1 : j + 1] = tour[i + 1 : j + 1][::-1]
                improved = True
                succ = np.roll(tour, -1)
                d_cur = dist[tour, succ]
    return tour


def nn_candidate_lists(dist: np.ndarray, cl: int) -> np.ndarray:
    """cl nearest neighbors per city, excluding the city itself; shape (n, cl)."""
    order = np.argsort(dist, axis=1)
    return order[:, 1 : cl + 1]


if __name__ == "__main__":
    dist = euclidean_instance(30, seed=0)
    rng = np.random.default_rng(1)
    rand_tour = rng.permutation(30).astype(np.int64)
    opt_tour = two_opt(rand_tour, dist)
    print(f"random: {tour_length(rand_tour, dist):.3f} -> 2-opt: {tour_length(opt_tour, dist):.3f}")
    # Expected: 2-opt shortens a random tour substantially, e.g. ~14-17 down to ~4.4-5.0.
```

The MMAS driver below continues the same module (it calls the helpers defined above; imports are
repeated so the block parses on its own). The weight matrix `tau**alpha * eta**beta` is recomputed
once per iteration and shared by all ants — trails do not change during MMAS construction.

```python
"""MMAS for the symmetric TSP with 2-opt on every ant (same module as above)."""
from __future__ import annotations

import numpy as np


def construct_tour(w: np.ndarray, cand: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """One ant: random proportional rule on the candidate list, full-scan fallback."""
    n = w.shape[0]
    tour = np.empty(n, dtype=np.int64)
    visited = np.zeros(n, dtype=bool)
    cur = int(rng.integers(n))
    tour[0] = cur
    visited[cur] = True
    for step in range(1, n):
        nbrs = cand[cur]
        nbrs = nbrs[~visited[nbrs]]
        if nbrs.size == 0:                       # candidate list exhausted
            nbrs = np.flatnonzero(~visited)
        weights = w[cur, nbrs]
        total = weights.sum()
        if total > 0.0:
            cur = int(nbrs[rng.choice(nbrs.size, p=weights / total)])
        else:
            cur = int(nbrs[rng.integers(nbrs.size)])
        tour[step] = cur
        visited[cur] = True
    return tour


def mmas_tsp(
    dist: np.ndarray,
    n_ants: int = 20,
    alpha: float = 1.0,
    beta: float = 3.0,
    rho: float = 0.2,
    p_best: float = 0.05,
    cl: int = 15,
    n_iterations: int = 300,
    gb_every: int = 25,
    seed: int = 0,
) -> tuple[np.ndarray, float, list[float]]:
    """MAX-MIN Ant System for symmetric TSP, 2-opt applied to every ant's tour."""
    n = dist.shape[0]
    rng = np.random.default_rng(seed)
    eta_beta = (1.0 / np.maximum(dist, 1e-12)) ** beta
    np.fill_diagonal(eta_beta, 0.0)
    cand = nn_candidate_lists(dist, min(cl, n - 1))
    start = two_opt(rng.permutation(n).astype(np.int64), dist)
    best_tour, best_cost = start, tour_length(start, dist)
    tau = np.full((n, n), 1.0 / (rho * best_cost))         # tau_max initialization
    history: list[float] = []
    for it in range(n_iterations):
        w = (tau ** alpha) * eta_beta                      # shared by all ants
        iter_tour, iter_cost = best_tour, float("inf")
        for _ in range(n_ants):
            tour = two_opt(construct_tour(w, cand, rng), dist)
            cost = tour_length(tour, dist)
            if cost < iter_cost:
                iter_tour, iter_cost = tour, cost
        if iter_cost < best_cost:
            best_tour, best_cost = iter_tour.copy(), iter_cost
        tau_max = 1.0 / (rho * best_cost)
        p = p_best ** (1.0 / n)
        tau_min = min(tau_max, tau_max * (1.0 - p) / ((n / 2.0 - 1.0) * p))
        tau *= 1.0 - rho
        dep = best_tour if (it + 1) % gb_every == 0 else iter_tour
        dep_cost = tour_length(dep, dist)
        nxt = np.roll(dep, -1)
        tau[dep, nxt] += 1.0 / dep_cost                    # symmetric deposit
        tau[nxt, dep] += 1.0 / dep_cost
        np.clip(tau, tau_min, tau_max, out=tau)
        history.append(best_cost)
    return best_tour, best_cost, history


if __name__ == "__main__":
    dist = euclidean_instance(40, seed=42)
    tour, cost, hist = mmas_tsp(dist, n_iterations=120, seed=1)
    assert sorted(tour.tolist()) == list(range(40))
    assert all(a >= b for a, b in zip(hist, hist[1:]))     # best-so-far never worsens
    print(f"best tour length: {cost:.4f}")
    # Expected: a valid 40-city tour with length ~5.0-5.5; the best-so-far history
    # is non-increasing and the final value matches or beats multi-start 2-opt.
```

Implementation notes: candidate lists change construction from O(n) to O(cl) per step and usually
*improve* quality, because long edges are excluded from sampling. Initialization at tau_max keeps
early iterations close to a randomized greedy heuristic; learning takes over as trails
differentiate. For symmetric TSP deposit on both (i, j) and (j, i); for asymmetric TSP deposit
only on the directed arcs actually traversed.

## Variant Mechanics: Ant Colony System

ACS converges faster than MMAS at the price of less exploration; it is the better choice for
tight time budgets. The block below isolates ACS without local search so the three differences are
visible: pseudorandom proportional rule, in-construction local update, best-so-far-only global update.

```python
"""Ant Colony System for symmetric TSP (Dorigo & Gambardella 1997)."""
from __future__ import annotations

import numpy as np


def nearest_neighbor_cost(dist: np.ndarray) -> float:
    """Length of the nearest-neighbor tour from city 0, used to calibrate tau_0."""
    n = dist.shape[0]
    visited = np.zeros(n, dtype=bool)
    visited[0] = True
    cur, total = 0, 0.0
    for _ in range(n - 1):
        d = np.where(visited, np.inf, dist[cur])
        nxt = int(np.argmin(d))
        total += dist[cur, nxt]
        visited[nxt] = True
        cur = nxt
    return total + dist[cur, 0]


def acs_tsp(
    dist: np.ndarray,
    n_ants: int = 10,
    beta: float = 2.0,
    rho: float = 0.1,
    xi: float = 0.1,
    q0: float = 0.9,
    n_iterations: int = 400,
    seed: int = 0,
) -> tuple[np.ndarray, float]:
    """ACS without local search, to isolate the variant's mechanics."""
    n = dist.shape[0]
    rng = np.random.default_rng(seed)
    eta_beta = (1.0 / np.maximum(dist, 1e-12)) ** beta
    np.fill_diagonal(eta_beta, 0.0)
    tau0 = 1.0 / (n * nearest_neighbor_cost(dist))
    tau = np.full((n, n), tau0)
    best_tour = np.arange(n, dtype=np.int64)
    best_cost = float(dist[best_tour, np.roll(best_tour, -1)].sum())
    for _ in range(n_iterations):
        for _ in range(n_ants):
            tour = np.empty(n, dtype=np.int64)
            visited = np.zeros(n, dtype=bool)
            cur = int(rng.integers(n))
            tour[0] = cur
            visited[cur] = True
            for step in range(1, n):
                cand = np.flatnonzero(~visited)
                scores = tau[cur, cand] * eta_beta[cur, cand]
                if rng.random() < q0:                      # exploit
                    nxt = int(cand[np.argmax(scores)])
                else:                                      # biased exploration
                    total = scores.sum()
                    if total > 0.0:
                        nxt = int(cand[rng.choice(cand.size, p=scores / total)])
                    else:
                        nxt = int(rng.choice(cand))
                tau[cur, nxt] = (1.0 - xi) * tau[cur, nxt] + xi * tau0   # local update
                tau[nxt, cur] = tau[cur, nxt]
                tour[step] = nxt
                visited[nxt] = True
                cur = nxt
            cost = float(dist[tour, np.roll(tour, -1)].sum())
            if cost < best_cost:
                best_tour, best_cost = tour.copy(), cost
        nxt_b = np.roll(best_tour, -1)                     # global update: best edges only
        tau[best_tour, nxt_b] = (1.0 - rho) * tau[best_tour, nxt_b] + rho / best_cost
        tau[nxt_b, best_tour] = tau[best_tour, nxt_b]
    return best_tour, best_cost


if __name__ == "__main__":
    rng = np.random.default_rng(5)
    pts = rng.random((30, 2))
    dist = np.sqrt(((pts[:, None, :] - pts[None, :, :]) ** 2).sum(axis=2))
    tour, cost = acs_tsp(dist, n_iterations=250, seed=2)
    assert sorted(tour.tolist()) == list(range(30))
    print(f"ACS tour length: {cost:.4f}")
    # Expected: a valid 30-city tour, length ~4.4-5.0 without local search; adding
    # 2-opt per ant (as in the MMAS example) closes most of the remaining gap.
```

Note the asymmetry of the global update: in ACS, evaporation touches only the best-so-far edges.
This is what makes ACS aggressive — the matrix drifts toward tau0 while elite edges are reinforced.

## Worked Example 2: QAP with Pair-Assignment Pheromones

The quadratic assignment problem places n facilities at n locations to minimize the flow-weighted
distance sum: min over permutations p of sum_{i,j} flow[i,j] * dist[p[i], p[j]]. The pheromone here
is **not** on edges of a path: tau[i, k] is the learned desirability of placing facility i at
location k — the pair-assignment model. QAP has no reliable a-priori visibility, so beta = 0,
following MMAS-QAP (Stützle & Hoos 2000): pheromone-only construction plus 2-exchange local search
with O(n) delta evaluation (see **fitness-evaluation-and-caching** for the general pattern).

```python
"""QAP utilities: instance generator, vectorized cost, exact O(n) swap delta."""
from __future__ import annotations

import numpy as np


def random_qap_instance(n: int, seed: int) -> tuple[np.ndarray, np.ndarray]:
    """Symmetric random QAP, integer flows/distances in [0, 100), zero diagonal."""
    rng = np.random.default_rng(seed)
    flow = np.triu(rng.integers(0, 100, (n, n)), 1)
    dist = np.triu(rng.integers(0, 100, (n, n)), 1)
    return (flow + flow.T).astype(np.float64), (dist + dist.T).astype(np.float64)


def qap_cost(p: np.ndarray, flow: np.ndarray, dist: np.ndarray) -> float:
    """sum_{i,j} flow[i,j] * dist[p[i], p[j]], fully vectorized."""
    return float((flow * dist[np.ix_(p, p)]).sum())


def swap_delta(p: np.ndarray, flow: np.ndarray, dist: np.ndarray, r: int, s: int) -> float:
    """Exact O(n) cost change of swapping the locations of facilities r and s.

    Valid for asymmetric flow/distance matrices as well (Taillard 1991 formula).
    """
    pr, ps = p[r], p[s]
    mask = np.ones(p.size, dtype=bool)
    mask[[r, s]] = False
    pk = p[mask]
    delta = (
        (flow[r, r] - flow[s, s]) * (dist[ps, ps] - dist[pr, pr])
        + (flow[r, s] - flow[s, r]) * (dist[ps, pr] - dist[pr, ps])
        + (flow[r, mask] - flow[s, mask]) @ (dist[ps, pk] - dist[pr, pk])
        + (flow[mask, r] - flow[mask, s]) @ (dist[pk, ps] - dist[pk, pr])
    )
    return float(delta)


def two_exchange(p: np.ndarray, flow: np.ndarray, dist: np.ndarray) -> np.ndarray:
    """First-improvement 2-exchange local search; loops until locally optimal."""
    p = p.copy()
    n = p.size
    improved = True
    while improved:
        improved = False
        for r in range(n - 1):
            for s in range(r + 1, n):
                if swap_delta(p, flow, dist, r, s) < -1e-9:
                    p[r], p[s] = p[s], p[r]
                    improved = True
    return p


if __name__ == "__main__":
    flow, dist = random_qap_instance(8, seed=1)
    rng = np.random.default_rng(2)
    p = rng.permutation(8).astype(np.int64)
    base = qap_cost(p, flow, dist)
    q = p.copy()
    q[2], q[5] = q[5], q[2]
    assert abs((qap_cost(q, flow, dist) - base) - swap_delta(p, flow, dist, 2, 5)) < 1e-9
    print("delta evaluation matches full recomputation")
    # Expected: the assertion passes -- the O(n) delta equals the O(n^2) recomputation.
```

The ACO driver continues the same module. Construction assigns facilities in a *random order* each
time — a fixed order would bias early facilities toward locations chosen under an emptier board —
and samples a free location for facility i in proportion to tau[i, :].

```python
"""MMAS for the QAP with pair-assignment pheromones (same module as above)."""
from __future__ import annotations

import numpy as np


def construct_assignment(tau: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Assign facilities in random order; sample a free location ~ tau[i, :]."""
    n = tau.shape[0]
    p = np.empty(n, dtype=np.int64)
    free = np.ones(n, dtype=bool)
    for i in rng.permutation(n):
        w = np.where(free, tau[i], 0.0)
        total = w.sum()
        if total > 0.0:
            loc = int(rng.choice(n, p=w / total))
        else:
            loc = int(rng.choice(np.flatnonzero(free)))
        p[i] = loc
        free[loc] = False
    return p


def mmas_qap(
    flow: np.ndarray,
    dist: np.ndarray,
    n_ants: int = 10,
    rho: float = 0.2,
    p_best: float = 0.05,
    n_iterations: int = 200,
    gb_every: int = 20,
    seed: int = 0,
) -> tuple[np.ndarray, float, list[float]]:
    """MMAS-QAP: beta = 0 (no visibility), 2-exchange local search on every ant."""
    n = flow.shape[0]
    rng = np.random.default_rng(seed)
    start = two_exchange(rng.permutation(n).astype(np.int64), flow, dist)
    best_p, best_cost = start, qap_cost(start, flow, dist)
    tau = np.full((n, n), 1.0 / (rho * best_cost))         # tau_max initialization
    fac = np.arange(n)
    history: list[float] = []
    for it in range(n_iterations):
        iter_p, iter_cost = best_p, float("inf")
        for _ in range(n_ants):
            p = two_exchange(construct_assignment(tau, rng), flow, dist)
            cost = qap_cost(p, flow, dist)
            if cost < iter_cost:
                iter_p, iter_cost = p, cost
        if iter_cost < best_cost:
            best_p, best_cost = iter_p.copy(), iter_cost
        tau_max = 1.0 / (rho * best_cost)
        q = p_best ** (1.0 / n)
        tau_min = min(tau_max, tau_max * (1.0 - q) / ((n / 2.0 - 1.0) * q))
        tau *= 1.0 - rho
        dep = best_p if (it + 1) % gb_every == 0 else iter_p
        tau[fac, dep] += 1.0 / qap_cost(dep, flow, dist)   # deposit on (i, p[i]) pairs
        np.clip(tau, tau_min, tau_max, out=tau)
        history.append(best_cost)
    return best_p, best_cost, history


if __name__ == "__main__":
    flow, dist = random_qap_instance(12, seed=7)
    p, cost, hist = mmas_qap(flow, dist, n_iterations=80, seed=3)
    assert sorted(p.tolist()) == list(range(12))
    print(f"best QAP cost: {cost:.0f}")
    # Expected: a valid permutation of 12 locations; cost matches the best value
    # found by ~100 independent 2-exchange restarts, usually within 30 iterations.
```

Differences from the TSP model worth internalizing: the pheromone row index is the decision
stage's identity (facility), not the previous choice — there is no "current node" and the
construction graph is bipartite. Deposit hits exactly n entries (one per facility), not n edges of
a cycle. And with beta = 0 the colony learns purely from solution quality; local search supplies
the intensification that eta supplies in routing problems.

## Advanced Techniques

### Stagnation detection and restarts

The standard convergence diagnostic is the average lambda-branching factor (Gambardella & Dorigo
1995, Ant-Q): per pheromone row, count entries above a threshold interpolated between the row's
min and max; a value near 1 means construction has become deterministic. Restart only when the
branching factor is low *and* the best-so-far has not improved for a fixed number of iterations.

```python
"""Stagnation diagnosis via the average lambda-branching factor."""
from __future__ import annotations

import numpy as np


def avg_branching_factor(tau: np.ndarray, lam: float = 0.05) -> float:
    """Mean number of 'attractive' choices per construction step (>=1)."""
    t_min = tau.min(axis=1, keepdims=True)
    t_max = tau.max(axis=1, keepdims=True)
    thresh = t_min + lam * (t_max - t_min)
    return float((tau >= thresh).sum(axis=1).mean())


def maybe_restart(
    tau: np.ndarray, tau_max: float, stale_iters: int,
    lam: float = 0.05, bf_limit: float = 2.0, stale_limit: int = 100,
) -> bool:
    """Reset all trails to tau_max when converged AND stuck; return True if reset."""
    if stale_iters >= stale_limit and avg_branching_factor(tau, lam) < bf_limit:
        tau.fill(tau_max)
        return True
    return False
    # Usage: call every iteration with stale_iters = iterations since last
    # best-so-far improvement; after a restart, deposit only iteration-best for
    # a while so the colony re-explores instead of re-converging instantly.
```

### Vectorized batch construction

For large colonies the Python-level loop over ants dominates. Advance all m ants one step at a
time and sample m categorical distributions in a single shot with the Gumbel-max trick. This needs
strictly positive weights for all unvisited components (true whenever tau >= tau_min > 0).

```python
"""Batch construction: all m ants advance one step per Python-level iteration."""
from __future__ import annotations

import numpy as np


def construct_tours_batch(w: np.ndarray, m: int, rng: np.random.Generator) -> np.ndarray:
    """Build m tours at once from weight matrix w = tau**alpha * eta**beta."""
    n = w.shape[0]
    tours = np.empty((m, n), dtype=np.int64)
    visited = np.zeros((m, n), dtype=bool)
    cur = rng.integers(n, size=m)
    tours[:, 0] = cur
    visited[np.arange(m), cur] = True
    for step in range(1, n):
        scores = np.where(visited, 0.0, w[cur])            # (m, n) gather + mask
        gumbel = -np.log(-np.log(rng.random((m, n)) + 1e-300) + 1e-300)
        with np.errstate(divide="ignore"):
            logits = np.log(scores)                        # log(0) -> -inf is intended
        cur = np.argmax(logits + gumbel, axis=1)           # categorical sample per row
        tours[:, step] = cur
        visited[np.arange(m), cur] = True
    return tours


if __name__ == "__main__":
    rng = np.random.default_rng(0)
    w = rng.random((50, 50)) + 0.1
    np.fill_diagonal(w, 0.0)
    tours = construct_tours_batch(w, m=20, rng=rng)
    assert all(sorted(t) == list(range(50)) for t in tours.tolist())
    print("20 valid tours built in", tours.shape[1] - 1, "batched steps")
    # Expected: all 20 tours are permutations of 0..49; runtime scales with n,
    # not with m*n, at the Python level.
```

### Local search hybridization schedules

Three budget knobs control the ACO/local-search balance: *which ants* get improved (all ants is
the published default for MMAS; improving only the iteration-best saves 90%+ of the local-search
time at a quality cost), *how deep* (2-opt to local optimality vs. a capped number of passes), and
*which neighborhood* (2-opt for tours, 2-exchange for assignments; 3-opt or Or-opt only on the
best-so-far solution). A robust scheme for expensive objectives: a cheap first-improvement pass
for every ant, full optimization only for the iteration-best. Always deposit the *improved*
solutions — depositing pre-local-search solutions discards what local search just learned.

### The hyper-cube framework

Blum & Dorigo (2004, the hyper-cube framework for ant colony optimization) normalize the deposit
so trails always stay in [0, 1]: tau <- (1 - rho) tau + rho * delta, where delta is 1 on the
components of the deposit solution and 0 elsewhere (or a weighted average over several solutions).
The pheromone scale becomes independent of objective magnitude, so one parameter setting transfers
across instances and numerical under/overflow disappears.

### Choosing the deposit schedule

MMAS quality is sensitive to the iteration-best vs. best-so-far mix. The published long-run
schedule tightens over time: deposit best-so-far every 25 iterations early, every 5 mid-run, every
iteration late; after a restart, return to iteration-best only. If you tune one ACO-specific
parameter beyond rho and beta, tune this schedule.

## Practical Challenges

**All ants build the same solution after a few hundred iterations.** This is trail stagnation, the
canonical ACO failure. Verify trail limits are actually applied (a missing `np.clip` is the most
common bug), lower p_best to raise tau_min, slow the deposit schedule (more iteration-best), and
add branching-factor-triggered restarts. If stagnation happens within tens of iterations, rho is
too high or alpha > 1.

**ACO is slower than multi-start local search at equal quality.** Expected when the pheromone adds
nothing — check that the best-so-far keeps improving after the first restart-free phase. If not,
the pheromone model may not match the decision structure (e.g., edge pheromones on a problem where
position matters), or eta dominates (beta too high) so the colony never learns. ACO earns its cost
when trails concentrate search on shared building blocks of elite solutions.

**Construction dominates runtime in Python.** Precompute the weight matrix tau^alpha * eta^beta
once per iteration (MMAS), use candidate lists, and switch to batched construction (Gumbel-max) or
numba for the inner loop. Profile first: with strong local search, 2-opt usually dwarfs
construction, and the right fix is don't-look bits, not faster sampling.

**Deposit magnitudes differ wildly across instances.** With deposit 1/C, an instance with costs in
the millions learns trails 10^6 times smaller than a toy instance, breaking tuned tau limits.
MMAS's coupled limits (both scale with 1/C_best) handle this; otherwise normalize costs or adopt
the hyper-cube framework.

**Asymmetric problems with a symmetric update.** For asymmetric TSP or directed routing, deposit
only on traversed arcs and keep tau asymmetric. Symmetrizing the deposit on a directed problem
blurs the learning signal; the colony learns "this edge is good in some direction," which is much
weaker information.

**The heuristic term is useless or misleading.** For QAP, timetabling, and many scheduling
problems no good static eta exists. Set beta = 0 rather than inventing a weak eta — a misleading
visibility term actively fights the learned trails. Compensate with local search on every ant.

**Trails saturate at the bounds and learning stops.** If most of tau sits at tau_min with a few
entries at tau_max, the effective search is a randomized greedy around one solution. Decrease rho
(slower convergence), increase p_best slightly, or shorten the gb_every schedule less aggressively.
Log the fraction of entries at each bound per iteration; it is the cheapest health metric.

## Tools & Libraries

| Library / tool | When to use | Note |
|---|---|---|
| numpy | always | trail matrices, vectorized weights, batch sampling |
| scipy.spatial.distance (cdist) | building distance matrices | faster and cleaner than manual broadcasting for large n |
| numba | construction loop too slow, n > ~2000 | JIT the per-ant loop; keep numpy for updates |
| ACOTSP (Stützle, C code) | reference results on TSPLIB | the canonical implementation behind the MMAS papers |
| scikit-opt (`sko.ACA`) | quick prototype on small TSPs | basic Ant System only; no trail limits or restarts |
| MEALPY | comparing many metaheuristics in one harness | ACO variants included; verify update rules before publishing numbers |
| OR-Tools routing | you need good VRP/TSP solutions, not ACO research | uses guided local search, not ACO — often the pragmatic choice |
| tsplib95 | loading TSPLIB instances | pairs with QAPLIB files (plain text) for QAP experiments |

## Output Format

A complete ACO deliverable contains:

1. **Configuration summary** — every parameter, explicit and seeded:

| Field | Example |
|---|---|
| variant | MMAS |
| ants / alpha / beta / rho | 20 / 1.0 / 3.0 / 0.2 |
| trail limits | p_best = 0.05, coupled to best-so-far |
| deposit schedule | iteration-best; best-so-far every 25 |
| local search | 2-opt, all ants, first-improvement; 15-NN candidate list |
| budget / seeds | 300 iterations; seeds 0-9 |

2. **Solution report** — best objective per seed, validated by an independent checker (re-compute
   the objective from the raw solution; assert the solution is a permutation / covers all
   customers), plus gap to best-known or to an exact bound where available.
3. **Convergence summary** — best-so-far curve data per seed (iteration, value), iteration of last
   improvement, final average branching factor, number of restarts triggered.
4. **Comparison table** — mean/best/std over seeds vs. the multi-start local search baseline at
   the same evaluation budget; report evaluations consumed, not just iterations.
5. **Artifacts** — `results.csv` (instance, seed, variant, parameters, best_cost, evaluations,
   wall_time, iteration_of_best), best solutions in plain text, and the producing commit hash.

## Questions to Ask

- What does one solution look like — a tour, an assignment, a subset, a schedule?
- How large are the instances, and what is the wall-clock budget per run?
- Is there a natural greedy desirability measure for single decisions, or will beta = 0?
- Is a local search with cheap delta evaluation available or implementable for this problem?
- Is the goal research-grade comparison (seeds, statistics, baselines) or one good solution?
- Are there hard constraints that construction cannot maintain implicitly, requiring repair or
  penalties?
- Symmetric or asymmetric cost structure (affects deposit direction)?
- Does the problem change online (favors ACS-style fast adaptation)?
- What baseline must ACO beat to be worth keeping?

## Related Skills

- **traveling-salesman-problem** — when the task is the tour problem itself: exact formulations
  with subtour cuts, TSPLIB handling, and stronger tour-specific machinery than ACO provides.
- **vehicle-routing-problem** — when construction extends to multiple capacitated routes; the
  pheromone models here carry over, but VRP-specific operators and benchmarks live there.
- **local-search-and-neighborhoods** — when designing the 2-opt / exchange improvement step that
  competitive ACO hybrids require, including don't-look bits and scanning order.
- **fitness-evaluation-and-caching** — when construction or local search dominates runtime and you
  need delta evaluation, memoization, or batched objective computation.
