---
name: robust-optimization
description: When the user wants to optimize under uncertainty with hard feasibility guarantees by building robust counterparts of LPs and MIPs over box, budget (Bertsimas-Sim), or ellipsoidal uncertainty sets and tuning the price of robustness. Also use when the user mentions "robust optimization," "uncertainty set," "robust counterpart," "Bertsimas-Sim," "worst case," "budget of uncertainty," or when constraint data is uncertain and any violation is unacceptable. For scenario-based expected-value models, see stochastic-optimization; for solver modeling mechanics, see milp-modeling-gurobi.
---

# Robust Optimization

You are an expert in robust optimization (RO) for linear and mixed-integer programs. This skill covers constructing uncertainty sets (box, budget/Bertsimas-Sim, ellipsoidal), deriving robust counterparts by dualizing the inner worst-case problem, quantifying the price of robustness, choosing between RO and stochastic programming, and the adjustable-RO extension via affine decision rules. Use the framework below as a protocol: characterize the uncertainty, pick the set, derive the counterpart on paper, implement it as ordinary constraints, then validate the solution out of sample before recommending it.

## Initial Assessment

Establish these points before writing any model or code:

- **What is actually uncertain.** List the uncertain data by location: objective coefficients, constraint matrix entries, right-hand sides. The counterpart construction differs by location, and uncertain equality constraints are a special hazard (see Practical Challenges).
- **Consequence of violation.** If a violated constraint means an infeasible plan in the real system (capacity exceeded, safety margin broken, contract breached), RO with hard guarantees is appropriate. If violation only costs money, a stochastic or penalized model may serve better; see the RO-vs-SP protocol below.
- **Distribution knowledge.** Do you have a trusted distribution, only historical samples, only ranges, or only expert bounds? Ranges and bounds point to RO; a rich, trusted distribution points to stochastic programming (see stochastic-optimization).
- **Support of the uncertainty.** For each uncertain coefficient, identify nominal value and maximum deviation. If you cannot bound the deviation, you cannot write a meaningful uncertainty set; go back to the data first.
- **Correlation structure.** Independent coefficient deviations favor budget sets with probabilistic guarantees. Strong correlations favor ellipsoidal sets built from a covariance estimate, or a factor model inside a polyhedral set.
- **Problem class to preserve.** Box and budget sets keep an LP an LP and a MIP a MIP. Ellipsoidal sets turn them into SOCPs/MISOCPs. If the nominal model is a large MIP, prefer polyhedral sets so the branch-and-bound machinery is unaffected.
- **Decision dynamics.** Are all decisions made before uncertainty is revealed (static), or do some decisions adapt to observed values (multi-stage)? Static RO on a multi-stage problem is often needlessly conservative or even infeasible; plan for adjustable RO with decision rules.
- **Solver availability.** Gurobi handles LP/MIP/SOCP/MISOCP counterparts directly. If only an LP solver is available, restrict to polyhedral sets.
- **Conservatism budget.** Ask the stakeholder what objective degradation is acceptable (e.g., "at most 5% worse than nominal") and what violation probability is tolerable (e.g., 1 in 100). These two numbers calibrate the size parameter (Gamma or Omega) of the set.
- **Validation plan.** Decide how you will simulate realizations to estimate out-of-sample violation probability and cost. A robust model without an out-of-sample check is an unfinished deliverable.
- **Instance size.** The budget counterpart adds one variable and one constraint per uncertain coefficient plus one variable per robust row. Estimate the inflated model size before committing; a 10^6-coefficient uncertain matrix doubles the model.

## Uncertainty Sets and Robust Counterparts

### The uncertain LP and the worst-case principle

Consider an LP with row-wise uncertain constraint data:

$$ \min_x \; c^\top x \quad \text{s.t.} \quad a_i^\top x \le b_i \;\; \forall a_i \in U_i, \; i = 1, \dots, m $$

A solution $x$ is **robust feasible** if every constraint holds for every realization in its uncertainty set, equivalently

$$ \bar a_i^\top x + \max_{\zeta \in Z_i} \, (\Delta_i \zeta)^\top x \le b_i, $$

where the uncertain row is parameterized as $a_i = \bar a_i + \Delta_i \zeta$ with $\bar a_i$ the nominal row, $\Delta_i$ the deviation pattern, and $\zeta$ a primitive uncertainty vector living in a set $Z_i$. Two structural facts drive everything else:

1. **Constraint-wise decomposition.** For a static problem, robustifying each row against its own set is exact when the uncertainty set is a product across rows, and it is the standard (slightly conservative) treatment otherwise (Ben-Tal & Nemirovski 1999, "Robust solutions of uncertain linear programs"). You therefore derive counterparts one row at a time.
2. **The inner problem is linear in $\zeta$.** For fixed $x$, $\max_{\zeta \in Z_i} (\Delta_i \zeta)^\top x$ is an LP (polyhedral $Z_i$) or a norm maximization (ellipsoidal $Z_i$). Duality converts this inner maximization into a minimization, whose variables and constraints embed directly into the outer model. No max remains.

### The three standard sets

With scaled deviations $a_{ij} = \bar a_{ij} + \hat a_{ij} \zeta_j$, $\hat a_{ij} \ge 0$, and $J_i = \{j : \hat a_{ij} > 0\}$:

| Set | Definition of $Z_i$ | Worst-case term added to row $i$ | Counterpart class | Conservatism |
|---|---|---|---|---|
| Box (Soyster 1973) | $\|\zeta\|_\infty \le 1$ | $\sum_{j \in J_i} \hat a_{ij} \lvert x_j \rvert$ | LP / MIP | Maximal: every coefficient at its worst simultaneously |
| Budget (Bertsimas & Sim 2004) | $\|\zeta\|_\infty \le 1, \; \|\zeta\|_1 \le \Gamma_i$ | $\beta_i(x, \Gamma_i)$, see below | LP / MIP | Tunable: $\Gamma_i = 0$ nominal, $\Gamma_i = \lvert J_i \rvert$ box |
| Ellipsoid (Ben-Tal & Nemirovski 1998) | $\|\zeta\|_2 \le \Omega$ | $\Omega \, \lVert \hat a_i \circ x \rVert_2$ | SOCP / MISOCP | Tunable via $\Omega$; smooth, exploits cancellation |

Decision guidance:

- **Use box** when violations are catastrophic, the number of uncertain coefficients per row is small (so joint worst case is plausible), or you need the simplest possible model. Expect the largest objective degradation.
- **Use budget** as the default for LPs and MIPs. It models the empirical fact that not all coefficients deviate adversely at once, has a clean probabilistic guarantee under independence, keeps the problem class, and exposes one interpretable dial $\Gamma_i$ per row.
- **Use ellipsoidal** when deviations are approximately jointly normal or a covariance estimate is reliable, and the problem is continuous or a small MIP. It is the least conservative for a given probabilistic guarantee but costs you conic constraints inside branch-and-bound.

### The duality recipe (general polyhedral set)

Protocol for any polyhedral set $Z_i = \{\zeta : C\zeta \le d\}$ (this subsumes box and budget):

1. Write the robust requirement for one row: $\bar a_i^\top x + \sup_{\zeta : C\zeta \le d} x^\top \Delta_i \zeta \le b_i$.
2. The inner sup is an LP in $\zeta$. Its dual is $\min \{ d^\top w : C^\top w = \Delta_i^\top x, \; w \ge 0 \}$.
3. By LP strong duality (assuming $Z_i$ nonempty and bounded; see linear-programming-fundamentals), the sup equals the min. Replace the sup with the dual objective and **drop the min**: any dual-feasible $w$ certifies an upper bound on the worst case, and the outer model is already minimizing pressure on the row.
4. Embed: row $i$ becomes $\bar a_i^\top x + d^\top w_i \le b_i$, $C^\top w_i = \Delta_i^\top x$, $w_i \ge 0$, with a fresh dual vector $w_i$ per robust row.

The result is a deterministic LP/MIP, larger but of the same class. This recipe is the single most reusable tool in RO: whenever someone hands you a new polyhedral uncertainty set, you do not need a new theory, only this dualization.

### The budget set worked through

For $Z_i = \{\zeta : \lVert\zeta\rVert_\infty \le 1, \lVert\zeta\rVert_1 \le \Gamma_i\}$, the inner problem for fixed $x$ is

$$ \beta_i(x, \Gamma_i) = \max \Big\{ \sum_{j \in J_i} \hat a_{ij} \lvert x_j \rvert \, u_j \; : \; \sum_{j \in J_i} u_j \le \Gamma_i, \; 0 \le u_j \le 1 \Big\}, $$

whose LP dual (multiplier $z_i$ on the budget row, $p_{ij}$ on each $u_j \le 1$) gives the **Bertsimas-Sim counterpart** of row $i$:

$$ \sum_j \bar a_{ij} x_j + \Gamma_i z_i + \sum_{j \in J_i} p_{ij} \le b_i, \qquad z_i + p_{ij} \ge \hat a_{ij} \, y_j, \qquad -y_j \le x_j \le y_j, \qquad z_i, p_{ij} \ge 0. $$

Interpretation: $z_i$ is the protection price per unit of budget; $p_{ij}$ tops up coefficients whose individual worst-case impact $\hat a_{ij}\lvert x_j\rvert$ exceeds $z_i$. The inner LP has integral vertices, so fractional $\Gamma_i$ is meaningful: $\lfloor \Gamma_i \rfloor$ coefficients deviate fully and one deviates by the fraction $\Gamma_i - \lfloor \Gamma_i \rfloor$.

**Probabilistic guarantee.** If the scaled deviations $\zeta_j$ are independent and symmetrically distributed on $[-1, 1]$, Bertsimas & Sim (2004), "The price of robustness," bound the violation probability of the robust row by $\exp(-\Gamma_i^2 / (2\lvert J_i\rvert))$, with the sharper estimate $\Pr[\text{violation}] \lesssim 1 - \Phi\big((\Gamma_i - 1)/\sqrt{\lvert J_i \rvert}\,\big)$. Inverting the sharper form gives the standard sizing rule

$$ \Gamma_i \approx 1 + \Phi^{-1}(1 - \epsilon)\sqrt{\lvert J_i \rvert} $$

for a target violation probability $\epsilon$. For $\lvert J_i\rvert = 100$ and $\epsilon = 0.01$, $\Gamma_i \approx 1 + 2.33 \cdot 10 \approx 24$ — protecting against 24 of 100 simultaneous adverse deviations already yields a 99% guarantee. This sublinear growth is why budget sets are rarely much worse than nominal in objective value.

### Uncertainty elsewhere than the matrix

- **Objective coefficients.** Move the objective into a constraint with an epigraph variable: $\min \theta$ s.t. $c^\top x \le \theta$ for all $c \in U_c$, then robustify that single row with the same recipe.
- **Right-hand side.** Treat $b_i$ as the coefficient of a constant variable $x_{n+1} = -1$ appended to the row, or equivalently subtract the worst-case RHS deviation. For box uncertainty $b_i \in [\bar b_i - \hat b_i, \bar b_i + \hat b_i]$ on a $\le$ row, simply use $\bar b_i - \hat b_i$.
- **Equality constraints.** A row $a_i^\top x = b_i$ with uncertain $a_i$ has, in general, **no** static robust feasible $x$ except ones with $x_j = 0$ wherever $\hat a_{ij} > 0$. Eliminate the equality by substitution, model the underlying physics as two inequalities with slack, or move to adjustable RO where downstream variables absorb the realization.

## Robust Counterparts in Gurobi

The two builders below implement the box and budget counterparts as drop-in row constructors. They take the nominal row, the deviation vector, and the budget, and add only named variables and constraints, so they compose with any existing model (see milp-modeling-gurobi for the surrounding modeling discipline). If the affected variables are known nonnegative (e.g., binaries), pass them as `nonneg=True` to skip the absolute-value linearization.

```python
import gurobipy as gp
import numpy as np
from gurobipy import GRB


def _abs_envelope(
    model: gp.Model, x: list[gp.Var], idx: list[int], nonneg: bool, tag: str
) -> dict[int, gp.Var | gp.LinExpr]:
    """Return y_j >= |x_j| for j in idx; reuse x_j itself when x is nonnegative."""
    if nonneg:
        return {j: gp.LinExpr(x[j]) for j in idx}
    y = model.addVars(idx, lb=0.0, name=f"y_{tag}")
    model.addConstrs((x[j] <= y[j] for j in idx), name=f"absp_{tag}")
    model.addConstrs((-x[j] <= y[j] for j in idx), name=f"absn_{tag}")
    return dict(y)


def add_box_robust_row(
    model: gp.Model,
    x: list[gp.Var],
    a_bar: np.ndarray,
    a_hat: np.ndarray,
    rhs: float,
    tag: str,
    nonneg: bool = False,
) -> None:
    """Add the Soyster (box) counterpart of sum_j a_j x_j <= rhs,
    a_j in [a_bar_j - a_hat_j, a_bar_j + a_hat_j]."""
    n = len(x)
    idx = [j for j in range(n) if a_hat[j] > 0]
    y = _abs_envelope(model, x, idx, nonneg, tag)
    model.addConstr(
        gp.quicksum(a_bar[j] * x[j] for j in range(n))
        + gp.quicksum(a_hat[j] * y[j] for j in idx)
        <= rhs,
        name=f"box_{tag}",
    )


def add_budget_robust_row(
    model: gp.Model,
    x: list[gp.Var],
    a_bar: np.ndarray,
    a_hat: np.ndarray,
    rhs: float,
    gamma: float,
    tag: str,
    nonneg: bool = False,
) -> None:
    """Add the Bertsimas-Sim counterpart of sum_j a_j x_j <= rhs with budget gamma."""
    n = len(x)
    idx = [j for j in range(n) if a_hat[j] > 0]
    y = _abs_envelope(model, x, idx, nonneg, tag)
    z = model.addVar(lb=0.0, name=f"z_{tag}")
    p = model.addVars(idx, lb=0.0, name=f"p_{tag}")
    model.addConstrs(
        (z + p[j] >= a_hat[j] * y[j] for j in idx), name=f"prot_{tag}"
    )
    model.addConstr(
        gp.quicksum(a_bar[j] * x[j] for j in range(n)) + gamma * z + p.sum()
        <= rhs,
        name=f"budget_{tag}",
    )
```

A small production-planning demonstration: two products, two uncertain resource rows. The robust objective degrades monotonically as the uncertainty set grows from nominal ($\Gamma = 0$) through budget to box.

```python
import gurobipy as gp
import numpy as np
from gurobipy import GRB


def solve_production(kind: str, gamma: float = 1.0) -> float:
    """Solve max 8 x1 + 6 x2 under two uncertain resource rows; return objective."""
    a_bar = [np.array([2.0, 1.0]), np.array([1.0, 3.0])]
    a_hat = [np.array([0.4, 0.2]), np.array([0.2, 0.6])]
    rhs = [10.0, 15.0]
    m = gp.Model("production")
    m.Params.OutputFlag = 0
    x = [m.addVar(lb=0.0, name=f"x{j}") for j in range(2)]
    for i in range(2):
        if kind == "nominal":
            m.addConstr(gp.quicksum(a_bar[i][j] * x[j] for j in range(2)) <= rhs[i],
                        name=f"row{i}")
        elif kind == "box":
            # local copy of the builder pattern: x >= 0 here, so y_j = x_j
            m.addConstr(gp.quicksum((a_bar[i][j] + a_hat[i][j]) * x[j]
                                    for j in range(2)) <= rhs[i], name=f"row{i}")
        else:  # budget
            z = m.addVar(lb=0.0, name=f"z{i}")
            p = m.addVars(2, lb=0.0, name=f"p{i}")
            m.addConstrs((z + p[j] >= a_hat[i][j] * x[j] for j in range(2)),
                         name=f"prot{i}")
            m.addConstr(gp.quicksum(a_bar[i][j] * x[j] for j in range(2))
                        + gamma * z + p.sum() <= rhs[i], name=f"row{i}")
    m.setObjective(8.0 * x[0] + 6.0 * x[1], GRB.MAXIMIZE)
    m.optimize()
    assert m.Status == GRB.OPTIMAL
    return m.ObjVal


for kind in ("nominal", "budget", "box"):
    print(f"{kind:8s} objective = {solve_production(kind):.2f}")
# Expected: nominal 48.00, budget (Gamma=1) 42.41, box 40.00 —
# the budget solution recovers part of the box solution's lost profit
# while still protecting against any single worst-case coefficient per row.
```

Reading the output is part of the method: the gap nominal-to-box is the **maximum** price of full protection; the budget row lets you buy back a controlled fraction of it. Never report the robust objective alone — always next to the nominal one.

## End-to-End Example: Robust Knapsack and the Price of Robustness

This is the canonical study from Bertsimas & Sim (2004), reproduced as a complete protocol: build the counterpart, sweep $\Gamma$, and validate each solution by simulation. The 0-1 knapsack (see knapsack-problems for the problem family) has profits $p_j$, uncertain weights $w_j \in [\bar w_j - \hat w_j, \bar w_j + \hat w_j]$, and capacity $C$:

$$ \max \Big\{ p^\top x \; : \; \sum_j \bar w_j x_j + \beta(x, \Gamma) \le C, \; x \in \{0,1\}^n \Big\}. $$

Because $x \ge 0$, the absolute-value envelope is just $x$ itself and the counterpart stays a compact MIP. The study reports, for each $\Gamma$: the objective, the **price of robustness** $(z_{nom} - z_{rob})/z_{nom}$, the simulated violation probability, and the theoretical bound. The deliverable is the table; the recommendation is the smallest $\Gamma$ whose empirical violation rate meets the target.

```python
import math

import gurobipy as gp
import numpy as np
import pandas as pd
from gurobipy import GRB


def solve_robust_knapsack(
    profit: np.ndarray,
    w_bar: np.ndarray,
    w_hat: np.ndarray,
    capacity: float,
    gamma: float,
) -> tuple[float, np.ndarray]:
    """Solve the Bertsimas-Sim robust 0-1 knapsack; return (objective, selection)."""
    n = profit.size
    m = gp.Model("robust_knapsack")
    m.Params.OutputFlag = 0
    x = m.addVars(n, vtype=GRB.BINARY, name="x")
    z = m.addVar(lb=0.0, name="z")
    p = m.addVars(n, lb=0.0, name="p")
    m.addConstrs((z + p[j] >= w_hat[j] * x[j] for j in range(n)), name="prot")
    m.addConstr(
        gp.quicksum(w_bar[j] * x[j] for j in range(n)) + gamma * z + p.sum()
        <= capacity,
        name="capacity",
    )
    m.setObjective(gp.quicksum(profit[j] * x[j] for j in range(n)), GRB.MAXIMIZE)
    m.optimize()
    assert m.Status == GRB.OPTIMAL
    sel = np.array([x[j].X > 0.5 for j in range(n)], dtype=float)
    return m.ObjVal, sel


def violation_rate(
    sel: np.ndarray,
    w_bar: np.ndarray,
    w_hat: np.ndarray,
    capacity: float,
    n_samples: int,
    seed: int,
) -> float:
    """Monte Carlo estimate of P(realized weight of the selection exceeds capacity)."""
    rng = np.random.default_rng(seed)
    zeta = rng.uniform(-1.0, 1.0, size=(n_samples, w_bar.size))
    realized = (w_bar + w_hat * zeta) @ sel
    return float(np.mean(realized > capacity))


def bound_violation(gamma: float, n_uncertain: int) -> float:
    """Bertsimas-Sim normal approximation: 1 - Phi((gamma - 1) / sqrt(n))."""
    if gamma <= 0.0:
        return 1.0
    t = (gamma - 1.0) / math.sqrt(n_uncertain)
    return 0.5 * (1.0 - math.erf(t / math.sqrt(2.0)))


def price_of_robustness_study(seed: int = 7) -> pd.DataFrame:
    """Sweep Gamma on one random knapsack; report objective, price, violation."""
    rng = np.random.default_rng(seed)
    n = 30
    profit = rng.integers(20, 80, n).astype(float)
    w_bar = rng.integers(10, 40, n).astype(float)
    w_hat = 0.2 * w_bar
    capacity = 0.5 * float(w_bar.sum())
    z_nom, _ = solve_robust_knapsack(profit, w_bar, w_hat, capacity, gamma=0.0)
    rows = []
    for gamma in (0.0, 1.0, 2.0, 3.0, 5.0, 8.0, 12.0, 20.0, 30.0):
        obj, sel = solve_robust_knapsack(profit, w_bar, w_hat, capacity, gamma)
        rows.append({
            "gamma": gamma,
            "objective": obj,
            "price_%": 100.0 * (z_nom - obj) / z_nom,
            "violation_%": 100.0 * violation_rate(
                sel, w_bar, w_hat, capacity, n_samples=20_000, seed=seed + 1),
            "bound_%": 100.0 * bound_violation(gamma, n),
        })
    return pd.DataFrame(rows)


df = price_of_robustness_study()
print(df.to_string(index=False, float_format=lambda v: f"{v:8.2f}"))
# Expected: objective is non-increasing in gamma; empirical violation falls from
# roughly a third at gamma=0 to 0% well before gamma=30, always below the
# normal-approximation bound; the price of robustness grows sublinearly and
# flattens once gamma protects the few items with the largest w_hat * x_j.
```

Three methodological points the table should make explicit in any write-up:

- **The bound is loose; the simulation is the evidence.** Recommend $\Gamma$ from the empirical column, and quote the bound only as the distribution-free guarantee.
- **The violation estimate is conditional on the deviation model.** The simulation above samples uniform $\zeta$; rerun it with the deviation distribution the stakeholder believes in (or bootstrap historical deviations). The robust feasibility certificate holds for any distribution supported on the set; the probability numbers do not.
- **Most protection is bought cheaply.** Typically the first few units of $\Gamma$ collapse the violation probability while costing a small share of profit; quantify that knee point — it is the main managerial output of the study.

## RO versus Stochastic Programming: Decision Protocol

RO and stochastic programming (SP) answer different questions about the same uncertain data. SP optimizes an expectation (or risk measure) over a known distribution and treats constraint violation through recourse costs or chance constraints; RO guarantees feasibility for every realization in a set and optimizes the worst case. Choosing between them is a modeling decision, not a taste decision. Work through this tree with the stakeholder:

```text
1. Is constraint violation acceptable at a price (recourse, penalty, lost sales)?
   ├─ NO, violation is unacceptable (safety, physical, contractual)
   │    └─> RO on those constraints. Go to 4 to size the set.
   └─ YES -> 2
2. Do you trust a distribution (fitted, simulated, or rich historical sample)?
   ├─ NO, only ranges / few samples / regime changes expected
   │    └─> RO (or distributionally robust; see Advanced Techniques).
   └─ YES -> 3
3. Is the decision repeated many times so averages are the right target?
   ├─ YES -> SP: two-stage with recourse, SAA over scenarios
   │         (see stochastic-optimization). Consider CVaR if tails matter.
   └─ NO, one-shot or career-risk decision
        └─> Worst-case reasoning still relevant: RO, or SP with CVaR at
            high confidence; compare both out of sample.
4. Sizing the RO set: get (a) tolerable violation probability epsilon,
   (b) tolerable objective degradation vs nominal. Sweep Gamma/Omega,
   simulate, and pick the smallest set meeting (a) within budget (b).
   If no Gamma meets both -> the requirements are inconsistent; renegotiate.
```

| Criterion | Robust optimization | Stochastic programming |
|---|---|---|
| Input needed | Support/ranges of the data | Distribution or scenario set |
| Guarantee | Feasibility for all realizations in the set | Optimal expectation; violations possible |
| Objective | Worst case (or worst-case regret) | Expected value, possibly CVaR |
| Model growth | Polynomial, modest (dual variables per row) | Linear in scenario count; can explode |
| Problem class | Preserved (polyhedral sets) | Preserved, but scenario count is the cost |
| Conservatism control | Set size ($\Gamma$, $\Omega$) | Risk measure, chance-constraint level |
| Fails when | Set badly calibrated; deviations correlated across rows | Distribution misspecified; tails underestimated |

The honest comparison is empirical: solve both models, then evaluate **both** solutions on the same out-of-sample realizations. The harness below does this for the knapsack of the previous section against a scenario-feasibility (SAA-style) model that enforces the capacity on $K$ sampled weight vectors — a common SP-flavored surrogate when feasibility, not cost, is the issue.

```python
import gurobipy as gp
import numpy as np
from gurobipy import GRB


def solve_scenario_knapsack(
    profit: np.ndarray, weight_scn: np.ndarray, capacity: float
) -> tuple[float, np.ndarray]:
    """Max profit s.t. capacity holds in every training scenario (rows of weight_scn)."""
    k, n = weight_scn.shape
    m = gp.Model("scenario_knapsack")
    m.Params.OutputFlag = 0
    x = m.addVars(n, vtype=GRB.BINARY, name="x")
    m.addConstrs(
        (gp.quicksum(weight_scn[s, j] * x[j] for j in range(n)) <= capacity
         for s in range(k)),
        name="cap_scn",
    )
    m.setObjective(gp.quicksum(profit[j] * x[j] for j in range(n)), GRB.MAXIMIZE)
    m.optimize()
    assert m.Status == GRB.OPTIMAL
    return m.ObjVal, np.array([x[j].X > 0.5 for j in range(n)], dtype=float)


def solve_budget_knapsack(
    profit: np.ndarray, w_bar: np.ndarray, w_hat: np.ndarray,
    capacity: float, gamma: float,
) -> tuple[float, np.ndarray]:
    """Bertsimas-Sim robust knapsack (x >= 0 so the envelope is x itself)."""
    n = profit.size
    m = gp.Model("budget_knapsack")
    m.Params.OutputFlag = 0
    x = m.addVars(n, vtype=GRB.BINARY, name="x")
    z = m.addVar(lb=0.0, name="z")
    p = m.addVars(n, lb=0.0, name="p")
    m.addConstrs((z + p[j] >= w_hat[j] * x[j] for j in range(n)), name="prot")
    m.addConstr(gp.quicksum(w_bar[j] * x[j] for j in range(n))
                + gamma * z + p.sum() <= capacity, name="cap")
    m.setObjective(gp.quicksum(profit[j] * x[j] for j in range(n)), GRB.MAXIMIZE)
    m.optimize()
    assert m.Status == GRB.OPTIMAL
    return m.ObjVal, np.array([x[j].X > 0.5 for j in range(n)], dtype=float)


def compare_out_of_sample(seed: int = 11) -> None:
    """Train scenario and robust models, then test both on fresh realizations."""
    rng = np.random.default_rng(seed)
    n, k_train, k_test = 30, 100, 20_000
    profit = rng.integers(20, 80, n).astype(float)
    w_bar = rng.integers(10, 40, n).astype(float)
    w_hat = 0.2 * w_bar
    capacity = 0.5 * float(w_bar.sum())
    train = w_bar + w_hat * rng.uniform(-1.0, 1.0, size=(k_train, n))
    test = w_bar + w_hat * rng.uniform(-1.0, 1.0, size=(k_test, n))
    gamma = 1.0 + 2.326 * np.sqrt(n)  # target epsilon ~ 1%
    for label, (obj, sel) in {
        "scenario(K=100)": solve_scenario_knapsack(profit, train, capacity),
        f"budget(G={gamma:.1f})": solve_budget_knapsack(
            profit, w_bar, w_hat, capacity, gamma),
    }.items():
        viol = float(np.mean(test @ sel > capacity))
        print(f"{label:18s} profit={obj:8.1f}  oos_violation={100 * viol:5.2f}%")


compare_out_of_sample()
# Expected: the scenario model earns a higher profit but shows a nonzero
# out-of-sample violation rate (it only saw 100 scenarios); the budget model
# earns slightly less and violates (essentially) never. Neither dominates:
# report both lines and let the violation tolerance decide.
```

Report this comparison even when the stakeholder asked for only one method. If the scenario model's out-of-sample violation is acceptable and its profit is materially higher, recommending RO would cost real money for unneeded protection; the reverse mistake ships a fragile plan.

## Adjustable Robust Optimization (Sketch)

Static RO forces every decision before any uncertainty resolves. In multi-period problems this is both wrong as a model of reality and a source of severe conservatism — often outright infeasibility. **Adjustable RO** (Ben-Tal, Goryashko, Guslitzer & Nemirovski 2004, "Adjustable robust solutions of uncertain linear programs") lets later decisions be functions of observed data: $y = y(\zeta)$. Optimizing over arbitrary functions is intractable (the fully adjustable problem is NP-hard already for polyhedral sets), so the workhorse restriction is the **affine decision rule** (AARC):

$$ y_t(\zeta) = y_t^0 + \sum_{s \in \text{obs}(t)} Y_{ts} \, \zeta_s, $$

where $\text{obs}(t)$ indexes the uncertainty observed before decision $t$ (the information base — getting this index set right is the modeling step that matters most). Substituting the rule makes every constraint affine in $\zeta$ again, with coefficients that are now linear in the decision variables $(y^0, Y)$, so the same counterpart recipe applies. Under fixed recourse and box uncertainty, "for all $\zeta$" of an affine row needs only absolute values of decision-linear coefficients, handled by auxiliary variables.

The classic demonstration is multi-period inventory: order quantities adapt to demand already observed. The instance below is built so that the **static** counterpart is infeasible — total worst-case demand exceeds what the inventory cap allows you to pre-commit — while the affine policy absorbs the spread.

```python
import gurobipy as gp
import numpy as np
from gurobipy import GRB


def add_box_le(
    model: gp.Model,
    const: gp.LinExpr,
    coefs: list[gp.LinExpr],
    mid: np.ndarray,
    dev: np.ndarray,
    ub: float,
    tag: str,
) -> None:
    """Enforce const + sum_s coefs[s] * d_s <= ub for all d_s in [mid-dev, mid+dev].

    const and each coefs[s] are linear expressions in the decision variables.
    Worst case over the box: const + sum_s (mid_s coefs[s] + dev_s |coefs[s]|).
    """
    T = len(coefs)
    w = model.addVars(T, lb=0.0, name=f"w_{tag}")
    for s in range(T):
        model.addConstr(w[s] >= coefs[s], name=f"wp_{tag}_{s}")
        model.addConstr(w[s] >= -1.0 * coefs[s], name=f"wn_{tag}_{s}")
    model.addConstr(
        const + gp.quicksum(mid[s] * coefs[s] + dev[s] * w[s] for s in range(T))
        <= ub,
        name=f"box_{tag}",
    )


def solve_affine_inventory(
    d_bar: np.ndarray, rho: float, cost: np.ndarray,
    q_max: float, i_max: float, adjustable: bool,
) -> tuple[int, float]:
    """Min worst-case ordering cost; orders q_t = q0_t + sum_{s<t} Q_ts d_s.

    Demand d_t in [d_bar (1-rho), d_bar (1+rho)]; inventory must stay in
    [0, i_max] for every demand path; returns (status, objective or nan).
    """
    T = d_bar.size
    mid, dev = d_bar.copy(), rho * d_bar
    m = gp.Model("aarc_inventory")
    m.Params.OutputFlag = 0
    m.Params.DualReductions = 0  # report INFEASIBLE, never INF_OR_UNBD
    q0 = m.addVars(T, lb=-GRB.INFINITY, name="q0")
    Q = m.addVars(T, T, lb=-GRB.INFINITY, name="Q")
    for t in range(T):
        for s in range(T):
            if s >= t or not adjustable:  # information base: only past demands
                Q[t, s].LB = Q[t, s].UB = 0.0
    theta = m.addVar(lb=-GRB.INFINITY, name="theta")

    def q_terms(t: int) -> tuple[gp.LinExpr, list[gp.LinExpr]]:
        return gp.LinExpr(q0[t]), [gp.LinExpr(Q[t, s]) for s in range(T)]

    for t in range(T):  # 0 <= q_t(d) <= q_max for all d
        const, coefs = q_terms(t)
        add_box_le(m, const, coefs, mid, dev, q_max, f"qub{t}")
        add_box_le(m, -1.0 * const, [-1.0 * e for e in coefs], mid, dev, 0.0,
                   f"qlb{t}")
    for t in range(T):  # 0 <= I_t(d) <= i_max, I_t = sum_{u<=t} (q_u - d_u)
        const = gp.quicksum(q0[u] for u in range(t + 1))
        coefs = [gp.quicksum(Q[u, s] for u in range(t + 1))
                 - (1.0 if s <= t else 0.0) for s in range(T)]
        add_box_le(m, const, coefs, mid, dev, i_max, f"iub{t}")
        add_box_le(m, -1.0 * const, [-1.0 * e for e in coefs], mid, dev, 0.0,
                   f"ilb{t}")
    cost_const = gp.quicksum(cost[t] * q0[t] for t in range(T))  # theta >= cost(d)
    cost_coefs = [gp.quicksum(cost[t] * Q[t, s] for t in range(T))
                  for s in range(T)]
    add_box_le(m, cost_const - theta, cost_coefs, mid, dev, 0.0, "cost")

    m.setObjective(theta, GRB.MINIMIZE)
    m.optimize()
    obj = m.ObjVal if m.Status == GRB.OPTIMAL else float("nan")
    return m.Status, obj


d_bar = np.array([20.0, 30.0, 50.0, 60.0, 40.0, 30.0])
cost = np.array([1.0, 1.5, 1.2, 1.8, 1.1, 1.6])
for adjustable in (False, True):
    status, obj = solve_affine_inventory(
        d_bar, rho=0.25, cost=cost, q_max=80.0, i_max=60.0,
        adjustable=adjustable)
    label = "affine " if adjustable else "static "
    print(f"{label} status={status}  worst-case cost={obj:.2f}")
# Expected: static prints status=3 (GRB.INFEASIBLE, cost=nan) — committing all
# orders upfront cannot keep inventory in [0, 60] for both the highest and the
# lowest demand path. The affine policy is feasible with worst-case cost 350.50:
# adjustability is a feasibility mechanism here, not just a cost saver.
```

What to know before reaching for AARC, and what to flag in a deliverable:

- **Affine rules are a restriction**, so the AARC value upper-bounds (for minimization) the fully adjustable optimum. For two-stage problems with simplex-type or box uncertainty there are cases where affine rules are provably optimal (Bertsimas & Goyal 2012); in general they are a strong, cheap heuristic with a certificate.
- **Model growth is quadratic-ish**: $O(T^2)$ rule coefficients and one absolute-value envelope per robust row per uncertainty component. Exploit sparsity by restricting rules to a rolling window of recent observations when $T$ is large.
- **State variables (inventory) need no rule of their own** when they are linear in decisions and data, as above; substitute them out. Give rules only to genuine recourse decisions.
- **Integer recourse breaks AARC** (an affine rule cannot output binaries). Standard escapes: keep first-stage variables integer and recourse continuous; piecewise-constant rules on a partition of the set; or column-and-constraint generation (Zeng & Zhao 2013), which solves a growing master over worst-case scenarios — that algorithm pairs naturally with the decomposition material in stochastic-optimization.

## Advanced Techniques

### Ellipsoidal sets and SOCP counterparts

For $Z_i = \{\zeta : \lVert\zeta\rVert_2 \le \Omega\}$ the inner maximization is a norm: $\max_{\lVert\zeta\rVert_2 \le \Omega} (\hat a_i \circ \zeta)^\top x = \Omega \lVert \hat a_i \circ x \rVert_2$ (Cauchy-Schwarz, tight). The robust row $\bar a_i^\top x + \Omega \lVert \hat a_i \circ x \rVert_2 \le b_i$ is a second-order cone constraint; with a covariance estimate $\Sigma$ of the row, use $\bar a_i^\top x + \Omega \lVert \Sigma^{1/2} x \rVert_2 \le b_i$. The violation guarantee under independent symmetric bounded deviations is $\exp(-\Omega^2/2)$ — note it does not depend on $\lvert J_i \rvert$, which is why ellipsoids win when rows are long. In Gurobi, lift the norm with $u = \Sigma^{1/2} x$, a nonnegative scalar $t$, and the SOC-shaped quadratic constraint $u^\top u \le t^2$:

```python
import gurobipy as gp
import numpy as np
from gurobipy import GRB


def add_ellipsoidal_robust_row(
    model: gp.Model,
    x: list[gp.Var],
    a_bar: np.ndarray,
    sigma_half: np.ndarray,
    omega: float,
    rhs: float,
    tag: str,
) -> None:
    """Add a_bar^T x + omega * ||sigma_half @ x||_2 <= rhs as an SOC constraint."""
    n = len(x)
    u = model.addVars(n, lb=-GRB.INFINITY, name=f"u_{tag}")
    t = model.addVar(lb=0.0, name=f"t_{tag}")
    model.addConstrs(
        (u[k] == gp.quicksum(sigma_half[k, j] * x[j] for j in range(n))
         for k in range(n)),
        name=f"lift_{tag}",
    )
    model.addConstr(  # Gurobi recognizes u'u <= t^2 with t >= 0 as SOC
        gp.quicksum(u[k] * u[k] for k in range(n)) <= t * t, name=f"soc_{tag}"
    )
    model.addConstr(
        gp.quicksum(a_bar[j] * x[j] for j in range(n)) + omega * t <= rhs,
        name=f"lin_{tag}",
    )


m = gp.Model("ellipsoid_demo")  # max x1 + x2, one row with correlated deviations
m.Params.OutputFlag = 0
x = [m.addVar(lb=0.0, name=f"x{j}") for j in range(2)]
add_ellipsoidal_robust_row(
    m, x, a_bar=np.array([1.0, 1.0]),
    sigma_half=np.array([[0.30, 0.10], [0.10, 0.20]]),
    omega=2.0, rhs=10.0, tag="r0",
)
m.setObjective(x[0] + x[1], GRB.MAXIMIZE)
m.optimize()
assert m.Status == GRB.OPTIMAL
print(f"x = ({x[0].X:.3f}, {x[1].X:.3f}), robust objective = {m.ObjVal:.3f}")
# Expected: objective ~6.9 versus nominal 10.0, with weight shifted toward x2
# (the variable with the smaller deviation column of sigma_half).
```

Reserve ellipsoidal counterparts for continuous models or MIPs with few integers — conic relaxations inside branch-and-bound are markedly slower than LPs.

### Calibrating the set from data

The deviation magnitudes $\hat a_{ij}$ are as decision-relevant as $\Gamma$. Protocol: (1) collect historical realizations of each coefficient; (2) set $\bar a_{ij}$ to the median, $\hat a_{ij}$ to a high empirical quantile of $\lvert a_{ij} - \bar a_{ij}\rvert$ (e.g., the 95th) rather than the absolute maximum, which is noise-dominated; (3) choose $\Gamma$ by the sizing rule, then (4) validate the *pair* $(\hat a, \Gamma)$ by out-of-sample simulation against held-out data, exactly as in the knapsack study. If coefficients co-move, fit a low-rank factor model $a_i = \bar a_i + F\eta$ and put the box/budget set on the factors $\eta$ — fewer primitive uncertainties, tighter sets, same counterpart machinery.

### Distributionally robust optimization (positioning)

DRO optimizes the worst case over a family of distributions — moment-based (known mean/covariance; Delage & Ye 2010) or statistical-distance balls around the empirical distribution (Wasserstein; Mohajerin Esfahani & Kuhn 2018). It interpolates between SP (singleton family) and RO (all distributions on a support). Practically: Wasserstein DRO of many losses reduces to convex programs barely larger than the SAA, and moment-based chance constraints reduce to SOC constraints structurally identical to the ellipsoidal counterpart above. If the stakeholder objects "the worst case in your set is absurd, but I do not trust my scenario fit either," DRO is the answer; treat it as RO over a lifted set and reuse this skill's recipe.

### Worst-case regret and soft robustness

Two relaxations of min-max cost reduce conservatism without abandoning guarantees. **Min-max regret** minimizes $\max_{u \in U} [ c(x, u) - c^*(u) ]$, the gap to the best decision in hindsight; for interval objective uncertainty in combinatorial problems, regret counterparts are harder (often $\Sigma_2^p$-flavored) and are attacked by row generation: alternate between a master over candidate scenarios and a worst-case-regret separation problem. **Light robustness** (Fischetti & Monaci 2009) fixes a maximum allowed objective degradation versus nominal and then minimizes the protection slack that must be given up — useful when the budget on degradation, not the violation probability, is the binding managerial input.

### Row generation instead of monolithic counterparts

When the uncertainty set is complicated (many facets, combinatorial structure) or the counterpart bloats memory, do not dualize — separate. Keep the nominal model; iteratively (1) solve it, (2) for each robust row solve the inner maximization at the current $x^*$ to find the worst realization, (3) if violated, add the realized constraint $a^\top x \le b_i$ as a plain cut and resolve. This "cutting-set" / adversarial method (Mutapcic & Boyd 2009) converges finitely for polyhedral sets, parallels Benders-style row generation, and is the only practical route when the inner problem is itself a MIP. It also drops into Gurobi callbacks as lazy constraints (see milp-modeling-gurobi).

## Practical Challenges

**The robust counterpart is infeasible.** First check uncertain equality constraints — they admit essentially no static robust solution; substitute them out or split with slack. Then check whether the set is unintentionally huge ($\hat a$ from absolute extremes, $\Gamma$ at the box limit, RHS robustified on both sides). If genuinely infeasible at the required protection level, the finding is real and valuable: the system lacks the flexibility to absorb the stated uncertainty. Escalate to adjustable RO before shrinking the set silently.

**The robust solution looks absurdly conservative.** Diagnose by decomposing the protection term row by row: report $\Gamma_i z_i + \sum_j p_{ij}$ next to the slack of each row at the nominal solution. Usual culprits: deviations $\hat a$ set to worst-ever observations, all rows robustified when only two matter, or independent-deviation budget sets applied to strongly correlated data (use a factor model). The price-of-robustness sweep is the systematic fix — never pick a single $\Gamma$ blind.

**Equality constraints with uncertain coefficients.** A flow-balance row $\sum_j a_{ij} x_j = b_i$ with uncertain $a$ forces $x_j = 0$ on every uncertain coefficient in any static robust solution. Re-model: eliminate the equality by variable substitution, question whether the physics is really equality (often it is "at least demand, inventory absorbs the rest"), or make downstream variables adjustable so the equality defines them per realization.

**Absolute-value envelope used where it is not tight.** The linearization $-y_j \le x_j \le y_j$ only enforces $y_j \ge \lvert x_j\rvert$. In the counterpart this is safe — protection pressure pushes $y$ down onto $\lvert x \rvert$ — but if you reuse $y_j$ elsewhere with a sign that rewards larger $y_j$, the model is wrong. Keep envelope variables private to the robust row that created them, and skip them entirely for variables with known sign.

**Reporting the robust objective as the expected outcome.** The robust objective is a worst-case-over-the-set figure, not a forecast. Stakeholders anchor on it and conclude robustness is unaffordable. Always report the triple: nominal objective, robust objective (the guarantee), and the simulated average performance of the robust solution — the last is typically close to nominal, which is the persuasive number.

**$\Gamma$ chosen per model instead of per row.** The guarantee $1 - \Phi((\Gamma_i - 1)/\sqrt{\lvert J_i\rvert})$ is per row and depends on the row's count of uncertain coefficients. A single global $\Gamma$ over-protects short rows and under-protects long ones. Size each $\Gamma_i$ from its own $\lvert J_i \rvert$ and its own violation tolerance; rows encoding soft preferences can take much larger $\epsilon$ than safety rows.

**The MIP slows down badly after robustification.** Budget counterparts preserve linearity but the protection rows ($z + p_j \ge \hat a_j y_j$) weaken the LP relaxation, and ellipsoidal counterparts force conic branch-and-bound. Mitigations: robustify only binding-risk rows; warm-start from the nominal solution; for the budget knapsack family, use the Bertsimas-Sim decomposition result — the robust problem solves as $\lvert J\rvert + 1$ nominal problems with modified coefficients, one per candidate value of the critical $\hat a_{j} \lvert x_j \rvert$ threshold — preserving any specialized combinatorial algorithm.

**Simulation contradicts the guarantee.** If out-of-sample violations exceed the bound, the realizations are leaving the uncertainty set: deviations larger than $\hat a$, asymmetric distributions (the bound assumes symmetry), or cross-row correlation concentrating bad luck. Recalibrate the set from the same data used for simulation, and state the support assumption explicitly in the report. The certificate is only as good as the set.

## Tools & Libraries

| Library | When to use | Note |
|---|---|---|
| gurobipy | Hand-built counterparts in production models | Full control and named constraints; budget RC stays LP/MIP; see milp-modeling-gurobi |
| RSOME | Algebraic RO/DRO modeling in Python | Declares sets and decision rules directly; generates the counterpart for you; good for AARC prototyping |
| Pyomo + PyROS | Robustifying nonconvex/nonlinear Pyomo models | Implements the iterative cutting-set method, not dualization; solver-agnostic |
| ROmodel | Polyhedral/ellipsoidal RO inside Pyomo | Lightweight uncertainty-set annotations on existing Pyomo models |
| cvxpy | Quick SOCP counterparts, research prototypes | Write the norm term literally; not ideal for large MIPs |
| numpy | Monte Carlo validation, set calibration | `np.random.default_rng(seed)`; vectorize realization sampling |
| pandas | Gamma sweeps, out-of-sample comparison tables | The deliverable tables in this skill are DataFrames |

## Output Format

A complete robust-optimization deliverable contains:

1. **Uncertainty model statement.** A table of uncertain coefficients: location (row/column), nominal value source, deviation magnitude source (quantile of data, expert bound), assumed support and symmetry, correlation treatment. This table is the audit trail for the whole study.
2. **Counterpart derivation.** One worked row showing the dualization, so a reviewer can verify the implementation against the math. Name the set (box / budget with $\Gamma_i$ / ellipsoid with $\Omega$) per constraint family.
3. **Model summary table.** Rows robustified, set type and size parameter per row family, added variables/constraints, final model dimensions, solve time vs nominal.
4. **Price-of-robustness sweep.** The $\Gamma$ (or $\Omega$) sweep table: objective, price vs nominal in %, simulated violation %, theoretical bound % — as in the knapsack study. Recommend a specific value with one sentence of justification tied to the stakeholder's $\epsilon$ and degradation budget.
5. **Out-of-sample validation.** Sample size, sampling distribution and its relation to the set, violation rates and average/worst realized objective for: nominal solution, recommended robust solution, and (if built) the stochastic-programming alternative.
6. **Solution diff.** What structurally changes versus the nominal plan (items dropped, capacity reserved, orders shifted) — robustness recommendations are adopted when the structural change is explainable.
7. **Artifacts.** Reproducible script with seeds, the counterpart-builder module, and the sweep results as CSV; for adjustable models, the decision-rule coefficients $(y^0, Y)$ exported so operations can evaluate the policy on realized data.

## Questions to Ask

- Which numbers in the model are actually uncertain, and what do you have on them: ranges, history, a distribution, or expert judgment?
- What happens in reality if this constraint is violated — a cost, a renegotiation, or an unacceptable failure?
- What violation probability is tolerable, per constraint family? Is 1-in-20 fine for some rows and 1-in-1000 required for others?
- How much objective degradation versus the nominal plan is acceptable to buy protection?
- Are all decisions committed now, or do some adapt after demand/prices/yields are observed (and in what order)?
- Do the uncertain coefficients move together (common drivers, seasonality), or roughly independently?
- Is the nominal model an LP or a MIP, how large, and what solve time is acceptable after the model grows?
- Do you need a distribution-free guarantee for a regulator/auditor, or is empirical out-of-sample performance the standard of proof?
- Will this decision be re-optimized regularly (rolling horizon) — making adjustable rules or simple recourse more relevant than static worst-case planning?

## Related Skills

- **stochastic-optimization** — when a trusted distribution or scenario set exists and expected-value (or CVaR) optimization with recourse fits the decision better than worst-case guarantees; also for the SAA machinery used in the comparison protocol here.
- **milp-modeling-gurobi** — when implementing the counterparts: constraint-builder discipline, named constraints, lazy-constraint callbacks for the cutting-set method, and warm starts for the robustified MIP.
- **linear-programming-fundamentals** — when the duality step in the counterpart derivation needs grounding: LP duality, strong duality conditions, and reading dual variables as protection prices.
- **knapsack-problems** — when the uncertain-weight knapsack of the worked example is the actual application, or when specialized knapsack algorithms should be preserved via the Bertsimas-Sim decomposition into nominal subproblems.
