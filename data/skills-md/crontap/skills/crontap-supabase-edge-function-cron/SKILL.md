---
name: crontap-supabase-edge-function-cron
description: >
  Schedule a protected Supabase Edge Function or HTTP-facing RPC through
  Crontap with an external clock and observable delivery. Use when a user needs
  recurring Supabase work with retries, history, or failure alerts.
license: MIT
metadata:
  version: "1.0.0"
  tools: create_schedule
---

# Schedule a Supabase Edge Function

Use Supabase `pg_cron` for SQL-only database maintenance. Use this pattern when
the recurring unit is an HTTP Edge Function and an external scheduler is
desired.

## Prerequisites

- Deploy the function before creating its schedule.
- Make the function idempotent for one logical period.
- Protect it with a dedicated server-side cron secret.
- Never send a Supabase service-role key to Crontap.

## Function security pattern

Read a dedicated header or bearer value and compare it with a server-only
environment variable before doing work. If Supabase gateway JWT verification
is disabled for the function, this application-layer check is mandatory.

Keep the function response bounded. For long work, durably enqueue the job and
return success only after the queue accepts it.

## Workflow

1. Deploy the Edge Function and configure its cron secret.
2. Call it manually from a controlled environment with and without the secret.
3. Confirm expected status codes and idempotency behavior.
4. Create the Crontap schedule with the deployed HTTPS URL.
5. Verify the resolved cadence and first retained run.

## MCP example

```json
{
  "tool": "create_schedule",
  "arguments": {
    "url": "https://project-ref.supabase.co/functions/v1/nightly-cleanup",
    "text": "every day at 02:00",
    "timezone": "UTC",
    "method": "POST",
    "headers": {
      "Authorization": "Bearer <cron-secret-from-secure-store>",
      "Content-Type": "application/json"
    },
    "body": {
      "source": "crontap"
    },
    "label": "Supabase nightly cleanup"
  }
}
```

Use the real project reference from the Supabase project URL. Do not place a
secret in the function URL or JSON body.

## REST fallback

REST requires Ultra API access:

```bash
curl --fail-with-body https://api.crontap.com/v1/schedule \
  -X POST \
  -H "ClientId: $CRONTAP_CLIENT_ID" \
  -H "ApiKey: $CRONTAP_API_KEY" \
  -H "Content-Type: application/json" \
  --data '{
    "url": "https://project-ref.supabase.co/functions/v1/nightly-cleanup",
    "interval": "0 2 * * *",
    "timezone": "UTC",
    "verb": "POST",
    "headers": {
      "Authorization": "Bearer <cron-secret-from-secure-store>",
      "Content-Type": "application/json"
    },
    "data": {"source": "crontap"},
    "label": "Supabase nightly cleanup"
  }'
```

Prefer MCP when available.

## Verification

- A request without the cron secret returns 401 before side effects.
- A request with the secret returns the intended success status.
- Two requests for the same logical period create one durable side effect.
- The Crontap history outcome matches Supabase function logs at the same time.

## Safety and plan limits

- Do not use `SUPABASE_SERVICE_ROLE_KEY` as the scheduler credential.
- Scope the function to the narrow recurring operation.
- If the Supabase project can pause, remember that an external clock exposes
  the failure but cannot make an unavailable project execute.
- If Crontap rejects the cadence or capacity, present the returned four-option
  ladder and smallest viable option.

## Troubleshooting

- Supabase 401 means gateway or function authorization rejected the request.
- Supabase 404 usually means the project reference, function slug, or deploy
  environment is wrong.
- A 2xx with missing work requires application logs and an idempotency-record
  check.
- Timeouts are better fixed with durable queueing than aggressive retries.

## References

- [Supabase cron jobs](https://crontap.com/guides/supabase-cron-jobs)
- [Supabase Edge Function cron jobs](https://crontap.com/use-cases/cron-jobs-for-supabase-edge-functions)
- [Cron troubleshooting](https://crontap.com/guides/cron-troubleshooting)
- [Live REST API reference](https://api.crontap.com/docs/)
