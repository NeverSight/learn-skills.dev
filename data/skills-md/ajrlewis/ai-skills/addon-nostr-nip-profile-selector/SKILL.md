---
name: addon-nostr-nip-profile-selector
description: Use when Nostr features must map to explicit NIP profiles by product mode; pair with addon-nostr-client-nextjs.
---

# Add-on: Nostr NIP Profile Selector

Use this skill when a Nostr project should explicitly select which NIPs it supports instead of ad hoc protocol use.

## Compatibility

- Best with `addon-nostr-client-nextjs`.
- Commonly paired with `addon-nostr-key-custody`, `addon-nostr-nip23-longform`, and `addon-nostr-nip-sync-lock`.

## Inputs

Collect:
- `PRODUCT_MODE`: `social-client` | `longform-publisher` | `dm-client` | `custom`.
- `LEGACY_COMPAT`: `yes` | `no` (default `no`).
- `NIP_OVERRIDE`: optional comma-separated explicit NIP list.

## Integration Workflow

1. Add files:
```text
src/lib/nostr/nip-profile.ts
docs/nostr/NIP_PROFILE.md
```

2. Define profile defaults (override when needed):
- `social-client`: `01,07,10,19,21,25,27,65`
- `longform-publisher`: `01,07,19,21,23,65`
- `dm-client`: `01,07,17,44,59`

3. Apply constraints:
- Exclude deprecated/legacy NIPs by default.
- Only include legacy NIPs when `LEGACY_COMPAT=yes`, and document why.

4. Wire runtime checks:
- Expose selected NIPs in a typed config object.
- Use selected NIPs to gate feature flags (DM, longform publish, reactions, etc).

## Required Template

### `src/lib/nostr/nip-profile.ts`
```typescript
export type NostrProfileMode = "social-client" | "longform-publisher" | "dm-client" | "custom";

export const NIP_PROFILES: Record<NostrProfileMode, number[]> = {
  "social-client": [1, 7, 10, 19, 21, 25, 27, 65],
  "longform-publisher": [1, 7, 19, 21, 23, 65],
  "dm-client": [1, 7, 17, 44, 59],
  custom: [],
};
```

## Guardrails

- Documentation contract for generated code:
  - Python: write module docstrings and docstrings for public classes, methods, and functions.
  - Next.js/TypeScript: write JSDoc for exported components, hooks, utilities, and route handlers.
  - Add concise rationale comments only for non-obvious logic, invariants, or safety constraints.
  - Apply this contract even when using template snippets below; expand templates as needed.


- Treat NIP selection as an explicit contract, not implicit behavior.
- Do not include NIP-04 for new builds unless explicit legacy requirement exists.
- Keep `docs/nostr/NIP_PROFILE.md` synchronized with code and review bundle.

## Validation Checklist

- Confirm generated code includes required docstrings/JSDoc and rationale comments for non-obvious logic.


```bash
test -f src/lib/nostr/nip-profile.ts
test -f docs/nostr/NIP_PROFILE.md
rg -n "NIP_PROFILES|social-client|longform-publisher|dm-client" src/lib/nostr/nip-profile.ts
```
Manual checks:
- Profile selection maps to enabled app features.
- Legacy NIP usage is explicitly documented when enabled.

## Decision Justification Rule

- Every non-trivial decision must include a concrete justification.
- Capture the alternatives considered and why they were rejected.
- State tradeoffs and residual risks for the chosen option.
- If justification is missing, treat the task as incomplete and surface it as a blocker.
