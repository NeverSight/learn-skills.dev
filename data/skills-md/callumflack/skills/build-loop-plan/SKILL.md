---
name: build-loop-plan
description: "Turn a spec or PRD into a local implementation plan with executable slices, evidence gates, and closeout rules. Use when the user wants child work kept in a local folder instead of published to an issue tracker."
---

# Build Loop Plan

Use this when a spec is ready to become local execution work in an ad hoc local folder, not a tracker.

## Inputs

Identify before writing:

- source spec path or URL;
- local work folder, defaulting to `.scratch/<slug>/`;
- target plan path, defaulting to `.scratch/<slug>/IMPLEMENTATION_PLAN.md`;
- human owner;
- tracker policy, defaulting to local-only;
- artifact convention;
- validation commands or done gates.

Ask only if a wrong assumption would create work in the wrong place.

## Rule

The plan is executable state, not a rewrite of the spec. It should tell the next agent exactly what to build, what not to claim, and how to prove each slice.

Keep child work in the local folder until the user explicitly asks to publish it. Do not hook up Linear, GitHub Issues, or another tracker by default.

## Workflow

1. Read the source spec and any repo-local routing or contribution docs.
2. Extract the real implementation constraints: real inputs, unavailable inputs, owner boundaries, user stories, validation.
3. Slice vertically. Each slice should produce a reviewable behavior or decision, not just a layer.
4. Mark each slice `AFK` when an agent can finish it without human judgment; mark it `HITL` when it needs product, design, credential, or ownership input.
5. Use true dependencies only. Prefer `Blocked by: None` unless a previous slice must literally land first.
6. Translate formal spec labels into executor language: `Real input`, `Limit`, `Fixture rule`, `Follow-up ask`.
7. Ground the draft before writing:
   - verify each `Real input` against the codebase at a named symbol; a claimed producer that does not exist is a finding, not a detail;
   - account for every user story as covered by a slice or explicitly deferred with a reason;
   - for substantial plans, run `plan-optimizer` in a fresh agent context (the author must not grade its own draft), then verify the critique's load-bearing claims before merging fixes.
8. Ask before writing if the local folder, target path, tracker policy, owner, or artifact convention is uncertain. Recommend `.scratch/<slug>/` when the repo has no obvious convention.
9. Write the plan to the target path.

## During Execution

Keep the plan current while working from it:

1. Re-read the plan before claiming a slice is done.
2. Update only progress, checked acceptance criteria, and discovered blockers.
3. Do not turn the plan into a command log.
4. If implementation drifts from the plan, name the drift and patch the plan narrowly or ask before changing scope.
5. Before handoff or commit, compare checked boxes to branch/file evidence.

## Closeout

Close out the plan only when every accepted slice has matching evidence and the user agrees it is no longer active.

Move or archive the local folder according to the host repo convention. Do not invent a new archive folder if the repo already has one.

## Template

```md
# <Spec Title> Implementation Plan

Source: `<path-or-url>` Work folder: `.scratch/<slug>/` Status: active Author: <human owner> Tracker policy: local-only

## Rules

- Child work stays in this folder until the user explicitly asks to publish it.
- Do not create tracker issues from this plan unless explicitly asked.
- One loop handles one slice.
- Stage or commit only when the workflow grants it.
- Keep this plan synchronized with verified branch evidence.

## Slices

### 01 <Title>

Type: AFK | HITL Blocked by: None | 01 User stories covered: <ids or none>

What to build: <short end-to-end behavior>

Real input:

- <exact API, file, session method, route, adapter, or repo evidence>

Limit:

- <what this slice must not fake or overclaim>

Fixture rule:

- <when fixture data is acceptable, or none>

Follow-up ask:

- <missing product/backend/design/owner decision, or none>

Acceptance criteria:

- [ ] <observable result>

Validation:

- `<command or inspection>`
```
