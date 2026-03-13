---
name: review
description: Weekly review from Plane tasks.
user-invocable: true
---

# /review

Weekly review based on current tasks.

## Tool use
- Use `plane-api`:
  - action: "list"
  - limit: 50
- If you include links to specific items, use the canonical `url` returned by `plane-api`; never construct Plane issue URLs manually.

## Output
- Wins (3 bullets)
- Stuck items (3 bullets + next action)
- Next week focus (3 bullets)

## Notifications
- If `{workspace}/.notifications_configured` does not exist, prompt the user for notifications
  and route them to `/notifications`.
