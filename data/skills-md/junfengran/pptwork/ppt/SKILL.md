---
name: ppt
description: Build PPT / PowerPoint / 演示文稿 / slide decks end-to-end via a .pptwork/<deck>/ filesystem contract. Use when the user wants to plan, author, screenshot, or export a slide deck. Provides Node scripts for deck CRUD, headless screenshot, and editable PPTX export. Covers clarification, story planning, single-page authoring (via the ppt-html-authoring skill), visual QC, and export troubleshooting.
---

# PPT skill — deck-level orchestration

You build slide decks (PPT / PowerPoint / 演示文稿) by treating the filesystem
as the database: every deck is a folder under `.pptwork/<deck-name>/` with a
machine-readable `deck.json`, per-slide `design.md` + `slide.html`, and
optional outline / research notes.

This skill ships:

- **Methodology** for clarifying intent, planning the story arc, doing visual
  QC, and exporting (this file + `references/`).
- **Scripts** under `scripts/` for deck CRUD (`deck.mjs`), headless thumbnails
  (`screenshot.mjs`), and PPTX export (`export.mjs`, with both editable and
  raster modes).
- The companion **ppt-html-authoring** skill handles single-page authoring
  (read its SKILL.md when you actually write a slide.html).

This skill ships **two built-in starter buckets** under `assets/`:

- `assets/corporate-light/` — 5 layouts (cover, agenda, two-column + chart, KPI row, closing)
- `assets/claude-warm/` — 5 layouts (cover, section, timeline, quote, bento grid)

Each bucket has an `index.json` listing every layout's `id`, `pageType`,
`description`, `authoringHints`, and `htmlPath`. Story planning reads
`index.json` to pick layouts; authoring reads the matching HTML to borrow
composition. Add your own buckets alongside the starters, or skip buckets
entirely and compose from scratch.

## Setup (first time)

```bash
cd skills/ppt
npm install   # or `bun install`
```

The screenshot / export scripts launch a real headless browser. They look for
Chrome/Edge in this order: `PPT_BROWSER_EXECUTABLE` env var → playwright's
bundled chromium → system Chrome (channel) → system Edge. If none of those
work, run `npx playwright install chromium` once.

Export toolchain:

| Library | Role |
|---|---|
| **playwright-core** | Headless Chromium/Edge rendering of `slide.html`, screenshots |
| **html2pptx-pro** | Editable PPTX (HTML structure mapping) — default export engine |
| **dom-to-pptx** | DOM → slide elements — backup editable engine for diagnostics |
| **pptxgenjs** | PPTX file writing, raster export |

## Working directory

All scripts operate against `process.cwd()/.pptwork/`. Run them from the
user's project root.

## Disk layout

See [`references/disk-layout.md`](references/disk-layout.md) for the full
contract. The short version: `.pptwork/<deck>/deck.json` is the only source
of truth for slide order; per-slide folders hold `design.md`, `slide.html`,
`thumbnail.png`.

## End-to-end work flow

This is one operator (you) running through phases — there are no hidden
subagents. Read the matching `references/<phase>.md` when you enter a phase.

```
1. Clarify intent
2. (optional) Material digest        → references/material-digest.md
3. (optional) Research               → references/research.md
4. Story planning                    → references/story-planning.md
5. Initialize deck + first slides    → scripts/deck.mjs init / init-slide
6. Author each slide                 → ppt-html-authoring skill
7. Visual QC each slide              → references/visual-qc.md + scripts/screenshot.mjs
8. Export                            → scripts/export.mjs (+ references/export-troubleshooting.md)
```

### Step 1 — Clarify intent

Ask only for what's missing — don't make it up:

- Audience (internal report / customer pitch / public talk / training)
- Scenario & length (meeting length, target decision, offline reading?)
- Page count expectation (lower / upper bound)
- Style / brand (corporate template? specific reference PPTX? color palette?)
- Must-have sections (anything the user insists on)
- Output language
- Whether external facts need verification (numbers / news / market data)
- Export target: ask whether the user wants `raster` or `editable`
  - `raster` is recommended by default: pixel-faithful, not editable in PowerPoint
  - `editable` is only for in-PowerPoint editing and carries layout drift risk; authoring must follow `references/editable-html-rules.md`

### Step 2 — Material digest (when needed)

Trigger when **any** of:

- User dumped a long doc / multiple files / meeting minutes.
- An imported reference deck is large (many pages of HTML).

Skip when the user has only a one-line topic, or you already have a digest.

Method → [`references/material-digest.md`](references/material-digest.md).

### Step 3 — Research (when needed)

Trigger when:

- The topic involves time-sensitive data (market size, release cadence,
  policy).
- The user explicitly asked you to verify a number / fact.
- Competitor / industry benchmark info is missing.

This skill does **not** ship its own web fetch / search tool. Use the host
app's built-in webfetch / websearch (OpenCode `webfetch`/`websearch`,
Claude Code WebFetch/WebSearch, Cursor WebSearch/WebFetch, etc.). Archive
the structured findings into `.pptwork/<deck>/materials/research.md` so they
don't pollute the main context.

Method → [`references/research.md`](references/research.md).

### Step 4 — Story planning

Inputs: clarification + (optional) digest + (optional) research summary.
Output: `.pptwork/<deck>/outline.md` for decks ≥ 5 pages; structured
in-context summary for short decks. Do a light review for:
template diversity, source citations, must-have section coverage.

Do **not** write `slide.html` in this phase.

Method → [`references/story-planning.md`](references/story-planning.md).

### Step 5 — Initialize deck & slide skeletons

```bash
node skills/ppt/scripts/deck.mjs init <deck-name> --mode raster
node skills/ppt/scripts/deck.mjs init-slide <deck-name> <slide-name>
```

`<slide-name>` should be short and meaningful (`intro-dark`, `agenda-clean`,
`summary-bold`).

**Author 1~2 pages first and confirm with the user before scaling out.**
Structural mistakes cost more than time; a wrong story arc detected at
page 12 means redoing 10 pages.

### Step 6 — Author each slide

Hand single-page authoring off to the **ppt-html-authoring** skill. That
skill is a separate trigger point so a user who just wants "design me one
slide" doesn't need the whole deck pipeline. It produces:

- `design.md` (frontmatter `title` + `layout` + `## Content` / `## Note` /
  `## Design`)
- `slide.html` (single-file, self-contained; speaker notes mirrored into a
  `#ppt-speaker-notes-json` script island)

Pass the deck `exportMode` into authoring. If `exportMode=editable`, require
the authoring step to follow `references/editable-html-rules.md`.

For long decks, run authoring page-by-page; do not batch all pages into one
authoring call.

### Step 7 — Visual QC each slide

```bash
node skills/ppt/scripts/screenshot.mjs <deck> <slide>
```

Then read the produced `thumbnail.png` and walk the checklist in
[`references/visual-qc.md`](references/visual-qc.md). Micro-edit
`slide.html` until the checklist passes; cap at 3 iterations and surface
unresolved issues to the user.

### Step 8 — Export

```bash
# default: editable via html2pptx-pro — editable, but still verify output
node skills/ppt/scripts/export.mjs <deck-name>

# high-fidelity fallback: raster — pixel-faithful, text not editable
node skills/ppt/scripts/export.mjs <deck-name> --mode raster

# backup editable engine for one-slide diagnostics
node skills/ppt/scripts/export.mjs <deck-name> --editable-engine dom-to-pptx
```

Output defaults to `.pptwork/<deck-name>/<deck-name>.pptx`. Override with
`--output <path>`.

If the deck's `deck.json` has `exportMode`, omitted `--mode` follows that
preference. Decks without `exportMode` are treated as `editable`.

**Editable (default)** uses `html2pptx-pro` to convert slide HTML into
editable PowerPoint objects. This is now the main path, but it still needs
PowerPoint verification: fonts, complex CSS, and layout edge cases can drift.

The revision loop is:

```
edit slide.html  →  screenshot.mjs to verify  →  export.mjs to ship
```

This is the supported way to "edit a deck": change the HTML, re-export.
Don't try to edit the .pptx output and expect changes to round-trip.

**Raster** bakes each slide into a single full-page PNG and places it onto a
13.333×7.5 inch slide. Use it when the editable output drifts and visual
fidelity matters more than PowerPoint editability.

**dom-to-pptx** is a backup editable engine for diagnostics only. It has shown
layout drift on real decks and currently supports one-slide backup export.

If the export looks wrong, see
[`references/export-troubleshooting.md`](references/export-troubleshooting.md).

If the user first created a raster / complex-HTML deck and later asks for
an editable PPTX, do **not** just re-run `--mode editable`. First rewrite
each `slide.html` with a language model according to
`references/editable-html-rules.md`, then screenshot-QC and export editable.

## Template buckets

Built-in starters: `assets/corporate-light/` and `assets/claude-warm/`
(see repo `examples/` for decks that exercise both). Drop additional
buckets under `assets/<bucket-name>/` to extend the library.

A bucket is a directory with this shape:

```
assets/<bucket>/
├── index.json                     # array of template descriptors
├── html/<id>.html                 # one self-contained reference slide per id
├── specs/<id>.json                # optional structured zone description
└── materials/<id>/                # optional images/svgs the template uses
    └── manifest.json
```

Minimal `index.json` entry (everything not marked optional is required):

```json
{
  "id": "cover-hero",
  "pageType": "cover",
  "description": "Hero opener with full-bleed background and a single conclusion title.",
  "authoringHints": "Title goes in the centered `[data-role=hero-title]` slot. Background image at `[data-role=hero-bg]`.",
  "htmlPath": "html/cover-hero.html",
  "materialDir": "materials/cover-hero",
  "zones": [
    { "selector": "[data-role=hero-title]", "kind": "text" },
    { "selector": "[data-role=hero-bg]",    "kind": "image" }
  ]
}
```

**Story planning reads only `id` / `pageType` / `description` /
`authoringHints`** — not the raw HTML. The HTML body is for the authoring
phase to borrow composition (version safe area, columns, hierarchy, slot
positions). Don't copy the placeholder copy in the reference HTML
("Acme Corp", "2024 Q3 revenue", "scene illustration") into your real deck.

If you don't have a template bucket yet, the skill still works — story
planning can describe layouts in plain language and authoring can produce
slide.html from scratch. Buckets just speed both phases up by giving the
authoring step a known-good composition to riff on.

## Script reference

| Script | Purpose |
|---|---|
| `scripts/deck.mjs init <deck>` | Create `.pptwork/<deck>/deck.json` skeleton. |
| `scripts/deck.mjs init-slide <deck> <slide> [--at N]` | Create slide folder + empty `design.md`, register in `deck.json`. |
| `scripts/deck.mjs move <deck> <slide> <to-pos>` | Reorder slides. |
| `scripts/deck.mjs delete <deck> <slide> [<slide>...]` | Remove slide folders + `deck.json` entries. |
| `scripts/deck.mjs path <deck> <slide>` | Print absolute path + folder contents. |
| `scripts/deck.mjs list <deck>` | List slides in `deck.json` order. |
| `scripts/screenshot.mjs <deck> <slide>` | Headlessly render `slide.html` → `thumbnail.png`. |
| `scripts/screenshot.mjs <slide-dir>` | Same, given a direct slide directory. |
| `scripts/export.mjs <deck> [--mode editable\|raster] [--output ...]` | Export deck to a single .pptx. |

Every script emits a `[Done] / [State] / [Next] / [Hint] / [Error]` block
on stdout — those tags are how you track your own next step. Treat them as
a to-do list.

## Common pitfalls

- Skipping clarification and jumping straight to story planning → user says
  "this isn't what I wanted".
- User dropped a 10MB PPTX worth of material and you didn't run material
  digest first → context blown out.
- Time-sensitive page authored without research first → numbers are
  hallucinated.
- Long deck with no visual QC → exported file has 3 pages cropped.
- Batched 20 pages of authoring at once → authoring stops after the first
  few pages; "single page only" is a hard contract.
- Picked `--mode editable` proactively without the user asking → don't.
  Default is raster. Editable mode only opens when the user explicitly
  needs to edit inside PowerPoint, because editable export drifts on
  complex CSS / fonts / SVG.
- User asked for editable after a raster deck was already authored, and you
  exported directly without rewriting the HTML to the editable rules → wrong.
- Editable export looks wrong → drop the `--mode editable` flag. Default
  raster is the bulletproof path; do not stay in editable tweaking the
  same slide forever.
- User asked to "edit a slide" and you tried to mutate the exported .pptx
  → wrong loop. Edit `slide.html` instead, re-screenshot, re-export.
  HTML is the source of truth.
- Tried to use a tool named `web_fetch` / `web_search` and it doesn't
  exist → use the host's built-in webfetch / websearch instead. This skill
  ships none of its own.
