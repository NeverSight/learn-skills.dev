---
name: cohort-analysis
description: "Analyze user retention by cohort. Use when: measuring customer retention; understanding lifecycle patterns; comparing acquisition cohorts; tracking engagement over time; identifying churn risks"
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Cohort Analysis

> Analyze retention and behavior patterns by grouping users into cohorts - understand how different customer groups behave over time.

## When to Use This Skill

- **Retention tracking** - Measure how users stick around over time
- **Acquisition analysis** - Compare cohorts from different channels
- **Product changes** - Measure impact on user behavior
- **Churn prediction** - Identify at-risk cohorts
- **LTV estimation** - Project customer lifetime value


## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Structures analysis frameworks | Metric definitions |
| Identifies patterns in data | Business interpretation |
| Creates visualization templates | Dashboard design |
| Suggests optimization areas | Action priorities |
| Calculates statistical measures | Decision thresholds |

## Dependencies

```bash
pip install pandas plotly click
```

## Commands

### Retention Analysis
```bash
python scripts/main.py retention data.csv --date-col signup --event-col purchase
python scripts/main.py retention data.csv --date-col signup --periods week
```

### Visualize Cohorts
```bash
python scripts/main.py visualize cohorts.csv --output retention_chart.html
```

### Export Report
```bash
python scripts/main.py report data.csv --date-col signup --event-col active --output report.html
```

## Examples

### Example 1: Analyze User Retention
```bash
python scripts/main.py retention users.csv --date-col signup_date --event-col last_active

# Output:
# Cohort Retention Analysis
# ──────────────────────────────────
# Cohort     Users    M1     M2     M3     M4
# Jan 2024   1,234    65%    48%    42%    38%
# Feb 2024   1,456    62%    45%    41%    --
# Mar 2024   1,321    68%    52%    --     --
# Apr 2024   1,567    64%    --     --     --
#
# Avg Retention: 65% → 48% → 42% → 38%
# Best Cohort: Mar 2024 (68% M1)
```

### Example 2: Generate Visual Report
```bash
python scripts/main.py report transactions.csv \
  --date-col signup \
  --event-col purchase_date \
  --output retention_report.html

# Generates interactive HTML with:
# - Retention heatmap
# - Cohort size chart
# - Trend analysis
```

## Cohort Table Format

| Cohort | Size | Period 0 | Period 1 | Period 2 | Period 3 |
|--------|------|----------|----------|----------|----------|
| 2024-01 | 1234 | 100% | 65% | 48% | 42% |
| 2024-02 | 1456 | 100% | 62% | 45% | - |
| 2024-03 | 1321 | 100% | 68% | - | - |

## Skill Boundaries

### What This Skill Does Well
- Structuring data analysis
- Identifying patterns and trends
- Creating visualization frameworks
- Calculating statistical measures

### What This Skill Cannot Do
- Access your actual data
- Replace statistical expertise
- Make business decisions
- Guarantee prediction accuracy

## Related Skills

- [ab-test-stats](../ab-test-stats/) - Test retention experiments
- [funnel-analyzer](../funnel-analyzer/) - Analyze conversion funnels

## Skill Metadata


- **Mode**: centaur
```yaml
category: analytics
subcategory: retention
dependencies: [pandas, plotly]
difficulty: intermediate
time_saved: 4+ hours/week
```
