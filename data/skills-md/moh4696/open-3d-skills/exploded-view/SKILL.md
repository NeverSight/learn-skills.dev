---
name: exploded-view
description: Builds interactive 3D explainers of how a machine or product works, in three.js, with a staged exploded view driven by a slider or scroll, x-ray shells, a section cut through the casing, labels pinned to parts with leader lines that never cover the model, and hover or click to pick parts. Works on code-built models and loaded GLB files. Use for "show how it works", teardown or cutaway pages, product anatomy, engine, motor, gearbox, camera, phone or vehicle internals, technical education pages, or turning a 2D cutaway drawing into an interactive 3D one.
---

# Exploded view

People understand a machine when they see it come apart in the order it was put together, with each part named where it sits. This skill does that in the browser: parts slide apart along sensible lines, outer shells go ghostly or get cut open, and labels follow their parts without ever sitting on top of the model.

## Tools

| File | What it does |
| --- | --- |
| `assets/explode.js` | `Exploder` (staged explode), `Labels` (pinned labels with leader lines), `Xray`, `Section` (clipping plane through shells), `Picker` (hover and click) |
| `assets/demo/` | A complete page: a code-built induction motor taken apart, with sliders, x-ray and section. `?explode=1`, `?cut=1`, `?xray=1` set the state |

Requires three.js (r169 in the demo's import map). Build the model with `threejs-scene` techniques or load a GLB.

## Build

### 1. Structure the model as parts

The unit of an exploded view is a part: a `Group` that moves as one. Make every part a direct child of one assembly group, and give each part **its own materials** (x-ray and hover change materials; shared ones would change every part at once).

For a GLB, regroup on load: walk the scene, and parent meshes into named part groups by their node names. Preserve world transforms when re-parenting (`group.attach(mesh)`).

### 2. Decide how each part moves

Per-part settings live on `userData`:

```js
housing.userData = { shell: true, stage: 0, explode: [0, 0.32, 0] };   // lifts off first
rotor.userData   = { stage: 2, explode: [0.42, 0, 0] };                // slides out along the shaft last
```

- `explode: [x, y, z]` is the offset at full explosion. Without it, the part moves away from the assembly centre (along `axis` if you pass one to `Exploder`), scaled by its distance.
- `stage` orders the motion: stage 0 moves first, and each later stage starts when the previous is half done. Take things apart the way a mechanic would: covers and shells, then fasteners and caps, then the inner parts.
- `shell: true` marks casings for x-ray and section cuts.

Lay out the exploded state like a technical illustration: one main axis (the shaft, the stack direction), parts spaced so each is clear of its neighbours, large shells moved off-axis (up) so the core stays visible.

```js
const ex = new Exploder(assembly);
ex.set(t);   // 0 assembled .. 1 exploded; ease toward a target each frame for slider input
```

### 3. Label the parts

```js
const labels = new Labels(document.querySelector(".labels"), camera, canvas);
labels.add(rotor, "Rotor", { note: "turns in the magnetic field", anchor: [0.03, 0.07, 0] });
// every frame, after renderer.render():
labels.update();
```

Labels sit in two columns at the screen edges, keep their anchors' vertical order and push apart when they would overlap; a leader line runs from each label to its anchor point. They follow the part as it explodes and hide when the part is hidden or behind the camera. Anchor each label on a point of the part that stays visible from the main view (the top edge, the end of a shaft), in the part's local coordinates.

Style `.label`, `.label b`, `.label span`, `.leader` and their `.focus` variants in CSS. On narrow phones, hide the labels and show the hovered or tapped part's name in one caption instead: two columns of labels do not fit beside a model on a 390 px screen.

### 4. X-ray and section

```js
const xray = new Xray(assembly);      xray.set(true);          // shells to 14% opacity, no depth write
renderer.localClippingEnabled = true;
const section = new Section(assembly, [0, 0, -1]);  section.set(0);   // cut the shells' front half away; null = off
```

The section plane cuts only shells, so the interior stays whole inside an opened casing, the way a cutaway drawing shows it. Cut materials are made double-sided so the inside of the casing reads.

### 5. Picking

```js
new Picker(canvas, camera, assembly.children, {
  onHover: (part) => highlightLabelOf(part),
  onPick: (part) => focusOn(part),
});
```

Hover tints the part's emissive slightly and switches the pointer cursor. A click can isolate the part, fly the camera to it, or open its description.

## Camera and framing

- Fit the camera to the assembly for the current screen shape, and let the distance follow the explode amount (the demo's `autoDistance`): close when assembled, pulled back when exploded. Stop doing it once the visitor zooms or orbits.
- Raise `OrbitControls.maxDistance` above the fitted distance, or the controls silently clamp it and phones see a crop.
- A three-quarter view slightly from above (the demo uses direction 0.42, 0.34, 1) shows ends and sides of a cylindrical machine at once.

## Driving it from scroll

Map scroll progress to `ex.set()` through keys with holds, as `scroll-film` does for frames: assembled while the intro reads, explode stage by stage with a caption per stage, hold fully exploded, then section cut. The model is real-time, so the visitor can stop and orbit at any point.

## Rendering

Product-shot lighting suits explainers better than a sky: a `RoomEnvironment` PMREM for reflections, one soft key light with shadows onto a `ShadowMaterial` floor, ACES tone mapping, and the page's own background colour as the clear colour (an opaque canvas defaults to black). Metals read through roughness 0.3 to 0.45 and metalness 0.8 to 0.95; painted parts through a clearcoat.

## Accuracy

If the subject is a real product, use real part names and the real assembly order, and say in the page copy which internal details are illustrative. An explainer that is wrong teaches the wrong thing confidently.
