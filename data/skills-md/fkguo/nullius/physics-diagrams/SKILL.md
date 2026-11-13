---
name: physics-diagrams
description: "Create, revise, and verify publication-grade physics diagrams for LaTeX papers: Feynman/process diagrams, tree/loop/exchange diagrams, Bethe-Salpeter/Faddeev/integral-equation schematics, colored recursion blocks, multi-panel process figures, and geometry/angle/coordinate diagrams. Use when your agent needs to draw or repair diagrams with mathematical labels that must not overlap lines, produce editable source plus vector PDF for manuscript insertion, or audit whether a physics figure is publication-ready. Default to explicit-coordinate TikZ; use tikz-feynhand for particle-line idioms in Feynman/process diagrams; use Matplotlib/Python only for geometry/coordinate/angle schematics or styling already-computed data where it is a better fit. Do not use this skill to compute external numerical results for plots."
---

# Physics Diagrams

Use this skill to produce paper-ready physics diagrams, not quick sketches. The default path is
LaTeX-native: explicit-coordinate TikZ with shared `pd*` styles and manual label lanes. Use
`tikz-feynhand` when its propagator idioms make a Feynman/process diagram clearer.
Compile a standalone vector PDF, render a high-DPI preview, inspect the preview, then deliver both
source and PDF.

## Decision Tree

1. **Feynman/process/tree/loop/exchange diagram**: use explicit-coordinate TikZ; add
   `tikz-feynhand` when particle-line idioms such as `\propag`, `pho`, or `sca` are useful. Use
   hand-placed vertices. Do not rely on automatic graph layout for final figures.
2. **Integral-equation, BSE/Faddeev, recursion, colored-block schematic**: use TikZ nodes,
   paths, nested `tikzpicture` blocks, and `tikz-feynhand` only for local line idioms.
3. **Geometry, coordinate frames, angle planes, projected vectors, kinematic sketches**:
   use Matplotlib/Python when that makes geometry clearer. Keep TeX-like math labels and
   vector PDF output.
4. **Existing data plotted as a figure**: this skill may help with visual styling, labels, vector
   export, and QA, but it does not compute the numerical data. Use the project's own computation
   pipeline for physics results, and use the sibling `figure-hygiene` skill for data/results-plot
   correctness and legibility (data fidelity, chart choice by data shape, label economy, colour
   threading, render-then-verify).
5. **FeynArts/QGRAF**: use only upstream to enumerate or check model-generated topologies. Redraw
   selected publication figures in TikZ/feynhand or another final-layout backend.
6. **Inkscape**: use only for optional finishing, imported SVG cleanup, or manual repair. It is not
   the canonical source unless the user explicitly chooses an SVG-first workflow.

Read [references/tool-selection.md](references/tool-selection.md) when the backend is uncertain.

## Required Workflow

1. Write a semantic mini-spec before drawing: diagram role, particles/objects, line styles,
   vertices/blocks, labels, preferred label side, panel layout, manuscript width.
2. For diagrams that summarize an existing calculation, read the calculation source first and write a
   calculation-to-figure map: each kernel term, channel, topology, subdiagram, zero/selection rule, and
   intermediate state must have a corresponding visual element or an explicit reason for omission.
3. Pick the narrowest backend from the decision tree.
4. Choose the abstraction level for each row: if a component is expanded in a lower row, use one
   representative glyph in the parent row unless the algebra truly contains multiple factors or terms.
5. Use one editable source of truth:
   - default: standalone `figs/src/<name>.tex` -> `figs/<name>.pdf`;
   - existing manuscript inline style: keep `figs/<name>.tikz`, but create a standalone wrapper for QA;
   - Python geometry/plot route: keep the Python script plus generated vector PDF.
6. Reserve label lanes before drawing lines. Place labels with explicit anchors and offsets.
7. Compile in a clean build directory with [scripts/build_diagram.py](scripts/build_diagram.py).
8. Open or view the rendered PNG preview. Check every math label against the quality gate.
9. State whether the current agent can actually read the preview image. If not, mark the figure
   `NOT publication-ready` until a human or visual subagent/model reviews the preview.
10. For complex/submission-bound figures, or any figure with more than six labels, multiple panels, or
   nested `tikzpicture` blocks, ask an independent visual reviewer/subagent to inspect the preview.
   If policy and tools allow, a different model family may be used for this visual review.
11. Iterate coordinates, anchors, backing boxes, and spacing until the preview passes. When user
    critique reveals a reusable failure mode, update this skill or its references after fixing the
    figure.
12. If moving an approved scratch figure into a target paper repo, adapt it to that repo's figure
    convention (for example `figs/src/*.tikz` plus a build script) and use neutral filenames such as
    `<subject>_schematic`, not overclaiming names such as `<subject>_publication`.
13. Deliver: source path, vector PDF path, insertion snippet, preview path, mini-spec,
    image-reading verdict, verifier identity, and verification status.

## Label Safety Rules

- Prefer manual coordinates and explicit anchors over automatic edge labels.
- Give near-line labels a white backing: `fill=white`, `fill opacity=0.92`, `text opacity=1`,
  `inner sep=1pt`.
- Offset labels from paths with `above`, `below`, `left`, `right`, `near start`, `near end`,
  `xshift`, and `yshift`; do not center labels on strokes unless the white backing is intentional.
- Use filled circles/boxes/diamonds for amplitudes, kernels, propagators, and operators only when the
  calculation treats them as unresolved effective objects. If a propagator is dressed or has an
  explicit self-energy/loop definition in the paper or code, draw that topology instead of a box.
- For compact filled vertex blobs, draw all incident lines to the same center coordinate first, then
  draw the filled circle last so the unphysical interior line pieces are hidden.
- For HEP particle-line schematics, draw individual particles as single lines. Use solid single lines
  for heavy mesons such as `D` and `D^*`; use dashed single lines for light exchanged particles such
  as `K` and `\pi` unless the manuscript defines another convention.
- Draw a dimer/isobar as two separate nearby lines, not TikZ's closed-ended `double` stroke. Each of
  the two dimer lines should inherit the line style of the constituent particle: e.g. `DK` is one solid
  plus one dashed line, while `DD^*` is two solid lines.
- At an exchange vertex, do not let a dimer continue through the vertex as a dimer. A dimer emits one
  constituent/exchanged particle and becomes the remaining single particle; on the other leg, a single
  particle plus the exchanged particle becomes the outgoing dimer.
- Keep default colors restrained: black/gray strokes with low-saturation fills. Use strong colors only
  when the user asks or the manuscript already has that palette.
- Draw lines up to a block boundary and resume after the block; do not let a line pass through a block
  and rely on the fill to hide it.
- If an interaction is physically a point vertex such as a WT vertex, draw it as a vertex blob/circle
  with incident lines connected to the center and hidden by the blob. Do not draw it as an operator box
  with visible gaps between the line ends and the symbol.
- Do not collapse a multi-loop kernel or box contribution into a single vertex/block. If the calculation
  uses a two-loop box, show the box topology and its live intermediate particles or include the existing
  verified box source/PDF as a vector inset.
- For a dressed dimer--spectator propagator such as `G_i`, draw the spectator as a straight line and
  the dimer leg with its self-energy bubble (dimer constituents propagate and recombine), matching the
  paper's self-energy figure and the implementation, rather than inventing a generic `G` block.
- For channel-dependent exchange kernels, draw separate exchange topologies for each allowed channel
  pair. Do not use one generic exchange diagram labeled with a list such as `K,D^*,D` when the
  exchanged particle depends on the initial/final channel.
- Avoid putting every kernel component or subdiagram inside its own decorative box. Use open
  topology, shared baselines, thin separators, and only physically meaningful filled blocks/vertices.
- Keep ordinary topology vertices consistent across a figure: either show all of them with the same
  small-blob style or omit all ordinary blobs. Reserve distinct blob sizes/fills for genuinely
  different physical objects.
- In hierarchy/equation figures, keep `+`, `=`, and arrow glyphs on their own whitespace lanes. They
  should never touch a diagram or read as a line label. Balance the visual distance from an operator
  to the diagrams on both sides; inconsistent operator gaps make the row read as hand-spaced rather
  than typeset.
- Draw hierarchy arrows to named panel/box boundaries so the arrowhead touches the target boundary
  cleanly. Do not leave arrows hovering above the target, and do not let them pierce into the physics
  content.
- Size panel boxes from the actual content bounding box with modest, consistent padding. Oversized
  bottom padding makes the figure read as disconnected modules and should be corrected in preview QA.
- Keep related topology glyphs on comparable vertical scales. Expanded loop/box subdiagrams may need
  a little more room than exchange diagrams, but their upper and lower external channels should not be
  separated so much more that the figure reads as a different scale.
- Align repeated channels by shared coordinates, not by eye.
- Do not assemble one continuous physical propagator from multiple nested `tikzpicture` nodes; tiny
  coordinate mismatches create visible breaks. Draw continuous physical lines in one coordinate system,
  and use nested nodes only for separate subdiagrams or algebraic factors.
- For loops, keep particle labels outside the loop on normal directions; keep arrow marks away from
  labels.
- For multi-panel diagrams, reserve a panel-label corner before placing physics labels.
- A white backing may cover an incidental line behind text; it must not hide a physical vertex,
  arrowhead, crossing, or topology-defining connection.

## Verification Gate

Compilation is not completion. A diagram is deliverable only when all applicable checks pass:

- standalone source compiles to PDF without LaTeX errors;
- final vector PDF exists and is nonempty;
- high-DPI PNG preview is rendered and inspected;
- the agent states whether it can read images in this session;
- complex/submission-bound figures, multi-panel figures, nested-equation figures, and figures with
  more than six labels get an independent visual review when a reviewer surface is available;
- every label is legible at the intended manuscript width;
- no math label, panel label, or symbol overlaps a line, arrowhead, vertex, or another label;
- labels and arrowheads are not clipped;
- line styles, arrow semantics, colors, and block styles are consistent across panels;
- `pdfimages -list` reports no unexpected raster image objects for vector schematics;
- `pdffonts` reports embedded fonts when available;
- scratch logs, previews, and JSON reports live outside the repo unless the user explicitly asks to
  keep them.

Use [references/quality-gate.md](references/quality-gate.md) for the full checklist.

## Pattern References

- Universal presentation rules shared with data/results figures — colour threading, CVD safety,
  label economy floor and ceiling, role-mapped typography, render-then-verify — live in the sibling
  `figure-hygiene` skill and apply to schematics too; this skill stays scoped to
  schematic/topological content.
- TikZ/feynhand templates and idioms: [references/tikz-patterns.md](references/tikz-patterns.md).
- Python/Matplotlib geometry schematics and existing-data figure styling: [references/python-geometry.md](references/python-geometry.md).
- Tool choice and non-default backends: [references/tool-selection.md](references/tool-selection.md).
- QA and publication acceptance: [references/quality-gate.md](references/quality-gate.md).

## Smoke Examples

The default golden example is [assets/examples/basic_process.tex](assets/examples/basic_process.tex):
a deliberately simple, low-saturation process diagram with aligned labels and a vertex blob whose
incident lines meet at the center but are hidden inside the filled circle.

[assets/examples/feynhand_process.tex](assets/examples/feynhand_process.tex) is the same visual
grammar implemented with real `tikz-feynhand` vertices and `\propag` particle-line commands.

[assets/examples/neutral_schematic.tex](assets/examples/neutral_schematic.tex) is a complex stress
example for nested equation blocks and hierarchy arrows; do not treat it as the default visual style.

Run:

```bash
python3 skills/physics-diagrams/scripts/build_diagram.py \
  skills/physics-diagrams/assets/examples/basic_process.tex \
  --out-dir /tmp/physics-diagrams-basic
```

For direct-PDF routes such as Matplotlib:

```bash
python3 skills/physics-diagrams/scripts/build_diagram.py \
  --qa-only /tmp/physics-diagrams-matplotlib-example/geometry.pdf \
  --out-dir /tmp/physics-diagrams-geometry-qa
```

Then inspect the rendered preview before trusting the PDF.
