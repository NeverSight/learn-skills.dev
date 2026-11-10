---
name: grid
description: >-
  Lay out any page on the Stripe and Mintlify grid structure, the version the
  user iterated to: two vertical rails with space on the left and right, no
  lines in the middle, no grid in the opening block, whole sections that start
  on full-width hairlines meeting the rails, one line weight and colour, and
  flat hairline cells whose edges are the rails. Works two ways: building a
  new page, or retrofitting an existing site in its own tokens and rules
  (Next.js, plain CSS, CSS modules, Tailwind). Use whenever building or fixing
  a layout, "the grid structure", "grid my site", "Stripe grid", "Mintlify
  grid", rails, borders, section lines, bento cells, or when lines look
  disconnected, doubled, misaligned or cross into the art.
---

# Stripe grid

The user's own definition: "there is a space from the left and from the
right, and a little bit from the top. There is no grid in the middle, as you
could see from Stripe and Mintlify." Read this whole file before drawing a
single line. Every rule below is a correction the user had to make.

Reference CSS in `reference/`: `GridFrame.module.css` (the rails),
`section.module.css` (sections, cells, helpers) and `audit.js` (the check).

## 0. Two modes

**Building a new page**: use the structure and the defaults below as they
are.

**Retrofitting an existing site** ("grid my site"): the structure below is
the skill; the values come from the site. Do these in order.

1. **Read the site's own rules first**: AGENTS.md, CLAUDE.md, the global
   tokens file (`globals.css`, a Tailwind theme), and the comments in the
   page's CSS. Where the site and this skill disagree on a value (a gap, a
   width, a colour), the site wins. This skill supplies the structure, not
   the numbers.
2. **Work on a copy.** A git worktree on its own branch, its own dev server
   on its own port. Never edit the user's live checkout, never push. Show
   the original and the gridded page side by side.
3. **Map, do not invent tokens.**
   - Rails stand **half a stage step outside** the site's existing content
     edge (`calc(<edge> - <stage-gap> / 2)`), so no word touches a line.
     Cell grids reach out to the rails and pad their contents back in by
     the same half step, so pictures in cells line up with the text above
     them. Do not move the content to fit the rails.
   - The line is the site's existing hairline token, at 1px, if it is
     opaque (`color-mix()` against the page colour is opaque; `rgba()` is
     not, so mix it) **and visible** (section 2). If the page's local
     hairline is fainter than that, use the site's own stronger default
     (often in the global tokens) for the grid. One line for the whole
     grid.
   - Section and cell spacing are `calc()`s of the site's own scale.
4. **Find the opening block** (a hero, or a name and bio intro) and leave
   it free of lines. The grid starts below it.
5. **Do not add chrome the site lacks.** No new nav bar, no new footer
   just to carry a line. If the page ends after its last section, close
   that section's last row with a rail-to-rail line and let the rails run
   on to the bottom of the page (step out of the page's bottom padding
   with a negative `bottom` on the rails). No full-width line at the very
   end: it would cut a small box into each gutter.
6. **Full-width lines without fighting the page's padding**: prefer the
   named-line section grid (section 1b) with the site's side margin as its
   gutter. Where the page wrapper owns the padding and cannot change, a
   section steps out with `margin-inline: calc(-1 * <edge>)` and pads back
   in with `padding-inline: <edge>`.
7. **Gapped card grids become cells**: `gap: 1px` over the line colour,
   each card on the page colour with the site's own inner padding. Keep
   the card's insides as they are (its image radius, its caption row).
8. **Fill the last row at every column count.** In a cell grid an empty
   slot shows the line colour as a solid block. Pad the row with empty
   cells, shown or hidden per breakpoint so each layout (4, 2, 1 columns)
   ends on a full row.
9. Run the check loop (section 7) with the selectors adapted to the site
   and `window.__auditType = false` set first (the audit's type rules are
   for new pages; the site's own type rules win),
   on the copy, at 1440 and 375, then report what changed and what the
   site's own rules made you do differently.

## 1. The structure

```
        page-pad          col (e.g. 1200px)           page-pad
 |  <------------>|<------------------------------>|<------------>  |
                  |                                |
   nav            |     (no lines in the hero)     |
   hero  .........|................................|.........      <- no rails here
 ─────────────────┼────────────────────────────────┼─────────────── <- section top: the ONLY kind of
                  |   heading and lead, inset by   |                   line that crosses the gutters
                  |   cell-pad from each rail      |
   (gutter: one   ├──────────┬──────────┬──────────┤                <- cells row top: rail to rail only
    tall empty    |  cell    |  cell    |  cell    |
    band)         |          |          |          |
 ─────────────────┼──────────┴──────────┴──────────┼─────────────── <- next section's top, which is
                  |                                |                   also the row's bottom edge
   footer: its top line, rails running on to the page's end
```

1. **Two rails only**, at `--rail: max(var(--page-pad), calc(50% - var(--col) / 2))`,
   drawn as `::before` / `::after` on one frame wrapper, 1px, `var(--border)`,
   `pointer-events: none`. **No vertical lines in the middle of the page.**
2. **The hero gets no lines across it, and the rails depend on its art.**
   - A hero with full-bleed art (a WebGL ribbon, a video, an image that runs
     to the window edge): no rails through it, no lines around it, no
     "lines outside the grid". The frame starts below the hero.
   - A text hero (a headline, a name and bio, a form): the rails may run
     through it from the top of the page, as on Cartesia, and nothing else
     does. The user asked for this on their own site. Ask when unsure.
   - **Never a line inside the hero.** A split hero (copy on one side, art
     on the other) is two plain columns, never a row of cells: a divider
     between the copy and the art is a vertical line in the middle of the
     hero, and the user rejected it.
3. **Each section starts on a full-width hairline** (`border-top: 1px solid
   var(--border)` across the window), so it meets both rails. A horizontal
   line that does not reach the rails is a bug ("the horizontal line that is
   not connected").
4. **Full-width lines are rare. The gutters stay calm.** Only a section's
   top line crosses the gutters. A section is whole: its heading, lead and
   cells live in **one** `<section>`. Never give a heading its own section
   and the cells under it another: that doubles the full-width lines and
   chops the strips outside the rails into a stack of small empty boxes
   ("the sides have too much boxes"). On OpenEvidence the full-width lines
   sit about 400 to 1300px apart, one per real section.
5. **Every line inside a section runs rail to rail only**: the rule under a
   heading, the top and bottom of a row of cells, group dividers. They never
   reach into the gutters. Give the row a `border-top` and a
   `margin-top: var(--shell-gap)` inside the section (`.ruled`).
6. **Cells share hairlines**: `display: grid; gap: 1px; background:
   var(--border)` with each child on `var(--bg)`. The outer edges are the
   rails themselves, so a cell's border sits **on** the rail, never 1px inside
   it ("the borders should be aligned with the grid line, not inside").
7. **One level of cells, never nested.** A cell never holds another grid
   of cells, and a row never gets its own `border-top` where it already
   sits on a gap line. Nesting doubles the line to 2px where two edges
   touch and leaves stray T shapes where an inner line stops at an outer
   edge. Need groups? Put them in one flat row and name each cell's group
   inside the cell, or give each group its own row, each a direct child of
   the section.
8. **A section that ends on a row of cells** has no bottom padding: the row's
   bottom edge is the next section's top line, so there is never an empty band
   between two lines (`.endsOnGrid`).
9. **No pluses or crosses** at intersections. They were tried and removed.
10. **Footer**: the rails run on through it to the very bottom of the
   page, so the frame never stops short. The footer gets its one top line
   and nothing else: no cells, no inner lines (a cell grid in the footer
   was built twice and removed both times). A page with no footer lets the
   rails run on to the page's end the same way.
11. **Nav**: one bottom line, sticky on a solid fill.

## 1b. How to build it (Cartesia's technique)

Measured on cartesia.ai, 2026-10-21. The cleanest way to get every rule
above, and the default for new pages and retrofits alike.

- **Every section is a three-column grid with named lines**, so nothing
  needs negative margins:
  ```css
  .cols {
    display: grid;
    grid-template-columns:
      [full-start] minmax(var(--gutter), 1fr)
      [content-start] minmax(0, var(--col)) [content-end]
      minmax(var(--gutter), 1fr) [full-end];
  }
  .cols > * { grid-column: content; }
  .cols > .bleed { grid-column: full; }
  ```
  Cartesia: gutter 80px on desktop, 16px on phones, content up to 1280px.
- **The rails are the content column's own side borders**
  (`border-inline: 1px solid var(--line)` on the `content` child of each
  section). Sections stack, so the rails run on unbroken from one to the
  next, through the footer, to the page's end.
- **Content sits a responsive step inside the rails**: Cartesia uses 16,
  32 and 48px (phone, tablet, wide). Map it to the site's scale.
- **A heading row** at the top of a section sits in its own band with a
  rail-to-rail line under it, then the cells.
- **Hierarchy by fill, not by weight.** To lead a group (a "Ranked #1"
  stat before a logo wall), give one cell a faint tint of the page colour
  and let it span rows. The lines stay identical.
- **Logo walls**: one logo per cell, centred, in one muted grey, cells of
  equal size.

### Optional: the seam

Cartesia does not divide sections with one line. Between two sections
runs a **seam**: a 16px band, window to window, made of a top line, a
bottom line, a faint centre line, and a ruler of 1px ticks every 8px at
30% opacity (`background-image: linear-gradient(to right, var(--line) 0
1px, transparent 1px); background-size: 8px 100%`). It is still the only
thing that crosses the gutters, so the gutters stay calm, but it reads as
a made thing rather than a hairline. Offer it as a choice ("plain line or
seam?"); use one style for every section boundary on a page, never both.

## 2. One line

Every line on the page is the same: **1px, solid, one opaque colour**.
Rails, section tops, cell edges, the nav line and the footer line all
match. Cartesia (measured: all 96 lines are `1px solid rgb(228, 227, 219)`),
Mintlify and Stripe work this way.

- **No second weight**, no "strong" border token, no bolder group dividers,
  no dashed lines. Hierarchy comes from space and placement, not from line
  weight.
- **Opaque, not transparent.** Mix the line colour onto the page colour
  once (about 9% of the text colour into the background) and write it as a
  solid hex. An `rgba()` line changes colour over art and gets darker where
  two lines cross.
- Light and dark each get their own solid line colour.
- **Visible, or it is not a grid.** About 9 to 12% of the text colour
  mixed into the page. Cartesia's line is about 11% on its paper. 5% on a
  white page cannot be seen ("I can't see lines on white background");
  check the line in a screenshot at 100%, not by its number.

## 3. Space

Use the project's spacing tokens, never raw px for page rhythm. Defaults the
user's projects share:

| Token | Desktop | Phone | Use |
|---|---|---|---|
| `--page-pad` | 32px | 16px | window edge to rail at narrow widths |
| `--cell-pad` | 28px | 16px | rail or hairline to content |
| `--section-pad` | 80px | 56px | top and bottom air inside a section |
| `--hairline-gap` | 10px | | a label and what it labels |
| `--row-gap` | 13px | | rows of text, buttons in a row |
| `--stage-gap` | 24px | | siblings inside a block |
| `--shell-gap` | 48px | | heading block to its content |
| `--col-text` | 760px | | headings and leads |
| `--col` | 1200px | | the rails |

- Text never touches a rail or a hairline: left-aligned text inside the rails
  keeps `--cell-pad` (`.inset`).
- **To make something narrower, change that thing's width, not the grid.**
  ("You changed the width of the grid, not the width of the chatbot.") The
  rails stay put; content gets a `max-width` inside them.
- Want it to feel fuller? Widen the column itself (the user preferred
  Stripe's wider frame over Grok's narrow one), but do it once, globally.

## 4. What may cross a rail

- Only full-bleed art marked `data-bleed`, and the section hairlines. Labels,
  legends and text inside bleed art still stay inside the rails.
- **Animations and canvases must not exceed the rails** unless marked bleed
  ("your router animation exceeded that"). Absolutely positioned visuals
  measure from the padding edge: pin with `right: 0` / `left: 0` of the inner
  box, not of the section.
- Hero art may run to the window edge, but never under the nav and never
  into the first section.

## 5. Filling the empty cells

Stripe, Mintlify, Human Delta and Modal make the frame feel alive with small
effects in empty spots (Mintlify's dots, a cursor-lit dot field). Use **one or
two** of these where a cell is genuinely empty and the section is relevant.
Putting hover effects everywhere made "the whole website look distorted".

- Logo walls (partners, investors, publishers) go into hairline cells as a
  sponsor list, not as bento cards. Group different kinds by giving each
  group its own side or its own row with a label, never by a heavier line
  and never by inventing new boxes. Groups of uneven size are fine; they do
  not have to be perfect squares.
- Cards in a row line up on shared baselines: price with price, button with
  button, using `subgrid` or fixed rows. Only the feature lists may run long.

## 6. Variant: the hidden grid

When the user wants no visible lines at all (the OpenRouter concept ended
here): one container (for example 1266px, content 16px inside), a 12 column
grid, **no rails, no marks, no section lines**. The columns only place
things; the nav keeps its bottom line. Keep invisible `.guides` markers at the
rail positions so the audit can still check that nothing crosses them.

Ask which one the page uses if it is not obvious: visible rails (Stripe,
Mintlify) or hidden grid.

## 7. Check loop (every layout change)

At 1440x900 and 375x812, the browser tab in front:

1. Run `reference/audit.js` in the page (adapt selectors: `.guides .frame` or
   the frame wrapper for rails, `.hero` for the hero). It must return `[]`:
   no horizontal overflow, nothing crossing a rail, hero art inside the hero,
   no full-width line inside a section, no two full-width lines closer than
   a quarter of the screen height, at most 240px ("gutter cut into boxes":
   merge the sections; a seam counts as one line), no clipped or
   overlapping labels.
2. By eye, on screenshots:
   - every horizontal line reaches both rails
   - the gutters hold a few tall empty bands, never a stack of small boxes
   - only section tops cross the gutters; every other line stops at the rails
   - no line runs through the hero
   - no vertical line between the rails except cell edges
   - no empty band between two hairlines
   - cell borders sit on the rails, not inside them
   - text is never closer than `--cell-pad` to a line
   - every line has the same weight and the same solid colour, and no line
     is ever doubled to 2px where two edges touch
   - the rails run through the footer to the page's end; the footer has
     only its top line inside them
   - the lines are visible in a 100% screenshot of a light page
3. Console clean. Fix and repeat, three rounds at most, then say what is
   still off.

## Rejected, do not repeat

- Vertical lines in the middle of the page.
- A heading in one section and its cells in the next: the gutters fill
  with boxes.
- Row, heading or group lines that run past the rails into the gutters.
- A grid, rails or framing lines in the hero.
- A vertical divider between the copy and the art in a split hero.
- Lines drawn "outside the grid" around the hero as a workaround.
- Floating horizontal lines that stop short of the rails.
- Plus marks or crosses at intersections.
- A full cell grid in the footer, or rails that stop above it.
- Lines too faint to see (5% ink on white).
- Hover effects on every cell.
- Widening the grid when only one element should change width.
- A heavier or "strong" line to set one group apart.
- A grid of cells nested inside a cell: doubled 2px lines and stray T
  shapes.
- A cell grid whose last row is short: the empty slot fills with the line
  colour.
- In a retrofit: moving the site's content to fit new rails, adding a nav
  or footer it never had, or overriding its spacing scale with this
  skill's defaults.
- Transparent `rgba()` line colours.
