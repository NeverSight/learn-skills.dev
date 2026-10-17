---
name: motion-animate
description: The motion vocabulary that separates premium animation from AI slop — text pop-blur-fade, sequential staggers, always-moving eased cameras, object entrances, and the timing/easing tables behind them. Includes ready code for Remotion (interpolate/spring) and HyperFrames (GSAP). Use when animating designed frames, when motion "feels stiff", "bouncy", "jittery", "too fast", "too uniform", or when writing any timing/easing code for video.
---

# motion-animate

Design decides whether a frame is good. **Motion decides whether it looks expensive.** The same composition animated with linear easing and simultaneous entrances reads as generated; animated with the vocabulary below it reads as authored.

Engine recipes: Appendix A, Appendix B.

## The four laws

1. **Nothing is linear.** Every property moves on an ease. Linear motion does not exist in the physical world and the eye knows it instantly.
2. **Nothing enters at once.** Elements arrive in a deliberate order with 60–120ms between them. Simultaneous entrance is the loudest motion tell.
3. **The camera is never fully still.** A slow continuous push or drift under every composition. Static frames read as slides.
4. **Nothing is metronomic.** Vary durations and cut spacing. Uniform 1s beats feel automated no matter how good each beat is.

## Timing table

Values at 30fps; scale for 60fps. Times in ms.

| Element | Duration | Stagger | Ease |
|---|---|---|---|
| Word in a text line | 400–550 | 60–90 | `out-expo` / `power3.out` |
| Text line (as a unit) | 500–650 | 120–180 | `out-cubic` / `power2.out` |
| Icon / small UI element | 350–450 | 80–120 | `out-back` (overshoot ≤1.06) |
| Panel / card | 550–700 | 140–200 | `out-quint` / `power4.out` |
| Hero object scale-in | 700–900 | — | `out-expo` |
| Hero object slide-in | 650–850 | — | `out-quint` |
| Line / stroke draw | 600–1000 | — | `in-out-cubic` |
| Camera push (per scene) | full scene length | — | `out-sine`, or linear-ish if very slow |
| Exit (any element) | 250–350 | 40–60 | `in-cubic` |

**Exits are always faster than entrances**, roughly half. A symmetric out-animation feels sluggish.

## The core moves

### Text — pop-blur-fade, word by word
The signature move. Every property animates together, per word, staggered.

```
y:       +18px → 0
blur:    12px  → 0
opacity: 0     → 1
ease:    out-expo,  duration 480ms,  stagger 70ms
```

Optionally add `scale: 0.96 → 1`. Do **not** add rotation. Do not bounce.

For a long line, stagger by **word**, not by character — character stagger reads as a typewriter gimmick and takes too long. Reserve character stagger for a single short accent word.

### Accent word
Runs the same move but **delayed 120–200ms after its neighbours** and given one extra property — a color shift, a scale bump to 1.04, or a highlight bar wiping in behind it. It should land last and land differently.

### Icons and UI
Pop-fade: `scale 0.7 → 1`, `opacity 0 → 1`, `out-back` with overshoot capped at 1.06. Anything past 1.1 reads as a cheap bounce.

Sequential rule: **the anchor element enters first**, then its dependents. A card enters, *then* its icon, *then* its label. Never the reverse, never together.

### Panels / cards / glass
`y: +40 → 0`, `opacity 0 → 1`, `out-quint`, 600ms, staggered 160ms across a stack. Add a light-sweep highlight that runs across the panel 150ms *after* it lands — the panel arrives, then it catches the light.

### Hero object
Two options, pick by archetype:
- **Scale-in**: `scale 1.25 → 1.00` with `rotate 3° → 0°`, `out-expo`, 800ms. Feels like it settles into place.
- **Slide-in**: from off-frame with a 2° tilt that resolves to 0°, `out-quint`, 750ms. Feels delivered.

The cast shadow and clipped texture must be **parented to the hero** so they move with it. Un-parented shadows sliding independently is a hard failure.

### Stroke / line draw
Animate path length 0 → 100%, `in-out-cubic`, 600–1000ms. Ease in *and* out — a draw that starts at full speed looks mechanical. Use to connect a label to a subject, underline an accent word, or trace a chart.

### Camera
Under every composition, one of:
- **Push in**: `scale 1.00 → 1.08` over the full beat, `out-sine`.
- **Push out**: `scale 1.12 → 1.00`, faster at the start, settling.
- **Drift**: `x` or `y` translate of 2–4% over the beat.

Anti-jitter contract:
- Animate a **wrapper element**, never the element that owns layout or clipping.
- Use `transform` only — never `top`/`left`/`width`/`height`.
- Scale up the moving layer ~6% beyond frame so edges never reveal.
- Set `will-change: transform` and force GPU compositing.
- Keep total travel small. Big camera moves amplify every rounding error.

### Transitions between beats
- **Hard cut** masked by an SFX hit — the default. Crossfades between designed frames muddy both.
- **Scale-through** — an element scales up to fill frame and the next scene is revealed inside it.
- **Wipe by a shape** — a circle or panel scales past frame edge, carrying the next scene.

Do not crossfade two designed compositions. Do not use a stock transition preset.

## Forbidden

- Linear easing on anything visible.
- Bounce overshoot >1.1 (exception: an intentionally playful SaaS/product style, and then consistently).
- All elements entering on the same frame.
- Uniform beat lengths across an edit.
- `repeat: -1` or any infinite loop — renders are frame-sampled and must be deterministic.
- `Math.random()`, `Date.now()`, or network fetches inside a composition. Same input must produce the same frame every time.
- Motion applied to a wrapper the framework already controls (see Appendix B §clip rule).

## Self-check

Scrub the render at 0.25× speed. Ask:
- Does anything start and stop abruptly? → missing ease.
- Does everything land together? → missing stagger.
- Does the frame ever sit dead still? → missing camera.
- Do consecutive beats feel like a drumbeat? → durations too uniform.
- Do edges of a moving layer ever reveal? → not over-scaled.

---

# Appendix A — Remotion recipes


Frame-based, deterministic by construction. All timing derives from `useCurrentFrame()`.

## Helper: time in ms, not frames

Authoring in frames hardcodes your fps. Convert.

```tsx
import {useVideoConfig, useCurrentFrame, interpolate, Easing} from 'remotion';

const useMs = () => {
  const {fps} = useVideoConfig();
  return (ms: number) => (ms / 1000) * fps;
};
```

## Easing map

The names in the timing table, in Remotion terms:

```tsx
Easing.out(Easing.exp)                    // out-expo
Easing.out(Easing.cubic)                  // out-cubic
Easing.out(Easing.quad)                   // out-quad
Easing.out(Easing.poly(4))                // out-quint-ish
Easing.inOut(Easing.cubic)                // in-out-cubic
Easing.out(Easing.sin)                    // out-sine
Easing.in(Easing.cubic)                   // in-cubic  (exits)
Easing.bezier(0.16, 1, 0.3, 1)            // the workhorse — expo-ish out
```

For overshoot, prefer a `spring` over `Easing.back` — it is easier to keep subtle.

```tsx
import {spring} from 'remotion';
const s = spring({frame, fps, config: {damping: 200, stiffness: 120, mass: 0.6}});
// damping 200 = no visible overshoot. Drop to ~14 for a small settle.
```

## Text — pop-blur-fade, word by word

```tsx
const Words: React.FC<{text: string; delay?: number}> = ({text, delay = 0}) => {
  const frame = useCurrentFrame();
  const ms = useMs();
  const STAGGER = ms(70);
  const DUR = ms(480);

  return (
    <span style={{display: 'inline-flex', flexWrap: 'wrap', gap: '0.28em'}}>
      {text.split(' ').map((word, i) => {
        const local = frame - ms(delay) - i * STAGGER;
        const p = interpolate(local, [0, DUR], [0, 1], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: Easing.bezier(0.16, 1, 0.3, 1),
        });
        return (
          <span
            key={i}
            style={{
              display: 'inline-block',
              opacity: p,
              filter: `blur(${(1 - p) * 12}px)`,
              transform: `translateY(${(1 - p) * 18}px)`,
              willChange: 'transform, filter, opacity',
            }}
          >
            {word}
          </span>
        );
      })}
    </span>
  );
};
```

The accent word is the same component with `delay` set 120–200ms later plus its own color and a `scale(1.04)`.

## Camera — always-on push

Wrap the whole scene. Over-scale so edges never reveal.

```tsx
const Camera: React.FC<{children: React.ReactNode; durationInFrames: number}> = ({
  children, durationInFrames,
}) => {
  const frame = useCurrentFrame();
  const scale = interpolate(frame, [0, durationInFrames], [1.0, 1.08], {
    extrapolateRight: 'clamp',
    easing: Easing.out(Easing.sin),
  });
  return (
    <AbsoluteFill style={{transform: `scale(${scale})`, willChange: 'transform'}}>
      {children}
    </AbsoluteFill>
  );
};
```

Put the camera **above** the ground layer and **below** any element that must stay pinned to the frame edge.

## Staggered card stack

```tsx
const cards = ['One', 'Two', 'Three'];
const ms = useMs();

{cards.map((label, i) => {
  const local = frame - i * ms(160);
  const p = interpolate(local, [0, ms(600)], [0, 1], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
    easing: Easing.out(Easing.poly(4)),
  });
  return (
    <div key={i} style={{
      opacity: p,
      transform: `translateY(${(1 - p) * 40}px)`,
    }}>{label}</div>
  );
})}
```

## Exit — half the entrance

```tsx
const exitStart = durationInFrames - ms(300);
const out = interpolate(frame, [exitStart, durationInFrames], [1, 0], {
  extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  easing: Easing.in(Easing.cubic),
});
```

## Structure

Use `<Sequence from={...} durationInFrames={...}>` per beat, driven directly by the `motion-plan` table. One `Sequence` per row. Beat durations come from the plan, not from round numbers.

```tsx
<Series>
  <Series.Sequence durationInFrames={ms(5200)}><BeatTwo /></Series.Sequence>
  <Series.Sequence durationInFrames={ms(2100)}><BeatThree /></Series.Sequence>
</Series>
```

## Determinism

- Never `Math.random()` — if you need scatter, seed it from the element index.
- Never `Date.now()` or `new Date()`.
- Never fetch inside a component. Preload with `staticFile()` / `delayRender()`.
- `<Video>`/`<Audio>` must be `<OffthreadVideo>` where possible for render correctness.

## Gotchas

- `filter: blur()` on many simultaneous elements is expensive — cap concurrent blurred nodes, or pre-blur in the asset.
- Font loading: use `@remotion/google-fonts` or `delayRender` around a local `FontFace.load()`, or the first frames render in a fallback face.
- `interpolate` throws if the input range is not monotonically increasing — guard computed ranges.
- Always pass `extrapolateLeft`/`extrapolateRight: 'clamp'` unless you specifically want the value to run past the range.

---

# Appendix B — HyperFrames / GSAP recipes


HyperFrames composes HTML + GSAP and renders by frame-sampling a headless browser. Determinism is mandatory.

Run `npx hyperframes docs` for the current API. This file is the **motion standard** on top of it — see the `hyperframes` skill for the pipeline (init → preview → lint → render).

## The clip rule (breaks renders if violated)

Every timed element needs `data-start`, `data-duration`, `data-track-index` **and** `class="clip"`. The framework owns visibility and transform on `.clip`.

**Never GSAP the `.clip` element itself.** Animate a child wrapper.

```html
<div class="clip" data-start="4.2" data-duration="5.2" data-track-index="2">
  <div class="cam">           <!-- camera moves here -->
    <div class="inner">       <!-- element motion here -->
      <h1 class="headline">…</h1>
    </div>
  </div>
</div>
```

## Timeline registration

```js
const tl = gsap.timeline({paused: true});
window.__timelines['main'] = tl;   // id must match data-composition-id
```

Paused, always. The renderer seeks it.

## Easing map

| Table name | GSAP |
|---|---|
| out-expo | `expo.out` |
| out-cubic | `power2.out` |
| out-quint | `power4.out` |
| out-back (capped) | `back.out(1.2)` |
| in-out-cubic | `power2.inOut` |
| out-sine | `sine.out` |
| in-cubic (exits) | `power2.in` |

## Text — pop-blur-fade, word by word

Split into word spans at author time (do not rely on a runtime splitter — it can race the first sampled frame).

```html
<h1 class="headline">
  <span class="w">What</span> <span class="w">looks</span>
  <span class="w accent">like</span> <span class="w">discipline</span>
</h1>
```

```js
tl.from('.headline .w', {
  y: 18,
  opacity: 0,
  filter: 'blur(12px)',
  duration: 0.48,
  ease: 'expo.out',
  stagger: 0.07,
}, 0);

// accent word lands last and differently
tl.from('.headline .accent', {
  scale: 0.96,
  color: 'var(--surface)',
  duration: 0.5,
  ease: 'expo.out',
}, 0.18);
```

## Camera

Animate `.cam`, never `.clip`.

```js
tl.fromTo('.cam',
  {scale: 1.0},
  {scale: 1.08, duration: 5.2, ease: 'sine.out', force3D: true},
0);
```

```css
.cam { will-change: transform; transform: translateZ(0); }
```

Over-scale the moving layer ~6% beyond the frame so edges never reveal during a push-out or drift.

## Staggered card stack

```js
tl.from('.card', {
  y: 40, opacity: 0,
  duration: 0.6, ease: 'power4.out', stagger: 0.16,
}, 1.2);

// light sweep lands 150ms after the panel
tl.fromTo('.card .sweep', {xPercent: -140}, {
  xPercent: 140, duration: 0.7, ease: 'power2.inOut', stagger: 0.16,
}, 1.35);
```

## Stroke draw

```js
tl.fromTo('.connector', {drawSVG: '0%'}, {drawSVG: '100%', duration: 0.8, ease: 'power2.inOut'});
// no DrawSVGPlugin? use stroke-dasharray/offset:
tl.fromTo('.connector', {strokeDashoffset: 1000}, {strokeDashoffset: 0, duration: 0.8, ease: 'power2.inOut'});
```

## Hard rules

1. Deterministic only — no `Math.random()`, no `Date.now()`, no fetch, no `repeat: -1`.
2. **9:16 = 1080×1920.** Set `#root { container-type: size; }` and size everything in `cqw`/`cqh` (1cqw = 10.8px), never `vw`/`vh`.
3. **Adjacent same-track clips must not touch.** Float math makes `3.2 + 0.35 = 3.5500000000000003`, which overlaps a clip starting at `3.55` and trips `overlapping_clips_same_track`. Leave a gap, or use durations like `0.34`.
4. **Audio:** videos are `muted`; use one pre-mixed master `<audio>` track (VO + SFX mixed with ffmpeg `adelay` + `amix`) on a high dedicated `data-track-index`. Multiple `<audio>` elements cause echo and desync.
5. Split long edits into sub-compositions (`data-composition-src="compositions/beat-04.html"`) — one dense track trips `timeline_track_too_dense`.
6. Fonts must be local `@font-face` woff2. A network font may not be loaded on the first sampled frame.

## Verify

Preview and screenshot key beats before rendering. After render, `ffprobe` for dimensions/duration/codec and spot-check frames against the preview. Motion problems (jitter, edge reveal, missing stagger) are visible in a contact sheet and invisible in a lint pass.
