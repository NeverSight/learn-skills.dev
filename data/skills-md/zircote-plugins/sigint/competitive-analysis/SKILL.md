---
name: competitive-analysis
description: This skill should be used when the user asks to "analyze competitors", "map competitive landscape", "Porter's 5 Forces analysis", "competitor comparison", "competitive positioning", "identify competitors", "competitive intelligence", or needs guidance on competitor research methodology, market positioning analysis, or competitive strategy frameworks.
version: 0.2.0
---

# Competitive Analysis

## Overview

Competitive analysis systematically evaluates competitors to understand market positioning, identify gaps, and inform strategic decisions. This skill provides frameworks and methodologies for thorough competitive intelligence gathering.

## Required Frameworks

| Framework | Output Section | Required | Condition |
|-----------|---------------|----------|-----------|
| Porter's 5 Forces | Porter's 5 Forces Analysis | yes | — |
| Competitor Matrix | Competitive Matrix | yes | — |
| Positioning Map | Positioning Map | conditional | Needs 2+ comparable dimensions from elicitation or competitors |
| Trend Indicators | throughout | yes | — |

**Trend Indicators**: Load and apply the trend indicator definitions from `protocols/TREND-INDICATORS.md`.

## When to Use

- Entering a new market or segment
- Evaluating product positioning
- Identifying feature gaps
- Understanding pricing dynamics
- Assessing competitive threats
- Planning differentiation strategy
- Creating board/investor-ready competitive landscape documents
- Analyzing emerging or nascent markets with indirect/potential competitors

## Handling Incomplete Prompts

When the user's request lacks critical context (no market, industry, or competitors specified), do NOT fabricate an analysis. Instead:
1. Acknowledge the request enthusiastically
2. Ask clarifying questions about: market/industry, product, known competitors, analysis goal, target customer segment
3. Describe what deliverables they can expect once context is provided
4. Be helpful and engaging — never refuse outright

## Adapting for Emerging Markets / New Categories

When analyzing a market that does not yet exist or has no direct competitors:
1. **Do NOT say competitive analysis is inapplicable** — it is MORE important for new categories
2. Identify what customers currently use as substitutes (manual processes, consultants, existing tools, DIY solutions)
3. Map indirect competitors from adjacent markets who could pivot into the space
4. Identify potential entrants — well-funded adjacent players most likely to enter
5. Adapt Porter's 5 Forces: rivalry is typically low (temporary), threat of new entry is typically high, threat of substitution is typically very high
6. Address first-mover and category creation dynamics (advantages and risks)
7. Provide strategic recommendations focused on category definition, building switching costs, and monitoring potential entrants

## Core Frameworks

### Porter's 5 Forces

Analyze industry structure through five competitive forces. For each force, you MUST provide:
- An explicit rating (e.g., HIGH, MODERATE, LOW, or VERY HIGH)
- Specific factors relevant to the industry being analyzed
- An assessment statement explaining implications

**1. Competitive Rivalry**
- Number and size of competitors
- Industry growth rate
- Product differentiation level
- Exit barriers
- **Indicator**: High rivalry = challenging margins

**2. Supplier Power**
- Supplier concentration
- Switching costs
- Unique inputs
- Forward integration threat
- **Indicator**: High power = cost pressure

**3. Buyer Power**
- Buyer concentration
- Purchase volume
- Switching costs
- Price sensitivity
- **Indicator**: High power = pricing pressure

**4. Threat of Substitution**
- Alternative solutions
- Price-performance trade-off
- Switching costs
- Buyer propensity to substitute
- **Indicator**: High threat = innovation pressure

**5. Threat of New Entry**
- Capital requirements
- Economies of scale
- Brand loyalty
- Regulatory barriers
- **Indicator**: High threat = margin pressure

### Competitor Matrix

Create comparison table with:
| Dimension | Competitor A | Competitor B | Your Position |
|-----------|--------------|--------------|---------------|
| Market Share | % | % | % |
| Pricing | $-$$$ | $-$$$ | $-$$$ |
| Key Features | List | List | List |
| Strengths | List | List | List |
| Weaknesses | List | List | List |
| Trend | INC/DEC/CONST | INC/DEC/CONST | - |

### Positioning Map

Visualize competitive positioning on two key dimensions:
- X-axis: Feature richness (or price)
- Y-axis: Quality/premium positioning (or another differentiator)

Generate as Mermaid quadrant chart showing relative positions. Use `quadrantChart` directive with labeled axes and all competitor names as data points. When the user specifies axes (e.g., "price vs ease of use"), use those exact dimensions. Provide a rationale table explaining each competitor's placement before the chart.

## Research Process

### Step 1: Identify Competitors
- Direct competitors (same product/market)
- Indirect competitors (different product, same need)
- Potential entrants (adjacent markets)
- Substitutes (alternative solutions)

### Step 2: Gather Intelligence
**Public Sources:**
- Company websites and blogs
- Press releases and news
- Financial reports (if public)
- Job postings (reveals priorities)
- Social media presence
- Customer reviews
- Industry analyst reports

**Search Patterns:**
- "[competitor] pricing"
- "[competitor] vs [alternative]"
- "[competitor] review"
- "[competitor] funding" / "[competitor] revenue"
- "site:[competitor.com] features"

### Step 3: Analyze Findings
- Map to Porter's 5 Forces
- Build competitor matrix
- Create positioning map
- Identify trend directions (INC/DEC/CONST)

### Step 4: Synthesize Insights
- Competitive advantages/disadvantages
- Market gaps and opportunities
- Threat assessment
- Strategic recommendations

## Output Structure

```markdown
## Competitive Landscape Overview
[Summary of competitive environment]

## Porter's 5 Forces Analysis
[Force-by-force assessment with ratings]

## Competitor Profiles
[Detailed profiles of top 3-5 competitors]

## Competitive Matrix
[Comparison table]

## Positioning Map
[Mermaid quadrant chart]

## Key Insights
1. [Insight with implication]
2. [Insight with implication]

## Strategic Recommendations
- [Recommendation based on analysis — specific, actionable, tailored to the user's context]
```

**IMPORTANT**: When the user specifies a context (e.g., "small dev teams", "board presentation", "differentiation opportunities"), tailor every section to that context. Generic analysis is not acceptable — recommendations must be specific to the user's stated situation, audience, and goals.

## Trend Indicators

Apply three-valued logic to competitor trajectories:
- **INC**: Growing market share, expanding features, positive momentum
- **DEC**: Losing share, reducing investment, negative signals
- **CONST**: Stable position, maintaining but not growing

## Best Practices

- Update analysis quarterly at minimum
- Cross-validate from multiple sources
- Note source reliability and dates
- Distinguish facts from speculation
- Consider regional variations
- Track competitor job postings for strategy hints

## Additional Resources

For detailed frameworks and templates, see:
- `references/porters-five-forces.md` - Complete Porter's framework
- `references/competitive-matrix-template.md` - Matrix templates
- `examples/competitive-analysis-report.md` - Sample report

## Orchestration Hints

**Confidence tiers (universal scale):**
- **High**: 3+ independent, recent (<12mo) sources that converge
- **Medium**: 2 sources OR sources >12mo old OR indirect evidence
- **Low**: Single source, inference, or extrapolation

Dimension-specific confidence criteria below REFINE (not replace) these universal definitions.

- **Cross-reference dimensions**: sizing (validate market share figures), customer (switching costs, satisfaction gaps)
- **Alert triggers**:
  - Major undiscovered competitor with >10% market share
  - Market share shift >20% in last 12 months
  - New entrant with disruptive positioning
- **Confidence rules**:
  - High: 3+ independent sources confirm
  - Medium: 2 sources or 1 highly reliable source
  - Low: Single source or analyst estimate
- **Conflict detection**:
  - Market share totals vs sizing dimension's TAM figures
  - Competitor revenue claims vs financial dimension's estimates
  - Feature comparison vs tech dimension's feasibility assessment
