---
name: assignment-problems
description: When the user wants to match agents to tasks at minimum cost - linear assignment via the Hungarian algorithm, LP duality, or linear_sum_assignment; generalized assignment (GAP) via MIP, Lagrangian relaxation, and local search; bottleneck (min-max) assignment. Also use when the user mentions "assignment problem," "Hungarian algorithm," "generalized assignment," "GAP," "linear_sum_assignment," "matching," or when each task needs one agent under capacity limits. For flow formulations, see network-flow-optimization; for interaction costs between assigned pairs, see quadratic-assignment-problem.
---

# Assignment Problems

You are an expert in assignment problems: linear assignment (LAP), generalized
assignment (GAP), and bottleneck assignment. This skill covers exact methods
(Hungarian algorithm, LP with total unimodularity, MIP), Lagrangian bounds,
and local-search heuristics, plus instance generation and independent solution
validation. Use the framework below to classify the variant, pick the cheapest
adequate method, implement it, and verify the result.

## Initial Assessment

Establish these points before formulating or recommending a method:

- **Cardinality structure.** One agent per task and one task per agent
  (one-to-one, LAP)? Or can one agent take several tasks subject to a
  capacity (many-to-one, GAP)? This single distinction separates a
  polynomial problem from an NP-hard one.
- **Objective sense and shape.** Minimize total cost, maximize total profit,
  or minimize the worst single cost (bottleneck)? Mixed conventions are the
  most common source of wrong answers; fix the sense first.
- **Sizes.** Number of agents m, tasks n. LAP with n up to ~10,000 is
  routine for `scipy.optimize.linear_sum_assignment`. GAP with m·n up to
  ~10^5 binaries is usually fine for a MIP solver; beyond that plan for
  Lagrangian bounds plus a heuristic.
- **Balanced or rectangular.** Equal numbers on both sides? If not, decide
  whether unmatched rows/columns are allowed and what they cost.
- **Forbidden pairs.** Are some (agent, task) combinations disallowed? Plan
  to encode them as `np.inf` (scipy) or by omitting variables (MIP), not as
  fragile big-M costs.
- **Resource data type (GAP).** Integer resource consumptions enable
  knapsack DP in the Lagrangian subproblems; float data must be scaled or
  the subproblems solved as small MIPs.
- **Solve count.** One-off solve, or LAP/GAP called thousands of times
  inside a heuristic or branch-and-bound loop? The embedded case changes
  the tooling (warm starts, C-backed LAP libraries, candidate lists).
- **Solver availability.** Gurobi license present? If not, scipy +
  open-source MIP (HiGHS) covers everything in this skill.
- **Optimality requirement.** LAP and bottleneck are always exact. For GAP,
  ask whether a proven optimum is required or a bounded-gap heuristic
  solution within a time budget suffices.
- **Validation path.** Agree up front that every reported solution passes an
  independent feasibility and objective check (provided below).

## Problem Variants and Formulation

### Linear assignment problem (LAP)

Given an n×n cost matrix C = (c_ij), choose a permutation assigning each row
to exactly one column:

$$
\min \sum_{i=1}^{n}\sum_{j=1}^{n} c_{ij}\, x_{ij}
\quad \text{s.t.} \quad
\sum_{j} x_{ij} = 1 \;\; \forall i, \qquad
\sum_{i} x_{ij} = 1 \;\; \forall j, \qquad
x_{ij} \ge 0 .
$$

No integrality constraints are written, and none are needed. The constraint
matrix is the node-edge incidence matrix of a bipartite graph, which is
**totally unimodular**: every square submatrix has determinant in {-1, 0, +1},
so every basic feasible solution of the LP is integral. Equivalently, the
extreme points of the feasible polytope (the Birkhoff polytope of doubly
stochastic matrices) are exactly the permutation matrices (Birkhoff 1946).
The Hungarian method (Kuhn 1955; Munkres 1957) is therefore a primal-dual LP
algorithm: it keeps dual potentials u_i, v_j with u_i + v_j ≤ c_ij and grows
a matching on tight edges; at optimality Σu + Σv equals the optimal cost.
Modern dense implementations follow Jonker & Volgenant (1987), O(n³).

### Bottleneck assignment problem

Same feasible set, different objective: minimize the largest cost used,

$$
\min_{x} \; \max \{\, c_{ij} : x_{ij} = 1 \,\}.
$$

Use it when the slowest pairing determines system performance (parallel
workers, latest completion time, worst-case latency). Threshold search solves
it exactly: the optimum is one of the O(n²) distinct cost values, and a
threshold t is feasible iff the edges with c_ij ≤ t admit a perfect matching.
Hopcroft-Karp gives ~O(n^2.5 log n); faster methods exist (Gabow & Tarjan 1988).

### Generalized assignment problem (GAP)

Agents I = {1,…,m} with capacities b_i; jobs J = {1,…,n}. Agent i spends
resource a_ij and cost c_ij on job j:

$$
\min \sum_{i \in I}\sum_{j \in J} c_{ij}\, x_{ij}
$$

$$
\sum_{i \in I} x_{ij} = 1 \quad \forall j \in J
\qquad \text{(each job done by exactly one agent)}
$$

$$
\sum_{j \in J} a_{ij}\, x_{ij} \le b_i \quad \forall i \in I
\qquad \text{(agent capacity)}, \qquad x_{ij} \in \{0,1\}.
$$

The capacity constraints destroy total unimodularity: the LP relaxation is
fractional, the problem is NP-hard, and even *deciding feasibility* is
NP-complete (Martello & Toth 1990, *Knapsack Problems*, ch. 7). Much of the
literature states GAP as profit maximization; convert with
c'_ij = max_kl(c_kl) − c_ij and keep one convention throughout your code.
LAP is the special case m = n, a_ij = 1, b_i = 1 with equality capacities.

### Method selection

| Situation | Method |
|---|---|
| One-to-one, dense costs, n ≤ ~10^4 | `scipy.optimize.linear_sum_assignment` |
| One-to-one, sparse costs | `scipy.sparse.csgraph.min_weight_full_bipartite_matching` |
| One-to-one, need duals / sensitivity | LP in gurobipy, read `Pi` (or own Hungarian potentials) |
| Min-max fairness objective | Bottleneck threshold search |
| Many-to-one with capacities, moderate size | GAP MIP in gurobipy |
| GAP, large or time-boxed | Lagrangian bound + local search / ejection chains |
| Costs depend on *pairs* of assignments | Not LAP/GAP — see quadratic-assignment-problem |
| Assignment is a subproblem of a flow network | See network-flow-optimization (min-cost flow) |

## Linear and Bottleneck Assignment

### scipy: the default LAP tool

`linear_sum_assignment` implements a Jonker-Volgenant-type shortest
augmenting path algorithm in C. It handles rectangular matrices (every row
matched when rows ≤ columns), maximization, and `np.inf` for forbidden pairs.

```python
import numpy as np
from scipy.optimize import linear_sum_assignment


def solve_lap(cost: np.ndarray, maximize: bool = False) -> tuple[np.ndarray, np.ndarray, float]:
    """Solve a (possibly rectangular) LAP with scipy's JV-type solver.

    Returns (rows, cols, total); row rows[k] is matched to column cols[k].
    np.inf entries mark forbidden pairs; scipy raises ValueError when no
    feasible complete assignment exists.
    """
    rows, cols = linear_sum_assignment(cost, maximize=maximize)
    return rows, cols, float(cost[rows, cols].sum())


cost = np.array([[4.0, 1.0, 3.0],
                 [2.0, 0.0, 5.0],
                 [3.0, 2.0, 2.0]])
print(solve_lap(cost))
# Expected: rows [0 1 2], cols [1 0 2], total 5.0

forbidden = cost.copy()
forbidden[0, 1] = np.inf                  # row 0 may not take column 1
print(solve_lap(forbidden))
# Expected: total 6.0 (two optimal supports exist for this matrix)

tasks = np.array([[9.0, 4.0, 6.0, 2.0],
                  [3.0, 8.0, 5.0, 7.0]])  # 2 workers, 4 tasks: rectangular
rows, cols, total = solve_lap(tasks)
print(rows, cols, total)
# Expected: both rows matched to distinct columns, total 5.0 (2.0 + 3.0)
```

### A reference Hungarian implementation

Owning a transparent O(n³) implementation is useful when you must instrument
the algorithm (extract potentials, warm-start, embed where C extensions are
unavailable). This is the shortest-augmenting-path variant; costs must be finite.

```python
import numpy as np


def hungarian(cost: np.ndarray) -> tuple[np.ndarray, float]:
    """Solve a square LAP by shortest augmenting paths, O(n^3).

    Maintains dual potentials u (rows) and v (columns) with
    u[i] + v[j] <= cost[i, j]; augments one row per outer iteration.
    Returns (col_of_row, total cost). Requires finite costs.
    """
    n = cost.shape[0]
    INF = float("inf")
    u = np.zeros(n + 1)                      # row potentials (1-based)
    v = np.zeros(n + 1)                      # column potentials (1-based)
    p = np.zeros(n + 1, dtype=int)           # p[j]: row matched to column j
    way = np.zeros(n + 1, dtype=int)         # alternating-path predecessors
    for i in range(1, n + 1):
        p[0] = i
        j0 = 0
        minv = np.full(n + 1, INF)
        used = np.zeros(n + 1, dtype=bool)
        while True:                          # Dijkstra over reduced costs
            used[j0] = True
            i0, delta, j1 = p[j0], INF, 0
            for j in range(1, n + 1):
                if not used[j]:
                    cur = cost[i0 - 1, j - 1] - u[i0] - v[j]
                    if cur < minv[j]:
                        minv[j], way[j] = cur, j0
                    if minv[j] < delta:
                        delta, j1 = minv[j], j
            for j in range(n + 1):           # dual update keeps feasibility
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta
            j0 = j1
            if p[j0] == 0:                   # reached an unmatched column
                break
        while j0:                            # flip the augmenting path
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1
    col_of_row = np.zeros(n, dtype=int)
    for j in range(1, n + 1):
        col_of_row[p[j] - 1] = j - 1
    total = float(cost[np.arange(n), col_of_row].sum())
    return col_of_row, total


cost = np.array([[4.0, 1.0, 3.0],
                 [2.0, 0.0, 5.0],
                 [3.0, 2.0, 2.0]])
print(hungarian(cost))
# Expected: col_of_row [1 0 2], total 5.0 (matches scipy)
```

### LAP as a pure LP: total unimodularity in action

Solving the LAP with *continuous* variables demonstrates the integrality
guarantee and exposes the duals, which are exactly the Hungarian potentials.
Use the simplex method so the reported solution is a vertex (barrier without
crossover can return a fractional interior point of an optimal face).

```python
import gurobipy as gp
from gurobipy import GRB
import numpy as np


def solve_lap_lp(cost: np.ndarray) -> tuple[np.ndarray, float]:
    """Solve the assignment problem as a pure LP.

    Total unimodularity of the bipartite incidence matrix guarantees an
    integral optimal vertex, so binary variables are unnecessary.
    Returns (col_of_row, optimal value).
    """
    n = cost.shape[0]
    model = gp.Model("lap_lp")
    model.Params.OutputFlag = 0
    model.Params.Method = 0                  # primal simplex -> vertex solution
    x = model.addVars(n, n, lb=0.0, ub=1.0, name="x")
    model.setObjective(
        gp.quicksum(cost[i, j] * x[i, j] for i in range(n) for j in range(n)),
        GRB.MINIMIZE,
    )
    row_c = model.addConstrs((x.sum(i, "*") == 1 for i in range(n)), name="row")
    col_c = model.addConstrs((x.sum("*", j) == 1 for j in range(n)), name="col")
    model.optimize()
    if model.Status != GRB.OPTIMAL:
        raise RuntimeError(f"unexpected LP status {model.Status}")
    sol = np.array([[x[i, j].X for j in range(n)] for i in range(n)])
    assert np.allclose(sol, sol.round()), "TU guarantees an integral vertex"
    col_of_row = sol.argmax(axis=1)
    # The LP duals are Hungarian potentials: u[i] + v[j] <= c[i, j], tight on
    # assigned pairs (complementary slackness); their sum equals the optimum.
    u = np.array([row_c[i].Pi for i in range(n)])
    v = np.array([col_c[j].Pi for j in range(n)])
    assert abs(u.sum() + v.sum() - model.ObjVal) < 1e-6
    return col_of_row, float(model.ObjVal)


cost = np.array([[4.0, 1.0, 3.0],
                 [2.0, 0.0, 5.0],
                 [3.0, 2.0, 2.0]])
print(solve_lap_lp(cost))
# Expected: col_of_row [1 0 2], objective 5.0, both asserts pass
```

### Bottleneck assignment by threshold search

```python
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import maximum_bipartite_matching


def bottleneck_assignment(cost: np.ndarray) -> tuple[np.ndarray, float]:
    """Solve the bottleneck (min-max) assignment problem exactly.

    Binary search over the sorted distinct cost values; feasibility of a
    threshold t is a perfect-matching test on edges with cost <= t
    (Hopcroft-Karp via scipy). Returns (col_of_row, bottleneck value).
    """
    n = cost.shape[0]
    values = np.unique(cost)
    lo, hi = 0, values.size - 1
    best_match: np.ndarray | None = None
    best_val = float("inf")
    while lo <= hi:
        mid = (lo + hi) // 2
        graph = csr_matrix(cost <= values[mid])
        match = maximum_bipartite_matching(graph, perm_type="column")
        if (match >= 0).all():               # perfect matching exists
            best_match, best_val = match.copy(), float(values[mid])
            hi = mid - 1
        else:
            lo = mid + 1
    if best_match is None:
        raise ValueError("no perfect matching exists (forbidden pairs block all)")
    return best_match.astype(int), best_val


cost = np.array([[3.0, 8.0, 6.0],
                 [2.0, 4.0, 9.0],
                 [7.0, 5.0, 1.0]])
col_of_row, value = bottleneck_assignment(cost)
print(col_of_row, value)
# Expected: col_of_row [0 1 2], bottleneck value 4.0
# (threshold 3 fails: rows 0 and 1 would both need column 0)
```

## Generalized Assignment: Exact MIP, Instances, Validation

### Exact MIP with explicit constraint builders

Keep each constraint family in its own named builder function. This makes the
model auditable, testable in isolation, and easy to extend (e.g., adding
assignment restrictions or multiple resources later).

```python
import gurobipy as gp
from gurobipy import GRB
import numpy as np


def add_job_assignment_constraints(model: gp.Model, x: gp.tupledict,
                                   n_agents: int, n_jobs: int) -> None:
    """Every job is assigned to exactly one agent."""
    model.addConstrs(
        (gp.quicksum(x[i, j] for i in range(n_agents)) == 1 for j in range(n_jobs)),
        name="assign",
    )


def add_capacity_constraints(model: gp.Model, x: gp.tupledict,
                             a: np.ndarray, b: np.ndarray) -> None:
    """Resource consumed on each agent stays within its capacity."""
    m, n = a.shape
    model.addConstrs(
        (gp.quicksum(a[i, j] * x[i, j] for j in range(n)) <= b[i] for i in range(m)),
        name="capacity",
    )


def build_gap_model(cost: np.ndarray, a: np.ndarray,
                    b: np.ndarray) -> tuple[gp.Model, gp.tupledict]:
    """Assemble the min-cost GAP MIP from its constraint builders."""
    m, n = cost.shape
    model = gp.Model("gap")
    model.Params.OutputFlag = 0
    x = model.addVars(m, n, vtype=GRB.BINARY, name="x")
    model.setObjective(
        gp.quicksum(cost[i, j] * x[i, j] for i in range(m) for j in range(n)),
        GRB.MINIMIZE,
    )
    add_job_assignment_constraints(model, x, m, n)
    add_capacity_constraints(model, x, a, b)
    return model, x


def solve_gap_mip(cost: np.ndarray, a: np.ndarray, b: np.ndarray,
                  time_limit: float = 60.0) -> tuple[np.ndarray, float, float]:
    """Solve GAP to optimality or time limit.

    Returns (assign, objective, mip_gap) where assign[j] is job j's agent.
    """
    m, n = cost.shape
    model, x = build_gap_model(cost, a, b)
    model.Params.TimeLimit = time_limit
    model.Params.MIPGap = 1e-6
    model.optimize()
    solved = model.Status == GRB.OPTIMAL or (
        model.Status == GRB.TIME_LIMIT and model.SolCount > 0
    )
    if not solved:
        raise RuntimeError(f"no solution: status {model.Status}")
    assign = np.array(
        [max(range(m), key=lambda i: x[i, j].X) for j in range(n)], dtype=int
    )
    return assign, float(model.ObjVal), float(model.MIPGap)


cost = np.array([[8.0, 6.0, 5.0, 7.0],
                 [6.0, 7.0, 8.0, 5.0]])
a = np.array([[3, 2, 4, 3],
              [3, 3, 3, 2]])
b = np.array([7, 6])
assign, obj, gap = solve_gap_mip(cost, a, b)
print(assign, obj, gap)
# Expected: assign [1 0 0 1], objective 22.0, gap 0.0
# (every job at its cheapest agent happens to fit: loads 6 <= 7 and 5 <= 6)
```

### Instance generator with seeds

The standard GAP test classes come from Chu & Beasley (1997), "A genetic
algorithm for the generalised assignment problem". Class difficulty rises
from C to E because cost and resource become inversely correlated: cheap
assignments consume more capacity, so greedy choices fight the capacities.

```python
import numpy as np


def generate_gap_instance(n_agents: int, n_jobs: int, gap_class: str = "c",
                          seed: int = 0) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Generate a min-cost GAP instance (cost, a, b), Chu-Beasley classes.

    'c': independent uniform cost and resource.
    'd': cost = 111 - a + noise (inverse correlation, hard).
    'e': resource log-distributed, cost ~ 1000/a (hardest).
    Capacities are 80% of average load; feasibility is NOT guaranteed by
    construction (GAP feasibility itself is NP-complete) - let the solver
    or validator detect infeasible draws.
    """
    rng = np.random.default_rng(seed)
    if gap_class == "c":
        a = rng.integers(5, 26, size=(n_agents, n_jobs))
        cost = rng.integers(10, 51, size=(n_agents, n_jobs))
    elif gap_class == "d":
        a = rng.integers(1, 101, size=(n_agents, n_jobs))
        cost = 111 - a + rng.integers(-10, 11, size=(n_agents, n_jobs))
    elif gap_class == "e":
        u = rng.random((n_agents, n_jobs))
        a = np.maximum(1, (1.0 - 10.0 * np.log(u)).astype(int))
        cost = np.maximum(1, (1000.0 / a - 10.0 * rng.random((n_agents, n_jobs))).astype(int))
    else:
        raise ValueError(f"unknown gap_class {gap_class!r}")
    b = np.maximum(
        np.ceil(0.8 * a.sum(axis=1) / n_agents).astype(int),
        a.max(axis=1),                       # each job must fit somewhere alone
    )
    return cost.astype(float), a.astype(int), b.astype(int)


cost, a, b = generate_gap_instance(3, 12, "c", seed=42)
print(cost.shape, a.shape, b)
# Expected: (3, 12) (3, 12) and a 3-entry capacity vector near
# 0.8 * (row resource sum) / 3, e.g. around 45-55 for these parameters
```

### Independent feasibility and objective validator

Never report a solution straight from a solver or heuristic. Recompute
feasibility and objective from the raw data with code that shares nothing
with the model. This catches indexing bugs, sense errors, and stale data.

```python
import numpy as np


def validate_lap_solution(col_of_row: np.ndarray, cost: np.ndarray) -> float:
    """Check a square-LAP solution is a permutation; return recomputed cost."""
    n = cost.shape[0]
    if sorted(col_of_row.tolist()) != list(range(n)):
        raise ValueError("not a permutation: a column is reused or missing")
    return float(cost[np.arange(n), col_of_row].sum())


def validate_gap_solution(assign: np.ndarray, cost: np.ndarray, a: np.ndarray,
                          b: np.ndarray) -> tuple[bool, float, list[str]]:
    """Independent feasibility + objective check for a GAP solution.

    assign[j] is the agent of job j. Recomputes loads and cost from raw
    data only. Returns (feasible, objective, issue messages).
    """
    m, n = cost.shape
    issues: list[str] = []
    if assign.shape != (n,):
        return False, float("nan"), [f"assign shape {assign.shape} != ({n},)"]
    if ((assign < 0) | (assign >= m)).any():
        return False, float("nan"), ["agent index out of range"]
    jobs = np.arange(n)
    load = np.bincount(assign, weights=a[assign, jobs], minlength=m)
    for i in np.flatnonzero(load > b + 1e-9):
        issues.append(f"agent {i}: load {load[i]:.0f} > capacity {b[i]:.0f}")
    objective = float(cost[assign, jobs].sum())
    return not issues, objective, issues


cost = np.array([[8.0, 6.0, 5.0, 7.0],
                 [6.0, 7.0, 8.0, 5.0]])
a = np.array([[3, 2, 4, 3], [3, 3, 3, 2]])
b = np.array([7, 6])
print(validate_gap_solution(np.array([1, 0, 0, 1]), cost, a, b))
# Expected: (True, 22.0, [])
print(validate_gap_solution(np.array([0, 0, 0, 0]), cost, a, b))
# Expected: (False, 26.0, ['agent 0: load 12 > capacity 7'])
```

## Generalized Assignment: Lagrangian Bound and Local Search

### Lagrangian relaxation with knapsack subproblems

Dualize the job-assignment equalities with unrestricted multipliers λ_j.
The relaxed problem separates by agent:

$$
L(\lambda) \;=\; \sum_{j} \lambda_j \;+\;
\sum_{i \in I} \min \Big\{ \sum_{j} (c_{ij} - \lambda_j)\, x_{ij}
\;:\; \sum_{j} a_{ij} x_{ij} \le b_i,\; x_{ij} \in \{0,1\} \Big\},
$$

one 0-1 knapsack per agent (select the items with negative reduced cost,
subject to capacity). L(λ) ≤ optimal GAP cost for every λ, and the best
Lagrangian bound equals the bound of the convexified problem, which is at
least as strong as the LP relaxation (Fisher 1981, "The Lagrangian
relaxation method for solving integer programming problems"). Maximize L
by subgradient ascent; recover feasible solutions by repairing the relaxed
ones. For step-size rules, stabilization, and the general machinery, see
**lagrangian-relaxation**.

```python
import numpy as np


def solve_knapsack_min_reduced_cost(red_cost: np.ndarray, weight: np.ndarray,
                                    capacity: int) -> np.ndarray:
    """Pick a job subset minimizing total reduced cost under one capacity.

    Equivalent to a max-knapsack on profits -red_cost (items with
    non-negative reduced cost are never beneficial). DP over capacity,
    O(n * capacity), vectorized over the capacity axis. Returns a boolean
    take-vector.
    """
    n = red_cost.size
    profit = -red_cost
    dp = np.zeros(capacity + 1)
    keep = np.zeros((n, capacity + 1), dtype=bool)
    for k in range(n):
        p, w = profit[k], int(weight[k])
        if p <= 0 or w > capacity:
            continue
        cand = dp.copy()
        cand[w:] = dp[: capacity + 1 - w] + p
        take = cand > dp
        keep[k] = take
        dp = np.where(take, cand, dp)
    take_vec = np.zeros(n, dtype=bool)
    c = capacity
    for k in range(n - 1, -1, -1):           # standard DP backtrack
        if keep[k, c]:
            take_vec[k] = True
            c -= int(weight[k])
    return take_vec


def repair_to_feasible(X: np.ndarray, cost: np.ndarray, a: np.ndarray,
                       b: np.ndarray) -> np.ndarray | None:
    """Turn a relaxed (per-agent) solution into a feasible assignment.

    Keeps each claimed job at its cheapest claiming agent if it fits, then
    greedily inserts the rest, hardest-to-place jobs first. Returns None
    when the greedy insertion gets stuck.
    """
    m, n = cost.shape
    assign = np.full(n, -1, dtype=int)
    load = np.zeros(m)
    for j in np.flatnonzero(X.sum(axis=0) >= 1):
        claimants = np.flatnonzero(X[:, j])
        i = claimants[np.argmin(cost[claimants, j])]
        if load[i] + a[i, j] <= b[i]:
            assign[j] = i
            load[i] += a[i, j]
    rest = np.flatnonzero(assign < 0)
    rest = rest[np.argsort(-a[:, rest].min(axis=0))]
    for j in rest:
        feasible = np.flatnonzero(load + a[:, j] <= b)
        if feasible.size == 0:
            return None
        i = feasible[np.argmin(cost[feasible, j])]
        assign[j] = i
        load[i] += a[i, j]
    return assign


def gap_lagrangian(cost: np.ndarray, a: np.ndarray, b: np.ndarray,
                   n_iters: int = 300) -> tuple[float, float, np.ndarray | None]:
    """Subgradient optimization of the GAP Lagrangian dual.

    Polyak-type step toward the incumbent upper bound; the step parameter
    theta halves after 20 iterations without dual improvement. Returns
    (best lower bound, best upper bound, best feasible assignment).
    """
    m, n = cost.shape
    lam = cost.min(axis=0).astype(float)     # start: column minima
    best_lb, best_ub = -np.inf, np.inf
    best_assign: np.ndarray | None = None
    theta, stall = 2.0, 0
    for _ in range(n_iters):
        X = np.zeros((m, n), dtype=bool)
        for i in range(m):
            X[i] = solve_knapsack_min_reduced_cost(cost[i] - lam, a[i], int(b[i]))
        lb = lam.sum() + ((cost - lam[None, :]) * X).sum()
        if lb > best_lb + 1e-9:
            best_lb, stall = lb, 0
        else:
            stall += 1
            if stall >= 20:
                theta, stall = theta / 2.0, 0
        assign = repair_to_feasible(X, cost, a, b)
        if assign is not None:
            ub = float(cost[assign, np.arange(n)].sum())
            if ub < best_ub:
                best_ub, best_assign = ub, assign.copy()
        g = 1.0 - X.sum(axis=0)              # subgradient of the dualized rows
        norm2 = float(g @ g)
        if norm2 < 1e-12 or best_ub - best_lb < 1e-6:
            break
        target = best_ub if np.isfinite(best_ub) else lb + abs(lb) + 1.0
        lam += theta * (target - lb) / norm2 * g
    return best_lb, best_ub, best_assign


cost = np.array([[8.0, 6.0, 5.0, 7.0],
                 [6.0, 7.0, 8.0, 5.0]])
a = np.array([[3, 2, 4, 3], [3, 3, 3, 2]])
b = np.array([7, 6])
lb, ub, assign = gap_lagrangian(cost, a, b)
print(lb, ub, assign)
# Expected: ub 22.0 with assign [1 0 0 1] (optimal); lb converges to ~22,
# closing the duality gap on this easy instance
```

Practical notes: the starting value Σ_j min_i c_ij (column minima) is the
classic weak bound; subgradient ascent improves it fast for ~50 iterations,
then crawls — stop early and spend the time in the primal heuristic. On
loosely capacitated instances the LP bound is nearly as good and far cheaper.

### Local search metaheuristic (vectorized)

A multi-start best-improvement *shift* descent on a penalized objective is
the standard GAP workhorse and the inner loop of stronger methods; all m·n
shift moves are scored in one vectorized pass. For neighborhood design and
delta-evaluation trade-offs see **local-search-and-neighborhoods**; the
high-end extension is ejection-chain tabu search (Yagiura, Ibaraki & Glover 2004).

```python
import numpy as np


def gap_local_search(cost: np.ndarray, a: np.ndarray, b: np.ndarray,
                     n_restarts: int = 20, seed: int = 0,
                     rho: float = 1000.0) -> tuple[np.ndarray, float]:
    """Multi-start best-improvement shift descent for min-cost GAP.

    Penalized objective: cost + rho * total capacity excess. Each
    iteration scores all (agent, job) shift moves as one (m, n) delta
    matrix. Returns (assign, penalized objective of the best restart).
    """
    rng = np.random.default_rng(seed)
    m, n = cost.shape
    jobs = np.arange(n)

    def loads(assign: np.ndarray) -> np.ndarray:
        return np.bincount(assign, weights=a[assign, jobs], minlength=m).astype(float)

    def penalized(assign: np.ndarray) -> float:
        excess = np.maximum(loads(assign) - b, 0.0).sum()
        return float(cost[assign, jobs].sum() + rho * excess)

    best_assign, best_val = None, np.inf
    for _ in range(n_restarts):
        assign = rng.integers(0, m, size=n)
        load = loads(assign)
        while True:
            cur_excess = np.maximum(load - b, 0.0)
            # Move job j from s = assign[j] to agent i: delta has shape (m, n).
            d_cost = cost - cost[assign, jobs][None, :]
            d_add = (np.maximum(load[:, None] + a - b[:, None], 0.0)
                     - cur_excess[:, None])
            src_after = load[assign] - a[assign, jobs]
            d_rem = np.maximum(src_after - b[assign], 0.0) - cur_excess[assign]
            delta = d_cost + rho * (d_add + d_rem[None, :])
            delta[assign, jobs] = 0.0        # null moves
            i_best, j_best = np.unravel_index(np.argmin(delta), delta.shape)
            if delta[i_best, j_best] > -1e-9:
                break                        # local optimum reached
            s = assign[j_best]
            load[s] -= a[s, j_best]
            load[i_best] += a[i_best, j_best]
            assign[j_best] = i_best
        val = penalized(assign)
        if val < best_val:
            best_val, best_assign = val, assign.copy()
    return best_assign, best_val


cost = np.array([[8.0, 6.0, 5.0, 7.0],
                 [6.0, 7.0, 8.0, 5.0]])
a = np.array([[3, 2, 4, 3], [3, 3, 3, 2]])
b = np.array([7, 6])
assign, val = gap_local_search(cost, a, b, n_restarts=20, seed=1)
print(assign, val)
# Expected: assign [1 0 0 1], value 22.0 (feasible optimum; no penalty active)
```

Run the validator from the previous section on every output of this heuristic:
a penalized objective equal to the raw cost does not by itself prove feasibility.

## Advanced Techniques

### Auction algorithm and warm-started reoptimization

Bertsekas (1988), "The auction algorithm", solves LAP by having unassigned
"persons" bid for their best objects, raising prices by at least ε.
With ε < 1/n on integer costs the final assignment is optimal; ε-scaling
(start coarse, refine) gives competitive O(n³)-class behavior. Auction's
practical edge: it parallelizes naturally, works on sparse graphs, and
restarts cheaply from old prices. When LAP is solved repeatedly with slowly
changing costs (inside branch-and-bound, ALNS repair, or tracking loops),
keep the dual prices/potentials between calls — reoptimization after a few
cost changes typically takes a small fraction of a cold solve.

### Reduced-cost variable fixing for GAP

After subgradient ascent, the per-agent knapsack DP tables give cheap
conditional bounds: the bound with x_ij forced to 1 is L(λ) plus the
insertion penalty of item j in agent i's knapsack (computable from the
forward and backward DP arrays). If that forced bound exceeds the incumbent
upper bound, fix x_ij = 0 permanently; symmetrically, forcing x_ij = 0 can
prove x_ij = 1. On Chu-Beasley class D/E instances this routinely removes a
large share of the variables before the MIP is even built — fix variables,
then hand the shrunken model to Gurobi.

### Ejection chains and very large neighborhoods

Shift and swap neighborhoods stall on tightly capacitated GAP because every
single move is blocked by capacities. Ejection chains (Yagiura, Ibaraki &
Glover 2004) move job j1 to agent i, ejecting some j2 from i to another
agent, possibly continuing the chain — a sequence of shifts that is
infeasible piecewise but feasible as a whole. A cheaper alternative is a
2-job swap neighborhood (exchange the agents of j1, j2), still O(n²) to
scan with vectorized deltas. Both compose well with the penalized descent
above: run shift descent to a local optimum, then probe chains/swaps.

### Sparse, rectangular, and optional assignment

For sparse cost structure use
`scipy.sparse.csgraph.min_weight_full_bipartite_matching` instead of
densifying with big-M entries. For optional assignment (a row may stay
unmatched at a known outside-option cost), append one dummy column per row
holding that row's outside cost — never pad with zeros in a minimization,
which silently makes "unmatched" free and optimal. Rectangular LAP with
rows ≤ columns is handled natively by scipy; with more rows than columns,
transpose and re-interpret.

### GAP inside decomposition

GAP is a canonical column-generation application: reformulate per agent,
where a column is one feasible job subset for that agent (a knapsack
solution), and the master is a set-partitioning problem over jobs.
Pricing = knapsack with duals as job prizes; branching on the semi-assignment
variables keeps pricing intact (Savelsbergh 1997, "A branch-and-price
algorithm for the generalized assignment problem"). Conversely, LAP appears
as a subproblem elsewhere — e.g., the assignment relaxation that bounds TSP
branch-and-bound. Recognizing an embedded LAP/GAP and solving it with the
right specialized code is often the single largest speedup available.

## Practical Challenges

**The answer is "right" but the convention was wrong.** Profit data fed into
a minimization (or vice versa) yields a feasible, confidently wrong result.
Fix the sense in one place: convert profits with c' = max(c) − c at the data
boundary, document it, and have the validator recompute the *original*
objective so the report shows numbers the stakeholder recognizes.

**GAP instance is infeasible and the solver only says INFEASIBLE.** Add an
artificial overflow agent with huge cost and infinite capacity; jobs landing
there pinpoint what does not fit. Alternatively compute a Gurobi IIS to find
the conflicting capacity rows. Check first that each job fits at least one
agent alone (a_ij ≤ b_i for some i) — the most common data bug.

**Forbidden pairs encoded as big-M leak into solutions.** A big-M of 10^6 on
costs of order 10 looks safe until the instance is infeasible without the
forbidden pair, and the solver quietly uses it. Prefer `np.inf` (scipy) or
simply not creating the variable (MIP). If big-M is unavoidable, assert
after solving that no selected entry carries it.

**Subgradient ascent stalls or oscillates.** Symptoms: the bound zigzags and
theta collapses to nothing. Use the Polyak step toward the best upper bound,
halve theta only after a patience window (20 iterations here), and consider
averaging the last multipliers instead of taking the final ones. If the gap
refuses to close, the instance likely has a genuine duality gap — switch
effort to the primal side.

**Knapsack DP explodes because resources are floats.** DP over capacity
needs integer weights. Scale by 10^k and round — but bound the rounding
error you introduce in the *capacity* direction (round consumption up,
capacity down, to stay conservative) or solve the per-agent pricing as a
tiny MIP instead.

**LAP inside a hot loop dominates runtime.** Profile first. Then: shrink the
matrix with candidate lists (k cheapest agents per task), reuse dual
potentials between consecutive solves, or switch to a C library handling
batches. Vectorizing the cost-matrix construction usually matters as much
as the solver call itself.

**Many optimal assignments make downstream behavior unstable.** Assignment
polytopes are highly degenerate; reruns return different optima and confuse
users and tests. Break ties deterministically: add a tiny seeded perturbation
ε·rng.random() with ε below half the smallest nonzero cost difference, or
lexicographic secondary costs. Record the seed with the result.

**Penalized local search returns infeasible "optima".** If rho is on the
order of the costs, buying capacity violation is cheaper than a bad
assignment. Set rho above the largest plausible cost gain of any single move
(here: > max(c) − min(c)), or escalate rho adaptively whenever a restart
ends infeasible — then always run the independent validator.

## Tools & Libraries

| Library / function | When to use | Note |
|---|---|---|
| `scipy.optimize.linear_sum_assignment` | Dense LAP up to ~10^4×10^4 | JV-type, C speed, rectangular + inf support |
| `scipy.sparse.csgraph.min_weight_full_bipartite_matching` | Sparse LAP | Avoids big-M densification |
| `scipy.sparse.csgraph.maximum_bipartite_matching` | Bottleneck feasibility tests | Hopcroft-Karp |
| gurobipy | GAP MIP, LP duals, variable fixing | License required; the reference exact path |
| OR-Tools (`LinearSumAssignment`, min-cost flow) | LAP with integer costs at scale | Also CP-SAT when side constraints appear |
| HiGHS via `scipy.optimize.milp` | License-free GAP MIP | Slower than Gurobi but adequate at moderate size |
| `lap` / `lapsolver` (PyPI) | Batched LAP in hot loops | Faster than scipy for many small matrices |
| networkx | Prototyping, tiny graphs, teaching | `min_weight_matching` is general-graph and slow |

## Output Format

A complete assignment-problem deliverable contains:

1. **Problem classification.** Variant (LAP/GAP/bottleneck), sense,
   dimensions, balanced/rectangular, forbidden pairs, data provenance.
2. **Method and certificate.** What was solved and what is proven: "MIP
   optimal, gap 0.0%", "Lagrangian LB 1412.3, heuristic UB 1437.0, gap
   1.75%", or "exact by total unimodularity / threshold search".
3. **Solution table.** Per agent: assigned jobs, load vs capacity, cost
   share. Per job (when n is small): chosen agent, cost, second-best agent
   and regret (useful for sensitivity discussions).
4. **Independent validation line.** Output of the validator, not the
   solver: feasibility verdict, recomputed objective, any issues.
5. **Reproducibility.** Instance seed/class, solver parameters and version,
   time limit, wall time, machine note.

```text
GAP solution report - instance c_3x12 (seed 42)
method        : Gurobi MIP (TimeLimit 60s) | status OPTIMAL | gap 0.00%
objective     : 312.0 (min cost)   validated: FEASIBLE, recomputed 312.0
bounds        : LP 297.4 | Lagrangian 305.1 | best integer 312.0
agent  jobs                load/capacity   cost
  0    2, 5, 7, 11         47/49           104.0
  1    0, 3, 6, 9          44/46           98.0
  2    1, 4, 8, 10         45/47           110.0
runtime 0.4 s | gurobipy 12.x | seed 42 | validator: 0 issues
```

For bound-only studies, report the bound trajectory (iteration, L(λ), best
UB) as a tidy table so convergence can be plotted later.

## Questions to Ask

- Can one agent take several tasks, or is the matching one-to-one?
- Minimize total cost, maximize total profit, or minimize the worst cost?
- How large is the instance (m agents × n tasks), and how dense are the costs?
- Are there forbidden agent-task pairs, and how are they encoded in the data?
- Are resource consumptions and capacities integers, or floats needing scaling?
- Is this solved once, or repeatedly inside another algorithm?
- Is a proven optimum required, or is a bounded-gap solution within a time
  budget acceptable?
- Is a Gurobi license available, or should everything run on scipy/HiGHS?
- What should happen when the instance is infeasible — fail, or report which
  jobs do not fit?

## Related Skills

- **network-flow-optimization** — when the assignment is better modeled as
  min-cost flow, or total unimodularity and integral LPs need deeper treatment
- **quadratic-assignment-problem** — when costs depend on pairs of assignments
  (flow × distance interactions), which breaks every method in this skill
- **lagrangian-relaxation** — when you need the general subgradient machinery,
  step-size rules, and primal recovery behind the GAP bound shown here
- **milp-modeling-gurobi** — when you need general MIP construction patterns,
  parameter handling, and solution extraction beyond the GAP model above
- **linear-programming-fundamentals** — when duality, reduced costs, and the
  LP background behind Hungarian potentials need deeper treatment
