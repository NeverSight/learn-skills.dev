---
name: motion-design
description: Taste rules for Remotion motion graphics — timing, easing, springs, typography, color, texture, and scene continuity, with concrete numbers. Use whenever you create, animate, retime, or polish a video, composition, scene, or transition in this repo.
---

# Motion design

Remotion teaches you the API. This file is the taste. Every number below comes from a shipped piece (`src/EffortVideo.tsx`); treat them as defaults you deviate from on purpose, not by accident.

## 1. Time lives in `timeline.json`

- Every beat is a named timestamp in seconds in `timeline.json`, grouped by scene (`s1`, `s2`, …). Components read it through `TL` from `src/lib.ts`; the video's cue sheet in `sfx/cues/` reads the same file. That is what keeps picture and sound locked.
- Never hardcode a start time inside a component. Offsets relative to a beat (`s1.exit + 0.05`) are fine.
- Retiming = editing `timeline.json`, then `npm run sfx` so audio follows.
- Everything is a pure function of `frame`. No CSS transitions or keyframes, no `Math.random()` (use `rand(n)`), no `Date`. Anything else flickers or drifts at render time.

## 2. Easing

| Curve | Use | Source |
|---|---|---|
| `easeOut` = `bezier(0.16, 1, 0.3, 1)` | entrances, reveals, anything arriving | `lib.ts` |
| `easeIn` = `bezier(0.6, 0, 0.9, 0.35)` | exits — leaves fast, doesn't linger | `lib.ts` |
| `easeInOut` = `bezier(0.65, 0, 0.35, 1)` | moves between two states (flip, dock, morph) | `lib.ts` |
| overshoot `bezier(0.55, 0, 0.2, 1.12)` | a value that "lands" (slider climbing to a level) | `effortAt` |

Linear is only for continuous motion: rotation, drift, grain, ticking hands.

Use `prog(t, t0, t1, ease)` for tweens and `band(x, a, b)` to derive one animation from another value (e.g. captions from the slider position) instead of giving it its own clock.

## 3. Springs (via `sp(frame, startSec, config)`)

| Feel | damping / stiffness / mass | Used for |
|---|---|---|
| default settle | 14 / 140 / 0.8 | general UI entering |
| heavy, calm | 15–20 / 140–240 / 0.6–1 | big panels, the rewind |
| knob / notch | 12 / 190 / 0.75 | a control snapping to a step |
| pop | 9–11 / 200–230 / 0.7 | callouts, badges, success dots |
| elastic accent | 8 / 200 | one hero moment per video, not more |

Springs for things that feel physical (UI, objects). Bezier tweens for type and camera-like moves.

## 4. Timing

- **Stagger** words by ~0.09 s, list items/chips by ~0.2–0.25 s, rings/dots by ~0.06 s.
- **Word reveal** ≈ 0.8 s with `Mask` (slide up out of a clip + slight tilt).
- **Exits are ~half an entrance** (0.35–0.55 s vs 0.7–1.25 s). Exits use `easeIn`.
- **Overlap scenes.** The next scene starts drawing on before the previous one has fully left (`s2.drawOn` 4.02 s < `s1.flipEnd` 4.4 s). Hard gaps read as "loading".
- **Typing** ≈ 0.035 s per character, caret blinks at ~2.4 Hz when idle.
- **Reading holds.** Every readable state needs a hold after it settles: ≥ 1 s for a short phrase, add ~0.25 s per word beyond three, ≥ 2 s for the final hook. The 22 s cut of the effort video exists because the 15 s one flashed text too fast — when in doubt, hold longer and animate less.

## 5. Typography

- Max three families: display serif (Instrument Serif), UI sans (Inter), mono (JetBrains Mono) for labels, prompts, numbers.
- Display type is big (≈ 138 px on a 1080 canvas) with tight tracking (`-0.02em`), `lineHeight: 1`.
- One accent per line: a single italic word in the accent color carries the point (`Same *prompt.*`).
- Mono labels: uppercase, `letterSpacing: 0.2–0.24em`, muted color. They're decoration; anything the viewer must read goes big.
- Phone test: at 360 px wide (how X shows it in the feed) the key message must still read. Check it on the contact sheet.

## 6. Color

- Palette tokens live in `C` (`lib.ts`). Don't introduce new hex values in components.
- One accent color (coral) and it means something: the thing that changed, the answer, the winner. If everything is coral, nothing is.
- Drive glow from state, not time (`glow = effort`): light should explain the story.

## 7. Texture — nothing is dead-still

- Film grain overlay (`Grain`, opacity ≈ 0.09, reseeded on twos).
- Vignette plus a dot grid drifting a few px/s (`Background`).
- Hand-drawn "line boil" (`WobbleFilter`) for sketchy/low-fidelity states, faded out as quality rises.
- Idle elements breathe: a ticking clock, a blinking caret, a slow rotation.

## 8. Continuity and transitions

- Prefer persistent objects over cuts. The prompt bar, the spark and the slider travel through scenes and change role; that's what makes it feel designed rather than assembled.
- Every transition is motivated by an object on screen (the five result dots merge into one, which becomes the iris). No generic wipes.
- Use velocity: derive motion trails / squash from `value(frame) - value(frame - 1)` instead of faking it.
- One hero moment per video (the iris + impact). Build to it; don't spend it early.

## 9. Anti-patterns

- Everything fading in at once, or everything using the same duration.
- Linear easing on anything that starts or stops.
- Text that moves while it's supposed to be read.
- More than one focal point per frame.
- Content within ~60 px of the frame edge (safe area) unless it's intentionally cropped.
- An empty or black frame 0 — X autoplays muted and the first frame is the thumbnail.

## Workflow

1. Write the beats into `timeline.json` first (a storyboard in numbers).
2. Build scenes as components in `src/scenes/`, shared bits in `src/components/`.
3. Run the `review-loop` skill after every meaningful change.
4. Run the `sound-design` skill once picture timing is locked.
