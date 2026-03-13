---
name: addon-vercel-ai-labs
description: Use when adding Vercel AI SDK and AI Labs-style generation flows to Next.js apps; pair with architect-nextjs-bun-app.
---

# Add-on: Vercel AI Labs

Use this skill when a Next.js app needs Vercel AI SDK based chat, generation, or streaming interactions with typed boundaries.

## Compatibility

- Best with `architect-nextjs-bun-app`.
- Can be combined with `addon-llm-translation`, `addon-langgraph-agent`, or `addon-langchain-llm`.
- For Python-first stacks, prefer `addon-langchain-llm` or `addon-langgraph-agent`.

## Inputs

Collect:
- `AI_PROVIDER`: `openai` | `anthropic` | `google` | `xai`.
- `AI_MODEL`: provider model id.
- `STREAM_MODE`: `yes` | `no` (default `yes`).
- `UI_SURFACE`: `chat` | `assistant` | `text-generation`.
- `MAX_INPUT_CHARS`: default `12000`.

## Integration Workflow

1. Add dependencies:
```bash
# Use the project's package manager (examples):
bun add ai zod
pnpm add ai zod
```
- Provider packages as needed:
```bash
# Use the project's package manager (examples):
bun add @ai-sdk/openai @ai-sdk/anthropic @ai-sdk/google @ai-sdk/xai
pnpm add @ai-sdk/openai @ai-sdk/anthropic @ai-sdk/google @ai-sdk/xai
```

2. Add files:
```text
src/lib/ai/providers.ts
src/lib/ai/schemas.ts
src/app/api/ai/chat/route.ts
src/components/ai/chat-panel.tsx
```

3. Keep model calls server-side:
- Route handlers own provider/model selection.
- Return typed JSON contract for non-streaming mode.
- For streaming mode, enforce bounded lifecycle and disconnect handling.

4. Enforce schema and policy:
- Validate request inputs and size before model invocation.
- Restrict model/provider to explicit allow-list.
- Add timeout/retry boundaries and fallback behavior.

## Required Template

### `src/lib/ai/schemas.ts`
```typescript
import { z } from "zod";

export const AiChatRequestSchema = z.object({
  message: z.string().min(1).max(12000),
});

export const AiChatResponseSchema = z.object({
  outputText: z.string().min(1),
  model: z.string().min(1),
  provider: z.string().min(1),
});
```

## Guardrails

- Documentation contract for generated code:
  - Python: write module docstrings and docstrings for public classes, methods, and functions.
  - Next.js/TypeScript: write JSDoc for exported components, hooks, utilities, and route handlers.
  - Add concise rationale comments only for non-obvious logic, invariants, or safety constraints.
  - Apply this contract even when using template snippets below; expand templates as needed.


- Never expose API keys to client bundles.
- Do not allow arbitrary model override from untrusted client input.
- Bound token/character budgets and request duration.
- Return controlled degraded response when provider is unavailable.

## Validation Checklist

- Confirm generated code includes required docstrings/JSDoc and rationale comments for non-obvious logic.


```bash
# Use the project's package manager (examples):
bun run lint
bun run build
pnpm run lint
pnpm run build
test -f src/app/api/ai/chat/route.ts
rg -n "AiChatRequestSchema|AiChatResponseSchema|provider|model" src/lib/ai/schemas.ts
```
- Manual checks:
- Chat route validates input and returns typed output.
- Streaming path terminates cleanly on client disconnect.

## Decision Justification Rule

- Every non-trivial decision must include a concrete justification.
- Capture the alternatives considered and why they were rejected.
- State tradeoffs and residual risks for the chosen option.
- If justification is missing, treat the task as incomplete and surface it as a blocker.
