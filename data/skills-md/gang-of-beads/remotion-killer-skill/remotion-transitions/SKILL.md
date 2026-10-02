---
name: remotion-transitions
description: Scene-to-scene transitions in Remotion using @remotion/transitions TransitionSeries — presentations, timing, custom presentations, and when to use manual cross-fades. Use when joining scenes.
---

# Scene Transitions

## TransitionSeries (default choice)

- Structure: `<TransitionSeries>` containing alternating `<TransitionSeries.Sequence durationInFrames>` and `<TransitionSeries.Transition presentation timing>` elements.
- The transition OVERLAPS its neighbors: its frames are taken from the tail of the previous and head of the next sequence. Total length = Σ(sequence durations) − Σ(transition durations). Each sequence must be longer than the transition duration.
- Give each sequence 10–20 extra tail/head frames of "settled" content so the transition has calm material to blend, not mid-animation motion.

## Presentations

- Built-ins: `fade`, `slide` (direction: from-left/right/top/bottom), `wipe`, `flip`, `clock-wipe`, plus linear/radial wipe variants. Import per module: `@remotion/transitions/fade` etc. (no combined barrel export).
- Choosing:
  - `fade` — neutral, safe, slightly boring; use for tone shifts.
  - `slide` — spatial metaphor (next chapter coming in); keep direction consistent across the whole video.
  - `wipe`/`clock-wipe` — energetic, retro; good for montage/countdown.
  - `flip` — dramatic reveal of a "back side"; needs calm content on both sides.
- Custom presentation: implement `(props) => ReactElement` receiving `progress` (0→1) and `enterTransition`/`exitTransition` flags; return children wrapped in a style driven by progress (transforms, opacity, filters). Register via `presentation={myPresentation()}`. Use for brand-specific moves (e.g. mask wipes with a logo shape).

## Custom presentations (the anti-PPT move)

- Built-in fade/slide read as slideshow if every cut uses them. Write custom presentations for signature moves — the API: a factory returning `{ component, props }`; the component receives `presentationProgress` (0→1), `presentationDirection` (`"entering" | "exiting"`), `presentationDurationInFrames`, and `children`. Wrap children in an AbsoluteFill whose style derives from progress; branch on direction (entering animates in, exiting animates out).
- Recipes (each ~20 lines, no library):
  - **Punch-zoom**: exiting scales 1→1.45 with blur 0→14px and early fade; entering scales 0.82→1 (ease-out cubic) with blur 10→0. Reads as "punching through the camera".
  - **Whip pan**: exiting translateX ±130% with skewX ∓6° and blur→18px; entering from the opposite side with ease-out quart and blur 18→0. Skew+directional blur fakes motion blur.
  - **Depth push**: exiting scales to 0.55 with brightness→0.2 (dives into the screen); entering scales 1.35→1 with brightness 0.3→1, on an opaque background fill so the two slides don't blend.
- Blur-based transitions are expensive: they rasterize both slides every transition frame. At 1080p and 16-frame transitions this is fine; at 4K prefer masks/transform-only.
- Pick 2–3 custom presentations and alternate them across the video; one repeated move also reads as PPT.

## Timing

- `linearTiming({durationInFrames})` — deterministic, predictable, default choice (12–24 frames at 30fps).
- `springTiming({config})` — physical ease for playful videos; harder to predict total length.
- Transition duration guideline: 15–25 frames (0.5–0.8s) for narrative videos, 8–12 frames for fast social edits.

## Manual cross-fades (when OK)

- A single one-off fade between two Sequences: overlap them with `<Sequence from>` offsets and interpolate opacity. Fine for one case; do not build a system of hand-managed offsets — use TransitionSeries for anything composed.
- Never nest plain `<Sequence>` inside `TransitionSeries.Sequence`; use `TransitionSeries.Sequence` (it supplies `from` automatically).

## Gotchas

- Transition duration must be ≤ both adjacent sequence durations.
- `flip` and 3D-ish presentations need perspective — built-ins handle it; custom ones must add their own `perspective` style.
- Scene-detect (ffmpeg `select=gt(scene,t)`) does not flag gradual fades — QA transitions with sampled frames, not scene scores.
- Audio does not transition automatically; VO/music continue across the cut (usually desired — narration bridges visuals).
