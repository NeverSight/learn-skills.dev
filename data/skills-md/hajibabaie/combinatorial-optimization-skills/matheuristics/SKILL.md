---
name: matheuristics
description: When the user wants to hybridize a MIP solver with heuristic search — fix-and-optimize, relax-and-fix, MIP-based destroy-and-repair (LNS with exact repair), local branching, or solution polishing — including budgeting solver calls inside the loop. Also use when the user mentions "matheuristic," "fix-and-optimize," "relax-and-fix," "local branching," "MIP heuristic hybrid," "proximity search," or when the full MIP stalls while sub-MIPs with most binaries fixed solve in seconds. For heuristic destroy-repair, see large-neighborhood-search; for MIP starts and variable hints, see warm-starts-and-initial-solutions.
---

# Matheuristics

You are an expert in matheuristics — model-based heuristics that embed an exact MIP solver inside a heuristic search loop. This skill covers fix-and-optimize, relax-and-fix, MIP-based destroy-and-repair (LNS with exact repair), local branching, proximity search and polishing, and the discipline of budgeting solver calls inside the loop. The reference treatment is Maniezzo, Boschetti & Stützle (2021), "Matheuristics: Algorithms and Implementations"; for routing-flavored variants see Archetti & Speranza (2014), "A survey on matheuristics for routing problems." Use the framework below to take a user from "the full MIP stalls at a 5% gap" to a calibrated hybrid that beats both the plain solver and a plain heuristic at equal wall clock.

## Initial Assessment

Establish these facts before writing any hybrid code:

- **Full-MIP baseline.** Run the complete model with the whole time budget first. Record incumbent, bound, and gap over time. If the solver reaches an acceptable gap, stop — a matheuristic only earns its complexity when the full model stalls. The baseline is also the honesty check every result must be compared against at equal wall clock.
- **Where the difficulty lives.** Does the solver struggle to find good incumbents (weak primal side) or to move the bound (weak dual side)? Matheuristics attack the primal side only; if the bound is the problem, look at formulation tightening and cuts instead.
- **Decision core.** Which variables are the combinatorial "deciders" (usually binaries: setups, assignments, openings) and which are followers (continuous quantities that an LP determines once the binaries are set)? Fixing schemes fix only the deciders; followers always re-optimize.
- **Decomposition dimension.** Is there a natural axis to slice the binaries — time periods, items, machines, regions, vehicles? Fix-and-optimize needs one; local branching and proximity search do not.
- **Feasible start.** Does a feasible solution exist already (from a heuristic, from the solver's truncated run, from last week's plan)? If not, construction must be part of the method — relax-and-fix or a truncated MIP run.
- **Fixing feasibility.** If part of an incumbent is fixed, does the subproblem stay feasible? Hard capacities, time windows, and inventory balances can make fixings dead-end. If so, plan soft feasibility: penalized slack/overtime variables in the model, kept expensive enough to be driven to zero.
- **Sub-MIP sizing.** How many free binaries solve to optimality in 1–5 seconds on this model? Measure it: solve a few random windows of increasing size and log status and runtime. This number drives every window/radius parameter.
- **Total budget and split.** How much wall clock per instance, and how should it split between construction, improvement, and a final polishing phase? Count solver calls: budget B with per-call limit tau gives roughly B/tau calls; window schemes must fit.
- **Persistent model.** Can one model object live in memory for the whole run so fixing happens through variable bounds? Rebuilding the model per iteration is the most common self-inflicted slowdown.
- **Objective structure.** Single objective or lexicographic? Penalty terms already present? Acceptance tests and cutoffs need a single comparable scalar.
- **Solver features available.** Gurobi-class solvers expose Cutoff, MIPFocus, Start values, solution pools, and callbacks — all essential here. With CBC/HiGHS the same patterns work but per-call budgets must grow; see the library table.
- **Comparison protocol.** Instance set, seeds per instance, and equal-budget reporting against the full MIP — fix these before tuning, exactly as for any metaheuristic.

## Matheuristic Anatomy

### The defining loop

All matheuristics in this skill instantiate one template. Given the MIP $\min\{c^\top x + d^\top z : Ax + Bz \ge b,\ x \in \{0,1\}^n,\ z \ge 0\}$ with binaries $x$ and followers $z$, the outer heuristic repeatedly chooses a restriction $N(\bar{x})$ around the incumbent $\bar{x}$ and asks the solver for

$$
x^{r+1} \in \arg\min \{ c^\top x + d^\top z : (x,z) \text{ feasible},\ x \in N(x^r) \},
$$

with $N(x^r)$ small enough that the sub-MIP solves within a per-call limit $\tau$, and large enough that it contains solutions the incumbent cannot reach by small heuristic moves. The five standard choices of $N$:

| Family | Outer loop chooses | Sub-MIP solves | First reach for |
|---|---|---|---|
| Fix-and-optimize | a window $W$ of binaries to free | full model with $x_j = \bar{x}_j$ for $j \notin W$ | rolling structures: lot sizing, rostering, multi-period plans |
| Relax-and-fix | a stage order (construction, no incumbent needed) | integer stage, LP-relaxed future, fixed past | building the first feasible solution |
| MIP-based destroy-repair | a randomized destroy set plus acceptance | exact reinsertion of the destroyed part | tight constraints where greedy repair dead-ends |
| Local branching | a Hamming-ball radius $k$ and recentering | model intersected with the ball around $\bar{x}$ | generic binary MIPs with no visible decomposition |
| Proximity search / polishing | an improvement threshold $\theta$ | min distance to $\bar{x}$ subject to improving by $\theta$ | refining a good incumbent late in the run |

Close relatives worth knowing by name: kernel search (Angelelli, Mansini & Speranza 2010) builds the window from LP information — solve the LP, take variables with nonzero value or small reduced cost as the kernel, then scan "buckets" of the rest; the corridor method (Sniedovich & Voß 2006) imposes a corridor constraint around the incumbent for an exact method other than B&B; POPMUSIC (Taillard & Voß 2002) is fix-and-optimize with parts defined by solution structure. Inside the solver, RINS (Danna, Rothberg & Le Pape 2005, "Exploring relaxation induced neighborhoods to improve MIP solutions") fixes the variables on which the node LP and the incumbent agree and solves the rest — the same idea used automatically at B&B nodes — and solution polishing (Rothberg 2007, "An evolutionary algorithm for polishing mixed integer programming solutions") runs combination/mutation sub-MIPs over a pool of incumbents.

### The two fixing schemes

**Fix-and-optimize** (also "exchange"; Pochet & Wolsey 2006, "Production Planning by Mixed Integer Programming"; Helber & Sahling 2010 for the multi-level CLSP) improves a feasible $\bar{x}$. For a window $W$:

$$
N_{\text{FO}}(\bar{x}, W) = \{ x \in \{0,1\}^n : x_j = \bar{x}_j \ \ \forall j \notin W \}.
$$

Each sub-MIP searches $2^{|W|}$ assignments exactly while the followers $z$ re-optimize globally, so the objective is always the true objective. Windows sweep a decomposition dimension with overlap; passes repeat until a full pass yields no improvement. Monotone descent, no acceptance test needed.

**Relax-and-fix** (Pochet & Wolsey 2006; Stadtler 2003 for rolling lot-sizing windows) constructs a solution when none exists. Order the binaries into stages $S_1, \dots, S_m$ (e.g., by time). Stage $s$ solves a model where $S_s$ is integer, $S_1, \dots, S_{s-1}$ are fixed to earlier results, and $S_{s+1}, \dots, S_m$ are LP-relaxed to $[0,1]$. The relaxed future gives lookahead that pure greedy construction lacks. The stage-1 objective is a valid lower bound on the full MIP (it is a relaxation); later stages are not bounds, because fixings have entered. Failure mode: a stage can be infeasible given earlier fixings — counter with stage overlap (re-open the previous stage) or penalized slack in the model.

### The two distance schemes

**Local branching** (Fischetti & Lodi 2003, "Local branching") needs no decomposition. Around incumbent $\bar{x}$ with support $S = \{j : \bar{x}_j = 1\}$, the Hamming ball of radius $k$ is the single linear constraint

$$
\Delta(x, \bar{x}) = \sum_{j \in S} (1 - x_j) + \sum_{j \notin S} x_j \ \le\ k .
$$

Solve the model plus the ball with a node time limit and a cutoff just below $f(\bar{x})$, so only strict improvements are returned. Manage $k$: improvement found — recenter and reset $k$; time-out without improvement — halve $k$ (the ball was too hard to search); ball proven empty — add the reverse cut $\Delta(x,\bar{x}) \ge k+1$ (a valid "tabu" region, since the objective threshold only ever decreases) and enlarge $k$. When the cardinality of the support is constant (assignment/partitioning structure, $\sum_i x_{ij} = 1$), the asymmetric form $\sum_{j \in S}(1-x_j) \le k$ is equivalent up to a factor 2 and halves the constraint length.

**Proximity search** (Fischetti & Monaci 2014, "Proximity search for 0-1 mixed-integer convex programming") flips the roles of objective and constraint: add the improvement cut $c^\top x \le c^\top \bar{x} - \theta$, replace the objective by $\min \Delta(x, \bar{x})$, and stop at the first feasible point. The solver's heuristics are very good at "find any solution near here," so each step is cheap; iterate with recentering until $\theta$ cannot be met.

### Decision guidance

- **Full MIP first.** Always. It is the baseline, and its truncated run is a free initial incumbent.
- **Natural axis + feasible start → fix-and-optimize.** The workhorse for lot sizing, rostering, and multi-period planning.
- **No start → relax-and-fix** to construct, then fix-and-optimize to improve. The classic pairing.
- **No visible decomposition → local branching** (early, when improvements are easy) and **proximity search** (late, to squeeze a good incumbent). Both treat the model as a black box.
- **Destroy logic known, repair hard → MIP-based destroy-repair.** When greedy repair keeps producing infeasible or poor completions, let the solver repair exactly; see large-neighborhood-search for the destroy side.
- **Sub-MIPs barely faster than the full model → stop.** If freeing 10% of the binaries already takes half the full-model solve time, the model has little decomposable slack; invest in the formulation instead.

### Parameter guidance

| Parameter | Typical range | Increasing it buys | At the cost of |
|---|---|---|---|
| Window size $|W|$ | 5–25% of binaries; sized so ~80% of sub-MIPs prove optimality within $\tau$ | larger exact moves per solve | longer sub-solves, fewer windows per budget |
| Window overlap | 25–50% of window width | improvements that straddle window borders | more solves per pass |
| Per-call limit $\tau$ | 1–30 s | more windows searched to proof | fewer calls in the budget |
| Sub-MIP gap limit | 0.1–1% (MIPGap per call) | no tail-chasing inside windows | slightly worse window optima |
| Passes $P$ | 2–6, stop on a no-improvement pass | extra polishing | diminishing returns |
| Relax-and-fix stage width | 2–6 periods (or one resource block) | better lookahead, fewer myopic fixings | slower stages |
| Local-branching $k_0$ | 5–20 | richer balls, bigger jumps | node time-outs, $k$ collapses |
| Node time limit (LB) | 5–60 s | balls searched to proof, reverse cuts valid | slower recentering |
| Proximity $\theta$ | 0.1–1% of incumbent objective | meaningful step per solve | steps prove infeasible sooner |

### Budgeting solver calls

The budget arithmetic is unforgiving: passes × windows × $\tau$ must fit the wall clock, with construction and the equal-budget baseline on top. Three rules keep it honest. First, log the status of every sub-solve; if most hit TIME_LIMIT, shrink the window or raise $\tau$ — exact repair that never proves anything is just an expensive heuristic. Second, set `MIPFocus=1` and a per-call `MIPGap` of 0.5–1%: sub-MIPs exist to find good solutions fast, not to prove tight bounds. Third, warm-start every call from the incumbent (`Start` values on the freed variables); the solver then begins with a feasible point and every call is a pure improvement attempt.

## Reusable Engines

The two engines below are problem-independent: they see the model through a `dict` mapping a hashable key to its binary variable, and they fix exclusively through variable bounds on one persistent model — the model is never rebuilt.

```text
FIX-AND-OPTIMIZE(model M, binaries B, feasible start x̄, windows, passes P, τ)
  fix every binary to x̄ (by bounds); solve M        // continuous completion:
  f* <- objective                                    // true cost of the start
  for pass p = 1..P:
      for each window W in windows(p):               // W ⊆ B is the free set
          unfix W; MIP-start W from x̄
          solve M with time limit τ                  // exact inside W
          if objective < f* - ε:  f* <- objective;  x̄|W <- solution
          re-fix W to x̄
      if the pass improved nothing: stop
  unfix everything; return x̄, f*
```

```python
import math
from dataclasses import dataclass, field
from typing import Callable, Hashable, Iterable

import gurobipy as gp
from gurobipy import GRB

Key = Hashable


@dataclass
class FixOptResult:
    """Incumbent, objective, and per-solve trace of a fix-and-optimize run."""
    incumbent: dict[Key, int]
    objective: float
    history: list[tuple[int, float, float]] = field(default_factory=list)


def solve_sub_mip(model: gp.Model, time_limit: float) -> float:
    """Solve the current sub-MIP; return its best objective, or +inf if none."""
    model.Params.TimeLimit = time_limit
    model.optimize()
    ok = model.Status in (GRB.OPTIMAL, GRB.TIME_LIMIT) and model.SolCount > 0
    return model.ObjVal if ok else math.inf


def fix_and_optimize(
    model: gp.Model,
    binaries: dict[Key, gp.Var],
    start: dict[Key, int],
    windows: Callable[[int], Iterable[set[Key]]],
    passes: int = 4,
    time_per_solve: float = 5.0,
    tol: float = 1e-6,
) -> FixOptResult:
    """Improve `start` by re-optimizing one window of binaries at a time.

    `model` is the full minimization model. `binaries` maps a key to its
    binary variable; continuous variables are never fixed and re-optimize
    in every sub-MIP, so objectives are always true objectives.
    `windows(pass_idx)` yields the key sets left free in each sub-MIP of
    that pass. Fixing happens through bounds on one persistent model.
    """
    model.Params.OutputFlag = 0
    model.Params.MIPFocus = 1            # sub-MIPs exist to find solutions fast
    incumbent = {k: int(round(v)) for k, v in start.items()}

    for k, var in binaries.items():      # evaluate the start: everything fixed
        var.LB = var.UB = incumbent[k]
    best = solve_sub_mip(model, time_per_solve)
    if math.isinf(best):
        raise ValueError(f"start solution infeasible (status {model.Status})")
    history = [(0, best, model.Runtime)]

    n_solve = 0
    for p in range(passes):
        improved_in_pass = False
        for window in windows(p):
            n_solve += 1
            for k in window:             # free the window, warm-start it
                binaries[k].LB, binaries[k].UB = 0.0, 1.0
                binaries[k].Start = incumbent[k]
            obj = solve_sub_mip(model, time_per_solve)
            if obj < best - tol:
                best = obj
                incumbent.update({k: int(round(binaries[k].X)) for k in window})
                improved_in_pass = True
            for k in window:             # re-fix to the (possibly new) incumbent
                binaries[k].LB = binaries[k].UB = incumbent[k]
            history.append((n_solve, best, model.Runtime))
        if not improved_in_pass:         # a full pass changed nothing: stop
            break
    for var in binaries.values():        # hand back the unfixed model
        var.LB, var.UB = 0.0, 1.0
    return FixOptResult(incumbent, best, history)
```

The companion constructor builds the start that fix-and-optimize needs. Stages are processed in order; each stage is integer, the past is fixed, the future stays LP-relaxed:

```python
from typing import Hashable, Sequence

import gurobipy as gp
from gurobipy import GRB

Key = Hashable


def relax_and_fix(
    model: gp.Model,
    binaries: dict[Key, gp.Var],
    stages: Sequence[set[Key]],
    time_per_solve: float = 10.0,
    overlap: int = 0,
) -> dict[Key, int]:
    """Construct a feasible solution with a rolling integer window.

    Stage s solves a MIP in which stages[s] (plus the previous `overlap`
    stages, re-opened) is binary, later stages are LP-relaxed to [0, 1],
    and earlier stages are fixed to their solved values. Returns the
    constructed binary solution; raises RuntimeError if a stage dead-ends
    (then: increase `overlap`, widen stages, or add penalized slack to the
    model so fixings cannot cut off feasibility).
    """
    model.Params.OutputFlag = 0
    model.Params.TimeLimit = time_per_solve
    for var in binaries.values():            # everything starts relaxed
        var.VType = GRB.CONTINUOUS
        var.LB, var.UB = 0.0, 1.0
    fixed: dict[Key, int] = {}
    for s, stage in enumerate(stages):
        integer_now = set(stage)
        for back in range(1, overlap + 1):   # re-open recent stages
            if s - back >= 0:
                integer_now |= stages[s - back]
        for k in integer_now:
            binaries[k].VType = GRB.BINARY
            if k in fixed:                   # unfix re-opened keys
                binaries[k].LB, binaries[k].UB = 0.0, 1.0
        model.optimize()
        if model.SolCount == 0:
            raise RuntimeError(
                f"relax-and-fix dead-ended at stage {s} (status {model.Status})")
        for k in integer_now:
            fixed[k] = int(round(binaries[k].X))
            binaries[k].LB = binaries[k].UB = fixed[k]
    for var in binaries.values():            # restore the full MIP
        var.VType = GRB.BINARY
        var.LB, var.UB = 0.0, 1.0
    return fixed
```

## Worked Application 1: Lot Sizing by Relax-and-Fix + Fix-and-Optimize

The capacitated lot-sizing problem (CLSP) is the canonical fix-and-optimize testbed (Trigeiro, Thomas & McClain 1989, "Capacitated lot sizing with setup times"). Items $i$, periods $t$, demand $d_{it}$, setup cost $f_i$ and setup time $st_i$, holding cost $h_i$, capacity $C_t$, overtime $o_t$ at unit cost $c^o$:

$$
\min \sum_{i,t} \big( f_i\, y_{it} + h_i\, s_{it} \big) + c^o \sum_t o_t
$$

subject to inventory balance $s_{i,t-1} + x_{it} = d_{it} + s_{it}$, the setup link $x_{it} \le M_{it} y_{it}$ with the tight big-M $M_{it} = \sum_{\tau \ge t} d_{i\tau}$, and capacity $\sum_i (x_{it} + st_i\, y_{it}) \le C_t + o_t$. The penalized overtime keeps every sub-MIP feasible no matter what the outer loop fixes — the standard soft-feasibility device in matheuristics. The deciders are the setups $y$; quantities $x, s, o$ are followers. For valid inequalities and reformulations that strengthen this model, see lot-sizing.

```python
from dataclasses import dataclass

import gurobipy as gp
import numpy as np
from gurobipy import GRB


@dataclass(frozen=True)
class ClspInstance:
    """Capacitated lot sizing: items i = 0..n-1, periods t = 0..T-1."""
    demand: np.ndarray        # (n, T)
    setup_cost: np.ndarray    # (n,)
    holding_cost: np.ndarray  # (n,)
    setup_time: np.ndarray    # (n,)
    capacity: np.ndarray      # (T,)
    overtime_cost: float


def random_clsp(n_items: int, n_periods: int, seed: int,
                utilization: float = 0.85) -> ClspInstance:
    """Trigeiro-style instance; tight capacity, feasibility via overtime."""
    rng = np.random.default_rng(seed)
    demand = rng.integers(40, 141, size=(n_items, n_periods)).astype(float)
    setup_cost = rng.uniform(300.0, 900.0, n_items)
    holding_cost = rng.uniform(1.0, 4.0, n_items)
    setup_time = rng.uniform(10.0, 50.0, n_items)
    load = demand.sum(axis=0) + setup_time.sum()
    capacity = np.full(n_periods, utilization * load.mean())
    return ClspInstance(demand, setup_cost, holding_cost, setup_time,
                        capacity, overtime_cost=25.0)


def build_clsp(inst: ClspInstance) -> tuple[gp.Model,
                                            dict[tuple[int, int], gp.Var]]:
    """CLSP MIP. Returns the model and its setup binaries y[i, t]."""
    n, T = inst.demand.shape
    m = gp.Model("clsp")
    x = m.addVars(n, T, name="x")                       # production
    s = m.addVars(n, T, name="s")                       # end inventory
    o = m.addVars(T, name="o")                          # overtime (soft slack)
    y = m.addVars(n, T, vtype=GRB.BINARY, name="y")     # setups: the deciders
    m.setObjective(
        gp.quicksum(inst.setup_cost[i] * y[i, t] + inst.holding_cost[i] * s[i, t]
                    for i in range(n) for t in range(T))
        + inst.overtime_cost * o.sum(), GRB.MINIMIZE)
    m.addConstrs(
        ((s[i, t - 1] if t > 0 else 0.0) + x[i, t] == inst.demand[i, t] + s[i, t]
         for i in range(n) for t in range(T)), name="balance")
    rem = inst.demand[:, ::-1].cumsum(axis=1)[:, ::-1]  # tight big-M
    m.addConstrs((x[i, t] <= rem[i, t] * y[i, t]
                  for i in range(n) for t in range(T)), name="setup_link")
    m.addConstrs(
        (gp.quicksum(x[i, t] + inst.setup_time[i] * y[i, t] for i in range(n))
         <= inst.capacity[t] + o[t] for t in range(T)), name="capacity")
    m.update()
    return m, {(i, t): y[i, t] for i in range(n) for t in range(T)}
```

The run constructs with relax-and-fix over 6-period time stages (overlap 1), then improves with fix-and-optimize, alternating time windows and item windows between passes — alternating the decomposition dimension is what lets the method escape the blind spots of either slicing:

```python
import time


def time_windows(n_items: int, n_periods: int, width: int,
                 step: int) -> list[set[tuple[int, int]]]:
    """Overlapping windows over periods: all items, t in [t0, t0 + width)."""
    return [{(i, t) for i in range(n_items)
             for t in range(t0, min(t0 + width, n_periods))}
            for t0 in range(0, max(n_periods - width, 0) + 1, step)]


def item_windows(n_items: int, n_periods: int,
                 block: int) -> list[set[tuple[int, int]]]:
    """Windows over items: all periods for `block` items at a time."""
    return [{(i, t) for i in range(i0, min(i0 + block, n_items))
             for t in range(n_periods)}
            for i0 in range(0, n_items, block)]


inst = random_clsp(n_items=30, n_periods=60, seed=7)   # 1800 setup binaries
model, y = build_clsp(inst)
n_items, n_periods = inst.demand.shape

t0 = time.time()
stages = [{(i, t) for i in range(n_items)
           for t in range(s0, min(s0 + 6, n_periods))}
          for s0 in range(0, n_periods, 6)]
start = relax_and_fix(model, y, stages, time_per_solve=5.0, overlap=1)


def clsp_windows(p: int) -> list[set[tuple[int, int]]]:
    """Alternate the decomposition dimension between passes."""
    if p % 2 == 0:
        return time_windows(n_items, n_periods, width=6, step=3)
    return item_windows(n_items, n_periods, block=5)


result = fix_and_optimize(model, y, start, clsp_windows,
                          passes=4, time_per_solve=3.0)
wall = time.time() - t0

full, _ = build_clsp(inst)                # honest equal-budget comparison
full.Params.OutputFlag = 0
full.Params.TimeLimit = wall
full.optimize()
assert full.SolCount > 0
print(f"relax-and-fix start {result.history[0][1]:.0f} -> "
      f"fix-and-optimize {result.objective:.0f} "
      f"({len(result.history) - 1} sub-MIPs, {wall:.0f}s)")
print(f"full MIP at {wall:.0f}s: obj {full.ObjVal:.0f}, "
      f"bound {full.ObjBound:.0f}")
# Expected (Gurobi 13; time-limit-driven, so machine-dependent): relax-and-
# fix start ~814000; fix-and-optimize ~785000 after ~25 sub-MIPs, ~125s in
# total. The full MIP given the same wall clock returns ~787000 over bound
# ~776000 -- the hybrid wins at equal budget, with margin growing in size.
```

Two design points carry the example. First, the per-solve trace in `result.history` shows which windows produced the improvements; in CLSP almost all gains come from time windows around capacity-tight periods, which is the signal to add more overlap exactly there. Second, the equal-budget full-MIP line is not decoration — without it, a matheuristic result is unreviewable.

## Worked Application 2: Generalized Assignment by Local Branching

The generalized assignment problem (GAP) assigns each job $j$ to exactly one agent $i$, minimizing $\sum_{ij} c_{ij} x_{ij}$ subject to $\sum_i x_{ij} = 1$ and agent budgets $\sum_j a_{ij} x_{ij} \le b_i$. There is no natural window dimension — capacity couples every job on an agent — so local branching is the right matheuristic. Because $\sum_i x_{ij} = 1$ fixes the support size at $n$, the asymmetric ball $\sum_{(i,j): \bar{x}_{ij}=1} (1 - x_{ij}) \le k$ reads "at most $k$ jobs change agent."

```text
LOCAL-BRANCHING(model M, binaries B, k0, node time τ, total budget T)
  x̄ <- incumbent from a truncated run of M       // any feasible point works
  k <- k0
  while budget remains and 1 <= k <= |support(x̄)|:
      add ball Δ(x, x̄) <= k;  set Cutoff just below f(x̄)
      solve M for at most τ seconds
      improved          -> recenter at the new incumbent;  k <- k0
      time-out, none    -> k <- k/2                // ball too large to search
      proven empty      -> add reverse cut Δ(x, x̄) >= k+1;  k <- k + k0/2
      remove the ball
  return the best incumbent found
```

```python
from dataclasses import dataclass

import gurobipy as gp
import numpy as np
from gurobipy import GRB


@dataclass(frozen=True)
class GapInstance:
    """Generalized assignment: agents i = 0..m-1, jobs j = 0..n-1."""
    cost: np.ndarray      # (m, n)
    resource: np.ndarray  # (m, n)
    budget: np.ndarray    # (m,)


def random_gap(n_agents: int, n_jobs: int, seed: int,
               tightness: float = 0.8) -> GapInstance:
    """OR-Library class-D style: cost anti-correlated with resource (hard)."""
    rng = np.random.default_rng(seed)
    resource = rng.integers(1, 101, size=(n_agents, n_jobs)).astype(float)
    cost = 111.0 - resource + rng.integers(-10, 11, size=(n_agents, n_jobs))
    budget = tightness * resource.sum(axis=1) / n_agents
    return GapInstance(cost, resource, budget)


def build_gap(inst: GapInstance) -> tuple[gp.Model,
                                          dict[tuple[int, int], gp.Var]]:
    """GAP MIP: every job to exactly one agent, within agent budgets."""
    m_agents, n_jobs = inst.cost.shape
    m = gp.Model("gap")
    x = m.addVars(m_agents, n_jobs, vtype=GRB.BINARY, name="x")
    m.setObjective(
        gp.quicksum(inst.cost[i, j] * x[i, j]
                    for i in range(m_agents) for j in range(n_jobs)),
        GRB.MINIMIZE)
    m.addConstrs((x.sum("*", j) == 1 for j in range(n_jobs)), name="assign")
    m.addConstrs(
        (gp.quicksum(inst.resource[i, j] * x[i, j] for j in range(n_jobs))
         <= inst.budget[i] for i in range(m_agents)), name="budget")
    m.update()
    return m, {(i, j): x[i, j] for i in range(m_agents) for j in range(n_jobs)}
```

The loop uses the solver's `Cutoff` parameter so a sub-solve can only return strict improvements; a proven-empty ball is then status `CUTOFF` (or `INFEASIBLE` once reverse cuts accumulate), which is a proof, not an error:

```python
from typing import Hashable

import gurobipy as gp
from gurobipy import GRB

Key = Hashable


def local_branching(
    model: gp.Model,
    binaries: dict[Key, gp.Var],
    k0: int = 15,
    node_time: float = 5.0,
    total_time: float = 60.0,
) -> tuple[dict[Key, int], float, list[tuple[float, float]]]:
    """Local branching (Fischetti & Lodi 2003) for a minimization MIP.

    Uses the asymmetric Hamming ball over the incumbent support, valid
    whenever the number of ones is constant across feasible solutions
    (assignment / partitioning structure). Returns (best solution,
    objective, trace of (clock, incumbent objective))."""
    model.Params.OutputFlag = 0
    model.Params.MIPFocus = 1
    model.Params.TimeLimit = min(node_time, total_time)
    model.optimize()                     # truncated run -> first incumbent
    if model.SolCount == 0:
        raise RuntimeError(f"no initial solution (status {model.Status})")
    center = {key: int(round(var.X)) for key, var in binaries.items()}
    best, best_obj = dict(center), model.ObjVal
    clock = model.Runtime
    trace = [(clock, best_obj)]
    k, n_tabu = k0, 0
    n_ones = sum(center.values())

    while clock < total_time and 1 <= k <= n_ones:
        support = [binaries[key] for key, v in center.items() if v == 1]
        ball = model.addConstr(gp.quicksum(1 - v for v in support) <= k,
                               name="lb_ball")
        model.Params.TimeLimit = min(node_time, total_time - clock)
        model.Params.Cutoff = best_obj - 1e-6   # improvements only
        model.optimize()
        clock += model.Runtime
        if model.SolCount > 0:           # strictly better by construction
            center = {key: int(round(var.X)) for key, var in binaries.items()}
            best, best_obj = dict(center), model.ObjVal
            model.remove(ball)
            k = k0                       # recenter, reset the radius
        elif model.Status == GRB.TIME_LIMIT:
            model.remove(ball)
            k //= 2                      # ball too hard to search: shrink
        else:                            # CUTOFF / INFEASIBLE: proven empty
            model.remove(ball)
            n_tabu += 1                  # forbid the explored ball for good
            model.addConstr(gp.quicksum(1 - v for v in support) >= k + 1,
                            name=f"lb_tabu_{n_tabu}")
            k += max(1, k0 // 2)         # and look further out
        trace.append((clock, best_obj))
    model.Params.Cutoff = GRB.INFINITY   # leave the model clean
    return best, best_obj, trace
```

The reverse cut deserves one line of justification: when a ball around an old center is proven to contain nothing better than the then-incumbent, it can never contain anything better than any later (smaller) incumbent, so the cut stays valid for the rest of the run. Run it on a hard class-D instance, validate independently, and compare at equal budget:

```python
import numpy as np

gap_inst = random_gap(n_agents=10, n_jobs=100, seed=3)
gap_model, x = build_gap(gap_inst)
best, obj, trace = local_branching(gap_model, x, k0=15, node_time=5.0,
                                   total_time=45.0)

# Independent validation -- never trust the loop's own bookkeeping.
assign = {j: i for (i, j), v in best.items() if v == 1}
loads = np.zeros(gap_inst.cost.shape[0])
for j, i in assign.items():
    loads[i] += gap_inst.resource[i, j]
assert len(assign) == gap_inst.cost.shape[1]
assert np.all(loads <= gap_inst.budget + 1e-6)
assert abs(sum(gap_inst.cost[i, j] for j, i in assign.items()) - obj) < 1e-6

ref, _ = build_gap(gap_inst)
ref.Params.OutputFlag = 0
ref.Params.TimeLimit = 45.0
ref.optimize()
print(f"local branching {trace[0][1]:.0f} -> {obj:.0f}; "
      f"full MIP 45s: {ref.ObjVal:.0f} (bound {ref.ObjBound:.0f})")
# Expected (Gurobi 13; time-limit-driven, so run-dependent): initial
# incumbent ~6335-6340; local branching improves it to ~6324-6331, on par
# with or better than the full MIP at equal wall clock (bound ~6318). The
# trace shows the k-management cycle: improve (k resets), time-out
# (k halves), proven-empty ball (reverse cut added, k grows).
```

## Advanced Techniques

### MIP-based destroy-and-repair

Fix-and-optimize with a *randomized* window is exactly LNS with exact repair: destroy = unfix a coherent group of binaries, repair = sub-MIP. The engine below takes the groups (one group per job, customer, period, or machine — the removable element of large-neighborhood-search) and hill-climbs over exact large moves; add Metropolis acceptance or adaptive group-family weights exactly as in large-neighborhood-search when it stalls. On the GAP instance above, freeing 40 of 100 job columns for 2-second repairs improves a truncated-run incumbent by several units within seconds.

```python
from typing import Hashable, Sequence

import gurobipy as gp
import numpy as np
from gurobipy import GRB

Key = Hashable


def mip_lns(
    model: gp.Model,
    binaries: dict[Key, gp.Var],
    start: dict[Key, int],
    groups: Sequence[Sequence[Key]],
    q: int,
    iterations: int = 50,
    time_per_solve: float = 2.0,
    seed: int = 0,
) -> tuple[dict[Key, int], float]:
    """LNS with exact repair: free q random groups of binaries, re-solve.

    Improvement-only acceptance; the destroyed part is repaired optimally
    (within the time limit) while everything else stays fixed by bounds."""
    rng = np.random.default_rng(seed)
    model.Params.OutputFlag = 0
    model.Params.MIPFocus = 1
    model.Params.TimeLimit = time_per_solve
    incumbent = {k: int(round(v)) for k, v in start.items()}
    for k, var in binaries.items():
        var.LB = var.UB = incumbent[k]
    model.optimize()
    if model.SolCount == 0:
        raise ValueError("start solution infeasible under full fixing")
    best = model.ObjVal
    for _ in range(iterations):
        chosen = rng.choice(len(groups), size=q, replace=False)
        window = [k for g in chosen for k in groups[g]]
        for k in window:
            binaries[k].LB, binaries[k].UB = 0.0, 1.0
            binaries[k].Start = incumbent[k]
        model.optimize()
        if model.SolCount > 0 and model.ObjVal < best - 1e-6:
            best = model.ObjVal
            for k in window:
                incumbent[k] = int(round(binaries[k].X))
        for k in window:
            binaries[k].LB = binaries[k].UB = incumbent[k]
    for var in binaries.values():
        var.LB, var.UB = 0.0, 1.0
    return incumbent, best
```

The destroy set should be *related* — groups that share a constraint (same agent, adjacent periods, nearby customers) — because the sub-MIP can only trade among what is simultaneously free. Random groups are the baseline; upgrade the selection with the relatedness measures from large-neighborhood-search.

### Proximity search and polishing

When fix-and-optimize and local branching both stall, proximity search often still moves: asking the solver for *any* solution at least $\theta$ better, as close as possible to the incumbent, exploits exactly what MIP heuristics are best at. `SolutionLimit=1` makes each step cheap.

```python
from typing import Hashable

import gurobipy as gp
from gurobipy import GRB

Key = Hashable


def proximity_search_step(
    model: gp.Model,
    binaries: dict[Key, gp.Var],
    center: dict[Key, int],
    center_obj: float,
    theta: float,
    time_limit: float = 10.0,
) -> dict[Key, int] | None:
    """One proximity-search step (Fischetti & Monaci 2014).

    Adds the improvement cut obj <= center_obj - theta, minimizes the
    Hamming distance to `center`, stops at the first feasible point.
    Returns the new center, or None if no improving point was found."""
    original = model.getObjective()
    cutoff = model.addConstr(original <= center_obj - theta, name="ps_cutoff")
    dist = gp.quicksum((1 - v) if center[k] == 1 else v
                       for k, v in binaries.items())
    model.setObjective(dist, GRB.MINIMIZE)
    model.Params.OutputFlag = 0
    model.Params.TimeLimit = time_limit
    model.Params.SolutionLimit = 1       # the first improving point suffices
    model.optimize()
    new_center = None
    if model.SolCount > 0:
        new_center = {k: int(round(v.X)) for k, v in binaries.items()}
    model.remove(cutoff)                 # restore the original model
    model.setObjective(original, GRB.MINIMIZE)
    model.Params.SolutionLimit = GRB.MAXINT
    return new_center
```

Iterate with recentering until a step returns `None` at the smallest useful $\theta$. This is also the cheap "polishing phase" to schedule for the last 10–20% of any matheuristic budget. Solvers ship their own polishing: Gurobi's `ImproveStartTime`/`ImproveStartGap` switch the B&B to pure solution improvement (Rothberg 2007), which is a zero-code alternative worth benchmarking against.

### Soft fixing and LP-guided windows

Hard fixing ($x_j = \bar{x}_j$) can be replaced by *soft fixing*: a local-branching constraint over the would-be-fixed set, allowing the sub-MIP to overrule a few fixings where it pays. Fischetti & Lodi's $\Delta \le k$ over the complement of the window is the standard form. LP information picks better windows than blind sweeps: solve the LP relaxation once per pass and (a) free the variables whose LP value disagrees with the incumbent (the RINS complement — Danna, Rothberg & Le Pape 2005), or (b) free variables with reduced cost near zero, the kernel-search criterion (Angelelli, Mansini & Speranza 2010). Both target exactly the variables the relaxation says are decided wrongly or barely decided.

### Adaptive window selection

Window families (time, item, machine, LP-guided, random-related) are operators; their per-family improvement-per-second statistics are rewards. Reuse the ALNS roulette and segment-update machinery from large-neighborhood-search verbatim, with one practical change: normalize rewards by sub-solve runtime, because a 30-second window that saves 100 cost units is worse than five 3-second windows saving 30 each.

### Warm starts and budget shaping across calls

Every sub-solve should start from the incumbent: set `Start` on freed variables (fixed variables are determined by bounds). For sub-MIPs that mostly prove optimality early, cap effort with a per-call `MIPGap` (0.5–1%) in addition to `TimeLimit`, and consider `BestObjStop` to return as soon as any improvement exists. Across the run, shape budgets like a cooling schedule: short calls and small windows early (many cheap improvements), longer calls and larger windows late (rare deep improvements), proximity-search polishing last. The mechanics of starts, hints, and partial starts are covered in warm-starts-and-initial-solutions; callback-level control (aborting a sub-solve once improvement stalls) in gurobi-advanced-features.

## Practical Challenges

**Sub-MIPs hit the time limit on every window.** The window is too large for the model's difficulty, or the sub-MIP inherits the full model's weak relaxation. Shrink the window until ~80% of calls prove optimality; set a per-call `MIPGap` so near-proofs terminate; check that fixing is done by bounds (presolve then removes the fixed variables — fixing by added equality constraints is much weaker). If even tiny windows are slow, the formulation is the problem, not the matheuristic.

**Relax-and-fix dead-ends or returns absurdly expensive plans.** A stage fixed itself into a corner. Add penalized slack variables (overtime, demand shortfall at high cost) so no fixing can cut off feasibility; increase stage overlap so the previous stage can be revised; widen stages so the integer window sees further. If the construction is feasible but poor, the LP-relaxed future is too optimistic — shorten stages or keep one extra stage integer.

**Fix-and-optimize stalls after the first pass.** Single-dimension windows converge to a "window-optimal" fixed point quickly. Alternate decomposition dimensions between passes, add 30–50% overlap, randomize window order, and grow window width by 50% whenever a pass fails — escalation is cheap because the pass would otherwise terminate the run anyway. Soft fixing (see Advanced Techniques) is the next escalation step.

**The first local-branching ball already times out.** $k_0$ is too large or the node budget too small; the ball sub-MIP is nearly as hard as the full model. Halve $k_0$, raise the node limit, use the asymmetric ball when support size is constant, and always warm-start the ball with the center. If the model is hard even at $k = 5$, switch to proximity search, which only needs the first feasible point.

**Gurobi reports CUTOFF and the loop treats it as a failure.** With `Cutoff` set, "no solution" is the *expected* outcome of a proven-empty ball, status `GRB.CUTOFF`. Handle the triple (improved / `TIME_LIMIT` without solution / proven empty) explicitly, as in the local-branching loop above; never read `.X` without checking `SolCount > 0`.

**Model rebuilding dominates the runtime.** Profiling shows 80% of the wall clock in model construction, not solving. Keep one persistent model; fix and free through `LB`/`UB`; cache the binary-variable dict once. Never call `model.copy()` per iteration, and batch attribute changes before the implicit `update()` that `optimize()` performs.

**The matheuristic loses to the plain MIP at equal time.** Common on small or loosely constrained instances — the solver's own heuristics (RINS, polishing) are already a strong matheuristic. Report it honestly and stop; scale tests to the instance sizes where the full model's incumbent trajectory flattens, which is where fixing schemes shine. If the loss persists at scale, the windows are misaligned with the problem's coupling structure.

**The heuristic start is rejected when fixed into the model.** Status `INFEASIBLE` on the evaluation solve usually means the start violates a constraint the heuristic ignored, or integer rounding broke a balance equation. Validate the start with an independent checker first; compute an IIS on the fully fixed model to name the violated constraints (see gurobi-advanced-features); fix tolerance mismatches by rounding before fixing, as the engines above do.

## Tools & Libraries

| Library / tool | When to use | Note |
|---|---|---|
| gurobipy | the engines in this skill | persistent model + bound fixing; `Cutoff`, `MIPFocus`, `Start`, `BestObjStop` per sub-solve |
| OR-Tools CP-SAT | exact repair on scheduling windows | `AddHint` for warm starts; strong when repair is feasibility-tight rather than cost-tight |
| python-mip (CBC) | license-free, same patterns | fix by bounds identically; expect 5–50x slower sub-solves, so grow tau |
| HiGHS (highspy) | license-free LP/MIP | excellent LP for relax-and-fix stages and LP-guided window selection |
| Pyomo persistent interfaces | solver-agnostic research code | use `gurobi_persistent`/`appsi`; plain re-solves rebuild the model and dominate runtime |
| alns (PyPI) | adaptive layer over MIP repair | register the sub-MIP repair as a repair operator; weights/acceptance come free |

## Output Format

A complete matheuristic deliverable contains:

1. **Decomposition summary** — what is fixed, what is free, and why:

| Element | Choice |
|---|---|
| Deciders / followers | setup binaries y / quantities x, s, o |
| Construction | relax-and-fix, 6-period stages, overlap 1 |
| Improvement | fix-and-optimize, time windows 6/3 alternating item blocks of 5 |
| Soft feasibility | overtime at 25/unit, verified zero in final solution |
| Polishing | proximity search, theta = 0.2% of incumbent |

2. **Budget plan** — total wall clock, per-call limit, expected number of calls, per-call parameters (`MIPFocus`, `MIPGap`, `Cutoff`), and the split construction / improvement / polishing.
3. **Run log** — one row per sub-solve: index, window or ball description, status, runtime, objective before/after, improvement. The status column is the diagnostic: mostly `OPTIMAL` means windows can grow; mostly `TIME_LIMIT` means they must shrink.
4. **Convergence summary** — start objective, best objective, time-to-best, improvement per pass; state which window family produced the gains.
5. **Equal-budget comparison** — the full MIP run at the same wall clock: incumbent, bound, and gap on both sides. A matheuristic result without this line is not reviewable.
6. **Independent validation** — feasibility check and objective recomputation of the final incumbent outside the model (no solver attributes), as in the GAP example.
7. **Reproducibility block** — instance generator seed, solver name and version, parameter dump, and machine note, since time-limit-driven results are hardware-dependent.

## Questions to Ask

- How large is the full MIP, and what gap does it reach within your time budget? What does its incumbent-over-time curve look like?
- Which variables are the combinatorial deciders, and which are continuous followers?
- Is there a natural axis to slice the deciders — periods, items, machines, regions — or is the coupling global?
- Do you already have a feasible solution from any source, or must the method construct one?
- If part of a solution is fixed, can the rest become infeasible? Which constraints would need penalized slack?
- What solver and license are available, and may one model object stay in memory for the whole run?
- What is the total wall-clock budget per instance, and over how many instances/seeds must results hold?
- What does success mean: beat the full MIP at equal time, reach a known bound, or just deliver feasibility reliably?

## Related Skills

- **milp-modeling-gurobi** — building the full model that the engines fix and free: variables, constraint builders, status handling, solution extraction.
- **large-neighborhood-search** — destroy-operator design, relatedness measures, acceptance criteria, and adaptive operator weights that drive the randomized-window variants here.
- **warm-starts-and-initial-solutions** — MIP starts, variable hints, and construction heuristics that seed every sub-solve and the overall run.
- **gurobi-advanced-features** — callbacks, IIS diagnosis, solution pools, and the parameter mechanics (`Cutoff`, `BestObjStop`, `ImproveStartTime`) used to budget sub-solves.
- **lot-sizing** — the problem-side depth behind the first worked example: Wagner-Whitin structure, (l,S) inequalities, and reformulations that make sub-MIPs solve faster.
