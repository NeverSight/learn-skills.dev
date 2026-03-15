---
name: develop-typescript
description: >-
  Use skill if you are writing or reviewing framework-agnostic TypeScript and need strict typing,
  tsconfig/lint decisions, safer refactors, or guidance on generics, unions, and typed boundaries.
---

# Develop TypeScript

Write, review, or refactor framework-agnostic TypeScript with strict type safety, correct tsconfig,
and idiomatic patterns.

## Trigger boundary

Use this skill when:

- writing new TypeScript code that must be strictly typed
- reviewing existing TypeScript for type safety, anti-patterns, or missing narrowing
- configuring or auditing tsconfig.json and linting rules
- migrating JavaScript to TypeScript (or upgrading TS versions)
- diagnosing and resolving type errors, inference failures, or performance issues

Do not use this skill when:

- the task is primarily React/Vue/Angular component work (use framework-specific skills)
- the task is exclusively about Node.js runtime APIs (use a Node.js skill)
- the task is about build tooling only (use tooling-specific skills)

## Definitions

- **Load** — read the file into working context so you can reference its content
- **Checked `as`** — a cast following a runtime guard that proves the type (safe)
- **Unchecked `as`** — a cast with no runtime proof; hides bugs (almost always wrong)
- **Block** — in review mode, flag the issue and stop approving; do not auto-fix

## Mode detection

Before starting, determine your mode:

| Signal | Mode | Behavior |
|---|---|---|
| "Write", "implement", "create", "add" | **Authoring** | Write code, apply fixes, output files |
| "Review", "audit", "check", "look at" | **Review** | Report findings, never auto-fix, block on P0 |
| Ambiguous | **Ask** | Clarify with the user before proceeding |

## Required workflow

### Step 1 — Classify the task

Identify the primary category and optionally one adjacent category:

| Category | Reference to load |
|---|---|
| Type system (generics, narrowing, inference) | type-system.md |
| Patterns (result types, branded types, builders) | patterns.md |
| Anti-patterns (any, ts-ignore, unsafe casts) | anti-patterns.md |
| Error handling (Result, retry, aggregation) | error-handling.md |
| Strict config (tsconfig, strict flags) | strict-config.md |
| Tooling (ESLint, Biome, Prettier, CI) | tooling.md |
| Migration (JS-to-TS, version upgrades) | migration.md |
| Performance (compilation speed, traces) | performance.md |
| Testing (type tests, expect-type, tsd) | testing.md |
| Modern features (decorators, using, satisfies) | modern-features.md |

> **Steering note:** Most tasks span two categories. Load the primary reference plus one adjacent.
> If uncertain which category fits, scan the table above for keywords that match the user request.

### Step 2 — Load references

Load the reference file(s) identified in Step 1. Read the full file — do not skim.

If the task involves existing code, also load:
- The project's tsconfig.json (compare against strict-config.md baseline)
- The project's ESLint/Biome config (check for rule conflicts)

> **Steering note:** When reviewing tsconfig.json, only flag `moduleResolution: "node"` as legacy.
> `"node16"`, `"nodenext"`, and `"bundler"` are all modern and correct for their contexts.

### Step 3 — Execute the task

Apply the patterns and rules from the loaded references.

**In authoring mode:**
- Write code that follows the patterns in the reference files
- Use `satisfies` for config objects, explicit return types for public functions
- Never use bare `any`, `@ts-ignore`, or unchecked `as`
- Prefer `unknown` + narrowing over `any` for dynamic data

**In review mode:**
- Scan for every item in the anti-patterns.md review-mode checklist (Section: Review-Mode Scanning Checklist)
- For each finding, classify as P0 (blocks approval) or P1 (should fix) or P2 (nit)
- **Block** on: bare `any` in new code, `@ts-ignore` (should be `@ts-expect-error`), unchecked `as`, missing error narrowing
- Flag but don't block on: style preferences, minor naming issues

> **Steering note:** Distinguish lint warnings from type errors. Lint warnings are project-specific
> (respect the project's config). Type errors from `tsc` are universal and always blocking.

### Step 4 — Audit and verify

Run these checks:

```bash
# Find unannotated exported functions (authoring mode)
grep -rn "^export function" --include="*.ts" | grep -v ": " | head -20

# Find bare 'any' usage
grep -rn ": any\b" --include="*.ts" --include="*.tsx" | grep -v node_modules | head -20

# Find @ts-ignore (should be @ts-expect-error)
grep -rn "@ts-ignore" --include="*.ts" --include="*.tsx" | grep -v node_modules

# Find unchecked type assertions
grep -rn " as [A-Z]" --include="*.ts" | grep -v "// checked" | head -20

# Search for satisfies opportunities (config objects typed with annotation)
grep -rn "^const .* : Record<" --include="*.ts" | head -10
grep -rn "^const .* : {" --include="*.ts" | head -10
```

> **Steering note:** The `satisfies` audit catches config objects that use type annotations
> where `satisfies` would preserve literal types. This is a common missed opportunity.

### Step 5 — Handle conflicts

If the project's lint config contradicts skill recommendations:

1. For **new code** you're writing: follow the skill's stricter rules
2. For **existing code** under review: respect the project's config, flag conflicts as informational
3. Document the conflict: "Project disables X — consider re-enabling for new code"

> **Steering note:** Do not unilaterally re-enable lint rules. The project may have valid reasons
> for disabling them (e.g., gradual migration from JavaScript, third-party type issues).

### Step 6 — Deliver

**In authoring mode:** Output the complete, compilable code. Ensure every exported function has an explicit return type annotation.

**In review mode:** Output findings as a structured list with severity levels. Include specific line references and fix suggestions for each P0 and P1 finding.

> **Steering note:** Always produce a deliverable — code or findings list. Never end with only
> commentary or advice. The user expects actionable output.

## Common mistakes to avoid

| Mistake | Why it's wrong | What to do instead |
|---|---|---|
| Flagging `node16` moduleResolution as legacy | Only bare `"node"` is legacy | Check strict-config.md flag table |
| Using `any` for "I'll fix it later" | `any` disables all checking downstream | Use `unknown` and narrow |
| Ignoring cross-realm instanceof issues | Objects from iframes/workers fail instanceof | Use brand checks or Symbol.hasInstance |
| Auto-fixing code in review mode | Review should report, not modify | Block and describe; let the author fix |
| Skipping the deliverable step | User gets advice but no output | Always output code or structured findings |
| Treating `@ts-ignore` and `@ts-expect-error` as equivalent | `@ts-ignore` suppresses silently forever | Always prefer `@ts-expect-error` — it alerts when the error is fixed |

## Reference routing

| File | Load when |
|---|---|
| [type-system.md](references/type-system.md) | Working with generics, conditional types, type guards, narrowing, variance |
| [patterns.md](references/patterns.md) | Implementing Result types, branded types, builders, middleware, retry logic |
| [anti-patterns.md](references/anti-patterns.md) | Reviewing code for unsafe patterns or scanning for anti-pattern violations |
| [error-handling.md](references/error-handling.md) | Implementing error handling, retry logic, error aggregation, or Result types |
| [strict-config.md](references/strict-config.md) | Configuring or auditing tsconfig.json and strict mode flags |
| [tooling.md](references/tooling.md) | Setting up or choosing between ESLint, Biome, Prettier, CI pipelines |
| [migration.md](references/migration.md) | Migrating JS to TS, upgrading TS versions, handling circular dependencies |
| [performance.md](references/performance.md) | Diagnosing slow compilation, reading traces, optimizing type-check speed |
| [testing.md](references/testing.md) | Writing type-level tests, choosing test strategies, testing generics |
| [modern-features.md](references/modern-features.md) | Using decorators, `using`/`Symbol.dispose`, `satisfies`, inferred predicates |

## Guardrails

- Never introduce `any` — use `unknown` and narrow
- Never use `@ts-ignore` — use `@ts-expect-error` with explanation
- Never use unchecked `as` — always guard first, then cast
- Always add explicit return types to exported functions
- Always verify tsconfig against strict-config.md baseline before suggesting config changes
- In review mode: report findings, never silently modify code
