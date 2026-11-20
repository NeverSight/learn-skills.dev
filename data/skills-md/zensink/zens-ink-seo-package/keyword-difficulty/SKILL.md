---
name: keyword-difficulty
description: >-
  Estimate keyword difficulty from SERP structure — no Ahrefs subscription.
  Analyzes who actually ranks (homepage vs inner pages, platform ecosystems,
  brand-word fingerprints, winnable seat count) and outputs a difficulty
  verdict with an entry strategy. Use when the user asks "how hard is this
  keyword", "can I rank for X", "keyword difficulty without Ahrefs", or wants
  a go/no-go call on a keyword. Needs a free Serper.dev key for SERP data.
metadata:
  version: 1.0.0
  author: ZensInk
  source: https://zens.ink/skills/#keyword-difficulty
  license: MIT
---

# Keyword difficulty from SERP structure

Most KD scores are paywalled link metrics. This reads the actual SERP and
answers the only question that matters: are there winnable seats, and what
type of page wins them?

## When to use

- "Can I rank for 'best crm for startups'?"
- "How competitive is this keyword?"
- "Should I write this article or skip it?"

## When NOT to use

- Head terms dominated by Wikipedia/major brands — the tool will tell you,
  but the answer is already no.
- The user needs a DR-style number to put in a report — use `domain_rating`
  (rank-tracking skill) for DR lookups instead.

## Setup

```bash
pip install zens-ink
```

Set `SERPER_API_KEY` in `.env` (free tier: 2,500 searches/month at
serper.dev).

## Commands

```bash
python3 -m zens_ink.kd "open source seo tools"
python3 -m zens_ink.kd "开源 seo 工具" --zh
python3 -m zens_ink.kd "best crm" --json          # machine-readable
python3 -m zens_ink.kd "best crm" --markdown       # self-contained report
```

## How to read the results

The analysis is built on three fingerprints of a locked SERP:

1. **Same-name official domains in top 3** — navigational lock, hard to enter.
2. **One domain family holding 2+ seats** — brand sitelinks, Google treats it
   as the canonical answer.
3. **Platform ecosystem density** — Reddit/YouTube/GitHub stacking means
   Google wants UGC/forum content for this query.

2+ fingerprints = brand-locked keyword. The output also after removing official and platform-fixed seats — that is the number
that decides go/no-go, not the raw top-10 strength.

**Decision rule:** if the winnable-seat difficulty is moderate and intent
matches the user's page type, write it. If every seat is brand-locked, pivot
to the long-tail variant (feed the seed back through the `keyword-research`
skill with `--expand`).

## Next steps

- Verify what Google actually rewards: the `search-intent` skill runs the
  SERP page-type breakdown.
- Batch-scored a list already? The `competitor-gap` skill finds what rivals
  rank for that the user does not.

## Going deeper

ZensInk Pro's Winability Score cross-references difficulty with the user's
own GSC footprint — keywords THEY can win, not keywords a generic site can:
https://zens.ink/pricing/
