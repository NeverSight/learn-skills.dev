---
name: team-code-review
description: 'Use for running the Team code review phase only on explicit request. Never infer from a plain review request. Reviews and fixes the branch.'
effort: medium
argument-hint: "[docs/plans/<id>/]"
---

# Team Code Review

Before each dispatch or retry, read [host dispatch](../team/references/15-host-dispatch.md) and supply its resolved installed paths.
Before artifact work, read [artifact schema](../team/references/artifacts.md).
Before the tier sort, read [finding format](../team/references/findings.md).
Before each consuming step, read its linked shared rules from this installed skill directory.
If a required read fails, stop that step with the exact path. Never use checkout fallback or recursive loading.
Before finalizing prose you author, read the [writing standards](../team/references/writing.md). Relay completed reviewer reports unchanged.

## Core contracts

- Require `1-task.md`, a non-default branch, at least one commit beyond the merge-base, and a tree clean outside `docs/plans/`; in multi-repo mode, every worktree `4-repos.md` lists.
- Write one `review-<n>.md` per completed round; never overwrite a record.
- **Never** ask the user which Blocking or Major items to address (the no-consult rule). The loop has no count cap; it ends only when no Blocking or Major finding remains.
- At PASS, return to the `/team` phase loop in the same turn when the TodoWrite ledger holds a `PR` phase item; otherwise print the Next line for `/team-security-review`. Never load `team-security-review` or `team-pr`.

## Procedure references

Read each reference completely when reaching it, in order.

1. [Input](references/01-input.md)
2. [Execution](references/02-execution.md)

## Applied principles

Read and apply: [execution rules](../team/references/execution.md).
