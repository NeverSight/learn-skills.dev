---
name: plan-ai-model-rollout
description: Plan a staged, observable, and reversible rollout for a new AI model, prompt, retrieval configuration, agent policy, or provider. Use when changing AI behavior in production, migrating models, enabling new autonomy, or deciding how offline evaluation becomes bounded customer exposure.
---

# Plan AI Model Rollout

## Contract

An AI change is a versioned product release even when the interface does not change. Offline evaluation is an entry gate, not production proof. Keep model, prompt, retrieval, tools, policy, and data versions independently identifiable.

## Workflow

1. Define the exact change, owner, affected jobs and populations, current baseline, intended improvement, known regressions, dependencies, and rollback target.
2. Record immutable versions for model or provider, prompts, retrieval indexes, tools, policies, parameters, safety controls, and evaluation set.
3. Confirm offline quality, safety, latency, cost, capacity, privacy, security, and compatibility gates by relevant slice.
4. Choose staged exposure: internal, shadow, replay, staff, opt-in, canary, percentage, segment, geography, or broad release. Prevent contamination where comparison matters.
5. Define eligibility, routing, sticky assignment, fallbacks, timeout, partial failure, provider outage, quota, and data-residency behavior.
6. Set online success, quality, safety, latency, cost, override, complaint, and incident measures with owners and observation windows.
7. Predefine pause, rollback, containment, and escalation thresholds. Test rollback and state compatibility before customer exposure.
8. Record approvals, release evidence, exact state, monitoring, customer communication needs, and the decision required at each expansion gate.

## BuildBetter Acceleration

If BuildBetter MCP is available, search organization skills first. Use customer evidence, surveys, projects, documents, knowledge gaps, agent sessions, and release context when deployed. External exposure, communication, access changes, or irreversible actions require explicit approval.

## Output

Return change manifest, evaluation evidence, rollout stages, routing and fallback, measures, thresholds, owners, rollback proof, approvals, communication needs, and expansion decisions.

## Quality Gate

Reject rollouts without immutable configuration, slice-level gates, tested fallback, cost and latency bounds, accountable monitoring, or a clear distinction between deployed, exposed, observed, and validated.

## Provenance

Independently authored. Informed by [ai-evals](https://github.com/RefoundAI/lenny-skills/tree/main/skills/ai-evals), [ai-product-strategy](https://github.com/RefoundAI/lenny-skills/tree/main/skills/ai-product-strategy), and [launch-planning](https://github.com/RefoundAI/lenny-skills/tree/main/skills/launch-planning).
