---
name: design-principles
description: "Define and align product design principles that teams can apply consistently across UX decisions. Use when product or UX direction is ambiguous and teams need explicit decision guardrails before detailed screens or components are produced; do not use for backend data-model or deployment pipeline decisions."
---

# Design Principles

## Overview
Use this skill to produce principle-level guardrails that reduce design churn and conflicting decisions across teams.

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

## Shared References
- Baseline governance contract:
  - `references/design-governance-contract.md`
- Principle quality heuristics:
  - `references/principle-quality-heuristics.md`

## Templates And Assets
- Principle set template:
  - `assets/design-principles-template.md`
- Review checklist:
  - `assets/design-principle-review-checklist.md`

## Inputs To Gather
- Product outcomes, user success criteria, and business constraints.
- Recurring design conflicts and inconsistency examples.
- Accessibility, localization, privacy, and brand constraints.
- Existing governance rules or review process already used in the project.

## Deliverables
- Principle set written as actionable decision rules.
- Principle rationale with explicit trade-offs and anti-patterns.
- Practical review checklist mapped one-to-one to each principle.
- Ownership and update cadence for principle maintenance.

## Quick Example
- Principle: "Optimize for task completion over visual novelty."
- Applies to: interaction density, information hierarchy, and default states.
- Anti-pattern: decorative elements that hide primary actions.
- Review check: critical action is visible without hover or tooltip dependency.

## Quality Standard
- Each principle is testable in design review, not just aspirational wording.
- Principles do not conflict with each other or with required constraints.
- Trade-offs are explicit so teams can resolve edge cases consistently.
- Checklist items are concrete enough for independent reviewers to agree.

## Workflow
1. Identify repeated decision conflicts from current product/design work.
2. Draft candidate principles in `assets/design-principles-template.md`.
3. Add anti-patterns and boundary conditions for each principle.
4. Validate against accessibility/localization/privacy constraints and run `assets/design-principle-review-checklist.md`.
5. Publish approved principles with ownership and revision policy.

## Failure Conditions
- Stop when principles are abstract slogans without observable checks.
- Stop when principles directly conflict with mandatory compliance requirements.
- Escalate when ownership is unclear and no team can enforce the principles.
