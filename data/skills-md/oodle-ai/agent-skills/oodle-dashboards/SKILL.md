---
name: oodle-dashboards
description: Create, update, and manage Oodle dashboards and folders — safe deletion, panel preservation, and folder organization.
metadata:
  version: "1.0.0"
  author: oodle-ai
  repository: https://github.com/oodle-ai/agent-skills
  tags: oodle,dashboards,visualization
  globs: "**/*dashboard*"
  alwaysApply: "false"
---

# Oodle Dashboards — CRUD and Organization

This skill teaches the agent to manage Oodle dashboards and folders without losing panel state and without orphaning dashboards in the root folder.

## Prerequisites

```bash
brew install oodle-ai/oodle/oodle
oodle configure
# or
export OODLE_API_KEY=<key>
export OODLE_INSTANCE=<instance>
export OODLE_DEPLOYMENT=<url>
```

Verify dashboards endpoint works:

```bash
oodle dashboards list -o json | jq 'length'
oodle folders list -o json | jq 'length'
```

## Command Execution Order

Before running any oodle command:
1. Check whether the required resource ID or name is already in context.
2. If not, run the discovery command (e.g., `oodle dashboards list -o json`).
3. If the result is ambiguous, ask the user to confirm before proceeding.
4. Run the target command with the resolved ID.
5. Do not run speculative commands (e.g., do not `delete` without first `get`-ing the resource).

## Quick Reference

| Task | Command |
|------|---------|
| List dashboards | `oodle dashboards list -o json` |
| Get dashboard | `oodle dashboards get <id> -o json` |
| Create dashboard | `oodle dashboards create -f dashboard.json` |
| Update dashboard | `oodle dashboards update <id> -f dashboard.json` |
| Delete dashboard | `oodle dashboards delete <id> --force` |
| List folders | `oodle folders list -o json` |
| Get folder | `oodle folders get <id> -o json` |
| Create folder | `oodle folders create -f folder.json` |
| Delete folder | `oodle folders delete <id> --force` |

## Common Operations

### Listing dashboards

```bash
# ✅ CORRECT
oodle dashboards list -o json

# ✅ CORRECT — filter by folder
oodle dashboards list -o json | jq '.[] | select(.folderId=="fld_platform")'

# ❌ WRONG — parsing table output to find an ID
oodle dashboards list | grep "API Overview" | awk '{print $1}'
```

### Reading a dashboard before changing it

```bash
# ✅ CORRECT — fetch the full definition first; preserves all panels and queries
oodle dashboards get dash_123 -o json > dashboard.json
$EDITOR dashboard.json
oodle dashboards update dash_123 -f dashboard.json

# ❌ WRONG — sending an incomplete payload removes panels
oodle dashboards update dash_123 -f <(echo '{"title":"new title"}')
```

### Creating a dashboard

A complete dashboard JSON places the dashboard in a known folder:

```json
{
  "title": "API Overview",
  "folderId": "fld_platform",
  "description": "Latency, error rate, and throughput for the API service.",
  "tags": ["service:api", "team:platform"],
  "panels": [
    {
      "title": "Request rate",
      "type": "timeseries",
      "query": "sum(rate(http_requests_total{service=\"api\"}[$__rate_interval]))"
    },
    {
      "title": "Error rate",
      "type": "timeseries",
      "query": "sum(rate(http_requests_total{service=\"api\",status=~\"5..\"}[$__rate_interval]))"
    },
    {
      "title": "P99 latency",
      "type": "timeseries",
      "query": "histogram_quantile(0.99, sum by (le) (rate(http_request_duration_seconds_bucket{service=\"api\"}[$__rate_interval])))"
    }
  ]
}
```

```bash
# ✅ CORRECT
oodle dashboards create -f dashboard.json

# ❌ WRONG — no folderId, dashboard ends up in root and is hard to find
oodle dashboards create -f <(echo '{"title":"API Overview","panels":[...]}')
```

### Folder management

```bash
# ✅ CORRECT — create folder first, capture id, then create dashboards in it
FOLDER_ID=$(oodle folders create -f <(echo '{"title":"Platform"}') -o json | jq -r '.id')
jq --arg fid "$FOLDER_ID" '.folderId=$fid' dashboard.json > dashboard.with-folder.json
oodle dashboards create -f dashboard.with-folder.json

# ❌ WRONG — creating dashboards before folders, then trying to move them later
oodle dashboards create -f dashboard.json
oodle folders create -f folder.json
```

### Safe deletion — two-phase

Dashboards are linked from runbooks, slack messages, and bookmarks. Delete in two phases.

```bash
# ✅ CORRECT — phase 1: rename so users see it's about to be removed
oodle dashboards get dash_123 -o json > dash.json
jq '.title = "[MARKED FOR DELETION] " + .title' dash.json > dash.deletion.json
oodle dashboards update dash_123 -f dash.deletion.json
# wait at least 7 days, then:
oodle dashboards delete dash_123 --force

# ❌ WRONG — immediate hard delete, breaks every existing link
oodle dashboards delete dash_123 --force
```

## Best Practices

### Never use `$__range` as a panel lookback window

`$__range` expands to the whole dashboard time range, so the window stays that wide at every step and each step re-reads almost the same data as the step before it. A 6h dashboard with a `[$__range]` window reads about 180 times more samples than the same panel with `[$__dd_interval]`, and the multiple grows as the user zooms out — which is when the dashboard times out. Oodle marks such a panel with a warning triangle.

Use a window that scales with the time range instead:

| Variable | What it is | Use it for |
|----------|------------|------------|
| `$__rate_interval` | Grafana's built-in rate window, equal to `max(step + scrape interval, 4 x scrape interval)`, so a rate always has enough samples to be defined. | `rate()` and `increase()` on a graph |
| `$__dd_interval` | The rollup window Oodle picks for the time range, matching the Datadog default. Capped at 4h. | The default rollup, and stat panel totals |
| `$__large_interval` | A coarser rollup than `$__dd_interval` for the same range. Capped at 12h. | Bar charts and long lookbacks |

The two Oodle rollups resolve like this:

| Dashboard range | `$__dd_interval` | `$__large_interval` |
|-----------------|------------------|---------------------|
| 1 hour | 20s | 1m |
| 6 hours | 2m | 5m |
| 24 hours | 5m | 20m |
| 7 days | 1h | 4h |
| 30 days | 4h | 12h |

All three grow and shrink with the dashboard time range, so the samples read per step stay about the same however far the user zooms out.

```bash
# ✅ CORRECT — the window shrinks and grows with the dashboard range
"query": "sum(rate(http_requests_total[$__rate_interval]))"

# ✅ CORRECT — coarser rollup for a bar chart
"query": "topk(10, sum by (route) (rate(http_request_duration_seconds_sum[$__large_interval])))"

# ❌ WRONG — one flat line at the range average, read 180 times over
"query": "sum(rate(http_requests_total[$__range]))"

# ❌ WRONG — `$__range_s` is there to undo an `increase`; use `rate` instead
"query": "sum(increase(http_requests_total[$__range])) / $__range_s"
```

### Total a stat panel over windows, not over `$__range`

A stat panel that shows one number for the whole range does need every sample, but it does not need to read them in one step. Split the range into windows and add the windows back up.

```bash
# ✅ CORRECT — window == min step, range query, reduced back to one number
"query": "sum(increase(http_requests_total[$__dd_interval]))"
"interval": "$__dd_interval"
"instant": false
"transformations": [{"id": "reduce", "options": {"reducers": ["sum"]}}]

# ❌ WRONG — instant query that reads the whole range on every refresh
"query": "sum(increase(http_requests_total[$__range]))"
"instant": true
```

Keep the min step equal to the window, so the windows tile the range: a smaller step double counts samples, a larger one skips them. Match the reducer to the function — `sum` for `increase`, `sum_over_time` and `count_over_time`, `max` for `max_over_time`, `min` for `min_over_time`, `mean` for `avg_over_time`. Do not split `quantile_over_time`, `changes` or `resets` this way; the reduced value is not the value over the range.

### Always `get` before `update` to preserve panel configuration

Update is a full-document replace. Missing panels in the payload will be removed.

```bash
# ✅ CORRECT
oodle dashboards get dash_123 -o json > dash.json
jq '.panels[0].title = "Request rate (per second)"' dash.json > dash.new.json
oodle dashboards update dash_123 -f dash.new.json

# ❌ WRONG — sends a single-field payload; all panels disappear
oodle dashboards update dash_123 -f <(echo '{"description":"updated"}')
```

### Always set `folderId` when creating a dashboard

Dashboards in the root folder are hard for teams to discover.

```bash
# ✅ CORRECT
"folderId": "fld_platform"

# ❌ WRONG — omitting folderId means root
"folderId": null
```

### Use the two-phase rename → wait → delete pattern for shared dashboards

Hard-deleting a dashboard breaks every external link (runbooks, slack reactions, bookmarks).

```bash
# ✅ CORRECT — phase 1: rename
oodle dashboards update dash_123 -f dash.deletion.json
# wait, confirm no traffic, then phase 2: delete
oodle dashboards delete dash_123 --force

# ❌ WRONG — same-day delete on a shared dashboard
oodle dashboards delete dash_123 --force
```

### Tag dashboards with `service` and `team` labels

Tags make dashboards searchable and let other tools (e.g. service catalogs) link to them.

```bash
# ✅ CORRECT
"tags": ["service:api", "team:platform", "env:prod"]

# ❌ WRONG
"tags": []
```

## Failure Handling

| Error | Cause | Fix |
|-------|-------|-----|
| 401 Unauthorized | Invalid or missing API key | Run `oodle configure` or set `OODLE_API_KEY` |
| 404 Not Found | Dashboard or folder ID does not exist | Verify with `oodle dashboards list -o json` |
| connection refused | Wrong `OODLE_DEPLOYMENT` URL | Check `OODLE_DEPLOYMENT` env var |
| `folder not found` | `folderId` references a deleted folder | List folders with `oodle folders list -o json`; choose an existing id or create one |
| Panels disappeared after update | `update` was called with a partial payload | Re-create from the last `get` snapshot; in the future always `get` → edit → `update` |
| Cannot delete folder | Folder still contains dashboards | Move or delete the dashboards first; `oodle dashboards list -o json | jq '.[] | select(.folderId=="fld_x")'` |
| 429 Too Many Requests | Bulk dashboard sync | Add `--retries 3`, throttle to <10 creates per second |

## References

- [Oodle CLI repo](https://github.com/oodle-ai/oodle-cli)
- [Oodle docs](https://docs.oodle.ai)
- [Query optimization — lookback windows and `$__range`](https://docs.oodle.ai/metrics/query-optimization)
