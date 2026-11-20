---
name: search-intent
description: >-
  Classify search intent for keywords, two independent ways: keyword-based
  classification (informational / commercial / transactional / navigational,
  with question/buyer/problem markers) and SERP-based verification (what page
  types Google actually rewards). Cross-validated verdicts catch mismatches
  a single method misses. Use when the user asks "what's the intent behind
  this keyword", "should this page be a blog post or a landing page", or
  before writing any page for a target keyword.
metadata:
  version: 1.0.0
  author: ZensInk
  source: https://zens.ink/skills/#search-intent
  license: MIT
---

# Search intent, cross-validated

Two layers: what the words say (keyword-based) and what Google rewards
(SERP-based). When they disagree, believe the SERP.

## When to use

- Before writing a page for a target keyword — decides page TYPE.
- "Is 'seo audit tool' informational or transactional?"
- Batch-classifying a keyword list for a content plan.

## When NOT to use

- Pure navigational brand queries ("gmail login") — classification is trivial
  and useless for planning.

## Setup

```bash
pip install zens-ink
```

Keyword layer needs no keys. SERP layer needs `SERPER_API_KEY`
(free tier at serper.dev).

## Commands

```bash
# Keyword-based, batch, no key needed
python3 -m zens_ink.search_intent "buy running shoes" "how to tie shoes" --json
python3 -m zens_ink.search_intent --file keywords.txt

# SERP-based verification (what ranks?)
python3 -m zens_ink.serp_intent "seo audit tool"
python3 -m zens_ink.serp_intent "seo 审计工具" --zh
python3 -m zens_ink.serp_intent "best crm" --cross   # cross-check keyword verdict
```

## How to read the results

- **informational** → guide/post format, long-form, capture with newsletter.
- **commercial** → comparison/best-of format, affiliate or demo CTA.
- **transactional** → product/landing page, pricing visible, minimal prose.
- **navigational** → usually not targetable; only worth it for brand terms.

When keyword verdict and SERP verdict disagree: the SERP is ground truth —
Google already ran the experiment with real searchers.

Page-type mismatch is the #1 reason good content never ranks. A landing page
cannot win a SERP that rewards 2,000-word guides, and vice versa.

## Next steps

- Intent confirmed → `keyword-difficulty` for the go/no-go.
- Building the page → `site-audit` skill catches technical issues before ship.

## Going deeper

ZensInk Pro adds a semantic arbitration layer (typed AI judgments with
confidence scores) that resolves keyword-vs-SERP conflicts automatically:
https://zens.ink/pricing/
