---
name: rhino-sdk-metrics
description: "This skill should be used when the user wants to run federated metrics or analytics using the Rhino Health Python SDK, asks about survival analysis, statistical tests, KaplanMeier, Cox, Mean, Count, TTest, ChiSquare, RocAuc, correlation, odds ratio, or needs help choosing or configuring a metric."
metadata:
  author: rhino-health
  version: "0.1.0"
---

# Rhino Health SDK — Metrics Guide

Help configure and run any of the 40+ federated metrics in the `rhino-health` Python SDK (v2.1.x).

## Context Loading

Before responding, read these reference files:

1. **Metrics Reference** — `../../context/metrics_reference.md`
   All metric classes with parameters, import paths, categories, and the Quick Decision Guide.

2. **Patterns & Gotchas** — `../../context/patterns_and_gotchas.md`
   Focus on §4 (Per-site vs Aggregated Metrics), §5 (Filtering), §6 (Group By), and §7 (Federated Joins).

## Metric Decision Tree

Map the user's question to the right metric class:

| User asks about... | Metric class | Category |
|---|---|---|
| Counts, frequencies | `Count` | Basic |
| Averages, means | `Mean` | Basic |
| Spread, variability | `StandardDeviation`, `Variance` | Basic |
| Totals, sums | `Sum` | Basic |
| Percentiles, medians, quartiles | `Percentile`, `NPercentile` | Quantile |
| Survival time, time-to-event | `KaplanMeier` | Survival |
| Hazard ratios, covariates + survival | `Cox` | Survival |
| ROC curves, AUC | `RocAuc` | ROC/AUC |
| ROC with confidence intervals | `RocAucWithCI` | ROC/AUC |
| Correlation between variables | `Pearson`, `Spearman` | Statistics |
| Inter-rater reliability | `ICC` | Statistics |
| Compare two group means | `TTest` | Statistics |
| Compare 3+ group means | `OneWayANOVA` | Statistics |
| Categorical association | `ChiSquare` | Statistics |
| 2x2 contingency table | `TwoByTwoTable` | Epidemiology |
| Odds ratio | `OddsRatio` | Epidemiology |
| Risk ratio / relative risk | `RiskRatio` | Epidemiology |
| Risk difference | `RiskDifference` | Epidemiology |
| Incidence rates | `Incidence` | Epidemiology |

If unsure, consult the full Quick Decision Guide in `metrics_reference.md`.

## Execution Mode

Choose the right execution method based on scope:

| Scope | Method | Signature |
|---|---|---|
| Single site/dataset | `session.dataset.get_dataset_metric(dataset_uid, config)` | One dataset UID (str) |
| Single site (shorthand) | `dataset.get_metric(config)` | Called on a Dataset object |
| Aggregated across sites | `session.project.aggregate_dataset_metric(dataset_uids, config)` | `List[str]` of UIDs — **must be strings, not Dataset objects** |
| Federated join (SQL-like) | `session.project.joined_dataset_metric(config, query_datasets, filter_datasets)` | `List[str]` UIDs for both params |

All metrics are imported from `rhino_health.lib.metrics` (NOT `rhino_health.metrics`).

## Filtering

Apply filters to narrow the data before computing the metric. Two approaches:

### Inline FilterVariable (for simple per-column filters)

```python
from rhino_health.lib.metrics import Mean, FilterType, FilterVariable

config = Mean(
    variable="Height",
    data_filters=[
        FilterVariable(
            data_column="Gender",
            filter_column="Gender",
            filter_value="Female",
            filter_type=FilterType.EQUALS,
        )
    ],
)
```

### Range Filter (BETWEEN)

```python
from rhino_health.lib.metrics import FilterBetweenRange, FilterType, FilterVariable

config = Mean(
    variable="Height",
    data_filters=[
        FilterVariable(
            data_column="Age",
            filter_column="Age",
            filter_value=FilterBetweenRange(min=18, max=65),
            filter_type=FilterType.BETWEEN,
        )
    ],
)
```

## Grouping

Split results by one or more categorical columns:

```python
config = Mean(
    variable="Height",
    group_by={"groupings": ["Gender"]},
)
```

Grouping and filtering can be combined on any metric.

## Response Format

Structure every response as:

1. **Recommended metric** — which class and why it fits the user's question
2. **Configuration** — complete metric config object with correct import path
3. **Execution call** — the right method (`get_dataset_metric`, `aggregate_dataset_metric`, or `joined_dataset_metric`) with correct parameter types
4. **Filtering/grouping** — if the user specified subsets or breakdowns, add the appropriate `data_filters` and/or `group_by`
5. **See also** — point to a matching example from `../../context/examples/INDEX.md` if one exists

## Working Examples

Check `../../context/examples/INDEX.md` for matching examples. Key ones for metrics:

- `eda.py` — per-site and aggregated metrics with filtering and grouping
- `cox.py` — Cox proportional hazard regression
- `metrics_examples.py` — TwoByTwoTable, OddsRatio, ChiSquare, TTest, ANOVA
- `roc_analysis.py` — ROC curves and confidence intervals
- `aggregate_quantile.py` — federated percentile calculations
