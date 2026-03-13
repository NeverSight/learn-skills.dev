---
name: ml-model-selection
description: "ML model selection workflow for transparent trade-offs across accuracy, latency, cost, and operability. Use when choosing among multiple model candidates for production use; do not use for generic API-layer or infrastructure-only changes."
---

# Ml Model Selection

## Overview
Use this skill to choose model candidates with explicit trade-off reasoning, not single-metric optimization.

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

## Shared References
- Model selection trade-off rules:
  - `references/model-selection-tradeoff-rules.md`

## Templates And Assets
- Model comparison matrix:
  - `assets/model-comparison-matrix-template.csv`

## Inputs To Gather
- Candidate models and benchmark evidence.
- Serving constraints (latency, throughput, hardware, cost).
- Risk requirements (robustness, fairness, explainability).
- Operational ownership and rollback constraints.

## Deliverables
- Candidate comparison matrix with decision rationale.
- Selected model and fallback candidate.
- Risk register and rollout recommendation.

## Workflow
1. Capture candidate metrics in `assets/model-comparison-matrix-template.csv`.
2. Apply trade-off policy from `references/model-selection-tradeoff-rules.md`.
3. Validate decision against production constraints.
4. Document rejected alternatives and why.
5. Publish selection and fallback plan.

## Quality Standard
- Selection criteria include accuracy + latency + cost + operability.
- Decision is evidence-backed and reproducible.
- Fallback strategy exists for failed rollout.

## Failure Conditions
- Stop when selection ignores production constraints.
- Stop when alternatives are not evaluated comparably.
- Escalate when no viable candidate meets minimum requirements.
