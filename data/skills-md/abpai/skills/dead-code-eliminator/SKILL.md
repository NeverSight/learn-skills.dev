---
name: dead-code-eliminator
description: >
  Audit a codebase for dead code — unreachable functions, unused imports,
  orphaned classes, unreachable branches, and stale feature flags — by
  tracing live call paths from all entry points. Also audits correctness
  (do implementations match their claimed purpose?) and algorithmic
  soundness. Produces an ASCII call graph and a categorized dead code
  report. Use when a codebase has gone through many iterations, a large
  refactor has landed, a feature was removed but its support code may
  remain, or the user asks to "find dead code", "clean up unused code",
  "audit what's actually used", or "find orphaned functions".
license: MIT
metadata:
  author: Andy Pai
  version: "1.0"
  tags: "dead-code cleanup refactor audit unused imports"
---

# Dead Code Eliminator

You are switching into **Dead Code Elimination** mode. Your role is static
analyst and safety-gated refactoring assistant. You trace every live call
path from every entry point, identify everything unreachable, audit
correctness and algorithmic soundness of live code, and present a full
report before touching a single line.

---

## Phase 1 — Entry Point Discovery

Identify all symbols that are reachable without being called by other
code in the project. These are the roots of the live call graph.

**Executable entry points**
- `main`, `__main__`, top-level scripts run directly
- CLI `bin` declarations in `package.json`, `pyproject.toml`, `setup.cfg`
- Makefile targets and shell scripts that invoke project code

**API / server entry points**
- Route handlers (Express, FastAPI, Rails, Django, etc.)
- Event listeners and message-queue consumers
- Cron jobs, scheduled tasks, webhooks, signal handlers

**Library exports**
- `export` / `export default` (JS/TS)
- `module.exports` (CommonJS)
- `__all__` (Python)
- Package index files (`index.ts`, `__init__.py`, `mod.rs`, `lib.rs`)

**Test files**
Treat as secondary live consumers. A symbol exercised by a test is
reachable — but note it as test-only, not as production-reachable.

**Framework magic**
- Lifecycle hooks invoked by convention (e.g., `componentDidMount`,
  `setUp`, `tearDown`, `beforeEach`)
- Decorator-driven wiring (`@Controller`, `@Injectable`, `@app.route`)
- Annotation-driven DI containers and ORM model registrations

List every discovered entry point before proceeding.

---

## Phase 2 — Live Call Graph

Trace the **transitive closure** from every entry point.

- Follow all direct calls, imports, and class instantiations.
- Follow dynamic dispatch where the target is statically determinable
  (e.g., polymorphism with a finite, known set of subtypes).
- **Flag** calls through `eval`, reflection, `getattr(obj, name)`,
  or string-keyed dispatch as **UNRESOLVABLE** — do not guess at
  reachability; require manual review.
- Mark symbols that are only reachable via a feature flag or
  environment-conditional branch as **CONDITIONALLY REACHABLE**; note
  the condition.
- Build the **live set**: every module, class, function, method, and
  import that is reachable from at least one entry point.

If the codebase is too large to trace completely, stop and ask the user
to scope the analysis to a subsystem or directory before continuing.

---

## Phase 3 — Dead Code Categorization

Everything **not** in the live set belongs to one of the following
categories. For each item record:
- `file:line`
- Category (from the list below)
- Inferred purpose (what it appears to have been for)
- Confidence: `HIGH` (provably unreachable) or `LOW` (heuristic /
  dynamic dispatch may reach it)

**Categories**

| Category | Description |
|---|---|
| Unreachable function/method | Never called from any live path |
| Orphaned class | Never instantiated, extended, or referenced |
| Unused import | Imported symbol never referenced in the file |
| Unreachable branch | Condition is provably always true or always false |
| Stale feature flag | Flag always-on or always-off; branch is dead |
| Unused export | Exported but never imported within the project |
| Dead test | Tests a function that no longer exists |
| Shadowed definition | Later definition overwrites an earlier one |

**Special handling**

- Library / package with possible external consumers: label as
  `UNUSED EXPORT (external consumers possible)` — do NOT treat as dead.
- Test-exercised symbols: list in a separate **Test-Only** section,
  not in the dead code list.
- Low-confidence items must be called out explicitly; never silently
  omit them.

---

## Phase 4 — Correctness and Algorithmic Soundness Audit

Audit **live code only** (the live set from Phase 2). Record all
findings as **Suggestions** — do NOT modify any code in this phase.

**Correctness**
- Does the function name accurately describe what it returns or does?
- Are documented contracts (param types, return values, raises) honored?
- Are edge cases handled? (empty input, null/None, zero, overflow)
- Are calculations and formulas correct for the stated domain?

**Algorithmic Soundness**
- Does the implementation match the claimed algorithm?
  (e.g., a function named `median` that actually returns the mean fails
  this check)
- Are performance characteristics consistent with the stated purpose?
  (e.g., an O(n²) inner loop inside a method called `fastSearch`)
- Does any recursion have a guaranteed base case?
- Does any loop have a guaranteed termination condition?

Suggestions use the same severity vocabulary as the rest of this
skill's output: `Critical`, `Important`, `Suggestion`.

---

## Phase 5 — Report

Produce the full report in this order:

### 5a — ASCII Call Graph

Render a **layered flow** call graph tracing from entry points to
leaf functions. Follow the ASCII style conventions:

- Box-drawing characters: `┌ ┐ └ ┘ ─ │ ├ ┤ ┬ ┴ ┼`
- Arrows: `▶ ▼ ◀ ▲` or `──▶` for directed edges
- Label every edge with the call type or condition
- **Maximum width: 70 characters**
- Collapse large subtrees with `[... N functions]` to stay within width
- One graph covers the entire project; use indentation for depth

Example layout:

```
main()
  │
  ├──▶ initConfig()
  │      └──▶ loadEnv()        [live]
  │
  ├──▶ startServer()
  │      ├──▶ GET /users ──▶ listUsers()    [live]
  │      └──▶ POST /users ──▶ createUser()  [live]
  │               └──▶ hashPassword()       [live]
  │
  └──▶ setupCron()
         └──▶ pruneExpired()   [live]
```

### 5b — Dead Code List

Group items by category. Within each category, order by file path.

```
┌─────────────────────────────────────────────────────┐
│  DEAD CODE REPORT                                   │
├─────────────────────────────────────────────────────┤
│  Unreachable functions/methods              N items │
│  Orphaned classes                           N items │
│  Unused imports                             N items │
│  Unreachable branches                       N items │
│  Stale feature flags                        N items │
│  Unused exports                             N items │
│  Dead tests                                 N items │
│  Shadowed definitions                       N items │
└─────────────────────────────────────────────────────┘
```

For each item:

```
[CATEGORY] src/utils/helpers.ts:42
  Function: formatLegacyDate()
  Purpose:  ISO-8601 formatter for v1 API responses (removed in v2)
  Confidence: HIGH
```

### 5c — Test-Only Symbols

List all symbols reachable only through test files. These are not dead
code but are also not production-reachable.

### 5d — Suggestions (Correctness and Soundness)

List findings from Phase 4 using this format:

```
[Critical/Important/Suggestion] src/auth/jwt.ts:88
  Function: verifyToken()
  Issue: Returns true for expired tokens when clock skew > 300s
  Recommendation: Compare exp against Date.now()/1000 before returning
```

Do not include style issues. This section covers correctness and
algorithmic soundness only.

### 5e — Safe Removal Order

Provide a numbered removal sequence that avoids dependency errors:

1. Unused imports (no dependents)
2. Leaf functions (called by no live or dead code)
3. Mid-graph functions (whose callees are already removed)
4. Orphaned classes (once all their methods are cleared)
5. Stale feature flag branches (condition removal + dead branch body)
6. Dead files (once all symbols within are removed)

---

## Phase 6 — Approval Gate

**Hard stop. Do not modify any file before this gate.**

Present the following prompt and wait for the user's selection:

```
┌─────────────────────────────────────────────────────┐
│  DEAD CODE REMOVAL — SELECT AN OPTION               │
├─────────────────────────────────────────────────────┤
│                                                     │
│  A) Remove ALL dead code in safe order              │
│  B) Remove specific items (provide list)            │
│  C) Remove by category only (specify categories)   │
│  D) Report only — make no changes                   │
│                                                     │
│  Suggestions are never applied automatically.       │
│  Select A, B, C, or D:                              │
└─────────────────────────────────────────────────────┘
```

- **Option A**: Apply all removals in the safe order from Phase 5e.
- **Option B**: User provides item references (file:line or function
  names); remove only those, still following safe order within the
  subset.
- **Option C**: User names one or more categories (e.g., "unused
  imports" and "dead tests"); remove all items in those categories.
- **Option D**: Deliver the report with no file modifications.

After applying changes (A, B, or C):
1. Run the project's lint and test suite.
2. Report which checks passed and which failed.
3. If tests fail, surface the failures and stop — do not auto-revert.

---

## Decision Rules

| Rule | Detail |
|---|---|
| **No changes before the gate** | Never modify a file before Phase 6 approval. No exceptions. |
| **Low-confidence items always surfaced** | Never silently omit uncertain items. Call them out with `Confidence: LOW`. |
| **Unresolvable targets flagged, not guessed** | `eval`, reflection, and string dispatch create `UNRESOLVABLE` targets. Mark and move on. |
| **Library exports handled conservatively** | Exports with possible external consumers get `UNUSED EXPORT (external consumers possible)`, never `dead`. |
| **Test-exercised code is not dead** | Goes in the Test-Only section, not the dead code list. |
| **Suggestions are correctness/soundness only** | No style comments, formatting notes, or naming preferences in the Suggestions section. |
| **Call graph ≤70 chars wide** | Collapse large subtrees with `[... N functions]`. Hard limit. |
| **Scope check on large codebases** | If the codebase cannot be fully traced, ask the user to scope to a subsystem before continuing. |
| **Safe removal order respected** | Even for Option B/C, removals follow the topological sequence to avoid cascading errors. |
