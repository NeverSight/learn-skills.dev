---
name: seo-geo-auditor
description: >
  This skill should be used when the user asks to "audit SEO", "audit GEO",
  "analyze semantic coverage", "find content gaps", "generate fan-out queries",
  "find missing pages", "audit Next.js SEO", "improve internal linking",
  "check schema.org", or mentions "programmatic SEO audit", "semantic coverage",
  "missing pages", "GEO optimization", "AI engine optimization",
  or any command starting with /seo-geo-audit.
---

# SEO/GEO Auditor

Expert SEO and GEO (Generative Engine Optimization) auditor for Next.js sites.
Uses fan-out query methodology to measure semantic coverage and identify content gaps.

## What This Skill Does

Produce a structured audit with 3 scores, fan-out queries grouped by semantic cluster,
gap analysis with specific file paths, and actionable code deltas. Works on any Next.js
site: comparators, SaaS, blogs, e-commerce, directories.

## Core Methodology

### Phase 1: Site Detection

Read the codebase to determine:
- **Thematic**: Main topic/industry (from page content, data files, metadata)
- **Site type**: Comparator, SaaS, blog, e-commerce, directory
- **Architecture**: App Router vs Pages, static vs dynamic, data sources
- **Existing pages**: Route inventory from `app/` directory + `generateStaticParams`

Priority order: read files first (`app/`, `lib/`, `components/`). Use crawl or fetch only when files are insufficient.

### Phase 2: Fan-Out Query Generation

Generate 25-50 realistic search queries that real users would type, grouped by semantic clusters.

**Cluster types by site type:**

| Site Type | Typical Clusters |
|-----------|-----------------|
| Comparator | solutions, vs comparisons, use-cases, company size, features, pricing |
| SaaS | features, alternatives, integrations, use-cases, how-to, pricing |
| Blog | informational, how-to, tools, trends, definitions |
| E-commerce | products, categories, buyer intent, comparisons |

**Volume indicators per query:**
- High: likely >1K searches/month
- Medium: 100-1K/month
- Niche: <100/month but high intent

For detailed methodology, consult `references/fan-out-methodology.md`.

### Phase 3: Scoring & Gaps

Calculate 3 mandatory scores:

1. **GEO Score /100** — How well can AI engines extract and cite the site's content
2. **Fan-Out Coverage %** — Percentage of generated queries covered by existing pages
3. **Next.js SEO Score /100** — Technical SEO implementation quality

For detailed scoring rubrics, consult `references/geo-scoring.md`.

## Output Modes

| Mode | Trigger | Queries | Detail |
|------|---------|---------|--------|
| Standard | default | 25-50 | Balanced: scores, queries, gaps, quick wins, roadmap |
| Express | `--express` | 15-25 | Ultra-concise: scores + top 5 quick wins + 3 pages |
| Deep | `--deep` | 50-80 | Exhaustive: per-page analysis, internal linking map, competitor analysis |

## Output Structure (strict order)

```
## Scores
GEO: XX/100 | Fan-Out: XX% | Next.js SEO: XX/100

## Fan-Out Queries (grouped by cluster, with volume indicators)

## Gaps (each pointing to a specific file path or missing route)

## Quick Wins (<48h, code deltas only)

## Routes to Create (path, title, H1, target queries)

## Templates (FAQ schema, comparison table — if relevant)

## Roadmap (J1-7, J8-30)

## Bonus (1-2 prompts to generate missing content)
```

For a real output example, consult `references/example-output.md`.

## Code Output Rules

- **Deltas only**: Never output complete files — only the diff to apply
- **Actionable**: Every recommendation includes a specific file path or route
- **Copy-paste ready**: Code snippets work as-is when pasted into the project

## Adaptation by Site Type

| Type | Focus |
|------|-------|
| **Comparator / pSEO** | Maximize `generateStaticParams`, cross-comparison pages, FAQ per entity, schema SoftwareApplication |
| **Blog** | Topical clusters, internal linking, schema Article, author pages |
| **SaaS** | Feature pages, /vs/ pages, /for/ pages, FAQ product, schema SoftwareApplication |
| **E-commerce** | Schema Product, category pages, buyer FAQ |

## Next.js Technical Checks

For the full checklist (30+ items), consult `references/nextjs-seo-checklist.md`.

Key checks: `generateMetadata` on every route, `generateStaticParams` for dynamic routes,
`sitemap.ts`, `robots.ts` with AI bot permissions, JSON-LD structured data,
OpenGraph images, `loading.tsx`, next/image optimization.

## Additional Resources

### Reference Files

- **`references/fan-out-methodology.md`** — Fan-out query generation, cluster design, volume estimation
- **`references/geo-scoring.md`** — Detailed scoring rubrics for all 3 scores
- **`references/nextjs-seo-checklist.md`** — Complete Next.js App Router SEO checklist
- **`references/example-output.md`** — Real audit output example (comparator site)
