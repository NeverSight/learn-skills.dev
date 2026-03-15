---
name: addon-nostr-key-custody
description: Use when users need NIP-07 plus local encrypted key custody in Next.js Nostr apps; pair with addon-nostr-client-nextjs.
---

# Add-on: Nostr Key Custody

Use this skill when users must manage private keys safely for Nostr signing.

## Compatibility

- Requires an existing Next.js Nostr client.
- Best with `architect-nextjs-bun-app` + `addon-nostr-client-nextjs`.

## Inputs

Collect:
- `SIGNER_MODE`: `nip07-only` | `hybrid` | `local-encrypted` (default `hybrid`).
- `ALLOW_EXPORT`: `yes` | `no` (default `yes`).
- `KEY_DERIVATION`: `nip06` | `random` (default `random`).

## Integration Workflow

1. Add dependencies:
```bash
# Use the project's package manager (examples):
bun add nostr-tools zod
pnpm add nostr-tools zod
```

2. Add files:
```text
src/lib/nostr/signer.ts
src/lib/nostr/key-custody.ts
src/lib/nostr/webcrypto.ts
src/components/nostr/key-manager.tsx
src/app/settings/keys/page.tsx
```

3. Implement signer abstraction:
- Prefer NIP-07 signer when available.
- Fallback to local encrypted signer only when user opts in.

4. Implement local encrypted custody:
- Encrypt secret key with WebCrypto + passphrase-derived key.
- Keep ciphertext in local storage; never store plaintext key.
- Require passphrase to unlock signing session.

## Required Template

### `src/lib/nostr/signer.ts`
```typescript
export type SignerKind = "nip07" | "local-encrypted";

export interface NostrSigner {
  kind: SignerKind;
  getPublicKey(): Promise<string>;
  signEvent(event: {
    kind: number;
    created_at: number;
    tags: string[][];
    content: string;
    pubkey: string;
  }): Promise<{
    id: string;
    pubkey: string;
    created_at: number;
    kind: number;
    tags: string[][];
    content: string;
    sig: string;
  }>;
}
```

## Guardrails

- Documentation contract for generated code:
  - Python: write module docstrings and docstrings for public classes, methods, and functions.
  - Next.js/TypeScript: write JSDoc for exported components, hooks, utilities, and route handlers.
  - Add concise rationale comments only for non-obvious logic, invariants, or safety constraints.
  - Apply this contract even when using template snippets below; expand templates as needed.


- Never send private keys to server routes.
- Never place key material in `NEXT_PUBLIC_*` env vars.
- Treat local encrypted mode as convenience, not hardware-grade custody.
- Provide explicit key export/delete flows with confirmation.
- Wipe decrypted key material from memory on logout/lock.

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
test -f src/lib/nostr/signer.ts
test -f src/lib/nostr/key-custody.ts
rg -n "Never send private keys|NEXT_PUBLIC" src || true
```
- Manual checks:
- NIP-07 login works when extension exists.
- Local encrypted flow can create, lock, unlock, and delete key safely.

## Decision Justification Rule

- Every non-trivial decision must include a concrete justification.
- Capture the alternatives considered and why they were rejected.
- State tradeoffs and residual risks for the chosen option.
- If justification is missing, treat the task as incomplete and surface it as a blocker.
