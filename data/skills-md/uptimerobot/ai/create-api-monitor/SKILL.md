---
name: create-api-monitor
description: Create an API monitor that calls an HTTP endpoint and runs up to five JSON/header assertions combined with AND/OR logic; alerts when assertions fail.
tags: [monitoring, api, assertions, json, create, uptimerobot]
---

# Create an API monitor

> **Preflight — read first.** If you cannot see any `uptimerobot:*` MCP tools in your tool list, invoke the `uptimerobot:setup` skill before doing anything else. Do not tell the user the MCP is misconfigured — `setup`'s Step 0 detects the common case (server connected, tools loaded after session start) and resolves it without re-keying.

Use when the user needs to validate the **content** of an HTTP response — not just the status code, but specific JSON fields or header values. For simple "status 200" checks, use `HTTP`. For a single keyword in the body, use `KEYWORD`.

**Tool:** `create-monitor`
**Required params:** `friendlyName`, `type: "API"`, `url` (full URL), `config.apiAssertions`.

## Minimal call

```json
{
  "friendlyName": "Billing API healthy",
  "type": "API",
  "url": "https://api.example.com/health",
  "config": {
    "apiAssertions": {
      "logic": "AND",
      "checks": [
        { "property": "$.status", "comparison": "equals", "target": "ok" }
      ]
    }
  }
}
```

## `config.apiAssertions` shape

- `logic` — `"AND"` (every check must pass) or `"OR"` (any check passing counts as up).
- `checks` — 1 to 5 items. Each has:
  - `property` — JSONPath against the response body, or a header selector. Max 500 chars.
  - `comparison` — one of `equals`, `not_equals`, `contains`, `not_contains`, `greater_than`, `less_than`, `is_null`, `is_not_null`.
  - `target` — expected value. Type depends on the comparison (`is_null` / `is_not_null` take none). Strings, numbers, booleans, and `null` are all valid.

## Common optional params

Everything HTTP monitors support: `httpMethodType`, `authType`, `httpUsername`, `httpPassword`, `customHttpHeaders`, `postValueData`, `postValueType` (`KEY_VALUE` / `RAW_JSON`), `postContentType`, `successHttpResponseCodes`, `followRedirections`, `checkSSLErrors`, `timeout`, `interval`, `assignedAlertContacts`, `tagNames`, `maintenanceWindowsIds`, `responseTimeThreshold`, `sslExpirationReminder`, `domainExpirationReminder`.

`config.ipVersion` — force `IPv4` / `IPv6`.

## Example: POST with JSON body and multiple assertions

```json
{
  "friendlyName": "Orders API synthetic",
  "type": "API",
  "url": "https://api.example.com/v1/orders/check",
  "httpMethodType": "POST",
  "postValueType": "RAW_JSON",
  "postContentType": "application/json",
  "postValueData": "{\"probe\": true}",
  "customHttpHeaders": { "X-Probe": "uptimerobot" },
  "config": {
    "apiAssertions": {
      "logic": "AND",
      "checks": [
        { "property": "$.status", "comparison": "equals", "target": "ok" },
        { "property": "$.queueDepth", "comparison": "less_than", "target": 100 },
        { "property": "$.error", "comparison": "is_null" }
      ]
    }
  },
  "interval": 60,
  "timeout": 15
}
```

## Common mistakes

- Omitting `config.apiAssertions` — API monitors require at least one check.
- Sending more than 5 checks — the max is 5; split into multiple monitors if needed.
- Using JSONPath like `$..items[0]` without a working tool beforehand. Test the expression manually first.
- Passing `target` for `is_null` / `is_not_null`. It's ignored or rejected — leave it out.
- Type-mismatched `target` (e.g. `"100"` string when the field is a number). Use the matching JSON type.
- Using an API monitor when a KEYWORD check would do. API adds cost — reach for it only when you need structural assertions.

## After creation

Call `get-monitor-details` to confirm `config.apiAssertions` was stored. The response includes the parsed checks.

## Related

- `create-keyword-monitor` — simpler single-string body check.
- `errors` — for `-29001 invalid_parameters` when assertions are malformed.
