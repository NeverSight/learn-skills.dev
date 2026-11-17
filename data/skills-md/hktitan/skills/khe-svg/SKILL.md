---
name: khe-svg
description: "Creates, cleans and animates SVG files: icons, illustrations, logo reveals, stroke draw-ons, path morphs, mascots, and flat video clips turned into one editable vector file, each on the token system and moved by the engine its home allows. Use when someone asks to make or fix an SVG, says \"this icon won't recolor\", \"the export is 200 KB\", \"it rotates around the corner\", \"the morph jumps\", or wants a logo, icon or mascot to move. For page transitions, gestures and timing beyond the file use `khe-ui`; for choosing an icon pack for a product use `khe-ui`; for stickers and sticker packs use `khe-sticker`; for diagrams use `khe-diagram`."
license: MIT
metadata:
  author: Harshit Khemani
  version: "1.0.0"
---

# SVG

You own the file from the request to an SVG that ships: clean, on the project's tokens, and moving by the engine its home allows.

A construction skill that works on the file and nothing else. It does not time page transitions or gestures (`khe-ui`), choose or size an icon pack for a product (`khe-ui`), draw a diagram (`khe-diagram`), design, animate or pack a sticker (`khe-sticker`), place icons inside a faux product demo (`stageshow`), or add the sound to a reveal (`khe-sound`).

## The one idea

**An SVG is markup the next person has to live with: it scales, takes the theme's colour, names its parts, and moves only by an engine its home can run, for a cause.**

Five ways it fails:

- **Picture.** Treated as an image: fixed `width` and `height`, no `viewBox`, every colour a baked hex, a PNG inside. It will not scale or recolour.
- **Anonymous.** A hundred unnamed groups, no accessible name and no decision to hide it, ids and selectors that collide the moment it is inlined. Nobody can address a part.
- **Export.** The generator's file shipped as it came: editor namespaces, 8-decimal paths, empty groups, the same gradient four times, 200 KB.
- **Wrong engine.** Page CSS aimed at a file loaded as an `<img>`, a hover inside an image, SMIL with no still, a native morph between paths whose commands do not match.
- **Restless.** Motion with no cause: a line, its area and its dot fading in together, a loop on something seen all day, a morph where a rotation or a swap was the honest answer, no reduced-motion state.

The first three make a file nobody can use, and they are worse than the last two. A file that ends with no animation is a valid result.

## Initial response

When this skill is invoked with no request, reply only with:

> I'm ready to create, clean or animate an SVG and keep it editable. Usage: `/khe-svg [create | animate] [target]`

Then wait. Give nothing else until the user asks.

## How hard to press

The files in `examples/` are the bar. Open the closest one beside yours: if yours has the longer root tag, the looser coordinates, the unnamed group or the extra rule, that is the first fix. Then look at the render the way the most exacting reviewer would, the one who screenshots a single wrong thing and sends it back: an icon one weight heavier than its neighbours, an arm orbiting the corner, a dot that shows before the line reaches it, a grey icon on a dark surface, a morph that jumps on its third frame. If you can picture that screenshot, you have found the next fix.

## Workflow

Most of the quality is decided before any path is drawn. Each step ends in an exit you check before moving on. Under `khe-auto` the same loop runs with this skill's gate.

1. **Plan.** Write five lines: the job (`create` for a new or messy file, `animate` for a clean file that should move; the second word of the request picks it; a sticker of any kind goes to `khe-sticker`); the home (inline, or loaded as an `<img>`, a background, in email, on a social upload); whether it moves at all, by [animation-decision-framework](references/animation-decision-framework.md); the engine that home allows; the frame shown under reduced motion. Photoreal video, gradients and texture stay raster. A gap in an icon set is filled from the set, never drawn by hand ([icon-systems](references/icon-systems.md)). Seen 100 or more times a day, or triggered by the keyboard: no motion, say so, stop. **Exit:** the five lines exist, and every motion in them names its cause.
2. **Read the contract.** [gotchas](references/gotchas.md), [pov](references/pov.md), then the project's tokens, icon set and stroke weight, and how the project styles things. **Exit:** you can name the colours, the stroke weight and the set, and none of them is your own invention.
3. **Start from the closest gold.** Pick it from the Examples table, copy the file, keep its root attributes and its structure. **Exit:** your file opens with the gold's root contract, and what you changed is geometry and names.
4. **Build the file.** By [svg-creation](references/svg-creation.md): whole numbers on the grid, named groups in back-to-front order, `currentColor` or `var(--token, #fallback)`, `<defs>` and `<symbol>` for repeats, the accessibility choice made. A file with unnamed groups or no `viewBox` is rebuilt this way before anything moves. **Exit:** you can name every group aloud, and the file recolours when you change one variable.
5. **Add the motion, when the plan has any.** Pick the path by the source: frames or a flat clip go through [video-to-vector-pipeline](references/video-to-vector-pipeline.md) and `node scripts/svg-flipbook.mjs`; a shape that changes goes through [svg-path-morphing](references/svg-path-morphing.md); anything else through [svg-animation](references/svg-animation.md). Take every curve from [easing-curves](references/easing-curves.md) and every duration from [duration-table](references/duration-table.md). Write `data-home="img"` or `data-home="inline"` on the root of a moving `.svg`, and put the reduced-motion state inside the file. **Exit:** each moving part has a cause from the plan, a named group, one curve and one duration.
6. **Optimize.** Run SVGO with `viewBox`, the animated ids and `<title>` / `<desc>` kept, then diff the render. **Exit:** the optimized render is identical to the source, and the size is inside its budget.
7. **Rehearse with the gate.** Run `node scripts/svg-check.mjs <file> --gate` and repeat until it ends `svg check passed`. Every line it prints is a fault someone will meet. Fix the largest visible fault first: a file that cannot be used, then wrong motion, then a mismatch with its set, then size. Never clear a line by hiding the thing it points at. Passing is necessary, not sufficient. **Exit:** the last line reads `svg check passed`, and every candidate line is fixed or has its reason.
8. **Look at it.** Render the file at the size it ships, on the light and the dark surface, an icon beside two neighbours from its set. Step the motion at 40 to 80ms. Turn reduced motion on. Then walk [verify](references/verify.md) and answer each question from what you looked at, never from the markup you remember. **Exit:** every answer is yes, each with its evidence.
9. **Fresh eye.** Hand the file, the gate report, the evidence and the closest gold to a reviewer by [review](references/review.md). Never hand them your plan or your reasons. **Exit:** a ranked list you have answered, or "nothing" with what they looked at.
10. **Hand over.** Write `SVG.md` beside the file from the template in [verify](references/verify.md), with the gate's last line pasted and what you did not check. Then reply by Output below. **Exit:** `SVG.md` exists and its `Not checked:` line is filled.

## Faults that come back every round

Check each before handing over.

- **A rotation left on the default origin**, so the part orbits the canvas corner ([svg-animation](references/svg-animation.md), The techniques).
- **A native morph between paths whose commands differ**, including `S` against `C` and `l` against `L` ([svg-path-morphing](references/svg-path-morphing.md), Author to the rule).
- **A morph where a rotation or a swap was the answer**: the same shape turned rotates, unrelated icons swap ([svg-path-morphing](references/svg-path-morphing.md), Usually you don't want a morph).
- **A copied animated icon with its own keyframes and no reduced-motion query** ([svg-animation](references/svg-animation.md), Gotcha).
- **A SMIL bounce with a spline outside 0 to 1**, which the browser rejects ([gotchas](references/gotchas.md)).
- **A hex left behind after cleanup, or a duotone second layer** ([svg-creation](references/svg-creation.md), Color that follows the system).
- **Global selectors and repeated ids once the file is inlined** ([svg-creation](references/svg-creation.md), Gotcha).
- **SVGO stripping the `viewBox`, the animated ids or the `<title>`** ([svg-creation](references/svg-creation.md), Optimize, carefully).
- **A line, its area and its end dot arriving together** ([svg-animation](references/svg-animation.md), A draw-on carries order).
- **An icon drawn by hand beside a set, or two stroke weights in one row** ([icon-systems](references/icon-systems.md), Pick one icon pack).

## Hard rules

1. **`viewBox` always, no fixed `width` or `height` on the root.** The `viewBox` defines the coordinates and CSS sets the size.
2. **Colour comes from `currentColor` or `var(--token, #fallback)`.** The theme then reaches inside the file, and dark mode is a variable flip instead of a second file.
3. **Name the groups before anything moves.** A mascot with unnamed groups cannot be animated by anyone.
4. **Pick the engine by where the file lives.** Inline and state-driven: CSS transitions or WAAPI. Loaded as an `<img>`, a background, in email or on a social upload: keyframes inside the file, or SMIL. A library only for gestures, springs or timeline work, because a runtime is a cost the file carries on every load.
5. **Morph only between paths with the same number, order and type of commands.** Draw both shapes on one point budget, resample both to the same N points, or hand the mismatch to a resampling library. The same shape turned rotates. Unrelated icons swap.
6. **Reduced motion ships inside the file.** SMIL cannot read the query, so a SMIL file needs a static fallback asset.
7. **Hold the size budget.** About 2 KB for an icon, 10 to 30 KB for a hero mascot, 20 to 60 KB for a 24-frame flipbook.
8. **Write in the project's own system.** Read how the project styles things, its tokens and its motion library, and express every fix there. A correct value written in a second styling system is a defect.

## Examples

Open the closest one before you start (step 3). They are the bar, and every value in them comes from the references.

| Need | Example | What to learn |
| --- | --- | --- |
| One clean icon | `examples/icon-clean.svg` | The root carries the whole contract, so the path carries geometry only |
| A small icon set | `examples/icon-set.svg` | Every symbol repeats one grid, one stroke weight and one ink, so no icon drifts from its neighbours |
| A logo reveal, loaded as an image | `examples/logo-draw.svg` | The stroke draws and the dot arrives when the line reaches it; keyframes and the reduced-motion state live inside the file |
| A path morph, inline | `examples/icon-morph.html` | Three lines per icon so any state morphs to any other; the spare line parks at the centre at opacity 0; cross is plus rotated |

`teaching/` holds 14 bad and good pairs, indexed in [teaching](references/teaching.md), for diagnosing a fault. The bad halves are never starting points.

## Find the reference

Open a reference only when the job needs it. Never load the whole folder.

| Job or symptom | Open |
| --- | --- |
| Drawing or refactoring a file, "it won't recolor", "it won't scale", SVGO flags, `<title>` and `<desc>`, a generated export to clean | [svg-creation](references/svg-creation.md) |
| Which icon pack, icon size, stroke against font weight, "these icons don't match" | [icon-systems](references/icon-systems.md) |
| "Should this icon or logo move at all?" | [animation-decision-framework](references/animation-decision-framework.md) |
| Choosing the engine, stroke draw-on, "it rotates around the corner", motion along a path, reduced motion in a file, file size | [svg-animation](references/svg-animation.md) |
| Which curve, how long | [easing-curves](references/easing-curves.md), [duration-table](references/duration-table.md) |
| "The morph jumps", "works in Chrome, jumps in Safari", play to pause, a logo that changes shape | [svg-path-morphing](references/svg-path-morphing.md) |
| A flat clip or frame sequence that should become one editable animated SVG, a boiling outline | [video-to-vector-pipeline](references/video-to-vector-pipeline.md) |
| Reporting a refactor | [review-format](references/review-format.md) |
| The last pass, a gate line you do not recognise, what the gate cannot check, the `SVG.md` template | [verify](references/verify.md) |
| Briefing a fresh-eye reviewer | [review](references/review.md) |
| "My file has this fault, show me the fix" | [teaching](references/teaching.md) |

## Never ship

| Never | Instead |
| --- | --- |
| Fixed `width` and `height` with no `viewBox` | `viewBox="0 0 24 24"`, size from CSS |
| `fill="#6b7280"` plus a 40% duotone layer | `fill="currentColor"`, quieted with `opacity` on the `<svg>` |
| A base64 PNG inside the file | Paths, or leave the image raster |
| A rotation left on the default origin, orbiting the corner | `transform-box: fill-box; transform-origin: center`, or the hinge you mean |
| Animating `d`, `r`, `stroke-width` or filters across a scene | `transform` and `opacity`; `d` on one icon or one hero shape only |
| `transition: d 240ms` from a 7-vertex pointer to a circle | Both outlines resampled to the same point count from the same start and winding, or a swap |
| A morph between unrelated icons (play to pause, copy to check) | A swap: the outgoing icon scales to 0.3, fades and blurs 3px while the incoming does the reverse |
| Arrow-right bending into arrow-down | One shape, rotated 90 degrees |
| A chart line, its area and its end dot fading in together | The stroke draws; the dot appears on the frame the line reaches it |
| Keyframes in the file with no reduced-motion query | `@media (prefers-reduced-motion: reduce)` inside the file's `<style>` |
| A `<style>` block with global selectors, inlined into a page | Selectors scoped under a root id, and `prefixIds` when several SVGs share a page |
| 48 frames at 24 fps traced from 11 anti-aliased colours, 200 KB | 24 frames at 12 fps, 5 flat colours quantized before tracing, 20 to 60 KB |

## Output

`create` returns, in order: the file, its size before and after, and for a refactor a Before, After, Why table by [review-format](references/review-format.md).

`animate` returns, in order: the motion plan as one table (trigger, engine, groups, values, reduced motion, size), then the file. When the decision is no motion, the reply is that verdict in one line with the frequency or purpose that decided it, and no animation code.

Every reply ends with the gate's last line and one line naming what was not checked. Leave out what SVG elements and CSS properties are, a menu of engines, and any value not taken from the references.

## Tone

Make the call and give the reason in one line. Say "this should not animate" for a keyboard-triggered or all-day element, "this is a swap, not a morph" for unrelated icons, "this is a rotation, not a morph" for one shape turned, and "this clip stays raster" for gradients and texture. Report sizes as numbers.

## Yours to edit

Read both before producing anything. They outrank the defaults in this skill, and a project's `.design` contract or DESIGN.md outranks them.

- [gotchas](references/gotchas.md): lived failures, one line each. Append one when something goes wrong.
- [pov](references/pov.md): your taste calls.

## Scripts

Run with Node from this folder.

- `scripts/svg-check.mjs`: the gate. `--gate` for the verdict, `--report` for JSON, `--self-test` to prove it on `examples/` and `teaching/`.
- `scripts/svg-flipbook.mjs`: a folder of SVG frames into one stepped, self-contained animated SVG.

## Pairs with

- `khe-ui`: once the question leaves the file (a page transition, a gesture, an icon family built to morph), its values and its spring rules take over.
- `khe-sticker`: a sticker of any kind, its motion and its pack are its job; this skill keeps icons, logos and general SVG.
- `khe-sound`: a reveal that makes a sound is cued to the contact frame this skill produces.
- `khe-ui`: it owns which icon pack the product uses and at what size; this skill only draws to match it.
- `stageshow`: icons going into a faux product demo are placed by it.
- `pick-ui-library`: a resampling or timeline library is a dependency call, taken only when the morph or the choreography is the product.
- `khe-auto`: it runs this skill's loop, with this skill's gate, as one step of a larger job.

Names without the `khe-` prefix are other people's skills, not part of this one: `stageshow` is Benji Taylor's ([benjitaylor/skills](https://github.com/benjitaylor/skills)); `animate`, `emil-design-eng` and the rest are Emil Kowalski's ([emilkowalski/skills](https://github.com/emilkowalski/skills)). Install them from their own repos.

Harshit Khemani. MIT.
