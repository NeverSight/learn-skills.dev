---
name: addon-langgraph-agent
description: Use when adding LangGraph stateful agent workflows in Python or Next.js stacks; pair with architect-stack-selector.
---

# Add-on: LangGraph Agent

Use this skill when a project needs multi-step agent execution (tool use, checkpoints, and bounded loops) through LangGraph.

## Compatibility

- Works with `architect-python-uv-fastapi-sqlalchemy` and `architect-nextjs-bun-app`.
- Can be combined with `addon-langchain-llm` for shared provider setup.
- Can be combined with `addon-google-agent-dev-kit` when ADK interop is needed.

## Inputs

Collect:
- `AGENT_SCOPE`: tasks the agent is explicitly allowed to perform.
- `CHECKPOINT_BACKEND`: `memory` | `postgres` | `redis`.
- `ALLOW_TOOLS`: explicit tool allow-list.
- `MAX_STEPS`: default `10`.
- `TIMEOUT_SECONDS`: default `45`.

## Integration Workflow

1. Add dependencies:
- Python:
```bash
uv add langgraph langchain-core pydantic-settings
```
- Next.js:
```bash
# Use the project's package manager (examples):
bun add @langchain/langgraph zod
pnpm add @langchain/langgraph zod
```

2. Add files by architecture:
- Python API:
```text
src/{{MODULE_NAME}}/agent/state.py
src/{{MODULE_NAME}}/agent/graph.py
src/{{MODULE_NAME}}/agent/tools.py
src/{{MODULE_NAME}}/api/routes/agent.py
```
- Next.js:
```text
src/lib/agent/state.ts
src/lib/agent/graph.ts
src/lib/agent/tools.ts
src/app/api/agent/runs/route.ts
```

3. Expose run lifecycle endpoints:
- Create run (`POST /v1/agent/runs` or app-equivalent route).
- Fetch run status (`GET /v1/agent/runs/{run_id}` or app-equivalent route).

4. Persist run telemetry:
- `run_id`, `status`, `steps`, `started_at`, `finished_at`, `error`.

## Required Template

### Agent run response shape
```json
{
  "runId": "uuid",
  "status": "queued"
}
```

## Guardrails

- Documentation contract for generated code:
  - Python: write module docstrings and docstrings for public classes, methods, and functions.
  - Next.js/TypeScript: write JSDoc for exported components, hooks, utilities, and route handlers.
  - Add concise rationale comments only for non-obvious logic, invariants, or safety constraints.
  - Apply this contract even when using template snippets below; expand templates as needed.


- Restrict tools to explicit allow-list only.
- Enforce max-step and timeout boundaries.
- Persist failure state for post-run inspection.
- Return deterministic fallback on provider/tool failure.

## Validation Checklist

- Confirm generated code includes required docstrings/JSDoc and rationale comments for non-obvious logic.


```bash
uv run ruff check . || true
uv run mypy src || true
# Use the project's package manager (examples):
bun run lint || true
pnpm run lint || true
rg -n "runId|MAX_STEPS|timeout|allow-list" src || true
```
- Manual checks:
- Run creation returns stable run id format.
- Agent aborts safely after max steps.

## Decision Justification Rule

- Every non-trivial decision must include a concrete justification.
- Capture the alternatives considered and why they were rejected.
- State tradeoffs and residual risks for the chosen option.
- If justification is missing, treat the task as incomplete and surface it as a blocker.
