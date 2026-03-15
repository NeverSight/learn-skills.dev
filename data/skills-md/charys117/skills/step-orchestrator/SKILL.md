---
name: step-orchestrator
description: >-
  Coordinate a multi-agent implementation and review loop from a step table, then
  commit each approved step and write the result back to the table. Use when Codex
  receives a natural-language request that names a step-table source or location,
  explicit step IDs or ranges such as 3-5,7, and a target workspace or repository,
  and the work should alternate implementer and reviewer agents until approval.
---

# Step Orchestrator

Coordinate one requested step at a time from a step table.

## Require these inputs

- Require a step-table source or location.
- Require explicit step IDs or ranges such as `3-5,7`.
- Require the target workspace or repository. Treat the current workspace as the default only when the user does not name another one.
- Accept tests, constraints, branch preferences, and acceptance criteria as optional additions.

## Load references only when needed

- Read [references/adapter-contract.md](references/adapter-contract.md) before mutating an unfamiliar backend.
- Choose the step-table interaction path from the context already available in the session, such as installed skills, MCP tools, repository utilities, or built-in capabilities.
- Stop and report a blocker if the current context cannot safely inspect and update the named step table.

## Run the coordinator loop

- Inspect the source schema before mutating anything.
- Resolve the requested range against a sortable numeric or order field.
- Normalize duplicates and process steps in ascending order.
- Handle one step at a time. Do not overlap steps.
- For each step:
  1. Mark the step `In Progress`.
  2. Spawn fresh implementer `A1` dedicated only to that step. Do not attach or reuse an implementer thread from any earlier step. If the runtime exposes `fork_context`, set `fork_context=false`. Instruct it not to commit, tag, or update the step table.
  3. Wait for `A1` to finish and return a complete handoff for that step before doing any implementation work on the same step yourself.
  4. Mark the step `In Review`.
  5. Spawn fresh reviewer `B1` dedicated only to that step. Do not attach or reuse a reviewer thread from any earlier step. If the runtime exposes `fork_context`, set `fork_context=false`. Keep reviewer read-only.
  6. Wait for `B1` to return a final review result before doing any review work on the same step yourself.
  7. If reviewer `B1` rejects the work, append `B1` review history, set the step back to `In Progress`, and spawn implementer `A2` with the review notes.
  8. Continue `A<n> -> B<n>` rounds until the reviewer approves or a hard blocker prevents safe progress.
  9. After approval, stage only the approved step's changes and commit `step {id}: {step_title}`.
  10. Mark the step `Done` and write back the approval summary plus commit SHA and message.
  11. Retire the step's subagents before continuing. Do not carry any implementer or reviewer thread across the step boundary.
- Continue to the next requested step only after the current step is approved, committed, and written back.

## Keep side effects centralized

- Let implementer agents patch code and run the tests needed for that step.
- Let reviewer agents inspect and report findings, but never patch code.
- Let only the coordinator commit, update the step table, and decide whether a blocker is hard.
- While an implementer or reviewer round is active, let the coordinator orchestrate and wait. Do not let it silently absorb the same round just because the subagent is slow.

## Wait deliberately for spawned agents

- Treat each spawned `A<n>` or `B<n>` as the owner of that round until it finishes, reports a blocker, or is explicitly replaced.
- Use long waits and sparse polling. A single timeout or slow response is not permission for the coordinator to take over the round.
- If a subagent is slow, ask for a status update or continue waiting. Prefer patience over duplicate work.
- If a subagent stalls across multiple waits, first nudge it or replace it with a fresh subagent for the same role and same step. Preserve the round history and handoff context as explicit notes, diffs, file paths, and test results rather than hidden thread state.
- Let the coordinator take over a round only when subagent execution is impossible in the current session, and record that reason in the review history or blocker notes.
- Never start the next step while any subagent still owns the current step.

## Isolate subagents by step

- Treat every step boundary as a hard context boundary. Each step gets new implementer and reviewer threads even when the workspace, code area, and role stay the same.
- Never attach a later step to a subagent from an earlier step. Reusing agent history across steps is a workflow bug because it leaks assumptions and review context.
- Pass forward only explicit artifacts such as the step table state, written handoff notes, commits, and test results. Do not pass forward hidden thread state by reusing the same subagent.
- If you need context from a prior step, summarize it in the new step prompt or writeback instead of reviving the earlier subagent.

## Pass only step-local context to subagents

- Never spawn a step subagent with the coordinator thread history attached. If the spawning tool supports `fork_context`, keep it `false`.
- Build each subagent prompt from explicit step-local inputs only: step ID and title, the step body or acceptance criteria, relevant file paths, required test commands, the current round's reviewer notes, and any concrete approved artifacts from earlier steps that this step depends on.
- Do not dump the full coordinator conversation, unrelated repository exploration, or future-step plans into the subagent prompt.
- When a later step depends on an earlier one, pass a short dependency summary or concrete artifacts such as commit SHA, changed paths, interface notes, and test results.
- Treat any leakage of coordinator thread state into a subagent as a workflow failure because it lets the subagent infer or preempt work outside the active step.

## Shape subagent prompts narrowly

```text
Role: <implementer|reviewer> for step <id> only.
Workspace: <path>.
Active step:
- title: <step title>
- objective: <step body or goal>
- acceptance criteria: <criteria>
Relevant artifacts:
- files or directories: <paths>
- prior approved dependency notes: <only what this step needs>
- current round review notes: <same-step notes only>
Run tests: <commands>
Rules:
- work only on this step
- do not infer or start later steps
- do not use or request hidden coordinator thread context
- implementer: do not commit or update the step table
- reviewer: read-only, report findings and verdict only
```

## Enforce the minimum contract

- Require one sortable numeric or order field for range resolution. Stop before mutation if it is missing.
- Infer a writable status field and map the local flow to `Todo`, `In Progress`, `In Review`, and `Done`. Stop before mutation if no writable status-like field exists.
- Infer notes and commit fields by name. If either field is missing, fall back to page-body or comment writeback instead of skipping the history.
- Append review history by round. Do not overwrite earlier `B1`, `B2`, or later reviewer feedback.
- Treat unsupported backends, missing required schema primitives, unrecoverable test or setup failures, or conflicting user changes as hard blockers. Write the blocker back when the backend allows it, then stop.

## Use this prompt shape

```text
Use the step-orchestrator skill with step source <table location>.
Process steps 3-5 in workspace <path>.
Run an implementer/reviewer loop until each step is approved.
Run tests: <commands>.
Constraints: <constraints>.
```
