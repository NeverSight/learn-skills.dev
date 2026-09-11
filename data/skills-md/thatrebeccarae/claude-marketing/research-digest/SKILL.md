---
name: research-digest
description: "Generate structured research briefs from RSS feeds and web sources on any topic. Synthesizes multiple sources into actionable analysis with key findings, data points, expert perspectives, and content angles."
license: MIT
origin: custom
author: Rebecca Rae Barton
author_url: https://github.com/thatrebeccarae
metadata:
  version: 1.0.0
  category: strategy
  domain: research
  updated: 2026-03-13
  tested: 2026-03-17
  tested_with: "Claude Code v2.1"
---

# Research Digest

Generate structured research briefs from RSS feeds, web sources, and industry publications.

## Install

```bash
git clone https://github.com/thatrebeccarae/claude-marketing.git && cp -r claude-marketing/skills/research-digest ~/.claude/skills/
```

## Core Capabilities

- Pull from RSS feeds, web search, and curated sources
- Assess source credibility and recency
- Cross-reference findings across multiple sources
- Extract trends, data points, and expert opinions
- Identify counter-arguments and nuance
- Produce actionable research briefs

## Workflow

### 1. Source Collection

Gather raw material from:
- **RSS feeds** — industry blogs, news sites, newsletters (via any RSS reader/API)
- **Web search** — targeted queries for recent coverage
- **Industry reports** — analyst reports, whitepapers, earnings calls
- **Social/community** — Reddit, Twitter/X, LinkedIn discussions

### 2. Source Assessment

Evaluate each source on:

| Criterion | Weight | Scale |
|-----------|--------|-------|
| Credibility | 30% | Original research > analysis > aggregation > opinion |
| Recency | 25% | Last 7 days > 30 days > 90 days > older |
| Relevance | 25% | Directly on topic > adjacent > tangential |
| Uniqueness | 20% | Novel data > unique angle > common knowledge |

### 3. Synthesis

- Identify convergent themes (3+ sources saying the same thing)
- Flag divergent views (contradictions between sources)
- Extract specific data points with citations
- Note the "so what" — why this matters for the target audience

### 4. Brief Generation

Produce a structured markdown brief.

## Brief Structure

```markdown
# Research Brief: [Topic]
**Date:** YYYY-MM-DD
**Depth:** Quick scan / Standard / Deep dive
**Sources reviewed:** [count]

## Executive Summary
- [Key finding 1]
- [Key finding 2]
- [Key finding 3]

## Key Findings

### Finding 1: [Headline]
[2-3 paragraph analysis with source citations]

### Finding 2: [Headline]
[2-3 paragraph analysis with source citations]

## Data Points
| Metric | Value | Source | Date |
|--------|-------|--------|------|

## Expert Perspectives
- "[Quote]" — [Name, Title, Source]

## Counter-Arguments & Nuance
- [Opposing view with source]

## Content Angles
- [Angle 1: how to use this research in content]
- [Angle 2]

## Sources
1. [Source name] — [URL] — [Credibility: High/Medium/Low]
```

## Options

| Option | Values | Default |
|--------|--------|---------|
| Time range | 24h, 7d, 30d, 90d | 7d |
| Depth | quick, standard, deep | standard |
| Focus | topic keyword or category | required |
| Output | brief, report, raw-notes | brief |

## Quality Standards

1. **Minimum 3 independent sources** per key finding
2. **Recency bias** toward last 30 days unless historical context is needed
3. **Always include counter-arguments** — at least one contrarian or skeptical view
4. **Separate facts from opinions** — clearly label which is which
5. **Link to original sources** — never cite without attribution
6. **No speculation** — if data is missing, say so rather than guessing

For source credibility framework and synthesis methodology, see [REFERENCE.md](REFERENCE.md).
