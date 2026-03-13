---
name: prod-fairflow-calculator
description: This skill should be used when the user asks to "plan a FairFlow campaign", "calculate LP APR", "estimate LM spend", "project TVL growth", "evaluate campaign efficiency", "set campaign targets", "calculate break-even", or mentions FairFlow, liquidity mining, LP yield, MEV redistribution, campaign ROI, or DeFi yield calculations.
license: MIT
metadata:
  author: hungv47
  version: "1.0.0"
---

# FairFlow Campaign Calculator

Help users plan, calculate, and evaluate FairFlow liquidity mining campaigns with data-driven projections and efficiency metrics.

## Philosophy

Sustainable yield beats speculation. Good liquidity mining campaigns have:

- **Data-driven projections** - Calculations based on realistic assumptions, not hopium
- **Efficiency tracking** - Cost per $1M volume, cost per $1 TVL matter more than raw spend
- **EG honesty** - Equilibrium Gains are market-dependent and unpredictable; model scenarios, don't guess
- **Clear graduation path** - Every campaign should have criteria for reducing LM dependency
- **ROI focus** - Fee revenue vs LM spend determines long-term viability

This skill answers three questions:
1. **What to spend?** - LM budget to achieve target APR
2. **What to expect?** - Projected TVL, volume, and efficiency metrics
3. **When to adjust?** - Decision rules for scaling, maintaining, or killing campaigns

## Mode Detection

Determine the operating mode based on user input:

**Plan Mode** (Design a new campaign):
- User says "plan a FairFlow campaign", "new campaign", "design a campaign"
- User has a pair in mind but no projections yet
- User wants help setting LM budget and targets

**Analysis Mode** (Calculate specific metrics):
- User says "calculate LP APR", "what's the LM APR", "estimate break-even"
- User has specific numbers and wants calculations
- User wants to understand a single metric

**Review Mode** (Evaluate existing campaign):
- User says "evaluate campaign", "review my campaign", "is my campaign efficient"
- User has an active campaign with actual data
- User wants to compare actuals vs projections

If unclear, ask: *"Do you want to (1) plan a new campaign, (2) calculate specific metrics, or (3) review an existing campaign?"*

---

## Plan Mode

Use this when helping users design new FairFlow campaigns.

### Plan Mode Overview

```
Inputs → APR Calculations → Efficiency Projections → EG Scenarios → Validation
```

### Step 1: Gather Campaign Inputs

Ask (using AskUserQuestion):

> **Pool Configuration**
> - What pair? (e.g., MON/USDC)
> - Which chain?
> - What fee tier? (0.01%, 0.05%, 0.30%)
> - Fee tier in bps? (1, 5, 30 — needed for EG adjustment calculation)

> **LM Configuration**
> - What LM token? (KNC or partner token)
> - Current LM token price?
> - Campaign duration? (weeks)

> **Targets & Competition**
> - What's your target TVL?
> - What's the competitor APR you're competing against?
> - What APR gap do you want to maintain? (+15%, +25%, etc.)

> **Current State**
> - Current TVL (if any)?
> - Current daily volume (if any)?

### Step 2: Calculate APR Components

Use the formulas to calculate each APR component.

See [references/formulas.md](references/formulas.md) for all calculation formulas.

**LP Fee APR:**
```
Daily Fee Revenue = Volume × bps
LP Fee APR = (Daily Fee Revenue / TVL) × 365
```

**LM APR (solve for LM budget):**
```
Required LM APR = Target Total APR - LP Fee APR - EG APR (estimated)
Daily LM Value = (LM APR × TVL) / 365
Daily LM Tokens = Daily LM Value / Token Price
```

**Base APR (without EG):**
```
Base APR = LP Fee APR + LM APR
```

### Step 3: Model EG Scenarios

EG (Equilibrium Gains) cannot be predicted. Always present three scenarios. EG multipliers scale inversely with fee tier — lower-fee pools capture proportionally more EG relative to fees.

**Fee-tier adjustment:**
```
EG Multiplier = Scenario Base × (5 / pool_bps)
```

| Scenario | Base (at 0.05%) | Adjustment | When This Happens |
|----------|----------------:|:----------:|-------------------|
| **Low** | 0.50 | × (5 / bps) | Low volatility, stable markets |
| **Mid** | 1.00 | × (5 / bps) | Normal market conditions |
| **High** | 2.00 | × (5 / bps) | High volatility, active arbitrage |

**Adjusted multipliers by fee tier:**

| Fee Tier | bps | Low | Mid | High |
|----------|----:|----:|----:|-----:|
| 0.01% | 1 | 2.50 | 5.00 | 10.00 |
| 0.05% | 5 | 0.50 | 1.00 | 2.00 |
| 0.30% | 30 | 0.08 | 0.17 | 0.33 |

**Example at 0.01% (1 bp):** If LP Fee APR = 7.30%
- Low EG: 18.25% (2.50 × 7.30%)
- Mid EG: 36.50% (5.00 × 7.30%)
- High EG: 73.00% (10.00 × 7.30%)

**Example at 0.05% (5 bp):** If LP Fee APR = 7.30%
- Low EG: 3.65% (0.50 × 7.30%)
- Mid EG: 7.30% (1.00 × 7.30%)
- High EG: 14.60% (2.00 × 7.30%)

**Total APR by scenario:**
```
Total APR = LP Fee APR + EG APR + LM APR
```

### Step 4: Project Weekly Metrics

Build a weekly projection table:

| Week | TVL Target | Volume Target | Vol/TVL | LP Fee APR | LM APR | Base APR | EG Low | EG Mid | EG High | Total (Mid) | Weekly LM | Cumulative LM |
|------|------------|---------------|---------|------------|--------|----------|--------|--------|---------|-------------|-----------|---------------|
| 1 | | | | | | | | | | | | |
| 2 | | | | | | | | | | | | |
| 3 | | | | | | | | | | | | |
| 4 | | | | | | | | | | | | |

### Step 5: Calculate Efficiency Metrics

For each week, calculate:

| Metric | Formula | Target |
|--------|---------|--------|
| LM Cost per $1M Volume | `Weekly LM Spend / (Weekly Volume / 1M)` | < $1,000 |
| LM Cost per $1K TVL | `Monthly LM Spend / (TVL / 1K)` | < $50 |
| Cost per $1 TVL Acquired | `Cumulative LM / (Current TVL - Starting TVL)` | < $0.10 |
| Fee Revenue Ratio | `Monthly Fee Revenue / Monthly LM Spend` | > 50% |

See [references/benchmarks.md](references/benchmarks.md) for efficiency targets.

### Step 6: Validate Campaign

Run validation checks:

**APR Gap Check:**
- Is APR gap sufficient? (> 15% minimum, > 25% strong)
- Is gap maintained across all EG scenarios?

**Efficiency Check:**
- LM cost per $1M volume < $1,000?
- Cost per $1 TVL acquired < $0.10?

**Sustainability Check:**
- What Vol/TVL is needed to self-sustain without LM?
- Is that Vol/TVL realistic for this pair?

See [references/decision-framework.md](references/decision-framework.md) for decision rules.

### Plan Mode Output

Produce a Campaign Plan document:

```markdown
# FairFlow Campaign: [PAIR]

## Overview
| Field | Value |
|-------|-------|
| **Pair** | [TOKEN_A/TOKEN_B] |
| **Chain** | [Chain] |
| **Fee Tier** | [X%] ([X] bps) |
| **EG Adjustment** | 5 / [bps] = [X]× (Low: [X], Mid: [X], High: [X]) |
| **Duration** | [X weeks] |
| **Total Budget** | [X tokens] ($X USD) |
| **Target TVL** | $[X] |

## APR Breakdown

### By Week
| Week | TVL | Volume | Vol/TVL | Fee APR | LM APR | Base APR | EG (Low/Mid/High) | Total (Mid) |
|------|-----|--------|---------|---------|--------|----------|-------------------|-------------|
| 1 | | | | | | | | |
| ... | | | | | | | | |

### Competitive Positioning
| Scenario | Total APR | vs Competitor | Gap |
|----------|-----------|---------------|-----|
| Low EG | X% | X% | +X% |
| Mid EG | X% | X% | +X% |
| High EG | X% | X% | +X% |

## Efficiency Metrics
| Metric | Week 1 | Week 4 | Target | Status |
|--------|--------|--------|--------|--------|
| LM per $1M Volume | | | <$1,000 | |
| Cost per $1 TVL | | | <$0.10 | |
| Fee Revenue Ratio | | | >50% | |

## Graduation Path
- Break-even Vol/TVL: [X]
- Current projected Vol/TVL: [X]
- Path to reduce LM: [description]

## Success Criteria
| Criteria | Threshold | Action |
|----------|-----------|--------|
| Ship | [condition] | Scale up |
| Maintain | [condition] | Continue as-is |
| Kill | [condition] | Stop campaign |

## Weekly Review Checklist
- [ ] TVL vs target (within 20%?)
- [ ] Vol/TVL ratio (above 1.5?)
- [ ] APR gap still competitive?
- [ ] LM efficiency improving?
- [ ] External factors (competitor moves, market)?
- [ ] Decision: Scale / Maintain / Reduce / Kill
```

---

## Analysis Mode

Use this when users need specific metric calculations.

### Common Calculations

**"What LM budget do I need for X% APR?"**
```
Daily LM Value = (Target LM APR × TVL) / 365
Weekly LM USD = Daily LM Value × 7
Weekly LM Tokens = Weekly LM USD / Token Price
```

**"What's my LP Fee APR?"**
```
Daily Fee Revenue = Daily Volume × Fee Tier (as decimal)
LP Fee APR = (Daily Fee Revenue / TVL) × 365
```

**"What Vol/TVL do I need to break even?"**
```
Required Fee APR = Target APR - Expected EG APR
Vol/TVL = Required Fee APR / (Fee Tier × 365)
```

**"Is my campaign efficient?"**
```
LM Cost per $1M Volume = Weekly LM Spend / (Weekly Volume / 1,000,000)
< $1,000 = Good, < $500 = Excellent
```

See [references/formulas.md](references/formulas.md) for the complete formula reference.

### Analysis Output

Provide calculations with work shown:

```markdown
## Calculation: [Metric Name]

### Inputs
- [Input 1]: [Value]
- [Input 2]: [Value]

### Formula
```
[Formula here]
```

### Calculation
```
[Step-by-step calculation]
```

### Result
**[Metric Name]:** [Value]

### Interpretation
[What this means, whether it's good/bad, what to do about it]
```

---

## Review Mode

Use this when evaluating active campaigns against projections.

### Step 1: Gather Actual Data

Ask:

> **Current Campaign Status**
> - Current TVL (actual)?
> - Current daily volume (actual)?
> - Weekly LM spend to date?
> - Campaign week number?

> **Projected vs Actual**
> - What were your TVL projections?
> - What were your volume projections?

### Step 2: Calculate Variance

| Metric | Projected | Actual | Variance |
|--------|-----------|--------|----------|
| TVL | $X | $X | +/- X% |
| Volume | $X | $X | +/- X% |
| Vol/TVL | X | X | +/- X% |
| LP Fee APR | X% | X% | +/- X% |

### Step 3: Apply Decision Framework

Based on actuals, recommend action:

| Condition | Action |
|-----------|--------|
| TVL growth > 20% WoW AND Vol/TVL > 1.5 | Scale LM +25% |
| TVL growth > 10% WoW AND APR gap > 20% | Maintain current LM |
| TVL flat AND Vol/TVL > 2.0 | Reduce LM -15% |
| TVL declining AND APR gap > 30% | Diagnose external factors |
| TVL < 50% of target after 2 weeks | Kill campaign |
| Vol/TVL < 0.5 for 2 consecutive weeks | Kill campaign |
| LM Cost per $1M Volume > $2,000 | Kill campaign |

See [references/decision-framework.md](references/decision-framework.md) for complete decision rules.

### Step 4: Check Graduation Criteria

| Graduation Signal | Status |
|-------------------|--------|
| Base APR (Fees + EG) > Competitor APR | Can begin LM reduction |
| TVL stable for 4 weeks at reduced LM | Continue reduction |
| Vol/TVL > 2.5 sustained | Pool is self-sustaining |

### Review Output

```markdown
## Campaign Review: [PAIR] - Week [X]

### Performance Summary
| Metric | Projected | Actual | Variance | Status |
|--------|-----------|--------|----------|--------|
| TVL | $X | $X | X% | ✅/⚠️/❌ |
| Volume | $X | $X | X% | ✅/⚠️/❌ |
| Vol/TVL | X | X | X% | ✅/⚠️/❌ |

### Efficiency
| Metric | Actual | Target | Status |
|--------|--------|--------|--------|
| LM per $1M Vol | $X | <$1,000 | ✅/❌ |
| Cost per $1 TVL | $X | <$0.10 | ✅/❌ |

### Decision
**Recommendation:** [Scale / Maintain / Reduce / Kill]
**Reasoning:** [Why this recommendation]

### Next Week Actions
1. [Action item]
2. [Action item]
```

---

## Integration Points

| Skill | How FairFlow Calculator Connects |
|-------|----------------------------------|
| **mkt-funnel-planner** | Campaign metrics feed into broader funnel tracking; LP retention is a funnel stage |
| **mkt-initiative-planner** | FairFlow campaigns become initiative proposals with defined hypotheses and success criteria |

When working with these skills:
- Campaign success criteria align with initiative KPIs
- LP retention metrics connect to funnel D30/D90 tracking
- Campaign budgets inform initiative resource planning

---

## How to Work

- **Show your math**: Always display calculations step-by-step, not just final answers
- **EG is unpredictable**: Never present EG as a single number; always show Low/Mid/High scenarios
- **Efficiency > raw spend**: A $50K campaign that's inefficient is worse than a $10K efficient one
- **Challenge unrealistic targets**: If Vol/TVL assumptions are aggressive, say so
- **Kill criteria matter**: Every campaign needs clear conditions for stopping
- **Graduation path**: Always define how the campaign becomes self-sustaining
- **Weekly reviews**: Recommend actual vs projected comparison weekly

### Anti-Patterns to Avoid

| Don't | Do |
|-------|-----|
| Present single EG projection | Always show Low/Mid/High scenarios |
| Ignore efficiency metrics | Calculate cost per $1M volume and cost per $1 TVL |
| Skip break-even analysis | Always show what Vol/TVL is needed to self-sustain |
| Set targets without kill criteria | Define stop conditions upfront |
| Assume LM continues forever | Plan graduation path from day one |
