---
name: zenf-mcp
description: "Unified 6-tool MCP tracking plane for ZenForge: zenf_find, zenf_create, zenf_update, zenf_delete, claim_task, transition_task."
---

# zenf-mcp — ZenForge Unified Tracking Plane

ZenForge is a SQLite WAL tracking plane for autonomous software engineering.
Work is coordinated through **6 canonical MCP tools**:

| Tool | Purpose | Key Parameters |
|---|---|---|
| `zenf_find` | Read, FTS, ID/URI lookup, relational filter | `uri`, `type`, `ids`, `filter`, `query`, `limit`, `include_packet` |
| `zenf_create` | Polymorphic batch creation | `type` ("project"|"plan"|"task"|"doc"|"agent"), `items` (plans carry `version: 1`, bump on update) |
| `zenf_update` | Polymorphic batch patch & notes | `type`, `items` (each with `id`/`slug` + patch fields; updates bump plan `version`) |
| `zenf_delete` | Polymorphic batch deletion/cancellation | `type`, `ids` |
| `claim_task` | Atomic preflight claim & ContextPacket | `task_id`, `worker_id`, `orchestrator_id`, `worker_role` (auto-links plan docs with query guide) |
| `transition_task` | State machine transitions & review gate | `task_ids`, `action`, `context`, `items` |

## Universal Resource Identifiers (`zenf://`)

All ZenForge entities (docs, tasks, plans, projects) expose a canonical URI scheme:
- **Documents**: `zenf://<project>/doc/<key_or_slug>` (e.g. `zenf://zenforge/doc/CONSTRUCTION_RULES` or `zenf://global/doc/RULES`)
- **Tasks**: `zenf://<project>/task/<task_id>` (e.g. `zenf://zenforge/task/task-01`)
- **Plans**: `zenf://<project>/plan/<plan_slug>` (e.g. `zenf://zenforge/plan/v0.4.1`)
- **Direct by UUID**: `zenf://doc/<uuid>`

### Resolving `zenf://` URIs
Whenever a prompt or user message references a `zenf://` URI:
```json
{
  "uri": "zenf://zenforge/doc/CONSTRUCTION_RULES"
}
```
Or pass directly in `ids`: `{"ids": ["zenf://zenforge/doc/CONSTRUCTION_RULES"]}`. `zenf_find` automatically resolves the project, entity type, and identifier.

## Task State Machine

```text
PENDING ──deps done──▶ READY ──claim_task──▶ RUNNING ──CHECKPOINT_PHASE──▶ RUNNING
                                        │        ├──COMPLETE_TASK──▶ COMPLETED
                                        │        └──COMPLETE_TASK (worktree)──▶ AWAITING_MERGE ──MERGED──▶ COMPLETED
                                        │                                       └──CONFLICT──▶ CONFLICT ──MERGED──▶ COMPLETED
                                        ├──FAIL_TASK──▶ FAILED (blocks downstream)
                                        ├──REQUEST_REVIEW──▶ AWAITING_REVIEW ──RESOLVE_REVIEW──▶ READY
                                        ├──RESET_TO_READY──▶ READY | BLOCKED
                                        └──CANCEL_TASK──▶ CANCELLED
```

## Action Verbs (`transition_task`)
- `COMPLETE_TASK`: Checks worktree. If worktree -> `AWAITING_MERGE`; else -> `COMPLETED`. Unblocks downstream dependents.
- `FAIL_TASK`: Transitions to `FAILED`. Cascades `BLOCKED` to downstream dependencies.
- `CHECKPOINT_PHASE`: Advances intra-task phase (`context.phase_id`, `context.phase_status`) and appends milestone note without losing claim.
- `REQUEST_REVIEW`: Worker requests human/architect review with `context.reason`, `context.details`, and `context.options`. Task moves to `AWAITING_REVIEW`.
- `RESOLVE_REVIEW`: Relays developer decision via `context.decision`, records guidance in notes, and resets task to `READY`.
- `RESET_TO_READY`: Evicts worker claim and returns task to `READY` (or `BLOCKED` if prerequisites changed).
- `CANCEL_TASK`: Terminal cancellation.

## Templates & Payloads
See [templates.md](references/templates.md) for complete copy-paste JSON structures.
