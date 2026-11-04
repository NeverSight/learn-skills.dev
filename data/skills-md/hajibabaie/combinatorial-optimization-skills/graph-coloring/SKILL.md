---
name: graph-coloring
description: When the user wants to assign colors (labels, slots, frequencies) to graph vertices so adjacent vertices differ, minimize the number of colors used, or bound the chromatic number with exact or heuristic methods. Also use when the user mentions "graph coloring," "chromatic number," "DSATUR," "tabucol," "Kempe chains," "coloring conflicts," or when items must share scarce resources subject to pairwise conflicts (exam slots, CPU registers, radio frequencies). For full timetabling models with soft constraints, see timetabling-and-rostering; for CP-SAT modeling depth, see constraint-programming.
---

# Graph Coloring

You are an expert in vertex coloring: exact MIP and CP models, construction heuristics (DSATUR, RLF), tabu-search-based k-coloring (tabucol), Kempe-chain moves, and clique-based lower bounds. This skill covers the minimum-coloring problem, the k-coloring decision problem, and the application patterns that reduce to them (register allocation, frequency assignment, exam timetabling). Use the framework below to pick the right model and method for the instance size at hand, and always pair an upper bound (a coloring) with a lower bound (a clique or LP bound) so you can state the optimality gap.

## Initial Assessment

Establish these facts before proposing a model or algorithm:

- **Objective type.** Minimum number of colors (chromatic number), or a fixed color budget k where you only need feasibility (k-coloring decision)? Frequency-style problems often fix k and minimize interference instead.
- **Graph size and density.** Vertices n, edges m, density 2m / (n(n-1)). Exact methods are realistic up to roughly n = 80-100 on dense random graphs; sparse structured graphs can be far larger. Heuristics handle millions of vertices.
- **Graph structure.** Random, geometric, interval, planar, or derived from an application (interference graph, conflict graph)? Interval graphs and chordal graphs are colorable optimally in polynomial time — check before deploying heavy machinery.
- **Hard vs soft constraints.** Pure coloring has only hard "endpoints differ" constraints. If the user mentions preferences, spread requirements, or penalties (exams close together, adjacent channels), the problem is a coloring-flavored timetabling/assignment problem; the coloring core still applies but the objective changes.
- **Precoloring or list constraints.** Are some vertices fixed to specific colors (precoloring extension)? Does each vertex have its own allowed color list (list coloring)? Both are easy to add to MIP/CP and to construction heuristics, but they invalidate symmetry-breaking tricks based on color interchangeability.
- **Solver availability.** Gurobi license available? If not, OR-Tools CP-SAT is free and is usually the stronger exact tool for coloring anyway; HiGHS/CBC handle the MIP variant.
- **Quality requirement.** Proof of optimality required (publication, exact benchmark), or is a good coloring with a reported gap acceptable (engineering use)?
- **Time budget.** Seconds (greedy/DSATUR only), minutes (tabucol descent + clique bound), hours (exact attempt with CP-SAT or branch-and-price)?
- **Data format.** Adjacency matrix, edge list, DIMACS `.col` file? Standard benchmarks (DIMACS challenge graphs: DSJC, flat, le450 families) come as DIMACS edge lists.
- **Reproducibility.** Fix seeds for instance generation and for every randomized heuristic; report them.

## Problem Definition and Model Landscape

### Formal definition

Given an undirected graph $G = (V, E)$ with $|V| = n$ and $|E| = m$, a *k-coloring* is a map $c : V \to \{1, \dots, k\}$. It is *proper* if $c(u) \neq c(v)$ for every edge $\{u, v\} \in E$. The *chromatic number* $\chi(G)$ is the smallest $k$ admitting a proper k-coloring. Each color class $c^{-1}(i)$ is an independent set, so coloring is equivalent to partitioning $V$ into the fewest independent sets.

Key bounds, with $\omega(G)$ the clique number, $\Delta(G)$ the maximum degree, and $d(G)$ the degeneracy (largest minimum degree over all subgraphs):

$$\omega(G) \;\le\; \chi_f(G) \;\le\; \chi(G) \;\le\; d(G) + 1 \;\le\; \Delta(G) + 1$$

where $\chi_f$ is the fractional chromatic number (LP bound of the set-covering formulation). Brooks (1941) sharpens the upper bound: $\chi(G) \le \Delta(G)$ unless $G$ is complete or an odd cycle. Greedy coloring in a smallest-last (degeneracy) order achieves $d(G)+1$ colors (Matula & Beck 1983).

Complexity: deciding k-colorability is NP-complete for every fixed $k \ge 3$; $\chi(G)$ is NP-hard to approximate within $n^{1-\varepsilon}$ (Zuckerman 2007). Exceptions worth checking: bipartite graphs ($\chi = 2$, test via BFS), interval and chordal graphs (perfect elimination ordering gives $\chi = \omega$ in linear time), planar graphs ($\chi \le 4$).

### Assignment MIP model

With a color budget $H$ (any valid upper bound, e.g. the DSATUR value), binary $x_{vc} = 1$ iff vertex $v$ takes color $c$, and $y_c = 1$ iff color $c$ is used:

$$
\begin{aligned}
\min \; & \sum_{c=1}^{H} y_c \\
\text{s.t.} \; & \sum_{c=1}^{H} x_{vc} = 1 \qquad && \forall v \in V \\
& x_{uc} + x_{vc} \le y_c && \forall \{u,v\} \in E,\; c = 1,\dots,H \\
& y_c \le y_{c-1} && c = 2,\dots,H \\
& x_{vc},\, y_c \in \{0,1\}
\end{aligned}
$$

Two structural weaknesses to know in advance. First, the LP relaxation is nearly useless: $x_{vc} = 1/H$, $y_c = 2/H$ is feasible whenever $E \neq \emptyset$, so the LP bound is at most 2 regardless of $\chi(G)$. Second, colors are interchangeable, so the model has $H!$ symmetric copies of every solution; the ordering constraints $y_c \le y_{c-1}$ remove only part of this. Always pre-fix a clique (vertex $i$ of a clique $Q$ gets color $i$) — it breaks symmetry much harder and injects the bound $\chi \ge |Q|$. See **integer-programming-techniques** for the general theory of symmetry and relaxation strength.

Stronger exact alternatives:

- **Representatives formulation** (Campêlo, Campos & Corrêa 2008): binary $x_{uv}$ = "u represents the color class of v", defined on non-adjacent pairs. No color indices, hence no color symmetry; tighter LP bound.
- **Set covering over independent sets** (Mehrotra & Trick 1996): $\min \sum_S \lambda_S$ over independent sets $S$ covering every vertex. Its LP value is $\chi_f(G)$ — the strongest practical lower bound — solved by column generation with a maximum-weight independent set pricing problem; branch-and-price closes many DIMACS instances.
- **CP model**: one integer variable per vertex with domain $\{0,\dots,H-1\}$, a binary disequality per edge, minimize the maximum color. Posting `AllDifferent` on extracted cliques strengthens propagation substantially. CP-SAT with clique fixing is usually the best off-the-shelf exact method for coloring.

### Method selection

| Situation | Method |
|---|---|
| Need proof of optimality, n up to ~80-100 (dense) | CP-SAT with clique fixing; MIP as fallback |
| Need proof, larger sparse or structured graph | Branch-and-price over independent sets (Mehrotra & Trick 1996) |
| Fixed k, want a proper coloring fast | tabucol; PARTIALCOL for hard instances |
| Quick upper bound, any size | DSATUR; RLF when density > ~0.3 |
| Huge sparse graph (millions of vertices) | Greedy in degeneracy order, no matrix storage |
| Lower bound | Multi-start greedy clique; exact max clique on small graphs; $\chi_f$ via column generation |
| Bipartite / interval / chordal suspected | Test the structure first; polynomial algorithms apply |

### Applications map

| Application | Graph construction | Notes |
|---|---|---|
| Register allocation | Interference graph: variables live at the same time are adjacent | k = number of registers; spill code when k-coloring fails (Chaitin 1982) |
| Exam timetabling | Conflict graph: exams sharing a student are adjacent | Colors = time slots; soft constraints push beyond pure coloring — see **timetabling-and-rostering** (de Werra 1985) |
| Frequency assignment | Interference graph between transmitters | Distance/bandwidth variants: $|c(u) - c(v)| \ge d_{uv}$ (Aardal et al. 2007, frequency assignment survey) |
| Sports league scheduling | Edge coloring of the match graph | Edge coloring of $K_n$ = round-robin schedule |
| Sudoku, Latin squares | Precoloring extension on a structured graph | CP handles these naturally |

## Instance Generation and Validation

Group C contract: every coloring study needs a seeded generator and an independent validator. The validator recomputes feasibility and the objective from the adjacency matrix alone — never trust the solver's own bookkeeping.

```python
import numpy as np


def random_graph(n: int, p: float, seed: int) -> np.ndarray:
    """Erdos-Renyi G(n, p) as a symmetric boolean adjacency matrix (no self-loops)."""
    rng = np.random.default_rng(seed)
    upper = np.triu(rng.random((n, n)) < p, k=1)
    return upper | upper.T


def planted_k_colorable(n: int, k: int, p: float, seed: int) -> tuple[np.ndarray, np.ndarray]:
    """Random graph that is k-colorable by construction.

    Vertices are split into k classes uniformly at random; edges appear only
    between different classes, each with probability p. Returns (adjacency,
    planted coloring). Useful for testing: chi(G) <= k is guaranteed, and for
    moderate p the planted value is also optimal with high probability.
    """
    rng = np.random.default_rng(seed)
    classes = rng.integers(0, k, size=n)
    cross = classes[:, None] != classes[None, :]
    upper = np.triu((rng.random((n, n)) < p) & cross, k=1)
    return upper | upper.T, classes


def edges_from_adjacency(adj: np.ndarray) -> list[tuple[int, int]]:
    """Edge list with u < v from a symmetric adjacency matrix."""
    iu, jv = np.nonzero(np.triu(adj, k=1))
    return list(zip(iu.tolist(), jv.tolist()))


if __name__ == "__main__":
    adj, planted = planted_k_colorable(n=20, k=3, p=0.5, seed=42)
    print(adj.shape, int(adj.sum()) // 2, planted[:5])
    # Expected: (20, 20), around 60-70 edges, and a planted class vector in {0,1,2}
```

```python
import numpy as np


def validate_coloring(adj: np.ndarray, colors: np.ndarray) -> dict[str, int | bool]:
    """Independent feasibility + objective check for a vertex coloring.

    Returns conflict count (violated edges), the number of distinct colors used,
    and whether the color indices are compact (0..K-1 with no gaps). Recomputes
    everything from the adjacency matrix; shares no code with any solver.
    """
    n = adj.shape[0]
    if colors.shape != (n,):
        raise ValueError(f"colors has shape {colors.shape}, expected ({n},)")
    iu, jv = np.nonzero(np.triu(adj, k=1))
    conflicts = int(np.sum(colors[iu] == colors[jv]))
    used = np.unique(colors)
    return {
        "feasible": conflicts == 0,
        "conflicts": conflicts,
        "num_colors": int(used.size),
        "compact_indices": bool(np.array_equal(used, np.arange(used.size))),
    }


if __name__ == "__main__":
    c5 = np.zeros((5, 5), dtype=bool)
    for u, v in [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]:
        c5[u, v] = c5[v, u] = True
    print(validate_coloring(c5, np.array([0, 1, 0, 1, 2])))
    # Expected: feasible=True, conflicts=0, num_colors=3, compact_indices=True
    print(validate_coloring(c5, np.array([0, 1, 0, 1, 0])))
    # Expected: feasible=False, conflicts=1 (edge (4,0) has both endpoints colored 0)
```

## Exact Models: MIP and CP-SAT

The assignment MIP below follows the Group C constraint-builder pattern: each constraint family lives in its own named function, so families can be unit-tested and reused independently. Pass a clique from the lower-bound routine in Advanced Techniques to activate the clique-fixing family — on symmetric coloring models this is the single highest-impact modeling decision.

```python
import gurobipy as gp
from gurobipy import GRB
import numpy as np


def add_assignment_constraints(model: gp.Model, x: gp.tupledict, data: dict) -> None:
    """Each vertex receives exactly one color."""
    for v in range(data["n"]):
        model.addConstr(
            gp.quicksum(x[v, c] for c in range(data["H"])) == 1, name=f"assign[{v}]"
        )


def add_conflict_constraints(
    model: gp.Model, x: gp.tupledict, y: gp.tupledict, data: dict
) -> None:
    """Edge endpoints cannot share color c; also links x to the color-use variable y."""
    for u, v in data["edges"]:
        for c in range(data["H"]):
            model.addConstr(x[u, c] + x[v, c] <= y[c], name=f"conflict[{u},{v},{c}]")


def add_color_ordering_constraints(model: gp.Model, y: gp.tupledict, data: dict) -> None:
    """Color c may be used only if color c-1 is used (partial symmetry breaking)."""
    for c in range(1, data["H"]):
        model.addConstr(y[c] <= y[c - 1], name=f"order[{c}]")


def add_clique_fixing_constraints(model: gp.Model, x: gp.tupledict, data: dict) -> None:
    """Pre-color a known clique: the i-th clique vertex takes color i.

    Valid because clique vertices need pairwise distinct colors and colors are
    interchangeable. Kills most color symmetry and implies the bound chi >= |Q|.
    """
    for i, v in enumerate(data["clique"]):
        model.addConstr(x[v, i] == 1, name=f"clique_fix[{v}]")


def solve_coloring_mip(
    adj: np.ndarray,
    H: int,
    clique: tuple[int, ...] = (),
    time_limit: float = 60.0,
) -> tuple[int, np.ndarray] | None:
    """Assignment-model MIP for minimum vertex coloring with color budget H.

    Returns (number of colors, coloring array) or None if no solution was found.
    H should be a known upper bound, e.g. the DSATUR color count.
    """
    iu, jv = np.nonzero(np.triu(adj, k=1))
    data = {
        "n": adj.shape[0],
        "H": H,
        "edges": list(zip(iu.tolist(), jv.tolist())),
        "clique": clique,
    }
    model = gp.Model("vertex_coloring")
    model.Params.OutputFlag = 0
    model.Params.TimeLimit = time_limit
    model.Params.Symmetry = 2  # aggressive solver-side symmetry detection on top
    x = model.addVars(data["n"], H, vtype=GRB.BINARY, name="x")
    y = model.addVars(H, vtype=GRB.BINARY, name="y")
    add_assignment_constraints(model, x, data)
    add_conflict_constraints(model, x, y, data)
    add_color_ordering_constraints(model, y, data)
    add_clique_fixing_constraints(model, x, data)
    model.setObjective(gp.quicksum(y[c] for c in range(H)), GRB.MINIMIZE)
    model.optimize()
    ok = model.Status == GRB.OPTIMAL or (
        model.Status == GRB.TIME_LIMIT and model.SolCount > 0
    )
    if not ok:
        return None
    colors = np.array(
        [max(range(H), key=lambda c: x[v, c].X) for v in range(data["n"])], dtype=int
    )
    return int(round(model.ObjVal)), colors


if __name__ == "__main__":
    c5 = np.zeros((5, 5), dtype=bool)
    for u, v in [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]:
        c5[u, v] = c5[v, u] = True
    result = solve_coloring_mip(c5, H=5, clique=(0, 1))
    print(result)
    # Expected: (3, coloring) — an odd cycle has chromatic number 3
```

CP-SAT is usually the stronger exact tool here: the disequality per edge propagates well, there are no big-M or linking artifacts, and clique fixing plugs in the same way. Minimize the maximum color index instead of counting used colors — with compact color use these coincide, and the max-objective propagates better.

```python
import numpy as np
from ortools.sat.python import cp_model


def solve_coloring_cpsat(
    adj: np.ndarray,
    H: int,
    clique: tuple[int, ...] = (),
    time_limit: float = 30.0,
) -> tuple[int, np.ndarray] | None:
    """CP-SAT minimum coloring: integer color per vertex, disequality per edge.

    Returns (number of colors, coloring) or None. Fixing a clique to colors
    0..|Q|-1 breaks color symmetry and seeds the lower bound. For interval
    variables, channeling, and search strategies see the constraint-programming
    skill.
    """
    n = adj.shape[0]
    model = cp_model.CpModel()
    x = [model.NewIntVar(0, H - 1, f"x[{v}]") for v in range(n)]
    max_color = model.NewIntVar(0, H - 1, "max_color")
    iu, jv = np.nonzero(np.triu(adj, k=1))
    for u, v in zip(iu.tolist(), jv.tolist()):
        model.Add(x[u] != x[v])
    model.AddMaxEquality(max_color, x)
    for i, v in enumerate(clique):
        model.Add(x[v] == i)
    model.Minimize(max_color)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit
    solver.parameters.num_workers = 8
    status = solver.Solve(model)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return None
    colors = np.array([solver.Value(x[v]) for v in range(n)], dtype=int)
    return int(solver.Value(max_color)) + 1, colors


if __name__ == "__main__":
    c5 = np.zeros((5, 5), dtype=bool)
    for u, v in [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]:
        c5[u, v] = c5[v, u] = True
    print(solve_coloring_cpsat(c5, H=5, clique=(0, 1)))
    # Expected: (3, coloring) — matches the MIP result, typically in milliseconds
```

When you need the decision version (is the graph k-colorable for fixed k?), drop `max_color` and the objective, set the domains to `0..k-1`, and call the solver once per k; CP-SAT's clause learning shines on these satisfiability-style runs.

## Construction Heuristics: DSATUR and RLF

DSATUR (Brélaz 1979) colors the vertex with the highest *saturation degree* (number of distinct colors among its neighbors) first, breaking ties by degree. It is exact on bipartite graphs and is the default quick upper bound — also the standard source of the color budget H for the exact models and the starting point for tabucol. RLF (Leighton 1979) builds one maximal independent set (color class) at a time; it uses more time per color but typically fewer colors on dense graphs.

```python
import numpy as np


def greedy_coloring(adj: np.ndarray, order: np.ndarray) -> np.ndarray:
    """Color vertices in the given order, always taking the smallest feasible color."""
    n = adj.shape[0]
    colors = np.full(n, -1, dtype=int)
    for v in order:
        taken = np.zeros(n + 1, dtype=bool)
        neighbor_colors = colors[adj[v]]
        taken[neighbor_colors[neighbor_colors >= 0]] = True
        colors[v] = int(np.argmin(taken))  # first False = smallest free color
    return colors


def degeneracy_order(adj: np.ndarray) -> np.ndarray:
    """Smallest-last ordering (Matula & Beck 1983); greedy on it uses <= degeneracy+1 colors."""
    n = adj.shape[0]
    deg = adj.sum(axis=1).astype(int)
    alive = np.ones(n, dtype=bool)
    order = np.empty(n, dtype=int)
    for i in range(n - 1, -1, -1):
        candidates = np.flatnonzero(alive)
        v = int(candidates[np.argmin(deg[candidates])])
        order[i] = v
        alive[v] = False
        deg[adj[v] & alive] -= 1
    return order


def dsatur(adj: np.ndarray) -> np.ndarray:
    """DSATUR (Brelaz 1979): repeatedly color the most saturated uncolored vertex.

    O(n^2) with the boolean saturation table below; exact on bipartite graphs.
    """
    n = adj.shape[0]
    colors = np.full(n, -1, dtype=int)
    degree = adj.sum(axis=1)
    sat_table = np.zeros((n, n + 1), dtype=bool)  # sat_table[v, c]: neighbor of v has color c
    for _ in range(n):
        uncolored = np.flatnonzero(colors < 0)
        sat = sat_table[uncolored].sum(axis=1)
        pick = uncolored[np.lexsort((-degree[uncolored], -sat))[0]]  # max sat, tie: max degree
        c = int(np.argmin(sat_table[pick]))  # smallest color absent from the neighborhood
        colors[pick] = c
        sat_table[adj[pick], c] = True
    return colors


if __name__ == "__main__":
    # validate_coloring and planted_k_colorable are defined earlier in this skill
    c5 = np.zeros((5, 5), dtype=bool)
    for u, v in [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]:
        c5[u, v] = c5[v, u] = True
    print(int(dsatur(c5).max()) + 1)
    # Expected: 3 — DSATUR finds the optimal 3-coloring of the 5-cycle
```

```python
import numpy as np


def rlf(adj: np.ndarray) -> np.ndarray:
    """Recursive Largest First (Leighton 1979): build one color class at a time.

    Each class is a maximal independent set grown to maximize coverage of the
    remaining graph: start from the highest-degree uncolored vertex, then
    repeatedly add the candidate with the most neighbors already excluded.
    Slower than DSATUR (O(n^3) worst case) but usually fewer colors on dense
    graphs.
    """
    n = adj.shape[0]
    colors = np.full(n, -1, dtype=int)
    uncolored = np.ones(n, dtype=bool)
    color = 0
    while uncolored.any():
        candidates = uncolored.copy()      # can still join this class
        excluded = np.zeros(n, dtype=bool)  # adjacent to the class, wait for a later color
        deg_in = (adj & candidates[None, :]).sum(axis=1)
        first = np.flatnonzero(candidates)
        v = int(first[np.argmax(deg_in[first])])
        while True:
            colors[v] = color
            uncolored[v] = False
            excluded |= adj[v] & candidates
            candidates &= ~adj[v]
            candidates[v] = False
            if not candidates.any():
                break
            toward_excluded = (adj & excluded[None, :]).sum(axis=1)
            pool = np.flatnonzero(candidates)
            v = int(pool[np.argmax(toward_excluded[pool])])
        color += 1
    return colors


if __name__ == "__main__":
    c5 = np.zeros((5, 5), dtype=bool)
    for u, v in [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]:
        c5[u, v] = c5[v, u] = True
    print(int(rlf(c5).max()) + 1)
    # Expected: 3 — RLF also colors the 5-cycle optimally
```

Practical rule: run DSATUR always (it is essentially free); add RLF when density exceeds ~0.3 or when DSATUR's value looks loose against the clique bound. For huge sparse graphs, use `greedy_coloring(adj, degeneracy_order(adj))` with sparse adjacency lists instead of the dense matrix.

## Tabucol: the Reference Metaheuristic

Tabucol (Hertz & de Werra 1987) is the classic tabu search for the *k-coloring decision problem* and remains the backbone of state-of-the-art coloring heuristics. Search space: all (improper) assignments of k colors. Objective: number of conflicting edges; zero means a proper k-coloring. Move: recolor one *conflicting* vertex. The whole method lives or dies on O(1) move evaluation via the matrix $\gamma[v, c]$ = number of neighbors of $v$ colored $c$: moving $v$ from $c_{old}$ to $c_{new}$ changes the conflict count by exactly $\gamma[v, c_{new}] - \gamma[v, c_{old}]$. Tenure, aspiration, and tabu-attribute design follow the **tabu-search** skill; the coloring-specific choice is the dynamic tenure $tt = \text{rand}(0,9) + 0.6 \cdot f$ tied to the current conflict count $f$.

```python
import numpy as np

BIG = 10**9


def tabucol(
    adj: np.ndarray, k: int, seed: int = 0, max_iters: int = 100_000
) -> tuple[np.ndarray, int]:
    """Tabucol (Hertz & de Werra 1987): tabu search for k-coloring.

    Minimizes the number of conflicting edges; returns (best coloring, best
    conflict count). A return of 0 conflicts means a proper k-coloring.
    All candidate moves are scored in one vectorized pass over the gamma matrix.
    """
    rng = np.random.default_rng(seed)
    n = adj.shape[0]
    colors = rng.integers(0, k, size=n)
    gamma = np.stack(
        [(adj & (colors == c)[None, :]).sum(axis=1) for c in range(k)], axis=1
    )  # gamma[v, c] = neighbors of v colored c
    conflicts = int(gamma[np.arange(n), colors].sum()) // 2
    best_colors, best_conf = colors.copy(), conflicts
    tabu_until = np.zeros((n, k), dtype=np.int64)  # (vertex, color) tabu expiry iteration
    for it in range(1, max_iters + 1):
        if best_conf == 0:
            break
        confl = np.flatnonzero(gamma[np.arange(n), colors] > 0)
        delta = gamma[confl] - gamma[confl, colors[confl]][:, None]  # (m_confl, k)
        delta[np.arange(confl.size), colors[confl]] = BIG            # forbid staying put
        tabu = tabu_until[confl] > it
        aspiration = conflicts + delta < best_conf                   # tabu override
        masked = np.where(~tabu | aspiration, delta, BIG)
        vi, c_new = np.unravel_index(int(np.argmin(masked)), masked.shape)
        if masked[vi, c_new] >= BIG:
            continue                                                 # everything tabu: skip
        v, c_old = int(confl[vi]), int(colors[confl[vi]])
        colors[v] = int(c_new)
        conflicts += int(delta[vi, c_new])
        gamma[adj[v], c_old] -= 1
        gamma[adj[v], int(c_new)] += 1
        tabu_until[v, c_old] = it + int(rng.integers(0, 10)) + int(0.6 * conflicts)
        if conflicts < best_conf:
            best_conf, best_colors = conflicts, colors.copy()
    return best_colors, best_conf
```

To minimize the number of colors, wrap tabucol in a descending-k driver: start from the DSATUR value and decrement k while a proper coloring is still found. A binary search on k is rarely worth it — failures at infeasible k burn the full iteration budget, so walking down one color at a time from a good upper bound is the standard protocol.

```python
import numpy as np


def tabucol_descent(adj: np.ndarray, seed: int = 0, iters_per_k: int = 200_000) -> np.ndarray:
    """Minimum coloring via tabucol with decreasing k.

    Starts one color below the DSATUR bound and keeps decrementing while
    tabucol reaches zero conflicts. Reuses dsatur() and tabucol() defined
    earlier in this skill.
    """
    best = dsatur(adj)
    k = int(best.max())  # one color fewer than the DSATUR coloring uses
    while k >= 1:
        candidate, conf = tabucol(adj, k, seed=seed, max_iters=iters_per_k)
        if conf > 0:
            break
        best, k = candidate, k - 1
    return best


if __name__ == "__main__":
    # planted_k_colorable and validate_coloring are defined earlier in this skill
    adj, _ = planted_k_colorable(n=60, k=5, p=0.5, seed=3)
    solution = tabucol_descent(adj, seed=7, iters_per_k=20_000)
    print(validate_coloring(adj, solution))
    # Expected: feasible=True; num_colors is typically 5 on this planted 5-colorable instance
```

Parameter guidance: the tenure constant 0.6 and the random component rand(0,9) are robust across DIMACS benchmarks (Galinier & Hao 1999 use the same recipe inside their hybrid). If the search cycles (conflict count oscillates over a small set of values), increase the multiplier toward 1.0 or add a reactive scheme; if it stagnates above zero on an instance you believe k-colorable, increase `max_iters` first — tabucol often needs millions of iterations near the chromatic number, and each iteration is cheap.

## Advanced Techniques

### Kempe chains

A *Kempe chain* for colors $(c_1, c_2)$ is a connected component of the subgraph induced by the vertices colored $c_1$ or $c_2$. Swapping the two colors along a chain keeps a proper coloring proper — this is the classic feasibility-preserving move for coloring, central to simulated-annealing approaches (Johnson, Aragon, McGeoch & Schevon 1991, "Optimization by simulated annealing, part II") and to soft-constraint optimization at fixed k in timetabling, where you improve penalties without ever breaking the conflict constraints. See **simulated-annealing** for cooling-schedule design around this neighborhood.

```python
import numpy as np


def kempe_chain(adj: np.ndarray, colors: np.ndarray, v: int, c2: int) -> np.ndarray:
    """Vertex indices of the Kempe chain containing v for colors (colors[v], c2)."""
    c1 = int(colors[v])
    mask = (colors == c1) | (colors == c2)
    chain = np.zeros(adj.shape[0], dtype=bool)
    frontier = np.zeros(adj.shape[0], dtype=bool)
    chain[v] = frontier[v] = True
    while frontier.any():
        reached = adj[frontier].any(axis=0) & mask & ~chain
        chain |= reached
        frontier = reached
    return np.flatnonzero(chain)


def kempe_swap(colors: np.ndarray, chain: np.ndarray, c1: int, c2: int) -> np.ndarray:
    """Exchange colors c1 and c2 on the chain; a proper coloring stays proper."""
    out = colors.copy()
    out[chain] = np.where(out[chain] == c1, c2, c1)
    return out


if __name__ == "__main__":
    # Triangle 0-1-2 plus pendant vertex 3 attached to vertex 0
    adj = np.zeros((4, 4), dtype=bool)
    for u, w in [(0, 1), (1, 2), (0, 2), (0, 3)]:
        adj[u, w] = adj[w, u] = True
    colors = np.array([0, 1, 2, 1])
    chain = kempe_chain(adj, colors, v=3, c2=2)
    print(chain, kempe_swap(colors, chain, c1=1, c2=2))
    # Expected: chain [3] (vertex 3 alone), new coloring [0 1 2 2] — still proper
```

### Clique lower bounds

Any clique $Q$ certifies $\chi(G) \ge |Q|$. A cheap multi-start greedy clique closes the gap surprisingly often on application graphs; when the greedy clique size equals the heuristic color count, optimality is proven without any exact solver. For small graphs, an exact maximum clique (networkx `max_weight_clique`, or a MIP) is affordable. Remember the bound can be arbitrarily loose: triangle-free graphs exist with unbounded $\chi$ (Mycielski construction), so when $|Q|$ stalls below the upper bound, switch to the fractional bound $\chi_f$ via column generation over independent sets (Mehrotra & Trick 1996).

```python
import numpy as np


def greedy_clique(adj: np.ndarray, seed: int = 0, restarts: int = 100) -> np.ndarray:
    """Multi-start greedy heuristic clique; its size lower-bounds chi(G).

    Each restart seeds at a degree-biased random vertex, then repeatedly adds
    the candidate with the most neighbors among the remaining candidates.
    """
    rng = np.random.default_rng(seed)
    n = adj.shape[0]
    degree = adj.sum(axis=1).astype(float)
    best = np.array([], dtype=int)
    probs = degree / degree.sum() if degree.sum() > 0 else np.full(n, 1.0 / n)
    for _ in range(restarts):
        v = int(rng.choice(n, p=probs))
        clique = [v]
        candidates = adj[v].copy()
        while candidates.any():
            pool = np.flatnonzero(candidates)
            scores = (adj[pool] & candidates[None, :]).sum(axis=1)
            v = int(pool[np.argmax(scores)])
            clique.append(v)
            candidates &= adj[v]
        if len(clique) > best.size:
            best = np.array(sorted(clique))
    return best


if __name__ == "__main__":
    # planted_k_colorable is defined earlier in this skill
    adj, _ = planted_k_colorable(n=60, k=5, p=0.5, seed=3)
    clique = greedy_clique(adj, seed=1)
    print(clique.size)
    # Expected: a clique of size 4-5; if 5, it matches the planted chromatic number
```

### Symmetry handling in exact models

Three escalating levels: (1) ordered color-use constraints $y_c \le y_{c-1}$ — cheap, weak; (2) clique pre-fixing — strong, costs nothing, always do it; (3) symmetry-free formulations — the representatives model (Campêlo et al. 2008) or set covering with branch-and-price. Solver-side symmetry detection (`Model.Params.Symmetry = 2` in Gurobi) helps but does not replace clique fixing, because the solver must rediscover structure you already know. Avoid combining aggressive manual fixing with lazy-constraint callbacks unless you verify the fixing remains valid for every cut you add.

### Beyond tabucol: PARTIALCOL and HEA

Two upgrades matter when tabucol stalls on hard DIMACS instances. PARTIALCOL (Blöchliger & Zufferey 2008) searches over *partial proper* colorings: uncolored vertices form the objective, moves assign a vertex to a class and evict conflicting neighbors; its reactive tenure removes the main tuning burden. The hybrid evolutionary algorithm HEA (Galinier & Hao 1999) wraps tabucol inside a population with the GPX crossover — children inherit entire color classes, alternately taking the largest class from each parent — and held best-known results on flat and DSJC graphs for two decades. Build HEA only after tabucol with a generous budget fails: the population machinery pays off only on the hardest 10 percent of instances.

### Variant colorings driven by applications

Frequency assignment needs distance constraints $|c(u) - c(v)| \ge d_{uv}$ (T-coloring); model in CP-SAT with `AbsEquality` or in MIP with two big-M inequalities per edge. Precoloring extension (some vertices fixed) and list coloring (per-vertex allowed sets) restrict domains directly in CP and fix or remove $x_{vc}$ variables in MIP — but both break color interchangeability, so drop the ordering constraints and clique fixing or re-derive them per instance. Equitable coloring (class sizes differ by at most one) adds cardinality bounds $\lfloor n/k \rfloor \le \sum_v x_{vc} \le \lceil n/k \rceil$ and appears in load-balancing applications.

## Practical Challenges

**The MIP explores millions of nodes without moving the lower bound.** This is the symmetry + weak-LP signature of the assignment model. Fix a clique, add ordering constraints, and give the solver the DSATUR coloring as a MIP start. If the bound still stalls, switch to CP-SAT for the decision version per k, or to branch-and-price if you need the tight $\chi_f$ bound.

**Tabucol reports a few stubborn conflicts at a k you believe feasible.** First scale iterations: near $\chi$ the search routinely needs $10^6$-$10^7$ iterations, and each costs microseconds. Then check the tenure: oscillation over few states means tenure too short; a frozen conflict set means tenure too long or the instance needs PARTIALCOL's partial-coloring search space.

**The clique bound and the heuristic upper bound do not meet.** This is normal, not a bug — both bounds can be loose simultaneously. Report the interval $[\,|Q|,\ k_{best}\,]$ honestly. To shrink it: exact max clique on graphs up to a few thousand vertices, fractional chromatic number via column generation, or an exact run of CP-SAT at $k = k_{best} - 1$ to prove the upper bound tight (UNSAT proves $\chi = k_{best}$).

**Validation passes in the heuristic but the MIP claims the instance needs more colors.** Almost always an indexing mismatch: heuristics here use colors 0..k-1 while the MIP uses a budget H of color slots. Run the independent validator on both solutions and compare `num_colors`, never the raw maximum index; check `compact_indices` to catch gap-ridden labelings.

**The graph is too large for a dense adjacency matrix.** A boolean n×n matrix at n = 100,000 is 10 GB. Switch to adjacency lists or `scipy.sparse` CSR; DSATUR, degeneracy ordering, and tabucol's gamma updates all translate — gamma becomes a per-vertex dict or a sparse n×k matrix, and you only ever touch rows of conflicting vertices.

**The user's "coloring problem" has soft constraints.** Exams should be spread out, registers have move-coalescing preferences, channels have adjacent-band penalties. Solve the hard coloring core first to fix k, then optimize the soft objective at fixed k with Kempe-chain moves (they preserve feasibility). If the soft structure dominates, hand the problem to the timetabling toolset — see **timetabling-and-rostering**.

**Benchmarking against DIMACS instances gives unstable results.** Coloring heuristics have heavy-tailed runtimes; a single seed says little. Run 10-30 seeds per instance, report success rate at fixed k plus median time-to-target, and fix the iteration budget per k so the descent protocol is comparable across methods.

**DSATUR uses far more colors than expected on a structured graph.** Check whether the graph is interval, chordal, or bipartite before blaming the heuristic — those classes have exact polynomial algorithms, and DSATUR's tie-breaking can be unlucky on them. On general graphs, try RLF and `greedy_coloring` over several random orders; the best-of ensemble is a stronger and still cheap upper bound.

## Tools & Libraries

| Library | When to use | Note |
|---|---|---|
| gurobipy | Assignment MIP, representatives model, branch-and-price master | Commercial license; set `Symmetry=2` and always clique-fix |
| OR-Tools CP-SAT | Exact coloring and k-coloring decision | Free; usually the best exact off-the-shelf choice here |
| networkx | `greedy_color` (strategies incl. DSATUR), clique finding, graph I/O | Convenient but slow on large graphs; fine up to ~10^5 edges |
| python-igraph | Large-graph handling, fast clique and component routines | C core; better than networkx beyond ~10^6 edges |
| scipy.sparse | Adjacency storage for huge graphs | CSR rows replace dense matrix rows in all algorithms above |
| numpy | Tabucol, DSATUR, RLF, validators | The implementations in this skill |
| DIMACS `.col` files | Standard benchmarks (DSJC, flat, le450, school) | Johnson & Trick (1996), DIMACS coloring challenge |

## Output Format

A complete coloring study reports both bounds, the certificate, and reproducibility data:

**Instance summary.** Name/seed, n, m, density, structure notes (bipartite/chordal checks performed), source (generator call or DIMACS file).

**Bounds table.** One row per bound with its source and time:

| Bound | Value | Source | Time (s) |
|---|---|---|---|
| Lower | 5 | greedy clique (100 restarts, seed 1) | 0.1 |
| Upper | 6 | DSATUR | 0.05 |
| Upper | 5 | tabucol descent (seed 7, 2e5 iters/k) | 3.2 |
| Status | proven optimal | LB = UB = 5 | — |

**Solution certificate.** The coloring itself (vertex → color array, compact indices), plus the validator output: `feasible=True, conflicts=0, num_colors=5`. Persist as CSV (`vertex,color`) or JSON next to the instance file.

**Method report.** For exact runs: solver, status (`OPTIMAL` / `TIME_LIMIT`), final MIP gap or CP-SAT best bound, time limit, clique used for fixing. For tabucol: seeds, iterations per k, the k-descent trajectory (k tried → success/fail → iterations consumed), and success rate over seeds if multiple runs.

**Gap statement.** If LB < UB, state the interval explicitly ("χ ∈ [5, 6]; 6-coloring found, 5-clique certified, k=5 undecided after 600 s CP-SAT") rather than reporting a single number.

**Artifacts.** Instance file (or generator call with seed), solution CSV, run log with parameters, and the validator invocation that anyone can re-run.

## Questions to Ask

- Do you need the minimum number of colors, or just any proper coloring within a fixed budget k?
- How large is the graph (vertices, edges), and is it dense or sparse?
- Where does the graph come from — could it be interval, chordal, bipartite, or planar?
- Are some vertices pre-assigned to colors, or do vertices have restricted color lists?
- Are there soft constraints or preferences beyond "adjacent vertices differ"?
- Do adjacent colors need separation (frequency-style distance constraints)?
- Is a proof of optimality required, or is a coloring with a reported gap enough?
- What time budget and compute do you have per instance?
- Do you have a Gurobi license, or should everything run on free solvers?
- Do you need results on standard benchmarks (DIMACS) for comparison with literature?

## Related Skills

- **constraint-programming** — when the exact route goes through CP-SAT: disequality models, AllDifferent on cliques, search strategies, and CP-vs-MIP selection.
- **simulated-annealing** — when using Kempe-chain neighborhoods inside SA for coloring or fixed-k soft-constraint optimization; cooling-schedule and acceptance design.
- **tabu-search** — when tuning tabucol: tenure schemes, aspiration criteria, move attributes, and diversification beyond the coloring-specific recipe shown here.
- **timetabling-and-rostering** — when the coloring is really an exam or course timetabling problem with soft constraints, room capacities, and benchmark formats.
- **integer-programming-techniques** — when the MIP route needs formulation tightening: symmetry breaking, LP-relaxation strength, and MIP-gap interpretation for the assignment model.
