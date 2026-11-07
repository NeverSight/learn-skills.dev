---
name: team-security-review
description: 'Use for running the Team security review phase only on explicit request. Never infer from a plain security review request. Reviews and fixes the branch.'
effort: medium
argument-hint: "[docs/plans/<id>/]"
---

# Team Security Review

Before each dispatch or retry, read [host dispatch](../team/references/15-host-dispatch.md) and supply its resolved installed paths.
Before artifact work, read [artifact schema](../team/references/artifacts.md).
Before the tier sort, read [finding format](../team/references/findings.md).
Before each consuming step, read its linked shared rules from this installed skill directory.
If a required read fails, stop that step with the exact path. Never use checkout fallback or recursive loading.
Before finalizing prose you author, read the [writing standards](../team/references/writing.md). Relay completed reviewer reports unchanged.

## Core contracts

- Run after CODE REVIEW passes. Require the `team-code-review` entry conditions, plus a newest `review-<n>.md` that is PASS and current.
- Dispatch `security-reviewer` alone. No other phase dispatches it.
- Run the review loop that the `team-code-review` execution reference states, with the deltas in [Execution](references/02-execution.md).
- Write one `security-review-<n>.md` per completed round. Never overwrite a record.
- Seed TodoWrite with `Security review round <n>`. Retry as `Security review round <n+1> (<b> Blocking, <m> Major open)`.
- **Never** stop to ask the user which Blocking or Major items to address (the no-consult rule).
- The loop has no count cap. It ends only when no Blocking or Major finding remains.
- At PASS, when the TodoWrite ledger holds a `PR` phase item, return to the `/team` phase loop in the same turn. Otherwise, print the Next line that [Execution](references/02-execution.md) step 9 names.
- Never load `team-code-review` or `team-pr`.

## Procedure references

Read each reference completely when reaching that stage. Follow them in order.

1. [Input](references/01-input.md)
2. [Execution](references/02-execution.md)

## Applied principles

Read and apply: [execution rules](../team/references/execution.md).
