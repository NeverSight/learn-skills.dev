---
name: data-quality
description: Quality dimensions, scorecards, distribution monitoring, and freshness checks. Use for data validation pipelines and quality gates.
allowed-tools: Read Write Edit Bash
---

# Data Quality

**Audience:** Data engineers building quality gates for pipelines.

**Goal:** Measure, monitor, and report on data quality dimensions.

**Related skills:**
- `data-profiler` - For comprehensive data profiling
- `anomaly-detector` - For outlier detection

## Scripts

Execute quality functions from `scripts/quality_metrics.py`:

```python
from scripts.quality_metrics import (
    QualityDimension,
    QualityMetric,
    QualityScorecard,
    calculate_completeness,
    calculate_uniqueness,
    check_freshness,
    check_volume,
    detect_distribution_drift,
    generate_scorecard,
    generate_html_report
)
```

## Usage Examples

### Quality Checks

```python
from scripts.quality_metrics import calculate_completeness, calculate_uniqueness

# Completeness check
completeness = calculate_completeness(df, required_cols=['id', 'email', 'status'])
print(f"Completeness: {completeness.score}% - {'PASS' if completeness.passed else 'FAIL'}")

# Uniqueness check
uniqueness = calculate_uniqueness(df, key_cols=['id'])
print(f"Uniqueness: {uniqueness.score}%")
```

### Freshness Check

```python
from scripts.quality_metrics import check_freshness

freshness = check_freshness(df, timestamp_col='updated_at', max_age_hours=24)
if not freshness.passed:
    print(f"Data is stale: {freshness.details['age_hours']} hours old")
```

### Generate Scorecard

```python
from scripts.quality_metrics import generate_scorecard, generate_html_report

scorecard = generate_scorecard(
    df,
    name="users_table",
    required_cols=['id', 'email'],
    key_cols=['id']
)

print(f"Overall Score: {scorecard.overall_score:.1f}%")
print(f"Status: {'PASSED' if scorecard.passed else 'FAILED'}")

# Generate HTML report
html = generate_html_report(scorecard)
```

### Distribution Drift

```python
from scripts.quality_metrics import detect_distribution_drift

drift = detect_distribution_drift(baseline_df['revenue'], current_df['revenue'])
if drift['drifted']:
    print(f"Distribution drift detected: {drift['test']} p-value={drift['p_value']:.4f}")
```

## Quality Dimensions

| Dimension | What It Measures |
|-----------|-----------------|
| Completeness | Missing values, required fields |
| Uniqueness | Duplicates in key columns |
| Validity | Format, range, pattern compliance |
| Accuracy | Correctness vs source of truth |
| Consistency | Cross-field logical rules |
| Timeliness | Data freshness, staleness |

## Dependencies

```
pandas
scipy  # For distribution drift detection
```
