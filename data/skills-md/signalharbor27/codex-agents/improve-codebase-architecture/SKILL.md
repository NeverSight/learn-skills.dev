---
name: improve-codebase-architecture
description: "Use when auditing repository or subsystem architecture for weak boundaries, domain drift, or navigation and verification friction; not for routine implementation or review of a bounded diff."
---

# Improve codebase architecture

## Overview

Diagnose structural problems in a codebase or subsystem, then turn the evidence into a practical improvement plan. The plan should simplify the code, support local reasoning, and make verification and handoff easier to bound.

## When to Use

- Architecture drift in a repository or subsystem
- Monorepo review across frontend, backend, shared-package, or CI seams
- Plans to simplify code, clean up boundaries, or improve test shape
- Checks against the current skill system and agent-friendly practices
- Decisions about what to preserve or refactor before broader modernization
- Maps of domain language, ownership boundaries, and decisions in an existing complex codebase

## When Not to Use

- Routine feature work or local refactoring
- Root-cause analysis of one failure path
- Narrow pattern questions owned by `engineering/references/boundary-design.md`
- Storage or distributed-systems review driven mainly by workload shape

## Minimal Workflow

1. Pin the review boundary and read-only authority. Inspect runtime entrypoints, owners, seams, build and test shape, domain terms, existing decisions, and named problems. For a post-code review, limit findings to the original diff and its direct effects; list broader or pre-existing issues separately.
2. For standalone audits, keep small or tightly coupled scope local and delegate material independent questions to read-only subagents. Within `review-and-simplify-changes`, independent reviewers perform the assigned checks and return findings without further delegation. The main agent owns synthesis and decisions.
3. Find the highest-cost structural problems using the judgment rules below. Support each finding with a trace from a real entrypoint through ownership, interfaces, effects, and proof where relevant. Do not inventory every possible cleanup.
4. Classify supported findings as pre-existing debt, current regression, preventable by `engineering`, `debugging`, or `test-design`, or a repo-doc candidate. Write a dependency-ordered plan sized to them. Use phases only when dependencies or rollout need them. If no finding is supported, report no actionable findings and any coverage limits.
5. Pressure-test material choices. Handle one unresolved approval inline; do not reopen settled decisions. Load the grilling reference only for an interactive interview or several interdependent consequential user-owned choices. Keep the plan in chat unless a durable target-repository file is already or explicitly authorized.

## Judgment rules

- Preserve existing guarantees and constraints unless evidence shows they are part of the problem.
- Compare simpler, deeper modules with clearer interfaces. Use module/interface/seam/depth/leverage/locality vocabulary and the deletion test from the engineering references below.
- Treat a one-adapter seam as hypothetical unless it hides real external complexity, policy variation, or a second adapter such as tests.
- Judge agent-friendliness by local reasoning and bounded evidence handoff, with domain ownership, explicit effects, and trustworthy proof seams.
- Recommend terms in `CONTEXT.md` or tradeoffs in ADRs only when they will guide future work; write them only within existing or explicit authority.

## Output contract

- Prioritized findings with file or subsystem evidence, impact, and confidence. When applicable, agent-friendly findings trace a real entrypoint through its owner, boundary, effects, and proof seam.
- For supported changes, an actionable plan with scope, payoff, dependencies, preserved behavior, and verification; phases only when needed.
- Material deferred work, alternatives, or open decisions. Explain real tradeoffs; omit empty sections.
- Completion requires evidence for every recommendation and no hidden consequential choice in the plan.

## Reference Routing

- Read [AGENT_FRIENDLY_REVIEW.md](AGENT_FRIENDLY_REVIEW.md) when navigation, local reasoning, delegation, or proof friction needs a structured review.
- Read [../engineering/references/boundary-design.md](../engineering/references/boundary-design.md) when judging domain ownership, caller knowledge, or interface depth.
- Read [../engineering/references/state-and-effects.md](../engineering/references/state-and-effects.md) when important side effects, retries, recovery, or partial failure are present.
- Read [../engineering/references/proof.md](../engineering/references/proof.md) when the trustworthy proof seam is unclear or a recommendation changes verification shape.
- Read [../grill-me/references/frontier.md](../grill-me/references/frontier.md) only for an interactive interview over several interdependent consequential user-owned decisions; retain this skill as primary.
- Read [../engineering/references/durable-plan.md](../engineering/references/durable-plan.md) only after a durable target-repo plan file is explicitly authorized.

## Failure modes

- Turning a constrained review into a greenfield redesign
- Recommending broad pattern churn without a clear payoff
- Overlooking existing tests, invariants, or operational constraints
- Returning a vague wish list or forcing phases onto a small recommendation
- Favoring internal cleverness over navigability, seams, and verifiability
