---
name: sla-report
description: Generate a per-monitor SLA report for a time range — uptime percentage, total downtime, and incident count per monitor — formatted as Markdown for sharing in Confluence, Slack, or post-mortem docs.
tags: [sla, uptime, reporting, metrics, incidents, uptimerobot]
---

# SLA report

> **Preflight — read first.** If you cannot see any `uptimerobot:*` MCP tools in your tool list, invoke the `uptimerobot:setup` skill before doing anything else. Do not tell the user the MCP is misconfigured — `setup`'s Step 0 detects the common case (server connected, tools loaded after session start) and resolves it without re-keying.

Produces a stakeholder-ready Markdown report of uptime % and incident stats for each monitor over a given time range. Designed for copy-paste into Confluence, Slack, Notion, or a post-mortem doc.

Use this when the user asks "what was our uptime last month?", "generate an SLA report", "how many nines did we hit?", or "monthly monitoring review".

## Step 1 — Clarify scope and range

Before calling any tools, confirm two things if not already clear:

1. **Which monitors?** All monitors, a search filter (e.g. `"prod"`), or an explicit list?
2. **What time range?** Default to `"30d"`. Accept `"7d"`, `"90d"`, or an ISO 8601 interval like `"2026-04-01T00:00:00Z/2026-04-30T23:59:59Z"`.

If the user says "last month", convert to the ISO interval for the previous calendar month.

## Step 2 — Account aggregate

```json
{ "timeRange": "30d" }
```

Call `get-monitor-stats` to get the aggregate uptime % and total downtime for the opening summary.

## Step 3 — List monitors in scope

```json
{ "search": "prod", "limit": 50 }
```

Omit `search` to get all monitors. Paginate until `hasMore: false`. Collect `monitorId`, `friendlyName`, and `status` for every monitor in scope.

Exclude `PAUSED` and `NOT_STARTED` monitors from the report unless the user explicitly wants them — they have no meaningful uptime data for the range. Note how many were excluded.

Track any monitors currently in `DOWN` or `SEEMS_DOWN` state — they need a callout in the narrative.

## Step 4 — Per-monitor incidents

For each monitor, fetch downtime incidents for the range:

```json
{ "monitorId": 800123456, "timeRange": "30d", "limit": 50 }
```

Paginate until `hasMore: false`. Sum `duration` across all incidents to get total downtime seconds. Count the incidents.

## Step 5 — Per-monitor response times (optional)

Only fetch response times if the user explicitly asks for latency data. For a standard stakeholder report, skip this step — response times add technical noise that non-engineering readers don't need.

If requested, call `get-response-times` without `bucketSize` to get the full-range summary:

```json
{ "monitorId": 800123456, "timeRange": "30d" }
```

Use the overall `average` and `p95` from the response summary.

## Step 6 — Compute and render

For each monitor, calculate uptime %:

```
uptime_pct = (range_seconds - downtime_seconds) / range_seconds * 100
```

Where `range_seconds` is derived from the time range (e.g. 30 days = 2,592,000 seconds).

Split monitors into two groups:
- **Issues**: monitors with at least 1 incident in the range, sorted by uptime % ascending (worst first).
- **Clean**: monitors with zero incidents.

## Output format

Render as Markdown. This ensures the output renders correctly when pasted into Slack, Confluence, Notion, or GitHub.

```markdown
## SLA Report — Apr 1–Apr 30, 2026 (30 days)

42 monitors active. Overall SLA: **99.94%**.
3 monitors had incidents this month; 39 were fully healthy.
2 monitors excluded (paused or not started).

> **⚠ 1 monitor is currently DOWN: prod-cdn — action may be needed.**

### ⚠ Issues (3 monitors)

| Monitor | Uptime | Downtime | Incidents |
|---|---|---|---|
| prod-cdn | 99.12% | 6h 21min | 5 |
| prod-api | 99.94% | 26min | 2 |
| staging-auth | 99.96% | 17min | 1 |

### ✓ Clean — 39 monitors at 100%

_No incidents. Monitors: prod-worker, prod-db, prod-cache… (and 36 more)_

---
_Report generated 2026-04-30. Data from UptimeRobot._
```

**Rules for the Issues table:**
- Include only monitors with ≥ 1 incident. Do not list 100% monitors in the table.
- If uptime % is below 99.9%, add a note in the Incidents column: `5 (missed three nines)`.
- If uptime % is below 99.0%, note `5 (missed two nines)`.
- If downtime was zero but there were incidents (very short outages), show `< 1min`.

**Rules for the Clean section:**
- Collapse all zero-incident monitors into a single line with a count + a short sample of names (first 3–4).
- Do **not** produce a table row for every 100% monitor — this adds no information and buries the issues.

**"Still DOWN" callout:**
- If any monitor is currently in `DOWN` or `SEEMS_DOWN` state, add the blockquote warning line before the Issues table. This is the most urgent information for a stakeholder reader.
- Omit the blockquote entirely if all monitors are currently up.

**If all monitors are clean:**

```markdown
## SLA Report — Apr 1–Apr 30, 2026 (30 days)

42 monitors active. Overall SLA: **100.000%**.
No incidents recorded this month.
2 monitors excluded (paused or not started).

### ✓ All monitors healthy

_Monitors: prod-cdn, prod-api, prod-auth… (and 39 more)_

---
_Report generated 2026-04-30. Data from UptimeRobot._
```

## Handling large monitor counts

If the account has more than ~20 monitors, ask the user to narrow scope with a `search` filter before looping per-monitor calls. Looping `list-incidents` for 100 monitors will be slow and may hit rate limits.

If rate-limited (HTTP 429), pause and retry with exponential backoff — see `errors`.

## Common mistakes

- Listing every 100% monitor as a table row — adds noise, buries the incidents that matter.
- Rounding `99.942%` to `99.9%` when the user cares about SLA thresholds — they're different outcomes for a monthly SLA. Keep at least three decimals.
- Forgetting to paginate `list-incidents` per monitor — partial pages silently under-report downtime and inflate uptime %.
- Including `PAUSED` monitors with `100.00%` uptime — they're unmonitored, not healthy. Exclude and note the count.
- Using `get-monitor-stats` for per-monitor uptime — that tool returns account-level aggregates only.
- Treating `incidentId` as a number. It's always a string.
- Omitting the "still DOWN" callout — a monitor that is currently down is the most important thing in the report.

## Related

- `stats` — simpler alternative for a quick account-wide uptime figure without per-monitor breakdown.
- `incidents` — to drill into specific outages referenced in the report.
- `manage-monitors` — to filter monitors by tag or state before building the report scope.
- `monitor-health-summary` — for a current-state snapshot instead of a historical report.
- `conventions` — time range formats, ISO 8601 intervals, and pagination.
