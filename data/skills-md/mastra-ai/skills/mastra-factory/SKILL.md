---
name: mastra-factory
description: "Operate and supervise Mastra Factory through `mastra api factory`. Use for Factory status or queue summaries, project and work-item inspection, metrics, health, decisions, attention, supervisor sessions, and user-authorized autonomous or interactive Factory operations on hosted, local, remote, or self-hosted servers."
license: Apache-2.0
metadata:
  author: Mastra
  version: "1.0.0"
  repository: https://github.com/mastra-ai/skills
---

# Mastra Factory Supervisor

Use `mastra api factory` as the operational control plane for Factory.

## Default behavior

For status, inspection, diagnosis, queue review, or recommendation requests:

1. Stay read-only.
2. Select the sole or explicitly named project; report choices when ambiguous.
3. Inspect project state, work items, metrics, thresholds, decisions, attention, and supervisor health/session.
4. Correlate stages, revisions, sessions, decisions, and health findings.
5. Report active/queued work, blocked or unhealthy items, running sessions, pending decisions, human attention, and one recommended next action.
6. Execute a recommendation only when the current request or a previously granted operating scope authorizes it.

## Required reference

Read [`references/factory-supervisor.md`](references/factory-supervisor.md) before running Factory commands. It is self-contained and includes target selection, output control, JSON envelopes, command discovery, the read-only workflow, mutation protocol, governance constraints, durable-session limitation, and error handling.

## Safety boundary

- Never read or reveal `.env`, bearer tokens, saved login contents, or platform/provider credentials.
- Never invent IDs, stages, revisions, request IDs, or sessions.
- Establish the user's operating scope before mutating. Authorization may cover one action or grant standing autonomy over named projects, resources, action types, or objectives.
- Within a clear delegated scope, act without asking for confirmation before every mutation. Ask only when an action is ambiguous, outside scope, or materially more destructive than the granted authority.
- Fetch current state before a write, make the smallest in-scope change, then refetch and report IDs, revisions, and final state.
- Use transitions—not metadata updates—for stage changes, with the current revision and a fresh UUID request ID.
- Never use private HTTP routes to bypass unsupported CLI operations.
- If `work-item start` lacks a supported durable user session, report the block; never substitute the supervisor session or invent a session UUID.
