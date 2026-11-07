---
name: nature-inspired-metaheuristics-overview
description: When the user needs a critical, operator-level assessment of metaphor-based metaheuristics — what harmony search, cuckoo search, firefly, grey wolf, whale, or bat algorithms actually compute, and when to just use an established method. Also use when the user mentions "harmony search," "cuckoo search," "firefly algorithm," "grey wolf optimizer," "novel metaheuristic," "metaphor-based," or asks whether a newly published nature-inspired algorithm is worth adopting. For designing a method from proven components, see metaheuristic-design-principles; for sound empirical comparison, see algorithm-benchmarking-statistics.
---

# Nature-Inspired Metaheuristics: A Critical Overview

You are an expert in metaheuristic optimization and its literature. This skill covers the metaphor-based algorithm family — harmony search, cuckoo search, firefly, grey wolf, whale, bat, and their hundreds of relatives — from a mechanism-first point of view: what each method actually computes, which classic algorithm it restates, and how to test any "novel" method fairly against established baselines. Use the framework below to translate metaphors into operators, audit claimed results, and decide when to simply use a proven method.

## Initial Assessment

Establish these points before answering:

- **Why the question is being asked.** Four cases need different answers: (1) the user wants to *adopt* a metaphor algorithm for a real problem; (2) a *reviewer, supervisor, or client* demands a comparison against one; (3) the user must *peer-review* a paper proposing or using one; (4) the user wants to *reproduce* published results. Identify the case explicitly.
- **Problem class.** Metaphor algorithms are almost all defined on continuous box-constrained vectors. If the user's problem is combinatorial, the algorithm needs an encoding or decoder layer, and the comparison set changes (ILS, tabu search, simulated annealing, ALNS become the relevant baselines).
- **Which algorithm, which variant.** "Grey wolf optimizer" alone is ambiguous: dozens of modified GWO variants exist with different update equations. Pin down the exact paper and equations before any analysis.
- **Whether a documented critique already exists.** For harmony search, cuckoo search, firefly, grey wolf, whale, bat, intelligent water drops, and several others, rigorous analyses already exist (see the mapping table below). Do not redo work the literature has settled.
- **Evaluation budget and dimension.** Claims about metaphor algorithms are extremely sensitive to budget, dimension, and benchmark choice. Get concrete numbers before judging any reported result.
- **Benchmark provenance.** Ask whether the reported results were obtained on unshifted, zero-centered test functions (classic sphere, Rastrigin, Ackley with optimum at the origin). Many metaphor algorithms carry a structural pull toward the center of the search domain, which inflates results on exactly those functions.
- **Tuning parity.** Were the baselines (DE, PSO, CMA-ES, GA) run with default 1990s parameters while the proposed method was tuned? This asymmetry is the most common flaw in metaphor-algorithm papers.
- **Statistical evidence.** How many independent seeds, which paired test, what effect size? "Mean over 30 runs, bold best value" is not evidence of superiority.
- **Code availability.** Whether reference code exists, and whether the user must reimplement from (often ambiguous) pseudocode.
- **Venue constraints.** The Journal of Heuristics explicitly requires metaphor-based methods to be described in standard optimization terminology; several other journals have followed. Application venues, in contrast, often expect a named nature-inspired method. This affects what the deliverable must look like.
- **The actual deliverable.** An algorithm recommendation, a fair-comparison experiment, a referee report, or a rebuttal each call for a different subset of this skill.

## Metaphor-to-Mechanism Mapping

Since roughly 2000, the field has produced hundreds of "novel" metaheuristics named after animals, physical processes, and human activities; the Evolutionary Computation Bestiary (Campelo & Aranha) catalogues well over 300. The foundational critique is Sörensen (2015), "Metaheuristics — the metaphor exposed" (International Transactions in Operational Research): most of these methods introduce no new mechanism, only new vocabulary for components that evolutionary computation and swarm intelligence defined decades earlier. Aranha et al. (2022), "Metaphor-based metaheuristics, a call for action" (Swarm Intelligence), turned this into concrete editorial recommendations. A readable component-level translation of many recent methods is Lones (2020), "Mitigating metaphors" (SN Computer Science).

Stripped of vocabulary, nearly every metaphor algorithm is an instance of one generic loop:

$$
x_i^{t+1} \;=\; \underbrace{\text{recombine}\big(x_i^t,\ \text{elite attractors}\big)}_{\text{"social" / "swarm" step}} \;+\; \underbrace{\sigma(t)\,\xi_i^t}_{\text{scheduled perturbation}}
$$

followed by some replacement rule (generational, replace-worst, or accept-if-better). The metaphor names the parts; the mechanics are recombination toward elites plus mutation with a step-size schedule. Selection, replacement, and mutation design are exactly the classic topics — see **selection-and-replacement-strategies** and **mutation-and-perturbation-operators** for the component catalogs rather than re-deriving them per metaphor.

### The mapping table

| Algorithm (source) | Metaphor vocabulary | Actual mechanism | Closest classic method | Documented critique |
|---|---|---|---|---|
| Harmony search (Geem, Kim & Loganathan 2001) | improvisation, harmony memory, pitch adjustment | per-gene uniform recombination over the population + creep/reset mutation, replace-worst | (μ+1) evolution strategy | Weyland (2010, 2015): HS is a special case of ES |
| Cuckoo search (Yang & Deb 2009) | nests, eggs, brood parasitism, abandonment | global random walk with heavy-tailed (Lévy) mutation + partial population restart | (μ+λ) ES with Lévy mutation | Camacho-Villalón, Stützle & Dorigo (2021): cuckoo search ≡ (μ+λ)-ES |
| Firefly algorithm (Yang 2009) | brightness, attractiveness, light absorption | each solution steps toward every better solution with distance-decaying weight, plus decaying uniform noise | memory-less multi-attractor PSO variant, O(n²d) per iteration | Camacho-Villalón, Dorigo & Stützle (2023) |
| Grey wolf optimizer (Mirjalili, Mirjalili & Lewis 2014) | alpha/beta/delta hierarchy, encircling prey | average of three randomized contractions toward the three best; single linear step-size schedule | leader-guided random walk (PSO family) | Camacho-Villalón et al. (2023); Niu et al. (2019): structural origin bias |
| Whale optimization (Mirjalili & Lewis 2016) | bubble-net feeding, spiral | mix of GWO-style contraction toward the best, a logarithmic-spiral move around the best, and a random-member walk | leader-guided random walk (PSO family) | Camacho-Villalón et al. (2023) |
| Bat algorithm (Yang 2010) | echolocation, loudness, pulse rate | PSO velocity update toward the global best + occasional local random walk around the best, gated by SA-like acceptance | PSO variant with extra parameters | Camacho-Villalón et al. (2023) |
| Intelligent water drops (Shah-Hosseini 2007) | rivers, soil, velocity | constructive solution building with shared "soil" memory on components | special case of Ant Colony Optimization | Camacho-Villalón, Dorigo & Stützle (2019) |

The pattern generalizes: when a new "X optimization algorithm" appears, translate its update equations into operator language (attractors, recombination, mutation distribution, schedule, replacement) and locate it in this table's columns. In almost all cases it lands on PSO, DE, ES, GA, or ACO with renamed parts — see **particle-swarm-optimization** and **differential-evolution** for the canonical versions of the two most common landing spots.

### Decision guidance

- **Default: use an established method.** For continuous black-box problems, CMA-ES and DE (plus PSO as a cheap alternative) dominate metaphor algorithms in well-controlled studies and have convergence analyses, tuned defaults, and mature implementations. For combinatorial problems, use the method families with real track records (ILS, SA, tabu, ALNS, GA/memetic) chosen via **metaheuristic-design-principles**.
- **Engage with a metaphor algorithm when** (a) you must reproduce or review published work; (b) a credible study in your application domain used one and you need comparability; (c) you are mining it for a genuinely reusable component (the only widely accepted example: Lévy-flight mutation popularized by cuckoo search).
- **Never accept "novel therefore better".** The no-free-lunch theorem (Wolpert & Macready 1997) is frequently cited in these papers to justify new methods; it actually says nothing about a new metaphor outperforming tuned classics on a structured problem class.
- **Complexity notes.** Firefly is O(n²d) per iteration versus O(nd) for DE/PSO/GWO — it pays a full pairwise-distance matrix every generation. None of the six algorithms above has a convergence proof comparable to (1+1)-ES theory or CMA-ES invariance results; most have no principled parameter semantics, so tuning advice transfers poorly between papers.

## One Skeleton, Many Metaphors

The fastest way to demystify this family is to implement the shared loop once and express individual "algorithms" as small move rules. The skeleton below covers GWO, WOA, firefly, bat, and most of their descendants.

```text
ATTRACTOR-SEARCH SKELETON  (covers GWO, WOA, firefly, bat, and most relatives)
1. Sample an initial population uniformly in the box; evaluate it.
2. Repeat until the evaluation budget is spent:
   a. Choose attractors: the best solution, the k best, or all better ones.
   b. Move every solution toward its attractors with randomized coefficients;
      a global schedule shrinks step sizes over time.
   c. Add a perturbation (uniform, Gaussian, or heavy-tailed noise).
   d. Evaluate the moved population; apply the replacement rule.
3. Return the best solution seen.
The metaphor renames steps (a)-(c); selection and replacement variants are the
classic ES/GA components.
```

```python
import numpy as np
from typing import Callable

Objective = Callable[[np.ndarray], np.ndarray]   # batch: (pop, dim) -> (pop,)
MoveRule = Callable[[np.ndarray, np.ndarray, float, np.random.Generator], np.ndarray]


def attractor_search(
    f: Objective,
    bounds: np.ndarray,
    budget: int,
    seed: int,
    move: MoveRule,
    pop_size: int = 30,
) -> tuple[np.ndarray, float, np.ndarray]:
    """Generic attractor-walk loop shared by GWO, WOA, firefly, and bat.

    `move(pop, fit, progress, rng)` returns the next population. Everything
    else (init, batch evaluation, best tracking, clipping) is metaphor-free.
    """
    rng = np.random.default_rng(seed)
    lb, ub = bounds[:, 0], bounds[:, 1]
    pop = rng.uniform(lb, ub, (pop_size, bounds.shape[0]))
    fit = f(pop)
    i = int(np.argmin(fit))
    best_x, best_f = pop[i].copy(), float(fit[i])
    n_iter = max(1, budget // pop_size - 1)
    history = [best_f]
    for t in range(n_iter):
        pop = np.clip(move(pop, fit, t / n_iter, rng), lb, ub)
        fit = f(pop)
        i = int(np.argmin(fit))
        if fit[i] < best_f:
            best_x, best_f = pop[i].copy(), float(fit[i])
        history.append(best_f)
    return best_x, best_f, np.array(history)


def gwo_move(pop: np.ndarray, fit: np.ndarray, progress: float,
             rng: np.random.Generator) -> np.ndarray:
    """Grey wolf update: mean of three randomized contractions toward the 3 best."""
    leaders = pop[np.argsort(fit)[:3]][:, None, :]            # (3, 1, dim)
    a = 2.0 * (1.0 - progress)                                # GWO's only schedule
    amp = rng.uniform(-a, a, (3,) + pop.shape)                # the "A" coefficient
    scale = rng.uniform(0.0, 2.0, (3,) + pop.shape)           # the "C" coefficient
    return (leaders - amp * np.abs(scale * leaders - pop)).mean(axis=0)


def firefly_move(pop: np.ndarray, fit: np.ndarray, progress: float,
                 rng: np.random.Generator, beta0: float = 1.0,
                 gamma: float = 0.01, alpha: float = 0.3) -> np.ndarray:
    """Firefly update: step toward every better solution with distance-decaying
    weight, plus a shrinking uniform perturbation. Costs O(n^2 d) per iteration.
    gamma must be scaled to the domain (order 1/range^2): with gamma = 1 on a
    [-5, 5]^8 box, exp(-gamma * d^2) underflows and all attraction vanishes."""
    diff = pop[None, :, :] - pop[:, None, :]                  # diff[i, j] = x_j - x_i
    weight = beta0 * np.exp(-gamma * (diff ** 2).sum(axis=2))
    weight = weight * (fit[None, :] < fit[:, None])           # pull only toward better
    pull = (weight[:, :, None] * diff).sum(axis=1)
    noise = alpha * (1.0 - progress) * rng.uniform(-0.5, 0.5, pop.shape)
    return pop + pull + noise


def shifted_sphere(x: np.ndarray) -> np.ndarray:
    """Sphere with the optimum moved off the origin."""
    return ((x - 1.7) ** 2).sum(axis=1)


bounds = np.array([[-5.0, 5.0]] * 8)
for name, mv in [("GWO", gwo_move), ("firefly", firefly_move)]:
    _, best_f, _ = attractor_search(shifted_sphere, bounds, budget=6000, seed=3, move=mv)
    print(f"{name}: best objective {best_f:.4f}")
# Expected: GWO around 1e-4, firefly around 1e-2 with these defaults. One
# skeleton, two "different animals", one algorithmic family: elite attraction
# plus a scheduled perturbation.
```

In GWO's original notation, each wolf moves by

$$
x_i^{t+1} = \frac{1}{3}\sum_{k \in \{\alpha,\beta,\delta\}}\Big(\ell_k - A_k \odot \big|\,C_k \odot \ell_k - x_i^t\,\big|\Big),
\qquad A_k \sim U[-a_t, a_t]^d,\; C_k \sim U[0,2]^d,\; a_t = 2\big(1 - t/T\big),
$$

which is exactly `gwo_move`: a randomized contraction toward the three incumbent leaders with a single linearly decaying amplitude. Note the term $|C_k \odot \ell_k - x_i|$: its magnitude scales with the *absolute coordinates* of leaders and wolves, not with their distance. This is the root of GWO's documented origin bias (Niu et al. 2019) — the probe in Advanced Techniques makes it visible in ten lines.

The blocks in this skill form one module. Save the framework block above and the harmony-search, ES, benchmark, DE, and GA blocks below into a file `metaphor_lab.py`; the demonstration and experiment blocks import from it.

## Worked Example 1: Harmony Search Is a (μ+1) Evolution Strategy

Harmony search (Geem et al. 2001) is the cleanest documented case of a metaphor wrapping a pre-existing algorithm. Weyland (2010), "A rigorous analysis of the harmony search algorithm", proved that HS is a special case of evolution strategies; Weyland (2015) demolished a flagship HS application (sudoku). The original method, in its own vocabulary: keep a "harmony memory" of HMS solutions; "improvise" one new harmony per iteration; replace the worst memory member if the new one is better. Improvisation works per dimension $j$:

$$
x'_j =
\begin{cases}
m_{r_j,\,j} + \mathbb{1}\!\left[u_j < \text{PAR}\right]\cdot \delta_j, & \text{with probability HMCR (memory consideration)}\\[4pt]
\sim U(l_j,\, h_j), & \text{otherwise (random selection)}
\end{cases}
$$

where $m_{r_j, j}$ is gene $j$ of a uniformly random memory member, and $\delta_j \sim U(-\text{bw}, \text{bw}) \cdot (h_j - l_j)$ is the "pitch adjustment". Translate each term:

| Harmony search term | Plain operator name | (μ+1)-ES term |
|---|---|---|
| harmony memory, size HMS | population | parent population, μ = HMS |
| improvisation | create one offspring per iteration | (μ+1) offspring generation |
| memory consideration, rate HMCR | per-gene uniform recombination over all members | global discrete recombination, gene-wise probability HMCR |
| pitch adjustment, rate PAR, bandwidth bw | creep mutation with uniform step | mutation, strength bw |
| random selection, rate 1−HMCR | random-reset mutation | reinitialization mutation |
| replace worst if better | replace-worst survivor selection | (μ+1) replacement |

Every component on the right existed in the ES literature by the 1970s. The two implementations below make the identity executable: they consume random draws in the same order, so with mapped parameters and the same seed they produce *bit-identical* runs.

```python
import numpy as np
from typing import Callable


def harmony_search(
    f: Callable[[np.ndarray], np.ndarray],
    bounds: np.ndarray,
    budget: int,
    seed: int,
    hms: int = 20,
    hmcr: float = 0.9,
    par: float = 0.3,
    bw: float = 0.05,
) -> tuple[np.ndarray, float, np.ndarray]:
    """Harmony search (Geem et al. 2001), faithful to the original rules.

    hms: memory size; hmcr: memory consideration rate; par: pitch adjustment
    rate; bw: bandwidth as a fraction of each variable's range.
    """
    rng = np.random.default_rng(seed)
    dim = bounds.shape[0]
    lb, ub = bounds[:, 0], bounds[:, 1]
    mem = rng.uniform(lb, ub, (hms, dim))
    fit = f(mem)
    evals = hms
    history = [float(fit.min())]
    cols = np.arange(dim)
    while evals < budget:
        use_mem = rng.random(dim) < hmcr                     # memory consideration
        donors = mem[rng.integers(0, hms, dim), cols]        # one donor per gene
        fresh = rng.uniform(lb, ub)                          # random selection
        adjust = rng.random(dim) < par                       # pitch adjustment
        step = rng.uniform(-1.0, 1.0, dim) * bw * (ub - lb)
        new = np.where(use_mem, donors, fresh)
        new = np.where(use_mem & adjust, np.clip(new + step, lb, ub), new)
        new_fit = float(f(new[None])[0])
        evals += 1
        worst = int(np.argmax(fit))
        if new_fit < fit[worst]:                             # replace worst if better
            mem[worst], fit[worst] = new, new_fit
        history.append(float(fit.min()))
    i = int(np.argmin(fit))
    return mem[i], float(fit[i]), np.array(history)
```

```python
import numpy as np
from typing import Callable


def mu_plus_one_es(
    f: Callable[[np.ndarray], np.ndarray],
    bounds: np.ndarray,
    budget: int,
    seed: int,
    mu: int = 20,
    p_recomb: float = 0.9,
    p_creep: float = 0.3,
    creep_width: float = 0.05,
) -> tuple[np.ndarray, float, np.ndarray]:
    """(mu+1)-ES with global discrete recombination, creep and random-reset
    mutation, and replace-worst survivor selection. Components from the
    classic ES literature; compare line by line with harmony_search."""
    rng = np.random.default_rng(seed)
    dim = bounds.shape[0]
    lb, ub = bounds[:, 0], bounds[:, 1]
    pop = rng.uniform(lb, ub, (mu, dim))
    fit = f(pop)
    evals = mu
    history = [float(fit.min())]
    cols = np.arange(dim)
    while evals < budget:
        recomb = rng.random(dim) < p_recomb                  # global discrete recombination
        donors = pop[rng.integers(0, mu, dim), cols]         # one parent per gene
        reset = rng.uniform(lb, ub)                          # random-reset mutation
        creep = rng.random(dim) < p_creep                    # creep mutation gate
        step = rng.uniform(-1.0, 1.0, dim) * creep_width * (ub - lb)
        child = np.where(recomb, donors, reset)
        child = np.where(recomb & creep, np.clip(child + step, lb, ub), child)
        child_fit = float(f(child[None])[0])
        evals += 1
        worst = int(np.argmax(fit))
        if child_fit < fit[worst]:                           # (mu+1) replacement
            pop[worst], fit[worst] = child, child_fit
        history.append(float(fit.min()))
    i = int(np.argmin(fit))
    return pop[i], float(fit[i]), np.array(history)
```

```python
import numpy as np
from metaphor_lab import harmony_search, mu_plus_one_es


def rastrigin(x: np.ndarray) -> np.ndarray:
    """Multimodal benchmark, batch form."""
    return (x ** 2 - 10.0 * np.cos(2.0 * np.pi * x)).sum(axis=1) + 10.0 * x.shape[1]


bounds = np.array([[-5.12, 5.12]] * 10)
_, hs_best, hs_hist = harmony_search(rastrigin, bounds, budget=5000, seed=42,
                                     hms=20, hmcr=0.9, par=0.3, bw=0.05)
_, es_best, es_hist = mu_plus_one_es(rastrigin, bounds, budget=5000, seed=42,
                                     mu=20, p_recomb=0.9, p_creep=0.3, creep_width=0.05)
print(f"HS best: {hs_best:.6f}   ES best: {es_best:.6f}")
print(f"identical trajectories: {np.array_equal(hs_hist, es_hist)}")
# Expected: identical best values and "identical trajectories: True". With the
# mapping HMS=mu, HMCR=p_recomb, PAR=p_creep, bw=creep_width, both functions
# consume the same random draws and produce the same run, bit for bit.
```

This is the template for any equivalence claim: align the random-draw order, map the parameters, and demonstrate identical trajectories. A renaming is not a new algorithm.

### Parameter guidance

The mapped reading also imports decades of ES tuning intuition that the HS literature lacks:

| Parameter (HS name) | ES reading | Typical range | What it trades off |
|---|---|---|---|
| HMS (memory size) | μ, parent population | 10–50 | diversity and restart resistance vs convergence speed; small μ behaves like a local search |
| HMCR (memory consideration) | per-gene recombination probability | 0.85–0.99 | exploitation of the population vs blind restarts; below ~0.8 the method degenerates toward random search in high dimension (probability HMCR^d of a fully memory-built solution collapses) |
| PAR (pitch adjustment) | creep mutation probability | 0.1–0.5 | local refinement frequency vs pure recombination; the only operator that creates *new* nearby values |
| bw (bandwidth) | mutation strength | 1–10% of range, or decaying schedule | exploration early vs precision late; a fixed bw caps final precision at O(bw) |
| budget per restart | offspring count | 10³–10⁵ evaluations | (μ+1) replacement makes HS strongly elitist; long stagnation usually means restart, not more budget |

## Worked Example 2: A Fair-Comparison Template against DE and GA Baselines

When a metaphor algorithm must be evaluated (case 2 and 3 from the Initial Assessment), run the comparison yourself under a sound protocol instead of trusting the paper's table. The non-negotiable protocol elements — details and statistical machinery in **algorithm-benchmarking-statistics**:

1. **Equal budgets in function evaluations**, not iterations: population sizes differ, so "500 iterations each" is not equal work.
2. **Shifted (ideally rotated) test functions.** Zero-centered benchmarks reward origin bias; randomize the optimum location per function and keep it fixed across algorithms and seeds.
3. **Tuning parity.** Tune both sides with the same effort (see **optuna-hyperparameter-tuning** style budgets) or run both at published defaults. Never tuned-vs-default.
4. **At least 15–30 seeds per (algorithm, function) pair**, identical seed lists across algorithms, paired nonparametric tests (Wilcoxon signed-rank per function; Friedman across functions).
5. **Report medians and dispersion**, not just means; report the budget, dimension, and shift policy in the table caption.

The three blocks below give signature-compatible baselines (`optimizer(f, bounds, budget, seed)`), a shifted benchmark suite, and the experiment runner.

```python
import numpy as np
from typing import Callable

Objective = Callable[[np.ndarray], np.ndarray]


def sphere(z: np.ndarray) -> np.ndarray:
    """Unimodal, separable; the minimum any method must handle."""
    return (z ** 2).sum(axis=1)


def rastrigin(z: np.ndarray) -> np.ndarray:
    """Highly multimodal, separable; a regular grid of local optima."""
    return (z ** 2 - 10.0 * np.cos(2.0 * np.pi * z)).sum(axis=1) + 10.0 * z.shape[1]


def rosenbrock(z: np.ndarray) -> np.ndarray:
    """Narrow curved valley, non-separable; optimum at all-ones before shifting."""
    return (100.0 * (z[:, 1:] - z[:, :-1] ** 2) ** 2
            + (1.0 - z[:, :-1]) ** 2).sum(axis=1)


def make_shifted(base: Objective, shift: np.ndarray) -> Objective:
    """Move the optimum to `shift` so that origin bias earns nothing."""
    def f(x: np.ndarray) -> np.ndarray:
        return base(x - shift)
    return f


def shifted_suite(dim: int, seed: int) -> dict[str, Objective]:
    """Three shifted functions; one fixed shift per function, shared by all
    algorithms and seeds in an experiment."""
    rng = np.random.default_rng(seed)
    bases = {"sphere": sphere, "rastrigin": rastrigin, "rosenbrock": rosenbrock}
    return {name: make_shifted(fn, rng.uniform(-2.0, 2.0, dim))
            for name, fn in bases.items()}
```

```python
import numpy as np
from typing import Callable


def de_rand1_bin(
    f: Callable[[np.ndarray], np.ndarray],
    bounds: np.ndarray,
    budget: int,
    seed: int,
    pop_size: int = 30,
    f_weight: float = 0.7,
    cr: float = 0.9,
) -> tuple[np.ndarray, float, np.ndarray]:
    """DE/rand/1/bin, fully vectorized: the standard continuous baseline.
    See differential-evolution for strategy variants and parameter theory."""
    rng = np.random.default_rng(seed)
    dim = bounds.shape[0]
    lb, ub = bounds[:, 0], bounds[:, 1]
    pop = rng.uniform(lb, ub, (pop_size, dim))
    fit = f(pop)
    evals = pop_size
    history = [float(fit.min())]
    rows = np.arange(pop_size)
    while evals + pop_size <= budget:
        perm = rng.random((pop_size, pop_size)).argsort(axis=1)
        others = perm[perm != rows[:, None]].reshape(pop_size, pop_size - 1)
        a, b, c = pop[others[:, 0]], pop[others[:, 1]], pop[others[:, 2]]
        mutant = np.clip(a + f_weight * (b - c), lb, ub)
        cross = rng.random((pop_size, dim)) < cr
        cross[rows, rng.integers(0, dim, pop_size)] = True   # guarantee one gene
        trial = np.where(cross, mutant, pop)
        trial_fit = f(trial)
        evals += pop_size
        better = trial_fit < fit
        pop[better], fit[better] = trial[better], trial_fit[better]
        history.append(float(fit.min()))
    i = int(np.argmin(fit))
    return pop[i], float(fit[i]), np.array(history)
```

```python
import numpy as np
from typing import Callable


def real_ga(
    f: Callable[[np.ndarray], np.ndarray],
    bounds: np.ndarray,
    budget: int,
    seed: int,
    pop_size: int = 30,
    tournament_k: int = 3,
    blx_alpha: float = 0.3,
    mut_prob: float = 0.1,
    mut_sigma: float = 0.1,
    n_elite: int = 2,
) -> tuple[np.ndarray, float, np.ndarray]:
    """Real-coded GA: tournament selection, BLX-alpha crossover, Gaussian
    mutation, elitism. pop_size must be even. Operator details and variants
    belong to the crossover-operators and mutation-and-perturbation-operators
    skills; this is a plain, defensible baseline configuration."""
    rng = np.random.default_rng(seed)
    dim = bounds.shape[0]
    lb, ub = bounds[:, 0], bounds[:, 1]
    span = ub - lb
    pop = rng.uniform(lb, ub, (pop_size, dim))
    fit = f(pop)
    evals = pop_size
    history = [float(fit.min())]
    while evals + pop_size <= budget:
        cand = rng.integers(0, pop_size, (pop_size, tournament_k))
        parents = pop[cand[np.arange(pop_size), np.argmin(fit[cand], axis=1)]]
        p1, p2 = parents[0::2], parents[1::2]
        spread = np.abs(p1 - p2)
        lo = np.minimum(p1, p2) - blx_alpha * spread
        hi = np.maximum(p1, p2) + blx_alpha * spread
        kids = np.vstack([rng.uniform(lo, hi), rng.uniform(lo, hi)])
        mut = rng.random(kids.shape) < mut_prob
        kids = np.where(mut, kids + rng.normal(0.0, mut_sigma, kids.shape) * span, kids)
        kids = np.clip(kids, lb, ub)
        kid_fit = f(kids)
        evals += pop_size
        elite = np.argsort(fit)[:n_elite]                    # keep parents' best
        worst_kids = np.argsort(kid_fit)[-n_elite:]
        kids[worst_kids], kid_fit[worst_kids] = pop[elite], fit[elite]
        pop, fit = kids, kid_fit
        history.append(float(fit.min()))
    i = int(np.argmin(fit))
    return pop[i], float(fit[i]), np.array(history)
```

```python
import numpy as np
import pandas as pd
from scipy import stats
from typing import Callable
from metaphor_lab import attractor_search, de_rand1_bin, gwo_move, real_ga, shifted_suite

Optimizer = Callable[..., tuple[np.ndarray, float, np.ndarray]]


def grey_wolf(f: Callable[[np.ndarray], np.ndarray], bounds: np.ndarray,
              budget: int, seed: int) -> tuple[np.ndarray, float, np.ndarray]:
    """GWO under the shared optimizer signature."""
    return attractor_search(f, bounds, budget, seed, move=gwo_move)


def run_experiment(algorithms: dict[str, Optimizer], dim: int, budget: int,
                   n_seeds: int, suite_seed: int = 2026) -> pd.DataFrame:
    """Tidy results, one row per (function, algorithm, seed); equal budgets,
    identical seed lists, fixed shifts shared by every algorithm."""
    bounds = np.array([[-5.0, 5.0]] * dim)
    rows = []
    for fname, f in shifted_suite(dim, suite_seed).items():
        for seed in range(n_seeds):
            for alg_name, alg in algorithms.items():
                _, best_f, _ = alg(f, bounds, budget, seed)
                rows.append({"function": fname, "algorithm": alg_name,
                             "seed": seed, "best_f": best_f})
    return pd.DataFrame(rows)


def paired_report(df: pd.DataFrame, contender: str, baseline: str) -> pd.DataFrame:
    """Per-function medians and paired Wilcoxon signed-rank p-values."""
    out = []
    for fname, g in df.groupby("function"):
        wide = g.pivot(index="seed", columns="algorithm", values="best_f")
        test = stats.wilcoxon(wide[contender], wide[baseline])
        out.append({"function": fname,
                    f"median_{contender}": wide[contender].median(),
                    f"median_{baseline}": wide[baseline].median(),
                    "wilcoxon_p": float(test.pvalue)})
    return pd.DataFrame(out)


algorithms: dict[str, Optimizer] = {"DE": de_rand1_bin, "GA": real_ga, "GWO": grey_wolf}
results = run_experiment(algorithms, dim=10, budget=10000, n_seeds=15)
print(paired_report(results, "GWO", "DE").to_string(index=False))
# Expected (this exact setup): DE wins sphere (median 4.6e-07 vs 1.7e-02) and
# rosenbrock (3.6 vs 15.3) decisively; GWO wins rastrigin (12.5 vs 37.6); all
# p = 6.1e-05. The rastrigin column is a tuning-parity lesson, not a GWO
# discovery: DE/rand/1/bin with cr=0.9 ignores separability. Rerun DE with
# cr=0.1 and its rastrigin median drops to ~7e-04, far below GWO. Draw no
# conclusion from one suite at default parameters; tune both sides (rule 3).
```

Extend the same runner with the contender's published variants, more functions (the CEC and BBOB suites with their official shift/rotation data), and a Friedman test across functions before drawing conclusions. If the metaphor algorithm wins *under this protocol*, that is a real result worth reporting — it almost never happens against tuned DE or CMA-ES.

## Advanced Techniques

### Structural-bias probe: optimize pure noise

Kononova et al. (2015), "Structural bias in population-based algorithms" (Information Sciences), proposed a decisive diagnostic: run the algorithm on an objective that returns i.i.d. noise for every evaluation. No search direction exists, so an unbiased sampler returns "best" points uniformly distributed over the box. An algorithm whose returned points cluster anywhere — typically the center — carries a structural bias that contaminates every benchmark whose optimum sits at that location. Kudela (2022, Nature Machine Intelligence) showed how badly this distorts published rankings of metaphor methods on zero-centered suites.

```python
import numpy as np
from typing import Callable
from metaphor_lab import attractor_search, de_rand1_bin, gwo_move

Optimizer = Callable[..., tuple[np.ndarray, float, np.ndarray]]


def gwo(f: Callable[[np.ndarray], np.ndarray], bounds: np.ndarray,
        budget: int, seed: int) -> tuple[np.ndarray, float, np.ndarray]:
    """GWO under the shared optimizer signature."""
    return attractor_search(f, bounds, budget, seed, move=gwo_move)


def structural_bias_probe(optimizer: Optimizer, dim: int = 20,
                          budget: int = 4000, n_runs: int = 20) -> float:
    """Optimize i.i.d. noise; report the mean distance of the returned points
    from the box center. Unbiased sampling matches the uniform reference."""
    bounds = np.array([[-100.0, 100.0]] * dim)
    dists = []
    for run in range(n_runs):
        noise_rng = np.random.default_rng(10_000 + run)

        def noise(x: np.ndarray) -> np.ndarray:
            return noise_rng.random(x.shape[0])

        best_x, _, _ = optimizer(noise, bounds, budget, run)
        dists.append(float(np.linalg.norm(best_x)))
    return float(np.mean(dists))


uniform_ref = 100.0 * (20.0 / 3.0) ** 0.5     # E[||x||] scale for U[-100,100]^20
print(f"uniform reference: {uniform_ref:.0f}")
print(f"DE : {structural_bias_probe(de_rand1_bin):.0f}")
print(f"GWO: {structural_bias_probe(gwo):.0f}")
# Expected (these settings): uniform reference 258; DE ~331 (its variance
# expansion drifts samples toward the box faces -- spread out, no center pull);
# GWO ~167, well below the reference, and the bias compounds with budget:
# ~102 at 12000 evaluations, ~19 at 30000. GWO's step term |C * leader - x|
# scales with absolute coordinates, so the population contracts toward the
# origin even though the objective carries no information at all.
```

Run this probe on any algorithm before trusting its results on benchmarks whose optima sit at the origin. It needs only the shared optimizer signature and minutes of compute.

### Mining metaphors for reusable components

The defensible way to engage with this literature is component extraction. The one broadly accepted contribution is the heavy-tailed mutation popularized by cuckoo search: Lévy-stable steps produce mostly small refinements with occasional long jumps, a useful restart-free diversification. Extract the component and use it inside DE, ES, or ILS perturbations directly.

```python
import numpy as np
from math import gamma, pi, sin


def levy_steps(rng: np.random.Generator, size: tuple[int, ...],
               beta: float = 1.5) -> np.ndarray:
    """Mantegna's algorithm: symmetric heavy-tailed steps, stability index
    beta in (1, 2); smaller beta gives heavier tails."""
    sigma = (gamma(1.0 + beta) * sin(pi * beta / 2.0)
             / (gamma((1.0 + beta) / 2.0) * beta
                * 2.0 ** ((beta - 1.0) / 2.0))) ** (1.0 / beta)
    u = rng.normal(0.0, sigma, size)
    v = rng.normal(0.0, 1.0, size)
    return u / np.abs(v) ** (1.0 / beta)


rng = np.random.default_rng(0)
steps = levy_steps(rng, (100_000,))
print(f"median |step| = {np.median(np.abs(steps)):.2f}, "
      f"max |step| = {np.abs(steps).max():.0f}")
# Expected: median |step| = 0.63, max |step| = 1791 -- mostly local moves
# with rare very long jumps. Plug into any mutation operator; no cuckoos
# required.
```

### Component ablation: test what actually works

When a metaphor paper claims its mechanism matters, ablate it. Replace each "novel" component with the plain classic it shadows (spiral move → Gaussian step around the best; three leaders → one; loudness gate → constant acceptance) and rerun the fair-comparison template. If performance does not change beyond noise, the component is decoration; if one substitution destroys performance, you have found the part doing the work — usually the elitism or the step-size schedule. This is the methodology behind the Camacho-Villalón et al. analyses, and it doubles as the honest way to *improve* a method: tune the load-carrying component with established theory instead of adding metaphor parameters.

### Reading a "novel metaheuristic" paper critically

Apply this checklist before believing any claim: (1) update equations stated unambiguously in vector form, with every random quantity's distribution specified; (2) an operator-level description free of the metaphor (per the Journal of Heuristics policy); (3) comparison against tuned modern baselines — CMA-ES, L-SHADE-class DE — not only 1995-default GA/PSO; (4) shifted or rotated benchmarks, or CEC/BBOB suites with official transformations; (5) equal evaluation budgets; (6) ≥15 seeds with paired statistics, not bolded means; (7) released code; (8) a structural-bias check or at least awareness of it. Papers failing (3)–(5) — the majority — support no superiority conclusion whatsoever. As a referee, request the missing items; as a reader, rerun the fair-comparison template above before adoption.

## Practical Challenges

**A reviewer demands comparison against grey wolf, whale, and two other metaphor algorithms.** Comply cheaply and rigorously: implement them in the attractor-search skeleton (each move rule is 5–15 lines), run them inside the fair-comparison template with equal budgets and shifted functions, and report paired statistics. The expected outcome — tuned DE/CMA-ES dominating — strengthens the paper. Cite Sörensen (2015) and Camacho-Villalón et al. (2023) when explaining the selection of baselines, and keep the tone factual.

**Published results of a metaphor algorithm cannot be reproduced.** First suspect the benchmark protocol, not your code: check whether the paper used unshifted functions, counted iterations instead of evaluations, or seeded the best-of-30 run. Reconstruct their exact setting once to confirm you can hit their numbers, then report both their setting and the sound protocol side by side. If the pseudocode is ambiguous (common), document every interpretation choice you made.

**The metaphor paper's table shows it beating DE and even CMA-ES.** Audit in this order: origin-centered benchmarks (run the structural-bias probe), unequal budgets, default-vs-tuned asymmetry, cherry-picked dimensions, and statistical tests on means of differently-scaled functions. Kudela (2022) documents how each of these manufactures wins. A claim that survives all five audits on BBOB/CEC suites with official shifts deserves genuine attention.

**You need the algorithm for a combinatorial problem, but it is defined on continuous vectors.** The standard bridge is a random-key decoder: keep the continuous dynamics, sort the keys to obtain a permutation. But note what this means — the metaphor now only generates real vectors that a decoder interprets, so any continuous method works identically. Choose by performance under the fair template, or skip the detour and use a native combinatorial method via **metaheuristic-design-principles**.

**Two papers describe "the same" algorithm with different update equations.** Version drift is endemic because the original descriptions are informal. Fix the variant by citing the exact equations you implement, prefer the most-cited original, and put your implementation under test (known-optimum instances, monotone best-so-far, the bias probe). Where the original is internally inconsistent — bat algorithm's loudness/pulse-rate updates are a known case — state your resolution explicitly.

**A stakeholder or supervisor wants the novel algorithm because it is recent and heavily cited.** Do not argue from authority; run the one-day experiment. The fair-comparison template with the stakeholder's own problem instances, equal budgets, and 15+ seeds settles the question with data and costs little. Frame the established method as the low-risk choice: known failure modes, tuning guidance, library support, and reviewable methodology.

**You found a genuinely new mechanism inside a metaphor paper.** It happens — heavy-tailed mutation via cuckoo search is the canonical example. Extract the component, describe it in operator language, ablate it inside an established method, and publish the component study. That contribution survives; the metaphor wrapper does not.

## Tools & Libraries

| Library | When to use | Note |
|---|---|---|
| mealpy | Reproducing metaphor algorithms without reimplementing | Largest curated Python collection (200+ methods); treat as a comparison harness, not a production solver |
| niapy | Same purpose, smaller scope | Cleaner API, fewer algorithms; good for quick referee checks |
| pymoo | Established EAs: GA, DE, ES, CMA-ES, NSGA-II | Well-tested implementations of the baselines that matter |
| pycma | CMA-ES reference implementation | The continuous black-box baseline any new method must beat |
| scipy.optimize | `differential_evolution`, `dual_annealing` | Zero extra dependencies; solid DE for the fair-comparison template |
| nevergrad | Algorithm portfolios and black-box comparison | Useful when the answer should be "run a portfolio, not one metaphor" |
| IOHprofiler / COCO (BBOB) | Benchmarking with official shifts, rotations, anytime performance | The protocol infrastructure that prevents origin-bias artifacts |

## Output Format

A complete answer about a metaphor-based algorithm contains:

1. **Mechanism translation table** — metaphor term → operator term → classic equivalent, like the HS table above, with the relevant critique citations (Sörensen 2015; Weyland 2010; Camacho-Villalón et al. 2023; Kononova et al. 2015; Kudela 2022).
2. **Family placement** — one sentence per algorithm: "X is a (μ+λ)-ES with heavy-tailed mutation" or "Y is a leader-guided random walk in the PSO family", with the update equation in vector form.
3. **Bias audit** — structural-bias probe numbers against the uniform reference, plus a statement of whether published results relied on zero-centered benchmarks.
4. **Fair-comparison results** — a table in this shape (numbers below are the verified output of the worked template: GWO as contender, dim 10, 10⁴ evaluations, 15 seeds, shifts U(−2, 2), both algorithms at published defaults):

| function | median[GWO] | IQR | median[DE] | IQR | Wilcoxon p | winner |
|---|---|---|---|---|---|---|
| shifted sphere | 1.7e-02 | 3.3e-03 | 4.6e-07 | 8.1e-07 | 6.1e-05 | DE |
| shifted rastrigin | 1.2e+01 | 1.6e+00 | 3.8e+01 | 1.5e+01 | 6.1e-05 | GWO at DE defaults; flips at cr = 0.1 |
| shifted rosenbrock | 1.5e+01 | 6.3e+00 | 3.6e+00 | 8.1e-01 | 6.1e-05 | DE |

   Report honest losses (the rastrigin row) together with their diagnosis — here, a separability-blind DE default, which is precisely what tuning parity exists to catch.

5. **Convergence summary** — best-so-far curves over evaluations (median with an inter-seed band), all algorithms on the same evaluation axis.
6. **Recommendation memo** — the decision (adopt / use established equivalent / extract component), the evidence line for it, and the concrete replacement: which established method, which implementation, which starting parameters.
7. **Artifacts** — `metaphor_lab.py` (algorithms + suite), the runner script, the tidy results table (CSV/parquet, one row per function-algorithm-seed), and the exact seeds and shifts for reproduction.

## Questions to Ask

- Are you choosing an algorithm for a real problem, answering a reviewer, reviewing a paper, or reproducing published results?
- Which exact algorithm and paper — and if a variant, which update equations?
- Is your problem continuous, combinatorial, or mixed? What are dimension and evaluation budget?
- What does one objective evaluation cost, and is it noisy?
- Which baselines do you already have implementations for (DE, CMA-ES, PSO, GA)?
- Were the published results you rely on produced on zero-centered, unshifted benchmark functions?
- Were the baselines in that study tuned with the same effort as the proposed method?
- How many seeds and which statistical tests can your compute budget afford?
- Does your venue restrict metaphor-based terminology, or does your application community expect a specific named method?

## Related Skills

- **metaheuristic-design-principles** — when the user should design a method from proven components (representation, operators, acceptance, restarts) instead of adopting a metaphor algorithm wholesale.
- **particle-swarm-optimization** — when the algorithm under review lands in the PSO family (firefly, bat, grey wolf, whale) and the user needs the canonical method, its theory, and its discrete adaptations.
- **differential-evolution** — when a strong continuous baseline is needed for a fair comparison, or as the concrete replacement recommendation for a metaphor method.
- **algorithm-benchmarking-statistics** — when designing the comparison protocol: instance/seed design, paired tests, effect sizes, performance profiles, and reporting standards.
