---
name: crontap-natural-language-schedules
description: >
  Translate plain-English timing into a reviewed cron expression and concrete
  next runs without creating a schedule. Use when a user describes a recurring
  cadence in words or when timezone and calendar wording is ambiguous.
license: MIT
metadata:
  version: "1.0.0"
  tools: preview_schedule
---

# Preview natural-language schedules

Use this skill to resolve timing before another skill creates or updates a
schedule. A preview is read-only.

## Prerequisites

- Identify the user's intended local timezone.
- Ask whether business-day wording means weekdays or a holiday-aware calendar.
- Capture any boundary requirement, such as start date or final day of month.

## Phrase schedules precisely

Prefer phrases with a frequency, local time, and calendar scope:

- `every weekday at 09:15`
- `every 6 hours`
- `at 02:30 every Sunday`
- `on the first day of every month at 08:00`

Avoid phrases such as `in the morning`, `twice a month`, `month end`, or
`weekdays` without a timezone. Five-field cron cannot represent every
holiday-aware or last-business-day rule.

## Workflow

1. Resolve an exact IANA timezone with the user.
2. Call `preview_schedule` with the original cadence and timezone.
3. If the response needs clarification, present its question and options.
4. Preview again with the user's answer.
5. Report the resolved cron, timezone, and every returned next run.
6. Ask for confirmation before any separate create or update operation.

## MCP example

```json
{
  "tool": "preview_schedule",
  "arguments": {
    "text": "every weekday at 09:15",
    "timezone": "America/New_York"
  }
}
```

Do not save a guessed cron if the response has `needs_clarification` or
`rejected` status. Treat returned options as choices, not as permission to pick
for the user.

## DST and calendar checks

- Verify next runs on both sides of a nearby daylight-saving transition.
- A named timezone preserves local wall-clock intent. A UTC schedule preserves
  a fixed UTC time.
- Confirm whether `weekday` excludes only Saturday and Sunday.
- For last-business-day logic, schedule a safe candidate cadence and put the
  final calendar check inside an idempotent endpoint.
- For one-time work, use a one-time schedule only after confirming its exact
  timestamp and cleanup behavior.

## REST fallback

The public API fallback requires Ultra API access:

```bash
curl --fail-with-body https://api.crontap.com/v1/schedule/preview \
  -X POST \
  -H "ClientId: $CRONTAP_CLIENT_ID" \
  -H "ApiKey: $CRONTAP_API_KEY" \
  -H "Content-Type: application/json" \
  --data '{"text":"every weekday at 09:15","timezone":"America/New_York"}'
```

MCP remains available without Ultra. Prefer MCP when connected.

## Safety and plan limits

- Previewing does not consume resource capacity.
- A valid preview can still produce a cadence below the account's creation
  floor. Creation is the authoritative entitlement check.
- If creation later returns a plan-limit response, preserve its four-option
  ladder and identify the smallest viable plan.
- Never infer user consent to create from a read-only preview.

## Troubleshooting

- If the phrase is rejected, simplify it to one frequency and one local time.
- If the cron looks right but next runs look wrong, check the timezone first.
- If a desired calendar rule cannot be represented, move that condition into
  the endpoint and keep the endpoint idempotent.

## References

- [Cron from English](https://crontap.com/tools/cron-from-english)
- [Cron syntax reference](https://crontap.com/blog/cron-syntax-cheatsheet)
- [Cron troubleshooting](https://crontap.com/guides/cron-troubleshooting)
- [Machine-readable product reference](https://crontap.com/llms.txt)
