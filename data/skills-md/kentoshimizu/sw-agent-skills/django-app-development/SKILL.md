---
name: django-app-development
description: "Django application development workflow for production-grade app changes. Use when Django-specific code (models, views, serializers/forms, routing, settings, middleware, auth flows) must be implemented or revised with framework runtime behavior in scope; do not use for repository-wide architecture governance or release management policy."
---

# Django App Development

## Overview
Use this skill to implement Django changes with explicit domain boundaries, safe migrations, and operationally predictable behavior.

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

## Shared References
- Layering and boundary guidance:
  - `references/django-layering-guidelines.md`

## Templates And Assets
- Change planning template:
  - `assets/django-change-plan-template.md`
- Migration safety checklist:
  - `assets/django-migration-safety-checklist.md`

## Inputs To Gather
- Feature requirements and affected domain boundaries.
- Existing app/module structure and cross-app dependencies.
- Data model constraints, traffic profile, and migration risk tolerance.
- Authentication/authorization expectations and operational requirements.
- Serializer/form input shapes and domain command object contracts.

## Deliverables
- App change design (models, views, forms/serializers, services/managers).
- Migration plan with rollout/rollback notes and data-safety checks.
- Security and permission model updates for affected routes/actions.
- Verification checklist (tests, manual checks, observability points).

## Quick Example
- Keep view/controller thin; move domain rules into service layer or model manager.
- Add DB constraints/indexes for integrity and query patterns, not only ORM-level validation.
- Use explicit transaction boundaries for multi-write critical flows.
- Fail fast when required environment variables are missing from settings.
- Convert serializer/form payloads to explicit typed command objects before domain service calls.

## Quality Standard
- App boundaries are cohesive and avoid circular dependency patterns.
- Migrations are reviewed for lock risk, backfill strategy, and reversibility policy.
- Authn/authz is explicit on every protected path.
- Error handling and logging expose failures without silent fallback behavior.
- Domain services receive explicit typed contracts, minimizing repeated casts and shape checks.

## Workflow
1. Scope impacted apps and define boundary-safe change plan in `assets/django-change-plan-template.md`.
2. Implement model and domain logic with explicit constraints.
3. Update views/forms/serializers while keeping transport and domain concerns separated.
4. Map request payloads to explicit typed structures (`dataclass`/`TypedDict`/Pydantic) rather than passing loose dicts through domain boundaries.
5. Create and review migrations with operational safety checks from `assets/django-migration-safety-checklist.md`.
6. Validate with tests and critical-flow verification before release.

## Failure Conditions
- Stop when domain responsibilities are spread across unrelated apps.
- Stop when migrations can cause unacceptable lock/data-loss risk without mitigation.
- Escalate when permission model changes are unclear or unverified.
