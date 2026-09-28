---
name: duo-design
description: UI patterns from the Duolingo design system — juicy motion, the character system as the emotional channel, design tokens (color/type/spacing), sound as a UX surface, accessibility as a default not a checklist, and "error-as-delight" detailing. Use when the user is designing a screen for a gamified or learning product, reviewing a design for "why does this feel flat," picking a motion system, building a character mascot, or auditing for accessibility. This skill owns design *rationale*; pixel craft (easing values, contrast ratios, component props) routes to the design-engineering skill.
license: MIT
metadata:
  author: HKTITAN
  version: "1.0.0"
  graph: true
---

# Duolingo Design — Map of Content

Duolingo has no public design-system site: `design.duolingo.com` 301-redirects to `blog.duolingo.com/hub/design/`, a four-post curated hub (checked 2026-09-22). So these nodes are built from the design and engineering posts on the blog, and they carry *patterns and rationale*, never literal tokens.

For the craft layer — easing curves, duration tables, contrast ratios, focus rings, component APIs — hand off per [[../duolingo/references/design-handoff]].

This skill is structured as a **graph**: scan the descriptions below, follow only the `[[wikilinks]]` you need.

## Motion and feeling

- [[references/juicy-motion]] — the bouncy, slightly-overshot easing curves that make every interaction feel responsive.
- [[references/celebration-design]] — visual grammar for "you did the thing" — confetti, scaling, character cameos.

## The character layer

- [[references/character-system]] — Duo and friends as the emotional API of the product; how to build one for any brand.

## Tokens

- [[references/color-tokens]] — the role/value split (e.g. *correct-feedback* vs. *green-500*) that lets a brand evolve without rewriting screens.
- [[references/type-system]] — Feather Bold, weight rules, and the legibility-first hierarchy.

## Surfaces

- [[references/sound-as-ux]] — non-optional audio feedback; cheap to add, disproportionately rewarding.
- [[references/progress-bars]] — the most important UI element in a gamified product, treated as such.
- [[references/bottom-bar-navigation]] — five tabs, character-icon recognition, never moves.

## Deciding what to build

- [[references/prototype-the-extremes]] — explore by pushing each competing value to its maximum as a separate direction, then harvest the breaking points.
- [[references/consistency-vs-purpose]] — consistency lowers learning cost and simplicity raises clarity; when either stops paying, tier the system instead of applying one rule everywhere.
- [[references/craft-pass-guardrail]] — how to fund and measure a pure polish project without pretending it will move the core metric.
- [[references/design-for-many-ship-one]] — build the layout for N at launch even when you enable one, so the later experiment costs an analysis rather than a redesign.

## What the interface claims about the user

- [[references/required-path-not-optional-branch]] — optional depth reads as skippable; put the behaviour you want on the main route and serialize for depth.
- [[references/capability-labels]] — name levels and units by what the user can do afterward, anchored to an external standard where one exists.
- [[references/label-the-hard-thing]] — telling users a task is hard before they attempt it raises tolerance for failing and pride in passing.

## Defaults

- [[references/accessibility-default]] — color-not-only, type-scaling, motion-reduce, screen-reader paths as ship blockers, not nice-to-haves.
- [[references/error-as-delight]] — an error state is a free chance to be the brand instead of break it.

## Sibling skills

- [[../duo-gamification/SKILL]] — *juicy-feedback* is design + gamification; the implementation lives here.
- [[../duo-voice/SKILL]] — celebrations and errors are also a copy problem.
- [[../duo-retention/SKILL]] — the bottom bar exists because retention requires a stable home.

## Sources

- blog.duolingo.com/hub/design/ — the four-post design hub (what `design.duolingo.com` now redirects to, as of 2026-09-22)
- @duolingo product surfaces — observed motion and sound
