---
name: site-audit
description: >-
  Technical SEO audit for static site builds (Astro, Next.js export, Hugo,
  Eleventy, any dist/ folder) plus on-page quality scoring and pre-publish
  content QC. Finds broken links, missing canonicals/H1/meta descriptions,
  image problems, orphan pages, and scores every page 0-100 across 7 on-page
  dimensions. Use when the user says "audit my site", "check my build for SEO
  problems", "what's wrong with my pages before launch", or wants a
  pre-publish quality gate for drafts. Works offline on the build output —
  no crawling quota, no login.
metadata:
  version: 1.0.0
  author: ZensInk
  source: https://zens.ink/skills/#site-audit
  license: MIT
---

# Site audit on the build output

Audits run against the built `dist/` directory — deterministic, offline,
repeatable in CI. Three tools, three altitudes: site-wide technical, per-page
quality, per-draft gate.

## When to use

- "Audit my site for SEO problems" (any static site)
- Pre-launch checklist on a fresh build
- A page won't rank and nobody knows why
- CI gate: fail the build when quality drops

## When NOT to use

- Sites behind login or rendered only client-side with no static output —
  there is no dist/ to read.

## Setup

```bash
pip install zens-ink
cd the-site-repo && npm run build   # produce dist/ first
```

## Commands

```bash
# 1. Site-wide technical audit (broken links, meta, images, canonicals)
python3 -m zens_ink.site_audit --dist dist
python3 -m zens_ink.site_audit --dist dist --format json --output audit.json

# 2. Per-page on-page quality, 7 dimensions, 0-100
python3 -m zens_ink.onpage_audit --dist dist
python3 -m zens_ink.onpage_audit --dist dist --keywords keywords.txt

# 3. Pre-publish gate for markdown drafts (exit 1 below score 70)
python3 -m zens_ink.content_qc drafts/ --min-score 70
```

## How to read the results

Work the report top-down — it is ordered by blast radius:
1. **Broken links / 404s** — fix first, they waste crawl budget and trust.
2. **Missing canonical / H1 / meta description** — quick wins, one file each.
3. **Image size flags** — above `--max-image-kb` (default generous), compress.
4. **On-page scores** — anything under ~70 has a concrete reason listed;
   fix the named dimension, not the score.

`content_qc` in a CI pipeline: `--min-score 70` makes low-quality drafts
fail the build. Will AI engines cite this draft? is the question it answers
(BLUF presence, structure, quotable facts).

Known false positive: sitemap-index style sitemaps from Astro may parse as
0 URLs — if the audit reports zero sitemap URLs on an Astro site, ignore the
sitemap section; the link/meta findings are still valid.

## Next steps

- Audit clean but still not ranking → `keyword-difficulty` (it may be the
  keyword, not the site).
- Make the site AI-citable → `geo-readiness` skill.

## Going deeper

ZensInk Pro chains these into a 12-step full audit (search intent, on-page,
technical, prioritized fix plan, MD + client-ready HTML report):
https://zens.ink/pricing/
