---
name: arcads-video-edit
description: >
  Turn a creator's multi-take product-demo recordings (each take = screen recording + camera video +
  mic WAV, usually the creator walking through Arcads) into a finished 9:16 ad: an EDL-driven base cut
  rotating three layouts (the speaker full screen / split with the screen on top / full-screen
  product with the speaker in a circle), every pause cut so they talk over their own pauses, retakes dropped; then a
  HyperFrames motion-graphics pass with full-screen takeovers, the base video moving into splits
  and circles, real generated footage in cards and montages, word-synced captions, SFX and
  music, reviewed on a here.now canvas and gated by a copy review and the 4-layer video QA. Use
  whenever the user hands over a folder of takes and says "edit these together",
  "make the base edit", "cut this into an ad", "add motion graphics / takeovers / captions /
  music", or leaves timeline notes on an Arcads-style edit, even if they never say Arcads or
  multicam. Not for reel-recut, embedded-captions, or a talking head with no screen footage
  (branded-ad-edit).
---

# Arcads video edit

Multi-take screen+camera+mic recordings in → a base cut the creator signs off → a motion-graphics
pass that impresses a senior editor → published on the review canvas, every round. Proven on a real
Arcads brand ad: V1–V5 base cut across 21 timeline notes and three QA rounds, then V6 (rejected:
"no full-screen takeovers… go crazy") → V7/V8 accepted ("overall much better!!").

Two phases, two different jobs. **Phase 1 is editing** — the picture gets locked and never moves
again. **Phase 2 is motion design on top of a locked picture.** Do not blur them: every V6 mistake
came from treating the graphics pass like overlays instead of a rebuild, and every base-cut mistake
came from trusting a number instead of measuring a frame.

Read the reference for each phase when you reach it — they carry the exact commands and every
trap that cost a render. Skim [references/gotchas.md](references/gotchas.md) before starting.

## What you produce

- **Base cut:** 1080×1920 @ exactly 30fps, −14 LUFS / ≤ −1.3 dBTP, both streams identical length,
  an `edl.json` that is the single source of truth, and a here.now canvas.
- **Graphics pass:** a new file per version (never overwrite an approved cut), same spec, plus
  the generator that made it (`mg/build-comp.mjs`) so every revision is regenerate-and-render.
- A SESSION_LOG entry and an ARCHITECTURE update at every milestone (hard rule for this repo).

## The pipeline

### 0. Intake — one question round, then run autonomously

Ask once, with recommendations, then build to a reviewable draft. For the base cut: take order,
what to do with an example ad's own audio (the proving run's answer: play it only when the
speaker is silent, later "start when I start talking, ad playing behind me with no sound"), music yes/no on V1. For the
graphics pass: the visual language (the proving run chose monochrome editorial — near-black
`#0E0E10`, cream `#F4F2EE`, Inter, no accent; check `MASTER_CONTEXT.md` for the user's own
tokens), **who runs the ad** (the brand's own ad account changes the brand-safety bar entirely), the music arc, and the fate of any risky lines (trademarks, unsourced numbers).
Two things the creator was emphatic about: "ask me any questions you have… this is really
important" at intake, and no questions mid-build.

### 1. Base cut — see [references/base-cut.md](references/base-cut.md)

1. Pull the takes; each one is `Take NN - Screen.mov` (5120×2880 ReplayKit, **VFR**),
   `Take NN - Camera.mov` (1920×1080) and `Take NN - Mic.wav`. Confirm A/V sync per take.
2. Transcribe every take; find the retakes and flubs; keep one clean read per line. The hard
   rule on paid deliverables: never trim approved copy for pacing, only marked alternates or flubs.
3. Write `edl.json`: one segment per shot with `take`, `in`/`out`, `layout` (cam | split | screen),
   `rect` (a named crop of the screen capture), `keep` sub-ranges, `screenOffset`, `veto`,
   `protect`, `gain`, `camX`, `flipScreen`, `joinPrev`. Rotate the three layouts by what the
   example on screen needs; put every example the speaker shows on screen while they talk about it.
4. `python3 build.py` renders one video-only segment per shot, measures each one's exact frame
   count, then builds the ENTIRE audio track in one pass to those measured lengths (per-segment
   AAC drifted 0.23s by the CTA). Two-pass loudnorm to −14.
5. `python3 tighten.py` rewrites every `keep` from the mic waveform so pauses *inside* sentences
   collapse — the "talking over myself" feel. Threshold is peak-relative
   (`max(noise+9, p95−18)`); the creator's own breath marks proved their standard 4 dB tighter than
   the first guess. Then run the QA harness: `qa/verify_cuts.ts` (A/B transcription of every cut),
   `qa/silent_gap.py`, `qa/clip_gains.py`, `qa/screen_offsets.py`.
6. Deliver on the canvas, read the notes back, apply them as EDL edits, re-render, republish to
   the same slug. Every note becomes a source-time edit found by walking the segment's `keep`
   ranges — never an output-time hack.

### 2. Graphics pass — see [references/graphics-pass.md](references/graphics-pass.md)

This is where "senior editor" shows, and where V6 failed. The base cut is a character, not a
background. The pass has its own sub-pipeline:

1. **Transcript per shot, never per cut.** Whisper on a concatenated cut drifts up to +1s;
   transcribe each shot's dry mic audio in isolation and map through the EDL
   (`scripts/transcribe-shots.ts`). Fix hallucinations on 1-second shots and clipped first words
   with a loudness-normalised re-pass. Then still expect a few onsets to be wrong — when the creator says a
   word is out of sync, measure the syllable on the waveform and hard-set it.
2. **Research before design.** What the reviewer has praised and killed across every past edit, the
   technique palette with mechanics, the real assets on disk (the Seedance library, screen
   captures to mine, the storyboard frames), the reference video extracted from the capture. Run
   these as parallel readers; the storyboard is only as good as this.
3. **Design panel, then synthesis.** Three independent storyboards from different angles, three
   judges with a rubric (the reviewer's notes, "impress a senior editor", feasibility, brand safety,
   pacing, real-asset use), one lead-editor synthesis with a build order. Do this even when it
   feels slow — the winning board was not the one a single pass would have written.
4. **Measure, then place.** `scripts/freespace.py` builds a per-shot importance map and a
   motion-based subject box from the rendered cut. Placement is a per-layout policy: cam shots
   take the top band, split shots put cards on the speaker's chest under the chin (the top half is
   the proof), screen shots use the top band and move captions above the circle. The creator also
   wanted the seam between a split's screen and their head used — "the space in the middle of the canvas".
5. **One generator** (`scripts/build-comp.mjs` is the V7/V8 template): the three-wrapper camera
   (`#vclip` clip-path | `#vwrap` x/y/scale | `#base` punch), five takeover archetypes, the
   circle-PIP hand-off to the cut's own layout, video cards, kinetic type, toggles/checks that
   press-fill-draw-ring-burst, captions on opaque pills, 80-ish SFX on words and motion, a bed
   that changes arrangement at the drop. Snapshot → look → fix, at least four rounds, before the
   first full render.
6. **Sound.** ElevenLabs kit generated, audited and normalised (a third of generations are duds;
   "pop" always came back as 0.48s of silence — derive it from the click). Two music beds
   crossfaded at the showcase so the arrangement changes, not just the gain; a gain envelope for
   the arc; the by-the-book bed level is inaudible on a phone.
7. Render (7 min, run it as a **tracked background job** — a foreground shell dies at 10 min),
   master (two-pass loudnorm, limiter 0.79–0.84, TP ≤ −1.3), the `video-qa` engine, copy review, canvas.

### 2b. Hook rebuilds — see [references/hook-rebuilds.md](references/hook-rebuilds.md)

When notes come back on the hooks after the body is locked, the body never re-renders: it is stream-copied
bit-identical into every deliverable. Hooks cut from a long screen recording are burnt-in composites with the
speaker's webcam already baked in, so the composite becomes the camera subject (one wrapper, named crops, the
bubble cut from its own circle) and every crop is bounded by that burnt-in circle. One config per hook, one
generator, and a fan-out of one agent per hook — which doubles as a review panel: the defects worth having
are the ones several agents report about the *approved* layout.

### 3. Review loop — see [references/review-loop.md](references/review-loop.md)

Reply leads with the canvas URL every round. Read every note back with `read-notes.mjs`, seek to
the frame before deciding what it means, and treat a note as a calibration of the reviewer's taste,
not a one-off: their breath marks re-tuned the silence threshold globally; "no full-screen takeovers"
re-wrote the face rule; "captions hard to read" became opaque pills everywhere.

### 4. Gates — see [references/brand-safety.md](references/brand-safety.md)

A final copy review is the last reader of every typeset word, and it earns it: on the proving run it caught a CTA that could
not function from the advertiser's account, a model name with no receipt, an unsourced 99% at
hero size, and the banned "not X, it's Y" beat rendered as a visual. The `video-qa` engine measures
the file, not the log — it found four overlapped frames a snapshot pass missed.

## Hard rules that are specific to this lane

- **Never cover the speaker's face.** Unconditional. Full-screen takeovers are *expected* on a
  brand-run ad and usually unwelcome on a creator's own organic reels; decide which regime you are
  in at intake (and check `MASTER_CONTEXT.md` for the user's rule).
- **Never re-whisper the render.** Per-shot transcripts through the EDL, always.
- **Measure, don't guess:** face points, crop scales (cam→split is exactly 0.50, split→circle 0.40),
  silence thresholds, word onsets, the popup rectangle the reference video flies back into. Every
  "circles aren't where they should be" in review history was a guessed geometry.
- **New version = new file** (`arcads-ad-v7.mp4`, `-v8`…); the canvas keeps one slug across rounds.
- **A render longer than ~8 minutes runs as a tracked background job.** Two renders died with the
  foreground shell's timeout; a third was `pkill`ed at 2237/2802 frames by a wait loop.

## Reference index

| File | Read when |
|---|---|
| [references/base-cut.md](references/base-cut.md) | ingesting takes, writing the EDL, tightening, the QA harness, applying base-cut notes |
| [references/graphics-pass.md](references/graphics-pass.md) | the whole motion-graphics pass: research, design panel, camera, takeovers, captions, sound, render |
| [references/review-loop.md](references/review-loop.md) | publishing to the canvas, reading notes, what the creator's notes have meant, the measurement-first fix pattern |
| [references/brand-safety.md](references/brand-safety.md) | before the copy review, and whenever a brand will run the ad from its own account |
| [references/hook-rebuilds.md](references/hook-rebuilds.md) | rebuilding N hooks onto a body that is already signed off (burnt-in composites, per-hook configs, fan-out) |
| [references/gotchas.md](references/gotchas.md) | before starting, and whenever a frame looks wrong |
| `scripts/` | the exact tools, copied into `<project>/` and `<project>/mg/` and run from there |
| `assets/` | the real `edl.json`, SFX kit, canvas config and b-roll prompt from the shipped ad |

Requires: ffmpeg/ffprobe (any build — all text is HyperFrames, no libass/drawtext needed;
`FFMPEG`/`FFPROBE` env vars override PATH), node ≥ 20 + `npx hyperframes`, `OPENAI_API_KEY`
(per-shot Whisper), `ELEVENLABS_API_KEY` (SFX + music), `ARCADS_BASIC_AUTH` or `ARCADS_API_KEY`
in `.env` for generated clips (see `arcads-broll`), here.now credentials, and the
`video-review-canvas`, `video-qa` and `branded-ad-edit` skills alongside, plus a final copy-review
pass on every typeset word.
