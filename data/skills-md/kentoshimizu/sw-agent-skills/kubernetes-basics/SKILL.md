---
name: kubernetes-basics
description: "Kubernetes fundamentals workflow for workload deployment, service discovery, and baseline cluster primitives. Use when teams need concrete namespace/workload/service/probe decisions before deployment; do not use for API contract design or requirement prioritization."
---

# Kubernetes Basics

## Overview
Use this skill to define a deployable Kubernetes baseline that is reproducible and operationally verifiable.

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

## Shared References
- Service discovery and probe rules:
  - `references/service-discovery-and-probe-rules.md`

## Templates And Assets
- Baseline workload manifest:
  - `assets/workload-baseline-template.yaml`
- Basics verification checklist:
  - `assets/k8s-basics-checklist.md`

## Inputs To Gather
- Target workloads and service exposure model.
- Namespace and resource-boundary requirements.
- Health signal requirements and dependency expectations.
- Rollout and rollback expectations.

## Deliverables
- Baseline workload/service manifest set.
- Probe and discovery policy aligned with runtime behavior.
- Namespace/resource boundary decisions.
- Deployment verification checklist and evidence.

## Workflow
1. Define workload/service baseline using `assets/workload-baseline-template.yaml`.
2. Apply probe and discovery guidance from `references/service-discovery-and-probe-rules.md`.
3. Align namespace/resource boundaries with ownership and blast radius.
4. Validate deployment behavior via `assets/k8s-basics-checklist.md`.
5. Publish residual risks and follow-up actions.

## Quality Standard
- Baseline manifests are declarative and reviewable.
- Service routing and probe semantics are explicit.
- Readiness reflects true traffic-safety conditions.
- Rollback path is clear before production rollout.

## Failure Conditions
- Stop when baseline workloads cannot be deployed reliably on target cluster.
- Stop when probes do not represent meaningful application health.
- Escalate when namespace/resource boundaries remain ambiguous.
