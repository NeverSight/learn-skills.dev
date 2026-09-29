---
name: engineering
description: "Use when implementing, refactoring, planning, or researching an understood software change. Excludes unknown-cause failures, test design as the main task, and review or audit work."
---

# Engineering

## Overview

Build the smallest production-complete change that delivers the requested outcome. The main agent owns the plan, shared contracts, integration, and completion claim. Delegated implementers use this skill with relevant domain guidance and return their slice and focused proof to the parent for independent review and integration.

## When to Use

- Features, understood bug fixes, refactors, migrations, and implementation plans
- Read-only research or design for a known software objective
- Greenfield work whose next useful behavior can be sliced vertically

## When Not to Use

- Use `debugging` when the cause or failing boundary is unknown
- Use `test-design` when tests, TDD, coverage, or proof design are the primary deliverable
- Use the matching review, audit, branch, or handoff skill when that is the actual task
- Add `writing-rust`, `effect-ts`, or `designing-data-intensive-systems` only as a modifier when its domain pressure is present

## Minimal Workflow

1. Inspect the real entrypoint, current owner, callers, contracts, and existing proof before proposing a shape.
2. Frame the requested outcome in observable terms: success evidence, behavior that must remain unchanged, permitted side effects, and the condition that ends the task. Separate that outcome from your interpretation and any experiment proposed to reduce uncertainty.
3. Before dependent planning or implementation, surface plausible interpretations that materially change the deliverable, acceptance criteria, or costly commitments. Inspect discoverable facts and use context to settle routine choices. Ask about one unresolved user-owned decision or missing authority inline; load the grilling reference for coupled consequential choices even when coding is technically possible. Continue unaffected authorized work, retain engineering ownership, and resume dependent work after answers under existing authority.
4. Start substantial work with a production-shaped tracer bullet: one retained path through the required boundaries to observable behavior and proof. Design the remaining slices for parallel implementation from the outset, with explicit dependencies, shared contracts, ownership, and acceptance criteria. Dispatch independent slices as their prerequisites settle; keep coupled work sequential. Continue until the requested outcome is complete. A small change may need only one slice.
5. Before the first edit, plan, or delegation brief, check every Reference Routing trigger against the task and read each reference whose trigger applies. Inspection, spikes, prior knowledge, or confidence do not replace a matching reference. Write the result as one line in the conversation before that first edit, plan, or brief: `refs: <reference names>` for the pressures actually present, or `refs: none (<reason>)`. Re-check when scope grows into a new trigger, and name the applicable reference paths in every delegated brief.
6. Keep an internal scope estimate of the boundaries likely to change. Revise it as inspection reveals necessary work; report material scope changes. Routine file choices need no advance approval or narrated file list.
7. Prefer the existing owner and direct code. Add a boundary only when it hides real complexity, protects a stable contract, or has more than one real implementation; otherwise keep it inline.
8. Implement the smallest complete slice. Do not add a hook, defensive branch, fallback, compatibility path, or duplicate representation unless a current caller, applicable failure mode, threat, rollout constraint, or stored-data contract requires it; avoid unrelated cleanup.
9. Choose the cheapest trustworthy proof through an observable seam. Cover the changed behavior and required surrounding checks. Add persistent tests only when they provide meaningful protection beyond existing evidence. After checks pass, broaden or repeat them only for new edits, failures, changed relevant state, or unresolved risks.
10. Close only affected contracts and operational artifacts: callers, types, migrations, generated outputs, config, docs, observability, or rollback notes.
11. Before the main agent's implementation handoff or an intended commit, apply `review-and-simplify-changes` and finish its review/fix loop on the combined intended diff. The parent owns this gate for delegated slices. Bound conclusions by the evidence: a completed experiment or slice supports only what it tested. Finish when evidence supports the entire requested outcome and every changed boundary is accounted for. Reuse earlier proof after confirming the tested code and relevant state are unchanged; rerun affected checks otherwise.

## Reference Routing

- Read [../grill-me/references/frontier.md](../grill-me/references/frontier.md) when several coupled user-owned choices materially affect the deliverable, acceptance criteria, or costly commitments, even when implementation could proceed.
- Read [references/feature-shape.md](references/feature-shape.md) for greenfield work, a new integration, or planning multiple slices and their parallel implementation.
- Read [references/boundary-design.md](references/boundary-design.md) when callers, ownership, trust boundaries, invariant-bearing types, module/API shape, or a proposed abstraction is consequential.
- Read [references/typescript-contracts.md](references/typescript-contracts.md) when TypeScript schema ownership, inference, semantic IDs, assertions, or exhaustiveness affect the contract; follow repository and `effect-ts` conventions.
- Read [../codebase-investigation/references/historical-evidence.md](../codebase-investigation/references/historical-evidence.md) when a change depends on why existing behavior was introduced or retained.
- Read [references/legacy-change.md](references/legacy-change.md) when behavior is poorly understood, under-tested, tightly coupled, migration-sensitive, or requires repeated mechanical edits.
- Read [references/state-and-effects.md](references/state-and-effects.md) for money, durable state, external effects, webhooks, jobs, retries, concurrency, or recovery.
- Read [references/compatibility-and-delivery.md](references/compatibility-and-delivery.md) for public contracts, SDK/schema changes, mixed-version deploys, migrations, rollout, or rollback.
- Read [references/security.md](references/security.md) for auth, permissions, secrets, attacker-controlled input, abuse, replay, or sensitive data.
- Read [references/performance-and-capacity.md](references/performance-and-capacity.md) for hot paths, latency/throughput targets, resource limits, or capacity work.
- Read [references/proof.md](references/proof.md) only when the trustworthy proof is not obvious or the change has material failure modes.
- Read [references/durable-plan.md](references/durable-plan.md) only after the user requests or authorizes an in-repo plan that must survive sessions or agents, including discovery work whose route is not yet execution-ready.

## Failure modes

- Horizontal scaffolding before one real path works
- Broad architecture preflights for pressures that are absent
- New layers, factories, adapters, or fallback paths justified only by possible future use
- Expanding the diff without a reason tied to the requested outcome
- Unit-green but contract-, persistence-, migration-, or runtime-incomplete work
- Completion claims based on stale, unexamined, or partial evidence
- Loading this skill but skipping a matching reference because inspection seemed sufficient, or editing before the `refs:` line
