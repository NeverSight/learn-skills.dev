---
name: motion-quality
description: Hard-won, measured rules for animating text and shipping registry components in snapcn. READ THIS BEFORE you animate a scale or transform on text, pick an easing curve, add will-change, set a transformOrigin, split a word into per-letter spans, or touch a component that has a rendered demo. Explains why scaled text looks "stuck" and "shaky" in a browser (glyph pixel snapping, font hinting), which fixes are real and which are cargo cult, why aggressive ease-out curves freeze on a frame clock, and how to verify an animation by measuring rendered frames instead of eyeballing it. Triggers - scale animation, zoom text, transform, transformOrigin, easing, cubic-bezier, ease-out, will-change, jitter, judder, stutter, wobble, blurry text, text not smooth, letters stuck, Remotion component, registry component, preview looks wrong.
---

# Motion quality

Every rule here was paid for. Each one is a bug that shipped, was measured on
rendered frames, and cost a user their afternoon. The numbers are real — they are
in the file so you cannot talk yourself out of the rule.

---

## Rule 0 — you cannot see a sub-pixel bug. Measure the frames.

"It looks fine" is not a claim about a frame-accurate animation. Render the frames
and measure them. Four checks catch almost everything:

| what | why it works | what a failure looks like |
| --- | --- | --- |
| **Consecutive frames where nothing is animating must be byte-identical** | the style is unchanged, so the pixels must be | non-zero diff = the renderer is non-deterministic |
| **Under a monotone scale, the ink's vertical centroid must move monotonically** | it is a pure affine map | direction reversals = the type is snapping to the pixel grid |
| **`ink area / width²` cannot change under a scale** | it is a shape invariant of a rigid shape | drift = the *glyph outlines* are changing shape (hinting) |
| **No frame should move < 0.5px while it is supposed to be animating** | sub-pixel motion rasterises to an identical frame | a run of them = the animation is visibly frozen |

Recover sub-pixel geometry from the antialiasing: `alpha = (pixel - bg) / (fg - bg)`,
then take intensity-weighted centroids. That is accurate to ~0.01px, which is far
finer than the bugs you are hunting.

**All four checks are code now — stop re-deriving them by hand.** `lib/motion-check`
is the measurement library (`settleFrame`, `holdIsStill`, `centroidMonotonic`,
`shapeInvariant`, `noFrozenFrames`, `edgeBleedDelta`, `detailCoverage`), pure and
tested on synthetic rasters; `lib/motion-check/capture.ts` renders a component's
frames straight into memory (one bundle, one browser, PNG buffers, no mp4 — h264
quantises away the very antialiasing the alpha recovery reads).

```bash
pnpm run motion:measure --only=text-build   # -> registry/__measured__.json
```

It also answers the two questions no test could: when a component **settles**
(a beat still animating when the next fades in over it — @remotion/transitions
overlaps 18 frames), and how much **copy** it can hold before the line runs off
the frame.

**If someone says it is still not smooth and your metric says it is fixed, your
metric is measuring the wrong thing.** Do not argue with them. Go find the metric
that reproduces what they see. Two separate bugs in this repo were missed exactly
this way.

---

## The two bugs that make scaled text look cheap

Browsers do **not** scale text the way they scale an image. They re-shape and
re-rasterise every glyph at the new size. Two things go wrong, they are
independent, and you need both fixes.

### 1. "Stuck" — glyph origins snap to whole pixels vertically

The rasteriser quantises each glyph's origin: quarter-pixel precision
horizontally, and **none at all vertically** — it rounds to a whole device pixel
(Skia, `SkGlyphPositionRoundingSpec::HalfAxisSampleFreq`). So a scale that *moves
the baseline* makes the type climb the pixel grid in whole-pixel jumps. At the
slow ends of an eased curve the baseline drifts a fraction of a pixel per frame,
which rounds to nothing for several frames and then to a whole pixel all at once.
Sit still, jump, sit still.

**Fix: pivot the scale on the baseline.** Then the baseline's device Y never
changes and there is nothing to snap.

```tsx
// measure it — never guess it from a line-height ratio
<span ref={lineRef} style={{ transformOrigin: `0% ${baseline}px`, scale }}>
  {…}
  {/* an empty zero-sized inline-block sits ON the baseline */}
  <span ref={baselineRef} style={{ display: "inline-block", width: 0, height: 0 }} />
</span>
// baseline = baselineRef.current.offsetTop
```

Measured, sweeping `transformOrigin` across a linear 1.6x → 1x ramp:

| pivot | vertical judder | direction reversals (40 frames) |
| --- | --- | --- |
| `50%` (the middle) | 0.284px | **29** |
| 74% | 0.273px | 6 |
| **80% (the baseline)** | **0.014px** | **0** |
| 90% | 0.284px | 0 |

A sharp minimum exactly on the baseline and nowhere else. Per-letter transforms
need the same pivot — `50% 100%` is the *bottom of the box*, which sits below the
baseline by the descent, so it drags the letter's baseline as it scales.

### 2. "Shake" — hinting boils the letterforms

Hinting bends each glyph's outline so its stems land on whole pixels. As the size
slides, every stem re-snaps to a different grid and **the letters literally change
shape frame to frame.** They boil.

**Fix: `text-rendering: geometricPrecision`.** It turns hinting off and renders the
outline as it actually is.

Measured over a fall-back, using the shape invariant that cannot change:

| | shape drift |
| --- | --- |
| hinting on (default) | **3.41%** |
| `geometricPrecision` | **0.22%** |

Fifteen times steadier. The type reads very slightly softer without hinting. That
is **not blur** — it is the absence of a lie, and it is what every professional
motion tool does with type. It also forces sub-pixel glyph positioning on, which
Blink otherwise only enables above a device scale factor of 1 — and a Remotion
render is exactly 1, so on Linux (where renders actually run) *both* axes snap to
whole pixels without it.

---

## `will-change: transform` — right for the Player, wrong for the render

It hands the scale to the compositor, which resamples a **bitmap** instead of
re-rasterising real type. That is the correct trade in one place and the wrong
trade in the other:

- **A render** is spread across parallel browser tabs, and each tab inherits a
  stale raster from whatever scale *it* drew last. Measured: frames whose style was
  *byte-identical* came out as **4 different rasterisations**, and ~9,000 pixels
  changed per frame during a hold where nothing was moving. The text shimmers while
  standing still. And the type is a rescaled texture, not type.
- **The Player** is one continuous tab with a hard ~8ms frame budget at 120Hz.
  Re-shaping a line of type at a brand-new size every frame is the most expensive
  thing you can ask a browser to do per frame. Measured on a single continuous tab:
  0.016px judder, **no loss of sharpness at all**.

So gate it:

```tsx
import { getRemotionEnvironment } from "remotion";
...(getRemotionEnvironment().isRendering ? null : { willChange: "transform" as const }),
```

### Cargo cult — these are not fixes

`translateZ(0)`, `translate3d(…, 0)`, `backface-visibility: hidden`,
`perspective(1px)`, `rotateY(0.01deg)`, `filter: blur(0px)`. Every one is the same
layer-promotion trick wearing a different hat, and they buy smoothness by turning
your type into a bitmap. `-webkit-font-smoothing: antialiased` does not touch glyph
positioning at all. Animating `font-size` instead of `scale` is *worse* — it
reflows every frame **and** still hits glyph snapping.

---

## Easing on a frame clock

Quint-out and expo-out — the curves everyone reaches for — cover 99% of their
travel in the first third and then crawl. On a frame clock that crawl is not a
graceful settle, it is **identical frames**.

Measured on a 50px rise at 30fps with `cubic-bezier(0.22, 1, 0.36, 1)`: **5 of its
14 frames moved less than half a pixel each.** They rasterised identically. The
word visibly stopped dead partway up and waited.

> **A settle worth one frame is a settle. A settle worth five frames is a freeze.**

Use a *moderate* decelerate — `cubic-bezier(0.2, 0.6, 0.35, 1)` — and check every
curve against the < 0.5px test above. Curves should still arrive at a standstill;
they just must not spend frames on travel you cannot see.

---

## Layout gotchas that will bite you

- **A trailing space inside an `inline-block` gets stripped.** It sits at the end
  of that box's line and CSS removes it, so per-word spans render as
  `Noextracharge`. Put the separator *between* the spans, not inside them.
- **`offsetWidth` / `offsetLeft` are layout px** — unaffected by transforms, which
  is exactly why they are the right tool for measuring a scene you are about to
  transform. But `offsetTop` is **rounded to an integer**; use
  `getBoundingClientRect()` when you need sub-pixel (and remember it *is* affected
  by transforms).
- **Measure once, behind `delayRender()`**, and `continueRender()` only after the
  measurement has re-rendered — otherwise frame 0 is captured with the wrong
  geometry.
- **Transforms do not reflow.** Animate `scale` / `translate` / `opacity` and
  nothing else, so the baseline is fixed and there is no layout shift.

---

## The live Player lies. Some components must ship a rendered demo.

A `<Player>` is not a video — it is React re-rendering on `requestAnimationFrame`
in real time. A 30fps composition on a 120Hz display must hold every frame for
exactly four refreshes; a frame that misses its budget is **shown for the wrong
length of time**, and the eye reads that as sticking and shaking. It is worst
during slow smooth motion, which is exactly where a title reveal lives.

For those scenes the preview makes a *correct* component look broken. The answer
is to stop previewing an approximation: add the slug to `RENDERED_DEMOS` in
`lib/rendered-demos.tsx` and the site plays the real mp4 instead. See CONTRIBUTING.md.

**If you change a component in `RENDERED_DEMOS`, re-render its demo in the same
change** — `pnpm run render:previews --only <slug>`. Nothing catches a stale one.

Watch for **identifier vs. label** when wiring previews: `PreviewStage` takes both
`slug` (the registry key) and `name` (a human label). Passing "Text Swell" where a
slug was wanted made the lookup miss silently and fall back to the stuttery Player,
and it looked exactly like the feature was never wired.

---

## A render has no global CSS. The site does.

A Remotion bundle loads none of the app's stylesheets, so a component can be
verified frame by frame in an mp4 and still be **invisible in the app that installs
it**. This is not hypothetical — it shipped:

Tailwind's preflight sets `img, video { max-width: 100% }`. It applies to `img` and
**not** to `svg`. A mark placed in an absolutely-positioned box at `left: 100%` has
*(containing block − left) = 0* available width, so the box is shrink-to-fit and
asks its content for a minimum. An `<svg width={58}>` answers "58" and holds it
open. An `<img>` under preflight answers **"I can be 0"** — the box collapses, 100%
of 0 is 0, and the image renders **zero pixels wide**. The rendered mp4 was perfect.
The docs page was a blank white rectangle, and the `<Player>` sat there looking
stuck.

So: **when a component takes an image, verify it on the site, not only in a render.**
Load the page and read back the element's real geometry —
`getBoundingClientRect()` on the `<img>` said `0 x 17`, which named the bug
instantly after a lot of guessing did not. And defend the component: `max-width:
none` on any image you size yourself, `width: max-content` on any shrink-to-fit box
you position at an edge.

---

## Perspective rushes fill the frame in one frame unless you plan for it

Under `scale = 1 / (1 - travel)`, *every* size threshold near the top is crossed
within a frame or two of every other one. Gate a "now cover the screen" event on the
mark exceeding the frame **diagonal** and you get 23% covered → 91% covered in a
single frame: a cut, not a fill. Open the gate earlier — when the mark is merely
*taller than the frame* — and the same event gets five or six frames to happen in,
without ever being able to start while the mark is small.

And a logo **cannot cover a frame by growing**: scaling it scales its holes by
exactly as much. Measured on a 28%-ink mark, solid-ink coverage needed **396x**. The
ending has to be the mark's colour flooding out from inside it — and it must be a
**shape** (a hard-edged disc born inside the mark's own ink), never an opacity ramp.
Fading a full-frame rectangle up leaves a half-transparent wash lying over the
backdrop for several frames, and there is no reading of that except "the screen faded
to blue".

---

## Repo gotchas

- **Never run a formatter over `registry/snap-cn/registry.json`.** It reflows the
  whole file and buries your one entry in hundreds of lines of noise.
- **`pnpm run registry:build` rewrites every `public/r/*.json`**, not just yours.
  If other components have uncommitted source edits, their outputs get regenerated
  too. Check `git status` and say so.
- **A re-rendered demo does not mean a re-rendered demo.** `public/demos/<slug>.mp4`
  keeps the same filename forever, and a browser that already has one will keep
  replaying it — `<video>` caches hardest of all. That cost *three* rounds of "you
  didn't fix it" against builds that no longer existed. It is fixed properly now:
  `render:previews` hashes every demo into `lib/demo-manifest.json` and
  `renderedDemoSrc()` puts that hash in the URL (`?v=<hash>`), so a re-rendered demo
  is a **different address** and a stale one is not something a cache can serve.
  `next.config.ts` also sends `no-store` for `/demos/*` in dev.
  **If you re-render a demo by hand, re-run `render:previews` so the manifest moves
  with it** — a stale manifest is a stale demo. And when someone says "you didn't
  fix it": check what is on disk (`md5`) and what the server actually serves before
  you believe them, and before you disbelieve them.
- **Match the reference, do not eyeball it.** When a user gives you a reference
  video, extract the frames and measure the actual curves (`ffmpeg` + threshold the
  ink + track bounding boxes). Every choreography detail in `text-reveal` and
  `text-swell` — the forward push, the two clocks, the letter swell, which words
  bounce — came out of measuring the reference, and every one of them was invisible
  to the naked eye.
