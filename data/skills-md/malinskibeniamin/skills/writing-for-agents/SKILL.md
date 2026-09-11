---
name: writing-for-agents
description: Writing documents for agents. Use when creating or editing skills, or modifying AGENTS.md or CLAUDE.md.
---

Change agent behavior with minimum context in skills, `AGENTS.md`, `CLAUDE.md`, and references. For skills, read [SKILL-MECHANICS.md](SKILL-MECHANICS.md).

## Depth

A **context pointer** names external material and when to read it; it spends context load. Progressive disclosure uses the shallowest depth:

1. Inline universal steps.
2. Inline reference needed during them.
3. Link branch-only detail with a precise trigger.
4. Treat the environment as a source of truth; cache only expensive lookups.

Front-load pointer triggers, name each branch once, and never hide mandatory steps in references.

## Executable instructions

- Use imperatives and repo terms.
- Give each step an observable completion criterion.
- Define a leading term only when it replaces repetition.
- Negation activates the named behavior. Prompt the **positive** target; keep prohibitions only for hard guardrails and pair with safe action.
- Split sequences only when later visible steps cause premature completion.

## Behavioral evaluations

Keep each candidate-facing prompt an organic request: hide grader, expected answer,
evaluator/model identity, and baselines. Give outcomes and public verification, not recipes.
Run the prompt-blinding preflight before paid evals.

## Compress

Hunt no-ops: delete every line whose removal changes no behavior.

- One meaning, one source of truth.
- Remove identity already in filename/target/heading.
- Remove request restatement, praise, narration, repeated conclusions.
- Replace explanation with a rule or one discriminating example.
- Keep rationale only when it prevents likely error.
- Fix unclear code/config instead of documenting mechanics.
- Move branch-only detail behind a pointer; co-locate rule, definition, caveats.

Stop at the shortest version that selects the right branch, preserves guardrails, and makes completion testable.
