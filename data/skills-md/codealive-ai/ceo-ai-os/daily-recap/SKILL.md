---
name: daily-recap
description: End-of-day consolidation — summarize daily log, track belief changes and customer conversations, promote durable facts to MEMORY.md
---

# Daily Recap

End-of-day consolidation. Triggered by heartbeat at 21:00-22:00 or manually ("recap the day").

## Algorithm

### 1. Read today's log

Open `memory/YYYY-MM-DD.md`. If empty or no entries — ask: "Quiet day. Any customer conversations or belief changes to log before we close?" If still nothing → HEARTBEAT_OK.

### 2. Extract key items

From all entries of the day, compile:

```markdown
## Daily Recap

**Customer conversations:** X today (Y this week, target 8-12/week)
- [who]: [key insight or outcome]

**Belief changes:** (what shifted in understanding)
- [was] -> [became] (evidence: [what showed it])

**Decisions:** (decisions made today)
- [decision]: [why] -> [what changes]

**Open threads:** (started but not finished)
- [topic]: [what remains to be done]

**Constraint check:** [current constraint] — today [exploit/subordinate/ignore]?
```

### 3. Conversation count + Focus status

Count customer conversations from today's log entries. Update `memory/heartbeat-state.json` field `weeklyConversations` (increment). If it's Monday — reset to 0.

If weekly count < 4 by Wednesday or < 6 by Friday — add warning: "Below target. What's blocking customer contact?"

Read `memory/focus-state.json`:
- GTM minimum today: done/waived/missed
- Streak: N days
- Waivers this week: N (list reasons if any)
- If `daily_minimum.done == false` at recap time and no waiver → note neutrally: "GTM не стартовал сегодня. Завтра снизим порог."

### 4. Check for promotion to MEMORY.md

For each belief change, ask:
- Does this change something in MEMORY.md? (Company, Wedge, PMF Stage, Metrics, Constraint)
- Is it sufficiently confirmed? (not a single data point)

If yes — update MEMORY.md. Keep MEMORY.md < 3KB.

### 5. Write recap to daily log

Append the `## Daily Recap` block to `memory/YYYY-MM-DD.md`.

### 6. Update heartbeat state

Set `"lastRecapDate": "YYYY-MM-DD"` in `memory/heartbeat-state.json`.

## Telegram Output Format

```
Day recap:

GTM: [done ✓ / waived (reason) / missed ✗]
Streak: N дн | Waivers: N/week

Conversations: X today (Y/week, target 8-12)
[list if any]

Belief changes: Z
[list — most important]

Decisions: N
[list if any]

Constraint: [exploit/subordinate/ignore today]
```

If the day was empty AND GTM missed: "Тихий день. GTM не стартовал — завтра снизим порог. Что-нибудь запомнить перед закрытием?"

Follow output preferences from USER.md (language, format, platform constraints).

## Rules

- Max 15 lines for Telegram
- Don't fabricate — only from today's entries
- Belief changes > conversations > decisions > threads by importance
- If MEMORY.md was updated — mention: "MEMORY.md updated: [what exactly]"
- If 0 conversations AND 0 belief changes — note factually, offer lower threshold for tomorrow
