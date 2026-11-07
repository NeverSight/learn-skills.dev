---
name: team-implement
description: 'Use for executing implementation plans only on explicit request. Never infer from a ready plan.'
effort: medium
argument-hint: "[docs/plans/<id>/]"
---

# Team Implement

Before each dispatch or retry, read [host dispatch](../team/references/15-host-dispatch.md) and supply its resolved installed paths.
Before artifact work, read [artifact schema](../team/references/artifacts.md).
Before each consuming step, read its linked shared rules from this installed skill directory.
If a required read fails, stop that step with the exact path. Never use checkout fallback or recursive loading.
Before finalizing prose you author, read the [writing standards](../team/references/writing.md).

## Core contracts

- Require `7-structure.md`, `8-plan.md`, and a non-default-branch worktree. Use `AskUserQuestion` only for missing standalone setup.
- With `4-repos.md`, multi-repo work requires worktrees; refuse in-place execution.
- After the implementer's completion report, print **"Next: run `/team-code-review docs/plans/<id>/`"** in every mode. Never load `team-code-review` or `team-pr`.

## Procedure references

Read each reference completely when reaching it, in order.

1. [Input](references/01-input.md)
2. [Worktree Check](references/02-worktree-check.md)
3. [Execution](references/03-execution.md)

## Applied principles

Read and apply: [execution rules](../team/references/execution.md).
