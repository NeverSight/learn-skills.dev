---
name: particle-swarm-optimization
description: When the user wants to design, implement, or tune particle swarm optimization, covering velocity and position updates, inertia weight, constriction, swarm topologies, and discrete adaptations such as random-key and binary PSO. Also use when the user mentions "particle swarm," "PSO," "inertia weight," "velocity update," "swarm topology," or "binary PSO," or when a gradient-free continuous box-constrained problem needs a population method. For the often stronger vector-difference alternative, see differential-evolution; for mapping particles to permutations, see decoder-based-representations.
---

# Particle Swarm Optimization

You are an expert in particle swarm optimization (PSO) for continuous and combinatorial
optimization. This skill covers the canonical velocity/position dynamics, inertia and
constriction variants, swarm topologies, parameter selection, and discrete adaptations
(random-key decoding and probability-based binary PSO). Use the framework below to
implement, configure, and diagnose PSO, and to decide when PSO is the right tool versus
an alternative population method.

## Initial Assessment

Establish the following before writing any code:

- **Search-space type.** Continuous box-constrained vectors are PSO's native habitat.
  Permutations, subsets, and schedules require a decoder (random keys) or the binary
  variant. Identify which case applies — it changes the algorithm, not just a parameter.
- **Dimension `d` and bounds.** Confirm explicit lower/upper bounds per variable. PSO
  needs them for initialization and velocity clamping. Note whether bounds are hard
  physical limits (must repair) or soft search-region hints.
- **Evaluation cost and total budget.** Ask for the cost of one objective evaluation and
  the budget (evaluation count or wall-clock). PSO spends `n_particles` evaluations per
  iteration; a 40-particle swarm over 1,000 iterations is 40,000 evaluations.
- **Batch evaluability.** Determine whether the objective can evaluate an
  `(n_particles, d)` matrix in one vectorized call. If yes, the whole swarm update is a
  handful of numpy operations and Python overhead disappears.
- **Multimodality.** A roughly unimodal landscape favors gbest topology and aggressive
  convergence; a rugged landscape favors ring topology, restarts, and larger swarms.
- **Constraints beyond bounds.** Decide the handling strategy up front: penalty in the
  objective, repair after the position update, or a feasibility-enforcing decoder.
- **Quality requirement.** A good feasible solution within budget, or a near-optimal
  result that must beat a published baseline? The second demands tuning, multi-seed
  protocols, and a comparison method.
- **Gradients.** If the objective is smooth and gradients are available, multistart
  L-BFGS will usually beat PSO. Use PSO when gradients are absent, noisy, or misleading.
- **Baseline.** Always plan a sanity baseline: random search at equal budget, and
  differential evolution for continuous problems. PSO results without a baseline are
  uninterpretable.
- **Reproducibility.** Fix seeds (`np.random.default_rng(seed)`), record every parameter,
  and plan at least 10-30 independent seeds for any reported comparison.

## Algorithm Anatomy

### Core dynamics

Each particle `i` carries a position `x_i` (a candidate solution), a velocity `v_i`, and
a memory `p_i` of its best visited position (personal best). It is also influenced by
`l_i`, the best personal best in its neighborhood (which neighborhood depends on the
topology). The canonical inertia-weight update (Shi & Eberhart, 1998, "A modified
particle swarm optimizer") is:

$$
v_i^{t+1} = w\,v_i^t + c_1\, r_1 \odot (p_i^t - x_i^t) + c_2\, r_2 \odot (l_i^t - x_i^t)
$$

$$
x_i^{t+1} = x_i^t + v_i^{t+1}
$$

where `r1, r2 ~ U(0,1)^d` are redrawn for every particle, component, and iteration, and
`⊙` is the component-wise product. The three velocity terms have distinct roles:

| Term | Name | Role |
|---|---|---|
| `w v_i` | inertia | momentum; keeps the particle exploring its current direction |
| `c1 r1 (p_i - x_i)` | cognitive | pull back toward the particle's own best find |
| `c2 r2 (l_i - x_i)` | social | pull toward the best find in the neighborhood |

The original formulation (Kennedy & Eberhart, 1995, "Particle swarm optimization") had
`w = 1` and diverges without velocity clamping. Two stabilizations dominate practice:

**Inertia weight:** fix `w < 1` (typically 0.72984) or schedule it from 0.9 down to 0.4.

**Constriction coefficient** (Clerc & Kennedy, 2002, "The particle swarm — explosion,
stability, and convergence in a multidimensional complex space"):

$$
v_i^{t+1} = \chi \left[ v_i^t + c_1 r_1 (p_i - x_i) + c_2 r_2 (l_i - x_i) \right],
\qquad
\chi = \frac{2}{\left| 2 - \varphi - \sqrt{\varphi^2 - 4\varphi} \right|},
\quad \varphi = c_1 + c_2 > 4 .
$$

With the standard choice `c1 = c2 = 2.05` (`φ = 4.1`), `χ ≈ 0.72984`. The constriction
form is algebraically identical to the inertia form with `w = χ` and accelerations
`χ·c = 1.49618` (Eberhart & Shi, 2000, "Comparing inertia weights and constriction
factors in particle swarm optimization"). These values give provable order-2 stability
of the sampling distribution (Poli, 2009, "Mean and variance of the sampling distribution
of particle swarm optimizers during stagnation"). Treat them as the default; deviate only
with evidence from tuning.

### Topology

The topology is the static social graph deciding which particles inform each other:

| Topology | Neighborhood | Behavior |
|---|---|---|
| gbest (star) | whole swarm | fastest information spread; fastest convergence; highest premature-convergence risk |
| lbest ring, `k` neighbors each side | 2k+1 particles | slow information spread; much more robust on multimodal landscapes |
| von Neumann (grid) | 4 lattice neighbors | empirically strong compromise (Kennedy & Mendes, 2002, "Population structure and particle swarm performance") |

Bratton & Kennedy (2007, "Defining a standard for particle swarm optimization")
recommend the ring topology with 50 particles as the reference configuration (SPSO):
gbest wins on easy unimodal functions but loses badly on multimodal ones, and the ring's
extra cost is only slower early convergence.

### Parameter guidance

| Parameter | Typical range | What it trades off |
|---|---|---|
| Swarm size `n` | 20-50 (50 in SPSO; 100+ only for `d` > 50 or heavy multimodality) | exploration per iteration vs. number of iterations under a fixed evaluation budget |
| Inertia `w` | 0.72984 fixed, or 0.9 → 0.4 linear schedule | momentum/exploration vs. settling speed; `w ≥ 1` diverges without clamping |
| Cognitive `c1` | 1.0-2.05 (default 1.49618 with `w = 0.72984`) | independent exploration around own history vs. slow convergence |
| Social `c2` | 1.0-2.05 (default 1.49618) | fast collective convergence vs. premature collapse onto one basin |
| Velocity clamp `v_max` | 10-50% of each variable's range | overshoot control vs. a step-size ceiling that slows fine refinement |
| Topology | gbest / ring (`k` = 1-2) / von Neumann | information-spread speed vs. robustness; pick ring unless the landscape is known unimodal |
| Iterations | budget / `n` | refinement depth vs. swarm breadth |

### When to use PSO — and when not

- **Use PSO** for continuous, box-constrained, gradient-free problems of moderate
  dimension (`d` up to ~100), especially when the objective evaluates in batch and you
  want a simple, transparent algorithm with few parameters.
- **Prefer differential evolution** when you can afford a small tuning budget: on
  standard continuous suites DE configurations are usually at least as strong, and its
  parameter behavior is better understood (see **differential-evolution**).
- **Prefer CMA-ES** for ill-conditioned, non-separable continuous problems; PSO has no
  mechanism to learn variable correlations.
- **Prefer native combinatorial methods** (local search, tabu search, GA with permutation
  operators, ILS) for permutation and assignment problems. Random-key PSO is a legitimate
  quick baseline, not a state-of-the-art method there — be explicit about this with users.

**Complexity.** Per iteration: `O(n·d)` arithmetic for the update plus `n` objective
evaluations plus `O(n·k)` for neighborhood-best lookups. Memory: `O(n·d)` for positions,
velocities, and personal bests. The objective evaluation dominates in any realistic
application, which is why batch evaluation matters more than micro-optimizing the update.

## Reference Implementation

The skeleton first; every PSO variant in this skill is a small change to it.

```text
PSO(objective, bounds, n_particles, n_iter, w, c1, c2, topology):
    initialize x_i uniformly in [lo, hi]
    initialize v_i small (e.g., 10% of the variable range)
    evaluate f(x_i); set personal bests p_i = x_i
    repeat n_iter times:
        for each particle i (vectorized over the whole swarm):
            l_i = argmin of pbest objective within i's neighborhood   # topology
            draw r1, r2 ~ U(0,1)^d                                    # fresh each time
            v_i = w*v_i + c1*r1*(p_i - x_i) + c2*r2*(l_i - x_i)
            clamp v_i to [-v_max, v_max]
            x_i = x_i + v_i
            repair x_i against bounds (clamp / reflect), adjust v_i
            if f(x_i) < f(p_i): p_i = x_i
    return the best personal best
```

The generic minimizer below is fully vectorized: one numpy expression per update step,
no per-particle Python loop. It supports gbest and ring topologies and uses the
constriction-equivalent defaults.

```python
import numpy as np
from dataclasses import dataclass
from typing import Callable


@dataclass
class PSOResult:
    """Best solution found plus the best-so-far trajectory."""
    best_x: np.ndarray
    best_f: float
    history: np.ndarray  # best-so-far objective value per iteration


def ring_neighbors(n: int, k: int = 1) -> np.ndarray:
    """Row i lists particle i's ring neighborhood: itself plus k indices on each side."""
    offsets = np.arange(-k, k + 1)
    return (np.arange(n)[:, None] + offsets[None, :]) % n


def pso(
    objective: Callable[[np.ndarray], np.ndarray],
    bounds: tuple[np.ndarray, np.ndarray],
    n_particles: int = 40,
    n_iter: int = 500,
    w: float = 0.72984,
    c1: float = 1.49618,
    c2: float = 1.49618,
    topology: str = "gbest",
    ring_k: int = 1,
    v_clamp: float = 0.5,
    seed: int = 0,
) -> PSOResult:
    """Vectorized PSO for minimization.

    `objective` must map an (n_particles, d) array to an (n_particles,) cost vector.
    Defaults are the constriction-equivalent values chi = 0.72984, chi * 2.05 = 1.49618
    (Clerc & Kennedy, 2002).
    """
    rng = np.random.default_rng(seed)
    lo, hi = bounds
    d = lo.size
    span = hi - lo
    v_max = v_clamp * span

    x = lo + rng.random((n_particles, d)) * span
    v = rng.uniform(-1.0, 1.0, (n_particles, d)) * span * 0.1
    f = objective(x)
    pbest_x, pbest_f = x.copy(), f.copy()
    nbrs = ring_neighbors(n_particles, ring_k) if topology == "ring" else None
    history = np.empty(n_iter)

    for t in range(n_iter):
        if nbrs is None:  # gbest: every particle sees the swarm-wide best
            l_idx = np.full(n_particles, int(np.argmin(pbest_f)))
        else:  # lbest: best personal best inside each ring window
            l_idx = nbrs[np.arange(n_particles), np.argmin(pbest_f[nbrs], axis=1)]

        r1 = rng.random((n_particles, d))
        r2 = rng.random((n_particles, d))
        v = w * v + c1 * r1 * (pbest_x - x) + c2 * r2 * (pbest_x[l_idx] - x)
        v = np.clip(v, -v_max, v_max)
        x = x + v

        out = (x < lo) | (x > hi)  # absorbing walls: clamp position, zero velocity
        x = np.clip(x, lo, hi)
        v = np.where(out, 0.0, v)

        f = objective(x)
        improved = f < pbest_f
        pbest_x[improved] = x[improved]
        pbest_f[improved] = f[improved]
        history[t] = pbest_f.min()

    best = int(np.argmin(pbest_f))
    return PSOResult(pbest_x[best].copy(), float(pbest_f[best]), history)


def sphere(x: np.ndarray) -> np.ndarray:
    """Sum of squares; unimodal, optimum 0 at the origin."""
    return np.sum(x * x, axis=1)


lo, hi = np.full(20, -5.12), np.full(20, 5.12)
result = pso(sphere, (lo, hi), n_particles=40, n_iter=600, seed=1)
print(f"sphere 20-D best: {result.best_f:.2e}")
# Expected: best objective below 1e-6 — gbest PSO converges fast on unimodal functions.
```

Implementation notes:

- **Personal bests are the memory.** The social attractor is always drawn from
  `pbest_x`, never from current positions; current positions may be worse than anything
  in memory.
- **Boundary handling** here is "absorb": clamp to the bound and zero the offending
  velocity component. Alternatives are discussed under Advanced Techniques; the choice
  measurably affects results in high dimensions.
- **Synchronous update.** All particles see the same neighborhood bests from the start
  of the iteration. Asynchronous updates (each particle immediately publishes its new
  pbest) converge slightly faster but are harder to vectorize and to reproduce.

## Worked Example 1: Continuous Benchmark Functions

Benchmarks are the controlled environment for verifying an implementation and choosing
a topology before touching the real problem. Two standard test functions, batched:

```python
import numpy as np


def rastrigin(x: np.ndarray) -> np.ndarray:
    """Highly multimodal with a regular grid of local optima; optimum 0 at the origin."""
    return np.sum(x * x - 10.0 * np.cos(2.0 * np.pi * x) + 10.0, axis=1)


def rosenbrock(x: np.ndarray) -> np.ndarray:
    """Long curved narrow valley; optimum 0 at (1, ..., 1)."""
    return np.sum(
        100.0 * (x[:, 1:] - x[:, :-1] ** 2) ** 2 + (1.0 - x[:, :-1]) ** 2, axis=1
    )
```

Rastrigin in 10-D is the classic topology stress test. gbest collapses into the nearest
deep local optimum; the ring keeps subpopulations searching different basins:

```python
import numpy as np
# Uses pso() from the reference implementation and rastrigin() defined above.

lo, hi = np.full(10, -5.12), np.full(10, 5.12)

rows: list[tuple[str, int, float]] = []
for topology in ("gbest", "ring"):
    for seed in range(5):
        res = pso(rastrigin, (lo, hi), n_particles=40, n_iter=1500,
                  topology=topology, ring_k=1, seed=seed)
        rows.append((topology, seed, res.best_f))

for topology in ("gbest", "ring"):
    vals = np.array([f for t, _, f in rows if t == topology])
    print(f"{topology:5s}  median {np.median(vals):7.3f}  best {vals.min():7.3f}")
# Expected: gbest median roughly 10-30 (stuck in local optima on several seeds);
# ring median clearly lower and less spread. Neither reliably reaches 0 in 10-D
# without restarts — that is the point of the test, not a bug.
```

Read the outcome as a decision rule, not a score: if your real problem behaves like
Rastrigin (many comparable basins), commit to the ring topology, more particles, and a
restart policy. If it behaves like Rosenbrock (single valley, bad conditioning), gbest
with a `w` schedule refines faster — and CMA-ES is worth a comparison run. Always report
the median and spread over seeds; a single PSO run proves nothing.

## Worked Example 2: TSP via Random-Key Decoding

PSO is continuous, the TSP is a permutation problem. The random-key bridge (Bean, 1994,
"Genetic algorithms and random keys for sequencing and optimization") keeps the particle
continuous in `[0, 1]^d` and decodes it by `argsort`: the city with the smallest key is
visited first. Velocity updates remain unchanged; only evaluation passes through the
decoder. Decoder design choices and their trade-offs are covered in depth in
**decoder-based-representations** — this section applies the simplest sort decoder.

The decoder costs `O(d log d)` per particle and is heavily redundant: a continuum of key
vectors maps to the same tour, and a small velocity step often changes nothing. That
redundancy is the price of reusing the continuous machinery.

```python
import numpy as np
from typing import Callable


def decode_keys(keys: np.ndarray) -> np.ndarray:
    """Random-key decoder: argsort each row of keys into a permutation per particle."""
    return np.argsort(keys, axis=1)


def make_tsp_objective(dist: np.ndarray) -> Callable[[np.ndarray], np.ndarray]:
    """Batch objective: (n_particles, n_cities) keys -> (n_particles,) closed-tour lengths."""
    def objective(keys: np.ndarray) -> np.ndarray:
        tours = decode_keys(keys)
        nxt = np.roll(tours, -1, axis=1)
        return dist[tours, nxt].sum(axis=1)
    return objective
```

A circle instance makes correctness visible: the optimal tour is the circle order, and
its length has a closed form.

```python
import numpy as np
# Uses pso() from the reference implementation and make_tsp_objective() defined above.

n_cities = 9
angles = 2.0 * np.pi * np.arange(n_cities) / n_cities
points = np.column_stack([np.cos(angles), np.sin(angles)])
dist = np.linalg.norm(points[:, None, :] - points[None, :, :], axis=2)

objective = make_tsp_objective(dist)
bounds = (np.zeros(n_cities), np.ones(n_cities))
res = pso(objective, bounds, n_particles=60, n_iter=500, topology="ring",
          v_clamp=0.3, seed=3)
tour = np.argsort(res.best_x)
print(f"tour {tour}, length {res.best_f:.4f}")
# Expected: length 6.1564 = 9 * 2*sin(pi/9), the cities in circle order
# (up to rotation and reversal). At n = 9, random-key PSO finds the optimum on
# most seeds; beyond roughly 30 cities it degrades fast without a local-search hybrid.
```

Honest scope statement to give users: random-key PSO is a reasonable baseline and a good
demonstration of decoder-based search, but it does not compete with 2-opt/Or-opt local
search, Lin-Kernighan, or a tuned GA with permutation crossovers on the TSP. If the user
needs TSP quality rather than a PSO exercise, say so and redirect. The decoder pattern
itself, however, generalizes well to scheduling problems where construction order matters
more than adjacency.

## Discrete Variant: Probability-Based Binary PSO

For subset-selection problems (knapsack, feature selection, facility opening decisions),
binary PSO (Kennedy & Eberhart, 1997, "A discrete binary version of the particle swarm
algorithm") reinterprets velocity as a per-bit propensity: `sigmoid(v)` is the
probability that the bit is 1 in the next iteration. Positions are resampled from these
probabilities every iteration — there is no position increment.

Two behavioral quirks to warn users about. First, large `|v|` means a *saturated*,
frozen bit, so velocity clamping (typically `v_max` of 4-6, giving flip probabilities
between ~0.002 and ~0.998) is what keeps exploration alive, the opposite of its role in
continuous PSO. Second, the inertia weight's effect is also inverted: small `w` pushes
velocities toward 0 and bits toward coin flips, so `w` near 0.9-1.0 is the stable choice.

```python
import numpy as np
from typing import Callable


def binary_pso(
    objective: Callable[[np.ndarray], np.ndarray],
    d: int,
    n_particles: int = 30,
    n_iter: int = 300,
    w: float = 0.9,
    c1: float = 2.0,
    c2: float = 2.0,
    v_max: float = 4.0,
    seed: int = 0,
) -> tuple[np.ndarray, float]:
    """Probability-based binary PSO (Kennedy & Eberhart, 1997), minimization.

    Velocity is a flip propensity: sigmoid(v) is the probability that a bit is 1.
    `objective` maps an (n_particles, d) 0/1 array to (n_particles,) costs.
    """
    rng = np.random.default_rng(seed)
    x = (rng.random((n_particles, d)) < 0.5).astype(np.int8)
    v = rng.uniform(-1.0, 1.0, (n_particles, d))
    f = objective(x)
    pbest_x, pbest_f = x.copy(), f.copy()

    for _ in range(n_iter):
        g = pbest_x[int(np.argmin(pbest_f))]
        r1 = rng.random((n_particles, d))
        r2 = rng.random((n_particles, d))
        v = w * v + c1 * r1 * (pbest_x - x) + c2 * r2 * (g - x)
        v = np.clip(v, -v_max, v_max)
        prob_one = 1.0 / (1.0 + np.exp(-v))
        x = (rng.random((n_particles, d)) < prob_one).astype(np.int8)
        f = objective(x)
        improved = f < pbest_f
        pbest_x[improved] = x[improved]
        pbest_f[improved] = f[improved]

    best = int(np.argmin(pbest_f))
    return pbest_x[best].copy(), float(pbest_f[best])
```

Validation on a 6-item 0-1 knapsack with a linear infeasibility penalty (for the broader
penalty-vs-repair decision, see the constraint-handling discussion in
**metaheuristic-design-principles**):

```python
import numpy as np
# Uses binary_pso() defined above.

values = np.array([60.0, 100.0, 120.0, 30.0, 70.0, 90.0])
weights = np.array([10.0, 20.0, 30.0, 5.0, 15.0, 25.0])
capacity = 60.0


def knapsack_cost(x: np.ndarray) -> np.ndarray:
    """Negative total value plus a penalty of 50 per unit of excess weight."""
    value = x @ values
    excess = np.maximum(0.0, x @ weights - capacity)
    return -value + 50.0 * excess


best_x, best_f = binary_pso(knapsack_cost, d=6, n_particles=30, n_iter=200, seed=5)
print(f"items {np.flatnonzero(best_x)}, value {best_x @ values:.0f}, "
      f"weight {best_x @ weights:.0f}")
# Expected: value 280 at weight 60. Two optimal subsets exist: {0, 1, 2} and
# {0, 2, 3, 4}. A 6-bit instance is trivial for BPSO; it exists to validate the code.
```

For serious binary problems, compare BPSO against a GA with bit-flip mutation and an
estimation-of-distribution baseline before recommending it; BPSO's advantage is mainly
its small implementation surface, not solution quality.

## Advanced Techniques

### Inertia schedules and adaptive parameters

A linearly decreasing `w` front-loads exploration and back-loads refinement; the
success-rate rule adapts `w` online — when many particles still improve their personal
bests, momentum is productive and `w` rises (Nickabadi, Ebadzadeh & Safabakhsh, 2011,
"A novel particle swarm optimization algorithm with adaptive inertia weight").

```python
import numpy as np


def linear_inertia(t: int, n_iter: int, w_start: float = 0.9, w_end: float = 0.4) -> float:
    """Linearly decreasing inertia weight (Shi & Eberhart, 1998)."""
    return w_start - (w_start - w_end) * t / max(n_iter - 1, 1)


def success_rate_inertia(w: float, success_rate: float,
                         target: float = 0.2, step: float = 0.05) -> float:
    """Raise w while many particles improve their pbest; lower it once improvement dries up."""
    if success_rate > target:
        return min(w + step, 0.9)
    return max(w - step, 0.3)
```

Wire either into the reference loop by replacing the constant `w` with a per-iteration
value (`success_rate` is `improved.mean()` from the pbest update). Adaptive schedules
buy robustness across instances more than peak performance on any single instance.

### Velocity clamping and boundary handling

Three boundary policies, in increasing order of exploration preserved: **absorb** (clamp
position, zero the velocity component — the reference implementation), **reflect**
(mirror the position inside the bound and negate the velocity component), and
**invisible walls** (leave the particle outside but skip its evaluation; it gets pulled
back by its attractors). In high dimensions a large fraction of particles touches a
bound every iteration, so the policy choice is not cosmetic — test absorb vs. reflect on
your problem before tuning anything else. Keep `v_max` per-dimension and proportional to
each variable's range; a global scalar `v_max` breaks on mixed-scale variables.

### Stagnation detection, diversity, and partial restarts

PSO stagnates silently: velocities shrink, the swarm contracts around the gbest, and the
best-so-far curve flattens while iterations keep burning budget. Monitor both the
objective trend and a spatial diversity measure, and restart the worst particles when
both flatline. Diversity metrics, niching, and restart policy design are treated fully
in **diversity-and-population-management**.

```python
import numpy as np


def swarm_diversity(x: np.ndarray) -> float:
    """Mean Euclidean distance from particles to the swarm centroid."""
    return float(np.linalg.norm(x - x.mean(axis=0), axis=1).mean())


def partial_restart(x: np.ndarray, v: np.ndarray, pbest_f: np.ndarray,
                    lo: np.ndarray, hi: np.ndarray, frac: float,
                    rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    """Reinitialize the worst `frac` of particles; personal-best memories stay intact."""
    n = x.shape[0]
    k = max(1, int(frac * n))
    worst = np.argpartition(pbest_f, -k)[-k:]
    x, v = x.copy(), v.copy()
    x[worst] = lo + rng.random((k, lo.size)) * (hi - lo)
    v[worst] = 0.0
    return x, v
```

A practical trigger: restart 30-50% of particles when the best-so-far value improved by
less than `1e-8` over the last 50 iterations *and* diversity fell below 1% of its initial
value. Keeping the personal bests preserves the swarm's memory, so a restart costs little.

### Multi-swarm and comprehensive learning variants

When a single swarm keeps collapsing, structural fixes beat parameter fixes. Cooperative
PSO splits the dimensions across subswarms that optimize their block against the current
best context (van den Bergh & Engelbrecht, 2004, "A cooperative approach to particle
swarm optimization") — effective for high-dimensional separable-ish problems. Comprehensive
Learning PSO (Liang, Qin, Suganthan & Baskar, 2006, "Comprehensive learning particle
swarm optimizer for global optimization of multimodal functions") replaces the single
social attractor with a per-dimension exemplar drawn from different particles' personal
bests, which slows convergence but strongly resists premature collapse on multimodal
functions. Reach for these only after the standard SPSO configuration with ring topology
and restarts has demonstrably failed.

### Hybridization with local search

The highest-leverage upgrade for combinatorial uses: periodically decode the best
particles and improve the phenotype with problem-specific local search (2-opt for tours,
swap/insertion for schedules), then re-encode the improved solution into the particle's
personal best (a Lamarckian update — write the improvement back into the key vector by
assigning sorted key values in the improved order). Budget local search like any other
evaluation cost: polishing the top 10% of the swarm every 20 iterations is a sane
default. This turns a mediocre random-key PSO into a competitive memetic method, but at
that point compare honestly against a memetic GA — the swarm dynamics may no longer be
the ingredient doing the work.

## Practical Challenges

**The swarm collapses onto one point in early iterations and never recovers.**
Classic premature convergence: gbest topology plus high `c2` lets one early lucky find
absorb the swarm. Switch to ring topology, use the constriction defaults, and add the
diversity-triggered partial restart. Verify by logging `swarm_diversity` per iteration —
a healthy run shows gradual, not cliff-shaped, contraction.

**Velocities explode and particles spend every iteration pinned to the bounds.**
`w ≥ 1`, missing velocity clamp, or `c1 + c2` far above `2(1 + w)`. Restore the stable
triple (0.72984, 1.49618, 1.49618), clamp velocity per dimension, and check that the
initial velocity scale is a fraction of the variable range, not of the whole domain.

**Random-key PSO loses to a plain local search on a permutation problem.**
Expected, not a bug. The sort decoder is redundant (many key vectors per tour) and PSO's
arithmetic on keys has no notion of adjacency or precedence. Hybridize with local search
(see Advanced Techniques), or switch to a native-operator method and keep PSO only if
the user's requirement is specifically a PSO-based approach.

**Binary PSO freezes: every bit probability sits near 0 or 1.**
Velocity saturation. Tighten `v_max` to 4 (flip probabilities then stay within roughly
[0.018, 0.982]), keep `w` near 0.9, and consider re-randomizing the velocities of
stagnant particles. Inspect `sigmoid(v)` histograms, not just objective values.

**Results vary wildly across seeds and the "best run" is being reported.**
PSO has high run-to-run variance by nature. Fix a seed list up front, run 20+ seeds,
and report median, interquartile range, and worst case. Never tune on the same seeds
used for reporting.

**The objective is too expensive for 40 particles × 1,000 iterations.**
Cut the swarm before cutting iterations (small swarms with ring topology degrade
gracefully; 10-15 particles is workable), vectorize the objective to evaluate the whole
swarm per call, and add an evaluation cache keyed on the decoded phenotype for
decoder-based problems where many particles decode identically.

**Constraints beyond bounds keep producing infeasible final answers.**
A static penalty that is too small makes infeasibility profitable; too large flattens
the landscape. Start with a penalty proportional to constraint violation magnitude,
validate the final solution with an independent feasibility check, and if feasibility is
hard to hit at all, move the constraint into a feasibility-enforcing decoder instead of
the objective.

**Published "improved PSO" parameters do not transfer to your problem.**
Most PSO-variant papers tune on small benchmark suites. Treat published values as
starting points, re-tune swarm size and topology on a held-out instance set, and always
include the plain SPSO configuration as a control — it is embarrassingly often the best
of the lot.

## Tools & Libraries

| Library | When to use | Note |
|---|---|---|
| numpy (this skill's pattern) | research code, full control, custom variants | the whole algorithm is ~60 lines; easiest to instrument and extend |
| pyswarms | quick continuous or binary PSO baseline | ready-made gbest/lbest/binary optimizers with topology options |
| pymoo | comparing PSO against GA/DE/NSGA-II in one framework | consistent termination and result objects across algorithms |
| nevergrad | black-box budget shootouts | PSO among dozens of optimizers behind one ask/tell interface |
| DEAP | custom evolutionary loops with PSO primitives | flexible but more boilerplate than a direct numpy implementation |
| mealpy | surveying many metaheuristic variants fast | large algorithm zoo; verify any implementation against a reference before publishing results |
| scipy.optimize | no PSO included | `differential_evolution` is the natural continuous baseline to run alongside |

## Output Format

A complete PSO deliverable contains:

1. **Configuration table** — every parameter with its value and one-line justification:
   swarm size, iterations, `w` (or schedule), `c1`, `c2`, topology, `v_max`, boundary
   policy, seed list, and for discrete problems the decoder.
2. **Convergence evidence** — the `history` array per seed, summarized as a median
   best-so-far curve with an interquartile band. A single-run curve is not evidence.
3. **Result table** — one row per (instance, seed); aggregate per instance:

   | instance | seeds | best | median | IQR | mean evals | time/run (s) |
   |---|---|---|---|---|---|---|
   | rastrigin-10d | 20 | 4.97 | 12.93 | 6.2 | 60,000 | 0.4 |
   | tsp-circle-9 | 20 | 6.156 | 6.156 | 0.0 | 30,000 | 0.2 |

4. **Baseline comparison** — random search at equal budget always; differential
   evolution for continuous problems; a native-operator heuristic for combinatorial
   ones. State the evaluation budget explicitly so the comparison is fair.
5. **Validation** — for constrained or decoded problems, recompute feasibility and the
   objective from the final phenotype with code independent of the swarm loop.
6. **Reproducibility block** — numpy version, seed list, and the exact command or
   function call; a reader must be able to regenerate every number in the table.
7. **Stated limitations** — where PSO was not the strongest choice and why it was used
   anyway (simplicity, user requirement, legacy comparison).

## Questions to Ask

- Is the search space continuous, binary, or a permutation — and if not continuous,
  is a decoder acceptable or is a native method preferred?
- What are the per-variable bounds, and are they hard constraints or search hints?
- How expensive is one objective evaluation, and what is the total budget
  (evaluations or wall-clock)?
- Can the objective evaluate the whole swarm as one `(n, d)` batch?
- Are there constraints beyond bounds, and should they be penalized, repaired, or
  built into a decoder?
- Is there a known optimum, bound, or published baseline to measure quality against?
- Is this a one-off solve or a recurring production task that justifies tuning?
- How many seeds and instances are available for a statistically defensible report?

## Related Skills

- **differential-evolution** — when the problem is continuous and you want the usually
  stronger vector-difference alternative, or self-adaptive variants (jDE, SHADE).
- **decoder-based-representations** — when applying PSO to permutations or schedules
  and the random-key or rule-based decoder needs careful design.
- **diversity-and-population-management** — when the swarm converges prematurely and
  you need diversity measures, restart policies, or niching.
- **metaheuristic-design-principles** — when choosing between PSO and other
  metaheuristics, or designing constraint handling and stopping criteria.
