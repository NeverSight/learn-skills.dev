---
name: selection-and-replacement-strategies
description: When the user wants to choose, implement, or tune parent selection and survivor replacement in evolutionary algorithms — tournament, roulette-wheel, rank, stochastic universal sampling, and Boltzmann selection, plus generational vs steady-state replacement, elitism, and (mu+lambda) vs (mu,lambda) — with selection-pressure and takeover-time analysis. Also use when the user mentions "selection operator," "tournament selection," "roulette wheel," "rank selection," "elitism," "steady-state GA," or when a population converges prematurely or stalls. For diversity machinery, see diversity-and-population-management; for the full GA loop, see genetic-algorithms.
---

# Selection and Replacement Strategies

You are an expert in selection and replacement for evolutionary and population-based metaheuristics. This skill is the reference catalog: for every standard parent-selection scheme — tournament, fitness-proportionate (roulette), linear and exponential rank, stochastic universal sampling, Boltzmann — and every standard survivor strategy — generational, elitist, steady-state, (mu+lambda), (mu,lambda) — it gives when to use it, a numpy implementation, a complexity note, and the algorithms and problem settings it fits. Use the pressure framework below (selection intensity, takeover time) to set pressure deliberately instead of inheriting it by accident from a default operator, and use the measurement harness to verify the setting empirically.

## Initial Assessment

Establish these facts before recommending or writing any selection code:

- **Maximize or minimize, and can fitness be negative or zero?** Fitness-proportionate selection requires strictly positive values and is not invariant to shifting; a penalized objective that dips below zero rules it out unless you accept that the shift itself silently sets the pressure. Rank and tournament are immune.
- **Audit every place selection pressure enters.** Parent selection, survivor selection, elitism, and duplicate handling all exert pressure, and their effects compound. Tournament k=3 parents feeding a replace-worst steady-state population is a very different machine from the same tournament feeding pure generational replacement.
- **Population size N and total evaluation budget.** Convert the budget to generations G = budget / lambda, then compare against takeover time. If takeover is far below G, most of the run is post-convergence mutation hill-climbing; if it is far above G, the run never exploits.
- **Which algorithm consumes the operator?** A canonical GA, a memetic algorithm with strong local search (tolerates and usually wants lower parent pressure), an EDA (wants truncation), an ES with self-adaptive parameters (requires comma replacement), or a multi-objective EA (selection ranks by dominance and crowding, see multi-objective-optimization).
- **Generational or steady-state architecture, and how is evaluation parallelized?** Generational and (mu,lambda) produce full batches that saturate parallel workers; steady-state evaluates one child at a time and serializes unless you run asynchronous variants.
- **Is the objective noisy or stochastic?** Noise discounts effective selection intensity and makes naive elitism enshrine lucky evaluations. Plan resampling or comma replacement before tuning anything else.
- **What disruption do the variation operators cause?** Strong mutation or local search after selection rebuilds diversity each generation and tolerates higher pressure; weak variation under high pressure converges prematurely.
- **Any observed pathology?** "Converges in 20 generations then stalls" means pressure (or compounded pressure) is too high or diversity machinery is missing; "never improves past random search" usually means pressure is too low or proportionate selection has collapsed.
- **Constraint handling.** Penalty terms stretch and compress the fitness scale over the run; scale-sensitive schemes (proportionate, raw Boltzmann) inherit that distortion, rank-based schemes do not.
- **Reproducibility.** Every stochastic scheme takes an explicit `np.random.Generator`; record seeds per run. A scheme comparison without fixed seeds and repeated runs is noise.

## Pressure Anatomy: Intensity, Takeover Time, and the Two Ends of Selection

### Two decisions, one budget

Every population algorithm makes two selection decisions per cycle: **parent selection** (who reproduces, possibly with repeats) and **survivor selection / replacement** (who stays in the population). Both convert fitness differences into copy-number differences; the product of the two is the algorithm's real pressure. This skill catalogs both ends separately and then measures them together, because tuning one end while ignoring the other is the most common selection mistake.

### Selection intensity

The standard scalar for pressure is the selection intensity (Mühlenbein & Schlierkamp-Voosen 1993, "Predictive Models for the Breeder Genetic Algorithm"): the standardized gain in mean fitness produced by selection alone,

$$
I = \frac{\bar f_{\mathrm{sel}} - \bar f}{\sigma_f},
$$

where $\bar f$ and $\sigma_f$ are the population mean and standard deviation and $\bar f_{\mathrm{sel}}$ is the mean of the selected parents. For approximately normal fitness distributions, closed forms exist per scheme (Blickle & Thiele 1996, "A Comparison of Selection Schemes Used in Evolutionary Algorithms") and are tabulated below. Intensity is measurable in any run — log it every generation; it is the cheapest diagnostic in this whole skill.

### Takeover time

Takeover time is the number of generations selection alone (no crossover, no mutation) needs before copies of the single best individual fill the population (Goldberg & Deb 1991, "A Comparative Analysis of Selection Schemes Used in Genetic Algorithms"). Approximate forms for population size N:

$$
\tau_{\text{tournament-}k} \approx \frac{\ln N + \ln \ln N}{\ln k},
\qquad
\tau_{\text{rank},\, s=2} \approx \log_2 N + \log_2 \ln N,
\qquad
\tau_{\text{proportionate}} \approx N \ln N \;\; (f(x) = x),
$$

$$
\tau_{(\mu,\lambda)} \approx \frac{\ln \lambda}{\ln(\lambda/\mu)} \qquad \text{(truncation)}.
$$

The truncation form is due to Bäck (1996), *Evolutionary Algorithms in Theory and Practice*. For N = 100: binary tournament takes about 9 generations, tournament k=7 about 3, proportionate selection on linear fitness about 460. The qualitative lesson is robust even where the formulas are loose: ordinal schemes take over in O(log N) generations, proportionate selection in O(N log N), and the gap is the entire design space. Budget rule of thumb: aim for takeover time between G/10 and G/2 of your generation budget G, then verify with the harness below and adjust.

### Master catalog: parent selection

| Scheme | Pressure knob | Intensity I (normal fitness) | Expected copies of best | Cost per generation | Scale-sensitive? |
|---|---|---|---|---|---|
| Roulette (proportionate) | none — the fitness scale itself | $\sigma_f / \bar f$ (coefficient of variation) | $N f_{\max} / \sum f$ | O(N log N) | yes, and not shift-invariant |
| Stochastic universal sampling | none (same expectation as roulette) | same as roulette, minimal variance | floor/ceil of expected | O(N log N) | yes |
| Linear rank, factor s | s in (1, 2] | $(s-1)/\sqrt{\pi}$ | s | O(N log N) (sort) | no |
| Exponential rank, base c | c in (0, 1) | grows as c decreases | can exceed 2 | O(N log N) | no |
| Tournament, size k | k (and win prob p) | 0.56 (k=2), 0.85 (k=3), 1.16 (k=5), 1.35 (k=7) | about k | O(Nk), no sort | no |
| Boltzmann, temperature T | T (anneal it) | about $\sigma_f / T$ raw; $1/t$ if sigma-scaled | exponentially tilted | O(N) | yes unless sigma-scaled |
| Truncation, ratio tau = mu/lambda | tau | $\phi(z_\tau)/\tau$: 0.80 (1/2), 1.27 (1/4), 1.75 (1/10) | lambda/mu | O(lambda) argpartition | no |

Linear rank with s=2 and binary tournament have the same expected behavior (both I = 0.564); tournament is cheaper and needs no global fitness statistics, which is why it became the modern default.

### Master catalog: replacement

| Strategy | Generation gap | Can lose the incumbent? | Pressure contribution | Use when |
|---|---|---|---|---|
| Generational, no elitism | full population | yes | none (parents only) | theory experiments; very strong parent pressure already present |
| Generational + e elites | all but e | no | mild, grows with e | the default GA configuration (e = 1-2) |
| Steady-state, replace worst | 1/N per step | no | strong (both ends push) | fast exploitation, memetic algorithms, asynchronous evaluation |
| Steady-state, replace oldest/random | 1/N per step | possibly | mild | gentler steady-state; behaves close to generational (Syswerda 1991) |
| (mu+lambda) truncation | pooled | no | strong, set by lambda/mu | static noise-free problems, combinatorial EAs, memetic algorithms |
| (mu,lambda) truncation | full | yes, by design | set by lambda/mu | self-adaptation, noisy or time-varying objectives (Beyer & Schwefel 2002) |

### Scheme-by-context fit

| Context | Recommended configuration | Why |
|---|---|---|
| Canonical GA, static noise-free objective | tournament k=2-4 or linear rank s=1.5-1.8, generational + 1-2 elites | scale-free, one knob, cheap, well understood |
| Memetic algorithm (strong local search) | k=2 parents + steady-state replace-worst with duplicate rejection | local search exploits; survivor end carries the pressure |
| Noisy fitness | larger tournaments + resampling; comma replacement; re-evaluated elites | noise discounts intensity; stale elites are poison |
| Self-adaptive parameters (ES-style) | (mu,lambda), lambda/mu in 4-7 | comma flushes stale strategy parameters with their carriers |
| EDA model fitting | truncation, tau = 0.3-0.5 | the probabilistic model wants a clean elite sample |
| Multi-objective EA | binary tournament on (nondomination rank, crowding); (mu+lambda) environmental selection | scalar fitness does not exist; see multi-objective-optimization |
| Parallel batched evaluation | generational or (mu,lambda) with large lambda | full offspring batches saturate workers |

## Parent Selection Catalog

All implementations take an explicit `np.random.Generator`, return integer index arrays into the population (so they compose with any genotype array), and are vectorized — no Python loop touches individuals.

### Fitness-proportionate selection (roulette wheel)

**When to use.** Almost never as a tuning choice in modern practice — its pressure equals the population's coefficient of variation, which you do not control and which decays to zero as the run converges (the "stall" pathology). It survives as the historical baseline (Holland 1975, *Adaptation in Natural and Artificial Systems*), as the sampling core that rank and Boltzmann reuse, and in settings where fitness genuinely is a nonnegative rate you want copies proportional to. **Complexity:** O(N) cumulative sum, O(log N) per draw via `searchsorted`. **Fits:** teaching, probability-matching components inside EDAs, never penalized objectives.

```python
import numpy as np


def roulette_select(
    fitness: np.ndarray, n_select: int, rng: np.random.Generator
) -> np.ndarray:
    """Fitness-proportionate selection; returns indices of selected parents.

    Requires strictly positive fitness. Each draw is independent, so the
    realized copy counts have high variance; prefer SUS for the same
    expected copies with minimal variance.
    """
    p = fitness / fitness.sum()
    cum = np.cumsum(p)
    cum[-1] = 1.0                                  # guard against rounding
    return np.searchsorted(cum, rng.random(n_select), side="right")


# Tiny instance: fitness 1..5, copies should be proportional to fitness.
rng = np.random.default_rng(0)
fit = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
counts = np.bincount(roulette_select(fit, 15_000, rng), minlength=5)
print(np.round(counts / 15_000, 3))
# Expected: approx [0.067, 0.133, 0.200, 0.267, 0.333] = fitness / 15
```

### Stochastic universal sampling (SUS)

**When to use.** Whenever you sample parents from an explicit probability vector — proportionate, rank, or Boltzmann probabilities alike. Baker (1987), "Reducing Bias and Inefficiency in the Selection Algorithm": one spin, `n_select` equally spaced pointers, so every individual receives either the floor or the ceiling of its expected copy count (zero bias, minimal spread). This removes the sampling-variance failure mode of roulette at identical expected pressure. **Complexity:** O(N) plus one `searchsorted` over all pointers; effectively free. **Fits:** drop-in replacement for any wheel.

```python
import numpy as np


def sus_select(
    fitness: np.ndarray, n_select: int, rng: np.random.Generator
) -> np.ndarray:
    """Stochastic universal sampling (Baker 1987) over positive fitness.

    Shuffles the result so downstream pairing of consecutive parents
    is random rather than fitness-sorted.
    """
    p = fitness / fitness.sum()
    cum = np.cumsum(p)
    cum[-1] = 1.0
    pointers = (rng.random() + np.arange(n_select)) / n_select
    return rng.permutation(np.searchsorted(cum, pointers, side="right"))


rng = np.random.default_rng(1)
fit = np.array([1.0, 2.0, 3.0, 4.0])
counts = np.bincount(sus_select(fit, 10, rng), minlength=4)
print(counts)
# Expected: [1 2 3 4] — expected copies n_select * p_i = [1, 2, 3, 4]
# are integers here, so SUS hits them exactly, every time, any seed
```

### Rank selection (linear and exponential)

**When to use.** When you want proportionate-style smooth probabilities but with pressure that is constant over the run and immune to the fitness scale: rank selection depends only on the ordering, so it is invariant under any monotone transform of the objective (penalties, log-scaling, sign flips handled by sort direction). Linear ranking (Baker 1985, "Adaptive Selection Methods for Genetic Algorithms") gives the best individual s expected copies, s in (1, 2]; the worst gets 2 - s. Exponential ranking breaks the s <= 2 ceiling when you need more pressure but still want smooth probabilities. **Complexity:** O(N log N) for the sort, then SUS. **Fits:** GENITOR-style steady-state GAs (Whitley 1989, "The GENITOR Algorithm and Selection Pressure"), any GA whose objective includes penalty terms.

```python
import numpy as np


def linear_rank_probs(fitness: np.ndarray, s: float = 1.7) -> np.ndarray:
    """Baker (1985) linear ranking probabilities; pressure knob 1 < s <= 2.

    Best individual expects s copies per N draws, worst expects 2 - s.
    Depends only on ranks, never on fitness magnitudes.
    """
    n = fitness.size
    ranks = np.empty(n)
    ranks[np.argsort(fitness)] = np.arange(n)      # 0 = worst, n-1 = best
    return (2.0 - s) / n + 2.0 * ranks * (s - 1.0) / (n * (n - 1.0))


def exponential_rank_probs(fitness: np.ndarray, c: float = 0.98) -> np.ndarray:
    """Exponential ranking: weight c^(n-1-rank), c in (0, 1).

    Smaller c means more pressure; c -> 1 approaches uniform selection.
    """
    n = fitness.size
    ranks = np.empty(n, dtype=np.int64)
    ranks[np.argsort(fitness)] = np.arange(n)
    w = c ** (n - 1.0 - ranks)
    return w / w.sum()


def rank_select(
    fitness: np.ndarray, n_select: int, rng: np.random.Generator,
    s: float = 1.7,
) -> np.ndarray:
    """Linear-rank selection drawn with SUS for minimal sampling variance."""
    p = linear_rank_probs(fitness, s)
    cum = np.cumsum(p)
    cum[-1] = 1.0
    pointers = (rng.random() + np.arange(n_select)) / n_select
    return rng.permutation(np.searchsorted(cum, pointers, side="right"))


fit = np.array([10.0, 1e6, 10.5, 11.0])            # one huge outlier
print(np.round(linear_rank_probs(fit, s=2.0), 3))
# Expected: [0. 0.5 0.167 0.333] — the outlier gets rank share 0.5, not
# probability ~1.0 as roulette would give it; ranking absorbs magnitude
```

### Tournament selection

**When to use.** The modern default. One integer knob k sets pressure (I from 0.56 at k=2 to 1.35 at k=7); no sort, no global fitness statistics, no positivity requirement; it needs only pairwise comparisons, so it works even when "fitness" is the outcome of a head-to-head simulation. The probability that the rank-r individual (r = 0 worst) wins a size-k tournament with replacement is $((r+1)^k - r^k)/N^k$. The probabilistic variant (winner with probability p, else the runner-up, geometrically) interpolates pressure below k=2 when even binary tournament is too greedy. Sokolov & Whitley (2005), "Unbiased Tournament Selection," removes the with-replacement sampling noise by permuting columns instead. **Complexity:** O(Nk) per generation, embarrassingly parallel. **Fits:** everything; the first thing to try.

```python
import numpy as np


def tournament_select(
    fitness: np.ndarray, n_select: int, rng: np.random.Generator,
    k: int = 3, p_win: float = 1.0,
) -> np.ndarray:
    """Tournament selection with replacement, fully vectorized.

    Draws an (n_select, k) candidate matrix and takes each row's best.
    With p_win < 1 the rank-j candidate of the tournament wins with
    probability p_win * (1 - p_win)^j (probabilistic tournament).
    """
    cand = rng.integers(0, fitness.size, size=(n_select, k))
    if p_win >= 1.0:
        return cand[np.arange(n_select), np.argmax(fitness[cand], axis=1)]
    order = np.argsort(-fitness[cand], axis=1, kind="stable")
    j = np.minimum(rng.geometric(p_win, size=n_select) - 1, k - 1)
    return cand[np.arange(n_select), order[np.arange(n_select), j]]


rng = np.random.default_rng(3)
fit = np.arange(10, dtype=float)                   # individual i has fitness i
sel = tournament_select(fit, 100_000, rng, k=2)
print(np.round(np.bincount(sel, minlength=10) / 100_000, 3))
# Expected: P(rank r) = ((r+1)^2 - r^2)/100 = (2r+1)/100, i.e. approximately
# [0.01, 0.03, 0.05, 0.07, 0.09, 0.11, 0.13, 0.15, 0.17, 0.19]
```

### Boltzmann selection

**When to use.** When you want pressure as an explicit, continuously *scheduled* quantity: $p_i \propto \exp(f_i / T)$, high temperature T is near-uniform exploration, low T is near-greedy exploitation, and annealing T over the run sweeps the whole range — the population analogue of simulated annealing's acceptance schedule (Goldberg 1990, "A Note on Boltzmann Tournament Selection for Genetic Algorithms and Population-Oriented Simulated Annealing"; Mahfoud & Goldberg 1995, parallel recombinative simulated annealing). Raw Boltzmann is scale-sensitive — dividing fitness by its standard deviation before the exponent makes the temperature scale-free and is strongly recommended. For approximately normal fitness, exponential tilting shifts the mean by $\sigma_f^2/T$, so intensity is about $\sigma_f / T$ (or $1/t$ with the sigma-scaled temperature t). **Complexity:** O(N). **Fits:** runs with a known evaluation budget where you want exploration early and exploitation late without changing operators.

```python
import numpy as np


def boltzmann_select(
    fitness: np.ndarray, n_select: int, rng: np.random.Generator,
    temperature: float,
) -> np.ndarray:
    """Boltzmann selection, p_i proportional to exp(f_i / T), computed stably.

    Subtracting the max before exponentiating prevents overflow; sampling
    uses SUS pointers for minimal variance.
    """
    z = (fitness - fitness.max()) / max(temperature, 1e-12)
    p = np.exp(z)
    p /= p.sum()
    cum = np.cumsum(p)
    cum[-1] = 1.0
    pointers = (rng.random() + np.arange(n_select)) / n_select
    return rng.permutation(np.searchsorted(cum, pointers, side="right"))


def geometric_temperature(t0: float, t_end: float, n_steps: int) -> np.ndarray:
    """Geometric annealing schedule from t0 down to t_end over n_steps."""
    alpha = (t_end / t0) ** (1.0 / max(n_steps - 1, 1))
    return t0 * alpha ** np.arange(n_steps)


rng = np.random.default_rng(4)
fit = np.array([1.0, 2.0, 3.0])
for temp in (10.0, 1.0, 0.1):
    counts = np.bincount(boltzmann_select(fit, 9_000, rng, temp), minlength=3)
    print(temp, np.round(counts / 9_000, 2))
# Expected: T=10 near [0.30 0.33 0.37] (almost uniform); T=1 about
# [0.09 0.24 0.67]; T=0.1 about [0.00 0.00 1.00] (effectively greedy)
```

### Measuring pressure directly: intensity and takeover harness

Closed forms assume normal fitness and large N; your penalized, multi-modal, finite-N reality differs. This harness measures both quantities for any scheme: realized intensity from one generation's selection, and takeover time by running selection alone (no variation) until the best type holds 90% of the population. The 90% criterion (instead of 100%) keeps near-neutral end-game drift from dominating the statistic; the best starts with 5% of the slots because a single copy goes extinct with noticeable probability under high-variance schemes, which would bias the median upward.

```python
import numpy as np
from collections.abc import Callable

SelectFn = Callable[[np.ndarray, int, np.random.Generator], np.ndarray]


def realized_intensity(fitness: np.ndarray, selected: np.ndarray) -> float:
    """Realized selection intensity I = (mean(selected) - mean) / std."""
    sd = float(fitness.std())
    if sd == 0.0:
        return 0.0
    return float((fitness[selected].mean() - fitness.mean()) / sd)


def takeover_time(
    select: SelectFn, n_pop: int, rng: np.random.Generator,
    share_target: float = 0.9, max_gen: int = 5_000,
) -> int:
    """Generations of selection alone until the best type holds share_target.

    Selection-only dynamics in the sense of Goldberg & Deb (1991): the
    population is just a fitness multiset, each generation replaced by the
    selected multiset. Returns max_gen if the target share is never reached
    (e.g. the best type drifted to extinction under a high-variance scheme).
    """
    fitness = np.linspace(0.5, 0.99, n_pop)
    fitness[: max(1, n_pop // 20)] = 1.0           # best starts at 5% share
    for gen in range(1, max_gen + 1):
        fitness = fitness[select(fitness, n_pop, rng)]
        if (fitness == 1.0).mean() >= share_target:
            return gen
    return max_gen


def median_takeover(select: SelectFn, n_pop: int, n_runs: int, seed: int) -> float:
    """Median takeover time over independent replicates."""
    times = [takeover_time(select, n_pop, np.random.default_rng(seed + r))
             for r in range(n_runs)]
    return float(np.median(times))


def tournament_k(k: int) -> SelectFn:
    """Size-k tournament closure for the harness."""
    def sel(f: np.ndarray, n: int, rng: np.random.Generator) -> np.ndarray:
        cand = rng.integers(0, f.size, size=(n, k))
        return cand[np.arange(n), np.argmax(f[cand], axis=1)]
    return sel


def proportionate(f: np.ndarray, n: int, rng: np.random.Generator) -> np.ndarray:
    """Roulette wheel for the harness (fitness here is already positive)."""
    cum = np.cumsum(f / f.sum())
    cum[-1] = 1.0
    return np.searchsorted(cum, rng.random(n), side="right")


for name, fn in [("tournament k=2", tournament_k(2)),
                 ("tournament k=7", tournament_k(7)),
                 ("proportionate", proportionate)]:
    print(name, median_takeover(fn, n_pop=100, n_runs=9, seed=7))
# Expected: tournament k=2 about 6-9 generations and k=7 about 2-4
# (Goldberg-Deb predict 8.9 and 3.2 for full takeover from a single copy at
# N=100); proportionate is one to two orders of magnitude slower — tens to a
# few hundred generations — because its pressure equals the population's
# relative fitness spread, which shrinks exactly as takeover proceeds.
```

## Replacement and Survivor Selection Catalog

Replacement decides the generation gap (De Jong 1975 dissertation: how much of the population turns over per cycle) and whether the incumbent can be lost. **Generational** replacement swaps the whole population and relies entirely on parent selection for pressure; adding **elitism** (copy the e best parents over the worst offspring) is the cheap fix that makes best-so-far monotone inside the population. **Steady-state** replacement (Whitley 1989, GENITOR; Syswerda 1991, "A Study of Reproduction in Generational and Steady-State Genetic Algorithms") inserts one child at a time: replace-worst adds strong survivor pressure on top of parent pressure, while replace-random or replace-oldest behaves close to generational. **(mu+lambda)** pools parents and offspring and keeps the best mu — pure exploitation, never loses the incumbent. **(mu,lambda)** keeps the best mu of the lambda offspring only — it deliberately forgets, which is exactly what self-adaptive strategy parameters and noisy or time-varying objectives need (Beyer & Schwefel 2002, "Evolution Strategies — A Comprehensive Introduction"); keep an external best-so-far archive for reporting. Truncation pressure is set by lambda/mu (intensity 0.80 at tau=1/2, 1.27 at 1/4, 1.75 at 1/10).

**Complexity:** all of the following are O(N) or O(N log N) per generation with `argpartition`; replacement is never the bottleneck. **Fits:** see the replacement table in the anatomy section.

```python
import numpy as np


def generational_replace(
    pop: np.ndarray, fit: np.ndarray,
    off: np.ndarray, off_fit: np.ndarray, n_elite: int = 1,
) -> tuple[np.ndarray, np.ndarray]:
    """Offspring replace the population; the n_elite best parents survive
    by overwriting the worst offspring (elitism, De Jong 1975)."""
    new_pop, new_fit = off.copy(), off_fit.copy()
    if n_elite > 0:
        elite = np.argpartition(-fit, n_elite - 1)[:n_elite]
        victims = np.argpartition(new_fit, n_elite - 1)[:n_elite]
        new_pop[victims], new_fit[victims] = pop[elite], fit[elite]
    return new_pop, new_fit


def mu_plus_lambda_replace(
    pop: np.ndarray, fit: np.ndarray,
    off: np.ndarray, off_fit: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """(mu+lambda): keep the best mu = len(pop) of parents and offspring pooled."""
    mu = pop.shape[0]
    all_pop = np.vstack((pop, off))
    all_fit = np.concatenate((fit, off_fit))
    keep = np.argpartition(-all_fit, mu - 1)[:mu]
    return all_pop[keep], all_fit[keep]


def mu_comma_lambda_replace(
    off: np.ndarray, off_fit: np.ndarray, mu: int,
) -> tuple[np.ndarray, np.ndarray]:
    """(mu,lambda): keep the best mu offspring; all parents die.

    Requires lambda >= mu (ES practice: lambda/mu in 4-7). Can lose the
    best-so-far by design — archive the incumbent externally.
    """
    keep = np.argpartition(-off_fit, mu - 1)[:mu]
    return off[keep], off_fit[keep]


def steady_state_insert(
    pop: np.ndarray, fit: np.ndarray, child: np.ndarray, child_fit: float,
) -> bool:
    """Replace-worst steady-state insertion with duplicate rejection.

    Rejects genotypes already present — without this check replace-worst
    floods the population with copies. Modifies pop/fit in place; returns
    True if the child was inserted.
    """
    if bool((pop == child).all(axis=1).any()):
        return False
    worst = int(np.argmin(fit))
    if child_fit <= fit[worst]:
        return False
    pop[worst], fit[worst] = child, child_fit
    return True


pop = np.array([[1, 1, 0], [0, 1, 1], [1, 0, 0], [0, 0, 0]], dtype=np.int8)
fit = np.array([8.0, 7.0, 3.0, 1.0])
off = np.array([[1, 1, 1], [0, 1, 0], [1, 0, 1], [0, 0, 1]], dtype=np.int8)
off_fit = np.array([9.0, 2.0, 6.0, 4.0])

print(sorted(generational_replace(pop, fit, off, off_fit, n_elite=1)[1]))
# Expected: [4.0, 6.0, 8.0, 9.0] — elite parent 8.0 replaced worst child 2.0
print(sorted(mu_plus_lambda_replace(pop, fit, off, off_fit)[1]))
# Expected: [6.0, 7.0, 8.0, 9.0] — best four of the pooled eight
print(sorted(mu_comma_lambda_replace(off, off_fit, mu=2)[1]))
# Expected: [6.0, 9.0] — best two offspring; parent 8.0 is forgotten
print(steady_state_insert(pop, fit, np.array([1, 1, 0], dtype=np.int8), 9.0))
# Expected: False — genotype already in the population (duplicate rejection)
print(steady_state_insert(pop, fit, np.array([1, 1, 1], dtype=np.int8), 9.0))
# Expected: True — replaces the worst (fitness 1.0) in place
```

## Worked Example: Selection-Pressure Experiment on One GA

The catalog's promise is that intensity predicts behavior. This experiment checks it on one fixed GA — generational with 1 elite, uniform crossover, 1/n bit-flip mutation — solving a penalized 0-1 knapsack, swapping only the parent-selection scheme. Two outputs per scheme: the mean realized intensity over the run (the measured knob) and the best objective over seeds (the consequence). Proportionate selection uses SUS sampling and a min-shift, which is the most favorable implementation it can get; it still loses because the shift plus the shrinking fitness spread destroy its pressure late in the run. Boltzmann uses a sigma-scaled geometric temperature schedule, so its intensity ramps from about 0.5 to effectively greedy.

```python
import numpy as np
import pandas as pd
from collections.abc import Callable

SelectFn = Callable[[np.ndarray, int, np.random.Generator, int], np.ndarray]


def make_knapsack(n_items: int, seed: int) -> tuple[np.ndarray, np.ndarray, float]:
    """Weakly correlated 0-1 knapsack: values tied to weights, capacity 50%."""
    rng = np.random.default_rng(seed)
    weights = rng.integers(5, 30, n_items).astype(float)
    values = weights + rng.integers(1, 15, n_items)
    return values, weights, 0.5 * float(weights.sum())


def fitness_pop(
    pop: np.ndarray, values: np.ndarray, weights: np.ndarray, capacity: float
) -> np.ndarray:
    """Penalized fitness of an (N, n) 0/1 population.

    The penalty rate exceeds every item's value/weight ratio, so no
    infeasible solution can outscore the feasible optimum.
    """
    rho = float((values / weights).max()) + 1.0
    return pop @ values - rho * np.maximum(pop @ weights - capacity, 0.0)


def sus_from_probs(p: np.ndarray, n: int, rng: np.random.Generator) -> np.ndarray:
    """SUS draw of n indices from a probability vector."""
    cum = np.cumsum(p)
    cum[-1] = 1.0
    idx = np.searchsorted(cum, (rng.random() + np.arange(n)) / n, side="right")
    return rng.permutation(idx)


def make_schemes(n_gens: int) -> dict[str, SelectFn]:
    """Five schemes under test, all with signature (fitness, n, rng, gen)."""

    def prop(f: np.ndarray, n: int, rng: np.random.Generator,
             gen: int) -> np.ndarray:
        shifted = f - f.min() + 1e-9               # proportionate needs > 0
        return sus_from_probs(shifted / shifted.sum(), n, rng)

    def lin_rank(f: np.ndarray, n: int, rng: np.random.Generator,
                 gen: int, s: float = 1.7) -> np.ndarray:
        m = f.size
        ranks = np.empty(m)
        ranks[np.argsort(f)] = np.arange(m)
        p = (2.0 - s) / m + 2.0 * ranks * (s - 1.0) / (m * (m - 1.0))
        return sus_from_probs(p, n, rng)

    def tournament(k: int) -> SelectFn:
        def sel(f: np.ndarray, n: int, rng: np.random.Generator,
                gen: int) -> np.ndarray:
            cand = rng.integers(0, f.size, size=(n, k))
            return cand[np.arange(n), np.argmax(f[cand], axis=1)]
        return sel

    def boltzmann(f: np.ndarray, n: int, rng: np.random.Generator,
                  gen: int) -> np.ndarray:
        t = 2.0 * (0.02 / 2.0) ** (gen / max(n_gens - 1, 1))   # 2.0 -> 0.02
        z = (f - f.max()) / (t * max(float(f.std()), 1e-9))    # sigma-scaled
        p = np.exp(z)
        return sus_from_probs(p / p.sum(), n, rng)

    return {"proportionate (SUS)": prop, "linear rank s=1.7": lin_rank,
            "tournament k=2": tournament(2), "tournament k=7": tournament(7),
            "Boltzmann t 2->0.02": boltzmann}


def run_ga(
    select: SelectFn, values: np.ndarray, weights: np.ndarray, capacity: float,
    n_pop: int = 100, n_gens: int = 150, seed: int = 0,
) -> tuple[float, float]:
    """Generational GA (uniform crossover, 1/n bit-flip, 1 elite).

    Returns (best penalized objective, mean realized selection intensity).
    """
    rng = np.random.default_rng(seed)
    n = values.size
    pop = (rng.random((n_pop, n)) < 0.5).astype(np.int8)
    fit = fitness_pop(pop, values, weights, capacity)
    best_i = int(np.argmax(fit))
    best_x, best_f = pop[best_i].copy(), float(fit[best_i])
    intensity = np.empty(n_gens)
    for gen in range(n_gens):
        parents = select(fit, n_pop, rng, gen)
        sd = float(fit.std())
        intensity[gen] = 0.0 if sd == 0 else (fit[parents].mean() - fit.mean()) / sd
        pa, pb = pop[parents[0::2]], pop[parents[1::2]]
        mask = rng.random(pa.shape) < 0.5
        off = np.vstack((np.where(mask, pa, pb), np.where(mask, pb, pa)))
        off ^= (rng.random(off.shape) < 1.0 / n).astype(np.int8)
        fit = fitness_pop(off, values, weights, capacity)
        victim = int(np.argmin(fit))               # 1-elite replacement
        off[victim], fit[victim] = best_x, best_f
        pop = off
        g = int(np.argmax(fit))
        if fit[g] > best_f:
            best_x, best_f = pop[g].copy(), float(fit[g])
    return best_f, float(intensity.mean())


values, weights, capacity = make_knapsack(60, seed=42)
rows = []
for name, sel in make_schemes(n_gens=150).items():
    out = np.array([run_ga(sel, values, weights, capacity, seed=s)
                    for s in range(5)])
    rows.append({"scheme": name,
                 "mean_best": round(float(out[:, 0].mean()), 1),
                 "std_best": round(float(out[:, 0].std()), 1),
                 "mean_intensity": round(float(out[:, 1].mean()), 2)})
print(pd.DataFrame(rows).to_string(index=False))
# Expected: measured mean_intensity orders the schemes
# proportionate < rank s=1.7 < tournament k=2 < tournament k=7 (about
# 0.33 / 0.39 / 0.55 / 0.96 here), with Boltzmann's per-generation intensity
# sweeping from ~0.5 to greedy as t anneals. mean_best follows the same
# order: proportionate trails with the largest std_best — its pressure
# collapses once the population's relative fitness spread narrows — while
# the high-pressure schemes win on this small, easy instance. On deceptive
# or rugged landscapes the high-pressure end pays for that speed with
# premature convergence; verify with the takeover harness before copying k=7.
```

Read the table the way you would tune a real run: if `mean_intensity` is below about 0.3 the scheme is barely selecting (raise s, k, or lower t); if it is above about 1.3 on a problem this small, expect seed-to-seed variance and premature convergence, and check the diversity diagnostics from diversity-and-population-management before trusting the best run.

## Worked Example: Replacement Strategies with Convergence Plots

Now hold parent selection fixed (tournament k=3) and swap only the survivor strategy, comparing at equal evaluation budget — the only fair x-axis, since (mu,lambda) here spends 2N evaluations per generation while steady-state spends 1 per step. The plot shows mean best-so-far over seeds with a min-max band per strategy.

```python
import numpy as np
import matplotlib.pyplot as plt


def make_knapsack(n_items: int, seed: int) -> tuple[np.ndarray, np.ndarray, float]:
    """Weakly correlated 0-1 knapsack instance."""
    rng = np.random.default_rng(seed)
    weights = rng.integers(5, 30, n_items).astype(float)
    values = weights + rng.integers(1, 15, n_items)
    return values, weights, 0.5 * float(weights.sum())


def fitness_pop(pop: np.ndarray, values: np.ndarray, weights: np.ndarray,
                capacity: float) -> np.ndarray:
    """Penalized fitness of an (N, n) 0/1 population."""
    rho = float((values / weights).max()) + 1.0
    return pop @ values - rho * np.maximum(pop @ weights - capacity, 0.0)


def make_offspring(pop: np.ndarray, fit: np.ndarray, n_off: int,
                   rng: np.random.Generator) -> np.ndarray:
    """n_off children: tournament k=3 parents, uniform crossover, 1/n bit-flip."""
    cand = rng.integers(0, fit.size, size=(2 * n_off, 3))
    parents = cand[np.arange(2 * n_off), np.argmax(fit[cand], axis=1)]
    pa, pb = pop[parents[:n_off]], pop[parents[n_off:]]
    child = np.where(rng.random(pa.shape) < 0.5, pa, pb)
    return child ^ (rng.random(child.shape) < 1.0 / pop.shape[1]).astype(np.int8)


def run(strategy: str, values: np.ndarray, weights: np.ndarray, capacity: float,
        seed: int, n_pop: int = 100, budget: int = 20_000,
        ) -> tuple[np.ndarray, np.ndarray]:
    """One GA run under a replacement strategy; returns (evals, best_so_far)."""
    rng = np.random.default_rng(seed)
    pop = (rng.random((n_pop, values.size)) < 0.5).astype(np.int8)
    fit = fitness_pop(pop, values, weights, capacity)
    evals, best = n_pop, float(fit.max())
    ev_log, best_log = [float(evals)], [best]
    while evals < budget:
        if strategy == "steady-state":
            child = make_offspring(pop, fit, 1, rng)[0]
            cf = float(fitness_pop(child[None, :], values, weights, capacity)[0])
            evals += 1
            if cf > fit.min() and not bool((pop == child).all(axis=1).any()):
                w = int(np.argmin(fit))
                pop[w], fit[w] = child, cf
        elif strategy == "mu,lambda":
            off = make_offspring(pop, fit, 2 * n_pop, rng)
            of = fitness_pop(off, values, weights, capacity)
            evals += 2 * n_pop
            keep = np.argpartition(-of, n_pop - 1)[:n_pop]
            pop, fit = off[keep], of[keep]
        else:
            off = make_offspring(pop, fit, n_pop, rng)
            of = fitness_pop(off, values, weights, capacity)
            evals += n_pop
            if strategy == "mu+lambda":
                allp = np.vstack((pop, off))
                allf = np.concatenate((fit, of))
                keep = np.argpartition(-allf, n_pop - 1)[:n_pop]
                pop, fit = allp[keep], allf[keep]
            elif strategy == "generational+1elite":
                v, e = int(np.argmin(of)), int(np.argmax(fit))
                off[v], of[v] = pop[e], fit[e]
                pop, fit = off, of
            else:                                   # pure generational
                pop, fit = off, of
        best = max(best, float(fit.max()))
        if evals % n_pop == 0 or evals >= budget:
            ev_log.append(float(evals))
            best_log.append(best)
    return np.array(ev_log), np.array(best_log)


values, weights, capacity = make_knapsack(60, seed=42)
strategies = ["generational", "generational+1elite", "steady-state",
              "mu+lambda", "mu,lambda"]
grid = np.arange(100, 20_001, 100, dtype=float)
fig, ax = plt.subplots(figsize=(7.0, 4.2))
summary: dict[str, float] = {}
for strat in strategies:
    curves = np.vstack([
        np.interp(grid, *run(strat, values, weights, capacity, seed=s))
        for s in range(5)])
    mean = curves.mean(axis=0)
    ax.plot(grid, mean, label=strat)
    ax.fill_between(grid, curves.min(axis=0), curves.max(axis=0), alpha=0.15)
    summary[strat] = round(float(mean[-1]), 1)
ax.set_xlabel("objective evaluations")
ax.set_ylabel("best penalized objective so far")
ax.legend(frameon=False)
fig.tight_layout()
fig.savefig("replacement_comparison.png", dpi=200)
print(summary)
# Expected: steady-state leads from the first checkpoints (it recycles good
# survivors after every single evaluation) and finishes best; mu+lambda is
# next fastest early but plateaus soonest — pure exploitation converges
# first; mu,lambda starts slower and closes the gap late, since its doubled
# lambda per generation buys exploration; pure generational trails the whole
# way because the best is repeatedly lost and rediscovered. The four
# pressure-bearing strategies end within ~0.3% of each other: on a static,
# noise-free instance of this size, replacement choice moves convergence
# speed far more than final quality.
```

Do not over-read a single instance: the ordering among the pressure-bearing strategies is budget- and problem-dependent, and on noisy objectives the comparison changes character entirely (naive elitism and the plus strategy lock in lucky evaluations; comma flushes them). The reusable artifact is the harness — equal-evaluation accounting, multiple seeds, best-so-far curves with bands — not this instance's specific ranking.

## Advanced Techniques

### Fitness scaling for proportionate selection

If you must keep a proportionate wheel (legacy code, probability-matching semantics), control its pressure with scaling (Goldberg 1989, *Genetic Algorithms in Search, Optimization and Machine Learning*, ch. 4). Linear scaling sets $f' = af + b$ with a, b chosen each generation so $\bar f' = \bar f$ and $f'_{\max} = C \bar f$, pinning the best individual's expected copies to C (typical C in 1.2-2.0, clipping negatives to zero). Sigma truncation uses $f' = \max(f - (\bar f - c\,\sigma_f),\, 0)$ with c in 1-3, which discards below-average stragglers and keeps the spread meaningful late in the run. Windowing subtracts the worst fitness of the last W generations. All three are per-generation monotone transforms — which is an admission that what you actually wanted was rank selection; switch when you can.

### Annealed and adaptive pressure schedules

Boltzmann selection makes pressure a schedule; the same idea applies to any scheme with a continuous knob: ramp linear-rank s from 1.1 to 2.0, or tournament p_win from 0.6 to 1.0, across the evaluation budget. The adaptive version closes the loop on a diversity signal instead of the clock: measure population entropy or mean pairwise distance each generation; if diversity falls below a floor, step pressure down (k=2, smaller s); if best-so-far stagnates for a window while diversity is high, step pressure up. Keep the controller coarse — two or three pressure levels with hysteresis — because intensity interacts with variation operators and a finely tuned controller overfits one instance. The diversity measurements and restart policies themselves are covered in diversity-and-population-management.

### Selection under noisy fitness

Noise of variance $\sigma_\epsilon^2$ added to true fitness of variance $\sigma_f^2$ discounts effective intensity by roughly $1/\sqrt{1 + \sigma_\epsilon^2/\sigma_f^2}$ (Miller & Goldberg 1996, "Genetic Algorithms, Selection Schemes, and the Varying Effects of Noise"). Countermeasures, in order of cheapness: enlarge the tournament (raises nominal intensity to compensate), average m re-evaluations per individual (cuts noise variance by m at m-fold cost — only worth it when selection errors are more expensive than evaluations), re-evaluate elites every generation so a lucky draw cannot squat in the population, and prefer comma replacement so overestimated individuals are flushed within one generation. Never compare a noisy champion against deterministic baselines without re-evaluation.

### Takeover-aware configuration

Use the takeover harness as a design tool, not a post-mortem. Given budget G generations, choose the scheme/knob whose measured takeover sits in [G/10, G/2]; for tournaments, solve $(\ln N + \ln\ln N)/\ln k \approx G/4$ for k as a starting point. Then account for replacement: replace-worst steady-state roughly doubles effective pressure over generational at the same parent scheme, and e elites add a floor of pressure that matters at small N. When N changes (parameter studies, parallel scaling), re-derive k — pressure that was right at N=50 is too low at N=1000 because takeover grows with log N while budgets usually grow linearly.

### Selection in ES and multi-objective frameworks

Evolution strategies implement pressure almost entirely at the survivor end: deterministic truncation with lambda/mu setting the intensity, and the comma variant mandatory once step sizes or covariances self-adapt, because a stale incumbent with an obsolete step size otherwise anchors the search (see evolution-strategies). Multi-objective EAs replace scalar fitness with a partial order: NSGA-II's binary tournament compares (nondomination rank, crowding distance) lexicographically and its (mu+lambda) environmental selection truncates by the same key — the same machinery as this skill, with a different comparator (see multi-objective-optimization).

## Practical Challenges

**Roulette selection stops selecting anything late in the run.** As the population converges, fitness values cluster, the coefficient of variation falls toward zero, and proportionate probabilities approach uniform — the algorithm degrades into random drift exactly when it should be exploiting. This is intrinsic, not a bug. Switch to rank or tournament, or apply sigma truncation if the wheel must stay.

**Fitness can be negative, and shifting it "fixes" the crash but changes the results.** Proportionate selection is not shift-invariant: adding a constant c rescales all probabilities toward uniform as c grows, so the shift constant is an undocumented pressure parameter. Penalized objectives make this acute because the effective shift varies per generation. Use rank or tournament, which are invariant under any monotone transform.

**The GA converges in 20 generations and idles for the remaining 480.** Compounded pressure: audit parent selection, survivor selection, and elitism together. Tournament k=5 plus replace-worst plus 5 elites at N=50 has a takeover time of 2-3 generations. Reduce one end at a time — k=2, replace-oldest instead of replace-worst, 1 elite — re-measuring takeover after each change, and add explicit diversity maintenance if the problem is deceptive.

**The steady-state population fills with copies of one genotype.** Replace-worst plus crossover of similar parents manufactures duplicates, and each duplicate further narrows parent selection. Reject exact duplicates at insertion (the `steady_state_insert` check, or a hash set of genotypes for large N), or replace the most-similar member instead of the worst — a crowding-flavored rule that preserves quality and diversity at once.

**(mu,lambda) keeps discarding the best solution found, and reviewers want elitism added.** Losing the incumbent is the point: it flushes stale self-adaptive parameters and overestimated noisy evaluations. Keep an external archive for reporting the best-ever solution — the archive does not feed back into the population. If the problem is static, noise-free, and has no self-adaptation, then yes: use (mu+lambda) instead, not comma-plus-patches.

**Tournament pressure steps are too coarse at small N.** k is an integer, so intensity jumps 0.56 to 0.85 to 1.16 with nothing in between, and at N=20 even k=2 takes over in a handful of generations. Use probabilistic tournaments (p_win in 0.6-0.9 interpolates below k=2), linear rank with a continuous s, or mix tournament sizes by drawing k per selection from {2, 3}.

**Elitism on a noisy objective enshrines lucky evaluations.** An elite kept by a +3-sigma noise draw is effectively unbeatable by honestly evaluated children, and the population anchors to a phantom. Re-evaluate elites every generation (or average a sliding window of re-evaluations), or drop elitism and switch to comma replacement with an external re-evaluated archive.

## Tools & Libraries

| Library | When to use | Note |
|---|---|---|
| numpy | every operator in this skill | `searchsorted` for wheels, `argpartition` for truncation, integer index arrays as the universal interface |
| DEAP | quick GA prototyping in Python | `tools.selTournament`, `selRoulette`, `selSUS`, `selBest`; roulette there carries the same positivity caveat as here |
| pymoo | research-grade single/multi-objective EAs | selection and survival are pluggable classes; NSGA-II survival = nondomination rank + crowding |
| inspyred | teaching and small experiments | clean `selectors`/`replacers` split mirroring this skill's two catalogs |
| pandas | experiment result tables | one row per (scheme, seed) run; pivot for the report table |
| matplotlib | convergence and takeover plots | best-so-far vs evaluations, band over seeds, as in the worked example |

## Output Format

A complete selection/replacement recommendation or implementation deliverable contains:

1. **Configuration summary** — chosen parent scheme and replacement strategy with every knob stated, plus the rationale tied to the anatomy tables: target intensity, predicted and measured takeover time, and the budget arithmetic (N, lambda, generations available).
2. **Code artifact** — the operator implementations (index-array interface, explicit `np.random.Generator`), slotted into the user's loop or the GA harness from the worked examples.
3. **Pressure report table** — one row per candidate configuration:

| scheme | knob | measured I | takeover (gens) | mean best (5 seeds) | std best | evals to 99% of final |
|---|---|---|---|---|---|---|
| tournament k=2 | k=2 | 0.55 | 8 | 1487.0 | 6.2 | 9,400 |
| linear rank | s=1.7 | 0.40 | 13 | 1484.2 | 5.1 | 11,800 |
| tournament k=7 | k=7 | 1.33 | 3 | 1480.6 | 14.8 | 4,100 |

4. **Convergence figure** — best-so-far versus evaluations, mean over seeds with min-max or interquartile band, one curve per configuration, saved as a vector or high-DPI file with the seed list and instance parameters in the caption.
5. **Reproducibility block** — instance generator parameters and seed, run seeds, library versions, and the exact commit or script that produced the table and figure.
6. **Caveats** — single-instance scope, noise assumptions, and which conclusions are expected to transfer (intensity ordering) versus which are instance-specific (the exact best-objective ranking).

## Questions to Ask

- Is the objective maximized or minimized, and can fitness values be negative, zero, or include penalty terms?
- What are the population size and the total evaluation budget — and is the budget in evaluations, generations, or wall-clock time?
- Which algorithm hosts the operator: plain GA, memetic with local search, ES with self-adaptation, EDA, or a multi-objective method?
- Is the codebase generational or steady-state today, and how costly would switching be?
- Is the fitness function noisy or stochastic, and how expensive is one evaluation?
- Have you observed premature convergence or stalling, and do you log any diversity measure?
- How disruptive are your variation operators (mutation rate, local search depth)?
- Do offspring evaluations run in parallel, and in what batch size?
- What reproducibility constraints exist — fixed seeds, multiple independent runs, statistical comparison against a baseline?

## Related Skills

- **genetic-algorithms** — when the question is the surrounding GA loop these operators plug into (encoding, crossover, mutation, population sizing), not the selection machinery itself
- **diversity-and-population-management** — when pressure is tuned correctly but the population still converges prematurely and needs explicit diversity measurement, sharing, crowding, or restarts
- **evolution-strategies** — when (mu+lambda)/(mu,lambda) appear in their native ES context with self-adaptive step sizes and continuous or mixed-integer search spaces
- **multi-objective-optimization** — when selection must rank by Pareto dominance and crowding distance instead of scalar fitness, as in NSGA-II's crowded tournament and environmental selection
