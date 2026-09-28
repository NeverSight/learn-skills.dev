---
name: svg-mascot-creator
description: Create a flat-illustration SVG mascot character with a consistent multi-pose set (neutral, waving, pointing, walking, celebrating, etc.) for websites, portfolios, apps, docs, or brands. Use this skill whenever the user asks for a mascot, character, avatar, brand buddy, site guide character, illustrated persona, or a set of character poses/stickers — even if they don't say "SVG" or "mascot" explicitly (e.g. "add a little guy to my landing page", "I want a character that waves on my hero section", "make poses of my character"). Also use it when extending an existing mascot with new poses or expressions.
---

# SVG Mascot Creator

Build hand-crafted, flat-illustration SVG mascots using a **fixed rig + swappable limbs** system. The result is a set of pose files (each ~5 KB, zero dependencies, no gradients or filters) that are pixel-consistent with each other — because every pose reuses the exact same head, torso, and layer order, and only the arms, legs, expression, and accent effects change.

This is NOT image generation and NOT generic clip-art. Every shape is authored as explicit SVG geometry so poses can be diffed, edited line-by-line, and animated later.

## Canonical example

`references/example-poses/` contains a complete 6-pose reference character (a developer with hoodie, glasses, ID badge, and laptop). Before building any mascot, read at least `01-neutral.svg` and one action pose (e.g. `02-waving.svg`) to internalize the construction style. Read `references/rig-anatomy.md` for the full layer-by-layer breakdown, coordinate map, and pose recipes.

## Workflow

### 1. Gather character identity

Get (or infer from context) before drawing:
- **Who is the mascot?** Person, animal, robot, object-with-a-face? Occupation/personality?
- **Brand palette** — 1 accent color minimum. If the user has a site, match its colors.
- **Signature props** — laptop, coffee cup, headphones, tool, hat… one or two max. Props are what make a mascot memorable.
- **Pose list** — default to the core six: neutral, waving, pointing, arms-crossed, walking, celebrating. Ask only if the use case suggests others (e.g. "thinking" for a docs assistant, "error/confused" for a 404 page).

If the user gives minimal direction, make confident choices and show a neutral pose first for approval before generating the full set. Iterating on ONE pose is cheap; regenerating six is not.

### 2. Design the rig (neutral pose first)

Follow these non-negotiable construction rules — they are what make the pose set consistent:

- **Canvas**: `viewBox="0 0 360 620"` for a standing humanoid, character centered on x=180, feet at y≈570, ground shadow ellipse at y≈574. (Non-humanoids may adapt proportions but keep one fixed canvas for all poses.)
- **Flat color only**: solid fills, no gradients, no filters, no `<defs>`. Depth comes from exactly two tricks: (a) one darker shade shape overlaid at ~0.55 opacity on the body's right side, (b) a semi-transparent black ground shadow ellipse (opacity 0.25).
- **Limbs are double-stroked polylines**: draw each arm/leg as a 2–3 point path TWICE — first with the outline color at a wider stroke (e.g. 29), then the fill color on top at a narrower stroke (e.g. 24), both with `stroke-linecap="round" stroke-linejoin="round"`. This produces an outlined tube limb with zero path complexity. End arms with a plain circle in skin/paw color (r ≈ 10.5) as the hand.
- **Fixed anchor points**: shoulders, hips, and neck coordinates are constants shared by every pose (in the reference: left shoulder ≈ (146,192), right shoulder ≈ (218,194), hips at the y=338 hip block). Arms and legs may only pivot from these anchors.
- **Strict layer order** (back → front): shadow → hips → legs → shoes → torso → torso shade → hem → collar → drawstrings/props on chest → far arm → held prop (if any) → near arm → neck → ears → face → hair → facial features → glasses/accessories last. Keep this order identical in every file.
- **Palette discipline**: define 10–18 named colors up front (skin, skin-dark, outfit, outfit-shade, sleeve, sleeve-outline, accent, ink, etc.) and reuse them verbatim across all poses. The accent color should appear in at least 3 places (e.g. drawstrings, badge stripe, spark FX).
- **Animation-ready grouping** (do it now, it costs nothing): wrap the animatable parts in `id`'d `<g>` groups — `#mascot` (the whole body), `#arm-near`, `#arm-far`, `#head`, `#eyes`, `#fx` — and keep the ground `#shadow` *outside* `#mascot`. A `<g>` with no transform renders identically, so this never changes a static pose, but it's exactly what lets the mascot be animated later without redrawing anything. Full recipes: `references/animation.md`.

### 3. Derive the other poses by minimal diff

A new pose is the neutral file with ONLY these edits allowed:
- **Arm paths** (both strokes + hand circle position) — this alone produces waving, pointing, arms-crossed.
- **Leg paths + shoe transforms + shadow width** — only for locomotion poses (walking, running, jumping).
- **Expression swap** — e.g. closed smile ↔ open laughing mouth. Keep eyes/glasses fixed unless the pose demands it (winking).
- **Accent FX** — small strokes/dots in the accent color: motion arcs beside a waving hand, spark lines above a celebrating fist, a sweat drop, "!?" marks. 2–4 elements max, opacity-varied.
- **Prop repositioning** — a held prop moves with its hand or is omitted (e.g. laptop absent in pointing pose).

Everything else must be byte-identical to neutral. After writing each pose, verify by diffing against neutral — if the head or torso paths changed, that's a bug.

Pose recipes (arm path shapes, FX patterns, walking leg geometry) are in `references/rig-anatomy.md`.

### 4. Validate

- Render every pose to PNG and view them side-by-side (e.g. with `rsvg-convert` or `cairosvg`, montage with PIL/ImageMagick). Actually LOOK at the render — check hands connect to sleeves, limbs don't detach from shoulders, FX don't collide with the head, and the silhouette reads clearly at 80 px tall.
- Confirm each file is a single valid `<svg>` root, ~4–7 KB, no external references.
- Check cross-pose consistency: `diff` each pose against neutral and confirm only intended lines changed.

### 5. Deliver

- Name files `NN-posename.svg` (01-neutral, 02-waving, …).
- Present all pose files plus a preview sheet (single PNG/HTML grid of all poses) so the user judges the set at a glance.
- If the user asked for web integration, offer inline-SVG usage tips: the mascot inherits `currentColor` nowhere (all colors are literal), so recoloring for dark mode means a find-replace on hex values.

### 6. Animate (optional, when the user wants motion)

Because the rig has fixed anchors and the pose is already split into `id`'d groups, the mascot animates **without touching a single path** — you rotate/translate wrapper groups around their anchor. Never animate path `d` values.

- **Idle loop** (most common ask): a slow whole-body bob on `#mascot`, a periodic blink on `#eyes`, and maybe a gentle head tilt or arm sway. This is the "it feels alive" default for a hero-section mascot.
- **Wave / celebrate**: deliver the raised-arm pose (`02-waving`, `06-celebrating`) and oscillate `#arm-near`/`#fx` a few degrees around the shoulder anchor.
- **Walk in place**: rotate `#leg-front`/`#leg-back` around their hip anchors with a two-beat body bob.
- **Pose-to-pose** (e.g. neutral → waving on hover): stack two pose files and cross-fade opacity — never tween one path into another. The shared rig means only the arm appears to move.

Default to **CSS in a `<style>` block inside the SVG** (self-contained, respects `prefers-reduced-motion`); use SMIL only when the target must animate as a bare `<img>` that strips `<style>`. Set each rotating group's pivot with `transform-box: view-box; transform-origin: <anchor-x>px <anchor-y>px`. Keep amplitudes subtle (bob ≤ 6px, idle sway ≤ 4°, head tilt ≤ 3°) and always add a `prefers-reduced-motion: reduce` block that stops all animation.

`references/animation.md` has the full recipe library (bob, breathe, blink, wave, sway, head tilt, walk cycle, FX pulse, pose transitions, the SMIL equivalent, and a validation checklist). `references/example-poses/01-neutral-animated.svg` is a complete working idle-loop reference (bob + blink + head tilt + arm sway) built from the neutral pose — read it to see the grouping and `<style>` block in context.

## Extending an existing mascot

If the user uploads previous pose files: treat their neutral pose as the rig source of truth. Extract its palette and anchor coordinates first, then generate new poses by the minimal-diff rule above. Never redraw the head or torso "slightly better" — consistency beats improvement.

## Style guardrails

- No copyrighted characters or lookalikes (no Mario, Pikachu, Disney-style knockoffs). Original characters only.
- Keep proportions friendly: oversized head (~25–30% of height), simple dot eyes or ring glasses, small rounded hands. Avoid realistic anatomy — it breaks at small sizes.
- Resist adding detail. The reference character reads perfectly with ~60 elements per pose. If a pose exceeds ~90 elements, simplify.
