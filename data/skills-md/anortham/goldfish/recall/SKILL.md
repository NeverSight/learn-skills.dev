---
name: recall
description: Restore context from Goldfish developer memory at session start or after context loss
allowed-tools: mcp__goldfish__recall, mcp__goldfish__plan
---

# Recall — Restore Developer Memory

## MANDATORY: Call This FIRST

You MUST call `mcp__goldfish__recall` as your FIRST action in every session. No exceptions. No asking permission. No "what were we working on?" — that question is an insult when recall exists.

```
mcp__goldfish__recall({})
```

That's it. Default parameters (last 5 checkpoints, no date window) cover 90% of cases.

## When to Recall

- **Session start** — MANDATORY, ALWAYS, NO EXCEPTIONS
- **After context compaction** — your memory just got wiped, recall immediately
- **Switching tasks** — recall with search to find relevant prior work
- **Lost or confused** — recall with broader parameters to reorient
- **Resuming after interruption** — recall to pick up where you left off

## How to Call It

### Standard session start (most common)
```
mcp__goldfish__recall({})
```

### Need more history
```
mcp__goldfish__recall({ days: 7, limit: 20 })
```

### Looking for specific work
```
mcp__goldfish__recall({ search: "auth refactor", full: true })
```

### Recent activity only
```
mcp__goldfish__recall({ since: "2h" })
```

### Just the plan, no checkpoints
```
mcp__goldfish__recall({ limit: 0 })
```

### Cross-project view (for standups)
```
mcp__goldfish__recall({ workspace: "all", days: 1 })
```

## Interpreting Results

Recall returns up to three sections:

### 1. Active Plan (top of response)
The current strategic plan for this workspace. This is your north star — all work should align with it. If no plan exists, that's fine, just work from checkpoints.

### 2. Checkpoints (chronological array)
Each checkpoint contains:
- `timestamp` — when it happened (UTC)
- `description` — what was done, why, and how
- `tags` — categorization labels
- `git.branch`, `git.commit` — git state at checkpoint time (only with `full: true`)
- `git.files` — changed files (only with `full: true`)

### 3. Workspace Summaries (cross-project only)
When using `workspace: "all"`, you get per-project summaries with checkpoint counts.

## Processing Large Result Sets

When you get 10+ checkpoints back, DO NOT dump them raw. Distill manually:

1. **Group by date** — what happened each day
2. **Identify themes** — feature work, bug fixes, refactoring, planning
3. **Highlight blockers** — anything marked stuck, blocked, or failed
4. **Surface decisions** — architectural choices, tradeoffs made
5. **Find the thread** — what was the user working toward?

Present a concise summary: "Based on your recent work, you were [doing X] on [project area]. Last session you [accomplished Y] and the next step appears to be [Z]."

## Critical Rules

- **Trust recalled context.** Do NOT re-verify information from checkpoints. They were written by you in a previous session. They are accurate.
- **Continue work immediately.** After recall, do not ask "should I continue?" Just proceed based on restored context.
- **Never skip recall to save time.** It takes 2 seconds and prevents 20 minutes of confused fumbling.
- **Use search for targeted recall.** If you know roughly what you're looking for, `search` with fuse.js fuzzy matching is faster than scanning everything.
- **Keep context lean.** Default `limit: 5` exists for a reason. Only increase when you genuinely need deeper history.

## After Recall

Once you have context, ACT on it. The pattern is:

1. Recall (restore memory)
2. Understand (process what you get back)
3. Continue (pick up where the last session left off)

There is no step where you ask the user what to do. You already know — it's in the checkpoints.
