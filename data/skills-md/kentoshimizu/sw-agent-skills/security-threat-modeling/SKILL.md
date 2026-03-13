---
name: security-threat-modeling
description: "Security workflow for threat modeling using assets, trust boundaries, attacker capabilities, and abuse paths. Use when systems or major features need explicit security design validation before implementation or major release; do not use for active incident containment."
---

# Security Threat Modeling

## Overview
Use this skill to make security risks explicit early, prioritize mitigations, and prevent costly redesign after implementation.

## Scope Boundaries
- New architecture, integration, or data flow introduces fresh trust boundaries.
- Significant feature changes alter attacker opportunity or impact.
- Security requirements need prioritization before implementation commitments.

## Templates And Assets
- Threat model template:
  - `assets/threat-model-template.md`

## Inputs To Gather
- System context, components, and data flow diagrams.
- Asset classification and business impact.
- Assumed attacker capabilities and exposure surface.
- Existing controls and operational detection capabilities.

## Deliverables
- Threat model with assets, trust boundaries, entry points, and abuse paths.
- Prioritized mitigation plan with owner, expected risk reduction, and timeline.
- Validation plan mapping top threats to test and monitoring evidence.

## Workflow
1. Define model scope and highest-value assets in `assets/threat-model-template.md`.
2. Identify trust boundaries and all ingress/egress paths.
3. Enumerate attacker goals and feasible attack paths for each boundary.
4. Assess risk using impact and exploitability, then rank mitigation candidates.
5. Select controls across prevention, detection, and response, not prevention only.
6. Record residual risks that are accepted, including owner and review date.
7. Convert priority threats into concrete engineering and verification tasks.

## Quality Standard
- Top abuse paths are evidence-backed and mapped to concrete controls.
- Mitigation prioritization is explicit and reproducible.
- Residual risks are intentionally accepted, not implied.
- Model output is actionable by engineering, security, and operations.

## Failure Conditions
- Stop when assets and trust boundaries are undefined.
- Stop when high-impact threats are listed without mitigation owner.
- Escalate when risk acceptance lacks accountable approval.
