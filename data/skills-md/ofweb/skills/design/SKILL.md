---
name: design
description: Design the code structure for one ready Feature Brief. Align technical choices, express contracts in code, and prepare an accepted baseline for Implementation.
---

# Design

Design is an alignment checkpoint for one ready Feature Brief. Express important types, signatures, boundaries, and stubs before full implementation. Keep this surface small so the user can check understanding and find structural mistakes while changes are cheap. Use agreed behaviour as the contract. Do not change feature scope or implement the complete feature during Design.

## Start from an agreed feature

Confirm that the working tree is clean. Run the repository's full compile, test, lint, format, and prose checks. Record failures and stop if the baseline is not sound. Do not repair or discard unrelated changes within Design.

Read the selected Feature Brief and its relevant Direction, Context, PDR, and ADR links. Confirm that stories and acceptance criteria describe one feature with settled behaviour. Return material behaviour questions to Shape. Read nearby code and tests before choosing new structure. Find the existing owners, representations, call paths, effects, and build conventions.

## Align the technical approach

Trace each significant design element to agreed behaviour or a durable constraint. Check that each important behaviour has a plausible implementation path. Resolve consequential questions about ownership, dependencies, state, persistence, errors, security boundaries, and compatibility with the user. Explain the repository evidence and the decision that work would otherwise make implicitly. Make local, reversible choices directly.

Before writing code, agree on the scope of design changes, the documentation required, and the testing approach. Challenge assumptions and unnecessary structure. Use a dedicated pushback skill when one is available. Record a durable architectural trade-off with `adr-document` when its criteria apply.

## Choose reviewable structure

Read [simple-code](../simple-code/SKILL.md) before choosing the code structure. Apply it to the responsibilities of types and modules, dependency direction, and effect boundaries. Check each abstraction for a concrete current need because Implementation will build around the accepted structure. Prefer readability, then testability, then performance. Let measured latency, memory use, power use, protocol limits, or hardware limits justify a different order for a specific path.

- Give important domain values distinct types when that prevents interchange or repeated explanation. Prefer the simplest type that rules out a meaningful mistake. Ask whether the type removes more concepts from the reader's head than it adds.
- Use sum types for mutually exclusive states. Avoid booleans and optional fields that permit invalid combinations. Keep signatures honest about required inputs, outputs, and distinguishable errors.
- Put parsed domain types in important signatures so Implementation can rely on their invariants.
- Give important decisions callable, deterministic inputs and outputs where practical. Plan effect boundaries that expose I/O without forcing every function into a pure form.
- Make the accepted surface explicit. Leave algorithms, private helpers, local types, and other internal choices to Implementation unless they change that surface.

## Express and check the baseline

Add only the modules, types, signatures, errors, effect boundaries, and selective stubs needed to make the agreed structure clear. State which feature behaviour remains unimplemented. Preserve non-obvious intent in concise comments or links to durable decisions. Do not write a parallel prose implementation plan or a full feature test suite.

Run compile or type checks, existing tests, formatting, lint, and prose checks after the design changes. Confirm that stubs are clear and that Design introduced no failing feature tests. Check that a fresh reader can locate the implementation target from the Feature Brief, code, and linked decisions.

Review important types, valid states, errors, ownership, and effect boundaries with the user. Explain how they express the agreed behaviour. Present the code baseline, ADRs, check results, and remaining constraints for explicit acceptance. A change belongs back in Design when it would have mattered during this review.

After acceptance and passing checks, commit the accepted Design state. Verify that the commit contains only accepted artifacts and record its SHA as the Implementation baseline. Do not hand off until the commit succeeds. The commit marks the implementation diff boundary; durable project decisions and the Feature Brief govern Review. Implementation starts in a fresh context from this commit. If implementation disproves a material design premise, reopen Design and accept a revised baseline before continuing.

## End-of-step report

After the commit succeeds, list the documents and code artifacts changed. State
that Design is complete, name the checks that passed, and give the Design commit
SHA. Name Implement as the next step for the feature ID. Give a copyable
`/clear` command and a separate copyable prompt that invokes `$implement` with
the feature ID and Design commit. Do not present this handoff before acceptance
or when a required check or commit failed.
