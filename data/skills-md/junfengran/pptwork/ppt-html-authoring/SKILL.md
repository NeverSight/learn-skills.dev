---
name: ppt-html-authoring
description: Author a single PPT slide as a self-contained slide.html + design.md, given one outline entry. Use when the user asks to design, draft, or rewrite an individual slide page (KPI page, agenda, cover, two-column comparison, chart slide, etc.). Single-page only; does not plan across pages, does not screenshot, does not export. Works alongside the `ppt` skill or standalone.
---

# Single-page PPT authoring

Given:

- A target slide directory (typically `.pptwork/<deck>/<slide-name>/`)
- One outline entry (`pageType`, `assetId`, key content, source, transition)
- The deck `exportMode` (`raster` or `editable`)

Produce:

- `design.md` — frontmatter `title` + `layout`, then `## Content` / `## Note`
  / `## Design` (all three sections must be non-empty)
- `slide.html` — single-file self-contained, with the `## Note` text mirrored
  into a `<script type="application/json" id="ppt-speaker-notes-json">` island

**Out of scope:** cross-page planning (use the `ppt` skill's story-planning
phase), screenshots and visual QC (use the `ppt` skill's `screenshot.mjs` +
visual-qc reference), exporting (use `export.mjs`), web search (use the host
app's webfetch / websearch).

## File contract

### `design.md`

- frontmatter:
  - `title` (required)
  - `layout` (required, short English identifier matching the layout you used)
- body, three sections, all non-empty:
  - `## Content` — page copy in human language: a **conclusion-form
    complete-sentence title** plus supporting bullets / short paragraphs.
  - `## Note` — speaker notes in natural prose (not bullets).
  - `## Design` — visual / engineering notes: layout choice rationale,
    transition from previous page, data source, `TBD` markers.
- No empty placeholders. "This is an introduction page" is not acceptable.
- Detailed schema → [`references/design-md-spec.md`](references/design-md-spec.md)

### `slide.html`

- **Must be single-file self-contained**: CSS in `<style>`, JS in `<script>`.
- Images: **inline base64** or **https CDN**. Local relative paths
  (`<img src="assets/...">`, `<link href="...">`) are forbidden — they break
  in `<iframe srcdoc>` previews and in the static-server-based renderer
  unless the sidecar files happen to land next to the HTML.
- Fonts, chart.js, d3 etc.: load from https CDN.
- Mirror `## Note` content into a
  `<script type="application/json" id="ppt-speaker-notes-json">…</script>`
  node. This is the only way speaker notes land in the exported PPTX.
- For the slide to render at the correct PowerPoint canvas size, set
  `html, body { width: 1280px; height: 720px; overflow: hidden; }`.
- Hard rules and common pitfalls →
  [`references/slide-html-rules.md`](references/slide-html-rules.md)
  (**must read**).
- If `exportMode=editable`, also follow
  [`references/editable-html-rules.md`](references/editable-html-rules.md).

## Workflow

### 1. Read context

Outline entry (`pageType` / `assetId` / key content / source / transition) +
the existing slide skeleton (`design.md` is an empty template, `slide.html`
may only have `<html>` head/tail) + `exportMode`.

### 2. Look up the layout (assets contract)

If the outline names an `assetId`, look it up under the sister `ppt`
skill's `../ppt/assets/<bucket>/index.json` and read the matching
descriptor:

| Read | For |
|---|---|
| `index.json` entry's `htmlPath` | Find the HTML reference path |
| `index.json` entry's `materialDir` / `zones` / `authoringHints` | Understand the layout's slot composition |
| Resolved `html/<id>.html` | Borrow composition (version safe area, columns, hierarchy) |
| `specs/<id>.json` `zones` | Get structured per-slot descriptions (optional) |

Default buckets live in the sister `ppt` skill at
`../ppt/assets/corporate-light/` and `../ppt/assets/claude-warm/` (5 layouts
each). Read `index.json` + the matching `html/<id>.html` when the outline
names an `assetId`. If no bucket is configured, skip this step and write
`slide.html` from scratch using `references/slide-html-rules.md` and
`references/ppt-best-practices.md` as your composition guide.

**Do not** pick the `assetId` yourself — that's a story-planning decision,
the outline already names it (or explicitly says "no preset, design from
scratch").

### 3. Don't copy the template HTML wholesale

Borrow only the composition (version safe area, columns, hierarchy, slot
positions). Replace **all** placeholder copy ("Acme Corp", "2024 Q3 revenue",
"scene illustration", etc.) with the page's real content. Placeholder bleed
into a finished deck is one of the most common authoring failures.

### 4. Write `design.md` first

In the order Content → Note → Design:

- `## Content`: **conclusion-form complete-sentence title** (not a noun
  phrase) + supporting bullets / short paragraphs.
- `## Note`: speaker notes, natural prose, not bullets.
- `## Design`: layout choice rationale, transition cue, data source, `TBD`
  markers.

### 5. Then write `slide.html`

Drive the HTML from the Content section. Whenever the data fits, **prefer
visuals over plain text**:

- Trends / proportions / comparisons → **Chart.js** (see
  [`references/diagram-and-chart.md`](references/diagram-and-chart.md)).
- Flow / architecture / system boundary → **inline SVG**.
- Decorative imagery → **base64 inline**; for large images (>2MB) compress
  or use a remote CDN.
- Icons → use a remote https SVG icon library (Heroicons, Lucide, Feather,
  Tabler, etc.) or paste a single inline SVG.

If `exportMode=editable`, write the HTML as PowerPoint-native objects:
real text nodes for important copy, simple solid-fill shapes for cards,
real tables, extractable Chart.js data, and separated background decoration.
Do not place important text inside SVG/canvas/images/pseudo-elements.

### 6. Sync `Note` into the HTML

Mirror the `## Note` text into the
`<script type="application/json" id="ppt-speaker-notes-json">…</script>`
island. This is the **only** path for speaker notes to land in the
exported PPTX.

### 7. Need an external fact?

If a single page is missing one number / fact / citation / competitor data
point:

- Use the host app's built-in webfetch / websearch tool. This skill ships
  no web tool of its own.
- Append findings to `.pptwork/<deck>/materials/research.md` (so they
  don't pollute the main context across slides).
- Cite the fact in `## Design` as `source: research.md §<timestamp>`.
- Do not fabricate numbers.

### 8. Self-check

- Any `<img src="assets/...">` / `<link href="...">` relative paths? Convert
  to base64 or remote https.
- Note section synced into the HTML?
- `data-id` / `data-role` attributes stable enough to support later
  `edit` / `patch` style touch-ups?

## References (read on demand)

| Doing | Read |
|---|---|
| Writing design.md | [`references/design-md-spec.md`](references/design-md-spec.md) |
| Writing / editing slide.html | [`references/slide-html-rules.md`](references/slide-html-rules.md) (**required**) |
| Writing / rewriting editable deck HTML | [`references/editable-html-rules.md`](references/editable-html-rules.md) |
| Adding charts, inline SVG, diagrams | [`references/diagram-and-chart.md`](references/diagram-and-chart.md) |
| Typography, font sizes, alignment, visual focus | [`references/ppt-best-practices.md`](references/ppt-best-practices.md) |

## Decision rules

- User says "tweak a sentence" → use `edit` / `patch` to mutate the
  matching `data-id` node, keep the outer structure intact.
- User says "rework the layout" → rewrite the whole `slide.html`, but
  keep `design.md`'s narrative intact.
- Existing raster / complex HTML deck now needs editable output → rewrite
  each page with a language model according to `editable-html-rules.md`;
  do not rely on a pure rule-based converter.
- Content is fundamentally about ratio / trend / comparison → **lead with
  a chart**, don't list raw numbers.
- Content is fundamentally about flow / architecture / boundary → **lead
  with inline SVG**, don't pile up paragraphs.
- A background / brand image is required → base64 inline; for large
  images (>2MB) compress first or use a remote CDN.
- Data is missing → use the host's webfetch/websearch, do not invent
  numbers.

## Common pitfalls

- Leaving template placeholder copy in the finished page ("Acme Corp Case"
  in an unrelated deck).
- Data page that's just "numbers + a paragraph" with no chart.
- `image-slot` left with a "scene illustration" placeholder — the
  thumbnail will look empty.
- `<img src="assets/diagram.png">` relative path — the iframe preview
  breaks.
- Forgot to mirror Note into `#ppt-speaker-notes-json` — exported PPTX has
  empty speaker notes.
- Title written as a noun phrase ("AI Agent market") instead of a
  conclusion sentence.
- Faked a number instead of running a quick fetch / asking the user.
