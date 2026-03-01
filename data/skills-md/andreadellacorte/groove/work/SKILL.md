---
name: work
description: "Compound engineering loop — 5 stages to reduce rework. Use when: (1) starting new work (brainstorm); (2) planning implementation (plan); (3) writing code (work); (4) evaluating output (review); (5) capturing lessons (compound). NOT for: daily rhythm (use daily); task management only (use task)."
license: MIT
allowed-tools: Read Write Edit Glob Grep Bash(git:*) AskUserQuestion
metadata:
  author: andreadellacorte
  version: "0.1.0"
---

<!-- groove:managed — do not edit; changes will be overwritten by groove update -->

# work

The compound engineering loop — five discrete stages that systematically reduce rework by front-loading clarity and back-loading lessons. Each stage can be run independently or in sequence.

## Git Root Detection

Before running any command, detect the git root:

```bash
git rev-parse --show-toplevel
```

## Commands

| Command | Description |
|---|---|
| `brainstorm` | Clarify scope through dialogue, surface key decisions and open questions |
| `plan` | Research codebase, write concrete implementation plan |
| `work` | Execute the plan, track progress in task backend |
| `review` | Evaluate output, identify lessons, decide accept/rework |
| `compound` | Document lessons, update rules/templates/docs |

## $ARGUMENTS Routing

| $ARGUMENTS | Action |
|---|---|
| `help` | → `commands/help.md` |
| `brainstorm` | → `commands/brainstorm.md` |
| `plan` | → `commands/plan.md` |
| `work` | → `commands/work.md` |
| `review` | → `commands/review.md` |
| `compound` | → `commands/compound.md` |
| _(empty)_ | → `commands/help.md` |

## Stage Task Naming

Each stage creates or updates a task in the configured backend (if `tasks != none`). Tasks follow the naming convention:

```
YYYY-MM-DD, <N>. <Stage>
```

e.g. `2026-02-28, 1. Brainstorm`, `2026-02-28, 2. Plan`

Tasks are created under the relevant workstream epic if one exists.

## Frustration Detection

If the user shows signs of repeated fixes, confusion, or rework — proactively suggest running `work compound` even mid-stream. The value of compound is in capturing lessons before they fade.

## Design Note

80% of the compound loop's value comes from `plan` and `review`. `work` is execution. Do not skip `plan` — scope creep and rework almost always trace back to an unclear plan.
