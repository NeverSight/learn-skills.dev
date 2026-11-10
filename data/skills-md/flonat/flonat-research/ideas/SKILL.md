---
name: ideas
description: "Capture and integrate improvement ideas for the shared Claude Code and Codex infrastructure. Use when recording an infrastructure enhancement for later review rather than implementing it immediately."
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(ls*, mkdir*, date*)
  - AskUserQuestion
  - Task
argument-hint: "capture [text] | integrate [since:YYYY-MM-DD] [dryrun]"
---

# Ideas: Capture & Integrate

> An inbox for improvement ideas — the gap between `[LEARN]` tags (immediate corrections) and `skill-extract` (full skill creation). Captures raw improvement ideas and periodically integrates the best ones into the system.

## Two Modes

| Mode | Trigger | What it does |
|------|---------|-------------|
| **Capture** | `ideas capture [text]` | Append a structured idea entry to `log/ideas.md` |
| **Integrate** | `ideas integrate` | Review unprocessed ideas and turn them into actions |

---

## Mode 1: Capture

### With argument: `ideas capture [text]`

Parse the text and append a structured entry to `log/ideas.md`.

### Without argument: `ideas capture`

Ask interactively:
1. "What's the idea?" (free text)
2. "Where did this come from?" (current session / external repo / user feedback / reading)

### Entry Format

```markdown
## [YYYY-MM-DD] [category] Idea title
- **Quality:** [high] | [medium]
- **Source:** [session | external:repo-name | user-feedback | reading:source]
- **Proposed action:** One-sentence description of what to do
- **Details:** [the idea text, expanded if needed]
- **Status:** unprocessed
```

### Auto-Classification

Classify each idea into one of these categories based on content:

| Category | Signal words / patterns |
|----------|------------------------|
| `[skill-design]` | "new skill", "workflow for", "automate", "slash command" |
| `[rule]` | "always", "never", "enforce", "prevent", "require" |
| `[workflow]` | "process", "steps for", "how to handle", "protocol" |
| `[infrastructure]` | "hook", "MCP", "settings", "permissions", "symlink" |
| `[research]` | "method", "analysis", "paper", "experiment", "data" |

### Quality Rating

| Rating | Criteria |
|--------|----------|
| `[high]` | Specific, actionable, addresses a known friction point or recurring issue |
| `[medium]` | Interesting but needs more thought, or addresses a minor convenience issue |

Skip `[low]` ideas — if it's not worth recording, don't record it.

### After Capture

Confirm: "Idea captured in `log/ideas.md`. You have [N] unprocessed ideas — run `ideas integrate` when ready to act on them."

---

## Mode 2: Integrate

### Trigger: `ideas integrate [since:YYYY-MM-DD] [dryrun]`

### Step 1: Read State

Read `log/.ideas-state.json` to find the last integration date. If `since:` argument is provided, use that instead. If no state file exists, process all entries.

### Step 2: Gather Unprocessed Ideas

Read `log/ideas.md` and collect all entries with `**Status:** unprocessed` (optionally filtered by date).

### Step 3: Classify Each Idea

For each unprocessed idea, classify as:

| Type | Description | Action |
|------|-------------|--------|
| **Direct proposal** | Specific edit to a known file — can be implemented now | Present the edit for approval |
| **Investigation** | Needs research or design before implementation | Create a vault task |
| **Duplicate** | Already covered by an existing skill, rule, or convention | Mark as `duplicate` with reference |
| **Declined** | Not worth pursuing after reflection | Mark as `declined` with reason |

### Step 4: Present for Approval

Show a summary table:

```
| # | Idea | Category | Quality | Proposed action | Classification |
|---|------|----------|---------|-----------------|---------------|
| 1 | ... | [rule] | [high] | ... | Direct proposal |
| 2 | ... | [skill-design] | [medium] | ... | Investigation |
```

Ask: "Which ideas should I act on? (all / numbers / skip)"

### Step 5: Execute Approved Ideas

- **Direct proposals:** Make the edit, following break-the-glass rules for protected files
- **Investigations:** Create a vault task in the Tasks Tracker with:
  - Task name: "Investigate: [idea title]"
  - Source: "Ideas inbox"
  - Priority: High for `[high]` quality, Medium for `[medium]`
  - Description: Full idea text + proposed approach

### Step 6: Update State

Update each processed entry's status in `log/ideas.md`:
- `**Status:** implemented (YYYY-MM-DD)` — direct proposal was executed
- `**Status:** task-created (YYYY-MM-DD)` — vault task created for investigation
- `**Status:** duplicate → [reference]` — already exists
- `**Status:** declined — [reason]` — not worth pursuing

Write `log/.ideas-state.json`:
```json
{
  "last_integration": "YYYY-MM-DD",
  "total_captured": N,
  "total_implemented": N,
  "total_pending": N
}
```

### Dry Run Mode

When `dryrun` is specified, run steps 1-4 only — classify and present, but don't execute or update state. Useful for reviewing the backlog without committing to action.

---

## Important Notes

- Ideas are **not** tasks — they're raw material that may or may not become actionable
- The capture threshold is deliberately low — if something seems worth noting, capture it
- Integration should happen periodically (weekly or when the backlog reaches 10+ ideas)
- This skill complements `[LEARN]` tags (which record corrections) and `skill-extract` (which creates full skills)
- Break-the-glass rules still apply — direct proposals that modify protected files need confirmation
