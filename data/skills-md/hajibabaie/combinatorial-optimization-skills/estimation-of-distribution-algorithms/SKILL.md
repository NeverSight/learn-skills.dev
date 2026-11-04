---
name: estimation-of-distribution-algorithms
description: When the user wants to design or implement an estimation of distribution algorithm — UMDA, PBIL, compact GA, tree models, BOA, or permutation EDAs with position-frequency, edge-histogram, or Mallows models — building and sampling probabilistic models over good solutions instead of using crossover. Also use when the user mentions "estimation of distribution," "EDA," "UMDA," "PBIL," "probabilistic model-building," or when variable interactions must be learned rather than hand-coded. For recombination-based search, see genetic-algorithms; for representation and decoder choices, see solution-encodings.
---

# Estimation of Distribution Algorithms

You are an expert in estimation of distribution algorithms (EDAs) for combinatorial optimization. This skill covers the whole model-building family — univariate models (UMDA, PBIL, compact GA), dependency models (MIMIC chains, Chow-Liu trees, ECGA, BOA), and permutation models (position-frequency/node histograms, edge histograms, Mallows and Generalized Mallows) — plus how to build, smooth, and sample these models reliably. Use the framework below to pick the right model class for the representation and interaction structure of the problem, implement it in clean vectorized numpy, and diagnose the failure modes (drift, fixation, sampling bias) that distinguish a working EDA from a stalled one.

## Initial Assessment

Establish these facts before writing any EDA code:

- **Representation.** Binary, integer/categorical, permutation, or mixed? This single fact selects the model family: Bernoulli marginals for binary, categorical marginals for integers, position/edge/Mallows models for permutations. If the natural encoding is unclear, settle it first (see solution-encodings).
- **Variable interactions.** Are decision variables nearly independent given good solutions, or do they form tight building blocks (e.g., deceptive traps, coupled assignment groups)? Univariate models solve the former and reliably fail on the latter; dependency learning (trees, BOA) costs real model-building time and is only worth it when interactions matter.
- **Problem size n and population sizing.** EDAs need populations large enough to estimate probabilities. As a rule of thumb from theory, UMDA-style algorithms need selected-set sizes of order $\sqrt{n}\log n$ on easy problems and exponentially more in the order k of deceptive building blocks (Krejca & Witt 2020, "Theory of estimation-of-distribution algorithms"). Check the implied evaluation budget is affordable.
- **Evaluation cost and budget.** Count the total evaluations you can afford. EDAs spend one full population per generation; model building adds $O(Nn)$ (univariate) to $O(n^2 N + k 2^k n^2)$ (Bayesian network) work per generation. If evaluation is cheap, model cost can dominate — profile both.
- **Constraints.** Sampled solutions are generated independently per variable (or per position), so constraints are violated by default. Decide now: repair inside the objective (and whether to write the repair back — Lamarckian), a feasibility-preserving decoder, or penalties.
- **Deception and multimodality.** A problem known to mislead frequency information (trap functions, plateaus with misleading marginals) rules out univariate EDAs. Either add linkage learning or use a crossover-based GA with a suitable operator (see genetic-algorithms).
- **Permutation semantics.** For permutation problems, ask what carries fitness: absolute positions (flow shop, assignment-like scheduling) favor position-frequency models; relative adjacency (TSP-like routing) favors edge histograms; consensus-with-spread structure favors Mallows models.
- **Baseline.** What does a tuned GA, local search, or problem-specific heuristic achieve? An EDA must justify its model-building overhead against these. Plan the comparison before running anything.
- **Diversity management.** EDAs converge by concentrating probability mass; unmanaged, marginals fixate and sampling collapses to duplicates. Plan probability clamping, smoothing, entropy monitoring, and a restart rule (see diversity-and-population-management).
- **Hybrid local search.** Is a fast local improvement step available? EDA + local search (sample, improve, refit on improved solutions) is usually much stronger than either alone, but it changes population sizing and budget math.
- **Memory limits.** The compact GA holds only a probability vector — relevant for embedded settings or enormous n; otherwise irrelevant.
- **Reproducibility.** Fix seeds per run, number of repetitions, and the statistics you will report; EDAs are stochastic and single-run claims are not evidence.

## Algorithm Anatomy

Every EDA iterates the same four-step loop; algorithms differ only in the model class $\mathcal{M}$ and how the model is updated:

$$
\text{select } S_t \subset P_t
\;\rightarrow\;
\hat{p}_{t+1} = \operatorname*{argmax}_{p \in \mathcal{M}} \;\prod_{x \in S_t} p(x)
\;\rightarrow\;
P_{t+1} \sim \hat{p}_{t+1}
\;\rightarrow\; \text{evaluate, repeat.}
$$

Crossover and mutation are replaced by *estimation* (fit a distribution to the selected set) and *sampling* (draw a fresh population from it). The model is an explicit, inspectable artifact — you can read off what the algorithm believes about good solutions at any generation, which is the main diagnostic advantage of EDAs over implicit-mixing GAs (Larrañaga & Lozano 2002, "Estimation of Distribution Algorithms"; Hauschild & Pelikan 2011, survey).

### Model taxonomy

| Model class | Algorithms | Captures | Model cost / generation | Sample cost |
|---|---|---|---|---|
| Univariate (product of marginals) | UMDA, PBIL, cGA | no interactions | $O(N n)$ | $O(N n)$ |
| Chain / tree (pairwise) | MIMIC, COMIT (Chow-Liu), BMDA | one parent per variable | $O(n^2 N)$ + spanning tree $O(n^2)$ | $O(N n)$ |
| Marginal products / Bayesian networks | ECGA, BOA, hBOA | building blocks, up to $k$ parents | $O(k\,2^k n^2 N)$ greedy search | $O(N n)$ ancestral |
| Permutation: position | NHBSA, position-frequency EDAs | job-to-position affinity | $O(N n)$ | $O(N n^2)$ sequential |
| Permutation: adjacency | EHBSA | edge (successor) frequencies | $O(N n)$ | $O(N n^2)$ sequential |
| Permutation: distance-based | Mallows / Generalized Mallows EDA | consensus + spread | $O(N n^2)$ distance + MLE | $O(N n^2)$ insertion |

### Univariate updates — the three classics

**UMDA** (Mühlenbein & Paass 1996, "From recombination of genes to the estimation of distributions I") refits each marginal from scratch as the frequency in the selected set $S_t$ (truncation selection of the best $\tau N$):

$$
p_{i,t+1} = \frac{1}{|S_t|} \sum_{x \in S_t} x_i,
\qquad
\hat{p}_{t+1}(x) = \prod_{i=1}^{n} p_{i,t+1}^{\,x_i}\,(1-p_{i,t+1})^{1-x_i}.
$$

**PBIL** (Baluja 1994, "Population-Based Incremental Learning") keeps a persistent probability vector and moves it toward the selected mean with learning rate $\alpha$, optionally perturbing the vector itself:

$$
p_{t+1} = (1-\alpha)\, p_t + \alpha \,\bar{x}_{S_t}.
$$

Small $\alpha$ gives a long memory and slow, stable convergence; $\alpha = 1$ recovers UMDA exactly.

**Compact GA** (Harik, Lobo & Goldberg 1999, "The compact genetic algorithm") simulates a population of virtual size $K$ with only the vector $p$: sample two individuals, compare, and shift each disagreeing coordinate by $\pm 1/K$ toward the winner. Memory $O(n)$; behavior approximates a steady-state GA with population $K$.

All three need two guards in practice: clamp marginals to $[1/n,\ 1 - 1/n]$ so no coordinate fixates irreversibly, and watch mean marginal entropy as a convergence/diversity signal.

### Genetic drift — the central failure mode

Without strong selection signal on coordinate $i$, the marginal $p_i$ performs a random walk with per-generation variance $\approx p_i(1-p_i)/|S_t|$ and is eventually absorbed at 0 or 1 *by chance, not by evidence*. This is genetic drift, and it is the reason undersized EDAs lose bits of the optimum early and never recover (Shapiro 2005; Krejca & Witt 2020). Defenses, in order of importance: a large enough selected set, marginal clamping, smoothing/priors (Laplace counts), PBIL-style slow learning rates, and restarts triggered by entropy collapse. Theory benchmark to remember: UMDA optimizes OneMax in $O(n \log n)$ expected evaluations with $|S_t| = \Theta(\sqrt{n}\log n)$ (Witt 2017) — populations far below that scale drift before they learn.

### Decision guidance

| Situation | Use |
|---|---|
| Binary/subset problem, weak interactions, want a robust baseline fast | UMDA with clamping + elitism |
| Same, but noisy fitness or very small populations affordable | PBIL with $\alpha \in [0.05, 0.2]$ (long memory averages noise) |
| Severe memory limits or hardware implementation | compact GA |
| Known pairwise structure (chains, trees of coupled variables) | Chow-Liu tree EDA (COMIT) |
| Deceptive building blocks of unknown composition, big budget | ECGA or BOA (accept the model-building cost) |
| Permutation problem, position-driven fitness (flow shop) | position-frequency (NHBSA-style) model |
| Permutation problem, adjacency-driven fitness (TSP-like) | edge-histogram model (EHBSA) |
| Permutation problem, strong consensus expected, principled spread control | Mallows EDA |
| Frequencies actively mislead (traps), or strong operators already exist | not an EDA — a GA or local search (see genetic-algorithms) |

### Parameter guidance

| Parameter | Typical range | Increasing it buys | At the cost of |
|---|---|---|---|
| Population $N$ | $50$–$500$; scale with $\sqrt{n}\log n$, more under deception/noise | drift resistance, model accuracy | evaluations per generation |
| Selected fraction $\tau$ (truncation) | $0.3$–$0.5$ | larger sample for estimation, less drift | weaker selection pressure, slower convergence |
| PBIL learning rate $\alpha$ | $0.05$–$0.2$ | faster convergence, sharper model | drift to fixation, premature convergence |
| PBIL vector mutation ($p_{\text{mut}}$, shift) | $0.02$, $0.05$ | sustained exploration late in the run | noisier model, slower exploitation |
| Marginal clamp margin | $1/n$ | every solution stays reachable | caps model certainty (harmless) |
| Elites re-injected | $1$–$2$ | monotone incumbent, anchor for refit | mild takeover pressure |
| Smoothing $\varepsilon$ (permutation matrices) | bias ratio $0.01$–$0.2$ of selected count | sampling exploration | blurs learned structure |
| Mallows spread $\theta$ | fit by MLE; cap near $10$ | concentration around consensus | early lock-in if uncapped |
| BOA max in-degree $k$ | $2$–$5$ | richer interaction capture | $O(2^k)$ parameters, slow model search |

Selection schemes, replacement policies, and mutation operators are shared infrastructure across population methods — take them from genetic-algorithms and diversity-and-population-management rather than reinventing them here; representation/decoder design is in solution-encodings.

## Reusable Univariate EDA Engine

One engine covers UMDA and PBIL: the only difference is whether the marginal vector is refit from scratch or updated incrementally. The objective maps a `(P, n)` 0/1 array to a `(P,)` array (minimization), so evaluation is one vectorized call per generation.

```text
UNIVARIATE BINARY EDA — minimization
  p <- (0.5, ..., 0.5); sample initial population X ~ Bernoulli(p)
  repeat until evaluation budget exhausted:
      evaluate X (one vectorized call)
      S <- best tau*N rows of X            // truncation selection
      UMDA: p <- column means of S
      PBIL: p <- (1 - alpha) * p + alpha * column means of S
            with prob p_mut per coordinate, shift p toward a random bit
      clamp p to [1/n, 1 - 1/n]            // anti-fixation
      sample X ~ Bernoulli(p); overwrite first row with the incumbent (elitism)
      track best-so-far and mean marginal entropy
  return best-so-far
```

```python
import numpy as np
from collections.abc import Callable
from dataclasses import dataclass, field


@dataclass
class EDAResult:
    x_best: np.ndarray
    f_best: float
    evaluations: int
    history: list[float] = field(default_factory=list)   # best-so-far per generation
    entropy: list[float] = field(default_factory=list)   # mean marginal entropy (bits)


def marginal_entropy(p: np.ndarray) -> float:
    """Mean Bernoulli entropy of the marginal vector, in bits."""
    q = np.clip(p, 1e-12, 1.0 - 1e-12)
    h = -(q * np.log2(q) + (1.0 - q) * np.log2(1.0 - q))
    return float(h.mean())


def binary_eda(
    objective: Callable[[np.ndarray], np.ndarray],
    n: int,
    pop_size: int = 100,
    truncation: float = 0.5,
    mode: str = "umda",          # "umda" or "pbil"
    alpha: float = 0.1,          # PBIL learning rate
    p_mut: float = 0.02,         # PBIL probability-vector mutation rate
    mut_shift: float = 0.05,     # PBIL mutation magnitude
    elite: int = 1,
    max_evals: int = 50_000,
    seed: int = 0,
) -> EDAResult:
    """Univariate EDA over binary strings, minimization.

    `objective` maps a (P, n) 0/1 int8 array to a (P,) float array. It may
    repair rows IN PLACE; repaired rows then feed model estimation
    (Lamarckian repair). Marginals are clamped to [1/n, 1 - 1/n].
    """
    rng = np.random.default_rng(seed)
    lo, hi = 1.0 / n, 1.0 - 1.0 / n
    p = np.full(n, 0.5)
    n_sel = max(2, int(round(truncation * pop_size)))

    X = (rng.random((pop_size, n)) < p).astype(np.int8)
    f = objective(X)
    evals = int(f.size)
    b = int(np.argmin(f))
    x_best, f_best = X[b].copy(), float(f[b])
    res = EDAResult(x_best, f_best, evals)

    while evals < max_evals:
        order = np.argsort(f, kind="stable")
        sel_mean = X[order[:n_sel]].mean(axis=0)
        if mode == "umda":
            p = sel_mean
        else:                                  # pbil
            p = (1.0 - alpha) * p + alpha * sel_mean
            mut = rng.random(n) < p_mut
            target = rng.integers(0, 2, size=n).astype(float)
            p = np.where(mut, (1.0 - mut_shift) * p + mut_shift * target, p)
        p = np.clip(p, lo, hi)

        X = (rng.random((pop_size, n)) < p).astype(np.int8)
        if elite > 0:
            X[:elite] = x_best                 # elitist re-injection
        f = objective(X)
        evals += int(f.size)
        g = int(np.argmin(f))
        if float(f[g]) < f_best:
            f_best, x_best = float(f[g]), X[g].copy()
        res.history.append(f_best)
        res.entropy.append(marginal_entropy(p))

    res.x_best, res.f_best, res.evaluations = x_best, f_best, evals
    return res
```

Two design points worth copying. First, the entropy trace is the EDA's vital sign: a healthy run shows entropy decaying smoothly toward zero *as* the objective improves; entropy collapsing while the objective stalls means drift or premature convergence — restart with a larger population or lower selection pressure. Second, elitist re-injection of the incumbent before evaluation makes the best solution a permanent member of the selected set, anchoring the model without distorting it.

## Worked Example: 0-1 Knapsack with UMDA

Maximize $\sum_i v_i x_i$ subject to $\sum_i w_i x_i \le C$, $x \in \{0,1\}^n$. The binary encoding is native for UMDA; the only design question is constraint handling. Independent Bernoulli sampling at 50% inclusion is heavily infeasible at the usual capacity levels, so a repair beats a penalty here: a two-pass greedy by value density first *drops* low-density items that overflow the capacity, then *fills* remaining slack. Repairing in place makes the repair Lamarckian — the model is estimated from feasible, locally tightened solutions, which sharpens the marginals exactly where it helps. (For exact DP/branch-and-bound on the same problem, and when those should replace a heuristic entirely, see knapsack-problems.)

```python
import numpy as np
from collections.abc import Callable


def knapsack_instance(n: int, seed: int = 0) -> tuple[np.ndarray, np.ndarray, float]:
    """Weakly correlated 0-1 knapsack; capacity = half the total weight."""
    rng = np.random.default_rng(seed)
    w = rng.integers(10, 100, size=n).astype(float)
    v = np.maximum(1.0, w + rng.integers(-20, 21, size=n))
    return v, w, 0.5 * float(w.sum())


def make_knapsack_objective(
    v: np.ndarray, w: np.ndarray, cap: float
) -> Callable[[np.ndarray], np.ndarray]:
    """Repairing objective: greedy drop/fill by value density, returns -value.

    Mutates X in place, so the engine refits its model on repaired
    (always feasible) solutions — Lamarckian repair.
    """
    order = np.argsort(-(v / w))                       # densest items first

    def objective(X: np.ndarray) -> np.ndarray:
        load = np.zeros(X.shape[0])
        for j in order:                                # drop pass
            keep = (X[:, j] == 1) & (load + w[j] <= cap)
            X[:, j] = keep
            load += keep * w[j]
        for j in order:                                # fill pass
            add = (X[:, j] == 0) & (load + w[j] <= cap)
            X[:, j] = X[:, j] | add
            load += add * w[j]
        return -(X * v).sum(axis=1)

    return objective


# --- tiny instance (binary_eda from the engine block above) ---
v, w, cap = knapsack_instance(80, seed=3)
obj = make_knapsack_objective(v, w, cap)
res = binary_eda(obj, n=80, pop_size=200, truncation=0.3, mode="umda",
                 elite=1, max_evals=40_000, seed=11)
greedy = obj(np.ones((1, 80), dtype=np.int8))          # repair of all-ones = density greedy
print(f"EDA value={-res.f_best:.0f}  load={float(res.x_best @ w):.0f}/{cap:.0f}  "
      f"greedy={-float(greedy[0]):.0f}")
# Expected: feasible solution (load <= cap); EDA value >= the density-greedy
# value (a fraction of a percent to a few percent on weakly correlated
# instances); res.entropy decays smoothly below ~0.2 bits by the final generations.
```

The repair has a subtle interaction with the model: because the fill pass prefers dense items, marginals of high-density items rise even when the sampled bit was 0, accelerating convergence. If you observe the model locking onto the greedy solution and refusing to explore swaps of dense-for-bulky items, lower the selection pressure (raise `truncation`) or switch to PBIL with a small `alpha` — both keep alternative item subsets alive longer.

## Permutation EDAs and the Flow-Shop Example

Permutations break the product-of-marginals trick: positions are mutually exclusive, so independent sampling produces invalid solutions. Three model families fix this, each preserving a different kind of structure (Ceberio, Irurozki, Lozano & Mendiburu 2012, "A review on estimation of distribution algorithms in permutation-based combinatorial optimization problems"):

1. **Position-frequency (node histogram, NHBSA)** — a matrix $F[j, k]$ of how often job $j$ occupies position $k$ among selected solutions (Tsutsui 2002; Tsutsui, Pelikan & Goldberg 2006). Fits problems where absolute placement carries fitness: permutation flow shop, single-machine scheduling with position-dependent costs.
2. **Edge histogram (EHBSA)** — a matrix $E[i, j]$ of how often $j$ immediately follows $i$ (Tsutsui 2002, "Probabilistic model-building genetic algorithms in permutation representation domain using edge histogram"). Fits adjacency-driven problems: TSP and routing-like orderings. Structurally close to a pheromone matrix in ant colony optimization — same sampling, different update.
3. **Mallows model** — an exponential model $P(\sigma) \propto \exp(-\theta\, d(\sigma, \sigma_0))$ around a consensus permutation $\sigma_0$ with spread $\theta$, usually with the Kendall-tau distance $d$ (Ceberio, Irurozki, Lozano & Mendiburu 2014, distance-based ranking EDA for flow shop). The permutation analogue of a Gaussian: principled, two-parameter-family control of concentration.

### Position-frequency EDA for permutation flow shop

The permutation flow-shop problem (PFSP): $n$ jobs through $m$ machines in the same order, minimize makespan $C_{\max}$. Completion times follow the recurrence $C_{k,j} = \max(C_{k,j-1},\, C_{k-1,j}) + p_{k,\pi(j)}$. Evaluation vectorizes over the population; the $m \times n$ recurrence loop is inherent to the DP.

```python
import numpy as np


def flowshop_instance(m: int, n: int, seed: int = 0) -> np.ndarray:
    """Taillard-style processing times, U{1..99}, shape (machines, jobs)."""
    rng = np.random.default_rng(seed)
    return rng.integers(1, 100, size=(m, n)).astype(float)


def makespan_batch(seqs: np.ndarray, ptimes: np.ndarray) -> np.ndarray:
    """Makespan of each job sequence; seqs (P, n) int permutations, ptimes (m, n)."""
    proc = ptimes[:, seqs]                       # (m, P, n) in sequence order
    comp = np.cumsum(proc[0], axis=1)            # machine 0: jobs never wait
    for k in range(1, ptimes.shape[0]):
        nxt = np.empty_like(comp)
        nxt[:, 0] = comp[:, 0] + proc[k][:, 0]
        for j in range(1, seqs.shape[1]):
            nxt[:, j] = np.maximum(nxt[:, j - 1], comp[:, j]) + proc[k][:, j]
        comp = nxt
    return comp[:, -1]
```

Sampling from a position model must be sequential: place position 0, remove the chosen job from the available set, renormalize, continue. The loop below runs over positions only — the categorical draw at each position is vectorized over the whole sample batch via inverse-CDF search.

```python
import numpy as np


def sample_from_position_model(
    F: np.ndarray, n_samples: int, rng: np.random.Generator
) -> np.ndarray:
    """Sample permutations position by position from a (jobs x positions) weight matrix."""
    n = F.shape[0]
    out = np.empty((n_samples, n), dtype=np.int64)
    avail = np.ones((n_samples, n), dtype=bool)
    rows = np.arange(n_samples)
    for pos in range(n):
        w = F[:, pos][None, :] * avail               # zero out already-placed jobs
        cdf = np.cumsum(w, axis=1)
        u = rng.random((n_samples, 1)) * cdf[:, -1:]
        choice = np.minimum((u > cdf).sum(axis=1), n - 1)
        out[:, pos] = choice
        avail[rows, choice] = False
    return out


def flowshop_pfm_eda(
    ptimes: np.ndarray,
    pop_size: int = 120,
    truncation: float = 0.3,
    bias_ratio: float = 0.05,
    inertia: float = 0.3,
    max_evals: int = 60_000,
    seed: int = 0,
) -> tuple[np.ndarray, float]:
    """NHBSA-style EDA for the permutation flow shop (minimize makespan)."""
    rng = np.random.default_rng(seed)
    n = ptimes.shape[1]
    n_sel = max(2, int(round(truncation * pop_size)))
    eps = bias_ratio * n_sel / n                     # Tsutsui-style smoothing bias

    pop = np.argsort(rng.random((pop_size, n)), axis=1)   # random permutations
    fit = makespan_batch(pop, ptimes)                # from the evaluation block above
    evals = pop_size
    b = int(np.argmin(fit))
    x_best, f_best = pop[b].copy(), float(fit[b])
    F = np.full((n, n), 1.0 / n)

    while evals < max_evals:
        sel = pop[np.argsort(fit, kind="stable")[:n_sel]]
        counts = np.zeros((n, n))
        np.add.at(counts, (sel.ravel(), np.tile(np.arange(n), n_sel)), 1.0)
        model = (counts + eps) / (counts + eps).sum(axis=0, keepdims=True)
        F = (1.0 - inertia) * model + inertia * F    # PBIL-like memory on the matrix
        pop = sample_from_position_model(F, pop_size, rng)
        pop[0] = x_best                              # elitist re-injection
        fit = makespan_batch(pop, ptimes)
        evals += pop_size
        g = int(np.argmin(fit))
        if float(fit[g]) < f_best:
            f_best, x_best = float(fit[g]), pop[g].copy()
    return x_best, f_best


# --- tiny instance ---
ptimes = flowshop_instance(m=5, n=20, seed=1)
x, cmax = flowshop_pfm_eda(ptimes, pop_size=120, max_evals=36_000, seed=5)
rand_pop = np.argsort(np.random.default_rng(99).random((1000, 20)), axis=1)
print(f"EDA Cmax={cmax:.0f}  best-of-1000-random={makespan_batch(rand_pop, ptimes).min():.0f}")
# Expected: a valid permutation (sorted(x) == range(20)); EDA makespan beats
# the best of 1,000 random sequences, typically by 2-6% at this size, and
# approaches the NEH-heuristic level when paired with a local search step.
```

The smoothing term `eps` is load-bearing: with raw counts, any (job, position) pair absent from the selected set gets probability zero and can never be sampled again — fixation at the matrix level. Tsutsui's bias, proportional to the selected count divided by $n$, keeps every cell reachable while letting strong frequencies dominate.

### Edge-histogram model (EHBSA)

For adjacency-driven problems, accumulate successor frequencies over selected solutions (symmetrized for undirected tours) and construct new tours city by city, choosing the next city proportional to edge weight among the unvisited.

```python
import numpy as np


def build_edge_histogram(sel: np.ndarray, n: int, bias_ratio: float = 0.05) -> np.ndarray:
    """Symmetric smoothed edge-frequency matrix from selected cyclic tours (S, n)."""
    E = np.zeros((n, n))
    nxt = np.roll(sel, -1, axis=1)
    np.add.at(E, (sel.ravel(), nxt.ravel()), 1.0)
    E = E + E.T
    E += bias_ratio * 2.0 * sel.shape[0] / (n - 1)   # smoothing on every edge
    np.fill_diagonal(E, 0.0)
    return E


def sample_tours_from_edges(
    E: np.ndarray, n_samples: int, rng: np.random.Generator
) -> np.ndarray:
    """Roulette tour construction: next city proportional to edge weight."""
    n = E.shape[0]
    out = np.empty((n_samples, n), dtype=np.int64)
    avail = np.ones((n_samples, n), dtype=bool)
    rows = np.arange(n_samples)
    out[:, 0] = rng.integers(0, n, size=n_samples)
    avail[rows, out[:, 0]] = False
    for pos in range(1, n):
        w = E[out[:, pos - 1]] * avail
        cdf = np.cumsum(w, axis=1)
        u = rng.random((n_samples, 1)) * cdf[:, -1:]
        choice = np.minimum((u > cdf).sum(axis=1), n - 1)
        out[:, pos] = choice
        avail[rows, choice] = False
    return out


# --- shape check on a toy selected set ---
rng = np.random.default_rng(0)
sel = np.argsort(rng.random((40, 12)), axis=1)
E = build_edge_histogram(sel, n=12)
tours = sample_tours_from_edges(E, n_samples=8, rng=rng)
print(tours.shape, np.all(np.sort(tours, axis=1) == np.arange(12)))
# Expected: (8, 12) True — every sampled tour is a valid permutation.
```

Tsutsui's template variant (EHBSA/WT) resamples only a random segment of an existing parent tour from the histogram, which sharply reduces the position bias of full sequential construction and is the recommended form for $n \gtrsim 100$.

### Mallows model — a parametric permutation distribution

The Mallows model puts $P(\sigma) \propto \exp(-\theta\, d_K(\sigma, \sigma_0))$ with Kendall-tau distance $d_K$ (number of discordant item pairs). Its key property: $d_K$ decomposes into independent terms $V_j \in \{0, \dots, n-j\}$, each truncated-geometric with rate $\theta$, so both the MLE of $\theta$ and exact sampling are tractable. Fit $\sigma_0$ by Borda count (sort items by mean position), then solve for $\theta$ from the observed mean distance $\bar{d}$ using

$$
\mathbb{E}[d_K] \;=\; \sum_{j=1}^{n-1} \left( \frac{q}{1-q} \;-\; \frac{m_j\, q^{m_j}}{1-q^{m_j}} \right),
\qquad q = e^{-\theta},\; m_j = n - j + 1,
$$

which is strictly decreasing in $\theta$ — bisection suffices. Exact samples come from the repeated insertion model: insert item $i$ into slot $k$ of the partial list with probability $\propto e^{-\theta (i-k)}$ (Doignon, Pekeč & Regenwetter 2004; Lu & Boutilier 2014).

```python
import numpy as np


def kendall_tau(sigma: np.ndarray, sigma0: np.ndarray) -> int:
    """Kendall-tau distance: number of discordant item pairs."""
    n = sigma.shape[0]
    rank0 = np.empty(n, dtype=np.int64)
    rank0[sigma0] = np.arange(n)
    seq = rank0[sigma]
    iu = np.triu_indices(n, 1)
    return int(np.sum(seq[iu[0]] > seq[iu[1]]))


def fit_mallows(sel: np.ndarray) -> tuple[np.ndarray, float]:
    """Estimate (sigma0, theta): Borda consensus + spread MLE by bisection."""
    n = sel.shape[1]
    pos = np.argsort(sel, axis=1)                    # pos[s, item] = its position
    sigma0 = np.argsort(pos.mean(axis=0), kind="stable")
    d_bar = max(float(np.mean([kendall_tau(s, sigma0) for s in sel])), 1e-3)

    def expected_distance(theta: float) -> float:
        q = np.exp(-theta)
        m = np.arange(2, n + 1, dtype=float)         # m_j = n - j + 1, j = 1..n-1
        return float(np.sum(q / (1.0 - q) - m * q**m / (1.0 - q**m)))

    lo, hi = 1e-4, 20.0
    for _ in range(60):                              # E[d] is decreasing in theta
        mid = 0.5 * (lo + hi)
        if expected_distance(mid) > d_bar:
            lo = mid
        else:
            hi = mid
    return sigma0, 0.5 * (lo + hi)


def sample_mallows(
    sigma0: np.ndarray, theta: float, n_samples: int, rng: np.random.Generator
) -> np.ndarray:
    """Exact Mallows sampling via the repeated insertion model."""
    n = sigma0.shape[0]
    out = np.empty((n_samples, n), dtype=np.int64)
    for s in range(n_samples):
        seq: list[int] = [0]
        for i in range(1, n):
            w = np.exp(-theta * (i - np.arange(i + 1)))   # slot k costs i-k inversions
            k = int(rng.choice(i + 1, p=w / w.sum()))
            seq.insert(k, i)
        out[s] = sigma0[np.array(seq)]               # recenter on the consensus
    return out


# --- sanity check ---
rng = np.random.default_rng(7)
sigma0 = np.arange(5)
samples = sample_mallows(sigma0, theta=1.0, n_samples=2000, rng=rng)
mean_d = float(np.mean([kendall_tau(s, sigma0) for s in samples]))
print(f"mean Kendall distance = {mean_d:.2f}")
# Expected: mean Kendall distance ~ 1.75 (the analytic E[d] for n=5, theta=1.0);
# fit_mallows on these samples recovers sigma0 exactly and theta within ~0.1.
```

A Mallows EDA replaces the matrix update of NHBSA with `fit_mallows` on the selected set and `sample_mallows` for the new population. Cap $\theta$ (e.g., at 10): the MLE diverges as the selected set concentrates, and an uncapped $\theta$ freezes sampling onto $\sigma_0$ — the permutation version of marginal fixation. The Generalized Mallows model assigns one $\theta_j$ per position, concentrating early positions faster than late ones — empirically the strongest variant on PFSP (Ceberio et al. 2014).

## Learning Dependencies: Tree EDAs and BOA

Univariate models assign independent probabilities; when good solutions share *combinations* (variable $i$ should be 1 exactly when variable $j$ is), the product model places most mass on never-seen mixtures. The cheapest fix that provably helps on chain/tree-structured interactions is the Chow-Liu tree: among all tree-factorized distributions, the maximum-likelihood one is the maximum spanning tree under pairwise mutual information (Chow & Liu 1968), used in EDAs as COMIT (Baluja & Davies 1997). Cost: $O(n^2)$ pairwise statistics plus an $O(n^2)$ Prim pass — affordable every generation.

```python
import numpy as np


def fit_chow_liu(S: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Fit a Chow-Liu tree to binary samples S (N, n).

    Returns (order, parent, cond0, cond1): parent[i] is i's parent (-1 = root);
    cond1[i]/cond0[i] = P(x_i=1 | parent=1/0); for the root, cond0 holds the marginal.
    Sampling must follow `order` (root first).
    """
    N, n = S.shape
    p1 = S.mean(axis=0)
    p11 = (S.T.astype(float) @ S) / N
    p10 = p1[:, None] - p11
    p01 = p1[None, :] - p11
    p00 = 1.0 - p1[:, None] - p1[None, :] + p11

    def term(pab: np.ndarray, pa: np.ndarray, pb: np.ndarray) -> np.ndarray:
        z = np.clip(pab, 1e-12, 1.0)
        return pab * np.log(z / np.clip(pa * pb, 1e-12, 1.0))

    mi = (term(p00, 1 - p1[:, None], 1 - p1[None, :])
          + term(p01, 1 - p1[:, None], p1[None, :])
          + term(p10, p1[:, None], 1 - p1[None, :])
          + term(p11, p1[:, None], p1[None, :]))
    np.fill_diagonal(mi, -np.inf)

    parent = np.full(n, -1, dtype=np.int64)
    in_tree = np.zeros(n, dtype=bool)
    in_tree[0] = True
    best_link, best_from = mi[0].copy(), np.zeros(n, dtype=np.int64)
    order = [0]
    for _ in range(n - 1):                            # Prim's max spanning tree
        j = int(np.argmax(np.where(in_tree, -np.inf, best_link)))
        parent[j] = best_from[j]
        in_tree[j] = True
        order.append(j)
        upd = mi[j] > best_link
        best_link = np.where(upd, mi[j], best_link)
        best_from = np.where(upd, j, best_from)

    eps = 1.0 / N
    cond0, cond1 = p1.copy(), p1.copy()
    for i in range(n):
        if parent[i] >= 0:
            pa = parent[i]
            cond1[i] = np.clip(p11[i, pa] / max(p1[pa], eps), eps, 1 - eps)
            cond0[i] = np.clip((p1[i] - p11[i, pa]) / max(1 - p1[pa], eps), eps, 1 - eps)
    return np.array(order), parent, cond0, cond1


def sample_chow_liu(
    order: np.ndarray, parent: np.ndarray, cond0: np.ndarray, cond1: np.ndarray,
    n_samples: int, rng: np.random.Generator,
) -> np.ndarray:
    """Ancestral sampling along the tree, vectorized over samples."""
    n = order.shape[0]
    X = np.zeros((n_samples, n), dtype=np.int8)
    for i in order:
        if parent[i] < 0:
            prob = np.full(n_samples, cond0[i])
        else:
            prob = np.where(X[:, parent[i]] == 1, cond1[i], cond0[i])
        X[:, i] = rng.random(n_samples) < prob
    return X


# --- recover a planted chain x0 -> x1 -> x2 ---
rng = np.random.default_rng(0)
x0 = (rng.random(3000) < 0.5).astype(np.int8)
x1 = np.where(rng.random(3000) < 0.9, x0, 1 - x0)
x2 = np.where(rng.random(3000) < 0.9, x1, 1 - x1)
order, parent, c0, c1 = fit_chow_liu(np.column_stack([x0, x1, x2]))
print(parent.tolist())
# Expected: a chain over (0, 1, 2): variable 1 links to 0 and variable 2 links
# to 1 (edge directions depend on the root, the undirected tree is 0-1-2).
```

Drop-in use: in `binary_eda`, replace the marginal update with `fit_chow_liu` on the selected rows and the Bernoulli sampling with `sample_chow_liu` — the rest of the loop (selection, elitism, entropy tracking on `cond0/cond1`) is unchanged.

**BOA, sketched.** When interactions are not tree-shaped, the Bayesian Optimization Algorithm (Pelikan, Goldberg & Cantú-Paz 1999, "BOA: The Bayesian optimization algorithm") learns a full Bayesian network by greedy score-based search:

```text
BOA — per generation
  S <- selected solutions
  B <- empty network over the n variables
  repeat:
      among all edge additions keeping B acyclic and in-degree <= k,
      apply the one with the best score gain (BDe or BIC); stop when no gain
  sample N candidates by ancestral sampling in a topological order of B
hBOA (Pelikan & Goldberg 2001) adds decision-tree local structure in the
  CPTs and restricted tournament replacement for niching.
```

The BIC score decomposes by variable, which is what makes greedy search tractable:

$$
\mathrm{BIC}(B) = \sum_{i=1}^{n} \Bigg[ \sum_{pa(\Pi_i)}\sum_{x_i} N_{i,pa,x_i} \log \hat{\theta}_{i,pa,x_i} \;-\; \frac{2^{|\Pi_i|}}{2} \log N \Bigg],
$$

where $\Pi_i$ are the parents of $x_i$ and $N_{i,pa,x_i}$ are counts in $S$. Each variable carries $O(2^{|\Pi_i|})$ parameters, so the in-degree cap $k$ is the complexity dial. Reach for BOA only when (a) univariate and tree models demonstrably stall, (b) the budget supports populations large enough to estimate $2^k$-cell tables, and (c) model-building time of order $O(k\,2^k n^2 |S|)$ per generation is acceptable. For implementation, build on a Bayesian-network library (pgmpy) rather than hand-rolling score search.

## Advanced Techniques

### Controlling drift: smoothing, margins, and population sizing

Three mechanically different tools attack the same failure. *Margins* (clamping marginals to $[1/n, 1-1/n]$, or matrix smoothing $\varepsilon$ in permutation models) guarantee ergodicity — any solution stays sampleable. *Slow learning* (PBIL's $\alpha$, the `inertia` term on the position matrix) low-pass-filters the estimation noise that drives drift. *Population sizing* removes the noise at the source: scale the selected-set size like $\sqrt{n}\log n$ for weakly interacting problems and grow it geometrically across restarts (double $N$ on each entropy-collapse restart, mirroring IPOP practice). When in doubt, prefer a bigger population over a cleverer update: most published EDA failures replicate as undersized populations (Krejca & Witt 2020).

### Hybridizing with local search

EDA + local search is the production configuration: sample from the model, improve each sample with a budgeted local search (first-improvement, capped passes), then select and refit. Two write-back policies: *Baldwinian* (fitness from the improved solution, genotype unchanged) preserves model diversity; *Lamarckian* (write the improved solution back, as in the knapsack repair above) accelerates convergence and is usually the right default for EDAs because the model only ever sees the basin representatives. Budget split guidance: spend 30–70% of evaluations inside local search; tune by checking whether generation-best improves more per evaluation inside or outside the improvement step. Neighborhood choices and delta evaluation live in local-search-and-neighborhoods.

### Adaptive selection pressure and restarts

Fix the selected fraction $\tau$, not the pressure schedule — but adapt on evidence. If mean marginal entropy falls below ~0.1 bits while the best-so-far has not improved for $G$ generations (stall), trigger a *soft restart*: re-smooth the model toward uniform ($p \leftarrow (1-\beta) p + \beta \cdot 0.5$, $\beta \approx 0.5$) while keeping the incumbent elite. If two soft restarts fail, hard-restart with doubled population. The same recipe applies to permutation matrices (blend toward $1/n$) and Mallows (halve $\theta$). Restart bookkeeping and diversity metrics are covered in diversity-and-population-management.

### Sampling temperature and explicit memory

The fitted model need not be the sampling model. Raising a temperature $T$ on a position or edge matrix — sample from $F^{1/T}$, $T > 1$ flattens, $T < 1$ sharpens — gives a free intensification/diversification dial without touching the learned statistics. A useful schedule starts at $T = 1.5$ and anneals to $0.8$ across the run. Separately, an explicit elite archive (the best $E$ distinct solutions ever seen) mixed into the selected set at refit time stabilizes the model against unlucky generations at negligible cost; deduplicate with a hash of the solution vector so the archive does not collapse to copies.

### Warm-starting the model from constructive heuristics

The uniform initial model wastes early generations rediscovering obvious structure. Seed it instead: for knapsack, initialize $p_i$ proportional to a normalized value density; for flow shop, run NEH or a handful of randomized dispatching rules and build the initial position matrix from those solutions (with heavy smoothing, $\varepsilon$ at the top of its range, so the heuristic bias guides but does not dictate). This is the EDA analogue of seeding a GA population with heuristic solutions, with the same caveat — over-sharp seeding plus truncation selection can lock the model in the heuristic's basin within two generations.

## Practical Challenges

**Marginals fixate early and the run stalls at a mediocre solution.** This is genetic drift, not a hard instance. Confirm via the entropy trace: entropy collapsing while best-so-far is flat. Fix in order: enlarge the population (first and most effective), clamp marginals to $[1/n, 1-1/n]$, raise the selected fraction toward 0.5, switch UMDA to PBIL with $\alpha \le 0.1$, and add entropy-triggered soft restarts.

**The univariate model cannot solve a problem with tight building blocks.** On trap-like structure, frequencies of single bits point away from the optimum, and no amount of population sizing rescues a product model. Either move up the taxonomy (Chow-Liu, ECGA, BOA) or hand the problem to a GA whose crossover respects the blocks (see genetic-algorithms). Diagnose cheaply: if a GA with uniform crossover also fails but one with linkage-respecting crossover succeeds, interactions are the issue.

**Sequentially sampled permutations are biased toward early positions.** Position-by-position construction renormalizes over the shrinking available set, so late positions are filled from leftovers — the model is honored at position 0 and progressively ignored. Mitigate with template-based resampling (EHBSA/WT-style: resample only a random segment of a parent), randomize the fill order of positions per sample for position models, or switch to the Mallows model whose insertion sampler has no such asymmetry.

**Model building dominates wall-clock time.** Common with dependency models and cheap objectives. Cap the BOA in-degree, refit the structure every $g$ generations while refreshing only the parameters in between, estimate pairwise statistics from a subsample of the selected set, and profile model-build vs. evaluate vs. sample before optimizing any of them.

**Sampled solutions are mostly infeasible.** Independent sampling ignores constraints by construction. Prefer repair-in-objective with Lamarckian write-back (the knapsack pattern above) when a cheap repair exists; otherwise use a feasibility-preserving decoder (see solution-encodings) so the model lives in a space where everything decodes to feasible. Penalties are the last resort in EDAs: infeasible-but-selected solutions poison the frequency estimates.

**Near convergence, the population is full of duplicates and evaluations are wasted.** A sharp model resamples the same few solutions. Deduplicate by hashing rows and resampling duplicates (cheap), apply sampling temperature $T > 1$ late in the run, or shrink the population near convergence and reallocate the budget to local search around the incumbent.

**PBIL oscillates or never commits.** Symptom of a mismatched learning rate: $\alpha$ too high makes the vector chase each generation's noise; too low makes progress invisible within budget. Start at $\alpha = 0.1$, and scale inversely with noise level: noisy fitness wants smaller $\alpha$ and larger populations. If the best-of-generation trace zigzags while the vector entropy is flat, halve $\alpha$.

**Results vary wildly across seeds.** Expected for any stochastic method; the response is protocol, not panic. Run $\ge 10$ seeds per configuration, report median and interquartile range, and compare methods with nonparametric tests. Per-generation entropy and best-so-far traces across seeds quickly separate "high-variance algorithm" from "occasionally drifts and dies" — the latter is fixable by sizing.

## Tools & Libraries

| Library | When to use | Note |
|---|---|---|
| numpy (hand-rolled, as here) | Default for production EDAs on standard encodings | Full control over smoothing/clamping — the details that decide success |
| EDAspy | Quick experiments with ready-made UMDA/EGNA/continuous EDAs | Convenient baselines; check its defaults for clamping before trusting runs |
| pgmpy | BOA-style Bayesian-network learning and ancestral sampling | Use its BIC/K2 scores and samplers instead of hand-rolling structure search |
| DEAP | When the EDA must live inside an existing DEAP experiment harness | Bring your own model code; DEAP supplies the loop and statistics |
| pymoo | Multi-objective wrappers and benchmark problems around a custom EDA | No native EDA core; treat it as the experiment frame |
| scikit-learn | Mutual-information utilities, quick model sanity checks | `mutual_info_score` for verifying hand-computed pairwise statistics |
| Mateda-2.0 | Reference implementations of many EDA variants (MATLAB) | Useful for cross-checking algorithmic details from the literature |

## Output Format

A complete EDA deliverable contains:

1. **Algorithm card** — one table: model class (with the taxonomy row it comes from), selection scheme and $\tau$, population size and how it was sized, smoothing/clamping settings, learning rate or inertia, elitism, restart rule, seed list. Every number justified in one clause.

   | Item | Value | Rationale |
   |---|---|---|
   | Model | position-frequency, $\varepsilon$ bias 0.05 | absolute positions carry PFSP fitness |
   | Population / selected | 120 / 36 ($\tau = 0.3$) | $\approx \sqrt{n}\log n$ scaled to budget |
   | Restart | soft at entropy < 0.1 bits, 30 stalled generations | drift guard |

2. **Convergence report** — best-so-far and mean model entropy per generation (table or plot), evaluations used vs. budget, and the generation where the final best was found. Flag any run where entropy collapsed before the budget midpoint.
3. **Solution validation** — independent recomputation of the objective and constraint check on the returned solution (never trust the search loop's own bookkeeping), plus encoding validity (permutations: `sorted(x) == range(n)`).
4. **Comparison** — median and IQR over $\ge 10$ seeds against the agreed baseline (greedy/GA/local search) at equal evaluation budget, with the test used and its p-value.
5. **Artifacts** — the runnable script with pinned seeds, a results table (CSV) of per-seed best values and runtimes, and the final fitted model (probability vector or matrix) saved for inspection — the model itself is often the most informative output of an EDA study.

## Questions to Ask

- What is the solution representation — binary, integer, permutation, or mixed — and is it already fixed?
- Do you know or suspect strong interactions between variables (building blocks, coupled groups), or are decisions roughly independent?
- What is the evaluation budget, and how expensive is one evaluation relative to fitting a model over n variables?
- Which constraints exist, and is there a cheap repair or a feasibility-preserving decoder?
- For permutation problems: does fitness come from absolute positions, adjacencies, or closeness to some consensus ordering?
- What baseline must the EDA beat, and at what budget?
- Is a fast local search available to hybridize with?
- How many seeds/repetitions can you afford, and what statistics does the report need?
- Are there memory or wall-clock limits that rule out dependency-model learning?

## Related Skills

- **genetic-algorithms** — when recombination on the native encoding is the better fit (especially under deception with known linkage), or to borrow selection/replacement machinery for the EDA loop.
- **solution-encodings** — when choosing between binary, integer, permutation, or decoder-based representations before committing to a probabilistic model class.
- **diversity-and-population-management** — when marginals or matrices fixate early and you need diversity metrics, archives, and restart policies.
- **knapsack-problems** — when the underlying problem is a knapsack variant and exact DP/branch-and-bound or stronger bounds should replace or complement the EDA.
