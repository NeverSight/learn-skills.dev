---
name: addon-llm-translation
description: Use when adding review-first LLM translation flows across Next.js or Python APIs; pair with architect-stack-selector.
---

# Add-on: LLM Translation

Use this skill when an app needs LLM translation endpoints or batch translation jobs with explicit user review before publish.

## Compatibility

- Works with `architect-nextjs-bun-app`, `architect-python-uv-fastapi-sqlalchemy`, and `architect-python-uv-batch`.
- Can be combined with `addon-langchain-llm` for provider abstraction.
- Can be combined with `addon-langgraph-agent` for multi-step translation workflows.

## Inputs

Collect:
- `SOURCE_LANGUAGE`: IETF language tag (for example `en`, `es`, `fr`).
- `TARGET_LANGUAGE`: IETF language tag.
- `LLM_PROVIDER`: `openai` | `anthropic` | `ollama`.
- `LLM_MODEL`: provider model id.
- `REVIEW_MODE`: `dual-output` (recommended) | `translation-only`.
- `MAX_SOURCE_CHARS`: default `12000`.

## Integration Workflow

1. Add dependencies:
- Next.js:
```bash
# Use the project's package manager (examples):
bun add zod
pnpm add zod
```
- Python:
```bash
uv add pydantic pydantic-settings
```

2. Add files by architecture:
- Next.js:
```text
src/lib/llm/translation.ts
src/app/api/translation/route.ts
```
- Python API:
```text
src/{{MODULE_NAME}}/schemas/translation.py
src/{{MODULE_NAME}}/services/translation.py
src/{{MODULE_NAME}}/api/routes/translation.py
```
- Python batch:
```text
src/{{MODULE_NAME}}/translation/jobs.py
src/{{MODULE_NAME}}/translation/schemas.py
```

3. Keep provider calls server-side:
- Never call provider APIs directly from browser clients.
- Return typed payloads with source text, translated text, and review metadata.

4. Enforce output schema and fallbacks:
- Validate `SOURCE_LANGUAGE`/`TARGET_LANGUAGE`.
- Reject empty translation output.
- Add provider timeout/retry boundaries and explicit degraded behavior.

## Required Templates

### Translation response shape
```json
{
  "sourceLanguage": "en",
  "targetLanguage": "es",
  "sourceText": "Hello world",
  "translatedText": "Hola mundo",
  "translatorNotes": "Preserved idiom intent."
}
```

## Guardrails

- Documentation contract for generated code:
  - Python: write module docstrings and docstrings for public classes, methods, and functions.
  - Next.js/TypeScript: write JSDoc for exported components, hooks, utilities, and route handlers.
  - Add concise rationale comments only for non-obvious logic, invariants, or safety constraints.
  - Apply this contract even when using template snippets below; expand templates as needed.


- Keep API keys server-only.
- Preserve user intent; do not silently rewrite meaning for fluency.
- Do not auto-publish untranslated or invalid outputs.
- Emit explicit review state for publish pipelines.

## Validation Checklist

- Confirm generated code includes required docstrings/JSDoc and rationale comments for non-obvious logic.


```bash
test -f src/lib/llm/translation.ts || true
test -f src/{{MODULE_NAME}}/api/routes/translation.py || true
rg -n "sourceLanguage|targetLanguage|translatedText" src || true
```
- Manual checks:
- Translation response validates with expected schema.
- Timeout/failure path returns controlled fallback response.

## Decision Justification Rule

- Every non-trivial decision must include a concrete justification.
- Capture the alternatives considered and why they were rejected.
- State tradeoffs and residual risks for the chosen option.
- If justification is missing, treat the task as incomplete and surface it as a blocker.
