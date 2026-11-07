---
name: quadratic-assignment-problem
description: When the user wants to model or solve the quadratic assignment problem — assigning n facilities to n locations to minimize the total flow-times-distance cost — with linearized MIP models or robust tabu search built on O(n) swap delta evaluation. Also use when the user mentions "quadratic assignment," "QAP," "flow distance," "QAPLIB," "facility layout," or "Koopmans-Beckmann," or when pairwise interaction costs depend on a permutation. For linear assignment without interaction terms, see assignment-problems; for choosing among product linearizations, see linearization-techniques.
---

# Quadratic Assignment Problem

You are an expert in the quadratic assignment problem (QAP). This skill covers the
flow-times-distance objective, MIP linearizations and why exact solving stalls around
n = 30, Gilmore-Lawler bounds, robust tabu search as the heuristic method of choice,
O(n) and amortized-O(1) delta evaluation, QAPLIB instances and validation. Use the
framework below to pick a formulation, build correct code, and report defensible results.

## Initial Assessment

Establish the following before recommending a model or writing code:

- **Instance size n.** The single most important fact. n ≤ 15: any exact model works.
  n ≤ 25-30: exact is possible with effort and time. n > 30: plan for heuristics,
  with bounds only for gap reporting.
- **Symmetry and diagonals.** Are F and D symmetric with zero diagonals? Most QAPLIB
  instances are. The fast delta-evaluation formulas below assume it; the general
  formulas cost the same asymptotically but more constants. Check before coding.
- **Linear term.** Is there a fixed cost b_ik for placing facility i at location k
  (Koopmans-Beckmann with linear part)? It changes the objective but not the structure.
- **Sparsity of F.** Many real layout instances have sparse flow matrices (esc, ste
  families in QAPLIB). Sparsity makes exact methods reach much larger n.
- **Data source and format.** QAPLIB .dat file, a distance matrix from coordinates,
  or raw flow logs that still need aggregation? Confirm the objective convention:
  QAPLIB uses sum over ordered pairs, so symmetric instances count each pair twice.
- **Exactness requirement.** Does the user need a provably optimal layout (rare) or a
  high-quality solution with a reported gap to the best-known value (common)?
- **Solver availability.** Gurobi license present? Without it, the Kaufman-Broeckx
  model below runs on any LP/MIP solver, and the tabu search needs only numpy.
- **Time budget.** Robust tabu search delivers near-best-known QAPLIB results in
  seconds to minutes; exact runs at n = 25+ can take hours to days.
- **Quality reference.** Are best-known values available (QAPLIB .sln files) so gaps
  can be reported, or must you generate bounds yourself (Gilmore-Lawler, MIP dual bound)?
- **Repetition protocol.** How many seeds/replications are expected for the heuristic,
  and is statistical comparison against another method required?

## Problem Definition and Formulations

### Formal definition

Given n facilities and n locations, a flow matrix $F = (f_{ij}) \in \mathbb{R}_{\ge 0}^{n \times n}$
(material moved between facilities i and j per period) and a distance matrix
$D = (d_{k\ell}) \in \mathbb{R}_{\ge 0}^{n \times n}$ (cost per unit flow between locations
k and ℓ), find a permutation $\pi$ of $\{1,\dots,n\}$, where $\pi(i)$ is the location of
facility i, minimizing

$$
\min_{\pi \in S_n} \; \sum_{i=1}^{n} \sum_{j=1}^{n} f_{ij}\, d_{\pi(i)\pi(j)}
\;+\; \sum_{i=1}^{n} b_{i\pi(i)},
$$

with the optional linear placement cost $B = (b_{ik})$. This is the Koopmans & Beckmann
(1957) form, introduced for plant layout. The fully general Lawler (1963) QAP replaces
$f_{ij} d_{k\ell}$ with an arbitrary cost tensor $c_{ijk\ell}$; everything below extends
to it at higher constant cost. In binary variables $x_{ik} = 1$ iff facility i sits at
location k:

$$
\min \sum_{i,j,k,\ell} f_{ij} d_{k\ell}\, x_{ik} x_{j\ell}
\quad \text{s.t.} \quad
\sum_k x_{ik} = 1 \;\forall i, \qquad
\sum_i x_{ik} = 1 \;\forall k, \qquad
x_{ik} \in \{0,1\}.
$$

Equivalently, over permutation matrices X: $\min \operatorname{tr}(F X D^\top X^\top)$.
The QAP is NP-hard, and even finding an ε-approximate solution is NP-hard
(Sahni & Gonzalez, 1976). The TSP is the special case where F is the adjacency matrix
of a Hamiltonian cycle, which already signals how hard the general problem is.

### Linearizations

The product $x_{ik} x_{j\ell}$ must be removed to obtain a MILP. The classic options:

| Linearization | Extra variables | Extra constraints | LP-relaxation bound | Use when |
|---|---|---|---|---|
| Kaufman & Broeckx (1978) | n² continuous | n² | Very weak (often 0) | Memory is tight; any MIP solver; small n |
| Frieze & Yadegar (1983) | n⁴ continuous | O(n³) | Moderate, ≥ Gilmore-Lawler | n ≤ ~20 and a stronger bound is needed |
| Adams & Johnson (1994), level-1 RLT | n⁴ continuous | O(n⁴) | Strong; dominates the two above | Basis of serious exact codes; heavy memory |
| Native binary quadratic (Gurobi) | Solver-internal | Solver-internal | Depends on `PreQLinearize` | Fast to write; let presolve pick the reformulation |

The Kaufman-Broeckx model is the smallest known MILP for the QAP; its price is an LP
bound that is usually 0, so branch-and-bound progress comes almost entirely from
integer feasibility. The level-1 reformulation-linearization technique (RLT) bound of
Adams & Johnson is what strong exact codes compute, typically via the Hahn & Grant
(1998) dual-ascent procedure rather than a generic LP solver. See
**linearization-techniques** for the generic machinery behind these constructions.

### Why exact solving stalls around n = 30

- The symmetric group has n! permutations; at n = 30 that is ~2.7·10³². Branch-and-bound
  survives only with strong bounds, and QAP bounds are expensive: Gilmore-Lawler is
  cheap but loose, RLT-1 is strong but needs O(n⁴) memory, RLT-2/RLT-3 are stronger
  still but explode to O(n⁶)/O(n⁸) data.
- The landmark exact solve of nug30 (Anstreicher, Brixius, Goux & Linderoth, 2002)
  used a convex quadratic programming bound and a computational grid of roughly a
  thousand processors for about a week — on the order of several CPU-years for one
  instance of size 30.
- Several QAPLIB instances of size 30-40 (notably the tai-a family) still have no
  proven optimum; reported "best known" values come from heuristics.
- Structure changes the picture: sparse or highly symmetric instances (esc family)
  have been solved up to n = 128 because symmetry reduction collapses the search tree.

Practical consequence: treat n ≈ 30 as the ceiling for general-purpose exact solving,
use a MIP only when n is small or a provable gap is genuinely required, and otherwise
go directly to robust tabu search with best-known values or bounds for quality control.

### Method selection

| Situation | Recommended approach |
|---|---|
| n ≤ 12, optimality proof wanted | Any MILP below; solves in seconds |
| 12 < n ≤ 25, optimality proof wanted | Kaufman-Broeckx or native quadratic + time limit; expect hours at the top of the range |
| n > 25, proof wanted | Specialized RLT-based branch-and-bound codes; budget CPU-years; usually reconsider |
| Any n, good solution fast | Robust tabu search (Taillard, 1991) — the standard QAP heuristic |
| Heuristic stalls on hard instances | Memetic algorithm with tabu/local-search improvement (see **memetic-algorithms**) |
| Quick quality floor without solving | Gilmore-Lawler bound (code in Advanced Techniques) |

## Instances, QAPLIB, and Validation

QAPLIB (Burkard, Karisch & Rendl, 1997) is the canonical benchmark archive: ~130
instances, n from 12 to 256, with best-known solutions in companion .sln files.
Families differ sharply in character: nug/tho/kra are layout-like with grid distances,
tai-a are uniform random (hard for everything), tai-b are structured/clustered,
esc are sparse. Always state which family you tested, because heuristic rankings
change across families.

Generate controlled synthetic instances when you need size/structure sweeps. Two
standard generators — uniform (tai-a style) and grid layout (nugent style):

```python
import numpy as np


def _random_symmetric(rng: np.random.Generator, n: int, high: int) -> np.ndarray:
    """Symmetric nonnegative integer matrix with zero diagonal."""
    upper = np.triu(rng.integers(1, high + 1, size=(n, n)), k=1)
    return (upper + upper.T).astype(float)


def generate_uniform_qap(n: int, seed: int, high: int = 100) -> tuple[np.ndarray, np.ndarray]:
    """Taillard-style uniform random instance (hard, unstructured)."""
    rng = np.random.default_rng(seed)
    return _random_symmetric(rng, n, high), _random_symmetric(rng, n, high)


def generate_grid_qap(rows: int, cols: int, seed: int, density: float = 0.4,
                      high: int = 10) -> tuple[np.ndarray, np.ndarray]:
    """Facility-layout instance: Manhattan grid distances, sparse symmetric flows."""
    rng = np.random.default_rng(seed)
    n = rows * cols
    r, c = np.divmod(np.arange(n), cols)
    D = (np.abs(r[:, None] - r[None, :]) + np.abs(c[:, None] - c[None, :])).astype(float)
    keep = np.triu(rng.random((n, n)) < density, k=1)
    flows = np.triu(rng.integers(1, high + 1, size=(n, n)), k=1) * keep
    F = (flows + flows.T).astype(float)
    return F, D


F, D = generate_uniform_qap(8, seed=42)
print(F.shape, bool(np.allclose(F, F.T)), float(F.diagonal().sum()))
Fg, Dg = generate_grid_qap(3, 4, seed=42)
print(Dg.max())
# Expected: (8, 8) True 0.0   then 5.0 (max Manhattan distance on a 3x4 grid)
```

For instances with a planted optimum (useful for regression-testing heuristics), use
the Palubeckis (2000) generator idea: build D as a graph metric and F so that a chosen
permutation aligns large flows with small distances; cite the construction if you
report results on such instances, because they are known to be easier than tai-a.

QAPLIB files are whitespace-separated token streams — line breaks vary between
instances, so parse tokens, never lines:

```python
from pathlib import Path

import numpy as np


def read_qaplib(path: str | Path) -> tuple[np.ndarray, np.ndarray]:
    """Parse a QAPLIB .dat file: n, then two n-by-n matrices A and B.

    Objective convention: sum_ij A[i, j] * B[perm[i], perm[j]] over ordered pairs.
    """
    tokens = Path(path).read_text().split()
    n = int(tokens[0])
    values = np.array(tokens[1:1 + 2 * n * n], dtype=float)
    return values[: n * n].reshape(n, n), values[n * n:].reshape(n, n)


def read_qaplib_solution(path: str | Path) -> tuple[float, np.ndarray]:
    """Parse a QAPLIB .sln file: 'n value' then a 1-indexed permutation."""
    tokens = Path(path).read_text().split()
    n, value = int(tokens[0]), float(tokens[1])
    perm = np.array(tokens[2:2 + n], dtype=int) - 1
    return value, perm


import tempfile

content = "3\n\n0 2 0\n2 0 1\n0 1 0\n\n0 1 2\n1 0 1\n2 1 0\n"
with tempfile.NamedTemporaryFile("w", suffix=".dat", delete=False) as fh:
    fh.write(content)
A, B = read_qaplib(fh.name)
print(A[0, 1], B[2, 0])
# Expected: 2.0 2.0
```

Every result you report must pass an independent validator that shares no code with
the solver or the delta machinery. Plain Python loops are deliberate here — slow,
boring, and trustworthy:

```python
import numpy as np


def validate_qap_solution(F: np.ndarray, D: np.ndarray, perm: np.ndarray,
                          reported_obj: float | None = None,
                          tol: float = 1e-6) -> tuple[bool, float, list[str]]:
    """Independent feasibility and objective check for a QAP solution.

    Verifies that perm is a bijection and recomputes the objective from the
    definition. Returns (feasible_and_consistent, objective, issues).
    """
    issues: list[str] = []
    n = F.shape[0]
    p = np.asarray(perm)
    if F.shape != (n, n) or D.shape != (n, n):
        issues.append(f"F is {F.shape}, D is {D.shape}; both must be ({n}, {n})")
    if p.shape != (n,):
        issues.append(f"permutation has shape {p.shape}, expected ({n},)")
    elif not np.array_equal(np.sort(p), np.arange(n)):
        issues.append("perm is not a bijection onto {0, ..., n-1}")
    obj = 0.0
    if not issues:
        for i in range(n):
            for j in range(n):
                obj += float(F[i, j]) * float(D[p[i], p[j]])
        if reported_obj is not None and abs(obj - reported_obj) > tol:
            issues.append(f"recomputed objective {obj} != reported {reported_obj}")
    return (not issues), obj, issues


F3 = np.array([[0, 2, 0], [2, 0, 1], [0, 1, 0]], dtype=float)
D3 = np.array([[0, 1, 2], [1, 0, 1], [2, 1, 0]], dtype=float)
print(validate_qap_solution(F3, D3, np.array([0, 1, 2]), reported_obj=6.0))
# Expected: (True, 6.0, [])
```

## Exact MIP Models in Gurobi

### Kaufman-Broeckx linearization

For each (i, k) introduce a continuous variable $w_{ik}$ that captures the interaction
cost facility i incurs if placed at location k. With the upper bound
$a_{ik} = \sum_{j,\ell} f_{ij} d_{k\ell} = (\sum_j f_{ij})(\sum_\ell d_{k\ell})$,
the constraints

$$
w_{ik} \;\ge\; \sum_{j,\ell} f_{ij} d_{k\ell}\, x_{j\ell} \;-\; a_{ik}\,(1 - x_{ik}),
\qquad w_{ik} \ge 0,
$$

force $w_{ik}$ to equal the true cost whenever $x_{ik} = 1$ (this needs $F, D \ge 0$),
and minimizing $\sum_{i,k} w_{ik}$ recovers the QAP objective. Only n² extra variables
and n² extra constraints — but the LP relaxation can set all $x_{ik} = 1/n$ and all
$w_{ik} = 0$, so expect a root bound of 0 and slow gap closure.

```python
import gurobipy as gp
import numpy as np
from gurobipy import GRB


def add_assignment_constraints(model: gp.Model, x: gp.tupledict, n: int) -> None:
    """Each facility takes exactly one location and each location one facility."""
    model.addConstrs((gp.quicksum(x[i, k] for k in range(n)) == 1 for i in range(n)),
                     name="facility_assigned")
    model.addConstrs((gp.quicksum(x[i, k] for i in range(n)) == 1 for k in range(n)),
                     name="location_filled")


def add_kaufman_broeckx_constraints(model: gp.Model, x: gp.tupledict, w: gp.tupledict,
                                    F: np.ndarray, D: np.ndarray) -> None:
    """Link w[i, k] to the interaction cost of facility i at location k."""
    n = F.shape[0]
    a = F.sum(axis=1)[:, None] * D.sum(axis=1)[None, :]   # a[i, k] upper bound
    for i in range(n):
        for k in range(n):
            cost_ik = gp.quicksum(float(F[i, j] * D[k, l]) * x[j, l]
                                  for j in range(n) if F[i, j] != 0.0
                                  for l in range(n) if D[k, l] != 0.0)
            model.addConstr(w[i, k] >= cost_ik - float(a[i, k]) * (1 - x[i, k]),
                            name=f"kb[{i},{k}]")


def solve_qap_kaufman_broeckx(F: np.ndarray, D: np.ndarray,
                              time_limit: float = 60.0) -> tuple[np.ndarray, float, float]:
    """Solve the QAP via the Kaufman-Broeckx MILP; returns (perm, objective, gap)."""
    n = F.shape[0]
    model = gp.Model("qap_kb")
    model.Params.OutputFlag = 0
    model.Params.TimeLimit = time_limit
    x = model.addVars(n, n, vtype=GRB.BINARY, name="x")
    w = model.addVars(n, n, lb=0.0, name="w")
    add_assignment_constraints(model, x, n)
    add_kaufman_broeckx_constraints(model, x, w, F, D)
    model.setObjective(w.sum(), GRB.MINIMIZE)
    model.optimize()
    if model.Status not in (GRB.OPTIMAL, GRB.TIME_LIMIT) or model.SolCount == 0:
        raise RuntimeError(f"no incumbent; Gurobi status {model.Status}")
    perm = np.array([k for i in range(n) for k in range(n) if x[i, k].X > 0.5])
    return perm, model.ObjVal, model.MIPGap


F3 = np.array([[0, 2, 0], [2, 0, 1], [0, 1, 0]], dtype=float)
D3 = np.array([[0, 1, 2], [1, 0, 1], [2, 1, 0]], dtype=float)
perm, obj, gap = solve_qap_kaufman_broeckx(F3, D3)
print(perm, obj, gap)
# Expected: permutation [0 1 2] (or [2 1 0]), objective 6.0, gap 0.0
```

A linear placement term B is added by appending `gp.quicksum(float(B[i, k]) * x[i, k]
for i in range(n) for k in range(n))` to the objective; nothing else changes.

### Native binary quadratic model

Since the variables are binary, you can hand Gurobi the quadratic objective directly
and let presolve choose the linearization. `PreQLinearize = 1` requests an MILP
reformulation aimed at a strong LP relaxation (RLT-flavored); `2` aims for compactness.
This is the fastest model to write and a good default for n ≤ ~20.

```python
import gurobipy as gp
import numpy as np
from gurobipy import GRB


def add_assignment_constraints(model: gp.Model, x: gp.tupledict, n: int) -> None:
    """Each facility takes exactly one location and each location one facility."""
    model.addConstrs((gp.quicksum(x[i, k] for k in range(n)) == 1 for i in range(n)),
                     name="facility_assigned")
    model.addConstrs((gp.quicksum(x[i, k] for i in range(n)) == 1 for k in range(n)),
                     name="location_filled")


def solve_qap_quadratic(F: np.ndarray, D: np.ndarray,
                        time_limit: float = 60.0) -> tuple[np.ndarray, float, float]:
    """Solve the QAP as a binary quadratic program; Gurobi linearizes internally."""
    n = F.shape[0]
    model = gp.Model("qap_quadratic")
    model.Params.OutputFlag = 0
    model.Params.TimeLimit = time_limit
    model.Params.PreQLinearize = 1     # reformulate for a strong LP relaxation
    x = model.addVars(n, n, vtype=GRB.BINARY, name="x")
    add_assignment_constraints(model, x, n)
    objective = gp.QuadExpr()
    for i in range(n):
        for j in range(n):
            if F[i, j] == 0.0:
                continue
            for k in range(n):
                for l in range(n):
                    if D[k, l] != 0.0:
                        objective.add(x[i, k] * x[j, l], float(F[i, j] * D[k, l]))
    model.setObjective(objective, GRB.MINIMIZE)
    model.optimize()
    if model.Status not in (GRB.OPTIMAL, GRB.TIME_LIMIT) or model.SolCount == 0:
        raise RuntimeError(f"no incumbent; Gurobi status {model.Status}")
    perm = np.array([k for i in range(n) for k in range(n) if x[i, k].X > 0.5])
    return perm, model.ObjVal, model.MIPGap


F3 = np.array([[0, 2, 0], [2, 0, 1], [0, 1, 0]], dtype=float)
D3 = np.array([[0, 1, 2], [1, 0, 1], [2, 1, 0]], dtype=float)
perm, obj, gap = solve_qap_quadratic(F3, D3)
print(perm, obj, gap)
# Expected: permutation [0 1 2] (or [2 1 0]), objective 6.0, gap 0.0
```

Model-building itself is O(n⁴) Python-loop work here; at n = 25 that is ~390,000
quadratic terms, which takes a few seconds — acceptable because solve time dominates.
Always validate the returned permutation with `validate_qap_solution` before reporting:
the MIP objective and the validator must agree to numerical tolerance.

## Delta Evaluation and Robust Tabu Search

### Swap delta in O(n)

All competitive QAP heuristics search the 2-exchange (swap) neighborhood: exchange the
locations of facilities r and s. Recomputing the objective from scratch costs O(n²)
per move; the delta can be computed in O(n). For general F, D (asymmetric, nonzero
diagonals allowed), with p = π:

$$
\Delta(\pi, r, s) =
f_{rr}(d_{p_s p_s} - d_{p_r p_r}) + f_{rs}(d_{p_s p_r} - d_{p_r p_s})
+ f_{sr}(d_{p_r p_s} - d_{p_s p_r}) + f_{ss}(d_{p_r p_r} - d_{p_s p_s})
$$
$$
+ \sum_{k \ne r,s} \Big[ (f_{kr} - f_{ks})(d_{p_k p_s} - d_{p_k p_r})
+ (f_{rk} - f_{sk})(d_{p_s p_k} - d_{p_r p_k}) \Big].
$$

For symmetric F, D with zero diagonals this collapses to
$\Delta = 2 \sum_{k \ne r,s} (f_{kr} - f_{ks})(d_{p_k p_s} - d_{p_k p_r})$.
Taillard (1991) showed that after performing swap (r, s), the deltas of all pairs
(u, v) disjoint from {r, s} can be updated in O(1) each, so a full neighborhood
re-evaluation costs O(n²) per iteration instead of O(n³). Always test delta code
against a brute-force recomputation — sign and convention bugs here are the most
common QAP implementation error:

```python
import numpy as np


def qap_objective(F: np.ndarray, D: np.ndarray, perm: np.ndarray) -> float:
    """Compute sum_{i,j} F[i, j] * D[perm[i], perm[j]]."""
    return float(np.sum(F * D[np.ix_(perm, perm)]))


def swap_delta(F: np.ndarray, D: np.ndarray, perm: np.ndarray, r: int, s: int) -> float:
    """Exact objective change of swapping the locations of facilities r and s.

    General O(n) form: valid for asymmetric F, D and nonzero diagonals.
    """
    p = perm
    k = np.arange(len(p))
    mask = (k != r) & (k != s)
    pk, pr, ps = p[mask], p[r], p[s]
    delta = (F[r, r] * (D[ps, ps] - D[pr, pr]) + F[r, s] * (D[ps, pr] - D[pr, ps])
             + F[s, r] * (D[pr, ps] - D[ps, pr]) + F[s, s] * (D[pr, pr] - D[ps, ps]))
    delta += float(np.sum((F[mask, r] - F[mask, s]) * (D[pk, ps] - D[pk, pr])
                          + (F[r, mask] - F[s, mask]) * (D[ps, pk] - D[pr, pk])))
    return float(delta)


rng = np.random.default_rng(7)
n = 6
F = rng.integers(0, 10, (n, n)).astype(float)    # asymmetric, nonzero diagonal
D = rng.integers(0, 10, (n, n)).astype(float)
perm = rng.permutation(n)
q = perm.copy()
q[[1, 4]] = q[[4, 1]]
print(abs(qap_objective(F, D, q) - qap_objective(F, D, perm) - swap_delta(F, D, perm, 1, 4)))
# Expected: 0.0 (delta matches full recomputation exactly)
```

### Robust tabu search (the method of choice)

Robust tabu search (Ro-TS, Taillard 1991, "Robust taboo search for the quadratic
assignment problem") remains the reference heuristic: simple, nearly parameter-free,
and still within fractions of a percent of best-known values on most QAPLIB instances.
Its ingredients:

- **Move attribute tabu list.** After moving facility r away from location p(r),
  forbid re-assigning r to p(r) for `tenure` iterations. A swap is tabu only if *both*
  facilities would return to recently left locations.
- **Randomized tenure** drawn around n (here uniformly from [0.9n, 1.1n] per move) —
  the "robust" ingredient that prevents cycling without instance-specific tuning.
- **Aspiration**: a tabu move is accepted if it improves the best solution found.
- **Full-neighborhood best-move selection** over all n(n-1)/2 swaps, possible only
  because of the maintained delta matrix.

The implementation below keeps the delta matrix exact: the Taillard O(1) update for
pairs avoiding {r, s}, plus an exact O(n²) recomputation of the two touched rows.
See **tabu-search** for tenure theory, aspiration variants, and long-term memory.

```python
import numpy as np


def qap_objective(F: np.ndarray, D: np.ndarray, perm: np.ndarray) -> float:
    """Compute sum_{i,j} F[i, j] * D[perm[i], perm[j]]."""
    return float(np.sum(F * D[np.ix_(perm, perm)]))


def _all_swap_deltas(F: np.ndarray, D: np.ndarray, perm: np.ndarray) -> np.ndarray:
    """All n^2 swap deltas via one matmul (symmetric F, D, zero diagonals)."""
    Dp = D[np.ix_(perm, perm)]
    A = F.T @ Dp
    dg = np.diag(A)
    return 2.0 * (A + A.T - dg[:, None] - dg[None, :] + 2.0 * F * Dp)


def robust_tabu_search_qap(F: np.ndarray, D: np.ndarray, n_iterations: int = 20_000,
                           seed: int = 0) -> tuple[np.ndarray, float]:
    """Robust tabu search for the symmetric zero-diagonal QAP (Taillard, 1991).

    perm[i] is the location of facility i. Tenure is redrawn per move from
    [0.9n, 1.1n]; aspiration admits tabu moves that beat the incumbent.
    """
    rng = np.random.default_rng(seed)
    n = F.shape[0]
    perm = rng.permutation(n)
    obj = qap_objective(F, D, perm)
    best_perm, best_obj = perm.copy(), obj
    tabu_until = np.zeros((n, n), dtype=np.int64)   # (facility, location) -> iteration
    iu, ju = np.triu_indices(n, k=1)                # all candidate facility pairs
    delta = _all_swap_deltas(F, D, perm)

    for it in range(1, n_iterations + 1):
        cand = delta[iu, ju]
        tabu = (tabu_until[iu, perm[ju]] >= it) & (tabu_until[ju, perm[iu]] >= it)
        aspired = (obj + cand) < best_obj - 1e-9
        scores = np.where(~tabu | aspired, cand, np.inf)
        k = int(np.argmin(scores))
        if not np.isfinite(scores[k]):
            tabu_until[:] = 0                       # every move tabu: rare reset
            continue
        r, s = int(iu[k]), int(ju[k])
        move_delta = float(delta[r, s])             # read BEFORE updating delta

        lo, hi = int(0.9 * n), int(1.1 * n) + 1
        tabu_until[r, perm[r]] = it + int(rng.integers(lo, hi + 1))
        tabu_until[s, perm[s]] = it + int(rng.integers(lo, hi + 1))

        # Taillard O(1)-per-pair update for pairs avoiding {r, s}; pre-swap perm.
        a = F[r] - F[s]
        b = (D[perm[r]] - D[perm[s]])[perm]
        delta += 2.0 * (a[:, None] - a[None, :]) * (b[:, None] - b[None, :])

        obj += move_delta
        perm[[r, s]] = perm[[s, r]]
        if obj < best_obj - 1e-9:
            best_obj, best_perm = obj, perm.copy()

        # Exact O(n^2) recomputation of the rows/columns touching r and s.
        Dp = D[np.ix_(perm, perm)]
        FD = F * Dp
        diag_a = np.einsum("ku,ku->u", F, Dp)
        for t in (r, s):
            row = 2.0 * (F[t] @ Dp + Dp[t] @ F - F[t] @ Dp[t] - diag_a + 2.0 * FD[t])
            row[t] = 0.0
            delta[t, :] = row
            delta[:, t] = row
    return best_perm, best_obj


F3 = np.array([[0, 2, 0], [2, 0, 1], [0, 1, 0]], dtype=float)
D3 = np.array([[0, 1, 2], [1, 0, 1], [2, 1, 0]], dtype=float)
perm, obj = robust_tabu_search_qap(F3, D3, n_iterations=200, seed=1)
print(perm, obj)
# Expected: objective 6.0 with permutation [0 1 2] or [2 1 0]
```

Parameter guidance for Ro-TS:

| Parameter | Typical setting | Trade-off |
|---|---|---|
| Tabu tenure | Uniform in [0.9n, 1.1n], redrawn per move | Shorter risks cycling; much longer over-restricts and slows intensification |
| Iterations | 1,000·n for screening, up to 100,000·n for records | Linear time-quality trade; time-to-best usually flattens early |
| Aspiration | Accept tabu move iff it beats the incumbent | Disabling it requires shorter tenures to keep progress |
| Restarts | New random permutation if no improvement for ~5,000·n iterations | Cheap diversification; keep the global best across restarts |
| Replications | ≥ 10 seeds per instance | Needed for honest mean/best reporting |

Per-iteration cost is O(n²), matching Taillard's original. For asymmetric instances,
replace the closed-form delta matrix with a loop of the general `swap_delta` (O(n³)
initialization, then the same maintenance structure with the general update formulas
from Taillard's paper).

## Advanced Techniques

### Gilmore-Lawler lower bound

The classic cheap bound (Gilmore, 1962; Lawler, 1963). For each pair (i, k), compute
the minimum possible interaction cost of placing facility i at location k by the
rearrangement inequality — match the off-diagonal flow row of i (sorted ascending)
with the off-diagonal distance row of k (sorted descending) — then solve a linear
assignment problem over these costs. O(n³) total and a valid lower bound; loose for
large uniform instances (often 60-80% of the optimum) but free quality control when
no MIP dual bound is available.

```python
import numpy as np
from scipy.optimize import linear_sum_assignment


def gilmore_lawler_bound(F: np.ndarray, D: np.ndarray) -> float:
    """Gilmore-Lawler lower bound: minimal scalar products + linear assignment."""
    n = F.shape[0]
    L = np.empty((n, n))
    for i in range(n):
        f_row = np.sort(np.delete(F[i], i))                # ascending
        for k in range(n):
            d_row = np.sort(np.delete(D[k], k))[::-1]      # descending
            L[i, k] = F[i, i] * D[k, k] + float(f_row @ d_row)
    rows, cols = linear_sum_assignment(L)
    return float(L[rows, cols].sum())


F3 = np.array([[0, 2, 0], [2, 0, 1], [0, 1, 0]], dtype=float)
D3 = np.array([[0, 1, 2], [1, 0, 1], [2, 1, 0]], dtype=float)
print(gilmore_lawler_bound(F3, D3))
# Expected: 6.0 (equals the optimum on this tiny instance)
```

The inner linear assignment step is exactly the machinery covered in
**assignment-problems**; reuse a LAP solver rather than writing one.

### Stronger bounds: reductions and RLT

Subtracting row/column constants from F and D (reduction) and re-adding them through
the linear term tightens Gilmore-Lawler noticeably at no asymptotic cost. The next
tier is the level-1 RLT bound (Adams & Johnson, 1994), best computed by Hahn-Grant
dual ascent; it dominates Gilmore-Lawler and most eigenvalue bounds and is the
workhorse inside serious exact codes. Anstreicher & Brixius (2001) derived a convex
quadratic programming bound that balances strength and speed and powered the nug30
solve. Rule of thumb: report Gilmore-Lawler for free, quote RLT-based bounds from the
literature, and do not hand-roll RLT-2 unless you have tens of gigabytes of memory.

### Long-term memory and diversification in Ro-TS

Taillard's full Ro-TS adds a second aspiration: if a facility-location pair has not
been occupied for more than `u` iterations (u on the order of n² or larger), a move
establishing it is forced — a built-in diversification that visits neglected regions.
Frequency-based penalties (penalize moves proportionally to how often they were made)
achieve a similar effect. Add these only after confirming stagnation: on most QAPLIB
instances below n = 60, plain Ro-TS with restarts is already competitive.

### Memetic intensification for hard instances

On tai-a and large structured instances, the best-known results come from population
hybrids: a small population of permutations, distance-preserving or cycle-based
crossover, and Ro-TS or deep 2-exchange local search applied to every offspring
(Merz & Freisleben, 2000; Drezner, 2003). The QAP-specific design points: keep the
population tiny (10-40), enforce minimum pairwise permutation distance to avoid
duplicate basins, and budget ~90% of CPU time to the local search. See
**memetic-algorithms** for the framework; QAP is its canonical success story. A
simulated annealing baseline (Burkard & Rendl, 1984; Connolly, 1990) with the same
swap neighborhood and delta evaluation is worth running for comparison — see
**simulated-annealing** for cooling-schedule guidance.

### Exploiting instance structure

Sparse F: iterate only over nonzero flow pairs in delta formulas and model building —
esc-family instances become orders of magnitude cheaper. Symmetric D from a grid:
location symmetries (rotations/reflections) create equivalent optima; in exact runs,
break them by restricting the location of one high-flow facility to one orbit
representative per symmetry class. In heuristics, symmetry is harmless but inflates
apparent solution diversity — compare solutions up to symmetry when measuring
population diversity.

## Practical Challenges

**The MIP root bound is 0 and the gap never moves.** That is the Kaufman-Broeckx LP
relaxation behaving as designed, not a bug. Switch to the native quadratic model with
`PreQLinearize = 1`, or accept that the run is effectively enumerative and set a time
limit plus a heuristic incumbent as MIP start. For n > 25, stop expecting proofs.

**Delta evaluation disagrees with full recomputation.** Almost always one of: the
instance is asymmetric or has nonzero diagonals while the code assumes the symmetric
simplification; the update used the post-swap permutation where the pre-swap one is
required; or perm stores facility-of-location while the formulas assume
location-of-facility. Keep a brute-force `qap_objective` check in your test suite and
run it on random swaps after every change to delta code.

**Heuristic reports a value better than the QAPLIB best known.** You have a bug, not a
publication. The usual cause is evaluating with the inverse permutation (QAPLIB .sln
permutations apply as B[perm[i], perm[j]] with the A/B order from the .dat file) or
counting symmetric pairs once while the reference counts ordered pairs. Validate
against a published .sln value before trusting any new number.

**Tabu search cycles between a few solutions.** Tenure is too short or deterministic.
Use the randomized tenure in [0.9n, 1.1n]; if cycling persists on small instances,
widen to [0.5n, 1.5n] and add the long-term aspiration described above.

**Model construction exhausts memory.** Frieze-Yadegar or RLT-style models allocate
O(n⁴) variables: at n = 30 that is 810,000 variables before constraints. Use
Kaufman-Broeckx (n² extras) or the native quadratic model, and exploit flow sparsity
when building cost expressions.

**QAPLIB file parses into the wrong matrices.** The archive mixes line layouts; some
files put several rows on one line. Token-based parsing (as in `read_qaplib`) is
immune. Also confirm which matrix plays the flow role: the objective convention
A[i, j]·B[perm[i], perm[j]] is what matters, not the names.

**Runs are not reproducible.** Every stochastic component must take an explicit seed
(`np.random.default_rng(seed)`), and result rows must record instance, seed, iteration
budget, and wall time. Re-running a "best" result that cannot be regenerated wastes
days; treat the seed as part of the result.

**numpy tabu search is slow despite vectorization.** Profile first: the usual culprits
are building `D[np.ix_(perm, perm)]` more often than needed, Python-level loops over
all pairs, or float64 delta matrices that thrash cache at n > 200. The implementation
above does O(n²) work per iteration with a handful of vectorized operations; if that
is still too slow, port the inner loop to numba or C — the algorithm, not the
language, is already optimal.

## Tools & Libraries

| Library / resource | When to use | Note |
|---|---|---|
| gurobipy | Exact MILP/MIQP models, n ≤ ~25 | Native quadratic objective + `PreQLinearize`; needs a license |
| numpy | All heuristic code, delta evaluation | `np.random.default_rng(seed)`; matmul-based delta initialization |
| scipy.optimize | `linear_sum_assignment` inside Gilmore-Lawler and repair steps | Jonker-Volgenant LAP, fast to n in the thousands |
| QAPLIB archive | Benchmark instances and best-known values | ~130 instances with .sln files; cite Burkard, Karisch & Rendl (1997) |
| HiGHS / CBC via PuLP or python-mip | No Gurobi license | Run the Kaufman-Broeckx MILP; no native quadratic support, so linearize explicitly |
| OR-Tools CP-SAT | Curiosity / small n with side constraints | Element-based QAP models are weak; prefer MIP or heuristics |
| pandas | Experiment tables (one row per run: instance, seed, objective, time) | Only for results management, not for solving |

## Output Format

A complete QAP answer or deliverable contains:

1. **Instance summary.** n, family/source, symmetry, diagonal, flow sparsity,
   best-known value if available.
2. **Method statement.** Model or algorithm, exact parameter values, seeds, time
   limit, hardware note if times are compared.
3. **Solution report.** The permutation itself (0- or 1-indexed, stated), the
   objective recomputed by `validate_qap_solution` (never only the solver's number),
   and the gap to the best-known value or to the strongest available lower bound.
4. **For exact runs:** solver status, incumbent objective, best bound, MIP gap,
   node count, wall time.
5. **For heuristic runs:** per-seed table and aggregate (best/mean/std objective,
   mean time-to-best), iteration budget, restart count.

A minimal report template:

```text
Instance: tai30a (QAPLIB), n=30, symmetric, zero diagonal, dense flows
Method:   Robust tabu search, tenure ~ U[27, 33], 600,000 iterations,
          10 seeds (0..9), restart after 150,000 idle iterations
Best:     1,818,146   (validated independently; bijection check passed)
Best known: 1,818,146  -> gap 0.00%
Mean over seeds: 1,822,034 (std 2,410); mean time-to-best 14.2 s
Bound:    Gilmore-Lawler = 1,514,510 (16.7% below best known, for reference)
Artifacts: results/tai30a_rts.csv (one row per seed), perm in results/tai30a_best.txt
```

Report best AND mean over seeds — best-only reporting is the most common reviewer
complaint in heuristic QAP papers. If you compare two methods, use matched seeds and
a paired statistical test, and say which instances each method won.

## Questions to Ask

- How large is n, and is a provably optimal solution actually required?
- Are F and D symmetric with zero diagonals, or is the instance general (asymmetric
  flows, self-loops, linear placement costs)?
- Where does the data come from — QAPLIB file, coordinates to be converted to
  distances, or raw flow records that need aggregation?
- Is there a Gurobi license, or must everything run on open-source solvers and numpy?
- What is the time budget per instance, and how many instances/seeds are in scope?
- Are best-known values available for gap reporting, or should bounds be computed?
- Are there side constraints (forbidden locations, fixed assignments, zoning) that
  break the pure permutation structure?
- Will results be compared against another method, and if so under what protocol
  (same time limit, same seeds, statistical test)?

## Related Skills

- **assignment-problems** — when the interaction term vanishes and the problem is a
  linear assignment, and for the LAP solvers used inside Gilmore-Lawler bounds.
- **tabu-search** — when tuning tenure, aspiration, candidate lists, or long-term
  memory beyond the compact robust tabu search given here.
- **memetic-algorithms** — when robust tabu search stalls on hard instances and a
  population hybrid with strong local search is the next step.
- **linearization-techniques** — when choosing among Kaufman-Broeckx, Frieze-Yadegar,
  and RLT reformulations or tightening the big-M style bounds inside them.
- **simulated-annealing** — when a simple single-solution baseline with the same swap
  neighborhood is wanted for comparison or as a starting point.
