---
name: data-story-charts
description: Data-story videos where an animated chart carries the argument - lines that draw as time passes, bars that grow, a big counter that ticks, axes that rescale when the data surprises, annotation pins on the key moments - rendered to MP4 at 9:16 or 16:9 with HyperFrames, SVG and GSAP. Use whenever someone wants to animate statistics, show a trend, growth or cost over time, compare numbers, break down a figure (salary, budget, benchmark), or turn a dataset or table into a short narrated video. Not for architecture or request flows (use system-diagram-animation) or text-only videos (use kinetic-typography).
license: MIT
compatibility: HyperFrames (Node 22+, FFmpeg) with GSAP and inline SVG. Fonts from Google Fonts.
---

# Data Story Charts

One chart, built and revealed in the order of the story. The number is the hero: a big counter at the top, a line or bars that move with it, and annotation pins that say why it changed. It should feel like explanatory journalism: clear, calm, with one or two dramatic moments.

## Options

| Option | Default | Notes |
|---|---|---|
| format | vertical 1080×1920 | or landscape 1920×1080 |
| duration | 15–20 s | about 3–5 s per data beat |
| chart | line | `line` (change over time), `bars` (compare), `stacked` (break down a total), `counter` (one big number) |
| tone | editorial | `editorial` (default, light paper), `dark` (navy, glowing accent), `punchy` (faster, colour flips on the big moment) |

## Brief (answer before planning)

1. What is the one number or change the viewer should remember?
2. What is the data (paste or file)? Units, time range, source.
3. What is the surprise: a spike, a drop, a crossing, a hidden cost?
4. Which 2–4 moments deserve an annotation pin?
5. What is the closing line?

Use only real numbers the user gave, or numbers you computed from their data. Never invent data. If something is an estimate, say so on screen.

## Reads sheet (write it with the beat list)

For every beat, write the one thing the viewer must understand ("the robot can't fly", "the cache missed") and how long it stays readable. One read at a time. Text floors: a label stays at least 0.8 s, a sentence about 0.3 s per word once fully on screen. If the text won't fit the time, cut words rather than speed up.

## Motion discipline

- Motion is causal: every move has a reason on screen (a click, a fall, a packet arriving), and the next move follows from it.
- Pick one main direction of travel for the whole video and keep it. Use the other directions for meaning: up for success or conclusion, a zoom out for "here's the whole picture".
- A scene's exit sets up the next entry: same axis, same direction, similar speed. Carry one object across the change instead of crossfading.
- No idle filler motion (floating, breathing, wobbling) on diagrams, charts or text. If nothing should move, hold still; one deliberate camera drift is enough.
- Easing: smooth ease-out for entries (`power2.out` to `power4.out`), quicker ease-in for exits (about 75% of the entry time). Entries at most 0.8 s. Total stagger for a group at most 0.5 s. Overshoot (`back.out`) only for small pops; no elastic or bounce.
- One thing moves at a time when it matters; the eye can follow only one.
- Add a 0.3–0.75 s beat of stillness right before the payoff.

## Style rules (always)

1. One chart type per scene and one series in focus. Other series are grey.
2. The chart is revealed by time or by story: lines draw left to right, bars grow in order, and nothing appears before it is talked about.
3. A big counter shows the current value and ticks with the chart (tabular numbers).
4. When the data outgrows the axis, the axis rescales on screen (an eased tween of the scale and its labels). That rescale is usually the best moment in the video.
5. Pins annotate the 2–4 key points with short labels.
6. Every label passes 3:1 contrast. Grid and tick labels are a muted dark grey, not pale grey.

## Defaults and overrides

Precedence: the user's brand or spec, then the explicit request, then these defaults.

- Editorial: paper `#f7f4ee`, ink `#16213a`, grid `#e3ded4`, tick labels `#5b6270`, accent `#e4572e`, positive `#047857`, warning `#a16207`, negative `#c2410c`.
- Dark: stage `#0f1724`, ink `#f2f5f9`, grid `#1f2b3d`, labels `#9fb0c8`, accent `#38d6e0`.
- Font: Inter (900 for the counter at 140–170 px, 800 for captions at 56–64 px, 600 for labels at 26–30 px).

## Setup (once)

```bash
node -v && ffmpeg -version
npx hyperframes init my-video --non-interactive --resolution portrait && cd my-video   # landscape for 16:9
```

## Route

| Need | SVG + GSAP in HyperFrames (default) | Remotion | D3 inside HyperFrames |
|---|:-:|:-:|:-:|
| Lines, bars, counters, pins | yes | yes | yes |
| Thousands of points or map projections | heavy | heavy | yes (draw from time `t`) |
| Runs with only Node and FFmpeg | yes | yes | yes |

## Layout

- **9:16:** kicker label at y 285, counter at y 350 (150 px), chart area x 120–960 by y 520–1000, axis labels below, caption at y 1110–1250.
- **16:9:** counter top-left, chart x 200–1720 by y 260–880, caption bottom-left or right of the chart.
- Pins sit above their data point with a dashed stem. Keep them clear of the counter and the caption.

## How to animate it (seek-safe)

Write the data as a function or an array, and draw the whole chart from one clock value `t`. One tween drives the clock, and its `onUpdate` redraws:

```js
const clock = { t: 0 };
tl.to(clock, { t: DURATION, duration: DURATION, ease: "none", onUpdate: () => draw(clock.t) }, 0);
draw(0);
```

`draw(t)` rebuilds the line path up to `t`, moves the marker and the counter, and positions pins and axis labels from the current axis maximum (itself a function of `t`). Because every pixel comes from `t`, any frame renders the same whenever HyperFrames seeks to it.

| Move | How |
|---|---|
| Line reveal | path built from samples up to `t` (about 30 per second of data) |
| Area under the line | the same path closed to the baseline, accent colour at 12% opacity |
| Bars grow | heights tween from 0 with a 0.08 s stagger, `power3.out` |
| Counter | text from the current value; 1 decimal under 10, whole numbers above |
| Axis rescale | `yMax(t)` eases from the old to the new maximum over 1–1.5 s, while tick labels update |
| Pin pop | scale 0.5 → 1 with `back.out(2.5)` at its time |
| Emphasis | the counter scales 1.12 yoyo on the key number |

## Make it eye-catching

- The first frame already has the counter, the axes and the question.
- The surprise moment gets the rescale, a pin and a caption change all within half a second.
- A small marker (a dot, an icon or a character) rides the tip of the line, so the eye knows where to look.
- The area fill and a soft accent glow on the leading point give depth without clutter.
- Captions are short sentences with the number in the accent colour ("Then: **120 m.**").
- Every frozen frame states a fact on its own.

## Starter

```html
<div id="root" data-composition-id="main" data-start="0" data-duration="10" data-width="1080" data-height="1920" style="background:#f7f4ee;font-family:Inter,sans-serif">
<svg viewBox="0 0 1080 1920" width="1080" height="1920" style="position:absolute;inset:0">
  <g id="grid" font-size="26" fill="#5b6270"></g>
  <line x1="120" y1="1000" x2="960" y2="1000" stroke="#16213a" stroke-width="4"/>
  <path id="area" fill="#e4572e" opacity=".12"/><path id="line" fill="none" stroke="#e4572e" stroke-width="9" stroke-linejoin="round" stroke-linecap="round"/>
  <circle id="dot" r="14" fill="#e4572e"/>
</svg>
<div style="position:absolute;left:60px;top:350px;font:900 150px/1 Inter,sans-serif;color:#16213a;font-variant-numeric:tabular-nums"><span id="num">0</span></div>
</div>
<script>
const D = 10, X0 = 120, X1 = 960, Y0 = 1000, Y1 = 520;
const data = (t) => 2 * t + (t > 6 ? 40 * ((t - 6) / 4) ** 2 : 0);          // replace with the user's data
const yMax = (t) => 20 + 60 * Math.min(1, Math.max(0, (t - 6.5) / 1.2));    // axis rescales at the surprise
const px = (t) => X0 + (X1 - X0) * (t / D), py = (v, m) => Y0 - (Y0 - Y1) * (v / m);
const NS = "http://www.w3.org/2000/svg", grid = document.getElementById("grid");
const ticks = [0, 0.5, 1].map((f) => { const l = document.createElementNS(NS, "line"), x = document.createElementNS(NS, "text");
  l.setAttribute("x1", X0); l.setAttribute("x2", X1); l.setAttribute("stroke", "#e3ded4"); x.setAttribute("x", X1); x.setAttribute("text-anchor", "end"); grid.append(l, x); return { f, l, x }; });
function draw(t) {
  const m = yMax(t); let d = "";
  ticks.forEach(({ f, l, x }) => { const y = Y0 - (Y0 - Y1) * f; l.setAttribute("y1", y); l.setAttribute("y2", y); x.setAttribute("y", y - 10); x.textContent = Math.round(m * f); });
  const n = Math.max(2, Math.round(t * 30));
  for (let i = 0; i <= n; i++) { const s = (t * i) / n; d += (i ? "L" : "M") + px(s).toFixed(1) + " " + py(data(s), m).toFixed(1); }
  document.getElementById("line").setAttribute("d", d);
  document.getElementById("area").setAttribute("d", d + "L" + px(t) + " " + Y0 + "L" + X0 + " " + Y0 + "Z");
  const dot = document.getElementById("dot"); dot.setAttribute("cx", px(t)); dot.setAttribute("cy", py(data(t), m));
  document.getElementById("num").textContent = Math.round(data(t));
}
const tl = gsap.timeline({ paused: true }), clock = { t: 0 };
tl.to(clock, { t: D, duration: D, ease: "none", onUpdate: () => draw(clock.t) }, 0);
draw(0);
window.__timelines["main"] = tl;
</script>
```

Add a `<head>` with GSAP (`https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js`), the Inter font from Google Fonts, and `html,body{margin:0;width:1080px;height:1920px;overflow:hidden}`. Add a kicker, captions and pins on the same timeline.

## Parameters to expose

`format` · `duration` · `chart` · `tone` · `data` (array or function) · `units` · `pins` (time, label, colour) · `captions` (time, text) · `rescaleAt`.

## Avoid

- Every number on screen must come from the user's data or a cited source. Keep a small facts list (number, source) next to the composition. Anything illustrative is labelled as such on screen.
- Invented or "illustrative" numbers presented as real.
- Several highlighted series at once, or rainbow palettes.
- Pale grey labels (they fail contrast checks and are unreadable on phones).
- Chart junk: 3D bars, heavy gridlines, legends when a direct label would do.
- Axes that jump without easing. Rescale smoothly so the viewer sees the change.
- Pins or captions covering the line at its key point.

## Failure modes

| Looks like | Cause | Fix |
|---|---|---|
| Line jumps or flickers on render | drawn from wall-clock time or per-frame randomness | draw only from the clock `t` in `onUpdate` |
| Pin labels overflow their pills | pill width guessed too small | width ≈ 36 + chars × 17 (× 23 for all caps) at 28 px, or measure after fonts load |
| Kicker and counter overlap | both positioned too close | leave 30+ px between the kicker baseline and the counter top |
| Surprise lands flat | no rescale, no pin, no caption change | stack all three within 0.5 s |
| Counter text wobbles | proportional digits | `font-variant-numeric: tabular-nums` |
| Contrast check fails on ticks | label colour too light | ticks `#5b6270` on light, `#9fb0c8` on dark |

## Validate

```bash
npx hyperframes check
npx hyperframes snapshot --at <start, each pin, mid-rescale, end>
npx hyperframes render -o renders/<name>.mp4
```

- [ ] numbers on screen match the data at those times
- [ ] the rescale is smooth and the labels stay readable during it
- [ ] pins and captions never cover the line's key point
- [ ] all text inside the safe area; contrast check passes
- [ ] the final frame states the takeaway

## Self-critique before the final render

Score the snapshot sheet 1–10 on: hook (first second), readability at phone width, motion quality, composition, accuracy, and the "muted test" (can a viewer summarise it in one sentence with no sound?). Fix only what scores 7 or below, re-snapshot, and repeat until everything is 8 or above. If you can, have a separate read-only pass do the scoring, so you aren't grading your own work.

| Don't | Instead |
|---|---|
| Crossfade between two busy layouts | exit the old content, then bring in the new, or carry one object across |
| Make several things move at once | stagger, one focus per moment |
| Fill pauses with floating or wobble | hold still, or let the character act |
| Add particles, rainbow gradients or 3D flips for "energy" | add a stronger event: a reveal, a hit, a camera move |
| Rush text to fit the time | cut words |

## Deliver

- Poster: the settled final chart frame, baked in as frame 0: `ffmpeg -ss <t> -i renders/<name>.mp4 -frames:v 1 poster.jpg`, then `ffmpeg -i renders/<name>.mp4 -i poster.jpg -filter_complex "[0:v][1:v]overlay=enable='eq(n,0)'" -c:a copy renders/<name>-final.mp4`.
- A caption with the key number and the source of the data.
- Tell the user the data beats and which numbers or pins to change for a revision.

## Study these

- @kimmonismus, "A Short History of AI", a timeline with milestone counters made in Remotion: https://x.com/kimmonismus/status/2102844654169575547
- @VincentWei93, Anthropic's rise as data-viz motion graphics with audio hits on the numbers: https://x.com/VincentWei93/status/2103381720410333314
- @sonnylazuardi, 81 years of Indonesian history as a 42,000-point dot map: https://x.com/sonnylazuardi/status/2103511590884815282
- @aakashgupta, a compensation offer broken down with stacked bars and counters: https://x.com/aakashgupta/status/2102998741359988832
- Ideas adapted (not copied) from the HyperFrames motion doctrine and faceless-explainer skills, JohnHeibel/ClaudeAnimationBase's animation guide, howseen-ai/claude-motion-design's critique loop, and latent-spaces/brag.
