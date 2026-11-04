---
name: job-shop-scheduling
description: When the user wants to model and solve job-shop scheduling problems, sequencing job operations on machines under fixed per-job routes, minimizing makespan or tardiness, via disjunctive MIP, CP-SAT interval models, or critical-path tabu search. Also use when the user mentions "job shop," "disjunctive constraints," "makespan," "operations sequencing," "critical path neighborhood," "shifting bottleneck," or when every job visits machines in its own technological order. For permutation flow shops, see flow-shop-scheduling; for deeper CP-SAT modeling, see constraint-programming.
---

# Job-Shop Scheduling

You are an expert in job-shop scheduling (JSP), one of the hardest classic combinatorial
optimization problems relative to its size. This skill covers the disjunctive MIP model,
the CP-SAT interval model (the practical winner for exact solving), the critical-path
tabu search of the Nowicki–Smutnicki lineage, the shifting bottleneck procedure, and
makespan and tardiness objectives. Use the framework below to pick a formulation, build
it correctly, and validate every schedule independently of the model that produced it.

## Initial Assessment

Establish these facts before writing any model:

- **Size.** Number of jobs `n`, machines `m`, total operations (classically `n * m`).
  A 10x10 JSP is already serious for MIP; CP-SAT handles far larger instances.
- **Classical assumptions.** Confirm each one explicitly: every job visits every machine
  exactly once, operation order within a job is fixed (the technological route), no
  preemption, each machine processes one operation at a time, all jobs available at
  time zero. Any broken assumption changes the model class.
- **Variants in play.** Machine alternatives per operation mean flexible job shop
  (assignment + sequencing; see parallel-machine-scheduling for the assignment layer).
  Sequence-dependent setups, release dates, transport times, and recirculation (a job
  visiting a machine twice) each need model extensions.
- **Objective.** Makespan `C_max`, total weighted tardiness, or a mix. All regular
  objectives (non-decreasing in completion times) admit semi-active schedules; with
  non-regular objectives (earliness penalties) inserted idle time becomes a decision.
- **Exact-versus-heuristic need.** Is a proof of optimality required, or is a good
  schedule within a known gap acceptable? This decides MIP/CP versus tabu search.
- **Time budget.** Seconds per solve in a rolling-horizon loop versus hours for a
  one-off benchmark run; this caps which method is realistic.
- **Solver availability.** Gurobi license present? OR-Tools CP-SAT is free and is the
  default recommendation for exact JSP solving either way.
- **Data.** Integer processing times? CP-SAT requires integers, so scale and round
  floats. Benchmark files (OR-Library `ft06`/`ft10`/`la`, Taillard `ta`) or real data?
- **Baselines.** For benchmark instances, look up the known optimum or best-known value
  so gaps mean something (e.g., `ft06` = 55, `ft10` = 930).
- **Validation requirements.** Plan an independent feasibility checker from day one;
  never trust the model that produced the schedule to also certify it.

## Problem Definition and Model Landscape

**Notation.** Jobs $J = \{1,\dots,n\}$, machines $M = \{1,\dots,m\}$. Job $j$ is an
ordered sequence of operations $O_{j,1}, \dots, O_{j,m}$; operation $O_{j,k}$ must run
on machine $\mu_{j,k} \in M$ for $p_{j,k}$ time units without interruption. Each machine
processes at most one operation at a time, and operation $O_{j,k+1}$ may start only
after $O_{j,k}$ finishes. A schedule assigns a start time $s_{j,k} \ge 0$ to every
operation. The classical objective is the makespan

$$
C_{\max} = \max_{j \in J} \; \bigl( s_{j,m} + p_{j,m} \bigr),
$$

i.e., the completion time of the last operation. In the three-field notation this is
$Jm \,||\, C_{\max}$.

**Disjunctive graph.** The standard structure (Roy & Sussmann 1964; Balas 1969) is
$G = (V, A, E)$: vertices $V$ are the operations plus dummy source/sink, conjunctive
arcs $A$ encode the fixed routes within each job, and disjunctive edge set $E$ contains
one undirected edge for every pair of operations sharing a machine. A *selection*
orients every disjunctive edge; an acyclic selection is exactly a feasible processing
order, and the makespan of its semi-active schedule equals the longest source-sink path
with vertex weights $p_{j,k}$. Operations on that longest path form the *critical path*;
maximal runs of consecutive critical operations on one machine are *critical blocks*.
Two consequences drive everything below:

1. Reversing a disjunctive arc that is not on a critical path can never reduce the
   makespan, so local search only needs to consider critical-path moves.
2. The makespan for a fixed selection is a longest-path computation, $O(nm)$ time.

**Complexity.** JSP is strongly NP-hard for $m \ge 3$ (Garey, Johnson & Sethi 1976);
even $3 \times 3$-style special cases stay hard, while $J2$ with at most two operations
per job is polynomial (Jackson 1956). The infamous $10 \times 10$ instance `ft10`
(Fisher & Thompson 1963) resisted exact solution for 26 years until Carlier & Pinson
(1989) proved $C_{\max}^* = 930$; Applegate & Cook (1991) document the computational
arms race. Simple lower bounds: the maximum machine load
$\max_m \sum_{(j,k):\,\mu_{j,k}=m} p_{j,k}$ and the maximum job length
$\max_j \sum_k p_{j,k}$. Stronger bounds come from one-machine relaxations with heads
and tails ($1\,|\,r_j, q_j\,|\,C_{\max}$, Carlier 1982).

**Model landscape and selection guidance.**

| Approach | Size | Bound quality | Practical reach | Use when |
|---|---|---|---|---|
| Disjunctive MIP (Manne 1960) | $O(n^2 m)$ binaries | Weak LP (big-M) | ~10x10 with effort | You need duals/side constraints, or a matheuristic backbone |
| Time-indexed MIP | $O(nmT)$ binaries | Stronger LP | Small horizons only | Cost varies with absolute time (tardiness shapes) |
| Rank-based MIP (Wagner 1959) | $O(n^2 m)$ binaries | Moderate | Small | Rarely the best choice; useful for position-indexed side constraints |
| CP-SAT intervals | $nm$ intervals | Excellent propagation + LCG bounds | Optimal for many 100x20 instances | Default exact method |
| Critical-path tabu search | n/a | None (heuristic) | Any size | Large instances or tight time budgets; best-known values on benchmarks |
| Shifting bottleneck | n/a | One-machine bounds | Mid-size | Teaching, decomposition intuition, warm starts |

Ku & Beck (2016, "Mixed Integer Programming models for job shop scheduling: a
computational analysis") show the disjunctive model dominates the other MIPs but is
outclassed by CP; Da Col & Teppan (2019) report CP-SAT solving industrial-size job
shops with thousands of operations. The honest default: **CP-SAT for exact, tabu search
for heuristic, disjunctive MIP when you specifically need MIP machinery.**

**Tardiness objectives.** With due dates $d_j$ and weights $w_j$, total weighted
tardiness is $\sum_j w_j T_j$ with $T_j = \max(0,\, C_j - d_j)$ and
$C_j = s_{j,m} + p_{j,m}$. It is regular, so all machinery below (semi-active
schedules, critical-path reasoning on a modified graph, CP-SAT) still applies; only
the objective rows change. See the Advanced Techniques section for the implementation.

## Instance Generation and Independent Validation

Generate reproducible random instances in the style of Taillard (1993, "Benchmarks for
basic scheduling problems"): random machine permutations per job, integer durations
uniform on $[1, 99]$. Keep the classic `ft06` instance around as a regression anchor
with a literature-certified optimum.

```python
import numpy as np


def generate_jsp_instance(n_jobs: int, n_machines: int, seed: int,
                          t_lo: int = 1, t_hi: int = 99) -> tuple[np.ndarray, np.ndarray]:
    """Random classical JSP instance in Taillard (1993) style.

    machines[j, k] is the machine of the k-th operation of job j (a random
    permutation, so every job visits every machine exactly once);
    times[j, k] is the integer processing time of that operation.
    """
    rng = np.random.default_rng(seed)
    machines = np.argsort(rng.random((n_jobs, n_machines)), axis=1)
    times = rng.integers(t_lo, t_hi + 1, size=(n_jobs, n_machines))
    return machines, times


# ft06 (Fisher & Thompson 1963): 6 jobs x 6 machines, known optimal makespan 55.
FT06_MACHINES = np.array([[2, 0, 1, 3, 5, 4],
                          [1, 2, 4, 5, 0, 3],
                          [2, 3, 5, 0, 1, 4],
                          [1, 0, 2, 3, 4, 5],
                          [2, 1, 4, 5, 0, 3],
                          [1, 3, 5, 0, 4, 2]], dtype=np.int64)
FT06_TIMES = np.array([[1, 3, 6, 7, 3, 6],
                       [8, 5, 10, 10, 10, 4],
                       [5, 4, 8, 9, 1, 7],
                       [5, 5, 5, 3, 8, 9],
                       [9, 3, 5, 4, 3, 1],
                       [3, 3, 9, 10, 4, 1]], dtype=np.int64)

machines, times = generate_jsp_instance(3, 3, seed=7)
print(machines.tolist(), times.tolist())
# Expected: machines [[0, 2, 1], [0, 1, 2], [0, 2, 1]] and
# times [[12, 47, 81], [31, 34, 28], [72, 26, 99]]. This is the running tiny
# instance below; its optimal makespan is 257 (proven by both exact models and
# confirmed by brute force over all (3!)^3 = 216 machine-sequence selections).
```

The validator below takes only the raw instance and a matrix of start times. It shares
no code with any model: it re-derives job precedence, machine exclusivity, and the
makespan from first principles. Run it after every solver call, exact or heuristic.

```python
import numpy as np


def validate_schedule(machines: np.ndarray, times: np.ndarray, start: np.ndarray,
                      reported_makespan: int | None = None) -> list[str]:
    """Independent feasibility check plus objective recomputation.

    Returns a list of human-readable violations; an empty list means the
    schedule is feasible and the reported makespan (if given) is correct.
    """
    errors: list[str] = []
    n_jobs, n_mach = machines.shape
    end = start + times
    if (start < 0).any():
        errors.append("negative start time")
    for j in range(n_jobs):
        for k in range(1, n_mach):
            if start[j, k] < end[j, k - 1]:
                errors.append(f"job {j}: op {k} starts before op {k - 1} ends")
    for m in range(n_mach):
        js, ks = np.nonzero(machines == m)
        order = np.argsort(start[js, ks], kind="stable")
        s_m, e_m = start[js, ks][order], end[js, ks][order]
        for idx in np.flatnonzero(s_m[1:] < e_m[:-1]):
            errors.append(f"machine {m}: ops of jobs {js[order][idx]} "
                          f"and {js[order][idx + 1]} overlap")
    if reported_makespan is not None and reported_makespan != int(end.max()):
        errors.append(f"reported makespan {reported_makespan} "
                      f"!= recomputed {int(end.max())}")
    return errors


machines = np.array([[0, 2, 1], [0, 1, 2], [0, 2, 1]])
times = np.array([[12, 47, 81], [31, 34, 28], [72, 26, 99]])
start = np.array([[0, 12, 77], [12, 43, 77], [43, 115, 158]])  # an optimal schedule
print(validate_schedule(machines, times, start, 257))
corrupted = start.copy()
corrupted[2, 1] = 100
print(validate_schedule(machines, times, corrupted, 257))
# Expected: first print is [] (feasible, makespan 257 confirmed); second print is
# ['job 2: op 1 starts before op 0 ends', 'machine 2: ops of jobs 1 and 2 overlap']
```

## Exact MIP: the Disjunctive Model in Gurobi

The disjunctive model (Manne 1960) uses continuous starts $s_{j,k}$, one binary
$y_{j_1 j_2 m}$ per unordered pair of jobs on each machine ($y = 1$ iff $j_1$ precedes
$j_2$ on $m$), and a big-M to deactivate one side of each disjunction:

$$
\begin{aligned}
\min\;& C_{\max} \\
\text{s.t.}\;\;
& s_{j,k} \ge s_{j,k-1} + p_{j,k-1} && j \in J,\; k = 2,\dots,m \\
& s_{j_1,k_1} + p_{j_1,k_1} \le s_{j_2,k_2} + M\,(1 - y_{j_1 j_2 m}) && \text{ops } (j_1,k_1), (j_2,k_2) \text{ on } m \\
& s_{j_2,k_2} + p_{j_2,k_2} \le s_{j_1,k_1} + M\, y_{j_1 j_2 m} && \\
& C_{\max} \ge s_{j,m} + p_{j,m} && j \in J
\end{aligned}
$$

$M = \sum_{j,k} p_{j,k}$ is always valid (some semi-active schedule fits in that
horizon). The LP relaxation is weak — with $y$ fractional the big-M terms relax both
disjuncts — which is why the model stalls around 10x10. Build each constraint family
in its own function so every family is unit-testable in isolation.

```python
import numpy as np
import gurobipy as gp


def _stage_of(machines: np.ndarray) -> np.ndarray:
    """k_of[j, m] = index k of the operation of job j that runs on machine m."""
    n_jobs, n_mach = machines.shape
    k_of = np.empty((n_jobs, n_mach), dtype=np.int64)
    k_of[np.repeat(np.arange(n_jobs), n_mach), machines.ravel()] = \
        np.tile(np.arange(n_mach), n_jobs)
    return k_of


def add_precedence_constraints(model: gp.Model, s: gp.tupledict,
                               data: tuple[np.ndarray, np.ndarray]) -> None:
    """Technological route: each operation starts after its job predecessor ends."""
    machines, times = data
    n_jobs, n_mach = machines.shape
    for j in range(n_jobs):
        for k in range(1, n_mach):
            model.addConstr(s[j, k] >= s[j, k - 1] + int(times[j, k - 1]),
                            name=f"prec[{j},{k}]")


def add_disjunctive_constraints(model: gp.Model, s: gp.tupledict, y: gp.tupledict,
                                data: tuple[np.ndarray, np.ndarray],
                                big_m: int) -> None:
    """Machine exclusivity: one big-M pair per unordered job pair per machine."""
    machines, times = data
    n_jobs, n_mach = machines.shape
    k_of = _stage_of(machines)
    for m in range(n_mach):
        for j1 in range(n_jobs):
            for j2 in range(j1 + 1, n_jobs):
                k1, k2 = int(k_of[j1, m]), int(k_of[j2, m])
                model.addConstr(
                    s[j1, k1] + int(times[j1, k1])
                    <= s[j2, k2] + big_m * (1 - y[j1, j2, m]),
                    name=f"disj_fwd[{j1},{j2},{m}]")
                model.addConstr(
                    s[j2, k2] + int(times[j2, k2])
                    <= s[j1, k1] + big_m * y[j1, j2, m],
                    name=f"disj_bwd[{j1},{j2},{m}]")


def add_makespan_constraints(model: gp.Model, s: gp.tupledict, cmax: gp.Var,
                             data: tuple[np.ndarray, np.ndarray]) -> None:
    """C_max bounds the completion time of every job's last operation."""
    machines, times = data
    n_jobs, n_mach = machines.shape
    for j in range(n_jobs):
        model.addConstr(cmax >= s[j, n_mach - 1] + int(times[j, n_mach - 1]),
                        name=f"mksp[{j}]")
```

Assemble, solve, and extract — checking the status before touching `.X`:

```python
import numpy as np
import gurobipy as gp
from gurobipy import GRB


def solve_jsp_mip(machines: np.ndarray, times: np.ndarray,
                  time_limit: float = 60.0) -> tuple[np.ndarray, int, bool]:
    """Disjunctive MIP for JSP. Returns (start times, makespan, proven optimal)."""
    n_jobs, n_mach = machines.shape
    big_m = int(times.sum())                       # valid horizon
    model = gp.Model("jsp_disjunctive")
    model.Params.OutputFlag = 0
    model.Params.TimeLimit = time_limit
    s = model.addVars(n_jobs, n_mach, lb=0.0, ub=big_m, name="s")
    y = model.addVars(
        ((j1, j2, m) for m in range(n_mach)
         for j1 in range(n_jobs) for j2 in range(j1 + 1, n_jobs)),
        vtype=GRB.BINARY, name="y")
    cmax = model.addVar(lb=0.0, ub=big_m, name="cmax")
    data = (machines, times)
    add_precedence_constraints(model, s, data)
    add_disjunctive_constraints(model, s, y, data, big_m)
    add_makespan_constraints(model, s, cmax, data)
    model.setObjective(cmax, GRB.MINIMIZE)
    model.optimize()
    if model.Status == GRB.OPTIMAL or (model.Status == GRB.TIME_LIMIT
                                       and model.SolCount > 0):
        start = np.array([[round(s[j, k].X) for k in range(n_mach)]
                          for j in range(n_jobs)], dtype=np.int64)
        return start, round(cmax.X), model.Status == GRB.OPTIMAL
    raise RuntimeError(f"no incumbent, Gurobi status {model.Status}")


machines, times = generate_jsp_instance(3, 3, seed=7)
start, makespan, proven = solve_jsp_mip(machines, times)
print(makespan, proven, validate_schedule(machines, times, start, makespan))
# Expected: 257 True [] -- proven optimum in well under a second. The same code
# proves ft06's optimum 55 in seconds, but expect hours (or failure) at 10x10:
# ft10 needs the CP-SAT model or the tabu search below.
```

Practical notes. Round extracted starts (`round(s[j,k].X)`) because Gurobi returns
floats within tolerance. Tighter per-pair big-M values from operation heads $r_o$
(longest path from source) and tails $q_o$ (longest path to sink) shrink the relaxation
gap noticeably; see integer-programming-techniques-style tightening in the
milp-modeling-gurobi skill. Warm-start with the tabu solution via `Start` attributes
when you need a proven gap on mid-size instances.

## CP-SAT Interval Model

CP-SAT (OR-Tools) is the practical winner for exact JSP: interval variables give the
solver the scheduling structure explicitly, `AddNoOverlap` triggers strong propagation
(edge finding, not-first/not-last), and lazy clause generation learns conflicts. The
whole model is $nm$ intervals — no big-M, no binary blow-up.

```python
import numpy as np
from ortools.sat.python import cp_model


def solve_jsp_cpsat(machines: np.ndarray, times: np.ndarray,
                    time_limit_s: float = 60.0) -> tuple[np.ndarray, int, str]:
    """JSP via CP-SAT intervals + NoOverlap. Returns (start, makespan, status)."""
    n_jobs, n_mach = machines.shape
    horizon = int(times.sum())
    model = cp_model.CpModel()
    start, end, interval = {}, {}, {}
    for j in range(n_jobs):
        for k in range(n_mach):
            start[j, k] = model.NewIntVar(0, horizon, f"s_{j}_{k}")
            end[j, k] = model.NewIntVar(0, horizon, f"e_{j}_{k}")
            interval[j, k] = model.NewIntervalVar(
                start[j, k], int(times[j, k]), end[j, k], f"iv_{j}_{k}")
    for j in range(n_jobs):                        # technological routes
        for k in range(1, n_mach):
            model.Add(start[j, k] >= end[j, k - 1])
    for m in range(n_mach):                        # one machine, one op at a time
        model.AddNoOverlap([interval[j, k]
                            for j in range(n_jobs) for k in range(n_mach)
                            if machines[j, k] == m])
    makespan = model.NewIntVar(0, horizon, "makespan")
    model.AddMaxEquality(makespan, [end[j, n_mach - 1] for j in range(n_jobs)])
    model.Minimize(makespan)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit_s
    solver.parameters.num_workers = 8              # portfolio search across cores
    status = solver.Solve(model)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        raise RuntimeError(f"CP-SAT status {solver.StatusName(status)}")
    sol = np.array([[solver.Value(start[j, k]) for k in range(n_mach)]
                    for j in range(n_jobs)], dtype=np.int64)
    return sol, int(solver.ObjectiveValue()), solver.StatusName(status)


machines, times = generate_jsp_instance(3, 3, seed=7)
start, makespan, status = solve_jsp_cpsat(machines, times, time_limit_s=10.0)
print(status, makespan, validate_schedule(machines, times, start, makespan))
# Expected: OPTIMAL 257 [] -- matching the MIP. On ft10 (10x10) CP-SAT proves the
# optimum 930 in seconds; the disjunctive MIP typically cannot close that gap.
```

CP-SAT requires integer durations — scale and round real-valued times, and document
the scaling factor. On timeout, `FEASIBLE` plus `solver.BestObjectiveBound()` still
yields a certified gap. For flexible job shops, give each operation one optional
interval per eligible machine plus an `AddExactlyOne` over the presence literals; the
constraint-programming skill covers optional intervals, `AddCumulative`, and search
strategies in depth.

## Critical-Path Tabu Search

For instances beyond exact reach (or sub-second budgets), the dominant metaheuristic
family is tabu search over critical-path neighborhoods — from van Laarhoven, Aarts &
Lenstra (1992) through Nowicki & Smutnicki (1996) to i-TSAB (Nowicki & Smutnicki 2005),
which held best-known values on many Taillard instances for years. The solution
representation is the *selection*: a job order per machine. Two facts make the
neighborhood cheap and safe:

- Only swapping **adjacent critical** operations on a machine can reduce the makespan;
  any move off the critical path is provably non-improving.
- Swapping an adjacent critical pair **never creates a cycle** (van Laarhoven et al.
  1992), so no feasibility check is needed after a move.

First the evaluation core: longest-path start times for a fixed selection (Kahn
topological propagation, $O(nm)$) and extraction of adjacent critical machine pairs.

```python
import numpy as np


def schedule_from_sequences(machines: np.ndarray, times: np.ndarray,
                            seq: np.ndarray) -> tuple[np.ndarray, int] | None:
    """Earliest-start (semi-active) schedule for fixed machine sequences.

    seq[m] lists jobs in processing order on machine m. Returns (start, C_max),
    or None if the selection contains a cycle (infeasible orientation).
    """
    n_jobs, n_mach = machines.shape
    n_ops = n_jobs * n_mach                        # op (j, k) has flat id j*n_mach + k
    k_of = np.empty((n_jobs, n_mach), dtype=np.int64)
    k_of[np.repeat(np.arange(n_jobs), n_mach), machines.ravel()] = \
        np.tile(np.arange(n_mach), n_jobs)
    mach_pred = np.full(n_ops, -1, dtype=np.int64)
    mach_succ = np.full(n_ops, -1, dtype=np.int64)
    for m in range(n_mach):
        ops = seq[m] * n_mach + k_of[seq[m], m]    # flat op ids in machine order
        mach_pred[ops[1:]] = ops[:-1]
        mach_succ[ops[:-1]] = ops[1:]
    p = times.ravel()
    indeg = (mach_pred >= 0).astype(np.int64)
    indeg.reshape(n_jobs, n_mach)[:, 1:] += 1      # job-precedence arcs
    start = np.zeros(n_ops, dtype=np.int64)
    end = np.zeros(n_ops, dtype=np.int64)
    stack = list(np.flatnonzero(indeg == 0))
    scheduled = 0
    while stack:                                   # Kahn topological propagation
        o = stack.pop()
        scheduled += 1
        job_ready = end[o - 1] if o % n_mach else 0
        mach_ready = end[mach_pred[o]] if mach_pred[o] >= 0 else 0
        start[o] = max(job_ready, mach_ready)
        end[o] = start[o] + p[o]
        successors = []
        if o % n_mach != n_mach - 1:
            successors.append(o + 1)
        if mach_succ[o] >= 0:
            successors.append(int(mach_succ[o]))
        for t in successors:
            indeg[t] -= 1
            if indeg[t] == 0:
                stack.append(t)
    if scheduled < n_ops:
        return None                                # cycle: not every op scheduled
    return start.reshape(n_jobs, n_mach), int(end.max())


def critical_pairs(machines: np.ndarray, times: np.ndarray, seq: np.ndarray,
                   start: np.ndarray) -> list[tuple[int, int]]:
    """Adjacent same-machine pairs (machine, position) along one critical path."""
    n_jobs, n_mach = machines.shape
    end = start + times
    k_of = np.empty((n_jobs, n_mach), dtype=np.int64)
    k_of[np.repeat(np.arange(n_jobs), n_mach), machines.ravel()] = \
        np.tile(np.arange(n_mach), n_jobs)
    pos = np.empty((n_mach, n_jobs), dtype=np.int64)   # pos[m, j]: rank of j on m
    pos[np.arange(n_mach)[:, None], seq] = np.arange(n_jobs)
    j, k = divmod(int(np.argmax(end)), n_mach)         # an op finishing at C_max
    pairs: list[tuple[int, int]] = []
    while True:                                        # walk tight predecessors back
        m = int(machines[j, k])
        i = int(pos[m, j])
        if i > 0:
            jp = int(seq[m, i - 1])
            kp = int(k_of[jp, m])
            if end[jp, kp] == start[j, k]:             # machine predecessor is tight
                pairs.append((m, i - 1))
                j, k = jp, kp
                continue
        if k > 0 and end[j, k - 1] == start[j, k]:     # job predecessor is tight
            k -= 1
            continue
        break
    return pairs


seq0 = np.tile(np.arange(6), (6, 1))   # every machine processes jobs 0..5 in order
start0, cmax0 = schedule_from_sequences(FT06_MACHINES, FT06_TIMES, seq0)
print(cmax0, len(critical_pairs(FT06_MACHINES, FT06_TIMES, seq0, start0)))
# Expected: 152 5 -- the naive selection is feasible but poor (optimum is 55),
# and its critical path crosses 5 adjacent same-machine pairs, i.e. 5 candidate moves.
```

The tabu search itself stays small: best-admissible move over critical swaps, a tabu
dict on reversed job pairs, aspiration on the global best, and a slightly randomized
tenure to break limit cycles. Tenure control, frequency-based diversification, and
elite-solution restarts are covered in the tabu-search skill — add them for serious
benchmark work.

```python
import numpy as np

# Uses schedule_from_sequences and critical_pairs from the evaluation block above.


def tabu_search_jsp(machines: np.ndarray, times: np.ndarray, seq0: np.ndarray,
                    iters: int = 3000, tenure: int = 6,
                    seed: int = 0) -> tuple[np.ndarray, int]:
    """Tabu search over adjacent critical swaps (N1 of van Laarhoven et al. 1992).

    seq0 must be a feasible selection (e.g., identity sequences or a
    Giffler-Thompson schedule). Tabu attribute: the reversed (machine, job, job)
    triple. Aspiration: tabu moves that beat the global best are allowed.
    """
    rng = np.random.default_rng(seed)
    seq = seq0.copy()
    start, cmax = schedule_from_sequences(machines, times, seq)
    best_seq, best_cmax = seq.copy(), cmax
    tabu: dict[tuple[int, int, int], int] = {}
    for it in range(iters):
        best_move = None
        for m, i in critical_pairs(machines, times, seq, start):
            a, b = int(seq[m, i]), int(seq[m, i + 1])
            trial = seq.copy()
            trial[m, i], trial[m, i + 1] = b, a
            # Adjacent critical swaps never create a cycle (van Laarhoven et al.
            # 1992), so the evaluation below cannot return None.
            t_start, t_cmax = schedule_from_sequences(machines, times, trial)
            if it < tabu.get((m, b, a), -1) and t_cmax >= best_cmax:
                continue                              # tabu, no aspiration
            if best_move is None or t_cmax < best_move[0]:
                best_move = (t_cmax, trial, t_start, (m, a, b))
        if best_move is None:
            break                                     # all moves tabu (rare): restart
        cmax, seq, start, (m, a, b) = best_move
        tabu[(m, a, b)] = it + tenure + int(rng.integers(0, 4))
        if cmax < best_cmax:
            best_seq, best_cmax = seq.copy(), cmax
    return best_seq, best_cmax


seq0 = np.tile(np.arange(6), (6, 1))
best_seq, best_cmax = tabu_search_jsp(FT06_MACHINES, FT06_TIMES, seq0,
                                      iters=3000, tenure=6, seed=0)
start, recheck = schedule_from_sequences(FT06_MACHINES, FT06_TIMES, best_seq)
print(best_cmax, validate_schedule(FT06_MACHINES, FT06_TIMES, start, recheck))
# Expected: 55 [] -- the proven optimum of ft06 (Fisher & Thompson 1963), reached
# from a naive start in seconds of pure numpy. Always re-validate the best solution.
```

This implementation re-evaluates each trial from scratch at $O(nm)$ per move, which is
fine up to mid-size instances and keeps the code honest. The classic speedup is
Taillard's (1994) head/tail move estimation: keep heads $r_o$ and tails $q_o$ for all
operations and bound a swap's new makespan in $O(1)$, re-evaluating exactly only the
chosen move. That single change plus the N5 neighborhood below is what makes tabu
search competitive on 100x20 instances.

## Advanced Techniques

### Nowicki–Smutnicki block neighborhood (N5)

N1 evaluates every adjacent critical swap; most are provably useless. Nowicki &
Smutnicki (1996, "A fast taboo search algorithm for the job shop problem") restrict
moves to critical **blocks** (maximal machine-consecutive critical runs): inside a
block, only swapping the first two or last two operations can improve the makespan —
interior swaps cannot. Border refinements: in the first block only the last pair
matters, in the last block only the first pair. The result is a neighborhood several
times smaller with no loss of improving moves, which multiplies effective search depth.
Their follow-up i-TSAB (Nowicki & Smutnicki 2005) adds path relinking between elite
solutions and held many Taillard best-known values for a decade. Implement N5 as a
filter on the `critical_pairs` output: group pairs by machine into blocks, keep block
edges only.

### Shifting bottleneck procedure (sketch)

The decomposition classic (Adams, Balas & Zawack 1988): repeatedly identify the most
constraining unsequenced machine via a one-machine relaxation and fix its sequence.

```text
SHIFTING BOTTLENECK (sketch)
S <- {}                              # machines already sequenced
while S != M:
    for each machine m not in S:
        derive heads r_o and tails q_o from longest paths in the partial graph
        solve 1 | r_j, q_j | Cmax on m        # Carlier (1982) B&B, or
                                              # Schrage's heuristic for speed
    b <- machine with the largest one-machine optimum   # the bottleneck
    fix b's optimal sequence; S <- S + {b}
    for each m in S, m != b:                  # local re-optimization
        unfix m, recompute heads/tails, re-solve, re-fix
recompute longest paths after every change
```

Each one-machine problem $1\,|\,r_j, q_j\,|\,C_{\max}$ is itself NP-hard but tiny and
fast in practice. The procedure gives good schedules and excellent intuition, but tabu
search dominates it as a pure heuristic; today its main uses are warm starts and
teaching the bottleneck decomposition pattern.

### Tardiness and other regular objectives

Swap the objective rows; the disjunctive core is untouched. For total weighted
tardiness, drop `cmax` and `add_makespan_constraints` and add tardiness variables:

```python
import numpy as np
import gurobipy as gp
from gurobipy import GRB


def add_tardiness_objective(model: gp.Model, s: gp.tupledict,
                            data: tuple[np.ndarray, np.ndarray],
                            due: np.ndarray, weights: np.ndarray) -> gp.tupledict:
    """Replace the makespan objective with total weighted tardiness."""
    machines, times = data
    n_jobs, n_mach = machines.shape
    tardy = model.addVars(n_jobs, lb=0.0, name="T")    # T_j >= 0 and T_j >= C_j - d_j
    for j in range(n_jobs):
        model.addConstr(
            tardy[j] >= s[j, n_mach - 1] + int(times[j, n_mach - 1]) - int(due[j]),
            name=f"tardy[{j}]")
    model.setObjective(
        gp.quicksum(float(weights[j]) * tardy[j] for j in range(n_jobs)),
        GRB.MINIMIZE)
    return tardy


# Assemble as in solve_jsp_mip, calling this instead of add_makespan_constraints.
# On the 3x3 seed-7 instance with due = [180, 180, 180] and weights = [1, 2, 1],
# the optimal total weighted tardiness is 77 (verified against brute force over
# all 216 sequence selections).
```

In CP-SAT the analogue is `model.AddMaxEquality(t_j, [end_j - d_j, 0])` per job and
minimizing the weighted sum. For tabu search, tardiness stays a longest-path quantity
per job, so critical-path reasoning extends by tracking the critical tree into every
tardy job rather than a single critical path.

### Priority-rule decoders and Giffler–Thompson

The Giffler & Thompson (1960) procedure generates **active** schedules — no operation
can start earlier without delaying another. The optimum is always active, so this is
the right construction space; it doubles as the standard decoder for GA/BRKGA-style
approaches (see decoder-based-representations for random-key variants).

```python
import numpy as np


def giffler_thompson(machines: np.ndarray, times: np.ndarray, rule: str = "mwr",
                     seed: int = 0) -> tuple[np.ndarray, np.ndarray]:
    """Active-schedule construction (Giffler & Thompson 1960) with a priority rule.

    rule: 'mwr' (most work remaining), 'spt' (shortest processing time), or
    'rand' (random tie-breaking, for multi-start). Returns (seq, start).
    """
    rng = np.random.default_rng(seed)
    n_jobs, n_mach = machines.shape
    next_k = np.zeros(n_jobs, dtype=np.int64)          # next unscheduled op per job
    job_ready = np.zeros(n_jobs, dtype=np.int64)
    mach_ready = np.zeros(n_mach, dtype=np.int64)
    work_left = times[:, ::-1].cumsum(axis=1)[:, ::-1] # remaining work from op k on
    start = np.zeros((n_jobs, n_mach), dtype=np.int64)
    seq: list[list[int]] = [[] for _ in range(n_mach)]
    for _ in range(n_jobs * n_mach):
        active = np.flatnonzero(next_k < n_mach)
        k_act = next_k[active]
        m_act = machines[active, k_act]
        est = np.maximum(job_ready[active], mach_ready[m_act])
        ect = est + times[active, k_act]
        i_star = int(np.argmin(ect))                   # earliest possible completion
        m_star = int(m_act[i_star])
        cand = active[(m_act == m_star) & (est < ect[i_star])]   # conflict set
        if rule == "mwr":
            j = int(cand[np.argmax(work_left[cand, next_k[cand]])])
        elif rule == "spt":
            j = int(cand[np.argmin(times[cand, next_k[cand]])])
        else:
            j = int(rng.choice(cand))
        k = int(next_k[j])
        start[j, k] = max(int(job_ready[j]), int(mach_ready[m_star]))
        job_ready[j] = mach_ready[m_star] = start[j, k] + int(times[j, k])
        seq[m_star].append(j)
        next_k[j] += 1
    return np.array(seq, dtype=np.int64), start


seq_gt, start_gt = giffler_thompson(FT06_MACHINES, FT06_TIMES, rule="mwr")
print(int((start_gt + FT06_TIMES).max()))
# Expected: 67 for ft06 with the MWR rule (optimum 55) -- a strong start for tabu
# search; 'spt' gives 94 here, and randomized runs support multi-start strategies.
```

### Lower bounds and gap reporting

Always report a gap, even for heuristics. Cheap bounds: maximum machine load and
maximum job length (both trivial from the data). Stronger: one-machine relaxations
with heads and tails per machine (the shifting-bottleneck subproblems), or simply the
`BestObjectiveBound()` from a truncated CP-SAT run — a few seconds of CP-SAT usually
yields a far better bound than any hand-computed relaxation, and the same run warm-
starts your comparison table.

## Practical Challenges

**The disjunctive MIP stalls with a huge gap beyond 10x10.** This is expected, not a
bug: the big-M LP relaxation is structurally weak (Ku & Beck 2016). Tighten per-pair
big-Ms with heads and tails, warm-start from tabu search, and accept that the right
fix is usually switching to CP-SAT for the proof and keeping the MIP only when side
constraints or duals demand it.

**Tabu search oscillates among equal-makespan solutions and stops improving.** Plain
N1/N5 with short tenure cycles through plateaus. Randomize the tenure (as in the code
above), add frequency-based penalties on repeated moves, and restart from elite
solutions with a perturbed selection. The tabu-search skill covers these long-term
memory mechanisms.

**CP-SAT returns a different schedule than the start times you reconstructed from its
sequences.** Two schedules can share sequences but differ in start times: CP-SAT may
return non-semi-active starts when multiple optima exist. Canonicalize by extracting
only the machine sequences, then recomputing semi-active starts with
`schedule_from_sequences` — for regular objectives this never worsens the objective.

**Jobs that skip machines or visit one twice break the `(n_jobs, n_machines)` matrix
layout.** Generalize the data structure to per-job operation lists before modeling
anything; the matrix layout here exploits the classical every-machine-once assumption.
Recirculation also breaks the one-binary-per-job-pair MIP indexing — index disjunctive
binaries by operation pair instead. CP-SAT needs no structural change.

**The validator passes but results disagree with published optima.** Check instance
parsing first: OR-Library and Taillard files disagree on machine indexing (0-based vs
1-based) and on row meaning (machine row vs duration row interleaving). Regression-test
the parser on `ft06` = 55 before trusting any benchmark table.

**Floating-point processing times.** CP-SAT rejects them and the MIP suffers numerics
with big-M. Multiply by a power of ten, round, and solve in integers; report the
scaling factor with the results. Keep durations well under $10^7$ after scaling so
horizon-sized sums stay safely within integer ranges.

**Makespan-optimal schedules are brittle in practice.** A schedule with zero slack
everywhere collapses under the first delay. Re-optimize with a secondary objective
(weighted tardiness against internal due dates, or total flow time) within a small
makespan tolerance, or move to the rolling-horizon re-solve pattern with CP-SAT and a
short time limit.

## Tools & Libraries

| Library / resource | When to use | Note |
|---|---|---|
| OR-Tools CP-SAT (`ortools`) | Default exact JSP engine | Free; integer durations; portfolio-parallel; certified bounds on timeout |
| `gurobipy` | Disjunctive MIP, tardiness MIPs, matheuristics | License required; weak LP at scale — pair with warm starts |
| `numpy` | Evaluators, tabu search, decoders, instance generation | The longest-path evaluator is the hot loop: keep it array-based |
| `networkx` | Disjunctive-graph prototyping, longest-path debugging | Clear but slow; switch to arrays for search loops |
| `pandas` | Run/result tables across instances and seeds | One row per (instance, algorithm, seed) run |
| `matplotlib` | Gantt charts and convergence plots | A Gantt chart catches modeling errors no table reveals |
| OR-Library, Taillard sets | Benchmarks: `ft06`/`ft10`/`la01-40`/`ta01-80` | Known optima/best-known values enable honest gap reporting |

## Output Format

A complete JSP answer contains:

1. **Model and run summary** — one table, no prose substitutes:

   | Field | Example |
   |---|---|
   | Instance | ft06 (6 jobs, 6 machines, 36 ops) |
   | Method | CP-SAT intervals |
   | Status | OPTIMAL |
   | Makespan | 55 |
   | Best bound | 55 |
   | Gap | 0.0% |
   | Wall time | 0.1 s |
   | Seed / params | n/a (exact) |

2. **The schedule itself** — per-machine job sequences plus a start-time matrix (or a
   tidy table with columns `job, op, machine, start, end`), not just the objective
   value. A Gantt chart artifact for any instance a human will inspect.
3. **Independent validation line** — explicit confirmation that `validate_schedule`
   returned zero violations on the reported start times, with the recomputed objective.
4. **Gap statement** — against the proven bound (exact) or the best-known/lower bound
   (heuristic), with the bound's source named.
5. **Reproducibility block** — seeds, parameter values (`iters`, `tenure`, time
   limits), library versions, and the instance generator call or file checksum.
6. **For heuristic comparisons** — multiple seeds per instance with best/mean/std and
   time-to-best, never a single lucky run; see algorithm-benchmarking practice in the
   related skills.

## Questions to Ask

- Does every job visit every machine exactly once, in a fixed order? Any recirculation
  or skipped machines?
- Can any operation run on more than one machine (flexible job shop)?
- Which objective: makespan, total weighted tardiness, or several at once?
- Are there release dates, due dates, sequence-dependent setups, or transport times?
- Are processing times integers, or do they need scaling?
- What instance sizes and what time budget per solve?
- Is a proof of optimality (or a certified gap) required, or is best-effort acceptable?
- Is a Gurobi license available, or should everything run on free solvers?
- Is this a one-off solve or a rolling re-optimization where schedule stability matters?
- Are results compared against published benchmarks, and which bound source defines
  the reported gap?

## Related Skills

- **constraint-programming** — when the CP-SAT model needs depth: optional intervals
  for flexible job shops, cumulative resources, channeling, and search strategies.
- **tabu-search** — when tuning tenure, aspiration, frequency-based diversification,
  or elite restarts beyond the critical-path implementation given here.
- **decoder-based-representations** — when building GA/BRKGA approaches on random keys
  or priority rules with schedule-generation schemes as decoders.
- **flow-shop-scheduling** — when all jobs share one machine order; the permutation
  structure unlocks NEH construction and iterated greedy.
- **milp-modeling-gurobi** — when extending the disjunctive MIP with side constraints,
  parameter tuning, warm starts, or solution pools.
- **parallel-machine-scheduling** — when operations choose among machine pools (the
  assignment layer of flexible job shops) or for single-machine due-date results.
