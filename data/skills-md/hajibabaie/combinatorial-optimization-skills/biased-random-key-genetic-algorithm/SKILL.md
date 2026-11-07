---
name: biased-random-key-genetic-algorithm
description: When the user wants to design, implement, or tune a biased random-key genetic algorithm (BRKGA), where chromosomes are random-key vectors in [0,1), evolution uses elite/mutant partitioning with biased uniform crossover, and a decoder is the only problem-specific component. Also use when the user mentions "BRKGA," "random keys," "random-key encoding," "biased crossover," "decoder," or when genetic operators must never produce infeasible solutions. For decoder design patterns, see decoder-based-representations; for general GA operators and selection, see genetic-algorithms.
---

# Biased Random-Key Genetic Algorithm (BRKGA)

You are an expert in biased random-key genetic algorithms for combinatorial optimization. This skill covers the random-key encoding, the elite/mutant population partition, biased uniform crossover, decoder design as the single problem-specific component, and a reusable numpy framework with two complete worked applications (permutation flow shop with a sort decoder, set covering with a threshold decoder). Use the framework below to assess whether BRKGA fits the problem, build a correct and efficient implementation, and diagnose convergence problems.

## Initial Assessment

Before writing any BRKGA code, establish the following:

- **Solution structure.** What object does a solution decode to: a permutation, a subset, an assignment, a schedule, or a combination? This single fact determines the decoder family (sort, threshold, greedy-priority, multi-segment) and therefore the chromosome length.
- **Chromosome length `n`.** Count the decisions one key must drive. For sequencing, `n` = number of jobs/items. For selection, `n` = number of candidate elements. Multi-segment chromosomes concatenate one key block per decision layer.
- **Decode cost.** Decoding dominates BRKGA runtime; the genetic operators are O(p·n) memory copies and never the bottleneck. Estimate the cost of one decode and multiply by `pop_size × generations`. If a single decode takes more than a few milliseconds, plan for vectorized batch decoding, caching of elite fitness, or parallel decoding from the start.
- **Constraint placement.** Decide, per constraint family, whether the decoder absorbs it (construct only feasible solutions), repairs it (fix violations after a cheap construction), or penalizes it (add a violation term to fitness). BRKGA's main selling point is that the decoder can guarantee feasibility, so prefer absorb/repair over penalties.
- **Objective.** BRKGA as described here minimizes a single scalar. Multi-objective variants exist (NSGA-II-style sorting on top of the BRKGA population) but need extra machinery.
- **Time budget and stopping rule.** Fixed generation count, wall-clock limit, or stall limit (no improvement for `k` generations)? This drives population size: with a tight budget, prefer a smaller population and more generations.
- **Baseline and warm start.** Is there a constructive heuristic (greedy, NEH, LPT) whose output can be encoded as keys and injected into the initial population? Always benchmark BRKGA against that baseline; a metaheuristic that loses to greedy is misconfigured.
- **Library vs. from scratch.** For production use, the maintained `brkga_mp_ipr` packages (Python/C++/Julia) implement multi-parent BRKGA with implicit path relinking. Implement from scratch (as below) when you need full control over the decoder/evaluation loop, vectorization across the population, or research instrumentation.
- **Exact alternative.** If instances are small enough for a MIP solver to close the gap in the available time, use the exact model and keep BRKGA for the large instances or as a warm-start provider.
- **Reproducibility.** Fix seeds for instance generation and for the algorithm separately. Plan multiple independent runs (different algorithm seeds) if you will report statistics.

## Algorithm Anatomy

BRKGA (Gonçalves & Resende, 2011, "Biased random-key genetic algorithms for combinatorial optimization") combines three ideas on top of Bean's random-key GA (Bean, 1994, "Genetic algorithms and random keys for sequencing and optimization"):

**1. Random-key encoding.** A chromosome is a vector $x \in [0,1)^n$. A problem-specific decoder $D$ maps any such vector to a feasible solution, and fitness is

$$ \text{fit}(x) = f(D(x)), \qquad D : [0,1)^n \to S, $$

where $S$ is the feasible set. Because *every* point of the hypercube decodes to something feasible, all genetic operators act on $[0,1)^n$ and never require problem-specific repair. The decoder is the only part you rewrite per problem.

**2. Elite/mutant partition.** Each generation, sort the population of size $p$ by fitness and split it:

- **Elite set** $E$: the best $n_e = \lceil p_e \cdot p \rceil$ chromosomes, copied unchanged to the next generation (strong elitism; best fitness is monotone).
- **Mutants**: $n_m = \lceil p_m \cdot p \rceil$ fresh uniform random vectors. BRKGA has *no per-gene mutation operator*; mutants play that diversification role, like immigrants.
- **Offspring**: the remaining $p - n_e - n_m$ slots, produced by biased crossover.

**3. Biased uniform crossover.** Each offspring takes one parent uniformly from the elite set and one from the non-elite set. Gene $i$ comes from the elite parent with probability $\rho_e > 0.5$:

$$ c_i = \begin{cases} a_i & \text{with probability } \rho_e \quad (a \in E) \\ b_i & \text{otherwise} \quad (b \notin E) \end{cases} $$

This is parameterized uniform crossover (Spears & De Jong, 1991, "On the virtues of parameterized uniform crossover") with the bias always pointing at the better parent. With $\rho_e = 0.7$ an offspring inherits 70% of its genes from an elite chromosome in expectation, so the search drifts toward elite regions while non-elite parents and mutants keep injecting variation. The requirement $p_e < 0.5$ keeps the elite pool smaller than the non-elite pool, which maintains selection pressure.

**Decoder taxonomy.** Choosing the decoder is the real design decision; see **decoder-based-representations** for the full catalog. The common families:

| Decoder family | Maps keys to | Mechanism | Typical problems |
|---|---|---|---|
| Sort decoder | Permutation | `argsort(keys)` is the sequence | Flow shop, single machine, TSP-like orderings |
| Threshold decoder | Subset / binary vector | `key >= 0.5` selects, then repair | Set covering, knapsack, facility selection |
| Greedy-priority decoder | Any constructive solution | Keys are priorities feeding a constructive heuristic | RCPSP serial SGS, parallel machine dispatch, bin packing |
| Allocation decoder | Categorical choice per item | Split $[0,1)$ into intervals, key picks the interval | Machine assignment, mode selection |
| Multi-segment chromosome | Several decisions at once | Concatenate key blocks, one decoder stage per block | Assign-then-sequence scheduling, location-then-routing |

**When to use BRKGA — and when not.**

- Use BRKGA when feasibility is hard to preserve under direct crossover/mutation, when a priority-driven constructive heuristic already exists (wrap it as a greedy decoder), or when you want one tested evolutionary engine reused across many problems with only the decoder changing.
- Prefer a permutation GA with OX/PMX operators (see **genetic-algorithms**) when *adjacency* carries the fitness signal (pure TSP): sort decoders preserve relative order under crossover, not adjacency, so BRKGA needs a local-search hybrid to be competitive there.
- Prefer trajectory methods (tabu search, ILS) when one decode is expensive and a fast incremental (delta) evaluation of small moves exists — population methods cannot exploit delta evaluation as directly.

**Complexity per generation.** Sorting is $O(p \log p)$; crossover and mutant generation are $O(p n)$ vectorized array operations; decoding costs $(p - n_e) \cdot C_{dec}$ because elite fitness is cached. With a sort decoder, $C_{dec} = O(n \log n)$ plus the objective evaluation. The decoder is almost always the bottleneck — vectorize it across the population whenever the construction logic allows.

**Landscape note.** The decoder is many-to-one: uncountably many key vectors map to the same solution (for a sort decoder, only the ordering of keys matters). This redundancy creates plateaus in key space. It is harmless to the dynamics but means diversity must be measured on *decoded solutions or fitness values*, never on raw key distances.

## Core Framework Implementation

The framework is fully problem-independent. Pseudocode first:

```text
BRKGA(decode, p, p_e, p_m, rho_e, G):
    population <- p random vectors drawn uniformly from [0,1)^n
    fitness    <- decode(population)                      # batch evaluation
    repeat G generations:
        sort population by fitness (ascending; minimization)
        ELITE  <- best ceil(p_e * p) chromosomes          # copied unchanged
        MUTANT <- ceil(p_m * p) fresh uniform random vectors
        for each of the p - |ELITE| - |MUTANT| offspring slots:
            a <- chromosome drawn uniformly from ELITE
            b <- chromosome drawn uniformly from NON-ELITE
            for each gene i in 1..n:
                child[i] <- a[i] with probability rho_e, else b[i]
        population <- ELITE  ∪  offspring  ∪  MUTANT
        fitness    <- cached elite fitness  ∪  decode(offspring ∪ MUTANT)
    return best chromosome, decode(best)
```

Save the following as `brkga_core.py`; both worked examples import from it. The `decode` callable receives the whole key matrix at once so problem code can vectorize across the population, and elite fitness values are never recomputed.

```python
"""brkga_core.py — generic BRKGA framework. Only the decoder is problem-specific."""
from dataclasses import dataclass
from typing import Callable

import numpy as np


@dataclass(frozen=True)
class BrkgaParams:
    """Configuration of one BRKGA run (minimization)."""
    n_genes: int
    pop_size: int = 100
    elite_frac: float = 0.20
    mutant_frac: float = 0.15
    rho_e: float = 0.70
    n_generations: int = 200
    seed: int = 0


def brkga(
    decode: Callable[[np.ndarray], np.ndarray],
    params: BrkgaParams,
    init_keys: np.ndarray | None = None,
) -> tuple[np.ndarray, float, list[float]]:
    """Run BRKGA; return (best chromosome, best fitness, best-per-generation history).

    `decode` maps a key matrix of shape (P, n_genes) to a fitness vector of
    shape (P,); lower is better. Rows of `init_keys` (if given) are injected
    into the initial population, e.g. to warm-start from a known solution.
    """
    rng = np.random.default_rng(params.seed)
    p, n = params.pop_size, params.n_genes
    n_elite = max(1, int(round(params.elite_frac * p)))
    n_mutant = max(1, int(round(params.mutant_frac * p)))
    n_offspring = p - n_elite - n_mutant

    pop = rng.random((p, n))
    if init_keys is not None:
        pop[: len(init_keys)] = init_keys
    fit = np.asarray(decode(pop), dtype=float)

    history: list[float] = []
    for _ in range(params.n_generations):
        order = np.argsort(fit)
        pop, fit = pop[order], fit[order]
        history.append(float(fit[0]))

        elite_parent = rng.integers(0, n_elite, size=n_offspring)
        other_parent = rng.integers(n_elite, p, size=n_offspring)
        from_elite = rng.random((n_offspring, n)) < params.rho_e
        offspring = np.where(from_elite, pop[elite_parent], pop[other_parent])
        mutants = rng.random((n_mutant, n))

        new_part = np.vstack([offspring, mutants])
        pop = np.vstack([pop[:n_elite], new_part])
        fit = np.concatenate([fit[:n_elite], np.asarray(decode(new_part), dtype=float)])

    best = int(np.argmin(fit))
    history.append(float(fit[best]))
    return pop[best].copy(), float(fit[best]), history
```

Implementation notes:

- The biased crossover is one `np.where` over a Boolean mask — all offspring for the generation are produced in a single vectorized expression.
- Elite chromosomes carry their cached fitness forward; only `offspring + mutants` are decoded each generation. With `p_e = 0.2`, that alone saves 20% of all decode work.
- The framework never inspects the decoded solutions. Re-decode the returned best chromosome in problem code to materialize the actual solution object.
- The decoder must be a deterministic function of the keys. If it were stochastic, cached elite fitness would diverge from re-decoded values and the monotonicity guarantee (and its use as a correctness check) would be lost.
- Maximization problems: negate the objective inside `decode`; keep the framework minimizing.

**Parameter guidance** (recommended ranges follow Gonçalves & Resende, 2011):

| Parameter | Symbol | Typical range | What it trades off |
|---|---|---|---|
| Population size | $p$ | $\max(100,\ n)$ up to $10n$ | Larger: broader sampling per generation, fewer generations per time budget. Scale with chromosome length. |
| Elite fraction | $p_e$ | 0.10 – 0.25 | Larger: stronger intensification and more cached fitness, but faster diversity loss and smaller offspring pool. Must stay below 0.5. |
| Mutant fraction | $p_m$ | 0.10 – 0.30 | Larger: more diversification (resistance to stagnation), fewer offspring doing directed search. |
| Elite inheritance | $\rho_e$ | 0.55 – 0.80 (0.70 is the standard default) | Higher: offspring closer to elite parents — faster convergence, higher premature-convergence risk. |
| Generations / stop | $G$ | Budget-driven; stall limit of $n$ – $2n$ generations is common | More generations help only while diversity remains; pair long budgets with restarts (see Advanced Techniques). |

Selection, replacement, and crossover are fixed by the method — do not graft tournament selection or per-gene mutation onto BRKGA; if you need those degrees of freedom, you want a classic GA (see **genetic-algorithms**) instead.

## Worked Example 1: Permutation Flow Shop with a Sort Decoder

**Problem.** $n$ jobs are processed by $m$ machines in the same machine order; one permutation $\pi$ of the jobs is used on every machine (permutation flow shop, $F_m \mid prmu \mid C_{\max}$). With processing times $p_{ij}$ for machine $i$ and job $j$, completion times follow the recurrence

$$ C_{i,\pi(k)} = \max\!\left(C_{i,\pi(k-1)},\; C_{i-1,\pi(k)}\right) + p_{i,\pi(k)}, $$

and the objective is the makespan $C_{\max} = C_{m,\pi(n)}$. The problem is NP-hard for $m \ge 3$. See **flow-shop-scheduling** for exact models, NEH, and the full heuristic landscape; here it serves as the canonical sort-decoder application.

**Encoding.** One key per job; `argsort(keys)` is the job sequence. Crossover on keys can produce any permutation, and every key vector decodes to a valid sequence — no repair, ever.

The instance generator and a population-batched makespan evaluator (the recurrence runs once over jobs and machines, but for *all* chromosomes simultaneously):

```python
"""flow_shop.py — instance generator and batched makespan evaluation."""
import numpy as np


def random_flow_shop(n_jobs: int, n_machines: int, seed: int) -> np.ndarray:
    """Taillard-style instance: integer times in [1, 99], shape (n_machines, n_jobs)."""
    rng = np.random.default_rng(seed)
    return rng.integers(1, 100, size=(n_machines, n_jobs)).astype(float)


def makespan_batch(perms: np.ndarray, proc: np.ndarray) -> np.ndarray:
    """Makespan of each job permutation. perms: (P, n) int; proc: (m, n) float."""
    n_pop, n_jobs = perms.shape
    n_mach = proc.shape[0]
    seq_times = proc[:, perms]                # (m, P, n): times in sequence order
    comp = np.zeros((n_pop, n_mach))          # completion time per (chromosome, machine)
    for j in range(n_jobs):
        stage = seq_times[:, :, j].T          # (P, m): j-th sequenced job, each machine
        comp[:, 0] += stage[:, 0]
        for i in range(1, n_mach):
            comp[:, i] = np.maximum(comp[:, i], comp[:, i - 1]) + stage[:, i]
    return comp[:, -1]
```

The loop nest is $O(nm)$ Python iterations, but each iteration is vectorized over the whole population, so evaluating 100 chromosomes costs barely more than evaluating one. The decoder and driver:

```python
"""run_flow_shop.py — BRKGA with a sort decoder on the permutation flow shop."""
import numpy as np

from brkga_core import BrkgaParams, brkga
from flow_shop import makespan_batch, random_flow_shop


def make_flow_shop_decoder(proc: np.ndarray):
    """Sort decoder: argsort of the keys is the job sequence."""
    def decode(keys: np.ndarray) -> np.ndarray:
        perms = np.argsort(keys, axis=1)      # (P, n) permutations, vectorized
        return makespan_batch(perms, proc)
    return decode


def makespan_single(perm: np.ndarray, proc: np.ndarray) -> float:
    """Independent scalar validator for one permutation."""
    n_mach = proc.shape[0]
    comp = np.zeros(n_mach)
    for j in perm:
        comp[0] += proc[0, j]
        for i in range(1, n_mach):
            comp[i] = max(comp[i], comp[i - 1]) + proc[i, j]
    return float(comp[-1])


if __name__ == "__main__":
    proc = random_flow_shop(n_jobs=20, n_machines=5, seed=42)
    params = BrkgaParams(n_genes=20, pop_size=100, elite_frac=0.20,
                         mutant_frac=0.15, rho_e=0.70, n_generations=200, seed=1)
    best_keys, best_makespan, history = brkga(make_flow_shop_decoder(proc), params)
    best_perm = np.argsort(best_keys)

    assert makespan_single(best_perm, proc) == best_makespan
    print(f"makespan: {history[0]:.0f} (gen 0 best) -> {best_makespan:.0f} (final)")
    print("sequence:", best_perm.tolist())
    # Expected: makespan 1351 (gen 0 best) -> 1243 (final) for these exact seeds;
    # history is non-increasing because the elite set is copied unchanged.
```

Two things to verify on any sort-decoder application: (a) the validator (`makespan_single`) recomputes the objective independently of the batched evaluator — they must agree exactly; (b) the history is monotone non-increasing — if it is not, elite fitness caching or the sort is broken.

## Worked Example 2: Set Covering with a Threshold Decoder

**Problem.** Given a 0/1 matrix $A \in \{0,1\}^{r \times c}$ and column costs $c_j > 0$, select a minimum-cost set of columns covering every row:

$$ \min \sum_{j} c_j y_j \quad \text{s.t.} \quad \sum_{j} a_{ij}\, y_j \ge 1 \;\; \forall i, \qquad y \in \{0,1\}^c. $$

**Encoding.** One key per column. The **threshold decoder** selects column $j$ when $x_j \ge 0.5$. Unlike the sort decoder, the raw selection can be infeasible (uncovered rows) or wasteful (redundant columns), so the decoder embeds two deterministic post-steps:

1. **Greedy repair** — while rows remain uncovered, add the unselected column minimizing cost per newly covered row (the classic Chvátal greedy ratio).
2. **Redundancy pruning** — scan selected columns in decreasing cost order and drop any column whose rows are all covered at least twice.

Because repair and pruning are deterministic, the decoder is still a well-defined function from keys to feasible solutions. Instance generator first:

```python
"""set_cover.py (part 1) — random SCP instance generator."""
import numpy as np


def random_set_cover(
    n_rows: int, n_cols: int, density: float, seed: int
) -> tuple[np.ndarray, np.ndarray]:
    """Random SCP: boolean cover matrix A (n_rows x n_cols) and integer column costs.

    Patches the random matrix so every row is coverable and no column is empty,
    which guarantees feasibility of the instance.
    """
    rng = np.random.default_rng(seed)
    A = rng.random((n_rows, n_cols)) < density
    for i in np.flatnonzero(~A.any(axis=1)):      # every row coverable
        A[i, rng.integers(n_cols)] = True
    for j in np.flatnonzero(~A.any(axis=0)):      # no useless columns
        A[rng.integers(n_rows), j] = True
    cost = rng.integers(1, 100, size=n_cols).astype(float)
    return A, cost
```

Repair, pruning, and an independent feasibility validator:

```python
"""set_cover.py (part 2) — repair, redundancy pruning, and validation."""
import numpy as np


def repair_and_prune(selected: np.ndarray, A: np.ndarray, cost: np.ndarray) -> np.ndarray:
    """Greedy repair (min cost per newly covered row), then drop redundant columns."""
    selected = selected.copy()
    covered = A[:, selected].any(axis=1) if selected.any() else np.zeros(A.shape[0], bool)
    while not covered.all():
        gain = A[~covered].sum(axis=0).astype(float)   # newly covered rows per column
        gain[selected] = 0.0
        ratio = np.where(gain > 0, cost / np.maximum(gain, 1e-12), np.inf)
        j = int(np.argmin(ratio))
        selected[j] = True
        covered |= A[:, j]
    count = A[:, selected].sum(axis=1)                 # coverage multiplicity per row
    for j in sorted(np.flatnonzero(selected), key=lambda col: -cost[col]):
        rows_j = A[:, j]
        if (count[rows_j] >= 2).all():
            selected[j] = False
            count[rows_j] -= 1
    return selected


def validate_cover(selected: np.ndarray, A: np.ndarray, cost: np.ndarray) -> float:
    """Independent check: raise if any row is uncovered, else return total cost."""
    if not A[:, selected].any(axis=1).all():
        raise ValueError("infeasible: some row is uncovered")
    return float(cost[selected].sum())
```

Decoder and driver. The thresholding is vectorized; repair is inherently sequential (each greedy pick changes the next pick), so it runs per chromosome — this is the expected shape for repair-based decoders, and the reason decode cost must be assessed up front:

```python
"""run_set_cover.py — BRKGA with a threshold decoder on set covering."""
import numpy as np

from brkga_core import BrkgaParams, brkga
from set_cover import random_set_cover, repair_and_prune, validate_cover


def make_scp_decoder(A: np.ndarray, cost: np.ndarray):
    """Threshold decoder: key >= 0.5 selects a column; repair restores feasibility."""
    def decode(keys: np.ndarray) -> np.ndarray:
        raw = keys >= 0.5                       # vectorized over the population
        vals = np.empty(len(keys))
        for k in range(len(keys)):              # repair is sequential per chromosome
            sel = repair_and_prune(raw[k], A, cost)
            vals[k] = cost[sel].sum()
        return vals
    return decode


if __name__ == "__main__":
    A, cost = random_set_cover(n_rows=40, n_cols=120, density=0.06, seed=7)
    params = BrkgaParams(n_genes=120, pop_size=120, elite_frac=0.20,
                         mutant_frac=0.15, rho_e=0.70, n_generations=150, seed=1)
    best_keys, best_cost, history = brkga(make_scp_decoder(A, cost), params)
    best_sel = repair_and_prune(best_keys >= 0.5, A, cost)

    greedy = repair_and_prune(np.zeros(120, dtype=bool), A, cost)
    print(f"BRKGA cost {validate_cover(best_sel, A, cost):.0f} "
          f"({int(best_sel.sum())} columns), greedy {validate_cover(greedy, A, cost):.0f}")
    # Expected: BRKGA cost 361 (17 columns) vs greedy 392 for these exact seeds;
    # BRKGA's gen-0 best is 417 and improves monotonically to 361.
```

Note the built-in baseline: decoding the all-zeros selection runs pure greedy-plus-pruning. BRKGA must beat it; if it does not, the decoder, parameters, or budget are wrong. Also note the fitness reported by `decode` is the *repaired* solution's cost — the chromosome itself is not changed (a "Cartesian" decoder). The Lamarckian alternative that writes the repair back into the keys is covered under Advanced Techniques.

## Advanced Techniques

### Warm starts and solution injection

Any known solution can be encoded as keys and injected via `init_keys`. For a sort decoder, build keys whose argsort reproduces a given permutation (e.g., from NEH — Nawaz, Enscore & Ham, 1983 — for flow shop, or LPT for **parallel-machine-scheduling** dispatch decoders):

```python
import numpy as np


def keys_from_permutation(perm: np.ndarray) -> np.ndarray:
    """Keys whose argsort reproduces `perm`; values spread uniformly over (0, 1)."""
    n = len(perm)
    keys = np.empty(n)
    keys[perm] = (np.arange(n) + 0.5) / n
    return keys


def jittered_copies(keys: np.ndarray, n_copies: int, sigma: float, seed: int) -> np.ndarray:
    """Stack of perturbed copies, clipped to [0, 1); avoids seeding identical clones."""
    rng = np.random.default_rng(seed)
    noise = rng.normal(0.0, sigma, size=(n_copies, len(keys)))
    return np.clip(keys + noise, 0.0, np.nextafter(1.0, 0.0))


perm = np.array([3, 0, 2, 1])
seeds = jittered_copies(keys_from_permutation(perm), n_copies=3, sigma=0.02, seed=0)
assert (np.argsort(keys_from_permutation(perm)) == perm).all()
# Expected: assertion passes; `seeds` holds 3 near-copies that mostly decode to perm.
```

Inject one exact copy plus a few jittered copies — never fill a large share of the population with one solution, or the elite set collapses to clones in the first generation. See **warm-starts** discussion in the Practical Challenges section below for the failure mode.

### Multi-parent crossover and implicit path relinking (BRKGA-MP-IPR)

Andrade, Toso, Gonçalves & Resende (2021, "The Multi-Parent Biased Random-Key Genetic Algorithm with Implicit Path Relinking and its real-world applications") generalize the two-parent crossover: each offspring has $\pi_t$ parents ($\pi_e$ of them elite), and each gene is copied from a parent chosen with rank-based bias weights, e.g. $w_r \propto 1/r$ for parent rank $r$. Two parents with $\rho_e = w_1/(w_1+w_2)$ recovers classic BRKGA.

```python
import numpy as np


def multi_parent_offspring(
    pop_sorted: np.ndarray,
    n_elite: int,
    n_offspring: int,
    total_parents: int,
    elite_parents: int,
    rng: np.random.Generator,
) -> np.ndarray:
    """BRKGA-MP gene transfer: each gene copied from one of `total_parents` parents,
    chosen with rank bias w_r = 1/r (Andrade et al., 2021). Assumes fitness-sorted pop."""
    p, n = pop_sorted.shape
    e_idx = rng.integers(0, n_elite, size=(n_offspring, elite_parents))
    o_idx = rng.integers(n_elite, p, size=(n_offspring, total_parents - elite_parents))
    parents = np.concatenate([e_idx, o_idx], axis=1)
    ranked = np.sort(parents, axis=1)          # lower population index = better rank
    weights = 1.0 / np.arange(1, total_parents + 1)
    choice = rng.choice(total_parents, size=(n_offspring, n), p=weights / weights.sum())
    src = ranked[np.arange(n_offspring)[:, None], choice]
    return pop_sorted[src, np.arange(n)]


rng = np.random.default_rng(0)
pop = rng.random((20, 6))
children = multi_parent_offspring(pop, n_elite=4, n_offspring=10,
                                  total_parents=5, elite_parents=2, rng=rng)
# Expected: children.shape == (10, 6); every gene equals some parent's gene.
```

*Implicit path relinking* (IPR) intensifies between two elite chromosomes without a problem-specific neighborhood: walk from one key vector toward the other by adopting blocks of keys (direct IPR) or block-induced permutation fragments (permutation IPR), decoding intermediate points and keeping the best. It is the standard answer when plain BRKGA stalls a few percent above best-known values; use the `brkga_mp_ipr` package rather than reimplementing IPR.

### Shaking and restarts

BRKGA's elitism makes stagnation visible: the best value flatlines. Two standard escapes, in increasing strength — *shaking* re-randomizes a fraction of elite genes in place; a *restart* rebuilds the population from scratch, optionally re-injecting a shaken incumbent:

```python
import dataclasses

import numpy as np

from brkga_core import BrkgaParams, brkga


def shake(elite_keys: np.ndarray, intensity: float, rng: np.random.Generator) -> np.ndarray:
    """Re-randomize a fraction `intensity` of elite genes (Andrade et al., 2021)."""
    mask = rng.random(elite_keys.shape) < intensity
    return np.where(mask, rng.random(elite_keys.shape), elite_keys)


def brkga_multistart(decode, params: BrkgaParams, n_starts: int,
                     shake_intensity: float = 0.2, n_injected: int = 2):
    """Sequential restarts; each restart re-seeds the population and injects
    shaken copies of the incumbent best chromosome."""
    rng = np.random.default_rng(params.seed)
    best_keys, best_val = None, np.inf
    for s in range(n_starts):
        run = dataclasses.replace(params, seed=params.seed + 1000 * (s + 1))
        init = None
        if best_keys is not None:
            init = shake(np.tile(best_keys, (n_injected, 1)), shake_intensity, rng)
        keys, val, _ = brkga(decode, run, init_keys=init)
        if val < best_val:
            best_keys, best_val = keys.copy(), val
    return best_keys, best_val
# Expected: returned best_val <= the single-run value for the same total budget
# on stagnation-prone instances; equal otherwise.
```

A practical trigger: restart when the best value has not improved for `n_genes` to `2 * n_genes` generations. Spend a long time budget as several restarts rather than one long run.

### Island model with elite migration

Run $K$ independent populations and periodically migrate elites along a ring. Islands restore diversity at the population level and parallelize trivially (one process per island):

```python
import numpy as np


def migrate_ring(pops: list[np.ndarray], fits: list[np.ndarray], n_migrants: int) -> None:
    """Ring migration: best n_migrants of island k overwrite the worst of island k+1.
    Migrant fitness travels with the keys, so no re-decoding is needed."""
    snapshots = [
        (pop[np.argsort(fit)[:n_migrants]].copy(), np.sort(fit)[:n_migrants])
        for pop, fit in zip(pops, fits)
    ]
    for k in range(len(pops)):
        dst = (k + 1) % len(pops)
        worst = np.argsort(fits[dst])[-n_migrants:]
        pops[dst][worst], fits[dst][worst] = snapshots[k]


rng = np.random.default_rng(0)
pops = [rng.random((30, 8)) for _ in range(4)]
fits = [rng.random(30) for _ in range(4)]
migrate_ring(pops, fits, n_migrants=2)
# Expected: each island now contains the previous island's two best chromosomes.
```

Typical settings: 2–4 islands, migrate every 25–100 generations, 1–3 migrants. More frequent migration makes the islands behave like one population and loses the benefit.

### Lamarckian decoders and online parameter control

A *Lamarckian* decoder writes its repair/local-search result back into the chromosome so the improvement is inherited. For a threshold decoder, reflect each key to the side of 0.5 matching the repaired solution — deterministic and information-preserving:

```python
import numpy as np


def lamarckian_threshold_keys(keys: np.ndarray, selected: np.ndarray) -> np.ndarray:
    """Push each key to the side of 0.5 that matches the repaired selection."""
    flip = selected != (keys >= 0.5)
    new = keys.copy()
    new[flip] = 1.0 - keys[flip]
    return new


keys = np.array([0.10, 0.90, 0.60, 0.40])
selected = np.array([True, True, False, False])
print(lamarckian_threshold_keys(keys, selected))
# Expected: [0.9 0.9 0.4 0.4] — genes 0 and 2 reflected across 0.5, others kept.
```

Lamarckian write-back accelerates convergence but reduces diversity; combine it with a higher mutant fraction. The same idea applies after embedding local search in the decoder (a memetic BRKGA): decode, improve with 2-opt/swap descent, write the improved solution's keys back. For online parameter control, the adaptive BRKGA of Chaves, Gonçalves & Lorena (2018, "Adaptive biased random-key genetic algorithm with local search for the capacitated centered clustering problem") shrinks $p_m$ and grows $\rho_e$ over the run, trading early exploration for late intensification — a sensible default schedule when tuning budget is scarce.

## Practical Challenges

**Decoding dominates runtime and the run crawls.** Profile first: in a correct BRKGA, >90% of time is decode. Then (a) vectorize the evaluation across the population as in `makespan_batch`; (b) exploit the framework's elite-fitness caching — never re-decode elites; (c) parallelize per-chromosome decoders (sequential repairs) across processes; (d) JIT-compile sequential repair loops with numba. Only after these, reduce `pop_size`.

**The population converges to copies of one solution in a few dozen generations.** Diversity collapse. Check $p_e \le 0.25$ and $\rho_e \le 0.8$; raise $p_m$ toward 0.3; add duplicate elimination — but compare *decoded* solutions or fitness fingerprints, not key vectors, because the decoder is many-to-one and distinct keys can hide identical solutions. If collapse recurs, add shaking/restarts.

**Best fitness history is not monotone non-increasing.** This is a bug, not noise: BRKGA copies elites unchanged, so the generation-best can never get worse. Usual causes: elite fitness not carried over with the elite keys after sorting, a stochastic decoder (decoder must be a deterministic function of the keys — fix any internal randomness with a hash of the chromosome if randomness is truly needed), or fitness recomputed with a different formula than reported.

**Warm-start injection makes results worse than cold start.** Too many copies of one solution seize the elite set in generation 0 and the run degenerates to mutation-only search around it. Inject 1 exact copy plus 2–3 jittered copies (`jittered_copies` above), never more than ~5% of the population.

**The threshold decoder spends all its time in repair on early generations.** With uniform keys, expected initial selection density is 0.5 — far above typical SCP solution density, so pruning does heavy work; in packing-type problems the same bias causes mass infeasibility. Fix the prior: draw initial keys (and mutants) from a Beta distribution or shift the threshold so expected density matches a greedy solution's density.

**Sort decoder behaves erratically after key write-back or injection.** Tied keys decode by `argsort`'s stable index order, which silently biases sequences. Continuous random keys never tie, but injected or reflected keys can. Add tiny uniform jitter (e.g., $10^{-9}$ scale) when constructing keys from solutions.

**BRKGA stalls a few percent above best-known values on routing-flavored problems.** Random keys preserve relative order through crossover, not adjacency, so edge-based structure is invisible to the operators. Either embed local search in the decoder (memetic BRKGA, Lamarckian write-back) or switch the representation — this is a model-choice problem, not a tuning problem.

**Too many parameters to tune and no budget.** Defaults $p = \max(100, n)$, $p_e = 0.2$, $p_m = 0.15$, $\rho_e = 0.7$ are robust starting points (Gonçalves & Resende, 2011). If tuning is worthwhile, tune $\rho_e$ and $p_m$ first; population size mostly trades quality for time. The decoder design moves results far more than any parameter — invest there.

## Tools & Libraries

| Library | When to use | Note |
|---|---|---|
| `brkga_mp_ipr` (Python) | Production / research use of BRKGA-MP-IPR without reimplementing | Official multi-parent + implicit path relinking implementation; config-file driven; Andrade et al. (2021). |
| brkgaAPI (C++) | Performance-critical decoders, large instances | Classic templated API of Toso & Resende (2015, "A C++ application programming interface for biased random-key genetic algorithms"); OpenMP-parallel decoding. |
| `brkga_mp_ipr` (Julia/C++) | Same algorithm, other host languages | Same API family; pick the language your decoder lives in. |
| numpy | The framework in this skill; vectorized crossover and batch decoding | `np.random.default_rng(seed)`; keep population, keys, and fitness as arrays. |
| numba | Per-chromosome sequential decoders (greedy repair, SGS) too slow in Python | `@njit` the repair loop; keep the framework itself in plain numpy. |
| multiprocessing / joblib | Expensive per-chromosome decoders that resist vectorization | Decode chunks of the offspring matrix in worker processes; islands map to processes naturally. |
| Optuna | Tuning $(p, p_e, p_m, \rho_e)$ on a training instance set | Tune on small instances, validate on held-out large ones; tune $\rho_e$, $p_m$ first. |

## Output Format

A complete BRKGA deliverable contains:

**1. Configuration summary** — every value needed to reproduce the run:

| Item | Value |
|---|---|
| Problem / instance | SCP, 40 rows × 120 cols, density 0.06, instance seed 7 |
| Encoding / decoder | one key per column; threshold 0.5 + greedy repair + pruning |
| pop_size / elite / mutant / rho_e | 120 / 0.20 / 0.15 / 0.70 |
| Generations / stop rule | 150 fixed (or: stall limit 240) |
| Algorithm seed(s) | 1 (single run) or list for replications |
| Framework version | brkga_core.py at commit hash |

**2. Solution-quality report** — final objective, gap to baseline and (if known) to best-known/optimal value, independent validation result. Always state the baseline: "BRKGA 361 vs. greedy 392 (−7.9%); feasibility confirmed by `validate_cover`."

**3. Convergence summary** — generation of last improvement, best-per-generation history (plot or table at checkpoints 0/25/50/100%), and whether the stall criterion fired. A run that improves in the final 10% of generations was stopped too early.

**4. Runtime breakdown** — total wall time, share spent in `decode` (expected: dominant), decodes per second. This tells the reader whether the next improvement should target the decoder or the search.

**5. Replication statistics** (when comparing methods) — per-seed final values, mean/median/std and a distribution plot over ≥10 seeds; never report a single lucky run when a comparison claim is made.

**6. File artifacts** — `brkga_core.py` (framework), one `<problem>.py` (instance + evaluator + validator), one `run_<problem>.py` (decoder + driver), and a results table (CSV) of per-run outcomes.

## Questions to Ask

- What does one solution look like structurally — a permutation, a subset, an assignment, or several of these at once?
- Is there an existing constructive heuristic we can drive with priorities (that becomes the decoder)?
- How expensive is evaluating one solution, and what is the total wall-clock budget?
- Which constraints must the decoder absorb or repair, and which can be penalized?
- How large are the instances (chromosome length), and how many instances must be solved?
- What is the quality bar: beat a stated baseline, match published best-known values, or "good solution fast"?
- Are known good solutions available for warm-starting?
- Is a single run enough, or do you need statistics over seeds for a publication-grade comparison?
- Should we use the maintained `brkga_mp_ipr` package, or is a from-scratch implementation required (custom instrumentation, vectorized decoding)?

## Related Skills

- **decoder-based-representations** — when the decoder itself needs design work: full catalog of sort, threshold, greedy/SGS, allocation, and multi-segment decoders and their feasibility guarantees.
- **genetic-algorithms** — when BRKGA's fixed operator set is too rigid and you need general GA machinery: selection schemes, permutation crossovers, mutation operators, replacement strategies.
- **flow-shop-scheduling** — when the application is the flow shop itself: exact MIP models, NEH and other constructive heuristics, lower bounds, and benchmark instances beyond the sort-decoder example here.
- **parallel-machine-scheduling** — when keys should drive a dispatch/assignment decoder for identical or unrelated parallel machines: list-scheduling decoders, LPT seeds, and makespan/total-completion-time objectives.
