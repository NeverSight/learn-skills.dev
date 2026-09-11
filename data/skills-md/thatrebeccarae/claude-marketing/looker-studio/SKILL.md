---
name: looker-studio
description: Looker Studio (formerly Google Data Studio) expertise. Build dashboards, design data visualizations, connect data sources, and create marketing reports. Use when the user asks about Looker Studio, Data Studio, marketing dashboards, data visualization, report building, or connecting analytics data sources.
license: MIT
origin: custom
author: Rebecca Rae Barton
author_url: https://github.com/thatrebeccarae
metadata:
  version: 1.0.0
  category: analytics
  domain: looker-studio
  updated: 2026-02-23
  tested: 2026-03-17
  tested_with: "Claude Code v2.1"
---

# Looker Studio (Google Data Studio)

Expert-level guidance for Looker Studio — building dashboards, connecting data sources, designing visualizations, and creating automated marketing reports.

## Install

```bash
git clone https://github.com/thatrebeccarae/claude-marketing.git && cp -r claude-marketing/skills/looker-studio ~/.claude/skills/
```

## Core Capabilities

### Dashboard Design
- Layout and visual hierarchy best practices
- Executive summary vs detailed operational dashboards
- Mobile-responsive report design
- Interactive controls: date range selectors, filters, drill-downs
- Consistent styling with themes and color palettes

### Data Sources & Connectors
- **Native (free)**: Google Analytics 4, Google Ads, Google Sheets, BigQuery, Search Console, YouTube Analytics
- **Partner connectors**: Facebook Ads, Microsoft Ads, LinkedIn Ads, HubSpot, Salesforce, Shopify, Klaviyo, Semrush
- **Community connectors**: Hundreds of third-party sources
- **Data blending**: Join multiple sources on shared dimensions
- **Custom queries**: BigQuery SQL, Google Sheets formulas as data sources

### Calculated Fields & Metrics
- Regex-based field creation (REGEXP_MATCH, REGEXP_REPLACE, REGEXP_EXTRACT)
- CASE statements for custom groupings and bucketing
- Date functions for period-over-period comparisons
- Aggregation (SUM, AVG, COUNT_DISTINCT, MEDIAN)
- Blended field calculations across sources

#### Formula Syntax Rules
- **No comments allowed** — Looker Studio formulas do not support `--`, `//`, or `/* */` style comments. Never include comments in formulas. Add context in the field description instead.
- **No inline flags in simple cases** — prefer `CONTAINS_TEXT()`, `LOWER()`, or exact match over regex when possible
- **RE2 regex engine** — supports `(?i)` for case-insensitive, but does NOT support lookaheads/lookbehinds
- **String escaping** — use `\\` for literal backslash in regex patterns within string literals (e.g., `"\\s"` for whitespace, `"\\|"` for literal pipe)

### Report Automation
- Scheduled email delivery (PDF snapshots)
- Embedded reports in websites and portals
- Template reports for client scaling
- Data freshness monitoring

## Dashboard Templates by Use Case

### Marketing Performance Dashboard
```
Page 1: Executive Summary
|- KPI scorecards (Revenue, ROAS, CPA, Spend, Conversions)
|- Period-over-period trend lines
|- Channel performance table (sortable)
|- Budget pacing gauge chart

Page 2: Paid Media Deep-Dive
|- Google Ads performance (campaign breakdown)
|- Meta Ads performance (campaign breakdown)
|- Microsoft Ads performance
|- Cross-channel spend allocation (pie/donut)
|- CPA trend by channel (combo chart)

Page 3: SEO & Organic
|- Google Search Console: impressions, clicks, CTR, position
|- Top queries table
|- Page-level performance
|- Organic landing page engagement (from GA4)

Page 4: Email & CRM
|- Email campaign metrics (opens, clicks, revenue)
|- List growth trend
|- Flow/automation revenue
|- Subscriber engagement tiers

Page 5: Conversion Funnel
|- Funnel visualization (awareness -> consideration -> conversion)
|- Landing page performance table
|- Device breakdown
|- Geographic heatmap
```

### E-commerce Dashboard
```
Page 1: Revenue Overview
|- Revenue, Orders, AOV, Conversion Rate scorecards
|- Revenue trend (daily/weekly)
|- Revenue by channel
|- Top products table

Page 2: Customer Acquisition
|- New vs returning customer revenue
|- CAC by channel
|- LTV:CAC ratio
|- First-order source attribution
```

### SEO Dashboard
```
Page 1: Organic Performance
|- Total clicks, impressions, CTR, avg position
|- Trend lines (90-day)
|- Top 20 queries (with position change)
|- Top landing pages
|- Device + country breakdown
```

## Key Visualization Guidelines

| Data Type | Best Chart | Avoid |
|-----------|-----------|-------|
| KPI with comparison | Scorecard with delta | Pie chart |
| Trend over time | Line chart or area chart | Bar chart (if >7 periods) |
| Category comparison | Horizontal bar chart | 3D charts |
| Part of whole | Stacked bar or donut | Pie with >6 slices |
| Distribution | Histogram or heatmap | Scatter (if not correlation) |
| Geographic | Geo map or heatmap | Tables for location data |
| Funnel | Custom funnel (shapes) | Bar chart |
| Table data | Table with heatmap bars | Unsorted tables |

## Workflow: Build a Dashboard

When asked to create a Looker Studio dashboard:

1. **Define Purpose** — Who views it? How often? What decisions does it inform?
2. **Identify Data Sources** — Which platforms/connectors needed? Any blending?
3. **Design KPI Framework** — Primary metrics, secondary metrics, diagnostic metrics
4. **Plan Layout** — Page structure, visual hierarchy, interactivity
5. **Create Calculated Fields** — Custom metrics, CASE groupings, regex transformations
6. **Build Visualizations** — Chart types matched to data types, consistent formatting
7. **Add Controls** — Date range, filters, drill-down parameters
8. **Style & Polish** — Theme, colors, fonts, logos, white space
9. **Test & Validate** — Cross-reference numbers with source platforms
10. **Set Up Delivery** — Scheduled emails, sharing permissions, embedding

## Calculated Field Recipes

### Period-over-Period Comparison
```
CASE
  WHEN date_field >= DATE_DIFF(TODAY(), INTERVAL 30 DAY) THEN "Current Period"
  WHEN date_field >= DATE_DIFF(TODAY(), INTERVAL 60 DAY) THEN "Previous Period"
  ELSE "Older"
END
```

### Channel Grouping (Custom)
```
CASE
  WHEN REGEXP_MATCH(source_medium, "google.*cpc|google.*paid") THEN "Google Ads"
  WHEN REGEXP_MATCH(source_medium, "facebook|fb|meta|instagram") THEN "Meta Ads"
  WHEN REGEXP_MATCH(source_medium, "bing.*cpc|microsoft") THEN "Microsoft Ads"
  WHEN REGEXP_MATCH(source_medium, "email|klaviyo|braze") THEN "Email"
  WHEN source_medium = "organic" THEN "Organic Search"
  WHEN REGEXP_MATCH(source_medium, "social") THEN "Organic Social"
  ELSE "Other"
END
```

### ROAS Calculation
```
SUM(revenue) / SUM(cost)
```

## How to Use This Skill

Ask me questions like:
- "Build a marketing performance dashboard in Looker Studio"
- "How do I connect Facebook Ads data to Looker Studio?"
- "Create a calculated field for custom channel grouping"
- "Design an executive summary page with KPI scorecards"
- "How do I blend Google Ads and GA4 data?"
- "Build an SEO dashboard with Search Console data"
- "What's the best way to show period-over-period comparisons?"
- "Help me set up automated email reports for my client"

For detailed Looker Studio function reference, connector setup guides, and advanced techniques, see [REFERENCE.md](REFERENCE.md).

---

## DTC Dashboard Recipes

Dashboard templates designed for DTC e-commerce teams running Klaviyo + Shopify + GA4.

### 1. CRM Performance Dashboard
Track email and SMS marketing effectiveness with Klaviyo data.

```
Page 1: Email & SMS Overview
|- Scorecards: Total Revenue, Flow Revenue %, Campaign Revenue %, List Size
|- Revenue trend: flows vs campaigns over time (area chart)
|- Channel split: email vs SMS revenue (stacked bar)
|- Engagement tiers donut: Active / Warm / At-Risk / Lapsed

Page 2: Flow Performance
|- Flow revenue table (sortable by revenue, click rate)
|- Welcome Series funnel (sent -> opened -> clicked -> converted)
|- Abandoned Cart recovery rate trend
|- Flow-over-flow comparison (combo chart)

Page 3: Campaign Performance
|- Campaign table: send date, subject, open rate, click rate, revenue
|- A/B test results (winner highlighting)
|- Send time heatmap (day of week x hour)
|- Unsubscribe rate trend
```

**Data source**: Google Sheets (fed by `data_pipeline.py --action sync-klaviyo`)

### 2. Lifecycle Marketing Dashboard
Map flow performance across the customer journey.

```
Page 1: Journey Overview
|- Stage funnel: Prospect -> New Customer -> Active -> VIP -> At-Risk -> Lapsed
|- Revenue by stage (horizontal bar)
|- Stage transition rates

Page 2: Stage Deep-Dive
|- Filter control: select lifecycle stage
|- Flow performance for selected stage
|- Customer count trend per stage
|- Revenue per customer by stage (combo chart)
```

### 3. Revenue Attribution Dashboard
Reconcile Klaviyo-attributed revenue with Shopify actuals.

```
Page 1: Attribution Overview
|- Scorecards: Shopify Revenue, Klaviyo Attributed, Attribution %, Gap
|- Daily revenue: Shopify total vs Klaviyo attributed (dual axis)
|- Channel breakdown: Email, SMS, Flows, Campaigns (stacked bar)
|- Attribution gap trend line

Page 2: Channel Detail
|- Channel performance table (Klaviyo revenue per channel)
|- Shopify source breakdown (UTM-based)
|- Overlap analysis notes
```

**Data source**: Blended — Shopify Orders sheet + Klaviyo Revenue sheet

### 4. Campaign ROI Tracker
Campaign-level ROI with A/B test insights.

```
Page 1: Campaign Scorecard
|- Filter: date range, campaign type, channel
|- Campaign table with conditional formatting (green/red on benchmarks)
|- Revenue per recipient trend
|- Best-performing subject lines (top 10)

Page 2: Send Optimization
|- Send time analysis (heatmap: day x hour)
|- Audience size vs performance scatter
|- Frequency analysis: sends per subscriber per month
```

## DTC Calculated Field Library

Copy-paste formulas for common DTC metrics in Looker Studio.

### Customer Lifetime Value (LTV)
```
SUM(total_revenue) / COUNT_DISTINCT(customer_email)
```

### Customer Acquisition Cost (CAC)
```
SUM(ad_spend) / COUNT_DISTINCT(CASE WHEN order_number = 1 THEN customer_email ELSE NULL END)
```

### LTV:CAC Ratio
```
(SUM(total_revenue) / COUNT_DISTINCT(customer_email)) / (SUM(ad_spend) / COUNT_DISTINCT(new_customer_email))
```

### Repeat Purchase Rate
```
COUNT_DISTINCT(CASE WHEN order_count > 1 THEN customer_email ELSE NULL END) / COUNT_DISTINCT(customer_email) * 100
```

### Flow Revenue Percentage
```
SUM(CASE WHEN source_type = "flow" THEN revenue ELSE 0 END) / SUM(revenue) * 100
```

### Engagement Tier
```
CASE
  WHEN days_since_last_open <= 30 THEN "Active (0-30d)"
  WHEN days_since_last_open <= 90 THEN "Warm (31-90d)"
  WHEN days_since_last_open <= 180 THEN "At-Risk (91-180d)"
  ELSE "Lapsed (180d+)"
END
```

### Revenue Per Recipient
```
SUM(revenue) / SUM(recipients)
```

### Discount Impact
```
SUM(discount_amount) / SUM(gross_revenue) * 100
```

## Data Source Setup

### Connecting Klaviyo Data (Free Method)

Paid connectors (Supermetrics, $30-100/mo) work but aren't necessary. The free pattern:

1. **Run the data pipeline script** to push Klaviyo data to Google Sheets:
   ```bash
   python scripts/data_pipeline.py --action sync-klaviyo --sheet-id YOUR_SHEET_ID
   ```
2. **In Looker Studio**, add data source > Google Sheets > select the spreadsheet
3. **Set date field type** to Date in the data source config
4. **Schedule sync** — run the pipeline daily via cron or n8n

### Connecting Shopify Data (Free Method)
1. Push order data to Sheets:
   ```bash
   python scripts/data_pipeline.py --action sync-shopify --sheet-id YOUR_SHEET_ID --days 30
   ```
2. Connect the Sheet in Looker Studio
3. Blend with Klaviyo sheet on Date dimension for attribution view

### Connecting GA4 Data (Native — Free)
1. In Looker Studio, add data source > Google Analytics > select your GA4 property
2. No intermediary needed — native connector is comprehensive and free

### Creating Pre-Formatted Sheets
```bash
# Create a sheet with correct headers for a CRM dashboard
python scripts/data_pipeline.py --action create-sheet --template crm-dashboard

# See all available templates
python scripts/data_pipeline.py --action list-templates
```

## Analysis Examples

For complete dashboard build walkthroughs and use cases, see [EXAMPLES.md](EXAMPLES.md).

## Scripts

The skill includes a data pipeline script for pushing data to Google Sheets:

### Sync Klaviyo Data
```bash
python scripts/data_pipeline.py --action sync-klaviyo --sheet-id SPREADSHEET_ID
```

### Sync Shopify Orders
```bash
python scripts/data_pipeline.py --action sync-shopify --sheet-id SPREADSHEET_ID --days 30
```

### Create Dashboard Sheet
```bash
python scripts/data_pipeline.py --action create-sheet --template crm-dashboard
```

## Troubleshooting

**Data not refreshing**: Google Sheets data in Looker Studio caches for ~15 minutes. Force refresh with the "Refresh data" button in Looker Studio, or set the data source cache to 1 minute in report settings.

**Calculated field errors**: Common causes:
- **Comments in formulas** — Looker Studio does NOT support `--`, `//`, or `/* */` comments. Never include comments in calculated field formulas. Use the field description for documentation instead.
- **Type mismatches** — Ensure date fields are typed as Date (not Text) in the data source config. Use CAST() to convert between types.
- **Regex escaping** — Patterns are inside string literals, so backslashes need double-escaping (e.g., `"\\s"` for whitespace, `"\\|"` for literal pipe).

**Blending shows nulls**: Left outer join means unmatched rows from the right source show null. Ensure join keys match exactly (case-sensitive, same date format).

**Sheets row limit**: Google Sheets has a 10M cell limit. For large datasets, aggregate before writing (daily summaries instead of per-event data), or use BigQuery instead.

**Service account permission errors**: The service account email must be shared on the target Google Sheet with Editor access. Check IAM permissions if Drive API calls fail.

## Security & Privacy

- **Never hardcode** API credentials in scripts — use `.env` files
- Store service account JSON **outside** version control
- Add `.env` and credential files to `.gitignore`
- The data pipeline writes to Google Sheets you control — data stays in your Google Workspace
- Pipeline scripts are read-only against Klaviyo and Shopify APIs
- Use least-privilege API scopes (read-only keys)
