---
name: youtube-transcribe
description: Absorb the knowledge in YouTube videos — find them, transcribe them with ElevenLabs Scribe v2, inspect their visuals, and digest what they actually teach. Use this whenever someone wants a video's content as text or knowledge rather than just a link — "transcribe this YouTube video", "what does this video say", "summarize/explain this talk", "pull the transcript", "get subtitles", "turn this lecture into notes", or research-style asks like "find 10-20 videos about <topic> and tell me everything", "research <topic> on YouTube", "what are people saying about <X>". Also use it when a question needs what is shown on screen (slides, charts, code, UI, product) and not only what is said — it extracts frames and, as a last resort, asks Google Gemini to describe the video. Works on any yt-dlp-supported URL. Trigger it even when the words "transcribe" or "skill" never appear but the goal is to learn from video.
license: MIT
compatibility: Needs internet, ffmpeg, and python3 (with python3-venv). ELEVENLABS_API_KEY is required for transcription; GEMINI_API_KEY is optional and only used for the visual fallback.
metadata: {"openclaw": {"requires": {"env": ["ELEVENLABS_API_KEY"]}, "optionalEnv": ["GEMINI_API_KEY"], "primaryEnv": "ELEVENLABS_API_KEY"}}
---

# YouTube Transcribe

Turn a video — or a whole topic's worth of videos — into text you can actually read and reason over. The point is not to hand back a transcript and stop; it is to **absorb what the video teaches** and report it back usefully.

Pipeline: **find → download → transcribe → (look at frames) → (ask Gemini) → synthesize.** Most tasks only need the middle. Reach for the visual steps when the spoken words are not enough.

## Setup (once per machine)

```bash
S=.claude/skills/youtube-transcribe/scripts
bash "$S/setup.sh"    # creates a venv, installs yt-dlp + elevenlabs + google-genai (idempotent)
```

If venv creation fails on Debian/Ubuntu, install `python3-venv` first (`sudo apt-get install -y python3-venv`).

**Keys:** transcription reads `ELEVENLABS_API_KEY`; the Gemini fallback reads `GEMINI_API_KEY`. Export them, or drop a `scripts/load-keys.local.sh` that resolves them however you like (the wrappers source it automatically, and it is gitignored so it never ships). Never print a key into your output.

## Mode A — one video

```bash
S=.claude/skills/youtube-transcribe/scripts
OUT=/tmp/claude/youtube-transcribe/<video-id>        # scratch; never a repo

bash "$S/download.sh"   "<url>" "$OUT" audio          # audio.mp3 + metadata.json
bash "$S/transcribe.sh" "$OUT/audio.mp3" "$OUT"        # transcript.txt + .diarized.txt + .json
```

Then **read `transcript.diarized.txt`** (timestamped, speaker-grouped) and write up what matters: the thesis, the steps/method, the concrete claims, the numbers, anything actionable. Skip the filler. If it is a tutorial, capture the actual how; if it is a talk, capture the argument and evidence.

`transcribe.sh` flags: `--no-diarize` (single speaker), `--lang spa` (hint; omit to auto-detect), `--keyterms "Kubernetes,PyTorch,yt-dlp"` (spell names/jargon right — Scribe will otherwise mangle them, which poisons the summary).

## Mode B — a topic (many videos)

Search is **free and needs no API key** — it uses yt-dlp's own search.

```bash
S=.claude/skills/youtube-transcribe/scripts

# 1. Find candidates — pick the good ones by title/channel/duration before spending transcription on them.
bash "$S/search.sh" "quantitative trading with LLMs" 20            # id | duration | channel | title
bash "$S/search.sh" "quantitative trading with LLMs" 20 --date     # sort by newest instead of relevance

# 2. Transcribe the chosen ones in one go (each lands in <OUT>/<video-id>/).
bash "$S/search.sh" "quantitative trading with LLMs" 20 --urls > /tmp/urls.txt
#   ...edit /tmp/urls.txt down to the 10-15 worth watching, then:
bash "$S/batch.sh" /tmp/claude/youtube-transcribe/topic /tmp/urls.txt
```

Be selective, not exhaustive: a 3-hour stream and a 40-second Short are rarely both worth it. Prefer substance (duration, channel authority, title specificity) over raw view count. Then read every transcript and produce **one synthesis** across all of them — the consensus, the disagreements, the best single source, and what is still unanswered — not N separate summaries.

## Seeing what is on screen

The transcript misses slides, charts, code, dashboards, product shots, and anyone pointing at "this". Two escalating tools:

**1. Frames (cheap, local).** Download the video, pull stills, and Read the JPGs.

```bash
bash "$S/download.sh" "<url>" "$OUT" video                 # video.mp4 (≤720p)
bash "$S/frames.sh"   "$OUT/video.mp4" "$OUT/frames" every 30          # one frame / 30s
bash "$S/frames.sh"   "$OUT/video.mp4" "$OUT/frames" at 00:01:20,00:04:05   # exact moments from the transcript
```

Use timestamps from `transcript.diarized.txt` to grab the exact moment someone says "as you can see here".

**2. Gemini (last resort, needs GEMINI_API_KEY).** When frames are not enough — you need the video *understood*, on-screen text read, or a direct visual question answered. Gemini ingests the YouTube URL directly (no download); for a local file it uploads first.

```bash
bash "$S/ask-gemini.sh" "<url-or-local-mp4>" "What indicators are shown on the chart at minute 4, and what are their values?"
```

Gemini is the fallback, not the default: transcription is cheaper, faster, and usually sufficient. Go to Gemini only when the answer is genuinely visual.

## Output — absorb, do not dump

Default to a tight knowledge digest, not a wall of transcript:

- **What it is:** title, channel, length, one-line framing.
- **Core knowledge:** the actual ideas/method/claims, in your own words, dense and specific.
- **Notable specifics:** numbers, names, tools, steps, quotes worth keeping (with `[mm:ss]` timestamps).
- **Caveats / what's unproven or salesy.** Many "educational" videos are funnels — say so plainly.

Keep the raw `transcript.txt` on disk and point to it; paste quotes, not the whole thing.

## Scripts

| Script | Does |
|---|---|
| `scripts/setup.sh` | Create the venv, install deps (idempotent) |
| `scripts/search.sh "<q>" [n] [--date] [--urls]` | Find videos for a topic — free, no API key |
| `scripts/download.sh <url> <out> [audio\|video\|both]` | yt-dlp audio (mp3) and/or video (≤720p) + metadata.json |
| `scripts/transcribe.sh <audio> <out> [--no-diarize] [--lang] [--keyterms]` | ElevenLabs Scribe v2 → text + diarized + raw json |
| `scripts/batch.sh <outdir> <urls-file>` | Download+transcribe many; one folder per video + manifest |
| `scripts/frames.sh <video> <out> every <sec> \| at <ts,ts>` | Extract stills to Read |
| `scripts/ask-gemini.sh <url\|file> "<question>"` | Gemini visual understanding (fallback) |

## Notes

- **Scratch only.** Media and transcripts go in `/tmp/claude/youtube-transcribe/…`, never in a repo. They can be large.
- **Scribe limits:** 3 GB / 10 h per file; 90+ languages, auto-detected. A ~12 min talk is a single call.
- **Age-restricted / members-only / private** videos may need cookies (`yt-dlp --cookies-from-browser` or `--cookies`). For Gemini, prefer uploading the downloaded file over passing a URL it cannot reach.
- **This is for learning from public videos.** Respect copyright and each platform's terms; do not republish someone's content as your own.
