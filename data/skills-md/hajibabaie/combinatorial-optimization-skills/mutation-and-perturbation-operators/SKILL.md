---
name: mutation-and-perturbation-operators
description: When the user wants to design or tune mutation and perturbation operators — bit-flip, creep, Gaussian, polynomial; swap, insertion, inversion, scramble, segment moves for permutations; destroy-style perturbations; and mutation-strength adaptation. Also use when the user mentions "mutation operator," "bit flip," "swap mutation," "inversion mutation," "Gaussian mutation," "perturbation strength," "mutation rate," or when a metaheuristic stagnates and needs calibrated noise. For two-parent recombination, see crossover-operators; for improving-move design, see local-search-and-neighborhoods.
---

# Mutation and Perturbation Operators

You are an expert in variation-operator design for combinatorial and continuous metaheuristics. This skill is the reference catalog for unary operators: mutation inside evolutionary algorithms, kick moves inside iterated local search, proposal moves inside simulated annealing, and destroy-style perturbations inside ruin-and-recreate loops. Use the framework below to pick the operator that matches the encoding and the problem structure, implement it correctly in vectorized numpy, calibrate its strength, and adapt that strength during the run.

## Initial Assessment

Establish these points before recommending or writing any operator:

- **Encoding.** Binary string, integer vector, real vector, permutation, or a structured object (routes, schedules)? The encoding fixes the admissible operator family. If the encoding itself is still open, settle it first (see solution-encodings).
- **Role of the operator.** Three distinct roles use the same mechanics with different strengths:
  - *Variation in a population method* (GA/ES): small, applied to every offspring, rate-controlled.
  - *Kick in a trajectory method* (ILS): medium, applied once per local-search round, must escape the local-search neighborhood.
  - *Proposal in an acceptance-based method* (SA): small, applied every iteration, evaluated via delta.
- **What structure the objective rewards.** Adjacency (TSP edges), absolute position (QAP assignments), relative order (scheduling precedence), or subset membership (knapsack)? Pick the operator that perturbs the rewarded structure *least* per unit of randomization, unless the explicit goal is diversification.
- **Feasibility.** Does the operator preserve constraints (permutation operators preserve permutation feasibility) or can it produce infeasible offspring (bit-flip under a capacity constraint)? If infeasible, decide repair vs penalty before coding.
- **Evaluation cost.** If the objective supports O(1) or O(n) delta evaluation for a move, the same move doubles as a local-search neighborhood; design the operator so the delta formula applies.
- **Strength budget.** What disruption level is wanted: expected Hamming distance, number of tour edges changed, sigma as a fraction of variable range? Every operator must expose exactly one strength knob.
- **Adaptation requirements.** Fixed strength, deterministic schedule, feedback-driven adaptation, or self-adaptation encoded in the genome? Match the choice to run length and tuning budget.
- **Population vs single solution.** Population methods justify fully vectorized operators over an (m, n) array; trajectory methods need fast single-solution variants.
- **Reproducibility.** One `np.random.default_rng(seed)` per run, passed into every operator; never module-level `np.random.*` calls.
- **Time budget for tuning.** A fixed rate of 1/n is the right default when there is no budget; adaptive schemes pay off on long runs and unknown instances.

## Operator Anatomy and Disruption Control

A mutation operator is a sampling rule: given a solution $x$, it draws $x' = M(x)$ from a distribution over the search space concentrated near $x$. Its single most important characteristic is the induced disruption

$$\mathbb{E}\big[\,d(x, M(x))\,\big]$$

measured in the metric $d$ that the objective actually cares about: Hamming distance for binary strings, Euclidean distance for real vectors, and — for permutations — *edge distance* (shared adjacencies), *positional distance* (Hamming on positions), or *Kendall tau* (pairwise order inversions), depending on the problem. The classic design error is measuring disruption in the wrong metric: inversion of a long segment is a tiny move in edge distance (2 tour edges) but a huge move in positional distance, so it is gentle for TSP and violent for QAP.

Three properties to check for any operator:

1. **Reachability (ergodicity).** Repeated application must connect the whole search space; otherwise the algorithm can never reach some optima. Bit-flip with $p_m > 0$, swap, insertion, and inversion all satisfy this; creep with a step too small to cross the domain in available iterations effectively does not.
2. **Unbiasedness.** Absent selection, the operator should not drift toward particular solutions. Boundary handling is the usual offender for real vectors: clipping creates an atom of probability exactly on the bounds (demonstrated in code below).
3. **Scalability of strength.** The knob (rate $p_m$, step $\sigma$, segment length, removal count) must move expected disruption smoothly from "almost nothing" to "near restart."

For per-gene operators applied with rate $p_m$ to length-$n$ genomes:

$$\mathbb{E}[\text{genes changed}] = n\,p_m, \qquad \Pr[\text{child} = \text{parent}] = (1 - p_m)^n \approx e^{-n p_m}.$$

At the standard default $p_m = 1/n$ (Bäck 1993, "Optimal mutation rates in genetic search"), about $e^{-1} \approx 37\%$ of children are exact copies of their parent. If every child must differ, force at least one change (flip one uniformly chosen gene when the sampled mask is empty).

### Master operator catalog

| Operator | Encoding | Strength knob | Expected disruption | Cost per child | Typical use |
|---|---|---|---|---|---|
| Bit-flip | binary | rate $p_m$ | $n p_m$ Hamming | O(n) | GA on selection/subset problems |
| k-flip | binary | k | exactly k Hamming | O(n) | deterministic-strength studies, theory-style runs |
| Creep | integer | rate, max step | small drift per gene | O(n) | quantity/level genes (lot sizes, machine counts) |
| Gaussian | real | $\sigma$, rate | $\sigma$ per mutated gene | O(n) | ES, real-parameter GA, SA proposals |
| Polynomial | real (bounded) | $\eta_m$, rate | shrinks as $\eta_m$ grows | O(n) | NSGA-II-style bounded problems |
| Swap (exchange) | permutation | repetitions | 2 positions; ≤4 tour edges | O(n) copy | QAP, assignment-type objectives |
| Insertion (shift) | permutation | repetitions | 3 tour edges; 1 item reordered | O(n) | sequencing/scheduling |
| Inversion | permutation | segment length | 2 tour edges; heavy order change | O(n) | symmetric-TSP-like adjacency objectives |
| Scramble | permutation | segment length | up to L+1 edges; segment randomized | O(L) | diversification, restarts-in-place |
| Segment move (3-opt) | permutation | segment length | 3 tour edges; block relocated | O(n) | routing kicks, Or-opt-style perturbation |
| Double bridge (4-opt) | permutation | fixed | exactly 4 tour edges | O(n) | the canonical ILS kick for TSP |
| Ruin & recreate | structured | removal count | controlled, repair-aware | O(k·n) | routing/scheduling, large kicks with quality retention |

Decision guidance:

- **Use the mildest operator whose repeated application still escapes the trap you face.** For GA variation, start at $p_m = 1/n$ or one swap. For ILS kicks, the perturbation must leave the basin of the local search: a 2-opt local search is escaped by double bridge but usually *not* by a single inversion (which *is* a 2-opt move, hence immediately undoable).
- **Tie operator choice to the preserved structure.** Adjacency objective → inversion / segment move / double bridge. Position objective → swap. Order objective → insertion.
- **Prefer one strong knob to many weak ones.** Repetition count of a fixed atomic move is the cleanest strength parameter for permutations.
- **Treat repair as part of the operator.** If a repair step follows mutation, measure disruption *after* repair; aggressive repair can silently cancel the mutation (Practical Challenges below).

The parameter-control vocabulary used throughout comes from Eiben, Hinterding & Michalewicz (1999), "Parameter control in evolutionary algorithms": *deterministic* (preset schedule), *adaptive* (feedback from the run), and *self-adaptive* (strength encoded in the genome and evolved).

## Bit-Flip, k-Flip, and Creep Mutation

**Bit-flip** — when to use: any binary encoding (knapsack, set covering, feature selection). Complexity O(mn) for an (m, n) population, fully vectorizable. Fits: GA, (1+1) EA, binary PSO repair stages. **k-flip** — when to use: when disruption must be exact and tunable (strength studies, racing operators). **Creep** — when to use: ordinal integer genes where neighboring values have similar meaning; never use bit-flip on an integer encoded in base 2 (Hamming cliffs: 7→8 flips four bits).

```python
import numpy as np


def bitflip_mutation(pop: np.ndarray, rate: float, rng: np.random.Generator) -> np.ndarray:
    """Flip each bit independently with probability `rate`; pop is an (m, n) 0/1 array."""
    mask = rng.random(pop.shape) < rate
    return np.where(mask, 1 - pop, pop)


def kflip_mutation(pop: np.ndarray, k: int, rng: np.random.Generator) -> np.ndarray:
    """Flip exactly k distinct, uniformly chosen bits per individual."""
    m, n = pop.shape
    ranks = rng.random((m, n)).argsort(axis=1)      # row-wise random permutation of columns
    mask = ranks < k
    return np.where(mask, 1 - pop, pop)


def creep_mutation(
    pop: np.ndarray, low: int, high: int, rate: float, max_step: int, rng: np.random.Generator
) -> np.ndarray:
    """Add a uniform step in {-max_step..-1, 1..max_step} to each gene with probability `rate`."""
    step = rng.integers(1, max_step + 1, size=pop.shape) * rng.choice([-1, 1], size=pop.shape)
    mask = rng.random(pop.shape) < rate
    return np.clip(np.where(mask, pop + step, pop), low, high)


rng = np.random.default_rng(0)
pop = rng.integers(0, 2, size=(1000, 50))
kids = bitflip_mutation(pop, rate=1.0 / 50, rng=rng)
flips = (kids != pop).sum(axis=1)
print(f"mean flips per child: {flips.mean():.2f}, unchanged children: {(flips == 0).mean():.2f}")
# Expected: mean flips ~ 1.0 and ~0.36 of children identical to their parent
# (e^-1) -- switch to kflip_mutation(pop, 1, rng) when every child must differ.
```

Strength guidance: $p_m = 1/n$ is the default; $p_m \in [1/n, 4/n]$ is the useful range for most GAs. Rates near $0.5$ turn mutation into uniform random sampling and destroy inheritance. For creep, `max_step` around 5-10% of the domain width keeps locality; pair a small-step creep (exploitation) with a rare large jump (exploration) rather than inflating one step size.

## Gaussian and Polynomial Mutation (Real Vectors)

**Gaussian mutation** — when to use: unbounded or softly bounded real genes; the canonical ES mutation. Complexity O(mn). Fits: evolution strategies, real-coded GA, SA on continuous relaxations. The strength knob is $\sigma$, best expressed as a fraction of the variable range (start near 5-10%). Boundary handling matters: *clip* is biased (probability atom on the bound), *reflect* keeps samples interior, *resample* is unbiased but loops.

```python
import numpy as np


def gaussian_mutation(
    pop: np.ndarray,
    sigma: float,
    low: float,
    high: float,
    rate: float,
    rng: np.random.Generator,
    bounds: str = "reflect",
) -> np.ndarray:
    """Add N(0, sigma^2) noise to each gene with probability `rate`, then handle bounds.

    bounds: 'clip' (fast, biased onto the bound), 'reflect' (mirror back into
    [low, high]), or 'resample' (redraw offending noise until feasible).
    """
    span = high - low
    noise = rng.normal(0.0, sigma, size=pop.shape)
    mask = rng.random(pop.shape) < rate
    out = pop + np.where(mask, noise, 0.0)
    if bounds == "clip":
        return np.clip(out, low, high)
    if bounds == "reflect":
        t = np.mod(out - low, 2.0 * span)
        return low + span - np.abs(t - span)
    while True:                                     # resample
        bad = (out < low) | (out > high)
        if not bad.any():
            return out
        redraw = pop + rng.normal(0.0, sigma, size=pop.shape)
        out = np.where(bad, redraw, out)


rng = np.random.default_rng(42)
x = np.full((10000, 1), 0.05)                       # parent sitting near the lower bound
for mode in ("clip", "reflect"):
    y = gaussian_mutation(x, sigma=0.2, low=0.0, high=1.0, rate=1.0, rng=rng, bounds=mode)
    print(f"{mode:>8}: mean={y.mean():.3f}, share exactly on bound={(y == 0.0).mean():.2f}")
# Expected: clip parks ~0.40 of all children exactly at 0.0; reflect leaves no
# probability atom on the bound. Use reflect or resample whenever optima may
# lie near, but not on, the boundary.
```

**Polynomial mutation** (Deb & Goyal 1996; the NSGA-II default) — when to use: bounded real genes where perturbation should automatically shrink near the bounds. The distribution index $\eta_m$ is the strength knob: larger $\eta_m$ concentrates children near the parent; $\eta_m = 20$ is the standard setting, $\eta_m \in [5, 50]$ the practical range. Complexity O(mn). Fits: real-coded GA/NSGA-II, memetic real-vector methods.

```python
import numpy as np


def polynomial_mutation(
    pop: np.ndarray, low: float, high: float, eta: float, rate: float, rng: np.random.Generator
) -> np.ndarray:
    """Bounded polynomial mutation (Deb & Goyal 1996). Larger eta = smaller steps."""
    span = high - low
    d1 = (pop - low) / span                         # normalized distance to lower bound
    d2 = (high - pop) / span                        # normalized distance to upper bound
    u = rng.random(pop.shape)
    lo_branch = (2.0 * u + (1.0 - 2.0 * u) * (1.0 - d1) ** (eta + 1.0)) ** (1.0 / (eta + 1.0)) - 1.0
    hi_branch = 1.0 - (2.0 * (1.0 - u) + 2.0 * (u - 0.5) * (1.0 - d2) ** (eta + 1.0)) ** (1.0 / (eta + 1.0))
    deltaq = np.where(u < 0.5, lo_branch, hi_branch)
    mask = rng.random(pop.shape) < rate
    return np.clip(np.where(mask, pop + deltaq * span, pop), low, high)


rng = np.random.default_rng(7)
x = np.full((20000, 1), 0.5)
for eta in (2.0, 20.0, 100.0):
    y = polynomial_mutation(x, low=0.0, high=1.0, eta=eta, rate=1.0, rng=rng)
    print(f"eta={eta:5.0f}: std of step = {np.std(y - x):.4f} (fraction of range)")
# Expected: step std shrinks monotonically with eta -- roughly 0.24 of the
# range at eta=2, 0.06 at eta=20, 0.014 at eta=100. Pick eta to hit the step
# size you would have chosen as sigma for Gaussian mutation.
```

The polynomial form is bound-aware by construction: as the parent approaches a bound, the step distribution toward that bound contracts, so no repair atom appears. Prefer it over Gaussian-plus-clip on box-constrained problems.

## Permutation Mutation Catalog (worked example: disruption on TSP)

Per-operator guidance — all preserve permutation feasibility, all cost O(n) per application due to array copying:

- **Swap (exchange).** Pick two positions, exchange contents. Minimal positional disruption (2 positions), but breaks up to 4 tour edges. Fits QAP, assignment-type encodings, SA proposals on positional objectives. Worst choice for TSP relative to its disruption.
- **Insertion (shift).** Remove one element, reinsert elsewhere. Breaks 3 tour edges; preserves the relative order of everything else. The natural unit move for sequencing problems (flow shop, single machine) and the atomic move behind Or-opt.
- **Inversion (segment reversal).** Reverse a contiguous segment. Breaks exactly 2 edges in a symmetric tour — it *is* a random 2-opt move — while reversing the order of the whole segment. Ideal for TSP-like objectives; poor for position/order objectives where it is maximally destructive.
- **Scramble.** Shuffle a contiguous segment uniformly. Strength scales with segment length L (up to L+1 edges broken). Use for diversification bursts, not as a routine variation operator.
- **Segment move (3-opt style).** Cut a segment, optionally reverse it, reinsert at another point. Breaks 3 edges; equivalent to a random Or-opt/3-opt move. Good mid-strength routing kick.
- **Double bridge (4-opt).** Cut the tour into four parts A|B|C|D and reconnect as A-D-C-B — equivalently, exchange the two non-adjacent blocks B and D. Breaks exactly 4 edges, reverses nothing, and — the key property — cannot be undone by any single 2-opt move, which makes it the canonical ILS kick (Martin, Otto & Felten 1991, "Large-step Markov chains"; Lourenço, Martin & Stützle 2003, ILS handbook chapter). Beware a common implementation slip: reconnecting as A-C-B-D exchanges *adjacent* blocks, breaks only 3 edges, and is just a segment move.

### Structure preserved vs destroyed

| Operator | Tour edges broken | Relative order | Absolute positions | Best-fit problems |
|---|---|---|---|---|
| Swap | ≤ 4 | nearly all kept | 2 changed | QAP, assignment |
| Insertion | 3 | kept except moved item | shifted by one in between | flow shop, sequencing |
| Inversion | 2 | segment fully reversed | segment fully reversed | symmetric TSP |
| Scramble | ≤ L+1 | destroyed inside segment | destroyed inside segment | diversification |
| Segment move | 3 | block kept internally | block relocated | routing (Or-opt kick) |
| Double bridge | exactly 4 | mostly kept | quarter blocks relocated | ILS kicks for TSP/routing |

The experiment below applies every operator to a 2-opt local optimum and measures (a) edges broken — the structural disruption — and (b) mean relative length increase — the fitness damage. Starting from a local optimum is essential: on a random tour the mean length change is near zero and tells you nothing.

```python
import numpy as np


def tour_length(tour: np.ndarray, dist: np.ndarray) -> float:
    """Length of the closed tour."""
    return float(dist[tour, np.roll(tour, -1)].sum())


def tour_edges(tour: np.ndarray) -> set[frozenset[int]]:
    """Undirected edge set of the closed tour."""
    return {frozenset((int(a), int(b))) for a, b in zip(tour, np.roll(tour, -1))}


def two_opt(tour: np.ndarray, dist: np.ndarray) -> np.ndarray:
    """First-improvement 2-opt to a local optimum (reference baseline, not tuned)."""
    tour, n = tour.copy(), tour.size
    improved = True
    while improved:
        improved = False
        for i in range(n - 2):
            for j in range(i + 2, n - (i == 0)):
                a, b, c, d = tour[i], tour[i + 1], tour[j], tour[(j + 1) % n]
                if dist[a, c] + dist[b, d] - dist[a, b] - dist[c, d] < -1e-12:
                    tour[i + 1 : j + 1] = tour[i + 1 : j + 1][::-1]
                    improved = True
    return tour


def swap(p: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Exchange the contents of two distinct positions."""
    i, j = rng.choice(p.size, size=2, replace=False)
    q = p.copy()
    q[[i, j]] = q[[j, i]]
    return q


def insertion(p: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Remove one element and reinsert it at a uniformly chosen slot."""
    i = int(rng.integers(p.size))
    q = np.delete(p, i)
    return np.insert(q, int(rng.integers(q.size + 1)), p[i])


def inversion(p: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Reverse a random contiguous segment (a random 2-opt move)."""
    i, j = np.sort(rng.choice(p.size, size=2, replace=False))
    q = p.copy()
    q[i : j + 1] = q[i : j + 1][::-1]
    return q


def scramble(p: np.ndarray, rng: np.random.Generator, seg: int = 8) -> np.ndarray:
    """Uniformly shuffle a random segment of length `seg`."""
    i = int(rng.integers(p.size - seg))
    q = p.copy()
    q[i : i + seg] = rng.permutation(q[i : i + seg])
    return q


def segment_move(p: np.ndarray, rng: np.random.Generator, seg: int = 5) -> np.ndarray:
    """Cut a segment, reverse it with probability 1/2, reinsert elsewhere (3-opt style)."""
    i = int(rng.integers(p.size - seg))
    block = p[i : i + seg][:: -1 if rng.random() < 0.5 else 1].copy()
    rest = np.concatenate([p[:i], p[i + seg :]])
    j = int(rng.integers(rest.size + 1))
    return np.concatenate([rest[:j], block, rest[j:]])


def double_bridge(p: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Classic 4-opt double bridge: A|B|C|D -> A D C B (swaps non-adjacent blocks B, D)."""
    a, b, c = np.sort(rng.choice(np.arange(1, p.size), size=3, replace=False))
    return np.concatenate([p[:a], p[c:], p[b:c], p[a:b]])


rng = np.random.default_rng(7)
n = 60
pts = rng.random((n, 2))
dist = np.linalg.norm(pts[:, None, :] - pts[None, :, :], axis=2)
base = two_opt(rng.permutation(n), dist)
base_len, base_edges = tour_length(base, dist), tour_edges(base)

catalog = {"swap": swap, "insertion": insertion, "inversion": inversion,
           "scramble": scramble, "segment-move": segment_move, "double-bridge": double_bridge}
print(f"{'operator':>14} {'edges broken':>13} {'mean dLen %':>12}")
for name, op in catalog.items():
    broken, dlen = [], []
    for _ in range(500):
        q = op(base, rng)
        broken.append(len(base_edges - tour_edges(q)))
        dlen.append(100.0 * (tour_length(q, dist) - base_len) / base_len)
    print(f"{name:>14} {np.mean(broken):13.2f} {np.mean(dlen):12.2f}")
# Expected (n=60, from a 2-opt local optimum): edges broken -- inversion exactly
# 2 (it IS a random 2-opt move), insertion ~3, segment-move ~3, swap ~4,
# double-bridge exactly 4, scramble ~7. Length damage tracks how many LONG
# random edges are introduced, not the raw edge count: swap and double-bridge
# (~25%) add 4 spatially uncorrelated edges each; scramble's ~7 new edges stay
# inside one short window (~19%); inversion is mildest (~13%). Swap pays the
# top damage for a tiny positional change -- a structure-mismatched operator.
```

Reading the table: for an ILS on TSP, double bridge gives a *fixed* structural change of exactly 4 edges that 2-opt cannot revert in one move — exactly what a kick needs; the local search recovers most of the length damage but lands in a different basin. Inversion looks attractive (least damage) but is useless as a kick on top of 2-opt: the local search undoes it immediately. For a GA on QAP, the same logic inverts — swap is the natural mutation because position is what the QAP objective prices, and a swap admits O(n) delta evaluation.

## Destroy-Style Perturbations and Strength Control

Destroy-style (ruin-and-recreate) perturbation removes a controlled part of the solution and rebuilds it greedily (Schrimpf et al. 2000, "Record breaking optimization results using the ruin & recreate principle"). It differs from atomic mutations in two ways: the strength knob is the *removal count* (directly interpretable), and the repair step injects problem knowledge, so even large perturbations land on reasonable solutions. This is the standard strong kick for routing and scheduling, and the conceptual bridge to ALNS.

```python
import numpy as np


def tour_length(tour: np.ndarray, dist: np.ndarray) -> float:
    """Length of the closed tour."""
    return float(dist[tour, np.roll(tour, -1)].sum())


def nearest_neighbor_tour(dist: np.ndarray, start: int = 0) -> np.ndarray:
    """Greedy nearest-neighbor construction."""
    n = dist.shape[0]
    tour, free = [start], np.ones(n, dtype=bool)
    free[start] = False
    for _ in range(n - 1):
        nxt = int(np.argmin(np.where(free, dist[tour[-1]], np.inf)))
        tour.append(nxt)
        free[nxt] = False
    return np.array(tour)


def cheapest_insertion(tour: list[int], city: int, dist: np.ndarray) -> list[int]:
    """Insert `city` at the position with the smallest length increase."""
    t = np.array(tour)
    nxt = np.roll(t, -1)
    inc = dist[t, city] + dist[city, nxt] - dist[t, nxt]
    pos = int(np.argmin(inc)) + 1
    return tour[:pos] + [city] + tour[pos:]


def ruin_recreate(
    tour: np.ndarray, dist: np.ndarray, n_remove: int, rng: np.random.Generator, mode: str = "segment"
) -> np.ndarray:
    """Remove `n_remove` cities (contiguous segment or scattered), greedily reinsert."""
    n = tour.size
    if mode == "segment":
        idx = (int(rng.integers(n)) + np.arange(n_remove)) % n
    else:                                            # scattered random removal
        idx = rng.choice(n, size=n_remove, replace=False)
    removed = tour[idx]
    partial = np.delete(tour, idx).tolist()
    for city in rng.permutation(removed):
        partial = cheapest_insertion(partial, int(city), dist)
    return np.array(partial)


rng = np.random.default_rng(11)
pts = rng.random((80, 2))
dist = np.linalg.norm(pts[:, None, :] - pts[None, :, :], axis=2)
tour = nearest_neighbor_tour(dist)
base = tour_length(tour, dist)
for mode in ("segment", "random"):
    lens = [tour_length(ruin_recreate(tour, dist, n_remove=12, rng=rng, mode=mode), dist)
            for _ in range(30)]
    print(f"{mode:>8}: mean dLen = {100.0 * (np.mean(lens) - base) / base:+.1f}%")
# Expected: both removal modes land within a few percent of the starting tour;
# on a nearest-neighbor start the greedy repair often *shortens* the tour
# (negative delta) -- destroy-repair perturbs and partially re-optimizes at
# once, which is why 10-25% removal makes a usable kick where a 25-element
# scramble would be a near restart.
```

Removal-mode guidance: *segment* removal targets one spatial region (strong local reshuffle); *scattered* removal spreads disruption thinly. A third standard option, *related removal* (remove items similar by distance/time), interpolates between them. Strength: removing 10-25% of elements is the usual kick range; beyond ~40% the repair heuristic dominates and the result no longer resembles the parent.

### Worked example: adaptive mutation rates on a knapsack GA

Mutation strength control is where most GA tuning effort should go. The experiment compares three policies from the Eiben-Hinterding-Michalewicz taxonomy on a weakly correlated 0-1 knapsack with greedy repair: fixed $p_m = 1/n$, self-adaptive per-individual rates (log-normal update, inherited through crossover), and stagnation-triggered doubling (rate escalates while the best value stalls, resets on improvement).

```python
import numpy as np


def make_knapsack(n: int, seed: int) -> tuple[np.ndarray, np.ndarray, float]:
    """Weakly correlated 0-1 knapsack instance (harder than uncorrelated)."""
    rng = np.random.default_rng(seed)
    weights = rng.integers(1, 31, size=n).astype(float)
    values = weights + rng.integers(1, 11, size=n).astype(float)
    return weights, values, 0.5 * float(weights.sum())


def dantzig_bound(weights: np.ndarray, values: np.ndarray, cap: float) -> float:
    """LP-relaxation upper bound: fill by ratio, fractional break item."""
    order = np.argsort(-values / weights)
    w_s, v_s = weights[order], values[order]
    cum = np.cumsum(w_s)
    k = int(np.searchsorted(cum, cap, side="right"))
    bound = float(v_s[:k].sum())
    if k < weights.size:
        used = float(cum[k - 1]) if k > 0 else 0.0
        bound += float(v_s[k]) * (cap - used) / float(w_s[k])
    return bound


def repair(pop: np.ndarray, weights: np.ndarray, values: np.ndarray, cap: float) -> np.ndarray:
    """Vectorized greedy repair: drop selected items in ascending value/weight order."""
    order = np.argsort(values / weights)             # worst ratio first
    sel_w = pop[:, order] * weights[order]
    need = sel_w.sum(axis=1, keepdims=True) - cap
    cum = np.cumsum(sel_w, axis=1)
    drop = (need > 0) & (sel_w > 0) & (cum - sel_w < need)
    fixed = pop[:, order].copy()
    fixed[drop] = 0
    out = np.empty_like(pop)
    out[:, order] = fixed
    return out


def run_ga(policy: str, weights: np.ndarray, values: np.ndarray, cap: float,
           seed: int, gens: int = 300, m: int = 80) -> float:
    """Binary GA with repair; the mutation-rate control policy is the only difference."""
    rng = np.random.default_rng(seed)
    n = weights.size
    base = 1.0 / n
    pop = repair((rng.random((m, n)) < 0.3).astype(np.int64), weights, values, cap)
    rates = np.full(m, base)
    best, stall = -np.inf, 0
    for _ in range(gens):
        fit = pop @ values
        if fit.max() > best + 1e-9:
            best, stall = float(fit.max()), 0
        else:
            stall += 1
        cand = rng.integers(0, m, size=(2, m))       # binary tournament selection
        parents = np.where(fit[cand[0]] >= fit[cand[1]], cand[0], cand[1])
        half = m // 2
        pa, pb = pop[parents[:half]], pop[parents[half:]]
        mask = rng.random(pa.shape) < 0.5            # uniform crossover
        kids = np.concatenate([np.where(mask, pa, pb), np.where(mask, pb, pa)])
        if policy == "fixed":
            kid_rates = np.full(m, base)
        elif policy == "self-adaptive":              # rate travels with the genome
            inherited = np.tile(0.5 * (rates[parents[:half]] + rates[parents[half:]]), 2)
            kid_rates = np.clip(inherited * np.exp(0.22 * rng.standard_normal(m)),
                                0.2 * base, 8.0 * base)
        else:                                        # stagnation-triggered doubling
            kid_rates = np.full(m, base * min(2.0 ** (stall // 15), 16.0))
        flip = rng.random((m, n)) < kid_rates[:, None]
        kids = repair(np.where(flip, 1 - kids, kids), weights, values, cap)
        elite = int(np.argmax(fit))
        kids[0], kid_rates[0] = pop[elite], rates[elite]   # 1-elitism
        pop, rates = kids, kid_rates
    return best


weights, values, cap = make_knapsack(100, seed=3)
print(f"LP upper bound: {dantzig_bound(weights, values, cap):.1f}")
for policy in ("fixed", "self-adaptive", "stagnation"):
    res = [run_ga(policy, weights, values, cap, seed=s) for s in range(5)]
    print(f"{policy:>14}: mean best {np.mean(res):.1f}, worst seed {np.min(res):.1f}")
# Expected: all three policies finish within ~0.2% of the LP upper bound (the
# integral optimum lies slightly below it), and fixed 1/n is NOT beaten on this
# single moderate instance -- adaptive control earns its keep on longer runs,
# tighter capacities, and unseen instances, which is exactly why a fixed-rate
# baseline is mandatory in any adaptive-mutation comparison.
```

Interpretation rules: adaptive control buys robustness, not magic. On short runs or well-tuned fixed rates, "fixed 1/n" is hard to beat; adaptive and self-adaptive policies pay off when instances vary, runs are long, or tuning budget is zero. Always compare against the fixed-rate baseline before adopting an adaptive scheme.

### Strength-control parameter guidance

| Policy | Knob(s) | Typical setting | Trade-off |
|---|---|---|---|
| Fixed rate | $p_m$ | $1/n$ | zero tuning, no reaction to stagnation |
| Deterministic schedule | decay law | $\sigma_t = \sigma_0 (\sigma_f/\sigma_0)^{t/T}$ | predictable; wrong if budget T changes |
| 1/5 success rule | window, factor | factor 0.85, window 10-50 | great for (1+1)-style; noisy signals on populations |
| Stagnation-triggered | patience, cap | double every 15-25 stale gens, cap 16x | simple, effective; patience must exceed normal stall time |
| Self-adaptive | learning rate $\tau$ | $\tau = 1/\sqrt{2n}$ | no external signal needed; slow on small populations |
| Heavy-tailed | exponent $\beta$ | $\beta = 1.5$ | one operator covers all strengths; fat tail wastes some evals |

## Advanced Techniques

### Self-adaptive step sizes (log-normal rule)

Encode $\sigma$ in the genome, mutate it first with a log-normal factor, then mutate the object variables with the *new* $\sigma$ (Schwefel 1981). Selection then favors individuals whose $\sigma$ produced good offspring — strength adapts without any external feedback signal. Order matters: mutating $\sigma$ after the variables decouples the step size from the success it caused.

```python
import numpy as np
from collections.abc import Callable


def sphere(Y: np.ndarray) -> np.ndarray:
    """Batch sphere function, the standard step-size testbed."""
    return np.sum(Y * Y, axis=1)


def self_adaptive_es(
    f: Callable[[np.ndarray], np.ndarray],
    n: int = 10, mu: int = 5, lam: int = 35, gens: int = 250, seed: int = 1,
) -> tuple[float, float]:
    """(mu, lambda)-ES with log-normal per-individual step-size self-adaptation."""
    rng = np.random.default_rng(seed)
    tau = 1.0 / np.sqrt(2.0 * n)
    X = rng.normal(0.0, 3.0, size=(mu, n))
    sigma = np.full(mu, 1.0)
    for _ in range(gens):
        idx = rng.integers(0, mu, size=lam)
        sig_kids = sigma[idx] * np.exp(tau * rng.standard_normal(lam))  # sigma first
        Y = X[idx] + sig_kids[:, None] * rng.standard_normal((lam, n))
        keep = np.argsort(f(Y))[:mu]
        X, sigma = Y[keep], sig_kids[keep]
    fx = f(X)
    b = int(np.argmin(fx))
    return float(fx[b]), float(sigma[b])


best_f, final_sigma = self_adaptive_es(sphere)
print(f"best f = {best_f:.2e}, final sigma = {final_sigma:.2e}")
# Expected: f drops many orders of magnitude (well below 1e-6) and sigma
# shrinks in step with the distance to the optimum -- the run "tunes itself."
```

### The 1/5 success rule

Rechenberg (1973): track the fraction of mutations that improve the parent over a window; if it exceeds $1/5$, *increase* the step ($\sigma \leftarrow \sigma / 0.85$), if below, decrease ($\sigma \leftarrow \sigma \cdot 0.85$). Rationale: too-high success means steps are timidly small; too-low success means steps overshoot. Apply per restart or per window of 10-50 mutations. The same logic transfers to discrete strengths — adjust the number of swaps in a kick by tracking how often the following local search accepts the perturbed solution.

### Heavy-tailed mutation (fast GA)

Sampling the flip count $k$ from a power law $P(k) \propto k^{-\beta}$ on $\{1, \dots, n/2\}$ with $\beta \approx 1.5$ gives mostly local steps plus occasional large jumps in one parameter-free operator (Doerr, Le, Makhmara & Nguyen 2017, "Fast genetic algorithms"). It provably accelerates escaping fitness valleys compared to the fixed $1/n$ rate, at modest cost on easy slopes.

```python
import numpy as np


def power_law_flip(pop: np.ndarray, beta: float, rng: np.random.Generator) -> np.ndarray:
    """Flip exactly k bits per child with P(k) ~ k^-beta on {1..n//2} (fast GA)."""
    m, n = pop.shape
    ks = np.arange(1, n // 2 + 1)
    p = ks.astype(float) ** -beta
    p /= p.sum()
    k = rng.choice(ks, size=m, p=p)
    ranks = rng.random((m, n)).argsort(axis=1)
    return np.where(ranks < k[:, None], 1 - pop, pop)


rng = np.random.default_rng(5)
pop = rng.integers(0, 2, size=(20000, 100))
flips = (power_law_flip(pop, beta=1.5, rng=rng) != pop).sum(axis=1)
print(f"median k = {np.median(flips):.0f}, mean k = {flips.mean():.1f}, max k = {flips.max()}")
# Expected: median k around 2, mean around 5-6, occasional children with k near
# 50 -- one operator spans local search steps and near-restart jumps.
```

### Stagnation- and diversity-triggered control

Couple the strength knob to an observable run signal. Two robust recipes: (a) *stagnation*: multiply strength by 2 every `patience` generations without improvement, reset on improvement, cap at 8-16x base (implemented in the knapsack GA above); (b) *diversity*: when mean pairwise population distance falls below a threshold (say 10% of its initial value), raise the mutation rate or fire a scramble/ruin burst on the worst half of the population. Diversity-triggered control reacts earlier than stagnation but needs a cheap distance proxy (Hamming on binary, shared-edge count on permutations).

### Distance-calibrated permutation perturbation

To hit a *target* disruption (e.g., "perturb to Kendall-tau distance ~k"), compose k atomic moves: k random insertions yield roughly k order displacements; k swaps yield ~2k positional changes; k inversions yield ~2k broken edges. Calibrate empirically with the disruption-measurement harness above — measure $\mathbb{E}[d(x, M^k(x))]$ as a function of k once per problem class, then expose k as the single strength knob of the composed operator. This is the standard way to give ILS a tunable kick: strength 1 = one double bridge, strength s = s double bridges, adapted by the 1/5-style rule.

## Practical Challenges

**Mutation silently does nothing.** With $p_m = 1/n$, ~37% of children are clones; with swap mutation, sampling i = j (when allowed) or scrambling a sorted segment can return the parent. If the algorithm relies on every child being new (duplicate elimination, strict steady-state), force a change: use k-flip with k ≥ 1, sample positions without replacement, and resample on identity.

**Clipping concentrates the population on the bounds.** Gaussian-plus-clip places a probability atom exactly on box bounds; after selection, genes pile up there even when the optimum is interior. Use reflection, resampling, or polynomial mutation. Detect it cheaply: report the fraction of genes exactly equal to a bound each generation; anything above a few percent (when the optimum is not known to be on the bound) signals the bias.

**The operator perturbs the wrong structure.** Swap mutation on TSP breaks 4 edges to achieve a 2-position change nobody priced; inversion on QAP reverses a whole segment of assignments to achieve a 2-edge change nobody priced. Diagnose with the disruption table: measure edges broken *and* positions changed, and check which one correlates with fitness damage on your objective.

**Local search undoes the kick.** In memetic algorithms and ILS, any perturbation inside the local-search neighborhood is wasted: 2-opt reverts a single inversion immediately. The kick must be outside the neighborhood's reach — double bridge against 2-opt, multi-segment ruin against single-route local search. Verify empirically: if the local search returns to the pre-kick solution more than ~30% of the time, the kick is too weak or not orthogonal enough.

**Repair cancels the mutation.** With greedy repair (knapsack, capacity constraints), a mutation that adds items beyond capacity is often exactly reverted by the repair dropping the same items. Measure disruption *after* repair; if post-repair Hamming distance is near zero, bias the mutation (flip 1→0 and 0→1 with different rates) or randomize the repair order.

**Rate semantics confusion.** "Mutation probability 0.1" means either *per gene* (expected 0.1n changes — huge) or *per individual* (one mutation applied to 10% of children — tiny). Papers mix both conventions. Always state the convention and the resulting expected disruption ($n p_m$ genes) when reporting parameters.

**Strength schedule decays too fast.** Exponentially decaying $\sigma$ or rate tuned on short test runs collapses to zero halfway through a long production run, freezing the search. Tie schedules to the *fraction* of the budget ($t/T$), not absolute iterations, and put a floor (e.g., $\sigma_f = 10^{-3} \cdot$ range, $p_m \ge 1/(4n)$) under every schedule.

**Irreproducible runs.** Operators that call `np.random.*` module-level functions or create their own generators internally make seeds meaningless and parallel runs correlated. Pass one `np.random.default_rng(seed)` per run through every operator call, and log the seed with every result row.

## Tools & Libraries

| Library | When to use | Note |
|---|---|---|
| numpy | always — the implementation substrate here | `default_rng`, `argsort`-rank tricks for per-row k-flips, broadcasting for population ops |
| DEAP | quick GA/ES prototypes | `tools.mutFlipBit`, `mutGaussian`, `mutShuffleIndexes`; operators are list-based, slow at scale |
| pymoo | bounded real and multi-objective work | reference `PolynomialMutation` (`eta`), `BitflipMutation`; clean operator interfaces |
| jMetalPy | metaheuristic experiments with many built-ins | permutation and real mutations with consistent APIs |
| scipy.stats | heavy-tailed step distributions | `zipfian`/custom discrete laws for power-law flip counts; `truncnorm` for bounded Gaussian |
| numba | hot single-solution loops (SA/ILS inner moves) | JIT the delta-evaluation + move pair when numpy vectorization does not apply |

## Output Format

A complete operator-design deliverable contains:

1. **Operator selection table** — one row per candidate operator: encoding, structure preserved, strength knob, expected disruption in the problem's metric, complexity per application, and the verdict with one-line justification.
2. **Strength and adaptation spec** — base strength (e.g., $p_m = 1/n = 0.01$), control policy (fixed / schedule / adaptive / self-adaptive), trigger and bounds (e.g., "double after 20 stale generations, cap 16x, reset on improvement"), and the convention used (per-gene vs per-individual).
3. **Disruption measurement report** — the harness output: for each operator and strength level, mean structural disruption (Hamming / edges broken / Kendall tau) and mean fitness damage from a locally optimal starting point, over ≥ 500 samples with a fixed seed. Example:

   | operator | strength | edges broken | mean fitness damage |
   |---|---|---|---|
   | inversion | 1 move | 2.0 | smallest |
   | double bridge | 1 move | 4.0 | high |
   | scramble | seg = 8 | ~7.0 | moderate (new edges stay local) |

4. **Integration notes** — where the operator sits in the loop (after crossover, as ILS kick, as SA proposal), interaction with repair (disruption measured post-repair), and whether the move admits delta evaluation.
5. **Reproducible code** — operator functions taking `(solution_or_population, ..., rng)` with type hints; one `np.random.default_rng(seed)` per run; a smoke test on a tiny synthetic instance with an `# Expected:` line.
6. **Validation checklist** — child feasibility verified by an independent checker (permutation property, bounds, capacity), no-op rate reported, boundary-atom fraction reported for bounded real operators, and a fixed-strength baseline included in any adaptive-policy comparison.

## Questions to Ask

- What is the encoding, and is it fixed — or can the representation still change?
- Is the operator a GA variation step, an ILS/SA move, or a kick that must escape a specific local search?
- What structure does the objective price: adjacency, position, order, or membership?
- Can mutation produce infeasible solutions, and is there a repair or penalty already in place?
- Is delta evaluation available for the candidate move, and is it expected to be used?
- What run budget applies — short tuned runs (fixed strength) or long/varied runs (adaptive strength)?
- How is disruption going to be measured for this problem — which distance metric?
- What no-op and clone tolerance does the surrounding algorithm have (duplicate elimination, strict elitism)?
- Are populations involved, making vectorized (m, n) operators worthwhile?
- Which seeds and how many replications will back any operator comparison?

## Related Skills

- **crossover-operators** — when two-parent recombination must be designed alongside mutation; preservation properties there mirror the disruption analysis here.
- **local-search-and-neighborhoods** — when the same atomic moves are used as systematic improving steps with delta evaluation instead of random perturbations.
- **iterated-local-search** — when the perturbation is the kick inside an ILS loop and its strength must defeat a specific local search.
- **solution-encodings** — when the representation is still open; the encoding decision constrains which operators in this catalog apply.
- **simulated-annealing** — when mutations serve as proposal moves under Metropolis acceptance and strength interacts with the temperature schedule.
