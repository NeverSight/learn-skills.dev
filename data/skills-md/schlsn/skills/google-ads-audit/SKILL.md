---
name: google-ads-audit
description: Comprehensive Google Ads account audit with actionable recommendations. Use when user wants to audit, analyze, or review a Google Ads account, campaigns, or performance. Triggers include requests to audit account structure, analyze Quality Score, review keywords and search terms, evaluate ads and extensions, check landing pages, identify optimization opportunities, find wasted spend, or create improvement roadmaps. Supports CSV/Excel exports from Google Ads or direct data input.
---

# Google Ads Account Audit

Perform comprehensive Google Ads audits producing prioritized, actionable recommendations.

## Workflow Overview

1. **Data intake** - Load and parse Google Ads export data
2. **Structure analysis** - Evaluate naming conventions and organization
3. **Quality Score audit** - Calculate weighted QS, find optimization opportunities
4. **Keyword & Search Term analysis** - Identify waste and scaling opportunities
5. **Ad evaluation** - Check RSA adoption, Ad Strength, relevance
6. **Extensions audit** - Verify coverage across campaigns
7. **Display/Placement review** - Analyze placement distribution (if applicable)
8. **Landing page assessment** - Evaluate relevance and best practices
9. **Anomaly detection** - Flag unusual patterns
10. **Generate outputs** - Create roadmap document + Excel summary

## Data Sources

### Option 1: Manual CSV Export

Request these reports from Google Ads (CSV/Excel):

| Report | Required Columns |
|--------|-----------------|
| Campaigns | Campaign, Type, Status, Cost, Conversions, Conv. Value, Impressions, Clicks, Impr. Share |
| Ad Groups | Campaign, Ad Group, Status, Cost, Conversions, CPA, Clicks, Impr. Share |
| Keywords | Campaign, Ad Group, Keyword, Match Type, Status, QS, Cost, Conversions, CPA, Clicks, Impressions, Impr. Share |
| Search Terms | Campaign, Ad Group, Search Term, Match Type, Cost, Conversions, CPA, Clicks, Added/Excluded |
| Ads | Campaign, Ad Group, Ad Type, Status, Ad Strength, Headlines, Descriptions, Final URL |
| Extensions | Campaign, Extension Type, Status |
| Placements (Display) | Campaign, Placement, Type, Cost, Conversions |

### Option 2: Google Ads API (Recommended)

For automated data extraction, see [references/google-ads-api.md](references/google-ads-api.md).

Benefits:
- Complete data without manual export
- Consistent column naming
- Can include historical comparisons
- Automatable for recurring audits

## Analysis Modules

### 1. Account Structure & Naming

Evaluate naming conventions for clarity:
- **Brand vs Non-brand** - Clear separation (e.g., `[Brand]`, `[NB]`, `_brand_`, `_generic_`)
- **Campaign types** - Identifiable (Search, Display, PMax, Shopping)
- **Geographic/Language** - If applicable, marked in names
- **Consistency** - Same pattern across account

**Output**: Structure score (1-10) + specific naming issues

### 2. Quality Score Analysis

See [references/quality-score.md](references/quality-score.md) for weighted average calculation and distribution analysis.

Key outputs:
- **QS Distribution**: Cost/Conv % by QS level (1-10)
- **Efficiency analysis**: Low QS (1-6) vs High QS (7-10) spend efficiency
- Weighted QS by campaign and ad group
- High-spend + low-QS keywords (improvement opportunities)
- QS component breakdown (Expected CTR, Ad Relevance, Landing Page)
- Estimated savings from QS improvements

Typical finding: 31% cost on QS < 7 yields only 19% conversions

### 3. Keywords & Search Terms

See [references/keyword-analysis.md](references/keyword-analysis.md) for detailed methodology.

Identify:
- **Pause candidates**: High spend, low/no conversions, high CPA
- **Scale candidates**: Low CPA + low impression share
- **Zero-impression keywords**: No activity in analysis period
- **Keyword overlap**: Same keywords across ad groups
- **Search term relevance**: Deviation from target keywords

### 3b. Match Type & Cross-Campaign Overlap

See [references/match-type-overlap.md](references/match-type-overlap.md) for detailed analysis.

**Match Type Performance**:
- Analyze cost vs conversion distribution by match type
- Calculate efficiency ratio (Conv% / Cost%)
- Typical finding: Exact match delivers 70% conv for 45% cost

**Cross-Campaign Overlap**:
- Detect same search terms triggering multiple campaigns
- Identify brand terms leaking to generic campaigns
- Find cannibalization between campaigns

**Recommendations focus**:
- Increase exact match keyword coverage
- Add negative keywords for brand protection
- Use phrase match for specific, high-intent terms

### 4. Ads Evaluation

See [references/ads-evaluation.md](references/ads-evaluation.md) for detailed methodology.

**RSA Count Analysis**:
- Check RSA count per ad group (target: 1-2 max)
- Flag ad groups with 3+ RSAs (data dilution)

**Ad Strength Distribution**:
- Analyze spend % by Ad Strength rating
- Typical issue: 52% spend on Poor RSAs, only 5% on Excellent/Good
- Priority: Optimize RSAs with high spend + low strength

Check for each campaign/ad group:
- RSA adoption (best practice = RSA only, no legacy ETA)
- Ad Strength rating (Poor/Average/Good/Excellent)
- Number of headlines (target: 15) and descriptions (target: 4)
- Pin usage (excessive pinning = Bad)

**LLM Relevance Check**: Compare ad copy to ad group keywords:
- Headlines contain target keywords or close variants?
- Descriptions address user intent?
- CTAs present and clear?

**Recommendations**:
- Optimize Poor/Average RSAs to Good/Excellent
- Add more headlines/descriptions with keywords
- Reduce RSA count to 1-2 per ad group
- Keep high-performing legacy ETAs if data supports

### 5. Extensions Audit

See [references/extensions-placements.md](references/extensions-placements.md) for coverage matrix and best practices.

Required extensions per campaign type:

| Extension | Search | Display | PMax |
|-----------|--------|---------|------|
| Sitelinks | ✓ | - | ✓ |
| Callouts | ✓ | - | ✓ |
| Structured Snippets | ✓ | - | - |
| Call | Industry-dependent | - | - |
| Location | Local business | - | ✓ |
| Image | ✓ | - | - |

**Output**: Missing extensions matrix

### 6. Display Placements (if applicable)

See [references/extensions-placements.md](references/extensions-placements.md) for placement categorization.

Analyze placement distribution:
- % spend on apps vs websites vs YouTube
- High-spend low-converting placements
- Placement exclusion recommendations

### 7. Landing Pages

Evaluate:
- URL diversity (one URL vs personalized per ad group)
- HTTPS usage
- Page load indicators (if available)
- Keyword relevance to landing page (from URL/path analysis)

### 8. Rejected Items

List all disapproved:
- Ads
- Keywords
- Extensions

With rejection reasons and fix recommendations.

### 9. Anomaly Detection

Flag:
- Sudden spend spikes in search terms
- New high-volume search terms
- CTR anomalies (very high or very low)
- CPA outliers

## Key Metrics Reference

| Metric | Good | Warning | Bad |
|--------|------|---------|-----|
| Quality Score | ≥7 | 5-6 | ≤4 |
| Search Impr. Share | >80% | 50-80% | <50% |
| CTR (Search) | >5% | 2-5% | <2% |
| Ad Strength | Excellent/Good | Average | Poor |

## Output Generation

### 1. Executive Summary (Markdown/DOCX)

Structure:
```
# Google Ads Audit: [Account Name]
Date: [Date]

## Executive Summary
[2-3 sentence overview of account health]

## Priority Roadmap
### Immediate (This Week)
1. [Action] - [Impact] - [Effort]
...

### Short-term (This Month)
...

### Medium-term (This Quarter)
...

## Detailed Findings
[Section per analysis module]

## Appendix
[Methodology notes]
```

### 2. Excel Workbook

Create workbook with sheets:
- **Summary** - Key metrics dashboard
- **Structure** - Naming issues
- **Quality Score** - Weighted QS by campaign/ad group
- **Keywords** - Pause/scale recommendations
- **Search Terms** - Top spenders + relevance
- **Ads** - Ad Strength + recommendations
- **Extensions** - Coverage matrix
- **Placements** - If Display campaigns present
- **Roadmap** - Prioritized actions

See [references/excel-template.md](references/excel-template.md) for column specifications.

## Priority Scoring

Score each recommendation:
- **Impact**: High (3) / Medium (2) / Low (1)
- **Effort**: Low (3) / Medium (2) / High (1)
- **Priority Score** = Impact × Effort

Sort roadmap by priority score descending.
