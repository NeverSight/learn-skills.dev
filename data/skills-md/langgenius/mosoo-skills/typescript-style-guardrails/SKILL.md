---
name: typescript-style-guardrails
description: Readability-first TypeScript and TSX style guardrails for strict codebases. Use when reviewing or editing TypeScript, defining shared contracts, creating lintable style rules, or deciding between type vs interface, null vs undefined, and Pick/Omit/Partial-heavy type expressions.
---

# Typescript Style Guardrails

## Overview

Enforce readable, boundary-aware TypeScript in strict codebases. Prefer code that a reviewer can parse quickly over clever inline type composition.
If the repository already documents a stronger local convention, follow the repository before applying this skill mechanically.

## Working Mode

1. Identify whether the code is a boundary type, an internal helper type, or UI-local state.
2. Optimize first for semantic clarity in signatures and exported APIs.
3. Use utility types as construction tools, not as the main surface a human reads.
4. Prefer lint-enforceable rules over taste-based advice.
5. If the repository already has a stronger local rule, follow the repository.

## Core Rules

### Prefer named types over inline type algebra

- Extract `Pick`, `Omit`, intersections, mapped types, and long unions into a named `type` or `interface` before using them in parameters, returns, props, or exports.
- Do not leave dense expressions like `Pick<Foo, "a" | "b" | "c"> & Bar` inline in a function signature unless the expression is trivially short.
- Name the type for the business meaning, not the mechanism. Prefer `EnvironmentSessionRow` over `PickedEnvironmentFields`.

### Use `interface` for object contracts and `type` for composition

- Prefer `interface` for exported object shapes that are meant to be implemented, extended, or merged naturally.
- Prefer `type` for unions, tuples, conditional types, mapped types, utility-type compositions, branded types, and extracted aliases.
- Do not force `interface` where the shape is fundamentally a union or type-level transform.

### Keep boundary types explicit

- Write explicit DTO or view-model shapes when a type crosses a service boundary, UI boundary, persistence boundary, or package boundary and the fields are stable.
- Use `Pick` or `Omit` only when the derived shape is tightly coupled to the source type and that coupling is useful.
- When a derived type starts accumulating exceptions, stop composing and write the object shape explicitly.

### Treat `null` as a contract, not a default

- Use `null` only when an external system, schema, protocol, or domain state explicitly distinguishes empty from omitted.
- Prefer `undefined`, optional properties, or absent fields for internal optionality unless the contract already uses `null`.
- Keep one absence model per boundary whenever possible. Do not mix optional, `undefined`, and `null` without a concrete reason.

### Avoid anonymous structural duplication

- Reuse shared entities and exported subpath contracts before inventing app-local duplicates.
- If a local shape differs for a real reason, give it a new semantic name and document the boundary.
- Do not import broad root barrels when the repository provides stable subpath exports.

### Keep React types boring

- Type props and state with named contracts when the shape is reused, edited, or non-trivial.
- Do not mirror props into state only to satisfy typing convenience.
- Avoid effect-driven type workarounds; derive values directly when possible.
- Keep component-local helper types local unless they cross module boundaries.

## Decision Rules

### `Pick` and `Omit`

Use them when:

- the source type is canonical
- the subset is small and obviously coupled to the source
- extraction improves reuse or prevents drift

Stop using them when:

- the field list is long enough to hide intent
- the resulting type appears in a public signature
- the subset represents a new domain concept
- multiple utility types are chained together to express one business type

Preferred rewrite:

```ts
type EnvironmentSessionRow = Pick<
  PipelineUserEnvironmentRow,
  | "pipelineId"
  | "userId"
  | "type"
  | "environmentId"
  | "deviceCode"
  | "metadata"
  | "hostConnectionId"
  | "hostAuthMode"
  | "hostAuthTokenId"
  | "hostAuthSessionId"
>;

function mapEnvironment(row: EnvironmentSessionRow) {
  // ...
}
```

Write the shape explicitly instead when the extracted alias still hides the business meaning.

### `null` vs `undefined`

Use `T | null` when:

- a database column is nullable
- JSON or RPC payloads intentionally send `null`
- the domain has a real "present but empty" state

Use `?` or `undefined` when:

- a caller may omit the field
- the value is optional only during local computation
- the code is modeling partial construction, config, or component state

## Review Checklist

Check these in order:

1. Can a reviewer understand the exported type or function signature without mentally expanding utility types?
2. Does the type name communicate domain meaning instead of implementation mechanics?
3. Is `null` justified by a real boundary contract?
4. Is a shared contract already available?
5. Can the proposed rule be enforced by ESLint, TypeScript, or code review guidance?

## Implementation Notes

- Keep rule text short and directive.
- Prefer examples that show the before/after of a readability improvement.
- When proposing repo-wide rules, pair style guidance with lint rules or review heuristics from `references/external-guides.md`.
- If a repository already documents a different convention, record the exception instead of overwriting it silently.

## References

- Read `references/external-guides.md` when you need upstream guidance or links to published style guides.
