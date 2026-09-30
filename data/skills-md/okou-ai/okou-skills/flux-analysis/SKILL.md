---
name: flux-analysis
description: Explain financial variances with driver analysis, period comparisons, waterfall bridges, and commentary.
---

## Decomposition Techniques

### Price x Volume Separation

The foundational split for any metric expressible as unit price multiplied by quantity.

**Two-factor formulas:**
```
Total Movement = Actual Result - Baseline (budget or prior period)

Quantity Component  = (Actual Units - Baseline Units) x Baseline Unit Price
Pricing Component   = (Actual Unit Price - Baseline Unit Price) x Actual Units

Check: Quantity Component + Pricing Component = Total Movement
       (when the interaction term is absorbed into one of the two factors)
```

**Three-factor formulas (isolating composition shifts):**
```
Quantity Component    = (Actual Units - Baseline Units) x Baseline Price x Baseline Mix Weights
Pricing Component     = (Actual Price - Baseline Price) x Baseline Units x Actual Mix Weights
Composition Component = Baseline Price x Baseline Units x (Actual Mix Weights - Baseline Mix Weights)
```

**Worked example — top-line revenue:**
- Baseline plan: 10,000 units at $50/unit = $500,000
- Actual outcome: 11,000 units at $48/unit = $528,000
- Net movement: +$28,000 favorable
  - Quantity uplift: +1,000 units x $50 = +$50,000 (favorable — higher volume)
  - Pricing drag: -$2 x 11,000 = -$22,000 (unfavorable — reduced average selling price)

### Blended Rate / Composition Separation

Applicable when aggregated results blend multiple segments with distinct unit economics.

**Formulas:**
```
Rate Component = Sum across segments of [Actual Volume_i x (Actual Rate_i - Baseline Rate_i)]
Composition Component = Sum across segments of [Baseline Rate_i x (Actual Volume_i - Proportional Volume_i at Baseline Mix)]
```

**Worked example — gross margin compression:**
- Segment X earns 60% margin; Segment Y earns 40% margin
- Plan assumed a 50/50 split -> blended 50% margin
- Actual split was 40/60 -> blended 48% margin
- The 2-point margin decline is attributable to the shift toward the lower-margin segment

### People-Cost Decomposition

Purpose-built for analyzing compensation and headcount-driven expense lines.

```
Total Compensation Movement = Actual Spend - Planned Spend

Break into:
1. Staffing level effect     = (Actual Headcount - Plan Headcount) x Plan Average Cost
2. Per-capita cost effect    = (Actual Average Cost - Plan Average Cost) x Plan Headcount
3. Composition effect        = Residual from shifts in seniority, department, or geography mix
4. Phasing effect            = Impact of hires arriving earlier or later than the plan assumed
5. Attrition benefit         = Savings from unplanned departures (partially offset by replacement and vacancy costs)
```

### Functional Expense Decomposition

For operating cost categories where a price-times-volume model does not apply naturally.

```
Total OpEx Movement = Actual Operating Costs - Planned Operating Costs

Segment into:
1. Headcount-linked costs       (wages, benefits, payroll taxes, recruiting fees)
2. Activity-linked costs        (cloud hosting, payment processing fees, sales commissions, freight)
3. Discretionary programs       (travel, conferences, outside services, campaign spend)
4. Committed / fixed costs      (facility leases, insurance, enterprise software licenses)
5. Non-recurring charges        (severance, litigation, asset write-downs, project-specific outlays)
6. Timing / phasing differences (spend that shifted between periods relative to the plan)
```

## Significance Thresholds & Prioritization

### Calibrating Thresholds

Thresholds govern which movements warrant formal investigation and written explanation. Base them on:

1. **Overall materiality:** Usually 1-5% of a primary benchmark (revenue, total assets, or net income)
2. **Relative line-item scale:** Apply tighter percentage gates to larger balances
3. **Historical volatility:** Allow wider bands for inherently variable accounts to filter noise
4. **Decision relevance:** Would this size of movement influence a management decision or board discussion?

### Suggested Threshold Grid

| Comparison Basis | Suggested Dollar Gate | Suggested Percentage Gate | Trigger Logic |
|---|---|---|---|
| Actual vs. annual plan | Entity-specific | 10% | Whichever is breached first |
| Actual vs. same period last year | Entity-specific | 15% | Whichever is breached first |
| Actual vs. latest forecast | Entity-specific | 5% | Whichever is breached first |
| Sequential month-over-month | Entity-specific | 20% | Whichever is breached first |

*Set the dollar gate at roughly 0.5-1% of revenue for income-statement lines.*

### Triage Order When Multiple Items Exceed Thresholds

1. **Greatest absolute dollar impact** — largest influence on the bottom line
2. **Greatest percentage deviation** — may signal a process breakdown or data error
3. **Counter-trend movements** — direction opposite to what history or forecasts predicted
4. **Newly emerged variances** — items previously on track that have just diverged
5. **Compounding variances** — gaps that have widened in each of the last several periods

## Writing Effective Variance Narratives

### Recommended Structure

```
[Line Item]: [Favorable / Unfavorable] movement of $[amount] ([X]%)
relative to [budget / prior period / forecast] for [reporting period]

Primary driver: [Brief label]
[Two to three sentences explaining the business cause, quantifying each
contributing factor where possible.]

Outlook: [One-time event / Likely to persist / Improving / Worsening]
Next step: [No action / Monitor / Deeper review / Adjust forecast]
```

### Quality Criteria

Strong narratives consistently satisfy these tests:

- **Precise:** Names concrete factors rather than restating the variance itself
- **Measured:** Attaches dollar or percentage weight to each cited driver
- **Explanatory:** Addresses why the movement occurred, not merely that it did
- **Prospective:** States whether the movement is expected to continue, reverse, or evolve
- **Directive:** Identifies any follow-up action or decision prompted by the finding
- **Compact:** Two to four sentences — not padded filler

### Pitfalls to Avoid

- Restating the outcome as its own cause ("Revenue rose because revenue was higher")
- Labeling a variance as "timing" without specifying what shifted and when normalization is expected
- Calling something "one-time" without describing the actual event
- Sweeping a material movement under "various small items" instead of decomposing further
- Explaining only the dominant driver while ignoring meaningful offsets
- Using vague qualifiers ("elevated," "slightly higher") without attached numbers

## Bridge / Waterfall Presentation

### Concept

A bridge (waterfall) chart traces the path from a starting value to an ending value through a sequence of additive and subtractive contributors. It is the visual companion to variance decomposition.

### Data Architecture

```
Starting point:   [Baseline figure — plan, prior period, or forecast]
Contributors:     [Ordered list of signed driver amounts]
Ending point:     [Actual figure]

Integrity check:  Starting point + Sum(all contributors) = Ending point
```

### Text-Format Bridge (When No Charting Tool Is Available)

```
BRIDGE: Operating Expenses — Q4 Actual vs. Q4 Plan

Q4 Planned OpEx                                       $8,000K
  |
  |--[+] Incremental headcount above plan              +$500K
  |--[+] Unplanned outside counsel fees                +$200K
  |--[-] Open-role savings (delayed hiring)            -$350K
  |--[-] Travel spend below budget                     -$180K
  |--[+] Cloud infrastructure overrun                  +$130K
  |--[-] Marketing program deferrals                   -$100K
  |
Q4 Actual OpEx                                        $8,200K

Net Movement: +$200K (+2.5% unfavorable)
```

### Companion Reconciliation Table

| Driver | Amount | Share of Total Movement | Running Total |
|---|---|---|---|
| Incremental headcount | +$500K | 250% | +$500K |
| Outside counsel | +$200K | 100% | +$700K |
| Open-role savings | -$350K | -175% | +$350K |
| Travel underspend | -$180K | -90% | +$170K |
| Cloud overrun | +$130K | 65% | +$300K |
| Marketing deferrals | -$100K | -50% | +$200K |
| **Net movement** | **+$200K** | **100%** | |

*Individual shares can exceed 100% when favorable and unfavorable drivers offset each other.*

### Presentation Guidelines

1. Sequence drivers from most favorable to most unfavorable (or in a logical business narrative order)
2. Cap the driver count at 5-8; roll smaller items into an "All other" bucket
3. Verify arithmetic: opening value plus all drivers equals closing value
4. Use color to distinguish direction — green for favorable, red for unfavorable — in graphical renderings
5. Annotate each segment with both the dollar amount and a short label
6. Include a summary segment showing the net total movement

## Multi-Scenario Comparisons

### Three-Column Layout

| Line Item | Annual Plan | Latest Forecast | Actual | Plan Var ($) | Plan Var (%) | Forecast Var ($) | Forecast Var (%) |
|---|---|---|---|---|---|---|---|
| Revenue | $X | $X | $X | $X | X% | $X | X% |
| Direct costs | $X | $X | $X | $X | X% | $X | X% |
| Gross profit | $X | $X | $X | $X | X% | $X | X% |

### Choosing the Right Baseline

- **Actual vs. annual plan:** Governance and incentive evaluation; the plan is fixed at the start of the fiscal year
- **Actual vs. rolling forecast:** Operational steering and early-warning detection; the forecast is refreshed monthly or quarterly
- **Forecast vs. plan:** Gauges how management expectations have shifted since planning; highlights planning-accuracy gaps
- **Actual vs. prior period (sequential):** Reveals trend direction; especially useful for new ventures or post-acquisition integration where a plan may not yet exist
- **Actual vs. prior year (year-over-year):** Growth assessment adjusted for seasonality

### Tracking Forecast Precision

Measure forecast quality over time to tighten future planning:

```
Period Accuracy = 1 - |Actual - Forecast| / |Actual|

MAPE (Mean Absolute Percentage Error) = Mean of |Actual - Forecast| / |Actual| across all periods
```

| Month | Forecast | Actual | Deviation | Accuracy |
|---|---|---|---|---|
| Jan | $X | $X | $X (X%) | XX% |
| Feb | $X | $X | $X (X%) | XX% |
| ... | ... | ... | ... | ... |
| **Full Year** | | | **MAPE** | **XX%** |

### Reading Variance Trends Across Time

- **Persistently favorable:** Plans may be overly conservative (potential sandbagging)
- **Persistently unfavorable:** Targets may be unrealistic or execution is lagging
- **Widening unfavorable gap:** Performance is deteriorating or external conditions are shifting
- **Narrowing gap:** Forecast accuracy is improving through the year (a healthy signal)
- **Erratic swings:** Business is inherently unpredictable or the forecasting methodology needs refinement
