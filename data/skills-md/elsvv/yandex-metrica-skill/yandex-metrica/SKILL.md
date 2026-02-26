---
name: yandex-metrica
description: |
  Работа с Yandex Metrica API: аналитика, отчёты, цели, логи.
  Use when the user needs web analytics data from Yandex Metrica —
  traffic stats, conversion reports, goal management, raw log exports,
  counter management, segments, filters, or grants.
  Triggers: метрика, metrica, аналитика, счётчик, визиты, конверсии,
  отчёт по трафику, источники трафика, Logs API, экспорт логов.
---

# yandex-metrica

Yandex Metrica API — web analytics: counters, reports, goals, logs export.

## Config

Requires `YANDEX_METRICA_TOKEN` in `config/.env`.
See `config/README.md` for token setup (OAuth, permissions: `metrika:read`, `metrika:write`).

## Quick Start

**IMPORTANT:** Always run scripts with `bash` prefix and **absolute paths** from the skill directory. Scripts use bash-specific features and will not work if sourced from zsh. Do NOT `source scripts/common.sh` directly — use the wrapper scripts below.

```bash
# 1. Setup token
bash scripts/get_token.sh --client-id YOUR_CLIENT_ID

# 2. Check connection
bash scripts/check_connection.sh

# 3. List counters
bash scripts/counters.sh --action list

# 4. Get traffic stats
bash scripts/stats.sh --counter 12345678 --preset traffic

# 5. Export raw logs
bash scripts/logs.sh --action create --counter 12345678 --date1 2025-01-01 --date2 2025-01-31
```

## API Overview

Base URL: `https://api-metrika.yandex.net`

Auth header: `Authorization: OAuth TOKEN`

| API | Purpose | Base Path |
|-----|---------|-----------|
| Management | Counters, goals, filters, grants, segments | `/management/v1/` |
| Reporting | Aggregated stats, dimensions, metrics | `/stat/v1/` |
| Logs | Raw visit/hit data export | `/management/v1/counter/{id}/logrequests` |

## Scripts

### check_connection.sh
Verify API token and list available counters.
```bash
bash scripts/check_connection.sh
```

### counters.sh
Manage counters: list, get details, get full info with goals/filters.
```bash
bash scripts/counters.sh --action list
bash scripts/counters.sh --action list --search "mysite.com"
bash scripts/counters.sh --action info --counter 12345678
```

### stats.sh
Pull reporting data with presets or custom metrics/dimensions.
```bash
# Traffic overview
bash scripts/stats.sh --counter 12345678 --preset traffic

# Traffic sources breakdown
bash scripts/stats.sh --counter 12345678 --preset sources

# Top pages
bash scripts/stats.sh --counter 12345678 --preset content

# Custom report with filters
bash scripts/stats.sh --counter 12345678 \
  --metrics "ym:s:visits,ym:s:users,ym:s:bounceRate" \
  --dimensions "ym:s:lastTrafficSource" \
  --filters "ym:s:trafficSource=='organic'" \
  --date1 2025-01-01 --date2 2025-01-31

# Time-series report
bash scripts/stats.sh --counter 12345678 --type bytime \
  --metrics "ym:s:visits" --date1 2025-01-01 --date2 2025-01-31

# Export to CSV
bash scripts/stats.sh --counter 12345678 --preset sources --csv report.csv
```

| Param | Default | Description |
|-------|---------|-------------|
| `--counter` | env var | Counter ID (required) |
| `--metrics` | visits,pageviews,users | Comma-separated metrics |
| `--dimensions` | — | Comma-separated dimensions |
| `--date1` | 30 days ago | Start date YYYY-MM-DD |
| `--date2` | today | End date YYYY-MM-DD |
| `--filters` | — | Filter expression |
| `--sort` | — | Sort field (prefix `-` for desc) |
| `--limit` | 100 | Max rows |
| `--preset` | — | traffic, sources, geo, content, technology |
| `--type` | data | data, bytime, drilldown, comparison |
| `--csv` | — | Export to CSV file |

### goals.sh
List and get goals for a counter.
```bash
bash scripts/goals.sh --action list --counter 12345678
bash scripts/goals.sh --action get --counter 12345678 --goal-id 999
```

### logs.sh
Raw data export via Logs API.
```bash
# Check if export is possible
bash scripts/logs.sh --action evaluate --counter 12345678 \
  --date1 2025-01-01 --date2 2025-01-31

# Create log request
bash scripts/logs.sh --action create --counter 12345678 \
  --source visits --date1 2025-01-01 --date2 2025-01-31

# Check status
bash scripts/logs.sh --action status --counter 12345678 --request-id 777

# Download when ready
bash scripts/logs.sh --action download --counter 12345678 \
  --request-id 777 --output ./exports

# Clean up server-side
bash scripts/logs.sh --action clean --counter 12345678 --request-id 777

# List all log requests
bash scripts/logs.sh --action list --counter 12345678
```

## Key Metrics Quick Reference

| Metric | Description |
|--------|-------------|
| `ym:s:visits` | Sessions |
| `ym:s:users` | Unique visitors |
| `ym:s:pageviews` | Total pageviews |
| `ym:s:bounceRate` | Bounce rate % |
| `ym:s:avgVisitDurationSeconds` | Avg session duration |
| `ym:s:newUsers` | New visitors |
| `ym:s:goal<ID>reaches` | Goal completions |
| `ym:s:goal<ID>conversionRate` | Goal conversion rate |
| `ym:s:ecommerceRevenue` | E-commerce revenue |

## Key Dimensions Quick Reference

| Dimension | Description |
|-----------|-------------|
| `ym:s:trafficSource` | Traffic source type |
| `ym:s:lastTrafficSource` | Last traffic source |
| `ym:s:<attr>UTMSource` | UTM source |
| `ym:s:<attr>UTMMedium` | UTM medium |
| `ym:s:startURL` | Landing page |
| `ym:s:regionCountry` | Country |
| `ym:s:regionCity` | City |
| `ym:s:browser` | Browser |
| `ym:s:deviceCategory` | Device type |
| `ym:s:operatingSystem` | OS |

`<attr>` = attribution model: `last`, `first`, `lastsign`, etc.

## Filter Syntax

```
ym:s:trafficSource=='organic'           # equals
ym:s:trafficSource!='organic'           # not equals
ym:s:trafficSource=.('organic','direct') # in list
ym:s:pageViews>5                        # greater than
ym:s:startURL=@'product'               # contains
ym:s:startURL=~'.*product.*'           # regex
ym:s:trafficSource=='organic' AND ym:s:isRobot=='No'  # combine
```

## Rate Limits

| Limit | Value |
|-------|-------|
| General API | 30 req/sec per IP |
| Logs API | 10 req/sec per IP |
| Parallel requests | 3 per user |
| Daily limit | 5,000 req/day |
| Reports API | 200 req/5 min |

## Detailed Reference

For comprehensive API documentation including all endpoints, field lists, curl examples, and advanced features, see:
[references/api-reference.md](references/api-reference.md)

Covers: Management API (counters, goals, filters, operations, grants, labels, segments, user params), Reporting API (data, bytime, drilldown, comparison, presets, full metrics/dimensions), Logs API (visits/hits fields).
