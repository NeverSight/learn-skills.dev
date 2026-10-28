---
name: create-http-monitor
description: Create an HTTP monitor in UptimeRobot to check that a URL returns a successful response on an interval.
tags: [monitoring, http, create, uptimerobot]
---

# Create an HTTP monitor

> **Preflight — read first.** If you cannot see any `uptimerobot:*` MCP tools in your tool list, invoke the `uptimerobot:setup` skill before doing anything else. Do not tell the user the MCP is misconfigured — `setup`'s Step 0 detects the common case (server connected, tools loaded after session start) and resolves it without re-keying.

Use when the user wants to monitor a website or HTTP(S) endpoint for reachability and/or specific response codes. HTTP is the default choice unless the user needs content matching (`KEYWORD`), response assertions (`API`), or low-level connectivity (`PING` / `PORT`).

**Tool:** `create-monitor`
**Required params:** `friendlyName`, `type: "HTTP"`, `url` (must be a full URL with scheme).

## Minimal call

```json
{
  "friendlyName": "Production API",
  "type": "HTTP",
  "url": "https://api.example.com/health"
}
```

## Common optional params

- `interval` — seconds between checks (30–86400). Defaults to the plan's default. Free-plan minimum is higher than paid plans.
- `timeout` — request timeout in seconds (1–60).
- `httpMethodType` — one of `HEAD`, `GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `OPTIONS`.
- `authType` — `NONE` (default), `HTTP_BASIC`, `DIGEST`, `BEARER`. Pair with `httpUsername` / `httpPassword`.
- `customHttpHeaders` — object, e.g. `{"X-Source": "uptimerobot"}`.
- `successHttpResponseCodes` — array of strings that count as success, e.g. `["200", "201", "2xx"]`.
- `followRedirections` — boolean, defaults to `true`.
- `checkSSLErrors` — boolean, validates cert errors when `true`.
- `sslExpirationReminder` / `domainExpirationReminder` — boolean flags for expiry alerts.
- `responseTimeThreshold` — milliseconds; 0 disables slow-response alerts.
- `assignedAlertContacts` — see below.
- `tagNames` — array of tag strings (max 20, ≤50 chars each).
- `maintenanceWindowsIds` — array of maintenance window IDs.

## Alert contacts

```json
"assignedAlertContacts": [
  { "alertContactId": "10", "threshold": 0, "recurrence": 0 },
  { "alertContactId": "20", "threshold": 5, "recurrence": 30 }
]
```

`alertContactId` values come from `list-integrations`. `threshold` = minutes of downtime before this contact fires. `recurrence` = re-notify every N minutes while still down.

## Full example with auth + headers

```json
{
  "friendlyName": "Internal API health",
  "type": "HTTP",
  "url": "https://internal.example.com/api/v1/health",
  "interval": 60,
  "timeout": 10,
  "httpMethodType": "GET",
  "authType": "BEARER",
  "httpPassword": "sk_live_...",
  "customHttpHeaders": { "X-Env": "prod" },
  "successHttpResponseCodes": ["200", "204"],
  "sslExpirationReminder": true,
  "assignedAlertContacts": [
    { "alertContactId": "10", "threshold": 0, "recurrence": 0 }
  ],
  "tagNames": ["prod", "critical"]
}
```

## Common mistakes

- Passing a bare hostname (`"api.example.com"`) — HTTP monitors require a full URL with scheme. Use `PING` for hostname-only checks.
- Sending numeric `type: 1` — MCP only accepts the string `"HTTP"`.
- Listing forbidden fields like `port` or `gracePeriod` on an HTTP monitor. The server rejects with `-29001 invalid_parameters`.
- Setting `interval` below the plan minimum. Returns `-28002 subscription_limit_exceeded`.

## After creation

Call `get-monitor-details` with the returned monitor id to confirm stored config. Read-after-write can lag a few seconds.

## Related

- `create-keyword-monitor` — if you need to assert specific text is (or isn't) in the body.
- `create-api-monitor` — if you need JSONPath assertions on the response body.
- `errors` — for recovering from `-28002`, `-29001`, `429`.
