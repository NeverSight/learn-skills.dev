---
name: seo
description: >
  Comprehensive SEO analysis for any website or business type. Performs full site
  audits, single-page deep analysis, technical SEO checks (crawlability, indexability,
  Core Web Vitals with INP), schema markup detection/validation/generation, content
  quality assessment (E-E-A-T framework per Dec 2025 update extending to all
  competitive queries), image optimization, sitemap analysis, and Generative Engine
  Optimization (GEO) for AI Overviews, ChatGPT, and Perplexity citations. Analyzes
  AI crawler accessibility (GPTBot, ClaudeBot, PerplexityBot), llms.txt compliance,
  brand mention signals, and passage-level citability. Industry detection for SaaS,
  e-commerce, local business, publishers, agencies. Triggers on: "SEO", "audit",
  "schema", "Core Web Vitals", "sitemap", "E-E-A-T", "AI Overviews", "GEO",
  "technical SEO", "content quality", "page speed", "structured data".
---

# SEO — Universal SEO Analysis Skill

Comprehensive SEO analysis across all industries (SaaS, local services,
e-commerce, publishers, agencies). Orchestrates 12 specialized sub-skills.

## Quick Reference

| Command | What it does |
|---------|-------------|
| `$seo audit <url>` | Full website audit with parallel specialized analyses |
| `$seo page <url>` | Deep single-page analysis |
| `$seo sitemap <url or generate>` | Analyze or generate XML sitemaps |
| `$seo schema <url>` | Detect, validate, and generate Schema.org markup |
| `$seo images <url>` | Image optimization analysis |
| `$seo technical <url>` | Technical SEO audit (8 categories) |
| `$seo content <url>` | E-E-A-T and content quality analysis |
| `$seo geo <url>` | AI Overviews / Generative Engine Optimization |
| `$seo plan <business-type>` | Strategic SEO planning |
| `$seo programmatic [url\|plan]` | Programmatic SEO analysis and planning |
| `$seo competitor-pages [url\|generate]` | Competitor comparison page generation |
| `$seo hreflang [url]` | Hreflang/i18n SEO audit and generation |

## Codex Invocation Notes

- Trigger this skill on natural-language requests such as "run an SEO audit", "analyze this page for SEO", or "validate schema markup".
- Treat the `$...` command examples as operation labels, not required CLI syntax.
- Prefer repository-local outputs and summarize assumptions before running broad crawls.
- For full audits, use Codex multi-agent mode: `spawn_agent` specialists in parallel and `wait` for completion before synthesis.

## Orchestration Logic

When the user requests a full SEO audit, execute in this order:
1. Detect business type (SaaS, local, ecommerce, publisher, agency, other)
2. Run core analyses in parallel where possible: `seo-technical`, `seo-content`, `seo-schema`, `seo-sitemap`, and `seo-images`
3. Aggregate findings into a unified SEO Health Score (0-100)
4. Create a prioritized action plan (Critical → High → Medium → Low)

For individual requests, trigger the corresponding specialized skill directly.

### Multi-Agent Role Mapping (Codex)

- Use `explorer` agents for site discovery and evidence gathering.
- Use `worker` agents for each specialist analysis (`seo-technical`, `seo-content`, `seo-schema`, `seo-sitemap`, `seo-images`).
- Use the `default` agent to reconcile conflicts, compute final scoring, and deliver recommendations.
- Keep delegated tasks independent and bounded (single URL/domain scope per agent unless user asks otherwise).

## Industry Detection

Detect business type from homepage signals:
- **SaaS**: pricing page, /features, /integrations, /docs, "free trial", "sign up"
- **Local Service**: phone number, address, service area, "serving [city]", Google Maps embed
- **E-commerce**: /products, /collections, /cart, "add to cart", product schema
- **Publisher**: /blog, /articles, /topics, article schema, author pages, publication dates
- **Agency**: /case-studies, /portfolio, /industries, "our work", client logos

## Quality Gates

Read `references/quality-gates.md` for thin content thresholds per page type.
Hard rules:
- ⚠️ WARNING at 30+ location pages (enforce 60%+ unique content)
- 🛑 HARD STOP at 50+ location pages (require user justification)
- Never recommend HowTo schema (deprecated Sept 2023)
- FAQ schema only for government and healthcare sites
- All Core Web Vitals references use INP, never FID

## Reference Files

Load these on-demand as needed — do NOT load all at startup:
- `references/cwv-thresholds.md` — Current Core Web Vitals thresholds and measurement details
- `references/schema-types.md` — All supported schema types with deprecation status
- `references/eeat-framework.md` — E-E-A-T evaluation criteria (Sept 2025 QRG update)
- `references/quality-gates.md` — Content length minimums, uniqueness thresholds

## Scoring Methodology

### SEO Health Score (0-100)
Weighted aggregate of all categories:

| Category | Weight |
|----------|--------|
| Technical SEO | 25% |
| Content Quality | 25% |
| On-Page SEO | 20% |
| Schema / Structured Data | 10% |
| Performance (CWV) | 10% |
| Images | 5% |
| AI Search Readiness | 5% |

### Priority Levels
- **Critical**: Blocks indexing or causes penalties (immediate fix required)
- **High**: Significantly impacts rankings (fix within 1 week)
- **Medium**: Optimization opportunity (fix within 1 month)
- **Low**: Nice to have (backlog)

## Sub-Skills

This skill orchestrates 12 specialized sub-skills:

1. **seo-audit** — Full website audit with parallel delegation
2. **seo-page** — Deep single-page analysis
3. **seo-technical** — Technical SEO (8 categories)
4. **seo-content** — E-E-A-T and content quality
5. **seo-schema** — Schema markup detection and generation
6. **seo-images** — Image optimization
7. **seo-sitemap** — Sitemap analysis and generation
8. **seo-geo** — AI Overviews / GEO optimization
9. **seo-plan** — Strategic planning with templates
10. **seo-programmatic** — Programmatic SEO analysis and planning
11. **seo-competitor-pages** — Competitor comparison page generation
12. **seo-hreflang** — Hreflang/i18n SEO audit and generation

## Parallel Analysis Areas

During a full audit, parallelize by analysis area:
- `seo-technical` — Crawlability, indexability, security, CWV
- `seo-content` — E-E-A-T, readability, thin content
- `seo-schema` — Detection, validation, generation
- `seo-sitemap` — Structure, coverage, quality gates
- `seo-images` — Image optimization and media hygiene
