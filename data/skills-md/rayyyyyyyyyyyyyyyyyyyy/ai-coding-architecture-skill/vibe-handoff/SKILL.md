---
name: vibe-handoff
description: Transfer precise task state at an actual agent handoff. Use only when another agent will consume or resume the work; not for human-only reports or A2A networking.
---

# Vibe Handoff

Transfer the smallest complete state the receiving agent needs.

## Native A2A

- Preserve existing `Task.id` and `contextId`. A `Message.taskId` references that `Task.id`; surface identifier mismatches and let the native runtime assign missing identifiers.
- Use the exact native `TaskState` enum inside `TaskStatus`; do not emit fallback aliases in native objects.
- Use `Message` for instructions, clarification, approval requests, or status.
- Use `Artifact` with `Part` values for task outputs; do not put a critical result only in a transient `Message`.
- Follow the host schema. [A2A 1.0.0](https://a2a-protocol.org/v1.0.0/specification/) is the semantic reference; this skill does not implement transport, discovery, authentication, streaming, push, or Agent Cards.

Choose the matching native state; do not use `TASK_STATE_UNSPECIFIED` when the lifecycle state is known:

- `TASK_STATE_SUBMITTED`, `TASK_STATE_WORKING`;
- `TASK_STATE_INPUT_REQUIRED`, `TASK_STATE_AUTH_REQUIRED`;
- `TASK_STATE_COMPLETED`, `TASK_STATE_FAILED`, `TASK_STATE_REJECTED`, `TASK_STATE_CANCELED`.

Terminal states stay terminal. Completion requires the delegated objective and decisive outputs. Use `TASK_STATE_INPUT_REQUIRED` for missing product or task content: a choice, fact, or other required input. Use `TASK_STATE_AUTH_REQUIRED` when an operation lacks required human approval or authorization, or when authentication or credentials are missing. If the host lacks an equivalent state, keep a valid host state and describe the dependency in `TaskStatus.message`.

## Collection labels

These are handoff labels, not normative A2A fields or artifact types:

- `change`: files, commit, patch, schema, asset;
- `evidence`: observed checks and results;
- `decision`: durable boundary or constraint;
- `remaining`: unresolved or unverified work.

Map them only to host-supported artifact names, descriptions, or metadata. State each fact once and reference durable repository artifacts instead of copying them.

Never omit failed or unexecuted verification, material risk, required input, approval, or authentication, uncertainty that changes the next action, or the local/external/production evidence boundary.

Send a `Message` only when a response is required. Without native A2A, use lowercase semantic state names in this A2A-inspired fallback:

```yaml
task: <objective>
status: <submitted|working|input-required|auth-required|completed|failed|rejected|canceled>
artifacts:
  - <label>: <path, result, or exact fact>
message: <only when a response is required>
```

The fallback is not an A2A payload and makes no interoperability claim.
