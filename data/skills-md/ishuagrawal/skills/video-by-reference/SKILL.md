---
name: video-by-reference
description: Make a fully code-generated animated video at the highest achievable visual and design quality (with an original synthesized soundtrack) whose look, sound, editing and pacing are learned from a reference video — in whatever style that reference uses (flat 2D, 3D/CG, anime, painterly, pixel art, hand-drawn, kinetic type, stop-motion feel…). Studies the reference frame-by-frame and by audio analysis, writes a measured style bible, derives an original story, picks a rendering approach that fits the style, builds a deterministic browser animation, renders it to MP4 with headless Chrome + ffmpeg, and QA-reviews it. Use this whenever the user shares a video/YouTube link or clip and wants an animation, short, trailer, teaser, explainer, mascot or character video "in the style of", "like this", "inspired by", or "with the vibe of" it — or asks you to study a video's art style, sound, camera, transitions or narrative and then make something similar — even if they never say "reference" or "skill".
license: MIT
---

# Video by Reference

Turn "make me something like *this video*" into a finished, high-quality animated short: a real
MP4 with picture and sound, whose craft is learned from the reference and whose story is original.

The skill is **style-agnostic by design**. The reference decides the look: its rendering model,
palette or grade, frame rate and holds, camera and lens behavior, FX design, editing rhythm, type
and sound. Your job is to measure those traits, understand the principles behind them, and choose
techniques that reproduce them. Nothing in this skill should push every film toward one look; the
worked examples (a flat screenprint-style 2D trailer, among others) are illustrations, not defaults.

The workflow was distilled from a full production (study a trailer → pitch → user redirect →
research → engine → synthesized score → render → review → re-pace after feedback). Each rule
exists because skipping it cost a re-render or a correction. Read the referenced files when you
reach their phase.

## Quality bar: HIGH

Design quality is **HIGH**. The video must look like the work of a skilled professional studio
working in the reference's style, not programmer art, a proof of concept, or "good for code".
Every decision should go toward the best visual quality you can achieve. When a choice trades
visual quality against effort, render time or simplicity, choose quality.

- **Make the best version of the reference's style, not a simplified one.** If the reference has
  rim lights, layered backgrounds, texture, secondary motion or rich props, build them. Don't
  cut a trait because it is hard to code.
- **Craft every frame as a finished still.** Each frame needs deliberate composition, a clear
  focal point, strong value structure, depth (foreground, midground, background), refined shapes,
  clean edges and finished environment detail. Any frame should hold up as a poster or
  screenshot.
- **Design the motion.** Use anticipation, follow-through, overlap, secondary motion, weight and
  shaped easing. No linear tweens or stiff rigs unless the reference moves that way.
- **Set type with care.** Use a clear hierarchy, good tracking and spacing, grid alignment, and
  faces and treatments that match the reference.
- **Render at full fidelity.** Supersample for crisp edges, use motion-blur subframes where the
  style calls for them, and encode at high quality. Accept longer renders.
- **Iterate past "works".** On every look-dev frame and contact sheet, ask what a top artist in
  this style would improve, then fix it. The first version that runs is a draft.
- **High quality is not more effects.** It means executing the reference's own style at its
  highest level. A pixel-art film is clean on the pixel grid; a flat poster film has crisp shapes
  and disciplined color; a cinematic film has believable light and lens. Don't add bloom,
  gradients or particles the reference doesn't use.
- **Polish serves the story.** Richness and detail never cost readability or pacing.

## What "done" looks like

- A rendered video (default 1920×1080, 24 fps unless the reference implies otherwise, H.264 +
  AAC, ~-15 LUFS, true peak ≤ -1 dBTP) with an original, frame-locked soundtrack (score + sound
  effects), delivered the way the user asked (a file unless they ask to publish).
- A viewer who knows the reference recognizes its style in your film. The style traits you
  reproduced were measured from the reference, not guessed.
- The picture meets the HIGH quality bar: frames stand up next to the reference's frames at full
  resolution. There is no placeholder art, rough or unfinished area, stiff motion or
  default-looking type.
- The story, scenes and gags are original. Inspired, never a shot-for-shot copy.
- Every on-screen sentence can be read, every key moment has room to land, nothing important is
  cropped, hidden or ambiguous. You verified this by looking at frames of the actual render.
- Facts the film asserts about the real world (product behavior, commands, prices, events) are
  checked.

## How to work with the user

Make the decisions yourself: style analysis, rendering approach, concept (when one is requested),
story, shots, palette mapping, music, length, technical stack. The user wants a result, not a
menu. Ask (with AskUserQuestion, recommended option first) only when genuinely blocked:

- The user asked for *suggestions*: pitch 3–5 original concepts and let them pick.
- A choice changes the deliverable in a way you can't infer (hard length limit, aspect ratio for
  a platform, language of on-screen text, whether a real brand may appear).
- The style needs something code can't credibly produce (e.g. photoreal humans, a full orchestral
  score). Propose the closest stylized route and ask whether that's acceptable, or whether they
  can supply assets/music.
- You need permission: downloading the reference file, installing software, publishing.
- The reference is unreachable and no substitute is obvious.

Post a one-line progress update when a phase completes or a long render starts. Be honest about
what you could not verify (you cannot hear audio; say you verified it by measurement).

## Phase 0: Set up

1. Read the repo's conventions (CLAUDE.md, any `refs/` folder of canonical assets such as a
   character sheet). Treat those assets as the visual source of truth and reference them by path.
2. Check tools: `node` (≥ 22), `ffmpeg`/`ffprobe`, a Chromium (prefer Playwright's
   `chrome-headless-shell`; see `references/render-pipeline.md`), Python 3 + numpy for analysis.
3. Scaffold from the template: `cp -r <skill>/assets/engine <project-dir>`, then prove the
   pipeline before any art: `node render/render.mjs --stills 1,3 --sheet smoke` and a full
   `node render/render.mjs`.

## Phase 1: Study the reference

Goal: a written **style bible** with measured numbers plus the **principles** behind them.
Read `references/reference-analysis.md`.

- Metadata: title, source, duration, re-upload or cut-down, the lore behind it.
- Measure: local file → `python3 scripts/analyze_media.py <video> --out <dir> [--music-range a-b]`.
  Browser-only page → `scripts/browser_probe.js` in the built-in browser (pause right after
  loading and confirm the title/duration; frame scans need the pane visible). You get cuts, shot
  lengths, drawing-rate holds, palette, luminance curve, loudness trace, onsets, tempo, tonal
  center and silent gaps, plus contact sheets.
- Treat measurements as evidence, not truth. Cross-check them against what you see, and validate
  a tool on a file whose answers you know before relying on it (a coarse FFT once reported the
  wrong key by a semitone; flickering effects show up as false cuts).
- Look at every shot and classify the **rendering model** (2D flat, 2D painterly, cel/anime, 3D
  toon, 3D realistic, pixel, line/sketch, collage/cut-out, typographic, mixed media), lighting,
  texture, line, depth cues, lens behavior, motion style, transitions, FX, typography and the
  narrative purpose of each shot.
- Audio: measure tempo, tonal center, accents vs. cuts, silences and dynamic shape.
- Write the bible (template in the reference file), ending with the rendering approach you'll
  use. Save key numbers to memory if available.

## Phase 2: Concept

Read `references/story-and-pacing.md`.

- Separate the reference's **DNA** (transferable principles: how it reveals, builds, cuts,
  breathes, jokes, lights and moves) from its **surface** (its specific scenes, props,
  characters). Carry the DNA; invent the surface. Users react badly to near-copies even when
  they ask for "the same vibe".
- If the film is about something real, research it (official docs and real cases), build the
  story on true facts, and don't show things the real product or world prevents.
- Pitch format when pitching: logline, 5–8 beat outline, the reveal, the ending button, why it
  fits the DNA. When the user picks or redirects, adopt the direction fully.

## Phase 3: Pre-production (before drawing anything)

1. **Cue sheet first** (`src/timeline.js`): every event time is a named cue derived from a few
   anchors (music start, `bar()`/`beat()` helpers if the film is cut to music). Shots and sound
   both read cues; no shot contains a literal absolute time. In the source production, re-timing
   a film whose times were hard-coded across files was the most expensive correction.
2. Pick fps and tempo so a beat is a whole number of frames when the edit follows music
   (`fps × 60 / BPM`).
3. **Pace for comprehension from the start** (rules in `references/story-and-pacing.md`): read
   time for text, title cards held long enough to read, set pieces with a held payoff, one new
   idea at a time. Action can be fast; information cannot.
4. Beat sheet: shots with start/end cue, framing, action, on-screen text and sound.
5. Look development: palette or grade per act (a color script), lighting setups, the hero's
   signature traits, how the reference's rendering model will be built. For a character from an
   image, measure its proportions from the pixels and plan a parametric rig.

## Phase 4: Build the picture

Read `references/engine.md` (architecture, determinism, camera, rigs, sets) and
`references/style-techniques.md` (how to build *this* reference's look: flat/cel, painterly,
3D, pixel, line, anime, collage, typography, live-action-like).

- The template's pipeline (deterministic `frame(t)`, cue sheet, camera, post pass, synth,
  headless renderer) is style-neutral. The drawing layer is yours to choose: the bundled
  `draw.js`/`fx.js` kits suit shape-based 2D. Extend or replace them (e.g. Three.js for 3D) to
  match the bible.
- Configure the post pass from the bible: lens distortion, vignette, grain, grade
  (contrast/saturation/tint), chromatic aberration, pixelation and motion-blur subframes. Use
  only what the reference actually shows.
- Build one world per location that every shot frames with its own camera (continuity for free).
- Work act by act: render 10–20 stills into a contact sheet, look, fix, repeat. Never write
  three acts before looking at one. Use `references/review-checklist.md` on every pass.
- Hold the HIGH quality bar on every pass. Look at stills at full resolution, not only as
  thumbnails, and keep refining shapes, lighting, detail and motion until frames match the
  reference's finish. Raise `supersample` (e.g. 1.5–2) if edges or fine lines look soft.

## Phase 5: Build the sound

Read `references/audio.md`. Score and Foley are synthesized with Web Audio in an
`OfflineAudioContext` from the same cue sheet, so they are sample-accurate to the picture.

- Match the reference's tempo, tonal center and genre feel with original material. Arrange by
  sections that follow the beat sheet, and use stop-time, drop-outs and silence as storytelling.
- Give every visible action a sound, and keep quiet room tone under "silent" beats.
- Verify by measurement (`python3 scripts/review.py <video>`), and tell the user you did.

## Phase 6: Render and review

1. Render audio and video in separate browser sessions (`--audio-only`, then `--reuse-audio`)
   with `chrome-headless-shell` (failure modes in `references/render-pipeline.md`).
2. `python3 scripts/review.py out/<name>.mp4 --fps 1 --cues out/cues.json` → contact sheets +
   an audio report whose loudness trace is annotated with your cue names. Review like
   a first-time viewer: can you follow the story at one frame per second? Does every title
   survive at least 3 samples? Does every payoff get held frames? Does it still look like the
   reference? Is every frame at the HIGH quality bar, or does any look cheaper than the
   reference?
3. Fix, spot-check ranges with `--from/--to`, then do the full render.

## Phase 7: Deliver

- Deliver the file the way the user wants. Large files may exceed upload limits for remote
  viewers; say so and offer a compressed copy.
- Summarize: the beats, which reference principles were applied and how, research sources
  (links), how to tweak (the cue sheet), and what you could not verify.
- Don't commit unless asked; keep render outputs out of git.
- On feedback ("too fast", "doesn't feel like the reference", "too busy"), diagnose the category
  (pacing, readability, tone, style fidelity) and fix it systemically across the film, not just
  at the moment they named.

## Bundled resources

| Path | Use it when |
| --- | --- |
| `references/reference-analysis.md` | Phase 1: measuring and describing a reference in any style; style-bible template; browser gotchas |
| `references/story-and-pacing.md` | Phases 2–3: DNA vs. surface, pitches, fact-grounding, pacing rules, cue sheet, beat sheet |
| `references/style-techniques.md` | Phases 3–4: turning style traits into techniques (2D flat/painterly/cel, 3D, pixel, line, collage, type, live-action feel) |
| `references/engine.md` | Phase 4: architecture, determinism, camera, rigs, sets, FX, text-in-world, performance |
| `references/audio.md` | Phase 5: score and Foley synthesis, arrangement, mix, verification without hearing |
| `references/render-pipeline.md` | Phases 0 and 6: headless rendering, encoding, troubleshooting |
| `references/review-checklist.md` | Every review pass: recurring corrections as a checklist |
| `scripts/analyze_media.py` | Measure a local reference video |
| `scripts/browser_probe.js` | Measure a reference that only plays in a web page |
| `scripts/review.py` | QA a render: contact sheets, loudness/true peak, loudness trace, spectrogram |
| `assets/engine/` | Starter project: style-neutral pipeline, demo film, preview player, renderer, synth |
