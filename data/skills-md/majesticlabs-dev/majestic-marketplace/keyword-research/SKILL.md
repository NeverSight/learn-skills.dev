---
name: keyword-research
description: Strategic content planning without expensive tools. 6 Circles Method to find what to write about and prioritize it.
triggers:
  - keyword research
  - content topics
  - what to write about
  - free seo tools
  - topic ideation
  - content planning without tools
  - 6 circles method
allowed-tools: Read Write Edit Grep Glob WebSearch WebFetch mcp__perplexity-ask__perplexity_ask AskUserQuestion
disable-model-invocation: true
---

# Keyword Research Without Expensive Tools

Find content topics and prioritize them using free tools and systematic frameworks.

## Required Input

Ask the user for:
1. **Niche/Industry** - What space are you in?
2. **Target Audience** - Who are you writing for?
3. **Business Goal** - Traffic, leads, sales, authority?
4. **Existing Content** - Do you have a site/blog already?

## The 6 Circles Method

Generate 13 content ideas from a single seed keyword using nested topic clusters.

### Structure

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

### Process

1. **Identify Primary Keyword** - High-traffic, high-intent topic in your niche
2. **Brainstorm 3 Sub-topics** - Related themes that support the primary
3. **Generate 3 Pieces per Sub-topic** - Specific articles addressing aspects of each

### Content Types for Supporting Pieces

| Type | Example |
|------|---------|
| How-to Guide | "How to [achieve outcome] with [method]" |
| Comparison | "[Option A] vs [Option B]: Which is better for [use case]" |
| List Post | "[Number] [adjective] ways to [achieve result]" |
| Case Study | "How [persona] achieved [result] using [approach]" |
| Trend Analysis | "[Topic] trends in [year]: What's changing" |
| Expert Roundup | "[Number] experts share their [topic] strategies" |
| Beginner Guide | "[Topic] for beginners: Everything you need to know" |
| Tool Review | "Best [category] tools for [audience/use case]" |
| Problem-Solution | "Why [problem happens] and how to fix it" |

## Free Tool Arsenal

### Demand Research

| Tool | Use For | How to Access |
|------|---------|---------------|
| **Google Keyword Planner** | Volume ranges, competition | ads.google.com (free account, no spend) |
| **Google Trends** | Seasonality, rising topics | trends.google.com |
| **Ahrefs Free Generator** | 150 suggestions with difficulty | ahrefs.com/keyword-generator |
| **Ubersuggest** | 3 searches/day with metrics | neilpatel.com/ubersuggest |

### Intent Discovery

| Tool | Use For | How to Access |
|------|---------|---------------|
| **Google Autocomplete** | Real-time user queries | Type in Google search bar |
| **People Also Ask** | Question-based content | Scroll down in Google SERP |
| **Answer the Public** | Visual question maps | answerthepublic.com (limited free) |
| **AlsoAsked** | PAA clustering | alsoasked.com (limited free) |

### Community Mining

| Source | What to Extract |
|--------|-----------------|
| **Reddit** | Pain points, questions, terminology |
| **Quora** | Question patterns, answer gaps |
| **Industry Forums** | Niche-specific problems |
| **YouTube Comments** | Objections, confusion points |
| **Amazon Reviews** | Customer language, unmet needs |

## Research Protocol

### Step 1: Seed Generation (50-100 keywords)

```markdown
## Seed Keywords for [Niche]

### From Google Autocomplete
- [keyword] + a-z variations
- "how to [keyword]"
- "best [keyword] for"
- "[keyword] vs"

### From People Also Ask
- [question 1]
- [question 2]
- [question 3]

### From Reddit r/[subreddit]
- Top posts this month: [themes]
- Common questions: [list]
- Pain points mentioned: [list]

### From Answer the Public
- Questions: [list]
- Prepositions: [list]
- Comparisons: [list]
```

### Step 2: Competition Assessment (Manual SERP Analysis)

For each target keyword, analyze top 10 results:

| Signal | What to Look For | Opportunity If... |
|--------|------------------|-------------------|
| **Content Depth** | Word count, comprehensiveness | Top results are thin (<1000 words) |
| **Freshness** | Publication date, last update | Top results are 2+ years old |
| **Format Match** | Does format match intent? | Results don't match searcher need |
| **Authority Gap** | Domain strength of rankers | Small sites ranking (not all big brands) |
| **Content Gaps** | Missing subtopics, unanswered questions | PAA questions not covered |

### Step 3: Prioritization Matrix

Score each keyword 1-10:

| Keyword | Demand | Competition | Intent Fit | Opportunity |
|---------|--------|-------------|------------|-------------|
| [keyword] | [1-10] | [1-10, lower=easier] | [1-10] | Demand - Competition |

**Prioritize:** Opportunity score >3, Intent fit >6

### Sweet Spot Targets

| Site Stage | Monthly Search Volume | Competition Level |
|------------|----------------------|-------------------|
| New site (0-6 months) | 100-500 | Low |
| Growing site (6-18 months) | 500-2,000 | Low-Medium |
| Established site (18+ months) | 1,000-10,000 | Medium |

## Output Format

```markdown
# Keyword Research: [Niche/Topic]

## 6 Circles Content Plan

### Primary Keyword: [keyword]
- Monthly searches: [range]
- Competition: [low/medium/high]
- Intent: [informational/commercial/transactional]

### Sub-topic A: [theme]
1. [Article idea] - [target keyword] - [volume]
2. [Article idea] - [target keyword] - [volume]
3. [Article idea] - [target keyword] - [volume]

### Sub-topic B: [theme]
4. [Article idea] - [target keyword] - [volume]
5. [Article idea] - [target keyword] - [volume]
6. [Article idea] - [target keyword] - [volume]

### Sub-topic C: [theme]
7. [Article idea] - [target keyword] - [volume]
8. [Article idea] - [target keyword] - [volume]
9. [Article idea] - [target keyword] - [volume]

## Prioritized Content Queue

| Priority | Topic | Keyword | Volume | Difficulty | Opportunity |
|----------|-------|---------|--------|------------|-------------|
| 1 | [topic] | [keyword] | [vol] | [1-10] | [score] |
| 2 | [topic] | [keyword] | [vol] | [1-10] | [score] |
| 3 | [topic] | [keyword] | [vol] | [1-10] | [score] |

## Quick Wins (Low Competition, Decent Volume)
- [keyword 1] - [rationale]
- [keyword 2] - [rationale]
- [keyword 3] - [rationale]

## Content Gaps Found
- [gap 1] - competitors missing [what]
- [gap 2] - outdated content on [topic]
- [gap 3] - no good [format] exists for [query]

## Reddit/Community Insights
- Top pain point: [description]
- Common question: [question]
- Terminology used: [terms]

## Next Steps
1. [ ] Create pillar content for [primary keyword]
2. [ ] Write [specific article] targeting [quick win keyword]
3. [ ] Research [sub-topic] deeper for more ideas
```

## Reddit Mining Protocol

### Search Queries
```
site:reddit.com "[niche]" + "how do I"
site:reddit.com "[niche]" + "help"
site:reddit.com "[niche]" + "struggling with"
site:reddit.com "[niche]" + "recommend"
site:reddit.com "[niche]" + "vs"
```

### What to Extract
- **Questions asked repeatedly** → Content opportunities
- **Complaints about existing solutions** → Angle differentiation
- **Terminology and slang** → Keyword variations
- **Recommended resources** → Competitor analysis
- **Upvote patterns** → Topic demand signals

## Integration with Other Skills

| After This Skill | Use For |
|------------------|---------|
| `content-planner` | Detailed outlines for prioritized topics |
| `bofu-keywords` | Bottom-of-funnel conversion keywords |
| `content-calendar` | Scheduling the content queue |
| `content-writer` | Writing the actual content |

## What This Skill Does NOT Do

- Provide exact search volume (use Keyword Planner for ranges)
- Guarantee rankings
- Replace comprehensive SEO audits
- Analyze existing site performance (use Google Search Console)
