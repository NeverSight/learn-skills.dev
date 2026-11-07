---
name: create-keyword-monitor
description: Create a KEYWORD monitor that fetches a URL and alerts when a given keyword appears (or is missing) in the response body.
tags: [monitoring, keyword, content-check, create, uptimerobot]
---

# Create a KEYWORD monitor

> **Preflight — read first.** If you cannot see any `uptimerobot:*` MCP tools in your tool list, invoke the `uptimerobot:setup` skill before doing anything else. Do not tell the user the MCP is misconfigured — `setup`'s Step 0 detects the common case (server connected, tools loaded after session start) and resolves it without re-keying.

Use when the user cares not just that an endpoint returns a 200, but that a specific string is present (login page has "Sign in") or absent (homepage is not showing "502 Bad Gateway"). For structured JSON assertions, prefer `create-api-monitor` instead.

**Tool:** `create-monitor`
**Required params:** `friendlyName`, `type: "KEYWORD"`, `url` (full URL), `keywordValue`, `keywordType`.

## Minimal call

```json
{
  "friendlyName": "Login page shows Sign in",
  "type": "KEYWORD",
  "url": "https://app.example.com/login",
  "keywordValue": "Sign in",
  "keywordType": "ALERT_NOT_EXISTS"
}
```

`keywordType`:

- `ALERT_NOT_EXISTS` — alert when the keyword **disappears** (expected content missing → down).
- `ALERT_EXISTS` — alert when the keyword **appears** (error string present → down).

## Common optional params

All HTTP-monitor params are supported: `httpMethodType`, `authType`, `httpUsername`, `httpPassword`, `followRedirections`, `checkSSLErrors`, `timeout`, `interval`, `sslExpirationReminder`, `domainExpirationReminder`, `responseTimeThreshold`, `assignedAlertContacts`, `tagNames`, `maintenanceWindowsIds`.

KEYWORD-specific:

- `keywordCaseType` — `0` for case-sensitive (default), `1` for case-insensitive.

## Example: alert when a 500 message appears

```json
{
  "friendlyName": "Homepage not erroring",
  "type": "KEYWORD",
  "url": "https://www.example.com/",
  "keywordValue": "Internal Server Error",
  "keywordType": "ALERT_EXISTS",
  "keywordCaseType": 1,
  "interval": 60,
  "assignedAlertContacts": [
    { "alertContactId": "10", "threshold": 0, "recurrence": 0 }
  ]
}
```

## Common mistakes

- Leaving off `keywordType` — it is required.
- Using an HTTP monitor when the user said "alert me if the page shows X" — use KEYWORD.
- Case-sensitivity confusion. Default is case-sensitive; pass `keywordCaseType: 1` for insensitive.
- `keywordValue` longer than 500 chars is rejected.
- HEAD requests cannot match body content. If `httpMethodType` is `HEAD`, the keyword check will not work as expected.

## After creation

Call `get-monitor-details` to confirm `keywordValue`, `keywordType`, and `keywordCaseType` are stored correctly.

## Related

- `create-http-monitor` — if only status code matters.
- `create-api-monitor` — for JSON/XML response assertions.
