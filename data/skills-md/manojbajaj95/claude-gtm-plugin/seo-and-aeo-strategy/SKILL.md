---
name: seo-and-aeo-strategy
description: SEO, AEO (Answer Engine Optimization), and GEO strategy for search engines and AI visibility. Triggers on "SEO audit," "technical SEO," "on-page SEO," "AI search optimization," "AEO," "GEO," "AI visibility," "optimize for ChatGPT," "optimize for Perplexity," "AI Overviews," "answer engine optimization," "generative engine optimization," "AI citations," "featured snippets," "meta tags," "schema markup," "search ranking," "content optimization," "E-E-A-T," "structured data," "search console," "SEO health check," "why am I not ranking," "AI search readiness," "backlink strategy," "link building," "domain authority," "programmatic SEO," "SEO at scale," "template-based SEO," "AEO monitoring," "AI search monitoring," "JSON-LD," "rich snippets," "schema.org," "SERP analysis," "search intent," "site architecture," "information architecture," "URL structure," "internal linking," or "navigation." For keyword research, see keyword-research-and-clustering.
---

# SEO & AEO Strategy

Traditional SEO gets pages ranked. AI search optimization (AEO/GEO) gets content **cited**. This skill covers both.

```
SEO  → Rank in traditional search results (blue links)
AEO  → Appear in featured snippets, AI Overviews, voice answers
GEO  → Get cited in generative AI responses (ChatGPT, Claude, Perplexity)
```

**2025 reality:** AI Overviews appear in ~47% of Google searches. 58% of queries end without a click. Optimize for citation, not just ranking.

---

## Initial Assessment

Check for `.claude/product-marketing-context.md` or `.agents/product-marketing-context.md` first. Use existing context; only ask for what's missing.

Before auditing, understand:

1. **Site context** — Type (SaaS, e-commerce, blog), primary SEO goal, priority keywords/topics
2. **Current state** — Known issues, organic traffic level, recent changes or migrations
3. **AI visibility** — Does the brand appear in AI-generated answers today? Checked ChatGPT, Perplexity, Google AI Overviews?
4. **Scope** — Full site vs. specific pages? Technical + on-page + AI, or one focus area?

---

## Technical SEO

### Crawlability

| Check | What to Verify |
|-------|---------------|
| **robots.txt** | No unintentional blocks, sitemap referenced, AI crawlers allowed |
| **XML Sitemap** | Exists, submitted to Search Console, canonical URLs only, < 50K URLs |
| **Site architecture** | Important pages within 3 clicks, logical hierarchy, no orphan pages |
| **Crawl budget** | Parameterized URLs controlled, faceted nav handled, no session IDs in URLs |

### Indexation

- `site:domain.com` check vs. Search Console coverage report
- Verify no `noindex` on important pages
- Check canonical tags (self-referencing on unique pages, HTTP→HTTPS, www consistency)
- Identify redirect chains/loops, soft 404s, duplicate content

### Core Web Vitals & Speed

| Metric | Target | Tool |
|--------|--------|------|
| LCP (Largest Contentful Paint) | < 2.5s | PageSpeed Insights |
| INP (Interaction to Next Paint) | < 200ms | Chrome DevTools |
| CLS (Cumulative Layout Shift) | < 0.1 | WebPageTest |
| TTFB (Time to First Byte) | < 800ms | Search Console |

### Mobile & Security

- Responsive design (not separate m. site), viewport configured, adequate tap targets (48px min)
- HTTPS across entire site, valid SSL, no mixed content, HSTS header

### URL Structure

- Lowercase, hyphen-separated, < 75 characters
- Include target keywords naturally, avoid unnecessary parameters

---

## On-Page SEO

### Title Tags

- 50–60 characters, primary keyword near beginning
- Unique per page, brand name at end (unless homepage)
- Compelling and click-worthy

### Meta Descriptions

- 150–160 characters, include primary keyword
- Clear value proposition with call-to-action, unique per page

### Heading Structure

- Single `<h1>` per page containing primary keyword
- Logical hierarchy (H1 → H2 → H3), no skipped levels
- Descriptive headings (not generic), include keywords naturally

### Image SEO

- Descriptive filenames with keywords, alt text on all images
- Compressed, modern formats (WebP/AVIF), lazy load below-fold
- Responsive images with `width`/`height` attributes

### Internal Linking

- Descriptive anchor text with keywords (not "click here")
- Important pages well-linked, no broken internal links
- Breadcrumb navigation for hierarchy

### Content Quality (E-E-A-T)

| Signal | Implementation |
|--------|---------------|
| **Experience** | First-hand accounts, case studies, original data |
| **Expertise** | Author credentials visible, accurate detailed information |
| **Authoritativeness** | Cited by others, industry credentials, recognized in space |
| **Trustworthiness** | Transparent sourcing, contact info, privacy policy, HTTPS |

---

## AI Search Optimization (AEO/GEO)

### How AI Search Platforms Select Sources

| Platform | Source Selection | Key Factor |
|----------|-----------------|------------|
| **Google AI Overviews** | Strong correlation with traditional rankings | Top 5 organic positions favored |
| **ChatGPT** | Wider range, not just top-ranked | Branded domain authority, recency |
| **Perplexity** | Always cites with links | Authoritative, recent, well-structured |
| **Gemini** | Google index + Knowledge Graph | E-E-A-T signals, structured data |
| **Copilot** | Bing index | Microsoft ecosystem (LinkedIn, GitHub) |
| **Claude** | Brave Search | Factual density, structural clarity |

For detailed platform-specific ranking factors, see [references/platform-ranking-factors.md](references/platform-ranking-factors.md) and [references/platform-algorithms.md](references/platform-algorithms.md).

### The Three Pillars

**1. Structure — Make content extractable**

AI systems extract passages, not pages. Every key claim should work standalone.

- Lead every section with a direct answer (don't bury it)
- Keep key answer passages to 40–60 words (optimal for snippet extraction)
- Use H2/H3 headings that match how people phrase queries
- Tables beat prose for comparisons; numbered lists beat paragraphs for processes

**Inverted pyramid pattern:**
```
┌──────────────────────────────────┐
│  DIRECT ANSWER (1-2 sentences)   │ ← AI extracts this first
├──────────────────────────────────┤
│  KEY FACTS & CONTEXT             │ ← Supporting bullets/data
├──────────────────────────────────┤
│  DETAILED EXPLANATION            │ ← Background, examples
└──────────────────────────────────┘
```

**2. Authority — Make content citable**

The Princeton GEO research (KDD 2024) ranked 9 optimization methods:

| Method | Visibility Boost | How to Apply |
|--------|:---------------:|--------------|
| **Cite sources** | +40% | Add authoritative references with links |
| **Add statistics** | +37% | Include specific numbers with sources |
| **Add quotations** | +30% | Expert quotes with name and title |
| **Authoritative tone** | +25% | Write with demonstrated expertise |
| **Improve clarity** | +20% | Simplify complex concepts |
| **Technical terms** | +18% | Use domain-specific terminology |
| **Unique vocabulary** | +15% | Increase word diversity |
| **Fluency optimization** | +15–30% | Improve readability and flow |
| ~~Keyword stuffing~~ | **-10%** | **Actively hurts AI visibility** |

**Best combination:** Fluency + Statistics = maximum boost. Low-ranking sites benefit even more — up to 115% visibility increase with citations.

For detailed GEO research, see [references/geo-research.md](references/geo-research.md).

**3. Presence — Be where AI looks**

AI systems cite where you appear, not just your site:
- Wikipedia mentions (7.8% of all ChatGPT citations)
- Reddit discussions, YouTube content, Quora answers
- Review sites (G2, Capterra, TrustRadius for B2B SaaS)
- Industry publications and guest posts

### Semantic Triples (Key AEO Technique)

Compact, unambiguous facts AI can't misread. Pattern: `[Subject]` `[specific verb]` `[concrete object]`.

```
✅ "HubSpot CRM syncs contact and company data."
✅ "Lead Scoring assigns priority based on engagement."
❌ "The system helps with various tasks."
❌ "It can do many things for users."
```

### AI Crawler Configuration

Ensure robots.txt allows AI crawlers:

```
User-agent: GPTBot          # OpenAI
Allow: /
User-agent: ChatGPT-User    # ChatGPT browsing
Allow: /
User-agent: PerplexityBot   # Perplexity
Allow: /
User-agent: ClaudeBot        # Anthropic
Allow: /
User-agent: Google-Extended  # Gemini/AI Overviews
Allow: /
```

See [references/ai-crawlers.md](references/ai-crawlers.md) for full configuration.

---

## Structured Data for Search & AI

Schema markup improves AI visibility by 30–40%. Priority types:

| Content Type | Schema | Citation Impact |
|-------------|--------|:---------------:|
| FAQs | `FAQPage` | 2.5x inclusion |
| Articles/Blog | `Article` + Author | 2.2x citations |
| Organization | `Organization` | 2.8x citations |
| How-to content | `HowTo` | Step extraction |
| Products | `Product` | Pricing/features |
| Reviews | `AggregateRating` | Trust signals |
| Breadcrumbs | `BreadcrumbList` | Navigation context |

For full JSON-LD templates, see [references/schema-templates.md](references/schema-templates.md) and [references/schema-for-ai.md](references/schema-for-ai.md).

Validate at [Google Rich Results Test](https://search.google.com/test/rich-results) and [Schema.org Validator](https://validator.schema.org/).

---

## Content Types That Get Cited Most

| Content Type | AI Citation Share | Why AI Cites It |
|-------------|:----------------:|----------------|
| Comparison articles | ~33% | Structured, balanced, high-intent |
| Definitive guides | ~15% | Comprehensive, authoritative |
| Original research/data | ~12% | Unique, citable statistics |
| Best-of/listicles | ~10% | Clear structure, entity-rich |
| Product pages | ~10% | Specific extractable details |
| How-to guides | ~8% | Step-by-step structure |

**Underperformers:** Generic blog posts without structure, thin product pages, gated content, undated content, PDF-only content.

For content templates and patterns, see [references/content-patterns.md](references/content-patterns.md) and [references/content-templates.md](references/content-templates.md).

---

## AEO Measurement

Track these four metrics monthly:

### 1. AI Visibility
Test priority queries across ChatGPT, Perplexity, Gemini, Google AI Overviews. **Target:** Appear in 60%+ of priority queries.

### 2. AI Share of Voice
`Share of Voice = (Your mentions / Total brand mentions) × 100`. **Target:** Match or exceed traditional search market share.

### 3. AI Citations
How often YOUR WEBSITE is the source. **Target:** Cited in 30%+ of relevant queries.

### 4. Referral Demand
Traffic originating in AI but arriving later (brand search after AI mention). Track via post-purchase survey: "How did you first hear about us?"

### Monitoring Tools

| Tool | Coverage | Best For |
|------|----------|----------|
| **Otterly AI** | ChatGPT, Perplexity, AI Overviews | Share of AI voice |
| **Peec AI** | ChatGPT, Gemini, Perplexity, Claude | Multi-platform monitoring |
| **ZipTie** | AI Overviews, ChatGPT, Perplexity | Brand mention + sentiment |
| **HubSpot AEO Grader** | AI visibility audit | Free audit |

### Interpreting Results

| Visibility | Share of Voice | Diagnosis |
|------------|----------------|-----------|
| ↓ Down | ↓ Down | Platform algorithm change (industry-wide) |
| ↓ Down | → Stable | Your content quality declined |
| → Stable | ↓ Down | Competitors improved |
| ↑ Up | ↑ Up | Your AEO strategy is working |

---

## Audit Checklists

### Critical (Fix Immediately)
- [ ] HTTPS enabled, valid SSL
- [ ] robots.txt allows crawling (including AI bots)
- [ ] No `noindex` on important pages
- [ ] Title tags present, unique, with primary keyword
- [ ] Single `<h1>` per page
- [ ] AI crawlers not blocked in robots.txt

### High Priority
- [ ] Meta descriptions present and compelling
- [ ] XML sitemap submitted to Search Console
- [ ] Canonical URLs set correctly
- [ ] Mobile-responsive, Core Web Vitals passing
- [ ] FAQPage schema on FAQ/support pages
- [ ] Article schema with author on blog/guide pages
- [ ] "Last updated" date visible on content

### Medium Priority
- [ ] Internal linking strategy implemented
- [ ] Image alt text on all images
- [ ] Descriptive URLs with keywords
- [ ] Breadcrumb navigation + schema
- [ ] Author bios with credentials
- [ ] Statistics cited with sources
- [ ] Content answers queries in first paragraph

### Ongoing
- [ ] Fix crawl errors in Search Console
- [ ] Update sitemap when content changes
- [ ] Refresh content quarterly (competitive topics)
- [ ] Monitor AI visibility monthly (manual or tools)
- [ ] Check for broken links
- [ ] Track AI share of voice vs. competitors

For complete SEO checklist, see [references/seo-checklist.md](references/seo-checklist.md).

---

## Tools

| Tool | Use |
|------|-----|
| Google Search Console | Monitor indexing, fix issues, track queries |
| Google PageSpeed Insights | Performance + Core Web Vitals |
| Rich Results Test | Validate structured data |
| Lighthouse | Full SEO audit |
| Screaming Frog | Crawl analysis |
| Semrush / Ahrefs | AI Overview tracking, backlinks, content gaps |

See [references/tools-and-apis.md](references/tools-and-apis.md) for API reference.

**Scripts available** in `scripts/`: SEO audit, keyword research, SERP analysis, backlink analysis, competitor gap analysis, autocomplete ideas. See script files for usage.

---

## References

- [references/platform-ranking-factors.md](references/platform-ranking-factors.md) — How each AI platform selects sources
- [references/platform-algorithms.md](references/platform-algorithms.md) — Detailed ranking factors per platform
- [references/geo-research.md](references/geo-research.md) — Princeton GEO research (9 methods)
- [references/content-patterns.md](references/content-patterns.md) — AI-optimized content block templates
- [references/content-templates.md](references/content-templates.md) — Page structure templates for AI
- [references/schema-templates.md](references/schema-templates.md) — JSON-LD schema templates
- [references/schema-for-ai.md](references/schema-for-ai.md) — Schema markup for AI visibility
- [references/ai-crawlers.md](references/ai-crawlers.md) — AI crawler robots.txt configuration
- [references/seo-checklist.md](references/seo-checklist.md) — Complete SEO audit checklist
- [references/aeo-geo-patterns.md](references/aeo-geo-patterns.md) — Content patterns for AI citation
- [references/ai-writing-detection.md](references/ai-writing-detection.md) — AI writing patterns to avoid
- [references/query-research.md](references/query-research.md) — Query research methodology
- [references/tools-and-apis.md](references/tools-and-apis.md) — Tools and API reference
- [references/google-docs-summary.md](references/google-docs-summary.md) — Google documentation summary

## Related Skills

- **keyword-research-and-clustering** — Keyword research, expansion, and topic clustering
- **schema-markup** — Structured data implementation details
- **programmatic-seo** — Building SEO pages at scale
- **competitor-alternatives** — Building comparison pages that get cited
- **content-strategy-and-planning** — Planning what content to create
- **data-and-funnel-analytics** — Measuring SEO/AEO performance
