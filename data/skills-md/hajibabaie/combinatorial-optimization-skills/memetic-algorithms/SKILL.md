---
name: memetic-algorithms
description: When the user wants to build or tune a memetic algorithm - a genetic algorithm hybridized with local search - covering Lamarckian vs Baldwinian learning, local-search frequency and depth budgeting, restart management, and population diversity under strong local search. Also use when the user mentions "memetic algorithm," "hybrid GA," "GA with local search," "Lamarckian," "cultural algorithm," or when a plain GA stalls far from optimality and needs intensification. For the underlying evolutionary loop, see genetic-algorithms; for neighborhood and delta-evaluation design, see local-search-and-neighborhoods.
---

# Memetic Algorithms

You are an expert in memetic algorithms (MAs): population-based metaheuristics that hybridize a genetic algorithm with local search so that every individual in the population is a local optimum (or near one). This skill covers the canonical MA loop, Lamarckian vs Baldwinian learning, budgeting local-search frequency and depth, restart management, and keeping a population diverse when strong local search keeps collapsing it. Use the framework below to design, implement, and tune an MA, with complete worked implementations for the quadratic assignment problem (QAP) and the traveling salesman problem (TSP).

## Initial Assessment

Establish the following before designing, implementing, or debugging a memetic algorithm:

- **Problem class and encoding.** Permutation (TSP, QAP, flow shop), binary selection (knapsack, set covering), integer assignment, or decoder-based? The encoding fixes which crossover, mutation, and neighborhood moves are legal. For representation choice see **solution-encodings**; for operator catalogs see **crossover-operators** and **mutation-and-perturbation-operators**.
- **Local-search ingredients.** Does a neighborhood with delta (incremental) evaluation already exist? What is the cost of one full descent in evaluations and milliseconds? An MA without fast delta evaluation is usually a mistake — fix that first (see **local-search-and-neighborhoods** and **fitness-evaluation-and-caching**).
- **Evaluation budget.** Wall-clock limit, evaluation-count limit, or both? Expect local search to consume 90%+ of all evaluations; the budget split between evolution and learning is the central design decision.
- **Lamarckian feasibility.** Can an improved phenotype be written back into the genotype? Direct encodings: yes. Decoder-based encodings (random keys, priority rules): often no — the improved schedule may have no preimage, which forces Baldwinian or repair-style designs.
- **Constraint handling.** Are all neighborhood moves feasibility-preserving, or do you need repair after crossover/mutation? Decide where infeasibility is allowed to exist (never, only pre-repair, or penalized throughout).
- **Quality requirement.** Gap to best-known values on benchmarks, or "good solution in 5 minutes"? MAs are the state of the art for QAP and TSP benchmarks but are heavier machinery than iterated local search (ILS).
- **Baselines.** Has anyone run plain GA, multistart local search, or ILS on this problem with the same budget? An MA must beat its own components, or the hybrid is not earning its complexity.
- **Instance scale and protocol.** Sizes (n), number of instances, tuning/test split, number of seeds per configuration.
- **Reproducibility.** Single `np.random.default_rng(seed)` per run; seed recorded with every result row.
- **Compute model.** Pure numpy on one core, multiprocessing for parallel descents, or batch (vectorized) fitness evaluation?

## Algorithm Anatomy

A memetic algorithm (Moscato 1989, "On Evolution, Search, Optimization, Genetic Algorithms and Martial Arts: Towards Memetic Algorithms") layers individual learning — local search — on top of populational evolution — selection, crossover, mutation. The term "cultural algorithm" is often used loosely for the same hybrid; strictly, cultural algorithms (Reynolds 1994) add a shared belief space that biases variation, but the practical design questions (who learns, how much, and what gets inherited) are identical, and the framework below covers both readings.

**The local-optimum subspace.** For minimization of $f$ over a finite set $X$ with neighborhood $N$, define the set of local optima

$$L_N = \{\, x \in X : f(x) \le f(y)\ \ \forall y \in N(x) \,\}.$$

After Lamarckian local search, every population member lies in $L_N$, so the MA effectively evolves over $L_N$ — typically orders of magnitude smaller than $X$ and, on many problems, structured: good local optima share components (a "big valley", Boese 1995 for TSP; high fitness-distance correlation for QAP in Merz & Freisleben 2000). Crossover exploits exactly that sharing: it recombines components of two local optima, mutation supplies escape energy, and local search projects the child back onto $L_N$:

$$x_{\text{child}} = \mathrm{LS}\big(\mathrm{mut}(\mathrm{cx}(x_{p_1}, x_{p_2}))\big) \in L_N.$$

**Learning models.** What happens after local search improves a child from $x$ to $x^\* = \mathrm{LS}(x)$:

| Model | Genotype stored | Fitness used by selection | Use when |
|---|---|---|---|
| Lamarckian | $x^\*$ (writeback) | $f(x^\*)$ | Direct encodings. Default for combinatorial optimization. |
| Baldwinian | $x$ (unchanged) | $f(x^\*)$ | Writeback impossible (decoder-based encodings) or genotypic diversity must be protected. |
| Partial Lamarckian | $x^\*$ with probability $q$ | $f(x^\*)$ | Compromise; $q \approx 0.5$ can beat both extremes on rugged landscapes (Houck, Joines, Kay & Wilson 1997). |

Whitley, Gordon & Mathias (1994, "Lamarckian evolution, the Baldwin effect and function optimization") showed Baldwinian search can win on deceptive landscapes, but for the combinatorial problems in this repository Lamarckian writeback is almost always faster and is the recommended default.

**Budget accounting.** With $\lambda$ offspring per generation, $G$ generations, local-search probability $p_{ls}$, and $\bar e_{ls}$ average (delta-)evaluations per descent:

$$E_{\text{total}} \;=\; \underbrace{\lambda G}_{\text{children}} \;+\; \underbrace{p_{ls}\,\lambda G\,\bar e_{ls}}_{\text{local search}} .$$

In practice the second term dominates — well over 90% of evaluations happen inside descents. MA design is therefore mostly the art of spending the local-search budget well: which children learn ($p_{ls}$ or a selection rule), and how deeply (`ls_max_moves`).

**When to use an MA versus alternatives:**

| Situation | Recommendation |
|---|---|
| Fast local search with delta evaluation exists, and good solutions share components | MA. Crossover recombines building blocks across basins (shared edges in TSP, shared assignments in QAP). |
| Solutions do not share exploitable structure, or no respectful crossover exists | ILS or tabu search — a population adds bookkeeping but little search power. |
| Objective is expensive and has no delta evaluation | Plain GA with surrogate evaluation, or an MA with highly selective, shallow local search. |
| Feasibility is hard to maintain under moves | Decoder- or repair-based GA first; add local search restricted to feasible moves later. |
| Best-known-quality results needed on classic benchmarks | MA is the state of the art for QAP (Merz & Freisleben 2000) and TSP (Nagata & Kobayashi 2013, the EAX genetic algorithm). |

**Complexity per generation.** $O(\lambda \cdot c_{\text{var}} + p_{ls}\lambda \cdot \bar e_{ls} \cdot c_{\text{move}})$ where $c_{\text{var}}$ is crossover+mutation cost ($O(n)$ for the permutation operators used below) and $c_{\text{move}}$ is the cost of one neighborhood move evaluation — $O(n)$ for a QAP swap delta, $O(1)$ for a TSP 2-opt delta. Population sizes are deliberately small (10–50): each member is an expensive, high-quality local optimum, not a cheap random sample.

## Generic Memetic Framework

The skeleton every MA below instantiates:

```text
MEMETIC_ALGORITHM(f, config):
    P ← INIT_POPULATION(pop_size)             # random or construction-heuristic seeds
    for x in P:
        x ← LOCAL_SEARCH(x, ls_max_moves)     # start the evolution from local optima
    best ← argmin_{x in P} f(x)
    while budget remains:
        O ← ∅
        while |O| < pop_size − elite_keep:
            p1, p2 ← TOURNAMENT(P)                        # selection on f_sel
            c  ← CROSSOVER(p1, p2)    with prob. crossover_rate, else copy p1
            c  ← MUTATE(c)            with prob. mutation_rate
            with prob. ls_probability:
                c* ← LOCAL_SEARCH(c, ls_max_moves)        # depth-budgeted descent
                if Lamarckian:  c ← c*                    # write the genotype back
                f_sel(c) ← f(c*)                          # Baldwinian: genotype kept
            else:
                f_sel(c) ← f(c)
            O ← O ∪ {c};  update best
        P ← (elite_keep best of P) ∪ O                    # elitist generational step
        if DIVERSITY(P) < restart_threshold:              # restart management
            P ← elites ∪ LOCAL_SEARCH(INIT_POPULATION())
    return best
```

A reusable numpy implementation for array-encoded solutions. The five problem-specific callables (initialization, evaluation, crossover, mutation, local search) are injected; the loop, learning model, elitism, diversity monitoring, and restart logic are generic:

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np


@dataclass
class MAConfig:
    """Memetic-algorithm parameters. See the parameter guidance table."""

    pop_size: int = 30
    n_generations: int = 100
    tournament_k: int = 2
    crossover_rate: float = 0.9
    mutation_rate: float = 0.3
    ls_probability: float = 1.0
    ls_max_moves: int = 10_000
    lamarckian: bool = True
    elite_keep: int = 1
    restart_threshold: float = 0.05
    seed: int = 0


def population_diversity(pop: np.ndarray) -> float:
    """Mean pairwise Hamming distance between rows, normalized to [0, 1]."""
    m, n = pop.shape
    diff = pop[:, None, :] != pop[None, :, :]
    return float(diff.sum() / (m * (m - 1) * n))


def memetic_algorithm(
    init_population: Callable[[np.random.Generator], np.ndarray],
    evaluate: Callable[[np.ndarray], float],
    crossover: Callable[[np.ndarray, np.ndarray, np.random.Generator], np.ndarray],
    mutate: Callable[[np.ndarray, np.random.Generator], np.ndarray],
    local_search: Callable[[np.ndarray, float, int], tuple[np.ndarray, float]],
    config: MAConfig,
) -> tuple[np.ndarray, float, list[float]]:
    """Generic memetic algorithm for minimization over array-encoded solutions.

    `init_population(rng)` must return an int array of shape (pop_size, n).
    `local_search(x, f_x, max_moves)` must return an improved pair (x', f').
    Lamarckian mode stores x' in the population; Baldwinian mode keeps x but
    lets f' drive selection and replacement.
    """
    rng = np.random.default_rng(config.seed)

    def seeded_population(fresh: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, float]:
        """Local-search every individual; also return the best improved pair."""
        fits = np.empty(len(fresh), dtype=float)
        top_x, top_f = fresh[0].copy(), float("inf")
        for i in range(len(fresh)):
            x1, f1 = local_search(fresh[i], evaluate(fresh[i]), config.ls_max_moves)
            if config.lamarckian:
                fresh[i] = x1
            fits[i] = f1
            if f1 < top_f:
                top_x, top_f = x1.copy(), float(f1)
        return fresh, fits, top_x, top_f

    pop, sel_fit, best_x, best_f = seeded_population(init_population(rng))
    history = [best_f]

    for _ in range(config.n_generations):
        offspring: list[np.ndarray] = []
        off_sel_fit: list[float] = []
        while len(offspring) < config.pop_size - config.elite_keep:
            cand = rng.integers(0, len(pop), size=(2, config.tournament_k))
            p1 = pop[cand[0][np.argmin(sel_fit[cand[0]])]]
            p2 = pop[cand[1][np.argmin(sel_fit[cand[1]])]]
            child = (crossover(p1, p2, rng)
                     if rng.random() < config.crossover_rate else p1.copy())
            if rng.random() < config.mutation_rate:
                child = mutate(child, rng)
            f_child = evaluate(child)
            f_sel = f_child
            if rng.random() < config.ls_probability:
                improved, f_impr = local_search(child, f_child, config.ls_max_moves)
                f_sel = f_impr
                if config.lamarckian:
                    child = improved
                if f_impr < best_f:
                    best_x, best_f = improved.copy(), float(f_impr)
            elif f_child < best_f:
                best_x, best_f = child.copy(), float(f_child)
            offspring.append(child)
            off_sel_fit.append(float(f_sel))

        elite = np.argsort(sel_fit)[: config.elite_keep]
        pop = np.vstack([pop[elite], np.array(offspring)])
        sel_fit = np.concatenate([sel_fit[elite], np.array(off_sel_fit)])
        history.append(best_f)

        if population_diversity(pop) < config.restart_threshold:
            elite = np.argsort(sel_fit)[: config.elite_keep]
            kept_x, kept_f = pop[elite].copy(), sel_fit[elite].copy()
            pop, sel_fit, top_x, top_f = seeded_population(init_population(rng))
            pop[: config.elite_keep] = kept_x
            sel_fit[: config.elite_keep] = kept_f
            if top_f < best_f:
                best_x, best_f = top_x, top_f

    return best_x, best_f, history
```

Smoke test on a toy permutation problem — minimize total displacement from the identity permutation (optimum 0). The operators here (PMX, swap mutation, swap descent) are simple stand-ins for the problem-specific operators of the worked examples; the block reuses `MAConfig` and `memetic_algorithm` from the framework block above:

```python
import numpy as np

N = 12
POP = 24


def init_pop(rng: np.random.Generator) -> np.ndarray:
    """Random permutation population of shape (POP, N)."""
    return np.array([rng.permutation(N) for _ in range(POP)])


def displacement(x: np.ndarray) -> float:
    """Toy objective: sum_i |x[i] - i| (0 exactly at the identity)."""
    return float(np.abs(x - np.arange(len(x))).sum())


def pmx(p1: np.ndarray, p2: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Partially mapped crossover: copy a slice of p1, repair conflicts by mapping."""
    n = len(p1)
    a, b = np.sort(rng.choice(n, size=2, replace=False))
    child = p2.copy()
    child[a:b + 1] = p1[a:b + 1]
    mapping = dict(zip(p1[a:b + 1].tolist(), p2[a:b + 1].tolist()))
    for i in list(range(a)) + list(range(b + 1, n)):
        v = int(child[i])
        while v in mapping:
            v = mapping[v]
        child[i] = v
    return child


def swap_mutation(x: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Exchange two random positions."""
    y = x.copy()
    i, j = rng.choice(len(y), size=2, replace=False)
    y[[i, j]] = y[[j, i]]
    return y


def swap_descent(x: np.ndarray, f_x: float, max_moves: int) -> tuple[np.ndarray, float]:
    """First-improvement swap descent with O(1) move deltas."""
    x, f, n, moves = x.copy(), f_x, len(x), 0
    improved = True
    while improved and moves < max_moves:
        improved = False
        for i in range(n - 1):
            for j in range(i + 1, n):
                delta = (abs(int(x[j]) - i) + abs(int(x[i]) - j)
                         - abs(int(x[i]) - i) - abs(int(x[j]) - j))
                if delta < 0:
                    x[[i, j]] = x[[j, i]]
                    f, moves, improved = f + delta, moves + 1, True
    return x, float(f)


config = MAConfig(pop_size=POP, n_generations=20, seed=42)
best_x, best_f, history = memetic_algorithm(
    init_pop, displacement, pmx, swap_mutation, swap_descent, config)
print(best_f, best_x)
# Expected: best_f == 0.0 and best_x == [0 1 2 ... 11]; history is non-increasing.
```

**Parameter guidance** (typical ranges for combinatorial MAs; tune on a training instance set, see optuna-hyperparameter-tuning):

| Parameter | Typical range | Trade-off |
|---|---|---|
| `pop_size` | 10–50 | Each member is an expensive local optimum. Larger populations buy diversity but slash generations per budget; below ~10 the "population" degenerates to parallel ILS. |
| `tournament_k` | 2–3 | Selection pressure. Keep low: local search already intensifies aggressively; high pressure plus strong LS collapses the population in a few generations. |
| `crossover_rate` | 0.7–0.95 | Lower values copy parents and waste descents on already-optimized genotypes. |
| `mutation_rate` | 0.2–0.5 | Higher than in a plain GA — mutation must push children out of the parents' basins or local search just walks back. |
| `ls_probability` | 0.1–1.0 | Fraction of children that learn. 1.0 with a depth cap is the common default; lower it when descents are expensive relative to the budget. |
| `ls_max_moves` | one truncated pass – full descent | Quality per child vs children per second. Truncated descents early, full descents once improvement stalls, is a robust schedule. |
| `elite_keep` | 1–2 | Guarantees monotone best; more elites accelerate takeover and premature convergence. |
| `restart_threshold` | 0.02–0.10 | Normalized population diversity below which a restart fires. Too high restarts productive runs; too low never fires. |

## Worked Example 1: QAP Memetic with 2-Exchange Local Search

The QAP assigns $n$ facilities to $n$ locations: with symmetric flow matrix $F$ and distance matrix $D$ (zero diagonals), minimize $\sum_{i,j} F_{ij} D_{p(i)p(j)}$ over permutations $p$. The QAP is the flagship MA application (Merz & Freisleben 2000, "Fitness Landscape Analysis and Memetic Algorithms for the Quadratic Assignment Problem"): exact methods stall near $n \approx 30$, and good local optima share many facility–location assignments, which positional crossover exploits. The 2-exchange (swap) neighborhood admits an $O(n)$ delta — the piece that makes the whole MA affordable:

```python
from __future__ import annotations

import numpy as np


def make_qap_instance(n: int, seed: int) -> tuple[np.ndarray, np.ndarray]:
    """Random symmetric QAP: integer flows F and rounded Euclidean distances D."""
    rng = np.random.default_rng(seed)
    F = np.triu(rng.integers(1, 10, size=(n, n)), 1)
    F = F + F.T
    pts = rng.uniform(0.0, 100.0, size=(n, 2))
    D = np.rint(np.hypot(pts[:, None, 0] - pts[None, :, 0],
                         pts[:, None, 1] - pts[None, :, 1])).astype(int)
    return F, D


def qap_cost(p: np.ndarray, F: np.ndarray, D: np.ndarray) -> float:
    """Objective sum_ij F[i, j] * D[p[i], p[j]] (facility i sits at location p[i])."""
    return float((F * D[np.ix_(p, p)]).sum())


def swap_delta(p: np.ndarray, r: int, s: int, F: np.ndarray, D: np.ndarray) -> float:
    """O(n) cost change of swapping the locations of facilities r and s.

    Valid for symmetric F and D with zero diagonals (Taillard 1991,
    'Robust taboo search for the quadratic assignment problem').
    """
    k = np.delete(np.arange(len(p)), [r, s])
    return float(2.0 * ((F[r, k] - F[s, k]) * (D[p[s], p[k]] - D[p[r], p[k]])).sum())


def two_exchange_ls(p: np.ndarray, f_p: float, max_moves: int,
                    F: np.ndarray, D: np.ndarray) -> tuple[np.ndarray, float]:
    """First-improvement 2-exchange descent using O(n) swap deltas."""
    p, f, n, moves = p.copy(), f_p, len(p), 0
    improved = True
    while improved and moves < max_moves:
        improved = False
        for r in range(n - 1):
            for s in range(r + 1, n):
                d = swap_delta(p, r, s, F, D)
                if d < -1e-9:
                    p[[r, s]] = p[[s, r]]
                    f, moves, improved = f + d, moves + 1, True
    return p, float(f)
```

The memetic loop. Genes carry positional meaning ("facility $i$ at location $p_i$"), so cycle crossover (CX) — every position inherits from one parent, no foreign values invented — fits better than order-based operators; for the full operator catalog and preservation properties see **crossover-operators**. Duplicate elimination at insertion is the diversity workhorse here: under strong local search, many children land on identical local optima, and storing copies kills the population. This block uses `make_qap_instance`, `qap_cost`, and `two_exchange_ls` from the block above:

```python
import numpy as np


def cycle_crossover(p1: np.ndarray, p2: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """CX: decompose positions into cycles, alternate the source parent per cycle."""
    n = len(p1)
    child = np.full(n, -1)
    pos_in_p1 = np.empty(n, dtype=int)
    pos_in_p1[p1] = np.arange(n)
    take_p1 = bool(rng.integers(0, 2))
    assigned = np.zeros(n, dtype=bool)
    for start in range(n):
        if assigned[start]:
            continue
        i, cycle = start, []
        while not assigned[i]:
            assigned[i] = True
            cycle.append(i)
            i = int(pos_in_p1[p2[i]])
        src = p1 if take_p1 else p2
        child[cycle] = src[cycle]
        take_p1 = not take_p1
    return child


def qap_memetic(F: np.ndarray, D: np.ndarray, pop_size: int = 20,
                n_generations: int = 40, ls_max_moves: int = 5000,
                mutation_rate: float = 0.3, elite_keep: int = 2,
                seed: int = 0) -> tuple[np.ndarray, float]:
    """Lamarckian memetic algorithm for the symmetric QAP."""
    rng = np.random.default_rng(seed)
    n = F.shape[0]
    pop = np.array([rng.permutation(n) for _ in range(pop_size)])
    fit = np.empty(pop_size)
    for i in range(pop_size):
        pop[i], fit[i] = two_exchange_ls(pop[i], qap_cost(pop[i], F, D),
                                         ls_max_moves, F, D)
    for _ in range(n_generations):
        order = np.argsort(fit)
        new_pop = [pop[i].copy() for i in order[:elite_keep]]
        new_fit = [float(fit[i]) for i in order[:elite_keep]]
        while len(new_pop) < pop_size:
            t1, t2 = rng.integers(0, pop_size, size=(2, 2))
            p1 = pop[t1[np.argmin(fit[t1])]]
            p2 = pop[t2[np.argmin(fit[t2])]]
            child = cycle_crossover(p1, p2, rng)
            if rng.random() < mutation_rate:
                i, j = rng.choice(n, size=2, replace=False)
                child[[i, j]] = child[[j, i]]
            child, f_child = two_exchange_ls(child, qap_cost(child, F, D),
                                             ls_max_moves, F, D)
            if any(abs(f_child - g) < 0.5 for g in new_fit):
                # Duplicate local optimum: insert a fresh restart member instead.
                child = rng.permutation(n)
                child, f_child = two_exchange_ls(child, qap_cost(child, F, D),
                                                 ls_max_moves, F, D)
            new_pop.append(child)
            new_fit.append(f_child)
        pop, fit = np.array(new_pop), np.array(new_fit)
    i_best = int(np.argmin(fit))
    return pop[i_best].copy(), float(fit[i_best])


F, D = make_qap_instance(12, seed=7)
best_p, best_f = qap_memetic(F, D, seed=1)
assert best_f == qap_cost(best_p, F, D)            # independent recomputation
assert sorted(best_p.tolist()) == list(range(12))  # valid permutation
print(best_f, best_p)
# Expected: a valid assignment whose cost matches the independent recomputation;
# different seeds converge to the same best cost on this 12-facility instance,
# which strongly suggests the optimum at this size.
```

Detecting duplicates by fitness equality (within 0.5 for integer costs) is a cheap proxy that occasionally merges distinct optima with equal cost; for exact duplicate detection hash the genotype bytes as in the cache under Advanced Techniques. Scaling up: replace first-improvement scans with Taillard's $O(n^2)$-memory delta table that updates all swap deltas in $O(n)$ amortized after a move (see **fitness-evaluation-and-caching** and **quadratic-assignment-problem**), and benchmark against robust tabu search, the standard QAP baseline.

## Worked Example 2: TSP Memetic with 2-Opt

Symmetric TSP: minimize the closed-tour length over permutations of $n$ cities. Local optima of 2-opt share most of their edges ("big valley"), so recombination plus re-descent is extremely effective; the strongest known TSP heuristics are memetic (Nagata & Kobayashi 2013, EAX-GA). Here the tour is a city sequence, adjacency — not position — carries meaning, so order crossover (OX) is the right family, and the 2-opt delta is $O(1)$:

```python
from __future__ import annotations

import numpy as np


def make_tsp_instance(n: int, seed: int) -> np.ndarray:
    """Random Euclidean TSP: n points in the unit square -> distance matrix."""
    rng = np.random.default_rng(seed)
    pts = rng.uniform(0.0, 1.0, size=(n, 2))
    return np.hypot(pts[:, None, 0] - pts[None, :, 0],
                    pts[:, None, 1] - pts[None, :, 1])


def tour_length(tour: np.ndarray, D: np.ndarray) -> float:
    """Total length of the closed tour."""
    return float(D[tour, np.roll(tour, -1)].sum())


def two_opt_ls(tour: np.ndarray, f_tour: float, max_moves: int,
               D: np.ndarray) -> tuple[np.ndarray, float]:
    """2-opt descent; for each first edge, the second edge is scanned vectorized.

    Removing edges (a,b) and (c,d) and reconnecting as (a,c),(b,d) reverses the
    segment between them; the delta D[a,c] + D[b,d] - D[a,b] - D[c,d] is O(1)
    per candidate and computed for all candidates j at once.
    """
    tour, f, n, moves = tour.copy(), f_tour, len(tour), 0
    improved = True
    while improved and moves < max_moves:
        improved = False
        for i in range(n - 2):
            a, b = tour[i], tour[i + 1]
            j_hi = n - 1 if i > 0 else n - 2   # skip the closing-edge pairing at i == 0
            j = np.arange(i + 2, j_hi + 1)
            if len(j) == 0:
                continue
            c, d = tour[j], tour[(j + 1) % n]
            deltas = D[a, c] + D[b, d] - D[a, b] - D[c, d]
            k = int(np.argmin(deltas))
            if deltas[k] < -1e-12:
                jj = int(j[k])
                tour[i + 1: jj + 1] = tour[i + 1: jj + 1][::-1]
                f, moves, improved = f + float(deltas[k]), moves + 1, True
    return tour, float(f)
```

The memetic loop. Mutation is the double bridge — the classic 4-opt kick that 2-opt cannot undo in one move (the same kick ILS uses; see **mutation-and-perturbation-operators** for the perturbation catalog). When a child lands on a local optimum already in the new population, it is kicked and re-descended rather than discarded, which converts wasted duplicates into extra basin exploration. This block uses `make_tsp_instance`, `tour_length`, and `two_opt_ls` from the block above:

```python
import numpy as np


def order_crossover(p1: np.ndarray, p2: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """OX: copy a slice of p1, fill remaining cities in p2's cyclic order."""
    n = len(p1)
    a, b = np.sort(rng.choice(n, size=2, replace=False))
    child = np.empty(n, dtype=int)
    child[a:b + 1] = p1[a:b + 1]
    used = np.zeros(n, dtype=bool)
    used[p1[a:b + 1]] = True
    order = np.concatenate([p2[b + 1:], p2[:b + 1]])
    child[np.concatenate([np.arange(b + 1, n), np.arange(a)])] = order[~used[order]]
    return child


def double_bridge(tour: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """4-opt double bridge: cut the tour at three points and reorder the segments."""
    n = len(tour)
    i, j, k = np.sort(rng.choice(np.arange(1, n), size=3, replace=False))
    return np.concatenate([tour[:i], tour[j:k], tour[i:j], tour[k:]])


def tsp_memetic(D: np.ndarray, pop_size: int = 20, n_generations: int = 30,
                ls_max_moves: int = 20_000, mutation_rate: float = 0.4,
                elite_keep: int = 2, seed: int = 0) -> tuple[np.ndarray, float]:
    """Lamarckian memetic algorithm for the symmetric TSP (2-opt local search)."""
    rng = np.random.default_rng(seed)
    n = D.shape[0]
    pop = np.array([rng.permutation(n) for _ in range(pop_size)])
    fit = np.empty(pop_size)
    for i in range(pop_size):
        pop[i], fit[i] = two_opt_ls(pop[i], tour_length(pop[i], D),
                                    ls_max_moves, D)
    for _ in range(n_generations):
        order = np.argsort(fit)
        new_pop = [pop[i].copy() for i in order[:elite_keep]]
        new_fit = [float(fit[i]) for i in order[:elite_keep]]
        while len(new_pop) < pop_size:
            t1, t2 = rng.integers(0, pop_size, size=(2, 2))
            p1 = pop[t1[np.argmin(fit[t1])]]
            p2 = pop[t2[np.argmin(fit[t2])]]
            child = order_crossover(p1, p2, rng)
            if rng.random() < mutation_rate:
                child = double_bridge(child, rng)
            child, f_child = two_opt_ls(child, tour_length(child, D),
                                        ls_max_moves, D)
            if any(abs(f_child - g) < 1e-9 for g in new_fit):
                # Duplicate local optimum: kick it out of the basin and re-descend.
                child = double_bridge(child, rng)
                child, f_child = two_opt_ls(child, tour_length(child, D),
                                            ls_max_moves, D)
            new_pop.append(child)
            new_fit.append(f_child)
        pop, fit = np.array(new_pop), np.array(new_fit)
    i_best = int(np.argmin(fit))
    return pop[i_best].copy(), float(fit[i_best])


D = make_tsp_instance(30, seed=3)
best_tour, best_len = tsp_memetic(D, seed=5)
assert sorted(best_tour.tolist()) == list(range(30))     # valid tour
assert abs(best_len - tour_length(best_tour, D)) < 1e-6  # honest objective
print(round(best_len, 4))
# Expected: a valid 30-city tour with length roughly 4.2-4.8 (uniform points in
# the unit square at n=30); the same seed always reproduces the same tour.
```

For serious TSP work, upgrade the learning step before anything else: 2-opt with neighbor lists and don't-look bits, then Or-opt, then Lin–Kernighan moves (Lin & Kernighan 1973). The MA scaffolding is unchanged — only `local_search` and (for state-of-the-art results) the crossover (edge assembly, EAX) are swapped, which is exactly why the framework keeps them injectable.

## Advanced Techniques

### Selective and adaptive local-search budgeting

Applying full descents to every child is the right default only when descents are cheap. Two refinements, in order of payoff. First, depth scheduling: truncated descents (`ls_max_moves` small) in early generations, full descents once the best-so-far stalls — early populations are far from good basins, so polishing them is wasted budget. Second, recipient selection: spend the per-generation LS budget on the most promising raw offspring plus a random remainder, instead of a uniform coin flip per child:

```python
import numpy as np


def ls_recipients(off_fit: np.ndarray, ls_budget: int, greedy_share: float,
                  rng: np.random.Generator) -> np.ndarray:
    """Choose which offspring receive local search under a per-generation budget.

    Most of the budget goes to the best raw offspring (they sit in the most
    promising basins); a random remainder keeps unexplored regions learning.
    """
    n = len(off_fit)
    k = min(ls_budget, n)
    n_greedy = min(k, max(1, int(round(greedy_share * k))))
    by_fit = np.argsort(off_fit)
    rest = by_fit[n_greedy:]
    n_rand = k - n_greedy
    rand = (rng.choice(rest, size=n_rand, replace=False)
            if n_rand > 0 else np.empty(0, dtype=int))
    return np.concatenate([by_fit[:n_greedy], rand.astype(int)])


rng = np.random.default_rng(0)
raw_fitness = rng.uniform(50.0, 100.0, size=12)
chosen = ls_recipients(raw_fitness, ls_budget=5, greedy_share=0.6, rng=rng)
print(sorted(chosen.tolist()))
# Expected: 5 distinct indices; the 3 best raw offspring are always included.
```

A further adaptive layer ties `ls_probability` or depth to the descent success rate: if fewer than ~20% of recent descents improved on their starting fitness by a meaningful margin, the population already sits on good local optima — shift budget from learning to variation (raise mutation strength) rather than burning it on no-op descents.

### Lamarckian, Baldwinian, and partial writeback

Default to Lamarckian for direct encodings: it is the budget-efficient choice and every classic MA result (QAP, TSP) uses it. Switch to Baldwinian only when forced — decoder-based representations where the improved phenotype has no genotype preimage (see **decoder-based-representations** for that situation) — or when diagnostics show Lamarckian writeback collapsing genotypic diversity within a few generations on a deceptive landscape (Whitley, Gordon & Mathias 1994). Partial Lamarckian (write back with probability $q$) is a one-parameter compromise worth trying at $q \in \{0.25, 0.5\}$ when restarts fire too often; Houck et al. (1997) report it competitive across landscapes. Note Baldwinian mode pays the full descent cost but discards the genotype gain, so its only currency is preserved diversity — measure that diversity (e.g., `population_diversity` above) before paying for it.

### Restart management without amnesia

A diversity-triggered restart (normalized pairwise distance below ~0.05) must not erase the run's knowledge. Keep the elite set verbatim; reseed the rest with fresh randomized solutions passed through local search (raw random members lose every tournament against resident local optima and never reproduce — a silently broken restart). Better than pure randomness: bias new members using frequency memory (assignments/edges that recurred in elites get higher sampling probability), or generate them by path relinking between stored elites (see **scatter-search-path-relinking** for the mechanics). Cap restarts per run; if the third restart re-converges to the same best value, the budget is better spent on a longer descent (Lin–Kernighan instead of 2-opt) than on more restarts.

### Caching repeated descents

Crossover between similar parents recreates identical children generation after generation, and each redundant descent costs thousands of delta evaluations. Memoize descent endpoints keyed by genotype bytes:

```python
from typing import Callable

import numpy as np


class LSCache:
    """Memoize local-search endpoints keyed by exact genotype bytes.

    Under strong local search the same children recur across generations;
    caching turns each repeat into a dictionary lookup. Bound the table size
    in long runs (evict oldest) to keep memory flat.
    """

    def __init__(self) -> None:
        self.table: dict[bytes, tuple[np.ndarray, float]] = {}
        self.hits = 0

    def get_or_run(self, x: np.ndarray,
                   run: Callable[[np.ndarray], tuple[np.ndarray, float]]
                   ) -> tuple[np.ndarray, float]:
        """Return the cached (local optimum, fitness) or compute and store it."""
        key = np.ascontiguousarray(x).tobytes()
        if key in self.table:
            self.hits += 1
            x_opt, f_opt = self.table[key]
            return x_opt.copy(), f_opt
        x_opt, f_opt = run(x)
        self.table[key] = (x_opt.copy(), f_opt)
        return x_opt.copy(), f_opt


calls = {"n": 0}


def fake_descent(x: np.ndarray) -> tuple[np.ndarray, float]:
    """Stand-in descent that counts how often real work happens."""
    calls["n"] += 1
    y = np.sort(x)
    return y, float(np.abs(y - np.arange(len(y))).sum())


cache = LSCache()
cache.get_or_run(np.array([2, 0, 1]), fake_descent)
cache.get_or_run(np.array([2, 0, 1]), fake_descent)
print(calls["n"], cache.hits)
# Expected: prints "1 1" - the second identical genotype hits the cache.
```

Cache hit rates of 10–30% are common in late-stage MA runs on permutation problems; combine with duplicate elimination at insertion so cached duplicates do not re-enter the population. Delta evaluation inside the descent itself is the bigger lever — see **fitness-evaluation-and-caching**.

### Adaptive meme selection

When several local searches are available (for TSP: 2-opt, Or-opt, 3-opt; for scheduling: swap vs insertion neighborhoods), let the MA learn which to apply: maintain a score per meme from recent improvement-per-evaluation, select memes by roulette or softmax over scores, and decay scores so the choice tracks search phase. This is multimeme / meta-Lamarckian learning (Krasnogor & Smith 2005, "A tutorial for competent memetic algorithms: model, taxonomy, and design issues"; Ong & Keane 2004, "Meta-Lamarckian learning in memetic algorithms") and is the same credit-assignment machinery as adaptive operator selection in ALNS and selection hyper-heuristics — reuse those reward schemes rather than inventing new ones.

## Practical Challenges

**Local search consumes the whole budget and the GA never gets to act.** With full descents on every child, 95%+ of evaluations happen inside descents and only a handful of generations complete. Cap `ls_max_moves`, apply LS selectively (recipient selection above), and schedule depth: shallow early, deep late. Log the LS share of total evaluations every run; if generations completed < ~20, you are effectively running multistart local search with population-sized overhead.

**The population collapses to near-copies of one local optimum.** Strong local search funnels many children into the same basin; selection then amplifies the copies. Detect via normalized pairwise distance or duplicate-fitness counts. Respond in this order: duplicate elimination at insertion (cheapest), higher mutation/kick strength, distance-based replacement (replace the most similar member rather than the worst), and finally diversity-triggered restarts that keep only elites.

**Crossover children always descend back into a parent's basin.** Then recombination adds nothing and the MA degenerates into parallel ILS. Either the crossover is too disruptive (random offspring land in random basins) or not disruptive enough (clones). Use operators that preserve the components parents share and randomize the rest — adjacency-preserving operators for tours, position-preserving for assignments (see **crossover-operators**) — and verify empirically: measure the fraction of children whose post-descent fitness beats both parents; below ~5%, redesign the operator.

**Baldwinian mode pays for local search twice and shows no benefit.** It spends full descent cost but discards the improved genotype, so progress relies on selection slowly favoring genotypes near good basins. For combinatorial problems with direct encodings this is almost always dominated by Lamarckian writeback (Whitley, Gordon & Mathias 1994). Use Baldwinian only when writeback is impossible; otherwise switch to Lamarckian or partial Lamarckian and re-run the comparison.

**Incremental fitness drifts away from the true objective.** Long chains of delta updates accumulate floating-point error or hide an off-by-one in the delta formula. Recompute the objective from scratch at every elite update and assert agreement within tolerance — exactly what the asserts in both worked examples do. A delta-evaluation bug that survives to the results table is the most expensive bug an MA paper can contain.

**Restarts throw away everything the run has learned.** Pure-random restarts repeat early-run work. Keep elites, locally optimize all fresh members before they enter (or they never win a tournament), bias regeneration with elite frequency statistics, or seed via path relinking between elites. Track best-so-far across restarts separately from the current population's best.

**You cannot tell whether the MA beats its own ingredients.** The mandatory ablation: plain GA (no LS), multistart local search, and ILS, all at the same evaluation or wall-clock budget, same instances, same seed protocol; compare with paired nonparametric tests (see algorithm-benchmarking-statistics). An MA that fails to beat multistart LS is mis-budgeted, not "slightly worse" — fix the budget split before touching operators.

**The same genotypes keep getting re-optimized.** Late-stage populations breed recurring children, and every repeated descent wastes thousands of delta evaluations. Hash genotypes, memoize descent endpoints (the `LSCache` above), and pair the cache with insertion-time duplicate elimination so retrieved duplicates are kicked rather than stored.

## Tools & Libraries

| Library / tool | When to use | Note |
|---|---|---|
| numpy | Every in-house MA in this repo's style | `np.random.default_rng(seed)`; vectorized population, delta, and distance operations |
| numba | Descent inner loops too slow in pure Python | `@njit` the swap/2-opt loops only; keep the orchestration in readable numpy |
| DEAP | Quick GA scaffolding to hybridize | Register local search as an extra step after the variation operators |
| pymoo | Multi-objective memetic variants | Repair/local-search hooks inside NSGA-II-style loops |
| jMetalPy | Cross-metaheuristic comparison studies | Ships GA and local-search templates with shared termination criteria |
| scipy | Exact repair subproblems inside the MA | `optimize.linear_sum_assignment` as a fast assignment-repair step |
| Optuna | Tuning pop size, depth, mutation strength | Tune on a training instance set, evaluate on held-out instances |
| pandas | Experiment bookkeeping | One row per (instance, seed, configuration) run |
| multiprocessing / joblib | Parallel descents across offspring | Descents are independent — embarrassingly parallel; vectorize first, parallelize second |

## Output Format

A complete memetic-algorithm deliverable contains:

1. **Configuration summary** — every parameter and the seed protocol, e.g.:

| Field | Value |
|---|---|
| Algorithm | Lamarckian MA (elitist generational) |
| Encoding | Permutation, n = 100 |
| Crossover / rate | OX / 0.9 |
| Mutation / rate | Double bridge / 0.4 |
| Local search | First-improvement 2-opt, `ls_max_moves` = 20,000 |
| `ls_probability` | 1.0 |
| Population / elites | 20 / 2 |
| Diversity / restart | Hamming, threshold 0.05 |
| Stop | 200 generations or 300 s |
| Seeds | 1–10 |

2. **Budget breakdown** — evaluations (and delta evaluations, counted separately) spent in initialization, variation, and local search; LS share as a percentage; generations completed.
3. **Convergence summary** — best-so-far per generation, mean ± min/max over seeds; generation of last improvement; number of restarts triggered; diversity trace alongside the fitness trace (the diversity collapse usually explains the fitness plateau).
4. **Solution report** — best objective per instance and seed, gap to best-known/optimal where available, and the solution itself validated by an independent recomputation plus a feasibility check (permutation validity, constraint satisfaction), as in both worked examples.
5. **Ablation table** — MA vs GA-only vs multistart-LS vs ILS at identical budgets, with paired statistical test results; without this table, "the hybrid works" is an unsupported claim.
6. **Artifacts** — results as one-row-per-run CSV (instance, seed, config hash, objective, time, evaluations), the convergence histories, and the exact code version (commit hash) that produced them.

## Questions to Ask

- What problem and encoding are we hybridizing for — permutation, binary, integer assignment, or decoder-based?
- Does a local search with delta evaluation already exist, and how long is one full descent on a typical instance?
- What is the evaluation budget — wall-clock seconds, evaluation count, or both — and per instance or total?
- Can improved solutions be written back into the genotype (Lamarckian), or is the encoding indirect?
- How is feasibility handled — feasibility-preserving moves, a repair step, or penalties?
- What must the MA beat — a plain GA, multistart local search, ILS, or a published best-known value?
- How many instances and seeds will the comparison use, and is there a tuning/test split?
- Are restarts acceptable, or must each run be a single trajectory for later analysis?
- Is parallel evaluation available (multiple cores, batch fitness), and should descents run concurrently?

## Related Skills

- **genetic-algorithms** — the underlying evolutionary loop: selection schemes, population sizing, elitism, and the vectorized GA machinery the memetic layer builds on.
- **local-search-and-neighborhoods** — neighborhood design, first vs best improvement, and delta evaluation; the quality of an MA is mostly the quality of this component.
- **fitness-evaluation-and-caching** — delta/incremental evaluation, memoized descents, and batch evaluation; where the MA spends over 90% of its time.
- **quadratic-assignment-problem** — the flagship MA application: QAPLIB instances, delta-table tricks, and the robust tabu search baseline every QAP memetic must beat.
