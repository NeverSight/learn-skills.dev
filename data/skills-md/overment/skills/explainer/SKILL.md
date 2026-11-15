---
name: explainer
description: >-
  Turns a system, flow, process, dataset or plan into a clear interactive diagram delivered as one self-contained HTML file: architecture and flow diagrams, sequence and state machines, bar, line, slope, scatter, waterfall, heatmap, treemap, Sankey, funnel, radar and quadrant charts, Gantt charts, timelines, kanban boards, user journeys, story maps, database schemas, UML class diagrams, swimlanes, fishbone and Wardley maps, and incident or release reports with an annotated timeline. Every diagram works bare or with text, in light and dark, with click-to-explore details and PNG capture. Use when asked to explain how something works, diagram or map a system, chart or compare numbers, plan a project, or screenshot such a diagram. Not for Svelte or .svx documents, app UI components, live dashboards over changing data, quick ASCII diagrams, or answers that read fine as a paragraph.
license: MIT (bundled Geist fonts under OFL-1.1, see assets/fonts/OFL.txt)
metadata:
  author: overment
  version: "0.5.0"
---

# Explainer

The reader is someone new to the system: a new teammate, a stakeholder, a reviewer. They need the model at a glance and the detail on demand. Without this skill, explanations become walls of text, or hand-drawn SVG where every box is styled differently. Arrows cross boxes, labels repeat what the arrow already says, and the diagram needs a paragraph of its own to decode.

You write a Markdown document with fenced data blocks. The engine places every part on a fixed grid, draws charts from your numbers, routes the connectors, and builds one HTML file with no network requests. You decide what to show. The engine decides how it looks, so don't fight it with styling.

Every page has two views: **bare** (diagrams and their interactions only) and **full** (plus the title, prose, a reading panel per figure, and the author's notes shown on the graph at once as numbered callouts). Readers switch with the controls; links and screenshots pick one with `#view=bare|full`. Design for bare first, and see [references/writing.md](references/writing.md) for the text budget.

A click on any mark opens a card inside the figure: computed facts (rank, share, delta), the `about` text and named relations, placed so it never hides what was clicked. Shift-click compares two marks. The whole state (selection, comparison, hidden series, step, theme, view) lives in the URL, so `shot` captures exactly what a reader saw.

## Workflow

1. **Read the real source.** Code, configs, docs, the conversation. Never invent a component, call or rule to make a figure look complete. If a part is unknown, leave it out and say so.
2. **Plan, then say the plan.** Pick a template (`new --list`) and a layout from the table below. In two or three lines, state the layout, the focal part, and what the budget forces out.
3. **Write the blocks, then the least prose that works.** A `title`, one or two sentences of conclusion, then the diagram. No eyebrow, no summary, no "the figure shows". Names go on the canvas and meaning goes in `about`. Link every claim to the marks that prove it (`[4,120 signups from organic search](#signups-organic-search)`, or `#a+b` to compare two). For the full view, add `notes:` (note 1 the focal fact, note 2 the pattern) and a `caveat:`; a `story:` plus a `steps` block walks the reader through. Syntax is in [references/format.md](references/format.md) and `references/blocks/`.
4. **Run `check`** until it reports no errors. Fix each warning, or say why it's acceptable.
5. **Run `build`** for a file, or **`watch`** while iterating with the user.
6. **Run `audit`** before handing over. It catches overflow, overlaps, contrast and broken clicks that `check` can't see.
7. **Run `shot`** when the user wants an image, or **`export`** when they want editable SVG.
8. **Report** the output path, plus what you simplified, merged or cut to stay in budget, so the user can ask for it back.

## Commands

```sh
bun <skill-dir>/scripts/explainer.ts <command> [args]
```

Needs Bun 1.4 or later and installs nothing. Only `audit`, `shot`, `export` and `gallery` need Chrome. They look at `CHROME_PATH` first, then the usual install locations. Set `CHROME_PATH` when Chrome isn't found.

| Command | What it does |
|---|---|
| `new <template> <out.md> \| new --list` | Copies a starter document. `new --list` lists the templates |
| `build <doc.md> [-o out.html] [--theme name\|path] [--mode light\|dark]` | Writes the HTML file and prints its path, size and diagnostics. Exits 1 on errors |
| `watch <doc.md> [--port 4646] [--theme name\|path] [--mode light\|dark] [--no-open]` | Serves the page and reloads it on every save |
| `check <doc.md>...` | Lints without a browser. Prints `file:line rule message` |
| `audit <doc.md\|out.html>... [--state "sel=x&theme=dark"]... [--json]` | Runs headless Chrome checks in light and dark, bare and full, at rest and with the focal element, a related element and every front-matter `shots:` state selected: text clipped or overflowing, engine-inserted `…`, label × line crossings, labels drawn over each other, figures wider than the column, the card covering the selection or what it relates to, related elements dimmed, dimmed text under 3:1, an invisible selection ring, relation rows that repeat both ends, the click test per element type, contrast, console errors and the no-JS render. Prints `✗` for failures and `–` for checks it could not run. Exits 1 on any failure |
| `shot <doc.md\|out.html> [--figure id] [--state "sel=gw&cmp=db&theme=dark"] [--view bare\|full] [--scale 2] [--width 1280] [--out x.png] [--page]` | Saves a PNG of a figure (with its open card, note markers, reading panel in `--view full`, and step note when a scene is on) or of the whole page, in any state. Wide boards are captured whole |
| `export <doc.md\|out.html> [--figure id] [--state "sel=gw&theme=dark"] [--mode light\|dark] [-o x.svg]` | Saves a standalone SVG with styles inlined, for Figma or Keynote. `--state` bakes the selection, its ring and the card into the file |
| `gallery [out-dir] [--src dir]... [--no-shots] [--open]` | Builds every template (plus any `--src` documents) and an index page showing each one at rest, selected and expanded (reading panel), in light and dark, including matrix and compare blocks. Use it to see what each layout looks like, or to review a set of documents together |
| `help [command] \| help --markdown` | Prints usage. `help --markdown` prints this table |

## Style guide

The look comes from one theme file: colors for light and dark, a sans and a mono font, the type sizes, the grid, and a single corner radius. To match a brand, create `<project>/.explainer/themes/<name>.json` (or `~/.explainer/themes/<name>.json` for every project) containing `{ "extends": "default" }` plus only the keys that change, then set `theme: <name>` in the front matter. Font files are `.woff2` placed next to the theme and embedded at build time. An optional `fonts.heading` sets a display face for the page title only; diagrams always use the sans. The keys are in [scripts/engine/types.ts](scripts/engine/types.ts) (`Theme`), and the shipped values are in [themes/default.json](themes/default.json). Never restyle inside a document. If something looks wrong everywhere, fix the theme.

## Which block for what

| To show… | Block | Starter |
|---|---|---|
| Parts and how things move between them | figure: `flow`, `zones`, `hub`, `layers`, `tree`, `cycle` | `single-figure`, `system-map`, `hub`, `layers`, `tree`, `cycle` |
| States and transitions, decisions (`kind: decision`) | figure: `states` | `states` |
| Who calls whom, in time order | figure: `sequence` | `sequence` |
| What a model is sent on each call; how an agent's context grows | `context` (pair with a `sequence`) | `context` |
| Who does what across teams, with handoffs | `swimlane` | `swimlane` |
| One path at a time | `scenes` + `steps` | `walkthrough` |
| Compare amounts across categories | `bar` (grouped, stacked) | `bar` |
| A start total bridged to an end total | `waterfall` | `waterfall` |
| Before and after per item | `dumbbell`, `slope` | `dumbbell`, `slope` |
| Trends over time; rank changes | `line` (area), `bump` | `line`, `bump` |
| Two measures per item; a third as size | `scatter` (bubbles) | `scatter` |
| One measure, one dot per item | `beeswarm` | `beeswarm` |
| Values across two dimensions | `heatmap` | `heatmap` |
| Part of a whole; shares within segments | `treemap`, `marimekko` | `treemap`, `marimekko` |
| Drop-off through stages; ranked levels | `funnel`, `pyramid` | `funnel`, `pyramid` |
| Quantities splitting and merging | `sankey` | `sankey` |
| Scores across several criteria; a cyclic measure | `radar`, `polar` | `radar`, `polar` |
| Overlap between sets; two-axis prioritisation | `venn`, `quadrant` | `venn`, `quadrant` |
| Work on a calendar, with dependencies; dated events | `gantt`, `timeline` | `gantt`, `timeline` |
| Work in progress by state | `kanban` | `kanban` |
| An experience stage by stage, with sentiment | `journey` | `journey` |
| A product backbone sliced into releases | `storymap` | `storymap` |
| Tables, columns and keys (column-to-column foreign keys, crow's feet); classes, members and relations | `schema`, `uml` | `schema`, `uml` |
| Causes of one effect; value chain vs evolution; containment | `fishbone`, `wardley`, `nested` | `fishbone`, `wardley`, `nested` |
| Which part may do what; two options side by side | `matrix`, `compare` | `explainer`, `compare` |
| A caveat, a term, a live control | `note`, `glossary`, `widget` | `explainer` |
| An incident, fix or release on one page: what happened when, root cause → fix, before/after numbers, how to verify | `meta`, `events`, `change`, `metrics`, `checklist` | `report` |

Grid layouts and their anti-patterns are in [references/layouts.md](references/layouts.md). Every other block's keys, defaults and budgets are in `references/blocks/`. Run `gallery` to see every starter rendered.

## Concepts

- **BLUF (inverted pyramid).** The first paragraph states the conclusion a reader would take away after reading everything. The figure proves it, and sections add detail in falling order of importance. A reader who stops after any section should still be right.
- **Deletion first.** A figure is done when nothing more can be removed, not when nothing more can be added. Budgets per figure are 9 nodes, 12 connectors and 2 focal parts. Over budget, split into an overview plus a detail figure; never shrink. Walk through the per-figure pass in [references/writing.md](references/writing.md).
- **Progressive disclosure.** The canvas carries names only: a short label, maybe a `sub`, and a connector label only where the arrow isn't obvious. Meaning lives in `about` and shows in the card on click, next to computed facts. The prose tells the story, the reading panel proves it note by note, and [interactions](references/interactions.md) let the reader dig.
- **Plain technical English (ASD-STE100).** Write labels, `about` texts, notes and prose about 80% of the way to STE: one fact or one instruction per sentence, the active voice, simple tenses, short noun clusters, one word per meaning. `check` warns on any sentence over 25 words (`sentence-long`). The rules and examples are in [references/writing.md](references/writing.md).
- **Trust.** Markdown text is escaped (raw HTML shows as text, only http(s), mailto and `#` links survive), so text lifted from code or conversations is safe in labels, prose and `about`. A `widget` body is code that runs in every reader's browser and in the Chrome that `shot`, `audit` and `export` start: never put untrusted text there.
- **One source of emphasis.** Mark at most two parts `focal`: the accent means "the author's point". Selection is an ink ring, never accent. Focus comes from dimming everything else, not from making the target louder. Never add colour, bold or extra boxes to make something stand out.

## Ask yourself before building

- Could someone new explain the system back to me after ten seconds with the figure?
- Does every node, connector and label earn its place? What did I cut?
- Is every part in the figure something I read in the source, not something I assumed?
- Would a teammate who joined today understand each part from its `about` alone: what it does, why it is there, what to watch?
- Is there one clear focal point, or is everything equally loud?

## References

- [references/format.md](references/format.md): every key of every block, containers, ids, grid geometry, label limits, lint rules.
- [references/layouts.md](references/layouts.md): the grid figure layouts with sketches.
- `references/blocks/`: charts ([bars](references/blocks/charts-bars.md), [lines](references/blocks/charts-lines.md), [grids](references/blocks/charts-grids.md), [flows](references/blocks/charts-flows.md), [radial](references/blocks/charts-radial.md)), plans ([time](references/blocks/plans-time.md), [boards](references/blocks/plans-boards.md)), structures ([schema and UML](references/blocks/structures-schema.md), [maps](references/blocks/structures-maps.md)), [model context](references/blocks/context.md) and [reports](references/blocks/report.md).
- [references/writing.md](references/writing.md): labelling voice, before-and-after pairs, the per-figure pass.
- [references/interactions.md](references/interactions.md): state and URL hash, selection tiers, the card, keyboard, prose linking, the reading panel, scenes and stories, widgets, and the engine contract.
- [references/capture.md](references/capture.md): `shot`, `export`, `audit`.
- [references/design-law.md](references/design-law.md): the visual rules the theme and engine enforce.
