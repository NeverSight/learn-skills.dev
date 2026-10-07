---
name: monomind-handoff
description: "Package the current work into a concise continuation brief for another agent, session, or human. Use when the user asks for a handoff, context will be reset, work spans sessions, or an unfinished task needs a precise next executable step."
---

# Monomind Handoff

Transfer durable state, not a transcript. Reference authoritative artifacts instead of copying them into a second source of truth.

## Reconstruct current state

Inspect the repository and available task state before writing. Do not rely only on conversational memory. Verify the working tree, current branch or revision, changed files, tests actually run, active task/spec, and unresolved external state. When `.monomind/workflow.md` exists, follow its authoritative context, decision-record, task, handoff, update-trigger, and freshness-owner fields; surface any unresolved continuity policy instead of inventing a destination. Repository context records live in [project-context](https://github.com/monomind-ai-lab/project-context) with the org-level hub in [project-hub](https://github.com/monomind-ai-lab/project-hub).

## Write the continuation brief

Use this structure in the requested destination; otherwise return it in the conversation:

```markdown
# Handoff: <objective>

## Outcome and scope
The desired result and explicit non-goals.

## Current state
What is complete, in progress, not started, and the exact repository state.

## Decisions
Only decisions not already authoritative elsewhere, with rationale or a pointer.

## Evidence
Commands run, pass/fail results, runtime artifacts, and what remains unverified.

## Next executable step
One concrete action the next owner can begin immediately, plus its completion condition.

## Blockers and risks
Required user decisions, external dependencies, unsafe assumptions, and likely failure points.

## Pointers
Specs, tasks, ADRs, diffs, files, issues, and artifacts needed to continue.
```

Do not duplicate specs, task bodies, decisions, or long command output that already has a stable path or URL. Name the relevant section and point to it. Include transient local details only when they are necessary to resume safely.

Update the repository's authoritative task or context record (see [project-context](https://github.com/monomind-ai-lab/project-context) and [project-hub](https://github.com/monomind-ai-lab/project-hub)) before compaction,
session transfer, a long pause, or handoff when project policy requires it. A
resuming owner must recheck repository and external state; a handoff is a
revision-bound starting point, not proof that the world has remained unchanged.

Redact tokens, credentials, personal data, private endpoints, and host-specific paths that do not belong in a shared artifact. Distinguish facts verified in the repository from inferences and user-reported state.

If writing a file, use the project's established handoff location or a user-specified path. Do not create external issues, messages, or shared documents unless the user requested that destination.

## Completion criteria

- The next owner can identify the objective, exact current state, and first executable step without rereading the transcript.
- Every verification claim names the command or artifact and its actual result.
- Pointers resolve and no authoritative content is unnecessarily duplicated.
- Blockers, unverified assumptions, and residual risks are explicit.
- The brief contains no secret or irrelevant host-specific state.
