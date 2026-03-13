---
name: kubernetes-security
description: "Kubernetes security workflow for cluster hardening, workload isolation, and policy enforcement. Use when RBAC, network policy, pod security, secret handling, or admission controls must be defined before production exposure; do not use for API contract design or requirement prioritization."
---

# Kubernetes Security

## Overview
Use this skill to implement enforceable Kubernetes security controls that reduce blast radius and privilege misuse.

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

## Shared References
- RBAC and NetworkPolicy baselines:
  - `references/rbac-networkpolicy-baselines.md`

## Templates And Assets
- Security control matrix:
  - `assets/security-control-matrix-template.csv`
- Pod security checklist:
  - `assets/pod-security-checklist.md`

## Inputs To Gather
- Workload trust boundaries and risk profile.
- Access requirements by service account/namespace.
- East-west network communication requirements.
- Secret lifecycle and policy constraints.

## Deliverables
- Kubernetes security control matrix with ownership.
- Pod-level hardening decisions.
- RBAC and network isolation policy definitions.
- Verification evidence for applied controls.

## Workflow
1. Build control matrix in `assets/security-control-matrix-template.csv`.
2. Define RBAC and network policy using `references/rbac-networkpolicy-baselines.md`.
3. Validate workload hardening with `assets/pod-security-checklist.md`.
4. Verify secret and policy enforcement behavior.
5. Publish accepted risks and remediation backlog.

## Quality Standard
- Access controls follow least-privilege principles.
- Network paths are explicit and deny-by-default where feasible.
- Pod security posture is consistent and reviewable.
- Secret handling minimizes exposure in runtime and config.

## Failure Conditions
- Stop when critical workloads run without required isolation controls.
- Stop when privilege model cannot be audited from manifests/policies.
- Escalate when required controls conflict with runtime constraints.
