---
name: optuna-hyperparameter-tuning
description: When the user wants to tune metaheuristic or solver parameters with Optuna, including search-space definition, TPE sampling, pruning weak configurations early, multi-instance objectives (mean/median over an instance set), and held-out validation against overtuning. Also use when the user mentions "Optuna," "hyperparameter tuning," "parameter tuning," "tune metaheuristic," "TPE sampler," "algorithm configuration," or when reported results hinge on hand-picked parameter values. For statistical comparison of tuned configurations, see algorithm-benchmarking-statistics; for deciding which parameters an algorithm should expose, see metaheuristic-design-principles.
---

# Optuna Hyperparameter Tuning for Optimization Algorithms

You are an expert in automated algorithm configuration with Optuna. This skill covers tuning the
parameters of metaheuristics and MIP solvers: defining search spaces, choosing samplers (TPE,
CMA-ES, NSGA-II), building multi-instance objectives, pruning bad configurations early,
persisting and parallelizing studies, and validating tuned configurations on held-out instances.
Use the pattern catalog below to set up tuning runs that produce parameters which generalize,
not parameters that memorize the training instances.

## Initial Assessment

Establish these facts before writing any tuning code:

- **What is being tuned?** A metaheuristic (SA, GA, ALNS), a MIP solver (Gurobi, CP-SAT), or a
  hybrid? The target determines the objective metric and the cost per evaluation.
- **Parameter inventory.** List every parameter with its type (continuous, integer, categorical,
  conditional), a plausible range, and the current default. Fewer than 10 parameters is the
  normal case; more than 15 suggests the algorithm design should be simplified first.
- **Objective metric.** Solution quality at a fixed budget? Time to proven optimality? Gap at a
  time limit? Anytime behavior? The metric must match how the algorithm will be used and
  reported later.
- **Cost per trial.** One trial = (instances per trial) x (seeds per instance) x (single-run
  budget). Compute the total wall-clock cost of the tuning run before starting it.
- **Instance set.** How many training instances exist? Are they representative of the instances
  used in the final experiments? Is a train/test split possible (it should be)?
- **Stochasticity.** Is the tuned algorithm randomized? If yes, plan multiple seeds per instance
  inside every trial; a single seed makes the objective so noisy that TPE chases luck.
- **Tuning budget.** How many trials are affordable? Under 30 trials, model-based sampling barely
  beats random search; plan the budget before choosing the sampler.
- **Hardware.** Single machine or cluster? Parallel trials need shared storage (SQLite is fine
  for a handful of workers, JournalStorage or an RDBMS beyond that).
- **Reproducibility requirements.** Will the tuning protocol be described in a paper? Then fix
  and record: sampler seed, instance list, seed lists, per-run budgets, and the Optuna version.
- **Reporting obligation.** Fair comparisons require that every compared algorithm receives the
  same tuning effort (same budget, same protocol). Decide this now, not after the experiments.

## The Algorithm Configuration Problem

Offline parameter tuning is itself an optimization problem. Given an algorithm $A$ with
parameter space $\Theta$, a distribution $\mathcal{D}$ over problem instances, and a cost
function $c(\theta, \pi, s)$ (the result of running $A(\theta)$ on instance $\pi$ with random
seed $s$), the goal is

$$
\theta^{*} \in \arg\min_{\theta \in \Theta} \;
\mathbb{E}_{\pi \sim \mathcal{D}, \; s} \big[ \, c(\theta, \pi, s) \, \big].
$$

Three properties make this problem awkward and drive every pattern in this skill:

1. **The expectation is approximated by a finite sample** of training instances and seeds. The
   empirical minimizer overfits this sample exactly like a machine-learning model overfits a
   training set. Generalization is checked with held-out instances, never assumed.
2. **Evaluating one $\theta$ is expensive** (a full algorithm run per instance per seed), so the
   tuner must be sample-efficient: model-based sampling (TPE) and early stopping of bad
   configurations (pruning, racing) both attack this.
3. **The evaluation is noisy** for randomized algorithms, so single observations of
   $c(\theta, \pi, s)$ must never be trusted; aggregate over seeds and instances.

### Families of tuning approaches

| Approach | Mechanism | Use when |
|---|---|---|
| Manual / factorial screening | Vary one or two parameters on a grid by hand | Early design phase; understanding sensitivity, not optimizing |
| Grid search | Exhaustive Cartesian product | At most 2-3 parameters with few levels each; never beyond |
| Random search | Uniform sampling of $\Theta$ | Cheap baseline; surprisingly strong (Bergstra & Bengio 2012, "Random Search for Hyper-Parameter Optimization") |
| Model-based (TPE, GP, SMAC) | Fit a surrogate of $c(\theta)$, sample promising regions | 30+ trials affordable; mixed/conditional spaces; this is Optuna's default mode |
| Racing (F-Race, irace) | Evaluate instance-by-instance, eliminate losers with statistical tests | Many instances, heterogeneous instance sets; see the irace subsection |
| Self-adaptation / parameter control | Adapt parameters online during one run | Step sizes and mutation rates; complements offline tuning (covered in evolution-strategies) |

### How TPE works, in two sentences

The Tree-structured Parzen Estimator (Bergstra, Bardenet, Bengio & Kegl 2011, "Algorithms for
Hyper-Parameter Optimization") splits observed trials into a good set (cost below a quantile
$\gamma$) and a bad set, fits kernel-density estimates $l(\theta)$ over the good and $g(\theta)$
over the bad configurations, and proposes the candidate maximizing $l(\theta)/g(\theta)$ — the
configuration most characteristic of good trials and least characteristic of bad ones. It handles
continuous, integer, log-scaled, and categorical dimensions natively, which is exactly the mix
that metaheuristic parameter spaces have.

### Sampler selection

| Sampler | Search space | Notes |
|---|---|---|
| `TPESampler` | Mixed, conditional | Default choice; set `multivariate=True` to model parameter interactions |
| `RandomSampler` | Any | Baseline and sanity check; trivially parallel |
| `CmaEsSampler` | Continuous/integer only | Strongest on purely numeric spaces; no categoricals or conditionals |
| `NSGAIISampler` | Mixed | Multi-objective studies (quality vs. time) |
| `GridSampler` | Small finite | Exhaustive enumeration when the space is tiny |

### Budgeting rule of thumb

Total cost = trials x instances/trial x seeds/instance x run budget. As a floor, give the tuner
10-20 trials per tuned parameter, after the `n_startup_trials` random warm-up (default 10).
Worked example: 5 parameters, 6 training instances, 2 seeds, 30 s per run, 100 trials
= 100 x 6 x 2 x 30 s = 10 hours sequential. If that is too much, cut in this order: (1) per-run
budget (tune on a reduced budget, validate on the real one), (2) seeds via pruning (Pattern 4),
(3) instance count — never below 4-5, or the tuned configuration will be instance-specific.

## Pattern Catalog: Search Spaces and Objectives

Each pattern below is a self-contained, runnable block: motivation, code, pitfall. Helper
functions are repeated where needed so every block stands alone.

### Pattern 1 — Minimal tuning loop for a metaheuristic

The base pattern: an `objective(trial)` function that (a) draws a configuration from the search
space, (b) runs the algorithm under that configuration on training data over several seeds,
(c) returns an aggregate score. Here: simulated annealing for the quadratic assignment problem
(QAP), with an O(n) swap-delta evaluation so the tuning run itself is not needlessly slow.

```python
import numpy as np
import optuna


def random_qap(n: int, seed: int) -> tuple[np.ndarray, np.ndarray]:
    """Random symmetric QAP instance (flow, distance) with zero diagonals."""
    rng = np.random.default_rng(seed)
    flow = np.triu(rng.integers(0, 100, (n, n)), k=1)
    dist = np.triu(rng.integers(1, 50, (n, n)), k=1)
    return flow + flow.T, dist + dist.T


def qap_cost(perm: np.ndarray, flow: np.ndarray, dist: np.ndarray) -> float:
    """Cost of assigning facility i to location perm[i]."""
    return float(np.sum(flow * dist[np.ix_(perm, perm)]))


def swap_delta(perm: np.ndarray, flow: np.ndarray, dist: np.ndarray,
               r: int, s: int) -> float:
    """O(n) cost change for swapping positions r and s (symmetric QAP)."""
    mask = np.ones(len(perm), dtype=bool)
    mask[[r, s]] = False
    df = flow[r, mask] - flow[s, mask]
    dd = dist[perm[s], perm[mask]] - dist[perm[r], perm[mask]]
    return 2.0 * float(df @ dd)


def sa_qap(flow: np.ndarray, dist: np.ndarray, t0: float, alpha: float,
           moves_per_temp: int, budget: int, seed: int) -> float:
    """Simulated annealing for QAP: swap moves, geometric cooling."""
    rng = np.random.default_rng(seed)
    perm = rng.permutation(len(flow))
    cost = qap_cost(perm, flow, dist)
    best, temp, evals = cost, t0, 0
    while evals < budget:
        for _ in range(min(moves_per_temp, budget - evals)):
            r, s = rng.choice(len(perm), size=2, replace=False)
            delta = swap_delta(perm, flow, dist, r, s)
            evals += 1
            if delta < 0 or rng.random() < np.exp(-delta / temp):
                perm[[r, s]] = perm[[s, r]]
                cost += delta
                best = min(best, cost)
        temp = max(alpha * temp, 1e-9)
    return best


def objective(trial: optuna.Trial) -> float:
    """Mean best cost of SA over 3 seeds on one training instance."""
    t0 = trial.suggest_float("t0", 1.0, 1e4, log=True)
    alpha = trial.suggest_float("alpha", 0.80, 0.999)
    moves = trial.suggest_int("moves_per_temp", 10, 1000, log=True)
    flow, dist = random_qap(25, seed=0)
    costs = [sa_qap(flow, dist, t0, alpha, moves, budget=30_000, seed=s)
             for s in (1, 2, 3)]
    return float(np.mean(costs))


optuna.logging.set_verbosity(optuna.logging.WARNING)
study = optuna.create_study(direction="minimize",
                            sampler=optuna.samplers.TPESampler(seed=42))
study.optimize(objective, n_trials=50)
print(study.best_params)
print(round(study.best_value, 1))
# Expected: a (t0, alpha, moves_per_temp) combination whose mean cost over the
# three seeds beats the default (t0=100, alpha=0.95, moves=100) by a clear margin.
```

Search-space conventions that matter: use `log=True` for scale-type parameters (temperatures,
penalty coefficients, mutation rates, population sizes) so TPE searches orders of magnitude
uniformly; use `step=` on integers when only multiples make sense; keep ranges generous on the
first run, then narrow once `study.trials_dataframe()` shows where good trials cluster.

**Pitfall:** This block tunes on a *single* instance, which is acceptable only as a teaching
device. Parameters tuned on one instance encode that instance's quirks (size, density, cost
scale) and routinely lose to defaults elsewhere; real tuning uses Pattern 3 (multi-instance
objective) plus Pattern 6 (held-out validation). Equally common: returning the cost of a single
seed — TPE's good/bad split is then contaminated by luck, and the "best trial" is often just the
luckiest seed.

### Pattern 2 — Conditional search spaces

Metaheuristic spaces are rarely flat: choosing the crossover operator activates that operator's
own parameters; choosing penalty-based constraint handling activates a penalty coefficient.
Optuna supports this directly — call `suggest_*` inside `if` branches. Sample a parameter only
when the configuration actually uses it, and give branch-specific parameters distinct names.

```python
import numpy as np
import optuna


def ga_knapsack(values: np.ndarray, weights: np.ndarray, capacity: float,
                pop_size: int, crossover: str, swap_prob: float, mode: str,
                penalty_coef: float, mutation_rate: float,
                generations: int, seed: int) -> float:
    """Vectorized binary GA for 0-1 knapsack; returns best feasible value."""
    rng = np.random.default_rng(seed)
    n = len(values)
    drop_order = np.argsort(values / weights)  # worst ratio first

    def repair(pop: np.ndarray) -> np.ndarray:
        for ind in pop:  # rows are views; edits write through
            load = float(ind @ weights)
            for j in drop_order:
                if load <= capacity:
                    break
                if ind[j]:
                    ind[j] = False
                    load -= weights[j]
        return pop

    pop = rng.random((pop_size, n)) < 0.5
    if mode == "repair":
        pop = repair(pop)
    best = 0.0
    for _ in range(generations):
        load = pop @ weights
        value = pop @ values
        excess = np.maximum(0.0, load - capacity)
        fit = value - (penalty_coef * excess if mode == "penalty" else 0.0)
        feasible = load <= capacity
        if feasible.any():
            best = max(best, float(value[feasible].max()))
        a = rng.integers(0, pop_size, size=pop_size)  # binary tournament
        b = rng.integers(0, pop_size, size=pop_size)
        parents = pop[np.where(fit[a] >= fit[b], a, b)]
        half = pop_size // 2
        p1, p2 = parents[:half], parents[half:2 * half]
        if crossover == "uniform":
            mask = rng.random((half, n)) < swap_prob
        else:  # one_point
            cut = rng.integers(1, n, size=(half, 1))
            mask = np.arange(n) >= cut
        pop = np.vstack([np.where(mask, p2, p1), np.where(mask, p1, p2)])
        pop = pop ^ (rng.random(pop.shape) < mutation_rate)
        if mode == "repair":
            pop = repair(pop)
    return best


rng = np.random.default_rng(0)
VALUES = rng.integers(10, 100, 50).astype(float)
WEIGHTS = rng.integers(5, 50, 50).astype(float)
CAPACITY = 0.4 * float(WEIGHTS.sum())


def objective(trial: optuna.Trial) -> float:
    """Conditional space: operator choice activates operator parameters."""
    pop_size = trial.suggest_int("pop_size", 20, 200, step=20)
    mutation_rate = trial.suggest_float("mutation_rate", 1e-3, 0.1, log=True)
    crossover = trial.suggest_categorical("crossover", ["uniform", "one_point"])
    swap_prob = (trial.suggest_float("uniform_swap_prob", 0.1, 0.5)
                 if crossover == "uniform" else 0.5)
    mode = trial.suggest_categorical("mode", ["penalty", "repair"])
    coef = (trial.suggest_float("penalty_coef", 1.0, 100.0, log=True)
            if mode == "penalty" else 0.0)
    vals = [ga_knapsack(VALUES, WEIGHTS, CAPACITY, pop_size, crossover,
                        swap_prob, mode, coef, mutation_rate,
                        generations=100, seed=s) for s in (1, 2)]
    return float(np.mean(vals))


optuna.logging.set_verbosity(optuna.logging.WARNING)
study = optuna.create_study(direction="maximize",
                            sampler=optuna.samplers.TPESampler(seed=13))
study.optimize(objective, n_trials=40)
print(study.best_params, round(study.best_value, 1))
# Expected: on this loosely constrained instance, repair-based handling with a
# moderate mutation rate typically wins; the conditional penalty_coef appears
# in best_params only when mode == "penalty" was selected.
```

**Pitfall:** Never reuse one parameter name across branches (e.g., a generic `"prob"` sampled
under both crossover choices). Optuna treats parameters by name; merging two semantically
different quantities into one distribution corrupts TPE's density model. Also know that with the
default univariate TPE, each conditional parameter is modeled only from the trials where it was
sampled — fine in principle, but with many branches each branch gets few observations. For
heavily conditional spaces, set `TPESampler(multivariate=True, group=True)` (see Advanced
Techniques) or consider irace, which was designed for such spaces.

### Pattern 3 — Multi-instance objective with gap normalization

A configuration must work across the instance distribution, so each trial evaluates a *set* of
training instances. Raw objective values must not be averaged across instances of different size
or cost scale — the largest instance would dominate the mean. Normalize each run to a relative
gap against a per-instance reference cost (best known value, or the best of a few
default-configuration runs), then aggregate.

```python
import numpy as np
import optuna


def random_qap(n: int, seed: int) -> tuple[np.ndarray, np.ndarray]:
    """Random symmetric QAP instance (flow, distance) with zero diagonals."""
    rng = np.random.default_rng(seed)
    flow = np.triu(rng.integers(0, 100, (n, n)), k=1)
    dist = np.triu(rng.integers(1, 50, (n, n)), k=1)
    return flow + flow.T, dist + dist.T


def sa_qap(flow: np.ndarray, dist: np.ndarray, t0: float, alpha: float,
           steps: int, seed: int) -> float:
    """Compact SA for QAP: swap moves, per-move geometric cooling."""
    rng = np.random.default_rng(seed)
    perm = rng.permutation(len(flow))
    cost = float(np.sum(flow * dist[np.ix_(perm, perm)]))
    best, temp = cost, t0
    for _ in range(steps):
        r, s = rng.choice(len(perm), size=2, replace=False)
        cand = perm.copy()
        cand[[r, s]] = cand[[s, r]]
        new = float(np.sum(flow * dist[np.ix_(cand, cand)]))
        if new < cost or rng.random() < np.exp((cost - new) / temp):
            perm, cost = cand, new
            best = min(best, cost)
        temp = max(alpha * temp, 1e-12)
    return best


TRAIN = [random_qap(n, seed) for n, seed in [(15, 1), (20, 2), (25, 3), (30, 4)]]
SEEDS = (101, 102)
STEPS = 4000

# Per-instance reference: best of five default-configuration runs.
REF = [min(sa_qap(f, d, t0=200.0, alpha=0.999, steps=STEPS, seed=s)
           for s in range(5)) for f, d in TRAIN]


def objective(trial: optuna.Trial) -> float:
    """Mean relative gap to reference over all training instances and seeds."""
    t0 = trial.suggest_float("t0", 1.0, 1e4, log=True)
    alpha = trial.suggest_float("alpha", 0.990, 0.99999)
    gaps = []
    for (flow, dist), ref in zip(TRAIN, REF):
        for s in SEEDS:
            cost = sa_qap(flow, dist, t0, alpha, STEPS, s)
            gaps.append((cost - ref) / ref)
    return float(np.mean(gaps))


optuna.logging.set_verbosity(optuna.logging.WARNING)
study = optuna.create_study(direction="minimize",
                            sampler=optuna.samplers.TPESampler(seed=21))
study.optimize(objective, n_trials=40)
print(study.best_params, round(study.best_value, 4))
# Expected: best mean gap at or below 0.0 -- the tuned configuration matches or
# beats the default-configuration reference across all four training instances.
```

Aggregation choice: the **mean** gap rewards configurations that are good everywhere but is
sensitive to one catastrophic instance; the **median** is robust to outliers but can hide a
configuration that fails on a minority of instances. For solver runtimes use the shifted
geometric mean (Pattern 7). When instance hardness varies wildly, report both mean and worst-case
gap, and consider tuning on the mean while monitoring the max.

**Pitfall:** Averaging raw costs instead of gaps is the classic error: a configuration that
shaves 2% off the n=30 instance moves the mean more than one that shaves 20% off the n=15
instance, so the tuner silently specializes to the biggest instance. The second error is a
reference set that is too weak (e.g., a single random-restart cost): gaps then compress toward
large negative values and differences between good configurations become invisible. Spend real
compute on the references once; they are reused by every trial.

## Pattern Catalog: Pruning, Storage, and Parallel Studies

### Pattern 4 — Instance-wise pruning (racing on a budget)

When each trial evaluates several instances sequentially, a configuration that is clearly bad
after two instances should not waste budget on the remaining ones. Report the running aggregate
after each instance with `trial.report(value, step)` and stop when `trial.should_prune()` fires.
This is a pragmatic, model-based cousin of racing methods like F-Race (Birattari, Stuetzle,
Paquete & Varrentrapp 2002, "A Racing Algorithm for Configuring Metaheuristics").

```python
import numpy as np
import optuna


def random_qap(n: int, seed: int) -> tuple[np.ndarray, np.ndarray]:
    """Random symmetric QAP instance (flow, distance) with zero diagonals."""
    rng = np.random.default_rng(seed)
    flow = np.triu(rng.integers(0, 100, (n, n)), k=1)
    dist = np.triu(rng.integers(1, 50, (n, n)), k=1)
    return flow + flow.T, dist + dist.T


def sa_qap(flow: np.ndarray, dist: np.ndarray, t0: float, alpha: float,
           steps: int, seed: int) -> float:
    """Compact SA for QAP: swap moves, per-move geometric cooling."""
    rng = np.random.default_rng(seed)
    perm = rng.permutation(len(flow))
    cost = float(np.sum(flow * dist[np.ix_(perm, perm)]))
    best, temp = cost, t0
    for _ in range(steps):
        r, s = rng.choice(len(perm), size=2, replace=False)
        cand = perm.copy()
        cand[[r, s]] = cand[[s, r]]
        new = float(np.sum(flow * dist[np.ix_(cand, cand)]))
        if new < cost or rng.random() < np.exp((cost - new) / temp):
            perm, cost = cand, new
            best = min(best, cost)
        temp = max(alpha * temp, 1e-12)
    return best


TRAIN = [random_qap(n, seed) for n, seed in [(15, 1), (20, 2), (25, 3), (30, 4)]]
SEEDS = (101, 102)
STEPS = 4000
REF = [min(sa_qap(f, d, t0=200.0, alpha=0.999, steps=STEPS, seed=s)
           for s in range(5)) for f, d in TRAIN]


def objective(trial: optuna.Trial) -> float:
    """Evaluate instances in a FIXED order; prune on the running mean gap."""
    t0 = trial.suggest_float("t0", 1.0, 1e4, log=True)
    alpha = trial.suggest_float("alpha", 0.990, 0.99999)
    gaps: list[float] = []
    for step, ((flow, dist), ref) in enumerate(zip(TRAIN, REF)):
        for s in SEEDS:
            cost = sa_qap(flow, dist, t0, alpha, STEPS, s)
            gaps.append((cost - ref) / ref)
        trial.report(float(np.mean(gaps)), step)
        if trial.should_prune():
            raise optuna.TrialPruned()
    return float(np.mean(gaps))


optuna.logging.set_verbosity(optuna.logging.WARNING)
study = optuna.create_study(
    direction="minimize",
    sampler=optuna.samplers.TPESampler(seed=11),
    pruner=optuna.pruners.MedianPruner(n_startup_trials=10, n_warmup_steps=1),
)
study.optimize(objective, n_trials=60)
n_pruned = sum(t.state == optuna.trial.TrialState.PRUNED for t in study.trials)
print(round(study.best_value, 4), n_pruned)
# Expected: roughly a third to half of the 60 trials are pruned after 2-3 of
# the 4 instances, cutting total tuning time substantially with little or no
# loss in best_value compared to the unpruned study of Pattern 3.
```

Pruner choice: `MedianPruner` (prune if worse than the median of completed trials at the same
step) is the safe default for instance-wise evaluation. `SuccessiveHalvingPruner` and
`HyperbandPruner` (Jamieson & Talwalkar 2016, successive halving; Li et al. 2018, Hyperband)
allocate budget more aggressively and pay off when trials report many steps (e.g., one step per
instance-seed pair, or per restart of an anytime algorithm).

**Pitfall:** Intermediate values are only comparable across trials if every trial sees the
instances in the *same fixed order* — never shuffle the instance list per trial. Order the
instances from cheapest to most expensive so pruning saves the most time, but be aware this
biases early pruning decisions toward performance on small instances; `n_warmup_steps>=1` and a
conservative `n_startup_trials` protect against killing configurations that only shine on the
larger instances. Pruning also interacts with noise: with one seed per instance, the running mean
is so noisy that good configurations get pruned on bad luck.

### Pattern 5 — Persistent storage, resuming, and parallel workers

Tuning runs of hours must survive crashes and should use idle cores. Back the study with
persistent storage; any number of worker processes can then attach to the same study by name and
call `optimize` concurrently. Each worker process runs this same script.

```python
import numpy as np
import optuna


def one_plus_one_es(sigma0: float, adapt: float, seed: int) -> float:
    """(1+1)-ES on a 10-D sphere; returns best objective after 500 evaluations."""
    rng = np.random.default_rng(seed)
    x = rng.normal(0.0, 1.0, 10)
    fx = float(x @ x)
    sigma = sigma0
    for _ in range(500):
        y = x + sigma * rng.normal(0.0, 1.0, 10)
        fy = float(y @ y)
        if fy <= fx:
            x, fx, sigma = y, fy, sigma * adapt
        else:
            sigma /= adapt ** 0.25
    return fx


def objective(trial: optuna.Trial) -> float:
    """Tune the ES step-size schedule; mean final quality over 3 seeds."""
    sigma0 = trial.suggest_float("sigma0", 1e-3, 10.0, log=True)
    adapt = trial.suggest_float("adapt", 1.01, 2.0)
    return float(np.mean([one_plus_one_es(sigma0, adapt, s) for s in (1, 2, 3)]))


optuna.logging.set_verbosity(optuna.logging.WARNING)
study = optuna.create_study(
    study_name="es_sphere_v1",
    storage="sqlite:///es_sphere.db",   # file-backed; resumable
    direction="minimize",
    sampler=optuna.samplers.TPESampler(seed=7, multivariate=True),
    load_if_exists=True,                # attach instead of failing if it exists
)
study.optimize(objective, n_trials=25)

df = study.trials_dataframe(attrs=("number", "value", "params", "state"))
df.to_csv("es_sphere_trials.csv", index=False)
print(len(study.trials), study.best_params)
# Expected: re-running this script continues the same study (trial count grows
# by 25 each run); best sigma0 is moderate (around 0.5-3) with adapt near
# 1.2-1.6, the classic 1/5th-success-rule regime.
```

**Pitfall:** SQLite serializes writes through file locks; with more than roughly 4-8 concurrent
workers (or a network filesystem) you will see `database is locked` errors. Switch to
`optuna.storages.JournalStorage` with a journal file backend, or a PostgreSQL/MySQL storage URL,
for larger worker counts. Second trap: giving every worker the same `TPESampler(seed=7)` makes
workers propose near-identical configurations in parallel. Either give each worker a different
sampler seed (and accept that exact reproducibility now requires replaying the stored study) or
set `constant_liar=True` in `TPESampler` so concurrent workers are steered apart. Finally, never
run two *different* objective definitions against the same `study_name` — the parameter records
will be inconsistent and the surrogate model meaningless.

## Pattern Catalog: Validation and Solver Tuning

### Pattern 6 — Train/test instance split and the overtuning check

Tuning is learning, so it is evaluated like learning: split the instance set, tune on the
training part, and report performance of the *single chosen configuration* on the held-out part
with fresh seeds. The gap between training score and test score is the measured overtuning bias.
Hooker (1995, "Testing Heuristics: We Have It All Wrong") made the underlying point early:
results demonstrated on the development set alone are not evidence.

```python
import numpy as np
import optuna


def random_qap(n: int, seed: int) -> tuple[np.ndarray, np.ndarray]:
    """Random symmetric QAP instance (flow, distance) with zero diagonals."""
    rng = np.random.default_rng(seed)
    flow = np.triu(rng.integers(0, 100, (n, n)), k=1)
    dist = np.triu(rng.integers(1, 50, (n, n)), k=1)
    return flow + flow.T, dist + dist.T


def sa_qap(flow: np.ndarray, dist: np.ndarray, t0: float, alpha: float,
           steps: int, seed: int) -> float:
    """Compact SA for QAP: swap moves, per-move geometric cooling."""
    rng = np.random.default_rng(seed)
    perm = rng.permutation(len(flow))
    cost = float(np.sum(flow * dist[np.ix_(perm, perm)]))
    best, temp = cost, t0
    for _ in range(steps):
        r, s = rng.choice(len(perm), size=2, replace=False)
        cand = perm.copy()
        cand[[r, s]] = cand[[s, r]]
        new = float(np.sum(flow * dist[np.ix_(cand, cand)]))
        if new < cost or rng.random() < np.exp((cost - new) / temp):
            perm, cost = cand, new
            best = min(best, cost)
        temp = max(alpha * temp, 1e-12)
    return best


SIZES_SEEDS = [(15, 1), (20, 2), (25, 3), (30, 4), (18, 5), (22, 6), (26, 7), (28, 8)]
ALL = [random_qap(n, s) for n, s in SIZES_SEEDS]
TRAIN, TEST = ALL[:5], ALL[5:]
STEPS = 4000


def references(instances: list[tuple[np.ndarray, np.ndarray]]) -> list[float]:
    """Best of five default-configuration runs per instance."""
    return [min(sa_qap(f, d, 200.0, 0.999, STEPS, s) for s in range(5))
            for f, d in instances]


REF_TRAIN, REF_TEST = references(TRAIN), references(TEST)


def evaluate(config: dict, instances: list, refs: list[float],
             seeds: tuple[int, ...]) -> float:
    """Mean relative gap of a configuration over instances x seeds."""
    gaps = [(sa_qap(f, d, config["t0"], config["alpha"], STEPS, s) - ref) / ref
            for (f, d), ref in zip(instances, refs) for s in seeds]
    return float(np.mean(gaps))


def objective(trial: optuna.Trial) -> float:
    config = {"t0": trial.suggest_float("t0", 1.0, 1e4, log=True),
              "alpha": trial.suggest_float("alpha", 0.990, 0.99999)}
    return evaluate(config, TRAIN, REF_TRAIN, seeds=(101, 102))


optuna.logging.set_verbosity(optuna.logging.WARNING)
study = optuna.create_study(direction="minimize",
                            sampler=optuna.samplers.TPESampler(seed=3))
study.optimize(objective, n_trials=60)

DEFAULT = {"t0": 200.0, "alpha": 0.999}
TEST_SEEDS = (501, 502, 503)  # disjoint from the tuning seeds
print("train gap, tuned:  ", round(study.best_value, 4))
print("test  gap, tuned:  ", round(evaluate(study.best_params, TEST, REF_TEST, TEST_SEEDS), 4))
print("test  gap, default:", round(evaluate(DEFAULT, TEST, REF_TEST, TEST_SEEDS), 4))
# Expected: the tuned configuration beats the default on the test set, but its
# test gap is worse than its train gap; that difference is the overtuning bias
# and should be reported, not hidden.
```

**Pitfall:** The number printed by `study.best_value` is an *optimistically biased* estimate —
it is the minimum of 60 noisy observations (the winner's curse). Never report it as the
performance of the tuned algorithm. Re-run the chosen configuration on test instances with seeds
that were never used during tuning. Also keep the split honest: if test instances come from a
different size range or generator than training instances, you are measuring extrapolation, not
generalization — sometimes that is exactly what you want to measure, but say so. For the final
tuned-vs-default comparison across instances, use paired statistical tests as described in
algorithm-benchmarking-statistics.

### Pattern 7 — Tuning Gurobi parameters for time-to-optimality

Solver parameter tuning has a different objective shape: minimize runtime to proven optimality at
a time limit, with a penalty for timeouts (PAR2 = twice the limit, a convention from the
algorithm-configuration literature, e.g., Hutter, Hoos & Leyton-Brown 2011, "Sequential
Model-Based Optimization for General Algorithm Configuration"). Aggregate runtimes with the
shifted geometric mean, the standard in MIP benchmarking (Achterberg 2007, "Constraint Integer
Programming").

```python
import gurobipy as gp
import numpy as np
import optuna
from gurobipy import GRB


def random_mkp(n: int, m: int, seed: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Correlated multidimensional knapsack instance (Chu-Beasley style)."""
    rng = np.random.default_rng(seed)
    w = rng.integers(1, 1000, size=(m, n))
    cap = (0.25 * w.sum(axis=1)).astype(np.int64)
    profit = (w.mean(axis=0) / 2 + rng.integers(1, 500, size=n)).astype(np.int64)
    return profit, w, cap


def add_capacity_constraints(model: gp.Model, x: gp.tupledict,
                             w: np.ndarray, cap: np.ndarray) -> None:
    """One knapsack constraint per resource dimension."""
    m, n = w.shape
    for k in range(m):
        model.addConstr(
            gp.quicksum(int(w[k, j]) * x[j] for j in range(n)) <= int(cap[k]),
            name=f"capacity[{k}]",
        )


def par2_runtime(profit: np.ndarray, w: np.ndarray, cap: np.ndarray,
                 params: dict, time_limit: float) -> float:
    """Runtime to proven optimality; PAR2 penalty (2x limit) on timeout."""
    model = gp.Model("mkp")
    model.Params.OutputFlag = 0
    model.Params.Threads = 1          # deterministic-ish, fair timing
    model.Params.TimeLimit = time_limit
    for name, value in params.items():
        model.setParam(name, value)
    n = len(profit)
    x = model.addVars(n, vtype=GRB.BINARY, name="x")
    add_capacity_constraints(model, x, w, cap)
    model.setObjective(gp.quicksum(int(profit[j]) * x[j] for j in range(n)),
                       GRB.MAXIMIZE)
    model.optimize()
    if model.Status == GRB.OPTIMAL:
        return model.Runtime
    return 2.0 * time_limit


def shifted_geomean(times: list[float], shift: float = 1.0) -> float:
    """Shifted geometric mean, the standard MIP runtime aggregate."""
    arr = np.asarray(times, dtype=float) + shift
    return float(np.exp(np.log(arr).mean()) - shift)


TRAIN = [random_mkp(n=120, m=10, seed=s) for s in (1, 2, 3, 4)]


def objective(trial: optuna.Trial) -> float:
    params = {
        "MIPFocus": trial.suggest_categorical("MIPFocus", [0, 1, 2, 3]),
        "Heuristics": trial.suggest_float("Heuristics", 0.0, 0.5),
        "Cuts": trial.suggest_categorical("Cuts", [-1, 0, 1, 2]),
        "Presolve": trial.suggest_categorical("Presolve", [-1, 0, 1, 2]),
        "VarBranch": trial.suggest_categorical("VarBranch", [-1, 0, 1, 2, 3]),
    }
    times = [par2_runtime(p, w, c, params, time_limit=30.0) for p, w, c in TRAIN]
    return shifted_geomean(times)


optuna.logging.set_verbosity(optuna.logging.WARNING)
study = optuna.create_study(direction="minimize",
                            sampler=optuna.samplers.TPESampler(seed=9))
study.optimize(objective, n_trials=40)
print(study.best_params, round(study.best_value, 2))
# Expected: on these small instances most configurations finish well inside the
# limit, so differences are modest; on instances sized to take 10-60 s at
# default settings, tuned parameters often give 1.5-3x geomean speedups.
```

Choose training instances that take roughly 10-60 seconds at default settings: instances that
solve in milliseconds make all configurations look identical (runtime differences are noise), and
instances that always time out make the objective a constant PAR2 plateau with no gradient for
the tuner. If proving optimality is out of reach, switch the metric to the MIP gap at the time
limit, read via `model.MIPGap` after checking `model.SolCount > 0`.

**Pitfall:** Wall-clock runtimes are machine- and load-dependent: a tuning run shared with other
jobs learns the scheduler, not the solver. Pin `Threads=1`, run on an idle machine, and prefer
Gurobi's deterministic work units (`model.Params.WorkLimit` and the `model.Work` attribute) over
seconds when comparability across machines matters. Also remember Gurobi ships its own tuning
tool (`grbtune` / `model.tune()`); use Optuna instead when the metric is custom (gap at limit,
primal integral, multi-instance aggregates) or when solver parameters are tuned jointly with
parameters of a surrounding matheuristic.

## Advanced Techniques

### Multivariate and grouped TPE

The default TPE is univariate: it models each parameter independently, which wastes information
when parameters interact (cooling rate and moves-per-temperature in SA jointly determine total
cooling; population size and mutation rate in a GA trade off against each other).
`TPESampler(multivariate=True)` fits a joint kernel density over all parameters;
adding `group=True` partitions the space into sub-spaces that co-occur in trials, which is the
correct treatment for the conditional spaces of Pattern 2. For parallel studies add
`constant_liar=True` so simultaneously running trials repel each other. These three flags
together are the recommended non-default setup for metaheuristic tuning.

### Warm-starting the study with known configurations

The published default configuration and configurations from earlier tuning runs are valuable
evidence; force them to be evaluated first with `enqueue_trial`. This guarantees the baseline is
in the study (so "tuned beats default" is checked inside the same protocol) and gives TPE a head
start in a sensible region.

```python
import optuna


def objective(trial: optuna.Trial) -> float:
    """Search space of Pattern 5; any multi-instance objective plugs in here."""
    sigma0 = trial.suggest_float("sigma0", 1e-3, 10.0, log=True)
    adapt = trial.suggest_float("adapt", 1.01, 2.0)
    return (sigma0 - 1.0) ** 2 + (adapt - 1.3) ** 2  # synthetic score for demo


optuna.logging.set_verbosity(optuna.logging.WARNING)
study = optuna.create_study(direction="minimize",
                            sampler=optuna.samplers.TPESampler(seed=0))
study.enqueue_trial({"sigma0": 1.0, "adapt": 1.5})  # literature default
study.enqueue_trial({"sigma0": 0.3, "adapt": 1.2})  # previous tuning result
study.optimize(objective, n_trials=30)
print(study.trials[0].params, round(study.trials[0].value, 4))
# Expected: trial 0 is exactly the enqueued default configuration, so the
# tuned-vs-default comparison is available from the study itself.
```

### Multi-objective tuning: quality versus budget

Solution quality and computational effort usually trade off, and collapsing them into one scalar
hides the trade-off from the person who has to choose. Declare two objectives and let NSGA-II
approximate the Pareto front of configurations; then pick the knee point, or the cheapest
configuration within tolerance of the best quality.

```python
import numpy as np
import optuna


def es_run(sigma0: float, adapt: float, evals: int, seed: int) -> float:
    """(1+1)-ES on a 10-D sphere with a configurable evaluation budget."""
    rng = np.random.default_rng(seed)
    x = rng.normal(0.0, 1.0, 10)
    fx = float(x @ x)
    sigma = sigma0
    for _ in range(evals):
        y = x + sigma * rng.normal(0.0, 1.0, 10)
        fy = float(y @ y)
        if fy <= fx:
            x, fx, sigma = y, fy, sigma * adapt
        else:
            sigma /= adapt ** 0.25
    return fx


def objective(trial: optuna.Trial) -> tuple[float, float]:
    """Objective 1: mean final quality. Objective 2: evaluation budget."""
    sigma0 = trial.suggest_float("sigma0", 1e-3, 10.0, log=True)
    adapt = trial.suggest_float("adapt", 1.01, 2.0)
    evals = trial.suggest_int("evals", 100, 2000, log=True)
    quality = float(np.mean([es_run(sigma0, adapt, evals, s) for s in (1, 2, 3)]))
    return quality, float(evals)


optuna.logging.set_verbosity(optuna.logging.WARNING)
study = optuna.create_study(directions=["minimize", "minimize"],
                            sampler=optuna.samplers.NSGAIISampler(seed=5))
study.optimize(objective, n_trials=80)
front = sorted((t.values[1], t.values[0], t.params) for t in study.best_trials)
for budget, quality, params in front[:5]:
    print(int(budget), round(quality, 6), params)
# Expected: study.best_trials holds the Pareto set; quality improves
# monotonically along the front as the evaluation budget grows.
```

### CMA-ES as the sampler for continuous spaces

When every tuned parameter is numeric (temperatures, rates, weights — no categoricals, no
conditionals), `optuna.samplers.CmaEsSampler` typically outperforms TPE after the first few dozen
trials, because CMA-ES learns the covariance of good configurations and follows correlated
valleys in the parameter space. The restrictions are real: categorical and conditional parameters
fall back to random sampling inside `CmaEsSampler`, so a mixed space silently loses most of the
benefit — split the tuning (categoricals first, then continuous refinement) or stay with
multivariate TPE. The mechanics of CMA-ES itself, and using it directly without Optuna, are
covered in evolution-strategies.

### irace, racing, and when not to use Optuna

irace (Lopez-Ibanez, Dubois-Lacoste, Perez Caceres, Birattari & Stuetzle 2016, "The irace
package: Iterated racing for automatic algorithm configuration") implements iterated F-Race:
candidate configurations race over a growing instance stream, statistical tests (Friedman, or
paired t) eliminate losers as soon as the evidence suffices, and survivors seed the next sampling
round. Prefer irace when the instance set is large and heterogeneous (adaptive instance
allocation then matters more than a surrogate model), when the space is dominated by categorical
and conditional choices, or when the venue expects an established algorithm-configuration tool.
Prefer Optuna when the pipeline is Python-native and you want pruning, storage, dashboards, and
multi-objective support in one tool. SMAC3 sits between the two: a random-forest surrogate
designed for runtime objectives with censoring. Whatever the tool, the protocol rules in this
skill — multi-instance objectives, seed discipline, held-out validation, equal tuning budgets —
are identical; see Eggensperger, Lindauer & Hutter (2019, "Pitfalls and Best Practices in
Algorithm Configuration") for an empirical catalog of what goes wrong otherwise.

## Practical Challenges

**The objective is noisy and TPE chases lucky seeds.** Symptom: best_params change completely
between repeated tuning runs, and the "best" trial does not reproduce. Fix: more seeds per trial
(2-5 as a start), fixed seed lists shared by all trials (paired evaluation, which reduces
between-trial variance), and gap normalization so noise is comparable across instances. If trials
are cheap, increase trials instead of seeds; if expensive, add pruning so the extra seeds only
cost time for promising configurations.

**Tuned parameters do not transfer to larger instances.** Tuning on n=20-30 instances because the
real n=200 instances are too slow is legitimate, but scale-dependent parameters (population
size, tabu tenure, temperature) rarely transfer as constants. Tune them as *functions* of
instance size — e.g., suggest a coefficient c and set tenure = c * n — or tune on a reduced run
budget at the real size. Always validate at the target size before reporting.

**A few slow instances dominate the tuning budget.** With heterogeneous instance sets, one hard
instance can consume most of each trial. Order instances cheap-to-expensive and rely on pruning
(Pattern 4); or cap the per-instance run budget during tuning and accept that the objective is
"quality at reduced budget," validating the final configuration at the full budget.

**Pruning kills slow starters.** Configurations with strong exploration (high initial
temperature, large perturbations) look bad on the first reported steps and excellent later.
Diagnose by comparing the pruned fraction per parameter region in `study.trials_dataframe()`;
mitigate with `n_warmup_steps`, a more conservative pruner, and by reporting a value only after
the run has used its full budget on that instance.

**The best trial looks great, validation looks ordinary.** This is the winner's curse: the
minimum of many noisy estimates is biased low. It is expected, not a bug. Report test-set
performance of the chosen configuration (Pattern 6). If the train-test gap is large, the search
space was too flexible relative to the instance sample — reduce tuned parameters, add training
instances, or regularize by narrowing ranges around robust defaults.

**Conditional parameters starve the model.** With many categorical branches, each branch-specific
parameter accumulates only a handful of observations and TPE's split is meaningless. Use
`TPESampler(multivariate=True, group=True)`, reduce branching by fixing design choices that the
metaheuristic-design-principles analysis already settled, or run a two-stage protocol: first a
categorical screening study with random sampling, then a numeric refinement study per surviving
branch.

**Parallel workers duplicate effort or corrupt the study.** Same-seeded samplers propose the same
points; SQLite locks under concurrent writes; two code versions write into one study. Use
`constant_liar=True`, per-worker sampler seeds, JournalStorage or an RDBMS beyond a few workers,
and a version tag in the study name (`sa_qap_v3`) so a changed objective never mixes with old
trials.

**The tuning run itself is not reproducible.** A reviewer asks how the parameters were obtained
and the answer cannot be regenerated. Record in version control: the tuning script, sampler and
its seed, instance list with generator seeds, per-trial seed lists, trial budget, Optuna version,
and the exported `trials_dataframe()` CSV. The combination replays the entire protocol; storing
only best_params does not.

**Runtime-based objectives measure the machine, not the algorithm.** Background load, turbo
boost, and NUMA effects inject correlated noise into wall-clock objectives. Use deterministic
counters where available (Gurobi work units, node counts, evaluation counts), pin threads, and
keep all trials on identical hardware. Never mix runtimes from different machines in one study.

**Reviewers ask whether the comparison was fair.** If your algorithm got 500 tuning trials and
the baseline got its paper defaults, the comparison is biased by tuning effort. Give every
compared method the same tuning protocol and budget (or explicitly justify defaults, e.g., the
baseline authors state their defaults are robust), and report the tuning budget in the paper.
The statistical machinery for the final comparison lives in algorithm-benchmarking-statistics.

## Tools & Libraries

| Library | When to use | Note |
|---|---|---|
| `optuna` | Default Python tuner for metaheuristic and solver parameters | TPE, CMA-ES, NSGA-II samplers; pruning; storage; this skill |
| `optuna-dashboard` | Inspecting a running or finished study | Live web view of trials, parameter importances, slice plots |
| `irace` (R package) | Racing over large, heterogeneous instance sets; conditional spaces | The de-facto standard in metaheuristics papers; iterated F-Race |
| `SMAC3` | Runtime minimization for solvers, censored observations | Random-forest surrogate; from the algorithm-configuration community |
| `hyperopt` | Legacy TPE implementation | Predecessor of Optuna's TPE; prefer Optuna for new work |
| `ParamILS` | Iterated local search in configuration space | Historic; useful reference point (Hutter et al. 2009) |
| Gurobi `grbtune` / `model.tune()` | Pure Gurobi parameter tuning on .mps/.lp files | Built-in; use Optuna when the metric or pipeline is custom |
| `scipy.stats` | Wilcoxon/Friedman tests on tuned-vs-default results | Final validation; see algorithm-benchmarking-statistics |

## Output Format

A complete tuning deliverable contains the protocol, the artifacts, and the validated result —
never just a dictionary of parameters.

**Tuning protocol checklist (fill in before the run):**

- [ ] Parameter table: name, type, range, scale (log/linear), default, conditional-on.
- [ ] Objective metric defined (gap to reference / runtime PAR2 / quality at budget) and its
      aggregation (mean / median / shifted geomean) stated.
- [ ] Training instances listed with generator seeds; test instances held out and untouched.
- [ ] Seeds per instance per trial fixed and listed; test seeds disjoint from tuning seeds.
- [ ] Sampler, sampler seed, pruner, `n_trials`, and per-run budget fixed.
- [ ] Total wall-clock estimate computed and accepted.
- [ ] Default configuration enqueued as trial 0.

**Run configuration template (store next to the results):**

```yaml
study_name: sa_qap_v3
direction: minimize
sampler: {type: TPESampler, seed: 42, multivariate: true, group: true}
pruner: {type: MedianPruner, n_startup_trials: 10, n_warmup_steps: 1}
n_trials: 100
objective:
  metric: mean_relative_gap_to_reference
  run_budget: {moves: 30000}
  train_instances: [qap_n15_s1, qap_n20_s2, qap_n25_s3, qap_n30_s4, qap_n18_s5]
  trial_seeds: [101, 102]
validation:
  test_instances: [qap_n22_s6, qap_n26_s7, qap_n28_s8]
  test_seeds: [501, 502, 503]
  baseline: {t0: 200.0, alpha: 0.999}
```

**Result report (what goes in the paper or README):**

- Chosen configuration with all parameter values.
- Train objective of the best trial AND test performance of the chosen configuration
  (tuned vs. default, same test seeds), with the overtuning gap visible.
- Tuning effort: trials run, trials pruned, total CPU time, hardware.
- Artifacts: `trials_dataframe()` CSV, study storage file, tuning script, config YAML — all
  committed or archived with the result tables.

## Questions to Ask

- Which algorithm and which of its parameters are we tuning — and which are fixed by design?
- What metric defines "better": solution quality at a fixed budget, time to optimality, or gap
  at a time limit?
- How many training instances exist, and can we hold some out for validation?
- Is the algorithm randomized, and how many seeds per instance can each trial afford?
- What is the total tuning budget in wall-clock hours, and on what hardware?
- Will instances in production/experiments be larger than the tuning instances?
- Do any parameters only exist under certain choices (conditional space)?
- Does the comparison baseline get the same tuning budget, and how will that be reported?
- Does the venue or advisor expect irace specifically, or is Optuna acceptable?

## Related Skills

- **algorithm-benchmarking-statistics** — when the tuned configuration must be compared against
  baselines with paired statistical tests, performance profiles, and sound reporting.
- **metaheuristic-design-principles** — when deciding which parameters an algorithm should expose
  to the tuner and which should be fixed or removed by design.
- **optimization-project-structure** — when wiring tuning runs into a reproducible research
  codebase with config files, seed management, and atomic result writing.
- **evolution-strategies** — when the parameter space is purely continuous and CMA-ES is the
  better tuner, or when online self-adaptation should replace offline tuning.
