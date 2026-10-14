---
name: repo-gardening
description: >-
  Find and remove recurring repository drift in small, verified batches. Use
  when code, configuration, dependencies, or related artifacts contain
  duplicated helpers, speculative abstractions, guessed data shapes, dead
  material, inconsistent patterns, or low-signal boilerplate. Update a document
  only when it is direct residue of that confirmed cleanup. Do not use for
  docs-only maintenance or for redesigning documentation ownership.
---

# Repository Gardening

Continuously remove repository entropy before agents copy and amplify it. Treat “AI slop” as a quality pattern, not a claim about who authored a line.

## Orient

1. Read `AGENTS.md` and follow repository-local instructions.
2. Read the selected task or tracker, its handoff, and relevant project documents when present.
3. Inspect the working tree. Preserve user and agent changes outside the cleanup scope.
4. Identify canonical patterns from maintained code, tests, configuration, CI, linters, and architecture documents.
5. Read the full [cleanup rubric](references/cleanup-rubric.md).

Label each candidate `Confirmed`, `Suspected`, or `Not slop`. Do not remove a candidate until repository evidence makes it `Confirmed`.

## Select a batch

Choose one cleanup theme and a small reviewable batch. Prefer deviations that are easy for future agents to copy, cheap to fix, and safe to verify.

Require at least one strong signal:

- A repository rule or enforced invariant is violated.
- A canonical implementation already covers the same behavior.
- References, configuration, and runtime discovery show an artifact is unused.
- A confirmed cleanup makes a linked document false, misleading, or unrouteable.
- A boundary is probed with guessed shapes despite an available schema or typed API.

Do not classify code as slop because it looks generated, verbose, unfamiliar, or stylistically different. Report uncertain or high-risk candidates instead of deleting them.

Do not use this skill for a docs-only audit, stale prose, or unknown document
ownership. When installed, route a known documentation repair to
`agent-docs-writer` and an unclear documentation map to
`agent-docs-architect`. Otherwise report the bounded case without mutating
documentation.

## Clean

For each confirmed candidate:

1. State the invariant, evidence, affected files, and expected unchanged behavior.
2. Inspect callers, imports, exports, tests, configuration, dynamic registration, and public interfaces.
3. Apply the smallest change that restores the canonical pattern.
4. Preserve behavior, data shape, public APIs, migrations, and compatibility unless the user explicitly scopes a change.
5. Remove residue created by the cleanup: imports, comments, tests, configuration, dependencies, and directly affected documentation that are now truly unused or false.
6. Run targeted checks after each coherent change, then run the repository verification path.
7. Stop expanding the batch when a new issue has a different cause or risk profile.

When verification exposes an unrelated baseline failure, record it and keep it outside the cleanup unless it blocks proof of the change.

## Capture recurring taste

When the same harmful pattern recurs, convert the lesson into the narrowest durable guardrail:

1. Reuse an existing test, linter, schema, type boundary, or canonical utility when possible.
2. Add a mechanical check when the rule is objective and violations are detectable.
3. Add a concise repository rule only when mechanical enforcement is impractical.
4. Write failure messages that name the invariant and the remediation.

Do not add a global rule for one isolated cleanup or personal style preference. Enforce boundaries and correctness; leave local implementation freedom.

## Safety

- Never run `git clean` or delete untracked work as cleanup.
- Never remove a module, migration, public API, persistent data, or broad directory without explicit scope and evidence.
- Do not trust text search alone for dynamically loaded code, plugins, reflection, dependency injection, or generated artifacts.
- Do not reformat unrelated files or combine gardening with feature work.
- Do not expand a code cleanup into a standalone documentation refresh.
- Do not create a shared abstraction unless multiple real consumers need it.
- Follow repository-specific verification and package-manager conventions.

## Report

Finish with:

```md
## Gardened
- <removed or consolidated item> — <evidence>

## Preserved
- <candidate not changed> — <reason or uncertainty>

## Verification
- `<command>` — <result>

## Guardrail
- <added rule/check, or “none; isolated deviation”>

## Next batch
- <one bounded candidate, or “none”>
```

Update only the selected canonical task or tracker when its state materially changes. Do not invent a cleanup tracker or new documentation hierarchy.
