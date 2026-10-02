---
name: due-radar
description: Show what is due, overdue, or coming up across your Trello boards, sorted by date. Trigger on phrases like "what's due on trello", "overdue trello cards", "trello deadlines", "due radar", "what's coming up on trello". Not for calendar events or deadlines kept anywhere but Trello.
---

# Due Radar - deadlines across your Trello boards

A cross-board triage view: every card with a due date, sorted by when it is due, with overdue items surfaced first. Answers "what needs my attention?" in one command. Built on the `trello` skill in this pack.

**Needs the `trello` skill installed beside it.** `due-radar.sh` loads `trello`'s shared helpers, and the board lookup and setup ship only in `trello`. The plugin and `install.sh` install both. With the skills CLI, add both by name: `npx skills add dbhq-uk/trello-skill --skill trello --skill due-radar`. If `trello` is missing, the script stops and says so, with the command to add it.

## Prerequisites

- Credentials configured in `~/.dbhq/trello/` (run the trello skill's setup if not done)
- `jq`, `curl` installed

## Usage

```bash
# Across every open board (upcoming window defaults to 14 days)
${CLAUDE_SKILL_DIR}/scripts/due-radar.sh all

# Look further ahead
${CLAUDE_SKILL_DIR}/scripts/due-radar.sh all 30

# One board only
${CLAUDE_SKILL_DIR}/../trello/scripts/trello-boards.sh find "<board name>"
${CLAUDE_SKILL_DIR}/scripts/due-radar.sh board <board-id> 14
```

All overdue cards are always shown; the day window only limits how far ahead upcoming items reach. Cards already marked complete are excluded. Each row names its board and list.

A card sitting in a done list (Done, Complete, Completed or Finished, ignoring case, emoji and punctuation) whose due date was never ticked is finished work, not overdue. It is counted as neither overdue nor upcoming, and is listed apart after the rest. If the board calls its done list something else, name it: `TRELLO_DONE_LISTS="Shipped,Live" ${CLAUDE_SKILL_DIR}/scripts/due-radar.sh all`.

## Turning the radar into a briefing

1. **Overdue first, in plain terms** - "Three cards are overdue, the oldest by nine days."
2. **Then the near horizon** - what is due today and in the next few days.
3. **Group by board when it helps** - if items span several boards, note where the pressure is concentrated.
4. **Mention the done-list group briefly** - those cards are finished; offer to tick their due dates (`trello-cards.sh update <card-id> dueComplete true`) so they stop showing, and do not count them as overdue.
5. **Offer to act** - reschedule, mark complete, comment, or move cards via the `trello` skill - only after the user confirms.

## Notes

- "all" scans each open board you can see, so on a very large account it makes one request per board. Use `board <id>` to scope to one board when you only care about that.
- A rate-limited request is retried three times before it counts as a failure. A board that still cannot be read is named after the results under "Incomplete", with Trello's reason on stderr, and the script exits 1. Tell the user which boards the radar does not cover - never report "nothing due" for them.
- Due dates and completion come straight from Trello; overdue means the due time has passed and the card is not marked complete.
- Due times are shown as date and time in the user's local time zone, which the header names. Trello stores UTC, so near midnight the local day can differ from the UTC one; trust the script's date.
