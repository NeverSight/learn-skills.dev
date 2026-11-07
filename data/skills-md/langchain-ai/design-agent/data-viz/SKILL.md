---
name: data-viz
description: Charts, stat cards, flywheels and diagrams (flows, architectures, hierarchies) rendered on brand from a JSON spec to PNG and SVG. Use for any visual whose job is numbers or relationships, including restyling an attached chart or diagram.
---

# data-viz

You describe the data and the words; the renderer applies the brand, computes every value (pivots,
totals, steps, bins, changes, ratios, scales) and refuses a chart that would misstate its data.

```bash
cd /workspace
V=/workspace/skills/data-viz/scripts/viz.mjs
node $V --spec projects/<slug>/chart.json                   # writes out (PNG) and svgOut if set
node $V --spec projects/<slug>/chart.json --validate-only   # gates and topology only, writes nothing
node $V --list-kinds                                        # every kind and its data fields
node $V --list-transforms                                   # allowlisted transforms and their arguments
```

Paths resolve under the working directory. Success prints one JSON line: dataset hash and gate
verdicts for charts, the topology hash and audit for diagrams, computed values, the palette actually
used, and the PNG size. Exit 1 means the spec, a gate or an audit failed: the message says which, so
fix the spec. Exit 2 means the tool could not run (toolchain, D2, fontconfig or brand pack missing):
report it.

## Pick the kind

| Job | kind |
| --- | --- |
| One number, or a before and after | `stat-card` |
| Compare values; one bar is the point | `bar` with `highlight` (and `annotate` for a short note) |
| Parts of a whole by group, or 2-3 groups side by side | `bar` with `series` (and `stack`) |
| A trend; several series with one that matters | `line` (`series` + `highlight` past 3 series) |
| A trade-off between two measures | `scatter` |
| A matrix | `heatmap` |
| From an opening to a closing number | `waterfall` |
| A distribution | `histogram` |
| Quantities flowing between stages | `sankey` |
| A loop of 2-8 stages (a flywheel) | `cycle` |
| A flow, architecture or hierarchy | `diagram` (D2, `elk` or `dagre`) |

Every field, with a minimal spec per kind: [references/spec-reference.md](references/spec-reference.md).
Start from an example: [bar with one annotated bar](examples/bar-annotated.json),
[flywheel](examples/flywheel-cycle.json), [stat card](examples/stat-card.json),
[diagram](examples/diagram-flow.json).

## The contract with you

- **Data goes in as a typed dataset** (`fields` with `dimension`, `measure` with `unit` and
  `precision`, or `temporal`; then `rows`). Reshape with declared `transforms` (`filter`, `sort`,
  `topN`, `aggregate`, `bin`, `normalize`, `percentChange`, `cumulative`), never by editing the
  numbers you were given, or the dataset hash stops being a receipt.
- **Gates fail closed** before anything renders: a bar, waterfall or histogram axis must include zero;
  one value axis carries one unit; shares marked `partToWhole` must sum to 100%; type must clear
  12 px at the delivered size; more than three series need a `highlight`.
- **Diagrams and cycles freeze meaning in a `contract`** (`nodes` with id and label; `edges` with id,
  from, to, kind and optional label). Pin `expectedTopologyHash` from the first render on every
  styling revision: the renderer then fails if a label, endpoint, direction or kind moved. After
  layout, the SVG is read back and must contain exactly the contract's nodes and edges.
- **Brand comes from the brand pack.** Ground, ink, accent, muted, rule and series colours are
  measured from `/workspace/brand/tokens.json`; fonts are its stacks. Pin a role to a token when the
  brand's graphic language asks for it (`"colors": {"ground": "--brand-color-paper"}`). A palette
  audit fails the render if any painted colour is not a brand colour, and a font check fails it if a
  brand family would fall back.

## Judgment

- **Concept first.** Decide the one thing the visual says, then pick the kind that says it. A box is
  its label; draw the actual mechanism, never a generic network of dots and nodes.
- **Fewest words.** `title` and `caption` only when the ask supplies them or the figure misreads
  without them; a caption is a source line, nothing more. The explanation goes in your reply.
- **One accent per frame**: the highlighted bar, line, point or stage. Everything else is quiet.
- **A data model shows its rules.** When the ask says a relationship is required or optional ("at
  least one user", "can relate to"), put it on the edge (`label`: `1..*`, `0..*`) rather than in a
  footnote: that rule is usually the reason for the diagram.
- **Look at the PNG** (`node /workspace/tools/review-thumb.mjs <png>`, then `look`) before you deliver.
  Gates prove the numbers and the structure, not the taste: crowded labels, a lopsided layout or a
  weak concept are still yours to catch. A blog or doc figure is read about 720 px wide; check that
  its labels survive that size.
- When values were estimated (read off a screenshot, rebuilt from a percentile), say so in the
  caption.

More craft and which-visual guidance: [references/viz-patterns.md](references/viz-patterns.md).

## Restyling an attached chart or diagram

A restyle is a transformation, not a redesign: keep every label, value, annotation, relationship and
grouping unless the brief changes it. Write the contract (or dataset) from the source first; read an
SVG or PDF's structure directly when you have it, and for a raster, inspect every arrowhead before
writing an edge. If an endpoint is ambiguous, ask. Recompose for the requested ratio by spacing what
is there, without adding a title, footer or logo to fill the frame. Then compare source and render
side by side (`visual-verify`).

## When not to use it

A typographic composition with no data or relationships (a three-up row of numbers, a quote card) is
an HTML still (`stills`). A conceptual illustration is `stills` or `image-generation`. A chart inside
a film is a HyperFrames scene that can embed this skill's SVG.
