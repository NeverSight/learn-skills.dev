---
name: news-sentiment-engine
description: Multi-source RSS news aggregation with Claude-powered sentiment analysis and structured briefing output
category: research
risk: critical
source: community
source_repo: tellmefrankie/news-engine
source_type: community
date_added: "2026-05-13"
author: tellmefrankie
tags: [news, rss, sentiment-analysis, briefing, research]
tools: [claude, websearch]
plugin:
  targets:
    codex: blocked
    claude: blocked
---
# News Sentiment Engine

Collect and analyze AI/tech news from multiple sources with Claude-powered sentiment analysis. Open source lite version.

## When to Use

- Use when preparing a concise AI or technology news briefing from multiple RSS sources.
- Use when you need ranked article summaries with sentiment, tags, and impact scoring.
- Use when monitoring industry changes across product launches, policy moves, and infrastructure shifts.
- Use when deduplicating overlapping coverage before writing a daily or weekly briefing.

## What it does

- Collects news from 4+ RSS feeds (TechCrunch, The Verge, Ars Technica, Hacker News)
- Deduplicates articles across sources
- Ranks by importance (industry impact, technology trends, policy changes)
- Generates structured briefing with sentiment tags
- Outputs formatted briefing card

## Usage

```
Collect latest AI/tech news from RSS feeds.
Rank top 5 by importance to the tech industry.
For each: summary (2-3 sentences), sentiment (positive/negative/neutral),
impact score (1-5), industry tags, one-sentence commentary.
Output as a structured briefing card.
```

## Example Output

```
Illustrative briefing format — not a news claim

1. [Verified article title]
   Source: [publisher and direct URL] | Published: [date] | Event: [date]
   Tags: [relevant topics]
   Sentiment: [interpretation with uncertainty]
   Summary: [source-supported facts]
   Commentary: [clearly labeled inference and evidence]

```

## Output Format

For each article:
- Title + source + publish date
- Summary (2-3 sentences)
- Industry tags: [AI, Semiconductor, Cloud, etc.]
- Sentiment: Positive/Negative/Neutral
- Impact score: 1-5
- Commentary: 1-sentence industry perspective

## Setup

The optional setup below clones and runs a third-party Node project from
`tellmefrankie/news-engine`. Review and pin that repository yourself before
running it, and do not expose API keys to an unreviewed checkout.

```bash
git clone https://github.com/tellmefrankie/news-engine
cd news-engine
pnpm install --ignore-scripts
# Configure a private gitignored credential file only if absent; preserve existing values.
# Requires: ANTHROPIC_API_KEY
pnpm dev -- --collect-only
```

Provider analysis can incur charges; verify current service pricing and quotas. This AAS guide does not bundle the external collector or engine.

## Limitations

- RSS feeds can lag, disappear, throttle, or duplicate syndicated coverage.
- Sentiment and impact scores are briefing aids, not authoritative market or policy analysis.
- The example setup runs third-party code; review the repository and environment variables before use.
- Outputs should be cross-checked against original article sources before publication or investment use.

## Source and interpretation

Commercial offers and operational volume claims in upstream marketing are not independently verified here. Compare publish and event dates, deduplicate at event level and corroborate material claims with primary sources. Sentiment and importance depend on the chosen audience/rubric; they are not investment-grade predictions. Scheduling or message delivery requires the user's corresponding authorization.
