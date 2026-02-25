---
name: planning-foundation
description: Implements persistent file-based planning for complex tasks. Creates .planning/ directory with progress.md and findings.md. Use when starting complex multi-step tasks, research projects, or any task requiring >5 tool calls. Foundation layer inherited by all other skills.
---

# Planning Foundation

Work like Manus: Use persistent markdown files as your "working memory on disk."

Every workflow skill in superpower-planning inherits this foundation. `.planning/` is the "RAM on disk" for the current work session.

## Planning Directory Convention

```
.planning/                     # gitignored, ephemeral working state
├── findings.md                # aggregated findings
├── progress.md                # Task Status Dashboard + session log
└── agents/                    # created on demand by subagents
    ├── implementer/           # one dir per role, reused across tasks
    │   ├── findings.md        # this agent's discoveries (appended across tasks)
    │   └── progress.md        # this agent's action log (appended across tasks)
    ├── spec-reviewer/
    └── ...
```

Plans go in `docs/plans/`. `.planning/` is ephemeral session state. The `agents/` directory is NOT created at init — each subagent creates its own subdirectory when dispatched.

## Quick Start

Before ANY complex task:

1. **Create `.planning/` directory** with init script or manually
2. **Create `progress.md`** — Use [templates/progress.md](templates/progress.md) (includes Task Status Dashboard)
3. **Create `findings.md`** — Use [templates/findings.md](templates/findings.md) as reference
4. **Re-read plan before decisions** — Refreshes goals in attention window
5. **Update after each phase** — Mark complete, log errors

## The Core Pattern

```
Context Window = RAM (volatile, limited)
Filesystem = Disk (persistent, unlimited)

-> Anything important gets written to disk.
```

## File Purposes

| File | Purpose | What Goes Here | When to Update |
|------|---------|----------------|----------------|
| `findings.md` | Knowledge base: discoveries, decisions, surprises | Code patterns, architecture insights, technical decisions + rationale, rejected alternatives, unexpected behavior, edge cases, dependency constraints, debugging root causes | After ANY discovery or decision |
| `progress.md` | Operations log: status, actions, evidence | Task Status Dashboard rows, phase status changes, actions taken (files modified), error log + retries, test results, verification evidence, batch/phase summaries | After ANY status change, action, or error |

## Critical Rules

### 1. Create Planning Dir First
Never start a complex task without `.planning/`. Plans always go in `docs/plans/`. Execution status is tracked via the Task Status Dashboard in `progress.md`.

### 2. The 2-Action Dispatch Rule
> "After every 2 read/search/explore operations, IMMEDIATELY save to the appropriate file by content type."

**Dispatch by content type:**

| Content type | Target file | Examples |
|---|---|---|
| Discoveries, decisions, surprises | `findings.md` | Code patterns, constraints, approach chosen and why, edge cases |
| Status, actions, errors, results | `progress.md` | Task marked complete, files modified, error + retry, test pass/fail |

This prevents both knowledge AND progress from being lost.

### 3. Read Before Decide
Before major decisions, read the plan file. This keeps goals in your attention window.

### 4. Update After Act
After completing any phase:
- Mark phase status: `in_progress` -> `complete`
- Log any errors encountered
- Note files created/modified

### 5. Log ALL Errors
Every error goes in the plan file. This builds knowledge and prevents repetition.

```markdown
## Errors Encountered
| Error | Attempt | Resolution |
|-------|---------|------------|
| FileNotFoundError | 1 | Created default config |
| API timeout | 2 | Added retry logic |
```

### 6. Never Repeat Failures
```
if action_failed:
    next_action != same_action
```
Track what you tried. Mutate the approach.

## The 3-Strike Error Protocol

```
ATTEMPT 1: Diagnose & Fix
  -> Read error carefully
  -> Identify root cause
  -> Apply targeted fix

ATTEMPT 2: Alternative Approach
  -> Same error? Try different method
  -> Different tool? Different library?
  -> NEVER repeat exact same failing action

ATTEMPT 3: Broader Rethink
  -> Question assumptions
  -> Search for solutions
  -> Consider updating the plan

AFTER 3 FAILURES: Escalate to User
  -> Explain what you tried
  -> Share the specific error
  -> Ask for guidance
```

## Read vs Write Decision Matrix

| Situation | Action | Reason |
|-----------|--------|--------|
| Just wrote a file | DON'T read | Content still in context |
| Viewed image/PDF | Write findings NOW | Multimodal -> text before lost |
| Browser returned data | Write to file | Screenshots don't persist |
| Starting new phase | Read plan/findings | Re-orient if context stale |
| Error occurred | Read relevant file | Need current state to fix |
| Resuming after gap | Read all planning files | Recover state |

## The 5-Question Reboot Test

If you can answer these, your context management is solid:

| Question | Answer Source |
|----------|---------------|
| Where am I? | Task Status Dashboard in progress.md |
| Where am I going? | Remaining phases |
| What's the goal? | Goal statement in plan |
| What have I learned? | findings.md |
| What have I done? | progress.md |

## When to Use This Pattern

**Use for:**
- Multi-step tasks (3+ steps)
- Research tasks
- Building/creating projects
- Tasks spanning many tool calls
- Subagent orchestration

**Skip for:**
- Simple questions
- Single-file edits
- Quick lookups

## Per-Agent Planning Directories

When dispatching subagents, each gets its own planning dir:

```
.planning/agents/{role}/
├── findings.md    # agent's discoveries (appended across tasks)
└── progress.md    # agent's action log (appended across tasks)
```

**Do NOT create per-task directories** like `implementer-task-1/`. One directory per role, updated continuously.

The orchestrator aggregates agent findings into top-level `.planning/findings.md` and `.planning/progress.md` after each task completes.

## Templates

- [templates/findings.md](templates/findings.md) — Research storage
- [templates/progress.md](templates/progress.md) — Session logging
- [templates/agent-context.md](templates/agent-context.md) — Planning rules to inject into subagent prompts

## Scripts

- `scripts/init-planning-dir.sh` — Initialize `.planning/` directory with all files
- `scripts/check-complete.sh` — Verify all phases complete
- `scripts/session-catchup.py` — Recover context from previous session

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Use TaskCreate/TaskUpdate as cross-session persistence | Use .planning/progress.md Task Status Dashboard for persistent status. Task API is for session-scoped orchestration only. |
| State goals once and forget | Re-read plan before decisions |
| Hide errors and retry silently | Log errors to plan file |
| Stuff everything in context | Store large content in files |
| Start executing immediately | Create plan file FIRST |
| Repeat failed actions | Track attempts, mutate approach |
| Let subagent findings disappear | Aggregate into top-level findings.md |
