---
name: swarm
description: "Fan out N parallel workers, drain them, and return one report. Use for $swarm, 'swarm this', or parallel coverage, races, gauntlets, and exploration."
---

# Swarm

Delegation and optional capabilities follow `../poteto-mode/references/codex-agent-runtime.md`.

Fan out N isolated workers. They may cover separate slices, race the same brief, or mix both. The parent waits, aggregates, and returns one report. If subagents or safe isolation are unavailable, use the declared sequential-parent or partial-result fallback.

## Start

Open a todolist with one entry per phase before launching anything.

1. Frame
2. Fan out
3. Aggregate
4. Report

## Phase A: Frame

1. State the done predicate and the artifact or report the swarm must return.
2. Choose the shape. Partition into slices, race N workers on identical briefs, or mix both. For a race or mixed shape, declare `first pass`, `rank all`, or `best-of` before spawning.
3. Set N from the user or derive it from the shape. Cap N at observable runtime capacity. Queue excess lanes; never drop them silently.
4. Pick the worker model from `swarm workers` in the installed pstack model profiles when present. Otherwise use the configured fast profile. For a model race, name each arm's model up front.
5. Give each worker its own writable output when it writes. Use a worktree, branch, or `/tmp1-<slug>/worker-<n>/`.

## Phase B: Fan out

After proving independent reads or isolated writes, dispatch all ready workers together through supported subagent tools. Use an installed role profile when validated; otherwise use generic agents with inherited model pairs. A worker that needs local devices or live-control capabilities stays on the surface that provides them. For a non-default base, create or select the exact worktree or branch before dispatch and name it in the brief.

Every brief stands alone. Include the goal, scope, exact slice or race arm, how to verify, and what to report. Reports use `PASS`, `ISSUES`, or `BLOCKED` with evidence.

If a worker drops out, reconcile its partial state and make one bounded retry when safe. Otherwise proceed with a labeled partial result or fail closed when that lane is required.

## Phase C: Aggregate

Read the terminal results. For coverage, every required slice needs a result. For a race, apply the selection rule declared up front. Use first pass, rank all, or best-of. Do not paste raw worker dumps.

Keep a compact result table, one-line evidenced issues, and explicit gaps or dropouts.

## Phase D: Report

Return one consolidated in-chat report with the table, issue one-liners, gaps or dropouts, and the race rule when used.
