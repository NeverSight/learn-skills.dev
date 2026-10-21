---
name: fire-paper-loader
description: Build a burning-paper ring loader whose GLSL flame is drawn by a Worker on an OffscreenCanvas started from the head, so a main thread blocked by the page build cannot freeze it, with a progress count, an even-paced run into the hand-off, and a clean fade to the page. Covers the ember thread and ember gradient, porous char, worker start-up, parallel shader compile with a waited 1-px warm-up draw, hand-off without a stall, reduced motion and hidden-tab behaviour. Use for a loading screen, preloader, page loader, splash, "kindling", burn loader, ember ring, burning paper hole, fire loader, or a loader that must keep moving while heavy JavaScript, three.js or shader builds hold the main thread.
---

# Fire-Paper Loader

A ring of burning paper opens on black while the page builds. **The mechanism: the fire is drawn by a Worker on an OffscreenCanvas that is started from `<head>`, so the ring keeps burning while the main thread is blocked for hundreds of milliseconds.** The flame look is staging; a loader that stops dead for 450 ms reads as a hang whatever it looks like.

Nearest skills: `web-design-performance` covers general page speed; this one is specifically a loader that survives a blocked thread. For the burning-paper look on scroll transitions (not a loader), the flame GLSL is the same `kbFlame` but the page draws it. For a spinner or AI-status orb, use `thinking-orbs`.

Stack, verified in the source: Vanilla JavaScript, raw WebGL 1 (GLSL ES 1.00, no Three.js in the loader), Worker plus OffscreenCanvas, CSS for the label and fade.

## Start from the head, not from the body

Symptom: the loader appears 1-2 s late, or the worker never gets a GL context, or the fire stands still while three.js downloads. A worker can start and create its WebGL context only while the main thread is free, which is during stylesheet loading in `<head>` and not again until the page is parsed.

- In a `<script>` in `<head>`: create a canvas, `transferControlToOffscreen()`, start a Worker from a Blob URL of a tiny boot script, post `{kbPre, canvas}` and call `getContext('webgl', {antialias:false, alpha:false, depth:false, stencil:false})` in the worker there and then. Keep the canvas and worker on `window.__kbPre`.
- The boot script is only a shell. The loader's own `<script>` (later in the body) sends its own `textContent` to the worker with `{kbInit, src, canvas:null, t0, origin: performance.timeOrigin, reduced, view, target}`, and the worker `eval`s it. One source text runs on both threads: `const IN_W = typeof document === 'undefined'`. Two copies drift apart.
- Guard every step: no `Worker`, no `OffscreenCanvas`, no `transferControlToOffscreen`, worker `onerror`, or a `fail` message means draw on the main thread with the same code after the same warm-up.
- Convert clocks. The worker's `performance.now()` differs from the page's: send `performance.timeOrigin`, and add `performance.timeOrigin - origin` in the worker so every timestamp the page reads is its own.

## Compile in parallel, warm the pipeline, then show

Symptom: the first visible frames are the slowest of the load (30-130 ms, once 408 ms on Metal).

1. Create both programs (ring, cinders), attach shaders, `linkProgram` both, and only then ask for status. With `KHR_parallel_shader_compile` the driver compiles on its own threads; reading `COMPILE_STATUS` per shader defeats it. Skip the per-shader check when the extension exists.
2. `warmUp()`: run a real frame's draws of both programs into a 1x1 viewport, then `readPixels` 1 pixel, waited. A first draw builds the GPU pipeline; make that happen before anything is seen.
3. Only then start `requestAnimationFrame`. The page's `LOAD.ready()` resolves when the worker draws (typically 0.15-0.3 s, timed out at 1.2 s); the build awaits it so it does not hold the thread off for a second while the fire stands still.
4. Show one canvas, not two. Drawing the fire on both threads first cost compile time in the first visible frames.

## The ring's pace is planned in what is seen

Symptom: the coal sits at one size for a second, then leaps 2.5x; or a ring that stalls is overtaken by a faster one and reads as two fires.

- Plan the growth in `S = gain + ln(radius / first radius)`, not in the raw progress `u`. Equal steps in S look like equal growth at every size. The fade-in weighs 0.3 in S (at 1 it held the size back for 0.9 s).
- Follow `S` with a critically damped spring (omega 5/s, speed clamped to 1.6/s, integrated in 1/120 s sub-steps) toward a goal that is the real progress but never behind a creep: `creep = 0.38*(1 - exp(-t/800 ms))`, and the goal cannot pass `WAIT` 0.290 while waiting, easing toward `CEIL` 0.335 with a 2.5 s time constant. A hard hold and progress arriving in lumps read as a ring parked, then shoved.
- Never still: minimum `VMIN` 0.016/s (about 5 px a frame at 8 fps), maximum `VMAX` 0.05/s. The seen radius: a 4 px fleck at progress 0, 5.8 px by 0.15, then the burn's own radius.
- Before the page has said anything, progress creeps on its own clock, so the ring lives while three.js is still on the wire.

## Hand off without a stall

Symptom: the ring lurches into the page's intro, or the page stutters for 55-240 ms when the loader goes away.

- `done()` runs a Hermite in S from the creep's speed to the intro's speed `V_HAND` 0.24 (u/s), over `ds = clamp(2.8*du/vH, 0.30, 1.2)` seconds, and reports when the rim reaches the hand-off progress `HAND` 0.36. The page resumes its own intro from exactly that progress and clock. A safety timer (`doneDur + 400 ms`, and 2.4 s on the page side) resolves anyway if rAF stalled.
- The label lands on 100 and fades on the compositor (`transition: opacity .40s linear .12s`): a busy first frame cannot cut it short.
- `close()`: set `alive = false` and tell the worker to stop drawing. Two contexts drawing during the fade shared the GPU and ran the fade's frames at 35-67 ms. The last frame stays up and is **faded with CSS opacity** (120 ms, 250 ms under reduced motion), scaled by Web Animations keyframes along the intro's own curve so it stays on the page's rim while it goes.
- **Do not `worker.terminate()` while the page is on screen.** It held the main thread 55-240 ms at any time. Post `free` (lose the GL context in the worker, on the worker's thread) and terminate only on `visibilitychange` hidden or `pagehide`. Never `loseContext()` on the main thread either: it waits on all queued GPU work, including the intro's first frames (100 ms).
- Yield between build stations: `await LOAD.step(p)` sets progress and, at most every 45 ms (90 ms when the worker draws, since only the count needs it), waits one `requestAnimationFrame` plus `setTimeout 0`. In a hidden tab it does not wait, because rAF does not run there.

## The burn look: the footer is the reference

Symptoms the owner named, in order: "too static", "the black part should be alpha masked", then after a four-step posterised ramp, "too non-realistic, like before, the footer burn was better".

- **A luminous gradient, not posterised steps.** The ember zone is a smooth ramp yellow to orange to deep red, hot stretches carrying yellow further back, ending at a crisp torn lip. Hard steps read as a poster.
- **A bright beading thread at the front**, 0.7-5 px, pinched and swollen along its length (an even stroke reads as neon), with a tight additive glow of 2-5 px. Nothing wider: a fat bloom turns the rim into a neon hoop.
- **It must move.** Heat pulses run along the edge both ways (`run`), patches flicker at 7 Hz (`flk`), beads drift, a roll travels back through the zone. A still frame of it looks fine; the loader is judged in motion.
- **Gold, not cream.** The hottest core colour is `(1.85, 1.02, 0.30)`, ember `(1.10, 0.64, 0.17)` at most, only where hot. Cream and khaki came from letting the hot end go white or dimming by darkening; a dim stretch goes down the ramp toward deep red instead.
- **Porous char, no rims.** The charred band behind the ember is near black `(0.0085, 0.0062, 0.0048)` with fibre grain, and pores open in it with age down to the frame beneath. Never ring the pores with glowing edges: they joined into one drawn contour along the edge.
- **A ring never starts as a disc or an "o".** It begins as a torn ember arc, 3.5-7 px thick, a little over half round, whose ends crawl round and meet between 6.5 and 12 px. Ring width is never under 3.5-7 px or it reads as a drawn outline.
- Cinders: four instanced sets (1800, 720, 360, 160 quads, seeded mulberry32 `0x2f6b9d1`), only off the upper arc (20-160 degrees), short lives, heat orange to deep red and never white. Tone-mapped ACES, then sRGB in the shader (`aces` then `srgb`), so keep `gl_FragColor` alpha 1 and the canvas `alpha:false`.

## Cost, measured

- Drawn on the main thread against a build that blocks it 250-450 ms at a time, the longest gap between fire frames was 450 ms. In the worker, on the same page, 9 ms.
- Render at DPR up to **1.5** (the source's cap; the general web cap is 2). The ring is one full-screen triangle plus 3040 cinder quads; the fragment shader is the cost, not the cinders.
- Time step: the worker draws on its own frames; the display clock is the page's, so a dt of the animation is clamped by design (`dtp` max 1.5 s, 1/120 s spring sub-steps).

## Lifecycle and accessibility

- `role="progressbar"` on the label with `aria-valuenow` kept in step; the canvases are `aria-hidden`. The count is text, so it is readable without the fire.
- `prefers-reduced-motion: reduce`: no time (`tSec = 0`), no cinders, no compositor scale; the ring still opens with progress as a still, grained rim and the fade is 250 ms. The frame is designed as a still, not hidden.
- Hidden tab: rAF pauses in both threads; `step()` stops waiting; `done()` resolves at once, and the worker is terminated only then.
- After 12 s at under 40 percent, the label says "Still kindling": slow connections should be told rather than burnt at quietly forever.
- Resize: post the new `view` (w, h, DPR) to the worker; the canvas resizes on the next frame.

## Boundary of what this skill gives you

Mechanism (keep): head-started worker, one source on two threads, parallel compile plus waited 1-px warm-up, S-space pacing, Hermite hand-off, stop-then-CSS-fade, no early terminate. Staging (replace freely): the fire's palette and shape, the label copy, the page it hands to. The demo stands in for the page's intro: after `done()` the loader's ring runs on along the intro curve for 1.8 s until it leaves the frame, where the real page draws its own rim from the hand-off progress.

Source: extracted from the KINDLING loader of KIBORI 木彫, a scroll-linked Three.js woodcraft page whose 1.1 MB build held the main thread for up to 1.2 s.
