---
name: crontap-retries-and-idempotency
description: >
  Configure Crontap retry policy safely and design scheduled endpoints so
  repeated requests do not duplicate side effects. Use when a user needs
  reliable delivery, exponential backoff, or help diagnosing duplicate work.
license: MIT
metadata:
  version: "1.0.0"
  tools: update_schedule,get_schedule_history
---

# Retries and idempotency

Retries improve delivery only when the endpoint can safely receive the same
logical job more than once. Make the receiver idempotent before broadening a
retry policy.

## Prerequisites

- Identify the schedule and each side effect it can create.
- Decide which failures are transient for this endpoint.
- Choose a stable deduplication key and retention window.

## Workflow

1. Inspect recent history to classify failures.
2. Add endpoint idempotency and test duplicate requests.
3. Update only the schedule's retry policy.
4. Verify a controlled transient failure and its eventual success.
5. Recheck history for attempt count, delay, and final outcome.

## MCP examples

Inspect failures before changing policy:

```json
{
  "tool": "get_schedule_history",
  "arguments": {
    "scheduleId": "<schedule-id>",
    "limit": 50
  }
}
```

Retry common transient classes:

```json
{
  "tool": "update_schedule",
  "arguments": {
    "scheduleId": "<schedule-id>",
    "retryPolicy": {
      "enabled": true,
      "maxRetries": 3,
      "baseDelayMs": 60000,
      "retryOn": ["5xx", "429", "network", "timeout"]
    }
  }
}
```

Allowed base delays are 30000, 60000, 300000, and 900000 milliseconds. The
maximum retry count is 5. Include `4xx` only when this specific endpoint uses a
known transient 4xx response.

## Endpoint idempotency pattern

Use a unique database constraint or atomic insert keyed by a logical job
identity:

```text
key = job-name + ":" + scheduled-period
insert key before side effects
if key already exists, return the recorded result
perform side effects once
store completion outcome
```

For money movement, email, provisioning, or external writes, pass the same key
to downstream systems that support idempotency. Do not rely on an in-memory
set, because restarts and multiple instances lose that protection.

## REST fallback

Custom policy management through REST requires Ultra API access:

```bash
curl --fail-with-body \
  https://api.crontap.com/v1/schedule/<schedule-id> \
  -X PUT \
  -H "ClientId: $CRONTAP_CLIENT_ID" \
  -H "ApiKey: $CRONTAP_API_KEY" \
  -H "Content-Type: application/json" \
  --data '{
    "retryPolicy": {
      "enabled": true,
      "maxRetries": 3,
      "baseDelayMs": 60000,
      "retryOn": ["5xx", "429", "network", "timeout"]
    }
  }'
```

MCP remains the preferred path and is not Ultra-only.

## Verification

- Send the same logical request twice and verify one durable side effect.
- Induce a safe transient failure in a non-production target.
- Confirm history records the retries and final result expected by the policy.
- Confirm alerting occurs after the final failed outcome, not on a successful
  recovery.

## Safety and plan limits

- Custom retry policy settings require Pro, Ultra, or legacy Pro. Standard
  automatic retry behavior remains available on Starter.
- Retrying authentication and validation failures usually adds load without
  improving success.
- Never reduce idempotency retention below the maximum retry window.
- If configuration returns `RETRY_POLICY_NOT_CONFIGURABLE`, present the
  structured four-option ladder and smallest viable option.

## Troubleshooting

- Duplicate work with one history entry usually comes from application logic
  or another caller, not a Crontap retry.
- Duplicate work across attempts means the receiver's dedupe transaction is
  incomplete or scoped too narrowly.
- Repeated 429 responses require rate-limit coordination, not more attempts.
- Omitted update fields preserve existing schedule secrets and settings.

## References

- [Automatic retries with exponential backoff](https://crontap.com/blog/introducing-automatic-retries-with-exponential-backoff)
- [Cron troubleshooting](https://crontap.com/guides/cron-troubleshooting)
- [Cron job monitoring](https://crontap.com/cron-job-monitoring)
- [Machine-readable product reference](https://crontap.com/llms.txt)
