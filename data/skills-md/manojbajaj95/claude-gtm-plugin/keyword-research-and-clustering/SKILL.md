---
name: keyword-research-and-clustering
description: Research, expand, and cluster keywords for content strategy. Use when planning content topics, building keyword lists, expanding seed keywords, clustering by topic and intent, or mapping keywords to funnel stages. Triggers on "keyword research," "keyword expansion," "keyword clustering," "content topics," "what to write about," "topic ideation," "content planning," "6 circles method," "seed keywords," "keyword difficulty," "search volume," "intent mapping," "pillar content strategy," or "content calendar planning." For SEO optimization and auditing, see seo-and-aeo-strategy.
---

# Keyword Research & Clustering

Research keywords, expand them systematically, cluster by topic and intent, and prioritize for content strategy — all without expensive tools.

---

## Required Input

Ask the user for:
1. **Niche/Industry** — What space are you in?
2. **Target Audience** — Who are you writing for?
3. **Business Goal** — Traffic, leads, sales, authority?
4. **Existing Content** — Do you have a site/blog already?

---

## The 6 Circles Method

Generate 13 content ideas from a single seed keyword using nested topic clusters.

```
                    ┌─────────────────────┐
                    │   PRIMARY KEYWORD   │  ← 1 pillar topic
                    │   (Largest Circle)  │
                    └─────────────────────┘
                              │
            ┌─────────────────┼─────────────────┐
            ▼                 ▼                 ▼
     ┌───────────┐     ┌───────────┐     ┌───────────┐
     │ Sub-topic │     │ Sub-topic │     │ Sub-topic │  ← 3 supporting themes
     │     A     │     │     B     │     │     C     │
     └───────────┘     └───────────┘     └───────────┘
            │                 │                 │
      ┌─────┼─────┐     ┌─────┼─────┐     ┌─────┼─────┐
      ▼     ▼     ▼     ▼     ▼     ▼     ▼     ▼     ▼
     [1]   [2]   [3]   [4]   [5]   [6]   [7]   [8]   [9]  ← 9 content pieces
```

**Process:**
1. Identify primary keyword — high-traffic, high-intent topic in your niche
2. Brainstorm 3 sub-topics — related themes that support the primary
3. Generate 3 pieces per sub-topic — specific articles addressing aspects of each

### Content Types for Supporting Pieces

| Type | Example |
|------|---------|
| How-to Guide | "How to [achieve outcome] with [method]" |
| Comparison | "[Option A] vs [Option B]: Which is better for [use case]" |
| List Post | "[Number] [adjective] ways to [achieve result]" |
| Case Study | "How [persona] achieved [result] using [approach]" |
| Trend Analysis | "[Topic] trends in [year]: What's changing" |
| Beginner Guide | "[Topic] for beginners: Everything you need to know" |
| Tool Review | "Best [category] tools for [audience/use case]" |
| Problem-Solution | "Why [problem happens] and how to fix it" |

---

## Seed Generation (50–100 Keywords)

### Google Autocomplete & PAA
- Type `[keyword]` + a–z variations
- "how to [keyword]", "best [keyword] for", "[keyword] vs"
- Capture People Also Ask questions from SERP

### Community Mining

| Source | What to Extract |
|--------|-----------------|
| **Reddit** | Pain points, questions, terminology |
| **Quora** | Question patterns, answer gaps |
| **Industry Forums** | Niche-specific problems |
| **YouTube Comments** | Objections, confusion points |
| **Amazon Reviews** | Customer language, unmet needs |

### Reddit Mining Protocol

Search queries:
```
site:reddit.com "[niche]" + "how do I"
site:reddit.com "[niche]" + "help"
site:reddit.com "[niche]" + "struggling with"
site:reddit.com "[niche]" + "recommend"
site:reddit.com "[niche]" + "vs"
```

Extract: Questions asked repeatedly (content opportunities), complaints about existing solutions (angle differentiation), terminology and slang (keyword variations), upvote patterns (demand signals).

---

## Keyword Expansion Techniques

### Modifier Categories

**Question modifiers:**
- What is {keyword} / How to {keyword} / Why {keyword} / When to {keyword}

**Comparative modifiers:**
- {keyword} vs {competitor} / {keyword} alternatives / best {keyword} / {keyword} comparison

**Intent modifiers:**
- {keyword} guide / {keyword} tutorial / {keyword} examples / {keyword} template / buy {keyword} / {keyword} pricing

**Audience modifiers:**
- {keyword} for beginners / {keyword} for {industry} / {keyword} for small business / {keyword} for enterprise

### Expansion Procedure

1. Extract current topic scope and any exclusions
2. Propose expansions: synonyms, related terms, acronyms
3. Add explicit exclusions for common false positives
4. Document "why" for each change
5. Keep query count manageable — merge near-duplicates instead of adding many variations

---

## Free Tool Arsenal

### Demand Research

| Tool | Use For | Access |
|------|---------|--------|
| **Google Keyword Planner** | Volume ranges, competition | ads.google.com (free account) |
| **Google Trends** | Seasonality, rising topics | trends.google.com |
| **Ahrefs Free Generator** | 150 suggestions with difficulty | ahrefs.com/keyword-generator |
| **Ubersuggest** | 3 searches/day with metrics | neilpatel.com/ubersuggest |

### Intent Discovery

| Tool | Use For | Access |
|------|---------|--------|
| **Google Autocomplete** | Real-time user queries | Type in search bar |
| **People Also Ask** | Question-based content | Scroll down in SERP |
| **Answer the Public** | Visual question maps | answerthepublic.com |
| **AlsoAsked** | PAA clustering | alsoasked.com |

---

## Competition Assessment (Manual SERP Analysis)

For each target keyword, analyze top 10 results:

| Signal | What to Look For | Opportunity If... |
|--------|------------------|-------------------|
| **Content Depth** | Word count, comprehensiveness | Top results are thin (<1000 words) |
| **Freshness** | Publication date, last update | Top results are 2+ years old |
| **Format Match** | Does format match intent? | Results don't match searcher need |
| **Authority Gap** | Domain strength of rankers | Small sites ranking (not all big brands) |
| **Content Gaps** | Missing subtopics, unanswered questions | PAA questions not covered |

### Sweet Spot Targets by Site Stage

| Site Stage | Monthly Search Volume | Competition Level |
|------------|----------------------|-------------------|
| New site (0–6 months) | 100–500 | Low |
| Growing site (6–18 months) | 500–2,000 | Low–Medium |
| Established site (18+ months) | 1,000–10,000 | Medium |

---

## Clustering Algorithm

1. **Extract seed topics** — Identify main themes from expanded list
2. **Group by semantic similarity** — Keywords with overlapping meaning
3. **Map intent** — Assign Informational / Commercial / Transactional / Navigational
4. **Identify pillar** — Highest-volume, broadest term = pillar page
5. **Map supporting** — Lower-volume terms support pillar

### Cluster Structure Example

```
PILLAR: "content marketing" (highest volume)
├── CLUSTER: "content marketing strategy" (commercial)
│   ├── content marketing plan template
│   ├── content marketing framework
│   └── how to create content marketing strategy
├── CLUSTER: "content marketing examples" (informational)
│   ├── B2B content marketing examples
│   ├── content marketing case studies
│   └── content marketing success stories
└── CLUSTER: "content marketing tools" (commercial)
    ├── best content marketing tools
    ├── content marketing software
    └── content marketing platforms
```

### Intent Classification

| Signal | Intent |
|--------|--------|
| "what is", "how to", "guide" | Informational |
| "best", "vs", "review", "compare" | Commercial |
| "buy", "price", "discount", brand | Transactional |
| Brand name, specific product | Navigational |

---

## Prioritization Matrix

Score each keyword 1–10:

| Keyword | Demand | Competition | Intent Fit | Opportunity |
|---------|--------|-------------|------------|-------------|
| [keyword] | [1–10] | [1–10, lower=easier] | [1–10] | Demand − Competition |

**Prioritize:** Opportunity score > 3, Intent fit > 6

---

## Output Format

```markdown
# Keyword Research: [Niche/Topic]

## 6 Circles Content Plan

### Primary Keyword: [keyword]
- Monthly searches: [range]
- Competition: [low/medium/high]
- Intent: [informational/commercial/transactional]

### Sub-topic A: [theme]
1. [Article idea] — [target keyword] — [volume]
2. [Article idea] — [target keyword] — [volume]
3. [Article idea] — [target keyword] — [volume]

### Sub-topic B: [theme]
4–6. [...]

### Sub-topic C: [theme]
7–9. [...]

## Prioritized Content Queue

| Priority | Topic | Keyword | Volume | Difficulty | Opportunity |
|----------|-------|---------|--------|------------|-------------|
| 1 | [topic] | [keyword] | [vol] | [1–10] | [score] |

## Quick Wins (Low Competition, Decent Volume)
- [keyword 1] — [rationale]
- [keyword 2] — [rationale]

## Content Gaps Found
- [gap 1] — competitors missing [what]
- [gap 2] — outdated content on [topic]

## Community Insights
- Top pain point: [description]
- Common question: [question]
- Terminology used: [terms]
```

---

## Related Skills

- **seo-and-aeo-strategy** — SEO optimization and AI search visibility
- **content-strategy-and-planning** — Detailed content strategy from keyword research
- **content-creation-and-marketing** — Writing the actual content
- **programmatic-seo** — Building SEO pages at scale from keyword data
