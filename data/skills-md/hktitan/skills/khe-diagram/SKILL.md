---
name: khe-diagram
description: "Decides whether a diagram earns its place over a sentence or a table, picks the surface by who touches the picture next, then draws a finished editorial figure or edits a live tldraw canvas, with connector, accent and budget rules that also serve as the review. Use when someone says \"can you diagram this\", \"draw the architecture\", \"make a flowchart\", \"sketch this on a board\", \"my diagram looks like Mermaid\", or names tldraw, a .tldraw file or diagram-design. For SVG markup and animation use `khe-svg`; for a live chart inside a product use `khe-ui`; for a leader line on a product shot use `stageshow`."
license: MIT
metadata:
  author: Harshit Khemani
  version: "1.0.0"
---

# Diagram

You own the picture from "can you diagram this?" to a figure someone can read, or a clear no. A diagram is the costliest way to say something.

A construction skill. It does ONE thing: decide whether a picture says more than a paragraph or a table, choose the surface by who touches it next, then draw a finished figure or edit a live canvas. It does not build a live chart inside a product (that's `khe-ui`, a component with loading, empty and error states), write general SVG markup or animate it (that's `khe-svg`), decide whether the figure moves (that's `khe-ui`), read the project's contract (that's `khe-design-tokens`), or annotate a product shot (that's `stageshow`).

## The one idea

**A figure ships only when it says what a paragraph or a table cannot, and then every box, line and color in it carries something the layout does not already show.**

Five ways it fails:

- **Needless.** Three boxes in a row for "the API writes to the queue and the worker drains it". The sentence was the figure. This is the worst of the five, because a needless picture still costs layout, labels, a legend and a review.
- **Misplaced.** The right picture on the wrong surface: a finished figure handed to a team that will move boxes tomorrow, or a canvas screenshot pasted into a doc.
- **Crowded.** 14 services in one frame. Past 9 nodes or 12 connectors it is two figures, and shrinking the type does not make it one.
- **Tangled.** Diagonal or stacked connectors, labels sitting on their lines, a line running behind a box, two arrows landing on one point.
- **Flat.** Identical boxes for different kinds of thing, the accent on five of them, or the generated look: a dark ground with a glow, pills with shadows, mono everywhere, a legend floating among the nodes.

The fix is deletion first. A figure is done when nothing can be removed. A reply that is one sentence and no figure is a correct result.

## Initial response

When this skill is invoked with no request, reply only with:

> I'm ready to decide whether this needs a diagram, then draw the figure or edit the canvas. Usage: `/khe-diagram [what]`

Then wait. Give nothing else until the user asks.

## How hard to press

Draw it the way an editor draws the one figure a page is allowed. The files in `examples/` are the bar: when yours is the more crowded, the flatter or the more tangled one beside the closest gold, that is the first fix. Then look at the render the way the most exacting reader would, the one who circles a single thing and sends it back: a label touching its stroke, two arrowheads sharing a point, a third blue box, a legend that explains a line style nobody used. When you can picture that circle, you have found the next fix. The hardest press is on step 1: the reviewer's first act is to write the paragraph your figure replaces, and a figure that loses to it does not ship.

## Workflow

Most of the quality is decided before any markup. Every step ends in an exit you check before the next one starts. Under `khe-auto` the same loop runs with this skill's gate.

1. **Decide whether to draw.** Write the paragraph first. When someone could redraw the picture from it and lose nothing, the paragraph ships. When a three-column table carries the same meaning, the table ships ([diagram-decision](references/diagram-decision.md)). **Exit:** a yes with its reason (flow, containment, order in time, dependency or position on two axes), or a no with the sentence or table that replaces the figure. On a no, deliver it in the shape of `examples/no-diagram.md` and stop.
2. **Choose the surface by who touches it next.** Readers get a finished figure, a team that keeps editing gets a tldraw canvas, the code gets a Mermaid block, a team in Figma gets FigJam. When the request does not say, ask; with nobody to answer, draw a finished figure and record the assumption. **Exit:** one line naming the surface, its owner and the next person to touch it.
3. **Plan and count.** List the nodes, the connectors, the one or two elements that take the accent, and the callouts. Run the four deletion tests in [diagram-craft](references/diagram-craft.md) on the list. Count against 9, 12, 2 and 2, and split into an overview and a detail before drawing past them. **Exit:** the list with its counts, written before any markup.
4. **Read the skin.** Read [gotchas](references/gotchas.md) and [pov](references/pov.md), then the project's `.design` or DESIGN.md. Map the contract onto the nine color roles and the families ([diagram-design-reconciliation](references/diagram-design-reconciliation.md)). With no contract, the default skin is diagram-design's. **Exit:** nine roles and two families, each with its source.
5. **Start from the closest gold.** Pick it from the Examples table and copy the file. Keep its layer order, class names, type ramp, node treatments and marker definitions; replace the slug, the content and the skin. **Exit:** the gold is named, and the copy passes the gate before you change its structure.
6. **Build.** In file order: connectors, then labels on their masks, then nodes, then callouts, then the legend strip. Every node origin and size divides by 4. With diagram-design installed, it draws and this skill reviews. A canvas job follows [tldraw-canvas](references/tldraw-canvas.md) and skips to step 9. **Exit:** the figure renders, and its counts match the plan from step 3.
7. **Rehearse with the gate.** Run `node scripts/diagram-check.mjs <figure> --gate` and read every line. Fix the largest fault first, in this order: existence, budget, connectors, signal, type, polish. Run it again. **Exit:** the run ends `diagram check passed`, and every candidate line has a decision.
8. **Look at it.** Render the figure at the width it ships at, on the page it ships on, and again at 400% wherever connectors meet a node. Put it beside the gold. **Exit:** you can say the one difference between yours and the gold, and it is not "more crowded", "flatter" or "more tangled".
9. **Walk the checklist from evidence.** Answer every question in [verify](references/verify.md) from the render or, for a canvas, from a copy of the board. Any no sends you back to the step that owns it. **Exit:** every answer is yes, each from something you looked at.
10. **Fresh-eye review.** Hand a reviewer the evidence and the brief in [review](references/review.md), never your plan or reasons. **Exit:** a ranked list you have answered, or "nothing" with the list of what was looked at.
11. **Hand over.** Write `FIGURE.md` beside the figure from the template in [verify](references/verify.md), with the gate's last line pasted and what you did not check. **Exit:** the file exists and names its unresolved items.

Passing the gate is necessary, not sufficient. The gate reads markup: it cannot tell whether the figure should exist, and it cannot read a live canvas.

## Faults that come back every round

Check these before handing over. Each names its gate line where one exists, and its rule.

- **A figure a sentence carries** (`sentence-figure:`): [diagram-decision](references/diagram-decision.md), Picture, table, or sentence.
- **The accent on a third element** (`accent-spread:`): [diagram-craft](references/diagram-craft.md), Signal.
- **A label on its line, or with no mask** (`label-on-line:`): [diagram-craft](references/diagram-craft.md), connector rule 2.
- **A square or diagonal turn** (`sharp-elbow:`, `diagonal:`): [diagram-craft](references/diagram-craft.md), connector rule 1.
- **Two connectors on one attach point** (`shared-attach:`): [diagram-craft](references/diagram-craft.md), connector rule 4.
- **Connectors written after the nodes** (`edge-over-node:`): [diagram-craft](references/diagram-craft.md), connector rule 6.
- **A legend dropped, or left among the nodes** (`missing-legend:`, `floating-legend:`): [diagram-craft](references/diagram-craft.md), Grid, type, legend.
- **Mono on node names** (`mono-label:`): [diagram-craft](references/diagram-craft.md), Grid, type, legend.
- **diagram-design's palette in a branded project** (`shipped-palette:`): [diagram-design-reconciliation](references/diagram-design-reconciliation.md), Gotcha.
- **A canvas arrow placed by coordinates:** [tldraw-canvas](references/tldraw-canvas.md), Canvas rules.

## Hard rules

1. **Write the paragraph first.** When it carries the picture, ship the paragraph. When a three-column table carries it, ship the table.
2. **Who touches it next picks the surface.** A finished figure can only be changed by running the skill again, so ask when the request does not say.
3. **Hold the budget: 9 nodes, 12 connectors, 2 callouts, the accent on 2 elements at most.** Past that it is an overview and a detail. Count before drawing.
4. **Connectors are orthogonal and drawn before the boxes.** Right-angle elbows rounded at r=8, labels on an opaque paper mask 6 to 10px clear of the stroke, 14 characters at most.
5. **One accent, on one or two elements.** The rest of the hierarchy comes from treatment (fill, stroke, dash), never from size.
6. **On a canvas, bind every meaningful connection and lint before done.** Fix every lint your edit introduced, on the shape you edited.
7. **The brand reaches the color roles and the type families, nothing else.** Inside a diagram-design file its geometry, type ramp and motion clock stand, because its own scripts check them.
8. **Never clear a gate line by hiding what it points at.** Renaming a class so a node is not counted is a bug, and the reviewer judges every line called intentional again.

## Examples

Open the closest one before step 5. Each is a complete file on the 4px grid in the worked contract's skin.

| Need | Example | What to learn |
|---|---|---|
| Services, stores and an external system | `examples/architecture.svg` | Four node treatments at one size; the accent on the queue and the one connector into it; one masked label; a legend strip |
| Steps with a branch | `examples/flow.svg` | Every turn an elbow rounded at r=8; each connector its own attach point; labels beside vertical runs |
| Order in time, a request and its reply | `examples/sequence.svg` | A reply as its own dashed line from the recipient; time runs down the page, so no step needs a number |
| A request that should not be a figure | `examples/no-diagram.md` | The verdict and its reason first; the table is the whole deliverable; what would make it a figure |

`teaching/` holds 14 bad and good pairs, one fault each, indexed in [teaching](references/teaching.md). Use them to diagnose a fault; the bad halves are never starting points.

## Find the reference

Open a reference only when the job needs it. Never load the whole folder.

| Job or symptom | Open |
|---|---|
| "Can you diagram this?", picture or table or sentence, which surface, "it has too many boxes", when to split | [diagram-decision](references/diagram-decision.md) |
| Drawing or reviewing a figure, "it looks like Mermaid", "it looks AI-made", connectors, labels on lines, accents, node treatments, the legend, an accessible figure | [diagram-craft](references/diagram-craft.md) |
| A diagram-design figure in a project with a `.design`, a DESIGN.md or a `.diagram-design` marker; whose paper, fonts, accent, small type or motion clock wins | [diagram-design-reconciliation](references/diagram-design-reconciliation.md) |
| A board people keep editing, a `.tldraw` or `.tldr` file, "the arrows fall off when I drag", comments on a canvas, board scripts | [tldraw-canvas](references/tldraw-canvas.md) |
| The last pass, what a gate line means, "what do I do about this fault", the canvas questions, the handover template | [verify](references/verify.md) |
| Briefing a second reader, or reviewing a figure someone else drew | [review](references/review.md) |
| "Which pair shows my bug?", what each `teaching/` folder teaches | [teaching](references/teaching.md) |

## Never ship

Check the work against this table before finishing.

| Never | Instead |
|---|---|
| Three boxes in a row for one relationship | The sentence |
| 14 services in one figure | Two figures: an overview of five zones, then one path in detail at 8 nodes |
| A canvas screenshot in a doc | A redraw from the board's shapes and bindings |
| A diagonal connector | A right-angle elbow rounded at r=8 (r=6 in a tight layout) |
| A label sitting on its line | An opaque paper mask 6 to 10px clear of the stroke, 14 characters at most |
| Parallel routes sharing a stroke, or connectors meeting at one point on an edge | Routes offset by 12px or more; each connector its own attach point at `L·k/(N+1)`, at least 12px apart |
| A two-headed arrow for a request and its reply | A solid request and a dashed `5,4` return that starts at the recipient |
| The accent on five nodes | The accent on one or two; everything else ink, muted or soft |
| A pill or a soft 16px card with a shadow | Nodes at radius 6, type tags at 2, borders and no shadow |
| A legend floating among the nodes | A horizontal strip under the figure, the `viewBox` widened by about 60px |
| Mono as a blanket "dev" font | Names in a sans at 600; mono only for ports, commands, URLs and field types |
| A raw arrow placed by coordinates, or a `text` shape floating over a card | `helpers.createArrowBetweenShapes`, and the label in the card's `richText` |
| A figure handed over on a green gate alone | The render looked at, the checklist walked, the review answered, `FIGURE.md` written |

## Output

In this order:

1. **The verdict**, one line: sentence, table, figure or canvas, and the reason. When the verdict is a sentence or a table, that sentence or table is the whole deliverable.
2. **The surface and its owner**, one line, with who touches it next.
3. **The artifact.** A figure is one self-contained HTML file with inline SVG; PNG or SVG export only on request. A canvas job is the edit itself.
4. **The counts** for a figure: nodes, connectors and callouts against 9, 12 and 2, and the elements that carry the accent.
5. **The gate's last line**, pasted, and `FIGURE.md` beside the figure.
6. **For a canvas**, a reply that names each shape by what identifies it ("Moved 'Billing worker' into Review and bound its arrow to 'Queue'"), the lint result, and the thread resolved.

Leave out an export nobody asked for, the source's coordinates, colors and fonts on a redraw, and a description of the geometry in `<desc>`.

## Tone

Short and editorial. Say "this is a sentence, not a diagram" and give the sentence. Ask "who edits this next?" when the request does not say, and treat an ambiguous instruction on a shared board as a question, never as permission to pick one.

## Yours to edit

Read both before producing anything. They outrank the defaults in this skill, and a project's `.design` contract or DESIGN.md outranks them.

- [gotchas](references/gotchas.md): lived failures, one line each. Append one when something goes wrong.
- [pov](references/pov.md): your taste calls.

## Pairs with

- `khe-auto`: it runs this skill's loop and names this skill's gate at each step.
- `khe-svg`: it owns the general markup rules behind an accessible figure and the SVGO pass after an export.
- `khe-design-tokens`: it reads the `.design` contract whose color roles and families become the figure's skin.
- `khe-ui`: whether a figure animates at all is its decision; this skill keeps the figure's own clock only once it does.
- `khe-ui`: its one-accent rule is the one this skill applies to nodes and to named canvas colors.

Names without the `khe-` prefix are other people's skills, not part of this one: `stageshow` is Benji Taylor's ([benjitaylor/skills](https://github.com/benjitaylor/skills)); `animate`, `emil-design-eng` and the rest are Emil Kowalski's ([emilkowalski/skills](https://github.com/emilkowalski/skills)). Install them from their own repos.

Harshit Khemani. MIT.
