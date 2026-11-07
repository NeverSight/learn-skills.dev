---
name: stills
description: On-brand still images built as HTML and rendered in a real browser, such as ads and banners in several sizes, social images, carousels, and paged PDFs (one-pagers, booklets, static decks). Not for charts or diagrams (data-viz), thumbnails or motion.
---

# Stills

Every still is one HTML page; every element is a layer you can move, restyle or swap. Chrome renders
it, the brand pack styles it, and every size is its own layout rather than a scaled copy.

```bash
node /workspace/tools/html2png.mjs projects/<slug>/still/comp.html --out projects/<slug>/renders \
  --name launch --size 1200x627 --size 1080x1080 --size 1080x1350 \
  --require-font "<display family>" --require-font "<text family>" [--format png|jpeg|webp] [--quality 90] [--scale 2]
node /workspace/tools/html2pdf.mjs --html projects/<slug>/doc/doc.html --out projects/<slug>/renders/doc.pdf \
  --size 8.5x11in --brand-fonts
```

`html2png` writes `<out>/<name>-<W>x<H>.<ext>` per size and prints one JSON line. Each size is a fresh
load at that viewport, so media queries, `vw`/`vh` and container queries recompose the layout. A
required font that does not paint, a page error or a failed asset writes nothing and exits 1; fix the
page. `--brand-fonts` requires the lead face of each brand stack instead of naming families. Exit 2
is a tooling failure: report it. Paged PDFs always go through `html2pdf`, never a hand-rolled
`page.pdf()` (it rounds glyph advances and clumps tracked type).

## Process

A small edit to an existing still (a word, a weight, a colour, a size) is: change the page, lint,
re-render, look, deliver.

1. **Classify the job.** A supplied visual plus "restyle", "reskin", "clean up", "resize" or "make it
   on brand" is a transformation: inventory every string, number, mark and relationship in the source
   and keep them all unless the brief says otherwise. A new asset whose sibling already shipped
   inherits the sibling's layout, type and colour; say what you inherited. Charts and diagrams go to
   `data-viz` even when the output is a PNG.
2. **Find the one message and the concept.** An ad carries one idea: what someone can now do, the next
   step, and at most one grounded number. Name the visual idea in one sentence before writing HTML:
   the real product moment, a sharp typographic statement, or a concrete metaphor. Brand primitives
   are not a concept, and generic dot, node or network wallpaper is never one.
3. **Pick the sizes.** Use exactly the sizes asked for. A named channel with no size gets its primary
   size; "a few sizes" with no channel gets the brand pack's formats (`/workspace/brand/brand.toml`)
   or the sets in [references/sizes-and-sets.md](references/sizes-and-sets.md).
4. **Build one page per layout.** Link `/workspace/brand/tokens.css` and use its custom properties
   (`var(--brand-color-…)`, `var(--brand-font-display)`, `var(--brand-font-text)`); never type a hex or
   a family. Logos come from `/workspace/brand/logos/` as real SVG, inline or `<img>`, at or above the
   minimum width in `brand.toml`, with its clear space; never redraw, recolour or stretch one. Sizes
   that share a layout share one responsive page; a size that needs a different arrangement (a
   728×90 banner against a 1080×1350 portrait) gets its own page, recomposed, never scaled.
5. **Lint, render, look.** `node /workspace/tools/brand-lint.mjs <page.html>` (and `--copy` on the
   words) must exit 0. Render every size in one call, then look at the set on one sheet
   (`node /workspace/tools/review-thumb.mjs --sheet <renders>`) like a reviewer who might reject it:
   hierarchy, a clear focal point, even spacing, nothing clipped, cramped or orphaned, the set
   consistent. Fix what you would not ship.
6. **Deliver** every file you looked at with `upload_files`, with one short line naming the concept
   and the calls you made.

Work in `/workspace/projects/<slug>/`: pages beside the brief, renders in `renders/`.

## Composing on brand

- **Fewest words.** The headline, what the ask supplied (a date, a name, an offer) and the next step,
  each once. No sub-line, caption, URL, footer or eyebrow the ask did not supply.
- **One accent element per frame**, from the brand's own rules (`/workspace/brand/graphic-language.md`).
  Grounds, fields and type follow the brand pack, including its light or dark choice for the set.
- **Every element a layer.** Absolutely position the few elements that carry the composition with
  explicit geometry on the brand grid, so a note like "move the logo up" is one property, not a reflow.
- **Taller twins spend their height on content.** A 4:5 version of a square layout scales elements
  and gaps together (about 1.25×); if the width caps the type, put the extra height in one deliberate
  band of air and say the twin runs airier.
- **No decorative bullets** (`•`, empty dots, ticks or pseudo-element markers), no type effects, no
  justified text, radii no larger than the brand's maximum.
- **Code in an image** must be valid and current; take request shapes and model ids from the
  provider's documentation read this run, not from memory. A long line truncates with an ellipsis.
- **Real assets over imitations.** Use the product's real UI, the source's real images and the real
  logo. Pull a public image with `node /workspace/tools/fetch-asset.mjs <url> --out
  projects/<slug>/assets --kind image`; ask for anything unpublished.
- **When options help, render them** (two or three concepts, each finished) instead of describing
  directions.

Carousels, paged documents and decks: [references/sizes-and-sets.md](references/sizes-and-sets.md).
