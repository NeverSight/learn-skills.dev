---
name: eve-job-lifecycle
description: Create, manage, and review Eve jobs, phases, and dependencies. Use when running knowledge work in Eve or structuring job hierarchies.
---

# Eve Job Lifecycle

Use jobs as the unit of work and keep phases explicit.

## Phases

- idea -> backlog -> ready -> active -> review -> done or cancelled
- Jobs default to `ready` and can be scheduled immediately.

## Create jobs

- `eve job create --description "..."`
- Add details with `--project`, `--priority`, `--phase`, `--labels`, `--review`.
- Create sub-jobs with `eve job create --parent <job-id> --description "..."`.

## Update and complete

- `eve job update <id> --phase <phase>`
- `eve job submit <id> --summary "..."`
- `eve job approve <id>` or `eve job reject <id> --reason "..."`
- `eve job close <id> --reason "..."`
- `eve job cancel <id> --reason "..."`

## Dependencies

- `eve job dep add <job> <blocking-job>`
- Use dependencies only for true blockers.
- Inspect with `eve job dep list <id>`.

## Agent control signals

- Emit a fenced `json-result` block with `eve.status` as `waiting`, `success`, or `failed`.
- Return `waiting` only after dependencies exist.