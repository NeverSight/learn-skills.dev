---
name: remotion-marketing-video
description: Build marketing and launch videos as Remotion compositions. Use when creating or editing any video in this repo - scene structure, timing math, kinetic captions and typed lines, springs and interpolation, dual 16:9/9:16 output, light/dark editions, verification, and rendering. This is the core skill; pair with motion-from-reference when matching a reference film's grammar, device-3d-stage for a real device on screen, ai-cinematic-broll for AI footage, and video-audio-stack for sound.
---

# Remotion Marketing Video

You are building a film as code. Every frame is a pure function of `useCurrentFrame()`.
That is the whole advantage: timing is data, edits are diffs, variants are props, and you
can verify a frame the way you verify a unit test.

## Philosophy

- **One film, not a slideshow.** A persistent backdrop with an emotional color arc plus a
  thin global chrome (progress bar, series chip, brand mark) bracket the scene stack so the
  whole piece feels continuous. Scenes change; the world persists.
- **Story first.** Do not open the editor until the script exists. The voiceover (or the
  silent narration) lives in a `script.ts` as frame-timed cues - it is the single source of
  truth that scenes, captions, and audio all read. Copy avoids em-dashes (they read as
  AI-generated) and is trimmed so no caption wraps past three lines in portrait.
- **Readable pacing beats tight pacing.** Give each line roughly its reading time plus a
  beat (~1-2 seconds of lead per chat message or caption). When a viewer says they could not
  finish reading, add time - do not cut copy.
- **Motion design, not slides.** The difference is whether elements are BORN OUT OF the
  elements they replace. A scene that mounts fresh shapes at their final size and fades
  between them is a slideshow with easing. Keep one piece of geometry alive across a
  sequence and transform it - see `lib/GeometryWords.tsx` and the
  `motion-from-reference` skill.
- **Build decisively.** Pick a strong default, state assumptions, build it, then offer
  specific adjustment levers (swap music, retime a beat, flip a media slot). Do not
  front-load configuration questions.

## Project structure

One folder per video. Everything the film needs lives inside it:

```
src/<video>/
  tokens.ts        # palette, fonts, FPS, SCENE durations, TOTAL_FRAMES, SCENE_START
  script.ts        # the VO / narration as Cue[] (frame-timed, scene-relative)
  <Video>.tsx      # the composition: Backdrop + Audio + <Series> of scenes + GlobalChrome
  <Video>Vertical.tsx  # 3-line portrait wrapper (see Dual aspect)
  scenes/          # one file per scene
  components/      # scene-local components
  audio/           # OPTIONAL: this film's cue sheet, if it has enough cues to
                   # deserve its own file (see the video-audio-stack skill)
```

Register every edition in `Root.tsx`, and have each film's compositions read THEIR OWN
`FPS` from their own `tokens.ts` - importing another film's constant is how a retime
silently fails to apply.

Assets load with `staticFile()`, never a plain string path:

```
public/<video>/   # anything specific to this film (clips, logos, stills)
public/audio/     # music beds, shared
public/sfx/       # the one-shot library, shared
```

Keep licensed audio out of git (`.gitignore` already covers `public/audio/*` and
`public/sfx/*` while keeping their READMEs).

Two films ship in this repo as working examples of the pattern: `src/example/` (kinetic
captions, cards, counters, chrome) and `src/grammar/` (typed lines, continuous geometry,
dust, three themes).

## Timing model (get this right or audio desyncs)

- Scene durations live in one `SCENE` const in `tokens.ts`, in frames, with a timecode
  comment per scene. `TOTAL_FRAMES` is **always computed as the sum - never hardcoded**.
- Also export `SCENE_START` (absolute start frame per scene). The persistent backdrop and
  chrome sit outside the `<Series>` and read absolute frames; scenes read scene-relative
  frames. Mixing these up is the most common bug.
- Prefer a plain `<Series>` (no transition overlap) when the film has frame-timed captions:
  the total is an exact sum and every cue frame number stays trustworthy. If you use
  `TransitionSeries`, the total is `sum(scenes) - numTransitions * TRANSITION_DURATION` -
  forgetting the subtraction breaks audio sync.
- **`useCurrentFrame()` inside a scene is SCENE-relative.** When validating a still, render
  at `SCENE_START.<scene> + offset`, not the raw offset.

## Animation grammar

- **Springs for entrances**, driving opacity plus one transform. Delay by subtracting from
  the frame: `spring({ frame: frame - delay, fps, config })`. Useful configs:
  `smooth` (damping 200), `snappy` (damping 20, stiffness 200), `bouncy` (damping 8),
  `heavy` (damping 15, stiffness 80, mass 2).
- **`interpolate` always clamps both sides.** Every time-range interpolation needs
  `{ extrapolateLeft: "clamp", extrapolateRight: "clamp" }` or values bleed into adjacent
  frames. No exceptions.
- **Kinetic captions** are the house narration style: word-by-word reveal (rise + blur +
  fade, ~2 frame stagger, ~9 frame word-in), emphasized substrings in the accent color so
  each line lands on the word a founder would hit out loud, and a localized radial scrim
  under live text for legibility. See `src/lib/KineticCaption.tsx`.
- **Numbers animate as numbers.** Counters interpolate the numeric value and format at
  render; never animate formatted strings.
- **Icons come from ONE icon set** per project, recolored via CSS filter
  (`brightness(0)` for black, `brightness(0) invert(1)` for white on stroke-black SVGs).
  Never hand-draw one-off glyphs - consistency with the product is the point.
- **Real UI beats mockups.** If the product is a web app or extension, consider running the
  actual components inside the composition behind a runtime shim: fake the host APIs
  (e.g. a `globalThis.chrome` stub with canned message responses), seed the state store
  deterministically per frame, and the demo can never drift from the shipped product.

### Shared primitives in `src/lib/`

Reach for these before writing a new one; each exists because its naive version looks
wrong in a specific, measurable way.

| Primitive | What it is for |
| --- | --- |
| `KineticCaption` | Word-by-word narration: rise + blur + fade, emphasis in the accent color |
| `TypedLine` | A line that types on one letter a frame and SWEEPS off (not a fade). Measured mechanics - see the `motion-from-reference` skill |
| `LetterLine` + `letterSweep` | Per-letter opacity from a function of index: sweeps, mirrored crossfades, brightness waves |
| `GeometryWords` | A value-word sequence carried by ONE continuous piece of geometry |
| `DustField` | Living dust motes for a dark ground (each mote has its own path, not a shared one with a phase offset) |
| `MusicBed` / `SfxCue` | The audio layers - see the `video-audio-stack` skill |

Type sizing is a measurement, not a feel: a cap height of 62px on a 1080-high frame is an
84-88px font. Portrait gets its OWN sizes (66px lines, 64px words at 1080 wide), never the
landscape number scaled.

**Backgrounds are a system too.** A dark frame wants texture, but points on a linear drift
with a twinkle read as a star field and look cheap. `DustField` gives every mote its own
depth, its own two-sine path and its own breathing period. Verify by compositing three
frames a second apart into R/G/B: parallel trails mean you built a star field.

### remotion-bits

The `remotion-bits` package (`npx remotion-bits find "<visual goal>"`) is a library of
working animation examples (text reveals, counters, particles, 3D camera scenes) with its
own agent skill at `github.com/av/remotion-bits`. Search it before hand-rolling a common
effect; adapt the closest example.

## Dual aspect: 16:9 and 9:16 from one scene tree

Every film ships landscape (YouTube, website, deck) and portrait (TikTok, Reels, Stories).
The portrait edition is NOT a re-edit and NOT a scale-and-crop (that pushes corner elements
off-canvas). It is the same composition rendered natively at 1080x1920 under a context flag:

```tsx
export const MyVideoVertical: React.FC = () => (
  <VerticalLayoutContext.Provider value={true}>
    <MyVideo />
  </VerticalLayoutContext.Provider>
);
```

Rules, learned the hard way:

1. `VerticalLayoutContext` lives in **its own file**. Importing it from the wrapper creates
   a `scenes -> Wrapper -> Video -> scenes` cycle that leaves the context undefined at module
   evaluation and renders the studio as a white screen.
2. Anything anchored to corners/edges with absolute offsets needs a `vertical ? {...} : {...}`
   branch - the 1080-wide canvas pulls side elements onto centered content.
3. Anything with a hardcoded width in landscape coords (a 1050px card) overflows 1080 -
   pass a narrower number through the same ternary.
4. Scene-center constants (`centerX = 960`) assume the 1920 canvas - recompute in portrait.
5. Centered flex rails (`left: 50%`, `inset: 0`) auto-adapt - leave them alone.
6. Backgrounds use `AbsoluteFill` / `inset: 0` with `object-fit: cover` - they fill both
   ratios for free. Never `width: 1920` on a background.
7. Write new scenes aspect-aware from day one; back-porting the branches later is worse.

## CSS pitfall: transform-scale leaks layout

An absolutely-positioned element with `transform: scale(N)` keeps its layout box at native
size but its **visual bounding box** becomes N times larger. That overflow leaks into the
iframe body layout and shifts every absolute sibling left by an unpredictable amount that
varies per render - it looks like a centering bug and is not.

**Fix:** wrap EACH scaled element (the camera-transformed stage AND any independently
scaled element) in its own composition-sized `overflow: hidden` container. `AbsoluteFill`'s
own overflow clipping is NOT sufficient - the leak happens at the body level.

**Verify:** render a still with debug dots at known `left` values and read their pixel x
with PIL - they must land within 1px.

## Verification loop (do this, always)

1. **Stills at exact frames**: `npx remotion still <Comp> out/f.png --frame=<SCENE_START + n>`
   after every meaningful change. Look at them - actually read the frame.
2. **Pixel-probe layouts** with `python3 -c "from PIL import Image; ..."` when centering or
   alignment matters.
3. **Frame-step motion**: render a short segment, screen-record the studio, or extract
   frames with ffmpeg and step through them. Morphs that "snap" instead of animating only
   show up frame-by-frame.
4. **Preview the longest copy** (longest locale/edition string) - that is what overflows.
5. Watch the full cut at 1x with sound before calling anything done. Then watch it once
   more pretending you cannot hear it.

## Variants without re-edits

- **Editions** (partner cut, locale, campaign): a React context provides an
  `EditionContent` object (messages, stats, chart points, source logos); scenes read the
  context. Layout and choreography stay identical; only content swaps.
- **Themes** (dark / light / mixed): `ThemeContext` in `src/theme-context.ts`, exactly
  like the vertical flag and in its own file for the same cycle reason. `mixed` gives
  each scene its own value from one table (`sceneThemes`), which is how a film alternates
  grounds the way an App Store screenshot set does. Crossed with the aspect ratios that
  is SIX deliverables from one scene tree - `src/grammar/` demonstrates it.
  - One component owns the ground; no scene paints its own background, so no scene can
    disagree with the edition.
  - Dust belongs to dark grounds only. On white it reads as dirt.
  - Marks and logos that are drawn white need inverting for the light edition
    (`filter: brightness(0)` on a white SVG), and that is easy to forget on the one
    scene you did not check.
- **Parameterized comps**: Zod-typed props on the composition (`schoolName`, `accentColor`)
  for per-audience renders from the CLI.

## Rendering

```bash
npx remotion studio                                    # live preview
npx remotion render <CompId> out/<name>.mp4            # standard 1080p
# High-quality master (archival / re-upload source):
npx remotion render <CompId> out/<name>-best.mp4 \
  --scale=2 --crf=14 --image-format=png --color-space=bt709 \
  --x264-preset=veryslow --pixel-format=yuv420p --concurrency=50%
```

`--scale=2` on a 1920x1080 comp gives a 4K master. Use `--crf=17 --jpeg-quality=100
--x264-preset=slow` for a faster near-best pass. Render portrait and landscape as separate
compositions, not crops.

### Deliverables are supersampled, not rendered at 1x

At 1x the browser stair-steps rotated elements, CSS clips, thin strokes and any WebGL
edge, and the result reads as cheap even to people who cannot say why. Render every
delivery at `--scale=2` and downscale with a Lanczos filter:

```bash
scripts/render-supersampled.sh Grammar 1920:1080
```

That script renders at 2x, downscales with ffmpeg, tags BT.709, writes a faststart MP4 and
deletes the 2x intermediate. Add each edition to its case list and the whole set is one
command. Drafts can stay at 1x; anything a human reviews for polish should not.

Pass `--gl=angle` as well whenever the composition contains a WebGL canvas, or it renders
blank with no error.
