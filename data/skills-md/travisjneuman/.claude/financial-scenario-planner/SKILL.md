---
name: financial-scenario-planner
description: Stress-test financial plans across scenarios (bull/bear/base), sensitivity tables, and Monte Carlo-style analysis. Use when evaluating financial assumptions, modeling risk scenarios, or building scenario-based financial plans.
---

# Financial Scenario Planner

Frameworks for building multi-scenario financial models, stress testing assumptions, sensitivity analysis, and probability-weighted financial planning.

## Scenario Analysis Framework

### Three-Scenario Model

```
SCENARIO PLANNING TEMPLATE:

                    BEAR CASE        BASE CASE        BULL CASE
                    (Pessimistic)    (Expected)       (Optimistic)
Probability:        20-25%           50-60%           20-25%

REVENUE ASSUMPTIONS:
  Growth rate:      [X%]             [X%]             [X%]
  New customers:    [N]              [N]              [N]
  Churn rate:       [X%]             [X%]             [X%]
  ARPU change:      [X%]             [X%]             [X%]
  Market size:      [$ ]             [$ ]             [$ ]

COST ASSUMPTIONS:
  COGS margin:      [X%]             [X%]             [X%]
  Headcount growth: [N]              [N]              [N]
  Salary inflation: [X%]             [X%]             [X%]
  Marketing spend:  [$ ]             [$ ]             [$ ]
  Capex:            [$ ]             [$ ]             [$ ]

EXTERNAL FACTORS:
  Interest rates:   [X%]             [X%]             [X%]
  Inflation:        [X%]             [X%]             [X%]
  FX rates:         [X ]             [X ]             [X ]
  Regulatory:       [Impact]         [Impact]         [Impact]

PROJECTED OUTCOMES:
  Revenue:          [$ ]             [$ ]             [$ ]
  EBITDA:           [$ ]             [$ ]             [$ ]
  Net income:       [$ ]             [$ ]             [$ ]
  Cash position:    [$ ]             [$ ]             [$ ]
  Runway (months):  [N]              [N]              [N]

EXPECTED VALUE:
  E[Revenue] = P(bear) x Rev(bear) + P(base) x Rev(base) + P(bull) x Rev(bull)
```

### Scenario Trigger Events

| Scenario Driver | Bear Trigger | Base Assumption | Bull Trigger |
|----------------|-------------|-----------------|-------------|
| **Market demand** | Recession, -15% | Steady growth, +5% | Market expansion, +20% |
| **Competition** | New entrant takes 20% share | Stable competition | Competitor exits market |
| **Regulation** | Restrictive new regulation | Status quo | Deregulation/favorable policy |
| **Technology** | Disruption makes product obsolete | Incremental improvement | Breakthrough advantage |
| **Funding** | Cannot raise next round | Raise at expected terms | Oversubscribed round |
| **Key personnel** | Lose critical team members | Normal retention | Key strategic hires |

## Sensitivity Analysis

### One-Variable Sensitivity Table

```
REVENUE SENSITIVITY TO PRICE CHANGE:

Price Change:     -20%    -10%    Base    +10%    +20%
Volume Impact:    +10%    +5%     Base    -3%     -8%
Revenue:          [$ ]    [$ ]    [$ ]    [$ ]    [$ ]
Gross Profit:     [$ ]    [$ ]    [$ ]    [$ ]    [$ ]
Net Income:       [$ ]    [$ ]    [$ ]    [$ ]    [$ ]
```

### Two-Variable Sensitivity (Tornado Chart Data)

```
TORNADO CHART DATA — NET INCOME SENSITIVITY:

Variable            | Low Value | High Value | Low Impact  | High Impact
Revenue growth      | 5%        | 25%        | -$500K      | +$800K
Customer churn      | 8%        | 2%         | -$400K      | +$300K
COGS margin         | 45%       | 35%        | -$350K      | +$350K
Headcount           | +15       | +5         | -$300K      | +$200K
Interest rates      | 7%        | 4%         | -$150K      | +$100K
FX rates            | -10%      | +5%        | -$120K      | +$60K

INTERPRETATION:
  - Revenue growth has the highest impact on outcomes
  - Focus risk mitigation on top 3 variables
  - Variables below $100K impact are noise
```

### Break-Even Analysis

```
BREAK-EVEN CALCULATOR:

FIXED COSTS (Monthly):
  Salaries:           $______
  Rent/facilities:    $______
  SaaS/tools:         $______
  Insurance:          $______
  Other fixed:        $______
  TOTAL FIXED:        $______

VARIABLE COSTS (per unit):
  COGS:               $______
  Commission:         $______
  Payment processing: $______
  Support cost:       $______
  TOTAL VARIABLE:     $______

PRICING:
  Average selling price: $______
  Contribution margin:   $______ (price - variable cost)
  Contribution %:        _____%

BREAK-EVEN:
  Units:  Fixed costs / Contribution margin = _____ units
  Revenue: Fixed costs / Contribution % = $______

MONTHS TO BREAK-EVEN:
  At current growth rate: _____ months
  At optimistic rate:     _____ months
  At pessimistic rate:    _____ months
```

## Monte Carlo Simulation Design

### Simulation Framework

```
MONTE CARLO SETUP:

STEP 1: IDENTIFY VARIABLES
  List all uncertain inputs that affect the outcome.
  For each variable, define:
    - Distribution type (normal, uniform, triangular, lognormal)
    - Parameters (mean, std dev, min, max)

STEP 2: DEFINE DISTRIBUTIONS
  Revenue growth:   Normal(mean=15%, std=5%)
  Customer churn:   Triangular(min=2%, mode=5%, max=12%)
  COGS margin:      Uniform(min=30%, max=45%)
  Headcount growth: Discrete([5, 8, 10, 12, 15], probs=[0.1, 0.2, 0.4, 0.2, 0.1])

STEP 3: RUN SIMULATIONS
  Iterations: 10,000 (minimum for stable results)
  For each iteration:
    1. Sample random value from each distribution
    2. Calculate outcome (revenue, profit, cash flow)
    3. Store result

STEP 4: ANALYZE RESULTS
  Mean outcome:           $______
  Median outcome:         $______
  Standard deviation:     $______
  5th percentile (VaR):   $______ (worst 5% of outcomes)
  95th percentile:        $______ (best 5% of outcomes)
  Probability of loss:    _____%
  Probability of target:  _____%

STEP 5: INTERPRET
  "There is a 90% probability that net income will fall between
   $______ and $______, with an expected value of $______."
```

### Distribution Selection Guide

| Variable Type | Recommended Distribution | Parameters | When to Use |
|--------------|------------------------|------------|-------------|
| **Growth rate** | Normal | Mean, Std Dev | Symmetric uncertainty |
| **Market size** | Lognormal | Mean, Std Dev | Right-skewed, can't be negative |
| **Project cost** | Triangular | Min, Mode, Max | Expert estimates with bounds |
| **Binary events** | Bernoulli | Probability | Will/won't happen (regulation, deal) |
| **Time to event** | Exponential | Rate | Customer lifetime, time to churn |
| **Counts** | Poisson | Rate | Number of events in a period |

## Cash Flow Stress Testing

### Runway Calculator

```
CASH RUNWAY ANALYSIS:

Current cash:           $______
Monthly burn rate:      $______
Monthly revenue:        $______
Net monthly cash flow:  $______ (revenue - burn)

SCENARIO RUNWAYS:
  Current trajectory:   ______ months
  If revenue drops 20%: ______ months
  If revenue drops 50%: ______ months
  If revenue goes to 0: ______ months (pure burn runway)

TRIGGER POINTS:
  6-month runway remaining: Begin fundraise / cut costs
  3-month runway remaining: Emergency cost reduction
  1-month runway remaining: Wind-down planning

COST REDUCTION LEVERS (by impact):
  Lever                    | Monthly Savings | Feasibility
  Freeze hiring            | $______         | High
  Reduce marketing 50%     | $______         | Medium
  Renegotiate vendor terms  | $______         | Medium
  Reduce headcount 10%     | $______         | Low (last resort)
  Eliminate office space    | $______         | Medium
```

### Personal Finance Stress Test

```
PERSONAL FINANCIAL STRESS TEST:

INCOME SCENARIOS:
  Current income:          $______/month
  Reduced income (-20%):   $______/month
  Job loss (0 income):     $______/month
  Disability (partial):    $______/month

FIXED OBLIGATIONS:
  Housing (mortgage/rent): $______
  Insurance premiums:      $______
  Debt payments:           $______
  Utilities:               $______
  TOTAL FIXED:             $______

EMERGENCY RESERVES:
  Liquid savings:          $______
  Investment (accessible): $______
  Credit available:        $______
  TOTAL RESERVES:          $______

SURVIVAL METRICS:
  Months covered (fixed only):     ______
  Months covered (full spending):  ______
  Months if income drops 20%:      ______

  Target: 6+ months of full spending coverage

WHAT-IF ANALYSIS:
  "If [EVENT] happens, I can sustain for [N] months
   by cutting [EXPENSES] and drawing on [RESERVES]."
```

## Scenario Planning Process

### Workshop Format

```
SCENARIO PLANNING WORKSHOP:

PHASE 1: IDENTIFY UNCERTAINTIES (30 min)
  - List all factors that could impact the plan
  - Rate each: Impact (1-5) x Uncertainty (1-5)
  - Select top 2 with highest combined score
  - These become the axes of your scenario matrix

PHASE 2: BUILD SCENARIOS (45 min)
  Using the 2x2 matrix:

            Factor A: Low          Factor A: High
  Factor B:
  High      Scenario 1:            Scenario 2:
            [Name and narrative]    [Name and narrative]

  Factor B:
  Low       Scenario 3:            Scenario 4:
            [Name and narrative]    [Name and narrative]

PHASE 3: MODEL FINANCIALS (60 min)
  For each scenario:
  - Revenue projection (12-36 months)
  - Cost structure changes
  - Cash flow impact
  - Key metrics (CAC, LTV, margins)

PHASE 4: DEVELOP STRATEGIES (45 min)
  For each scenario:
  - What would we do differently?
  - What early warning signals would we see?
  - What decisions should we make now?
  - What options should we preserve?

PHASE 5: ACTION PLAN (30 min)
  - "No regret" moves (good in all scenarios)
  - Contingency triggers and responses
  - Monitoring dashboard design
  - Review cadence (quarterly recommended)
```

## Reporting Templates

### Scenario Summary for Stakeholders

```
FINANCIAL SCENARIO SUMMARY

Period: [Timeframe]
Prepared: [Date]
Author: [Name]

EXECUTIVE SUMMARY:
  [2-3 sentences: key finding and recommended action]

SCENARIO OUTCOMES:
                    Bear        Base        Bull
  Revenue:          $____       $____       $____
  EBITDA:           $____       $____       $____
  Cash (end):       $____       $____       $____
  Probability:      ____%       ____%       ____%
  Expected Value:   $____ (probability-weighted)

KEY RISKS:
  1. [Risk] — Impact: $____ — Mitigation: [Action]
  2. [Risk] — Impact: $____ — Mitigation: [Action]
  3. [Risk] — Impact: $____ — Mitigation: [Action]

RECOMMENDED ACTIONS:
  1. [No-regret move that's good in all scenarios]
  2. [Contingency to prepare now]
  3. [Decision to make by specific date]

MONITORING:
  KPI                  | Current | Trigger (Action Needed)
  Monthly revenue      | $____   | Below $____
  Cash runway          | ___ mo  | Below 6 months
  Customer churn       | ____%   | Above ____%
```

## See Also

- [Finance](../finance/SKILL.md)
- [Risk Management](../risk-management/SKILL.md)
- [Data Science](../data-science/SKILL.md)
