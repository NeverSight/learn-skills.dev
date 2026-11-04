---
name: cutting-stock
description: When the user wants to solve one-dimensional cutting stock problems — cutting demanded item widths from standard stock rolls at minimum roll usage or trim loss — with pattern-based (Gilmore-Gomory) or compact MIP models, column generation with knapsack pricing, and integer rounding. Also use when the user mentions "cutting stock," "trim loss," "cutting patterns," "stock rolls," "pattern generation," "Gilmore-Gomory," or when a covering model has one column per feasible cutting pattern. For the generic restricted-master/pricing machinery, see column-generation; for the unit-demand cousin of this problem, see bin-packing.
---

# Cutting Stock

You are an expert in the one-dimensional cutting stock problem (1D-CSP): the canonical pattern-based optimization problem and the original application of column generation (Gilmore & Gomory, 1961, "A linear programming approach to the cutting-stock problem"). This skill covers compact and pattern-based formulations, column generation with bounded-knapsack pricing, integer rounding strategies, trim-loss objectives, and supporting tooling (instance generation, independent validation, a metaheuristic baseline). Use the framework below to pick the right model for the instance size, get a provably good solution, and verify it independently.

## Initial Assessment

Establish these facts before proposing a model or writing code:

- **Instance dimensions.** Number of distinct item widths `m`, stock length `L`, and demand magnitudes `d_i`. `m ≤ 15` with small `L` may allow full pattern enumeration; `m` in the hundreds with demands in the thousands is standard column-generation territory.
- **Width data type.** Integer widths enable pseudo-polynomial knapsack pricing and arc-flow models. Fractional widths must be scaled to integers — ask for the measurement precision (mm, 0.1 mm) and check the scaled `L` stays manageable.
- **Stock assortment.** One stock length or several? Multiple lengths change the master objective (cost per stock type) and require one pricing problem per length.
- **Objective.** Minimize number of rolls, total trim loss, or material cost? With identical rolls these align, but only under a stated overproduction policy — confirm whether cutting more pieces than demanded is waste, usable inventory, or forbidden.
- **Demand semantics.** Cover-at-least (`≥ d_i`, the default, gives nonnegative duals and a clean pricing problem) or meet-exactly (`= d_i`, harder: duals can be negative, master can be infeasible with few columns)?
- **Side constraints.** Maximum number of distinct patterns (setup costs), maximum pieces per pattern (knife count), pattern run-length limits, due dates per order. These decide between vanilla Gilmore-Gomory and an extension.
- **Optimality requirement.** Is `ceil(LP bound)` or `+1` roll acceptable (almost always reached by rounding heuristics), or is a proven optimum required (branch-and-price or arc-flow)?
- **Solver availability.** Gurobi licensed? If not, the same pattern applies with HiGHS/CBC for the master and a hand-written DP for pricing — only the master LP/IP calls change.
- **Time budget.** Column generation on `m ≤ 200` converges in seconds; a compact MIP on the same instance may not finish in hours because of symmetry.
- **Validation path.** Agree up front on an independent feasibility checker (pattern widths, demand coverage) so the model and the check do not share code.

## Problem Variants and Formulation

### Formal definition

Given stock pieces of integer length $L$ and item types $i \in I = \{1,\dots,m\}$ with width $w_i \in \mathbb{Z}_{>0}$, $w_i \le L$, and demand $d_i \in \mathbb{Z}_{>0}$: cut all demanded items from the minimum number of stock pieces. A **cutting pattern** is a vector $a = (a_1,\dots,a_m) \in \mathbb{Z}_{\ge 0}^m$ with $\sum_i w_i a_i \le L$; $a_i$ counts copies of item $i$ cut from one stock piece.

**Pattern-based (Gilmore-Gomory) model.** Let $J$ index all feasible patterns and $x_j$ the number of stock pieces cut with pattern $j$:

$$\min \sum_{j \in J} x_j \quad \text{s.t.} \quad \sum_{j \in J} a_{ij}\, x_j \ \ge\ d_i \quad \forall i \in I, \qquad x_j \in \mathbb{Z}_{\ge 0}.$$

$|J|$ grows exponentially in $m$, so the LP relaxation is solved by column generation: the pricing problem $\max\{\sum_i \pi_i a_i : \sum_i w_i a_i \le L,\ a \in \mathbb{Z}_{\ge 0}^m\}$ is a bounded integer knapsack over the dual prices $\pi_i$ of the demand rows. A pattern prices out (improves the master) iff its reduced cost $1 - \sum_i \pi_i a_i < 0$.

**Compact (Kantorovich, 1939) model.** Index potential stock pieces $k = 1,\dots,K$ ($K$ from any heuristic upper bound). Binary $y_k = 1$ if piece $k$ is used; integer $z_{ik}$ = copies of item $i$ cut from piece $k$:

$$\min \sum_k y_k \quad \text{s.t.} \quad \sum_k z_{ik} \ge d_i \ \forall i, \qquad \sum_i w_i z_{ik} \le L\, y_k \ \forall k, \qquad y_k \in \{0,1\},\ z_{ik} \in \mathbb{Z}_{\ge 0}.$$

### Bound quality — why the pattern model wins

- The Kantorovich LP relaxation equals the **material bound** $\sum_i w_i d_i / L$: set every $y_k$ fractional and spread items freely. It is weak, and the model has full symmetry over the $K$ piece indices, so branch-and-bound stalls.
- The Gilmore-Gomory LP relaxation $z_{LP}$ equals the Lagrangian/Dantzig-Wolfe bound of the Kantorovich model and is empirically extremely tight. The **MIRUP conjecture** (Scheithauer & Terno, 1995, "The modified integer round-up property") states $z_{IP} \le \lceil z_{LP} \rceil + 1$; no counterexample is known, and most instances satisfy $z_{IP} = \lceil z_{LP} \rceil$ (the integer round-up property). Practical consequence: once column generation gives $z_{LP}$, any feasible solution with $\lceil z_{LP} \rceil$ rolls is provably optimal.
- The 1D-CSP is NP-hard: with all $d_i = 1$ it is exactly bin packing. See the **bin-packing** skill for the unit-demand view, FFD worst-case ratios, and the L1/L2 lower bounds, which all transfer.

### Objective variants: rolls vs trim loss

Let $P = \sum_j (\text{used pattern width})\, x_j$ be the total cut width. Trim loss is $L \sum_j x_j - P$ (waste inside used rolls); overproduction is $\sum_i w_i (\text{produced}_i - d_i)$. With identical rolls and `≥` demands, minimizing roll count minimizes trim loss + overproduction width together — they only diverge when overproduced pieces count as usable stock or when rolls have different costs. State which convention applies before reporting "waste."

### Variant map and model choice

| Situation | Recommended model |
|---|---|
| `m ≤ ~15`, small `L`, maximal patterns enumerable (≤ ~10^5) | Enumerate patterns, solve pattern IP directly |
| General single stock length, near-optimality acceptable | Column generation + IP over generated columns + rounding |
| Proven optimum required | Branch-and-price, or arc-flow MIP (pseudo-polynomial size) |
| Multiple stock lengths/costs | CG with one knapsack pricing per stock type, cost coefficients in master |
| Distinct-pattern (setup) costs or pattern-count limit | Pattern minimization extensions (Vanderbeck, 2000) |
| Exact demand, no overproduction | `=` master rows, pricing bounds $a_i \le d_i$, handle negative duals |
| Tiny time budget, feasibility only | FFD construction; metaheuristic if FFD gap is unacceptable |

Complexity notes: pricing by dynamic programming is $O(L \sum_i u_i)$ for copy bounds $u_i$ (binary splitting of copies reduces this to $O(L \sum_i \log u_i)$); the number of CG iterations is typically a small multiple of $m$; full pattern enumeration grows like the number of integer points in the knapsack polytope — check its size before committing.

## Exact Models in Gurobi

Two exact entry points: the compact Kantorovich MIP (small instances only, but the formulation everyone writes first) and direct pattern enumeration + pattern IP (the right exact tool when `m` and `L` are small). General gurobipy modeling conventions — constraint-builder functions, status handling, parameter hygiene — follow the **milp-modeling-gurobi** skill.

### Compact Kantorovich MIP with constraint builders

```python
import gurobipy as gp
from gurobipy import GRB


def first_fit_decreasing(widths: list[int], demands: list[int],
                         capacity: int) -> list[list[int]]:
    """FFD on the expanded item list. Returns rolls as lists of item-type indices."""
    items = [i for i, d in enumerate(demands) for _ in range(d)]
    items.sort(key=lambda i: -widths[i])
    rolls: list[list[int]] = []
    space: list[int] = []
    for i in items:
        for r in range(len(rolls)):
            if widths[i] <= space[r]:
                rolls[r].append(i)
                space[r] -= widths[i]
                break
        else:
            rolls.append([i])
            space.append(capacity - widths[i])
    return rolls


def add_demand_constraints(model: gp.Model, z: gp.tupledict, data: dict) -> None:
    """Each item type i is cut at least d_i times across all rolls."""
    for i in range(len(data["widths"])):
        model.addConstr(
            gp.quicksum(z[i, k] for k in range(data["K"])) >= data["demands"][i],
            name=f"demand[{i}]",
        )


def add_capacity_constraints(model: gp.Model, y: gp.tupledict, z: gp.tupledict,
                             data: dict) -> None:
    """Width cut from roll k fits in the stock length; links z to the roll-open var y."""
    m = len(data["widths"])
    for k in range(data["K"]):
        model.addConstr(
            gp.quicksum(data["widths"][i] * z[i, k] for i in range(m))
            <= data["capacity"] * y[k],
            name=f"capacity[{k}]",
        )


def add_symmetry_breaking_constraints(model: gp.Model, y: gp.tupledict,
                                      data: dict) -> None:
    """Order the rolls: roll k+1 may be used only if roll k is used."""
    for k in range(data["K"] - 1):
        model.addConstr(y[k] >= y[k + 1], name=f"sym[{k}]")


def solve_kantorovich(widths: list[int], demands: list[int], capacity: int,
                      time_limit: float = 60.0) -> tuple[int, list[list[int]]]:
    """Compact MIP for 1D cutting stock. Returns (rolls_used, per-roll patterns)."""
    K = len(first_fit_decreasing(widths, demands, capacity))  # valid upper bound
    data = {"widths": widths, "demands": demands, "capacity": capacity, "K": K}
    m = len(widths)
    model = gp.Model("csp_kantorovich")
    model.Params.OutputFlag = 0
    model.Params.TimeLimit = time_limit
    y = model.addVars(K, vtype=GRB.BINARY, name="y")
    z = model.addVars(m, K, vtype=GRB.INTEGER, lb=0, name="z")
    add_demand_constraints(model, z, data)
    add_capacity_constraints(model, y, z, data)
    add_symmetry_breaking_constraints(model, y, data)
    model.setObjective(y.sum(), GRB.MINIMIZE)
    model.optimize()
    if model.Status not in (GRB.OPTIMAL, GRB.TIME_LIMIT) or model.SolCount == 0:
        raise RuntimeError(f"no solution, status {model.Status}")
    used = [k for k in range(K) if y[k].X > 0.5]
    patterns = [[round(z[i, k].X) for i in range(m)] for k in used]
    return len(used), patterns


widths, demands, capacity = [6, 5, 4, 3], [2, 2, 3, 4], 10
rolls, patterns = solve_kantorovich(widths, demands, capacity)
print(rolls, patterns)
# Expected: rolls = 5. Material bound ceil(46/10) = 5, so 5 is provably optimal.
```

Even with the `y[k] >= y[k+1]` ordering, the compact model degrades quickly: identical rolls remain interchangeable in the `z` block, and the LP bound is the material bound. Treat it as a correctness reference for `m ≲ 10` and total demand ≲ 50, not as a production model.

### Pattern enumeration + pattern IP (small instances)

A pattern is **maximal** if no further item fits into its residual width. Restricting to maximal patterns never hurts the roll-count objective with `≥` demand rows.

```python
import gurobipy as gp
from gurobipy import GRB


def enumerate_maximal_patterns(widths: list[int], capacity: int) -> list[list[int]]:
    """DFS over all maximal cutting patterns (no item fits in the residual width)."""
    m = len(widths)
    patterns: list[list[int]] = []

    def extend(i: int, residual: int, current: list[int]) -> None:
        if i == m:
            if all(residual < w for w in widths):
                patterns.append(current.copy())
            return
        for k in range(residual // widths[i], -1, -1):
            current.append(k)
            extend(i + 1, residual - k * widths[i], current)
            current.pop()

    extend(0, capacity, [])
    return patterns


def solve_pattern_ip(patterns: list[list[int]], demands: list[int],
                     time_limit: float = 60.0) -> tuple[int, dict[int, int]]:
    """Set-covering style pattern IP over an explicit pattern list."""
    model = gp.Model("csp_pattern_ip")
    model.Params.OutputFlag = 0
    model.Params.TimeLimit = time_limit
    x = model.addVars(len(patterns), vtype=GRB.INTEGER, lb=0, name="x")
    for i in range(len(demands)):
        model.addConstr(
            gp.quicksum(patterns[j][i] * x[j] for j in range(len(patterns)))
            >= demands[i],
            name=f"cover[{i}]",
        )
    model.setObjective(x.sum(), GRB.MINIMIZE)
    model.optimize()
    if model.Status not in (GRB.OPTIMAL, GRB.TIME_LIMIT) or model.SolCount == 0:
        raise RuntimeError(f"no solution, status {model.Status}")
    use = {j: round(x[j].X) for j in range(len(patterns)) if x[j].X > 0.5}
    return round(model.ObjVal), use


widths, demands, capacity = [6, 5, 4, 3], [2, 2, 3, 4], 10
pats = enumerate_maximal_patterns(widths, capacity)
obj, use = solve_pattern_ip(pats, demands)
print(len(pats), obj, {tuple(pats[j]): c for j, c in use.items()})
# Expected: 8 maximal patterns; optimum 5 rolls,
# e.g. (1,0,1,0) x2, (0,2,0,0) x1, (0,0,1,2) x2.
```

When enumeration is feasible this is the simplest provably exact method: the IP sees every column, so there is no integrality question beyond the IP solve itself.

## Gilmore-Gomory Column Generation

The workhorse. The restricted master LP holds a subset of patterns; bounded-knapsack pricing over the duals generates improving patterns until none has negative reduced cost. The loop below adds columns incrementally with `gp.Column` instead of rebuilding the master. For stabilization, convergence theory, and branch-and-price mechanics see the **column-generation** skill; for the pricing DP family (bounded/unbounded knapsack, branch-and-bound alternatives) see the **knapsack-problems** skill.

```python
import numpy as np
import gurobipy as gp
from gurobipy import GRB


def solve_pricing(widths: np.ndarray, duals: np.ndarray, capacity: int,
                  max_copies: np.ndarray) -> tuple[np.ndarray, float]:
    """Bounded integer knapsack by DP: max duals @ a, s.t. widths @ a <= capacity,
    0 <= a_i <= max_copies_i. Returns (pattern, optimal value)."""
    m = len(widths)
    dp = np.zeros(capacity + 1)
    take = np.zeros((m, capacity + 1), dtype=np.int64)
    for i in range(m):
        new = dp.copy()
        for c in range(int(widths[i]), capacity + 1):
            kmax = min(int(max_copies[i]), c // int(widths[i]))
            for k in range(1, kmax + 1):
                v = dp[c - k * int(widths[i])] + k * duals[i]
                if v > new[c] + 1e-12:
                    new[c] = v
                    take[i, c] = k
        dp = new
    pattern = np.zeros(m, dtype=np.int64)
    c = capacity
    for i in range(m - 1, -1, -1):
        pattern[i] = take[i, c]
        c -= int(take[i, c] * widths[i])
    return pattern, float(dp[capacity])


def column_generation(widths: list[int], demands: list[int], capacity: int,
                      tol: float = 1e-9, max_iter: int = 1000
                      ) -> tuple[list[list[int]], float, int]:
    """Gilmore-Gomory CG for the master LP. Returns (patterns, z_LP, iterations)."""
    m = len(widths)
    patterns = []
    for i in range(m):                       # homogeneous starting columns
        col = [0] * m
        col[i] = capacity // widths[i]
        patterns.append(col)
    model = gp.Model("csp_master_lp")
    model.Params.OutputFlag = 0
    cover = [model.addConstr(gp.LinExpr() >= demands[i], name=f"cover[{i}]")
             for i in range(m)]
    for j, col in enumerate(patterns):
        nz = [i for i in range(m) if col[i]]
        model.addVar(obj=1.0, lb=0.0, name=f"x[{j}]",
                     column=gp.Column([float(col[i]) for i in nz],
                                      [cover[i] for i in nz]))
    model.ModelSense = GRB.MINIMIZE
    w = np.asarray(widths, dtype=np.int64)
    d = np.asarray(demands, dtype=np.int64)
    for it in range(1, max_iter + 1):
        model.optimize()
        if model.Status != GRB.OPTIMAL:
            raise RuntimeError(f"master LP status {model.Status}")
        duals = np.array([c.Pi for c in cover])
        pattern, value = solve_pricing(w, duals, capacity, d)
        if value < 1.0 + tol:                # best reduced cost 1 - value >= -tol
            return patterns, model.ObjVal, it
        patterns.append(pattern.tolist())
        nz = [i for i in range(m) if pattern[i]]
        model.addVar(obj=1.0, lb=0.0, name=f"x[{len(patterns) - 1}]",
                     column=gp.Column([float(pattern[i]) for i in nz],
                                      [cover[i] for i in nz]))
    raise RuntimeError("column generation hit max_iter without converging")


def solve_ip_over_columns(patterns: list[list[int]], demands: list[int],
                          time_limit: float = 30.0) -> tuple[int, list[int]]:
    """Restricted-master IP: integer solve over the generated columns only."""
    model = gp.Model("csp_master_ip")
    model.Params.OutputFlag = 0
    model.Params.TimeLimit = time_limit
    x = model.addVars(len(patterns), vtype=GRB.INTEGER, lb=0, name="x")
    for i in range(len(demands)):
        model.addConstr(
            gp.quicksum(patterns[j][i] * x[j] for j in range(len(patterns)))
            >= demands[i],
            name=f"cover[{i}]",
        )
    model.setObjective(x.sum(), GRB.MINIMIZE)
    model.optimize()
    if model.Status not in (GRB.OPTIMAL, GRB.TIME_LIMIT) or model.SolCount == 0:
        raise RuntimeError(f"no solution, status {model.Status}")
    return round(model.ObjVal), [round(x[j].X) for j in range(len(patterns))]


widths, demands, capacity = [6, 5, 4, 3], [2, 2, 3, 4], 10
patterns, z_lp, iters = column_generation(widths, demands, capacity)
z_ip, counts = solve_ip_over_columns(patterns, demands)
print(f"z_LP={z_lp:.4f} ceil={int(np.ceil(z_lp - 1e-9))} z_IP={z_ip} iters={iters}")
# Expected: z_LP about 4.67, ceil(z_LP) = 5, z_IP = 5 -> proven optimal
# (material bound is 4.6; the LP bound dominates it).
```

Three facts to internalize:

1. **The stopping test is on the pricing optimum, not on master progress.** The master objective can stall for many iterations (degeneracy) while the duals still move; stop only when $\max_a \sum_i \pi_i a_i < 1 + \varepsilon$.
2. **`z_LP` is a valid lower bound only at convergence.** Mid-run, the restricted master objective is an upper bound on $z_{LP}$, not a lower bound on $z_{IP}$. If you must stop early, compute the Lagrangian bound $z_{RM} - (\text{pricing value} - 1)\sum_i d_i$-style safe bound from the **column-generation** skill instead of trusting the master value.
3. **The bounded copies `a_i ≤ d_i` are not just cosmetic.** They keep patterns sensible under `≥` rows and are required under `=` rows; they also shrink the DP.

### From LP to integers: rounding with residual repair

`solve_ip_over_columns` alone is a heuristic — the optimal integer solution may need a pattern that never priced out for the LP duals. The standard complement is round-down + residual repair: fix the integer parts of the LP solution, then cover the small residual demand by FFD (or by a recursive CG on the residual). On most instances one of the two routes reaches $\lceil z_{LP} \rceil$, which certifies optimality.

```python
import numpy as np


def round_down_and_repair(patterns: list[list[int]], x_lp: list[float],
                          demands: list[int], widths: list[int], capacity: int
                          ) -> tuple[list[list[int]], list[int]]:
    """Round the LP master solution down; cover residual demand by FFD.
    Returns (all_patterns, counts) including the repair patterns."""
    a = np.asarray(patterns, dtype=np.int64)
    x_dn = np.floor(np.asarray(x_lp) + 1e-9).astype(np.int64)
    residual = np.maximum(np.asarray(demands) - a.T @ x_dn, 0)
    items = np.repeat(np.arange(len(widths)), residual)   # expand residual items
    order = sorted(range(len(items)), key=lambda r: -widths[items[r]])
    rolls: list[list[int]] = []
    loads: list[int] = []
    for r in order:
        t = int(items[r])
        for k in range(len(rolls)):
            if loads[k] + widths[t] <= capacity:
                rolls[k][t] += 1
                loads[k] += widths[t]
                break
        else:
            fresh = [0] * len(widths)
            fresh[t] = 1
            rolls.append(fresh)
            loads.append(widths[t])
    all_patterns = [list(p) for p in patterns] + rolls
    counts = x_dn.tolist() + [1] * len(rolls)
    return all_patterns, counts


# Patterns over widths [6, 5, 4, 3], L = 10; LP solution with value 4.6667:
pats = [[1, 0, 1, 0], [0, 2, 0, 0], [0, 0, 1, 2], [0, 0, 0, 3]]
x_lp = [2.0, 1.0, 1.0, 2.0 / 3.0]
all_pats, counts = round_down_and_repair(pats, x_lp, [2, 2, 3, 4], [6, 5, 4, 3], 10)
print(sum(counts), [p for p, c in zip(all_pats, counts) if c])
# Expected: 5 rolls total -- round-down gives 4 rolls, residual (two items of
# width 3) packs into one repair roll; 5 = ceil(4.667) -> optimal.
```

Report whichever of {IP over columns, round-down + repair} is better, together with $\lceil z_{LP} \rceil$; if they meet the bound, say "optimal", otherwise report the absolute gap in rolls (it is almost always 0 or 1 — see MIRUP above).

## Metaheuristic Baseline: Random-Key GA

A metaheuristic is the right tool when side constraints break the knapsack pricing structure (knife limits, sequencing, pattern-dependent costs) or when no LP solver is available. For plain 1D-CSP it is a baseline, not a competitor to CG. A biased random-key GA with a first-fit decoder fits well: the decoder maps any key vector to a feasible solution, so no constraint handling is needed. Framework details, elite/mutant proportions, and decoder design guidance are in the **biased-random-key-genetic-algorithm** skill; the grouping-fitness idea is from Falkenauer (1996), "A hybrid grouping genetic algorithm for bin packing".

```python
import numpy as np
from collections import Counter


def decode_first_fit(keys: np.ndarray, item_types: np.ndarray, widths: list[int],
                     capacity: int) -> tuple[list[list[int]], list[int]]:
    """Sort items by key, first-fit into rolls. Returns (rolls as type lists, loads)."""
    rolls: list[list[int]] = []
    loads: list[int] = []
    for idx in np.argsort(keys):
        t = int(item_types[idx])
        for r in range(len(rolls)):
            if loads[r] + widths[t] <= capacity:
                rolls[r].append(t)
                loads[r] += widths[t]
                break
        else:
            rolls.append([t])
            loads.append(widths[t])
    return rolls, loads


def grouping_fitness(loads: list[int], capacity: int) -> float:
    """Falkenauer-style: roll count minus mean squared fill (prefer full rolls)."""
    fills = np.asarray(loads, dtype=float) / capacity
    return len(loads) - float(np.mean(fills**2))


def brkga_cutting_stock(widths: list[int], demands: list[int], capacity: int,
                        pop_size: int = 60, n_gen: int = 200, elite: float = 0.2,
                        mutant: float = 0.15, rho: float = 0.7, seed: int = 0
                        ) -> tuple[int, Counter]:
    """BRKGA over item-permutation random keys with a first-fit decoder."""
    rng = np.random.default_rng(seed)
    item_types = np.repeat(np.arange(len(widths)), demands)
    n = len(item_types)
    n_e = max(1, int(elite * pop_size))
    n_m = max(1, int(mutant * pop_size))
    n_o = pop_size - n_e - n_m
    pop = rng.random((pop_size, n))
    best_rolls: list[list[int]] = []
    best_fit = np.inf
    for _ in range(n_gen):
        fits = np.empty(pop_size)
        decoded = []
        for p in range(pop_size):
            rolls, loads = decode_first_fit(pop[p], item_types, widths, capacity)
            decoded.append(rolls)
            fits[p] = grouping_fitness(loads, capacity)
        order = np.argsort(fits)
        if fits[order[0]] < best_fit:
            best_fit, best_rolls = float(fits[order[0]]), decoded[order[0]]
        elites = pop[order[:n_e]]                       # vectorized BRKGA step
        e_par = elites[rng.integers(0, n_e, n_o)]
        o_par = pop[order[rng.integers(n_e, pop_size, n_o)]]
        mask = rng.random((n_o, n)) < rho
        pop = np.vstack([elites, np.where(mask, e_par, o_par),
                         rng.random((n_m, n))])
    counts = Counter(tuple(sorted(r, reverse=True)) for r in best_rolls)
    return len(best_rolls), counts


rolls, pattern_counts = brkga_cutting_stock([6, 5, 4, 3], [2, 2, 3, 4], 10, seed=1)
print(rolls, dict(pattern_counts))
# Expected: 5 rolls (optimal for this instance); recurring full patterns such
# as (6,4), (5,5), (3,3,4) appear among the decoded rolls.
```

Scaling warning: the random-key vector has one gene per demanded item, so total demand $\sum_i d_i$ in the tens of thousands makes decoding the bottleneck. At that size either work on the residual problem after an LP round-down, or switch representation to pattern sequences. Population-level operations above stay vectorized; only the decoder is inherently sequential.

## Instance Generation and Validation

### Seeded instance generator

Hardness in 1D-CSP is driven by the width distribution relative to `L`. Items near `L/4 … L/2` (2-4 items per roll, no easy fillers) are the hard region; many small items make FFD nearly optimal. The classification and generator conventions follow Wäscher & Gau (1996), "Heuristics for the integer one-dimensional cutting stock problem".

```python
import numpy as np

PRESETS: dict[str, dict] = {
    "easy_small_items": {"width_frac": (0.05, 0.20)},
    "hard_mid_items": {"width_frac": (0.25, 0.50)},
    "wascher_gau_like": {"width_frac": (0.15, 0.80), "demand_range": (1, 10)},
}


def generate_instance(m: int, capacity: int = 1000,
                      width_frac: tuple[float, float] = (0.1, 0.8),
                      demand_range: tuple[int, int] = (1, 100),
                      seed: int = 0) -> dict:
    """Random 1D-CSP instance with m distinct integer widths. Reproducible by seed."""
    rng = np.random.default_rng(seed)
    lo, hi = int(width_frac[0] * capacity), int(width_frac[1] * capacity)
    widths = rng.choice(np.arange(lo, hi + 1), size=m, replace=False)
    widths = np.sort(widths)[::-1]
    demands = rng.integers(demand_range[0], demand_range[1] + 1, size=m)
    return {
        "capacity": capacity,
        "widths": widths.tolist(),
        "demands": demands.tolist(),
        "material_bound": int(np.ceil(widths @ demands / capacity)),
    }


inst = generate_instance(m=8, capacity=100, **PRESETS["hard_mid_items"], seed=42)
print(inst)
# Expected: 8 distinct widths in [25, 50], demands in [1, 100], and the
# material bound; identical output on every run with seed=42.
```

For published comparisons use the BPPLIB collection (Delorme, Iori & Martello, 2018) and the classic Schwerin/Wäscher-Gau sets rather than only self-generated instances, and always report generator parameters and seeds.

### Independent feasibility and objective validator

Never reuse model code to check solutions — the validator must be a second, dumb implementation of the definition. It accepts the pattern-based form `(patterns, counts)` that every method above can produce.

```python
import numpy as np


def validate_solution(patterns: list[list[int]], counts: list[int],
                      widths: list[int], demands: list[int],
                      capacity: int) -> dict:
    """Independent check: pattern feasibility, demand coverage, recomputed objective."""
    a = np.asarray(patterns, dtype=np.int64)
    x = np.asarray(counts, dtype=np.int64)
    w = np.asarray(widths, dtype=np.int64)
    d = np.asarray(demands, dtype=np.int64)
    violations: list[str] = []
    if (x < 0).any():
        violations.append("negative pattern count")
    if (a < 0).any():
        violations.append("negative item count inside a pattern")
    pattern_width = a @ w
    for j in np.flatnonzero(pattern_width > capacity):
        violations.append(
            f"pattern {j} exceeds capacity: {int(pattern_width[j])} > {capacity}")
    produced = a.T @ x
    for i in np.flatnonzero(produced < d):
        violations.append(
            f"item {i} short: produced {int(produced[i])} < demand {int(d[i])}")
    return {
        "feasible": not violations,
        "rolls": int(x.sum()),
        "trim_loss": int(x @ (capacity - pattern_width)),
        "overproduction": (produced - d).tolist(),
        "violations": violations,
    }


pats = [[1, 0, 1, 0], [0, 2, 0, 0], [2, 0, 0, 0]]
report = validate_solution(pats, [2, 1, 1], [6, 5, 4, 3], [2, 2, 3, 4], 10)
print(report["feasible"], report["violations"])
# Expected: feasible = False with three violations -- pattern (2,0,0,0) has
# width 12 > 10, width-4 items are short (2 produced, 3 demanded), and
# width-3 items are short (0 produced, 4 demanded).
```

Run the validator on every reported solution, in tests and at the end of every experiment script. It also recomputes trim loss independently, which catches objective-definition mismatches early.

## Advanced Techniques

### Dual stabilization for degenerate masters

Cutting stock masters are heavily degenerate: many basic solutions share the LP value, the duals oscillate, and pricing chases noise — the classic tailing-off effect. Remedies, in increasing implementation effort: (i) interior-point master solves (`Model.Params.Method = 2`, `Crossover = 0`) give central duals; (ii) dual smoothing $\tilde\pi = \alpha \pi_{best} + (1-\alpha)\pi$ with $\alpha \approx 0.8$ (Wentges, 1997; Pessoa et al., 2018, automatic smoothing); (iii) boxstep/penalty stabilization around dual stability centers (du Merle et al., 1999). On hard CSP instances, smoothing alone often cuts iteration counts by a factor of 2-5. Implementation patterns are in the **column-generation** skill — they apply unchanged here because the pricing oracle stays a knapsack.

### Sequential value correction and residual recursion

Round-down + FFD repair is the basic integerization. Two stronger variants: (1) **residual CG recursion** — after round-down, run column generation again on the residual demand (it is a small CSP) and recurse; (2) **sequential value correction (SVC)** — build integer solutions pattern by pattern, maintaining pseudo-prices per item that are increased for items that keep appearing in wasteful patterns (Belov & Scheithauer, 2002, also covering branch-cut-price for 1D-CSP). SVC is the strongest simple heuristic known for 1D-CSP and frequently hits $\lceil z_{LP} \rceil$ where plain rounding misses it by one roll.

### Arc-flow and one-cut reformulations

The arc-flow model (Valério de Carvalho, 1999) encodes patterns as paths in a DAG with nodes $0,\dots,L$ and arcs $(c, c + w_i)$; a flow of $z$ units from 0 to $L$ decomposes into $z$ patterns. The model is pseudo-polynomial ($O(mL)$ arcs before reduction) and its LP bound equals the Gilmore-Gomory bound, so a plain MIP solver can prove optimality without any CG loop. Graph compression (Brandão & Pedroso, 2016, "Bin packing and related problems: general arc-flow formulation with graph compression") makes this practical for surprisingly large `L`. Reach for arc-flow when you need a proven optimum, integer widths, and want to avoid implementing branch-and-price; the survey by Delorme, Iori & Martello (2016), "Bin packing and cutting stock problems: mathematical models and exact algorithms", maps the whole landscape.

### Branch-and-price, briefly

If $\lceil z_{LP} \rceil$ is not attained by heuristics, optimality needs branching that keeps the pricing problem a knapsack. Branching on a single pattern variable $x_j$ is wrong: forbidding a pattern turns pricing into a "knapsack avoiding one solution" problem. Sound schemes branch on aggregate quantities — e.g., on arc-flow variables, or on $\sum_{j \in J(i,i')} x_j$ for item pairs appearing together (Ryan-Foster applied to the unit-demand expansion; Vance, 1998). Each branch adds a bound or a forbidden pair that the DP pricing absorbs as an extra state or arc removal. Full machinery in the **column-generation** skill.

### Pattern minimization and setup costs

Industrial cutters pay per knife reconfiguration, so the secondary objective "few distinct patterns" matters. The pattern-minimization problem (fix roll count, minimize distinct patterns) is strongly NP-hard even when the roll count is the minimum (Vanderbeck, 2000). Practical approaches: (i) bicriteria weighting in the master objective ($x_j$ cost 1, pattern-activation binary cost $\sigma$, linked by $x_j \le M u_j$ — choose $M = \max_i d_i$, see the **milp-modeling-gurobi** skill for linking-constraint hygiene); (ii) post-processing pattern-combination heuristics, e.g. KOMBI (Foerster & Wäscher, 2000), which merge pattern pairs without increasing roll usage.

## Practical Challenges

**The master LP value stalls for dozens of iterations and the run looks stuck.** That is degeneracy-driven tailing-off, not a bug. Verify the pricing value is still above $1+\varepsilon$, switch the master to barrier without crossover for central duals, and add dual smoothing. Also check you are not re-generating an existing column — if pricing returns a duplicate pattern, the duals are cycling and stabilization is mandatory.

**Fractional widths make the DP pricing impossible.** Scale: multiply all widths and `L` by $10^p$ for the measurement precision $p$ and round. Confirm with the data owner that rounding direction is safe (round widths up, `L` down, to stay conservative). If the scaled `L` explodes (e.g., $10^7$), replace the DP with a branch-and-bound knapsack or a small MIP for pricing — correctness is unchanged, only pricing speed.

**Demands in the hundreds of thousands blow up item-expanded code.** Keep everything in type-count space: the master, pricing, validator, and rounding all work on `(pattern, count)` pairs and never expand items. Only FFD repair and the metaheuristic decoder expand items — apply them to residual demands (small after round-down), never to the raw instance.

**IP over generated columns returns $\lceil z_{LP} \rceil + 1$ and you report it as near-optimal when it is optimal-unproven.** The gap statement must compare against $\lceil z_{LP} \rceil$, not $z_{LP}$, and only after CG converged. If the IP misses the bound by one, run round-down + residual CG and SVC before concluding the instance needs branch-and-price; in practice fewer than 1% of instances resist all three.

**Equality demand rows make the master infeasible or produce negative duals.** With `= d_i` rows, homogeneous starting columns may not combine to an exact cover — add slack/surplus columns with big-M cost for phase-1 feasibility, cap pricing copies at $a_i \le d_i$, and keep negative duals in the DP (the bounded DP above handles them: it simply takes zero copies). Decide first whether the business problem truly forbids overproduction; most cutting operations do not.

**The compact model "works on the test case" then fails at `m = 20`.** Expected: symmetry plus the material-bound LP relaxation means the node count explodes. Do not tune it — switch to pattern-based CG or arc-flow. Keep the compact model only as a cross-check oracle on tiny instances inside tests.

**Trim-loss numbers disagree between your report and the customer's.** Almost always an overproduction-accounting mismatch: waste-inside-rolls vs waste-plus-overproduced-width vs leftover-roll-tail conventions (a final partial roll may return to stock as usable). Fix the definition in writing, encode it in the validator, and report all three numbers in the solution summary.

## Tools & Libraries

| Library | When to use | Note |
|---|---|---|
| gurobipy | Master LP/IP, compact models, branch-and-price | Fastest LP reoptimization; `gp.Column` for incremental column addition |
| HiGHS (`highspy`) | License-free master LP/IP | Near-Gurobi LP speed; pair with a hand-written DP pricer |
| python-mip (CBC) | Teaching-scale CG, quick prototypes | Convenient `add_column`-style API; slower master solves |
| OR-Tools CP-SAT | Pattern problems with awkward side constraints (knife limits, sequencing) | Not for the LP master; good pricing fallback when DP structure breaks |
| numpy | Pricing DP, validators, instance generation, metaheuristics | Keep all data in type-count arrays |
| pandas | Experiment tables (instance, seed, bound, rolls, gap, time) | One row per run; aggregate over seeds for reports |
| VRPSolver / SCIP-GCG | Research-grade generic branch-and-price | When proving optimality at scale matters more than implementation time |

## Output Format

A complete cutting-stock deliverable contains:

1. **Instance summary.** `m`, `L`, total demand, material bound $\lceil \sum_i w_i d_i / L \rceil$, width distribution range, demand semantics (`≥` or `=`), overproduction policy.
2. **Bound and solution table.**

   | Quantity | Value |
   |---|---|
   | Material bound | 4.6 → 5 |
   | CG LP bound $z_{LP}$ (iterations, time) | 4.667 (12 it, 0.1 s) |
   | $\lceil z_{LP} \rceil$ | 5 |
   | Best integer solution (method) | 5 (IP over columns) |
   | Gap | 0 — proven optimal |

3. **Pattern table.** One row per used pattern: pattern composition (e.g., `2x36 + 1x14`), count, used width, trim per roll. Sorted by count descending. This is the artifact the cutting floor consumes — export as CSV.
4. **Waste accounting.** Total trim loss, total overproduction per item, leftover-tail convention used.
5. **Convergence note.** CG iterations, pricing time share, whether stabilization was active, tailing-off observed or not.
6. **Validator confirmation.** Output of the independent `validate_solution` call on the final `(patterns, counts)` — feasibility flag and recomputed objective must match the reported numbers.
7. **Reproducibility block.** Solver versions, parameter settings (`Method`, tolerances, time limits), instance source or generator seed.

If results feed a paper or thesis, add per-instance rows (instance, seed, $z_{LP}$, $z_{IP}$, gap, time) in a tidy table, one row per run.

## Questions to Ask

- How many distinct widths, what stock length, and how large are the demands — and are widths integers or measured decimals?
- One stock length or an assortment with different costs?
- Must demand be met exactly, or is overproduction allowed (and is it waste or usable inventory)?
- What exactly counts as "waste" in your reporting — trim inside rolls, overproduction, leftover roll tails?
- Is a solution within one roll of the lower bound acceptable, or do you need a proven optimum?
- Are there pattern-level side constraints: maximum cuts per pattern (knives), minimum run length per pattern, limits on distinct patterns (setups)?
- Do you have a Gurobi license, or should the implementation target HiGHS/CBC?
- What instance sizes must this handle in production, and what is the time budget per instance?
- Do you have historical or benchmark instances to calibrate against, or should I generate seeded synthetic ones?

## Related Skills

- **column-generation** — when the question is about the restricted-master/pricing loop itself: convergence, stabilization, Lagrangian bounds from partial runs, or full branch-and-price.
- **bin-packing** — when all demands are 1 or the user thinks in items-and-bins; FFD/BFD ratios and L1/L2 lower bounds transfer directly to cutting stock.
- **knapsack-problems** — when the pricing subproblem needs attention: bounded/unbounded DP variants, branch-and-bound pricing, or handling pricing-side constraints.
- **milp-modeling-gurobi** — when building or debugging the gurobipy models: constraint-builder structure, status handling, parameters, and linking-constraint (big-M) hygiene.
