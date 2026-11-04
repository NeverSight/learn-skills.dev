---
name: spec-driven-development
description: Spec-driven development (SDD) methodology for Buildpad DaaS apps. Use when starting a new project, feature, or significant change, or when requirements are unclear. Routes work through the spec workflow — requirements.md (EARS) → design.md → tasks.md in .kiro/specs/ — via the buildpad-spec-* skills, or Kiro's native specs when working in Kiro.
---

# Spec-Driven Development

## Overview

All non-trivial work follows spec-driven development: specifications are written and approved **before** code. A spec is a contract between intent and implementation — it prevents scope creep, aligns expectations, and gives reviewers something to verify against.

Every feature lives in `.kiro/specs/<feature-name>/` as three artifacts:

| Artifact | Contents | Produced by |
|---|---|---|
| `requirements.md` | User stories + acceptance criteria in EARS format | `/buildpad-spec-requirements` |
| `design.md` | Architecture, data model, file structure plan, diagrams | `/buildpad-spec-design` |
| `tasks.md` | Small, verifiable implementation tasks with dependencies | `/buildpad-spec-tasks` |

The same artifact format works in every IDE:

- **Kiro IDE** — use Kiro's **native specs** feature (the Specs panel / `requirements.md`, `design.md`, `tasks.md` workflow). Do not use the `buildpad-spec-*` skills in Kiro; they are the same workflow for agents without native spec support.
- **Claude Code, GitHub Copilot, Antigravity, and other agents** — use the bundled spec skills:
  1. `/buildpad-discovery <idea>` — when unsure whether the work is one spec, many specs, or no spec at all
  2. `/buildpad-spec-init <description>` — initialize the spec structure
  3. `/buildpad-spec-requirements <feature>` — generate requirements (review gate)
  4. `/buildpad-spec-design <feature>` — generate design (review gate)
  5. `/buildpad-spec-tasks <feature>` — generate tasks (review gate)
  6. `/buildpad-impl <feature>` — implement task-by-task with TDD and review
  7. `/buildpad-spec-status <feature>` — check progress at any time

Each stage has a **human review gate**: requirements are approved before design, design before tasks, tasks before implementation. Fast path for a single small spec: `/buildpad-spec-quick <description>`.

## When to Use

- Starting a new project or feature
- Requirements are complex or ambiguous
- Multiple people (or agents) will work on the implementation
- The change is significant enough that "just build it" risks wasted effort

**When NOT to use:** Single-file bug fixes, small refactors, or changes where the spec would be longer than the code.

## DaaS-Specific Considerations

When writing specs for DaaS applications:

- **Data model** (design.md): Use DaaS collection/field schema, not raw SQL design; include standard fields (audit, workflow, scope) per decision tree
- **Check DaaS built-in features first**: Does the platform already provide this? (audit trail, workflow, versioning, RBAC, scoping, cron, import/export) — never spec a rebuild of a built-in
- **API** (design.md): DaaS provides CRUD automatically — spec only custom endpoints
- **UI** (design.md): Name the Buildpad components to use (Buildpad-First rule)
- **Permissions**: Spec the RBAC model (roles, policies, access entries)
- **Workflow**: If content lifecycle needed, spec workflow states and transitions
- **Scope**: If multi-tenant, spec the scope hierarchy (on an Engine project the project is one tenant, and the hierarchy begins beneath its tenant node: no scope type or item without a parent)
- **Testing** (tasks.md): API tests, page tests, and E2E tests are tasks, not afterthoughts

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The feature is simple, no spec needed" | Simple features with unclear requirements become complex features with bugs. |
| "I'll figure it out as I go" | You'll figure out the wrong thing and refactor twice. |
| "The spec will slow us down" | The spec prevents the rework that actually slows you down. |
| "Requirements will change anyway" | Specs can change too — update the artifacts, then the code. The value is in the thinking process, not the document. |

## Red Flags

- Starting implementation without an approved requirements.md and design.md
- Requirements that only cover the happy path (no error cases, edge cases)
- tasks.md with no testing tasks
- No explicit out-of-scope statement in requirements (everything in scope = nothing is)
- Code that drifts from design.md without the design being updated

## Verification

Before moving from spec to implementation:

- [ ] requirements.md: objectives clear, acceptance criteria in EARS format, out of scope explicit
- [ ] design.md: data model, API surface, file structure plan, Buildpad components named
- [ ] DaaS built-in features are leveraged (not rebuilt)
- [ ] tasks.md: small verifiable tasks, dependencies annotated, tests included
- [ ] The user/stakeholder has approved each artifact at its review gate
