---
name: geo-readiness
description: >-
  Make a site citable by AI engines (ChatGPT, Perplexity, Google AI
  Overviews) — Generative Engine Optimization. Audits robots.txt AI-crawler
  policy and the llms.txt layer, generates llms.txt / llms-full.txt from a
  static build or sitemap, and plans Query Fan-out content (the sub-queries
  AI engines spawn from a seed question). Use when the user asks "how do I
  get cited by ChatGPT/Perplexity", "make my site AI-readable", "GEO audit",
  "generate llms.txt", or plans content for AI search visibility.
metadata:
  version: 1.0.0
  author: ZensInk
  source: https://zens.ink/skills/#geo-readiness
  license: MIT
---

# GEO: get cited by AI engines

AI engines cite pages they can retrieve, parse, and trust. This skill covers
the three layers: crawler policy (robots.txt), machine-readable index
(llms.txt), and content shaped for fan-out queries.

## When to use

- "How do I get my site cited by ChatGPT / Perplexity?"
- "Generate llms.txt for my site"
- "Audit my AI readiness"
- Planning content that answers AI-spawned sub-questions.

## When NOT to use

- The site has zero conventional rankings — AI citation mostly mirrors SERP
  strength; fix rankings first (`keyword-research` + `site-audit` skills).

## Setup

```bash
pip install zens-ink
```

## Commands

```bash
# 1. Audit the AI layer: robots.txt crawler policy + llms.txt presence
python3 -m zens_ink.ai_crawler_audit https://example.com
python3 -m zens_ink.ai_crawler_audit https://example.com --markdown report.md

# 2. Generate llms.txt + llms-full.txt from a build or remote sitemap
python3 -m zens_ink.llms_gen --dist dist --site https://example.com \
  --name "Example" --tagline "What the site does"
python3 -m zens_ink.llms_gen --sitemap https://example.com/sitemap.xml \
  --site https://example.com

# 3. Plan Query Fan-out content (sub-queries AI engines derive)
python3 -m zens_ink.geo_fanout "best crm" --icp "small business owners"
python3 -m zens_ink.geo_fanout "ai seo" --lang zh

# 4. Gate drafts for citability before publishing
python3 -m zens_ink.content_qc drafts/
```

## How to read the results

- **ai_crawler_audit**: decide the stance deliberately — allow search/RAG
  crawlers (ai-input=yes, get cited) while denying training crawlers
  (ai-train=no, protect original IP). Content Signals comments in robots.txt
  express this machine-readably.
- **llms_gen**: llms.txt is the index, llms-full.txt the deep layer. Keep
  descriptions factual (what the page answers), not marketing copy —
  agents route by task, not by adjectives.
- **geo_fanout**: each sub-query is a heading your content should answer
  directly (BLUF style, quotable facts). Fan-out coverage = more retrieval
  surface across engines.
- **content_qc**: scores whether a draft is citable (BLUF, structure,
  quotable specifics). Below 70, fix the named dimension.

The hard truth: plumbing does not create citations — retrieval does. SERP
presence feeds AI visibility. Treat this layer as necessary, not sufficient.

## Next steps

- Track whether citations actually appear: run a weekly probe of buyer
  questions against AI search stacks and diff the answers over time
  (pattern: fixed question set, saved answers, delta report).
- Technical issues blocking indexing → `site-audit` skill.

## Going deeper

ZensInk Pro ships a 16-dimension GEO Score (fact layer, structure, semantic,
  AI-access, trust) with prioritized P0/P1/P2 fixes: https://zens.ink/pricing/
