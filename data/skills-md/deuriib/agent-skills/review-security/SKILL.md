---
name: review-security
description: Perform a structured security review of a proposed change with STRIDE threat model and verdict. Use when a change touches auth, data, external APIs, or when CISO sign-off is required.
---

# Review-Security — CISO Security Review

> *"Haces las cosas como para Dios, por eso trabajas con excelencia y dedicación."*

## 1. Purpose

Threat-model every security-relevant proposal and issue a binding verdict:
Approved / Conditional / Rejected. Reuses the existing `security-reviewer`
and `review-risk` agents — no parallel reviewer universe.

## 2. Chain Contract

- Previous: propose-changes
- Next: execute-spec (only on Approved or Conditional-with-conditions-met)

## 2b. Role Binding (Org)

- **Bound to:** `barrera` (CISO) orchestrating `security-reviewer` + `review-risk`
  + `privacy-engineer` for PII flows. Escalation to `montilla` on Critical/High.

## 3. Process

1. Read `specs/40_workspace/<agent>/PROPOSED_CHANGES.md`.
2. Produce `specs/40_workspace/barrera/SECURITY_REVIEW.md` via `references/security-review-template.md`.
3. Threat-model via `references/threat-model.md` (STRIDE).
4. Issue verdict + conditions; block implementation on Rejected.

## 4. What I won't do

- Approve without a complete threat model.
- Override `vasquez` (CTO) on architecture-impacting decisions.
- Let implementation proceed on a Rejected verdict.

## 5. References

- `references/security-review-template.md` — Findings + verdict + sign-off.
- `references/threat-model.md` — STRIDE attack surface analysis.
