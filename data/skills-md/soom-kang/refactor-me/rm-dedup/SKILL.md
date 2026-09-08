---
name: rm-dedup
license: MIT
description: Audit or consolidate duplicated code when shared ownership and observable equivalence can be established. Use for repeated implementation logic, not general document SSOT, coincidentally similar code, or behavior-changing unification.
---

# Code duplication review

Determine whether repeated code represents one behavior that can be maintained together. Similar syntax alone does not justify extraction.

## Inputs

- Required: the suspected duplicated code or bounded search scope.
- Optional: affected callers, behavior contracts, allowed edit paths, validation commands, and existing consolidation authorization.
- Default: read-only audit. Edit only when the task already authorizes consolidation within the established scope; do not request the same permission twice.

## Procedure

1. Find the occurrences and their callers using complementary evidence suited to the language, such as text search plus imports, symbol references, registrations, or tests. Report the search boundary and unresolved dynamic references rather than claiming all occurrences were found.
2. Compare semantics: inputs and outputs, error types and order, side effects and their count, mutation, async ordering, dependencies, and relevant public or persisted interfaces. Label each occurrence:
   - `identical` — the same text, with no observable difference
   - `equivalent` — different text, same observable inputs, outputs, errors, ordering, and effects
   - `partial` — one covers a subset of what another does
   - `divergent` — a deliberate or contractual behavioral difference
   - `unknown` — the available evidence does not establish the behavior either way
3. Establish shared ownership and a natural dependency direction. Identify the maintained implementation or an existing module boundary where common code belongs, or extract a new owner at that boundary when no maintained implementation already holds the behavior. Do not create cross-layer coupling merely to remove repeated lines.
4. Identify evidence that would support preservation, using existing tests and the relevant contract checks. `unknown` semantics require evidence; `divergent` behavior requires separate treatment rather than consolidation that silently changes it.
5. Report the occurrence map, equivalence evidence, unique behavior that must remain, proposed common owner, and affected callers. Assign each occurrence outside the owner exactly one action:
   - `dedupe` — remove a redundant copy the owner already covers completely
   - `reference` — have the occurrence import or read from the owner instead of restating the behavior
   - `reconcile` — the occurrence disagrees, and which behavior is correct is the caller's decision, not this pass's
6. For authorized consolidation, preserve caller-specific behavior and user changes, edit only the allowed scope, and validate both successful and failing paths relevant to the extraction. Inspect references and the final diff for orphaned code or new dependency problems.

## Rules

- **Equivalence holds inside the boundary you declared.** The evidence covers the executions you observed, not every possible one. When error type, message, or ordering differs, the implementations are not interchangeable regardless of how similar the successful path looks.
- **Fold before you cut.** A detail that exists only in a non-canonical occurrence must already be present in the owner before that occurrence can be removed. Consolidation never sheds behavior on the way through.
- **Leave a pointer where removal would strand a reader or a caller.** A one-line re-export, alias, or note beats a deletion that breaks a path something still reaches.
- **Choose the owner by who maintains it, not by what is convenient.** The maintained implementation closest to where the behavior actually changes wins; a stale copy does not get promoted because it is easier to reach from here.
- **A trust or permission boundary stops the consolidation until confirmed.** Private into public, internal into customer-facing, or privileged into unprivileged is a decision to surface, not a duplicate to collapse.
- **Every replacement is a located replacement.** Confirm the occurrence is still present before rewriting it and report a MISS instead of reporting a step that changed nothing; migrate the occurrences one at a time; move structure with a language-aware tool or a script rather than a text substitution across files.
- **Existing authorization is enough.** When the task already permits consolidation in this scope, report the map and plan and then execute; do not pause for the same approval a second time. A pass that finds no useful duplication changes nothing, and that is a successful result.

## Output and stopping

Honor the caller's schema. Otherwise return the occurrences with their labels, proposed owner or reason to keep them separate, observed equivalence and gaps, proposed or actual changes with their chosen action, and validation results.

Stop after the audit or verified authorized change. Missing evidence, conflicting behavior, or a required scope expansion must be reported before dependent edits. Do not change public contracts, introduce production dependencies, delete unrelated files, commit, or deploy as an implied part of deduplication.

## Examples

- Normal: three handlers share parsing with identical error policy and dependency use. Map their callers, extract through the existing utility boundary if authorized, and check each caller's success and failure behavior.
- Edge: two validators return the same successful value but throw different errors when both inputs are invalid. Preserve their behavior and report the distinction; shared-looking syntax is insufficient for consolidation.

## Completion check

The owner follows an existing boundary, relevant behavior differences are accounted for, the output distinguishes audit from mutation, and validation claims match checks actually run.
