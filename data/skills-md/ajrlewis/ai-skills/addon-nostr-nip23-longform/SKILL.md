---
name: addon-nostr-nip23-longform
description: Use when publishing or reading NIP-23 kind 30023 long-form events in Next.js Nostr apps; pair with addon-nostr-client-nextjs.
---

# Add-on: Nostr NIP-23 Long-Form

Use this skill when a Next.js Nostr client must publish and read long-form content as NIP-23 events (`kind: 30023`).

## Compatibility

- Requires an existing Next.js Nostr client.
- Best with `architect-nextjs-bun-app` + `addon-nostr-client-nextjs`.
- Recommended with `addon-nostr-nip-profile-selector` including NIP-23 in selected profile.

## Inputs

Collect:
- `LONGFORM_RELAYS`: comma-separated relay URLs (defaults to app relays).
- `D_TAG_MODE`: `slug` | `timestamp` (default `slug`).
- `MAX_BODY_CHARS`: default `40000`.

## Integration Workflow

1. Add/confirm dependencies:
```bash
# Use the project's package manager (examples):
bun add nostr-tools zod
pnpm add nostr-tools zod
```

2. Add files:
```text
src/lib/nostr/nip23.ts
src/lib/nostr/longform.ts
src/lib/nostr/publish-longform.ts
src/components/nostr/longform-editor.tsx
src/app/api/nostr/longform/route.ts
```

3. Implement NIP-23 event builder:
- Enforce `kind = 30023`.
- Include at minimum tags: `["d", "..."]`, `["title", "..."]`, `["published_at", "..."]`.
- Optional tags: `["summary", "..."]`, `["image", "..."]`, `["t", "..."]`.

4. Implement sign + publish flow:
- Use browser signer (NIP-07) or project signer abstraction.
- Validate payload before signing/publish.
- Send to selected relays and return per-relay status.

5. Implement read flow:
- Query `kind: 30023` with `#d` and/or author filters.
- Normalize events into typed article model.

## Required Template

### `src/lib/nostr/nip23.ts`
```typescript
export type LongFormDraft = {
  title: string;
  summary?: string;
  body: string;
  d: string;
  image?: string;
  publishedAtIso: string;
  topics?: string[];
};

export function buildNip23Tags(draft: LongFormDraft): string[][] {
  const tags: string[][] = [
    ["d", draft.d],
    ["title", draft.title],
    ["published_at", draft.publishedAtIso],
  ];
  if (draft.summary) tags.push(["summary", draft.summary]);
  if (draft.image) tags.push(["image", draft.image]);
  for (const topic of draft.topics ?? []) tags.push(["t", topic]);
  return tags;
}
```

## Guardrails

- Documentation contract for generated code:
  - Python: write module docstrings and docstrings for public classes, methods, and functions.
  - Next.js/TypeScript: write JSDoc for exported components, hooks, utilities, and route handlers.
  - Add concise rationale comments only for non-obvious logic, invariants, or safety constraints.
  - Apply this contract even when using template snippets below; expand templates as needed.


- Do not publish malformed `kind`/tag combinations.
- Enforce content bounds (`title`, `summary`, `body`) before signing.
- Keep private key handling out of API routes by default.
- Never store secrets in `NEXT_PUBLIC_*`.

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
test -f src/lib/nostr/nip23.ts
rg -n "30023" src
rg -n '\["d"' src/lib/nostr/nip23.ts
```
- Manual checks:
- Long-form publish emits `kind: 30023` with required tags.
- Reader can fetch published article from configured relays.

## Decision Justification Rule

- Every non-trivial decision must include a concrete justification.
- Capture the alternatives considered and why they were rejected.
- State tradeoffs and residual risks for the chosen option.
- If justification is missing, treat the task as incomplete and surface it as a blocker.
