---
name: morning-brief
description: "Daily Morning Brief for CEO (09:30 cron). Reports what bot DID overnight, presents pre-staged GTM action for approval, shows pipeline status. Replaces old morning-briefing skill. Output = one Telegram message, max 15 lines."
user-invocable: true
---

## [YOUR_PRODUCT] Context

Read MEMORY.md for: constraint, ICP, wedge, metrics.
Read today's and yesterday's memory files.
Follow output preferences from USER.md. For chat platforms: keep under ~15 lines.

# Morning Brief

The CEO's primary daily touchpoint. Runs at 09:30 via cron. The brief is a REPORT of what was done + ONE action for approval. Not a nudge or question.

## Data Sources (read all before composing)

1. `memory/autonomous-actions.jsonl` — what bot did since last brief
2. `memory/pipeline.json` — current pipeline state
3. `memory/outreach-feedback.jsonl` — any responses received
4. `memory/focus-state.json` — GTM streak, daily minimum status
5. `memory/initiatives.json` — active multi-day projects
6. `memory/hypotheses.json` — active hypotheses
7. `memory/pr-opportunities.json` — found PR opportunities
8. `memory/github-stars.json` — recent stars

## Compose the Brief

### Section 1: Overnight Report (2-4 lines)
What the bot autonomously did since yesterday's recap:
- Enrichments completed
- Community replies published
- Pipeline changes (new prospects, updated scores)
- Signal scanner results
- PR opportunities found

If nothing happened: "Ночью без изменений."

### Section 2: GTM Action (3-5 lines)
Run `focus-keeper` (Mode: Morning Plan) to generate ONE pre-staged action.
Show the actual draft/deliverable inline.
Format: "→ [what CEO does]. Reply 'go' — сделаю."

Rules:
- ONE action only, no A/B/C menus
- Draft must be ready (not "I could draft...")
- Monkey-friendly: describe what CEO does, not the task
- Include time commitment (e.g., "3 мин")
- If pipeline has warm leads → prioritize follow-up over cold outreach
- RSD-aware: async email > LinkedIn comment > cold call

### Section 3: Status Line (1-2 lines)
```
Pipeline: N prospects | Streak: N дн | Hypotheses: N active
```

If outreach-feedback has new responses, mention them.

### Section 4: Pending Tier B Approvals (0-3 lines, only if items exist)
Items from autonomous work that need CEO approval:
- Draft emails to send
- LinkedIn posts to publish
- Content to approve

Format: "Tier B: [N] items pending. Reply 'show' to review."

## Output Template

```
Доброе утро.

Ночью:
- [action 1]
- [action 2]

→ [GTM action description] (N мин)
[draft inline]
Reply "go" — отправлю. "Позже" — вечером.

●○○○○○○ (N/7) | Pipeline: N | Hypotheses: N
```

## Rules

- Max 15 lines total
- No meta-questions ("how many conversations this week?")
- No shaming or compassion protocols — just report + action
- If CEO has ignored 5+ consecutive briefs, shrink to 3-line format
- After 3+ missed days, use fairy method (Dorofeyev) once, then just report
- Log brief delivery to autonomous-actions.jsonl

## Related Skills

- **focus-keeper** — generates the GTM action
- **evening-recap** — the other daily touchpoint
- **pipeline-manager** — manages pipeline data
- **structured-log** — logging
