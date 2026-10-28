---
name: bulk-pause
description: Pause (or resume) many UptimeRobot monitors at once — by tag, search term, or state — around a deployment or maintenance window.
tags: [bulk, pause, resume, deployment, maintenance, uptimerobot]
---

# Bulk pause / resume

> **Preflight — read first.** If you cannot see any `uptimerobot:*` MCP tools in your tool list, invoke the `uptimerobot:setup` skill before doing anything else. Do not tell the user the MCP is misconfigured — `setup`'s Step 0 detects the common case (server connected, tools loaded after session start) and resolves it without re-keying.

There is no single "pause all" tool. The workflow is: enumerate the target monitors with `list-monitors`, then call `update-monitor-status` for each.

Use this when the user says "pause everything", "silence alerts during deploy", "mute the api monitors", or "bring them all back online".

> **Prefer [`maintenance-windows`](../maintenance-windows/SKILL.md) for scheduled downtime.** Maintenance windows suppress *alerts* without changing monitor state and don't count against your plan's active-monitor cap on resume. Only bulk-pause when the user explicitly wants the monitors stopped, or when a maintenance window isn't suitable (ad-hoc, very short, or already in the middle of a deploy).

## Step 1 — List the target monitors

Filter as tightly as possible to avoid pausing unrelated monitors.

### By tag

```json
{ "search": "", "filter": [], "limit": 50 }
```

`list-monitors` doesn't support tag-based server-side filtering. Pull the page, then filter client-side on `tagNames` before touching anything.

### By name or URL

```json
{ "search": "api.example.com", "limit": 50 }
```

### By state (only currently-running monitors)

```json
{ "filter": ["UP", "DOWN", "NOT_STARTED"], "limit": 50 }
```

Excluding `PAUSED` avoids re-pausing already-paused monitors.

Follow the `instructions` field for pagination until `hasMore: false`. **Do not start pausing until the full list is collected** — partial pauses mid-paginate are easy to miss on resume.

## Step 2 — Confirm with the user

Before any write, echo the list back:

```
Pausing 14 monitors tagged `deploy-api`:
- Prod API (HTTP, UP)
- Prod API /healthz (KEYWORD, UP)
- ...
```

Wait for confirmation if the count is non-trivial (>5).

## Step 3 — Pause each monitor

```json
{ "monitorId": 800123456, "status": "PAUSED" }
```

Loop over the collected IDs. If you hit HTTP 429, back off with jitter (see `errors` skill).

## Step 4 — Track what you paused

Before pausing, store the list of `monitorId`s somewhere retrievable (chat context, a note file, a gist) — you'll need it to resume. Don't rely on re-filtering later: the user may have added or renamed monitors in the interim, and a tag-based filter can quietly pick up unrelated monitors on resume.

## Step 5 — Resume

Same loop, flip the status:

```json
{ "monitorId": 800123456, "status": "STARTED" }
```

Resuming a monitor can return `-28001 monitor_limit_exceeded` if the account is now over its active-monitor cap (e.g. the user added new monitors while these were paused). Surface which ones failed and suggest deleting or upgrading — **do not retry**.

## Full example flow

User: "Pause everything tagged `deploy-web` for the next 20 minutes."

1. `list-monitors` with `{ "limit": 50 }`, paginate, filter client-side where `tagNames` includes `"deploy-web"` → 8 monitors.
2. Echo the 8 names and `type`s. User confirms.
3. For each: `update-monitor-status` with `{"monitorId": ..., "status": "PAUSED"}`.
4. Note the 8 IDs. Tell the user: "Paused 8 monitors. Run `resume deploy-web` when you're done."
5. On resume: loop with `STARTED`. Report which recovered and which errored.

## Common mistakes

- Re-filtering on resume instead of using the stored ID list — will silently miss monitors whose tag or name changed.
- Skipping the confirmation step for large batches. Pausing production monitoring without echoing the list is high-risk.
- Pausing monitors already in `PAUSED` state — harmless but noisy. Filter them out up front.
- Retrying `-28001 monitor_limit_exceeded` on resume. It's a cap, not a rate limit.
- Using `update-monitor` with `status: ...` instead of `update-monitor-status`. Status lives on the dedicated tool.

## Related

- `manage-monitors` — for the underlying `list-monitors` and `update-monitor-status` tools.
- [`maintenance-windows`](../maintenance-windows/SKILL.md) — the scheduled/recurring alternative.
- `errors` — for `-28001`, `-31002`, and 429 handling.
- `incident-response` — when pausing is a response to ongoing incidents rather than a deploy.
