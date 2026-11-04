---
name: cutting-planes-valid-inequalities
description: When the user wants to strengthen a MIP with cutting planes and valid inequalities — deriving cover, clique, MIR, or Gomory cuts, writing separation routines, and adding them as user cuts or lazy constraints via Gurobi callbacks. Also use when the user mentions "valid inequalities," "cutting planes," "separation problem," "user cuts," "cover inequalities," "subtour elimination," or when a formulation needs exponentially many constraints generated on the fly. For callback mechanics beyond cuts, see gurobi-advanced-features; for formulation tightening, see integer-programming-techniques.
---

# Cutting Planes and Valid Inequalities

You are an expert in polyhedral methods for integer programming: deriving valid inequalities, implementing separation routines, and wiring them into a branch-and-cut solver as user cuts or lazy constraints. This skill covers the general-purpose families (Chvátal-Gomory, Gomory fractional/mixed-integer, MIR) and the structure-specific families (cover, clique, subtour elimination, flow cover, (l,S)), plus the engineering of a separation loop in gurobipy. Use the framework below to decide whether cuts are the right lever, pick the family that matches the substructure, implement exact or heuristic separation, and validate that every generated cut is actually valid.

## Initial Assessment

Before deriving or coding any cut, establish the following. Each answer changes the plan.

- **Why is the formulation weak?** Measure the root gap: solve the LP relaxation, compare to the best known integer solution. Cuts attack a weak relaxation. If the gap comes from symmetry or loose big-M constants, fix the formulation first (see integer-programming-techniques) — no cut family repairs a bad model efficiently.
- **Is the constraint family required for correctness or only for strength?** Subtour elimination in the DFJ TSP model is part of the model definition: without it, "optimal" solutions are wrong. That is a *lazy constraint*. A cover cut on a knapsack row only tightens the relaxation: the model is correct without it. That is a *user cut*. This single distinction drives the callback type, the parameters, and the failure modes.
- **What substructure does the model contain?** Knapsack rows (sums of bounded variables against a capacity) suggest cover and lifted cover cuts. Pairwise conflicts between binaries suggest clique cuts. Single mixed rows suggest MIR. Connectivity requirements suggest cut-set inequalities. No recognizable structure suggests letting Gomory/MIR machinery inside the solver do the work.
- **Has the solver's own cut engine been given a chance?** Gurobi separates Gomory, MIR, cover, clique, flow-cover, zero-half, and more by default. Try `Params.Cuts = 2` (aggressive) and read the cut summary in the log before writing custom separation. Custom cuts pay off when you know structure the solver cannot see.
- **Exact or heuristic separation?** Exact separation for covers and cliques is itself NP-hard (a knapsack and a max-weight clique, respectively), but pseudo-polynomial DP or greedy heuristics are standard. Subtour separation is polynomial (min cut). Decide what the time budget per node allows.
- **Problem size and cut volume.** Estimate how many cuts a round can produce. Thousands of dense cuts can slow each LP reoptimization more than the bound improvement is worth.
- **Solver and license.** The callback recipes here use gurobipy (`cbCut`, `cbLazy`). PySCIPOpt and python-mip/CBC offer equivalents; CP-SAT does not expose user cuts.
- **Data integrality.** Cover-cut DP separation and pure Gomory arguments assume integer row data. Scale or round the data, or switch to MIR, when coefficients are fractional.
- **Validation plan.** Every separation bug produces a cut that slices off the optimum, and the solver will not warn you. Keep at least one known feasible (ideally optimal) solution of a small instance and assert that every generated cut is satisfied by it.
- **Reporting needs.** For research output, record bound-versus-round traces and percentage of root gap closed per cut family, not just final runtimes.

## Cut Families and the Separation Problem

Let $X = \{x \in \mathbb{Z}^n_+ : Ax \le b\}$ (or a mixed-integer set) and let $P = \{x \ge 0 : Ax \le b\}$ be its LP relaxation. An inequality $\pi^\top x \le \pi_0$ is **valid** for $X$ if every point of $X$ satisfies it. A **cutting plane** at the fractional point $x^*$ is a valid inequality with $\pi^\top x^* > \pi_0$: it separates $x^*$ from $\mathrm{conv}(X)$. The **separation problem** for a family $\mathcal{F}$ of valid inequalities is: given $x^*$, return a member of $\mathcal{F}$ violated by $x^*$ or certify that none exists. By the ellipsoid-method equivalence of separation and optimization (Grötschel, Lovász & Schrijver 1981, "The ellipsoid method and its consequences in combinatorial optimization"), optimizing over the closure of a family is polynomially equivalent to separating it — which is why NP-hard separation problems (covers, cliques) are attacked heuristically in practice.

The master template for general-purpose cuts is the **Chvátal-Gomory rounding** step: for any multiplier vector $u \ge 0$,

$$
\sum_{j=1}^{n} \lfloor u^\top A_j \rfloor \, x_j \;\le\; \lfloor u^\top b \rfloor
$$

is valid for $X$ (Chvátal 1973, "Edmonds polytopes and a hierarchy of combinatorial problems"). Every family below is either a CG cut for a clever $u$, or its mixed-integer generalization.

### The catalog

| Family | Base structure | Inequality | Separation |
|---|---|---|---|
| Gomory fractional | simplex tableau row, pure IP | $\sum_{j \in N} f_{ij} x_j \ge f_{i0}$ | free from the optimal basis |
| Gomory mixed-integer (GMI) | tableau row, mixed IP | scaled two-slope formula (below) | free from the optimal basis |
| MIR | any single mixed $\le$ row | $\sum_j \alpha_j x_j \le \lfloor b \rfloor + \gamma s$ | closed formula per row; aggregation is the art |
| Cover (+ lifting) | knapsack row $\sum a_j x_j \le b$ | $\sum_{j \in C} x_j \le |C| - 1$ | NP-hard exact; DP pseudo-poly; greedy heuristic |
| Clique | conflict graph on binaries | $\sum_{j \in Q} x_j \le 1$ | NP-hard exact; greedy clique growing |
| Subtour elimination (DFJ) | connectivity / TSP | $x(\delta(S)) \ge 2$ | polynomial: min cut on the support graph |
| Flow cover | fixed-charge flow node | mixed cover on arcs into a node | heuristic, solver-internal |
| (l,S) | uncapacitated lot-sizing | $\sum_{t \in L \setminus S} x_t + \sum_{t \in S} d_{tl} y_t \ge d_{1l}$ | exact in $O(n^2)$ |

Key formulas. The **Gomory fractional cut** comes from a tableau row of an optimal LP basis for a pure integer program: if basic variable $x_{B(i)}$ has fractional value $\bar b_i$ in row $x_{B(i)} + \sum_{j \in N} \bar a_{ij} x_j = \bar b_i$, then with $f_{ij} = \bar a_{ij} - \lfloor \bar a_{ij} \rfloor$ and $f_{i0} = \bar b_i - \lfloor \bar b_i \rfloor$,

$$
\sum_{j \in N} f_{ij}\, x_j \;\ge\; f_{i0}
$$

is valid and cuts off the current LP optimum (Gomory 1958, "Outline of an algorithm for integer solutions to linear programs"). The **GMI cut** strengthens this for mixed problems: with $f_j = f_{ij}$, $f_0 = f_{i0}$,

$$
\sum_{\substack{j \in N_I:\, f_j \le f_0}} \frac{f_j}{f_0} x_j
+ \sum_{\substack{j \in N_I:\, f_j > f_0}} \frac{1 - f_j}{1 - f_0} x_j
+ \sum_{\substack{j \in N_C:\, \bar a_{ij} > 0}} \frac{\bar a_{ij}}{f_0} x_j
- \sum_{\substack{j \in N_C:\, \bar a_{ij} < 0}} \frac{\bar a_{ij}}{1 - f_0} x_j \;\ge\; 1 .
$$

The **MIR inequality** is the single-row engine behind GMI: for the set $\{(x, s) \in \mathbb{Z}^n_+ \times \mathbb{R}_+ : a^\top x \le b + s\}$ with $f = b - \lfloor b \rfloor > 0$ and $f_j = a_j - \lfloor a_j \rfloor$,

$$
\sum_j \Big( \lfloor a_j \rfloor + \frac{\max(f_j - f,\, 0)}{1 - f} \Big) x_j \;\le\; \lfloor b \rfloor + \frac{s}{1-f} .
$$

Marchand & Wolsey (2001, "Aggregation and mixed integer rounding to solve MIPs") showed that aggregating rows and applying MIR reproduces most cut families solvers use; GMI is exactly MIR applied to a tableau row.

### User cuts versus lazy constraints

| | User cuts | Lazy constraints |
|---|---|---|
| Purpose | tighten the relaxation; model is already correct | complete the model; required for correctness |
| Typical trigger | fractional node relaxation | candidate integer solution |
| Callback `where` | `GRB.Callback.MIPNODE` + `cbGetNodeRel` | `GRB.Callback.MIPSOL` + `cbGetSolution` (optionally also MIPNODE) |
| Gurobi call | `model.cbCut(...)` | `model.cbLazy(...)` |
| Required parameter | `Params.PreCrush = 1` | `Params.LazyConstraints = 1` |
| Solver may ignore them | yes — they are advice | no — every incumbent is re-checked against them |
| If separation is incomplete | bound is weaker, answer still right | **answer can be wrong** |

### When cuts help — and when they do not

Cuts help when the root gap is large *and* traceable to a known substructure; when the constraint family is exponential so it must be generated on demand (connectivity, subtours, combinatorial Benders); and when the same model family is solved repeatedly, so separation engineering amortizes. Cuts do not help when the gap comes from symmetry or weak big-M (reformulate instead), when the LP is already the bottleneck and extra dense rows make every reoptimization slower, or when instances are small enough that branching alone finishes in seconds. Measure with one number: **percentage of root gap closed**, $(z_{\text{cut}} - z_{\text{LP}}) / (z_{\text{IP}} - z_{\text{LP}})$, and watch for tailing off — the typical pattern is strong improvement for a few rounds, then stalling (branching beats round twelve of cutting; this is why branch-and-cut won over pure cutting planes, Padberg & Rinaldi 1991, "A branch-and-cut algorithm for the resolution of large-scale symmetric traveling salesman problems").

## Cutting-Plane Framework and General-Purpose Cuts

The reusable artifact is a root-node separation loop: solve the LP relaxation, call a list of separation routines on the fractional point, add the violated cuts, repeat until no violation or tailing off. The same loop runs inside a solver via callbacks; building it standalone first makes separation routines testable in isolation.

```text
ROOT CUTTING-PLANE LOOP
-----------------------
input: MIP model M, separation routines S1..Sk
1. R <- LP relaxation of M
2. repeat up to max_rounds:
3.     solve R; record bound; x* <- optimal point
4.     cuts <- union of Si(x*) for all i, keep violation > eps
5.     if no cuts: stop                      # x* is in all known closures
6.     sort by violation, keep the top K     # cut management
7.     add chosen cuts to R and to M         # M goes to branch-and-cut after
8. return strengthened M, bound trace
```

```python
"""Reusable root cutting-plane loop: solve the LP relaxation, separate, add, repeat."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

import gurobipy as gp
from gurobipy import GRB

# A cut is (coefficients keyed by variable name, sense "<=" or ">=", rhs).
Cut = tuple[dict[str, float], str, float]
Separator = Callable[[dict[str, float]], list[Cut]]


@dataclass
class CutLoopReport:
    """Round-by-round trace of the root cutting-plane loop."""

    bounds: list[float] = field(default_factory=list)
    cuts_per_round: list[int] = field(default_factory=list)

    @property
    def total_cuts(self) -> int:
        return sum(self.cuts_per_round)


def _violation(cut: Cut, point: dict[str, float]) -> float:
    """Amount by which `point` violates `cut` (positive means violated)."""
    coeffs, sense, rhs = cut
    lhs = sum(c * point[name] for name, c in coeffs.items())
    return lhs - rhs if sense == "<=" else rhs - lhs


def root_cutting_plane_loop(
    model: gp.Model,
    separators: list[Separator],
    max_rounds: int = 50,
    min_violation: float = 1e-6,
    max_cuts_per_round: int = 100,
) -> CutLoopReport:
    """Tighten the LP relaxation of a MIP by iterated separation.

    Every accepted cut is added to the working relaxation and to the original
    MIP (named gcut_*), so the strengthened model can then go to the MIP solve.
    """
    report = CutLoopReport()
    model.update()
    relax = model.relax()
    relax.Params.OutputFlag = 0
    cut_id = 0
    for _ in range(max_rounds):
        relax.optimize()
        if relax.Status != GRB.OPTIMAL:
            break
        report.bounds.append(relax.ObjVal)
        point = {v.VarName: v.X for v in relax.getVars()}
        violated = [
            cut
            for sep in separators
            for cut in sep(point)
            if _violation(cut, point) > min_violation
        ]
        if not violated:
            break
        violated.sort(key=lambda cut: -_violation(cut, point))
        for coeffs, sense, rhs in violated[:max_cuts_per_round]:
            for target in (relax, model):
                expr = gp.quicksum(
                    c * target.getVarByName(name) for name, c in coeffs.items()
                )
                constr = expr <= rhs if sense == "<=" else expr >= rhs
                target.addConstr(constr, name=f"gcut_{cut_id}")
            cut_id += 1
        report.cuts_per_round.append(min(len(violated), max_cuts_per_round))
        relax.update()
        model.update()
    return report


# Tiny instance: max 4a + 3b s.t. 2a + 2b <= 3, a, b binary.
# LP optimum (1, 0.5) with value 5.5; the cover cut a + b <= 1 closes the gap.
def _cover_separator(point: dict[str, float]) -> list[Cut]:
    """Hand-written separator for the single cover inequality a + b <= 1."""
    if point["a"] + point["b"] > 1.0 + 1e-6:
        return [({"a": 1.0, "b": 1.0}, "<=", 1.0)]
    return []


demo = gp.Model("demo")
demo.Params.OutputFlag = 0
a = demo.addVar(vtype=GRB.BINARY, name="a")
b = demo.addVar(vtype=GRB.BINARY, name="b")
demo.addConstr(2 * a + 2 * b <= 3, name="capacity")
demo.setObjective(4 * a + 3 * b, GRB.MAXIMIZE)
trace = root_cutting_plane_loop(demo, [_cover_separator])
print(trace.bounds, trace.total_cuts)
# Expected: bounds [5.5, 4.0] and 1 cut -- one cover cut moves the root
# bound from 5.5 to the integer optimum 4.0 before any branching.
```

### MIR as a callable formula

MIR needs no search: given a $\le$ row over nonnegative integer variables with a continuous slack, the cut is a closed-form rounding. The craft is in *which* row you feed it — aggregated rows, rows with complemented variables, and rows divided by a chosen coefficient all produce different MIR cuts.

```python
"""Mixed-integer rounding (MIR) cut for a single <= row with a continuous slack."""
import math

import numpy as np


def mir_cut(a: np.ndarray, b: float) -> tuple[np.ndarray, float, float] | None:
    """MIR inequality for X = {x in Z^n_+, s in R_+ : a @ x <= b + s}.

    Returns (alpha, beta, gamma) encoding alpha @ x <= beta + gamma * s, with
    alpha_j = floor(a_j) + max(f_j - f, 0) / (1 - f), beta = floor(b),
    gamma = 1 / (1 - f), where f = b - floor(b) and f_j = a_j - floor(a_j).
    Returns None when b is integral (the MIR inequality reduces to the base row).
    """
    f = b - math.floor(b)
    if f < 1e-9 or f > 1 - 1e-9:
        return None
    f_j = a - np.floor(a)
    alpha = np.floor(a) + np.maximum(f_j - f, 0.0) / (1.0 - f)
    return alpha, float(math.floor(b)), 1.0 / (1.0 - f)


# Tiny instance: the set {x integer >= 0, s >= 0 : x <= 2.5 + s}.
alpha, beta, gamma = mir_cut(np.array([1.0]), 2.5)
print(alpha, beta, gamma)
# Expected: alpha=[1.], beta=2.0, gamma=2.0 -- the MIR cut x <= 2 + 2s.
# It cuts off (x, s) = (2.5, 0) while keeping every mixed-integer point:
# at s = 0 it forces x <= 2, and at s = 0.5 the original bound returns.
```

### Gomory fractional cuts from the optimal basis

The implementation below recovers the optimal simplex tableau ($B^{-1}[A \mid I]$ and $B^{-1}b$) from Gurobi's basis statuses and generates one fractional cut per fractional basic row, expressed back in the structural variables by substituting each slack $s_i = b_i - A_i x$. The slack of every original row and of every Gomory cut is integral at integer points, which is what keeps later rounds valid.

```python
"""Gomory fractional cuts recovered from the optimal LP basis (pure integer program)."""
from __future__ import annotations

import numpy as np
import gurobipy as gp
from gurobipy import GRB

TOL = 1e-7


def _frac(values: np.ndarray) -> np.ndarray:
    """Fractional part, snapping entries within TOL of an integer to zero."""
    f = values - np.floor(values)
    f[f < TOL] = 0.0
    f[f > 1.0 - TOL] = 0.0
    return f


def solve_ip_by_gomory(
    c: np.ndarray, A: np.ndarray, b: np.ndarray, max_rounds: int = 100
) -> tuple[np.ndarray, float, int]:
    """Solve max c @ x s.t. A @ x <= b, x >= 0 integer, by Gomory fractional cuts only.

    Requires integer A and b. The slack of every original row and of every
    Gomory cut is integral at integer points, so each fractional basic row
    of the optimal tableau yields a valid cut. Returns (x, objective, n_cuts).
    """
    A_cur = A.astype(float)
    b_cur = b.astype(float)
    n = c.size
    n_cuts = 0
    for _ in range(max_rounds):
        m_rows = A_cur.shape[0]
        lp = gp.Model("gomory-lp")
        lp.Params.OutputFlag = 0
        lp.Params.Method = 0  # primal simplex: we need a basic optimal solution
        x = lp.addMVar(n, lb=0.0, name="x")
        lp.addConstr(A_cur @ x <= b_cur, name="row")
        lp.setObjective(c @ x, GRB.MAXIMIZE)
        lp.optimize()
        if lp.Status != GRB.OPTIMAL:
            raise RuntimeError(f"LP relaxation not optimal (status {lp.Status})")
        x_val = x.X
        if np.all(np.abs(x_val - np.round(x_val)) < 1e-6):
            return np.round(x_val), float(lp.ObjVal), n_cuts
        # Recover the optimal tableau: rows of B^-1 [A | I] and B^-1 b.
        vbasis = np.array(lp.getAttr("VBasis", lp.getVars()))
        cbasis = np.array(lp.getAttr("CBasis", lp.getConstrs()))
        basic = np.concatenate(
            [np.where(vbasis == GRB.BASIC)[0], n + np.where(cbasis == GRB.BASIC)[0]]
        )
        A_ext = np.hstack([A_cur, np.eye(m_rows)])
        basis_matrix = A_ext[:, basic]
        tableau = np.linalg.solve(basis_matrix, A_ext)
        rhs = np.linalg.solve(basis_matrix, b_cur)
        new_rows: list[np.ndarray] = []
        new_rhs: list[float] = []
        for i in range(m_rows):
            f0 = rhs[i] - np.floor(rhs[i])
            if f0 < 1e-6 or f0 > 1.0 - 1e-6:
                continue
            f = _frac(tableau[i])
            # Cut in (x, s) space: f_x @ x + f_s @ s >= f0; substitute s = b - A x.
            alpha = f[:n] - f[n:] @ A_cur
            beta = f0 - float(f[n:] @ b_cur)
            new_rows.append(-alpha)  # store in <= form
            new_rhs.append(-beta)
        if not new_rows:
            raise RuntimeError("fractional optimum but no cut generated (numerics)")
        A_cur = np.vstack([A_cur] + new_rows)
        b_cur = np.concatenate([b_cur, np.array(new_rhs)])
        n_cuts += len(new_rows)
    raise RuntimeError("round limit reached before integrality")


# Tiny instance: max 5x1 + 4x2 s.t. 6x1 + 4x2 <= 24, x1 + 2x2 <= 6, x integer.
c = np.array([5.0, 4.0])
A = np.array([[6.0, 4.0], [1.0, 2.0]])
b = np.array([24.0, 6.0])
x_opt, obj, cuts_used = solve_ip_by_gomory(c, A, b)
print(x_opt, obj, cuts_used)
# Expected: x = [4, 0] with objective 20.0 after 3 Gomory cuts. The LP
# relaxation was 21.0 at (3, 1.5); cuts close the gap with no branching,
# which is Gomory's 1958 finiteness result in action.
```

Pure Gomory loops are finite in theory but numerically fragile in long runs — fractional residues accumulate until "cuts" become invalid (Zanette, Fischetti & Balas 2011, "Lexicography and degeneracy: can a pure cutting plane algorithm work?"). Solvers therefore apply a few Gomory passes and hand over to branching; do the same.

## Worked Example: Knapsack Cover Cuts with Exact Separation and Lifting

Take a knapsack row $\sum_{j \in N} a_j x_j \le b$ with $x$ binary and integer data. A set $C \subseteq N$ is a **cover** if $\sum_{j \in C} a_j > b$: all of $C$ cannot be packed, so

$$
\sum_{j \in C} x_j \;\le\; |C| - 1
$$

is valid. A cover is **minimal** if dropping any item destroys the cover property; only minimal covers can be facet-inducing on the restricted polytope, and lifting extends them toward facets of the full polytope. These cuts powered the first large-scale 0-1 successes (Crowder, Johnson & Padberg 1983, "Solving large-scale zero-one linear programming problems"); modern computational practice is surveyed in Gu, Nemhauser & Savelsbergh (1998, "Lifted cover inequalities for 0-1 integer programs").

**Exact separation.** At the fractional point $x^*$, the most violated cover minimizes $\sum_{j \in C}(1 - x^*_j)$ over covers; a violated cover exists iff

$$
\zeta = \min \Big\{ \sum_j (1 - x^*_j)\, z_j \;:\; \sum_j a_j z_j \ge b + 1,\; z \in \{0,1\}^n \Big\} < 1 .
$$

This is itself a knapsack — NP-hard in general, solved below by a DP over the capped weight in $O(nb)$ time.

**Sequential lifting.** For $j \notin C$, the exact lifting coefficient is $\alpha_j = (|C| - 1) - \max\{\sum_i \alpha_i x_i : \sum_{i} a_i x_i \le b - a_j\}$, maximizing over the variables already in the inequality — again a small knapsack. Lifting order changes the result; descending $x^*_j$ is the standard choice because it strengthens the cut where the LP point puts weight.

```python
"""Exact cover separation for one knapsack row, with sequential lifting."""
from __future__ import annotations

import numpy as np


def separate_cover(
    a: np.ndarray, b: int, x_frac: np.ndarray
) -> tuple[list[int], float] | None:
    """Most violated cover for sum(a_j x_j) <= b at the fractional point x_frac.

    Solves min sum((1 - x*_j) z_j) s.t. sum(a_j z_j) >= b + 1 exactly by a DP
    over capped weight (needs integer a, b; O(n*b) time). Returns the cover as
    a minimal-cover index list plus its violation, or None if none is violated.
    """
    n = int(a.size)
    target = int(b) + 1
    cost = 1.0 - x_frac
    INF = float("inf")
    dp = np.full((n + 1, target + 1), INF)
    dp[0, 0] = 0.0
    take = np.zeros((n + 1, target + 1), dtype=bool)
    prev_w = np.zeros((n + 1, target + 1), dtype=int)
    for j in range(1, n + 1):
        dp[j] = dp[j - 1]
        prev_w[j] = np.arange(target + 1)
        for w in range(target + 1):
            if dp[j - 1, w] == INF:
                continue
            w2 = min(w + int(a[j - 1]), target)
            if dp[j - 1, w] + cost[j - 1] < dp[j, w2]:
                dp[j, w2] = dp[j - 1, w] + cost[j - 1]
                take[j, w2] = True
                prev_w[j, w2] = w
    if dp[n, target] >= 1.0 - 1e-9:
        return None
    cover: list[int] = []
    w = target
    for j in range(n, 0, -1):
        if take[j, w]:
            cover.append(j - 1)
        w = prev_w[j, w]
    # Make the cover minimal; dropping j raises violation by 1 - x*_j >= 0.
    weight = int(a[cover].sum())
    for j in sorted(cover, key=lambda i: x_frac[i]):
        if weight - int(a[j]) >= target:
            cover.remove(j)
            weight -= int(a[j])
    violation = float(x_frac[cover].sum()) - (len(cover) - 1)
    return sorted(cover), violation


def _knapsack_max(profit: np.ndarray, weight: np.ndarray, cap: int) -> int:
    """0-1 knapsack by DP over capacity; returns the max total profit."""
    dp = np.zeros(cap + 1, dtype=int)
    for p, w in zip(profit.astype(int), weight.astype(int)):
        if w <= cap:
            dp[w:] = np.maximum(dp[w:], dp[: cap + 1 - w] + p)
    return int(dp[cap])


def lift_cover(
    cover: list[int], a: np.ndarray, b: int, x_frac: np.ndarray
) -> dict[int, int]:
    """Sequential up-lifting of variables outside a minimal cover.

    For each outside j (in descending x*_j order), the exact lifting
    coefficient is alpha_j = (|C| - 1) - max{current LHS : weight <= b - a_j},
    a small knapsack solved by DP. Returns {index: coefficient} for all
    variables with a nonzero coefficient.
    """
    coeffs = {j: 1 for j in cover}
    rhs = len(cover) - 1
    outside = sorted(
        (j for j in range(int(a.size)) if j not in coeffs),
        key=lambda j: -x_frac[j],
    )
    for j in outside:
        cap = int(b) - int(a[j])
        if cap < 0:  # x_j = 1 is infeasible on its own; any coefficient <= rhs works
            coeffs[j] = rhs
            continue
        items = list(coeffs)
        best = _knapsack_max(
            np.array([coeffs[i] for i in items]),
            np.array([int(a[i]) for i in items]),
            cap,
        )
        if rhs - best > 0:
            coeffs[j] = rhs - best
    return coeffs


# Tiny instance (Wolsey 1998, Integer Programming, ch. 9 flavor):
# 79x1 + 53x2 + 53x3 + 45x4 + 45x5 <= 178, x binary.
a = np.array([79, 53, 53, 45, 45])
b = 178
x_frac = np.array([0.0, 1.0, 1.0, 0.75, 0.5])
cover, violation = separate_cover(a, b, x_frac)
print(cover, round(violation, 4))
print(lift_cover(cover, a, b, x_frac))
# Expected: cover [1, 2, 3, 4] (i.e., x2 + x3 + x4 + x5 <= 3) with violation
# 0.25; lifting then gives x1 the coefficient 1, so the final lifted cover
# inequality is x1 + x2 + x3 + x4 + x5 <= 3.
```

### Cover cuts inside a Gurobi user-cut callback

In the tree, separation runs at `MIPNODE` on the node relaxation. The callback below uses the standard greedy heuristic (items enter in increasing $(1 - x^*_j)/a_j$ order — the LP greedy for the separation knapsack); swap in the exact DP above when the heuristic dries up. `PreCrush = 1` is mandatory so Gurobi can translate cuts onto the presolved model.

```python
"""Cover cuts as Gurobi user cuts on a 0-1 multidimensional knapsack."""
from __future__ import annotations

import numpy as np
import gurobipy as gp
from gurobipy import GRB


def greedy_cover(a: np.ndarray, b: float, x_frac: np.ndarray) -> list[int] | None:
    """Heuristic separation: fill a cover cheapest-violation-first, then minimalize.

    Items enter in increasing (1 - x*_j) / a_j order (the LP-relaxation greedy
    for the exact separation knapsack); integer row data assumed. Returns a
    violated minimal cover or None.
    """
    order = np.argsort((1.0 - x_frac) / a)
    cover: list[int] = []
    weight = 0.0
    for j in order:
        cover.append(int(j))
        weight += float(a[j])
        if weight > b + 0.5:
            break
    else:
        return None  # all items together do not exceed b: no cover exists
    for j in sorted(cover, key=lambda i: x_frac[i]):
        if weight - float(a[j]) > b + 0.5:
            cover.remove(j)
            weight -= float(a[j])
    violation = float(x_frac[cover].sum()) - (len(cover) - 1)
    return sorted(cover) if violation > 1e-6 else None


def cover_cut_callback(model: gp.Model, where: int) -> None:
    """Separate cover cuts on every knapsack row at the root relaxation."""
    if where != GRB.Callback.MIPNODE:
        return
    if model.cbGet(GRB.Callback.MIPNODE_STATUS) != GRB.OPTIMAL:
        return
    if model.cbGet(GRB.Callback.MIPNODE_NODCNT) > 0:
        return  # root only; drop this test to separate throughout the tree
    x_frac = np.array(model.cbGetNodeRel(model._xvars))
    for i in range(model._A.shape[0]):
        cover = greedy_cover(model._A[i], float(model._b[i]), x_frac)
        if cover is not None:
            model.cbCut(
                gp.quicksum(model._xvars[j] for j in cover) <= len(cover) - 1
            )
            model._n_cover_cuts += 1


def solve_mkp_with_cover_cuts(
    profits: np.ndarray, A: np.ndarray, b: np.ndarray
) -> tuple[float, int]:
    """Solve max p @ x, A @ x <= b, x binary, separating our own cover cuts."""
    model = gp.Model("mkp-cover")
    model.Params.OutputFlag = 0
    model.Params.PreCrush = 1  # mandatory for user cuts: map cuts to presolved model
    model.Params.Cuts = 0      # disable Gurobi's own cuts to isolate the effect
    n = profits.size
    x = model.addVars(n, vtype=GRB.BINARY, name="x")
    model.addConstrs(
        (gp.quicksum(float(A[i, j]) * x[j] for j in range(n)) <= float(b[i])
         for i in range(A.shape[0])),
        name="knapsack",
    )
    model.setObjective(
        gp.quicksum(float(profits[j]) * x[j] for j in range(n)), GRB.MAXIMIZE
    )
    model._xvars = [x[j] for j in range(n)]
    model._A, model._b = A, b
    model._n_cover_cuts = 0
    model.optimize(cover_cut_callback)
    if model.Status != GRB.OPTIMAL:
        raise RuntimeError(f"unexpected status {model.Status}")
    return model.ObjVal, model._n_cover_cuts


# Tiny instance: 30 items, 5 knapsack rows, capacities at 35% of row weight.
rng = np.random.default_rng(7)
profits = rng.integers(10, 50, size=30)
A = rng.integers(5, 30, size=(5, 30))
b = (0.35 * A.sum(axis=1)).astype(int)
obj, n_cuts = solve_mkp_with_cover_cuts(profits, A, b)
print(obj, n_cuts)
# Expected: objective 445.0 with about 10 cover cuts separated at the root
# (seed 7; the exact cut count varies slightly across Gurobi versions).
```

## Worked Example: TSP with Lazy Subtour Elimination

The Dantzig-Fulkerson-Johnson formulation of the symmetric TSP on $n$ cities (Dantzig, Fulkerson & Johnson 1954, "Solution of a large-scale traveling-salesman problem") uses one binary $x_e$ per edge:

$$
\min \sum_{e} d_e x_e
\quad \text{s.t.} \quad
x(\delta(i)) = 2 \;\; \forall i, \qquad
x(\delta(S)) \ge 2 \;\; \forall\, \emptyset \ne S \subsetneq V, \qquad
x \in \{0,1\}^E ,
$$

where $\delta(S)$ is the set of edges with exactly one endpoint in $S$. The cut-set form $x(\delta(S)) \ge 2$ is equivalent, under the degree constraints, to the subtour form $\sum_{e \in E(S)} x_e \le |S| - 1$. There are exponentially many such constraints, so they are **lazy**: the model starts with degree constraints only (its LP is the 2-matching relaxation), and every candidate integer solution is checked for connectivity. Integer separation is just connected components, $O(n + |E^+|)$; this beats the compact MTZ formulation by orders of magnitude on nontrivial instances (see traveling-salesman-problem for the comparison and for heuristics).

```python
"""Symmetric TSP, DFJ formulation: lazy subtour-elimination cuts in a callback."""
from __future__ import annotations

import itertools

import numpy as np
import gurobipy as gp
from gurobipy import GRB


def euclidean_instance(n: int, seed: int) -> np.ndarray:
    """Random points in the unit square; returns the symmetric distance matrix."""
    rng = np.random.default_rng(seed)
    pts = rng.random((n, 2))
    diff = pts[:, None, :] - pts[None, :, :]
    return np.sqrt((diff**2).sum(axis=2))


def components(edges: list[tuple[int, int]], n: int) -> list[list[int]]:
    """Connected components of the support graph of the selected edges."""
    adj: list[list[int]] = [[] for _ in range(n)]
    for i, j in edges:
        adj[i].append(j)
        adj[j].append(i)
    seen = [False] * n
    comps: list[list[int]] = []
    for start in range(n):
        if seen[start]:
            continue
        stack, comp = [start], []
        seen[start] = True
        while stack:
            u = stack.pop()
            comp.append(u)
            for v in adj[u]:
                if not seen[v]:
                    seen[v] = True
                    stack.append(v)
        comps.append(comp)
    return comps


def solve_tsp(dist: np.ndarray, time_limit: float = 60.0) -> tuple[list[int], float]:
    """Exact symmetric TSP: degree constraints up front, DFJ cuts added lazily."""
    n = dist.shape[0]
    model = gp.Model("tsp-dfj")
    model.Params.OutputFlag = 0
    model.Params.LazyConstraints = 1  # mandatory whenever a callback calls cbLazy
    model.Params.TimeLimit = time_limit
    x = model.addVars(
        itertools.combinations(range(n), 2), vtype=GRB.BINARY, name="x"
    )
    model.addConstrs(
        (
            gp.quicksum(x[min(i, j), max(i, j)] for j in range(n) if j != i) == 2
            for i in range(n)
        ),
        name="degree",
    )
    model.setObjective(
        gp.quicksum(dist[i, j] * x[i, j] for i, j in x), GRB.MINIMIZE
    )
    model._n_sec = 0

    def subtour_callback(m: gp.Model, where: int) -> None:
        """Reject every integer point whose support graph is disconnected."""
        if where != GRB.Callback.MIPSOL:
            return
        vals = m.cbGetSolution(x)
        chosen = [(i, j) for (i, j), v in vals.items() if v > 0.5]
        comps = components(chosen, n)
        if len(comps) == 1:
            return  # a single Hamiltonian cycle: accept
        for comp in comps:
            m.cbLazy(
                gp.quicksum(
                    x[i, j] for i, j in itertools.combinations(sorted(comp), 2)
                )
                <= len(comp) - 1
            )
            m._n_sec += 1

    model.optimize(subtour_callback)
    if model.SolCount == 0:
        raise RuntimeError(f"no tour found (status {model.Status})")
    chosen = [(i, j) for (i, j), v in x.items() if v.X > 0.5]
    # Independent validation: degree 2 everywhere and a single component.
    degree = [0] * n
    for i, j in chosen:
        degree[i] += 1
        degree[j] += 1
    assert all(d == 2 for d in degree), "degree constraint violated"
    assert len(components(chosen, n)) == 1, "subtour survived the callback"
    adj = {i: [] for i in range(n)}
    for i, j in chosen:
        adj[i].append(j)
        adj[j].append(i)
    tour, prev = [0], -1
    while len(tour) < n:
        nxt = adj[tour[-1]][0] if adj[tour[-1]][0] != prev else adj[tour[-1]][1]
        prev = tour[-1]
        tour.append(nxt)
    length = sum(dist[tour[k], tour[(k + 1) % n]] for k in range(n))
    print(f"SEC added: {model._n_sec}, status: {model.Status}")
    return tour, length


dist = euclidean_instance(n=30, seed=42)
tour, length = solve_tsp(dist)
print(len(tour), round(length, 4))
# Expected: optimal tour over 30 cities with length 4.5698 (seed 42), after
# roughly two dozen lazy subtour cuts (the exact count varies with Gurobi
# version and heuristics; status 2 = OPTIMAL either way).
```

Three implementation rules for lazy constraints. First, the callback must reject **every** violating integer point, including those proposed by Gurobi's heuristics — never assume MIPSOL points come from your own branching. Second, add one cut per component (the complement set gives the same cut-set, so skip it or dedupe). Third, do not read `.X` inside the callback; only `cbGetSolution`/`cbGetNodeRel` are valid there.

## Advanced Techniques

### Fractional subtour separation by minimum cut

Waiting for integer points wastes information: a fractional LP point can already violate $x(\delta(S)) \ge 2$, and separation is polynomial — a global minimum cut on the support graph with capacities $x^*_e$. Any violated $S$ separates node 0 from some node $t$, so $n - 1$ max-flow calls suffice; Padberg & Rinaldi (1990, "An efficient algorithm for the minimum capacity cut problem") add shrinking to make this fast at scale. Add the resulting sets at `MIPNODE` via `cbCut` (they are user cuts there — the lazy MIPSOL check still guarantees correctness).

```python
"""Fractional subtour separation: min cuts on the LP support graph (no solver needed)."""
from __future__ import annotations

import numpy as np


def max_flow_min_cut(cap: np.ndarray, s: int, t: int) -> tuple[float, np.ndarray]:
    """Edmonds-Karp max flow on a dense capacity matrix.

    Returns (flow value, boolean mask of the source side of a min s-t cut).
    O(V * E^2) worst case; fine for LP support graphs, which are sparse.
    """
    n = cap.shape[0]
    residual = cap.astype(float).copy()
    flow = 0.0
    while True:
        parent = np.full(n, -1)
        parent[s] = s
        queue = [s]
        while queue and parent[t] == -1:
            u = queue.pop(0)
            for v in np.where(residual[u] > 1e-9)[0]:
                if parent[v] == -1:
                    parent[v] = u
                    queue.append(int(v))
        if parent[t] == -1:
            break
        bottleneck = float("inf")
        v = t
        while v != s:
            u = int(parent[v])
            bottleneck = min(bottleneck, residual[u, v])
            v = u
        v = t
        while v != s:
            u = int(parent[v])
            residual[u, v] -= bottleneck
            residual[v, u] += bottleneck
            v = u
        flow += bottleneck
    side = np.zeros(n, dtype=bool)
    side[s] = True
    stack = [s]
    while stack:
        u = stack.pop()
        for v in np.where((residual[u] > 1e-9) & ~side)[0]:
            side[v] = True
            stack.append(int(v))
    return flow, side


def violated_subtour_sets(
    x_frac: dict[tuple[int, int], float], n: int, tol: float = 1e-6
) -> list[set[int]]:
    """All distinct sets S with x*(delta(S)) < 2 - tol, via n-1 max-flow calls.

    Exact separation for the DFJ cut-set inequalities x(delta(S)) >= 2: any
    violated S separates node 0 from some t, so min cuts (0 -> t) for every
    t suffice (Padberg & Rinaldi 1990 refine this with graph shrinking).
    """
    cap = np.zeros((n, n))
    for (i, j), v in x_frac.items():
        if v > tol:
            cap[i, j] = cap[j, i] = v
    found: list[set[int]] = []
    seen: set[frozenset[int]] = set()
    for t in range(1, n):
        flow, side = max_flow_min_cut(cap, 0, t)
        if flow < 2.0 - tol:
            s_set = frozenset(int(v) for v in np.where(side)[0])
            small = (
                s_set
                if len(s_set) <= n - len(s_set)
                else frozenset(range(n)) - s_set
            )
            if 2 <= len(small) <= n - 2 and small not in seen:
                seen.add(small)
                found.append(set(small))
    return found


# Tiny instance: 6 nodes, the LP point puts two disjoint triangles at value 1.
# Degree constraints hold (every node has incident weight 2), but the point
# is far outside the TSP polytope.
x_lp = {
    (0, 1): 1.0, (1, 2): 1.0, (0, 2): 1.0,
    (3, 4): 1.0, (4, 5): 1.0, (3, 5): 1.0,
}
print(violated_subtour_sets(x_lp, n=6))
# Expected: [{0, 1, 2}] -- one violated set (its complement gives the same
# cut), yielding the user cut x(delta({0,1,2})) >= 2.
```

### Clique cuts from conflict graphs

When the model implies pairwise conflicts $x_i + x_j \le 1$ (from set-packing rows, from probing on big-M rows, or from one-machine overlap), any clique $Q$ in the conflict graph gives $\sum_{j \in Q} x_j \le 1$ — strictly dominating the edge inequalities it merges. Exact separation is max-weight clique (NP-hard); the greedy below grows a clique in descending-$x^*$ order, which is the standard cheap heuristic.

```python
"""Clique cut separation on a conflict graph by greedy weighted clique growing."""
from __future__ import annotations

import numpy as np


def separate_clique(
    conflicts: np.ndarray, x_frac: np.ndarray, tol: float = 1e-6
) -> list[int] | None:
    """Grow a clique greedily in descending-x* order; report it if violated.

    conflicts[i, j] = True means x_i + x_j <= 1 is implied by the model.
    Returns a clique Q with sum(x*[Q]) > 1 + tol -- the violated clique cut
    sum_{j in Q} x_j <= 1 -- or None. Exact separation is NP-hard.
    """
    order = np.argsort(-x_frac, kind="stable")
    clique: list[int] = []
    for v in order:
        if x_frac[v] <= tol:
            break
        if all(conflicts[v, u] for u in clique):
            clique.append(int(v))
    weight = float(x_frac[clique].sum())
    return clique if weight > 1.0 + tol else None


# Tiny instance: conflicts (0,1), (0,2), (1,2), (2,3); x* = (.5, .5, .5, .3, 0).
n = 5
conflicts = np.zeros((n, n), dtype=bool)
for i, j in [(0, 1), (0, 2), (1, 2), (2, 3)]:
    conflicts[i, j] = conflicts[j, i] = True
x_frac = np.array([0.5, 0.5, 0.5, 0.3, 0.0])
print(separate_clique(conflicts, x_frac))
# Expected: [0, 1, 2] -- every pair sums to exactly 1.0, so the point obeys
# all edge inequalities, yet the triangle has weight 1.5 > 1: the clique cut
# x0 + x1 + x2 <= 1 is violated by 0.5.
```

### (l,S) inequalities for lot-sizing

For uncapacitated lot-sizing with production $x_t$, setup $y_t$, demand $d_t$, and $d_{tl} = \sum_{u=t}^{l} d_u$: for every $l$ and every $S \subseteq L = \{1, \dots, l\}$,

$$
\sum_{t \in L \setminus S} x_t \;+\; \sum_{t \in S} d_{tl}\, y_t \;\ge\; d_{1l} .
$$

Demand through $l$ is met either by production in periods outside $S$ or by periods in $S$, each capped at $d_{tl}$ once its setup is paid. Separation is exact and $O(n^2)$: for each $l$, put $t$ into $S$ exactly when $d_{tl} y^*_t < x^*_t$. Adding the full family describes the convex hull (Barany, Van Roy & Wolsey 1984, "Uncapacitated lot-sizing: the convex hull of solutions") — one of the rare cases where a cut family finishes the job alone. See lot-sizing for the model context and the capacitated extensions.

### Cut management: rounds, pools, and purging

Adding every violated cut is a beginner mistake. Practical rules: cap cuts per round (10-100) and keep the most violated, breaking near-parallel ties (skip a cut whose coefficient vector has cosine similarity above ~0.95 with an accepted one); limit cut density — a cut touching half the variables slows every later LP; purge cuts whose slack has stayed large for many consecutive LP solves (solvers move them to a pool and re-add on violation); stop the root loop when a round improves the bound by less than ~0.01% — tailing off is structural, not a tuning failure. Inside Gurobi, the equivalents are `Params.Cuts` plus per-family knobs (`CoverCuts`, `CliqueCuts`, `MIRCuts`, `GomoryPasses`) and `CutPasses` for root rounds; see gurobi-advanced-features.

### Numerical safety for generated cuts

Reject cuts with coefficient dynamic range above ~$10^6$, violation below $10^{-6}$, or coefficients below $10^{-9}$ (zero them and re-check validity). Snap near-integer values before computing fractional parts, as `_frac` above does. After deep rounds of tableau-based cuts, re-derive from the original rows rather than from cut-on-cut tableaus. Cornuéjols (2008, "Valid inequalities for mixed integer linear programs") surveys the theory; the engineering rule is simpler — every cut you generate should pass an assertion against a stored feasible solution before it enters the model.

## Practical Challenges

**The solver errors out or silently ignores your cuts because parameters are missing.** `cbLazy` requires `Params.LazyConstraints = 1` and `cbCut` requires `Params.PreCrush = 1` — set them at model build time, not in the callback. Without `PreCrush`, Gurobi cannot map your cut onto the presolved model and may reject it; without `LazyConstraints`, dual presolve reductions can make lazily-added constraints incorrect, so Gurobi refuses the call.

**Wrong "optimal" solutions with lazy constraints.** The callback must check every MIPSOL point — including incumbents found by internal heuristics — and must cover the *complete* family: if some violated subtour can slip through (e.g., you only check components containing node 0), the run terminates with an infeasible "optimum". Validate the final solution with an independent checker, as the TSP example does, on every run.

**A separation bug cuts off the true optimum.** This is the worst failure because the solver gives no signal. Defense: on a small instance, enumerate the optimum by brute force, then assert every generated cut is satisfied by it. Run this test for each new cut family before trusting any benchmark numbers.

**Cuts are added but the bound barely moves.** Common causes: the cuts duplicate what presolve/solver cuts already imply (compare against `Params.Cuts = 0` to measure your real contribution); the violated inequalities are weak members of the family (lift covers before adding them); or the gap source is elsewhere — recheck root-gap attribution before investing in more separation.

**The LP gets slower each round until the loop crawls.** Cut accumulation. Cap cuts per round, prefer sparse and strongly violated cuts, purge rows with persistent slack, and stop at tailing-off. If the root LP is degenerate, many Gomory rounds also produce near-parallel cuts — switch families instead of adding passes.

**Callback reads crash or return stale values.** Inside a callback only `cbGet*` accessors are valid: `cbGetNodeRel` at MIPNODE (and only when `MIPNODE_STATUS == GRB.OPTIMAL`), `cbGetSolution` at MIPSOL. Reading `var.X`, `model.ObjVal`, or modifying the model directly inside a callback is undefined behavior in gurobipy.

**Exact separation is too slow per node.** Time-box it: exact DP/min-cut at the root, cheap greedy in the tree, and skip separation entirely below a depth or above a node-count threshold. A cut family that closes 90% of the root gap usually earns its keep in the first few rounds; deeper in the tree, branching is cheaper than separation.

## Tools & Libraries

| Library | When to use | Note |
|---|---|---|
| gurobipy | default for branch-and-cut with custom cuts | `cbCut`/`cbLazy` callbacks; `PreCrush`, `LazyConstraints`; per-family cut parameters |
| PySCIPOpt | research on separation itself | full separator plugins (`Sepa`), priorities, and access to SCIP's cut selection |
| python-mip (CBC) | license-free lazy/user cuts | `ConstrsGenerator` interface for both cut types; slower LPs than Gurobi |
| HiGHS (highspy) | license-free MIP without custom cuts | no user-cut/lazy callbacks as of 1.x; rely on internal separators |
| OR-Tools CP-SAT | when the model fits CP | no user cuts — encode structure in constraints instead |
| networkx | quick separation prototypes | `minimum_cut`, `gomory_hu_tree` for cut-set separation before hand-rolling max-flow |
| numpy | DP separation, tableau algebra | basis recovery and vectorized knapsack DPs as in the blocks above |

## Output Format

A complete cutting-plane deliverable contains:

1. **Model statement** — the base formulation, plus each cut family used: the inequality, its validity argument (one paragraph or a citation), and whether it enters as a user cut or a lazy constraint.
2. **Separation summary** — per family: exact or heuristic, complexity, where it runs (root loop, MIPNODE, MIPSOL).
3. **Cut impact table** — the experiment that justifies the machinery:

| Configuration | Root bound | Root gap closed | Nodes | Time (s) |
|---|---|---|---|---|
| LP relaxation | 21.00 | — | — | 0.01 |
| + solver default cuts | 20.45 | 55% | 38 | 0.4 |
| + custom cover cuts | 20.10 | 90% | 9 | 0.3 |

   Report root gap closed as $(z_{\text{cut}} - z_{\text{LP}})/(z_{\text{IP}} - z_{\text{LP}})$, nodes to optimality, and wall time, each against the no-custom-cuts baseline (same seeds, same time limits).
4. **Code artifacts** — separation routines as pure functions taking a fractional point and returning cuts (testable without a solver), the callback wiring, and the parameter settings (`PreCrush`, `LazyConstraints`, `Cuts`) stated explicitly.
5. **Validation evidence** — the assertion harness: every generated cut checked against a known feasible/optimal solution on small instances, and an independent feasibility check of the final solution (degree/connectivity for TSP, capacity for knapsack).
6. **Reproducibility block** — instance generator seeds, solver version, and per-run logs of cuts added per family per round.

## Questions to Ask

- Is the candidate constraint family required for correctness (lazy) or only for bound strength (user cuts)?
- What is the root gap now, and what does the Gurobi cut log already separate on this model?
- Which substructures exist — knapsack rows, pairwise conflicts, connectivity, fixed-charge arcs, lot-sizing rows?
- Are the row data integral, or do covers/Gomory arguments need scaling or an MIR route?
- What time budget per node is acceptable for separation, and is exact separation affordable at the root?
- Is there a known optimal or feasible solution on small instances to assert cut validity against?
- Will the cuts be benchmarked properly — same seeds, baseline with `Cuts=0`, baseline with default cuts?
- Does the user need a one-off solve (lean on solver internals) or a reusable branch-and-cut code (invest in separation)?
- Are there exponentially many constraints in the intended formulation that must be generated on the fly?

## Related Skills

- **integer-programming-techniques** — when the gap comes from weak big-M, symmetry, or formulation choice rather than missing inequalities; cuts complement, not replace, a tight model.
- **gurobi-advanced-features** — when callback mechanics beyond cuts are needed: heuristic solution injection, termination control, IIS, solution pools, and parameter tuning.
- **traveling-salesman-problem** — when the actual goal is solving TSPs: formulation comparison (MTZ vs DFJ), construction heuristics, and local search around the exact core shown here.
- **milp-modeling-gurobi** — when the base MIP itself still needs building: variables, constraint-builder functions, objectives, and status handling that this skill assumes.
- **lot-sizing** — when applying (l,S) inequalities and their capacitated relatives in production planning models.
