---
name: anatomy-asset
description: Make crafted, highly detailed isometric SVG assets for landing pages, product sites, launch posts, social cards and decks — a hero object, a set of spot illustrations, a feature-tile scene — drawn as real, well-made physical things with many small precise solid parts, four-tone shading, correct painter's order and calm CSS-only ambient motion, mostly monochrome with brand accents. Use this when someone wants a nice-looking illustration, hero image, product visual, spot illustration, icon set, isometric artwork, "Linear-style" or "premium" drawing, or a visual for a section of a site, where the goal is a striking, on-brand picture rather than a diagram that explains how something works. Ships a standalone .svg that works as <img>, inline or in design tools, plus a preview page; can add WebGL shaders or the 3D mode when asked. For interactive figures that explain a technical concept with a live readout, use the anatomy skill instead.
license: MIT
compatibility: Written for Claude Code; also runs in Antigravity, OpenCode and Codex. Needs Node.js 20.10+, and Chrome or Chromium for the checks.
metadata:
  opencode/slash: "true"
  forked-from: "https://github.com/wheresryan22/anatomy"
---

# Anatomy Asset

A fork of Anatomy for assets instead of explainers. The drawing is the same: a real object you could build, made of many small, precise, solid parts, shaded in four tones, painted back to front, every line ending on something. What changes is the job. An Anatomy figure has to *explain*; an asset has to *look right on the page*: carry the brand, hold a composition, leave room for a headline, and reward a second look.

So the rules split in two:

- **Craft is fixed.** Solids, not wireframes. The kit shades. Small precise detail, never noise. Every line ends on something. No part passes through another. Painter's order is true. Curved surfaces shade smoothly. Every creation is highly detailed at 1× and still rewarding at 4×. These come from Anatomy unchanged, with the same checks.
- **Style follows the user.** Subject, mood, colour, composition, how literal or playful the object is, whether there's text: these are the user's calls. Where the user asks for something Anatomy forbids (two accents, a word on a sign, a floating part, a pastel ground), do it, and do it with the same craft.

Thirteen examples ship with this fork, and eight from Anatomy are kept as references for craft. Open the closest one before you start.

- `examples/synth-hero/` is the asset reference: a compact synthesiser as a 1200 × 640 landing-page hero, art in the right 56%, headline space on the left. Two knobs in the brand colour, black keys in a dark neutral, one knob cap lifted off its shaft as a product-shot moment, LEDs that blink and a fader that drifts in CSS only. About 95 solids and 880 paths, 240 KB. `node build.mjs` (dark) and `node build.mjs --light` write `synth-hero.svg` and a preview page.
- `examples/writing-desk/` is a hero in a craft mood: an oak desk with a pigeonhole hutch, brass, wood, leather and ebony as material ramps, and the green pen floating over its socket. About 157 solids. It shows rule lines passed as a card's `inner`, so their caps don't notch its outline.
- `examples/espresso-tile/` is a 640 × 480 feature tile with a playful subject built strictly: a red espresso machine and a small robot barista with jointed arms. About 113 solids. It has vertical-face helpers and a custom "mostly on" blink through `assetSvg`'s `css`.
- `examples/feature-spots/` is a set of three 320 × 320 spots (stopwatch, safe-deposit box, battery lantern) from one script: one camera, one scale, one part vocabulary, weight 0.5, each under 70 KB thanks to a path-minifying post-pass.
- `examples/bottling-line/` is a 1600 × 560 banner: a bottling line run diagonally at azimuth 62°, bottles as a glass-grey material ramp, violet caps, and one bottle sliding a pitch along the belt. About 190 solids, under 400 KB.
- `examples/aero-*` and `examples/energy-*` are two complete brand sets, each a hero, a banner, a feature tile and three spots for one landing page: Aether (electric aviation, dark, ice blue) and Halden (clean energy, light, green). They show one brand carried across placements, aircraft built on the lathe with the audit, light composite material ramps that keep a hull bright on a dark page, tilted solar panels with `G.prismOf`, and diorama ground slabs.
- From Anatomy, for craft: `dial-indicator/` (smallest, about 300 lines), `test-rig/` (the quality bar for the drawing), `desk-computer/` (screens drawn on faces), `arcade-cabinet/` (cutaways and camera placement), `raptor-engine/` (round parts, pipes, harnesses and the audit), `spot-plate/` (shapes that morph), `ripple-tank/` (WebGL water and light), `turning-dial/` (the 3D mode). Read them for how parts are built, not for how they are framed: their card, readout and legend belong to explainers.

## The one idea that matters

**The object carries the message.** Don't draw a logo on a slab, a stack of floating cards, or a screenshot in an isometric frame. Find a real, beautifully made thing that *is* the product's promise, and build it so well people want to look at it.

| Brief | Object |
|---|---|
| A music-making app, "make sound in seconds" | A compact synth with brand-coloured knobs, one cap lifted off its shaft |
| An email tool that sorts your inbox | A brass-and-oak letter sorting cabinet, pigeonholes filling, one envelope mid-flight |
| A database that never loses data | A bank-vault door ajar, its bolt work and dial visible, a soft light inside |
| A payments API | A cash register crossed with a telegraph key, receipt tape curling out |
| A calm focus timer | A kitchen timer, a candle and a tea tin on a small walnut tray |
| A dev platform's "ship faster" | A model rocket on a launch rail on a workbench, toolbox open beside it |

The object can be literal (the product as a machine), a metaphor (what the product feels like), or a small scene (a diorama around the object). It can be playful or impossible — a lighthouse on a teacup, a server rack that is also a bookshelf — as long as every part is built as if it were real. Exaggerate proportions, but never the craft.

Ways this fails:

- **Too abstract.** Floating slabs, cubes and cards don't read as anything, and they don't sell anything either.
- **Too flat and bland.** One big shape with a few lines has no volume and nothing to discover.
- **Too busy.** Detail everywhere at the same weight, so nothing leads. One subject, one or two accents, calm around them.
- **Off-brand.** A good drawing in the wrong mood: a chrome industrial machine for a cosy journaling app.

`references/concepts.md` has the ideation method and more mappings.

**Every creation is highly detailed.** However small the asset — a 160 px spot illustration included — it is a dense, real object, never a few slabs. What scales with the size (workflow step 1) is how far you push the 4× sweep.
- **Read the real thing.** Build it the way the real object is built: every screw, seam, bevel, hinge, foot, knurl, label plate and cable.
- **Two looks.** At 1× it reads as one striking object. At 4× every region still has something true to find.
- **Purposeful, never noise.** Detail comes from parts that belong to the object. Each one sits on another part, ends on an edge, and fades rather than stops.

## Workflow

Work in this order. Write the brief, the concepts and the parts list before any geometry.

1. **Size it.** Name the size before any other work.
   - **Spot**: one small object, 25–50 parts, square or near-square, for a feature list, an empty state or an icon set. Build it without asking.
   - **Asset**: one hero object, 50–120 parts, with a composition and optional ambient motion. Build it without asking; a long one, say so.
   - **Scene**: a diorama, a whole set of spots that must match, or anything with WebGL or the 3D mode, 120+ parts. Give an estimate, propose an Asset version that keeps the core, and build the Scene only when the user chooses it.
   - Have a working preview page within the first hour, and deepen it from there.
2. **Brief first.** Pin down, from the request or by asking only what you can't infer: what the product or page is, the one feeling or promise the asset carries, the page colour it sits on, the brand colour(s), the placement (hero right, hero centre, feature tile, spot, banner, OG card, deck slide) and the delivery size. If the user gave none of this and it's a quick request, choose sensible defaults and say what you chose.
3. **Concepts.** Write three to five object ideas in one line each (literal, metaphor, scene), say which you'd pick and why, and go with the user's choice or your pick. Then say in one sentence what the object is and where the eye lands. Never copy a reference image: take its finish, not its object.
4. **Parts list.** Write the parts, grouped: base (plate, feet, tray, cloth), structure (case, frame, cheeks, posts), mechanism (what makes it this object), controls (knobs, keys, latches) and the subject — the one part that carries the accent or the moment. At least 25 for a Spot, 50 for an Asset. `references/craft.md` has a vocabulary of parts with recipes.
5. **Compose.** Choose the canvas and where the art lives in it (`references/composition.md`): a region for the art, a safe zone for headline text, and a camera. Fit with `fitInto(points, region, { pad, azimuth })` from `kit/asset.mjs`. Turn the azimuth until the most interesting face points at the viewer (the synth uses 60° to show the long front with its keys).
6. **Build geometry once.** With the kit, exactly as Anatomy does: `slabOf`, `cylinder`, `extrude`, `planOutline`, `topTicks`, `knurl`, `coil`, `radialTicks`; round parts on any axis from `kit/lathe.mjs`, pipes and cables from `kit/tube.mjs`.
7. **Paint back to front, bottom to top.** Sort repeated parts with `depthOf`. Split anything that wraps another part. Once an asset has pipes, cables and round parts, record shapes with `A.recorder`, settle the keys with `A.settle`, and end with `A.auditOrExit` (Anatomy's step 7, unchanged).
8. **Colour it.** Mostly monochrome, grounded in the page colour, with brand accents as scoped token sets (`references/brand.md`): `assetSvg({ paper, accents: { brand: "#ff5a1f" } })` and `<g class="ac-brand">` around the parts that carry it. One accent family by default; more when the user asks.
9. **Bring it to life.** Every asset moves, CSS only, so it runs inside `<img>`; the signature motion is the object working (rotors spin with `amRotor`, a conveyor runs with `amLoop`, a needle swings with `amSwing`, keys play with `amPress`, ink writes with `amDraw`, and `amFlip` for anything else), plus small echoes: a part that floats (`amFloat`), drifts (`amSlide`), breathes (`amPulse`), blinks (`amBlink`) or spins in its own plane (`amSpin`: rotors, propellers, fans, turbine blades, which should always turn). Two or three moving things at most, slow, out of phase, nothing that changes the painter's order, and still under reduced motion. Interactive behaviour (pointer, scroll, keyboard) is for when the user asks; then follow Anatomy's `references/motion.md`.
10. **Ship it.** `assetSvg` writes the standalone `.svg`; `previewHtml` writes a page that shows it on its page colour with the safe zone checked. `references/export.md` has the formats: SVG, PNG at 2×, inline in React, a set.
11. **Verify like a critic.** The checks are Anatomy's, run on the preview page:
    - `xmllint --noout asset.svg` must be silent: an SVG that isn't valid XML renders blank in `<img>`.
    - `node scripts/capture.mjs asset.html --out shots/asset.png` in each theme you ship, and at 390 px wide when it will be shown on phones. The console must be clean: the preview logs an error when the art enters the safe zone (open it with `?safe` to see the zone).
    - `node scripts/lines.mjs asset.html --out shots/lines.png` must print `line ends: 0`.
    - With pipes, cables or round parts, `node build.mjs --audit` must end `audit passed`.
    - 4× close-ups (`--zoom`) of every junction and every accent part, in each theme.
    - With motion, shots at several `--times` and one with `--reduced`.
    - Put your PNG next to the synth and ask: is it instantly a real, well-made object? Does the eye land where you meant? Does it sit on the page — colour, mood, space for the headline? Is it rewarding at 4×? Iterate until yes. Checklist: `references/verify.md`, plus the asset checks in `references/export.md`.

## Setup

The kit is Anatomy's (`kit/`), plus one module:

| File | Use it for |
|---|---|
| `kit/asset.mjs` | The asset layer. `assetSvg` (the standalone drop: styles inlined and scoped, ground tokens for the page colour, accents, ambient motion, valid XML), `previewHtml` (the page the checks run on, with a safe-zone check), `fitInto` (fit into one region of a wide canvas), `groundTokens` and `accentTokens`/`accentCss` (the palette), `amFloat`, `amSlide`, `amPulse`, `amBlink`, `amSpin` with `planeMatrix`, `topPlane` and `bladesPath` (CSS-only motion). |
| `kit/iso-kit.mjs`, `kit/iso-kit.ts`, `kit/iso.css` | The core: camera, solids, parts library, SVG strings, `ISO_CSS`. |
| `kit/lathe.mjs`, `kit/tube.mjs`, `kit/audit.mjs` | Round parts, pipes and cables, and the audit that proves them. |
| `kit/gl.mjs`, `kit/turn*.mjs`, `kit/react/` | WebGL layers, the 3D mode and React components, when an asset needs them. |
| `scripts/capture.mjs`, `scripts/drive.mjs`, `scripts/lines.mjs` | Screenshots, scripted sequences and the line-end check. They find the preview page's stage on their own. |

A build script looks like `examples/synth-hero/build.mjs`: import `kit/iso-kit.mjs` and `kit/asset.mjs`, assemble strings with `solidSvg`, `lineSvg`, `dotsSvg`, wrap them with `assetSvg`, and write the `.svg` and `previewHtml(...)`. For a React or Next.js site, ship the `.svg` (as `<img>` or `next/image` with `unoptimized`) unless the user wants interaction; then follow Anatomy's `references/react.md`.

## Craft rules (short form)

Anatomy's rules, with what an asset changes. `references/craft.md` gives the full reasoning and recipes; where it talks about cards, readouts and legends, those are explainer-only.

- **Solids, not wireframes.** Every part is filled with the page colour and painted in order. No see-through edges, no dashed hidden lines.
- **Let the kit shade.** `extrude` returns four side tones and a lighter top. Use `flat` only for inlays thinner than 1 unit.
- **Tone hierarchy.** Base and feet `lo`, structure `mid`, the subject `hi`, one `lit` part. Accents don't replace the hierarchy: an accent part still has tones, shades and lines, all from its own ramp.
- **Colour is a choice, not noise.** Grey by default, the brand accent on the subject and one or two echoes of it. Every colour is a token (`references/brand.md`), never a hex typed into a fill. More colours when the user asks: then each is its own ramp, and they share one lightness.
- **Small precise detail, never noise.** Bevels 0.4–1.6, grooves inset 3–5 from an edge, screws as 0.4–0.55 dots with a ring, knurls on knobs, ticks rooted on a strip or a scale arc.
- **Lines resolve.** Every line ends on something: a face, another line or a dot. A pointer starts on a hub dot; a knurl ends on a seam.
- **No pipe or cable passes through anything,** and every crossing is in true depth order, proved by the audit.
- **Curved surfaces shade smoothly,** never in a staircase. A texture ends on a real edge or fades.
- **Text is the user's call.** Default to none in the drawing — the page has the headline. When the user wants a word on the object (a brand name on a plate, a number on a display), it is part of the object: in the face plane, fitted and clipped to its window (`craft.md`, section 10).
- **Volume.** Real thickness, things standing on things, a soft halo under the base and under anything lifted.
- **Composition.** The art fills its region, not the canvas; it stays out of the safe zone; it reads at the size it will be shown (`references/composition.md`).
- **Line weight scales with the canvas.** 0.6 px suits a 600-wide figure; a 1200-wide hero wants `weight: 0.8`–`1`, a 160 px spot `0.5`.

## WebGL and 3D

They work exactly as in Anatomy and cost the same, so they make an asset a Scene. Use a shader only for what lines can't draw (fire, water, lamp light, glow, steam), keep the light theme designed for paper, and note that a shader needs a page with script: it can't ship as a plain `.svg`. Read `references/webgl.md` and `references/3d.md` first.

## References

Read these as you need them:

- `references/concepts.md`: from a brief to an object — the ideation method, literal vs metaphor vs scene, mood and finish, and more mappings.
- `references/composition.md`: canvases and placements (hero right or centre, feature tile, spot, banner, OG card, slide), safe zones, cameras for heroes, sets that match, line weight and phone sizes.
- `references/brand.md`: the palette — grounding the greys in any page colour, accent ramps (`body` and `ink`), dark neutrals, multiple accents, light and dark.
- `references/export.md`: shipping — the `.svg`, the preview page, `<img>` vs inline, PNGs, size budgets, ambient motion, and the asset checks.
- `references/craft.md`: the look in depth: parts vocabulary, tones, painter's order, round parts and pipes, screens and things on faces, anti-patterns.
- `references/kit.md`: the API, with signatures and examples.
- `references/verify.md`: `capture.mjs`, `drive.mjs`, the line check, the audit and close-ups.
- `references/motion.md`: interactive motion, for an asset the user wants to respond to the pointer or scroll.
- `references/webgl.md`, `references/3d.md`, `references/react.md`: shaders, the 3D mode and React, unchanged from Anatomy.
- `references/walkthrough.md`: how Anatomy's test rig was designed, step by step — the same discipline applies to an asset.
