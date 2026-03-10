---
name: memory-ledger
description: Maintain a structured ledger of decisions, discovered bugs and fixes, user preferences, constraints, current status, and failed approaches throughout multi-step agentic tasks. Auto-update after every significant step. Triggers on "where were we", "continue", "summarize status", "remember", or when a new agent instance takes over a task.
---

# Memory Ledger Protocol

Keep a structured log of everything learned during a task. Goal: when a new instance takes over, it reads the ledger and continues from where things left off — no starting from scratch.

---

## Ledger Structure

One ledger block per task. Updated incrementally as the task progresses — never rewritten from scratch.

```
MEMORY LEDGER
Task        : [task name / short description]
Started     : [first step number or timestamp]
Last updated: [step number or description]

## Goal
[What is being done — 1-2 sentences. Scope and success criteria.]

## User Preferences & Constraints
- [Preference / constraint 1]
- [Preference / constraint 2]
[If empty: "None established yet"]

## Decisions Made
| # | Decision | Rationale | Step |
|---|----------|-----------|------|
| 1 | [what was decided] | [why] | [which step] |

## Current Status
Completed  : [list or "—"]
In progress: [list or "—"]
Pending    : [list or "—"]

## Failed Approaches
| Approach | Why It Failed | Step |
|----------|---------------|------|
| [what was tried] | [error / issue] | [which step] |
[If empty: "None yet"]

## Bugs & Fixes
| Bug | Fix | Status |
|-----|-----|--------|
| [error message / description] | [applied fix] | Fixed / Open |
[If empty: "None yet"]

## Next Step
[The next thing to do — clear and actionable]
```

---

## Update Rules

Update the ledger when **any** of these events occur:

| Event | Section to Update |
|-------|-------------------|
| Subtask completed | Current Status, Next Step |
| Decision made | Decisions Made |
| Error occurred | Bugs & Fixes |
| Error resolved | Bugs & Fixes (update status) |
| Approach failed | Failed Approaches |
| User stated preference/constraint | User Preferences & Constraints |

**Updates must be small and surgical** — only change the affected section, do not rewrite the entire ledger.

---

## Handover Protocol

When a new instance takes over a task, first action is to read the ledger:

```
LEDGER READ — Task resumed
Task    : [task name]
Status  : [current status summary]
Next    : [next step]
Warning : [if any open bugs or failed approaches]
Continuing...
```

---

## Ledger Close

When the task is complete, close the ledger:

```
LEDGER CLOSED
Task completed
Total steps   : N
Decisions made: N
Bugs resolved : N
```

---

## When to Skip

- Single-step, short tasks (< 5 minutes, < 3 steps)
- User is only asking a question, no task
- Context is already small and manageable

---

## Guardrails

- **Never let the ledger grow stale** — if 3+ steps pass without an update, force one.
- **Keep entries concise** — one line per decision, one line per bug. No paragraphs.
- **Cross-skill**: integrates with `task-decomposer` (tracks subtask progress), `error-recovery` (logs errors and fixes), and `agent-reviewer` (provides retrospective data).
