---
name: hyper-heuristics
description: When the user wants to build a hyper-heuristic — a search method that selects or generates low-level heuristics instead of searching solutions directly — covering selection hyper-heuristics (heuristic selection plus move acceptance), low-level heuristic pool design, learning and reward schemes, and generation hyper-heuristics. Also use when the user mentions "hyper-heuristic," "operator selection," "low-level heuristics," "heuristic selection," "move acceptance," "choice function," or when many candidate operators exist and none dominates across instances. For adaptive destroy/repair weights, see large-neighborhood-search; for choosing the overall search paradigm, see metaheuristic-design-principles.
---

# Hyper-Heuristics

You are an expert in hyper-heuristics for combinatorial optimization — search methods that operate on a *space of heuristics* rather than directly on the space of solutions. This skill covers selection hyper-heuristics (heuristic selection plus move acceptance), the design of low-level heuristic pools, online learning and credit assignment (reward schemes), and generation hyper-heuristics that assemble new heuristics from components. Use the framework below to take a user from "I have many candidate operators and no idea which to apply when" to a reproducible hyper-heuristic with measured operator usage, a calibrated acceptance criterion, and a defensible ablation against simpler baselines.

## Initial Assessment

Establish these facts before writing any hyper-heuristic code:

- **Why a hyper-heuristic at all.** If one well-understood metaheuristic with one strong neighborhood already works, a hyper-heuristic adds machinery without value. The case for a hyper-heuristic is: a pool of plausible operators with instance-dependent usefulness, heterogeneous instances, or a requirement for cross-domain reuse.
- **Pool inventory.** Which low-level heuristics already exist (moves, repair rules, construction rules)? A hyper-heuristic cannot fix a weak pool — it only arbitrates among the heuristics it is given. Aim for 4–12 heuristics with genuinely different behaviors.
- **Constructive or perturbative low-level heuristics.** Constructive heuristics extend a partial solution (pick the next packing rule, the next dispatching rule); perturbative heuristics modify a complete solution (move, swap, ruin-and-recreate). The loop structure differs; decide first.
- **Objective and scaling.** One scalar objective the engine can read through the domain barrier. If hard constraints are penalized, fix the penalty weights before any credit learning — rewards inherit the objective's scale.
- **Evaluation cost and budget.** Iterations available = time budget / (heuristic call + evaluation). Credit assignment needs hundreds of selections per heuristic to mean anything; with fewer than ~50 calls per heuristic, use uniform random selection.
- **Per-call cost asymmetry.** Does the pool mix microsecond moves with millisecond ruin-and-recreate heuristics? If yes, credit must be improvement *per unit time*, not per call, or cheap heuristics will be unfairly favored — and vice versa.
- **Online vs offline learning.** Online: learn during the run on this instance (selection rules below). Offline: tune selection/acceptance parameters or evolve heuristics on a training instance set beforehand. Most practical systems combine both.
- **No-op behavior.** Can a heuristic return the solution unchanged (e.g., no feasible swap found)? Decide how no-ops are credited (zero reward) and detected, or they silently distort the statistics.
- **Acceptance scale.** Move acceptance needs either a temperature (Metropolis) or a history length (late acceptance). Both must be set relative to the objective scale and the iteration budget.
- **Single-domain or cross-domain.** A one-problem project can let problem knowledge leak into selection. A cross-domain tool must keep the domain barrier strict: the engine sees only objective values and heuristic indices.
- **Baselines.** Always run (a) uniform random selection with the same pool and acceptance, and (b) the single best heuristic alone. The learning layer must beat both to justify itself.
- **Reproducibility.** One `np.random.default_rng(seed)` per run, seeds and parameters logged per run, usage statistics saved with results.

## Hyper-Heuristic Anatomy

### Heuristic space and the domain barrier

A hyper-heuristic searches over heuristics: "heuristics to choose heuristics" (Cowling, Kendall & Soubeiga 2001, "A Hyperheuristic Approach to Scheduling a Sales Summit"; the term itself appears in Denzinger, Fuchs & Fuchs 1997). The defining architectural idea is the **domain barrier**: the high-level strategy sees only (i) the indices of the low-level heuristics, (ii) the objective value returned after applying one, and (iii) bookkeeping such as elapsed time. It never sees the solution representation. Everything problem-specific lives below the barrier, inside the low-level heuristics and the evaluation function. This is what makes the high-level strategy reusable across domains, and it is enforced literally in the HyFlex benchmark framework (Ochoa et al. 2012, "HyFlex: A Benchmark Framework for Cross-domain Heuristic Search").

The standard classification (Burke et al. 2010, "A Classification of Hyper-heuristic Approaches"; surveyed in Burke et al. 2013, "Hyper-heuristics: A Survey of the State of the Art" and Drake et al. 2020, "Recent Advances in Selection Hyper-heuristics") has two axes:

| Axis | Options | Coverage in this skill |
|---|---|---|
| Nature of the heuristic space | **selection** (choose from a fixed pool) vs **generation** (build new heuristics from components) | selection in depth; generation as a working sketch |
| Nature of the low-level heuristics | **constructive** (extend partial solutions) vs **perturbative** (modify complete solutions) | perturbative engine + constructive bin-packing rules |
| Feedback | online learning, offline learning, no learning | online credit schemes; offline tuning/evolution |

### Selection hyper-heuristic = heuristic selection + move acceptance

A selection hyper-heuristic decomposes into two nearly independent components (Özcan, Bilgin & Korkmaz 2008, "A Comprehensive Analysis of Hyper-heuristics"): a **selection rule** that picks the next low-level heuristic, and a **move acceptance** rule that decides whether the modified solution replaces the incumbent. Both matter; in the CHeSC 2011 cross-domain competition, the winner AdapHH (Mısır et al. 2012) combined adaptive selection with an adaptive acceptance threshold, and ablations show acceptance often contributes more than selection.

**Credit assignment.** After applying heuristic $i$ to incumbent $x$ and obtaining $x'$, assign a reward and update a quality estimate $q_i$ by a recency-weighted average:

$$
r_t = \frac{\max\big(0,\; f(x) - f(x')\big)}{s_t} \;+\; \mathbf{1}\{f(x') < f(x^*)\}, \qquad
q_i \leftarrow (1-\lambda)\, q_i + \lambda\, r_t ,
$$

where $s_t$ is a running scale of $|f|$ (keeps rewards dimensionless) and the indicator adds a new-global-best bonus. This is non-stationary reinforcement learning in the sense of Nareyek (2003), "Choosing Search Heuristics by Non-Stationary Reinforcement Learning": the value of a heuristic changes as the search moves through the landscape, so old evidence must decay.

**Selection rules**, in increasing sophistication:

- *Uniform random* — the mandatory baseline; "simple random" in the HH literature.
- *$\varepsilon$-greedy* — exploit $\arg\max_i q_i$ with probability $1-\varepsilon$, explore uniformly otherwise.
- *Roulette (probability matching)* — select $i$ with probability $\propto q_i + q_{\min}$; smooth but slow to commit.
- *Upper confidence bound (UCB)* — treat selection as a multi-armed bandit (Fialho et al. 2010, "Analyzing Bandit-based Adaptive Operator Selection Mechanisms"):

$$
i_t = \arg\max_i \left( q_i + c \sqrt{\frac{\ln t}{n_i}} \right),
$$

with $n_i$ the usage count and $c$ the exploration strength. The decay $\lambda$ in $q_i$ supplies the non-stationarity handling that plain UCB lacks.

- *Choice function* — a learned score combining solo performance, pairwise (follow-up) performance, and time since last use (Cowling et al. 2001); implementation in Advanced Techniques.

**Move acceptance** rules, with their characters:

- *Improve-only* (`improve_only`): accept iff $f(x') \le f(x)$. Greedy; stalls in local optima but a clean ablation baseline.
- *Accept-all* (`accept_all`): the search becomes a random walk guided only by selection; useful with very strong, self-improving heuristics (e.g., a pool of ruin-and-recreate operators).
- *Metropolis*: accept worse moves with probability $e^{-(f(x')-f(x))/T}$, $T$ cooled geometrically — simulated-annealing acceptance.
- *Late acceptance* (LAHC; Burke & Bykov 2017, "The Late Acceptance Hill-Climbing Heuristic"): accept iff $f(x') \le f(x)$ **or** $f(x') \le f_{t-L}$, the incumbent value $L$ iterations ago, kept in a ring buffer. One parameter ($L$), no temperature calibration, strong empirical record — the recommended default.

### Decision guidance

- **Use a selection hyper-heuristic when** you have ≥4 heuristics whose relative usefulness varies by instance or by search phase, and an evaluation budget of at least a few thousand iterations.
- **Use the ALNS framing instead when** your heuristics decompose naturally into destroy and repair halves applied as a pair — that is a selection hyper-heuristic specialized to routing/scheduling; see large-neighborhood-search for segment-based weight updates.
- **Use a single tuned metaheuristic when** one neighborhood dominates (e.g., 2-opt on plain TSP) — see metaheuristic-design-principles for the selection logic.
- **Use a generation hyper-heuristic when** the deliverable is a *reusable fast rule* (a dispatching rule, a packing rule) to be applied online to many future instances, not one solution to one instance.
- **Complexity.** The high-level layer costs $O(k)$ per iteration for $k$ heuristics — negligible. Runtime is dominated by heuristic calls and objective evaluations; spend engineering effort below the barrier (delta evaluation inside low-level heuristics), not above it.

### Parameter guidance

| Parameter | Typical range | Increasing it buys | At the cost of |
|---|---|---|---|
| Pool size $k$ | 4–12 | Behavioral coverage | Credit split thinner, slower learning |
| $\varepsilon$ ($\varepsilon$-greedy) | 0.05–0.30 | Starvation protection, exploration | Budget spent on weak heuristics |
| UCB exploration $c$ | 0.3–2.0 | Re-testing of currently weak heuristics | Slower commitment to the best heuristic |
| Reward decay (memory) $1-\lambda$ | 0.90–0.99 | Stable estimates, long memory | Slow reaction to search-phase changes |
| New-best bonus | 0.5–2.0 (normalized units) | Bias toward record-breaking heuristics | Overrates single lucky events |
| LAHC list length $L$ | 50–5,000 | Diversification, better final quality | Slower convergence; scale $L$ with budget |
| Metropolis $T_0$ | 1–10% of $\|f(x_0)\|$ | Early exploration | Random-walk burn-in |
| Cooling rate | set so $T_{\text{end}}/T_0 \approx 10^{-3}$ over the budget | Final intensification | Long frozen tail |
| Segment length (batched updates) | 50–200 iterations | Stable per-segment scores | Slower adaptation |

Tune acceptance ($L$ or the temperature schedule) before tuning selection; it usually has the larger effect. For offline tuning of these parameters over an instance set, use the protocol in optuna-hyperparameter-tuning. For the design of the low-level moves themselves, reuse the operator catalogs in mutation-and-perturbation-operators and local-search-and-neighborhoods rather than re-inventing them.

## Reusable Selection Hyper-Heuristic Engine

The engine is problem-independent and enforces the domain barrier: it sees the solution only as an opaque object passed to `copy_solution`, the heuristics, and `objective`. Low-level heuristics have the uniform signature `(solution, rng) -> solution` and may mutate their argument (the engine always passes a copy).

```text
SELECTION-HH(x0, pool H = {h1..hk}, budget M)
  x <- x0;  x* <- x
  q_i <- 0, n_i <- 0  for all i                  // learned quality, usage count
  for t = 1 .. M:
      i  <- SELECT(q, n, t)                      // uniform | eps-greedy | roulette | UCB
      x' <- h_i(copy(x))                         // apply low-level heuristic
      r  <- max(0, f(x) - f(x')) / scale         // credit ...
             + bonus if f(x') < f(x*)            //   ... with new-best bonus
      q_i <- (1 - lambda) * q_i + lambda * r     // recency-weighted average
      n_i <- n_i + 1
      if ACCEPT(f(x'), f(x), memory):            // improve-only | accept-all | LAHC | Metropolis
          x <- x'
      if f(x') < f(x*):  x* <- x'
      update acceptance memory                   // LAHC ring buffer / temperature
  return x*, usage statistics
```

```python
"""Problem-independent single-point selection hyper-heuristic (minimization)."""
from dataclasses import dataclass, field
from typing import Any, Callable

import numpy as np

LowLevelHeuristic = Callable[[Any, np.random.Generator], Any]


@dataclass
class HHResult:
    """Outcome and bookkeeping of one hyper-heuristic run."""
    best: Any
    f_best: float
    usage: np.ndarray       # times each heuristic was selected
    accepted: np.ndarray    # times its candidate was accepted
    new_best: np.ndarray    # times it produced a new global best
    trace: list[float] = field(default_factory=list)  # best-so-far per iteration


class SelectionHyperHeuristic:
    """Heuristic selection + move acceptance over a pool of low-level heuristics.

    selection : 'uniform' | 'epsilon_greedy' | 'roulette' | 'ucb'
    acceptance: 'improve_only' | 'accept_all' | 'late_acceptance' | 'metropolis'
    """

    def __init__(
        self,
        heuristics: list[LowLevelHeuristic],
        objective: Callable[[Any], float],
        copy_solution: Callable[[Any], Any],
        selection: str = "ucb",
        acceptance: str = "late_acceptance",
        epsilon: float = 0.15,
        ucb_c: float = 0.5,
        reward_decay: float = 0.95,
        la_length: int = 100,
        t0: float | None = None,
        cooling: float = 0.999,
        seed: int = 0,
    ) -> None:
        self.heuristics = heuristics
        self.objective = objective
        self.copy_solution = copy_solution
        self.selection = selection
        self.acceptance = acceptance
        self.epsilon = epsilon
        self.ucb_c = ucb_c
        self.reward_decay = reward_decay
        self.la_length = la_length
        self.t0 = t0
        self.cooling = cooling
        self.rng = np.random.default_rng(seed)

    def _select(self, q: np.ndarray, n: np.ndarray, it: int) -> int:
        """Pick a heuristic index from quality estimates q and usage counts n."""
        k = q.size
        if self.selection == "uniform":
            return int(self.rng.integers(k))
        if self.selection == "epsilon_greedy":
            if self.rng.random() < self.epsilon:
                return int(self.rng.integers(k))
            return int(self.rng.choice(np.flatnonzero(q == q.max())))
        if self.selection == "roulette":
            w = q - q.min() + 1e-6
            return int(self.rng.choice(k, p=w / w.sum()))
        untried = np.flatnonzero(n == 0)  # selection == 'ucb'
        if untried.size:
            return int(untried[0])
        bound = q + self.ucb_c * np.sqrt(np.log(it + 1.0) / n)
        return int(self.rng.choice(np.flatnonzero(bound == bound.max())))

    def _accept(self, f_new: float, f_cur: float, f_late: float, t: float) -> bool:
        """Move acceptance: does the candidate replace the incumbent?"""
        if self.acceptance == "improve_only":
            return f_new <= f_cur
        if self.acceptance == "accept_all":
            return True
        if self.acceptance == "late_acceptance":
            return f_new <= f_cur or f_new <= f_late
        if f_new <= f_cur:  # acceptance == 'metropolis'
            return True
        return self.rng.random() < np.exp(-(f_new - f_cur) / max(t, 1e-12))

    def run(self, x0: Any, n_iters: int) -> HHResult:
        """Run the selection hyper-heuristic loop from initial solution x0."""
        k = len(self.heuristics)
        cur = self.copy_solution(x0)
        f_cur = self.objective(cur)
        best, f_best = self.copy_solution(cur), f_cur
        q = np.zeros(k)                      # recency-weighted reward per heuristic
        n = np.zeros(k)
        accepted = np.zeros(k, dtype=int)
        new_best = np.zeros(k, dtype=int)
        late = np.full(self.la_length, f_cur)
        t = self.t0 if self.t0 is not None else 0.05 * abs(f_cur) + 1e-9
        scale = abs(f_cur) + 1e-9            # running reward normalizer
        trace: list[float] = []
        for it in range(n_iters):
            i = self._select(q, n, it)
            cand = self.heuristics[i](self.copy_solution(cur), self.rng)
            f_cand = self.objective(cand)
            n[i] += 1
            reward = max(0.0, f_cur - f_cand) / scale
            if f_cand < f_best:
                reward += 1.0                # new-global-best bonus
            q[i] = self.reward_decay * q[i] + (1.0 - self.reward_decay) * reward
            if self._accept(f_cand, f_cur, float(late[it % self.la_length]), t):
                cur, f_cur = cand, f_cand
                accepted[i] += 1
            if f_cand < f_best:
                best, f_best = self.copy_solution(cand), f_cand
                new_best[i] += 1
            late[it % self.la_length] = f_cur
            scale = 0.99 * scale + 0.01 * (abs(f_cur) + 1e-9)
            t *= self.cooling
            trace.append(f_best)
        return HHResult(best, f_best, n.astype(int), accepted, new_best, trace)
```

Smoke test on a synthetic problem: minimize the quadratic pseudo-boolean function $f(x) = x^\top Q x$, $x \in \{0,1\}^{60}$, with a four-heuristic pool that mixes blind perturbations and one greedy move. The greedy move uses the closed-form flip delta $\Delta_j = (1-2x_j)(Q_{jj} + 2\sum_{i\ne j} Q_{ij}x_i)$.

```python
"""Smoke test: binary quadratic minimization with a four-heuristic pool."""
import numpy as np

rng0 = np.random.default_rng(7)
N = 60
Q = rng0.normal(0.0, 1.0, (N, N))
Q = (Q + Q.T) / 2.0


def f_bqp(x: np.ndarray) -> float:
    """Quadratic pseudo-boolean objective x^T Q x (minimize)."""
    return float(x @ Q @ x)


def flip_one(x: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Flip one random bit."""
    x[int(rng.integers(x.size))] ^= 1
    return x


def flip_three(x: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Flip three distinct random bits."""
    x[rng.choice(x.size, 3, replace=False)] ^= 1
    return x


def flip_block(x: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Flip a contiguous block of five bits (strong perturbation)."""
    j = int(rng.integers(x.size - 5))
    x[j:j + 5] ^= 1
    return x


def best_single_flip(x: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Greedy: flip the bit with the steepest objective decrease."""
    s = Q @ x - np.diag(Q) * x
    deltas = (1 - 2 * x) * (np.diag(Q) + 2 * s)
    x[int(np.argmin(deltas))] ^= 1
    return x


pool = [flip_one, flip_three, flip_block, best_single_flip]
x0 = rng0.integers(0, 2, N)
hh = SelectionHyperHeuristic(pool, f_bqp, np.copy, selection="epsilon_greedy",
                             acceptance="late_acceptance", la_length=80, seed=11)
res = hh.run(x0, n_iters=3000)
print(f"f(x0)={f_bqp(x0):.1f}  f_best={res.f_best:.1f}")
names = ["flip1", "flip3", "block5", "greedy"]
print("usage:", dict(zip(names, res.usage)))
print("new_best:", dict(zip(names, res.new_best)))
# Expected: f_best around -229 from a start near -33; usage concentrates on
# the greedy flip (~1,900 of 3,000 calls, ~35 of ~36 new bests), with
# flip_one second (~870 calls) as the cheap escape move.
```

Read the usage statistics before celebrating: a healthy $\varepsilon$-greedy run shows the intensifier exploited heavily while the exploration floor keeps every heuristic alive. Selection rules differ in how the learning shows up: on this same instance UCB finds the same $f^{best}$ but with *near-uniform usage* (750 calls each), because once rewards vanish its confidence radii equalize the counts — under UCB, read the `new_best` and `accepted` columns, not raw usage. If a blind perturbation dominates `new_best`, the reward scale or the acceptance criterion is broken.

## Worked Example 1: Exam Timetabling Selection Hyper-Heuristic

Timetabling is the classic hyper-heuristic domain (the field grew out of timetabling and rostering systems; see timetabling-and-rostering for full domain models and benchmark formats). The instance here: $n$ events, $T$ timeslots, and a symmetric conflict matrix $C$ where $C_{ij}$ counts students enrolled in both events $i$ and $j$. The solution is a slot vector $s \in \{0,\dots,T-1\}^n$. The cost combines hard conflicts (same slot) and a proximity soft cost — a linear simplification of the Carter cost $2^{4-d}$ (Carter, Laporte & Lee 1996, "Examination Timetabling: Algorithmic Strategies and Applications"):

$$
f(s) = W \sum_{i<j,\; s_i = s_j} C_{ij} \;+\; \sum_{i<j,\; 1 \le |s_i - s_j| \le 2} C_{ij}\,\big(3 - |s_i - s_j|\big), \qquad W = 1000 .
$$

```python
"""Exam timetabling: instance, vectorized cost, and a five-heuristic pool."""
import numpy as np


def make_timetabling_instance(n_events: int, n_slots: int, density: float,
                              seed: int) -> tuple[np.ndarray, int]:
    """Random symmetric conflict matrix; C[i, j] = students shared by events i, j."""
    rng = np.random.default_rng(seed)
    raw = np.where(rng.random((n_events, n_events)) < density,
                   rng.integers(1, 10, (n_events, n_events)), 0)
    C = np.triu(raw, 1)
    return C + C.T, n_slots


def timetable_cost(slots: np.ndarray, C: np.ndarray,
                   hard_weight: float = 1000.0) -> float:
    """Hard: conflicting events in one slot. Soft: proximity max(0, 3 - d)."""
    D = np.abs(slots[:, None] - slots[None, :])
    hard = (C * (D == 0)).sum() / 2.0
    soft = (C * np.maximum(0, 3 - D) * (D > 0)).sum() / 2.0
    return hard_weight * float(hard) + float(soft)


def make_timetabling_pool(C: np.ndarray, n_slots: int) -> list:
    """Five perturbative low-level heuristics closing over the instance."""
    n = C.shape[0]

    def event_penalty(slots: np.ndarray) -> np.ndarray:
        """Per-event share of the total cost (for targeting bad events)."""
        D = np.abs(slots[:, None] - slots[None, :])
        pen = C * ((D == 0) * 1000.0 + np.maximum(0, 3 - D) * (D > 0))
        return pen.sum(axis=1)

    def move_random(slots: np.ndarray, rng: np.random.Generator) -> np.ndarray:
        """Move one random event to one random slot."""
        slots[int(rng.integers(n))] = int(rng.integers(n_slots))
        return slots

    def move_worst_greedy(slots: np.ndarray, rng: np.random.Generator) -> np.ndarray:
        """Pick among the 5 worst events; place it in its cheapest slot."""
        e = int(rng.choice(np.argsort(event_penalty(slots))[-5:]))
        costs = np.empty(n_slots)
        for sl in range(n_slots):
            d = np.abs(slots - sl)
            costs[sl] = (C[e] * ((d == 0) * 1000.0
                                 + np.maximum(0, 3 - d) * (d > 0))).sum()
        slots[e] = int(rng.choice(np.flatnonzero(costs == costs.min())))
        return slots

    def swap_events(slots: np.ndarray, rng: np.random.Generator) -> np.ndarray:
        """Exchange the slots of two random events."""
        a, b = rng.choice(n, 2, replace=False)
        slots[a], slots[b] = slots[b], slots[a]
        return slots

    def kempe_chain(slots: np.ndarray, rng: np.random.Generator) -> np.ndarray:
        """Swap a Kempe chain between a random event's slot and a target slot."""
        e = int(rng.integers(n))
        a, b = int(slots[e]), int(rng.integers(n_slots))
        if a == b:
            return slots
        in_ab = (slots == a) | (slots == b)
        chain, frontier = {e}, [e]
        while frontier:
            v = frontier.pop()
            for u in np.flatnonzero((C[v] > 0) & in_ab):
                if int(u) not in chain:
                    chain.add(int(u))
                    frontier.append(int(u))
        idx = np.fromiter(chain, dtype=int)
        slots[idx] = np.where(slots[idx] == a, b, a)
        return slots

    def shuffle_slot(slots: np.ndarray, rng: np.random.Generator) -> np.ndarray:
        """Scatter all events of one random slot (diversification)."""
        members = np.flatnonzero(slots == int(rng.integers(n_slots)))
        if members.size:
            slots[members] = rng.integers(n_slots, size=members.size)
        return slots

    return [move_random, move_worst_greedy, swap_events, kempe_chain, shuffle_slot]
```

The pool deliberately mixes intensifiers (`move_worst_greedy`, `kempe_chain` — the standard timetabling/coloring move that swaps a connected component between two slots and never splits a conflict pair across the wrong side) with diversifiers (`move_random`, `shuffle_slot`). That mix is what the selection layer is for: the right blend changes between the "repair hard conflicts" phase and the "polish proximity cost" phase, and the credit scheme tracks the change.

```python
"""Run the engine on a 50-event, 9-slot instance and report usage."""
import numpy as np

C, n_slots = make_timetabling_instance(n_events=50, n_slots=9,
                                       density=0.20, seed=3)
pool = make_timetabling_pool(C, n_slots)
names = ["move_random", "move_worst_greedy", "swap_events",
         "kempe_chain", "shuffle_slot"]

x0 = np.random.default_rng(1).integers(n_slots, size=50)
hh = SelectionHyperHeuristic(
    heuristics=pool,
    objective=lambda s: timetable_cost(s, C),
    copy_solution=np.copy,
    selection="epsilon_greedy",
    acceptance="late_acceptance",
    la_length=200,
    seed=1,
)
res = hh.run(x0, n_iters=6000)
D = np.abs(res.best[:, None] - res.best[None, :])
hard_left = int((C * (D == 0)).sum() / 2)
print(f"start cost={timetable_cost(x0, C):.0f}  final cost={res.f_best:.0f}  "
      f"hard conflicts left={hard_left}")
for nm, u, a, b in zip(names, res.usage, res.accepted, res.new_best):
    print(f"{nm:18s} used={u:5d} accepted={a:5d} new_best={b:3d}")
# Expected: hard conflicts reach 0 and the final cost is pure proximity
# penalty around 270 (start: ~158,600). Usage concentrates on
# move_worst_greedy (~2,600 calls, every one accepted, ~47 new bests) and
# kempe_chain (~1,700 calls); shuffle_slot stays a rare diversifier.
```

## Worked Example 2: Bin Packing with a Heuristic Pool

One-dimensional bin packing: items with sizes $w_i$, bins of capacity $c$, minimize the number of bins $B$. The raw bin count is a terrible search objective — it forms huge plateaus where almost no move changes the value. Use the Falkenauer fitness (Falkenauer 1996, "A Hybrid Grouping Genetic Algorithm for Bin Packing"), here written as a minimization cost:

$$
f(\text{assign}) = 1 - \frac{1}{B} \sum_{b=1}^{B} \left( \frac{\text{fill}_b}{c} \right)^2 ,
$$

which strictly prefers packings with a few very full bins plus one slack bin over evenly half-full bins, giving the search a gradient toward emptying bins. All pool heuristics below are feasibility-preserving, so no penalty term is needed.

```python
"""Bin packing: representation helpers, Falkenauer cost, pool, validator."""
import numpy as np


def compact(assign: np.ndarray) -> np.ndarray:
    """Relabel bins to 0..B-1, removing empty labels."""
    return np.unique(assign, return_inverse=True)[1]


def best_fit_insert(assign: np.ndarray, sizes: np.ndarray, cap: float,
                    items: np.ndarray) -> np.ndarray:
    """Reinsert `items` largest-first into the tightest feasible bin (best fit),
    opening a new bin when nothing fits. Mutates and returns `assign`."""
    assign[items] = -1
    placed = assign >= 0
    n_bins = int(assign[placed].max()) + 1 if placed.any() else 0
    fills = np.bincount(assign[placed], weights=sizes[placed],
                        minlength=n_bins).astype(float)
    for i in items[np.argsort(-sizes[items])]:
        room = cap - fills
        feas = np.flatnonzero(room >= sizes[i] - 1e-9)
        if feas.size:
            b = int(feas[np.argmin(room[feas])])
        else:
            b = fills.size
            fills = np.append(fills, 0.0)
        assign[i] = b
        fills[b] += sizes[i]
    return assign


def falkenauer_cost(assign: np.ndarray, sizes: np.ndarray, cap: float) -> float:
    """1 - mean((fill/cap)^2): plateau-free bin-minimization surrogate."""
    a = compact(assign)
    fills = np.bincount(a, weights=sizes)
    return 1.0 - float(np.mean((fills / cap) ** 2))


def validate_packing(assign: np.ndarray, sizes: np.ndarray, cap: float) -> int:
    """Independent feasibility check; returns the number of bins used."""
    fills = np.bincount(assign, weights=sizes)
    assert (fills <= cap + 1e-9).all(), "capacity violated"
    assert (np.bincount(assign) > 0).all(), "empty bin label present"
    return int(assign.max()) + 1


def make_binpacking_pool(sizes: np.ndarray, cap: float) -> list:
    """Five feasibility-preserving low-level heuristics over an assignment vector."""
    n = sizes.size

    def fills_of(assign: np.ndarray) -> np.ndarray:
        """Current load of every bin label."""
        return np.bincount(assign, weights=sizes,
                           minlength=int(assign.max()) + 1)

    def move_item(assign: np.ndarray, rng: np.random.Generator) -> np.ndarray:
        """Move one random item to the tightest other bin with room."""
        i = int(rng.integers(n))
        room = cap - fills_of(assign)
        room[assign[i]] = -1.0
        feas = np.flatnonzero(room >= sizes[i])
        if feas.size:
            assign[i] = int(feas[np.argmin(room[feas])])
        return compact(assign)

    def swap_items(assign: np.ndarray, rng: np.random.Generator) -> np.ndarray:
        """Swap two items between bins if both capacities allow it."""
        i, j = rng.choice(n, 2, replace=False)
        bi, bj = int(assign[i]), int(assign[j])
        if bi == bj:
            return assign
        f = fills_of(assign)
        if (f[bi] - sizes[i] + sizes[j] <= cap
                and f[bj] - sizes[j] + sizes[i] <= cap):
            assign[i], assign[j] = bj, bi
        return assign

    def empty_smallest(assign: np.ndarray, rng: np.random.Generator) -> np.ndarray:
        """Empty the least-full bin; reinsert its items best-fit-decreasing."""
        items = np.flatnonzero(assign == int(np.argmin(fills_of(assign))))
        return compact(best_fit_insert(assign, sizes, cap, items))

    def empty_two_random(assign: np.ndarray, rng: np.random.Generator) -> np.ndarray:
        """Ruin-and-recreate: empty two random bins, reinsert best-fit-decreasing."""
        labels = np.unique(assign)
        if labels.size < 3:
            return assign
        chosen = rng.choice(labels, size=2, replace=False)
        items = np.flatnonzero(np.isin(assign, chosen))
        return compact(best_fit_insert(assign, sizes, cap, items))

    def largest_from_smallest(assign: np.ndarray,
                              rng: np.random.Generator) -> np.ndarray:
        """Relocate the largest item of the least-full bin (targets bin closure)."""
        f = fills_of(assign)
        b = int(np.argmin(f))
        items = np.flatnonzero(assign == b)
        i = int(items[np.argmax(sizes[items])])
        room = cap - f
        room[b] = -1.0
        feas = np.flatnonzero(room >= sizes[i])
        if feas.size:
            assign[i] = int(feas[np.argmin(room[feas])])
        return compact(assign)

    return [move_item, swap_items, empty_smallest,
            empty_two_random, largest_from_smallest]
```

The pool spans three granularities — single-item moves, pair swaps, and bin-level ruin-and-recreate — which is the bin-packing analogue of mixing small and large neighborhoods. `best_fit_insert` doubles as the constructor (called on an all-unassigned vector it performs best-fit-decreasing, BFD) and as the repair half of the ruin heuristics.

```python
"""Run: BFD start, hyper-heuristic improvement, independent validation."""
import numpy as np

rng = np.random.default_rng(42)
sizes = rng.integers(20, 70, size=60).astype(float)
cap = 100.0
lb = int(np.ceil(sizes.sum() / cap))           # L1 lower bound

x0 = best_fit_insert(np.full(60, -1), sizes, cap, np.arange(60))
bins0 = validate_packing(x0, sizes, cap)

hh = SelectionHyperHeuristic(
    heuristics=make_binpacking_pool(sizes, cap),
    objective=lambda a: falkenauer_cost(a, sizes, cap),
    copy_solution=np.copy,
    selection="epsilon_greedy",
    epsilon=0.2,
    acceptance="late_acceptance",
    la_length=300,
    seed=0,
)
res = hh.run(x0, n_iters=5000)
bins_final = validate_packing(res.best, sizes, cap)
names = ["move_item", "swap_items", "empty_smallest",
         "empty_two_random", "largest_from_smallest"]
print(f"L1 lower bound={lb}  BFD bins={bins0}  HH bins={bins_final}")
print("usage:", dict(zip(names, res.usage)))
# Expected: BFD opens 29 bins; the hyper-heuristic closes one and reaches the
# L1 bound of 28. swap_items dominates usage (~2,800 calls) by earning
# frequent small Falkenauer gains that skew fills; the bin-closing new-best
# events split between swap_items and ruin-and-recreate (empty_two_random).
```

If the run stalls at the BFD value, the usual cause is acceptance too greedy for a plateau-heavy problem — verify the Falkenauer cost is in use (not the bin count) and lengthen the LAHC list before touching the selection parameters.

## Advanced Techniques

### Choice-function selection

The choice function (Cowling et al. 2001) scores each heuristic by three terms: $f_1$ — decayed solo improvement; $f_2$ — decayed improvement when following the previously applied heuristic (captures productive pairs such as ruin→repair); $f_3$ — time since last use (a built-in diversification clock). The modified choice function of Drake, Özcan & Burke (2012, "An Improved Choice Function Heuristic Selection for Cross Domain Heuristic Search") replaces hand-tuned weights with a reactive $\phi$: jump to exploitation on any improvement, drift toward exploration otherwise.

```python
"""Choice-function heuristic selection (Cowling, Kendall & Soubeiga 2001),
with the reactive phi of Drake, Ozcan & Burke (2012)."""
import numpy as np


class ChoiceFunction:
    """Score_i = phi*(f1_i + f2[prev, i]) + (1 - phi)*(time since last use)."""

    def __init__(self, k: int, decay: float = 0.9) -> None:
        self.f1 = np.zeros(k)
        self.f2 = np.zeros((k, k))
        self.last_used = np.zeros(k)
        self.prev: int | None = None
        self.decay = decay
        self.phi = 0.5
        self.it = 0

    def select(self) -> int:
        """Greedy argmax of the choice function."""
        follow = self.f2[self.prev] if self.prev is not None else np.zeros_like(self.f1)
        score = (self.phi * (self.f1 + follow)
                 + (1.0 - self.phi) * (self.it - self.last_used))
        return int(np.argmax(score))

    def update(self, i: int, improvement: float) -> None:
        """Report f(x) - f(x') (positive = better) for the applied heuristic i."""
        self.it += 1
        self.last_used[i] = self.it
        self.f1[i] = improvement + self.decay * self.f1[i]
        if self.prev is not None:
            self.f2[self.prev, i] = improvement + self.decay * self.f2[self.prev, i]
        self.prev = i
        self.phi = 0.99 if improvement > 0 else max(0.01, self.phi - 0.01)


# Wiring into the engine loop: replace `i = self._select(q, n, it)` with
# `i = cf.select()` and the q-update with `cf.update(i, f_cur - f_cand)`.
```

The $f_2$ matrix is the cheapest way to learn heuristic *sequences*; if its entries dominate $f_1$ after a run, the pool has strong pair structure and a sequence-based method (below) is worth trying.

### Sequence-based selection

Single-step credit assumes the next-best heuristic is independent of what was just applied — often false (ruin is only good before repair; a greedy move is best right after a perturbation). The sequence-based selection hyper-heuristic of Kheiri & Keedwell (2015, "A Sequence-based Selection Hyper-heuristic Utilising a Hidden Markov Model") learns transition probabilities between heuristics plus an "end sequence / evaluate now" signal, effectively evolving short macros. The lightweight version: learn the $k \times k$ transition matrix exactly like the choice function's $f_2$, but *sample* the next heuristic from the softmax of the active row instead of taking an argmax, and only invoke acceptance at sequence ends.

### Acceptance engineering

Empirically, swapping the acceptance rule changes cross-domain performance more than swapping the selection rule (consistent with the ALNS finding of Santini et al. 2018 that acceptance criteria matter and simple ones do well — see large-neighborhood-search). Practical rules: LAHC's list length $L$ should scale with the iteration budget ($L \approx$ budget/100 is a sane start); Metropolis needs the warm-up calibration of $T_0$ from an accepted-gap target; accept-all only works when every heuristic embeds its own improvement step. For tight time budgets, record-to-record travel — accept iff $f(x') < f(x^*) + \theta$ with a shrinking $\theta$ — is a robust two-line alternative. Always re-tune acceptance after any change to the objective scaling (penalty weights included).

### Generation hyper-heuristics: evolving a packing rule

Generation hyper-heuristics search the space of heuristics themselves, classically with genetic programming over expression trees of problem features (Burke et al. 2009, "Exploring Hyper-heuristic Methodologies with Genetic Programming"; evolved packing and strip-packing rules that rediscover and beat first fit). The working sketch below keeps the idea and drops the GP machinery: parameterize an *index policy* — score every feasible bin by a weighted feature sum, pack into the argmax — and evolve the weights with a (1+1)-ES on a training set. The evolved object is a fast, reusable *online* heuristic, not a solution.

```text
GENERATION-HH (rule evolution)
  genome w  ->  rule "place item into feasible bin maximizing
                w0*fill + w1*leftover + w2*[perfect fit]"
  fitness(w) = total bins used by the rule over a TRAINING instance set
  search over w with (1+1)-ES (or CMA-ES / GP for richer rule spaces)
  validate the evolved rule on a held-out TEST instance set
```

```python
"""Generation hyper-heuristic sketch: evolve an online bin-packing index rule."""
import numpy as np


def pack_with_rule(w: np.ndarray, sizes: np.ndarray, cap: float) -> int:
    """Pack items in arrival order with the parameterized rule; return bins used."""
    fills: list[float] = []
    for s in sizes:
        best_b, best_score = -1, -np.inf
        for b, f in enumerate(fills):
            leftover = cap - f - s
            if leftover >= -1e-9:
                score = w[0] * f + w[1] * leftover + w[2] * (leftover < 1e-9)
                if score > best_score:
                    best_b, best_score = b, score
        if best_b < 0:
            fills.append(float(s))
        else:
            fills[best_b] += float(s)
    return len(fills)


def evolve_rule(train: list[np.ndarray], cap: float, iters: int = 150,
                seed: int = 0) -> np.ndarray:
    """(1+1)-ES over rule weights; fitness = total bins over training instances."""
    rng = np.random.default_rng(seed)
    w = rng.normal(0.0, 1.0, 3)
    f_w = sum(pack_with_rule(w, s, cap) for s in train)
    for _ in range(iters):
        cand = w + rng.normal(0.0, 0.3, 3)
        f_c = sum(pack_with_rule(cand, s, cap) for s in train)
        if f_c <= f_w:
            w, f_w = cand, f_c
    return w


rng = np.random.default_rng(5)
cap = 100.0
train = [rng.integers(20, 70, 60).astype(float) for _ in range(5)]
test = [rng.integers(20, 70, 60).astype(float) for _ in range(5)]
w_star = evolve_rule(train, cap, iters=150, seed=5)
best_fit = np.array([1.0, 0.0, 0.0])    # 'fullest feasible bin' = best fit
evolved_bins = sum(pack_with_rule(w_star, s, cap) for s in test)
bf_bins = sum(pack_with_rule(best_fit, s, cap) for s in test)
print(f"test bins: evolved={evolved_bins}  best-fit={bf_bins}")
# Expected: evolved=142, best-fit=142 on the held-out instances — the ES
# *rediscovers* best fit: the evolved weights put a large negative weight on
# leftover space, which is exactly the best-fit rule. Linear index policies
# rarely beat best fit; richer rule spaces (GP trees over more features,
# lookahead terms) are where evolved rules win, as in Burke et al. (2009).
```

Two disciplines carry over from machine learning: evolve on a *training* set and report on a *held-out* set (rules overfit to instance distributions), and always include the human-designed rule (best fit, first fit decreasing) as a baseline genome. Rediscovering the baseline, as above, is the expected outcome for a small rule space — it validates the pipeline before you pay for a larger one.

### Cross-domain design: the HyFlex lesson

HyFlex (Ochoa et al. 2012) fixed six domains (SAT, bin packing, personnel scheduling, flow shop, TSP, VRP), each exposing pools of mutation, ruin-recreate, local-search, and crossover heuristics behind a strict domain barrier; the CHeSC 2011 competition compared twenty high-level strategies on it. Lessons that generalize: (1) winners (AdapHH, Mısır et al. 2012) adapt *both* selection and acceptance, and dynamically exclude heuristics that perform badly on the current instance; (2) heuristic *type* information (mutational vs local search) is worth exploiting — alternate diversifying and intensifying types instead of treating the pool as flat; (3) robust average performance across domains, not peak performance on one, is the honest success metric for a hyper-heuristic — report it with the protocol from algorithm-benchmarking-statistics.

## Practical Challenges

**One heuristic starves the rest of the pool.** Greedy selection plus a strong intensifier produces 95% usage on one heuristic, and the search flatlines once its improvements dry up. Keep an exploration floor — $\varepsilon$-greedy's $\varepsilon$, UCB's $c$, or a minimum selection probability of 0.5–2% per heuristic — and rely on reward decay so a starved heuristic can recover when the phase changes.

**Rewards vanish as the search converges.** Late in a run all improvements are tiny, $q_i \to 0$ for every $i$, and selection degenerates to noise. Normalize rewards by a running scale (as the engine does), or switch to rank-based credit (reward = 1 for the best improvement in a sliding window, 0 otherwise) or extreme-value credit, which Fialho et al. (2010) show is more robust than average improvement precisely because operator value is driven by rare large gains.

**Cheap and expensive heuristics are credited per call.** A ruin-and-recreate heuristic costing 100× a swap must produce 100× the improvement per call to be worth selecting under a time budget. Divide rewards by measured call time (the choice function's original $f_1$ is improvement per second), and report usage in both calls and CPU share.

**Redundant heuristics split credit.** Two near-identical moves each look mediocre while their union is the best behavior in the pool. Diagnose by correlating per-heuristic acceptance patterns across a run; merge or drop duplicates. Pool curation beats selection tuning — AdapHH's dynamic exclusion of useless heuristics was central to winning CHeSC 2011.

**No-op moves poison the statistics.** Heuristics that fail to find a feasible change return the solution unchanged; with `improve_only`-style acceptance ($f' \le f$) they are "accepted," earn zero reward, and inflate acceptance counts. Detect candidates with unchanged objective and identical solution, credit zero, and if a heuristic no-ops more than ~30% of calls, fix the heuristic (let it fall back to a random feasible variant) rather than the selector.

**Selection and acceptance are tuned in isolation.** The two components interact: aggressive acceptance makes diversifying heuristics look good (their moves get accepted), greedy acceptance makes them look useless. Tune acceptance first with uniform selection, then freeze it and enable learning; finish with a 2×2 ablation (learned/uniform × tuned/default acceptance) so the contribution of each layer is measured, not assumed.

**The hyper-heuristic loses to a tuned single metaheuristic.** Expected on a single narrow instance class — the adaptive layer pays an exploration tax. The honest claims for a selection hyper-heuristic are robustness across heterogeneous instances and removal of per-instance operator tuning. If the project is one instance family forever, take the usage statistics from a hyper-heuristic run as a *design tool*, then hard-code the winning operator mix into a simpler method (see metaheuristic-design-principles).

**Results are irreproducible across runs.** Adaptive layers amplify seed sensitivity: an early lucky improvement locks selection onto one heuristic. Run ≥10 seeds, report distributions, and check that usage profiles are stable across seeds — unstable profiles mean the learner is reading noise, so increase reward memory or segment length.

## Tools & Libraries

| Library / framework | When to use | Note |
|---|---|---|
| numpy | All engines in this skill | `default_rng(seed)`; the HH layer is light — vectorize the objective and the low-level heuristics instead |
| `alns` (Python package) | Destroy/repair-shaped pools | Wouda & Lan (2023); mature operator-weight + acceptance machinery reusable as a selection HH scaffold |
| HyFlex (Java) | Cross-domain benchmarking of high-level strategies | Six domains, strict domain barrier, CHeSC 2011 reference results (Ochoa et al. 2012) |
| OR-Tools CP-SAT | When the timetabling/scheduling domain should be solved exactly instead | Try it before building a HH for small/medium instances |
| Optuna | Offline tuning of HH parameters ($\varepsilon$, $c$, $L$, decay) over an instance set | Tune on training instances only; see optuna-hyperparameter-tuning |
| irace | Offline configuration when runs are long and noisy | Racing discards bad configurations early |
| pandas + matplotlib | Usage logs, credit traces, convergence and usage-over-time plots | One row per iteration segment; plot usage share over time, not just totals |

## Output Format

A complete hyper-heuristic deliverable contains:

1. **Pool specification table** — one row per low-level heuristic: name, type (intensifier / diversifier / ruin-recreate), expected cost per call, feasibility behavior (preserving / repairing / may no-op).
2. **Engine configuration** — selection rule and its parameters, acceptance rule and its parameters, reward scheme (decay, bonus, normalization), seed policy, iteration/time budget.
3. **Solution-quality report** — per instance and seed: initial objective, final best objective, gap to bound or best known, wall-clock time; aggregated mean/median/std over seeds.
4. **Usage and credit table** — per heuristic: selections, acceptance rate, new-best count, CPU share, final $q_i$; ideally split into early/middle/late thirds of the run to show phase behavior.
5. **Ablation** — the same pool under uniform random selection, and the best single heuristic alone, same budget and seeds; a Wilcoxon signed-rank test over instances for the learned-vs-uniform comparison.
6. **Convergence trace** — best-so-far curve per seed (band plot), with acceptance-rate trace if acceptance is adaptive.
7. **Artifacts** — the result table (CSV/parquet, one row per run), usage log, and the exact config + seed needed to reproduce every row.

Example usage table (the timetabling run above, 6,000 iterations):

| Heuristic | Used | Accepted | New best | Role observed |
|---|---|---|---|---|
| move_worst_greedy | 2,601 | 2,601 | 47 | main intensifier (never worsens) |
| kempe_chain | 1,737 | 470 | 10 | conflict repair / polish |
| move_random | 1,073 | 193 | 6 | cheap escape |
| swap_events | 409 | 139 | 12 | occasional record-breaker |
| shuffle_slot | 180 | 10 | 0 | rare diversifier |

## Questions to Ask

- Which low-level heuristics already exist, and what does each cost per call?
- Is the goal one good solution for one instance, or a reusable solver across many heterogeneous instances?
- Roughly how many iterations fit in the time budget (evaluation cost × budget)?
- Are the low-level heuristics perturbative (modify complete solutions) or constructive (build solutions)?
- Can heuristics return the solution unchanged, and how often?
- Is there a single scalar objective, or do penalty weights for hard constraints still need fixing?
- What must the hyper-heuristic beat — a tuned single metaheuristic, uniform random selection, a MIP with a time limit?
- Do heuristic calls differ in cost by more than ~10×, forcing time-normalized credit?
- Single domain forever, or is cross-domain reuse (strict domain barrier) a requirement?
- How many seeds and instances are available for the offline tuning and the final comparison?

## Related Skills

- **metaheuristic-design-principles** — when the real question is which search paradigm to use at all; a hyper-heuristic is one design option among several, and its pool design follows the operator/representation guidance there.
- **selection-and-replacement-strategies** — when choosing the selection pressure mechanics (roulette, tournament-style argmax, probability matching) that drive heuristic selection; the same pressure/diversity trade-offs apply one level up.
- **large-neighborhood-search** — when the heuristic pool decomposes into destroy/repair pairs; ALNS is the specialized selection hyper-heuristic for that structure, with segment-based weight updates.
- **timetabling-and-rostering** — when the application is educational timetabling or rostering itself; that skill provides the full domain models, hard/soft constraint catalogs, and benchmark formats behind the worked example here.
