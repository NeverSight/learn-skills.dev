---
name: branded-ad-edit
description: >
  Turn a RAW talking-head video into a FINISHED, branded, motion-graphics ad for any
  brand or industry — a designed motion graphic on every spoken line, the brand's real
  colors/logo/screenshots, word-synced karaoke captions, ElevenLabs SFX + a low music
  bed, website B-roll in browser frames, dramatic full-bleed cuts, and optional hook
  A/B variants. Renders 9:16 MP4s via HyperFrames. Use this whenever someone hands over
  raw talking-head footage plus a brand and wants "the full edit", "motion graphics on
  every line", "make it look like their winning ads", "the brand-deal edit", "edit this
  like that winning ad", or an ad-ready version of a talking video — even if they never
  say "motion graphics". NOT for plain subtitles (embedded-captions), a personal
  signature reel style (reel-recut), or unbranded overlay cards (talking-head-recut) —
  this skill owns the brand-research → design → sound-design → A/B pipeline end to end.
---

# Branded Ad Edit

Raw talking-head in → finished branded ad out. The speaker's footage and audio play
**untouched, in full** (no re-cutting their words, except optional hook-splitting —
or, for multi-take raw, a best-take assembly cut FIRST, then the assembled master
plays untouched); everything else — graphics, captions, sound, framing — is built
around them, in the target brand's visual language. Proven on a real paid brand-deal
delivery, a 4-round style-clone reel, and a product-news explainer built from a
generated likeness.

**Read the reference file for each phase when you reach it** — they carry the exact
commands, contracts, and hard-won gotchas. Skim [references/gotchas.md](references/gotchas.md)
**before starting**; every entry cost real time once.

## What you produce

- 1080×1920 @ 30fps MP4 (other ratios on request), duration = source duration.
- A **framing grammar** of 4 modes the video moves between:
  - `split` — video in a bottom band (1080×840 @ y1080), 1:1 graphic square on top
  - `solo` — video centered, banner graphics above and below the speaker
  - `fullhim` — full-bleed 9:16 crop of the speaker, floating chips over footage + vignette
  - `full` — video hidden, full-screen graphic takeover (reserve for ≤3 beats)
- **One motion-graphic card per spoken line** (~15–20 for a 60–75s cut), every beat
  word-synced to the transcript.
- Karaoke captions (1–3 words, heavy sans, sentiment-colored highlights), a top
  progress bar, zoom-punches, count-ups on every number.
- Original VO dominant + ~40 SFX hits + a music bed ~19dB under voice peaks.

## Pipeline

Work through the phases in order. Verify visually at EVERY stage — extract frames /
snapshot and look at them; measure audio with `volumedetect`. Every bug this skill's
history caught was found in pixels or dB, never by re-reading code.

### 0. Intake (one question round, then run autonomously)

Collect: the raw video; the brand's website URL; reference/winning ads if any;
canvas ratio (default 9:16); layout preference (default: mixed split/solo/full-bleed/
takeover); single edit or hook A/B variants. Ask once with recommendations, then
build to a reviewable draft — humans redirect drafts well and specs poorly.

### 1. Ingest & crops (+ assembly cut for multi-take raw)

Probe the source (`ffprobe`: duration, resolution, fps). **If the raw is a multi-take
line-by-line read** (a 4min file for a 70s script), build a best-take master first:
`silencedetect` → speech-segment map → transcribe each segment IN ISOLATION (gotcha
#18: whisper on continuous audio dedupes back-to-back retakes and hides them) → flag
slow-rate segments (<1.6 w/s = probable false start) → keep one take per line → cut
with an ffmpeg trim/concat filtergraph, writing an **EDL JSON** (`raw_start/raw_end/
master_start/master_end` per window) — every later revision and caption depends on it.
Re-transcribe the assembled master too: each pass catches flubs the other hides.

Then TWO crops of a 16:9 source: the 1080×840 "band" crop and a tight 1080×1920
full-bleed crop. Extract a frame of each and LOOK — center on the face by eye, not
math. **Re-encode everything with `-g 30 -keyint_min 30`** (sparse-GOP media freezes
on seek in the renderer). Commands: [references/composition.md](references/composition.md) §1.

### 2. Transcribe

For an uncut source: `npx hyperframes transcribe audio.mp3 -d <dir> --json --model
small.en` → flat word array `[{text, start, end}]`. **For ANY cut-up source (assembly
cut or revision cuts): never caption from whisper-on-the-cut** — it drifts up to +1s
late by the back half (gotcha #19). Instead transcribe every EDL window as an isolated
clip and stitch: `master_time = window.master_start + clip_time`. Fix ASR errors in
place (brand names!), merge split brand mentions, group into sentences (≈ one card
each), clamp ends to media duration.

### 3. Brand research

Scrape the live site for a color histogram + logo files; screenshot it and look.
Build the token block (`--brand-accent`, `--bg-dark`, semantic green/red/gold…).
Pull REAL assets (screenshots, dashboards, metrics) from any brand folder — real
screenshots read as proof, recreations read as ads. If a winning-ads board exists,
study it and clone the recurring *moves*, not the pixels.
Details: [references/design.md](references/design.md) §1–2.

### 4. Website B-roll

4–6 clips (3–6s) of the brand's site scrolling smoothly, captured clean via a kiosk
system-Chrome + scripted eased scrolling, recorded or screencast, then cut with dense
keyframes. Played inside a browser-chrome frame in the composition. Recipe + the
capture gotchas (keychain dialogs, chat widgets, ancestor-div scroll traps):
[references/design.md](references/design.md) §3.

### 5. Storyboard

Map each sentence to a mode + a card archetype + word-timestamps for every internal
beat. The 12 proven archetypes (WRONG-stamp screenshot, count-up cost, before/after
bracket, word-synced checklist, icon tiles + stat, strikethrough list → answer,
one-word takeover, ring timer, brand reveal + B-roll, social-proof count-up,
guarantee shield, CTA card) generalize to any industry:
[references/design.md](references/design.md) §4. Write `storyboard.json` (planning
artifact) before authoring HTML.

### 6. Build the composition

Two files: a hand-authored `index-template.html` (cards + one paused GSAP timeline,
with `{{CAPTION_SPANS}}` / `{{CAPTION_TWEENS}}` / `{{SFX_ELEMENTS}}` placeholders)
and a build script that injects generated content. **Start from
[assets/index-template-starter.html](assets/index-template-starter.html)** — a
contract-compliant skeleton (backdrop, both video wrappers, vignette, progress bar,
timeline helpers, caption CSS) with «FILL» markers; don't re-derive the boilerplate.
Hand-author the ~18 cards where design judgment lives; **generate the repetitive 90%**
(captions, SFX elements) — use [scripts/generate-captions.mjs](scripts/generate-captions.mjs).
The composition contract, framing tweens, and retention devices:
[references/composition.md](references/composition.md) §2–5. Non-negotiables: one
paused timeline on `window.__timelines`, transforms only, CSS initial-hides, unique
ids on ALL media, everything local (no network at render).

### 7. Sound design

Run [scripts/generate-sfx.py](scripts/generate-sfx.py) with a kit config — it
generates each effect, **audits for the near-silent duds** (~1/3 of ElevenLabs
generations), retries them louder, peak-normalizes the kit to −3dB, flags late
onsets, and writes `durations.json` for the builder. Then place ~40 hits as
individual audio elements landing on exact words, and generate the music bed
(~19dB under VO peaks). Prompts, mixing table, music API and the artist-name ToS
trap: [references/audio.md](references/audio.md).

### 8. QA → render → verify

`npx hyperframes check` until 0 errors → one multi-timestamp `snapshot` call → LOOK
at the contact sheet with vision and fix what you see → render with
`PRODUCER_BROWSER_GPU_MODE=hardware` → then run the automated 4-layer QA on the MP4
itself with the bundled engine (`tools/video-qa`; procedure and manifest shapes in the
`video-qa` skill):

```bash
npm --prefix tools/video-qa run qa:video -- --lane hyperframes --video <proj>/output.mp4 \
    --edl <proj>/edl.json \                 # picture-lock cut list (EDL shape: video-qa skill)
    --words <proj>/words-master.json --words-are-output \
    [--placement <proj>/preview/manifest.json]   # SFX/card placements if present
```

It ffprobes the FILE (never trust the render log — gotcha #6), runs blackdetect /
freezedetect (catches frozen un-synced b-roll) / scene-spike flash detection /
silencedetect / LUFS / clipping, checks every EDL seam against the output-time word
map (clipped words, duplicate phrases, butt-splice clicks — isolated seam re-probes
only, NEVER a full re-whisper of the render), and has Gemini watch+listen to a proxy
with audio intact. On the proving run it heard both documented seam flubs in the
known-dirty cut and passed the repaired one. Read `_qa/<name>/qa-report.md`;
HIGH/CRITICAL issues come with inspection packets (contact sheet + marked waveform +
transcript + audio stats). Fix within the whitelist (`tools/video-qa/README.md`),
re-render, re-run; max 3 rounds, then escalate to the user with the packet.

Then **master the audio**: any level change (especially scaling the kit per gotcha
#23) can push the mix over full scale while every individual hit still measures fine.
Measure the render with `ebur128=peak=true` and land it at ≈ −14 LUFS / ≤ −1 dBTP — a
limiter pass with `-c:v copy` fixes it in seconds without re-rendering (gotcha #30).
Still manual: the SFX audit and confirming the bed in word-gaps. **Audit SFX with a
SFX-only render**, not an A/B against a no-SFX render — if the VO is loudness-normalised
it swamps every hit in a peak or RMS window and the diff reports hits missing that are
actually present (gotcha #22).
Checklist: [references/composition.md](references/composition.md) §6.

### 9. Hook variants (optional)

If the opening stacks two hooks — or the client wants A/B — ship one version per hook
via programmatic EDL remapping (never hand-retime): cut ranges on the original
timeline, `mapTime()` everything (timeline positions, attrs, captions, SFX), excise
fully-cut cards, pre-cut media per variant, hide splices inside framing changes.
Full recipe + the immediateRender landmine: [references/variants.md](references/variants.md).

### 10. Deliver on a review canvas

New versions are NEW files — never overwrite an approved cut. Ship MP4s + the project
dir so tweaks are regenerate-and-re-render.

**The cut goes to the reviewer on a here.now review canvas, and the reply LEADS with
that URL** — use the **`video-review-canvas`** skill, which builds the player +
frame-accurate scrubber + click-the-timeline notes + a beat map from a config and reads
the notes back next round. Write the beat map straight from `storyboard.json`; naming
each card is what turns "something's off in the middle" into "at 0:14.3 the chip lands
early". A file card without the link reads as "not delivered". Then log every gotcha
you hit.

**Client revision cuts** (removing VO after the composition is built) are EDL remaps,
not hand-retimes — see [references/variants.md](references/variants.md) §Revision cuts.

## Reference index

| File | Read when |
|---|---|
| [references/gotchas.md](references/gotchas.md) | BEFORE starting, and whenever something looks wrong |
| [references/example.md](references/example.md) | at storyboard time — a real 18-card beat map that shipped, and what the client's feedback taught |
| [references/composition.md](references/composition.md) | building crops, the template, captions, QA/render |
| [references/design.md](references/design.md) | brand research, B-roll, storyboard/card design |
| [references/audio.md](references/audio.md) | SFX + music generation and mixing |
| [references/variants.md](references/variants.md) | hook A/B splitting |
| [assets/index-template-starter.html](assets/index-template-starter.html) | copy as your template's starting point |
| [scripts/generate-captions.mjs](scripts/generate-captions.mjs) | caption generation (see its header for config) |
| [scripts/generate-sfx.py](scripts/generate-sfx.py) | SFX kit generation + audit + normalize |
| the `video-qa` skill + `tools/video-qa` | the automated 4-layer QA run in step 8 |
| the `video-review-canvas` skill | delivering the cut and reading timeline notes back (step 10) |

Requires: node ≥ 20 + `npx hyperframes` (skills: `talking-head-recut` brings fonts +
gsap.min.js — run `npx hyperframes skills update talking-head-recut`), `ffmpeg`/
`ffprobe`, a local whisper for `npx hyperframes transcribe` (whisper-cli + a ggml
model), Puppeteer for B-roll/brand capture, and `ELEVENLABS_API_KEY` for sound —
export it or put it in a `.env` at the repo root (the SFX script reads either).
