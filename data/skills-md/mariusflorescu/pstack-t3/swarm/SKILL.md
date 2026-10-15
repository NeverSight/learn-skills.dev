---
name: swarm
description: "Fan out N parallel workers, drain them, and return one report. Use for /swarm, 'swarm this', or parallel coverage, races, gauntlets, and exploration."
disable-model-invocation: true
---

# Swarm

A skill named in bold or in backticks, or run as `/<name>`, is the file `../<name>/SKILL.md` beside this skill's directory, and a principle named without its prefix is `../principle-<name>/SKILL.md`. Read the file and follow it. Most pstack skills are user-only, so your skill tool cannot load them. Every `delegate_task` call follows the defaults in the Subagents section of `../poteto-mode/SKILL.md`.

Fan out N parallel workers. They may cover separate slices, race the same brief, or mix both. The parent waits, aggregates, and returns one report.

## Start

Open a task list (your harness's task tool, or a checklist file at `~/.local/state/pstack/checklists/<repo>-<branch>.md` when it has none) with one entry per phase before launching anything.

1. Frame
2. Fan out
3. Aggregate
4. Report

## Phase A: Frame

1. State the done predicate and the artifact or report the swarm must return.
2. Choose the shape. Partition into slices, race N workers on identical briefs, or mix both. For a race or mixed shape, declare `first pass`, `rank all`, or `best-of` before spawning.
3. Set N from the user or derive it from the shape. N is total workers, not a concurrency limit.
4. Pick the worker model from the `swarm workers` line in `~/.config/pstack/pstack-models.md`. An entry `<providerInstanceId>/<model> (<effort>)` becomes `target: {"providerInstanceId": ..., "model": ..., "options": {"<effort option id>": "<effort>"}}`, with the effort option id `orchestrator_capabilities` lists for that model. For `auto` or `inherit-parent`, or when the file or that line is missing, omit `target` so the workers run on the parent model. With no file, say so and suggest `/setup-pstack`. If `delegate_task` rejects an entry, use the closest model of the same provider that `orchestrator_capabilities` lists and say so. For a model race, name each arm's model up front. Pick each subagent's reasoning level and fast or standard speed for the job, per the Subagents section of the **poteto-mode** skill.
5. Give each worker its own writable output when it writes. When workers verify or measure commits, each brief names the exact SHAs. A measurement brief also names the method (sample count, what one sample is, order). The worker records both in its result.

## Phase B: Fan out

Spawn all N workers in one turn as `delegate_task` children with `mode: "async"`, a `title` naming the slice or race arm, and the step 4 `target`, left unset for `auto` or `inherit-parent`. Children share your checkout, so parallel writers there own disjoint files and run no git commands. A worker that needs its own tree or branch is a `t3_thread_launch` thread with `workspaceStrategy: {"type":"worktree","baseRef":"<commit or branch>","branch":"<new branch>","startFromOrigin":false}`, `modelSelection: {"instanceId": ..., "model": ..., "options": ...}` from step 4, and the brief in `message`. Commit first, because uncommitted edits do not reach a new worktree. One writer per worktree or branch.

When a worker must start from a non-default branch, launch it as a `t3_thread_launch` thread with that branch as `baseRef`.

Every brief stands alone. Include the goal, scope, exact slice or race arm, how to verify, and what to report. Reports use `PASS`, `ISSUES`, or `BLOCKED` with evidence. A worker that can prove a defect reports `ISSUES` and lists every issue it can prove, not only the first.

End the turn after spawning. Each child's completion notification wakes you. Use `task_status` only when you need a result mid-turn, and `t3_thread_wait` for a launched thread. If a worker drops out, proceed with N-1 and note it.

## Phase C: Aggregate

Read the terminal results. Drop a result that does not record the SHAs and method its brief names, and respawn that worker once. After a second miss, record a gap. A gap does not count as a pass. For coverage, every required slice needs a result. For a race, apply the selection rule declared up front. Use first pass, rank all, or best-of. Do not paste raw worker dumps.

Keep a compact result table, one-line evidenced issues, and explicit gaps or dropouts.

## Phase D: Report

Return one consolidated in-chat report with the table, issue one-liners, gaps or dropouts, and the race rule when used.
