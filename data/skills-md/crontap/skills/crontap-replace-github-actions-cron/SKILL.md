---
name: crontap-replace-github-actions-cron
description: >
  Replace a GitHub Actions schedule trigger with a Crontap HTTP dispatch while
  keeping the workflow, runner, and logs on GitHub. Use when a user needs a
  timezone-aware external clock or wants to avoid scheduled-workflow drift.
license: MIT
metadata:
  version: "1.0.0"
  group: patterns-migrations
  order: 9
  title: Replace GitHub Actions cron
  summary: Replace drifting repository schedules with a protected dispatch endpoint and evidence for every triggered run.
  bestFor: Repository dispatch, drift, and timezone-safe triggers
  guide: https://crontap.com/blog/github-actions-cron-drift-problem
  guideTitle: GitHub Actions cron drift
  tools: create_schedule,pause_schedule,resume_schedule
---

# Replace GitHub Actions cron

Crontap sends a repository dispatch request. GitHub still runs the workflow.

## Prerequisites

Before using the required tools, check whether they are available. If any are
missing, stop and offer the user exactly two choices:

1. Connect Crontap MCP at `https://mcp.crontap.com/mcp`. MCP access works on
   every Crontap tier.
2. Configure `$CRONTAP_CLIENT_ID` and `$CRONTAP_API_KEY` for the raw API. Raw
   API access requires Ultra.

Do not silently choose a path or continue until the user selects one.

- Make the workflow safe to dispatch more than once.
- Create a fine-grained GitHub token restricted to the target repository with
  the permission required by the repository dispatch endpoint.
- Store the token in a secure store and plan its expiration and rotation.
- Confirm the desired IANA timezone.

## Change the workflow

Replace the scheduled trigger with manual and repository dispatch triggers:

```yaml
on:
  workflow_dispatch:
  repository_dispatch:
    types: [scheduled-run]
```

Keep `workflow_dispatch` for manual operation. Crontap calls
`repository_dispatch`. Do not leave `on.schedule` enabled after cutover.

## Workflow

1. Commit and deploy the dispatch-capable workflow.
2. Test a repository dispatch with a non-production-safe workflow path.
3. Remove the old `schedule` trigger at the agreed cutover time.
4. Create the Crontap schedule.
5. Verify GitHub returns 204 and one workflow run appears.
6. Pause the Crontap schedule during maintenance or rollback.

## MCP examples

Create the external dispatch:

```json
{
  "tool": "create_schedule",
  "arguments": {
    "url": "https://api.github.com/repos/example-org/example-repo/dispatches",
    "text": "every weekday at 09:00",
    "timezone": "Europe/London",
    "method": "POST",
    "headers": {
      "Authorization": "Bearer <fine-grained-token-from-secure-store>",
      "Accept": "application/vnd.github+json",
      "X-GitHub-Api-Version": "2022-11-28",
      "Content-Type": "application/json"
    },
    "body": {
      "event_type": "scheduled-run"
    },
    "label": "GitHub scheduled run"
  }
}
```

Pause:

```json
{
  "tool": "pause_schedule",
  "arguments": {
    "scheduleId": "<schedule-id>"
  }
}
```

Resume:

```json
{
  "tool": "resume_schedule",
  "arguments": {
    "scheduleId": "<schedule-id>"
  }
}
```

## REST fallback

REST creation requires Ultra API access:

```bash
curl --fail-with-body https://api.crontap.com/v1/schedule \
  -X POST \
  -H "ClientId: $CRONTAP_CLIENT_ID" \
  -H "ApiKey: $CRONTAP_API_KEY" \
  -H "Content-Type: application/json" \
  --data '{
    "url": "https://api.github.com/repos/example-org/example-repo/dispatches",
    "interval": "0 9 * * 1-5",
    "timezone": "Europe/London",
    "verb": "POST",
    "headers": {
      "Authorization": "Bearer <fine-grained-token-from-secure-store>",
      "Accept": "application/vnd.github+json",
      "X-GitHub-Api-Version": "2022-11-28",
      "Content-Type": "application/json"
    },
    "data": {"event_type": "scheduled-run"},
    "label": "GitHub scheduled run"
  }'
```

## Verification

- Confirm the deployed workflow no longer contains `on.schedule`.
- Confirm `event_type` matches the workflow's dispatch type exactly.
- Verify one Crontap run corresponds to one GitHub workflow run.
- Confirm a non-expired token is scoped only to the required repository and
  operation.

## Safety and plan limits

- Never use a broad classic token when a restricted fine-grained token works.
- Avoid top-of-hour assumptions when comparing old GitHub timing evidence.
- Make downstream workflow writes idempotent.
- If the Crontap create call hits a cap or cadence floor, present the returned
  four-option ladder and smallest viable option.

## Troubleshooting

- GitHub 401 means the token is invalid or expired.
- GitHub 403 usually means repository access or permissions are insufficient.
- GitHub 404 can intentionally hide a repository the token cannot access.
- GitHub 422 often means the event type or request body is invalid.
- Duplicate runs usually mean both the old schedule trigger and Crontap remain
  active.

## References

- [Crontap Agent Skills catalogue](https://crontap.com/skills)
- [GitHub Actions cron drift](https://crontap.com/blog/github-actions-cron-drift-problem)
- [Crontap vs GitHub Actions cron](https://crontap.com/alternatives/github-actions-cron)
- [GitHub repository dispatch API](https://docs.github.com/en/rest/repos/repos#create-a-repository-dispatch-event)
- [Cron troubleshooting](https://crontap.com/guides/cron-troubleshooting)
