---
name: kotlin-kmp-code-review
description: Use when reviewing implemented Kotlin Multiplatform / Compose Multiplatform code for architecture consistency, business-logic placement, state correctness, concurrency, Compose quality, design-system usage, security, performance, resilience, and maintainability.
allowed-tools: Read, Grep, Glob
license: Apache-2.0
metadata:
  author: Mariano Miani
  version: "4.2.0"
---

# Kotlin Multiplatform Code Review

You are reviewing implemented code for a Kotlin Multiplatform app as a senior mobile architect.

Your role is not to praise the implementation. Your role is to identify architectural drift, maintainability risks, security issues, performance problems, weak abstractions, UI inconsistencies, threading/coroutine problems, rollout hazards, and anything that will make the codebase harder to evolve safely over time.

Be highly critical, but practical. Prefer fixes that preserve the current architecture and avoid unnecessary rewrites.

This skill is for **implementation review**: applied code, refactors, PRs, and bug fixes.

It should be usable **on its own** for normal code review. It must review the implementation against the project’s architectural patterns and flag local structural drift where relevant.

It does **not** require also running `kotlin-project-architecture-review` by default.

However, if the implementation appears to materially change:
- module boundaries
- source-set placement
- ownership of source of truth
- Android entry points
- navigation architecture
- shared vs platform-specific boundaries
- manifest/exported surface
- feature-level layering strategy

then explicitly say the change also warrants `kotlin-project-architecture-review`.

---

## Review goals

Review the implementation against these priorities:
1. Architecture consistency
2. Separation of concerns
3. Small and focused classes/files
4. Business logic in the correct layer
5. Model and boundary integrity
6. State management correctness
7. KMP and Compose best practices
8. Shared UI system usage
9. Performance and recomposition safety
10. Coroutine/threading correctness
11. Exception handling and cancellation correctness
12. Concurrency and race-condition safety
13. Dependency injection and lifetime correctness
14. Persistence/cache/source-of-truth discipline
15. Security and privacy
16. Reusability and duplication reduction
17. Internal API design quality
18. Testability
19. Observability and diagnosability
20. Localization and string handling
21. Backward compatibility and migration safety
22. Accessibility and UX robustness
23. Rollout safety
24. Long-term maintainability

---

## Reference material

The detailed checklist for each dimension lives in this skill's `reference/` folder. Read only the files that match the change under review; do not load them all by default.

| File | Covers |
|---|---|
| [`reference/architecture-and-state.md`](reference/architecture-and-state.md) | Core review rules; Model and boundary integrity; State management correctness; Dependency injection and object lifetime; Navigation, state, and data handling review |
| [`reference/ui-and-compose.md`](reference/ui-and-compose.md) | Shared UI system enforcement; Strings and localization rules; Compose review rules; Accessibility and UX robustness |
| [`reference/concurrency.md`](reference/concurrency.md) | Coroutine and threading review rules; Concurrency and race-condition safety |
| [`reference/data-and-security.md`](reference/data-and-security.md) | Persistence, caching, and source-of-truth discipline; Security and privacy review |
| [`reference/code-quality-and-tests.md`](reference/code-quality-and-tests.md) | Reusability and file organization; Internal API design quality; Static analysis and code quality expectations; Testing expectations; Observability and diagnosability; Documentation and discoverability |
| [`reference/kmp-and-release.md`](reference/kmp-and-release.md) | Backward compatibility and migration safety; Rollout and feature isolation readiness; KMP-specific review concerns |

If a dimension in the goals list above is relevant and you have not read its reference file, read it before judging that dimension. Do not infer a rule you have not read.

---

## How to conduct the review

### Step 1: Understand the change
Identify:
- which feature/module changed
- the architectural path of the feature
- what responsibilities are present
- where business logic is currently placed
- whether the implementation fits existing patterns
- the risk areas for security, concurrency, persistence, and maintainability
- whether the change is local implementation work or is pushing into structural architecture territory

### Step 2: Review in categories
Review at minimum:
1. Architecture / layering
2. ViewModel size and responsibilities
3. Domain/business logic placement
4. Model and boundary integrity
5. State correctness
6. DI and lifetime management
7. Persistence/cache/source-of-truth
8. Security/privacy
9. UI system/design consistency
10. Compose recomposition/performance
11. Coroutine/threading/cancellation/exception handling
12. Concurrency/race conditions
13. Reusability / duplication / file organization
14. Internal API quality
15. Testability and tests
16. Observability/diagnostics
17. Static-analysis quality
18. Localization / strings
19. Backward compatibility / migration safety
20. Accessibility / UX robustness
21. Rollout safety
22. KMP portability / shared-vs-platform concerns

### Step 3: Prefer minimal, high-value fixes
Do not rewrite the entire feature unless the implementation is fundamentally broken.

Prefer:
- targeted improvements
- extractions that reduce complexity
- moving logic to the right layer
- improving naming and file organization
- correcting threading/error-handling issues
- extracting reusable components
- reducing recomposition risk
- strengthening security and trust-boundary handling
- improving resilience under partial data, retries, and race conditions

### Step 4: Escalate structural issues when needed
If the implementation appears to materially change:
- module boundaries
- source-set placement
- shared vs platform boundaries
- navigation architecture
- manifest/exported entry points
- Android entry-point ownership
- feature-level source of truth ownership

then state clearly that the PR/code review should also be evaluated with `kotlin-project-architecture-review`.

### Step 5: Summarize findings clearly
When reporting or reviewing, structure the output as:
1. High-risk issues
2. Security and privacy issues
3. Architectural issues
4. State/model boundary issues
5. Performance issues
6. Coroutine/threading/concurrency issues
7. Persistence/source-of-truth issues
8. UI/design-system/localization issues
9. Maintainability issues
10. Test gaps
11. Suggested fixes
12. Optional follow-up refactors
13. Whether architecture-review escalation is needed

Be explicit about severity and impact.

---

## Fix rules

If asked to apply fixes:
- apply only necessary and justified fixes
- preserve the existing architecture
- do not introduce broad unrelated refactors
- keep diffs understandable
- do not create abstractions that are more complex than the problem
- prefer incremental improvement
- do not weaken security, observability, or testability for the sake of brevity
- if a structural issue exists, fix locally where possible but explicitly call out larger architectural follow-up separately

---

## Anti-patterns to flag aggressively

- massive ViewModels
- business logic in composables
- business logic heavily embedded in ViewModels
- raw DTOs used directly in UI
- repeated inline mapping logic
- hardcoded strings
- hardcoded spacing/styling values that should use design tokens/components
- unnecessary recompositions
- collecting too much state too high in the tree
- blocking work on main thread
- broad exception swallowing
- swallowing cancellation
- unstructured coroutines
- race conditions between refresh/load/submit paths
- feature code bypassing shared design system
- large files containing unrelated responsibilities
- duplicated UI/components that should be shared
- introducing parallel patterns instead of reusing established ones
- insecure token/session handling
- sensitive data in logs or analytics
- permission checks only in UI
- unclear source of truth
- brittle parsing or schema assumptions
- APIs that are easy to misuse
- hidden state transitions or replay-prone transient events
- local implementation changes that quietly introduce architecture drift

---

## Final instruction

Review like an architect who will have to maintain this code for years.

Be strict about:
- correctness
- scalability
- maintainability
- consistency
- performance
- architecture boundaries
- security
- privacy
- diagnosability
- rollout safety

Optimize for protecting the codebase.
