---
name: grimoire-simplify
description: Simplify existing code from one function to a repository through deletion, flattening, consolidation, and coherent internal rewrites while preserving behavior.
---

# Purpose

Reduce the concepts, states, branches, indirections, dependencies, and maintained code required to understand existing behavior. Favor real subtraction over cosmetic movement.

# Scope and authorization

Works independently: establish the baseline, discover candidates, implement, and verify without requiring a map, report, or another skill. Accept optional orchestration context or a persisted map, but verify it against current source.

Explicit simplification requests authorize behavior-preserving internal changes, including coherent rewrites and file reorganization within established responsibility boundaries. Do not pause for per-rewrite approval when that work is already authorized. Analyze-only or discussion requests produce candidates without code changes. Ask before changing observable behavior/public contracts, moving responsibilities across architectural boundaries beyond authorization, or irreversible actions. Structural redesign belongs to `grimoire-improve` when selected; otherwise report it as outside this skill's boundary and continue safe in-scope work.

# Leading words

- **behavior contract** — observable behavior, public API, error and concurrency semantics, ownership/lifetime, and important performance guarantees.
- **understanding path** — concepts, states, branches, representations, files, and calls needed to explain the logic.
- **work unit** — the smallest coherent change including affected callers and verification, not necessarily one file.

# Workflow

## 1. Establish baseline and coverage

Read target code, callers, registration/configuration, and relevant tests. Record contracts, boundaries, source revision/dirty state, validation commands, and baseline results. In implementation mode, add characterization coverage for high-risk poorly tested paths before rewriting them; in analyze-only mode, record missing coverage without changing tests or production code.

For broad requests, inventory all in-scope first-party modules and maintain `.grimoire/simplify-state.json` with baseline, coverage, candidate evidence/dispositions, work-unit dependencies, results, and next action. Analyze both module-local and cross-module opportunities. Track unread/blocked regions explicitly; search hits do not equal inspected code. Under orchestration, use the supplied scope and return ledger updates rather than write shared state.

For comprehensive simplification, default to a net production LOC reduction target of at least 30% unless the user specifies otherwise. Bounded tasks use their stated goal. Fix the counter/version, command, formatting, filters, and baseline inventory before edits: nonblank/noncomment first-party production LOC; report tests/config/docs/generated/vendor separately. Count all new and moved implementations in the final scope. Compute `100 * (baseline - final) / baseline` on the integrated tree; zero baseline is not applicable. Never reset the denominator mid-run or count minification, comment removal, deleted useful tests, or complexity transferred to configuration/dependencies as simplification.

Under orchestration, use the coordinator's shared baseline and assigned unit criteria; the global reduction target is not a per-module or per-worker quota. Report unit deltas without claiming global acceptance.

Completion: Behavior, coverage, baseline evidence, and any quantitative acceptance target are explicit and reproducible.

## 2. Discover and choose transformations

Trace entry points through policy, state, and effects. Find dead/duplicate code, repeated policies, redundant state/conversions, deep routing, forwarding chains, and confusing private decomposition. Apply [references/candidate-guide.md](./references/candidate-guide.md) for retention and hidden contracts, and [references/examples.md](./references/examples.md) for comparisons.

Prefer deletion, inlining valueless indirection, merging equivalent behavior/state, and clearer names. Compare with a section or bounded module rewrite when incremental edits would preserve a confusing implementation shape. Introduce helpers only when they shorten the understanding path or enforce a real boundary; do not inline meaningful domain operations merely because they have one caller.

For broad refactoring, apply [references/large-scale-patterns.md](./references/large-scale-patterns.md): split god files cohesively, consolidate semantic duplicates under one owner, and flatten control flow without changing decision order. Establish shared contracts before independent consumer migrations. Deduplicate candidates by root cause and group coupled changes with their callers/tests.

Completion: Each selected unit has an explicit complexity reduction, owned scope, preserved contract, dependencies, and verification plan. No display limit truncates the backlog.

In analyze-only mode, return the candidate ledger, inspected coverage, evidence, proposed units, and verification needs here; do not enter implementation or claim the proposed reduction was achieved. Analysis completion is distinct from implementation acceptance.

## 3. Implement coherent units

Proceed within authorization, replacing obsolete private paths completely rather than layering the new design alongside the old. Remove newly unreachable helpers, state, adapters, registrations, imports, and dependencies. Preserve public compatibility where required; do not leave unnecessary private compatibility shims.

Execute dependency-ready units in small verifiable waves. Independent workers may use isolated worktrees when permitted; overlapping files and shared helpers need one owner or serial changes. Preserve user work, inspect actual returned diffs, and validate the combined tree after integration. Serial execution is a full alternative, not a reduced-quality mode.

Completion: Each unit is complete end to end, with no unexplained migration residue or unauthorized contract change.

## 4. Verify preservation and actual simplification

Run baseline and changed-risk checks, including affected consumers and integration paths. Inspect guarantees tests may miss: authorization, error precedence, ordering, cleanup, transactions, concurrency, ownership, and sensitive performance. Repair or selectively undo regressions without discarding unrelated user edits. Unavailable checks remain unresolved evidence, not passes.

Explain each transformed path and compare it to the original. Keep changes only when they reduce understanding cost without hiding complexity. Measure LOC and relevant before/after structural signals: duplicate implementations, nesting, responsibility concentration, cycles, and call/file hops. A file split alone is not LOC reduction; fewer lines alone do not prove readability.

Completion: Retained changes have behavior evidence and a materially clearer understanding path; actual net metrics include additions and integrated effects.

## 5. Rescan and close

Repeat discovery and implementation while actionable in-scope candidates remain. For comprehensive requests, revisit all modules and cross-module seams after integration; do not stop at the largest files, an arbitrary count, or merely reaching 30%. Reuse only hash-validated inspection evidence and recheck affected relationships.

Retain code when further changes are only stylistic, equivalent-complexity swaps, speculative generalization, hidden complexity, or contract violations. Record a concrete reason per remaining material candidate. Update affected navigation/docs and refresh an existing map or flag changed shards stale.

Completion requires full requested coverage, no unresolved actionable in-scope candidates, preserved behavior with required validation, and all requested numeric/structural gates. If safe candidates are exhausted below the LOC target, report the actual shortfall as an unmet criterion with evidence; never delete necessary behavior or declare success. On blocked checks or interrupted execution, persist the next action and report incomplete.

# Final response and handoff

Report deleted/flattened/consolidated/rewritten code, contracts preserved, source snapshot, actual changed paths, commands/results, before/after metrics, coverage, and remaining work or reasons for retention. Under orchestration, include the unit ID and actual base/head or fingerprints; do not overwrite shared maps, reports, or acceptance status. Standalone responses may be concise and need no orchestration artifacts for small tasks.

# Rule

**Delete when possible. Rewrite when clearer. Preserve behavior. Finish the scope, not just the easy findings.**

# References

- [candidate-guide.md](./references/candidate-guide.md) — retention tests and hidden contracts
- [examples.md](./references/examples.md) — before/after transformations
- [large-scale-patterns.md](./references/large-scale-patterns.md) — god files, helper ownership, routing, and dead-code evidence
