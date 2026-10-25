---
name: requirements-definition
description: "Turns a vague interface brief into numbered, testable requirements with explicit assumptions and open questions. Use when a brief must be made precise before design or review, or when existing requirements are untestable or conflicting."
---

# Requirements Definition

## Purpose
Turn a vague or partial interface brief into numbered, testable requirements with explicit assumptions and open questions, so later design and review work has a stable reference.

## When to use
- Use when: a brief, request, or idea must be made precise before design or review begins.
- Use when: existing requirements are untestable, conflicting, or mix goals with solutions.
- Do not use when: requirements are already numbered, testable, and agreed; refine them in place instead.

## Inputs
- Required: the brief, request, or source material describing the desired interface or outcome.
- Optional: target users, platforms, business or technical constraints, existing product context, applicable standards or policies.
- Assumptions: none may be silently added; unknowns are recorded as assumptions or open questions.

## Process
1. Extract stated goals, users, tasks, constraints, and success signals from the input. Quote or cite the source of each.
2. Separate each item into a goal (outcome), a requirement (binding condition), a constraint (limit on solutions), or a preference (non-binding).
3. Rewrite each requirement as one observable, testable statement with a unique ID (R1, R2, …). Split compound statements.
4. Identify solution statements disguised as requirements; restate the underlying need, and keep the solution only as a labeled constraint if it is truly mandated.
5. Detect conflicts, gaps (for example no error handling, no accessibility target, no platform), and ambiguous terms. Record each as an open question with the decision it blocks.
6. Where work must proceed without an answer, record a bounded assumption and the consequence if it is wrong.
7. Assign priority (Must, Should, Could) only where the source states or clearly implies importance, and cite it. Otherwise write Unspecified and, if the missing priority blocks scope or order, add an open question for the owner. Never choose a priority just to fill the field.

## Rules and heuristics
- Required: every requirement is verifiable by observation, measurement, or inspection; state how.
- Required: never present an assumption as a requirement or a preference as a binding condition.
- Required: preserve requirements that come from applicable standards or policy and cite their authority.
- Required: a priority the source does not support is recorded as Unspecified, not guessed. A requirement inferred rather than stated is labeled as an inference in its source.
- Recommended: write from the user's or system's outcome ("a user can …") rather than from a component.
- Recommended: keep the set small and non-overlapping; merge duplicates.

## Checks
- Every requirement has an ID, a priority (or Unspecified with the reason), a source, and a verification method.
- No requirement names a specific technology, tool, or visual solution unless it is a labeled constraint.
- Conflicts and gaps found in step 5 are each recorded, not resolved by guesswork.
- Each assumption states its consequence if wrong.

## Output
Return a requirements set containing: numbered requirements (ID, statement, priority, source, verification), constraints, assumptions with consequences, open questions with the decisions they block, and explicit non-goals. Use the [requirements set](templates/requirements-set.md).

## Completion criteria
- Every item in the input is represented as a requirement, constraint, assumption, preference, question, or non-goal.
- Requirements are numbered, testable, and traceable to a source.
- Unresolved questions are listed rather than answered by invention.
