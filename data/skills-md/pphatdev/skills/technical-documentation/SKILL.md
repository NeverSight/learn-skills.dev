---
name: technical-documentation
description: Load this skill when writing documentation for engineers - architecture overviews, internals, contributor guides, and decision records. Also load when a change is significant enough to need a written rationale.
user-invocable: true
---

# Technical Documentation

Category: Documentation (Content)

## Purpose

Explain the system to the engineers who build and maintain it: what it is,
why it is that way, and how to work in it.

## Document types

1. **Architecture overview.** Components, each with a one-sentence
   responsibility; the dependencies between them; the data flow for the
   main paths; the trust and failure boundaries. A diagram for structure,
   prose for rationale.
2. **Decision records (ADRs).** One per significant decision: the context
   that forced it, the options considered, the decision, and its
   consequences including what we gave up. Written when the decision is
   made, not reconstructed later.
3. **Contributor guide.** How to set up, build, test, and ship; the
   conventions that reviews enforce; where things live. Test the setup
   instructions on a clean machine or admit you have not.
4. **Internals / deep dives.** For subsystems too complex to read top-down:
   the invariants that must always hold, the lifecycle of its main objects,
   the known sharp edges.

## Standards

- **Why, not how.** The code already says how. Document the constraints,
  history, and reasons the code cannot tell.
- **Audience test.** Write for a competent engineer on their first day in
  this repo - the docs must close the gap between "can code" and "can
  contribute here".
- **Code truth rule.** Docs that contradict the code are worse than no
  docs - they actively mislead. When updating code that has adjacent docs,
  update both in the same change, or flag the doc as stale explicitly.
- **Adjacency.** Keep docs near the code they describe (README in the
  module, ADR in a decisions folder) so changes trip over them.

## Anti-patterns

- Line-by-line narration of the implementation ("this function loops over
  the items...") - that is what the code is for.
- Architecture diagrams without a single sentence saying why the boxes are
  arranged that way.
- Decision records that record only the decision ("we chose X") with no
  context - future readers cannot tell whether X is still right.
