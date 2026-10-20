---
name: fable-wise
description: Low-level agentic design patterns and cognitive reflexes across Depth, Breadth, Coil, and Mesh. Turns senior engineering wisdom into reflexes that remove bloat, preserve truth, prevent drift, and compound learning (re0, readchk, autobahn, ssotize, detool, feynman, debloat, sip, hate, macrothink, prism). Use when refactoring complex systems, stripping AI slop, rewriting drifted artifacts from clean v0, consolidating truth into single sources, or evaluating architectural decisions against contrarian counter-arguments.
version: 1.0.0
pack: system
inputs:
  - engineering_artifact
  - pattern_directive
requires:
  - codebase_access
produces:
  - debloated_artifact
  - consolidated_truth
gates:
  - single_source_of_truth
  - contrarian_test_passed
fallback: fable-simplify
mutatesWorkspace: true
parallelSafe: true
neural_links:
  precursors:
    - fable-discover
    - fable-plan
  continuations:
    - fable-execute
    - fable-review
  lateral_peers:
    - fable-simplify
  recovery: fable-recover
---

# Fable Wise

Low-level cognitive reflexes and architectural patterns that counteract AI slop, complexity bloat, and artifact drift. Instead of adding speculative code and boilerplate, enforce patterns that simplify, cut, consolidate, and ground decisions in observable reality.

## Purpose

Enforce senior architectural wisdom through cognitive reflexes across Depth, Breadth, Coil, and Mesh. Replace bloated abstractions with direct mechanisms, consolidate single sources of truth, rewrite heavily patched artifacts from clean v0, and stress-test plans with contrarian critiques.

## When to Use

- Rewriting a drifted, heavily patched artifact into a clean v0 (`/re0`).
- Checking the model's interpretation of a subtle request before executing (`/readchk`).
- Carving unsafe scope out up front so the safe remainder runs at full strength (`/autobahn`).
- Auditing scattered facts and consolidating them into a single source of truth (`/ssotize`).
- Replacing incidental framework/stack nouns with fundamental language mechanisms (`/detool`).
- Pressing a newly made technical decision until it is simple or exposed as weak (`/feynman`).
- Stress-testing an engineering plan with the one contrarian objection that could kill it (`/hate`).
- Splitting an artifact across independent evaluation lenses to expose hidden conflicts (`/prism`).
- Tasting proposed changes with the repository's clean-and-true checks (`/sip`).

## When NOT to Use

- Routine small bugfixes with zero structural complexity (use `fable-execute`).
- Automated dependency updates or standard CI repair (use `fable-tend`).
- High-level multi-host lifecycle routing (use `get-fable`).

## Inputs

- `engineering_artifact`: Code file, architecture document, configuration, or plan.
- `pattern_directive`: Selected Paperthin cognitive reflex or command (e.g. `re0`, `detool`, `ssotize`, `hate`).

## Expected Outputs

- `debloated_artifact`: A simplified, drift-free artifact grounded in native language primitives.
- `consolidated_truth`: Single source of truth configuration eliminating duplicated parameters.

## Procedure

1. **Stage 1 — Cardinality & Temporal Classification**:
   - **Depth (One artifact, now)**: Is this single artifact clean, minimal, and true? Apply `re0`, `readchk`, `detool`, `debloat`, `feynman`.
   - **Breadth (Many artifacts, now)**: Is one truth consistent everywhere? Apply `ssotize`, `reorder`.
   - **Coil (One project, across iterations)**: Did each cycle teach the next? Apply `re0-loop`, `re0-memo`, `re0-work`, `catchup`, `nba`.
   - **Mesh (Many perspectives, across rounds)**: Does the group converge on truth? Apply `prism`.
2. **Stage 2 — Bloat Removal & Mechanism Substitution**:
   - Remove marketing buzzwords, promotional adjectives, and AI boilerplate.
   - Replace incidental third-party library nouns with standard language mechanisms.
   - Compress bloated artifacts to their load-bearing density: cut words, never rules.
3. **Stage 3 — Contrarian Testing & Cold Reads**:
   - Apply the Feynman check: explain the decision in simple terms without jargon.
   - Apply the Hate check: find the single fatal flaw and devise the cheapest test to falsify it.
   - Cold-read the artifact as a detached third party: does it stand alone without prior conversation context?
4. **Stage 4 — Single Source Consolidation (SSOT)**:
   - When multiple documents or modules declare conflicting parameters, designate one canonical authority.
   - Update all satellite references to point to the single authority; eliminate duplicative drift.

## Decision Rules

| Tempting Rationalization | Hard Reality / Invariant | Why |
|---|---|---|
| "Adding more explanations makes the document clearer." | **Violation.** Explanations dilute core rules. | Bloated documents cause agents to miss critical instructions. |
| "We should patch this legacy file one more time." | **Violation.** When patches accumulate, rewrite to a clean v0 (`re0`). | Repeated patching conceals underlying design rot. |
| "The plan looks great to everyone; no need to object." | **Forbidden.** Always apply the contrarian test (`hate`). | Identifying fatal flaws early costs minutes; finding them in prod costs weeks. |
| "Duplicating this config in two places is harmless." | **Forbidden.** Consolidate to one SSOT immediately (`ssotize`). | Duplicate configurations inevitably drift out of sync. |

- Prioritize removal over addition: removing bloat, removing drift, removing unproven assumptions.
- An artifact is finished not when nothing more can be added, but when nothing more can be removed without losing required behavior.

## Tool Policy

- Use standard file viewing and editing tools to consolidate duplicated code and configs.
- Execute project linters and tests to verify behavior is preserved after debloating.
- Do not introduce third-party helper dependencies when native standard library features suffice.

## Evidence Requirements

- Diff showing net reduction in code lines or documentation complexity.
- Test suites passing with 100% parity before and after simplification.

## Failure Handling

- If a debloating refactor breaks existing tests, identify the hidden invariant, document it explicitly, and restore passing behavior.
- If a contrarian `hate` check reveals an unfixable flaw in a plan, abort the plan and report the flaw.

## Completion Criteria

- All redundant boilerplate, unnecessary layers, and duplicate configurations stripped.
- Single source of truth established and verified across all referencing files.
- Behavioral correctness confirmed by passing test execution.
