---
name: plan-dossier
description: "Coordinate living plans, phase execution, technical contracts, and targeted delta amendments via ZenForge MCP tracking plane with offline scratch fallback."
disable-model-invocation: true
---

# plan-dossier — Living Plan & Targeted Delta Custodian

Coordinates living software execution plans, technical contracts, and DAG task state machines. Operates natively on top of the `zenf-mcp` tracking plane (`zenf_find`, `zenf_create`, `zenf_update`, `transition_task`), falling back to local scratch storage (`.agents/scratch/plans/<slug>/`) only when the MCP server is unreachable.

---

## Operating Invariants

1. **ZenForge Native Tracking First**: The living plan, task DAG, and associated technical specifications live in the `zenf` tracking plane. If the MCP tracking plane is unavailable or offline, persist artifacts to `.agents/scratch/plans/<slug>/`.
2. **Technical Artifacts as Plan Documents**: Accompanying technical specifications, API contracts, and architectural decisions are registered as plan-scoped documents (`scope="PLAN"`, `scope_ref="<plan_slug>"`). The daemon automatically injects their briefs into `ContextPacket.linked_documents` for every task in the plan.
3. **Plan Version Governance**: Plans carry an integer `version` (starting at 1). Every re-ingest or update automatically advances the plan version (`v{version}`). Tasks and documentation reference the active plan version.
4. **Targeted Delta Amendment**: When requirements change, scope expands, or implementation drifts from the agreed plan:
   - Inspect the current state using `zenf_find` before mutating.
   - Never wipe or blindly recreate the graph.
   - Patch modified tasks via `zenf_update(type="task", items=[...])`.
   - Ingest newly added vertical slices via `zenf_create(type="task", items=[...])`.
   - Terminate obsolete tasks via `transition_task(action="CANCEL_TASK")` or `zenf_delete`.
   - Update plan technical documentation via `zenf_update(type="doc", items=[...])`.
5. **Human Alignment Gate on Ingest**: Stage the proposed plan, task breakdown, and technical documents for affirmative caller confirmation before submitting to the tracking plane.
6. **Evidence-Backed Verification**: Tasks and phases transition to terminal completion strictly when supported by concrete evidence (clean test execution with exit code 0 and git commit SHA).
7. **Drift Breaker**: Halt implementation immediately upon encountering architectural divergence. Transition the task to review via `transition_task(action="REQUEST_REVIEW")` so the caller or orchestrator can steer before applying delta amendments.

---

## Operations & Lifecycle

### 1. Ingest Living Plan (`init`)

When initializing an initiative:
1. **Define the Plan**: Name, slug, owning project, and initial version.
2. **Draft Technical Documents**: Architectural seams, API contracts, or verification specs.
3. **Draft Task DAG**: Decompose vertical slices with clear dependencies, priority, risk, target files, acceptance criteria, and verification commands.
4. **Register in ZenForge**:
   - Register plan and initial tasks atomically:
     ```json
     zenf_create(type="plan", items=[{
       "slug": "<slug>",
       "project_slug": "<project_slug>",
       "title": "<Plan Title>",
       "tasks": [...]
     }])
     ```
   - Register accompanying technical documentation:
     ```json
     zenf_create(type="doc", items=[{
       "project_slug": "<project_slug>",
       "key": "TECH_SPEC",
       "slug": "<slug>-spec",
       "type": "SPECIFICATION",
       "scope": "PLAN",
       "scope_ref": "<slug>",
       "title": "Technical Specification",
       "content": "<markdown content>"
     }])
     ```
5. *Offline Fallback*: If MCP is unreachable, write the plan dashboard to `.agents/scratch/plans/<slug>/README.md` alongside `01-contracts.md` and `02-seam-strategy.md`.

### 2. Targeted Delta Amendment (`amend`)

When the caller introduces modifications, design changes, or shifts from the original roadmap:
1. **Find Current Graph**:
   `zenf_find(type="task", filter={"plan_slug": "<slug>"})` and `zenf_find(type="plan", ids=["<slug>"])`
2. **Assess Lifecycle Status**:
   - Do NOT modify tasks already `COMPLETED`.
   - Preserve in-flight tasks (`RUNNING`, `AWAITING_MERGE`) unless the caller explicitly cancels them.
3. **Execute Targeted Delta**:
   - **Update existing tasks**: Call `zenf_update(type="task", items=[{"id": "<id>", "title": "...", "target_files": [...]}])`.
   - **Add new tasks**: Call `zenf_create(type="task", items=[{...}])` with `plan_slug` and explicit dependency references.
   - **Cancel deprecated tasks**: Call `transition_task(task_ids=["<obsolete_id>"], action="CANCEL_TASK")`.
   - **Revise Plan Specs**: Call `zenf_update(type="doc", items=[{"id": "<doc_id>", "content": "..."}])`.
   - Bumping the plan version tracks the new revision across the web cockpit and worker context packets.

### 3. Verification & Completion (`verify`)

- Execute verification commands.
- On exit code 0 and valid git commit SHA, complete the task via `transition_task(task_ids=["<task_id>"], action="COMPLETE_TASK")`.
- Once all plan tasks are verified, archive or complete the plan:
  `zenf_update(type="plan", items=[{"slug": "<slug>", "status": "COMPLETED"}])`.

---

## Canonical Output Contract

```markdown
# Plan Dossier: <Initiative Title> (`<slug>`) · <ACTIVE | COMPLETED | DRIFTED>

**Project**: `<project_slug>` | **Version**: `v<version>` | **Store**: `<ZenForge Native | Scratch Fallback>`
**Technical Docs**: `<TECH_SPEC | API_CONTRACT | none>`

## Task State Matrix

| Task ID | Title | Priority | Status | Dependencies | Target Files / Seam |
| :--- | :--- | :--- | :--- | :--- | :--- |
| <id> | <title> | <P0-P3> | <STATUS> | <deps | '-'> | <files | '-'> |

## Delta Summary
*(Include when amending an existing plan)*
- **Added**: `<N>` tasks
- **Modified**: `<N>` tasks
- **Cancelled**: `<N>` tasks
- **Preserved In-Flight**: `<task_ids>`
```

Autonomous runner micro-token:
```text
PLAN | slug: <slug> | v: <version> | status: <STATUS> | tasks: <completed>/<total>
```
