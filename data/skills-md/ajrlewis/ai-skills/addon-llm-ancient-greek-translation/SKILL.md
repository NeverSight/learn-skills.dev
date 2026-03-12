---
name: addon-llm-ancient-greek-translation
description: Use when adding Koine or Attic Greek translation to Next.js content flows; pair with ui-editorial-writing-surface and addon-nostr-nip23-longform.
---

# Add-on: LLM Ancient Greek Translation

Use this skill when an app needs LLM translation to Ancient Greek before review or publish.

## Compatibility

- Works with Next.js App Router projects.
- Best with `architect-nextjs-bun-app`.
- Commonly paired with Nostr add-ons for translated publishing flows.

## Inputs

Collect:
- `GREEK_VARIANT`: `koine` | `attic`.
- `LLM_PROVIDER`: `openai` | `anthropic` | `ollama`.
- `LLM_MODEL`: provider model id.
- `REVIEW_MODE`: `dual-output` (recommended) | `translation-only`.

## Integration Workflow

1. Add dependencies:
```bash
# Use the project's package manager (examples):
bun add zod
pnpm add zod
```

2. Add files:
```text
src/lib/llm/ancient-greek.ts
src/lib/llm/prompts/ancient-greek.ts
src/app/api/translation/ancient-greek/route.ts
src/components/journal/translation-panel.tsx
```

3. Keep calls server-side:
- Use server route handlers for provider calls.
- Return typed JSON containing source text, translated text, and notes.

4. Enforce output schema:
- Variant must be one of `koine`/`attic`.
- Reject empty translation output.
- Bound source length before provider call.

## Required Template

### `src/lib/llm/ancient-greek.ts`
```typescript
import { z } from "zod";

export const AncientGreekResponseSchema = z.object({
  variant: z.enum(["koine", "attic"]),
  sourceText: z.string().min(1),
  translatedText: z.string().min(1),
  translatorNotes: z.string().optional(),
});

export type AncientGreekResponse = z.infer<typeof AncientGreekResponseSchema>;
```

## Guardrails

- Documentation contract for generated code:
  - Python: write module docstrings and docstrings for public classes, methods, and functions.
  - Next.js/TypeScript: write JSDoc for exported components, hooks, utilities, and route handlers.
  - Add concise rationale comments only for non-obvious logic, invariants, or safety constraints.
  - Apply this contract even when using template snippets below; expand templates as needed.


- API keys stay server-only (`OPENAI_API_KEY`, etc.).
- Do not auto-publish untranslated or invalid translation payloads.
- Preserve user intent and meaning; expose translation notes for user review.
- Provide explicit fallback behavior when provider is unavailable.

## Validation Checklist

- Confirm generated code includes required docstrings/JSDoc and rationale comments for non-obvious logic.


```bash
# Use the project's package manager (examples):
bun run lint
bun run build
pnpm run lint
pnpm run build
```
Fallback (`offline-smoke`):
```bash
test -f src/lib/llm/ancient-greek.ts
test -f src/app/api/translation/ancient-greek/route.ts
rg -n "koine|attic" src/lib/llm/ancient-greek.ts
```
- Manual checks:
- Translation route returns valid schema for both variants.
- UI displays source + translation clearly before publish.

## Decision Justification Rule

- Every non-trivial decision must include a concrete justification.
- Capture the alternatives considered and why they were rejected.
- State tradeoffs and residual risks for the chosen option.
- If justification is missing, treat the task as incomplete and surface it as a blocker.
