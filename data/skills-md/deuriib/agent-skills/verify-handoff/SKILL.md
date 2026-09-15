---
name: verify-handoff
description: Verify completed implementation meets Definition of Done and produce a structured handoff. Use when a specialist declares work complete and it needs review before shipping.
---

# Verify-Handoff — Definition of Done Verification

> *"Haces las cosas como para Dios, por eso trabajas con excelencia y dedicación."*

## 1. Purpose

Run the full DoD checklist against spec + test matrix + open gate report, then
produce HANDOFF.md routing to the next agent. No gate OPEN, no handoff.

## 2. Chain Contract

- Previous: quality-gate (must be OPEN)
- Next: ship-release (on complete) or execute-spec (on findings)

## 2b. Role Binding (Org)

- **Bound to:** owning C-level gate (`vasquez` / `barrera` / domain owner) with
  `montilla` synthesizing cross-domain handoffs.

## 3. Process

1. Read spec + test matrix + `GATE_REPORT.md`.
2. Run DoD via `references/dod-checklist.md`.
3. Produce `specs/40_workspace/<agent>/HANDOFF.md` via `references/handoff-template.md`.
4. All gates pass → hand off to `ship-release`.
5. Gates fail → return to `execute-spec` with specific findings.

## 4. What I won't do

- Approve without the full DoD checklist.
- Skip security verification for security-relevant specs.
- Allow shipping without doc updates.

## 5. References

- `references/handoff-template.md` — Deliverables + DoD + next agent.
- `references/dod-checklist.md` — Functional/quality/security/docs gates.
