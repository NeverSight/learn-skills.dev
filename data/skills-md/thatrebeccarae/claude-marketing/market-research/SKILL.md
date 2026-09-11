---
name: market-research
description: "Generate comprehensive market research reports (50+ pages) in the style of top consulting firms (McKinsey, BCG, Gartner). Professional LaTeX formatting, strategic analysis frameworks (Porter's Five Forces, PESTLE, SWOT, TAM/SAM/SOM, BCG Matrix), and deep research integration."
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

# Market Research

Consulting-grade market research reports with professional formatting and strategic analysis frameworks.

## Install

```bash
git clone https://github.com/thatrebeccarae/claude-marketing.git && cp -r claude-marketing/skills/market-research ~/.claude/skills/
```

## Core Capabilities

- **Porter's Five Forces** — competitive intensity analysis
- **PESTLE Analysis** — macro-environmental scanning
- **SWOT Analysis** — strengths, weaknesses, opportunities, threats
- **TAM/SAM/SOM** — market sizing
- **BCG Matrix** — portfolio positioning
- **Value Chain Analysis** — margin and efficiency mapping
- **Competitive Positioning Maps** — quadrant-based competitor mapping

## Report Structure

| Chapter | Content |
|---------|---------|
| 1. Executive Summary | Key findings, market size, growth rate, top recommendations |
| 2. Market Overview | Definition, scope, segmentation, history |
| 3. Market Size & Growth | TAM/SAM/SOM, CAGR, revenue forecasts |
| 4. Industry Dynamics | Porter's Five Forces assessment |
| 5. Competitive Landscape | Player profiles, market share, positioning map |
| 6. Customer Analysis | Segments, behavior, needs, trends |
| 7. Technology & Innovation | Emerging tech, disruption risk, adoption curves |
| 8. Regulatory & Macro | PESTLE analysis, compliance landscape |
| 9. Opportunities & Threats | SWOT synthesis, scenario analysis |
| 10. Strategic Recommendations | Prioritized actions, implementation roadmap |
| 11. Appendices | Data tables, methodology, bibliography |

## Workflow

### Phase 1: Research
- Define market boundaries and scope
- Deep web research for market data, reports, earnings calls
- Collect data points: market size, growth rates, player revenue, funding
- Identify 5-10 key competitors with detailed profiles
- Gather regulatory and macroeconomic data

### Phase 2: Analysis
- Apply each framework to the collected data
- Cross-reference findings across frameworks
- Identify convergent themes and contradictions
- Build scenario models (base, optimistic, pessimistic)
- Score opportunities by attractiveness and feasibility

### Phase 3: Visual Generation
- Market growth charts and TAM/SAM/SOM diagrams
- Competitive positioning maps (2x2 quadrants)
- Porter's Five Forces radar chart
- Risk heatmaps
- Industry ecosystem maps

### Phase 4: Writing
- Structured prose in consulting style (not bullets)
- Every claim backed by data with source citation
- Key insight callout boxes throughout
- Executive summary written last (distilled from findings)

### Phase 5: Compilation
- LaTeX formatting with custom style package
- Table of contents, bibliography, appendices
- PDF generation via LaTeX compiler

## Output Format

Professional LaTeX with custom environments:
- **Key Insight boxes** — highlighted findings
- **Market Data callouts** — statistics with source
- **Risk boxes** — threats with severity rating
- **Recommendation boxes** — prioritized actions
- **SWOT boxes** — four-quadrant analysis
- **Porter's Five Forces boxes** — force-by-force assessment
- **Pull quotes** — notable expert opinions
- **Stat boxes** — large-format key numbers

## Quality Standards

1. **Every claim needs a source.** No unsourced statistics.
2. **Recency matters.** Prefer data from the last 2 years.
3. **Triangulate.** Cross-reference market sizes across 3+ sources.
4. **Acknowledge uncertainty.** Use ranges, not false precision.
5. **Actionable recommendations.** Each recommendation has: what, why, how, expected impact.
6. **No filler.** Every paragraph must add information or insight.

For analysis templates, LaTeX formatting, and data patterns, see [REFERENCE.md](REFERENCE.md).
