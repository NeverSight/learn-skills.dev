---
name: eve-plan-implementation
description: Execute software engineering plan documents using Eve jobs, dependencies, and review gating.
---

# Eve Plan Implementation (Jobs)

Translate a plan document into Eve jobs, parallelize work, and drive review/verification
through job phases and dependencies.

**Orchestration model**: The root epic is the *orchestrator* — it plans, delegates, and
coordinates but does not execute heavy work itself. Phase jobs are *sub-orchestrators*
that break a phase into tasks. Task jobs are *workers* — each one receives a
self-contained description and executes independently with no access to the parent's
context.

## When to Use

- A plan/spec exists and the work should be orchestrated as Eve jobs.
- The initial job says "use eve-plan-implementation to implement the plan."

## Workflow

### 1) Load context (orchestrator)

- Read the plan doc and extract phases, deliverables, and blockers.
- If present, read `AGENTS.md` for repo-specific rules.
- Fetch current job context:
  ```bash
  eve job current --json
  ```
- Stay lightweight: the orchestrator reads just enough to plan the breakdown.
  Delegate deep analysis (reading large files, exploring code) to worker jobs.

### 2) Create or confirm the root epic (orchestrator)

If the root job does not exist, create one:
```bash
eve job create \
  --project $EVE_PROJECT_ID \
  --description "Implement <plan name>" \
  --review human \
  --phase backlog
```

If a root job already exists, use it as the orchestrator. The root epic
never executes implementation work — it creates phase jobs, wires up
dependencies, and waits.

### 3) Break down into phase jobs (sub-orchestrators)

Create one child job per plan phase. Each phase job acts as a sub-orchestrator:
it breaks its scope into task jobs and coordinates them.

```bash
eve job create \
  --project $EVE_PROJECT_ID \
  --parent $EVE_JOB_ID \
  --description "Phase: <name>. Deliverable: <artifact/result>" \
  --phase ready
```

Add dependencies so the parent waits on each phase:
```bash
eve job dep add $EVE_JOB_ID $PHASE_JOB_ID --type waits_for
```

### 4) Create task jobs under each phase (workers)

Split each phase into 2-6 atomic tasks with clear deliverables.

**If a phase has only one task, execute it directly** in the phase job rather
than creating a child — avoid unnecessary orchestration overhead.

For multi-task phases, create child worker jobs. Each worker description must be
**self-contained**: the executing agent has no access to the parent's context, the
plan document, or prior conversation. Include in the description:
- The objective and deliverable
- Relevant file paths and module names
- Any constraints, conventions, or context the worker needs to succeed

```bash
eve job create \
  --project $EVE_PROJECT_ID \
  --parent $PHASE_JOB_ID \
  --description "Task: <objective>. Deliverable: <result>. Files: <paths>. Context: <anything the worker needs>" \
  --phase ready
```

Make the phase wait on its tasks:
```bash
eve job dep add $PHASE_JOB_ID $TASK_JOB_ID --type waits_for
```

### 5) Parallelize by default

- Independent tasks should have no dependencies and run in parallel.
- Use `blocks` only for true sequencing requirements.

### 6) Execute tasks and update phases

Workers pick up task jobs and execute them independently. Each worker:
1. Reads its own job description for scope and context.
2. Does the work (reads files, writes code, runs tests).
3. Reports completion.

```bash
eve job update $TASK_JOB_ID --phase active
# do the work
eve job submit $TASK_JOB_ID --summary "Completed <deliverable>"
```

If no review is required:
```bash
eve job close $TASK_JOB_ID --reason "Done"
```

### 7) Verification and review

- Add a dedicated verification job (tests, manual checks) gated after
  implementation tasks.
- Submit the phase job when all tasks are complete.
- When all phases complete, submit the root epic for review.

### 8) Orchestrator waiting signal

After an orchestrator (root or phase) creates its child jobs and wires
dependencies, it should return a waiting signal. This frees the orchestrator's
resources while children execute in parallel:

```json-result
{
  "eve": {
    "status": "waiting",
    "summary": "Spawned child jobs and added waits_for relations"
  }
}
```

## Context Management

Orchestrators should stay lightweight:
- **Read just enough** to plan the decomposition — don't analyze entire codebases.
- **Push context into child descriptions** — file paths, conventions, constraints.
- **Delegate reading and analysis** to workers. A worker that needs to understand a module should read it itself.
- **Avoid duplicating work** — if two tasks need the same context, mention the shared source in both descriptions rather than summarizing it for them.

## Minimal Mapping from Beads to Eve Jobs

- Epic -> root job (issue_type via `--type` if available).
- Phase -> child job under the epic.
- Task -> child job under the phase.
- `bd dep add` -> `eve job dep add <parent> <child> --type waits_for`
- `bd ready/blocked` -> `eve job dep list <id>` + `eve job list --phase ...`

## Optional: Git controls template

If tasks require code changes on a shared branch:

```bash
eve job create \
  --project $EVE_PROJECT_ID \
  --description "Task: <objective>" \
  --git-ref main \
  --git-ref-policy explicit \
  --git-branch feature/<name> \
  --git-create-branch if_missing \
  --git-commit required \
  --git-push on_success
```

Keep git controls consistent across tasks so all changes land in one PR.
