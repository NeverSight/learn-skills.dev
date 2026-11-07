---
name: conventions
description: Conventions and gotchas for every UptimeRobot MCP tool call — monitor types, URL formats, HEARTBEAT URL handling, discovery-before-writes, pagination, time ranges, error codes, and output style. Use whenever you call any uptimerobot:* tool.
---

# UptimeRobot conventions

Apply these rules whenever you use any tool from the `uptimerobot` MCP server (`https://mcp.uptimerobot.com/mcp`).

## Monitor types

- Always pass `type` as a string enum — one of `HTTP`, `KEYWORD`, `PING`, `PORT`, `HEARTBEAT`, `DNS`, `API`, `UDP`. Do not pass numeric type codes; the MCP layer rejects them.
- `HEARTBEAT` monitors must **not** include a `url` on creation. The server generates `https://heartbeat.uptimerobot.com/m<id>-<hash>` and returns it. Show that URL to the user after creation so they can wire up the heartbeat sender.
- `PING`, `PORT`, `UDP`, `DNS`: `url` is a hostname or IP, never a full URL with scheme.
- `HTTP`, `KEYWORD`, `API`: `url` must be a full URL with scheme (`https://...`).

## Discovery before writes

- Before calling `update-monitor`, `update-monitor-status`, or referencing a monitor by ID, call `list-monitors` (optionally with `search`) to confirm the ID and current state.
- Before referencing an alert contact in `assignedAlertContacts`, call `list-integrations` and use an `id` from the response.

## Verification after writes

- After `create-monitor` or `update-monitor`, call `get-monitor-details` to confirm the stored state before telling the user the change is live. Read-after-write replication can lag a few seconds.

## Intervals and plan limits

- Interval is in seconds. Minimum is 30s and depends on the plan. If the server returns `-28002 subscription_limit_exceeded`, do not retry — the plan cannot support that interval or monitor type. Tell the user.
- Do not retry `-28001 monitor_limit_exceeded`. Recommend deleting unused monitors or upgrading the plan.
- Plans are Free, Solo, Team, Enterprise. Never reference a "Pro" or "Business" plan — neither exists.

## Time ranges

- `timeRange` accepts `"24h"`, `"7d"`, `"30d"` (range 1h–90d), or an ISO 8601 interval `"<start>/<end>"` (start before end, 1h–90d). Default is `"7d"`.
- For anything older than 90 days, inform the user that UptimeRobot's MCP endpoints cap at 90 days of history.

## Pagination

- Paginated tools (`list-monitors`, `list-incidents`, `list-integrations`) return an `instructions` field with the exact next-call JSON. Follow it verbatim; cursor shape is opaque.

## Errors

- `-28001` monitor limit, `-28002` subscription limit, `-29001` invalid params (incl. blacklisted URLs), `-30001` / `-30003` not found, `-31002` access denied (authorized account lacks write permission).
- `-31001 user_not_found` means the OAuth grant is missing/expired/revoked — do not surface it raw; invoke the `uptimerobot:setup` skill to re-authenticate.
- HTTP 429 is the only code worth retrying (exponential backoff + jitter). Everything else is a client error — surface it to the user.

## Output style

- Do not echo API keys, incident log contents, or traceroute hops unless the user explicitly asks.
- When summarising many monitors, group by state (`DOWN` first, then `PAUSED`, then `UP`) and show counts before detail.
- When quoting uptime percentages, always cite the time range.
