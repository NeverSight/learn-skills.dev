---
name: problem-formulation
description: When the user wants to translate a word problem or real-world planning situation into a formal optimization model — identifying decision variables, objective function, and constraints, choosing the model type (LP, MIP, CP, or heuristic), estimating model size, and auditing the data before any solver code is written. Also use when the user mentions "formulate," "model this problem," "decision variables," "objective function," "translate to optimization," or when a problem arrives as plain prose with no mathematical structure yet. For implementing the resulting MIP, see milp-modeling-gurobi; for nonlinear terms that must become linear, see linearization-techniques.
---

# Problem Formulation

You are an expert in translating real-world decision problems into formal optimization models. This skill covers the full path from a prose description to a precise, solvable model: extracting decisions, objective, and constraints; choosing among LP, MIP, CP, and heuristic approaches; estimating model size; auditing input data; and recognizing when a problem needs decomposition. It is the entry-point skill — use the protocol below before writing any solver code, then hand off to the method-specific skill the decision tree selects.

## Initial Assessment

Establish these facts before formulating anything. Most formulation failures trace back to a skipped item on this list.

- **Restate the problem in one sentence.** Force the template "Choose ___ to minimize/maximize ___ subject to ___." If the stakeholder cannot fill all three blanks, the problem is not yet an optimization problem — it is a requirements-gathering problem.
- **Identify the decision maker and the decision moment.** What is actually controllable, and when is it decided? Quantities decided after uncertainty resolves are recourse, not first-stage decisions.
- **List candidate decisions explicitly.** Selection (yes/no), assignment (who does what), sequencing (in what order), timing (when), quantity (how much), routing (which path). Each maps to a different variable archetype.
- **Separate hard from soft constraints.** Ask for each stated rule: "What happens if this is violated?" If the answer is a cost or a complaint, it is soft. If the answer is "physically impossible" or "contract breach," it is hard.
- **Identify the objective — and whether there is exactly one.** Multiple objectives stated as one ("minimize cost while maximizing service") must be surfaced as a trade-off before modeling, not averaged silently.
- **Estimate instance size.** Cardinality of every entity set (items, machines, periods, customers, scenarios). Multiply index sets to predict variable counts before committing to a formulation.
- **Audit the data.** Does data exist at the granularity the model needs? Units consistent? Signs sensible? Aggregate capacity at least equal to aggregate demand? Run the audit script below before modeling.
- **Establish the solution requirement.** Proven optimality, a quality guarantee (gap), or "good and fast"? This decides exact vs heuristic more than problem structure does.
- **Establish the compute budget.** Seconds (online decision), minutes (interactive planning), or hours (overnight batch)? And how often will the model be re-solved?
- **Check solver availability.** Gurobi license, open-source MIP only, or no MIP solver at all? CP-SAT is free; that fact alone sometimes decides the model type.
- **Identify what changes between runs.** Data that varies per run becomes parameters; structure that varies (new constraint types) means the model document must be versioned, not just the data.
- **Find the closest classic problem.** Knapsack, assignment, facility location, routing, scheduling, covering, lot sizing. Matching to a classic problem imports decades of formulation and algorithm knowledge for free.

## Formulation Protocol

Work through seven steps in order. Steps 1–5 produce the formal model; steps 6–7 select the method and validate. The model is method-independent: write it down before choosing LP/MIP/CP/heuristic, because the same model document drives all four.

**Step 1 — One-sentence restatement.** "Choose ___ to optimize ___ subject to ___." Get the stakeholder to confirm this sentence in writing. Every later disagreement is settled against it.

**Step 2 — Sets and parameters (the nouns).** Entities the problem talks about become index sets ($P$ = plants, $K$ = products, $T$ = periods). Given quantities become parameters with units written next to them ($c_{pk}$ = unit cost [EUR/unit], $a_{pk}$ = processing time [h/unit]). A parameter without a unit is a bug waiting to happen. Audit the data now (script in the worked example below).

**Step 3 — Decision variables (the verbs of choice).** Each controllable action becomes a variable family with a one-sentence meaning, a domain, and units:

| Decision archetype | Variable | Domain |
|---|---|---|
| Select / open / use | $z_i$ | $\{0,1\}$ |
| Assign $i$ to $j$ | $x_{ij}$ | $\{0,1\}$ |
| Quantity / flow | $y_i$ or $x_{ij}$ | $\mathbb{R}_{\ge 0}$ (or $\mathbb{Z}_{\ge 0}$ if indivisible) |
| Sequence / order | permutation, or precedence binaries $x_{ij}$ | permutation space / $\{0,1\}$ |
| Timing | start time $s_i$ | $\mathbb{R}_{\ge 0}$ or interval variable (CP) |

Two design heuristics. First, choose variables so the objective and constraints come out linear; a clever variable definition (e.g., $x_{ij}$ = "$j$ immediately follows $i$" instead of "position of $i$") often removes nonlinearity entirely. Second, prefer disaggregated variables when they tighten the LP relaxation — the classic example is $x_{ij} \le z_j$ for every $i$ instead of $\sum_i x_{ij} \le n\, z_j$ (Vielma 2015, "Mixed Integer Linear Programming Formulation Techniques").

**Step 4 — Objective.** Write it as a sum of named cost/benefit terms, each traceable to a parameter with units. If terms have different units (EUR and minutes), stop: either convert with an explicit exchange rate or treat the problem as multi-objective.

**Step 5 — Constraints, family by family.** Translate prose signals into archetypes:

| Prose signal | Archetype | Canonical form |
|---|---|---|
| "cannot exceed," "at most," "budget" | capacity / knapsack | $\sum_i a_i x_i \le b$ |
| "must meet," "at least," "cover" | demand / covering | $\sum_i a_i x_i \ge d$ |
| "exactly one," "each ... to one" | assignment / partitioning | $\sum_j x_{ij} = 1$ |
| "if A then B" | implication | $z_A \le z_B$ |
| "either A or B" | disjunction | $z_A + z_B \ge 1$, or big-M pair |
| "fixed cost when used" | fixed charge | $y \le M z$, $f z$ in objective |
| "B after A finishes" | precedence | $s_B \ge s_A + p_A$ |
| "not at the same time" | disjunctive / no-overlap | big-M pair, or CP `NoOverlap` |
| "balanced," "fair," "worst case" | min-max | $\ell \ge \text{load}_i \;\forall i$, min $\ell$ |
| "all different" | AllDifferent | CP global, or assignment binaries |

Mark every family hard or soft (step from Initial Assessment). Soft families get violation variables and penalties — see Advanced Techniques.

**Step 6 — Size estimation and model-type choice.** Multiply index-set cardinalities per variable and constraint family; compare against the rule-of-thumb table in the next section; run the decision tree. This is where LP vs MIP vs CP vs heuristic is decided — by evidence, not habit.

**Step 7 — Smallest instance first.** Build an instance small enough to verify by hand (2–4 elements per set). Solve it, check the answer against manual reasoning, and only then scale up. A model that is wrong on 2 plants and 3 warehouses is also wrong on 50 and 200 — just less visibly.

The generic model every step feeds into:

$$
\min_{x} \; f(x) \quad \text{s.t.} \quad g_i(x) \le b_i \;\; (i \in I), \qquad x_j \in D_j \;\; (j \in J)
$$

where the formulation work is precisely: choosing the $x_j$ and their domains $D_j$ (step 3), writing $f$ (step 4), and writing the $g_i$ (step 5). The standard reference for this craft is Williams (2013), "Model Building in Mathematical Programming," 5th ed.

## Model-Type Selection and Size Estimation

### Decision tree

```text
START: a decision problem described in prose, model written per the protocol
|
+-- Are any decisions discrete (select / assign / sequence / count)?
|     NO  -> all-continuous: LP (network flow special case if the constraint
|            matrix is a flow matrix -> integral LP, very fast)
|     YES
|      +-- Is the core difficulty logical/sequencing structure (disjunctions,
|      |   AllDifferent, no-overlap, long implication chains) with few or no
|      |   continuous quantities?
|      |     YES -> CP first (see constraint-programming); keep a MIP as the
|      |            fallback if optimality proofs on loose objectives stall
|      |     NO
|      |      +-- Can every nonlinear term be linearized exactly (products
|      |      |   with binaries, |.|, min/max, piecewise linear, logic)?
|      |      |     YES -> MIP (see linearization-techniques for the rewrite,
|      |      |            milp-modeling-gurobi for the build)
|      |      |     NO  -> convex MINLP if curvature cooperates; otherwise
|      |      |            piecewise-linear approximation + MIP, or heuristic
|      |      +-- Does size estimation put the model beyond solver reach
|      |            (table below), or is the answer needed in under a second?
|      |            YES -> metaheuristic (see metaheuristic-design-principles
|      |                   for the method, solution-encodings for the
|      |                   representation); keep the exact model for
|      |                   validation on small instances
|      |            NO  -> exact model; check for decomposable structure
|      |                   before solving monolithically (Advanced Techniques)
|
RULE: the formal model comes first; the method choice is a consequence.
```

### Size rules of thumb

These are structure-dependent; treat them as order-of-magnitude triggers for concern, not hard limits.

| Model class | Routine on modern solvers | Concern threshold (typical) |
|---|---|---|
| LP | millions of variables/rows | $> 5 \times 10^7$ nonzeros: memory and build time dominate |
| MIP | $10^4$–$10^5$ binaries with good structure | $> 10^6$ binaries, or weak relaxation at any size |
| CP-SAT | $10^5$–$10^6$ booleans, feasibility-driven | loose continuous objectives; large integer ranges |
| Quadratic discrete (QAP-like) | $n \lesssim 30$ exactly | anything larger: linearize or go heuristic |
| Metaheuristic | bounded only by evaluation cost | objective evaluation slower than ~1 ms ungated |

Structure beats counts: a set-partitioning MIP with $10^6$ columns and a tight relaxation often solves faster than a weak big-M model with $10^4$ binaries. The estimator below makes the counting mechanical.

```python
from dataclasses import dataclass
from math import prod


@dataclass
class SizeReport:
    """Estimated dimensions of a model before any code is written."""
    n_binary: int
    n_integer: int
    n_continuous: int
    n_constraints: int
    n_nonzeros: int
    warnings: list[str]


def estimate_size(
    var_families: dict[str, tuple[tuple[int, ...], str]],
    constraint_families: dict[str, tuple[tuple[int, ...], int]],
) -> SizeReport:
    """Estimate model size from index-set cardinalities.

    var_families: name -> (index-set sizes, vtype in {'B', 'I', 'C'}).
    constraint_families: name -> (index-set sizes, average terms per row).
    """
    counts = {"B": 0, "I": 0, "C": 0}
    for sizes, vtype in var_families.values():
        counts[vtype] += prod(sizes)
    n_rows = 0
    n_nz = 0
    for sizes, terms in constraint_families.values():
        rows = prod(sizes)
        n_rows += rows
        n_nz += rows * terms
    warnings: list[str] = []
    if n_nz > 50_000_000:
        warnings.append("nonzeros > 5e7: build time and memory become the bottleneck")
    if counts["B"] + counts["I"] > 1_000_000:
        warnings.append("over 1e6 discrete variables: consider decomposition or a heuristic")
    if n_rows > 0 and n_nz / n_rows > 10_000:
        warnings.append("very dense rows: look for avoidable all-pairs sums")
    return SizeReport(counts["B"], counts["I"], counts["C"], n_rows, n_nz, warnings)


# Tiny synthetic check: production-distribution with 50 plants, 200 warehouses, 30 products.
report = estimate_size(
    var_families={
        "y_production": ((50, 30), "C"),
        "x_shipping": ((50, 200, 30), "C"),
        "z_setup": ((50, 30), "B"),
    },
    constraint_families={
        "flow_balance": ((50, 30), 201),
        "demand": ((200, 30), 51),
        "capacity": ((50,), 30),
        "setup_link": ((50, 30), 2),
    },
)
print(report.n_binary, report.n_continuous, report.n_constraints, report.n_nonzeros)
print(report.warnings)
# Expected: 1500 binaries, 301500 continuous, 9050 constraints, 612000 nonzeros,
# and an empty warning list -- a routine MIP at this scale.
```

The decision tree itself is mechanical enough to encode. Keeping it as code forces every assessment answer to be written down, which is the actual point.

```python
def recommend_model_type(
    has_discrete: bool,
    has_continuous: bool,
    nonlinear_terms: str,
    sequencing_dominated: bool,
    n_discrete_vars: int,
    needs_optimality_proof: bool,
    time_budget_s: float,
    has_mip_solver: bool,
) -> list[str]:
    """Rank model types for an assessed problem; first entry is the primary pick.

    nonlinear_terms is one of 'none', 'linearizable', 'hard'.
    """
    if not has_discrete and nonlinear_terms == "none":
        return ["LP (check for network-flow structure first)"]
    recs: list[str] = []
    if sequencing_dominated and not has_continuous:
        recs.append("CP (boolean/interval model in CP-SAT)")
    if nonlinear_terms in ("none", "linearizable") and has_mip_solver:
        label = "MIP after linearization" if nonlinear_terms == "linearizable" else "MIP"
        recs.append(label)
    out_of_reach = n_discrete_vars > 1_000_000 or time_budget_s < 1.0
    if out_of_reach or nonlinear_terms == "hard" or not has_mip_solver:
        recs.append("metaheuristic (validate against exact on small instances)")
    if needs_optimality_proof and recs and recs[0].startswith("metaheuristic"):
        recs.append("decompose the exact model rather than abandoning the proof")
    return recs or ["MIP"]


# Tiny synthetic check: the production-distribution profile from the estimator above.
ranking = recommend_model_type(
    has_discrete=True, has_continuous=True, nonlinear_terms="none",
    sequencing_dominated=False, n_discrete_vars=1_500,
    needs_optimality_proof=True, time_budget_s=3600.0, has_mip_solver=True,
)
print(ranking)
# Expected: ['MIP'] -- discrete + continuous mix, fully linear, small enough,
# proof required, solver available: the exact branch wins without contest.
```

## Worked Example 1: Production–Distribution Planning (prose to MIP)

**The word problem, as a stakeholder states it.** "We run two plants, A and B, and serve three regional warehouses with two product families. Making a family at a plant during the month means setting up a line, which has a fixed cost. Each plant has a monthly machine-hour budget; products consume hours at plant-specific rates. Production cost per unit differs by plant, and shipping a unit from a plant to a warehouse has a known cost. Warehouse demand per family must be met exactly. We want the cheapest overall plan."

**Step-by-step extraction (protocol steps 1–5).**

| Protocol step | Result |
|---|---|
| 1. One sentence | Choose where to set up, how much to make, and how to ship, to minimize setup + production + shipping cost, subject to demand and machine-hour capacity. |
| 2. Sets | $P$ plants, $W$ warehouses, $K$ product families |
| 2. Parameters | $b_p$ capacity [h], $a_{pk}$ rate [h/unit], $f_{pk}$ setup [EUR], $c_{pk}$ unit cost [EUR/unit], $s_{pw}$ shipping [EUR/unit], $d_{wk}$ demand [units] |
| 3. Variables | $y_{pk} \ge 0$ units made; $x_{pwk} \ge 0$ units shipped; $z_{pk} \in \{0,1\}$ setup decision |
| 4. Objective | $\sum f_{pk} z_{pk} + \sum c_{pk} y_{pk} + \sum s_{pw} x_{pwk}$, all in EUR |
| 5. Constraints | flow balance, demand (hard), capacity (hard), fixed-charge link |

The formal model:

$$
\begin{aligned}
\min \quad & \sum_{p,k} f_{pk} z_{pk} + \sum_{p,k} c_{pk} y_{pk} + \sum_{p,w,k} s_{pw} x_{pwk} \\
\text{s.t.} \quad & \sum_{w} x_{pwk} = y_{pk} && \forall p \in P,\, k \in K && \text{(ship what you make)} \\
& \sum_{p} x_{pwk} = d_{wk} && \forall w \in W,\, k \in K && \text{(meet demand)} \\
& \sum_{k} a_{pk}\, y_{pk} \le b_p && \forall p \in P && \text{(machine hours)} \\
& y_{pk} \le M_{pk}\, z_{pk} && \forall p \in P,\, k \in K && \text{(fixed charge)} \\
& y, x \ge 0, \quad z \in \{0,1\}
\end{aligned}
$$

The only modeling subtlety is $M_{pk}$. A lazy $M = 10^6$ wrecks the LP relaxation; the tight value is the most product $k$ that plant $p$ could ever usefully make: $M_{pk} = \min\!\big(b_p / a_{pk},\; \sum_w d_{wk}\big)$. This is the simplest instance of the tightening discipline covered in **linearization-techniques**.

**Protocol step 2 includes the data audit.** Run it before building the model — an aggregate-infeasible or unit-inconsistent instance wastes a modeling iteration.

```python
import numpy as np


def audit_instance(
    cap: dict[str, float],
    hours: dict[tuple[str, str], float],
    demand: dict[tuple[str, str], float],
    ship: dict[tuple[str, str], float],
) -> list[str]:
    """Audit a production-distribution instance before any model is built.

    Returns a list of findings; an empty list means every check passed.
    """
    findings: list[str] = []
    plants = set(cap)
    families = {k for (_, k) in hours}

    # 1. Index consistency: every (plant, family) pair needs an hours entry,
    #    and shipping costs must not reference unknown plants.
    missing = [(p, k) for p in plants for k in families if (p, k) not in hours]
    if missing:
        findings.append(f"missing hours entries: {sorted(missing)}")
    dangling = sorted({p for (p, _) in ship if p not in plants})
    if dangling:
        findings.append(f"shipping costs reference unknown plants: {dangling}")

    # 2. Sign checks at the data boundary (the one place defensive checks belong).
    for name, table in [("cap", cap), ("hours", hours), ("demand", demand), ("ship", ship)]:
        bad = {key: v for key, v in table.items() if v < 0}
        if bad:
            findings.append(f"negative values in {name}: {bad}")

    # 3. Necessary feasibility condition: even with the cheapest-hours plant
    #    making everything, total demand must fit total capacity.
    needed = sum(
        sum(d for (_, kk), d in demand.items() if kk == k)
        * min(hours[p, k] for p in plants)
        for k in families
    )
    have = sum(cap.values())
    if needed > have:
        findings.append(f"aggregate infeasible: need >= {needed:.0f} h, have {have:.0f} h")

    # 4. Numerical scale: coefficient ratios beyond ~1e6 invite solver trouble
    #    (Klotz & Newman 2013, practical guidelines for difficult MIPs).
    values = np.array([v for t in (cap, hours, demand, ship) for v in t.values() if v > 0])
    if values.size and values.max() / values.min() > 1e6:
        findings.append(f"coefficient range {values.min():.2g}..{values.max():.2g}: rescale units")
    return findings


cap = {"A": 100.0, "B": 80.0}
hours = {("A", "k1"): 1.0, ("A", "k2"): 2.0, ("B", "k1"): 1.5, ("B", "k2"): 1.0}
demand = {("w1", "k1"): 10.0, ("w1", "k2"): 5.0, ("w2", "k1"): 15.0,
          ("w2", "k2"): 10.0, ("w3", "k1"): 5.0, ("w3", "k2"): 5.0}
ship = {("A", "w1"): 1.0, ("A", "w2"): 2.0, ("A", "w3"): 3.0,
        ("B", "w1"): 3.0, ("B", "w2"): 2.0, ("B", "w3"): 1.0}
print(audit_instance(cap, hours, demand, ship))
# Expected: [] -- index-consistent, nonnegative, aggregate-feasible, well-scaled.
```

**Protocol step 7: build the model and validate on the hand-checkable instance.** The instance is small enough to reason about manually: producing family k1 at A and k2 at B costs setups 50+40, production 60+40, shipping 55+40 — total 285 — and no other setup pattern beats it.

```python
import gurobipy as gp
from gurobipy import GRB


def build_production_distribution(
    cap: dict[str, float],
    hours: dict[tuple[str, str], float],
    fixed: dict[tuple[str, str], float],
    var_cost: dict[tuple[str, str], float],
    ship: dict[tuple[str, str], float],
    demand: dict[tuple[str, str], float],
) -> tuple[gp.Model, dict[str, gp.tupledict]]:
    """Build the production-distribution MIP exactly as formulated above."""
    plants = sorted(cap)
    families = sorted({k for (_, k) in hours})
    warehouses = sorted({w for (w, _) in demand})
    total_demand = {k: sum(demand[w, k] for w in warehouses) for k in families}

    m = gp.Model("prod_dist")
    y = m.addVars(plants, families, name="y")
    x = m.addVars(plants, warehouses, families, name="x")
    z = m.addVars(plants, families, vtype=GRB.BINARY, name="z")

    m.addConstrs(
        (y[p, k] == x.sum(p, "*", k) for p in plants for k in families),
        name="flow",
    )
    m.addConstrs(
        (x.sum("*", w, k) == demand[w, k] for w in warehouses for k in families),
        name="demand",
    )
    m.addConstrs(
        (gp.quicksum(hours[p, k] * y[p, k] for k in families) <= cap[p] for p in plants),
        name="capacity",
    )
    # Tight big-M: production of k at p never exceeds the capacity bound or total demand.
    big_m = {
        (p, k): min(cap[p] / hours[p, k], total_demand[k])
        for p in plants for k in families
    }
    m.addConstrs(
        (y[p, k] <= big_m[p, k] * z[p, k] for p in plants for k in families),
        name="setup_link",
    )
    m.setObjective(
        gp.quicksum(fixed[p, k] * z[p, k] + var_cost[p, k] * y[p, k]
                    for p in plants for k in families)
        + gp.quicksum(ship[p, w] * x[p, w, k]
                      for p in plants for w in warehouses for k in families),
        GRB.MINIMIZE,
    )
    return m, {"y": y, "x": x, "z": z}


cap = {"A": 100.0, "B": 80.0}
hours = {("A", "k1"): 1.0, ("A", "k2"): 2.0, ("B", "k1"): 1.5, ("B", "k2"): 1.0}
fixed = {("A", "k1"): 50.0, ("A", "k2"): 60.0, ("B", "k1"): 70.0, ("B", "k2"): 40.0}
var_cost = {("A", "k1"): 2.0, ("A", "k2"): 3.0, ("B", "k1"): 2.5, ("B", "k2"): 2.0}
ship = {("A", "w1"): 1.0, ("A", "w2"): 2.0, ("A", "w3"): 3.0,
        ("B", "w1"): 3.0, ("B", "w2"): 2.0, ("B", "w3"): 1.0}
demand = {("w1", "k1"): 10.0, ("w1", "k2"): 5.0, ("w2", "k1"): 15.0,
          ("w2", "k2"): 10.0, ("w3", "k1"): 5.0, ("w3", "k2"): 5.0}

model, mvars = build_production_distribution(cap, hours, fixed, var_cost, ship, demand)
model.Params.OutputFlag = 0
model.Params.MIPGap = 1e-6
model.Params.TimeLimit = 60
model.optimize()
if model.Status == GRB.OPTIMAL or (model.Status == GRB.TIME_LIMIT and model.SolCount > 0):
    opened = sorted((p, k) for (p, k), v in mvars["z"].items() if v.X > 0.5)
    print(f"cost={model.ObjVal:.1f} setups={opened}")
# Expected: cost=285.0, setups=[('A', 'k1'), ('B', 'k2')] -- matches the hand
# calculation: plant A makes all of family k1, plant B makes all of k2.
```

From here, scaling to 50 plants × 200 warehouses × 30 products changes only the data dictionaries — the size estimate above already showed this remains a routine MIP. Implementation details (statuses, parameters, extraction patterns) are the territory of **milp-modeling-gurobi**.

## Worked Example 2: Technician Rostering (prose to CP)

**The word problem.** "Four technicians cover a five-day week with a day shift and a night shift; each shift needs exactly one technician. Nobody works two shifts on the same day, nobody works more than four shifts in the week, and a night shift must never be followed by the next day's day shift. Technician 0 is unavailable on day 2's day shift. Spread the load as evenly as possible."

**Why CP and not MIP, by the decision tree.** Discrete decisions: yes. Continuous quantities: none — there is no cost rate, no flow, no capacity arithmetic beyond counting. The difficulty is logical structure: one-shift-per-day, a forbidden shift pattern, availability, and a min-max fairness objective. That is the CP branch. A MIP would work, but CP-SAT handles pure-boolean feasibility structure with shift-pattern logic at least as well, needs no license, and the model reads like the prose. The CP modeling toolbox (interval variables, `NoOverlap`, `Cumulative`, channeling, search hints) is covered in **constraint-programming**; here we only need booleans and linear-over-boolean sums.

**Extraction.** Sets: technicians $T$, days $D$, shifts $S = \{\text{day}, \text{night}\}$. Variables: $w_{tds} \in \{0,1\}$, "technician $t$ works shift $s$ on day $d$." Constraints: coverage $\sum_t w_{tds} = 1$; one shift per day $\sum_s w_{tds} \le 1$; weekly cap $\sum_{d,s} w_{tds} \le 4$; rest rule $w_{t,d,\text{night}} + w_{t,d+1,\text{day}} \le 1$; availability $w_{0,2,\text{day}} = 0$. Objective: minimize $\ell$ with $\ell \ge \sum_{d,s} w_{tds}$ for all $t$ (the min-max archetype from the constraint table).

```python
from ortools.sat.python import cp_model


def build_roster(
    n_techs: int,
    n_days: int,
    shifts: list[str],
    coverage: int,
    max_shifts: int,
    unavailable: set[tuple[int, int, str]],
) -> tuple[cp_model.CpModel, dict[tuple[int, int, str], cp_model.IntVar], cp_model.IntVar]:
    """Build the rostering CP-SAT model; returns (model, assignment vars, load var)."""
    model = cp_model.CpModel()
    work = {
        (t, d, s): model.new_bool_var(f"work_t{t}_d{d}_{s}")
        for t in range(n_techs) for d in range(n_days) for s in shifts
    }
    for d in range(n_days):
        for s in shifts:
            model.add(sum(work[t, d, s] for t in range(n_techs)) == coverage)
    for t in range(n_techs):
        for d in range(n_days):
            model.add_at_most_one(work[t, d, s] for s in shifts)
    for t in range(n_techs):
        model.add(sum(work[t, d, s] for d in range(n_days) for s in shifts) <= max_shifts)
        for d in range(n_days - 1):
            # Rest rule: a night shift forbids the next day's day shift.
            model.add(work[t, d, "night"] + work[t, d + 1, "day"] <= 1)
    for (t, d, s) in unavailable:
        model.add(work[t, d, s] == 0)
    # Fairness as min-max: minimize the heaviest individual load.
    max_load = model.new_int_var(0, n_days * len(shifts), "max_load")
    for t in range(n_techs):
        model.add(max_load >= sum(work[t, d, s] for d in range(n_days) for s in shifts))
    model.minimize(max_load)
    return model, work, max_load


model, work, max_load = build_roster(
    n_techs=4, n_days=5, shifts=["day", "night"], coverage=1,
    max_shifts=4, unavailable={(0, 2, "day")},
)
solver = cp_model.CpSolver()
solver.parameters.max_time_in_seconds = 10.0
status = solver.solve(model)
if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    print("status optimal:", status == cp_model.OPTIMAL, "| max load =", solver.value(max_load))
# Expected: OPTIMAL with max load = 3. Ten shifts over four technicians give the
# lower bound ceil(10/4) = 3, and a roster attaining 3 exists despite the rest rule.
```

The validation logic mirrors the MIP example: the bound $\lceil 10/4 \rceil = 3$ is hand-computable, so an optimal value of 3 confirms the model, and any other value signals a formulation bug. If this roster later gains continuous pay rates, overtime costs, and budget arithmetic, the balance tips back toward MIP — revisit the decision tree whenever the constraint mix changes.

## Advanced Techniques

### Recognizing decomposable structure

Run this test on the finished model document before solving monolithically: for each constraint family, ask "if I deleted this family, would the model fall apart into independent blocks?" Three patterns matter. **Block-angular constraints** (independent subproblems per plant/vehicle/period tied by a few linking constraints) point to Dantzig-Wolfe reformulation and column generation. **Complicating variables** (a few design variables, e.g. facility-open decisions, coupling otherwise-easy operational subproblems) point to Benders decomposition. **Stage structure** (decisions now, recourse after uncertainty) points to two-stage stochastic programming or, pragmatically, a rolling horizon. Decomposition is a formulation-time decision: the variable and constraint families must be drawn so the blocks are visible. A model that mixes plant indices into every constraint hides a block structure that a per-plant family layout would expose.

### Tightening the formulation at design time

Two formulations with identical integer-feasible sets can have wildly different LP relaxations, and relaxation strength — not variable count — usually decides whether branch-and-bound finishes. Apply at formulation time: (1) disaggregate linking constraints ($x_{ij} \le z_j$ beats $\sum_i x_{ij} \le n z_j$); (2) compute big-M values from problem data as in Worked Example 1, never as round large numbers; (3) break symmetry when identical resources exist (e.g., force $z_1 \ge z_2 \ge \dots$ over identical machines), because symmetric optima multiply the search tree; (4) prefer formulations with known tight variants — facility location, lot sizing, and routing all have documented strong/weak pairs (Vielma 2015). When a product of variables or a logical condition forces a choice between formulations, **linearization-techniques** covers the trade-offs per construct.

### Soft constraints and elastic relaxation

Constraints triaged as soft in the Initial Assessment get a violation variable and a penalty instead of a hard bound. The same pattern rescues a model that real data renders infeasible: relax the suspect families elastically, solve, and read which violations are positive. Calibrate the penalty above the largest marginal benefit a unit of violation could buy elsewhere in the objective, otherwise the solver shops for cheap violations.

```python
import gurobipy as gp
from gurobipy import GRB


def add_soft_leq(
    model: gp.Model,
    lhs: gp.LinExpr,
    rhs: float,
    penalty: float,
    name: str,
) -> gp.Var:
    """Add lhs <= rhs as a soft constraint; return the violation variable."""
    viol = model.addVar(lb=0.0, name=f"viol_{name}")
    model.addConstr(lhs - viol <= rhs, name=f"soft_{name}")
    viol.Obj = penalty
    return viol


m = gp.Model("soft_demo")
m.Params.OutputFlag = 0
make = m.addVars(["k1", "k2"], name="make")
m.addConstr(make["k1"] >= 8, name="demand_k1")
m.addConstr(make["k2"] >= 5, name="demand_k2")
# A hard capacity of 10 is infeasible (demand needs 13); make it soft instead.
overtime = add_soft_leq(m, make["k1"] + make["k2"], 10.0, penalty=100.0, name="capacity")
m.ModelSense = GRB.MINIMIZE
m.optimize()
if m.Status == GRB.OPTIMAL:
    print(f"overtime used = {overtime.X:.0f}, penalty cost = {m.ObjVal:.0f}")
# Expected: overtime used = 3, penalty cost = 300 -- the model now reports the
# violation it needs instead of returning INFEASIBLE.
```

### Surfacing multiple objectives instead of averaging them

When step 4 finds two objectives, refuse the silent weighted average. Offer the stakeholder three explicit framings: a weighted sum with the weight stated as an exchange rate in real units ("1 hour of lateness = 40 EUR"); a lexicographic order ("minimize lateness first, break ties on cost"), which Gurobi's multi-objective API and CP-SAT both support natively; or a small set of trade-off solutions generated by re-solving with the secondary objective bounded at several levels. The formulation document must record which framing was chosen and why — this is the single most common source of "the model optimizes the wrong thing" complaints.

### Moving from model to encoding when exactness is off the table

When the decision tree lands on a metaheuristic, the formulation work is not wasted — it is the specification the heuristic must honor. Translate each model element: the variable families become a solution representation (permutation, binary vector, assignment array — chosen via **solution-encodings**); the objective becomes the fitness function, recomputed independently from the model document so the heuristic and the exact model can cross-check each other on small instances; each hard constraint family gets an explicit handling decision — encode it away (representation cannot express violations), repair it, or penalize it. The handling decision per constraint family and the overall algorithm choice are the subject of **metaheuristic-design-principles**; the formulation document is its required input.

## Practical Challenges

**The stakeholder's stated objective is not the real one.** "Minimize cost" often means "minimize cost without firing anyone, breaking promised dates, or changing last year's plan too much." Probe by showing an aggressively cost-optimal solution early and recording every objection — each objection is a missing constraint or objective term. Iterate the one-sentence restatement until solutions stop surprising the stakeholder.

**Everything is presented as a hard constraint.** Real problems over-constrained this way come back infeasible. Triage each rule with "what happens if we violate it by 5%?" and move anything answerable in money or goodwill to a soft constraint with the elastic pattern above. Keep a written hard/soft register; it will be challenged later.

**The data does not exist at the model's granularity.** The model wants per-product-per-plant hours; the company tracks plant-level totals. Either aggregate the model (honest, less precise) or disaggregate the data with documented assumptions (precise-looking, fragile). Never let the model silently imply data quality that is not there — record the choice in the formulation document.

**The first solve on real data is infeasible.** Do not hand-hunt. Relax all soft-candidate families elastically and read which violations are positive, or compute an irreducible infeasible subsystem (IIS) to get a minimal conflicting constraint set. Most "infeasibilities" are data errors the audit script should have caught — extend the audit with every incident.

**The model is correct but too slow.** Diagnose before redesigning: a large MIP gap that barely moves indicates a weak relaxation (fix the formulation: tighter big-M, disaggregation, symmetry breaking); steady gap progress that is merely slow indicates size (decompose, or accept a 1–2% gap as the stopping rule); slow LP relaxations at the root indicate density or numerics (rescale, sparsify).

**Two plausible formulations of the same problem disagree.** Treat it as a bug with a bisection protocol: generate small random instances, solve both, and on the first disagreement enumerate all feasible solutions by brute force to identify which model is wrong. Disagreement is usually a quietly different interpretation of one prose sentence — update the one-sentence restatement and the constraint table when found.

**Units and scaling break the solver.** Demand in single units, budgets in millions, rates in percentages: coefficient ranges over $10^6$ cause numerical warnings, false infeasibility, and weird dual values (Klotz & Newman 2013). Fix at formulation time by choosing units that keep coefficients within a few orders of magnitude — thousands of units, millions of EUR — and record the units in the model document.

**Scope creep merges three problems into one model.** Strategic location choices, tactical capacity setting, and operational routing do not belong in one monolith re-solved nightly. Split along decision-frequency lines, pass solutions downward as fixed parameters, and revisit only if the loss from the split is demonstrably large on historical data.

## Tools & Libraries

| Library | When to use | Note |
|---|---|---|
| gurobipy | Building LP/MIP once the formulation is fixed | Fastest commercial solver; license required; see milp-modeling-gurobi |
| OR-Tools CP-SAT | Sequencing/logic-dominated models from the CP branch | Free, excellent on scheduling and rostering; integer-only arithmetic |
| HiGHS / SCIP / CBC | LP/MIP without a commercial license | HiGHS for LP and mid-size MIP; SCIP when callbacks/cuts are needed |
| PuLP / Pyomo / python-mip | Solver-agnostic model statements | Useful when the solver choice must stay open; Pyomo for larger projects |
| numpy | Data audits, instance generation, size arithmetic | Also the substrate for any later metaheuristic |
| scipy.optimize | Quick LP (`linprog`) and assignment (`linear_sum_assignment`) checks | Good for validating small instances independently |
| networkx | Detecting flow/graph structure hiding in a problem | A min-cost-flow recognition can replace a MIP entirely |
| pandas | Result and experiment tables only | Keep model data in plain dicts/arrays; tables are for reporting |

## Output Format

A complete formulation deliverable contains six artifacts, in this order:

1. **One-sentence problem statement** — the confirmed "Choose ___ to optimize ___ subject to ___."
2. **Model document** — sets, parameters with units, variables with domains and one-line meanings, objective term by term, constraint families with prose origin and hard/soft tag. Skeleton:

```text
PROBLEM: <one-sentence restatement, confirmed by stakeholder on DATE>

SETS         P plants (|P|=2), W warehouses (|W|=3), K families (|K|=2)
PARAMETERS   b_p   capacity [h]          source: machine ledger, monthly
             a_pk  rate [h/unit]         source: routing files
             d_wk  demand [units]        source: order book, frozen horizon
VARIABLES    y_pk >= 0   units of k made at p
             x_pwk >= 0  units of k shipped p -> w
             z_pk in {0,1}  1 if line for k is set up at p
OBJECTIVE    min  setup(f.z) + production(c.y) + shipping(s.x)   [EUR]
CONSTRAINTS  flow      sum_w x_pwk = y_pk        hard   "ship what you make"
             demand    sum_p x_pwk = d_wk        hard   "demand must be met"
             capacity  sum_k a_pk y_pk <= b_p    hard   "machine-hour budget"
             setup     y_pk <= M_pk z_pk         hard   M_pk = min(b_p/a_pk, D_k)
SOFT REGISTER  none yet; capacity becomes soft if overtime is purchasable
```

3. **Size estimate** — the `SizeReport` numbers for the production instance scale, with the warning list and the rule-of-thumb verdict.
4. **Data audit findings** — output of the audit script on real data, plus the list of checks run.
5. **Model-type recommendation** — the decision-tree path actually taken, with the rejected branches and one sentence on why each was rejected.
6. **Validated micro-instance** — the tiny instance, its hand-computed expectation, and the solver's matching answer, exactly as in the worked examples.

Quality gates before hand-off to implementation: every parameter has a unit and a source; every constraint family has a prose origin and a hard/soft tag; the micro-instance solves to the hand-computed value; the size estimate and method choice are consistent with the compute budget.

## Questions to Ask

- Can you state the problem as "choose ___ to optimize ___ subject to ___" — and which blank is hardest to fill?
- For each rule you stated: what concretely happens if it is violated by a little?
- Is there one objective, or several in disguise? If several, what is the exchange rate between them?
- How large is a real instance — counts for every entity type, not adjectives like "big"?
- Does the data exist at the granularity the model needs, and who owns it?
- Do you need a proven optimum, a quality guarantee, or just a good answer quickly?
- What is the compute budget per solve, and how often is the model re-solved?
- Which solvers and licenses are available in the deployment environment?
- What does the closest textbook problem look like — routing, scheduling, packing, covering, location?
- What will change next quarter — data only, or the rules themselves?

## Related Skills

- **milp-modeling-gurobi** — when the formulation is fixed and you need to build, parameterize, solve, and extract the MIP in gurobipy.
- **metaheuristic-design-principles** — when size estimation or hard nonlinearity rules out exact methods and a heuristic must be designed from the formulation document.
- **solution-encodings** — when moving from the declarative model to a representation a metaheuristic can search, with constraint-handling decided per family.
- **linearization-techniques** — when the natural formulation contains variable products, absolute values, min/max, piecewise terms, or logical conditions that must become linear.
- **constraint-programming** — when the decision tree lands on the logic/sequencing branch and the model should be built with CP-SAT booleans and intervals.
