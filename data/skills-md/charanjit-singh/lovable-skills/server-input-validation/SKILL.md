---
name: server-input-validation
description: >-
  Use when validating request bodies in edge functions, RPC payloads, or any
  server endpoint — Zod (or similar) on the server, never trusting the client.
  Not for client-only forms (use typed-api-hooks-forms).
---

# Server input validation

Client Zod (`typed-api-hooks-forms`) improves UX; **server validation is mandatory** for security.

## Edge function pattern

```ts
import { z } from "npm:zod@3";

const createProjectSchema = z.object({
  name: z.string().min(1).max(80),
  organization_id: z.string().uuid(),
});

let body: unknown;
try {
  body = await req.json();
} catch {
  return jsonError(400, "invalid_input", "Body must be valid JSON");
}

const parsed = createProjectSchema.safeParse(body);
if (!parsed.success) {
  return new Response(
    JSON.stringify({ error: "invalid_input", details: parsed.error.flatten() }),
    { status: 400, headers: { "Content-Type": "application/json" } },
  );
}
const { name, organization_id } = parsed.data;
```

## Auth + validation order

1. Verify JWT / webhook signature.
2. Parse and validate body with Zod.
3. Authorize (membership, RLS via user-scoped client, or explicit check).
4. Execute mutation.

## Share schemas (optional)

- `shared/schemas/project.ts` imported by Vite + edge via duplicate or npm workspace — keep shapes identical.
- Never import server secrets into shared files.

## RPC arguments

Validate inside SQL function with `raise exception` or validate in edge before `rpc()`.

## Avoid

- `const { name } = await req.json()` without schema.
- Trusting `user_id` from body — use `auth.uid()` from JWT.
- Returning stack traces to clients in production.

## Checklist

- [ ] Every edge POST/PATCH has a Zod schema
- [ ] 400 on validation failure with stable `error` code
- [ ] Authorization after validation
