---
name: keyword-clusterer
description: "Cluster keywords by semantic similarity and intent. Use when: organizing keyword research; creating content pillars; mapping keywords to pages; identifying content gaps; grouping search intent"
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Keyword Clusterer

> Group keywords by semantic similarity using embeddings - turn a keyword list into an organized content strategy.

## When to Use This Skill

- **Content planning** - Group keywords into topic clusters
- **Site structure** - Map keywords to pages
- **Intent analysis** - Categorize by search intent
- **Gap analysis** - Find missing keyword themes
- **PPC organization** - Group keywords for ad groups


## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Structures analysis frameworks | Strategic priorities |
| Synthesizes market data | Competitive positioning |
| Identifies opportunities | Resource allocation |
| Creates strategic options | Final strategy selection |
| Suggests implementation approaches | Execution decisions |

## Dependencies

```bash
pip install scikit-learn sentence-transformers pandas click
# For simpler usage without ML:
pip install click pandas
```

## Commands

### Cluster Keywords
```bash
python scripts/main.py cluster keywords.csv --n-clusters 10
python scripts/main.py cluster keywords.csv --column keyword --n-clusters 15
```

### Find Similar
```bash
python scripts/main.py similar "content marketing" --count 20
```

### Analyze Intent
```bash
python scripts/main.py intent keywords.csv --column keyword
```

## Examples

### Example 1: Cluster Keyword Research
```bash
# Input: keywords.csv with 500 keywords
python scripts/main.py cluster keywords.csv --n-clusters 12 --output clustered.csv

# Output:
# Cluster 1 (45 keywords): "content marketing"
#   - content marketing strategy
#   - content marketing tips
#   - how to do content marketing
#
# Cluster 2 (38 keywords): "email marketing"
#   - email marketing tools
#   - best email marketing software
#   - email campaign tips
# ...
```

### Example 2: Categorize by Intent
```bash
python scripts/main.py intent keywords.csv --column keyword

# Output:
# Intent Analysis
# ──────────────────────
# Informational: 234 (47%)
#   - how to, what is, guide, tips
# Commercial: 156 (31%)
#   - best, top, review, compare
# Transactional: 78 (16%)
#   - buy, price, discount, order
# Navigational: 32 (6%)
#   - login, contact, brand names
```

## Search Intent Categories

| Intent | Signals | Content Type |
|--------|---------|--------------|
| **Informational** | how, what, why, guide | Blog posts, guides |
| **Commercial** | best, top, review, vs | Comparisons, reviews |
| **Transactional** | buy, price, discount | Product pages |
| **Navigational** | [brand], login, contact | Landing pages |

## Clustering Methods

| Method | Best For | Speed |
|--------|----------|-------|
| **semantic** | Meaning-based grouping | Slower |
| **lexical** | Word overlap grouping | Faster |
| **intent** | Search intent categories | Fast |

## Skill Boundaries

### What This Skill Does Well
- Structuring strategic analysis
- Identifying market opportunities
- Creating strategic frameworks
- Synthesizing competitive data

### What This Skill Cannot Do
- Replace market research
- Guarantee strategic success
- Know proprietary competitor info
- Make executive decisions

## Related Skills

- [content-repurposer](../../automation/content-repurposer/) - Create content for clusters
- [lighthouse-audit](../lighthouse-audit/) - Optimize cluster pages

## Skill Metadata


- **Mode**: centaur
```yaml
category: seo-tools
subcategory: keyword-research
dependencies: [scikit-learn, sentence-transformers, pandas]
difficulty: intermediate
time_saved: 5+ hours/week
```
