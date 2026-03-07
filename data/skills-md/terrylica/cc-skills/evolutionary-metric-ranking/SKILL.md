---
name: evolutionary-metric-ranking
description: Multi-objective evolutionary optimization for per-metric percentile cutoffs and intersection-based config selection. TRIGGERS - ranking optimization, cutoff search, metric intersection, Optuna cutoffs, evolutionary search, percentile ranking, multi-objective ranking, config selection, survivor analysis, binding metrics, Pareto frontier cutoffs.
allowed-tools: Read, Grep, Glob, Bash
---

# Evolutionary Metric Ranking

Methodology for systematically zooming into high-quality configurations across multiple evaluation metrics using per-metric percentile cutoffs, intersection-based filtering, and evolutionary optimization. Domain-agnostic principles with quantitative trading case studies.

**Companion skills**: `rangebar-eval-metrics` (metric definitions) | `adaptive-wfo-epoch` (WFO integration) | `backtesting-py-oracle` (SQL validation)

---

## When to Use This Skill

Use this skill when:

- Ranking and filtering configs/strategies/models across multiple quality metrics
- Searching for optimal per-metric thresholds that select the best subset
- Identifying which metrics are binding constraints vs inert dimensions
- Running multi-objective optimization (Optuna TPE / NSGA-II) over filter parameters
- Performing forensic analysis on optimization results (universal champions, feature themes)
- Designing a metric registry for pluggable evaluation systems

---

## Core Principles

### P1 - Percentile Ranks, Not Raw Values

Raw metric values live on incompatible scales (Kelly in [-1,1], trade count in [50, 5000], Omega in [0.8, 2.0]). Percentile ranking normalizes every metric to [0, 100], making cross-metric comparison meaningful.

```
Rule: scipy.stats.rankdata(method='average') scaled to [0, 100]
      None/NaN/Inf -> percentile 0 (worst)
      "Lower is better" metrics -> negate before ranking (100 = best)
```

**Why average ties**: Tied values receive the mean of the ranks they would span. This prevents artificial discrimination between genuinely identical values.

### P2 - Independent Per-Metric Cutoffs

Each metric gets its own independently-tunable cutoff. `cutoff=20` means "only configs in the top 20% survive this filter." This creates a 12-dimensional (or N-dimensional) search space where each axis controls one quality dimension.

```
cutoff=100 -> no filter (everything passes)
cutoff=50  -> top 50% survives
cutoff=10  -> top 10% survives (stringent)
cutoff=0   -> nothing passes
```

**Why independent, not uniform**: Different metrics have different discrimination power. Uniform tightening (all metrics at the same cutoff) wastes filtering budget on inert dimensions while under-filtering on binding constraints.

### P3 - Intersection = Multi-Metric Excellence

A config survives the final filter only if it passes **ALL** per-metric cutoffs simultaneously. This intersection logic ensures no single-metric champion sneaks through with terrible performance elsewhere.

```
survivors = metric_1_pass AND metric_2_pass AND ... AND metric_N_pass
```

**Why intersection, not scoring**: Weighted-sum scoring hides metric failures. A config with 99th percentile Sharpe but 1st percentile regularity would score well in a weighted sum but is clearly deficient. Intersection enforces minimum quality across every dimension.

### P4 - Start Wide Open, Tighten Evolutionarily

All cutoffs default to 100% (no filter). The optimizer progressively tightens cutoffs to find the combination that best satisfies the chosen objective. This is the opposite of starting strict and relaxing.

```
Initial state:  All cutoffs = 100 (1008 configs survive)
After search:   Each cutoff independently tuned (11 configs survive)
```

**Why start wide**: Starting strict risks missing the global optimum by immediately excluding configs that would survive under a different cutoff combination. Wide-to-narrow exploration is characteristic of global optimization.

### P5 - Multiple Objectives Reveal Different Truths

No single objective function captures "quality." Run multiple objectives and compare survivor sets. Configs that survive **all** objectives are the most robust.

| Objective                | Asks                                  | Reveals                                       |
| ------------------------ | ------------------------------------- | --------------------------------------------- |
| max_survivors_min_cutoff | Most configs at tightest cutoffs?     | Efficient frontier of quantity vs stringency  |
| quality_at_target_n      | Best quality in top N?                | Optimal cutoffs for a target portfolio size   |
| tightest_nonempty        | Absolute tightest with >= 1 survivor? | Universal champion (sole survivor)            |
| pareto_efficiency        | Survivors vs tightness trade-off?     | Full Pareto front (NSGA-II)                   |
| diversity_reward         | Are cutoffs non-redundant?            | Which metrics provide independent information |

**Cross-objective consistency**: A config that appears in ALL objective survivor sets is the most defensible selection. One that appears in only one is likely an artifact of that objective's bias.

### P6 - Binding Metrics Identification

After optimization, identify **binding metrics** - those that would increase the intersection if relaxed to 100%. Non-binding metrics are either already loose or perfectly correlated with a binding metric.

```
For each metric with cutoff < 100:
    Relax this metric to 100, keep others fixed
    If intersection grows: this metric IS binding
    If intersection unchanged: this metric is redundant at current cutoffs
```

**Why this matters**: Binding metrics are the actual constraints on your quality frontier. Effort to improve configs should focus on binding dimensions.

### P7 - Inert Dimension Detection

A metric is **inert** if it provides zero discrimination across the population. Detect this before optimization to reduce dimensionality.

```
If max(metric) == min(metric) across all configs: INERT
If percentile spread < 5 points: NEAR-INERT
```

**Action**: Remove inert metrics from the search space or permanently set their cutoff to 100. Including them wastes optimization budget.

### P8 - Forensic Post-Analysis

After optimization, perform forensic analysis to extract actionable insights:

1. **Universal champions** - configs surviving ALL objectives
2. **Feature frequency** - which features appear most in survivors
3. **Metric binding sequence** - order in which metrics become binding as cutoffs tighten
4. **Tightening curve** - intersection size vs uniform cutoff (100% -> 5%)
5. **Metric discrimination power** - which metric kills the most configs at each tightening step

---

## Architecture Pattern

```
Metric JSONL files (pre-computed)
        |
        v
MetricSpec Registry  <-- Defines name, direction, source, cutoff var
        |
        v
Percentile Ranker    <-- scipy.stats.rankdata, None->0, flip lower-is-better
        |
        v
Per-Metric Cutoff    <-- Each metric independently filtered
        |
        v
Intersection         <-- Configs passing ALL cutoffs
        |
        v
Evolutionary Search  <-- Optuna TPE/NSGA-II tunes cutoffs
        |
        v
Forensic Analysis    <-- Cross-objective consistency, binding metrics
```

### MetricSpec Registry

The registry is the single source of truth for metric definitions. Each entry is a frozen dataclass:

```python
@dataclass(frozen=True)
class MetricSpec:
    name: str              # Internal key (e.g., "tamrs")
    label: str             # Display label (e.g., "TAMRS")
    higher_is_better: bool # Direction for percentile ranking
    default_cutoff: int    # Default percentile cutoff (100 = no filter)
    source_file: str       # JSONL filename containing raw values
    source_field: str      # Field name in JSONL records
```

**Design principle**: Adding a new metric = adding one MetricSpec entry. No other code changes required. The ranking, cutoff, intersection, and optimization machinery is fully generic.

### Env Var Convention

Each metric's cutoff is controlled by a namespaced environment variable:

```
RBP_RANK_CUT_{METRIC_NAME_UPPER} = integer [0, 100]
```

This enables:

- Shell-level override without code changes
- Copy-paste of optimizer output directly into next run
- CI/CD integration via environment configuration
- Mise task integration via `[env]` blocks

---

## Evolutionary Optimizer Design

### Sampler Selection

| Scenario             | Sampler                     | Why                                                              |
| -------------------- | --------------------------- | ---------------------------------------------------------------- |
| Single-objective     | TPE (Tree-Parzen Estimator) | Bayesian, handles integer/categorical, good for 10-20 dimensions |
| Multi-objective (2+) | NSGA-II                     | Pareto-frontier discovery, population-based                      |

**Determinism**: Always seed the sampler (`seed=42`). Optimization results must be reproducible.

### Search Space Design

```python
def suggest_cutoffs(trial):
    cutoffs = {}
    for spec in metric_registry:
        cutoffs[spec.name] = trial.suggest_int(spec.name, 5, 100, step=5)
    return cutoffs
```

**Why step=5**: Reduces the search space by 20x (20 values per metric vs 100) while maintaining sufficient granularity. For 12 metrics, this is 20^12 = 4 x 10^15 vs 100^12 = 10^24.

**Why lower bound = 5**: cutoff=0 always produces empty intersection. Values below 5 are too stringent to be useful in practice.

### Data Pre-Loading (Critical Performance Pattern)

```python
# Load metric data ONCE, share across all trials
metric_data = load_metric_data(results_dir, metric_registry)

def objective(trial):
    cutoffs = suggest_cutoffs(trial)
    # Pass pre-loaded data - avoids disk I/O per trial
    result = run_ranking_with_cutoffs(cutoffs, metric_data=metric_data)
    return obj_fn(result, cutoffs)
```

**Why**: Each trial evaluates in ~6ms when data is pre-loaded (pure NumPy/set operations). Without pre-loading, each trial incurs ~50ms of disk I/O. At 10,000 trials, this is 60 seconds vs 500 seconds.

### Objective Function Patterns

#### Pattern 1 - Ratio Optimization

```python
def obj_max_survivors_min_cutoff(result, cutoffs):
    n = result["n_intersection"]
    if n == 0:
        return 0.0
    mean_cutoff = sum(cutoffs.values()) / len(cutoffs)
    return n / mean_cutoff  # More survivors per unit of looseness
```

**Use when**: Exploring the efficiency frontier - how much quality can you get for how much filtering?

#### Pattern 2 - Constrained Quality

```python
def obj_quality_at_target_n(result, cutoffs, target_n=10):
    n = result["n_intersection"]
    avg_pct = result["avg_percentile"]
    if n < target_n:
        return avg_pct * (n / target_n)  # Partial credit
    return avg_pct  # Full credit: maximize quality
```

**Use when**: You have a target portfolio size and want the highest quality subset.

#### Pattern 3 - Minimum Budget

```python
def obj_tightest_nonempty(result, cutoffs):
    n = result["n_intersection"]
    if n == 0:
        return 0.0
    total_budget = sum(cutoffs.values())
    return max_possible_budget - total_budget  # Lower budget = better
```

**Use when**: Finding the single most universally excellent config.

#### Pattern 4 - Diversity Reward

```python
def obj_diversity_reward(result, cutoffs):
    n = result["n_intersection"]
    if n == 0:
        return 0.0
    n_binding = result["n_binding_metrics"]
    n_active = sum(1 for v in cutoffs.values() if v < 100)
    if n_active == 0:
        return 0.0
    efficiency = n_binding / n_active
    return n * efficiency
```

**Use when**: Ensuring that tightened cutoffs provide independent information, not redundant filtering.

#### Pattern 5 - Pareto (Multi-Objective)

```python
study = optuna.create_study(
    directions=["maximize", "minimize"],  # max survivors, min cutoff
    sampler=optuna.samplers.NSGAIISampler(seed=42),
)
def objective(trial):
    cutoffs = suggest_cutoffs(trial)
    result = run_ranking_with_cutoffs(cutoffs, metric_data=metric_data)
    return result["n_intersection"], sum(cutoffs.values()) / len(cutoffs)
```

**Use when**: You want to see the full trade-off landscape between two competing objectives.

---

## Forensic Analysis Protocol

After running all objectives, perform this analysis:

### Step 1 - Cross-Objective Survivor Sets

```
For each objective:
    survivors_{objective} = set of configs in final intersection

universal_champions = survivors_1 AND survivors_2 AND ... AND survivors_K
```

If a config survives all K objective functions, it is robust to objective choice.

### Step 2 - Feature Theme Extraction

Count feature appearances across all survivors:

```
feature_counts = Counter()
for config_id in quality_survivors:
    for feature in config_id.split("__"):
        feature_counts[feature.split("_")[0]] += 1
```

Dominant features reveal the underlying market microstructure that the ranking system is selecting for.

### Step 3 - Uniform Tightening Curve

Apply the same cutoff to ALL metrics and plot intersection size:

```
@100%: 1008 survivors (no filter)
@80%:  502 survivors
@60%:  210 survivors
@40%:   68 survivors
@20%:   12 survivors
@10%:    3 survivors
@5%:     0 survivors
```

The shape of this curve reveals whether the metric space has natural clusters or is uniformly distributed.

### Step 4 - Binding Sequence

Tighten uniformly and at each step identify which metric was the "tightest killer" - the metric that eliminated the most configs:

```
@90%: 410 survivors | tightest killer: rachev (-57)
@80%: 132 survivors | tightest killer: headroom (-27)
@70%:  29 survivors | tightest killer: n_trades (-12)
@60%:   6 survivors | tightest killer: dsr (-6)
```

This reveals the binding constraint hierarchy.

---

## Implementation Checklist

When implementing this methodology in a new domain:

1. [ ] Define MetricSpec registry (name, direction, source, default cutoff)
2. [ ] Implement percentile ranking (scipy.stats.rankdata)
3. [ ] Implement per-metric cutoff application
4. [ ] Implement set intersection across all metrics
5. [ ] Add env var override for each cutoff
6. [ ] Create `run_ranking_with_cutoffs()` API function
7. [ ] Add binding metric detection
8. [ ] Create tightening analysis function
9. [ ] Write markdown report generator
10. [ ] Add Optuna optimizer with at least 3 objective functions
11. [ ] Pre-load metric data for optimizer performance
12. [ ] Run 5-objective forensic analysis (10K+ trials per objective)
13. [ ] Extract universal champions (cross-objective consistency)
14. [ ] Identify inert dimensions (remove from search space)
15. [ ] Document binding constraint sequence
16. [ ] Record feature themes in survivors

---

## Anti-Patterns

| Anti-Pattern              | Symptom                                                | Fix                                       | Severity |
| ------------------------- | ------------------------------------------------------ | ----------------------------------------- | -------- |
| Weighted-sum scoring      | Single metric dominates, others ignored                | Use intersection (P3)                     | CRITICAL |
| Starting strict           | Miss global optimum, premature convergence             | Start at 100%, tighten (P4)               | HIGH     |
| Uniform cutoffs only      | Over-filters inert metrics, under-filters binding ones | Per-metric independent cutoffs (P2)       | HIGH     |
| Single objective          | Artifact of objective bias                             | Run 5+ objectives, check consistency (P5) | HIGH     |
| Raw value comparison      | Scale-dependent, misleading                            | Always use percentile ranks (P1)          | HIGH     |
| Including inert metrics   | Wastes optimization budget                             | Detect and remove inert dimensions (P7)   | MEDIUM   |
| No data pre-loading       | Optimizer 10x slower                                   | Pre-load once, share across trials        | MEDIUM   |
| Unseeded optimizer        | Non-reproducible results                               | Always seed sampler (seed=42)             | MEDIUM   |
| Missing forensic analysis | Raw numbers without insight                            | Run full forensic protocol (P8)           | MEDIUM   |

---

## References

| Topic                | Reference File                                                                |
| -------------------- | ----------------------------------------------------------------------------- |
| Range Bar Case Study | [case-study-rangebar-ranking.md](./references/case-study-rangebar-ranking.md) |
| Objective Functions  | [objective-functions.md](./references/objective-functions.md)                 |
| Metric Design Guide  | [metric-design-guide.md](./references/metric-design-guide.md)                 |

### Related Skills

| Skill                                                      | Relationship                                                  |
| ---------------------------------------------------------- | ------------------------------------------------------------- |
| [rangebar-eval-metrics](../rangebar-eval-metrics/SKILL.md) | Metric definitions (TAMRS, Omega, DSR, etc.) fed into ranking |
| [adaptive-wfo-epoch](../adaptive-wfo-epoch/SKILL.md)       | Walk-Forward metrics that could be ranked                     |
| [backtesting-py-oracle](../backtesting-py-oracle/SKILL.md) | Validates trade outcomes used in metric computation           |

### Dependencies

```bash
pip install scipy numpy optuna>=4.7
```

---

## TodoWrite Task Templates

### Template A - Implement Ranking System (New Project)

```
1. [Preflight] Identify all evaluation metrics and their JSONL sources
2. [Preflight] Define MetricSpec registry (name, direction, source_file, source_field)
3. [Execute] Implement percentile_ranks() with scipy.stats.rankdata
4. [Execute] Implement apply_cutoff() and intersection()
5. [Execute] Add env var override for each metric cutoff (RANK_CUT_{NAME})
6. [Execute] Create run_ranking_with_cutoffs() API for optimizer
7. [Execute] Add binding metric detection and tightening analysis
8. [Execute] Write markdown report generator
9. [Verify] Unit tests for all pure functions (14+ tests)
10. [Verify] Run with default cutoffs (100%) - all configs should survive
```

### Template B - Add Evolutionary Optimizer

```
1. [Preflight] Verify ranking module has run_ranking_with_cutoffs() API
2. [Preflight] Add optuna>=4.7 dependency
3. [Execute] Implement 5 objective functions
4. [Execute] Create suggest_cutoffs() with step=5 search space
5. [Execute] Pre-load metric data once, share across trials
6. [Execute] Handle pareto_efficiency (NSGA-II) as special case
7. [Execute] Write JSONL output with provenance (git commit, timestamp)
8. [Verify] POC with 10 trials - verify non-trivial cutoffs found
9. [Verify] Full run with 10K trials per objective
```

### Template C - Forensic Analysis

```
1. [Preflight] Collect optimization results from all 5 objectives
2. [Execute] Extract survivor sets per objective
3. [Execute] Compute cross-objective intersection (universal champions)
4. [Execute] Run uniform tightening analysis (100% -> 5%)
5. [Execute] Identify binding metrics at each tightening step
6. [Execute] Extract feature themes from quality survivors
7. [Execute] Detect inert dimensions (zero discrimination)
8. [Verify] Document findings in structured summary table
```

---

## Post-Change Checklist (Self-Maintenance)

After modifying this skill:

1. [ ] Principles P1-P8 remain internally consistent
2. [ ] Anti-patterns table covers new patterns discovered
3. [ ] References in references/ are up to date
4. [ ] Case study reflects latest production results
5. [ ] Implementation checklist is complete and ordered
6. [ ] Plugin README updated if description changed

---

## Troubleshooting

| Issue                                 | Cause                             | Solution                                            |
| ------------------------------------- | --------------------------------- | --------------------------------------------------- |
| All cutoffs converge to 100%          | Metrics are all correlated        | Check for metric redundancy (Spearman r > 0.95)     |
| Zero intersection at mild cutoffs     | One metric has near-zero variance | Detect inert dimensions (P7)                        |
| Optimizer takes too long              | Disk I/O per trial                | Pre-load metric data (see Performance section)      |
| Different objectives give same answer | Objectives poorly differentiated  | Verify objective formulas test different trade-offs |
| Universal champion is mediocre        | Survival != excellence            | Check raw values, not just survival                 |
| Binding sequence changes across runs  | Unseeded optimizer                | Always use seed=42                                  |
| Too many survivors                    | Cutoffs too loose                 | Increase n_trials, lower step size                  |
| Zero survivors                        | Cutoffs too tight                 | Check for inert metrics inflating dimensionality    |
