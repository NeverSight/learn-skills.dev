---
name: dantzig-wolfe-decomposition
description: When the user wants to reformulate a structured LP or MIP via Dantzig-Wolfe decomposition — detect block-angular structure, build the master with convexity constraints, price columns from independent subproblems, and relate the DW bound to LP and Lagrangian bounds. Also use when the user mentions "Dantzig-Wolfe," "block-angular," "decomposable structure," "convexification," "master problem reformulation," or when a model splits into blocks tied by a few linking constraints. For the pricing loop and branch-and-price, see column-generation; for subgradient dual bounds, see lagrangian-relaxation.
---

# Dantzig-Wolfe Decomposition

You are an expert in Dantzig-Wolfe (DW) decomposition for linear and mixed-integer programs. This skill covers detecting block-angular structure in a constraint matrix, reformulating the original (compact) model into a master problem with convexity constraints plus independent pricing subproblems, solving the reformulation by column generation, and interpreting the resulting bound against the LP relaxation, the Lagrangian dual, and the integer optimum. Use the framework below to decide whether a model is worth decomposing, to execute the reformulation correctly, and to verify the bound relationships on the user's instance.

## Initial Assessment

Establish the following before reformulating anything:

- **Structure.** Which constraint rows couple otherwise-independent variable groups? Ask the user to name the natural blocks (plants, vehicles, machines, periods, scenarios). If they cannot, run structure detection on the constraint matrix (section below).
- **Linking fraction.** Count linking rows m0 versus total rows. DW pays off when m0 is small relative to the block rows — a useful rule of thumb is linking rows below 10-20% of all rows.
- **Problem class.** LP or MIP? If MIP, locate the integrality: integer variables inside blocks make the DW bound potentially stronger than the LP bound; integrality that lives only in the linking rows gains nothing from convexification.
- **Block inventory.** Number of blocks K, variables per block, and whether the blocks are identical (same costs, same constraint data). Identical blocks call for the aggregated master, which removes symmetry.
- **Pricing tractability.** What does one block look like in isolation? A knapsack, a shortest path, a small assignment, a small MIP? The whole method stands or falls on solving the pricing problem quickly and repeatedly.
- **Boundedness.** Are the block polyhedra bounded? If not, the implementation must handle extreme rays, not just extreme points.
- **Goal.** A tighter dual bound, a faster LP solve on a huge structured model, or an integer optimum? The first two end with column generation; the third requires branch-and-price (hand off to the column-generation skill).
- **Baseline.** Solve the compact model (or its LP relaxation) first. Record z_LP, the MIP gap, and the time. Without this baseline you cannot say whether DW helped.
- **Solver access.** Gurobi license for master and pricing? If not, plan for HiGHS as the master LP solver and GCG/SCIP for an automatic end-to-end alternative.
- **Stopping policy.** Run column generation to proven optimality, or stop early on a Lagrangian-bound gap? Agree on the tolerance up front.
- **Time budget.** Per-iteration cost is one RMP LP plus K pricing solves. Estimate iterations in the tens-to-hundreds range and check the budget supports that.

## Decomposition Anatomy

### Block-angular form

DW applies to problems whose constraint matrix is block-angular: a few linking rows across all variables, then independent diagonal blocks.

$$
z_{\mathrm{IP}} \;=\; \min \;\sum_{k=1}^{K} c_k^{\top} x_k
\quad \text{s.t.} \quad
\sum_{k=1}^{K} A_k x_k \;\{\le,=,\ge\}\; b \;\;[\pi], \qquad
x_k \in X_k, \;\; k = 1,\dots,K,
$$

where $X_k = \{x \in \mathbb{Z}_+^{n_k} \text{ (or } \mathbb{R}_+^{n_k}\text{)} : D_k x \le d_k\}$ collects the block-k constraints and the linking constraints have $m_0$ rows with duals $\pi$.

### Reformulation by convexification

By the Minkowski-Weyl theorem, every point of $\operatorname{conv}(X_k)$ is a convex combination of its extreme points $\{x_k^p\}_{p \in P_k}$ plus a conic combination of its extreme rays $\{r_k^q\}_{q \in Q_k}$. Substituting

$$
x_k = \sum_{p \in P_k} \lambda_{kp}\, x_k^p + \sum_{q \in Q_k} \mu_{kq}\, r_k^q,
\qquad \sum_{p \in P_k} \lambda_{kp} = 1, \quad \lambda, \mu \ge 0
$$

into the linking constraints yields the **DW master problem**:

$$
z_{\mathrm{DW}} = \min \sum_{k,p} (c_k^{\top} x_k^p)\, \lambda_{kp} + \sum_{k,q} (c_k^{\top} r_k^q)\, \mu_{kq}
$$

$$
\text{s.t.} \quad \sum_{k,p} (A_k x_k^p)\, \lambda_{kp} + \sum_{k,q} (A_k r_k^q)\, \mu_{kq} \;\{\le,=,\ge\}\; b \;\;[\pi],
\qquad \sum_{p} \lambda_{kp} = 1 \;\;[\sigma_k], \;\; k=1,\dots,K.
$$

The per-block equations $\sum_p \lambda_{kp} = 1$ are the **convexity constraints**; their duals $\sigma_k$ price block membership. The master has one column per extreme point or ray — exponentially many — so it is solved by column generation over a **restricted master problem (RMP)**: solve the RMP, read $(\pi, \sigma)$, and for each block solve the **pricing problem**

$$
\bar{c}_k \;=\; \min_{x \in X_k} \;(c_k - A_k^{\top}\pi)^{\top} x \;-\; \sigma_k .
$$

If $\bar{c}_k < 0$, add the optimal point as a column (coefficients $A_k x$, convexity coefficient 1). If pricing is unbounded, the returned extreme ray $r$ with $(c_k - A_k^{\top}\pi)^{\top} r < 0$ enters as a ray column (no convexity coefficient). When no block prices out, the master is optimal (Dantzig & Wolfe 1960, "Decomposition principle for linear programs"; finite convergence because there are finitely many extreme points and rays).

### Bound hierarchy and the Lagrangian connection

For a MIP with integer blocks, convexification replaces each block's LP relaxation by $\operatorname{conv}(X_k)$, so

$$
z_{\mathrm{LP}} \;\le\; z_{\mathrm{DW}} \;=\; z_{\mathrm{LD}} \;\le\; z_{\mathrm{IP}},
$$

where $z_{\mathrm{LD}}$ is the Lagrangian dual obtained by dualizing exactly the linking constraints. The first inequality is strict precisely when some $\operatorname{conv}(X_k)$ is strictly inside the block's LP relaxation — i.e., when the subproblems lack the **integrality property** (Geoffrion 1974, "Lagrangean relaxation for integer programming"). If every block prices integrally already (network flow, assignment, transportation blocks), then $z_{\mathrm{DW}} = z_{\mathrm{LP}}$ and DW buys structure and parallelism but no bound.

At any iteration with duals $\pi$, weak duality gives the **Lagrangian bound**

$$
L(\pi) \;=\; \pi^{\top} b + \sum_{k} \min_{x \in X_k} (c_k - A_k^{\top}\pi)^{\top} x
\;=\; z_{\mathrm{RMP}} + \sum_{k} \bar{c}_k \;\le\; z_{\mathrm{DW}},
$$

using LP duality on the RMP ($z_{\mathrm{RMP}} = \pi^{\top}b + \sum_k \sigma_k$). Track $\max_\pi L(\pi)$ across iterations: it sandwiches $z_{\mathrm{DW}}$ from below and supports early stopping long before pricing fully converges. If any block pricing is unbounded, $L(\pi) = -\infty$ for that $\pi$ and the bound update is skipped.

### When to decompose — decision guidance

| Situation | Recommendation |
|---|---|
| Many blocks, few linking rows, integer blocks without integrality property | DW: bound improves and pricing decomposes |
| Blocks are pure network/assignment structures | DW bound = LP bound; decompose only for size/parallelism |
| Identical blocks (rolls, vehicles, machines) | DW with aggregated master; removes block symmetry |
| Linking rows dominate the matrix | Do not decompose; consider Benders if variables (not rows) split instead |
| Pricing has no exploitable structure and is itself a hard MIP | Expect pricing to dominate runtime; try heuristic pricing or skip DW |
| Compact LP already solves in seconds with a small gap | Skip DW; the overhead will not pay |

## Detecting Block-Angular Structure

Before reformulating, confirm the structure actually decomposes. Remove the candidate linking rows and compute connected components of the row-column bipartite graph: each component is one block. The greedy density heuristic below is cheap and works when coupling rows are dense; production-grade detection uses hypergraph partitioning (Bergner et al. 2015, "Automatic Dantzig-Wolfe reformulation of mixed integer programs", the basis of GCG's detector).

```python
"""Block-angular structure detection on the constraint matrix."""
import numpy as np
import scipy.sparse as sp
from scipy.sparse.csgraph import connected_components


def find_blocks(A: sp.csr_matrix,
                linking_rows: np.ndarray) -> list[tuple[np.ndarray, np.ndarray]]:
    """Split A into independent blocks after removing the linking rows.

    Returns one (row_indices, col_indices) pair per block, with row indices
    referring to the original matrix. Columns appearing only in linking rows
    form their own zero-row blocks and are reported too.
    """
    m, n = A.shape
    keep = np.setdiff1d(np.arange(m), np.asarray(linking_rows, dtype=int))
    pattern = (A[keep, :] != 0).astype(np.int8)
    # Bipartite graph: kept rows are nodes 0..len(keep)-1, columns follow.
    graph = sp.bmat([[None, pattern], [pattern.T, None]], format="csr")
    _, labels = connected_components(graph, directed=False)
    blocks = []
    for comp in np.unique(labels[len(keep):]):           # components holding a column
        rows = keep[labels[: len(keep)] == comp]
        cols = np.where(labels[len(keep):] == comp)[0]
        blocks.append((rows, cols))
    return blocks


def greedy_linking_rows(A: sp.csr_matrix, max_linking: int) -> np.ndarray:
    """Cheap detection heuristic: peel off the densest rows one at a time.

    Dense rows are the most likely coupling rows. Keep the smallest removal
    set that maximizes the block count within the budget. Serious detection
    uses hypergraph partitioning (Bergner et al. 2015).
    """
    density = np.diff(A.tocsr().indptr)                  # nonzeros per row
    order = np.argsort(-density)
    best = np.array([], dtype=int)
    best_count = len(find_blocks(A, best))
    for take in range(1, max_linking + 1):
        cand = order[:take]
        count = len(find_blocks(A, cand))
        if count > best_count:
            best, best_count = cand, count
    return np.sort(best)


if __name__ == "__main__":
    # 3 blocks of 2 vars each, 2 block rows per block, 2 dense linking rows on top.
    block = np.array([[3.0, 5.0], [4.0, 2.0]])
    A = sp.csr_matrix(np.vstack([np.ones((2, 6)),
                                 sp.block_diag([block] * 3).toarray()]))
    linking = greedy_linking_rows(A, max_linking=3)
    print("linking rows:", linking)
    for rows, cols in find_blocks(A, linking):
        print("block rows", rows, "cols", cols)
    # Expected: linking rows [0 1]; three blocks with rows [2 3], [4 5], [6 7]
    # and columns [0 1], [2 3], [4 5] respectively.
```

If the heuristic finds no decomposition, the model may still decompose after assigning a small number of "ambiguous" rows to blocks by hand, or after a variable permutation suggested by domain knowledge (one block per machine, period, or scenario). When the matrix is born from a model you wrote, prefer annotating blocks at modeling time over rediscovering them numerically.

## Generic Dantzig-Wolfe Implementation

The driver below is problem-independent. Each block supplies its cost vector, its linking-row coefficients, and a pricing oracle; the driver owns the RMP, the artificial columns, the dual extraction, the ray handling, and the Lagrangian bound.

```text
DANTZIG-WOLFE COLUMN GENERATION (minimization)

Input: blocks k = 1..K with costs c_k, linking coefficients A_k, sets X_k;
       linking RHS b with senses; tolerance tol.

1   build RMP: linking rows, one convexity row per block,
    big-M artificial columns so the RMP starts feasible
2   repeat
3       solve RMP (LP)  ->  z_RMP, duals pi (linking), sigma_k (convexity)
4       for each block k:
5           solve pricing  v_k = min { (c_k - A_k' pi)' x : x in X_k }
6           if unbounded with extreme ray r:  rc = (c_k - A_k' pi)' r
7           else:                             rc = v_k - sigma_k
8           if rc < -tol: add the point/ray column to the RMP
9       if no block returned a ray:
10          best_LB = max(best_LB, z_RMP + sum_k rc_k)     # Lagrangian bound
11  until no column was added  or  z_RMP - best_LB <= tol
12  z_DW = z_RMP; recover x_k = sum_p lambda_kp x_k^p + sum_q mu_kq r_k^q
13  fail loudly if any artificial is positive (original problem infeasible)
```

```python
"""Generic Dantzig-Wolfe driver. Save as dw_framework.py for the worked examples."""
import math
from dataclasses import dataclass
from typing import Callable

import gurobipy as gp
import numpy as np
from gurobipy import GRB

PricingResult = tuple[float, np.ndarray, bool]  # (value, point or ray, is_ray)


@dataclass
class Block:
    """Subproblem k: cost c_k, linking coefficients A_k, and a pricing oracle.

    pricing(price) minimizes price @ x over X_k. It returns (value, x, False)
    for an optimal extreme point, or (price @ r, r, True) for an extreme ray r
    that proves the pricing problem is unbounded.
    """

    c: np.ndarray                    # shape (n_k,): original block costs
    A: np.ndarray                    # shape (m0, n_k): linking-row coefficients
    pricing: Callable[[np.ndarray], PricingResult]


def make_block_pricing(D: np.ndarray, d: np.ndarray,
                       vtype: str = GRB.CONTINUOUS) -> Callable[[np.ndarray], PricingResult]:
    """Build a pricing oracle for X_k = {x >= 0 : D x <= d} (LP or integer)."""
    model = gp.Model("pricing")
    model.Params.OutputFlag = 0
    model.Params.InfUnbdInfo = 1     # make extreme rays available
    model.Params.DualReductions = 0  # distinguish INFEASIBLE from UNBOUNDED
    x = model.addMVar(D.shape[1], lb=0.0, vtype=vtype, name="x")
    model.addConstr(D @ x <= d, name="block")

    def pricing(price: np.ndarray) -> PricingResult:
        """Minimize price @ x over the block polyhedron."""
        model.setObjective(price @ x, GRB.MINIMIZE)
        model.optimize()
        if model.Status == GRB.OPTIMAL:
            return model.ObjVal, x.X.copy(), False
        if model.Status == GRB.UNBOUNDED and vtype == GRB.CONTINUOUS:
            ray = np.array(model.getAttr("UnbdRay", model.getVars()))
            ray /= np.abs(ray).max()           # scale for numerical sanity
            return float(price @ ray), ray, True
        raise RuntimeError(f"pricing status {model.Status}: integer blocks must be bounded")

    return pricing


class DantzigWolfe:
    """Dantzig-Wolfe master with one convexity constraint per block."""

    def __init__(self, blocks: list[Block], b: np.ndarray, senses: str,
                 big_m: float = 1e6) -> None:
        """senses is one character per linking row, each of '<', '=', '>'."""
        self.blocks = blocks
        self.b = np.asarray(b, dtype=float)
        self.master = gp.Model("rmp")
        self.master.Params.OutputFlag = 0
        smap = {"<": GRB.LESS_EQUAL, "=": GRB.EQUAL, ">": GRB.GREATER_EQUAL}
        self.link = [self.master.addLConstr(gp.LinExpr(), smap[s], rhs, name=f"link[{i}]")
                     for i, (s, rhs) in enumerate(zip(senses, self.b))]
        self.conv = [self.master.addLConstr(gp.LinExpr(), GRB.EQUAL, 1.0, name=f"conv[{k}]")
                     for k in range(len(blocks))]
        # Artificial variables keep the RMP feasible before real columns exist.
        self.artificials: list[gp.Var] = []
        for i, s in enumerate(senses):
            if s in ("=", ">"):
                self.artificials.append(self.master.addVar(
                    obj=big_m, name=f"art_up[{i}]", column=gp.Column([1.0], [self.link[i]])))
            if s in ("=", "<"):
                self.artificials.append(self.master.addVar(
                    obj=big_m, name=f"art_dn[{i}]", column=gp.Column([-1.0], [self.link[i]])))
        for k in range(len(blocks)):
            self.artificials.append(self.master.addVar(
                obj=big_m, name=f"art_conv[{k}]", column=gp.Column([1.0], [self.conv[k]])))
        self.columns: list[tuple[int, np.ndarray, bool, gp.Var]] = []
        self.history: list[dict] = []

    def _add_column(self, k: int, x: np.ndarray, is_ray: bool) -> None:
        """Append one point or ray column for block k to the RMP."""
        blk = self.blocks[k]
        coeffs = [float(v) for v in blk.A @ x]
        constrs: list[gp.Constr] = list(self.link)
        if not is_ray:
            coeffs.append(1.0)               # convexity coefficient (points only)
            constrs.append(self.conv[k])
        var = self.master.addVar(obj=float(blk.c @ x), lb=0.0,
                                 name=f"col[{k},{len(self.columns)}]",
                                 column=gp.Column(coeffs, constrs))
        self.columns.append((k, x.copy(), is_ray, var))

    def solve(self, tol: float = 1e-6, max_iters: int = 200) -> dict:
        """Run column generation; return bounds, recovered x_k, and the iteration log."""
        best_lb = -math.inf
        z_rmp = math.inf
        for it in range(1, max_iters + 1):
            self.master.optimize()
            if self.master.Status != GRB.OPTIMAL:
                raise RuntimeError(f"RMP status {self.master.Status}")
            z_rmp = self.master.ObjVal
            pi = np.array([c.Pi for c in self.link])
            sigma = np.array([c.Pi for c in self.conv])
            new_cols, rc_sum, ray_seen = 0, 0.0, False
            for k, blk in enumerate(self.blocks):
                value, x, is_ray = blk.pricing(blk.c - blk.A.T @ pi)
                rc = value if is_ray else value - sigma[k]
                ray_seen = ray_seen or is_ray
                rc_sum += 0.0 if is_ray else rc
                if rc < -tol:
                    self._add_column(k, x, is_ray)
                    new_cols += 1
            if not ray_seen:                  # Lagrangian bound L(pi), see anatomy
                best_lb = max(best_lb, z_rmp + rc_sum)
            self.history.append({"iter": it, "z_rmp": z_rmp,
                                 "lower_bound": best_lb, "new_cols": new_cols})
            if new_cols == 0 or z_rmp - best_lb <= tol * max(1.0, abs(z_rmp)):
                break
        if any(a.X > 1e-6 for a in self.artificials):
            raise RuntimeError("artificials positive at the end: instance infeasible "
                               "or big_m too small")
        x_blocks = [np.zeros(len(blk.c)) for blk in self.blocks]
        for k, x, _, var in self.columns:
            x_blocks[k] += var.X * x
        return {"z_dw": z_rmp, "lower_bound": best_lb,
                "iterations": len(self.history), "x_blocks": x_blocks}
```

Design notes. The pricing oracle is a closure over a persistent Gurobi model, so each call only swaps the objective — no model rebuild. Reduced-cost sums feed the Lagrangian bound $L(\pi) = z_{\mathrm{RMP}} + \sum_k \bar{c}_k$ every iteration, which is what allows the early-exit gap test on line `z_rmp - best_lb <= tol * ...`. Rays carry no convexity coefficient, exactly mirroring the reformulation. The recovered `x_blocks` solve the original constraints but are generally fractional in the original variables even when every generated column is integral — that is the convexification at work, and it is why integer answers need branch-and-price.

## Worked Example 1: Multi-Plant Production Planning

Three plants produce two products in integer batches. Each plant k has its own two resource constraints (the block $X_k = \{x \in \mathbb{Z}_+^2 : R_k x \le \mathrm{cap}_k\}$), and the only coupling is demand coverage:

$$
\min \sum_{k=1}^{3}\sum_{j=1}^{2} c_{kj} x_{kj}
\quad \text{s.t.} \quad
\sum_{k} x_{kj} \ge \mathrm{dem}_j \;\; (j=1,2), \qquad
x_k \in X_k \;\; (k=1,2,3).
$$

Each plant's linking coefficients are $A_k = I_2$: plant k contributes its own production to each demand row. The blocks are bounded integer programs without the integrality property, so $z_{\mathrm{DW}}$ should strictly beat $z_{\mathrm{LP}}$.

```python
"""Multi-plant production planning: compact MIP and its LP relaxation.

Save as multiplant.py; the DW run in the next block imports make_instance.
"""
import gurobipy as gp
import numpy as np
from gurobipy import GRB


def make_instance() -> dict:
    """Three plants, two products, two resources per plant. Integer batches."""
    return {
        "cost": np.array([[4.0, 7.0], [5.0, 6.0], [6.0, 5.0]]),   # (K, J)
        "use": [np.array([[3.0, 5.0], [4.0, 2.0]]),               # R_k: (2, J)
                np.array([[2.0, 4.0], [5.0, 3.0]]),
                np.array([[4.0, 3.0], [3.0, 4.0]])],
        "cap": [np.array([25.0, 22.0]),
                np.array([20.0, 24.0]),
                np.array([26.0, 23.0])],
        "demand": np.array([10.0, 8.0]),
    }


def solve_compact(data: dict, relax: bool) -> float:
    """Solve the compact model; relax=True drops integrality on the batches."""
    K, J = data["cost"].shape
    model = gp.Model("multiplant")
    model.Params.OutputFlag = 0
    vtype = GRB.CONTINUOUS if relax else GRB.INTEGER
    x = model.addMVar((K, J), lb=0.0, vtype=vtype, name="x")
    for k in range(K):
        model.addConstr(data["use"][k] @ x[k, :] <= data["cap"][k], name=f"capacity[{k}]")
    model.addConstr(x.sum(axis=0) >= data["demand"], name="demand")
    model.setObjective((data["cost"] * x).sum(), GRB.MINIMIZE)
    model.optimize()
    assert model.Status == GRB.OPTIMAL
    return model.ObjVal


if __name__ == "__main__":
    data = make_instance()
    print(f"compact LP relaxation: {solve_compact(data, relax=True):.4f}")
    print(f"compact IP optimum:    {solve_compact(data, relax=False):.4f}")
    # Expected: compact LP relaxation 90.0909, compact IP optimum 92.0000
```

Now decompose: one `Block` per plant with integer pricing over its own capacity polytope, identity linking coefficients, and `>` senses on the two demand rows.

```python
"""Dantzig-Wolfe on the multi-plant instance: convexified integer blocks."""
import numpy as np
from gurobipy import GRB

from dw_framework import Block, DantzigWolfe, make_block_pricing   # framework above
from multiplant import make_instance, solve_compact                # compact model above


def run() -> None:
    """Compare z_LP <= z_DW <= z_IP on the three-plant instance."""
    data = make_instance()
    K, J = data["cost"].shape
    blocks = [Block(c=data["cost"][k],
                    A=np.eye(J),     # plant k adds x_kj to demand row j
                    pricing=make_block_pricing(data["use"][k], data["cap"][k],
                                               vtype=GRB.INTEGER))
              for k in range(K)]
    dw = DantzigWolfe(blocks, b=data["demand"], senses=">" * J)
    result = dw.solve()
    z_lp = solve_compact(data, relax=True)
    z_ip = solve_compact(data, relax=False)
    print(f"z_LP = {z_lp:.4f}  z_DW = {result['z_dw']:.4f}  z_IP = {z_ip:.4f}")
    print(f"iterations = {result['iterations']}, columns = {len(dw.columns)}")
    for k, xk in enumerate(result["x_blocks"]):
        print(f"plant {k}: x = {np.round(xk, 4)}")
    for row in dw.history:
        print(row)


if __name__ == "__main__":
    run()
    # Expected: z_LP = 90.0909 < z_DW = 91.4000 < z_IP = 92.0000
    # (6 iterations, 12 columns; DW closes about 69% of the LP-IP gap).
    # Recovered plan: plant 0 -> [5, 1], plant 1 -> [3.2, 2.6], plant 2 -> [1.8, 4.4];
    # plants 1 and 2 are fractional convex combinations of integer pricing points.
```

Reading the run: the first two RMP values are dominated by big-M artificials; once real columns cover the demand rows, z_RMP drops to the 90s while the Lagrangian bound climbs (73.2 → 86.0 → 91.0 → 91.4) until the two meet at the DW optimum. Every column generated is an integer production plan for one plant, yet the master mixes them fractionally — the bound improved from 90.09 to 91.4 exactly because conv(X_k) cuts off fractional plans like x = (8.33, 0) that the compact LP relaxation allows.

## Worked Example 2: Cutting Stock — Compact vs. DW Reformulation

The one-dimensional cutting-stock problem is the canonical demonstration that the *same problem* under two formulations gives very different bounds. The compact (Kantorovich) model has one identical block per stock roll $k$: $y_k \in \{0,1\}$ (roll used) and $x_{ik} \in \mathbb{Z}_+$ (copies of item i cut from roll k), with block constraint $\sum_i l_i x_{ik} \le W y_k$ and linking constraints $\sum_k x_{ik} \ge d_i$. Its LP relaxation is famously weak — exactly the material bound $\sum_i l_i d_i / W$ (de Carvalho 2002, "LP models for bin packing and cutting stock problems").

Applying DW with one convexity row per roll and then **aggregating the identical blocks** (sum the K convexity constraints into $\sum_p \lambda_p \le K$, which is slack at the optimum and can be dropped because the objective already counts used rolls) yields the Gilmore-Gomory pattern formulation (Gilmore & Gomory 1961, "A linear programming approach to the cutting-stock problem"):

$$
z_{\mathrm{DW}} = \min \sum_{p} \lambda_p
\quad \text{s.t.} \quad
\sum_{p} a_{ip}\, \lambda_p \ge d_i \;\;[\pi_i], \qquad \lambda \ge 0,
$$

with one column per feasible cutting pattern $a \in \mathbb{Z}_+^{n}$, $\sum_i l_i a_i \le W$. Pricing is an unbounded knapsack: a pattern improves the master iff $\sum_i \pi_i a_i > 1$. The DW bound is so strong that the modified integer round-up property $z_{\mathrm{IP}} \le \lceil z_{\mathrm{DW}} \rceil + 1$ is conjectured to always hold (Scheithauer & Terno 1995).

```python
"""Cutting stock, compact (Kantorovich) model. Save as kantorovich.py."""
import gurobipy as gp
import numpy as np
from gurobipy import GRB


def make_instance() -> dict:
    """Tiny cutting-stock instance: roll width 10, three item lengths."""
    return {"W": 10.0,
            "lengths": np.array([6.0, 5.0, 3.0]),
            "demand": np.array([2, 2, 4])}


def solve_kantorovich(data: dict, relax: bool) -> float:
    """One block per roll: y_k roll used, x_ik copies of item i cut from roll k."""
    lengths, demand, W = data["lengths"], data["demand"], data["W"]
    n_items, n_rolls = len(lengths), int(demand.sum())   # demand.sum() rolls suffice
    model = gp.Model("kantorovich")
    model.Params.OutputFlag = 0
    if relax:
        y = model.addMVar(n_rolls, lb=0.0, ub=1.0, name="y")
        x = model.addMVar((n_items, n_rolls), lb=0.0, name="x")
    else:
        y = model.addMVar(n_rolls, vtype=GRB.BINARY, name="y")
        x = model.addMVar((n_items, n_rolls), lb=0.0, vtype=GRB.INTEGER, name="x")
    for k in range(n_rolls):
        model.addConstr(lengths @ x[:, k] <= W * y[k], name=f"width[{k}]")   # block k
    model.addConstr(x.sum(axis=1) >= demand, name="demand")                  # linking
    model.setObjective(y.sum(), GRB.MINIMIZE)
    model.optimize()
    assert model.Status == GRB.OPTIMAL
    return model.ObjVal


if __name__ == "__main__":
    data = make_instance()
    print(f"Kantorovich LP bound: {solve_kantorovich(data, relax=True):.4f}")
    print(f"material bound:       {data['lengths'] @ data['demand'] / data['W']:.4f}")
    print(f"IP optimum:           {solve_kantorovich(data, relax=False):.4f}")
    # Expected: Kantorovich LP bound 3.4000 (= material bound 3.4000), IP optimum 4.0000
```

The DW reformulation, with dynamic-programming knapsack pricing instead of a MIP oracle — this is the structure-exploitation payoff the Initial Assessment asks about:

```python
"""Cutting stock, Dantzig-Wolfe (Gilmore-Gomory) reformulation with aggregation."""
import gurobipy as gp
import numpy as np
from gurobipy import GRB

from kantorovich import make_instance, solve_kantorovich   # compact model above


def knapsack_pricing(lengths: np.ndarray, W: float, pi: np.ndarray) -> tuple[float, np.ndarray]:
    """Unbounded knapsack DP: max pi @ a s.t. lengths @ a <= W, a integer >= 0."""
    cap = int(W)
    sizes = lengths.astype(int)
    value = np.zeros(cap + 1)
    choice = np.full(cap + 1, -1, dtype=int)
    for w in range(1, cap + 1):
        value[w] = value[w - 1]                # leave one unit of width unused
        for i, s in enumerate(sizes):
            if s <= w and value[w - s] + pi[i] > value[w]:
                value[w] = value[w - s] + pi[i]
                choice[w] = i
    pattern = np.zeros(len(lengths))
    w = cap
    while w > 0:
        if choice[w] >= 0:
            pattern[choice[w]] += 1
            w -= sizes[choice[w]]
        else:
            w -= 1                             # unused width unit
    return float(value[cap]), pattern


def solve_gilmore_gomory(data: dict, tol: float = 1e-9) -> dict:
    """Aggregated DW master: min sum(lambda), pattern coverage >= demand."""
    lengths, demand, W = data["lengths"], data["demand"], data["W"]
    n_items = len(lengths)
    master = gp.Model("gg_master")
    master.Params.OutputFlag = 0
    cover = [master.addLConstr(gp.LinExpr(), GRB.GREATER_EQUAL, float(demand[i]),
                               name=f"cover[{i}]") for i in range(n_items)]
    patterns: list[np.ndarray] = []
    lam: list[gp.Var] = []

    def add_pattern(a: np.ndarray) -> None:
        """Register pattern a as a master column with unit cost."""
        col = gp.Column([float(a[i]) for i in range(n_items)], cover)
        lam.append(master.addVar(obj=1.0, lb=0.0, name=f"lam[{len(patterns)}]", column=col))
        patterns.append(a.copy())

    for i in range(n_items):                              # initial single-item patterns
        a = np.zeros(n_items)
        a[i] = np.floor(W / lengths[i])
        add_pattern(a)
    iterations = 0
    while True:
        iterations += 1
        master.optimize()
        assert master.Status == GRB.OPTIMAL
        pi = np.array([c.Pi for c in cover])
        best_value, pattern = knapsack_pricing(lengths, W, pi)
        if best_value <= 1.0 + tol:                       # reduced cost 1 - best >= 0
            break
        add_pattern(pattern)
    z_dw = master.ObjVal
    for v in lam:                                         # integer solve on final patterns
        v.VType = GRB.INTEGER
    master.optimize()
    z_int = master.ObjVal
    used = [(patterns[j], round(lam[j].X)) for j in range(len(lam)) if lam[j].X > 0.5]
    return {"z_dw": z_dw, "z_int_over_patterns": z_int,
            "iterations": iterations, "n_patterns": len(patterns), "used": used}


if __name__ == "__main__":
    data = make_instance()
    res = solve_gilmore_gomory(data)
    print(f"Kantorovich LP bound:        {solve_kantorovich(data, relax=True):.4f}")
    print(f"DW (pattern) LP bound:       {res['z_dw']:.4f}")
    print(f"integer over final patterns: {res['z_int_over_patterns']:.0f}")
    print(f"Kantorovich IP optimum:      {solve_kantorovich(data, relax=False):.0f}")
    print(f"CG iterations: {res['iterations']}, patterns: {res['n_patterns']}")
    for a, count in res["used"]:
        print(f"  cut {count} roll(s) with pattern {a.astype(int)}")
    # Expected: Kantorovich LP 3.4000 < DW pattern LP 3.6667; integer solve over
    # the final patterns gives 4 = IP optimum, in 2 CG iterations with 4 patterns.
    # Used patterns: 1 x [0 2 0], 1 x [0 0 3], 2 x [1 0 1].
```

The reformulation comparison in one line: identical bounded integer blocks, dualized demand rows, knapsack pricing — and the bound jumps from 3.4 to 3.667 while the model shrinks from `n_items × n_rolls` integer variables to a handful of pattern columns. The integer solve over the generated columns is a heuristic (columns optimal for the LP need not contain an optimal integer solution); here it happens to hit the optimum, which the Kantorovich IP confirms. Note also the relation to the modified round-up property: $\lceil 3.667 \rceil = 4 = z_{\mathrm{IP}}$.

## Advanced Techniques

### Dual stabilization with a soft box

Early RMP duals are wild — extreme points of a dual polyhedron that barely constrains them — so pricing chases noise ("heading-in") and convergence crawls near the end ("tailing-off"). A soft box (du Merle et al. 1999, "Stabilized column generation"; the hard-box ancestor is Marsten, Hogan & Blankenship 1975, the Boxstep method) penalizes duals for leaving a trust region around a center, typically the best Lagrangian point found so far:

```python
"""Soft dual box (du Merle et al. 1999) for stabilizing the DW master."""
import gurobipy as gp
import numpy as np
from gurobipy import GRB


def add_dual_box(master: gp.Model, link_constrs: list[gp.Constr],
                 center: np.ndarray, half_width: float,
                 eps: float) -> list[gp.Var]:
    """Pull each linking dual toward [center_i - w, center_i + w] via slack columns.

    In the RMP dual, the +1 column with cost center_i + w enforces
    pi_i <= center_i + w while the slack stays inside its bound; the -1 column
    enforces pi_i >= center_i - w. The upper bound eps makes the box soft:
    duals may leave it once a slack hits eps, so the master cannot become
    unbounded when the box misses the true dual region. Shrink w and recenter
    on the best Lagrangian point as CG converges; remove the columns and
    re-optimize before declaring the master optimal.
    """
    added: list[gp.Var] = []
    for i, con in enumerate(link_constrs):
        up = master.addVar(obj=float(center[i]) + half_width, lb=0.0, ub=eps,
                           name=f"stab_up[{i}]", column=gp.Column([1.0], [con]))
        dn = master.addVar(obj=-(float(center[i]) - half_width), lb=0.0, ub=eps,
                           name=f"stab_dn[{i}]", column=gp.Column([-1.0], [con]))
        added.extend([up, dn])
    return added


def remove_stabilization(master: gp.Model, stab_vars: list[gp.Var]) -> None:
    """Drop the box columns; re-optimize before trusting duals or the bound."""
    for v in stab_vars:
        master.remove(v)
    master.update()


if __name__ == "__main__":
    m = gp.Model("toy_rmp")
    m.Params.OutputFlag = 0
    x = m.addVar(obj=5.0, name="x")
    c = m.addLConstr(2.0 * x, GRB.GREATER_EQUAL, 4.0, name="link")
    stab = add_dual_box(m, [c], center=np.array([1.0]), half_width=1.0, eps=10.0)
    m.optimize()
    print(f"dual with box:    {c.Pi:.1f}")
    remove_stabilization(m, stab)
    m.optimize()
    print(f"dual without box: {c.Pi:.1f}")
    # Expected: dual with box 2.0 (capped at center + half_width), without box 2.5
```

A cheaper alternative that often suffices: solve the RMP with the barrier method and no crossover (`Method=2`, `Crossover=0`), which returns well-centered interior duals instead of vertex duals. Smoothing schemes (Wentges 1997; Pessoa et al. 2018 give the modern automatic variant) average the current duals with the best Lagrangian point and pair naturally with the bound tracking already in the framework. Full treatment belongs to the column-generation skill.

### Convexification versus discretization

Everything above is **convexification**: $\lambda$ continuous, integrality conceptually retained on the original $x_k$. The alternative, **discretization** (Vanderbeck 2000; Vanderbeck & Savelsbergh 2006, "A generic view of Dantzig-Wolfe decomposition in mixed integer programming"), enumerates the *integer points* of $X_k$ (not just extreme points) and requires $\lambda$ integral in the master. Both give the same LP bound, but discretization matters when you must express integrality in master variables: with aggregated identical blocks, "$\lambda_p$ = number of blocks using pattern p" is meaningful and branchable — exactly the Gilmore-Gomory integer master — whereas convexified $\lambda$ has no integer meaning per block. Rule of practice: pure-integer bounded blocks plus aggregation calls for discretization semantics; mixed-integer or unbounded blocks stay with convexification.

### Aggregating identical blocks

When all K blocks share the same data, per-block convexity constraints create a master in which permuting block indices yields equivalent solutions — heavy degeneracy and symmetry. Replace $\sum_p \lambda_{kp} = 1$ for each k by one aggregated constraint $\sum_p \lambda_p = K$ (or $\le K$, droppable when the objective counts active blocks, as in cutting stock). The aggregated master is smaller, prices once per iteration instead of K times, and removes the symmetry. To recover a per-block solution afterwards, greedily split the aggregated $\lambda$ into K unit-sum groups; any split is valid because the blocks are interchangeable.

### Choosing DW-CG versus subgradient on the same dual

DW column generation and Lagrangian relaxation optimize the same dual function $L(\pi)$ — DW by an LP master holding all observed cuts of the dual function, subgradient methods by first-order steps. DW gives exact dual optima, a primal (convexified) solution for free, and clean stopping criteria, but each iteration costs an LP solve and master degeneracy can hurt. Subgradient iterations are nearly free and memory-light but need step-size tuning and never certify optimality tightly. A robust hybrid: run a few hundred subgradient steps to get a good dual point cheaply, then start DW-CG with the box of the section above centered there. Cross-check: at termination both must report the same bound up to tolerance — a mismatch means a bug in pricing or in the dualization.

## Practical Challenges

**The first RMP iterations return absurd objective values and duals.** That is the big-M artificial phase: with no real columns, artificials carry the constraints and the duals equal ±big_m. It is harmless if big_m exceeds any realistic dual, but a too-small big_m silently produces an infeasible "optimum". Safer variants: a phase-1 master that minimizes artificial mass only, or seeding each block with one column priced at $\pi = 0$ (i.e., the block solved with original costs) so convexity rows are covered from the start.

**Column generation stalls near the optimum (tailing-off).** Dozens of iterations gain 0.001 each. Use the Lagrangian bound already computed by the framework: stop when $z_{\mathrm{RMP}} - \max L(\pi)$ falls below the accuracy you actually need — for a MIP bound, below 1 ulp of the rounding unit (e.g., gap < 1 when the objective is integral means the bound is proven). Stabilize the duals before blaming the method.

**Your chosen "blocks" turn out not to be independent.** A single forgotten coupling row makes pricing solutions invalid as columns. Always validate with `find_blocks` on the actual matrix: the union of returned blocks must cover every column, and every non-linking row must land in exactly one block. If a row straddles two would-be blocks, either promote it to linking (master grows) or merge the two blocks (pricing grows). Prefer merging when the merged pricing stays polynomial; prefer promoting when the row is one of few.

**Integer pricing dominates the runtime.** Each iteration solves K MIPs. Mitigations in order of payoff: replace the MIP oracle with a specialized algorithm (DP knapsack as in the cutting-stock example, labeling shortest path); accept *any* negative-reduced-cost heuristic column and call the exact oracle only when the heuristic fails (the final exact pass still certifies optimality); price blocks in parallel; keep a column pool and re-check old columns before re-pricing.

**The DW bound equals the LP bound — all that reformulation for nothing.** The blocks have the integrality property (Geoffrion 1974): e.g., assignment or pure network-flow blocks solve integrally as LPs. Re-draw the decomposition line so the *hard* integer structure sits inside the blocks: dualize a different constraint family, or enlarge blocks until they lose integrality. If no such split exists, DW still helps only via size/parallelism — say so explicitly rather than promising a better bound.

**The master solution is fractional but the user needs an integer plan.** Re-solving the final RMP with integer $\lambda$ (as in the cutting-stock example) is a quick heuristic but carries no guarantee — it can even be infeasible for set-partitioning masters. The exact route is branch-and-price with branching rules compatible with pricing; hand off to the column-generation skill rather than improvising branching on $\lambda$ variables, which destroys the pricing structure.

**Identical blocks create a degenerate, symmetric master.** K identical convexity rows admit factorially many equivalent bases; the simplex cycles through them and duals jump around. Aggregate the convexity constraints (section above). If blocks are *nearly* identical, group truly identical ones and aggregate per group.

**Degenerate master gives unstable duals even without symmetry.** Multiple dual optima are the norm in DW masters. Vertex duals from primal simplex are the worst choice; `Method=2` with `Crossover=0` (barrier, no crossover) yields interior duals that change smoothly between iterations and measurably cut iteration counts — often the cheapest "stabilization" available before adding boxes or smoothing.

## Tools & Libraries

| Library / tool | When to use | Note |
|---|---|---|
| gurobipy | RMP + LP/MIP pricing oracles, as in this skill | Fast LP reoptimization and `gp.Column` make manual DW straightforward |
| GCG (SCIP) | You want automatic detection + DW + branch-and-price without writing code | Implements Bergner et al. (2015) detection; reads plain MPS/LP files |
| PySCIPOpt | Custom pricer callbacks inside a full branch-and-price tree in Python | `Pricer` plugin class; free for academic and commercial use |
| HiGHS (highspy) | License-free RMP LP solver | Swap in for the master when no Gurobi license is at hand |
| Coluna.jl | Julia branch-and-price framework with block annotations | `BlockDecomposition` declares blocks on a JuMP model |
| VRPSolver | Routing-shaped problems needing state-of-the-art DW/branch-cut-and-price | Generic model but tuned for resource-constrained path pricing |
| scipy.sparse.csgraph | Block-structure detection on the constraint matrix | `connected_components` as used in the detection section |

## Output Format

A complete Dantzig-Wolfe deliverable contains:

1. **Decomposition summary table** — one row per block: block id, variables, constraint rows, pricing problem class (LP / knapsack / MIP), bounded or not, identical-group id. Plus the linking rows: count, senses, and which original constraints they are.
2. **Bound table** — z_LP (compact relaxation), z_DW, best incumbent / z_IP if available, absolute and relative gap closed by DW: `(z_DW - z_LP) / (z_IP - z_LP)` when z_IP is known. State explicitly whether blocks have the integrality property and therefore whether z_DW > z_LP was even possible.
3. **Convergence log** — per iteration: `iter, z_RMP, Lagrangian LB, columns added, cumulative columns, pricing time, master time`. The framework's `history` list maps one-to-one to this table; report the final gap and the stopping reason (priced out vs. gap tolerance vs. iteration cap).
4. **Recovered solution** — per-block $x_k$ from the convex combination, with an independent feasibility check against the *original* constraints (linking and block), and a clear statement of which components are fractional.
5. **File artifacts** — `dw_framework.py` (or equivalent), one script per worked model, the instance data with seeds/parameters, and a results CSV holding the convergence log so plots can be regenerated.
6. **Recommendation** — one paragraph: whether DW is worth keeping for this problem (bound gained, time per iteration, pricing cost), and the suggested next step (stabilization, aggregation, branch-and-price, or staying with the compact model).

## Questions to Ask

- What are the natural blocks in your model — machines, plants, vehicles, periods, scenarios — and how many are there?
- Which constraints couple the blocks, and how many such rows are there relative to the model?
- Is the model an LP or a MIP, and do the integer variables live inside the blocks or in the coupling?
- Are the blocks identical copies of each other, or all different?
- What does one block look like in isolation — knapsack, shortest path, small assignment, generic MIP?
- Are the block polyhedra bounded, or do I need extreme-ray handling?
- Do you need a tighter dual bound, a faster LP solve, or a proven integer optimum?
- Have you solved the compact model already — what were z_LP, the MIP gap, and the runtime?
- Which solvers and licenses are available for the master and the pricing problems?
- What gap tolerance and time budget should the column-generation loop respect?

## Related Skills

- **column-generation** — when the focus shifts to the pricing loop itself: stabilization variants in depth, heuristic pricing, convergence management, or branch-and-price to reach proven integer optima.
- **lagrangian-relaxation** — when a subgradient method on the same dualized constraints is the cheaper road to the identical dual bound, or to cross-check a DW bound against an independently computed Lagrangian bound.
- **linear-programming-fundamentals** — when duals, reduced costs, degeneracy, or sensitivity in the restricted master need grounding before the decomposition makes sense.
- **milp-modeling-gurobi** — when the compact model must first be built, debugged, or benchmarked in gurobipy before any reformulation is justified.
