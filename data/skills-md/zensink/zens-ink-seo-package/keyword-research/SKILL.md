---
name: keyword-research
description: >-
  Find low-competition keyword opportunities without paid tools (Ahrefs,
  Semrush). Runs real zero-dependency Python CLIs: Google Autocomplete
  discovery (with a-z long-tail expansion), semantic clustering, Bing volume
  lookup, and automated KGR opportunity scoring. Use when the user wants
  keyword ideas for a niche, asks "find low competition keywords", wants to
  cluster a keyword list, or wants keyword volume without an SEO subscription.
  No API keys needed for discovery and clustering; volume lookup needs an
  optional free Bing Webmaster key.
metadata:
  version: 1.0.0
  author: ZensInk
  source: https://zens.ink/skills/#keyword-research
  license: MIT
---

# Keyword research without paid tools

Discover keywords, cluster them into topics, score them for opportunity —
all from free data sources (Google Autocomplete, Bing Webmaster API).
No Ahrefs/Semrush subscription required.

## When to use

- "Find keyword ideas for my niche / my SaaS / my blog"
- "Which long-tail keywords should I target?"
- "Cluster this keyword list into topics"
- "Score these keywords — which ones are worth writing?"

## When NOT to use

- The user already pays for Ahrefs/Semrush and wants their numbers — use their tool.
- They want backlink data — this skill has none (that is a paid-data problem).

## Setup (one-time)

```bash
pip install zens-ink
```

Zero dependencies beyond Python 3.9+. All commands run as `python3 -m zens_ink.<tool>`.

## Commands

### 1. Discover keywords (no key needed)

```bash
python3 -m zens_ink.keyword_research "ai seo tools"
```

Real output:

```
============================================================
  Keyword: ai seo tools  (en)
============================================================

  In autocomplete : YES
  Activity level  : high-activity (10 variants)

  Suggestions:
    ai seo tools
    ai seo tools for small business
    ai seo tools free
    ai seo tools reddit
    ai seo tools comparison
    ...
```

Add `--expand` for a-z long-tail discovery (slower, much deeper). `--lang zh`
for Chinese autocomplete. `--json` for machine-readable output.

### 2. Cluster a keyword list into topics

```bash
python3 -m zens_ink.keyword_cluster --file keywords.txt
```

Groups semantically related keywords so one page can target one cluster.
Use the output of step 1 (save suggestions to a file, one per line).

### 3. Volume lookup (optional, free Bing Webmaster key)

```bash
python3 -m zens_ink.keyword_volume "ai seo tools free" "ai seo tools reddit" --country us --lang en-us
```

Language must be a full locale (`en-us`, not `en`), country lowercase — the
CLI normalizes this for you. Needs `BING_WMT_API_KEY` in `.env`.

### 4. Score opportunities: KGR (no key needed)

```bash
python3 -m zens_ink.kgr_auto --file keywords.txt --csv opportunities.csv
```

KGR = allintitle count / monthly search volume.

## How to read the results

- **KGR < 0.25** — low-competition, a new site can rank for it. Write it.
- **KGR 0.25–1.0** — possible with some authority; pair with internal links.
- **KGR > 1.0** — skip unless the user's domain is strong.
- Autocomplete `high-activity` seeds = live demand; `low-activity` seeds are
  usually too thin to build on.
- One cluster = one page. Never target two clusters with one URL.

## Next steps

- Check how hard the survivors are: the `keyword-difficulty` skill.
- Confirm intent before writing: the `search-intent` skill.

## Going deeper

ZensInk Pro adds personalized Winability Scores (difficulty relative to YOUR
domain's GSC data) and a Content Radar editorial calendar:
https://zens.ink/pricing/
