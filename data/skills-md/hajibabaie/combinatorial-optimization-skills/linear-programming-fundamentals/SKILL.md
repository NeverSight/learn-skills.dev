---
name: linear-programming-fundamentals
description: When the user wants to formulate linear programs, solve them with simplex or barrier methods, and interpret the result through duality — shadow prices, reduced costs, sensitivity ranges, degeneracy. Also use when the user mentions "linear programming," "dual values," "shadow price," "sensitivity analysis," "reduced cost," "LP relaxation duals," or when a constraint's economic price is needed to explain or decompose a model. For mixed-integer models, see milp-modeling-gurobi; for LPs whose columns must be priced on demand, see column-generation.
---

# Linear Programming Fundamentals

You are an expert in linear optimization: formulating LPs, solving them with simplex and
interior-point methods, and reading the full dual picture out of a solution — shadow prices,
reduced costs, sensitivity ranges, and degeneracy diagnostics. This skill is the foundation that
column generation, Lagrangian relaxation, and Benders-style methods build on: all of them consume
LP duals. Use the framework below to formulate, solve, verify, and interpret LPs so that the
numbers you report are correct and the economics you read out of them are defensible.

## Initial Assessment

Establish these points before writing any model code:

- **Confirm the problem is actually linear.** Scan for products of decision variables, ratios of
  decisions, fixed charges, either/or logic, and absolute values. Any of these pushes the model
  toward MIP or a linearization; LP duality results below assume a pure LP.
- **Estimate size.** Count rows (constraints), columns (variables), and nonzeros. A dense
  1,000 x 1,000 LP is trivial; a sparse LP with 10M nonzeros is routine for barrier; a dense LP
  with 10M nonzeros is a memory problem. Sparsity drives algorithm choice more than row count.
- **Check solver availability and license.** Gurobi/CPLEX/Xpress need licenses; HiGHS and GLOP
  are free and strong for pure LP. Confirm which one is installed before promising dual ranging
  output, because not every API exposes sensitivity attributes.
- **Identify the data format.** Dense numpy arrays, sparse scipy matrices, pandas tables, or
  dictionaries keyed by entity names. Decide early; it determines whether you build with the
  matrix API or with name-indexed variables, and name-indexed models give readable dual reports.
- **Clarify which outputs matter.** Only the optimal plan? Or also shadow prices for pricing and
  capacity decisions, reduced costs for "what would have to change" questions, and ranging for
  robustness statements? Sensitivity output requires a simplex basis — plan the method accordingly.
- **Determine the re-solve pattern.** One-shot solve, RHS sweeps, repeated solves inside a
  decomposition loop, or LP relaxations inside branch-and-bound. Re-solve patterns decide between
  primal simplex, dual simplex, and barrier (see the algorithm table below).
- **Probe for degeneracy risk.** Many symmetric resources, balanced equality structures
  (transportation, assignment), or redundant constraints mean degenerate optima and non-unique
  duals. Warn the user before they over-interpret a single shadow-price vector.
- **Audit the numeric range.** Ratio of largest to smallest nonzero coefficient above ~1e9 invites
  numerical trouble. Rescale units (tons instead of grams, k-dollars instead of cents) first.
- **Fix the time budget and accuracy target.** LP is polynomially solvable; for almost all
  practical sizes the answer arrives in seconds to minutes. If it does not, the model build
  (Python loops) is usually the bottleneck, not the solver.
- **Plan independent verification.** Decide up front how the solution will be checked: recompute
  the objective from raw data, verify constraint activities, and confirm strong duality.

## LP Anatomy: Geometry, Algorithms, Duality

**Primal-dual pair.** Take the symmetric form with nonnegative variables (any LP converts to it):

$$
\text{(P)} \quad \min_{x} \; c^\top x \quad \text{s.t.} \quad Ax \ge b, \; x \ge 0
\qquad\qquad
\text{(D)} \quad \max_{y} \; b^\top y \quad \text{s.t.} \quad A^\top y \le c, \; y \ge 0
$$

Each dual variable $y_i$ prices one primal constraint; each dual constraint says one primal
variable must not be "overpriced". Three theorems carry all of LP analysis
(Dantzig 1963, *Linear Programming and Extensions*; Chvátal 1983, *Linear Programming*):

- **Weak duality.** Any feasible pair satisfies $b^\top y \le c^\top x$. Every dual feasible
  solution is a valid lower bound on the primal optimum — the root of all bounding methods.
- **Strong duality.** If either problem has a finite optimum, both do, and
  $c^\top x^* = b^\top y^*$. Equality of the two objectives is the cheapest correctness check
  you will ever run.
- **Complementary slackness.** At optimality,
  $y_i^* (a_i^\top x^* - b_i) = 0$ for every row and $x_j^* (c_j - A_j^\top y^*) = 0$ for every
  column: a price is only nonzero on a binding constraint, and a variable is only used when its
  reduced cost is zero.

**The three numbers a solved LP gives you.**

- *Shadow price (dual value, `Pi`)*: rate of change of the optimal objective per unit increase of
  one RHS, valid while the optimal basis stays optimal (`SARHSLow`/`SARHSUp` in Gurobi give that
  interval). It is a local derivative, not a global price.
- *Reduced cost (`RC`)*: $\bar{c}_j = c_j - y^\top A_j$, the amount the objective coefficient of a
  nonbasic variable must improve before that variable enters the optimal solution. In column
  generation, the pricing problem searches for a column with negative reduced cost.
- *Slack*: $b_i - a_i^\top x^*$ (sign per sense). Nonzero slack forces a zero shadow price by
  complementary slackness.

**Sign conventions (Gurobi: `Pi` = change in objective per unit RHS increase).**

| Objective sense | Binding `>=` row | Binding `<=` row | `=` row | Var at LB | Var at UB | Basic var |
|---|---|---|---|---|---|---|
| minimize | `Pi >= 0` | `Pi <= 0` | any sign | `RC >= 0` | `RC <= 0` | `RC = 0` |
| maximize | `Pi <= 0` | `Pi >= 0` | any sign | `RC <= 0` | `RC >= 0` | `RC = 0` |

A "wrong-signed" dual almost always means the sense or the objective direction is not what you
assumed — check this table before suspecting the solver.

**Simplex intuition.** The feasible region is a polyhedron; some vertex is optimal. Simplex walks
vertex to vertex: a basis $B$ (one column per row) defines $x_B = B^{-1}b$; pricing computes
reduced costs $\bar{c}_j$; a negative one (minimization) admits an improving edge; the ratio test
picks the leaving variable. Worst case is exponential (Klee & Minty 1972, *How Good Is the
Simplex Algorithm?*), but in practice iteration counts grow roughly linearly with row count
(Bixby 2002, *Solving Real-World Linear Programs*). Simplex output includes an optimal **basis**,
which is what makes warm starts, ranging, and branch-and-bound node re-solves cheap.

**Barrier intuition.** Interior-point methods follow the central path of the log-barrier problem
$\min c^\top x - \mu \sum_j \ln x_j$, driving $\mu \to 0$ with Newton steps; each step factorizes
$A D A^\top$ (Karmarkar 1984 started the practical line). Iteration counts are nearly constant
(20-100) regardless of size, so barrier wins on large sparse one-shot solves — but it returns an
interior point, not a basis. Run **crossover** (on by default in Gurobi) when you need ranging,
warm starts, or vertex solutions.

**Algorithm choice.**

| Method | Use when | Why |
|---|---|---|
| Primal simplex (`Method=0`) | Re-solving after adding columns or changing costs | Old basis stays primal feasible |
| Dual simplex (`Method=1`) | Re-solving after RHS/bound changes or new rows; B&B nodes | Old basis stays dual feasible |
| Barrier (`Method=2`) | Large sparse LP solved from scratch; parallel cores available | Few iterations, scales well |
| Concurrent (`Method=3`, Gurobi default `-1`) | Unknown structure, single solve | First finisher wins |

**Degeneracy.** Primal degeneracy = a basic variable sits exactly at a bound (more binding
constraints than dimensions at the vertex). Consequences: simplex can stall on zero-length steps,
and the optimal dual solution is **not unique** — different methods (or the same method after
permuting rows) return different, equally valid shadow-price vectors. Dual degeneracy (a nonbasic
variable with zero reduced cost) means multiple primal optima. Balanced transportation and
assignment structures are degenerate by construction; treat their reported duals with care
(see the transportation example and Advanced Techniques).

## Generic Workflow: Solve, Extract, Verify

The reusable skeleton every LP analysis follows:

```text
LP SOLVE-AND-ANALYZE SKELETON
input : c (objective), A, senses, b, variable bounds
output: x*, duals y*, reduced costs, sensitivity report, verification log

1. BUILD   one variable per column with explicit bounds;
           one NAMED constraint per row (names make dual reports readable)
2. METHOD  first large sparse solve -> barrier + crossover
           re-solve after RHS/bound change -> dual simplex
           re-solve after new columns -> primal simplex
3. SOLVE   check status:
           OPTIMAL    -> continue
           INFEASIBLE -> compute IIS or elastic relaxation, report, stop
           UNBOUNDED  -> inspect the ray, find the missing constraint, stop
4. EXTRACT in one pass: x (.X), reduced costs (.RC), duals (.Pi),
           slacks (.Slack), basis (.VBasis/.CBasis),
           ranging (.SAObjLow/.SAObjUp, .SARHSLow/.SARHSUp)
5. VERIFY  independently of the model object:
           recompute c'x from raw data; check strong duality c'x == b'y;
           check complementary slackness pairwise; check dual signs
6. REPORT  solution table, dual table with validity ranges, verification log
```

Generic implementation (dense data for clarity; swap in `scipy.sparse` matrices unchanged —
`addMConstr` accepts them):

```python
from dataclasses import dataclass

import gurobipy as gp
import numpy as np
from gurobipy import GRB


@dataclass
class LPResult:
    """Everything downstream analysis needs from one LP solve."""
    status: int
    objective: float | None = None
    x: np.ndarray | None = None
    reduced_costs: np.ndarray | None = None
    duals: np.ndarray | None = None
    slacks: np.ndarray | None = None
    vbasis: list[int] | None = None
    cbasis: list[int] | None = None


def solve_lp(
    c: np.ndarray,
    a_mat: np.ndarray,
    senses: list[str],
    rhs: np.ndarray,
    minimize: bool = True,
    method: int = 0,
) -> LPResult:
    """Solve min/max c@x s.t. A x {<=,=,>=} b, x >= 0, and extract the full dual picture.

    method: 0 primal simplex, 1 dual simplex, 2 barrier (keep Crossover at its
    default >= 1 with barrier, otherwise basis-dependent attributes are missing).
    """
    model = gp.Model("generic_lp")
    model.Params.OutputFlag = 0
    model.Params.Method = method
    x = model.addMVar(c.shape[0], lb=0.0, name="x")
    model.setObjective(c @ x, GRB.MINIMIZE if minimize else GRB.MAXIMIZE)
    sense_char = {"<=": GRB.LESS_EQUAL, "=": GRB.EQUAL, ">=": GRB.GREATER_EQUAL}
    model.addMConstr(a_mat, x, [sense_char[s] for s in senses], rhs, name="row")
    model.optimize()
    if model.Status != GRB.OPTIMAL:
        return LPResult(status=model.Status)
    cons = model.getConstrs()
    return LPResult(
        status=model.Status,
        objective=model.ObjVal,
        x=np.asarray(x.X),
        reduced_costs=np.asarray(x.RC),
        duals=np.asarray(model.getAttr("Pi", cons)),
        slacks=np.asarray(model.getAttr("Slack", cons)),
        vbasis=model.getAttr("VBasis", model.getVars()),
        cbasis=model.getAttr("CBasis", cons),
    )


if __name__ == "__main__":
    # Tiny instance (the diet LP from the next section, in matrix form).
    c = np.array([2.0, 3.0, 2.5])
    a_mat = np.array([[4.0, 2.0, 1.0],
                      [1.0, 2.0, 1.0],
                      [1.0, 1.0, 0.0]])
    res = solve_lp(c, a_mat, [">=", ">=", "<="], np.array([8.0, 4.0, 100.0]))
    print(res.objective, res.x, res.duals, res.reduced_costs)
    # Expected: objective = 6.6667, x = [1.3333, 1.3333, 0.0],
    # duals = [0.1667, 1.3333, 0.0]  (third row is slack, so its price is 0),
    # reduced_costs = [0.0, 0.0, 1.0].
```

Sensitivity extraction as tidy tables (pandas is appropriate here — these are report artifacts).
Both functions require an optimal **basis**: simplex, or barrier with crossover.

```python
import gurobipy as gp
import pandas as pd
from gurobipy import GRB


def variable_sensitivity(model: gp.Model) -> pd.DataFrame:
    """One row per variable: value, reduced cost, objective-coefficient range."""
    if model.Status != GRB.OPTIMAL:
        raise ValueError(f"need an optimal basis, got status {model.Status}")
    if model.IsMIP:
        raise ValueError("sensitivity attributes exist only for pure LPs")
    rows = [
        {"var": v.VarName, "value": v.X, "reduced_cost": v.RC,
         "obj_coeff": v.Obj, "obj_low": v.SAObjLow, "obj_up": v.SAObjUp,
         "lb": v.LB, "ub": v.UB}
        for v in model.getVars()
    ]
    return pd.DataFrame(rows)


def constraint_sensitivity(model: gp.Model) -> pd.DataFrame:
    """One row per constraint: shadow price, slack, RHS validity range."""
    if model.Status != GRB.OPTIMAL:
        raise ValueError(f"need an optimal basis, got status {model.Status}")
    rows = [
        {"constr": con.ConstrName, "sense": con.Sense, "rhs": con.RHS,
         "slack": con.Slack, "shadow_price": con.Pi,
         "rhs_low": con.SARHSLow, "rhs_up": con.SARHSUp}
        for con in model.getConstrs()
    ]
    return pd.DataFrame(rows)
```

Independent verification — never read duals without confirming they certify optimality. This
check uses only raw data plus the returned vectors, not the model object, so a modeling bug
cannot certify itself:

```python
import numpy as np


def verify_lp_duality(
    c: np.ndarray,
    a_mat: np.ndarray,
    senses: list[str],
    rhs: np.ndarray,
    x: np.ndarray,
    duals: np.ndarray,
    reduced_costs: np.ndarray,
    tol: float = 1e-6,
) -> dict[str, bool]:
    """Certify a min-LP solution (x >= 0, no finite upper bounds) via duality theory.

    Returns named boolean checks; all True means (x, duals) is an optimal pair.
    """
    activity = a_mat @ x
    slack = rhs - activity
    primal_obj = float(c @ x)
    dual_obj = float(rhs @ duals)
    rc_from_duals = c - a_mat.T @ duals
    return {
        "primal_feasible": all(
            (s == ">=" and act >= b - tol)
            or (s == "<=" and act <= b + tol)
            or (s == "=" and abs(act - b) <= tol)
            for s, act, b in zip(senses, activity, rhs)
        ) and bool(np.all(x >= -tol)),
        "dual_signs": all(
            (s == ">=" and d >= -tol) or (s == "<=" and d <= tol) or s == "="
            for s, d in zip(senses, duals)
        ),
        "dual_feasible": bool(np.all(rc_from_duals >= -tol)),
        "reduced_cost_identity": bool(np.allclose(reduced_costs, rc_from_duals, atol=1e-5)),
        "strong_duality": abs(primal_obj - dual_obj) <= tol * (1.0 + abs(primal_obj)),
        "compl_slack_rows": bool(np.all(np.abs(duals * slack) <= tol * (1.0 + np.abs(rhs)))),
        "compl_slack_cols": bool(np.all(np.abs(reduced_costs * x) <= tol * (1.0 + np.abs(c)))),
    }
```

If `strong_duality` fails but both feasibility checks pass, the solve terminated early or the
extraction mixed up rows — investigate before reporting anything.

## Worked Example 1: Diet/Blending LP with Full Dual Analysis

The diet problem (Stigler 1945, *The Cost of Subsistence*) is the canonical pricing LP: choose
quantities $x_j \ge 0$ of foods with unit costs $c_j$ so that every nutrient floor is met and a
fat ceiling is respected, at minimum cost. The same structure covers alloy blending, feed mix,
and fuel blending.

$$
\min \sum_j c_j x_j
\quad \text{s.t.} \quad
\sum_j a_{nj} x_j \ge r_n \;\; \forall n \in N \text{ (nutrient floors)}, \qquad
\sum_j f_j x_j \le F \text{ (fat ceiling)}, \qquad x \ge 0
$$

Its dual prices the nutrients ($u_n \ge 0$ per unit of floor $r_n$) and the fat budget
($w \le 0$, since raising a ceiling can only help a minimization):

$$
\max \sum_n r_n u_n + F w
\quad \text{s.t.} \quad
\sum_n a_{nj} u_n + f_j w \le c_j \;\; \forall j, \qquad u \ge 0, \; w \le 0
$$

The dual constraint for food $j$ reads: the nutritional value of one unit of food $j$, priced at
the optimal nutrient prices, never exceeds its market cost. Foods actually bought are priced
exactly fairly (complementary slackness); foods not bought are overpriced by exactly their
reduced cost.

```python
import gurobipy as gp
from gurobipy import GRB

# Tiny blending instance: 3 foods, 2 nutrient floors, 1 fat ceiling.
foods = ["grain", "dairy", "legume"]
cost = {"grain": 2.0, "dairy": 3.0, "legume": 2.5}
nutrients = ["calories", "protein"]
floor = {"calories": 8.0, "protein": 4.0}
content = {  # content[nutrient][food] = units per unit of food
    "calories": {"grain": 4.0, "dairy": 2.0, "legume": 1.0},
    "protein": {"grain": 1.0, "dairy": 2.0, "legume": 1.0},
}
fat = {"grain": 1.0, "dairy": 1.0, "legume": 0.0}
fat_cap = 100.0

model = gp.Model("diet")
model.Params.OutputFlag = 0
model.Params.Method = 0  # primal simplex: we want a basis for ranging
buy = model.addVars(foods, lb=0.0, name="buy")
model.setObjective(gp.quicksum(cost[f] * buy[f] for f in foods), GRB.MINIMIZE)
need = model.addConstrs(
    (gp.quicksum(content[n][f] * buy[f] for f in foods) >= floor[n] for n in nutrients),
    name="need",
)
fat_con = model.addConstr(
    gp.quicksum(fat[f] * buy[f] for f in foods) <= fat_cap, name="fat_cap"
)
model.optimize()

if model.Status == GRB.OPTIMAL:
    print(f"total cost = {model.ObjVal:.4f}")
    for f in foods:
        print(f"  buy[{f}] = {buy[f].X:.4f}   reduced_cost = {buy[f].RC:+.4f}   "
              f"obj range = [{buy[f].SAObjLow:.3f}, {buy[f].SAObjUp:.3f}]")
    for n in nutrients:
        con = need[n]
        print(f"  {n}: shadow = {con.Pi:.4f}   slack = {con.Slack:.4f}   "
              f"rhs range = [{con.SARHSLow:.3f}, {con.SARHSUp:.3f}]")
    print(f"  fat_cap: shadow = {fat_con.Pi:.4f}   slack = {fat_con.Slack:.4f}")

# Expected: total cost = 6.6667; buy[grain] = buy[dairy] = 1.3333, buy[legume] = 0.
# Expected: shadow(calories) = 0.1667, shadow(protein) = 1.3333, shadow(fat_cap) = 0
#           (the fat ceiling has slack 97.33, so its price must be 0).
# Expected: reduced_cost(legume) = +1.0000 -> legume enters only if it gets 1.0 cheaper,
#           i.e. exactly when its cost reaches its priced nutritional value 1.5.
```

Reading the dual analysis:

- **Shadow prices are marginal nutrient prices.** One more unit of the calorie floor costs
  0.1667 in extra purchases; one more unit of the protein floor costs 1.3333. Within the printed
  RHS ranges these rates are exact, not approximations.
- **Reduced cost as a bid threshold.** Legume is overpriced by 1.0: its cost (2.5) exceeds its
  nutrient value at optimal prices ($1 \cdot 0.1667 + 1 \cdot 1.3333 = 1.5$). The `SAObjLow`
  column for legume confirms the entry threshold.
- **Zero price on a slack ceiling.** The fat ceiling is not binding, so paying for more fat
  budget is worthless — complementary slackness made that conclusion before you looked at slack.

Strong duality, made concrete — build the dual explicitly and confirm both objectives meet:

```python
import gurobipy as gp
from gurobipy import GRB

# Explicit dual of the diet LP above: price nutrients so no food is overpriced.
model = gp.Model("diet_dual")
model.Params.OutputFlag = 0
u_cal = model.addVar(lb=0.0, name="u_calories")
u_pro = model.addVar(lb=0.0, name="u_protein")
w_fat = model.addVar(lb=-GRB.INFINITY, ub=0.0, name="w_fat")  # prices a <= ceiling
model.setObjective(8.0 * u_cal + 4.0 * u_pro + 100.0 * w_fat, GRB.MAXIMIZE)
model.addConstr(4.0 * u_cal + 1.0 * u_pro + 1.0 * w_fat <= 2.0, name="price_grain")
model.addConstr(2.0 * u_cal + 2.0 * u_pro + 1.0 * w_fat <= 3.0, name="price_dairy")
model.addConstr(1.0 * u_cal + 1.0 * u_pro <= 2.5, name="price_legume")
model.optimize()

if model.Status == GRB.OPTIMAL:
    print(f"dual objective = {model.ObjVal:.4f}")
    print(f"prices: calories = {u_cal.X:.4f}, protein = {u_pro.X:.4f}, fat = {w_fat.X:.4f}")

# Expected: dual objective = 6.6667 — equal to the primal cost (strong duality).
# Expected: prices = (0.1667, 1.3333, 0.0), matching the primal shadow prices, and the
#           dual variables of THIS model reproduce the primal solution (1.3333, 1.3333, 0).
```

Run `variable_sensitivity` / `constraint_sensitivity` from the generic section on the primal
model to get the same analysis as DataFrames ready for a report.

## Worked Example 2: Transportation LP

The transportation problem (Hitchcock 1941) ships from plants $i$ with supplies $s_i$ to
customers $j$ with demands $d_j$ at unit cost $c_{ij}$, balanced so
$\sum_i s_i = \sum_j d_j$:

$$
\min \sum_{i,j} c_{ij} x_{ij}
\quad \text{s.t.} \quad
\sum_j x_{ij} = s_i \;\forall i, \qquad
\sum_i x_{ij} = d_j \;\forall j, \qquad x \ge 0
$$

The dual has a free price per plant ($u_i$) and per customer ($v_j$) with one constraint per
lane: $u_i + v_j \le c_{ij}$. Optimality means $c_{ij} - u_i - v_j = 0$ on every shipping lane
and $\ge 0$ elsewhere — exactly the MODI (u-v) method test from classical OR courses. Two
structural facts matter:

- **Integrality for free.** The constraint matrix is totally unimodular (Hoffman & Kruskal 1956),
  so with integer supplies and demands every basic optimal solution is integer — no MIP needed.
  This is the same mechanism that makes pure network-flow LPs integral.
- **Built-in dual non-uniqueness.** The $m + n$ balance rows sum to the same identity on both
  sides, so one row is redundant: rank is $m + n - 1$, a basis has $m + n - 1$ lanes, and duals
  are unique only up to adding a constant to all $u_i$ and subtracting it from all $v_j$.
  Report **reduced costs** (shift-invariant), not raw $u, v$ values.

```python
import gurobipy as gp
from gurobipy import GRB

supply = {"p1": 20.0, "p2": 30.0}
demand = {"c1": 15.0, "c2": 25.0, "c3": 10.0}
cost = {
    ("p1", "c1"): 4.0, ("p1", "c2"): 6.0, ("p1", "c3"): 8.0,
    ("p2", "c1"): 5.0, ("p2", "c2"): 3.0, ("p2", "c3"): 7.0,
}
assert abs(sum(supply.values()) - sum(demand.values())) < 1e-9, "must be balanced"

model = gp.Model("transportation")
model.Params.OutputFlag = 0
model.Params.Method = 0
ship = model.addVars(cost.keys(), lb=0.0, name="ship")
model.setObjective(ship.prod(cost), GRB.MINIMIZE)
out_bal = model.addConstrs((ship.sum(i, "*") == supply[i] for i in supply), name="supply")
in_bal = model.addConstrs((ship.sum("*", j) == demand[j] for j in demand), name="demand")
model.optimize()

if model.Status == GRB.OPTIMAL:
    print(f"min cost = {model.ObjVal:.2f}")
    for (i, j), var in ship.items():
        if var.X > 1e-9:
            print(f"  {i} -> {j}: {var.X:.1f}")
    u = {i: out_bal[i].Pi for i in supply}
    v = {j: in_bal[j].Pi for j in demand}
    for (i, j) in cost:
        rc = cost[i, j] - u[i] - v[j]
        print(f"  rc[{i},{j}] = {rc:+.3f}")

# Expected: min cost = 210.00 with ship p1->c1 = 15, p1->c3 = 5, p2->c2 = 25, p2->c3 = 5.
# Expected: rc = 0 on all four shipping lanes; rc[p1,c2] = +2, rc[p2,c1] = +2.
# Note: individual u, v values depend on the solver's normalization (one redundant row);
#       only the reduced costs are well defined. Here one valid pair is
#       u = (0, -1), v = (4, 4, 8).
```

The reduced costs answer the operational question directly: lane p1->c2 is 2.0/unit too
expensive to use; if its tariff drops below 4.0, the optimal shipping plan changes.

Basis diagnostics — count basic lanes and check integrality and degeneracy:

```python
import gurobipy as gp
import numpy as np
from gurobipy import GRB


def transportation_basis_report(model: gp.Model) -> dict[str, int | bool]:
    """Inspect an optimal transportation basis: size, degeneracy, integrality."""
    if model.Status != GRB.OPTIMAL:
        raise ValueError(f"not optimal, status {model.Status}")
    x = np.asarray(model.getAttr("X", model.getVars()))
    vbasis = np.asarray(model.getAttr("VBasis", model.getVars()))
    basic = vbasis == 0  # Gurobi code 0 == basic
    return {
        "n_basic_lanes": int(basic.sum()),
        "rank_m_plus_n_minus_1": model.NumConstrs - 1,
        "degenerate": bool(np.any(basic & (x < 1e-9))),
        "integral": bool(np.all(np.abs(x - np.round(x)) < 1e-9)),
    }

# Usage on the solved model above:
# transportation_basis_report(model)
# Expected: {'n_basic_lanes': 4, 'rank_m_plus_n_minus_1': 4,
#            'degenerate': False, 'integral': True}
# A degenerate instance (e.g. one supply exactly equal to one demand) keeps
# n_basic_lanes at 4 but with a basic lane at flow 0 -> duals become ambiguous
# beyond the constant shift.
```

When the instance grows, the same model is better solved as a min-cost flow
(`network-flow-optimization` covers dedicated algorithms that beat general LP by orders of
magnitude on pure network structure).

## Advanced Techniques

### Degeneracy and non-unique shadow prices

When the optimal vertex is degenerate, several bases describe it and each basis has its own dual
vector. The objective as a function of one RHS then has a kink **at the current value**: the
right derivative (price of more) and the left derivative (price of less) differ, and the reported
`Pi` is whichever one the final basis encodes. Defensive protocol: (1) detect degeneracy (a basic
variable at a bound, or `SARHSLow == SARHSUp == RHS`); (2) if a price drives a real decision,
measure both one-sided prices by re-solving with `RHS + eps` and `RHS - eps`; (3) never compare
shadow prices coming from different solver methods/runs on degenerate models without this check.

### The validity range of a shadow price

The optimal value of a min-LP is a convex piecewise-linear function of any single RHS. The shadow
price is the slope of the current piece; `SARHSLow`/`SARHSUp` delimit that piece. Outside the
range the basis changes and the price moves (always against you, by convexity). Demonstrate or
audit it with a sweep:

```python
import gurobipy as gp
import numpy as np
from gurobipy import GRB


def rhs_sweep(
    model: gp.Model, constr_name: str, rhs_values: np.ndarray
) -> list[tuple[float, float]]:
    """Re-solve one LP for each RHS value of one constraint; return (rhs, objective)."""
    model.Params.OutputFlag = 0
    model.Params.Method = 1  # dual simplex: RHS changes keep the old basis dual feasible
    con = model.getConstrByName(constr_name)
    points: list[tuple[float, float]] = []
    for b in rhs_values:
        con.RHS = float(b)
        model.optimize()
        obj = model.ObjVal if model.Status == GRB.OPTIMAL else float("nan")
        points.append((float(b), obj))
    return points

# On the diet model: rhs_sweep(model, "need[protein]", np.linspace(2.0, 8.0, 13))
# Expected: a convex piecewise-linear curve; slope 1.3333 around rhs = 4.0,
# changing exactly at the SARHSLow/SARHSUp values reported by the single solve.
# NaN segments mark RHS values where the LP becomes infeasible.
```

Sensitivity ranges are one-at-a-time statements. For simultaneous changes use the 100% rule
(Bradley, Hax & Magnanti 1977, *Applied Mathematical Programming*) or simply re-solve — modern
LP re-solves are cheap enough that re-solving is usually the honest answer.

### Basis reuse and warm starts

A stored basis turns a family of related solves into a sequence of short re-optimizations — the
mechanism behind fast branch-and-bound nodes and column-generation iterations:

```python
import gurobipy as gp
from gurobipy import GRB


def save_basis(model: gp.Model) -> tuple[list[int], list[int]]:
    """Snapshot the optimal basis (variable and constraint status codes)."""
    return (
        model.getAttr("VBasis", model.getVars()),
        model.getAttr("CBasis", model.getConstrs()),
    )


def load_basis(model: gp.Model, basis: tuple[list[int], list[int]]) -> None:
    """Install a saved basis; the next solve starts from it instead of from scratch."""
    vbasis, cbasis = basis
    model.setAttr("VBasis", model.getVars(), vbasis)
    model.setAttr("CBasis", model.getConstrs(), cbasis)
    model.Params.LPWarmStart = 1

# Pattern: solve once, save_basis; perturb RHS/costs; load_basis; re-solve.
# Expected: iteration count near 0-10 on the re-solve versus a cold start,
# because only the rows/columns affected by the perturbation need pivots.
```

Rule of thumb: after RHS or bound changes, the old basis stays **dual** feasible — use dual
simplex. After cost changes or new columns, it stays **primal** feasible — use primal simplex.

### Duals as engines for decomposition

Every classic decomposition consumes the quantities defined in this skill. Column generation
prices an absent column $j$ by $c_j - y^\top A_j$ using the restricted master's duals and asks a
subproblem to find the most negative one. Lagrangian relaxation moves constraints into the
objective with multipliers that play the role of (and at convergence relate to) LP duals; the
subgradient at $\lambda$ is exactly the constraint violation. Benders cuts are built from
subproblem duals (optimality cuts) and dual rays (feasibility cuts). If shadow prices and reduced
costs are solid for you here, those three methods are bookkeeping on top.

### Scaling and numerical conditioning

Keep the ratio of largest to smallest nonzero coefficient below ~1e9, ideally 1e6, by choosing
units; do the same for RHS and bounds. Symptoms of bad conditioning: warnings about large
coefficient ranges, duals that flip between runs, tiny negative values in supposedly nonnegative
variables. Remedies in order: rescale the data; set `NumericFocus=2..3`; switch method (barrier
and simplex fail differently); as a last resort `Quad=1`. Inspect `model.KappaExact` when you
suspect an ill-conditioned basis. Never "fix" conditioning by loosening feasibility tolerances —
that hides the disease and corrupts the duals you are about to interpret.

## Practical Challenges

**A constraint everyone calls critical has a zero shadow price.** Two legitimate causes: the
constraint is not binding (check slack first), or the optimum is degenerate and an alternative
optimal dual vector assigns it a positive price. Re-solve with the RHS perturbed by a small eps
in each direction; the two one-sided objective changes are the honest prices to report.

**Dual values have the "wrong" sign.** Almost always a convention mismatch, not a solver bug.
Gurobi's `Pi` is the objective change per unit RHS *increase*; a binding `<=` row in a
minimization therefore has `Pi <= 0`. Check the sign table in the anatomy section, and confirm
the model sense (`ModelSense`) before re-deriving anything.

**Sensitivity attributes raise errors after a barrier solve.** Ranging (`SAObjLow`, `SARHSLow`)
and basis attributes need a vertex/basis. Barrier with `Crossover=0` returns an interior point —
no basis, no ranging, and on degenerate models a *different* (well-centered) dual than simplex
returns. Re-enable crossover or re-solve with `Method=0/1` when the analysis needs a basis.

**The LP is infeasible and the user wants to know why.** Do not bisect by hand. Compute an IIS
(`model.computeIIS()`) to get a minimal conflicting subsystem, or run an elastic relaxation
(`model.feasRelaxS(0, False, False, True)`) to find the cheapest constraint violations. The
violated-set output is the diagnosis; report it instead of "infeasible".

**The LP is unbounded, which "cannot happen" for this application.** A cost coefficient with the
wrong sign or a missing constraint family lets some activity run to infinity. Set
`InfUnbdInfo=1`, read `UnbdRay`, and the nonzero entries of the ray name exactly the variables
riding to infinity — that names the missing constraint. Note Gurobi may first report
`INF_OR_UNBD` with presolve on; set `DualReductions=0` and re-solve to split the two cases.

**Model build time dwarfs solve time.** Ten million `addConstr` calls in a Python loop take far
longer than the solve. Switch to the matrix API (`addMVar`/`addMConstr` with `scipy.sparse`
input), or batch with `addConstrs` over generators; keep name strings short or empty on bulk
rows (names cost memory) but always name the rows whose duals you intend to read.

**Reported duals differ between two machines / solver versions on the same data.** Expected on
degenerate models: multiple optimal dual solutions exist and tie-breaking is implementation
detail. Fix the random seed (`Seed`), pin the method, and — if reproducibility of duals matters —
report shift-invariant or perturbation-validated quantities (reduced costs, one-sided prices)
rather than raw `Pi` vectors.

**Free variables make the textbook dual derivation break.** A free primal variable produces a
dual *equality*; a primal equality produces a free dual. Mechanical recipe: min problem —
`>=` row gives $y_i \ge 0$, `<=` row gives $y_i \le 0$, `=` row gives free $y_i$; variable
$x_j \ge 0$ gives dual row $\le c_j$, free $x_j$ gives dual row $= c_j$. Write the table down
before deriving any dual by hand; most hand-derivation bugs are sign/sense slips.

## Tools & Libraries

| Library | Use when | Note |
|---|---|---|
| gurobipy | Default for serious LP work with a license | Full duals, ranging, basis, IIS, warm starts |
| HiGHS (`highspy`) | Free, high-performance simplex/barrier | Duals and basis exposed; the strongest open LP code |
| `scipy.optimize.linprog` | Small/medium LPs inside a SciPy stack | `method="highs"`; duals via `result.ineqlin.marginals` |
| OR-Tools GLOP | Free LP inside an OR-Tools pipeline | Solid simplex; fewer sensitivity features |
| PuLP | Quick modeling layer over CBC/HiGHS/Gurobi | Easy start; sensitivity access depends on backend |
| Pyomo | Large structured models, solver-agnostic research code | Duals via `Suffix(direction=Suffix.IMPORT)` |
| CVXPY | LP mixed with conic/convex pieces | Duals via `constraint.dual_value`; not basis-oriented |
| pandas | Sensitivity and solution report tables | Output artifact, not a solver |

## Output Format

A complete LP analysis deliverable contains:

1. **Model summary.**

| item | value |
|---|---|
| sense / rows / cols / nonzeros | min / 3 / 3 / 8 |
| method / iterations / time | primal simplex / 3 / 0.01 s |
| status | OPTIMAL |

2. **Solution table** — variable, value, reduced cost, objective-coefficient range
   (the `variable_sensitivity` DataFrame).
3. **Dual table** — constraint, sense, RHS, slack, shadow price, RHS validity range
   (the `constraint_sensitivity` DataFrame).
4. **Verification log** — output of `verify_lp_duality`: primal feasibility, dual feasibility,
   strong duality, complementary slackness, all True, with the tolerance used.
5. **Interpretation paragraph** — each binding constraint's price in domain units
   ("one extra hour of finishing capacity is worth 13.0 of profit, valid up to 120 h"),
   each zero-price constraint named as non-binding, each attractive nonbasic variable's entry
   threshold from its reduced cost.
6. **Caveats** — degeneracy flags, one-at-a-time validity of ranges, scaling applied to the
   data, and the solver/version/seed for reproducibility.

Files worth writing: `model.lp` (human-readable model dump via `model.write("model.lp")`) for
review, `solution.csv` / `duals.csv` for downstream use. For decomposition contexts, also store
the basis (`model.write("warm.bas")`) so follow-up solves warm start.

## Questions to Ask

- How large is the model — rows, columns, nonzeros — and is the matrix sparse?
- Is everything truly continuous and linear, or are there hidden integrality/logic requirements?
- Which solver and license are available, and must the code also run on a free stack?
- Do you need dual values and sensitivity ranges, or only the optimal plan?
- Will the model be solved once or re-solved many times with small changes (which changes)?
- Are there equality-heavy structures (balance equations) that make degeneracy likely?
- What units are the data in, and how wide is the coefficient range?
- Which decision will the shadow prices actually drive — capacity purchase, pricing, contracts?
- What counts as proof of correctness for your setting — duality check, known optimum, both?

## Related Skills

- **milp-modeling-gurobi** — when the model needs integer or binary decisions; this skill's LP
  machinery becomes the relaxation engine inside the MIP.
- **column-generation** — when there are exponentially many variables and the restricted-master
  duals from this skill drive a pricing subproblem.
- **lagrangian-relaxation** — when duals are needed for constraints you would rather move into
  the objective; multipliers generalize the shadow prices defined here.
- **network-flow-optimization** — when the LP has pure flow structure (transportation,
  assignment, shortest path); specialized algorithms and integrality results apply.
- **problem-formulation** — when the word problem is not yet a model; decide decisions,
  objective, and constraints before any of the analysis here applies.
