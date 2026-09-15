---
name: translate-to-spec
description: Translate an approved Product Brief into domain specs, architecture contracts, and testable requirements. Use after a brief is approved or when a new domain needs spec coverage.
---

# Translate-to-Spec — Brief to Domain Specs

> *"Haces las cosas como para Dios, por eso trabajas con excelencia y dedicación."*

## 1. Purpose

Route the brief to the owning C-levels and produce testable REQ-IDs plus the
canonical architecture contract. The brief is read-only here.

## 2. Chain Contract

- Previous: frame-intent
- Next: propose-changes

## 2b. Role Binding (Org)

- **Bound to:** owning C-levels — `vasquez` (engineering), `barrera` (security),
  `dauhajre` (finance), `subero` (legal), `vera` (marketing), `santana` (people),
  `montero` (revenue), `espinoza` (automation consult).
- `vasquez` consolidates `ARCHITECTURE.md` + `API_CONTRACTS.md`.

## 3. Process

1. Read `docs/briefs/BRIEF-<slug>.md` (reference only, never paste full context).
2. Route to C-levels by domains touched.
3. Each produces a spec using `references/spec-template.md`.
4. `vasquez` consolidates `specs/10_design/ARCHITECTURE.md` and `API_CONTRACTS.md`.
5. Index requirements in `specs/15_requirements/` via `references/requirements-template.md`.
6. Hand off to `propose-changes`.

## 4. What I won't do

- Approve specs without `barrera` review for security-relevant domains.
- Modify the brief (escalate to `frame-intent`).
- Bypass the canonical architecture contract.

## 5. References

- `references/spec-template.md` — Spec with Context/REQ/AC/Contracts/Out-of-scope.
- `references/architecture-template.md` — Architecture contract.
- `references/requirements-template.md` — Requirements index.
