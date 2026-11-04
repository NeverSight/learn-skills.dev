---
name: decoder-based-representations
description: When the user wants to design an indirect encoding where a decoder maps a simple genotype (random keys, priority vectors, rule choices) to a feasible solution, including serial/parallel schedule-generation schemes and feasibility-enforcing decoders. Also use when the user mentions "decoder," "random keys," "indirect encoding," "schedule generation scheme," "priority-based encoding," "genotype-phenotype mapping," or when operators are easier to apply to a vector than to the constrained solution. For direct representation choice, see solution-encodings; for the evolutionary engine around a decoder, see biased-random-key-genetic-algorithm.
---

# Decoder-Based Representations

You are an expert in indirect (decoder-based) representations for combinatorial optimization. This skill is the catalog of decoder families — random-key decoders (sort, interval, threshold), priority- and rule-based decoders, serial and parallel schedule-generation schemes (SGS), and feasibility-enforcing constructive decoders — with the design criteria (coverage, bias, locality, redundancy, decode time) that decide between them. Use the framework below to pick a decoder family for a given problem, implement it correctly in numpy, and diagnose the failure modes that are specific to genotype-phenotype mappings.

## Initial Assessment

Before designing or reviewing a decoder, establish the following:

- **Phenotype structure.** What object must the decoder output: a permutation, a subset, an assignment vector, a start-time schedule, a packing? The phenotype type narrows the decoder family immediately (sort decoder for sequences, interval decoder for categorical assignments, SGS for resource-constrained schedules).
- **Constraint families and their placement.** List every constraint and decide, per family, whether the decoder absorbs it (constructs only feasible solutions), a repair step fixes it, or a penalty prices it. Decoders earn their keep by absorbing the constraints that crossover and mutation would otherwise break; see **constraint-handling-techniques** for the penalty/repair alternatives.
- **Existing constructive heuristic.** If a greedy or dispatching heuristic already exists (NEH, LPT, FFD, earliest-due-date), the cheapest strong decoder is usually that heuristic with its fixed priority replaced by genotype-supplied priorities. This also gives a free warm start: encode the heuristic's own priorities as keys.
- **Search engine that will drive the genotype.** BRKGA and GAs with uniform crossover want random keys in $[0,1)^n$; integer-vector genotypes (rule indices, category ids) want integer mutation/crossover; PSO, DE, ES, and CMA-ES want a continuous box, which random keys provide. Choose the genotype the engine handles natively so no operator needs rewriting.
- **Evaluation budget and decode cost.** Decoding dominates runtime in decoder-based metaheuristics: total cost is roughly `population × generations × decode_cost`. Estimate one decode (sort decoders: O(n log n); SGS: roughly O(n² K)) and check the budget before committing. Plan batch/vectorized decoding from the start if the population is large.
- **Coverage requirement.** Must the decoder's image provably contain an optimal solution? Serial SGS guarantees this for regular objectives (it generates active schedules); parallel SGS does not. If you will claim convergence-to-optimum or run long high-budget searches, coverage matters; for fast good-enough heuristics it may not.
- **Locality requirement.** Will the engine rely on small steps (PSO velocities, Gaussian mutation, BRKGA biased crossover)? Then the decoder should map small key changes to small phenotype changes. Heavily repairing or strongly greedy decoders can destroy this property.
- **Determinism and tie-breaking.** The same genotype must always decode to the same phenotype: fix tie-breaking (stable sorts, lowest-index-first), avoid internal randomness, avoid iteration over unordered containers. Determinism is a precondition for caching and reproducibility.
- **Instance scale.** For SGS decoders, the time horizon and resource count set the memory and per-decode cost; for sort decoders only n matters. Check the largest instance, not the test instance.
- **Validation plan.** An independent feasibility checker (separate code path from the decoder) must verify every reported solution; on small instances, compare decoder-reachable optima against an exact solver.
- **Reproducibility.** Seed the genotype sampler (`np.random.default_rng(seed)`) and keep the decoder seed-free. Report results over multiple seeds.

## Decoder Anatomy and Design Criteria

A decoder replaces direct search over the feasible set $S$ with search over a simple genotype space $G$:

$$ \min_{g \in G} \; f(D(g)) \qquad \text{instead of} \qquad \min_{s \in S} f(s), \qquad D : G \to S . $$

The search engine only ever sees $G$ (a hypercube, an integer lattice, a permutation set); the decoder $D$ carries all problem knowledge. The design criteria, following Rothlauf (2006, "Representations for Genetic and Evolutionary Algorithms"):

1. **Feasibility.** $D(g) \in S$ for every $g \in G$. This is the defining advantage: arbitrary crossover and mutation on $G$ can never produce an infeasible phenotype.
2. **Coverage.** The image $D(G)$ should contain at least one optimal solution — or, weaker, solutions within the quality target. A decoder that is too greedy shrinks the image past the optimum and no amount of search recovers it.
3. **Bias.** Uniform sampling of $G$ induces a distribution over $S$. Some bias toward good solutions is useful (it is a prior); uncontrolled bias concentrates mass on mediocre phenotypes and starves the rest.
4. **Locality.** Small genotype distances should map to small phenotype distances. Low locality turns guided search into random search: offspring resemble their parents in $G$ but not in $S$.
5. **Redundancy.** $D$ is many-to-one; for a sort decoder, only the ordering of keys matters, so each permutation has an uncountable preimage. Redundancy itself is harmless, but it creates plateaus in $G$ and means diversity must be measured on phenotypes or fitness values, never on genotype distance.
6. **Decode time.** The decoder runs once per evaluation. Its complexity, not the engine's, sets the runtime.
7. **Determinism.** $D$ must be a function. Fixed tie-breaking is part of the decoder specification.

### Decoder family catalog

| Family | Genotype | Phenotype | Feasibility | Decode cost | Typical problems |
|---|---|---|---|---|---|
| Sort decoder | keys $[0,1)^n$ | permutation | always | $O(n \log n)$ | flow shop, single machine, TSP-like orders |
| Interval (allocation) decoder | keys $[0,1)^n$ | categorical vector | per-item yes; coupling constraints need repair | $O(n)$ | machine assignment, mode selection, clustering |
| Threshold decoder | keys $[0,1)^n$ | binary vector | only with repair/completion | $O(n)$ + repair | set covering, knapsack, facility selection |
| Greedy-priority decoder | keys as priorities | any constructive solution | always (construction respects constraints) | cost of the greedy | parallel machines, bin packing, graph coloring |
| Rule-selection decoder | integer vector of rule ids | dispatching trajectory | always | cost of the simulation | dynamic scheduling, hyper-heuristic style search |
| Serial SGS | activity priorities | start-time schedule | always; image = active schedules | $O(n^2 K)$ | RCPSP, project scheduling, job shop variants |
| Parallel SGS | activity priorities | start-time schedule | always; image = non-delayed schedules | $O(n^2 K)$ | RCPSP when speed beats coverage |
| Multi-segment chromosome | concatenated key blocks | layered decision (assign then sequence) | inherits from each stage | sum of stages | assign-and-sequence scheduling, location-routing |

### Property comparison across the catalog

| Family | Coverage of optima | Bias under uniform keys | Locality | Redundancy |
|---|---|---|---|---|
| Sort decoder | full (all permutations) | uniform over permutations | good (rank changes are gradual) | high (only key order matters) |
| Interval decoder | full (all assignments) | uniform over categories | good | moderate (within-interval changes are silent) |
| Threshold + repair | full if repair can reach all feasible | depends on repair; often strong | poor near the repair boundary | moderate |
| Greedy-priority | usually wide, rarely provable | strong toward greedy-like solutions | moderate | high |
| Serial SGS | contains an optimum (regular objectives) | toward active, left-shifted schedules | moderate | high |
| Parallel SGS | may exclude every optimum | toward non-delayed schedules | moderate | high |
| Rule-selection | only rule-reachable trajectories | strong (rules are few) | moderate | very high |

### Genotype-engine compatibility

| Genotype | Engines that drive it natively | Note |
|---|---|---|
| Random keys $[0,1)^n$ | BRKGA, GA with uniform/blend crossover, PSO, DE, ES, CMA-ES | one genotype, many engines — the main reason random keys are popular (Bean, 1994, "Genetic algorithms and random keys for sequencing and optimization") |
| Integer vector | GA with integer mutation, simulated annealing on component moves | also reachable from keys via an interval decode |
| Permutation + decoder | GA with OX/PMX, iterated local search on swaps | use when order itself is the genotype but the phenotype needs construction (sequence-then-pack) |

**Decision guidance.**

- Use a **sort decoder** when the phenotype is a pure sequence and relative order carries the fitness signal (flow shop). Avoid it when adjacency carries the signal (pure TSP): order-preserving inheritance does not preserve edges, so add local search or use permutation operators directly (see **solution-encodings**).
- Use an **interval decoder** for independent categorical choices; add repair only for coupling constraints (capacities across items).
- Use a **greedy-priority or SGS decoder** when constraints are complex enough that direct operators would almost always break them — resource-constrained scheduling is the canonical case (Hartmann, 1998, "A competitive genetic algorithm for resource-constrained project scheduling").
- Use **rule-selection** when good dispatching rules exist and the search should mix them per decision point rather than discover sequences from scratch.
- Prefer the **weakest decoder whose image still contains near-optimal solutions**: weaker decoders preserve locality and coverage; stronger decoders save evaluations but bias and shrink the image.

## Random-Key Decoders

Random keys (Bean, 1994) put the genotype in $[0,1)^n$ so every continuous or position-wise operator applies unchanged. The two core mappings are sorting (keys to a permutation) and interval splitting (keys to categories).

### Sort decoder — worked example: permutation flow shop

When to use: the phenotype is a sequence and any sequence is feasible. Fits flow shop, single-machine problems, and any sequence-driven constructive pipeline. Complexity: $O(n \log n)$ per chromosome, fully batchable. This is the standard BRKGA decoder for flow shop; the engine side is in **biased-random-key-genetic-algorithm**, and continuous engines such as PSO and DE drive the same keys (see **particle-swarm-optimization**).

```python
"""Sort decoder: random keys -> permutation, applied to permutation flow shop."""
import numpy as np


def sort_decode(keys: np.ndarray) -> np.ndarray:
    """Decode a key matrix (P, n) into P permutations: stable argsort per row.

    Stable sort fixes tie-breaking (lowest index first), so decoding is
    deterministic. Cost: O(P n log n).
    """
    return np.argsort(keys, axis=1, kind="stable")


def flowshop_makespan(perms: np.ndarray, proc: np.ndarray) -> np.ndarray:
    """Vectorized makespan of P job sequences on an (n_jobs, n_machines) instance.

    Recurrence C[j,k] = max(C[j-1,k], C[j,k-1]) + p[j,k], evaluated for all P
    sequences at once. Cost: O(P n m).
    """
    n_machines = proc.shape[1]
    completion = np.zeros((perms.shape[0], n_machines))
    for pos in range(perms.shape[1]):
        p_job = proc[perms[:, pos], :]                    # (P, m)
        for k in range(n_machines):
            prev = completion[:, k - 1] if k > 0 else 0.0
            completion[:, k] = np.maximum(completion[:, k], prev) + p_job[:, k]
    return completion[:, -1]


rng = np.random.default_rng(0)
proc = rng.integers(1, 20, size=(8, 4)).astype(float)     # 8 jobs, 4 machines
keys = rng.random((64, 8))                                # population of 64
perms = sort_decode(keys)
cmax = flowshop_makespan(perms, proc)
best = int(np.argmin(cmax))
print(perms[best].tolist(), float(cmax[best]))
# Expected: best sequence [2, 3, 5, 7, 1, 4, 6, 0] with makespan 122.0 —
# 64 uniform key vectors already sample 64 (likely distinct) permutations.
```

The redundancy is explicit here: scaling all keys by 0.5 changes nothing. Measure population diversity on `perms` or `cmax`, never on `keys`.

### Interval (allocation) decoder

When to use: one independent categorical decision per item — machine assignment, execution mode, color class. Equal-width intervals give every category the same prior probability; unequal widths inject a prior (give a larger interval to a cheaper machine). Complexity: $O(n)$ per chromosome. Fits BRKGA, PSO, DE on keys; coupling constraints (machine capacities) need a repair pass or a greedy-priority decoder instead.

```python
"""Interval (allocation) decoder: each key selects one of c categories."""
import numpy as np


def interval_decode(keys: np.ndarray, n_categories: int) -> np.ndarray:
    """Map keys in [0,1) to categories: category = floor(key * c).

    The min() guards against a key exactly equal to 1.0 (possible after
    clipping by a continuous engine). Cost: O(P n).
    """
    return np.minimum((keys * n_categories).astype(np.int64), n_categories - 1)


rng = np.random.default_rng(1)
proc = rng.integers(2, 12, size=10).astype(float)         # 10 jobs
n_machines = 3
keys = rng.random((32, 10))
assign = interval_decode(keys, n_machines)                # (32, 10) machine ids
onehot = assign[:, :, None] == np.arange(n_machines)      # (32, 10, 3)
loads = (onehot * proc[None, :, None]).sum(axis=1)        # (32, 3)
cmax = loads.max(axis=1)
print(float(cmax.min()))
# Expected: best makespan 25.0 over 32 random assignments
# (total work 68.0, so the lower bound ceil(68/3) = 23 is approached).
```

Multi-segment chromosomes concatenate blocks: keys `[0:n]` assign machines via interval decode, keys `[n:2n]` sequence each machine via sort decode. Decode the blocks in stage order and document the block layout next to the decoder.

## Priority-Rule and Rule-Selection Decoders

These decoders feed the genotype into a constructive procedure: the genotype supplies priorities (which item next) or rules (how to choose the next item), and the construction enforces feasibility step by step.

### Greedy-priority decoder: list scheduling on identical machines

When to use: a list-scheduling or greedy heuristic exists and its input order is the lever. The decoder below visits jobs in key order and assigns each to the least-loaded machine — every genotype yields a feasible assignment. Complexity: $O(n m)$ per chromosome here, vectorized across the whole population. Fits parallel-machine scheduling, bin packing, graph coloring (visit order for a greedy colorer).

```python
"""Greedy-priority decoder: keys order the jobs, list scheduling assigns machines."""
import numpy as np


def list_schedule_decode(
    keys: np.ndarray, proc: np.ndarray, n_machines: int
) -> tuple[np.ndarray, np.ndarray]:
    """Decode keys (P, n) into machine assignments (P, n) by list scheduling.

    Jobs are visited in increasing key order; each goes to the currently
    least-loaded machine. Always feasible. Vectorized over the population:
    O(P n m) total, or O(P n log m) with per-row heaps.
    """
    P, n = keys.shape
    order = np.argsort(keys, axis=1, kind="stable")
    loads = np.zeros((P, n_machines))
    assign = np.empty((P, n), dtype=np.int64)
    rows = np.arange(P)
    for pos in range(n):
        job = order[:, pos]
        machine = loads.argmin(axis=1)
        assign[rows, job] = machine
        loads[rows, machine] += proc[job]
    return assign, loads.max(axis=1)


rng = np.random.default_rng(2)
proc = rng.integers(1, 30, size=12).astype(float)
keys = rng.random((50, 12))
assign, cmax = list_schedule_decode(keys, proc, n_machines=3)
lpt_keys = (np.argsort(np.argsort(-proc)).astype(float) / 12.0)[None, :]
_, lpt_cmax = list_schedule_decode(lpt_keys, proc, n_machines=3)
print(float(cmax.min()), float(lpt_cmax[0]))
# Expected: best random-key makespan 59.0 vs LPT warm start 60.0 — the rank
# encoding reproduces LPT exactly and random keys already explore beyond it
# (total work 174.0 gives the lower bound 58).
```

The `lpt_keys` line is the standard warm-start construction: encode a known heuristic order as ranks divided by n, and the decoder reproduces that heuristic exactly. Inject such rows into the initial population of any key-driven engine.

### Rule-selection decoder

When to use: strong dispatching rules exist (SPT, EDD, slack-based) and the open question is which rule to apply at which decision point. The genotype is an integer vector of rule indices — or random keys passed through `interval_decode` so a continuous engine can drive it. The image is the set of trajectories reachable by stagewise rule mixtures; it always contains every pure rule, so the decoder never does worse than the best single rule given enough search. Complexity: cost of simulating the dispatch, here $O(n^2)$.

```python
"""Rule-selection decoder: the genotype picks a dispatching rule per decision."""
import numpy as np

RULES = ("SPT", "LPT", "EDD", "MST")


def rule_decode(rule_idx: np.ndarray, proc: np.ndarray, due: np.ndarray) -> np.ndarray:
    """Build one sequence; decision k applies RULES[rule_idx[k]] to the
    remaining jobs (single machine). Ties resolve to the lowest job index via
    argmin/argmax. Cost: O(n^2).
    """
    n = proc.size
    remaining = list(range(n))
    seq = np.empty(n, dtype=np.int64)
    t = 0.0
    for k in range(n):
        cand = np.array(remaining)
        rule = RULES[int(rule_idx[k]) % len(RULES)]
        if rule == "SPT":
            pick = cand[np.argmin(proc[cand])]
        elif rule == "LPT":
            pick = cand[np.argmax(proc[cand])]
        elif rule == "EDD":
            pick = cand[np.argmin(due[cand])]
        else:                                  # MST: minimum slack due - t - p
            pick = cand[np.argmin(due[cand] - t - proc[cand])]
        seq[k] = pick
        t += proc[pick]
        remaining.remove(int(pick))
    return seq


def total_tardiness(seq: np.ndarray, proc: np.ndarray, due: np.ndarray) -> float:
    """Sum of max(0, completion - due) along the sequence."""
    completion = np.cumsum(proc[seq])
    return float(np.maximum(completion - due[seq], 0.0).sum())


rng = np.random.default_rng(5)
proc = rng.integers(1, 10, size=8).astype(float)
due = rng.integers(5, 40, size=8).astype(float)
genotypes = rng.integers(0, 4, size=(60, 8))
tard = [total_tardiness(rule_decode(g, proc, due), proc, due) for g in genotypes]
edd = total_tardiness(rule_decode(np.full(8, 2), proc, due), proc, due)
print(min(tard), edd)
# Expected: best mixed-rule tardiness 52.0 < pure-EDD tardiness 55.0; EDD is
# in the image as the all-2 genotype, so the decoder can only improve on it.
```

The same pattern extends to job-shop dispatching: run a Giffler-Thompson construction and let the genotype break ties among the conflict set. Machine-level models and neighborhoods for that problem are in **job-shop-scheduling**.

## Schedule-Generation Schemes

The SGS is the decoder workhorse of resource-constrained project scheduling (RCPSP). Notation: activities $i = 1..n$ with durations $d_i \ge 1$, precedence relation $P$ ($p \to i$ means $i$ starts after $p$ finishes), renewable resources $k = 1..K$ with per-period capacities $R_k$, constant per-period demands $r_{ik}$. A schedule assigns start times $s_i$; the regular objective here is makespan $\max_i (s_i + d_i)$.

Schedule classes order the decoder images (Sprecher, Kolisch & Drexl, 1995, "Semi-active, active, and non-delay schedules for the resource-constrained project scheduling problem"):

| Class | Definition | Contains an optimum (regular objective)? | Generated by |
|---|---|---|---|
| Semi-active | no activity can start earlier with the same sequence | yes | any left-shift pass |
| Active | no activity can start earlier without delaying another | yes | serial SGS over all priority vectors |
| Non-delayed | no resource is left idle while some activity could start | not guaranteed | parallel SGS |

Non-delayed $\subseteq$ active $\subseteq$ semi-active. The serial scheme is the safe decoder; the parallel scheme is a stronger greedy whose image can exclude every optimal schedule (Kolisch, 1996, "Serial and parallel resource-constrained project scheduling methods revisited: theory and computation").

### Serial SGS — worked example: RCPSP-style decoder

When to use: default SGS decoder; coverage guarantee plus simple implementation. The genotype is one priority key per activity; random keys, GA-evolved keys, or PSO particles all work. Complexity below: $O(n^2 + nTK)$ with horizon $T = \sum_i d_i$; event-list implementations reach $O(n^2 K)$.

```python
"""sgs_decoders.py — serial schedule-generation scheme for RCPSP-style problems.

Conventions: activities 0..n-1; preds[i] lists predecessors of i; durations
are >= 1; demand[i, k] is the per-period demand of activity i on renewable
resource k; capacity[k] is the per-period limit; every activity fits capacity
on its own.
"""
import numpy as np


def serial_sgs(
    priorities: np.ndarray,
    durations: np.ndarray,
    preds: list[list[int]],
    capacity: np.ndarray,
    demand: np.ndarray,
) -> tuple[np.ndarray, int]:
    """Serial SGS: n stages; each stage starts the highest-priority eligible
    activity at its earliest precedence- and resource-feasible time.

    Returns (start_times, makespan). The image over all priority vectors is
    the set of active schedules, which contains an optimal schedule for any
    regular objective.
    """
    n = durations.size
    horizon = int(durations.sum()) + 1
    usage = np.zeros((horizon, capacity.size))
    start = np.zeros(n, dtype=np.int64)
    finish = np.zeros(n, dtype=np.int64)
    scheduled = np.zeros(n, dtype=bool)
    for _ in range(n):
        eligible = [
            i for i in range(n)
            if not scheduled[i] and all(scheduled[p] for p in preds[i])
        ]
        j = max(eligible, key=lambda i: priorities[i])
        t = max((int(finish[p]) for p in preds[j]), default=0)
        d = int(durations[j])
        while np.any(usage[t:t + d] + demand[j] > capacity):
            t += 1
        start[j], finish[j] = t, t + d
        usage[t:t + d] += demand[j]
        scheduled[j] = True
    return start, int(finish.max())


def validate_schedule(
    start: np.ndarray,
    durations: np.ndarray,
    preds: list[list[int]],
    capacity: np.ndarray,
    demand: np.ndarray,
) -> None:
    """Independent feasibility check: precedence and per-period resource load."""
    finish = start + durations
    for i, plist in enumerate(preds):
        for p in plist:
            assert finish[p] <= start[i], f"precedence {p}->{i} violated"
    for t in range(int(finish.max())):
        active = (start <= t) & (t < finish)
        assert np.all(demand[active].sum(axis=0) <= capacity), f"overload at t={t}"


if __name__ == "__main__":
    durations = np.array([3, 4, 2, 2, 4, 3, 2, 1])
    preds = [[], [], [0], [0, 1], [1], [2, 3], [4], [5, 6]]
    capacity = np.array([3, 3])
    demand = np.array(
        [[2, 0], [1, 1], [2, 1], [0, 2], [1, 1], [2, 2], [1, 0], [2, 1]]
    )
    rng = np.random.default_rng(7)
    starts, mks = serial_sgs(rng.random(8), durations, preds, capacity, demand)
    validate_schedule(starts, durations, preds, capacity, demand)
    print(starts.tolist(), mks)
    # Expected: starts [0, 0, 3, 5, 4, 7, 8, 10] with makespan 11; the
    # validator passes silently (precedence and both capacities respected).
```

### Parallel SGS and the coverage gap

When to use: speed and a strong greedy bias toward packed schedules matter more than reachability of the optimum — typical for very large instances or as one decoder inside a portfolio. The demo below is a minimal separating instance: a "timer" chain forces the optimum to leave the resource idle at $t = 0$, which non-delayed schedules forbid by definition. Parallel SGS therefore decodes *every* priority vector to a suboptimal schedule, while serial SGS reaches the optimum.

```python
"""Parallel SGS (append to sgs_decoders.py): time-driven decoding."""
import numpy as np

from sgs_decoders import serial_sgs, validate_schedule


def parallel_sgs(
    priorities: np.ndarray,
    durations: np.ndarray,
    preds: list[list[int]],
    capacity: np.ndarray,
    demand: np.ndarray,
) -> tuple[np.ndarray, int]:
    """Parallel SGS: sweep time over finish events; at each decision time start
    eligible activities in priority order while resources allow.

    The image is the set of non-delayed schedules, which may exclude every
    optimal schedule (Kolisch, 1996). Cost: O(n^2 (n + K)) worst case.
    """
    n = durations.size
    start = np.full(n, -1, dtype=np.int64)
    finish = np.zeros(n, dtype=np.int64)
    done = np.zeros(n, dtype=bool)
    running: list[int] = []
    avail = capacity.astype(float).copy()
    t, n_started = 0, 0
    while n_started < n:
        for i in [i for i in running if finish[i] <= t]:
            done[i] = True
            avail += demand[i]
        running = [i for i in running if finish[i] > t]
        while True:
            ready = [
                i for i in range(n)
                if start[i] < 0
                and all(done[p] for p in preds[i])
                and np.all(demand[i] <= avail + 1e-9)
            ]
            if not ready:
                break
            j = max(ready, key=lambda i: priorities[i])
            start[j], finish[j] = t, t + int(durations[j])
            avail -= demand[j]
            running.append(j)
            n_started += 1
        if n_started < n:
            t = min(int(finish[i]) for i in running)
    return start, int(finish.max())


if __name__ == "__main__":
    # Separating instance: u (timer) -> v -> z chain, w independent; one
    # unit-capacity resource used by v and w only. Optimum: keep the resource
    # idle during u, run v at t=1, then z and w in parallel -> makespan 7.
    durations = np.array([1, 1, 5, 5])                 # u, v, z, w
    preds = [[], [0], [1], []]
    capacity = np.array([1])
    demand = np.array([[0], [1], [0], [1]])
    good = np.array([0.9, 0.8, 0.7, 0.1])              # prefer the chain
    s_start, s_mks = serial_sgs(good, durations, preds, capacity, demand)
    p_start, p_mks = parallel_sgs(good, durations, preds, capacity, demand)
    validate_schedule(s_start, durations, preds, capacity, demand)
    validate_schedule(p_start, durations, preds, capacity, demand)
    print(s_mks, p_mks)
    # Expected: 7 11 — parallel SGS must start w at t=0 (non-delayed rule),
    # which blocks v until t=5 and pushes the chain to finish at 11.
```

The practical reading: pick the serial scheme unless profiling proves it too slow, and if you do use the parallel scheme, verify on small instances (exact solver or enumeration) how much the coverage gap costs on your instance class.

## Feasibility-Enforcing Decoders

These decoders absorb the binding constraints into construction, so every genotype decodes to a feasible solution and the engine needs no penalties or repair operators. Compare this against penalty and repair strategies in **constraint-handling-techniques** before committing: feasibility-enforcing decoders trade a smaller, biased image for a clean search space.

### Greedy-fill knapsack decoder

When to use: budget/capacity constraints where a greedy fill is sensible. Visit items in key order; take an item only if it still fits. Always feasible, vectorized across the population. The image contains every maximal feasible set (no item can be added), which always includes an optimal solution of the 0-1 knapsack. Complexity: $O(Pn)$ after the $O(Pn\log n)$ argsort.

```python
"""Feasibility-enforcing knapsack decoder: greedy fill in key order."""
import numpy as np


def knapsack_decode(
    keys: np.ndarray, values: np.ndarray, weights: np.ndarray, capacity: float
) -> tuple[np.ndarray, np.ndarray]:
    """Decode keys (P, n) to feasible selections: visit items by descending
    key, take each item that still fits. Returns (selection matrix, values).
    Vectorized across the population: the loop is over positions, not rows.
    """
    P, n = keys.shape
    order = np.argsort(-keys, axis=1, kind="stable")
    selected = np.zeros((P, n), dtype=bool)
    load = np.zeros(P)
    rows = np.arange(P)
    for pos in range(n):
        item = order[:, pos]
        fits = load + weights[item] <= capacity
        selected[rows, item] = fits
        load += weights[item] * fits
    return selected, selected @ values


rng = np.random.default_rng(3)
values = rng.integers(10, 100, size=15).astype(float)
weights = rng.integers(5, 40, size=15).astype(float)
capacity = 120.0
sel, totals = knapsack_decode(rng.random((40, 15)), values, weights, capacity)
assert np.all(sel @ weights <= capacity)
print(float(totals.max()))
# Expected: best value 450.0 across 40 chromosomes; the assert confirms every
# decoded selection respects the capacity without any repair step.
```

### Sequence-then-first-fit bin-packing decoder

When to use: packing-type constraints where a placement rule (first fit, best fit) guarantees feasibility and the genotype controls the order items arrive. The FFD heuristic is in the image by construction (encode decreasing-size ranks as keys), so search starts at least as good as FFD. Complexity: $O(n \cdot \text{bins})$ per chromosome; this construction is inherently sequential, so vectorize over chromosomes with care or batch in compiled code.

```python
"""Sequence-then-first-fit decoder for bin packing: feasible by construction."""
import numpy as np


def first_fit_decode(
    keys: np.ndarray, sizes: np.ndarray, cap: float
) -> tuple[list[list[int]], int]:
    """Decode one key vector: visit items in increasing key order, place each
    in the first bin with room, opening a new bin when none fits.
    Returns (bin contents, number of bins).
    """
    loads: list[float] = []
    content: list[list[int]] = []
    for item in np.argsort(keys, kind="stable"):
        for b, load in enumerate(loads):
            if load + sizes[item] <= cap + 1e-9:
                loads[b] += float(sizes[item])
                content[b].append(int(item))
                break
        else:
            loads.append(float(sizes[item]))
            content.append([int(item)])
    return content, len(loads)


rng = np.random.default_rng(4)
sizes = rng.uniform(0.2, 0.7, size=20)
ffd_keys = np.argsort(np.argsort(-sizes)).astype(float) / sizes.size
bins_ffd = first_fit_decode(ffd_keys, sizes, cap=1.0)[1]
bins_rnd = min(first_fit_decode(rng.random(20), sizes, cap=1.0)[1] for _ in range(30))
print(bins_ffd, bins_rnd)
# Expected: 12 12 — FFD-as-keys opens 12 bins; the best of 30 random key
# orders matches it here (sum of sizes 10.26 gives lower bound 11 bins).
```

When a feasibility-enforcing construction does not exist (general coupling constraints), fall back to threshold decoding plus a repair/completion pass — for example, decode `key >= 0.5` to a tentative cover and greedily add the cheapest columns until all rows are covered. The repair design rules live in **constraint-handling-techniques**.

## Advanced Techniques

### Lamarckian write-back and warm starting

When local search improves a decoded phenotype, the genotype still encodes the old solution; the improvement is lost at the next crossover unless it is written back. For sort decoders the write-back is exact and $O(n)$:

```python
"""Lamarckian write-back: re-encode an improved phenotype into key space."""
import numpy as np


def encode_permutation(perm: np.ndarray) -> np.ndarray:
    """Return keys in (0,1) whose stable argsort reproduces `perm` exactly.

    Sequence position p gets key (p + 0.5)/n, written to gene perm[p].
    Round trip: argsort(encode(perm), kind="stable") == perm. Cost: O(n).
    """
    n = perm.size
    keys = np.empty(n)
    keys[perm] = (np.arange(n) + 0.5) / n
    return keys


perm = np.array([3, 0, 4, 1, 2])
keys = encode_permutation(perm)
print(np.array_equal(np.argsort(keys, kind="stable"), perm))
# Expected: True — the improved sequence survives decoding unchanged, so a
# local-search gain is inherited by offspring (Lamarckian learning).
```

The same construction warm-starts any key-driven engine from a constructive heuristic (LPT, FFD, NEH): encode the heuristic's order and inject it into the initial population. For decoders without an exact inverse (greedy-priority, SGS), write back the priorities implied by the improved solution's start order — approximate, but it keeps the gain reachable.

### Forward-backward justification for SGS

Justification (Valls, Ballestín & Quintanilla, 2005, "Justification and RCPSP: a technique that pays") right-shifts all activities against the deadline in decreasing finish-time order, then left-shifts back. Each pass costs one extra decode and typically tightens makespan by several percent on PSPLIB-style instances. Apply it inside the decoder (decode, justify, return the improved schedule) and write the resulting activity order back into the keys so the improvement is heritable.

### Decoder strength: time versus coverage

Decoder design moves along a spectrum. At the weak end, a sort decoder spends $O(n \log n)$ and covers the entire permutation space — all problem knowledge must come from search. At the strong end, a decoder embedding justification or local search spends far more per decode, biases hard toward good phenotypes, and shrinks the image. Two working rules: (1) choose the *cheapest* decoder whose image still contains near-optimal solutions, then buy quality with more evaluations, not more decoder; (2) when you strengthen a decoder, re-verify coverage empirically — solve small instances exactly and check that the decoder can still express the optima. The parallel-SGS demo above is the canonical warning: a stronger greedy silently removed the optimum from the image.

### Measuring bias, redundancy, and locality

Treat the decoder as a measurable object before trusting it. Sample uniform genotypes, decode, and inspect the phenotype distribution; the script below quantifies the parallel-SGS coverage gap and confirms the sort decoder's uniformity.

```python
"""Measure decoder bias: sample uniform keys, compare phenotype distributions."""
import numpy as np

from sgs_decoders import parallel_sgs, serial_sgs

durations = np.array([1, 1, 5, 5])
preds = [[], [0], [1], []]
capacity = np.array([1])
demand = np.array([[0], [1], [0], [1]])

rng = np.random.default_rng(11)
samples = rng.random((500, 4))
serial_mks = np.array(
    [serial_sgs(k, durations, preds, capacity, demand)[1] for k in samples]
)
parallel_mks = np.array(
    [parallel_sgs(k, durations, preds, capacity, demand)[1] for k in samples]
)
print(np.unique(serial_mks).tolist(), np.unique(parallel_mks).tolist())
print(round(float((serial_mks == 7).mean()), 3))

perms = np.argsort(rng.random((5000, 4)), axis=1, kind="stable")
_, counts = np.unique(perms, axis=0, return_counts=True)
print(len(counts), int(counts.min()), int(counts.max()))
# Expected: serial makespans [7, 11] with ~1/3 of the mass on the optimum 7
# (prints 0.334; the optimum needs activity 3 to carry the lowest priority);
# parallel makespans [11] only. The sort decoder hits all 24 permutations of
# n=4 with counts near the uniform 5000/24 ~ 208 — unbiased coverage.
```

For locality, correlate genotype perturbation size with phenotype distance (e.g., Kendall tau between decoded permutations before and after a Gaussian key perturbation). A flat or noisy relationship predicts that small-step engines will behave like random search on this decoder.

### Driving decoders with continuous optimizers

Random keys make PSO, DE, ES, and CMA-ES applicable to combinatorial problems with zero operator changes — the engine optimizes in $[0,1)^n$ and the decoder does the rest (see **particle-swarm-optimization** for the engine side). Two integration details matter. First, bound handling: clipping pushes many keys to exactly 0.0 or 1.0, creating ties that a stable argsort resolves toward low indices — a hidden bias; prefer reflection or wrapping (`keys % 1.0`), or rank-rescale each genotype after the update. Second, the redundancy plateau: convergence metrics in key space (velocity norms, step sizes) keep shrinking long after the phenotype has frozen, so base stopping criteria on phenotype or fitness stagnation instead.

## Practical Challenges

**Phenotype diversity collapses while key diversity looks healthy.** The decoder is many-to-one, so genotype distance overstates real diversity. Measure diversity on decoded solutions (distinct phenotype hashes, fitness spread, pairwise phenotype distance). If phenotypes froze, restart or inject mutants — key-space metrics will not warn you in time.

**Local search gains vanish after one generation.** The improved phenotype was never written back into the genotype, so crossover recombines stale keys. Apply Lamarckian write-back (exact for sort decoders, priority-based approximation for constructive decoders), or accept slower Baldwinian convergence deliberately and document the choice.

**A continuous engine drives keys out of $[0,1)$.** Clipping creates mass points at the bounds and tie clusters that bias the sort decoder toward low indices. Use wrapping or reflection, or re-rank keys after each update; for interval decoders, keep the final `min(category, c-1)` guard so a key of exactly 1.0 cannot index out of range.

**Decoding consumes nearly all runtime.** Profile first; then vectorize across the population (the knapsack and list-scheduling decoders above show the position-loop pattern), cache fitness for elite genotypes that survive unchanged, and hash *phenotypes* (not genotypes) for memoization since many genotypes share one phenotype.

**Search barely beats random restarts.** Classic low-locality symptom: offspring decode to phenotypes unrelated to their parents. Measure the perturbation-distance correlation; if it is flat, weaken the decoder (less repair, less internal greediness) or switch genotype so inheritance acts on the decisions that matter.

**The decoder can never produce the known optimum.** Coverage failure. Check on small instances by enumerating or solving exactly, then comparing against the best decodable solution over many sampled genotypes. Typical causes: parallel SGS (non-delayed image), over-aggressive repair, greedy steps with no genotype influence. Fix by weakening the greedy or adding a serial/weak variant to a decoder portfolio.

**Same genotype, different phenotypes across runs.** Hidden nondeterminism: unstable sorts (`kind="quicksort"` ties), iteration over Python sets/dicts with nondeterministic order, internal `random` calls. Make tie-breaking explicit (`kind="stable"`, lowest-index rules), keep the decoder free of RNG, and add a regression test that decodes a fixed genotype and compares against a stored phenotype.

**Multi-segment chromosomes drift out of sync with the model.** When the assignment block grows but the sequencing block does not (or vice versa), decoding silently misreads genes. Centralize the block layout in one place (named slices), assert the genotype length at the decoder boundary, and version the layout alongside saved populations.

## Tools & Libraries

| Library | When to use | Note |
|---|---|---|
| numpy | all decoders in this skill | `argsort(kind="stable")` for deterministic ties; position-loop pattern vectorizes constructive decoders across the population |
| brkga_mp_ipr | production BRKGA around your decoder | multi-parent BRKGA with implicit path relinking; you supply only the decode callable |
| pymoo | GA/DE/PSO engines with custom problems | wrap the decoder inside `Problem._evaluate`; supports batch evaluation |
| scipy.stats | locality measurement | `kendalltau` between decoded permutations quantifies phenotype distance |
| OR-Tools CP-SAT | exact baseline for coverage checks | solve small RCPSP/scheduling instances exactly to verify the decoder image contains the optimum |
| networkx | precedence-graph handling | topological sorts and transitive closures when preparing SGS inputs |
| numba | sequential decoders too slow in Python | SGS and first-fit loops compile well; keep the numpy reference version for testing |
| pandas | decoder-comparison experiments | one row per (instance, seed, decoder, engine) run; aggregate before claiming one decoder wins |

## Output Format

A complete decoder-design deliverable contains:

1. **Decoder specification table** — one row per candidate decoder, stating the contract before any tuning:

| Field | Example entry |
|---|---|
| Genotype space | $[0,1)^{n}$, one key per activity |
| Phenotype | start-time vector, active schedule |
| Decode rule | serial SGS, highest key first, stable ties |
| Feasibility | guaranteed (precedence + capacity absorbed) |
| Coverage | contains an optimum for regular objectives |
| Complexity | $O(n^2 K)$ per decode |
| Tie-breaking | lowest activity index |
| Warm start | encode heuristic priorities as ranks/n |

2. **Code artifacts** — the decoder module (pure functions, no RNG inside), an independent `validate_*` feasibility checker on a separate code path, and the warm-start encoder if one exists.
3. **Determinism evidence** — a regression test decoding a fixed genotype to a stored phenotype, run on at least two platforms/numpy versions if results will be published.
4. **Bias and coverage report** — distribution of phenotype quality under uniform genotype sampling; on small instances, gap between the exact optimum and the best decodable solution (sampled or enumerated). State explicitly whether the image provably contains an optimum.
5. **Engine integration summary** — which engine drives the genotype, bound-handling rule for continuous engines, write-back policy for local search, and where elite fitness is cached.
6. **Experiment table** — mean/best objective and decode time per (instance, decoder, seed), aggregated over ≥10 seeds, so the decoder choice is backed by data rather than taste.

Report solution quality always on validated phenotypes: run the independent checker on every solution that appears in a table.

## Questions to Ask

- What object is the phenotype — sequence, subset, assignment, schedule — and which constraints must the decoder absorb versus repair or penalize?
- Which search engine will drive the genotype (BRKGA, GA, PSO, DE), and is the genotype type chosen to match its native operators?
- Is there an existing constructive heuristic whose priorities the genotype can replace — and should it be encoded as a warm start?
- What is the evaluation budget, and what does one decode cost at the largest instance size?
- Must the decoder's image provably contain an optimal solution, or is a strong greedy bias acceptable?
- How are ties broken, and is the decoder fully deterministic (no internal randomness, stable sorts)?
- Will local search run on phenotypes, and if so, is Lamarckian write-back possible for this decoder?
- How will feasibility be verified independently of the decoder?
- On which small instances can decoder coverage be checked against an exact solver?
- How many seeds and instances will back the comparison between candidate decoders?

## Related Skills

- **solution-encodings** — when the question is choosing between direct and indirect representations, or matching encodings to operators before committing to a decoder.
- **biased-random-key-genetic-algorithm** — when a decoder exists and the standard random-key evolutionary engine (elite/mutant partition, biased crossover) should drive it.
- **constraint-handling-techniques** — when constraints will be penalized or repaired instead of absorbed into the decoder, or to design the repair step of a threshold decoder.
- **job-shop-scheduling** — when the decoded phenotype is a job-shop schedule and disjunctive models, Giffler-Thompson construction, or critical-path neighborhoods are needed.
- **particle-swarm-optimization** — when a continuous engine drives random keys and velocity, topology, or bound-handling questions arise.
