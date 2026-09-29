---
name: pdr-document
description: Create or update a product decision record when Direction or Shape has a durable product or behavioural choice whose rationale matters beyond one Feature Brief.
---

# Product decision record

A PDR records an applicable product or behavioural choice and its rationale.
Direction or Shape decides when the choice needs a record. Create it only after
the user makes a durable decision whose reasoning matters beyond one local
Feature Brief. Architecture belongs in an ADR. Small reversible choices need
no PDR. Keep unresolved candidates in Direction, Backlog, or discussion.

## Create or update

Read related PDRs and Direction, Backlog, and Feature Brief material that bears
on the decision. Check for an existing record before creating one. Store PDRs in
`.workflow/decisions/pdr/`. Give each record the next unused `PDR-0001` style
ID and name its file `0001-short-title.md`. Do not reuse a deleted ID; check
Git history when needed. Keep the ID and filename stable while the record applies.
If the decision already has a record elsewhere, do not create a duplicate or
migrate it in this skill.

Use this compact structure. Add optional sections only when they help a future
reader understand or revisit the choice.

```markdown
# PDR-0001: Short title

Status: Accepted

## Context

## Decision

## Rationale

## Scope

## Consequences

## Assumptions and reconsideration

## Alternatives considered

## Related records
```

Omit optional sections with no useful content.

State the question or constraint in Context. State the choice in Decision and
the reasons in Rationale. Bound its authority in Scope. Record consequences,
assumptions, and rejected alternatives only when they matter later. Link the
Direction material, Backlog items, Feature Briefs, or other records that depend
on the decision. Do not copy their content into the PDR.

Tell the owning workflow which affected Feature Briefs must link to the PDR.

The PDR directory contains current decisions, not a decision archive. Revise
the same PDR when the answer changes within its durable question and scope.
Keep its ID and inbound links. Create a new PDR for a different or independent
decision. Delete an obsolete PDR when nothing current depends on it. Update
affected links when a record is removed or its scope changes. Git preserves
earlier answers. Surface conflicts with other current PDRs rather than silently
choosing one.

Aim for 150–300 words; the hard limit is 500 words. Near that limit, remove
stale context, repeated material, and optional sections that add no useful
information. Prefer links to canonical sources. Do not retain old status or
rationale solely for history.

Do not include discussion transcripts, option matrices, full feature
requirements, implementation plans, or status tracking. Invoke `concise-prose`
before writing or revising the PDR. Follow its STE100 and Vale repair loop until
`prose-check` passes. `workflow-document-check` must be installed
alongside this skill; use it after the edit.
Prune or restructure after a hard-limit failure. Check the ID,
status, scope, and links before finishing.
