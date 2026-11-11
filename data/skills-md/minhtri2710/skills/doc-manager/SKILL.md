---
name: doc-manager
description: Reconcile Markdown documentation with the implementation and produce only source-grounded claims, citing non-obvious facts to path:line and asking when evidence is ambiguous. Use for README, docs, and component Markdown that must match code. If a document contains a setup, release, deploy, or operational runbook, also validate that section through the check-only path in references/runbook-validation.md. Do not use for API-reference generation, product copy, or AGENTS.md/CLAUDE.md.
license: MIT
effort: medium
---

# Doc Manager

Keep in-scope Markdown documentation aligned with the code without filling gaps
with guesses. The deliverable is a documented evidence trail: every non-obvious
claim is cited to `path:line`, every unresolved evidence gap is visible as
`Not-Assessed`, and every runbook section has a safe validation path.

## 1. Establish scope and evidence

- Confirm the requested Markdown files or the repository's documented scope.
  Do not expand into unrelated docs, generated API references, product copy,
  `AGENTS.md`, or `CLAUDE.md`.
- Inventory each in-scope document and each runbook section. Give every document
  a starting status: `unknown`, `runbook`, or `reference`.
- Read the implementation, configuration, scripts, tests, and existing decisions
  that can establish the documented behavior. Treat existing prose as a lead,
  not as evidence for a non-obvious fact.
- Keep a source note for each claim while writing it. A line citation must point
  to the current source and the cited line or range must actually support the
  claim.

The scope pass is complete only when every edited document and every section that
may contain operational steps is listed.

## 2. Reconcile claims

For each claim in scope, choose exactly one outcome:

- **Verified:** retain or write it with an inline citation to the exact source
  path and line or range that supports the claim.
- **Corrected:** replace a stale or contradictory claim with what the current
  evidence shows, then cite the replacement.
- **Not-Assessed:** when evidence is absent, inaccessible, or genuinely
  ambiguous, write `Not-Assessed — <claim or missing evidence>` and ask the
  operator the smallest question that would resolve it. Never turn a plausible
  inference into a fact.

Cite defaults, commands, paths, flags, environment variables, endpoints,
permissions, ordering, failure behavior, and other facts a reader could get
wrong. Use a precise line or range; cite multiple sources when the behavior is
emergent. Re-check existing citations after edits because line numbers move.

When sources disagree, show the conflict and ask rather than silently selecting
one. If the project has an existing decision log, append the answer there with
the date and relevant source; do not create a new decision system merely to
close a documentation task.

## 3. Write and validate

Generate missing Markdown only from verified evidence or an operator's explicit
answer. Reconcile existing Markdown in place when it is in scope. Preserve
useful accurate prose, but do not preserve an unsupported claim as if it were
true: mark it `Not-Assessed` and surface it.

For any document containing setup, release, deploy, migration, or operational
steps, read [references/runbook-validation.md](references/runbook-validation.md)
and apply its check-only contract to the runbook section. Do not load that
reference for ordinary reference documentation.

A runbook validator may inspect local state and perform read-only reachability
checks, but its default path must not write, deploy, migrate, delete, push, send,
or otherwise change external state. Mark actions that cannot be safely checked as
`MANUAL:`. Destructive or outward actions require explicit Human authorization
for the current task; an agent must not treat a command-line flag, a prompt, or
an inferred permission as that authorization.

## 4. Close with checkable status

Before reporting completion:

- every in-scope document is `updated`, `verified-current`, or
  `Not-Assessed` with its open question visible;
- every non-obvious factual claim has a current citation or is marked
  `Not-Assessed`;
- every internal link introduced or changed resolves;
- every runbook section links its check-only validator and each documented step
  maps to a check or `MANUAL:` line;
- validator failures remain visible and are classified as agent-satisfiable or
  operator prerequisites; do not weaken a check to obtain exit 0;
- no destructive or outward action was performed without an explicit Human gate.

Report the documents reviewed, claims corrected or left `Not-Assessed`, checks
run and their exit codes, operator prerequisites, and any unanswered question.
