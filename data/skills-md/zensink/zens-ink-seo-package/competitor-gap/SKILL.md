---
name: competitor-gap
description: >-
  Find content competitors rank for that the user does not, by diffing
  sitemaps — no paid tool, no login. Turns the gap into a prioritized content
  opportunity matrix (cluster x score). Use when the user asks "what content
  is my competitor ranking for that I'm missing", "compare my site to
  COMPETITOR", "what should I write next based on competitors", or gives 2-5
  competitor domains.
metadata:
  version: 1.0.0
  author: ZensInk
  source: https://zens.ink/skills/#competitor-gap
  license: MIT
---

# Competitor content gap from sitemaps

Competitors' sitemaps are public. Diffing them against the user's sitemap
reveals exactly what they publish that the user does not — URLs are the
units, no API key needed.

## When to use

- "Compare my content to competitor.com"
- "Find my content gaps vs these 3 sites"
- Building a content roadmap from competitor coverage.

## When NOT to use

- Competitor has no sitemap or blocks it — nothing to diff.
- The user wants rank positions (who ranks #1 for X) — that is the
  `rank-tracking` skill, not a sitemap diff.

## Setup

```bash
pip install zens-ink
```

## Commands

```bash
# Single competitor vs you
python3 -m zens_ink.competitor_gap --url https://competitor.com/sitemap.xml

# Multiple competitors at once, diff against all
python3 -m zens_ink.competitor_gap --compare \
  https://rival1.com/sitemap.xml https://rival2.com/sitemap.xml --lang en

# Then: prioritize the gap into a ranked matrix
python3 -m zens_ink.content_matrix \
  --scores opportunities.csv \
  --clusters clusters.json \
  --csv content-matrix.csv
```

`scores` comes from the `keyword-research` skill (kgr_auto CSV), `clusters`
from keyword_cluster JSON — pipe the two skills into this one.

## How to read the results

- URLs only the competitor has = topic-level gaps. Read their slug patterns:
  a `/glossary/` tree means a whole content program, not one page to copy.
- Filter by `--lang` when competitors are multilingual, or the diff fills
  with translated duplicates.
- The matrix ranks by expected value per hour of work — top rows are the
  first posts to write. Do not work alphabetically.

## Next steps

- Before writing each gap page: `search-intent` (right page type) then
  `keyword-difficulty` (winnable?).

## Going deeper

ZensInk Pro's Competitor Radar adds pricing intel and community sentiment
  to the same gap list: https://zens.ink/pricing/
