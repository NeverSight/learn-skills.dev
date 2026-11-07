---
name: linearization-techniques
description: When the user wants to turn nonlinear terms — variable products, absolute values, min/max, piecewise-linear functions, logical implications, or fractional objectives — into mixed-integer linear constraints, or needs tight big-M values. Also use when the user mentions "linearize," "big-M," "bilinear," "piecewise linear," "indicator constraint," "product of variables," or "McCormick," or when a quadratic model must run on a MILP solver. For overall MILP construction, see milp-modeling-gurobi; for formulation strength and cuts, see integer-programming-techniques.
---

# Linearization Techniques

You are an expert in reformulating nonlinear and logical model constructs as mixed-integer
linear programs. This skill covers exact linearization of variable products, absolute values,
min/max terms, piecewise-linear functions, logical implications, and fractional objectives,
plus the discipline of choosing tight big-M constants. Use the framework below to classify
each nonlinear term, pick the sharpest valid reformulation, and verify the result.

## Initial Assessment

Establish these facts before proposing any reformulation:

- **Inventory the nonlinear terms.** List every product, absolute value, min/max, ratio,
  piecewise function, and if-then condition. The right technique differs per term type.
- **Variable domains in each product.** Binary times binary and binary times continuous have
  exact linearizations. Continuous times continuous does not — only relaxations (McCormick)
  or piecewise approximations. Confirm which case you are in before promising exactness.
- **Finite bounds.** Almost every technique here needs finite lower/upper bounds on the
  continuous variables involved. Ask where bounds come from: physical limits, capacity data,
  or bound-propagation. If a variable is genuinely unbounded, fix that first.
- **Convex use or nonconvex use.** A term like |w| or max(w1, w2) needs no binaries when the
  optimization direction already pushes it the right way (epigraph use). It needs binaries
  when used in the opposite direction. Identify the direction before adding integer variables.
- **Where the term sits.** Objective-only nonlinearity sometimes allows lighter treatment
  (epigraph, Dinkelbach) than nonlinearity inside constraints.
- **Solver and license.** Gurobi, CPLEX, and SCIP accept indicator constraints, SOS sets, and
  native PWL/general constraints; a pure-LP or open-source pipeline may force manual big-M.
  Gurobi can also solve bilinear models directly with `Params.NonConvex = 2` — sometimes the
  honest answer is "do not hand-linearize."
- **Problem size after reformulation.** Linearizing all products in a quadratic model with n²
  binaries creates O(n⁴) variables. Estimate the blow-up; pick a compact scheme (e.g.
  Kaufman–Broeckx) if the full one will not fit in memory.
- **Accuracy requirement.** Piecewise-linear approximation of a smooth function trades
  breakpoint count against error. Get a tolerance before choosing the grid.
- **Numerical scale.** Note the ratio between the largest and smallest constraint
  coefficients you are about to create. Big-M values that push this ratio past ~1e6 will
  cause solver trouble; plan bound tightening up front.

## Linearization Catalog

Quick reference. "Exact" means the reformulation describes the same feasible set; "relaxation"
means it only over-approximates it.

| Nonlinear term | Reformulation | Extra vars / constrs | Exact? |
|---|---|---|---|
| z = x·y, x,y binary | Fortet inequalities | 1 cont. / 3 | exact, hull-sharp |
| z = x·w, x binary, w ∈ [L,U] | 4-inequality envelope | 1 cont. / 4 | exact, hull-sharp |
| z = v·w, both continuous | McCormick envelope | 1 cont. / 4 | relaxation only |
| t = \|w\|, convex use | epigraph t ≥ ±w | 1 cont. / 2 | exact in epigraph use |
| t = \|w\|, nonconvex use | sign split + 1 binary | 3 / 4 | exact |
| t = max(w₁..w_m), convex use | t ≥ w_i | 1 cont. / m | exact in epigraph use |
| t = max(w₁..w_m), nonconvex use | selector binaries | m bin. / 2m+1 | exact |
| x=1 ⟹ a·w ≤ b | big-M or indicator | 0 / 1 | exact given valid M |
| piecewise-linear f(w) | SOS2 / incremental / multiple choice | see PWL table | exact on breakpoints |
| max (c·x+α)/(d·x+β), LP | Charnes–Cooper scaling | 1 cont. / 1 | exact |
| max (p·x+p₀)/(q·x+q₀), MIP | Dinkelbach iterations | none (sequence of MIPs) | exact at convergence |

### Products of variables

**Binary × binary.** For x, y ∈ {0,1}, z = xy is enforced by

$$z \le x,\qquad z \le y,\qquad z \ge x + y - 1,\qquad z \ge 0.$$

z may stay continuous; integrality of x, y forces it. These inequalities describe the convex
hull of the five feasible points, so nothing tighter exists (Fortet 1960; Glover & Woolsey
1974, converting 0-1 polynomial programs to 0-1 linear programs). For a product of three or
more binaries, chain pairwise or use the single-z generalization z ≥ Σx_i − (k−1), z ≤ x_i.

**Binary × continuous.** For x ∈ {0,1}, w ∈ [L, U], z = xw is enforced by

$$z \le Ux,\qquad z \ge Lx,\qquad z \le w - L(1-x),\qquad z \ge w - U(1-x).$$

Also hull-sharp (Glover 1975, improved linear integer formulations of nonlinear integer
problems). Tight bounds L, U matter: they are the big-Ms of this reformulation.

**Continuous × continuous.** For v ∈ [Lv, Uv], w ∈ [Lw, Uw], the McCormick envelope
(McCormick 1976, computability of global solutions to factorable nonconvex programs)

$$z \ge L_v w + L_w v - L_v L_w,\quad z \ge U_v w + U_w v - U_v U_w,$$
$$z \le U_v w + L_w v - U_v L_w,\quad z \le L_v w + U_w v - L_v U_w$$

is only a relaxation. Exactness requires spatial branching (let the solver do it via
`NonConvex = 2`) or piecewise McCormick (see Advanced Techniques).

### Absolute value, minimum, maximum

For t = |w|, w ∈ [L, U] with L < 0 < U: in epigraph use (minimizing t, or t on the small
side of ≤ constraints), t ≥ w and t ≥ −w suffice. Otherwise split w = w⁺ − w⁻ with
w⁺ ≤ U·b, w⁻ ≤ −L·(1−b), b binary, and set t = w⁺ + w⁻. The binary forbids simultaneous
positive parts, which is what the epigraph version cannot do.

For t = max_i w_i: epigraph use needs only t ≥ w_i. Exact encoding adds selector binaries:

$$t \ge w_i \;\forall i,\qquad t \le w_i + \big(\max_j U_j - L_i\big)(1 - b_i)\;\forall i,\qquad \sum_i b_i = 1.$$

min(·) is symmetric (flip signs). The coefficient max_j U_j − L_i is again a big-M built from
bounds — tighten the bounds and the formulation tightens with them.

### Logical implications

x = 1 ⟹ a·w ≤ b becomes a·w ≤ b + M(1 − x) with M ≥ max{a·w} − b over the feasible region.
The reverse direction a·w < b ⟹ x = 1 is modeled through the contrapositive
x = 0 ⟹ a·w ≥ b; a strict inequality needs an explicit tolerance ε on one side, chosen
larger than the solver's feasibility tolerance. Indicator constraints
(`addGenConstrIndicator`) express the same implication without any M; the solver converts
internally, often deriving better constants than a careless user would. Disjunctions
(w ∈ P₁ ∨ w ∈ P₂) admit either big-M per disjunct or the tighter but larger convex-hull
extended formulation (Balas 1998, disjunctive programming).

### Piecewise-linear functions

Given breakpoints (x₀,y₀),…,(x_K,y_K), the main exact MILP encodings:

| Method | Binaries | Idea | Use when |
|---|---|---|---|
| Convex epigraph | 0 | t ≥ slope_k·w + intercept_k | f convex and minimized (or concave and maximized) |
| Lambda + SOS2 | 0 (SOS2 set) | convex combination of breakpoints | solver branches well on SOS; no bound on K |
| Incremental (delta) | K−1 | fill segments left to right | sequential/filling structure; couples well with fixed charges |
| Multiple choice | K | one binary per segment, disaggregated w | strong LP relaxation wanted; locally ideal |
| Logarithmic | ⌈log₂K⌉ | Gray-code branching on segments | many breakpoints (K ≳ 16) |

Croxton, Gendron & Magnanti (2003) show the LP relaxations of the standard exact encodings
coincide with the lower convex envelope; Vielma, Ahmed & Nemhauser (2010) compare them
computationally — multiple choice and logarithmic usually win on hard instances.

### Fractional objectives

Maximizing (c·x + α)/(d·x + β) over a polyhedron with positive denominator: Charnes & Cooper
(1962) substitute t = 1/(d·x + β), y = tx, giving the LP max c·y + αt subject to
Ay − bt ≤ 0, d·y + βt = 1, y, t ≥ 0; recover x = y/t. With integer variables the
substitution breaks (y = tx is bilinear), so use Dinkelbach (1967): repeatedly solve the
parametric problem max p·x + p₀ − λ(q·x + q₀) and update λ to the incumbent ratio; the root
of F(λ) is the optimal ratio, and convergence is superlinear. A third option for 0-1
fractional programs: multiply out and linearize the binary-times-continuous products with
the Glover envelope above.

### Choosing tight big-M values

Rules that prevent most big-M damage:

1. **Derive every M from bounds, never invent one.** M = (interval-arithmetic max of LHS) −
   RHS is the smallest generally valid constant. Camm, Raturi & Tsubakitani (1990), "cutting
   big M down to size," is the classic statement.
2. **One M per constraint, not one global M.** Per-row constants are almost always smaller.
3. **Spend an LP to save a tree.** When interval arithmetic is loose, solve the auxiliary
   bounding LP max{a·w : relaxed constraints} for a valid and tighter M.
4. **Watch IntFeasTol × M.** A binary may sit at 1e-5 in an "integral" solution; with
   M = 1e7 that admits a phantom slack of 100 ("trickle flow"). Keep M ≤ ~1e6·tolerance
   headroom, or use indicators.
5. **Big-M caps the LP bound.** The LP relaxation can pay a fraction x = b/(b+M·…) to switch
   constraints off cheaply; the bigger the M, the weaker the root bound.

## Reusable Linearization Toolkit

The generic procedure, then implementation-grade gurobipy helpers for each catalog family.

```text
LINEARIZE(model):
  1. Inventory nonlinear terms: products, |.|, min/max, PWL, implications, ratios.
  2. For each term:
     a. Establish finite bounds [L, U] on every continuous variable involved
        (bound propagation; auxiliary bounding LPs when propagation is loose).
     b. Classify the use direction: convex/epigraph use (no binaries needed)
        versus nonconvex use (exact encoding with binaries or SOS).
     c. Pick the reformulation from the catalog; prefer hull-sharp encodings.
     d. Add auxiliary variables and named constraints; record every M together
        with the bound derivation that produced it.
  3. Re-run bound tightening; shrink each recorded M whose bounds improved.
  4. Validate: re-evaluate the original nonlinear expressions at the MILP
     optimum; any mismatch beyond tolerance means a wrong bound or missed case.
```

### Products and the big-M helper

```python
import gurobipy as gp
from gurobipy import GRB


def link_binary_product(model: gp.Model, x: gp.Var, y: gp.Var, name: str) -> gp.Var:
    """Return z enforced to equal x*y for binary x, y (Fortet 1960; Glover & Woolsey 1974)."""
    z = model.addVar(lb=0.0, ub=1.0, name=f"z[{name}]")
    model.addConstr(z <= x, name=f"prod_le_x[{name}]")
    model.addConstr(z <= y, name=f"prod_le_y[{name}]")
    model.addConstr(z >= x + y - 1, name=f"prod_ge[{name}]")
    return z


def link_binary_continuous(model: gp.Model, x: gp.Var, w: gp.Var,
                           lb: float, ub: float, name: str) -> gp.Var:
    """Return z enforced to equal x*w for binary x and continuous w in [lb, ub]."""
    z = model.addVar(lb=min(lb, 0.0), ub=max(ub, 0.0), name=f"z[{name}]")
    model.addConstr(z <= ub * x, name=f"bc_ub_x[{name}]")
    model.addConstr(z >= lb * x, name=f"bc_lb_x[{name}]")
    model.addConstr(z <= w - lb * (1 - x), name=f"bc_w_ub[{name}]")
    model.addConstr(z >= w - ub * (1 - x), name=f"bc_w_lb[{name}]")
    return z


def tight_big_m(coeffs: list[float], lbs: list[float], ubs: list[float], rhs: float) -> float:
    """Smallest M valid for 'sum(c_i w_i) <= rhs + M(1-x)' by interval arithmetic on w."""
    worst = sum(c * (u if c > 0 else l) for c, l, u in zip(coeffs, lbs, ubs))
    return max(worst - rhs, 0.0)


# Tiny synthetic check: maximize x*y + x*w, with w <= 3.5.
m = gp.Model("products")
m.Params.OutputFlag = 0
x = m.addVar(vtype=GRB.BINARY, name="x")
y = m.addVar(vtype=GRB.BINARY, name="y")
w = m.addVar(lb=0.0, ub=5.0, name="w")
m.addConstr(w <= 3.5, name="w_cap")
obj = link_binary_product(m, x, y, "xy") + link_binary_continuous(m, x, w, 0.0, 5.0, "xw")
m.setObjective(obj, GRB.MAXIMIZE)
m.optimize()
assert m.Status == GRB.OPTIMAL
print(f"obj={m.ObjVal:.1f} x={int(round(x.X))} y={int(round(y.X))} w={w.X:.1f}")
print(f"M={tight_big_m([2.0, 3.0], [0.0, 0.0], [5.0, 5.0], 4.0):.0f}")
# Expected: obj=4.5 (x=1, y=1, w=3.5); M=21 (= 2*5 + 3*5 - 4)
```

### Absolute value and max in the nonconvex direction

Both demos below would be answered wrongly by the epigraph-only version: maximizing an
epigraph variable lets it float to its upper bound, and `t >= w_i` alone cannot make a
`max(...) >= 3` constraint force any single variable up to 3.

```python
import gurobipy as gp
from gurobipy import GRB


def add_abs(model: gp.Model, w: gp.Var, lb: float, ub: float, name: str) -> gp.Var:
    """Return t enforced to equal |w| exactly (sign split with one binary)."""
    t = model.addVar(lb=0.0, ub=max(abs(lb), abs(ub)), name=f"abs[{name}]")
    if lb >= 0:
        model.addConstr(t == w, name=f"abs_id[{name}]")
        return t
    if ub <= 0:
        model.addConstr(t == -w, name=f"abs_neg[{name}]")
        return t
    wp = model.addVar(lb=0.0, ub=ub, name=f"wpos[{name}]")
    wn = model.addVar(lb=0.0, ub=-lb, name=f"wneg[{name}]")
    b = model.addVar(vtype=GRB.BINARY, name=f"sign[{name}]")  # b = 1  <=>  w >= 0
    model.addConstr(w == wp - wn, name=f"abs_split[{name}]")
    model.addConstr(t == wp + wn, name=f"abs_sum[{name}]")
    model.addConstr(wp <= ub * b, name=f"abs_cmpl_p[{name}]")
    model.addConstr(wn <= -lb * (1 - b), name=f"abs_cmpl_n[{name}]")
    return t


def add_max(model: gp.Model, ws: list[gp.Var], lbs: list[float],
            ubs: list[float], name: str) -> gp.Var:
    """Return t enforced to equal max(ws) exactly (one selector binary per term)."""
    t = model.addVar(lb=max(lbs), ub=max(ubs), name=f"max[{name}]")
    pick = model.addVars(len(ws), vtype=GRB.BINARY, name=f"argmax[{name}]")
    top = max(ubs)
    for i, (w, lb_i) in enumerate(zip(ws, lbs)):
        model.addConstr(t >= w, name=f"max_ge[{name},{i}]")
        model.addConstr(t <= w + (top - lb_i) * (1 - pick[i]), name=f"max_le[{name},{i}]")
    model.addConstr(pick.sum() == 1, name=f"max_pick[{name}]")
    return t


# Check 1: maximize |w| over w in [-1, 2]. Epigraph alone would report t at its bound.
m1 = gp.Model("abs_nonconvex_side")
m1.Params.OutputFlag = 0
w = m1.addVar(lb=-1.0, ub=2.0, name="w")
t = add_abs(m1, w, -1.0, 2.0, "w")
m1.setObjective(t, GRB.MAXIMIZE)
m1.optimize()
assert m1.Status == GRB.OPTIMAL
print(f"max |w| = {m1.ObjVal:.1f} at w = {w.X:.1f}")

# Check 2: minimize w1 + w2 subject to max(w1, w2) >= 3 (nonconvex side of max).
m2 = gp.Model("max_lower_bounded")
m2.Params.OutputFlag = 0
w1 = m2.addVar(lb=0.0, ub=4.0, name="w1")
w2 = m2.addVar(lb=0.0, ub=4.0, name="w2")
tmax = add_max(m2, [w1, w2], [0.0, 0.0], [4.0, 4.0], "w12")
m2.addConstr(tmax >= 3.0, name="peak_req")
m2.setObjective(w1 + w2, GRB.MINIMIZE)
m2.optimize()
assert m2.Status == GRB.OPTIMAL
print(f"min w1+w2 = {m2.ObjVal:.1f}")
# Expected: max |w| = 2.0 at w = 2.0; min w1+w2 = 3.0 (one variable pushed to 3)
```

### Implications: big-M and indicator

```python
import gurobipy as gp
from gurobipy import GRB


def add_implication_big_m(model: gp.Model, x: gp.Var, lhs: gp.LinExpr,
                          lhs_ub: float, rhs: float, name: str) -> float:
    """Enforce x = 1 -> lhs <= rhs with M = lhs_ub - rhs. Returns the M used.

    lhs_ub must be a valid upper bound on lhs over the feasible region
    (compute it by interval arithmetic or an auxiliary bounding LP).
    """
    m_val = max(lhs_ub - rhs, 0.0)
    model.addConstr(lhs <= rhs + m_val * (1 - x), name=f"impl[{name}]")
    return m_val


def add_iff_threshold(model: gp.Model, x: gp.Var, w: gp.Var, lb: float, ub: float,
                      thresh: float, eps: float, name: str) -> None:
    """Enforce x = 1 <=> w >= thresh (with tolerance eps on the strict side)."""
    model.addConstr(w >= thresh - (thresh - lb) * (1 - x), name=f"iff_fwd[{name}]")
    model.addConstr(w <= (thresh - eps) + (ub - thresh + eps) * x, name=f"iff_bwd[{name}]")


# Check: x = 1 -> 2 w1 + 3 w2 <= 4, with a bonus of 5 for setting x = 1.
m = gp.Model("implication")
m.Params.OutputFlag = 0
x = m.addVar(vtype=GRB.BINARY, name="x")
w1 = m.addVar(lb=0.0, ub=5.0, name="w1")
w2 = m.addVar(lb=0.0, ub=5.0, name="w2")
used_m = add_implication_big_m(m, x, 2.0 * w1 + 3.0 * w2, lhs_ub=25.0, rhs=4.0, name="cap")
m.setObjective(w1 + w2 + 5.0 * x, GRB.MAXIMIZE)
m.optimize()
assert m.Status == GRB.OPTIMAL
print(f"big-M: obj={m.ObjVal:.1f} x={int(round(x.X))} M={used_m:.0f}")

# Same implication via Gurobi's indicator constraint (no M at all).
m2 = gp.Model("indicator")
m2.Params.OutputFlag = 0
x2 = m2.addVar(vtype=GRB.BINARY, name="x")
v1 = m2.addVar(lb=0.0, ub=5.0, name="v1")
v2 = m2.addVar(lb=0.0, ub=5.0, name="v2")
m2.addGenConstrIndicator(x2, True, 2.0 * v1 + 3.0 * v2 <= 4.0, name="ind_cap")
m2.setObjective(v1 + v2 + 5.0 * x2, GRB.MAXIMIZE)
m2.optimize()
assert m2.Status == GRB.OPTIMAL
print(f"indicator: obj={m2.ObjVal:.1f}")

# Check the iff: with w capped at 2.5 < 3, x is forced to 0.
m3 = gp.Model("iff")
m3.Params.OutputFlag = 0
x3 = m3.addVar(vtype=GRB.BINARY, name="x")
w3 = m3.addVar(lb=0.0, ub=10.0, name="w")
add_iff_threshold(m3, x3, w3, lb=0.0, ub=10.0, thresh=3.0, eps=1e-4, name="th")
m3.addConstr(w3 <= 2.5, name="w_cap")
m3.setObjective(x3, GRB.MAXIMIZE)
m3.optimize()
assert m3.Status == GRB.OPTIMAL
print(f"iff: x={int(round(x3.X))}")
# Expected: big-M obj=10.0 with x=0 and M=21; indicator obj=10.0; iff x=0
```

### Piecewise-linear functions: lambda/SOS2 and incremental

```python
import gurobipy as gp
from gurobipy import GRB


def add_pwl_lambda(model: gp.Model, x: gp.Var, xs: list[float], ys: list[float],
                   name: str) -> gp.Var:
    """Return y = f(x) for the PWL function through (xs[k], ys[k]): lambda method + SOS2."""
    n = len(xs)
    lam = model.addVars(n, lb=0.0, ub=1.0, name=f"lam[{name}]")
    y = model.addVar(lb=min(ys), ub=max(ys), name=f"pwl[{name}]")
    model.addConstr(lam.sum() == 1.0, name=f"pwl_conv[{name}]")
    model.addConstr(x == gp.quicksum(xs[k] * lam[k] for k in range(n)), name=f"pwl_x[{name}]")
    model.addConstr(y == gp.quicksum(ys[k] * lam[k] for k in range(n)), name=f"pwl_y[{name}]")
    model.addSOS(GRB.SOS_TYPE2, [lam[k] for k in range(n)], list(range(1, n + 1)))
    return y


def add_pwl_delta(model: gp.Model, x: gp.Var, xs: list[float], ys: list[float],
                  name: str) -> gp.Var:
    """Return y = f(x) via the incremental (delta) method with filling-order binaries."""
    nseg = len(xs) - 1
    widths = [xs[k + 1] - xs[k] for k in range(nseg)]
    slopes = [(ys[k + 1] - ys[k]) / widths[k] for k in range(nseg)]
    delta = model.addVars(nseg, lb=0.0, ub=widths, name=f"dlt[{name}]")
    fill = model.addVars(max(nseg - 1, 0), vtype=GRB.BINARY, name=f"fill[{name}]")
    for k in range(nseg - 1):
        model.addConstr(delta[k] >= widths[k] * fill[k], name=f"pwl_full[{name},{k}]")
        model.addConstr(delta[k + 1] <= widths[k + 1] * fill[k], name=f"pwl_open[{name},{k}]")
    y = model.addVar(lb=min(ys), ub=max(ys), name=f"pwl[{name}]")
    model.addConstr(x == xs[0] + delta.sum(), name=f"pwl_x[{name}]")
    model.addConstr(y == ys[0] + gp.quicksum(slopes[k] * delta[k] for k in range(nseg)),
                    name=f"pwl_y[{name}]")
    return y


# Check: concave cost (slopes 4, 2, 1); minimizing it is the nonconvex direction.
xs, ys = [0.0, 2.0, 5.0, 10.0], [0.0, 8.0, 14.0, 19.0]
for method in (add_pwl_lambda, add_pwl_delta):
    m = gp.Model(method.__name__)
    m.Params.OutputFlag = 0
    x = m.addVar(lb=0.0, ub=10.0, name="x")
    y = method(m, x, xs, ys, "cost")
    m.addConstr(x >= 7.0, name="demand")
    m.setObjective(y, GRB.MINIMIZE)
    m.optimize()
    assert m.Status == GRB.OPTIMAL
    print(f"{method.__name__}: f(7) = {m.ObjVal:.1f}")
# Expected: both methods print f(7) = 16.0 (= 14 + 1*2 on the third segment)
```

For pure approximation jobs (a given nonlinear curve, you choose the grid),
`model.addGenConstrPWL(x, y, xs, ys)` lets Gurobi pick its own internal encoding.

### Fractional objectives: Charnes–Cooper and Dinkelbach

```python
import numpy as np
import gurobipy as gp
from gurobipy import GRB


def solve_lp_fractional_charnes_cooper(
        c: np.ndarray, alpha: float, d: np.ndarray, beta: float,
        a_mat: np.ndarray, b: np.ndarray) -> tuple[np.ndarray, float]:
    """Maximize (c@x + alpha)/(d@x + beta) s.t. a_mat@x <= b, x >= 0, d@x + beta > 0.

    Charnes & Cooper (1962): substitute t = 1/(d@x + beta), y = t*x. Returns (x*, ratio*).
    """
    n = c.size
    m = gp.Model("charnes_cooper")
    m.Params.OutputFlag = 0
    y = m.addMVar(n, lb=0.0, name="y")
    t = m.addMVar(1, lb=1e-9, name="t")
    m.addConstr(a_mat @ y - b * t <= 0.0, name="scaled_rows")
    m.addConstr(d @ y + beta * t == 1.0, name="normalize")
    m.setObjective(c @ y + alpha * t, GRB.MAXIMIZE)
    m.optimize()
    assert m.Status == GRB.OPTIMAL
    return y.X / t.X[0], m.ObjVal


def solve_binary_fractional_dinkelbach(
        p: np.ndarray, p0: float, q: np.ndarray, q0: float,
        a_mat: np.ndarray, b: np.ndarray, tol: float = 1e-9) -> tuple[np.ndarray, float]:
    """Maximize (p@x + p0)/(q@x + q0) over binary x with a_mat@x <= b, q@x + q0 > 0.

    Dinkelbach (1967): solve max p@x + p0 - lam*(q@x + q0), update lam, repeat until ~0.
    """
    n = p.size
    lam = 0.0
    for _ in range(100):
        m = gp.Model("dinkelbach")
        m.Params.OutputFlag = 0
        x = m.addMVar(n, vtype=GRB.BINARY, name="x")
        m.addConstr(a_mat @ x <= b, name="caps")
        m.setObjective((p - lam * q) @ x + (p0 - lam * q0), GRB.MAXIMIZE)
        m.optimize()
        assert m.Status == GRB.OPTIMAL
        if m.ObjVal <= tol:
            return x.X.round().astype(int), lam
        xv = x.X
        lam = float(p @ xv + p0) / float(q @ xv + q0)
    raise RuntimeError("Dinkelbach did not converge in 100 iterations")


# Check 1: max (3x1 + x2 + 1)/(x1 + 2x2 + 2), x1 + x2 <= 4, x >= 0.
x_cc, ratio_cc = solve_lp_fractional_charnes_cooper(
    np.array([3.0, 1.0]), 1.0, np.array([1.0, 2.0]), 2.0,
    np.array([[1.0, 1.0]]), np.array([4.0]))
print(f"CC: ratio={ratio_cc:.4f} at x={x_cc.round(4)}")

# Check 2: max (4x1+3x2+2x3+1)/(2x1+x2+3x3+1) with x1+x2+x3 <= 2, x binary.
x_dk, ratio_dk = solve_binary_fractional_dinkelbach(
    np.array([4.0, 3.0, 2.0]), 1.0, np.array([2.0, 1.0, 3.0]), 1.0,
    np.array([[1.0, 1.0, 1.0]]), np.array([2.0]))
print(f"Dinkelbach: ratio={ratio_dk:.4f} at x={x_dk}")
# Expected: CC ratio = 2.1667 at x = [4, 0]; Dinkelbach ratio = 2.0 (e.g. x = [0, 1, 0])
```

## Worked Example 1: QAP via the Kaufman–Broeckx Linearization

The Koopmans–Beckmann quadratic assignment problem places n facilities at n locations.
With flow matrix F = (f_ik) and distance matrix D = (d_jl), x_ij = 1 if facility i sits at
location j:

$$\min \sum_{i,k}\sum_{j,l} f_{ik}\, d_{jl}\, x_{ij}\, x_{kl}
\quad \text{s.t.}\quad \sum_j x_{ij} = 1 \;\forall i,\quad \sum_i x_{ij} = 1 \;\forall j,\quad x \in \{0,1\}^{n\times n}.$$

The objective is a sum of n⁴ binary products. Full Fortet/Glover linearization of every
product needs O(n⁴) auxiliary variables. Kaufman & Broeckx (1978) instead apply the
binary-times-continuous envelope at the level of whole expressions. Define the interaction
cost of placing i at j given the rest of the assignment:

$$c_{ij}(x) = \sum_{k,l} f_{ik}\, d_{jl}\, x_{kl},
\qquad \text{objective} = \sum_{i,j} x_{ij}\, c_{ij}(x).$$

Introduce w_ij ≥ 0 to stand for x_ij·c_ij(x). Since minimization presses w down, only the
lower envelope is needed: w_ij ≥ c_ij(x) − a_ij(1 − x_ij), with a_ij an upper bound on
c_ij(x). Rearranged into the standard Kaufman–Broeckx constraint:

$$a_{ij}\, x_{ij} + \sum_{k,l} f_{ik}\, d_{jl}\, x_{kl} - w_{ij} \le a_{ij}
\qquad \forall i, j.$$

The constant a_ij is a big-M; tighten it with assignment structure. Because Σ_l x_kl = 1 and
d ≥ 0, every facility k contributes at most f_ik · max_l d_jl, so
a_ij = (Σ_k f_ik)(max_l d_jl) is valid and smaller than the naive Σ_kl f_ik d_jl.

Size: only n² extra continuous variables and n² extra constraints — the most compact known
exact QAP linearization. Price: its LP relaxation is extremely weak. On the demo instance
below the root LP bound is 0.0 even with the tightened a_ij (the relaxation pays fractional
x to switch every KB constraint off). The Adams–Johnson (1994) level-1 RLT linearization
gives far stronger bounds at O(n⁴) size — see Advanced Techniques and the dedicated
quadratic-assignment-problem skill for that trade-off.

```python
import itertools
import numpy as np
import gurobipy as gp
from gurobipy import GRB


def qap_instance(n: int, seed: int) -> tuple[np.ndarray, np.ndarray]:
    """Random symmetric QAP instance: integer flows/distances in {0,...,9}, zero diagonal."""
    rng = np.random.default_rng(seed)
    f = rng.integers(0, 10, size=(n, n))
    d = rng.integers(0, 10, size=(n, n))
    f, d = (f + f.T) // 2, (d + d.T) // 2
    np.fill_diagonal(f, 0)
    np.fill_diagonal(d, 0)
    return f.astype(float), d.astype(float)


def qap_objective(perm: np.ndarray, f: np.ndarray, d: np.ndarray) -> float:
    """Quadratic objective for an assignment: facility i sits at location perm[i]."""
    return float((f * d[np.ix_(perm, perm)]).sum())


def solve_qap_kaufman_broeckx(f: np.ndarray, d: np.ndarray,
                              time_limit: float = 60.0) -> tuple[np.ndarray, float]:
    """Solve the QAP via the Kaufman-Broeckx linearization. Returns (perm, objective)."""
    n = f.shape[0]
    cost = np.einsum("ik,jl->ijkl", f, d)        # cost[i,j,k,l] = f[i,k] * d[j,l]
    a = np.outer(f.sum(axis=1), d.max(axis=1))   # tightened a_ij (needs f, d >= 0)
    m = gp.Model("qap_kb")
    m.Params.OutputFlag = 0
    m.Params.TimeLimit = time_limit
    x = m.addVars(n, n, vtype=GRB.BINARY, name="x")
    w = m.addVars(n, n, lb=0.0, name="w")
    m.addConstrs((x.sum(i, "*") == 1 for i in range(n)), name="facility")
    m.addConstrs((x.sum("*", j) == 1 for j in range(n)), name="location")
    m.addConstrs(
        (a[i, j] * x[i, j]
         + gp.quicksum(cost[i, j, k, l] * x[k, l] for k in range(n) for l in range(n))
         - w[i, j] <= a[i, j]
         for i in range(n) for j in range(n)),
        name="kb")
    m.setObjective(w.sum(), GRB.MINIMIZE)
    m.optimize()
    assert m.Status == GRB.OPTIMAL or (m.Status == GRB.TIME_LIMIT and m.SolCount > 0)
    perm = np.array([next(j for j in range(n) if x[i, j].X > 0.5) for i in range(n)])
    return perm, m.ObjVal


f, d = qap_instance(n=5, seed=3)
perm, obj = solve_qap_kaufman_broeckx(f, d)
assert abs(obj - qap_objective(perm, f, d)) < 1e-6   # independent validation
brute = min(qap_objective(np.array(p), f, d) for p in itertools.permutations(range(5)))
print(f"KB optimum = {obj:.0f}, brute force = {brute:.0f}, perm = {perm}")
# Expected: KB optimum = 204, brute force = 204, perm = [3 1 4 0 2]
```

## Worked Example 2: Fixed-Charge Network with Piecewise-Linear Costs

Single-commodity min-cost flow on a digraph (V, A) where each arc a charges a fixed cost K_a
when opened plus a concave piecewise-linear flow cost g_a(w_a) (decreasing marginal rates —
economies of scale):

$$\min \sum_{a \in A}\Big(K_a\, y_a + g_a(w_a)\Big)
\quad \text{s.t.}\quad \sum_{a \in \delta^+(v)} w_a - \sum_{a \in \delta^-(v)} w_a = b_v \;\forall v,
\qquad 0 \le w_a \le u_a\, y_a,\qquad y_a \in \{0,1\}.$$

Two linearizations interact here:

1. **Fixed charge.** w_a ≤ M_a y_a is a binary-times-continuous envelope in disguise. The
   tight M_a is min(u_a, total demand): no arc ever carries more than the network demands,
   even if its nominal capacity is larger. This single tightening is the classic fix for
   weak fixed-charge network LPs.
2. **Concave PWL cost.** Minimizing a concave g_a is the nonconvex direction — the LP lower
   envelope is the chord under the curve, so binaries (or SOS2) are mandatory. The
   incremental method fits naturally: its first segment variable can couple directly to the
   fixed-charge binary (δ₁ ≤ width₁·y_a), so the arc-opening binary and the PWL chain share
   one variable instead of two. Croxton, Gendron & Magnanti (2003) study exactly this model
   class and show the standard PWL encodings have the same LP bound.

```python
import numpy as np
import gurobipy as gp
from gurobipy import GRB


def fcn_instance(seed: int) -> dict:
    """Small fixed-charge network: node 0 supplies 20 units; nodes 3, 4 demand 12 and 8."""
    rng = np.random.default_rng(seed)
    arcs = [(0, 1), (0, 2), (1, 2), (1, 3), (1, 4), (2, 3), (2, 4)]
    balance = {0: 20.0, 1: 0.0, 2: 0.0, 3: -12.0, 4: -8.0}
    arc = {}
    for a in arcs:
        s1 = float(rng.integers(4, 9))
        arc[a] = {"cap": float(rng.integers(8, 21)),
                  "fixed": float(rng.integers(20, 61)),
                  "slopes": [s1, 0.6 * s1, 0.3 * s1]}   # concave: economies of scale
    return {"arcs": arcs, "balance": balance, "arc": arc}


def pwl_points(cap: float, slopes: list[float]) -> tuple[list[float], list[float]]:
    """Breakpoints (xs, ys) of the concave arc cost on [0, cap], equal-width segments."""
    nseg = len(slopes)
    xs = [cap * k / nseg for k in range(nseg + 1)]
    ys = [0.0]
    for k in range(nseg):
        ys.append(ys[-1] + slopes[k] * (xs[k + 1] - xs[k]))
    return xs, ys


def pwl_eval(v: float, xs: list[float], ys: list[float]) -> float:
    """Evaluate the PWL function defined by (xs, ys) at v."""
    for k in range(len(xs) - 1):
        if v <= xs[k + 1] + 1e-9:
            frac = (v - xs[k]) / (xs[k + 1] - xs[k])
            return ys[k] + frac * (ys[k + 1] - ys[k])
    return ys[-1]


def solve_fixed_charge_pwl(inst: dict) -> tuple[dict, float]:
    """Min-cost flow with fixed charges and concave PWL flow costs. Returns (flows, cost)."""
    total_demand = sum(-b for b in inst["balance"].values() if b < 0)
    m = gp.Model("fcnf_pwl")
    m.Params.OutputFlag = 0
    flow, use, cost_terms = {}, {}, []
    for a in inst["arcs"]:
        d = inst["arc"][a]
        cap = min(d["cap"], total_demand)            # tightened arc big-M
        xs, ys = pwl_points(cap, d["slopes"])
        nseg = len(d["slopes"])
        widths = [xs[k + 1] - xs[k] for k in range(nseg)]
        use[a] = m.addVar(vtype=GRB.BINARY, name=f"use[{a}]")
        delta = m.addVars(nseg, lb=0.0, ub=widths, name=f"dlt[{a}]")
        fill = m.addVars(nseg - 1, vtype=GRB.BINARY, name=f"fill[{a}]")
        m.addConstr(delta[0] <= widths[0] * use[a], name=f"open[{a}]")
        for k in range(nseg - 1):
            m.addConstr(delta[k] >= widths[k] * fill[k], name=f"full[{a},{k}]")
            m.addConstr(delta[k + 1] <= widths[k + 1] * fill[k], name=f"next[{a},{k}]")
        flow[a] = m.addVar(lb=0.0, ub=cap, name=f"w[{a}]")
        m.addConstr(flow[a] == delta.sum(), name=f"link[{a}]")
        cost_terms.append(d["fixed"] * use[a]
                          + gp.quicksum(d["slopes"][k] * delta[k] for k in range(nseg)))
    for v, b in inst["balance"].items():
        m.addConstr(
            gp.quicksum(flow[a] for a in inst["arcs"] if a[0] == v)
            - gp.quicksum(flow[a] for a in inst["arcs"] if a[1] == v) == b,
            name=f"balance[{v}]")
    m.setObjective(gp.quicksum(cost_terms), GRB.MINIMIZE)
    m.optimize()
    assert m.Status == GRB.OPTIMAL
    return {a: flow[a].X for a in inst["arcs"]}, m.ObjVal


def validate(inst: dict, flows: dict, reported: float) -> None:
    """Recompute cost and conservation independently of the model."""
    total_demand = sum(-b for b in inst["balance"].values() if b < 0)
    cost = 0.0
    for a, v in flows.items():
        d = inst["arc"][a]
        cap = min(d["cap"], total_demand)
        if v > 1e-6:
            xs, ys = pwl_points(cap, d["slopes"])
            cost += d["fixed"] + pwl_eval(v, xs, ys)
    for node, b in inst["balance"].items():
        out_v = sum(v for a, v in flows.items() if a[0] == node)
        in_v = sum(v for a, v in flows.items() if a[1] == node)
        assert abs(out_v - in_v - b) < 1e-6, f"conservation violated at {node}"
    assert abs(cost - reported) < 1e-6, f"cost mismatch: {cost} vs {reported}"


inst = fcn_instance(seed=7)
flows, obj = solve_fixed_charge_pwl(inst)
validate(inst, flows, obj)
used = {a: round(v, 2) for a, v in flows.items() if v > 1e-6}
print(f"optimal cost = {obj:.2f}, flows = {used}")
# Expected: optimal cost = 456.77 with 5 arcs used, e.g. flows
# {(0,1): 11.0, (0,2): 9.0, (1,3): 11.0, (2,3): 1.0, (2,4): 8.0}
```

## Advanced Techniques

### Reformulation-Linearization Technique (RLT)

Sherali & Adams (1990) generate stronger linearizations systematically: multiply each
constraint by each binary variable and by its complement, expand, then replace every product
with a linearization variable. Level-1 RLT applied to the QAP (Adams & Johnson 1994) yields
the variables y_ijkl = x_ij x_kl plus consistency rows such as Σ_k y_ijkl = x_ij; its LP
bound dominates Kaufman–Broeckx, Lawler, and most Lagrangian bounds, at the price of O(n⁴)
variables. The general recipe — multiply, expand, substitute — is the standard way to trade
model size for root-bound strength on any 0-1 polynomial program.

### Logarithmic piecewise-linear formulations

The lambda and incremental methods use K−1 or K binaries for K segments. Vielma & Nemhauser
(2011), modeling disjunctive constraints with a logarithmic number of binary variables,
encode the active segment with ⌈log₂K⌉ binaries using a Gray code so adjacent segments
differ in one bit. For cost curves with dozens of breakpoints (price ladders, unit-commitment
heat curves) this shrinks the binary count dramatically while remaining locally ideal. Use it
when K ≳ 16 and the model has many PWL terms; below that the simpler encodings branch as well.

### Convex-hull formulations for disjunctions

For a disjunction w ∈ P₁ ∨ w ∈ P₂ with bounded polyhedra, Balas (1998) gives the extended
hull formulation: duplicate w into copies w¹, w², enforce each copy inside its (scaled)
polyhedron A_i w^i ≤ b_i λ_i, and add w = w¹ + w², λ₁ + λ₂ = 1, λ binary. Its LP relaxation
equals the convex hull of the disjunction — strictly tighter than any big-M version — but it
doubles the variables per disjunction. Rule of thumb: hull formulations pay off when the
disjunction sits in few constraints of a hard model; big-M with tight constants wins when
there are thousands of small disjunctions.

### Optimization-based bound tightening for big-M

Interval arithmetic ignores constraint interaction, so its Ms are often loose. OBBT solves,
for each expression e = a·w that needs a bound, the auxiliary LP max{e : LP relaxation of the
model} and uses the optimum as the new bound. Iterating propagation and OBBT shrinks Ms
monotonically; each shrink tightens the LP relaxation of every implication that uses it.
Budget OBBT like presolve: run it once on the root relaxation, only for the Ms that appear in
constraints the LP actually leaves slack.

### Piecewise McCormick for continuous bilinear terms

When z = v·w with both variables continuous must be handled inside a MILP, partition the
domain of one variable into segments, apply the McCormick envelope per segment, and select
the active segment with binaries (or SOS1). The relaxation error of McCormick shrinks
quadratically with segment width, so even 4–8 partitions help substantially. Compare against
simply setting `model.Params.NonConvex = 2` and letting Gurobi spatial-branch: for a handful
of bilinear terms the built-in method usually wins; for structured products that repeat
thousands of times, a hand-built piecewise McCormick with shared partition binaries can
dominate.

## Practical Challenges

**Trickle flow: solutions violate the logic although the solver says optimal.** With
IntFeasTol = 1e-5 (Gurobi default) a binary can sit at 1e-5 while counted as 0, so a
constraint w ≤ M·y with M = 1e7 silently admits w = 100. Shrink M from bounds, switch the
constraint to an indicator, or tighten IntFeasTol — in that order of preference.

**The LP bound collapses after linearization.** Compact big-M linearizations (Kaufman–Broeckx
is the extreme case — root bound 0.0 in the worked example) buy small size with weak bounds.
If branch-and-bound stalls with a near-zero bound, move along the size/strength curve:
tighter Ms first, then disaggregated or RLT-style variables, then hull formulations.

**Linearizing every product blows up memory.** A quadratic objective over n² binaries has
O(n⁴) products. Before generating them all, check whether an expression-level trick (KB
style), a solver-native quadratic mode, or a Lagrangian/decomposition approach avoids the
expansion entirely. Generating 10⁸ rows is a modeling failure, not a solver failure.

**Epigraph shortcut used in the wrong direction.** t ≥ |w| linearized as t ≥ ±w is correct
only while something presses t down. The bug appears later, when someone adds a term that
rewards large t and the model silently reports t at its upper bound. Audit every abs/min/max
linearization whenever the objective or constraint sense changes; encode exactly (with
binaries) if the use direction is unclear.

**Strict inequalities in reverse implications.** "If w < b then x = 1" has no exact MILP
form; you must pick ε > 0 and model w ≤ b − ε on one branch. Choose ε well above
FeasibilityTol (1e-6), document it, and check the optimum is not sitting inside the ε gap.

**Indicator constraints solve slower than expected.** Indicators are exact and M-free, but
the solver's internal reformulation may be weaker than a hand-tightened big-M when good
bounds exist. Benchmark both on a representative instance: keep indicators when bounds are
poor or Ms would exceed ~1e6; keep explicit big-M when tight constants are available.

**SOS2 versus binary PWL encodings.** SOS2 adds no binaries but relies on special branching;
with many PWL terms, binary encodings (incremental, multiple choice, logarithmic) usually
give better bounds because cuts and presolve act on binaries. If the SOS2 model drifts with
a weak bound, re-encode with binaries before blaming the solver.

**Numerical conditioning after linearization.** Mixing M = 1e6 rows with 1e-3 cost
coefficients yields coefficient ranges the solver flags (`Warning: Model contains large
coefficient range`). Rescale units (move from grams to tonnes, cents to thousands of
dollars) so all matrix coefficients land within roughly [1e-3, 1e6], and re-derive Ms after
rescaling.

## Tools & Libraries

| Library / feature | When to use | Note |
|---|---|---|
| gurobipy general constraints (`addGenConstrAbs/Max/Min/And/Or/Indicator`) | abs, min/max, logic without manual Ms | solver picks the reformulation; bounds still matter |
| gurobipy `addGenConstrPWL` | piecewise-linear objective/constraint terms | pass breakpoints; no manual SOS2 needed |
| gurobipy `Params.NonConvex = 2` | bilinear/quadratic terms left as-is | spatial branch-and-bound; baseline to beat before hand-linearizing |
| Pyomo `Piecewise` + GDP | solver-agnostic models; disjunctive modeling | GDP transformations: `gdp.bigm` and `gdp.hull` map directly to this skill |
| OR-Tools CP-SAT (`AddMultiplicationEquality`, channeling) | integer products and logic at scale | CP propagation replaces linearization for pure-integer terms |
| PySCIPOpt | open-source MINLP with indicator/SOS support | SCIP applies OBBT and its own reformulations |
| docplex (CPLEX) | logical constraints, PWL via `model.piecewise` | automatic indicator handling similar to Gurobi |

## Output Format

A complete linearization deliverable contains:

1. **Reformulation summary table** — one row per nonlinear term:

   | Term | Technique | Aux vars | Aux constrs | Exact / relaxation |
   |---|---|---|---|---|
   | x_ij·c_ij(x) (n² terms) | Kaufman–Broeckx envelope | n² cont. | n² | exact |
   | g_a(w_a), concave, 3 segs | incremental + shared fixed-charge binary | 3 cont. + 2 bin. per arc | 5 per arc | exact |

2. **Big-M provenance table** — every constant with its derivation, so reviewers can audit:

   | Constraint family | M value | Derived from | Slack at optimum |
   |---|---|---|---|
   | kb[i,j] | a_ij = (Σ_k f_ik)(max_l d_jl) | row sums of F, row maxima of D | reported per row |

3. **Model statistics before/after** — variables (cont./bin.), constraints, nonzeros, and
   the root LP bound of the linearized model versus the best known bound, so the
   size/strength trade actually made is visible.

4. **Validation report** — the original nonlinear objective re-evaluated at the MILP
   optimum by independent code (like `qap_objective` and `validate` above), the absolute
   and relative gap to the reported MILP objective, and a pass/fail line per logical
   implication checked at the solution.

5. **Reproducible script** — instance generator seed, solver version, parameter settings
   (`IntFeasTol`, `TimeLimit`, `NonConvex`), and the exact commands run.

State explicitly which reformulations are exact and which are relaxations/approximations,
and give the approximation error bound for any PWL grid used.

## Questions to Ask

- Which variables in each product are binary, integer, or continuous — and what are their
  tightest known bounds?
- Is the nonlinear term used in its convex direction (epigraph is enough) or do we need the
  exact encoding with binaries?
- What solver and version are available — are indicator constraints, SOS2, native PWL, or a
  nonconvex quadratic mode on the table?
- How many instances of each term exist — does the reformulation stay within memory at
  O(count × aux vars)?
- For PWL approximations of smooth functions: what error tolerance is acceptable, and over
  what domain?
- For fractional objectives: is the denominator provably positive over the feasible region?
- Are there strict inequalities or "exactly when" conditions that need an explicit ε?
- What integrality and feasibility tolerances will the production run use (they bound the
  largest safe M)?

## Related Skills

- **milp-modeling-gurobi** — when the question is broader model construction, variable
  design, or Gurobi API usage rather than a specific nonlinear-term reformulation.
- **integer-programming-techniques** — when the linearized model solves slowly and needs
  formulation strengthening, valid inequalities, or branching insight.
- **quadratic-assignment-problem** — when the user works on the QAP itself and needs the
  full formulation landscape (Lawler, RLT, bounds) beyond the linearization shown here.
- **facility-location-problem** — when fixed-charge and big-M patterns appear in location
  models, where the same envelope and tightening ideas drive formulation quality.
