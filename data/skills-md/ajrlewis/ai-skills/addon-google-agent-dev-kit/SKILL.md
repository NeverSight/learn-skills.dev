---
name: addon-google-agent-dev-kit
description: Use when implementing Google Agent Development Kit (ADK) agents in Python or Next.js stacks; pair with architect-stack-selector.
---

# Add-on: Google Agent Development Kit

Use this skill when a project needs Google Agent Development Kit based agent workflows and runtime contracts.

## Compatibility

- Works with `architect-python-uv-fastapi-sqlalchemy` and `architect-nextjs-bun-app`.
- Can be combined with `addon-langgraph-agent` when graph-based execution is also required.
- Prefer Python-first implementation when both runtime options are viable.
- Can be combined with `addon-llm-judge-evals`; when used together, declare `google-adk` in `config/skill_manifest.json` so the judge runner can resolve the backend deterministically.

## Inputs

Collect:
- `ADK_RUNTIME`: `python` | `nextjs` (default from selected architecture).
- `ADK_DEFAULT_MODEL`: default model id for ADK-backed runs.
- `AGENT_GOAL`: one-sentence scope statement.
- `ALLOW_TOOLS`: explicit list of allowed tools.
- `MAX_AGENT_STEPS`: default `10`.
- `TIMEOUT_SECONDS`: default `60`.

## Integration Workflow

1. Add dependencies by runtime:
- Python:
```bash
uv add google-adk pydantic-settings
```
- Next.js:
```bash
# Use the project's package manager (examples):
bun add @google/adk zod
pnpm add @google/adk zod
```

2. Add files by runtime:
- Python:
```text
src/{{MODULE_NAME}}/agent/adk_runtime.py
src/{{MODULE_NAME}}/agent/tools.py
src/{{MODULE_NAME}}/api/routes/agent.py
```
- Next.js:
```text
src/lib/agent/adk-runtime.ts
src/lib/agent/tools.ts
src/app/api/agent/runs/route.ts
```

3. Enforce agent policy boundaries:
- Allow only explicitly approved tools.
- Add bounded step count and timeout.
- Emit run telemetry and decision traces.

4. Add fallback mode:
- If ADK provider/runtime is unavailable, return explicit degraded status and retry guidance.

5. If `addon-llm-judge-evals` is also selected:
- emit `config/skill_manifest.json` with `addon-google-agent-dev-kit` in `addons`
- declare `"judge_backends": ["google-adk"]` in `capabilities`
- allow the judge runner to reuse `ADK_DEFAULT_MODEL` when `JUDGE_MODEL` is unset

## Required Template

### Agent run status shape
```json
{
  "runId": "uuid",
  "status": "queued|running|completed|failed|degraded",
  "steps": 0
}
```

## Guardrails

- Documentation contract for generated code:
  - Python: write module docstrings and docstrings for public classes, methods, and functions.
  - Next.js/TypeScript: write JSDoc for exported components, hooks, utilities, and route handlers.
  - Add concise rationale comments only for non-obvious logic, invariants, or safety constraints.
  - Apply this contract even when using template snippets below; expand templates as needed.


- Keep API credentials server-only.
- Do not expose unrestricted tool execution from public routes.
- Preserve auditability of agent decisions and failures.
- Keep degraded behavior explicit and non-silent.
- If judge evals are enabled, do not silently mix ADK and non-ADK judge implementations; require explicit backend selection when multiple judge-capable addons are present.

## Validation Checklist

- Confirm generated code includes required docstrings/JSDoc and rationale comments for non-obvious logic.


```bash
uv run ruff check . || true
uv run mypy src || true
# Use the project's package manager (examples):
bun run lint || true
pnpm run lint || true
rg -n "degraded|ALLOW_TOOLS|MAX_AGENT_STEPS|status" src || true
```
- Manual checks:
- Agent run endpoint returns bounded status contract.
- Disallowed tool invocation fails with controlled error.

## Decision Justification Rule

- Every non-trivial decision must include a concrete justification.
- Capture the alternatives considered and why they were rejected.
- State tradeoffs and residual risks for the chosen option.
- If justification is missing, treat the task as incomplete and surface it as a blocker.
