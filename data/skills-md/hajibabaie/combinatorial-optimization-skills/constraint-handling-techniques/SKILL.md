---
name: constraint-handling-techniques
description: When the user wants to handle constraints inside metaheuristics by choosing among penalty functions (static, dynamic, adaptive), repair operators, feasibility-preserving operators, decoder-based feasibility, stochastic ranking, and Deb's feasibility rules. Also use when the user mentions "constraint handling," "penalty function," "repair operator," "infeasible solutions," "feasibility rules," "adaptive penalty," or when a metaheuristic keeps returning infeasible solutions. For representation choice, see solution-encodings; for feasibility-enforcing decoders, see decoder-based-representations.
---

# Constraint-Handling Techniques

You are an expert in constraint handling for metaheuristics and evolutionary computation. This skill catalogs the six main technique families — penalty functions (static, dynamic, adaptive), repair operators, feasibility-preserving operators, decoder-based feasibility, stochastic ranking, and Deb's feasibility rules — with numpy implementations, complexity notes, and per-constraint-type selection guidance. Use the framework below to pick a technique per constraint, implement it correctly, and verify the choice empirically with a head-to-head experiment.

## Initial Assessment

Establish these facts before recommending any technique:

- **Constraint inventory.** List every constraint. For each: inequality or equality? Linear or black-box? How many?
- **Hard vs soft.** Hard constraints define feasibility; soft constraints are preferences. Soft constraints belong in the objective (weighted or lexicographic), never in a feasibility mechanism. Confirm the user agrees on the split.
- **Feasible-region density.** Sample random solutions: what fraction is feasible? Above ~10%, penalties and feasibility rules work out of the box. Below ~0.1%, you need repair, decoders, or feasibility-preserving operators — random search will never find the feasible region.
- **Constraint structure.** Is feasibility cheap to check (O(n) capacity sums) or expensive (a simulation)? Cheap checks enable repair and move filtering; expensive checks favor penalties on cached violation values.
- **Representation already chosen?** If the encoding is still open, the cheapest fix is to encode constraints away (permutation encoding for "visit each once", fixed-cardinality sets for "choose exactly k"). See solution-encodings before adding machinery here.
- **Algorithm family.** Population methods (GA, DE, EDA) can rank by violation across a population; single-solution methods (SA, tabu, ILS) need per-move decisions — repair, move filtering, or a penalized delta.
- **Equality constraints present?** Penalties handle equalities poorly (the feasible set has measure zero). Plan for reformulation, decoders, or projection-style repair.
- **Where does the optimum live?** For most resource-constrained problems the optimum sits on the feasibility boundary (Michalewicz & Schoenauer 1996). Techniques that cannot search near or across the boundary lose quality.
- **Evaluation budget and time limit.** Repair and decoding add per-individual cost; confirm the budget tolerates it.
- **Validation hook.** Confirm an independent feasibility checker exists (separate from the fitness code) so the chosen technique can be audited — see solution-validation-testing.

## Technique Taxonomy and Selection

The constrained combinatorial problem, in minimization form:

$$
\min_{x \in S} f(x) \quad \text{s.t.} \quad g_j(x) \le 0 \;(j = 1,\dots,m), \qquad h_k(x) = 0 \;(k = 1,\dots,p),
$$

where $S$ is the space reachable by the representation. Define per-constraint violations

$$
v_j(x) = \max(0,\, g_j(x)), \qquad v_{m+k}(x) = \max(0,\, |h_k(x)| - \varepsilon),
$$

with a tolerance $\varepsilon > 0$ for equalities, and the scalar total violation

$$
\phi(x) = \sum_j \left( \frac{v_j(x)}{s_j} \right)^{\beta},
$$

where $s_j$ is a per-constraint scale (typical: the constraint's right-hand side or a sampled violation quantile) and $\beta \in \{1, 2\}$. Every technique below is a different way to use $f$ and $\phi$ (or to avoid ever creating $\phi > 0$).

Six families (Coello 2002, "Theoretical and numerical constraint-handling techniques used with evolutionary algorithms"; Mezura-Montes & Coello 2011 survey):

1. **Penalty functions** — optimize $F(x) = f(x) + \rho \cdot \phi(x)$. Static $\rho$, time-dependent $\rho(t)$, or population-adaptive $\rho$.
2. **Feasibility rules (Deb 2000)** — never aggregate: compare solutions lexicographically by $(\phi, f)$.
3. **Stochastic ranking (Runarsson & Yao 2000)** — probabilistic balance between $f$-comparisons and $\phi$-comparisons during sorting.
4. **Repair operators** — map infeasible solutions to feasible ones after variation.
5. **Decoder-based feasibility** — the genotype-to-phenotype mapping only produces feasible solutions.
6. **Feasibility-preserving operators** — variation moves are filtered or designed so feasible parents always yield feasible offspring.

### Technique comparison

| Technique | Tuning burden | Offspring always feasible | Searches infeasible region | Extra cost per evaluation | Main failure mode |
|---|---|---|---|---|---|
| Static penalty | High ($\rho$, $\beta$) | No | Yes | $O(m)$ | $\rho$ too low → infeasible winner; too high → stuck at boundary |
| Dynamic penalty | Medium ($C$, $\alpha$) | No (late: nearly) | Yes, early | $O(m)$ | Schedule mismatched to evaluation budget |
| Adaptive penalty (APM, Bean–Hadj-Alouane) | Low to none | No | Yes | $O(\text{pop} \cdot m)$ per generation | Coefficient oscillation on noisy populations |
| Deb feasibility rules | None | No | Barely | $O(m)$ | Diversity collapse onto first feasible basin |
| Stochastic ranking | Low ($P_f \approx 0.45$) | No | Controlled | $O(\text{pop} \cdot \text{sweeps})$ per ranking | Sensitive $P_f$ on very tight problems |
| Repair | Design effort | Yes (after repair) | Variation yes, evaluation no | Repair routine cost | Repair bias: offspring cluster on repair targets |
| Decoder | Design effort | Yes | No | Decode cost per individual | Locality loss, genotype redundancy |
| Feasibility-preserving operators | Design effort | Yes | No | Move feasibility check | Feasible region disconnected under the move set |

### Choosing per constraint type

| Constraint type | Example | First choice | Second choice |
|---|---|---|---|
| Representation-level (each-exactly-once, cardinality $=k$) | TSP tour, choose $k$ medians | Encode it away (permutation / fixed-size set) | Feasibility-preserving operators |
| Single resource budget | 0-1 knapsack capacity | Greedy repair (Chu & Beasley 1998) | Calibrated static penalty |
| Several resource budgets | Multidimensional knapsack, GAP | Repair + Deb rules for ranking | Adaptive penalty (APM) |
| Coupling / equality | Flow balance, demand = supply | Decoder or reformulate variables out | Projection-style repair |
| Sparse feasible region (<0.1% feasible) | Tight scheduling with time windows | Decoder (e.g., schedule-generation scheme) | Repair + feasibility-preserving moves |
| Black-box inequality | Simulation output limit | Stochastic ranking or $\varepsilon$-constrained | Deb rules |
| Soft constraints | Preferred shifts, balance goals | Weighted objective term (not a feasibility issue) | Lexicographic objectives |

Decision shortcuts:

- Use **penalties** when violations are cheap to compute, graded (a little violation is meaningfully better than a lot), and the feasible region is reasonably dense.
- Use **Deb rules or stochastic ranking** when you refuse to tune $\rho$; prefer stochastic ranking when optima lie on the boundary and pure feasibility-first stalls.
- Use **repair** when a cheap greedy mapping from infeasible to feasible exists — resource budgets almost always have one.
- Use **decoders** when feasibility is hard to restore but easy to construct incrementally (scheduling, packing); see decoder-based-representations for full decoder design.
- Use **feasibility-preserving operators** in single-solution methods (SA, tabu, ILS) where each move can be checked in O(1)–O(n) — then the question of infeasibility never arises.
- Combining is normal: repair for capacity + permutation encoding for sequencing + penalty for a soft balance term in one algorithm.

## Penalty Function Catalog

Shared infrastructure: compute violations for a whole population at once. Keep violation computation separate from the objective so every technique below can reuse it.

```python
import numpy as np


def violation_matrix(G: np.ndarray) -> np.ndarray:
    """Elementwise inequality violations max(0, g_j(x)) for a batch.

    G: (pop, m) constraint values with the convention feasible <=> g_j <= 0.
    """
    return np.maximum(G, 0.0)


def total_violation(
    G: np.ndarray, scale: np.ndarray | None = None, beta: float = 1.0
) -> np.ndarray:
    """Scalar violation per individual: sum_j (v_j / s_j)^beta."""
    V = np.maximum(G, 0.0)
    if scale is not None:
        V = V / scale
    return (V**beta).sum(axis=1)


# Tiny instance: 3 individuals, 2 constraints (g <= 0 feasible)
G = np.array([[-1.0, -2.0], [0.5, -1.0], [2.0, 1.0]])
print(total_violation(G))
# Expected: [0.  0.5 3. ] -- row 0 feasible, row 2 violates both constraints
```

**Complexity.** $O(\text{pop} \cdot m)$; trivially vectorized. **Fits.** Every technique in this skill consumes these arrays.

### Static penalty

**When to use.** Constraint scales are known, violations are graded, and you can afford a short calibration study for $\rho$. The classic default — and the most common silent failure when $\rho$ is guessed.

```python
import numpy as np


def static_penalty(
    f: np.ndarray, G: np.ndarray, rho: float, beta: float = 2.0
) -> np.ndarray:
    """Penalized objective F = f + rho * sum_j max(0, g_j)^beta (minimization)."""
    V = np.maximum(G, 0.0)
    return f + rho * (V**beta).sum(axis=1)


def calibrate_rho(
    f_sample: np.ndarray, G_sample: np.ndarray, margin: float = 2.0
) -> float:
    """Set rho from a random sample so typical violations outweigh the f range.

    Rule: rho = margin * (objective range) / (mean violation of infeasible samples).
    """
    V = np.maximum(G_sample, 0.0).sum(axis=1)
    infeasible = V > 0
    if not infeasible.any():
        return 1.0
    f_range = float(f_sample.max() - f_sample.min()) + 1e-12
    return margin * f_range / float(V[infeasible].mean())


f = np.array([100.0, 90.0, 80.0])
G = np.array([[0.0, 0.0], [2.0, 0.0], [3.0, 1.0]])
print(static_penalty(f, G, rho=10.0))
# Expected: [100. 130. 180.] -- the feasible solution now ranks first
```

**Complexity.** $O(\text{pop} \cdot m)$ per generation. **Fits.** Any algorithm; the only option when the algorithm needs one scalar fitness (e.g., roulette selection, SA acceptance on deltas). Theory note: for linearly constrained problems an exact penalty exists once $\rho$ exceeds the largest dual multiplier, but in metaheuristics $\rho$ is a search-control parameter, not just a correctness parameter — too-large $\rho$ makes all infeasible solutions equally hopeless and freezes the search at the feasibility boundary.

### Dynamic and annealing penalties

**When to use.** You want early exploration through infeasible space and late feasibility pressure, and you know the total generation budget (the schedule must be tied to it).

```python
import numpy as np


def dynamic_penalty(
    f: np.ndarray,
    G: np.ndarray,
    t: int,
    C: float = 0.5,
    alpha: float = 2.0,
    beta: float = 2.0,
) -> np.ndarray:
    """Joines & Houck (1994): F = f + (C*t)^alpha * sum_j v_j^beta, t = generation >= 1."""
    V = np.maximum(G, 0.0)
    return f + (C * t) ** alpha * (V**beta).sum(axis=1)


def annealing_penalty(
    f: np.ndarray, G: np.ndarray, tau: float, beta: float = 2.0
) -> np.ndarray:
    """Michalewicz & Attia (1994): F = f + sum_j v_j^beta / (2*tau), tau cooled toward 0."""
    V = np.maximum(G, 0.0)
    return f + (V**beta).sum(axis=1) / (2.0 * tau)


f = np.array([10.0, 9.0])  # second solution is better on f ...
G = np.array([[0.0], [1.0]])  # ... but violates the constraint by 1
for t in (1, 10, 50):
    print(t, dynamic_penalty(f, G, t))
# Expected: at t=1 the infeasible point still wins (9.25 < 10.0);
# at t=10 the penalty dominates (34.0 > 10.0) and the feasible point wins
```

**Complexity.** Same as static per generation. **Fits.** Population methods with a fixed generation budget; SA (annealing penalty pairs naturally with the SA temperature). Pitfall: with $(Ct)^{\alpha}$ and $\alpha = 2$, pressure grows quadratically — if the budget doubles, the schedule must be re-tuned or the run spends most generations in the effectively-static high-penalty regime.

### Adaptive penalties: Bean–Hadj-Alouane and APM

**When to use.** You cannot calibrate $\rho$ offline, instance scales vary, or feasibility difficulty changes during the run. Adaptive schemes read the population and set coefficients automatically.

```python
import numpy as np


class PenaltyController:
    """Bean & Hadj-Alouane (1992): multiply/divide rho from recent best-individual feasibility.

    If the generation-best was feasible for `window` straight generations, rho /= factor
    (relax, search the boundary); if infeasible for `window` straight, rho *= factor.
    """

    def __init__(self, rho: float = 1.0, factor: float = 2.0, window: int = 5):
        self.rho = rho
        self.factor = factor
        self.window = window
        self.history: list[bool] = []

    def update(self, best_is_feasible: bool) -> float:
        """Record this generation's best-individual feasibility; return updated rho."""
        self.history.append(best_is_feasible)
        recent = self.history[-self.window :]
        if len(recent) == self.window:
            if all(recent):
                self.rho /= self.factor
            elif not any(recent):
                self.rho *= self.factor
        return self.rho


def apm_fitness(f: np.ndarray, G: np.ndarray) -> np.ndarray:
    """Adaptive Penalty Method, Barbosa & Lemonge (2003): parameter-free coefficients.

    k_j = |mean f| * mean(v_j) / sum_l mean(v_l)^2, recomputed every generation.
    Infeasible solutions with f below the population mean are first lifted to the mean.
    """
    V = np.maximum(G, 0.0)
    f_mean = float(f.mean())
    v_mean = V.mean(axis=0)
    denom = float((v_mean**2).sum())
    if denom == 0.0:  # fully feasible population: no penalty needed
        return f.copy()
    k = abs(f_mean) * v_mean / denom
    lifted = np.where(f > f_mean, f, f_mean)
    feasible = V.sum(axis=1) == 0
    return np.where(feasible, f, lifted + V @ k)


f = np.array([5.0, 3.0, 7.0, 4.0])
G = np.array([[0.0], [2.0], [0.0], [1.0]])
print(np.round(apm_fitness(f, G), 2))
# Expected: [ 5.   17.42  7.   11.08] -- feasible kept, infeasible pushed past mean f
```

**Complexity.** APM adds $O(\text{pop} \cdot m)$ statistics per generation. **Fits.** GAs and DE on problems with several heterogeneous constraints; APM also self-scales across constraints, which removes the manual $s_j$ choice. Pitfall: both schemes assume the population statistics are meaningful — with tiny populations (under ~20) the coefficients oscillate; smooth them with an exponential moving average.

## Ranking, Repair, and Construction-Based Techniques

### Deb's feasibility rules

**When to use.** Default parameter-free choice for population methods. Three rules (Deb 2000, "An efficient constraint handling method for genetic algorithms"): feasible beats infeasible; two feasible compare on $f$; two infeasible compare on total violation $\phi$. Equivalent to lexicographic order on $(\phi, f)$ — no penalty coefficient exists at all.

```python
import numpy as np


def deb_rank(f: np.ndarray, v: np.ndarray) -> np.ndarray:
    """Indices best-first under Deb (2000): sort by (total violation, objective)."""
    return np.lexsort((f, v))


def deb_tournament(
    f: np.ndarray, v: np.ndarray, n_offspring: int, rng: np.random.Generator
) -> np.ndarray:
    """Vectorized binary tournament under the feasibility rules; returns winner indices."""
    n = len(f)
    a = rng.integers(n, size=n_offspring)
    b = rng.integers(n, size=n_offspring)
    a_wins = (v[a] < v[b]) | ((v[a] == v[b]) & (f[a] <= f[b]))
    return np.where(a_wins, a, b)


f = np.array([10.0, 5.0, 8.0])
v = np.array([0.0, 2.0, 0.0])
print(deb_rank(f, v))
# Expected: [2 0 1] -- feasible solutions ordered by f, infeasible one last
rng = np.random.default_rng(7)
print(deb_tournament(f, v, 5, rng))
# Expected: winners drawn only from indices {0, 2} unless both entrants are index 1
```

**Complexity.** $O(\text{pop} \log \text{pop})$ to rank, $O(1)$ per tournament comparison. **Fits.** Any selection-based method; the standard inside NSGA-II's constrained dominance. Weakness: feasibility pressure is absolute, so the population collapses into the first feasible basin found — pair with strong diversity preservation when the feasible region is fragmented.

### Stochastic ranking

**When to use.** Optima on the feasibility boundary, where Deb's rules are too greedy. Stochastic ranking (Runarsson & Yao 2000, "Stochastic ranking for constrained evolutionary optimization") sorts the population with a stochastic bubble sort: when at least one of an adjacent pair is infeasible, compare on $f$ with probability $P_f$ and on $\phi$ otherwise. $P_f < 0.5$ keeps net pressure toward feasibility while letting good infeasible solutions survive near the boundary.

```python
import numpy as np


def stochastic_ranking(
    f: np.ndarray,
    v: np.ndarray,
    p_f: float = 0.45,
    sweeps: int | None = None,
    rng: np.random.Generator | None = None,
) -> np.ndarray:
    """Runarsson & Yao (2000): index array best-first via stochastic bubble sort.

    The sort is inherently sequential; sweeps default to the population size.
    """
    rng = np.random.default_rng() if rng is None else rng
    n = len(f)
    sweeps = n if sweeps is None else sweeps
    idx = np.arange(n)
    for _ in range(sweeps):
        u = rng.random(n - 1)
        swapped = False
        for i in range(n - 1):
            a, b = idx[i], idx[i + 1]
            both_feasible = v[a] == 0.0 and v[b] == 0.0
            compare_on_f = both_feasible or u[i] < p_f
            out_of_order = (f[a] > f[b]) if compare_on_f else (v[a] > v[b])
            if out_of_order:
                idx[i], idx[i + 1] = b, a
                swapped = True
        if not swapped:
            break
    return idx


f = np.array([1.0, 2.0, 3.0, 4.0])
v = np.array([5.0, 0.0, 0.0, 1.0])
rng = np.random.default_rng(0)
print(stochastic_ranking(f, v, p_f=0.0, rng=rng))  # pure feasibility-first
print(stochastic_ranking(f, v, p_f=1.0, rng=rng))  # pure objective order
# Expected: [1 2 3 0] for p_f=0.0 and [0 1 2 3] for p_f=1.0; p_f=0.45 interpolates
```

**Complexity.** $O(\text{pop}^2)$ worst case per ranking (bubble sort), fine for populations up to a few thousand. **Fits.** $(\mu, \lambda)$ evolution strategies (its original home), GAs with rank-based selection. Tuning: $P_f \in [0.4, 0.475]$; $P_f \ge 0.5$ loses the feasibility guarantee in expectation.

### Repair operators

**When to use.** A cheap greedy map from infeasible to feasible exists. For budget constraints this is the empirical winner — on multidimensional knapsack, repair-based GAs dominate penalty GAs (Chu & Beasley 1998, "A genetic algorithm for the multidimensional knapsack problem").

```python
import numpy as np


def repair_knapsack(
    X: np.ndarray, w: np.ndarray, p: np.ndarray, cap: float
) -> np.ndarray:
    """Greedy DROP/ADD repair for 0-1 knapsack populations (Chu & Beasley 1998).

    DROP: remove worst profit/weight items until the load fits.
    ADD:  insert best-ratio missing items that still fit (also improves feasible rows).
    Returns a repaired copy; X is (pop, n) with 0/1 entries.
    """
    X = X.copy()
    ratio = p / w
    drop_order = np.argsort(ratio)  # worst ratio first
    add_order = drop_order[::-1]  # best ratio first
    load = X @ w
    for i in np.flatnonzero(load > cap):
        for j in drop_order:
            if X[i, j]:
                X[i, j] = 0
                load[i] -= w[j]
                if load[i] <= cap:
                    break
    for i in range(X.shape[0]):
        for j in add_order:
            if not X[i, j] and load[i] + w[j] <= cap:
                X[i, j] = 1
                load[i] += w[j]
    return X


w = np.array([4.0, 3.0, 2.0, 5.0])
p = np.array([8.0, 7.0, 3.0, 5.0])
X = np.array([[1, 1, 1, 1]], dtype=np.int8)
print(repair_knapsack(X, w, p, cap=7.0))
# Expected: [[1 1 0 0]] -- drops items 3 and 2 (worst ratios), keeps load 7 <= 7
```

**Complexity.** $O(n \log n)$ sort once plus $O(n)$ per repaired individual. **Fits.** Binary GAs, EDAs, ALNS repair phases; any budget/cover constraint with a natural greedy. Two write-back policies: **Lamarckian** (repaired genotype replaces the original — faster convergence, standard for combinatorial problems) vs **Baldwinian** (evaluate the repaired phenotype but keep the original genotype — preserves diversity); see Advanced Techniques.

### Decoder-based feasibility

**When to use.** Feasibility is hard to restore but easy to build constructively. The genotype orders or prioritizes decisions; a greedy decoder makes only feasible choices, so infeasible phenotypes cannot exist. Full design treatment in decoder-based-representations.

```python
import numpy as np


def decode_keys_knapsack(
    K: np.ndarray, w: np.ndarray, cap: float
) -> np.ndarray:
    """Random-key decoder for 0-1 knapsack: every genotype maps to a feasible solution.

    Items are considered in decreasing key order and inserted while they fit.
    K: (pop, n) real-valued keys in [0, 1).
    """
    pop, n = K.shape
    order = np.argsort(-K, axis=1)
    X = np.zeros((pop, n), dtype=np.int8)
    for r in range(pop):
        load = 0.0
        for j in order[r]:
            if load + w[j] <= cap:
                X[r, j] = 1
                load += w[j]
    return X


w = np.array([4.0, 3.0, 2.0, 5.0])
K = np.array([[0.9, 0.5, 0.8, 0.1]])
print(decode_keys_knapsack(K, w, cap=7.0))
# Expected: [[1 0 1 0]] -- key order 0,2,1,3; items 0 and 2 fit (load 6), 1 and 3 do not
```

**Complexity.** $O(n \log n)$ per individual (the sort dominates). **Fits.** BRKGA natively; PSO/DE on combinatorial problems via random keys; scheduling through serial/parallel schedule-generation schemes. Cost: decoder redundancy (many genotypes, one phenotype) and weaker locality — small key changes can flip the whole insertion order.

### Feasibility-preserving operators

**When to use.** Single-solution methods (SA, tabu, ILS, VNS) and any setting where checking a move's feasibility is cheap. Design or filter moves so a feasible solution can only become another feasible solution; the algorithm then never spends evaluations outside the feasible region. Requirement: the feasible region must stay **connected** under the move set, or the search gets trapped in a feasible component that excludes the optimum. The second worked example below implements this technique end to end.

### Catalog cross-reference: technique × algorithm fit

| Technique | GA / EDA | SA / tabu / ILS | DE / PSO (keys) | ALNS | Notes |
|---|---|---|---|---|---|
| Static / dynamic penalty | Good | Good (delta-friendly) | Good | Rarely needed | One scalar fitness; SA deltas stay O(move) |
| Adaptive penalty (APM) | Good | Poor (no population stats) | Good | No | Needs population statistics |
| Deb rules | Good | Via better-of-two acceptance | Good | Acceptance test | No parameters |
| Stochastic ranking | Good (rank selection) | No | Good (ES origin) | No | Needs a ranking step |
| Repair | Good | As move post-processing | On decoded phenotype | Core (repair = insertion) | Lamarckian write-back standard |
| Decoder | Good (BRKGA) | Indirect neighborhoods | Core enabler | No | Moves act on genotype space |
| Feasibility-preserving ops | Crossover is hard to preserve | Core | No | Destroy keeps partial feasibility | Check connectivity |

## Worked Example: Knapsack — Penalty vs Repair Head-to-Head

The canonical experiment: one binary GA, two constraint-handling modes, identical budget and seeds, exact DP optimum as the reference. This protocol generalizes — when two techniques are candidates, run them head-to-head before committing (see knapsack-problems for the problem family itself).

```python
import numpy as np


def make_knapsack(n: int, seed: int) -> tuple[np.ndarray, np.ndarray, float]:
    """Weakly correlated 0-1 knapsack; capacity = half the total weight."""
    rng = np.random.default_rng(seed)
    w = rng.integers(10, 100, size=n).astype(float)
    p = np.maximum(w + rng.integers(-10, 30, size=n), 1.0)
    return w, p, 0.5 * float(w.sum())


def dp_optimum(w: np.ndarray, p: np.ndarray, cap: float) -> float:
    """Exact 0-1 knapsack DP over integer capacities (reference optimum)."""
    best = np.zeros(int(cap) + 1)
    for wi, pi in zip(w.astype(int), p):
        best[wi:] = np.maximum(best[wi:], best[:-wi] + pi)
    return float(best[-1])


def repair(X: np.ndarray, w: np.ndarray, p: np.ndarray, cap: float) -> np.ndarray:
    """Greedy DROP/ADD repair (Chu & Beasley 1998) for a 0/1 population matrix."""
    X = X.copy()
    drop_order = np.argsort(p / w)
    add_order = drop_order[::-1]
    load = X @ w
    for i in np.flatnonzero(load > cap):
        for j in drop_order:
            if X[i, j]:
                X[i, j] = 0
                load[i] -= w[j]
                if load[i] <= cap:
                    break
    for i in range(X.shape[0]):
        for j in add_order:
            if not X[i, j] and load[i] + w[j] <= cap:
                X[i, j] = 1
                load[i] += w[j]
    return X


def knapsack_ga(
    w: np.ndarray,
    p: np.ndarray,
    cap: float,
    mode: str,
    pop_size: int = 100,
    gens: int = 200,
    seed: int = 0,
) -> float:
    """Binary GA; mode is 'penalty' (rho = 2 * max profit/weight) or 'repair'.

    Returns the best FEASIBLE profit found (the only fair comparison metric).
    """
    rng = np.random.default_rng(seed)
    n = len(w)
    rho = 2.0 * float((p / w).max())
    X = (rng.random((pop_size, n)) < 0.3).astype(np.int8)
    if mode == "repair":
        X = repair(X, w, p, cap)
    best = 0.0
    for _ in range(gens):
        load, profit = X @ w, (X @ p).astype(float)
        fit = profit - rho * np.maximum(load - cap, 0.0) if mode == "penalty" else profit
        feasible = load <= cap
        if feasible.any():
            best = max(best, float(profit[feasible].max()))
        a = rng.integers(pop_size, size=pop_size)
        b = rng.integers(pop_size, size=pop_size)
        parents = np.where((fit[a] >= fit[b])[:, None], X[a], X[b])
        mask = rng.random((pop_size // 2, n)) < 0.5
        kids = np.vstack(
            [
                np.where(mask, parents[0::2], parents[1::2]),
                np.where(mask, parents[1::2], parents[0::2]),
            ]
        )
        flip = rng.random((pop_size, n)) < 1.0 / n
        kids = np.where(flip, 1 - kids, kids).astype(np.int8)
        if mode == "repair":
            kids = repair(kids, w, p, cap)
        kids[0] = X[np.argmax(fit)]  # elitism
        X = kids
    return best


w, p, cap = make_knapsack(50, seed=42)
opt = dp_optimum(w, p, cap)
for mode in ("penalty", "repair"):
    res = knapsack_ga(w, p, cap, mode, seed=1)
    print(f"{mode:8s} best={res:7.0f}  gap={(opt - res) / opt:6.2%}")
print(f"DP optimum = {opt:.0f}")
# Expected: repair best=1955 (gap 0.05%), penalty best=1947 (gap 0.46%),
# DP optimum 1956. The repair GA wins and converges in fewer generations: every
# evaluation is spent on a feasible point and ADD acts as a built-in local improver.
```

Reading the result correctly: the repair GA wins here because the knapsack greedy is near-optimal repair. The honest report states the comparison metric (best feasible), identical budgets, and multiple seeds — single-seed wins are noise. With $\rho = 2 \max_j p_j / w_j$ the penalty is provably strong enough that dropping overweight items always pays, yet the penalty GA still trails: penalties waste evaluations ranking infeasible solutions against each other.

## Worked Example: Capacitated Assignment with Feasibility-Preserving Operators

Capacitated assignment: $n$ jobs with weights $w_j$, $m$ machines with capacities $b_i$, machine-dependent cost $c_{ij}$; minimize total cost subject to $\sum_{j: a_j = i} w_j \le b_i$ for every machine $i$. The move set — **shift** (reassign one job) and **swap** (exchange two jobs' machines) — is filtered so capacity feasibility is invariant: the search starts feasible and stays feasible at every step.

```python
import numpy as np


def make_instance(
    n_jobs: int, n_mach: int, seed: int
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Random capacitated-assignment instance with ~25% slack capacity."""
    rng = np.random.default_rng(seed)
    cost = rng.uniform(1.0, 20.0, size=(n_mach, n_jobs))
    w = rng.uniform(5.0, 25.0, size=n_jobs)
    cap = np.full(n_mach, 1.25 * w.sum() / n_mach)
    return cost, w, cap


def greedy_start(
    cost: np.ndarray, w: np.ndarray, cap: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """Feasible construction: heaviest job first onto the cheapest machine with room."""
    n_mach, n_jobs = cost.shape
    assign = np.full(n_jobs, -1)
    load = np.zeros(n_mach)
    for j in np.argsort(-w):
        for i in np.argsort(cost[:, j]):
            if load[i] + w[j] <= cap[i]:
                assign[j], load[i] = i, load[i] + w[j]
                break
        if assign[j] < 0:
            raise ValueError("greedy failed; instance too tight for this constructor")
    return assign, load


def descend(
    assign: np.ndarray, load: np.ndarray, cost: np.ndarray, w: np.ndarray, cap: np.ndarray
) -> None:
    """Best-improvement descent over feasibility-preserving shifts and swaps (in place)."""
    n_mach, n_jobs = cost.shape
    jobs = np.arange(n_jobs)
    while True:
        cur = cost[assign, jobs]
        # Shift deltas (machine i, job j); infeasible/no-op targets masked out.
        fits = (load[:, None] + w[None, :]) <= cap[:, None] + 1e-9
        fits[assign, jobs] = False
        d_shift = np.where(fits, cost - cur[None, :], np.inf)
        si, sj = np.unravel_index(np.argmin(d_shift), d_shift.shape)
        # Swap deltas (jobs j, k); M[j, k] = cost of job j on job k's machine.
        M = cost[assign[None, :], jobs[:, None]]
        d_swap = M + M.T - cur[:, None] - cur[None, :]
        head = cap[assign] - load[assign]  # free space on each job's machine
        ok = (
            (assign[:, None] != assign[None, :])
            & (w[None, :] - w[:, None] <= head[:, None] + 1e-9)
            & (w[:, None] - w[None, :] <= head[None, :] + 1e-9)
        )
        d_swap = np.where(ok, d_swap, np.inf)
        pj, pk = np.unravel_index(np.argmin(d_swap), d_swap.shape)
        if min(d_shift[si, sj], d_swap[pj, pk]) > -1e-9:
            return
        if d_shift[si, sj] <= d_swap[pj, pk]:
            load[assign[sj]] -= w[sj]
            load[si] += w[sj]
            assign[sj] = si
        else:
            a, b = assign[pj], assign[pk]
            load[a] += w[pk] - w[pj]
            load[b] += w[pj] - w[pk]
            assign[pj], assign[pk] = b, a


def perturb(
    assign: np.ndarray,
    load: np.ndarray,
    w: np.ndarray,
    cap: np.ndarray,
    k: int,
    rng: np.random.Generator,
) -> None:
    """Kick: k random feasible shifts in place; never leaves the feasible region."""
    n_jobs = len(assign)
    for _ in range(k):
        j = int(rng.integers(n_jobs))
        room = np.flatnonzero(load + w[j] <= cap + 1e-9)
        room = room[room != assign[j]]
        if room.size:
            i = int(rng.choice(room))
            load[assign[j]] -= w[j]
            load[i] += w[j]
            assign[j] = i


def is_feasible(assign: np.ndarray, w: np.ndarray, cap: np.ndarray) -> bool:
    """Independent capacity check, separate from all search code."""
    load = np.bincount(assign, weights=w, minlength=len(cap))
    return bool((load <= cap + 1e-9).all())


cost, w, cap = make_instance(n_jobs=40, n_mach=5, seed=3)
rng = np.random.default_rng(11)
assign, load = greedy_start(cost, w, cap)
jobs = np.arange(len(w))
start_cost = float(cost[assign, jobs].sum())
descend(assign, load, cost, w, cap)
best_assign, best_cost = assign.copy(), float(cost[assign, jobs].sum())
for _ in range(30):  # small ILS on top of the same feasibility-preserving moves
    trial_a, trial_l = best_assign.copy(), np.bincount(
        best_assign, weights=w, minlength=len(cap)
    )
    perturb(trial_a, trial_l, w, cap, k=4, rng=rng)
    descend(trial_a, trial_l, cost, w, cap)
    trial_cost = float(cost[trial_a, jobs].sum())
    if trial_cost < best_cost - 1e-9:
        best_assign, best_cost = trial_a, trial_cost
print(f"greedy {start_cost:.1f} -> descent {float(cost[assign, jobs].sum()):.1f}"
      f" -> ILS {best_cost:.1f}  feasible={is_feasible(best_assign, w, cap)}")
# Expected: greedy 198.9 -> descent 181.5 -> ILS 176.8 (about 11% total improvement)
# with feasible=True throughout -- no evaluation ever touched an infeasible point
```

Design notes that generalize:

- **Move filtering is vectorized.** Both feasibility masks (`fits`, `ok`) are full matrices computed by broadcasting, so the per-iteration cost is $O(mn + n^2)$ instead of looping over moves.
- **Swaps rescue what shifts cannot.** Near capacity, no single job may move anywhere, yet exchanging a heavy job for a light one is feasible. Richer moves keep the feasible region connected — exactly the connectivity requirement from the catalog entry.
- **The perturbation is also feasibility-preserving.** The whole ILS never needs a repair or penalty path, so the objective code stays trivially simple.
- **The validator is independent.** `is_feasible` recomputes loads from scratch and shares no state with the search — the pattern solution-validation-testing prescribes.

## Advanced Techniques

### Epsilon-constrained method

Takahama & Sakai (2006, "Constrained optimization by the ε constrained differential evolution") relax Deb's rules: a solution with $\phi(x) \le \varepsilon(t)$ counts as feasible, and $\varepsilon(t)$ shrinks to 0 on a schedule, typically $\varepsilon(t) = \varepsilon(0)(1 - t/T_c)^{cp}$ with $cp \in [2, 10]$, $\varepsilon(0)$ set to the violation of the population's $\theta$-quantile (often the median), and $T_c$ at 20–80% of the budget. This restores boundary exploration that pure feasibility-first loses, and it is the standard fix when Deb's rules stall on active constraints. Equality constraints get the same treatment with $\varepsilon$ as the equality tolerance, which is the most reliable way metaheuristics handle equalities at all.

### Constraint handling as multi-objective search

Treat $(f, \phi)$ as a bi-objective problem and keep the non-dominated front: good infeasible solutions survive as stepping stones across infeasible gaps. Variants range from simple — keep the best feasible plus the least-violating infeasible elite — to full bi-objective runs whose final answer is the best $\phi = 0$ point. A related two-population design (FI-2Pop, Kimbrough et al. 2008) evolves a feasible and an infeasible population separately with migration between them, which protects boundary diversity without any penalty coefficient. Use these when single-ranking methods repeatedly converge to the same mediocre feasible basin.

### Lamarckian versus Baldwinian repair

Lamarckian repair writes the repaired solution back into the genotype; Baldwinian repair evaluates the repaired phenotype but leaves the genotype untouched. Lamarckian is the combinatorial default — faster convergence, and the population stores what it actually scored. Baldwinian preserves genetic diversity and helps when the repair is strongly biased (many infeasible points repair to the same feasible point), at the price of a genotype–fitness mismatch that confuses distance-based diversity measures. A practical middle ground: write back with probability 5–10% (partial Lamarckism), which empirically tracks the best of both on multidimensional knapsack-type problems.

### Violation normalization and constraint scaling

A penalty or ranking over raw violations silently weights constraints by their units: a capacity violated by 50 kg dominates a count violated by 2 even if the count matters more. Normalize each $v_j$ by its right-hand side, or adaptively by the running maximum violation observed for constraint $j$ (clipped to avoid division by very small values). For Deb's rules and stochastic ranking this matters as much as for penalties, since $\phi$ aggregates across constraints in both. Recheck normalization whenever instance sizes change — a scheme tuned on 50-job instances can invert constraint priorities on 500-job instances.

### Adaptive switching between techniques

The technique itself can be a decision variable. ALNS-style adaptive schemes maintain several handling modes (e.g., penalty with low $\rho$, penalty with high $\rho$, repair) and select per iteration with weights updated from success statistics. Simpler and often sufficient: run the first 20% of the budget with a mild penalty (exploration), then switch to repair plus Deb rules (exploitation). Log the feasibility rate per generation; the switch point belongs where the rate plateaus. Tune any remaining coefficients with the protocol from metaheuristic-design-principles rather than by hand.

## Practical Challenges

**The penalty coefficient looks fine on small instances and fails on large ones.** Objective and violation magnitudes scale differently with instance size ($f$ may grow like $n$, capacity violations like $\sqrt{n}$). Never ship a hard-coded $\rho$; recalibrate per instance from a random sample (`calibrate_rho` above) or use APM, which rescales every generation.

**The run reports an excellent objective that turns out infeasible.** The classic penalty failure: $\rho$ too small, and the reporting code read the penalized incumbent. Always track and report *best feasible* separately from best penalized, and gate the final answer through an independent checker (solution-validation-testing). If no feasible solution was ever found, say so — do not report the least-infeasible one as a solution.

**Equality constraints make every technique look broken.** With $h_k(x) = 0$, random solutions have $\phi > 0$ almost surely, penalties chase a measure-zero set, and repair has no slack to work with. Reformulate first: eliminate variables using the equality, or build the equality into a decoder (e.g., assign the residual demand to a closing variable). If neither works, use the epsilon-constrained method with a decaying tolerance.

**Repair destroys diversity.** A deterministic greedy repair maps many infeasible parents onto few feasible points; the population collapses within tens of generations. Randomize the repair order among near-tied candidates, repair with probability less than 1, or go Baldwinian. Monitor unique-solution counts per generation to catch this early.

**Deb's rules converge fast and then never improve.** Absolute feasibility-first kills the boundary search that most resource-constrained optima require. Switch to stochastic ranking ($P_f \approx 0.45$) or the epsilon-constrained method, and add an infeasible elite archive so boundary-adjacent material survives selection.

**Feasibility-preserving moves cannot reach the optimum.** The feasible region is disconnected under the move set — common when capacities are tight and only single-item shifts are allowed. Enlarge the move set (swaps, ejection chains, 2-exchanges) until empirical connectivity returns, or allow a bounded infeasible corridor: accept moves with $\phi \le \varepsilon$ during exploration and close $\varepsilon$ later.

**The decoder is feasible but the search stalls anyway.** Decoder redundancy means most genotype changes do not change the phenotype, so the effective neighborhood is tiny. Measure the phenotype-change rate of mutations; if under ~30%, redesign keys (e.g., perturb keys by rank, not value) or move problem-specific structure from the decoder into the operators. See decoder-based-representations for locality diagnostics.

**Two techniques were compared with different effort and the wrong one won.** Repair adds per-individual cost, so equal-generation comparisons favor it unfairly on wall-clock terms (or punish it on evaluation terms). Fix the budget in wall-clock time or in objective evaluations — state which — and use identical seeds, instances, and reporting metrics, as in the head-to-head example above.

## Tools & Libraries

| Library | When to use | Note |
|---|---|---|
| numpy | All techniques in this skill | Vectorized violations, masks, and rankings; `np.random.default_rng(seed)` everywhere |
| pymoo | Population methods with constraints out of the box | Implements feasibility-first (Deb) ranking, $\phi$ aggregation (`CV`), and constrained NSGA-II |
| DEAP | Custom GA loops where you control selection | Bring your own constraint handling; its `DeltaPenalty`/`ClosestValidPenalty` decorators cover static penalty and repair hooks |
| jMetalPy | Benchmarking constrained evolutionary algorithms | Includes stochastic-ranking-style comparators for ES baselines |
| scipy | Repair by projection / matching | `scipy.optimize.linear_sum_assignment` repairs broken assignment structure optimally |
| OR-Tools CP-SAT | When constraints belong in an exact model instead | If every operator fights the constraints, the problem may be CP-shaped — move the hard part to a solver |
| gurobipy | Matheuristic repair | A small MIP as the repair step (fix most variables, restore feasibility optimally) is often the strongest repair available |
| pandas | Head-to-head experiment tables | One row per (instance, seed, technique); aggregate feasibility rate and best-feasible gap |

## Output Format

A complete constraint-handling recommendation or implementation contains:

1. **Constraint inventory table** — one row per constraint family: type (inequality/equality), hard/soft, violation definition $v_j$, scale $s_j$, chosen technique, rationale.

   | Constraint | Type | Hard? | Violation measure | Technique | Why |
   |---|---|---|---|---|---|
   | Machine capacity | $\le$ | Hard | $\max(0, \text{load}_i - b_i)/b_i$ | Feasibility-preserving shift+swap | Cheap O(1) move check; region connected under swaps |
   | Each job assigned once | $=$ | Hard | structural | Encoded away (assignment vector) | Representation-level |
   | Workload balance | $\le$ | Soft | weighted term in $f$ | Objective term | Preference, not feasibility |

2. **Technique parameters** — every coefficient with its value and origin: $\rho$ (calibrated how), $C/\alpha$ schedule and budget link, $P_f$, $\varepsilon(t)$ schedule, repair order rule, write-back policy (Lamarckian/Baldwinian).
3. **Feasibility telemetry** — per generation: feasible fraction of the population, best feasible objective, mean $\phi$ of infeasible members. Report the generation at which the first feasible solution appeared.
4. **Solution-quality report** — best feasible objective, gap to a reference bound (DP, LP relaxation, or best known), seeds and budget used, and an explicit statement that the final solution passed the independent feasibility checker.
5. **Head-to-head evidence when two techniques were candidates** — table over instances × seeds with best-feasible mean/std per technique and identical budgets; name the winner and the margin.
6. **Code artifacts** — violation functions, the technique implementation, and the independent validator as separate functions (never let the validator share code with the fitness path).

## Questions to Ask

- Which constraints are truly hard, and which are preferences someone would trade for a better objective?
- What fraction of random solutions is feasible — has anyone sampled this?
- Are there equality constraints, and can they be eliminated by reformulation before any handling technique is chosen?
- How expensive is one feasibility check relative to one objective evaluation?
- Is the representation fixed, or can we still choose an encoding that removes constraints structurally?
- Which algorithm family is this for — population-based or single-solution local search?
- Does a natural greedy repair exist (drop/add, reinsertion, projection)?
- Is the evaluation budget defined in wall-clock time or objective evaluations, and how large is it?
- Do known good solutions sit on the feasibility boundary (active constraints at the optimum)?
- Is there an independent feasibility checker, or does feasibility currently rely on the search code being correct?

## Related Skills

- **solution-encodings** — when constraints can be removed structurally by choosing a better representation before any handling technique is added
- **decoder-based-representations** — when feasibility should be guaranteed by construction through random keys, priority decoding, or schedule-generation schemes
- **metaheuristic-design-principles** — when constraint handling must be chosen jointly with representation, operators, and the intensification/diversification balance
- **solution-validation-testing** — when the chosen technique needs an independent feasibility checker and regression tests against known optima
- **knapsack-problems** — when the budget-constraint patterns from this skill (penalty calibration, greedy repair, key decoders) meet their canonical problem family
