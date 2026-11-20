---
name: rank-tracking
description: >-
  Track keyword rankings in a local SQLite history, pull real Google Search
  Console performance (impressions, clicks, position by query and page), and
  look up Ahrefs Domain Rating via the free public API with local caching.
  Use when the user asks "track my rankings", "how is my site performing in
  Google", "check my domain rating / DR", "which queries bring me clicks",
  or wants rank history over time instead of one-off checks.
metadata:
  version: 1.0.0
  author: ZensInk
  source: https://zens.ink/skills/#rank-tracking
  license: MIT
---

# Rankings, GSC performance, DR

Three data legs: rank snapshots over time (SQLite), GSC ground truth, and
DR lookups for sizing up any domain.

## When to use

- "Track these 10 keywords weekly"
- "What queries actually bring me clicks?" (GSC)
- "What's the DR of these 5 domains?"

## When NOT to use

- Daily rank checks on a big keyword set — rank checks cost SERP quota;
  weekly cadence is the intended rhythm.

## Setup

```bash
pip install zens-ink
python3 -m zens_ink.setup_gsc   # one-time GSC auth (for search_performance)
```

Keys in `.env`: `SERPER_API_KEY` (rank checks), `GSC_*` (Search Console),
`AHREFS_API_KEY` (DR lookups — free public API).

## Commands

```bash
# Rankings with history
python3 -m zens_ink.rank_tracker add "open source seo tools,seo cli tool"
python3 -m zens_ink.rank_tracker check      # snapshot now
python3 -m zens_ink.rank_tracker trend       # latest vs previous
python3 -m zens_ink.rank_tracker history "seo cli tool"

# GSC performance (real data, read-only)
python3 -m zens_ink.search_performance --queries --limit 30
python3 -m zens_ink.search_performance --pages
python3 -m zens_ink.search_performance --page /pricing/ --start 2026-09-01

# Domain Rating (free Ahrefs public API, cached locally)
python3 -m zens_ink.domain_rating zens.ink competitor.com
python3 -m zens_ink.domain_rating --file domains.txt --csv dr.csv
```

Real DR output:

```
  Domain Rating | 1 target(s) | Data: Domain Rating by Ahrefs (https://ahrefs.com/)

  [1/1] zens.ink                                 DR 21
```

Attribution note: DR output must keep the "Domain Rating by Ahrefs" credit
line — it is a license requirement of the free API.

## How to read the results

- **GSC position 5-30 with impressions** = quick-win zone: pages Google
  already likes. Improve title/on-page, add internal links, re-index.
- Position 30+ with impressions = crawling fine, ranking weak — content or
  authority problem, not technical.
- Impressions with zero clicks across the board = title/snippet problem.
- DR: compare against the sites actually ranking for your target keywords,
  not industry averages. Results cache in `dr-cache.json`; `--no-cache` to
  refresh.

## Next steps

- Quick-wins found in GSC → `site-audit` skill on those exact pages.
- New keyword ideas → `keyword-research` skill.

## Going deeper

ZensInk Pro's GSC quadrants tool plots the official Google bubble chart
(CTR vs position) across the whole property: https://zens.ink/pricing/
