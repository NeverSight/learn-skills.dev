---
name: risk-requirements-analysis
description: "Requirement risk analysis workflow for failure scenarios, scoring, and mitigation before implementation commitment. Use when approved requirements need explicit risk assessment; do not use for initial requirement elicitation or sprint task breakdown."
---

# Risk Requirements Analysis

## Overview
Use this skill to make requirement-level risk visible before release commitments are locked.

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

## Shared References
- Requirement risk scoring rules:
  - `references/requirement-risk-scoring-rules.md`

## Templates And Assets
- Requirement risk register template:
  - `assets/requirement-risk-register-template.csv`

## Inputs To Gather
- Approved requirement baseline and dependencies.
- Incident history and known failure modes.
- Delivery timeline and operational constraints.
- Compliance/security criticality context.

## Deliverables
- `RSK-*` register linked to `REQ-*`.
- Mitigation and contingency ownership map.
- Residual risk summary for decision makers.

## Workflow
1. Identify failure modes per requirement.
2. Score risks using `references/requirement-risk-scoring-rules.md`.
3. Record risks in `assets/requirement-risk-register-template.csv`.
4. Assign mitigation and contingency owners with dates.
5. Publish residual-risk decision package.

## Quality Standard
- High-risk requirements have explicit risk entries.
- High-severity risks have mitigation and contingency plans.
- Risk acceptance authority is explicit.

## Failure Conditions
- Stop when critical risks have no owner or decision date.
- Stop when compliance risks are accepted without authority.
- Escalate when residual risk exceeds commitment policy.
