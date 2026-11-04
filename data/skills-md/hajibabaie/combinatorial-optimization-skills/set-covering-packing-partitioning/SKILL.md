---
name: set-covering-packing-partitioning
description: When the user wants to model or solve set covering, set packing, or set partitioning problems with exact MIP models, the greedy heuristic and its ln(n) guarantee, LP rounding, or Lagrangian-based heuristics in the Caprara-Fischetti-Toth style. Also use when the user mentions "set covering," "set partitioning," "set packing," "crew scheduling," "covering constraint," "winner determination," or when each row must be hit at least once, exactly once, or at most once by selected columns. For pricing the columns of huge set-partitioning masters, see column-generation; for the routes behind those columns, see vehicle-routing-problem.
---

# Set Covering, Packing, and Partitioning

You are an expert in integer programming and combinatorial optimization with deep
experience in covering-type models. This skill covers the set covering problem (SCP),
set packing, and set partitioning: exact MIP formulations, the greedy
ln(n)-approximation, LP rounding, Lagrangian-based heuristics in the
Caprara-Fischetti-Toth tradition, GRASP, and the crew-scheduling and column-generation
context where these models dominate. Use the framework below to classify the variant
first, then pick a solution path that matches instance size and optimality needs.

## Initial Assessment

Establish these facts before writing any model or code:

- **Row semantics.** Must each row be hit at least once (covering), exactly once
  (partitioning), or at most once (packing)? This single choice changes feasibility
  behavior, LP strength, and the right algorithm more than anything else.
- **Direction of the objective.** Covering and partitioning minimize cost; packing
  maximizes profit. Confirm the user is not mixing the two (e.g., "maximize coverage"
  is a different model: maximal covering location, a budgeted variant).
- **Instance size and density.** How many rows m, columns n, and what fraction of
  entries are nonzero? OR-Library SCP instances run from 200 x 1000 at 2% density to
  unicost instances at 5,000+ columns. Density drives both memory layout and LP
  difficulty.
- **Are the columns explicit or implicit?** If columns are routes, crew pairings, or
  patterns that must be generated, this is a column-generation master problem, not a
  static MIP. Route the conversation accordingly.
- **Cost structure.** Unicost (all c_j = 1) instances behave very differently from
  general-cost ones: LP bounds are weaker and greedy is less informative. Ask.
- **Side constraints.** Base capacities in crew scheduling, cardinality limits,
  mutual-exclusion pairs. These break pure SCP structure and may push toward a plain
  MIP or branch-and-price.
- **Over-covering tolerance.** In practice, can a row be covered twice (a deadheading
  crew, a doubly visited customer)? If yes, replace fragile partitioning constraints
  with covering plus a penalty.
- **Solver availability and time budget.** Gurobi licensed? Seconds or hours? Proven
  optimal or "good cover fast"? Gurobi solves most general-cost SCPs of moderate size
  outright; large unicost and partitioning instances are where heuristics earn their
  keep.
- **Validation requirements.** Agree up front that every reported solution passes an
  independent feasibility and objective check, separate from the model code.

## Problem Definitions and Formulations

Ground set $I = \{1, \dots, m\}$ of rows (elements, tasks, flight legs). A family of
$n$ columns (subsets) $S_j \subseteq I$, each with cost or profit $c_j > 0$. The
incidence matrix $A \in \{0,1\}^{m \times n}$ has $a_{ij} = 1$ iff $i \in S_j$.
Binary variable $x_j = 1$ iff column $j$ is selected.

**Set covering (SCP)** — every row hit at least once, minimize cost:

$$
\min \; \sum_{j=1}^{n} c_j x_j \quad \text{s.t.} \quad \sum_{j:\, i \in S_j} x_j \ge 1 \;\; \forall i \in I, \qquad x \in \{0,1\}^n
$$

**Set packing** — rows hit at most once, maximize profit:

$$
\max \; \sum_{j=1}^{n} c_j x_j \quad \text{s.t.} \quad \sum_{j:\, i \in S_j} x_j \le 1 \;\; \forall i \in I, \qquad x \in \{0,1\}^n
$$

**Set partitioning** — every row hit exactly once, minimize cost:

$$
\min \; \sum_{j=1}^{n} c_j x_j \quad \text{s.t.} \quad \sum_{j:\, i \in S_j} x_j = 1 \;\; \forall i \in I, \qquad x \in \{0,1\}^n
$$

All three are NP-hard; SCP and exact cover (partitioning feasibility) are among
Karp's original 21 problems (Karp 1972, "Reducibility Among Combinatorial Problems").

### Variant selection

| Variant | Constraint | Objective | Typical applications |
|---|---|---|---|
| Set covering | $Ax \ge \mathbf{1}$ | min cost | shift staffing levels, sensor/facility coverage, route masters with free over-cover |
| Set packing | $Ax \le \mathbf{1}$ | max profit | combinatorial auction winner determination, disjoint project or slot selection |
| Set partitioning | $Ax = \mathbf{1}$ | min cost | airline crew pairing, political districting, exact customer-to-route assignment |

Relationships worth exploiting:

- A partition is exactly a solution that is simultaneously a cover and a packing.
- If over-covering is physically harmless (free disposal), solve the covering
  relaxation of a partitioning model: every cover can be interpreted as a partition
  plus tolerated duplicates, and the covering LP is far better behaved (less
  degenerate, always feasible when every row has a column).
- Set packing with rows = edges and columns = vertices is maximum-weight independent
  set, so packing inherits its inapproximability: no $n^{1-\varepsilon}$
  approximation unless P = NP (Hastad 1999, "Clique is hard to approximate";
  Zuckerman 2007 derandomization).
- Partitioning feasibility alone is NP-complete (exact cover), so heuristics need an
  explicit feasibility strategy, not just an objective-improvement loop.

### Approximability and bound quality

| Result | Statement | Reference |
|---|---|---|
| Greedy guarantee | cost $\le H(d) \cdot \mathrm{OPT}$, $H(d) = \sum_{k=1}^{d} 1/k \le \ln d + 1$, $d = \max_j |S_j|$ | Chvatal (1979), "A greedy heuristic for the set-covering problem" |
| LP rounding | $f$-approximation, $f$ = max columns through any row | Hochbaum (1982), "Approximation algorithms for the set covering and vertex cover problems" |
| Randomized rounding | $O(\ln m)$-approximation with high probability | Raghavan & Thompson (1987) |
| Covering hardness | no $(1-o(1))\ln n$ approximation unless P = NP | Feige (1998); sharpened by Dinur & Steurer (2014) |
| Packing hardness | no $n^{1-\varepsilon}$ approximation unless P = NP | Hastad (1999) |
| LP gap (covering) | integrality gap is $\Theta(\ln m)$ in the worst case, but typically 1-2% on general-cost OR-Library instances | Beasley (1987) computational evidence |

Decision guidance:

- **Use the MIP directly** when n is up to a few hundred thousand explicit columns and
  costs are general. Modern solvers exploit the structure well.
- **Use greedy / GRASP / Lagrangian heuristics** for unicost instances, very large n,
  tight time budgets, or as upper bounds and MIP starts.
- **Use column generation / branch-and-price** when columns are implicit (pairings,
  routes, patterns); see the Advanced Techniques section.
- **Reformulate partitioning as penalized covering** whenever the application
  tolerates over-coverage; this is standard practice in crew scheduling.

## Exact Models in Gurobi

One builder function per constraint family keeps the model auditable: each family can
be unit-tested on a tiny instance, constraint names make IIS output readable when a
partitioning model turns out infeasible, and switching variant means swapping one
builder. For partitioning instances where finding any feasible point is hard, set
`MIPFocus = 1` and consider seeding a cover-based start (see Practical Challenges).

```python
import gurobipy as gp
from gurobipy import GRB
import numpy as np


def add_cover_constraints(model: gp.Model, x: gp.tupledict, A: np.ndarray) -> None:
    """Covering rows: each row is hit at least once."""
    for i in range(A.shape[0]):
        cols = np.flatnonzero(A[i])
        model.addConstr(gp.quicksum(x[j] for j in cols) >= 1, name=f"cover[{i}]")


def add_packing_constraints(model: gp.Model, x: gp.tupledict, A: np.ndarray) -> None:
    """Packing rows: each row is hit at most once."""
    for i in range(A.shape[0]):
        cols = np.flatnonzero(A[i])
        model.addConstr(gp.quicksum(x[j] for j in cols) <= 1, name=f"pack[{i}]")


def add_partition_constraints(model: gp.Model, x: gp.tupledict, A: np.ndarray) -> None:
    """Partitioning rows: each row is hit exactly once."""
    for i in range(A.shape[0]):
        cols = np.flatnonzero(A[i])
        model.addConstr(gp.quicksum(x[j] for j in cols) == 1, name=f"part[{i}]")


def build_set_system_model(
    A: np.ndarray, c: np.ndarray, mode: str
) -> tuple[gp.Model, gp.tupledict]:
    """Build the SCP / set packing / set partitioning MIP over incidence matrix A."""
    n = A.shape[1]
    model = gp.Model(f"set-{mode}")
    model.Params.OutputFlag = 0
    x = model.addVars(n, vtype=GRB.BINARY, name="x")
    sense = GRB.MAXIMIZE if mode == "packing" else GRB.MINIMIZE
    model.setObjective(gp.quicksum(float(c[j]) * x[j] for j in range(n)), sense)
    builders = {
        "cover": add_cover_constraints,
        "packing": add_packing_constraints,
        "partition": add_partition_constraints,
    }
    builders[mode](model, x, A)
    return model, x


def solve_set_system(
    A: np.ndarray, c: np.ndarray, mode: str, time_limit: float = 60.0
) -> dict[str, object]:
    """Solve the chosen variant and extract the incumbent; raise if none exists."""
    model, x = build_set_system_model(A, c, mode)
    model.Params.TimeLimit = time_limit
    model.Params.MIPGap = 1e-6
    model.optimize()
    usable = model.Status == GRB.OPTIMAL or (
        model.Status == GRB.TIME_LIMIT and model.SolCount > 0
    )
    if not usable:
        raise RuntimeError(f"no solution available, Gurobi status {model.Status}")
    sol = np.array([x[j].X > 0.5 for j in range(A.shape[1])])
    return {"x": sol, "objective": model.ObjVal, "bound": model.ObjBound,
            "gap": model.MIPGap, "status": model.Status}


# Tiny instance: 4 rows, 5 columns S1..S5 with S3 = {1,3}, S4 = {2,4}.
A = np.array([[1, 0, 1, 0, 1], [1, 0, 0, 1, 1],
              [0, 1, 1, 0, 1], [0, 1, 0, 1, 1]], dtype=bool)
c = np.array([3.0, 3.0, 2.0, 2.0, 5.0])
for mode in ("cover", "partition", "packing"):
    res = solve_set_system(A, c, mode)
    print(mode, res["objective"], sorted(np.flatnonzero(res["x"])))
# Expected: cover 4.0 [2, 3] / partition 4.0 [2, 3] / packing 6.0 [0, 1]
```

The same data yields three different optima: columns S3 and S4 form both the cheapest
cover and the cheapest partition (cost 4), while the most profitable packing takes S1
and S2 (profit 6). Keeping the three builders separate makes such comparisons a
two-line experiment.

## Instance Generation and Independent Validation

Benchmark conventions follow Beasley (1987, 1990; OR-Library): classes scp4x-scp6x
and scpa-scpe have densities of 2-20% and costs uniform in [1, 100]; the scpnr and
unicost classes (including Steiner triple systems) are markedly harder for both LP
bounds and heuristics. The generator below reproduces that style with two guarantees:
every row is coverable by at least two columns (so covering is feasible and no column
is trivially forced), and no column is empty.

```python
import numpy as np


def generate_scp_instance(
    m: int, n: int, density: float = 0.05, cost_mode: str = "random", seed: int = 0
) -> tuple[np.ndarray, np.ndarray]:
    """Random set-system instance in OR-Library style (Beasley 1987).

    cost_mode: 'unicost' (all 1), 'random' (uniform integers in [1, 100]),
    or 'size_correlated' (cost grows with column size, which weakens greedy).
    """
    rng = np.random.default_rng(seed)
    A = rng.random((m, n)) < density
    # Repair empty columns: give each one a random row.
    empty_cols = np.flatnonzero(~A.any(axis=0))
    A[rng.integers(0, m, size=empty_cols.size), empty_cols] = True
    # Repair rows covered fewer than twice.
    for i in np.flatnonzero(A.sum(axis=1) < 2):
        need = 2 - int(A[i].sum())
        candidates = np.flatnonzero(~A[i])
        A[i, rng.choice(candidates, size=need, replace=False)] = True
    if cost_mode == "unicost":
        c = np.ones(n)
    elif cost_mode == "random":
        c = rng.integers(1, 101, size=n).astype(float)
    else:  # size_correlated
        c = np.ceil(A.sum(axis=0) * rng.uniform(0.8, 1.2, size=n) * 10.0)
    return A, c


A, c = generate_scp_instance(m=50, n=200, density=0.05, cost_mode="random", seed=42)
print(A.shape, int(A.sum(axis=1).min()), float(c.min()), float(c.max()))
# Expected: (50, 200) with minimum row coverage >= 2 and costs inside [1, 100].
```

The validator recomputes feasibility and objective from the raw incidence matrix
only. It shares no code with the model builders, so a bug in constraint construction
cannot hide itself. Run it on every solution you report, from any method.

```python
import numpy as np


def validate_solution(
    A: np.ndarray, c: np.ndarray, x: np.ndarray, mode: str
) -> dict[str, object]:
    """Independent feasibility + objective check from raw data; trusts no solver."""
    x = np.asarray(x, dtype=bool)
    coverage = A[:, x].sum(axis=1)
    if mode == "cover":
        violated = np.flatnonzero(coverage < 1)
    elif mode == "partition":
        violated = np.flatnonzero(coverage != 1)
    elif mode == "packing":
        violated = np.flatnonzero(coverage > 1)
    else:
        raise ValueError(f"unknown mode {mode!r}")
    return {
        "feasible": violated.size == 0,
        "objective": float(c[x].sum()),
        "violated_rows": violated.tolist(),
        "n_selected": int(x.sum()),
        "max_coverage": int(coverage.max()) if coverage.size else 0,
    }


A = np.array([[1, 0, 1, 0, 1], [1, 0, 0, 1, 1],
              [0, 1, 1, 0, 1], [0, 1, 0, 1, 1]], dtype=bool)
c = np.array([3.0, 3.0, 2.0, 2.0, 5.0])
report = validate_solution(A, c, np.array([0, 0, 1, 1, 0]), "partition")
print(report["feasible"], report["objective"], report["violated_rows"])
# Expected: True 4.0 [] -- columns S3 and S4 partition all four rows at cost 4.
```

The `max_coverage` field is a cheap diagnostic: a covering solution with
`max_coverage` well above 1 usually still contains redundant columns and should go
through reverse delete before being reported.

## Approximation Algorithms: Greedy and LP Rounding

The greedy heuristic (Chvatal 1979) repeatedly selects the column minimizing
$c_j / |\text{newly covered rows}|$. Its cost is at most $H(d) \cdot \mathrm{OPT}$
with $d = \max_j |S_j|$ and $H(d) \le \ln d + 1$, and this is essentially the best
possible for polynomial algorithms: Feige (1998) showed no $(1-o(1))\ln n$
approximation exists unless P = NP. Greedy output often contains redundant columns
picked early, so always follow it with reverse delete (drop expensive columns whose
rows remain covered).

```python
import numpy as np


def greedy_set_cover(A: np.ndarray, c: np.ndarray) -> np.ndarray:
    """Chvatal (1979) greedy: best cost per newly covered row, until all covered.

    Guarantee: cost <= H(d) * OPT with d = largest column size. Assumes every
    row is covered by at least one column.
    """
    m, n = A.shape
    uncovered = np.ones(m, dtype=bool)
    selected = np.zeros(n, dtype=bool)
    while uncovered.any():
        gain = A[uncovered].sum(axis=0).astype(float)
        gain[selected] = 0.0
        ratio = np.full(n, np.inf)
        pos = gain > 0
        ratio[pos] = c[pos] / gain[pos]
        j = int(np.argmin(ratio))
        selected[j] = True
        uncovered &= ~A[:, j]
    return selected


def remove_redundant_columns(
    A: np.ndarray, c: np.ndarray, selected: np.ndarray
) -> np.ndarray:
    """Reverse delete: drop the most expensive redundant columns first."""
    selected = selected.copy()
    cover = A[:, selected].sum(axis=1)
    for j in sorted(np.flatnonzero(selected), key=lambda k: -c[k]):
        rows = A[:, j]
        if np.all(cover[rows] >= 2):
            selected[j] = False
            cover[rows] -= 1
    return selected


A = np.array([[1, 0, 1, 0, 1], [1, 0, 0, 1, 1],
              [0, 1, 1, 0, 1], [0, 1, 0, 1, 1]], dtype=bool)
c = np.array([3.0, 3.0, 2.0, 2.0, 5.0])
x = remove_redundant_columns(A, c, greedy_set_cover(A, c))
print(sorted(np.flatnonzero(x)), float(c[x].sum()))
# Expected: [2, 3] 4.0 -- the MIP optimum; the a-priori guarantee was H(4) ~ 2.08 * OPT.
```

LP rounding (Hochbaum 1982) gives a complementary guarantee tied to row frequency
rather than column size. Solve the LP relaxation, then select every column with
$x_j^{LP} \ge 1/f$, where $f$ is the maximum number of columns through any row. Each
covering row has at most $f$ fractional variables summing to at least 1, so at least
one of them clears the threshold: the rounded solution is always feasible, and its
cost is at most $f \cdot \mathrm{OPT}$. With $f = 2$ this is exactly the classic
vertex-cover 2-approximation. The LP value is also the standard lower bound to report
alongside any heuristic. Randomized rounding (select column $j$ with probability
$\min(1, \alpha x_j^{LP})$, $\alpha = O(\ln m)$, repeat until feasible) usually does
better in cost but needs the repetition loop.

```python
import gurobipy as gp
from gurobipy import GRB
import numpy as np


def lp_rounding_cover(A: np.ndarray, c: np.ndarray) -> tuple[np.ndarray, float]:
    """Hochbaum (1982) deterministic LP rounding: an f-approximation for SCP.

    f = max number of columns covering any single row. Returns (solution, LP bound).
    """
    m, n = A.shape
    model = gp.Model("scp-lp")
    model.Params.OutputFlag = 0
    x = model.addVars(n, lb=0.0, ub=1.0, name="x")
    for i in range(m):
        cols = np.flatnonzero(A[i])
        model.addConstr(gp.quicksum(x[j] for j in cols) >= 1, name=f"cover[{i}]")
    model.setObjective(gp.quicksum(float(c[j]) * x[j] for j in range(n)), GRB.MINIMIZE)
    model.optimize()
    if model.Status != GRB.OPTIMAL:
        raise RuntimeError(f"LP not solved to optimality, status {model.Status}")
    x_lp = np.array([x[j].X for j in range(n)])
    f = int(A.sum(axis=1).max())
    rounded = x_lp >= 1.0 / f - 1e-9
    return rounded, float(model.ObjVal)


A = np.array([[1, 0, 1, 0, 1], [1, 0, 0, 1, 1],
              [0, 1, 1, 0, 1], [0, 1, 0, 1, 1]], dtype=bool)
c = np.array([3.0, 3.0, 2.0, 2.0, 5.0])
x_round, lp_bound = lp_rounding_cover(A, c)
print(sorted(np.flatnonzero(x_round)), float(c[x_round].sum()), lp_bound)
# Expected: [2, 3] 4.0 4.0 -- the LP is integral here, so rounding returns the optimum.
```

Practical reading of the two guarantees: greedy wins when columns are large and rows
are in many columns (big $f$, moderate $d$); LP rounding wins when each row appears
in few columns (small $f$), as in vertex-cover-like structures. On general-cost
OR-Library instances, both typically land within a few percent of the LP bound, and
the LP bound itself is within 1-2% of the integer optimum.

## GRASP and the Caprara-Fischetti-Toth Lagrangian Heuristic

GRASP is a natural fit for SCP — it was introduced on this very problem (Feo &
Resende 1989, "A probabilistic heuristic for a computationally difficult set covering
problem"). Each iteration builds a cover with a restricted candidate list (RCL) over
the greedy cost-effectiveness ratio, then cleans it with reverse delete. The
implementation below stays under 80 lines; the **grasp** skill covers reactive alpha
tuning, RCL design choices, and path relinking between elite covers, all of which
drop into this loop unchanged.

```python
import numpy as np


def _rcl_construction(
    A: np.ndarray, c: np.ndarray, alpha: float, rng: np.random.Generator
) -> np.ndarray:
    """Greedy randomized construction: sample uniformly from the RCL of columns
    whose cost-effectiveness is within alpha of the best."""
    m, n = A.shape
    uncovered = np.ones(m, dtype=bool)
    selected = np.zeros(n, dtype=bool)
    while uncovered.any():
        gain = A[uncovered].sum(axis=0).astype(float)
        gain[selected] = 0.0
        ratio = np.full(n, np.inf)
        pos = gain > 0
        ratio[pos] = c[pos] / gain[pos]
        r_min, r_max = ratio[pos].min(), ratio[pos].max()
        threshold = r_min + alpha * (r_max - r_min)
        rcl = np.flatnonzero(ratio <= threshold + 1e-12)
        j = int(rng.choice(rcl))
        selected[j] = True
        uncovered &= ~A[:, j]
    return selected


def _drop_redundant(A: np.ndarray, c: np.ndarray, selected: np.ndarray) -> np.ndarray:
    """Reverse delete: drop selected columns (most expensive first) not needed."""
    selected = selected.copy()
    cover = A[:, selected].sum(axis=1)
    for j in sorted(np.flatnonzero(selected), key=lambda k: -c[k]):
        rows = A[:, j]
        if np.all(cover[rows] >= 2):
            selected[j] = False
            cover[rows] -= 1
    return selected


def grasp_set_cover(
    A: np.ndarray, c: np.ndarray, n_iters: int = 200, alpha: float = 0.3, seed: int = 0
) -> tuple[np.ndarray, float]:
    """GRASP for SCP (Feo & Resende 1989): RCL construction + redundancy removal.

    alpha = 0 is pure greedy; alpha = 1 is uniformly random construction.
    See the grasp skill for reactive alpha and path relinking extensions.
    """
    rng = np.random.default_rng(seed)
    best_x = np.zeros(A.shape[1], dtype=bool)
    best_cost = np.inf
    for _ in range(n_iters):
        x = _drop_redundant(A, c, _rcl_construction(A, c, alpha, rng))
        cost = float(c[x].sum())
        if cost < best_cost:
            best_x, best_cost = x.copy(), cost
    return best_x, best_cost


A = np.array([[1, 0, 1, 0, 1], [1, 0, 0, 1, 1],
              [0, 1, 1, 0, 1], [0, 1, 0, 1, 1]], dtype=bool)
c = np.array([3.0, 3.0, 2.0, 2.0, 5.0])
x_best, cost_best = grasp_set_cover(A, c, n_iters=50, alpha=0.3, seed=7)
print(sorted(np.flatnonzero(x_best)), cost_best)
# Expected: [2, 3] 4.0 -- GRASP finds the optimal cover {S3, S4} on this instance.
```

The strongest classical SCP heuristic is Lagrangian-based: Caprara, Fischetti & Toth
(1999), "A heuristic method for the set covering problem", won the FASTER competition
on instances with millions of columns. Dualize the covering constraints with
multipliers $u \ge 0$:

$$
L(u) = \sum_{i} u_i + \sum_{j} \min\bigl(0,\; c_j - \textstyle\sum_{i \in S_j} u_i\bigr),
\qquad x_j(u) = 1 \iff c_j - \textstyle\sum_{i \in S_j} u_i < 0 .
$$

Maximize $L(u)$ by subgradient ascent ($g_i = 1 - \sum_j a_{ij} x_j(u)$, step
$\lambda (UB - L(u)) / \lVert g \rVert^2$), and periodically recover primal covers by
running greedy on the Lagrangian reduced costs — near-optimal multipliers make
reduced costs an excellent column-quality signal. Because the Lagrangian subproblem
has the integrality property, the best achievable bound equals the LP bound, but it
arrives orders of magnitude faster than solving the LP on huge instances. The
**lagrangian-relaxation** skill covers step-size rules and convergence in depth.

```python
import numpy as np


def _greedy_with_costs(A: np.ndarray, score: np.ndarray) -> np.ndarray:
    """Greedy cover driven by an arbitrary nonnegative score vector as costs."""
    m, n = A.shape
    uncovered = np.ones(m, dtype=bool)
    selected = np.zeros(n, dtype=bool)
    while uncovered.any():
        gain = A[uncovered].sum(axis=0).astype(float)
        gain[selected] = 0.0
        ratio = np.where(gain > 0, score / np.maximum(gain, 1e-12), np.inf)
        j = int(np.argmin(ratio))
        selected[j] = True
        uncovered &= ~A[:, j]
    return selected


def lagrangian_scp(
    A: np.ndarray, c: np.ndarray, n_iters: int = 300, seed: int = 0
) -> dict[str, float]:
    """CFT-style subgradient + Lagrangian greedy (Caprara, Fischetti & Toth 1999).

    Returns the best lower bound, best validated upper bound, and gap percent.
    """
    m, n = A.shape
    Af = A.astype(float)
    cost_per_row = c / A.sum(axis=0)          # cost per covered row, per column
    u = np.array([cost_per_row[A[i]].min() for i in range(m)])
    x0 = _greedy_with_costs(A, c.astype(float))
    best_x, best_ub = x0, float(c[x0].sum())
    best_lb, lam, stall = 0.0, 2.0, 0
    for it in range(n_iters):
        reduced = c - Af.T @ u
        x_u = reduced < 0.0
        lb = float(u.sum() + reduced[x_u].sum())
        if lb > best_lb + 1e-9:
            best_lb, stall = lb, 0
        else:
            stall += 1
        if stall == 20:
            lam, stall = lam / 2.0, 0
        g = 1.0 - Af @ x_u
        sq = float(g @ g)
        if sq < 1e-12:
            break                              # x(u) feasible: multipliers optimal
        if it % 10 == 0:                       # primal recovery on reduced costs
            x_h = _greedy_with_costs(A, np.maximum(reduced, 0.0) + 1e-6)
            ub = float(c[x_h].sum())
            if ub < best_ub:
                best_ub, best_x = ub, x_h
        u = np.maximum(0.0, u + lam * (best_ub - lb) / sq * g)
    gap = 100.0 * (best_ub - best_lb) / best_ub
    return {"best_lb": best_lb, "best_ub": best_ub,
            "gap_pct": gap, "n_selected": float(best_x.sum())}


A = np.array([[1, 0, 1, 0, 1], [1, 0, 0, 1, 1],
              [0, 1, 1, 0, 1], [0, 1, 0, 1, 1]], dtype=bool)
c = np.array([3.0, 3.0, 2.0, 2.0, 5.0])
res = lagrangian_scp(A, c, n_iters=100, seed=1)
print(round(res["best_lb"], 2), res["best_ub"], round(res["gap_pct"], 2))
# Expected: 4.0 4.0 0.0 -- the Lagrangian dual matches the LP bound and closes the gap.
```

## Advanced Techniques

### Lagrangian cores and column fixing

The full CFT method wraps the subgradient loop above in two scaling devices. First, a
**core problem**: keep only the 5 or so columns with the smallest Lagrangian reduced
cost per row (plus columns in the incumbent), run everything on this core, and
periodically re-price the full column set against the current multipliers to refresh
it. This is what makes million-column instances tractable in memory and time. Second,
**reduced-cost fixing**: with lower bound $LB$ and incumbent $UB$, any column with
$c_j - \sum_{i \in S_j} u_i > UB - LB$ cannot appear in an improving solution and is
fixed to zero; conversely, CFT fixes to one the columns that persist across several
near-best Lagrangian greedy solutions, then re-optimizes the residual problem. Both
devices transfer directly to any Lagrangian heuristic you build on covering-type
models.

### Crew scheduling as set partitioning

Airline and rail crew pairing is the canonical industrial set partitioning problem
(Garfinkel & Nemhauser 1969; Barnhart et al. 1998, "Branch-and-Price: Column
Generation for Solving Huge Integer Programs"). Rows are flight legs or trips in a
planning horizon; a column is a legal *pairing* — a multi-day sequence of legs
respecting duty-time, rest, and connection rules — with cost equal to guaranteed pay
minus flying credit. The model is $\min c^\top x$, $Ax = \mathbf{1}$, plus side
constraints such as crew-base capacities $\sum_{j \in B_b} x_j \le \kappa_b$.
Practitioners almost always solve the **covering relaxation** $Ax \ge \mathbf{1}$
with an over-cover penalty: a doubly covered leg means one crew deadheads on it,
which is operationally legal and priced at a real cost. This single modeling choice
removes most partitioning infeasibility and LP degeneracy pain. Calibrate the
penalty to the true deadhead cost, not to an arbitrary big-M, or the optimizer will
trade real flying for fake savings.

### The column generation connection

In crew pairing, vehicle routing, and cutting stock, the column set is implicit and
astronomically large, so the partitioning/covering model is solved as a
**restricted master problem**: keep a manageable subset of columns, get duals $u_i$
from the LP, and price new columns by solving $\min_j c_j - \sum_{i \in S_j} u_i$
over the implicit set — a resource-constrained shortest path for pairings and routes,
a knapsack for cutting patterns. Negative reduced cost columns enter; repeat to LP
optimality, then branch with rules that preserve pricing structure (Ryan & Foster
1981: branch on a row pair (s, t) being covered by the same or different columns).
The Lagrangian multipliers from the CFT loop are interchangeable with LP duals here,
which is why the two literatures cross-reference constantly. The
**column-generation** skill covers the master-pricing loop, stabilization, and
branch-and-price mechanics; the **vehicle-routing-problem** skill shows the
route-based master in full.

### Preprocessing and problem reductions

Apply these dominance rules before any algorithm; on OR-Library instances they often
remove 10-50% of the matrix (Beasley 1987):

- **Row domination.** If the column set covering row $k$ is a subset of the columns
  covering row $i$, any solution covering $k$ also covers $i$: delete row $i$.
- **Column domination (covering only).** If $S_{j'} \supseteq S_j$ and
  $c_{j'} \le c_j$, delete column $j$. Never apply this to partitioning — the
  smaller column may be needed for exactness.
- **Forced columns.** A row covered by a single column fixes that column to 1;
  remove all rows it covers (and, in partitioning, delete every column that
  intersects them — this cascade is powerful).
- **Duplicate columns.** Keep the cheapest of each identical column; in packing,
  keep the most profitable.

Iterate the rules to a fixed point: each fixing can enable new dominations.

## Practical Challenges

**The set partitioning model is infeasible, or the solver finds no incumbent for
hours.** Partitioning feasibility is itself NP-complete, so do not expect the solver
to stumble into it. Add one artificial slack column per row with a cost above any
plausible over-cover penalty, or switch to the covering relaxation with calibrated
penalties. Seed a MIP start from a greedy cover with duplicates removed. Set
`MIPFocus = 1` to bias the search toward feasibility.

**The partitioning LP is massively degenerate and dual values swing wildly between
iterations.** Equality rows with many identical-cost columns create degenerate
vertices. Use barrier without crossover (`Method = 2`, `Crossover = 0`) when you only
need dual prices for pricing or fixing, perturb costs by tiny amounts, or stabilize
duals around a Lagrangian center as in CFT.

**Unicost instances give weak LP bounds and indifferent greedy choices.** With all
$c_j = 1$ the cost-effectiveness ratio collapses to coverage counts and ties are
everywhere. Break ties randomly across restarts (GRASP does this for free), use
Lagrangian multipliers to differentiate columns, and report gaps against the
Lagrangian bound rather than the raw LP when the LP is too slow.

**The incidence matrix does not fit in dense memory.** A 10,000 x 1,000,000 instance
is 10 GB dense but a few hundred MB sparse. Store columns as index lists or
`scipy.sparse` CSC; build Gurobi constraints from the sparse structure directly. The
dense-numpy code in this skill is for clarity at moderate sizes — swap the matrix
products for sparse ones without changing the algorithms.

**Branching on fractional x_j stalls branch-and-bound on partitioning models.**
Fixing a single column variable to 0 barely changes the LP, producing huge, unbalanced
trees. Use Ryan-Foster row-pair branching (same/different), which splits the solution
space evenly and remains compatible with column generation pricing.

**Heuristic covers carry hidden redundancy.** Greedy and GRASP constructions
routinely include early columns that later picks make unnecessary; reporting them
overstates cost by several percent. Always run reverse delete, and check the
validator's `max_coverage` output — values above 2 on most rows signal a sloppy
construction loop.

**Over-cover penalties distort the objective.** If the penalty for double-covering a
row is far above its real operational cost, the model buys expensive exact partitions
it does not need; far below, it spams duplicates. Price the penalty at the measured
cost of the real-world event (deadhead, double visit) and run a sensitivity sweep
over a 2x range to confirm solution stability.

**Identical and dominated columns inflate the model and create symmetry.** Column
generators (route enumerators, pairing builders) frequently emit duplicates and
dominated variants, multiplying symmetric optima and slowing the MIP. Run the
preprocessing reductions above after every generation batch, not just once.

## Tools & Libraries

| Library / resource | When to use | Note |
|---|---|---|
| gurobipy | Exact MIP/LP for all three variants | Fastest path to proven optimality; see milp-modeling-gurobi |
| HiGHS (highspy) | License-free exact solving | Strong on covering LPs; good MIP for moderate sizes |
| OR-Tools CP-SAT | Partitioning feasibility with rich side constraints | `add_exactly_one` maps directly; great at finding feasible points |
| SCIP / PySCIPOpt | Branch-and-price research codes | Pricer plugins for implicit-column masters |
| numpy | Heuristics on dense instances | All vectorized code in this skill |
| scipy.sparse | Large sparse incidence matrices | CSC for column slicing, CSR for row checks |
| pandas | Experiment result tables | One row per (instance, method, seed) run |
| OR-Library (Beasley 1990) | Benchmark SCP instances | Classes scp4-scp6, scpa-scpe, scpnr, unicost |

## Output Format

A complete answer to a covering/packing/partitioning task contains:

1. **Variant statement.** One sentence fixing the constraint sense (>= / = / <=),
   the objective direction, and any side constraints, plus the m x n size and
   density of the instance.
2. **Method and bound.** What was run (MIP, greedy, LP rounding, GRASP, Lagrangian)
   with parameters and seed, the best solution cost, and the best available lower
   (upper, for packing) bound with the resulting gap.
3. **Validator confirmation.** The output of `validate_solution` on the reported
   solution — never report a solution that has not passed it.
4. **Solution artifact.** The selected column indices (and, where meaningful, the
   row-to-column assignment), written to a file for nontrivial sizes.

A reporting template:

```text
Instance      : scp45 (m=200, n=1000, density=2.0%, costs in [1,100])
Variant       : set covering (Ax >= 1, minimize)
Method        : CFT Lagrangian heuristic, 300 subgradient iters, seed 42
Best cost     : 512.0       (validator: feasible=True, objective=512.0)
Lower bound   : 508.3       (Lagrangian dual, = LP bound up to convergence)
Gap           : 0.73 %
Time          : 1.8 s
Artifact      : results/scp45_seed42_solution.json (87 columns selected)
```

For method comparisons, add a table with one row per (method, seed) and columns
{cost, bound, gap %, time, n_selected}, aggregated over seeds with mean and best.
State explicitly which preprocessing reductions were applied, since they change the
effective instance.

## Questions to Ask

- Must every row be hit at least once, exactly once, or at most once — and what does
  an over-covered row mean physically in your application?
- Are the columns given explicitly as data, or generated from rules (routes,
  pairings, patterns)? Roughly how many are there?
- What are m, n, and the matrix density? Unicost or general costs?
- Are there side constraints beyond the row constraints (capacities, cardinality,
  incompatible column pairs)?
- Do you need a proven optimum, a bounded gap, or just a good solution within a time
  budget — and what is that budget?
- Is a Gurobi license available, or should the solution path use open-source tools?
- Do you have benchmark or historical instances to calibrate against, or should we
  generate synthetic ones with controlled density and cost structure?
- How will solutions be consumed downstream — do you need the row-to-column
  assignment, or just the selected columns and cost?

## Related Skills

- **grasp** — when the greedy-randomized construction here needs reactive alpha
  tuning, RCL design depth, or path relinking between elite covers.
- **column-generation** — when columns are implicit and the covering/partitioning
  model is the restricted master of a pricing loop or branch-and-price.
- **milp-modeling-gurobi** — when the exact models need richer gurobipy patterns:
  parameters, status handling, warm starts, and constraint-builder organization.
- **lagrangian-relaxation** — when the CFT-style subgradient loop needs step-size
  rules, convergence diagnostics, or different dualization choices.
- **vehicle-routing-problem** — when the set-partitioning master's columns are
  vehicle routes and the application is routing rather than crews or patterns.
