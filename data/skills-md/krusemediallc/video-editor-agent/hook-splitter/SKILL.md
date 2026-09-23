---
name: hook-splitter
description: >-
  Split ONE long recording that contains many separate hooks/takes into a set of
  standalone videos — one per hook — and tighten each so there is no dead air, no
  stumble, and nothing said twice. Use whenever the user hands over a single long file
  and wants the pieces cut out: "split these hooks out", "there are 20+ hooks in
  here, make them each their own video", "cut these into individual clips", "one
  video per example", "chop this composite up", "tighten these and send them to
  me". Also use for the follow-up rounds — reading the reviewer's timeline notes back off the
  review canvas and applying them. Built for the prompt→result demo shape (the creator sets
  up a prompt, plays an AI-generated video, reacts) but the machinery is general:
  any long recording of repeated takes. NOT for styling a single finished reel with
  banners/captions (reel-recut), NOT for a brand-deal graphics edit
  (branded-ad-edit), and NOT the canvas itself for a single cut
  (video-review-canvas — this skill ships its own 21-up gallery variant).
---

# hook-splitter — one long recording → N tight standalone hooks

Cuts a composite into one MP4 per hook, removes every gap and flub, and delivers the
whole set on a here.now gallery canvas where **each video has its own comment box**.

Built and proven on `Rough Cut - Composite.mov` (16:26, 21 hooks): 946s of hook spans
became 627s across 21 videos, then three feedback rounds off the canvas.

## The two rules that matter most

**1. Never trim copy for pacing.** Remove dead air, stumbles, aborted takes and
repeats. Do NOT shorten what the speaker actually said to hit a runtime. If a hook runs long
because the setup is long, ship it long and say so — the trim is the user's call. (Approved copy on a paid
deliverable is never trimmed for pacing.)

**2. Transcribe the RENDER, not just the source.** This is the single highest-value
step in the pipeline. Whisper *smooths a repeated take into one clean line* on a
full-file pass, so real doubles are invisible in every source-side transcript — but
they show up immediately in a transcript of the cut. Four of the flubs the reviewer caught on the proving
run were of exactly this kind. `scripts/qa.py` exists to catch them before the reviewer does.

## Pipeline

Everything is driven by one `hooks.json` (see `assets/hooks.example.json`). Scripts
take its path as `$1` and default to `./hooks.json`.

| # | Script | What it does |
|---|---|---|
| 1 | `probe.py` | reads the source, extracts one wav per audio stream, computes 10 ms dB envelopes, and **tells you which stream is the mic and which is the system capture** |
| 2 | `video_regions.py` | the "a video is playing" mask (see below) |
| 3 | `detect_loops.py` | where each played video **restarts** (players loop) |
| 4 | `build_mix.py` | `work/mixed.mov`: video stream-copied, audio tracks summed, loop tails muted |
| 5 | `plan.py` | `cuts.json` — speech map, gap collapse, your hook table + kills |
| 6 | `render.py` | `final/hook-NN.mp4`, one per hook |
| 7 | `qa.py` | re-transcribes every render and scans for repeats **(never skip)** |
| 8 | `build_canvas.py` | the gallery canvas → publish with `here-now` |
| 9 | `map_notes.py` | round 2+: pull the reviewer's notes back and map them to source time |

## The spine: a clean "video is playing" mask

A screen recording made with a mic **plus** system-audio capture has two audio
streams, and the system one is *digital silence* whenever nothing is playing. That
gives an exact, free mask, and the entire edit hangs off it:

- **inside a video region** → never cut. That is the only silence the brief allows.
- **outside one** → the speaker is talking; every gap collapses to a fixed residual.

`probe.py` identifies the streams by their silence fraction (the system track is
>50% digital silence; the mic never is). **Verify alignment before trusting it** —
transcribe the same 45s window from both near the start and near the end. It has been
exact so far, but a drifting mask would corrupt all 21 outputs silently.

**Only one audio stream?** Then there is no free mask. Mark the video regions by hand
in `hooks.json` (`"video_regions": [[13.2,16.45], …]`), reading them off
`scripts/probe.py --map` output plus the transcript. Everything downstream is
unchanged. Do not try to infer them from the mic track alone — the ad audio bleeds in
~22 dB down and sits right on the speech threshold.

## Delivery

`build_canvas.py` + the `here-now` publish script. It is a 21-up gallery, not the
single-video canvas: the `comments` collection carries a `hook` field so each video
gets its own box, and a note stamps that player's current frame.

**Reply LEADS with the canvas URL, every round** (see `video-review-canvas`).

Bump `version` every round so answered notes stop cluttering, and version-stamp the
filename of **every hook whose bytes changed** (`hook-04-v2.mp4`) so no one gets a
cached old cut. Delete the superseded files; verify the old name 404s.

## Read next

- `references/workflow.md` — the step-by-step, including the feedback rounds
- `references/gotchas.md` — the measured numbers and the traps that cost real time

Requires: ffmpeg/ffprobe (PATH, or `FFMPEG`/`FFPROBE` env vars), `whisper-cli` +
`ggml-large-v3.bin` (`WHISPER_CLI`/`WHISPER_MODEL`), `whisper-vad-speech-segments` + a
silero VAD model (`VAD_BIN`/`VAD_MODEL`), numpy, `OPENAI_API_KEY` for `transcribe.py`, and
here.now credentials for the gallery canvas. If an agent sandbox kills ffmpeg, re-run with
the sandbox disabled.
