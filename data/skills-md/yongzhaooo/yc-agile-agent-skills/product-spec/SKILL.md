---
name: product-spec
description: Create or revise a project's living product spec (docs/product.md), the current expected shape of the product, and its required reader overview (docs/overview.md), a short illustrated page for people. Use when the user asks to write or update the product spec or overview, or when a settled decision changes what the product should be. Not for one change's plan (plan-work) or progress state (wayfinder).
---

# Product Spec

`docs/product.md` states what the product should be now: the destination. Wayfinder
records where the work stands; code and tests record what exists; a change plan records
how one change gets made. Keep one product spec per project. If the project already has
an equivalent authority, revise that instead of creating a competitor.

## When to update

Update on events, not on a calendar:

- a grilling round, pilot result, review, or user decision settles a change to the
  product's shape;
- a wayfinder route reassessment finds an expectation no longer holds;
- the user changes an expectation.

Update the spec in the same change that alters the product's shape. Work that leaves the
shape unchanged does not touch it. Every spec change also brings `docs/overview.md` up to
date (see Keep the overview).

## Write it

- Present tense, current expectations only. Replace a superseded expectation in place;
  history lives in Git and dated change specs.
- Write each expectation as observable behavior: who or what, what happens, and how one
  could tell it holds. Group by user-facing capability, not by implementation module.
- List consciously excluded shapes under Non-goals.
- List undecided shape questions under Open questions, each with what it blocks. The user
  settles them; writing the spec does not.
- Mark expectations the user has not confirmed with `(proposed)`. `Last confirmed` is the
  date the user last confirmed the whole document, or `not yet confirmed`; partial edits
  do not refresh it.
- Link detailed contracts such as API docs or schemas instead of copying them. Keep the
  document readable in one sitting.

For a new spec, draft from the user's statements, the README, and the wayfinder Project
outcome; ask only for shape decisions you cannot find. When the project has
`docs/wayfinder.md`, link the spec's actual path from its Project outcome.

```markdown
# <Product> product spec

Last confirmed: <YYYY-MM-DD | not yet confirmed>

## Purpose
<who it serves and the result it delivers>

## Expectations
### <capability>
- <observable expectation>

## Non-goals
- <excluded shape>

## Open questions
- <question>; blocks: <what>
```

## Keep the overview

Every project with a product spec also keeps `docs/overview.md`: one page that lets a
stakeholder or new team member understand the product in about five minutes. This skill
owns it. Create it with the spec, and update it in the same change whenever the spec, the
blueprint's target structure or route, or a recorded decision changes what it says. A spec
without a current overview is incomplete; when you touch such a spec, add the overview.

The overview is a reading copy, not an authority. Every statement comes from the spec,
the blueprint (`docs/architecture.md` or the project's equivalent roadmap) or a recorded
decision. Fix a conflict in the owning document first, and say plainly when something is
not yet agreed. Task status stays in wayfinder; the overview links to it.

Write it in plain language for its audience:

- what the product is, who it serves and why, in two or three sentences;
- at least one diagram of how it works or the target picture, plus a route diagram when a
  blueprint or roadmap exists;
- what it will and will not do;
- the route at milestone level, with dates only where the blueprint gives them;
- the decisions needed from readers, taken from the open questions;
- links to the spec, the blueprint and the wayfinder map.

Keep each diagram's source (Mermaid, Graphviz, SVG) beside its rendered image so it can
be regenerated, and check the rendered image is legible in each format readers receive; a
Word page shrinks wide diagrams until the text is unreadable. Produce Word or PDF copies
only when the audience needs them, regenerated from the Markdown. Write the prose without
AI writing patterns, using `humanizer` when available.

## Boundaries

Editing the spec does not authorize implementation. When code and spec disagree, report
the gap; change either side only under authority for that change.
