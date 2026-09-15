---
name: execute-spec
description: Execute an approved spec through structured implementation with test traceability. Use when a proposal is approved and the specialist is cleared to write code. Triggered by "implement this spec" or "execute SPEC-XXX".
---

# Execute-Spec — Specialist Implementation

> *"Haces las cosas como para Dios, por eso trabajas con excelencia y dedicación."*

## 1. Purpose

Implement strictly within the approved proposal boundaries with REQ-ID →
test → artifact traceability. Scope expansion requires a new proposal.

## 2. Chain Contract

- Previous: propose-changes (+ review-* approvals)
- Next: quality-gate

## 2b. Role Binding (Org)

- **Bound to:** leaf specialists — `backend`, `frontend`, `devops`, `data-engineer`.
- C-levels dispatch with reference-only packets; specialists never self-dispatch.

## 3. Process

1. Confirm all required approvals are recorded.
2. Create implementation plan via `references/implementation-plan.md`.
3. Implement only files in the approved change list.
4. Produce test matrix via `references/test-matrix.md`.
5. Run quality gates (lint, types, tests, security checks).
6. Hand off to `quality-gate`.

## 4. What I won't do

- Exceed spec scope without a new proposal.
- Skip tests for P0 requirements.
- Modify files outside the approved change list.

## 5. References

- `references/implementation-plan.md` — Steps + order + rollback points.
- `references/test-matrix.md` — REQ-ID to test traceability.
