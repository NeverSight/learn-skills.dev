---
name: write-maintainable-code
description: Design, implement, repair, refactor, review, and test maintainable program code across languages and frameworks. Use whenever Codex changes executable behavior beyond trivial formatting, including feature work, bug fixes, APIs, scripts, concurrency, persistence, integrations, security boundaries, performance-sensitive paths, or tests. Enforce repository-first discovery, explicit behavioral contracts, minimal coherent changes, secure boundary handling, behavior-focused tests, and independent diff review.
---

# Write Maintainable Code

Apply repository instructions and language- or framework-specific constraints
before this general workflow. Keep the process proportional: a tiny local fix
needs a focused check, while state, API, concurrency, migration, or security
changes need explicit invariants and broader verification.

Read `references/engineering-foundations.md` when choosing a nontrivial design,
security boundary, test strategy, or review standard.

## Establish the contract

1. Read the governing instructions, working-tree state, nearby implementation,
   call sites, tests, and build constraints before editing.
2. State one observable completion criterion and the behavior that must remain
   unchanged. Separate requirements from attractive but unrequested cleanup.
3. For a defect, reproduce or independently confirm the failing behavior when
   safe. Preserve a regression case that would fail under the old behavior.
4. For a non-obvious decision, compare two or three viable designs. Prefer the
   smallest design that fits existing boundaries and keeps future removal or
   rollback simple.

Do not introduce a dependency, abstraction, configuration option, or extension
point for hypothetical future use.

## Design the change

Define the relevant inputs, outputs, invariants, ownership, failure behavior,
and compatibility surface before implementation. Preserve public APIs, stored
data, protocols, and error semantics unless the requested change authorizes a
break.

Place validation and conversion at trust boundaries. Keep domain logic separate
from I/O when that improves testability. Make dependencies and side effects
visible. For concurrency or mutable state, identify who owns each transition
and what makes it atomic, ordered, idempotent, or safely retryable.

## Implement one coherent purpose

- Follow an existing good pattern in the repository unless evidence shows it is
  the cause of the problem.
- Keep the diff focused. Separate broad renaming, formatting, generated output,
  dependency updates, and unrelated refactoring from behavioral work.
- Use names that expose intent and units. Prefer straightforward control flow
  over compressed cleverness.
- Keep functions and modules cohesive. Extract code when it creates a real
  boundary or removes meaningful duplication, not merely to reduce line count.
- Explain decisions and constraints in comments; let clear code explain normal
  mechanics. Update API or operator documentation when behavior changes.
- Return or surface actionable failures. Do not swallow exceptions, silently
  fall back, or report success after partial failure.
- Treat inputs as untrusted at the relevant boundary. Use allow-list validation,
  context-appropriate encoding, least privilege, safe defaults, and secret-free
  diagnostics.
- Optimize only against a stated constraint or measurement. Preserve the
  simpler implementation when performance evidence does not justify complexity.

## Prove behavior

Choose the cheapest test level that exercises the changed contract:

- Use unit tests for deterministic local logic.
- Use integration tests for serialization, filesystem, database, process,
  framework, or service boundaries.
- Use end-to-end checks only for critical paths that lower levels cannot prove.

Cover the success path, meaningful boundaries, expected failure behavior, and
the reported regression. Keep tests deterministic, isolated where appropriate,
self-checking, and readable. Assert externally meaningful behavior instead of
private implementation details.

Run focused checks first, then the relevant broader suite, build, type check,
lint, or formatter. An exit code alone is not proof: inspect generated output or
state with an independent method. If a required check cannot run, state why and
where it will be settled.

## Review before handoff

Read the final diff and the complete changed functions or modules as a reviewer,
not only as the author. Check:

- correctness across callers, boundaries, and failure paths;
- accidental API, data-format, permission, or compatibility changes;
- state cleanup, resource lifetime, retries, concurrency, and partial failure;
- tests that would actually fail if the behavior regressed;
- unused code, debug output, stale comments, unrelated edits, and secrets;
- whether the change improves or at least preserves overall code health.

Report the behavior changed, important design choice, exact validation run, and
any remaining uncertainty. Never say a path was tested when it was only read or
reasoned about.
