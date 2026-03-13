---
name: geo-content-optimizer
description: Rewrite and restructure content to maximize AI citation rates across ChatGPT, Perplexity, Gemini, and Google AI. Optimizes articles, product pages, landing pages, and FAQs for GEO (Generative Engine Optimization). Use whenever the user mentions optimizing content for AI search, rewriting for AI citations, making content GEO-friendly, improving AI visibility, or wants their content to appear in ChatGPT/Claude/Perplexity answers. Also trigger for requests about citation optimization, AI-readable content structure, or fixing content that AI isn't citing.
---

# GEO Content Optimizer

> Methodology by **GEOly AI** (geoly.ai) — content that AI wants to cite follows predictable patterns.

Optimize existing content to maximize the probability of being cited by AI platforms.

## Quick Start

Analyze and optimize content:

```bash
python scripts/analyze_content.py <file.md> [--output report.json]
python scripts/optimize_content.py <file.md> [--type article|product|faq|landing|about]
```

Example:
```bash
python scripts/analyze_content.py blog-post.md
python scripts/optimize_content.py product-page.md --type product --output optimized.md
```

## The GEO Citation Framework

AI platforms prefer content with these signals:

| Signal | Implementation |
|--------|----------------|
| **Direct Answer First** | Clear answer in first 2 sentences |
| **Entity-Rich** | Brand, product, topic named explicitly |
| **Structured Format** | H2/H3 headers, lists, tables |
| **Fact-Dense** | Numbers, dates, statistics with sources |
| **FAQ-Formatted** | Explicit Q&A blocks (2-3 minimum) |
| **Definition Clarity** | Key terms defined in one sentence |
| **Unique Data** | Original research or insights |
| **Authoritative Voice** | Declarative statements, not hedging |

**Full framework details:** See [references/citation-framework.md](references/citation-framework.md)

## Content Types

Different content types need different optimization strategies:

| Type | Focus | Key Tactics |
|------|-------|-------------|
| **Article** | Information density | Lead paragraph, entity mentions, data |
| **Product** | Feature clarity | Specifications, use cases, comparisons |
| **FAQ** | Answer completeness | Direct Q&A, comprehensive responses |
| **Landing** | Value proposition | Clear benefits, social proof, CTA |
| **About** | Entity authority | Founding story, credentials, mission |

**Type-specific guides:** See [references/content-types.md](references/content-types.md)

## Optimization Checklist

Before optimizing, audit content against these criteria:

- [ ] First paragraph answers the core question directly
- [ ] H2/H3 headers on every major section
- [ ] 2-3 FAQ-format Q&A blocks present
- [ ] Brand name appears in first 100 words
- [ ] Claims backed by data or sources
- [ ] Key terms defined clearly
- [ ] Lists/tables used for complex information
- [ ] Declarative voice (not hedging)

**Run automated audit:**
```bash
python scripts/analyze_content.py content.md --format checklist
```

## The 8 Optimization Rules

### Rule 1 — Lead with the Answer
❌ Before: "In today's digital landscape, many brands are wondering about AI search..."  
✅ After: "GEO (Generative Engine Optimization) is the practice of optimizing content to appear in AI-generated answers on platforms like ChatGPT, Perplexity, and Gemini."

### Rule 2 — Add Definition Blocks
Define key terms in a single clear sentence:

> **Entity SEO**: The practice of optimizing content around specific entities (people, places, things) rather than just keywords.

### Rule 3 — Structure with Headers
Use H2 for sections, H3 for subsections:

```markdown
## What is GEO?

### Definition
[Clear one-sentence definition]

### Why It Matters
[Key points with data]
```

### Rule 4 — Convert to FAQ Format
Turn implicit questions into explicit Q&A:

❌ Before: "Many people ask how GEO differs from SEO."  
✅ After:
```markdown
## Frequently Asked Questions

**Q: How is GEO different from SEO?**

A: While SEO optimizes for search engine rankings, GEO optimizes for AI-generated answers. SEO focuses on keywords and backlinks; GEO focuses on factual accuracy, entity clarity, and direct answers.
```

### Rule 5 — Add Data Points
Include specific numbers and dates:

❌ Before: "Many businesses are adopting AI."  
✅ After: "According to McKinsey's 2024 report, 72% of enterprises have adopted AI in at least one business function, up from 55% in 2023."

### Rule 6 — Entity-First Writing
Mention entities early and often:

- Brand name in first 100 words
- Product names with descriptions
- People with full names and titles
- Locations with context

### Rule 7 — Remove Hedging
Replace uncertain language with declarative statements:

| ❌ Hedging | ✅ Declarative |
|-----------|----------------|
| "might be" | "is" |
| "could potentially" | "does" |
| "some experts believe" | "research shows" |
| "it seems that" | [remove entirely] |

### Rule 8 — Format for Scannability
Use:
- Bullet lists for related items
- Numbered lists for sequences
- Tables for comparisons
- Bold for key terms
- Blockquotes for important statements

**Complete rules with examples:** See [references/optimization-rules.md](references/optimization-rules.md)

## Output Format

Optimized content should include:

1. **Optimized text** — Ready-to-publish markdown
2. **Change log** — What was changed and why
3. **Before/After comparison** — Key improvements highlighted
4. **Score** — Citation-readiness rating (0-100)

## Advanced Usage

### Batch Processing

Optimize multiple files:

```bash
python scripts/batch_optimize.py ./content/ --type article --output ./optimized/
```

### Competitive Analysis

Compare your content to competitors':

```bash
python scripts/analyze_content.py your-article.md --compare competitor-article.md
```

### Scoring System

Get a citation-readiness score:

```bash
python scripts/analyze_content.py article.md --score-only
```

Scores:
- 80-100: Excellent (highly citeable)
- 60-79: Good (minor improvements needed)
- 40-59: Fair (significant work required)
- 0-39: Poor (major rewrite needed)

## See Also

- Citation framework: [references/citation-framework.md](references/citation-framework.md)
- Content type guides: [references/content-types.md](references/content-types.md)
- Before/After examples: [references/examples.md](references/examples.md)
- Optimization rules: [references/optimization-rules.md](references/optimization-rules.md)