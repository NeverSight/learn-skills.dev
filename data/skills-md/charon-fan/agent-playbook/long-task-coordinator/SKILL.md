---
name: long-task-coordinator
description: Coordinates multi-session, delegated, or long-running work with persistent state, recovery checks, and explicit status transitions. Use when a task spans multiple turns, multiple agents, background jobs, or scheduled loops, or when interrupted work must be resumed reliably.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion
metadata:
  hooks:
    after_complete:
      - trigger: session-logger
        mode: auto
        reason: "Log long-task coordination activity"
---

# Long Task Coordinator

> Keep long-running work recoverable, stateful, and honest.

## When to Use This Skill

Use this skill when the work:
- Spans multiple turns or multiple sessions
- Involves handoffs to workers, subagents, or background jobs
- Needs explicit waiting states instead of "still looking" updates
- Must survive interruption and resume from a durable state file

Skip this skill for small, single-turn tasks. Use `planning-with-files` when simple planning is enough and recovery logic is not the main concern.

## Related Skills

- `planning-with-files` keeps multi-step work organized in files.
- `workflow-orchestrator` chains follow-up skills after milestones.
- `long-task-coordinator` makes long-running work resumable, auditable, and safe to hand off.

## Core Rules

### 1. Create one source of truth

For any real long task, maintain one durable state file. Chat history is not a reliable state store.

The state file should capture at least:
- Goal
- Success criteria
- Current status
- Current step
- Completed work
- Next action
- Next checkpoint
- Blockers
- Active owners or workers

### 2. Separate roles only when needed

Use the smallest role model that fits the task:
- **Origin**: owns the goal and acceptance criteria
- **Coordinator**: owns state, sequencing, and recovery
- **Worker**: executes bounded sub-work
- **Watchdog**: checks liveness and recovery only

Simple tasks can collapse these roles into one agent. Long or delegated tasks should make the split explicit.

### 3. Run every cycle in this order

For each coordination round:

```text
READ -> RECOVER -> DECIDE -> PERSIST -> REPORT -> END
```

Do not report conclusions before the state file has been updated.

### 4. Treat `awaiting-result` as a valid state

If a worker or background job was dispatched successfully, the task is not failing just because the result is not back yet.

Valid transitions include:
- `running -> awaiting-result`
- `awaiting-result -> running`
- `running -> paused`
- `running -> complete`

### 5. Non-terminal rounds must create real progress

A coordination round is only valid if it does at least one of the following:
- Dispatches bounded work
- Consumes new results
- Updates the current stage or decision
- Persists a new next step or checkpoint
- Performs explicit recovery

If nothing changed, do not pretend the task advanced.

### 6. Keep recovery separate from domain work

Recovery answers:
- Did execution drift from the saved state?
- Is the expected worker result still pending?
- Do we need to wait, retry, or re-dispatch?

Domain work answers:
- What should we build, analyze, or deliver next?

Recover first, then continue domain work.

## Operating Workflow

### Step 1: Decide whether the task needs coordination

Use this skill when at least one is true:
- The task will outlive the current turn
- The task will hand off work to another execution unit
- The task needs checkpoints, polling, or scheduled follow-up
- The task has enough complexity that loss of state would be expensive

### Step 2: Create or load the state file

Prefer a path that is easy to rediscover, such as:
- `docs/<topic>-execution-plan.md`
- `docs/<topic>-state.md`
- `worklog/<topic>-state.md`

If no durable state exists yet, create one from `references/workflow.md`.

### Step 3: Recover before acting

At the start of every new round:
1. Read the state file
2. Check whether the recorded next step still makes sense
3. Confirm whether any delegated work returned
4. Repair stale assumptions before new action

### Step 4: Persist before reporting

After deciding the next action:
1. Update the state file
2. Record new status, owners, blockers, and checkpoint
3. Only then report progress to the user or caller

### Step 5: Close the round honestly

End each round with one of these states:
- `running`
- `awaiting-result`
- `paused`
- `blocked`
- `complete`

The reported status should match the persisted status exactly.

## Output Expectations

When using this skill, produce updates that are grounded in saved state:
- What status the task is in now
- What changed this round
- What is expected next
- What would unblock or complete the task

## Acceptance Criteria

Treat the coordination work as complete only when all relevant items below are true:

- A durable state file exists in a predictable path
- The saved status matches the real task state
- Completed work, next action, and blockers are recorded explicitly
- Any delegated work has a named owner and a return condition
- The final report is derived from the persisted state, not from transient reasoning

If the task is not truly complete, end in `running`, `awaiting-result`, `paused`, or `blocked` rather than pretending the work is done

## Anti-Patterns

Avoid:
- Reconstructing progress from memory instead of the state file
- Reporting a conclusion before saving it
- Marking waiting as failure
- Ending a round with no new action and no state change
- Mixing recovery checks with domain decisions in one fuzzy step

## References

- `references/workflow.md` - Detailed workflow, state template, and recovery checklist
