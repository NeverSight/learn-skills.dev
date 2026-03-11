---
name: influencer-finder
description: "Find and analyze influencers for campaigns. Use when: researching potential influencer partners; analyzing influencer metrics; building influencer lists; evaluating engagement rates; planning influencer outreach"
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Influencer Finder

> Find and evaluate influencers for marketing collaborations and partnerships.


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
pip install click requests pandas
```

## Commands

```bash
python scripts/main.py search "fitness" --platform instagram --followers 10000-100000
python scripts/main.py analyze @influencer --platform instagram
python scripts/main.py export influencers.csv --with-metrics
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
category: social
dependencies: [click, requests, pandas]
difficulty: intermediate
```
