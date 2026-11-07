---
name: metaheuristic-design-principles
description: When the user wants to choose or design a metaheuristic for a combinatorial problem — picking a representation, designing operators, handling constraints, balancing intensification and diversification, and setting stopping criteria and evaluation budgets. Also use when the user mentions "which metaheuristic," "design a heuristic," "intensification," "diversification," "stopping criterion," "metaheuristic framework," or when exact methods cannot scale to the required instance size. For representation choice, see solution-encodings; for move and neighborhood design, see local-search-and-neighborhoods.
---

# Metaheuristic Design Principles

You are an expert in metaheuristic design for combinatorial optimization. This is the hub skill for choosing and structuring a metaheuristic: representation choice, operator design, constraint handling, intensification versus diversification, stopping criteria, parameter classes, and evaluation budgeting, organized around the single-solution vs population taxonomy. Use the framework below to turn a problem statement into a concrete, testable algorithm design, then hand operator-level detail off to the component skills listed at the end. Two complete end-to-end designs are worked out: a permutation problem (flow-shop sequencing) and a binary selection problem (multidimensional knapsack).

## Initial Assessment

Establish these facts before proposing any algorithm. Every later design decision is conditional on them.

- **Confirm a metaheuristic is justified.** Ask whether an exact method (MIP, CP, DP) with a time limit already reaches the required instance size with an acceptable gap. A metaheuristic adds tuning and validation cost; it must earn its place. If the problem is not yet formalized, route through **problem-formulation** first.
- **Identify the decision structure.** Classify the core decision: permutation (sequencing, routing), binary selection (subsets, knapsack-like), assignment (items to agents), partition (clustering, coloring), or a mix. The structure drives representation and operator choice.
- **Get realistic instance dimensions.** n = 50 and n = 50,000 need different designs. Ask for the largest instance that must be solved in production, not the average one.
- **Classify constraints as hard or soft.** Hard constraints must hold in every reported solution; soft constraints carry a violation price in the objective. List each constraint with its class. This determines the constraint-handling strategy (penalty, repair, decoder, feasibility-preserving operators).
- **Time one objective evaluation.** Microsecond evaluations allow millions of moves and favor single-solution local search; millisecond-to-second evaluations force small budgets, caching, batch vectorization, or surrogates.
- **Check for delta (incremental) evaluation.** If a move's effect on the objective can be computed in O(1) or O(n) instead of a full recomputation, single-solution methods gain an order-of-magnitude advantage.
- **Fix the budget.** Agree on a wall-clock budget per run, then convert it to an approximate evaluation budget. State budgets in evaluations where possible: they are hardware-independent and make comparisons reproducible.
- **Define the quality target.** "Within 1% of best-known," "any feasible solution in 10 s," or "beat the incumbent planning tool by 3%" lead to different designs. Refuse to design against an undefined target.
- **Inventory baselines.** A greedy rule, an existing planning heuristic, random-restart local search, or a MIP solver with a time limit. The new design must beat the honest baseline under equal budgets, or it is not worth deploying.
- **Determine stochasticity.** Deterministic objective, or noisy (simulation-based, sampled scenarios)? Noise changes acceptance rules, evaluation replication, and statistical reporting.
- **Check data and instance availability.** Real instances, public benchmarks, or a synthetic generator with seeds? Tuning needs a training set of instances disjoint from the test set.
- **Record reproducibility requirements.** Seeds, library versions, number of independent runs, and the statistical protocol expected for reporting (see **algorithm-benchmarking-statistics**).

## Design Framework and Taxonomy

A metaheuristic approximately solves

$$\min_{x \in X} f(x), \qquad X \subseteq S,$$

where $S$ is the set of solutions the chosen representation can express and $X \subseteq S$ is the feasible set. The relation between $S$ and $X$ is itself a design decision with three standard options:

1. **$S = X$ (feasibility by construction).** Representation and operators only produce feasible solutions, e.g. permutations for sequencing. Cheapest and safest when available.
2. **$S \supset X$ with penalties or repair.** The search visits infeasible points; either minimize $f(x) + \lambda \, v(x)$ with violation measure $v$, or repair each candidate back into $X$. See **constraint-handling-techniques**.
3. **Decoder.** Search a genotype space $G$ and map $g \mapsto d(g) \in X$ with a feasibility-enforcing decoder (random keys, priority rules). Moves all feasibility logic into one function.

### The five design decisions

Every metaheuristic, whatever its name, is fully specified by five decisions (Blum & Roli 2003, "Metaheuristics in combinatorial optimization"; Talbi 2009, "Metaheuristics: From Design to Implementation"):

1. **Representation** — how a solution is stored: bitstring, integer vector, permutation, matrix, random keys. Criteria: completeness (can it express every feasible solution?), locality (do small changes in the encoding cause small changes in the solution?), redundancy. Details in **solution-encodings**.
2. **Evaluation** — exact or approximate $f$, full or delta computation, single or batched. The evaluation function consumes 80-99% of runtime in most implementations; design it first, not last.
3. **Operators** — construction (greedy, randomized greedy), local moves/neighborhoods, perturbations, and (for populations) recombination and mutation. Details in **local-search-and-neighborhoods**, crossover-operators, and mutation-and-perturbation-operators.
4. **Search control** — acceptance rule, memory structures, selection and replacement, restart policy. This is where intensification and diversification are balanced.
5. **Stopping criterion** — evaluation budget, wall clock, stagnation window, or target value.

### Single-solution vs population methods

| Property | Single-solution (trajectory) | Population-based |
|---|---|---|
| Members | simulated annealing, tabu search, ILS, VNS, GLS, LNS/ALNS | GA, memetic, BRKGA, EDA, DE, PSO (via decoders), ACO, scatter search |
| Search state | one incumbent plus memory (tabu list, penalties) | a solution set, possibly plus a model (pheromones, distributions) |
| Strengths | deep intensification; cheap iterations; exploits delta evaluation fully | recombines building blocks; batch evaluation vectorizes; built-in diversity |
| Weaknesses | needs explicit escape mechanisms (kicks, restarts, penalties) | slower per improvement; diversity must be managed; more parameters |
| Choose when | a strong neighborhood with fast delta evaluation exists | good solutions share identifiable components; evaluation is batchable; the landscape is multimodal |

Decision guidance:

- **Default first design: ILS** (Lourenço, Martin & Stützle 2003, "Iterated Local Search") — local search plus perturbation plus acceptance. It is the strongest simple baseline for most permutation and assignment problems, and every component generalizes.
- **Tightly constrained routing/scheduling: LNS/ALNS.** When feasible solutions are sparse but good repair heuristics exist, destroy-and-repair dominates small-move local search.
- **Meaningful recombination: population methods.** If two good solutions share components whose combination is plausibly good (item subsets, edge sets, machine assignments), crossover adds real value; otherwise a population is an expensive random restart.
- **A natural decoder exists: BRKGA / random keys.** When feasibility logic is complex but a priority-based constructor exists, put all problem knowledge in the decoder.
- **Pick mechanisms, not metaphors.** Evaluate any proposed "novel" algorithm by its operators and control logic, not its naming story (Sörensen 2015, "Metaheuristics — the metaphor exposed").

### Intensification vs diversification

Every control parameter pushes one of two pressures (Glover & Laguna 1997, "Tabu Search"; Blum & Roli 2003):

| Lever | Intensifies when... | Diversifies when... |
|---|---|---|
| Acceptance rule | only improvements accepted | worse moves accepted (Metropolis, restart-to-random) |
| Perturbation / mutation strength | small (1-2 moves, rate 1/n) | large (segment moves, rate 5/n+) |
| Selection pressure | large tournaments, strong elitism | small tournaments, uniform selection |
| Memory | restart from elite solutions, path relinking | frequency-based penalties, tabu lists on repeated attributes |
| Population management | truncation replacement | duplicate elimination, random immigrants, niching |

Diagnostic rule of thumb: if runs improve fast then flatline far from any bound, the design over-intensifies — strengthen perturbation, soften acceptance, or restart on stagnation. If the best value jitters without a trend, the design over-diversifies — deepen local search, raise selection pressure, shrink perturbation.

### Stopping criteria

- **Evaluation budget** (preferred): hardware-independent, makes tuning and comparison fair. Count every objective call, including construction and repair.
- **Wall-clock limit**: what production deployments actually impose; report both.
- **Stagnation window**: stop or restart after no incumbent improvement in the last $w$ evaluations (typically 10-30% of the budget).
- **Target value**: stop when a known bound or required quality is reached; enables time-to-target analysis.

Combine budget + stagnation. Never use "the population converged" alone as a stopping rule — convergence of the population says nothing about distance to the optimum.

### Parameter classes and typical ranges

Structural parameters (representation, neighborhood set, operator pool) are design decisions fixed before tuning. Behavioral parameters are tuned on a training instance set (see **optuna-hyperparameter-tuning**). Budget parameters are fixed by the experimental protocol. Static settings vs online adaptation is the parameter-control taxonomy of Eiben, Hinterding & Michalewicz (1999).

| Parameter | Class | Typical range | What it trades off |
|---|---|---|---|
| population size $\mu$ | budget | 30-200 | exploration breadth vs generations affordable under a fixed evaluation budget |
| offspring per generation $\lambda$ | budget | $\mu$ to $7\mu$ | sampling width per generation vs number of generations |
| tournament size | behavioral | 2-5 | selection pressure vs diversity (takeover time) |
| mutation / bit-flip rate | behavioral | $1/n$ to $5/n$ per gene | refinement vs disruption of good solutions |
| perturbation strength $k$ | behavioral | 2-8 moves, or 10-30% destroyed | escape distance vs loss of accumulated quality |
| initial uphill acceptance (SA) | behavioral | 50-80% of early worse moves | early exploration vs wasted budget |
| tabu tenure | behavioral | $\approx n/10$ to $\approx \sqrt{n \cdot m}$ | cycling prevention vs over-restriction |
| elite fraction | behavioral | 0.05-0.20 | convergence speed vs premature convergence |
| stagnation window $w$ | stopping | 10-30% of budget | persistence in a basin vs wasted tail of the run |

## Reusable Framework Skeletons

Both worked designs below instantiate one of two generic drivers. The drivers fix the control flow; all problem knowledge enters through callables (evaluation, local search, perturbation, variation). This separation is what makes a design testable: each component can be validated alone, swapped, and tuned without touching the loop.

```text
GENERIC METAHEURISTIC TEMPLATE (minimization)

Design-time decisions (fixed before any run):
  representation : how a solution is stored (permutation, bitstring, keys, ...)
  evaluation     : f(x); count EVERY call against one shared budget
  operators      : construction, local move(s), perturbation / variation
  search control : acceptance rule, memory, selection, replacement, restarts
  stopping       : evaluation budget + stagnation guard

SINGLE-SOLUTION TEMPLATE (ILS-shaped)
  x  <- construct()                       # greedy or randomized greedy
  x  <- local_search(x)                   # intensification
  x* <- x
  while budget remains:
      x' <- perturb(x)                    # diversification
      x' <- local_search(x')              # intensification
      if f(x') < f(x*): x* <- x'          # incumbent update
      x  <- accept(x, x')                 # search control
  return x*

POPULATION TEMPLATE
  P <- init_population(); evaluate(P)
  while budget remains:
      parents  <- select(P)               # exploitation pressure
      children <- vary(parents)           # recombination + mutation
      children <- repair_or_penalize(children)
      P <- replace(P, children)           # elitism + duplicate control
  return best(P)
```

The single-solution driver. The `Budget` wrapper is the one non-negotiable piece: wrap the raw objective once and pass the wrapper to every component, so construction, local search, and the main loop all draw from the same counted budget.

```python
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

import numpy as np

Objective = Callable[[np.ndarray], float]


class Budget:
    """Wraps a raw objective and counts evaluations against a fixed budget."""

    def __init__(self, objective: Objective, max_evaluations: int) -> None:
        self._objective = objective
        self.max_evaluations = max_evaluations
        self.used = 0

    def __call__(self, x: np.ndarray) -> float:
        """Evaluate x and charge one evaluation to the budget."""
        self.used += 1
        return self._objective(x)

    @property
    def exhausted(self) -> bool:
        """True once the budget is spent."""
        return self.used >= self.max_evaluations


@dataclass
class SearchResult:
    """Best solution plus an (evaluations, objective) convergence trace."""

    best: np.ndarray
    best_obj: float
    trace: list[tuple[int, float]] = field(default_factory=list)


def single_solution_search(
    initial: np.ndarray,
    budget: Budget,
    local_search: Callable[[np.ndarray, Budget], tuple[np.ndarray, float]],
    perturb: Callable[[np.ndarray, np.random.Generator], np.ndarray],
    accept: Callable[[float, float, np.random.Generator], bool],
    seed: int = 0,
) -> SearchResult:
    """Generic single-solution driver (minimization), ILS-shaped.

    `local_search` is the intensification component, `perturb` the
    diversification component, `accept` the search-control component.
    """
    rng = np.random.default_rng(seed)
    current, current_obj = local_search(initial, budget)
    best, best_obj = current.copy(), current_obj
    result = SearchResult(best, best_obj, [(budget.used, best_obj)])
    while not budget.exhausted:
        candidate = perturb(current, rng)
        candidate, candidate_obj = local_search(candidate, budget)
        if candidate_obj < best_obj:
            best, best_obj = candidate.copy(), candidate_obj
            result.trace.append((budget.used, best_obj))
        if accept(candidate_obj, current_obj, rng):
            current, current_obj = candidate, candidate_obj
    result.best, result.best_obj = best, best_obj
    return result
```

The population driver. Replacement is $(\mu + \lambda)$ truncation — inherently elitist — with duplicate elimination, plus random immigrants if duplicates collapse the population. Both guards exist because truncation alone destroys diversity on small discrete spaces.

```python
from __future__ import annotations

from typing import Callable

import numpy as np


def population_search(
    init_population: Callable[[np.random.Generator], np.ndarray],
    evaluate_population: Callable[[np.ndarray], np.ndarray],
    make_offspring: Callable[[np.ndarray, np.ndarray, np.random.Generator], np.ndarray],
    n_generations: int,
    seed: int = 0,
) -> tuple[np.ndarray, float, list[float]]:
    """Generic population driver (minimization).

    `make_offspring` bundles selection and variation: it receives the
    population with its objective vector and returns a candidate batch.
    """
    rng = np.random.default_rng(seed)
    pop = init_population(rng)
    obj = evaluate_population(pop)
    mu = len(pop)
    trace = [float(obj.min())]
    for _ in range(n_generations):
        children = make_offspring(pop, obj, rng)
        merged = np.vstack([pop, children])
        merged_obj = np.concatenate([obj, evaluate_population(children)])
        merged, keep = np.unique(merged, axis=0, return_index=True)
        merged_obj = merged_obj[keep]
        if len(merged) < mu:  # diversity collapsed: inject random immigrants
            immigrants = init_population(rng)[: mu - len(merged)]
            merged = np.vstack([merged, immigrants])
            merged_obj = np.concatenate([merged_obj, evaluate_population(immigrants)])
        order = np.argsort(merged_obj)[:mu]
        pop, obj = merged[order], merged_obj[order]
        trace.append(float(obj.min()))
    winner = int(np.argmin(obj))
    return pop[winner], float(obj[winner]), trace
```

## Worked Design 1: Permutation Problem — Flow-Shop Sequencing

Problem: $n$ jobs visit $m$ machines in the same order; minimize the makespan $C_{\max}$ of the job permutation. Processing times follow the $U\{1,99\}$ convention of Taillard (1993, "Benchmarks for basic scheduling problems"). The walkthrough below applies the five design decisions in order.

1. **Representation: permutation of job indices.** Direct and complete — every permutation is feasible, so this is the $S = X$ case with zero constraint-handling cost. Random keys were considered and rejected: they add decoder cost and lose locality, with no benefit when native permutation operators exist (see **solution-encodings**).
2. **Evaluation: full $O(nm)$ recursion.** Flow-shop insertion moves have no $O(1)$ delta evaluation (unlike TSP 2-opt), so the budget is counted in full evaluations. Taillard's acceleration evaluates all $n$ insertion positions of one job in $O(nm)$ total — the single most valuable refinement if more speed is needed.
3. **Construction: NEH** (Nawaz, Enscore & Ham 1983). Costs $O(n^2)$ evaluations and typically lands within a few percent of the best known — far cheaper than recovering the same quality from a random start.
4. **Local move: remove-and-reinsert (insertion).** The insertion neighborhood dominates adjacent-swap and exchange for flow-shop makespan. First-improvement scanning keeps iterations cheap.
5. **Search control: kick + better-or-equal acceptance.** Perturbation removes $k=3$ random jobs and reinserts them at random positions; acceptance allows plateau drift but never accepts a strictly worse solution. Metropolis acceptance is deliberately left out of the first design — add it only if stagnation diagnostics demand it.
6. **Stopping: a fixed evaluation budget** shared by all components through the `Budget` wrapper, so NEH, the descent, and the main loop are charged honestly.

The result is an ILS-shaped single-solution method, chosen because evaluation is cheap and a strong neighborhood exists. For the method-specific refinements (acceptance variants, adaptive kicks) see the dedicated iterated-local-search skill; for perturbation operator catalogs see mutation-and-perturbation-operators.

```python
import numpy as np


def random_flow_shop(n_jobs: int, n_machines: int, seed: int) -> np.ndarray:
    """Processing times p[j, m] ~ U{1, 99}, the Taillard (1993) convention."""
    rng = np.random.default_rng(seed)
    return rng.integers(1, 100, size=(n_jobs, n_machines)).astype(float)


def makespan(perm: np.ndarray, p: np.ndarray) -> float:
    """Makespan of job sequence `perm` for processing times p (jobs x machines).

    Recursion C[j, m] = max(C[j, m-1], C[j-1, m]) + p[perm[j], m]. The
    recursion is sequential in both indices, so explicit loops are correct
    here; cost is O(n*m) per evaluation.
    """
    seq = p[perm]
    completion = np.empty_like(seq)
    completion[0] = np.cumsum(seq[0])
    for j in range(1, seq.shape[0]):
        completion[j, 0] = completion[j - 1, 0] + seq[j, 0]
        for m in range(1, seq.shape[1]):
            completion[j, m] = max(completion[j, m - 1], completion[j - 1, m]) + seq[j, m]
    return float(completion[-1, -1])


p_demo = random_flow_shop(6, 3, seed=42)
print(makespan(np.arange(6), p_demo))
# Expected: 439.0 — makespan of the identity permutation on this 6x3 instance.
```

Construction. Note the signature: NEH takes the *counted* evaluator, not the raw data, so its $O(n^2)$ evaluations are charged to the same budget as everything else.

```python
import numpy as np
from typing import Callable


def neh(p: np.ndarray, evaluate: Callable[[np.ndarray], float]) -> np.ndarray:
    """NEH construction (Nawaz, Enscore & Ham, 1983).

    Insert jobs in decreasing total-work order, each at its best position.
    Uses the makespan evaluator from the block above via `evaluate`.
    """
    order = np.argsort(-p.sum(axis=1), kind="stable")
    perm = [int(order[0])]
    for job in order[1:]:
        best_perm, best_val = perm, np.inf
        for pos in range(len(perm) + 1):
            candidate = perm[:pos] + [int(job)] + perm[pos:]
            val = evaluate(np.array(candidate))
            if val < best_val:
                best_perm, best_val = candidate, val
        perm = best_perm
    return np.array(perm)
```

Local search, perturbation, acceptance, and the assembled run. These three callables plug into `single_solution_search` from the framework section unchanged.

```python
import numpy as np


def insertion_local_search(perm: np.ndarray, budget: "Budget") -> tuple[np.ndarray, float]:
    """First-improvement insertion descent.

    Remove one job, reinsert it at another position; restart the scan after
    every improvement; stop at a local optimum or when the budget runs out.
    """
    current, current_obj = perm.copy(), budget(perm)
    improved = True
    while improved and not budget.exhausted:
        improved = False
        for j in range(len(current)):
            job, removed = current[j], np.delete(current, j)
            for pos in range(len(current)):
                if pos == j:
                    continue
                candidate = np.insert(removed, pos, job)
                candidate_obj = budget(candidate)
                if candidate_obj < current_obj - 1e-9:
                    current, current_obj, improved = candidate, candidate_obj, True
                    break
                if budget.exhausted:
                    return current, current_obj
            if improved:
                break
    return current, current_obj


def reinsertion_kick(perm: np.ndarray, rng: np.random.Generator, k: int = 3) -> np.ndarray:
    """Diversification kick: remove k random jobs, reinsert at random positions."""
    out = perm.copy()
    for _ in range(k):
        j = int(rng.integers(len(out)))
        job = out[j]
        out = np.insert(np.delete(out, j), int(rng.integers(len(out))), job)
    return out


def accept_better_equal(candidate_obj: float, current_obj: float,
                        rng: np.random.Generator) -> bool:
    """Accept improvements and plateau moves; reject strictly worse ones."""
    return candidate_obj <= current_obj


p = random_flow_shop(n_jobs=30, n_machines=8, seed=11)
budget = Budget(lambda perm: makespan(perm, p), max_evaluations=60_000)
start = neh(p, budget)
print("NEH makespan:", makespan(start, p))
result = single_solution_search(start, budget, insertion_local_search,
                                reinsertion_kick, accept_better_equal, seed=7)
print("best:", result.best_obj, "evaluations:", budget.used)
# Expected: NEH makespan: 2005.0, then best: 1971.0 with 60000 evaluations —
# the descent reaches 2001 by evaluation ~1500, then kicks find 1982, 1977, 1971.
```

## Worked Design 2: Binary Selection Problem — Multidimensional Knapsack

Problem: choose a subset of $n$ items maximizing profit $\sum_i p_i x_i$ subject to $m$ resource constraints $\sum_i w_{ki} x_i \le c_k$, $x \in \{0,1\}^n$. The classic GA study and repair scheme are due to Chu & Beasley (1998, "A genetic algorithm for the multidimensional knapsack problem"). The same five decisions, now leading to a population method:

1. **Representation: bitstring.** The natural encoding for selection problems. Here $S \supset X$ — infeasible bitstrings exist — so constraint handling is mandatory.
2. **Constraint handling: greedy repair, not penalties.** For the MKP, static penalties either dominate the profit signal or leave the search wandering through infeasible space; the two-phase repair (drop worst-ratio items until feasible, then greedily refill) keeps every individual feasible and even improves it. The full decision logic between penalties, repair, decoders, and feasibility rules is in **constraint-handling-techniques**.
3. **Method family: population.** Good knapsack solutions share building blocks — profitable, low-weight item combinations — so uniform crossover recombines useful material. Batch evaluation is one matrix product, so the population vectorizes for free. Maximization is handled by negating profits: the drivers always minimize.
4. **Variation: uniform crossover + bit-flip mutation at rate $1/n$.** Operator alternatives and their bias properties are cataloged in crossover-operators and mutation-and-perturbation-operators; nothing problem-specific is needed here because repair carries the problem knowledge.
5. **Search control and stopping: binary tournament selection; $(\mu+\lambda)$ truncation with duplicate elimination and random immigrants** (already built into `population_search`); a generation count chosen so that $\mu + \lambda \cdot g$ matches the agreed evaluation budget.

```python
import numpy as np


def random_mkp(n_items: int, n_constraints: int, seed: int,
               tightness: float = 0.5) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Chu & Beasley (1998)-style instance.

    Weights ~ U{1, 1000}; capacity = tightness * total weight per
    constraint; profits correlated with mean weight plus noise.
    """
    rng = np.random.default_rng(seed)
    weights = rng.integers(1, 1001, size=(n_constraints, n_items)).astype(float)
    capacities = tightness * weights.sum(axis=1)
    profits = weights.mean(axis=0) + rng.integers(1, 501, size=n_items)
    return profits, weights, capacities


def mkp_batch_objective(pop: np.ndarray, profits: np.ndarray) -> np.ndarray:
    """Batch profit of a 0/1 population, negated so the drivers can minimize."""
    return -(pop @ profits)


def greedy_repair(pop: np.ndarray, profits: np.ndarray, weights: np.ndarray,
                  capacities: np.ndarray) -> np.ndarray:
    """Two-phase repair (Chu & Beasley, 1998).

    Drop selected items in increasing profit/aggregate-weight ratio until
    feasible, then greedily re-add items in decreasing ratio while they fit.
    The per-individual pass is sequential by nature; inner work is vectorized.
    """
    ratio = profits / weights.sum(axis=0)
    drop_order = np.argsort(ratio)
    add_order = drop_order[::-1]
    repaired = pop.copy()
    for ind in repaired:
        load = weights @ ind
        for item in drop_order:
            if np.all(load <= capacities):
                break
            if ind[item]:
                ind[item] = 0
                load -= weights[:, item]
        for item in add_order:
            if not ind[item] and np.all(load + weights[:, item] <= capacities):
                ind[item] = 1
                load += weights[:, item]
    return repaired


profits_d, weights_d, caps_d = random_mkp(20, 3, seed=5)
raw = (np.random.default_rng(5).random((4, 20)) < 0.8).astype(np.int64)
rep = greedy_repair(raw, profits_d, weights_d, caps_d)
print("feasible after repair:", bool(np.all(weights_d @ rep.T <= caps_d[:, None])))
# Expected: feasible after repair: True — dense random bitstrings become feasible.
```

The three callables for `population_search`, built by a factory so the instance data is bound once. Selection, crossover, and mutation are vectorized across the whole offspring batch — no Python loop touches individual genes.

```python
import numpy as np
from typing import Callable

OffspringFn = Callable[[np.ndarray, np.ndarray, np.random.Generator], np.ndarray]


def make_mkp_components(
    profits: np.ndarray, weights: np.ndarray, capacities: np.ndarray,
    pop_size: int, flip_rate: float,
) -> tuple[Callable[[np.random.Generator], np.ndarray],
           Callable[[np.ndarray], np.ndarray], OffspringFn]:
    """Build the three callables `population_search` needs for the MKP."""

    def init_population(rng: np.random.Generator) -> np.ndarray:
        """Random sparse bitstrings, repaired to feasibility."""
        raw = (rng.random((pop_size, len(profits))) < 0.3).astype(np.int64)
        return greedy_repair(raw, profits, weights, capacities)

    def evaluate_population(pop: np.ndarray) -> np.ndarray:
        """Negated batch profit (the drivers minimize)."""
        return mkp_batch_objective(pop, profits)

    def make_offspring(pop: np.ndarray, obj: np.ndarray,
                       rng: np.random.Generator) -> np.ndarray:
        """Binary tournament + uniform crossover + bit flips, all batched."""
        n, n_items = pop.shape
        a, b = rng.integers(n, size=n), rng.integers(n, size=n)
        parents_1 = pop[np.where(obj[a] <= obj[b], a, b)]
        a, b = rng.integers(n, size=n), rng.integers(n, size=n)
        parents_2 = pop[np.where(obj[a] <= obj[b], a, b)]
        cross = rng.random((n, n_items)) < 0.5
        children = np.where(cross, parents_1, parents_2)
        flips = rng.random((n, n_items)) < flip_rate
        children = np.where(flips, 1 - children, children)
        return greedy_repair(children, profits, weights, capacities)

    return init_population, evaluate_population, make_offspring


profits, weights, capacities = random_mkp(n_items=30, n_constraints=5, seed=3)
init, evaluate, offspring = make_mkp_components(
    profits, weights, capacities, pop_size=50, flip_rate=1 / 30)
best, best_obj, trace = population_search(init, evaluate, offspring,
                                          n_generations=80, seed=3)
feasible = bool(np.all(weights @ best <= capacities))
print("profit:", -best_obj, "items:", int(best.sum()), "feasible:", feasible)
# Expected: profit: 12609.2, items: 15, feasible: True — the best-so-far trace
# improves from -12370.4 (generation 0) to -12609.2; about 4,100 evaluations total.
```

Contrast with Design 1: the flow shop got a single-solution method because evaluation is cheap and sequential while the neighborhood is strong; the MKP got a population method because evaluation batches into one matrix product and good solutions share recombinable item subsets. Same five decisions, opposite outcomes — the taxonomy, not taste, made the call.

## Advanced Techniques

### Adaptive perturbation strength

Fixed kick strength $k$ is the most common silent failure in ILS-shaped designs: too small and the search falls back into the same basin, too large and it degenerates into random restart. Reactive control adjusts $k$ from the search's own feedback — the discrete analogue of step-size adaptation in evolution strategies (Eiben, Hinterding & Michalewicz 1999).

```python
import numpy as np


def adapt_kick_strength(k: int, improved: bool, k_min: int = 2, k_max: int = 10) -> int:
    """Shrink the kick after an improving iteration (stay near a good basin);
    grow it after a failed one (escape further next time)."""
    return max(k_min, k - 1) if improved else min(k_max, k + 1)


k, history = 4, []
rng = np.random.default_rng(0)
for _ in range(8):
    improved = bool(rng.random() < 0.3)  # stand-in for "iteration improved incumbent"
    k = adapt_kick_strength(k, improved)
    history.append(k)
print(history)
# Expected: [5, 4, 3, 2, 3, 4, 5, 6] — k decays during a successful stretch,
# then climbs while iterations fail.
```

### Diversity monitoring and restarts

Population methods should measure diversity, not assume it. For bitstrings, mean per-gene entropy is a one-line monitor; for permutations, use mean pairwise distance instead. Act on the signal: raise mutation, inject immigrants, or restart from elites when diversity collapses while the incumbent stagnates.

```python
import numpy as np


def population_entropy(pop: np.ndarray) -> float:
    """Mean per-gene Shannon entropy of a 0/1 population, in [0, 1].

    1.0 means every gene is 50/50 across the population; near 0 means the
    population is near-copies and recombination has stopped contributing.
    """
    freq = pop.mean(axis=0)
    eps = 1e-12
    h = -(freq * np.log2(freq + eps) + (1 - freq) * np.log2(1 - freq + eps))
    return float(max(0.0, h.mean()))


rng = np.random.default_rng(1)
diverse = (rng.random((40, 60)) < 0.5).astype(np.int64)
collapsed = np.tile((rng.random(60) < 0.5).astype(np.int64), (40, 1))
print(round(population_entropy(diverse), 3), round(population_entropy(collapsed), 3))
# Expected: 0.986 0.0 — restart or raise mutation when entropy falls below ~0.2
# while the best objective has not improved within the stagnation window.
```

### Hybridization patterns

Three patterns cover most practical hybrids. (a) **Memetic**: apply local search to some or all offspring; budget it — local search on every individual at full depth usually wastes evaluations, so refine only new elites or sample a fraction. (b) **Matheuristic**: call a MIP solver inside the loop — repair via a small exact subproblem, or improve by fixing most variables and re-optimizing the rest; budget solver calls in wall-clock seconds. (c) **Warm-start exchange**: feed metaheuristic incumbents to an exact solver as MIP starts, and exact solutions of reduced problems back into the population.

### Evaluation-budget engineering

The evaluation function deserves more engineering than the search logic. In priority order: delta evaluation (compute only a move's effect), batch vectorization (evaluate a population as one matrix expression, as in the MKP design), memoization (hash canonical solution forms when revisits are frequent), and surrogate screening (rank candidates with a cheap proxy, evaluate only the promising ones exactly). Profile first — measure what fraction of runtime evaluation takes before optimizing anything else.

### Tuning without self-deception

Tune behavioral parameters on a training instance set; report on a disjoint test set. Use racing or model-based tuners — Optuna's TPE (see **optuna-hyperparameter-tuning**) or irace (López-Ibáñez et al. 2016, "The irace package") — with the same per-run budget as the final experiments. Prefer scale-free parameterizations (mutation rate $c/n$, perturbation as a fraction of $n$, windows as a fraction of budget) so tuned values transfer across instance sizes. Then compare against baselines under the protocol of **algorithm-benchmarking-statistics**; a design decision justified only by one lucky seed is not a result.

## Practical Challenges

**The search improves fast, then flatlines far from any bound.** Over-intensification. Strengthen diversification: larger or adaptive kicks, softer acceptance (better-or-equal instead of strictly-better, or Metropolis), stagnation-triggered restarts from perturbed elites. Verify with the trace: if all improvement happens in the first 5% of the budget, the remaining 95% is being wasted in one basin.

**The population becomes near-identical copies within a few generations.** Selection pressure is too high relative to variation, and duplicates are not controlled. Reduce tournament size, add duplicate elimination at replacement (as in `population_search`), monitor entropy, and inject random immigrants when it collapses. If diversity dies repeatedly, the real problem is usually a crossover that produces children identical to parents.

**Most candidate solutions are infeasible and the search makes no progress.** The constraint-handling choice does not match constraint tightness. Static penalties fail when feasible solutions are sparse; switch to repair (as in the MKP design), a feasibility-enforcing decoder, or feasibility-preserving operators. If only a soft-constraint trade-off is intended, calibrate the penalty weight so that violation cost exceeds any achievable objective gain.

**Results vary wildly across seeds.** First rule out a bug: validate the best solutions of several runs with an independent feasibility and objective checker. If the algorithm is correct, run at least 10-30 seeds per instance and report distributions, not single values; high variance with a healthy mean usually means the budget is too small or acceptance is too random.

**The design works on toy instances but is unusable at production size.** Per-iteration cost grows superlinearly. Profile the evaluation share, add delta evaluation, restrict neighborhoods with candidate lists, vectorize population operations, and re-express parameters as functions of $n$ so behavior scales. Never tune at toy size and deploy at production size without re-checking.

**Tuned parameters do not transfer to new instances.** The tuning set leaked into the evaluation, or parameters were absolute instead of scale-free. Keep training and test instance sets disjoint, tune rates and fractions rather than absolute counts, and re-tune per instance family only when families differ structurally (tightness, size, correlation).

**No one can tell whether the metaheuristic is actually good.** There is no honest baseline. Implement random-restart local search and a greedy constructor as floors, run a MIP or CP solver under the same wall clock as a ceiling reference, report gaps to bounds or best-known values, and apply paired statistical tests across instances. "Our method found good solutions" without a baseline and a gap is not evidence.

**The objective is noisy (simulation-based or sampled scenarios).** Single evaluations mislead acceptance and selection. Fix a common scenario set per comparison (common random numbers), replicate evaluations of the incumbent and final candidates, and prefer rank-based selection, which is more robust to noise than threshold acceptance on raw values.

## Tools & Libraries

| Library | When to use | Note |
|---|---|---|
| numpy | every custom metaheuristic in this repo | vectorize population operations; always `np.random.default_rng(seed)` |
| scipy.optimize | continuous subproblems (`differential_evolution`, `dual_annealing`) | not suited to combinatorial structures directly |
| alns (PyPI) | ALNS with adaptive operator weights | clean separation of accept/stop/operator modules |
| DEAP | quick evolutionary prototyping | flexible but loop-heavy; slow for large populations |
| pymoo | multi-objective evolutionary algorithms | reference NSGA-II and quality indicators |
| nevergrad | gradient-free optimization portfolios | strong defaults for mixed parameter spaces |
| OR-Tools CP-SAT | exact baseline or exact repair subproblems | also a strong feasibility heuristic in its own right |
| Optuna | tuning behavioral parameters | TPE sampler with pruning; multi-instance objectives |
| irace (R package) | racing-based tuning, instance-aware | the de facto tuner in the metaheuristics literature |

## Output Format

A complete metaheuristic design deliverable contains six artifacts:

1. **Design-decision table** — one row per decision, with the rejected alternative and the reason. Example:

| Decision | Choice | Rejected alternative | Reason |
|---|---|---|---|
| Representation | permutation | random keys | native operators exist; decoder adds cost, loses locality |
| Constraint handling | none needed ($S=X$) | penalties | every permutation feasible |
| Construction | NEH | random start | few-percent gap at $O(n^2)$ evaluation cost |
| Local move | insertion, first improvement | swap | insertion dominates for flow-shop makespan |
| Diversification | adaptive k-reinsertion kick | full restart | preserves good substructure |
| Acceptance | better-or-equal | Metropolis | simplest control that allows plateau drift |
| Stopping | 60k evaluations + 15k stagnation window | wall clock only | hardware-independent, comparable |

2. **Parameter table** — every parameter with its value, class (structural/behavioral/budget), and how it was set (default, tuned with which tuner on which training set).
3. **Reproducible code** — explicit seeds for instance generation and search, an instance generator or instance files, and a single entry point that reruns everything.
4. **Results table** — one row per (instance, seed): best objective, time-to-best, evaluations used, wall-clock time; aggregated best/mean/std per instance; gap to bound or best-known where available.
5. **Convergence evidence** — best-so-far traces (the `trace` fields above) per seed; explicitly flag runs still improving at budget exhaustion, since they indicate the budget understates achievable quality.
6. **Independent validation** — a feasibility-and-objective checker that shares no code with the search, run on every reported solution.

## Questions to Ask

- What is the largest instance that must be solved, and in what wall-clock time?
- How expensive is one objective evaluation, and is incremental (delta) evaluation possible?
- Which constraints are hard, and which may be violated at a price?
- Has an exact solver been tried with a time limit, and what gap did it reach?
- What does "good enough" mean here — a gap, a target value, or beating an incumbent method?
- Is this a one-off solve or a repeatedly run production component (how much tuning effort is justified)?
- Is the objective deterministic, or noisy / simulation-based?
- Are real or benchmark instances available, and can synthetic ones be generated for tuning?
- Do good solutions plausibly share components worth recombining (population), or is the strength in the neighborhood (single-solution)?

## Related Skills

- **solution-encodings** — when the representation choice (binary, permutation, random keys, matrix) needs deeper selection criteria and operator-compatibility tables.
- **local-search-and-neighborhoods** — when designing the move set, delta evaluation, and scanning order for the intensification component.
- **constraint-handling-techniques** — when choosing among penalties, repair, decoders, and feasibility rules for hard constraints.
- **algorithm-benchmarking-statistics** — when comparing the designed metaheuristic against baselines with sound statistical protocols.
- **optuna-hyperparameter-tuning** — when tuning behavioral parameters on a training instance set without overtuning.
- **problem-formulation** — when the problem is not yet formalized or an exact model should be attempted before any heuristic.
