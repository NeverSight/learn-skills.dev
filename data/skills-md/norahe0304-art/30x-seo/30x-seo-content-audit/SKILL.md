---
name: 30x-seo-content-audit
description: >
  Content quality audit for both traditional SEO (E-E-A-T) and AI search
  (citability, structure, authority). Use when user says "content audit",
  "content quality", "E-E-A-T", "AI citability", "content analysis", or
  "is my content good for SEO".
allowed-tools:
  - WebFetch
  - Read
---

# Content Quality Audit

> Check both traditional SEO (E-E-A-T) and AI search (citability)

## Two Dimensions

| Dimension | Goal | Key Metrics |
|-----------|------|-------------|
| **Traditional SEO** | Google rankings | E-E-A-T score, keywords, structure |
| **AI Citability** | ChatGPT/Perplexity citations | Extractability, authority signals, third-party presence |

---

## Part 1: Traditional SEO - E-E-A-T Analysis

## E-E-A-T Framework (updated Sept 2025 QRG)

Read `seo/references/eeat-framework.md` for full criteria.

### Experience (first-hand signals)
- Original research, case studies, before/after results
- Personal anecdotes, process documentation
- Unique data, proprietary insights
- Photos/videos from direct experience

### Expertise
- Author credentials, certifications, bio
- Professional background relevant to topic
- Technical depth appropriate for audience
- Accurate, well-sourced claims

### Authoritativeness
- External citations, backlinks from authoritative sources
- Brand mentions, industry recognition
- Published in recognized outlets
- Cited by other experts

### Trustworthiness
- Contact information, physical address
- Privacy policy, terms of service
- Customer testimonials, reviews
- Date stamps, transparent corrections
- Secure site (HTTPS)

## Content Metrics

### Word Count Analysis
Compare against page type minimums:
| Page Type | Minimum |
|-----------|---------|
| Homepage | 500 |
| Service page | 800 |
| Blog post | 1,500 |
| Product page | 300+ (400+ for complex products) |
| Location page | 500-600 |

> **Important:** These are **topical coverage floors**, not targets. Google has confirmed word count is NOT a direct ranking factor. The goal is comprehensive topical coverage — a 500-word page that thoroughly answers the query will outrank a 2,000-word page that doesn't. Use these as guidelines for adequate coverage depth, not rigid requirements.

### Readability
- Flesch Reading Ease: target 60-70 for general audience

> **Note:** Flesch Reading Ease is a useful proxy for content accessibility but is NOT a direct Google ranking factor. John Mueller has confirmed Google does not use basic readability scores for ranking. Yoast deprioritized Flesch scores in v19.3. Use readability analysis as a content quality indicator, not as an SEO metric to optimize directly.
- Grade level: match target audience
- Sentence length: average 15-20 words
- Paragraph length: 2-4 sentences

### Keyword Optimization
- Primary keyword in title, H1, first 100 words
- Natural density (1-3%)
- Semantic variations present
- No keyword stuffing

### Content Structure
- Logical heading hierarchy (H1 → H2 → H3)
- Scannable sections with descriptive headings
- Bullet/numbered lists where appropriate
- Table of contents for long-form content

### Multimedia
- Relevant images with proper alt text
- Videos where appropriate
- Infographics for complex data
- Charts/graphs for statistics

### Internal Linking
- 3-5 relevant internal links per 1000 words
- Descriptive anchor text
- Links to related content
- No orphan pages

### External Linking
- Cite authoritative sources
- Open in new tab for user experience
- Reasonable count (not excessive)

## AI Content Assessment (Sept 2025 QRG addition)

Google's raters now formally assess whether content appears AI-generated.

### Acceptable AI Content
- Demonstrates genuine E-E-A-T
- Provides unique value
- Has human oversight and editing
- Contains original insights

### Low-Quality AI Content Markers
- Generic phrasing, lack of specificity
- No original insight
- Repetitive structure across pages
- No author attribution
- Factual inaccuracies

> **Helpful Content System (March 2024):** The Helpful Content System was merged into Google's core ranking algorithm during the March 2024 core update. It no longer operates as a standalone classifier. Helpfulness signals are now weighted within every core update — the same principles apply (people-first content, demonstrating E-E-A-T, satisfying user intent), but enforcement is continuous rather than through separate HCU updates.

## AI Citation Readiness (GEO signals)

Optimize for AI search engines (ChatGPT, Perplexity, Google AI Overviews):

- Clear, quotable statements with statistics/facts
- Structured data (especially for data points)
- Strong heading hierarchy (H1→H2→H3 flow)
- Answer-first formatting for key questions
- Tables and lists for comparative data
- Clear attribution and source citations

### AI Search Visibility & GEO (2025-2026)

**Google AI Mode** launched publicly in May 2025 as a separate tab in Google Search, available in 180+ countries. Unlike AI Overviews (which appear above organic results), AI Mode provides a fully conversational search experience with **zero organic blue links** — making AI citation the only visibility mechanism.

**Key optimization strategies for AI citation:**
- **Structured answers:** Clear question-answer formats, definition patterns, and step-by-step instructions that AI systems can extract and cite
- **First-party data:** Original research, statistics, case studies, and unique datasets are highly cited by AI systems
- **Schema markup:** Article, FAQ (for non-Google AI platforms), and structured content schemas help AI systems parse and attribute content
- **Topical authority:** AI systems preferentially cite sources that demonstrate deep expertise — build content clusters, not isolated pages
- **Entity clarity:** Ensure brand, authors, and key concepts are clearly defined with structured data (Organization, Person schema)
- **Multi-platform tracking:** Monitor visibility across Google AI Overviews, AI Mode, ChatGPT, Perplexity, and Bing Copilot — not just traditional rankings. Treat AI citation as a standalone KPI alongside organic rankings and traffic.

**Generative Engine Optimization (GEO):**
GEO is the emerging discipline of optimizing content specifically for AI-generated answers. Key GEO signals include: quotability (clear, concise extractable facts), attribution (source citations within your content), structure (well-organized heading hierarchy), and freshness (regularly updated data). Cross-reference the `seo-geo` skill for detailed GEO workflows.

## Content Freshness

- Publication date visible
- Last updated date if content has been revised
- Flag content older than 12 months without update for fast-changing topics

## Output

### Content Quality Score: XX/100

### E-E-A-T Breakdown
| Factor | Score | Key Signals |
|--------|-------|-------------|
| Experience | XX/25 | ... |
| Expertise | XX/25 | ... |
| Authoritativeness | XX/25 | ... |
| Trustworthiness | XX/25 | ... |

### AI Citation Readiness: XX/100

### Issues Found
### Recommendations

---

## Part 2: AI Citability - Three Pillars

> Source: Princeton GEO Research + Industry Best Practices

### Pillar 1: Structure (Extractability)

AI systems extract paragraphs, not entire pages. Each key claim should stand alone.

| Content Block Type | Use Case | Example |
|-------------------|----------|---------|
| Definition block | "What is X?" | "CRM is software that manages customer relationships..." |
| Steps block | "How to do X?" | "Step 1... Step 2... Step 3..." |
| Comparison table | "X vs Y" | Feature comparison table |
| Pros/cons block | Evaluation queries | "Pros:... Cons:..." |
| FAQ block | Common questions | Q:... A:... |
| Statistics block | Data support | "According to 2025 survey, 73% of users..." |

**Structure Rules**:
- Lead each paragraph with the answer (don't bury it)
- Key paragraphs 40-60 words (optimal AI extraction length)
- Use question format for H2/H3 headings (match user search)
- Use tables for comparisons, lists for steps

### Pillar 2: Authority (Citability)

| Optimization Method | Visibility Boost | How to Do |
|---------------------|:----------------:|-----------|
| Cite sources | +40% | Add authoritative citations and links |
| Add statistics | +37% | Specific numbers + source |
| Expert quotes | +30% | "According to [expert]..." |
| Authoritative tone | +25% | Demonstrate expertise |
| Keyword stuffing | **-10%** | **Reduces AI visibility** |

**Best combination**: Fluency + Statistics = Maximum boost

### Pillar 3: Presence (Third-Party Exposure)

AI doesn't just cite your website, it cites where you appear.

| Platform | AI Citation Share | Action |
|----------|:-----------------:|--------|
| Wikipedia | 7.8% | Ensure brand page is accurate |
| Reddit | 1.8% | Participate in relevant communities |
| YouTube | High | Create video content |
| Review sites | Medium | Keep G2, Capterra updated |
| Quora | Medium | Give in-depth answers to related questions |

---

## Combined Score Output

```
Content Quality Audit Report

1. Traditional SEO Score: XX/100
   - Experience: XX/25
   - Expertise: XX/25
   - Authoritativeness: XX/25
   - Trustworthiness: XX/25

2. AI Citability Score: XX/100
   - Structure Extractability: XX/33
   - Authority Signals: XX/33
   - Third-Party Presence: XX/33

3. Combined Score: XX/100

4. Priority Fixes
   - [Specific recommendations]
```

[PROTOCOL]: Update this header on changes, then check CLAUDE.md
