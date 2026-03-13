---
name: board-meeting
description: Use when the user wants a status review, progress check, strategic update, or to receive new action items from the c-suite. Use when the user says "board meeting," "status update," "what should I focus on," or "check in."
---

# Board Meeting

## Overview

Run a structured leadership review. Process what the human has completed, dispatch active roles to assess their domains, synthesize findings, and deliver prioritized next steps.

**Core principle:** Input (human updates) → Analysis (role dispatches) → Output (synthesized priorities + new action items).

## On Load

1. Read `company-profile.md` — if missing, tell the user to run c-suite-onboarding first. Stop.
2. Read `HUMAN_AGENDA.md` — categorize items:
   - `[x]` completed with `NOTE:` → new inputs to act on
   - `[p]` in progress with `NOTE:` → may need plan adjustment
   - `[ ]` open → track what's still pending
3. Read all files in `docs/` — scan existing deliverables to understand current state.
4. Run the board meeting.

## Meeting Structure

### 1. Process Human Updates

For every `[x]` item, especially those with `NOTE:` feedback:
- Acknowledge completion
- Route the outcome to the relevant role (e.g., completed customer interviews → CPO + CMO)
- Flag any feedback that changes assumptions

For every `[p]` item with `NOTE:`:
- Check if the note signals a blocker or pivot
- Adjust plans accordingly

### 2. Dispatch Active Roles

Dispatch all roles that have existing deliverables or pending HUMAN_AGENDA items. Use the Task tool with `subagent_type: "general-purpose"` in parallel.

**Each role sub-agent receives:**
- Their role persona and thinking framework (from CEO skill role definitions)
- The full company profile
- The current HUMAN_AGENDA.md (so they see what's completed and what's pending)
- Their existing deliverables (paste content or reference file paths)
- Specific instruction: "Review your domain. What's on track? What's at risk? What should the founder do next? Update your deliverables if needed."

**Sub-agent output format:**
- **Status:** What's on track vs. at risk in your domain
- **Completed item impact:** How do completed HUMAN_AGENDA items change your recommendations
- **New action items:** What the c-suite can execute independently right now. If founder action is also needed, note it for the HUMAN_AGENDA backlog — do not let it block progress.
- **Updated deliverables:** Any files that need updating based on new information

### 3. Synthesize and Prioritize

After all roles report back:

- **Resolve conflicts** — If CMO says "focus on outreach" and CPO says "focus on MVP," make the strategic call.
- **Prioritize ruthlessly** — The founder is one person. Pick the top 3 things for this week.
- **Update HUMAN_AGENDA.md** — Add new items, archive completed items that have been processed.

### 4. Deliver the Report

Present to the user in this format:

```
## Board Meeting — [DATE]

### Progress Since Last Meeting
- [Completed items and their impact]

### Domain Updates
- **[Role]:** [1-2 sentence status]
- ...

### This Week's Priorities
1. [Most important action — why it matters]
2. [Second priority — why it matters]
3. [Third priority — why it matters]

### New Items Added to HUMAN_AGENDA.md
- [List of new action items by priority]

### Risks and Blockers
- [Anything that could derail the 3-month objectives]
```

## Anti-Patterns

| Bad behavior | What to do instead |
|---|---|
| Dispatching roles with no existing deliverables or agenda items | Only dispatch roles that have active work. Don't create busywork. |
| Listing 10+ priorities | A solo founder gets 3 priorities per week. Pick the highest-leverage ones. |
| Repeating old information without new synthesis | Every meeting should surface something new or reprioritize based on new data. |
| Skipping conflict resolution between roles | If roles disagree, make the call. That's the CEO's job. |
| Not updating HUMAN_AGENDA.md | The meeting isn't done until the agenda is updated with new items and processed completions. |
| Stalling on `[ ]` or `[p]` items | Human-pending items are not blockers for the c-suite. Acknowledge them, move past them, and find what can be executed independently right now. |

