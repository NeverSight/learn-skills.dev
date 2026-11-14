---
name: b3-figure-drawing
description: |
  Draw a figure for a document — comparison, process, ranked numbers, layered
  architecture, two-variable plot, claimed-vs-verified gap, or a timeline.
  Produces greyscale serif SVG: no colour at all, real axes, sentence legends,
  and a built-in dark mode. Load when writing a report, wiki page, paper, or
  deck that has a shape reading would lose. Not for decorative diagrams, and
  not for knowledge graphs.
metadata:
  version: "1.1.2"
  library: figlib.mjs
---

# b3-figure-drawing

Eight builders that take content and own every coordinate. You never hand-write
SVG, and you never pick colours, because there are none.

Needs Node 18+ on PATH. No dependencies, no build step.

## Decide whether to draw at all

Draw when the section has **a shape that reading loses**. Skip when it is pure
argument, an unordered list, or one number standing alone — a figure that
restates the paragraph above it just takes up room.

| Shape | Builder | Signal in the text |
|---|---|---|
| Comparison | `compare` | two or three things side by side, each with matching attributes |
| Process or loop | `flow` | steps in sequence, especially when the last returns to the first |
| A row of numbers | `bars` | price, duration, benchmark — any table with a ranking |
| Layered architecture | `layers` | tiers nested inside tiers, especially with a boundary cutting across |
| Two variables | `plot` | break-even threshold, trend line, crossing point |
| One number measured twice | `gap` | "the source says 180K, verification says 247K" |
| Points in time | `timeline` | a roadmap by week, product generations, historical eras |
| Grid of lists | `matrix` | SWOT, a 2×2 matrix, pros and cons — each cell is its own bullet list |

Two to four figures per document is the working ceiling. More than that is a
sign of drawing to fill a quota.

## Three pairs are easy to confuse

Picking wrong still produces a figure. It just loses the reason you drew it.

**`flow` vs `timeline`.** Both show order. `flow` has *no axis* — its steps sit
evenly apart because sequence is the point. Use `timeline` only when the
distance between points carries meaning: six quiet years then three frantic
months has to *look* like that. Eight weeks inserted at the front of a roadmap
push everything after them, and only a real axis shows it.

**`compare` vs `matrix`.** Both put boxes side by side. `compare` gives every
item its own box and lines the rows up, so it only works when item 2 on the left
*corresponds* to item 2 on the right. SWOT cells don't correspond: the third
strength has nothing to do with the third weakness, and `compare` draws rows that
imply they do. Lists that belong to a cell, not to a row → `matrix`.

**`bars` vs `gap`.** Both compare numbers. `bars` ranks **independent**
quantities. `gap` is **one** quantity measured twice, and the connector's length
is the finding. Three different numbers → `bars`. One number where the source
and the verification disagree → `gap`.

## Style is not yours to choose

- **No colour, only weight.** Five tones, darkest first: `ink` (solid fill,
  reversed-out text — for the thing being emphasised) · `mid` · `pale`
  (default) · `open` (outline only) · `hatch` (45° hatching).
- **Four categories is the ceiling.** Past that the ramp runs out. Split into
  two figures; never invent a fifth grey, because adjacent greys stop being
  distinguishable.
- **Legends are sentences** under the figure, not a key box in the corner.
- **Every string you pass in is prose, and `b3-write-human` owns the prose
  rules.** Load that skill before you write a title, label, legend, or note,
  and don't restate its rules here: a second copy drifts. For Vietnamese,
  its "Vietnamese output" section ends with four rules written for text
  inside a figure: every label is a sentence with a subject, full
  diacritics everywhere, the title is a name with no "nháp" or date, and a
  label may drop the English gloss in parentheses when the paragraph beside
  the figure or the caption already carries it. Those four come from the
  three things that actually went wrong in a figure on 22/10/2026.
  `van-ngan-tieng-viet.md` next to it covers short strings: one concept
  keeps one name across the figure, a verb plus an object beats a noun pile,
  no hook phrases. Labels feel like data, which is why they skip the pass.
  They aren't.
- **A title is a name and a note says what the eye can't get.** The page
  carries status and date; the reader is already looking at the layout. If
  deleting `note` loses nothing, leave it out.
- **Vietnamese numbers** in Vietnamese documents: `61,5%` not `61.5%`. `vnum()`
  handles it; pass `digits` when a money column needs even decimals.
- Numbers in a figure must match numbers in the text and carry the same
  sourcing. A figure is not a place to estimate.

## How to run it

`figlib.mjs` sits **next to this SKILL.md**. Import it by absolute path — you
know that directory, because it is the one you just read this file from. If you
lost it, `find ~/.claude -name figlib.mjs -not -path '*/node_modules/*'` finds
it.

Write a small script to a temp file and run it with plain `node`:

```js
import { gap, render } from '<skill-dir>/figlib.mjs';

render('/tmp/fig1-chi-phi.svg', gap({
  title: 'Chi phí vốn: con số khai và con số kiểm chứng',
  axisNote: 'Chi phí mỗi người dùng trả tiền, mỗi tháng (USD)',
  ends: ['bên khai', 'kiểm chứng'],
  digits: 2,
  rows: [
    { label: 'Gói Solo', from: 3.85, to: 3.29, note: 'khai cao hơn thực' },
    { label: 'Gói Team', from: 9.2, to: 11.69 },
  ],
  note: 'Mũi tên chỉ về phía số đã kiểm chứng.',
}));
```

**Read the docstring above the builder you picked** in `figlib.mjs` for its
parameters. They are documented there and only there — this file deliberately
does not restate the API, because a second copy drifts.

## Always look at what you drew

An SVG that parses is not an SVG that reads. Open it, or rasterise it with
whatever headless browser the machine has:

```bash
chromium --headless --disable-gpu --hide-scrollbars \
  --screenshot=/tmp/fig1.png --window-size=940,420 file:///tmp/fig1-chi-phi.svg
```

`chromium`, `google-chrome`, or a Playwright Chromium under `~/.cache/ms-playwright/`
all work. Add `--force-dark-mode --enable-features=WebUIDarkMode` for the dark
check. The palette is declared as CSS custom properties inside the SVG with a
`prefers-color-scheme` block, so one file serves both themes — but check it,
because a reversed-out tone is where mistakes hide.

Things that have actually gone wrong, worth looking for: text vanishing on a
dark fill, an axis label printing as `0,6000`, a line label running off the
right edge, and two dots merging into one lump when their values are nearly
equal.

## Hard rules

1. **Never hand-write SVG.** If no builder fits, say so rather than improvising
   one — the style holds together because every figure goes through the same
   frame, legend, and palette code.
2. **`gap` takes one unit per figure.** The axis is shared, so mixing "247
   thousand stars" with "13 years old" flattens every other row against the
   left edge. Split instead.
3. **No log scale.** It makes a gap look smaller, which is the opposite of why
   that figure exists.
4. **`gap` starts at zero by default.** Passing `min` crops the axis and
   exaggerates the difference; if you crop, say why in `note`.

## Where the style came from

The four figures drawn for an AI4Econ&Biz 2026 conference paper: serif
typeface, no hue anywhere (19 distinct greys across the four files), category
carried by fill weight plus hatching, real axes with tick labels and dashed
reference lines, and legends written as full sentences under the figure. The
library adds the one thing print did not need — a dark palette, because these
figures are read on screens.
