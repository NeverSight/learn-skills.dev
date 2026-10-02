---
name: sharpen-dedupe
license: MIT
description: Audit repeated code for shared behavior and ownership before consolidation. Use to decide what can share an implementation, what must remain separate, or what needs more evidence; not for document SSOT or behavior-changing unification.
---

# Sharpen Dedupe

Similar syntax does not establish shared behavior or ownership. Default to read-only audit; consolidation requires existing authorization for its scope.

## Inputs

Required: suspected duplicates or a bounded search area. Optional: callers, contracts, allowed paths, tests, and consolidation authorization.

## Procedure

1. Find occurrences and callers using complementary language-appropriate evidence: search, imports, symbol references, registrations, or tests. Declare the search boundary and unresolved dynamic references.
2. Compare observable inputs, outputs, errors and their order, effects and their count, mutation, async ordering, dependencies, public interfaces, and persisted shapes. Assign semantic labels:
   - `identical`: same text and established observable behavior
   - `equivalent`: different text with established equivalent observables
   - `partial`: only a subset of behavior overlaps
   - `divergent`: established intentional or contractual differences
   - `unknown`: evidence cannot establish the relationship
3. Assess ownership and dependency direction independently of semantics. Same behavior in separate domains need not share a runtime dependency. Do not cross trust or permission boundaries without confirmation.
4. Propose an existing maintained owner, or a new owner at a natural boundary only if sharing is justified. In an audit, do not create it. Record unique behavior that must survive and evidence needed before extraction.
5. Assign each non-owner an action separately from its semantic label:
   - `dedupe`: remove a redundant copy fully covered by the owner
   - `reference`: import or use the owner while preserving required behavior
   - `reconcile`: incompatible requirements require an owner's decision
   - `keep`: retain an intentional difference or ownership boundary
   - `defer`: postpone judgment or consolidation until specified evidence exists
6. Missing evidence is not a contradiction. Use `defer` for unknown semantics and `keep` for justified separation. Partial overlap may share only the proven portion while preserving caller-specific behavior.
7. If consolidation is authorized, report the map and plan, then execute without asking for the same permission again. Fold unique required behavior into the owner before removing copies. Preserve necessary re-exports or aliases so reachable paths remain usable.
8. Make located edits, verify replacement targets, and use language-aware tools or a reviewed script for structural moves. Preserve unrelated user work. Run relevant success and failure checks and inspect callers, orphaned references, dependency direction, and the final diff.

## Output and stopping

Honor the caller's format. Otherwise use a short table or a few paragraphs identifying the compared locations, their semantic relationship, the proposed action and its evidence. Include the owner proposal and unresolved gaps only where they affect the decision. The procedure steps are reasoning steps, not required report sections. Distinguish proposed edits from actual edits and executed checks. A justified no-op may be reported in a few sentences.

Stop after the audit or verified authorized change. Stop dependent edits for missing evidence, conflicting requirements, or scope expansion. Do not imply universal equivalence from finite checks or alter public contracts, add production dependencies, commit, or deploy as incidental deduplication.

## Examples

- Identical parsers owned by independent products stay separate when their dependency contract forbids sharing.
- A dynamic registry is unavailable: report `unknown` plus `defer`, not a guessed merge or invented conflict.
