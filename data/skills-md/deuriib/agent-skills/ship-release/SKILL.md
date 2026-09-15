---
name: ship-release
description: Orchestrate release shipping including release notes, changelog, and deployment coordination. Use when verified work is ready to ship or when preparing a tagged release.
---

# Ship-Release — COO Release Orchestration

> *"Haces las cosas como para Dios, por eso trabajas con excelencia y dedicación."*

## 1. Purpose

Turn verified handoffs into a shippable release with notes, changelog,
deployment order, and archival. Never ship without verification gates complete.

## 2. Chain Contract

- Previous: verify-handoff
- Next: none (chain close; lessons captured by owning C-level on PASS)

## 2b. Role Binding (Org)

- **Bound to:** `montilla` (CEO) delegating orchestration to the COO function
  with `vasquez` (CTO) + `devops` for deployment mechanics.

## 3. Process

1. Verify all DoD checklists + gate reports are OPEN.
2. Produce `specs/30_delivery/RELEASE_NOTES.md` via `references/release-notes.md`.
3. Update changelog via `references/changelog-template.md`.
4. Coordinate `devops` deployment with rollback plan.
5. Archive completed spec to `specs/50_archive/`.

## 4. What I won't do

- Ship without verification gates complete.
- Skip changelog for user-facing changes.
- Deploy without a rollback plan.

## 5. References

- `references/release-notes.md` — Highlights/features/fixes/breaking/rollback.
- `references/changelog-template.md` — Keep-a-Changelog format.
