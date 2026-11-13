---
name: multi-agent-orchestration
description: Split a large task across parallel sub-agents with clean role boundaries and a merge step. Use when the user asks to "parallelize", "use multiple agents", "fan out", or when a task has independent workstreams that bottleneck on one agent.
---

# Multi-Agent Orchestration

Decompose work into independent units, dispatch them to sub-agents in parallel, and reconcile the results. The orchestrator owns decomposition, the contract, and the merge — sub-agents own execution only.

## When to use

Use when the task has **genuinely independent** subtasks (separate files/modules, parallel research threads, fan-out search) and the serial cost is real. The win comes from independence.

Do **not** use when subtasks share mutable state, must run in sequence, or the coordination overhead exceeds the work. One focused agent beats five stepping on each other.

## Decompose

Split so each unit is:

- **Independent** — no shared mutable state; no unit depends on another's output mid-flight.
- **Self-contained** — the prompt carries all context (paths, constraints, definition of done). Sub-agents do not see the conversation.
- **Verifiable** — a clear, checkable deliverable.

If two units must touch the same file or one needs another's result, either merge them into one unit or sequence them — don't parallelize.

## Dispatch

- Launch independent units in a **single batch** so they run concurrently; do not spawn one, await, repeat.
- Give each agent: objective, exact scope (in *and* out), inputs/paths, output format, done criteria.
- Match the agent to the job (read-only exploration vs. implementation vs. review).
- Cap concurrency at the real independence width — more agents than independent units just adds merge cost.

## Roles (assign explicitly)

- **Orchestrator** — decomposes, dispatches, merges, resolves conflicts. Writes no feature code.
- **Workers** — execute one unit, report a structured result.
- **Reviewer** (optional) — independent agent checks merged output against the spec; never reviews its own work.

## Merge

1. Collect structured results; the worker's message is the only thing returned — relay what matters.
2. Detect conflicts: overlapping edits, contradictory findings, drifted assumptions.
3. Reconcile deliberately (orchestrator decides; re-dispatch a unit if a worker missed scope).
4. Run an integration check on the combined result — units green individually can break together.

## Anti-patterns

- "Parallel" agents editing the same file → race and lost work.
- Sequential dispatch (spawn, wait, spawn) labeled as parallel — no speedup.
- Vague sub-prompts assuming conversation context the agent can't see.
- Accepting merged output without an integration check.
- Spawning N agents for 2 independent units.

## Done when

Every unit's deliverable meets its criteria, conflicts are resolved, and the integrated result passes an end-to-end check against the original objective.