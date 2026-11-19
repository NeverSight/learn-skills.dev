---
name: abp-ddd-module-designer
description: Design, implement, review, or refactor ABP business modules with meaningful business invariants, aggregate boundaries, and domain behavior. Not intended for simple CRUD, reporting-only pages, or infrastructure-only tasks.
---

# ABP DDD Module Designer

Make business rules and consistency boundaries explicit, then place behavior in the appropriate ABP layer.

## Start from the task

- Inspect the files or use case named by the user, repository instructions, and nearby implementation patterns.
- For a new module, identify business invariants and lifecycle before choosing aggregates. If only field validation and basic CRUD are needed, keep the design lightweight.
- For an existing module, investigate the boundaries affected by the task. Do not require a full domain redesign for a local change.
- Follow installed ABP/EF Core versions and project conventions. Verify unfamiliar APIs against installed source or version-appropriate official documentation before generating code.
- A review produces findings; it does not authorize refactoring. Implement only changes within the requested scope.

## Model consistency before structure

- Define which state must remain consistent in one transaction. Use that requirement to choose the aggregate boundary.
- Give an aggregate its own lifecycle and protect invariants through explicit domain operations.
- Keep child entities under aggregate control. Use value objects where identity is irrelevant and equality is by value.
- Prefer Id references between aggregates. Do not enlarge an aggregate or introduce cross-aggregate navigation just to simplify a query; assess existing mappings before proposing changes.
- Treat logs, history, and reporting data as separate candidates unless they must participate in the aggregate's consistency boundary. License validation history, for example, need not be a child collection merely because it refers to a license.
- For rules spanning aggregates, state the transaction or eventual-consistency strategy. A domain service alone does not establish atomicity.
- For uniqueness or concurrency-sensitive rules, consider database constraints and conflict handling; a lookup before writing does not prevent races.
- Add domain events only when a concrete consumer or consistency requirement justifies them.

## Place behavior

| Location | Responsibility |
| --- | --- |
| Entity / aggregate | Rules and state transitions based on its own state. |
| Domain service | Domain rules requiring repository access or coordination that do not naturally belong to one entity. Follow project naming, commonly `*Manager`. |
| Application service | Authorization, use-case sequencing, transaction boundaries, invoking domain behavior, and DTO assembly. |
| Repository / query service | Persistence and retrieval; read-specific projections when needed. |

Do not introduce a manager, custom repository, or read-model abstraction solely to complete a layer diagram.

## Preserve domain boundaries

- Constructors or factories establish valid initial state. Retain ORM-compatible construction where required.
- Protect invariant-bearing fields and collection mutations; use explicit methods for meaningful state changes.
- Supply identifiers through the project's identifier-generation mechanism rather than generating them inside entities by default.
- Input DTOs validate transport shape; domain operations enforce business rules. Avoid blind DTO-to-entity mapping that bypasses those operations.
- Application service contracts expose DTOs, not persistence entities.
- Keep domain code independent of EF Core and application-layer concerns. Place custom repository interfaces in Domain and persistence implementations in EntityFrameworkCore.
- Prefer repository methods or projections over leaking persistence-specific query composition. Where the project uses ABP query abstractions, assess the actual dependency and execution boundary rather than treating every `IQueryable` as an automatic defect.
- Keep EF mappings in the persistence layer. Do not introduce lazy loading implicitly.
- Reuse the project's DbContext composition, unit-of-work, async, and cancellation patterns. Do not create a new DbContext or project merely to satisfy a template.
- Generate EF migrations and frontend API clients with project-supported commands; do not hand-edit generated snapshots or proxies. If generation is blocked, report the command and blocker.

## Match the deliverable to the request

- **Design:** Explain relevant invariants, aggregate boundaries, responsibility choices, and unresolved tradeoffs. Include layout or code only when useful.
- **Review:** Read [references/review-guide.md](references/review-guide.md). Prioritize concrete findings with evidence and the smallest corrective action.
- **Implementation:** Implement the requested behavior using existing patterns. For a new module's layout, consult [references/module-layout.md](references/module-layout.md).
- **Refactor:** Explain the behavior being preserved, choose the smallest safe change, and account for callers and persisted data. Avoid unrelated architectural cleanup.

Do not impose fixed response sections or supply a code skeleton for every task. Keep assumptions distinguishable from confirmed requirements.

## Verify proportionally

- Follow the user's verification scope and repository instructions.
- For business-rule changes, use focused regression tests for the affected invariant or transition, plus appropriate compilation checks.
- For instruction-only or low-risk supporting changes, use the narrowest applicable static validation.
- Report what was verified and any remaining runtime or integration gap. A successful build does not prove business behavior.
