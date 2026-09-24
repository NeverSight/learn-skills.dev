---
name: code-review
description: |
  Performs a structured, comprehensive code review of git changes.
  Detects stack and architecture automatically, applies relevant
  stack/pattern-specific rules, and reports findings by severity.
  Use when: user runs /code-review, /review-pr, or asks to "review my changes".
author: felipereis
version: 1.0.0
date: 2026-03-11
---

# Code Review

## Step 0 — Scope Selection

Before anything else, ask the user the following question and wait for their answer:

---

**What would you like to review?**

1. **Uncommitted changes** — files modified but not yet staged or committed (`git diff HEAD`)
2. **Staged changes only** — files added to the index but not yet committed (`git diff --cached`)
3. **Current branch vs base branch** — all commits introduced by this branch compared to its merge base (e.g. `git diff main...HEAD`)
4. **A specific commit** — changes introduced by a single commit (provide the commit hash)
5. **A commit range** — changes across a range of commits (provide `<from>..<to>`)

*Type the number of your choice. For options 4 or 5, also provide the commit hash or range.*

---

Once the user answers, run the appropriate git command to obtain the diff, then proceed with the review below.

| Choice | Command to run |
|--------|---------------|
| 1 | `git diff HEAD` |
| 2 | `git diff --cached` |
| 3 | Ask: *"What is the base branch? (e.g. main, develop)"* — then run `git diff $(git merge-base HEAD <base-branch>)...HEAD` |
| 4 | `git show <commit-hash>` |
| 5 | `git diff <from>..<to>` |

---

Findings should be reported with severity levels:

- **Critical**: blocks the merge; must be fixed before merging
- **Warning**: should be fixed shortly after merging; not a blocker
- **Suggestion**: optional improvement; does not block merge

---

## Step 1 — Codebase Investigation

Before reviewing anything, identify the project's stack by inspecting the following files (read only what exists):

- `package.json` → identifies JS/TS frameworks, bundlers, and tools
- `composer.json` → identifies PHP frameworks (Laravel, Symfony, etc.)
- `pyproject.toml` / `requirements.txt` / `setup.py` → Python
- `go.mod` → Go
- `*.csproj` / `global.json` → .NET / C#
- `pom.xml` / `build.gradle` → Java / Spring Boot
- `pubspec.yaml` → Flutter / Dart
- `vite.config.*` / `webpack.config.*` → bundler and frontend stack
- `tailwind.config.*` → Tailwind CSS
- `tsconfig.json` → TypeScript
- `Dockerfile` / `docker-compose.yml` → Docker
- `*.tf` → Terraform / IaC
- Top-level directory structure → architecture pattern signals (DDD, Clean Architecture, etc.)

Based on what you find, load and apply **only** the stack and pattern files that match this project. Do not evaluate or report on technologies not present.

> **API Validation:** Before flagging a misuse of a library API, validate the syntax and best practice against live docs using `mcp__plugin_context7_context7__query-docs` for the version detected in `package.json` or `composer.json`. Avoids false positives from outdated training data.

**Stack files to load if relevant:**

Read these files using the path relative to this skill file's directory. If a file cannot be read, continue with the generic rules above.

- `./stacks/laravel.md`
- `./stacks/vue.md`
- `./stacks/nuxt.md`
- `./stacks/react.md`
- `./stacks/angular.md`
- `./stacks/svelte.md`
- `./stacks/typescript.md`
- `./stacks/tailwind.md`
- `./stacks/node.md`
- `./stacks/python.md`
- `./stacks/go.md`
- `./stacks/java-spring.md`
- `./stacks/dotnet.md`
- `./stacks/react-native.md`
- `./stacks/flutter.md`
- `./stacks/docker.md`
- `./stacks/terraform.md`
- `./stacks/kafka.md`
- `./stacks/inertia.md`
- `./stacks/pest.md`

**Pattern files to load if relevant:**

Read these files using the path relative to this skill file's directory. If a file cannot be read, continue with the generic rules above.

- `./patterns/clean-architecture.md`
- `./patterns/ddd.md`
- `./patterns/event-driven.md`
- `./patterns/microservices.md`
- `./patterns/cqrs.md`

---

## Step 1.5 — Consistency Check

Before flagging any pattern violation, check what the codebase already does. Laravel, Vue, and similar frameworks offer multiple valid approaches — the best choice is the one already established in the project, even if another would be theoretically better. **Inconsistency is worse than a suboptimal pattern.**

- Check sibling controllers, services, components, or tests for established conventions
- If the project already uses a non-standard pattern consistently, follow it — report it as a **Suggestion** at most, not a blocker
- These checklist rules are defaults for when no pattern exists yet, not overrides of working conventions

---

## 1. Security

- **Injection vulnerabilities**: SQL injection, command injection, XSS, LDAP injection
- **Authentication & Authorization**: proper access control checks, no hardcoded credentials, no exposed secrets
- **Input validation & sanitization**: all user inputs validated at system boundaries
- **Sensitive data exposure**: no secrets, tokens, or PII in logs, responses, or source code
- **CSRF protection**: state-changing operations protected against cross-site request forgery
- **Dependency vulnerabilities**: no known CVEs in added/updated dependencies
- **File upload handling**: proper validation of file types, sizes, and storage paths
- **Rate limiting & abuse prevention**: endpoints exposed to the public have appropriate limits
- **Secure defaults**: encryption, HTTPS, secure cookies, proper CORS configuration
- **Mass assignment protection**: objects not blindly accepting all user input fields

---

## 2. Performance

- **N+1 queries**: data access patterns avoid unnecessary repeated queries
- **Indexing**: new queries have proper database indexes to support them
- **Caching**: appropriate use of caching for expensive or repeated operations
- **Pagination**: large datasets are paginated, not loaded entirely into memory
- **Lazy loading vs eager loading**: relationships loaded efficiently for the use case
- **Unnecessary computation**: no redundant loops, recalculations, or re-renders
- **Memory leaks**: no event listeners, subscriptions, or references left dangling
- **Bundle size**: no unnecessarily large dependencies added for small functionality
- **Database transactions**: long-running transactions avoided; transactions scoped minimally
- **Async operations**: I/O-bound work uses async patterns where available

---

## 3. Tests & Coverage

- **New code has tests**: all new public methods/endpoints have corresponding tests
- **Edge cases covered**: null values, empty collections, boundary conditions, error states
- **Happy path and sad path**: both success and failure scenarios tested
- **Test isolation**: tests don't depend on each other or on external state
- **Mocking**: external services and I/O properly mocked; no real API calls in unit tests
- **Assertions are meaningful**: tests assert behavior, not implementation details
- **Coverage**: no significant drop in test coverage percentage
- **Regression tests**: if fixing a bug, a test exists that would have caught it

---

## 4. Architecture & Design Principles

### SOLID
- **Single Responsibility**: each class/module/function does one thing well
- **Open/Closed**: code is extendable without modifying existing behavior
- **Liskov Substitution**: subtypes can replace their base types without breaking behavior
- **Interface Segregation**: interfaces are small and focused, not bloated
- **Dependency Inversion**: high-level modules depend on abstractions, not concrete implementations

### DRY (Don't Repeat Yourself)
- No duplicated logic across files or methods — extract shared behavior when duplication introduces a risk of inconsistency

### KISS (Keep It Simple, Stupid)
- Solution uses the simplest approach that works; no over-engineering
- No premature abstractions or unnecessary design patterns

### General
- **Separation of concerns**: business logic, data access, and presentation are clearly separated
- **Naming conventions**: variables, functions, and classes have clear, descriptive names
- **Error handling**: errors are handled gracefully with meaningful messages; no silent catches
- **Code readability**: code is self-documenting; complex logic has brief explanatory comments
- **No dead code**: unused imports, variables, functions, or commented-out blocks are removed
- **Consistent patterns**: new code follows the patterns already established in the codebase
- **Immutability**: prefer immutable data structures where appropriate; avoid mutating shared state
- **Pure functions**: side effects isolated and explicit; core logic written as pure functions where possible

### Code & File Size
- **Method/function length**: methods exceeding **30 lines** should be justified; methods exceeding **50 lines** require refactoring — they are doing too much (Clean Code / Rule of 30)
- **Class length**: classes exceeding **200 lines** should be reviewed for single-responsibility violations; classes exceeding **500 lines** require decomposition
- **File length**: source files exceeding **300 lines** are a signal of multiple responsibilities; files exceeding **500 lines** should be investigated and split
- **Component length** *(Vue/React)*: SFCs or components exceeding **300 total lines** should be decomposed; `<template>` and `<script>` blocks each kept under **150 lines** where possible
- **Binary files in git**: images, PDFs, videos, database dumps, and compiled binaries not committed to the repository; `.gitignore` covers them; Git LFS used for large assets that must be versioned
- **File reading at runtime**: files read from disk using streaming (not loaded entirely into memory) when the file size is not bounded and could be large

---

## 5. Potential Bug Investigation

Actively trace the modified code looking for latent bugs — do not just check style or structure. For each item below, reason through the changed code paths and report anything that could produce incorrect behavior, data corruption, or a runtime failure.

- **Null / undefined / zero dereference**: identify paths where a variable could be `null`, `undefined`, `0`, or an empty collection at the point it is used without a guard
- **Off-by-one errors**: check loop bounds, slice indices, pagination offsets, and comparisons using `<` vs `<=`
- **Inverted or incomplete conditions**: logic conditions that appear reversed (`!==` where `===` was intended), missing `else` branches, or `switch` cases without a `default`
- **Implicit assumptions about state**: code that assumes a record exists, a list is non-empty, a value has already been set, or a previous step has succeeded — without verifying
- **Broken contracts with dependents**: changes to a method signature, return shape, event payload, or database column that are not reflected in all callers, consumers, or downstream modules
- **Race conditions in async flows**: multiple async operations that share state and could interleave in a way that produces inconsistent results
- **Data mutation side effects**: functions that mutate their input arguments, shared collections, or global state in ways that callers do not expect
- **Query / migration data hazards**: SQL changes that could silently drop data, produce incorrect results on existing rows, or behave differently on empty vs non-empty tables
- **Error paths that silently succeed**: catch blocks that swallow exceptions and return a success response; missing re-throws; errors logged but not propagated
- **Type coercion surprises**: implicit type coercions (PHP loose comparisons, JavaScript `==`, string-to-number) that could produce wrong results at the boundary of the changed code
- **Unreachable or dead logic**: conditions that can never be true given the surrounding context; code after an unconditional `return`; branches that contradict earlier guards

---

## 6. Accessibility *(only if the diff includes frontend/UI changes)*

- **Semantic HTML**: correct use of headings, landmarks, lists, buttons, and form elements
- **ARIA attributes**: `aria-label`, `aria-describedby`, `role`, etc. used correctly and only when native semantics are insufficient
- **Keyboard navigation**: all interactive elements reachable and operable via keyboard
- **Focus management**: focus order is logical; focus traps used appropriately in modals/dialogs
- **Color contrast**: text and UI elements meet WCAG AA contrast ratios
- **Images & icons**: meaningful images have `alt` text; decorative images use `alt=""`
- **Form labels**: all inputs have associated `<label>` or `aria-label`

---

## 7. Observability

- **Structured logging**: logs use a structured format (JSON or key=value); no `console.log` / `var_dump` left in production code
- **Sensitive data in logs**: no passwords, tokens, PII, or secrets logged — even partially
- **Log levels**: appropriate log levels used (`debug`, `info`, `warning`, `error`); no critical events logged at `debug`
- **Correlation IDs**: requests and async jobs carry a trace/correlation ID through logs
- **Error reporting**: exceptions are captured and forwarded to the error tracking system (e.g. Sentry, Bugsnag)
- **Metrics**: significant new operations (queue jobs, external calls, cache hits) are instrumented where relevant

---

## 8. API Design *(only if the diff includes API endpoints or API client code)*

- **HTTP methods**: correct verbs used (`GET` for reads, `POST` for creation, `PUT`/`PATCH` for updates, `DELETE` for removal)
- **Status codes**: correct HTTP status codes returned (`201` for creation, `204` for no content, `422` for validation errors, `404` for not found, etc.)
- **Versioning**: API version is reflected in the URL or header; breaking changes bump the version
- **Consistent error responses**: error payloads follow a uniform structure across all endpoints
- **Pagination**: consistent strategy used (cursor or offset); metadata included in response
- **Filtering & sorting**: query parameters follow established conventions
- **Idempotency**: `PUT`/`PATCH`/`DELETE` operations are idempotent; `POST` operations are idempotent where appropriate (e.g. with idempotency keys)
- **No sensitive data in URLs**: tokens, passwords, and PII passed in headers or body, not in query strings or paths
- **GraphQL** *(only if project uses GraphQL)*: N+1 prevented with DataLoader, query depth limited, introspection disabled in production, mutations validate input

---

## 9. Resilience & Fault Tolerance *(only if the diff involves external calls, queues, or critical flows)*

- **Timeouts**: all outbound HTTP calls, database queries, and queue operations have explicit timeouts
- **Retry with backoff**: transient failures retried with exponential backoff and jitter; non-retriable errors not retried
- **Circuit breakers**: repeated failures to an external dependency trip a circuit breaker to prevent cascade
- **Graceful degradation**: the system degrades gracefully when a non-critical dependency is unavailable
- **Idempotency**: operations that may be retried are idempotent (safe to execute more than once)
- **Bulkhead isolation**: slow or failing dependencies do not exhaust shared resources (thread pools, connections)

---

## 10. Zero-Downtime Database Migrations *(only if the diff includes migrations)*

- **Additive changes first**: new columns added as nullable or with a default before application code uses them
- **No instant NOT NULL without default**: adding a NOT NULL column without a default on a large table causes a full table lock
- **Column/table rename safety**: old column kept alongside new one during a transition period; renamed in a follow-up migration after code is deployed
- **Column removal safety**: column removed only after code no longer references it and the deployment is stable
- **Index creation**: indexes on large tables created concurrently (e.g. `CREATE INDEX CONCURRENTLY`) to avoid locking
- **Reversibility**: `down` method correctly undoes the `up` method without data loss

---

## 11. Concurrency & Thread Safety *(only if the diff involves shared state, background jobs, or concurrent operations)*

- **Race conditions**: operations on shared state are atomic or properly synchronized
- **Locks & mutexes**: locking strategy is correct; no deadlock potential (consistent lock ordering)
- **Atomic operations**: counters and flags updated atomically (e.g. database atomic increments, compare-and-swap)
- **Job uniqueness**: background jobs that must not run concurrently are protected by a unique lock
- **Shared mutable state**: global or static mutable state avoided; dependencies injected rather than shared

---

## 12. Internationalization (i18n) *(only if the project supports multiple languages or locales)*

- **No hardcoded strings**: all user-facing text uses translation keys, not inline strings
- **Date & time formatting**: dates, times, and durations formatted via locale-aware utilities, not manual string building
- **Number & currency formatting**: numbers and currency amounts formatted according to the user's locale
- **Pluralization**: plural forms handled correctly via i18n library, not with manual conditionals
- **RTL support**: layout does not break for right-to-left languages if RTL is supported
- **Locale in URLs or headers**: locale derived from user preference or `Accept-Language`, not hardcoded

---

## 13. Privacy & Data Compliance *(only if the diff involves user data, PII, or data storage)*

- **Minimal data collection**: only data strictly necessary for the feature is collected and stored
- **PII handling**: personal data identified, encrypted at rest where required, and access-controlled
- **Data retention**: data is deleted or anonymized according to defined retention policies
- **Consent**: data collection requiring user consent is gated behind explicit opt-in
- **Audit trail**: access to and modification of sensitive data is logged for audit purposes
- **Third-party data sharing**: data shared with external services is documented and limited to what is necessary

---

## 14. What Was Done Well

Before listing issues, acknowledge what was done well in this change. Point out strong design decisions, good test coverage, clean abstractions, or anything that should be recognized and repeated.

---

## 15. Output Format

For each finding, report:

```
### [Category] — [Severity]

**File:** `path/to/file.ext:line`
**Issue:** Brief description of the problem.
**Fix:** Suggested correction or approach.
```

At the end, provide a summary table covering all evaluated categories (use N/A for categories that do not apply to this change):

```
## Summary

| Category              | Critical | Warning | Suggestion | N/A |
|-----------------------|----------|---------|------------|-----|
| Security              | 0        | 0       | 0          |     |
| Performance           | 0        | 0       | 0          |     |
| Tests/Coverage        | 0        | 0       | 0          |     |
| Architecture          | 0        | 0       | 0          |     |
| Code & File Size      | 0        | 0       | 0          |     |
| Potential Bugs        | 0        | 0       | 0          |     |
| Accessibility         | 0        | 0       | 0          |     |
| Observability         | 0        | 0       | 0          |     |
| API Design            | 0        | 0       | 0          |     |
| Resilience            | 0        | 0       | 0          |     |
| DB Migrations         | 0        | 0       | 0          |     |
| Concurrency           | 0        | 0       | 0          |     |
| i18n                  | 0        | 0       | 0          |     |
| Privacy/Compliance    | 0        | 0       | 0          |     |
| Architecture Patterns | 0        | 0       | 0          |     |
| Stack-Specific        | 0        | 0       | 0          |     |
| **Total**             | **0**    | **0**   | **0**      |     |
```

If no issues are found, state: **"Code review passed — no issues found."**
