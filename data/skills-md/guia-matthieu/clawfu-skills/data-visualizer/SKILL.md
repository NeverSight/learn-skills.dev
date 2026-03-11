---
name: data-visualizer
description: "Create marketing visualizations from data. Use when: creating charts for reports; visualizing campaign performance; generating dashboards; presenting data insights; exporting charts for presentations"
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Data Visualizer

> Generate professional charts and visualizations from CSV data for marketing reports.


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
pip install plotly pandas click
```

## Commands

```bash
python scripts/main.py chart data.csv --type bar --x month --y revenue
python scripts/main.py dashboard data.csv --metrics "revenue,users,churn"
python scripts/main.py export chart.html --format png
```

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

## Skill Metadata


- **Mode**: centaur
```yaml
category: automation
dependencies: [plotly, pandas]
difficulty: beginner
```
