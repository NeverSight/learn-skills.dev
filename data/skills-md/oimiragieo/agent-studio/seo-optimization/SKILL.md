---
name: seo-optimization
description: Comprehensive 7-phase SEO optimization workflow covering technical SEO auditing, keyword research strategy, on-page optimization, content SEO and E-E-A-T, structured data implementation, link building, and AI search optimization. Use when auditing search engine visibility, diagnosing ranking issues, implementing schema markup, conducting keyword research, optimizing content for E-E-A-T signals, or adapting for AI-driven search (AI Overviews, SGE).
version: 1.0.0
license: MIT
invoked_by: agent
user_invocable: false
tools:
  - Read
  - Write
  - Edit
  - Bash
  - WebSearch
  - WebFetch
  - Glob
  - Grep
  - TaskUpdate
  - Skill
agents:
  - marketing-strategist
  - aso-specialist
category: domain-specific
tags:
  - seo
  - search-engine-optimization
  - technical-seo
  - keyword-research
  - on-page-optimization
  - structured-data
  - schema-markup
  - core-web-vitals
  - link-building
  - e-e-a-t
  - content-seo
  - ai-search
  - marketing
  - aso
---

<!-- Agent: developer | Task: #14 | Session: 2026-03-02 -->

# SEO Optimization

Comprehensive 7-phase SEO optimization workflow. Audit search visibility, diagnose ranking issues, implement structured data, and produce actionable optimization recommendations for both traditional and AI-driven search.

## When to Apply

Use this skill when:

- Conducting a full technical SEO audit
- Diagnosing ranking drops or crawlability issues
- Implementing structured data / schema markup for rich results
- Conducting keyword research and building content strategy
- Optimizing on-page elements (title tags, meta descriptions, headers)
- Building topical authority via content clustering
- Evaluating and improving E-E-A-T signals
- Preparing content for AI Overview (SGE) visibility
- Planning or evaluating a link building strategy
- Optimizing App Store listings alongside web SEO (ASO correlation)

## Core Ranking Factors (2025-2026)

| Category  | Factor                          | Weight | Notes                                               |
| --------- | ------------------------------- | ------ | --------------------------------------------------- |
| Technical | Core Web Vitals (LCP, INP, CLS) | High   | Direct ranking signal since 2021                    |
| Technical | Crawlability / indexing         | High   | robots.txt, sitemaps, canonical tags                |
| Technical | HTTPS / security                | Medium | Baseline expectation                                |
| Content   | E-E-A-T signals                 | High   | Critical for YMYL and AI Overview                   |
| Content   | Topical authority               | High   | Hub-and-spoke content clusters                      |
| Content   | Search intent match             | High   | Informational/navigational/commercial/transactional |
| On-Page   | Title tag / H1 / meta           | Medium | Title is primary keyword signal                     |
| Authority | Backlink quality and relevance  | High   | Domain Rating + topical alignment                   |
| AI Search | Structured data / schema        | High   | 57% of SERPs show AI Overviews (2025)               |
| AI Search | Content clarity and structure   | High   | LLMs favor scannable, factual content               |

## 7-Phase SEO Workflow

### Phase 1: Technical SEO Audit

Assess crawlability, indexing, and site health before optimizing content.

**Crawlability Checklist:**

- [ ] `robots.txt` does NOT block JS/CSS (Googlebot renders pages)
- [ ] XML sitemap exists at `/sitemap.xml` with `<lastmod>`, `<changefreq>`, `<priority>`
- [ ] Sitemap submitted to Google Search Console and Bing Webmaster Tools
- [ ] No orphaned pages (all pages reachable via internal links within 3 clicks)
- [ ] Pagination handled with `rel="next"` / `rel="prev"` or via sitemap

**Indexing Checklist:**

- [ ] Canonical tags (`<link rel="canonical" href="...">`) on all pages
- [ ] Duplicate content resolved (trailing slash, `www` vs non-`www`, `http` vs `https`)
- [ ] `noindex` only on pages that should NOT appear in SERPs (thank-you pages, admin)
- [ ] Google Search Console verified and no coverage errors
- [ ] Core Web Vitals reported in Search Console (Page Experience report)

**Core Web Vitals Targets:**

| Metric                 | Good    | Needs Improvement | Poor    |
| ---------------------- | ------- | ----------------- | ------- |
| LCP (loading)          | ≤ 2.5s  | 2.5s–4.0s         | > 4.0s  |
| INP (interactivity)    | ≤ 200ms | 200ms–500ms       | > 500ms |
| CLS (visual stability) | ≤ 0.1   | 0.1–0.25          | > 0.25  |

For deep Core Web Vitals optimization, invoke:

```javascript
Skill({ skill: 'web-perf' });
```

**Diagnosis Tools:**

```bash
# Lighthouse CLI audit
npx lighthouse https://example.com --only-categories=performance,seo --output=json

# Check indexing status
# Search: site:yourdomain.com in Google

# Validate robots.txt
curl https://yourdomain.com/robots.txt

# Check XML sitemap
curl https://yourdomain.com/sitemap.xml
```

### Phase 2: Keyword Research and Strategy

Build a keyword strategy grounded in search intent before optimizing any page.

**Search Intent Classification:**

| Intent Type   | Query Pattern                | Content Type                     |
| ------------- | ---------------------------- | -------------------------------- |
| Informational | "how to", "what is", "guide" | Blog posts, guides, tutorials    |
| Navigational  | Brand name, product name     | Landing pages, product pages     |
| Commercial    | "best", "vs", "review"       | Comparison pages, listicles      |
| Transactional | "buy", "price", "discount"   | Product/category pages, checkout |

**Keyword Research Process:**

1. **Seed keywords**: Start with 3-5 core topics your product/service covers
2. **Expand with long-tail**: Use tools (Ahrefs, SEMrush, Google Keyword Planner) to find related, lower-competition terms
3. **LSI synonyms**: For each primary keyword, identify 3-5 Latent Semantic Indexing variants
4. **Competitor gap analysis**: Find keywords competitors rank for that you don't
5. **Group by topic cluster**: Group related keywords into hub-and-spoke architecture

**Keyword Prioritization Matrix:**

| Priority | Search Volume       | Keyword Difficulty  | Intent Match      |
| -------- | ------------------- | ------------------- | ----------------- |
| P0       | High (1000+/mo)     | Low-Medium (<50 KD) | Exact match       |
| P1       | Medium (100-999/mo) | Medium (<65 KD)     | Strong match      |
| P2       | Low (<100/mo)       | Any                 | Long-tail / niche |

**Content Cluster Architecture:**

```
Pillar Page: "Complete Guide to [Topic]"
├── Cluster: "[Topic] for Beginners"
├── Cluster: "[Topic] Best Practices"
├── Cluster: "[Topic] vs [Alternative]"
├── Cluster: "How to [Specific Action] with [Topic]"
└── Cluster: "[Topic] Pricing and Plans"
```

Internal links: Every cluster page links to pillar; pillar links to all clusters.

### Phase 3: On-Page Optimization

Optimize each page's metadata and content structure for target keywords.

**Per-Page Optimization Checklist:**

- [ ] **Title tag**: Primary keyword near front, unique, ≤ 60 characters
- [ ] **Meta description**: Includes keyword, compelling CTA, 150-160 characters
- [ ] **H1 tag**: Exactly one per page, matches or contains primary keyword
- [ ] **H2/H3 tags**: Logical hierarchy, include secondary keywords naturally
- [ ] **URL**: Short, hyphenated, includes primary keyword, no parameters
- [ ] **First 100 words**: Primary keyword appears in opening paragraph
- [ ] **Image alt text**: Descriptive, includes keyword when contextually natural
- [ ] **Internal links**: 3-5 internal links per page to related content
- [ ] **Outbound links**: 1-2 links to authoritative external sources (Google, Wikipedia, gov, .edu)
- [ ] **Content length**: Matches competitive SERP (run `Skill({ skill: 'ripgrep' })` to audit)

**Title Tag Formula:**

```
Primary Keyword + Secondary Modifier + Brand Name
Example: "SEO Audit Checklist 2025 | YourBrand"
Maximum: 60 characters (avoid truncation in SERPs)
```

**Meta Description Formula:**

```
Action verb + Primary keyword + Key benefit + CTA
Example: "Run a complete SEO audit with our 2025 checklist. Fix technical issues, optimize content, and boost rankings. Free template included."
Maximum: 160 characters
```

### Phase 4: Content SEO and E-E-A-T

Build content that demonstrates Experience, Expertise, Authoritativeness, and Trustworthiness.

**E-E-A-T Signal Checklist:**

- [ ] Author bio pages with credentials, LinkedIn links, publications
- [ ] "About" page with team credentials, company history, contact details
- [ ] Citations to authoritative external sources (studies, government data, official docs)
- [ ] User reviews and testimonials with star ratings
- [ ] Press mentions, awards, certifications listed
- [ ] Privacy Policy and Terms of Service pages
- [ ] Physical address and phone number (especially for local SEO)
- [ ] Last-updated dates on evergreen content
- [ ] Editorial standards / fact-checking process published (for news/medical content)

**YMYL Content (Your Money or Your Life) — Highest E-E-A-T Required:**

YMYL topics: finance, medical, legal, safety, news. These require:

- Named, credentialed author on every page
- Medical/legal/financial review process documented
- Regular content freshness updates
- Expert citations for all factual claims

**Content Quality Framework:**

| Dimension   | Standard                                                        | Check                          |
| ----------- | --------------------------------------------------------------- | ------------------------------ |
| Depth       | Covers topic comprehensively; answers follow-up questions       | Compare to top 5 ranking pages |
| Accuracy    | All factual claims sourced or verifiable                        | Spot-check key claims          |
| Freshness   | Published/updated date visible; outdated data refreshed         | Audit annually                 |
| Readability | Flesch-Kincaid Grade Level ≤ 9 for general audiences            | Run readability tool           |
| Structure   | Headers, bullets, tables; scannable for 8-second attention span | Visual audit                   |
| Uniqueness  | Original research, data, or synthesis; not paraphrased          | Plagiarism check               |

**AI-Generated Content Policy (2025):**

- AI content is acceptable but MUST be reviewed for accuracy, tone, and nuance
- Never publish raw AI output: edit for real examples, expert insights, brand voice
- Disclose AI assistance in editorial process documentation (E-E-A-T signal)
- Use AI to generate outlines and research; add original expert insight manually

### Phase 5: Structured Data Implementation

Implement JSON-LD schema markup to enable rich results and AI Overview eligibility.

**Priority Schema Types:**

| Schema Type                | Use Case            | Rich Result Benefit               |
| -------------------------- | ------------------- | --------------------------------- |
| `Article`                  | Blog posts, news    | Author byline, date in SERP       |
| `Product`                  | E-commerce items    | Price, rating, availability stars |
| `FAQ`                      | Q&A sections        | Expandable Q&A in SERP            |
| `LocalBusiness`            | Physical locations  | Map pack, hours, phone in SERP    |
| `BreadcrumbList`           | Site navigation     | Breadcrumb trail in SERP URL      |
| `Organization`             | Company info        | Knowledge panel, logo             |
| `Review`/`AggregateRating` | Reviews             | Star rating in SERP               |
| `HowTo`                    | Step-by-step guides | Numbered steps in SERP            |
| `Event`                    | Events/webinars     | Event listing in SERP             |

**JSON-LD Template (Article):**

```html
<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "Your Article Title",
    "author": {
      "@type": "Person",
      "name": "Author Name",
      "url": "https://example.com/author/name"
    },
    "publisher": {
      "@type": "Organization",
      "name": "Brand Name",
      "logo": {
        "@type": "ImageObject",
        "url": "https://example.com/logo.png"
      }
    },
    "datePublished": "2025-01-01",
    "dateModified": "2025-06-01",
    "mainEntityOfPage": "https://example.com/article-url",
    "image": "https://example.com/article-image.jpg"
  }
</script>
```

**JSON-LD Template (FAQ):**

```html
<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {
        "@type": "Question",
        "name": "What is [topic]?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Clear, concise answer under 200 words."
        }
      }
    ]
  }
</script>
```

**Validation Tools:**

- Google Rich Results Test: `https://search.google.com/test/rich-results`
- Schema.org Validator: `https://validator.schema.org/`
- Google Search Console > Enhancements > Monitor structured data errors

**Implementation Checklist:**

- [ ] JSON-LD (not Microdata) used for all structured data
- [ ] Schema type matches actual page content (no misleading markup)
- [ ] Required properties for each schema type included
- [ ] Validated with Google Rich Results Test (0 errors)
- [ ] Monitored in Search Console Enhancements report

### Phase 6: Link Building Strategy

Build high-quality backlinks using relevance-first outreach.

**Link Quality Framework:**

| Metric               | Target                                         | Tool                 |
| -------------------- | ---------------------------------------------- | -------------------- |
| Domain Rating (DR)   | ≥ 40 for most link sources                     | Ahrefs               |
| Topical Relevance    | Same or adjacent industry                      | Manual review        |
| Traffic              | Linking page receives organic traffic          | Ahrefs Site Explorer |
| Link Placement       | In-content (not sidebar/footer)                | Manual review        |
| Dofollow vs Nofollow | Prefer dofollow; nofollow still drives traffic | Chrome SEO extension |

**Effective Link Building Tactics (2025):**

1. **Digital PR**: Create data studies, original research, or infographics; pitch to journalists
2. **Guest posting**: Contribute expert articles to industry publications (DR 40+)
3. **Broken link building**: Find broken links on authority sites; suggest your content as replacement
4. **Resource page outreach**: Find "Best Resources for [Topic]" pages; request inclusion
5. **Testimonials**: Write testimonials for tools/services you use; earn links from their testimonials page
6. **HARO/Connectively**: Respond to journalist queries to earn media mentions and links
7. **Competitor backlink analysis**: Identify where competitors earned links; replicate

**Anchor Text Diversity (avoid over-optimization):**

| Anchor Type   | Target % | Example                      |
| ------------- | -------- | ---------------------------- |
| Branded       | 40-50%   | "YourBrand"                  |
| Generic       | 20-25%   | "click here", "learn more"   |
| Partial match | 15-20%   | "SEO tool for agencies"      |
| Exact match   | 5-10%    | "technical SEO audit"        |
| Naked URL     | 5-10%    | "<https://example.com/page>" |

**Anti-Patterns to Avoid:**

- Link farms, PBNs (Private Blog Networks): Google penalty risk
- Paid links without `rel="sponsored"` disclosure: Guidelines violation
- Comment spam: Zero value, potential penalty
- Reciprocal link schemes: Devalued by Google algorithms
- Low-DR, irrelevant sites: Dilutes link profile

### Phase 7: AI Search Optimization

Optimize for AI Overviews, Google SGE, and LLM citation patterns (AI Overviews appear in 57% of SERPs as of 2025).

**AI Overview Eligibility Signals:**

- [ ] Clear, direct answers to specific questions (FAQ format favored)
- [ ] Structured content: `<h2>`/`<h3>` headers, numbered lists, bullet points
- [ ] FAQ schema markup implemented (Phase 5)
- [ ] Page demonstrates E-E-A-T (Phase 4)
- [ ] Page already ranks in top 10 for target query
- [ ] Content is factually accurate with cited sources

**Content Formatting for AI Readability:**

```markdown
# Topic Title (H1)

## What is [Topic]? (H2 — Direct answer format)

[First sentence: direct answer in under 50 words]
[Remaining sentences: expand with context and nuance]

## How to [Do Thing] (H2 — How-to format)

1. Step one: [Action verb + clear instruction]
2. Step two: [Action verb + clear instruction]
3. Step three: [Action verb + clear instruction]

## [Topic] vs [Alternative] (H2 — Comparison format)

[Clear differentiation table]

## Frequently Asked Questions (H2 — FAQ format)

**Q: [Common question?]**
A: [Direct answer under 100 words]
```

**Entity Building for AI Visibility:**

- Establish brand/person entity on Wikipedia (if notable)
- Maintain consistent Name/Address/Phone (NAP) across the web
- Claim Google Business Profile and other directory listings
- Build brand mentions across news, social, and industry sites
- Cross-link between official brand assets (website, YouTube, social profiles)

**Knowledge Panel Optimization:**

- Add `Organization` or `Person` schema to homepage
- Use `sameAs` property to link all official profiles:

```json
{
  "@type": "Organization",
  "name": "YourBrand",
  "sameAs": [
    "https://twitter.com/yourbrand",
    "https://linkedin.com/company/yourbrand",
    "https://en.wikipedia.org/wiki/YourBrand"
  ]
}
```

## SEO Audit Report Template

```markdown
# SEO Audit Report

**Domain:** [target domain]
**Date:** [audit date]
**Auditor:** [agent/team]

## Executive Summary

[2-3 sentences: overall health, critical issues, priority action]

## Technical SEO

### Core Web Vitals

| Metric | Score | Rating                      | Target  |
| ------ | ----- | --------------------------- | ------- |
| LCP    | X.Xs  | GOOD/NEEDS IMPROVEMENT/POOR | ≤ 2.5s  |
| INP    | Xms   | GOOD/NEEDS IMPROVEMENT/POOR | ≤ 200ms |
| CLS    | X.XX  | GOOD/NEEDS IMPROVEMENT/POOR | ≤ 0.1   |

### Crawlability / Indexing

- Indexed pages: [N]
- Coverage errors in Search Console: [N]
- sitemap.xml: [PRESENT/MISSING]
- robots.txt issues: [list or NONE]

## Keyword and Content Analysis

- Primary keywords targeted: [list]
- Pages without title tags: [N]
- Duplicate title tags: [N]
- Missing meta descriptions: [N]
- Pages missing H1: [N]

## Structured Data

- Schema types implemented: [list]
- Rich result errors in Search Console: [N]
- Validation status: [PASS/FAIL]

## Link Profile

- Total backlinks: [N]
- Referring domains: [N]
- Average DR of referring domains: [N]
- Toxic/spammy links: [N]

## Findings (Priority Order)

### P0 (Immediate Action Required)

1. [Finding] — [Impact] — [Recommended Fix]

### P1 (Address This Sprint)

1. [Finding] — [Impact] — [Recommended Fix]

### P2 (Address This Quarter)

1. [Finding] — [Impact] — [Recommended Fix]

## Optimization Roadmap

1. [Action with estimated impact and timeline]
2. [Action with estimated impact and timeline]
3. [Action with estimated impact and timeline]
```

## Enforcement Hooks

Input validated against `schemas/input.schema.json` before execution.
Output contract defined in `schemas/output.schema.json`.

See `hooks/pre-execute.cjs` for pre-execution validation and `hooks/post-execute.cjs` for observability event emission.

## Anti-Patterns

- Do NOT optimize content before completing technical SEO audit — crawl/index issues negate content work
- Do NOT target keywords without analyzing search intent — mismatched intent kills rankings
- Do NOT implement schema markup that misrepresents page content — Google manual action risk
- Do NOT pursue exact-match anchor text aggressively (>10%) — over-optimization penalty risk
- Do NOT use AI-generated content without human review — accuracy and tone issues hurt E-E-A-T
- Do NOT ignore Core Web Vitals on mobile — majority of Google indexing is mobile-first
- Do NOT create individual keyword-stuffed pages — topical clusters outperform thin pages
- Do NOT set `rel="noindex"` to solve duplicate content — use canonical tags instead
- Do NOT skip FAQ schema on Q&A content — missed AI Overview eligibility
- Do NOT use `disallow: /` in robots.txt for pages you want indexed — blocks Googlebot

## Iron Laws

1. **ALWAYS** audit technical SEO (crawlability, indexing, CWV) before content or keyword work — broken technical foundation negates all other effort
2. **NEVER** target a keyword without first classifying search intent — content that mismatches intent cannot rank regardless of quality
3. **ALWAYS** validate structured data with Google Rich Results Test before deploying — invalid schema produces no rich result benefit
4. **NEVER** pursue link building without ensuring on-page fundamentals are in place — links to poorly optimized pages waste link equity
5. **ALWAYS** use JSON-LD for structured data implementation — Google's recommended format over Microdata or RDFa
6. **NEVER** publish AI-generated content without human review for accuracy, E-E-A-T signals, and brand voice — raw AI output fails E-E-a-T standards
7. **ALWAYS** align content to topical clusters rather than isolated keyword pages — Google rewards demonstrated topical authority

## References

- [Google Search Central — Structured Data](https://developers.google.com/search/docs/appearance/structured-data)
- [Google Rich Results Test](https://search.google.com/test/rich-results)
- [Core Web Vitals — web.dev](https://web.dev/vitals/)
- [Google Search Console](https://search.google.com/search-console)
- [Schema.org](https://schema.org/)
- [Google Quality Rater Guidelines (E-E-A-T)](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)
- [WordStream SEO Ranking Factors 2025](https://www.wordstream.com/blog/seo-ranking-factors-2025)
- [Backlinko SEO Best Practices](https://backlinko.com/hub/seo/best-practices)
- Research Report: `.claude/context/artifacts/research-reports/seo-optimization-research-2026-03-02.md`

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

Check for:

- Previous SEO audits run on this domain
- Known CWV issues or structured data errors
- Established keyword strategy or cluster architecture

**After completing:**

- New SEO pattern discovered → Append to `.claude/context/memory/learnings.md`
- Crawl/indexing issue found → Append to `.claude/context/memory/issues.md`
- Keyword strategy decision → Append to `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: Your context may reset. If it's not in memory, it didn't happen.
