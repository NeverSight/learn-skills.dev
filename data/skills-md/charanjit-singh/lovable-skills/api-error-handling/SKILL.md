---
name: api-error-handling
description: >-
  Use when standardizing API and edge function errors: HTTP status codes, error
  JSON shape, logging, or mapping Supabase/Stripe errors to client responses.
  Not for UI toast copy only or form field validation messages.
---

# API error handling

## Response shape

Use a consistent JSON body:

```json
{
  "error": "forbidden",
  "message": "You do not have access to this project."
}
```

Optional `details` for validation (`api-error-handling` + `server-input-validation`).

| Code | `error` slug | When |
|------|----------------|------|
| 400 | `invalid_input` | Zod / bad params |
| 401 | `unauthorized` | Missing/invalid JWT |
| 403 | `forbidden` | Authenticated, not allowed |
| 404 | `not_found` | Resource hidden or missing |
| 409 | `conflict` | Unique violation, duplicate |
| 429 | `rate_limited` | Too many requests |
| 500 | `internal_error` | Unexpected — generic message to client |

## Edge helper

```ts
function jsonError(status: number, error: string, message: string) {
  return new Response(JSON.stringify({ error, message }), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}
```

## Supabase errors

```ts
const { error } = await supabase.from("posts").insert(row);
if (error) {
  if (error.code === "23505") return jsonError(409, "conflict", "Already exists");
  if (error.code === "42501") return jsonError(403, "forbidden", "Not allowed");
  console.error(error);
  return jsonError(500, "internal_error", "Something went wrong");
}
```

## Logging

- `console.error` with correlation id (`crypto.randomUUID()` in response header `x-request-id`).
- Never log passwords, tokens, full card data.

## Client consumption

Hooks/forms map `error` slug to toast; show `message` to users, not raw DB text.

## Avoid

- `200` with `{ success: false }` for errors.
- Leaking `error.message` from Postgres in production.
- Empty `catch {}` blocks.

## Checklist

- [ ] All edge paths return JSON errors, not HTML
- [ ] 500 messages are generic; details in logs only
