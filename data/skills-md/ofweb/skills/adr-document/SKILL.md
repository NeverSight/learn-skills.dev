---
name: adr-document
description: Create or revise an architectural decision record when Shape or Design settles a durable architectural trade-off.
---

# Architecture decision record

An ADR preserves an applicable architectural choice and its rationale. Shape may create one only when architecture must be settled for feature feasibility, observable behaviour, or boundaries. Design may create one for a durable choice in implementation structure. Implementation returns new architectural questions to Design.

## Decide if a record is needed

Create an ADR when changing the choice later has meaningful cost, future contributors could reasonably reverse it without its rationale, and the choice resolved a real trade-off. Keep routine implementation choices in code. Do not create a record for an unresolved option or the only practical choice.

Read related ADRs, Feature Briefs, PDRs, and relevant code before creating a record. Check for an existing ADR that owns the same decision. Store current records in `.workflow/decisions/adr/`. Give each record the next unused `ADR-0001` style ID and a matching `0001-short-title.md` filename. Check Git history before assigning an ID so deleted IDs are not reused. Keep the ID and filename stable while the decision applies.

If a record exists outside the canonical location, do not create a duplicate or migrate it in this skill. Ask for a separate migration.

## Record the decision

Use this compact structure. Omit optional sections with no useful content.

```markdown
# ADR-0001: Short title

Status: Accepted

## Context

## Decision

## Rationale

## Scope

## Consequences

## Alternatives considered

## Related records
```

State the architectural question or constraint in Context. State the choice in Decision and its reasons in Rationale. Bound its authority in Scope. Include non-obvious consequences and rejected alternatives only when they help a future contributor apply or reconsider the choice. Link affected Feature Briefs, PDRs, Context terms, or code. Tell the owning workflow which Feature Briefs must link back to this ADR.

An ADR is authoritative within its stated scope. Revise or replace a changed decision so the current constraint is clear. Delete an obsolete ADR when nothing current depends on it. Update affected links after a revision, replacement, or deletion. Git preserves older decisions.

Do not include feature requirements, acceptance criteria, an implementation plan, an architecture tour, copied code structure, or a discussion transcript.

## Size and validation

Aim for 200–400 words. The hard limit is 700 words. Near that limit, remove stale context and repeated detail. Link canonical material instead of copying it.

Invoke `concise-prose` before writing or revising the ADR. Follow its STE100 and
Vale repair loop until `prose-check` passes. Install `workflow-document-check`
alongside this skill and run it after edits. Check the ID, status, scope,
rationale, and links before finishing.
