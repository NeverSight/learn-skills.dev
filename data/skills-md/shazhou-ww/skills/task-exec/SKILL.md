---
name: task-exec
description: "Claim, resume, and complete an existing repository task, preferably from an attached canonical Task.md. Use when the user invokes /task-exec, attaches a task, or asks to execute backlog or ongoing work."
argument-hint: "[attach Task.md or optionally name a task]"
user-invocable: true
---

# Execute Repository Task

Use this entry to resolve one existing task and execute it through the
`repository-task-ledger` lifecycle.

## Load The Core

Load `repository-task-ledger` by name, then the repository's agent instructions
and task profile. If the core is unavailable, stop and request the complete
skill package. Do not reconstruct it, invent a substitute, or change task or
implementation files.

## Resolve One Task

1. Prefer exactly one attached canonical `Task.md` as a locator, not a content
   snapshot. Otherwise resolve from the supplied name or description, then the
   latest explicit conversation context.
2. Refresh the shared branch and read the latest canonical `Task.md` and
   `Progress.md` before routing status.
3. Require one unambiguous task in one owning repository. For no match,
   conflicting locators, multiple plausible matches, or ambiguous ownership,
   ask for the smallest clarification. Never create a task; route new intake
   through `task-new`.
4. Route by current status:
   - **Backlog:** validate identity and overlap, then claim and publish before
     implementation.
   - **Ongoing here:** resume from canonical task and progress state.
   - **Ongoing elsewhere:** coordinate or hand off; never take over implicitly.
   - **Archived:** report the recorded outcome and stop.

## Execute The Lifecycle

After resolving the route, follow `repository-task-ledger` and the repository
profile as the sole authority for implementation, validation, progress,
publication, acceptance, handoff, abandonment, and archival. Continue until
the task reaches its next genuine external blocker or its completed archive
state. A pending human review checkpoint is such a blocker: publish its review
artifact and current progress, request an explicit decision, and do not cross
the protected implementation or completion gate. Do not pause merely to
request permission for routine lifecycle actions that the core protocol
already authorizes.

Finish by reporting the resolved task, resulting ledger state, validation
outcome, and shared-primary-branch publication state. When blocked, preserve
the exact blocker and next action in the task progress record before reporting
it.