---
name: eve-orchestration
description: Orchestrate jobs via depth propagation, parallel decomposition, relations, and control signals
---

# Eve Orchestration

This skill explains how to orchestrate complex work in Eve Horizon by spawning child jobs, managing
dependencies, and maximizing parallel execution while respecting depth limits.

## Core Principles

1. Parent sets a target depth and passes it to children.
2. Each job decides its own decomposition based on scope and depth.
3. Parallelize by default when tasks can proceed independently.
4. Use relations to encode true dependencies, not preference.
5. Leaf jobs execute; parent jobs orchestrate and wait.
6. Orchestrators stay lightweight — dispatch work, don't accumulate it.

## When to Orchestrate vs Execute Directly

Not every job needs decomposition. Use this heuristic:

- **Execute directly** when the work is atomic, self-contained, and fits comfortably in a single agent's context and capability. Examples: fix a single bug, write one document section, run a diagnostic check.
- **Orchestrate** when the work has independent sub-parts that benefit from parallelism, when the scope exceeds what a single agent should hold in context at once, or when different parts require different skills or tool access.
- **Default to direct execution.** Orchestration has overhead (job creation, waiting, resumption). Only decompose when parallelism or scope genuinely demands it.

## Always Start With Context

Fetch the current job context before deciding anything:

```bash
eve job current --json
# or explicit
eve job current $EVE_JOB_ID --json
```

Use the context to confirm:
- `job.depth` (current depth)
- `children` (existing sub-jobs)
- `relations` (dependencies)
- `blocked` / `waiting` / `effective_phase`

## Environment and IDs

Use the environment to avoid guessing identifiers:

- `EVE_JOB_ID`: current job
- `EVE_PROJECT_ID`: owning project
- `EVE_ATTEMPT_ID`: current attempt
- `EVE_REPO_PATH`: workspace path
- `EVE_AGENT_ID`: agent identifier (optional)

## Depth Propagation

The parent decides the target depth and passes it to children (in the child description or data).
Each child must read and honor the same target depth.

Example snippet to include in child descriptions:

```
Target depth: 3 (EPIC). Current depth: 1.
If current depth < target, you may create child jobs and use waits_for relations to parallelize.
If current depth >= target, execute directly.
```

### Default Depth Rules

- EPIC: target depth = 3
  - Root orchestrates children
  - Children may orchestrate grandchildren
  - Grandchildren execute

- Story: target depth = 2
  - Root orchestrates children
  - Children execute

If no target depth is provided, default to Story depth (2) unless the scope clearly indicates EPIC.

## Context Management

The orchestrator's most precious resource is its context window. Protect it:

- **Do not read large files or datasets in the orchestrator.** If analysis is needed, create a child job to do the reading and summarize the results.
- **Keep the orchestrator's role to planning, dispatching, and synthesizing.** The orchestrator decides *what* to do and *how to split it*, then delegates the actual work.
- **Avoid accumulating child outputs inline.** When resuming after children complete, read only the summaries or outcomes you need to verify completion — not the full content of every child's work product.
- **Front-load decomposition thinking.** Spend context on planning the breakdown, not on doing partial work that will be redone by children.

A well-run orchestrator should finish with most of its context budget unspent.

## Per-Job Orchestration Flow

1. Fetch context (`eve job current --json`).
2. Determine depth:
   - Read inherited target depth.
   - If `current_depth >= target_depth`, execute directly.
3. Decide whether to decompose:
   - If the work is sizable or parallelizable, create child jobs.
   - Each child inherits the same target depth.
4. Write self-contained child descriptions (see template below).
5. Add relations:
   - Use `waits_for` for standard gating.
   - Use `blocks` only for strict ordering constraints.
6. Return waiting signal after relations exist.
7. Resume when children complete; read summaries, verify, and continue.

## Creating Child Jobs

Create child jobs using `eve job create` with `--parent`. Each child description must be
**fully self-contained** — the child agent has no access to the parent's conversation,
context, or reasoning. Everything the child needs to act must be in the description itself.

```bash
# Create two child jobs in parallel
eve job create --project $EVE_PROJECT_ID \
  --parent $EVE_JOB_ID \
  --description $'Target depth: 3 (EPIC). Current depth: 1.\nScope: Research sources\nDeliverable: Annotated bibliography' \
  --phase ready

eve job create --project $EVE_PROJECT_ID \
  --parent $EVE_JOB_ID \
  --description $'Target depth: 3 (EPIC). Current depth: 1.\nScope: Draft outline\nDeliverable: Structured outline' \
  --phase ready
```

After creating children, add dependencies so the parent waits on them:

```bash
eve job dep add $EVE_JOB_ID $CHILD_A_ID --type waits_for
eve job dep add $EVE_JOB_ID $CHILD_B_ID --type waits_for
```

## Parallel Decomposition Guidance

- Favor multiple small, independent children over one large child.
- If tasks can run in parallel, create them and make the parent wait on all.
- Avoid chaining children unless the output of one is a genuine input to the next.
- Every child repeats the same decision process and may create grandchildren if depth allows.
- A good decomposition reduces each child's scope to something a single agent can complete without exhausting its context window.

## Dependencies and Relations

Use the CLI dependency commands to express relationships:

```bash
eve job dep add $PARENT_JOB_ID $CHILD_JOB_ID --type waits_for
eve job dep add $CHILD_JOB_ID $OTHER_JOB_ID --type blocks
eve job dep list $JOB_ID
```

Relation guidance:
- `waits_for`: standard parent waits for child completion
- `blocks`: strict ordering constraint
- `conditional_blocks`: use only when the dependency is conditional

Add relations before returning a waiting control signal.

## Control Signals (json-result)

When you spawn children and set relations, pause the parent with a waiting signal:

```json-result
{
  "eve": {
    "status": "waiting",
    "summary": "Spawned 3 parallel child jobs; waiting on waits_for relations"
  }
}
```

Rules:
- Only return `waiting` after dependencies exist.
- `waiting` requeues the job to `ready` while it stays blocked by relations.
- Returning `waiting` without blockers triggers a short backoff; avoid it.
- Use `success` when the work is complete.
- Use `failed` only for unrecoverable outcomes.

## Review Mechanics (Optional)

Default: no review unless explicitly required by the parent or project settings.

If review is required:
- Apply at the specified level (top only, all levels, or none).
- Do not submit for review when returning `waiting`.
- Submit for review only when the job is complete.

```bash
eve job submit $EVE_JOB_ID --summary "Completed work and ready for review"
```

## Parent Review of Child Work

When a parent resumes after children complete:

- Read child summaries and outcomes — not their full work products. Protect context.
- Verify that child outputs collectively satisfy the parent's scope.
- If review is required, submit the parent for review after verification.
- If no review is required, synthesize child outcomes into a parent summary and complete.

## Failure Handling

If a child fails:
- Re-check context and determine whether to retry, replace, or stop.
- Remove or adjust relations if the plan changes.
- Do not leave the parent waiting on a permanently failed child.

## Child Job Description Template

Every child description must be self-contained. The child agent starts cold — no access to
the parent's conversation, files read, or reasoning. Include everything it needs:

```
Target depth: 3 (EPIC). Current depth: 1.
If current depth < target, you may create child jobs and use waits_for relations to parallelize.
If current depth >= target, execute directly.

Context: <why this work exists — enough background for the child to act without asking>
Scope: <concise child objective — what to do>
Inputs: <specific file paths, data references, or prior outputs the child needs>
Deliverable: <clear, verifiable outcome — what "done" looks like>
Constraints: <boundaries, standards, or requirements to honor>
```

Key rules for child descriptions:
- **Name specific files and paths.** "Update the auth module" is ambiguous; "Update `/src/auth/handler.ts` to add token refresh logic" is actionable.
- **Include relevant decisions already made.** If the parent chose an approach, tell the child — don't make it re-derive the decision.
- **State the deliverable as a verifiable condition.** "Tests pass" or "File exists at path X" beats "implement feature Y."
- **Never assume the child can read the parent's mind.** If in doubt, over-specify.

## Knowledge-Work Examples (Non-SWE)

- Research: parallel literature review, data gathering, synthesis
- Writing: outline, draft sections in parallel, consolidate
- Ops: parallel checks (metrics, logs, status), then summary
- Strategy: parallel SWOT, stakeholder analysis, risk assessment

## Quick Checklist

- [ ] Read context and depth
- [ ] Determine target depth and level
- [ ] Decide: execute directly or orchestrate? (default to direct if work is atomic)
- [ ] If orchestrating: plan the decomposition, then create children with self-contained descriptions
- [ ] Favor parallel children over sequential chains
- [ ] Add relations before signaling
- [ ] Return `json-result` waiting (if children exist)
- [ ] On resume: read child summaries (not full outputs), verify, and complete
