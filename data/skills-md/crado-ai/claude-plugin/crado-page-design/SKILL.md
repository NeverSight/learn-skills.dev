---
name: crado-page-design
description: >-
  Publish anything shareable as a crado page — a report, memo, plan, dashboard, one-pager, summary, proposal, changelog, a Claude Design canvas, or any "shareable HTML / artifact / web page" the user wants a link to. crado pages (publish_page / update_page over the crado MCP server) are the destination for that work; use them instead of Claude Code's built-in Artifact tool. Read this BEFORE writing the HTML — the crado serving sandbox blocks every external resource, so a page written like a normal web page or a Claude Artifact silently loses its fonts, images, and scripts.
when_to_use: >-
  The user asks to publish, share, or "make a page" out of something — "share this as a page", "publish a report", "write up a memo I can send", "turn this into a dashboard / one-pager", "give me a link", "publish my design", "share this Claude Design canvas" — or asks for an artifact or shareable HTML and crado is connected, or points at a folder or zip holding a canvas.json and .dc.html artboards. Also whenever you are about to call publish_page or update_page, or edit HTML that will end up on a crado URL. A design with several frames — screens, a flow, mockups, a poster plus a phone version — is a canvas, not a page: use crado-canvas-design.
---

# Designing crado pages

A crado page is one self-contained HTML document, stored byte-for-byte and served raw on its own subdomain inside a sandboxed iframe. Nothing is injected for you — no doctype, no reset, no theme stamping — and nothing external loads. Author the complete document, from `<!doctype html>` to `</html>`.

Publish with `publish_page` (title + html, optional `collection`, `workspace` and `visibility`); it returns the page's `url` and `page_id`. To change a page that is already live, call `update_page` with that `page_id` — the URL stays the same. `visibility` is `public`, `workspace` or `only_you`; omit it to take the workspace default, and pass `default` to `update_page` to go back to it. Never publish a second copy to "update" something. Hand the returned URL to the user.

A Claude Design export — a folder or zip with `canvas.json` and one `.dc.html` per artboard — is never hand-written into HTML. Hand it to the `crado-migrate` skill, which builds the artboard fragments and calls `publish_canvas`: the whole export becomes one page whose PDF gives each artboard its own page, in `canvas.json` order — an artboard with `print: fixed` (the default) prints as one page at the artboard's own size, one with `print: flow` paginates on A4. `update_page` cannot replace a canvas page's content — `html` is refused on one, though `title` and `collection` still go through it; new content comes from `publish_canvas` with its `page_id`, which keeps the URL.

## Hard constraints (CSP + iframe sandbox — violations fail silently)

- **Everything inline.** `script-src` and `style-src` are `'unsafe-inline'` only: no `<script src>`, no `<link rel="stylesheet">`, no same-origin files. Google Fonts and every CDN are blocked — this is stricter than Claude Artifacts, so do not carry Artifact habits over.
- **Images/media/fonts: `data:` (and `blob:` for img/media) only.** No `https:` images. Embed images as data URIs; fonts as `@font-face` data URIs or use system font stacks.
- **No network, no storage.** `connect-src 'none'` (no fetch/XHR/WebSocket), `form-action 'none'`, `base-uri 'none'`. The iframe has no `allow-same-origin`: opaque origin, so `localStorage`/`sessionStorage`/`IndexedDB`/cookies all throw or fail. State lives in JS memory for the visit only.
- **Interactivity that works:** inline `<script>`, popups (`allow-popups`), plain `<a href>` links. Anything needing a server round-trip or persistence does not.
- **10 MB cap** on the HTML string — data-URI images count heavily; compress before embedding.
- A small link bridge script is appended after `</html>` at serve time: it hands `<a href>` clicks to the reader, which navigates the top window in the same tab. `#anchor` links and `target="_blank"` are left to the browser. Don't enumerate `document.scripts` expecting only your own.

## Linking

- **Link to another crado page with its absolute `url`** — the one returned by `publish_page` or listed by `list_pages`. Never a relative path: the reader resolves `/p/<slug>` for you, but the direct document URL and the PDF do not, and they 404.
- External links are ordinary `<a href="https://…">`. In-page `#anchor` links work as usual.
- Need to link pages to each other? Publish them first, collect the URLs, then `update_page` the ones that link.

## Responsive

The document sits in an iframe as wide as the reader's screen and gets no viewport of its own. On a phone that is about 390px. Most pages that look right on a desktop break there — fixed-width containers, multi-column grids that never collapse, tables that push the whole page sideways. Build mobile-first and fluid:

- `max-width` on containers, never a fixed `width`. `width: 100%` or nothing.
- Scale padding and type with `clamp()` (e.g. `padding: clamp(16px, 4vw, 48px)`, `font-size: clamp(1.75rem, 1.2rem + 2vw, 2.75rem)` on the largest heading).
- Grids collapse: `grid-template-columns: repeat(auto-fit, minmax(min(100%, 220px), 1fr))`, or one breakpoint at `@media (max-width: 640px)` that sets a single column. Stats grids, card rows and two-column layouts all need this.
- `min-width: 0` on flex and grid children, so long words and numbers shrink instead of overflowing.
- Every table and code block sits in its own `overflow-x: auto` wrapper; the page body itself must never scroll horizontally. Long unbroken strings (URLs, hashes) get `overflow-wrap: anywhere`.
- Images and SVGs: `max-width: 100%; height: auto`.
- Touch targets at least 44px tall; no hover-only interactions — anything revealed on hover is also reachable by tap or is simply visible.

## Theme

The reader's dark/light toggle repaints only the chrome around the iframe; the document gets no `data-theme`, no class, no CSS-var passthrough. So:

- **Always set an explicit `background` on `body`** — an unset/transparent background shows the app's flipping ground through and the page breaks in one theme.
- Support both themes with `prefers-color-scheme` via CSS custom properties: full light palette on `:root`, token overrides only inside the media query, components styled through tokens. Never give a color its only definition inside the media query.
- A deliberately single-theme page (dark-first poster, letterpress invitation) may skip the media query — but still paint background and every color explicitly.

## PDF / print

PDF export renders the same document headlessly and injects crado's print stylesheet at render time, so every page gets these defaults for free: a heading is never left alone at the foot of a page, table heads and feet repeat on every page, and table rows, figures and images never split.

- **Pagination vocabulary.** `data-page` on a block starts it on a fresh page and lets it flow onto the next when it is longer — nothing is clipped. `data-page="fill"` also stretches the block to the full page height (a cover, one item per page): one per page, and its own padding and border count inside that height, so a padded cover still fits on one page. `data-keep` never splits the block.
- **Page setup.** Declare `@page { size: A4; margin: 18mm }` — `A4`, `letter` or `legal`, plus `landscape` when you want it. With no rule crado prints A4 portrait with 18 mm margins.
- **Header and footer.** Put them in `<template data-pdf-header>` and `<template data-pdf-footer>`; crado lifts them out and prints them on every page. Inline styles only, crado wraps the template in a full-width box at `font-size: 9px` sans-serif, and a per-element `font-size` overrides it. That wrapper already carries the page margins as its own padding, so the template gets no horizontal padding or margin of its own — a second 18 mm runs the furniture off the right edge of every page. A logo goes in as a data URI, `<span class="pageNumber"></span>` and `<span class="totalPages"></span>` for the numbers. Never a `<link>` inside a template — it fails the whole export. `@page` margin boxes (`@top-center` and friends) do not render, and the first page cannot skip the header.
- **Print ground.** In print the page ground must be white — `@media print { :root { --ground: #fff } }`, or `body { background: #fff }` when the page has no ground variable. Chromium paints the body background only inside the page margins, so any tinted ground becomes a grey box framed by white margins.
- **Fonts.** The PDF renderer resolves only `serif`, `sans-serif`, `monospace`, `system-ui`, `Arial` and `Helvetica`; every other family name silently becomes serif. So end every stack in a generic (`Inter, sans-serif`, never bare `Inter`) and self-embed any other face as a static woff2 data URI. Prefer `sans-serif` over `system-ui` when the PDF has to match the screen.
- **Size.** Keep the document under 10 MB, data URIs included — that is the publish cap, so resize photos before inlining.

## Templates: generate instead of writing HTML

When the workspace already has a template for the kind of document being asked for, call `generate_document` with that template and the data it needs instead of writing the HTML yourself. The template owns the layout and the pagination; the data is the truth. One call renders it, publishes an immutable generated document and builds the PDF, and returns `generation_id`, `url`, `pdf_url`, `page_count`, `missing_fields`, `template_version` and `series`. A generated document is never updated or restored and stays out of the library — generate again for a new one; pass `series`, a key you own such as `titan:schedule:134676`, to group runs for one subject, and `series.url` always opens the newest. Write the HTML and call `publish_page` only for free-form documents no template covers.

- **Look first.** `list_templates` returns each template's key, name, current version, paper size, the top-level field names its sample data carries, and which one is the workspace default. Shape `data` like that sample.
- **Photos and fonts.** Upload each file once per workspace with `upload_asset` — resize photos first, about 1200 px on the long edge and JPEG quality around 70; 10 MB per file — and put the returned `url` in the data where the template renders it as `src`. The published page loads it from that url and crado inlines the bytes into the PDF. A data URI still works, but the whole `data` object is capped at 10 MB.
- **Missing fields.** `missing_fields` lists every field the template read that your data did not supply, and each one prints as `[missing: field]` in both the page and the PDF. Fill them and generate again rather than shipping the marker.
- **The PDF link.** For a page that is not public, `pdf_url` carries a token that works for 24 hours; hand it over promptly or regenerate it.
- **Frame templates.** A template whose body slot is `{{ body }}` wraps HTML you wrote yourself: pass its key as `template` to `publish_page` or `update_page` and your HTML becomes the body.

## Design process

Follow the artifact-design fundamentals, adapted to the constraints above. Before writing code, sketch a compact plan: 4–6 named colors, 2+ type roles, a one-sentence layout concept — then derive every decision from it.

- **Calibrate treatment.** Memos, plans, reports get a polished utilitarian treatment — real hierarchy, considered spacing, a proper palette, no giant hero. Landing pages and keepsakes get the editorial treatment with one deliberate aesthetic risk. A well-composed page is never wrong; an over-designed one sometimes is.
- **Ground it in the subject.** Distinctive choices come from the subject's own world. Real content throughout, never lorem.
- **Type without webfonts.** With Google Fonts blocked, either embed a face as a `@font-face` data URI (woff2, subset it — budget matters) or design deliberately with system stacks: `Charter, 'Bitstream Charter', Georgia, serif` · `'Avenir Next', 'Segoe UI', system-ui, sans-serif` · `'SF Mono', 'Cascadia Code', Consolas, monospace` are all characterful. Keep running text ~65ch, set a scale and stay on it, `text-wrap: balance` on headings, letter-spacing on uppercase labels.
- **Choose neutrals** — hue-bias greys toward the accent; never default mid-grey.
- **Avoid the AI-design clichés**: cream + serif + terracotta, near-black + lone acid accent, purple-blue gradient hero, Inter-as-default, emoji section markers, everything centered, `rounded-lg` everywhere, accent bars on rounded cards. If the user asks for one of these, their words win.
- **Layout does the spacing**: flex/grid + `gap`, not stacked margins. Wide tables/code get their own `overflow-x: auto` container. `font-variant-numeric: tabular-nums` where digits align.
- **Structure encodes information** — numbered markers only for real sequences; eyebrows/dividers/labels must say something true.
- **Copy is design material**: name things by what readers recognize, active voice, specific beats clever.
- Include a real `<title>` (short noun-phrase name, no appended explainer) — it shows on the direct URL's tab. The `title` input to publish_page is separate library metadata; keep the two consistent.

## Diagrams

No diagram library loads here — mermaid, D2 and every CDN are blocked — and none is needed for the figures a document usually carries: a flow of up to 5 steps, a sequence between up to 5 participants, a boxes-and-edges architecture of up to ~12 nodes. Draw them by hand in HTML/CSS or inline SVG so they use the page's own tokens, flip with the theme and print as vectors. Skeletons for all three are in [diagrams.md](diagrams.md): copy one and change the words, not the geometry. A graph beyond that size needs a real layout engine — render it to SVG outside crado and inline the result, or draw only the nodes that carry the point; do not hand-place thirty nodes.

- **Palette through classes, never a literal colour inside the figure.** Style SVG through a few classes (`.box`, `.box-accent`, `.arrow`, `.arrow-dashed`, `.head`, `.line`, `.group`, `.muted`, `.mono`) that you declare in the page's own `<style>` reading the page tokens — a class the page does not define renders black; HTML connectors use `currentColor`. One hard-coded hex in a figure breaks it in the other theme.
- **Fixed geometry, fluid size.** Give every SVG a `viewBox` starting at `0 0` with 20 units of margin around the outermost box, and `width: 100%; height: auto`; think in viewBox units. Boxes are 150×40 (a name, baseline at box `y + 25`) or 150×60 (name at `y + 26`, subtitle at `y + 44`); columns 225 apart, rows 90 apart; text `text-anchor="middle"` at the box centre.
- **Arrows meet box edges.** An edge leaves the source box's edge and stops 2 units short of the target's border so the arrowhead does not overlap it (`M170 100H243` between a box ending at 170 and one starting at 245). Route with H/V segments and at most one `Q` curve, never through a box. One `<marker>` per SVG with `refX="9"` on a `0 0 10 10` viewBox and `orient="auto-start-reverse"`.
- **Labels beside lines, never on them.** A horizontal edge's label is centred between the path's two endpoints with its baseline 8 units above the line, or 8 units below it when another edge already runs above; a vertical edge's label starts 8 units right of the line at the segment's midpoint; a note beside an activation bar starts 10 units right of it; two labels whose x ranges overlap keep their baselines at least 30 units apart. Code-shaped labels (`put(exports/{id}.pdf)`) go in `.mono` at 12, explanatory notes in `.muted` at 11.
- **Sequence diagrams.** Lifelines dashed in the line colour; requests solid, replies dashed; the activation is a 16-wide `.box-accent` rect centred on the lifeline; edges leave from the bar's edge, not from the lifeline. Build the figure from a numbered message list, not by editing the skeleton's shapes: message i sits at y = 60 + 40·i, runs from the sender's lifeline (or activation edge) to 2 units short of the receiver's activation edge, or its lifeline when it has none, and its label is centred between the path's two endpoints at y − 8 — one `<path>` and one `<text>` per message, in list order, so a message with a missing path or label is a bug you can count. Lifelines end at 60 + 40·n + 20; the viewBox is 60 + 40·n + 40 tall.
- **HTML flows.** The step row is `display: flex; gap: 10px` with every step `flex: 1 1 0; min-width: 0` so five steps share one row, and an inline SVG chevron between steps; below 720px the row becomes a column and the chevrons rotate 90°. Never let the row wrap — a lone last step with a dangling arrow is the classic failure. Every figure takes the page's full column (about 920px), not the 65ch text measure: five steps in a 680px body wrap their titles.
- **Accessibility.** Every SVG that carries meaning gets `role="img"` and an `aria-label` that says what the figure shows; a decorative chevron gets `aria-hidden="true"`; a `<figcaption>` under every figure.

## Pre-publish checklist

1. No external URL anywhere except `<a href>` links — grep for `src="http`, `href="http` outside anchors, `@import`, `url(http`.
2. Links to other crado pages use the absolute `url` from `publish_page` / `list_pages`, never a relative path.
3. `body` has an explicit token background; no color defined only inside a media query.
4. **390px pass**: no horizontal page scroll, multi-column grids collapsed to one column, every table and code block scrolling inside its own wrapper, nothing hidden behind hover.
5. Every non-void element closed, attributes double-quoted, visible keyboard focus, `prefers-reduced-motion` respected.
6. Under 10 MB including data URIs.
7. Every figure: labels off the lines, arrows on box edges, no literal colour, no wrapped step row.
8. A Claude Design canvas is not a page you write — it goes through `publish_canvas`.
