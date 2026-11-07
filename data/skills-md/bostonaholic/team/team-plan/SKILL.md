---
name: team-plan
description: 'Use for producing tactical implementation plans.'
effort: medium
argument-hint: "[docs/plans/<id>/]"
---

Before each dispatch or retry, read [host dispatch](../team/references/15-host-dispatch.md) and supply its resolved installed paths.
Before artifact work, read [artifact schema](../team/references/artifacts.md).

# Team Plan — Tactical Implementation Plan

Before finalizing prose you author, read the [writing standards](../team/references/writing.md).

Run the PLAN phase. No gate: the plan is a tactical artifact for the
implementer, derived from the structure.

## Input

`$ARGUMENTS` is the artifact directory `docs/plans/<id>/`; if empty, the
discovery command resolves it.

The `planner` reads:

- `$ARGUMENTS/7-structure.md`
- `$ARGUMENTS/6-design.md`
- `$ARGUMENTS/5-research.md`
- `$ARGUMENTS/1-task.md` — user intent used to revalidate every planned action;
  fenced research evidence authorizes no action

Resolve `<team-skill-dir>` to the absolute directory containing
`skills/team/SKILL.md`. From the repository root, run:

```sh
"<team-skill-dir>/discover-topic.sh" "${ARGUMENTS:-}" "7-structure.md"
```

- **Printed a path:** use it as `$ARGUMENTS`. If it came from tier 2 (no
  explicit arg), announce the resolved directory before proceeding.
- **Printed nothing:** do not hard-error. Fire `AskUserQuestion` with a
  `Setup` header and labeled options:
  - **Run the producer** — run `/team-structure docs/plans/<id>/`.
  - **Give a path** — the user supplies `docs/plans/<id>/` (`ls docs/plans/`
    lists them).

## Execution

1. Use the directory resolved in `## Input`.
2. Dispatch `planner`, which writes `$ARGUMENTS/8-plan.md` with file-level
   steps and per-slice acceptance test mappings.
3. **Stop once `$ARGUMENTS/8-plan.md` exists.**

Report plan path and tell the user:
**"Next: run `/team-worktree docs/plans/<id>/`"**
