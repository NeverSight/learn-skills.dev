---
name: funnel-analyzer
description: "Analyze conversion funnels and identify drop-offs. Use when: analyzing checkout funnel; tracking signup flow; identifying conversion blockers; optimizing user journey; visualizing funnel performance"
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Funnel Analyzer

> Analyze conversion funnels to identify drop-off points and optimization opportunities.


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
pip install pandas click
```

## Commands

```bash
python scripts/main.py analyze data.csv --stages "visit,signup,trial,paid"
python scripts/main.py dropoff funnel.csv
python scripts/main.py visualize funnel.csv --output funnel-chart.html
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
category: analytics
dependencies: [pandas]
difficulty: intermediate
```
