---
name: zod-validation
description: 'Zod v4 schema validation for TypeScript. Covers primitives, string formats, objects, arrays, unions, coercion, transforms, refinements, parsing, type inference, error customization, JSON Schema, file validation, and metadata. Use when writing schemas, validating input, parsing data, inferring types, or converting schemas with Zod.'
license: MIT
metadata:
  author: oakoss
  version: '1.1'
---

# Zod Validation (v4)

Type-safe schema validation for TypeScript. Zod v4 introduces top-level format functions, `z.stringbool()`, `z.iso.*` date formats, `z.overwrite()` transforms, `z.file()`, `z.toJSONSchema()`, getter-based recursive types, `.meta()`, and the unified `error` function.

**Package:** `zod` (also `zod/mini` for smaller bundles)

## Quick Reference

| Pattern                                    | Usage                                          |
| ------------------------------------------ | ---------------------------------------------- |
| `z.object({ ... })`                        | Define object schemas                          |
| `z.string()`, `z.number()`                 | Primitive types                                |
| `z.email()`, `z.url()`, `z.uuid()`         | Top-level string formats (v4)                  |
| `z.iso.date()`, `z.iso.datetime()`         | ISO date/time formats (v4)                     |
| `z.int()`, `z.float32()`, `z.int32()`      | Fixed-width number formats (v4)                |
| `z.templateLiteral([...])`                 | Template literal type validation (v4)          |
| `z.enum([...])`, `z.literal()`             | Enums and literals                             |
| `z.union([...])`, `z.discriminatedUnion()` | Union types                                    |
| `z.array()`, `z.tuple()`                   | Array and tuple types                          |
| `z.record()`, `z.map()`                    | Key-value collections                          |
| `.optional()`, `.nullable()`               | Optional and nullable modifiers                |
| `.default()`, `.catch()`                   | Default values and fallbacks                   |
| `.prefault()`                              | Pre-parse default (parsed through schema, v4)  |
| `z.coerce.number()`                        | Type coercion before validation                |
| `z.stringbool()`                           | String-to-boolean parsing (v4)                 |
| `.transform()`, `.overwrite()`             | Output transforms                              |
| `z.pipe()`                                 | Chain schemas (output feeds next input)        |
| `.refine()`, `.superRefine()`              | Custom validation logic                        |
| `.parse()`, `.safeParse()`                 | Validate and extract data                      |
| `z.infer<typeof Schema>`                   | Extract TypeScript type from schema            |
| `z.input<>`, `z.output<>`                  | Input vs output types with transforms          |
| `z.file()`                                 | File instance validation (v4)                  |
| `z.toJSONSchema()`                         | Convert schema to JSON Schema (v4)             |
| `.meta()`, `.describe()`                   | Attach metadata to schemas (v4)                |
| `z.prettifyError()`                        | Human-readable error formatting (v4)           |
| `z.treeifyError()`                         | Structured error tree (replaces .format(), v4) |
| `z.registry()`                             | Typed schema registry (v4)                     |
| `{ error: (issue) => ... }`                | Unified error customization (v4)               |
| Getter-based recursion                     | Recursive types without `z.lazy()` (v4)        |
| `z.globalRegistry`                         | Global schema metadata registry (v4)           |
| `z.config(z.locales.en())`                 | Internationalized error messages (v4)          |

## Common Mistakes

| Mistake                                 | Fix                                                           |
| --------------------------------------- | ------------------------------------------------------------- |
| `z.string().email()`                    | `z.email()` (v4 top-level format)                             |
| `z.string().url()`                      | `z.url()` (v4 top-level format)                               |
| Using `parse` without try/catch         | Use `safeParse` for error handling                            |
| Forgetting `.optional()`                | Add when field may be undefined                               |
| `z.any()` for unknown data              | Use `z.unknown()` for type-safe unknown                       |
| `.transform()` for same-type changes    | Use `.overwrite()` (introspectable, v4)                       |
| Missing `.min(1)` on strings            | Empty strings pass `z.string()` by default                    |
| `z.number().parse(Infinity)`            | `z.number()` rejects `Infinity` in v4                         |
| `z.number().safe()` for floats          | `.safe()` equals `.int()` in v4 (no floats)                   |
| `z.lazy()` for recursive types          | Use getter syntax in v4 (retains object methods)              |
| `required_error` / `invalid_type_error` | Use unified `error` function in v4                            |
| `.refine(fn, (val) => ({ message }))`   | Function-as-second-arg overload removed; use `.superRefine()` |
| `errorMap` on schemas                   | Replaced by `error` function in v4                            |
| `z.record(z.string())` single arg       | v4 requires two args: `z.record(z.string(), z.string())`      |
| `.format()` / `.flatten()` on ZodError  | Deprecated; use `z.treeifyError(err)` in v4                   |
| `.default()` with input type value      | v4 `.default()` uses output type; use `.prefault()` for input |

## Delegation

Use this skill for Zod schema definition, validation, parsing, type inference, coercion, error formatting, metadata, and JSON Schema conversion. For form integration, delegate to the tanstack-form skill.

## References

- [Schema Types](references/schema-types.md) — primitives, string formats, number formats, template literals, objects, arrays, enums, unions, records, optional, nullable
- [Transforms and Parsing](references/transforms-and-parsing.md) — coercion, stringbool, transforms, overwrite, pipe, refinements, parsing, type inference
- [Error Handling](references/error-handling.md) — unified error function, prettifyError, treeifyError, ZodError, error formatting, internationalization
- [Common Patterns](references/common-patterns.md) — form validation, API responses, environment variables, schema composition, recursive types, branded types
- [Metadata and JSON Schema](references/metadata-and-json-schema.md) — meta, describe, globalRegistry, toJSONSchema, file validation, Zod Mini
