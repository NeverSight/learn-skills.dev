---
name: incident-response
description: End-to-end incident workflow — find what's down, diagnose it, pause flapping monitors, and verify recovery.
tags: [incidents, downtime, triage, response, runbook, uptimerobot]
---

# Incident response

> **Preflight — read first.** If you cannot see any `uptimerobot:*` MCP tools in your tool list, invoke the `uptimerobot:setup` skill before doing anything else. Do not tell the user the MCP is misconfigured — `setup`'s Step 0 detects the common case (server connected, tools loaded after session start) and resolves it without re-keying.

The full loop a user runs when something's on fire:

1. Find what's down (`list-monitors` with `DOWN` filter).
2. Pull incident details for the worst offenders (`get-incident-details`).
3. Optionally silence flapping monitors while the underlying issue is being fixed (`update-monitor-status` → `PAUSED`).
4. Log findings as you go with incident comments (requires the `incident-comments` plan feature).
5. After the fix, verify recovery with `get-monitor-stats` and/or `get-response-times`.

Use this when the user says "what's down?", "is production still broken?", "triage the alerts", or "show me the outage".

## Step 1 — Find what's down

```json
{ "filter": ["DOWN"], "limit": 50 }
```

Paginate until `hasMore: false`. Group the results by tag or friendly-name prefix before reporting — the user typically cares "what system is down", not "which individual checks are failing".

Also surface `NOT_STARTED` monitors on request — they're not actively monitored but show up in downtime reports.

### Active-only view

To exclude paused and unstarted:

```json
{ "filter": ["DOWN"], "limit": 50 }
```

(`DOWN` by itself excludes `PAUSED` / `NOT_STARTED` automatically.)

## Step 2 — Pull recent incidents

For each down monitor that the user wants to dig into:

```json
{ "monitorId": 800123456, "timeRange": "24h", "limit": 5 }
```

Returns a list of incidents (active and resolved). Note `incidentId` is a **string**.

Lead with the active (unresolved) incident, then show recently-resolved ones as flap history.

## Step 3 — Diagnose one incident

```json
{ "incidentId": "inc_abcdef1234567890" }
```

Returns:

- Per-checker probe results (location, IP, HTTP status, error kind, response body snippet).
- Traceroute hops where available.
- Start time, duration, and root-cause category if assigned.

Useful output pattern:

- "All 5 checker locations saw connection refused on port 443 starting at 14:02 UTC."
- "2 of 5 checkers (NA, EU) see 503; 3 others see 200 — looks regional."
- "First hop fails on traceroute — likely a firewall rule."

Don't paste the full log body unless asked — summarise the error kind and HTTP status.

## Step 4 — Log findings as an incident comment thread (optional)

Requires the `incident-comments` plan feature. Rather than only reporting a final summary at the end, add a comment each time you learn something material — it builds a timeline other responders (and future you, writing the postmortem) can read directly on the incident:

```json
{ "incidentId": "inc_abcdef1234567890", "content": "5/5 checkers see connection refused on :443 since 14:02 UTC. Not regional — looks like the LB is down." }
```

`incidentId` here is a BigInt passed as a numeric string (same value as `get-incident-details`). If you posted something and later learn it was wrong (e.g. misidentified root cause), fix it with `update-incident-comment` (needs the numeric `commentId` from the create response or `list-incident-comments`) rather than leaving a stale comment alongside a correction — the thread should read as a clean timeline, not a debug log.

When writing the final summary (below), pull the full thread with `list-incident-comments` so nothing gets lost between what was said live and what makes the postmortem.

## Step 5 — Silence flapping monitors (optional)

If a monitor is flapping while the underlying issue is being fixed and the noise is distracting, pause just that monitor (not everything — see `bulk-pause` for that):

```json
{ "monitorId": 800123456, "status": "PAUSED" }
```

Confirm with the user first — pausing a monitor also stops alerts, which is exactly what you want during known downtime but dangerous if the user forgets to resume.

Store the paused IDs so you can resume them later. [`maintenance-windows`](../maintenance-windows/SKILL.md) is a better choice when the downtime is planned ahead of time rather than reactive.

## Step 6 — Verify recovery

Once the user says the fix is deployed, confirm the monitor is actually green.

### Current state of one monitor

```json
{ "monitorId": 800123456 }
```

Call `get-monitor-details`. Expect `status: UP` and a recent `lastCheckedAt`.

### Aggregate over the window

```json
{ "timeRange": "1h" }
```

Call `get-monitor-stats` to see if overall uptime % is recovering. Pair with `get-response-times` on the specific monitor:

```json
{ "monitorId": 800123456, "timeRange": "1h", "bucketSize": "1m" }
```

Look for response times returning to baseline, not just "up vs down".

### Resume anything you paused

For each paused monitor ID you stored in step 5:

```json
{ "monitorId": 800123456, "status": "STARTED" }
```

Watch for `-28001 monitor_limit_exceeded` on resume (see `errors`).

## Reporting back to the user

Typical structured summary:

```
Incident on `prod-api` (monitor 800123456)
- Started: 2026-04-21T14:02:00Z
- Duration: 18 min (resolved)
- Impact: 5/5 checker locations saw 503 Service Unavailable
- Root cause: deploy-related, resolved after rollback at 14:20 UTC
- Currently: UP. Response times at 220ms (baseline 190ms).
Related monitors also down during window: `prod-api-healthz`, `prod-api-db`.
```

## Common mistakes

- Showing raw checker logs without summarising. The user wants cause-and-impact, not JSON.
- Forgetting to filter out `NOT_STARTED` monitors when reporting "what's down" — they're not an outage.
- Pausing monitors and not tracking what you paused. Resuming requires the list.
- Claiming recovery from `status: UP` alone. Check `get-response-times` — a monitor can be UP with 10x response time and still degraded.
- Treating a resolved-then-retriggered incident as one event. Sometimes `list-incidents` returns two rows for a flap.
- Requesting `timeRange` > 90 days. Max is 90d.
- Leaving an incorrect incident comment uncorrected instead of using `update-incident-comment` — the thread is the record other people read.
- Trying to comment on an incident when the account's plan lacks the `incident-comments` feature — check for `-28002` and fall back to reporting in chat only.

## Related

- `manage-monitors` — for `list-monitors`, `get-monitor-details`, `update-monitor-status`.
- `incidents` — detailed reference for `list-incidents` and `get-incident-details`.
- `stats` — for `get-monitor-stats` and `get-response-times`.
- `bulk-pause` — when many monitors need silencing at once.
- [`maintenance-windows`](../maintenance-windows/SKILL.md) — the scheduled alternative to pausing during known downtime.
- [`status-pages`](../status-pages/SKILL.md) — post a public-facing announcement alongside internal incident comments.
- `errors` — `-28001` on resume, `-28002` for plan-gated features, `-30001` on stale IDs, 429 handling during heavy loops.
