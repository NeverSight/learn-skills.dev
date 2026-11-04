---
name: numpy-vectorization-for-optimization
description: When the user wants to remove slow Python loops from metaheuristic or optimization code using NumPy — population-level operations, batch fitness evaluation, distance matrices, broadcasting, argsort/argpartition idioms, default_rng, and memory layout. Also use when the user mentions "vectorize," "numpy broadcasting," "population fitness," "distance matrix," "speed up metaheuristic," or "slow Python loop." For computing less instead of faster (delta evaluation, caching), see fitness-evaluation-and-caching; for multiprocessing and island models, see parallel-and-hybrid-metaheuristics.
---

# NumPy Vectorization for Optimization

You are an expert in high-performance scientific Python for combinatorial optimization. This skill
covers turning loop-based metaheuristic code into vectorized NumPy: population-level operations,
batch fitness evaluation, distance matrices, broadcasting, `argsort`/`argpartition` idioms, the
`default_rng` Generator API, and memory layout — plus the profiling discipline that decides which
loops are worth removing. Use the pattern catalog below to deliver 10-1000x constant-factor
speedups without changing what the algorithm computes.

## Initial Assessment

Establish these facts before rewriting any loop:

- **Profile evidence.** Ask for (or produce) a `cProfile` or timing breakdown. Never vectorize a
  loop that consumes 3% of runtime; Amdahl's law caps the whole-run gain at 1.03x.
- **Algorithm class.** Population methods (GA, DE, PSO, EDA) vectorize naturally: one array axis
  is the population. Trajectory methods (SA, tabu, ILS) have sequentially dependent iterations;
  only their inner evaluations and neighborhood scans vectorize.
- **Loop inventory.** Classify every hot loop: over individuals, over genes within an individual,
  over parent pairs, over neighborhood moves, over generations, over restarts. Each class has a
  different replacement pattern (see the decision table below).
- **Array sizes.** NumPy pays a fixed ~1 µs dispatch cost per call. Arrays under a few hundred
  elements rarely amortize it; a `(pop_size, n)` batch almost always does.
- **Objective structure.** Can the objective be written as gathers (fancy indexing), elementwise
  ops, reductions, and matrix products? Sums of local terms vectorize; recursions with
  data-dependent state (e.g., makespan propagation) resist and may need a JIT instead.
- **Branchiness.** Data-dependent `if`/`else` per element converts to masks and `np.where`; deep
  nested control flow may produce unreadable mask algebra — consider Numba for those kernels.
- **Memory headroom.** Broadcasting materializes temporaries: `(n, n, d)` for pairwise
  differences, `(p, n, n)` for batched matrix gathers. Check RAM before promising speed.
- **dtype and value ranges.** Integer products overflow silently in NumPy fixed-width ints;
  float32 halves bandwidth but costs precision. Decide dtypes up front.
- **Reproducibility contract.** Vectorizing changes the RNG draw order, so results differ from
  the loop version even with the same seed. Agree on equivalence: bit-identical (rarely
  possible), numerically identical given the same inputs, or statistically equivalent.
- **Dependency policy.** NumPy only, or are SciPy (`cdist`), Numba, and threadpoolctl allowed?
- **Hardware and BLAS.** Core count and BLAS backend (OpenBLAS/MKL) matter for `@`-heavy code,
  and BLAS threading interacts badly with `multiprocessing` workers.
- **Target throughput.** Evaluations/second needed for the experiment budget. Stop optimizing
  when the budget fits; refactoring time is also research time.

## The Vectorization Cost Model

A pure-Python loop pays interpreter dispatch on every element; a NumPy expression pays a fixed
per-call cost and then streams memory at C speed (Harris et al. 2020, "Array programming with
NumPy"). For an n-element operation expressed as k chained array calls:

$$
T_{\text{loop}}(n) \;\approx\; n \, c_{\text{py}},
\qquad
T_{\text{vec}}(n) \;\approx\; k \, c_{\text{call}} + n \, k\, c_{\text{elem}},
$$

with typical magnitudes $c_{\text{py}} \approx 50\text{–}200$ ns per element of interpreter work,
$c_{\text{call}} \approx 0.5\text{–}5$ µs per NumPy call, and $c_{\text{elem}} \approx 1\text{–}4$
ns per element. Consequences:

- **Break-even size.** Vectorization wins once $n \gtrsim k\,c_{\text{call}} / c_{\text{py}}$ — a
  few hundred elements. Batch the *population*, not one individual at a time.
- **Death by small calls.** Ten chained ufuncs on a `(50,)` array inside a Python loop over the
  population is still loop-bound. Lift the population axis into the arrays: `(p, n)`.
- **Constant factor only.** Vectorization never changes the exponent. An $O(n^2)$ full
  re-evaluation stays $O(n^2)$; delta evaluation makes it $O(n)$ or $O(1)$
  (see **fitness-evaluation-and-caching**). Reduce work first, then vectorize what remains.
- **Amdahl bound.** If evaluation is fraction $f$ of runtime, the whole-run speedup is at most
  $1/(1-f)$ no matter how fast the kernel gets (Amdahl 1967).

### Decision table: loop type → replacement

| Loop found in the profile | Verdict | Replacement |
|---|---|---|
| Over individuals to compute fitness | vectorize | batch fitness (Patterns 4-6) |
| Over genes inside one individual | vectorize | row-wise array algebra |
| Over parent pairs in crossover/mutation | vectorize | mask-based batch operators (Pattern 3) |
| Over a neighborhood (best improvement) | delta first, then vectorize | whole-neighborhood delta matrix (Advanced) |
| Trajectory main loop (SA/tabu iterations) | do not vectorize | sequentially dependent — JIT the kernel (Advanced) |
| Over independent restarts or instances | parallelize | **parallel-and-hybrid-metaheuristics** |
| Over file/solver I/O | neither | overlap I/O or batch it; vectorization is irrelevant |

### Broadcasting rules and the shape vocabulary

Broadcasting aligns shapes from the *right*; two dimensions are compatible when they are equal or
one of them is 1; missing leading dimensions are treated as 1. The standard shapes in vectorized
metaheuristics:

| Array | Shape | Role |
|---|---|---|
| Population | `(p, n)` | one row per individual, C-contiguous |
| Data vector (values, weights, due dates) | `(n,)` | broadcasts across all rows |
| Per-individual scalar (fitness, load) | `(p,)` or `(p, 1)` | use `keepdims=True` for further row math |
| Cost/flow/distance matrix | `(n, n)` | read via fancy-indexing gathers |
| Pairwise point differences | `(n, 1, d) - (1, n, d) → (n, n, d)` | distance matrices (Pattern 7) |
| Batched permuted matrix | `(p, n, n)` | QAP-style objectives (Pattern 6) |

The single most common silent bug is mixing `(p,)` with `(p, 1)`: adding them broadcasts to
`(p, p)` instead of raising an error. Annotate shapes in comments and `assert` them at function
boundaries during development.

### Order of attack

1. **Profile** (Pattern 10) — find where time goes; confirm the loop is hot.
2. **Reduce work** — delta evaluation, caching, better neighborhoods (other skills).
3. **Vectorize** the remaining work with the patterns below.
4. **JIT** the kernels that are inherently sequential (Advanced).
5. **Parallelize** across cores only after single-core throughput is respectable.
6. **Re-profile and re-validate** — every step ends with `np.allclose` against the naive code.

## Pattern Catalog I — Random Numbers and Population Operations

### Pattern 1: One seeded Generator, batch sampling

All randomness flows through a single `np.random.Generator` created by `default_rng(seed)` and
passed explicitly to every function. Batch sampling replaces per-individual draws: one call
creates the whole binary population, and `rng.permuted(..., axis=1)` runs an independent
Fisher–Yates shuffle per row in O(p·n).

```python
import numpy as np


def init_populations(seed: int, pop_size: int, n: int) -> tuple[np.ndarray, np.ndarray]:
    """Create a binary population and a permutation population from one seeded Generator."""
    rng = np.random.default_rng(seed)
    binary_pop = rng.integers(0, 2, size=(pop_size, n), dtype=np.int8)
    perm_pop = rng.permuted(np.tile(np.arange(n), (pop_size, 1)), axis=1)
    return binary_pop, perm_pop


binary_pop, perm_pop = init_populations(seed=42, pop_size=4, n=6)
print(binary_pop.shape, perm_pop.shape)
print(np.sort(perm_pop, axis=1))
# Expected: (4, 6) (4, 6); every sorted row of perm_pop equals [0 1 2 3 4 5],
# i.e. each row is a valid independent permutation.
```

The argsort alternative `rng.random((p, n)).argsort(axis=1)` also yields uniform random
permutations (O(p·n log n)) and doubles as a random-key decoder. For parallel workers, derive
independent streams with `rng.spawn(k)` or `np.random.SeedSequence(seed).spawn(k)` — never reuse
the same seed across processes.

**Pitfall:** `rng.permutation(x, axis=1)` and `rng.permuted(x, axis=1)` are different functions.
`permutation` applies *one* shared column permutation to the whole matrix; `permuted` shuffles
*within* each row independently. Using the former silently makes all individuals identical up to
row content. Also avoid the legacy global API (`np.random.seed`, `np.random.rand`): it is shared
mutable global state, and any library call that touches it destroys your reproducibility.

### Pattern 2: Vectorized tournament selection

Selection loops over offspring are pure indexing arithmetic. Draw the whole `(n_parents, k)`
entrant matrix in one call, gather fitness with fancy indexing, and take a row-wise `argmax`.

```python
import numpy as np


def tournament_select(fitness: np.ndarray, n_parents: int, k: int,
                      rng: np.random.Generator) -> np.ndarray:
    """Indices of n_parents winners of independent k-tournaments (maximization)."""
    entrants = rng.integers(fitness.shape[0], size=(n_parents, k))
    winner_col = fitness[entrants].argmax(axis=1)
    return entrants[np.arange(n_parents), winner_col]


rng = np.random.default_rng(0)
fitness = np.array([1.0, 9.0, 3.0, 7.0, 5.0])
parents = tournament_select(fitness, n_parents=100_000, k=3, rng=rng)
print(np.round(np.bincount(parents, minlength=5) / 100_000.0, 2))
# Expected: close to the theoretical win probabilities ((r+1)^3 - r^3)/125
# for fitness ranks r = 0..4, i.e. [0.008 0.488 0.056 0.296 0.152].
```

The same gather-then-reduce shape works for rank and Boltzmann selection: compute a `(p,)`
probability vector once, then `rng.choice(p, size=n_parents, p=probs)`.

**Pitfall:** `fitness[entrants]` is advanced indexing and returns a *copy* of shape
`(n_parents, k)` — fine here, but the same idiom inside a per-individual Python loop re-pays the
dispatch cost n_parents times. Also note `argmax` breaks ties by first occurrence, which couples
tie outcomes to entrant draw order; this is acceptable but document it for reproducibility.

### Pattern 3: Batch crossover and mutation

For binary and real-valued encodings, crossover and mutation are mask algebra over the whole
mating pool: no loop over pairs, no loop over genes.

```python
import numpy as np


def uniform_crossover(parents_a: np.ndarray, parents_b: np.ndarray,
                      rng: np.random.Generator) -> np.ndarray:
    """Uniform crossover on a batch of parent pairs; one child per pair."""
    mask = rng.random(parents_a.shape) < 0.5
    return np.where(mask, parents_a, parents_b)


def bitflip_mutation(pop: np.ndarray, rate: float, rng: np.random.Generator) -> np.ndarray:
    """Flip each bit independently with probability rate; returns a new array."""
    flips = rng.random(pop.shape) < rate
    return pop ^ flips.astype(pop.dtype)


rng = np.random.default_rng(7)
a = np.zeros((3, 8), dtype=np.int8)
b = np.ones((3, 8), dtype=np.int8)
children = uniform_crossover(a, b, rng)
mutated = bitflip_mutation(children, rate=1.0 / 8, rng=rng)
print(round(float(children.mean()), 2), mutated.shape)
# Expected: children.mean() near 0.5 (each gene equally likely from either
# parent) and shape (3, 8); on average one bit per row is then flipped.
```

One-point crossover vectorizes the same way: draw cut points `c = rng.integers(1, n, size=p)`
and build the mask as `np.arange(n) < c[:, None]` — a textbook broadcast.

**Pitfall:** these masks are only valid for encodings where genes are independent. Applying them
to permutation rows produces invalid tours (duplicate cities). Permutation operators (OX, PMX,
swap/inversion mutation) need index bookkeeping that vectorizes across the population but not
within one individual; implement them row-wise inside a thin loop or via Numba, and see
**genetic-algorithms** for full operator loops built on this pattern.

## Pattern Catalog II — Batch Fitness Evaluation

### Pattern 4: Linear objectives as matrix products (knapsack)

Any objective of the form "sum of per-gene contributions" over a 0-1 population is a single
matrix-vector product, and a linear constraint check is another one. BLAS executes both.

```python
import numpy as np


def knapsack_batch_fitness(pop: np.ndarray, values: np.ndarray, weights: np.ndarray,
                           capacity: float, penalty: float) -> np.ndarray:
    """Penalized 0-1 knapsack fitness for a whole (pop_size, n) population at once."""
    total_value = pop @ values
    overload = np.maximum(pop @ weights - capacity, 0.0)
    return total_value - penalty * overload


values = np.array([10.0, 7.0, 4.0, 3.0])
weights = np.array([5.0, 4.0, 3.0, 1.0])
pop = np.array([[1, 1, 0, 0],
                [1, 1, 1, 1],
                [0, 0, 0, 1]], dtype=np.float64)
fit = knapsack_batch_fitness(pop, values, weights, capacity=9.0, penalty=100.0)
print(fit)
# Expected: [17. -376. 3.] — row 0 feasible (weight 9, value 17), row 1
# overloaded by 4 units (24 - 100*4), row 2 feasible with value 3.
```

The same shape covers set covering (`cover_counts = pop @ incidence`), multidimensional knapsack
(`loads = pop @ W.T` with `W` of shape `(m, n)`), and any weighted-sum objective.

**Pitfall:** keep the population in a float dtype (or cast once per generation) before `@`.
Integer and `int8` matmuls do not dispatch to BLAS and can be an order of magnitude slower;
`bool` arrays promote in surprising ways. One explicit `pop.astype(np.float64)` per generation
costs far less than a slow integer matmul.

### Pattern 5: Permutation objectives by fancy-indexed gathers (TSP)

Tour lengths for an entire population are one gather into the distance matrix plus a row
reduction. `dist[tours, nxt]` reads, for every individual and every position, the cost of the
edge leaving that position.

```python
import numpy as np


def batch_tour_lengths(dist: np.ndarray, tours: np.ndarray) -> np.ndarray:
    """Length of every closed tour in a (pop_size, n) integer array of permutations."""
    nxt = np.roll(tours, -1, axis=1)
    return dist[tours, nxt].sum(axis=1)


coords = np.array([[0.0, 0.0], [0.0, 1.0], [1.0, 1.0], [1.0, 0.0]])
diff = coords[:, None, :] - coords[None, :, :]
dist = np.sqrt((diff ** 2).sum(axis=2))
tours = np.array([[0, 1, 2, 3],
                  [0, 2, 1, 3]])
print(np.round(batch_tour_lengths(dist, tours), 3))
# Expected: [4.    4.828] — the unit square visited in order has length 4;
# the crossing tour pays two diagonals (2 + 2*sqrt(2)).
```

The gather idiom generalizes: machine assignment costs `C[machines, jobs]`, position-dependent
costs `C[np.arange(n), perm]`, sequence-dependent setups `S[perm[:, :-1], perm[:, 1:]]`.

**Pitfall:** this computes *full* evaluations. Inside a 2-opt or insertion local search, a single
move changes two edges, and delta evaluation costs O(1) versus O(n) here — vectorized full
re-evaluation inside a trajectory search is the classic case of making the wrong thing fast
(see **fitness-evaluation-and-caching**). Also ensure `tours` has an integer dtype; float
permutations raise `IndexError` only after a confusing cast attempt.

### Pattern 6: Quadratic objectives with einsum (QAP)

Objectives with two interacting indices — QAP's flow×distance, quadratic knapsack's `x^T Q x` —
fit `np.einsum`, which contracts indices without materializing intermediate products you do not
need. For a batch of permutations, gather the permuted distance matrix per individual, then
contract against the flow matrix.

```python
import numpy as np


def qap_batch_objective(A: np.ndarray, B: np.ndarray, perms: np.ndarray) -> np.ndarray:
    """QAP objective sum_ij A[i,j] * B[perm[i], perm[j]] for each row of perms."""
    B_perm = B[perms[:, :, None], perms[:, None, :]]  # shape (p, n, n) gather
    return np.einsum("ij,pij->p", A, B_perm)


A = np.array([[0, 3, 1],
              [3, 0, 2],
              [1, 2, 0]], dtype=np.float64)
B = np.array([[0, 1, 4],
              [1, 0, 2],
              [4, 2, 0]], dtype=np.float64)
perms = np.array([[0, 1, 2],
                  [2, 1, 0]])
print(qap_batch_objective(A, B, perms))
# Expected: [22. 24.] — identity assignment costs 2*(3*1 + 1*4 + 2*2) = 22;
# the reversed assignment costs 2*(3*2 + 1*4 + 2*1) = 24.
```

For binary quadratic objectives the batched form is one line:
`np.einsum("pi,ij,pj->p", pop, Q, pop)` with `optimize=True` to let einsum pick a contraction
order that goes through BLAS.

**Pitfall:** the `(p, n, n)` gather is the memory hog: for p = 10,000 and n = 100 it is 8 GB in
float64. Bound it by chunking the population (Advanced Techniques) or, for swap-based local
search on QAP, switch to O(n) delta formulas instead of batch full evaluation — vectorize the
*delta matrix*, not the objective (Taillard 1991, robust taboo search).

## Pattern Catalog III — Distance Matrices and Selection Idioms

### Pattern 7: Pairwise distance matrices

Two standard constructions: the broadcast form (simple, memory-heavy) and the Gram-matrix form
(BLAS-fast, numerically delicate). Both beat any Python double loop by 2-3 orders of magnitude.

```python
import numpy as np


def pairwise_sq_broadcast(X: np.ndarray) -> np.ndarray:
    """All-pairs squared Euclidean distances via an (n, n, d) broadcast temporary."""
    diff = X[:, None, :] - X[None, :, :]
    return (diff ** 2).sum(axis=2)


def pairwise_sq_gram(X: np.ndarray) -> np.ndarray:
    """All-pairs squared distances via ||x-y||^2 = ||x||^2 + ||y||^2 - 2 x.y (BLAS path)."""
    sq = (X ** 2).sum(axis=1)
    d2 = sq[:, None] + sq[None, :] - 2.0 * (X @ X.T)
    return np.maximum(d2, 0.0)  # clip tiny negatives from floating-point cancellation


rng = np.random.default_rng(3)
X = rng.random((5, 2))
print(np.allclose(pairwise_sq_broadcast(X), pairwise_sq_gram(X)))
# Expected: True — both constructions agree to floating-point tolerance.
```

Use the broadcast form for n up to a few thousand (the `(n, n, d)` temporary is the limit), the
Gram form when d is large, and `scipy.spatial.distance.cdist` in production — it is
C-implemented, never builds the `(n, n, d)` temporary, and supports many metrics (Virtanen et
al. 2020, "SciPy 1.0"). The same matrices feed TSP/VRP instances, p-median costs, and
distance-based population-diversity measures.

**Pitfall:** the Gram identity cancels catastrophically for near-duplicate points: `d2` can come
out as `-1e-15`, and `np.sqrt` then yields NaN that propagates through every later reduction.
Always clip at zero before the square root. If exact symmetric zeros on the diagonal matter,
enforce them explicitly with `np.fill_diagonal(d2, 0.0)`.

### Pattern 8: argpartition / argsort idioms

Most selection bookkeeping reduces to three idioms: top-k extraction (elites, parents),
rank computation (rank selection, crowding), and k-nearest-neighbor lists (candidate lists for
local search, related removal in LNS). `np.argpartition` finds an unordered top-k in O(n)
introselect; full `argsort` is O(n log n) and only needed when the complete order matters.

```python
import numpy as np


def top_k_indices(fitness: np.ndarray, k: int) -> np.ndarray:
    """Indices of the k largest fitness values, best first, in O(n + k log k)."""
    part = np.argpartition(fitness, -k)[-k:]
    return part[np.argsort(fitness[part])[::-1]]


def dense_ranks(fitness: np.ndarray) -> np.ndarray:
    """Rank of each individual (0 = worst), reproducible under ties via stable sort."""
    order = np.argsort(fitness, kind="stable")
    ranks = np.empty_like(order)
    ranks[order] = np.arange(fitness.size)
    return ranks


def neighbor_lists(dist: np.ndarray, k: int) -> np.ndarray:
    """k nearest neighbors per node (self excluded); rows are unordered within the k."""
    d = dist.copy()
    np.fill_diagonal(d, np.inf)
    return np.argpartition(d, kth=k - 1, axis=1)[:, :k]


fitness = np.array([0.2, 0.9, 0.5, 0.7, 0.1])
print(top_k_indices(fitness, 2), dense_ranks(fitness))
coords = np.array([[0.0, 0.0], [0.0, 1.0], [1.0, 1.0], [1.0, 0.0]])
dist = np.sqrt(((coords[:, None, :] - coords[None, :, :]) ** 2).sum(axis=2))
print(np.sort(neighbor_lists(dist, 2), axis=1))
# Expected: [1 3] [1 4 2 3 0]; each sorted neighbor row lists the two adjacent
# corners of the unit square (node 0 -> [1 3]), never the diagonal opposite.
```

**Pitfall:** `argpartition` guarantees only that the kth element is in its sorted position with
smaller values before it — the k results are *unordered*, so code that assumes "first is best"
is wrong. And the default `argsort` kind is an unstable introsort: under fitness ties, elite
sets can differ across NumPy versions and platforms. Pass `kind="stable"` wherever tie order
affects reported results or seeded reproducibility.

## Pattern Catalog IV — Memory and Profiling

### Pattern 9: Views, copies, temporaries, and dtype

Keep the population `(p, n)` C-contiguous so each individual is one contiguous row, prefer
reductions along the last axis, and reuse preallocated output buffers in the generation loop.
Know which operations return views (basic slices) and which return copies (advanced indexing).

```python
import numpy as np


def evaluate_into(pop: np.ndarray, values: np.ndarray, out: np.ndarray) -> np.ndarray:
    """Batch linear fitness written into a preallocated buffer (no per-call allocation)."""
    np.matmul(pop, values, out=out)
    return out


pop = np.arange(20, dtype=np.float64).reshape(4, 5)

half = pop[:2]          # basic slice  -> view (shares memory)
elite = pop[[3, 1]]     # fancy index  -> copy (independent)
print(np.shares_memory(pop, half), np.shares_memory(pop, elite))

work = np.empty_like(pop)
np.multiply(pop, pop, out=work)   # pop**2 with no temporary
work += 1.0                       # in place
print(work.sum(axis=1))
# Expected: True False, then [35. 260. 735. 1460.] — row sums of x^2 + 1
# for rows [0..4], [5..9], [10..14], [15..19].
```

dtype strategy: `int8` for binary genes (8x smaller than the default `int64`), `int32` or `int64`
for permutations, `float64` for fitness. After `pop.T` or strided slicing, restore contiguity
with `np.ascontiguousarray` before hot kernels — BLAS and reductions are bandwidth-bound, and a
contiguous gene axis is what lets them stream memory.

**Pitfall:** the elitism view bug. `best = pop[best_idx]` with a scalar index or slice returns a
*view*; when the next generation overwrites `pop` in place, your recorded best mutates with it.
Always store elites with `.copy()`. The dual bug: scatter-updates with duplicate indices,
`counts[idx] += 1`, silently drop repeats because the gather-modify-scatter is buffered — use
`np.add.at(counts, idx, 1)` or `np.bincount`. And chained indexing `pop[mask][:, 0] = 1` writes
into a temporary copy and is lost; use single-step indexing `pop[mask, 0] = 1`.

### Pattern 10: Profiling to find loops worth removing

Profile, vectorize, then prove equivalence and measure the speedup — all in one harness. The
naive implementation is kept permanently: it is the test oracle for the fast one.

```python
import cProfile
import io
import pstats
import time
from collections.abc import Callable

import numpy as np


def loop_fitness(pop: np.ndarray, values: np.ndarray, weights: np.ndarray,
                 capacity: float) -> np.ndarray:
    """Per-individual Python-loop evaluation: the 'before' version and test oracle."""
    out = np.empty(pop.shape[0])
    for i in range(pop.shape[0]):
        v = 0.0
        w = 0.0
        for j in range(pop.shape[1]):
            if pop[i, j]:
                v += values[j]
                w += weights[j]
        out[i] = v if w <= capacity else v - 100.0 * (w - capacity)
    return out


def batch_fitness(pop: np.ndarray, values: np.ndarray, weights: np.ndarray,
                  capacity: float) -> np.ndarray:
    """Vectorized equivalent: the 'after' version."""
    v = pop @ values
    over = np.maximum(pop @ weights - capacity, 0.0)
    return v - 100.0 * over


def best_time(fn: Callable[[], np.ndarray], repeats: int = 5) -> float:
    """Minimum wall-clock time of fn() over several repeats (warm-up excluded)."""
    times = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        fn()
        times.append(time.perf_counter() - t0)
    return min(times)


rng = np.random.default_rng(1)
pop = rng.integers(0, 2, size=(512, 200)).astype(np.float64)
values = rng.random(200)
weights = rng.random(200)

profiler = cProfile.Profile()
profiler.enable()
for _ in range(20):
    loop_fitness(pop, values, weights, capacity=50.0)
profiler.disable()
stream = io.StringIO()
pstats.Stats(profiler, stream=stream).sort_stats("cumulative").print_stats(5)
print(stream.getvalue().strip().splitlines()[0])

ref = loop_fitness(pop, values, weights, 50.0)
fast = batch_fitness(pop, values, weights, 50.0)
t_loop = best_time(lambda: loop_fitness(pop, values, weights, 50.0))
t_vec = best_time(lambda: batch_fitness(pop, values, weights, 50.0))
print(np.allclose(ref, fast), f"speedup ~{t_loop / t_vec:.0f}x")
# Expected: a pstats header line, then True and a speedup of two to three
# orders of magnitude depending on hardware and BLAS backend.
```

Read profiles in two passes: `cumulative` time finds which top-level phase dominates
(evaluation vs operators vs bookkeeping); `tottime` finds the function whose own body burns the
cycles. For per-line attribution inside one hot function, use `line_profiler`.

**Pitfall:** `cProfile` instruments Python function calls only — it cannot see inside a NumPy
ufunc, and its per-call overhead inflates code with many tiny Python calls relative to code with
few large array calls. Compare candidate kernels with `time.perf_counter` (or `timeit`) on
realistic sizes, not under the profiler. And beware the benchmarking trap of measuring the first
call: it pays warm-up costs (allocator, BLAS thread pool, JIT); time a loop of repeated calls.

## Advanced Techniques

### Whole-neighborhood delta matrices

For best-improvement local search, vectorize the *move evaluation*, not the objective: compute
the delta of every move in one broadcast expression, then `argmin`. For symmetric TSP 2-opt, the
move (i, j) replaces edges (t_i, s_i) and (t_j, s_j) with (t_i, t_j) and (s_i, s_j), so all
O(n^2) deltas come from four gathered matrices:

```python
import numpy as np


def all_two_opt_deltas(dist: np.ndarray, tour: np.ndarray) -> np.ndarray:
    """Delta of every 2-opt move (i, j), i < j: reverse tour positions i+1..j."""
    t = tour
    s = np.roll(tour, -1)
    removed = dist[t, s]
    delta = (dist[t[:, None], t[None, :]] + dist[s[:, None], s[None, :]]
             - removed[:, None] - removed[None, :])
    upper = np.triu(np.ones_like(delta, dtype=bool), k=1)
    return np.where(upper, delta, np.inf)


coords = np.array([[0.0, 0.0], [0.0, 1.0], [1.0, 1.0], [1.0, 0.0]])
dist = np.sqrt(((coords[:, None, :] - coords[None, :, :]) ** 2).sum(axis=2))
tour = np.array([0, 2, 1, 3])  # crossing tour of length 2 + 2*sqrt(2)
deltas = all_two_opt_deltas(dist, tour)
i, j = np.unravel_index(int(np.argmin(deltas)), deltas.shape)
print((i, j), round(float(deltas[i, j]), 3))
# Expected: (0, 2) -0.828 — uncrossing the tour saves 2*sqrt(2) - 2,
# restoring the optimal unit-square tour of length 4.
```

This is a constant-factor accelerator for one scan; pair it with neighbor-list pruning
(Pattern 8) to cut the scan from O(n^2) to O(n·k), and with delta *tables* maintained across
moves for QAP-style problems (Taillard 1991).

### Chunked evaluation to bound peak memory

When a batch expression needs a `(p, n, n)` temporary, evaluate in fixed-size chunks: same
result, bounded peak memory, and only one extra Python-level loop whose per-iteration body is
large enough to amortize dispatch.

```python
import numpy as np
from collections.abc import Callable


def chunked_eval(pop: np.ndarray, evaluate: Callable[[np.ndarray], np.ndarray],
                 chunk: int) -> np.ndarray:
    """Apply a batch evaluator in fixed-size chunks to bound peak temporary memory."""
    out = np.empty(pop.shape[0], dtype=np.float64)
    for start in range(0, pop.shape[0], chunk):
        block = slice(start, start + chunk)
        out[block] = evaluate(pop[block])
    return out


def qap_batch(A: np.ndarray, B: np.ndarray, perms: np.ndarray) -> np.ndarray:
    """QAP batch objective; peak temporary is O(len(perms) * n^2) floats."""
    return np.einsum("ij,pij->p", A, B[perms[:, :, None], perms[:, None, :]])


rng = np.random.default_rng(5)
n, p = 12, 1000
A = rng.integers(0, 10, (n, n)).astype(np.float64)
B = rng.integers(0, 10, (n, n)).astype(np.float64)
perms = rng.permuted(np.tile(np.arange(n), (p, 1)), axis=1)
full = qap_batch(A, B, perms)
chunked = chunked_eval(perms, lambda blk: qap_batch(A, B, blk), chunk=128)
print(np.allclose(full, chunked))
# Expected: True — identical objectives, but the chunked version's largest
# temporary is 128*12*12 floats instead of 1000*12*12.
```

Pick the chunk size so the temporary fits comfortably in the last-level cache or at worst a few
percent of RAM; throughput is flat over a wide range, so round numbers (128-4096) are fine.

### JIT compilation for inherently sequential loops

Simulated annealing's accept/reject chain, label-correcting shortest paths, and serial schedule
decoders have iteration t depending on t-1: no array axis exists to vectorize over. The tool is
Numba (`@numba.njit` on a function whose body uses NumPy arrays and scalars), which compiles the
loop to machine code at ~C speed (Lam, Pitrou & Seibert 2015, "Numba: a LLVM-based Python JIT
compiler"). Practical rules: keep JIT kernels small and purely numeric; pass arrays and scalars,
not Python objects; hoist all allocation out of the kernel; and keep a pure-Python twin of each
kernel as the test oracle, exactly as in Pattern 10. Expect the first call to pay a compilation
delay of 0.1-1 s — irrelevant for runs of minutes, confusing in micro-benchmarks.

### dtype strategy and BLAS threading

float32 halves memory traffic and roughly doubles throughput on bandwidth-bound kernels
(distance matrices, large populations), at ~7 decimal digits of precision — enough for fitness
*comparison*, not always for accumulating 10^6 terms; when in doubt, reduce in float64 via
`np.sum(x, dtype=np.float64)`. NumPy's `sum` uses pairwise summation, so error grows like
O(log n), but mixed-precision deltas still drift — resynchronize with a full evaluation every
few thousand moves. Separately, `@`/`einsum` calls are multithreaded by the BLAS backend; when
you also parallelize at the process level, cap BLAS threads per worker (threadpoolctl, or
`OMP_NUM_THREADS=1`) or p workers × c BLAS threads will oversubscribe p·c threads onto c cores
and run *slower* than serial — coordinate with **parallel-and-hybrid-metaheuristics**.

## Practical Challenges

**The vectorized version is slower than the loop.** The arrays are too small to amortize the
~1 µs per-call dispatch: ten chained ufuncs on a `(30,)` array cost more than 30 interpreter
iterations. Batch a bigger axis into the call (whole population, whole neighborhood); if no such
axis exists, the loop was fine — JIT it instead of vectorizing it.

**Memory exploded after broadcasting.** An `(n, 1, d) - (1, n, d)` difference or a `(p, n, n)`
gather materialized gigabytes. Chunk the batch axis, switch to the Gram form, use
`scipy.spatial.distance.cdist`, or contract with `einsum` so the intermediate is never built.
Measure peak with `tracemalloc` — the profiler shows time, not memory.

**Same seed, different results after vectorizing.** Expected: batch sampling consumes the RNG
stream in a different order than the loop did, so trajectories diverge even though both are
correct. Do not chase bit-equality of full runs. Test operators on fixed inputs, test the
evaluator with `np.allclose` against the naive oracle, and compare run *distributions* over
seeds.

**Scatter updates lose increments.** `counts[idx] += 1` with duplicate entries in `idx` applies
the gather-modify-scatter once per *unique* index, silently dropping repeats. Use
`np.add.at(counts, idx, 1)` (unbuffered) or `np.bincount(idx, minlength=n)` — the latter is much
faster for large index arrays.

**NaNs appeared in the distance matrix.** The Gram identity produced `-1e-15` for near-duplicate
points and `sqrt` turned it into NaN, which then poisoned every `min`/`argmin` downstream. Clip
squared distances at zero before the root; audit with `np.isnan(D).any()` in the validator.

**Silent integer overflow after a dtype "optimization".** Flow×distance products in int32 wrap
around without any warning (NumPy fixed-width ints are modular). Promote to int64 or float64
before products of large magnitudes, and keep an eye on `np.iinfo(dtype).max` versus the largest
representable intermediate, not just the final objective.

**Boolean-mask writes do not stick.** `pop[mask][:, 0] = 1` first creates a copy (`pop[mask]`),
then writes into that copy, then discards it. Fuse into one indexing expression,
`pop[mask, 0] = 1`, which NumPy translates into a true in-place scatter.

**The profile now shows time smeared across dozens of ufuncs.** That is the signature of
small-array vectorization inside a remaining Python loop: each ufunc is individually cheap, the
dispatch sum is not. Lift the loop axis into the arrays (Patterns 2-6) so the call count per
generation is O(1) instead of O(p).

**Vectorized code became unreadable.** Mask algebra with four broadcast axes is write-only code.
Name every intermediate after its meaning, comment the shape on each line (`# (p, n)`), assert
shapes at function entry, and keep the naive loop implementation in the test suite as executable
documentation of the semantics.

**Speedup vanished under multiprocessing.** Each worker's BLAS spawned its own thread pool and
the machine thrashed on context switches. Set one BLAS thread per worker (threadpoolctl or
`OMP_NUM_THREADS=1`) and keep process-level parallelism for independent runs; vectorize within a
run, parallelize across runs.

## Tools & Libraries

| Tool / library | When to use | Note |
|---|---|---|
| numpy | everything in this skill | use the `default_rng` Generator API, not the legacy global state |
| scipy.spatial.distance | distance matrices in production | `cdist`/`pdist`: C loops, no `(n, n, d)` temporary, many metrics |
| scipy.sparse | huge sparse incidence matrices (set covering, assignment) | `csr_matrix @ x` batch-evaluates coverage cheaply |
| numba | inherently sequential kernels (SA chains, decoders) | `@njit`; keep kernels numeric-only; first call pays compile time |
| cProfile + pstats | first-pass, call-level profiling | sort by `cumulative` then `tottime`; cannot see inside ufuncs |
| line_profiler | per-line timing of one hot function | decorate with `@profile`, run `kernprof -lv` |
| tracemalloc | peak-memory measurement | catches broadcast temporaries the time profiler never shows |
| threadpoolctl | cap BLAS threads per process | mandatory when mixing `@`-heavy code with multiprocessing |
| timeit / perf_counter | micro-benchmarks of candidate kernels | repeat and take the minimum; never time the first (warm-up) call |
| numexpr | very long elementwise expression chains | evaluates without temporaries, multithreaded; niche but easy |

## Output Format

A vectorization task is complete when it produces three artifacts: the fast code, the proof of
equivalence, and the before/after measurement. Work through this checklist:

**Vectorization checklist**

1. Profile captured before any change; the target loop demonstrably dominates (>30% runtime).
2. Algorithmic reductions (delta evaluation, caching) considered first and either applied or
   ruled out with a reason.
3. Naive reference implementation preserved and importable as the test oracle.
4. Vectorized version validated with `np.allclose` (state rtol/atol) on randomized inputs,
   including edge shapes: empty selection, single individual, all-equal fitness ties.
5. All randomness drawn from an explicit `np.random.Generator` parameter; seeds recorded.
6. Shapes commented on non-obvious lines; dtypes chosen deliberately and stated.
7. Peak memory of new temporaries estimated (and chunked if above budget); `tracemalloc` spot
   check on the largest instance.
8. Before/after timings on realistic sizes with `perf_counter` over repeated calls; report both
   kernel speedup and whole-run speedup (Amdahl).
9. Stable sorts (`kind="stable"`) wherever tie order affects reported results.
10. BLAS thread interaction checked if the code also runs under multiprocessing.

**Before/after report template (filled example)**

```text
Vectorization report — knapsack batch fitness
target          : loop_fitness() in ga/evaluate.py
profile before  : 82% of a 60 s GA run inside loop_fitness (cProfile, cumulative)
baseline        : 512 x 200 population, 1.8e4 evals/s  (Python loop)
vectorized      : same instance,        6.1e6 evals/s  (pop @ values, ~330x kernel)
equivalence     : np.allclose(ref, fast, rtol=1e-12, atol=0) on 50 random pops -> True
rng             : default_rng(seed) per run; draw order changed -> distribution tests only
peak memory     : +0.9 MB (two (512,) temporaries); tracemalloc verified
dtype           : pop cast once/generation to float64; data vectors float64
whole-run gain  : 4.7x wall clock (evaluation was 82% of runtime -> Amdahl-consistent)
```

Report kernel and whole-run numbers separately in papers and experiment logs; store both in the
run table (see **pandas-experiment-management**).

## Questions to Ask

- Do you have a profile, or shall we capture one first? Which function dominates, and by what
  fraction of total runtime?
- Is the algorithm population-based or a single-solution trajectory method? Where exactly is the
  hot loop: fitness, operators, neighborhood scan, or bookkeeping?
- What are the realistic sizes — population, solution length, instance count — now and at the
  largest experiment you plan?
- Can the objective be written as gathers, reductions, and matrix products, or does it contain a
  sequential recursion (e.g., schedule propagation)?
- How much RAM is available, and are O(n^2) or O(p·n^2) temporaries acceptable?
- What reproducibility do you need: same-seed bit equality with the old code, or statistically
  equivalent results with recorded seeds?
- Are SciPy and Numba acceptable dependencies, or is this NumPy-only?
- Will this code also run under multiprocessing or on a shared cluster node (BLAS threading)?
- Is there already a delta/incremental evaluation, or would that beat vectorization here?
- What throughput target would make the experiment plan feasible — and can we stop there?

## Related Skills

- **fitness-evaluation-and-caching** — when the win should come from computing less work (delta
  and incremental evaluation, memoization, surrogates) rather than doing the same work faster.
- **genetic-algorithms** — when these vectorized population patterns need to be assembled into a
  complete GA loop with selection, crossover, mutation, and elitism.
- **parallel-and-hybrid-metaheuristics** — when single-process vectorization is exhausted and
  the next factor must come from multiprocessing, island models, or portfolios.
- **pandas-experiment-management** — when before/after timings, speedups, and seeds need to be
  recorded as tidy run tables and aggregated across instances.
