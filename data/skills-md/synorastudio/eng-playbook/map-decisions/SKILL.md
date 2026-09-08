---
name: map-decisions
description: Map unresolved decisions in the configured issue tracker when proposed work has unclear design or Milestone boundaries. Do not use for already-accepted scope or ordinary implementation planning.
---

# Map decisions

Create a tracker-backed Decision Map that makes uncertainty visible and discovers whether proposed work should become one Milestone or a sequence.

Use this workflow only when dependent product or design decisions make the shape of the work unclear. Skip it when the outcome and its main boundaries are already accepted. A Decision Map organizes questions and records accepted answers. It does not invent resolutions, write a Spec, create delivery issues, or authorize implementation.

## Gather the proposed work

Read only the context needed to identify decisions:

- The current conversation and accepted intake summary.
- Relevant `LANGUAGE.md` files, ADRs, and Living Docs.
- Existing code when it establishes current behavior or constraints.
- Related tracker items when they may overlap with the proposed work.

Keep accepted facts separate from assumptions. Treat possible Milestones as candidates until the decisions that shape them are resolved.

## Choose the tracker

Read `AGENTS.md` for the configured issue tracker. If it does not name one, ask where Decision Maps, Specs, and Feature Issues should live, then record that durable choice in `AGENTS.md`.

Create the Decision Map directly in that tracker. Do not save a copy in the repo.

## Create the map

Include only sections that carry real content:

```md
# Map decisions for <proposed outcome>

Status: Draft

## Proposed outcome

## Current boundaries

## Accepted constraints

## Decision branches

## Candidate Milestones

## Resolved decisions

## Resulting Milestones

## Deferred questions

## References
```

Map the decisions that can change product scope, user-visible behavior, system or domain boundaries, data ownership, state transitions, security, external dependencies, or costly-to-reverse choices. Leave reversible implementation details to `implement`.

Order branches by dependency. Identify the branch that blocks the most downstream decisions first.

## Split only substantial decisions

Keep small questions in the Decision Map and record their explicit resolution there. Create a child Decision Issue only when one question needs its own Grilling Session, research effort, prototype, or owner.

Each Decision Issue should state the question, why it matters, known constraints, credible options, the current recommendation when one exists, resolution criteria, consequences, and references. Route it to `grill`, `prototype`, or research as appropriate.

Keep full reasoning in the child issue. When it resolves, add a short linked resolution to the parent map. Use `write-adr` when the accepted answer is hard to reverse, surprising, and resulted from a real trade-off.

## Establish Milestones

A Milestone is a bounded outcome that can be accepted, sequenced, and declared complete. The proposed work may become one Milestone or several. Do not preserve the original feature boundary when the decisions show that another sequence is clearer.

Blocking decisions must resolve before their affected Milestone becomes accepted scope. A deferred question may remain only when it does not threaten that Milestone's outcome or boundaries.

## Keep tracker and Git structure separate

A Decision Map and its Decision Issues create no Git branches by default. When accepted decisions change `LANGUAGE.md`, ADRs, or Living Docs, group repository changes into focused, coherent pull requests according to the target repo's workflow. Do not create a branch per Decision Issue or keep a long-lived branch open merely because the map remains active.

## Keep the map active and route the work

Finish the initial mapping pass when no material decision branch is hidden, the branches are ordered by dependency, each unresolved branch has a named resolution workflow, and candidate Milestones are clearly marked as provisional. Leave the Decision Map active while its blocking decisions remain unresolved.

After every blocking decision is resolved or explicitly deferred outside the affected Milestone, replace candidate Milestones with the resulting Milestone or Milestone sequence. Link each one to its accepted source. Route to `write-spec` when a Milestone needs product review or cross-session continuity, `write-issues` when tracking separate delivery outcomes would help, or `implement` when the accepted work can proceed directly. Close the Decision Map after its resulting work is linked and no blocking decision remains hidden.
