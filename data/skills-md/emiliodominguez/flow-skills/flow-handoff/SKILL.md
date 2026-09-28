---
name: flow-handoff
description: "Resumable handoff record for another session. Use when pausing or ending a session mid-task, or saving an interrupted plan or run. Routes to `flow-orchestrate`, `flow-work` or the named specialist."
metadata:
  stage: plan
---

# Handoff

Give a fresh agent a reliable starting point: current intent, evidence and unresolved work,
not a retelling of the conversation.

## Process

1. Identify the user's latest goal and steering, branch/revision, local changes, live plan and
   any orchestration run. Do not replace the goal with the last status question.
2. Write to the user's location or `.handoffs/<date>-<topic>.md`, preserving ignore policy.
   A Git-ignored file stays on this machine; share it or use an agreed tracked location when
   the next session runs elsewhere. A path alone does not transfer a file.
3. Record decisions with rationale, source paths, accepted and pending work, dead-ends,
   missing prerequisites and the exact next action. Reference plan and run records instead of
   duplicating them.
4. Include the verification revision and evidence location, not a list of green commands. For
   orchestration, keep worker/verifier identities, rejected attempts, budget consumed, stale
   acceptance and in-flight actions. The next session must not reset limits.
5. Name the resume command and first inspection: compare current source with recorded inputs,
   reconcile in-flight operations, and inspect unknown postconditions before replaying
   non-idempotent actions.

## Handoff record

```markdown
# Handoff - <goal>
Status: in-progress | blocked | review-pending | complete
Repository: <branch, commit, relevant staged/unstaged/untracked changes>
Current intent: <goal, non-goals, latest user constraints>
Plan/run: <paths, revision, direct or orchestrated>
Accepted work: <tasks, verifier/evidence, revision>
Pending/rejected work: <task, reason, next action>
In-flight actions: <identity, known outcome, how to inspect>
Budget: <attempts/time consumed, remaining limits>
Decisions and dead-ends: <why, not transcript>
Required access: <capability names, no credentials>
Resume: <skill + artifact path + first check>
Artifact availability: <local-only or shared location>
```

Skip fields that do not apply, but never omit an unresolved dependency or unknown external
outcome. The live plan carries the checklist; the handoff carries the context to trust it in the
next session.

## Anti-patterns

- Calling an ignored directory durable across machines because it sits inside a repo.
- Resuming at the next unchecked task while its dependency evidence is stale.
- Dumping the transcript or copying credentials.
- Using a new session to reset a failed correction loop.

## Done when

- The file exists and its actual availability is stated.
- The next session can recover intent, accepted evidence, remaining work and blockers.
- The first resume action checks state before further changes.

Resume an existing run with `flow-orchestrate`, a direct plan with `flow-work`, or the documented
specialist for diagnosis, research or review.
