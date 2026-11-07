---
name: algorithm-benchmarking-statistics
description: When the user wants to compare optimization algorithms with a sound empirical protocol — instance and seed design, time limits, best/mean/gap reporting, nonparametric hypothesis tests, effect sizes, and the plots that summarize them. Also use when the user mentions "compare algorithms," "statistical test," "Wilcoxon," "Friedman test," "performance profile," "time-to-target," or asks "is my algorithm better" than a baseline. For benchmark instance sets and parsers, see instance-generation-and-benchmarks; for tidy run tables and aggregation, see pandas-experiment-management.
---

# Algorithm Benchmarking & Statistics

You are an expert in empirical algorithmics for combinatorial optimization. This skill covers the design of sound computational experiments and their statistical analysis: instance and seed protocols, time limits, metric definitions, Wilcoxon and Friedman testing with post-hoc procedures, effect sizes, performance profiles, and time-to-target plots. Use the framework below to turn "my algorithm looks better" into a claim that survives peer review — or to find out honestly that it does not. Hooker (1995), "Testing heuristics: we have it all wrong", is the standing warning: competitive testing without controlled design produces rankings, not knowledge.

## Initial Assessment

Establish these points before running a single experiment:

- **State the claim as one falsifiable sentence.** Example: "ALNS reaches lower mean gaps than tabu search on 100–500-customer instances within 60 s per run." Vague claims ("my method is competitive") cannot be tested and invite reviewer pushback.
- **Identify the experimental unit.** The instance is the unit of replication. Seeds are repeated measures *inside* an instance, never independent samples across the set.
- **Fix the competitor set and provenance.** Which baselines, which implementations, which parameter settings? Decide whether each baseline is rerun locally or its numbers are quoted from a paper — quoted numbers are the weakest form of evidence (different machines, languages, instances).
- **Fix the instance set.** Source (TSPLIB, OR-Library, Solomon, generated), size range, and count. Aim for 15–30+ instances for a paired two-algorithm test, 10+ for Friedman with k ≥ 3 algorithms. Document why these instances and not others.
- **Separate tuning from testing.** Parameters must be tuned on a disjoint tuning set with an equal budget for every competitor. Tuning on the test set is the most common silent flaw in metaheuristic papers.
- **Set the computational budget.** Wall-clock time, CPU time, or evaluation count — pick one, justify it, and apply it identically to all algorithms. Decide single-run or anytime measurement (trajectory of best-so-far).
- **Control the machine.** One machine (or identical nodes), fixed thread count, no concurrent load, fixed library versions. Record CPU model, RAM, OS, Python/solver versions.
- **Choose metrics before running.** Best over seeds, mean ± std, gap to best-known, wins/ties/losses, shifted geometric mean of time, time-to-target. Adding metrics after seeing results is p-hacking.
- **Pre-register the analysis.** Which test, one- or two-sided, which α, which correction for multiple comparisons. Write it down before the runs start.
- **Decide confirmatory vs exploratory.** One pre-stated hypothesis gets a confirmatory test with family-wise error control. A screen over many variants is exploratory and must be labeled as such.
- **Plan reproducibility.** Log every (algorithm, instance, seed, parameters, code version) tuple with the result row. A result that cannot be regenerated is not a result.

## Designing the Comparison

### Protocol rules that decide validity

1. **Instance = unit, seed = replicate.** Statistical tests operate on per-instance summaries (mean or best over seeds). Pooling all (instance, seed) runs into one sample is pseudo-replication: runs on the same instance are correlated, the effective sample size is inflated, and p-values come out too small.
2. **Identical budgets, identical clocks.** Time every algorithm with the same mechanism, in the same process model. A C++ baseline vs a Python prototype on wall time answers a question about languages, not algorithms; in that case compare on evaluation counts or report both.
3. **Pair whenever possible.** All algorithms on all instances gives a paired (blocked) design. Pairing removes between-instance variance — which usually dwarfs between-algorithm variance — and multiplies statistical power.
4. **Equal tuning effort.** Tuned-vs-default comparisons are biased by construction. Give each competitor the same tuning budget on the tuning split.
5. **Validate before analyzing.** Run an independent feasibility checker on every reported solution. A "better" result that is infeasible invalidates the whole campaign.

### Metric definitions

For minimization, with reference value $z^{*}_{p}$ (optimum or best known) on instance $p$:

$$
\text{gap}_{a,p} = 100 \cdot \frac{z_{a,p} - z^{*}_{p}}{|z^{*}_{p}|}
$$

For maximization flip the sign of the numerator. If $z^{*}_{p}$ is zero or near zero, gaps explode: switch to absolute differences or shift the reference. Keep the *primal gap* (distance of your solution to the best known) distinct from the *solver optimality gap* (distance between a solver's incumbent and its dual bound) — they answer different questions.

| Metric | Definition | Use when |
|---|---|---|
| best (over seeds) | min objective across seeds per instance | what the method can achieve; sensitive to seed count |
| mean ± std | average across seeds per instance | typical behavior; the input to statistical tests |
| gap % | formula above, per run or per instance | comparing across instances of different scales |
| wins / ties / losses | per-instance score against a rival | robustness; compact paper tables |
| shifted geometric mean of time | $e^{\text{mean}(\ln(t+s))} - s$, shift $s \in [1, 10]$ s | aggregating runtimes; the MIPLIB convention (Achterberg 2007) |
| time-to-target | wall time until a target objective is first reached | randomized anytime algorithms; restart analysis |
| primal integral | gap integrated over running time (Berthold 2013) | anytime quality under a shared time limit |

Arithmetic means of runtimes are dominated by the slowest instances; arithmetic means of ratios are biased by the choice of denominator. The shifted geometric mean avoids both, which is why MIP benchmarking standardized on it.

### Choosing the statistical test

Nonparametric tests are the default in this field: gap and runtime distributions are skewed, outliers are routine, and instance counts are small, so t-test normality assumptions rarely hold (Demšar 2006, "Statistical comparisons of classifiers over multiple data sets" — the canonical reference, directly transferable to optimization benchmarks).

```text
What is being compared?
│
├─ TWO algorithms
│   ├─ Both run on every instance of one set (paired design)
│   │   ├─ ≥ 10 instances → Wilcoxon signed-rank on per-instance mean gaps
│   │   │                    + matched rank-biserial effect size
│   │   └─ < 10 instances → sign test (direction only), or get more
│   │                        instances; report all per-instance numbers
│   └─ One instance, many independent seeds (unpaired samples)
│       → Mann-Whitney U per instance + Vargha-Delaney A12;
│         never pool seeds across instances into one sample
│
├─ THREE OR MORE algorithms, all on the same instance set
│   → Friedman test on per-instance ranks (+ Iman-Davenport correction)
│       ├─ all-pairs question → Nemenyi critical-difference analysis
│       └─ one algorithm is "yours" → Holm-corrected Wilcoxon vs control
│            (uses the budget on fewer hypotheses → more power)
│
└─ Solution quality fixed or irrelevant, runtime is the metric
    → performance profiles (Dolan & Moré 2002) + shifted geometric
      means; report failures/timeouts explicitly, never drop them
```

A significant p-value says the difference is unlikely under the null; it says nothing about size. Always pair the test with an effect size (rank-biserial, A12) and with the absolute gap difference, then judge practical relevance against a threshold chosen in advance.

### Sample sizes and power realities

- An exact two-sided Wilcoxon signed-rank test cannot reach p < 0.05 with fewer than 6 nonzero differences; 15–30 instances is a comfortable working range.
- Friedman needs N ≥ 10 instances and k ≥ 3 algorithms as a practical floor; below that, exact permutation tests or more instances.
- For randomized algorithms use 10–30 seeds per (algorithm, instance). Seeds shrink the noise of the per-instance summary, but the test's power grows with the number of *instances* — with a fixed run budget, more instances beats more seeds.
- Ties (identical gaps, e.g., both algorithms reach the optimum) reduce the effective n of signed-rank tests. If most instances tie, the instance set is too easy for quality comparison — switch to time-to-target.

## The Benchmarking Pipeline

The full protocol, in order. Steps 1–2 happen before any test run; steps 3–8 are mechanical once the design is frozen.

1. Freeze claim, metrics, instance split, budget, seeds, and the statistical analysis.
2. Tune every competitor with the same budget on the tuning instances only.
3. Run the full grid — every (algorithm, instance, seed) cell — under identical limits.
4. Validate every reported solution with an independent feasibility checker.
5. Aggregate seeds into per-instance summaries; compute gaps against references.
6. Apply the pre-chosen test; record exact p-values, effect sizes, wins/ties/losses.
7. Draw performance profiles or time-to-target plots; check they agree with the test.
8. Write the reporting checklist (see Output Format) into the paper or report.

The runner below produces the tidy one-row-per-run table everything else consumes.

```python
import time
from collections.abc import Callable, Iterable
from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class RunResult:
    """One tidy row: a single (algorithm, instance, seed) run."""

    algorithm: str
    instance: str
    seed: int
    objective: float
    runtime_s: float
    time_to_best_s: float


def run_experiment(
    algorithms: dict[str, Callable[[dict, int], tuple[float, float]]],
    instances: dict[str, dict],
    seeds: Iterable[int],
) -> pd.DataFrame:
    """Run every (algorithm, instance, seed) cell of the grid.

    Each algorithm callable maps (instance_data, seed) to
    (best_objective, time_to_best_seconds). Timing happens here so every
    algorithm is measured by the same clock.
    """
    seed_list = list(seeds)
    rows: list[RunResult] = []
    for inst_name, inst_data in instances.items():
        for algo_name, algo in algorithms.items():
            for seed in seed_list:
                t0 = time.perf_counter()
                objective, time_to_best = algo(inst_data, seed)
                elapsed = time.perf_counter() - t0
                rows.append(RunResult(algo_name, inst_name, seed,
                                      objective, elapsed, time_to_best))
    return pd.DataFrame(rows)


def add_gap(df: pd.DataFrame, best_known: dict[str, float],
            minimize: bool = True) -> pd.DataFrame:
    """Add a gap_pct column vs best-known values; sign-flipped for maximization."""
    out = df.copy()
    ref = out["instance"].map(best_known)
    sign = 1.0 if minimize else -1.0
    out["gap_pct"] = sign * 100.0 * (out["objective"] - ref) / ref.abs()
    return out


def make_mock(bias: float, noise: float) -> Callable[[dict, int], tuple[float, float]]:
    """Mock solver for demonstration: optimum inflated by bias plus noise."""
    def solve(inst: dict, seed: int) -> tuple[float, float]:
        rng = np.random.default_rng(seed)
        return inst["opt"] * (1.0 + bias + noise * rng.random()), 0.05
    return solve


instances = {"i1": {"opt": 100.0}, "i2": {"opt": 250.0}}
algos = {"A": make_mock(0.02, 0.01), "B": make_mock(0.05, 0.03)}
runs = add_gap(run_experiment(algos, instances, seeds=range(5)),
               {"i1": 100.0, "i2": 250.0})
print(runs.shape, runs.groupby("algorithm")["gap_pct"].mean().round(2).to_dict())
# Expected: (20, 7) and mean gaps {'A': 2.49, 'B': 6.46} — 2 algorithms x
# 2 instances x 5 seeds, one tidy row per run, gap computed vs the optimum.
```

Aggregation is two-stage by design: seeds collapse into per-instance summaries first, instances aggregate second. Pooling everything in one step lets instances with many seeds or large scales dominate the averages.

```python
import numpy as np
import pandas as pd


def shifted_geometric_mean(values: np.ndarray, shift: float = 1.0) -> float:
    """Shifted geometric mean — the MIPLIB convention for aggregating runtimes."""
    v = np.asarray(values, dtype=float)
    return float(np.exp(np.log(v + shift).mean()) - shift)


def summary_table(runs: pd.DataFrame) -> pd.DataFrame:
    """Aggregate a tidy run table into the per-algorithm summary for a paper."""
    per_inst = runs.groupby(["algorithm", "instance"]).agg(
        best_gap=("gap_pct", "min"),
        mean_gap=("gap_pct", "mean"),
        mean_time=("runtime_s", "mean"),
    ).reset_index()
    winners = per_inst.loc[
        per_inst.groupby("instance")["mean_gap"].idxmin(), "algorithm"
    ].value_counts()
    out = per_inst.groupby("algorithm").agg(
        mean_gap=("mean_gap", "mean"),
        best_gap=("best_gap", "mean"),
    )
    out["wins"] = winners.reindex(out.index).fillna(0).astype(int)
    out["sgm_time_s"] = [
        shifted_geometric_mean(runs.loc[runs["algorithm"] == a, "runtime_s"].to_numpy())
        for a in out.index
    ]
    return out.round(2)


runs = pd.DataFrame({
    "algorithm": ["A"] * 4 + ["B"] * 4,
    "instance": ["i1", "i1", "i2", "i2"] * 2,
    "seed": [0, 1, 0, 1] * 2,
    "gap_pct": [1.0, 1.2, 2.0, 2.2, 0.8, 1.2, 2.5, 2.9],
    "runtime_s": [10.0, 11.0, 40.0, 42.0, 9.0, 9.5, 55.0, 60.0],
})
print(summary_table(runs))
# Expected: A — mean_gap 1.60, wins 1 (on i2), sgm_time 20.96;
#           B — mean_gap 1.85, wins 1 (on i1), sgm_time 23.47. Each algorithm
#           wins one instance: a mean-only table would hide the split decision.
```

## Worked Example 1: Two Algorithms, Paired over an Instance Set

The standard situation: a new method (here ALNS) against one baseline (a GA), both run on every instance with multiple seeds. The complete script — aggregation, test, two effect sizes, verdict — follows the protocol exactly.

```python
"""Two-algorithm paired comparison: Wilcoxon signed-rank, effect sizes, verdict.

Protocol: the instance is the experimental unit. Collapse seeds into one
summary per (algorithm, instance) first, then test the paired per-instance
differences. Testing on the raw (instance, seed) pool is pseudo-replication:
runs on the same instance are correlated and the p-value comes out too small.
"""
import numpy as np
import pandas as pd
from scipy import stats


def matched_rank_biserial(diff: np.ndarray) -> float:
    """Matched-pairs rank-biserial correlation (Kerby 2014), in [-1, 1].

    With diff = gap_A - gap_B on a minimization problem: -1.0 means every
    nonzero difference favors A, +1.0 means every one favors B, 0.0 balance.
    """
    d = np.asarray(diff, dtype=float)
    d = d[d != 0.0]
    ranks = stats.rankdata(np.abs(d))
    return float((ranks[d > 0].sum() - ranks[d < 0].sum()) / ranks.sum())


def vargha_delaney_a12(x: np.ndarray, y: np.ndarray) -> float:
    """A12 = P(X > Y) + 0.5 P(X = Y) over all pairs (Vargha & Delaney 2000)."""
    diff = np.asarray(x, dtype=float)[:, None] - np.asarray(y, dtype=float)[None, :]
    return float(((diff > 0).sum() + 0.5 * (diff == 0).sum()) / diff.size)


def mean_per_instance_a12(df: pd.DataFrame, algo_a: str, algo_b: str) -> float:
    """Average per-instance A12 over seed distributions; never pool seeds."""
    values = [
        vargha_delaney_a12(
            g.loc[g["algorithm"] == algo_a, "gap_pct"].to_numpy(),
            g.loc[g["algorithm"] == algo_b, "gap_pct"].to_numpy(),
        )
        for _, g in df.groupby("instance")
    ]
    return float(np.mean(values))


def compare_paired(df: pd.DataFrame, algo_a: str, algo_b: str,
                   alpha: float = 0.05) -> dict[str, object]:
    """Full paired comparison on mean per-instance gaps (minimization)."""
    per_inst = (
        df[df["algorithm"].isin([algo_a, algo_b])]
        .groupby(["instance", "algorithm"])["gap_pct"].mean()
        .unstack("algorithm")
    )
    a = per_inst[algo_a].to_numpy()
    b = per_inst[algo_b].to_numpy()
    d = a - b
    if np.count_nonzero(d) < 6:
        return {"verdict": "inconclusive — fewer than 6 nonzero differences; "
                           "an exact two-sided Wilcoxon cannot reach p < 0.05"}
    _, p = stats.wilcoxon(a, b, zero_method="pratt", alternative="two-sided")
    rb = matched_rank_biserial(d)
    if p >= alpha:
        verdict = "no significant difference"
    else:
        verdict = f"{algo_a} better" if rb < 0.0 else f"{algo_b} better"
    return {
        "n_instances": int(d.size),
        "wins": {algo_a: int((d < 0).sum()), algo_b: int((d > 0).sum()),
                 "ties": int((d == 0).sum())},
        "mean_gap": {algo_a: round(float(a.mean()), 3),
                     algo_b: round(float(b.mean()), 3)},
        "wilcoxon_p": float(p),
        "rank_biserial": round(rb, 3),
        "verdict": verdict,
    }


rng = np.random.default_rng(42)
rows: list[tuple[str, str, int, float]] = []
for i in range(15):
    base = rng.uniform(1.0, 4.0)
    for seed in range(10):
        rows.append(("ALNS", f"inst{i:02d}", seed, base + rng.normal(0.0, 0.3)))
        rows.append(("GA", f"inst{i:02d}", seed, base + 0.8 + rng.normal(0.0, 0.5)))
df = pd.DataFrame(rows, columns=["algorithm", "instance", "seed", "gap_pct"])

print(compare_paired(df, "ALNS", "GA"))
print(f"mean per-instance A12 = {mean_per_instance_a12(df, 'ALNS', 'GA'):.2f}")
# Expected: ALNS wins all 15 instances, wilcoxon_p = 6.1e-05 (the smallest
# two-sided value n = 15 allows), rank_biserial = -1.0, verdict 'ALNS better',
# and A12 = 0.08 — far from 0.5, a large effect on the Vargha-Delaney scale
# (large when A12 <= 0.29 or >= 0.71).
```

What goes in the paper: the exact p-value (not "p < 0.05"), the effect size with its interpretation, the wins/ties/losses count, and the mean gaps. The two effect sizes answer different questions — rank-biserial measures consistency of the per-instance direction; A12 measures how often a random run of one algorithm beats a random run of the other on the same instance (Arcuri & Briand 2011 recommend A12 as the default in randomized-algorithm assessment).

## Worked Example 2: Five Algorithms with Friedman and Post-Hoc

For k ≥ 3 algorithms over N instances, running all pairwise Wilcoxon tests at α = 0.05 inflates the family-wise error rate. The Demšar (2006) procedure: Friedman test on per-instance ranks first; only if it rejects, proceed to post-hoc comparisons with correction. The Friedman statistic on average ranks $R_j$ is

$$
\chi^2_F = \frac{12N}{k(k+1)} \left[ \sum_{j=1}^{k} R_j^2 - \frac{k(k+1)^2}{4} \right],
$$

with the Iman–Davenport transform $F_F = \frac{(N-1)\chi^2_F}{N(k-1) - \chi^2_F}$ being less conservative. Two algorithms differ in the Nemenyi sense when their average ranks differ by at least the critical difference

$$
CD = q_{\alpha} \sqrt{\frac{k(k+1)}{6N}} .
$$

```python
"""k-algorithm comparison: Friedman + Iman-Davenport, Nemenyi CD, Holm vs control.

Input is the per-instance gap matrix (rows = instances, columns = algorithms),
i.e., seeds are already collapsed to per-instance means. Follows Demsar (2006).
"""
import numpy as np
import pandas as pd
from scipy import stats

# Studentized-range-based q values for the Nemenyi test, alpha = 0.05
# (Demsar 2006, Table 5), indexed by the number of algorithms k.
Q_ALPHA_05 = {2: 1.960, 3: 2.343, 4: 2.569, 5: 2.728,
              6: 2.850, 7: 2.949, 8: 3.031, 9: 3.102, 10: 3.164}


def friedman_report(gap_matrix: pd.DataFrame) -> dict[str, object]:
    """Friedman test with Iman-Davenport correction and Nemenyi CD at 0.05."""
    n, k = gap_matrix.shape
    ranks = gap_matrix.rank(axis=1, method="average")   # rank 1 = lowest gap
    chi2, p_chi2 = stats.friedmanchisquare(
        *(gap_matrix[c].to_numpy() for c in gap_matrix.columns))
    ff = (n - 1) * chi2 / (n * (k - 1) - chi2)
    p_id = float(stats.f.sf(ff, k - 1, (k - 1) * (n - 1)))
    cd = Q_ALPHA_05[k] * float(np.sqrt(k * (k + 1) / (6.0 * n)))
    return {
        "avg_ranks": ranks.mean(axis=0).sort_values(),
        "chi2": float(chi2), "p_chi2": float(p_chi2),
        "iman_davenport_F": float(ff), "p_iman_davenport": p_id,
        "critical_difference": cd,
    }


def holm_vs_control(gap_matrix: pd.DataFrame, control: str,
                    alpha: float = 0.05) -> pd.DataFrame:
    """Holm-corrected Wilcoxon signed-rank tests of every algorithm vs a control.

    More powerful than Nemenyi when one algorithm plays the role of control
    (Demsar 2006, Section 3.2.2): the alpha budget is spent on k-1 hypotheses
    instead of k(k-1)/2.
    """
    others = [c for c in gap_matrix.columns if c != control]
    raw: list[tuple[str, float]] = []
    for name in others:
        _, p = stats.wilcoxon(gap_matrix[control].to_numpy(),
                              gap_matrix[name].to_numpy(), zero_method="pratt")
        raw.append((name, float(p)))
    raw.sort(key=lambda item: item[1])
    rows: list[dict[str, object]] = []
    alive = True                       # Holm rejects sequentially, then stops
    for i, (name, p) in enumerate(raw):
        threshold = alpha / (len(raw) - i)
        alive = alive and p <= threshold
        rows.append({"vs_control": name, "p_raw": p,
                     "holm_threshold": round(threshold, 4), "significant": alive})
    return pd.DataFrame(rows)


rng = np.random.default_rng(7)
n_inst = 20
base = rng.uniform(1.0, 5.0, size=n_inst)
gaps = pd.DataFrame({
    "TS": base + rng.normal(0.0, 0.3, n_inst),
    "ALNS": base + 0.1 + rng.normal(0.0, 0.3, n_inst),
    "SA": base + 0.9 + rng.normal(0.0, 0.4, n_inst),
    "GRASP": base + 1.0 + rng.normal(0.0, 0.4, n_inst),
    "GA": base + 1.4 + rng.normal(0.0, 0.5, n_inst),
}, index=[f"inst{i:02d}" for i in range(n_inst)])

report = friedman_report(gaps)
print(report["avg_ranks"].round(2).to_dict())
print(f"Iman-Davenport p = {report['p_iman_davenport']:.2e}, "
      f"CD = {report['critical_difference']:.3f}")
print(holm_vs_control(gaps, control="TS"))
# Expected: average ranks TS 1.25, ALNS 1.85, SA 3.50, GRASP 3.70, GA 4.70;
# Iman-Davenport p = 6.5e-26 and CD = 1.364, so the Nemenyi analysis cannot
# separate TS from ALNS (rank difference 0.6 < CD) while both beat the rest.
# Holm vs TS rejects all four — including ALNS (p = 0.0064): the focused
# vs-control procedure has more power than the all-pairs CD, exactly as
# Demsar (2006) argues.
```

Read the result as a partial order, not a ranking: "TS and ALNS are statistically indistinguishable; both outperform the other three." Reporting "TS is the best because its average rank is lowest" overstates what the data supports. For all-pairs significance matrices, `scikit-posthocs` provides `posthoc_nemenyi_friedman` and `posthoc_conover_friedman` as one-liners on the same gap matrix.

## Performance Profiles and Time-to-Target Plots

### Performance profiles (Dolan & Moré 2002)

Profiles compare solvers on runtime (or any cost where lower is better) across a problem set while keeping failures visible. With $t_{p,s}$ the cost of solver $s$ on problem $p$:

$$
r_{p,s} = \frac{t_{p,s}}{\min_{s'} t_{p,s'}}, \qquad
\rho_s(\tau) = \frac{1}{|P|}\,\bigl|\{\, p : r_{p,s} \le \tau \,\}\bigr| .
$$

$\rho_s(1)$ is the fraction of problems where $s$ is (tied-)fastest; the height of the right tail is the fraction it solves at all. One plot answers both "who is fastest" and "who is most robust".

```python
"""Dolan-More performance profiles with explicit failure handling."""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def performance_profiles(metric: pd.DataFrame,
                         n_grid: int = 200) -> tuple[np.ndarray, dict[str, np.ndarray]]:
    """Compute profiles from a problems x solvers cost matrix (lower = better).

    Encode failed runs (timeout, crash, infeasible answer) as np.inf. Assumes
    at least one solver succeeds on every problem. Returns the tau grid and
    one rho_s curve per solver.
    """
    m = metric.to_numpy(dtype=float)
    ratios = m / m.min(axis=1, keepdims=True)
    finite = ratios[np.isfinite(ratios)]
    taus = np.logspace(0.0, np.log10(float(finite.max()) * 1.05), n_grid)
    profiles = {
        solver: (ratios[:, j][:, None] <= taus[None, :]).mean(axis=0)
        for j, solver in enumerate(metric.columns)
    }
    return taus, profiles


def plot_profiles(taus: np.ndarray, profiles: dict[str, np.ndarray],
                  path: str) -> None:
    """Save a publication-style performance-profile figure."""
    fig, ax = plt.subplots(figsize=(4.5, 3.2))
    for solver, rho in profiles.items():
        ax.step(taus, rho, where="post", label=solver)
    ax.set_xscale("log")
    ax.set_xlabel(r"performance ratio $\tau$")
    ax.set_ylabel(r"$\rho_s(\tau)$")
    ax.set_ylim(0.0, 1.02)
    ax.legend(frameon=False, loc="lower right")
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


rng = np.random.default_rng(11)
n = 40
t_a = rng.lognormal(mean=2.0, sigma=0.4, size=n)        # steady solver
t_b = rng.lognormal(mean=1.3, sigma=1.0, size=n)        # fast but erratic
t_b[rng.random(n) < 0.10] = np.inf                      # ~10% failures for B
times = pd.DataFrame({"A": t_a, "B": t_b})
taus, profiles = performance_profiles(times)
plot_profiles(taus, profiles, "perf_profile.png")
print({s: round(float(rho[0]), 2) for s, rho in profiles.items()})
# Expected: rho at tau=1 is {'A': 0.38, 'B': 0.62} — B is fastest on more
# problems, but its curve plateaus below 1.0 because of failures while A's
# reaches 1.0: the classic speed-vs-robustness picture one mean would hide.
```

Caveat: profiles are *relative to the best solver in the compared set*. Adding or removing one solver changes every other curve, so do not read pairwise dominance between two non-best solvers from a multi-solver profile (Gould & Scott 2016 document the misinterpretations). For pairwise claims, draw the two-solver profile or use the paired tests above.

### Time-to-target plots (Aiex, Resende & Ribeiro 2007)

TTT plots characterize a *randomized* algorithm on *one* instance: fix a target objective (e.g., the best-known value, or 1% above it), run the algorithm 100+ times with independent seeds until the target is first reached, and plot the empirical CDF of those times. Crossing curves reveal which algorithm wins at small vs large budgets. If the times fit a shifted exponential — which Aiex et al. show is typical for GRASP-like multistart methods — the distribution is memoryless beyond the shift and restarts at a well-chosen cutoff provably help.

```python
"""Time-to-target (TTT) plots: empirical runtime distributions to a fixed target."""
import matplotlib.pyplot as plt
import numpy as np


def ttt_points(times: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Empirical CDF points: sorted times vs plotting positions (i - 0.5)/n."""
    t = np.sort(np.asarray(times, dtype=float))
    p = (np.arange(1, t.size + 1) - 0.5) / t.size
    return t, p


def shifted_exponential_fit(times: np.ndarray) -> tuple[float, float]:
    """Fit (location mu, scale lam) of a shifted exponential to run times."""
    t = np.sort(np.asarray(times, dtype=float))
    mu = float(t[0])
    return mu, float(t.mean() - mu)


def plot_ttt(samples: dict[str, np.ndarray], path: str) -> None:
    """Overlay TTT curves for several algorithms on one instance and target."""
    fig, ax = plt.subplots(figsize=(4.5, 3.2))
    for name, times in samples.items():
        t, p = ttt_points(times)
        ax.plot(t, p, drawstyle="steps-post", label=name)
    ax.set_xlabel("time to target (s)")
    ax.set_ylabel("cumulative probability")
    ax.set_ylim(0.0, 1.02)
    ax.legend(frameon=False, loc="lower right")
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


rng = np.random.default_rng(5)
samples = {
    "ILS": rng.exponential(scale=8.0, size=100) + 1.0,
    "SA": rng.exponential(scale=20.0, size=100) + 0.5,
}
plot_ttt(samples, "ttt.png")
p_ils_first = float(np.mean(samples["ILS"][:, None] < samples["SA"][None, :]))
print(round(p_ils_first, 2), [round(v, 1) for v in shifted_exponential_fit(samples["ILS"])])
# Expected: 0.68 — the probability that a random ILS run reaches the target
# before a random SA run — and a fit of (1.0, 8.0): location ~1 s, scale ~8 s,
# so restarting ILS after a fixed cutoff loses little expected time.
```

The printed probability is exactly the unpaired effect size A12 applied to runtimes, which makes TTT data and the statistical machinery above fully compatible: Mann–Whitney U on the two time samples tests the same comparison the plot shows.

## Advanced Techniques

### Multiple-comparison control beyond Holm

Nemenyi is simple but conservative for all-pairs analysis. Bergmann–Hommel exploits logical relations among the hypotheses and is the most powerful classical choice after Friedman (García & Herrera 2008, "An extension on statistical comparisons of classifiers over multiple data sets"); `scikit-posthocs` implements it. Distinguish goals: confirmatory claims in a paper need family-wise error control (Holm, Bergmann–Hommel); exploratory screens over many algorithm variants are better served by false-discovery-rate control (Benjamini–Hochberg via `statsmodels.stats.multitest.multipletests`), with the survivors re-tested confirmatorily on fresh instances.

### Bootstrap confidence intervals for aggregate metrics

Mean gaps are right-skewed, so normal-theory intervals misstate the uncertainty. The percentile bootstrap needs no distributional assumption and works for any statistic — mean gap, shifted geometric mean, win rate.

```python
import numpy as np


def bootstrap_ci_mean(values: np.ndarray, n_boot: int = 10_000,
                      level: float = 0.95, seed: int = 0) -> tuple[float, float]:
    """Percentile bootstrap CI for the mean of a per-instance metric."""
    rng = np.random.default_rng(seed)
    v = np.asarray(values, dtype=float)
    idx = rng.integers(0, v.size, size=(n_boot, v.size))
    means = v[idx].mean(axis=1)
    lo, hi = np.quantile(means, [(1.0 - level) / 2.0, 1.0 - (1.0 - level) / 2.0])
    return float(lo), float(hi)


rng = np.random.default_rng(3)
gaps = rng.gamma(shape=2.0, scale=0.8, size=25)     # skewed, like real gap data
print(round(float(gaps.mean()), 2), tuple(round(x, 2) for x in bootstrap_ci_mean(gaps)))
# Expected: sample mean 1.64 with interval (1.23, 2.10) — asymmetric around
# the mean because gap distributions have a heavy right tail.
```

Resample *instances* (the experimental unit), never individual seed-level runs, or the interval inherits the pseudo-replication bias.

### Bayesian comparison and practical equivalence

Frequentist tests cannot conclude "the algorithms are equivalent" — only "no significant difference", which may just mean low power. The Bayesian signed-rank test of Benavoli, Corani, Demšar & Zaffalon (2017, "Time for a change: a tutorial for comparing multiple classifiers through Bayesian analysis") returns three probabilities: P(A better), P(B better), and P(practically equivalent) given a region of practical equivalence (ROPE) such as |Δgap| < 0.1%. This turns an inconclusive p = 0.21 into a usable statement like "equivalent with probability 0.91". The `baycomp` package implements it directly on the paired per-instance vectors.

### Data profiles and the primal integral

When the budget is function evaluations rather than time — surrogate-assisted search, expensive simulators — use data profiles (Moré & Wild 2009): the fraction of problems brought within accuracy τ of the best achievable value, as a function of the evaluation budget in multiples of n+1. Unlike performance profiles, the x-axis is an absolute budget, so the curve says what a user with that budget gets. For anytime heuristics under a shared time limit, the primal integral (Berthold 2013) integrates the primal gap over the run and rewards finding good solutions early; report it alongside the final gap when convergence speed is part of the claim.

### Racing to prune large campaigns

When screening dozens of variants, do not run the full grid. F-Race (Birattari, Stützle, Paquete & Varrentrapp 2002) evaluates all candidates instance by instance, applies the Friedman test after each block, and drops candidates that are already significantly worse than the leader; the saved budget goes to the survivors. `irace` packages this with sampling of the configuration space. Race for screening and tuning, then confirm the finalists with the full pre-registered protocol on the untouched test instances.

## Practical Challenges

**The new algorithm wins on average but the test says nothing.** A few instances with huge gaps inflate one mean. The paired test works on per-instance directions, which is the more honest summary. Report wins/ties/losses and the median gap difference next to the mean; if the method only wins on one instance family, say so — that is a finding, not a failure.

**p < 0.001 but the improvement is 0.02% gap.** Large instance counts make trivial differences significant. Statistical significance is necessary, not sufficient. Define the minimal practically relevant difference before the experiment (e.g., 0.5% gap or 20% time) and judge effect sizes against it; consider the ROPE-based Bayesian analysis to quantify equivalence.

**Rankings flip when the time limit changes.** Anytime behavior differs: greedy-start heuristics win short budgets, population methods win long ones. Report at least two budgets, or the full convergence trajectory with the primal integral, and state the budget in the claim itself ("better within 60 s").

**Baseline numbers copied from a paper.** Different machine, language, instance files, and stopping rules make the comparison unsound. Rerun baselines locally whenever code exists. If rerunning is impossible, label the comparison as indicative, compare on machine-independent measures (evaluations, gap at convergence), and never run statistical tests on numbers you did not generate.

**Your method is tuned, the baselines run on defaults.** This bias is invisible in the results table and reviewers ask about it. Give every competitor the same tuning budget on the same tuning instances and report that budget. If a baseline's authors published tuned settings, use them as that algorithm's starting point.

**Most instances tie at the optimum.** Zero differences carry no information for the signed-rank test (with `zero_method="pratt"` they at least deflate the statistic honestly). The instance set is too easy: move to larger instances, or change the question from quality to speed and use time-to-target plots.

**Seeds treated as independent samples.** Thirty seeds on ten instances is n = 10, not n = 300. Collapse seeds into per-instance summaries before testing. If per-seed resolution matters (robustness claims), analyze per-instance A12 values or report the std over seeds per instance.

**The grid is too expensive to finish.** A full (algorithm, instance, seed) grid with generous budgets can take CPU-months. Cut scope in this order: fewer algorithm variants (race them first), then fewer seeds, then shorter budgets — never cut instances below the testing floor. Cache every completed run so a crashed campaign resumes instead of restarting.

## Tools & Libraries

| Library | When to use | Note |
|---|---|---|
| scipy.stats | Wilcoxon, Mann–Whitney U, Friedman, rankdata | exact small-sample methods built in; the default choice |
| scikit-posthocs | Nemenyi, Conover, Bergmann–Hommel after Friedman | one call returns the full pairwise p-value matrix |
| statsmodels | `multipletests` for Holm / Benjamini–Hochberg | apply to any list of raw p-values |
| numpy | effect sizes, bootstrap, profiles, TTT curves | `np.random.default_rng(seed)` for reproducible resampling |
| pandas | tidy run tables, gap matrices, rank tables | one row per run; pivot to instances × algorithms for tests |
| matplotlib | performance profiles, TTT, convergence bands | vector output (PDF/SVG) for papers |
| baycomp | Bayesian signed-rank with ROPE | probability-of-win and equivalence statements |
| irace / Optuna | tuning and racing before the comparison | keep tuning and test instances strictly disjoint |

## Output Format

A complete benchmarking deliverable contains five parts.

1. **Protocol declaration** — stated before any numbers:

```text
Claim:        ALNS < TS on mean gap, 60 s/run, instances with 100-500 customers
Instances:    32 test (R1xx + C1xx Solomon-derived), 12 tuning, disjoint
Runs:         3 algorithms x 32 instances x 20 seeds, 60 s wall clock each
Machine:      1x AMD EPYC 7543, 1 thread/run, Python 3.11, numpy 1.26
Tuning:       irace, 2,000 runs budget per algorithm, tuning instances only
Analysis:     Wilcoxon signed-rank (two-sided, alpha 0.05) on per-instance
              mean gaps; matched rank-biserial + mean per-instance A12;
              Friedman + Holm vs ALNS for the 3-way table
References:   best-known values from the maintained benchmark page, frozen
              at experiment start; all reported solutions revalidated
```

2. **Summary table** — per algorithm: mean gap, best gap, wins/ties/losses, shifted geometric mean time, all aggregated instance-first.

| Algorithm | mean gap % | best gap % | W/T/L | sgm time (s) |
|---|---|---|---|---|
| ALNS | 0.84 | 0.31 | 21/6/5 | 41.2 |
| TS | 1.27 | 0.55 | 5/6/21 | 38.9 |

3. **Statistical verdict** — exact p-value, effect size with interpretation, and the one-sentence conclusion matched to the original claim ("ALNS achieves lower mean gaps than TS; p = 3.1e-4, rank-biserial = -0.71, a large and consistent per-instance effect").

4. **Figures** — a performance profile or TTT plot, plus a convergence plot with bands over seeds where anytime behavior matters; every figure referenced in the text.

5. **Reproducibility appendix** — checklist, all items required:

- [ ] hardware, OS, language and library versions recorded
- [ ] time limit, thread count, and memory limit per run stated
- [ ] instance set named and obtainable; generator seeds published if synthetic
- [ ] all seeds and the full tidy run table archived alongside the code version
- [ ] tuning protocol and budget reported for every algorithm
- [ ] metric formulas stated (gap reference values frozen and cited)
- [ ] exact p-values and effect sizes, not significance stars alone
- [ ] failures/timeouts counted and included, not silently dropped

## Questions to Ask

- What is the exact claim — better quality at equal time, equal quality faster, or more robust across instances?
- How many instances are available, and can tuning and test sets be disjoint?
- How many seeds per (algorithm, instance) cell does the compute budget allow?
- Are all competitors run locally on one machine, or are some numbers quoted from papers?
- Has every competitor received the same tuning effort?
- Is this confirmatory (one pre-stated hypothesis) or exploratory (screening many variants)?
- Minimization or maximization, and is a trustworthy best-known value available per instance?
- Is the budget wall-clock time, CPU time, or evaluation count — and is parallelism fixed?
- Does the target venue expect specific tests, profiles, or table formats?

## Related Skills

- **instance-generation-and-benchmarks** — when the test bed itself is the question: standard benchmark sets, parsers, and synthetic generators with controlled hardness and proper train/test splits.
- **pandas-experiment-management** — when building the tidy one-row-per-run tables, run metadata, and aggregation pipelines that feed every test in this skill.
- **optuna-hyperparameter-tuning** — when competitors must be tuned fairly with equal budgets on a separate tuning instance set before any comparison.
- **matplotlib-optimization-visualization** — when performance profiles, convergence bands, and other figures need publication-quality styling and export.
- **nature-inspired-metaheuristics-overview** — when a "novel" metaphor-based method must be benchmarked against established baselines before any novelty claim.
