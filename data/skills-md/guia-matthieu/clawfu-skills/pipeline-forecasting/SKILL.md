---
name: pipeline-forecasting
description: Generate predictive pipeline forecasts with confidence intervals and scenario modeling for revenue planning
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Pipeline Forecasting

> Build accurate, data-driven revenue forecasts using historical conversion rates, deal velocity, and confidence-weighted projections.

## When to Use This Skill

- Weekly/monthly pipeline reviews with leadership
- Board meeting revenue projections
- Quota setting and territory planning
- Identifying gaps between forecast and target
- Scenario planning for best/worst/likely outcomes

## Methodology Foundation

Based on **Clari's Revenue Operations methodology** and **Forrester's B2B Revenue Waterfall**, combining:
- Weighted pipeline (probability × value)
- Historical stage conversion rates
- Deal velocity analysis
- Commit vs. upside categorization

## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Calculates weighted pipeline by stage | Which deals to include/exclude |
| Applies historical conversion rates | Override factors for specific deals |
| Generates confidence intervals | Final commit number to leadership |
| Identifies forecast risks | Actions to close gaps |
| Models best/worst/likely scenarios | Which scenario to plan against |

## What This Skill Does

1. **Ingests pipeline data** - Current opportunities with stage, value, close date
2. **Applies conversion math** - Historical win rates by stage, segment, rep
3. **Calculates weighted forecast** - Probability-adjusted revenue projection
4. **Generates scenarios** - Best case, commit, worst case with confidence bands
5. **Identifies risks** - Deals pushing, pipeline gaps, coverage ratios

## How to Use

```
I need a pipeline forecast for Q1. Here's our current pipeline:

[Paste pipeline data: Deal name, Stage, Value, Close Date, Rep]

Historical context:
- Average win rate: 25%
- Stage 3→Close rate: 45%
- Stage 4→Close rate: 70%
- Average sales cycle: 45 days

Target: $2.5M for Q1
```

## Instructions

### Step 1: Pipeline Categorization
Segment deals into:
- **Commit** - High confidence (Stage 4+, verbal commit)
- **Best Case** - Medium confidence (Stage 3, engaged)
- **Upside** - Low confidence (Stage 1-2, early)

### Step 2: Weighted Calculation
```
Weighted Value = Deal Value × Stage Probability × Rep Factor

Stage Probabilities (adjust to your data):
- Stage 1 (Discovery): 10%
- Stage 2 (Qualification): 20%
- Stage 3 (Proposal): 40%
- Stage 4 (Negotiation): 70%
- Stage 5 (Verbal): 90%
```

### Step 3: Coverage Analysis
```
Pipeline Coverage = Total Pipeline ÷ Target
- Healthy: 3-4x coverage
- At Risk: 2-3x coverage
- Critical: <2x coverage
```

### Step 4: Scenario Modeling
- **Worst Case**: Commit only (90%+ probability deals)
- **Likely Case**: Commit + 50% of Best Case
- **Best Case**: Commit + Best Case + 25% of Upside

### Step 5: Risk Identification
Flag deals with:
- Close date in past (needs update)
- No activity in 14+ days (stalled)
- Pushing from previous quarter (slip risk)
- Missing key fields (data quality)

## Examples

### Example 1: Quarterly Forecast

**Input:**
```
Pipeline for Q1:
- Acme Corp: Stage 4, $150K, Jan 30, Rep: Sarah
- Beta Inc: Stage 3, $80K, Feb 15, Rep: Mike
- Gamma Ltd: Stage 2, $200K, Mar 1, Rep: Sarah
- Delta Co: Stage 4, $120K, Feb 28, Rep: Lisa
- Echo Systems: Stage 1, $500K, Mar 15, Rep: Mike

Target: $400K
```

**Output:**
```
## Q1 Pipeline Forecast

### Weighted Pipeline
| Deal | Stage | Value | Probability | Weighted |
|------|-------|-------|-------------|----------|
| Acme Corp | 4 | $150K | 70% | $105K |
| Delta Co | 4 | $120K | 70% | $84K |
| Beta Inc | 3 | $80K | 40% | $32K |
| Gamma Ltd | 2 | $200K | 20% | $40K |
| Echo Systems | 1 | $500K | 10% | $50K |
| **Total** | | **$1.05M** | | **$311K** |

### Scenario Analysis
- **Worst Case (Commit)**: $189K (Acme + Delta at 70%)
- **Likely Case**: $245K (Commit + 50% Best Case)
- **Best Case**: $361K (All weighted)

### Coverage Ratio
- Pipeline: $1.05M
- Target: $400K
- Coverage: 2.6x ⚠️ (At Risk - need 3x+)

### Risks Identified
1. ⚠️ Echo Systems ($500K) is Stage 1 with Mar close - unlikely
2. ⚠️ Gap of $155K between Likely ($245K) and Target ($400K)

### Recommendations
1. Pressure test Acme and Delta for verbal commits
2. Accelerate Beta Inc to Stage 4 this week
3. Add $200K+ new pipeline to reach 3x coverage
```

### Example 2: Monthly Roll-Up

**Input:**
```
January pipeline by rep:
Sarah: $450K weighted, $280K commit
Mike: $320K weighted, $150K commit
Lisa: $280K weighted, $200K commit

Team target: $500K
```

**Output:**
```
## January Team Forecast

| Rep | Weighted | Commit | % to Target |
|-----|----------|--------|-------------|
| Sarah | $450K | $280K | 56% |
| Mike | $320K | $150K | 30% |
| Lisa | $280K | $200K | 40% |
| **Team** | **$1.05M** | **$630K** | **126%** |

### Forecast Summary
- **Team Commit**: $630K (126% of $500K target) ✅
- **Confidence**: HIGH - commit exceeds target

### Risk Watch
- Mike at 30% commit coverage - needs deal acceleration
- Sarah carrying most weight - concentration risk
```

## Skill Boundaries

### What This Skill Does Well
- Mathematical pipeline calculations
- Scenario modeling with clear assumptions
- Identifying data quality issues
- Coverage ratio analysis

### What This Skill Cannot Do
- Predict which specific deals will close (human judgment)
- Account for market changes or competitive moves
- Replace rep-level deal knowledge
- Guarantee forecast accuracy

### When to Escalate to Human
- Deals with unusual circumstances (M&A, champion left)
- Market disruptions affecting close rates
- Strategic accounts requiring executive judgment
- Final commit numbers for board/investors

## Iteration Guide

### Follow-up Prompts
- "What if we lose the top 2 deals? Show me that scenario."
- "Apply a 20% haircut to all Stage 2 deals and recalculate."
- "Which deals have the highest impact on our forecast?"
- "Show me the gap between forecast and target by month."

### Refinement Cycle
1. Generate initial forecast → Review with reps
2. Update deal probabilities based on rep input
3. Re-run forecast with adjusted assumptions
4. Lock commit number, track weekly variance

## Checklists & Templates

### Weekly Forecast Review Checklist
- [ ] All deals have current close dates
- [ ] Stage progression updated this week
- [ ] Commit deals have next steps scheduled
- [ ] Risks flagged and mitigation assigned
- [ ] Coverage ratio calculated

### Forecast Template
```markdown
## [Period] Revenue Forecast

**Generated:** [Date]
**Pipeline Cutoff:** [Date]

### Summary
- Target: $X
- Commit: $X (X% of target)
- Best Case: $X
- Coverage: Xx

### By Segment
[Table]

### Risks & Mitigations
[List]

### Actions This Week
[List]
```

## References

- Clari Revenue Operations Playbook
- Forrester B2B Revenue Waterfall Model
- MEDDICC Deal Qualification Framework
- Gartner Sales Forecasting Best Practices

## Related Skills

- `deal-risk-scoring` - Assess individual deal health
- `lead-scoring` - Qualify top-of-funnel
- `account-health` - Customer retention signals

## Skill Metadata

- **Domain**: RevOps
- **Complexity**: Intermediate
- **Mode**: centaur
- **Time to Value**: 15-30 minutes per forecast
- **Prerequisites**: Pipeline data export, historical win rates
