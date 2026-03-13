---
name: ml-feature-engineering
description: "ML feature engineering workflow for feature definition, lineage, and online-offline parity. Use when model performance depends on explicit feature design and parity controls; do not use for generic API-layer or infrastructure-only changes."
---

# Ml Feature Engineering

## Overview
Use this skill to design features that are useful, explainable, and consistent across training and serving.

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

## Shared References
- Online/offline parity rules:
  - `references/online-offline-parity-rules.md`

## Templates And Assets
- Feature specification template:
  - `assets/feature-spec-template.csv`

## Inputs To Gather
- Candidate feature hypotheses and business rationale.
- Data sources and freshness constraints.
- Serving path capabilities and latency budget.
- Leakage/fairness/compliance constraints.

## Deliverables
- Feature catalog with lineage and ownership.
- Parity validation plan for train vs serve paths.
- Feature risk and maintenance notes.

## Workflow
1. Define feature specs in `assets/feature-spec-template.csv`.
2. Validate parity assumptions with `references/online-offline-parity-rules.md`.
3. Prioritize features by incremental value vs complexity.
4. Verify leakage and freshness assumptions.
5. Publish feature rollout and deprecation plan.

## Quality Standard
- Feature definitions are versioned and reproducible.
- Online/offline behavior is consistent for decision-critical features.
- Feature ownership and monitoring are explicit.

## Failure Conditions
- Stop when feature logic diverges between training and serving.
- Stop when feature value cannot justify operational complexity.
- Escalate when parity gaps remain unresolved.
