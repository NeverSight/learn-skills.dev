---
name: scout-api
description: Query Scout APM performance data via REST API. Use when investigating app performance, slow endpoints, error groups, traces, or insights like N+1 queries and memory bloat.
allowed-tools: Bash(curl:*)
---

# Scout APM API

Query application performance monitoring data from Scout APM using the REST API.

## When to Use

- Investigating slow endpoints or response time regressions
- Listing applications and their metrics (apdex, throughput, error rate, p95)
- Fetching traces for a specific endpoint
- Reviewing error groups and individual error stacktraces
- Checking insights: N+1 queries, memory bloat, slow queries

Do not use for configuring Scout agents or instrumenting code — this is the read-only reporting API.

## Setup

### API Key

1. Log into [Scout APM](https://scoutapm.com)
2. Go to [organization settings](https://scoutapm.com/settings)
3. Create a named API token
4. Export it in your shell profile:

```bash
export SCOUT_API_KEY="your-token-here"
```

### Base URL

```
https://scoutapm.com/api/v0
```

### Authentication

Every request must include the key via **one** of:
- Header: `X-SCOUT-API: $SCOUT_API_KEY`
- Query param: `?key=$SCOUT_API_KEY`

All examples below use the header approach.

## Quick Reference

```bash
# List apps
curl -sS -H "X-SCOUT-API: $SCOUT_API_KEY" "https://scoutapm.com/api/v0/apps"

# App details
curl -sS -H "X-SCOUT-API: $SCOUT_API_KEY" "https://scoutapm.com/api/v0/apps/{id}"

# Available metrics for an app
curl -sS -H "X-SCOUT-API: $SCOUT_API_KEY" "https://scoutapm.com/api/v0/apps/{id}/metrics"

# Metric time-series (requires from/to)
curl -sS -H "X-SCOUT-API: $SCOUT_API_KEY" \
  "https://scoutapm.com/api/v0/apps/{id}/metrics/{metric_type}?from=2026-02-18T00:00:00Z&to=2026-02-19T00:00:00Z"

# List endpoints (requires from/to)
curl -sS -H "X-SCOUT-API: $SCOUT_API_KEY" \
  "https://scoutapm.com/api/v0/apps/{id}/endpoints?from=2026-02-18T00:00:00Z&to=2026-02-19T00:00:00Z"

# Endpoint metrics (endpoint is base64-url-encoded)
curl -sS -H "X-SCOUT-API: $SCOUT_API_KEY" \
  "https://scoutapm.com/api/v0/apps/{id}/endpoints/{endpoint_b64}/metrics/{metric_type}?from=...&to=..."

# List traces for endpoint (max 100, within 7 days)
curl -sS -H "X-SCOUT-API: $SCOUT_API_KEY" \
  "https://scoutapm.com/api/v0/apps/{id}/endpoints/{endpoint_b64}/traces?from=...&to=..."

# Trace detail (includes spans)
curl -sS -H "X-SCOUT-API: $SCOUT_API_KEY" \
  "https://scoutapm.com/api/v0/apps/{id}/traces/{trace_id}"

# Error groups (max 100, within 30 days)
curl -sS -H "X-SCOUT-API: $SCOUT_API_KEY" \
  "https://scoutapm.com/api/v0/apps/{id}/error_groups?from=...&to=..."

# Error group detail (includes latest_error with stacktrace)
curl -sS -H "X-SCOUT-API: $SCOUT_API_KEY" \
  "https://scoutapm.com/api/v0/apps/{id}/error_groups/{error_id}"

# Individual errors in a group (max 100)
curl -sS -H "X-SCOUT-API: $SCOUT_API_KEY" \
  "https://scoutapm.com/api/v0/apps/{id}/error_groups/{error_id}/errors"

# All insights (cached 5 min)
curl -sS -H "X-SCOUT-API: $SCOUT_API_KEY" \
  "https://scoutapm.com/api/v0/apps/{id}/insights"

# Insights by type: n_plus_one | memory_bloat | slow_query
curl -sS -H "X-SCOUT-API: $SCOUT_API_KEY" \
  "https://scoutapm.com/api/v0/apps/{id}/insights/{type}?limit=20"

# Insights history (cursor-paginated)
curl -sS -H "X-SCOUT-API: $SCOUT_API_KEY" \
  "https://scoutapm.com/api/v0/apps/{id}/insights/history?from=...&to=...&limit=10"

# Insights history by type
curl -sS -H "X-SCOUT-API: $SCOUT_API_KEY" \
  "https://scoutapm.com/api/v0/apps/{id}/insights/history/{type}?from=...&to=...&limit=10"
```

## Endpoints Reference

### Applications

| Method | Path | Description |
|--------|------|-------------|
| GET | `/apps` | List all apps |
| GET | `/apps/{id}` | Get app details |

### Metrics

| Method | Path | Params | Description |
|--------|------|--------|-------------|
| GET | `/apps/{id}/metrics` | — | List available metric types |
| GET | `/apps/{id}/metrics/{metric_type}` | `from`, `to` | Time-series data for a metric |

**Metric types:** `apdex`, `response_time`, `response_time_95th`, `errors`, `throughput`, `queue_time`

### Endpoints

| Method | Path | Params | Description |
|--------|------|--------|-------------|
| GET | `/apps/{id}/endpoints` | `from`, `to` | List endpoints with stats |
| GET | `/apps/{id}/endpoints/{endpoint}/metrics/{metric_type}` | `from`, `to` | Metric data for one endpoint |

**Endpoint encoding:** The `{endpoint}` path segment must be **Base64 URL-encoded**.

```bash
# Encode "UsersController#index" → base64
echo -n "UsersController#index" | base64
# VXNlcnNDb250cm9sbGVyI2luZGV4
```

### Traces

| Method | Path | Params | Description |
|--------|------|--------|-------------|
| GET | `/apps/{id}/endpoints/{endpoint}/traces` | `from`, `to` | List traces (max 100, 7-day window) |
| GET | `/apps/{id}/traces/{trace_id}` | — | Trace detail with spans |

Trace detail includes: `id`, `time`, `total_call_time`, `mem_delta`, `metric_name`, `uri`, `context`, `git_sha`, `allocations_count`, `limited`, `spans[]`. V2 traces also include `transaction_id` and `hostname`.

### Errors

| Method | Path | Params | Description |
|--------|------|--------|-------------|
| GET | `/apps/{id}/error_groups` | `from`, `to`, `endpoint` (optional, base64) | List error groups (max 100, 30-day window) |
| GET | `/apps/{id}/error_groups/{error_id}` | — | Error group detail + latest error |
| GET | `/apps/{id}/error_groups/{error_id}/errors` | — | Individual errors (max 100) |

Each error includes: `message`, `created_at`, `request_params`, `request_uri`, `location`, `request_session`, `trace` (stacktrace lines), `context`.

### Insights

| Method | Path | Params | Description |
|--------|------|--------|-------------|
| GET | `/apps/{id}/insights` | `limit` | All insight types (cached 5 min) |
| GET | `/apps/{id}/insights/{type}` | `limit` | Single insight type |
| GET | `/apps/{id}/insights/history` | `from`, `to`, `limit`, `pagination_cursor`, `pagination_direction`, `pagination_page` | Historical insights |
| GET | `/apps/{id}/insights/history/{type}` | (same as above) | Historical insights by type |

**Insight types:** `n_plus_one`, `memory_bloat`, `slow_query`

**Pagination:** Cursor-based. Response includes `pagination.has_more`, `pagination.pagination_cursor`, and `pagination.next_pagination_page`. Pass `pagination_direction=forward` (default) or `backward`.

## Time Steps

Duration determines the resolution of returned time-series data:

| Duration | Step |
|----------|------|
| ≤ 60 min | 1 minute |
| ≤ 3 hrs | 2 minutes |
| ≤ 12 hrs | 5 minutes |
| ≤ 1 day | 10 minutes |
| ≤ 3 days | 30 minutes |
| ≤ 7 days | 1 hour |
| ≤ 14 days | 2 hours |

## Response Format

All responses follow a standard envelope:

```json
{
  "header": {
    "status": { "code": 200, "message": "OK" },
    "apiVersion": "0.1"
  },
  "results": { ... }
}
```

Error responses use the same envelope with codes `403` (bad key), `404` (not found), or `422` (bad params).

## Workflow: Investigate a Slow Endpoint

```bash
# 1. Find the app
curl -sS -H "X-SCOUT-API: $SCOUT_API_KEY" "https://scoutapm.com/api/v0/apps" | jq '.results.apps[] | {id, name}'

# 2. List endpoints sorted by response time (last 24h)
FROM=$(date -u -v-1d +%Y-%m-%dT%H:%M:%SZ)  # macOS
TO=$(date -u +%Y-%m-%dT%H:%M:%SZ)
curl -sS -H "X-SCOUT-API: $SCOUT_API_KEY" \
  "https://scoutapm.com/api/v0/apps/{id}/endpoints?from=$FROM&to=$TO" \
  | jq '.results | sort_by(-.response_time) | .[:10] | .[] | {name, response_time, throughput, error_rate}'

# 3. Get p95 response time series for the slowest endpoint
ENDPOINT_B64=$(echo -n "Controller#action" | base64)
curl -sS -H "X-SCOUT-API: $SCOUT_API_KEY" \
  "https://scoutapm.com/api/v0/apps/{id}/endpoints/$ENDPOINT_B64/metrics/response_time_95th?from=$FROM&to=$TO"

# 4. Pull traces to find the slow requests
curl -sS -H "X-SCOUT-API: $SCOUT_API_KEY" \
  "https://scoutapm.com/api/v0/apps/{id}/endpoints/$ENDPOINT_B64/traces?from=$FROM&to=$TO" \
  | jq '.results.traces | sort_by(-.total_call_time) | .[:5]'

# 5. Inspect the slowest trace's spans
TRACE_ID=12345
curl -sS -H "X-SCOUT-API: $SCOUT_API_KEY" \
  "https://scoutapm.com/api/v0/apps/{id}/traces/$TRACE_ID" \
  | jq '.results.trace.spans'
```

## Workflow: Review Errors

```bash
# 1. List error groups (last 7 days)
FROM=$(date -u -v-7d +%Y-%m-%dT%H:%M:%SZ)
TO=$(date -u +%Y-%m-%dT%H:%M:%SZ)
curl -sS -H "X-SCOUT-API: $SCOUT_API_KEY" \
  "https://scoutapm.com/api/v0/apps/{id}/error_groups?from=$FROM&to=$TO" \
  | jq '.results.error_groups | sort_by(-.errors_count) | .[:10] | .[] | {id, name, message, errors_count, last_error_at}'

# 2. Get detail + latest stacktrace
curl -sS -H "X-SCOUT-API: $SCOUT_API_KEY" \
  "https://scoutapm.com/api/v0/apps/{id}/error_groups/{error_id}" \
  | jq '.results.error_group | {name, message, status, errors_count, latest_error}'
```

## Workflow: Check Insights

```bash
# Quick overview — are there N+1s, memory bloat, or slow queries?
curl -sS -H "X-SCOUT-API: $SCOUT_API_KEY" \
  "https://scoutapm.com/api/v0/apps/{id}/insights" \
  | jq '.results.insights | to_entries[] | {type: .key, count: .value.count, new: .value.new_count}'

# Drill into N+1 queries
curl -sS -H "X-SCOUT-API: $SCOUT_API_KEY" \
  "https://scoutapm.com/api/v0/apps/{id}/insights/n_plus_one?limit=10"
```

## Common Pitfalls

- **Missing `from`/`to` params** — most endpoints require ISO 8601 timestamps; omitting them returns 422
- **Endpoint encoding** — the `{endpoint}` path segment must be base64-encoded; raw strings like `Users#index` will 404
- **Trace time window** — traces endpoint is limited to a 7-day window
- **Error group time window** — error_groups endpoint is limited to 30 days
- **Insights cache** — current insights are cached for 5 minutes; don't poll more frequently
- **Max results** — traces and error lists cap at 100 items; no built-in pagination for those endpoints
- **Time step granularity** — you don't control it; it's determined by the duration of your `from`/`to` window (see Time Steps table)
