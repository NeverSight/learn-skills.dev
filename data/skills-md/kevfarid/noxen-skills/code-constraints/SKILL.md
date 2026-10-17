---
name: code-constraints
description: >
  Use when writing or reviewing code for file size, comment quality, or
  component-per-file discipline in a TypeScript codebase. Trigger on tasks
  like "is this file too long", "should I split this component", "review
  this file for size/style", or "how should I comment this". Do NOT trigger
  for component architecture or typing decisions themselves — see the
  sibling react-patterns and typescript skills.
metadata:
  version: 1.0
  collection: noxen
---

# Noxen — Code Constraints

Part of the **Noxen** skill set (a personal engineering standard for React +
TypeScript + Tailwind). This skill covers file-size and comment discipline
only.

## One Component Per File — No Exceptions

```tsx
// ❌ Bad
export function DashboardPage() { ... }
export function DashboardCard() { ... }

// ✅ Good — separate files
// dashboard-page.tsx
export function DashboardPage() { ... }

// components/dashboard-card.tsx
export function DashboardCard() { ... }
```

Extract to its own file when:
- Used by the parent
- Has its own logic or state
- Exceeds 10 lines
- Could be reused

## Max 200 Lines Per File

When exceeded, extract: sub-components, custom hooks, service file, constants, types.

If splitting would make the code worse, say so:
```
This file is X lines, over the 200-line limit.
I recommend keeping it together because: [reason].
Options: 1. Split anyway  2. Keep as exception  3. Different approach?
```

Exceptions (no limit): `package.json`, `*.lock`, `tsconfig.*`, `vite.config.ts`, `*.d.ts`, generated files.

## Comments — WHY Not WHAT

```ts
// ❌ Repeats code
const userName = user.name; // Set the user name

// ✅ Explains why
/**
 * Processes in batches to avoid memory overflow
 * on datasets > 10k items
 */
const processInBatches = (items: Item[]) => { ... };

// ✅ JSDoc for props
interface UserProfile {
  /** Unique identifier from auth provider */
  id: string;
  /** Display name — may differ from auth name */
  displayName: string;
}
```

Use JSDoc only for: component props interfaces, complex functions, public APIs, business logic needing context.

## A Documented Convention Without Enforcement Isn't a Standard

Every naming/style rule in this collection (kebab-case files, boolean
prefixes, `interface` vs `type`, etc.) should have a matching lint rule
backing it — otherwise it's a suggestion that erodes the first time someone
is in a hurry. A minimal enforcement setup:

```
eslint-plugin-check-file           → enforces kebab-case filenames
@typescript-eslint/naming-convention → enforces the boolean-prefix list (see `typescript`)
consistent-type-imports            → enforces `import type` (see `typescript`)
no-nested-ternary, no-unneeded-ternary → error, not warn
```

Wire it to the git flow so violations can't land silently:

```
husky pre-commit   → runs the linter, blocks the commit on failure
husky commit-msg   → runs commitlint against Conventional Commits
```

When introducing a new convention into a project, add the lint rule (or a
`// TODO: add lint rule for X` if the linter can't express it) in the same
change — don't leave it as prose alone.

## Hard Rules

- One exported component per file, no exceptions.
- Max 200 lines per source file (excluding config/generated files) — flag and propose options instead of silently splitting.
- Comments explain WHY, never restate WHAT the code already says.
- A new naming/style convention ships with a lint rule enforcing it, or an explicit note that none exists yet — not prose alone.
