---
name: motion-from-reference
description: Build a film's motion grammar by measuring a reference film frame by frame instead of eyeballing it. Use when someone says "make it like THIS video", when type animation looks like a slideshow instead of motion design, or when a cut feels slow/cheap next to the reference. Covers frame extraction, measuring type and timing, the continuous-geometry rule, casting your own story into a borrowed grammar, and the verification loop.
---

# Motion From Reference

Someone hands you a video and says "like this". The failure mode is to watch it four
times, form an impression, and build the impression. The impression is always wrong in
the specific ways that matter: the type is smaller than you think, the holds are shorter
than you think, and the thing that made it feel expensive was one continuous move you
did not consciously see.

So do not build the impression. **Extract every frame and measure it.** A 26 second
reference is under 800 frames, and the four moments you actually need to understand are
maybe 200 of them. An afternoon of measuring produces numbers you can type into `tokens.ts`, and
numbers survive the "can you make it feel more like the reference" note that eyeballing
never does.

## What you copy and what you do not

You copy **grammar**: pacing, how type arrives and leaves, how geometry moves, what the
camera does, where silence sits. Grammar is not ownable and every title sequence in the
world is built from borrowed grammar.

You do not copy content, assets, music, or a shot-for-shot recreation that passes for the
original. Your story, your words, your footage, your brand, your track.

Write the grammar down in prose before you write any code. If you cannot describe the
move in a sentence that contains numbers, you have not finished measuring.

## Step 1: extract and measure

```bash
# every frame, named by index
ffmpeg -i reference.mp4 -vsync 0 frames/%04d.png
ffprobe -v error -select_streams v -show_entries stream=r_frame_rate,width,height,nb_frames \
  -of default=nw=1 reference.mp4
```

Then measure the four things that carry a film. `references/measure-reference.md` has the
copy-paste Python for each.

1. **Type size, as a ratio.** Measure the CAP HEIGHT in pixels and divide by the frame
   height. Never trust the studio preview: a line that looks right on a 27 inch monitor
   is small on a phone. One real measurement: a 62px cap on a 1080-high frame, which is
   an 84 to 88px font at that weight, and the big words ~96px. If your film reads
   "smaller than the reference", this is almost always why.
2. **The type-on.** Diff consecutive frames to find the frame each letter appears.
   Expect roughly one letter per frame, with a two-frame breath after each space and the
   odd one-frame hitch mid-word. Perfectly even letters read mechanical.
3. **The type-off.** This is where references are won and lost. Measure the visible ink's
   left and right edges per frame through the exit. One measured exit: over 13 frames the
   left edge runs RIGHT until ~70% of the line is gone, through a soft edge about eight
   letters wide, while the whole line drifts DOWN about half a cap height on an ease-in
   and the standing part dims slightly; then it SNAPS out rather than fading to zero.
   Implemented in `src/lib/TypedLine.tsx`.
4. **Hold lengths.** Count frames from "fully arrived" to "starts leaving" for every
   card. Holds are shorter than they feel. If your cut runs 58 seconds against a 26
   second reference, the holds are the problem, not the content.

## Step 2: the continuous-geometry rule

The single most valuable thing measurement reveals: **in good motion design the geometry
never restarts.**

The naive build of "three words with line art" fades each word in at its final size
inside its own fresh circle, and cuts to the next. It reads as SLIDES, every time, no
matter how good the easing is. What the reference actually does is keep ONE piece of
geometry alive across every word:

```
word 1   a GIANT hairline outline of the word, wider than the frame, inside a dashed
         circle bigger than the frame. Word and circle SHRINK together on one ease-out
         (44 frames, measured) down to the small word. At the end of the collapse the word
         HARD-FILLS solid - a cut, not a fade - and dashed rails run out of the circle
         to both frame edges.
word 2   hard word cut, but THE SAME CIRCLE: its dashes close up into a solid line, it
         grows, and two more circles slide out of it to the sides into a Venn that keeps
         drifting apart.
word 3+  the side circles slide off the edges while the words crossfade MIRRORED: old
         letters fade left-to-right while new ones arrive right-to-left dim, then
         brighten left-to-right. Two opposite waves in one beat.
last     the line leaves as a whole-line fade with a scale-up and a blur, written as an
         exit so the next element can start UNDERNEATH it.
```

Working implementation: `src/lib/GeometryWords.tsx`, demonstrated in `src/grammar/`.

The general principle generalizes past circles: **a new element should be born out of the
element it replaces.** When you catch yourself writing a scene that mounts fresh shapes
at their final size, you are writing a slideshow.

## Step 3: cast your story into the grammar

Write a casting table that maps every reference beat to your own content, in order, with
the same FUNCTION. Do not reorder; the order is part of the grammar.

| Reference beat | Its job | Your content |
| --- | --- | --- |
| Opening typed line | the announcement | your launch sentence |
| Macro device corner, app updating | the product arriving | your product, same framing |
| Three value words in geometry | the promise | your beats, one per word |
| Device rises, camera pushes in | the proof | your real recordings |
| Closing typed line | the identity | your brand line |
| Logo lockup | the signature | your lockup |
| Two-word close | the call | your two words |

Note the symmetry worth keeping: the opener is the ANNOUNCEMENT ("Rebuilt for X") and
the close is the IDENTITY ("Built for Y"). Swapping them makes the film feel like it
starts in the middle.

If a reference beat has no equivalent in your product, cut it rather than invent filler.
A 33 second film in a 26 second grammar is fine; a 58 second one is a different film.

## Step 4: build it as data

Everything measured goes into `tokens.ts` as named constants with the measurement in the
comment, not as magic numbers inside a scene:

```ts
// Frames per word, measured: word 1 carries the 44-frame collapse of its giant
// outline and circle, then holds; the rest are short holds; the last holds a few
// frames longer while the device rises under it.
export const WORD_FRAMES = [70, 36, 36, 36, 40] as const;
```

A future note of "slow it down and match exactly" is then a diff of numbers, not a
rewrite. That note WILL come.

## Step 5: verify against the reference, not against taste

- Render your frames and put them **side by side** with the reference frames at the same
  beat. `ffmpeg -i mine.mp4 -vf "crop=..." -frames:v 1` plus the extracted reference
  frame, stacked with `hstack`.
- Frame-step every morph. A move that "snaps" instead of animating is invisible at 1x
  and obvious at 4 frames per second.
- Check the type ratio on a phone-sized render, not in the studio.
- Watch both cuts back to back at 1x with sound. If yours feels longer, it is.

## Honest limits

- The reference's own spend is invisible. A 3D phone that took three days of material
  setup reads as one shot. Budget for the thing you cannot see.
- Some moves are keyframed by hand over hours in After Effects and are genuinely
  cheaper to approximate than to reproduce. Approximate deliberately and say so.
- A grammar borrowed whole from a famous film will be recognized. That is usually fine
  (grammar is shared) but it is a positioning choice, so make it on purpose.

Pair with: `remotion-marketing-video` (how to build it), `device-3d-stage` (when the
grammar wants a real device on screen), `video-audio-stack` (the reference's silence is
also measurable, and is usually more silent than you think).
