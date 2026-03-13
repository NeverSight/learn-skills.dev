---
name: testing-regression-strategy
description: "Risk-based regression suite curation for release gating under time and budget limits. Use when teams must decide what runs always versus conditionally by impact and risk; do not use for implementing a single test type in isolation."
---

# Testing Regression Strategy

## Overview
Use this skill to select regression coverage that maximizes risk reduction within execution constraints.

## Scope Boundaries
- Use when not all tests can run every change and selection policy is required.
- Typical requests:
  - `Optimize regression coverage under CI time budget.`
  - `Define mandatory versus conditional suites by risk.`
  - `Map change impact to regression gates.`
- Do not use when:
  - The task is implementing one specific test case only.
  - The task is observability/alert policy design (`observability-*`).

## Inputs
- Release risk profile and CI budget
- Test inventory with cost, flakiness, and detection value
- Change-impact and component criticality model

## Outputs
- Tiered regression policy (always-run, conditional, periodic)
- Decision record for suite selection logic and trade-offs
- Verification checklist and gap register

## Workflow
1. Classify system areas by business and technical risk.
2. Quantify each suite by execution cost and detection value in `assets/regression-tiering-template.csv`.
3. Compare selection policies and choose one with rationale.
4. Define trigger rules for conditional suites.
5. Publish policy, residual risk, and review cadence.

## Quality Gates
- High-risk areas are always covered by mandatory gates.
- Selection policy is explainable and auditable.
- Budget trade-offs are explicit, not implicit.
- Policy includes periodic recalibration triggers.

## Failure Handling
- Stop when high-risk areas are uncovered by mandatory tests.
- Escalate when budget and required risk coverage conflict.

## Bundled Resources
- `references/trigger-and-examples.md`: trigger patterns, anti-patterns, and deliverable expectations.
- `assets/regression-tiering-template.csv`: quick-start matrix for always/conditional/nightly suite selection.
