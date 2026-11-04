---
name: multi-objective-optimization
description: When the user wants to optimize two or more conflicting objectives and reason about Pareto trade-offs — Pareto dominance and efficient sets, exact front generation with weighted-sum and epsilon-constraint scalarizations in Gurobi, NSGA-II mechanics (fast non-dominated sorting, crowding distance, crowded tournament), pymoo workflows, and hypervolume/IGD quality indicators with sound normalization. Also use when the user mentions "multi-objective," "Pareto front," "NSGA-II," "epsilon-constraint," "hypervolume," "trade-off," "nadir point," or when a model carries several objectives that cannot be merged into one number. For selection machinery inside evolutionary algorithms, see selection-and-replacement-strategies; for plotting Pareto fronts and convergence, see matplotlib-optimization-visualization.
---

# Multi-Objective Optimization

You are an expert in multi-objective combinatorial optimization. This skill covers the full a-posteriori workflow — define Pareto optimality, generate the nondominated front exactly (weighted sum, epsilon-constraint with Gurobi) or approximately (NSGA-II, from scratch and via pymoo), measure approximation quality (hypervolume, IGD/IGD+), and support the final single-solution decision. Use the protocols below to pick the right method for the objective count, problem class, and budget, and to report results that survive peer review.

## Initial Assessment

Establish these facts before writing any model or algorithm:

- **How many objectives M, and are they genuinely conflicting?** Sample feasible solutions and check pairwise objective correlation. Two strongly positively correlated objectives collapse to (nearly) one; optimizing both separately wastes the entire multi-objective apparatus.
- **What does the decision maker actually need?** One solution under known priorities (a-priori articulation), the whole trade-off curve to choose from afterwards (a-posteriori), or an interactive loop? This single question selects most of the method.
- **Is the model an explicit MILP or a black-box evaluation?** Epsilon-constraint needs a solvable scalarized model; if each scalarized MILP solves in seconds-to-minutes, an exact bi-objective front is usually affordable. Black-box or very large models push you to evolutionary methods.
- **Are the objective functions integer-valued?** Integer objectives let the epsilon-constraint sweep step by exactly 1 and terminate with the provably complete front. Continuous objectives need a grid density decision and yield a representation, not the full front.
- **Estimate the nondominated set size.** Bi-objective integer programs can have very many nondominated points (growing exponentially in the worst case — see Ehrgott (2005), *Multicriteria Optimization*). The cost of an exact sweep is one MILP per front point; budget accordingly.
- **Objective scales and units.** Cost in euros vs CO2 in tons differ by orders of magnitude. Every distance-based mechanism (crowding, hypervolume, IGD) silently breaks without normalization. Fix ideal/nadir estimates and record them.
- **Hard constraints vs objectives.** A "constraint" with a negotiable bound is often better treated as an objective (and vice versa). Epsilon-constraint makes this conversion explicit; confirm with the stakeholder which quantities are negotiable.
- **Solver availability and license.** Gurobi for the exact scalarization loops here; for license-free settings the same loops run on HiGHS/SCIP with longer runtimes.
- **Evaluation budget for evolutionary methods.** Population size N and generations G give N×G evaluations. The front cannot hold more points than the population; size N at 2-5× the front cardinality you intend to report.
- **Comparison protocol.** If two or more algorithms (or parameter settings) will be compared, fix now: instances, seeds per algorithm (10-30), identical normalization bounds, one shared hypervolume reference point, and a reference front (exact if available, else pooled best-known).
- **Reproducibility.** Every stochastic component takes an explicit seed (`np.random.default_rng(seed)`); every exact solve logs status, gap, and runtime per epsilon grid point.
- **Decision-support endgame.** Plan how the front turns into a decision: knee points, pseudo-weights, or a stakeholder workshop. A 200-point front without a selection protocol is not a deliverable.

## Pareto Optimality and Method Selection

### Definitions

For minimization of $M$ objectives over feasible set $X$:

$$
\min_{x \in X} \; F(x) = \big(f_1(x), \dots, f_M(x)\big).
$$

Solution $x$ **dominates** $y$ (written $x \prec y$) iff $f_i(x) \le f_i(y)$ for all $i$ and $f_j(x) < f_j(y)$ for at least one $j$. If only the first condition holds, $x$ *weakly dominates* $y$. A solution dominated by no feasible solution is **efficient** (Pareto-optimal); the efficient solutions form the efficient set $X_E$, and their image $Y_N = F(X_E)$ is the **Pareto front**. Two reference points bound the front:

$$
z^{I}_i = \min_{x \in X_E} f_i(x) \quad \text{(ideal point)}, \qquad
z^{N}_i = \max_{x \in X_E} f_i(x) \quad \text{(nadir point)}.
$$

The ideal point comes from $M$ single-objective solves. The nadir is exact from the payoff table only for $M = 2$; for $M \ge 3$ it must be estimated, and a wrong nadir distorts every normalized quantity downstream.

A nondominated point is **supported** if it minimizes some strictly positive weighted sum of the objectives — geometrically, it lies on the boundary of the convex hull of $Y_N + \mathbb{R}^M_{\ge 0}$. All other nondominated points are **unsupported**. Convex problems have no unsupported points (Geoffrion 1968, properly efficient solutions); integer programs routinely have many — often the majority of the front. This single fact is why the weighted sum is not a complete method for MILPs.

### Decision tree

```text
What does the decision maker need?
├─ One solution, strict priority order known
│   └─ lexicographic / hierarchical solve (Gurobi setObjectiveN)        [a priori]
├─ One solution, aspiration levels ("about 100k cost, about 20t CO2")
│   └─ achievement scalarizing function (Wierzbicki 1980), one solve    [a priori]
└─ The trade-off curve itself                                           [a posteriori]
    ├─ M = 2, explicit MILP, scalarized solves tractable
    │   └─ augmented epsilon-constraint sweep → exact complete front
    ├─ M = 3, explicit MILP
    │   └─ AUGMECON2 grid (exact but solve count grows with grid²)
    ├─ M = 2-3, black-box / too large for repeated MILPs
    │   └─ NSGA-II (own implementation or pymoo)
    └─ M ≥ 4 (many-objective)
        └─ NSGA-III / MOEA/D — plain dominance stops discriminating
```

### Method comparison

| Method | Finds unsupported points? | Exactness | Cost | Use when |
|---|---|---|---|---|
| Weighted sum sweep | no | each solve gives an efficient point (w > 0) | one MILP per weight | quick supported-front sketch; convex problems; warm-starting other methods |
| Augmented epsilon-constraint | yes | complete front for M=2 with integer objectives | one MILP per front point (+1) | the default exact method for bi-objective MILPs |
| Lexicographic (hierarchical) | n/a — one point | efficient point under priority order | M chained solves | priorities known and strict; also builds payoff tables |
| Achievement scalarizing | yes | one efficient point per reference point | one solve | decision maker supplies aspiration levels |
| NSGA-II (Deb et al. 2002) | yes | approximation, no guarantee | N×G evaluations | M = 2-3, black-box, large instances, nonlinearities |
| NSGA-III (Deb & Jain 2014) / MOEA/D (Zhang & Li 2007) | yes | approximation | N×G evaluations | M ≥ 4, or when a structured spread is wanted |

### Complexity notes

- Fast non-dominated sorting: $O(M N^2)$ per population of size $N$; crowding distance $O(M N \log N)$. NSGA-II's per-generation cost is dominated by these plus evaluation.
- Exact hypervolume is polynomial for $M \le 3$ ($O(n \log n)$ for $M = 2$) and #P-hard in general; use Monte Carlo approximation or `moocore` for $M \ge 5$.
- An epsilon-constraint sweep for $M = 2$ solves exactly $|Y_N| + 1$ MILPs (the last one proves infeasibility). For $M = 3$ the AUGMECON2 grid multiplies solves by the grid resolution of the second constrained objective.

## Exact Pareto Fronts with Gurobi

### Scalarization math

**Weighted sum.** For weights $w \in \mathbb{R}^M_{> 0}$, any optimum of $\min_x \sum_m w_m f_m(x)$ is efficient. The converse fails for non-convex feasible images: unsupported points are optimal for *no* weight vector. Sweeping weights therefore yields only the supported front, and evenly spaced weights yield unevenly spaced points (clustered where the hull is flat).

**Epsilon-constraint** (Haimes, Lasdon & Wismer 1971). Keep one objective, bound the others:

$$
\min_x \; f_1(x) \quad \text{s.t.} \quad f_j(x) \le \varepsilon_j \;\; (j = 2, \dots, M), \;\; x \in X.
$$

Every efficient solution is optimal for some $\varepsilon$, including unsupported ones. Two practical refinements:

1. **Augmentation** (Mavrotas 2009, "Effective implementation of the ε-constraint method in multi-objective mathematical programming problems" — AUGMECON): a plain epsilon-constraint optimum can be only *weakly* efficient. Add the constrained objectives' slacks to the objective with a small premium $\delta$, or equivalently optimize $f_1 + \delta f_2$ directly. With integer-valued $f_1$ and $\delta < 1 / (\max f_2 - \min f_2 + 1)$, this maximizes $f_1$ exactly and breaks ties lexicographically by $f_2$ — every solve returns a nondominated point.
2. **Adaptive stepping** for integer objectives: after finding the point with value $f_2 = z_2$, set the next bound to $z_2 \pm 1$ (direction per optimization sense). The sweep then enumerates the complete front with no grid-density guesswork.

The worked example is a bi-objective 0-1 knapsack (two profit vectors, one capacity), a maximization problem — all inequalities flip accordingly. The instance is built so that one front point is unsupported, which makes the weighted sum's blind spot visible.

### Weighted-sum sweep (supported points only)

```python
import numpy as np
import gurobipy as gp
from gurobipy import GRB


def weighted_sum_front(
    p1: list[float], p2: list[float], w: list[float], capacity: float, n_weights: int = 21
) -> list[tuple[float, float]]:
    """Supported nondominated points of max(p1·x, p2·x) s.t. w·x <= capacity, x binary.

    Sweeps n_weights convex weight combinations and filters dominated outcomes.
    """
    n = len(w)
    m = gp.Model("bi_knapsack_ws")
    m.Params.OutputFlag = 0
    m.Params.MIPGap = 0.0
    x = m.addVars(n, vtype=GRB.BINARY, name="x")
    m.addConstr(gp.quicksum(w[i] * x[i] for i in range(n)) <= capacity, name="capacity")
    f1 = gp.quicksum(p1[i] * x[i] for i in range(n))
    f2 = gp.quicksum(p2[i] * x[i] for i in range(n))

    points: set[tuple[float, float]] = set()
    for w1 in np.linspace(0.0, 1.0, n_weights):
        m.setObjective(w1 * f1 + (1.0 - w1) * f2, GRB.MAXIMIZE)
        m.optimize()
        if m.Status == GRB.OPTIMAL:
            points.add((round(f1.getValue()), round(f2.getValue())))

    # Filter dominated/duplicate outcomes (extreme weights can return weakly efficient points).
    front: list[tuple[float, float]] = []
    best_f2 = -float("inf")
    for z1, z2 in sorted(points, reverse=True):       # descending f1
        if z2 > best_f2:
            front.append((z1, z2))
            best_f2 = z2
    return front


p1, p2, w = [10.0, 1.0, 6.0], [1.0, 10.0, 6.0], [4.0, 4.0, 4.0]
print(weighted_sum_front(p1, p2, w, capacity=8.0))
# Expected: [(16, 7), (7, 16)] — only the two supported points. The nondominated
# point (11, 11) lies inside the convex hull and is optimal for NO weight vector.
```

### Augmented epsilon-constraint (complete front)

```python
import gurobipy as gp
from gurobipy import GRB


def pareto_front_epsilon(
    p1: list[float], p2: list[float], w: list[float], capacity: float
) -> list[tuple[int, int]]:
    """Complete nondominated front of max(p1·x, p2·x) s.t. w·x <= capacity, x binary.

    Augmented epsilon-constraint with adaptive integer stepping: requires
    integer-valued objective coefficients. One MILP solve per front point.
    """
    n = len(w)
    m = gp.Model("bi_knapsack_eps")
    m.Params.OutputFlag = 0
    m.Params.MIPGap = 0.0
    x = m.addVars(n, vtype=GRB.BINARY, name="x")
    m.addConstr(gp.quicksum(w[i] * x[i] for i in range(n)) <= capacity, name="capacity")
    f1 = gp.quicksum(p1[i] * x[i] for i in range(n))
    f2 = gp.quicksum(p2[i] * x[i] for i in range(n))

    # Tie-break premium: small enough that one unit of f1 always outweighs all of f2.
    delta = 1.0 / (sum(p2) + 1.0)
    m.setObjective(f1 + delta * f2, GRB.MAXIMIZE)
    eps_con = m.addConstr(f2 >= 0.0, name="epsilon")

    front: list[tuple[int, int]] = []
    eps = 0.0
    while True:
        eps_con.RHS = eps
        m.optimize()
        if m.Status != GRB.OPTIMAL:          # INFEASIBLE terminates the sweep
            break
        z1, z2 = round(f1.getValue()), round(f2.getValue())
        front.append((z1, z2))
        eps = z2 + 1                         # demand strictly better f2 next
    return front


p1, p2, w = [10.0, 1.0, 6.0], [1.0, 10.0, 6.0], [4.0, 4.0, 4.0]
print(pareto_front_epsilon(p1, p2, w, capacity=8.0))
# Expected: [(16, 7), (11, 11), (7, 16)] — the complete front in 4 MILP solves,
# including the unsupported point (11, 11) that the weighted-sum sweep misses.
```

For larger models, keep the same persistent-model pattern: build once, update only `eps_con.RHS` between solves so Gurobi reuses presolve work, set a per-solve `TimeLimit`, and record `(Status, MIPGap, Runtime)` per grid point. Any point returned at `GRB.TIME_LIMIT` with `SolCount > 0` is feasible but possibly dominated — flag it in the output table rather than silently mixing it into an "exact" front.

### Gurobi's native multi-objective API (a priori, one point)

Gurobi's `setObjectiveN` solves blended (weighted) or hierarchical (lexicographic with allowed degradation) multi-objective models. It returns **one** preferred solution, not a front — use it when priorities are known, and the sweep above when the trade-off curve is the deliverable.

```python
import gurobipy as gp
from gurobipy import GRB


def lexicographic_knapsack(
    p1: list[float], p2: list[float], w: list[float], capacity: float, reltol: float
) -> tuple[float, float]:
    """Hierarchical solve: maximize p1·x first, then p2·x, allowing reltol
    relative degradation of the first objective."""
    n = len(w)
    m = gp.Model("bi_knapsack_lex")
    m.Params.OutputFlag = 0
    x = m.addVars(n, vtype=GRB.BINARY, name="x")
    m.addConstr(gp.quicksum(w[i] * x[i] for i in range(n)) <= capacity, name="capacity")
    m.ModelSense = GRB.MAXIMIZE
    m.setObjectiveN(gp.quicksum(p1[i] * x[i] for i in range(n)),
                    index=0, priority=2, reltol=reltol, name="profit1")
    m.setObjectiveN(gp.quicksum(p2[i] * x[i] for i in range(n)),
                    index=1, priority=1, name="profit2")
    m.optimize()
    if m.Status != GRB.OPTIMAL:
        raise RuntimeError(f"unexpected status {m.Status}")
    values = []
    for k in range(2):
        m.Params.ObjNumber = k
        values.append(m.ObjNVal)
    return values[0], values[1]


p1, p2, w = [10.0, 1.0, 6.0], [1.0, 10.0, 6.0], [4.0, 4.0, 4.0]
print(lexicographic_knapsack(p1, p2, w, capacity=8.0, reltol=0.4))
# Expected: (11.0, 11.0) — allowing 40% degradation of profit1 (16 -> 9.6) lets
# the second level pick the balanced solution. With reltol=0.0 it returns (16, 7).
```

The same payoff-table pattern (lexicographically optimize each objective in turn) produces the ideal point and, for $M = 2$, the exact nadir — the bounds the epsilon sweep and all normalization need.

## NSGA-II: Mechanics and a Complete Implementation

NSGA-II (Deb, Pratap, Agarwal & Meyarivan 2002, "A Fast and Elitist Multiobjective Genetic Algorithm: NSGA-II") replaces a GA's scalar fitness with a two-level criterion: nondominated rank first, crowding distance second. Everything else is a standard elitist (mu+lambda) GA — see genetic-algorithms for operator depth and selection-and-replacement-strategies for the pressure analysis that carries over unchanged.

```text
NSGA-II generation (population P, |P| = N, minimization)
  1. rank  <- fast_nondominated_sort(F(P))                  # O(M N^2)
  2. crowd <- crowding_distance within each front           # O(M N log N)
  3. parents <- binary tournament on (rank asc, crowd desc), 2N draws
  4. offspring Q <- crossover + mutation on parent pairs, |Q| = N
  5. evaluate F(Q)
  6. P <- best N of P ∪ Q by (rank, then crowding) truncation   # elitist
Stop on the generation/evaluation budget; report the rank-0 set of P.
```

Crowding distance of an interior point is the sum, over objectives, of the normalized gap between its two sorted neighbors; boundary points get infinity so the extremes always survive. It is a density estimator: in the survival truncation and the tournament tie-break it pushes the population toward an even spread along the front.

### Core machinery

```python
import numpy as np


def fast_nondominated_sort(F: np.ndarray) -> np.ndarray:
    """Front index per row of objective matrix F (minimization); 0 = best. O(M N^2)."""
    weak = (F[:, None, :] <= F[None, :, :]).all(axis=2)
    strict = (F[:, None, :] < F[None, :, :]).any(axis=2)
    dom = weak & strict                       # dom[i, j]: i dominates j
    counts = dom.sum(axis=0)                  # number of dominators per point
    ranks = np.full(len(F), -1, dtype=int)
    unassigned = np.ones(len(F), dtype=bool)
    r = 0
    while unassigned.any():
        front = unassigned & (counts == 0)
        ranks[front] = r
        counts = counts - dom[front].sum(axis=0)
        unassigned &= ~front
        r += 1
    return ranks


def crowding_distance(F: np.ndarray) -> np.ndarray:
    """Crowding distance of each row within ONE front (minimization)."""
    n, m = F.shape
    if n <= 2:
        return np.full(n, np.inf)
    d = np.zeros(n)
    for k in range(m):
        order = np.argsort(F[:, k], kind="stable")
        fk = F[order, k]
        d[order[0]] = d[order[-1]] = np.inf
        span = fk[-1] - fk[0]
        if span > 0:
            d[order[1:-1]] += (fk[2:] - fk[:-2]) / span
    return d


F = np.array([[1.0, 5.0], [2.0, 4.0], [3.0, 3.0], [2.5, 4.5], [4.0, 4.5]])
ranks = fast_nondominated_sort(F)
print(ranks, crowding_distance(F[ranks == 0]))
# Expected: ranks [0 0 0 1 2] — (2.5,4.5) is dominated by (2,4); (4,4.5) also by
# (2.5,4.5). Crowding on front 0: [inf 2.0 inf] (boundaries infinite, middle 1+1).
```

### End-to-end NSGA-II for a bi-objective permutation flow shop

The application minimizes (makespan, total flowtime) over job permutations — the standard bi-objective extension of the permutation flow shop (see flow-shop-scheduling for the single-objective toolkit this builds on). The block is self-contained: machinery, permutation operators, main loop, and a seeded demo.

```python
import numpy as np


def fast_nondominated_sort(F: np.ndarray) -> np.ndarray:
    """Front index per row of objective matrix F (minimization); 0 = best."""
    weak = (F[:, None, :] <= F[None, :, :]).all(axis=2)
    strict = (F[:, None, :] < F[None, :, :]).any(axis=2)
    dom = weak & strict
    counts = dom.sum(axis=0)
    ranks = np.full(len(F), -1, dtype=int)
    unassigned = np.ones(len(F), dtype=bool)
    r = 0
    while unassigned.any():
        front = unassigned & (counts == 0)
        ranks[front] = r
        counts = counts - dom[front].sum(axis=0)
        unassigned &= ~front
        r += 1
    return ranks


def crowding_distance(F: np.ndarray) -> np.ndarray:
    """Crowding distance of each row within one front (minimization)."""
    n, m = F.shape
    if n <= 2:
        return np.full(n, np.inf)
    d = np.zeros(n)
    for k in range(m):
        order = np.argsort(F[:, k], kind="stable")
        fk = F[order, k]
        d[order[0]] = d[order[-1]] = np.inf
        span = fk[-1] - fk[0]
        if span > 0:
            d[order[1:-1]] += (fk[2:] - fk[:-2]) / span
    return d


def nsga2_survival(F: np.ndarray, n_keep: int) -> np.ndarray:
    """Indices of the n_keep rows kept by rank-then-crowding truncation."""
    ranks = fast_nondominated_sort(F)
    keep: list[int] = []
    for r in range(ranks.max() + 1):
        idx = np.where(ranks == r)[0]
        if len(keep) + idx.size <= n_keep:
            keep.extend(idx.tolist())
        else:
            order = np.argsort(-crowding_distance(F[idx]), kind="stable")
            keep.extend(idx[order[: n_keep - len(keep)]].tolist())
            break
    return np.array(keep)


def crowded_tournament(ranks: np.ndarray, crowd: np.ndarray,
                       rng: np.random.Generator, n_draws: int) -> np.ndarray:
    """Binary tournament under the crowded-comparison operator; returns indices."""
    a = rng.integers(0, len(ranks), n_draws)
    b = rng.integers(0, len(ranks), n_draws)
    a_wins = (ranks[a] < ranks[b]) | ((ranks[a] == ranks[b]) & (crowd[a] > crowd[b]))
    return np.where(a_wins, a, b)


def evaluate_flowshop(perm: np.ndarray, proc: np.ndarray) -> tuple[float, float]:
    """(makespan, total flowtime) of permutation perm on proc[(n_jobs, n_machines)]."""
    p = proc[perm].astype(float)
    comp = np.zeros_like(p)
    comp[0] = np.cumsum(p[0])
    for j in range(1, p.shape[0]):
        comp[j, 0] = comp[j - 1, 0] + p[j, 0]
        for k in range(1, p.shape[1]):
            comp[j, k] = max(comp[j - 1, k], comp[j, k - 1]) + p[j, k]
    return comp[-1, -1], comp[:, -1].sum()


def order_crossover(p1: np.ndarray, p2: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """OX variant: copy a slice from p1, fill remaining positions in p2's order."""
    n = p1.size
    a, b = np.sort(rng.choice(n, size=2, replace=False))
    child = np.full(n, -1)
    child[a : b + 1] = p1[a : b + 1]
    child[child < 0] = p2[~np.isin(p2, p1[a : b + 1])]
    return child


def swap_mutation(perm: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Swap two random positions."""
    q = perm.copy()
    i, j = rng.choice(perm.size, size=2, replace=False)
    q[i], q[j] = q[j], q[i]
    return q


def nsga2_flowshop(proc: np.ndarray, pop_size: int = 60, n_gen: int = 150,
                   p_cx: float = 0.9, p_mut: float = 0.3,
                   seed: int = 0) -> tuple[np.ndarray, np.ndarray]:
    """NSGA-II minimizing (makespan, total flowtime). Returns (front F, permutations)."""
    rng = np.random.default_rng(seed)
    n = proc.shape[0]
    pop = np.array([rng.permutation(n) for _ in range(pop_size)])
    F = np.array([evaluate_flowshop(p, proc) for p in pop])
    for _ in range(n_gen):
        ranks = fast_nondominated_sort(F)
        crowd = np.zeros(pop_size)
        for r in np.unique(ranks):
            idx = np.where(ranks == r)[0]
            crowd[idx] = crowding_distance(F[idx])
        parents = crowded_tournament(ranks, crowd, rng, 2 * pop_size)
        kids = []
        for i in range(0, 2 * pop_size, 2):
            child = (order_crossover(pop[parents[i]], pop[parents[i + 1]], rng)
                     if rng.random() < p_cx else pop[parents[i]].copy())
            if rng.random() < p_mut:
                child = swap_mutation(child, rng)
            kids.append(child)
        Fk = np.array([evaluate_flowshop(p, proc) for p in kids])
        all_F, all_pop = np.vstack([F, Fk]), np.vstack([pop, np.array(kids)])
        keep = nsga2_survival(all_F, pop_size)
        pop, F = all_pop[keep], all_F[keep]
    best = fast_nondominated_sort(F) == 0
    _, uniq = np.unique(F[best].round(6), axis=0, return_index=True)
    return F[best][np.sort(uniq)], pop[best][np.sort(uniq)]


rng = np.random.default_rng(7)
proc = rng.integers(1, 20, size=(12, 4))          # 12 jobs, 4 machines
front, perms = nsga2_flowshop(proc, pop_size=48, n_gen=120, seed=7)
print(front[np.argsort(front[:, 0])])
# Expected: a small set (typically 3-10 points) of mutually nondominated
# (makespan, flowtime) pairs; the minimum-makespan end sits well below the
# average random permutation (roughly 10-20% better at this instance size).
```

### Parameter guidance

| Parameter | Typical range | Trade-off |
|---|---|---|
| Population size N | 50-200 (≥ 2× target front size) | spread and front capacity vs evaluations per generation |
| Generations G | from budget: G = evals / N | convergence depth vs wall-clock |
| Crossover prob. p_cx | 0.7-0.95 | recombination pressure vs pure survival of parents |
| Mutation prob. (per individual) | 0.1-0.4 (or 1/n per gene) | diversity and unsupported-region reach vs disruption |
| Tournament size | 2 (fixed in canonical NSGA-II) | larger sizes over-concentrate on front extremes |

## pymoo in Practice

Write your own NSGA-II to understand and control it; use pymoo when you need tested implementations of NSGA-II/III, MOEA/D, SMS-EMOA, reference-direction tooling, and indicators behind one API. The same flow-shop problem in pymoo:

```python
import numpy as np
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.problem import ElementwiseProblem
from pymoo.indicators.hv import HV
from pymoo.operators.crossover.ox import OrderCrossover
from pymoo.operators.mutation.inversion import InversionMutation
from pymoo.operators.sampling.rnd import PermutationRandomSampling
from pymoo.optimize import minimize


class BiObjectiveFlowShop(ElementwiseProblem):
    """Permutation flow shop minimizing (makespan, total flowtime)."""

    def __init__(self, proc: np.ndarray):
        self.proc = proc
        super().__init__(n_var=proc.shape[0], n_obj=2,
                         xl=0, xu=proc.shape[0] - 1, vtype=int)

    def _evaluate(self, x: np.ndarray, out: dict, *args, **kwargs) -> None:
        p = self.proc[x.astype(int)].astype(float)
        comp = np.zeros_like(p)
        comp[0] = np.cumsum(p[0])
        for j in range(1, p.shape[0]):
            comp[j, 0] = comp[j - 1, 0] + p[j, 0]
            for k in range(1, p.shape[1]):
                comp[j, k] = max(comp[j - 1, k], comp[j, k - 1]) + p[j, k]
        out["F"] = [comp[-1, -1], comp[:, -1].sum()]


rng = np.random.default_rng(7)
proc = rng.integers(1, 20, size=(12, 4))
algorithm = NSGA2(
    pop_size=48,
    sampling=PermutationRandomSampling(),
    crossover=OrderCrossover(),
    mutation=InversionMutation(),
    eliminate_duplicates=True,
)
res = minimize(BiObjectiveFlowShop(proc), algorithm, ("n_gen", 120),
               seed=7, verbose=False)

ideal, nadir = res.F.min(axis=0), res.F.max(axis=0)
span = np.where(nadir > ideal, nadir - ideal, 1.0)
hv = HV(ref_point=np.array([1.1, 1.1]))((res.F - ideal) / span)
print(len(res.F), round(float(hv), 3))
# Expected: a front of a few nondominated permutations and a normalized
# hypervolume around 1.0-1.2 (upper bound 1.21 for ref point (1.1, 1.1)).
```

pymoo notes worth knowing: `ElementwiseProblem` evaluates one solution per call (simple, slower) while `Problem` receives the whole population matrix (vectorize the evaluation there); constraints go in `out["G"]` with the convention `G <= 0` feasible, handled by constrained dominance; `res.X` holds the decision vectors aligned with `res.F`; `pymoo.indicators.igd.IGD` and `igd_plus.IGDPlus` take the reference front at construction. For real-valued problems the default SBX/polynomial-mutation operators apply, with the usual `eta` distribution indices.

## Quality Indicators: Hypervolume and IGD

Comparing front approximations needs set-quality indicators, not single-objective statistics.

- **Hypervolume (HV)** (Zitzler & Thiele 1999): the volume of objective space dominated by the front, bounded by a reference point $r$ that every front point must dominate. HV is strictly Pareto-compliant — if approximation A dominates B, HV(A) > HV(B). It rewards both convergence and spread, needs no known true front, but depends on $r$ and on normalization.
- **IGD**: mean distance from each point of a reference front $Z$ to its nearest approximation point. Cheap, intuitive, but *not* Pareto-compliant — a dominated front can score better. Prefer **IGD+** (Ishibuchi, Masuda, Tanigaki & Nojima 2015), which measures only the dominated-direction component and is weakly Pareto-compliant.
- Report HV (primary) plus IGD+ (when a reference front exists), with the normalization bounds and reference point stated explicitly. Standard protocol: normalize all fronts by the ideal/nadir of the pooled reference front, then use $r = (1.1, \dots, 1.1)$ (Ishibuchi et al. 2018 recommend a reference point slightly worse than the nadir).

```python
import numpy as np


def nondominated_mask(F: np.ndarray) -> np.ndarray:
    """Boolean mask of nondominated rows of F (minimization)."""
    weak = (F[:, None, :] <= F[None, :, :]).all(axis=2)
    strict = (F[:, None, :] < F[None, :, :]).any(axis=2)
    return ~(weak & strict).any(axis=0)


def normalize_front(F: np.ndarray, ideal: np.ndarray, nadir: np.ndarray) -> np.ndarray:
    """Scale objectives so the reference range [ideal, nadir] maps to [0, 1]."""
    span = np.where(nadir > ideal, nadir - ideal, 1.0)
    return (F - ideal) / span


def hypervolume_2d(F: np.ndarray, ref: np.ndarray) -> float:
    """Exact hypervolume of a 2-objective minimization front w.r.t. reference point."""
    A = F[(F < ref).all(axis=1)]              # only points that dominate ref count
    if A.size == 0:
        return 0.0
    A = A[nondominated_mask(A)]
    A = A[np.argsort(A[:, 0])]                # f1 ascending => f2 strictly descending
    x = np.append(A[:, 0], ref[0])
    return float(np.sum((x[1:] - x[:-1]) * (ref[1] - A[:, 1])))


def igd(Z: np.ndarray, A: np.ndarray) -> float:
    """Inverted generational distance from reference front Z to approximation A."""
    d = np.linalg.norm(Z[:, None, :] - A[None, :, :], axis=2)
    return float(d.min(axis=1).mean())


def igd_plus(Z: np.ndarray, A: np.ndarray) -> float:
    """IGD+ (Ishibuchi et al. 2015): only dominated-direction distance; minimization."""
    diff = np.maximum(A[None, :, :] - Z[:, None, :], 0.0)
    d = np.linalg.norm(diff, axis=2)
    return float(d.min(axis=1).mean())


Z = np.array([[1.0, 3.0], [2.0, 2.0], [3.0, 1.0]])      # reference front
A = np.array([[1.0, 3.0], [2.5, 2.5], [3.0, 1.0]])      # an approximation
ref = np.array([4.0, 4.0])
print(hypervolume_2d(Z, ref), hypervolume_2d(A, ref))
print(round(igd(Z, A), 4), round(igd_plus(Z, A), 4))
# Expected: HV(Z) = 6.0 > HV(A) = 5.25; IGD = IGD+ ≈ 0.2357 (only the middle
# reference point (2,2) is missed, by distance sqrt(0.5)/3). All indicators
# agree that A is slightly worse than Z.
```

For $M = 3$ use `moocore` or pymoo's `HV` (exact algorithms scale to small fronts); beyond $M \approx 5$ switch to Monte Carlo HV estimation and report the sampling error. When comparing stochastic algorithms, compute the indicator per seed, then test the per-seed indicator samples (Wilcoxon signed-rank across instances) — never pool fronts across seeds into one super-front for the comparison.

## Advanced Techniques

### Payoff tables and nadir estimation

Build the payoff table lexicographically: for each objective $k$, optimize $f_k$ first, then re-optimize the others subject to $f_k$ fixed at its optimum (Gurobi's hierarchical API does this in one call). Row minima give the exact ideal point. For $M = 2$ the table's off-diagonal entries give the exact nadir; for $M \ge 3$ they only bound it, and the true nadir can be strictly worse than every payoff-table entry. When normalization matters (it always does), widen the estimated nadir by 5-10% and freeze it for the whole experiment rather than re-estimating per run.

### AUGMECON2 and grids for three or more objectives

For $M = 3$, the epsilon sweep becomes a 2D grid over $(\varepsilon_2, \varepsilon_3)$. AUGMECON2 (Mavrotas & Florios 2013) accelerates it with two devices: the slack-augmented objective guarantees nondominated output per solve, and the *bypass coefficient* uses the surplus of the innermost constrained objective to skip grid points that would re-derive the same solution. Order the constrained objectives so the innermost has the largest range, and exploit early-exit: when a grid row becomes infeasible, all tighter bounds in that row are infeasible too.

### Many-objective scaling: NSGA-III, MOEA/D, SMS-EMOA

As $M$ grows past 3, the fraction of mutually nondominated solutions in a random population approaches 1, so rank-0 stops discriminating and crowding distance degenerates. NSGA-III (Deb & Jain 2014) replaces crowding with niching against a structured set of reference directions on the unit simplex; MOEA/D (Zhang & Li 2007) decomposes the problem into many scalarized neighbors solved cooperatively; SMS-EMOA (Beume, Naujoks & Emmerich 2007) selects by hypervolume contribution directly (expensive but well-aligned with the reporting metric). Practical rule: $M \le 3$ NSGA-II; $4 \le M \le 10$ NSGA-III or MOEA/D; for any $M$, reconsider whether some objectives are really constraints in disguise.

### Hybridizing exact and evolutionary front generation

The two families compose well. (a) Two-phase method (Ulungu & Teghem 1995): compute all supported points exactly by dichotomic weighted-sum search (Aneja & Nair 1979), then search the triangles between adjacent supported points for unsupported ones — by epsilon-constraint for exactness or by a seeded MOEA for speed. (b) Seed NSGA-II's initial population with scalarization optima (extremes plus a few interior weights); the front then anchors on provably efficient endpoints. (c) Use an NSGA-II front to warm-start the epsilon sweep: pass the nearest heuristic point as a MIP start for each grid point, which routinely halves exact-sweep runtimes on hard instances.

### Decision support on a computed front

A front is an input to a decision, not the decision. Two standard mechanical aids: **knee points** — points where accepting a small loss in one objective buys a large gain in another, found as maxima of distance to the extreme-point line (Branke et al. 2004) — and **pseudo-weights** (Deb 2001, *Multi-Objective Optimization using Evolutionary Algorithms*), which assign each front point the implicit weight vector it best answers:

```python
import numpy as np


def pseudo_weights(F: np.ndarray) -> np.ndarray:
    """Deb's pseudo-weights per front point (minimization): relative gain per objective."""
    ideal, nadir = F.min(axis=0), F.max(axis=0)
    span = np.where(nadir > ideal, nadir - ideal, 1.0)
    raw = (nadir - F) / span
    return raw / raw.sum(axis=1, keepdims=True)


def pick_by_weights(F: np.ndarray, target: np.ndarray) -> int:
    """Index of the front point whose pseudo-weights best match the target weights."""
    return int(np.argmin(np.linalg.norm(pseudo_weights(F) - target, axis=1)))


F = np.array([[1.0, 9.0], [3.0, 5.0], [4.0, 4.0], [8.0, 1.0]])
print(pick_by_weights(F, np.array([0.5, 0.5])))
# Expected: 2 — the (4, 4) point is the balanced compromise on this front.
```

Present stakeholders with 3-5 points: both extremes, the knee, and one or two pseudo-weight matches for stated preferences, each with its full objective vector in original units.

## Practical Challenges

**Objectives on different scales corrupt crowding and every indicator.** Cost in millions next to a count of late jobs makes crowding distance, hypervolume, and IGD effectively single-objective. Normalize with explicit ideal/nadir bounds, freeze those bounds across all algorithms and seeds of an experiment, and write them into the results table. Re-estimating bounds per run makes indicator values incomparable between runs even for the same algorithm.

**The weighted sum silently returns an incomplete front.** On MILPs, no weight vector reaches unsupported points, and evenly spaced weights cluster solutions where the convex hull is flat while leaving steep regions empty. If the deliverable is "the trade-off curve," the weighted sum alone is wrong by construction of the problem class — use the epsilon-constraint sweep, and keep the weighted sum for warm starts and supported-front sketches.

**Plain epsilon-constraint returns weakly efficient points.** When alternative optima exist at a given bound, the solver may return a point that another solution weakly dominates. Always augment: add $\delta \times$ (constrained objective or its slack) with $\delta$ around $10^{-6}$-$10^{-3}$ after scaling, or chain two lexicographic solves per grid point. Verify the final list with an independent dominance filter before reporting.

**An exact sweep with thousands of MILP solves blows the time budget.** Keep one persistent model and update only the epsilon RHS (preserves presolve and structure detection), set a per-solve `TimeLimit` with status logging, seed each solve with a MIP start from a cheap heuristic front, and thin the grid: an exact front of 2,000 points is rarely more useful than 100 well-spread exact points plus the guarantee that nothing between them is missed by more than the grid step.

**The hypervolume reference point quietly decides the winner.** A reference point chosen per algorithm (e.g., each run's own worst values) makes HV values incomparable and can reverse rankings. Protocol: pool all fronts of the whole experiment, extract the combined nondominated reference front, take its ideal/nadir for normalization, and use the shared reference point $(1.1, \dots, 1.1)$ in normalized space for every HV computation.

**The reported front is bloated with duplicates.** Permutation problems generate many genotypes with identical objective vectors; reporting all of them inflates cardinality without adding information. Deduplicate objective vectors for reporting (keep one representative solution each), but keep genotype-level duplicates under control inside the population too (pymoo's `eliminate_duplicates`, or a hash set of objective tuples) so crowding is not fooled by stacked copies.

**For M ≥ 3 everything becomes nondominated.** Front-0 membership approaches the whole population, selection pressure collapses, and the front itself has too many points to inspect. Switch to reference-direction methods (NSGA-III/MOEA/D), report a bounded epsilon-archive instead of the raw front, and re-examine with the stakeholder whether some objectives are constraints with negotiable bounds rather than true objectives.

**The stakeholder wants one solution, not two hundred.** Plan the reduction step from the start: extremes, knee point, pseudo-weight matches to stated preferences, and a table in original units. If priorities harden during that conversation, switch to a hierarchical solve (Gurobi `setObjectiveN`) and deliver one defensible solution with the front as context.

## Tools & Libraries

| Library | Use when | Note |
|---|---|---|
| pymoo | default Python MOEA library | NSGA-II/III, MOEA/D, SMS-EMOA, HV/IGD/IGD+ indicators, permutation operators |
| gurobipy | exact scalarization and front sweeps | epsilon-constraint loops; native multi-objective API is blended/hierarchical only — it returns one solution, never a front |
| DEAP | custom EA loops needing full control | `selNSGA2` and tools primitives; more wiring than pymoo |
| jMetalPy | algorithm-research experiments | broad MOEA zoo, quality indicators, experiment harness |
| Platypus | quick NSGA-II/III baselines | compact API, fewer operators and indicators |
| pygmo | parallel archipelago runs | C++ speed, NSGA-II/MOEA/D, batch fitness islands |
| moocore | indicator computation at scale | fast exact hypervolume for M ≥ 3, EAF/attainment tools |
| scipy | distance work inside custom indicators | `spatial.distance.cdist` or KDTree for large reference sets |

## Output Format

A complete multi-objective deliverable contains:

1. **Setup summary table** — objectives with units and senses, method(s), instance(s), budgets (time limit per MILP solve, or population × generations), seeds, normalization bounds (ideal/nadir used), HV reference point.
2. **Front artifact** — one tidy CSV per (instance, method): one row per reported nondominated point.

| column | meaning |
|---|---|
| instance | instance identifier |
| method | e.g. `eps-constraint`, `nsga2-s7` |
| point_id | index within the front, sorted by f1 |
| f1, f2, ... | objective values in original units |
| status | per-solve Gurobi status, or `heuristic` |
| gap | MIP gap if time-limited, else 0.0 |
| solution | decision-vector reference (file or encoding) |

3. **Indicator report** — for each method: front cardinality, normalized HV, IGD+ against the reference front; mean ± std over seeds for stochastic methods, with the statistical test named when methods are compared.
4. **Plots** — 2D front scatter with all methods overlaid plus the reference front; HV-versus-evaluations convergence curve with a band over seeds; parallel-coordinates plot for M ≥ 4 (construction details in matplotlib-optimization-visualization).
5. **Decision shortlist** — 3-5 representative points (extremes, knee, pseudo-weight matches) with full objective vectors in original units and one-line interpretations.
6. **Reproducibility note** — seeds, solver versions and parameters, normalization bounds, and the exact command or script that regenerates every table and figure.

State explicitly whether the front is exact (and under what tolerance — `MIPGap`, integer objectives, grid step) or an approximation, and never present time-limited sweep points as proven nondominated.

## Questions to Ask

- How many objectives are there, and is each pair genuinely conflicting on sampled solutions?
- Do you need the whole trade-off curve, or one solution under known priorities or aspiration levels?
- Is the problem an explicit MILP that Gurobi can scalarize and solve repeatedly, or a black-box evaluation?
- Are the objective functions integer-valued (enables a provably complete epsilon sweep)?
- What are the units and plausible ranges of each objective, for normalization and nadir bounds?
- What is the total compute budget — per-solve time limits for exact sweeps, or an evaluation budget for MOEAs?
- Will results be compared across algorithms or papers — which reference front, seeds, and indicator protocol?
- Who makes the final choice from the front, and what selection aid (knee, pseudo-weights, workshop) do they need?

## Related Skills

- **selection-and-replacement-strategies** — when tuning the selection pressure feeding NSGA-II's crowded tournament, or replacing its survival scheme with another elitist strategy.
- **flow-shop-scheduling** — when the bi-objective flow-shop application here needs the single-objective toolkit underneath: NEH construction, iterated greedy, Taillard instances.
- **matplotlib-optimization-visualization** — when Pareto scatter plots, attainment overlays, and HV convergence curves must reach publication quality.
- **genetic-algorithms** — when the underlying GA machinery (encodings, crossover/mutation operators, population sizing) needs more depth than NSGA-II's ranking layer adds.
- **milp-modeling-gurobi** — when the scalarized subproblems themselves need careful MILP construction, named constraints, parameter control, and status handling.
