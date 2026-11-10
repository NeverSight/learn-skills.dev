---
name: reanimate-flutter
description: Rebuild an animation from a website, video, gif or Lottie file as a Flutter widget, then verify the Flutter version against the reference frame by frame (timing, easing, pixels) using a Flutter web build. Works on top of the reanimate skill. reanimate records the reference and writes the motion spec; this skill turns CSS / Web Animations keyframes into an AnimationController + TweenSequence widget, renders it in a web harness at the reference's position and compares it with reanimate's tools until it matches. Use whenever the user wants to clone, port or recreate a web or video animation "in Flutter", "as a Flutter widget", "in our Flutter app", or asks to convert a CSS / Framer Motion / GSAP animation, a loader, a hero entrance, a stagger, a hover or a loop to Flutter.
---

# reanimate-flutter

Move the motion of a reference into Flutter and prove it with the same frame-by-frame comparison reanimate uses. The deliverable is a widget in the user's Flutter project plus evidence (numbers and side-by-side sheets).

This skill relies on the **reanimate** skill for capture, analysis and comparison. `<reanimate>` below is that skill's directory: the sibling folder `../reanimate` when both are installed from this repository. `<skill>` is the directory this SKILL.md lives in.

## Workflow

### 0. Scope and reference: done by reanimate

Follow reanimate's steps 0 to 3 (`<reanimate>/SKILL.md`): scope, `setup.sh`, capture the reference, read every sheet, write `spec.md`. Use the same fidelity levels. For Flutter, add one more line to the top of `spec.md`:

- **Destination**: the Flutter project, the file the widget goes in, and which screen uses it.

Capture the reference with **`--clock virtual`**. The Flutter clone can only be captured on the virtual clock (its frames are drawn on a canvas, and the virtual clock is what makes them exact), and both sides must be captured the same way. A loop or idle animation should also use `--trigger none --pre-js <skill>/templates/restart.js` so both sides start their timeline at the same moment.

### 1. Generate the motion widget

When `inspect.json › animations` holds the motion (CSS animations, transitions, WAAPI), generate the widget instead of writing it by hand:

```bash
bun <skill>/scripts/css2flutter.ts --inspect ref/inspect.json --name <@keyframes name> --widget <Name>Motion --out <app>/lib/<name>_motion.dart
```

Every element running that animation shares one `AnimationController`:
- infinite loops get a phase per element (negative CSS delays)
- finite staggers get an `Interval` per element (delay + duration over the whole run)
- each changing property gets a `TweenSequence` with the exact keyframe offsets, holds and per-keyframe easings

The widget takes the visuals as `children` (one per animated element, in DOM order) and an optional `layout`. It exposes `restart()`.

The generator covers `transform` (translate, scale, rotate, computed `matrix`) and `opacity` with cubic-bezier and keyword easings. Anything else is yours to write by hand, from `references/mapping.md`:
- JS-driven motion (GSAP, Framer Motion springs), where `track.json` + `easing.ts` give the curve
- `steps()`, colour, size or clip animations
- scroll-linked motion
- canvas and WebGL

### 2. Build the visuals

Write the static widgets from `spec.md` and `inspect.json › nodes`: sizes, radii, colours, opacity, fonts (pixel-faithful only). Keep each animated element a separate child so the generated widget can move it.

### 3. Verify in a web harness

1. Create a harness app next to the evidence (it is not the user's app):
   ```bash
   flutter create --platforms web -e --project-name <name>_clone .reanimate/<name>/flutter_clone
   ```
   If the user's widget lives in their app, add that app as a path dependency or copy the widget file in.
2. Copy `<skill>/templates/main.dart` to `lib/main.dart` and fill its TODOs:
   - the page background
   - the animated container's position and size in the reference viewport (`inspect.json › nodes`, CSS px)
   - the widget and its children
   The harness registers `window.__reanimateRestart` for the capture.
3. Build and serve it:
   ```bash
   flutter build web --release --no-web-resources-cdn   # CanvasKit bundled, no CDN during capture
   bun <skill>/scripts/serve.ts .reanimate/<name>/flutter_clone/build/web --port 5180   # run in the background
   ```
4. Capture it with the reference's exact command, changing only `--url http://localhost:5180/`, `--out flutter-N` and the tracking. Flutter draws on a canvas, so drop `--track`. Add `--wait-before 3000` so the engine has booted before the trigger.
5. Compare and look at the sheets every round, exactly as reanimate's step 5 says:
   ```bash
   bun <reanimate>/scripts/compare.ts --ref ref/frames --clone flutter-N/frames --out compare-flutter-N
   bun <reanimate>/scripts/sheet.ts compare --ref ref/frames --clone flutter-N/frames --diff compare-flutter-N/diff --out compare-flutter-N/sheets --every 2 --offset <alignment from report.json>
   ```

Loop until every spec row passes (2 to 5 rounds). Change the smallest thing the evidence points at:
- the curve
- a keyframe offset
- the phase
- the layout offset of a child

Then rebuild, re-capture and re-compare.

### 4. Report

Same as reanimate's step 6, plus:
- where the widget is and how the app uses it
- the harness path
- the last compare round's numbers

Name the residuals that come from Flutter itself rather than from your code (see `references/mapping.md › Known differences`).

## Pitfalls

- **Real-clock capture with `--scale` above 1**: reanimate's real-clock mode crops the 1× video with scaled coordinates. Use `--clock virtual`, which you need for Flutter anyway.
- **Different `--track` selectors on the two sides**: `easing.ts --compare-track` needs the same selector in both tracks. Flutter has no DOM, so compare Flutter clones by pixels and activity curves, not tracks.
- **CanvasKit from the CDN**: without `--no-web-resources-cdn` the build fetches the engine from gstatic during capture. That is slower, needs the network and can time out on the virtual clock.
- **Starting state**: render the pre-motion state in the first frame, as the reference does (the generated sequences start at the first keyframe). Do not show the final state before the controller ticks.
- **Opacity inside and outside**: a child's own `Opacity` multiplies with an animated opacity. Put an element's static opacity in the child only when the keyframes do not animate opacity.
- **Transform order**: the generated widget applies translate → rotate → scale around the centre. That is right for `translate() rotate() scale()`. Reorder the wrappers by hand for any other order, and set `alignment` when `transform-origin` is not the centre.
