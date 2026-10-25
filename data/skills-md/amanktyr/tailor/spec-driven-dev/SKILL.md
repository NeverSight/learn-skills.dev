---
name: spec-driven-dev
description: Enforces Spec-Driven Development (SDD). Converts user intent into formal specifications, reuse-aware technical architecture plans, and granular, verified task checklists.
---

# Spec-Driven Development (SDD) Skill

Activate this skill when creating non-trivial features, refactoring major subsystems, building multi-file modules, or executing structured engineering workflows.

> **Operational Axiom:** *The specification is the contract. Reuse is the law. Code is the verifiable artifact.*

---

## 1. The Spec-Driven Lifecycle

```
┌────────────────────────────────────────────────────────┐
│ 1. CONSTITUTION: .ai/CONSTITUTION.md                   │
│    Project non-negotiables, intensity, guardrails       │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│ 2. SPECIFICATION: specs/<id>-<name>/spec.md            │
│    User stories, functional requirements, edge cases   │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│ 3. TECHNICAL PLAN: specs/<id>-<name>/plan.md           │
│    AST REUSE AUDIT + file layout + 0-dep verification  │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│ 4. TASK CHECKLIST: specs/<id>-<name>/tasks.md          │
│    Granular task ordering (TRIVIAL -> CRITICAL)        │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│ 5. IMPLEMENTATION & VERIFICATION                       │
│    Atomic changes + unit tests (Exit code: 0)          │
└────────────────────────────────────────────────────────┘
```

---

## 2. Command Reference & Artifact Standards

### A. `/constitution` (`.ai/CONSTITUTION.md`)
Establishes project-wide architectural principles, intensity mode (`lite`, `balanced`, `ultra`, `strict`), testing requirements, and forbidden patterns.

### B. `/spec-new <feature-name>` (`specs/<id>-<name>/spec.md`)
Defines the problem domain and user acceptance criteria:
```markdown
# Feature: [Feature Name]
**ID:** [001] | **Status:** Draft | Proposed | Approved

## 1. Problem Statement & User Value
Clear explanation of what problem this solves and for whom.

## 2. User Stories & Acceptance Criteria
- As a [role], I want [action] so that [outcome].
  - [ ] Given [precondition], when [action], then [expected result].

## 3. Scope Boundaries
- **In-Scope:** Specific capabilities included in this release.
- **Out-of-Scope:** Explicitly deferred or rejected capabilities.

## 4. Edge Cases & Error Handling
- Network timeouts, missing permissions, invalid payloads, race conditions.
```

### C. `/spec-plan <id>` (`specs/<id>-<name>/plan.md`)
Translates specification into a concrete technical architecture plan with a **mandatory AST Reuse Audit**:
```markdown
# Technical Plan: [Feature Name]

## 1. Architectural Approach
High-level module layout, data flow, and state boundaries.

## 2. Mandatory Reuse-First Audit
| Requirement / Capability | Existing Project Match | Decision | Rationale |
| :--- | :--- | :--- | :--- |
| Confirmation Popup | `src/components/ui/Dialog.tsx` | **REUSE** | Parameterize with title/variant props |
| User Profile Fetcher | `src/services/userService.ts` | **EXTEND** | Add `getUserMetadata` method |

## 3. Dependency & Pragmatism Gate
- Proposed New Packages: `0` (Standard library and native APIs only)
- Intensity Mode Compliance: Checked against active constitution level.

## 4. File Layout & Contract Changes
- `[NEW] src/features/billing/components/InvoiceTable.tsx`
- `[MODIFY] src/services/billingService.ts`
```

### D. `/spec-tasks <id>` (`specs/<id>-<name>/tasks.md`)
Breaks the plan into granular, dependency-ordered, complexity-tagged tasks:
```markdown
# Task Checklist: [Feature Name]

- [ ] Task 1 [SMALL]: Extend `billingService.ts` to support invoice query parameters.
- [ ] Task 2 [SMALL]: Implement unit test suite in `tests/unit/billingService.test.ts`.
- [ ] Task 3 [MEDIUM]: Create `InvoiceTable.tsx` reusing existing `Table` and `Badge` components.
- [ ] Task 4 [TRIVIAL]: Register route in navigation sidebar.
- [ ] Task 5 [SMALL]: Run full verification suite and assert clean exit code 0.
```

---

## 3. The Implementation & Verification Loop

When executing `/spec-implement <id>`:
1. Work sequentially through `tasks.md` from top to bottom.
2. Complete each task atomically: write code, write corresponding unit test, execute test.
3. Mark task completed (`- [x]`) in `tasks.md` only after verifying exit code 0.
4. If a test fails, halt and resolve the failure before advancing to the next task.
