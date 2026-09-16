---
name: crontap-recurring-agent-endpoint
description: >
  Schedule an HTTP endpoint that a deployed application uses to start its own
  agent workflow, then monitor completion with a heartbeat. Use when a user has
  an application-owned agent runtime that needs a durable external clock.
license: MIT
metadata:
  version: "1.0.0"
  tools: create_schedule,create_heartbeat,get_heartbeat_pings
---

# Schedule an app-owned agent endpoint

Use this architecture only when the user controls a deployed HTTP service that
starts the workflow. Crontap schedules the HTTP request and monitors check-ins.
It does not wake agents, IDE sessions, chats, or MCP clients.

For a recurring prompt inside Cursor, Claude, ChatGPT, Codex, or another
client, use that client's native automation feature. MCP clients initiate tool
calls; an MCP server does not initiate contact with them.

## Architecture

```text
Crontap clock -> protected app endpoint -> app-owned queue -> agent worker
                                                     |
                                                     +-> heartbeat on completion
```

## Prerequisites

- A deployed application endpoint and durable worker already exist.
- The endpoint authenticates a dedicated cron secret.
- Enqueueing and downstream effects are idempotent by logical run period.
- The worker can securely read a heartbeat URL.

## Workflow

1. Create a heartbeat with a period and grace matching expected completion.
2. Store its secret URL in the worker's secret manager.
3. Update the worker to ping only after durable successful completion and use
   `/fail` for explicit terminal failure.
4. Create a Crontap schedule for the protected enqueue endpoint.
5. Verify enqueue evidence, worker evidence, and heartbeat evidence.

## MCP examples

Create completion monitoring:

```json
{
  "tool": "create_heartbeat",
  "arguments": {
    "name": "Daily agent workflow completion",
    "periodMinutes": 1440,
    "graceMinutes": 60
  }
}
```

Create the HTTP clock:

```json
{
  "tool": "create_schedule",
  "arguments": {
    "url": "https://agent-app.example.com/api/jobs/daily-analysis",
    "text": "every day at 07:00",
    "timezone": "UTC",
    "method": "POST",
    "headers": {
      "Authorization": "Bearer <cron-secret-from-secure-store>",
      "Content-Type": "application/json"
    },
    "body": {
      "workflow": "daily-analysis"
    },
    "label": "Daily analysis enqueue"
  }
}
```

Inspect heartbeat evidence for one UTC day:

```json
{
  "tool": "get_heartbeat_pings",
  "arguments": {
    "heartbeatId": "<heartbeat-id>",
    "day": "2026-09-14"
  }
}
```

## Endpoint contract

- Authenticate before reading the request body or enqueueing.
- Derive or receive a stable logical-run key and enforce uniqueness durably.
- Return 2xx only after the queue has accepted the job.
- Return a retryable 5xx only when another enqueue attempt is safe.
- Keep model provider credentials inside the worker environment.

## REST fallback

REST creation requires Ultra API access:

```bash
curl --fail-with-body https://api.crontap.com/v1/schedule \
  -X POST \
  -H "ClientId: $CRONTAP_CLIENT_ID" \
  -H "ApiKey: $CRONTAP_API_KEY" \
  -H "Content-Type: application/json" \
  --data '{
    "url": "https://agent-app.example.com/api/jobs/daily-analysis",
    "interval": "0 7 * * *",
    "timezone": "UTC",
    "verb": "POST",
    "headers": {
      "Authorization": "Bearer <cron-secret-from-secure-store>",
      "Content-Type": "application/json"
    },
    "data": {"workflow": "daily-analysis"},
    "label": "Daily analysis enqueue"
  }'
```

Use MCP when connected. MCP access is not Ultra-only.

## Verification

- One schedule call creates one durable queue record for the logical period.
- A worker retry does not duplicate external side effects.
- Success pings happen after durable completion, not merely after enqueue.
- A missing or failed run appears in heartbeat history without exposing the
  secret URL.

## Safety and plan limits

- Never expose model keys, cron secrets, or heartbeat URLs in prompts or logs.
- Bound cost, runtime, model calls, and external writes inside the app-owned
  worker.
- Use native client automation when no deployed endpoint exists.
- If a resource limit blocks creation, preserve the returned four-option
  ladder and identify the smallest viable option.

## Troubleshooting

- Schedule success plus heartbeat silence means enqueue succeeded but the
  worker did not complete or did not ping.
- Schedule failure means debug the HTTP boundary before the worker.
- Repeated queue records mean the enqueue endpoint lacks atomic idempotency.
- A pending heartbeat has not received its first accepted ping.

## References

- [Scheduled AI jobs](https://crontap.com/use-cases/scheduled-ai-jobs)
- [Crontap heartbeats](https://crontap.com/heartbeats)
- [Cron job monitoring](https://crontap.com/cron-job-monitoring)
- [Crontap MCP](https://crontap.com/mcp)
