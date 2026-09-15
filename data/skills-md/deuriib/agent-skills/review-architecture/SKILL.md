---
name: review-architecture
description: Review a proposal against the canonical architecture contract and record an ADR. Use when a change modifies public APIs, data models, or cross-cutting concerns.
---

# Review-Architecture — CTO Architecture Review

> *"Haces las cosas como para Dios, por eso trabajas con excelencia y dedicación."*

## 1. Purpose

Validate proposals against `specs/10_design/ARCHITECTURE.md` and record
significant decisions as ADRs. No invariant break without an explicit ADR.

## 2. Chain Contract

- Previous: propose-changes (or review-security)
- Next: execute-spec (only on Approved)

## 2b. Role Binding (Org)

- **Bound to:** `vasquez` (CTO) with `architect` for design input and `espinoza`
  for independent review. Disputes arbitrated by `vasquez`; cross-domain needs
  briefed to `montilla`.

## 3. Process

1. Read `specs/40_workspace/<agent>/PROPOSED_CHANGES.md`.
2. Compare against `ARCHITECTURE.md` + `API_CONTRACTS.md`.
3. Produce/update ADR via `references/adr-template.md`.
4. Issue review via `references/architecture-review.md`.
5. Hand off to `execute-spec` if approved.

## 4. What I won't do

- Approve invariant violations without an explicit ADR.
- Override `barrera` (CISO) on security conditions.
- Modify the architecture contract without an ADR.

## 5. References

- `references/adr-template.md` — Architecture Decision Record.
- `references/architecture-review.md` — Contract compliance + verdict.
