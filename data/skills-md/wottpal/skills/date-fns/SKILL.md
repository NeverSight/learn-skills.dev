---
name: date-fns
description: Practical workflow for date-fns v4 and native @date-fns/tz usage, covering imports, parsing/formatting, calculations, timezone-safe patterns, and common pitfalls.
---

# date-fns + @date-fns/tz

## Purpose

Use this skill to implement, review, and refactor date/time code with modern `date-fns` and the native timezone package `@date-fns/tz`.

## Version baseline (re-check when invoked)

- `date-fns` latest verified: `4.1.0`
- `@date-fns/tz` latest verified: `1.4.1`
- Re-check commands:
  - `npm view date-fns version`
  - `npm view @date-fns/tz version`
  - `npm view date-fns dist-tags --json`
  - `npm view @date-fns/tz dist-tags --json`

## When to use

- Parsing, validating, formatting, comparing, and calculating dates.
- Building timezone-aware business logic (scheduling, boundaries, reporting).
- Migrating date logic to immutable utility patterns.
- Hardening code against DST and token-format bugs.

## Non-negotiable rules

- Use native timezone package: `@date-fns/tz`.
- Do not recommend `date-fns-tz`.
- If legacy code already uses `date-fns-tz`, suggest migration to `@date-fns/tz`.
- Parse once, validate early (`isValid`), and pass `Date` values through operations.
- Use Unicode tokens correctly (`yyyy`, `MM`, `dd`) and avoid Moment-style token assumptions.
- For timezone-sensitive calculations, use explicit timezone context (`TZDate` or `{ in: tz("...") }`).

## Canonical imports

```ts
import { format, parseISO, isValid, addDays, startOfDay } from "date-fns";
import { TZDate, tz, tzOffset, tzName, tzScan } from "@date-fns/tz";
```

## Workflow

### 1) Normalize input

- Use `parseISO`/`toDate` for conversion.
- Guard with `isValid`.
- Keep internal values as `Date`/`TZDate`, not mixed string math.

### 2) Compute with pure helpers

- Prefer `add/sub`, `differenceIn*`, `startOf*/endOf*`, `isSame*`, `isWithinInterval`.
- Avoid mutating `Date` via setters unless there is a clear reason.

### 3) Apply timezone context explicitly

- Option A: use `TZDate` values.
- Option B: use date-fns `in` option with `tz("Area/City")` for deterministic zone context.

### 4) Format/output safely

- Use `format` for display.
- Use standards helpers for exchange formats (`formatISO`, `formatRFC3339`).
- Keep transport format and display format separate.

## Deliverables

When answering, provide:

- Exact imports.
- Minimal correct function set for the use case.
- Timezone strategy (`TZDate` vs `{ in: tz(...) }`) and why.
- Edge-case notes (DST boundaries, token correctness, invalid inputs).

## Progressive disclosure

Load only what is needed:

- `reference/core-functions.md` for essential helpers.
- `reference/native-timezones.md` for `@date-fns/tz` patterns.
- `reference/imports-and-practices.md` for import/runtime practices.
- `reference/format-parse-tokens.md` for token correctness.
- `reference/examples.md` for copy-ready snippets.
- `reference/anti-patterns.md` for strict "never use `date-fns-tz`" guidance.
- `reference/version-and-sources.md` for version checks and source links.
