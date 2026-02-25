---
name: pipeline-analytics
description: Generate interactive analytics dashboards from CRM data. Use when asked to "show pipeline stats", "create a report", "analyze leads", "show conversion rates", "build a dashboard", "visualize outreach data", "funnel analysis", or any data visualization request from DuckDB workspace data.
metadata: { "openclaw": { "emoji": "📊" } }
---

# Pipeline Analytics — NL → SQL → Interactive Charts

Transform natural language questions into DuckDB queries and render results as interactive Recharts dashboards inline in chat.

## Workflow

```
User asks question in plain English
→ Translate to DuckDB SQL against workspace pivot views (v_*)
→ Execute query
→ Format results as report-json
→ Render as interactive Recharts components
```

## DuckDB Query Patterns

### Discovery — What objects exist?
```sql
-- List all objects and their entry counts
SELECT o.name, o.display_name, COUNT(e.id) as entries
FROM objects o
LEFT JOIN entries e ON e.object_id = o.id
GROUP BY o.name, o.display_name
ORDER BY entries DESC;

-- List fields for an object
SELECT f.name, f.field_type, f.display_name
FROM fields f
JOIN objects o ON f.object_id = o.id
WHERE o.name = 'leads'
ORDER BY f.position;

-- Available pivot views
SELECT table_name FROM information_schema.tables
WHERE table_name LIKE 'v_%';
```

### Common Analytics Queries

#### Pipeline Funnel
```sql
SELECT "Status", COUNT(*) as count
FROM v_leads
GROUP BY "Status"
ORDER BY CASE "Status"
  WHEN 'New' THEN 1
  WHEN 'Contacted' THEN 2
  WHEN 'Qualified' THEN 3
  WHEN 'Demo Scheduled' THEN 4
  WHEN 'Proposal' THEN 5
  WHEN 'Closed Won' THEN 6
  WHEN 'Closed Lost' THEN 7
  ELSE 99
END;
```

#### Outreach Activity Over Time
```sql
SELECT DATE_TRUNC('week', "Last Outreach"::DATE) as week,
       "Outreach Channel",
       COUNT(*) as messages_sent
FROM v_leads
WHERE "Last Outreach" IS NOT NULL
GROUP BY week, "Outreach Channel"
ORDER BY week;
```

#### Conversion Rates by Source
```sql
SELECT "Source",
       COUNT(*) as total,
       COUNT(*) FILTER (WHERE "Status" = 'Qualified') as qualified,
       COUNT(*) FILTER (WHERE "Status" IN ('Closed Won', 'Converted')) as converted,
       ROUND(100.0 * COUNT(*) FILTER (WHERE "Status" = 'Qualified') / COUNT(*), 1) as qual_rate,
       ROUND(100.0 * COUNT(*) FILTER (WHERE "Status" IN ('Closed Won', 'Converted')) / COUNT(*), 1) as conv_rate
FROM v_leads
GROUP BY "Source"
ORDER BY total DESC;
```

#### Reply Rate Analysis
```sql
SELECT "Outreach Channel",
       COUNT(*) as sent,
       COUNT(*) FILTER (WHERE "Reply Received" = true) as replied,
       ROUND(100.0 * COUNT(*) FILTER (WHERE "Reply Received" = true) / COUNT(*), 1) as reply_rate
FROM v_leads
WHERE "Outreach Status" IS NOT NULL
GROUP BY "Outreach Channel";
```

#### Time-to-Convert
```sql
SELECT "Source",
       AVG(DATEDIFF('day', created_at, "Converted At"::DATE)) as avg_days_to_convert,
       MEDIAN(DATEDIFF('day', created_at, "Converted At"::DATE)) as median_days
FROM v_leads
WHERE "Status" = 'Converted' AND "Converted At" IS NOT NULL
GROUP BY "Source";
```

## Report-JSON Format

Generate Recharts-compatible report cards:

```json
{
  "type": "report",
  "title": "Pipeline Analytics — February 2026",
  "generated_at": "2026-02-17T14:30:00Z",
  "panels": [
    {
      "title": "Pipeline Funnel",
      "type": "funnel",
      "data": [
        {"name": "New Leads", "value": 200},
        {"name": "Contacted", "value": 145},
        {"name": "Qualified", "value": 67},
        {"name": "Demo Scheduled", "value": 31},
        {"name": "Closed Won", "value": 13}
      ]
    },
    {
      "title": "Outreach Activity",
      "type": "area",
      "xKey": "week",
      "series": [
        {"key": "linkedin", "name": "LinkedIn", "color": "#0A66C2"},
        {"key": "email", "name": "Email", "color": "#EA4335"}
      ],
      "data": [
        {"week": "Feb 3", "linkedin": 25, "email": 40},
        {"week": "Feb 10", "linkedin": 30, "email": 35}
      ]
    },
    {
      "title": "Lead Source Breakdown",
      "type": "donut",
      "data": [
        {"name": "LinkedIn Scrape", "value": 95, "color": "#0A66C2"},
        {"name": "YC Directory", "value": 45, "color": "#FF6600"},
        {"name": "Referral", "value": 30, "color": "#10B981"},
        {"name": "Inbound", "value": 20, "color": "#8B5CF6"}
      ]
    },
    {
      "title": "Reply Rates by Channel",
      "type": "bar",
      "xKey": "channel",
      "series": [{"key": "rate", "name": "Reply Rate %", "color": "#3B82F6"}],
      "data": [
        {"channel": "LinkedIn", "rate": 32},
        {"channel": "Email", "rate": 18},
        {"channel": "Multi-Channel", "rate": 41}
      ]
    }
  ]
}
```

## Chart Types Available

| Type | Use Case | Recharts Component |
|------|----------|-------------------|
| `bar` | Comparisons, categories | BarChart |
| `line` | Trends over time | LineChart |
| `area` | Volume over time | AreaChart |
| `pie` | Distribution (single level) | PieChart |
| `donut` | Distribution (with center metric) | PieChart (innerRadius) |
| `funnel` | Stage progression | FunnelChart |
| `scatter` | Correlation (2 variables) | ScatterChart |
| `radar` | Multi-dimension comparison | RadarChart |

## Pre-Built Report Templates

### 1. Pipeline Overview
- Funnel: Lead → Contacted → Qualified → Demo → Closed
- Donut: Lead source breakdown
- Number cards: Total leads, conversion rate, avg deal size

### 2. Outreach Performance
- Area: Messages sent over time (by channel)
- Bar: Reply rates by channel
- Line: Conversion trend week-over-week
- Number cards: Total sent, reply rate, meetings booked

### 3. Rep Performance (if multi-user)
- Bar: Leads contacted per rep
- Bar: Reply rate per rep
- Bar: Conversions per rep
- Scatter: Activity volume vs. conversion rate

### 4. Cohort Analysis
- Heatmap-style: Conversion rate by signup week × time elapsed
- Line: Retention/engagement curves by cohort

## Natural Language Mapping

| User Says | SQL Pattern | Chart Type |
|-----------|-------------|------------|
| "show me pipeline" | GROUP BY Status | funnel |
| "outreach stats" | COUNT by channel + status | bar + area |
| "how are we converting" | conversion rates | funnel + line |
| "compare sources" | GROUP BY Source | bar |
| "weekly trend" | DATE_TRUNC + GROUP BY | line / area |
| "who replied" | FILTER Reply Received | table |
| "best performing" | ORDER BY conversion DESC | bar |
| "lead breakdown" | GROUP BY any dimension | pie / donut |

## Saving Reports

Reports can be saved as `.report.json` files in the workspace:
```
~/.openclaw/workspace/reports/
  pipeline-overview.report.json
  weekly-outreach.report.json
  monthly-review.report.json
```

These render as live dashboards in the Ironclaw web UI when opened.

## Cron Integration

Auto-generate weekly/monthly reports:
```json
{
  "name": "Weekly Pipeline Report",
  "schedule": { "kind": "cron", "expr": "0 9 * * MON", "tz": "America/Denver" },
  "payload": {
    "kind": "agentTurn",
    "message": "Generate weekly pipeline analytics report. Query DuckDB for this week's data. Create report-json with: funnel, outreach activity (area), reply rates (bar), source breakdown (donut). Save to workspace/reports/ and announce summary."
  }
}
```
