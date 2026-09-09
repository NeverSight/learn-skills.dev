---
name: implement-small-change
description: Implement narrowly scoped code changes with focused validation. Use for small bug fixes, tweaks, and features.
disable-model-invocation: true
---

# Implement Small Change

Use the smallest workflow that can prove the requested behavior without hiding risk.

## 1. Establish the boundary

Before editing:

1. Read the applicable repository instructions and inspect the current Git status/diff. Preserve unrelated user changes.
2. State the requested observable outcome in one sentence and identify the smallest check that could prove it.
3. Discover the repository before deciding that the change is small. Prefer the user's currently available local MCP or other repo-aware tools over the agent's built-in file search:
   - If a codebase knowledge graph MCP is available, use it first. If the repository is not indexed, complete that tool's required indexing or setup before querying it; then prefer its graph search, dependency or caller tracing, targeted code retrieval, and architecture or relationship queries to establish the affected symbols and blast radius.
   - If another local repo-aware MCP or repository navigation tool is available, use it before `rg`, globbing, or broad file reads.
   - Fall back to the agent's built-in tools only when no suitable MCP/repo-aware tool is available, or when those tools return insufficient, stale, or inapplicable results. Built-in search remains appropriate for string literals, configuration, scripts, and other non-code files that the graph does not model.
   - Follow repository-specific discovery instructions and use the strongest available source of evidence; do not assume a tool is available merely because it is named in documentation.
4. Locate the exact symbols or configuration involved. Inspect relevant callers, callees, tests, contracts, and runtime path using the selected discovery tools.
5. Classify semantic impact. Do not classify by file count alone; a one-line shared-contract change can be broad, while several colocated files can still be one local change.

Do not ask the user for facts that can be discovered from the repository, runtime, logs, or tools.

## 2. Apply the scope gate

Continue in the fast lane only when all of these are true:

- The request has one clear behavior and an unambiguous expected result.
- The affected callers and downstream behavior are understood.
- The change stays within one module or established seam.
- A focused check can detect the requested behavior or original bug.
- The change is easy to reverse and does not perform destructive or external state changes.
- No hard-stop condition below applies.

Treat any one of these as a hard stop:

- The change crosses presentation, API, domain, persistence, or infrastructure layers in a way that requires a new decision.
- It changes a public API, serialized shape, event, shared contract, database schema, migration, or compatibility promise.
- It touches authentication, authorization, security, privacy, payments, transactions, concurrency, cache invalidation, or a distributed workflow.
- It introduces or changes a domain term, state transition, invariant, ownership rule, or architectural seam.
- Multiple plausible interpretations would produce different user-visible behavior.
- A shared utility or central path has callers whose impact cannot be bounded quickly.
- The existing system has no trustworthy seam or signal for validating the change.

When a hard stop exposes an unresolved decision or cross-layer behavior:

1. Explicitly tell the user that `$implement-small-change` is pausing because the request has hidden scope.
2. Invoke `$grill-with-docs`.
3. Pass it a concise impact brief containing the requested outcome, discovered symbols and callers, affected layers or contracts, plausible interpretations, and decisions that must be resolved.
4. End this skill's workflow and let `$grill-with-docs` own what happens next.

If the problem is difficult to reproduce or the cause remains uncertain rather than merely ambiguous, hand off to `$diagnosing-bugs`.

## 3. Make the smallest coherent change

- For a bug, run the focused check against the original symptom before editing whenever practical. Prefer a fast, deterministic, red-capable repro.
- For a tweak or small feature, implement one minimal vertical slice through the existing interface.
- Add a regression test when a correct existing seam can express the behavior cheaply. Do not create a testing framework, mock internals, or add a shallow test merely to satisfy process.
- Avoid adjacent refactors, speculative abstractions, formatting churn, dependency upgrades, and unrelated cleanup.
- Preserve current public interfaces and domain language unless the requested outcome explicitly requires changing them.
- Stop and re-apply the scope gate if new evidence expands the blast radius.

## 4. Validate proportionately

Run the smallest set of checks that could catch a mistake in this change:

- Re-run the exact bug repro or behavioral check.
- Run the narrowest relevant test file, filter, parser, linter, typecheck, build target, API request, or UI interaction.
- Add an affected project/package build when compilation or static contracts changed.
- Inspect the final diff and status for unintended edits, debug instrumentation, contract drift, and newly discovered hard stops.

Do not run the full test suite or invoke formal `$code-review` by default. Use them when repository instructions require them, the user explicitly requests them, the focused signal is insufficient, or the scope gate proves the change is not actually small.

Do not commit or push unless the user or applicable repository workflow requests it.

## 5. Report the evidence

Report:

- The observable result.
- The root cause for a bug, when established.
- The files or symbols changed.
- The exact validation commands or interactions and their results.
- Any broader checks intentionally not run and why the focused evidence was sufficient.

Never claim the change is safe merely because the diff is small.
