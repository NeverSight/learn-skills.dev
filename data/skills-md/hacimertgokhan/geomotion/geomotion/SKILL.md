---
name: geomotion
description: Create hand-drawn, morphing line animations (boiling ink, riso-style fills) from simple shapes and export them as animated SVG, Lottie JSON, HTML or shareable links. Use when the user wants an animated icon, loader, illustration, explainer motion, logo sting, empty-state or success animation, "hand-drawn" / "sketchy" / "doodle" animation, or asks for geomotion.
---

# geomotion

geomotion turns a JSON **spec** — a list of keyframes, each a list of shapes — into a hand-drawn
animation. Shapes with the same `id` morph into each other between keyframes; lines keep
"boiling" (re-inked ~12×/s) so the result feels traced by hand.

Site & studio: https://hacimertgokhan.github.io/geomotion · Repo: https://github.com/hacimertgokhan/geomotion

## Workflow

1. **Pick a route** (use the first that is available):
   - **MCP tools** (`geomotion_guide`, `geomotion_get_preset`, `geomotion_render`, `geomotion_share_link`): call `geomotion_guide` once, then render.
   - **CLI** (Node 18+ with network): `npx -y github:hacimertgokhan/geomotion render spec.json --both --formats svg,lottie,html`
   - **No tooling**: write the spec, then run `python scripts/link.py spec.json` (in this skill folder) to get a player/studio link the user can open, edit and export from.
2. **Start from a preset when one is close** (see catalog below) and adapt ids, positions, colours.
3. **Write the spec** following the rules below. Validate (MCP `geomotion_validate` or `geomotion check spec.json`).
4. **Deliver**: file paths and/or the player link. Mention the studio link so they can tweak it. Offer a transparent version (`transparent: true` or `"both"`) when the animation will sit on a website.

## Spec essentials

```json
{
  "name": "idea",
  "size": [1200, 1200],
  "fps": 24, "boil": 12, "loop": true,
  "background": "ivory",
  "hold": 0.7, "duration": 0.9, "ease": "inOutCubic",
  "style": { "width": 24, "wobble": 1, "misregister": [-14, 10] },
  "keyframes": [
    { "shapes": [ { "id": "bulb", "type": "circle", "cx": 600, "cy": 520, "r": 220, "fill": "oat" } ] },
    { "hold": 1.2, "shapes": [
      { "id": "bulb", "type": "circle", "cx": 600, "cy": 520, "r": 240, "fill": "sun" },
      { "id": "ray", "type": "line", "from": [600, 200], "to": [600, 110], "enter": "draw", "delay": 0.3 }
    ] }
  ]
}
```

- Keyframe: `hold` (seconds shown), `duration` (morph to the next keyframe), `ease`.
- Shape types: `circle {cx,cy,r}`, `ellipse {cx,cy,rx,ry}`, `rect {x,y,w,h,radius?}` or `{cx,cy,w,h}`,
  `line {from,to}`, `polyline {points,closed?}`, `polygon {points}`, `regular {cx,cy,r,sides}`,
  `triangle {cx,cy,r}`, `star {cx,cy,r,inner?,points?}`, `heart {cx,cy,size}`, `blob {cx,cy,r,seed?}`,
  `crescent {cx,cy,r,thickness?,angle?}`, `wave {from,to,amplitude?,waves?,phase?}`, `spiral {cx,cy,r,turns?}`,
  `arc {cx,cy,r,start,end}` (degrees, 0 = right, clockwise), `path {d}` (any SVG path).
- Shape options: `id` (match across keyframes — always set it), `fill`, `stroke` (colour or `false`),
  `width`, `opacity`, `enter`/`exit` (`grow` | `pop` | `draw` | `fade` | `cut`), `delay` (0–0.95, stagger),
  `ease`, `transform {translate, rotate, scale, origin}`, `misregister: false` for tiny solid dots.
- Palette names: ink, slate, ivory, paper, oat, kraft, clay, coral, fig, sky, cactus, olive, heather, sun, white (or any hex).
- Easings: linear, in/out/inOut Quad·Cubic·Sine, inOutQuart, outExpo, inOutExpo, outBack, inOutBack, outElastic, outBounce.

## Design rules that make it look good

1. 1200×1200 canvas, ~120 px margin, 2–5 bold shapes per pose. Small details read badly.
2. Ink for every outline, **one or two accent fills** per pose (oat, clay, sun, sky, cactus, coral).
3. Tell a story through ids: the same element transforms (sun → moon, envelope → paper plane, dot → heart).
4. Stagger with `delay` 0 / 0.15 / 0.3; use `"enter": "draw"` for lines that should feel written, `"pop"` for playful arrivals.
5. Holds 0.5–1.2 s, morphs 0.5–1.2 s. `inOutCubic` = calm, `inOutBack`/`outBack` = playful, `outElastic` = jelly.
6. Rotations > 30° between two keyframes make lines cut corners — split big rotations into several keyframes (see the `spinner`, `gears`, `orbit` presets).
7. Solid dots (eyes, typing dots): `"stroke": false, "fill": "ink", "misregister": false`.

## Preset catalog (start points)

- **interface**: loader, spinner, success, error, toggle, bell, search
- **nature**: sunrise, sprout, rain, night, sea
- **communication**: chat, send, like, connect
- **ideas**: idea, growth, target, gears, house
- **characters**: smile, ghost, sparkle
- **abstract**: drift, orbit, kaleido, pebbles
- **motion**: bounce, pendulum, jelly

Any preset opens directly: `https://hacimertgokhan.github.io/geomotion/play/#preset=<name>`
(add `&bg=0` for a transparent background) or in the studio: `/studio/#preset=<name>`.

## Embedding on a website

```html
<script type="module" src="https://hacimertgokhan.github.io/geomotion/src/embed.js"></script>
<geo-motion preset="success" transparent style="width:160px"></geo-motion>
<geo-motion code="z…"></geo-motion>   <!-- the #s=… part of a share link -->
```
