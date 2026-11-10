---
name: session-health
description: "Check whether the current session has coherent guidance, focus, handoff state, working-tree ownership, and enough context to proceed safely. Use when starting, resuming, or diagnosing a confused session. Not for auditing the machine or deployed AI infrastructure; use $system-audit."
allowed-tools:
  - Read
  - Glob
  - Bash(ls*, cat*)
---

# Context Status: Session Health Check

On-demand diagnostic showing context usage, preservation state, and open work items. Fast and lightweight — no vault queries.

## What to Check

### 1. Context Usage Estimate (host-aware)

Use the active client's native context meter when it is exposed. A client adapter may provide a tool-call counter, but it is optional and must never be treated as shared memory. If no meter is available, report `SKIPPED (client does not expose context telemetry)`; do not guess a percentage from conversation length.

Calculate:
- Tool calls so far
- Estimated percentage (calls / 150)
- Which thresholds have fired (from the `fired` array)
- Time since last warning

### 2. Active Plan

Find the latest file in `log/plans/`:
- If found: show filename, first 3 lines, and whether it contains "APPROVED" or is still "DRAFT"
- If none: report "No active plan"

### 3. Latest Session Log

Find the latest non-compact `.md` file in `log/` (skip files with `-compact` in the name):
- If found: show filename and first 3 lines
- If none: report "No session log found"

### 4. Focus Freshness

Check when `.context/current-focus.md` was last modified:
- Show the modification date
- If older than 3 days: warn "Focus file is stale — consider running `update-focus`"
- Show the first 5 lines (headline)

### 5. Preservation and Continuity

Verify the client-neutral continuity files first: applicable root guidance, `.context/ai-handoff.md`, `.context/current-focus.md`, latest approved plan, and portable memory index. Then read `docs/reference/ai-surface-availability.md` or run the staged AI-infrastructure doctor to report each client hook adapter as CONFIGURED, UNAVAILABLE, or NOT APPLICABLE. Missing optional lifecycle hooks are informational when the files-first layer is healthy.

### 6. Open Loops

Count unchecked items (`- [ ]`) in `.context/current-focus.md`:
- Report the count
- If > 5: warn "Many open loops — consider triaging"

## Output Format

Present as a compact status panel:

```
## Session Health

| Metric | Value |
|--------|-------|
| Context usage | ~XX% (N/150 tool calls) |
| Thresholds fired | none / info / warning / critical |
| Active plan | filename (DRAFT/APPROVED) / none |
| Latest log | filename / none |
| Focus freshness | N days ago / stale warning |
| Open loops | N items |

### Preservation Hooks

| Hook | Status |
|------|--------|
| Files-first continuity | HEALTHY / DEGRADED |
| Current client lifecycle adapter | CONFIGURED / UNAVAILABLE / NOT APPLICABLE |
| Context telemetry | AVAILABLE / SKIPPED |

### Recommendations

[Only if there are issues — e.g., stale focus, missing hooks, high context usage]
```

### 7. Compaction Guidance

When context is high (>60%), include these reference tables in the output:

**When to compact:**

| Phase Transition | Compact? | Why |
|---|---|---|
| Research to Planning | Yes | Research context is bulky; plan is the distilled output |
| Planning to Implementation | Yes | Plan is in a file; free up context for code |
| Implementation to Testing | Maybe | Keep if tests reference recent code |
| Debugging to Next feature | Yes | Debug traces pollute context |
| Mid-implementation | No | Losing file paths and partial state is costly |
| After a failed approach | Yes | Clear dead-end reasoning |

**What survives compaction:**

| Persists | Lost |
|---|---|
| CLAUDE.md / AGENTS.md + rules | Intermediate reasoning |
| Task list | File contents previously read |
| MEMORY.md + `.context/` | Multi-step conversation context |
| Git state | Tool call history |
| Files on disk | Verbal preferences |
| `.context/ai-handoff.md` | — |

## When to Use

- When the context monitor fires a warning
- Before starting a large task (to check remaining capacity)
- After resuming a session (to verify state was preserved)
- When unsure if preservation hooks are working
