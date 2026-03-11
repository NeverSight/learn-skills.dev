---
name: llm-optimized-content
description: Use when creating content that must be discoverable by AI search engines (ChatGPT, Perplexity, Gemini). Use when SEO alone isn't enough, when you need AI citations, or when optimizing for the "zero-click" future.
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# LLM-Optimized Content & GEO

> Create content optimized for AI-powered search using Generative Engine Optimization (GEO) principles.

## Purpose
Create content optimized for both traditional search engines AND AI/LLM-powered search (ChatGPT, Perplexity, Google AI Overviews, Claude) using **Generative Engine Optimization (GEO)** principles.

---

## What is GEO?

**Generative Engine Optimization** = Practices to ensure AI models:
1. **UNDERSTAND** your content
2. Judge it **RELEVANT and RELIABLE**
3. **USE** it to formulate direct responses

**Strategic Importance:** Gartner predicts 25% drop in traditional search volume by 2026. Queries now average 23 words (vs. 4 before).

---

## SEO vs GEO: Critical Difference

| Criteria | SEO (Traditional) | GEO (New Frontier) |
|----------|-------------------|-------------------|
| **Objective** | Rank page on Google SERP | Become the SOURCE in AI response |
| **Metric** | Position on results page | Mention/citation in generated response |
| **Mechanic** | Links, backlinks, domain authority | Language, semantics, contextual relevance |
| **User Result** | Click to your site | Info consumed without click |
| **Optimization** | Keywords, tags, structure | Semantic clarity, E-E-A-T, direct answers |

---

## GEO Optimization Strategies

### 1. Semantic Clarity & Relevance

**Principle:** AI must understand CONTEXT, not just keywords.

**Actions:**
- Dense in MEANING, not just keywords
- Natural vocabulary, no keyword stuffing
- Clear context in first 1-2 sentences
- Define technical terms at first appearance

```
❌ "Our SEO GEO optimization ranking solution"
✅ "GEO (Generative Engine Optimization) optimizes content so AI like
    ChatGPT cites your brand in their responses."
```

### 2. Direct Answers (Answer-First)

**Principle:** Provide key answer at the BEGINNING, not the end.

**Actions:**
- Main answer in 1st paragraph
- Format: "Question → Immediate answer → Development"
- No "teasing" (saving answer for later)

**Optimal Structure:**
```markdown
## [Question]
[Direct answer in 1-2 sentences]

[Detailed development]

[Concrete examples]

[Conclusion/Action]
```

**Example:**
```markdown
## What is ethical copywriting?

Ethical copywriting is a persuasive writing approach that excludes
manipulation and is founded on transparency, honesty, and respect
for the prospect.

[Details follow...]
```

### 3. AI-Parser Optimized Structure

**Principle:** AI favors content that's easy to analyze ("parse").

#### Headers (H1-H6)
- Descriptive and informative (not clickbait)
- Strict logical hierarchy
- Contain keywords naturally

```
✅ "## How to create a landing page that converts?"
❌ "## The secret marketers don't want you to know"
```

#### Bullet Lists
- For enumerations, steps, comparisons
- Preferred over long paragraphs
- Start each item with strong keyword

#### Tables
- For comparisons, specifications, data
- Clear, descriptive headers
- Concise cells

#### Question-Answer Format (FAQ)
- H3 structure for questions
- Immediate answer after
- Ideal for featured snippets AND GEO

### 4. E-E-A-T: Credibility for AI

**E-E-A-T = Expertise + Experience + Authority + Trustworthiness**

#### Expertise
- Demonstrate deep knowledge
- Use precise domain terminology
- Reference research/studies

#### Experience
- First-hand concrete examples
- Real case studies
- Measurable results obtained

#### Authority
- Author bio with credentials
- Citations by recognized experts
- Publications in reference media
- Certifications, awards

#### Trustworthiness
- Cited and dated sources
- Transparency about limits/biases
- Accessible contact and legal notices
- HTTPS, professional design

**Concrete Signals to Integrate:**
```
"According to a [University X] study published in [year]..."
"Based on our analysis of [X] clients over [period]..."
"Source: [URL of official document]"
"Last updated: [date]"
```

### 5. Optimal Length & Depth

**Data:**
- Articles 2000-3000 words = sweet spot for GEO
- But: Quality > Quantity
- Depth on ONE subject > Overview of several

**Ideal GEO Article Structure:**
```
1. Intro with direct answer (100-150 words)
2. Definition/Context (200-300 words)
3. In-depth development (1500-2000 words)
   - Subsections with H2/H3
   - Concrete examples
   - Tables/lists
4. Case studies/Proof (300-500 words)
5. Actionable conclusion (100-150 words)
```

### 6. Freshness & Updates

**Principle:** AI favors RECENT information.

**Actions:**
- Explicitly date content
- Mention "updated on [date]"
- Recent statistics (< 2 years)
- References to relevant current events

### 7. Citation-Friendly Format

**Principle:** Facilitate extraction and citation by AI.

**Techniques:**
- Autonomous sentences (understandable alone)
- Statistics with immediate context
- Clear, concise definitions

```
❌ "That's 37% more."
✅ "Ethical copywriting increases conversion rates by 37% on average
    compared to manipulative approaches."
```

---

## GEO by Content Type

### Blog Articles
- Title = Natural question
- Answer in meta description AND 1st paragraph
- H2 subtitles = Secondary questions
- FAQ at end of article

### Product/Service Pages
- Main benefit in H1 (visualizable + falsifiable)
- Technical specs in table
- Concrete use cases (storytelling)
- Testimonials with context

### Landing Pages
- Clear value proposition in hero
- Sections with descriptive H2s
- Measurable social proof
- FAQ for common objections

---

## Content Structure Template

```markdown
# [H1: Clear Title with Primary Topic]

[Opening paragraph with direct answer to main query]

## Quick Summary
- **What:** [One-line definition]
- **Why it matters:** [Key benefit/importance]
- **Key takeaway:** [Main action or insight]

## Table of Contents
[For posts >1500 words]

## [H2: First Major Section]

[Direct answer/definition first, then elaboration]

### [H3: Supporting Detail]
[Expand with examples, data, explanations]

## [H2: How to [Action]]

1. **Step 1:** [Clear instruction]
   - [Supporting detail]

2. **Step 2:** [Clear instruction]
   - [Supporting detail]

## [H2: Comparison Section] (if applicable)

| Aspect | Option A | Option B |
|--------|----------|----------|
| [Criteria] | [Value] | [Value] |

## Key Takeaways

- [Bullet summary 1]
- [Bullet summary 2]
- [Bullet summary 3]

## Frequently Asked Questions

### [Natural language question]?
[2-3 sentence direct answer]

### [Natural language question]?
[2-3 sentence direct answer]

## Conclusion
[Summary + clear call to action]

---
*Last updated: [Date]*
*Sources: [Citations]*
```

---

## Common Question Patterns to Answer

For any topic, consider addressing:
- **What is [topic]?** → Clear definition
- **How does [topic] work?** → Process explanation
- **Why is [topic] important?** → Benefits/significance
- **How to [action with topic]?** → Step-by-step guide
- **[Topic] vs [alternative]?** → Comparison
- **Best [topic] for [use case]?** → Recommendations
- **How much does [topic] cost?** → Pricing/investment
- **How long does [topic] take?** → Timeline expectations

---

## GEO Checklist

### Structure
- [ ] Descriptive title (not clickbait)
- [ ] Direct answer in first 150 words
- [ ] Informative H2/H3 headers
- [ ] Bullet lists for key points
- [ ] Table for comparisons/data

### Content
- [ ] Dense in meaning (clear context)
- [ ] Autonomous citable sentences
- [ ] Statistics with context
- [ ] Definitions at first mention
- [ ] Concrete examples

### Credibility (E-E-A-T)
- [ ] Cited and dated sources
- [ ] Author bio with expertise
- [ ] First-hand examples
- [ ] Visible publication/update date

### Length
- [ ] 2000-3000 words for main subject
- [ ] Depth > Overview
- [ ] Each section developed

### Technical
- [ ] Descriptive URL
- [ ] Meta description = direct answer
- [ ] Schema markup (if applicable)
- [ ] Images with descriptive alt text

---

## Writing for 3 Audiences

**Simultaneously optimize for:**

1. **Human** → Persuasion, engagement, emotional connection
2. **Ranking Algorithm (SEO)** → Keywords, links, structure
3. **Generation Algorithm (GEO)** → Semantic clarity, E-E-A-T, direct answers

---

## Errors to Avoid

❌ **Keyword stuffing** → AI detects and devalues
❌ **Clickbait headlines** → AI seeks descriptive info
❌ **Superficial content** → AI prefers depth
❌ **Absence of sources** → Trustworthiness questioned
❌ **Unexplained jargon** → Missing context
❌ **Buried answers** → AI scans the beginning

---

## What Claude Does vs What You Decide

| Claude handles | You provide |
|---------------|-------------|
| Applying GEO structure and formatting | Topic expertise and unique insights |
| Creating FAQ sections from content | Validation of accuracy |
| Optimizing for semantic clarity | E-E-A-T signals (credentials, experience) |
| Suggesting citable sentence structures | Source verification and dates |
| Generating comparison tables | Strategic decisions on positioning |

---

## Skill Boundaries

### This skill excels for:
- Blog articles and long-form content
- Product/service pages
- FAQ and knowledge base content
- Landing pages with informational elements

### This skill is NOT ideal for:
- Pure conversion copy → Use copywriting skills
- Technical documentation → Structure matters more than GEO
- Internal communications → No AI discoverability needed

---

## Iteration Guide

| Pass | Focus | Action |
|------|-------|--------|
| **1st** | Structure | Apply GEO template, answer-first format |
| **2nd** | E-E-A-T | Add citations, credentials, dates |
| **3rd** | Citability | Make sentences autonomous and extractable |
| **4th** | Checklist | Run GEO checklist to verify all elements |

---

## Skill Metadata

```yaml
name: llm-optimized-content
category: seo-tools
subcategory: geo
version: 2.0
author: GUIA
source_expert: GEO Framework (Gartner, industry research)
difficulty: intermediate
mode: cyborg
tags: [geo, seo, llm, ai-search, content, perplexity, chatgpt]
created: 2026-01-28
updated: 2026-02-03
```
