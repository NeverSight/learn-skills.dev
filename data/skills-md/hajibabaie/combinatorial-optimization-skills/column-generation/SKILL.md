---
name: column-generation
description: When the user wants to solve linear or integer programs whose variable set is too large to enumerate, by iterating between a restricted master problem and a reduced-cost pricing problem, up to full branch-and-price. Also use when the user mentions "column generation," "pricing problem," "restricted master problem," "branch-and-price," "Gilmore-Gomory," or when the problem has exponentially many variables such as patterns, routes, or crew schedules. For deriving the master from a compact model, see dantzig-wolfe-decomposition; for labeling algorithms used in pricing, see dynamic-programming.
---

# Column Generation

You are an expert in column generation and branch-and-price for large-scale linear and integer programming. This skill covers the restricted master / pricing loop, reduced-cost pricing oracles, convergence and dual bounds, stabilization, heuristic pricing, and branching rules that remain compatible with the pricing problem. Use the framework below to recognize when a problem calls for column generation, implement the loop correctly in gurobipy, and extend it to a full branch-and-price algorithm when the LP bound alone is not enough.

## Initial Assessment

Establish the following before writing any code:

- **Why are there too many variables?** Identify the combinatorial object a column represents: a cutting pattern, a vehicle route, a crew pairing, a machine schedule, a cluster. If columns cannot be described implicitly by a structured subproblem, column generation does not apply.
- **What is the master structure?** Set covering (`>=`), set partitioning (`==`), or a general linking system? Covering masters give nonnegative duals and more freedom in pricing; partitioning masters are needed when over-coverage is costed or infeasible.
- **What is the pricing problem and how hard is it?** Knapsack (pseudo-polynomial DP), shortest path with resources (labeling), matching, or an NP-hard problem you will solve as a small MIP? Pricing consumes 80-95% of runtime in mature codes; its complexity decides instance reach.
- **LP bound or integer solutions?** Decide up front: column generation alone gives the master LP bound plus a heuristic integer solution (price-and-branch). Proven integer optimality requires branch-and-price, which roughly triples implementation effort.
- **Problem size.** Number of master rows (items, customers, tasks), expected number of CG iterations (often 1-5x the row count), and pricing instance size. A 1,000-customer routing master with exact elementary pricing is a research project; a 200-item cutting-stock LP solves in seconds.
- **Solver availability.** Gurobi or another LP solver with reliable dual values for the master; the pricing solver can be custom code. For true branch-and-price with column generation at every node, check whether SCIP's pricer interface or a framework (Coluna.jl, VRPSolver) saves you from writing tree management yourself.
- **Dual stability risk.** Degenerate masters (set partitioning with many ties, identical items) cause oscillating duals and slow convergence. Plan for stabilization if the row count exceeds a few hundred or the master is highly degenerate.
- **Time budget and accuracy.** Is a bound within 0.5% in minutes acceptable (stop early via Lagrangian/Farley bounds), or do you need exact LP convergence?
- **Data format.** Confirm the instance source (OR-Library cutting stock, Solomon/CVRPLIB routing, custom) and the units of costs and capacities; reduced-cost tolerances must match the cost scale.
- **Validation plan.** On small instances, the CG master LP value must match the LP relaxation of the equivalent Dantzig-Wolfe reformulation, and branch-and-price must match a compact MIP solved directly. Build that cross-check first.

## Algorithm Anatomy

### The master problem and its restriction

Column generation solves a linear program whose columns are indexed by an exponentially large set $\Omega$:

$$
z_{MP} = \min \sum_{p \in \Omega} c_p \lambda_p
\quad \text{s.t.} \quad
\sum_{p \in \Omega} a_p \lambda_p \ge b, \qquad \lambda \ge 0 ,
$$

where each column $p$ has cost $c_p$ and coefficient vector $a_p \in \mathbb{R}^m$. The **restricted master problem (RMP)** is the same LP over a small subset $\Omega' \subset \Omega$. Solving the RMP yields primal values $\lambda^*$ and dual values $\pi \ge 0$ on the $m$ rows.

### Pricing and the optimality condition

The reduced cost of column $p$ is $\bar{c}_p = c_p - \pi^\top a_p$. The **pricing problem** computes

$$
\bar{c}^* = \min_{p \in \Omega} \; c_p - \pi^\top a_p
$$

by exploiting the structure of $\Omega$ (a knapsack over patterns, a resource-constrained shortest path over routes) instead of enumeration. Two outcomes:

- $\bar{c}^* \ge 0$: no column can improve the RMP; the current RMP solution is optimal for the full master LP. Stop.
- $\bar{c}^* < 0$: add the minimizing column (and optionally other negative-reduced-cost columns) to $\Omega'$ and re-solve.

This is the simplex method with the entering-variable step delegated to an optimization oracle. Convergence is finite because $\Omega$ is finite and the RMP value is non-increasing; in practice the iteration count is governed by dual stability, not by $|\Omega|$.

### Bounds available during the loop

The RMP value $z_{RMP}$ is an **upper** bound on $z_{MP}$ (a minimization over fewer columns). Two lower bounds close the gap before full convergence (Lübbecke & Desrosiers 2005, "Selected topics in column generation"):

- **Lagrangian bound.** If some optimal master solution satisfies $\sum_p \lambda_p \le \kappa$, then $z_{MP} \ge z_{RMP} + \kappa \, \bar{c}^*$. The bound is exact at convergence and lets you stop when $\lceil z_{RMP} + \kappa \bar{c}^* \rceil = \lceil z_{RMP} \rceil$ for integer-valued objectives.
- **Farley bound** (Farley 1990). For unit-cost covering masters ($c_p = 1$, $a_p \ge 0$): if the pricing optimum is $\zeta^* = \max_p \pi^\top a_p > 1$, then $\pi / \zeta^*$ is dual feasible for the full master, so $z_{MP} \ge z_{RMP} / \zeta^*$.

### Relation to Dantzig-Wolfe and Lagrangian relaxation

When the master comes from convexifying a block of constraints (Dantzig-Wolfe reformulation), the master LP value equals the Lagrangian dual bound obtained by dualizing the linking constraints (Geoffrion 1974, "Lagrangean relaxation for integer programming"). This bound dominates the compact LP relaxation, strictly so whenever the pricing polyhedron does not have integral vertices for free. That bound improvement is the usual reason to accept the engineering cost of column generation.

### Decision guidance

- **Use column generation when** the natural formulation is set covering/partitioning over combinatorial structures, the pricing problem has an efficient algorithm (DP, labeling, small MIP), and you need a bound stronger than the compact LP relaxation.
- **Do not use it when** a compact formulation solves within budget in a modern MIP solver, when pricing has no exploitable structure, or when the integrality gap of the master is large anyway (the stronger LP bound buys nothing).
- **Complexity picture.** Per iteration: one LP re-solve (warm-started dual simplex, cheap) plus one pricing call (dominant). Total iterations: typically $O(m)$ to a small multiple of $m$ with stabilization; unstabilized degenerate masters can need 10-50x more.

## Generic Master-Pricing Framework

The loop below is the reusable core. Everything problem-specific lives in the pricing oracle.

```text
COLUMN-GENERATION(rhs b, initial columns Omega', pricing oracle, tol)
    build RMP:  min sum(c_p * x_p : p in Omega')
                s.t. sum(a_p * x_p : p in Omega') >= b,  x >= 0
    repeat
        solve RMP                          -> primal x*, duals pi
        call pricing(pi)                   -> columns with cbar_p = c_p - pi^T a_p
        keep columns with cbar_p < -tol
        if none kept:
            return x*, z_RMP               # optimal for the full master LP
        add kept columns to the RMP        # warm-started dual simplex re-solve
    until iteration limit reached
```

Implementation notes baked into the code: columns are added with `gp.Column` so the model grows without rebuilding; duals are read only after checking `GRB.OPTIMAL`; the negative-reduced-cost filter is applied inside the loop so a sloppy oracle cannot stall it; and initial columns must make the RMP feasible (here, one column per row, or artificial variables in the branch-and-price section below).

```python
import gurobipy as gp
from gurobipy import GRB
from dataclasses import dataclass
from typing import Callable, Sequence


@dataclass(frozen=True)
class Column:
    """One master column: objective cost plus its nonzero row coefficients."""
    cost: float
    coeffs: tuple[tuple[int, float], ...]  # (row index, coefficient) pairs


# A pricing oracle maps RMP duals to columns with negative reduced cost.
# Returning [] certifies that no such column exists.
PricingOracle = Callable[[list[float]], list[Column]]


def solve_cg(
    rhs: Sequence[float],
    initial_columns: Sequence[Column],
    pricing: PricingOracle,
    max_iters: int = 1000,
    tol: float = 1e-6,
) -> tuple[float, list[Column], list[float]]:
    """Column generation for min c^T x s.t. A x >= rhs, x >= 0 with priced columns.

    Returns (master LP value, all RMP columns, their primal values).
    """
    model = gp.Model("rmp")
    model.Params.OutputFlag = 0
    rows = [model.addConstr(gp.LinExpr() >= rhs[i], name=f"row[{i}]")
            for i in range(len(rhs))]
    cols: list[Column] = []
    var_list: list[gp.Var] = []

    def add_column(col: Column) -> None:
        gcol = gp.Column([a for _, a in col.coeffs], [rows[i] for i, _ in col.coeffs])
        var_list.append(model.addVar(obj=col.cost, lb=0.0, column=gcol,
                                     name=f"x[{len(cols)}]"))
        cols.append(col)

    for col in initial_columns:
        add_column(col)

    for iteration in range(max_iters):
        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"RMP status {model.Status} at iteration {iteration}")
        duals = [r.Pi for r in rows]
        improving = [c for c in pricing(duals)
                     if c.cost - sum(duals[i] * a for i, a in c.coeffs) < -tol]
        if not improving:
            break  # pricing proves optimality of the master LP
        for col in improving:
            add_column(col)
    return model.ObjVal, cols, [v.X for v in var_list]


# Tiny smoke test: 3 covering rows, oracle scans a fixed 6-column universe.
universe = [
    Column(1.0, ((0, 1.0),)), Column(1.0, ((1, 1.0),)), Column(1.0, ((2, 1.0),)),
    Column(1.5, ((0, 1.0), (1, 1.0))), Column(1.5, ((1, 1.0), (2, 1.0))),
    Column(2.4, ((0, 1.0), (1, 1.0), (2, 1.0))),
]


def scan_pricing(duals: list[float]) -> list[Column]:
    """Toy oracle: return the most negative reduced-cost column of the universe."""
    best = min(universe, key=lambda c: c.cost - sum(duals[i] * a for i, a in c.coeffs))
    return [best]


obj, _, _ = solve_cg([1.0, 1.0, 1.0], universe[:3], scan_pricing)
print(f"{obj:.2f}")
# Expected: 2.40 -- the triple column (cost 2.4) replaces three singletons (cost 3.0)
```

A real oracle never enumerates a universe; the two worked examples below replace `scan_pricing` with a knapsack DP and a shortest-path labeling algorithm.

## Worked Example: Cutting Stock (Gilmore-Gomory)

Cut stock rolls of width $W$ into item widths $w_i$ to meet demands $d_i$, minimizing rolls used. A column is a **cutting pattern** $a \in \mathbb{Z}_{\ge 0}^n$ with $\sum_i w_i a_i \le W$. The master (Gilmore & Gomory 1961, "A linear programming approach to the cutting-stock problem"):

$$
z = \min \sum_{p \in P} x_p
\quad \text{s.t.} \quad
\sum_{p \in P} a_{ip} x_p \ge d_i \;\; \forall i, \qquad x_p \ge 0 .
$$

With duals $\pi_i \ge 0$, the reduced cost of pattern $a$ is $1 - \pi^\top a$, so pricing is an **unbounded integer knapsack**:

$$
\zeta^* = \max \Big\{ \sum_i \pi_i a_i : \sum_i w_i a_i \le W,\; a \in \mathbb{Z}_{\ge 0}^n \Big\},
$$

and an improving pattern exists iff $\zeta^* > 1$. The DP below runs in $O(nW)$ time and recovers the pattern by backtracking. For bounded counts ($a_i \le d_i$) switch to a bounded-knapsack DP; for huge $W$, solve pricing as a small integer program instead.

```python
def knapsack_pricing(width: int, sizes: list[int], duals: list[float]) -> tuple[float, list[int]]:
    """Unbounded integer knapsack: max sum_i duals[i]*a_i s.t. sum_i sizes[i]*a_i <= width.

    Returns (optimal value, pattern as item counts). Tabular DP, O(n * width).
    """
    best = [0.0] * (width + 1)
    choice = [-1] * (width + 1)  # item added at capacity c; -1 = none
    for c in range(1, width + 1):
        best[c], choice[c] = best[c - 1], -1
        for i, (w, profit) in enumerate(zip(sizes, duals)):
            if w <= c and best[c - w] + profit > best[c] + 1e-12:
                best[c], choice[c] = best[c - w] + profit, i
    pattern = [0] * len(sizes)
    c = width
    while c > 0:
        if choice[c] == -1:
            c -= 1
        else:
            pattern[choice[c]] += 1
            c -= sizes[choice[c]]
    return best[width], pattern


value, pattern = knapsack_pricing(9, [3, 4, 5], [0.33, 0.50, 0.55])
print(f"{value:.2f}", pattern)
# Expected: 1.05 [0, 1, 1] -- one width-4 plus one width-5 piece fills capacity 9
```

The full Gilmore-Gomory loop seeds the RMP with homogeneous patterns (as many copies of one item as fit), prices with the DP, and finally solves the last RMP as an integer program. That final step is the **price-and-branch heuristic**: it is restricted to generated columns, hence optimal only when its value hits $\lceil z_{LP} \rceil$. For cutting stock this almost always happens; the MIRUP conjecture (Scheithauer & Terno 1995) states $z_{IP} \le \lceil z_{LP} \rceil + 1$ and no counterexample beyond gap 1 is known.

```python
import gurobipy as gp
from gurobipy import GRB
# Continues the same module: uses knapsack_pricing from the previous block.


def solve_cutting_stock(
    width: int, sizes: list[int], demands: list[int], tol: float = 1e-6,
) -> tuple[float, int, dict[tuple[int, ...], int]]:
    """Gilmore-Gomory column generation, then the final RMP solved as an IP.

    Returns (LP bound, integer roll count, chosen patterns with multiplicities).
    """
    n = len(sizes)
    model = gp.Model("cutting_stock_rmp")
    model.Params.OutputFlag = 0
    cover = [model.addConstr(gp.LinExpr() >= demands[i], name=f"cover[{i}]")
             for i in range(n)]
    patterns: list[list[int]] = []
    use: list[gp.Var] = []

    def add_pattern(pattern: list[int]) -> None:
        col = gp.Column([float(a) for a in pattern], cover)
        use.append(model.addVar(obj=1.0, lb=0.0, column=col,
                                name=f"use[{len(patterns)}]"))
        patterns.append(pattern)

    for i in range(n):  # homogeneous starting patterns: as many of item i as fit
        start = [0] * n
        start[i] = width // sizes[i]
        add_pattern(start)

    while True:
        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"RMP status {model.Status}")
        duals = [c.Pi for c in cover]
        value, pattern = knapsack_pricing(width, sizes, duals)
        if value <= 1.0 + tol:  # min reduced cost 1 - value >= -tol: LP optimal
            break
        add_pattern(pattern)

    lp_bound = model.ObjVal
    for v in use:  # price-and-branch heuristic: integerize the final RMP
        v.VType = GRB.INTEGER
    model.optimize()
    if model.Status != GRB.OPTIMAL:
        raise RuntimeError(f"final IP status {model.Status}")
    chosen = {tuple(p): round(v.X) for p, v in zip(patterns, use) if v.X > 0.5}
    return lp_bound, round(model.ObjVal), chosen


lp, rolls, plan = solve_cutting_stock(100, [45, 36, 31, 14], [97, 610, 395, 211])
print(f"LP bound {lp:.3f}, integer rolls {rolls}, patterns used {len(plan)}")
# Expected: LP bound 452.250, integer rolls 453 -- ceil(452.25) = 453 proves optimality.
# Plan: 49 x (2,0,0,0), 206 x (0,2,0,2), 198 x (0,1,2,0).
```

## Worked Example: Vehicle Routing as Set Covering with Shortest-Path Pricing

The set-partitioning view of the capacitated VRP selects routes from the set $R$ of all capacity-feasible depot-to-depot routes (Desrochers, Desrosiers & Solomon 1992 established the CG approach for VRPTW). Using a covering relaxation (valid because triangle-inequality costs make over-coverage removable, and it keeps duals nonnegative):

$$
\min \sum_{r \in R} c_r \lambda_r
\quad \text{s.t.} \quad
\sum_{r \in R} a_{ir} \lambda_r \ge 1 \;\; \forall i \in N, \qquad \lambda \ge 0 ,
$$

where $a_{ir} = 1$ if route $r$ visits customer $i$. With duals $\pi_i$, the reduced cost of a route is $c_r - \sum_{i \in r} \pi_i$. Charging $\pi_i$ to every arc leaving customer $i$ gives arc reduced costs $\hat{d}_{ij} = d_{ij} - \pi_i$, and pricing becomes an **elementary shortest path problem with resource constraints (ESPPRC)**: find the cheapest elementary depot-to-depot walk respecting capacity. ESPPRC is NP-hard (Dror 1994), but a labeling algorithm with dominance solves practical sizes; this sketch uses a visited-customer bitmask, exact and fast up to roughly 15-20 customers. Production codes relax elementarity (see Advanced Techniques) and use bidirectional labeling (Righini & Salani 2006).

A label is dominated when another label at the same node is no worse in cost and load and has visited a subset of its customers (so it has at least the same extension options).

```python
import collections
from dataclasses import dataclass


@dataclass(frozen=True)
class Label:
    """Partial-path state: reduced cost, load, visited set, current node, path."""
    rcost: float
    load: int
    visited: int  # bitmask: bit i-1 set means customer i was visited
    node: int
    path: tuple[int, ...]


def espprc_pricing(
    dist: list[list[float]], demand: list[int], capacity: int,
    duals: list[float], max_routes: int = 10, tol: float = 1e-6,
) -> list[tuple[float, tuple[int, ...]]]:
    """Elementary shortest path with capacity, via labeling with dominance.

    Node 0 is the depot, customers are 1..n; duals[i-1] belongs to customer i
    and is charged on the arc leaving i: rc(i, j) = dist[i][j] - duals[i-1].
    Returns up to max_routes routes with reduced cost < -tol, most negative first.
    """
    n = len(demand) - 1
    start = Label(0.0, 0, 0, 0, (0,))
    store: dict[int, list[Label]] = {i: [] for i in range(n + 1)}
    store[0].append(start)
    queue = collections.deque([start])
    completed: list[tuple[float, tuple[int, ...]]] = []

    def dominates(a: Label, b: Label) -> bool:
        """a dominates b: no worse cost and load, visited a subset of b's."""
        return (a.rcost <= b.rcost + 1e-12 and a.load <= b.load
                and a.visited & ~b.visited == 0)

    while queue:
        lab = queue.popleft()
        if lab not in store[lab.node]:
            continue  # removed by dominance while waiting in the queue
        i = lab.node
        out_dual = duals[i - 1] if i != 0 else 0.0
        if i != 0:  # close the route at the depot
            rc = lab.rcost + dist[i][0] - out_dual
            if rc < -tol:
                completed.append((rc, lab.path + (0,)))
        for j in range(1, n + 1):
            if lab.visited >> (j - 1) & 1 or lab.load + demand[j] > capacity:
                continue
            new = Label(lab.rcost + dist[i][j] - out_dual, lab.load + demand[j],
                        lab.visited | 1 << (j - 1), j, lab.path + (j,))
            if any(dominates(old, new) for old in store[j]):
                continue
            store[j] = [old for old in store[j] if not dominates(new, old)]
            store[j].append(new)
            queue.append(new)
    completed.sort(key=lambda entry: entry[0])
    return completed[:max_routes]


toy_dist = [[0.0, 4.0, 5.0, 6.0],
            [4.0, 0.0, 2.0, 5.0],
            [5.0, 2.0, 0.0, 3.0],
            [6.0, 5.0, 3.0, 0.0]]
best = espprc_pricing(toy_dist, [0, 3, 4, 5], capacity=8, duals=[7.0, 7.0, 7.0])[0]
print(best)
# Expected: (-3.0, (0, 1, 2, 0)) -- cost 4+2+5=11 minus duals 7+7=14 gives -3
```

The master seeds with singleton routes (depot-customer-depot), prices with the labeling algorithm, and adds several negative columns per iteration -- returning the 5-10 best routes per pricing call typically cuts iteration counts by 3-5x at negligible cost.

```python
import gurobipy as gp
import numpy as np
from gurobipy import GRB
# Continues the same module: uses espprc_pricing from the previous block.


def route_cost(dist: list[list[float]], route: tuple[int, ...]) -> float:
    """Total arc length of a depot-to-depot route."""
    return sum(dist[a][b] for a, b in zip(route, route[1:]))


def solve_vrp_lp(
    dist: list[list[float]], demand: list[int], capacity: int, tol: float = 1e-6,
) -> tuple[float, float, list[tuple[int, ...]]]:
    """Set-covering master over routes, priced by ESPPRC labeling.

    Returns (LP bound, integer UB from the final RMP as an IP, routes in that UB).
    """
    n = len(demand) - 1
    model = gp.Model("vrp_rmp")
    model.Params.OutputFlag = 0
    cover = [model.addConstr(gp.LinExpr() >= 1, name=f"visit[{i}]")
             for i in range(1, n + 1)]
    pool: list[tuple[int, ...]] = []
    use: list[gp.Var] = []

    def add_route(route: tuple[int, ...]) -> None:
        members = sorted(set(route) - {0})
        col = gp.Column([1.0] * len(members), [cover[i - 1] for i in members])
        use.append(model.addVar(obj=route_cost(dist, route), lb=0.0,
                                column=col, name=f"r[{len(pool)}]"))
        pool.append(route)

    for i in range(1, n + 1):  # singleton seed routes keep the RMP feasible
        add_route((0, i, 0))

    while True:
        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"RMP status {model.Status}")
        duals = [c.Pi for c in cover]
        new_routes = espprc_pricing(dist, demand, capacity, duals, tol=tol)
        if not new_routes:
            break
        for _, route in new_routes:
            add_route(route)

    lp_bound = model.ObjVal
    for v in use:
        v.VType = GRB.BINARY
    model.optimize()
    if model.Status != GRB.OPTIMAL:
        raise RuntimeError(f"final IP status {model.Status}")
    chosen = [r for r, v in zip(pool, use) if v.X > 0.5]
    return lp_bound, model.ObjVal, chosen


rng = np.random.default_rng(7)
points = rng.uniform(0, 100, size=(8, 2))  # row 0 = depot, rows 1..7 = customers
D = np.linalg.norm(points[:, None, :] - points[None, :, :], axis=2)
demand = [0] + [int(d) for d in rng.integers(3, 9, size=7)]
lp_b, ub, routes = solve_vrp_lp(D.tolist(), demand, capacity=15)
print(f"LP bound {lp_b:.2f}, integer over columns {ub:.2f}, {len(routes)} routes")
# Expected: LP bound 468.41, integer 482.85 with 4 routes:
# (0,7,0), (0,5,6,0), (0,4,1,0), (0,3,2,0) -- each load <= 15, all customers covered
```

The 3% gap between 468.41 and 482.85 is the price-and-branch gap: the IP over generated columns is a heuristic. Closing it exactly requires branch-and-price.

## Branch-and-Price

When the rounded master IP is not provably optimal, embed column generation in branch-and-bound: solve the master LP by CG at **every** tree node (Barnhart, Johnson, Nemhauser, Savelsbergh & Vance 1998, "Branch-and-price: column generation for solving huge integer programs").

**Why you must not branch on master variables.** Branching $\lambda_p = 0$ forbids one specific column, but the pricing oracle will regenerate it: you would need a "best column excluding a list" oracle, which destroys the DP/labeling structure and yields a hopelessly unbalanced tree ($\lambda_p = 1$ is strong, $\lambda_p = 0$ is nearly vacuous). Correct branching rules act on quantities the pricing problem can absorb natively:

- **Ryan-Foster branching** (Ryan & Foster 1981) for set partitioning. In any fractional basic solution there exist two rows $i, j$ with fractional pair coverage $f_{ij} = \sum_{p:\, a_{ip} = a_{jp} = 1} \lambda_p \in (0,1)$. Branch SAME ($i$ and $j$ always together in a column) versus DIFFER (never together). Pricing absorbs SAME by merging the items (or adding $y_i = y_j$) and DIFFER by a conflict constraint ($y_i + y_j \le 1$). If every pair coverage is integral, the basic solution is integral -- so this rule is complete.
- **Branching on original variables** for routing and flow structures: the aggregated arc flow $x_{ij} = \sum_r a^r_{ij} \lambda_r$ is a compact-model variable. Fixing $x_{ij} = 0$ deletes arc $(i,j)$ from the pricing network and drops incompatible columns; $x_{ij} = 1$ forces the arc by deleting competing arcs. The pricing problem type is unchanged (Desrosiers & Lübbecke 2011 survey these schemes; Vanderbeck 2000 gives a generic framework).

The implementation below does Ryan-Foster branch-and-price for **bin packing** (cutting stock with unit demands). Pricing is a 0-1 knapsack solved as a small Gurobi MIP because the SAME/DIFFER side constraints break the plain DP; conflict-aware DP or labeling is the high-performance alternative.

```python
import gurobipy as gp
from gurobipy import GRB


def bp_pricing(
    sizes: list[int], capacity: int, duals: list[float],
    same: list[tuple[int, int]], differ: list[tuple[int, int]],
    tol: float = 1e-6,
) -> frozenset[int] | None:
    """Max-profit 0-1 knapsack pricing with Ryan-Foster side constraints.

    same: item pairs forced together-or-absent; differ: pairs never together.
    Returns the best column as an item set if its reduced cost < -tol, else None.
    """
    m = gp.Model("bp_pricing")
    m.Params.OutputFlag = 0
    n = len(sizes)
    y = m.addVars(n, vtype=GRB.BINARY, name="y")
    m.addConstr(gp.quicksum(sizes[i] * y[i] for i in range(n)) <= capacity,
                name="cap")
    for k, (i, j) in enumerate(same):
        m.addConstr(y[i] == y[j], name=f"same[{k}]")
    for k, (i, j) in enumerate(differ):
        m.addConstr(y[i] + y[j] <= 1, name=f"differ[{k}]")
    m.setObjective(gp.quicksum(duals[i] * y[i] for i in range(n)), GRB.MAXIMIZE)
    m.optimize()
    if m.Status != GRB.OPTIMAL:
        return None
    if 1.0 - m.ObjVal < -tol:  # column cost is 1 (one bin)
        return frozenset(i for i in range(n) if y[i].X > 0.5)
    return None


col = bp_pricing([6, 6, 5], 12, [0.6, 0.6, 0.5], same=[], differ=[])
print(sorted(col))
# Expected: [0, 1] -- profit 1.2 > 1, reduced cost -0.2; items 6+6 fill the bin
```

The tree driver keeps a global column pool, filters it for compatibility with each node's SAME/DIFFER decisions, runs CG to optimality at the node, prunes by $\lceil z_{node} \rceil \ge$ incumbent (valid because bin counts are integral), and branches on the pair coverage closest to 1/2. The node master uses equality rows (true set partitioning) so the Ryan-Foster integrality argument applies; an artificial column keeps every node LP feasible and flags genuinely infeasible nodes.

```python
import collections
import math

import gurobipy as gp
from gurobipy import GRB
# Continues the same module: uses bp_pricing from the previous block.


def node_lp(
    sizes: list[int], capacity: int, pool: list[frozenset[int]],
    same: list[tuple[int, int]], differ: list[tuple[int, int]],
    tol: float = 1e-6,
) -> tuple[float, list[tuple[frozenset[int], float]]] | None:
    """Column generation at one branch-and-price node.

    Returns (node LP value, support of the solution) or None if infeasible.
    """
    n = len(sizes)

    def compatible(col: frozenset[int]) -> bool:
        return (all((i in col) == (j in col) for i, j in same)
                and all(not (i in col and j in col) for i, j in differ))

    model = gp.Model("node_rmp")
    model.Params.OutputFlag = 0
    cover = [model.addConstr(gp.LinExpr() == 1, name=f"item[{i}]")
             for i in range(n)]
    art = model.addVar(obj=float(2 * n), lb=0.0, name="art",
                       column=gp.Column([1.0] * n, cover))
    cols: list[frozenset[int]] = []
    use: list[gp.Var] = []

    def add(col: frozenset[int]) -> None:
        gcol = gp.Column([1.0] * len(col), [cover[i] for i in sorted(col)])
        use.append(model.addVar(obj=1.0, lb=0.0, column=gcol,
                                name=f"p[{len(cols)}]"))
        cols.append(col)

    for col in pool:
        if compatible(col):
            add(col)

    while True:
        model.optimize()
        if model.Status != GRB.OPTIMAL:
            return None
        duals = [c.Pi for c in cover]
        new_col = bp_pricing(sizes, capacity, duals, same, differ, tol)
        if new_col is None:
            break
        if new_col not in pool:
            pool.append(new_col)  # share across the whole tree
        add(new_col)

    if art.X > tol:
        return None  # no compatible columns can cover every item
    return model.ObjVal, [(c, v.X) for c, v in zip(cols, use) if v.X > tol]


def branch_and_price(sizes: list[int], capacity: int) -> tuple[int, list[frozenset[int]]]:
    """Ryan-Foster branch-and-price for bin packing. Returns (bins, packing)."""
    n = len(sizes)
    pool: list[frozenset[int]] = [frozenset([i]) for i in range(n)]
    incumbent_value, incumbent = n + 1, []
    stack: list[tuple[list[tuple[int, int]], list[tuple[int, int]]]] = [([], [])]
    tol = 1e-6

    while stack:
        same, differ = stack.pop()
        result = node_lp(sizes, capacity, pool, same, differ, tol)
        if result is None:
            continue
        lp_value, frac = result
        if math.ceil(lp_value - tol) >= incumbent_value:
            continue  # bound: this node cannot beat the incumbent
        pair_use: dict[tuple[int, int], float] = collections.defaultdict(float)
        for col, val in frac:
            for i in col:
                for j in col:
                    if i < j:
                        pair_use[(i, j)] += val
        fractional = {p: v for p, v in pair_use.items() if tol < v < 1.0 - tol}
        if not fractional:  # integral by the Ryan-Foster argument
            packing = [col for col, val in frac if val > 0.5]
            if len(packing) < incumbent_value:
                incumbent_value, incumbent = len(packing), packing
            continue
        i, j = min(fractional, key=lambda p: abs(fractional[p] - 0.5))
        stack.append((same, differ + [(i, j)]))   # DIFFER child explored second
        stack.append((same + [(i, j)], differ))   # SAME child explored first (DFS)
    return incumbent_value, incumbent


bins, packing = branch_and_price([6, 6, 5, 5, 5, 4, 4, 4, 2], capacity=12)
print(bins, [sorted(c) for c in packing])
# Expected: 4 bins, e.g. [[3], [5, 6, 7], [2, 4, 8], [0, 1]] -- a partition of all
# nine items with every bin load <= 12; the LP bound 41/12 rounds up to 4.
```

Engineering notes that carry to real codes: process children depth-first with the SAME child first (it fixes structure fastest and finds incumbents early); share the column pool globally and filter per node rather than regenerating; finish each node's CG before pruning, because the node LP value is only a valid bound at pricing convergence (or use the Lagrangian bound mid-loop); and for minimization masters with integer costs, prune with the ceiling of the node bound.

## Advanced Techniques

### Dual stabilization

Unstabilized CG sends extreme dual points to the pricing oracle, and the dual sequence oscillates -- the cutting-plane view of the master dual explains why (each column is a cut in dual space; Kelley-style methods are known to zigzag). Remedies in increasing sophistication: boxstep trust regions on duals (Marsten, Hogan & Blankenship 1975), penalty stabilization with slacks around a stability center (du Merle, Villeneuve, Desrosiers & Hansen 1999, "Stabilized column generation"), and **dual-price smoothing** (Wentges 1997), which prices at a convex combination of the best dual point seen and the current RMP duals. Smoothing is the best effort-to-benefit ratio: 10 lines of code, often 2-10x fewer iterations, and it can be automated (Pessoa, Sadykov, Uchoa & Vanderbeck 2018).

```python
import numpy as np


class WentgesSmoothing:
    """Dual-price smoothing: price at pi_sep = alpha*center + (1-alpha)*pi_out.

    The stability center is the dual point with the best Lagrangian bound so
    far. A misprice (no improving column at pi_sep although pi_sep != pi_out)
    must trigger a re-price directly at pi_out before declaring convergence.
    """

    def __init__(self, alpha: float = 0.8) -> None:
        self.alpha = alpha
        self.center: np.ndarray | None = None
        self.best_bound = -np.inf

    def separation_point(self, pi_out: list[float]) -> list[float]:
        """Smoothed duals to hand to the pricing oracle."""
        out = np.asarray(pi_out, dtype=float)
        if self.center is None:
            self.center = out.copy()
        return (self.alpha * self.center + (1.0 - self.alpha) * out).tolist()

    def update(self, pi_sep: list[float], lagrangian_bound: float) -> None:
        """Move the center to pi_sep whenever it improves the Lagrangian bound."""
        if lagrangian_bound > self.best_bound:
            self.best_bound = lagrangian_bound
            self.center = np.asarray(pi_sep, dtype=float).copy()


smooth = WentgesSmoothing(alpha=0.5)
smooth.update([1.0, 1.0], lagrangian_bound=10.0)
print(smooth.separation_point([3.0, 5.0]))
# Expected: [2.0, 3.0] -- midpoint of center (1,1) and RMP duals (3,5)
```

Typical schedule: start with $\alpha \in [0.7, 0.9]$, reduce $\alpha$ on a misprice, reset toward 0 near convergence so the final optimality proof prices at the true RMP duals.

### Lower bounds and early termination

Compute a valid lower bound at every iteration and stop when it meets the rounded RMP value. The Lagrangian bound $z_{RMP} + \kappa\,\bar{c}^*$ needs an a-priori bound $\kappa$ on the column count (vehicle limit, total demand over smallest pattern). For unit-cost covering masters, Farley's bound needs nothing extra:

```python
def farley_bound(rmp_value: float, pricing_value: float) -> float:
    """Farley (1990) bound for unit-cost covering masters: z* >= z_RMP / zeta.

    Valid whenever the pricing optimum zeta = max pi^T a exceeds 1; scaling the
    RMP duals by 1/zeta makes them dual feasible for the full master.
    """
    return rmp_value / max(pricing_value, 1.0)


print(farley_bound(500.0, 1.25))
# Expected: 400.0 -- so an RMP at 500 with pricing value 1.25 is within 25% of optimal
```

For integer objectives (rolls, bins, vehicles), terminate as soon as $\lceil \text{LB} \rceil = \lceil z_{RMP} \rceil$: the LP tail contributes nothing to the integer bound.

### Heuristic and partial pricing

The pricing oracle only needs to be exact at the **final** iteration. Run a cheap heuristic first (greedy knapsack filling by $\pi_i / w_i$; labeling with an aggressive dominance that drops the visited-set test) and call the exact oracle only when the heuristic finds no negative column. In multi-subproblem settings (one pricing problem per vehicle type or machine), use partial pricing: stop at the first subproblem that yields negative columns and round-robin the starting point. Both tricks routinely cut wall time 2-5x without affecting correctness.

### Column pool management

Add 5-30 diverse negative columns per iteration, not just the single best -- diversity matters more than depth (columns covering different rows help the LP most). The RMP grows; when it exceeds, say, 10x the row count, delete non-basic columns whose reduced cost stayed above a threshold for many iterations, but keep them in an external pool and re-check the pool (cheap dot products) before invoking the expensive oracle. In branch-and-price, the pool is global and per-node compatibility filtering replaces deletion.

### Pricing relaxations for routing: ng-routes and decremental state space

Exact ESPPRC labeling is exponential in the visited set. Relaxations trade bound quality for speed while keeping validity: $q$-route relaxations allow repeated customers (weakest, fastest); **ng-route** relaxations (Baldacci, Mingozzi & Roberti 2011) forbid only cycles within small per-customer neighborhoods, recovering most of the elementary bound at a fraction of the cost; decremental state-space relaxation (Righini & Salani 2008) starts non-elementary and re-adds offending customers iteratively. Bidirectional labeling with a merge at half of the capacity resource roughly halves the label count. See **dynamic-programming** for the underlying labeling machinery.

## Practical Challenges

**The master is degenerate and the duals oscillate; iteration counts explode.** Set partitioning masters with many similar columns are massively degenerate: the RMP value stalls while duals jump between extreme alternative optima. Apply Wentges smoothing first; if stalling persists, add a boxstep trust region or use the barrier method without crossover (`Method=2`, `Crossover=0`) to obtain interior, well-centered duals. Interior duals alone often halve iteration counts on partitioning masters.

**The tail of the run makes no progress (tailing-off).** Hundreds of iterations improve the RMP by less than 0.01%. Compute the Lagrangian or Farley lower bound each iteration and stop at $\lceil \text{LB} \rceil = \lceil z_{RMP} \rceil$ when the objective is integral; otherwise stop at a relative gap of 1e-6. Do not run CG to exact LP convergence inside a branch-and-price node unless the node bound decides pruning.

**Pricing keeps returning a column that is already in the RMP.** This signals an inconsistency: duals read from a non-optimal basis, a sign error in the reduced cost (covering rows give $\pi \ge 0$; equality rows give free duals -- check the convention), or a tolerance mismatch where pricing uses a tighter threshold than the LP's feasibility tolerance. Assert that a returned column's reduced cost recomputed from RMP duals is below `-tol` before adding it; deduplicate columns by a canonical key (sorted item tuple) as a backstop.

**The initial RMP is infeasible, or branching makes it infeasible.** Seed covering masters with singleton or homogeneous columns; for partitioning masters or branched nodes where such columns are incompatible, add artificial variables with a cost exceeding any optimal value (not an astronomic big-M, which wrecks duals) and declare the node infeasible if an artificial stays positive at convergence. SCIP's alternative is Farkas pricing: generate columns that reduce infeasibility using the dual ray.

**The integer solution over generated columns is taken as optimal.** Price-and-branch (integerize the final RMP) is a heuristic: columns needed by the integer optimum may never have been generated because they price out positive at the LP optimum. Report the gap against $\lceil z_{LP} \rceil$ honestly; if it is nonzero and matters, implement branch-and-price -- there is no shortcut.

**Exact ESPPRC pricing dominates runtime and blows up on 50+ customer instances.** Switch the exact oracle to ng-route labeling, add heuristic pricing rounds in front, use bidirectional labeling, and cap labels per node with a cost-based cutoff. Confirm bound validity after each relaxation: the master LP value with relaxed pricing is still a valid lower bound for the original problem, just possibly weaker.

**Numerical tolerances cause endless loops or premature stops.** A pricing oracle that declares "no negative column" at `-1e-9` while the LP works at a 1e-6 feasibility tolerance can loop forever on re-added columns, or stop with slightly suboptimal masters. Use one tolerance (1e-6 on normalized costs) across master and pricing, scale costs so they are within a few orders of magnitude, and never compare raw floating-point reduced costs to exact zero.

**Branching slows pricing to a crawl deep in the tree.** Every SAME/DIFFER pair or fixed arc adds constraints to the pricing problem; MIP-based pricing degrades fastest. Prefer branching rules that map to graph operations (arc deletion) over side constraints, branch on the most fractional aggregated quantity to keep the tree shallow, and apply strong branching on a small candidate set when node counts matter more than node time.

## Tools & Libraries

| Library | When to use | Note |
|---|---|---|
| gurobipy | RMP solving, MIP pricing, price-and-branch | Reliable duals; `gp.Column` adds columns without rebuilding the model |
| PySCIPOpt | True branch-and-price via the `Pricer` plugin | Only mainstream Python path where the solver tree calls your pricer at every node, including Farkas pricing |
| HiGHS (highspy) | Free LP master when no Gurobi license | Fast dual simplex; manage the CG loop yourself |
| OR-Tools CP-SAT | Pricing subproblems with awkward side constraints | Good at conflict/logic-heavy pricing where DP breaks |
| cspy | Resource-constrained shortest-path pricing | Ready-made labeling (bidirectional, elementary) for routing pricing |
| networkx | Pricing network manipulation, arc deletions under branching | Prototype-grade speed; switch to adjacency arrays for performance |
| Coluna.jl (Julia) | Full branch-cut-and-price framework | Worth crossing the language boundary for research-grade BCP |
| VRPSolver (BaPCod) | State-of-the-art BCP for routing-like models | Model as a resource-constrained-path master; heavy but dominant on VRP variants |

## Output Format

A complete column-generation deliverable contains:

1. **Model statement.** Master LP/IP with row meaning, column definition, and the pricing problem written as an optimization problem with the dual-dependent objective. State the covering-vs-partitioning choice and why.
2. **Convergence log**, one row per iteration (print every iteration or every k-th):

| iter | z_RMP | min reduced cost | lower bound | columns added | RMP size | pricing time (s) |
|---|---|---|---|---|---|---|
| 1 | 481.0 | -3.42 | 411.9 | 8 | 15 | 0.04 |
| 2 | 472.3 | -1.17 | 446.0 | 6 | 21 | 0.05 |
| 14 | 452.25 | 0.00 | 452.25 | 0 | 87 | 0.06 |

3. **Solution-quality report.** Master LP bound; best integer value and how it was obtained (price-and-branch or branch-and-price); absolute and relative gap; for branch-and-price additionally node count, deepest level, and incumbent history.
4. **Timing split.** Total time decomposed into master re-solves vs pricing calls vs tree overhead; this tells the reader where tuning effort should go.
5. **Validated solution artifact.** The chosen columns in domain terms (patterns with multiplicities, routes with loads) plus an independent feasibility check: every demand met / every customer visited exactly once, every column respects its internal constraints (capacity, width), objective recomputed from raw data and matched against the solver value.
6. **Reproducibility block.** Instance source or generator seed, solver versions, parameter settings (tolerances, smoothing alpha, columns-per-iteration), and the stopping rule that ended the run.

## Questions to Ask

- What combinatorial object does one column represent, and what makes enumerating all of them impossible?
- Is the master naturally set covering or set partitioning -- is over-coverage harmless, costed, or infeasible?
- Do you need the LP bound only, a good integer solution, or proven integer optimality (branch-and-price)?
- What algorithm fits the pricing problem -- knapsack DP, shortest-path labeling, or a small MIP -- and how large is one pricing instance?
- How many master rows, and what iteration budget does that imply with and without stabilization?
- Are there side constraints in the master beyond covering rows (vehicle count limits, budgets) that change the dual structure?
- Which solver licenses are available, and does the project justify SCIP/Coluna for tree-integrated pricing?
- Is there a small-instance ground truth (compact MIP) to validate the master bound and the final solution against?
- What are the cost units and magnitudes, so reduced-cost tolerances can be set sanely?

## Related Skills

- **dantzig-wolfe-decomposition** — when the master problem must first be derived from a compact block-angular model; explains convexity rows and why the CG bound equals the Lagrangian dual.
- **cutting-stock** — when the application is trim-loss minimization itself; covers pattern models, integer rounding, and compact alternatives beyond the CG mechanics shown here.
- **linear-programming-fundamentals** — when dual values, reduced costs, or degeneracy in the RMP need deeper grounding; CG is simplex pricing delegated to an oracle.
- **branch-and-bound** — when designing the tree around the CG node solver: node selection, incumbent management, and bounding discipline carry over directly to branch-and-price.
- **dynamic-programming** — when building pricing oracles: knapsack recursions and resource-constrained shortest-path labeling are the two workhorse pricing algorithms.
