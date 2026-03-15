---
name: addon-langchain-llm
description: Use when adding LangChain-based LLM routes or services in Python or Next.js stacks; pair with architect-stack-selector.
---

# Add-on: LangChain LLM

Use this skill when an existing project needs LangChain primitives for chat, retrieval, or summarization.

## Compatibility

- Works with `architect-python-uv-fastapi-sqlalchemy`, `architect-python-uv-batch`, and `architect-nextjs-bun-app`.
- Can be combined with `addon-rag-ingestion-pipeline`.
- Can be combined with `addon-langgraph-agent` when graph orchestration is required.
- Can be combined with `addon-llm-judge-evals`; when used together, declare `langchain` in `config/skill_manifest.json` so the judge runner can resolve the backend without guessing.

## Inputs

Collect:
- `LLM_PROVIDER`: `openai` | `anthropic` | `ollama`.
- `DEFAULT_MODEL`: provider model id.
- `ENABLE_STREAMING`: `yes` | `no` (default `yes`).
- `USE_RAG`: `yes` | `no`.
- `MAX_INPUT_TOKENS`: default `8000`.

## Integration Workflow

1. Add dependencies:
- Python:
```bash
uv add langchain langchain-core langchain-community pydantic-settings tiktoken
```
- Next.js:
```bash
# Use the project's package manager (examples):
bun add langchain zod
pnpm add langchain zod
```
- Provider packages (as needed):
```bash
uv add langchain-openai langchain-anthropic langchain-ollama
# Use the project's package manager (examples):
bun add @langchain/openai @langchain/anthropic @langchain/ollama
pnpm add @langchain/openai @langchain/anthropic @langchain/ollama
```

2. Add files by architecture:
- Python API:
```text
src/{{MODULE_NAME}}/llm/provider.py
src/{{MODULE_NAME}}/llm/chains.py
src/{{MODULE_NAME}}/api/routes/llm.py
```
- Next.js:
```text
src/lib/llm/langchain.ts
src/lib/llm/chains.ts
src/app/api/llm/chat/route.ts
```

3. Enforce typed request/response contracts:
- Validate input lengths before chain invocation.
- Return stable schema for streaming and non-streaming modes.

4. If `USE_RAG=yes`, compose retriever + prompt + model chain:
- Keep retrieval source metadata in outputs.
- Bound document count and token budget.

5. If `addon-llm-judge-evals` is also selected:
- emit `config/skill_manifest.json` with `addon-langchain-llm` in `addons`
- declare `"judge_backends": ["langchain"]` in `capabilities`
- allow the judge runner to reuse `DEFAULT_MODEL` when `JUDGE_MODEL` is unset

## Required Template

### Chat response shape
```json
{
  "outputText": "string",
  "model": "string",
  "provider": "string"
}
```

## Guardrails

- Documentation contract for generated code:
  - Python: write module docstrings and docstrings for public classes, methods, and functions.
  - Next.js/TypeScript: write JSDoc for exported components, hooks, utilities, and route handlers.
  - Add concise rationale comments only for non-obvious logic, invariants, or safety constraints.
  - Apply this contract even when using template snippets below; expand templates as needed.


- Enforce provider/model allow-lists.
- Add timeout and retry limits around provider calls.
- Never log secrets or raw auth headers.
- On streaming disconnect, stop upstream generation promptly.
- If judge evals are enabled, keep the judge path on the same provider abstraction instead of bypassing it with ad hoc SDK calls.

## Validation Checklist

- Confirm generated code includes required docstrings/JSDoc and rationale comments for non-obvious logic.


```bash
uv run ruff check . || true
uv run mypy src || true
# Use the project's package manager (examples):
bun run lint || true
pnpm run lint || true
rg -n "langchain|outputText|provider" src
```
- Manual checks:
- Typed chat route returns valid response.
- Invalid payloads fail with controlled validation errors.

## Decision Justification Rule

- Every non-trivial decision must include a concrete justification.
- Capture the alternatives considered and why they were rejected.
- State tradeoffs and residual risks for the chosen option.
- If justification is missing, treat the task as incomplete and surface it as a blocker.
