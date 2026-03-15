---
name: plan
description: "Plan: create an execution Plan from an approved Shaping doc"
disable-model-invocation: true
---

# Plan: create an execution Plan from an approved Shaping doc

When the user types `/plan` and references an approved Shaping doc, do the following:

## 1) Study the Shaping doc and the codebase (required)

- Read the Shaping doc end-to-end.
- Re-identify the **primary workflow(s)**, system boundary, and the smallest end-to-end slice.
- Search the repo for the most relevant implementation paths (models, controllers, services, jobs, GraphQL, frontend, permissions, feature flags).
- Prefer integration points that match existing patterns (Flipper flags, Sidekiq jobs, Stripe clients, GraphQL "view model" conventions, observability conventions).

## 2) Create a new Plan markdown file

- **Location**: `projects/<domain-name>/<project-name>/plan.md`
- **Domain name**: the product area or team domain (e.g., `payments`, `family-messaging`, `attendance-plus`)
- **Project name**: derive a stable folder slug from the referenced shaping path when possible (prefer `projects/<domain-name>/<project-name>/shaping.md`).
- **First line**: `# Plan: <Project name>`
- **Source links**: include links to the Shaping doc path (and Pitch path if available).

## 3) Populate the Plan (no blanks)

Fill every section. If something cannot be inferred, write the smallest explicit note stating what's missing and what decision would unblock it.

### Context and goals

- **Problem statement**: one paragraph
- **Users and workflows**: bullets
- **Success metrics**: 3–6 bullets (include at least one operational metric)

### Scope

- **In scope (must ship)**: bullets, aligned to appetite
- **Out of scope (explicit no-gos)**: bullets
- **Milestones**: 3–6 milestones with crisp outputs, each deliverable and demo-able

### Technical approach

- **Data model**: entities, keys, and relationships
- **Sync strategy**: triggers, schedule, idempotency, failure handling
- **API surface**:
  - If GraphQL: one operation per screen; bounded lists; auth at top-level resolver; UUIDs at boundary
  - If Rails HTML: controller/actions/views, and how auth is enforced
- **UI**: places, navigation entry, major components

### Rollout, permissions, and safety

- **Feature flag plan**:
  - Exact flag name(s) following the convention `<domain>_<feature_name>_enabled` or `<domain>_<feature_name>` (e.g., `payments_stripe_payout_sync_enabled`, `family_messaging_chat_threads_v2`)
  - Domain prefix indicates the product area (payments, family_messaging, attendance_plus, etc.)
  - Where enforced (controller, resolver, view, service layer)
  - Flag must be created in the first implementation task
- **Permissions**: which roles/abilities are required for each screen/action
- **Fallback behavior**: stale data, partial mapping, external dependency failures
- **Flag-off guarantees**: what users see/experience when the flag is off (should be unchanged from current behavior)

### Observability

- **Logging**: what to log, include Stripe request IDs and low-cardinality tags
- **Metrics**: success/failure + duration; avoid high-cardinality tags
- **Runbook notes**: how to debug common failures

### Testing strategy

- **TDD discipline**: Write tests first for new models, services, and business logic
- **Unit tests**: what layers to test (models, services, helpers)
- **Integration tests**: key flows and failure modes (prefer real implementations over mocks)
- **Controller tests**: characterization tests that verify HTML output and behavior
- **GraphQL tests**: operation tests with MSW mocks for frontend, resolver tests for backend
- **Feature flag tests**: verify behavior with flag on AND flag off
- **Backfill/sync tests**: idempotency and pagination (if applicable)
- **Accessibility tests**: verify keyboard navigation and screen reader support (if UI changes)

### Work breakdown

A short, sequenced list of implementation tasks (each task should be shippable and reviewable). **All tasks are documented in the plan.md file itself — do NOT create separate task files.**

**IMPORTANT**: The first task must always be:

- **Task 1: Add feature flag** — create the Flipper flag(s), add to feature flag registry, and verify flag enforcement in the relevant controllers/resolvers/views.

**Testing approach**: Use TDD (test-driven development) whenever appropriate:

- Write failing tests first for new models, services, and business logic
- Write integration tests for API endpoints and GraphQL operations
- Write characterization tests for controller changes
- Prefer real implementations over mocks (see `.cursor/rules/_prefer-integration-tests-over-mocks.mdc`)

**Feature flag discipline**: Every task should:

- Be implemented behind the feature flag
- Include tests that verify flag-on and flag-off behavior
- Be safely shippable to production with the flag off

**Task structure**: For each task, include:

- **Title**: short, action-oriented
- **Goal**: what changes for users/system
- **Feature flag notes**: how this task respects the flag
- **TDD approach**: what tests to write first (if applicable)
- **Key touch points**: concrete likely files/classes/modules to touch
- **Manual testing**: brief description of how to verify

## 4) Output constraints

**DO NOT**:
- Create separate task breakdown files (e.g., `tasks/1-add-feature-flag.md`)
- Start implementing any code
- Create any files other than `plan.md`

**DO**:
- Create/update only the single `plan.md` file
- Include all task details inline in the Work breakdown section
- Stop after writing the plan and ask for confirmation

## 5) Ask only for true decision inputs

After writing the Plan, ask the user to confirm:

- Any exact policy/legal wording required in UI or exports
- Any hard constraints on data retention, audit requirements, or export formats
