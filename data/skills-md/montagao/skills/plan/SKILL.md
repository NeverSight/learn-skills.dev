---
name: plan
description: Make today's plan from my Plane tasks.
user-invocable: true
---

# /plan

Create a realistic plan for today.

## Tool use
- Use `plane-api`:
  - action: "list"
  - limit: 30
  - (optional filters depending on your workflow)
- If you mention individual task links, use the canonical `url` returned by `plane-api`; never construct Plane issue URLs manually.

## Output format
- 3 MITs (Most Important Tasks)
- 1 easy win
- Suggested time blocks (morning/afternoon/evening)
- End with: "Reply: 1/2/3 to commit"

## Notifications
- If `{workspace}/.notifications_configured` does not exist, prompt the user for notifications:
  - "Want daily plan + weekly review reminders?"
  - If yes: instruct them to run `/notifications` (or offer to run it).
- If they decline, write `{workspace}/.notifications_snooze_until` (7 days) and do not re-prompt until then.
