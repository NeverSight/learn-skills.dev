---
name: motion-graphics
description: Build frame-exact motion graphics — animated logos, kinetic typography, brand videos, animated titles and social clips — as a single HTML file driven by a paused Web Animations timeline, then export them to MP4 in 1:1, 4:5 and 9:16. Use this whenever someone wants to animate a wordmark or logo, make a video from text, build a title sequence or lower third, produce a clip for LinkedIn / Instagram / Reels / TikTok, "turn this design into a video", animate a landing-page hero, or export a web animation to a video file — and also when an existing animation of this kind needs fixing, retiming, restyling or re-exporting. Reach for it even if the person only says "animate our logo", "make this move", or "I need a short video for the launch", without naming any of the above.
---

# Motion graphics as code

Everything here is built the same way: **one HTML file, one paused timeline, deterministic export**. No video editor, no After Effects, no timeline GUI. The animation is code, so it is diffable, reviewable, re-renderable at any size, and — crucially — *measurable*.

That last word is the heart of this skill. Motion work invites eyeballing, and eyeballing lies. Nearly every real defect you will hit here is invisible to a glance and obvious to a measurement, and several things that *look* broken turn out to be the measuring script's fault. Build the habit early: when something looks wrong, get a number before you get an opinion.

## The shape of the thing

```
project/
├── video.html      # canvas, scenes, timeline — the whole animation
├── export.js       # frame-by-frame capture → MP4, all aspect ratios
└── verify.js       # whatever you need to assert about this piece
```

Copy `assets/starter.html` to begin. It is a complete, working animation with the engine already wired — type that enters, a recurring mark that highlights a word, and a scene that exits. Its palette and motif are placeholders; the structure is the point. Read it before writing anything; it is faster than assembling the pieces from the references.

`scripts/timeline.js` is the engine and `scripts/physics.js` the simulator — inline both into the HTML, since a single self-contained file is the deliverable. `scripts/export.js` and `scripts/verify.js` run in Node and work unchanged for any project that exposes `window.__seek` and `window.__duration`.

## Why a paused timeline

CSS animations and libraries run on wall-clock time. That is fine for a website and useless for a video: to capture frame 847 you must be able to *put* the animation at frame 847, exactly, on demand.

So: every animation is created through the Web Animations API with `fill: 'both'`, its absolute start time baked into the timing as `delay`, and immediately paused. Then

```js
function seek(s){ A.forEach(a => { a.pause(); a.currentTime = s * 1000; }); }
```

positions the entire piece at any instant. The exporter walks `0 → duration` in `1/fps` steps and screenshots. The result is identical on any machine and does not care whether the browser can hit 60fps in real time.

This buys you something else: you can *interrogate* any moment. `seek(7.2)` then read a `getBoundingClientRect()`. That is what makes the verification below possible.

## Workflow

**1. Lay out the canvas.** Fixed internal coordinates (1080 wide is a good default), scenes absolutely positioned and stacked, only the height varying per aspect ratio. Read `references/craft.md` before placing type — optical centering is not the same as centering the box, and getting it wrong is the single most common reason a composition "feels off" without anyone being able to say why.

**2. Build the timeline.** Scene by scene. Give each element one animation covering its whole life. Keep an eye on the four failure modes below; they account for most of the time lost on work like this.

**3. Verify by measuring.** Before showing anything, write the small script that checks the thing you are unsure about. `references/verify.md` has the recipes and, more importantly, the traps in the measuring scripts themselves.

**4. Export.** `node export.js` → the MP4s. `references/export.md` covers the encoder flags that decide whether a platform accepts your file.

## The four things that will bite you

These are not style preferences. Each one produced a bug that survived visual review.

### One animation per element

Entrance, hold and exit go in a single keyframe list. Two animations with `fill: 'both'` touching the same property collide, and **the later-created one wins from time zero** — so an element that should appear at 14s is visible from the first frame, with its "before" state applied backwards through the whole piece.

The symptom is bizarre and misleading: content from a later scene bleeding through an earlier one. If you see that, count the animations on the element.

### `seek()` must pause first

A preview loop keeps playing. Set `currentTime` on a *running* animation and it advances a few milliseconds before the screenshot lands. This is not a preview annoyance — it silently corrupts **every frame of the export**, and the result looks plausible enough that you will ship it.

Pause, then set the time, and cancel the preview loop the first time an external seek arrives.

### Keyframe times must be monotonic

When you chain moves — "then it hops here, then there" — it is easy to schedule one before the previous finished. WAAPI rejects the whole animation with `Offsets must be monotonically non-decreasing`, which tells you nothing about which move overlapped.

Clamp on the way in, so the times in your script are *intentions* rather than fragile arithmetic:

```js
const push = (t, s, ease) => { t = Math.max(t, lastT); lastT = t; /* ... */ };
```

The same hazard reappears in anything assembled from several sequences (a shared camera track, for instance). Clamp there too.

### Measure before you animate

`fill: 'both'` applies the first keyframe immediately, so the moment you create the animations, every `getBoundingClientRect()` reflects a transform. Do all layout measurement first, then build the timeline. Ordering: build DOM → optically centre → measure targets → create animations.

## Pick a motion language, then hold to it

The most common way a piece looks amateur is that different elements arrive in different ways. Choose **one** way things enter and one way they leave, and apply it everywhere. Which one is a **tone** decision, not a technical one:

| Language | Says | `MG.ENTER` / `MG.EXIT` |
| --- | --- | --- |
| Speed — arrives fast with a directional smear and brakes | urgency, sport, news, "we move fast" | `speed` |
| Pop — grows from nothing and overshoots | playful, product, consumer, toy | `pop` |
| Wipe — a hard edge uncovers it, nothing moves | editorial, architectural, confident | `wipe` |
| Drift — barely moves, the fade does the work | premium, calm, luxury, serious | `drift` |
| Rise — comes up out of its own baseline | cinematic titles, credits | `rise` |
| Focus — comes into focus from blurred | photographic, dreamy, memory | `focus` |

They return keyframe *steps*, so an entrance and an exit concatenate into one list:

```js
tl(el, [...MG.ENTER.pop(tIn, {size: fs}), ...MG.EXIT.drift(tOut, {size: fs})]);
```

Nothing about the rest of this skill assumes a particular one. If a brief does not suggest a tone, ask — it is a bigger decision than any timing.

## What holds regardless of language

**Nothing should ever be perfectly still.** A frame that holds motionless for two seconds reads as *stuck*, even at a flawless 60fps. Every scene gets a slow continuous push — settle over ~1.5s, then keep drifting a fraction of a percent. Around 0.7% total; at 1.4% people notice things "levitating".

**Arrivals decelerate, departures accelerate.** Whatever the language, matching the two curves makes everything feel rubbery.

**Chained ease-outs read as stop-start.** Each segment decelerates to zero and the next starts fast again. Use ease-in-out for anything continuous, and reserve the braking curve for actual arrivals.

**Stagger is a lever.** The same language feels completely different per-letter, per-word or per-line. Per-letter is energetic and gets tiring past a few words; per-line is calm and reads better for sentences.

**Scale the exit down for large type.** Exit distance is usually proportional to size, so at 112px a default sweep crosses half the screen and collides with the next scene.

**A recurring element can carry the whole piece.** One shape that persists across scenes gives a video a spine that cuts alone cannot — a rule that underlines the key word, a dot, a cursor, a colour block that reframes each card, a mask edge. Treat it as a character rather than a graphic: anticipation before it moves, overshoot on arrival, weight when it lands, a small idle vocabulary for when it waits. Drive any randomness from a seeded generator, because `Math.random()` makes the preview and the export different films.

**An element that crosses text reads as a rendering bug**, even when the copy explicitly calls for a strikethrough. Keep it behind the type so letters cut through it.

**Dark backgrounds change things.** A trail's colour, flat-area banding, and the fact that two stacked vignettes draw a visible ellipse edge. `MG.trail()` takes a colour for exactly this reason — hardcoded black on a dark ground is an invisible smear.

## Physics, when you need it

For anything thrown, dropped or bounced, integrate the motion rather than reaching for an easing curve. An `ease-out` is not a fall — it decelerates, and falls accelerate. The same goes for departures, which start slow and build.

`scripts/physics.js` has this solved. `PHYS.drop()` does projectile, bounce and topple for boxes; `PHYS.roll()` does the same for anything round, which is a genuinely different solver; `PHYS.departure()` does something pulling away; `PHYS.keyframes()` turns any of them into keyframes. Use them rather than rewriting — the two bugs that make hand-rolled rigid bodies look wrong are already handled, and `references/physics.md` explains what they were.

## Verify by measuring

The habit, concretely: before you claim something is fixed, write six lines that check it and print a number.

- Reproducing a reference exactly? Diff the rendered pixels, then — because pixel counts explode from sub-pixel antialiasing — **also compare geometry**, element by element, at matching instants. Geometry is the real claim; the pixel count is a coarse net.
- Something "feels janky"? Measure frame times before touching the design. It is often not dropped frames.
- Element flying off-frame? Sample its rect across the window and report the worst overflow.

And a warning that will save you an hour: **when a check suddenly fails, suspect the check.** In practice most alarms were stale measurement windows, a fixed timestamp that drifted after a retime, a comparison of elements that were invisible at that moment, or a race in the harness. Confirm the failure independently before you "fix" working code.

`scripts/verify.js` has each of these as a function you can import; `references/verify.md` explains what each one is really testing.

## Export

`node export.js` renders 1:1, 4:5 and 9:16. Three things decide whether the file is usable:

- **`yuv420p`** — without it, platforms and QuickTime refuse to decode.
- **`+faststart`** — without it, playback waits for the whole download.
- **A silent audio track** — some platforms reject video-only uploads outright.

Change aspect ratio by making the **canvas** taller, never by padding a square with flat colour. If the design has any vignette or gradient reaching the edge, flat padding leaves a visible seam.

One trap specific to Playwright: `screenshot({ animations: 'disabled' })` does not freeze anything — it fast-forwards animations to their end state, and every exported frame comes out identical. The timeline is already paused; do not pass it.

## When the copy is the problem

If you are writing the words too and two rounds of alternatives all feel wrong, stop generating options. The words are usually fine — the *slot* has no defined job. Ask what that beat is for (name the problem? answer the objection? show proof?) and the line tends to write itself. A defensive beat dropped into the middle of a persuasive sequence will feel wrong no matter how well it is phrased.

Two related instincts: consistency between scenes beats cleverness in one of them — a scene that is twice as long as its neighbours reads as a mistake even when its content earns the time. And when someone says a section is "too slow", scale its whole sequence by a factor rather than trimming one hold; the internal rhythm is usually right.

## References

Read the one you need, when you need it.

| File | What is in it |
| --- | --- |
| `references/engine.md` | Timeline internals, the failure modes in depth, camera and shared tracks |
| `references/craft.md` | Optical centering, trails, easing, recurring elements, idle vocabulary |
| `references/physics.md` | Why the solver in `scripts/physics.js` is built the way it is |
| `references/verify.md` | Measurement recipes, and the traps in the measuring scripts |
| `references/export.md` | ffmpeg flags, aspect ratios, platform requirements |
