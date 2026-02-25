---
name: real-estate-analyzer
description: Property valuation, market analysis, investment ROI calculations, comparable analysis, and rental yield assessment. Use when evaluating real estate investments, analyzing property markets, or calculating returns.
---

# Real Estate Analyzer

Comprehensive frameworks for property valuation, investment analysis, and market assessment.

## Property Valuation Methods

### Comparable Sales Approach (CMA)

The most common method for residential properties. Relies on recent sales of similar properties.

```
COMPARABLE SELECTION CRITERIA:
1. Location: Same neighborhood or within 1 mile
2. Recency: Sold within last 6 months (3 months preferred)
3. Size: Within 10-20% of subject GLA (gross living area)
4. Condition: Similar age, updates, and maintenance
5. Style: Same property type (SFH, condo, townhome)
6. Lot: Similar lot size and features

ADJUSTMENT CATEGORIES:
+ / - Location premium/discount
+ / - Size differential ($X per sq ft)
+ / - Bedroom/bathroom count
+ / - Garage, pool, upgrades
+ / - Lot size difference
+ / - Condition adjustment
= Adjusted Comparable Value
```

### Comparable Property Analysis Template

| Factor           | Subject | Comp 1 | Adj 1 | Comp 2 | Adj 2 | Comp 3 | Adj 3 |
| ---------------- | ------- | ------ | ----- | ------ | ----- | ------ | ----- |
| Sale Price       | --      |        |       |        |       |        |       |
| Sale Date        | --      |        |       |        |       |        |       |
| Distance (mi)    | --      |        |       |        |       |        |       |
| GLA (sq ft)      |         |        |       |        |       |        |       |
| Lot Size         |         |        |       |        |       |        |       |
| Year Built       |         |        |       |        |       |        |       |
| Bedrooms         |         |        |       |        |       |        |       |
| Bathrooms        |         |        |       |        |       |        |       |
| Garage           |         |        |       |        |       |        |       |
| Condition        |         |        |       |        |       |        |       |
| Pool/Upgrades    |         |        |       |        |       |        |       |
| **Adj. Price**   | --      |        |       |        |       |        |       |
| **Price/Sq Ft**  | --      |        |       |        |       |        |       |

### Income Approach (Cap Rate)

Primary method for commercial and multi-family investment properties.

```
NET OPERATING INCOME (NOI):
Gross Potential Rent (GPR)
+ Other Income (laundry, parking, storage)
= Gross Potential Income (GPI)
- Vacancy & Credit Loss (typically 5-10%)
= Effective Gross Income (EGI)
- Operating Expenses
  - Property taxes
  - Insurance
  - Management fees (8-12%)
  - Maintenance & repairs
  - Utilities (owner-paid)
  - Landscaping
  - Reserves for replacement (3-5%)
= NET OPERATING INCOME (NOI)

PROPERTY VALUE = NOI / Cap Rate
```

### Cap Rate Calculator

| Property Type      | Typical Cap Rate | Risk Profile |
| ------------------ | ---------------- | ------------ |
| Class A Multifamily | 4.0-5.5%        | Low          |
| Class B Multifamily | 5.5-7.0%        | Low-Medium   |
| Class C Multifamily | 7.0-9.0%        | Medium       |
| Retail (NNN)       | 5.0-7.0%        | Medium       |
| Office (Class A)   | 5.5-7.5%        | Medium       |
| Industrial         | 5.0-7.0%        | Low-Medium   |
| Self-Storage       | 5.5-8.0%        | Medium       |
| Hotels             | 8.0-12.0%       | High         |

### Cost Approach

Used for unique properties, new construction, or insurance purposes.

```
COST APPROACH:
Land Value (from comparable land sales)
+ Replacement Cost New (current construction cost)
- Depreciation
  - Physical (age, wear)
  - Functional (outdated features)
  - External/Economic (market decline, location)
= ESTIMATED PROPERTY VALUE
```

## Investment Return Calculations

### Cash-on-Cash Return

```
ANNUAL CASH-ON-CASH RETURN:
Annual Pre-Tax Cash Flow / Total Cash Invested x 100

TOTAL CASH INVESTED:
Down Payment
+ Closing Costs
+ Rehab/Renovation Costs
+ Initial Reserves
= Total Cash Invested

ANNUAL PRE-TAX CASH FLOW:
NOI
- Annual Debt Service (mortgage payments)
= Pre-Tax Cash Flow

Target: 8-12% for buy-and-hold residential
```

### Rental Yield Analysis

| Metric             | Formula                                    | Good Target |
| ------------------ | ------------------------------------------ | ----------- |
| Gross Yield        | Annual Rent / Purchase Price               | 8-12%       |
| Net Yield          | NOI / Purchase Price                       | 5-8%        |
| Cap Rate           | NOI / Current Market Value                 | 5-10%       |
| Cash-on-Cash       | Cash Flow / Cash Invested                  | 8-12%       |
| DSCR               | NOI / Annual Debt Service                  | 1.25x+      |
| Price-to-Rent      | Purchase Price / Annual Rent               | 10-15x      |
| GRM                | Purchase Price / Gross Annual Income       | 8-12x       |

### Full Investment Return Template

```
PURCHASE ANALYSIS:
Purchase Price:              $__________
Down Payment (___%):         $__________
Loan Amount:                 $__________
Closing Costs:               $__________
Renovation Budget:           $__________
Total Cash Required:         $__________

MONTHLY INCOME:
Gross Monthly Rent:          $__________
Other Income:                $__________
Vacancy (___% of GMR):     ($__________)
Effective Monthly Income:    $__________

MONTHLY EXPENSES:
Mortgage (P&I):              $__________
Property Tax:                $__________
Insurance:                   $__________
HOA/Condo Fees:              $__________
Property Management:         $__________
Maintenance Reserve:         $__________
Utilities (owner-paid):      $__________
Total Monthly Expenses:      $__________

MONTHLY CASH FLOW:           $__________
ANNUAL CASH FLOW:            $__________
CASH-ON-CASH RETURN:         ____%

5-YEAR PROJECTION:
Year 1 Cash Flow:            $__________
Cumulative CF (5 yr):        $__________
Equity Built (5 yr):         $__________
Appreciation (___/yr):       $__________
Total Return (5 yr):         $__________
Annualized ROI:              ____%
```

## Mortgage Payment Framework

```
MONTHLY PAYMENT (P&I):
M = P [ r(1+r)^n ] / [ (1+r)^n - 1 ]

Where:
  M = Monthly payment
  P = Loan principal
  r = Monthly interest rate (annual / 12)
  n = Total number of payments (years x 12)

AMORTIZATION SNAPSHOT (Year 1 vs Year 15 vs Year 30):
| Period  | Payment | Principal | Interest | Balance   |
| ------- | ------- | --------- | -------- | --------- |
| Month 1 |         |           |          |           |
| Year 5  |         |           |          |           |
| Year 10 |         |           |          |           |
| Year 15 |         |           |          |           |
| Year 30 |         |           |          |           |
```

## Market Analysis Framework

### Market Fundamentals Assessment

| Factor               | Metric                     | Data Source                 | Signal      |
| -------------------- | -------------------------- | -------------------------- | ----------- |
| Population Growth    | Annual % change            | Census, BLS                | > 1% = good |
| Job Growth           | YoY employment change      | BLS, local data            | > 2% = good |
| Median Income Growth | YoY change                 | Census ACS                 | > 3% = good |
| Supply Pipeline      | Permits issued             | Census, HUD                | Monitor     |
| Vacancy Rate         | % of units unoccupied      | Census, CoStar             | < 5% = good |
| Days on Market       | Average DOM                | MLS data                   | < 30 = hot  |
| Price-to-Income      | Median Price / Median Income | Zillow, Census           | < 4x = affordable |
| Rent-to-Income       | Monthly Rent / Monthly Income | HUD, local data         | < 30% = sustainable |

### Neighborhood Scoring Matrix

| Category        | Weight | Factors to Evaluate                         | Score (1-10) |
| --------------- | ------ | ------------------------------------------- | ------------ |
| Employment      | 25%    | Job diversity, major employers, growth      |              |
| Schools         | 20%    | Ratings, proximity, district reputation     |              |
| Safety          | 15%    | Crime stats, trends, perception             |              |
| Infrastructure  | 15%    | Transit, roads, walkability, internet       |              |
| Amenities       | 10%    | Retail, dining, parks, healthcare           |              |
| Growth Trend    | 10%    | New development, rezoning, investment       |              |
| Affordability   | 5%     | Price relative to metro, rent trends        |              |
| **Total Score** | 100%   |                                             |              |

## Investment Property Scorecard

```
PROPERTY SCORECARD:
Score each factor 1-5, multiply by weight.

| Factor               | Weight | Score | Weighted |
| -------------------- | ------ | ----- | -------- |
| Location Quality     | 20%    |       |          |
| Cash Flow Potential  | 20%    |       |          |
| Appreciation Outlook | 15%    |       |          |
| Condition / CapEx    | 15%    |       |          |
| Tenant Demand        | 10%    |       |          |
| Financing Terms      | 10%    |       |          |
| Management Burden    | 10%    |       |          |
| TOTAL                | 100%   |       | __ / 5.0 |

RATING:
4.0-5.0  Strong Buy
3.0-3.9  Buy / Hold
2.0-2.9  Hold / Caution
< 2.0    Pass
```

## Due Diligence Checklist

### Pre-Offer

- [ ] Run comparable sales analysis (3-6 recent comps)
- [ ] Verify rental income (request rent rolls, leases)
- [ ] Calculate NOI, cap rate, and cash-on-cash return
- [ ] Check zoning and permitted use
- [ ] Review neighborhood crime statistics
- [ ] Confirm flood zone and insurance requirements
- [ ] Estimate renovation/repair costs

### Under Contract

- [ ] Order professional inspection (structural, roof, HVAC, plumbing, electrical)
- [ ] Order appraisal
- [ ] Review title report and survey
- [ ] Verify property taxes and assessment history
- [ ] Obtain insurance quotes
- [ ] Review HOA documents (if applicable)
- [ ] Confirm utility costs (12-month history)
- [ ] Environmental assessment (Phase I if commercial)
- [ ] Verify all permits for past renovations
- [ ] Review tenant leases and estoppel certificates

### Pre-Closing

- [ ] Final walk-through inspection
- [ ] Confirm financing terms and closing costs
- [ ] Set up property management (if using)
- [ ] Transfer utilities and insurance
- [ ] Prepare lease agreements for vacant units

## 1031 Exchange Overview

```
1031 LIKE-KIND EXCHANGE:
Defer capital gains tax by reinvesting proceeds into "like-kind" property.

KEY RULES:
- 45-day identification period (ID up to 3 properties)
- 180-day closing deadline
- Must use Qualified Intermediary (QI)
- Equal or greater value and debt required
- Same taxpayer name on both transactions
- Cannot receive "boot" (cash or unlike property)

IDENTIFICATION RULES:
1. Three Property Rule: ID up to 3 properties of any value
2. 200% Rule: ID any number, but FMV cannot exceed 200% of relinquished
3. 95% Rule: ID any number if you acquire 95%+ of identified value

COMMON PITFALLS:
- Missing the 45-day or 180-day deadline
- Touching proceeds (must go through QI)
- Attempting related-party exchanges
- Not matching debt levels (creates taxable boot)
- Mixing personal use with investment use
```

## Quick Reference: The 1% and 2% Rules

```
1% RULE (screening test):
Monthly Rent >= 1% of Purchase Price
$200,000 property should rent for >= $2,000/month

2% RULE (strong cash flow):
Monthly Rent >= 2% of Purchase Price
Rarely achievable in appreciating markets

50% RULE (expense estimate):
Operating expenses = ~50% of gross rent (excluding mortgage)
Quick NOI estimate = Gross Rent x 0.50

70% RULE (for flips):
Max Purchase = (ARV x 70%) - Repair Costs
ARV = After Repair Value
```

## See Also

- [Finance](../finance/SKILL.md)
- [Risk Management](../risk-management/SKILL.md)
- [Investment Memo Generator](../investment-memo-generator/SKILL.md)
