---
name: github-actions-workflow-design
description: "Design and maintain GitHub Actions workflows with explicit trigger scope, security boundaries, and reliable job orchestration. Use when GitHub automation (build/test/release jobs, triggers, permissions, caching, concurrency, environments) must be created or revised; do not use for non-GitHub runtime architecture or data-layer design."
---

# Github Actions Workflow Design

## Overview
Use this skill to design CI/CD workflows that are secure, debuggable, and aligned with repository protection policy.

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

## Shared References
- Permissions matrix:
  - `references/actions-permissions-matrix.md`
- Reusable snippet examples:
  - `references/workflow-snippets.md`

## Templates And Assets
- Workflow topology template:
  - `assets/workflow-topology-template.md`
- Workflow design checklist:
  - `assets/workflow-design-checklist.md`

## Inputs To Gather
- Required checks and branch protection policy.
- Build/test/deploy responsibilities and runtime matrix.
- Secret handling policy and environment separation.
- Expected runtime budget and failure triage expectations.

## Deliverables
- Workflow topology with explicit triggers and job dependencies.
- Permission model per job and environment.
- Cache/artifact strategy with invalidation notes.
- Verification checklist for PR and protected branch runs.

## Workflow
1. Define topology in `assets/workflow-topology-template.md`.
2. Scope triggers to required events and branches only.
3. Split jobs by responsibility and assign least-privilege permissions.
4. Add cache/concurrency controls and environment protection.
5. Validate with `assets/workflow-design-checklist.md`.

## Quality Standard
- Required checks exactly match branch protection gates.
- Job permissions are minimal and explicit.
- Workflow runtime and cache behavior are observable.
- Failure output is actionable for on-call and contributors.

## Failure Conditions
- Stop when trigger scope can cause unsafe or noisy execution.
- Stop when deploy job permissions are broader than required.
- Escalate when workflow design conflicts with repository governance.
