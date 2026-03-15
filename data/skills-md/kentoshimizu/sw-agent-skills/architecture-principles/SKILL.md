---
name: architecture-principles
description: "Define architecture principles and review guardrails before choosing monolith, microservices, serverless, or event-driven options. Use when teams need explicit decision criteria; do not use to record final decisions."
---

# Architecture Principles

## Overview
Use this skill to produce principle-level guardrails that help agents and humans make consistent architecture decisions. The output must be concrete enough to guide design reviews and implementation planning.

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

## Inputs To Gather
- Business outcomes and failure impact.
- Quality priorities (latency, reliability, security, consistency, cost, delivery speed).
- Hard constraints (regulatory, legal, platform, security).
- Team ownership model and operational maturity.

## Deliverables
- Principle catalog with rationale.
- Review guardrail checklist.
- Tradeoff policy for conflicting principles.
- Re-decision triggers when assumptions change.

## Quality Standard
- Each principle states:
  - Why it exists.
  - What decision it constrains.
  - How to verify pass/fail in review.
  - Who approves exceptions.
- Hard constraints are separated from optimization preferences.
- Tradeoffs are explicit: what is intentionally worse and why.
- Re-decision triggers are observable and testable.

## Workflow
1. Convert business goals into ranked architecture drivers.
2. Draft principles that constrain real decisions, not slogans.
3. Add measurable review checks and exception handling.
4. Resolve conflicts between principles with explicit priority rules.
5. Publish the principle set and review cadence.

## Failure Conditions
- Stop when priorities are contradictory or missing.
- Stop when principles cannot be evaluated objectively.
- Escalate when legal or security constraints conflict with product goals.
