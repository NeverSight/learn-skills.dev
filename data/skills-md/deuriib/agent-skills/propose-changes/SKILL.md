---
name: propose-changes
description: Produce a structured PROPOSED_CHANGES.md for a spec without modifying repository files. Use when a specialist is ready to implement or a change needs pre-approval.
---

# Propose-Changes — Proposal Without Code

> *"Haces las cosas como para Dios, por eso trabajas con excelencia y dedicación."*

## 1. Purpose

Force design-before-code. The proposal is reviewable; the repo is untouched.

## 2. Chain Contract

- Previous: translate-to-spec
- Next: review-security / review-architecture (as required), then execute-spec

## 2b. Role Binding (Org)

- **Bound to:** leaf specialists (`backend`, `frontend`, `devops`, `data-engineer`)
  and owning C-levels for domain proposals.

## 3. Process

1. Read the target spec (`specs/20_backlog/` or individual spec file).
2. Produce `specs/40_workspace/<agent>/PROPOSED_CHANGES.md` via `references/proposal-template.md`.
3. Include risk assessment via `references/risk-assessment.md`.
4. Identify approvers and block until approval.
5. Hand off to `review-security` / `review-architecture` as required.

## 4. What I won't do

- Modify repository files during proposal phase.
- Skip risk assessment for auth, data, or external-API changes.
- Approve my own proposal.

## 5. References

- `references/proposal-template.md` — Proposed-changes template.
- `references/risk-assessment.md` — Risk matrix + blast radius + rollback.
