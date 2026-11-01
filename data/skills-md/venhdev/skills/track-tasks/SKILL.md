---
name: track-tasks
description: "Persist, synchronize, and update task lifecycle states to the configured issue tracker or local repository markdown store."
disable-model-invocation: true
---

# track-tasks — Task Persistence & Lifecycle Synchronization

## Operating Invariants

- **Storage Exclusivity**: Mutate task records exclusively in the configured tracker from `.agents/task-tracker.md` (Local Markdown `.agents/tasks/`, GitHub Issues, GitLab, or Linear); never touch production code.
- **State Integrity**: Maintain canonical states: `ready`, `in-progress`, `done`. Treat `blocked` as a derived state based on prerequisite tasks; a task is only `ready` when all predecessor dependencies are `done`.
- **Idempotent Synchronization**: Check existing issues/files before creating; re-read after writing to verify IDs and persistence.
- **Self-Contained Payloads**: Embed acceptance criteria, verification commands, and inline proof into task bodies so subagents execute independently without local scratch dependencies.
- **Completion Purge**: Delete `.agents/tasks/<feature-slug>/` (or close remote tickets) once all tasks reach `done` and verified.
- **Adaptive Invocation Output**: Render a persistence summary table for humans; emit a compact micro-token for autonomous runners.

## Domain Rubric

### 1. Tracker Resolution
Read `.agents/task-tracker.md`. If absent, stage local Markdown storage under `.agents/tasks/<feature-slug>/` using `<NN>-<slug>.md` naming conventions (via [references/issue-tracker-local.md](references/issue-tracker-local.md)). Honor remote tracking (`gh`, `glab`, Linear) when authenticated CLI access is confirmed. When formatting task bodies, adhere to [references/task-template.md](references/task-template.md).

### 2. State & Task Lifecycle Transitions
- `STAGED`: Tasks partitioned and ready for persistence authorization.
- `DONE`: Tasks verified persisted in tracker storage; implementation remains pending.
- `UNRESOLVED`: Tracker communication failure or missing authorization.

## Canonical Output Contract

```markdown
# Task Persistence: <Feature / Scope> · <STAGED | DONE | UNRESOLVED>

Tracker Backend: <Local Markdown | GitHub | GitLab | Linear>
Target Collection: <Path or Project Name>

| Slice ID | System Ref | Persisted Status | Blocked By | Verification Checksum |
| :--- | :--- | :--- | :--- | :--- |
| S-01 | .agents/tasks/auth/01-token.md (#102) | ready | None | <hash or pass> |
| S-02 | .agents/tasks/auth/02-refresh.md (#103) | ready (blocked) | S-01 | PENDING |

Sync Delta: <C> created, <U> updated, <D> unchanged.
*(omit if clean)* Gap: <Tracker communication failure or missing credentials.>
```

*Autonomous Micro-Token Contract*:
```text
SYNCED | tracker: <backend> | created: <C> | updated: <U> | ready: <ID>
```

### Routing

- Persistence verified and immediate implementation of eligible task authorized → (via /forge).
- Requirements conflict prevents reliable recording → (via /clarify).
- Tracker credentials missing or service unreachable → Report UNRESOLVED.

## Execution Protocol

1. Read `.agents/task-tracker.md` to identify the active persistence target.
2. Ingest Task DAG manifest from `/split-tasks` or caller.
3. Check for existing tasks to avoid duplicate tickets.
4. Write task files or call tracker APIs, embedding verification commands and parent provenance.
5. Re-read stored tasks to confirm persistence, then output Markdown table or autonomous micro-token.
