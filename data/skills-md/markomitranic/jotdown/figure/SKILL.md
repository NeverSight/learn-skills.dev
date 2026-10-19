---
name: figure
description: Use only when working on the docs site. Draw or edit an inline SVG figure in a docs page. Use whenever a page needs a diagram or a visual explainer, or when an existing figure needs changes.
---
# Figure

Docs pages in this repo illustrate mechanisms with hand-drawn figures. The
default medium is an inline SVG that lives directly in the `.mdx` and paints
only with `--jd-fig-*` CSS variables, so it works in both colour modes for
free. An HTML figure is the escape hatch, near the end of this file.

This file is the index: how to choose the shape of a figure, and the rules
every figure follows. The layout grammar of each shape lives in
`references/forms/`, one file per form, loaded once the form is chosen and never
all at once. The craft of drawing comes from skills that ship with Claude Code,
loaded through the Skill tool before the first line of SVG.

The palette is thirteen tokens, each worked out from the project's theme:

| Token | Paints |
| --- | --- |
| `--jd-fig-ink` | labels, from `foreground` |
| `--jd-fig-muted` | sublabels and quiet text, from the muted foreground |
| `--jd-fig-line` | box outlines and connectors |
| `--jd-fig-line-soft` | hairlines, dividers, the faintest outline |
| `--jd-fig-surface` | a box's fill |
| `--jd-fig-accent`, `--jd-fig-accent-soft` | the one or two elements the figure is about, from `primary` |
| `--jd-fig-p-ink`, `--jd-fig-p-bg` | the first hue, from `chart-1` |
| `--jd-fig-d-ink`, `--jd-fig-d-bg` | the second hue, from `chart-2` |
| `--jd-fig-i-ink`, `--jd-fig-i-bg` | the third hue, from `chart-3` |

## Figure, chart or editorial illustration

This skill draws figures: the parts of a mechanism and how they connect,
standardised, in the site's figure palette. Two other skills sit beside it:

- A bar, line, area, pie or radar chart of real numbers is a `<Chart />` block.
  Use the `chart` skill.
- The picture that opens every page, the way a magazine opens an article, is an
  editorial illustration. Use the `editorial-illustration` skill, which paints
  in its own style into an SVG file of its own, not into the page, and does not
  follow the rules below. A figure belongs in the chapters, where it explains.

## Which built-in skill to load

Load one, not all, picked by the form decided below:

| Form | Load | It covers |
| --- | --- | --- |
| any mechanism: boxes and arrows, a flow, a hierarchy, a timeline | `artifact-diagramming` | when a picture earns its place, drawing the real mechanism, labelling arrows |
| any chart | `dataviz` | which chart, how few marks it needs, axis and label rules, a colour formula |
| an HTML figure with real typography | `frontend-design` (a plugin, not always installed) | type, spacing and layout choices that do not look templated |

Skip `artifact-design`, `artifact-capabilities` and `design`; they are about
whole Artifact pages. Any other visual skill you have access to is fair to load.
Their mechanics are for standalone pages, so ignore what they say about
`data-theme`, `currentColor`, CDNs and page layout. Only the drawing advice
carries over; markup and colour are decided here.

## Pick the form first

Read the paragraph the figure will sit beside and ask what kind of thing it is
talking about. Then find that thing in the tables. Before any row, the cheaper
test: if a sentence or a three-column markdown table says it as fast, write that
instead.

A row is a candidate, not a verdict. Open its file and read the entry test at
the top before placing a rectangle; a form that fails its own test is the wrong
form, however well the row read. The last row of the Mechanisms table is a real
destination, not an apology, and landing there is not a failure to classify.
Several forms share a file, so the reference column is what you open.

### Mermaid or a figure

A ```mermaid fence is the other way to draw here, and the repo rule is already
set: Mermaid for a deterministic reference diagram a human will maintain, a
figure for an illustration beside prose. Four forms are nearly always the first
kind, because their content is a data set someone will edit later: a Gantt, a
kanban board, an ER or database schema, a class diagram. Their rows point at
the fence and there is no form file for them. For everything else, ask which
kind this one is. The sequence that specifies an API is a fence; the three-actor
sequence that explains why the cache is there is a figure.

### Mechanisms

| The prose is about | Form | Reference |
| --- | --- | --- |
| components of a system and which pairs are connected | What talks to what | `forms/what-talks-to-what.md` |
| where software runs: hosts, zones, replicas, versions | Deployment | `forms/what-talks-to-what.md` |
| a data platform end to end: sources, core, consumers | Platform integration | `forms/what-talks-to-what.md` |
| a legacy landscape, the "before" of a migration | Current state | `forms/what-talks-to-what.md` |
| a decision with branches, a "should I" | Flowchart | `forms/flowchart.md` |
| messages between actors in time order, a request trace | Sequence | `forms/sequence.md` |
| states and what moves a thing between them | State machine | `forms/state.md` |
| events placed in time: releases, milestones, an incident | Timeline | `forms/timeline.md` |
| a process with handoffs between teams or roles | Swimlane | `forms/swimlane.md` |
| the same, with what each step consumes and produces | Process | `forms/swimlane.md` |
| stacked abstraction levels, a stack, a cascade | Layer stack | `forms/layers.md` |
| storage tiers of one dataset by quality level | Medallion | `forms/layers.md` |
| scope by containment, trust zones, blast radius | Nested | `forms/nested.md` |
| parent to children: a taxonomy, a file tree | Tree | `forms/tree.md` |
| who owns what, routing, escalation | Org chart | `forms/tree.md` |
| what depends on what, with a shared dependency or a cycle | Dependency graph | `forms/dependency.md` |
| a cycle where the last step feeds the first and a hub keeps state | Loop | `forms/loop.md` |
| entities, fields, cardinality, or real tables and foreign keys | ER, schema | a ```mermaid fence, `erDiagram` |
| classes, inheritance, composition, operations | UML class | a ```mermaid fence, `classDiagram` |
| commits, branches and merges | Git graph | a ```mermaid fence, `gitGraph` |
| a mechanism none of these names | draw what the prose describes | no file, the Rules below |

### Comparisons and positions

| The prose is about | Form | Reference |
| --- | --- | --- |
| two axes, prioritisation, a 2x2 | Quadrant | `forms/quadrant.md` |
| where two or three concepts overlap | Venn | `forms/venn.md` |
| a ranked hierarchy, or a conversion drop-off | Pyramid or funnel | `forms/pyramid.md` |
| a value chain against how commoditised each part is | Wardley map | `forms/wardley.md` |
| per-role, per-component permissions | Access matrix | a markdown table |

### Work and people

| The prose is about | Form | Reference |
| --- | --- | --- |
| what a person does at each stage and how it feels | User journey | `forms/journey.md` |
| a narrative backbone sliced into releases | Story map | `forms/story-map.md` |
| the causes of one effect, grouped by category | Fishbone | `forms/fishbone.md` |
| tasks with start and end dates, in phases | Gantt | a ```mermaid fence, `gantt` |
| work in progress by state, WIP limits, blocked items | Kanban | a ```mermaid fence, `kanban` |

### Numbers

Load `dataviz` for the chart itself. Three sentences of numbers in a paragraph
should have been one of these. A plain bar, line, area, pie or radar chart is a
`<Chart />` block from the `chart` skill; draw one here only when it needs a form
that block does not have, or annotation it cannot carry.

| The prose is about | Form | Reference |
| --- | --- | --- |
| a value that changed, or quantities per category, or a ranking | bar | `forms/bar.md` |
| exactly two values per item where the gap is the story | dumbbell | `forms/bar.md` |
| a start total bridged to an end total by signed steps | waterfall | `forms/waterfall.md` |
| a trend over time | line | `forms/line.md` |
| change between exactly two points in time, per item | slopegraph | `forms/line.md` |
| rank movement across several snapshots | bump | `forms/line.md` |
| one distribution per series | ridgeline | `forms/line.md` |
| two variables: correlation, clusters, outliers | scatter | `forms/scatter.md` |
| three variables: x, y and a magnitude | bubble | `forms/scatter.md` |
| one variable, one dot per item | beeswarm | `forms/scatter.md` |
| a quantity splitting and merging across stages | sankey | `forms/sankey.md` |
| part of a whole, where relative size is the story | treemap | `forms/treemap.md` |
| several things scored on three to five criteria | radar | `forms/radar.md` |
| one series across categories whose cyclic order matters | polar | `forms/radar.md` |

## Markup

```mdx
<figure className="jd-fig">
  <div className="jd-fig-frame">
    <svg viewBox="0 0 960 240" role="img" aria-label="One sentence describing what the figure shows">
      ...
    </svg>
  </div>
  <figcaption>The takeaway.</figcaption>
</figure>
```

The framework's `jd-fig` class handles the frame, the width, scaling down on a
narrow screen and the mono face for `<text>`, so a figure carries none of that
itself.

An SVG figure's caption is not shown on the page. Screen readers and search
read it, and it appears under the drawing when the reader expands it. So the
prose around the figure carries the point, and the caption restates it for
the reader looking at the drawing alone. An HTML figure cannot be expanded and
keeps its caption visible.

## Rules

- **Every colour is a `var(--jd-fig-*)`**, fills and strokes alike. Each token
  is derived from the project's theme: neutrals from the shell, the accent from
  `primary`, and the p, d and i hues from `chart-1` to `chart-3`. A figure never
  names a colour of its own.
- **This is JSX.** Attributes are camelCase: `fontSize`, `strokeWidth`,
  `strokeDasharray`, `textAnchor`, `markerEnd`, `letterSpacing`. Escape `&` as
  `&amp;`. Comments are `{/* ... */}`.
- **A label is still markdown.** `_category_.json` in a `<text>` renders an
  `<em>` inside the SVG, the browser moves it out, React finds a tree it did not
  send, and the page is thrown away and drawn again on the client. Escape
  emphasis in a label (`\_category\_`, `\*`) or write the word without it. A
  colon before a word (`11:04:07`) is the same trap, and that one the framework
  already puts back as text.
- **Marker ids are page-global.** Every figure on a page shares one DOM, so
  prefix every `<marker>` id per figure (`lk-arrow`, `lk-arrow-accent`) and
  never reuse `arrow` across figures.
- **4px grid.** Every x, y, width, height, radius and gap is a multiple of 4.
  A coordinate ending in 1, 2, 3, 5, 6, 7 or 9 is a mistake. Stroke widths and
  font sizes are exempt.
- **`viewBox` is 960 wide.** Pick the height to fit the drawing, no dead space.
- **Type scale.** 12 for node labels (`fontWeight="600"` for a name), 10 for
  annotations and arrow labels, 9.5 with `opacity="0.75"` for sublabels.
  All-caps eyebrows and band titles are `fontSize="10" letterSpacing="1.5"`.
  Never `writing-mode` vertical text: stack words as separate lines instead.
- **Accent on one thing, two at most.** `--jd-fig-accent` marks what the figure
  is about: the hop being added, the state the reader should notice, the path
  under discussion. If four things want it, you have not decided what the
  figure is about. Everything else is ink, muted and the layer hues.

### Node roles

Shape and stroke carry the role. Fill is quiet unless the role says otherwise.

| Role | Fill | Stroke |
| --- | --- | --- |
| the one or two the figure is about | `accent-soft` | `accent`, `strokeWidth="1.5"` |
| a step, a service, a component | `surface` | `line`, or the layer ink (`p-ink`, `d-ink`, `i-ink`) when the figure has layers |
| a store, state at rest, a file, a record | the layer bg (`p-bg`, `d-bg`, `i-bg`), or `line-soft` unlayered | as a component |
| outside our control: a vendor, a browser, a third party | `surface` | `line-soft`, label in `muted` |
| optional, async, not always present | `surface` | `line`, `strokeDasharray="4 3"` |
| a zone, a boundary, a group | none | `line-soft`, `rx="8"`, eyebrow label inside the top-left corner |

Nodes are `<rect rx="4">`.

### Zones

A zone groups the nodes that share a tier, an owner, an environment or a trust
boundary. Any form may use one; several do.

- A `<rect rx="8">` with no fill and a `line-soft` stroke, drawn before
  everything else so arrows and labels land on top of it. Dashed
  (`strokeDasharray="4 4"`) when the boundary is a network or trust edge rather
  than a grouping: a VPC, a security group, an environment.
- An eyebrow label inside its top-left corner, `fontSize="10"
  letterSpacing="1.5"` in `muted`, with 16px clear between that label and the
  first node under it.
- Three at most. More than three reads as a swimlane, so draw one of those
  instead.
- A zone is not a node and owns no arrows. Connect the nodes inside it, and let
  the zone say what they have in common.

### Connectors

Draw zones first, then arrows, then arrow labels, then nodes, then node text.
A box painted after its arrow hides the arrow's overshoot, and a label painted
before the nodes has to sit in open canvas or a node will cover it.

One marker per stroke colour, defined once, ids prefixed per figure:

```mdx
<marker id="lk-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
  <path d="M0,0 L10,5 L0,10 z" fill="var(--jd-fig-line)" />
</marker>
```

| Line | Meaning |
| --- | --- |
| solid `line`, `strokeWidth="1.5"`, filled head | the primary flow, a call, data moving |
| solid `accent`, `strokeWidth="1.5"`, accent head | the one path the figure is about |
| dashed `muted`, `strokeDasharray="4 3"`, `strokeWidth="1"`, filled head | a return, a secondary flow, something optional |
| dashed `muted`, open head (`fill="none"`, stroked path in the marker) | async, an event, one-way notify |
| plain `line`, no head | a relationship with no direction, a hairline |

Six rules, for every form unless its file names an exemption (a data curve, a
sankey ribbon, a loop's ring and spokes, a fishbone's bones, a Wardley link):

1. **Orthogonal, with rounded corners.** A straight `<line>` only joins two
   points that share an x or a y. Anything else is an elbow with quarter-arc
   corners of radius 8. Right and down, from (200,120) to (400,200), bending at
   x 300:
   ```mdx
   <path d="M 200,120 H 292 Q 300,120 300,128 V 192 Q 300,200 308,200 H 400"
     fill="none" stroke="var(--jd-fig-line)" strokeWidth="1.5" markerEnd="url(#lk-arrow)" />
   ```
   Dashed paths route the same way; the dash says what a line means, not how it
   travels.
2. **A label sits 6 to 10px clear of its stroke, never on it.** Centred on its
   segment, above a horizontal one or beside a vertical one, three words at
   most. No masking rectangles: a label goes where there is open canvas, and if
   there is nowhere clear the figure is over budget.
3. **No two connectors share a path.** Parallel runs stay 12px apart end to
   end. Two that must cross: the less important one hops with a small arc, and
   only one hops. If you are stacking connectors, two nodes are too close.
4. **Connectors sharing a box edge get their own attach points**, the k-th of N
   at `L · k / (N + 1)` along an edge of length L, never closer than 12px.
5. **A connector never passes behind a box that is not its source or
   destination.** Reroute. The one exception is a box that physically sits on
   the only straight path, a footer bar say: then the line is dashed, its label
   sits at the visible end, and no arrowhead lands on the box being crossed.
6. **A label never sits where a box drawn later will cover it.** A badge inside
   its own node is fine; a label over a zone is fine since zones paint first.

### Charts

- The plot spans x 80 to 920 and y 40 to 420 inside `viewBox="0 0 960 480"`,
  leaving room for axis values on the left and category names below.
- Four to six gridlines in `line-soft`, `strokeWidth="0.8"`; axis lines in
  `line`; axis values `fontSize="10"` `muted` right-aligned at x 72; category
  names `fontSize="12" fontWeight="600"`.
- One focal mark in the accent. Every other mark is `line-soft` fill with a
  `muted` stroke.
- Values on the marks, `fontSize="10"`. A legend only when the same encoding
  repeats, and then a strip under the plot with a hairline above it.
- A magnitude axis starts at zero. The caption says what the marks encode, and
  the prose says where the numbers came from.

## HTML figures

Prefer SVG. Reach for HTML only when SVG is worse at the specific kind of
figure: real text wrapping, a long list, or a comparison table dressed as a
figure. Something interactive is beyond a page, since a page cannot run code.

An HTML figure keeps the same `jd-fig` / `jd-fig-frame` wrapper and styles
itself through a `<style>` tag inside the figure. MDX parses `{ ... }` as a JSX
expression, so the CSS must be a template-literal child or the build fails:

```mdx
<figure className="jd-fig fig-checkout">
  <style>{`
    .fig-checkout .step { background: var(--jd-fig-surface); border: 1px solid var(--jd-fig-line); }
    .fig-checkout .step.active { background: var(--jd-fig-d-bg); color: var(--jd-fig-d-ink); }
  `}</style>
  <div className="jd-fig-frame">
    ...
  </div>
  <figcaption>...</figcaption>
</figure>
```

- Nest every selector under a unique `fig-*` class on the figure. Bare class
  names like `.step` are global while the page is mounted and restyle theme
  elements.
- Colours still come only from `--jd-fig-*` tokens. No inline `style`
  attributes, same as everywhere else in the repo.
- This is the only place a page-local `<style>` tag is allowed. Never promote
  figure styling into a new prose-block class; article prose is plain markdown.

## Taste

A figure accompanies a specific piece of prose and shows the thing the prose is
explaining, the way a good educator draws on a whiteboard. Be creative in the
form of the drawing, not in metaphor: illustrate what the paragraph says and
what is changing.

- Chapter paragraphs, code and figures are interwoven. A figure points at the
  concept in the paragraphs around it.
- One idea per figure. A figure that needs a legend is usually two figures.
- Draw the actual mechanism. Boxes are real components, arrows are real calls or
  data, and every arrow is labelled with what travels along it.
- The highest-quality move is usually deletion. Two nodes that always travel
  together are one node. A relationship obvious from layout needs no line.
  Above nine nodes it is probably two figures.
- Fewer than 20 words inside a figure. Detail belongs in the prose; the
  figure is for seeing.

## Say the plan before you draw

Write one or two sentences, in the reply, before the first line of SVG: the form
you picked, what the figure is about (the thing that gets the accent), and
anything the budget forces out. If there is a human to read it, they can
redirect you for the price of a sentence instead of the price of a figure.

The point is that a misrouted form is cheap to fix at this moment and expensive
twenty minutes later, when the coordinates are laid out and the sunk cost argues
for keeping them. Skip it only when the request already names the form and the
content.

## Render it and look

You cannot judge an SVG from its source. Render the page's figures, read the
images, fix what is wrong and render again:

```sh
export AGENT_BROWSER_SESSION="$(agent-browser session id --scope worktree --prefix task)"
bun .agents/skills/figure/scripts/render.ts docs/index.mdx
```

It paints every `jd-fig` on the page in the project's theme, dark and light, and prints the paths of the PNGs. A number after
the page renders just that figure. Run it from the repository root, with
`agent-browser` installed; `node` runs it as well as `bun`.

## Before you finish

- Does the figure carry everything its form file says it must carry?
- Did you say the form and the claim before you drew, and is what you drew
  still that?
- Can any node, arrow or label be removed and the figure still read?
- Is the accent on at most two elements, and are they what the figure is about?
- Every colour a token, every attribute camelCase, every marker id prefixed?
- Every coordinate on the 4px grid, every connector an elbow or a straight line,
  every label clear of its stroke and of every box?
- Did you render it in both modes and read the images?
- Does the `aria-label` say what the figure shows, in one sentence, without
  describing the shapes?
