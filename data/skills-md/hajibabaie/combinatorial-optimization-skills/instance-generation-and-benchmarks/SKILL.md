---
name: instance-generation-and-benchmarks
description: When the user wants to assemble instances for optimization experiments by parsing standard benchmarks (TSPLIB, CVRPLIB/Solomon, OR-Library, MIPLIB, QAPLIB, Taillard), writing seeded generators with controlled hardness, reporting instance features, or building train/test splits for tuning. Also use when the user mentions "benchmark instances," "TSPLIB," "Solomon instances," "OR-Library," "instance generator," "test instances," or when a study needs a defensible test bed. For statistical comparison, see algorithm-benchmarking-statistics; for feasibility checking, see solution-validation-testing.
---

# Instance Generation and Benchmarks

You are an expert in computational experimentation for combinatorial optimization. This skill covers obtaining, parsing, generating, and organizing problem instances: the standard benchmark libraries (TSPLIB, CVRPLIB/Solomon, OR-Library, MIPLIB, QAPLIB, Taillard), seeded synthetic generators with controlled hardness, instance feature reporting, and train/test instance splits for parameter tuning. Use the pattern catalog below to build instance pipelines whose experiments are reproducible byte-for-byte and whose conclusions survive review.

## Initial Assessment

Establish the following before writing any parser or generator:

- **Problem class and existing libraries.** Identify whether a curated benchmark set already exists for the problem (TSP → TSPLIB; CVRP/VRPTW → CVRPLIB, Solomon, Gehring-Homberger, Uchoa X instances; QAP → QAPLIB; flow shop / job shop → Taillard; general MIP → MIPLIB 2017; set covering, scheduling, knapsack and ~40 other classes → OR-Library). Never invent instances when comparison to published results is the goal.
- **Purpose of each instance group.** Separate three roles: development instances (tiny, known optima, used for debugging), tuning instances (train set for parameter search), and evaluation instances (test set, touched only for final runs). Conflating these roles invalidates the comparison.
- **Comparability requirement.** Ask whether results must be directly comparable to published numbers. If yes, the exact rounding and distance conventions of the library are mandatory, not optional details.
- **Distance/rounding conventions.** Confirm them before parsing: TSPLIB `EUC_2D` rounds to nearest integer; `CEIL_2D` rounds up; `ATT` is pseudo-Euclidean; Solomon distances are real-valued and best-known solutions assume double precision.
- **Sizes and counts.** Establish target instance sizes, how many instances per size/class, and how many seeds per instance the time budget allows. Coordinate with the comparison protocol (see algorithm-benchmarking-statistics) so the instance count supports the planned statistical tests.
- **Hardness target.** Decide whether instances should be representative of an application, deliberately hard (phase-transition region, correlated coefficients), or scaled families for empirical complexity estimation. These call for different generator designs.
- **Feasibility guarantees.** Determine whether the generator must guarantee feasible instances (e.g., total demand within fleet capacity, at least one feasible schedule) or whether infeasibility is itself a study subject.
- **Reproducibility contract.** Fix the seeding scheme (one named seed per instance), record the generator version with each instance, and decide the on-disk format (raw library format vs cached `.npz`).
- **Licensing and redistribution.** Check whether the benchmark files may be redistributed with your code. If not, plan a download script with checksums instead of committing data.
- **Best-known values.** Locate the authoritative source for optima/best-known solutions (TSPLIB optima list, SINTEF pages for VRPTW, QAPLIB pages, MIPLIB status tags) and record source and access date.

## Benchmark Landscape and Instance Design

### The standard libraries

| Library | Problems | Format style | Reference |
|---|---|---|---|
| TSPLIB | TSP, ATSP, HCP, CVRP | keyword header + data sections | Reinelt (1991), "TSPLIB — A traveling salesman problem library" |
| Solomon / Gehring-Homberger | VRPTW (100 / up to 1000 customers) | fixed-layout text, R/C/RC classes | Solomon (1987); Gehring & Homberger (1999) |
| CVRPLIB (incl. X instances) | CVRP | TSPLIB-like `.vrp` | Uchoa et al. (2017), "New benchmark instances for the CVRP" |
| OR-Library | ~40 classes: SCP, GAP, MKP, scheduling, location | per-family ad hoc text | Beasley (1990), "OR-Library: distributing test problems by electronic mail" |
| MIPLIB 2017 | general MIP | MPS files + curated benchmark subset, easy/hard/open tags | Gleixner et al. (2021) |
| QAPLIB | QAP | n + two n×n matrices | Burkard, Karisch & Rendl (1997) |
| Taillard sets | flow shop, job shop, open shop, QAP | header + matrices, several instances per file | Taillard (1993), "Benchmarks for basic scheduling problems" |
| DIMACS challenge sets | clique, coloring, TSP | `.col` edge lists, challenge-specific | Johnson & Trick (1996); Johnson & McGeoch (2002) for TSP |

### Instances as draws from a distribution

Treat a synthetic generator as a map $G(\phi, s) \mapsto I$ from a parameter vector $\phi$ (size, tightness, correlation, structure) and a seed $s$ to an instance $I$. Fixing $\phi$ and varying $s$ defines an instance family — a distribution you can sample train and test sets from. Parameter tuning then has a well-defined generalization statement:

$$
\theta^{*} = \arg\min_{\theta \in \Theta} \; \frac{1}{|\mathcal{I}_{\mathrm{train}}|} \sum_{I \in \mathcal{I}_{\mathrm{train}}} m(A_{\theta}, I),
\qquad
\text{report} \quad \frac{1}{|\mathcal{I}_{\mathrm{test}}|} \sum_{I \in \mathcal{I}_{\mathrm{test}}} m(A_{\theta^{*}}, I),
$$

where $m(A_\theta, I)$ is the performance measure (gap, objective, time-to-target) of algorithm $A$ with parameters $\theta$ on instance $I$. Reporting tuning-set performance as the result is the instance-level analogue of testing on training data.

### Hardness control knobs

Empirical hardness is algorithm-relative, but a few knobs move it predictably:

| Knob | Mechanism | Example |
|---|---|---|
| Size $n$ | search-space growth | sweep $n$ geometrically (50, 100, 200, 400) for scaling studies |
| Constraint tightness | feasible region shrinks, bounds weaken | knapsack capacity ratio $c / \sum w_j$; vehicle count vs total demand |
| Coefficient correlation | LP bound and greedy ranking degrade | strongly correlated knapsack profits $p_j = w_j + \delta$ (Pisinger 2005) |
| Phase-transition parameter | solvable/unsolvable boundary concentrates hard instances | 3-coloring of $G(n,p)$ near average degree ≈ 4.7 (Cheeseman, Kanefsky & Taylor 1991) |
| Spatial structure | neighborhood and pruning behavior change | clustered vs uniform TSP/VRP customer locations |
| Symmetry | duplicated subtrees in branch-and-bound | identical machines, interchangeable bins |

### Decision guidance

- **Use standard benchmarks** when the contribution is a method and readers must compare against literature numbers. Use the complete standard set or a pre-registered, rule-based subset — never a hand-picked one.
- **Use synthetic generators** when studying how performance responds to structure (tightness, correlation, clustering), when the application's instances differ systematically from public benchmarks, or when you need unlimited train/test instances for tuning.
- **Use both** in most papers: benchmarks for comparability, synthetic families for controlled-factor analysis.
- **Cache parsed instances** (e.g., `.npz` of the distance matrix) but keep the raw library file as the source of truth and re-derivable.

## Pattern Catalog: Parsing Standard Benchmark Formats

### Pattern 1 — TSPLIB parser with exact rounding conventions

TSPLIB optima are defined with respect to specific integer distance functions. A parser that returns float distances, or rounds with `floor` instead of nearest-integer, produces tour lengths that disagree with every published optimum.

```python
from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class TSPInstance:
    """Symmetric TSP instance with a precomputed integer distance matrix."""

    name: str
    n: int
    dist: np.ndarray            # shape (n, n), dtype int64
    coords: np.ndarray | None   # shape (n, 2), or None for EXPLICIT instances


def _euc_2d(coords: np.ndarray) -> np.ndarray:
    """TSPLIB EUC_2D: Euclidean distance rounded to the nearest integer."""
    diff = coords[:, None, :] - coords[None, :, :]
    return np.rint(np.sqrt((diff * diff).sum(axis=2))).astype(np.int64)


def _ceil_2d(coords: np.ndarray) -> np.ndarray:
    """TSPLIB CEIL_2D: Euclidean distance rounded up."""
    diff = coords[:, None, :] - coords[None, :, :]
    return np.ceil(np.sqrt((diff * diff).sum(axis=2))).astype(np.int64)


def _att(coords: np.ndarray) -> np.ndarray:
    """TSPLIB ATT pseudo-Euclidean distance (att48, att532)."""
    diff = coords[:, None, :] - coords[None, :, :]
    r = np.sqrt((diff * diff).sum(axis=2) / 10.0)
    t = np.rint(r)
    return np.where(t < r, t + 1, t).astype(np.int64)


def _explicit(values: list[int], n: int, fmt: str) -> np.ndarray:
    """Rebuild a full matrix from an EXPLICIT EDGE_WEIGHT_SECTION."""
    d = np.zeros((n, n), dtype=np.int64)
    it = iter(values)
    if fmt == "FULL_MATRIX":
        for i in range(n):
            for j in range(n):
                d[i, j] = next(it)
    elif fmt == "UPPER_ROW":
        for i in range(n):
            for j in range(i + 1, n):
                d[i, j] = d[j, i] = next(it)
    elif fmt == "LOWER_DIAG_ROW":
        for i in range(n):
            for j in range(i + 1):
                d[i, j] = d[j, i] = next(it)
    else:
        raise ValueError(f"unsupported EDGE_WEIGHT_FORMAT {fmt}")
    return d


def parse_tsplib(text: str) -> TSPInstance:
    """Parse a TSPLIB .tsp file given as a string."""
    header: dict[str, str] = {}
    coords_rows: list[tuple[float, float]] = []
    weight_values: list[int] = []
    section = ""
    for raw in text.splitlines():
        ln = raw.strip()
        if not ln:
            continue
        upper = ln.upper()
        if ":" in ln and section == "":
            key, _, val = ln.partition(":")
            header[key.strip().upper()] = val.strip()
        elif upper.startswith("NODE_COORD_SECTION"):
            section = "coords"
        elif upper.startswith("EDGE_WEIGHT_SECTION"):
            section = "weights"
        elif upper.startswith(("DISPLAY_DATA_SECTION", "EOF")):
            section = "done"
        elif section == "coords":
            parts = ln.split()
            coords_rows.append((float(parts[1]), float(parts[2])))
        elif section == "weights":
            weight_values.extend(int(float(tok)) for tok in ln.split())
    n = int(header["DIMENSION"])
    ewt = header.get("EDGE_WEIGHT_TYPE", "EXPLICIT").upper()
    if ewt == "EXPLICIT":
        fmt = header.get("EDGE_WEIGHT_FORMAT", "FULL_MATRIX").upper()
        dist, coords = _explicit(weight_values, n, fmt), None
    else:
        coords = np.array(coords_rows, dtype=float)
        dist = {"EUC_2D": _euc_2d, "CEIL_2D": _ceil_2d, "ATT": _att}[ewt](coords)
    return TSPInstance(header.get("NAME", "unnamed"), n, dist, coords)


_TINY = """NAME : tiny4
TYPE : TSP
DIMENSION : 4
EDGE_WEIGHT_TYPE : EUC_2D
NODE_COORD_SECTION
1 0 0
2 3 4
3 6 0
4 3 -4
EOF
"""
inst = parse_tsplib(_TINY)
print(inst.name, inst.n, inst.dist[0, 1], inst.dist[0, 2])
# Expected: tiny4 4 5 6  (EUC_2D distances 5.0 and 6.0 round to integers 5 and 6)
```

**Pitfall:** The rounding convention is the single most common source of "my optimum does not match TSPLIB." `eil51` has optimum 426 only under nearest-integer `EUC_2D`; with float distances the optimal tour length is different and even the optimal tour can change. Validate every new parser by recomputing one published optimal tour value before running any experiment. Also note `GEO` (geographic) instances such as `gr96` need a separate latitude/longitude formula — raise on unsupported types rather than guessing.

### Pattern 2 — Solomon / Gehring-Homberger VRPTW parser

Solomon's 56 instances (R1/R2/C1/C2/RC1/RC2 classes) and the Gehring-Homberger extensions share one fixed text layout. Parse defensively by token patterns, not by line numbers, so both families pass through the same function.

```python
from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class VRPTWInstance:
    """Solomon-format VRPTW instance. Node 0 is the depot."""

    name: str
    n_vehicles: int
    capacity: int
    coords: np.ndarray    # (n+1, 2)
    demand: np.ndarray    # (n+1,)
    ready: np.ndarray     # (n+1,)
    due: np.ndarray       # (n+1,)
    service: np.ndarray   # (n+1,)
    dist: np.ndarray      # (n+1, n+1), float Euclidean


def parse_solomon(text: str) -> VRPTWInstance:
    """Parse a Solomon / Gehring-Homberger VRPTW file given as a string."""
    lines = [ln for ln in text.splitlines() if ln.strip()]
    name = lines[0].strip()
    rows: list[list[float]] = []
    n_vehicles = capacity = -1
    expect_vehicle = False
    for ln in lines[1:]:
        toks = ln.split()
        head = toks[0].upper()
        if head in {"VEHICLE", "CUSTOMER", "CUST"}:
            continue
        if head == "NUMBER":
            expect_vehicle = True
            continue
        if expect_vehicle:
            n_vehicles, capacity = int(toks[0]), int(toks[1])
            expect_vehicle = False
            continue
        if len(toks) == 7:
            rows.append([float(t) for t in toks])
    data = np.array(rows)
    data = data[np.argsort(data[:, 0])]      # depot (id 0) first
    coords = data[:, 1:3]
    diff = coords[:, None, :] - coords[None, :, :]
    dist = np.sqrt((diff * diff).sum(axis=2))
    return VRPTWInstance(
        name=name,
        n_vehicles=n_vehicles,
        capacity=capacity,
        coords=coords,
        demand=data[:, 3].astype(np.int64),
        ready=data[:, 4].astype(np.int64),
        due=data[:, 5].astype(np.int64),
        service=data[:, 6].astype(np.int64),
        dist=dist,
    )


_TINY = """TINY1

VEHICLE
NUMBER     CAPACITY
   2         50

CUSTOMER
CUST NO.  XCOORD.  YCOORD.  DEMAND  READY TIME  DUE DATE  SERVICE TIME
    0       0        0        0        0          100        0
    1       3        4       10        0           80       10
    2       6        0       20       10           90       10
"""
v = parse_solomon(_TINY)
print(v.name, v.n_vehicles, v.capacity, round(float(v.dist[0, 1]), 1))
# Expected: TINY1 2 50 5.0
```

**Pitfall:** Distance precision is a silent convention split. Solomon's original work and many 1990s papers truncated travel times to one decimal; the best-known solutions curated by SINTEF use full double precision. The same routes can differ in cost and even in time-window feasibility between the two conventions. State the convention in your experiment metadata, and never mix best-known values from one convention with your costs from the other.

### Pattern 3 — Token-stream parsers for QAPLIB and Taillard files

Matrix-based formats (QAPLIB `.dat`, Taillard scheduling files) wrap rows at arbitrary widths and mix in human-readable header lines. Parsing by lines is fragile; extracting the full integer token stream and consuming it positionally is robust to any wrapping.

```python
import re
from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class QAPInstance:
    """QAP instance: minimize sum_ij flow[i,j] * distance[pi(i), pi(j)]."""

    n: int
    flow: np.ndarray
    distance: np.ndarray


def parse_qaplib(text: str) -> QAPInstance:
    """Parse a QAPLIB .dat file: n, then two n-by-n integer matrices."""
    tokens = [int(t) for t in re.findall(r"-?\d+", text)]
    n = tokens[0]
    need = 1 + 2 * n * n
    if len(tokens) < need:
        raise ValueError(f"expected {need} integers, found {len(tokens)}")
    a = np.array(tokens[1 : 1 + n * n], dtype=np.int64).reshape(n, n)
    b = np.array(tokens[1 + n * n : need], dtype=np.int64).reshape(n, n)
    return QAPInstance(n=n, flow=a, distance=b)


@dataclass(frozen=True)
class FlowShopInstance:
    """Permutation flow-shop instance in Taillard's format."""

    n_jobs: int
    n_machines: int
    proc: np.ndarray     # (n_machines, n_jobs) processing times
    upper_bound: int
    lower_bound: int


def parse_taillard_flowshop(text: str) -> list[FlowShopInstance]:
    """Parse a Taillard flow-shop file; each file holds several instances."""
    tokens = [int(t) for t in re.findall(r"-?\d+", text)]
    pos = 0
    out: list[FlowShopInstance] = []
    while pos < len(tokens):
        n_jobs, n_mach, _seed, ub, lb = tokens[pos : pos + 5]
        pos += 5
        body = tokens[pos : pos + n_jobs * n_mach]
        pos += n_jobs * n_mach
        proc = np.array(body, dtype=np.int64).reshape(n_mach, n_jobs)
        out.append(FlowShopInstance(n_jobs, n_mach, proc, ub, lb))
    return out


qap = parse_qaplib("2\n0 1\n1 0\n0 3\n3 0\n")
print(qap.n, qap.flow.tolist(), qap.distance.tolist())
# Expected: 2 [[0, 1], [1, 0]] [[0, 3], [3, 0]]

shops = parse_taillard_flowshop("2 3 1234 99 90\n5 7\n4 6\n3 2\n")
print(len(shops), shops[0].proc.shape, shops[0].proc[0].tolist())
# Expected: 1 (3, 2) [5, 7]
```

**Pitfall:** QAPLIB defines the objective with matrix A as flows and B as distances, but several contributed families follow the opposite convention. For symmetric instances the objective value is unaffected; for asymmetric ones (e.g., `bur` family) it is not. The only safe check: recompute the published best-known value from the published permutation before trusting the parser. The same applies to Taillard files — confirm the matrix is machine-major (rows = machines), and remember each file contains ten instances, not one.

### Pattern 4 — OR-Library parsers with a recomputation checksum

OR-Library (Beasley 1990) hosts dozens of problem classes, each with its own ad hoc text format. The set covering format below is typical: a header, a cost vector, then per-row cover lists with 1-based column indices.

```python
import re

import numpy as np


def parse_orlib_scp(text: str) -> tuple[np.ndarray, list[np.ndarray]]:
    """Parse an OR-Library set covering file (scp4x, scp5x, scpnr families).

    Returns (cost vector of length n_cols, list of n_rows arrays holding the
    0-based column indices that cover each row).
    """
    tokens = [int(t) for t in re.findall(r"-?\d+", text)]
    pos = 0
    m, n = tokens[pos], tokens[pos + 1]
    pos += 2
    cost = np.array(tokens[pos : pos + n], dtype=np.int64)
    pos += n
    rows: list[np.ndarray] = []
    for _ in range(m):
        k = tokens[pos]
        pos += 1
        cols = np.array(tokens[pos : pos + k], dtype=np.int64) - 1  # 1-based file
        pos += k
        rows.append(cols)
    return cost, rows


def scp_objective(cost: np.ndarray, rows: list[np.ndarray], chosen: set[int]) -> int:
    """Recompute a cover's cost; raise if any row is uncovered (checksum use)."""
    for i, cols in enumerate(rows):
        if not chosen.intersection(cols.tolist()):
            raise ValueError(f"row {i} uncovered")
    return int(cost[sorted(chosen)].sum())


cost, rows = parse_orlib_scp("3 4\n2 3 4 5\n2 1 2\n2 2 3\n1 4\n")
print(cost.tolist(), [r.tolist() for r in rows])
print(scp_objective(cost, rows, {1, 3}))
# Expected: [2, 3, 4, 5] [[0, 1], [1, 2], [3]] then 8 (columns 1 and 3 cover all rows)
```

**Pitfall:** OR-Library formats are family-specific even when they look similar. The `scp*` files list, for each row, the columns covering it; the `rail*` crew-scheduling files are column-major (for each column: cost, row count, row list). Reusing one parser across families misreads data without any error. Defend with a checksum: take one published solution for the family, recompute its objective through your parsed data, and assert equality in a unit test (see solution-validation-testing).

## Pattern Catalog: Synthetic Generators with Controlled Hardness

### Pattern 5 — Euclidean TSP generator: uniform and clustered

Uniform random points are the default but are statistically special: the optimal tour length concentrates around $k\sqrt{nA}$ (Beardwood, Halton & Hammersley 1959), and most heuristics behave very uniformly on them. The DIMACS TSP Challenge therefore pairs uniform instances (`portgen`) with clustered ones (`portcgen`), which stress different heuristic behavior.

```python
import numpy as np


def generate_tsp(
    n: int,
    seed: int,
    kind: str = "uniform",
    n_clusters: int = 8,
    cluster_std: float = 25.0,
    box: float = 1000.0,
) -> np.ndarray:
    """Generate TSP coordinates, 'uniform' in a box or 'clustered' around centers."""
    rng = np.random.default_rng(seed)
    if kind == "uniform":
        return rng.uniform(0.0, box, size=(n, 2))
    if kind == "clustered":
        centers = rng.uniform(0.0, box, size=(n_clusters, 2))
        labels = rng.integers(0, n_clusters, size=n)
        pts = centers[labels] + rng.normal(0.0, cluster_std, size=(n, 2))
        return np.clip(pts, 0.0, box)
    raise ValueError(f"unknown kind {kind!r}")


def nint_distance_matrix(coords: np.ndarray) -> np.ndarray:
    """TSPLIB-convention rounded Euclidean distance matrix."""
    diff = coords[:, None, :] - coords[None, :, :]
    return np.rint(np.sqrt((diff * diff).sum(axis=2))).astype(np.int64)


coords = generate_tsp(50, seed=42, kind="clustered")
d = nint_distance_matrix(coords)
print(coords.shape, d.shape, int(d[0, 0]), bool((d == d.T).all()))
# Expected: (50, 2) (50, 50) 0 True — and seed 42 reproduces this instance exactly
```

**Pitfall:** A generator that draws from `np.random` module-level state instead of an explicit `np.random.default_rng(seed)` is not reproducible once any other code touches the global stream. One seed per instance, stored in the instance name (`clu_n50_s42`), is the contract that lets a reviewer regenerate your entire test bed from the paper. Also resist `cluster_std` so small that clusters collapse to points — rounded distances of 0 between distinct cities break many tour data structures.

### Pattern 6 — Knapsack generator with Pisinger correlation classes

Knapsack hardness is driven almost entirely by the profit-weight correlation structure and the capacity, not by size. Pisinger (2005), "Where are the hard knapsack problems?", showed that uncorrelated instances are easy at any size solvers reach, while strongly correlated ones stall branch-and-bound because the LP bound stays weak.

```python
import numpy as np


def generate_knapsack(
    n: int,
    seed: int,
    kind: str = "uncorrelated",
    r: int = 1000,
    h: int = 50,
    h_max: int = 100,
) -> tuple[np.ndarray, np.ndarray, int]:
    """Generate a 0-1 knapsack instance (profits, weights, capacity).

    Correlation classes follow Pisinger (2005): uncorrelated, weakly,
    strongly, inverse_strongly, subset_sum. The capacity series rule
    c = h / (h_max + 1) * sum(w) spans loose to tight capacities as h grows.
    """
    rng = np.random.default_rng(seed)
    w = rng.integers(1, r + 1, size=n)
    if kind == "uncorrelated":
        p = rng.integers(1, r + 1, size=n)
    elif kind == "weakly":
        lo = np.maximum(w - r // 10, 1)
        p = rng.integers(lo, w + r // 10 + 1)
    elif kind == "strongly":
        p = w + r // 10
    elif kind == "inverse_strongly":
        p = rng.integers(1, r + 1, size=n)
        w = p + r // 10
    elif kind == "subset_sum":
        p = w.copy()
    else:
        raise ValueError(f"unknown kind {kind!r}")
    c = int(h * int(w.sum()) / (h_max + 1))
    return p.astype(np.int64), w.astype(np.int64), max(c, int(w.max()))


p, w, c = generate_knapsack(8, seed=1, kind="strongly")
print(len(p), bool((p == w + 100).all()), bool(c <= int(w.sum())))
# Expected: 8 True True — profits sit exactly 100 above weights; capacity ~ half of total weight
```

**Pitfall:** Generating one instance with a single random capacity tells you nothing about hardness; a slightly different capacity can flip the same profit/weight vectors from trivial to very hard. For hardness studies, sweep the full capacity series $h = 1, \dots, h_{\max}$ over the same weights, as Pisinger's test sets do. And keep the coefficient range $r$ fixed when scaling $n$, otherwise you confound size with coefficient magnitude (which changes DP pseudo-polynomial cost).

### Pattern 7 — Graph generators at the phase transition

For graph problems (coloring, clique, covering), random instances are easy almost everywhere except near a phase transition in a control parameter. Cheeseman, Kanefsky & Taylor (1991), "Where the really hard problems are", located the hard 3-coloring instances of $G(n,p)$ near average degree ≈ 4.7. Geometric graphs add the spatial structure typical of frequency-assignment and sensor applications.

```python
import numpy as np


def gnp_graph(n: int, p: float, seed: int) -> np.ndarray:
    """Erdos-Renyi G(n, p) as a symmetric boolean adjacency matrix."""
    rng = np.random.default_rng(seed)
    upper = np.triu(rng.random((n, n)) < p, k=1)
    return upper | upper.T


def gnp_at_average_degree(n: int, avg_degree: float, seed: int) -> np.ndarray:
    """G(n, p) with p chosen to hit a target average degree (hardness knob)."""
    p = min(avg_degree / (n - 1), 1.0)
    return gnp_graph(n, p, seed)


def geometric_graph(n: int, radius: float, seed: int) -> tuple[np.ndarray, np.ndarray]:
    """Random geometric graph on the unit square: connect points within radius."""
    rng = np.random.default_rng(seed)
    pts = rng.random((n, 2))
    diff = pts[:, None, :] - pts[None, :, :]
    d2 = (diff * diff).sum(axis=2)
    adj = (d2 <= radius * radius) & ~np.eye(n, dtype=bool)
    return adj, pts


adj = gnp_at_average_degree(60, avg_degree=4.7, seed=7)
print(adj.shape, bool((adj == adj.T).all()), int(adj.sum()) // 2)
# Expected: (60, 60) True and roughly 140 edges (n * avg_degree / 2); exact count varies with seed
```

**Pitfall:** Sampling the control parameter uniformly (e.g., $p \sim U(0,1)$) produces a test bed that is almost entirely easy instances, which then "proves" any algorithm fast. If the claim is about hard instances, sample densely around the transition and verify hardness empirically (median solve time of a reference solver). Conversely, if the claim is about application performance, $G(n,p)$ is a poor proxy for real graphs — geometric or scale-free generators usually match application structure better.

## Pattern Catalog: Instance Features and Experiment Splits

### Pattern 8 — Instance feature extraction into a tidy table

Reporting instance features (size, dispersion, clustering, tightness) lets readers judge what your instance set actually covers and is the raw material for instance space analysis. Keep features cheap to compute and store one row per instance.

```python
import numpy as np
import pandas as pd


def tsp_features(coords: np.ndarray) -> dict[str, float]:
    """Cheap TSP instance features for reporting and instance-space analysis."""
    n = len(coords)
    diff = coords[:, None, :] - coords[None, :, :]
    d = np.sqrt((diff * diff).sum(axis=2))
    off = d[~np.eye(n, dtype=bool)]
    nn = np.where(np.eye(n, dtype=bool), np.inf, d).min(axis=1)
    area = float(np.ptp(coords[:, 0]) * np.ptp(coords[:, 1]))
    return {
        "n": float(n),
        "dist_mean": float(off.mean()),
        "dist_cv": float(off.std() / off.mean()),   # bimodal under clustering -> high
        "nn_mean": float(nn.mean()),
        "nn_cv": float(nn.std() / nn.mean()),       # spread of local point density
        "density": float(n / area) if area > 0 else float("inf"),
    }


rng = np.random.default_rng(3)
uniform_pts = rng.uniform(0.0, 1000.0, size=(40, 2))
centers = rng.uniform(0.0, 1000.0, size=(4, 2))
clustered_pts = centers[rng.integers(0, 4, size=40)] + rng.normal(0.0, 15.0, size=(40, 2))
features = pd.DataFrame(
    [
        {"instance": "uniform40", **tsp_features(uniform_pts)},
        {"instance": "clustered40", **tsp_features(clustered_pts)},
    ]
).set_index("instance")
print(features[["n", "dist_cv", "nn_mean"]].round(2))
# Expected: two rows; clustered40 shows a clearly higher dist_cv (bimodal distances)
# and a clearly lower nn_mean (dense clusters) than uniform40
```

**Pitfall:** Features computed from the full $n \times n$ distance matrix cost $O(n^2)$ memory; for $n > 20{,}000$ switch to k-d tree nearest-neighbor queries and sampled pairwise distances. More importantly, do not let feature choice silently define "representative": a feature table shows what your set covers, but only a comparison against application instances (when they exist) shows whether the coverage is the relevant one.

### Pattern 9 — Family-stratified train/test split with a persisted manifest

Parameters tuned on the same instances used for the final comparison overstate performance — the instance-level form of overfitting. Split once, stratified by family so both sides cover all structures, write the manifest to disk, and have every script read the manifest instead of re-splitting.

```python
import json
from pathlib import Path

import numpy as np


def split_instances(
    names: list[str],
    families: list[str],
    seed: int,
    train_fraction: float = 0.5,
) -> dict[str, list[str] | int]:
    """Family-stratified train/test split for tuning vs final evaluation.

    Every family with at least two members contributes to both sides;
    singleton families go to the test side.
    """
    rng = np.random.default_rng(seed)
    train: list[str] = []
    test: list[str] = []
    for fam in sorted(set(families)):
        members = sorted(n for n, f in zip(names, families) if f == fam)
        perm = rng.permutation(len(members))
        cut = min(max(1, round(train_fraction * len(members))), len(members) - 1)
        train.extend(members[i] for i in perm[:cut])
        test.extend(members[i] for i in perm[cut:])
    return {"seed": seed, "train": sorted(train), "test": sorted(test)}


def save_split(split: dict[str, list[str] | int], path: Path) -> None:
    """Persist the split so every script reads the same manifest."""
    path.write_text(json.dumps(split, indent=2), encoding="utf-8")


names = [f"u{n}_{i}" for n in (50, 100) for i in range(4)]
families = [f"uniform-{n}" for n in (50, 100) for _ in range(4)]
split = split_instances(names, families, seed=2024)
print(len(split["train"]), len(split["test"]), sorted(set(families)))
# Expected: 4 4 ['uniform-100', 'uniform-50'] — two instances per family on each side
```

**Pitfall:** The subtle leak is iterative: tune on train, evaluate on test, dislike the result, retune, re-evaluate. After a few iterations the test set has effectively been tuned on. Pre-register the protocol: the test set is run once per algorithm configuration that appears in the paper. If you need iteration, carve a validation subset out of the train side. A second leak: splitting runs (seeds) of the same instance across train and test — the unit of splitting must be the instance (or the family), never the run.

## Advanced Techniques

### Planted solutions with known optima

For development and regression tests you want instances whose optimal value is known without solving. The generic trick plants a solution and prices the instance so the planted solution is provably optimal. For linear assignment, set the planted entries to cost 0 and everything else positive:

```python
import numpy as np
from scipy.optimize import linear_sum_assignment


def planted_assignment(n: int, seed: int, noise: int = 100) -> tuple[np.ndarray, np.ndarray]:
    """Linear assignment instance whose optimal value is 0 by construction."""
    rng = np.random.default_rng(seed)
    perm = rng.permutation(n)
    cost = rng.integers(1, noise + 1, size=(n, n))
    cost[np.arange(n), perm] = 0
    return cost, perm


cost, perm = planted_assignment(30, seed=11)
rows, cols = linear_sum_assignment(cost)
print(int(cost[rows, cols].sum()))
# Expected: 0 — the planted permutation is provably optimal
```

Zero-margin planting makes instances easy, so use them for correctness tests, not performance claims. Hall & Posner (2001), "Generating experimental data for computational testing with machine scheduling applications", treat the harder question of generating instances with known optima that remain non-trivial to solve.

### Targeting phase transitions with hardness sweeps

When the study needs hard instances, sweep the control parameter (average degree, capacity ratio, constraint density), solve a sample at each setting with a reference solver under a fixed time limit, and plot median solve time against the parameter. Keep the settings around the empirical peak. Report the sweep itself — it documents that hardness was measured, not assumed, and it makes the generator setting reproducible.

### Instance space analysis

Smith-Miles & Bowly (2015), "Generating new test instances by evolving in instance space", project instances into a 2D feature space and ask two questions: where do the standard benchmarks sit (often in a small cluster), and where does each algorithm win? Use the Pattern 8 feature table with a PCA projection to check whether your test bed covers a region or a point. If published benchmarks cluster tightly, complement them with generated instances that fill the empty regions — that is where the interesting algorithm-selection structure lives.

### Evolving instances that discriminate between algorithms

To stress-test a claimed improvement, search the generator's parameter-and-seed space for instances maximizing the performance gap between your method and the baseline — a simple (1+1) evolutionary loop over generator parameters with the measured gap as fitness suffices. If no discriminating instances exist, the methods are equivalent in that family; if many exist, characterize them with features. This is also an effective bug hunter: instances evolved to make two "equivalent" implementations disagree usually expose rounding or tie-breaking differences.

### Scaling families for empirical complexity

To estimate how runtime grows with size, generate families that vary only $n$, keeping all other generator parameters fixed (coefficient range, tightness ratio, cluster count proportional to $n$). Use geometric size steps (50, 100, 200, 400, 800) with the same number of seeds per size, fit $\log t$ against $\log n$, and report the exponent with a confidence interval rather than a single fitted line.

## Practical Challenges

**Recomputed objective does not match the published optimum.** Almost always a convention mismatch: rounding (TSPLIB nearest-integer vs float), distance truncation (Solomon one-decimal vs double), matrix order (QAPLIB flow/distance swap), or 1-based indices read as 0-based. Resolve by recomputing one published solution through your parser and asserting the published value; keep that assertion as a permanent regression test.

**Off-by-one node indexing corrupts solutions silently.** TSPLIB, OR-Library, and QAPLIB files are 1-based; Python is 0-based. The dangerous failure is not a crash but a quietly shifted permutation that remains feasible. Convert to 0-based at the parser boundary, document the convention in the dataclass docstring, and never let raw file indices cross into algorithm code.

**Benchmark overfitting in the literature.** Decades of methods tuned on TSPLIB and Solomon mean that "wins on the standard set" partly measures fit to those specific instances. Mitigate by adding a synthetic family with different structure (clustering, tightness) and reporting both; flag in the write-up when conclusions differ between the benchmark set and the synthetic family.

**Cherry-picked instance subsets.** Selecting "representative" instances after seeing results biases every downstream statistic. Pre-register a rule ("all instances with n ≤ 1000", "the MIPLIB 2017 benchmark subset") before running, and report the rule in the paper. If the full set is too expensive, sample it randomly with a recorded seed.

**Generator drift across code versions.** A refactor that changes the order of `rng` calls changes every generated instance, invalidating cached results. Treat generators as versioned artifacts: store a generator version string in each instance's metadata, write generated instances to disk once, and have experiments read files rather than regenerate. A unit test that regenerates one instance and compares a hash catches drift immediately.

**Parsing cost dominates experiment startup.** Re-parsing a 10,000-node TSPLIB file and rebuilding its distance matrix for every run wastes minutes per experiment. Cache the parsed form (`np.savez` with coords, matrix, metadata) keyed by file hash; keep the raw file as the source of truth so the cache is always re-derivable and never committed as primary data.

**Hardness does not transfer between solvers.** Instances that stall a MIP solver can be trivial for CP or a metaheuristic, and vice versa; empirical hardness is a property of the (instance, algorithm) pair (the lesson of algorithm-selection research). Never label an instance set "hard" in general — say hard for what, and include the reference solver and time limit that established it.

**Best-known values disagree between sources.** VRPTW best-knowns change as new papers appear, and secondary tables copy stale values. Record the source and access date of every best-known value in your metadata file, prefer the maintained primary source (SINTEF for Solomon/Homberger, CVRPLIB for CVRP, QAPLIB pages), and recompute gaps from raw objectives rather than copying gap numbers.

**Redistribution restrictions on benchmark data.** Some libraries restrict redistribution, and shipping copies also freezes stale versions into your repo. Commit a download script with URLs and SHA-256 checksums plus the parser, not the data; verify checksums at download time so a silently changed upstream file fails loudly instead of corrupting results.

**Generated instances are accidentally infeasible.** Random generation can produce VRPs whose total demand exceeds fleet capacity or scheduling instances with empty feasible sets, and a metaheuristic will happily return its best infeasible solution. Decide per family: either constrain the generator so feasibility is guaranteed by construction, or run an independent feasibility check at generation time and regenerate with the next seed, recording the rejection rate.

## Tools & Libraries

| Library / tool | When to use | Note |
|---|---|---|
| `tsplib95` | reading TSPLIB TSP/ATSP/CVRP files | handles all edge-weight types incl. GEO; verify rounding against one known optimum anyway |
| `vrplib` | reading CVRPLIB and Solomon files | one interface for both formats; returns dict-of-arrays |
| `numpy` | matrices, generators, features | `np.random.default_rng(seed)` is the reproducibility backbone |
| `scipy` | k-d trees, `linear_sum_assignment`, sparse matrices | `cKDTree` for nearest-neighbor features at large n |
| `networkx` | graph generators and graph features | G(n,p), geometric, scale-free generators with seeds; slow above ~10^5 edges |
| `pandas` | instance feature tables, split manifests | one row per instance; write parquet or CSV next to the instances |
| `gurobipy` | reading MIPLIB `.mps` files | `gp.read("model.mps")` loads an instance for probing or feature extraction |
| `hashlib` + `urllib` (stdlib) | download scripts with checksums | SHA-256 every benchmark file; fail loudly on mismatch |
| MIPLIB 2017 collection | general-MIP benchmarking | use the curated benchmark subset and the easy/hard/open tags (Gleixner et al. 2021) |

## Output Format

A complete instance-pipeline deliverable contains four artifacts.

**1. Instance set checklist** — confirm every box before experiments start:

- [ ] Every instance has a unique name encoding family, size, and seed (`clu_n200_s7`).
- [ ] Parsers validated by recomputing at least one published solution value per format.
- [ ] Distance/rounding conventions stated explicitly in metadata.
- [ ] Raw files (or a checksummed download script) under version control; caches re-derivable.
- [ ] Generator code versioned; a hash regression test pins generated output.
- [ ] Train/test split manifest written to disk and read by all scripts.
- [ ] Feature table covers all instances (one row each).
- [ ] Best-known values recorded with source and access date.

**2. Set-level metadata file** — one JSON per instance set:

```json
{
  "set_name": "tsp-clustered-v2",
  "created": "2026-06-12",
  "generator": {"module": "gen_tsp.py", "version": "2.1", "kind": "clustered",
                "n_clusters": 8, "cluster_std": 25.0, "box": 1000.0},
  "instances": [
    {"name": "clu_n200_s7", "n": 200, "seed": 7, "file": "clu_n200_s7.tsp"},
    {"name": "clu_n200_s8", "n": 200, "seed": 8, "file": "clu_n200_s8.tsp"}
  ],
  "distance_convention": "TSPLIB EUC_2D nearest-integer",
  "best_known": {"source": "self-computed, Gurobi 12, 3600s", "date": "2026-06-10"},
  "split": {"manifest": "split_seed2024.json", "train_fraction": 0.5}
}
```

**3. Feature report** — the Pattern 8 table, aggregated per family (mean and range of each feature), included in the paper's appendix or supplement.

**4. Reporting paragraph for the paper** — names the libraries and exact subsets used, the generator with all parameters and seeds, the convention statement, the split protocol, and where readers can regenerate or download everything. If a reader cannot rebuild the instance set from this paragraph plus the repository, the description is incomplete.

## Questions to Ask

- Which problem class, and does a standard benchmark library already exist for it?
- Must the results be comparable to published numbers, or is this an internal study?
- What distance/rounding convention do the target benchmarks use, and is it documented?
- How many instances and what sizes does the compute budget realistically allow?
- Are the instances for debugging, tuning, or final evaluation — and is the split already fixed?
- Should generated instances be application-like, deliberately hard, or a scaling family?
- Is feasibility of generated instances guaranteed by construction or checked afterwards?
- Can the benchmark files be redistributed with the code, or is a download script needed?
- Where will best-known values come from, and how will they be kept current?

## Related Skills

- **algorithm-benchmarking-statistics** — when the instance set is ready and the question becomes how to run, measure, and statistically compare algorithms on it.
- **traveling-salesman-problem** — when the TSPLIB instances parsed here need formulations, construction heuristics, and local search to actually solve them.
- **optimization-project-structure** — when instance files, caches, manifests, and download scripts need a reproducible place in the research-code layout.
- **solution-validation-testing** — when parsers and generators need regression tests against known optima and independent feasibility checkers.
