---
name: dynamic-programming
description: When the user wants to design and implement dynamic programming for combinatorial optimization — state-space design, Bellman recursions, memoization vs tabulation, solution recovery, and labeling algorithms for resource-constrained shortest paths. Also use when the user mentions "dynamic programming," "Bellman recursion," "state space," "Held-Karp," "labeling algorithm," "memoization," or when the problem decomposes into stages with overlapping subproblems. For pricing loops that call a DP oracle, see column-generation; for tree search driven by DP bounds, see branch-and-bound.
---

# Dynamic Programming

You are an expert in exact combinatorial optimization, specifically in designing and implementing dynamic programming (DP) algorithms. This skill covers the full design loop — choosing a state space, writing the Bellman recursion, deciding between memoization and tabulation, recovering the optimal solution, and controlling the curse of dimensionality — plus labeling algorithms for resource-constrained shortest paths, the DP family that powers column-generation pricing. Use the framework below to assess whether the problem decomposes, design the state deliberately, implement against the patterns given, and validate against brute force on tiny instances.

## Initial Assessment

Before writing any code, establish the following. Each answer changes a design decision downstream.

- **Optimal substructure.** Can an optimal solution be assembled from optimal solutions of subproblems? If swapping in a better sub-solution can break feasibility or optimality of the whole, DP does not apply directly and the state must be enriched until it does.
- **Overlapping subproblems.** Count distinct subproblems vs total recursive calls. If every call produces a fresh subproblem (no overlap), plain recursion or branch-and-bound is the right tool; DP buys nothing.
- **State-space size, numerically.** Multiply out the state dimensions for the target instance size before coding. `n=100` items × `W=10^9` capacity is 10^11 states — dead on arrival; the same knapsack with `W=10^4` is trivial. This single estimate decides feasibility.
- **Integer or discretizable data.** Pseudo-polynomial DPs (knapsack-style) need integer resource values. If weights/durations are floats, ask what scaling factor is acceptable and what error bound the user needs.
- **Value only, or solution too.** Recovering the optimal solution costs either full-table memory (parent pointers) or extra recomputation (divide-and-conquer recovery). A bound inside branch-and-bound often needs only the value.
- **Standalone or subroutine.** A DP called once can afford O(n²) time. A pricing DP called thousands of times inside column generation, or a bound called millions of times inside branch-and-bound, must be lean and warm-startable.
- **Acyclic structure.** Is there a natural stage ordering (items, periods, nodes of a DAG)? Cyclic state graphs need label-correcting/label-setting treatment or a resource that strictly increases along every transition to guarantee termination.
- **Memory budget.** A 2D table of 10^8 `float64` entries is 800 MB. Decide early whether rolling arrays (value only) suffice or whether full recovery is required.
- **Exactness requirement.** If the exact state space is too large, is an approximation acceptable? Profit-scaling FPTAS for knapsack (Ibarra & Kim 1975), state-space relaxation for routing, or coarser time discretization all trade accuracy for size — but change what you can claim about the answer.
- **One run or a family of runs.** If the user will re-solve with slightly different data (duals changing each pricing iteration, capacities varying), structure the code so the instance-independent parts (graph construction, sorting) are reused.
- **Python performance ceiling.** Pure-Python nested loops handle ~10^6–10^7 state transitions per second; numpy-vectorized inner loops reach 10^8–10^9. Estimate transition count and pick the implementation style accordingly.
- **Validation oracle.** What independent check exists? Brute-force enumeration up to n≈15–20, a MIP model of the same problem, or known optima from a benchmark library. Plan the cross-check before trusting any DP.

## Algorithm Anatomy

Dynamic programming (Bellman 1957, *Dynamic Programming*) solves a problem by ordering decisions into stages and exploiting the **principle of optimality**: an optimal policy has the property that, whatever the initial state and first decision, the remaining decisions form an optimal policy for the state that results from the first decision. Formally, with states $s$, actions $A(s)$, transition $\tau(s,a)$, and stage cost $c(s,a)$, the value function satisfies the Bellman recursion

$$
V(s) \;=\; \min_{a \in A(s)} \Big\{\, c(s,a) + V\big(\tau(s,a)\big) \,\Big\},
\qquad V(s) = v_T(s) \ \text{ for terminal } s ,
$$

and the optimal solution is recovered by following the argmin actions from the initial state. Maximization flips min to max; nothing else changes.

### The five design decisions

| Component | Question it answers | Failure mode if wrong |
|---|---|---|
| State | What is the minimal information that makes the future independent of the past? | Missing information → wrong answers; extra information → exponential blowup |
| Stages / transitions | In what order are decisions made, and what states do they lead to? | Cycles in the state graph → non-terminating recursion |
| Recursion | How does $V(s)$ combine stage cost and successor values? | Double-counted or dropped costs |
| Base cases | What are the terminal states and their values? | Off-by-one stage errors, infeasible states valued 0 instead of $+\infty$ |
| Recovery | How is the optimal solution rebuilt from the table? | Value correct, reported solution inconsistent with it |

**State design discipline.** The state is correct exactly when two different decision histories that reach the same state always have the same set of optimal completions. Test it on paper: construct two histories mapping to one state and ask whether any future constraint or cost can tell them apart. If yes, the distinguishing quantity belongs in the state. This is the Markov property of the decomposition, and forgetting it is the most common DP bug — for example, a knapsack state of "items considered" without "capacity used", or a shortest-path label without the time-window resource.

### Memoization vs tabulation

| Aspect | Memoization (top-down) | Tabulation (bottom-up) |
|---|---|---|
| States touched | Only those reachable from the initial state | Every state in a fixed enumeration order |
| Implementation | Recursion + cache (`dict`, `functools.lru_cache`) | Nested loops over the table |
| Python performance | Function-call overhead; recursion limit (default 1000 frames) | Fast loops; inner dimension vectorizable with numpy |
| Memory control | Hard — the cache keeps everything | Easy — rolling arrays keep only the rows the recursion reads |
| Best when | Reachable states are sparse or transitions irregular | The state space is dense and rectangular |

Rule of thumb in Python: prototype top-down to get the recursion right, then convert to bottom-up tabulation with a numpy-vectorized inner dimension for production use. The worked knapsack example below shows the same recursion in both styles.

### Complexity landscape

| DP | State | Time | Memory | Note |
|---|---|---|---|---|
| 0-1 knapsack | (items considered, capacity used) | O(nW) | O(W) value-only | Pseudo-polynomial: W is a magnitude, not an input length |
| Wagner-Whitin lot sizing | (first uncovered period) | O(T²), improvable to O(T log T) | O(T) | Wagelmans, van Hoesel & Kolen (1992) |
| Held-Karp TSP | (visited subset, last city) | O(n²·2ⁿ) | O(n·2ⁿ) | Exact to n ≈ 20–23 in Python/numpy |
| SPPRC labeling | (node, resource vector) | Output-sensitive | Dominance-dependent | Column-generation pricing workhorse (Irnich & Desaulniers 2005) |
| DAG shortest path | node | O(V+E) | O(V) | Every finite acyclic DP is a shortest path on its state graph |

**Curse of dimensionality.** State spaces grow multiplicatively in the number of state dimensions: a vector of d resources each with R levels gives Rᵈ states per node. Remedies, in order of preference: (1) drop a dimension by proving the recursion never needs it; (2) relax the state space (project to fewer dimensions, accept a bound instead of the exact value — see Advanced Techniques); (3) coarsen discretization with a quantified error bound; (4) abandon exactness for approximate DP (Powell 2011, *Approximate Dynamic Programming*) or a metaheuristic.

### When to use DP — and when not

- **Use DP standalone** when the state-space estimate is comfortably within memory/time (≤ ~10⁸ transitions in numpy), data is integer or cleanly discretizable, and a proof of optimality is wanted. For knapsack with moderate W, uncapacitated lot sizing, sequence alignment, and small-subset problems, DP beats MIP solvers outright.
- **Use DP as a subroutine** when an outer method needs it: labeling DPs as pricing oracles in column generation, DP over relaxed states as bounding functions in branch-and-bound, DP decoders inside metaheuristics (optimal split of a giant tour, optimal timing for a fixed sequence).
- **Prefer a MIP** when constraints couple decisions in ways that explode the state (many global side constraints), when data is fractional and scaling is unacceptable, or when the model will keep gaining new constraint types — a MIP absorbs a new constraint in one line; a DP may need a new state dimension.
- **Prefer branch-and-bound** when subproblems barely overlap but good bounds and dominance rules exist; B&B with a DP-based bound is often the best of both (see branch-and-bound).

## Generic DP Engine

The skeleton every finite DP follows, independent of problem:

```text
SOLVE-DP(initial state s0):
  define VALUE(s):
    if s in memo:            return memo[s]
    if s is terminal:        memo[s] = terminal_value(s); return it
    best = +inf  (minimization)
    for each action a in A(s):
      v = c(s, a) + VALUE(tau(s, a))
      if v < best: best = v; best_action[s] = a
    memo[s] = best
    return best

  opt = VALUE(s0)
  # recovery: walk the argmin policy from s0
  s = s0; plan = []
  while s not terminal:
    a = best_action[s]; plan.append(a); s = tau(s, a)
  return opt, plan
```

A direct, reusable implementation. It is deliberately generic — use it to prototype a recursion and to cross-check specialized tabulations; rewrite hot DPs as bottom-up numpy code afterwards.

```python
from __future__ import annotations

import math
from collections.abc import Callable, Hashable, Iterable
from typing import Any

State = Hashable
Action = Any


def solve_dp(
    initial: State,
    is_terminal: Callable[[State], bool],
    terminal_value: Callable[[State], float],
    actions: Callable[[State], Iterable[Action]],
    transition: Callable[[State, Action], State],
    cost: Callable[[State, Action], float],
    sense: str = "min",
) -> tuple[float, list[Action]]:
    """Memoized Bellman recursion over a finite acyclic state graph.

    Returns (optimal value, optimal action sequence from `initial`).
    Requires: every state reaches a terminal state; the state graph is acyclic;
    recursion depth (longest state chain) stays below Python's recursion limit.
    """
    memo: dict[State, tuple[float, Any]] = {}

    def value(s: State) -> float:
        if s in memo:
            return memo[s][0]
        if is_terminal(s):
            memo[s] = (terminal_value(s), None)
            return memo[s][0]
        best_v = math.inf if sense == "min" else -math.inf
        best_a: Any = None
        for a in actions(s):
            v = cost(s, a) + value(transition(s, a))
            if (sense == "min" and v < best_v) or (sense == "max" and v > best_v):
                best_v, best_a = v, a
        memo[s] = (best_v, best_a)
        return best_v

    opt = value(initial)
    plan: list[Action] = []
    s = initial
    while not is_terminal(s):
        a = memo[s][1]
        plan.append(a)
        s = transition(s, a)
    return opt, plan


# Tiny demo: shortest path on a 4-node DAG, arcs[u] = [(successor, cost), ...]
arcs: dict[int, list[tuple[int, float]]] = {
    0: [(1, 2.0), (2, 5.0)],
    1: [(3, 4.0)],
    2: [(3, 2.0)],
}
val, plan = solve_dp(
    initial=0,
    is_terminal=lambda s: s == 3,
    terminal_value=lambda s: 0.0,
    actions=lambda s: [v for v, _ in arcs.get(s, [])],
    transition=lambda s, a: a,
    cost=lambda s, a: dict(arcs[s])[a],
)
print(val, plan)
# Expected: 6.0 [1, 3]  -- path 0 -> 1 -> 3 costs 2 + 4 = 6, beating 0 -> 2 -> 3 = 7
```

Every finite DP is a shortest (or longest) path on its state graph; if the engine above gives a different answer than your specialized tabulation on small instances, the tabulation has a bug, not the recursion.

## Worked Example 1: 0-1 Knapsack

The decomposition. Items $1,\dots,n$ with profits $p_i$ and integer weights $w_i$, capacity $W$. Define $V(i,w)$ as the best profit achievable using a subset of the first $i$ items with total weight at most $w$ — the state $(i, w)$ records exactly what the remaining items need to know about the past:

$$
V(i, w) \;=\; \max\Big\{\, \underbrace{V(i-1,\, w)}_{\text{skip item } i},\;\; \underbrace{V(i-1,\, w - w_i) + p_i}_{\text{take item } i,\ \text{only if } w_i \le w} \,\Big\},
\qquad V(0, w) = 0 .
$$

The state is two-dimensional and dense, so bottom-up tabulation with a numpy-vectorized capacity axis is the production implementation. Time O(nW), pseudo-polynomial — see Kellerer, Pferschy & Pisinger (2004), *Knapsack Problems*, for the full algorithmic landscape.

```python
import numpy as np


def knapsack_dp(profits: np.ndarray, weights: np.ndarray, capacity: int) -> tuple[int, list[int]]:
    """0-1 knapsack by bottom-up tabulation; full table kept for solution recovery.

    profits, weights: integer arrays of length n. Time O(nW), memory O(nW).
    Returns (optimal profit, sorted list of chosen item indices).
    """
    n = len(profits)
    V = np.zeros((n + 1, capacity + 1), dtype=np.int64)
    for i in range(1, n + 1):
        w_i, p_i = int(weights[i - 1]), int(profits[i - 1])
        V[i] = V[i - 1]  # default: skip item i (row assignment copies values)
        if w_i <= capacity:
            take = V[i - 1, : capacity - w_i + 1] + p_i  # vectorized over capacity
            V[i, w_i:] = np.maximum(V[i - 1, w_i:], take)
    # Recovery: walk the table backwards; a row change means item i was taken.
    chosen: list[int] = []
    w = capacity
    for i in range(n, 0, -1):
        if V[i, w] != V[i - 1, w]:
            chosen.append(i - 1)
            w -= int(weights[i - 1])
    chosen.reverse()
    return int(V[n, capacity]), chosen


profits = np.array([60, 100, 120])
weights = np.array([10, 20, 30])
value, items = knapsack_dp(profits, weights, capacity=50)
print(value, items)
# Expected: 220 [1, 2]  -- items 1 and 2: weight 20 + 30 = 50, profit 100 + 120 = 220
```

The same recursion top-down, for contrast. Memoization touches only reachable `(i, w)` pairs — a real saving when capacities cluster — but pays Python call overhead and recursion depth equal to n:

```python
import sys
from functools import lru_cache


def knapsack_topdown(profits: list[int], weights: list[int], capacity: int) -> int:
    """Top-down memoized 0-1 knapsack (value only).

    Explores only reachable (i, w) states; recursion depth equals len(profits).
    """
    sys.setrecursionlimit(max(10_000, len(profits) + 100))

    @lru_cache(maxsize=None)
    def best(i: int, w: int) -> int:
        if i == 0:
            return 0
        skip = best(i - 1, w)
        if weights[i - 1] <= w:
            return max(skip, best(i - 1, w - weights[i - 1]) + profits[i - 1])
        return skip

    return best(len(profits), capacity)


print(knapsack_topdown([60, 100, 120], [10, 20, 30], 50))
# Expected: 220
```

When only the value is needed — typically when the DP serves as a bound inside branch-and-bound or as a pricing oracle — collapse the table to one rolling row. The numpy right-hand side is evaluated fully before assignment, so a single ascending-index statement still implements the 0-1 (not the unbounded) recursion:

```python
import numpy as np


def knapsack_value_only(profits: np.ndarray, weights: np.ndarray, capacity: int) -> int:
    """0-1 knapsack optimal value in O(W) memory with one rolling array.

    Correctness note: `dp[: capacity - w + 1] + p` is materialized before the
    assignment to dp[w:], so every item is used at most once.
    """
    dp = np.zeros(capacity + 1, dtype=np.int64)
    for p, w in zip(profits.tolist(), weights.tolist()):
        if w <= capacity:
            dp[w:] = np.maximum(dp[w:], dp[: capacity - w + 1] + p)
    return int(dp[capacity])


print(knapsack_value_only(np.array([60, 100, 120]), np.array([10, 20, 30]), 50))
# Expected: 220
```

If both O(W) memory **and** the chosen item set are required, use divide-and-conquer recovery (Hirschberg 1975 style): solve forward over items 1..n/2 and backward over n/2+1..n, find the capacity split that attains the optimum, and recurse on each half — O(nW) time total, O(W) memory.

## Worked Example 2: Wagner-Whitin Lot Sizing

The decomposition. Periods $1,\dots,T$ with demands $d_t \ge 0$, setup cost $K_s$ when producing in period $s$, and unit holding cost $h_t$ for inventory carried from $t$ to $t+1$. Production capacity is unlimited. Wagner & Whitin (1958, "Dynamic version of the economic lot size model") proved the **zero-inventory-ordering (ZIO) property**: some optimal plan produces only when inventory is zero, so each setup in period $s$ covers a consecutive block of demands $d_s, \dots, d_t$. Let

$$
c(s,t) \;=\; K_s + \sum_{u=s}^{t} \Big( \sum_{v=s}^{u-1} h_v \Big) d_u
$$

be the cost of one setup in $s$ covering periods $s..t$. With $F(t)$ the optimal cost of satisfying demands $1..t$:

$$
F(t) \;=\; \min_{1 \le s \le t} \big\{ F(s-1) + c(s, t) \big\}, \qquad F(0) = 0 .
$$

The state is a single index (first uncovered period), so the DP is O(T²) with the batch-cost matrix built incrementally. An O(T log T) algorithm exists via the monotonicity of optimal break points (Wagelmans, van Hoesel & Kolen 1992; Federgruen & Tzur 1991), but for the T ≤ a few thousand typical of planning models, O(T²) numpy code is simpler and fast enough.

```python
import numpy as np


def wagner_whitin(
    demand: np.ndarray, setup: np.ndarray, holding: np.ndarray
) -> tuple[float, list[tuple[int, int]]]:
    """Uncapacitated lot sizing by the Wagner-Whitin forward recursion.

    demand[t]: demand of period t; setup[s]: setup cost if producing in s;
    holding[t]: unit cost of carrying inventory from period t to t+1.
    Returns (optimal cost, production plan) where the plan lists
    (production period, last period covered), all 0-indexed.
    Time O(T^2), memory O(T^2) for the batch-cost matrix.
    """
    T = len(demand)
    c = np.full((T, T), np.inf)  # c[s, t] = setup in s covering demand[s..t]
    for s in range(T):
        c[s, s] = float(setup[s])
        cum_h = 0.0
        for t in range(s + 1, T):
            cum_h += float(holding[t - 1])  # sum of holding[s..t-1]
            c[s, t] = c[s, t - 1] + cum_h * float(demand[t])
    F = np.full(T + 1, np.inf)
    F[0] = 0.0
    pred = np.zeros(T + 1, dtype=np.int64)
    for t in range(1, T + 1):
        cands = F[:t] + c[np.arange(t), t - 1]  # vectorized over setup period s
        s = int(np.argmin(cands))
        F[t], pred[t] = float(cands[s]), s
    plan: list[tuple[int, int]] = []
    t = T
    while t > 0:
        s = int(pred[t])
        plan.append((s, t - 1))
        t = s
    plan.reverse()
    return float(F[T]), plan


demand = np.array([20, 50, 10, 50])
setup = np.array([100, 100, 100, 100])
holding = np.array([1.0, 1.0, 1.0, 1.0])
cost, plan = wagner_whitin(demand, setup, holding)
print(cost, plan)
# Expected: 270.0 [(0, 2), (3, 3)] -- produce 80 units in period 0 (covers periods
# 0-2: setup 100 + holding 1*50 + 2*10 = 170) and 50 units in period 3 (setup 100)
```

Two practical notes. First, validate against the ZIO property: in the recovered plan, every production period must coincide with zero entering inventory — an independent feasibility check that catches indexing bugs. Second, the **planning-horizon theorem** (Wagner & Whitin 1958) says that if the optimal $F(t)$ chooses a setup in period $s$, no later period's optimal plan ever needs a setup before $s$; this is what the O(T log T) algorithms exploit, and it also enables rolling-horizon re-solving without recomputing the past. Once capacities enter, the DP state would need the inventory level and the problem becomes NP-hard — switch to the MIP and valid-inequality machinery in lot-sizing.

## Labeling Algorithms for Constrained Shortest Paths

The shortest path problem with resource constraints (SPPRC) asks for a minimum-cost source-sink path where each arc also consumes resources (time, load, fuel) and resource accumulation must respect limits. It is *the* pricing subproblem of vehicle routing and crew scheduling column generation (Irnich & Desaulniers 2005, "Shortest path problems with resource constraints"), where arc costs are **reduced costs** built from the master problem's duals — and are therefore often negative, which kills Dijkstra but not DP.

A **label** is the DP state attached to a node: $L = (\text{node}, \text{cost}, r_1, \dots, r_k)$ representing one feasible partial path. Extending $L$ along arc $(u,v)$ applies resource extension functions, in the simplest additive case

$$
\text{cost}' = \text{cost} + c_{uv}, \qquad r' = r + r_{uv}, \qquad \text{feasible iff } r' \le R .
$$

Because multiple Pareto-incomparable (cost, resource) pairs can coexist at one node, the DP keeps a *set* of labels per node, pruned by **dominance**: $L_1$ dominates $L_2$ at the same node if $\text{cost}_1 \le \text{cost}_2$ and $r_1 \le r_2$ componentwise — every feasible extension of $L_2$ is then matched or beaten by the same extension of $L_1$. Dominance is what keeps label counts manageable; without it the label set grows exponentially.

Termination with negative costs requires that no negative-cost cycle be traversable forever. The standard device — used below — is to require every arc to consume a strictly positive amount of some bounded resource, which is exactly the relaxation (non-elementary paths, "q-routes") used in classic VRP pricing. Forbidding repeated customers exactly (the *elementary* SPPRC) adds a visited-set to the label (Feillet, Dejax, Gendreau & Gueguen 2004) at significant cost; see Advanced Techniques for the modern middle ground.

```python
from __future__ import annotations

import heapq
from collections import defaultdict
from dataclasses import dataclass, field


@dataclass(order=True)
class Label:
    """A partial path: cumulative cost (heap key) and resource, with parent link."""
    cost: float
    resource: float = field(compare=False)
    node: int = field(compare=False)
    pred: "Label | None" = field(compare=False, default=None)


def shortest_path_with_resource(
    arcs: dict[int, list[tuple[int, float, float]]],
    source: int,
    sink: int,
    resource_limit: float,
) -> tuple[float, list[int]] | None:
    """Labeling algorithm for the one-resource SPPRC.

    arcs[u] = [(v, cost, resource), ...]. Costs may be negative; every arc must
    consume resource > 0 so path length is bounded and the algorithm terminates
    (the standard non-elementary relaxation used in column-generation pricing).
    Returns (cost, node path) of the best resource-feasible path, or None.
    """
    start = Label(0.0, 0.0, source)
    open_heap: list[Label] = [start]
    labels: dict[int, list[Label]] = defaultdict(list)
    labels[source].append(start)
    best: Label | None = None
    while open_heap:
        lab = heapq.heappop(open_heap)
        # Lazy deletion: skip labels dominated after they entered the heap.
        if all(existing is not lab for existing in labels[lab.node]):
            continue
        for v, c, r in arcs.get(lab.node, []):
            new = Label(lab.cost + c, lab.resource + r, v, lab)
            if new.resource > resource_limit:
                continue
            if any(
                ex.cost <= new.cost and ex.resource <= new.resource
                for ex in labels[v]
            ):
                continue  # new label is dominated
            labels[v] = [
                ex
                for ex in labels[v]
                if not (new.cost <= ex.cost and new.resource <= ex.resource)
            ]
            labels[v].append(new)
            if v == sink and (best is None or new.cost < best.cost):
                best = new
            heapq.heappush(open_heap, new)
    if best is None:
        return None
    path: list[int] = []
    cur: Label | None = best
    while cur is not None:
        path.append(cur.node)
        cur = cur.pred
    path.reverse()
    return best.cost, path


# Demo: negative-cost arcs (reduced costs), resource limit makes the cheap path infeasible.
arcs = {
    0: [(1, -6.0, 3.0), (2, 1.0, 1.0)],
    1: [(3, 2.0, 2.0)],
    2: [(3, -4.0, 1.0)],
}
print(shortest_path_with_resource(arcs, source=0, sink=3, resource_limit=4.0))
# Expected: (-3.0, [0, 2, 3]) -- path 0-1-3 is cheaper (-4.0) but needs resource 5 > 4,
# so dominance-pruned labeling returns the best resource-feasible path
```

Engineering notes that matter at pricing scale: keep each node's labels sorted by cost so dominance checks can stop early; bucket labels by discretized resource consumption to process them in increasing-resource order (then labels are never extended before all potential dominators exist — Desrochers' bucket idea); and expose a "return all negative-cost sink labels" mode, because column generation wants *many* improving columns per pricing call, not just the single best (see column-generation).

## Advanced Techniques

### Held-Karp: exact TSP over subsets

Held & Karp (1962, "A dynamic programming approach to sequencing problems") solve the TSP with state (subset of visited cities, last city). With $C(S, j)$ the cheapest path from city 0 through all of $S \subseteq \{1..n-1\}$ ending at $j \in S$:

$$
C(\{j\}, j) = d_{0j}, \qquad
C(S, j) = \min_{k \in S \setminus \{j\}} \big\{ C(S \setminus \{j\}, k) + d_{kj} \big\}, \qquad
z^* = \min_j \big\{ C(\{1..n-1\}, j) + d_{j0} \big\}.
$$

O(n²·2ⁿ) time and O(n·2ⁿ) memory — still the best known exact complexity for general TSP, and a sharp illustration of the curse of dimensionality: n=20 needs ~0.4 GB for the table; n=30 needs ~0.5 TB. Use it for exact answers up to n≈20, as an optimal decoder for small sub-sequencing problems inside larger heuristics, and as ground truth when testing TSP heuristics (see traveling-salesman-problem for what to do beyond that).

```python
import numpy as np


def held_karp(dist: np.ndarray) -> tuple[float, list[int]]:
    """Exact TSP by Held-Karp subset DP. O(n^2 * 2^n) time, O(n * 2^n) memory.

    dist: (n, n) matrix, n >= 2. Returns (optimal tour length, tour as a city
    list starting at 0; the cycle closes back to city 0).
    """
    n = dist.shape[0]
    m = n - 1                      # cities 1..n-1, bit j <-> city j+1
    full = 1 << m
    C = np.full((full, m), np.inf)
    parent = np.full((full, m), -1, dtype=np.int64)
    for j in range(m):
        C[1 << j, j] = dist[0, j + 1]
    for S in range(1, full):
        if S & (S - 1) == 0:
            continue               # singletons are base cases
        for j in range(m):
            if not (S >> j) & 1:
                continue
            prev = S ^ (1 << j)
            ks = [k for k in range(m) if (prev >> k) & 1]
            cand = C[prev, ks] + dist[np.array(ks) + 1, j + 1]  # vectorized over k
            i = int(np.argmin(cand))
            C[S, j], parent[S, j] = float(cand[i]), ks[i]
    closing = C[full - 1] + dist[1:, 0]
    j = int(np.argmin(closing))
    best = float(closing[j])
    tour_rev: list[int] = []
    S, cur = full - 1, j
    while cur != -1:
        tour_rev.append(cur + 1)
        nxt = int(parent[S, cur])
        S ^= 1 << cur
        cur = nxt
    return best, [0] + tour_rev[::-1]


dist = np.array(
    [[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]], dtype=float
)
length, tour = held_karp(dist)
print(length, tour)
# Expected: 80.0 [0, 2, 3, 1] -- the cycle 0-2-3-1-0 = 15+30+25+10 = 80
# (the reverse orientation 0-1-3-2-0 is the same optimal tour)
```

### State-space relaxation: bounds from projected states

When the exact state is too rich, **project** it onto a smaller space and take the min over all states mapping to the same projection (Christofides, Mingozzi & Toth 1981, "State-space relaxation procedures for the computation of bounds to routing problems"). The relaxed DP runs over the small space and yields a valid **lower bound**, because every feasible solution of the original problem is still represented (possibly alongside infeasible ones). Canonical example: relax Held-Karp's "subset visited" to "number of cities visited" — state (count, last city), O(n³) time — giving the q-route bound used in early VRP exact methods. The **ng-route relaxation** (Baldacci, Mingozzi & Roberti 2011) interpolates: each label remembers visited customers only within a per-customer neighborhood set, tuning the bound-vs-effort trade-off; it is the default in modern branch-cut-and-price. Use relaxed-DP bounds inside branch-and-bound or to prune labels (a label whose cost plus a relaxed completion bound exceeds the incumbent can be discarded).

### Bidirectional labeling

Labeling effort grows roughly exponentially with path length. Righini & Salani (2006, "Symmetry helps: bounded bi-directional dynamic programming for the resource constrained shortest path") extend labels forward from the source and backward from the sink, each only up to half the critical resource, then join compatible forward/backward label pairs at a middle node. The halved extension depth typically cuts label counts by orders of magnitude on VRPTW pricing; it is standard in production branch-and-price codes. Implementation cost: a backward resource-extension function and a join feasibility check per (node, pair).

### DP as a column-generation pricing engine

The cleanest illustration is Gilmore-Gomory cutting stock: the master LP selects cutting patterns; pricing asks for the pattern maximizing total dual value packed into one roll — an **unbounded knapsack** DP. A new column improves the master iff its reduced cost $1 - \sum_i \pi_i a_i$ is negative. The same template scales up: VRP pricing swaps the knapsack for the SPPRC labeling DP above, with duals entering the arc reduced costs.

```python
import numpy as np


def price_cutting_pattern(
    duals: np.ndarray, widths: np.ndarray, roll_width: int
) -> tuple[float, np.ndarray]:
    """Pricing oracle for Gilmore-Gomory cutting stock: unbounded knapsack DP.

    duals[i]: master dual for item i; widths[i]: integer item width.
    Returns (reduced cost of best pattern, pattern as item counts).
    The column improves the restricted master iff reduced cost < 0.
    """
    dp = np.zeros(roll_width + 1)
    choice = np.full(roll_width + 1, -1, dtype=np.int64)
    for w in range(1, roll_width + 1):
        for i, (wi, pi) in enumerate(zip(widths.tolist(), duals.tolist())):
            if wi <= w and dp[w - wi] + pi > dp[w]:
                dp[w], choice[w] = dp[w - wi] + pi, i
    pattern = np.zeros(len(widths), dtype=np.int64)
    w = roll_width
    while w > 0 and choice[w] >= 0:
        pattern[choice[w]] += 1
        w -= int(widths[choice[w]])
    return 1.0 - float(dp[roll_width]), pattern


rc, pattern = price_cutting_pattern(
    duals=np.array([0.4, 0.6]), widths=np.array([3, 5]), roll_width=10
)
print(rc, pattern)
# Expected: reduced cost -0.2 (up to float rounding) and pattern [3 0] -- three
# width-3 pieces pack dual value 1.2; 1 - 1.2 = -0.2 < 0, so the column enters the master
```

Pricing-loop hygiene: the DP is called once per master iteration with fresh duals, so precompute everything dual-independent (sorted widths, graph topology) outside the call, and return several near-best columns per call to cut master iterations (see column-generation for the surrounding loop and stabilization).

### Memory reduction and solution recovery

Three standard devices, in increasing sophistication. (1) **Rolling arrays**: when stage $i$ reads only stage $i-1$, keep one or two rows — value only, O(state-per-stage) memory. (2) **Checkpointing**: store every k-th table row; recover the solution by re-running the DP between consecutive checkpoints — k× less memory for ~2× time. (3) **Divide-and-conquer recovery** (Hirschberg 1975): meet-in-the-middle on stages, find where the optimum crosses the midline, recurse on both halves — full solution in O(state-per-stage) memory at ~2× time. Pick (1) for bounds, (3) when both memory and the full solution matter.

## Practical Challenges

**The state space explodes at realistic instance sizes.** First try to prove a dimension redundant (dominance between states differing only in that dimension). Then relax: project the state (state-space relaxation), coarsen resource discretization with an explicit error bound, or cap label sets per node keeping the k cheapest (a heuristic DP — report it as such). If the exact answer is mandatory, move to branch-and-bound with the relaxed DP as the bounding function rather than forcing the full DP through.

**Top-down recursion hits Python's recursion limit or is too slow.** The recursion limit (default 1000) breaks on chains longer than ~1000 stages; `sys.setrecursionlimit` is a band-aid that risks interpreter stack overflow. Convert to bottom-up tabulation in stage order — every acyclic DP admits one — and vectorize the innermost state dimension with numpy. Expect one to two orders of magnitude speedup over memoized recursion in CPython.

**Weights or durations are fractional, breaking pseudo-polynomial DPs.** Scale by 10^k and round, then bound the error: rounding weights changes feasibility (be conservative — round consumption up), rounding profits changes only the objective by at most n·(scale unit). The knapsack FPTAS (Ibarra & Kim 1975) formalizes profit scaling: an ε-optimal answer with table size O(n²/ε). State clearly which quantity was rounded and in which direction.

**The labeling DP does not terminate or returns absurd negative costs.** Symptom of a traversable negative-cost cycle. Verify every arc consumes a strictly positive amount of a bounded resource; if the model has genuine zero-consumption arcs (e.g., waiting), break ties with a hop-count resource. For elementary-path requirements, add ng-neighborhood memory rather than the full visited set first — full elementarity (Feillet et al. 2004) is often 10-100× slower and rarely needed early in a pricing loop.

**The DP value is right but the recovered solution is wrong or infeasible.** Classic causes: parent pointers read after the table row was overwritten (rolling array + recovery do not mix), argmin recomputed with a different tie-break than the forward pass, or off-by-one in the walk-back. Fix structurally: recover by re-checking `V[i][w] != V[i-1][w]`-style identities against the stored table, and always run an independent feasibility check plus objective recomputation on the recovered solution.

**Two histories reach the same state but have different futures (hidden state).** The answer is silently wrong, usually optimistic. Detect it by brute-force cross-validation: enumerate all solutions for n ≤ 12-15 instances across random seeds and compare. Any mismatch means the state lacks information — enlarge it (add the forgotten resource) rather than patching the transition.

**Dominance is too weak and label counts blow up.** Strengthen it with completion bounds: precompute a lower bound on cost-to-sink per (node, resource bucket) by a backward unconstrained DP; discard any label whose cost plus completion bound cannot beat the best known sink label. This "bounded labeling" often reduces labels by orders of magnitude and is the labeling counterpart of branch-and-bound pruning.

**The DP is re-solved thousands of times with slightly changed data and dominates runtime.** Inside column generation or a rolling horizon, hoist all data-independent work out of the call (graph arrays, sort orders, bucket structures), reuse allocated numpy buffers, and consider warm-starting label sets from the previous duals. Profile first: the bottleneck is usually dominance checking, not extension — sorting labels by cost makes most dominance checks O(1) early exits.

## Tools & Libraries

| Library / tool | When to use | Note |
|---|---|---|
| numpy | Bottom-up tabulation with a vectorizable state axis | The default for production DPs; broadcasting over the capacity/resource axis |
| functools.lru_cache | Top-down prototypes, sparse reachable state spaces | Zero-boilerplate memoization; watch recursion depth and unbounded cache growth |
| numba | Pure-Python DP loops that resist vectorization (labeling, irregular transitions) | `@njit` on the inner loop often gives 50-200×; keep data in typed arrays |
| networkx | DAG shortest/longest path, topological order, small graph DPs | `dag_longest_path`, `shortest_path` on the state graph; convenience over speed |
| scipy.sparse.csgraph | Large shortest-path computations (Dijkstra, Bellman-Ford) feeding a DP | C-speed on CSR matrices; no resource constraints |
| OR-Tools (CP-SAT / KnapsackSolver) | Cross-checking DP answers; knapsacks with many side constraints | `KnapsackSolver` is a tuned B&B/DP hybrid; CP-SAT validates small instances |
| cspy | Resource-constrained shortest paths without writing your own labeling | Implements (bi)directional labeling; useful baseline before customizing |
| pandas | Result and experiment tables only | One row per (instance, method, seed); never inside the DP itself |

## Output Format

A complete DP deliverable contains, in order:

1. **Recursion statement.** State definition in one sentence ("$V(i,w)$ = best profit using items $1..i$ with capacity $w$"), the Bellman equation in display math, base cases, and where the answer is read off. No code before this exists.
2. **Size and complexity estimate.** State-space cardinality and transition count for the user's target instance, time/memory in O-notation *and* in concrete numbers (entries × bytes). State explicitly whether the algorithm is polynomial, pseudo-polynomial, or exponential.
3. **Implementation.** Tabulation (or labeling) code with type hints, solution recovery, and a fixed-seed synthetic instance demonstrating it, ending in an `# Expected:` line.
4. **Validation evidence.** Brute-force or MIP cross-check on small instances (n ≤ 15, multiple seeds), plus an independent feasibility check and objective recomputation of the recovered solution.
5. **Run report.** One table per experiment:

| Field | Example |
|---|---|
| Instance | knapsack n=500, W=10^5, seed 42 |
| Method | bottom-up numpy tabulation, O(W) rolling + D&C recovery |
| States / labels generated | 5.0 × 10^7 |
| Wall time | 0.84 s |
| Optimal value | 27 343 |
| Optimality status | exact (DP, validated vs CP-SAT on n ≤ 15) |
| Peak memory | 0.8 MB (rolling array) |

6. **Scope statement.** What was relaxed or rounded (if anything), the resulting guarantee (exact / lower bound / ε-optimal), and the instance size at which this approach stops being viable, with the recommended escalation path (relaxation, branch-and-bound hybrid, or metaheuristic).

## Questions to Ask

- What are the realistic instance dimensions — and the largest you will ever need to solve?
- Are the resource quantities (weights, capacities, durations) integers, or floats that must be scaled?
- Do you need the optimal solution itself, or only its value (e.g., as a bound)?
- Is this DP solved once, or repeatedly inside a loop (pricing, rolling horizon, B&B nodes)?
- What memory is available, and is a 2× time penalty acceptable to cut memory by orders of magnitude?
- If the exact state space is too large, is a provable bound or an ε-guarantee acceptable instead?
- Is there a natural stage order, or does the state graph contain cycles (waiting, revisits)?
- What can serve as the validation oracle — brute force, a MIP model, or known benchmark optima?
- For path problems: which resources constrain the path, and must paths be elementary (no repeated nodes)?

## Related Skills

- **knapsack-problems** — when the user needs the full knapsack family (bounded, multiple, multidimensional, quadratic) and the B&B/MIP/greedy alternatives beyond the 0-1 DP shown here.
- **lot-sizing** — when Wagner-Whitin meets capacities: CLSP MIP models, (l,S) valid inequalities, and fix-and-optimize heuristics.
- **traveling-salesman-problem** — when n exceeds Held-Karp's reach and MIP formulations with subtour cuts or local search take over.
- **column-generation** — when the labeling or knapsack DP built here becomes the pricing oracle inside a restricted-master loop or branch-and-price.
- **branch-and-bound** — when the state space explodes and DP-based bounds plus dominance rules should drive a tree search instead of a full table.
