---
name: kotlin-project-architecture-review
description: Use when reviewing KMP architecture, feature proposals, PR structure, layer boundaries, state-holder design, Android entry-point discipline, source-set placement, modularization, and long-term maintainability in Kotlin Multiplatform / Compose Multiplatform projects.
allowed-tools: Read, Grep, Glob
license: Apache-2.0
metadata:
  author: Mariano Miani
  version: "4.1.0"
---

# Kotlin Multiplatform Architecture Review

Use this skill to review architecture decisions, feature plans, pull requests, migrations, and refactors in a Kotlin Multiplatform project.

This skill is **architecture-review only**. It evaluates structural fit, ownership, boundaries, layering, source-set placement, Android entry-point discipline, resilience, security/privacy boundaries, rollout safety, and long-term maintainability.

It does **not** perform detailed implementation-level code review for Compose recomposition, coroutine misuse, static-analysis details, line-by-line refactoring, or file-level style issues. For that, use `kotlin-project-code-review`.

This skill is intentionally strict. Its purpose is to protect maintainability, correctness of shared code placement, clean boundaries between layers, realistic ownership of state and data, Android entry-point discipline, safe trust boundaries, diagnosability, rollout resilience, and long-term scalability.

---

## Primary review goals

The review should validate whether the proposal:

- preserves a clear single source of truth for important data
- follows unidirectional data flow
- uses a proper UI state production pipeline
- keeps Android components as platform entry points rather than business-logic containers
- places business logic in the right layer
- uses the domain layer only when it adds real value
- keeps repositories and data sources responsible for data ownership concerns
- uses source sets correctly in KMP
- preserves modular boundaries and avoids accidental coupling
- keeps platform-specific behavior at the edges
- remains testable and understandable as the codebase grows
- is resilient to partial backend data, evolving schemas, and phased rollouts
- does not introduce architectural security or privacy weaknesses
- preserves diagnosability for important flows
- does not over-couple features, modules, or targets in ways that will slow future evolution

Do not optimize for theoretical purity alone.

Optimize for:
- maintainability
- correctness
- consistency
- architectural clarity
- safe evolution
- production resilience

---

## Official architecture defaults to review against

Unless the project has a strong, deliberate reason not to, prefer these defaults:

- Single source of truth for each important data type
- Unidirectional data flow
- UI driven from data models
- State holders for UI complexity
- ViewModels or equivalent state holders such as presenters, reducers, or state machines exposing UI state and receiving user actions
- Coroutines and Flow for async work and observable state
- Clear separation of UI, domain, data, and platform integration
- Domain layer only when business logic is complex or reused
- Repositories as the main boundary for exposing and coordinating app data
- Android components treated as lifecycle-bound entry points, not as general-purpose business-logic containers
- Platform-specific behavior isolated at the edges
- Transport, persistence, and external SDK details hidden behind stable boundaries
- Defensive handling of partial data, unknown values, and rollout skew
- Observability designed into high-risk flows
- Minimal, explicit trust boundaries for auth/session/admin or privileged behavior

---

## What this skill should review

Use this skill for:
- feature architecture proposals
- source-set and shared-vs-platform placement decisions
- module extraction or consolidation decisions
- state-holder strategy decisions
- navigation architecture changes
- deep link / intent / manifest surface changes
- SSOT ownership decisions
- repository/domain boundary design
- Android entry-point ownership and delegation
- cross-feature coordination and modularization
- persistence/source-of-truth architecture
- architecture-level security/privacy and rollout concerns
- PRs that introduce structural changes rather than only local implementation changes

Use `kotlin-project-code-review` instead when the main question is whether implemented code is clean, safe, performant, and consistent within an already chosen architecture.

---

## Review dimensions

The 22 review dimensions and their check/flag criteria live in this skill's `reference/` folder. Read only the files that match the proposal under review; do not load them all by default.

| File | Covers |
|---|---|
| [`reference/dimensions-core.md`](reference/dimensions-core.md) | 1-10: Single source of truth; Unidirectional data flow; Android component entry-point discipline; UI layer responsibilities; State-holder quality; Domain layer usage; Data layer responsibilities; Failure model; Layering and separation of concerns; Dependency boundaries and lifetime |
| [`reference/dimensions-kmp-modularity.md`](reference/dimensions-kmp-modularity.md) | 11-15: Source-set correctness in KMP; Shared vs platform-specific boundary quality; Module boundaries and modularization quality; Navigation and Android component interaction; Manifest and exported-surface review |
| [`reference/dimensions-resilience.md`](reference/dimensions-resilience.md) | 16-22: Security and privacy architecture; Responsiveness and configuration resilience; Resources and presentation boundaries; Observability and diagnosability; Backward compatibility, migration, and rollout safety; Testability; Architecture consistency with existing project patterns |

If a dimension is relevant and you have not read its reference file, read it before judging that dimension. Do not infer a rule you have not read.

## Severity framework

### High severity

Likely to cause architectural drift, correctness problems, security exposure, or rollout risk.

Examples:
- no single source of truth
- business logic embedded in Activities or Fragments
- repositories bypassed by UI/state-holder code
- platform APIs in `commonMain`
- major module-boundary violations
- manifest/exported entry points that bypass intended architecture
- authorization-sensitive behavior trusted to UI only
- rollout assumptions that require synchronized upgrades
- externally reachable entry points that expose privileged flows accidentally

### Medium severity

Workable, but likely to create maintenance cost or fragility.

Examples:
- weak domain-layer justification
- oversized state holder
- DTO leakage into presentation
- unclear module ownership
- inconsistent failure modeling
- partial observability gaps
- insufficient migration or partial-data resilience
- portability costs introduced without strong benefit
- competing patterns appearing in nearby features

### Low severity

Structurally acceptable but worth improving.

Examples:
- naming obscures ownership
- package split could be clearer
- tests miss important transitions
- route modeling could be more explicit
- diagnostics could be more deliberate
- ownership is correct but not obvious enough from the design

---

## Required output format

When performing the review, respond with:

1. **Verdict**
   - good fit
   - acceptable with revisions
   - poor fit

2. **Architecture summary**
   - what the proposal is doing
   - which layers, modules, source sets, and Android entry points it affects
   - whether this is a local structural adjustment or a broader architectural shift

3. **What is structurally sound**
   - concrete strengths only

4. **Issues by review dimension**
   - SSOT
   - UDF
   - Android component boundaries
   - UI layer
   - state-holder quality
   - domain-layer usage
   - data-layer design
   - failure model
   - dependency/lifetime design
   - source sets
   - shared vs platform boundaries
   - modularization
   - navigation / intents / manifest surface
   - security / privacy architecture
   - responsiveness/resources
   - observability
   - backward compatibility / rollout safety
   - testability
   - architecture consistency with existing project patterns
   - other relevant sections

5. **Severity for each issue**
   - high / medium / low

6. **Concrete recommendations**
   - exact structural changes
   - better layer placement
   - better component delegation
   - better module/source-set placement
   - better ownership boundaries
   - safer rollout / migration / authorization boundaries where needed
   - whether the proposal should be narrowed to reduce architectural surface area

7. **Suggested target structure**
   - proposed module/package/source-set / entry-point layout if useful
   - proposed ownership map if useful

8. **Open risks**
   - migration cost
   - rollout concerns
   - backward-compatibility concerns
   - operational/debugging concerns
   - cross-platform consistency concerns

---

## Tone

Be direct and practical.

Do not give vague praise.

If the proposal is weak, say so clearly and explain why.

Do not soften structural criticism with filler. The value of the review comes from precision.

---

## Anti-patterns to flag aggressively

- no clear single source of truth
- bidirectional or ad hoc state mutation
- business logic in composables, Activities, or Fragments
- DTO-driven UI
- state-holder-free complex screens
- meaningless pass-through domain layer
- repositories bypassed by upper layers
- transport details leaking upward
- platform-specific APIs in `commonMain`
- modules with unclear purpose
- manifest or intent-filter surface that does not match the intended architecture
- hidden or inconsistent failure handling
- architecture that is only testable through large integration paths
- permission checks only in UI
- untrusted external input bypassing intended architecture boundaries
- rollout-sensitive changes with brittle assumptions
- critical flows with no diagnosable ownership path
- parallel architectural patterns introduced without good reason
- large shared abstractions that hide important platform behavior
- source-set decisions made for convenience rather than correctness

---

## Review method

Follow this sequence:

### Step 1: Understand the proposal

Identify:
- what is changing
- what architectural problem it is trying to solve
- which layers/modules/entry points/source sets are affected
- whether the proposal is local or cross-cutting
- what new ownership or responsibilities are being introduced

### Step 2: Review structural fit

Evaluate:
- ownership clarity
- layering
- source-of-truth placement
- state-holder boundaries
- repository/domain responsibilities
- platform/shared split
- Android component delegation
- navigation and entry-point fit
- trust boundaries
- rollout/migration resilience

### Step 3: Review long-term evolution cost

Evaluate:
- whether the proposal makes future features easier or harder
- whether it creates a new parallel pattern
- whether it increases coupling across targets/modules/features
- whether it is diagnosable in production
- whether it will be testable without fragile end-to-end dependence

### Step 4: Prefer targeted structural changes

Do not recommend a broad rewrite unless the proposal is fundamentally broken.

Prefer:
- narrowing responsibility
- restoring proper ownership
- moving code or responsibilities to the right boundary
- reducing exported surface
- simplifying shared/platform boundaries
- clarifying module responsibilities
- making rollout and failure handling more explicit

### Step 5: Summarize with a clear verdict

Use the required output format and be explicit about what is:
- structurally sound
- structurally risky
- fixable locally
- likely to require broader migration planning

---

## Final instruction

Review like an architect who will have to maintain this system for years.

Be strict about:
- correctness
- long-term scalability
- ownership clarity
- architectural consistency
- safe platform/shared boundaries
- security and privacy boundaries
- diagnosability
- rollout safety
- testability

Do not optimize for politeness.

Optimize for protecting the codebase.


## References

- Android app architecture: https://developer.android.com/topic/architecture
- Android architecture recommendations: https://developer.android.com/topic/architecture/recommendations
- Android UI layer: https://developer.android.com/topic/architecture/ui-layer
- Android domain layer: https://developer.android.com/topic/architecture/domain-layer
- Android data layer: https://developer.android.com/topic/architecture/data-layer
- Android application fundamentals: https://developer.android.com/guide/components/fundamentals
- Kotlin Multiplatform project structure: https://kotlinlang.org/docs/multiplatform/multiplatform-discover-project.html
- Kotlin Multiplatform hierarchy: https://kotlinlang.org/docs/multiplatform/multiplatform-hierarchy.html
