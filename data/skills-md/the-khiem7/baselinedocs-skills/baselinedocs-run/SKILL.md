---
name: baselinedocs-run
description: Execute an initialized baseline roadmap phase by phase with durable checkpoints, optional approval gates, and explicitly authorized phase commits. Use explicitly when the user asks the agent to implement all phases or run a loop-engineering workflow from an existing pack.
---

# Baseline Docs Run

Execute the active roadmap while keeping the pack resumable after every material phase.

## Inputs

Resolve from the current request and pack:

- active pack or initiative index
- phase order and dependencies
- `approval_policy`: `phase` or `continuous`
- `commit_policy`: `none` or `per-phase`
- verification commands and release gates

Read `references/execution-contract.md` before execution.

Read `references/pack-contract.md` in full before creating or editing any pack file, every time. It is the only definition of which document owns which content; do not infer that from a filename, from an earlier session, or from memory.

Read `references/report-style.md` in full before reporting to the user, every time. It governs how a pack element is named in conversation; an identifier stated without its meaning is a question the user has to ask.

## Policy Selection Gate

Before implementation, determine whether the user's current request clearly answers both execution questions, regardless of invocation style or whether internal policy names are used.

If either answer is missing or ambiguous, stop and ask only for the unclear choice:

```text
Before I begin, how would you like me to work through this roadmap?

- Should I stop after each completed phase for your approval, or continue through every phase that is ready?
- Should I leave the changes uncommitted, or create a separate commit after each verified phase?
```

Ask in the user's language and adapt the wording to the conversation. Do not expose internal policy identifiers unless the user asks for technical details.

Apply this gate to every invocation style. `$baselinedocs-run @docpack` is only one example where both questions are unanswered. Do not silently apply defaults, infer the choices from an earlier turn, or begin implementation while waiting.

Selecting `per-phase` in the user's reply is explicit commit authorization for that run. Selecting the skill by itself is not.

## Workflow

1. Complete the policy selection gate.
2. Validate that the roadmap has executable phases, acceptance criteria, and dependency order.
3. Confirm current repository state and preserve unrelated user changes.
4. Execute the next ready phase.
5. Verify the phase in proportion to risk.
6. Checkpoint the pack before starting another phase:
   - current phase status
   - final evidence and affected files
   - open risks and exact next action
   - document frontmatter
7. If `approval_policy` is `phase`, stop for approval after the checkpoint.
8. If `commit_policy` is `per-phase`, commit only phase-related code and docs after verification. Follow the repository's existing commit message convention.
9. Continue until all authorized phases are complete or a real blocker requires the user.

## Revision Policy

Treat post-initial corrections as revisions of an existing phase when they preserve its outcome, acceptance criteria, and dependency boundary. Add a new phase only when the change introduces a distinct outcome, dependency, release gate, or independently reviewable scope.

Aggregate small revisions under a `Revision summary` entry. Do not create one phase per feedback turn.

## Safety

- Selecting this skill is not permission to commit.
- Do not commit unless the current user request explicitly authorizes it.
- A phase commit must be indistinguishable in form from the repository's own commits. Do not add authorship, attribution, or tool-generated trailers that the repository's history does not already use. A pack is operational memory, not a byline.
- Do not start implementation until every missing policy has been selected.
- Do not mark runtime, deployment, integration, or external-service behavior verified from build or formatting checks alone.
- Do not begin a dependent phase when its prerequisite is unverified.
