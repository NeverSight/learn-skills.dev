---
name: decision-records
description: >-
  Document significant technical and architectural decisions as lightweight
  Architecture Decision Records (ADRs). Use this skill when `workflow/SPEC.md`
  or `workflow/PLAN.md` introduces a hard-to-reverse choice, cross-cutting
  trade-off, new dependency, or protocol/schema change worth preserving for
  future contributors.
---

# Decision Records (ADRs)

Capture **why** important technical decisions were made—along with alternatives considered and trade-offs accepted—in concise, immutable Markdown records.

## When to Create an ADR

Create an ADR when a change involves:

- A **hard-to-reverse** architectural or data-model choice.
- A **cross-cutting trade-off** affecting multiple modules, services, or teams.
- Adding or replacing a core dependency, protocol, storage engine, or integration pattern.

**Skip ADRs** for routine implementation details, local refactorings, or easily reversible choices—those belong in `workflow/PLAN.md` or code comments.

## Storage & Naming

- Store records in `docs/decisions/` (or `docs/adr/` if the repository already uses that convention).
- Name files sequentially with a lowercase hyphenated slug:
  `docs/decisions/0001-short-decision-title.md`
- Start from the template in [ADR.md](./resources/ADR.md).

## Rules

1. **Link with `workflow/`**: Reference the ADR from `workflow/PLAN.md` (and `workflow/SPEC.md` if applicable) so design context stays connected.
2. **Keep it concise**: Focus on context, decision, alternatives rejected, and consequences—avoid turning an ADR into a tutorial or full specification.
3. **Immutable history**: Once accepted, do not rewrite an old ADR's intent; if a decision changes later, create a new ADR that marks the previous one as `Superseded by <ADR-XXXX>`.
