---
name: gaql-query-patterns
description: Reusable GAQL query templates for Google Ads API. Auto-invoke when writing Google Ads queries, analyzing campaign data, querying performance metrics, or building custom reports.
---

# GAQL Query Patterns

Ready-to-use GAQL (Google Ads Query Language) query templates for common PPC analysis tasks.

## What This Skill Deliberately Does NOT Do

- **Run the queries.** These are copy-paste templates, not a runner — paste them into your own API client, Google Ads Scripts, or [`google-ads-query`](../google-ads-query/) to actually execute and export.
- **Mutate anything.** Every template is a read-only `SELECT`; nothing here changes an account.
- **Cover change-history queries.** Pulling what changed and when needs a finite date window and a `LIMIT`, and lives in [`change-history-checker`](../change-history-checker/) — a windowless change query won't run.
- **Diagnose the results.** The "Use for" and "Interpreting results" notes point you at the analysis; the actual root-causing lives in the diagnostic skills (e.g. [`impression-share-diagnostics`](../impression-share-diagnostics/) for the impression-share query).

---

## Campaign Queries

### 7-Day Campaign Spend Analysis

```sql
SELECT
    campaign.id,
    campaign.name,
    campaign.status,
    campaign.advertising_channel_type,
    campaign.bidding_strategy_type,
    campaign_budget.amount_micros,
    campaign_budget.explicitly_shared,
    metrics.cost_micros,
    metrics.impressions,
    metrics.clicks,
    metrics.conversions,
    metrics.conversions_value
FROM campaign
WHERE segments.date DURING LAST_7_DAYS
ORDER BY campaign.name
```

**Use for:** Recent spend analysis, budget utilization, campaign health checks

---

### Month-to-Date Pacing

```sql
SELECT
    campaign.id,
    campaign.name,
    campaign_budget.amount_micros,
    metrics.cost_micros
FROM campaign
WHERE segments.date DURING THIS_MONTH
ORDER BY campaign.name
```

**Use for:** Monthly pacing calculations, budget tracking

---

### Campaign Settings Audit

```sql
SELECT
    campaign.id,
    campaign.name,
    campaign.status,
    campaign.advertising_channel_type,
    campaign.bidding_strategy_type,
    campaign.target_cpa.target_cpa_micros,
    campaign.target_roas.target_roas,
    campaign_budget.amount_micros,
    campaign_budget.explicitly_shared
FROM campaign
WHERE campaign.status = 'ENABLED'
```

**Use for:** Configuration audits, bidding strategy checks, budget review

---

## Impression Share

### Search Impression Share Analysis

```sql
SELECT
    campaign.id,
    campaign.name,
    campaign.advertising_channel_type,
    metrics.search_impression_share,
    metrics.search_budget_lost_impression_share,
    metrics.search_rank_lost_impression_share,
    metrics.impressions
FROM campaign
WHERE segments.date DURING LAST_7_DAYS
  AND campaign.advertising_channel_type IN ('SEARCH', 'PERFORMANCE_MAX')
ORDER BY metrics.search_budget_lost_impression_share DESC
```

**Use for:** Diagnosing underspending, identifying budget constraints vs. quality issues

**Interpreting results:**
- High Budget Lost IS → increase budget to capture more impressions
- High Rank Lost IS → quality/relevance issue (not a budget problem)
- Both high → budget is primary constraint, but quality also needs work

---

## Search Terms

### Search Term Report (Last 30 Days)

```sql
SELECT
    search_term_view.search_term,
    campaign.name,
    ad_group.name,
    metrics.impressions,
    metrics.clicks,
    metrics.cost_micros,
    metrics.conversions,
    search_term_view.status
FROM search_term_view
WHERE segments.date DURING LAST_30_DAYS
  AND metrics.impressions > 0
ORDER BY metrics.cost_micros DESC
```

**Use for:** Negative keyword discovery, search term audits, intent analysis

---

### High-Spend Non-Converting Search Terms

```sql
SELECT
    search_term_view.search_term,
    campaign.name,
    metrics.clicks,
    metrics.cost_micros,
    metrics.conversions
FROM search_term_view
WHERE segments.date DURING LAST_30_DAYS
  AND metrics.conversions = 0
  AND metrics.cost_micros > 0
ORDER BY metrics.cost_micros DESC
```

**Use for:** Finding wasted spend, negative keyword candidates

---

## Keywords

### Keyword Performance with Quality Score

```sql
SELECT
    ad_group.name,
    ad_group_criterion.keyword.text,
    ad_group_criterion.keyword.match_type,
    ad_group_criterion.quality_info.quality_score,
    ad_group_criterion.quality_info.creative_quality_score,
    ad_group_criterion.quality_info.post_click_quality_score,
    ad_group_criterion.quality_info.search_predicted_ctr,
    metrics.impressions,
    metrics.clicks,
    metrics.cost_micros,
    metrics.conversions
FROM keyword_view
WHERE segments.date DURING LAST_30_DAYS
  AND ad_group_criterion.status = 'ENABLED'
ORDER BY metrics.cost_micros DESC
```

**Use for:** Quality score audits, keyword performance analysis

---

### Non-Serving Keywords (Zero Impressions)

```sql
SELECT
    campaign.name,
    ad_group.name,
    ad_group_criterion.keyword.text,
    ad_group_criterion.keyword.match_type,
    ad_group_criterion.status,
    metrics.impressions
FROM keyword_view
WHERE segments.date DURING LAST_180_DAYS
  AND campaign.status = 'ENABLED'
  AND ad_group.status = 'ENABLED'
  AND ad_group_criterion.status = 'ENABLED'
  AND metrics.impressions = 0
```

**Use for:** Finding dead keywords to clean up, account hygiene

---

## Ads

### RSA Performance

```sql
SELECT
    campaign.name,
    ad_group.name,
    ad_group_ad.ad.id,
    ad_group_ad.ad.responsive_search_ad.headlines,
    ad_group_ad.ad.responsive_search_ad.descriptions,
    ad_group_ad.ad_strength,
    metrics.impressions,
    metrics.clicks,
    metrics.conversions,
    metrics.cost_micros
FROM ad_group_ad
WHERE segments.date DURING LAST_30_DAYS
  AND ad_group_ad.ad.type = 'RESPONSIVE_SEARCH_AD'
  AND ad_group_ad.status = 'ENABLED'
ORDER BY metrics.impressions DESC
```

**Use for:** Ad performance review, RSA optimization

---

## Conversions

### Conversion Actions List

```sql
SELECT
    conversion_action.id,
    conversion_action.name,
    conversion_action.type,
    conversion_action.status,
    conversion_action.category,
    conversion_action.value_settings.default_value,
    conversion_action.counting_type,
    conversion_action.attribution_model_settings.attribution_model
FROM conversion_action
WHERE conversion_action.status = 'ENABLED'
ORDER BY conversion_action.name
```

**Use for:** Conversion tracking audits, identifying misconfigured actions

---

### Conversion Performance by Action

```sql
SELECT
    segments.conversion_action_name,
    segments.conversion_action_category,
    metrics.conversions,
    metrics.conversions_value,
    metrics.all_conversions,
    metrics.cost_micros
FROM campaign
WHERE segments.date DURING LAST_30_DAYS
ORDER BY metrics.conversions DESC
```

**Use for:** Understanding which conversion actions are firing, value distribution

---

## Geographic Performance

```sql
SELECT
    geographic_view.country_criterion_id,
    geographic_view.location_type,
    campaign.name,
    metrics.impressions,
    metrics.clicks,
    metrics.cost_micros,
    metrics.conversions
FROM geographic_view
WHERE segments.date DURING LAST_30_DAYS
ORDER BY metrics.cost_micros DESC
```

**Use for:** Geographic bid adjustments, location targeting audits

---

## Device Performance

```sql
SELECT
    campaign.name,
    segments.device,
    metrics.impressions,
    metrics.clicks,
    metrics.cost_micros,
    metrics.conversions,
    metrics.average_cpc
FROM campaign
WHERE segments.date DURING LAST_30_DAYS
ORDER BY campaign.name, segments.device
```

**Use for:** Device bid adjustments, mobile vs. desktop analysis

---

## Account-Level Summary

```sql
SELECT
    customer.id,
    customer.descriptive_name,
    metrics.cost_micros,
    metrics.impressions,
    metrics.clicks,
    metrics.conversions,
    metrics.conversions_value
FROM customer
WHERE segments.date DURING LAST_30_DAYS
```

**Use for:** High-level account overview, executive reporting

---

## Date Range Reference

| Keyword | Meaning |
|---------|---------|
| `YESTERDAY` | Yesterday only |
| `TODAY` | Today only |
| `LAST_7_DAYS` | Last 7 days |
| `LAST_14_DAYS` | Last 14 days |
| `LAST_30_DAYS` | Last 30 days |
| `THIS_MONTH` | Current month to date |
| `LAST_MONTH` | Previous calendar month |
| `THIS_WEEK_MON_TODAY` | This week (Monday to today) |

---

## Key Field Notes

### Micros Conversion
The API returns monetary values in **micros** (1,000,000 = $1):
```
50000000 micros = $50.00
1234567 micros = $1.23
```
Always divide by 1,000,000 when displaying to users.

### Impression Share Returns Decimals
The API returns impression share as **decimals (0.0 - 1.0)**, NOT percentages:
- API value `0.2464` = **24.64%** actual impression share
- Always multiply by 100 when displaying

### Metrics Require Date Segmentation
Any query with `metrics.*` fields MUST include a `WHERE segments.date` clause. Without it, the query will fail.

### Impression Share is Search/PMax Only
`search_impression_share`, `search_budget_lost_impression_share`, and `search_rank_lost_impression_share` are only available for Search and Performance Max campaigns.

### AND vs OR
GAQL doesn't support `OR`. Use `IN` instead:
```sql
-- Wrong
WHERE campaign.status = 'ENABLED' OR campaign.status = 'PAUSED'

-- Correct
WHERE campaign.status IN ('ENABLED', 'PAUSED')
```

---

## When to Load Other Skills

| Skill | When |
|-------|------|
| [`google-ads-query`](../google-ads-query/) | To run these templates against an account and export the results to CSV — this skill is the templates, that one is the runner |
| [`change-history-checker`](../change-history-checker/) | For "what changed and when" queries — they require a finite date window (90-day / 30-day) and a `LIMIT` that these general templates don't carry |
| [`impression-share-diagnostics`](../impression-share-diagnostics/) | To interpret the impression-share query — Search IS, Budget Lost IS, and Rank Lost IS root-causing lives there |

Several skills reach for these templates when they outgrow their own — [`underspending-investigation`](../underspending-investigation/), [`budget-recommendation-calculator`](../budget-recommendation-calculator/), and [`mcc-hack-audit`](../mcc-hack-audit/) all point back here for custom GAQL.
