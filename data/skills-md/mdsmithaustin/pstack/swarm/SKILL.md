---
name: swarm
description: "Fan out N parallel workers, drain them, and return one report. Use for /swarm, 'swarm this', or parallel coverage, races, gauntlets, and exploration."
---

# Swarm

Fan out N parallel workers. They may cover separate slices, race the same brief, or mix both. The parent waits, aggregates, and returns one report.

## Start

Open a worklist with one entry per phase before launching anything.

1. Frame
2. Fan out
3. Aggregate
4. Report

## Phase A: Frame

1. State the done predicate and the artifact or report the swarm must return.
2. Choose the shape. Partition into slices, race N workers on identical briefs, or mix both. For a race or mixed shape, declare `first pass`, `rank all`, or `best-of` before spawning.
3. Set N from the user or derive it from the shape. N is total workers, not how many run at once.
4. Pick each worker's role by what it does. Use the **pstack-harness** skill for the spawn. Its **Spawn a role** section resolves the role and builds this CLI's spawn call.
   - A worker that runs something and reports what it saw uses the `swarm workers` role, default `sonnet`. Its `PASS` or `ISSUES` comes from a command's output or an observed result. Gate, live, regression, and perf lanes, coverage slices, and exploration partitions are this kind.
   - A worker that reads code, a diff, or another artifact and judges it uses the `trail reviewer` role, default `opus`. Audit and review lanes are this kind, and so is a worker that both runs something and judges the work. Before you spawn it, find the model that wrote the work, because **Spawn a role** passes it as `--work-model` and the resolver picks a different model in the work model's family for this role when the config allows one. When that model is unknown, run the role as resolved and say so in the report.
   - For a model race, name each arm's model up front. A named arm overrides both roles.
5. Give each worker its own writable output when it writes. When workers verify or measure commits, each brief names the exact SHAs. A measurement brief also names the method (sample count, what one sample is, order). The worker records both in its result.

## Phase B: Fan out

Spawn all N workers in one message with no persona, `run_in_background: true`, and the spawn call **Spawn a role** builds from each worker's step 4 role.

A worker that must start from another pushed branch gets a worktree at that branch's SHA, named in its brief.

Every brief stands alone. Include the goal, scope, exact slice or race arm, how to verify, and what to report. Reports use `PASS`, `ISSUES`, or `BLOCKED` with evidence. A worker that can prove a defect reports `ISSUES` and lists every issue it can prove, not only the first.

For races, use the **arena** skill's [required-arm rule](../arena/SKILL.md#required-arms). For coverage, a missing required slice makes the report incomplete. Retain useful results and record the gap. A discretionary worker may drop out with a recorded limitation.

## Phase C: Aggregate

Read the terminal results. Drop a result that does not record the SHAs and method its brief names, and respawn that worker once. After a second miss, record a gap. A gap does not count as a pass. For coverage, every required slice needs a result. For a race, apply the selection rule declared up front. Use first pass, rank all, or best-of. Do not paste raw worker dumps.

Keep a compact result table, one-line evidenced issues, and explicit gaps or dropouts.

## Phase D: Report

Return one consolidated in-chat report with the table, issue one-liners, gaps or dropouts, and the race rule when used.
