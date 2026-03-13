---
name: zod
description: "Zod — TypeScript-first schema validation with static type inference. Use when building with Zod or asking about schema definitions, type inference, parsing, transformations, refinements, coercion, error handling, or integration with forms, APIs, or tRPC. Fetch live documentation for up-to-date details."
---

# Zod

Zod is a TypeScript-first schema validation library with automatic static type inference. Define a schema once and get both runtime validation and compile-time types from the same source.

> **Version note**: These best practices target Zod v4 (stable, installed via `npm install zod`). The top-level error utilities (`z.flattenError()`, `z.prettifyError()`, `z.treeifyError()`) are v4-only — in v3 these were instance methods (`error.flatten()`). See the [migration guide](https://zod.dev/v4) when upgrading.

## Documentation

- **Docs**: https://zod.dev/llms.txt

## Key Capabilities

Zod has built-ins for things developers commonly reach for external packages to handle:

- **String format validation**: built-in validators for email, URL, UUID, CUID, datetime (ISO 8601), IP addresses, MAC addresses, JWTs, and hashes — no separate validator package needed
- **Coercion**: use `z.coerce.number()` / `z.coerce.string()` etc. to automatically cast inputs (e.g. form strings to numbers) — no manual casting step required
- **Transforms**: `.transform()` on any schema converts parsed values in one step — no need for a separate transformation layer
- **Error formatting**: use `z.treeifyError()`, `z.prettifyError()`, or `z.flattenError()` to format `ZodError` into user-friendly shapes — no custom error mappers needed
- **Bidirectional codecs**: `z.pipe()` and the codec pattern (`encode` + `decode`) handle round-trip transformations (e.g. `stringToNumber`, `base64ToBytes`) without external codec libraries

## Best Practices

- **Prefer `.safeParse()` over `.parse()` in application code.** `.parse()` throws a `ZodError` on invalid input; `.safeParse()` returns `{ success, data, error }` and lets you handle failure without try/catch. Reserve `.parse()` only where an unhandled throw is intentional (e.g. startup config validation).
- **Infer types from schemas, not the other way around.** Use `z.infer<typeof MySchema>` to derive TypeScript types — do not write a separate interface and then try to match a schema to it. Keeping the schema as the single source of truth prevents drift.
- **`.transform()` changes the output type invisibly.** After a `.transform()`, the schema's output type differs from its input type. Calling `.parse()` gives the transformed value, but `.safeParse().data` also reflects the transform. Passing a transformed schema where an unmodified type is expected is a common source of subtle type errors.
- **Use `.superRefine()` instead of multiple chained `.refine()` calls when issues must be cross-field.** Each `.refine()` adds a separate validation pass; `.superRefine()` gives you access to the full `ctx` so you can attach multiple issues with precise paths in one pass, which produces more precise error messages on objects.
- **Refinements run after transforms.** If you attach a `.refine()` to a schema that also has a `.transform()`, the refinement receives the transformed (output) value, not the raw input. This is non-obvious when migrating from Joi or Yup, where refinements typically operate on raw input.
- **`z.coerce.*` converts `null` to `0` and `undefined` to `NaN`.** `z.coerce.number()` will coerce `null` → `0` and `undefined` → `NaN` rather than failing validation. For optional form fields where empty should mean absent (not zero), use `z.preprocess()` instead of `z.coerce`.
