---
name: addon-nostr-client-nextjs
description: Use when adding Nostr relay subscribe or publish flows to Next.js; pair with addon-nostr-nip-profile-selector.
---

# Add-on: Nostr Client for Next.js

Use this skill when an existing Next.js app needs to read/write Nostr events as a client.

## Compatibility

- Requires an existing Next.js App Router project.
- Best paired with `architect-nextjs-bun-app`.
- Recommended with `addon-nostr-nip-profile-selector`.

## Inputs

Collect:
- `RELAYS`: comma-separated relay URLs.
- `DEFAULT_KIND`: default event kind (usually `1` for notes).
- `USE_NIP07`: `yes`/`no` (default `yes` for browser signer extensions).
- `NIP_PROFILE_MODE`: `social-client` | `longform-publisher` | `dm-client` | `custom`.

## Integration Workflow

1. Add dependencies:
```bash
# Use the project's package manager (examples):
bun add nostr-tools zod
pnpm add nostr-tools zod
```

2. Add modules:
```text
src/lib/nostr/client.ts
src/lib/nostr/relays.ts
src/lib/nostr/filters.ts
src/lib/nostr/signing.ts
src/components/nostr/login-publish.tsx
src/types/nostr.d.ts
src/app/api/nostr/publish/route.ts
```

3. Add env config:
- `NEXT_PUBLIC_NOSTR_RELAYS=wss://relay.damus.io,wss://nos.lol`
4. If NIP profile selector is present:
- wire selected profile into feature gating and document supported NIPs in `docs/nostr/NIP_PROFILE.md`.

5. Implement read path:
- Create relay pool/client.
- Subscribe by filters (`kinds`, `authors`, `since`, `limit`).
- Normalize and dedupe events by `id`.

6. Implement publish path:
- Prefer NIP-07 signer in browser.
- For server-side publish route, require explicit auth and rate limiting.
- UI must require login before enabling publish.
- Wire `src/components/nostr/login-publish.tsx` into `src/app/page.tsx` (or equivalent route entry).

## Required Defaults

### `src/lib/nostr/relays.ts`
```typescript
export function parseRelays(envValue: string | undefined): string[] {
  if (!envValue) return ["wss://relay.damus.io", "wss://nos.lol"];
  return envValue
    .split(",")
    .map((s) => s.trim())
    .filter(Boolean);
}
```

### `src/lib/nostr/filters.ts`
```typescript
import type { Filter } from "nostr-tools";

export function makeNoteFilter(limit = 50): Filter {
  return {
    kinds: [1],
    limit,
  };
}
```

### `src/lib/nostr/signing.ts`
```typescript
export async function ensureNip07Available(): Promise<void> {
  if (typeof window === "undefined") {
    throw new Error("NIP-07 signer is only available in the browser");
  }
  if (!("nostr" in window)) {
    throw new Error("NIP-07 extension not found");
  }
}
```

### `src/lib/nostr/client.ts`
```typescript
import { ensureNip07Available } from "@/lib/nostr/signing";

export async function loginWithNip07(): Promise<string> {
  await ensureNip07Available();
  return window.nostr.getPublicKey();
}

export async function signNote(content: string): Promise<{
  id: string;
  pubkey: string;
  created_at: number;
  kind: number;
  tags: string[][];
  content: string;
  sig: string;
}> {
  await ensureNip07Available();
  const pubkey = await window.nostr.getPublicKey();
  return window.nostr.signEvent({
    kind: 1,
    created_at: Math.floor(Date.now() / 1000),
    tags: [],
    content,
    pubkey,
  });
}
```

### `src/components/nostr/login-publish.tsx`
```typescript
"use client";

import { useState } from "react";
import { loginWithNip07, signNote } from "@/lib/nostr/client";

export default function LoginPublish() {
  const [pubkey, setPubkey] = useState("");
  const [content, setContent] = useState("");

  async function onLogin() {
    setPubkey(await loginWithNip07());
  }

  async function onPublish() {
    if (!content.trim() || !pubkey) return;
    await signNote(content.trim());
    setContent("");
  }

  return (
    <section>
      <button onClick={onLogin} type="button">
        {pubkey ? "Re-authenticate" : "Login with NIP-07"}
      </button>
      <textarea
        disabled={!pubkey}
        onChange={(e) => setContent(e.target.value)}
        value={content}
      />
      <button disabled={!pubkey || !content.trim()} onClick={onPublish} type="button">
        Publish
      </button>
    </section>
  );
}
```

### `src/types/nostr.d.ts`
```typescript
export {};

declare global {
  interface Window {
    nostr: {
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
    };
  }
}
```

### `src/app/api/nostr/publish/route.ts`
```typescript
import { NextResponse } from "next/server";
import { z } from "zod";

const PublishSchema = z.object({
  event: z.object({
    id: z.string(),
    pubkey: z.string(),
    created_at: z.number(),
    kind: z.number(),
    tags: z.array(z.array(z.string())),
    content: z.string(),
    sig: z.string(),
  }),
  relays: z.array(z.string().url()).min(1),
});

export async function POST(req: Request) {
  const token = process.env.NOSTR_PUBLISH_TOKEN;
  if (token && req.headers.get("x-publish-token") !== token) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }
  const payload = await req.json().catch(() => null);
  const parsed = PublishSchema.safeParse(payload);
  if (!parsed.success) {
    return NextResponse.json({ error: "Invalid payload" }, { status: 400 });
  }
  return NextResponse.json({ accepted: false }, { status: 501 });
}
```

## Guardrails

- Documentation contract for generated code:
  - Python: write module docstrings and docstrings for public classes, methods, and functions.
  - Next.js/TypeScript: write JSDoc for exported components, hooks, utilities, and route handlers.
  - Add concise rationale comments only for non-obvious logic, invariants, or safety constraints.
  - Apply this contract even when using template snippets below; expand templates as needed.


- Never store private keys in `NEXT_PUBLIC_*` vars.
- Keep signing in browser when possible (`window.nostr` / NIP-07).
- Use timeout/retry boundaries for relay connections.
- Validate event payloads with `zod` before publish.
- Sanitize and bound user-controlled filters to prevent abuse.

## Validation Checklist

- Confirm generated code includes required docstrings/JSDoc and rationale comments for non-obvious logic.


```bash
# Use the project's package manager (examples):
bun run lint
bun run build
pnpm run lint
pnpm run build
```
- Manual checks:
- Relay subscription returns events.
- Publish flow works with NIP-07 extension.
- UI gracefully handles relay disconnects/timeouts.
- Publish button stays disabled until login succeeds.

## Decision Justification Rule

- Every non-trivial decision must include a concrete justification.
- Capture the alternatives considered and why they were rejected.
- State tradeoffs and residual risks for the chosen option.
- If justification is missing, treat the task as incomplete and surface it as a blocker.
