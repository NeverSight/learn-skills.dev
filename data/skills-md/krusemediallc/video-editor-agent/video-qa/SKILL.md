---
name: video-qa
description: >-
  Four-layer QA for a rendered video edit — run it on any .mp4/.mov you or a pipeline just
  produced. Use when asked to QA / check / verify / audit a render or export, hunt clipped
  words, duplicate dialogue at cuts, dead air, splice clicks, black / frozen / flash frames,
  loudness (LUFS) or clipping problems, confirm a fix after a re-render, or build an
  inspection packet (contact sheet + waveform + transcript) for a suspect timestamp.
  L1 = ffmpeg/ffprobe technical checks, L2 = transcript edit-boundary checks mapped through
  the EDL, L3 = optional Gemini watch+listen pass on a 480p proxy, L4 = targeted inspection
  packets. Needs only ffmpeg/ffprobe; whisper and GEMINI_API_KEY unlock the deeper layers.
---

# video-qa — 4-layer QA for rendered video edits

A finished render is an **audio + video artifact** — roughly half of real editing mistakes
are audible, not visible (a live post-mortem on a shipped branded edit found 6 audible seam
flubs that stills-only QA missed). This skill QAs an edit without screenshot sweeps by
spending compute cheap → expensive:

```
CHEAP    L1  ffprobe/ffmpeg technical (blackdetect, freezedetect, flash frames,
             decode errors, duration-vs-intent, silencedetect + RMS envelope,
             LUFS via ebur128, clipping)
         L2  transcript edit-boundary checks on EVERY dialogue cut
             (clipped words, duplicate phrases, seam dead-air, caption coverage,
             butt-splice clicks) + isolated seam re-probes
         L3  a multimodal model watches AND listens to a 480p proxy (audio intact),
             5fps sampling, enforced JSON — tells you WHERE to look (optional)
EXPENSIVE L4 inspection packets: contact sheet + marked waveform + word-level
             transcript + audio stats for one window — verify before changing an edit
```

## Run the engine first (`tools/video-qa`)

The procedure below is implemented as a standalone node package. Install once
(`npm --prefix tools/video-qa install`), then:

```bash
# reel-recut lane — the manifest build_reel.py dumps next to the spec, + SOURCE-time words
npm --prefix tools/video-qa run qa:video -- --manifest <p>/spec.qa-manifest.json --words <p>/transcript.json

# hyperframes lane — the picture-lock EDL + OUTPUT-time words (+ optional placement manifest)
npm --prefix tools/video-qa run qa:video -- --lane hyperframes --video <p>/out.mp4 \
    --edl <p>/edl.json --words <p>/words-master.json --words-are-output [--placement <p>/preview/manifest.json]

# any mp4, no edit intent — L1 + L3 only
npm --prefix tools/video-qa run qa:video -- --video <p>/out.mp4

# a Layer-4 inspection packet for one window
npm --prefix tools/video-qa run qa:inspect -- --manifest <p>/spec.qa-manifest.json --start 31.5 --end 33.0

# check every planned graphic, then collect actual-render evidence
npm --prefix tools/video-qa run qa:storyboard -- --storyboard <p>/storyboard.json \
    --html <p>/composition.html --video <p>/out.mp4

# enforce completed technical + transcript checks before delivery
npm --prefix tools/video-qa run qa:video -- --manifest <p>/spec.qa-manifest.json \
    --require-layers technical,transcript
```

Flags: `--skip-semantic` (no Gemini), `--fps N`, `--instructions file.txt` (the original
brief, given to Gemini), `--no-cache`, `--out dir`, `--json`. Exit **0** PASS · **1**
PASS_WITH_WARNINGS · **2** FAIL. Reports land in `<video dir>/_qa/<stem>/qa-report.{md,json}`
with packets under `inspect/<issue-id>/`. Relative paths resolve from the directory you ran
the command in; `.env` is read from there first, then from this pack's root. Full flag and
environment reference: `tools/video-qa/README.md`.

Coverage is explicit in the JSON/Markdown report. Missing or degraded optional layers
produce PASS_WITH_WARNINGS; unavailable required layers produce FAIL. Technical is required
by default. `--skip-semantic` is supported and its unavailable coverage is shown. Layer
failures preserve the completed layers in a partial report. Cache fingerprints include
effective instructions, semantic FPS, thresholds, transcript configuration and source-file
identity; degraded/skipped layers are retried, not cached.

## Storyboard completeness

Save `storyboard.json` from the accepted plan before authoring HTML:

```json
{"version":1,"elements":[{"id":"proof-card","start":4,"end":8},{"id":"cta","selector":"#closing-cta","start":12,"end":15}]}
```

Each `id` is stable and unique. `selector` is optional and supports a single HTML `#id`;
it defaults to the storyboard ID. Targets or their timed ancestors use absolute output-time
`data-start` plus `data-duration` or `data-end`. The checker reports omitted/duplicate IDs,
missing schedules, zero/reversed windows, and schedules that do not cover their planned
windows. The JSON schema is `tools/video-qa/schemas/storyboard.schema.json`.

Run once against HTML before rendering and again with `--video` afterward. The latter
extracts three frames from the actual MP4 for every planned element (10%, 50%, 90% of its
window), writes indexed contact sheets and records the render hash and timestamps. Read
the samples for what should be present. A static schedule pass **does not prove rendered
visibility**: JS/GSAP, CSS/occlusion, external HTML, and nested composition offsets are not
evaluated. The report keeps `renderedVisibility: "not_verified"`; visually review the real
samples before saying a graphic appears. A missing/unreadable evidence window fails the CLI.

When the engine cannot run (no node, a lane it has no adapter for), do the layers by hand:

You (the agent) ARE the orchestrator: run the commands, parse the logs, apply the
calibration gates, write the report. Each layer is a documented procedure, not a black box.

## The three iron rules (learned the hard way)

1. **Never re-whisper the whole render and diff it.** Whisper hallucinates connective
   phrases at jump cuts and fuses words differently every run. L2 maps SOURCE-side word
   times through the EDL; suspect seams get an **isolated 5.5s window re-probe** of the
   render, arbitrated by word *presence* — never by whisper's duration numbers (word ends
   are routinely padded into pauses).
2. **The manifest comes from edit INTENT, never from analyzing the output.** Use the cut
   list / EDL / placement data the build itself produced. A manifest derived from the render
   would inherit the exact bugs QA exists to catch.
3. **Measure the FILE, never the log.** Duration, streams, loudness all come from
   ffprobe/ffmpeg on the actual output file. Render logs lie.

## Inputs

| input | required? | gives you |
|---|---|---|
| rendered video file | yes | L1 always runs |
| edit-intent manifest (EDL / cut list / placements) | strongly recommended | L2 boundary checks, intentional-region gating, stable issue anchors |
| source-time word timings (whisper of the SOURCE) | recommended | clipped-word + duplicate + caption checks |
| source footage | optional | lets you transcribe the source yourself |
| `GEMINI_API_KEY` in `.env` at repo root | optional | L3 — skip gracefully without it, never crash |

Manifest format, EDL adaptation, and the source→output word-mapping algorithm:
[references/manifest-and-edl.md](references/manifest-and-edl.md). No manifest at all →
run L1 + L3 only ("generic lane") and say so in the report.

## Procedure

Work in a scratch dir next to the video: `<video dir>/_qa/<video stem>/`.

1. **L1 — technical.** Follow [references/layer1-technical.md](references/layer1-technical.md).
   Three ffmpeg/ffprobe passes + the RMS-envelope lull scan
   (`scripts/rms_scan.py`). Timestamps from this layer are EXACT — downstream windows can
   be tight.
2. **L2 — transcript boundaries.** Follow
   [references/layer2-transcript.md](references/layer2-transcript.md). Runs on every
   dialogue cut; escalate marginal calls to isolated seam re-probes. Degrades (click checks
   only) when no word timings exist — never blocks.
3. **L3 — semantic watch+listen.** Follow
   [references/layer3-semantic.md](references/layer3-semantic.md). Build a 480p proxy with
   audio intact, upload to Gemini, get schema-enforced JSON. Skip cleanly if no key. Its
   timestamps are ±2s — its job is to tell you WHERE to look, never to be trusted blindly.
4. **Aggregate.** Merge issues; a semantic finding overlapping a deterministic finding
   (compatible defect categories plus the same event anchor, or overlapping time windows
   within 1s) is **corroborated** — raise confidence on
   both. Gemini-only issues never exceed HIGH.
5. **L4 — inspect before you touch anything.** For every CRITICAL/HIGH issue (top ~4),
   build an inspection packet per
   [references/layer4-inspection.md](references/layer4-inspection.md), look at it, and only
   then decide. Deterministic windows: pad ±0.5s. Gemini windows: pad ±1.5s.
6. **Report.** Write `qa-report.md` (+ `.json` if scripting) in the `_qa` dir: verdict,
   per-layer status, issues sorted severity-then-time, each with its stable anchor, evidence,
   and suggested fix. Packets live under `inspect/<issue-id>/`.

## Issue anchoring

Anchor issues to **stable manifest event ids** (`cut:src48.8`, `caption:12` — keys derived
from the edit's own identifiers), not timestamps. A fix that shifts the timeline moves every
timestamp but keeps the anchors, so comparing anchored issues across re-renders tells you
reliably whether something was actually fixed.

## Severity and verdict

- **CRITICAL** — corrupt/unreadable render, missing expected audio stream, hard clipping at
  0 dBFS, >1s duration mismatch. Never ship.
- **HIGH** — probe-confirmed clipped word, duplicate dialogue, unexpected black or frozen
  frames, flash frames at a seam. FAIL until fixed or explicitly overridden.
- **MEDIUM** — dead air, splice click, loudness off target, caption mismatch, SFX masking
  VO. Warn — reviewable, not blocking.
- **LOW** — informational (hot-but-unclipped master, paraphrased captions by design,
  unconfirmed suspicions). Never blocks; never auto-"fix".

Verdict: any CRITICAL/HIGH → **FAIL** · any MEDIUM → **PASS_WITH_WARNINGS** · else
**PASS** when all layers completed. Unavailable optional coverage → **PASS_WITH_WARNINGS**;
unavailable required coverage → **FAIL**. Use exit codes 0 / 1 / 2 in that order. Never call
partial checks a clean pass.

## Fix loop + auto-fix whitelist

`run QA → FAIL? → read packet → fix → re-render → re-run`. You may apply these repairs
**without asking**:

| action | limit |
|---|---|
| nudge a cut point | ≤ 500ms |
| retime a caption | to its spoken window |
| gain/level adjustment | ≤ 3dB |
| extend/trim a clip | ≤ 500ms |
| remove an accidental duplicate segment | exact duplicate only |
| add an edge fade at a splice click | 25–30ms |

Anything else — restructuring the edit, dropping content, creative changes — goes to the
user with the inspection packet (2–3s subclips beat scrubbing). **Max 3 fix→re-render
rounds**, then stop and escalate. Never loop on LOW or subjective issues.

## Calibration notes (from live runs)

- A shipped-clean reel with 49 silence-derived cuts must come back PASS with zero HIGH —
  keep a known-clean video as your false-positive canary.
- A known-dirty pre-fix edit: the L3 pass heard both documented seam flubs (a false-start
  "Because…" fragment and a re-take clip) that stills-based QA had missed.
- A repaired edit came back PASS_WITH_WARNINGS for a quiet −21 LUFS master + one splice
  click — both real observations, neither blocking. That is the system working.
- **Silence QA needs BOTH silencedetect AND an RMS-envelope pass**: breathy −28..−36dB
  lulls read as gaps to humans but sail under −38/−40dB silencedetect. Two real dead-air
  gaps in a shipped edit were only found by the envelope scan. See L1 reference.
- Silence-derived cuts (a cut whose removed region was measured silence) cannot clip
  audible speech — word "overlap" there is whisper end-padding. 40 of 49 cuts false-flagged
  on a live reel before this gate existed. Only probe-confirmed misses flag.
- L3 API 503s: retry ×3 with backoff, then mark the layer `skipped` with the reason in the
  report — never a crash.

## Dependencies

Offline regression suite: `npm --prefix tools/video-qa test`; typecheck:
`npm --prefix tools/video-qa run typecheck`. The default tests use fixed seam probes and
generated local media, including the production cut assembler's 128-span render. They do
not call an inference API, install a model, or use TTS. Live macOS TTS/transcriber integration
is a separate opt-in: `npm --prefix tools/video-qa run test:live`.

- **node >= 20** + `npm --prefix tools/video-qa install` for the engine (tsx, zod, dotenv).
- **ffmpeg / ffprobe** on PATH (or `FFMPEG_PATH` / `FFPROBE_PATH` env vars; the engine also
  looks in `/opt/homebrew/bin` and `/usr/local/bin`). Note: many
  builds lack `drawtext` — text on images goes through PIL (`scripts/draw_markers.py`).
- **whisper**, either via `npx hyperframes transcribe` (whisper.cpp under the hood; install
  with `npx hyperframes`) or a local `whisper-cli` + ggml model. Only needed for L2
  transcription/probes when no word timings were provided.
- **python3** for the helper scripts; **PIL (Pillow)** optional, only for waveform markers.
- **GEMINI_API_KEY** in a `.env` at repo root for L3 (`GEMINI_QA_MODEL` optional, default
  `gemini-flash-latest`). Missing key = L3 skipped, everything else runs.
- **OPENAI_API_KEY** (optional) — cloud whisper-1 fallback when whisper.cpp is unavailable
  (`VIDEO_QA_TRANSCRIBER=auto|whispercpp|openai|none`).
