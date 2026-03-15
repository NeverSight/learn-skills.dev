---
name: seo-team-the-doctor
description: Crawls, scores, and prescribes fixes for technical SEO, content quality, backlink health, and AI visibility issues at site and page level. Use when the user wants to audit a site, diagnose ranking problems, run an SEO health check, compare a page against competitors, or get a prioritised fix list.
license: MIT
prerequisites:
  - DataForSEO API key
metadata:
  author: Skill Atlas
  version: "0.1.2"
  homepage: https://skillatlas.sh/
---

# SEO Doctor — Site & Page Diagnostician

The Doctor audits sites and pages, scores SEO health across five dimensions, and produces a prioritised fix list.

## Prerequisites

- **DataForSEO API key** — This skill uses `seocli`, which sources all its data from the [DataForSEO API](https://dataforseo.com/). You need a DataForSEO account and API key before using any SEO team skill.

## Two Operating Modes

Infer mode from the user's request:

| Mode                  | Trigger                                                                         | API Cost    |
| --------------------- | ------------------------------------------------------------------------------- | ----------- |
| **Site-Wide Audit**   | "audit my site," "health check," domain reference without specific page+keyword | 25–35 calls |
| **Single-Page Audit** | Specific URL + keyword, "why isn't this ranking," page vs competitor comparison | 9–12 calls  |

```
IF user mentions a specific URL + keyword pair → Single-Page Audit
ELSE IF user mentions a domain, "my site", "health check", or "audit" → Site-Wide Audit
ELSE → Ask: "Would you like me to audit your entire site, or diagnose a specific page?"
```

## Pre-Flight (Both Modes)

Before any API calls:

1. **Check audit history** — Look in `workspace/seo/audit-history/` for recent audits. If one ran within 7 days, offer to reuse crawl data.
2. **Load config** — Read `workspace/seo/config.yaml` for domain, competitors, location.
3. **Load keyword context** — Read `workspace/seo/keyword-map.json` for target keywords to spot-check.
4. **Confirm scope** (site-wide only) — Ask site size (small <50, medium 50–500, large >500) and type (blog, catalog, SaaS, mixed).

## Cost Estimation & Confirmation

Before executing, estimate API calls and confirm with the user:

**Site-Wide:** ~25–35 calls (1 crawl + 6 result retrievals + 3–5 Lighthouse + 5 backlink + 3 ranking + 1 LLM mentions + 5–10 AI Overview checks + 1 llms.txt check).

**Single-Page:** ~9–12 calls (1 on-page live + 1 SERP organic + 1 SERP AI mode + 3 competitor on-page + 3 competitor backlinks).

---

## Mode 1: Site-Wide Audit

```
PRE-FLIGHT → CRAWL → LIGHTHOUSE → BACKLINKS → RANKINGS → AI VISIBILITY → ON-PAGE SPOT-CHECKS → SCORE → PRIORITISE → REPORT
```

### Step 1 — Technical Crawl

Start an async crawl with content parsing, micromarkup validation, spell checking, resource loading, and keyword density enabled:

```bash
seocli on-page create \
  --target "example.com" \
  --max-crawl-pages 500 \
  --enable-content-parsing \
  --validate-micromarkup \
  --check-spell \
  --load-resources \
  --calculate-keyword-density
```

Adapt crawl config by site signals: small site → `--max-crawl-pages 100`; large/e-commerce → `--max-crawl-pages 500 --crawl-delay 1`; international → `--allow-subdomains`; pre-launch → `--enable-www-redirect-check`.

Poll for completion, then retrieve results:

```bash
seocli on-page summary --id <task-id>
seocli on-page pages --id <task-id> --limit 500
seocli on-page duplicate-content --id <task-id>
seocli on-page duplicate-tags --id <task-id> --type duplicate_title
seocli on-page duplicate-tags --id <task-id> --type duplicate_description
seocli on-page redirect-chains --id <task-id>
seocli on-page resources --id <task-id>
```

**Extract from crawl:** Total pages and error pages (4xx, 5xx); pages blocked by robots.txt (check Googlebot, OAI-SearchBot, PerplexityBot); orphan pages; missing title/meta/H1; duplicate titles/descriptions; redirect chains >2 hops; mixed HTTP/HTTPS; broken links; missing canonicals; thin content (<300 words); keyword density outliers (>3% or <0.5%); invalid schema; spelling errors; image alt text coverage.

### Step 2 — Performance / Lighthouse

Run Lighthouse on homepage + 3–5 key pages (highest internal link count from crawl, or user-specified):

```bash
seocli on-page lighthouse --url "https://example.com/"
```

**Extract:** Performance, Accessibility, Best Practices, SEO scores (flag <80). Core Web Vitals: LCP (<2.5s), CLS (<0.1), INP (<200ms). Top performance opportunities.

### Step 3 — Backlink Health

```bash
seocli backlinks summary --target "example.com"
seocli backlinks bulk-spam-score --targets "example.com"
seocli backlinks referring-domains --target "example.com" --limit 100
seocli backlinks anchors --target "example.com" --limit 50
seocli backlinks bulk-ranks --targets "example.com"
```

**Extract and flag:** Total backlinks and referring domains; domain rank; spam score (>30 concerning, >60 toxic); referring domain diversity ratio; anchor text distribution (>30% exact-match = over-optimisation); top referring domains by authority.

### Step 4 — Keyword Position Snapshot

Use Labs estimates for directional ranking intelligence:

```bash
seocli labs bulk-ranking-keywords --targets "example.com"
seocli labs domain-rank-overview --target "example.com"
seocli labs bulk-traffic-estimation --targets "example.com"
```

Spot-check 5–10 top keywords against live SERPs:

```bash
seocli serp google organic live --keyword "target keyword" --depth 10
```

**Extract:** Estimated organic keywords, traffic, domain rank trend, top keywords by traffic, spot-check calibration.

### Step 5 — AI Visibility Check

```bash
seocli ai-optimization llm-mentions --target "example.com"

# For top 5–10 keywords:
seocli serp google ai-mode live --keyword "target keyword"

# Check llms.txt:
seocli on-page live --url "https://example.com/llms.txt"
```

**Extract and flag:** LLM platform mention count and sentiment; AI Overview presence per keyword; missing llms.txt (easy win).

### Step 6 — On-Page Spot Checks

Analyse the top 20 pages (by internal link count or estimated traffic) from crawl data against the **8-factor on-page rubric**. See [reference/scoring.md](reference/scoring.md) for the full rubric.

Also assess **Content Freshness** (flag pages >12 months without updates) and **E-E-A-T signals** (author credentials, expert quotes, original data, authoritative sources — flag pages where ≥2 of 4 are present).

### Step 7 — Scoring

Score across **5 dimensions** (0–100 each), weighted:

| Dimension            | Weight | Key Data Sources                                                      |
| -------------------- | ------ | --------------------------------------------------------------------- |
| Technical Health     | 30%    | Crawl errors, redirects, page speed, CWV, mobile                      |
| Content Quality      | 25%    | Thin/duplicate content, spelling, keyword density, E-E-A-T, freshness |
| On-Page Optimisation | 20%    | Titles, metas, headings, schema, internal links, alt text             |
| Backlink Profile     | 15%    | Domain rank, referring domains, spam score, anchor distribution       |
| AI Visibility        | 10%    | LLM mentions, AI Overview citations, llms.txt                         |

```
Overall SEO Score = Σ (dimension_score × dimension_weight)
```

**Grade thresholds:** A+ (90–100), A (80–89), B (70–79), C (60–69), D (40–59), F (0–39). See [reference/scoring.md](reference/scoring.md) for detailed scoring methodology.

### Step 8 — Issue Prioritisation

Categorise every issue into four severity tiers:

**Critical** — Blocking indexing/rendering: noindex on important pages, broken redirects to key pages, 5xx errors, missing sitemap, Googlebot blocked, rendering failures.

**Important** — Directly hurting rankings: duplicate content, missing titles on high-traffic pages, thin content on key pages, toxic backlinks (spam >60), slow speed (LCP >4s, CLS >0.25), 3+ hop redirects.

**Opportunity** — Quick wins: missing meta descriptions, missing schema, no llms.txt, orphan pages, missing alt text, no LLM mentions, content needing refresh (>12 months).

**Nice-to-Have** — Marginal gains: spelling errors, suboptimal title length, minor heading hierarchy issues, anchor diversity improvements.

### Step 9 — Report Generation

Generate a Markdown report saved to workspace with:

1. **SEO Health Score** (0–100) with dimensional breakdown
2. **Executive Summary** — 3-sentence diagnosis
3. **Prioritised Issue List** — Critical → Important → Opportunity → Nice-to-Have, each with: issue, affected URLs, severity, fix instructions
4. **Quick Wins** — Top 5–10 highest-impact, lowest-effort fixes
5. **Technical Issues Table**
6. **Backlink Health Summary**
7. **AI Visibility Report**
8. **Performance Summary** — Lighthouse scores and CWV

File naming: `{domain}-audit-{date}.md`

### Forced Reasoning Phase

Before scoring, explicitly document: (1) what's present and healthy, (2) what's missing or broken, (3) what's critical vs cosmetic. This prevents recency bias in scoring. Include as a "Findings Summary" section in the report.

---

## Mode 2: Single-Page Audit

```
FETCH PAGE → PULL SERP → SCORE PAGE → FETCH COMPETITORS → COMPARE → GAP ANALYSIS → REPORT
```

### Step 1 — Instant Page Analysis

```bash
seocli on-page live \
  --url "https://example.com/target-page" \
  --load-resources \
  --validate-micromarkup \
  --check-spell \
  --enable-content-parsing
```

**Extract:** Title, meta description, H1, heading hierarchy, word count, keyword density, schema, canonical, link counts, alt text coverage, speed indicators, mobile rendering.

### Step 2 — SERP Analysis

```bash
seocli serp google organic live --keyword "target keyword" --depth 20
seocli serp google ai-mode live --keyword "target keyword"
```

**Extract:** Top 20 results with URLs/titles/descriptions, SERP features (snippet, PAA, video, images, knowledge panel, AI Overview).

### Step 3 — Score the Target Page

Apply the **8-factor weighted single-page rubric**. See [reference/scoring.md](reference/scoring.md) for full rubric details. Factors: Title Tag (15%), Headers (10%), Content (25%), Keywords (15%), Internal Links (10%), Images (10%), Technical (10%), Meta (5%).

### Step 4 — Competitor Comparison

For the top 3 ranking pages from Step 2:

```bash
seocli on-page live --url "https://competitor.com/page" --enable-content-parsing
seocli backlinks summary --target "https://competitor.com/page"
```

Build a comparison matrix: word count, H2 sections, internal links, backlinks, schema types, page speed.

### Step 5 — Gap Analysis

From the comparison, identify specific gaps with prescriptions:

| Gap Type               | Detection                                    | Example Prescription                                                       |
| ---------------------- | -------------------------------------------- | -------------------------------------------------------------------------- |
| Content Depth          | Word count <50% of avg top 3                 | "Expand from 600 to ~2,500 words. Add sections on [topics]."               |
| Topic Coverage         | H2 topics in top 3 you're missing            | "Add sections: Pricing, Pros & Cons, Alternatives."                        |
| Schema                 | Competitors have structured data, you don't  | "Add FAQ + Article schema."                                                |
| Internal Links         | Count <50% of avg top 3                      | "Add 8–10 internal links from high-authority pages."                       |
| Backlinks              | Referring domains far below competitors      | "Content-level gap. Pursue link-worthy assets."                            |
| Intent/Format Mismatch | 4+ of top 5 are a different content type     | "Reformat to match SERP expectation. This is a format problem, not depth." |
| Freshness              | Older than competitors                       | "Update with current data and statistics."                                 |
| AI Optimisation        | Competitors cited in AI Overview, you aren't | "Add definitions, statistics, numbered lists."                             |

**Intent/Format Mismatch Detection:** Classify top 5 SERP results by content type. If 4+ share a type and your page is different, flag as intent mismatch and elevate priority — this requires reframing, not just expansion.

### Step 6 — Report Generation

1. **Page Audit Score** (0–100) with per-factor breakdown
2. **Competitor Comparison Card** — side-by-side metrics
3. **Gap Analysis** — prioritised fixes with estimated effort
4. **Prescription** — the single most impactful action
5. **Quick Wins** — fixes achievable in under 30 minutes

File naming: `{slug}-page-audit-{date}.md`

---

## Shared Data & Handoff Protocol

### Reads From

- `workspace/seo/config.yaml` — domain, competitors, location
- `workspace/seo/keyword-map.json` — target keywords for spot-checking
- `workspace/seo/audit-history/` — previous audits (reuse/compare)

### Writes To

- `workspace/seo/audit-history/{domain}-{date}.json` — timestamped audit (overall score, dimensional scores, issue counts, top keywords, top quick wins, timestamp)

### Handoff

**Receives from `seo-team-the-researcher`:** keyword-map.json for spot-check targeting.
**Receives from `seo-team-the-general`:** Priority pages/keywords from strategy plan's next_actions.
**Sends to `seo-team-the-writer`:** Pages needing refresh, optimisation, or schema — with specific prescriptions.
**Sends to `seo-team-the-general`:** Audit scores and issue counts for tracking improvement over time.
**Sends to `seo-team-the-researcher`:** Keywords discovered during audit not in the keyword map.

---

## Cost Guardrails

| Guardrail           | Implementation                                                                  |
| ------------------- | ------------------------------------------------------------------------------- |
| Pre-flight estimate | Calculate expected calls, present to user before starting                       |
| Reuse recent crawls | Offer to reuse crawl data <7 days old                                           |
| Batch endpoints     | Use bulk-spam-score, bulk-ranks, bulk-traffic-estimation, bulk-ranking-keywords |
| Progressive depth   | Start with summaries; drill into per-page detail only for flagged issues        |
| Lighthouse sampling | Test 3–5 pages, not all — homepage + highest internal link count                |
| AI check sampling   | Check 5–10 keywords for AI Overview, not the full universe                      |

---

## Reference Files

- **Scoring rubrics and methodology:** [reference/scoring.md](reference/scoring.md)
- **Complete seocli command reference:** [reference/commands.md](reference/commands.md)
