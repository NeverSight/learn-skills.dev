---
name: crontap-heartbeat-for-cron
description: >
  Add a Crontap dead-man's-switch heartbeat to an existing recurring job,
  inspect check-ins, and rotate its secret token safely. Use when a user needs
  alerts for a cron job that fails explicitly or stops running.
license: MIT
metadata:
  version: "1.0.0"
  group: main
  order: 5
  title: Add a heartbeat to a recurring job
  summary: Add reliable check-ins to an existing recurring job and receive an alert when expected reports stop.
  bestFor: Missed jobs, grace periods, and explicit failures
  guide: https://crontap.com/heartbeats
  guideTitle: Heartbeat monitoring
  tools: create_heartbeat,get_heartbeat_pings,rotate_heartbeat_token
---

# Add a heartbeat to a recurring job

A heartbeat monitors a job that already has its own clock. The job pings after
successful work. Silence beyond the period and grace window becomes a missed
check-in, while the `/fail` variant reports explicit failure.

## Prerequisites

Before using the required tools, check whether they are available. If any are
missing, stop and offer the user exactly two choices:

1. Connect Crontap MCP at `https://mcp.crontap.com/mcp`. MCP access works on
   every Crontap tier.
2. Configure `$CRONTAP_CLIENT_ID` and `$CRONTAP_API_KEY` for the raw API. Raw
   API access requires Ultra.

Do not silently choose a path or continue until the user selects one.

- Know the job's real maximum interval, including expected jitter.
- Choose a grace window long enough for ordinary delay and runtime.
- Decide which component securely stores the returned ping URL.

## Workflow

1. Create the heartbeat with the expected period and grace.
2. Capture the returned ping URL once and store it as a secret.
3. Add a success ping only after the job completes successfully.
4. Add a `/fail` ping to the job's handled failure path.
5. Inspect ping history after deployment and after any incident.
6. Rotate the token only for compromise or planned credential rotation.

## MCP examples

Create a daily heartbeat with 30 minutes of grace:

```json
{
  "tool": "create_heartbeat",
  "arguments": {
    "name": "Nightly import",
    "periodMinutes": 1440,
    "graceMinutes": 30,
    "emailCooldownMinutes": 60
  }
}
```

The response contains a secret ping URL. Do not echo it into source control,
CI logs, support tickets, or later agent messages.

Inspect one UTC day:

```json
{
  "tool": "get_heartbeat_pings",
  "arguments": {
    "heartbeatId": "<heartbeat-id>",
    "day": "2026-09-14"
  }
}
```

Rotate after explicit confirmation:

```json
{
  "tool": "rotate_heartbeat_token",
  "arguments": {
    "heartbeatId": "<heartbeat-id>"
  }
}
```

Rotation invalidates both variants of the old URL immediately. Update the job
with the newly returned URL before its next deadline.

## Job integration

Use an environment variable such as `CRONTAP_HEARTBEAT_URL`.

```bash
run_the_job &&
  curl --fail --silent --show-error "$CRONTAP_HEARTBEAT_URL"
```

On a handled failure, call
`"$CRONTAP_HEARTBEAT_URL/fail?msg=bounded-error-summary"`. Keep messages free
of credentials, personal data, and large stack traces.

## REST fallback

REST requires Ultra API access. MCP does not.

```bash
curl --fail-with-body https://api.crontap.com/v1/heartbeat \
  -X POST \
  -H "ClientId: $CRONTAP_CLIENT_ID" \
  -H "ApiKey: $CRONTAP_API_KEY" \
  -H "Content-Type: application/json" \
  --data '{
    "name": "Nightly import",
    "periodMinutes": 1440,
    "graceMinutes": 30
  }'
```

## Verification

- Send one test success from the deployed job environment.
- Confirm the heartbeat moves from pending after an accepted ping.
- Exercise a safe failure path and verify a `fail` event without exposing the
  ping URL.
- Check that the period plus grace reflects the job's worst normal runtime.

## Safety and plan limits

- The ping URL is a credential. Anyone holding it can report activity.
- A heartbeat detects silence but does not start or restart the job.
- Starter heartbeat cadence and count limits differ from paid plans. Let the
  create response enforce the current account.
- On a plan-limit response, present its four-option ladder and the smallest
  viable option without inventing prices.

## Troubleshooting

- No deadline starts until the first accepted ping.
- Pings while paused record history but do not change deadlines.
- Repeated rapid pings may be rate limited while still returning HTTP 200.
- If the old URL stops working after rotation, that is expected. Deploy the
  replacement secret.

## References

- [Crontap Agent Skills catalogue](https://crontap.com/skills)
- [Crontap heartbeats](https://crontap.com/heartbeats)
- [Scheduled AI jobs](https://crontap.com/use-cases/scheduled-ai-jobs)
- [Cron job monitoring](https://crontap.com/cron-job-monitoring)
- [Live REST API reference](https://api.crontap.com/docs/)
