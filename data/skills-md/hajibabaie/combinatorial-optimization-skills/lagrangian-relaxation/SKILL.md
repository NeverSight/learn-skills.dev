---
name: lagrangian-relaxation
description: When the user wants to compute strong dual bounds for integer programs by dualizing complicating constraints, optimizing the Lagrangian dual with subgradient methods, and recovering feasible solutions with Lagrangian heuristics. Also use when the user mentions "Lagrangian relaxation," "subgradient," "Lagrangian bound," "dualize constraints," "Lagrangian heuristic," or when a MIP would be easy except for a few coupling constraints. For LP duality foundations, see linear-programming-fundamentals; for the column-generation view of the same bound, see dantzig-wolfe-decomposition.
---

# Lagrangian Relaxation

You are an expert in Lagrangian relaxation for integer programming. This skill covers selecting which constraints to dualize, evaluating the Lagrangian dual, subgradient optimization with practical step-size rules, interpreting the duality gap, Lagrangian heuristics for primal recovery, and honest bound comparison against LP relaxations. Use the framework below to derive the relaxation on paper first, then implement the oracle, the multiplier update, and the heuristic as three separable pieces.

## Initial Assessment

Establish these points before writing any model or code:

- **Coupling structure.** Identify which constraints make the problem hard. Ask: if I delete this constraint family, what remains? The remainder must decompose or become polynomially solvable, otherwise relaxation buys nothing.
- **Subproblem algorithm.** Name the algorithm that solves the relaxed subproblem (closed form, sort, shortest path, knapsack DP, assignment) and its complexity per oracle call. If you cannot name it, reconsider the dualization.
- **Integrality property check.** Determine whether the subproblem's LP relaxation has integral extreme points. If it does, the Lagrangian dual equals the LP bound (Geoffrion 1974) and the value of the exercise is speed and heuristics, not a tighter bound. Decide whether that is acceptable.
- **Number of multipliers.** One multiplier per dualized row. Hundreds to a few thousand is comfortable for subgradient methods; far more suggests dualizing a different family or aggregating.
- **Constraint sense.** Equality rows get free multipliers; inequality rows get sign-constrained multipliers with projection. Get this right before coding.
- **Purpose of the bound.** Standalone quality certificate, bound inside a custom branch-and-bound, or guidance for a heuristic? This sets the iteration budget and the stopping tolerance.
- **Upper-bound source.** The Polyak step size needs a finite upper bound. Plan the Lagrangian heuristic (or an external construction heuristic) before tuning the dual loop; see warm-starts-and-initial-solutions.
- **Data properties.** Integer capacities or weights enable pseudo-polynomial DP subproblems. Cost magnitudes affect multiplier scaling; consider normalizing costs to a common range.
- **Verification baseline.** Decide how you will validate: solve small instances exactly with a MIP solver, and compute the LP relaxation of the same formulation you compare against (weak vs strong formulations give different z_LP).
- **Time budget.** An oracle call is usually cheap; budget iterations (200-1000 typical) and decide how often the heuristic runs (every 1-10 iterations).

## Relaxation Anatomy and the Lagrangian Dual

### The construction

Start from a minimization integer program with the constraints split into a complicating family and a tractable remainder:

$$ z_{IP} = \min \{ c^\top x : Ax \ge b, \; Dx \ge d, \; x \in X \} $$

where $X$ encodes integrality and simple bounds, $Dx \ge d$ is kept, and $Ax \ge b$ (m rows) is the complicating family. Dualize the complicating rows with multipliers $\lambda \ge 0$:

$$ L(\lambda) = \min_{x \in X, \, Dx \ge d} \; c^\top x + \lambda^\top (b - Ax) $$

For every $\lambda \ge 0$, $L(\lambda) \le z_{IP}$: any feasible $x$ for the original problem satisfies $b - Ax \le 0$, so the penalty term is non-positive at feasible points (weak duality). Dualized equality rows take free multipliers and the bound argument still holds. The best bound is the **Lagrangian dual**:

$$ z_{LD} = \max_{\lambda \ge 0} L(\lambda) $$

Properties of $L$ that drive every algorithm in this skill:

- $L$ is concave and piecewise linear in $\lambda$ — one linear piece per subproblem solution $x$.
- $L$ is not differentiable where the subproblem has multiple optima, which is exactly where the maximum tends to sit.
- If $x(\lambda)$ solves the subproblem at $\lambda$, then $g = b - Ax(\lambda)$ is a **subgradient** of $L$ at $\lambda$. Positive components mean the row is violated by the subproblem solution; the multiplier should rise.

### Bound strength and the integrality property

Geoffrion (1974), "Lagrangean relaxation for integer programming," gives the convexification view:

$$ z_{LD} = \min \{ c^\top x : Ax \ge b, \; x \in \mathrm{conv}(\{x \in X : Dx \ge d\}) \} $$

Consequences you should state explicitly in any deliverable:

- $z_{LP} \le z_{LD} \le z_{IP}$ always (minimization), where $z_{LP}$ is the LP relaxation of the formulation containing both constraint families.
- If the subproblem has the **integrality property** (its LP relaxation already has integral extreme points), then $\mathrm{conv}(\cdot)$ adds nothing and $z_{LD} = z_{LP}$. You gain speed and a heuristic, not a tighter bound.
- If the subproblem lacks the integrality property (knapsack, spanning-tree-with-degree, TSP 1-tree), $z_{LD}$ can strictly dominate $z_{LP}$. The historical origin is Held & Karp (1970, 1971), who used 1-tree relaxations to produce TSP bounds far stronger than the assignment LP.
- $z_{LD}$ is exactly the bound of the Dantzig-Wolfe master obtained by convexifying the same subproblem — the two methods compute the same number by different algorithms (see dantzig-wolfe-decomposition).

### Choosing constraints to dualize

Score each candidate constraint family on five criteria:

| Criterion | Question | Red flag |
|---|---|---|
| Subproblem tractability | Does removal leave a polynomial or pseudo-polynomial problem? | Subproblem still NP-hard with no small DP |
| Separability | Does the subproblem split into independent blocks (per machine, per facility, per period)? | One monolithic subproblem as big as the original |
| Bound strength | Does the subproblem lack the integrality property? | Integrality property holds and you needed a tighter bound |
| Multiplier count | How many rows are dualized? | Tens of thousands of multipliers with slow oracle |
| Primal recovery | Is it easy to repair subproblem solutions into feasible ones? | Dualized constraints are the hard feasibility core |

When two dualizations are tractable, prefer the one whose subproblem lacks the integrality property (stronger bound), unless its oracle is much slower or repair is much harder. The GAP example below works through this trade-off concretely.

### The subgradient method

Since $L$ is concave but non-smooth, the workhorse is projected subgradient ascent (Polyak 1969; validated for integer programming by Held, Wolfe & Crowder 1974):

$$ \lambda^{k+1} = P\big(\lambda^k + t_k \, g^k\big), \qquad g^k = b - A x(\lambda^k) $$

where $P$ projects sign-constrained multipliers onto the nonnegative orthant and leaves free multipliers untouched. Step-size rules:

| Rule | Formula | Convergence | Practice |
|---|---|---|---|
| Polyak / Held-Wolfe-Crowder | $t_k = \theta_k (UB - L(\lambda^k)) / \lVert g^k \rVert^2$, $\theta_k \in (0,2]$ | To $z_{LD}$ if $UB \ge z_{LD}$ | Default. Start $\theta = 2$, halve after 15-30 iterations without bound improvement |
| Divergent series | $t_k = a/(b + k)$ with $\sum t_k = \infty$, $t_k \to 0$ | Guaranteed, slow | Fallback when no finite UB exists |
| Constant | $t_k = t$ | Only to a neighborhood | Avoid except for quick prototyping |

Stopping criteria, in priority order: (1) $UB - L^{best} \le$ tolerance — optimality proven; (2) $\lVert g \rVert = 0$ — the subproblem solution satisfies all dualized rows and $\lambda$ is a dual maximizer; (3) $\theta$ below a floor — the method has stalled; (4) iteration limit.

### When to choose Lagrangian relaxation

- **Use it** when the coupling structure is clean, when you need bounds cheaper than solving large LPs at every node of a custom branch-and-bound, when the subproblem lacks the integrality property, or when the subproblem solutions feed a natural repair heuristic.
- **Skip it** when the full MIP solves within budget (just solve it), when no dualization leaves a tractable subproblem, or when you need the exact convexified bound with clean termination — then a column-generation/Dantzig-Wolfe master is the better algorithm for the same bound.

## Generic Subgradient Framework

The decomposition logic lives in the oracle; the dual loop is problem-independent. Skeleton first:

```text
SUBGRADIENT OPTIMIZATION of  z_LD = max_lam L(lam)      (primal: minimization)

input : oracle(lam) -> (L(lam), subgradient g, subproblem solution)
        optional Lagrangian heuristic(lam, solution) -> feasible UB
        theta in (0, 2], patience K, shrink factor sigma, tolerances
output: best bound L*, best multipliers lam*, best feasible UB

lam <- lam0 (zeros, or a warm start such as LP duals)
L* <- -inf; UB <- +inf; stall <- 0
repeat
    (L, g, x_sub) <- oracle(lam)                # solve the easy subproblem
    if L > L*: L* <- L; lam* <- lam; stall <- 0  else stall <- stall + 1
    every few iterations: UB <- min(UB, heuristic(lam, x_sub))
    stop if UB - L* <= tol            # gap closed: L* is proven optimal value
    stop if ||g|| = 0                 # lam is a dual maximizer
    if stall >= K: theta <- sigma * theta; stall <- 0
    stop if theta < theta_min
    t <- theta * (UB - L) / ||g||^2   # Polyak step toward the target UB
    lam <- lam + t * g
    project lam_i <- max(0, lam_i) on rows dualized from inequalities
until iteration limit
```

The implementation below is reused by both worked examples. The oracle owns all problem knowledge; the loop only sees values, subgradients, and an opaque subproblem solution that it forwards to the heuristic.

```python
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

import numpy as np

Oracle = Callable[[np.ndarray], tuple[float, np.ndarray, Any]]
Heuristic = Callable[[np.ndarray, Any], float]


@dataclass
class SubgradientLog:
    """Per-iteration history of a subgradient run."""

    bound: list[float] = field(default_factory=list)
    best_bound: list[float] = field(default_factory=list)
    upper_bound: list[float] = field(default_factory=list)


@dataclass
class SubgradientResult:
    """Outcome of subgradient optimization of a Lagrangian dual."""

    best_bound: float
    best_multipliers: np.ndarray
    best_upper_bound: float
    iterations: int
    log: SubgradientLog


def subgradient_optimize(
    oracle: Oracle,
    n_multipliers: int,
    nonneg_mask: np.ndarray | None = None,
    heuristic: Heuristic | None = None,
    lam0: np.ndarray | None = None,
    initial_upper_bound: float = float("inf"),
    max_iters: int = 500,
    theta: float = 2.0,
    theta_min: float = 1e-4,
    shrink: float = 0.5,
    patience: int = 20,
    gap_tol: float = 1e-6,
    heuristic_every: int = 5,
) -> SubgradientResult:
    """Maximize the Lagrangian dual of a minimization problem.

    `oracle(lam)` must return `(L(lam), subgradient, subproblem solution)`
    with the subgradient of each dualized row written as g = rhs - lhs.
    Step size: Polyak rule t = theta * (UB - L(lam)) / ||g||^2 with the
    Held-Wolfe-Crowder schedule (halve theta after `patience` iterations
    without improvement of the best bound). `nonneg_mask[i] = True`
    projects lam[i] onto lam[i] >= 0 (row dualized from an inequality);
    the default projects every multiplier. Pass an all-False mask when
    the dualized rows are equalities.
    """
    if nonneg_mask is None:
        nonneg_mask = np.ones(n_multipliers, dtype=bool)
    lam = np.zeros(n_multipliers) if lam0 is None else lam0.astype(float).copy()
    best_bound, best_lam = -np.inf, lam.copy()
    ub = float(initial_upper_bound)
    log = SubgradientLog()
    stall, it = 0, 0
    for it in range(1, max_iters + 1):
        value, g, sub_solution = oracle(lam)
        if value > best_bound + 1e-12:
            best_bound, best_lam, stall = value, lam.copy(), 0
        else:
            stall += 1
        if heuristic is not None and (it == 1 or it % heuristic_every == 0):
            ub = min(ub, heuristic(lam, sub_solution))
        log.bound.append(value)
        log.best_bound.append(best_bound)
        log.upper_bound.append(ub)
        norm_sq = float(g @ g)
        if norm_sq <= 1e-14:
            break  # zero subgradient: lam is a dual maximizer
        if np.isfinite(ub) and ub - best_bound <= gap_tol * max(1.0, abs(ub)):
            break  # bound and incumbent meet: optimality proven
        if stall >= patience:
            theta *= shrink
            stall = 0
        if theta < theta_min:
            break
        target = ub if np.isfinite(ub) else best_bound + max(1.0, abs(best_bound))
        step = theta * max(target - value, 1e-12) / norm_sq
        lam = lam + step * g
        lam[nonneg_mask] = np.maximum(lam[nonneg_mask], 0.0)
    return SubgradientResult(best_bound, best_lam, ub, it, log)


def _toy_oracle(lam: np.ndarray) -> tuple[float, np.ndarray, dict[str, Any]]:
    """min x1 + 2*x2 s.t. x1 + x2 >= 1, x binary; the >= row is dualized."""
    lam1 = float(lam[0])
    x1 = 1 if 1.0 - lam1 < 0 else 0
    x2 = 1 if 2.0 - lam1 < 0 else 0
    value = lam1 + min(0.0, 1.0 - lam1) + min(0.0, 2.0 - lam1)
    g = np.array([1.0 - x1 - x2])
    return value, g, {"x": (x1, x2)}


result = subgradient_optimize(_toy_oracle, n_multipliers=1,
                              initial_upper_bound=1.0, max_iters=100)
print(round(result.best_bound, 4))
# Expected: 1.0 -- the dual closes the gap on this instance (z_LD = z_IP = 1);
# the multiplier settles near lam = 1 where the subproblem has multiple optima.
```

Design notes. The loop tracks the **best** bound, not the last one — subgradient iterates are not monotone. The heuristic receives both the multipliers and the raw subproblem solution because good repairs start from what the subproblem already decided. The fallback target when no UB exists keeps the method moving but converges slowly; supply a real upper bound as early as possible.

## Worked Example 1: Uncapacitated Facility Location

### Decomposition and bound

The UFLP with customers $i \in C$ ($n$ of them), facilities $j \in F$, opening costs $f_j > 0$, and assignment costs $c_{ij}$:

$$ z = \min \sum_{j} f_j y_j + \sum_{i}\sum_{j} c_{ij} x_{ij} \quad \text{s.t.} \quad \sum_j x_{ij} = 1 \;\; \forall i, \quad x_{ij} \le y_j \;\; \forall i,j, \quad x, y \in \{0,1\} $$

Dualize the assignment equalities with free multipliers $\lambda_i$:

$$ L(\lambda) = \sum_i \lambda_i + \min_{x_{ij} \le y_j} \sum_j \Big( f_j y_j + \sum_i (c_{ij} - \lambda_i) \, x_{ij} \Big) $$

The subproblem separates by facility. Define the facility contribution

$$ \rho_j = f_j + \sum_i \min(0, \, c_{ij} - \lambda_i) $$

Open facility $j$ exactly when $\rho_j < 0$, and serve customer $i$ from open facility $j$ exactly when $c_{ij} - \lambda_i < 0$. Then $L(\lambda) = \sum_i \lambda_i + \sum_j \min(0, \rho_j)$, computable in $O(|C| \cdot |F|)$. The subgradient component for customer $i$ is $g_i = 1 - \sum_j x_{ij}(\lambda)$.

Bound caveat, stated up front: this subproblem **has the integrality property** (its LP relaxation solves integrally facility by facility), so $z_{LD}$ equals the LP bound of the strong, disaggregated formulation (Cornuejols, Fisher & Nemhauser 1977 analyze this family of bounds). The relaxation still earns its keep: the oracle is a single pass over the cost matrix — far cheaper than solving the large strong LP — and the subproblem solutions seed an effective drop heuristic. Erlenkotter (1978) built one of the most effective UFLP exact codes on the closely related dual-ascent view.

```python
from __future__ import annotations

from typing import Any

import numpy as np


def uflp_oracle(lam: np.ndarray, fixed_cost: np.ndarray,
                assign_cost: np.ndarray) -> tuple[float, np.ndarray, dict[str, Any]]:
    """UFLP Lagrangian oracle after dualizing sum_j x_ij = 1 (free lam).

    `assign_cost` has shape (n_customers, n_facilities). One oracle call
    is a single vectorized pass: O(n_customers * n_facilities).
    """
    reduced = assign_cost - lam[:, None]                 # c_ij - lam_i
    rho = fixed_cost + np.minimum(reduced, 0.0).sum(axis=0)
    open_fac = rho < 0.0
    x = (reduced < 0.0) & open_fac[None, :]
    value = float(lam.sum() + rho[open_fac].sum())
    g = 1.0 - x.sum(axis=1).astype(float)                # 1 - sum_j x_ij
    return value, g, {"open": open_fac, "x": x, "rho": rho}


def uflp_heuristic(lam: np.ndarray, sub_solution: dict[str, Any],
                   fixed_cost: np.ndarray, assign_cost: np.ndarray) -> float:
    """Lagrangian heuristic: repair the subproblem into a feasible plan.

    Opens the facilities the subproblem suggests (at least one), assigns
    every customer to its cheapest open facility, then greedily drops
    facilities while the total cost improves. Always feasible.
    """
    open_fac = sub_solution["open"].copy()
    if not open_fac.any():
        open_fac[int(np.argmin(fixed_cost + assign_cost.sum(axis=0)))] = True

    def total_cost(mask: np.ndarray) -> float:
        return float(fixed_cost[mask].sum()
                     + assign_cost[:, mask].min(axis=1).sum())

    best = total_cost(open_fac)
    improved = True
    while improved:
        improved = False
        for j in np.flatnonzero(open_fac):
            if open_fac.sum() == 1:
                break
            open_fac[j] = False
            cost = total_cost(open_fac)
            if cost < best - 1e-9:
                best, improved = cost, True
            else:
                open_fac[j] = True
    return best
```

The driver below wires the oracle and heuristic into the framework, then verifies the three-way bound relation against Gurobi on a synthetic Euclidean instance.

```python
from __future__ import annotations

import gurobipy as gp
import numpy as np
from gurobipy import GRB

# Requires subgradient_optimize (framework section) plus uflp_oracle and
# uflp_heuristic (previous block) in the same module or session.


def build_uflp_model(fixed_cost: np.ndarray, assign_cost: np.ndarray) -> gp.Model:
    """Strong (disaggregated) UFLP formulation with named constraints."""
    n_cust, n_fac = assign_cost.shape
    model = gp.Model("uflp")
    model.Params.OutputFlag = 0
    y = model.addVars(n_fac, vtype=GRB.BINARY, name="y")
    x = model.addVars(n_cust, n_fac, vtype=GRB.BINARY, name="x")
    model.addConstrs((x.sum(i, "*") == 1 for i in range(n_cust)), name="assign")
    model.addConstrs((x[i, j] <= y[j]
                      for i in range(n_cust) for j in range(n_fac)), name="link")
    model.setObjective(
        gp.quicksum(float(fixed_cost[j]) * y[j] for j in range(n_fac))
        + gp.quicksum(float(assign_cost[i, j]) * x[i, j]
                      for i in range(n_cust) for j in range(n_fac)),
        GRB.MINIMIZE)
    return model


rng = np.random.default_rng(42)
n_cust, n_fac = 25, 8
customers = rng.uniform(0.0, 100.0, (n_cust, 2))
sites = rng.uniform(0.0, 100.0, (n_fac, 2))
assign_cost = np.linalg.norm(customers[:, None, :] - sites[None, :, :], axis=2)
fixed_cost = rng.uniform(100.0, 200.0, n_fac)

mip = build_uflp_model(fixed_cost, assign_cost)
mip.optimize()
assert mip.Status == GRB.OPTIMAL
z_opt = mip.ObjVal

lp = mip.relax()
lp.optimize()
z_lp = lp.ObjVal

res = subgradient_optimize(
    oracle=lambda lam: uflp_oracle(lam, fixed_cost, assign_cost),
    n_multipliers=n_cust,
    nonneg_mask=np.zeros(n_cust, dtype=bool),    # equality rows: free multipliers
    heuristic=lambda lam, s: uflp_heuristic(lam, s, fixed_cost, assign_cost),
    lam0=assign_cost.min(axis=1),                # warm start: cheapest assignment
    max_iters=300,
)
print(f"z_LP={z_lp:.2f}  z_LD={res.best_bound:.2f}  "
      f"UB={res.best_upper_bound:.2f}  z*={z_opt:.2f}")
# Expected: z_LP <= z_LD <= z* <= UB, with z_LD ~= z_LP (the subproblem has
# the integrality property) and the heuristic UB within about 1% of z*.
```

The warm start $\lambda_i = \min_j c_{ij}$ matters: at $\lambda = 0$ every reduced cost is positive, no facility opens, and the first subgradient is all ones — the method spends many iterations just inflating multipliers. Starting at the cheapest assignment cost puts the dual immediately in the interesting region. Duals of the strong LP relaxation are an even better warm start when that LP is affordable.

## Worked Example 2: Generalized Assignment with a Lagrangian Heuristic

### Choosing the dualization

The GAP assigns tasks $i \in T$ to machines $j \in M$ with costs $c_{ij}$, resource use $a_{ij}$, and capacities $b_j$:

$$ z = \min \sum_i \sum_j c_{ij} x_{ij} \quad \text{s.t.} \quad \sum_j x_{ij} = 1 \;\; \forall i, \quad \sum_i a_{ij} x_{ij} \le b_j \;\; \forall j, \quad x \in \{0,1\} $$

Both constraint families are candidates for dualization — this is the canonical example of the trade-off (Fisher 1981, "The Lagrangian relaxation method for solving integer programming problems"):

| Dualized family | Subproblem | Integrality property | Bound | Multipliers |
|---|---|---|---|---|
| Assignment $\sum_j x_{ij} = 1$ | One 0-1 knapsack per machine | No | $z_{LD} \ge z_{LP}$, usually strictly better | $|T|$, free |
| Capacities $\sum_i a_{ij} x_{ij} \le b_j$ | Per-task cheapest-machine choice | Yes | $z_{LD} = z_{LP}$ | $|M|$, nonnegative |

Dualizing the capacities gives a trivial oracle but only the LP bound. Dualizing the assignment rows costs one pseudo-polynomial knapsack DP per machine and is rewarded with a strictly stronger bound on most instances. We take the second route:

$$ L(\lambda) = \sum_i \lambda_i + \sum_{j} \min \Big\{ \sum_i (c_{ij} - \lambda_i) \, x_{ij} : \sum_i a_{ij} x_{ij} \le b_j, \; x_{\cdot j} \in \{0,1\}^{|T|} \Big\} $$

Each machine subproblem minimizes reduced costs, i.e. maximizes profits $\lambda_i - c_{ij}$ over a knapsack of capacity $b_j$ — only tasks with positive profit are candidates. The subgradient is again $g_i = 1 - \sum_j x_{ij}(\lambda)$: a task selected by no machine pushes its multiplier up, a task selected by several machines pushes it down.

```python
from __future__ import annotations

from typing import Any

import numpy as np


def knapsack_01_max(profit: np.ndarray, weight: np.ndarray,
                    capacity: int) -> tuple[float, np.ndarray]:
    """Exact 0-1 knapsack (maximize) by DP over capacities, O(n * capacity).

    Items with non-positive profit are never taken. Returns the optimal
    value and the boolean selection vector via keep-table backtracking.
    """
    n = profit.size
    dp = np.zeros(capacity + 1)
    keep = np.zeros((n, capacity + 1), dtype=bool)
    for i in range(n):
        w = int(weight[i])
        if profit[i] <= 0.0 or w > capacity:
            continue
        candidate = np.full(capacity + 1, -np.inf)
        candidate[w:] = dp[:capacity + 1 - w] + profit[i]
        take = candidate > dp
        keep[i] = take
        dp = np.where(take, candidate, dp)
    best_c = int(np.argmax(dp))
    best_value = float(dp[best_c])
    chosen = np.zeros(n, dtype=bool)
    c = best_c
    for i in range(n - 1, -1, -1):
        if keep[i, c]:
            chosen[i] = True
            c -= int(weight[i])
    return best_value, chosen


def gap_oracle(lam: np.ndarray, cost: np.ndarray, weight: np.ndarray,
               capacity: np.ndarray) -> tuple[float, np.ndarray, dict[str, Any]]:
    """GAP Lagrangian oracle after dualizing the assignment equalities.

    `cost` and `weight` have shape (n_tasks, n_machines); one knapsack
    per machine. Complexity O(n_machines * n_tasks * max(capacity)).
    """
    n_tasks, n_machines = cost.shape
    x = np.zeros((n_tasks, n_machines), dtype=bool)
    value = float(lam.sum())
    for j in range(n_machines):
        profit = lam - cost[:, j]                   # maximize lam_i - c_ij
        best, chosen = knapsack_01_max(profit, weight[:, j], int(capacity[j]))
        x[:, j] = chosen
        value -= best
    g = 1.0 - x.sum(axis=1).astype(float)
    return value, g, {"x": x}


value, chosen = knapsack_01_max(np.array([6.0, 10.0, 12.0]),
                                np.array([1, 2, 3]), capacity=5)
print(value, chosen)
# Expected: 22.0 [False  True  True] -- items 2 and 3 fill the knapsack.
```

### The Lagrangian heuristic

A subproblem solution violates exactly the dualized rows: some tasks are taken by several machines, others by none. The repair has two phases — resolve duplicates, then insert the leftovers with a regret rule (the machine you skip matters as much as the one you pick). Capacities stay feasible throughout because phase 1 only removes items and phase 2 checks residual capacity before every insertion.

```python
from __future__ import annotations

from typing import Any

import numpy as np


def gap_lagrangian_heuristic(lam: np.ndarray, sub_solution: dict[str, Any],
                             cost: np.ndarray, weight: np.ndarray,
                             capacity: np.ndarray) -> float:
    """Repair a GAP subproblem solution into a feasible assignment.

    Phase 1: a task chosen by several machines keeps only its cheapest
    copy. Phase 2: unassigned tasks are inserted largest-regret-first
    into the cheapest machine with enough residual capacity. Returns
    +inf when the greedy repair fails; the dual loop then simply keeps
    its previous incumbent and continues.
    """
    n_tasks, n_machines = cost.shape
    x = sub_solution["x"]
    assign = np.full(n_tasks, -1)
    load = np.zeros(n_machines)
    for i in range(n_tasks):
        machines = np.flatnonzero(x[i])
        if machines.size:
            j = int(machines[np.argmin(cost[i, machines])])
            assign[i] = j
            load[j] += weight[i, j]
    unassigned = [i for i in range(n_tasks) if assign[i] < 0]
    while unassigned:
        pick_task, pick_machine, pick_regret = -1, -1, -1.0
        for i in unassigned:
            feasible = np.flatnonzero(load + weight[i] <= capacity)
            if feasible.size == 0:
                return float("inf")
            order = feasible[np.argsort(cost[i, feasible])]
            regret = (float(cost[i, order[1]] - cost[i, order[0]])
                      if order.size > 1 else float("inf"))
            if regret > pick_regret:
                pick_task, pick_machine, pick_regret = i, int(order[0]), regret
        assign[pick_task] = pick_machine
        load[pick_machine] += weight[pick_task, pick_machine]
        unassigned.remove(pick_task)
    return float(cost[np.arange(n_tasks), assign].sum())
```

A stronger variant reassigns by reduced cost $c_{ij} - \lambda_i$ instead of raw cost, and falls back to ejection moves (move one assigned task elsewhere to make room) when insertion fails; add those only if the plain repair fails too often on your instances.

```python
from __future__ import annotations

import gurobipy as gp
import numpy as np
from gurobipy import GRB

# Requires subgradient_optimize (framework section) plus gap_oracle and
# gap_lagrangian_heuristic (previous blocks).


def build_gap_model(cost: np.ndarray, weight: np.ndarray,
                    capacity: np.ndarray) -> gp.Model:
    """GAP minimization MIP with named assignment and capacity constraints."""
    n_tasks, n_machines = cost.shape
    model = gp.Model("gap")
    model.Params.OutputFlag = 0
    x = model.addVars(n_tasks, n_machines, vtype=GRB.BINARY, name="x")
    model.addConstrs((x.sum(i, "*") == 1 for i in range(n_tasks)), name="assign")
    model.addConstrs(
        (gp.quicksum(int(weight[i, j]) * x[i, j] for i in range(n_tasks))
         <= float(capacity[j]) for j in range(n_machines)),
        name="capacity")
    model.setObjective(gp.quicksum(float(cost[i, j]) * x[i, j]
                                   for i in range(n_tasks)
                                   for j in range(n_machines)), GRB.MINIMIZE)
    return model


rng = np.random.default_rng(7)
n_tasks, n_machines = 20, 5
weight = rng.integers(5, 21, (n_tasks, n_machines))
cost = rng.uniform(10.0, 50.0, (n_tasks, n_machines))
capacity = np.full(n_machines, int(1.3 * weight.mean() * n_tasks / n_machines))

mip = build_gap_model(cost, weight, capacity)
mip.optimize()
assert mip.Status == GRB.OPTIMAL
z_opt = mip.ObjVal

lp = mip.relax()
lp.optimize()
z_lp = lp.ObjVal

res = subgradient_optimize(
    oracle=lambda lam: gap_oracle(lam, cost, weight, capacity),
    n_multipliers=n_tasks,
    nonneg_mask=np.zeros(n_tasks, dtype=bool),     # equality rows: free lam
    heuristic=lambda lam, s: gap_lagrangian_heuristic(lam, s, cost, weight,
                                                      capacity),
    lam0=cost.min(axis=1),
    max_iters=400,
    heuristic_every=3,
)
print(f"z_LP={z_lp:.2f}  z_LD={res.best_bound:.2f}  "
      f"UB={res.best_upper_bound:.2f}  z*={z_opt:.2f}")
# Expected: z_LP <= z_LD <= z* <= UB with z_LD strictly above z_LP on most
# seeds -- the knapsack subproblems lack the integrality property -- and the
# repaired UB within a few percent of z*.
```

Report all four numbers, always in this order, and verify the chain $z_{LP} \le z_{LD} \le z^* \le UB$ programmatically on every run: a violated inequality is the fastest possible signal of a sign error in the oracle or a bug in the repair.

## Advanced Techniques

### Deflected and averaged subgradients

Plain subgradient directions zigzag: consecutive subgradients often point in nearly opposite directions, and the iterates crawl along a ridge of $L$. Camerini, Fratta & Maffioli (1975) deflect the direction whenever the new subgradient forms an obtuse angle with the previous direction. A complementary idea keeps an ergodic (weighted) average of the multipliers and of the subproblem solutions; the averaged solutions converge toward a primal solution of the convexified problem, which the volume algorithm of Barahona & Anbil (2000) exploits to extract approximate primal values from a pure dual method.

```python
from __future__ import annotations

import numpy as np


def deflected_direction(g: np.ndarray, prev_dir: np.ndarray,
                        gamma: float = 1.5) -> np.ndarray:
    """Camerini-Fratta-Maffioli deflection to damp subgradient zigzag.

    Returns d = g + beta * prev_dir with beta chosen so consecutive
    directions never form an obtuse angle. Use d in place of g in the
    Polyak step (gamma in [1, 2]; 1.5 is the classic choice).
    """
    dot = float(g @ prev_dir)
    if dot >= 0.0 or not prev_dir.any():
        return g.copy()
    beta = -gamma * dot / float(prev_dir @ prev_dir)
    return g + beta * prev_dir


g_new = np.array([1.0, 0.0])
d_prev = np.array([-1.0, 1.0])
print(deflected_direction(g_new, d_prev))
# Expected: [0.25 0.75] -- the deflected direction keeps a share of the
# previous progress direction instead of reversing it.
```

### Variable fixing with Lagrangian penalties

At any multiplier vector, the oracle prices every structural decision. If forcing a decision raises the Lagrangian bound above the incumbent upper bound, that decision is provably absent from every improving solution — fix it and shrink the problem. For the UFLP oracle above, the penalty of forcing facility $j$ open is $\max(0, \rho_j)$ and of forcing it closed is $\max(0, -\rho_j)$. The same logic powers "core" reductions in set covering (Caprara, Fischetti & Toth 1999) and node pruning in Lagrangian branch-and-bound.

```python
from __future__ import annotations

import numpy as np


def uflp_fix_by_penalties(lagrangian_bound: float, upper_bound: float,
                          rho: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Lagrangian variable fixing for UFLP facility variables.

    rho[j] is facility j's contribution at the current multipliers (see
    the UFLP oracle). Forcing a closed facility open raises the bound by
    rho[j] >= 0; forcing an open facility closed raises it by -rho[j].
    Any forced bound above the incumbent proves the opposite fixing.
    """
    fix_closed = (rho >= 0.0) & (lagrangian_bound + rho > upper_bound + 1e-9)
    fix_open = (rho < 0.0) & (lagrangian_bound - rho > upper_bound + 1e-9)
    return fix_closed, fix_open


rho = np.array([40.0, -25.0, 3.0])
closed, opened = uflp_fix_by_penalties(100.0, 120.0, rho)
print(closed, opened)
# Expected: [ True False False] [False  True False] -- facility 0 is fixed
# closed (100 + 40 > 120) and facility 1 is fixed open (100 + 25 > 120).
```

Run the fixing test at the best multipliers each time the incumbent improves; fixings compound, and a smaller subproblem makes every later oracle call cheaper.

### Bundle and cutting-plane dual methods

The dual function admits an outer linearization: each oracle call yields the cut $L(\lambda) \le L(\lambda^k) + g^{k\top}(\lambda - \lambda^k)$, and maximizing the cut model is Kelley's cutting-plane method — which is exactly the LP master of Dantzig-Wolfe. Pure Kelley oscillates badly; bundle methods stabilize it with a proximal term $-\frac{u}{2}\lVert \lambda - \hat\lambda \rVert^2$ around a stability center that moves only on sufficient ascent (Lemarechal; see Frangioni 2005, "About Lagrangian methods in integer optimization," for the survey). Choose bundle methods over subgradient when oracle calls are expensive (each one deserves to be remembered), when you need a reliable termination certificate, or when multiplier accuracy matters because the multipliers feed pricing or fixing. Subgradient remains the right tool when the oracle is very cheap and thousands of rough iterations cost less than a handful of master QPs.

### Lagrangian decomposition (variable splitting)

When two constraint families are both hard and neither leaves a tractable subproblem alone, duplicate the variables: write $x = y$, give constraint family 1 to $x$ and family 2 to $y$, and dualize only the linking equalities $x = y$. The resulting bound is at least as strong as the better of the two single-family Lagrangian bounds, and often strictly stronger (Guignard & Kim 1987). The price is one multiplier per variable and two subproblems per oracle call. This is the standard escape when the dualization checklist scores every single family poorly.

### Relax-and-cut

When the complicating family is exponentially large (subtour elimination, cover inequalities), you cannot hold one multiplier per row. Relax-and-cut (Lucena 2005) dualizes constraints dynamically: separate violated inequalities at the current subproblem solution, attach multipliers only to those, and let multipliers of slack rows decay to zero. The subgradient loop is unchanged; the multiplier vector just grows and shrinks. This combines naturally with the fixing tests above and gives Lagrangian analogues of branch-and-cut bounds at a fraction of the LP cost.

## Practical Challenges

**The bound zigzags and stalls far from the dual optimum.** This is normal subgradient behavior, not a bug. Verify the Held-Wolfe-Crowder schedule is active (theta actually halves), add CFM deflection, and warm-start the multipliers from LP duals or a domain guess such as cheapest-assignment costs. If the bound still crawls after a few hundred iterations, switch to a bundle method rather than tuning forever.

**The Polyak step needs an upper bound you do not have yet.** Run the Lagrangian heuristic from iteration 1, not after convergence. Until it succeeds, use the fallback target (best bound plus a margin) but shrink theta faster, because steps toward a fake target overshoot. Never use the unknown optimum as the target: if the target drops below $z_{LD}$, the step sizes collapse to zero before reaching the optimum.

**The heuristic never produces a feasible solution.** The dualized rows are exactly what the subproblem ignores, so repair difficulty equals the hardness of restoring those rows. Invest in regret-based insertion and one round of ejection moves before anything else. If repair stays hopeless, the dualization is wrong for primal recovery — consider dualizing the other family even at the price of a weaker bound, or finish solutions with a small MIP over the undecided variables.

**You dualized constraints and the subproblem is still hard.** A pseudo-polynomial DP is acceptable when capacities are small integers; otherwise re-derive. Check for a hidden block structure (per machine, per period) you failed to exploit, and consider Lagrangian decomposition before abandoning the approach.

**The Lagrangian bound exactly equals the LP bound and the effort feels wasted.** Diagnose, do not guess: check the integrality property of your subproblem. If it holds, equality is a theorem (Geoffrion 1974), and the remaining value is oracle speed plus the heuristic. If you need a strictly stronger bound, change the dualization so the kept constraints define a non-integral polytope.

**Multipliers of equality rows drift to huge magnitudes.** Free multipliers have no projection to restrain them. Scale costs to a common order of magnitude, warm-start sensibly, and cap the step length in the first iterations. Persistent drift usually means a sign error: confirm the subgradient is rhs minus lhs and that you are maximizing $L$, not minimizing it.

**The duality gap refuses to close.** For most integer programs $z_{LD} < z_{IP}$ is structural — no step-size rule fixes a nonconvexity gap. Report the gap honestly, then close it by branching: embed the Lagrangian bound in branch-and-bound, reusing parent multipliers as child warm starts. Interpret the remaining gap with the same discipline as a MIP gap (see integer-programming-techniques).

**Bound comparisons across formulations are inconsistent.** $z_{LP}$ depends on the formulation: the weak UFLP formulation (aggregated linking constraints) has a much weaker LP bound than the strong one. Always state which formulation's LP you compare against, and recompute it yourself rather than quoting a paper that may have used the other.

## Tools & Libraries

| Library | When to use | Note |
|---|---|---|
| gurobipy | Verification MIPs/LPs, MIP-based subproblems, LP duals as warm starts | `model.relax()` gives the LP bound of the same formulation for fair comparison |
| numpy | Oracles, subgradient loop, heuristics | Vectorize the oracle first; it runs hundreds of times |
| scipy.optimize | `linear_sum_assignment` for assignment-shaped subproblems | Exact Hungarian in C, instant oracle |
| networkx | Shortest-path or spanning-tree subproblems (e.g. Held-Karp 1-trees) | Fine to prototype; rewrite hot loops in numpy if the oracle dominates runtime |
| HiGHS / PuLP | License-free verification when Gurobi is unavailable | Same role as gurobipy here; interface differs |
| pandas | Iteration logs and bound-comparison tables across instances | One row per iteration or per run; see the Output Format section |
| matplotlib | Convergence plots: L(lam), best bound, UB per iteration | The standard figure for any Lagrangian study |

## Output Format

A complete Lagrangian relaxation deliverable contains:

1. **Dualization statement.** Which constraint family is dualized, multiplier signs (free vs nonnegative), and the resulting subproblem with its solution algorithm and per-call complexity. State whether the subproblem has the integrality property and therefore where $z_{LD}$ sits relative to $z_{LP}$.
2. **Dual loop configuration.** Step-size rule and schedule (theta start, patience, shrink factor), multiplier warm start, heuristic frequency, stopping criteria, iteration limit.
3. **Convergence log.** A table (and plot) over iterations:

| iter | L(lam) | best LB | best UB | gap % | theta |
|---|---|---|---|---|---|
| 1 | 1042.7 | 1042.7 | 1311.0 | 20.5 | 2.000 |
| 50 | 1180.3 | 1184.9 | 1216.4 | 2.6 | 1.000 |
| 200 | 1196.1 | 1198.2 | 1204.5 | 0.5 | 0.250 |

4. **Bound comparison table.** For each instance: $z_{LP}$ (state the formulation), $z_{LD}$, best heuristic UB, exact optimum where available, gaps in percent, oracle calls, wall time. Verify $z_{LP} \le z_{LD} \le z^* \le UB$ on every row.
5. **Primal solution artifact.** The best feasible solution found, validated by an independent feasibility checker, with its objective recomputed from raw data — never trusted from inside the loop.
6. **Recommendation.** If a gap remains: whether to branch on it, stabilize the dual, strengthen the heuristic, or accept the certificate as is — with the expected cost of each option.

## Questions to Ask

- Which constraints make the problem hard — what easy structure remains if we remove them?
- Are the dualized constraints equalities or inequalities, and in which direction?
- How large is the instance: variables, dualized rows, and the expected oracle cost per call?
- Do you need the bound alone, or also good feasible solutions from the same run?
- Is a Gurobi license available for verification, or should comparisons use HiGHS?
- What time budget per instance, and what gap tolerance counts as success?
- Are capacities and weights integral (enables DP subproblems), and how large are they?
- Do you already have a feasible solution or construction heuristic to supply the first upper bound?
- Will the bound run inside branch-and-bound (multiplier warm starts across nodes matter) or once per instance?

## Related Skills

- **linear-programming-fundamentals** — when you need duality, dual values, and the LP-relaxation bound that every Lagrangian bound must be compared against.
- **facility-location-problem** — when the application is UFLP/CFLP/p-median and you need the full formulation menu and alternative solution paths.
- **integer-programming-techniques** — when you need to interpret bounds and gaps inside branch-and-bound or tighten the formulation instead of decomposing it.
- **warm-starts-and-initial-solutions** — when you need construction heuristics for the upper bounds that the Polyak step and the fixing tests depend on.
- **dantzig-wolfe-decomposition** — when you want the same convexified bound computed through a master/column-generation reformulation with clean termination.
