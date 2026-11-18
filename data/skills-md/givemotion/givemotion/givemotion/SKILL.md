---
name: givemotion
description: Makes videos from HTML + CSS + JS with givemotion and renders MP4/WebM/GIF/ProRes. Use for any request to create, edit, check or render a video, animation, motion graphic, explainer, promo, logo sting, title card, lower third, animated chart or data story, captions, whiteboard/hand-drawn video, UI or product demo, or vertical social clip, or when a givemotion composition is open.
metadata:
  version: "0.1.6"
---

# givemotion: HTML in, video out

A composition is one HTML file. Every frame is that page at a moment in time. CSS animations, transitions, Web Animations, timers, `requestAnimationFrame`, canvas and WebGL all run on a virtual clock, so what you write renders frame-exact and identically every time. No script tag or import is needed: the runtime (`window.gm`) and a preset stylesheet are injected for you.

This file is the core (read it all). Then read **only** the 1-3 technique recipes your video needs (table at the end): each one shows how a professional builds that effect, with numbers and a working example. Look up anything else when you need it.

## The loop (for an edit, only the steps it needs)

0. **Direct.** Decide how a top studio would make this look. Start from what you have (brand kit, earlier videos, references, a detailed brief); research only what is still open, with a web search if you have one. Then write at the top of the HTML: the look, type system, motion language and shot list (time, on screen, move, hand-over). How: `references/direction.md`.
1. **Style frames.** Build the 2-3 key holds first, still, and `still` each: judge them as posters (one focal point, hierarchy, margins). Then animate.
2. **Write** the motion; `npx givemotion check video.html` as you go: fix every ✖; ⚠ are real faults unless meant; ℹ are style hints.
3. **Review.** `npx givemotion review video.html` (reads `brief.md` beside the page, or `--brief`) shows what a viewer sees: overview, the frames people read, motion strips, `beats.png` (each brief beat at its times). Check each beat word by word, score per `review/REVIEW.md`, fix the five worst. On the near-final cut, give one sub-agent the critic prompt in REVIEW.md, fix what it finds. Brief times go in `data-expect`.
4. **Render:** `npx givemotion render video.html -o out/video.mp4`.

`--json` for machine output, `--help` for options. `still video.html -t 3.2 -o f.png` renders one moment; `inspect --at 4.5 --el "#logo"` says where an element is.

## How good motion is made here

The engine gives you any HTML/CSS/SVG/canvas and a frame-exact timeline; the look comes from how you choreograph it. Blind viewers preferred videos where every element was choreographed by hand over videos built from one-word presets.

1. **Choreograph by hand.** Use `gm.timeline` for anything that matters: explicit start times, per-move easing (a fast `expo.out` slam, a soft `sine.inOut` drift, a `back.out(1.6)` landing), offsets of 40-120 ms between related parts. Presets (`data-enter`, `data-camera`) are fine for small supporting things.
2. **Three layers on every hero moment:** the main move; secondary detail that sells it (blur while fast, a glow, a shadow that grows, follow-through, a ring or particles on impact); and ambient motion so the frame is never frozen (drifting background, slow camera push).
3. **Contrast in timing.** Fast in, slow settle; holds of 0.4-1 s after something lands; exits shorter than entrances. Never move everything at the same speed with the same curve.
4. **Follow the brief exactly** for colors, fonts, copy, sizes and timing; your craft goes into how things move, not into extra content.
5. **Frame 0 is the hook**, nothing is cut by the frame edge, text is big (titles 96-200 px, body ≥ 36 px at 1080p; in 9:16, size headlines to the width), one hero per moment, scenes flow into each other (push, whip, morph, match cut) rather than fading.
6. **Things come from things.** A new element is born from one already on screen, not spawned from nowhere: three circles squeeze out of the main one; a rectangle on screen slides over and becomes the underline; a card grows out of the clicked button; the logo's mark becomes the end card's mark. Reuse before you add. **Plant the next set early**: already in the world (small, dim) while this beat plays, so the camera reveals it.
7. **A camera move means "look here".** Push in only toward something the viewer should read next. Never zoom into empty space or into the old scene as a way to transition: to leave a scene, move sideways (push, whip, wipe) or carry an element across (morph, the rule above).
8. **Animate** `transform`/`translate`/`scale`/`rotate`/`opacity`/`filter`/`clip-path`, not `width`/`top`/`left`.
9. **Every element gets a planned life:** in, a readable hold (~1 s + 0.25 s a word), then an exit or hand-over. The shot list gives each hold.

## Hierarchy: one thing matters at a time

Viewers preferred videos where the eye always knew where to look.
- **Every line has a key word.** Give the word that carries the meaning contrast (accent color, heavier weight, bigger size, or a highlight drawn on); the rest stays quieter. One per line, at most two per screen. If everything is accent, nothing is.
- **Every moment has one hero:** the biggest, brightest thing with the most motion. Support is smaller (hero ≥ 1.6× the next size; three levels at most), dimmer (muted or 50-70% opacity), arrives after the hero and moves less. Effects (rings, sparks) frame the hero, never cross it.
- **Lead the eye in order:** the hero lands first; the key word gets its color or underline 0.2-0.4 s after the line settles; support follows. When the camera or a callout focuses on something, dim the rest.
- **Palette roles strictly:** accent for emphasis only, muted for secondary text.

## Easing: match the curve to the motion

- **Entering** decelerates (ease-out: `expo.out`, `power3.out`, or `back.out(1.4)` when it lands with weight).
- **Leaving** accelerates (ease-in: `power2.in`), shorter than the entrance (60-70%).
- **Moving from A to B** while visible, camera moves, a scale change of something already on screen: ease-in-out (`power2.inOut`, `sine.inOut`): it starts gently and lands gently.
- **Ambient drift:** long `sine.inOut`; `linear` only for loops (spins, tickers). Nothing that starts or stops on screen moves linearly.
- Leave `ease` out and the engine already does this (entrances spring in, moves ease in and out, exits ease in); when you set one, follow the rules above.

## Minimal composition

```html
<!doctype html>
<html data-width="1920" data-height="1080" data-fps="30" data-duration="2.5">
<head>
<style>
  :root { --bg: #0b0d12; --ink: #fff; --accent: #7c9cff; }
  body { background: var(--bg); color: var(--ink); font-family: Inter, sans-serif; }
  .scene { display: grid; place-items: center; }          /* .scene is already absolute + full frame */
  h1 { font-size: 160px; letter-spacing: -0.03em; margin: 0; }
  .glow { position: absolute; width: 900px; height: 900px; border-radius: 50%; background: var(--accent); filter: blur(160px); opacity: .25; }
</style>
</head>
<body>
  <section class="scene">
    <div class="glow"></div>
    <h1 id="t" data-split="chars">Hello</h1>
  </section>
  <script>
    gm.timeline('.scene')
      .from('.glow', { scale: 0.6, opacity: 0, duration: 1.2, ease: 'sine.out' }, 0)             // ambient: light blooms in…
      .to('.glow', { x: 220, y: -90, duration: 2.5, ease: 'sine.inOut' }, 0)                        // …and keeps drifting
      .from('#t .gm-char', { y: 140, opacity: 0, filter: 'blur(12px)', duration: 0.7, ease: 'expo.out', stagger: 0.05 }, 0.2) // main: fast in, blur while fast
      .fromTo('#t', { letterSpacing: '0.12em' }, { letterSpacing: '-0.03em', duration: 2.4, ease: 'expo.out' }, 0.2)        // detail: tracking tightens
      .to('#t', { scale: 1.06, duration: 1.9, ease: 'sine.inOut' }, 0.6);                        // the hold keeps breathing
  </script>
</body>
</html>
```

Built-in fonts: `Inter`, `JetBrains Mono`, `Playfair Display`, `Space Grotesk`, `Bebas Neue`, `Nunito`, `Caveat`; others via `@font-face`.

## Timing model (read this)

- Settings live on `<html>`: `data-width`, `data-height` (even numbers), `data-fps` (default 30), optional `data-duration`, optional `data-background`.
- Times are seconds: `1.5`, `1.5s`, `500ms`, `45f` (frames), `1:02.5`.
- **Clips.** An element with `data-start`, `data-duration` or `data-end` only exists (is `display`ed) from start to start+duration. Times are relative to its parent clip. Elements without timing are always there.
- **Video length** = `data-duration` on `<html>`, otherwise the end of the last clip.
- **Sequences.** `data-sequence` on a container plays its children one after another. Every child needs `data-duration`, or give the container `data-cuts="0 2.13 4.27"` (when each child starts; also `"beats: 0 4 8"` / `"bars: 0 1 2"`). `data-gap="0.2"` (negative = overlap). `data-transition="<name> <seconds> [easing]"` overlaps neighbours and animates the change; a child can set its own `data-transition` (how it comes in). **Each transition takes its length off the total**: 3 scenes of 4s with `fade 0.5` last 11s. Cuts on the beat, `data-cut-align`, and where a scene's time 0 then sits: `references/timeline.md`.
- **Transitions:** `push-`/`cover-`/`whip-`/`wipe-` + `left/right/up/down` (push: new pushes old out; cover: slides over; whip: fast) `diagonal` `clock` `iris` `zoom` `zoom-through` (old scene flies past) `flip` (3D) `dip` (through black) `blur` `fade-up` `fade`, and **`morph`**: elements with the same `data-morph="name"` in both scenes fly and resize from the old place to the new one while the rest crossfades. Carries a logo or card across; in one scene: `gm.fly`.
- **CSS animations run on clip time.** `animation: fade-up .6s .4s both` starts .4s after its clip appears. Use `both` (or `backwards`) fill so the element is hidden before its delay.
- **Something appears later inside a long scene** (one camera world, one whiteboard): the delay in `data-enter` counts from the start of the element's clip, so `data-enter="write 0.8 11.9"` writes a label 11.9 s into the scene and keeps it hidden until then. No extra clip needed.
- `gm.onFrame(fn)` gets the **video's** time, even in a scene; `gm.onFrame('#s', (local, info, el) => …)` counts from `#s`'s start, like `gm.timeline('#s')`.
- Timers, `requestAnimationFrame`, `Date.now()`, `performance.now()` are virtual and `Math.random()` is seeded. Normal web animation code works.

## Timeline: precise choreography (GSAP-style, built in)

For anything with more than a few moving parts, use `gm.timeline`: the GSAP API you know, computed from the time (frame-exact, parallel). Times are seconds **relative to the clip that contains the scope**.

```js
gm.timeline('#scene2')                                     // scope: selectors are looked up inside it
  .from('.title .gm-word', { y: 120, opacity: 0, rotate: 8, stagger: 0.06 })   // no ease: springs in
  .to('.card', { x: 400, y: -60, scale: 1.2 }, '+=0.3')                 // arcs, sized to the distance
  .fromTo('.bar', { scaleY: 0 }, { scaleY: 1, stagger: { each: 0.08, from: 'center' } }, '<')
  .to('#line', { draw: 1, duration: 1.5 }, 2)                       // draw an SVG stroke
  .to('.price', { textContent: 249, duration: 1.5 }, 2.5);          // count a number
gm.fly('#event', { from: '#slot2', at: 7.5, duration: 0.8 });      // fly from another element's box into its own place
```
`from()`/`fromTo()` show their start values from the clip's start (hidden until they enter). Overlapping tweens on one property: the latest start wins. Positions, all props and options, labels, keyframes, `gm.fly` and SVG caveats: `references/timeline.md`.

Also built in (tables in `references/api.md`): `data-enter`/`data-exit` presets, `data-split`, `data-stagger`, `data-count` (`-roll`), `data-roll`, `data-type` (typewriter), `data-scramble`, `data-camera` (push, float, shake…), `data-parallax`, `data-morph`, `data-fit`, `data-pulse`, easing names (GSAP names work), preset CSS keyframes and `var(--px)`, and ready-made blocks (`npx givemotion blocks`: captions, code-window, cursor, browser-window, charts…).

## Technique recipes (read the ones your video needs)

| Your video has… | Read |
|---|---|
| A logo, brand sting, intro or end card | `references/techniques/logo-reveal.md` |
| Big type that slams, stacks, rotates; a headline as the star | `references/techniques/kinetic-type.md` |
| Text reveals: words/chars, typewriter, write-on, scramble, highlight | `references/techniques/text-reveals.md` |
| Camera moves: push, follow, whip, bank, zoom to a detail, shake | `references/techniques/camera-moves.md` |
| Several scenes handing over (push, whip, morph, shape wipes) | `references/techniques/scene-transitions.md` |
| Glow, light sweeps, gradients, grain, blur, depth | `references/techniques/light-and-depth.md` |
| Numbers, counters, bar/line charts, callouts | `references/techniques/numbers-and-charts.md` |
| Lines that draw, routes, maps, pins, something travelling a path | `references/techniques/paths-and-maps.md` |
| Flat shapes: grow, squash, split, orbit, morph | `references/techniques/shapes-and-motion-graphics.md` |
| An app/UI with a cursor, clicks, typing, lists | `references/techniques/ui-demo.md` |
| Code in an editor, typing, line highlights | `references/techniques/code-on-screen.md` |
| Impact and energy: slams, shake, bursts, music beats | `references/techniques/impacts-and-energy.md` |
| Word-by-word captions, vertical 9:16 clips | `references/techniques/captions-vertical.md` |
| Whiteboard, sketch, hand-drawn | `references/techniques/hand-drawn.md` |
| A living background behind everything | `references/techniques/backgrounds-and-ambient.md` |

## API reference (look up when needed)

| When… | Read |
|---|---|
| An attribute, preset, easing name, preset CSS or block | `references/api.md` |
| `gm.timeline` in full: positions, keyframes, labels, `gm.fly`, SVG | `references/timeline.md` |
| `gm.camera` worlds, shots, `gm.path.travel`, riding, parallax | `references/camera.md` |
| `gm.chart.*`, chart blocks | `references/charts.md` |
| Diagrams, arrows, `data-sketch`, `gm.connect`, `gm.shape`, path morphs | `references/diagrams.md` |
| Music, beats, voice-over + `givemotion words`, video clips, captions | `references/media-audio.md` |
| Data/templates, `<gm-include>` (scope, scenes, brand kit), blocks, highlight, cursor | `references/data-templates.md` |
| `gm.onFrame`, canvas, three.js, `gm.burst`, springs, noise, random, Lottie | `references/javascript.md` |
| Render options, transparency, cache | `references/output.md` |
| Reviewing frames, learning from a reference video | `references/review.md` |
| A check code | `references/check-codes.md` |
| Motion principles in depth (optional) | `references/motion-design.md`; genre structures in `references/genres/` |
