---
name: crontap-ai-built-apps
description: >
  Add recurring HTTP work and liveness monitoring to apps built with Lovable,
  Bolt, Replit, or v0 by exposing a protected endpoint. Use when a user wants
  an AI-built app to perform durable scheduled work after deployment.
license: MIT
metadata:
  version: "1.0.0"
  group: patterns-migrations
  order: 11
  title: Add recurring work to an AI-built app
  summary: Give apps built with Lovable, Bolt, Replit, or v0 a secure HTTP boundary for recurring work.
  bestFor: Lovable, Bolt, Replit, and v0 projects
  guide: https://crontap.com/blog/scheduled-tasks-for-ai-built-apps
  guideTitle: Scheduled tasks for AI-built apps
  tools: create_schedule,create_heartbeat
---

# Recurring work for AI-built apps

The deployed app must expose an HTTP endpoint. Crontap owns the clock and calls
that endpoint. The builder chat is used to create code, not as the production
runtime for recurring prompts.

## Prerequisites

Before using the required tools, check whether they are available. If any are
missing, stop and offer the user exactly two choices:

1. Connect Crontap MCP at `https://mcp.crontap.com/mcp`. MCP access works on
   every Crontap tier.
2. Configure `$CRONTAP_CLIENT_ID` and `$CRONTAP_API_KEY` for the raw API. Raw
   API access requires Ultra.

Do not silently choose a path or continue until the user selects one.

- Identify the builder's deployed server or function runtime.
- Define one narrow recurring operation and its durable side effect.
- Add a server-only cron secret and idempotency storage.
- Confirm the production URL and IANA timezone.

## Builder prompt

Adapt this prompt to the app's framework:

```text
Create a POST /api/jobs/daily-report endpoint. Before any work, compare the
Authorization bearer value with the server-only CRON_SECRET environment
variable and return 401 on mismatch. Persist an idempotency key for the current
logical reporting day before creating side effects. Queue long work durably.
Return JSON with a bounded status and no secrets. Add tests for unauthorized,
first-run, and duplicate-run behavior.
```

Review the generated code. Verify that secret comparison and idempotency happen
server-side, not in browser code.

## Workflow

1. Generate and review the protected endpoint in the builder.
2. Deploy it and run authorized and unauthorized tests.
3. Optionally create a heartbeat for independent run evidence.
4. Create the schedule with the protected endpoint.
5. Inspect the first run in both Crontap and application logs.

## MCP examples

Create a heartbeat first when missed-run monitoring is useful:

```json
{
  "tool": "create_heartbeat",
  "arguments": {
    "name": "Daily report delivery",
    "periodMinutes": 1440,
    "graceMinutes": 30
  }
}
```

Store the returned ping URL securely. It can be connected to schedule outcome
webhooks or called by the deployed endpoint after durable completion.

Create the HTTP schedule:

```json
{
  "tool": "create_schedule",
  "arguments": {
    "url": "https://app.example.com/api/jobs/daily-report",
    "text": "every day at 08:00",
    "timezone": "America/New_York",
    "method": "POST",
    "headers": {
      "Authorization": "Bearer <cron-secret-from-secure-store>",
      "Content-Type": "application/json"
    },
    "body": {
      "source": "crontap"
    },
    "label": "AI-built app daily report"
  }
}
```

## REST fallback

REST requires Ultra API access:

```bash
curl --fail-with-body https://api.crontap.com/v1/schedule \
  -X POST \
  -H "ClientId: $CRONTAP_CLIENT_ID" \
  -H "ApiKey: $CRONTAP_API_KEY" \
  -H "Content-Type: application/json" \
  --data '{
    "url": "https://app.example.com/api/jobs/daily-report",
    "interval": "0 8 * * *",
    "timezone": "America/New_York",
    "verb": "POST",
    "headers": {
      "Authorization": "Bearer <cron-secret-from-secure-store>",
      "Content-Type": "application/json"
    },
    "data": {"source": "crontap"},
    "label": "AI-built app daily report"
  }'
```

Use MCP for connected non-Ultra accounts.

## Verification

- Confirm the endpoint is server-side and unavailable before authentication.
- Confirm duplicate requests for one logical period create one side effect.
- Verify the first Crontap run and the corresponding application record.
- If using a heartbeat, verify success and explicit failure paths separately.

## Safety and plan limits

- Never put a cron secret or heartbeat URL in client-side environment values.
- Avoid scheduling preview or development deployment URLs.
- Crontap does not keep the builder session open and does not initiate prompts.
- If creation hits a cap or cadence floor, present the returned four-option
  ladder and smallest viable option.

## Troubleshooting

- A 404 often means the builder did not deploy the server route.
- A 401 means the deployed environment and Crontap use different secrets.
- Platform sleep or cold starts can cause timeouts. Queue long work durably.
- Duplicate effects mean the endpoint's idempotency boundary is incomplete.

## References

- [Crontap Agent Skills catalogue](https://crontap.com/skills)
- [Scheduled tasks for AI-built apps](https://crontap.com/blog/scheduled-tasks-for-ai-built-apps)
- [Scheduled AI jobs](https://crontap.com/use-cases/scheduled-ai-jobs)
- [Cron jobs for Lovable](https://crontap.com/use-cases/cron-jobs-for-lovable)
- [Cron jobs for Bolt](https://crontap.com/use-cases/cron-jobs-for-bolt)
- [Cron jobs for Replit](https://crontap.com/use-cases/cron-jobs-for-replit)
