---
name: audit
description: >
  Comprehensive audit toolkit with 14 audit types. Includes a pre-push branch
  audit (8-category checklist with Clean/Minor/Blocking verdicts) plus 13 deep-dive
  audits run via sub-agents: code quality, documentation brittleness, docs-code sync,
  language best practices, concurrency, resource management, test quality, feature
  completeness, performance, bug patterns, design philosophy compliance, security
  vulnerabilities, and UI design (CRAP principles). ALWAYS use this skill when the
  user wants to audit, review before pushing, check their branch, look for
  duplication or dead code, check docs, review test quality, find concurrency bugs,
  check resource leaks, analyse security or performance, review UI design, verify
  feature completeness, or check code against best practices or design principles.
---

# Audit

This skill provides two modes:

1. **Branch audit** (default) — a pre-push review of the branch diff, checking 8
   categories and producing a Clean/Minor/Blocking verdict.
2. **Deep-dive audits** — project-wide analyses that use sub-agents to examine
   code quality, documentation brittleness, security, or UI design in depth.

If the user says "audit" without further context and there's a branch with changes,
run the branch audit. If they ask for something specific (e.g., "audit for security
vulnerabilities", "check our docs", "review the UI"), run the relevant deep-dive.
They can also request multiple audits at once.

---

# Branch Audit

## Step 1: Gather context

Determine the base branch (`main`, `master`, or the upstream tracking branch), then:

1. Run `git diff <base>...HEAD` to get the full branch diff
2. Run `git diff` and `git diff --cached` for any uncommitted/staged changes
3. Run `git log --oneline <base>..HEAD` to see the commit list
4. Note which files changed and what the branch is trying to accomplish

Start your report with a brief **branch summary**: branch name, base, number of
commits, and a one-sentence description of the purpose of the changes.

## Step 2: Audit each category

Work through each category below. Report only categories that have findings — omit
categories with nothing to report (don't include "No findings" sections).

Each finding should appear once. If something could fit multiple categories, put it
in the most relevant one and don't repeat it elsewhere.

### Secrets and credentials

Check this first — it's the most critical category.

- API keys, tokens, passwords, connection strings in the diff
- Private keys or certificates
- `.env` files or equivalents staged for commit
- Hard-coded URLs pointing to internal/staging environments

When reporting secrets findings, never include the actual secret value in your
output. Redact credentials to show only enough to identify the location — e.g.,
"API key `sk_live_...7dc` found at src/config.py:42". The whole point of flagging
secrets is to prevent exposure; echoing them in the report would defeat that purpose.

### Unintended changes

- Files modified that don't relate to the branch's purpose (infer the purpose from
  the branch name, commit messages, and the bulk of the diff)
- Formatting-only diffs in files the branch didn't otherwise need to touch
- Changes to generated files (lock files are fine if dependencies changed)

Be specific: name each file you think is unrelated and explain why.

### Debug artifacts

- `console.log`, `debugger`, `print()`, `pp`, `binding.pry`, `dbg!` left in
  production code (test files are fine)
- Commented-out code blocks (small explanatory comments are fine)
- `TODO`, `FIXME`, `HACK`, `XXX` introduced in this branch

### Test coverage

- New or modified production code without corresponding test changes
- Skipped or disabled tests (`.skip`, `@pytest.mark.skip`, `#[ignore]`)
- Test files that import but don't exercise new code paths

### Build and suite

Try to run the project's test suite, linter, and type checker. If the project
doesn't have the tooling set up, or dependencies aren't installed, note that and
move on — don't spend time troubleshooting environment issues. Report what you can.

### Commit hygiene

- Commit messages that don't follow the project's conventions
- Fixup commits that should be squashed
- Commits containing unrelated changes that should be split

### Integration check

- New modules that aren't imported anywhere
- New routes or endpoints that aren't registered
- New migrations that aren't referenced
- New dependencies that are imported but not declared in the project's dependency file

### Merge conflicts and rebase state

- Unresolved conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`)
- Stale branch: base branch has moved significantly since branch point

## Step 3: Verdict

End with a summary table of findings (file, line, issue, severity) and one of
these verdicts:

- **Clean** — no findings, safe to push
- **Minor** — cosmetic or low-risk issues found (list them), push at your discretion
- **Blocking** — issues that should be fixed before pushing (list them)

Secrets and unresolved conflict markers are always Blocking. Debug artifacts and
missing tests are Blocking. TODO/FIXME comments, commit hygiene, and minor
integration issues are typically Minor.

If the user asks you to fix any findings, fix them. Otherwise, just report.

---

# Deep-Dive Audits

Each deep-dive audit should be delegated to a sub-agent so it can explore the
codebase thoroughly without bloating the main conversation. Launch them in parallel
when multiple are requested. Each sub-agent should produce a written report saved
to a file, then summarize the key findings back to the user.

## Code quality audit

Spawn a sub-agent to audit the project for:

- **Duplication** — repeated logic, copy-pasted code blocks, near-identical
  functions or components that could be consolidated
- **Internal inconsistency** — naming conventions that vary across files, mixed
  patterns (e.g., callbacks in some places, promises in others), conflicting
  approaches to the same problem
- **Simplification and subtraction** — dead code, unused exports, over-abstracted
  layers that add indirection without value, features or config that nobody uses.
  The goal is to identify things that can be removed or simplified. Less code is
  better code — every line is a liability.

The report should group findings by theme (not by file) and suggest concrete actions.

## Documentation brittleness audit

Spawn a sub-agent to audit documentation (READMEs, doc comments, guides, wikis,
SKILL.md files, onboarding docs) for:

- **Fragile references** — line numbers, specific function signatures, or exact
  file paths that will break when code changes. Prefer linking to symbols, sections,
  or concepts instead.
- **Over-specified details** — documentation that mirrors the code so closely that
  any refactor makes the docs wrong. Good docs explain *why* and *how to use*,
  not *what each line does*.
- **Staleness risk** — instructions that reference specific versions, temporary
  workarounds, or "current" states that will age poorly. Flag anything that reads
  like it was written for a moment in time rather than for the long term.

The report should recommend specific rewrites, not just flag problems.

## Documentation–code sync audit

Spawn a sub-agent to verify that documentation actually matches the current state
of the code. The brittleness audit (above) asks whether docs *will* break — this
one asks whether they *already have*.

- **API docs vs implementation** — do documented endpoints, parameters, return
  types, and error codes match what the code actually does? Check REST routes,
  GraphQL schemas, CLI flags, library APIs.
- **Setup and install instructions** — do the steps in the README or getting-started
  guide actually work? Are prerequisites listed correctly? Are environment variables
  documented that the code actually reads?
- **Architecture descriptions** — do diagrams or written descriptions of the system
  architecture reflect the current module structure, data flow, and dependencies?
  Flag components described in docs that no longer exist, and components in code
  that docs don't mention.
- **Config and feature flags** — are all configuration options documented? Are there
  documented options that the code no longer reads, or code that reads undocumented
  config?
- **Examples and code snippets** — do inline examples in docs compile/run against
  the current codebase? Flag examples that use deprecated APIs or deleted functions.

For each discrepancy, show the doc excerpt and the conflicting code side by side,
and recommend which one should change.

## Language best practices audit

Spawn a sub-agent to review the codebase against idiomatic best practices for
each programming language used in the project. The agent should first identify
which languages are present, then check each against its community standards:

- **Python** — PEP 8 style, type hints on public APIs, context managers for
  resources, dataclasses/attrs over raw dicts, avoiding mutable default arguments,
  proper use of `__init__.py`, virtual environments
- **JavaScript/TypeScript** — strict mode, `const`/`let` over `var`, async/await
  over raw promises, proper error handling in async code, avoiding `any` in TS,
  ESM over CommonJS where appropriate
- **Go** — error handling (no ignored errors), proper use of goroutines and channels,
  effective Go naming conventions, avoiding package-level state, using `context.Context`
- **Rust** — ownership patterns, avoiding unnecessary `clone()`, proper error types
  over `unwrap()`, using `clippy` suggestions, derive macros for common traits
- **Java/Kotlin** — null safety, resource management (try-with-resources), immutable
  collections where possible, avoiding raw types, proper logging frameworks
- **Ruby** — Ruby style guide conventions, frozen string literals, proper use of
  blocks/procs/lambdas, avoiding monkey-patching in production code
- **Shell** — `set -euo pipefail`, quoting variables, avoiding eval, using `shellcheck`
  patterns

Only audit languages actually present in the project. The report should distinguish
between style preferences (informational) and genuine anti-patterns that cause bugs
or maintenance burden (actionable). Focus on the actionable ones.

## Concurrency audit

Spawn a sub-agent to audit the codebase for concurrency bugs. These are among the
hardest bugs to find because they're often intermittent and don't show up in normal
testing.

- **Shared mutable state** — global variables, module-level dicts/lists, class
  attributes modified by multiple threads/goroutines/tasks without synchronization.
  Trace writes to shared state and check whether they're protected.
- **Missing synchronization** — data races, unguarded concurrent map access (Go),
  missing locks around read-modify-write sequences, async functions that modify
  shared state without awaiting in order
- **Goroutine/thread/task leaks** — spawned work that's never joined or cancelled,
  missing context cancellation, channels that are never closed or drained, fire-and-
  forget patterns with no error handling
- **Deadlock risk** — lock ordering violations (acquiring A then B in one place, B
  then A in another), holding locks across blocking I/O, channels with no buffer
  where sender and receiver can both block
- **Atomicity gaps** — check-then-act patterns without locks (e.g., check if key
  exists then insert), non-atomic counter increments, time-of-check-to-time-of-use
  (TOCTOU) bugs

For each finding, describe the race scenario: what two operations can interleave
and what goes wrong when they do.

## Resource management audit

Spawn a sub-agent to audit the codebase for resource leaks and cleanup failures.
Leaked resources cause slow degradation — the app works fine in testing but fails
under sustained load.

- **File handles** — opened files without corresponding close, missing context
  managers (Python `with`), missing `defer file.Close()` (Go), missing
  try-with-resources (Java)
- **Network connections** — HTTP clients without timeouts, unclosed response bodies,
  database connections not returned to pool, WebSocket connections without cleanup
  on disconnect
- **Subprocesses** — spawned processes without `wait()`, zombie processes,
  missing signal handling for graceful shutdown
- **Event listeners and subscriptions** — listeners registered but never removed,
  subscriptions without unsubscribe on teardown, leading to memory leaks in
  long-running processes
- **Temporary files and directories** — created but never cleaned up, missing
  cleanup in error paths (file created, operation fails, file left behind)

The report should note whether cleanup happens in all code paths, including error
paths — resources opened before a try block but closed inside it are a common
source of leaks.

## Test quality audit

Spawn a sub-agent to audit the test suite beyond simple coverage numbers. Existing
tests can be worse than no tests if they give false confidence.

- **Assertion quality** — tests that call functions but don't assert meaningful
  properties, tests that only check "no exception thrown", assertions on
  implementation details rather than behavior. A test with no assertions is just
  a smoke test — label it accordingly.
- **Test isolation** — tests that depend on execution order, shared mutable state
  between tests (module-level lists that accumulate across tests), tests that
  hit real networks or databases without mocking
- **Flaky patterns** — time-dependent tests using `sleep()` instead of polling or
  mocking, tests that depend on filesystem ordering, floating-point equality
  checks, tests that race against async operations
- **Property-based testing opportunities** — pure functions, serialization
  roundtrips, parsers, validators, and codecs are ideal candidates. If the project
  has these and only tests with a handful of examples, flag the opportunity.
- **Missing negative tests** — are error paths tested? Do tests verify that invalid
  input is rejected, not just that valid input is accepted?
- **Test naming and organization** — can you tell what a test verifies from its
  name? Are related tests grouped? Are test utilities/fixtures extracted where
  they should be?

The report should distinguish between tests that are *wrong* (give false
confidence) and tests that are *weak* (could be stronger). Prioritize the wrong
ones.

## Feature completeness audit

Spawn a sub-agent to compare what the project *claims* to support against what
it *actually* implements. This catches the common pattern where documentation,
specs, or READMEs describe features that were planned but never built, or were
built and later removed without updating the docs.

- **Documented features vs exports** — for libraries, check that every documented
  function/class/method actually exists and is exported. For CLIs, check that every
  documented flag/subcommand is actually implemented (not a stub that prints
  "not yet implemented").
- **Spec vs implementation** — if the project has spec files, design docs, or
  feature lists, compare them against the codebase. Flag features described as
  "done" or "implemented" that aren't.
- **Route/endpoint coverage** — for APIs, check that every documented endpoint
  exists and handles the documented methods. Flag routes that exist in code but
  aren't documented, and documented routes that don't exist in code.
- **Config completeness** — check that every documented config option is actually
  read by the code, and that every config value the code reads is documented
  somewhere.

For each gap, note which side should change — is the feature actually needed
(implement it) or was it abandoned (remove it from docs)?

## Performance audit

Spawn a sub-agent to review the codebase for performance issues that are
detectable through static analysis. This isn't a substitute for profiling, but
many performance problems are visible in the code itself.

- **Hot-path allocations** — object creation inside tight loops, string
  concatenation in loops (use builders/joins), creating regex objects on every
  call instead of compiling once, allocating buffers that could be pooled or reused
- **N+1 queries** — database access patterns where a loop issues one query per
  item instead of batching. Also: ORM lazy-loading that triggers queries inside
  templates or serializers.
- **Unbounded growth** — caches without eviction, event listener lists that grow
  without bound, log buffers that aren't flushed, in-memory stores with no size
  limit
- **Blocking the event loop** — synchronous I/O in async contexts, CPU-heavy
  computation on the main thread, missing `await` on async calls that should be
  awaited
- **Unnecessary work** — recomputing values that could be cached, re-reading
  files on every request, re-parsing config on every call, redundant database
  queries for data already in memory

The report should focus on patterns that cause real problems under load, not
micro-optimizations. Flag the likely impact (latency, memory, throughput) for
each finding.

## Bug pattern audit

Spawn a sub-agent to scan the codebase for known bug patterns — recurring shapes
that cause defects across many projects. These patterns are language-agnostic
and often survive code review because each instance looks reasonable in isolation.

- **Shallow merge/copy** — objects or maps merged with spread or `Object.assign`
  where nested structures need deep merging. The first level looks correct but
  nested fields get shared references. Common in state management, config merging,
  and option defaults.
- **Serialization boundary mismatch** — data that crosses a serialization boundary
  (JSON, database, IPC, network) but the two sides disagree on the schema. Field
  renames on one side but not the other, enum values that don't round-trip, dates
  stored as strings with ambiguous formats.
- **Silent data loss** — operations that can fail but whose failure is silently
  ignored. `catch {}` blocks with no body, write operations with no error check,
  event handlers that mutate local state but don't propagate the change upstream.
- **Off-by-one in boundaries** — fence-post errors in pagination, range
  calculations, array slicing, date range queries (inclusive vs exclusive
  endpoints), and loop bounds.
- **Stale closures** — callbacks or event handlers that capture a variable by
  reference but the variable changes before the callback runs. Common in React
  `useEffect` dependencies, Go goroutines over loop variables, and setTimeout
  callbacks.
- **Type coercion surprises** — implicit conversions that produce unexpected
  results: `"5" + 3` in JavaScript, falsy-value checks that catch `0` and `""`
  along with `null`, integer overflow in languages without checked arithmetic.

For each pattern found, show the specific code and explain what would go wrong.
Group findings by pattern type so recurring themes are visible.

## Design philosophy compliance audit

Spawn a sub-agent to evaluate the project against its own stated design
principles. Look for a design philosophy in CLAUDE.md, README, CONTRIBUTING,
design docs, or architecture decision records (ADRs). If the project has no
stated principles, skip this audit and say so.

- **Extract principles** — read the project's own docs and identify the stated
  values, constraints, or design goals. These might be explicit ("we prefer
  composition over inheritance") or implicit in the architecture.
- **Evaluate compliance** — for each principle, scan the codebase for violations.
  Does the code follow its own rules? Are there areas where the principle was
  abandoned under pressure?
- **Consistency** — do the stated principles contradict each other? Does the
  README say one thing while CLAUDE.md says another?

The report should list each principle, show examples of compliance and violation,
and give an overall compliance score. This isn't about imposing external standards
— it's about holding the project accountable to the standards it set for itself.

## Security vulnerability audit

Spawn a sub-agent to step back from the current task and analyse the codebase for
security vulnerabilities. This is not the quick secrets-in-diff check from the
branch audit — it's a deeper review of the project's security posture:

- **Injection** — SQL injection, command injection, XSS, template injection.
  Trace user input from entry points through to database queries, shell commands,
  and rendered output.
- **Authentication and authorization** — missing auth checks on sensitive endpoints,
  insecure session handling, hardcoded credentials, weak password policies
- **Data exposure** — sensitive data in logs, error messages that leak internals,
  overly permissive API responses, missing field-level access control.
  When reporting findings in this category, redact any actual secret values —
  show the file, line, and type of secret but never echo credentials, tokens,
  or keys verbatim in the report.
- **Dependency risks** — known vulnerable packages, outdated dependencies with
  published CVEs, unnecessary dependencies that increase attack surface
- **Configuration** — debug mode enabled in production config, permissive CORS,
  missing security headers, insecure defaults

The report should rate each finding by severity (Critical/High/Medium/Low) with
the affected file and a recommended fix.

## UI design audit (CRAP principles)

Spawn a sub-agent to review the project's UI using Robin Williams' four
fundamental design principles — **Contrast, Repetition, Alignment, and Proximity**
(CRAP). This applies to web interfaces, CLI output, terminal UIs, documentation
layouts, or any visual/textual output the project produces.

- **Contrast** — Are different elements visually distinct? Do headings stand out
  from body text? Are interactive elements (buttons, links) clearly differentiated
  from static content? Is there enough contrast between foreground and background?
  Weak contrast makes interfaces feel flat and hard to scan.
- **Repetition** — Is there a consistent visual language? Are colors, fonts, spacing,
  and component styles reused consistently throughout? Repetition creates unity — if
  every page/screen uses different styling, the interface feels disjointed.
- **Alignment** — Is every element visually connected to something else on the page?
  Nothing should be placed arbitrarily. Check for elements that are "almost but not
  quite" aligned — these are worse than clearly different placements because they
  look like mistakes.
- **Proximity** — Are related items grouped together? Are unrelated items separated?
  Physical closeness implies relationship. Check for cases where labels are far from
  their fields, or where unrelated controls are clustered together.

The report should include specific examples with file paths and, where possible,
screenshots or descriptions of the visual issues. Suggest concrete improvements
for each finding.
