---
name: explicit-code-style
description: >-
  Apply explicit, safe coding conventions when writing or reviewing code: use
  multiline braced control flow, explicit loops, and strict TypeScript value
  handling. Use when editing, reviewing, or refactoring application code;
  respect API contracts and language-specific constraints.
---

# Explicit code style

Prefer code whose control flow, errors, types, and absence semantics are visible
at a glance. Apply these conventions without exposing implementation details or
changing contracts. Follow the current repository's `AGENTS.md` and tool-enforced
rules when they add stricter constraints; never use that as a reason to weaken
the API JSON rule below.

## Multiline control flow

Write `if`, `for`, and `while` statements with braces and a multiline body where
the language supports them. Avoid single-line control-flow bodies, even when
they are short. This keeps future edits safe and makes branches easy to scan.

```ts
if (!user) {
  return;
}
```

Avoid:

```ts
if (!user) return;
```

Apply the equivalent block form in languages with different syntax. Do not
rewrite a language construct into invalid or less safe syntax merely to imitate
the TypeScript example.

## Explicit iteration

Avoid callback-style `.forEach(...)` and iterator `.for_each(...)`. Prefer an
explicit `for`, `for...of`, or language-equivalent loop so that `break`,
`continue`, `return`, and error propagation have clear semantics.

```ts
for (const item of items) {
  process(item);
}
```

Use transformations such as `map`, `filter`, or `reduce` when they express a
value transformation clearly; this rule is about callback iteration, not a ban
on functional operations generally.

## Absence values in TypeScript and JavaScript

In TypeScript/JavaScript, represent an absent optional value with `undefined`
or an optional field rather than `null`. Convert database `NULL` at the
persistence boundary. Do not claim an external API or library omits `null` if
it does not; normalize the value at the adapter boundary.

```ts
let timeout: ReturnType<typeof setTimeout> | undefined;
type Profile = { nickname?: string };
```

Do not apply JavaScript's `undefined` rule literally to other languages. Use
their explicit optional-value type or idiom (for example, `Option<T>` in Rust).

## TypeScript safety conventions

When editing TypeScript, avoid `any`, type assertions (including non-null
assertions), and unused variables. Prefer explicit types, validated parsers,
type guards, and removing dead declarations. At external-data boundaries,
receive untrusted data as `unknown` and validate it before it crosses into
business logic.

Handle errors deliberately: do not swallow exceptions or leave empty catch
handlers. Add context, map to a safe domain error, or report through the
project's established mechanism. In async codebases that standardize on
`try`/`await`, use that convention rather than detached promise rejection
handlers.

## Review checklist

- Are conditionals and loop bodies braced and multiline?
- Is callback-style `forEach` used where an explicit loop would clarify control
  flow?
- In TypeScript, are `any`, unsafe assertions, unused variables, and swallowed
  errors avoided?
- Is external data validated before entering business logic?
- Did the change preserve language, API, and repository-specific contracts?
