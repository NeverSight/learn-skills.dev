---
name: review
description: Review one completed feature against durable project intent with focused specialists and independent checks, then prepare candidates for Acceptance.
---

# Review

Review one completed feature in a fresh context. Derive intended behaviour and constraints from the Feature Brief, linked PDRs and ADRs, and relevant Direction and Context documents. Inspect the Implementation commit, tests, affected callers and callees, and integration paths as evidence. Do not use current code to define what the feature was supposed to do. The Design commit only marks the start of the implementation diff. A difference from Design code is not itself a finding. Do not use the Implementation conversation or its check reports as evidence.

## Establish the reviewed snapshot

Record the feature ID, Design commit SHA, and Implementation commit SHA. Confirm the checked-out revision matches the Implementation commit and the tracked working tree is clean, or use an isolated checkout. Review that immutable commit and compare it with the Design commit. Follow affected callers, callees, types, state, and integration paths when the change can affect them. Do not audit unrelated code.

Independently run the repository's configured compile or type check, complete test suite, lint, formatting check, and other relevant mechanical checks against the reviewed commit. Use check-only commands. If a check would modify the implementation tree, run it in isolation or record it as incomplete. Run mechanical prose checks on changed documentation and comments embedded in source files. If the checker cannot inspect source comments directly, extract the changed comments and check that text. Record comment coverage as incomplete when neither method works. Report failed or incomplete checks with evidence; do not repair the feature. The prose specialist separately evaluates comment meaning and usefulness.

## Dispatch focused specialists

Use several narrow subagents. Give each the same feature, durable artifacts, snapshot, and change boundary, but only its own review responsibility. Run them in batches when capacity is limited. A specialist returns evidence-backed candidate findings and does not edit production code or propose fixes.

1. **Feature behaviour and tests:** Compare stories and acceptance criteria with observed behaviour. Find missing or extra behaviour, weak tests, important failures, and edge cases. Identify the regression each important test detects. Recheck affected old tests.
2. **Correctness and integration:** Check algorithms, conditions, state transitions, errors, cleanup, callers, callees, protocols, and compatibility.
3. **Types and boundaries:** Check type safety, domain distinctions, invalid states, ownership, and parsing of weak input at trust boundaries. Check constructors that could bypass invariants.
4. **Simple code:** Read [simple-code](../simple-code/SKILL.md) and give this exact path to the specialist. Apply it to the changed responsibilities, data and control flow, dependencies, effects, abstractions, duplication, and reasoning cost. Require a concrete consequence instead of a style preference.
5. **Prose and comments:** Check changed documentation and comments against code and durable decisions. Find stale, misleading, redundant, or unclear prose. Preserve comments that explain non-obvious intent. Cite an applicable project style rule when one exists.

Add separate specialists for security, concurrency, persistence or lifecycle, protocol compatibility, or domain-specific risks when the feature exposes them. Keep each specialist within the feature's impact. Record missing required coverage as incomplete, not clean.

The test specialist may introduce a deliberate fault only when a critical test's effectiveness is unclear. Use an isolated disposable workspace, record the fault and result, and discard the workspace. Skip this check when isolation is unavailable.

## Curate candidates

Each candidate identifies its specialist, exact location, expected and observed behaviour, supporting code or durable contract, plausible consequence, and preliminary impact and severity. Mechanical failures also identify the check and result. Keep supported uncertainty visible. Merge duplicates and omit claims that are unsupported, contradicted, unrelated, or outside the feature's impact. Do not verify findings on Acceptance's behalf, recommend solutions, or decide that the feature is complete.

## Hand off to Acceptance

Before writing, verify that the intended path in `.workflow/review/` is ignored by Git in this project. If it is not, report the project setup problem and do not edit `.gitignore` or write the report. Write one temporary report at `.workflow/review/<feature-id>-<implementation-sha>.md`. Include both commit SHAs, check results, specialist coverage, and retained candidates. The report is workflow state, not permanent project documentation. Acceptance transfers relevant evidence and deletes it. Give the report path for a fresh Acceptance context; do not present unverified candidates directly to the user or continue into Acceptance here.

## End-of-step report

List the report path and any documents changed, or state that none changed.
State that Review is complete, identify the Implementation commit, and summarize
which checks passed, failed, or could not run. Name Acceptance as the next step
for the feature ID. Give a copyable `/clear` command and a separate copyable
prompt that asks for Acceptance using the report path. Do not expose candidate
findings in this message; Acceptance evaluates them first.
