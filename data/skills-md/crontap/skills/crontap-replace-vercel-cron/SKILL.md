---
name: crontap-replace-vercel-cron
description: >
  Move a Vercel Cron schedule to Crontap while keeping the existing protected
  HTTP route, timezone intent, and rollback path. Use when a user wants an
  external scheduler for a Vercel deployment or has outgrown native cron limits.
license: MIT
metadata:
  version: "1.0.0"
  tools: create_schedule,pause_schedule,resume_schedule
---

# Replace Vercel Cron

Keep Vercel as the runtime and move only the clock. Crontap calls the deployed
route over HTTPS.

## Prerequisites

- Read the existing `vercel.json` cron path and expression.
- Confirm the production hostname and route method.
- Protect the route with a dedicated secret header.
- Make the handler idempotent before cutover.

## Cutover workflow

1. Add or verify route authentication in the Vercel application.
2. Test the protected production route with a controlled request.
3. Choose a cutover time and explain the brief overlap or gap risk.
4. Remove or disable the `vercel.json` schedule.
5. Create the matching Crontap schedule immediately.
6. Verify the resolved timezone, next runs, and first history entry.
7. Keep a rollback plan: pause Crontap, restore the Vercel cron, then deploy.

Do not leave both clocks enabled. Two schedulers can create duplicate side
effects even when both are operating correctly.

## MCP examples

Create the replacement:

```json
{
  "tool": "create_schedule",
  "arguments": {
    "url": "https://app.example.com/api/cron/daily-report",
    "cron": "0 9 * * 1-5",
    "timezone": "UTC",
    "method": "GET",
    "headers": {
      "Authorization": "Bearer <secret-from-secure-store>"
    },
    "label": "Vercel daily report"
  }
}
```

Pause for rollback or maintenance:

```json
{
  "tool": "pause_schedule",
  "arguments": {
    "scheduleId": "<schedule-id>"
  }
}
```

Resume the same configuration:

```json
{
  "tool": "resume_schedule",
  "arguments": {
    "scheduleId": "<schedule-id>"
  }
}
```

Confirm the selected ID before pause or resume.

## Protected route pattern

Compare the request authorization header with a server-only environment
variable. Return 401 before performing work when it does not match. Do not use
a secret in the query string or route path.

If the route queues work, persist the logical schedule period as an idempotency
key before enqueueing. Return success only after the queue accepts the job.

## REST fallback

REST creation requires Ultra API access:

```bash
curl --fail-with-body https://api.crontap.com/v1/schedule \
  -X POST \
  -H "ClientId: $CRONTAP_CLIENT_ID" \
  -H "ApiKey: $CRONTAP_API_KEY" \
  -H "Content-Type: application/json" \
  --data '{
    "url": "https://app.example.com/api/cron/daily-report",
    "interval": "0 9 * * 1-5",
    "timezone": "UTC",
    "verb": "GET",
    "headers": {
      "Authorization": "Bearer <secret-from-secure-store>"
    },
    "label": "Vercel daily report"
  }'
```

Use MCP for non-Ultra accounts.

## Verification

- Confirm the old Vercel schedule is absent from the deployed configuration.
- Confirm only one Crontap schedule targets the route.
- Verify a 401 without the secret and success with the secret.
- Inspect the first real run and the application-level side effect.

## Safety and plan limits

- Never paste the production route secret into the skill, repository, or chat.
- Pause before restoring the old scheduler during rollback.
- Preserve the original cadence's UTC semantics unless the user explicitly
  chooses a local IANA timezone.
- On a cap or cadence error, present the returned four-option ladder and
  smallest viable option.

## Troubleshooting

- A Vercel 401 means the configured schedule header and route secret differ.
- A 404 often means the route is not deployed on the hostname being called.
- Duplicate output means both clocks are active or endpoint idempotency failed.
- A timeout may require durable queueing instead of long synchronous work.

## References

- [Vercel Cron limits and alternatives](https://crontap.com/blog/vercel-cron-hourly-limit-and-how-to-beat-it)
- [Vercel Cron alternative](https://crontap.com/use-cases/vercel-cron-alternative)
- [Cron troubleshooting](https://crontap.com/guides/cron-troubleshooting)
- [Cron job monitoring](https://crontap.com/cron-job-monitoring)
