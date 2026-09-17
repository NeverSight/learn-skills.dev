---
name: dispatching-parallel-agents
description: Use when permitted delegation can accelerate independent, substantial tasks without conflicting edits or shared mutable state.
---

# Delegate Independent Work

Use parallel agents when independent work is substantial enough to justify the
context and coordination cost. Two files do not automatically mean two tasks.
Keep short, tightly coupled work local.

Before dispatch, identify each task's scope, acceptance criteria, dependencies,
and owned files or read-only boundary. Give each agent enough context to work
without inheriting unrelated conversation. Follow the actual host tool schema;
do not invent tool names or capabilities.

Do not ask multiple agents to edit the same state concurrently. Shared-checkout
agents must not switch branches, reset files, or commit others' work. Use separate
workspaces if independent implementation needs isolation. Delegation does not
expand authorization; production mutations and external writes remain bounded by
the user's request.

While agents work, do useful local work. When idle, use the host's completion/wait
mechanism rather than busy polling. Avoid duplicate investigation without a
specific reason.

On return, inspect the changes and evidence, resolve conflicts, and verify the
integrated result. Report gaps honestly. The controller remains responsible for
the result; an agent's completion message is not sufficient proof.
