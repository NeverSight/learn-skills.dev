---
name: crontap-uptime-monitor
description: >
  Create and operate a Crontap uptime monitor, tune its failure threshold,
  pause it during deployments, and inspect probe evidence. Use when a user
  wants availability checks and down or recovery alerts for an HTTP endpoint.
license: MIT
metadata:
  version: "1.0.0"
  tools: create_monitor,update_monitor,get_monitor_probes
---

# Monitor an HTTP endpoint

Crontap uptime monitors send HTTP GET probes. HTTP 200 through 399 is healthy.
Network errors, timeouts, and other status codes count as failed probes.

## Prerequisites

- Select a lightweight health URL that represents the dependency being
  monitored.
- Confirm the required interval and consecutive-failure threshold.
- Decide whether planned deploys should pause the monitor.

## Workflow

1. Create the monitor with a name, URL, interval, and threshold.
2. Verify the saved cadence and pending state.
3. Inspect a UTC day of probes after the first checks run.
4. Set `status` to `paused` before a maintenance window when alerts would be
   misleading.
5. Set `status` to `pending` after maintenance to resume cleanly.

## MCP examples

Create a five-minute monitor that becomes down after two failures:

```json
{
  "tool": "create_monitor",
  "arguments": {
    "name": "Public API health",
    "url": "https://api.example.com/health",
    "intervalMinutes": 5,
    "failureThreshold": 2,
    "emailCooldownMinutes": 15
  }
}
```

Pause during maintenance:

```json
{
  "tool": "update_monitor",
  "arguments": {
    "monitorId": "<monitor-id>",
    "status": "paused"
  }
}
```

Resume after verification:

```json
{
  "tool": "update_monitor",
  "arguments": {
    "monitorId": "<monitor-id>",
    "status": "pending"
  }
}
```

Inspect probe evidence:

```json
{
  "tool": "get_monitor_probes",
  "arguments": {
    "monitorId": "<monitor-id>",
    "day": "2026-09-14"
  }
}
```

## REST fallback

Use REST only with Ultra API access:

```bash
curl --fail-with-body https://api.crontap.com/v1/monitor \
  -X POST \
  -H "ClientId: $CRONTAP_CLIENT_ID" \
  -H "ApiKey: $CRONTAP_API_KEY" \
  -H "Content-Type: application/json" \
  --data '{
    "name": "Public API health",
    "url": "https://api.example.com/health",
    "intervalMinutes": 5,
    "failureThreshold": 2
  }'
```

To pause, send `{"status":"paused"}` with PUT to
`/v1/monitor/<monitor-id>`. Use `pending` to resume.

## Verification

- Confirm at least one probe and its status code or network error.
- Check that a healthy endpoint transitions the monitor from pending to up.
- Use an intentionally separate test endpoint if validating down and recovery
  alerts. Do not break a production health route.
- Confirm the configured threshold matches the desired alert sensitivity.

## Safety and plan limits

- Monitor public or intentionally reachable endpoints. Do not expose a private
  admin route only to make it probeable.
- Avoid URLs with embedded credentials. Use an endpoint designed for health
  checks.
- Starter and paid plans have different monitor counts and cadence floors.
- If creation or update returns a plan-limit error, explain the four-option
  ladder and identify the smallest viable option.

## Troubleshooting

- A 401 or 403 probe means the health endpoint is not publicly probeable.
- Frequent short outages may require a higher failure threshold, but confirm
  user impact before masking them.
- A timeout can indicate a slow health handler or a downstream dependency.
- No probes while paused is expected.

## References

- [Crontap uptime monitoring](https://crontap.com/uptime)
- [Cron job monitoring](https://crontap.com/cron-job-monitoring)
- [Cron troubleshooting](https://crontap.com/guides/cron-troubleshooting)
- [Live REST API reference](https://api.crontap.com/docs/)
