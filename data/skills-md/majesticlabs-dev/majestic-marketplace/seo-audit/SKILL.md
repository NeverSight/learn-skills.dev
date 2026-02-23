---
name: seo-audit
description: Run SEO and GEO audits on URLs covering technical SEO, content quality, E-E-A-T signals, and AI citation readiness. Use when evaluating search performance or diagnosing ranking issues.
disable-model-invocation: true
---

# SEO Audit Skill

A comprehensive SEO audit methodology that evaluates content for both traditional search engine optimization and modern AI/LLM visibility (GEO). Informed by Google's multi-stage ranking pipeline.

## When to Use

- Auditing existing content for SEO performance
- Reviewing new content before publication
- Identifying optimization opportunities
- Assessing AI citation readiness
- Evaluating E-E-A-T signals
- Checking technical SEO elements
- Diagnosing why content isn't ranking
- Auditing new domains (sandbox considerations)

## Google's Ranking Pipeline

Content passes through sequential evaluation gates. Understanding this pipeline informs what to audit and why.

```
Mustang → Topicality (T*) → NavBoost → Twiddlers
   ↓           ↓              ↓           ↓
 Initial   Query-match    User clicks   Final
 scoring   relevance      (13 months)   adjustments
```

**Key Implications:**
- Content must pass Mustang's quality gate before relevance even matters
- User behavior (NavBoost) accumulates over 13 months—patience required
- Two foundational pillars: Q* (site quality) and P* (popularity via Chrome data)
- Page potential is capped by domain's `siteAuthority` score

See `assets/google-ranking-signals.yaml` for complete signal reference.

## Audit Framework

### Phase 0: Domain & History Context

Before auditing content, assess domain-level factors that cap page potential:

**Domain Authority Check:**
- [ ] Established domain (>6 months) or new domain sandbox?
- [ ] Site-wide quality signals (clutterScore, ad density)
- [ ] Homepage authority inheritance for new pages
- [ ] Brand entity recognition (`queriesForWhichOfficial`)

**URL History Assessment:**
- [ ] Is this an established URL with history?
- [ ] URL changes reset accumulated trust (Google tracks last 20 versions)
- [ ] Evergreen URL structure (no dates unless news content)
- [ ] URL permanence strategy in place

**Sandbox Awareness (New Domains/Pages):**
| Factor | Status | Impact |
|--------|--------|--------|
| hostAge | New (<6mo) / Established | Domain-level sandbox |
| documentHistory | New URL / Has history | Page-level demotion |
| Graduation signals | Social, backlinks, engagement | Exit sandbox |

**If new domain:** Set realistic expectations. Dual sandbox (host + document) requires consistent quality publishing, backlinks, and positive engagement over months.

### Phase 1: Technical SEO Check

Evaluate foundational technical elements:

**Page-Level Technical:**
- [ ] URL structure (clean, descriptive, <60 chars, evergreen)
- [ ] Title tag (50-60 chars, keyword in first 30) → affects `titlematchScore`
- [ ] Meta description (150-160 chars, compelling CTA)
- [ ] H1 tag (single, matches topic)
- [ ] Header hierarchy (logical H1→H2→H3) → larger text weighted higher
- [ ] Image alt text (descriptive, keyword-relevant)
- [ ] Internal links (contextual, relevant)
- [ ] External links (authoritative sources)

**Site-Level Technical:**
- [ ] HTTPS enabled
- [ ] Mobile-friendly
- [ ] Page speed (<1.8s mobile)
- [ ] Schema markup present
- [ ] XML sitemap inclusion
- [ ] robots.txt accessibility

**Entity & Trust Signals:**
- [ ] Verifiable ownership/authorship (disconnected entity problem)
- [ ] Contact information accessible
- [ ] Organization schema linking to Knowledge Graph

### Phase 2: Content Quality Assessment

Evaluate content depth and value. Google's `contentEffort` signal measures ML-assessed effort invested.

**Content Completeness:**
| Factor | Check | Score | Signal |
|--------|-------|-------|--------|
| Topic coverage | Comprehensive vs. shallow | /10 | contentEffort |
| Unique value | Original insights vs. rehash | /10 | OriginalContentScore |
| Accuracy | Factual, verifiable | /10 | Trust signals |
| Freshness | Current data/sources | /10 | semanticDate |
| Depth | Expert-level detail | /10 | contentEffort |

**Token Truncation Awareness:**
Google uses token limits—long documents may be truncated. Optimize for this:
- [ ] Critical information in first 20% of content (inverted pyramid)
- [ ] Key facts lead each section
- [ ] Paragraphs <120 words
- [ ] Front-load value, don't bury it

**Readability:**
- Reading level (target: Grade 8-10)
- Paragraph length (2-3 sentences ideal)
- Sentence variety
- Scannable formatting (bullets, headers)
- Visual aids (images, tables, diagrams)

**Freshness Audit:**
Google evaluates freshness through three distinct methods:
- [ ] Explicit byline date (visible, accurate)
- [ ] URL date signals (avoid dates in evergreen URLs)
- [ ] Semantic freshness (are facts/sources current, not just timestamp?)

⚠️ **Freshness spam detection:** Changing timestamps without updating substance is detected via `semanticDate` comparison.

### Phase 3: Keyword & Semantic Analysis

Assess keyword optimization. Affects Topicality (T*) stage scoring.

**Primary Keyword:**
- Present in title tag (first 30 chars ideal)
- In H1 and early H2s
- Natural density (0.5-1.5%)
- In meta description
- In first 100 words

**Semantic Coverage:**
- LSI keywords present
- Related entities covered (`webrefEntities` signal)
- Topic cluster alignment
- Question variations addressed
- Search intent match

**Entity Optimization:**
- [ ] Content associates with Knowledge Graph entities
- [ ] Clear entity relationships established
- [ ] Supports topical authority building

### Phase 4: E-E-A-T Evaluation

Assess Experience, Expertise, Authority, Trust signals. These map directly to technical signals.

**Experience Signals:**
- [ ] First-hand experience indicated
- [ ] Case studies/examples included
- [ ] Original data/research
- [ ] Process documentation

**Expertise Signals:** (→ `contentEffort`, `OriginalContentScore`)
- [ ] Author credentials visible
- [ ] Technical accuracy
- [ ] Comprehensive coverage
- [ ] Expert quotes/interviews

**Authority Signals:** (→ `siteAuthority`, `author` attribute)
- [ ] Authoritative external citations
- [ ] Industry recognition
- [ ] Brand mentions
- [ ] Published research

**Trust Signals:**
- [ ] Contact information (disconnected entity fix)
- [ ] Privacy policy
- [ ] Editorial guidelines
- [ ] Reviews/testimonials
- [ ] Security indicators

**Disconnected Entity Check:**
Sites without verifiable ownership, author info, and contact transparency trigger algorithmic distrust—even with high content quality.

### Phase 5: AI/GEO Readiness

Assess content for LLM visibility:

**Extractability:**
- [ ] TL;DR or summary present (first 100 words)
- [ ] Paragraphs <120 words (token limit friendly)
- [ ] Clear topic sentences (lead with facts)
- [ ] Bullet lists for features
- [ ] Tables for comparisons
- [ ] FAQ section present

**Fact-Density:**
- [ ] Statistics with sources
- [ ] Specific numbers/dates
- [ ] Verifiable data points
- [ ] Expert quotes with attribution

**Structure for AI:**
- [ ] Question-based headers
- [ ] Direct answers near top (inverted pyramid)
- [ ] Logical information hierarchy
- [ ] Schema markup (FAQPage, HowTo)

### Phase 6: User Behavior Signals

Google's NavBoost uses 13 months of aggregated click behavior. Audit for "good clicks" potential.

**Click Quality Indicators:**
- [ ] Title/meta accurately represent content (no clickbait)
- [ ] Content matches search intent (dwell time)
- [ ] Clear value proposition visible above fold
- [ ] Low bounce risk (content delivers on promise)

**Engagement Factors:**
| Signal | Status | Improvement |
|--------|--------|-------------|
| Expected dwell time | Low/Med/High | Match intent better |
| Bounce risk | Low/Med/High | Clearer value prop |
| Return visit potential | Low/Med/High | Brand building |

## Output Format

### SEO Audit Report

```markdown
## SEO Audit Report

**Page:** [URL or filename]
**Date:** [Audit date]
**Overall Score:** X/100
**Domain Status:** [Established/New (sandbox considerations)]

### Executive Summary
[2-3 sentence overview including pipeline stage bottlenecks]

### Scores by Category

| Category | Score | Status | Key Signal |
|----------|-------|--------|------------|
| Domain/History | X/10 | [Status] | siteAuthority |
| Technical SEO | X/15 | [Status] | titlematchScore |
| Content Quality | X/25 | [Status] | contentEffort |
| Keyword Optimization | X/10 | [Status] | Topicality |
| E-E-A-T Signals | X/20 | [Status] | Trust signals |
| AI/GEO Readiness | X/10 | [Status] | Extractability |
| User Behavior | X/10 | [Status] | NavBoost |

### Pipeline Bottleneck Analysis
[Which pipeline stage is the primary blocker? Mustang quality? Topicality match? NavBoost signals?]

### Priority Issues (Fix First)

1. **[Issue]** - [Impact] - [Fix] - [Signal affected]
2. **[Issue]** - [Impact] - [Fix] - [Signal affected]
3. **[Issue]** - [Impact] - [Fix] - [Signal affected]

### Domain Context
[Sandbox status, authority inheritance, URL history]

### Technical SEO Findings
[Detailed findings with specific recommendations]

### Content Quality Findings
[contentEffort indicators, token optimization, freshness]

### Keyword Analysis
[Primary keyword performance, semantic gaps, entity coverage]

### E-E-A-T Assessment
[Specific signals present/missing, disconnected entity risk]

### AI Visibility Assessment
[GEO readiness score and improvements]

### User Behavior Optimization
[Click quality, dwell time, engagement improvements]

### Action Plan

**Immediate (This Week):**
- [ ] Action 1
- [ ] Action 2

**Short-term (This Month):**
- [ ] Action 1
- [ ] Action 2

**Ongoing (Sandbox Graduation):**
- [ ] Consistent quality publishing
- [ ] Social signal building
- [ ] Backlink acquisition
- [ ] User engagement optimization
```

## Scoring Guide

**90-100:** Excellent - Minor optimizations only
**70-89:** Good - Some improvements needed
**50-69:** Needs Work - Significant gaps to address
**Below 50:** Critical - Major overhaul required

**New Domain Adjustment:** Subtract 10-15 points for sandbox limitations. Focus on graduation signals.

## Quick Audit Option

For faster audits, focus on:

1. **Domain Context** - Established or sandbox? URL history?
2. **Title & Meta** - Optimized for `titlematchScore`?
3. **Content Quality** - `contentEffort` indicators present?
4. **E-E-A-T** - Disconnected entity risk?
5. **AI Ready** - Inverted pyramid, extractable format?

Deliver top 5 issues with affected signals and fixes.

## Signal Reference

For detailed signal documentation, see:
`assets/google-ranking-signals.yaml`

Key signals to remember:
- `titlematchScore` - Title relevance to query
- `contentEffort` - ML-assessed content investment
- `OriginalContentScore` - Uniqueness (0-512 scale)
- `semanticDate` - Actual freshness of facts/sources
- `siteAuthority` - Domain-level authority cap
- `chromeInTotal` - Popularity via Chrome data
