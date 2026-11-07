---
name: parallel-and-hybrid-metaheuristics
description: When the user wants to parallelize a metaheuristic or combine several searches — island models with migration, master-slave fitness evaluation, parallel multistart, cooperative search, or algorithm portfolios — with the Python practicalities (multiprocessing, joblib, vectorization-first). Also use when the user mentions "parallel metaheuristic," "island model," "migration," "master-slave," "cooperative search," "portfolio," or when single runs are too slow and CPU cores sit idle. For removing Python loops inside one process, see numpy-vectorization-for-optimization; for choosing the base algorithm, see metaheuristic-design-principles.
---

# Parallel and Hybrid Metaheuristics

You are an expert in parallel and hybrid metaheuristics for combinatorial optimization.
This skill covers the architectures that distribute or combine searches — island models
with migration, master-slave fitness evaluation, independent multistart, cooperative
search with shared elite memory, and algorithm portfolios — together with the Python
practicalities (multiprocessing, joblib, picklable workers, seed management) that decide
whether a parallel design actually pays off. Use the framework below to pick an
architecture from the bottleneck profile, implement it with process pools and numpy,
and report speedups honestly.

## Initial Assessment

Establish the following before recommending an architecture or writing any code:

- **Profile first.** What fraction of wall-clock time is fitness evaluation? What fraction
  is operators, copying, bookkeeping? Parallelizing a part that takes 10% of runtime caps
  the speedup at 1.11x regardless of core count.
- **Cost of one evaluation.** Microseconds (pure arithmetic), milliseconds (delta-evaluated
  neighborhood scans), or seconds (simulation, embedded LP/ML model)? This single number
  selects the architecture: see the decision guidance below.
- **Vectorization status.** Is the base algorithm already numpy-vectorized at the population
  level? One vectorized process routinely beats eight processes running slow Python loops.
  Climb the vectorization rung before the parallelism rung.
- **Base method class.** Population-based (GA, DE, ACO) maps naturally to islands and
  master-slave; single-solution methods (ILS, SA, tabu) map to multistart, cooperative
  search, and portfolios.
- **Hardware.** Physical cores (not hyperthreads), memory per worker, single machine or
  cluster. Most research workloads end at one machine with 8-64 cores; design for that first.
- **Operating system and start method.** Windows and macOS spawn worker processes (fresh
  interpreter, everything pickled); Linux can fork. Spawn imposes module-level worker
  functions and `if __name__ == "__main__"` guards.
- **Picklability.** Can the objective and instance data cross a process boundary? Open
  solver handles, database connections, GUI objects, and lambdas cannot.
- **Goal type.** Shorter wall-clock to reach the same quality, or better quality within the
  same wall-clock? Island models and cooperation target the second; master-slave targets
  the first.
- **Reproducibility requirement.** Bit-for-bit reproducible runs rule out asynchronous
  designs whose result depends on OS scheduling; synchronous patterns with
  `SeedSequence.spawn` keep determinism.
- **Experiment-level parallelism.** A study running 10 instances x 10 seeds already has 100
  independent jobs. Parallelizing across runs is trivial, perfectly efficient, and often all
  that is needed — check this before touching the algorithm's internals.
- **Time budget per run and per study.** Communication-heavy designs amortize poorly over
  short runs; a 5-second run cannot absorb 0.5 s of pool startup.

## Parallel Architectures

Five architectures cover practice. The classification follows Crainic & Toulouse (2010),
"Parallel Metaheuristics" (Handbook of Metaheuristics), and Alba (2005), "Parallel
Metaheuristics: A New Class of Algorithms".

| Architecture | Grain | What runs in parallel | Communication | Changes search behavior? |
|---|---|---|---|---|
| Master-slave (global) | fine | fitness evaluations of one population | every generation, master <-> workers | no — same trajectory, faster |
| Island model (coarse) | coarse | whole subpopulations | rare migration events | yes — restricted mixing |
| Cellular (fine-grained) | very fine | per-individual updates on a grid | implicit, overlapping neighborhoods | yes — slow diffusion |
| Independent multistart | run-level | full runs with different seeds | none | no — same per-run distribution |
| Cooperative search | coarse | heterogeneous searches | shared elite pool / adaptive memory | yes — by design |

Algorithm **portfolios** are multistart generalized across algorithms: run several
different methods (or configurations) on the same instance and keep the best result
(Huberman, Lukose & Hogg 1997, "An Economics Approach to Hard Computational Problems";
Gomes & Selman 2001, "Algorithm Portfolios").

### Speedup arithmetic

Speedup and efficiency with $p$ workers, where $T_p$ is wall-clock time:

$$
S(p) = \frac{T_1}{T_p}, \qquad E(p) = \frac{S(p)}{p}.
$$

Amdahl (1967): if only a fraction $\phi$ of the work parallelizes,

$$
S(p) \le \frac{1}{(1-\phi) + \phi/p}.
$$

With $\phi = 0.9$ (evaluation is 90% of runtime), 16 workers give at most 6.4x. This is
why master-slave designs must move *all* heavy work, not just part of it, into workers.

For independent multistart there is a second, quality-based argument. If one run reaches a
target quality with probability $q$ within the budget, $p$ independent runs succeed with
probability $1-(1-q)^p$. Empirically, time-to-target of well-designed GRASP/ILS-type
methods is approximately exponentially distributed (Aiex, Resende & Ribeiro 2002,
"Probability distribution of solution time in GRASP"), and the minimum of $p$ i.i.d.
exponentials is exponential with rate multiplied by $p$ — independent multistart then
achieves near-linear speedup in expected time-to-target with zero communication.

### Decision guidance

- **Use master-slave when** one evaluation costs >= 1-10 ms and dominates runtime
  (simulation-based objectives, embedded solver calls). It preserves the algorithm exactly;
  only wall-clock changes, so no re-tuning is needed.
- **Use an island model when** the method is population-based, evaluation is cheap, and the
  goal is better quality at equal time. Restricted migration preserves diversity that a
  single panmictic population loses (Whitley, Rana & Heckendorn 1999, "The island model
  genetic algorithm: on separability, population size and convergence"). Islands also give
  near-perfect parallel efficiency because communication is rare.
- **Use independent multistart when** the base method is single-solution with high
  run-to-run variance (ILS, SA). It is the easiest correct parallelization and a mandatory
  baseline for any fancier design: a cooperative scheme that cannot beat independent
  multistart at equal core-count is not cooperating usefully.
- **Use cooperative search when** different searches can exploit each other's elites —
  e.g., construction-heavy and improvement-heavy methods, or differently-tuned copies of one
  method. The shared elite pool is the "adaptive memory" of Rochat & Taillard (1995),
  "Probabilistic diversification and intensification in local search for vehicle routing".
- **Use a portfolio when** no single algorithm dominates across instances or runtime is
  heavy-tailed; racing configurations hedges the choice. Portfolios compose with everything
  above (each entry may itself be parallel).
- **Skip cellular models in Python** unless targeting GPUs; their very fine grain suits
  SIMD hardware, not process pools.

### The vectorization-first ladder

Climb in order; each rung is cheaper to implement and to debug than the next.

1. **Vectorize within one process** — numpy population operations, batch fitness, delta
   evaluation. Often 10-100x; no new failure modes.
2. **Parallelize evaluation** — master-slave over a process pool; only when one call is
   expensive enough to amortize pickling (rule of thumb: task >= 1 ms, better >= 10 ms).
3. **Parallelize runs** — multistart, islands, portfolios; communication rare or absent.
4. **Distribute** — ray / mpi4py / dask across machines, only when one machine is provably
   insufficient.

The Python global interpreter lock (GIL) serializes pure-Python bytecode across threads,
so CPU-bound metaheuristics need *processes*, not threads. numpy releases the GIL inside
large array operations, which is exactly why rung 1 works so well.

## Reference Implementation: Synchronous Island Model

The island model is an algorithmic structure first and a parallelization second: the
restricted-migration dynamics improve search even when islands execute sequentially in one
process. The framework below is problem-independent — `init` and `step` are the only
problem-specific parts (swap in any population method; see genetic-algorithms for a
complete GA `step`).

```text
ISLAND_MODEL(init, step, k, interval, m, topology, G):
    for i in 1..k:
        (P_i, F_i) <- init(rng_i)            # rng_i spawned from one SeedSequence
    for gen in 1..G:
        for i in 1..k:                       # parallelizable: islands are independent
            (P_i, F_i) <- step(P_i, F_i, rng_i)
        if gen mod interval == 0:            # rare, structured communication
            for i in 1..k:
                E_i <- copies of the m best of island i      # select emigrants FIRST
            for i in 1..k:
                for each source j of island i under topology:
                    replace the m worst of island i with E_j
    return best individual over all islands
```

```python
"""Problem-independent synchronous island model over swappable (init, step) callables."""
from dataclasses import dataclass
from typing import Callable

import numpy as np

InitFn = Callable[[np.random.Generator], tuple[np.ndarray, np.ndarray]]
StepFn = Callable[[np.ndarray, np.ndarray, np.random.Generator],
                  tuple[np.ndarray, np.ndarray]]


@dataclass
class IslandConfig:
    """Topology and migration policy of a synchronous island model."""
    n_islands: int = 8
    migration_interval: int = 25        # generations between migration events
    n_migrants: int = 2                 # emigrants per island per event
    topology: str = "ring"              # "ring" or "complete"


def migrate(pops: list[np.ndarray], fits: list[np.ndarray],
            cfg: IslandConfig) -> None:
    """Copy each island's best into its neighbors, replacing the targets' worst.

    Emigrants are selected before any replacement, so a solution overwritten on
    its home island still travels intact. Minimization; modifies in place.
    """
    k = len(pops)
    sel = [np.argpartition(f, cfg.n_migrants)[:cfg.n_migrants] for f in fits]
    movers = [(p[s].copy(), f[s].copy()) for p, f, s in zip(pops, fits, sel)]
    for i in range(k):
        sources = [(i - 1) % k] if cfg.topology == "ring" else \
            [j for j in range(k) if j != i]
        inc = np.vstack([movers[j][0] for j in sources])
        inc_fit = np.concatenate([movers[j][1] for j in sources])
        worst = np.argpartition(fits[i], -inc.shape[0])[-inc.shape[0]:]
        pops[i][worst] = inc
        fits[i][worst] = inc_fit


def run_island_model(init: InitFn, step: StepFn, cfg: IslandConfig,
                     n_generations: int, seed: int) -> tuple[np.ndarray, float]:
    """Evolve cfg.n_islands subpopulations with periodic migration; return the best."""
    rngs = [np.random.default_rng(s)
            for s in np.random.SeedSequence(seed).spawn(cfg.n_islands)]
    pops, fits = map(list, zip(*(init(r) for r in rngs)))
    for gen in range(1, n_generations + 1):
        for i in range(cfg.n_islands):
            pops[i], fits[i] = step(pops[i], fits[i], rngs[i])
        if gen % cfg.migration_interval == 0:
            migrate(pops, fits, cfg)
    i = int(np.argmin([f.min() for f in fits]))
    j = int(np.argmin(fits[i]))
    return pops[i][j].copy(), float(fits[i][j])


if __name__ == "__main__":
    def init(rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
        """40 random binary strings; objective: minimize the number of zeros."""
        pop = rng.integers(0, 2, size=(40, 64))
        return pop, (64 - pop.sum(axis=1)).astype(float)

    def step(pop: np.ndarray, fit: np.ndarray,
             rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
        """Elitist bit-flip step applied to every population slot at once."""
        child = np.where(rng.random(pop.shape) < 1 / 64, 1 - pop, pop)
        child_fit = (64 - child.sum(axis=1)).astype(float)
        keep = child_fit < fit
        return np.where(keep[:, None], child, pop), np.where(keep, child_fit, fit)

    sol, val = run_island_model(init, step, IslandConfig(n_islands=4), 600, seed=3)
    print(val)
    # Expected: 0.0 (the all-ones string is found) on nearly all seeds within
    # 600 generations; 4 islands of 40 with ring migration every 25 generations.
```

### Parameter guidance

| Parameter | Typical range | What it trades off |
|---|---|---|
| `n_islands` | 4-16 on one machine (one process per island at the parallel rung) | more islands: more diversity and parallelism, but each subpopulation gets smaller and weaker |
| subpopulation size | 30-200 per island | within-island selection strength vs total evaluation budget per generation |
| `migration_interval` | 10-50 generations | frequent: islands merge into one effective panmictic population; rare: islands converge separately and synergy arrives too late |
| `n_migrants` | 1-5 (<= 5% of the subpopulation) | takeover speed vs diversity; migration is itself a selection operator |
| `topology` | ring (default), complete, random k-regular | takeover time: ring slowest (most diversity), complete fastest (Cantu-Paz 2000, "Efficient and Accurate Parallel Genetic Algorithms") |
| migrant policy | best-replace-worst (default); random-replace-random for gentler pressure | the selection pressure added by migration on top of within-island selection |
| sync vs async | synchronous (default in Python) | reproducibility and simplicity vs no barrier wait at segment ends |

## Worked Example: Island GA with Migration for TSP

A complete, parallel island GA for the symmetric TSP. The pattern is
**segment-synchronous**: each process-pool task evolves one island for
`migration_interval` generations, the master gathers the islands, performs ring
migration, and dispatches the next segment. This keeps communication at one
gather/scatter per segment, so parallel efficiency stays high. Operator details (order
crossover, inversion mutation, tournament selection) are standard; see crossover-operators
and mutation-and-perturbation-operators for the full catalogs and genetic-algorithms for
panmictic GA design.

```python
"""Island GA for the symmetric TSP: ring migration, islands in worker processes."""
from concurrent.futures import ProcessPoolExecutor

import numpy as np


def tour_lengths(pop: np.ndarray, dist: np.ndarray) -> np.ndarray:
    """Vectorized lengths of a population of closed tours; pop has shape (P, n)."""
    return dist[pop, np.roll(pop, -1, axis=1)].sum(axis=1)


def nearest_neighbor(dist: np.ndarray, start: int) -> np.ndarray:
    """Nearest-neighbor construction; standard warm start for TSP populations."""
    n = dist.shape[0]
    unvisited = np.ones(n, dtype=bool)
    unvisited[start] = False
    tour = [start]
    for _ in range(n - 1):
        cand = np.flatnonzero(unvisited)
        nxt = int(cand[np.argmin(dist[tour[-1], cand])])
        tour.append(nxt)
        unvisited[nxt] = False
    return np.array(tour)


def order_crossover(p1: np.ndarray, p2: np.ndarray,
                    rng: np.random.Generator) -> np.ndarray:
    """OX: keep a random slice of p1, fill the rest in p2's order."""
    n = p1.shape[0]
    a, b = np.sort(rng.choice(n, size=2, replace=False))
    child = np.full(n, -1, dtype=p1.dtype)
    child[a:b + 1] = p1[a:b + 1]
    child[np.concatenate([np.arange(b + 1, n), np.arange(a)])] = (
        p2[~np.isin(p2, p1[a:b + 1])])
    return child


def generation(pop: np.ndarray, fit: np.ndarray, dist: np.ndarray,
               rng: np.random.Generator, elite: int = 2,
               p_mut: float = 0.9) -> tuple[np.ndarray, np.ndarray]:
    """One elitist generation: tournament-3 parents, OX, inversion mutation."""
    P, n = pop.shape
    new = np.empty_like(pop)
    new[:elite] = pop[np.argsort(fit)[:elite]]
    cand = rng.integers(0, P, size=(2, P - elite, 3))
    winners = np.take_along_axis(
        cand, np.argmin(fit[cand], axis=2)[..., None], axis=2)[..., 0]
    for i in range(P - elite):
        child = order_crossover(pop[winners[0, i]], pop[winners[1, i]], rng)
        if rng.random() < p_mut:
            a, b = np.sort(rng.choice(n, size=2, replace=False))
            child[a:b + 1] = child[a:b + 1][::-1]      # inversion mutation
        new[elite + i] = child
    return new, tour_lengths(new, dist)


def evolve_segment(args: tuple[np.ndarray, np.ndarray, np.ndarray,
                               np.random.SeedSequence, int]
                   ) -> tuple[np.ndarray, np.ndarray]:
    """Advance one island by `gens` generations (module-level so it pickles)."""
    pop, fit, dist, seed, gens = args
    rng = np.random.default_rng(seed)
    for _ in range(gens):
        pop, fit = generation(pop, fit, dist, rng)
    return pop, fit


def ring_migration(pops: list[np.ndarray], fits: list[np.ndarray],
                   n_migrants: int) -> None:
    """Island i-1 sends copies of its best to island i, replacing i's worst."""
    k = len(pops)
    sel = [np.argpartition(f, n_migrants)[:n_migrants] for f in fits]
    movers = [(pops[i][sel[i]].copy(), fits[i][sel[i]].copy()) for i in range(k)]
    for i in range(k):
        sol, val = movers[(i - 1) % k]
        worst = np.argpartition(fits[i], -n_migrants)[-n_migrants:]
        pops[i][worst] = sol
        fits[i][worst] = val


def island_ga_tsp(dist: np.ndarray, n_islands: int = 4, pop_size: int = 80,
                  n_segments: int = 12, seg_gens: int = 25, n_migrants: int = 2,
                  seed: int = 0, workers: int | None = None
                  ) -> tuple[np.ndarray, float]:
    """Segment-synchronous island GA: evolve islands in parallel, migrate, repeat."""
    n = dist.shape[0]
    ss = np.random.SeedSequence(seed)
    rng = np.random.default_rng(ss)
    pops = [np.array([nearest_neighbor(dist, int(rng.integers(n)))
                      if j < 4 else rng.permutation(n)        # 4 warm starts/island
                      for j in range(pop_size)])
            for _ in range(n_islands)]
    fits = [tour_lengths(p, dist) for p in pops]
    with ProcessPoolExecutor(max_workers=workers) as ex:
        for _ in range(n_segments):
            seeds = ss.spawn(n_islands)            # fresh child streams per segment
            jobs = [(pops[i], fits[i], dist, seeds[i], seg_gens)
                    for i in range(n_islands)]
            pops, fits = map(list, zip(*ex.map(evolve_segment, jobs)))
            ring_migration(pops, fits, n_migrants)
    i = int(np.argmin([f.min() for f in fits]))
    j = int(np.argmin(fits[i]))
    return pops[i][j].copy(), float(fits[i][j])


if __name__ == "__main__":
    rng = np.random.default_rng(42)
    pts = rng.random((40, 2))
    dist = np.linalg.norm(pts[:, None, :] - pts[None, :, :], axis=2)
    tour, length = island_ga_tsp(dist, seed=7)
    assert sorted(tour.tolist()) == list(range(40))    # valid permutation
    print(round(length, 3))
    # Expected: ~5.2-5.6 (seed 7 gives 5.437): the GA improves the best
    # nearest-neighbor start (5.71) but, without local search, will not close
    # the gap to the ~4.5-5.0 2-opt level — hybridize (memetic-algorithms) for
    # that. Wall-clock drops near-linearly up to n_islands workers.
```

Two implementation points matter. First, the per-segment `ss.spawn(n_islands)` gives
every island a fresh, statistically independent stream each segment without shipping
generator state back from the workers — simple and reproducible. Second, `dist` is
re-pickled into every task; for instances above a few MB, move it into the workers once
via the pool `initializer` pattern shown in the master-slave section.

## Worked Example: Parallel Multistart ILS with multiprocessing

Independent multistart is the correct first parallelization for single-solution methods.
Each worker runs a full ILS (2-opt descent plus double-bridge kicks; see
local-search design notes in metaheuristic-design-principles and the ILS loop in its own
skill) from its own seed; the master takes the minimum. No communication, perfect
load-balance granularity at the run level, and the exponential time-to-target argument
above predicts near-linear speedup to a fixed quality target.

```python
"""Parallel multistart ILS for the symmetric TSP with a process pool."""
from concurrent.futures import ProcessPoolExecutor

import numpy as np


def tour_length(tour: np.ndarray, dist: np.ndarray) -> float:
    """Length of one closed tour."""
    return float(dist[tour, np.roll(tour, -1)].sum())


def two_opt(tour: np.ndarray, dist: np.ndarray) -> np.ndarray:
    """2-opt descent; the delta scan over all j for fixed i is vectorized."""
    n = tour.shape[0]
    improved = True
    while improved:
        improved = False
        for i in range(n - 2):
            a, b = tour[i], tour[i + 1]
            j = np.arange(i + 2, n)
            c, d = tour[j], tour[(j + 1) % n]
            delta = dist[a, c] + dist[b, d] - dist[a, b] - dist[c, d]
            k = int(np.argmin(delta))
            if delta[k] < -1e-10:
                jj = i + 2 + k
                tour[i + 1: jj + 1] = tour[i + 1: jj + 1][::-1]
                improved = True
    return tour


def double_bridge(tour: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Classic 4-opt kick: cut into four segments A|B|C|D, reorder to A C B D."""
    n = tour.shape[0]
    a, b, c = np.sort(rng.choice(np.arange(1, n), size=3, replace=False))
    return np.concatenate([tour[:a], tour[b:c], tour[a:b], tour[c:]])


def ils_run(args: tuple[np.ndarray, np.random.SeedSequence, int]
            ) -> tuple[float, np.ndarray]:
    """One independent ILS run (module-level so it pickles under spawn)."""
    dist, seed, n_kicks = args
    rng = np.random.default_rng(seed)
    cur = two_opt(rng.permutation(dist.shape[0]), dist)
    cur_len = tour_length(cur, dist)
    best, best_len = cur.copy(), cur_len
    for _ in range(n_kicks):
        cand = two_opt(double_bridge(cur, rng), dist)
        cand_len = tour_length(cand, dist)
        if cand_len < cur_len - 1e-10:          # better-only acceptance
            cur, cur_len = cand, cand_len
            if cur_len < best_len:
                best, best_len = cur.copy(), cur_len
    return best_len, best


def parallel_multistart_ils(dist: np.ndarray, n_starts: int, n_kicks: int,
                            seed: int, workers: int | None = None
                            ) -> tuple[np.ndarray, float]:
    """Run n_starts independent ILS in separate processes; return the best."""
    seeds = np.random.SeedSequence(seed).spawn(n_starts)
    jobs = [(dist, s, n_kicks) for s in seeds]
    with ProcessPoolExecutor(max_workers=workers) as ex:
        results = list(ex.map(ils_run, jobs))
    best_len, best = min(results, key=lambda r: r[0])
    return best, best_len


if __name__ == "__main__":
    rng = np.random.default_rng(11)
    pts = rng.random((60, 2))
    dist = np.linalg.norm(pts[:, None, :] - pts[None, :, :], axis=2)
    best, best_len = parallel_multistart_ils(dist, n_starts=8, n_kicks=150, seed=0)
    print(round(best_len, 3))
    # Expected: 6.305 — on this instance all 8 starts converge to the same
    # (almost surely optimal) tour, while plain 2-opt local optima average ~6.9.
    # With 8 cores, wall-clock is close to the cost of ONE run, not eight.
```

Practical notes for this pattern:

- **Seeds:** never pass `seed + i` by hand; `SeedSequence.spawn` guarantees independent
  streams even across thousands of workers and avoids accidental stream overlap.
- **Windows/macOS spawn:** the worker (`ils_run`) and everything it calls must be
  importable at module top level, and the driver must sit under
  `if __name__ == "__main__":` — otherwise each worker re-executes the script and the
  pool recurses.
- **Reporting:** return per-start results (not just the min) so the run table records the
  distribution across starts; one row per (instance, seed, start) is the tidy format.

## Master-Slave Evaluation, Portfolios, and Cooperative Search

### Master-slave fitness evaluation

The master runs the (unchanged) metaheuristic loop; workers evaluate candidates. Use it
only when one evaluation is expensive — for cheap objectives, vectorized batch evaluation
in one process wins (see fitness-evaluation-and-caching for delta evaluation and
memoization, which often remove the bottleneck entirely). Two details carry the pattern:
push large read-only data into workers **once** via `initializer`, and keep the executor
alive across generations instead of rebuilding it.

```python
"""Master-slave parallel evaluation: workers hold read-only data, master evolves."""
from concurrent.futures import ProcessPoolExecutor

import numpy as np

_DATA: dict[str, np.ndarray] = {}


def init_worker(dist: np.ndarray) -> None:
    """Run once per worker process: stash large read-only arrays in a global."""
    _DATA["dist"] = dist


def eval_one(tour: np.ndarray) -> float:
    """Evaluation stand-in: tour length computed the slow way on purpose.

    Replace the body with the real expensive objective (simulation, ML model,
    embedded LP). A process pool only pays off when one call costs >= ~1 ms.
    """
    dist = _DATA["dist"]
    total = 0.0
    for a, b in zip(tour, np.roll(tour, -1)):
        total += float(dist[a, b])
    return total


def evaluate_parallel(ex: ProcessPoolExecutor, pop: np.ndarray,
                      chunksize: int = 8) -> np.ndarray:
    """Order-preserving parallel batch evaluation of a population."""
    return np.fromiter(ex.map(eval_one, pop, chunksize=chunksize),
                       dtype=float, count=pop.shape[0])


if __name__ == "__main__":
    rng = np.random.default_rng(2)
    pts = rng.random((50, 2))
    dist = np.linalg.norm(pts[:, None, :] - pts[None, :, :], axis=2)
    pop = np.array([rng.permutation(50) for _ in range(64)])
    with ProcessPoolExecutor(max_workers=4, initializer=init_worker,
                             initargs=(dist,)) as ex:
        fit = evaluate_parallel(ex, pop)       # reuse `ex` across generations
    serial = np.array([float(dist[t, np.roll(t, -1)].sum()) for t in pop])
    print(bool(np.allclose(fit, serial)))
    # Expected: True — parallel evaluation must be a pure speed change, never a
    # semantic one. Verify this equivalence in a test before trusting speedups.
```

`chunksize` batches tasks to amortize inter-process round trips: with microsecond tasks
even `chunksize=256` cannot save the pattern (vectorize instead); with multi-second tasks
use `chunksize=1` so slow tasks do not strand fast workers.

joblib wraps the same idea with worker reuse and automatic batching; its `loky` backend
survives interactive sessions and reuses the pool between calls:

```python
"""Master-slave evaluation with joblib: reusable pool, automatic batching."""
import numpy as np
from joblib import Parallel, delayed


def eval_one(x: np.ndarray) -> float:
    """Costly black-box stand-in: a sequential recursion over the vector."""
    state = 0.0
    for v in x:
        state = 0.8 * state + float(np.tanh(v))
    return state


if __name__ == "__main__":
    rng = np.random.default_rng(0)
    pop = rng.normal(size=(200, 64))
    with Parallel(n_jobs=-1, batch_size=16) as pool:   # keep workers warm
        fit = np.asarray(pool(delayed(eval_one)(x) for x in pop))
    print(fit.shape)
    # Expected: (200,) — same values and order as the serial list comprehension
    # [eval_one(x) for x in pop]; speedup appears only for genuinely costly calls.
```

### Algorithm portfolios

A portfolio races entries (algorithm, configuration, seed) on the same instance and keeps
the best. It exploits run-time and run-quality variance instead of fighting it, and it
removes the "which configuration do I trust" decision when tuning budget is short. Entries
finish at different times, so collect with `as_completed`; note that Python cannot kill a
*running* future — enforce budgets inside the workers.

```python
"""Parameter portfolio: race SA configurations on min x^T Q x, x binary."""
from concurrent.futures import ProcessPoolExecutor, as_completed

import numpy as np


def annealer(Q: np.ndarray, seed: np.random.SeedSequence, n_moves: int,
             t0_scale: float, cooling: float) -> tuple[float, np.ndarray]:
    """Single-flip simulated annealing with O(n) move deltas; one portfolio entry."""
    rng = np.random.default_rng(seed)
    n = Q.shape[0]
    diag = np.diag(Q).copy()
    x = rng.integers(0, 2, size=n)
    val = float(x @ Q @ x)
    best_val, best_x = val, x.copy()
    temp = t0_scale * float(np.abs(Q).sum()) / n
    for _ in range(n_moves):
        i = int(rng.integers(n))
        delta = (1 - 2 * x[i]) * (float((Q[i] + Q[:, i]) @ x)
                                  - 2 * diag[i] * x[i] + diag[i])
        if delta < 0 or rng.random() < np.exp(-delta / max(temp, 1e-12)):
            x[i] ^= 1
            val += delta
            if val < best_val:
                best_val, best_x = val, x.copy()
        temp *= cooling
    return best_val, best_x


def run_entry(args: tuple[str, np.ndarray, np.random.SeedSequence, int,
                          float, float]) -> tuple[str, float, np.ndarray]:
    """Portfolio worker: one labeled entry (module-level so it pickles)."""
    label, Q, seed, n_moves, t0_scale, cooling = args
    val, x = annealer(Q, seed, n_moves, t0_scale, cooling)
    return label, val, x


def race(Q: np.ndarray, n_moves: int, seed: int,
         workers: int | None = None) -> list[tuple[str, float]]:
    """Race four SA configurations in parallel; return (label, value) sorted."""
    configs = [("hot-slow", 2.0, 0.9999), ("hot-fast", 2.0, 0.999),
               ("cold-slow", 0.3, 0.9999), ("cold-fast", 0.3, 0.999)]
    seeds = np.random.SeedSequence(seed).spawn(len(configs))
    results: list[tuple[str, float]] = []
    with ProcessPoolExecutor(max_workers=workers) as ex:
        futs = [ex.submit(run_entry, (lab, Q, sd, n_moves, t0, c))
                for (lab, t0, c), sd in zip(configs, seeds)]
        for fut in as_completed(futs):          # report entries as they finish
            label, val, _ = fut.result()
            results.append((label, val))
    return sorted(results, key=lambda r: r[1])


if __name__ == "__main__":
    rng = np.random.default_rng(5)
    Q = rng.normal(size=(60, 60))
    table = race(Q, n_moves=120_000, seed=1)
    print(table[0][0], round(table[0][1], 2))
    # Expected: "hot-slow -155.11" for these seeds (deterministic: the sort
    # removes completion-order effects). WHICH configuration wins varies with
    # seed and instance — exactly the variance a portfolio is built to exploit.
```

### Cooperative search

Cooperation adds communication to multistart: workers periodically deposit their best
solutions into a shared elite pool and restart from (perturbed) pool members. This is the
pool-and-restart form of adaptive memory (Rochat & Taillard 1995); it intensifies around
the globally best material while the perturbation keeps workers from collapsing onto one
basin. The segment-synchronous skeleton avoids shared-memory machinery entirely.

```python
"""Cooperative multistart: independent SA segments plus a shared elite pool."""
from concurrent.futures import ProcessPoolExecutor

import numpy as np


def sa_segment(args: tuple[np.ndarray, np.ndarray, np.random.SeedSequence,
                           int, float]) -> tuple[float, np.ndarray]:
    """One SA segment on min x^T Q x from a given start (module-level, pickles)."""
    Q, x0, seed, n_moves, temp = args
    rng = np.random.default_rng(seed)
    diag = np.diag(Q).copy()
    x = x0.copy()
    val = float(x @ Q @ x)
    best_val, best_x = val, x.copy()
    for _ in range(n_moves):
        i = int(rng.integers(Q.shape[0]))
        delta = (1 - 2 * x[i]) * (float((Q[i] + Q[:, i]) @ x)
                                  - 2 * diag[i] * x[i] + diag[i])
        if delta < 0 or rng.random() < np.exp(-delta / max(temp, 1e-12)):
            x[i] ^= 1
            val += delta
            if val < best_val:
                best_val, best_x = val, x.copy()
        temp *= 0.999
    return best_val, best_x


def cooperative_search(Q: np.ndarray, n_workers: int = 4, n_rounds: int = 5,
                       n_moves: int = 20_000, seed: int = 0
                       ) -> tuple[np.ndarray, float]:
    """Pool-and-restart cooperation: share the incumbent between SA rounds."""
    ss = np.random.SeedSequence(seed)
    rng = np.random.default_rng(ss)
    n = Q.shape[0]
    starts = [rng.integers(0, 2, size=n) for _ in range(n_workers)]
    elite_x, elite_val = None, np.inf
    temp = float(np.abs(Q).sum()) / n
    with ProcessPoolExecutor(max_workers=n_workers) as ex:
        for _ in range(n_rounds):
            seeds = ss.spawn(n_workers)
            jobs = [(Q, starts[w], seeds[w], n_moves, temp)
                    for w in range(n_workers)]
            for val, x in ex.map(sa_segment, jobs):
                if val < elite_val:
                    elite_val, elite_x = val, x.copy()
            flips = rng.random((n_workers, n)) < 0.05    # diversified restarts
            starts = [np.where(flips[w], 1 - elite_x, elite_x)
                      for w in range(n_workers)]
            temp *= 0.5                                  # cool across rounds
    return elite_x, float(elite_val)


if __name__ == "__main__":
    rng = np.random.default_rng(9)
    Q = rng.normal(size=(80, 80))
    x, val = cooperative_search(Q)
    print(round(val, 2))
    # Expected: -294.42 for these seeds (the segment pattern is deterministic).
    # Benchmark requirement: at equal total moves, this should beat or match
    # n_workers fully independent SA runs on most seeds — verify, don't assume.
```

The 5% restart-flip rate is the cooperative analog of ILS kick strength: too small and all
workers intensify the same basin; too large and cooperation degenerates to independent
multistart. Tune it exactly like a perturbation strength.

## Advanced Techniques

### Asynchronous islands and topology effects

Synchronous segments waste time at the barrier when islands run at different speeds.
Asynchronous designs let each island push/pull migrants through queues
(`multiprocessing.Queue`, ray actors, or MPI nonblocking sends) without a global
generation clock. The cost is reproducibility: results depend on OS scheduling, so log
every migrant event if you go asynchronous. Topology is a second lever on the same
diversity dial: takeover time — the generations until one genotype occupies everything —
grows from complete graphs (fastest takeover, least diversity) through random k-regular
to rings (slowest takeover, most diversity); see Cantu-Paz (2000). When migration is rare
and the topology sparse, an island model approximates independent multistart; when
migration is frequent and dense, it approximates one big panmictic population. Place your
design deliberately between those poles.

### Heterogeneous islands

Nothing forces islands to share parameters or even operators: give each island a
different mutation rate, crossover, or acceptance temperature, and migration lets the
configurations rescue each other on instances where one setting stalls. This is a
portfolio folded into an island model and is the cheapest insurance against mis-tuning —
the spread of parameters substitutes for a tuning study when the budget is small.

### Cooperative-search design rules

Cooperation changes the search trajectory; treat the communication policy as part of the
algorithm, not as plumbing (Toulouse, Crainic & Gendreau 1996 showed that careless sharing
can make cooperating searches *worse* than independent ones). Three rules of thumb: share
**rarely** (every segment, not every iteration), share **selectively** (a bounded elite
pool with duplicate elimination, not every improvement), and **diversify on receipt**
(perturb what you adopt, as in the restart-flip above, so receivers do not pile onto the
sender's basin). Bound the pool (10-50 entries) and evict by worst-objective-first with a
distance filter so the memory stays diverse.

### Measuring parallel performance honestly

Report speedup against the **best serial implementation** (the vectorized one), not
against a deliberately slow baseline — this single rule eliminates most inflated claims.
For quality-targeting designs, report time-to-target plots (Aiex, Resende & Ribeiro 2007,
"TTT plots") and quality-vs-wall-clock curves over 10+ seeds rather than a single
speedup number. Super-linear speedup is possible for island models because 8 islands of
50 is a *different algorithm* than one population of 400 (Alba 2002, "Parallel
evolutionary algorithms can achieve super-linear performance") — when you observe it, say
that the search dynamics changed; do not present it as a hardware miracle.

### Scaling beyond one machine

Cross the machine boundary only when a profiled single-machine setup is insufficient.
ray maps cleanly onto this skill's patterns: actors for asynchronous islands holding
their own state, `ray.put` for sharing large instance data once per node, tasks for
master-slave evaluation. mpi4py is the standard on academic clusters (synchronous
segment exchange via `allgather`, asynchronous migration via `isend/irecv`). Keep the
algorithm code identical and swap only the executor layer; if your code is structured
like the examples above (module-level pure workers + a thin driver), the port is
mechanical.

## Practical Challenges

**"Can't pickle local object" or workers crash immediately on Windows.**
Spawn-based start (Windows, macOS default) re-imports the main module in each worker:
every worker function must live at module top level (no lambdas, no closures, no
methods of unpicklable objects), and the driver must be guarded by
`if __name__ == "__main__":`. Without the guard each worker re-runs the script and
recursively spawns pools. On Linux the same code "works" under fork — test on the
deployment OS, not just the development one.

**The parallel version is slower than the serial one.**
Process startup (hundreds of ms), per-task pickling, and result transfer are fixed costs;
they dominate when tasks are tiny. Fix the granularity: batch work with `chunksize` /
`batch_size`, move whole runs or segments (not single evaluations) into tasks, ship large
read-only data once via `initializer` instead of per task, and reuse one executor for the
whole run. If a task still finishes in under a millisecond, the correct fix is rung 1:
vectorize, don't parallelize.

**All workers produce identical results.**
Classic seeding bug: the same seed (or the same global RNG state under fork) reaches
every worker. Spawn child seeds with `np.random.SeedSequence(seed).spawn(k)` and build a
fresh `default_rng` inside each worker from its own child. Never reseed from `time()` in
workers — simultaneous starts collide.

**The machine is oversubscribed and everything crawls.**
numpy's BLAS may use all cores for matrix work; p worker processes times c BLAS threads
equals p*c runnable threads thrashing the caches. In workers, pin BLAS to one thread
(set `OMP_NUM_THREADS=1` / `MKL_NUM_THREADS=1` before numpy import, or use
`threadpoolctl.threadpool_limits(1)` in the initializer) and give the pool one process
per physical core.

**Migration destroyed diversity and all islands converged to the same tour.**
Migration is a selection operator; best-replace-worst on a complete topology with many
migrants causes rapid takeover. Lengthen the interval, cut migrants to 1-2, switch to a
ring, or migrate random individuals instead of the best. Diagnose by tracking per-island
best and inter-island distance: if islands agree early, migration pressure is too high.

**Results are not reproducible run-to-run even with fixed seeds.**
Asynchronous collection (`as_completed`), unordered `imap_unordered`, and
scheduling-dependent cooperation make the outcome depend on timing. For reproducibility,
prefer synchronous segment patterns and order-preserving `ex.map`; if asynchrony is
essential, log every exchanged solution and the round it arrived in, and report that runs
are reproducible only in distribution.

**One slow task strands seven idle cores.**
Run-time variance causes load imbalance at synchronization points. Make tasks smaller
than (budget / workers) so the pool can rebalance, use `chunksize=1` for long
heterogeneous tasks, or enforce per-task wall-clock budgets inside the worker so all
segments end near-simultaneously.

**The speedup claim does not survive review.**
Common causes: baseline was unvectorized Python (inflates speedup), comparison used equal
iterations instead of equal wall-clock (parallel runs got more compute), or a single seed
(noise). Fix with the reporting protocol in Output Format: best serial baseline, equal
wall-clock, 10+ seeds, and time-to-target curves alongside the speedup table.

## Tools & Libraries

| Library | Use for | Note |
|---|---|---|
| `concurrent.futures` | process pools on one machine | `ProcessPoolExecutor` is the cleanest stdlib API; `map(..., chunksize=)` for batching |
| `multiprocessing` | lower-level control: queues, shared memory, start methods | `get_context("spawn")` for cross-platform determinism of behavior |
| joblib | parallel loops with worker reuse and auto-batching | loky backend keeps the pool warm across calls; `batch_size` controls granularity |
| numpy | rung 1: vectorized populations and batch fitness | one vectorized process often beats 8 looping ones; releases the GIL in array ops |
| threadpoolctl | limiting BLAS threads inside workers | prevents p x c thread oversubscription |
| ray | distributed tasks/actors beyond one machine | actors fit asynchronous islands; `ray.put` shares big instance data per node |
| mpi4py | HPC clusters with MPI schedulers | standard for academic clusters; `isend/irecv` for asynchronous migration |
| dask | cluster futures when the results pipeline already uses dask | heavier than needed for plain metaheuristic parallelism |
| `threading` | I/O-bound waiting only (file/network) | the GIL serializes CPU-bound pure-Python work; free-threaded builds are not yet the default |

## Output Format

A complete parallelization deliverable contains:

1. **Bottleneck profile.** One short table: component, % of serial wall-clock, evaluation
   cost per call. This justifies the chosen rung of the ladder.
2. **Architecture decision.** Which of the five architectures, topology and migration (or
   pool/portfolio) policy, and why the cheaper rungs were insufficient.
3. **Code artifacts.** Module-level workers, a thin driver under
   `if __name__ == "__main__":`, a config object holding all parallel parameters, and a
   seed policy based on `SeedSequence.spawn` recorded in the run log.
4. **Correctness evidence.** For master-slave: a test that parallel and serial evaluation
   return identical fitness arrays. For islands/cooperation: an independent-multistart
   baseline at equal core count and equal wall-clock.
5. **Performance report.** One row per worker count, 10+ seeds per row:

   | workers | wall-clock (s) | best | mean +/- sd | speedup | efficiency |
   |---|---|---|---|---|---|
   | 1 (vectorized serial) | 120.0 | 5.62 | 5.71 +/- 0.05 | 1.00 | 1.00 |
   | 4 | 31.5 | 5.59 | 5.66 +/- 0.04 | 3.81 | 0.95 |
   | 8 | 17.2 | 5.58 | 5.63 +/- 0.04 | 6.98 | 0.87 |

   plus quality-vs-time curves (best-so-far over wall-clock, band over seeds) and, for
   quality-targeting studies, time-to-target plots.
6. **Reproducibility statement.** OS and start method, core count, BLAS thread settings,
   library versions, master seed, and whether results are bit-reproducible or
   reproducible in distribution only.

## Questions to Ask

- What fraction of serial runtime is fitness evaluation, and how long is one call?
- Is the implementation already numpy-vectorized, and has it been profiled?
- How many physical cores and how much memory per worker are available — one machine or a cluster?
- Which OS will runs execute on (spawn vs fork changes the code patterns)?
- Is the goal shorter wall-clock at equal quality, or better quality at equal wall-clock?
- Must runs be bit-for-bit reproducible, or is reproducibility in distribution enough?
- Is the objective picklable — free of open solver handles, sockets, or GUI state?
- Is the workload one long run, or many instances x seeds that parallelize trivially at the run level?
- Is the base method population-based or single-solution (this preselects the architecture)?

## Related Skills

- **metaheuristic-design-principles** — when the base algorithm itself (representation,
  operators, constraint handling, stopping) still needs design before it is worth
  parallelizing.
- **genetic-algorithms** — when implementing or tuning the GA that runs inside each island,
  including selection, crossover, and elitism choices.
- **numpy-vectorization-for-optimization** — when one process can still get 10-100x faster
  by removing Python loops; always exhaust this rung before adding processes.
- **fitness-evaluation-and-caching** — when delta evaluation, memoization, or batched
  evaluation can shrink the evaluation cost that motivated parallelism in the first place.
