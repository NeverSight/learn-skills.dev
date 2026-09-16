---
name: task-new
description: "Record a repository implementation task only when the user explicitly invokes /task-new. Use active conversation context when available; never trigger from an ordinary implementation request or proposal alone."
argument-hint: "[optional task context]"
user-invocable: true
---

# New Repository Task

Use this entry only after explicit user invocation. Never invoke it because
work appears large or long-running. Lifecycle rules belong to
`repository-task-ledger`.

## Load The Core

Load `repository-task-ledger` by name, then the repository's agent instructions
and task profile. If the core is unavailable, stop and request the complete
skill package. Do not reconstruct it, invent a substitute, or change task
state.

## Record The Candidate

1. If the user did not explicitly invoke `task-new`, stop before reading or
   changing the ledger. Ordinary requests, discussion, and agent suggestions
   are not invocations.
2. Resolve the candidate from the latest explicit direction and settled
   conversation outcome. Command text is optional and overrides older context;
   do not ask the user to restate one clear outcome.
3. Identify the owning repository, one testable outcome, important boundaries,
   and observable acceptance criteria. Invocation counts as acceptance only
   when the candidate is sufficiently specified and passes core admission.
4. Populate the task template's human review checkpoints for this specific
   outcome. Scope alignment and delivery acceptance are always required. Mark
   interface, business and data model, and architecture review as `Required`,
   `Not applicable` with a reason, or `Assess during execution` with the
   decision trigger. Name the expected reviewer or role, concrete review
   artifact, and approval gate. Do not ask for every approval during intake;
   unresolved design details belong at their planned execution checkpoint.
   Acceptance of the candidate for the backlog is not scope approval.
5. Inspect current backlog and ongoing definitions only for a plausible match.
   Ignore unrelated claims, dirty files, and surface overlap during intake. If
   a match exists, ask whether to merge context or create a distinct task; do
   not mutate either route until the user decides.
6. Apply core admission and ask only for the smallest missing decision. Keep
   rejected, duplicate, unconfirmed, and task-free requests outside the ledger.
   For admitted work, use the core template, profile, validation, and
   publication rules.

Finish by reporting whether the candidate was admitted and whether it was
merged or created. When created, include the task's canonical backlog path and
published state. Do not claim or implement the task unless the user explicitly
changes the intent to execution.