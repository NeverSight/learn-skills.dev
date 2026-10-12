---
name: simplification-review
description: Review a change in fresh context for a smaller design that still meets the spec.
disable-model-invocation: true
---

# Simplification review

Find unnecessary scope, repeated domain logic, avoidable state, and duplicate tests. Recommend concrete changes that reduce the effort needed to understand and maintain the code.

Prioritize simplicity and elegance while preserving required behavior.

A review can finish with no findings. A large diff can be justified by its requirements.

Produce a review. Make code changes only when the user also requests them.

## 1. Establish fresh context

Use a reviewer session that did not implement the change.

If the current session participated in implementation, start a reviewer with no inherited conversation. Give it:

- This skill.
- The repository path and review target.
- The spec, accepted requirements, and user constraints.
- Pointers to applicable repository instructions and domain documentation.

Let the reviewer form its assessment from those sources and the code.

If a fresh session cannot be started, provide a ready-to-use review prompt and state that the independent review is pending.

This step is complete when the reviewer has the required inputs without the implementation conversation.

## 2. Establish repository context and the review boundary

Read the spec and resolve the comparison base, target commit, and any uncommitted changes included in the request.

Read applicable agent-facing documentation in full:

- Root `AGENTS.md` and `CLAUDE.md`.
- Instructions in ancestor directories and subdirectories that govern changed files.
- Instructions governing affected callers or locations proposed for moved code.
- Root `GLOSSARY.md` where available. If root `GLOSSARY-MAP.md` exists, also read it and the relevant context glossaries.
- Documents referenced by those instructions.

Use the repository's domain terms. Adopt its documented conventions as the starting point for the review. Identify compatibility, migration, security, and operational constraints that explain apparent complexity.

Evaluate the conventions themselves when they contribute to complexity. A useful simplification may require an exception, a revised convention, or work beyond the documented approach.

For each such suggestion, cite the relevant instruction and flag the departure. Explain why the alternative is simpler, what behavior it preserves, and its tradeoffs. Present the recommendation for the developer to decide. Keep the recommendation distinct from authorization to change the code or documentation.

Build a complete changed-file inventory and map it to requirements and implementation areas. Account for frontend, backend, shared types, persistence, tests and fixtures, build and deployment tooling, and documentation wherever they appear in the diff. Record missing requirements as uncertainty. Confirm a change is unnecessary before proposing its removal.

Use that map to find relevant skills in the available catalog and [Greg's skills repository](https://github.com/GregM1991/skills). Prefer an available local checkout; otherwise inspect the relevant files in the repository. Read selected `SKILL.md` files in full.

For React changes, consider `review-react-codebase-red-flags` for maintainability, `improve-frontend-architecture` for module boundaries, `react-performance-guidelines` for state and update paths, and `build-react-codebase-guidelines` for implementation conventions.

Default to at most four optional skills. Use fewer when they cover the review's questions. Read mandatory repository instructions and their required references regardless of this budget.

This step is complete when every changed area is accounted for, applicable documentation has been read, and the behavior to preserve is explicit.

## 3. Examine the design

For large diffs spanning several areas, use up to three specialist scouts when they improve coverage. Split the work by area, such as frontend, backend, and tests/tooling. Give each scout the fixed comparison, its file scope, the accepted requirements, and pointers to applicable instructions and skills. Ask for code evidence, candidate simplifications, and coverage gaps.

The lead reviewer covers remaining areas, checks interactions between areas, and verifies scout findings against the code before including them in the final review.

Read the changed code and enough surrounding code to verify each candidate finding.

Check each area through these questions:

| Area | Questions |
| --- | --- |
| Scope | Which changes are required by the spec? Which can leave this change without breaking acceptance criteria or a required dependency? |
| Domain logic | Where does the same rule have multiple owners? Can one existing operation own validation, transitions, or persistence? |
| State | Which values can be derived? Which state copies require synchronization? Can the model represent fewer invalid combinations? |
| Frontend | Are component boundaries, props, hooks, forms, and state ownership easy to follow? Where do UI paths repeat commands or presentation rules? Can they share an owner while preserving interaction, selection, and Undo behavior? |
| Tests | What behavior and failure boundary does each test protect? Which tests repeat that protection without adding a distinct case? |

Also inspect helpers, wrappers, and configuration introduced by the change. Check whether they reduce caller complexity or distribute one operation across more places.

When implementations look duplicated, compare their validation, provenance updates, state transitions, and error handling. Trace differences to requirements to distinguish intentional policy from accidental inconsistency. A shared implementation must preserve each caller's required behavior. For test removal, identify the coverage that remains.

Distinguish complexity introduced by the change from existing complexity it merely touches.

This step is complete when each changed area has been checked or recorded as unreviewed with a reason. When the diff includes frontend work, record its coverage explicitly, even if it produces no findings.

## 4. Verify the proposed simplifications

For each candidate:

- Cite the concrete code locations and current behavior.
- Describe the smaller design, including what is removed and what owns the remaining behavior.
- Trace the proposal against the acceptance criteria and relevant callers.
- Explain the reduction in rules, state, dependencies, or coordination.
- Identify the checks needed to confirm behavior is preserved.
- State migration costs, tradeoffs, and unresolved assumptions.

Use a small isolated experiment when it can resolve uncertainty about a behavioral difference. Keep it separate from application data and source changes. Record the inputs, result, and limits of what it proves. An isolated result supports only the behavior it exercises.

Retain findings whose benefit exceeds the complexity of making and maintaining the change. Prefer an existing operation when it already owns the required behavior.

Keep promising ideas that need more evidence or a design decision as exploration tasks. Record the code evidence, unresolved question, smallest useful investigation, and decision needed from the developer.

Treat line counts as supporting evidence. Preserve required validation, compatibility, and distinct test coverage.

This step is complete when each candidate is a supported recommendation, an exploration task, or a rejected idea with a reason.

## 5. Return the review

Start with whether the change has material simplification opportunities. Rank supported recommendations by expected benefit and change risk. Include the evidence, design, behavior to preserve, tradeoffs, and validation from step 4. Flag departures from repository guidance as described in step 2.

Present exploration tasks separately. Follow up with the developer using a specific question, the viable options, and a recommended next step. Make clear what must be resolved before the idea is ready to implement.

State the reviewed base and target, coverage gaps, and which claims were verified from code or execution. If no material simplification is justified, say so.

This step is complete when the developer has the review and specific questions for any unresolved decisions.
