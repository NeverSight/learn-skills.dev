---
name: stochastic-optimization
description: When the user wants to optimize decisions under uncertainty with two-stage stochastic programming — extensive (deterministic-equivalent) form in Gurobi, scenario generation and reduction, sample average approximation (SAA), and EVPI/VSS analysis. Also use when the user mentions "stochastic programming," "two-stage," "scenarios," "SAA," "recourse," "uncertainty in demand," or when decisions split into here-and-now and wait-and-see stages. For L-shaped decomposition of large scenario models, see benders-decomposition; for distribution-free worst-case models, see robust-optimization.
---

# Stochastic Optimization

You are an expert in stochastic programming for combinatorial and mixed-integer optimization. This skill covers the full methodology of a two-stage stochastic study: deciding whether uncertainty must be modeled at all, building the extensive form in Gurobi, generating and reducing scenarios, quantifying the value of the stochastic model (EVPI, VSS), and running the sample average approximation (SAA) protocol with statistically valid optimality gaps. Use the decision trees and protocols below to structure the study, and the worked capacity-planning example as the implementation template. The canonical references are Birge & Louveaux (2011), "Introduction to Stochastic Programming," and Shapiro, Dentcheva & Ruszczyński (2009), "Lectures on Stochastic Programming."

## Initial Assessment

Establish these facts before writing any model. Most failed stochastic studies skipped one of them.

- **Identify exactly which parameters are random.** Demand, prices, yields, travel times, capacities, failures. Everything else is deterministic data — do not blur the two.
- **Locate the source of the distribution.** Historical observations, a fitted parametric model, expert ranges, or a simulator. No credible distribution at all is a signal to consider robust optimization instead.
- **Establish the stage structure.** Which decisions are made before the uncertainty is observed (here-and-now), and which can react afterwards (wait-and-see)? A problem with no recourse decisions is a chance-constrained or robust problem, not a two-stage program.
- **Check recourse completeness.** Is the second stage feasible for every first-stage decision and every outcome? If not, decide now between penalized slack variables (complete recourse by construction) and feasibility cuts later.
- **Locate the integer variables.** Integers only in the first stage keep the L-shaped method available; integers in the second stage restrict you to the extensive form, integer L-shaped, or progressive hedging.
- **Estimate the extensive-form size.** Rows ≈ first-stage rows + S × second-stage rows; columns likewise. This single estimate decides extensive form vs decomposition vs SAA.
- **Fix the scenario budget.** How many scenarios can you solve within the time budget? Run a 2-minute timing test on 10, 50, 100 scenarios before promising anything.
- **Establish the risk attitude.** Expected cost only, or do rare bad outcomes matter? Risk aversion changes the objective (mean-CVaR) and raises the scenario count needed to resolve the tail.
- **Check for dependence among random parameters.** Correlated demands or common shocks must survive scenario generation; independent sampling of correlated quantities silently destroys the problem.
- **Reserve out-of-sample data.** Keep an evaluation sample (or holdout years of history) that is never used to optimize. All reported performance comes from this sample.
- **Clarify how the decision is used.** One-shot strategic decision (capacity, location) fits two-stage; a decision re-made every period fits a rolling horizon, where two-stage is solved repeatedly.
- **Run the cheap screen first.** Solve the mean-value problem and a coarse 20-scenario stochastic model; compute EVPI and VSS. If both are tiny and the user is risk-neutral, the deterministic model may be enough — report that finding, it is a result.
- **Confirm solver access.** The extensive form is an ordinary MIP: Gurobi if licensed, otherwise HiGHS/CBC handle moderate sizes.

## Two-Stage Modeling Framework

The risk-neutral two-stage stochastic program with recourse:

$$
\min_{x}\;\; c^{\top} x + \mathbb{E}_{\xi}\!\left[\, Q(x, \xi) \,\right]
\quad \text{s.t.}\quad A x \ge b,\;\; x \in X,
$$

where the recourse function is the optimal value of the second-stage problem,

$$
Q(x, \xi) \;=\; \min_{y \ge 0} \;\left\{\, q(\xi)^{\top} y \;:\; W y = h(\xi) - T(\xi)\, x \,\right\}.
$$

| Term | Meaning |
|---|---|
| First stage $x$ (here-and-now) | Decided before $\xi$ is observed; identical in every scenario |
| Second stage $y$ (wait-and-see, recourse) | Reacts to the observed scenario; one copy per scenario |
| Technology matrix $T(\xi)$ | Couples the first-stage decision into the second stage |
| Fixed recourse | $W$ does not depend on $\xi$ — required by most theory and by the L-shaped method |
| Complete recourse | Second stage feasible for every $x$ and every $\xi$ (e.g., via penalized slacks) |
| Relatively complete recourse | Feasible for every $x$ that is first-stage feasible |
| Nonanticipativity | $x$ may not depend on the scenario; implicit when one $x$ is shared by all scenario blocks |

When $\xi$ has finite support $\{\xi_1,\dots,\xi_S\}$ with probabilities $p_s$, the model collapses to the **extensive form** (deterministic equivalent) — an ordinary LP/MIP:

$$
\min\; c^{\top} x + \sum_{s=1}^{S} p_s\, q_s^{\top} y_s
\quad \text{s.t.}\quad A x \ge b;\qquad T_s x + W y_s = h_s,\;\; y_s \ge 0 \quad (s = 1, \dots, S).
$$

Size grows linearly in $S$: with $m_2$ second-stage rows and $n_2$ second-stage columns per scenario, the extensive form has about $m_1 + S\,m_2$ rows and $n_1 + S\,n_2$ columns. A second stage of 500 rows × 800 columns with 1,000 scenarios is a 500k × 800k LP — block-angular, and exactly the structure the L-shaped method exploits.

### Decision tree: how should uncertainty enter the model?

```text
Is the uncertain data essentially harmless (small variation, or the optimal
decision barely moves when it changes)?
├─ YES → deterministic model + sensitivity analysis. Stop here.
└─ NO
   ├─ Do you have (or can you fit) a credible probability distribution?
   │   ├─ NO  → distribution-free worst-case protection → robust-optimization.
   │   └─ YES
   │       ├─ Can some decisions react AFTER uncertainty is revealed?
   │       │   ├─ NO  → chance constraints (see Advanced Techniques) or static RO.
   │       │   └─ YES
   │       │       ├─ One observe-then-act point → TWO-STAGE program (this skill).
   │       │       └─ Observe-then-act repeats over many periods → multistage
   │       │          program / SDDP (see Advanced Techniques), or a rolling
   │       │          horizon of two-stage models.
   │       └─ Risk-neutral?
   │           ├─ YES → expectation objective.
   │           └─ NO  → mean-CVaR objective (see Advanced Techniques).
```

### Decision tree: how should you solve the two-stage model?

```text
Does the extensive form (≈ m1 + S·m2 rows) fit memory and the time budget?
├─ YES → build it in Gurobi (default). Simplest, and the solver's presolve,
│        cuts, and heuristics all work on it.
└─ NO
   ├─ Second stage continuous (LP)? → L-shaped method = Benders on the scenario
   │        blocks, lazy-constraint callbacks → benders-decomposition.
   ├─ Second stage has integers? → integer L-shaped (Laporte & Louveaux 1993),
   │        progressive hedging, or scenario reduction + extensive form.
   └─ Distribution continuous / scenario count effectively unbounded?
            → SAA: sample N scenarios, replicate M times, estimate the gap
              (protocol below). Combine freely with either solver path.
```

### Study protocol

1. Run the Initial Assessment; write down stages, random parameters, recourse type.
2. Build the deterministic core model and validate it on a tiny instance (this is the per-scenario block).
3. Add penalized slacks if needed so recourse is complete; price the penalty economically.
4. Implement a seeded scenario generator; test it for stability (Advanced Techniques).
5. Build the extensive form as a function of (scenario set, probabilities) — never hard-code $S$.
6. Solve EV, WS, RP on a moderate scenario set; report EVPI and VSS.
7. If the true distribution is continuous or $S$ must be huge, run the SAA protocol.
8. If the extensive form is too big at the required $N$, switch to the L-shaped method.
9. Evaluate the final first-stage plan on a fresh out-of-sample scenario set; report the cost distribution, not just the mean.
10. Archive seeds, solver version, parameters, and the scenario sets next to the results.

## Worked Example: Stochastic Capacity Planning in Gurobi

The running example is two-stage capacity planning with uncertain demand — the stochastic core of facility sizing (see **facility-location-problem** for the deterministic relatives). Sites $i \in I$, customers $j \in J$, scenarios $s$ with probability $p_s$. First stage: open site ($z_i \in \{0,1\}$, fixed cost $f_i$) and size it ($x_i \ge 0$, unit cost $c_i$, limit $\bar{x}_i$). Second stage: ship $y_{ijs} \ge 0$ at unit cost $q_{ij}$; unmet demand $u_{js} \ge 0$ is penalized at $\rho$ per unit, which gives complete recourse.

$$
\begin{aligned}
\min\;\; & \sum_{i} \big(f_i z_i + c_i x_i\big) \;+\; \sum_{s} p_s \Big( \sum_{i,j} q_{ij}\, y_{ijs} + \rho \sum_{j} u_{js} \Big) \\
\text{s.t.}\;\; & x_i \le \bar{x}_i\, z_i \qquad\qquad\;\; i \in I \\
& \textstyle\sum_{j} y_{ijs} \le x_i \qquad\;\;\; i \in I,\; \forall s \\
& \textstyle\sum_{i} y_{ijs} + u_{js} = d_{js} \quad j \in J,\; \forall s \\
& z_i \in \{0,1\},\quad x_i,\, y_{ijs},\, u_{js} \ge 0.
\end{aligned}
$$

Instance data and a seeded Monte Carlo scenario sampler:

```python
from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class CapPlanInstance:
    """Two-stage capacity planning: open and size sites, then serve random demand."""

    fixed_cost: np.ndarray   # (m,) fixed cost of opening site i
    unit_cap_cost: np.ndarray  # (m,) cost per unit of capacity at site i
    ship_cost: np.ndarray    # (m, n) unit cost of serving customer j from site i
    max_cap: np.ndarray      # (m,) capacity limit at an open site
    penalty: float           # unit cost of unmet demand (lost-sales value)
    demand_mean: np.ndarray  # (n,) mean demand per customer
    demand_cv: float         # coefficient of variation of demand


def make_instance(m: int, n: int, seed: int) -> CapPlanInstance:
    """Generate a random capacity-planning instance on the unit square."""
    rng = np.random.default_rng(seed)
    sites = rng.uniform(0.0, 1.0, size=(m, 2))
    customers = rng.uniform(0.0, 1.0, size=(n, 2))
    dist = np.linalg.norm(sites[:, None, :] - customers[None, :, :], axis=2)
    demand_mean = rng.uniform(10.0, 30.0, size=n)
    return CapPlanInstance(
        fixed_cost=rng.uniform(300.0, 600.0, size=m),
        unit_cap_cost=rng.uniform(4.0, 8.0, size=m),
        ship_cost=10.0 * dist,
        max_cap=np.full(m, 0.6 * demand_mean.sum()),
        penalty=50.0,
        demand_mean=demand_mean,
        demand_cv=0.3,
    )


def sample_scenarios(
    inst: CapPlanInstance, n_scen: int, seed: int
) -> tuple[np.ndarray, np.ndarray]:
    """Monte Carlo demand scenarios; returns (demands (S, n), probabilities (S,))."""
    rng = np.random.default_rng(seed)
    sigma = inst.demand_cv * inst.demand_mean
    demands = rng.normal(inst.demand_mean, sigma, size=(n_scen, inst.demand_mean.size))
    demands = np.maximum(demands, 0.0)
    prob = np.full(n_scen, 1.0 / n_scen)
    return demands, prob


inst = make_instance(m=3, n=4, seed=7)
demands, prob = sample_scenarios(inst, n_scen=5, seed=11)
print(demands.round(1))
# Expected: a (5, 4) array of nonnegative demands centered near inst.demand_mean
# with roughly 30% relative spread; probabilities are uniform 1/5.
```

The extensive form, built as a function of the scenario set so the same code serves the stochastic model, the mean-value model ($S=1$), and every SAA replication:

```python
import gurobipy as gp
import numpy as np
from gurobipy import GRB


def build_extensive_form(
    fixed_cost: np.ndarray,
    unit_cap_cost: np.ndarray,
    ship_cost: np.ndarray,
    max_cap: np.ndarray,
    penalty: float,
    demands: np.ndarray,
    prob: np.ndarray,
) -> tuple[gp.Model, gp.tupledict, gp.tupledict, gp.tupledict, gp.tupledict]:
    """Deterministic equivalent of the capacity-planning model; returns (model, z, x, y, u)."""
    m_sites, n_cust = ship_cost.shape
    n_scen = demands.shape[0]
    model = gp.Model("capplan_extensive")
    z = model.addVars(m_sites, vtype=GRB.BINARY, name="open")
    x = model.addVars(m_sites, lb=0.0, name="cap")
    y = model.addVars(n_scen, m_sites, n_cust, lb=0.0, name="ship")
    u = model.addVars(n_scen, n_cust, lb=0.0, name="unmet")

    model.addConstrs((x[i] <= max_cap[i] * z[i] for i in range(m_sites)), name="link")
    model.addConstrs(
        (y.sum(s, i, "*") <= x[i] for s in range(n_scen) for i in range(m_sites)),
        name="capacity",
    )
    model.addConstrs(
        (y.sum(s, "*", j) + u[s, j] == demands[s, j]
         for s in range(n_scen) for j in range(n_cust)),
        name="demand",
    )

    first_stage = gp.quicksum(
        fixed_cost[i] * z[i] + unit_cap_cost[i] * x[i] for i in range(m_sites)
    )
    second_stage = gp.quicksum(
        prob[s] * (
            gp.quicksum(ship_cost[i, j] * y[s, i, j]
                        for i in range(m_sites) for j in range(n_cust))
            + penalty * gp.quicksum(u[s, j] for j in range(n_cust))
        )
        for s in range(n_scen)
    )
    model.setObjective(first_stage + second_stage, GRB.MINIMIZE)
    return model, z, x, y, u


def solve_extensive(
    model: gp.Model,
    z: gp.tupledict,
    x: gp.tupledict,
    time_limit: float = 60.0,
) -> tuple[float, np.ndarray, np.ndarray]:
    """Solve the extensive form; return (objective, open vector, capacity vector)."""
    model.Params.OutputFlag = 0
    model.Params.TimeLimit = time_limit
    model.Params.MIPGap = 1e-4
    model.optimize()
    if model.Status not in (GRB.OPTIMAL, GRB.TIME_LIMIT) or model.SolCount == 0:
        raise RuntimeError(f"no solution available, status {model.Status}")
    z_val = np.array([z[i].X for i in range(len(z))]).round()
    x_val = np.array([x[i].X for i in range(len(x))])
    return float(model.ObjVal), z_val, x_val


inst = make_instance(m=3, n=4, seed=7)
demands, prob = sample_scenarios(inst, n_scen=5, seed=11)
model, z, x, y, u = build_extensive_form(
    inst.fixed_cost, inst.unit_cap_cost, inst.ship_cost,
    inst.max_cap, inst.penalty, demands, prob,
)
rp, z_val, x_val = solve_extensive(model, z, x)
print(f"RP = {rp:.1f}  open = {z_val.astype(int)}  capacity = {x_val.round(1)}")
# Expected: solves to optimality in well under a second; opens 2 of 3 sites with
# total capacity ~113, enough to cover even the worst sampled scenario -- here the
# unmet-demand penalty (50) dwarfs the unit capacity-plus-shipping cost, so it is
# optimal to insure fully against the 5 sampled outcomes.
```

### EV, WS, EVPI, and VSS: is the stochastic model worth it?

Three reference problems quantify what modeling uncertainty buys. **RP** (recourse problem) is the stochastic optimum above. **WS** (wait-and-see) solves one deterministic problem per scenario, as if the future were known, and averages the optima. **EV** solves the mean-value problem; freezing its first-stage plan and evaluating it across all scenarios gives **EEV**. For minimization,

$$
\text{WS} \;\le\; \text{RP} \;\le\; \text{EEV}, \qquad
\text{EVPI} = \text{RP} - \text{WS} \;\ge\; 0, \qquad
\text{VSS} = \text{EEV} - \text{RP} \;\ge\; 0,
$$

and additionally $\text{EV} \le \text{WS}$ when the recourse value is convex in the uncertain parameter (Madansky 1960). EVPI is the most you should pay for a perfect forecast; VSS — introduced by Birge (1982), "The value of the stochastic solution in stochastic linear programs with fixed recourse" — is what solving the stochastic model instead of the mean-value model is worth. Report both in every study: large EVPI with small VSS means forecasting helps but the stochastic model does not, and vice versa.

```python
import gurobipy as gp
import numpy as np
from gurobipy import GRB

# Builds on CapPlanInstance, make_instance, sample_scenarios, build_extensive_form,
# and solve_extensive from the blocks above.


def fixed_plan_scenario_costs(
    inst: CapPlanInstance,
    z_val: np.ndarray,
    x_val: np.ndarray,
    demands: np.ndarray,
) -> np.ndarray:
    """Total cost (first stage + optimal recourse) of a fixed plan, per scenario."""
    n_scen = demands.shape[0]
    weights = np.full(n_scen, 1.0 / n_scen)  # any positive weights: scenarios decouple
    model, z, x, y, u = build_extensive_form(
        inst.fixed_cost, inst.unit_cap_cost, inst.ship_cost,
        inst.max_cap, inst.penalty, demands, weights,
    )
    for i in range(len(z_val)):
        z[i].LB, z[i].UB = z_val[i], z_val[i]
        x[i].LB, x[i].UB = x_val[i], x_val[i]
    model.Params.OutputFlag = 0
    model.optimize()
    if model.Status != GRB.OPTIMAL:
        raise RuntimeError(f"evaluation failed, status {model.Status}")
    m_sites, n_cust = inst.ship_cost.shape
    first = float(inst.fixed_cost @ z_val + inst.unit_cap_cost @ x_val)
    costs = np.empty(n_scen)
    for s in range(n_scen):
        ship = sum(inst.ship_cost[i, j] * y[s, i, j].X
                   for i in range(m_sites) for j in range(n_cust))
        unmet = inst.penalty * sum(u[s, j].X for j in range(n_cust))
        costs[s] = first + ship + unmet
    return costs


def stochastic_metrics(
    inst: CapPlanInstance, demands: np.ndarray, prob: np.ndarray
) -> dict[str, float]:
    """Compute RP, WS, EV, EEV and the derived EVPI / VSS for one scenario set."""
    args = (inst.fixed_cost, inst.unit_cap_cost, inst.ship_cost,
            inst.max_cap, inst.penalty)
    model, z, x, _, _ = build_extensive_form(*args, demands, prob)
    rp, _, _ = solve_extensive(model, z, x)

    scen_optima = []
    for s in range(demands.shape[0]):
        m_s, z_s, x_s, _, _ = build_extensive_form(*args, demands[s:s + 1], np.ones(1))
        obj_s, _, _ = solve_extensive(m_s, z_s, x_s)
        scen_optima.append(obj_s)
    ws = float(prob @ np.array(scen_optima))

    mean_demand = (prob[:, None] * demands).sum(axis=0, keepdims=True)
    m_ev, z_ev, x_ev, _, _ = build_extensive_form(*args, mean_demand, np.ones(1))
    ev, z_bar, x_bar = solve_extensive(m_ev, z_ev, x_ev)
    eev = float(prob @ fixed_plan_scenario_costs(inst, z_bar, x_bar, demands))

    return {"WS": ws, "EV": ev, "RP": rp, "EEV": eev,
            "EVPI": rp - ws, "VSS": eev - rp}


inst = make_instance(m=3, n=4, seed=7)
demands, prob = sample_scenarios(inst, n_scen=5, seed=11)
metrics = stochastic_metrics(inst, demands, prob)
print({k: round(v, 1) for k, v in metrics.items()})
# Expected: WS <= RP <= EEV up to MIP tolerance, hence EVPI >= 0 and VSS >= 0.
# The mean-value plan under-sizes capacity (it never sees above-average demand),
# so EEV pays penalty costs that the stochastic plan avoids.
```

## Scenario Generation and Reduction

A scenario set is a finite approximation of the true distribution. The quality criterion is decision-oriented: two scenario sets are equally good if they induce (nearly) the same optimal first-stage decision and objective — distributional fidelity beyond that is wasted scenario budget (Kaut & Wallace 2007, "Evaluation of scenario-generation methods").

| Method | Strength | Use when |
|---|---|---|
| Crude Monte Carlo | Unbiased; trivially correct with `default_rng(seed)` | Default inside SAA; large $N$ affordable |
| Latin hypercube (LHS) | Stratifies every marginal; large variance reduction | Moderate $N$; independent or copula-coupled marginals |
| Antithetic pairs | Exact mean for symmetric marginals; negative correlation | Cheap add-on to MC for symmetric distributions |
| Moment matching | Small sets reproducing mean/cov/skew (Høyland & Wallace 2001) | Very tight scenario budgets (S ≤ 50) |
| Historical / bootstrap | No distributional assumption; keeps dependence | Enough representative history exists |

```python
import numpy as np
from scipy.stats import norm


def mc_scenarios(mean: np.ndarray, sigma: np.ndarray, n_scen: int, seed: int) -> np.ndarray:
    """Plain Monte Carlo normal demand sample, truncated at zero."""
    rng = np.random.default_rng(seed)
    return np.maximum(rng.normal(mean, sigma, size=(n_scen, mean.size)), 0.0)


def lhs_scenarios(mean: np.ndarray, sigma: np.ndarray, n_scen: int, seed: int) -> np.ndarray:
    """Latin hypercube sample: each marginal stratified into n_scen equal-probability bins."""
    rng = np.random.default_rng(seed)
    n_dim = mean.size
    strata = (np.arange(n_scen)[:, None] + rng.uniform(size=(n_scen, n_dim))) / n_scen
    u = rng.permuted(strata, axis=0)  # independent row permutation per column
    return np.maximum(mean + sigma * norm.ppf(u), 0.0)


def antithetic_scenarios(mean: np.ndarray, sigma: np.ndarray, n_scen: int, seed: int) -> np.ndarray:
    """Antithetic pairs (z, -z): exact sample mean for symmetric marginals."""
    rng = np.random.default_rng(seed)
    half = n_scen // 2
    z = rng.standard_normal((half, mean.size))
    return np.maximum(mean + sigma * np.vstack([z, -z]), 0.0)


mean = np.array([20.0, 15.0, 25.0, 18.0])
sigma = 0.3 * mean
est_mc = [mc_scenarios(mean, sigma, 20, s).sum(axis=1).mean() for s in range(200)]
est_lhs = [lhs_scenarios(mean, sigma, 20, s).sum(axis=1).mean() for s in range(200)]
print(f"std of E[total demand] estimate: MC {np.std(est_mc):.3f}  LHS {np.std(est_lhs):.3f}")
# Expected: the LHS estimator's standard deviation is several times smaller than
# crude Monte Carlo at the same sample size (20 scenarios); both center near 78.
```

For correlated demands, sample multivariate normals with a Cholesky factor (`rng.multivariate_normal` or `mean + z @ L.T`) before any marginal transform; for non-normal marginals, transform LHS uniforms through each marginal's inverse CDF and couple them with a Gaussian copula.

**Scenario reduction** shrinks a large set to $k$ scenarios while staying close in a probability metric (a transport/Wasserstein-type distance between the original and reduced measures). The fast-forward algorithm of Heitsch & Römisch (2003), "Scenario Reduction Algorithms in Stochastic Programming" (building on Dupačová, Gröwe-Kuska & Römisch 2003), greedily adds the scenario that most reduces this distance, then moves each deleted scenario's probability to its nearest kept neighbor:

```python
import numpy as np


def fast_forward_reduction(
    scenarios: np.ndarray, prob: np.ndarray, k: int
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Reduce S scenarios to k by fast-forward selection (Heitsch & Roemisch 2003).

    Greedy: each step keeps the scenario that most reduces the probability-
    weighted distance to the kept set; deleted probability mass moves to the
    nearest kept scenario. O(k * S^2) time, O(S^2) memory for the distances.
    """
    dist = np.linalg.norm(scenarios[:, None, :] - scenarios[None, :, :], axis=2)
    n = prob.size
    selected: list[int] = []
    closest = np.full(n, np.inf)
    for _ in range(k):
        cand_cost = prob @ np.minimum(closest[:, None], dist)
        cand_cost[selected] = np.inf
        pick = int(np.argmin(cand_cost))
        selected.append(pick)
        closest = np.minimum(closest, dist[:, pick])
    keep = np.array(selected)
    nearest = keep[np.argmin(dist[:, keep], axis=1)]
    new_prob = np.array([prob[nearest == s].sum() for s in keep])
    return scenarios[keep], new_prob, keep


rng = np.random.default_rng(3)
scen = rng.normal([20.0, 15.0], [6.0, 4.5], size=(200, 2))
reduced, new_prob, kept = fast_forward_reduction(scen, np.full(200, 1 / 200), k=10)
print(kept, new_prob.round(3), float(new_prob.sum()))
# Expected: probabilities sum to 1.0; kept scenarios near the distribution center
# carry large weights, while a few outlying scenarios survive with small weights.
```

Two cautions. First, the Euclidean distance above is a proxy; when costs are very asymmetric in the random parameter, weight the coordinates by their cost impact. Second, reduction systematically thins the tails — never reduce scenarios before computing CVaR or chance constraints without checking tail coverage explicitly (see Practical Challenges).

## The SAA Protocol

When the distribution is continuous (or $S$ would have to be astronomically large), sample average approximation replaces the expectation by a sample mean:

$$
\hat{v}_N \;=\; \min_{x \in X}\; \hat{f}_N(x) \;=\; c^{\top} x + \frac{1}{N} \sum_{k=1}^{N} Q(x, \xi^k).
$$

The two facts that make SAA a *statistical method* rather than a heuristic (Kleywegt, Shapiro & Homem-de-Mello 2002, "The Sample Average Approximation Method for Stochastic Discrete Optimization"; Mak, Morton & Wood 1999, Monte Carlo bounding techniques):

- **Downward bias:** $\mathbb{E}[\hat{v}_N] \le v^*$, and the bias shrinks monotonically in $N$. Averaging $\hat{v}_N$ over $M$ independent replications estimates a *lower bound* on $v^*$, with a confidence interval from the replication variance.
- **Unbiased evaluation:** for any fixed feasible $\hat{x}$, $\hat{f}_{N'}(\hat{x})$ on an independent sample is an unbiased estimate of $f(\hat{x}) \ge v^*$ — an *upper bound* with its own confidence interval.

The difference of the two estimates bounds the optimality gap of $\hat{x}$. For finite feasible sets (binary first stages), the probability that the SAA solution is exactly optimal converges to one exponentially fast in $N$ — which is why moderate $N$ with several replications usually beats one huge $N$ (the empirical study of Linderoth, Shapiro & Wright 2006 confirms this on large two-stage problems).

Protocol: (1) pick $N$ so one SAA problem solves comfortably in the time budget; (2) solve $M = 5{-}20$ replications with independent seeds; (3) screen all $M$ candidate plans on one common evaluation sample (common random numbers make the comparison sharper); (4) re-evaluate only the winner on a fresh sample of size $N' \gg N$ to remove selection bias; (5) report both confidence intervals and the gap estimate; (6) if the gap is too large, double $N$ and repeat.

```python
import numpy as np
import pandas as pd

# Builds on CapPlanInstance, make_instance, sample_scenarios, build_extensive_form,
# solve_extensive, and fixed_plan_scenario_costs from the worked example above.

Z975 = 1.96  # standard normal quantile for 95% two-sided intervals


def saa_study(
    inst: CapPlanInstance,
    n_train: int,
    n_repl: int,
    n_eval: int,
    seed: int,
) -> tuple[pd.DataFrame, dict[str, float]]:
    """Full SAA protocol: replicate, bound from below, evaluate, estimate the gap."""
    args = (inst.fixed_cost, inst.unit_cap_cost, inst.ship_cost,
            inst.max_cap, inst.penalty)

    rows: list[dict[str, float]] = []
    candidates: list[tuple[np.ndarray, np.ndarray]] = []
    for m in range(n_repl):
        demands, prob = sample_scenarios(inst, n_train, seed=seed + m)
        model, z, x, _, _ = build_extensive_form(*args, demands, prob)
        v_n, z_val, x_val = solve_extensive(model, z, x)
        candidates.append((z_val, x_val))
        rows.append({"replication": m, "v_N": v_n,
                     "n_open": int(z_val.sum()), "total_cap": float(x_val.sum())})
    df = pd.DataFrame(rows)

    # Statistical lower bound on v*:  E[v_N] <= v*, estimated over replications.
    lb = float(df["v_N"].mean())
    lb_se = float(df["v_N"].std(ddof=1)) / np.sqrt(n_repl)

    # Screen all candidates on ONE common sample (common random numbers).
    demands_screen, _ = sample_scenarios(inst, n_eval, seed=seed + 10_000)
    screen_means = [
        float(fixed_plan_scenario_costs(inst, zv, xv, demands_screen).mean())
        for zv, xv in candidates
    ]
    best = int(np.argmin(screen_means))

    # Final, selection-bias-free evaluation of the winner on a FRESH sample.
    demands_final, _ = sample_scenarios(inst, n_eval, seed=seed + 20_000)
    costs = fixed_plan_scenario_costs(inst, *candidates[best], demands_final)
    ub = float(costs.mean())
    ub_se = float(costs.std(ddof=1)) / np.sqrt(n_eval)

    report = {
        "lower_bound": lb, "lb_halfwidth": Z975 * lb_se,
        "upper_bound": ub, "ub_halfwidth": Z975 * ub_se,
        "gap_estimate": ub - lb,
        "gap_halfwidth": Z975 * float(np.sqrt(lb_se ** 2 + ub_se ** 2)),
        "selected_replication": float(best),
    }
    return df, report


inst = make_instance(m=3, n=4, seed=7)
df, report = saa_study(inst, n_train=10, n_repl=5, n_eval=120, seed=42)
print(df.to_string(index=False))
print({k: round(v, 2) for k, v in report.items()})
# Expected: v_N varies visibly across the 5 replications (sampling noise); the
# gap estimate is a small fraction of the objective. A slightly negative
# gap_estimate is possible -- the true gap is nonnegative, the estimator is noisy.
```

Reading the output: if the replication objectives `v_N` disagree wildly, $N$ is too small for the decision to stabilize — increase $N$ before trusting any candidate. If the gap confidence interval is dominated by `lb_halfwidth`, add replications; if by `ub_halfwidth`, enlarge the evaluation sample (cheap — evaluation is LP-only with the first stage fixed).

## Advanced Techniques

### From the extensive form to the L-shaped method

For continuous second stages, $Q_s(x) = \min\{q_s^\top y : Wy = h_s - T_s x,\, y \ge 0\}$ is piecewise-linear convex in $x$. The L-shaped method (Van Slyke & Wets 1969) — Benders decomposition applied to the scenario structure — keeps only $x$ and an epigraph variable $\theta$ in the master and adds, at each iterate $\hat{x}$ with subproblem duals $\pi_s$, the optimality cut

$$
\theta \;\ge\; \sum_{s} p_s\, \pi_s^{\top} \big(h_s - T_s x\big),
$$

plus feasibility cuts from dual rays when recourse is incomplete. The multicut variant keeps one $\theta_s$ per scenario — fewer iterations, bigger master (Birge & Louveaux 1988); prefer it when scenarios are heterogeneous and $S$ is moderate. Binary first stages with integer recourse need the integer L-shaped cuts of Laporte & Louveaux (1993). Implementation — lazy-constraint callbacks, cut management, stabilization — lives in **benders-decomposition**; build the extensive form first anyway, as the correctness reference for the decomposed code.

### Risk-averse objectives: mean-CVaR

$\text{CVaR}_\alpha$ is the expected cost in the worst $(1-\alpha)$ tail. Rockafellar & Uryasev (2000), "Optimization of conditional value-at-risk," give the linearizable form $\text{CVaR}_\alpha(C) = \min_\eta\, \eta + \mathbb{E}[(C - \eta)^+]/(1-\alpha)$, which drops straight into the extensive form:

```python
import gurobipy as gp
from gurobipy import GRB


def add_mean_cvar_objective(
    model: gp.Model,
    first_stage_cost: gp.LinExpr,
    scenario_cost: list[gp.LinExpr],
    prob: list[float],
    alpha: float = 0.95,
    lam: float = 0.5,
) -> None:
    """Replace the expectation objective with (1-lam)*E[cost] + lam*CVaR_alpha."""
    n_scen = len(prob)
    eta = model.addVar(lb=-GRB.INFINITY, name="cvar_eta")
    excess = model.addVars(n_scen, lb=0.0, name="cvar_excess")
    model.addConstrs(
        (excess[s] >= first_stage_cost + scenario_cost[s] - eta
         for s in range(n_scen)),
        name="cvar_def",
    )
    expectation = first_stage_cost + gp.quicksum(
        prob[s] * scenario_cost[s] for s in range(n_scen))
    cvar = eta + gp.quicksum(prob[s] * excess[s] for s in range(n_scen)) / (1.0 - alpha)
    model.setObjective((1.0 - lam) * expectation + lam * cvar, GRB.MINIMIZE)
# Usage: pass the per-scenario second-stage cost expressions built alongside the
# extensive form; at the optimum eta equals the alpha-quantile (VaR) of total cost.
```

Mind the tail resolution: at $\alpha = 0.95$ with 100 scenarios, only 5 scenarios inform CVaR. Use $\ge 20/(1-\alpha)$ scenarios, and never feed CVaR a reduced scenario set without re-checking tail coverage.

### Chance constraints via scenario indicators

A constraint that must hold with probability $\ge 1 - \varepsilon$ becomes, on a scenario set, a big-M MIP: binaries $\delta_s$ mark allowed violations, each scenario row is relaxed by $M_s \delta_s$, and $\sum_s p_s \delta_s \le \varepsilon$ caps the violated mass. Tighten the $M_s$ per scenario (see **milp-modeling-gurobi**'s big-M guidance via linearization) and expect harder MIPs than expectation models of the same size. Sample-size guidance and strengthened mixing-set formulations: Luedtke & Ahmed (2008), "A sample approximation approach for optimization with probabilistic constraints."

### Multistage programs and scenario trees

With repeated observe-then-act cycles, scenarios become a tree; nonanticipativity forces decisions to agree on nodes with a shared history. The tree grows as $b^{T}$ for branching factor $b$ over $T$ stages, so extensive forms die quickly; the standard escapes are nested Benders / SDDP under stagewise independence (Pereira & Pinto 1991) or progressive hedging on the scenario formulation. Before committing to multistage machinery, test a rolling horizon of two-stage models — it is the strongest cheap baseline and often within a few percent.

### Testing a scenario generator for stability

Run two checks before trusting any generator (Kaut & Wallace 2007). **In-sample stability:** generate $K \approx 10$ scenario sets of the same size with different seeds, solve each; the optimal objectives should agree within the accuracy you plan to report. **Out-of-sample stability:** evaluate each of the $K$ first-stage plans on one large common reference sample; the evaluated costs should also agree. In-sample agreement with out-of-sample disagreement is the fingerprint of a generator that systematically misses part of the distribution (usually the tails).

## Practical Challenges

**The extensive form exhausts memory once the scenario count grows.** Size is linear in $S$, but solve time is not — MIPs degrade superlinearly. First reduce scenarios (fast-forward to a few hundred), then switch to the L-shaped method via **benders-decomposition**. Keep the small extensive form as a correctness oracle: both codes must agree on 20-scenario instances to machine precision.

**Some scenario makes the second stage infeasible.** Diagnose with `model.computeIIS()` on the failing scenario block. The structural fix is complete recourse: penalized slack on the binding resource (unmet demand, emergency purchase, overtime). Price the slack at its real economic cost — an arbitrary big number turns the model into a feasibility game and destroys dual information for L-shaped cuts.

**The SAA candidate changes every time the seed changes.** Expected when $N$ is small and the objective is flat near the optimum. Check whether the *evaluated costs* of the differing candidates agree (flat objective: pick any, report the tie) or disagree ($N$ too small: double it). Report decision stability across replications — `n_open` and `total_cap` in the replication table — not just objective stability.

**Reported objective beats out-of-sample performance.** That is the downward bias of $\hat{v}_N$ plus selection bias from picking the best candidate on the screening sample. Never report in-sample objectives as performance; the only honest number is the fresh-sample evaluation of the final plan (step 4 of the SAA protocol).

**Scenario reduction quietly removes the tail that drives risk.** Fast-forward keeps probability-mass centers, exactly the wrong set for CVaR or chance constraints. Either reduce conditionally (keep all scenarios beyond the $\alpha$-quantile of a pilot cost run, reduce only the bulk) or skip reduction for risk-averse models and pay the larger extensive form.

**The penalty parameter, not the data, decides the solution.** If doubling $\rho$ flips the first-stage plan, the model is answering "how much do you fear shortage" rather than "what does the data imply." Sweep $\rho$ over its defensible economic range and report the plan as a function of $\rho$; where the plan is constant, the recommendation is robust.

**Integer second-stage variables break the standard L-shaped method.** $Q_s(x)$ becomes nonconvex and LP duals no longer give valid cuts. Options in order of practicality: extensive form on a reduced scenario set, progressive hedging as a strong heuristic, integer L-shaped cuts (exact but slow), or convexifying the second stage and bounding the relaxation error.

**EVPI and VSS are both near zero — was the stochastic model pointless?** For a risk-neutral user, yes, and that is a publishable finding: the deterministic model suffices, documented with the EVPI/VSS table. But check the cost *distribution* first — a plan with the same mean and a fat loss tail still argues for the mean-CVaR model, which EVPI/VSS do not measure.

## Tools & Libraries

| Library / tool | When to use | Note |
|---|---|---|
| gurobipy | Extensive forms; L-shaped via lazy callbacks | Default here; extensive forms are ordinary MIPs and benefit fully from presolve |
| Pyomo + mpi-sppy | Scenario decomposition at scale (EF, PH, APH) | The maintained successor of PySP; MPI-parallel progressive hedging |
| SDDP.jl | Multistage with stagewise-independent uncertainty | Julia; the practical standard for hydro-scheduling-style problems |
| numpy (`default_rng`) | Scenario sampling, reduction, plan evaluation | Seed everything; vectorize scenario math |
| scipy.stats | Fitting marginals, inverse CDFs for LHS, copulas | Pair `norm.ppf` with stratified uniforms as in the LHS block |
| pandas | Replication and evaluation tables | One row per (replication, candidate); aggregate for the report |

## Output Format

A complete stochastic-optimization deliverable contains:

1. **Model summary** — stages, variable counts and types per stage, recourse type (complete / relatively complete), extensive-form size at the chosen $S$.
2. **Uncertainty report** — random parameters, distribution source, generation method and seeds, stability-check result, correlation treatment.
3. **Value-of-model table** — EV, WS, RP, EEV with EVPI and VSS in absolute terms and as % of RP.
4. **SAA table** (when used) — $M$, $N$, $N'$, lower/upper bounds with 95% CIs, gap estimate with CI, decision stability across replications.
5. **Recommended plan** — first-stage decision values, out-of-sample expected cost, cost quantiles (5%, 50%, 95%) and CVaR if risk matters.
6. **Reproducibility block** — seeds, solver version and parameters, wall-clock times, commit hash of the scenario generator.

```text
## Stochastic capacity plan -- results summary
Model: two-stage, first stage 3 binary + 3 continuous, recourse complete (penalty 50)
Scenarios: LHS, normal demand cv=0.3, seeds 42..46 (train) / 20042 (final eval)

Metric table          SAA table (M=5, N=100, N'=2000)
  EV    = 1,180.4       lower bound  1,492.3  +/- 11.8
  WS    = 1,455.1       upper bound  1,512.6  +/-  9.4
  RP    = 1,503.8       gap          20.3 +/- 15.1   (1.3% of UB)
  EEV   = 1,611.0
  EVPI  =    48.7  (3.2% of RP)
  VSS   =   107.2  (7.1% of RP)

Recommended plan: open sites {0, 2}, capacities (41.3, 0, 38.9)
Out-of-sample cost: mean 1,512.6; q05 1,318; q95 1,775; CVaR_0.95 1,841
```

Report the gap and both half-widths together — a small gap with a huge half-width is no evidence of quality. When the deterministic model wins (tiny EVPI and VSS), say so explicitly and recommend it.

## Questions to Ask

- Which input data is actually uncertain, and how large is its variation relative to its mean?
- What can still be decided after the uncertainty is revealed — what is the recourse?
- Where does the distribution come from: history, a fitted model, or expert judgment?
- Are the random parameters correlated, and must that correlation be preserved?
- Is the user risk-neutral, or do rare expensive outcomes need explicit protection (CVaR)?
- What happens physically when demand cannot be met — lost sale, backorder, emergency purchase — and at what cost?
- How many scenarios can the time budget afford per solve, and how often is the model re-solved?
- Is this a one-shot strategic decision or a rolling operational one?
- What optimality-gap and confidence level must the final report defend?
- Is there a deterministic incumbent model whose plan we should benchmark via EEV?

## Related Skills

- **benders-decomposition** — when the extensive form exceeds memory or the time budget; implements the L-shaped method (optimality/feasibility cuts, lazy-constraint callbacks) that this skill only sketches.
- **facility-location-problem** — when the application is plant or warehouse location and sizing under uncertain demand; provides the deterministic core models the stochastic extension builds on.
- **robust-optimization** — when no credible distribution exists and worst-case protection over an uncertainty set fits better; includes RO-vs-SP selection guidance and the price of robustness.
- **instance-generation-and-benchmarks** — when you need reproducible scenario sets, controlled-hardness synthetic instances, and train/test splits for tuning and evaluating stochastic models.
