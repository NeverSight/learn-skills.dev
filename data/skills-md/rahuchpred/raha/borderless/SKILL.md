---
name: borderless
description: >-
  Build or retrofit UI the borderless way (Luma, Gemini, Cursor, ChatGPT's
  composer, Mobbin, Linear) instead of the boxed look AI tools default to.
  Separation comes from surface steps, space and one solid primary, never a
  1px outline and a drop shadow on every box. Keeps a line only where it
  does a job (a focused or empty input, a secondary button beside a solid
  primary, a data table's row rule). Works two ways: building a new screen,
  or de-bordering an existing one in its own tokens (Next.js, plain CSS, CSS
  modules, Tailwind). Use whenever someone says borderless, "too many
  borders", "looks AI generated", "remove the outlines", "cards everywhere",
  "make it cleaner", "like Luma / Linear / Cursor", or asks for a card,
  dialog, form, settings page, dashboard, sidebar or composer that should
  not look generated. Ships an audit script that counts outlines, rings,
  glows and stacked shadows on a page.
---

# Borderless

The idea in one line: **a box earns a line only when the line tells you
what the thing is or what state it is in. If the line only says "this is
a box", it goes, and a surface step or space does its job instead.**

AI tools draw a white box on a white page, then need a 1px outline (often
a Tailwind `ring-1`) and a drop shadow to make the box visible at all.
Every card, row, chip and button gets the same treatment, so nothing leads
and the screen reads as generated. The borderless products do the
opposite. Read this whole file before writing CSS. Every rule below is a
correction someone had to make.

Reference files in `reference/`:
- `audit.js`: run it in the page (browser console or a browser tool). It
  returns every outline, ring, glow and stacked shadow, and the score you
  are aiming for. Run it before and after.
- `reel.css`: optional. The animated before and after (lines reeling in
  along their own edge, a red and green review pass), for demos and
  posts only. Never put it in product UI.

## 0. Two modes

**Building a new screen**: use the system in section 2 with the default
palette in section 3.

**Retrofitting an existing screen** ("de-border this", "make it
borderless"):
1. Read the project's own rules first: AGENTS.md, CLAUDE.md, the tokens
   file (`globals.css`, a Tailwind theme, a tokens JSON). Where the project
   and this skill disagree on a value (a grey, a radius, a gap, the brand
   accent), the project wins. This skill supplies the method, not the
   numbers. Section 4 is the exception: those effects go even when the
   project has them. A brand's own accent stays (purple included) but
   turns solid; what goes is its gradient and its glow. A violet that only
   appears as a framework default with no token behind it is not a brand:
   make the primary ink.
2. Run `reference/audit.js` on the page and keep the list. That is the
   before.
3. Sort every line on the list with the test in section 1. Write the
   verdict down per element (keep / surface / nothing) before editing.
4. Edit, then run the audit again. Report the before and after counts and
   name each line you kept and why.
5. Keep the scope. Fix lines, surfaces and shadows; do not redesign the
   layout. If the page was never responsive, say so in the report and
   leave it.

## 1. The test: which lines stay

Keep the line when it is one of these. Everything else goes.

| Keep | Why |
|---|---|
| A text input, textarea or select **at rest** on a surface of the same colour | Its edge says "type here". On a grey surface it may become a white fill instead (section 2). |
| A focused input | The focus ring is state. Use the product's ring, never a glow. |
| A secondary button beside a solid primary | The outline is what makes it secondary. |
| A data table's row rule, a list where rows are dense and scanned across | The rule guides the eye along the row. One hairline, between rows, never boxes around cells. |
| A divider between two regions of different jobs (a sidebar and a canvas) | One line, full height, where the product really has a seam. Not needed when one side already has its own surface step. |
| A rule above a total in a summary | Optional. Try weight and space first; one hairline if the total still floats. |
| An image whose edge would vanish into the page (a white screenshot on white) | A hairline or an inset ring of 6 to 8% black, never a card around it. |

Goes, every time:
- The outline on a card, panel, dialog or popover. It gets a surface step
  or a soft shadow instead.
- Outlines on list rows, menu items, chips that are not selected, icon
  buttons, tabs and segmented controls. They get nothing, or a fill when
  hovered or selected.
- A nested outline (a bordered row inside a bordered list inside a
  bordered card). Never more than one level of anything.
- A card wrapped around an image, with padding between the line and the
  picture. The image is its own edge.

## 2. The system

1. **Surface steps instead of lines.** Pick one of the two moves per
   region, never both:
   - **Grey container, white controls** (Luma, Gemini, Mobbin): the region
     gets a surface one step off the page (`#f4f4f5` on white) and the
     controls on it stay white. The colour step is the edge.
   - **White container, lifted** (dialogs, popovers, a floating composer):
     the container stays white and gets one soft shadow (`--lift`): a
     blurred hairline and one long faint fall, two layers, never a 0-blur
     ring. Its fields inside become light grey fills.
2. **Steps are small.** Cursor's dark surfaces step about 6 points of
   lightness at a time. On light themes: page `#fff`, surface `#f4f4f5`,
   raised fill inside a white card `#f4f4f5`, hover `#ececee`. If you can
   name the step from across the room it is too big.
3. **Rows, idle chips and icon buttons get nothing.** Space groups them.
   Hover and selected states get a fill, not a line.
4. **One solid primary per view.** The primary action goes solid (the
   accent, or ink). Secondary actions are outlined (that line stays) or
   plain text. Never a gradient button.
5. **Selected state is a solid step**, in surface and weight: a white
   segment on a grey track, an ink chip with white type. Never a
   translucent wash, never a ring around the selected thing. **It must
   read at a glance**: shrink the screenshot to a quarter and the
   selected item should still be obvious. A white step on `#f4f4f5`
   alone is too faint for anything bigger than a segment; add a second
   signal (below).
6. **Depth only where something floats.** A dialog, popover, menu or
   toast gets a shadow. Nothing that sits in the page flow does.
7. **Destructive actions stay quiet until confirmed**: red text on a
   plain or white button. The solid red belongs to the confirmation step,
   not the settings row.
8. **Switches, sliders and checkboxes** are fills, never outlines: the off
   track is `--fill`, the on track the accent, the knob or thumb white
   with the one small shadow it is allowed (it floats on its track).
9. **Choice cards** (delivery options, plans, radio cards) need two
   signals on the selected one, never just a surface step:
   - **An indicator**: every option shows a radio at the leading edge,
     the selected one filled (accent or ink, a white centre dot), the
     others an empty `--line-strong` circle with no outline (`--fill`
     vanishes on the grey track). Or a check in the
     accent at the trailing edge.
   - **A step**: the selected option is white with a 600 weight title on
     the grey track; the others stay on the track at 500.
   Never a ring around the selected card, never a tinted wash.
10. **An inline action beside a field** (Apply next to a promo code, Copy
   next to a link) is a text button, not a second outlined box.
11. **Lists of content** (messages, comments, a feed) get no rules and no
   boxes: space and the author line separate them. Code blocks are a
   `--surface` fill, the one place mono belongs. Unread counts are solid
   ink pills.
12. **A field on a grey surface** (a promo code in a summary panel, a
   search in a sidebar) is a white fill with no line. On a white page it
   keeps its line (section 1).
13. **A white field next to white buttons on the same grey surface reads
   as another button.** Keep the field's hairline in that case
   (`--line-strong`), or make the buttons plain text actions.
14. **No primary when nothing waits to be confirmed.** A settings page
   that saves on change has no solid button at all; the selected states
   carry the weight.
15. **Colour comes from content**, not chrome: avatars, real images, app
   icons in solid tiles, status pills that mean status. The chrome stays
   neutral with one accent.

## 3. Default palette (new screens only)

```css
--page: #fff;
--surface: #f4f4f5;      /* a container one step off the page */
--fill: #e9e9eb;         /* a small control inside a white card */
--hover: #ececee;
--ink: #0b0b0c;
--ink-2: #8e8e93;        /* secondary text */
--line: #e3e3e8;         /* the few lines you keep */
--line-strong: #d1d1d6;  /* a kept input or secondary button */
--accent: #0a84ff;       /* one accent, or use ink for the primary */
--lift:
  0 0 1px rgb(0 0 0 / 12%),      /* a blurred hairline, not a ring */
  0 18px 50px rgb(0 0 0 / 12%);  /* the one shadow, floating things only */
```

Dark themes: depth comes from a lighter surface, not a shadow. Page
`#0b0b0c`, surface `#161618`, fill `#1f1f22`, lines at 8 to 10% white.

## 4. Never (each was tried and rejected)

- **Glow.** No coloured `box-shadow` halos, no blurred accent rings, no
  glowing buttons. A focus ring is a crisp 2px ring in the accent at most.
- **Stacked heavy shadows** (`shadow-2xl` plus a ring plus an inner
  highlight). One soft shadow, on floating things only.
- **Bevels and inset wells**: `inset 0 1px 0 white` highlights, inset
  shadows on fields.
- **Gradient buttons and gradient text.** Solid colour.
- **Purple as "the AI colour"**, sparkles as decoration.
- **A coloured or gradient plate behind the UI** to make it pop. The page
  is the ground. (Exception: a marketing hero that is itself art.)
- **Fake art.** No CSS-gradient "paintings" or placeholder sunsets
  standing in for images. Use the project's real images, real app icons,
  avatars with initials, or icon tiles (a white glyph on a solid colour
  square). If there is no real content for a slot, drop the slot.
- **A card around an image** with padding between line and picture.
- **Monospace for labels or counters.** One family; mono only for code.
- **Copying a reference's layout.** Borrow the visual language (surface
  steps, one primary, colour in content), never the composition, the
  strings or the arrangement of the reference screen.

## 5. Details that give it away

- **A solid button's border is the fill colour or none.** A border the
  same colour as the fill still reads as an outline to tools and to the
  eye at the corners; set `border: 0`.
- **Pills drawn as SVG outlines need a real radius**: half the height
  (`16px` on a 32px pill). A huge radius like `999px` is clamped per axis
  by SVG and draws an oval. CSS `border-radius: 999px` is fine.
- **Fit the text before fixing the box**; sizes 13 to 15px for UI text,
  a title 17 to 22px, sentence case.
- **Padding inside a surface** is 12 to 22px; a row is 44 to 60px tall;
  controls are 32 to 50px tall. Equal inset all round.
- **Nested radii**: inner radius = outer radius minus the padding between
  them.
- **A grey surface on a warm page** looks dirty. Match the surface to the
  page's temperature: mix the page colour toward ink rather than using a
  cool grey on cream.

## 6. Check loop

1. Run `reference/audit.js`. Aim for: outlines only on the elements you
   kept in section 1 (mark each with `data-keep="reason"` so the report
   names it), zero glows, zero bevels, at most one shadow per floating
   element, no element with both a ring and a shadow. The audit reads
   pseudo-elements too, but not hover, focus or `:focus-within`: tab
   through the page once and look at each focus ring.
2. Screenshot at 1440 and 375. Look at it small: can you still tell what
   is clickable, what is selected, what is the primary? If not, a surface
   step is missing; add a fill, not a line.
3. Check both themes if the project has them.
4. Report: the before and after counts, each kept line with its reason
   from section 1, and anything the project's own rules made you do
   differently.

## 7. Optional: the animated before and after

For a demo or a post, `reference/reel.css` animates the change: each
outline is an SVG `rect` with `pathLength="1"`, dashed a hair over 1 on
and 1 off, so shifting `stroke-dashoffset` by a whole unit reels the line
in along its own edge. A review pass marks each line red ("1px") or green
("keep") first, the red ones reel in with their shadows in a cascade, the
surfaces fade up as each line finishes leaving, and the kept ones settle
to grey. A caption counts the outlines down to "N borders kept", in the
page's own type. The file's comments say how to wire it.
