---
name: anatomy-reveal
description: Build any physical object (a product, a tool, furniture, an instrument, a shoe, a vehicle, a piece of jewellery, kitchenware, a toy, even a fruit or a flower) as a crafted isometric "anatomy" figure made of many small convex parts, then turn it into (1) an interactive dissection page you can drag, turn and take apart, and (2) a product-reveal film (MP4, 9:16, 4:5, 1:1 or 16:9, 30 fps, motion blur, white paper look, 10 s by default, any length from 3 to 60 s). The film tumbles in, whips to macro shots of the object's details, shows one feature working, explodes into its parts and snaps back together for a hero shot. Works from a photo of the object or from just its name. Use it when someone asks for an exploded view, a teardown or dissection drawing, an anatomy figure, or a product reveal or product motion video of an object.
license: MIT
compatibility: Node.js 20+, Google Chrome / Chromium / Edge (set CHROME_PATH if it is not found), ffmpeg, ImageMagick 7 (magick). Any agent that can run shell commands and write files.
---

# Anatomy Reveal

The object is never a stock 3D model or a traced picture. It is built part by part from its real dimensions, with the Anatomy kit's 3D mode (`template/kit`):
- every panel, screw, dial, glass element and board is its own convex solid;
- each part is shaded in four tones by how it faces the light;
- parts are painted in an order solved from separating planes.

Because the object is real geometry, the same model turns through any angle, comes apart, and drives both outputs.

`template/` is a complete working project. Its worked example is a dual-boiler espresso machine with a built-in grinder (82 parts), but nothing in the pipeline is specific to espresso machines: any object the user names or shows works the same way. Start every job from the template and replace the object.

Read before building:
- `references/inputs.md`: getting from a photo or a name to dimensions, features and a parts list.
- `references/objects.md`: how any kind of object comes apart, and how to build curved, organic, soft and large shapes from convex parts.
- `references/object.md`: how to build the object so it turns through every angle and comes apart cleanly.
- `references/shots.md`: the film's beats, the timeline format, eases and framing.
- `references/look.md`: the paper look, materials and line weights.

## Inputs: two cases

**A. The user uploads an image of the object.**
- Study it for silhouette, proportions, materials, colours, surface decoration, visible controls, ports and markings, and anything that moves.
- If you can tell what product it is, also look up its real dimensions and internals as in case B. Otherwise estimate the size from a feature of known size and say what you assumed.
- The image is a reference only. Rebuild every shape, colour and ornament as geometry: never trace it, embed it, or map its pixels onto anything.

**B. The user only names the object.**
- Research the real product:
  - overall dimensions in millimetres, and the main sub-dimensions;
  - materials and colourways;
  - every visible control, port and marking;
  - how it opens, folds, slides or turns;
  - what is inside (teardowns are the best source).
- Use web search when you have it. Without it, use what you know and list your assumptions.
- If the name is ambiguous (a model family, several generations), pick the most common variant and say which.

Either way, finish with a short spec before any geometry: the dimensions, the feature list, the parts list grouped by assembly, and the one or two features that will move in the film. Show it to the user if anything is uncertain.

## Workflow

1. **Size it.** An object is a "Hero": 100–150 parts, about 2–4 hours for the object and about 1 hour for the film. Tell the user, then build. Have the object rendering on a test page early, and deepen it from there.
2. **Gather the facts** for case A or B above (`references/inputs.md`).
3. **Scaffold:** `node <skill>/scripts/new-project.mjs <dir>`. It copies `template/`, installs `puppeteer-core` and builds the example, which proves the toolchain works on this machine.
4. **Build the object** in `object/geometry.mjs`, following the rules in `references/object.md`:
   - a hollow shell of convex panels;
   - explode assemblies whose outer parts lead;
   - feature groups (hinges, turns, slides);
   - anchors for every shot;
   - markings as face planes.

   Iterate with these, and look at every image you make:
   - `node object/test-page.mjs --light`;
   - `node object/shots.mjs object/test-light.html out/t/a '{"yaw":-35,"pitch":12}' '{"yaw":-35,"pitch":20,"apart":1}'`;
   - `node object/scan-apart.mjs <yaw> <pitch>` from five views (front, back, top, below, side), until each says no pairs pass through each other and no forced picks.
5. **Describe the object** in `object/film.mjs`. The figure page and the film read everything object-specific from this one file:
   - `FILM`: the title, the scene radius (about 0.8 × the largest dimension in mm), an accessible label, the bounding box;
   - `FIGURE`: the page title, starting view, legend keys and caption (with `{parts}`, `{assemblies}` filled in);
   - `FEATURE_DEFAULTS` and `FEATURE_KEYS`: each moving feature, its key on the page, its values or step;
   - `featureValues` and `featureTravel`: how features map to groups and how far they move a part.
6. **The anatomy page.** Run `node object/build.mjs` and `--light` to write `object/figure.html` and `object/figure-light.html`. Serve the folder over http to look at it in a browser.
7. **Choose the length and the ratio.** Ask the user if they have not said (default 10 s, 9:16), then build the film page with `node motion/build.mjs --duration <seconds> --ratio <9:16|4:5|1:1|16:9>` (3–60 s). Whips keep their length; drifts and holds stretch or compress. For films over about 12 s, add beats (more detail shots) rather than only stretching.
8. **Choreograph** `motion/timeline.mjs` beat by beat (`references/shots.md`):
   - frame every shot with `node motion/render.mjs poses '[…]' out/p` and pick by eye;
   - check timing with `node motion/render.mjs stills 0,1.2,2.3,3.5,4.6,5.6,7.9,10 out/s`;
   - `node motion/scan.mjs` must report every frame clean.
9. **Render:** `node motion/render.mjs blur out/blur --step 4 --most 40`, then `node motion/encode.mjs out/blur out/<name>.mp4`.
   - The render sizes each frame's motion blur from how far the picture moves: whips get up to 40 sub-frames, holds 1.
   - It takes about 2 minutes per second of film. Run it in the background and keep other browser work off the machine.
10. **Check the MP4 itself.** Extract frames (`ffmpeg -i out/<name>.mp4 -vsync 0 out/check/f_%03d.png`), contact-sheet a dozen of them, and look.
11. **Deliver:** the MP4, the two figure pages and the project folder. Say what you did not verify. The film is silent; offer to cut it to a track the user supplies.

## Rules

- **Geometry only.** No images from the user, the web or a generator end up in the figure or the film. Decoration such as engraving, filigree or print is drawn: SVG on a face plane, or raised convex pieces.
- **True to the object.** Use real millimetres, the real count of buttons and screws, and the real way it opens. Detail comes from real parts, never noise.
- **Convex parts only, never sunk in.** The build refuses a pair it cannot separate: move or split the part.
- **One continuous take.** Change subject with a whip (about 0.24 s); holds keep drifting; the last half-second is the only stillness.
- **Paper look.** The film is drawn on warm white paper in the kit's light theme: ink outlines, four-tone fills. Keep it unless the user asks otherwise.
- **Neutral markings by default.** Label parts generically (SoC, crown, battery). Draw a maker's logo or trademark only when the user asks for a faithful replica.

## Files

| Path | What |
|---|---|
| `scripts/new-project.mjs` | Copies the template into a new folder, installs, builds the example. |
| `template/kit/` | The Anatomy kit (MIT), with extra materials (glass, pcb, sensor, signal, porcelain, lavender, knit, coffee, bean, milk, smoke) and two debug hooks in `turn.mjs`. |
| `template/object/geometry.mjs` | The object: parts, groups, explode assemblies, feature poses, anchors. |
| `template/object/scene.mjs` | Projection, build, `orient()` (yaw, pitch, roll in view space), `explodeValues()`. |
| `template/object/film.mjs` | Everything object-specific the page and the film read: titles, scene radius, labels, bounds, feature channels and keys. |
| `template/object/build.mjs`, `live.js` | The interactive anatomy page. |
| `template/object/test-page.mjs`, `shots.mjs`, `scan-apart.mjs`, `capture.mjs` | The bare test page, posed screenshots, the explode pass-through sweep, page captures. |
| `template/motion/timeline.mjs` | Keys, eases, labels, the retiming behind `--duration` and the framing behind `--ratio`. |
| `template/motion/build.mjs`, `look.css` | The film page: `frame(t)`, `pose(state)`, `speed(t)`. |
| `template/motion/render.mjs`, `encode.mjs`, `scan.mjs` | Stills, poses, the adaptive-blur render; averaging and H.264 encode; the per-frame order check. |
| `template/scripts/browser.mjs` | Finds Chrome, Chromium or Edge on macOS, Linux or Windows (`CHROME_PATH` overrides). |
