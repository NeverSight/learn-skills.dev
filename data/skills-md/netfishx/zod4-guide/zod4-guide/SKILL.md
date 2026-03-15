---
name: zod4-guide
description: Use when writing, reviewing, or debugging Zod schemas. Covers Zod 4 breaking changes from Zod 3, new APIs, and common pitfalls. Triggers on z.object, z.string, z.enum, z.record, z.refine, ZodError, schema validation, form validation, API response parsing.
license: MIT
metadata:
  author: netfishx
  version: "1.0.0"
---

# Zod 4 API Guide

## Overview

Zod 4 is a major rewrite with breaking changes from Zod 3. Claude's training data contains Zod 3 patterns — always prefer the Zod 4 syntax below. When unsure, consult https://zod.dev/v4/changelog.

## Breaking Changes (Zod 3 → 4)

| Category | Zod 3 (WRONG) | Zod 4 (CORRECT) |
|----------|---------------|-----------------|
| Error msg | `{ message: "..." }` | `{ error: "..." }` |
| Error params | `{ invalid_type_error, required_error }` | `{ error: (issue) => issue.input === undefined ? "Required" : "Invalid" }` |
| Error format | `.format()` / `.flatten()` | `z.treeifyError(err)` |
| Pretty print | manual formatting | `z.prettifyError(err)` |
| String formats | `z.string().email()` | `z.email()` |
| UUID | `z.string().uuid()` | `z.uuidv4()` (strict RFC 9562) or `z.guid()` (lenient) |
| IP address | `z.string().ip()` | `z.ipv4()` or `z.ipv6()` |
| CIDR | `z.string().cidr()` | `z.cidrv4()` or `z.cidrv6()` |
| Record | `z.record(valueSchema)` | `z.record(keySchema, valueSchema)` |
| Native enum | `z.nativeEnum(MyEnum)` | `z.enum(MyEnum)` |
| Enum access | `.Enum` / `.Values` | `.enum` only |
| Object merge | `.merge(other)` | `.extend(other.shape)` |
| Object strict | `.strict()` | `z.strictObject({...})` |
| Object loose | `.passthrough()` | `z.looseObject({...})` |
| Deep partial | `.deepPartial()` | Removed — flatten manually |
| Refinement chain | `z.string().refine(...).min(5)` broke | `z.string().refine(...).min(5)` works |
| Type predicate | `.refine((v): v is T => ...)` narrowed | No longer narrows inferred type |
| Function | `z.function().args(...).returns(...)` | `z.function({ input: [...], output: ... })` |
| Promise | `z.promise(schema)` | Removed — await before parsing |
| Default + optional | `z.string().default("x").optional()` → `{}` | → `{ a: "x" }` (default applies) |
| Prefault | N/A | `.prefault(val)` replicates v3 `.default()` input behavior |
| Coerce input type | Matched output type | Always `unknown` |
| Infinity | Passed `z.number()` | Rejected by `z.number()` |
| `.int()` / `.safe()` | Different behavior | Both restrict to safe integer range |
| Intersection error | Threw `ZodError` | Throws regular `Error` |
| `ZodTypeAny` | Available | Removed — use `z.ZodType` |
| `._def` | `schema._def` | `schema._zod.def` |
| Symbols as literal | Supported | Removed |
| `z.ostring()` etc. | Available | Removed |

## New APIs in Zod 4

**Recursive types** — use getter instead of `z.lazy()`:
```ts
const Category = z.object({
  name: z.string(),
  get subcategories() { return z.array(Category); }
});
```

**Template literals** — type-safe string templates:
```ts
const css = z.templateLiteral([z.number(), z.enum(["px", "em"])]);
// Type: `${number}px` | `${number}em`
```

**File validation**: `z.file().min(1024).max(5_000_000).mime(["image/png"])`

**Number formats**: `z.int32()`, `z.uint32()`, `z.float32()`, `z.int64()`

**String boolean**: `z.stringbool()` — parses "true"/"yes"/"1" → true

**Overwrite** (type-preserving transform): `z.number().overwrite(v => v ** 2).max(100)`

**Metadata**: `schema.meta({ title: "Email", examples: ["a@b.com"] })`

**JSON Schema**: `z.toJSONSchema(schema)`

**Zod Mini** (1.88kb): `import * as z from "zod/mini"` — functional API, tree-shakable

## Common Pitfalls

1. **`$ZodIssue` has no `received` field** — Zod 4 removed it. Access `issue.input` instead.
2. **`z.record(schema)` fails** — must be `z.record(keySchema, valueSchema)`.
3. **UUID rejects valid v4 UUIDs** — `z.uuidv4()` enforces RFC 9562 variant bits. Use `z.guid()` for lenient.
4. **Enum keys in record are required** — `z.record(z.enum([...]), val)` requires ALL keys. Use `z.partialRecord()` for optional.
5. **`.default()` applies inside `.optional()`** — `z.string().default("x").optional().parse(undefined)` → `"x"` not `undefined`.
6. **Error map precedence reversed** — schema-level `error` now beats parse-time handler (opposite of v3).
7. **Refinements no longer narrow types** — `z.unknown().refine((v): v is string => ...)` stays `unknown`.
