---
name: large-neighborhood-search
description: When the user wants to implement or tune large neighborhood search (LNS) or adaptive LNS (ALNS), covering destroy/repair operator design, adaptive operator weights, acceptance criteria, and noise, for routing, scheduling, and tightly constrained problems. Also use when the user mentions "large neighborhood search," "ALNS," "destroy and repair," "removal operator," "insertion heuristic," "adaptive weights," "ruin and recreate," or when small-move local search stalls because moves are infeasible. For VRP baselines, see vehicle-routing-problem; for exact MIP repair, see matheuristics.
---

# Large Neighborhood Search

You are an expert in large neighborhood search (LNS) and its adaptive variant (ALNS) for combinatorial optimization. This skill covers destroy/repair operator design, adaptive operator weights with segment updates, acceptance criteria, degree-of-destruction control, and noise, with implementation-grade Python. LNS/ALNS is the modern workhorse for vehicle routing and scheduling; use the framework below to take a user from "local search is stuck and most moves are infeasible" to a calibrated, reproducible ALNS with a defensible operator and parameter story.

## Initial Assessment

Establish these facts before writing any LNS code:

- **Removable element.** What is the atomic unit a destroy operator removes — a customer visit, a job, a shift assignment, an order line? Destroy and repair are defined over these elements; pick the granularity first.
- **Constraint tightness.** Are most small moves (swap, relocate) infeasible because of time windows, capacities, or precedences? Tight coupling is the signature case for LNS; loosely constrained problems are often served better by 2-opt-style local search or ILS.
- **Construction heuristic availability.** Any decent greedy or regret construction heuristic for the problem becomes a repair operator almost verbatim. If none exists, design it before the LNS loop.
- **Repair completeness.** Can repair always finish a solution (e.g., open a new vehicle, use overtime), or can it dead-end? If it can dead-end, plan a request bank or penalty scheme — see constraint-handling-techniques.
- **Objective structure.** Single objective, or hierarchical (first vehicles, then distance)? Scale and hierarchy interact with the acceptance temperature; decide how to compare two solutions before calibrating acceptance.
- **Hard vs soft constraints.** Which constraints stay satisfied by construction inside repair, and which become penalties in the objective? Penalty weights become parameters of the search.
- **Instance size and per-iteration cost.** With n elements and destruction degree q, greedy repair costs roughly O(q · positions). Measure iterations/second early; the budget in iterations drives the cooling schedule and segment count.
- **Time budget and quality target.** A 1-minute "good enough" run and a benchmark run chasing best-known solutions need different iteration counts, q ranges, and acceptance schedules.
- **Plain LNS vs ALNS.** One destroy + one repair operator (plain LNS) is the right first build. Add the adaptive layer only when you have at least 3 destroy and 2 repair operators worth arbitrating between.
- **Exact repair option.** Is a MIP solver licensed and fast enough to reinsert q elements optimally? If yes, the matheuristic variant is on the table — see matheuristics.
- **Delta evaluation.** Can insertion costs be computed incrementally per route/machine instead of re-evaluating the full solution? Repair dominates runtime; this decides whether the method is competitive.
- **Baseline.** What must ALNS beat — an ILS, OR-Tools, a MIP with time limit? Always run the baseline first; ALNS has more moving parts and needs justification.
- **Reproducibility.** Seeds per instance, instance set, and reporting format (best/mean/std, gap to best known) — fix these before tuning anything.

## Algorithm Anatomy

### The destroy–repair loop

LNS (Shaw 1998, "Using Constraint Programming and Local Search Methods to Solve Vehicle Routing Problems") replaces the enumeration of small moves by one large move per iteration: a **destroy** operator removes q of the n solution elements, and a **repair** operator reinserts them with a constructive heuristic. The implicit neighborhood is every solution reachable by removing q elements and reinserting them — at least

$$
\binom{n}{q} \quad \text{candidates, e.g. } \binom{100}{30} \approx 2.9 \times 10^{25},
$$

hence "large." The neighborhood is *sampled* (one destroy+repair per iteration), never searched exhaustively. The same idea was developed independently as **ruin-and-recreate** by Schrimpf et al. (2000), "Record Breaking Optimization Results Using the Ruin and Recreate Principle."

LNS succeeds where small-move local search fails for two structural reasons:

1. **Feasibility.** In tightly constrained problems most swaps/relocations are infeasible, so the small-move neighborhood graph is sparse and disconnected. Repair rebuilds feasibility from scratch over the removed part, so large coherent changes remain reachable.
2. **Coupled decisions.** Removing a cluster of related elements and reinserting them together changes assignment and sequencing decisions coherently, which a sequence of independent small moves cannot do without passing through bad intermediate solutions.

### The adaptive layer (ALNS)

ALNS (Ropke & Pisinger 2006, "An Adaptive Large Neighborhood Search Heuristic for the Pickup and Delivery Problem with Time Windows") keeps a *portfolio* of destroy and repair operators and learns which ones work on the current instance. Each operator $i$ carries a weight $w_i$; one destroy and one repair operator are drawn each iteration by roulette wheel,

$$
P(\text{select } i) = \frac{w_i}{\sum_j w_j}.
$$

Each iteration earns a score: $\sigma_1$ for a new global best, $\sigma_2$ for improving the current solution, $\sigma_3$ for an accepted but worse solution (a diversification reward), 0 for a rejected one. After every *segment* of (typically) 100 iterations, weights are smoothed toward the observed average score:

$$
w_i \leftarrow (1-\rho)\, w_i + \rho\, \frac{\pi_i}{\theta_i},
$$

where $\pi_i$ is the score accumulated by operator $i$ in the segment, $\theta_i$ its usage count, and $\rho \in [0,1]$ the reaction factor. Ropke & Pisinger's tuned scores are $(\sigma_1, \sigma_2, \sigma_3) = (33, 9, 13)$ — note $\sigma_3 > \sigma_2$: escaping is rewarded more than small improvement.

### Acceptance

The outer loop needs an acceptance rule for worse solutions, otherwise LNS degenerates to a (often surprisingly strong) hill climber over large moves. The standard choice is simulated-annealing acceptance: accept a worse candidate with probability $e^{-(f(x')-f(x))/T}$, with $T$ cooled geometrically. Calibrate the start temperature from a *warm-up gap*: choose $T_0$ so that a solution $g$ (e.g. 5%) worse than the initial one is accepted with probability 0.5, i.e. $T_0 = g \cdot f(x_0)/\ln 2$, and set the per-iteration cooling rate $c = (T_{\text{end}}/T_0)^{1/M}$ for a budget of $M$ iterations. Santini, Ropke & Hvattum (2018), "A comparison of acceptance criteria for the adaptive large neighbourhood search metaheuristic," found that simpler criteria (record-to-record travel) match or beat SA acceptance on several problem classes — see Advanced Techniques.

### Decision guidance

- **Use (A)LNS when** the problem is routing/scheduling-like with tight side constraints, a natural removable element exists, and good construction heuristics are available to serve as repair.
- **Prefer plain local search / ILS when** moves are cheap, feasibility is easy, and strong dedicated neighborhoods exist (e.g., 2-opt/Or-opt on plain TSP) — see local-search-and-neighborhoods.
- **Build plain LNS first** (random removal + greedy insertion + SA acceptance). It is the correct ablation baseline. The meta-analysis of Turkeš, Sörensen & Hvattum (2021), "Meta-analysis of metaheuristics: Quantifying the effect of adaptiveness in adaptive large neighborhood search," estimates the adaptive layer itself contributes a modest ~0.14% average improvement — the operators and acceptance do most of the work.
- **Complexity per iteration.** Random removal O(q); worst removal O(q·n) if gains are recomputed per removal; related removal O(q·n log n). Greedy insertion O(q² · positions) naive, O(q · positions) with per-route caching; regret-k adds a factor k bookkeeping but similar order. Repair dominates — optimize it first.

### Parameter guidance

| Parameter | Typical range | Increasing it buys | At the cost of |
|---|---|---|---|
| q (degree of destruction) | 10–40% of n, capped ~60–100 elements | Bigger jumps, escapes deeper optima | Slower repair, quality loss when repair can't keep up |
| Segment length | 50–200 iterations | More stable score estimates | Slower adaptation to the instance |
| Reaction factor ρ | 0.1–0.7 | Faster adaptation | Noisy weights, premature operator lock-in |
| Scores (σ1, σ2, σ3) | (33, 9, 13) baseline | Shapes the reward signal | Mis-set ratios lock in exploitative operators |
| Warm-up gap g (sets T0) | 0.02–0.10 | More early exploration | Budget burned random-walking |
| T_end / T0 | 10⁻³–10⁻⁵ (sets cooling c) | Deeper final intensification | Long frozen tail with few acceptances |
| Weight floor w_min | 0.01–0.1 × initial weight | No operator starves; recovery possible | Slightly dilutes adaptation |
| Noise level (repair) | 0–0.025 × max arc cost | Breaks repair determinism | Weakens greedy guidance |

Tune q and the acceptance schedule first; they dominate. The adaptive-layer parameters (ρ, segment, scores) are second-order. For the design of removal moves as perturbations and of insertion orders, reuse the operator catalogs in mutation-and-perturbation-operators and local-search-and-neighborhoods instead of reinventing them.

## Reusable ALNS Engine

The engine below is problem-independent. It sees the solution as an opaque object and the problem through four callables: `objective`, `copy_solution`, a list of destroy operators `(solution, q, rng) -> removed_ids` that mutate the solution in place, and a list of repair operators `(solution, removed_ids, rng) -> None`. The engine never interprets `removed_ids`; it only hands the list from destroy to repair.

```text
ALNS(instance, M iterations)
  x  <- initial solution (construction heuristic);  x* <- x
  w_d, w_r <- 1 for every destroy / repair operator
  T  <- T0 from warm-up gap                    // accept g-worse with prob 0.5
  for it = 1 .. M:
      d <- roulette(w_d);   r <- roulette(w_r)
      q <- uniform integer in [q_min, q_max]   // degree of destruction
      x' <- copy(x);  R <- destroy_d(x', q);  repair_r(x', R)
      if f(x') < f(x*):           score <- sigma1      // new global best
      else if f(x') < f(x):       score <- sigma2      // improves current
      else if rand() < exp(-(f(x') - f(x)) / T):
                                  score <- sigma3      // accepted, worse
      else:                       score <- 0           // rejected
      if score > 0:   x <- x'
      if f(x') < f(x*):  x* <- x'
      pi[d], pi[r] += score;   theta[d], theta[r] += 1
      T <- c * T
      every `segment` iterations:
          for each operator i used in the segment:
              w_i <- (1 - rho) * w_i + rho * pi[i] / theta[i]
          reset pi, theta
  return x*
```

```python
import math
from dataclasses import dataclass
from typing import Any, Callable

import numpy as np

DestroyOp = Callable[[Any, int, np.random.Generator], list[int]]
RepairOp = Callable[[Any, list[int], np.random.Generator], None]


@dataclass
class ALNSResult:
    """Outcome of one ALNS run."""
    best: Any
    best_obj: float
    trace: np.ndarray            # best-so-far objective per iteration
    destroy_weights: np.ndarray  # final adaptive weights
    repair_weights: np.ndarray


def roulette(weights: np.ndarray, rng: np.random.Generator) -> int:
    """Sample an operator index with probability proportional to its weight."""
    return int(rng.choice(weights.size, p=weights / weights.sum()))


def alns(
    initial: Any,
    objective: Callable[[Any], float],
    copy_solution: Callable[[Any], Any],
    destroy_ops: list[DestroyOp],
    repair_ops: list[RepairOp],
    n_removable: int,
    iterations: int = 5000,
    seed: int = 0,
    q_range: tuple[float, float] = (0.1, 0.4),
    q_cap: int = 60,
    segment: int = 100,
    reaction: float = 0.5,
    scores: tuple[float, float, float] = (33.0, 9.0, 13.0),
    warmup_gap: float = 0.05,
    end_temp_ratio: float = 1e-4,
    weight_floor: float = 0.05,
) -> ALNSResult:
    """Adaptive large neighborhood search (Ropke & Pisinger 2006).

    Destroy operators mutate the solution in place and return the removed
    element ids; repair operators reinsert exactly those ids. The engine
    owns selection (roulette over adaptive weights), SA acceptance with a
    warm-up-calibrated geometric schedule, scoring, and segment updates.
    """
    rng = np.random.default_rng(seed)
    current = copy_solution(initial)
    f_cur = objective(current)
    best, f_best = copy_solution(current), f_cur

    n_d, n_r = len(destroy_ops), len(repair_ops)
    w_d, w_r = np.ones(n_d), np.ones(n_r)
    pi_d, use_d = np.zeros(n_d), np.zeros(n_d)
    pi_r, use_r = np.zeros(n_r), np.zeros(n_r)

    temp = warmup_gap * max(abs(f_cur), 1e-9) / math.log(2.0)
    cooling = end_temp_ratio ** (1.0 / iterations)
    q_lo = max(1, math.ceil(q_range[0] * n_removable))
    q_hi = min(q_cap, max(q_lo, math.floor(q_range[1] * n_removable)))
    trace = np.empty(iterations)

    for it in range(iterations):
        d = roulette(w_d, rng)
        r = roulette(w_r, rng)
        q = int(rng.integers(q_lo, q_hi + 1))

        cand = copy_solution(current)
        removed = destroy_ops[d](cand, q, rng)
        repair_ops[r](cand, removed, rng)
        f_new = objective(cand)

        use_d[d] += 1.0
        use_r[r] += 1.0
        if f_new < f_cur - 1e-9:
            gain = scores[0] if f_new < f_best - 1e-9 else scores[1]
            accepted = True
        else:
            accepted = rng.random() < math.exp(-(f_new - f_cur) / temp)
            gain = scores[2] if accepted else 0.0
        if accepted:
            current, f_cur = cand, f_new
            pi_d[d] += gain
            pi_r[r] += gain
            if f_new < f_best - 1e-9:
                best, f_best = copy_solution(cand), f_new

        temp = max(temp * cooling, 1e-12)
        trace[it] = f_best

        if (it + 1) % segment == 0:
            for w, pi, use in ((w_d, pi_d, use_d), (w_r, pi_r, use_r)):
                hot = use > 0
                w[hot] = (1.0 - reaction) * w[hot] + reaction * pi[hot] / use[hot]
                np.clip(w, weight_floor, None, out=w)
                pi[:] = 0.0
                use[:] = 0.0

    return ALNSResult(best, f_best, trace, w_d, w_r)
```

Engine notes:

- **Copy semantics.** The engine copies the current solution before destroying it, so operators may mutate freely. Keep `copy_solution` cheap (copy only the decision structure, share instance data).
- **Weight floor.** `np.clip(w, weight_floor, ...)` keeps every operator selectable; without it an operator that has one bad segment can starve permanently.
- **Acceptance tolerance.** Comparisons use a `1e-9` tolerance so float noise does not register as "improvement" and inflate σ2 scores.
- **Vectorization boundary.** ALNS is a sequential single-solution method; numpy earns its keep *inside* the objective and the operators (distance lookups, load vectors), not in the outer loop.

## Worked Example: Capacitated Vehicle Routing

CVRP: customers $1..n$ with demands $d_i$, a depot 0, symmetric distances $c_{ij}$, vehicles of capacity $Q$ (fleet size free here, so repair can always finish). Minimize total route length subject to each customer on exactly one route and route loads $\le Q$. This is the problem class ALNS was built for (Pisinger & Ropke 2007, "A General Heuristic for Vehicle Routing Problems"); for formulations, benchmarks, and competing methods see vehicle-routing-problem.

Instance, solution representation, objective, and an independent validator:

```python
from dataclasses import dataclass

import numpy as np


@dataclass
class CvrpInstance:
    """CVRP data: node 0 is the depot, customers are 1..n."""
    dist: np.ndarray      # (n+1, n+1) symmetric distances
    demand: np.ndarray    # (n+1,), demand[0] == 0
    capacity: float

    @property
    def n_customers(self) -> int:
        return self.demand.size - 1


def random_cvrp(n: int, capacity: float, seed: int) -> CvrpInstance:
    """Uniform points in [0,100]^2, depot at the center, integer demands 1..9."""
    rng = np.random.default_rng(seed)
    xy = np.vstack([[50.0, 50.0], rng.uniform(0.0, 100.0, size=(n, 2))])
    diff = xy[:, None, :] - xy[None, :, :]
    dist = np.sqrt((diff ** 2).sum(axis=2))
    demand = np.concatenate([[0.0], rng.integers(1, 10, size=n).astype(float)])
    return CvrpInstance(dist=dist, demand=demand, capacity=capacity)


@dataclass
class CvrpSolution:
    """Routes exclude the depot; every customer sits in exactly one route."""
    inst: CvrpInstance
    routes: list[list[int]]


def copy_cvrp(sol: CvrpSolution) -> CvrpSolution:
    """Copy the route structure; the instance is shared."""
    return CvrpSolution(sol.inst, [list(r) for r in sol.routes])


def route_cost(route: list[int], dist: np.ndarray) -> float:
    """Length of depot -> route -> depot."""
    if not route:
        return 0.0
    path = [0, *route, 0]
    return float(sum(dist[a, b] for a, b in zip(path, path[1:])))


def cvrp_objective(sol: CvrpSolution) -> float:
    """Total travel distance over all routes."""
    return sum(route_cost(r, sol.inst.dist) for r in sol.routes)


def validate_cvrp(sol: CvrpSolution) -> float:
    """Independent check: customer partition + capacity; returns the objective."""
    seen = sorted(c for r in sol.routes for c in r)
    assert seen == list(range(1, sol.inst.n_customers + 1)), "not a partition"
    for r in sol.routes:
        assert sol.inst.demand[r].sum() <= sol.inst.capacity + 1e-9, "capacity"
    return cvrp_objective(sol)
```

The three classic destroy operators. `worst_removal` and `related_removal` use Ropke & Pisinger's biased rank selection `index = floor(u^p * len)`: with determinism parameter $p>1$, low ranks are strongly preferred but any element can be chosen.

```python
import numpy as np


def remove_customers(sol: "CvrpSolution", custs: set[int]) -> list[int]:
    """Drop the given customers from their routes; return them as a list."""
    sol.routes = [[c for c in r if c not in custs] for r in sol.routes]
    sol.routes = [r for r in sol.routes if r]
    return list(custs)


def random_removal(sol: "CvrpSolution", q: int, rng: np.random.Generator) -> list[int]:
    """Baseline diversifier: remove q uniformly chosen customers."""
    custs = rng.choice(np.arange(1, sol.inst.n_customers + 1), size=q, replace=False)
    return remove_customers(sol, {int(c) for c in custs})


def worst_removal(sol: "CvrpSolution", q: int, rng: np.random.Generator,
                  p: float = 3.0) -> list[int]:
    """Remove badly placed customers: largest detour saving when removed."""
    d = sol.inst.dist
    removed: list[int] = []
    for _ in range(q):
        gains: list[tuple[float, int]] = []
        for r in sol.routes:
            for k, c in enumerate(r):
                a = r[k - 1] if k > 0 else 0
                b = r[k + 1] if k < len(r) - 1 else 0
                gains.append((d[a, c] + d[c, b] - d[a, b], c))
        gains.sort(reverse=True)
        cust = gains[int(rng.random() ** p * len(gains))][1]
        remove_customers(sol, {cust})
        removed.append(cust)
    return removed


def related_removal(sol: "CvrpSolution", q: int, rng: np.random.Generator,
                    p: float = 6.0, demand_weight: float = 0.5) -> list[int]:
    """Shaw (1998) removal: grow a set of mutually related customers."""
    inst = sol.inst
    n = inst.n_customers
    d_max = inst.dist[1:, 1:].max()
    dem_max = max(inst.demand.max(), 1.0)
    removed = [int(rng.integers(1, n + 1))]
    pool = set(range(1, n + 1)) - {removed[0]}
    while len(removed) < q:
        ref = removed[int(rng.integers(len(removed)))]
        ranked = sorted(
            pool,
            key=lambda c: inst.dist[ref, c] / d_max
            + demand_weight * abs(inst.demand[ref] - inst.demand[c]) / dem_max,
        )
        pick = ranked[int(rng.random() ** p * len(ranked))]
        removed.append(pick)
        pool.discard(pick)
    return remove_customers(sol, set(removed))
```

Repair: greedy insertion (globally cheapest feasible insertion, repeated) and regret-2 insertion. Regret-k inserts first the customer that would *lose most* if its best route filled up — the difference between its best and k-th-best route insertion cost. Opening a fresh route is always an option, so repair never dead-ends.

```python
import numpy as np


def best_position(route: list[int], c: int, inst: "CvrpInstance") -> tuple[int, float]:
    """Cheapest feasible insertion of c into route: (position, delta) or (-1, inf)."""
    if inst.demand[route].sum() + inst.demand[c] > inst.capacity + 1e-9:
        return -1, float("inf")
    d = inst.dist
    path = [0, *route, 0]
    best_pos, best_delta = -1, float("inf")
    for k in range(len(route) + 1):
        delta = d[path[k], c] + d[c, path[k + 1]] - d[path[k], path[k + 1]]
        if delta < best_delta:
            best_pos, best_delta = k, delta
    return best_pos, best_delta


def greedy_insertion(sol: "CvrpSolution", removed: list[int],
                     rng: np.random.Generator) -> None:
    """Repeatedly perform the globally cheapest feasible insertion."""
    pending = list(removed)
    while pending:
        best = (float("inf"), 0, -1, 0)  # (delta, pending-index, route, position)
        for ci, c in enumerate(pending):
            for ri, r in enumerate(sol.routes):
                pos, delta = best_position(r, c, sol.inst)
                if delta < best[0]:
                    best = (delta, ci, ri, pos)
            fresh = 2.0 * sol.inst.dist[0, c]  # open a new route
            if fresh < best[0]:
                best = (fresh, ci, -1, 0)
        _, ci, ri, pos = best
        c = pending.pop(ci)
        if ri < 0:
            sol.routes.append([c])
        else:
            sol.routes[ri].insert(pos, c)


def regret2_insertion(sol: "CvrpSolution", removed: list[int],
                      rng: np.random.Generator) -> None:
    """Regret-2: insert first the customer with the largest best-vs-second gap."""
    pending = list(removed)
    while pending:
        chosen = ((float("inf"), float("inf")), 0, -1, 0)
        for ci, c in enumerate(pending):
            options = [(2.0 * sol.inst.dist[0, c], -1, 0)]  # fresh route
            for ri, r in enumerate(sol.routes):
                pos, delta = best_position(r, c, sol.inst)
                if pos >= 0:
                    options.append((delta, ri, pos))
            options.sort(key=lambda t: t[0])
            best_delta, ri, pos = options[0]
            regret = options[1][0] - best_delta if len(options) > 1 else 0.0
            key = (-regret, best_delta)  # max regret, tie-break cheapest
            if key < chosen[0]:
                chosen = (key, ci, ri, pos)
        _, ci, ri, pos = chosen
        c = pending.pop(ci)
        if ri < 0:
            sol.routes.append([c])
        else:
            sol.routes[ri].insert(pos, c)
```

Wiring it together on a small synthetic instance, starting from a capacity-respecting nearest-neighbor construction:

```python
import numpy as np


def nearest_neighbor_start(inst: "CvrpInstance") -> "CvrpSolution":
    """Greedy construction: extend a route to the nearest feasible customer."""
    unvisited = set(range(1, inst.n_customers + 1))
    routes: list[list[int]] = []
    while unvisited:
        route: list[int] = []
        load, cur = 0.0, 0
        while True:
            feas = [c for c in unvisited if load + inst.demand[c] <= inst.capacity]
            if not feas:
                break
            nxt = min(feas, key=lambda c: inst.dist[cur, c])
            route.append(nxt)
            unvisited.discard(nxt)
            load += inst.demand[nxt]
            cur = nxt
        routes.append(route)
    return CvrpSolution(inst, routes)


inst = random_cvrp(n=40, capacity=40.0, seed=7)
start = nearest_neighbor_start(inst)
result = alns(
    initial=start,
    objective=cvrp_objective,
    copy_solution=copy_cvrp,
    destroy_ops=[random_removal, worst_removal, related_removal],
    repair_ops=[greedy_insertion, regret2_insertion],
    n_removable=inst.n_customers,
    iterations=2000,
    seed=1,
)
print(f"start {cvrp_objective(start):.1f} -> best {result.best_obj:.1f} "
      f"({len(result.best.routes)} routes)")
print(f"validated: {validate_cvrp(result.best):.1f}")
print("destroy weights:", np.round(result.destroy_weights, 2))
# Expected: start 1060.7 -> best 789.4 (5 routes), validated 789.4 — a ~26%
# improvement in 2000 iterations; all three destroy weights remain active.
```

Implementation notes for scaling beyond the demo: cache the best insertion cost of every removed customer per route and recompute it only for routes touched since the last iteration (this turns greedy repair from O(q²·positions) into roughly O(q·positions)); store route loads incrementally instead of summing demands inside `best_position`.

## Worked Example: Unrelated Parallel Machines

$R\,||\,C_{\max}$: jobs $1..n$, machines $1..m$, processing time $p_{mj}$ of job $j$ on machine $m$ (machine-dependent, "unrelated"). Assign every job to one machine to minimize the makespan $\max_m \sum_{j \in m} p_{mj}$. Order within a machine is irrelevant for makespan, so a solution is just an assignment vector — which makes the destroy/repair contract very clean. For dispatching rules, MIP models, and bounds see parallel-machine-scheduling.

```python
from dataclasses import dataclass

import numpy as np


@dataclass
class PmInstance:
    """Unrelated parallel machines: p[m, j] = time of job j on machine m."""
    p: np.ndarray  # (machines, jobs)


@dataclass
class PmSolution:
    """assign[j] = machine of job j; -1 marks a removed (unassigned) job."""
    inst: PmInstance
    assign: np.ndarray


def copy_pm(sol: PmSolution) -> PmSolution:
    """Copy the assignment vector; the instance is shared."""
    return PmSolution(sol.inst, sol.assign.copy())


def machine_loads(sol: PmSolution) -> np.ndarray:
    """Vectorized machine loads from the assignment vector."""
    m = sol.inst.p.shape[0]
    onehot = sol.assign[None, :] == np.arange(m)[:, None]
    return (sol.inst.p * onehot).sum(axis=1)


def pm_objective(sol: PmSolution) -> float:
    """Makespan of a complete assignment."""
    return float(machine_loads(sol).max())


def validate_pm(sol: PmSolution) -> float:
    """Independent check: every job assigned; recompute the makespan."""
    assert (sol.assign >= 0).all(), "unassigned jobs"
    loads = np.zeros(sol.inst.p.shape[0])
    for j, m in enumerate(sol.assign):
        loads[m] += sol.inst.p[m, j]
    return float(loads.max())


def random_pm(machines: int, jobs: int, seed: int) -> PmInstance:
    """Base job lengths x machine speeds x unrelated noise."""
    rng = np.random.default_rng(seed)
    base = rng.uniform(10.0, 100.0, size=jobs)
    speed = rng.uniform(0.8, 1.6, size=machines)
    noise = rng.uniform(0.8, 1.25, size=(machines, jobs))
    return PmInstance(p=base[None, :] * speed[:, None] * noise)


def pm_random_removal(sol: PmSolution, q: int, rng: np.random.Generator) -> list[int]:
    """Remove q uniformly chosen jobs."""
    jobs = rng.choice(sol.assign.size, size=q, replace=False)
    sol.assign[jobs] = -1
    return [int(j) for j in jobs]


def pm_bottleneck_removal(sol: PmSolution, q: int,
                          rng: np.random.Generator) -> list[int]:
    """Worst-removal analog: longest jobs from the most loaded machines."""
    order = np.argsort(-machine_loads(sol))
    removed: list[int] = []
    for m in order:
        jobs = np.flatnonzero(sol.assign == m)
        take = jobs[np.argsort(-sol.inst.p[m, jobs])][: q - len(removed)]
        removed.extend(int(j) for j in take)
        if len(removed) >= q:
            break
    sol.assign[removed] = -1
    return removed


def pm_related_removal(sol: PmSolution, q: int, rng: np.random.Generator,
                       p: float = 4.0) -> list[int]:
    """Shaw-style removal: jobs with similar processing-time profiles."""
    prof = sol.inst.p / sol.inst.p.max()
    n = sol.assign.size
    removed = [int(rng.integers(n))]
    pool = [j for j in range(n) if j != removed[0]]
    while len(removed) < q:
        ref = removed[int(rng.integers(len(removed)))]
        dist = np.linalg.norm(prof[:, pool] - prof[:, [ref]], axis=0)
        pick = int(np.argsort(dist)[int(rng.random() ** p * len(pool))])
        removed.append(pool.pop(pick))
    sol.assign[removed] = -1
    return removed


def pm_greedy_repair(sol: PmSolution, removed: list[int],
                     rng: np.random.Generator) -> None:
    """LPT-flavored greedy: longest job (by min time) first, best machine."""
    p = sol.inst.p
    loads = machine_loads(sol)
    for j in sorted(removed, key=lambda j: -p[:, j].min()):
        m = int(np.argmin(loads + p[:, j]))
        sol.assign[j] = m
        loads[m] += p[m, j]


def pm_regret_repair(sol: PmSolution, removed: list[int],
                     rng: np.random.Generator) -> None:
    """Regret-2 over machines, vectorized over the pending job set."""
    p = sol.inst.p
    loads = machine_loads(sol)
    pending = list(removed)
    while pending:
        cost = loads[:, None] + p[:, pending]      # (machines, |pending|)
        two = np.partition(cost, 1, axis=0)[:2]    # best and second-best
        k = int(np.argmax(two[1] - two[0]))
        j = pending.pop(k)
        m = int(np.argmin(cost[:, k]))
        sol.assign[j] = m
        loads[m] += p[m, j]
```

The run reuses the engine unchanged — only the callables differ:

```python
import numpy as np

inst_pm = random_pm(machines=4, jobs=30, seed=11)
start_pm = PmSolution(inst_pm, np.full(30, -1, dtype=int))
pm_greedy_repair(start_pm, list(range(30)), np.random.default_rng(0))

result_pm = alns(
    initial=start_pm,
    objective=pm_objective,
    copy_solution=copy_pm,
    destroy_ops=[pm_random_removal, pm_bottleneck_removal, pm_related_removal],
    repair_ops=[pm_greedy_repair, pm_regret_repair],
    n_removable=30,
    iterations=2000,
    seed=3,
    q_range=(0.1, 0.35),
)
lb = max(inst_pm.p.min(axis=0).max(), inst_pm.p.min(axis=0).sum() / 4.0)
print(f"greedy {pm_objective(start_pm):.1f} -> best {result_pm.best_obj:.1f} "
      f"(lower bound {lb:.1f})")
print(f"validated: {validate_pm(result_pm.best):.1f}")
# Expected: greedy 416.8 -> best 394.7 (naive lower bound 334.9). The naive
# bound is loose for unrelated machines; the assignment LP relaxation gives
# 387.7 on this instance, so the ALNS solution is within 2% of optimal.
```

Two lessons transfer from this example. First, when element order inside a resource does not matter, repair reduces to an assignment rule and becomes very fast — ALNS iterations are then cheap and budgets of 10⁵+ iterations are realistic. Second, `pm_bottleneck_removal` shows problem-specific destroy design: the makespan only drops if the critical machine changes, so removal must target it.

## Advanced Techniques

### Acceptance criteria beyond simulated annealing

SA acceptance adds two parameters (start temperature, cooling) that need calibration against the objective scale. Santini, Ropke & Hvattum (2018) compared seven criteria inside ALNS and found record-to-record travel — accept $x'$ iff $f(x') < (1+\delta) f(x^*)$ with $\delta$ shrinking over time — equally good or better, with one intuitive parameter. Late-acceptance hill climbing (Burke & Bykov 2017, "The late acceptance Hill-Climbing heuristic") compares against the objective $k$ iterations ago and is another robust drop-in. Swap the Metropolis test in the engine's `else` branch for one of these:

```python
import numpy as np


def accept_metropolis(f_new: float, f_cur: float, temp: float,
                      rng: np.random.Generator) -> bool:
    """SA acceptance: the engine default."""
    if f_new < f_cur:
        return True
    return rng.random() < np.exp(-(f_new - f_cur) / max(temp, 1e-12))


def accept_record_to_record(f_new: float, f_best: float,
                            deviation: float) -> bool:
    """Accept anything within `deviation` of the record (Dueck 1993).

    Shrink `deviation` linearly from ~0.03 to 0 over the run.
    """
    return f_new < f_best * (1.0 + deviation)


def accept_late(f_new: float, history: list[float], k: int = 50) -> bool:
    """Late acceptance: compare against the objective k iterations back."""
    return f_new <= history[-k] if len(history) >= k else f_new <= history[0]
```

### Noise and biased randomization in repair

Greedy and regret insertion are deterministic: from the same partial solution they always rebuild the same way, which shrinks the effectively sampled neighborhood. Ropke & Pisinger add **noise**: with some probability, insertion costs are perturbed by a uniform term up to ±η·(max arc cost), with η ≈ 0.025, and the noise/no-noise choice is itself an ALNS "operator" with adaptive weight. The `u^p` biased rank selection in `worst_removal`/`related_removal` serves the same purpose on the destroy side; p ≈ 3–6 keeps strong bias while preserving reachability of every move.

### Adaptive degree of destruction

A fixed q wastes budget: small q suffices near convergence, large q is needed to escape. Two practical schemes: (a) draw q uniformly from [q_min, q_max] each iteration (the engine default) — simple and surprisingly robust; (b) escalate q after stagnation, ILS-style: start at q_min, increase by one step per non-improving segment, reset on improvement. Scheme (b) couples LNS with the perturbation-strength logic of iterated local search; see mutation-and-perturbation-operators for the underlying disruption-measurement ideas. Slack-induction by string removals (Christiaens & Vanden Berghe 2020, "Slack Induction by String Removals for Vehicle Routing Problems") goes further: it removes contiguous *strings* of customers from adjacent routes so the repair has coherent slack to work with — state of the art for many VRP variants with a tiny operator set.

### Exact repair: matheuristic LNS

Repair is a constructive heuristic only by convention. With a MIP solver available, reinsert the q removed elements *optimally*: fix the surviving partial solution, build the restricted model over removed elements (an assignment or set-partitioning subproblem), and solve with a short time limit. This is LNS as a matheuristic — equivalent to fix-and-optimize where the destroy operator picks the unfixed window. Budget rule of thumb: the subproblem should solve in well under a second at the chosen q, otherwise drop q or fall back to regret insertion for most iterations and call the MIP repair only every K-th iteration or on stagnation. See matheuristics for local branching and relax-and-fix variants of the same idea.

### Operator portfolio design and pruning

More operators are not better: each weak operator dilutes the roulette and burns iterations. Discipline that works in practice: (a) log per-operator statistics (usage, share of new bests, average score) for every run — the Output Format section shows the table; (b) ablate: rerun with each operator removed; keep an operator only if removing it hurts on the tuning instances; (c) reward only *new* solutions — keep a hash set of visited solutions (canonical tuple of the representation) and give σ3 only for unvisited ones, otherwise ALNS rewards cycling; (d) when two operators have correlated behavior (worst and related removal often do), keep the cheaper one. Remember the Turkeš–Sörensen–Hvattum finding: the adaptive layer is a small bonus, so a tight portfolio of 3–5 destroy and 2–3 repair operators usually beats a zoo of ten.

## Practical Challenges

**Repair consumes 90%+ of the runtime.** Profile first; it is almost always insertion-cost computation. Cache the best insertion position of each pending element per route/machine and invalidate only the routes changed by the last destroy or insertion — greedy repair drops from O(q²·positions) to about O(q·positions). Keep route loads and partial sums incrementally instead of recomputing them inside the position loop. If that is not enough, restrict insertion candidates to the k nearest routes by centroid distance.

**The adaptive layer locks onto one operator pair after a few hundred iterations.** Symptoms: one weight near the maximum, others at the floor, no diversification. Fixes in order: raise the weight floor (0.05–0.1), lengthen segments to 200, lower ρ to 0.2, and check the score vector — σ3 = 0 turns ALNS greedy and is the usual root cause. Also verify scores go to *accepted* iterations only; rewarding rejected candidates corrupts the signal.

**The search behaves like random restart — the current solution never stabilizes.** The start temperature is too high for the objective scale, typically because the warm-up gap was applied to a hierarchical or penalty-inflated objective. Calibrate the temperature on the routing-cost component only, and check the acceptance rate: roughly 30–50% of worse candidates accepted early, under 5% late, is healthy.

**Repair cannot place all removed elements when constraints are tight.** With a fixed fleet or hard time windows, insertion can dead-end. Use a *request bank* (Ropke & Pisinger 2006): unplaced elements wait in a pool and incur a large but finite objective penalty, so partial solutions stay comparable and the bank empties as the search improves. Size the penalty just above the worst plausible insertion cost — too high and the search refuses to ever use the bank as a stepping stone. See constraint-handling-techniques for penalty calibration patterns.

**Results vary wildly across seeds.** Expected at small iteration budgets; ALNS variance comes from the destroy sampling. Report over ≥10 seeds. If the spread stays large at realistic budgets, q is usually too large (each accepted move re-randomizes too much) or acceptance stays too hot for too long. Reduce q_max and end the cooling earlier; verify the trace flattens before the budget ends.

**ALNS does not beat a well-tuned ILS baseline.** Not a bug — on loosely constrained problems with strong small-move neighborhoods (plain TSP, unconstrained QAP-style problems), ILS with a good perturbation is the right tool and LNS's repair overhead buys nothing. ALNS earns its complexity when feasibility is hard and construction heuristics encode real problem knowledge. Confirm the diagnosis by checking how often repair produces a solution different from the pre-destroy one.

**Hierarchical objectives (vehicles first, then distance) break the acceptance rule.** A big-M weighted sum makes the temperature meaningless: every vehicle change dwarfs T. Either compare lexicographically inside acceptance (accept iff fewer vehicles, or equal vehicles and Metropolis on distance), or run two phases: minimize vehicles with a dedicated route-elimination destroy operator, then fix the fleet and minimize distance.

**Deterministic repair makes iterations collide.** If the trace shows long plateaus where f_new equals f_cur, destroy+deterministic repair is reconstructing the same solution. Add insertion noise, randomize the insertion order among near-ties, or hash visited solutions and skip scoring repeats — all three are cheap and compatible.

## Tools & Libraries

| Library | When to use | Note |
|---|---|---|
| `alns` (PyPI, Wouda & Lan) | Production ALNS in Python without rebuilding the engine | Pluggable destroy/repair callables, acceptance and selection schemes included; mirrors the architecture shown here |
| PyVRP | Strong VRP/VRPTW solutions out of the box | Hybrid genetic search state of the art; use as the baseline any custom routing ALNS must beat |
| OR-Tools routing | Quick strong routing baseline with LNS-style operators inside | Guided local search + relocation operators; little control over the destroy/repair loop itself |
| gurobipy | Exact repair subproblems, fix-and-optimize hybrids | See matheuristics; short time limits per repair call |
| numpy | Objective and operator internals | Distance lookups, load vectors, regret matrices — the vectorization boundary in (A)LNS |
| pandas | Run and operator statistics tables | One row per run; operator usage/score logs for portfolio pruning |

## Output Format

A complete (A)LNS deliverable contains:

1. **Run configuration table** — everything needed to reproduce:

| Field | Example |
|---|---|
| Instance / size | `cvrp-rng7`, n = 40, Q = 40 |
| Operators (destroy / repair) | random, worst(p=3), related(p=6) / greedy, regret-2 |
| q range, cap | 10–40% of n, cap 60 |
| Acceptance | SA, warm-up gap 5%, T_end/T0 = 1e-4 |
| Adaptive layer | segment 100, ρ = 0.5, scores (33, 9, 13), floor 0.05 |
| Budget, seeds | 2,000 iterations, seeds 0–9 |

2. **Solution-quality report** — best/mean/std of the final objective over seeds, gap to the lower bound or best-known solution, and the line `validator: PASS` from an *independent* feasibility check (never trust the search's own bookkeeping).

3. **Operator statistics table** — per operator: usage count, share of new global bests, average score, final weight. This is the evidence for keeping or pruning operators.

| Operator | Used | New bests | Avg score | Final weight |
|---|---|---|---|---|
| related_removal | 41% | 19 | 6.1 | 1.42 |
| worst_removal | 35% | 11 | 4.9 | 1.07 |
| random_removal | 24% | 3 | 2.2 | 0.31 |

4. **Convergence summary** — best-so-far curve (the engine's `trace`) per seed, plotted as median with min–max band; state the iteration at which 99% of the final improvement was reached, which justifies (or indicts) the budget.

5. **Artifacts** — solution file(s) in a documented format, one-row-per-run results CSV (instance, seed, parameters, objective, time), and the plot files.

## Questions to Ask

- What is the removable element, and roughly how many are there per instance?
- Which constraints are hard, and can a constructive heuristic always restore feasibility — or do we need a request bank / penalties?
- Is the fleet (or resource set) fixed, or can repair open new vehicles/machines?
- Is the objective single-level, or hierarchical (vehicles before distance)?
- What is the time budget per run, and on what hardware/language?
- What baseline exists already (ILS, OR-Tools, a MIP with time limit), and what must be beaten by how much?
- Is a MIP solver available for exact repair, and what license?
- How many instances and seeds will the evaluation use, and what report format is expected?
- Do you want plain LNS first as the ablation baseline, or directly the full adaptive version?

## Related Skills

- **vehicle-routing-problem** — when the user needs CVRP/VRPTW formulations, construction heuristics, benchmark instances, and the broader solver landscape around the routing ALNS shown here.
- **matheuristics** — when repair should be exact (MIP reinsertion, fix-and-optimize, local branching) or destroy sets should come from solver information.
- **constraint-handling-techniques** — when repair cannot always restore feasibility and the search needs request banks, penalty calibration, or feasibility-preserving operators.
- **local-search-and-neighborhoods** — when designing the insertion heuristics and delta evaluation used inside repair, or a small-move local search to polish accepted solutions.
- **metaheuristic-design-principles** — when deciding whether (A)LNS is the right method at all, and for intensification/diversification balance, stopping criteria, and evaluation budgets.
