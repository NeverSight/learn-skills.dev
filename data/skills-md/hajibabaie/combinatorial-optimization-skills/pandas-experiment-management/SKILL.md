---
name: pandas-experiment-management
description: When the user wants to record, store, and aggregate computational-experiment results for optimization algorithms with pandas - tidy one-row-per-run tables, run metadata (instance, seed, algorithm, parameters, runtime, objective), atomic CSV/parquet writing, aggregation across instances and seeds, and pivot tables for papers. Also use when the user mentions "experiment results," "results dataframe," "aggregate runs," "experiment tracking," "results CSV," "results parquet," or when thousands of raw runs must become one defensible paper table. For statistical comparison of algorithms, see algorithm-benchmarking-statistics; for turning result tables into figures, see matplotlib-optimization-visualization.
---

# Pandas Experiment Management

You are an expert in managing computational-experiment data for combinatorial optimization research.
This skill covers tidy result tables (one row per run), run-metadata capture, atomic CSV/parquet
writing, aggregation across instances and seeds, and pivot tables ready for papers. Use the pattern
catalog below to build a results pipeline that survives crashes, parallel workers, and reviewer
questions — and that turns thousands of raw runs into one table you can defend.

## Initial Assessment

Establish these facts before recommending a results pipeline:

- **Campaign size.** Count expected rows: instances × algorithms × configurations × seeds. A
  3-algorithm, 30-instance, 10-seed study is 900 rows (CSV is fine); a tuning campaign with 500
  configurations is 150,000 rows (parquet, partitioning).
- **Run cost.** Seconds per run or hours per run? Expensive runs make crash-safe writing and
  resume logic mandatory, not optional.
- **Parallelism.** Single process, `multiprocessing` pool, or cluster array jobs writing to a
  shared filesystem? This decides the write strategy (one file per run vs. one shared file).
- **What is recorded per run.** Final objective only, or also the incumbent trace over time?
  Traces need their own table (long format), never list-valued cells in the runs table.
- **Optimization sense.** Minimization or maximization? Mixed across problems? Store the raw
  objective plus a `sense` column; convert only at aggregation time.
- **Reference values.** Are best-known solutions (BKS) available for gap computation, or is the
  reference the best value found inside the campaign itself?
- **Failure modes.** Can runs time out, crash, or end infeasible? The schema needs a `status`
  column from day one; retrofitting it later contaminates every aggregate already computed.
- **Downstream consumers.** Statistical tests, convergence plots, LaTeX tables for a paper, or
  all three? The tidy runs table must serve all of them without re-running experiments.
- **Storage stack.** Is `pyarrow` available for parquet? Is the filesystem local or networked
  (atomicity of `os.replace` holds within one filesystem only)?
- **Existing data.** Is there a legacy spreadsheet or ad-hoc CSV to migrate? Migrate once, into
  the schema below, and freeze the old files as read-only.

## The Tidy Results Layer

The foundation is tidy data (Wickham 2014, "Tidy Data"): each variable is a column, each
observation is a row, each type of observational unit is a table. For optimization
experiments the observational unit is **one run** — one execution of one algorithm configuration
on one instance with one seed. Everything else (per-algorithm summaries, per-instance pivots,
paper tables) is a *derived view*, recomputed from the runs table by a script.

### Column taxonomy

| Column group | Typical columns | Role |
|---|---|---|
| Identity | `run_id`, `timestamp_utc`, `host` | unique row identity, audit trail |
| Factors | `instance`, `algorithm`, `config_id`, `seed`, `param_*` | everything you will ever `groupby` |
| Responses | `objective`, `runtime_sec`, `iterations`, `status`, `feasible` | measured outcomes |
| Provenance | `git_commit`, `solver_version`, `instance_md5` | reproduce-this-number metadata |

### The run key

The tuple `(instance, algorithm, config_id, seed)` is the **run key**. Two invariants must hold
across the whole campaign:

1. The run key is unique in the consolidated table (enforce on load, Pattern 5).
2. The planned campaign is a full factorial over the key components (or a documented subset), so
   completeness can be checked by an anti-join against the plan (Pattern 6).

### Two tables, not one

Keep **two** tidy tables linked by `run_id`:

- `runs` — one row per run, final outcomes only.
- `traces` — one row per incumbent improvement: `run_id`, `time_sec`, `best_obj` (Pattern 10).

Storing traces inside the runs table (lists in cells, stringified arrays) breaks `groupby`,
inflates file size, and makes parquet column compression useless.

### Gaps as the common currency

Raw objectives are not comparable across instances of different scale. The standard normalization
for minimization with positive reference value $f^{\mathrm{ref}}_i$ (best known, or best found in
the campaign) is the percentage gap:

$$ \mathrm{gap}_{a,i} = 100 \cdot \frac{f_{a,i} - f^{\mathrm{ref}}_i}{f^{\mathrm{ref}}_i} $$

If $f^{\mathrm{ref}}_i$ can be zero or negative (e.g., net-profit objectives), shift the
denominator (`max(|f_ref|, 1)`) or report absolute differences and say so in the caption. A
negative gap means the campaign improved a best-known value — verify it with an independent
feasibility checker before celebrating.

### Storage format decision table

| Format | Use when | Notes |
|---|---|---|
| One JSON file per run | during the campaign | crash-safe, parallel-safe, trivially resumable |
| CSV | human inspection; consolidated tables < ~10^5 rows | dtypes drift on round-trip; set `float_format` |
| Parquet | canonical consolidated store | dtypes preserved, compressed, fast; needs `pyarrow` |
| Partitioned parquet + DuckDB | > ~10^7 rows, query-without-loading | SQL over file globs; see Advanced Techniques |

Decision guidance:

- **During the campaign:** append-only, one small file per run (Patterns 1-3).
- **After (or periodically during) the campaign:** consolidate to one parquet/CSV (Pattern 4).
- **At analysis time:** load through a schema contract (Pattern 5), aggregate (Patterns 7-9).
- Wide layouts (algorithms as columns) exist only at presentation time, produced by `pivot`.
  Storage stays long/tidy forever.

## Recording Runs

### Pattern 1 — One row per run, parameters flattened

Every run, successful or not, becomes exactly one flat dict. Algorithm parameters are flattened
into `param_<name>` columns so that later `groupby("param_tenure")` works without parsing strings.

```python
import dataclasses
import datetime
import platform
import uuid


@dataclasses.dataclass(frozen=True)
class RunRecord:
    """One finished algorithm run; becomes exactly one row in the results table."""

    instance: str
    algorithm: str
    seed: int
    params: dict[str, object]
    objective: float
    runtime_sec: float
    iterations: int
    status: str  # "ok" | "timeout" | "error" | "infeasible"
    run_id: str = dataclasses.field(default_factory=lambda: uuid.uuid4().hex[:12])
    timestamp_utc: str = dataclasses.field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
    )
    host: str = dataclasses.field(default_factory=platform.node)

    def to_row(self) -> dict[str, object]:
        """Flatten to one flat dict; params become param_<name> columns."""
        row = dataclasses.asdict(self)
        for key, value in row.pop("params").items():
            row[f"param_{key}"] = value
        return row


rec = RunRecord(
    instance="tai30a", algorithm="tabu_search", seed=7,
    params={"tenure": 9, "max_iters": 20000},
    objective=1818146.0, runtime_sec=3.41, iterations=20000, status="ok",
)
print(sorted(k for k in rec.to_row() if k.startswith("param_")))
# Expected: ['param_max_iters', 'param_tenure']
```

**Pitfall:** Storing the parameter dict as a single stringified column makes every later
`groupby`, `pivot`, and filter require string parsing — flatten at write time. Flattening must be
stable: if a later campaign phase renames `tenure` to `tabu_tenure`, the table silently forks into
two half-empty columns. Renames are forbidden; add a new parameter name only together with a new
`config_id` (Pattern 2) and record the change in a lookup file.

### Pattern 2 — Stable configuration identifiers

When tuning produces dozens of parameter combinations, grouping by every `param_*` column is
clumsy. Hash the canonical JSON of the parameter dict into a short `config_id` and group by that.

```python
import hashlib
import json


def config_id(params: dict[str, object]) -> str:
    """Stable short id for a parameter configuration.

    Canonical JSON (sorted keys, compact separators) hashed with sha1:
    the same dict gives the same id on every machine and every run.
    """
    blob = json.dumps(params, sort_keys=True, separators=(",", ":"), default=repr)
    return hashlib.sha1(blob.encode("utf-8")).hexdigest()[:10]


print(config_id({"tenure": 9, "alpha": 0.3}) == config_id({"alpha": 0.3, "tenure": 9}))
# Expected: True
```

**Pitfall:** `str(params)` or an unsorted `json.dumps` is not canonical — Python dict insertion
order differs between call sites, so identical configurations get different ids and your seeds-
per-configuration counts silently drop. Also store the canonical JSON itself in a `params_json`
column (or a separate `configs.csv` with one row per `config_id`): a hash without its preimage
cannot answer "what was configuration `3fa2b81c90` again?" two months later.

### Pattern 3 — Atomic one-file-per-run writes

Parallel workers appending to one shared CSV interleave bytes and corrupt the file; a crash during
`to_csv` leaves a half-written row. The robust pattern: each run writes its own small JSON file,
via a temporary name plus `os.replace`, which is atomic on both POSIX and Windows.

```python
import json
import os
import tempfile
from pathlib import Path


def write_row_atomic(row: dict[str, object], out_dir: Path) -> Path:
    """Write one run record as its own JSON file, atomically.

    Write to a temporary file in the same directory, then os.replace it
    into its final name. A crash can never leave a half-written file
    visible under the final name.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    final = out_dir / f"{row['run_id']}.json"
    fd, tmp_name = tempfile.mkstemp(dir=out_dir, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(row, fh)
        os.replace(tmp_name, final)
    except BaseException:
        os.unlink(tmp_name)
        raise
    return final


with tempfile.TemporaryDirectory() as d:
    p = write_row_atomic({"run_id": "abc123", "objective": 42.0}, Path(d))
    print(p.name)
# Expected: abc123.json
```

**Pitfall:** The temporary file must live in the *destination directory*. `os.replace` is atomic
only within one filesystem; a temp file in `/tmp` moved to a network share degrades to a
copy-then-delete, which can be interrupted half-way. Name the final file after `run_id` (unique by
construction), not after the run key — a retried run then creates a second file instead of
clobbering evidence of the first attempt, and deduplication happens explicitly at consolidation.

## Consolidating, Loading, and Resuming

### Pattern 4 — Consolidate per-run files into one table

Thousands of small JSON files are great for writing and terrible for analysis. Periodically (and
at campaign end) merge them into one tidy table, deduplicate on `run_id`, and write the output
atomically too.

```python
import json
import tempfile
from pathlib import Path

import pandas as pd


def consolidate_runs(run_dir: Path, out_path: Path) -> pd.DataFrame:
    """Merge all per-run JSON files into one tidy table; write it atomically.

    Suffix of out_path picks the format: .parquet (needs pyarrow) or .csv.
    """
    rows = [json.loads(p.read_text(encoding="utf-8")) for p in sorted(run_dir.glob("*.json"))]
    df = pd.DataFrame(rows).drop_duplicates(subset="run_id", keep="last")
    tmp = out_path.with_name(out_path.name + ".tmp")
    if out_path.suffix == ".parquet":
        df.to_parquet(tmp, index=False)
    else:
        df.to_csv(tmp, index=False)
    tmp.replace(out_path)
    return df


with tempfile.TemporaryDirectory() as d:
    run_dir = Path(d)
    for i in range(3):
        (run_dir / f"r{i}.json").write_text(
            json.dumps({"run_id": f"r{i}", "objective": float(i)}), encoding="utf-8"
        )
    df = consolidate_runs(run_dir, run_dir / "all_runs.csv")
    print(len(df))
# Expected: 3
```

**Pitfall:** Consolidation must be idempotent — running it twice must give the same table. That is
why it reads *all* per-run files every time and deduplicates, instead of appending "new" rows to
the previous output. Keep the raw per-run JSON files until the paper is accepted; they are the
source of truth, and disk is cheaper than re-running a two-week campaign because a consolidation
script had a bug.

### Pattern 5 — A schema contract at the load boundary

Analysis code should never discover halfway through that `seed` became `float64` or that two rows
share a run key. Validate once, at the file boundary, then trust the frame everywhere downstream.

```python
import os
import tempfile

import pandas as pd

RESULTS_SCHEMA: dict[str, str] = {
    "run_id": "string",
    "instance": "string",
    "algorithm": "string",
    "config_id": "string",
    "seed": "int64",
    "objective": "float64",
    "runtime_sec": "float64",
    "status": "string",
}
RUN_KEY = ["instance", "algorithm", "config_id", "seed"]


def load_results(path: str) -> pd.DataFrame:
    """Load a results table and enforce the column contract."""
    df = pd.read_parquet(path) if path.endswith(".parquet") else pd.read_csv(path)
    missing = sorted(set(RESULTS_SCHEMA) - set(df.columns))
    if missing:
        raise ValueError(f"{path}: missing columns {missing}")
    df = df.astype(RESULTS_SCHEMA)
    dup = df.duplicated(subset=RUN_KEY, keep=False)
    if dup.any():
        raise ValueError(f"{path}: {int(dup.sum())} rows share a run key {RUN_KEY}")
    return df


with tempfile.TemporaryDirectory() as d:
    p = os.path.join(d, "runs.csv")
    pd.DataFrame({
        "run_id": ["a", "b"], "instance": ["i1", "i1"], "algorithm": ["ts", "ts"],
        "config_id": ["c0", "c0"], "seed": [1, 2],
        "objective": [10.0, 12.0], "runtime_sec": [1.0, 1.1], "status": ["ok", "ok"],
    }).to_csv(p, index=False)
    print(load_results(p)["seed"].dtype)
# Expected: int64
```

**Pitfall:** CSV round-trips drift dtypes. The classic case: one crashed run wrote a missing seed,
pandas upcasts the whole column to `float64`, and `astype("int64")` raises. That loud failure is
*correct* — it points at a recorder bug. Reach for the nullable `"Int64"` dtype only when missing
values are genuinely legitimate. Do not scatter defensive checks through analysis code; the file
boundary is the one real validation point.

### Pattern 6 — Campaign plan and resume by anti-join

A campaign that runs for days will be interrupted. Resume logic must answer exactly: which planned
runs have no completed row yet? Build the full factorial plan, then anti-join against the
consolidated results on the run key.

```python
import itertools

import pandas as pd


def build_plan(instances: list[str], algorithms: list[str], seeds: list[int]) -> pd.DataFrame:
    """Full factorial run plan: one row per run that should exist."""
    rows = itertools.product(instances, algorithms, seeds)
    return pd.DataFrame(rows, columns=["instance", "algorithm", "seed"])


def pending_runs(plan: pd.DataFrame, done: pd.DataFrame) -> pd.DataFrame:
    """Anti-join: plan rows with no completed run yet."""
    key = ["instance", "algorithm", "seed"]
    merged = plan.merge(done[key].drop_duplicates(), on=key, how="left", indicator=True)
    return merged.loc[merged["_merge"] == "left_only", key].reset_index(drop=True)


plan = build_plan(["i1", "i2"], ["ts"], [1, 2])
done = pd.DataFrame({"instance": ["i1"], "algorithm": ["ts"], "seed": [1]})
print(len(pending_runs(plan, done)))
# Expected: 3
```

**Pitfall:** Resuming by counting files (`if len(files) < n_planned: rerun everything`) cannot say
*which* runs are missing; the anti-join is exact. Decide explicitly what "done" means: if `done`
includes rows with `status == "error"`, those runs will not be retried. Filter
(`done[done.status == "ok"]`) when failed runs should be re-dispatched, and cap retries so a
deterministic crash does not loop forever.

## Aggregating Across Instances and Seeds

### Pattern 7 — Collapse seeds first, then compute gaps

Aggregation has a fixed order: (1) collapse seed replications to per-(instance, algorithm)
statistics; (2) normalize to gaps per instance; (3) only then average across instances. Skipping
step 2 averages raw objectives of different scales, which is meaningless.

```python
import pandas as pd


def aggregate_over_seeds(df: pd.DataFrame) -> pd.DataFrame:
    """Collapse seed replications: one row per (instance, algorithm)."""
    return (
        df.groupby(["instance", "algorithm"], as_index=False)
        .agg(
            obj_best=("objective", "min"),
            obj_mean=("objective", "mean"),
            obj_std=("objective", "std"),
            time_mean=("runtime_sec", "mean"),
            n_seeds=("seed", "nunique"),
        )
    )


def add_gap_columns(agg: pd.DataFrame, best_known: pd.Series | None = None) -> pd.DataFrame:
    """Add percentage gaps to a per-instance reference (minimization).

    best_known: optional Series indexed by instance name. If None, the
    reference is the best objective any algorithm found for that instance.
    """
    agg = agg.copy()
    if best_known is None:
        ref = agg.groupby("instance")["obj_best"].transform("min")
    else:
        ref = agg["instance"].map(best_known)
    agg["gap_best"] = 100.0 * (agg["obj_best"] - ref) / ref
    agg["gap_mean"] = 100.0 * (agg["obj_mean"] - ref) / ref
    return agg


runs = pd.DataFrame({
    "instance": ["i1"] * 4 + ["i2"] * 4,
    "algorithm": ["ts", "ts", "sa", "sa"] * 2,
    "seed": [1, 2, 1, 2] * 2,
    "objective": [10.0, 12.0, 11.0, 15.0, 90.0, 100.0, 95.0, 105.0],
    "runtime_sec": [1.0] * 8,
})
agg = add_gap_columns(aggregate_over_seeds(runs))
row = agg[(agg["instance"] == "i1") & (agg["algorithm"] == "sa")]
print(float(row["gap_mean"].iloc[0]))
# Expected: 30.0
```

**Pitfall:** "Mean of gaps" and "gap of means" differ once the reference varies by instance — fix
the order above and state it in the paper ("gaps computed per instance from mean-over-10-seeds
objectives, then averaged"). A *negative* gap against published best-known values means either a
new best solution or a bug in your objective computation; run the independent feasibility checker
before claiming the former. For maximization, negate the gap formula explicitly — do not flip
objective signs inside the table, or every later reader misreads the raw column.

### Pattern 8 — Paired win/tie/loss counts

Reviewers ask "on how many instances is A better than B?" Pair the algorithms per instance on the
same aggregate (mean over the same seed set), compare with a tolerance, and count.

```python
import pandas as pd


def win_tie_loss(
    runs: pd.DataFrame, algo_a: str, algo_b: str, tol: float = 1e-6
) -> dict[str, int]:
    """Per-instance paired comparison of mean-over-seeds objectives (minimization)."""
    means = runs.groupby(["instance", "algorithm"])["objective"].mean().unstack("algorithm")
    a, b = means[algo_a], means[algo_b]
    return {
        "wins": int((a < b - tol).sum()),
        "ties": int(((a - b).abs() <= tol).sum()),
        "losses": int((a > b + tol).sum()),
    }


runs = pd.DataFrame({
    "instance": ["i1"] * 4 + ["i2"] * 4,
    "algorithm": ["ts", "ts", "sa", "sa"] * 2,
    "seed": [1, 2, 1, 2] * 2,
    "objective": [10.0, 12.0, 11.0, 15.0, 90.0, 100.0, 95.0, 105.0],
})
print(win_tie_loss(runs, "ts", "sa"))
# Expected: {'wins': 2, 'ties': 0, 'losses': 0}
```

**Pitfall:** Without a tolerance, two objectives differing in the 12th decimal digit count as a
"win". Set `tol` from the objective's natural resolution (1 for integer-valued objectives). And a
win/tie/loss count alone is not evidence: 18-2-10 can be statistically insignificant. Follow up
with a Wilcoxon signed-rank test on the paired values — see algorithm-benchmarking-statistics for
the protocol, including why pairing on common seeds tightens the comparison.

### Pattern 9 — Pivot tables and LaTeX export

The paper table is a pivot: instances as rows, algorithms as columns, one summary statistic as
values, an average row at the bottom, best value per row in bold. Generate it from the aggregated
frame; never hand-edit numbers.

```python
import numpy as np
import pandas as pd


def paper_pivot(agg: pd.DataFrame, value: str = "gap_mean") -> pd.DataFrame:
    """Instances as rows, algorithms as columns, plus a closing average row."""
    table = agg.pivot(index="instance", columns="algorithm", values=value).sort_index()
    table.loc["average"] = table.mean(axis=0)
    return table


def to_latex_bold_best(table: pd.DataFrame, minimize: bool = True, decimals: int = 2) -> str:
    """Render a numeric pivot to LaTeX (booktabs rules), best value per row in bold."""

    def fmt_row(row: pd.Series) -> pd.Series:
        best = row.min() if minimize else row.max()
        texts = {
            col: (rf"\textbf{{{val:.{decimals}f}}}" if np.isclose(val, best)
                  else f"{val:.{decimals}f}")
            for col, val in row.items()
        }
        return pd.Series(texts)

    return table.apply(fmt_row, axis=1).to_latex(escape=False)


agg = pd.DataFrame({
    "instance": ["i1", "i1", "i2", "i2"],
    "algorithm": ["sa", "ts", "sa", "ts"],
    "gap_mean": [30.0, 10.0, 11.1, 5.6],
})
table = paper_pivot(agg)
print(table.loc["average", "ts"], r"\textbf{10.00}" in to_latex_bold_best(table))
# Expected: 7.8 True
```

**Pitfall:** `pivot` silently inserts NaN for missing (instance, algorithm) combinations, and the
average row then averages *different instance subsets per column* — an unfair comparison that is
invisible in the rendered table. Assert completeness first: `assert table.drop(index="average",
errors="ignore").notna().all().all()`, ideally against the campaign plan from Pattern 6. Regenerate
the `.tex` file from a script on every data change (`scripts/make_tables.py`); the moment someone
edits the LaTeX by hand, the table and the data diverge forever. The output uses booktabs rules
(`\toprule` etc.), so load the `booktabs` package.

## Convergence Traces

### Pattern 10 — Long-format traces aligned to a common grid

Convergence plots and time-to-target analyses need the incumbent objective over time, per run.
Record one row per *improvement event* (not per iteration), then align all runs onto a common time
grid with step interpolation before averaging.

```python
import numpy as np
import pandas as pd


def trace_rows(run_id: str, events: list[tuple[float, float]]) -> pd.DataFrame:
    """Long-format incumbent trace: one row per improvement event."""
    df = pd.DataFrame(events, columns=["time_sec", "best_obj"])
    df.insert(0, "run_id", run_id)
    return df


def align_traces(traces: pd.DataFrame, grid: np.ndarray) -> pd.DataFrame:
    """Sample each run's best-so-far objective on a common time grid.

    Step interpolation: at grid time t, take the last event at or before t.
    Grid points before a run's first event get NaN, not an invented value.
    """
    parts = []
    for run_id, g in traces.groupby("run_id", sort=False):
        g = g.sort_values("time_sec")
        idx = np.searchsorted(g["time_sec"].to_numpy(), grid, side="right") - 1
        vals = np.where(idx >= 0, g["best_obj"].to_numpy()[np.maximum(idx, 0)], np.nan)
        parts.append(pd.DataFrame({"run_id": run_id, "time_sec": grid, "best_obj": vals}))
    return pd.concat(parts, ignore_index=True)


t1 = trace_rows("r1", [(0.0, 50.0), (1.2, 42.0), (3.0, 40.0)])
t2 = trace_rows("r2", [(0.0, 55.0), (2.5, 41.0)])
aligned = align_traces(pd.concat([t1, t2]), grid=np.array([0.0, 2.0, 4.0]))
band = aligned.groupby("time_sec")["best_obj"].mean()
print(band.loc[2.0])
# Expected: 48.5
```

**Pitfall:** Logging every iteration produces 10^6-row traces per run and gigabyte files for
nothing — best-so-far is a step function fully determined by its improvement events. Averaging
across runs requires that every run has a defined value at each grid point: truncate the grid at
the shortest run's time limit, or report medians and state the NaN policy. The aligned table is
exactly what matplotlib-optimization-visualization expects for mean-plus-band convergence plots;
linear interpolation between incumbents is wrong (the incumbent does not improve continuously).

## Advanced Techniques

### Failed and censored runs in aggregates

Dropping failed runs before `groupby` makes a fragile algorithm look strong: its surviving seeds
are a biased sample. Keep failures in the table and make the success rate a first-class column.

```python
import numpy as np
import pandas as pd


def seed_aggregate_with_failures(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate over seeds; means use successful runs, failures stay visible."""
    ok = df["status"].eq("ok")
    g = df.assign(obj_ok=df["objective"].where(ok)).groupby(
        ["instance", "algorithm"], as_index=False
    )
    out = g.agg(
        obj_mean=("obj_ok", "mean"),
        n_ok=("obj_ok", "count"),
        n_runs=("status", "size"),
    )
    out["success_rate"] = out["n_ok"] / out["n_runs"]
    return out


runs = pd.DataFrame({
    "instance": ["i1"] * 3, "algorithm": ["ts"] * 3, "seed": [1, 2, 3],
    "objective": [10.0, 11.0, np.nan], "status": ["ok", "ok", "timeout"],
})
out = seed_aggregate_with_failures(runs)
print(float(out["obj_mean"].iloc[0]), round(float(out["success_rate"].iloc[0]), 2))
# Expected: 10.5 0.67
```

Timeouts that still return a feasible incumbent are *censored*, not failed: record the incumbent
with `status="timeout"` and decide per analysis whether censored objectives enter the mean (they
usually should, with the time limit stated in the caption).

### Normalizing across heterogeneous instances

Three defensible normalizations, in increasing robustness: percentage gaps (Pattern 7), ranks per
instance (the input to a Friedman test), and the shifted geometric mean for runtimes — the
standard in MIP benchmarking (Achterberg 2007, "Constraint Integer Programming") because it damps
both near-zero times and outliers.

```python
import numpy as np


def shifted_geomean(values: np.ndarray, shift: float = 10.0) -> float:
    """Shifted geometric mean, standard for aggregating runtimes across instances."""
    values = np.asarray(values, dtype=float)
    return float(np.exp(np.mean(np.log(values + shift))) - shift)


print(round(shifted_geomean(np.array([1.0, 100.0])), 2))
# Expected: 24.79
```

The arithmetic mean of those two runtimes is 50.5 — dominated by the slow instance; the shifted
geometric mean (24.79) weighs both. Never average raw objective values across instances under any
of these schemes; normalize first.

### Provenance columns

Every row should be traceable to the exact code and data that produced it. At run time (not at
analysis time), capture: the short git commit via
`subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True)`, the
solver version (`gurobipy.gurobi.version()` or equivalent), and an `instance_md5` checksum of the
instance file (`hashlib.md5(path.read_bytes()).hexdigest()`). When a reviewer asks why Table 3
changed between submissions, `runs[runs.git_commit == "a1b2c3d"]` answers in one line. Tag the
commit that produced each paper-table snapshot.

### Partitioned storage for large campaigns

Beyond ~10^7 rows (large tuning studies, per-iteration traces), one flat file stops working. Two
escalation steps: (1) partitioned parquet —
`results/algorithm=ts/instance_set=tai/part-0.parquet` — which `pandas.read_parquet` and pyarrow
datasets can filter by partition without reading everything; (2) DuckDB, which runs SQL directly
over file globs (`SELECT instance, avg(objective) FROM 'results/**/*.parquet' GROUP BY instance`)
with no load step and spills to disk instead of exhausting RAM. The tidy schema is unchanged;
only the container grows.

### Keep tuning results out of paper tables

Parameter-tuning runs and final-evaluation runs answer different questions and must live in
different tables (`results/tuning/`, `results/final/`). Reporting the tuned configuration's
performance on the instances it was tuned on is overfitting in the experimental-design sense; hold
out a test set of instances for the paper table. See instance-generation-and-benchmarks for
train/test instance splits and optuna-style tuning protocols for the tuning loop itself.

## Practical Challenges

**Two workers produced rows with the same run key.** Deduplicate at consolidation
(`drop_duplicates(subset=RUN_KEY, keep="last")` after sorting by timestamp), then find the root
cause: usually a dispatcher that re-issued a plan row after a worker stalled. Make the dispatcher
derive work items only from the `pending_runs` anti-join, and make duplicate keys a hard error at
load time so the issue cannot resurface silently.

**The seed column became float and `astype("int64")` now fails.** One run wrote a missing seed and
CSV has no integer-with-missing representation, so pandas upcast the column. Quarantine the broken
rows into a separate file for inspection, fix the recorder so `seed` is always written, and only
use the nullable `"Int64"` dtype if missing seeds are a legitimate state in your design.

**A mid-campaign parameter change forked the table.** New `param_*` columns are NaN for old rows
and old columns are NaN for new rows. This is recoverable if every row has a `config_id`: treat
the phases as distinct configurations, document both in `configs.csv`, and never compare across
phases as if they were one configuration. Without config ids, the phases can only be separated by
timestamp — fragile and embarrassing in a rebuttal.

**Means look great because failed seeds vanished.** A `dropna()` early in the pipeline removed
crashed and timed-out runs, leaving a biased sample of lucky seeds. Aggregate with the
status-aware pattern (Advanced Techniques) and always print `n_ok / n_runs` next to any mean. A
mean over 6 of 10 seeds is a different claim than a mean over 10.

**Excel mangled instance names and seeds.** Opening the results CSV in Excel converted `OCT4` to a
date and stripped leading zeros from ids, then someone saved it back. Keep the canonical store in
parquet (or a write-protected CSV), and export disposable view copies for spreadsheet users. Any
file a spreadsheet program has saved is no longer trusted data.

**Trace files are gigabytes.** Per-iteration logging again. Record improvement events only
(Pattern 10); a run's best-so-far curve rarely has more than a few hundred improvements. If traces
are already huge, downsample once onto a fixed grid with `align_traces`, store the aligned table,
and archive the raw traces compressed.

**The pivot's average row compares unequal instance subsets.** Some (instance, algorithm) cells
are NaN because runs are missing, and column means then cover different instances. Check
completeness against the plan before pivoting; if a cell is legitimately impossible (algorithm
inapplicable), exclude that instance from *all* columns of the summary row and say so in the
caption.

**A number in the paper cannot be traced to code.** The table was produced by a script that has
since changed, from a results file that was overwritten. Prevention is cheap: provenance columns
on every row, generated `.tex` tables only, a git tag per submitted table snapshot, and raw
per-run files kept read-only. Reconstruction after the fact is somewhere between painful and
impossible.

**Raw objectives were averaged across instances.** A summary said "algorithm A: mean objective
5,432" over instances whose optima range from 50 to 50,000 — the large instances drown out
everything. Recompute as mean gap, mean rank, or shifted geometric mean as appropriate, and add a
unit test that fails when an aggregation groups across `instance` without a prior normalization
column.

**CSV round-trips change the 15th decimal and diff-based checks fire.** `to_csv` writes a default
float representation; re-reading gives a bitwise-different frame. Either write parquet (exact), or
set `float_format="%.17g"` for round-trippable CSV, and compare frames with
`pandas.testing.assert_frame_equal(..., rtol=1e-12)` instead of `==`.

## Tools & Libraries

| Library | Use for | Note |
|---|---|---|
| pandas | the whole results layer | `groupby`/`pivot`/`merge` cover every pattern here |
| numpy | grid alignment, vectorized stats | `searchsorted`, `isclose`, geometric means |
| pyarrow | parquet engine | install it; CSV-only pipelines drift dtypes |
| duckdb | SQL over many parquet/CSV files | query 10^8 rows without loading into RAM |
| fastparquet | parquet alternative | lighter install when pyarrow is too heavy |
| tabulate | quick console tables | sanity-check aggregates before LaTeX export |
| openpyxl / xlsxwriter | Excel export for collaborators | export views only; never re-import |
| mlflow / W&B | heavyweight run tracking | built for ML loops; usually overkill for batch OR campaigns — the tidy-files pattern is simpler and survives offline clusters |

## Output Format

A finished experiment-management setup hands over the following artifacts.

Results directory template:

```text
results/
  raw/                      # one JSON per run, append-only, read-only after campaign
    a3f9c2e41b07.json
    ...
  runs.parquet              # consolidated tidy table (Pattern 4), regenerated, never edited
  traces.parquet            # long-format improvement events, linked by run_id
  configs.csv               # config_id -> canonical params_json, one row per configuration
  plan.csv                  # full factorial campaign plan (Pattern 6)
  tables/
    main_comparison.tex     # generated by scripts/make_tables.py only
```

Schema checklist — every results table has:

- [ ] one row per run; no list-valued or dict-valued cells
- [ ] full run key (`instance`, `algorithm`, `config_id`, `seed`) and uniqueness enforced on load
- [ ] `status` column covering ok / timeout / error / infeasible
- [ ] `objective`, `runtime_sec` as floats; `seed` as integer
- [ ] provenance: `git_commit`, `solver_version`, `instance_md5`, `timestamp_utc`, `host`
- [ ] parameters flattened to `param_*` columns and hashed into `config_id`

Pre-paper-table checklist — before any table goes into the manuscript:

- [ ] completeness verified: anti-join of plan vs. results is empty (or gaps documented)
- [ ] success rates reported wherever failures occurred; censored runs handled explicitly
- [ ] aggregation order stated: seeds collapsed first, gaps per instance, then across instances
- [ ] best-per-row bolding generated by code, with an explicit tolerance
- [ ] `.tex` produced by a script, committed, and the producing commit tagged
- [ ] statistical backing for any "better than" claim (see algorithm-benchmarking-statistics)

## Questions to Ask

- How many instances, algorithms, configurations, and seeds — what is the expected row count?
- How expensive is one run, and how likely are interruptions (cluster preemption, time limits)?
- Do runs execute in parallel, and do workers share a filesystem?
- Minimization or maximization — and is the sense uniform across all problems in the study?
- Are best-known values available per instance, or is the reference internal to the campaign?
- Do you need incumbent traces for convergence plots, or final objectives only?
- Can runs fail or time out, and should a timed-out incumbent count as a result?
- Who consumes the tables — statistics scripts, plotting scripts, LaTeX, a co-author with Excel?
- Is `pyarrow` (or another parquet engine) available in the execution environment?
- Is there existing result data that must be migrated into the schema?

## Related Skills

- **algorithm-benchmarking-statistics** — when aggregated tables must back a claim: Wilcoxon and
  Friedman tests, effect sizes, performance profiles, and reporting protocols.
- **matplotlib-optimization-visualization** — when result and trace tables become convergence
  bands, performance profiles, and other publication figures.
- **optimization-project-structure** — when the surrounding codebase (configs, scripts, results
  directories, factories, seeds) needs the same discipline as the tables.
- **instance-generation-and-benchmarks** — when choosing benchmark sets, generating synthetic
  instances, and splitting train/test instances for the campaign these tables record.
