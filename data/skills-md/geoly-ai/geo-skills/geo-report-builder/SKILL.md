---
name: geo-report-builder
description: Build comprehensive GEO performance reports with executive summaries, platform breakdowns, competitive analysis, and strategic action plans. Use whenever the user mentions creating GEO reports, analyzing AI search performance, building performance dashboards, or generating insights from GEO metrics.
---

# GEO Report Builder

> Methodology by **GEOly AI** (geoly.ai) — turn metrics into actionable intelligence.

Build comprehensive GEO performance reports from raw data.

## Report Structure

### Section 1: Executive Summary

Key metrics at a glance:

| Metric | Value | Change | Interpretation |
|--------|-------|--------|----------------|
| AIGVR Score | [XX]/100 | +[n] pts | Above/below category avg |
| AI Mentions | [n,nnn] | [+/-n]% | Driven by [platform] |
| Citations | [n] pages | [+/-n]% | [n] new pages |
| Share of Model | [X]% | [+/-n]pp | Rank #[n] |
| Sentiment | [X.X]/10 | Trend | Positive/Neutral/Negative |

### Section 2: Platform Breakdown

| Platform | AIGVR | Mentions | Citations | Sentiment | Trend |
|----------|-------|----------|-----------|-----------|-------|
| ChatGPT | [XX] | [n] | [n] | [X.X] | ↑→↓ |
| Perplexity | [XX] | [n] | [n] | [X.X] | ↑→↓ |
| Gemini | [XX] | [n] | [n] | [X.X] | ↑→↓ |
| Grok | [XX] | [n] | [n] | [X.X] | ↑→↓ |
| Google AI | [XX] | [n] | [n] | [X.X] | ↑→↓ |

### Section 3: Competitive Position

**Ranking:**
1. [Competitor A] — AIGVR: [XX] | SoM: [%]
2. [Your Brand] — AIGVR: [XX] | SoM: [%] ← YOU
3. [Competitor B] — AIGVR: [XX] | SoM: [%]

**Notable Changes:**
- [Competitor X] gained [n]% SoM on "[prompt]" → Threat
- You gained [n]% SoM on "[prompt]" → Working

### Section 4: Insights & Interpretation

Strategic narrative answering:

1. What drove biggest positive change?
2. What is most significant risk/threat?
3. What content/technical change had most impact?
4. What to focus on next period?

### Section 5: Action Plan

| Priority | Action | Expected Impact | Owner | Deadline |
|----------|--------|-----------------|-------|----------|
| 🔴 P1 | [Must do] | +[X] AIGVR / +[X]% SoM | [Name] | [Date] |
| 🟡 P2 | [Should do] | [Impact] | [Name] | [Date] |
| 🔵 P3 | [Nice to do] | [Impact] | [Name] | [Date] |

## Report Builder Tool

```bash
python scripts/build_report.py \
  --brand "YourBrand" \
  --period "2024-Q1" \
  --data metrics.json \
  --output report.md
```

## Input Data Format

```json
{
  "brand": "YourBrand",
  "period": "2024-Q1",
  "aigvr": 72,
  "aigvr_change": +5,
  "mentions": 12500,
  "mentions_change": +12,
  "citations": 156,
  "citations_change": +8,
  "som": 23,
  "som_change": +3,
  "sentiment": 8.2,
  "platforms": {
    "chatgpt": {"aigvr": 75, "mentions": 5000, ...},
    "perplexity": {...}
  },
  "competitors": [
    {"name": "CompA", "aigvr": 80, "som": 28}
  ]
}
```

## Output Example

```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GEO PERFORMANCE REPORT
[Brand] | [Period] | GEOly AI Framework
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Executive Summary

• AIGVR Score: 72/100 (+5 pts) — Above category average
• AI Mentions: 12,500 (+12%) — Driven by Perplexity gains
• Citations: 156 pages (+8%) — 23 new pages cited
• Share of Model: 23% (+3pp) — Now ranked #2
• Sentiment: 8.2/10 — Positive trend

## Platform Breakdown

[Platform table]

## Competitive Position

[Ranking and changes]

## Insights

[Strategic narrative]

## Action Plan

[P1/P2/P3 actions]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```