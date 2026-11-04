---
name: branch-and-bound
description: When the user wants to implement a custom branch-and-bound algorithm — designing bounding functions, branching rules, node selection (depth-first vs best-first), dominance rules, and incumbent management — or to decide when custom B&B beats a MIP solver. Also use when the user mentions "custom branch and bound," "bounding function," "branching rule," "node selection," "best-first search," or when the bounding relaxation is combinatorial rather than an LP. For solver-internal B&B and MIP gaps, see integer-programming-techniques; for branch-and-price trees, see column-generation.
---

# Branch-and-Bound

You are an expert in exact combinatorial optimization, specifically in designing and implementing custom branch-and-bound (B&B) algorithms. This skill covers the five design decisions of any B&B — bounding function, branching rule, node selection, dominance rules, and incumbent management — plus the engineering judgment of when a hand-built tree search beats a commercial MIP solver. Use the framework below to assess the problem, pick each component deliberately, implement against the reusable engine, and validate the result against an independent exact baseline.

## Initial Assessment

Before writing any code, establish the following. Each answer changes a design decision downstream.

- **Optimization sense.** Minimization or maximization? Pick one convention for the implementation (the engine below minimizes; negate to maximize) and never mix the two.
- **Objective integrality.** If all costs are integers, you can prune a node whenever `ceil(bound) >= incumbent`. This is free pruning power; confirm it before discarding it.
- **Instance size, now and at target scale.** Estimate depth × branching factor. A depth-40 binary tree is fine; a depth-200 one needs a very strong bound or it will not finish.
- **Available relaxations.** What can you solve fast that bounds the problem? LP relaxation, assignment problem, knapsack greedy bound, a DP over a relaxed state space, a Lagrangian dual. Measure the root gap (relaxation value vs best known solution) before committing — it is the single best predictor of tree size.
- **Bound cost vs bound strength.** A bound evaluated a million times must be O(n) or amortized O(n); an O(n^3) bound must close the gap enough to pay for itself in pruned nodes.
- **MIP solver availability and license.** If gurobipy (or HiGHS/SCIP) handles the formulation, build that model first as the correctness baseline and the performance bar to beat.
- **Proof requirement.** Does the user need proven optimality, a certified gap (e.g., within 1%), or just the best solution found within a time budget? This sets the termination criterion and how you report results.
- **Memory budget.** Best-first search can hold an exponential open list. Tight memory pushes you toward DFS or a hybrid.
- **Incumbent source.** Is there a fast construction heuristic for an initial upper bound? Without an early incumbent, no bound-based pruning happens until the first leaf.
- **Dominance structure.** Can two partial solutions over the same remaining decisions be compared componentwise (one weakly better in every respect)? If yes, dominance rules can prune more than bounds do.
- **Determinism and logging needs.** Research use demands reproducible node counts: fix tie-breaking explicitly (insertion counters), fix seeds in instance generation, and log nodes explored/pruned and incumbent updates.
- **Future extensions.** If the tree will later host column generation (branch-and-price) or custom cuts, branching decisions must be expressible inside the pricing/separation subproblem — design the node state accordingly.

## Algorithm Anatomy

Branch-and-bound (Land & Doig 1960, "An automatic method of solving discrete programming problems"; the name is from Little, Murty, Sweeney & Karel 1963, "An algorithm for the traveling salesman problem") solves

$$
z^* = \min_{x \in S} f(x)
$$

by recursively splitting the solution set $S$ into subsets $S_1, \dots, S_k$ (branching) and computing for each subset a lower bound $b(S_i) \le \min_{x \in S_i} f(x)$ (bounding). With $\bar{z}$ the value of the best feasible solution found so far (the incumbent), a node is discarded — pruned — for one of three reasons:

1. **Bound:** $b(S_i) \ge \bar{z}$ — no completion can strictly improve the incumbent.
2. **Infeasibility:** $S_i = \emptyset$ — the relaxation itself is infeasible (signal with $b(S_i) = +\infty$).
3. **Optimality / dominance:** the subset's best completion is known exactly, or another node provably leads to a solution at least as good (Ibaraki 1977, "The power of dominance relations in branch-and-bound algorithms").

The algorithm is exact as long as (a) branching *covers* all solutions of the parent (a partition is ideal, but overlapping covers are still correct, only wasteful) and (b) the bound is valid for *every* completion of the node. Termination with an empty frontier proves $\bar{z} = z^*$.

### The five design decisions

| Component | Question it answers | Default starting point |
|---|---|---|
| Bounding function | How do I underestimate the best completion cheaply? | The tightest relaxation you can solve in O(n)–O(n^2) per node |
| Branching rule | How do I split a node so children are smaller and balanced? | Fix the most constrained / most fractional decision; smallest valid branching set |
| Node selection | Which open node do I expand next? | Best-first if memory allows; DFS dives for incumbents otherwise |
| Dominance rules | Can another node make this one redundant? | Per-state Pareto filter when partial solutions are comparable |
| Incumbent management | Where do upper bounds come from? | Construction heuristic at the root; feasibility checks at every node |

### Node selection trade-offs

| Strategy | Open-list memory | First incumbent | Total nodes to prove optimality | Use when |
|---|---|---|---|---|
| Depth-first (DFS) | O(depth × branching factor) | Fast (dives to a leaf) | Often more than best-first | Memory is tight; good branching order known |
| Best-first (best bound) | Can grow exponentially | Slow (only at leaves) | Minimal for a fixed branching rule (never expands a node with bound above $z^*$) | Bound is strong; memory is available |
| DFS dive + best-first (hybrid) | Moderate | Fast | Near-minimal | Default for serious implementations; this is what MIP solvers do |
| Breadth-first | Exponential, fast | Slowest | No advantage | Almost never |

Best-first with a *consistent* bound (child bound ≥ parent bound) expands only nodes with bound < $z^*$, which is optimal among node orders for that bound — but it pays in memory and in late incumbents. See Morrison, Jacobson, Sauppe & Sewell (2016), "Branch-and-bound algorithms: A survey of recent advances in searching, branching, and pruning" for a thorough treatment.

### When custom B&B beats a MIP solver

Write the MIP first. Gurobi/HiGHS/SCIP embody decades of presolve, cut, and heuristic engineering; a naive custom B&B loses to them on any plain MILP. Build your own tree only when at least one of these holds:

- **The bound is combinatorial and much cheaper than an LP.** Assignment relaxation in O(n^3) with O(n^2) re-optimization per child, a greedy knapsack bound in O(n), a DP bound — evaluated millions of times, these beat repeated LP solves.
- **Dominance rules exist that a MIP cannot express.** Componentwise comparisons between partial schedules/loads prune entire subtrees that LP bounds cannot touch.
- **The formulation is exponential.** Branch-and-price (see column-generation) requires custom branching compatible with the pricing oracle.
- **The problem is small but solved millions of times** (real-time or inside a heuristic loop), where solver model-build overhead dominates.
- **Specialized constraint propagation** at each node (scheduling, routing resources) is stronger than the MIP relaxation.

If none apply, stop here and use the solver — see integer-programming-techniques for getting the most out of it.

### Complexity notes

B&B has exponential worst-case time; its practical value is entirely in how far pruning cuts the $2^n$ (or $n!$) tree. Useful instrumentation: nodes explored, nodes pruned by bound vs by dominance, root gap, and incumbent-update trace. A root gap above ~10% on a deep tree is a warning that the bound, not the code, needs work.

## Generic Branch-and-Bound Framework

The engine below is the reusable artifact: minimization, pluggable callbacks, best-first or DFS node selection, stale-bound re-checks, integral-objective pruning, and a time limit. The worked examples later in this skill follow exactly this anatomy (they are written self-contained so each block runs as-is).

```text
BRANCH-AND-BOUND (minimization)
-------------------------------
input: root node, callbacks lower_bound / branch / is_complete / objective
state: incumbent (z_bar, x_bar), frontier of (bound, node)

1. z_bar <- heuristic value (or +inf); push (lower_bound(root), root)
2. while frontier not empty and time remains:
3.     pop node N                      # heap pop (best-first) or stack pop (DFS)
4.     if bound(N) >= z_bar: prune     # bound may be stale -> re-check at pop
5.     if N is complete:
6.         if objective(N) < z_bar: update incumbent
7.         continue
8.     for child C in branch(N):       # children must cover all solutions of N
9.         b <- lower_bound(C)
10.        if b < z_bar: push (b, C)   # else pruned at birth
11. return incumbent; optimal iff loop ended with empty frontier
```

```python
"""Reusable branch-and-bound engine: pluggable bound, branching, and node selection."""
from __future__ import annotations

import heapq
import itertools
import math
import time
from dataclasses import dataclass
from typing import Any, Callable, Iterable


@dataclass
class BnBResult:
    """Outcome of a branch-and-bound run."""

    best_value: float
    best_node: Any
    nodes_explored: int
    nodes_pruned: int
    proven_optimal: bool
    runtime: float


class BranchAndBound:
    """Minimization branch-and-bound. To maximize, negate bounds and objectives.

    Callbacks:
        lower_bound(node):  valid lower bound on every completion of the node;
                            return math.inf to declare the node infeasible.
        branch(node):       child nodes covering all solutions of the node.
        is_complete(node):  True if the node encodes one full feasible solution.
        objective(node):    exact objective value of a complete node.
    """

    def __init__(
        self,
        lower_bound: Callable[[Any], float],
        branch: Callable[[Any], Iterable[Any]],
        is_complete: Callable[[Any], bool],
        objective: Callable[[Any], float],
        node_selection: str = "best-first",  # "best-first" or "dfs"
        integral_objective: bool = False,
        tol: float = 1e-9,
    ) -> None:
        self.lower_bound = lower_bound
        self.branch = branch
        self.is_complete = is_complete
        self.objective = objective
        self.node_selection = node_selection
        self.integral_objective = integral_objective
        self.tol = tol

    def _prunable(self, bound: float, incumbent: float) -> bool:
        """True when no completion under this bound can beat the incumbent."""
        if self.integral_objective:
            return math.ceil(bound - self.tol) >= incumbent
        return bound >= incumbent - self.tol

    def solve(
        self,
        root: Any,
        incumbent_value: float = math.inf,
        incumbent_node: Any = None,
        time_limit: float = math.inf,
    ) -> BnBResult:
        """Explore the tree rooted at `root`; return the best solution found."""
        start = time.perf_counter()
        tie = itertools.count()  # deterministic heap tie-breaking
        explored = pruned = 0
        best_value, best_node = incumbent_value, incumbent_node
        frontier: list[tuple[float, int, Any]] = [(self.lower_bound(root), next(tie), root)]
        timed_out = False
        while frontier:
            if time.perf_counter() - start > time_limit:
                timed_out = True
                break
            if self.node_selection == "best-first":
                bound, _, node = heapq.heappop(frontier)
            else:  # dfs: frontier behaves as a stack
                bound, _, node = frontier.pop()
            if self._prunable(bound, best_value):  # bound may be stale by now
                pruned += 1
                continue
            explored += 1
            if self.is_complete(node):
                value = self.objective(node)
                if value < best_value:
                    best_value, best_node = value, node
                continue
            children = []
            for child in self.branch(node):
                child_bound = self.lower_bound(child)
                if self._prunable(child_bound, best_value):
                    pruned += 1
                else:
                    children.append((child_bound, next(tie), child))
            if self.node_selection == "best-first":
                for entry in children:
                    heapq.heappush(frontier, entry)
            else:  # push the most promising child last so it is popped first
                children.sort(key=lambda entry: entry[0], reverse=True)
                frontier.extend(children)
        return BnBResult(
            best_value, best_node, explored, pruned, not timed_out, time.perf_counter() - start
        )


def _demo() -> None:
    """Pick exactly k of n items at minimum total cost (toy wiring example).

    Node = (next_index, chosen_indices). Bound = chosen cost + k' smallest
    remaining costs, where k' items are still to be picked.
    """
    costs = [7.0, 2.0, 5.0, 3.0, 9.0]
    k, n = 2, 5

    def lower_bound(node: tuple[int, tuple[int, ...]]) -> float:
        i, chosen = node
        need = k - len(chosen)
        remaining = sorted(costs[i:])
        if need > len(remaining):
            return math.inf  # infeasible: not enough items left
        return sum(costs[j] for j in chosen) + sum(remaining[:need])

    def branch(node: tuple[int, tuple[int, ...]]) -> list[tuple[int, tuple[int, ...]]]:
        i, chosen = node
        children = []
        if len(chosen) < k:
            children.append((i + 1, chosen + (i,)))  # take item i
        if n - i - 1 >= k - len(chosen):
            children.append((i + 1, chosen))  # skip item i (still completable)
        return children

    engine = BranchAndBound(
        lower_bound=lower_bound,
        branch=branch,
        is_complete=lambda node: len(node[1]) == k,
        objective=lambda node: sum(costs[j] for j in node[1]),
        node_selection="best-first",
    )
    result = engine.solve(root=(0, ()))
    print(result.best_value, result.best_node[1], result.nodes_explored)


_demo()
# Expected: 5.0 (1, 3) 5  -- items 1 and 3 at total cost 5, five nodes explored
```

Two details in the engine repay attention. First, bounds are re-checked at pop time: a node pushed before an incumbent improvement may be prunable by the time it surfaces. Second, the deterministic tie counter makes node counts reproducible run-to-run, which you need for honest benchmarking.

## Worked Example 1: 0-1 Knapsack with LP Bound

The 0-1 knapsack problem:

$$
\max \sum_{i=1}^{n} v_i x_i \quad \text{s.t.} \quad \sum_{i=1}^{n} w_i x_i \le C, \qquad x \in \{0,1\}^n .
$$

Its LP relaxation has a closed-form optimum (Dantzig 1957, "Discrete-variable extremum problems"). Sort items by value density $v_1/w_1 \ge v_2/w_2 \ge \dots$, let the *break item* be $s = \min\{ j : \sum_{i \le j} w_i > C \}$, and let $\bar{C} = C - \sum_{i < s} w_i$ be the residual capacity. The LP optimum — a valid upper bound on every 0-1 completion — is

$$
U_{\mathrm{Dantzig}} = \sum_{i < s} v_i + \bar{C}\,\frac{v_s}{w_s}.
$$

It costs O(n) per node (O(1) amortized with suffix preprocessing), and with integral values you may use $\lfloor U \rfloor$. Branching fixes the next item in density order to 1 (if it fits) or 0 — the classic schemes of Kolesar (1967) and the DFS variant of Horowitz & Sahni (1974); Martello & Toth (1990, *Knapsack Problems*) is the reference text. Because every node's partial selection is itself feasible, the incumbent can be updated at *every* node, not only at leaves.

```python
"""0-1 knapsack branch-and-bound with the Dantzig LP-relaxation upper bound."""
from __future__ import annotations

import heapq
import itertools

import numpy as np


def solve_knapsack_bb(
    values: list[float],
    weights: list[float],
    capacity: float,
    node_selection: str = "best-first",
) -> tuple[float, list[int], int]:
    """Maximize value under one capacity constraint.

    Returns (optimal value, chosen item indices, nodes explored).
    """
    n = len(values)
    order = sorted(range(n), key=lambda i: values[i] / weights[i], reverse=True)
    v = [values[i] for i in order]
    w = [weights[i] for i in order]

    def upper_bound(level: int, value: float, weight: float) -> float:
        """Dantzig bound: greedy fill in density order, fractional break item."""
        cap = capacity - weight
        bound = value
        for j in range(level, n):
            if w[j] <= cap:
                cap -= w[j]
                bound += v[j]
            else:
                bound += v[j] * cap / w[j]
                break
        return bound

    tie = itertools.count()
    best_value, best_set = 0.0, ()
    root = (-upper_bound(0, 0.0, 0.0), next(tie), 0, 0.0, 0.0, ())
    frontier = [root]
    explored = 0
    while frontier:
        if node_selection == "best-first":
            neg_bound, _, level, value, weight, taken = heapq.heappop(frontier)
        else:
            neg_bound, _, level, value, weight, taken = frontier.pop()
        if -neg_bound <= best_value + 1e-9:  # stale or never-promising node
            continue
        explored += 1
        if value > best_value:  # every partial selection is feasible
            best_value, best_set = value, taken
        if level == n:
            continue
        children = []
        if weight + w[level] <= capacity:  # branch x[level] = 1
            children.append((level + 1, value + v[level], weight + w[level], taken + (level,)))
        children.append((level + 1, value, weight, taken))  # branch x[level] = 0
        scored = []
        for lvl, val, wt, tk in children:
            ub = upper_bound(lvl, val, wt)
            if ub > best_value + 1e-9:
                scored.append((-ub, next(tie), lvl, val, wt, tk))
        if node_selection == "best-first":
            for entry in scored:
                heapq.heappush(frontier, entry)
        else:  # DFS: pop the highest-bound child first
            scored.sort(key=lambda entry: entry[0], reverse=True)
            frontier.extend(scored)
    chosen = sorted(order[j] for j in best_set)
    return best_value, chosen, explored


# --- tiny instance ---------------------------------------------------------
values, weights, capacity = [60.0, 100.0, 120.0], [10.0, 20.0, 30.0], 50.0
best, items, nodes = solve_knapsack_bb(values, weights, capacity)
print(best, items, nodes)
# Expected: 220.0 [1, 2] with a single-digit node count

# --- seeded weakly correlated instance (harder for the bound) --------------
rng = np.random.default_rng(7)
w_arr = rng.integers(20, 70, size=30).astype(float)
v_arr = (w_arr + rng.integers(1, 30, size=30)).astype(float)
cap = float(0.5 * w_arr.sum())
for strategy in ("best-first", "dfs"):
    best, items, nodes = solve_knapsack_bb(list(v_arr), list(w_arr), cap, strategy)
    print(strategy, best, nodes)
# Expected: optimum 1037.0 from both strategies; best-first explores fewer
# nodes than DFS here (128 vs 162) -- it never expands a node with bound <= optimum
```

Validate any custom B&B against an independent exact solve before trusting node-count experiments. The MIP takes ten lines:

```python
"""Cross-check the custom knapsack B&B against a gurobipy MIP solve."""
import gurobipy as gp
from gurobipy import GRB


def solve_knapsack_mip(
    values: list[float], weights: list[float], capacity: float
) -> tuple[float, list[int]]:
    """Solve the 0-1 knapsack as a MIP; reference baseline for the custom B&B."""
    n = len(values)
    model = gp.Model("knapsack")
    model.Params.OutputFlag = 0
    x = model.addVars(n, vtype=GRB.BINARY, name="x")
    model.addConstr(
        gp.quicksum(weights[i] * x[i] for i in range(n)) <= capacity, name="capacity"
    )
    model.setObjective(gp.quicksum(values[i] * x[i] for i in range(n)), GRB.MAXIMIZE)
    model.optimize()
    if model.Status != GRB.OPTIMAL:
        raise RuntimeError(f"unexpected solver status {model.Status}")
    chosen = [i for i in range(n) if x[i].X > 0.5]
    return model.ObjVal, chosen


obj, chosen = solve_knapsack_mip([60.0, 100.0, 120.0], [10.0, 20.0, 30.0], 50.0)
print(obj, chosen)
# Expected: 220.0 [1, 2] -- matches the custom B&B exactly
```

### Bound strength is the whole game

The experiment below swaps the Dantzig bound for the naive "add all remaining values" bound inside an otherwise identical DFS B&B. Same optimum, wildly different node counts — this is the empirical case for investing in the bound before anything else.

```python
"""Bound-strength experiment: Dantzig LP bound vs naive remaining-value bound."""
from __future__ import annotations

from typing import Callable

import numpy as np
import pandas as pd


def bb_node_count(
    v: np.ndarray, w: np.ndarray, capacity: float, bound: Callable[[int, float, float], float]
) -> tuple[float, int]:
    """Lean DFS knapsack B&B (items pre-sorted by density); returns (optimum, nodes)."""
    n = len(v)
    best, explored = 0.0, 0
    stack = [(0, 0.0, 0.0)]
    while stack:
        level, value, weight = stack.pop()
        if bound(level, value, weight) <= best + 1e-9:
            continue
        explored += 1
        best = max(best, value)
        if level == n:
            continue
        stack.append((level + 1, value, weight))  # exclude first ...
        if weight + w[level] <= capacity:
            stack.append((level + 1, value + v[level], weight + w[level]))  # ... include on top
    return best, explored


def make_dantzig_bound(
    v: np.ndarray, w: np.ndarray, capacity: float
) -> Callable[[int, float, float], float]:
    """LP-relaxation bound: greedy fill plus fractional break item."""

    def bound(level: int, value: float, weight: float) -> float:
        cap, total = capacity - weight, value
        for j in range(level, len(v)):
            if w[j] <= cap:
                cap -= w[j]
                total += v[j]
            else:
                total += v[j] * cap / w[j]
                break
        return total

    return bound


def make_naive_bound(
    v: np.ndarray, w: np.ndarray, capacity: float
) -> Callable[[int, float, float], float]:
    """Weak bound: current value plus the sum of all remaining values."""
    suffix = np.concatenate([np.cumsum(v[::-1])[::-1], [0.0]])

    def bound(level: int, value: float, weight: float) -> float:
        return value + float(suffix[level])

    return bound


rows = []
for seed in range(5):
    rng = np.random.default_rng(seed)
    w_arr = rng.integers(20, 70, size=24).astype(float)
    v_arr = (w_arr + rng.integers(1, 30, size=24)).astype(float)
    density_order = np.argsort(-v_arr / w_arr)
    v_arr, w_arr = v_arr[density_order], w_arr[density_order]
    cap = float(0.5 * w_arr.sum())
    for name, factory in [("dantzig", make_dantzig_bound), ("naive", make_naive_bound)]:
        opt, nodes = bb_node_count(v_arr, w_arr, cap, factory(v_arr, w_arr, cap))
        rows.append({"seed": seed, "bound": name, "optimum": opt, "nodes": nodes})

table = pd.DataFrame(rows)
print(table.pivot(index="seed", columns="bound", values="nodes"))
assert table.groupby("seed")["optimum"].nunique().eq(1).all()  # same optimum either way
# Expected: identical optima per seed; the naive bound explores roughly 10,000x
# more nodes (about 1.6-2.4 million vs 15-288 across these five seeds)
```

## Worked Example 2: TSP B&B with Assignment Relaxation

The asymmetric TSP (ATSP) over cost matrix $c_{ij}$:

$$
\min \sum_{i \ne j} c_{ij} x_{ij}
\quad \text{s.t.} \quad
\sum_{j} x_{ij} = 1 \;\; \forall i, \qquad
\sum_{i} x_{ij} = 1 \;\; \forall j, \qquad
x \in \{0,1\}^{n \times n},
$$

plus subtour-elimination constraints. Dropping subtour elimination leaves the **assignment problem (AP)**, solvable in O(n^3) by the Hungarian algorithm. The AP optimum is a valid lower bound on the ATSP, and its solution decomposes into disjoint directed cycles:

- **One cycle covering all cities** → the AP solution *is* an optimal tour for this node; the node is complete.
- **Several cycles** → branch. Any Hamiltonian tour must omit at least one arc of any proper subtour (a tour cannot contain a full smaller cycle), so creating one child per arc of a chosen subtour, each child forbidding that arc, covers all tours (Bellmore & Malone 1971, "Pathology of traveling-salesman subtour-elimination algorithms"). Choose the *shortest* subtour to minimize the branching factor. Carpaneto & Toth (1980, "Some new branching and bounding criteria for the asymmetric travelling salesman problem") refine this into disjoint children by additionally forcing the arcs already considered.

The AP bound is excellent on asymmetric instances — typically within 1-2% of the optimum on random ATSP (Balas & Toth 1985, "Branch and bound methods", in Lawler et al., *The Traveling Salesman Problem*) — but weak on **symmetric** instances, where cheap 2-cycles (i→j→i) dominate the AP solution; use the Held-Karp 1-tree bound there instead (see Advanced Techniques).

```python
"""ATSP branch-and-bound: assignment-relaxation bound, subtour-arc branching."""
from __future__ import annotations

import heapq
import itertools

import numpy as np
from scipy.optimize import linear_sum_assignment


def assignment_bound(cost: np.ndarray) -> tuple[float, np.ndarray]:
    """Solve the AP relaxation; return (bound value, successor array)."""
    rows, cols = linear_sum_assignment(cost)
    succ = np.empty(len(cost), dtype=int)
    succ[rows] = cols
    return float(cost[rows, cols].sum()), succ


def cycles_of(succ: np.ndarray) -> list[list[int]]:
    """Decompose an assignment's successor function into directed cycles."""
    seen = np.zeros(len(succ), dtype=bool)
    result = []
    for start in range(len(succ)):
        if seen[start]:
            continue
        cycle, node = [], start
        while not seen[node]:
            seen[node] = True
            cycle.append(node)
            node = int(succ[node])
        result.append(cycle)
    return result


def nearest_neighbor_tour(dist: np.ndarray) -> tuple[float, list[int]]:
    """Greedy construction for the initial incumbent."""
    n = len(dist)
    tour, unvisited = [0], set(range(1, n))
    while unvisited:
        last = tour[-1]
        nxt = min(unvisited, key=lambda j: dist[last, j])
        unvisited.remove(nxt)
        tour.append(nxt)
    cost = sum(float(dist[tour[i], tour[(i + 1) % n]]) for i in range(n))
    return cost, tour


def solve_atsp_bb(dist: np.ndarray) -> tuple[float, list[int], int]:
    """Best-first B&B for the (a)symmetric TSP with the AP bound.

    Returns (tour cost, tour as a city list starting at 0, nodes explored).
    Forbidden arcs are encoded by a BIG cost; an AP value >= BIG means the
    node has no feasible assignment and is pruned.
    """
    n = len(dist)
    big = float(dist[np.isfinite(dist)].max()) * (n + 1) + 1.0
    cost0 = dist.astype(float).copy()
    np.fill_diagonal(cost0, big)

    best_value, best_tour = nearest_neighbor_tour(dist)
    tie = itertools.count()
    bound0, succ0 = assignment_bound(cost0)
    frontier = [(bound0, next(tie), cost0, succ0)]
    explored = 0
    while frontier:
        bound, _, cost, succ = heapq.heappop(frontier)
        if bound >= best_value - 1e-9 or bound >= big:
            continue
        explored += 1
        subtours = cycles_of(succ)
        if len(subtours) == 1:  # the AP solution is a Hamiltonian tour
            tour = subtours[0]
            shift = tour.index(0)
            best_value, best_tour = bound, tour[shift:] + tour[:shift]
            continue
        branch_cycle = min(subtours, key=len)  # smallest branching factor
        for i in branch_cycle:  # child k forbids arc (i, succ[i])
            child_cost = cost.copy()
            child_cost[i, int(succ[i])] = big
            child_bound, child_succ = assignment_bound(child_cost)
            if child_bound < best_value - 1e-9 and child_bound < big:
                heapq.heappush(frontier, (child_bound, next(tie), child_cost, child_succ))
    return best_value, best_tour, explored


# --- tiny symmetric instance ------------------------------------------------
d4 = np.array(
    [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0],
    ],
    dtype=float,
)
cost, tour, nodes = solve_atsp_bb(d4)
print(cost, tour, nodes)
# Expected: 80.0 [0, 1, 3, 2] 0 -- nearest neighbor already hits the optimum,
# the AP root bound equals 80, so the whole tree is pruned without branching

# --- seeded asymmetric instance ---------------------------------------------
rng = np.random.default_rng(14)
d9 = rng.integers(10, 100, size=(9, 9)).astype(float)
cost, tour, nodes = solve_atsp_bb(d9)
print(cost, sorted(tour) == list(range(9)), nodes)
# Expected: 278.0 True 7 -- seven nodes explored; the cost is confirmed by the
# Held-Karp cross-check below
```

The 4-city run shows the ideal case: heuristic incumbent = relaxation bound, zero branching. Always check this at the root before celebrating a "fast" B&B — a strong bound plus a good heuristic sometimes means the search itself is doing nothing, and a pure heuristic-plus-bound report would suffice.

Cross-check against Held-Karp dynamic programming (exact for n up to ~18; see dynamic-programming for the recursion in depth):

```python
"""Held-Karp DP cross-check for the TSP B&B (exact, O(n^2 2^n))."""
from __future__ import annotations

import math

import numpy as np


def held_karp(dist: np.ndarray) -> float:
    """Exact TSP optimum by bitmask DP over subsets of cities 1..n-1."""
    n = len(dist)
    full = 1 << (n - 1)
    dp = np.full((full, n - 1), math.inf)
    for j in range(n - 1):
        dp[1 << j, j] = dist[0, j + 1]
    for mask in range(full):
        for j in range(n - 1):
            if not (mask >> j) & 1 or math.isinf(dp[mask, j]):
                continue
            for k in range(n - 1):
                if (mask >> k) & 1:
                    continue
                cand = dp[mask, j] + dist[j + 1, k + 1]
                if cand < dp[mask | (1 << k), k]:
                    dp[mask | (1 << k), k] = cand
    return float(min(dp[full - 1, j] + dist[j + 1, 0] for j in range(n - 1)))


d4 = np.array(
    [[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]], dtype=float
)
print(held_karp(d4))
# Expected: 80.0 -- matches the B&B result

rng = np.random.default_rng(14)  # same seed as the B&B block above
d9 = rng.integers(10, 100, size=(9, 9)).astype(float)
print(held_karp(d9))
# Expected: 278.0 -- identical to the B&B optimum on the seeded instance
```

Implementation notes worth copying into any AP-based B&B:

- **Re-optimization, not re-solving.** Forbidding one arc invalidates one row's assignment; the Hungarian method re-optimizes in O(n^2) from the parent's dual values instead of O(n^3) from scratch. The teaching code above re-solves for clarity; production code should not.
- **BIG, not infinity.** `linear_sum_assignment` handling of infeasible entries varies; a finite BIG plus an explicit `bound >= big` infeasibility check is portable and makes the pruning logic visible.
- **Matrix-per-node memory.** Storing an n×n copy per open node costs O(n^2) each; for larger n, store only the forbidden-arc list and rebuild (or re-optimize) at pop time.

## Advanced Techniques

### Stronger bounds: Lagrangian and 1-tree

When the natural relaxation is weak, dualize the complicating constraints and optimize the multipliers. For the symmetric TSP, the Held-Karp 1-tree bound (Held & Karp 1970-1971, "The traveling-salesman problem and minimum spanning trees" I-II) computes a minimum spanning tree on cities 2..n plus the two cheapest edges at city 1, with node-degree penalties updated by subgradient steps; it reaches within ~1% of the optimum where the AP bound stalls on 2-cycles. For knapsack, the Martello-Toth bound tightens Dantzig by considering the break item's exclusion and inclusion separately. The general recipe: bound strength is worth almost any per-node cost you can amortize, because tree size is exponential in the gap.

### Dominance rules

When two nodes face the *same remaining decision set*, componentwise comparison can prune without any bound. In density-ordered knapsack, a node with (weight, value) = (10, 50) at level 3 dominates (12, 45) at level 3: less capacity used, more value collected, identical items remaining. Keep a per-level Pareto store:

```python
"""Per-level dominance filter for knapsack-style B&B nodes."""
from __future__ import annotations


class DominanceFilter:
    """Per tree level, keep the Pareto-undominated (weight, value) pairs seen.

    Valid only when nodes at the same level share the same remaining
    decisions (fixed item order). A node is rejected when an earlier node
    has weight <= its weight and value >= its value.
    """

    def __init__(self) -> None:
        self._pareto: dict[int, list[tuple[float, float]]] = {}

    def admit(self, level: int, weight: float, value: float) -> bool:
        """Record and accept the node unless a stored pair dominates it."""
        pairs = self._pareto.setdefault(level, [])
        for w, v in pairs:
            if w <= weight and v >= value:
                return False
        pairs[:] = [(w, v) for (w, v) in pairs if not (weight <= w and value >= v)]
        pairs.append((weight, value))
        return True


flt = DominanceFilter()
print(flt.admit(3, 10.0, 50.0), flt.admit(3, 12.0, 45.0), flt.admit(3, 9.0, 55.0))
# Expected: True False True -- the second node is dominated by the first
```

This is exactly the mechanism that turns knapsack B&B into the DP recursion when applied exhaustively (Ibaraki 1977) — dominance and dynamic programming are two ends of one spectrum.

### Branching rule design

Branch on the decision that *most constrains* the children: the fractional break item in knapsack, the shortest subtour in ATSP, the most fractional variable in LP-based trees. Emulate strong branching when the bound is cheap: tentatively evaluate the bound of each candidate branching decision and pick the one maximizing the *minimum* child bound — fewer, harder children beat many easy ones. For covering (non-partition) schemes like Bellmore-Malone arc exclusion, switch to the Carpaneto-Toth disjoint variant when profiling shows repeated subproblems.

### Node selection hybrids and memory control

The production pattern is best-first with DFS *diving*: pop the best-bound node, then follow one greedy child path to a leaf (updating the incumbent), then return to the heap. This gets DFS's early incumbents and best-first's small proven-optimal tree. Under memory pressure, cap the open list and overflow into DFS on the worst-bound nodes, or store nodes as (parent pointer + one decision) and rebuild state on pop — O(depth) rebuild against O(n) state per node is usually a good trade.

### Incumbent management

Treat the incumbent pipeline as a first-class component: a construction heuristic at the root (nearest neighbor above; greedy by density for knapsack), cheap completion heuristics at interior nodes (round the LP solution, patch AP subtours into a tour — Karp 1979 patching), and optionally a few local-search iterations on every new incumbent. Every incumbent improvement immediately re-prunes the open list, so heuristic effort inside the tree pays compound interest. Log every incumbent with its timestamp and node count: time-to-first-good-solution is often the metric users actually care about.

## Practical Challenges

**The tree explodes even on medium instances.** Measure the root gap first: `(incumbent - root_bound) / incumbent`. If it exceeds a few percent on a deep tree, no search-order trick will save you — invest in the bound (Lagrangian, problem-specific tightening) or add dominance rules. Node-selection tuning changes constants; bound strength changes the exponent.

**Floating-point pruning cuts off the true optimum.** Pruning with `bound >= incumbent` and accumulated float error can discard the optimal branch. Always prune with a tolerance (`bound >= incumbent - 1e-9`), and when objectives are integral, prune with `ceil(bound - tol) >= incumbent` — stronger *and* safer. Unit-test on instances with known optima (see the cross-check blocks above).

**Best-first runs out of memory.** The open list of best-first search can grow exponentially before the first incumbent. Switch to the dive-and-best-first hybrid, store compact node encodings (decision diffs, not full states), or impose an open-list cap with DFS overflow. If memory still binds, plain DFS with a strong branching order is the honest fallback.

**Each node re-solves the relaxation from scratch.** Re-solving the AP in O(n^3) per child when O(n^2) re-optimization from parent duals is available wastes a factor of n. The same applies to LP warm starts and to incremental Dantzig bounds via suffix arrays. Profile bound evaluation: it is usually >90% of runtime, and incrementality there beats any other optimization.

**The AP bound stalls on symmetric instances.** Symmetric cost matrices make 2-cycles nearly free, so the AP bound flatlines far below the tour cost and the tree degenerates. Detect symmetry up front and switch to the 1-tree bound, or hand the instance to a MIP with subtour cuts (see traveling-salesman-problem).

**No pruning happens for a long time.** Without an incumbent, every node survives the bound test. Always seed the search with a construction heuristic, even a crude one — the first 5% of solution quality buys the first 95% of pruning.

**Node counts are not reproducible across runs.** Heap ties broken by object identity or hash order make experiments unrepeatable. Use an explicit insertion counter in the heap key, fix all instance-generation seeds, and report nodes explored and pruned alongside runtimes.

**The custom B&B loses to gurobipy and it is unclear why.** Compare like with like: same time limit, same machine, solver presolve on. If the solver wins, check whether your advantage hypothesis (cheaper bound, dominance, exponential formulation) actually holds; if none does, keep the MIP and spend your effort on formulation tightening instead — see integer-programming-techniques.

## Tools & Libraries

| Library / module | When to use | Note |
|---|---|---|
| `heapq` (stdlib) | Best-first open list | Min-heap; add an insertion counter for deterministic ties |
| `dataclasses` (stdlib) | Node and result records | Keep nodes immutable; mutation bugs in shared state are the classic B&B defect |
| `numpy` | Cost matrices, bound vectorization | Suffix sums for O(1) amortized bounds; matrix copies per node are O(n^2) |
| `scipy.optimize.linear_sum_assignment` | AP relaxation bound | Jonker-Volgenant implementation; re-solves from scratch (no warm start) |
| `gurobipy` | Baseline MIP and correctness cross-checks | Build the MIP first; it is the bar your custom B&B must beat |
| `networkx` | 1-tree bounds (minimum spanning trees), graph utilities | Convenient but slow; replace with numpy MST for inner loops |
| `pandas` | Node-count and runtime experiment tables | One row per (instance, seed, configuration) run |

## Output Format

A complete custom-B&B deliverable contains, in order:

1. **Problem and relaxation statement.** The exact optimization problem, the relaxation used for bounding, and a short validity argument for the bound and for branching completeness (children cover the parent).
2. **Design summary table.** One row per component:

| Component | Choice | Rationale |
|---|---|---|
| Bound | Dantzig LP bound, O(n) per node | Root gap 2.1% on target instances |
| Branching | Fix break item to 1 / 0 | Most constrained decision |
| Node selection | Best-first, insertion-counter ties | Memory fits; minimal proven tree |
| Dominance | Per-level (weight, value) Pareto filter | Same remaining decisions per level |
| Incumbent | Greedy-by-density at root, update at every node | Pruning active from node 1 |

3. **Search report per instance.** Root bound, initial incumbent, final value, proof status (optimal / gap at time limit), nodes explored, nodes pruned (by bound vs by dominance), runtime, and the incumbent-update trace (value, time, node count).
4. **Validation evidence.** Agreement with an independent exact baseline (MIP or DP) on all small instances, stated explicitly with the instance seeds.
5. **Code artifacts.** The engine, the problem-specific callbacks, the instance generator with seeds, and the experiment script that regenerates every reported number.

## Questions to Ask

- Is the problem a minimization or maximization, and are the objective coefficients integral?
- How large are the instances now, and how large must they get for the project to succeed?
- Do you need proven optimality, a certified gap, or the best solution within a time budget?
- What relaxation can you solve quickly, and what is its gap at the root on a typical instance?
- Do you have a Gurobi (or other MIP solver) license, and has the straightforward MIP been tried as a baseline?
- What are the memory and per-instance time limits?
- Is there a fast construction heuristic to seed the incumbent?
- Will this tree later need to host column generation or custom cutting planes?
- Do partial solutions admit componentwise comparison (potential dominance rules)?

## Related Skills

- **integer-programming-techniques** — when the question is about branch-and-bound *inside* a MIP solver: MIP gaps, branching priorities, formulation tightening, and solver parameters instead of a hand-built tree.
- **dynamic-programming** — when the bound or the whole subproblem is DP-solvable (Held-Karp, labeling algorithms); exhaustive dominance turns B&B into DP, and DP often wins at small state spaces.
- **knapsack-problems** — for the full knapsack family (bounded, multiple, multidimensional, quadratic) beyond the 0-1 B&B worked here, including DP and MIP alternatives.
- **traveling-salesman-problem** — for TSP formulations (MTZ, DFJ with lazy cuts), construction heuristics, and local search that complement the assignment-relaxation B&B shown here.
- **column-generation** — when the master problem has exponentially many variables; branch-and-price is this skill's tree search with branching rules kept compatible with the pricing oracle.
