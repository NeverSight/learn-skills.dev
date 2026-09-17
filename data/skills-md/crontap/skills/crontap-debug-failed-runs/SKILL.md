---
name: crontap-debug-failed-runs
description: >
  Diagnose failed Crontap schedule runs from saved configuration and retained
  execution history, separating scheduler, network, timeout, and endpoint
  failures. Use when a scheduled HTTP job is late, failing, or unexpectedly
  unauthorized.
license: MIT
metadata:
  version: "1.0.0"
  group: main
  order: 6
  title: Debug failed schedule runs
  summary: Trace failed runs through status, timing, and authentication evidence, then confirm the fix on the next attempt.
  bestFor: HTTP errors, timeouts, auth, and run history
  guide: https://crontap.com/guides/cron-troubleshooting
  guideTitle: Cron troubleshooting
  tools: get_schedule_history,get_schedule
---

# Debug failed schedule runs

Diagnose from evidence before changing cadence, retries, or credentials.

## Prerequisites

Before using the required tools, check whether they are available. If any are
missing, stop and offer the user exactly two choices:

1. Connect Crontap MCP at `https://mcp.crontap.com/mcp`. MCP access works on
   every Crontap tier.
2. Configure `$CRONTAP_CLIENT_ID` and `$CRONTAP_API_KEY` for the raw API. Raw
   API access requires Ultra.

Do not silently choose a path or continue until the user selects one.

- Obtain the schedule ID from the user or the schedule list.
- Define the incident window and the expected endpoint behavior.
- Do not ask the user to paste secret header values or full tokens.

## Workflow

1. Read the current schedule configuration with `get_schedule`.
2. Read the latest history page with `get_schedule_history`.
3. Compare several runs to identify a persistent error or a one-off event.
4. Classify the failure before proposing a bounded fix.
5. Verify the next run or a separately authorized test after a change.

## MCP examples

Read the active configuration:

```json
{
  "tool": "get_schedule",
  "arguments": {
    "scheduleId": "<schedule-id>"
  }
}
```

Read recent outcomes:

```json
{
  "tool": "get_schedule_history",
  "arguments": {
    "scheduleId": "<schedule-id>",
    "limit": 50
  }
}
```

If the response includes a cursor, pass it unchanged to inspect older runs:

```json
{
  "tool": "get_schedule_history",
  "arguments": {
    "scheduleId": "<schedule-id>",
    "limit": 50,
    "cursor": "<opaque-cursor>"
  }
}
```

## Failure decision tree

- No history and a future next run: verify cron, timezone, pause state, and
  account cadence floor.
- HTTP 401 or 403: rotate or repair the target credential in its secure store.
- HTTP 404: confirm route, deployment environment, and trailing path.
- HTTP 429: inspect target rate limits and retry policy before adding traffic.
- HTTP 500 through 599: use endpoint logs and trace IDs for the same timestamp.
- Network error: check DNS, TLS, firewall, and public reachability.
- Timeout: reduce endpoint work, move long processing behind a queue, or return
  an accepted response after durable enqueue.
- Intermittent duplicate side effects: add endpoint idempotency before enabling
  more retries.

## REST fallback

REST history access requires Ultra API access:

```bash
curl --fail-with-body \
  "https://api.crontap.com/v1/schedule/<schedule-id>/history?limit=50" \
  -H "ClientId: $CRONTAP_CLIENT_ID" \
  -H "ApiKey: $CRONTAP_API_KEY"
```

Prefer MCP when connected. It is available independently of Ultra REST access.

## Verification

- State the first failing timestamp, repeated signature, and last known success.
- Tie every recommendation to current configuration or history evidence.
- After a fix, verify both the HTTP outcome and the intended application side
  effect.
- Keep the previous evidence so a transient recovery is not mistaken for a
  permanent fix.

## Safety and plan limits

- Read operations do not authorize a configuration change.
- Never reveal hidden headers or ask Crontap to return stored secret values.
- Do not enable broad retries for 4xx responses without an explicit reason.
- If a proposed cadence or retry change hits an entitlement error, present its
  four-option ladder and smallest viable option.

## Troubleshooting

- A not-found result usually means a stale ID. List schedules in the connected
  account rather than guessing.
- History is retained by plan and may not cover the full incident window.
- A successful HTTP code does not prove downstream work completed. Check an
  application-level receipt, record, or trace.

## References

- [Crontap Agent Skills catalogue](https://crontap.com/skills)
- [Cron troubleshooting guide](https://crontap.com/guides/cron-troubleshooting)
- [Automatic retries](https://crontap.com/blog/introducing-automatic-retries-with-exponential-backoff)
- [Cron job monitoring](https://crontap.com/cron-job-monitoring)
- [Live REST API reference](https://api.crontap.com/docs/)
