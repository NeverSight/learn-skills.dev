---
name: zod
description: "Define and use Zod schemas for TypeScript-first validation: primitives, objects, arrays, unions, refinements, transform, z.infer, parse, safeParse. Use when validating input, parsing API data, form validation with react-hook-form, or when the user mentions Zod, schema validation, or z.infer."
---

# Zod

## Overview

Zod is a **TypeScript-first schema validation library** with **static type inference**. Define a schema once; you get both runtime validation and a TypeScript type (via `z.infer`). Zero external dependencies; works in Node and browsers. Ideal for forms (e.g. with react-hook-form), API parsing, env vars, and any untrusted input.

**Requirements**: TypeScript 5.5+ recommended; enable **`strict`** in `tsconfig.json`.

**Install**: `npm install zod`

---

## Quick start

```ts
import { z } from "zod";

const User = z.object({
  name: z.string(),
  age: z.number().optional(),
});

type User = z.infer<typeof User>;
// { name: string; age?: number }

const data = User.parse(input); // throws ZodError if invalid
const result = User.safeParse(input); // { success: true, data } | { success: false, error }
```

---

## Primitives and common types

| Schema | Type | Notes |
|--------|------|--------|
| `z.string()` | string | |
| `z.number()` | number | |
| `z.boolean()` | boolean | |
| `z.bigint()` | bigint | |
| `z.date()` | Date | |
| `z.undefined()` | undefined | |
| `z.null()` | null | |
| `z.void()` | void | |
| `z.any()` | any | |
| `z.unknown()` | unknown | |
| `z.never()` | never | |
| `z.literal("x")` | literal | |
| `z.enum(["a", "b"])` | union of literals | |
| `z.string().email()` | string | email format |
| `z.string().url()` | string | URL |
| `z.string().uuid()` | string | UUID |
| `z.string().datetime()` | string | ISO datetime |
| `z.number().int()` | number | integer |
| `z.number().min(n).max(m)` | number | range |
| `z.boolean()` / `z.string().transform(...)` | stringbool | "true"/"false" coercion |

Optional: `.optional()` → `T | undefined`. Nullable: `.nullable()` → `T | null`. Nullish: `.nullish()` → `T | null | undefined`. Default: `.default(value)`.

---

## Objects

```ts
const Schema = z.object({
  name: z.string(),
  age: z.number().optional(),
  tags: z.array(z.string()).default([]),
});

type Schema = z.infer<typeof Schema>;
```

- **.shape**: `Schema.shape.name` (access field schema).
- **.keyof()**: `Schema.keyof()` → enum of keys.
- **.extend({ ... })**: Add or override keys.
- **.pick({ name })** / **.omit({ age })**: Subset of keys.
- **.partial()** / **.required({ name })**: Optionalize or require.
- **.strict()**: No extra keys (default in z.object). **z.strictObject** / **z.looseObject** for behavior variants.
- **.catchall(z.string())**: Allow extra keys with a schema.
- **Nested**: `z.object({ user: z.object({ name: z.string() }) })`.
- **Recursive**: `z.lazy(() => Category)` for self-referential structures.

---

## Arrays and tuples

- **Arrays**: `z.array(z.string())`, `z.string().array()`.
- **Tuples**: `z.tuple([z.string(), z.number()])` — fixed length and types.
- **Non-empty**: `.min(1)` or dedicated helpers if available.

---

## Unions and intersections

- **Union**: `z.union([z.string(), z.number()])` or `z.string().or(z.number())`.
- **Discriminated union**: Use a common key (e.g. `type: "a"`) and `z.discriminatedUnion("type", [z.object({ type: z.literal("a"), ... }), ...])`.
- **Intersection**: `z.intersection(A, B)` or `A.and(B)`.

---

## Refinements and transform

- **.refine(fn, message?)**: Custom validation; keep type unchanged.
- **.superRefine**: Multiple issues or async; push to `ctx`.
- **.transform(fn)**: Change output type. Input and output can differ; use `z.input<typeof schema>` and `z.output<typeof schema>` (or `z.infer` for output).
- **.pipe(otherSchema)**: Chain validation/transform (e.g. string → number via `z.string().pipe(z.coerce.number())`).

---

## Parsing and errors

- **.parse(input)**: Returns data or throws **ZodError**.
- **.safeParse(input)**: Returns `{ success: true, data }` or `{ success: false, error: ZodError }`.
- **ZodError**: `error.issues` (array of `{ path, message, code }`), `error.format()` for nested shape.
- **Async**: `.parseAsync` / `.safeParseAsync` for schemas with async refinements or transforms.

---

## Type inference

- **z.infer<typeof schema>**: Output type (after transforms/defaults).
- **z.input<typeof schema>**: Input type (before transforms; useful when input ≠ output).
- **z.output<typeof schema>**: Same as `z.infer` for output type.

```ts
const S = z.string().transform((s) => s.length);
type In = z.input<typeof S>;  // string
type Out = z.output<typeof S>; // number
```

---

## Integration: React Hook Form

Use **@hookform/resolvers** with **zodResolver**:

```ts
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";

const formSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

type FormValues = z.infer<typeof formSchema>;

const form = useForm<FormValues>({
  resolver: zodResolver(formSchema),
  defaultValues: { email: "", password: "" },
});
```

---

## Best practices

- Prefer **strict** schemas (no extra keys) for API boundaries; use **.passthrough()** only when you need to forward unknown keys.
- Use **.default()** for optional fields with a default value.
- For API/env parsing, use **safeParse** and handle errors; show user-friendly messages from `error.issues`.
- Use **discriminated unions** for variant payloads (e.g. events by `type`).
- Coerce only when safe: `z.coerce.number()`, `z.coerce.boolean()`, or custom `.transform()`.

---

## Common mistakes

- **Forgetting strict**: Keep TypeScript `strict: true`; Zod works best with it.
- **Input vs output**: After `.transform()`, use `z.input<>` / `z.output<>` if the type seen by callers differs.
- **parse in hot path**: Prefer validating once at boundaries (e.g. API handler, form submit) rather than on every render.
- **Overly broad schema**: Prefer specific types (e.g. `.email()`, `.min()`) instead of plain `z.string()` when the domain has rules.

---

## Additional resources

- [reference.md](reference.md) — Official Zod docs links, API sections (primitives, objects, strings, numbers, refinements, etc.), Zod Mini, ecosystem.
- **Official**: https://zod.dev — Introduction, API, basics, ecosystem.
- **API (Zod 4)**: https://zod.dev/api — Full schema types and methods.
- **LLMs / index**: https://zod.dev/llms.txt — Structured doc for tools/agents.
