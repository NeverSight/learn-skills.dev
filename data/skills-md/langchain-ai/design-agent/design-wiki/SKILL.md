---
name: design-wiki
description: Design doctrine to weigh on any visual. Hierarchy, typography, colour, layout, platform sizes, chart and diagram principles, and the review rubric critics score against.
---

# Design wiki

What good looks like on a still, a slide, a chart or a frame of film, and why. The making lives in
the production skills (`stills`, `data-viz`, `thumbnails`, `storyboard`, `motion-direction`); brand
facts live in the brand pack (`/workspace/brand/`); this wiki is the shared doctrine they all lean on.

## How to read it

Every page here is either a **rule with evidence** you can check (a standard, a published guide, a
measurement), or a **default to weigh**, marked as such, which a good reason overrides. Brand rules
are not here: they come from the pack, and the pack wins over a default. When a job teaches something
new, save it as an observation (`save_observations`) with its evidence rather than editing this wiki;
a person decides what becomes doctrine.

| Job | Page |
| --- | --- |
| Deciding what the eye sees first; grids, margins, space, safe areas | [references/hierarchy-and-layout.md](references/hierarchy-and-layout.md) |
| Type roles, sizes at the delivered size, line length, casing, legibility | [references/typography.md](references/typography.md) |
| Grounds, the one accent, colour that means something, contrast | [references/color.md](references/color.md) |
| Sizes and specs per platform, with the date they were checked | [references/platforms.md](references/platforms.md) |
| Which chart or diagram, and how to keep it honest | [references/data-and-diagrams.md](references/data-and-diagrams.md) |
| Scoring a piece at a review: areas, anchors, verdicts | [references/review-rubric.md](references/review-rubric.md) |

## The doctrine in brief

**One message, one focal point.** A frame says one thing. Name each separate thing a viewer must
interpret (the headline, a card, a chart): one is the good frame, two is the ceiling, a third is a
second frame. Everything that is not the focal element steps down hard in size, weight or contrast.
(Default to weigh; the attention-demand count is how you check it.)

**Concept before composition.** The visual idea is the real product surface, a specific metaphor, or
bold type. Decorative node, dot or network fields are never a concept (`brand-design`, the kill test).

**Fewest words.** Each fact once. No sub-line, caption, footer, URL or eyebrow the ask did not supply;
the explanation belongs in the reply or the post. Copy the person supplied ships exactly.

**Real over imitation.** The product's real UI, real data with its source, the real logo. A number on
a frame is a claim: it goes in the brief's claims ledger with its source (`content-brief`).

**Contrast is measured, not judged.** Text meets WCAG 2.1 contrast: 4.5:1, or 3:1 for large text
(at least 18 pt, or 14 pt bold); meaningful graphics and UI parts meet 3:1 against what is next to
them ([color](references/color.md)). `brand-lint` measures text contrast against the tokens.

**Size for where it is seen.** The smallest text a person must read has to survive the smallest view
the piece gets: a phone feed, a thumbnail rail, a projector at the back of a room
([typography](references/typography.md), [platforms](references/platforms.md)). A new size is a new
layout, never a scaled or cropped copy.

**Look at the render.** Every gate passing is the floor. You look at the pixels yourself before
anyone else does (`visual-verify`), against the [review rubric](references/review-rubric.md).

## Using the rubric in a review

A critic, a helper or you before delivery scores the piece on the rubric's areas, 1 to 5, each with
the timestamp, the crop or the number behind it, and writes at most a dozen notes ranked by impact,
each marked must-fix or nice-to-have. The verdict follows the rubric's rule (ship, fix then ship,
rework). Two things decide before any score: an invented claim fails the piece outright, and a gate
that could not run (exit 2) is not a pass. Motion adds pacing, sound and finish areas: the film
rubric is in [motion-direction](../motion-direction/references/review.md); the critic brief for a
launch film points at both.

## Where the rules came from

The evidence column of each page names a public, linkable source (a W3C standard, a platform's help
page, a published book or style guide) or says "default to weigh". Platform specs change; each spec
row carries the date it was checked, and a placement that matters is re-checked against the
platform's own page before a final.
