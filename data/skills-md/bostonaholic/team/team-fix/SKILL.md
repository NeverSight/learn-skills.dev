---
name: team-fix
description: 'Use for the full bug-fix pipeline only on explicit request. Never infer from an ordinary bug fix. Runs the compressed pipeline.'
effort: high
argument-hint: "<ticket id, issue URL, or bug description>"
---

# Team Fix — Bug Fix Pipeline

Before each consuming step, read its linked shared rules from this installed skill directory.
If a required read fails, stop that step with the exact path. Never use checkout fallback or recursive loading.

Invocation follows [human control rules](../team/principles/human-control.md): fire only on stated pipeline intent; a plain "fix this bug" asks for an inline fix.

## Core contracts

- Run `WORKTREE → REPRODUCE → RED → GREEN → VERIFY → SHIP` in order.
- For a ticket, read [tracking rules](../team-pr/references/tracking.md); move it to in-progress before work, and to in-review only after its draft PR becomes ready.
- After Worktree, run each step in its own fresh subagent per Execution's `## Step dispatch`; keep gates, aborts, and ticket moves inline.

## Procedure references

Read each reference completely when reaching it, in order; later stages depend on earlier state and gates.

1. [Input](references/01-input.md)
2. [When to Use](references/02-when-to-use.md)
3. [Pipeline](references/03-pipeline.md)
4. [Setup](references/04-setup.md)
5. [Worktree](references/05-worktree.md)
6. [Execution](references/06-execution.md)
7. [Ship](references/07-ship.md)
8. [Aborting](references/08-aborting.md)

## Applied principles

Read and apply: [bug fix rules](playbooks/bug-fix.md) and [execution rules](../team/references/execution.md).
