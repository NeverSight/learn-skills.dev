---
name: json-schema
description: How to write and review JSON Schema documents per the 2020-12 specification (https://json-schema.org/draft/2020-12) - project-agnostic. Covers boolean schemas, the core vocabulary ($schema, $id, $ref, $anchor, $dynamicRef/$dynamicAnchor, $defs, $vocabulary, $comment), validation keywords for each JSON type, applicators (allOf/anyOf/oneOf/not/if-then-else), unevaluatedProperties/unevaluatedItems, annotations (title, description, default, examples, deprecated, readOnly, writeOnly), and the format/content vocabularies. Use when writing a schema to validate JSON (config files, API request/response bodies, event payloads), reviewing a schema for spec compliance, debugging why a document does or doesn't validate, or deciding between $ref and $dynamicRef for recursive/extensible schemas.
---

# JSON Schema (2020-12)

A vocabulary for annotating and validating JSON documents — itself
expressed as JSON (or YAML). The 2020-12 draft is the current
specification; full text at
[json-schema.org/draft/2020-12](https://json-schema.org/draft/2020-12)
and its [release notes](https://json-schema.org/draft/2020-12/release-notes).
It's split into three specs that a schema author rarely needs to
separate in practice:
- **Core** — structure, identifiers, references. See
  [`references/identifiers-and-refs.md`](references/identifiers-and-refs.md).
- **Validation** — the assertion keywords themselves (type checks,
  ranges, required properties, ...). See
  [`references/validation-keywords.md`](references/validation-keywords.md).
- **Vocabularies** (format, content, meta-data, unevaluated) — optional
  keyword sets a dialect can mix in. See
  [`references/vocabularies-and-annotations.md`](references/vocabularies-and-annotations.md).

## The core idea

A schema is either a **boolean** or an **object**:
- `true` — matches every instance. `false` — matches nothing. Most
  often seen as `"additionalProperties": false`.
- An object whose keywords each add a constraint. Every keyword an
  implementation doesn't recognize (including `$comment`, and any
  keyword from a vocabulary that isn't in play) is silently ignored,
  not an error — schemas degrade gracefully across dialects.

Every applicable keyword's assertion must hold for the instance to be
valid — there's no keyword ordering or short-circuiting that changes
the result, only performance. `type` doesn't gate the other keywords:
`{"type": "string", "minimum": 5}` is legal (if useless) — a number
instance fails `type` and a string instance trivially passes `minimum`
(it doesn't apply to non-numbers), so the schema behaves like
`type` alone.

## Quick example

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.com/schemas/product.json",
  "title": "Product",
  "type": "object",
  "properties": {
    "id": { "type": "integer" },
    "name": { "type": "string", "minLength": 1 },
    "price": { "type": "number", "exclusiveMinimum": 0 },
    "tags": {
      "type": "array",
      "items": { "type": "string" },
      "uniqueItems": true
    }
  },
  "required": ["id", "name", "price"],
  "additionalProperties": false
}
```

`$schema` declares the dialect being written against — always include
it, since it's the only signal a validator has for which keyword set
and semantics to apply (2020-12 changed `items`, `exclusiveMinimum`,
and reference resolution behavior from earlier drafts — see
[Gotchas](#gotchas)).

## Where to look

| Reference | Covers |
|---|---|
| [`references/validation-keywords.md`](references/validation-keywords.md) | `type`, `enum`/`const`, numeric/string/array/object assertion keywords, `allOf`/`anyOf`/`oneOf`/`not`, `if`/`then`/`else`, `dependentRequired`/`dependentSchemas` |
| [`references/identifiers-and-refs.md`](references/identifiers-and-refs.md) | `$id`, `$anchor`, `$ref`, `$dynamicRef`/`$dynamicAnchor`, `$defs`, base-URI resolution, recursive and extensible schemas, bundling multiple resources in one document |
| [`references/vocabularies-and-annotations.md`](references/vocabularies-and-annotations.md) | `$schema`/`$vocabulary` and the 2020-12 vocabulary list, `unevaluatedProperties`/`unevaluatedItems`, `format` (annotation vs. assertion), `contentEncoding`/`contentMediaType`/`contentSchema`, meta-data annotations, `$comment` |

## Gotchas

- **`items` changed shape in 2020-12.** Tuple validation (per-index
  schemas) is now `prefixItems` (an array of schemas); `items` takes a
  single schema applied to every element after the `prefixItems`
  positions (or to all elements if there's no `prefixItems`).
  `additionalItems` from older drafts is gone — `items` does its job.
  A draft-07-style `"items": [...]` array is not valid 2020-12.
- **`exclusiveMinimum`/`exclusiveMaximum` are numbers**, not booleans —
  `{"exclusiveMinimum": 0}`, not `{"minimum": 0, "exclusiveMinimum": true}`
  (that was draft-04). Mixing the two styles from a copy-pasted example
  is a common source of schemas that silently validate nothing useful.
- **`$ref` can sit alongside other keywords** in the same schema object
  since 2019-09 — unlike draft-07/4, where every other keyword next to
  `$ref` was ignored. Don't assume old advice to "never put anything
  next to `$ref`" still applies; the sibling keywords are now honored.
- **`format` doesn't validate by default.** It's annotation-only unless
  the dialect opts into the Format-Assertion vocabulary or the
  implementation is explicitly configured to assert — see
  [`references/vocabularies-and-annotations.md`](references/vocabularies-and-annotations.md).
  Don't rely on `{"format": "email"}` alone to reject bad emails without
  checking your validator's configuration.
- **`required` lists property names, not a per-property flag.** There's
  no `"required": true` inside a property's own subschema — required-ness
  is declared once, as an array, on the parent object schema.
- **`patternProperties`/`pattern` use ECMA-262 regex**, and `pattern`
  is unanchored by default — `"pattern": "foo"` matches `"xxfooxx"`.
  Anchor explicitly with `^`/`$` when you mean the whole string.
- **Unknown keywords are ignored, not rejected** — a typo like
  `"require"` instead of `"required"` produces a schema that silently
  validates everything, not a schema-loading error. Validate schemas
  themselves against the meta-schema when debugging unexpected passes.
