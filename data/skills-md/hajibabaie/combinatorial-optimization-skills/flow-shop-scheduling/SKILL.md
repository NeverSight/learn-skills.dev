---
name: flow-shop-scheduling
description: When the user wants to model or solve flow-shop scheduling problems - permutation flow-shop makespan computation, the NEH heuristic, MIP models in gurobipy, and iterated greedy as the state-of-the-art metaheuristic, with a makespan-plus-tardiness multi-objective extension. Also use when the user mentions "flow shop," "permutation flow shop," "NEH," "iterated greedy," "Taillard," "makespan minimization," or when every job visits all machines in the same fixed order. For job-specific machine routes, see job-shop-scheduling; for Pareto trade-off analysis, see multi-objective-optimization.
---

# Flow-Shop Scheduling

You are an expert in flow-shop scheduling. This skill covers the permutation flow-shop problem (PFSP):
fast makespan evaluation, the NEH construction heuristic, exact MIP formulations, iterated greedy (IG)
as the state-of-the-art heuristic, Taillard-style benchmark instances, and the multi-objective
extension with makespan plus total tardiness. Use the framework below to match the formulation and
solution method to instance size, objective, and time budget.

## Initial Assessment

Establish the following before writing any model or code:

- **Instance size.** Number of jobs `n` and machines `m`. Taillard sizes run from 20x5 to 500x20.
  Exact methods prove optimality only for roughly `n <= 15`; everything larger is heuristic territory.
- **Routing structure.** Confirm every job visits machines `1..m` in the same order. If jobs have
  job-specific routes, this is a job shop — switch to job-shop-scheduling.
- **Permutation assumption.** Is the same job order required on all machines? Standard PFSP assumes
  yes. For `m >= 4`, the best non-permutation schedule can beat the best permutation schedule;
  confirm the user accepts the (almost universal) permutation restriction.
- **Buffer behavior.** Unlimited intermediate buffers (standard), no buffers (blocking), or
  no waiting allowed between machines (no-wait)? Each changes the makespan recursion.
- **Setup times.** Sequence-dependent setup times (SDST) change both the MIP and the acceleration
  data structures; ask explicitly.
- **Objective.** Makespan `C_max`, total flowtime, total (weighted) tardiness, or several at once?
  Tardiness needs due dates — ask how they are generated or provided.
- **Exact vs heuristic need.** Is a provable optimum required, or is "within 1% of best known in
  30 seconds" acceptable? This decides MIP vs NEH/IG immediately.
- **Time budget.** Per-instance wall-clock limit. The standard PFSP stopping convention is
  `t = n * (m / 2) * 60` milliseconds (Ruiz & Stuetzle 2007); confirm what comparison protocol applies.
- **Solver availability.** Gurobi license present? If not, the MIP parts map to HiGHS/CBC via the
  same model structure, or skip exact methods entirely.
- **Data format.** Matrix of processing times `p[i][j]` (machine-major) or job-major? Taillard files
  list processing times machine by machine; off-by-one transposition is the most common data bug.
- **Benchmark expectations.** Will results be compared against Taillard or VRF best-known values?
  Then fix seeds, report relative percentage deviation (RPD), and pin the reference-value snapshot.
- **Reproducibility.** Seeds for instance generation and for every metaheuristic run; one result row
  per (instance, algorithm, seed).

## Problem Definition and Model Landscape

**Permutation flow-shop problem, `Fm | prmu | C_max`.** Given `n` jobs and `m` machines, job `j`
needs processing time `p_{i,j} >= 0` on machine `i`. Every job visits machines `1, 2, ..., m` in this
order. All machines process jobs in the same sequence `pi` (a permutation of the jobs). Each machine
handles one job at a time; operations are non-preemptive. Completion times follow the recursion

$$
C_{i,\pi(k)} = \max\big(C_{i-1,\pi(k)},\; C_{i,\pi(k-1)}\big) + p_{i,\pi(k)},
\qquad C_{0,\cdot} = 0,\quad C_{\cdot,\pi(0)} = 0,
$$

for machines `i = 1..m` and sequence positions `k = 1..n`. The makespan is
`C_max(pi) = C_{m, pi(n)}`. The search space is the set of `n!` permutations.

Complexity landmarks:

- `F2 || C_max` is solvable in `O(n log n)` by Johnson's rule (Johnson 1954, "Optimal two- and
  three-stage production schedules with setup times included").
- `F3 || C_max` is already strongly NP-hard (Garey, Johnson & Sethi 1976, "The complexity of
  flowshop and jobshop scheduling").
- For `m <= 3` an optimal permutation schedule exists; for `m >= 4` the gap between the best
  permutation and the best non-permutation schedule can grow with `m`
  (Potts, Shmoys & Williamson 1991). In practice almost all research and industry use restricts
  to permutations.

### Variants

| Variant | What changes | Practical note |
|---|---|---|
| Standard PFSP `Fm\|prmu\|C_max` | nothing — the base case | this skill's core |
| No-wait `Fm\|nwt\|C_max` | a job may never wait between machines | reduces to an asymmetric TSP over completion-distance |
| Blocking `Fm\|block\|C_max` | no intermediate buffers; a finished job blocks its machine | different recursion (departure times), different acceleration |
| No-idle | machines must run without idle time | niche; changes feasibility of sequences |
| SDST | sequence-dependent setup `s_{i,j,k}` between job j and k on machine i | add setups to recursion and MIP; IG still works well |
| Hybrid / flexible flow shop | parallel machines per stage | assignment + sequencing; combine with parallel-machine ideas |
| Distributed PFSP | several factories, assign then sequence | two-level decisions; IG variants dominate |

### Objectives

| Objective | Definition | Method of choice |
|---|---|---|
| Makespan `C_max` | completion of last job on last machine | NEH + iterated greedy |
| Total flowtime `sum C_j` | sum of last-machine completions | IG variants with different acceleration (Pan & Ruiz 2012) |
| Total tardiness `sum T_j` | `T_j = max(C_j - d_j, 0)` with due dates `d_j` | IG/local search; due-date generation matters |
| Bi-objective (`C_max`, `sum T_j`) | Pareto front | weighted sum / epsilon-constraint / NSGA-II — see multi-objective-optimization |

### Method selection

- `n <= 12-15`: solve the MIP to optimality; warm start with NEH. Use the exact optimum to validate
  the heuristic pipeline.
- Any `n`, milliseconds available: NEH. It lands within roughly 2-4% of best known on Taillard
  instances and is the standard starting point for everything else.
- Seconds to minutes available: iterated greedy. Despite hundreds of published "novel"
  metaheuristics, IG and close relatives remain the state of the art for PFSP makespan
  (Ruiz & Stuetzle 2007; Fernandez-Viagas, Ruiz & Framinan 2017 review).
- Population-based alternative (e.g., when a decoder-based framework already exists): BRKGA with a
  sort decoder — see biased-random-key-genetic-algorithm.
- Non-permutation, blocking with complex side constraints, or mixed shop features: consider the
  CP-SAT interval model from job-shop-scheduling instead of forcing a PFSP shape.

### Benchmarks

Taillard (1993, "Benchmarks for basic scheduling problems"): 120 instances, 12 sizes
(20x5 up to 500x20), 10 instances per size, processing times integer uniform on `[1, 99]` from a
published seed list. Vallada, Ruiz & Framinan (2015) add 480 larger, harder instances (VRF).
Report performance as relative percentage deviation from the best-known value:
`RPD = 100 * (C - C_best) / C_best`, averaged over instances and seeds.

## Makespan Evaluation and the NEH Heuristic

Everything in PFSP work stands on a fast, correct makespan function. The recursion is a max-plus
scan that is sequential in both dimensions, so the right vectorization axis is the *batch* of
permutations (populations, multi-seed evaluation), not a single sequence.

```python
import numpy as np


def makespan(p: np.ndarray, perm: np.ndarray) -> int:
    """C_max of permutation `perm` for processing times p with shape (m, n).

    Rolling-array form of the recursion; O(nm) time, O(n) memory. The max-plus
    scan is sequential in both dimensions, so these two loops cannot be replaced
    by broadcasting; vectorize over batches of permutations instead.
    """
    q = p[:, perm]
    c = np.zeros(q.shape[1], dtype=np.int64)
    for i in range(q.shape[0]):
        c[0] += q[i, 0]
        for k in range(1, q.shape[1]):
            c[k] = max(c[k], c[k - 1]) + q[i, k]
    return int(c[-1])


def completion_matrix(p: np.ndarray, perm: np.ndarray) -> np.ndarray:
    """Full (m, n) completion-time matrix in sequence order.

    C[i, k] is the completion of the k-th sequenced job on machine i; use it
    for Gantt charts, tardiness objectives, and validators."""
    m, n = p.shape
    q = p[:, perm]
    c = np.zeros((m, n), dtype=np.int64)
    for i in range(m):
        for k in range(n):
            left = c[i, k - 1] if k > 0 else 0
            up = c[i - 1, k] if i > 0 else 0
            c[i, k] = max(left, up) + q[i, k]
    return c


def makespan_batch(p: np.ndarray, perms: np.ndarray) -> np.ndarray:
    """Makespans of a (B, n) batch of permutations, vectorized over the batch.

    Use this to evaluate whole metaheuristic populations in one call."""
    m = p.shape[0]
    q = p[:, perms]                       # (m, B, n) via fancy indexing
    c = np.zeros(perms.shape, dtype=np.int64)
    for i in range(m):
        c[:, 0] += q[i, :, 0]
        for k in range(1, perms.shape[1]):
            c[:, k] = np.maximum(c[:, k], c[:, k - 1]) + q[i, :, k]
    return c[:, -1]


p = np.array([[3, 2, 4], [2, 4, 1]])      # m=2 machines, n=3 jobs
print(makespan(p, np.array([0, 1, 2])))   # Expected: 10 (optimal; Johnson's rule confirms)
print(makespan_batch(p, np.array([[0, 1, 2], [2, 0, 1]])))
# Expected: [10 13]
```

**NEH** (Nawaz, Enscore & Ham 1983) sorts jobs by decreasing total processing time and inserts them
one at a time at the makespan-minimizing position. Implemented naively it costs `O(n^3 m)`; with
Taillard's head/tail acceleration (Taillard 1990, "Some efficient heuristic methods for the flow
shop sequencing problem") all `k+1` insertion positions of one job are evaluated in `O(mk)` total,
giving `O(n^2 m)` for the whole heuristic. The same routine is the engine inside iterated greedy.

For a partial sequence `s` of length `k`, define heads `e[i, l]` (earliest completion of `s[l]` on
machine `i`), tails `t[i, l]` (time from the start of `s[l]` on machine `i` to the end of the
schedule, computed backwards), and `f[i, l]` (completion of the inserted job at position `l` on
machine `i`). The makespan after inserting at position `l` is `max_i (f[i, l] + t[i, l])`, with a
zero tail when inserting at the end.

```python
import numpy as np


def insertion_makespans(p: np.ndarray, seq: np.ndarray, job: int) -> np.ndarray:
    """Makespan of inserting `job` at every position 0..len(seq) of `seq`.

    Taillard (1990) acceleration: heads e, tails t, and inserted-job completions
    f give all len(seq)+1 makespans in O(m * len(seq)) total, instead of
    O(m * len(seq)^2) for naive re-evaluation of every position.
    """
    m, k = p.shape[0], seq.size
    q = p[:, seq].astype(np.float64)
    e = np.zeros((m, k))       # e[i, l]: completion of seq[l] on machine i
    t = np.zeros((m, k))       # t[i, l]: tail from the start of seq[l] on machine i
    f = np.zeros((m, k + 1))   # f[i, l]: completion of `job` inserted at position l
    for i in range(m):
        for l in range(k):
            e[i, l] = max(e[i, l - 1] if l else 0.0,
                          e[i - 1, l] if i else 0.0) + q[i, l]
    for i in range(m - 1, -1, -1):
        for l in range(k - 1, -1, -1):
            t[i, l] = max(t[i, l + 1] if l < k - 1 else 0.0,
                          t[i + 1, l] if i < m - 1 else 0.0) + q[i, l]
    for l in range(k + 1):
        for i in range(m):
            f[i, l] = max(e[i, l - 1] if l else 0.0,
                          f[i - 1, l] if i else 0.0) + p[i, job]
    tails = np.hstack([t, np.zeros((m, 1))])   # inserting at the end has no tail
    return (f + tails).max(axis=0)


def neh(p: np.ndarray) -> tuple[np.ndarray, int]:
    """NEH heuristic (Nawaz, Enscore & Ham 1983), O(n^2 m) with acceleration.

    Sort jobs by decreasing total processing time (stable, so ties keep index
    order — document this, ties change the result), then insert each job at the
    position minimizing the partial-sequence makespan.
    """
    order = np.argsort(-p.sum(axis=0), kind="stable")
    seq = order[:1].copy()
    best = int(p[:, order[0]].sum())
    for job in order[1:]:
        ms = insertion_makespans(p, seq, int(job))
        pos = int(np.argmin(ms))
        best = int(ms[pos])
        seq = np.insert(seq, pos, job)
    return seq, best


p = np.array([[3, 2, 4], [2, 4, 1]])
perm, cmax = neh(p)
print(perm, cmax)
# Expected: perm [1 0 2] with makespan 10 (NEH finds the optimum on this instance)
```

## Exact MIP Models in Gurobi

Two classic formulation families exist (computational comparison: Tseng, Stafford & Gupta 2004).
Both prove optimality only on small instances; their real value is validating heuristics and
producing certified optima/bounds for papers.

**Positional model (Wilson 1989 family).** Binary `x[j,k] = 1` if job `j` occupies sequence
position `k`; continuous `c[i,k]` is the completion time of the position-`k` job on machine `i`:

$$
\min\ c_{m,n} \quad \text{s.t.}\quad
\sum_k x_{jk} = 1,\ \sum_j x_{jk} = 1;\qquad
c_{ik} \ge c_{i-1,k} + \textstyle\sum_j p_{ij} x_{jk};\qquad
c_{ik} \ge c_{i,k-1} + \textstyle\sum_j p_{ij} x_{jk}.
$$

No big-M appears: position-indexed completion times encode both the machine order and the sequence
order directly, which gives a comparatively strong LP relaxation at the price of `n^2` binaries.

```python
import gurobipy as gp
import numpy as np
from gurobipy import GRB


def add_assignment_constraints(model: gp.Model, vars_: dict, data: np.ndarray) -> None:
    """Each job takes exactly one position; each position holds exactly one job."""
    x = vars_["x"]
    n = data.shape[1]
    model.addConstrs((x.sum(j, "*") == 1 for j in range(n)), name="job_once")
    model.addConstrs((x.sum("*", k) == 1 for k in range(n)), name="pos_once")


def add_route_constraints(model: gp.Model, vars_: dict, data: np.ndarray) -> None:
    """The job in position k starts on machine i only after leaving machine i-1."""
    x, c = vars_["x"], vars_["c"]
    m, n = data.shape
    for i in range(m):
        for k in range(n):
            proc = gp.quicksum(float(data[i, j]) * x[j, k] for j in range(n))
            prev = c[i - 1, k] if i > 0 else 0.0
            model.addConstr(c[i, k] >= prev + proc, name=f"route[{i},{k}]")


def add_sequence_constraints(model: gp.Model, vars_: dict, data: np.ndarray) -> None:
    """Machine i starts position k only after finishing position k-1."""
    x, c = vars_["x"], vars_["c"]
    m, n = data.shape
    for i in range(m):
        for k in range(1, n):
            proc = gp.quicksum(float(data[i, j]) * x[j, k] for j in range(n))
            model.addConstr(c[i, k] >= c[i, k - 1] + proc, name=f"seq[{i},{k}]")


def solve_pfsp_positional(p: np.ndarray, time_limit: float = 60.0,
                          warm_start: np.ndarray | None = None) -> tuple[list[int], float, float]:
    """Positional PFSP MIP. Returns (permutation, C_max, final MIP gap)."""
    m, n = p.shape
    model = gp.Model("pfsp_positional")
    model.Params.OutputFlag = 0
    model.Params.TimeLimit = time_limit
    x = model.addVars(n, n, vtype=GRB.BINARY, name="x")
    c = model.addVars(m, n, lb=0.0, name="c")
    vars_ = {"x": x, "c": c}
    add_assignment_constraints(model, vars_, p)
    add_route_constraints(model, vars_, p)
    add_sequence_constraints(model, vars_, p)
    model.setObjective(c[m - 1, n - 1], GRB.MINIMIZE)
    if warm_start is not None:               # e.g. the NEH permutation (MIP start)
        for k, j in enumerate(warm_start):
            x[int(j), int(k)].Start = 1.0
    model.optimize()
    ok = model.Status == GRB.OPTIMAL or (model.Status == GRB.TIME_LIMIT and model.SolCount > 0)
    if not ok:
        raise RuntimeError(f"no feasible solution, status {model.Status}")
    perm = [j for k in range(n) for j in range(n) if x[j, k].X > 0.5]
    return perm, model.ObjVal, model.MIPGap


p = np.array([[3, 2, 4], [2, 4, 1]])
perm, cmax, gap = solve_pfsp_positional(p, time_limit=10.0)
print(perm, cmax, gap)
# Expected: a permutation with C_max = 10.0 and gap 0.0 (e.g. [0, 1, 2])
```

**Disjunctive model (Manne 1960 family).** One precedence binary `y[j,l]` per unordered job pair,
shared across all machines — sharing is exactly what enforces the permutation property. Big-M
constraints order each pair on each machine. Only `n(n-1)/2` binaries, but the LP relaxation is
weak because of the big-M terms. In the Tseng-Stafford-Gupta experiments Manne-type models are
often the fastest to *solve* despite the weaker bound, because they are much smaller — test both
on your instances.

```python
import gurobipy as gp
import numpy as np
from gurobipy import GRB


def add_route_constraints(model: gp.Model, vars_: dict, data: np.ndarray) -> None:
    """Each job follows the machine order 1..m."""
    c = vars_["c"]
    m, n = data.shape
    for j in range(n):
        model.addConstr(c[0, j] >= float(data[0, j]), name=f"first[{j}]")
        for i in range(1, m):
            model.addConstr(c[i, j] >= c[i - 1, j] + float(data[i, j]),
                            name=f"route[{i},{j}]")


def add_disjunctive_constraints(model: gp.Model, vars_: dict, data: np.ndarray) -> None:
    """One precedence binary per job pair, shared by all machines (permutation property)."""
    c, y = vars_["c"], vars_["y"]
    m, n = data.shape
    big_m = float(data.sum())            # tightest simple bound: total work
    for j in range(n):
        for l in range(j + 1, n):
            for i in range(m):
                model.addConstr(c[i, j] >= c[i, l] + float(data[i, j]) - big_m * y[j, l],
                                name=f"disj_a[{i},{j},{l}]")
                model.addConstr(c[i, l] >= c[i, j] + float(data[i, l]) - big_m * (1 - y[j, l]),
                                name=f"disj_b[{i},{j},{l}]")


def add_makespan_constraints(model: gp.Model, vars_: dict, data: np.ndarray) -> None:
    """C_max dominates every job's completion on the last machine."""
    c, cmax = vars_["c"], vars_["cmax"]
    m, n = data.shape
    model.addConstrs((cmax >= c[m - 1, j] for j in range(n)), name="span")


def solve_pfsp_manne(p: np.ndarray, time_limit: float = 60.0) -> tuple[list[int], float, float]:
    """Manne-style disjunctive PFSP model: n(n-1)/2 binaries, big-M precedence."""
    m, n = p.shape
    model = gp.Model("pfsp_manne")
    model.Params.OutputFlag = 0
    model.Params.TimeLimit = time_limit
    c = model.addVars(m, n, lb=0.0, name="c")
    y = model.addVars(((j, l) for j in range(n) for l in range(j + 1, n)),
                      vtype=GRB.BINARY, name="y")
    cmax = model.addVar(lb=0.0, name="cmax")
    vars_ = {"c": c, "y": y, "cmax": cmax}
    add_route_constraints(model, vars_, p)
    add_disjunctive_constraints(model, vars_, p)
    add_makespan_constraints(model, vars_, p)
    model.setObjective(cmax, GRB.MINIMIZE)
    model.optimize()
    ok = model.Status == GRB.OPTIMAL or (model.Status == GRB.TIME_LIMIT and model.SolCount > 0)
    if not ok:
        raise RuntimeError(f"no feasible solution, status {model.Status}")
    perm = sorted(range(n), key=lambda j: c[m - 1, j].X)
    return perm, cmax.X, model.MIPGap


p = np.array([[3, 2, 4], [2, 4, 1]])
perm, cmax_val, gap = solve_pfsp_manne(p, time_limit=10.0)
print(perm, cmax_val, gap)
# Expected: C_max = 10.0 with gap 0.0; perm read off last-machine completion order
```

Feed the NEH permutation into `warm_start` whenever you run the positional model — the solver gets
an incumbent immediately and the search becomes pure bound-proving. Patterns for MIP starts and
variable hints live in warm-starts-and-initial-solutions.

## Iterated Greedy — the State of the Art

Iterated greedy (Ruiz & Stuetzle 2007, "A simple and effective iterated greedy algorithm for the
permutation flowshop scheduling problem") repeats two steps from an NEH start: **destruction**
(remove `d` random jobs) and **construction** (reinsert each removed job at its best position with
the Taillard acceleration), with a constant-temperature Metropolis acceptance. It is the IG
instantiation of the ILS template — perturbation-strength tuning, acceptance variants, and restart
logic are covered in iterated-local-search. The insertion evaluation is the vectorizable hot spot:
each call scores all `k+1` positions in one accelerated pass.

```python
import numpy as np


def _makespan(p: np.ndarray, perm: np.ndarray) -> float:
    """C_max via the rolling-array recursion; O(nm)."""
    q = p[:, perm]
    c = np.zeros(q.shape[1])
    for i in range(q.shape[0]):
        c[0] += q[i, 0]
        for k in range(1, q.shape[1]):
            c[k] = max(c[k], c[k - 1]) + q[i, k]
    return float(c[-1])


def _best_insertion(p: np.ndarray, seq: np.ndarray, job: int) -> tuple[int, float]:
    """Best insertion position and resulting C_max (Taillard acceleration, O(m*len(seq)))."""
    m, k = p.shape[0], seq.size
    q = p[:, seq].astype(np.float64)
    e = np.zeros((m, k))
    t = np.zeros((m, k))
    f = np.zeros((m, k + 1))
    for i in range(m):
        for l in range(k):
            e[i, l] = max(e[i, l - 1] if l else 0.0, e[i - 1, l] if i else 0.0) + q[i, l]
    for i in range(m - 1, -1, -1):
        for l in range(k - 1, -1, -1):
            t[i, l] = max(t[i, l + 1] if l < k - 1 else 0.0,
                          t[i + 1, l] if i < m - 1 else 0.0) + q[i, l]
    for l in range(k + 1):
        for i in range(m):
            f[i, l] = max(e[i, l - 1] if l else 0.0, f[i - 1, l] if i else 0.0) + p[i, job]
    ms = (f + np.hstack([t, np.zeros((m, 1))])).max(axis=0)
    pos = int(np.argmin(ms))
    return pos, float(ms[pos])


def iterated_greedy(p: np.ndarray, seed: int = 0, max_iters: int = 2000, d: int = 4,
                    temp_factor: float = 0.4) -> tuple[np.ndarray, float]:
    """IG of Ruiz & Stuetzle (2007): NEH start, destruct-reconstruct loop,
    constant-temperature acceptance. Framework: see iterated-local-search."""
    rng = np.random.default_rng(seed)
    m, n = p.shape
    temp = temp_factor * p.sum() / (10.0 * n * m)
    order = np.argsort(-p.sum(axis=0), kind="stable")    # NEH construction
    cur = order[:1].copy()
    for job in order[1:]:
        pos, _ = _best_insertion(p, cur, int(job))
        cur = np.insert(cur, pos, job)
    cur_ms = _makespan(p, cur)
    best, best_ms = cur.copy(), cur_ms
    for _ in range(max_iters):
        removed = rng.choice(n, size=min(d, n - 1), replace=False)
        partial = cur[~np.isin(cur, removed)]
        cand_ms = cur_ms
        for job in removed:                              # greedy reconstruction
            pos, cand_ms = _best_insertion(p, partial, int(job))
            partial = np.insert(partial, pos, job)
        if cand_ms < cur_ms or rng.random() < np.exp((cur_ms - cand_ms) / temp):
            cur, cur_ms = partial, cand_ms
            if cur_ms < best_ms:
                best, best_ms = cur.copy(), cur_ms
    return best, best_ms


p = np.array([[3, 2, 4], [2, 4, 1]], dtype=np.float64)
perm, cmax = iterated_greedy(p, seed=42, max_iters=200, d=2)
print(perm, cmax)
# Expected: C_max = 10.0 (the optimum for this 3-job, 2-machine instance)
```

Parameter guidance (defaults are robust — IG is famously insensitive):

| Parameter | Typical range | Trade-off |
|---|---|---|
| `d` (jobs removed) | 2-8, default 4 | larger = stronger perturbation, slower reconstruction |
| `temp_factor` | 0.2-0.7, default 0.4 | higher accepts more worsening moves (diversification) |
| stopping | `n*(m/2)*60` ms or fixed iterations | time-based for benchmark comparability |

The full IG_RS adds an insertion local search (repeatedly extract one job, reinsert at its best
position, until a full pass yields no improvement) after each reconstruction; it costs `O(n^2 m)`
per pass and buys roughly 0.3-0.6% average RPD on Taillard instances. Add it when the time budget
allows more than a few seconds.

## Instance Generation and Independent Validation

Group every experiment around seeded generators and a validator that shares no code with the
optimization pipeline. The generator below follows Taillard's distribution; the due-date scheme
follows the tardiness literature (Vallada, Ruiz & Minella 2008, tardiness benchmark design).

```python
import numpy as np


def taillard_instance(m: int, n: int, seed: int) -> np.ndarray:
    """Taillard (1993)-style PFSP instance: integer processing times U[1, 99].

    Returns p with shape (m, n). Fix the seed and report (m, n, seed) next to
    every result row so any number in a paper can be regenerated."""
    rng = np.random.default_rng(seed)
    return rng.integers(1, 100, size=(m, n), dtype=np.int64)


def lower_bound(p: np.ndarray) -> int:
    """Machine-based lower bound on C_max (Taillard 1993).

    For each machine: its total load plus the smallest head (work before it)
    and smallest tail (work after it) over jobs; also the longest job."""
    m, n = p.shape
    heads = np.vstack([np.zeros(n), np.cumsum(p, axis=0)[:-1]])   # work before machine i
    tails = p[::-1].cumsum(axis=0)[::-1] - p                      # work after machine i
    machine_lb = (p.sum(axis=1) + heads.min(axis=1) + tails.min(axis=1)).max()
    job_lb = p.sum(axis=0).max()
    return int(max(machine_lb, job_lb))


def due_dates(p: np.ndarray, seed: int, tf: float = 0.4, rdd: float = 0.6) -> np.ndarray:
    """Due dates for tardiness objectives via the TF/RDD scheme.

    Drawn uniformly from [LB*(1-tf-rdd/2), LB*(1-tf+rdd/2)] where LB estimates
    C_max. Larger tf = tighter dates = more tardy jobs; larger rdd = wider
    spread. Both shift instance difficulty, so always report (tf, rdd, seed)."""
    rng = np.random.default_rng(seed)
    lb = lower_bound(p)
    lo, hi = lb * (1.0 - tf - rdd / 2.0), lb * (1.0 - tf + rdd / 2.0)
    d = rng.uniform(max(lo, 0.0), hi, size=p.shape[1])
    return np.maximum(d, p.sum(axis=0))    # a job is never due before its own total work


p_small = np.array([[3, 2, 4], [2, 4, 1]])
print(lower_bound(p_small))    # Expected: 10 — matches the optimal C_max on this instance
p = taillard_instance(5, 20, seed=1)
print(p.shape, bool(p.min() >= 1 and p.max() <= 99))
# Expected: (5, 20) True
```

The validator recomputes feasibility and the objective in plain Python, on purpose: a bug in the
vectorized evaluator (or in the MIP) cannot also live in this code path. Run it on every solution
that leaves the pipeline, and cross-check exact-vs-heuristic results on small instances.

```python
import numpy as np


def validate_pfsp(p: np.ndarray, perm: np.ndarray, claimed_cmax: float,
                  tol: float = 1e-6) -> list[str]:
    """Independent feasibility + objective check; returns violations (empty == valid).

    Checks: (1) perm is a true permutation of 0..n-1; (2) the claimed makespan
    equals a from-scratch completion-time recomputation done in plain Python,
    independent of any vectorized or solver code."""
    m, n = p.shape
    if sorted(int(j) for j in perm) != list(range(n)):
        return [f"perm is not a permutation of 0..{n - 1}: {list(perm)}"]
    c = [[0.0] * n for _ in range(m)]
    for k, j in enumerate(int(v) for v in perm):
        for i in range(m):
            left = c[i][k - 1] if k > 0 else 0.0
            up = c[i - 1][k] if i > 0 else 0.0
            c[i][k] = max(left, up) + float(p[i, j])
    recomputed = c[m - 1][n - 1]
    if abs(recomputed - float(claimed_cmax)) > tol:
        return [f"claimed C_max {claimed_cmax} != recomputed {recomputed}"]
    return []


p = np.array([[3, 2, 4], [2, 4, 1]])
print(validate_pfsp(p, np.array([1, 0, 2]), 10))
# Expected: [] (valid)
print(validate_pfsp(p, np.array([1, 0, 2]), 9))
# Expected: ['claimed C_max 9 != recomputed 10.0']
```

## Advanced Techniques

### Taillard acceleration beyond NEH

The head/tail data structure pays off anywhere insertions are evaluated: NEH (`O(n^3 m)` down to
`O(n^2 m)`), IG reconstruction, and the insertion local search. Two caveats. First, the trick is
makespan-specific — tails do not exist for total flowtime or tardiness, where every completion time
matters; flowtime needs different incremental schemes (Pan & Ruiz 2012) or honest recomputation.
Second, heads `e` can be reused across the `d` insertions of one IG reconstruction only for the
prefix untouched by earlier insertions; the simple version above recomputes them, which is still
the standard implementation and rarely the bottleneck below `n = 500`.

### NEH tie-breaking and priority orders

Two tie sources change NEH results between implementations: equal job totals in the initial sort
and equal makespans in `argmin` over positions. A stable sort plus first-best `argmin` (as coded
above) is reproducible but not best-performing. NEH-D (Dong, Huang & Chen 2008) orders jobs by
mean plus standard deviation of processing times; the tie-breaker of Fernandez-Viagas & Framinan
(2014) picks among equal-makespan positions the one minimizing front-machine idle time and is the
strongest published variant. When you compare against published NEH numbers, state the exact
tie-breaking rule — differences up to 1% RPD come from ties alone.

### Tuning and extending iterated greedy

IG's strength is robustness: on Taillard benchmarks, `d = 4` and `temp_factor = 0.4` are
near-optimal across all sizes, so tune the stopping rule before anything else. Worthwhile
extensions, in order of payoff: (1) insertion local search after reconstruction (IG_RS); (2)
local search also on the partial sequence after destruction (IG variants of Fernandez-Viagas &
Framinan); (3) for total flowtime or tardiness, swap the acceptance to best-insertion under the new
objective and replace the acceleration. Population-based methods (BRKGA with a sort decoder, EDAs
with position-frequency models) reach similar quality but need more evaluations; they pay off when
a decoder framework or parallel fitness evaluation already exists.

### Bi-objective makespan + tardiness

Bi-objective PFSP (`C_max`, `sum T_j`) is the standard multi-objective extension (survey: Minella,
Ruiz & Ciavotta 2008). For a handful of trade-off points run epsilon-constraint on the MIP
(constrain `sum T_j <= eps`, minimize `C_max`, sweep `eps`); for a dense front use NSGA-II or a
Pareto-archive IG. Non-dominated sorting, crowding, hypervolume, and pymoo usage are in
multi-objective-optimization. The building blocks:

```python
import numpy as np


def bi_objective(p: np.ndarray, d: np.ndarray, perm: np.ndarray) -> tuple[float, float]:
    """(C_max, total tardiness) of a permutation; d[j] is job j's due date."""
    q = p[:, perm]
    c = np.zeros(q.shape[1])
    for i in range(q.shape[0]):
        c[0] += q[i, 0]
        for k in range(1, q.shape[1]):
            c[k] = max(c[k], c[k - 1]) + q[i, k]
    tardiness = float(np.maximum(c - d[perm], 0.0).sum())
    return float(c[-1]), tardiness


def pareto_front(points: np.ndarray) -> np.ndarray:
    """Indices of non-dominated rows of `points` (minimization), vectorized.

    Duplicates are kept: identical points do not dominate each other."""
    le = (points[:, None, :] <= points[None, :, :]).all(axis=2)
    lt = (points[:, None, :] < points[None, :, :]).any(axis=2)
    dominated = (le & lt).any(axis=0)
    return np.flatnonzero(~dominated)


p = np.array([[3, 2, 4], [2, 4, 1]])
d = np.array([6.0, 5.0, 11.0])
pts = np.array([bi_objective(p, d, np.array(s))
                for s in ([0, 1, 2], [1, 0, 2], [2, 1, 0])])
print(pts[pareto_front(pts)])
# Expected: [[10. 3.]] — perm [1, 0, 2] dominates the other two sequences
```

### Lower bounds and gap reporting

The machine-based bound in `lower_bound` is cheap and surprisingly tight on Taillard instances with
`n >> m` (often within 1-2% of the optimum for 100x5). Use it three ways: sanity-check every
reported makespan (`C >= LB` always), report heuristic gaps on instances without best-known values
(`100 * (C - LB) / LB` is then an upper bound on the true gap), and prune in any custom
branch-and-bound. The LP relaxation of the positional model gives a stronger but far more
expensive bound; it is rarely worth solving for bounds alone.

## Practical Challenges

**The MIP stalls beyond about 15 jobs.** This is expected, not a modeling bug: PFSP MIPs have weak
relaxations relative to the combinatorial structure, and `n = 20` is already out of reach for proof
of optimality in reasonable time. Use the MIP to certify optima on small instances (validating the
heuristic pipeline), warm start it with NEH, and report the residual `MIPGap` honestly when hitting
the time limit.

**Your IG results are worse than published numbers.** Check, in order: time-based stopping with the
`n*(m/2)*60` ms convention versus your iteration cap; presence of the insertion local search
(published IG_RS includes it); the temperature constant (the denominator `10*n*m` is part of the
formula, not a typo); and the RPD protocol (averaging over the right instance set, 5+ seeds per
instance, best-known values from the same snapshot the paper used).

**NEH gives different makespans across implementations.** Ties in the initial sort and in the
insertion `argmin` are resolved differently. Fix a deterministic rule (stable sort, first
minimizing position), document it, and never compare NEH variants across codebases without
matching tie-breakers.

**Makespan evaluation dominates the runtime.** Profile before optimizing, but the usual fixes are:
never rebuild the full completion matrix when the accelerated insertion routine answers the same
question; evaluate populations with `makespan_batch` instead of a Python loop over individuals;
and keep processing times in one contiguous `(m, n)` int64 array — repeated fancy indexing of
ragged structures costs more than the recursion itself.

**The permutation assumption silently discards better schedules.** For `m >= 4` the best
non-permutation schedule can beat the best permutation one. Almost all benchmarks and applications
accept this restriction, but say so explicitly in any write-up; if buffers are actually finite or
zero, the model must change (blocking PFSP), not just the search space.

**Tardiness results are not comparable across papers.** Due-date generation parameters (TF, RDD)
move instances between trivially easy (everything early) and brutally tight. Publish the generator,
the parameters, and the seeds with the results, and never mix due-date schemes inside one
experiment table.

**Best-known values drift over the years.** Taillard upper bounds have been improved repeatedly
since 1993. Pin the snapshot of best-known values you compare against (date + source), or your RPD
numbers cannot be reproduced after the next improvement.

**Integer data, float drift.** Taillard processing times are integers, so makespans are integers;
compute and compare them in int64 where possible. The float versions inside IG are fine for search,
but validate final results with exact integer recomputation to avoid reporting a 1245.0000000002.

## Tools & Libraries

| Library | When to use | Note |
|---|---|---|
| gurobipy | exact MIP models, warm-started optimality proofs | both formulations above; commercial license |
| OR-Tools CP-SAT | shop variants with side constraints, non-permutation schedules | interval variables; see job-shop-scheduling |
| HiGHS (highspy) / PuLP | no Gurobi license | same model structure; expect smaller solvable sizes |
| numpy | makespan evaluation, NEH, IG, batch population evaluation | the whole heuristic stack needs nothing else |
| pandas | result tables: one row per (instance, algorithm, seed) | aggregation to mean/best RPD per size |
| matplotlib | Gantt charts from `completion_matrix`, convergence curves | vector output for papers |
| pymoo | NSGA-II and quality indicators for the bi-objective extension | pairs with the `bi_objective` evaluator |

## Output Format

A complete flow-shop answer contains:

1. **Problem statement echo.** `n`, `m`, objective(s), variant (standard/blocking/SDST), permutation
   assumption confirmed, data source (Taillard set or generator with seeds).
2. **Model/method summary table.**

   | Component | Choice | Why |
   |---|---|---|
   | Construction | NEH (stable sort, first-best insertion) | standard, reproducible baseline |
   | Improvement | IG, `d=4`, `temp_factor=0.4`, time `n*(m/2)*60` ms | state of the art for C_max |
   | Exact reference | positional MIP, NEH warm start, 300 s limit | optima for n <= 12 validation set |
   | Validation | `validate_pfsp` on every reported solution | independent recomputation |

3. **Solution-quality report.** Per instance size: best/mean/worst RPD over seeds, mean time to
   best, and for MIP runs the bound, incumbent, and final gap. State the best-known-value snapshot.
4. **Validator confirmation.** Explicit statement that every reported permutation passed the
   independent check, plus the exact-vs-heuristic cross-check result on the small-instance set.
5. **Artifacts.** `results.csv` (one row per run: instance, m, n, seed, algorithm, parameters,
   objective, time), instance files or generator seeds, and optionally `gantt.png` of the best
   schedule and a convergence plot (best-so-far C_max vs time, band over seeds).
6. **Reproduction line.** The exact command/function call and seed list that regenerate every
   number shown.

## Questions to Ask

- How many jobs and machines, and is the size fixed or growing in production use?
- Does every job really visit all machines in the same order, or do some skip machines or take
  different routes?
- Is the same sequence on all machines acceptable (permutation schedules), or do you need the
  extra freedom of non-permutation schedules?
- Are there buffers between machines — unlimited, limited, or none (blocking)?
- Are setup times relevant, and do they depend on the job sequence?
- Which objective: makespan, flowtime, tardiness, or a trade-off between several?
- If tardiness matters: where do due dates come from, and how tight are they?
- Do you need a provable optimum, or a high-quality solution within a time budget — and what is
  that budget per instance?
- Is a Gurobi license available, or must everything run on open-source tools?
- Will results be benchmarked against Taillard/VRF best-known values for a paper?

## Related Skills

- **job-shop-scheduling** — when jobs have machine-specific routes, or you want the CP-SAT interval
  model for shop problems with side constraints.
- **iterated-local-search** — for the ILS framework behind IG: perturbation strength, acceptance
  criteria, and restart strategies.
- **biased-random-key-genetic-algorithm** — population-based alternative for the PFSP using a
  sort decoder over random keys.
- **multi-objective-optimization** — Pareto methods, epsilon-constraint, NSGA-II, and hypervolume
  for the makespan-plus-tardiness extension.
- **warm-starts-and-initial-solutions** — feeding NEH into MIP starts and seeding metaheuristic
  populations with construction heuristics.
