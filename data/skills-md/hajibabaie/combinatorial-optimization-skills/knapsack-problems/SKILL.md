---
name: knapsack-problems
description: When the user wants to formulate and solve knapsack problems — 0-1, bounded, multiple, multidimensional, or quadratic — using dynamic programming, branch-and-bound, MIP, greedy bounds, or metaheuristics. Also use when the user mentions "knapsack," "0-1 knapsack," "multidimensional knapsack," "subset selection," "capacity constraint," or when a knapsack appears as a pricing or separation subproblem inside a larger algorithm. For Bellman recursions and state design, see dynamic-programming; for pricing loops built on a knapsack solver, see column-generation.
---

# Knapsack Problems

You are an expert in knapsack problems, the core selection-under-capacity structure of combinatorial optimization. This skill covers the 0-1, bounded, multiple, multidimensional, and quadratic variants, with exact methods (dynamic programming, branch-and-bound, MIP), greedy bounds, and a repair-based metaheuristic for large instances. Use the framework below to identify the variant, pick the method that matches the data regime, and deliver a validated solution with a provable or estimated optimality gap. Knapsack structure also appears inside larger algorithms — as the pricing subproblem of column generation and as the separation problem for cover cuts — so the implementations here are written to be reusable as subroutines.

## Initial Assessment

Establish the following before formulating or coding anything:

- **Identify the variant.** One container or several? One resource constraint or many? Are items binary, bounded integer, or unbounded? Do item pairs interact in the objective (quadratic terms)? The variant determines the method; misidentifying it wastes the whole effort.
- **Check data types.** Integer weights and capacity enable pseudo-polynomial DP. Fractional weights force B&B/MIP or require scaling. Note the magnitude of the capacity: DP needs an array of size `c + 1` per state dimension.
- **Estimate size.** Record `n` (items), `m` (constraints or knapsacks), and `c` (capacity magnitude). `n * c <= 1e8` with integer data: DP is the simplest exact route. Larger `c`: B&B or MIP. Multidimensional with `n > 500`: plan for a heuristic with a bound.
- **Establish the role of the knapsack.** Standalone problem solved once, or a subroutine called thousands of times (pricing, separation, Lagrangian subproblem)? Subroutine use demands a fast specialized solver, not a general MIP model with per-call build overhead.
- **Clarify exact-vs-heuristic requirements.** Is a proven optimum required (e.g., inside an exact decomposition), or is a 1-2% gap acceptable? What is the wall-clock budget per solve?
- **Confirm solver availability.** Gurobi license present? If not, plan for OR-Tools, HiGHS, or the pure-numpy DP/B&B routes in this skill.
- **Check correlation structure.** Profit-weight correlation drives empirical hardness (Pisinger 2005, "Where are the hard knapsack problems?"). Strongly correlated and subset-sum-like instances are hard for ratio-based B&B; ask where the data comes from.
- **Audit constraint semantics.** Is the capacity hard or soft? Must every item be considered, or are some pre-fixed? Are there side constraints (conflicts, precedences) that silently turn the problem into something else (e.g., a knapsack with conflicts is graph-structured and much harder)?
- **Agree on deliverables.** Selected item set, objective value, bound and gap, solve time, and an independent feasibility check (see the validator below).

## Problem Variants and Formulations

Notation: `n` items indexed by `j`, profit `p_j >= 0`, weight `w_j > 0`, capacity `c`. All data integer unless stated otherwise.

### The 0-1 knapsack and its relatives

The 0-1 knapsack problem (KP):

$$
\max \sum_{j=1}^{n} p_j x_j \quad \text{s.t.} \quad \sum_{j=1}^{n} w_j x_j \le c, \qquad x_j \in \{0,1\}.
$$

- **Bounded knapsack (BKP):** `x_j ∈ {0, 1, ..., u_j}`. Reduce to 0-1 by binary splitting: item `j` becomes copies with multiplicities `1, 2, 4, ..., remainder`, only `O(log u_j)` copies each.
- **Unbounded knapsack (UKP):** `x_j ∈ Z_{>=0}`. Solved by a one-dimensional DP over capacities in `O(n c)`; this is the pricing workhorse for cutting stock.

KP is weakly NP-hard: DP solves it in pseudo-polynomial `O(n c)` time, and an FPTAS exists (Ibarra & Kim 1975). The canonical references are Martello & Toth (1990), *Knapsack Problems: Algorithms and Computer Implementations*, and Kellerer, Pferschy & Pisinger (2004), *Knapsack Problems*.

### Multiple, multidimensional, and quadratic variants

**Multiple knapsack (MKP-m):** `m` containers with capacities `c_i`; each item goes into at most one container.

$$
\max \sum_{i=1}^{m}\sum_{j=1}^{n} p_j x_{ij} \quad \text{s.t.} \quad \sum_{j} w_j x_{ij} \le c_i \;\; \forall i, \qquad \sum_{i} x_{ij} \le 1 \;\; \forall j, \qquad x_{ij} \in \{0,1\}.
$$

Strongly NP-hard (it contains 3-partition). No FPTAS even for `m = 2`, but a PTAS exists (Chekuri & Khanna 2005).

**Multidimensional knapsack (d-KP, often also abbreviated MKP — always disambiguate):** one selection vector, `m` resource rows.

$$
\max \; p^{\top} x \quad \text{s.t.} \quad W x \le b, \qquad x \in \{0,1\}^n, \quad W \in \mathbb{Z}_{\ge 0}^{m \times n}.
$$

No FPTAS for `m >= 2` unless P = NP; a PTAS exists for fixed `m` (Frieze & Clarke 1984). Exact MIP works to a few hundred items; beyond that, the Chu & Beasley (1998) repair GA remains the standard heuristic baseline. Survey: Fréville (2004).

**Quadratic knapsack (QKP):** pairwise profits `q_{ij} >= 0` earned when both items are selected.

$$
\max \sum_{j} p_j x_j + \sum_{i<j} q_{ij} x_i x_j \quad \text{s.t.} \quad \sum_{j} w_j x_j \le c, \qquad x \in \{0,1\}^n.
$$

Strongly NP-hard (contains max clique). Bounds and exact methods: Caprara, Pisinger & Toth (1999).

### Greedy bounds and the critical item

Sort items by non-increasing efficiency `p_j / w_j` (Dantzig 1957). The **critical item** `s` is the first item that no longer fits after greedily packing the prefix. The LP-relaxation optimum is then

$$
U_{\text{Dantzig}} = \sum_{j<s} p_j + \left\lfloor \bar{c} \, \frac{p_s}{w_s} \right\rfloor, \qquad \bar{c} = c - \sum_{j<s} w_j,
$$

i.e., the LP solution has at most one fractional variable, `x_s`. Martello & Toth's `U2` bound tightens this by considering both integer roundings of `x_s`. The greedy integer solution (prefix only) can be arbitrarily bad alone, but `max(greedy prefix, best single item)` is a 1/2-approximation. These bounds power the B&B implementation below and explain why strongly correlated instances (all efficiencies nearly equal) are hard: the bound is nearly flat across nodes.

### Method selection

| Variant | Data regime | Recommended method |
|---|---|---|
| 0-1 KP | integer data, `n * c <= ~1e8` | DP over capacities (exact, simple, fast) |
| 0-1 KP | large `c`, low correlation | B&B with Dantzig bound; or minknap/combo-class codes (Martello, Pisinger & Toth 1999) |
| 0-1 KP | strongly correlated, large `c` | MIP solver (cuts help where ratio bounds stall) |
| Bounded | moderate `u_j` | binary splitting + 0-1 DP |
| Multiple | `m` small, `n <= ~200` | MIP with symmetry breaking on identical containers |
| Multidimensional | `n <= ~250`, `m <= ~30` | MIP (often optimal within minutes) |
| Multidimensional | `n >= 500` | repair GA + LP or Lagrangian bound for the gap |
| Quadratic | `n <= ~150` | Gurobi binary MIQP, or Glover linearization |
| Quadratic | larger `n` | tabu/memetic heuristics + upper-bound from Caprara-Pisinger-Toth-style relaxation |
| Pricing subproblem | repeated solves, fractional profits | DP over the *weight* axis (profits are dual values, not integers) |

## Exact MIP Models in gurobipy

State the model, then build it with explicit constraint-builder functions so each constraint family is named, testable, and reusable. The first model covers 0-1, bounded, and multidimensional knapsacks in one function: weights enter as an `(m, n)` matrix (pass a 1-D array for the single-constraint case), and item bounds switch the variables from binary to general integer.

```python
import gurobipy as gp
import numpy as np
from gurobipy import GRB


def add_capacity_constraints(
    model: gp.Model, x: gp.tupledict, weights: np.ndarray, capacities: np.ndarray
) -> None:
    """Add one named capacity row per resource dimension: sum_j w[i,j] x_j <= b_i."""
    m, n = weights.shape
    for i in range(m):
        model.addConstr(
            gp.quicksum(int(weights[i, j]) * x[j] for j in range(n))
            <= int(capacities[i]),
            name=f"capacity[{i}]",
        )


def solve_knapsack_mip(
    profits: np.ndarray,
    weights: np.ndarray,
    capacities: np.ndarray | int,
    bounds: np.ndarray | None = None,
    time_limit: float = 60.0,
) -> tuple[int, np.ndarray]:
    """Solve 0-1, bounded, or multidimensional knapsack as a MIP.

    weights: (m, n) for m resource dimensions, or (n,) for a single one.
    bounds: per-item integer upper bounds; None means binary items.
    Returns (objective value, selection vector).
    """
    W = np.atleast_2d(np.asarray(weights))
    b = np.atleast_1d(np.asarray(capacities))
    n = W.shape[1]
    model = gp.Model("knapsack")
    model.Params.OutputFlag = 0
    model.Params.TimeLimit = time_limit
    if bounds is None:
        x = model.addVars(n, vtype=GRB.BINARY, name="x")
    else:
        x = model.addVars(
            n, vtype=GRB.INTEGER, lb=0, ub=[int(u) for u in bounds], name="x"
        )
    add_capacity_constraints(model, x, W, b)
    model.setObjective(
        gp.quicksum(int(profits[j]) * x[j] for j in range(n)), GRB.MAXIMIZE
    )
    model.optimize()
    if model.Status not in (GRB.OPTIMAL, GRB.TIME_LIMIT) or model.SolCount == 0:
        raise RuntimeError(f"no solution found (status {model.Status})")
    solution = np.array([round(x[j].X) for j in range(n)], dtype=np.int64)
    return int(round(model.ObjVal)), solution


p = np.array([60, 100, 120])
w = np.array([10, 20, 30])
value, x_sol = solve_knapsack_mip(p, w, 50)
print(value, x_sol)
# Expected: 220, x = [0, 1, 1]
```

For `n` up to a few hundred items this model is optimal in well under a second for any number of dimensions; the LP relaxation of a single-constraint knapsack is so tight (one fractional variable) that the solver mostly verifies the greedy structure.

### Multiple knapsack

The multiple knapsack needs two constraint families: each item placed at most once, and each container within its own capacity. Containers with identical capacities create symmetric solutions; break the symmetry by ordering container loads, otherwise B&B explores permutations of the same packing.

```python
import gurobipy as gp
import numpy as np
from gurobipy import GRB


def add_assignment_constraints(
    model: gp.Model, x: gp.tupledict, n_items: int, n_knapsacks: int
) -> None:
    """Each item goes into at most one knapsack: sum_i x[i,j] <= 1."""
    for j in range(n_items):
        model.addConstr(
            gp.quicksum(x[i, j] for i in range(n_knapsacks)) <= 1,
            name=f"assign[{j}]",
        )


def add_knapsack_capacity_constraints(
    model: gp.Model, x: gp.tupledict, weights: np.ndarray, capacities: np.ndarray
) -> None:
    """Each knapsack respects its own capacity: sum_j w_j x[i,j] <= c_i."""
    n = len(weights)
    for i in range(len(capacities)):
        model.addConstr(
            gp.quicksum(int(weights[j]) * x[i, j] for j in range(n))
            <= int(capacities[i]),
            name=f"capacity[{i}]",
        )


def add_load_ordering_constraints(
    model: gp.Model, x: gp.tupledict, weights: np.ndarray, capacities: np.ndarray
) -> None:
    """Symmetry breaking for identical capacities: non-increasing loads."""
    n, m = len(weights), len(capacities)
    for i in range(m - 1):
        if capacities[i] == capacities[i + 1]:
            model.addConstr(
                gp.quicksum(int(weights[j]) * x[i, j] for j in range(n))
                >= gp.quicksum(int(weights[j]) * x[i + 1, j] for j in range(n)),
                name=f"load_order[{i}]",
            )


def solve_multiple_knapsack(
    profits: np.ndarray,
    weights: np.ndarray,
    capacities: np.ndarray,
    time_limit: float = 60.0,
) -> tuple[int, np.ndarray]:
    """0-1 multiple knapsack: returns (objective, (m, n) assignment matrix)."""
    n, m = len(profits), len(capacities)
    model = gp.Model("multiple_knapsack")
    model.Params.OutputFlag = 0
    model.Params.TimeLimit = time_limit
    x = model.addVars(m, n, vtype=GRB.BINARY, name="x")
    add_assignment_constraints(model, x, n, m)
    add_knapsack_capacity_constraints(model, x, weights, capacities)
    add_load_ordering_constraints(model, x, weights, capacities)
    model.setObjective(
        gp.quicksum(int(profits[j]) * x[i, j] for i in range(m) for j in range(n)),
        GRB.MAXIMIZE,
    )
    model.optimize()
    if model.Status not in (GRB.OPTIMAL, GRB.TIME_LIMIT) or model.SolCount == 0:
        raise RuntimeError(f"no solution found (status {model.Status})")
    assign = np.array(
        [[round(x[i, j].X) for j in range(n)] for i in range(m)], dtype=np.int64
    )
    return int(round(model.ObjVal)), assign


p = np.array([6, 5, 5, 4])
w = np.array([6, 5, 5, 4])
caps = np.array([10, 10])
value, assign = solve_multiple_knapsack(p, w, caps)
print(value, assign.sum(axis=0))
# Expected: 20, every item packed (loads 10 and 10), e.g. {6,4} and {5,5}.
```

### Quadratic knapsack

Gurobi accepts binary quadratic objectives directly and convexifies or linearizes internally; for hand linearization (needed for solvers without MIQP support), Glover (1975) replaces `x_i * x_j` products with one continuous variable per item plus four bounding rows — far fewer variables than the naive `O(n^2)` product linearization.

```python
import gurobipy as gp
import numpy as np
from gurobipy import GRB


def solve_qkp(
    linear_profits: np.ndarray,
    quadratic_profits: np.ndarray,
    weights: np.ndarray,
    capacity: int,
    time_limit: float = 60.0,
) -> tuple[int, np.ndarray]:
    """Quadratic knapsack: max p'x + sum_{i<j} q_ij x_i x_j s.t. w'x <= c.

    quadratic_profits is used as an upper-triangular matrix.
    """
    n = len(linear_profits)
    model = gp.Model("qkp")
    model.Params.OutputFlag = 0
    model.Params.TimeLimit = time_limit
    x = model.addVars(n, vtype=GRB.BINARY, name="x")
    model.addConstr(
        gp.quicksum(int(weights[j]) * x[j] for j in range(n)) <= int(capacity),
        name="capacity",
    )
    objective = gp.quicksum(int(linear_profits[j]) * x[j] for j in range(n))
    objective += gp.quicksum(
        int(quadratic_profits[i, j]) * x[i] * x[j]
        for i in range(n)
        for j in range(i + 1, n)
        if quadratic_profits[i, j] != 0
    )
    model.setObjective(objective, GRB.MAXIMIZE)
    model.optimize()
    if model.Status not in (GRB.OPTIMAL, GRB.TIME_LIMIT) or model.SolCount == 0:
        raise RuntimeError(f"no solution found (status {model.Status})")
    solution = np.array([round(x[j].X) for j in range(n)], dtype=np.int64)
    return int(round(model.ObjVal)), solution


p = np.array([10, 5, 8, 3])
Q = np.zeros((4, 4), dtype=np.int64)
Q[0, 1], Q[2, 3] = 6, 4
w = np.array([4, 3, 5, 2])
value, x_sol = solve_qkp(p, Q, w, capacity=9)
print(value, x_sol)
# Expected: 24, x = [1, 1, 0, 1]  (10 + 5 + 3 linear + 6 pairwise)
```

## Dynamic Programming and Branch-and-Bound

For integer data with moderate capacity, the Bellman DP is exact, deterministic, and has no solver dependency. The recursion over capacities `0..c` is

$$
z_j(d) = \max\{\, z_{j-1}(d), \; z_{j-1}(d - w_j) + p_j \,\}, \qquad z_0(d) = 0,
$$

implemented below with the inner maximization vectorized over the whole capacity axis. The `keep` table costs `n * (c+1)` bits and gives exact solution recovery; drop it (rolling array) when only the value is needed. See **dynamic-programming** for state-design guidance and the divide-and-conquer recovery trick that avoids the table entirely.

```python
import numpy as np


def knapsack_dp(
    profits: np.ndarray, weights: np.ndarray, capacity: int
) -> tuple[int, np.ndarray]:
    """0-1 knapsack Bellman DP, O(n*c), vectorized over the capacity axis.

    Returns (optimal value, binary selection vector).
    """
    n = len(profits)
    value = np.zeros(capacity + 1, dtype=np.int64)
    keep = np.zeros((n, capacity + 1), dtype=bool)
    for j in range(n):
        wj, pj = int(weights[j]), int(profits[j])
        if wj > capacity:
            continue
        candidate = value.copy()
        candidate[wj:] = value[: capacity + 1 - wj] + pj
        keep[j] = candidate > value
        value = np.maximum(candidate, value)
    x = np.zeros(n, dtype=np.int64)
    d = capacity
    for j in range(n - 1, -1, -1):
        if keep[j, d]:
            x[j] = 1
            d -= int(weights[j])
    return int(value[capacity]), x


def split_bounded_items(
    profits: np.ndarray, weights: np.ndarray, bounds: np.ndarray
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Binary splitting for the bounded knapsack.

    An item with bound u becomes copies of multiplicity 1, 2, 4, ...,
    remainder, so any count 0..u is reachable with O(log u) 0-1 copies.
    Returns (profits, weights, owner index) of the equivalent 0-1 instance.
    """
    split_p, split_w, owner = [], [], []
    for j, (pj, wj, uj) in enumerate(zip(profits, weights, bounds)):
        remaining, mult = int(uj), 1
        while remaining > 0:
            take = min(mult, remaining)
            split_p.append(int(pj) * take)
            split_w.append(int(wj) * take)
            owner.append(j)
            remaining -= take
            mult *= 2
    return (
        np.array(split_p, dtype=np.int64),
        np.array(split_w, dtype=np.int64),
        np.array(owner, dtype=np.int64),
    )


p = np.array([60, 100, 120])
w = np.array([10, 20, 30])
value, x = knapsack_dp(p, w, 50)
print(value, x)
# Expected: 220, x = [0, 1, 1]
```

When the capacity is too large for DP, branch on items in efficiency order with the Dantzig bound pruning the tree. This is the textbook custom B&B (Horowitz & Sahni 1974 lineage); the best-first variant below can stop the moment the top-of-heap bound meets the incumbent. See **branch-and-bound** for node-selection trade-offs (DFS saves memory; best-first minimizes explored nodes).

```python
import heapq

import numpy as np


def dantzig_bound(
    p: np.ndarray, w: np.ndarray, c: int, j: int, value: int, load: int
) -> float:
    """Greedy fractional-fill upper bound using items j..n-1 (Dantzig 1957).

    Assumes items already sorted by non-increasing profit/weight ratio.
    """
    bound, room = float(value), c - load
    for k in range(j, len(p)):
        if w[k] <= room:
            room -= int(w[k])
            bound += int(p[k])
        else:
            bound += int(p[k]) * room / int(w[k])
            break
    return bound


def knapsack_branch_and_bound(
    profits: np.ndarray, weights: np.ndarray, capacity: int
) -> tuple[int, np.ndarray]:
    """Best-first 0-1 knapsack B&B with the Dantzig LP bound."""
    order = np.argsort(-(profits / weights))
    p = profits[order].astype(np.int64)
    w = weights[order].astype(np.int64)
    n = len(p)
    best_value, best_items = 0, []
    heap = [(-dantzig_bound(p, w, capacity, 0, 0, 0), 0, 0, 0, [])]
    while heap:
        neg_bound, j, value, load, chosen = heapq.heappop(heap)
        if -neg_bound <= best_value:
            break  # best-first: every remaining node is bounded by the incumbent
        if j == n:
            continue
        if load + w[j] <= capacity:  # branch: include item j
            v, d = value + int(p[j]), load + int(w[j])
            if v > best_value:
                best_value, best_items = v, chosen + [j]
            ub = dantzig_bound(p, w, capacity, j + 1, v, d)
            if ub > best_value:
                heapq.heappush(heap, (-ub, j + 1, v, d, chosen + [j]))
        ub = dantzig_bound(p, w, capacity, j + 1, value, load)  # exclude item j
        if ub > best_value:
            heapq.heappush(heap, (-ub, j + 1, value, load, chosen))
    x_sorted = np.zeros(n, dtype=np.int64)
    x_sorted[best_items] = 1
    x = np.zeros(n, dtype=np.int64)
    x[order] = x_sorted
    return best_value, x


p = np.array([60, 100, 120])
w = np.array([10, 20, 30])
value, x = knapsack_branch_and_bound(p, w, 50)
print(value, x)
# Expected: 220, x = [0, 1, 1]
```

For production-grade single-knapsack solving at scale, the expanding-core codes minknap (Pisinger 1997) and combo (Martello, Pisinger & Toth 1999) dominate both routines above; the algorithms here are for when you need full control or a teaching-grade reference.

## A Repair-Based Genetic Algorithm for the Multidimensional Knapsack

For multidimensional instances beyond exact reach (`n >= 500`, or tight time budgets), the standard baseline is the Chu & Beasley (1998) GA: binary encoding, uniform crossover, and a two-phase DROP/ADD repair driven by a pseudo-utility ordering, so the population stays feasible at all times. The repair loops over items (in utility order) but is vectorized across the whole population, which keeps it fast in numpy. See **genetic-algorithms** for the loop design (selection, crossover, elitism) and **constraint-handling-techniques** for when a penalty beats repair (it rarely does on the multidimensional knapsack, where feasible space is thin).

```python
import numpy as np


def repair(
    X: np.ndarray, W: np.ndarray, b: np.ndarray, order: np.ndarray
) -> np.ndarray:
    """Chu & Beasley DROP/ADD repair, vectorized over the population.

    DROP removes items in increasing pseudo-utility from infeasible rows;
    ADD inserts items in decreasing utility wherever they still fit.
    """
    X = X.copy()
    loads = X @ W.T  # (pop, m)
    for j in order[::-1]:  # worst utility first
        violating = (loads > b).any(axis=1) & (X[:, j] == 1)
        if violating.any():
            X[violating, j] = 0
            loads[violating] -= W[:, j]
    for j in order:  # best utility first
        fits = (X[:, j] == 0) & ((loads + W[:, j]) <= b).all(axis=1)
        X[fits, j] = 1
        loads[fits] += W[:, j]
    return X


def mkp_genetic_algorithm(
    profits: np.ndarray,
    W: np.ndarray,
    b: np.ndarray,
    pop_size: int = 100,
    generations: int = 500,
    seed: int = 0,
) -> tuple[int, np.ndarray]:
    """Binary GA with repair for max p'x s.t. Wx <= b, x binary.

    pop_size must be even. Returns (best value, best selection vector).
    """
    rng = np.random.default_rng(seed)
    n = len(profits)
    utility = profits / W.mean(axis=0)  # pseudo-utility drives the repair order
    order = np.argsort(-utility)
    X = repair((rng.random((pop_size, n)) < 0.3).astype(np.int64), W, b, order)
    fit = X @ profits
    for _ in range(generations):
        a, c = rng.integers(0, pop_size, (2, pop_size))  # binary tournaments
        parents = np.where((fit[a] > fit[c])[:, None], X[a], X[c])
        mask = rng.random((pop_size // 2, n)) < 0.5  # uniform crossover
        p1, p2 = parents[0::2], parents[1::2]
        children = np.concatenate([np.where(mask, p1, p2), np.where(mask, p2, p1)])
        children ^= (rng.random((pop_size, n)) < 2.0 / n).astype(np.int64)
        children = repair(children, W, b, order)
        pool = np.vstack([X, children])  # (mu + lambda) elitist replacement
        pool_fit = np.concatenate([fit, children @ profits])
        elite = np.argpartition(-pool_fit, pop_size - 1)[:pop_size]
        X, fit = pool[elite], pool_fit[elite]
    k = int(np.argmax(fit))
    return int(fit[k]), X[k]


rng = np.random.default_rng(7)
W = rng.integers(1, 100, size=(3, 30))
b = (0.5 * W.sum(axis=1)).astype(np.int64)
p = W.mean(axis=0).astype(np.int64) + rng.integers(1, 50, size=30)
best_value, best_x = mkp_genetic_algorithm(p, W, b, pop_size=80, generations=300, seed=1)
print(best_value, int(best_x.sum()))
# Expected: a feasible selection with value within a few percent of the MIP
# optimum for this 30-item instance (cross-check with solve_knapsack_mip
# and validate_knapsack_solution below).
```

Report the LP-relaxation value (or the Lagrangian bound from Advanced Techniques) next to the GA result so the user sees a gap, not just a number.

## Instance Generation and Validation

Controlled synthetic instances are essential for testing: correlation class and capacity tightness are the two hardness dials. The generator follows the standard classes from Pisinger (2005) for single-constraint knapsacks and the Chu & Beasley (1998) scheme for multidimensional ones.

```python
import numpy as np


def generate_knapsack_instance(
    n: int, seed: int, correlation: str = "uncorrelated", r: int = 1000
) -> tuple[np.ndarray, np.ndarray, int]:
    """Generate a 0-1 knapsack instance (profits, weights, capacity).

    Correlation classes follow Pisinger (2005): 'uncorrelated', 'weak'
    (profits near weights), 'strong' (p = w + r/10), 'subset-sum' (p = w).
    Capacity is half the total weight.
    """
    rng = np.random.default_rng(seed)
    w = rng.integers(1, r + 1, size=n)
    if correlation == "uncorrelated":
        p = rng.integers(1, r + 1, size=n)
    elif correlation == "weak":
        p = np.clip(w + rng.integers(-r // 10, r // 10 + 1, size=n), 1, None)
    elif correlation == "strong":
        p = w + r // 10
    elif correlation == "subset-sum":
        p = w.copy()
    else:
        raise ValueError(f"unknown correlation class: {correlation}")
    return p.astype(np.int64), w.astype(np.int64), int(w.sum() // 2)


def generate_mkp_instance(
    n: int, m: int, seed: int, tightness: float = 0.5, r: int = 1000
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Multidimensional knapsack instance in the style of Chu & Beasley (1998).

    Capacities are tightness * row sums; profits correlate with average
    weight plus noise, which makes greedy ordering informative but not exact.
    Returns (profits, (m, n) weights, capacities).
    """
    rng = np.random.default_rng(seed)
    W = rng.integers(1, r + 1, size=(m, n))
    b = (tightness * W.sum(axis=1)).astype(np.int64)
    p = (W.mean(axis=0) / 2 + rng.integers(1, r // 2 + 1, size=n)).astype(np.int64)
    return p, W.astype(np.int64), b


p, w, c = generate_knapsack_instance(8, seed=42, correlation="weak")
print(len(p), len(w), c > 0)
# Expected: 8 8 True — deterministic arrays for seed=42; capacity is half of sum(w).
```

Never trust the solver's own objective report as the final word. Validate every solution — exact or heuristic — with an independent function that recomputes everything from raw data. This catches indexing bugs, scaling mistakes, and stale-variable errors that otherwise survive into papers.

```python
import numpy as np


def validate_knapsack_solution(
    x: np.ndarray,
    profits: np.ndarray,
    weights: np.ndarray,
    capacities: np.ndarray | int,
    bounds: np.ndarray | None = None,
) -> tuple[bool, int]:
    """Independent feasibility + objective check for 0-1/bounded/multidim KP.

    Recomputes the objective and checks every capacity row and item bound
    from the raw data. Returns (feasible, objective).
    """
    x = np.asarray(x, dtype=np.int64)
    W = np.atleast_2d(np.asarray(weights, dtype=np.int64))
    b = np.atleast_1d(np.asarray(capacities, dtype=np.int64))
    upper = np.ones_like(x) if bounds is None else np.asarray(bounds, dtype=np.int64)
    within_bounds = bool(np.all(x >= 0) and np.all(x <= upper))
    within_capacity = bool(np.all(W @ x <= b))
    objective = int(np.asarray(profits, dtype=np.int64) @ x)
    return within_bounds and within_capacity, objective


def validate_multiple_knapsack_solution(
    assign: np.ndarray,
    profits: np.ndarray,
    weights: np.ndarray,
    capacities: np.ndarray,
) -> tuple[bool, int]:
    """Check an (m, n) assignment matrix for the multiple knapsack.

    Verifies binarity, at-most-one placement per item, and every
    per-knapsack capacity. Returns (feasible, objective).
    """
    A = np.asarray(assign, dtype=np.int64)
    w = np.asarray(weights, dtype=np.int64)
    binary = bool(np.all((A == 0) | (A == 1)))
    placed_once = bool(np.all(A.sum(axis=0) <= 1))
    caps_ok = bool(np.all(A @ w <= np.asarray(capacities, dtype=np.int64)))
    objective = int(A.sum(axis=0) @ np.asarray(profits, dtype=np.int64))
    return binary and placed_once and caps_ok, objective


ok, obj = validate_knapsack_solution(
    np.array([0, 1, 1]), np.array([60, 100, 120]), np.array([10, 20, 30]), 50
)
print(ok, obj)
# Expected: True 220
```

Wire the validator into every experiment script: solve, validate, and refuse to log any run whose validator disagrees with the solver's reported objective.

## Advanced Techniques

### Core-based algorithms (Balas & Zemel)

Sort by efficiency and locate the critical item `s`. In optimal solutions of large random instances, almost all items far above `s` in efficiency are selected and almost all far below are not; only a small **core** around `s` is genuinely undecided (Balas & Zemel 1980). Core algorithms fix the outer items, solve the core exactly (DP or B&B), and verify optimality with reduced-cost arguments; if verification fails, the core expands. minknap and combo are expanding-core codes, and this is why they solve `n = 10^5` instances in milliseconds. Use the idea manually when a huge instance must be solved with the tools here: solve a core of 50-100 items around `s` with `knapsack_dp`, then confirm with the Dantzig bound that no fixed item can profitably flip.

### Knapsack as a pricing subproblem

In Gilmore-Gomory column generation for cutting stock, each pricing call asks for a cutting pattern with reduced cost below zero: a pattern `a` minimizing `1 - sum_j dual_j * a_j` subject to `sum_j width_j * a_j <= roll_width`, i.e., an **unbounded knapsack with fractional profits**. Profits are duals, so DP must run over the weight axis (which stays integer), not the profit axis. The same pattern appears in Lagrangian subproblems and cover-cut separation. See **column-generation** for the restricted-master loop around this function.

```python
import numpy as np


def price_cutting_pattern(
    duals: np.ndarray, widths: np.ndarray, roll_width: int, tol: float = 1e-9
) -> tuple[float, np.ndarray] | None:
    """Pricing step of Gilmore-Gomory column generation for cutting stock.

    Solves an unbounded knapsack max duals'a s.t. widths'a <= roll_width
    over integer counts a, by DP on the (integer) width axis. Returns
    (dual value of the pattern, pattern) when the pattern's reduced cost
    1 - value is negative, else None.
    """
    W = int(roll_width)
    value = np.zeros(W + 1)
    choice = np.full(W + 1, -1, dtype=np.int64)
    for d in range(1, W + 1):
        for j in range(len(widths)):
            wj = int(widths[j])
            if wj <= d and value[d - wj] + duals[j] > value[d] + tol:
                value[d] = value[d - wj] + duals[j]
                choice[d] = j
    if value[W] <= 1.0 + tol:
        return None
    pattern = np.zeros(len(widths), dtype=np.int64)
    d = W
    while d > 0 and choice[d] >= 0:
        pattern[choice[d]] += 1
        d -= int(widths[choice[d]])
    return float(value[W]), pattern


result = price_cutting_pattern(np.array([0.4, 0.5]), np.array([3, 4]), roll_width=10)
print(result)
# Expected: (1.3, array([2, 1])) — two width-3 pieces and one width-4 piece;
# reduced cost 1 - 1.3 = -0.3 < 0, so the pattern enters the master.
```

### Lagrangian and surrogate relaxation for the multidimensional knapsack

Dualizing all but one constraint row of `Wx <= b` with multipliers `λ >= 0` leaves a single-constraint 0-1 knapsack solvable by `knapsack_dp`; optimizing `λ` by subgradient gives an upper bound that is often far tighter than the LP for tight instances. The **surrogate relaxation** instead aggregates rows into one constraint `(λᵀW) x <= λᵀb`, again a single knapsack; its bound dominates the Lagrangian bound for this problem class. Both give bound-and-heuristic pairs: the relaxed solution seeds a repair pass. See **lagrangian-relaxation** for multiplier updates, step-size rules, and primal recovery.

### Cover inequalities generated from knapsack rows

A set `C` with `sum_{j in C} w_j > c` is a cover, and `sum_{j in C} x_j <= |C| - 1` is valid; lifting strengthens it. Separation — finding the most violated cover for a fractional `x*` — is itself a 0-1 knapsack: minimize `sum (1 - x*_j) z_j` subject to `sum w_j z_j > c`. Every MIP solver applies these automatically to knapsack-like rows, which is why a general MIP often beats naive B&B on strongly correlated instances. Implement custom separation only inside decomposition schemes where you control the LP.

### From DP to an FPTAS

Scale profits by `K = ε * p_max / n`, run DP over scaled profits (table size `O(n^2 / ε)` on the profit axis), and the result is within factor `1 - ε` of optimal (Ibarra & Kim 1975). Use it when capacity is astronomically large but a quality guarantee is still required; in practice combo-class exact codes usually win anyway, so treat the FPTAS as a fallback with provable behavior rather than the default tool.

## Practical Challenges

**Weights or capacity are fractional, but DP needs integers.** Multiply by a power of ten and round, then check the rounding error against constraint slack: scaled-feasible must imply true-feasible, so round weights up and capacity down. If the needed scale makes `c` huge, switch to B&B or MIP, which never required integrality.

**The DP table exhausts memory.** The value-only rolling array is `O(c)`, but recovery needs the `keep` table at `n * (c+1)` bits. Either pack it with `np.packbits`, or use divide-and-conquer recovery: find the capacity split at item `n/2` from two half-DPs, then recurse — `O(c)` memory, doubles runtime.

**The MIP is slow on strongly correlated single-knapsack instances.** All efficiency ratios are nearly equal, so LP bounds barely discriminate and ratio-based B&B degenerates. Prefer DP whenever `n * c` allows; otherwise rely on the MIP solver's cover cuts rather than a custom B&B, and report the gap honestly if the time limit hits.

**The GA returns infeasible solutions or stalls at low quality.** Infeasibility means repair is missing or runs before mutation instead of after — repair must be the last operator before evaluation. Stalling usually means duplicates flooding the elitist pool; add duplicate elimination, or steal Chu & Beasley's child-replaces-worst steady-state scheme.

**Identical knapsacks make the multiple-knapsack MIP crawl.** Symmetric solutions multiply the tree. Add load-ordering constraints as in `add_load_ordering_constraints`, or aggregate identical containers into one capacity with a count, when the per-container identity does not matter.

**Pricing calls dominate column-generation runtime.** Do not rebuild a Gurobi model per pricing call. Use the DP pricer above (`O(n * W)` per call, no license traffic), cache it across iterations, and accept any column with sufficiently negative reduced cost instead of the most negative one — convergence usually needs fewer total seconds even with more iterations.

**Solver says optimal, validator disagrees.** Almost always an indexing or scaling mismatch between model data and validator data, or reading `.X` values without rounding (Gurobi returns 0.9999999 for binaries at default tolerances). Round with `round(var.X)`, validate in original units, and treat any remaining disagreement as a modeling bug, never as solver noise to ignore.

**Negative profits or a minimization form appears.** Drop items with `p_j <= 0` and `w_j >= 0` upfront (never selected). For minimization-with-covering forms (select items to *cover* at least a demand), complement variables `y_j = 1 - x_j` to recover a maximization knapsack — keep the transformation in one documented function so the validator can check in the original space.

## Tools & Libraries

| Library | When to use | Note |
|---|---|---|
| gurobipy | exact MIP/MIQP for all variants, side constraints | best-in-class B&B with automatic cover cuts; license required |
| numpy | DP, B&B, GA, validators, generators | everything in this skill runs on numpy alone |
| OR-Tools `KnapsackSolver` | fast exact 0-1/multidimensional solving without a MIP license | 64-bit integer B&B; multidimensional via the `*_BRANCH_AND_BOUND` solver type |
| OR-Tools CP-SAT | knapsack plus logical side constraints (conflicts, dependencies) | model capacity as a linear constraint over Booleans |
| HiGHS (via `highspy` or PuLP) | open-source MIP route for KP/multiple/multidimensional | no MIQP; linearize QKP first |
| `mknapsack` (PyPI) | classic Fortran codes (MT1, MTM, MTHM) behind a Python API | Martello-Toth algorithms; solid for single and multiple knapsack |
| pandas | experiment tables across instances/seeds | one row per run: instance, seed, method, value, bound, gap, time |

## Output Format

A complete knapsack deliverable contains:

1. **Variant statement.** One line naming the variant and the formal model used, with `n`, `m`, capacity magnitude, and data source.
2. **Method justification.** Which method was chosen and why, referencing the data regime (e.g., "integer weights, n*c = 2e6, DP exact in 0.1 s").
3. **Solution-quality table.**

| Field | Value |
|---|---|
| Instance | name / generator seed and parameters |
| Method | DP / B&B / MIP / GA + repair |
| Objective (validated) | integer value from the independent validator |
| Upper bound | LP, Dantzig, Lagrangian, or solver bound |
| Gap | (bound - objective) / bound, in percent |
| Status | proven optimal / time limit / heuristic |
| Wall time | seconds |
| Seed(s) | every RNG seed used |

4. **Validation line.** Explicit confirmation that `validate_knapsack_solution` (or the multiple-knapsack variant) returned feasible with the reported objective — quoted, not implied.
5. **Solution artifact.** The selected item indices (or assignment matrix) written to CSV/JSON next to the run metadata, so results are reproducible without rerunning the solver.
6. **For heuristic runs:** number of seeds, best/mean/worst values, and the bound used to estimate the gap. Never report a single heuristic run as "the" result.

## Questions to Ask

- Which variant is this exactly: one knapsack or several, one resource dimension or many, binary or integer item counts, any pairwise interaction profits?
- Are weights, profits, and capacity integers? If fractional, what precision actually matters?
- How large is the instance (`n`, `m`) and how large is the capacity relative to weights?
- Do you need a proven optimum, or is a small, quantified gap acceptable?
- Is the knapsack the whole problem, or a subroutine called many times inside something larger?
- What is the time budget per solve, and is a Gurobi license available?
- Where does the data come from — should I expect correlated profits and weights?
- Are there side constraints (item conflicts, precedences, mandatory items) that change the problem class?
- How will results be consumed: one solution, or a benchmark table across instances and seeds?

## Related Skills

- **dynamic-programming** — when state design, memory-saving recurrences, or labeling extensions of the knapsack DP are the focus.
- **branch-and-bound** — when building custom tree search: node selection, bounding functions, and dominance beyond the basic B&B here.
- **genetic-algorithms** — when tuning the GA loop itself: selection pressure, crossover choice, population sizing for the binary encoding.
- **constraint-handling-techniques** — when deciding between penalty, repair, and decoder approaches for capacity constraints in metaheuristics.
- **column-generation** — when the knapsack is the pricing subproblem and the restricted master loop, convergence, and stabilization matter.
- **lagrangian-relaxation** — when multiplier optimization, subgradient step sizes, and Lagrangian bounds for the multidimensional knapsack are needed.
