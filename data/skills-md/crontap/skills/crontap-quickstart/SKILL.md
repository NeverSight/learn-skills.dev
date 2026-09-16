---
name: crontap-quickstart
description: >
  Choose the right Crontap resource, inspect account limits, and verify an IANA
  timezone before making changes. Use when a user is new to Crontap or needs to
  decide between schedules, uptime monitors, and heartbeats.
license: MIT
metadata:
  version: "1.0.0"
  tools: get_account_usage,list_timezones
---

# Crontap quickstart

Crontap provides three related resources:

- A schedule sends an HTTP request on a cron or plain-English cadence.
- An uptime monitor probes a URL and records availability.
- A heartbeat expects an existing job to ping after it runs.

MCP lets the current agent manage these resources. Crontap owns HTTP scheduling
and observability, not the lifecycle of the MCP client.

## Prerequisites

- Connect the remote MCP server at `https://mcp.crontap.com/mcp` and complete
  OAuth in the target Crontap account.
- Know the intended endpoint, local timezone, and desired failure signal.
- Treat endpoint authorization values and heartbeat ping URLs as secrets.

## Workflow

1. Call `get_account_usage` before creating resources when capacity is
   uncertain.
2. Compare `usage.combined` with `caps.combined` and inspect feature flags.
3. Choose a schedule for outbound execution, a monitor for endpoint
   availability, or a heartbeat for missed check-ins.
4. Call `list_timezones` when the exact IANA timezone is uncertain.
5. Hand off to the focused skill for creation and verification.

## MCP examples

Inspect the active tier, usage, caps, features, and plan options:

```json
{
  "tool": "get_account_usage",
  "arguments": {}
}
```

Find accepted timezone names:

```json
{
  "tool": "list_timezones",
  "arguments": {
    "query": "Copenhagen"
  }
}
```

Use the exact returned timezone, such as `Europe/Copenhagen`. Do not substitute
a fixed UTC offset for a local-time business schedule.

## REST fallback

The public API is a fallback only for accounts with Ultra API access. MCP is
not Ultra-only.

```bash
curl --fail-with-body https://api.crontap.com/v1/account \
  -H "ClientId: $CRONTAP_CLIENT_ID" \
  -H "ApiKey: $CRONTAP_API_KEY"
```

Keep both values in environment variables or a secret manager. Never put them
in a repository, agent transcript, URL, or example output.

## Safety and plan limits

- Starter, Pro, and Ultra use one combined cap for schedules, monitors, and
  heartbeats. Some resource-specific caps and cadence floors also apply.
- Treat the returned account object as authoritative. Do not hard-code prices
  or assume a feature from the tier name.
- If a tool returns a structured plan-limit error, present its ordered
  four-option ladder and identify the smallest viable option. Do not invent a
  fifth option or hide the all-plans URL.
- Confirm the target account before any write operation.

## Troubleshooting

- If OAuth fails, reconnect the MCP server in the client and retry once.
- If a timezone search returns no match, try a city or region substring.
- If REST returns `API_REQUIRES_ULTRA`, continue through MCP or let the user
  choose an Ultra option.
- If `MAX_ITEMS_REACHED` appears, do not retry the same create call unchanged.

## References

- [Crontap MCP](https://crontap.com/mcp)
- [Crontap pricing](https://crontap.com/pricing)
- [Live REST API reference](https://api.crontap.com/docs/)
- [Crontap machine-readable product reference](https://crontap.com/llms.txt)
