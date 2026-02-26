---
name: general-coding-guidelines
description: Always use this skill when writing or reviewing code.
---

# General Coding Guidelines

These are general guidelines that apply to all code. They need to be followed when creating and code and reviewed code is expected to follow these guidelines.

## 1) Coding Principles

### A) Correctness > Clarity > Consistency > Performance > Cleverness

- Do not introduce clever abstractions.
- Prefer boring, standard solutions that match the repo style.

### B) DRY (practical)

- Avoid repeating logic that might change.
- Avoid multiple large chunks of code in a single function.
- Extract shared logic into:
  1) private method (same class)
  2) dedicated service (bounded context)
  3) helper (only if truly global and reusable)

### C) SOLID (practical)

- Classes/functions should have one reason to change.
- Prefer composition over inheritance.
- Depend on interfaces/contracts where it improves testability and flexibility.

## 2) Variables & Functions (readability rules)

- Prefer clear naming over fewer variables.
- Inline values only if it improves clarity and avoids noise.
- Extract a function when:
  - a block repeats,
  - a block is hard to name inline,
  - it improves testability.

## 3) Comments Policy

- Avoid inline comments.
- Prefer descriptive names and small functions.
- Allowed comments:
  - Non-obvious constraints
  - Workarounds for external bugs
  - “Why” something is done (not “what”)

## 4) Database & Migrations Safety (language/framework-agnostic)

- Prefer additive, backwards-compatible schema changes when possible.
- Avoid destructive changes unless explicitly required.
- For destructive changes:
  - Call out irreversibility and data risk.
  - Provide a safe plan (two-step deploy or backfill approach).
- For large tables:
  - Avoid long-running locks where possible.
  - Prefer online/low-lock patterns (nullable column → backfill in batches → add constraints).
- Always consider rollback behavior:
  - Implement a rollback when feasible.
  - If rollback is unsafe, explicitly document it.
- Never drop/rename in a way that breaks running code during rolling deploys unless coordinated.

## 5) Performance & Query Hygiene (framework-agnostic)

- Default to clarity, but avoid obvious performance pitfalls.
- When touching query/data-heavy code:
  - Avoid N+1-style behavior (load in batches, use joins/eager loading equivalents).
  - Avoid fetching full records when only checking existence/count.
  - Paginate/limit large result sets.
  - Select only needed fields for large reads.
- Add indexes for frequently filtered/sorted columns where appropriate.
- Mention any performance-related changes in Notes/Risks.

## 6) Git / Commits

- Do not commit changes unless otherwise instructed.
- The user handles commits.

## 7) Linters / Static Analysis

- Do not run linters (eslint/phpstan/etc.) unless explicitly requested.
- However, write code that would pass typical linters.

## 8) Global Helpers

- Only create global helpers when reuse is likely across the codebase.
- If you add global helpers, document them in the project's README or AGENTS.md.

## 9) Avoid code smells

Watch for and avoid these anti-patterns:

### a) Long Functions

```typescript
// ❌ BAD: Function > 50 lines
function processMarketData() {
  // 100 lines of code
}

// ✅ GOOD: Split into smaller functions
function processMarketData() {
  const validated = validateData()
  const transformed = transformData(validated)
  return saveData(transformed)
}
```

### b) Deep Nesting

```typescript
// ❌ BAD: 3+ levels of nesting
if (user) {
  if (user.isAdmin) {
    if (market) {
      if (market.isActive) {
        if (hasPermission) {
          // Do something
        }
      }
    }
  }
}

// ✅ GOOD: Early returns
if (!user) return
if (!user.isAdmin) return
if (!market) return
if (!market.isActive) return
if (!hasPermission) return

// Do something
```

### c) Magic Numbers

```php
// ❌ BAD: Unexplained numbers
if ($retryCount > 3) { }
set_time_limit(500);

// ✅ GOOD: Named constants
$MAX_RETRIES = 3;
$DEBOUNCE_DELAY_MS = 500;

if ($retryCount > $MAX_RETRIES) { }
set_time_limit($DEBOUNCE_DELAY_MS);
```

## 10) .env files

.env.example files are a great way to document the environment variables required for a project. Populate them with happy defaults. if an environment variables should always be changed by the user, add it to the .env.example file without a value. For example:
```.env.example
ADMIN_USERNAME=admin
ADMIN_PASSWORD=
```
