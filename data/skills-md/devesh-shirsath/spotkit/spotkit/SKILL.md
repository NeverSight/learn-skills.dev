---
name: spotkit
description: Generate minimal, abstract, UI-inspired illustrations for software product features — as deterministic SVG. Use when asked for a feature illustration, product illustration, spot illustration, empty-state graphic, feature-card artwork, docs or developer-portal illustration, or a consistent illustration set/family for a product. Also use to turn a feature description or a product screenshot into an abstract UI illustration, to add a new illustration to an existing family, or to retheme an existing set.
---

# Spotkit

Turn a feature description into a quiet, abstract illustration that looks like a
product interface reduced to its most recognizable primitives.

The governing principle:

> **Abstract the interface, not the idea.**

Someone should look at the result and think *"I understand what this feature
does"* — not *"that's a screenshot of the product."*

## Output format

**Default to SVG.** This style is pure geometry — hairline borders, exact radii,
repeated placeholder bars, one stroke weight. Writing it directly gives exact,
repeatable output and makes every illustration in a set provably identical in
treatment. Image models fail at precisely these things, and fail hardest at
consistency across a set.

Use `references/image-prompt.md` only when the user explicitly wants a prompt for
an external image model.

## Workflow

**Read `SPEC.md` first.** It holds every number, the SVG template, the building
blocks and a complete example — enough to draw from. The references below are
for the decisions; open one only when a step needs it.

1. **Interpret the feature.** One sentence: what does it actually do?
   → `references/metaphor.md`
2. **Choose the metaphor.** What *relationship* is this feature about — grouping,
   connecting, gating, packaging, reviewing, sequencing?
3. **Pick 2–5 primitives** that carry that relationship. Not more.
4. **Pick one of the twelve layouts — then adapt it, don't invent.**
   → `SPEC.md` §7. Choose by the relationship, then by how many elements the
   idea needs, then by what its neighbour already uses.
5. **Start from that layout's example file** (`SPEC.md` §7 names it) and keep
   its geometry: panel, backdrop, float, card sizes and positions. Change only
   the content — the icon, what sits inside the cards, how many rows within the
   layout's limit. Icon paths come from `references/icons.md`. If you can run
   Python here, copy the layout's function in `build.py` and edit its content.
6. **Check it.** Run `python3 check.py your.svg` if you can, then the list in
   `SPEC.md` §9. Simplify what they flag.

If the concept is genuinely ambiguous, offer 2–3 **conceptual** directions before
drawing — different metaphors, never different styling.

## The standing rule: adapt, don't invent

Composition is where models drift. Given the same brief, one run that adapted
the Split layout produced something that sat in the family at a glance; another
that invented a new arrangement produced a busier, off-centre piece that didn't —
and the same brief in a different tool drifted further still. The twelve
layouts have been balanced against each other; a fresh composition has not.

So, every time, in every tool:

- **Adapt the nearest layout.** Its geometry is fixed; its content is yours.
  Invent a new composition only when none of the twelve can carry the
  relationship — and say so in the delivery note, naming the rule that forced it.
- **Centred and square.** Weight on x=80, filling the 160 square. A landscape
  strip with empty space above and below is not a spot illustration.
- **Few, large elements.** Nothing that carries meaning is smaller than 9 units
  — that is 9 pixels at display size. If an idea needs more detail than that, it
  needs fewer elements, not smaller ones.
- **Show change as states.** A flow reads fastest as before → after: two cards
  and an arrow (L12), or one rail (L11). Not a rail *and* cards *and* a badge.
- **Never improvise a value.** Every number, colour and snippet comes from
  `SPEC.md`. If a value you need is not there, reuse the nearest one that is.

## What is fixed and what is yours

The skill separates the method from the look.

**Fixed — these hold for any illustration in this genre:**

- Abstract the interface, not the idea
- Text-independence — it must read with every label removed
- One dominant visual idea per illustration
- ~20–40% of real UI fidelity
- Legible depth hierarchy, *however* it is achieved
- Whitespace as structure, not leftover space
- Restraint: few icons, few colors, one interaction cue
- Internal consistency across a set

**Yours — set once per project, then inherited by the whole family:**

elevation model · edge treatment · overhang · corner language · stroke weight ·
icon style · palette · accent · density

A coherent combination of those is a **style spec**. One ships today — *soft
shadow, fade-out edge, overhanging float, generous radii, hairline strokes,
monoline icons, warm grayscale, optional single accent, sparse density* — and it
is what `assets/` and `examples/` implement. Additional directions are additive;
nothing in the method changes when one is added.

## Invariants of the shipped spec

- **One base panel, sized to its content.** Not a fixed box — a timeline gets a
  narrow frame, a table of rows a wide one. Its edge either fades (open bottom:
  *there is more*) or is contained (closed: *this is all of it*). Choose by
  meaning.
- **One thing carries the shadow.** Usually a floating element breaking past
  the panel's edges; sometimes a raised row or the middle card of a fan. (The
  corner-chip layout's diagonal pair counts as one.)
- **The elevation goes on the record being acted on**, not on a decorative circle
  above it. When a medallion sits over a prominent first row, the row floats and
  the medallion stays flat.
- **Placeholder bars, never words**, always short-over-long, never equal widths.
- **A backdrop is optional and varied** — none, a plate, an offset sheet, or a
  twin stack. The same plate behind every illustration is what makes a set look
  mechanical.
- **One stroke width and one stroke colour, everywhere.** Width 0.5, `--il-line`.
  Hierarchy comes from fills, opacity and elevation — never line weight.
  Separators are filled hairlines, not strokes.
- **Equal top and bottom padding inside every card**, bottom never zero. This
  fails silently more than anything else here — verify it by arithmetic.
- **The panel sits above its backdrop**, and no two sheets share a top edge.
- **Nothing overlaps what it sits between.** A glyph in a gap fits inside it
  with clearance; a rail is capped by its first node. `build.py` has guards
  (`fits`, `rail`, `padded`) that raise rather than ship these — use them.
- **One icon family, one radius language, one shadow** across the entire set.
- **Every card carries a hairline**, not just a shadow — at 160px there is no text
  to hold the hierarchy, so the surfaces have to, and a shadow alone does not
  separate white on near-white.
- **The last content block sits inside the fade** and half-dissolves. That
  half-visible row says "and more" without adding anything. Equally: nothing
  *important* may land below `y=112`, or it dissolves mid-content.
- **Vary the layout, never the language.** Monotony is the failure mode of this
  style — a set where every piece is "header card, then rows" reads as one image
  twelve times. See `archetypes.md`.

## Two things that will bite you

- **Icons are Phosphor `regular`, filled, on a 256 grid.** Set `fill`, never
  `stroke`. Bold reads heavy against 0.5-unit structural strokes. Paste the
  paths from `references/icons.md`; never draw a glyph yourself.
- **CSS custom properties do not cross into `<img>` or `<object>`.** An SVG
  loaded that way shows fallback colors forever and will not follow dark mode.
  Inline the markup to theme it — and suffix every `id` when you do, or masks
  and filters cross-apply between illustrations.

## Reference files

Read the one you need; don't load them all.

| File | Read it when |
|---|---|
| `SPEC.md` | **Always, first.** Every number, the template, one full example. |
| `references/examples.md` | You picked a layout — its finished SVG, to adapt. |
| `references/icons.md` | You need an icon — paste-ready Phosphor paths. |
| `references/metaphor.md` | Translating a feature into a concept. Catalog of ~24 common SaaS features. |
| `references/archetypes.md` | Choosing a layout. Twelve compositions and the four choices that generate them. |
| `references/primitives.md` | You need the reasoning behind a building block. |
| `references/theme.md` | Colors, tokens, light/dark, accent rules, deriving your own palette. |
| `references/scaling.md` | Any canvas that is not a ~160px square. |
| `references/screenshots.md` | The user supplied a screenshot of the real UI. |
| `references/sets.md` | Producing or extending a family. |
| `references/checklist.md` | Before delivering. Always. |
| `references/image-prompt.md` | The user explicitly wants an image-model prompt. |

## Delivering

The minimum useful answer is a short concept note plus the SVG:

> **Feature interpretation** — one line.
> **Metaphor** — one line.
> **Primitives** — the 2–5 used.
> **The SVG.**

Don't pad it with explanation the user didn't ask for.

## Assets

- `assets/illustration.css` — token definitions, light and dark. Drop into a site.
- `examples/` — twelve exemplars, one per layout.
  Open `examples/gallery.html` for the contact sheet in both themes.
- `icons.py` — embedded Phosphor geometry (regular is what the system uses;
  bold is kept for anyone who wants a heavier variant).
- `check.py` — lints an SVG against the rules that fail silently
  (`python3 check.py file.svg`), and the docs against `build.py` (`--docs`).
- `build.py` — the generator that produced them. Every constant in one place;
  change one and the whole family moves together. Worth copying for any set
  larger than about eight.
