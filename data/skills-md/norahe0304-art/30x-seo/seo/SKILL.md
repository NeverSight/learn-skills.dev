---
name: seo
description: >
  Master SEO orchestrator with 23 specialized sub-skills across 8 categories.
  Comprehensive SEO analysis for any website or business type. Performs full site
  audits, single-page deep analysis, technical SEO checks (crawlability, indexability,
  Core Web Vitals with INP), schema markup, content quality (E-E-A-T framework),
  image optimization, sitemap analysis, site architecture planning, AI search
  optimization (GEO for ChatGPT, Perplexity, AI Overviews), backlink analysis,
  keyword research, SERP tracking, and AI visibility monitoring.
  Industry detection for SaaS, e-commerce, local business, publishers, agencies.
  Triggers on: "SEO", "audit", "schema", "Core Web Vitals", "sitemap", "E-E-A-T",
  "AI Overviews", "GEO", "technical SEO", "content quality", "page speed",
  "structured data", "site architecture", "metadata", "AI SEO", "backlinks",
  "link building", "keywords", "keyword research", "SERP", "AI visibility".
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
---

# SEO — Master Orchestrator (23 Sub-Skills)

[PROTOCOL]: Update this header on changes

Comprehensive SEO analysis across all industries (SaaS, local services,
e-commerce, publishers, agencies). Orchestrates **23 specialized sub-skills**
organized in 8 categories, plus 6 parallel subagents for audits.

---

## Quick Reference

### 1. Audit
| Command | What it does |
|---------|-------------|
| `/seo page <url>` | Deep single-page analysis: title, meta, headings, links, images, Schema, E-E-A-T |
| `squirrelscan audit <url>` | Full-site 230+ rules audit via CLI (`npm i -g squirrelscan`) |

### 2. Technical SEO
| Command | What it does |
|---------|-------------|
| `/seo technical <url>` | 8-category audit: crawl, index, security, URLs, mobile, CWV, structured data, JS |
| `/seo sitemap <url>` | Validate XML sitemaps, detect issues, generate new ones |
| `/seo hreflang <url>` | Multi-language SEO: self-refs, return tags, x-default, ISO codes |
| `/seo schema <url>` | Detect, validate, generate JSON-LD structured data |
| `/seo geo-technical <url>` | AI crawler management: GPTBot, ClaudeBot, llms.txt, SSR check |

### 3. Links
| Command | What it does |
|---------|-------------|
| `/seo internal-links <url>` | Orphan pages, click depth, anchor text, link equity |
| `/seo backlinks profile <domain>` | Backlink profile analysis *(DataForSEO)* |
| `/seo backlinks gap <domain> <competitor>` | Find link gap opportunities *(DataForSEO)* |
| `/seo redirects <url>` | Chains, loops, 301/302 mix, protocol issues, trailing slashes |

### 4. Content
| Command | What it does |
|---------|-------------|
| `/seo content-audit <url>` | E-E-A-T scoring + AI citability analysis |
| `/seo images <url>` | Alt text, file sizes, formats (WebP/AVIF), lazy loading, CLS |
| `/seo content-decay <url>` | Detect declining content, recommend refresh priorities |
| `/seo cannibalization <domain>` | Find keyword conflicts between pages |
| `/seo content-brief <keyword>` | Analyze SERP top 10, generate content briefs |
| `/seo content-writer` | SEO + AI optimized writing guidelines |

### 5. Planning
| Command | What it does |
|---------|-------------|
| `/seo plan <business-type>` | Competitor analysis, keyword strategy, content calendar, 4-phase roadmap |
| `/seo architecture <url>` | URL structure, navigation design, internal linking strategy |

### 6. Programmatic SEO
| Command | What it does |
|---------|-------------|
| `/seo programmatic plan` | Scale content: data sources, templates, quality gates, index control |
| `/seo competitor-pages generate` | X vs Y comparisons, alternatives pages, feature matrices |

### 7. Monitoring
| Command | What it does |
|---------|-------------|
| `/seo monitor overview` | Monitor your site: rankings, clicks, CTR, position changes *(GSC)* |
| `/seo serp check <keyword>` | Live SERP check for any keyword *(DataForSEO)* |
| `/seo ai-visibility domain <domain>` | Track mentions in ChatGPT, Claude, Perplexity, AI Overview *(DataForSEO)* |

### 8. Data
| Command | What it does |
|---------|-------------|
| `/seo keywords research <seed>` | Ideas, volume, difficulty, intent, trends *(DataForSEO)* |
| `/seo keywords site <domain>` | Keywords a site ranks for *(DataForSEO)* |
| `/seo keywords gap <domain> <competitor>` | Find keyword opportunities *(DataForSEO)* |

---

## Command → Skill Routing

| Command | Loads Skill |
|---------|-------------|
| `page` | 30x-seo-page |
| `technical` | 30x-seo-technical |
| `sitemap` | 30x-seo-sitemap |
| `hreflang` | 30x-seo-hreflang |
| `schema` | 30x-seo-schema |
| `geo-technical` | 30x-seo-geo-technical |
| `internal-links` | 30x-seo-internal-links |
| `backlinks` | 30x-seo-backlinks |
| `redirects` | 30x-seo-redirects |
| `content-audit` | 30x-seo-content-audit |
| `images` | 30x-seo-images |
| `content-decay` | 30x-seo-content-decay |
| `cannibalization` | 30x-seo-cannibalization |
| `content-brief` | 30x-seo-content-brief |
| `content-writer` | 30x-seo-content-writer |
| `plan` | 30x-seo-plan |
| `architecture` | 30x-seo-architecture |
| `programmatic` | 30x-seo-programmatic |
| `competitor-pages` | 30x-seo-competitor-pages |
| `monitor` | 30x-seo-monitor |
| `serp` | 30x-seo-serp |
| `ai-visibility` | 30x-seo-ai-visibility |
| `keywords` | 30x-seo-keywords |

---

## Orchestration Logic

When user invokes `/seo audit`, delegate to subagents in parallel:
1. Detect business type (SaaS, local, ecommerce, publisher, agency, other)
2. Spawn subagents: technical, content, schema, sitemap, performance, visual
3. Collect results and generate unified report with SEO Health Score (0-100)
4. Create prioritized action plan (Critical → High → Medium → Low)

---

## Industry Detection

Detect business type from homepage signals:
- **SaaS**: pricing page, /features, /integrations, /docs, "free trial", "sign up"
- **Local Service**: phone number, address, service area, "serving [city]", Google Maps embed
- **E-commerce**: /products, /collections, /cart, "add to cart", product schema
- **Publisher**: /blog, /articles, /topics, article schema, author pages, publication dates
- **Agency**: /case-studies, /portfolio, /industries, "our work", client logos

---

## Quality Gates

Hard rules:
- WARNING at 30+ location pages (enforce 60%+ unique content)
- HARD STOP at 50+ location pages (require user justification)
- Never recommend HowTo schema (deprecated Sept 2023)
- FAQ schema only for government and healthcare sites
- All Core Web Vitals references use INP, never FID

---

## Scoring Methodology

### SEO Health Score (0-100)

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
- **Critical**: Blocks indexing or causes penalties (immediate fix)
- **High**: Significantly impacts rankings (fix within 1 week)
- **Medium**: Optimization opportunity (fix within 1 month)
- **Low**: Nice to have (backlog)

---

## Sub-Skills (23 Total, 8 Categories)

### 1. Audit (1 skill + CLI)
| Skill | What it does |
|-------|-------------|
| **30x-seo-page** | Deep single-page analysis |
| **squirrelscan** *(CLI)* | Full-site 230+ rules audit |

### 2. Technical SEO (5 skills)
| Skill | What it does |
|-------|-------------|
| **30x-seo-technical** | 8-category technical audit |
| **30x-seo-sitemap** | Sitemap validation and generation |
| **30x-seo-hreflang** | International SEO / hreflang |
| **30x-seo-schema** | Schema.org JSON-LD |
| **30x-seo-geo-technical** | AI crawler management |

### 3. Links (3 skills)
| Skill | What it does |
|-------|-------------|
| **30x-seo-internal-links** | Internal link analysis |
| **30x-seo-backlinks** | Backlink profile *(DataForSEO)* |
| **30x-seo-redirects** | Redirect chain analysis |

### 4. Content (6 skills)
| Skill | What it does |
|-------|-------------|
| **30x-seo-content-audit** | E-E-A-T + AI citability |
| **30x-seo-images** | Image optimization |
| **30x-seo-content-decay** | Content freshness analysis |
| **30x-seo-cannibalization** | Keyword conflict detection |
| **30x-seo-content-brief** | SERP-based content briefs |
| **30x-seo-content-writer** | SEO writing guidelines |

### 5. Planning (2 skills)
| Skill | What it does |
|-------|-------------|
| **30x-seo-plan** | Strategic SEO planning |
| **30x-seo-architecture** | Site structure planning |

### 6. Programmatic SEO (2 skills)
| Skill | What it does |
|-------|-------------|
| **30x-seo-programmatic** | Scale content with templates |
| **30x-seo-competitor-pages** | X vs Y comparison pages |

### 7. Monitoring (3 skills)
| Skill | What it does |
|-------|-------------|
| **30x-seo-monitor** | Your site via GSC |
| **30x-seo-serp** | Any site via DataForSEO |
| **30x-seo-ai-visibility** | AI search visibility |

### 8. Data (1 skill)
| Skill | What it does |
|-------|-------------|
| **30x-seo-keywords** | Keyword research *(DataForSEO)* |

---

## Dependencies

| Category | Skills | Dependency |
|----------|--------|------------|
| Audit | 1 | WebFetch |
| Technical SEO | 5 | WebFetch |
| Links | 3 | WebFetch + DataForSEO (backlinks) |
| Content | 6 | WebFetch |
| Planning | 2 | WebFetch |
| Programmatic SEO | 2 | WebFetch |
| Monitoring | 3 | GSC + DataForSEO |
| Data | 1 | DataForSEO |

**18 skills work without any API. 4 skills require DataForSEO. 1 skill requires Google Search Console.**

---

## Subagents

For parallel analysis during audits:
- `seo-technical` — Crawlability, indexability, security, CWV
- `seo-content` — E-E-A-T, readability, thin content
- `seo-schema` — Detection, validation, generation
- `seo-sitemap` — Structure, coverage, quality gates
- `seo-performance` — Core Web Vitals measurement
- `seo-visual` — Screenshots, mobile testing, above-fold
