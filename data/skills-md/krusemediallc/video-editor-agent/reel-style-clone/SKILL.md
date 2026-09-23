---
name: reel-style-clone
description: >-
  Reverse-engineer a reference reel's editing style frame-by-frame into a
  replicable STYLE GUIDE plus per-line BUILD DIRECTIVES, then apply that style
  to the user's own footage. Use whenever someone hands over (or points at) an
  existing short-form video and says "edit mine like this", "clone this
  editing style", "match this reel", "why does this edit feel so good — copy
  it", "break down how this video is edited", "steal this creator's style",
  or "make my video look like [reference]". The output is analysis + a build
  plan, not a rendered video — the actual edit is built by branded-ad-edit
  (or reel-recut for the simple banner/caption look) from the directives this
  skill produces. Not for cloning a STATIC image ad (image-ad-clone), plain
  subtitles (embedded-captions), or an edit with no reference to match.
---

# reel-style-clone — forensic style extraction from a reference reel

Take a reference reel apart with ffmpeg forensics — cut detection, contact
sheets, audio spectrograms, whisper transcript — analyze the evidence
frame-by-frame (with parallel subagents when available), and synthesize a
**style guide** + **per-line build directives** that let a build skill
reproduce the style on completely different footage.

The core belief: an editing style is not a vibe, it is a countable, nameable
system — a cut density, a caption register grammar, a fixed graphic
vocabulary, one signature trick. Extract the system and you can apply it to
any script. Proven on a real style-clone delivery that went through client
review rounds.

**Read [references/method.md](references/method.md) before running the
pipeline** — it has the exact commands, the subagent prompts, the style-guide
template, and the hard-won analysis heuristics. This file is the map; that
file is the territory.

## Inputs

1. **The reference video, as a local file.** The user provides it. If they
   only have a platform URL (Instagram/TikTok/YouTube), platform downloads
   usually require the *user's own authenticated session* — ask them to
   download it themselves (screen-record as a last resort) or to provide
   their logged-in browser session; do not scrape anonymously and expect it
   to work.
2. **The user's own footage and/or script** that the style will be applied to.
   (Can arrive later — phases 1–5 need only the reference.)

## Pipeline

### 1. Probe & cut detection

`ffprobe` the reference (duration / resolution / fps). Detect hard cuts with
`select='gt(scene,0.25)',showinfo` → a list of cut timestamps **and** a PNG of
the first frame after every cut. Compute cuts/sec overall and per-section
shot lengths (hook vs body vs CTA usually pace differently). Commands:
[references/method.md](references/method.md) §2.

### 2. Frame evidence

Extract frames at 2fps scaled to 360w; tile them into 5×4 contact sheets
(20 frames = 10 seconds of video per sheet). A 60s reel becomes ~6 images an
agent can actually study. §3.

### 3. Audio evidence

Extract audio → whisper-transcribe (base model is fine — you need narration
beats, not perfect words) → render a spectrogram (`showspectrumpic`) and
waveform (`showwavespic`). From these, infer: music present or not, BPM from
kick spacing, where SFX hits land, and the energy arc (where the mix lifts
and drops). §4.

### 4. Parallel forensic analysis

When subagents are available, fan out — one agent per contact sheet
(frame-by-frame: caption typography/position/case/colors, graphic overlay
types, B-roll grammar, framing modes, grade), one agent on the cut frames
(shot-alternation grammar — what each cut *lands on*, flash/transition
tricks), one agent on the audio evidence. Solo fallback: same passes,
sequential. Prompts: §5.

### 5. Synthesize the style guide

One synthesizer merges the reports into a single guide with exactly these
sections — **PACING / CAPTIONS / GRAPHIC LANGUAGE / B-ROLL GRAMMAR / COLOR &
GRADE / SOUND DESIGN / BUILD DIRECTIVES**. Sound design is written *as an
ElevenLabs music prompt* so it is directly generatable. Build directives are
a per-line plan applying the style to the USER'S script: cut points, visuals,
caption treatment, SFX hits — matching the reference's cuts-per-second
density. Template + rules: §6–7.

### 6. Hand off to the build

Give the style guide + build directives to **branded-ad-edit** (the full
motion-graphics pipeline) — or **reel-recut** if the reference style is just
banner + karaoke captions + tight pacing. The directives are written so the
build skill can execute them without re-watching the reference.

## The five analysis lessons (why this works)

These are the difference between "purple captions, fast cuts" and a guide
that actually clones the style. Full detail in
[references/method.md](references/method.md) §8.

1. **Mode/register systems are the signature.** Editors run conditional
   rules, not constant looks — e.g. *sans-serif lowercase while the face is
   on screen, serif ALL-CAPS when a graphic replaces it*. Catch the
   condition, not just the two looks, or the clone reads wrong instantly.
2. **Count internal builds, not just cuts.** Perceived pace ≈ 2× the hard-cut
   rate, because elements pop on *within* shots (caption words, list items,
   zoom punches). A clone that matches cuts/sec but not builds/sec feels
   sluggish next to the reference.
3. **Find the once-per-video trick — and use it exactly once.** Most refs
   have one spike moment (a light-leak flash, an inverted frame, a speed
   ramp). Used once it is a signature; repeated it is a gimmick and the
   clone feels cheaper than the original.
4. **Name the recurring devices.** e.g. *screenshot-over-own-blur* (a
   screenshot floated over a blurred blow-up of itself — fills 9:16 with any
   aspect evidence) and the *blue reading-highlight* (a translucent swipe
   that paints text as the VO reads it — eye control). Devices you can name,
   you can rebuild.
5. **Say what each overlay is FOR, not just what it looks like.** "White
   serif caps on black" is copying; "the AUTHORITY register — used when the
   edit wants you to take a claim as fact" is cloning. Every graphic in the
   guide gets a *function*, so build directives can deploy it on new lines
   the reference never spoke.

## Outputs

Write into the project working directory (not into this skill):

- `style-guide.md` — the seven-section guide (§6 template)
- `build-directives.md` or a table inside the guide — per-line plan for the
  user's script
- `evidence/` — cuts list + cut PNGs, contact sheets, spectrogram, waveform,
  transcript (keep these; review rounds re-open them)

## Requirements

- `ffmpeg` / `ffprobe` on PATH
- A local whisper (`whisper-cli` + a ggml model — base is enough here), or
  `npx hyperframes transcribe` (node ≥ 20) which wraps it
- Subagents (Task tool) optional but strongly recommended for §5 fan-out
- No API keys needed for analysis. The downstream build via branded-ad-edit
  needs `ELEVENLABS_API_KEY` in a `.env` at the repo root — that's its
  requirement, documented there.
