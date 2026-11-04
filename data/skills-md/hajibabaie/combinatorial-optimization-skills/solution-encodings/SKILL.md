---
name: solution-encodings
description: When the user wants to choose or design a solution representation for a metaheuristic — binary, integer, real-valued, permutation, matrix, set-based, or mixed — and judge candidates by locality, redundancy, feasibility coverage, and bias. Also use when the user mentions "solution representation," "encoding," "permutation encoding," "binary encoding," "genotype," "representation choice," or when operators keep producing infeasible or invalid offspring. For indirect encodings and decoder design, see decoder-based-representations; for recombination operators per encoding, see crossover-operators.
---

# Solution Encodings

You are an expert in solution representations for combinatorial optimization. This skill covers the catalog of direct encodings (binary, integer, real-valued, permutation, matrix, set-based, mixed), the formal criteria for judging a representation (completeness, locality, redundancy, feasibility coverage, bias), and the compatibility between encodings, variation operators, and algorithm families. Use the framework below to pick the representation first — it constrains every later design decision — and to diagnose representation problems in an existing metaheuristic.

## Initial Assessment

Establish these facts before recommending an encoding:

- **Decision structure.** Classify what a solution actually decides: a subset (selection), an assignment (item to resource), a sequence (ordering), a grouping (partition), continuous parameters, or several of these at once. The decision structure, not the algorithm, drives the encoding choice.
- **Constraint inventory.** List every hard constraint and mark which ones the encoding could enforce structurally (e.g., a permutation enforces "each job exactly once" for free), which need a repair or decoder, and which must go to penalties.
- **Solution size.** Get concrete numbers: how many bits, integers, or positions per genotype. Encodings that are fine at n = 50 can be hopeless at n = 5,000 (e.g., a full n×m binary matrix when an integer vector of length n suffices).
- **Evaluation cost and decode cost.** Ask how expensive one fitness evaluation is. If the objective is cheap, a decoder that costs O(n log n) per evaluation may dominate runtime; if the objective is a simulation, decoder cost is irrelevant.
- **Algorithm constraints.** Determine whether the algorithm is already fixed. Differential evolution and particle swarm operate on real vectors; a genetic algorithm accepts any encoding with matching operators; local search only needs a neighborhood. A fixed algorithm narrows the encoding shortlist.
- **Operator availability.** Check which crossover/mutation operators the user's codebase or library already provides. An exotic encoding without tested operators is a liability.
- **Known structure of good solutions.** Ask whether good solutions are known to be balanced, sparse, clustered, or otherwise structured. A biased decoder that concentrates sampling on that structure can be a large win — or a coverage hole if the structure assumption is wrong.
- **Feasibility ratio.** Estimate what fraction of random genotypes is feasible. Below roughly 1% feasible, plan for repair or a feasibility-enforcing decoder from the start.
- **Reproducibility needs.** Confirm seeds will be threaded through all sampling (`np.random.default_rng(seed)` everywhere) so encoding experiments are repeatable.
- **Validation plan.** Agree on an invariant checker (e.g., "is this row a valid permutation?") that runs after every custom operator during development.

## Representation Anatomy and Selection Criteria

A representation is a pair: a **genotype space** $G$ that operators act on, and a mapping $p : G \to P$ into the **phenotype space** $P$ of actual solutions. For direct encodings $p$ is the identity or a trivial reshape; for indirect encodings $p$ is a decoder (covered in depth in decoder-based-representations). Five criteria, following Rothlauf (2006), *Representations for Genetic and Evolutionary Algorithms*, determine whether a representation will help or hurt:

1. **Completeness / coverage.** Every feasible phenotype should be the image of at least one genotype. A coverage hole that excludes the optimum is fatal and silent: the algorithm converges normally to the best *representable* solution. Always check whether a known good solution (from a heuristic or a small exact run) is encodable.
2. **Locality.** Small genotype changes should produce small phenotype (and fitness) changes. High locality lets local search and mutation exploit gradients in the landscape. A useful empirical proxy is

$$ L = \mathbb{E}\big[\, |f(m(g)) - f(g)| \,\big], $$

   the mean fitness jump under one minimal mutation $m$; compare candidate encodings under the same mutation budget (implementation in Advanced Techniques).
3. **Redundancy.** If many genotypes map to one phenotype ($|G| \gg |P|$), search effort is spent on neutral moves. *Synonymous* redundancy (redundant genotypes are neighbors, as with random keys) is mostly harmless and can even help by adding neutral paths; *non-synonymous* redundancy (the same phenotype reachable from distant genotype regions) fragments the population and slows convergence.
4. **Feasibility coverage.** The fraction of genotype space that decodes to feasible phenotypes. Permutations give 100% feasibility for "visit each once" constraints; a naive binary matrix for the same constraint gives a vanishing fraction (quantified in the worked example below).
5. **Bias.** The phenotype distribution induced by uniform genotype sampling. Unbiased is the safe default; deliberate bias toward known-good structure (e.g., a list-scheduling decoder that only produces non-delay schedules) trades coverage for sampling efficiency. State the bias explicitly so it is a design decision, not an accident.

### Genotype space sizes

| Encoding | Genotype space | Size at n = 20, k = 5 | Structural constraint enforced |
|---|---|---|---|
| Binary vector | $\{0,1\}^n$ | $2^{20} \approx 10^6$ | none |
| Integer vector | $\{0..k-1\}^n$ | $5^{20} \approx 10^{14}$ | each item gets exactly one value |
| Real vector | $[l,u]^n$ | continuous | box bounds |
| Permutation | $S_n$ | $20! \approx 2.4\times10^{18}$ | each element exactly once |
| Binary matrix (one-hot) | one 1 per row | $k^n$ (after repair) | assignment, both axes visible |
| Set (variable size) | $2^{U}$ | $2^{20} \approx 10^6$ | membership only |
| Random keys | $[0,1]^n$ | continuous; $n!$ effective | feasibility via decoder |

### Decision guidance

- **Subset selection** (knapsack, feature selection, set covering): binary vector when the universe is small and dense; set-based when solutions are sparse (a few dozen members out of millions of candidates).
- **Assignment / grouping** (machine assignment, clustering, coloring): integer vector indexed by item, value = resource/group. Switch to a matrix view only when constraints act on both axes simultaneously (e.g., per-resource cardinality and per-item exclusions) and you want operators that see columns.
- **Sequencing** (TSP, flow shop, single-machine scheduling): permutation. Be explicit about which of the three permutation semantics carries the fitness — position, precedence/order, or adjacency — because operators preserve different properties (see crossover-operators).
- **Sequencing with a real-vector algorithm** (DE, PSO, ES, BRKGA): random keys, decoded by argsort. This is the standard bridge from continuous operators to permutation problems (Bean, 1994, *Genetic algorithms and random keys for sequencing and optimization*).
- **Continuous parameters**: real vector with explicit bounds and a bound-handling rule (clip, reflect, resample).
- **Several coupled decision types** (open facilities + customer assignment; routes + packing): mixed genotype with one segment per decision type, or a single simpler genotype plus a decoder that derives the dependent decisions greedily.
- **Heavily constrained problems** where random genotypes are almost never feasible: prefer a feasibility-enforcing decoder over repair-after-the-fact; see decoder-based-representations.

Complexity note: encoding choice fixes the per-evaluation overhead. Direct encodings decode in O(1)–O(n); argsort decoders cost O(n log n); list-scheduling and insertion decoders cost O(n·m) or O(n²). Multiply by the evaluation budget (often 10⁵–10⁷) before accepting a slow decoder.

## Encoding Catalog

Each entry: when to use it, a numpy implementation, complexity, and where it fits. All implementations are population-oriented and vectorized where broadcasting applies.

### Binary vectors

Use for subset selection and yes/no decision sets. Fits genetic algorithms (the classic home turf), simulated annealing with bit-flip neighborhoods, estimation-of-distribution algorithms (UMDA/PBIL build probability vectors directly on bits). Constraints like capacity are NOT structural — pair the encoding with repair or penalties. When binary strings encode *integers*, standard binary positional coding creates Hamming cliffs (7→8 flips four bits); reflected Gray code makes adjacent integers differ in one bit (Caruana & Schaffer, 1988, *Representation and hidden bias: Gray vs. binary coding for genetic algorithms*).

```python
import numpy as np


def init_binary_population(pop_size: int, n_bits: int, p_one: float, seed: int) -> np.ndarray:
    """Sample a binary population of shape (pop_size, n_bits) with P(bit = 1) = p_one."""
    rng = np.random.default_rng(seed)
    return (rng.random((pop_size, n_bits)) < p_one).astype(np.int8)


def repair_knapsack(pop: np.ndarray, values: np.ndarray, weights: np.ndarray,
                    capacity: float) -> np.ndarray:
    """Drop the worst value/weight items from overweight genotypes until feasible."""
    pop = pop.copy()
    loads = pop @ weights
    drop_order = np.argsort(values / weights)  # worst ratio first
    for i in np.flatnonzero(loads > capacity):
        for j in drop_order:
            if loads[i] <= capacity:
                break
            if pop[i, j]:
                pop[i, j] = 0
                loads[i] -= weights[j]
    return pop


def binary_to_gray(bits: np.ndarray) -> np.ndarray:
    """Reflected Gray code, row-wise, most significant bit first."""
    gray = bits.copy()
    gray[:, 1:] = bits[:, 1:] ^ bits[:, :-1]
    return gray


def gray_to_binary(gray: np.ndarray) -> np.ndarray:
    """Inverse Gray map: cumulative XOR along each row."""
    return np.bitwise_xor.accumulate(gray, axis=1)


values = np.array([10.0, 7.0, 4.0, 3.0])
weights = np.array([5.0, 4.0, 3.0, 1.0])
pop = repair_knapsack(init_binary_population(6, 4, 0.5, seed=1), values, weights, 8.0)
print((pop @ weights <= 8.0).all(), (gray_to_binary(binary_to_gray(pop)) == pop).all())
# Expected: True True — every repaired genotype is feasible, and the Gray
# round-trip recovers the original bits exactly.
```

Complexity: O(pop·n) for batch evaluation via matrix products; repair is O(n) per infeasible genotype. Memory: int8 keeps a 10,000 × 1,000 population at 10 MB.

### Integer vectors

Use for assignment and grouping: genotype index = item, value = chosen resource, group, or level. Every genotype is structurally feasible for "each item assigned exactly once," which makes this the default for machine assignment, graph coloring, and clustering. Fits GAs (uniform/k-point crossover, random-reset and creep mutation — see mutation-and-perturbation-operators), local search (single reassignment neighborhoods), and integer-valued EDAs.

```python
import numpy as np


def init_assignment_population(pop_size: int, n_jobs: int, n_machines: int,
                               seed: int) -> np.ndarray:
    """Uniform random machine index per job; every genotype is feasible for P||Cmax."""
    rng = np.random.default_rng(seed)
    return rng.integers(0, n_machines, size=(pop_size, n_jobs))


def machine_loads(assign: np.ndarray, proc: np.ndarray, n_machines: int) -> np.ndarray:
    """Batch machine loads, shape (pop_size, n_machines), via scatter-add."""
    pop_size = assign.shape[0]
    loads = np.zeros((pop_size, n_machines))
    np.add.at(loads, (np.arange(pop_size)[:, None], assign), proc)
    return loads


proc = np.array([4.0, 3.0, 3.0, 2.0, 2.0])
pop = init_assignment_population(8, 5, 2, seed=7)
makespans = machine_loads(pop, proc, 2).max(axis=1)
print(makespans.min())
# Expected: 7.0 — total work is 14 on 2 identical machines, so no genotype can
# beat 7.0, and the balanced split (4+3 | 3+2+2) appears in this small sample.
```

Complexity: O(pop·n) batch evaluation. Locality is high under single-gene mutation (one item moves). Watch for label symmetry in grouping problems: genotypes `[0,0,1,1]` and `[1,1,0,0]` are the same partition; this non-synonymous redundancy hurts crossover badly (see Practical Challenges).

### Real-valued vectors

Use for continuous parameters, and — via random keys — as a carrier for sequencing problems inside real-vector algorithms (DE, PSO, ES, BRKGA). Always state bounds and a bound-handling rule; reflection preserves locality near borders better than clipping, which piles probability mass on the bound.

```python
import numpy as np


def init_real_population(pop_size: int, dim: int, low: np.ndarray, high: np.ndarray,
                         seed: int) -> np.ndarray:
    """Uniform real genotypes inside the box [low, high]."""
    rng = np.random.default_rng(seed)
    return low + rng.random((pop_size, dim)) * (high - low)


def reflect_into_bounds(pop: np.ndarray, low: np.ndarray, high: np.ndarray) -> np.ndarray:
    """Reflect out-of-bounds coordinates back inside the box (triangle-wave fold)."""
    span = high - low
    t = np.mod(pop - low, 2.0 * span)
    return low + span - np.abs(t - span)


def keys_to_permutation(keys: np.ndarray) -> np.ndarray:
    """Random-key decode: rank order of the keys gives the permutation, row-wise."""
    return np.argsort(keys, axis=1, kind="stable")


low, high = np.zeros(3), np.ones(3)
pop = init_real_population(4, 3, low, high, seed=11)
shifted = reflect_into_bounds(pop + 0.8, low, high)
print(((shifted >= 0.0) & (shifted <= 1.0)).all(), keys_to_permutation(np.array([[0.7, 0.1, 0.4]])))
# Expected: True [[1 2 0]] — all reflected points are back in the box, and the
# key vector (0.7, 0.1, 0.4) sorts to the permutation (1, 2, 0).
```

Complexity: O(pop·n) for sampling and folding; O(pop·n log n) for argsort decoding. Random keys are synonymously redundant (a continuum of key vectors per permutation), which is benign; the full treatment of decoder design lives in decoder-based-representations.

### Permutations

Use for sequencing. Three distinct semantics decide which operators make sense:

- **Position** matters (QAP: facility i at position π(i)) → swap-based operators, cycle crossover.
- **Order/precedence** matters (flow shop, single machine: job priority order) → insertion moves, order crossover (OX).
- **Adjacency** matters (TSP: which edges the tour uses) → inversion/2-opt moves, edge recombination.

Mismatching semantics and operator is the most common permutation-encoding mistake; the full operator-by-property table is in crossover-operators.

```python
import numpy as np


def init_permutation_population(pop_size: int, n: int, seed: int) -> np.ndarray:
    """Independent uniform random permutations, shape (pop_size, n)."""
    rng = np.random.default_rng(seed)
    return rng.permuted(np.tile(np.arange(n), (pop_size, 1)), axis=1)


def is_valid_permutation(pop: np.ndarray) -> np.ndarray:
    """True per row iff the row is a permutation of 0..n-1; run after custom operators."""
    return (np.sort(pop, axis=1) == np.arange(pop.shape[1])).all(axis=1)


def tour_lengths(perms: np.ndarray, dist: np.ndarray) -> np.ndarray:
    """Batch closed-tour lengths under the adjacency interpretation (TSP)."""
    nxt = np.roll(perms, -1, axis=1)
    return dist[perms, nxt].sum(axis=1)


rng = np.random.default_rng(3)
pts = rng.random((6, 2))
dist = np.linalg.norm(pts[:, None, :] - pts[None, :, :], axis=2)
perms = init_permutation_population(10, 6, seed=3)
print(is_valid_permutation(perms).all(), round(float(tour_lengths(perms, dist).min()), 3))
# Expected: True 2.372 — every sampled row is a valid permutation and batch
# evaluation needs no Python loop over the population.
```

Complexity: O(pop·n) batch tour evaluation with fancy indexing. Structural feasibility ("each city once") is free; side constraints (time windows, precedence) are not and usually push toward a decoder.

### Binary matrices

Use when the decision is an assignment AND constraints act on both axes — rows (items) and columns (resources) — so operators benefit from seeing the matrix structure (timetabling slots × rooms, machine × job with per-machine cardinality caps). For plain assignment, prefer the integer vector: the matrix is its one-hot expansion and only adds redundancy and infeasibility.

```python
import numpy as np


def assignment_to_matrix(assign: np.ndarray, n_machines: int) -> np.ndarray:
    """One-hot expansion: (pop, n_jobs) integer genotypes -> (pop, n_jobs, n_machines)."""
    return (assign[..., None] == np.arange(n_machines)).astype(np.int8)


def repair_column_capacity(mat: np.ndarray, cap: int, seed: int) -> np.ndarray:
    """Move random jobs out of over-capacity machine columns into the least-loaded
    ones; requires cap * n_machines >= n_jobs (one job-by-machine 0/1 matrix)."""
    rng = np.random.default_rng(seed)
    mat = mat.copy()
    col_load = mat.sum(axis=0)
    while (col_load > cap).any():
        over = int(np.argmax(col_load))
        job = int(rng.choice(np.flatnonzero(mat[:, over])))
        under = int(np.argmin(col_load))
        mat[job, over] = 0
        mat[job, under] = 1
        col_load[over] -= 1
        col_load[under] += 1
    return mat


assign = np.array([[0, 0, 0, 0, 1, 2]])
mat = assignment_to_matrix(assign, 3)[0]          # 6 jobs x 3 machines
fixed = repair_column_capacity(mat, cap=2, seed=5)
print(fixed.sum(axis=0), (fixed.sum(axis=1) == 1).all())
# Expected: [2 2 2] True — machine 0 sheds two of its four jobs to the
# least-loaded machines and every job still has exactly one machine.
```

Complexity: one-hot expansion is O(pop·n·m) memory — the real cost of this encoding. Repair is O(moves). Fits GAs with row- or column-wise crossover and CP-style problems where you later migrate to an exact model.

### Set-based encodings

Use for sparse selection from a large universe (set covering with thousands of columns, crew schedules, pattern selection). The genotype is the member set itself — stored as a boolean mask when the universe fits in memory, or as sorted index arrays when it does not. Operators are add/drop/swap of members plus problem-aware construction; uniform crossover on masks works, but greedy union-then-prune recombination respects the problem better.

```python
import numpy as np


def greedy_cover(cover: np.ndarray, cost: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Randomized greedy set cover: boolean column mask covering all rows.
    Assumes every row is coverable by at least one column."""
    n_rows, n_cols = cover.shape
    chosen = np.zeros(n_cols, dtype=bool)
    uncovered = np.ones(n_rows, dtype=bool)
    while uncovered.any():
        gain = cover[uncovered].sum(axis=0)
        score = np.where(gain > 0, cost / np.maximum(gain, 1), np.inf)
        pick = int(rng.choice(np.flatnonzero(score <= score.min() * 1.2)))
        chosen[pick] = True
        uncovered &= ~cover[:, pick].astype(bool)
    return chosen


def drop_redundant(chosen: np.ndarray, cover: np.ndarray, cost: np.ndarray) -> np.ndarray:
    """Remove columns whose rows stay covered without them, most expensive first."""
    chosen = chosen.copy()
    for j in np.argsort(-cost):
        if chosen[j]:
            chosen[j] = False
            if (cover[:, chosen].sum(axis=1) == 0).any():
                chosen[j] = True
    return chosen


cover = np.array([[1, 0, 1, 0], [1, 1, 0, 0], [0, 1, 0, 1], [0, 0, 1, 1]], dtype=np.int8)
cost = np.array([3.0, 2.0, 2.0, 2.0])
rng = np.random.default_rng(2)
sol = drop_redundant(greedy_cover(cover, cost, rng), cover, cost)
print(sol, float(cost[sol].sum()))
# Expected: a feasible 2-column cover — this seed yields columns {0, 3}, cost 5.0,
# not the optimal {1, 2} at 4.0; randomized greedy gives diverse starts, not optima,
# and redundancy elimination never increases cost.
```

Complexity: greedy construction O(|S|·rows·cols) in the worst case; the prune pass O(cols·rows). Fits GRASP-style multistart, GAs with union/prune crossover, and any method where solution *size* varies — which fixed-length vectors handle awkwardly.

### Mixed genotypes

Use when one solution bundles different decision types: binary "open facility" flags plus an integer assignment vector, or a permutation plus real-valued timing offsets. Keep one array per segment (parallel arrays), apply segment-appropriate operators independently, and add a cheap consistency repair that runs before every evaluation — coupled segments drift apart under independent variation.

```python
import numpy as np


def repair_consistency(open_mask: np.ndarray, assign: np.ndarray,
                       dist: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Mixed-genotype repair for facility location: guarantee at least one open
    facility and reassign customers of closed facilities to their nearest open one."""
    open_mask = open_mask.copy()
    if not open_mask.any():
        open_mask[int(np.argmin(dist.sum(axis=0)))] = True
    open_idx = np.flatnonzero(open_mask)
    assign = assign.copy()
    bad = ~open_mask[assign]
    if bad.any():
        assign[bad] = open_idx[np.argmin(dist[bad][:, open_idx], axis=1)]
    return open_mask, assign


def uflp_cost(open_mask: np.ndarray, assign: np.ndarray,
              fixed_cost: np.ndarray, dist: np.ndarray) -> float:
    """Fixed opening costs plus assignment distances."""
    return float(fixed_cost[open_mask].sum() + dist[np.arange(assign.size), assign].sum())


fixed_cost = np.array([3.0, 3.0, 3.0])
dist = np.array([[1.0, 4.0, 5.0], [4.0, 1.0, 5.0], [5.0, 4.0, 1.0], [2.0, 3.0, 4.0]])
open_mask, assign = repair_consistency(np.array([True, False, False]),
                                       np.array([0, 1, 2, 0]), dist)
print(assign, uflp_cost(open_mask, assign, fixed_cost, dist))
# Expected: [0 0 0 0] 15.0 — customers 1 and 2 pointed at closed facilities and
# are reassigned to the only open one; cost = 3.0 fixed + 12.0 distance.
```

Complexity: repair is O(customers·open). An alternative to the mixed genotype is encoding only `open_mask` and deriving `assign` greedily inside the decoder — smaller search space, but it silently fixes the assignment rule; make that trade explicit.

## Worked Example: Parallel-Machine Assignment Under Three Encodings

The same problem, three representations, identical search budget. Problem: unrelated parallel machines, minimize makespan (R||Cmax). Data: `PROC[m, j]` = processing time of job j on machine m, 3 machines × 8 jobs. The search wrapper is a deliberately plain first-improvement climber (accept if not worse, 2,000 evaluations) so that *only the encoding differs*.

### Encoding A — direct integer vector

Genotype: `assign[j] ∈ {0, 1, 2}`. Structurally feasible always; mutation = reassign one job.

```python
import numpy as np

PROC = np.array([
    [4.0, 7.0, 3.0, 8.0, 5.0, 6.0, 2.0, 5.0],
    [6.0, 3.0, 6.0, 4.0, 7.0, 3.0, 5.0, 4.0],
    [5.0, 5.0, 4.0, 6.0, 3.0, 8.0, 4.0, 6.0],
])


def makespan(assign: np.ndarray, proc: np.ndarray) -> float:
    """Makespan of a machine-index genotype on unrelated machines."""
    loads = np.zeros(proc.shape[0])
    np.add.at(loads, assign, proc[assign, np.arange(assign.size)])
    return float(loads.max())


def hill_climb_integer(proc: np.ndarray, budget: int, seed: int) -> float:
    """First-improvement climb: reassign one random job to a random machine."""
    rng = np.random.default_rng(seed)
    n_machines, n_jobs = proc.shape
    cur = rng.integers(0, n_machines, n_jobs)
    cur_val = makespan(cur, proc)
    for _ in range(budget):
        cand = cur.copy()
        cand[int(rng.integers(n_jobs))] = int(rng.integers(n_machines))
        val = makespan(cand, proc)
        if val <= cur_val:
            cur, cur_val = cand, val
    return cur_val


print(hill_climb_integer(PROC, budget=2000, seed=0))
# Expected: 10.0 — close to the lower bound sum(min_m proc[m,j]) / 3 = 26/3 ≈ 8.7;
# every visited genotype is feasible, so the full budget goes into real moves.
```

### Encoding B — flattened binary matrix with repair

Genotype: 24 bits, the 3×8 matrix `X[m, j]`. The constraint "each job on exactly one machine" is NOT structural: a uniform random bit matrix satisfies it with probability $(3/2^3)^8 = (0.375)^8 \approx 3.9 \times 10^{-4}$. Repair must run on essentially every move, and a one-bit mutation that the repair then rewrites has poor effective locality.

```python
import numpy as np

PROC = np.array([
    [4.0, 7.0, 3.0, 8.0, 5.0, 6.0, 2.0, 5.0],
    [6.0, 3.0, 6.0, 4.0, 7.0, 3.0, 5.0, 4.0],
    [5.0, 5.0, 4.0, 6.0, 3.0, 8.0, 4.0, 6.0],
])


def repair_one_per_column(mat: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Force exactly one 1 per job column: fill empty columns, thin crowded ones."""
    mat = mat.copy()
    n_machines, n_jobs = mat.shape
    for j in range(n_jobs):
        ones = np.flatnonzero(mat[:, j])
        if ones.size != 1:
            keep = int(rng.integers(n_machines)) if ones.size == 0 else int(rng.choice(ones))
            mat[:, j] = 0
            mat[keep, j] = 1
    return mat


def hill_climb_matrix(proc: np.ndarray, budget: int, seed: int) -> float:
    """Bit-flip mutation on the flattened matrix, repair before every evaluation."""
    rng = np.random.default_rng(seed)
    n_machines, n_jobs = proc.shape
    cur = repair_one_per_column((rng.random((n_machines, n_jobs)) < 0.5).astype(np.int8), rng)
    cur_val = float((cur * proc).sum(axis=1).max())
    for _ in range(budget):
        cand = cur.copy()
        cand[np.unravel_index(int(rng.integers(cand.size)), cand.shape)] ^= 1
        cand = repair_one_per_column(cand, rng)
        val = float((cand * proc).sum(axis=1).max())
        if val <= cur_val:
            cur, cur_val = cand, val
    return cur_val


raw = np.random.default_rng(0).random((20000, 3, 8)) < 0.5
feasible_ratio = float((raw.sum(axis=1) == 1).all(axis=1).mean())
print(round(feasible_ratio, 5), hill_climb_matrix(PROC, budget=2000, seed=0))
# Expected: 0.00025 11.0 — the raw feasibility ratio is near the theoretical
# 0.375**8 ≈ 0.00039, and the climb stalls at makespan 11.0 where encoding A
# reached 10.0 with the same budget: repair rewrites moves, so effective
# locality is lower and the last improvement step is never found.
```

### Encoding C — random keys with a list-scheduling decoder

Genotype: 8 keys in [0,1]. Decoder: sort jobs by key, assign each to the machine that finishes it earliest. Feasibility is guaranteed and the decoder injects a load-balancing bias — uniform random keys already produce good schedules. The price: coverage is restricted to "earliest-finish" schedules, and the decoder costs O(n·m) per evaluation.

```python
import numpy as np

PROC = np.array([
    [4.0, 7.0, 3.0, 8.0, 5.0, 6.0, 2.0, 5.0],
    [6.0, 3.0, 6.0, 4.0, 7.0, 3.0, 5.0, 4.0],
    [5.0, 5.0, 4.0, 6.0, 3.0, 8.0, 4.0, 6.0],
])


def decode_keys(keys: np.ndarray, proc: np.ndarray) -> tuple[np.ndarray, float]:
    """List-scheduling decoder: jobs in key order, each to its earliest-finish machine."""
    n_machines, n_jobs = proc.shape
    loads = np.zeros(n_machines)
    assign = np.empty(n_jobs, dtype=np.int64)
    for j in np.argsort(keys, kind="stable"):
        finish = loads + proc[:, j]
        m = int(np.argmin(finish))
        assign[j] = m
        loads[m] = finish[m]
    return assign, float(loads.max())


def hill_climb_keys(proc: np.ndarray, budget: int, seed: int) -> float:
    """Perturb one key with Gaussian noise; the decoder guarantees feasibility."""
    rng = np.random.default_rng(seed)
    n_jobs = proc.shape[1]
    cur = rng.random(n_jobs)
    _, cur_val = decode_keys(cur, proc)
    for _ in range(budget):
        cand = cur.copy()
        j = int(rng.integers(n_jobs))
        cand[j] = float(np.clip(cand[j] + rng.normal(0.0, 0.2), 0.0, 1.0))
        _, val = decode_keys(cand, proc)
        if val <= cur_val:
            cur, cur_val = cand, val
    return cur_val


print(round(decode_keys(np.random.default_rng(0).random(8), PROC)[1], 1),
      hill_climb_keys(PROC, budget=2000, seed=0))
# Expected: a single random key vector already decodes to makespan ≈ 11 (the
# decoder's balancing bias), and the climb reaches 10.0 like the other encodings.
```

### Trade-off analysis

| Criterion | A: integer vector | B: binary matrix + repair | C: random keys + decoder |
|---|---|---|---|
| Genotype space | $3^8 = 6{,}561$ | $2^{24} \approx 1.7\times10^7$ | continuous |
| Feasibility coverage | 100% structural | ~0.04% raw, 100% after repair | 100% by construction |
| Phenotype coverage | complete | complete (after repair) | only earliest-finish schedules |
| Locality of one mutation | high (one job moves) | low (repair may rewrite the move) | medium (one key shift can reorder several jobs) |
| Sampling bias | none | none (repair is uniform-ish) | strong, toward balanced loads |
| Decode cost / evaluation | O(n) | O(n·m) incl. repair | O(n log n + n·m) |
| Natural operators | uniform/k-point crossover, reset mutation | bit operators (then repaired) | any real-vector operator: DE, PSO, ES, BRKGA |
| Verdict | default choice | avoid unless both axes carry constraints | choose when the algorithm is real-vector, or when the bias is wanted |

Even on this 8-job toy the encodings separate: A and C reach makespan 10.0, while B stalls at 11.0 with the identical budget because repair keeps rewriting its moves. The gaps widen with size: at n = 500 jobs, encoding B spends most of its time in repair, and encoding C's decoder bias usually beats encoding A's unbiased start under a tight evaluation budget — measure both before committing (protocol in metaheuristic-design-principles).

## Encoding–Operator Compatibility

The full operator catalogs live in crossover-operators and mutation-and-perturbation-operators; these tables answer the selection question only.

### Crossover families × encodings

| Crossover | Binary | Integer | Real | Permutation | Matrix | Set |
|---|---|---|---|---|---|---|
| One-/two-point | yes | yes | workable | invalid (duplicates) | per-row variant | on membership mask |
| Uniform | yes | yes | workable | invalid | per-column variant | on membership mask |
| Arithmetic / blend / SBX | no | no | yes | via random keys only | no | no |
| OX / PMX / CX (position & order) | no | no | no | yes | no | no |
| ERX / AEX (adjacency) | no | no | no | yes (TSP-like) | no | no |
| Union + greedy prune | no | no | no | no | no | yes |

### Mutation families × encodings

| Mutation | Binary | Integer | Real | Permutation | Matrix | Set |
|---|---|---|---|---|---|---|
| Bit-flip | yes | no | no | no | yes (then repair) | flip membership |
| Random reset / creep | no | yes | no | no | move a 1 within a column | no |
| Gaussian / polynomial | no | no | yes | via random keys | no | no |
| Swap / insertion / inversion / scramble | no | swap groups | no | yes | row swap | swap members |
| Add / drop element | no | no | no | no | no | yes |

### Algorithm families × encodings

| Algorithm family | Natural encodings | Notes |
|---|---|---|
| Genetic algorithms | binary, integer, permutation, set, mixed | most flexible host; pick operators per the tables above |
| Evolution strategies, DE, PSO | real | combinatorial problems enter via random keys or rounding |
| BRKGA | random keys only | the decoder is the entire problem-specific part |
| EDAs (UMDA, PBIL) | binary, integer | permutations need specialized models (edge histograms, Mallows) |
| Local search, SA, tabu | any with a neighborhood | encoding = move definition; delta evaluation drives the choice |
| ACO | constructive (implicit) | the construction graph replaces the genotype |

## Advanced Techniques

### Measuring locality before trusting an encoding

Do not argue about locality — measure it. Sample random genotypes, apply one minimal mutation, and record the fitness jump. Compare encodings (or mutation operators) under identical sampling. Low mean jump with nonzero variance indicates a landscape that local search can exploit; jumps as large as random resampling indicate a needle-in-a-haystack encoding.

```python
import numpy as np
from collections.abc import Callable


def fitness_locality(init: Callable[[np.random.Generator], np.ndarray],
                     mutate: Callable[[np.ndarray, np.random.Generator], np.ndarray],
                     fitness: Callable[[np.ndarray], float],
                     n_starts: int, n_steps: int, seed: int) -> float:
    """Mean |f(mutant) - f(x)| over one-step mutations; smaller = higher locality."""
    rng = np.random.default_rng(seed)
    jumps = []
    for _ in range(n_starts):
        x = init(rng)
        fx = fitness(x)
        jumps.extend(abs(fitness(mutate(x, rng)) - fx) for _ in range(n_steps))
    return float(np.mean(jumps))


pts = np.random.default_rng(5).random((12, 2))
DIST = np.linalg.norm(pts[:, None] - pts[None, :], axis=2)


def tour_len(p: np.ndarray) -> float:
    """Closed tour length on the module-level distance matrix."""
    return float(DIST[p, np.roll(p, -1)].sum())


def init_perm(rng: np.random.Generator) -> np.ndarray:
    """Uniform random permutation of 12 cities."""
    return rng.permutation(12)


def reverse_segment(p: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Reverse a random contiguous segment (a 2-opt move: changes 2 tour edges)."""
    q = p.copy()
    i, j = np.sort(rng.choice(p.size, 2, replace=False))
    q[i:j + 1] = q[i:j + 1][::-1]
    return q


def swap_two(p: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Exchange two random positions (changes up to 4 tour edges)."""
    q = p.copy()
    i, j = rng.choice(p.size, 2, replace=False)
    q[i], q[j] = q[j], q[i]
    return q


def scramble_segment(p: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Shuffle a random contiguous segment (changes many tour edges)."""
    q = p.copy()
    i, j = np.sort(rng.choice(p.size, 2, replace=False))
    q[i:j + 1] = rng.permutation(q[i:j + 1])
    return q


locs = [round(fitness_locality(init_perm, op, tour_len, 50, 40, seed=1), 3)
        for op in (reverse_segment, swap_two, scramble_segment)]
print(locs, locs[0] < locs[1] < locs[2])
# Expected: [0.332, 0.453, 0.506] True — mean fitness jump grows with the number
# of edges an operator touches; under the adjacency semantics of TSP, segment
# reversal is the highest-locality move, which is exactly why 2-opt works.
```

### Quantifying redundancy and decoder bias

For an indirect encoding, sample genotypes uniformly, decode, and inspect the phenotype distribution: how many distinct phenotypes appear, and how concentrated is the mass? Heavy concentration means the decoder is doing most of the optimizing — good if its bias matches the problem, harmful if the optimum lies outside its image.

```python
import numpy as np
from collections import Counter


def decoder_bias(n_samples: int, seed: int) -> tuple[int, float]:
    """Sample uniform keys, decode by list scheduling on a 2x4 identical-machine
    instance; return (distinct phenotypes, share of the most frequent one)."""
    proc = np.array([[4.0, 3.0, 2.0, 2.0], [4.0, 3.0, 2.0, 2.0]])
    rng = np.random.default_rng(seed)
    counts: Counter = Counter()
    for _ in range(n_samples):
        loads = np.zeros(2)
        assign = np.empty(4, dtype=int)
        for j in np.argsort(rng.random(4)):
            m = int(np.argmin(loads + proc[:, j]))
            assign[j] = m
            loads[m] += proc[m, j]
        counts[tuple(assign)] += 1
    return len(counts), counts.most_common(1)[0][1] / n_samples


n_distinct, top_share = decoder_bias(5000, seed=4)
print(n_distinct, round(top_share, 2))
# Expected: 7 0.17 — only 7 of the 2**4 = 16 direct assignments are reachable,
# and the most frequent one draws 17% of the mass (2.7x the uniform 1/16 share):
# the decoder concentrates sampling on balanced schedules and cannot express
# unbalanced ones, a deliberate coverage-for-bias trade.
```

### Choosing the feasibility strategy per constraint

For each hard constraint pick exactly one mechanism and write it down: (1) **structural** — the encoding cannot express violations (permutation for "each once"); (2) **decoder** — the genotype is unconstrained, the decoder builds only feasible phenotypes; (3) **repair** — violations are fixed after variation, ideally writing the repaired genotype back (Lamarckian) so the population learns; (4) **penalty** — violations survive but cost fitness. Order of preference is usually 1 > 2 > 3 > 4 for tight constraints and 4 for soft or rarely-violated ones. Mixing mechanisms on the *same* constraint creates bugs; mixing across constraints is normal.

### Hamming cliffs and Gray-coded integers

When a bounded integer or discretized real parameter must live on a binary genotype (e.g., for a binary EDA), use the reflected Gray code from the catalog: every adjacent value pair differs in one bit, so bit-flip mutation can always reach the neighboring value. Standard binary coding blocks the 2^k boundaries behind multi-bit flips. If the algorithm permits integer genes directly, skip the bits entirely — creep mutation on integers has strictly better locality than any bit coding.

### Structured genotypes without object overhead

For mixed encodings keep one numpy array per segment and pass them together (a small dataclass of arrays, or a dict of arrays for a whole population). Avoid arrays of Python objects and numpy structured dtypes inside hot loops — they defeat vectorization. Population-level layout: `dict[str, np.ndarray]` with shapes `(pop, n_seg)` per segment lets each operator stay vectorized over the population axis.

## Practical Challenges

**Crossover produces invalid permutations.** One-point or uniform crossover on permutations duplicates and drops elements. Either switch to permutation-aware operators (OX, PMX, CX — see crossover-operators) or move to random keys where any real-vector crossover is safe. Add `is_valid_permutation` as an assertion after every operator during development; remove it for production runs.

**Repair erases what variation built.** If repair is deterministic and aggressive (always drop the worst-ratio item), offspring lose exactly the novel genes crossover introduced, and the population collapses to the repair operator's fixed points. Randomize the repair order, repair minimally (stop at first feasibility), and write the repaired genotype back so selection sees what evaluation saw.

**Grouping symmetry destroys crossover.** In clustering/coloring with integer encodings, group labels are arbitrary: two parents can encode the same partition with permuted labels, and uniform crossover of them yields garbage. Renumber labels canonically (first occurrence order) before crossover, or use grouping-aware operators that exchange whole groups (Falkenauer, 1998, *Genetic Algorithms and Grouping Problems*).

**The optimum is not representable.** Decoder-based encodings restrict the phenotype image — list scheduling only produces non-delay schedules, and some instances have only delayed optima. Spot-check coverage: take the best known solution from another method and verify some genotype decodes to it (or within tolerance). If not, either accept the gap consciously or widen the decoder.

**Genotype diversity looks fine but the search stalls.** With redundant encodings, distinct genotypes can be the same phenotype; entropy on genotypes overstates real diversity. Measure diversity in phenotype space (or fitness space) instead, e.g., count distinct decoded solutions per generation. Redundancy-heavy encodings like random keys need this routinely.

**One mutation changes everything.** A small genotype change that reshuffles the whole phenotype (low locality) shows up as local search behaving like random restart. Run the `fitness_locality` measurement; if the mean jump under minimal mutation is close to the jump under full resampling, change the encoding or the operator before tuning anything else.

**Mixed-genotype segments evolve at different speeds.** A binary open-facility segment converges in 50 generations while the assignment segment needs 500; the frozen segment then traps the rest. Give each segment its own mutation rate, tune them separately, and consider alternating phases (optimize segment B with A frozen, then swap) — effectively coordinate descent across segments.

**Bit-string integers stall at power-of-two boundaries.** Fitness plateaus where improving the solution requires crossing 0111→1000 are Hamming cliffs from binary positional coding. Switch to Gray code or to direct integer genes; verify by checking whether stalled populations sit just below such boundaries.

## Tools & Libraries

| Library | When to use | Note |
|---|---|---|
| numpy | always: population arrays, batch decoding, vectorized evaluation | `default_rng(seed)`, int8 for binary populations, fancy indexing for batch tours |
| DEAP | custom GA with a nonstandard encoding | you define the genotype as any Python structure; operators are plain functions |
| pymoo | NSGA-II/III and friends with permutation or binary problems | ships permutation sampling/crossover/mutation; clean operator plug-in API |
| scipy | repairs needing optimal matching (`optimize.linear_sum_assignment`) | turns "reassign violators" into an optimal O(n³) repair |
| networkx | adjacency-based phenotype checks (tours, connectivity) | validation only; keep it out of the evaluation hot loop |
| pandas | encoding-comparison experiment tables | one row per (encoding, seed, budget) run; pivot for the trade-off table |

## Output Format

A complete representation-design answer contains:

1. **Decision table** — candidate encodings scored against the five criteria for *this* problem, with the chosen one and a one-sentence justification.
2. **Genotype specification** — dtype, shape, bounds/value sets, and the structural invariants (e.g., "row is a permutation of 0..n-1"), stated precisely enough to write a validator from.
3. **Feasibility map** — every hard constraint with its mechanism: structural / decoder / repair / penalty.
4. **Operator shortlist** — 1-2 crossover and 1-2 mutation operators compatible with the encoding (from the tables above), with references to crossover-operators and mutation-and-perturbation-operators for implementations.
5. **Decoder contract** (if indirect) — input, output, per-call complexity, and an explicit statement of the bias and any coverage restriction.
6. **Validation hooks** — the invariant checker, a coverage spot-check against a known good solution, and a locality measurement plan.
7. **Code artifacts** — initializer, (decoder,) evaluator, and validator as runnable functions with seeds.

Template for the decision summary:

```text
REPRESENTATION DECISION — <problem name>
Decision structure : assignment of 500 jobs to 12 unrelated machines
Chosen encoding    : integer vector, shape (500,), values 0..11
Rejected           : binary matrix (feasibility 1e-150 raw, repair-dominated);
                     random keys + list scheduling (coverage excludes delayed
                     schedules; revisit if DE/PSO becomes the algorithm)
Constraints        : one machine per job -> structural
                     machine eligibility -> decoder masks ineligible machines
                     max 60 jobs/machine -> repair (move from over-cap columns)
Operators          : uniform crossover; random-reset mutation (rate 1/n)
Validation         : eligibility checker after every operator (dev builds);
                     coverage check vs. LPT solution; locality vs. swap baseline
```

## Questions to Ask

- What does one complete solution decide — a subset, an assignment, an ordering, a grouping, parameters, or several of these?
- Which constraints are hard, and which of them could the representation enforce by construction?
- How large is one solution (items, machines, positions), and how large might instances get?
- Is the algorithm already fixed (DE/PSO need real vectors; BRKGA needs keys), or is it open?
- How expensive is one fitness evaluation, and what total evaluation budget is realistic?
- Is there a known construction heuristic whose logic could become a decoder?
- Do you have a best-known solution we can use to test that the encoding can represent it?
- What fraction of uniformly random genotypes do you expect to be feasible?
- Are good solutions known to have structure (balanced, sparse, clustered) worth biasing toward?
- Which operator implementations already exist in your codebase or chosen library?

## Related Skills

- **decoder-based-representations** — when the genotype should stay simple and a decoder (random keys, priority rules, schedule-generation schemes) should construct the feasible phenotype.
- **crossover-operators** — when choosing or implementing recombination for a specific encoding; full catalog with position/order/adjacency preservation properties.
- **mutation-and-perturbation-operators** — when choosing mutation or perturbation moves per encoding, and controlling mutation strength.
- **metaheuristic-design-principles** — when the encoding decision must be made jointly with algorithm choice, constraint handling, and the evaluation budget.
- **genetic-algorithms** — when wiring an encoding and its operators into a full population-based loop with selection and elitism.
