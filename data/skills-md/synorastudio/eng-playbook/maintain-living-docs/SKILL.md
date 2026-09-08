---
name: maintain-living-docs
description: Maintain Living Docs without creating sprawl. Use when working on architecture, onboarding, operations, project guides, or implementation that changes durable system knowledge. Use narrower skills for vocabulary, decisions, issues, and handoffs.
---

# Maintain living docs

Keep durable explanatory docs current. Route vocabulary, decisions, work breakdown, and session continuity to their owning skills.

## Update docs when

Update living docs only when the information is:

- Durable beyond the current session.
- Useful to a future agent or human.
- Explanatory rather than definitional or decisional.
- Not better captured in code, tests, issue comments, `LANGUAGE.md`, an ADR, or a handoff.

Skip temporary plans, unresolved speculation, and details that will rot quickly.

## Boundaries

This skill owns living explanatory docs:

- Current system shape in `docs/architecture.md`.
- Operational procedures in focused docs under `docs/`.
- Onboarding or navigation docs that help a future agent or human work in the repo.
- Project-specific guides with durable ownership.

This skill does not own:

- Vocabulary. Use `maintain-language`.
- Hard-to-reverse trade-off decisions. Use `write-adr`.
- Unresolved product or design work. Use `map-decisions`.
- Product scope awaiting review or cross-session execution. Use `write-spec`.
- Work breakdown. Use `write-issues`.
- Session continuity. Use `handoff`.

If vocabulary or decisions dominate the requested update, stop and suggest the narrower skill.

## docs/architecture.md

Keep `docs/architecture.md` as a navigational overview, not an exhaustive spec.

Include what helps a future agent understand the current system:

- Major components and responsibilities.
- Important data or request flows.
- External services and integrations.
- Links to relevant ADRs.
- Pointers to deeper docs.

Avoid speculative future architecture, detailed implementation plans, and duplicated ADR rationale.

## Workflow

1. Read the relevant doc and the code or source artifacts that establish current behavior.
2. Update an existing doc when it already owns the topic. Create a doc only when the topic has durable ownership of its own.
3. Replace stale statements instead of layering corrections beneath them. Link to source artifacts for details that already live elsewhere.
4. Check every changed claim against the current implementation.
5. Report what changed and what you intentionally left undocumented.

Finish when every changed claim matches the current system and no obsolete version of that claim remains in the edited docs.
