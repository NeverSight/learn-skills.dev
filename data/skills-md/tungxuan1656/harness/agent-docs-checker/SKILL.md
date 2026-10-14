---
name: agent-docs-checker
description: >-
  Check agent-facing specs, plans, decision records, design documents,
  architecture maps, and instruction routes against repository evidence.
  Use for read-only documentation audits, drift checks, and pre-implementation
  consistency or over-engineering review. Report bounded repairs without
  changing files, choosing architecture, or claiming runtime correctness.
---

# Agent Docs Checker

Check whether selected documents support correct implementation with the
smallest process. Read and report only; do not fix documents or source files.

## Inspect proportionally

1. Establish the requested scope and applicable instruction precedence.
2. Read the selected docs and the sources needed to verify their claims:
   relevant code, tests, manifests, schemas, CI, and accepted decisions.
3. Follow links needed for that scope. Do not load every doc or audit unrelated code.
4. Separate intended behavior from observed implementation. A mismatch can be
   an implementation bug or an unmade decision, not necessarily stale prose.
5. Inspect commands before running any check; use only safe read-only checks.

If no files are selected, start at the agent router and requested subsystem.
State coverage and unvisited sources. Do not create an audit report file unless asked.

## Check

- **Specs**: observable behavior, boundaries, edge cases, acceptance; unresolved rules remain questions.
- **Plans**: cover approved acceptance with the smallest complete change; use existing patterns and exact paths/checks.
- **Decisions/design**: distinguish proposed, accepted, superseded, and uncertain choices; preserve rationale and consequences.
- **Architecture**: topology, ownership, dependency direction, and flows match their labelled sources.
- **Routes**: links resolve; one canonical owner per fact; no contradictory or duplicated rules.
- **Freshness**: volatile facts have a source and update trigger; generated sources are reproducible when applicable.
- **Simplicity**: flag abstractions, options, dependencies, phases, or mandatory artifacts without a demonstrated need.

Do not treat every code/docs difference as a defect. Do not require every doc
type, metadata field, diagram, or template section. Missing critical behavior
is a gap; omitted generic prose is not. Do not reject a necessary security,
data-integrity, accessibility, or recovery constraint merely for being complex.

## Report

Findings first, ordered by concrete impact:

- Severity: HIGH (unsafe or wrong implementation), MEDIUM (drift/ambiguity),
  LOW (routing or maintenance friction).
- File and line; conflicting source with file and line when available.
- Evidence labelled `Observed`, `Intended`, `Proposed`, or `Uncertain`.
- Failure that the mismatch can cause; smallest repair or question and its decision owner.

Finish with coverage, commands actually run, and unresolved assumptions. Say
explicitly when no findings are supported. Documentation consistency is not
proof of runtime correctness; never claim tests passed from inspection alone.

## Handoff

- Known owner and bounded repair: `agent-docs-writer`.
- Unclear ownership, hierarchy, or missing canonical source: `agent-docs-architect`.
- Whole operating harness: `harness-review`.

Recommend a handoff; do not invoke it or make product/architecture decisions
without approval. When a companion is unavailable, return the precise repair
boundary or open question instead of requiring installation.
