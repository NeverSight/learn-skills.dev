---
name: aeo-geo-optimizer
description: Answer Engine Optimization (AEO) and Generative Engine Optimization (GEO) specialist. Optimize content and websites to appear in AI-generated answers from ChatGPT, Perplexity, Claude, Google AI Overviews, and other LLM-powered search experiences. Use when the user asks about AI search optimization, AEO, GEO, AI Overviews, appearing in AI answers, LLM citations, or optimizing for generative search.
license: MIT
origin: custom
author: Rebecca Rae Barton
author_url: https://github.com/thatrebeccarae
metadata:
  version: 1.0.0
  category: seo
  domain: ai-search-optimization
  updated: 2026-03-18
  tested: 2026-03-18
  tested_with: "Claude Code v2.1"
---

# AEO/GEO Optimizer

Optimize content and websites for AI-powered search experiences — ChatGPT, Perplexity, Claude, Google AI Overviews, and Bing Copilot.

## Install

```bash
git clone https://github.com/thatrebeccarae/claude-marketing.git && cp -r claude-marketing/skills/aeo-geo-optimizer ~/.claude/skills/
```

## Why This Matters

Traditional SEO optimizes for 10 blue links. AEO/GEO optimizes for AI-generated answers. When someone asks ChatGPT or Perplexity a question, the answer synthesizes from sources — and those sources get cited, linked, and trusted. If your content is not structured for AI consumption, you are invisible in the fastest-growing search channel.

## Core Concepts

### AEO vs GEO vs Traditional SEO

| Dimension | Traditional SEO | AEO (Answer Engine) | GEO (Generative Engine) |
|-----------|----------------|---------------------|------------------------|
| **Target** | Google/Bing SERPs | Featured snippets, AI Overviews, voice assistants | ChatGPT, Perplexity, Claude citations |
| **Goal** | Rank on page 1 | Be THE answer | Be cited in AI-generated responses |
| **Content format** | Long-form, keyword-rich | Concise, structured Q&A | Authoritative, quotable, fact-dense |
| **Signals** | Backlinks, keywords, UX | Schema markup, direct answers, authority | E-E-A-T, data density, citation-worthiness |
| **Measurement** | Rankings, traffic | Answer box appearance, voice search hits | AI citation tracking, brand mentions in AI |

### The Citation Hierarchy

AI models prioritize sources based on:

1. **Authority signals** — Domain authority, author expertise, institutional backing
2. **Content structure** — Clear headings, direct answers, structured data
3. **Freshness** — Recent publication dates, updated statistics
4. **Specificity** — Exact numbers, named sources, verifiable claims
5. **Uniqueness** — Original research, proprietary data, novel frameworks

## AEO/GEO Audit Workflow

### Step 1: Assess Current AI Visibility

1. **Test AI citation presence**: Query ChatGPT, Perplexity, and Google AI Overviews with questions your content should answer. Document which queries cite your content vs competitors.

2. **Check structured data**: Validate schema markup coverage using Google Rich Results Test or Schema.org validator.

3. **Evaluate content structure**: Score each page on AEO readiness using the Content Scorecard below.

### Step 2: Content Scorecard

Rate each piece of content (1-5) on these dimensions:

| Dimension | Score 1 (Poor) | Score 5 (Excellent) |
|-----------|---------------|-------------------|
| **Direct answers** | Buried in paragraphs | Clear Q&A format, first-sentence answers |
| **Data density** | Opinions without evidence | Specific numbers, percentages, dates |
| **Source attribution** | No citations | Named sources, linked studies |
| **Structure** | Wall of text | H2/H3 hierarchy, lists, tables |
| **Schema markup** | None | Article, FAQ, HowTo, or relevant type |
| **Freshness signals** | No dates | Published date, "Updated" date, recent data |
| **Author authority** | No byline | Named author with expertise credentials |
| **Quotability** | Meandering prose | Crisp, self-contained statements AI can extract |

**Scoring**: 32-40 = AI-ready. 24-31 = Needs optimization. Below 24 = Major rework needed.

### Step 3: Optimize for AI Citation

#### Content Structure Patterns

**The Direct Answer Pattern:**
```
## [Question as H2]

[One-sentence direct answer.] [Supporting context in 2-3 sentences.]

**Key details:**
- [Specific data point]
- [Specific data point]
- [Source attribution]
```

**The Definition Pattern:**
```
## What Is [Term]?

[Term] is [clear, concise definition in one sentence]. [Elaboration with context.] [How it differs from related concepts.]
```

**The Comparison Pattern:**
```
## [X] vs [Y]: Key Differences

| Dimension | [X] | [Y] |
|-----------|-----|-----|
| [Aspect 1] | [Specific detail] | [Specific detail] |
| [Aspect 2] | [Specific detail] | [Specific detail] |

**Bottom line:** [One-sentence recommendation with reasoning.]
```

**The Statistics Pattern:**
```
## [Topic] Statistics ([Year])

- **[Stat 1]**: [Number] ([Source, Year])
- **[Stat 2]**: [Number] ([Source, Year])
- **[Stat 3]**: [Number] ([Source, Year])

*Sources: [List with links]*
```

#### Writing for AI Extraction

1. **Lead with the answer.** AI models extract the first sentence after a heading. Make it count.
2. **Use specific numbers.** "Revenue increased 47% year-over-year" beats "revenue increased significantly."
3. **Name your sources.** "According to a 2026 McKinsey report" is citable; unsourced claims are not.
4. **Create self-contained paragraphs.** Each paragraph should make sense extracted in isolation.
5. **Use comparison tables.** AI models love structured comparisons — they are easy to synthesize.
6. **Include "What is" and "How to" headings.** These directly match common AI queries.
7. **Add freshness signals.** Include publication date, last-updated date, and date-stamp your statistics.
8. **Write quotable sentences.** Crisp, declarative statements that AI can extract verbatim.

#### Technical Optimization

1. **Schema markup** — See the schema-markup-generator skill for implementation
2. **Canonical URLs** — Ensure AI models find the authoritative version
3. **XML sitemap** — Keep it current so AI crawlers find new content
4. **Page speed** — AI crawlers respect crawl budgets; fast sites get crawled more
5. **robots.txt** — Ensure AI crawlers (GPTBot, anthropic-ai, PerplexityBot) are not blocked

### Step 4: Monitor AI Visibility

#### AI Crawler User Agents

| Crawler | User Agent | Purpose |
|---------|-----------|---------|
| OpenAI | GPTBot | ChatGPT training and browsing |
| Anthropic | anthropic-ai, ClaudeBot | Claude training and citations |
| Perplexity | PerplexityBot | Perplexity search citations |
| Google | Google-Extended | Gemini/AI Overview training |
| Microsoft | Bingbot (+ AI signals) | Bing Copilot citations |
| Meta | Meta-ExternalAgent | Meta AI features |
| Apple | Applebot-Extended | Apple Intelligence |

#### robots.txt Recommendations

```
# Allow AI crawlers for maximum AI search visibility
User-agent: GPTBot
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /
```

**Decision framework:** If your goal is AI visibility (AEO/GEO), allow all AI crawlers. If you have licensing concerns about training data, selectively block training-only crawlers while allowing search/citation crawlers.

#### Measurement Approaches

| Method | What It Tracks | Tools |
|--------|---------------|-------|
| **Manual citation checks** | Query AI platforms, document citations | ChatGPT, Perplexity, Google |
| **Server log analysis** | AI crawler frequency and pages crawled | Log analyzers, custom scripts |
| **Brand mention monitoring** | Your brand/content mentioned in AI answers | Manual checks, brand monitoring tools |
| **Referral traffic** | Traffic from AI platforms | GA4 (check referral sources for chat.openai.com, perplexity.ai) |
| **Schema validation** | Structured data coverage and errors | Google Search Console, Rich Results Test |

## Content Types and AI Optimization

### Blog Posts / Articles
- Add FAQ schema for common questions
- Structure with clear H2 question headings
- Include "Key Takeaways" or "TL;DR" section
- Date-stamp all statistics

### Product / Service Pages
- Add Product or Service schema
- Include comparison tables vs alternatives
- Answer "What is [product]?" in first paragraph
- List specific features with quantified benefits

### Documentation / How-To Content
- Add HowTo schema with explicit steps
- Number every step
- Include time estimates and difficulty level
- Add "Prerequisites" and "Common Mistakes" sections

### Research / Data Content
- Add Dataset schema where applicable
- Lead with key findings before methodology
- Create a "Key Statistics" summary section
- Cite sample sizes, date ranges, and confidence levels

## Anti-Patterns (Never Do)

1. **Do not block AI crawlers** if your goal is AI visibility
2. **Do not write "click here" or "read more below"** — AI extracts content out of context
3. **Do not bury answers in long introductions** — lead with the answer
4. **Do not use vague qualifiers** — "many," "significant," "some" — use specific numbers
5. **Do not neglect author bylines** — E-E-A-T signals matter to AI models
6. **Do not duplicate content across pages** — AI models deduplicate and may ignore both
7. **Do not over-optimize for one AI platform** — optimize for all of them
8. **Do not forget internal linking** — AI crawlers follow links to build topical authority maps

## Integration with Other Skills

- **technical-seo-audit** — Run technical audit first, then layer AEO/GEO optimization
- **schema-markup-generator** — Generate the structured data this skill recommends
- **seo-content-writer** — Apply AEO writing patterns during content creation
- **content-creator** — Use brand voice analysis to maintain voice while optimizing for AI
