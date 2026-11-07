---
name: manage-monitors
description: List monitors, fetch details, and pause or resume monitors in UptimeRobot.
tags: [monitoring, list, pause, resume, uptimerobot]
---

# Manage monitors

> **Preflight — read first.** If you cannot see any `uptimerobot:*` MCP tools in your tool list, invoke the `uptimerobot:setup` skill before doing anything else. Do not tell the user the MCP is misconfigured — `setup`'s Step 0 detects the common case (server connected, tools loaded after session start) and resolves it without re-keying.

Covers monitor discovery and status control:

- `list-monitors` — paginated discovery with search + state filters.
- `get-monitor-details` — full config for one monitor.
- `update-monitor-status` — pause or resume.

For **creating** monitors see the `create-*-monitor` skills. For **editing** an existing monitor's configuration (rename, URL, interval, alert contacts, tags, type-specific settings) see [`update-monitor`](../update-monitor/SKILL.md).

## List monitors

```json
{
  "search": "api",
  "filter": ["DOWN"],
  "limit": 50
}
```

Parameters:

- `search` — full-text match against `friendlyName` and `url`.
- `filter` — array, any of `UP`, `DOWN`, `PAUSED`, `NOT_STARTED`, `EXPIRING_DOMAIN`, `EXPIRING_SSL_CERTIFICATE`, `WITH_API_KEY`, `WITHOUT_API_KEY`.
- `limit` — page size (clamped server-side).
- `cursor` — from the previous page's `nextCursor`.

The response includes an `instructions` field with the exact next-page call JSON. Follow it verbatim.

## Get monitor details

```json
{ "monitorId": 800123456 }
```

Returns the full config (type, URL, interval, thresholds, alert contacts, tags, type-specific fields) plus current status and state duration. Use this:

- To confirm a `create-monitor` / `update-monitor` took effect.
- To inspect one monitor's config before editing.
- To retrieve the generated URL for a HEARTBEAT monitor.

## Update monitor configuration

Covered in its own skill: [`update-monitor`](../update-monitor/SKILL.md) — rename, URL, interval, alert contacts, tags, HTTP/keyword/API/heartbeat type-specific settings, and read‑modify‑write patterns for array fields.

## Update monitor status

```json
{ "monitorId": 800123456, "status": "PAUSED" }
```

`status` is one of `PAUSED` (stop monitoring) or `STARTED` (resume). Resuming a paused monitor can return `-28001 monitor_limit_exceeded` if the account is over its active-monitor cap.

## Common mistakes

- Skipping `get-monitor-details` after a status change. Replication lag can mean the next `list-monitors` call still shows the old state.
- Calling `update-monitor-status` when the authorized account lacks write access — returns `-31002 access_denied`.
- Forgetting that resume counts against the active-monitor cap — `-28001 monitor_limit_exceeded`.

## Related

- [`update-monitor`](../update-monitor/SKILL.md) — edit configuration of an existing monitor.
- [`bulk-pause`](../bulk-pause/SKILL.md) — pause/resume many monitors at once.
- [`incidents`](../incidents/SKILL.md) — downtime history for a monitor.
- [`stats`](../stats/SKILL.md) — aggregated uptime / response-time metrics.
- [`errors`](../errors/SKILL.md) — recovering from `-28001`, `-28002`, `-29001`, `-31002`.
