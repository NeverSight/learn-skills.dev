---
name: benders-decomposition
description: When the user wants to solve a structured MILP or two-stage stochastic program by Benders decomposition — splitting it into an integer master and LP subproblems, deriving optimality and feasibility cuts from subproblem duals, and implementing either the classic iterative loop or branch-and-Benders-cut with lazy-constraint callbacks in Gurobi. Also use when the user mentions "Benders decomposition," "Benders cuts," "L-shaped method," "feasibility cut," "optimality cut," "master problem," or when fixing a few complicating variables leaves an easy or separable subproblem. For scenario generation and SAA, see stochastic-optimization; for callback mechanics and parameters, see gurobi-advanced-features.
---

# Benders Decomposition

You are an expert in exact decomposition methods for mixed-integer optimization, specifically Benders decomposition in its classic (iterative master/subproblem loop) and modern (branch-and-Benders-cut via lazy-constraint callbacks) forms, including the L-shaped method for two-stage stochastic programs. This skill covers the master–subproblem split, the derivation of optimality and feasibility cuts from LP duality, complete gurobipy implementations of both execution modes, and the acceleration techniques (Pareto-optimal cuts, stabilization, cut aggregation) that decide whether Benders converges in 20 iterations or 2,000. Use the framework below to verify the problem has the right structure, derive the cuts on paper, implement against the reusable loop or the callback pattern, and validate against the monolithic model.

## Initial Assessment

Before decomposing anything, establish the following. Each answer changes the design.

- **Identify the complicating variables.** Which variables, once fixed, leave an easy remaining problem? Benders needs a clean split: integer/design variables `y` in the master, continuous recourse variables `x` in the subproblem. If no such split exists, Benders is the wrong tool.
- **Subproblem class.** Is the subproblem an LP for every fixed `y`? Classic Benders cuts come from LP duals. If the subproblem keeps integer variables, you need logic-based Benders or integer L-shaped cuts (see Advanced Techniques) — a different, weaker machinery.
- **Subproblem separability.** Does the subproblem split into independent blocks (per scenario, per customer, per period)? Separability is the main source of speedup and enables multi-cut formulations and parallel subproblem solves.
- **Feasibility structure.** Can the subproblem be infeasible for some master solutions? If yes, you need feasibility cuts (dual extreme rays / Farkas certificates). Check first whether a small master-side constraint (e.g., total capacity ≥ total demand) or penalized slack variables can give *relatively complete recourse* and remove feasibility cuts entirely.
- **Why decompose at all?** Estimate the extensive (monolithic) model size: variables = |y| + |x|·(blocks), constraints likewise. Modern solvers handle millions of nonzeros; decompose only when the monolith is too large, too slow, or the subproblem has special structure (closed-form duals, network structure) the solver cannot exploit.
- **Execution mode.** Classic loop (sequence of master MIPs) for prototyping, analysis, and cheap masters; branch-and-Benders-cut (one search tree, lazy cuts) for production runs where re-solving the master MIP from scratch each iteration is wasteful.
- **Bound on the recourse term.** What is a valid lower bound for `eta` (minimization)? Without one the first master solve is unbounded. Nonnegative recourse costs give `eta ≥ 0`; per-block bounds (e.g., cheapest assignment per customer) are tighter and free.
- **Solver and license.** gurobipy available? Callbacks, `FarkasDual`/`UnbdRay`, and lazy constraints are needed. With open-source solvers, SCIP supports Benders plugins; HiGHS supports only the classic loop.
- **Scale and budget.** Number of scenarios/blocks, master integer variables, target gap, wall-clock budget. These set single-cut vs multi-cut, stabilization needs, and whether subproblems must be parallelized.
- **Validation baseline.** Build the monolithic model on small instances first. Every Benders implementation must reproduce its optimum exactly before you trust it at scale.

## Decomposition Anatomy

Benders decomposition (Benders 1962, "Partitioning procedures for solving mixed-variables programming problems") targets problems of the form

$$
\min_{y,\,x} \; f^\top y + q^\top x
\quad \text{s.t.} \quad
W x \ge h - T y, \qquad x \ge 0, \qquad y \in Y,
$$

where `y` are the *complicating* variables (typically integer: open/close, build/buy, capacity levels) and, for fixed `y`, the remaining problem in `x` is an LP. Project `x` out:

$$
\min_{y \in Y} \; f^\top y + z(y),
\qquad
z(y) = \min \{\, q^\top x \;:\; W x \ge h - T y,\; x \ge 0 \,\}.
$$

Dualize the inner LP. Its dual feasible region

$$
U = \{\, u \ge 0 \;:\; W^\top u \le q \,\}
$$

does **not** depend on `y` — only the dual objective does:

$$
z(y) = \max \{\, u^\top (h - T y) \;:\; u \in U \,\}.
$$

This is the single fact the whole method rests on. `U` is a fixed polyhedron with finitely many extreme points $u_1, \dots, u_P$ and extreme rays $r_1, \dots, r_R$, so for every `y`:

- if the subproblem is feasible, $z(y) = \max_{p} \; u_p^\top (h - T y)$ (the max is attained at an extreme point);
- the subproblem is feasible **iff** $r_k^\top (h - T y) \le 0$ for every extreme ray $r_k$ — otherwise the dual is unbounded along some ray, which is exactly a Farkas certificate of primal infeasibility.

Substituting gives a master problem equivalent to the original:

$$
\min_{y \in Y,\ \eta} \; f^\top y + \eta
\quad \text{s.t.} \quad
\underbrace{\eta \ge u_p^\top (h - T y)}_{\text{optimality cuts, } p = 1..P}, \qquad
\underbrace{r_k^\top (h - T y) \le 0}_{\text{feasibility cuts, } k = 1..R}.
$$

Nobody enumerates `P` and `R`. The algorithm keeps a *relaxed* master with a small subset of cuts and alternates:

1. Solve the relaxed master → candidate $(\hat{y}, \hat{\eta})$ and a **lower bound** $f^\top \hat{y} + \hat{\eta}$ (minimization).
2. Solve the dual subproblem at $\hat{y}$. Unbounded → add the feasibility cut from the ray. Optimal with value $z(\hat{y})$ → an **upper bound** $f^\top \hat{y} + z(\hat{y})$, and if $z(\hat{y}) > \hat{\eta} + \varepsilon$, add the optimality cut from the optimal extreme point.
3. Stop when $z(\hat{y}) \le \hat{\eta} + \varepsilon$: then UB ≤ LB, so $\hat{y}$ is optimal.

The lower bound is monotone nondecreasing (the master only gains constraints); the upper bound is **not** monotone — always track the incumbent best. Convergence is finite because each iteration produces an extreme point or ray not yet in the master, and there are finitely many.

### Two execution modes

| Mode | How it runs | Use when |
|---|---|---|
| Classic iterative loop | Solve master MIP to optimality, add cuts, repeat | Prototyping; cheap or LP master; root-node cut warm-up; teaching the cut logic |
| Branch-and-Benders-cut | One B&B tree on the master; separate cuts at each integer candidate via lazy-constraint callback | Production default; master MIP is expensive; avoids re-proving the same branching work every iteration |

The classic loop wastes effort: iteration k re-solves a master MIP that differs from iteration k−1 by one row. Branch-and-Benders-cut (also called one-tree Benders; see Fortz & Poss 2009 and the survey by Rahmaniani, Crainic, Gendreau & Rei 2017, "The Benders decomposition algorithm: A literature review") keeps a single tree and rejects integer candidates with lazy cuts. Worked Example 1 implements it.

### When Benders pays off — and when it does not

Use Benders when at least one of these holds:

- **The subproblem separates** into many independent LPs (scenarios in stochastic programs, customers in facility location, commodities in network design). The extensive form is huge; the pieces are tiny.
- **The subproblem has special structure**: closed-form dual solutions (UFL — Worked Example 1), network flow (solvable by a combinatorial algorithm), or a structure destroyed by mixing with `y`.
- **Memory**: the monolithic model does not fit, but master + one block at a time does.

Avoid Benders when the subproblem keeps integer variables (classic duals do not exist), when `T` is dense so every cut is dense and the master degrades, or when the monolith solves in minutes anyway — a modern MIP solver with a strong formulation beats a naive decomposition embarrassingly often. Build the monolith first; it is both the baseline and the burden of proof.

### The L-shaped method

A two-stage stochastic program with finite scenarios $s = 1..S$, probabilities $p_s$,

$$
\min_{y \in Y} \; f^\top y + \sum_{s} p_s\, Q_s(y),
\qquad
Q_s(y) = \min \{\, q_s^\top x \;:\; W x \ge h_s - T_s y,\; x \ge 0 \,\},
$$

is exactly the Benders structure with a block-diagonal subproblem — one block per scenario. Benders applied to it is the **L-shaped method** (Van Slyke & Wets 1969). Two cut layouts:

- **Single-cut**: one variable `theta` approximates the whole expectation; each iteration adds one cut aggregating the probability-weighted duals of all scenarios.
- **Multi-cut**: one `theta_s` per scenario, one cut per violated scenario (Birge & Louveaux 1988). More master rows, far fewer iterations; the right default when `S` is moderate (≤ a few thousand).

Feasibility cuts disappear under *relatively complete recourse* — the subproblem is feasible for every master-feasible `y`. Design for it: add penalized shortfall variables to the second stage (Worked Example 2) instead of letting scenarios go infeasible.

## Generic Benders Framework

The reusable artifact: a classic Benders loop for `min f@y + q@x s.t. Wx >= h - Ty, x >= 0, y binary`, with the dual subproblem built **once** (its feasible region never changes — only the objective moves with `y`), feasibility cuts from extreme rays, and the standard termination test. The worked examples follow the same anatomy; every block is self-contained and runs as-is.

```text
BENDERS DECOMPOSITION (classic loop, minimization)
--------------------------------------------------
input: f, q, W, T, h; optional master-only constraints D y >= d
state: relaxed master over (y, eta); dual subproblem over u (built once)

1. master: min f@y + eta, s.t. D y >= d, eta >= eta_lb
2. repeat:
3.     solve master -> (y_hat, eta_hat); LB <- master objective
4.     solve dual subproblem: max u@(h - T y_hat) s.t. W'u <= q, u >= 0
5.     if unbounded along ray r:
6.         add feasibility cut  (r@T) y >= r@h          # cuts y_hat off
7.     else, with optimal point u*, value z_hat:
8.         UB <- min(UB, f@y_hat + z_hat)
9.         if z_hat <= eta_hat + eps: STOP (y_hat optimal)
10.        add optimality cut  eta + (u*@T) y >= u*@h
11. return incumbent; LB is monotone, UB is not -> track the best
```

```python
"""Reusable classic Benders loop: binary master, LP subproblem via its dual."""
from __future__ import annotations

import math
from dataclasses import dataclass

import gurobipy as gp
import numpy as np
from gurobipy import GRB


@dataclass
class BendersData:
    """min f@y + q@x  s.t.  W x >= h - T y, x >= 0, y binary, D y >= d (master-only)."""

    f: np.ndarray            # (n_y,) master costs
    q: np.ndarray            # (n_x,) subproblem costs
    W: np.ndarray            # (m, n_x) subproblem matrix
    T: np.ndarray            # (m, n_y) linking matrix
    h: np.ndarray            # (m,) linking rhs
    D: np.ndarray | None = None   # optional master-only constraints D y >= d
    d: np.ndarray | None = None


class DualSubproblem:
    """Dual subproblem max u@(h - T y) s.t. W'u <= q, u >= 0 — built once.

    The feasible region is independent of y; only the objective changes.
    """

    def __init__(self, data: BendersData) -> None:
        self.data = data
        self.model = gp.Model("benders-dual-subproblem")
        self.model.Params.OutputFlag = 0
        self.model.Params.InfUnbdInfo = 1     # expose UnbdRay when unbounded
        self.model.Params.DualReductions = 0  # report UNBOUNDED, never INF_OR_UNBD
        self.model.Params.Method = 0          # primal simplex: returns extreme rays
        self.u = self.model.addMVar(data.W.shape[0], lb=0.0, name="u")
        self.model.addConstr(data.W.T @ self.u <= data.q, name="dual_feasibility")

    def solve(self, y_val: np.ndarray) -> tuple[str, float, np.ndarray]:
        """Return ('point', z(y), u*) or ('ray', inf, r) at the given master solution."""
        rhs = self.data.h - self.data.T @ y_val
        self.model.setObjective(rhs @ self.u, GRB.MAXIMIZE)
        self.model.optimize()
        if self.model.Status == GRB.OPTIMAL:
            return "point", self.model.ObjVal, self.u.X
        if self.model.Status == GRB.UNBOUNDED:
            ray = np.array(self.model.getAttr(GRB.Attr.UnbdRay, self.model.getVars()))
            return "ray", math.inf, ray
        raise RuntimeError(f"dual subproblem status {self.model.Status}: "
                           "dual infeasible means the primal recourse is unbounded")


def benders_solve(data: BendersData, eta_lb: float = 0.0, tol: float = 1e-6,
                  max_iters: int = 500) -> dict:
    """Classic Benders loop. eta_lb must be a valid lower bound on z(y)."""
    master = gp.Model("benders-master")
    master.Params.OutputFlag = 0
    y = master.addMVar(data.f.size, vtype=GRB.BINARY, name="y")
    eta = master.addVar(lb=eta_lb, name="eta")
    master.setObjective(data.f @ y + eta, GRB.MINIMIZE)
    if data.D is not None:
        master.addConstr(data.D @ y >= data.d, name="master_side")
    sub = DualSubproblem(data)

    best_ub, best_y, log = math.inf, None, []
    for it in range(1, max_iters + 1):
        master.optimize()
        if master.Status != GRB.OPTIMAL:
            raise RuntimeError(f"master status {master.Status}: feasibility cuts "
                               "may have emptied Y — check the original model")
        lb = master.ObjVal
        y_val = np.rint(y.X)              # clean integrality noise before cutting
        kind, z_hat, vec = sub.solve(y_val)
        if kind == "ray":                 # feasibility cut: (r@T) y >= r@h
            master.addConstr((vec @ data.T) @ y >= float(vec @ data.h),
                             name=f"feas_cut_{it}")
            log.append((it, lb, best_ub, "feasibility"))
            continue
        ub = float(data.f @ y_val) + z_hat
        if ub < best_ub:
            best_ub, best_y = ub, y_val.astype(int)
        log.append((it, lb, best_ub, "optimality"))
        if z_hat <= eta.X + tol * max(1.0, abs(z_hat)):
            break                         # eta matches the true recourse: optimal
        master.addConstr(eta + (vec @ data.T) @ y >= float(vec @ data.h),
                         name=f"opt_cut_{it}")
    return {"y": best_y, "objective": best_ub, "lower_bound": lb, "log": log}


# --- tiny instance: open plants (capacity 8 each) to serve demand 10 --------
f = np.array([10.0, 14.0])                          # plant opening costs
q = np.array([1.0, 2.0])                            # unit production costs
W = np.array([[1.0, 1.0], [-1.0, 0.0], [0.0, -1.0]])  # demand row, capacity rows
h = np.array([10.0, 0.0, 0.0])
T = np.array([[0.0, 0.0], [8.0, 0.0], [0.0, 8.0]])  # -x_i >= -8 y_i
res = benders_solve(BendersData(f, q, W, T, h))
print(res["y"], round(res["objective"], 4), [step[3] for step in res["log"]])
# Expected: [1 1] 36.0 ['feasibility', 'optimality', 'optimality'] -- the first
# master tries y=(0,0); the ray cut 8*y0 + 8*y1 >= 10 forces both plants open
# (one plant covers only 8 < 10); convergence at iteration 3 with cost 36.
```

Two details repay attention. First, the dual subproblem is constructed once and re-optimized with a new objective each call — simplex warm starts make repeat solves nearly free, and the construction makes the theory visible: extreme points and rays come from one fixed polyhedron. Second, `eta` needs a valid lower bound (`0` here, because `q ≥ 0`); without it the first master solve is unbounded and Gurobi raises an error before the loop ever produces a cut.

When the subproblem is solved in its **primal** form instead (often more natural — Worked Example 2), the same information comes from Gurobi attributes: `Constr.Pi` gives the optimal dual point, and `Constr.FarkasDual` (with `InfUnbdInfo=1`, on an infeasible primal) gives the ray. The cut algebra is identical.

## Worked Example 1: Uncapacitated Facility Location via Benders Callbacks

The uncapacitated facility location problem (UFLP): open facilities $i \in F$ at fixed cost $f_i$, serve every customer $j \in C$ from an open facility at cost $c_{ij}$:

$$
\min \; \sum_i f_i y_i + \sum_j \sum_i c_{ij} x_{ij}
\quad \text{s.t.} \quad
\sum_i x_{ij} = 1 \;\; \forall j, \qquad
x_{ij} \le y_i, \qquad x \ge 0, \; y \in \{0,1\}^{|F|}.
$$

For fixed $\hat{y} \ne 0$ the `x`-LP separates **by customer**, and each block has a closed-form optimum: assign customer `j` to the cheapest open facility, $z_j(\hat{y}) = \min \{ c_{ij} : \hat{y}_i = 1 \}$. The dual of customer `j`'s block (dual variable $v_j$ for the assignment row, $w_{ij} \ge 0$ for each linking row) is

$$
\max \; v_j - \sum_i w_{ij} \hat{y}_i
\quad \text{s.t.} \quad
v_j - w_{ij} \le c_{ij} \;\; \forall i, \qquad w_{ij} \ge 0,
$$

with the closed-form optimal extreme point $v_j = z_j(\hat{y})$, $w_{ij} = \max(0,\, v_j - c_{ij})$. The disaggregated (per-customer) optimality cut is therefore

$$
\eta_j \;\ge\; z_j(\hat{y}) - \sum_i \bigl(z_j(\hat{y}) - c_{ij}\bigr)^+ \, y_i ,
$$

valid for every `y` by weak duality and tight at $\hat{y}$. Read it as: the bound starts at the current best cost and drops by $(z_j - c_{ij})^+$ for each cheaper facility `i` that opens. No LP is ever solved — the entire separation is a sort-free `min` and a `maximum` over a cost column. This closed-form, disaggregated scheme is what makes Benders the method of choice for very large UFLP (Fischetti, Ljubić & Sinnl 2017, "Redesigning Benders decomposition for large-scale facility location"). Feasibility cuts are avoided by construction: the master keeps `sum(y) >= 1`, so the subproblem is always feasible — an instance of the general rule *move structural feasibility into the master when you can*.

```python
"""UFLP Benders separation in closed form: dual values and one cut per customer."""
from __future__ import annotations

import numpy as np


def ufl_cut(c_j: np.ndarray, y: np.ndarray) -> tuple[float, np.ndarray]:
    """Closed-form dual for one customer at binary y (>= 1 facility open).

    Returns (v, w) defining the optimality cut  eta_j >= v - w @ y,
    with v = cost of the cheapest open facility and w_i = max(0, v - c_ij).
    """
    v = float(c_j[y > 0.5].min())
    w = np.maximum(0.0, v - c_j)
    return v, w


# --- tiny instance: 3 facilities x 4 customers, facilities 0 and 2 open -----
c = np.array([[2.0, 7.0, 5.0, 4.0],
              [5.0, 3.0, 6.0, 8.0],
              [6.0, 4.0, 2.0, 3.0]])   # c[i, j]
y_hat = np.array([1, 0, 1])
for j in range(c.shape[1]):
    v, w = ufl_cut(c[:, j], y_hat)
    print(j, v, w)
# Expected: v = 2, 4, 2, 3 for customers 0..3; all w vectors are zero except
# customer 1, where w = [0, 1, 0]: its cut reads eta_1 >= 4 - 1*y_1, i.e. the
# bound drops to 3 if the (currently closed, cheaper) facility 1 opens.
```

The production implementation is branch-and-Benders-cut: one master tree over `(y, eta)`, with the cuts above added lazily whenever Gurobi finds an integer candidate (`MIPSOL`). `Params.LazyConstraints = 1` is mandatory — it tells the solver that not all constraints are present, disabling reductions that would otherwise cut off solutions only the callback knows are infeasible.

```python
"""UFLP by branch-and-Benders-cut: lazy per-customer optimality cuts in Gurobi."""
from __future__ import annotations

import gurobipy as gp
import numpy as np
from gurobipy import GRB


def generate_ufl(n_fac: int, n_cust: int, seed: int) -> tuple[np.ndarray, np.ndarray]:
    """Euclidean UFLP instance in the unit square; returns (fixed costs, c[i, j])."""
    rng = np.random.default_rng(seed)
    fac, cust = rng.random((n_fac, 2)), rng.random((n_cust, 2))
    c = 10.0 * np.linalg.norm(fac[:, None, :] - cust[None, :, :], axis=2)
    return rng.uniform(5.0, 15.0, size=n_fac), c


def solve_ufl_benders(f: np.ndarray, c: np.ndarray,
                      tol: float = 1e-6) -> tuple[float, np.ndarray, int]:
    """Master over (y, eta_j); closed-form cuts separated in a MIPSOL callback."""
    n_fac, n_cust = c.shape
    model = gp.Model("ufl-benders")
    model.Params.OutputFlag = 0
    model.Params.LazyConstraints = 1            # mandatory for cbLazy
    y = model.addVars(n_fac, vtype=GRB.BINARY, name="y")
    eta = model.addVars(n_cust, lb=c.min(axis=0).tolist(), name="eta")
    model.setObjective(gp.quicksum(f[i] * y[i] for i in range(n_fac))
                       + gp.quicksum(eta.values()), GRB.MINIMIZE)
    model.addConstr(gp.quicksum(y.values()) >= 1, name="open_at_least_one")
    n_cuts = 0

    def separate(model: gp.Model, where: int) -> None:
        """Lazily add every violated per-customer cut at an integer candidate."""
        nonlocal n_cuts
        if where != GRB.Callback.MIPSOL:
            return
        y_val = np.array(model.cbGetSolution([y[i] for i in range(n_fac)]))
        eta_val = model.cbGetSolution([eta[j] for j in range(n_cust)])
        open_mask = y_val > 0.5                 # candidate values are not exact
        for j in range(n_cust):
            v = float(c[open_mask, j].min())
            if eta_val[j] >= v - tol:
                continue                        # this customer's eta is correct
            w = np.maximum(0.0, v - c[:, j])
            model.cbLazy(eta[j] >= v - gp.quicksum(
                float(w[i]) * y[i] for i in range(n_fac) if w[i] > 0.0))
            n_cuts += 1

    model.optimize(separate)
    assert model.Status == GRB.OPTIMAL and model.SolCount > 0
    y_opt = np.array([y[i].X for i in range(n_fac)]).round().astype(int)
    return model.ObjVal, y_opt, n_cuts


f, c = generate_ufl(n_fac=15, n_cust=40, seed=7)
obj, y_opt, n_cuts = solve_ufl_benders(f, c)
print(round(obj, 4), int(y_opt.sum()), n_cuts > 0)
# Expected: 109.0666 4 True -- four facilities open; the objective matches the
# monolithic MIP below to full precision because both are exact.
```

Validation is non-negotiable: a buggy separation routine does not crash — it silently returns a wrong "optimum", because with `LazyConstraints=1` the solver trusts the callback to reject every bad integer point. Reproduce the monolithic optimum on the same seeded instance before scaling up.

```python
"""Monolithic UFLP MIP: the correctness baseline for the Benders solver."""
from __future__ import annotations

import gurobipy as gp
import numpy as np
from gurobipy import GRB


def generate_ufl(n_fac: int, n_cust: int, seed: int) -> tuple[np.ndarray, np.ndarray]:
    """Identical generator and seed => identical instance to the Benders block."""
    rng = np.random.default_rng(seed)
    fac, cust = rng.random((n_fac, 2)), rng.random((n_cust, 2))
    c = 10.0 * np.linalg.norm(fac[:, None, :] - cust[None, :, :], axis=2)
    return rng.uniform(5.0, 15.0, size=n_fac), c


def solve_ufl_direct(f: np.ndarray, c: np.ndarray) -> float:
    """Strong (disaggregated) formulation with x[i, j] <= y[i]."""
    n_fac, n_cust = c.shape
    model = gp.Model("ufl-direct")
    model.Params.OutputFlag = 0
    y = model.addVars(n_fac, vtype=GRB.BINARY, name="y")
    x = model.addVars(n_fac, n_cust, lb=0.0, ub=1.0, name="x")
    model.setObjective(
        gp.quicksum(f[i] * y[i] for i in range(n_fac))
        + gp.quicksum(c[i, j] * x[i, j] for i in range(n_fac) for j in range(n_cust)),
        GRB.MINIMIZE)
    model.addConstrs((gp.quicksum(x[i, j] for i in range(n_fac)) == 1
                      for j in range(n_cust)), name="assign")
    model.addConstrs((x[i, j] <= y[i]
                      for i in range(n_fac) for j in range(n_cust)), name="link")
    model.optimize()
    assert model.Status == GRB.OPTIMAL
    return model.ObjVal


f, c = generate_ufl(n_fac=15, n_cust=40, seed=7)
print(round(solve_ufl_direct(f, c), 4))
# Expected: 109.0666 -- identical to the Benders objective on the same seed.
```

## Worked Example 2: Two-Stage Stochastic Capacity Planning (L-shaped Method)

Capacity planning under demand uncertainty: choose integer capacity units $y_i \in \{0, \dots, u^{\max}\}$ at plant `i` (unit cost $f_i$, unit size $\kappa$) **before** demand is known; after scenario `s` reveals demands $d_{js}$, ship $x_{ij} \ge 0$ at cost $c_{ij}$ and absorb any shortfall $g_j \ge 0$ at penalty $\rho$:

$$
\min_y \; \sum_i f_i y_i + \sum_s p_s\, Q_s(y),
\qquad
Q_s(y) = \min_{x, g \ge 0} \; \sum_{ij} c_{ij} x_{ij} + \rho \sum_j g_j
$$

$$
\text{s.t.} \quad
\sum_j x_{ij} \le \kappa\, y_i \;\; \forall i \;\;(\mu_{is} \le 0),
\qquad
\sum_i x_{ij} + g_j \ge d_{js} \;\; \forall j \;\;(\pi_{js} \ge 0).
$$

The shortfall variables give relatively complete recourse — every scenario LP is feasible for every `y`, so the L-shaped method needs **no feasibility cuts**. From LP duality, any optimal dual pair $(\pi_s, \mu_s)$ at $\hat{y}$ satisfies $Q_s(\hat{y}) = \pi_s^\top d_s + \sum_i \mu_{is}\, \kappa\, \hat{y}_i$ and stays dual-feasible for every other `y`, giving the multi-cut optimality cut

$$
\theta_s \;\ge\; \pi_s^\top d_s + \sum_i \mu_{is}\, \kappa\, y_i .
$$

First the deterministic-equivalent (extensive form) model — the validation baseline and the thing the L-shaped method avoids building at scale: with `S` scenarios it has $S(|F||C| + |C|)$ second-stage variables, while the decomposition holds one scenario block at a time.

```python
"""Two-stage capacity planning: extensive form (deterministic equivalent)."""
from __future__ import annotations

import gurobipy as gp
import numpy as np
from gurobipy import GRB


def generate_capacity_instance(m: int, n: int, n_scen: int, seed: int) -> dict:
    """m plants x n customers; uniform scenario demands; shortfall penalty rho."""
    rng = np.random.default_rng(seed)
    return {"fixed": rng.uniform(40.0, 80.0, size=m), "kappa": 10.0, "u_max": 6,
            "cost": rng.uniform(1.0, 6.0, size=(m, n)),
            "demand": rng.uniform(5.0, 25.0, size=(n_scen, n)),
            "prob": np.full(n_scen, 1.0 / n_scen), "rho": 50.0}


def solve_extensive_form(inst: dict) -> tuple[float, np.ndarray]:
    """One monolithic MIP with a copy of the second stage per scenario."""
    m, n = inst["cost"].shape
    n_scen = inst["demand"].shape[0]
    model = gp.Model("capacity-extensive")
    model.Params.OutputFlag = 0
    y = model.addVars(m, vtype=GRB.INTEGER, ub=inst["u_max"], name="y")
    x = model.addVars(m, n, n_scen, lb=0.0, name="x")
    g = model.addVars(n, n_scen, lb=0.0, name="g")
    model.setObjective(
        gp.quicksum(inst["fixed"][i] * y[i] for i in range(m))
        + gp.quicksum(inst["prob"][s] * (
            gp.quicksum(inst["cost"][i, j] * x[i, j, s]
                        for i in range(m) for j in range(n))
            + inst["rho"] * gp.quicksum(g[j, s] for j in range(n)))
            for s in range(n_scen)),
        GRB.MINIMIZE)
    model.addConstrs((gp.quicksum(x[i, j, s] for j in range(n))
                      <= inst["kappa"] * y[i]
                      for i in range(m) for s in range(n_scen)), name="capacity")
    model.addConstrs((gp.quicksum(x[i, j, s] for i in range(m)) + g[j, s]
                      >= inst["demand"][s, j]
                      for j in range(n) for s in range(n_scen)), name="demand")
    model.optimize()
    assert model.Status == GRB.OPTIMAL
    return model.ObjVal, np.array([round(y[i].X) for i in range(m)])


inst = generate_capacity_instance(m=4, n=6, n_scen=20, seed=3)
obj, y_ef = solve_extensive_form(inst)
print(round(obj, 4), y_ef)
# Expected: 773.5573 [6 4 1 0] -- eleven capacity units over three plants;
# the L-shaped method below reproduces this value exactly.
```

The L-shaped implementation uses the **primal** subproblem pattern: one scenario LP built once, re-targeted per `(y, scenario)` by updating constraint right-hand sides (`Constr.RHS`), with duals read from `Constr.Pi`. RHS updates preserve the basis, so each re-solve is a warm-started dual simplex — orders of magnitude cheaper than rebuilding.

```python
"""Multi-cut L-shaped method for two-stage stochastic capacity planning."""
from __future__ import annotations

import math

import gurobipy as gp
import numpy as np
from gurobipy import GRB


def generate_capacity_instance(m: int, n: int, n_scen: int, seed: int) -> dict:
    """Identical generator and seed => identical instance to the extensive form."""
    rng = np.random.default_rng(seed)
    return {"fixed": rng.uniform(40.0, 80.0, size=m), "kappa": 10.0, "u_max": 6,
            "cost": rng.uniform(1.0, 6.0, size=(m, n)),
            "demand": rng.uniform(5.0, 25.0, size=(n_scen, n)),
            "prob": np.full(n_scen, 1.0 / n_scen), "rho": 50.0}


class ScenarioSubproblem:
    """Second-stage LP built once; only constraint RHS change per (y, scenario)."""

    def __init__(self, inst: dict) -> None:
        m, n = inst["cost"].shape
        self.inst = inst
        self.model = gp.Model("second-stage")
        self.model.Params.OutputFlag = 0
        x = self.model.addVars(m, n, lb=0.0, name="x")
        g = self.model.addVars(n, lb=0.0, name="g")
        self.model.setObjective(
            gp.quicksum(inst["cost"][i, j] * x[i, j] for i in range(m) for j in range(n))
            + inst["rho"] * gp.quicksum(g.values()), GRB.MINIMIZE)
        self.cap = [self.model.addConstr(
            gp.quicksum(x[i, j] for j in range(n)) <= 0.0, name=f"cap_{i}")
            for i in range(m)]
        self.dem = [self.model.addConstr(
            gp.quicksum(x[i, j] for i in range(m)) + g[j] >= 0.0, name=f"dem_{j}")
            for j in range(n)]

    def solve(self, y_val: np.ndarray, demand: np.ndarray) -> tuple[float, np.ndarray, np.ndarray]:
        """Return (Q_s(y), pi over demand rows, mu over capacity rows)."""
        for i, con in enumerate(self.cap):
            con.RHS = self.inst["kappa"] * y_val[i]
        for j, con in enumerate(self.dem):
            con.RHS = demand[j]
        self.model.optimize()
        assert self.model.Status == GRB.OPTIMAL   # complete recourse: never infeasible
        return (self.model.ObjVal,
                np.array([con.Pi for con in self.dem]),
                np.array([con.Pi for con in self.cap]))


def solve_lshaped(inst: dict, tol: float = 1e-6, max_iters: int = 100) -> dict:
    """Multi-cut L-shaped loop; integer master re-solved each iteration."""
    m, n = inst["cost"].shape
    n_scen = inst["demand"].shape[0]
    master = gp.Model("lshaped-master")
    master.Params.OutputFlag = 0
    y = master.addVars(m, vtype=GRB.INTEGER, ub=inst["u_max"], name="y")
    theta = master.addVars(n_scen, lb=0.0, name="theta")  # recourse cost >= 0
    master.setObjective(
        gp.quicksum(inst["fixed"][i] * y[i] for i in range(m))
        + gp.quicksum(inst["prob"][s] * theta[s] for s in range(n_scen)),
        GRB.MINIMIZE)
    sub = ScenarioSubproblem(inst)

    best_ub, best_y, log = math.inf, None, []
    for it in range(1, max_iters + 1):
        master.optimize()
        lb = master.ObjVal
        y_val = np.array([round(y[i].X) for i in range(m)], dtype=float)
        expected, n_cuts = 0.0, 0
        for s in range(n_scen):
            q_s, pi, mu = sub.solve(y_val, inst["demand"][s])
            expected += inst["prob"][s] * q_s
            if theta[s].X < q_s - tol * max(1.0, abs(q_s)):
                master.addConstr(
                    theta[s] >= float(pi @ inst["demand"][s]) + gp.quicksum(
                        float(mu[i]) * inst["kappa"] * y[i] for i in range(m)),
                    name=f"opt_cut_s{s}_it{it}")
                n_cuts += 1
        ub = float(inst["fixed"] @ y_val) + expected
        if ub < best_ub:
            best_ub, best_y = ub, y_val.astype(int)
        log.append((it, round(lb, 4), round(best_ub, 4), n_cuts))
        if n_cuts == 0:
            break                                  # every theta_s is exact: optimal
    return {"objective": best_ub, "y": best_y, "log": log}


inst = generate_capacity_instance(m=4, n=6, n_scen=20, seed=3)
res = solve_lshaped(inst)
print(round(res["objective"], 4), res["y"], len(res["log"]))
for row in res["log"]:
    print(row)
# Expected: 773.5573 [6 4 1 0] in 6 iterations -- identical objective and y to
# the extensive form; the log shows LB rising monotonically to meet UB, with
# all 20 scenarios cutting in early rounds (20, 20, 20 cuts), then 18, 7, 0.
```

Two contrasts with Worked Example 1 are deliberate. The classic loop here re-solves the master MIP per iteration — affordable because the master is tiny and iterations are few; switch to the callback pattern of Example 1 when it is not. And the subproblem is solved in primal form with `Pi` duals — the right pattern when the primal is the natural model and complete recourse rules out rays. For scenario generation, sample-average approximation, and EVPI/VSS analysis around this model, see stochastic-optimization.

## Advanced Techniques

### Pareto-optimal cuts (Magnanti–Wong)

Degenerate subproblems have many optimal dual solutions, and the one the simplex method happens to return often yields a weak cut. Magnanti & Wong (1981, "Accelerating Benders decomposition: algorithmic enhancement and model selection criteria") select, among all duals optimal at $\hat{y}$, one maximizing the cut value at a *core point* $y^0$ (a point in the relative interior of conv(Y)): solve a second LP over the optimal-dual face. The resulting cut is Pareto-optimal — no other cut from the same subproblem dominates it.

```python
"""Magnanti-Wong Pareto-optimal cut: re-optimize over the optimal-dual face."""
from __future__ import annotations

import gurobipy as gp
import numpy as np
from gurobipy import GRB


def pareto_optimal_cut(W: np.ndarray, T: np.ndarray, h: np.ndarray, q: np.ndarray,
                       y_hat: np.ndarray, z_hat: float,
                       y_core: np.ndarray) -> np.ndarray:
    """Among duals optimal at y_hat (value z_hat), maximize depth at y_core."""
    model = gp.Model("magnanti-wong")
    model.Params.OutputFlag = 0
    u = model.addMVar(W.shape[0], lb=0.0, name="u")
    model.addConstr(W.T @ u <= q, name="dual_feasibility")
    model.addConstr((h - T @ y_hat) @ u == z_hat, name="optimal_face")
    model.setObjective((h - T @ y_core) @ u, GRB.MAXIMIZE)
    model.optimize()
    assert model.Status == GRB.OPTIMAL
    return u.X


# --- plant-opening instance with demand 8: y_hat=(1,0) is already feasible --
W = np.array([[1.0, 1.0], [-1.0, 0.0], [0.0, -1.0]])
T = np.array([[0.0, 0.0], [8.0, 0.0], [0.0, 8.0]])
h, q = np.array([8.0, 0.0, 0.0]), np.array([1.0, 2.0])
u_mw = pareto_optimal_cut(W, T, h, q, y_hat=np.array([1.0, 0.0]), z_hat=8.0,
                          y_core=np.array([0.5, 0.5]))
print(u_mw, float(u_mw @ h), (u_mw @ T))
# Expected: one maximizer is u = [2, 1, 0], giving the cut eta >= 16 - 8*y_0,
# which dominates the naive tight cut eta >= 8 everywhere with y_0 < 1: the
# subproblem at y_hat is degenerate, and MW picks the deepest dual.
```

Practical notes: the face constraint can make the MW problem unbounded when the optimal face is — add a normalization (bound `u`'s components or its sum) or use the simpler $\varepsilon$-perturbation variant of Papadakos (2008). A fixed core point such as `0.5 * ones` works for binary masters; updating it as a running average of incumbents is common.

### Single-cut, multi-cut, and partial aggregation

Multi-cut (one `theta_s` per block) carries more information per iteration and typically cuts iteration counts by 5–10× at the price of a larger master; single-cut keeps the master lean but learns one aggregate hyperplane per round. Between them, *partial aggregation* clusters scenarios into K groups with one `theta_k` each — for thousands of scenarios, K in the tens is a strong default (Trukhanov, Ntaimo & Schaefer 2010, adaptive multicut). Choose by master-solve share of runtime: master-bound → aggregate more; iteration-bound → disaggregate.

### Stabilization and in-out separation

The master's argmin jumps wildly between distant `y` in early iterations ("bang-bang" behavior), producing shallow cuts and the long flat tail typical of naive Benders. In-out separation (Ben-Ameur & Neto 2007; used to great effect in Fischetti, Ljubić & Sinnl 2017) separates not at the master optimum $\hat{y}$ but at an interpolation $\lambda \hat{y} + (1-\lambda) \tilde{y}$ toward a stabilizing point $\tilde{y}$ (e.g., the incumbent or a core point), with $\lambda \approx 0.5$ and a fallback to $\hat{y}$ when no cut is violated. Alternatives with the same intent: trust-region constraints on `y` (limit Hamming distance per iteration), level-method stabilization, and warm-starting `eta`/`theta` with cuts harvested from the LP relaxation before integrality is enforced.

### Cuts at fractional points

Branch-and-Benders-cut as implemented in Worked Example 1 separates only at integer candidates (`MIPSOL`). Separating also at fractional LP solutions (`MIPNODE` + `cbCut`, as *user cuts*) tightens the tree bound — for UFLP the closed-form separation works unchanged at fractional `y` by replacing the open-facility minimum with the LP value $z_j(\hat{y}) = \min_i$ over a sorted scan. Standard recipe: run a classic-loop warm-up on the LP relaxation until the root bound stalls, load those cuts into the MIP, then go single-tree with `MIPSOL` lazy cuts plus throttled `MIPNODE` cuts (e.g., only at the root). See gurobi-advanced-features for callback plumbing details.

### Integer or nonlinear subproblems

Classic cuts need LP duality. When the subproblem keeps discrete decisions: **logic-based Benders** (Hooker & Ottosson 2003) derives problem-specific cuts from an inference dual — standard in planning-plus-scheduling splits where the subproblem is a CP feasibility check; **combinatorial Benders cuts** (Codato & Fischetti 2006) exclude minimal infeasible assignments via no-good cuts `sum(1 - y_i over ones) + sum(y_i over zeros) >= 1`; the **integer L-shaped method** (Laporte & Louveaux 1993) handles integer recourse with optimality cuts built from a global lower bound `L`. All are much weaker per cut than LP-dual cuts — expect many more iterations and design the master to carry as much structure as possible. For convex nonlinear subproblems, generalized Benders (Geoffrion 1972) replaces LP duals with convex duality.

## Practical Challenges

**The first master solve is unbounded.** `eta` (or `theta_s`) has no lower bound until the first optimality cut arrives. Always set a valid bound: 0 when recourse costs are nonnegative, per-block bounds like `eta_j >= min_i c[i, j]` (Worked Example 1), or the LP-relaxation recourse value. A tight initial bound also speeds up the first iterations measurably.

**The subproblem reports status `INF_OR_UNBD` and no ray or dual is available.** Presolve's dual reductions blur the infeasible/unbounded distinction, and barrier solves do not produce vertex certificates. Set `DualReductions=0` plus `InfUnbdInfo=1`, and force simplex (`Method=0` or `1`) on subproblems whose rays or `FarkasDual` you intend to read.

**Cuts with wrong signs silently break everything.** A sign error in dualization makes cuts that are invalid (cut off the optimum) or vacuous (never bind). Discipline: derive the dual on paper for your exact inequality directions; then assert at runtime that every added cut is violated by the current master point and satisfied by a known feasible solution; and reproduce the monolithic optimum on small seeded instances before scaling. Gurobi's `Pi` convention — duals of `<=` rows are ≤ 0 in minimization, duals of `>=` rows are ≥ 0 — means you can use `Pi` values directly in the formulas of Worked Example 2 without manual sign flips.

**Convergence stalls with a long flat tail.** The textbook loop often closes 95% of the gap in a few iterations and crawls for hundreds more. In order of impact: switch to multi-cut, add Magnanti–Wong or in-out stabilization, keep a partial copy of linking constraints in the master (partial Benders retains some `x`-aggregates in the master to strengthen its relaxation), and harvest LP-relaxation cuts before going integer.

**The callback returns a wrong optimum without any error.** With `LazyConstraints=1`, correctness rests entirely on the separation routine rejecting every bad integer candidate. Off-by-one in an index, a `>` vs `>=` in the violation test, or forgetting a customer loop iteration produces a clean-looking wrong answer. Independent validation against the monolith is the only reliable detector; also log cut counts — zero cuts on a nontrivial instance is a red flag.

**The same cut is added over and over.** Usually a tolerance problem: the violation test uses a tighter tolerance than the solver's feasibility tolerance (`FeasibilityTol`, default 1e-6), so a "violated" cut is already satisfied to solver precision. Test violation with a margin one or two orders looser than what you require of the cut, scale by `max(1, |rhs|)`, and round master integer values (`np.rint`) before computing cut coefficients.

**Subproblem solves dominate the runtime.** Build each subproblem model once and update only objectives or RHS between solves — basis reuse makes re-solves nearly free (both worked examples do this). Separable blocks can be solved in parallel processes; with closed-form duals (UFLP) the LP disappears entirely. Profile master vs subproblem time per iteration before optimizing either.

**The master relaxation is hopelessly weak.** Benders moves all `x`-information out of the master; if the cuts carry it back slowly, the master bound stays near trivial. Keep valid inequalities linking `y` directly to data in the master (total capacity ≥ total demand, covering cuts, knapsack rows from aggregated constraints). They cost little and often save more iterations than any acceleration trick.

## Tools & Libraries

| Library / tool | When to use | Note |
|---|---|---|
| gurobipy | Reference implementation vehicle for both modes | `LazyConstraints`, `cbLazy`/`cbCut`, `Pi`, `FarkasDual`, `UnbdRay`; see gurobi-advanced-features |
| CPLEX (docplex) | Want automatic Benders without writing the loop | `Benders annotations` let CPLEX split master/sub itself (full or user-guided) |
| SCIP / PySCIPOpt | Open-source branch-and-Benders-cut | Benders decomposition framework with pluggable cut generators |
| HiGHS | Open-source classic loop only | Fast LP/MIP, duals available; no lazy-constraint callbacks |
| Pyomo + mpi-sppy | Stochastic programs at scale | L-shaped and progressive hedging, MPI-parallel scenario solves |
| scipy.optimize.linprog | Tiny dual subproblems without a MIP license | HiGHS backend returns duals (`res.ineqlin.marginals`) |
| networkx | Subproblems that are pure flows | Solve subproblem combinatorially, recover duals from potentials |

## Output Format

A complete Benders deliverable contains:

1. **Decomposition design summary** — a short table stating the split and cut types before any numbers:

| Element | Content |
|---|---|
| Master variables | `y` (binary/integer design), `eta`/`theta_s` (recourse value) |
| Master constraints | structural `y`-constraints, initial bounds on recourse terms |
| Subproblem(s) | LP per block (scenario/customer); primal or dual form; closed-form if available |
| Optimality cuts | formula with dual variables named; aggregation level (single/multi/partial) |
| Feasibility cuts | formula from rays, or "none — relatively complete recourse by <design choice>" |
| Execution mode | classic loop / branch-and-Benders-cut; separation points (MIPSOL/MIPNODE) |

2. **Convergence log** — one row per iteration (classic loop) or per incumbent (callback mode): `iteration, LB, best UB, gap %, optimality cuts added, feasibility cuts added, master time, subproblem time`. Report the final gap against tolerance, total iterations, and total cut counts by type.

3. **Validation report** — monolithic-model objective vs Benders objective on at least three seeded instances small enough to solve directly, with the maximum absolute deviation (must be within solver tolerance, not "close").

4. **Solution artifacts** — the first-stage decision `y` in problem terms (which facilities open, which capacities built), per-scenario or per-block recourse costs, and the instance/seed identifiers needed to reproduce every number.

5. **Performance notes** — master vs subproblem share of runtime, effect of any acceleration applied (cuts-per-iteration and iterations-to-gap with and without), and the scale at which the monolith was abandoned.

## Questions to Ask

- Which variables are the complicating ones — what would you fix to make the rest easy?
- Is the subproblem an LP once those are fixed, or does it keep integer decisions?
- Does the subproblem separate into independent blocks (scenarios, customers, periods)? How many?
- Can the subproblem be infeasible for some master solutions, or can we design that away (penalized slacks, master-side capacity constraints)?
- How large is the extensive form — has the monolithic model actually been tried in a modern solver?
- Is Gurobi (or another callback-capable solver) available, or are we restricted to a classic loop?
- What gap and wall-clock budget define "solved" — proven optimality or 1% in an hour?
- For stochastic problems: how many scenarios, and are they fixed or sampled (SAA)?
- Is there a known feasible first-stage solution to warm-start the upper bound and stabilize separation?

## Related Skills

- **stochastic-optimization** — when the two-stage structure itself is the question: scenario generation and reduction, sample-average approximation, EVPI/VSS, and the extensive form this skill decomposes.
- **facility-location-problem** — when you need the full UFLP/CFLP problem context around Worked Example 1: formulations, Lagrangian alternatives, and heuristics to warm-start the Benders master.
- **gurobi-advanced-features** — when the implementation bottleneck is solver plumbing: callback APIs, lazy vs user cuts, parameter tuning, IIS diagnosis, and MIP starts for the master.
- **milp-modeling-gurobi** — when the monolithic model needs to be built first (as baseline or because decomposition is premature): variables, constraint builders, status handling, solution extraction.
