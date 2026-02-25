---
name: fundraising-analyzer
description: Nonprofit fundraising performance analysis with donor segmentation, campaign ROI, retention metrics, and trend analysis. Use when evaluating fundraising effectiveness, analyzing donor data, or planning campaigns.
---

# Fundraising Analyzer

Frameworks for analyzing nonprofit fundraising performance, segmenting donors, evaluating campaign effectiveness, and building data-driven fundraising strategies.

## Donor Analysis

### Donor Segmentation Framework

```
DONOR SEGMENTATION MATRIX:

BY GIVING LEVEL:
  Tier              | Annual Giving      | % of Donors | % of Revenue
  ------------------|--------------------| ------------|-------------
  Major donors      | $10,000+           | [%]         | [%]
  Mid-level donors  | $1,000 - $9,999    | [%]         | [%]
  Grassroots donors | $100 - $999        | [%]         | [%]
  Small donors      | Under $100         | [%]         | [%]

BY ENGAGEMENT:
  Segment           | Definition                    | Strategy
  ------------------|-------------------------------|------------------
  Champions         | Top 10% by giving + volunteer | Steward, recognize
  Loyal             | 3+ consecutive years giving   | Retain, upgrade
  Growing           | Increased gift this year      | Encourage, cultivate
  Lapsed risk       | Decreased gift or late renewal| Re-engage campaign
  Lapsed            | No gift in 13+ months         | Win-back campaign
  New               | First gift in last 12 months  | Welcome series

BY RECENCY-FREQUENCY-MONETARY (RFM):
  Score each 1-5:
  Recency:   How recently did they give? (5 = this month)
  Frequency: How often do they give?     (5 = monthly)
  Monetary:  How much do they give?      (5 = top tier)

  RFM Score  | Segment    | Priority
  555        | Best       | Highest — personal stewardship
  5XX        | Active     | High — upgrade opportunities
  X5X        | Frequent   | Medium — increase gift size
  XX5        | High value | High — increase frequency
  1XX        | At risk    | High — re-engagement needed
  111        | Lost       | Low — win-back or remove
```

### Donor Lifetime Value

```
DONOR LIFETIME VALUE (LTV) CALCULATOR:

INPUTS:
  Average annual gift:           $______
  Average giving years:          ______ years
  Donor retention rate:          ______%
  Discount rate:                 ______% (typically 5-8%)

SIMPLE LTV:
  LTV = Average annual gift × Average giving years
  LTV = $______ × ______ = $______

ADJUSTED LTV (with retention):
  LTV = Average gift × (Retention rate / (1 - Retention rate))
  LTV = $______ × (____% / (1 - ____%)) = $______

COST-ADJUSTED LTV:
  Acquisition cost:              $______
  Annual stewardship cost:       $______
  Net LTV = Adjusted LTV - Acquisition cost - (Stewardship × Years)
  Net LTV = $______

BY SEGMENT:
  Segment          | Avg Gift | Retention | LTV     | Acq Cost | Net LTV
  -----------------|----------|-----------|---------|----------|--------
  Major donors     | $______  | ____%     | $______ | $______  | $______
  Mid-level        | $______  | ____%     | $______ | $______  | $______
  Grassroots       | $______  | ____%     | $______ | $______  | $______
  Small            | $______  | ____%     | $______ | $______  | $______
```

## Campaign Analysis

### Campaign Performance Dashboard

```
CAMPAIGN REPORT: [Campaign Name]
Period: [Start Date] — [End Date]
Goal: $______

RESULTS:
  Revenue raised:       $______  (___% of goal)
  Number of gifts:      ______
  Average gift:         $______
  Median gift:          $______
  New donors acquired:  ______
  Returning donors:     ______

COST ANALYSIS:
  Total campaign cost:  $______
  Cost per dollar raised: $______
  Cost per acquisition:   $______
  ROI: (Revenue - Cost) / Cost = ______%

CHANNEL PERFORMANCE:
  Channel          | Revenue  | Gifts | Avg Gift | Cost    | ROI
  -----------------|----------|-------|----------|---------|-----
  Email            | $______  | _____ | $______  | $______ | ___%
  Direct mail      | $______  | _____ | $______  | $______ | ___%
  Social media     | $______  | _____ | $______  | $______ | ___%
  Website          | $______  | _____ | $______  | $______ | ___%
  Events           | $______  | _____ | $______  | $______ | ___%
  Phone/text       | $______  | _____ | $______  | $______ | ___%

YEAR-OVER-YEAR:
  Metric           | Last Year | This Year | Change
  Revenue          | $______   | $______   | ____%
  Donors           | ______    | ______    | ____%
  Avg gift         | $______   | $______   | ____%
  New donors       | ______    | ______    | ____%
```

### Campaign Comparison Matrix

| Metric | Spring Appeal | Year-End | Gala Event | Giving Tuesday | Peer-to-Peer |
|--------|-------------|----------|-----------|---------------|-------------|
| **Revenue** | $______ | $______ | $______ | $______ | $______ |
| **Cost** | $______ | $______ | $______ | $______ | $______ |
| **ROI** | ____% | ____% | ____% | ____% | ____% |
| **New donors** | ______ | ______ | ______ | ______ | ______ |
| **Avg gift** | $______ | $______ | $______ | $______ | $______ |

## Key Metrics

### Fundraising Health Scorecard

```
ANNUAL FUNDRAISING SCORECARD:

GROWTH METRICS:
  Total revenue:                  $______ (target: $______)
  Revenue growth (YoY):           ____%   (benchmark: 5-10%)
  Number of donors:               ______  (target: ______)
  Donor growth (YoY):             ____%   (benchmark: 5-8%)

RETENTION METRICS:
  Overall retention rate:         ____%   (benchmark: 45-50%)
  First-year donor retention:     ____%   (benchmark: 25-30%)
  Multi-year donor retention:     ____%   (benchmark: 60-65%)
  Donor upgrade rate:             ____%   (benchmark: 10-15%)
  Donor downgrade rate:           ____%   (target: <10%)

EFFICIENCY METRICS:
  Cost to raise a dollar:         $______ (benchmark: $0.20-0.30)
  Fundraising expense ratio:      ____%   (benchmark: <15%)
  Average gift size:              $______
  Revenue per donor:              $______
  Revenue per staff FTE:          $______

DIVERSITY METRICS:
  # of revenue sources:           ______  (target: 5+)
  Largest source % of total:      ____%   (target: <30%)
  Individual vs institutional:    ___% / ___%

HEALTH INDICATORS:
  ✓ Green:  Retention > 50%, Growth > 5%, Diversity > 5 sources
  △ Yellow: Retention 40-50%, Growth 0-5%, 3-4 sources
  ✗ Red:    Retention < 40%, Decline, < 3 sources
```

### Benchmark Comparison

| Metric | Your Org | Sector Avg | Top Quartile | Status |
|--------|---------|-----------|-------------|--------|
| Retention rate | ____% | 45% | 65%+ | |
| First-year retention | ____% | 27% | 40%+ | |
| Cost per dollar | $____ | $0.25 | <$0.15 | |
| Online giving % | ____% | 13% | 25%+ | |
| Major gift % | ____% | 60% | 75%+ | |
| Monthly giving % | ____% | 15% | 30%+ | |

## Trend Analysis

### Multi-Year Trend Template

```
5-YEAR FUNDRAISING TRENDS:

YEAR          | Y-4      | Y-3      | Y-2      | Y-1      | Current
              |----------|----------|----------|----------|--------
Revenue       | $______  | $______  | $______  | $______  | $______
Donors        | ______   | ______   | ______   | ______   | ______
Avg Gift      | $______  | $______  | $______  | $______  | $______
Retention     | ____%    | ____%    | ____%    | ____%    | ____%
New Donors    | ______   | ______   | ______   | ______   | ______
Lapsed Donors | ______   | ______   | ______   | ______   | ______

TREND ANALYSIS:
  Revenue trend:    [Increasing / Stable / Declining] at ___% annually
  Donor base trend: [Growing / Stable / Shrinking] at ___% annually
  Key concern:      [Identify the most worrying trend]
  Key strength:     [Identify the most positive trend]

PROJECTIONS (next 3 years):
  If current trends continue:
    Revenue Y+1: $______
    Revenue Y+2: $______
    Revenue Y+3: $______

  If retention improves by 5%:
    Revenue Y+1: $______
    Revenue Y+2: $______
    Revenue Y+3: $______
```

## Giving Strategy Templates

### Monthly Giving Program Analysis

```
MONTHLY GIVING PROGRAM:

CURRENT STATE:
  Monthly donors:           ______
  Average monthly gift:     $______
  Annual value per donor:   $______ (monthly × 12)
  Total annual revenue:     $______
  % of total fundraising:   ____%
  Retention rate:           ____%  (benchmark: 80-90%)

GROWTH ANALYSIS:
  New monthly donors (this year):    ______
  Upgraded from one-time:            ______
  Cancelled:                         ______
  Net change:                        ______

UPGRADE OPPORTUNITIES:
  Donors giving < $25/month:         ______ → Upgrade to $35
  Donors giving $25-49/month:        ______ → Upgrade to $50
  Donors giving $50-99/month:        ______ → Upgrade to $100
  Potential revenue increase:        $______/year

ACQUISITION CHANNELS:
  Channel              | Conversions | Avg Gift | Cost/Acquisition
  Website popup        | ______      | $______  | $______
  Email campaign       | ______      | $______  | $______
  Direct mail insert   | ______      | $______  | $______
  Thank-you page upsell| ______      | $______  | $______
```

### Major Gift Pipeline

```
MAJOR GIFT PIPELINE: FY[Year]

STAGE           | # Prospects | Total Value | Avg Gift  | Probability
----------------|-------------|-------------|-----------|------------
Identification  | ______      | $______     | $______   | 10%
Qualification   | ______      | $______     | $______   | 25%
Cultivation     | ______      | $______     | $______   | 50%
Solicitation    | ______      | $______     | $______   | 75%
Closed          | ______      | $______     | $______   | 100%

WEIGHTED PIPELINE VALUE:
  = Σ (Value at each stage × Probability)
  = $______

PIPELINE METRICS:
  Average cultivation time:    ______ months
  Close rate (solicited):      ____%
  Average solicitation:        $______
  Average closed gift:         $______
  Gifts above ask:             ____%
  Gifts below ask:             ____%
```

## See Also

- [Impact Report Writer](../impact-report-writer/SKILL.md)
- [Grant Proposal Builder](../grant-proposal-builder/SKILL.md)
- [Volunteer Coordinator](../volunteer-coordinator/SKILL.md)
