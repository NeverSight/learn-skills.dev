---
name: vector-scene-layout
description: Builds the static vector scenes of an animation as Remotion components - project scaffold, design tokens per target (safe margins, font sizes, stroke, contrast), one scene per beat, stills. Use when the user asks to set up the Remotion project, design or lay out the scenes or frames of an animation, or fix text that is too small or cut off. Not for storyboarding, motion, or rendering video.
license: MIT
---

# vector-scene-layout

Turns a validated `storyboard.json` into a Remotion project with one static scene
per beat. It fixes the failures that show up when an agent goes straight to
animating: pixel sizes typed by hand that are unreadable on a phone, text placed
under the feed's controls, a composition whose duration disagrees with the
storyboard, fonts that swap mid-video, and scenes that only look right at one aspect
ratio. Motion is not added here; the deliverable is a set of stills the agent has looked at.

## When to use / when NOT to use

Use when the storyboard exists and the project, tokens, scenes or frames need
building or fixing, when text is too small or clipped, or when a colour pair needs a
contrast check for video.

Do NOT use for: writing the beats (`animation-storyboard`), choosing or licensing
assets (`vector-asset-sourcing`), timing and easing (`smooth-motion-choreography`),
rendering video files (`animation-export-presets`), reviewing a finished render
(`animation-frame-qa`), web page or slide-deck layout, or Remotion API questions the
official `remotion-dev/skills` answer.

## Workflow

1. **Scaffold once** (steps and file layout in `references/project-structure.md`):
   `npx create-video@4.0.522 --blank <name>`, install `@remotion/transitions`,
   `@remotion/google-fonts`, `@remotion/paths` at the same version, add
   `"resolveJsonModule": true` to `tsconfig.json`, install `remotion-dev/skills`,
   copy `storyboard.json` and `assets/manifest.json` in, and write
   `animation.config.json` with `remotion_license_basis` (free tier only for
   individuals, companies of ≤3 people and non-profits; otherwise a Company License).
2. **Generate tokens**, never type pixel values:
   ```bash
   python3 "${CLAUDE_SKILL_DIR}/scripts/frame_tokens.py" --target linkedin-4x5 --target pptx-16x9 --ts > src/tokens.ts
   ```
   Tokens give width, height, safe insets, type scale (caption 32 / body 48 /
   headline 84 / display 120 px at 1080 wide; feed targets scale with width, slides
   with height), minimum weights, stroke widths, icon sizes, grid columns and the
   phone preview scale. Why those numbers: `references/legibility.md`. fps and
   duration come from the storyboard through `timeline.ts`, never from tokens.
3. **Copy the templates** from `assets/templates/` into `src/`: `timeline.ts`
   (frame schedule from the storyboard), `fonts.ts`, `Video.tsx` (TransitionSeries over
   the beats), `SceneOnly.tsx` and `Root.tsx` (one composition per target plus one
   per beat, `<target>--<beatId>`, for isolated stills), `scenes/`. Check brand colours:
   ```bash
   python3 "${CLAUDE_SKILL_DIR}/scripts/frame_tokens.py" contrast "#F5F7FF" "#0B1020"
   ```
4. **Write one scene per beat** in `src/scenes/<beatId>.tsx` and register it in
   `scenes/index.ts`. Each scene is a pure function of `beat` and `tokens`: text at or
   above the token size for its role, everything essential inside `tokens.safe`, one
   focal element, icons from `public/` inline as SVG sized from `tokens.icon`, strokes
   ≥ `tokens.stroke.min`. No `useCurrentFrame()` yet.
5. **Render and look** at every beat alone (no transitions blended in), full size
   and at phone width:
   ```bash
   python3 "${CLAUDE_SKILL_DIR}/scripts/render_stills.py" storyboard.json --target linkedin-4x5 --out out/stills
   python3 "${CLAUDE_SKILL_DIR}/scripts/render_stills.py" storyboard.json --target linkedin-4x5 --phone --out out/stills-phone
   ```
   Open the PNGs, the phone-width ones especially. Fix clipping, undersized text, weak
   contrast, crowding; repeat for every target in `animation.config.json`.
   `npx tsc --noEmit` and `npx eslint src` must be clean.
6. **Hand off**: list the scenes, the tokens used per target, and anything the
   storyboard asked for that the layout could not honour. Next: `smooth-motion-choreography`.

## Output spec

- A Remotion project with `animation.config.json`, `src/tokens.ts` (generated),
  `src/timeline.ts`, `src/Video.tsx`, `src/Root.tsx`, `src/scenes/<beatId>.tsx` for
  every beat, and `out/stills/*.png` per target.
- Every still checked by eye at phone scale; text inside safe areas at token sizes.
- Composition duration equals the storyboard's `total_frames` (from `timeline.ts`).

## Gotchas

- A 1080-wide video is ~390 logical px wide on a phone: 48 px body text is 17 pt
  there, 32 px is the floor (Apple's 11 pt). A 1920-wide landscape post in the same
  feed column needs 1.78× larger text; the tokens scale feed targets by width.
  Hairlines under 3 px vanish after encoding.
- Vertical (9:16) feeds cover the bottom third with UI and some feeds crop to 4:5:
  tokens reserve 35% at the bottom and 15% at the top; do not fight them.
- Contrast belongs in luminance. Thin saturated red or blue text fringes after 4:2:0
  chroma subsampling; light-on-dark with weight ≥ 600 is the safe default.
- Load fonts with `waitUntilDone()` behind `delayRender()` (the template does) or the
  first frames render in a fallback font.
- Never animate or vary `font-size`, `width` or `left` between frames later; lay out
  with transforms in mind so the motion step only touches `transform` and `opacity`.
- The composition id is the target id; `durationInFrames` comes from `timeline.ts`.
  If the storyboard changes, regenerate nothing by hand: re-validate, re-render stills.
- Frame 0 is the LinkedIn thumbnail: the hook scene must read as a poster on its own.
- Scenes must be pure: no `Math.random`, `Date.now`, fetches or CSS transitions.

## Pointers

- `scripts/frame_tokens.py` — tokens (`--ts`, `--target`, `custom --width --height`), `contrast`; `--self-test`.
- `scripts/render_stills.py` — one isolated still per beat at its midpoint; `--phone` renders at 390 px wide.
- `assets/templates/` — `timeline.ts`, `fonts.ts`, `Video.tsx`, `SceneOnly.tsx`, `Root.tsx`, `scenes/` (typecheck-clean).
- `references/project-structure.md` — scaffold commands, file layout, how the pieces connect, loops.
- `references/legibility.md` — type scale derivation, contrast, safe areas with sources.
