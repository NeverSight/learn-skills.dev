---
name: fitness-landscape-analysis
description: When the user wants to analyze a fitness landscape before or while designing a search algorithm — measuring ruggedness with random-walk autocorrelation and correlation length, fitness-distance correlation, plateaus and neutrality, and sampled local optima networks — and to use those measurements to choose operators and predict problem hardness. Also use when the user mentions "fitness landscape," "ruggedness," "fitness-distance correlation," "autocorrelation," "problem hardness," "big valley," or "neutrality," or when a metaheuristic stagnates for unclear reasons. For move and neighborhood design, see local-search-and-neighborhoods; for turning the diagnosis into a full algorithm design, see metaheuristic-design-principles.
---

# Fitness Landscape Analysis

You are an expert in fitness landscape analysis for combinatorial optimization. This skill covers the core landscape concepts — ruggedness via random-walk autocorrelation, fitness-distance correlation (FDC), plateaus and neutrality, and sampled local optima networks (LONs) — and, most importantly, the methodology for turning these measurements into decisions: which neighborhood operator to use, which metaheuristic family fits, and how hard an instance family is likely to be. Use the protocols below to run a disciplined analysis instead of guessing, and hand the resulting design decisions to **metaheuristic-design-principles** and **local-search-and-neighborhoods**.

## Initial Assessment

Establish these facts before measuring anything. Landscape statistics are meaningless without them.

- **Fix the representation and candidate neighborhoods first.** A landscape is the triple (solution set, neighborhood, objective). The same problem under 2-opt and under city-swap is two different landscapes. List every candidate operator the eventual algorithm might use; each one gets its own analysis.
- **Confirm the objective direction and scale.** Minimization or maximization, and whether the objective is integer-valued (a source of neutrality) or real-valued (usually no exact ties). Decide a tolerance for "equal fitness" up front.
- **Get the evaluation cost.** Autocorrelation needs walks of 10^4–10^5 steps; FDC needs 10^2–10^3 local-search descents; LON sampling needs 10^3–10^5 descents. If one evaluation takes seconds, the analysis budget dominates — shrink instances or use delta evaluation.
- **Check whether the global optimum (or a strong best-known) is available.** FDC requires a reference optimum. Without one, you can only use best-found solutions, and you must report that caveat.
- **Pick representative instances.** Landscape features vary across an instance family. Analyze at least 3–5 instances per size, and at least two sizes, before generalizing. Use seeded generators so the study is reproducible.
- **Decide what decision the analysis must inform.** Typical decisions: (a) which of k candidate operators to adopt, (b) single-solution vs population method, (c) whether plateau handling is needed, (d) whether restarts or perturbation-based escapes fit better, (e) predicting which instances will be hard. Measure only what feeds the decision.
- **Confirm distance metrics.** FDC and neutral walks need a genotype distance consistent with the neighborhood: Hamming distance for bit-flip, bond (shared-edge) distance for 2-opt on tours, swap distance for permutations under exchange moves. A mismatched metric invalidates the analysis.
- **Set the analysis budget explicitly.** A good rule: landscape analysis should consume at most 5–10% of the total experimentation budget (tuning + benchmarking). It is a scouting step, not the campaign.
- **Record seeds and walk parameters.** Walk length, number of walks, number of restarts, perturbation strength for LON sampling. These go into the final report verbatim.
- **Check for known theory.** Many classic landscapes are "elementary" with closed-form autocorrelation (TSP under 2-opt, graph coloring under vertex recolor, NK under bit-flip). When theory exists, use measurements to validate the harness, not to rediscover the formula.

## Landscape Anatomy and Measures

A fitness landscape is a triple

$$\mathcal{L} = (S, N, f), \qquad N: S \to 2^S, \qquad f: S \to \mathbb{R},$$

where $S$ is the search space induced by the representation, $N(x)$ the neighborhood induced by the move operator, and $f$ the objective (minimization throughout this skill). The algorithm does not search "the problem"; it searches this landscape. Changing $N$ changes the number of local optima, the basin structure, and every statistic below.

### The four measure families in scope

| Measure | What it captures | Sampling protocol | Cost | Primary reference |
|---|---|---|---|---|
| Autocorrelation $r(s)$, correlation length $\ell$ | Ruggedness: how fast fitness decorrelates along a walk | Unbiased random walk, 10^4–10^5 steps | Low | Weinberger (1990); Stadler (1996) |
| Fitness-distance correlation $r_{fd}$ | Global structure: do good solutions cluster near the optimum? | Multistart descent to 10^2–10^3 local optima + distance to reference optimum | Medium | Jones & Forrest (1995) |
| Neutral degree, neutral walks | Plateaus: fraction of equal-fitness neighbors, plateau extent | Random sample + walks restricted to equal fitness | Low–medium | Reidys & Stadler (2001) |
| Local optima network (sketch) | Coarse topology: optima as nodes, escape transitions as edges; funnels | Basin-hopping sampling: descend, perturb, descend | High | Ochoa et al. (2008); Ochoa & Veerapen (2016) |

### Ruggedness: autocorrelation and correlation length

Run an unbiased random walk $x_0, x_1, \dots$ where $x_{t+1}$ is drawn uniformly from $N(x_t)$, and record $f_t = f(x_t)$. The autocorrelation function and correlation length are

$$r(s) = \frac{\operatorname{Cov}(f_t, f_{t+s})}{\operatorname{Var}(f_t)}, \qquad \ell = -\frac{1}{\ln r(1)}.$$

Interpretation: $\ell$ is roughly the number of random steps over which fitness stays informative. Large $\ell$ relative to the landscape diameter means smooth; $\ell$ near 1 means near-random. For *elementary landscapes* (Grover 1992; Stadler 1996), $r(s) = r(1)^s$ exactly, and $r(1)$ has closed forms: OneMax under bit-flip gives $r(1) = 1 - 2/n$; NK landscapes give $r(1) \approx 1 - (K+1)/N$; symmetric TSP under 2-opt gives $\ell \approx n/2$, under insertion $\approx n/3$, under city-swap $\approx n/4$ (Stadler & Schnabl 1992, "The landscape of the travelling salesman problem"). The correlation length conjecture (Stadler & Schnabl 1992) links larger $\ell$ to fewer local optima, which is the basis for using $\ell$ to rank operators.

Always compare $\ell$ values for the *same problem under different operators*, or normalize by the diameter of the neighborhood graph before comparing across problems.

### Global structure: fitness-distance correlation

Collect samples $(f(x_i), d(x_i, x^*))$ — usually local optima from multistart descent — where $x^*$ is the global or best-known optimum and $d$ a representation-appropriate distance. FDC is the Pearson correlation

$$r_{fd} = \frac{\operatorname{Cov}(f, d)}{\sigma_f \, \sigma_d}.$$

For minimization (Jones & Forrest 1995, adapted): $r_{fd} \geq 0.15$ means "straightforward" — cost decreases toward the optimum, so guided search and recombination of good solutions help; $|r_{fd}| < 0.15$ means uninformative structure; $r_{fd} \leq -0.15$ means deceptive — local guidance points away from the optimum. A strong positive FDC over local optima, together with mean inter-optima distance well below the diameter, is the classic *big valley* signature (Boese, Kahng & Muddu 1994, on TSP), which justifies iterated local search with small perturbations and path-based recombination. FDC is a summary statistic with known counterexamples (Altenberg 1997): always plot the fitness–distance scatter, never report the number alone.

### Plateaus and neutrality

The neutral degree of $x$ is $\nu(x) = |\{y \in N(x) : |f(y) - f(x)| \leq \tau\}|$ for tolerance $\tau$. The average neutrality ratio $\bar\nu / |N(x)|$ over random solutions, and the length of *neutral walks* (walks restricted to equal-fitness neighbors that move away from their start), quantify plateau width. High neutrality is typical of integer-valued objectives (satisfiability counts, makespan with ties, min-conflicts in coloring/timetabling). It breaks naive descent (no improving neighbor does not mean a basin bottom) and demands neutral-move acceptance, tie-breaking rules, or fitness refinement.

### Local optima networks (sketch)

A LON compresses the landscape to a graph: nodes are local optima, edges are transitions "perturb then descend" with weights equal to observed frequencies (Ochoa et al. 2008, "A study of NK landscapes' basins and local optima networks"). The *monotonic* LON keeps only non-worsening edges; its sinks are funnel bottoms, and the number of funnels predicts whether perturbation-based methods get trapped (Ochoa & Veerapen 2016, on TSP funnels). Exhaustive LONs are only feasible for toy sizes, so in practice you sample them; treat a sampled LON as the search-relevant subnetwork, biased toward large basins.

### Step-by-step analysis protocol

```text
INPUT: problem + representation, candidate operators O1..Ok, instance set,
       evaluation budget for analysis, decision to inform.

1. Harness: implement fitness, each operator as a random-step function,
   neighbor enumeration, a descent routine, and a distance metric.
   Validate on a landscape with known theory (e.g., OneMax: r(1) = 1 - 2/n).
2. Ruggedness: for each operator Oi and instance, run >= 5 random walks of
   >= 10^4 steps; report r(1), correlation length, and dispersion across walks.
3. Neutrality: sample >= 10^3 random solutions; report the neutral ratio.
   If ratio > ~0.05, run neutral walks to estimate plateau extent.
4. Global structure: multistart descent (10^2-10^3 restarts) under the
   best operator from step 2; compute FDC vs best-known; plot the scatter;
   record mean pairwise distance between optima vs diameter.
5. LON sketch (only if step 4 is ambiguous or escape design matters):
   basin-hopping sampling; report #optima, improving-edge fraction,
   #sinks/funnels.
6. Decide:
   - Rank operators by correlation length (same budget per move).
   - smooth + single funnel        -> aggressive intensification, ILS/VNS
   - smooth + positive FDC         -> big valley: ILS, path relinking,
                                      distance-preserving crossover
   - rugged + weak FDC             -> population + strong diversity control,
                                      larger perturbations, restarts
   - high neutrality               -> accept equal moves with cycle guards,
                                      add tie-breaking objective
   - deceptive (FDC < -0.15)       -> rethink representation/operators
                                      before tuning anything
7. Report: measures table + plots + seeds + the design decision taken.
```

## Measurement Protocols

Each subsection gives the protocol, then a self-contained implementation. The code is generic: you pass in the fitness function, the step/neighbor functions, and the distance metric, so the same harness serves bitstrings, permutations, and assignment vectors.

### Random-walk autocorrelation and correlation length

Protocol: start from a uniform random solution, take unbiased random steps, record fitness. Estimate $r(s)$ for small lags, take $\ell = -1/\ln r(1)$. Use several independent walks and report the spread; one walk can be unlucky. Validate the harness against a landscape with a known closed form before trusting it on your problem.

```python
import numpy as np
from typing import Any, Callable


def random_walk_fitness(
    start: Any,
    step: Callable[[Any, np.random.Generator], Any],
    fitness: Callable[[Any], float],
    n_steps: int,
    rng: np.random.Generator,
) -> np.ndarray:
    """Fitness series f(x_0..x_T) along an unbiased random walk."""
    series = np.empty(n_steps + 1)
    x = start
    series[0] = fitness(x)
    for t in range(1, n_steps + 1):
        x = step(x, rng)
        series[t] = fitness(x)
    return series


def autocorrelation(series: np.ndarray, max_lag: int) -> np.ndarray:
    """Empirical autocorrelation r(s), s = 0..max_lag, of a fitness series."""
    f = series - series.mean()
    var = float(f @ f)
    if var == 0.0:  # perfectly flat walk: define r(s) = 0 for s >= 1
        out = np.zeros(max_lag + 1)
        out[0] = 1.0
        return out
    n = len(f)
    return np.array(
        [float(f[: n - s] @ f[s:]) * n / ((n - s) * var) for s in range(max_lag + 1)]
    )


def correlation_length(r1: float) -> float:
    """ell = -1 / ln r(1) (Weinberger 1990; Stadler 1996). Larger = smoother."""
    if r1 >= 1.0:
        return float("inf")
    if r1 <= 0.0:
        return 0.0
    return float(-1.0 / np.log(r1))


def flip_step(x: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Flip one uniformly chosen bit (returns a copy)."""
    y = x.copy()
    y[rng.integers(len(y))] ^= 1
    return y


def onemax_cost(x: np.ndarray) -> float:
    """Minimization form of OneMax: number of zero bits."""
    return float(len(x) - x.sum())


# Harness validation on a landscape with known theory: OneMax is elementary
# under bit-flip with r(1) = 1 - 2/n exactly.
rng = np.random.default_rng(42)
n = 20
series = random_walk_fitness(
    rng.integers(0, 2, n), flip_step, onemax_cost, n_steps=20_000, rng=rng
)
r = autocorrelation(series, max_lag=5)
print(f"r(1) = {r[1]:.3f}   ell = {correlation_length(r[1]):.2f}")
# Expected: r(1) within ~0.01 of theory 1 - 2/20 = 0.900; ell near the
# theoretical 9.5 (this seed measures r(1) = 0.905, ell = 10.0).
```

Walk-length guidance: the standard error of $\hat r(1)$ scales like $1/\sqrt{T}$; with $T = 2\cdot 10^4$ steps the estimate of a true $r(1) = 0.9$ is typically within $\pm 0.01$. For expensive evaluations, prefer one long walk over many short ones at equal budget — short walks bias $r(s)$ downward at all lags.

### Fitness-distance correlation

Protocol: generate local optima by multistart descent under the operator your algorithm will actually use, compute each optimum's distance to the reference optimum, report the Pearson correlation *and* the scatter plot. Sampling local optima (rather than uniform random solutions) measures the region where search actually operates; uniform sampling mostly measures the irrelevant bulk of the space.

```python
import numpy as np
from typing import Any, Callable, Iterable, Iterator


def first_improvement_descent(
    x: Any,
    fitness: Callable[[Any], float],
    neighbors: Callable[[Any], Iterable[Any]],
) -> tuple[Any, float]:
    """Descend to a local optimum with first-improvement moves (minimization)."""
    fx = fitness(x)
    improved = True
    while improved:
        improved = False
        for y in neighbors(x):
            fy = fitness(y)
            if fy < fx:
                x, fx = y, fy
                improved = True
                break
    return x, fx


def fitness_distance_correlation(fits: np.ndarray, dists: np.ndarray) -> float:
    """Pearson correlation between fitness values and distances to the optimum."""
    f = fits - fits.mean()
    d = dists - dists.mean()
    denom = float(np.sqrt((f @ f) * (d @ d)))
    return float(f @ d) / denom if denom > 0.0 else 0.0


def fdc_protocol(
    sample_start: Callable[[np.random.Generator], Any],
    fitness: Callable[[Any], float],
    neighbors: Callable[[Any], Iterable[Any]],
    distance_to_opt: Callable[[Any], float],
    n_restarts: int,
    seed: int,
) -> tuple[float, np.ndarray, np.ndarray]:
    """Multistart descent, then FDC over the sampled local optima."""
    rng = np.random.default_rng(seed)
    fits = np.empty(n_restarts)
    dists = np.empty(n_restarts)
    for i in range(n_restarts):
        opt, fopt = first_improvement_descent(sample_start(rng), fitness, neighbors)
        fits[i] = fopt
        dists[i] = distance_to_opt(opt)
    return fitness_distance_correlation(fits, dists), fits, dists


# Demo: Ising spin glass with external field (QUBO-equivalent), n = 14,
# small enough to enumerate the true optimum and genuinely multimodal.
nq = 14
rng = np.random.default_rng(23)
J = rng.normal(size=(nq, nq))
J = (J + J.T) / 2.0
np.fill_diagonal(J, 0.0)
h = rng.normal(size=nq)


def ising_cost(x: np.ndarray) -> float:
    """Spin-glass energy s^T J s + h^T s with s = 2x - 1 (minimization)."""
    s = 2.0 * np.asarray(x, dtype=np.float64) - 1.0
    return float(s @ J @ s + h @ s)


def flip_neighbors(x: np.ndarray) -> Iterator[np.ndarray]:
    """All single-bit-flip neighbors, each as a fresh copy."""
    for i in range(len(x)):
        y = x.copy()
        y[i] ^= 1
        yield y


X_all = ((np.arange(2**nq)[:, None] >> np.arange(nq)) & 1).astype(np.int8)
S_all = (2 * X_all - 1).astype(np.float64)
costs_all = np.einsum("ij,jk,ik->i", S_all, J, S_all) + S_all @ h
x_star = X_all[int(costs_all.argmin())].astype(np.int64)


def dist_to_star(x: np.ndarray) -> float:
    """Hamming distance to the enumerated global optimum."""
    return float(np.abs(np.asarray(x) - x_star).sum())


r_fd, fits, dists = fdc_protocol(
    sample_start=lambda g: g.integers(0, 2, nq),
    fitness=ising_cost,
    neighbors=flip_neighbors,
    distance_to_opt=dist_to_star,
    n_restarts=200,
    seed=11,
)
print(f"FDC over 200 local optima: {r_fd:+.2f}  (best cost {fits.min():.2f}, "
      f"global {costs_all.min():.2f})")
# Expected: a clearly positive r_fd (+0.85 for this seeded instance, which
# has 12 true local optima; descent sampling weights them by basin size) ->
# cost falls toward the optimum: "straightforward" per Jones & Forrest (1995).
```

When the global optimum is unknown, substitute the best solution found across all analysis runs and say so in the report. Re-run the FDC computation against the second- and third-best solutions; if the correlation moves a lot, the statistic is not stable enough to base decisions on.

### Neutrality and plateau measures

Protocol: estimate the average neutral ratio from random solutions. If it is non-negligible, run neutral walks — walks that only accept equal-fitness neighbors and try to increase the distance from the walk's start — to estimate plateau extent (Reidys & Stadler 2001, "Neutrality in fitness landscapes").

```python
import numpy as np
from typing import Any, Callable, Iterable


def neutral_ratio(
    sample_start: Callable[[np.random.Generator], Any],
    fitness: Callable[[Any], float],
    neighbors: Callable[[Any], Iterable[Any]],
    n_samples: int,
    seed: int,
    tol: float = 0.0,
) -> float:
    """Mean fraction of equal-fitness neighbors over random solutions."""
    rng = np.random.default_rng(seed)
    ratios = np.empty(n_samples)
    for i in range(n_samples):
        x = sample_start(rng)
        fx = fitness(x)
        nbrs = list(neighbors(x))
        ratios[i] = sum(abs(fitness(y) - fx) <= tol for y in nbrs) / len(nbrs)
    return float(ratios.mean())


def neutral_walk(
    x: Any,
    fitness: Callable[[Any], float],
    neighbors: Callable[[Any], Iterable[Any]],
    distance: Callable[[Any, Any], float],
    rng: np.random.Generator,
    max_steps: int,
    tol: float = 0.0,
) -> int:
    """Walk on equal-fitness neighbors that move away from the start.

    Returns the number of steps taken: a proxy for plateau radius.
    """
    x0, fx, d = x, fitness(x), 0.0
    for step in range(max_steps):
        cands = [
            y
            for y in neighbors(x)
            if abs(fitness(y) - fx) <= tol and distance(y, x0) > d
        ]
        if not cands:
            return step
        x = cands[rng.integers(len(cands))]
        d = distance(x, x0)
    return max_steps


# Demo: quantized OneMax, cost = floor((n - ones)/4), which creates plateaus.
nb = 24


def quant_cost(x: np.ndarray) -> float:
    """Integer-valued objective with plateaus of width 4."""
    return float((nb - int(x.sum())) // 4)


def bit_neighbors(x: np.ndarray) -> list[np.ndarray]:
    """All single-bit-flip neighbors."""
    out = []
    for i in range(len(x)):
        y = x.copy()
        y[i] ^= 1
        out.append(y)
    return out


def hamming(a: np.ndarray, b: np.ndarray) -> float:
    """Hamming distance between two bit vectors."""
    return float(np.abs(a - b).sum())


ratio = neutral_ratio(
    lambda g: g.integers(0, 2, nb), quant_cost, bit_neighbors, 300, seed=3
)
rng = np.random.default_rng(4)
walks = [
    neutral_walk(rng.integers(0, 2, nb), quant_cost, bit_neighbors, hamming,
                 rng, max_steps=30)
    for _ in range(50)
]
print(f"neutral ratio = {ratio:.2f}   mean neutral walk = {np.mean(walks):.1f}")
# Expected: neutral ratio near 0.73 and mean neutral walk around 21 of the
# 30-step cap -> wide plateaus; plain descent stalls without neutral moves.
```

Decision impact: if the neutral ratio exceeds roughly 0.05 under the production operator, configure the local search to accept equal-fitness moves with a step cap or tabu memory (see **local-search-and-neighborhoods**), or refine the objective with a tie-breaking secondary term so plateaus gain slope.

### Local optima network sampling (sketch)

Protocol: map solutions to their local optimum with a *deterministic* best-improvement descent (so each solution has a unique basin representative), then explore with basin hopping: perturb the current optimum, descend, record the edge, move on. The result is the escape-edge LON restricted to the sampled region. This is a sketch of the full LON methodology — enough to count sinks and estimate funnel structure.

```python
import numpy as np
from collections import Counter
from typing import Callable, Hashable


def best_improvement_descent(
    x: np.ndarray, cost: Callable[[np.ndarray], float]
) -> tuple[tuple[int, ...], float]:
    """Deterministic basin mapping for bit vectors under single-bit flips."""
    fx = cost(x)
    while True:
        best_i, best_f = -1, fx
        for i in range(len(x)):
            x[i] ^= 1
            fy = cost(x)
            x[i] ^= 1
            if fy < best_f - 1e-12:
                best_i, best_f = i, fy
        if best_i < 0:
            return tuple(int(v) for v in x), fx
        x[best_i] ^= 1
        fx = best_f


def sample_lon(
    cost: Callable[[np.ndarray], float],
    n: int,
    n_starts: int,
    n_hops: int,
    kick: int,
    seed: int,
) -> tuple[dict[Hashable, float], Counter]:
    """Basin-hopping LON sample: nodes = optima, edges = perturb+descend."""
    rng = np.random.default_rng(seed)
    nodes: dict[Hashable, float] = {}
    edges: Counter = Counter()
    for _ in range(n_starts):
        v, fv = best_improvement_descent(rng.integers(0, 2, n), cost)
        nodes[v] = fv
        for _ in range(n_hops):
            y = np.array(v, dtype=np.int64)
            y[rng.choice(n, size=kick, replace=False)] ^= 1
            w, fw = best_improvement_descent(y, cost)
            nodes[w] = fw
            if w != v:
                edges[(v, w)] += 1
            v, fv = w, fw  # continue the hop chain from the new optimum
    return nodes, edges


def lon_summary(nodes: dict, edges: Counter) -> dict[str, float]:
    """Sinks of the monotonic LON and a greedy funnel count."""
    improving = {(v, w): c for (v, w), c in edges.items()
                 if nodes[w] < nodes[v] - 1e-12}
    out_best: dict = {}
    for (v, w), c in improving.items():
        if v not in out_best or c > improving[(v, out_best[v])]:
            out_best[v] = w
    sinks = [v for v in nodes if v not in out_best]

    def follow(v: Hashable) -> Hashable:
        seen = {v}
        while v in out_best:
            v = out_best[v]
            if v in seen:
                break
            seen.add(v)
        return v

    funnels = {follow(v) for v in nodes}
    return {
        "n_optima": len(nodes),
        "n_edges": len(edges),
        "improving_edge_frac": len(improving) / max(len(edges), 1),
        "n_sinks": len(sinks),
        "n_funnels": len(funnels),
        "best_cost": min(nodes.values()),
    }


# Demo: Ising spin glass with field, n = 12 (11 true local optima).
nl = 12
rng = np.random.default_rng(19)
J = rng.normal(size=(nl, nl))
J = (J + J.T) / 2.0
np.fill_diagonal(J, 0.0)
h = rng.normal(size=nl)


def spin_cost(x: np.ndarray) -> float:
    """Spin-glass energy s^T J s + h^T s with s = 2x - 1."""
    s = 2.0 * np.asarray(x, dtype=np.float64) - 1.0
    return float(s @ J @ s + h @ s)


nodes, edges = sample_lon(spin_cost, nl, n_starts=20, n_hops=25, kick=2, seed=23)
print(lon_summary(nodes, edges))
# Expected: ~10 of the 11 optima sampled, ~28 distinct edges, improving-edge
# fraction near 0.57, 2 sinks / 2 funnels, best cost = global (-35.39) ->
# kick = 2 escapes basins, and a second funnel exists: ILS needs restarts
# or occasional larger kicks on this landscape.
```

Reading the summary: a single funnel containing the best-known optimum supports iterated local search with the sampled `kick` size. Several funnels of similar depth mean ILS will get trapped; you need restarts, larger perturbations, or population-level diversity (see **diversity-and-population-management**). An improving-edge fraction near zero at the sampled kick strength means the perturbation is too weak to escape basins — increase `kick` and resample.

## End-to-End Example: NK Landscapes with Tunable Ruggedness

The NK model (Kauffman 1993, "The Origins of Order") is the standard test bed because $K$ dials ruggedness: each of $N$ bits contributes a table value depending on itself and $K$ random other bits, and theory gives $r(1) \approx 1 - (K+1)/N$. With $N = 16$ the space (65,536 states) can be enumerated, so every statistic below is exact or checkable. This script is the complete protocol of the framework section on one family: measured ruggedness vs theory, exact local optima counts, and FDC against the true optimum — ending in a pandas table you can paste into a report.

```python
import numpy as np
import pandas as pd


class NKLandscape:
    """Kauffman NK model in minimization form: cost = 1 - mean contribution."""

    def __init__(self, n: int, k: int, seed: int) -> None:
        rng = np.random.default_rng(seed)
        self.n, self.k = n, k
        self.links = np.array(
            [
                np.concatenate(
                    ([i], rng.choice(np.delete(np.arange(n), i), size=k,
                                     replace=False))
                )
                for i in range(n)
            ]
        )
        self.tables = rng.random((n, 2 ** (k + 1)))

    def cost_batch(self, X: np.ndarray) -> np.ndarray:
        """Cost of each row of X (shape (m, n), entries in {0, 1})."""
        idx = np.zeros((X.shape[0], self.n), dtype=np.int64)
        for j in range(self.k + 1):
            idx = (idx << 1) | X[:, self.links[:, j]].astype(np.int64)
        contrib = self.tables[np.arange(self.n), idx]  # (m, n)
        return 1.0 - contrib.mean(axis=1)


def all_bitstrings(n: int) -> np.ndarray:
    """All 2^n bit vectors; bit b of code i equals (i >> b) & 1."""
    return ((np.arange(2**n)[:, None] >> np.arange(n)) & 1).astype(np.int8)


def walk_r1(costs: np.ndarray, n: int, steps: int,
            rng: np.random.Generator) -> float:
    """r(1) from a bit-flip random walk, using the enumerated cost table."""
    code = int(rng.integers(2**n))
    f = np.empty(steps + 1)
    f[0] = costs[code]
    for t, b in enumerate(rng.integers(0, n, size=steps), start=1):
        code ^= 1 << int(b)
        f[t] = costs[code]
    g = f - f.mean()
    return float(g[:-1] @ g[1:]) * len(g) / ((len(g) - 1) * float(g @ g))


def analyze_nk(n: int, k: int, seed: int) -> dict[str, float]:
    """Full landscape profile of one NK instance via exact enumeration."""
    nk = NKLandscape(n, k, seed)
    X = all_bitstrings(n)
    costs = nk.cost_batch(X)
    codes = np.arange(2**n)
    is_lo = np.ones(2**n, dtype=bool)
    for b in range(n):  # exact local optima under single-bit flips
        is_lo &= costs <= costs[codes ^ (1 << b)]
    lo = np.flatnonzero(is_lo)
    g_star = int(costs.argmin())
    dists = np.abs(X[lo] - X[g_star]).sum(axis=1).astype(float)
    fits = costs[lo]
    f = fits - fits.mean()
    d = dists - dists.mean()
    denom = float(np.sqrt((f @ f) * (d @ d)))
    fdc = float(f @ d) / denom if denom > 0 else 0.0
    rng = np.random.default_rng(seed + 1)
    r1 = float(np.mean([walk_r1(costs, n, 50_000, rng) for _ in range(3)]))
    return {
        "K": k,
        "r1_measured": round(r1, 3),
        "r1_theory": round(1 - (k + 1) / n, 3),
        "corr_length": round(-1.0 / np.log(r1), 2),
        "n_local_optima": int(lo.size),
        "fdc_local_optima": round(fdc, 2),
    }


rows = [analyze_nk(n=16, k=k, seed=100 + k) for k in (1, 3, 7)]
print(pd.DataFrame(rows).to_string(index=False))
# Expected: r1_measured tracks r1_theory (0.875 / 0.750 / 0.500); the
# correlation length falls from ~6 to ~1.4; n_local_optima explodes from
# 8 to ~500; FDC drops from +0.93 to ~0 as K grows -> harder instances.
```

How to read the table for design decisions: at $K = 1$ the correlation length is roughly 40% of the diameter ($n = 16$ flips), the landscape has only a handful of optima, and FDC is strongly positive — a simple ILS or even multistart descent suffices. At $K = 7$ the correlation length is near 1, optima are numerous, and FDC is weak — expect population methods with explicit diversity control to be needed, and expect tuning to matter much more. If your real problem's profile resembles the $K = 7$ row under *every* candidate operator, treat that as a hardness warning and revisit the representation before investing in tuning.

## End-to-End Example: Choosing a TSP Neighborhood from the Landscape

The most common practical use of landscape analysis: several move operators are on the table, and you must pick one before building the algorithm. For symmetric TSP, theory (Stadler & Schnabl 1992) predicts correlation lengths near $n/2$ for 2-opt (changes 2 edges), $n/3$ for insertion (3 edges), and $n/4$ for city-swap (4 edges). This script measures all three on a random Euclidean instance, then checks the big-valley signature under the winning operator, and prints the resulting design decision.

```python
import numpy as np


def tour_length(tour: np.ndarray, D: np.ndarray) -> float:
    """Cyclic tour length."""
    return float(D[tour, np.roll(tour, -1)].sum())


def step_two_opt(tour: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Reverse a random segment: changes exactly 2 edges."""
    i, j = np.sort(rng.choice(len(tour), size=2, replace=False))
    y = tour.copy()
    y[i : j + 1] = y[i : j + 1][::-1]
    return y


def step_swap(tour: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Exchange two cities: changes up to 4 edges."""
    i, j = rng.choice(len(tour), size=2, replace=False)
    y = tour.copy()
    y[i], y[j] = y[j], y[i]
    return y


def step_insertion(tour: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Move one city to a new position: changes 3 edges."""
    i = int(rng.integers(len(tour)))
    city = tour[i]
    y = np.delete(tour, i)
    return np.insert(y, int(rng.integers(len(y) + 1)), city)


def measure_ell(step, D: np.ndarray, steps: int, seed: int) -> float:
    """Correlation length of the tour-length landscape under one operator."""
    rng = np.random.default_rng(seed)
    tour = rng.permutation(len(D))
    f = np.empty(steps + 1)
    f[0] = tour_length(tour, D)
    for t in range(1, steps + 1):
        tour = step(tour, rng)
        f[t] = tour_length(tour, D)
    g = f - f.mean()
    r1 = float(g[:-1] @ g[1:]) * len(g) / ((len(g) - 1) * float(g @ g))
    return -1.0 / np.log(r1)


def two_opt_descent(tour: np.ndarray, D: np.ndarray) -> tuple[np.ndarray, float]:
    """First-improvement 2-opt descent with O(1) move deltas."""
    tour = tour.copy()
    n = len(tour)
    improved = True
    while improved:
        improved = False
        for i in range(n - 1):
            for j in range(i + 1, n):
                if i == 0 and j == n - 1:
                    continue  # reversing the whole tour changes nothing
                a, b = tour[i - 1], tour[i]
                c, d = tour[j], tour[(j + 1) % n]
                if D[a, c] + D[b, d] < D[a, b] + D[c, d] - 1e-12:
                    tour[i : j + 1] = tour[i : j + 1][::-1]
                    improved = True
    return tour, tour_length(tour, D)


def edge_set(tour: np.ndarray) -> set[frozenset]:
    """Undirected edge set of a cyclic tour."""
    n = len(tour)
    return {frozenset((int(tour[i]), int(tour[(i + 1) % n]))) for i in range(n)}


rng = np.random.default_rng(5)
n = 30
pts = rng.random((n, 2))
D = np.sqrt(((pts[:, None, :] - pts[None, :, :]) ** 2).sum(-1))

print("operator      ell   theory")
for name, step, theo in (("2-opt", step_two_opt, n / 2),
                         ("insertion", step_insertion, n / 3),
                         ("swap", step_swap, n / 4)):
    ell = float(np.mean([measure_ell(step, D, 20_000, s) for s in (1, 2, 3)]))
    print(f"{name:<12}{ell:5.1f}   ~{theo:.1f}")

# Big-valley check under the winner (2-opt): FDC over multistart optima.
opts, fits = [], []
for s in range(100):
    t, f = two_opt_descent(np.random.default_rng(1000 + s).permutation(n), D)
    opts.append(t)
    fits.append(f)
fits_arr = np.array(fits)
best = opts[int(fits_arr.argmin())]
best_edges = edge_set(best)
dists = np.array([n - len(edge_set(t) & best_edges) for t in opts], float)
f0 = fits_arr - fits_arr.mean()
d0 = dists - dists.mean()
fdc = float(f0 @ d0 / np.sqrt((f0 @ f0) * (d0 @ d0)))
print(f"FDC over 100 two-opt optima (bond distance): {fdc:+.2f}; "
      f"mean dist {dists.mean():.1f} of diameter {n}")
print("Decision: adopt 2-opt (longest correlation length); positive FDC and "
      "clustered optima = big valley -> iterated local search with small "
      "double-bridge perturbations; recombine via shared edges.")
# Expected: ell ordering 2-opt > insertion > swap (about 13 / 9 / 7 here),
# tracking the theoretical n/2, n/3, n/4 (Stadler & Schnabl 1992); FDC
# strongly positive (+0.85) with optima clustered within ~5 edge swaps of
# the best -> the big valley reported by Boese, Kahng & Muddu (1994).
```

The decision logic generalizes beyond TSP. Given equal move cost, prefer the operator with the longest correlation length: smoother landscapes have fewer, larger basins (correlation length conjecture), so the same descent budget reaches better optima. If the smoother operator is much more expensive per move (e.g., it breaks delta evaluation), re-run the comparison with budgets in wall-clock time, not in steps — see **local-search-and-neighborhoods** for delta-evaluation design and **metaheuristic-design-principles** for how the choice propagates into the full algorithm.

## Advanced Techniques

### Information content of walks

Entropy-based measures (Vassilev, Fogarty & Miller 2000, "Information characteristics and the structure of landscapes") read more from the same random walk than $r(1)$ does. Encode consecutive fitness changes as symbols in $\{-1, 0, 1\}$ using a sensitivity $\varepsilon$; the entropy of adjacent symbol pairs $H(\varepsilon)$ measures the mix of rugged and smooth segments, and the partial information content $M(\varepsilon)$ — the density of slope sign changes — estimates modality along the walk (expected local optima encountered $\approx M \cdot T / 2$). Sweeping $\varepsilon$ from 0 to the fitness range shows at which scale the ruggedness lives, which a single $r(1)$ hides.

```python
import numpy as np
from collections import Counter


def information_content(series: np.ndarray, eps: float) -> tuple[float, float]:
    """H(eps) and partial information content M(eps) of a fitness walk."""
    diff = np.diff(series)
    s = np.where(diff > eps, 1, np.where(diff < -eps, -1, 0))
    n_pairs = len(s) - 1
    counts = Counter(zip(s[:-1], s[1:]))
    probs = [c / n_pairs for (p, q), c in counts.items() if p != q]
    h = float(-sum(p * np.log(p) / np.log(6.0) for p in probs))
    slopes = s[s != 0]
    blocks = 0 if slopes.size == 0 else 1 + int(
        np.count_nonzero(slopes[1:] != slopes[:-1])
    )
    return h, blocks / len(s)


rng = np.random.default_rng(8)
smooth = np.cumsum(rng.normal(size=5000))  # correlated walk: tiny steps vs range
rugged = rng.normal(size=5000)             # white noise: steps span the range
for name, w in (("smooth", smooth), ("rugged", rugged)):
    eps_scaled = 0.05 * float(w.max() - w.min())
    h0, m0 = information_content(w, eps=0.0)
    h1, m1 = information_content(w, eps=eps_scaled)
    print(f"{name}: eps=0 -> M = {m0:.2f}   eps=5% of range -> M = {m1:.2f}, "
          f"H = {h1:.2f}")
# Expected: at eps = 0 both series show frequent slope reversals (M ~ 0.5 and
# ~0.65). At eps = 5% of the fitness range, the correlated walk collapses to
# M ~ 0 and H ~ 0 (its steps are tiny relative to its range) while white
# noise keeps M ~ 0.5 -> its ruggedness lives at the full fitness scale.
```

### Funnel diagnostics from sampled LONs

Beyond counting sinks, weight matters: compute the fraction of monotonic-LON paths that end in the funnel containing the best-known optimum (its *funnel basin share*). A share near 1 means perturbation-based search almost always drifts to the right region — invest in intensification. A share below ~0.5 means deep suboptimal funnels: add restarts from scratch, use larger or structurally different perturbations (e.g., double bridge instead of segment reversal for tours), or maintain a population spread across funnels. Ochoa & Veerapen (2016) show that hard TSPLIB instances are precisely the multi-funnel ones; the same diagnostic transfers to QAP, NK, and scheduling landscapes.

### Sampling-bias control

Every protocol here samples. Three corrections keep conclusions honest. First, random walks spend their time at typical (mediocre) fitness levels; complement them with *adaptive* walks (descents) so you also see the region where search operates. Second, sampled LONs over-represent large basins; report sample coverage (new-optima discovery rate over time — stop when it flattens) and label results as the search-relevant subnetwork. Third, estimate dispersion: run every measure on $\geq 5$ seeds/walks and report mean ± standard deviation; a correlation-length difference between operators smaller than the dispersion is not a decision basis. Where theory exists (elementary landscapes; exact $r(1)$ via Fourier/elementary-component decompositions, Chicano, Whitley & Alba 2011), prefer the closed form and use sampling only for validation.

### From measurements to hardness prediction

To predict hardness across an instance family, build a feature table — $r(1)$, $\ell/\text{diameter}$, neutral ratio, FDC, funnel count, plus cheap problem features (size, density, cost matrix variance) — and regress observed algorithm performance (mean gap at fixed budget) on it. Even a small regression or decision tree over 20–50 instances reveals which features drive difficulty, and flags outlier instances worth inspection. This is the combinatorial analogue of exploratory landscape analysis used for continuous algorithm selection; see Malan & Engelbrecht (2013), "A survey of techniques for characterising fitness landscapes and some possible ways forward" for the feature menu, and **algorithm-benchmarking-statistics** for the experimental design and statistical tests that make the performance side of the regression trustworthy.

## Practical Challenges

**The analysis used a different neighborhood than the algorithm.** The most common error: measuring under bit-flip, then running an algorithm whose mutation flips several bits, or measuring tours under 2-opt and deploying Or-opt moves. Every statistic is operator-specific. Re-run the protocol under the exact production operator, including any repair step, because repair reshapes the landscape too.

**FDC requires an optimum nobody has.** Use the best solution from all analysis runs as the reference, state this in the report, and test stability by recomputing FDC against the runner-up solutions. If conclusions flip, downgrade FDC to "inconclusive" and rely on autocorrelation plus the LON sketch instead. Never silently treat best-found as the global optimum.

**Plateaus make descent loop or stall.** With float objectives, exact equality tests miss near-ties; with integer objectives, equal-move acceptance can cycle forever. Use an explicit tolerance for "equal," cap consecutive neutral moves, and keep a small recent-solution memory to break cycles. When neutrality is structural (count-based objectives), add a lexicographic tie-breaker — e.g., total tardiness after makespan — so the search regains gradient.

**One global statistic hides anisotropy.** Many real landscapes are non-isotropic: smooth in some regions, rugged near constraint boundaries. Segment long walks into windows and report the distribution of window-level $r(1)$, not just the mean. Large window-to-window spread is itself a finding: it argues for adaptive operators and against one fixed move size.

**Walks are too short and lags too long.** Estimating $r(s)$ at lag $s$ from a walk of length $T$ effectively uses $T - s$ pairs and the estimate degrades fast; never interpret lags beyond $T/50$. With expensive evaluations, prefer one long walk over many short ones, and report confidence via multiple seeds rather than asymptotic formulas.

**Analysis cost crowds out the actual optimization.** Cap the analysis at 5–10% of the experimentation budget. Order measures by cost-to-insight: autocorrelation first (cheapest, ranks operators), neutrality second, FDC third, LON sampling only when the escape/perturbation design is genuinely uncertain. Stop as soon as the pending design decision is resolved.

**Results don't transfer to larger instances.** Statistics drift with size: correlation length typically grows with $n$, while normalized $\ell/\text{diameter}$ may shrink. Measure at two or three sizes and check the trend of the *normalized* quantities before extrapolating to production scale. If the trend is unstable, repeat the key measurement at the largest affordable size.

**Sampled LONs flatter the landscape.** Basin-hopping discovers big basins early and may miss the deep narrow funnel that traps real runs. Track the discovery curve of new optima; if it has not flattened by the end of the sampling budget, report the LON as exploratory only, and weight the autocorrelation and FDC evidence more heavily in the final decision.

## Tools & Libraries

| Library | When to use | Note |
|---|---|---|
| numpy | All sampling, walks, vectorized enumeration | `np.random.default_rng(seed)`; vectorize batch evaluation as in the NK example |
| pandas | Measure tables across instances/operators | One row per (instance, operator); feeds the final report directly |
| networkx | LON storage and graph metrics | Sinks, weakly connected components, path-based funnel shares |
| matplotlib | $r(s)$ decay curves, FDC scatter plots, LON drawings | The FDC scatter is mandatory in reports; the number alone misleads |
| scipy.stats | Pearson/Spearman correlations with p-values | Spearman is safer when fitness–distance relations are monotone but nonlinear |
| scikit-learn | Hardness regression over feature tables | Small trees/linear models; beware overfitting with < 30 instances |
| pflacco / ELA tooling | Continuous-domain landscape features | Mostly for continuous spaces; combinatorial work uses the protocols above |

## Output Format

A complete landscape-analysis deliverable contains, in order:

1. **Setup record** — instance generator + seeds, representation, every operator analyzed, distance metric, tolerance for ties, and all sampling parameters (walk lengths, restart counts, kick strength).
2. **Measures table** — one row per (instance, operator), columns for $r(1)$ ± sd, correlation length (raw and diameter-normalized), neutral ratio, FDC (with reference-optimum caveat), and LON counts when sampled.
3. **Figures** — $r(s)$ decay per operator on one axis; fitness–distance scatter with the FDC value in the caption; optional LON sketch with node size = basin sample count.
4. **Interpretation and decision** — the chosen operator and algorithm family, justified line by line from the table, plus the hardness verdict for the instance family.
5. **Reproduction note** — exact commands/seeds so the study can be re-run.

```text
LANDSCAPE ANALYSIS REPORT — <problem family, instance sizes>
Setup: representation=..., operators={...}, distance=..., tol=...,
       walks=5 x 20000 steps, restarts=200, LON: 20 starts x 25 hops, kick=2
----------------------------------------------------------------------
instance  operator   r(1)+-sd     ell   ell/diam  neutral  FDC    funnels
inst-A    2-opt      0.93+-.01   14.6     0.49     0.00    +0.55     1
inst-A    swap       0.87+-.01    7.2     0.24     0.00    +0.31     3
----------------------------------------------------------------------
Decision: 2-opt neighborhood; big-valley structure -> ILS with double-bridge
kicks; no plateau handling needed; instances with funnels >= 3 flagged hard.
```

The decision section must name the follow-up owner for each item: operator implementation details to **local-search-and-neighborhoods**, overall algorithm architecture to **metaheuristic-design-principles**, and the benchmarking protocol that validates the choice to **algorithm-benchmarking-statistics**.

## Questions to Ask

- Which representation and which candidate move operators are on the table? (No analysis without them.)
- Is the objective integer-valued or otherwise tie-prone — should we expect plateaus?
- Is a global optimum or strong best-known solution available as the FDC reference?
- How expensive is one evaluation, and is delta evaluation available for walks and descents?
- Which design decision should the analysis settle: operator choice, algorithm family, perturbation strength, or hardness prediction?
- How many instances and sizes can we analyze, and is there a seeded generator?
- What distance metric matches the neighborhood (Hamming, bond distance, swap distance)?
- What fraction of the total experimentation budget may the analysis consume?
- Are there known theoretical results (elementary landscape forms) for this problem and operator?
- Will conclusions need to transfer to instance sizes larger than we can analyze?

## Related Skills

- **local-search-and-neighborhoods** — when the analysis ranks operators and you need to design the chosen neighborhood, its delta evaluation, and plateau-aware acceptance rules.
- **diversity-and-population-management** — when the landscape shows many funnels or weak FDC and the algorithm needs explicit population diversity to avoid collapsing into one basin.
- **metaheuristic-design-principles** — when the landscape diagnosis is done and must be turned into a full algorithm design (representation, operators, search control, budgets).
- **algorithm-benchmarking-statistics** — when the operator or algorithm choice suggested by the landscape must be validated with sound experimental design and statistical tests.
