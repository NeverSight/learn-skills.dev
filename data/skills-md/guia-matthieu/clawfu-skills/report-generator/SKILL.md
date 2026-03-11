---
name: report-generator
description: "Generate PDF/HTML reports from templates and data. Use when: creating client reports; generating weekly summaries; producing marketing performance reports; automating recurring reports"
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Report Generator

> Automate marketing report generation from templates and data sources.


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
pip install jinja2 pandas click
# For PDF output:
pip install weasyprint
```

## Commands

```bash
python scripts/main.py generate template.html --data data.json --output report.html
python scripts/main.py weekly metrics.csv --output weekly-report.html
python scripts/main.py client data/ --template agency --output client-report.pdf
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
dependencies: [jinja2, pandas]
difficulty: intermediate
```
