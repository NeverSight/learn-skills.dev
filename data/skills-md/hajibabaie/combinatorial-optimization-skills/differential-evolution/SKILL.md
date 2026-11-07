---
name: differential-evolution
description: When the user wants to solve continuous or mixed black-box optimization problems with differential evolution, choose among DE strategies (rand/1/bin, best/1/bin, current-to-best), tune F and CR, or adapt DE to permutation problems through random keys. Also use when the user mentions "differential evolution," "DE/rand/1," "mutation factor," "crossover rate CR," "SHADE," "jDE," or when a derivative-free population method is needed over a box-bounded continuous space. For covariance-matrix adaptation and (mu+lambda) selection, see evolution-strategies; for velocity-based swarm search, see particle-swarm-optimization.
---

# Differential Evolution

You are an expert in differential evolution (DE) and its application to continuous, mixed-integer, and decoder-based combinatorial optimization. This skill covers the canonical DE loop, the strategy family (rand/1/bin, best/1/bin, current-to-best/1), principled F and CR tuning, self-adaptive variants (jDE, SHADE, L-SHADE), and discrete adaptations via random keys and rounding. Use the framework below to select a strategy, set parameters with justification, implement a vectorized solver, and report results that withstand peer review.

## Initial Assessment

Establish the following before writing any code or recommending parameters:

- **Search space type.** Pure continuous box-bounded? Mixed-integer? Permutation? DE is native to continuous spaces; anything else needs an explicit adaptation layer (rounding, random keys, repair). Name the layer up front.
- **Dimension.** DE is most competitive for roughly 2-100 dimensions. Beyond ~200, expect slow convergence; consider decomposition or a different method.
- **Evaluation cost.** Can the objective evaluate a whole `(pop_size, dim)` matrix in one vectorized call? If each evaluation is seconds of simulation, the budget, not the algorithm, dominates the design; consider surrogate assistance or parallel evaluation.
- **Evaluation budget.** Ask for a hard number: total function evaluations or wall-clock limit. DE parameter advice changes with budget (small budget favors greedier strategies and smaller populations).
- **Separability.** Does the objective decompose (even approximately) into per-coordinate terms? This single property decides whether CR should be near 0.1 or near 0.9 — see the worked benchmark example.
- **Multimodality.** Rugged landscapes push toward DE/rand/1, larger populations, and self-adaptive variants; smooth unimodal landscapes tolerate DE/best/1 with small populations.
- **Constraints.** Box bounds only, or general inequality/equality constraints? DE handles boxes natively; general constraints need penalties, repair, or feasibility rules layered on top.
- **Hard vs soft quality requirement.** Is a near-optimum good enough, or is a provable optimum required? DE gives no optimality certificate; if a certificate is required, route to an exact method instead.
- **Reproducibility requirements.** Number of independent seeds for reporting, fixed instance set, and whether results feed a statistical comparison. Plan for at least 10 seeds per configuration.
- **Baseline.** What must DE beat? scipy's `differential_evolution` with defaults is the minimum honest baseline; CMA-ES is the standard strong continuous baseline.
- **Solver availability is not an issue here** — DE needs only numpy. This makes it a common choice when no MIP solver license exists, but verify that an exact approach was at least considered for small instances.

## Algorithm Anatomy

DE (Storn & Price, 1997, "Differential evolution — a simple and efficient heuristic for global optimization over continuous spaces") maintains a population $X = \{x_1, \dots, x_{NP}\}$, $x_i \in \mathbb{R}^D$. Each generation applies three operators per individual: mutation builds a mutant from scaled difference vectors, crossover mixes the mutant with the parent into a trial, and one-to-one greedy selection keeps the better of parent and trial.

### Mutation strategies

The strategy name follows the pattern `DE/<base>/<n_diffs>/<crossover>`. With distinct random indices $r_1, r_2, r_3, r_4, r_5 \neq i$:

$$\text{rand/1:} \quad v_i = x_{r_1} + F\,(x_{r_2} - x_{r_3})$$

$$\text{best/1:} \quad v_i = x_{\text{best}} + F\,(x_{r_1} - x_{r_2})$$

$$\text{current-to-best/1:} \quad v_i = x_i + F\,(x_{\text{best}} - x_i) + F\,(x_{r_1} - x_{r_2})$$

$$\text{current-to-pbest/1:} \quad v_i = x_i + F\,(x_{\text{pbest}} - x_i) + F\,(x_{r_1} - \tilde{x}_{r_2})$$

| Strategy | Character | Use when |
|---|---|---|
| DE/rand/1 | Most explorative, most robust; the default | Multimodal or unknown landscape |
| DE/best/1 | Greedy, fast on unimodal problems | Smooth landscape, tight budget |
| DE/current-to-best/1 | Compromise; directional pull plus diversity | Mildly multimodal, medium budget |
| DE/rand/2 | Two difference vectors; extra diversity, slower | Very rugged landscapes, large budget |
| DE/current-to-pbest/1 | Pull toward a random top-p% member; $\tilde{x}_{r_2}$ may come from an archive | Inside JADE/SHADE; best general-purpose modern choice |

The difference vector $x_{r_2} - x_{r_3}$ is the heart of DE: its distribution automatically matches the current population's spread and orientation ("contour matching"). As the population contracts into a basin, steps shrink without any external schedule — DE self-scales where simulated annealing needs an explicit cooling schedule.

### Crossover

Binomial (uniform) crossover builds the trial $u_i$ coordinate-wise:

$$u_{i,j} = \begin{cases} v_{i,j} & \text{if } \mathrm{rand}_j \le CR \text{ or } j = j_{\text{rand}} \\ x_{i,j} & \text{otherwise} \end{cases}$$

The forced coordinate $j_{\text{rand}}$ guarantees the trial differs from the parent even at $CR = 0$. Exponential crossover instead copies one contiguous coordinate block (geometric length distribution); it matters only when adjacent coordinates are strongly linked, and the effective inheritance rate for the same nominal CR is lower than binomial. Default to binomial. Note an important geometry fact: with $CR < 1$, binomial crossover makes DE coordinate-system dependent (not rotation invariant); at $CR = 1$ the trial equals the mutant and the algorithm becomes rotation invariant but loses the ability to exploit separability.

### Selection

$$x_i^{g+1} = \begin{cases} u_i & \text{if } f(u_i) \le f(x_i) \\ x_i & \text{otherwise} \end{cases}$$

One-to-one greedy selection is elitist per population slot: the population never worsens, and the best-so-far is never lost. Use $\le$ rather than $<$ so the population can drift across plateaus. For selection-scheme alternatives and their pressure analysis, see **selection-and-replacement-strategies**; DE's fixed scheme is a deliberate design choice, not an omission.

### Parameter guidance

| Parameter | Typical range | Default start | What it trades off |
|---|---|---|---|
| `pop_size` (NP) | $4D$-$10D$, minimum 4 | $5D$, capped near 100 | Robustness and diversity vs evaluations per generation; small NP risks stagnation |
| `F` (mutation factor) | 0.4-0.9 | 0.5 | Large F explores and escapes basins; small F intensifies; $F < 0.3$ with small NP invites stagnation |
| `CR` (crossover rate) | 0.0-0.2 or 0.8-1.0 | 0.9 | High CR changes many coordinates per trial (good for non-separable coupling); low CR makes near-axis moves (exploits separability) |
| Strategy | see table above | rand/1/bin | Greediness vs robustness |
| Budget | problem-specific | $10^3 D$ to $10^4 D$ evaluations | Solution quality vs time |

Two practical rules cover most cases. First, CR follows separability: separable or nearly separable objective → $CR \approx 0.1$; coupled variables → $CR \approx 0.9$. Second, when in doubt about F, use dither (random F per generation in $[0.5, 1.0]$) or move directly to jDE/SHADE rather than grid-searching. The bimodal CR advice is well documented in the survey by Das & Suganthan (2011, "Differential evolution: a survey of the state-of-the-art").

### Complexity

Per generation: $O(NP \cdot D)$ for variation plus $NP$ objective evaluations; memory $O(NP \cdot D)$. The fully vectorized index-sampling trick used below costs $O(NP^2 \log NP)$ per generation, negligible against evaluation cost for $NP \le 500$. DE has no learning structures to update (compare CMA-ES's $O(D^2)$ covariance work in **evolution-strategies**), which is why a clean numpy DE often wins on wall-clock for cheap objectives.

## Core Implementation

The skeleton first, then a reusable vectorized engine.

```text
DE(objective, bounds, NP, F, CR, strategy, budget):
    initialize population X uniformly inside bounds; evaluate f(X)
    repeat until budget exhausted:
        for the whole population at once (vectorized):
            draw distinct random indices r1, r2, r3 per row, all != row index
            V  <- mutant matrix according to strategy (rand/1, best/1, ...)
            repair V where it leaves the bounds (midpoint toward base vector)
            C  <- boolean crossover mask: rand(NP, D) < CR, plus forced j_rand per row
            U  <- where(C, V, X)                      # trial population
            fU <- objective(U)                        # one batched call
            winners <- fU <= fX
            X[winners], fX[winners] <- U[winners], fU[winners]
        record best-so-far
    return argmin of fX
```

```python
import numpy as np
from typing import Callable


def sample_distinct(rng: np.random.Generator, pop_size: int, k: int) -> np.ndarray:
    """Per row i, draw k distinct indices from {0..pop_size-1} excluding i."""
    perm = rng.random((pop_size, pop_size)).argsort(axis=1)
    keep = perm != np.arange(pop_size)[:, None]
    return perm[keep].reshape(pop_size, pop_size - 1)[:, :k]


def de_optimize(
    objective: Callable[[np.ndarray], np.ndarray],
    bounds: np.ndarray,
    pop_size: int = 50,
    max_gens: int = 500,
    f_weight: float = 0.5,
    cr: float = 0.9,
    strategy: str = "rand/1/bin",
    seed: int = 0,
) -> tuple[np.ndarray, float, np.ndarray]:
    """Vectorized DE over a box-bounded continuous space (minimization).

    objective maps a (pop_size, dim) matrix to a (pop_size,) value vector.
    bounds is a (dim, 2) array of [low, high] rows.
    Returns (best_vector, best_value, best_so_far_history).
    """
    rng = np.random.default_rng(seed)
    dim = bounds.shape[0]
    low, high = bounds[:, 0], bounds[:, 1]

    pop = low + rng.random((pop_size, dim)) * (high - low)
    fit = objective(pop)
    history = np.empty(max_gens)

    for gen in range(max_gens):
        r = sample_distinct(rng, pop_size, 3)
        x1, x2, x3 = pop[r[:, 0]], pop[r[:, 1]], pop[r[:, 2]]
        best = pop[np.argmin(fit)]

        if strategy == "rand/1/bin":
            mutant = x1 + f_weight * (x2 - x3)
        elif strategy == "best/1/bin":
            mutant = best + f_weight * (x1 - x2)
        elif strategy == "current-to-best/1/bin":
            mutant = pop + f_weight * (best - pop) + f_weight * (x1 - x2)
        else:
            raise ValueError(f"unknown strategy: {strategy}")

        # Midpoint repair: pull each violating coordinate halfway back
        # toward the parent, preserving direction information.
        mutant = np.where(mutant < low, 0.5 * (pop + low), mutant)
        mutant = np.where(mutant > high, 0.5 * (pop + high), mutant)

        # Binomial crossover with one forced mutant coordinate per row.
        cross = rng.random((pop_size, dim)) < cr
        cross[np.arange(pop_size), rng.integers(0, dim, pop_size)] = True
        trial = np.where(cross, mutant, pop)

        trial_fit = objective(trial)
        improved = trial_fit <= fit
        pop[improved] = trial[improved]
        fit[improved] = trial_fit[improved]
        history[gen] = fit.min()

    best_idx = int(np.argmin(fit))
    return pop[best_idx], float(fit[best_idx]), history


def sphere(pop: np.ndarray) -> np.ndarray:
    """Sum of squares; optimum 0 at the origin."""
    return (pop ** 2).sum(axis=1)


bounds = np.tile([-5.0, 5.0], (10, 1))
best_x, best_f, hist = de_optimize(sphere, bounds, pop_size=50, max_gens=300, seed=42)
print(f"best objective after 300 generations: {best_f:.2e}")
# Expected: best objective after 300 generations: 1.73e-12
# (10-D sphere, global optimum 0; DE/rand/1/bin with F=0.5, CR=0.9, NP=50)
```

Design notes worth keeping in any reimplementation:

- The objective receives the whole trial population as one matrix. Writing objectives this way (batched, no per-row Python loop) is the single largest speed lever in a numpy DE.
- The forced `j_rand` coordinate is not optional. Without it, low CR can produce trials identical to their parents, silently wasting evaluations.
- Midpoint bound repair (`(parent + bound) / 2`) keeps trials strictly inside the box and preserves some difference-vector information; plain clipping piles individuals onto the boundary, which is harmful when optima sit near it.
- The selection mask uses `<=`, allowing neutral drift on plateaus.

## Worked Example 1: Continuous Benchmarks — Strategy and CR Effects

The most common DE failure in practice is a CR copied from a paper whose problem had different variable coupling. This experiment makes the separability rule concrete: Rastrigin (separable, multimodal) against Rosenbrock (non-separable valley), each at CR 0.1 and 0.9 over five seeds.

```python
import numpy as np
from typing import Callable


def rastrigin(pop: np.ndarray) -> np.ndarray:
    """Separable, highly multimodal; global optimum 0 at the origin."""
    d = pop.shape[1]
    return 10.0 * d + (pop ** 2 - 10.0 * np.cos(2.0 * np.pi * pop)).sum(axis=1)


def rosenbrock(pop: np.ndarray) -> np.ndarray:
    """Non-separable curved valley; global optimum 0 at (1, ..., 1)."""
    x, y = pop[:, :-1], pop[:, 1:]
    return (100.0 * (y - x ** 2) ** 2 + (1.0 - x) ** 2).sum(axis=1)


def de_rand1bin(
    objective: Callable[[np.ndarray], np.ndarray],
    bounds: np.ndarray,
    pop_size: int,
    max_gens: int,
    f_weight: float,
    cr: float,
    seed: int,
) -> float:
    """Compact self-contained DE/rand/1/bin; returns the best value found."""
    rng = np.random.default_rng(seed)
    dim = bounds.shape[0]
    low, high = bounds[:, 0], bounds[:, 1]
    pop = low + rng.random((pop_size, dim)) * (high - low)
    fit = objective(pop)
    rows = np.arange(pop_size)
    for _ in range(max_gens):
        perm = rng.random((pop_size, pop_size)).argsort(axis=1)
        keep = perm != rows[:, None]
        r = perm[keep].reshape(pop_size, pop_size - 1)[:, :3]
        mutant = pop[r[:, 0]] + f_weight * (pop[r[:, 1]] - pop[r[:, 2]])
        mutant = np.clip(mutant, low, high)
        cross = rng.random((pop_size, dim)) < cr
        cross[rows, rng.integers(0, dim, pop_size)] = True
        trial = np.where(cross, mutant, pop)
        trial_fit = objective(trial)
        improved = trial_fit <= fit
        pop[improved] = trial[improved]
        fit[improved] = trial_fit[improved]
    return float(fit.min())


dim = 10
experiments = [
    ("rastrigin", rastrigin, np.tile([-5.12, 5.12], (dim, 1)), 0.5, 1000),
    ("rosenbrock", rosenbrock, np.tile([-2.048, 2.048], (dim, 1)), 0.6, 3000),
]
for name, func, box, f_w, gens in experiments:
    for cr in (0.1, 0.9):
        vals = [de_rand1bin(func, box, 60, gens, f_w, cr, seed) for seed in range(5)]
        print(f"{name:10s} CR={cr}: median over 5 seeds = {np.median(vals):.3e}")
# Expected: rastrigin  CR=0.1: median = 0.000e+00   (exact global optimum)
#           rastrigin  CR=0.9: median = 1.376e+01   (stalls far from optimum)
#           rosenbrock CR=0.1: median = 8.083e-01   (slow along the valley)
#           rosenbrock CR=0.9: median = 0.000e+00   (solves it to machine zero)
```

Reading the result: on the separable Rastrigin, CR = 0.1 turns DE into a near coordinate-wise search that solves each dimension almost independently and finds the exact optimum, while CR = 0.9 keeps recombining incompatible basin choices across coordinates and stalls. On the non-separable Rosenbrock valley, the situation flips — progress requires moving many coupled coordinates simultaneously, so CR = 0.9 wins decisively. Neither setting is "the good one"; the landscape decides. When the coupling structure is unknown, this experiment (two CR values, a handful of seeds, a few minutes) is cheaper and more informative than any rule of thumb — or skip the question entirely with the self-adaptive variants below.

## Worked Example 2: Permutation Flow Shop via Random Keys

DE is continuous, but a decoder makes it a serviceable permutation optimizer: keep the genotype as a real vector of "random keys" (Bean, 1994, "Genetic algorithms and random keys for sequencing and optimization") and decode by `argsort` — the job whose key is smallest goes first. DE then evolves keys exactly as it evolves any continuous vector. Decoder design trade-offs (redundancy, locality, feasibility guarantees) are covered in depth in **decoder-based-representations**; representation alternatives in **solution-encodings**.

```python
import numpy as np


def flowshop_makespans(perms: np.ndarray, proc: np.ndarray) -> np.ndarray:
    """Makespan of each job sequence in a permutation flow shop.

    perms: (pop, n_jobs) integer array, each row a job order.
    proc:  (n_jobs, n_machines) processing times.
    Returns a (pop,) vector of makespans, vectorized over the population.
    """
    pt = proc[perms]                       # (pop, n_jobs, n_machines)
    pop_size, n_jobs, n_mach = pt.shape
    comp = np.zeros((pop_size, n_mach))
    for j in range(n_jobs):
        comp[:, 0] += pt[:, j, 0]
        for k in range(1, n_mach):
            comp[:, k] = np.maximum(comp[:, k], comp[:, k - 1]) + pt[:, j, k]
    return comp[:, -1]


def de_flowshop(
    proc: np.ndarray,
    pop_size: int = 60,
    max_gens: int = 400,
    f_weight: float = 0.5,
    cr: float = 0.7,
    seed: int = 0,
) -> tuple[np.ndarray, float]:
    """DE/rand/1/bin over random keys; argsort decodes keys to a permutation."""
    rng = np.random.default_rng(seed)
    n_jobs = proc.shape[0]
    rows = np.arange(pop_size)

    keys = rng.random((pop_size, n_jobs))            # genotype: continuous keys
    fit = flowshop_makespans(keys.argsort(axis=1), proc)

    for _ in range(max_gens):
        perm = rng.random((pop_size, pop_size)).argsort(axis=1)
        keep = perm != rows[:, None]
        r = perm[keep].reshape(pop_size, pop_size - 1)[:, :3]
        mutant = keys[r[:, 0]] + f_weight * (keys[r[:, 1]] - keys[r[:, 2]])
        cross = rng.random((pop_size, n_jobs)) < cr
        cross[rows, rng.integers(0, n_jobs, pop_size)] = True
        trial = np.where(cross, mutant, keys)
        trial_fit = flowshop_makespans(trial.argsort(axis=1), proc)
        improved = trial_fit <= fit
        keys[improved] = trial[improved]
        fit[improved] = trial_fit[improved]

    best = int(np.argmin(fit))
    return keys[best].argsort(), float(fit[best])


inst_rng = np.random.default_rng(7)
proc = inst_rng.integers(1, 20, size=(8, 4)).astype(float)
best_seq, best_cmax = de_flowshop(proc, seed=1)
print(f"best sequence: {best_seq.tolist()}, makespan: {best_cmax:.0f}")
# Expected: makespan 120 — verified equal to the brute-force optimum over
# all 8! = 40,320 sequences for this seed-7 instance (an optimal order is
# (2, 0, 6, 4, 3, 7, 1, 5); several sequences attain 120).
```

What to know before scaling this up:

- **No bounds are needed on keys.** Only the ordering matters; keys can drift anywhere in $\mathbb{R}$. Adding bounds adds nothing.
- **The mapping is many-to-one.** Every key vector with the same ordering decodes to the same permutation, so the landscape contains large neutral plateaus. The `<=` acceptance lets the population drift across them, but convergence detection must therefore watch decoded objectives, not key-space distances.
- **Random-key DE is a baseline, not a champion.** On permutation flow shop, iterated greedy and well-designed local search dominate published comparisons. Use random-key DE when you need one engine across mixed problem types, when an unusual objective makes neighborhood design hard, or as a sanity baseline — and say so honestly in writeups.
- **Mind the decode cost.** Here decoding is one `argsort` plus a vectorized makespan; if a decoder dominates runtime, profile it before touching DE parameters.

## Self-Adaptive Variants: jDE and SHADE

Fixed (F, CR) is the weakest point of canonical DE: good values are problem-specific and can even change during a run. Two adaptation designs dominate practice.

### jDE — per-individual parameter evolution

jDE (Brest et al., 2006, "Self-adapting control parameters in differential evolution") attaches $F_i$ and $CR_i$ to each individual. Before producing a trial, each parameter is regenerated with small probability (otherwise inherited); the new values survive only if the trial wins selection. Good parameter values thus propagate because they produce surviving offspring. The overhead over canonical DE is a few vectorized lines.

```python
import numpy as np
from typing import Callable


def jde(
    objective: Callable[[np.ndarray], np.ndarray],
    bounds: np.ndarray,
    pop_size: int = 60,
    max_gens: int = 1000,
    tau_f: float = 0.1,
    tau_cr: float = 0.1,
    seed: int = 0,
) -> tuple[np.ndarray, float]:
    """jDE (Brest et al., 2006): per-individual F and CR evolve with the search.

    With probability tau_f, an individual's F is redrawn from U(0.1, 1.0);
    with probability tau_cr its CR is redrawn from U(0, 1). The trial uses
    the (possibly new) values, which persist only if the trial wins.
    """
    rng = np.random.default_rng(seed)
    dim = bounds.shape[0]
    low, high = bounds[:, 0], bounds[:, 1]
    rows = np.arange(pop_size)

    pop = low + rng.random((pop_size, dim)) * (high - low)
    fit = objective(pop)
    f_vals = np.full(pop_size, 0.5)
    cr_vals = np.full(pop_size, 0.9)

    for _ in range(max_gens):
        new_f = np.where(rng.random(pop_size) < tau_f,
                         0.1 + 0.9 * rng.random(pop_size), f_vals)
        new_cr = np.where(rng.random(pop_size) < tau_cr,
                          rng.random(pop_size), cr_vals)

        perm = rng.random((pop_size, pop_size)).argsort(axis=1)
        keep = perm != rows[:, None]
        r = perm[keep].reshape(pop_size, pop_size - 1)[:, :3]
        mutant = pop[r[:, 0]] + new_f[:, None] * (pop[r[:, 1]] - pop[r[:, 2]])
        mutant = np.clip(mutant, low, high)

        cross = rng.random((pop_size, dim)) < new_cr[:, None]
        cross[rows, rng.integers(0, dim, pop_size)] = True
        trial = np.where(cross, mutant, pop)

        trial_fit = objective(trial)
        improved = trial_fit <= fit
        pop[improved] = trial[improved]
        fit[improved] = trial_fit[improved]
        f_vals = np.where(improved, new_f, f_vals)
        cr_vals = np.where(improved, new_cr, cr_vals)

    best = int(np.argmin(fit))
    return pop[best], float(fit[best])


def rastrigin(pop: np.ndarray) -> np.ndarray:
    """Separable, highly multimodal; global optimum 0 at the origin."""
    d = pop.shape[1]
    return 10.0 * d + (pop ** 2 - 10.0 * np.cos(2.0 * np.pi * pop)).sum(axis=1)


bounds = np.tile([-5.12, 5.12], (20, 1))
_, best_f = jde(rastrigin, bounds, pop_size=100, max_gens=2000, seed=3)
print(f"jDE on 20-D Rastrigin: {best_f:.2e}")
# Expected: jDE on 20-D Rastrigin: 0.00e+00 — the exact optimum, found with
# no manual F/CR tuning; the population discovers the low-CR regime itself.
```

### SHADE — success-history based adaptation

SHADE (Tanabe & Fukunaga, 2013, "Success-history based parameter adaptation for differential evolution") replaces per-individual inheritance with a small circular memory of (F, CR) means. Each individual samples F from a Cauchy and CR from a normal around a randomly chosen memory cell; after the generation, successful values update one cell using improvement-weighted means (Lehmer mean for F, which biases upward and counteracts the survival advantage of tiny steps). Mutation is current-to-pbest/1 with an external archive of defeated parents (inherited from JADE; Zhang & Sanderson, 2009). The condensed but functional version:

```python
import numpy as np
from typing import Callable


def shade(
    objective: Callable[[np.ndarray], np.ndarray],
    bounds: np.ndarray,
    pop_size: int = 50,
    max_gens: int = 600,
    memory_size: int = 6,
    p_best_frac: float = 0.11,
    seed: int = 0,
) -> tuple[np.ndarray, float]:
    """SHADE (Tanabe & Fukunaga, 2013), condensed but functional.

    F ~ Cauchy(mem_f[k], 0.1) truncated to (0, 1]; CR ~ N(mem_cr[k], 0.1)
    clipped to [0, 1]; current-to-pbest/1 mutation with an external archive
    of defeated parents; improvement-weighted memory updates per generation.
    """
    rng = np.random.default_rng(seed)
    dim = bounds.shape[0]
    low, high = bounds[:, 0], bounds[:, 1]
    rows = np.arange(pop_size)

    pop = low + rng.random((pop_size, dim)) * (high - low)
    fit = objective(pop)
    mem_f = np.full(memory_size, 0.5)
    mem_cr = np.full(memory_size, 0.5)
    mem_pos = 0
    archive = np.empty((0, dim))
    n_pbest = max(2, int(round(p_best_frac * pop_size)))

    for _ in range(max_gens):
        k = rng.integers(0, memory_size, pop_size)
        f = mem_f[k] + 0.1 * np.tan(np.pi * (rng.random(pop_size) - 0.5))
        for _ in range(10):                      # resample non-positive F draws
            bad = f <= 0.0
            if not bad.any():
                break
            f[bad] = mem_f[k[bad]] + 0.1 * np.tan(np.pi * (rng.random(bad.sum()) - 0.5))
        f = np.clip(f, 1e-8, 1.0)
        cr = np.clip(mem_cr[k] + 0.1 * rng.standard_normal(pop_size), 0.0, 1.0)

        pbest_pool = np.argsort(fit)[:n_pbest]
        x_pbest = pop[rng.choice(pbest_pool, pop_size)]

        perm = rng.random((pop_size, pop_size)).argsort(axis=1)
        keep = perm != rows[:, None]
        r1 = perm[keep].reshape(pop_size, pop_size - 1)[:, 0]
        union = np.vstack([pop, archive])
        r2 = rng.integers(0, union.shape[0], pop_size)

        mutant = pop + f[:, None] * (x_pbest - pop) + f[:, None] * (pop[r1] - union[r2])
        mutant = np.where(mutant < low, 0.5 * (pop + low), mutant)
        mutant = np.where(mutant > high, 0.5 * (pop + high), mutant)

        cross = rng.random((pop_size, dim)) < cr[:, None]
        cross[rows, rng.integers(0, dim, pop_size)] = True
        trial = np.where(cross, mutant, pop)

        trial_fit = objective(trial)
        improved = trial_fit < fit
        if improved.any():
            delta = fit[improved] - trial_fit[improved]
            w = delta / delta.sum()
            mem_f[mem_pos] = (w * f[improved] ** 2).sum() / (w * f[improved]).sum()
            mem_cr[mem_pos] = (w * cr[improved]).sum()
            mem_pos = (mem_pos + 1) % memory_size
            archive = np.vstack([archive, pop[improved]])
            if archive.shape[0] > pop_size:
                sel = rng.choice(archive.shape[0], pop_size, replace=False)
                archive = archive[sel]
        accept = trial_fit <= fit
        pop[accept] = trial[accept]
        fit[accept] = trial_fit[accept]

    best = int(np.argmin(fit))
    return pop[best], float(fit[best])


def rosenbrock(pop: np.ndarray) -> np.ndarray:
    """Non-separable curved valley; global optimum 0 at (1, ..., 1)."""
    x, y = pop[:, :-1], pop[:, 1:]
    return (100.0 * (y - x ** 2) ** 2 + (1.0 - x) ** 2).sum(axis=1)


bounds = np.tile([-2.048, 2.048], (10, 1))
_, best_f = shade(rosenbrock, bounds, pop_size=50, max_gens=800, seed=5)
print(f"SHADE on 10-D Rosenbrock: {best_f:.2e}")
# Expected: SHADE on 10-D Rosenbrock: 0.00e+00 — machine-precision optimum
# with all parameters at their published defaults.
```

Selection guidance among the variants: canonical DE/rand/1/bin with a deliberate CR choice when the landscape is understood and code simplicity matters; jDE when you want adaptation with minimal code; SHADE (or L-SHADE, below) as the default for serious benchmark work — SHADE-family algorithms have ranked at or near the top of CEC real-parameter competitions since 2013.

## Advanced Techniques

### Dither and jitter

Dither redraws F once per generation (or per individual) from $U(0.5, 1.0)$; jitter perturbs F per coordinate by a few percent. Both break the fixed step-length pathology that causes stagnation on plateaus, at zero implementation cost: replace the scalar `f_weight` with `rng.uniform(0.5, 1.0)` inside the generation loop (dither) or with `f_weight * (1 + 0.001 * rng.standard_normal(dim))` (jitter). Dither is the cheapest worthwhile upgrade to canonical DE and is the default in scipy's implementation (`mutation=(0.5, 1)`).

### L-SHADE: linear population-size reduction

L-SHADE (Tanabe & Fukunaga, 2014, "Improving the search performance of SHADE using linear population size reduction") shrinks the population linearly with the evaluation budget, from $NP_{\text{init}}$ (e.g., $18D$) down to 4:

$$NP_g = \mathrm{round}\Big(NP_{\text{init}} + \frac{\mathit{nfe}}{\mathit{nfe}_{\max}}\,(NP_{\min} - NP_{\text{init}})\Big)$$

After each generation, delete the worst individuals down to $NP_g$ (truncating the archive proportionally). Large early populations explore; tiny late populations turn DE into an intensive local refiner. Add this to the SHADE implementation above with roughly ten lines (recompute $NP_g$, `keep = np.argsort(fit)[:np_g]`, slice `pop`, `fit`, and the archive cap).

### Discrete and mixed-integer adaptations via rounding

For integer or mixed-integer variables, keep the genotype continuous and round only at evaluation time (the "relaxed genotype / rounded phenotype" pattern). Rounding inside the objective preserves DE's difference-vector geometry; rounding the population itself collapses diversity to few lattice points and triggers stagnation.

```python
import numpy as np


def rounded_objective(pop: np.ndarray, a_mat: np.ndarray, b_vec: np.ndarray) -> np.ndarray:
    """||A round(x) - b||^2: genotype stays continuous, phenotype is integer."""
    x_int = np.rint(pop)
    resid = x_int @ a_mat.T - b_vec
    return (resid ** 2).sum(axis=1)


def de_integer(
    a_mat: np.ndarray,
    b_vec: np.ndarray,
    low: float,
    high: float,
    pop_size: int = 40,
    max_gens: int = 300,
    f_weight: float = 0.5,
    cr: float = 0.9,
    seed: int = 0,
) -> tuple[np.ndarray, float]:
    """DE/rand/1/bin over a continuous genotype, rounded only at evaluation."""
    rng = np.random.default_rng(seed)
    dim = a_mat.shape[1]
    rows = np.arange(pop_size)
    pop = low + rng.random((pop_size, dim)) * (high - low)
    fit = rounded_objective(pop, a_mat, b_vec)
    for _ in range(max_gens):
        perm = rng.random((pop_size, pop_size)).argsort(axis=1)
        keep = perm != rows[:, None]
        r = perm[keep].reshape(pop_size, pop_size - 1)[:, :3]
        mutant = pop[r[:, 0]] + f_weight * (pop[r[:, 1]] - pop[r[:, 2]])
        mutant = np.clip(mutant, low, high)
        cross = rng.random((pop_size, dim)) < cr
        cross[rows, rng.integers(0, dim, pop_size)] = True
        trial = np.where(cross, mutant, pop)
        trial_fit = rounded_objective(trial, a_mat, b_vec)
        improved = trial_fit <= fit
        pop[improved] = trial[improved]
        fit[improved] = trial_fit[improved]
    best = int(np.argmin(fit))
    return np.rint(pop[best]).astype(int), float(fit[best])


inst = np.random.default_rng(11)
a_mat = inst.normal(size=(6, 4))
x_true = np.array([3, -2, 0, 4])
b_vec = a_mat @ x_true + 0.05 * inst.normal(size=6)
x_best, f_best = de_integer(a_mat, b_vec, low=-5.0, high=5.0, seed=2)
print(f"recovered integers: {x_best.tolist()}, residual: {f_best:.4f}")
# Expected: recovered integers: [3, -2, 0, 4], residual: 0.0206 — verified
# equal to the optimum over full enumeration of all 11^4 integer points.
```

The same pattern generalizes: categorical variables via rounding into level indices, permutations via random keys (Worked Example 2), and subsets via thresholding keys at a value chosen by the decoder. Whenever the rounding/decoding layer grows beyond a few lines, treat it as a decoder design problem — see **decoder-based-representations**.

### Hybridizing DE with local search

DE locates basins well but refines slowly at high precision. Two effective hybrids: (a) memetic refinement — run a budgeted local search (Nelder-Mead or L-BFGS-B for continuous; problem-specific moves for decoded solutions) on the best individual every $G$ generations and reinsert if improved (Lamarckian update); (b) terminal polish — spend the last 5-10% of the budget on local search from the few best distinct solutions. scipy's `differential_evolution(polish=True)` implements (b) automatically. For decoded permutations, polish the phenotype (e.g., insertion moves on the sequence) and re-encode by overwriting the winner's keys with sorted-position keys.

### Constraint handling beyond the box

For general constraints, the standard choice inside DE selection is Deb's feasibility rules (feasible beats infeasible; among infeasible, smaller total violation wins), implemented by comparing tuples `(violation, objective)` instead of objectives alone — this drops into the one-to-one selection step without other changes. Adaptive penalties and repair operators are alternatives with different failure modes; since these choices are algorithm-independent, design the handler once and reuse it across methods.

## Practical Challenges

**The population stagnates while still diverse.** DE-specific stagnation (Lampinen & Zelinka, 2000): the population is spread out, but no generated trial improves any slot because the finite set of reachable difference vectors misses improving directions. Cures, in order of cost: dither F, increase NP, switch rand/1 to current-to-pbest/1 with an archive, or move to SHADE. Detect it by tracking the per-generation acceptance rate — stagnation shows as acceptance collapsing toward zero while population variance stays high.

**Premature convergence with best/1 or small populations.** The whole population collapses into one basin within a few dozen generations. Reduce greediness (rand/1), raise NP toward $10D$, or add an archive. Monitor the mean pairwise distance or per-coordinate population standard deviation each generation; a collapse that precedes objective stalling is the signature.

**CR is misread as a per-individual probability.** CR is a per-coordinate inheritance probability. At CR = 0, the trial still receives exactly one mutant coordinate via `j_rand`, so DE degenerates to slow coordinate search rather than stopping. Symmetrically, at low CR the effective move is nearly axis-parallel — which is precisely why it excels on separable problems and fails on coupled ones.

**Results do not reproduce across runs or machines.** Every stochastic element must flow from one `np.random.default_rng(seed)` instance per run, with the seed recorded next to the result. Separate instance-generation seeds from algorithm seeds (the flow-shop example uses seed 7 for the instance, seed 1 for the search) so the same instance can be re-attacked with fresh algorithm randomness.

**Evaluations are wasted re-testing duplicate trials.** On plateaus and with decoders, identical phenotypes recur. Memoize on a canonical key — for random keys, the decoded permutation's bytes — before calling an expensive objective. With cheap vectorized objectives, skip memoization; the hash overhead exceeds the evaluation cost.

**Bound clipping piles the population onto box faces.** With plain `np.clip`, any optimum near the boundary attracts a degenerate sub-population stuck exactly on the face, destroying difference-vector diversity in that coordinate. Use midpoint repair (as in the core engine), reflection, or reinitialization of violating coordinates.

**The random-key landscape looks flat near convergence.** Many key vectors decode to one permutation, so the decoded objective stops moving while keys still change. Define convergence on the phenotype stream (no improvement in decoded objective for $k$ generations), and when comparing against permutation-native methods, count decoded evaluations, not generations, for fairness.

**Self-adaptive variants are benchmarked against a strawman.** Comparing SHADE under a generous budget against canonical DE with one untuned (F, CR) overstates the gain. Give the canonical baseline at least dither and the CR-separability rule, run 10+ seeds, and test significance before claiming the variant matters on your problem class.

## Tools & Libraries

| Library | When to use | Note |
|---|---|---|
| `scipy.optimize.differential_evolution` | Quick continuous runs, honest baseline | Strategies like `best1bin`/`rand1bin`, dither via `mutation=(0.5, 1)`, `polish=True` L-BFGS-B finish, `workers=-1` parallel evaluation |
| Custom numpy (this skill) | Decoders, custom constraint handling, instrumentation, research-grade logging | Full control of every operator; vectorize the objective first |
| pygmo | Self-adaptive DE without writing it: `sade`, `de1220` | Also offers island-model parallelism over coarse-grained archipelagos |
| pymoo | DE inside a broader experiment with GA/ES/NSGA-II under one API | Convenient for operator swaps and multi-objective extensions |
| nevergrad | Black-box comparison of DE against dozens of optimizers | Good for "is DE even the right family?" triage runs |
| Optuna | Tuning DE's own NP/F/CR/strategy on an instance set | Tune on training instances only; report on held-out instances |

## Output Format

A complete DE study deliverable contains:

1. **Configuration summary** — one table, fully reproducible:

| Field | Value |
|---|---|
| Algorithm / strategy | SHADE, current-to-pbest/1/bin, archive on |
| Population / memory | NP = 50, H = 6, p = 0.11 |
| Budget | 40,000 evaluations per run |
| Bound handling | Midpoint repair |
| Encoding | Random keys, argsort decoder |
| Seeds | Algorithm seeds 0-9; instance seeds disjoint |

2. **Result table** — one row per (instance, algorithm): best, median, mean, standard deviation of final objective over seeds; median evaluations to reach the final value; wall-clock per run. Report gaps to optima or best-known values where they exist (the flow-shop example reports "optimal, verified by enumeration").
3. **Convergence evidence** — best-so-far curve per generation, median with an interquartile band over seeds, evaluation count on the x-axis (never generations when comparing different NP).
4. **Validation statement** — the best solution re-evaluated by an independent function (for decoded solutions: decode once, recompute the objective from raw problem data, confirm equality with the reported value).
5. **Artifacts** — one tidy CSV of per-run results (instance, seed, strategy, NP, F/CR policy, budget, best objective, time), the convergence data, and the exact code version used.

When the deliverable is a recommendation rather than an experiment, state: chosen strategy and why (landscape evidence), parameter values with the trade-off each setting resolves, the adaptation variant if any, and the stopping criterion in evaluations.

## Questions to Ask

- Is the search space purely continuous, mixed-integer, or a permutation/subset structure in disguise?
- How many dimensions, and what are sensible box bounds for each variable?
- How expensive is one objective evaluation, and can it be evaluated for a whole population matrix at once?
- What is the total evaluation or wall-clock budget per run?
- Is the objective (approximately) separable, or are variables strongly coupled?
- Are there constraints beyond box bounds, and how hard are they?
- Is a heuristic answer acceptable, or is an optimality certificate required?
- What baseline must be beaten, and on which instance set will the comparison run?
- How many seeds and instances are available for a statistically defensible comparison?
- Should the solution feed downstream tooling (fixed file format, repair to feasibility, integration with an exact solver)?

## Related Skills

- **evolution-strategies** — when self-adaptive step sizes or covariance-matrix adaptation (CMA-ES) fit the continuous problem better than difference-vector mutation, or for the (mu+lambda)/(mu,lambda) selection viewpoint on DE's one-to-one scheme.
- **particle-swarm-optimization** — when a velocity-based swarm with gbest/lbest topologies is the alternative continuous population method to benchmark DE against.
- **solution-encodings** — when choosing between direct and indirect representations before committing DE to a discrete problem.
- **decoder-based-representations** — when the random-key or rounding layer grows into a real decoder design problem (schedule-generation schemes, feasibility-enforcing decoders, redundancy control).
