---
name: springs
description: "Make motion feel physical with closed-form springs from lib/motion.js: presets, ζ/Hz params, track(), loopTrack loops, named easing curves, anticipation, squash. Use for 'feels linear', 'add bounce', 'easing to springs'."
argument-hint: "[file, scene or element]"
---

# Springs (course step 08)

Cheap motion eases from A to B on a fixed curve. Motion with mass accelerates, overshoots a hair and settles. The
springs in `lib/motion.js` are closed-form step responses, so they stay a pure function of time: frame 812 renders
without simulating frames 0 to 811, and `seek(t)` stays deterministic.

Import from the film project's `lib/motion.js` (paths relative to the file: `../lib/motion.js` from `film/film.js`,
`../../lib/motion.js` from `film/scenes/*.js`). Full preset numbers live in
`${CLAUDE_SKILL_DIR}/references/presets.md` ([references/presets.md](references/presets.md)).

## 1. API

| Function | Returns | Notes |
|---|---|---|
| `sp(t, preset = 'default')` | 0 to 1 | the everyday call; `t` is time since release (`lt - 0.2`), 0 before release |
| `spring(t, k, d, m = 1)` / `springVel(...)` / `springPV(...)` | x / v / `[x, v]` | raw k/d form; exact under-, critically and overdamped |
| `SPRINGS` | `{ snappy, default, heavy, playful }` | `{k, d}` pairs, see the table below |
| `resolveSpring(p)` | `{k, d}` | accepts a preset name, `{k, d}`, `{duration, bounce}` or `{zeta, freq}` everywhere a spring is expected |
| `springFromFeel({ duration, bounce })` / `feelFromSpring({k, d})` | `{k, d}` / `{duration, bounce}` | designer-friendly parameters (Apple convention) |
| `springFromRatio({ zeta = 0.7, freq = 2 })` / `ratioFromSpring(spec)` | `{k, d}` / `{zeta, freq}` | damping ratio ζ and natural frequency in Hz, the way briefs state springs ("ζ 0.6") |
| `track(t, keys, spring = 'default')` / `trackVel(...)` | value / velocity | `keys = [[time, value], ...]` sorted; one spring per change, summed; an optional third element overrides the spring for that change (`[2.4, 420, 'heavy']`) |
| `loopTrack(t, keys, dur, spring = 'default', cycles = null)` | value | seamless loops. Key times are within one cycle, `0..dur`, and are not wrapped (outside throws). Last value must equal the first. A key exactly at `dur` is the seam change |
| `indicator(t, stops, { width = 120, lead = 'snappy', trail = {k: 140, d: 22} })` | `{ left, right }` | tab indicator that stretches: edges on different springs |
| `swapAlpha(t, tIn, tOut, { inDelay = 0.08, inDur = 0.12, outLead = 0.1, outDur = 0.1 })` | 0 to 1 | text inside a morphing box: in after the morph starts, out before the next |
| `stagger(i, step = 0.03)` | seconds | delay for item `i` |
| `stepTime(t, rate = 12)` | stepped `t` | "on twos" for drawings only, never camera or global fades. Pass `c.frameLt` (or `c.frameT`), the output frame's time, for a hard cut between steps; `c.t` / `lt` are subframe times and blend the two steps on the frames where a step changes |
| `loopT(t, dur)` | `t` wrapped into `[0, dur)` | time wrap; not enough on its own for springs (use `loopTrack`) |
| `settleTime(spring, eps = 0.01)` / `overshoot(spring)` | seconds / fraction | plan holds and cut points |
| `tween(t, t0, dur, from = 0, to = 1, ease = 'outQuint')` | value | a timed move on a named curve; holds `from` before `t0` and `to` after |
| `EASES`, `resolveEase(e)`, `cubicBezier(x1, y1, x2, y2)` | p => y | `outExpo`, `outQuint`, `outCubic`, `outBack`, `inOutQuart`, `inOutCubic`, `inExpo`, `inQuint`, `linear`; exact CSS curves |
| `windup(t, at, { lead = 0.18, depth = 0.1, spring = 'playful' })` | value | anticipation: dips the other way for `lead` s, then springs 0 → 1 from `at` |
| `squash(s, { preserve = 'area' })` | `{ along, across }` | squash and stretch that keeps the mass (`'area'` 1/s, `'volume'` 1/√s) |
| `loopWave(t, dur, cycles = 1, phase = 0)` | −1 to 1 | a sine with whole cycles per loop (refuses a fraction: the seam would jump) |
| `holdTime(words)` / `framesPerBeat(fps, bpm)` | seconds / frames | 0.3 s per word + 0.5 s; fps × 60 / bpm |
| `easeOutCubic`, `easeInOutCubic` | 0 to 1 | only for non-physical fades (opacity); never for things that move |

## 2. Presets

| Preset | k / d | Damping ratio | Overshoot | Settles (1%) | Use for |
|---|---|---|---|---|---|
| `snappy` | 320 / 30 | 0.839 | 0.79% | 0.24 s | buttons, toggles, leading edges, cursor |
| `default` | 170 / 26 | 0.997 | 0 | 0.51 s | cards, containers, camera |
| `heavy` | 90 / 20 | 1.054 | 0 | 0.78 s | big type, 3D objects, logo lockups |
| `playful` | 220 / 14 | 0.472 | 18.6% | 0.59 s | mascots, stickers |

House rule: tiny overshoot on UI (`snappy`), none on type (`default` or `heavy` for scale and position of hero text),
`playful` only where the overshoot is the joke. Springs for things with mass; a named curve (`tween`, `outExpo` in,
`inExpo` out, `inOutQuart` for the camera) where the landing frame is part of the choreography. Entrances ease out,
exits ease in and run 40 to 50% shorter. Adjective-to-number tables (durations, ζ ranges, hierarchy, animation
principles, beats and frames, loops, accessibility): [references/numbers.md](references/numbers.md). Full numbers, feel conversions and formulas:
[references/presets.md](references/presets.md).

## 3. Recipes

Inside a scene `draw(g, lt, c)`: `lt` is the time since the scene started, `c.t` the film time, `c.L` the layout,
`c.brand` the brand tokens, `c.grid` the beat grid, `c.film.dur` the film length (`c.dur` is the scene length). With
motion blur on, `c.t` and `lt` are the subframe time being painted (motion blurs by itself); `c.frameT` / `c.frameLt`
are the output frame's time and `c.frame` its index, identical for every subframe. The snippets assume
`const { t, L } = c;` and imports from `lib/motion.js`, `lib/draw.js` and `lib/rng.js`.

One-shot entrance (release 0.15 s into the scene):

```js
const s = sp(lt - 0.15, 'snappy');
withTransform(g, { x: L.cx, y: lerp(L.cy + 80 * L.u, L.cy, s), s: lerp(0.92, 1, s) }, () => { /* draw */ });
```

This one starts visible: position and scale are at their start values while the spring is 0, so frame 0 is not empty.
It would be empty if `s` drove the only thing on screen through opacity or a clip. For a scene that is on screen at
frame 0 (the hook), open mid-action by releasing the spring BEFORE the scene: `sp(lt + 0.3, 'snappy')`, or
`kinetic(g, 'MAKE IT MOVE.', x, y, lt + 0.3, { ... })`, or `kinetic(..., { delay: -0.3 })`. At `lt = 0` the type is then 0.3 s
into its rise instead of not drawn (`kinetic` skips every glyph whose spring is still at 0). The critique flags an empty
frame 0 as a P0 (`frame 0 is nearly empty`).

A value with several targets (never restart a spring; add one per change):

```js
// cursor x in logical px: rests at 200, moves at 1.0 s and 2.4 s, returns at 3.6 s
const cx = track(t, [[0, 200 * L.u], [1.0, 640 * L.u], [2.4, 420 * L.u], [3.6, 200 * L.u]], 'snappy');
```

The first key's time is ignored: its value is the rest value from the start. Every change after that starts its own
spring at its own time, and the sum stays continuous in position and velocity even when a new target arrives before
the last one settled.

One-shape morph (container never cuts; every property is a track on the same key times):

```js
const K = [0, 1, 2, 3].map((n) => c.grid.bar(n));       // state changes on downbeats, from the grid
const w = track(t, [[K[0], 320], [K[1], 120], [K[2], 760], [K[3], 320]].map(([k, v]) => [k, v * L.u]));
const h = track(t, [[K[0], 96], [K[1], 120], [K[2], 480], [K[3], 96]].map(([k, v]) => [k, v * L.u]));
const r = track(t, [[K[0], 48], [K[1], 60], [K[2], 32], [K[3], 48]].map(([k, v]) => [k, v * L.u]));
fillRoundRect(g, L.cx - w / 2, L.cy - h / 2, w, h, Math.max(0, r), c.brand.colors.fg);
withAlpha(g, swapAlpha(t, K[1], K[2]), () => ring(g, L.cx, L.cy, 36 * L.u, sp(t - K[1] - 0.1), { color: c.brand.colors.accent }));
```

Colors: spring a 0-to-1 progress and mix with `mixColor(a, b, p)` from `lib/draw.js` (it clamps `p`), or, for a color
with several targets, track each channel and clamp to 0 to 255. Radius and sizes that can overshoot below zero need
`Math.max(0, ...)`.

Tab indicator that stretches between stops:

```js
const { left, right } = indicator(t, [[0, x0], [1.5, x1], [3.0, x2]], { width: 140 * L.u });
fillRoundRect(g, left, y, right - left, 6 * L.u, 3 * L.u, c.brand.colors.accent);
```

Seamless loop (the value and its velocity match across the seam):

```js
// 6 s loop: a at rest, b at 1.5 s, c2 at 3 s, back to a at 4.5 s
const x = loopTrack(t, [[0, a], [1.5, b], [3, c2], [4.5, a]], c.film.dur, 'default');
// the same loop with the return as the seam change: the last key sits exactly at dur
const y = loopTrack(t, [[0, a], [1.5, b], [3, c2], [c.film.dur, a]], c.film.dur, 'default');
```

Rules of `loopTrack` (checked against `lib/motion.js`):

| Rule | Detail |
|---|---|
| key times stay in `0..dur` | they are cycle-relative and never wrapped; a time outside throws `loopTrack: key <i> time <t> is outside 0..<dur>` (a hair past `dur` from grid arithmetic is tolerated) |
| the first key is the rest value | its time is ignored (it must still lie in `0..dur`); the value is what the first change starts from |
| the last value equals the first | otherwise it throws `the last value (...) must equal the first (...)` |
| a key at `dur` is the seam change | the spring starts at `t = 0` of the next cycle: frame 0 (= frame `dur`) shows the pre-seam value and eases to the first value. It equals writing `[[0, pre], [0, post], ...]`. Write the seam change once, at `0` or at `dur` |
| a change just before `dur` may still be moving at frame 0 | the sum is exactly periodic, so position and velocity match across the seam whatever the timing. To open on a still frame, keep the last change at least `settleTime(preset)` before `dur` (0.51 s for `default`) |
| cycles | the number of summed previous cycles follows the settle time and the latest key, so late keys are safe; `cycles` overrides it |

Plain `loopT` plus `track` jumps at the seam because the springs released near the end are still moving at `t = 0`.
`loopTrack` also sums the springs from previous cycles (enough of them to settle) and gives, with keys
`[[0, 0], [2, 100], [4, 40], [6, 0]]` and `dur` 6, the values 0.001 / 99.997 / 40.002 at `t = 1 / 3 / 5`. Check the seam
in `out/review/<fmt>/loop.png` after `npm run critique`: `|last - first|` should look like one normal step and
`|end - first|` (the unwrapped end state) should be black.

Staggered pops (per-element seeds, never one shared stream):

```js
for (let i = 0; i < n; i++) {
  const r = rngFor('tile', i);
  const s = sp(lt - stagger(i, 0.035) - range(r, 0, 0.06), 'playful');
  // draw tile i scaled by s
}
```

Kinetic type: `kinetic(g, str, x, y, lt, { size, family, weight, color, spring: 'snappy', stagger: 0.035, rise: 0.6, by: 'char' | 'word',
mask, delay, alpha, align, baseline, style, tracking })`. `family` defaults to `brand.fonts.display` and `weight` to the nearest
weight the family has registered, so leave both out unless the design needs another face. `mask: true` clips the run to its
line box so glyphs rise from behind an edge instead of fading; `delay` shifts the whole run (negative opens mid-action).
For hero type, pass `spring: 'default'` or `'heavy'` when the rise is large enough for 0.8% overshoot to show.
Multi-line copy: `wrapText(g, text, maxW, font(size, family))` returns the lines (never cutting inside a Hangul syllable);
draw them with `y + i * 1.2 * size` or more and give each line its own `delay`.

Drawings on twos (hand-drawn look): `const td = stepTime(c.frameLt, 12)` for the drawing's own animation (the output frame's
time, so each step is a hard cut even with motion blur on); keep camera moves, fades and UI on continuous `lt`, or pans
step 12 times a second and read as lag.

## 4. Refactor a whole film

Use the prompt template in the project: read `prompts/refactor-springs.txt` and follow it (or paste it as a task). It
replaces every linear interpolation and stock easing that moves something with presets, `track()`, `loopTrack()`,
`indicator()` and `swapAlpha()`, keeps the timing, and reports each change. Then:

1. `npm run lint` (must be clean).
2. `npm run stills` and `node tools/critique.mjs --strip-at <t>` at the busiest moment: `strip.png` shows 12
   consecutive frames, which exposes pops, restarts and slides that a contact sheet hides.
3. Log the change in the next critique round (`/motion-studio:critique-loop`).

## 5. Mistakes to catch

| Mistake | What it looks like | Fix |
|---|---|---|
| restarting a spring at each target (`sp(t - tNew)` from the old value) | velocity snaps to 0, a visible kink | `track()` with all targets |
| hand-rolled sums of springs with their own start values | jumps when two changes overlap | one `track()` per value; per-change presets go in the key's third element |
| `loopT` alone on a spring value | jump at the seam | `loopTrack()` with keys in `0..dur` and last value == first |
| overshoot on type | text wobbles, reads cheap | `default` / `heavy` for type |
| `playful` on UI chrome | toy-like interface | `snappy` for UI |
| spring on opacity only while position is linear | fades nicely, slides cheaply | spring the position; opacity can follow `easeOutCubic` |
| everything on the same preset and delay | mechanical, no hierarchy | lead with `snappy`, follow with `default`, `stagger()` the rest |

Next: `/motion-studio:sound-design` to lock the motion to the beat, then `/motion-studio:critique-loop`.
