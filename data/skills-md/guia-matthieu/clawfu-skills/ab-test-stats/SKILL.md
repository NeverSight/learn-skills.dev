---
name: ab-test-stats
description: "Calculate A/B test statistical significance. Use when: determining if test results are significant; calculating required sample size; estimating test duration; analyzing conversion experiments; making data-driven decisions"
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# A/B Test Statistics Calculator

> Calculate statistical significance for A/B tests - know when your results are real, not random chance.

## When to Use This Skill

- **Test analysis** - Determine if results are statistically significant
- **Sample planning** - Calculate required sample size before testing
- **Duration estimation** - Know how long to run experiments
- **Power analysis** - Ensure tests can detect meaningful differences


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
pip install scipy numpy click
```

## Commands

### Check Significance
```bash
python scripts/main.py significance --control 1000,50 --variant 1000,65
python scripts/main.py significance --control 5000,250 --variant 5000,300 --confidence 0.99
```

### Calculate Sample Size
```bash
python scripts/main.py sample-size --baseline 0.05 --mde 0.02
python scripts/main.py sample-size --baseline 0.10 --mde 0.01 --power 0.90
```

### Estimate Duration
```bash
python scripts/main.py duration --traffic 1000 --baseline 0.05 --mde 0.02
```

## Examples

### Example 1: Analyze Test Results
```bash
# Control: 1000 visitors, 50 conversions (5%)
# Variant: 1000 visitors, 65 conversions (6.5%)
python scripts/main.py significance --control 1000,50 --variant 1000,65

# Output:
# A/B Test Results
# ─────────────────────────
# Control:  5.00% (50/1000)
# Variant:  6.50% (65/1000)
# Lift:     +30.0%
#
# Statistical Analysis
# ─────────────────────────
# p-value:      0.089
# Confidence:   91.1%
# Result:       NOT SIGNIFICANT (need 95%)
#
# Recommendation: Continue test for more data
```

### Example 2: Plan Sample Size
```bash
# Baseline 5% conversion, want to detect 20% relative lift (1% absolute)
python scripts/main.py sample-size --baseline 0.05 --mde 0.01

# Output:
# Sample Size Calculator
# ──────────────────────────────
# Baseline conversion: 5.0%
# Minimum detectable effect: 1.0% (20% relative)
# Target conversion: 6.0%
#
# Required per variant: 3,842 visitors
# Total required: 7,684 visitors
#
# At 1000 daily visitors: ~8 days
```

## Key Concepts

| Term | Definition |
|------|------------|
| **p-value** | Probability result is due to chance |
| **Confidence** | 1 - p-value (usually want 95%+) |
| **Power** | Probability of detecting real effect (usually 80%) |
| **MDE** | Minimum Detectable Effect - smallest lift worth detecting |
| **Lift** | Relative improvement (variant - control) / control |

## When Results Are Significant

| p-value | Confidence | Verdict |
|---------|------------|---------|
| < 0.01 | > 99% | Highly Significant ✓ |
| < 0.05 | > 95% | Significant ✓ |
| < 0.10 | > 90% | Marginally Significant |
| ≥ 0.10 | < 90% | Not Significant ✗ |

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

- [cohort-analysis](../cohort-analysis/) - Analyze user cohorts
- [funnel-analyzer](../funnel-analyzer/) - Analyze conversion funnels

## Skill Metadata


- **Mode**: centaur
```yaml
category: analytics
subcategory: statistics
dependencies: [scipy, numpy]
difficulty: intermediate
time_saved: 3+ hours/week
```
