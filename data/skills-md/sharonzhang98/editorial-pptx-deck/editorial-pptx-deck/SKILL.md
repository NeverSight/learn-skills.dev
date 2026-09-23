---
name: editorial-pptx-deck
description: >-
  Build editable business PPTX decks in an editorial minimalist style — white
  background, Georgia serif titles, a single red accent bar, and full-height
  photo section dividers. Exports a real editable .pptx (native text boxes) from
  HTML slides. Use when the user asks for a business report / pitch deck / PPT /
  PPTX in this clean editorial or "photo-divider" style, or references this skill.
---

# Editorial PPTX Deck

Produce a polished, editorial-minimalist slide deck and export it to an **editable PPTX**. The final deliverable is the **`.pptx` only** — HTML slides are just the build source, and PDF/HTML viewers are not produced.

## How it works

Slides are authored as constrained HTML (one file per slide), then `scripts/html2pptx.js` translates each DOM element into a native PowerPoint object (real, double-click-editable text boxes). Body is fixed at **1280px × 720px = 960pt × 540pt** (`LAYOUT_WIDE`).

## Build workflow

Copy this checklist and track progress:

```
- [ ] 1. Scaffold project (shared/ assets/ slides/ output/)
- [ ] 2. Plan narrative → map each slide to a template type
- [ ] 3. Write slides/NN-name.html from templates (edit text only)
- [ ] 4. check_overflow → fix any slide that isn't exactly 1280x720
- [ ] 5. Export PPTX (only)
- [ ] 6. Clean up build source (keep only the .pptx)
```

**1. Scaffold.** In the working project create `shared/`, `assets/`, `slides/`, `output/`. Copy `shared/tokens.css` from this skill into the project's `shared/`. Copy only the photos you'll use from this skill's `assets/` into the project's `assets/`. Ensure deps once:

```bash
npm i pptxgenjs playwright sharp && npx playwright install chromium
```

**2. Plan.** Turn the source content into a slide list. Every slide is one of the [template types](#template-catalog). A typical deck = cover → (divider → 1–3 content slides) × sections → closing. Keep text concise; this style is airy.

**3. Write slides.** Copy the closest template from `templates/` into `slides/NN-name.html` and replace the text. Rules:
- Keep `<link rel="stylesheet" href="../shared/tokens.css">`.
- Titles use the serif; everything else is sans (already wired in tokens).
- One red accent only. Use the dark panel (`--ink-panel`) sparingly for contrast, with the gold `#C9A24B` as its only accent.
- Photos go in via `<img>` (never CSS `background-image`). See [photo library](#photo-library).

**4. Verify fit.** Slides that overflow get clipped in PPTX:

```bash
node scripts/check_overflow.mjs --slides slides
```

Fix anything flagged `OVERFLOW` (shorten text or nudge positions) until all report `1280x720`.

**5. Export PPTX only.**

```bash
node scripts/export_deck_pptx.mjs --slides slides --out output/DeckName.pptx
```

Slides are ordered by filename (`01-…`, `02-…`). Do **not** run any PDF/HTML export — PPTX is the sole deliverable.

**6. Clean up.** Delete the `slides/` HTML and any temp files so only `output/DeckName.pptx` remains (plus reusable `shared/` + `assets/` if the user wants to iterate).

## Design system

Defined in `shared/tokens.css`. Do not invent new colors.

| Token | HEX | Use |
|---|---|---|
| `--ink` | `#1A1A1A` | Titles & primary body |
| `--soft` | `#555555` | Secondary body |
| `--muted` | `#8C8C8C` | Labels, notes, page numbers |
| `--red` | `#C8102E` | The one accent: bar, kicker, key words, underlines |
| `--red-deep` | `#A00C24` | Negative emphasis in tables |
| `--red-pale` | `#FBE9EC` | Connector chips (e.g. "→" circles) |
| `--box` | `#F4F3F1` | Light cards / zebra rows |
| `--line` | `#E4E2DE` | Hairline separators |
| `--ink-panel` | `#1C1C1C` | Dark contrast panels |
| gold | `#C9A24B` | Accent **only** on dark panels |
| background | `#FFFFFF` | Page |

- **Type:** Georgia serif for `h*`/titles; Arial/Helvetica sans for all else.
- **Signature:** thin red vertical bar left of the title + small letter-spaced red kicker above it; tiny centered page number at bottom.
- **Brand swap:** to match another company, change `--red` (and optionally `--ink-panel`/gold) in `tokens.css` — nothing else.

## Photo library

Photos live in this skill's `assets/`. Portrait images fill the right ~40% divider/cover panel (`object-fit:cover`); landscape images suit full-bleed covers.

| File | Orientation | Best for |
|---|---|---|
| `sail.png` | portrait 589×1024 | divider / cover right panel (default) |
| `lighthouse-cliff.png` | portrait 627×1024 | divider / cover right panel |
| `staircase.png` | tall 312×1024 | calm/abstract divider strip |
| `mast.png` | narrow 208×1024 | narrow divider strip |
| `hiker-clouds.png` | narrow 225×1024 | narrow divider strip |
| `lighthouse-sunset.png` | landscape 1024×721 | full-bleed cover / top band |
| `sailboat-deck.png` | landscape 1024×721 | full-bleed cover / top band |

Swap a photo by changing the `<img src="../assets/….png">`. Keep one consistent photo (or one motif) across all dividers for cohesion. Users may also drop their own images into `assets/`.

## Template catalog

In `templates/` (each is a complete, overflow-safe 1280×720 slide):

| File | Type |
|---|---|
| `01-cover.html` | Split cover: serif title left, portrait photo right |
| `02-divider.html` | Section divider: kicker + serif title + red bar, portrait photo right |
| `03-three-column.html` | Kicker/title + core line + 3 columns + result strip |
| `04-mapping.html` | Two-column "what they want → what we do" with connector chips |
| `05-compare-table.html` | 3-column comparison table, zebra rows |
| `06-dark-contrast.html` | Two panels (light vs dark) + serif footer line |
| `07-pipeline.html` | Numbered horizontal step pipeline + dark output bar |
| `08-closing.html` | Closing pitch: numbered serif lines + portrait photo right |

## Hard constraints

The HTML→PPTX conversion fails or misrenders if these are broken. Full details + fixes in [reference.md](reference.md):

1. Text only inside `<p>`/`<h1>`–`<h6>` (never loose text in a `<div>`).
2. No CSS gradients.
3. `background`/`border`/`box-shadow` only on `<div>`, never on text tags.
4. No `background-image`; use `<img>`.
5. Inline tags (`span`/`em`/`strong`) can't have margins.
6. Body stays 1280×720; nothing may overflow.
