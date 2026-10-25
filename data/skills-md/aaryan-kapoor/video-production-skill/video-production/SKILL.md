---
name: video-production
description: End-to-end narrated video production with research, source extraction, storyboard/script, Manim/ffmpeg visuals, TTS voiceover, QC, archival backups, and optional local/Tailscale hosting. Use when the user asks to make, create, generate, render, or produce a video, explainer, paper walkthrough, product demo, briefing, daily summary video, Manim animation, or narrated presentation.
license: MIT
metadata: {"author":"Aaryan Kapoor","homepage":"https://github.com/Aaryan-Kapoor/video-production-skill","version":"0.2.0"}
---

# Video Production

## Core Rule

Treat a video request as a finished deliverable, not a plan. Research, script, produce, render, verify, archive, and deliver or host unless blocked by missing access, missing dependencies, or an explicit user constraint.

When the user gives broad creative freedom, preserve the "go all out" standard: polished visuals, clear narrative, source-grounded claims, animated diagrams/charts, narration, caveats, and a strong takeaway.

## Compatibility

Requires Python 3.10+ and ffmpeg/ffprobe. Recommended optional tools: Manim, Kokoro or another TTS stack, poppler-utils, Pillow, and Tailscale for private hosting. Kokoro can be wired portably with `KOKORO_PYTHON`, `KOKORO_TTS_DIR`, `KOKORO_VOICE`, and `KOKORO_LANG_CODE`; do not hardcode user-specific install paths.

## Workspace Contract

Use a durable workspace. By default the helper scripts use:

```text
$VIDEO_PRODUCTION_ROOT if set, otherwise ~/video-productions/
├── jobs/<YYYY-MM-DD-HHMM-slug>/
│   ├── assets/      # durable source figures, crops, tables, screenshots
│   ├── audio/       # narration segments + final voiceover
│   ├── frames/      # QC preview frames
│   ├── src/         # Manim/Python scripts, storyboard, segments.json
│   ├── renders/     # intermediate renders
│   ├── exports/     # final videos for this job
│   ├── logs/
│   └── manifest.json
├── backups/<YYYY-MM-DD>/   # copy every finished video here
├── serve/<slug>/           # one-file hosting dirs
└── current -> jobs/latest
```

For OpenClaw, run scripts with `{baseDir}`. For other agents, resolve `scripts/...` relative to this skill folder.

Initialize every non-trivial video job:

```bash
python {baseDir}/scripts/init_video_job.py "Topic or title" --prompt "original user prompt" [--source URL_OR_PATH]
```

Archive every completed MP4:

```bash
python {baseDir}/scripts/archive_video.py path/to/final.mp4 --job "$VIDEO_PRODUCTION_ROOT/current"
```

Use `/tmp/video-production-<slug>/` only for disposable intermediates. Keep durable sources, scripts, final renders, and QC frames in the job folder.

## Standard Workflow

1. **Clarify only if necessary.** If the prompt is enough, act. Make reasonable choices for length, style, and depth.
2. **Create the job workspace.** Save prompt, source IDs/URLs, scripts, and final artifacts under the video production root.
3. **Gather sources.**
   - Paper: fetch PDF/page, extract text and page images.
   - Current/mutable topic: browse or use first-party sources.
   - Stable topic: use knowledge plus targeted verification where useful.
4. **Build a production brief.** For long/technical sources, summarize thesis, structure, figures/tables, numbers, caveats, and narrative arc before scripting.
5. **Write narration as segments.** One short spoken paragraph per scene in `src/segments.json`. Keep it conversational and educational.
6. **Generate voiceover.** Use an available TTS stack such as Kokoro, OpenAI TTS, ElevenLabs, or platform-native TTS. Normalize audio with ffmpeg loudnorm.
7. **Produce visuals.** Prefer Manim for diagrams, equations, charts, timelines, and animated mechanisms. Use ffmpeg/PIL for crops, previews, and compositing.
8. **Sync by segment timing.** Read generated audio durations and allocate scene animations to match. The final video should not drift from narration.
9. **Render and mux.** Render video, mux voiceover with AAC, export MP4 at 720p or 1080p depending time/size constraints.
10. **QC before delivery.** Extract representative frames and inspect for cropped text, unreadable charts, broken LaTeX, severe overlap, and missing audio stream.
11. **Archive and deliver.** Copy final MP4 into job exports and backups. If direct media upload fails, host only the intended video file and share the URL.

## Source-Specific Guidance

Read `references/source-playbooks.md` when the video depends on a paper, product or project material, current events, or a recurring daily summary.

Read `references/production-standards.md` when the user asks for a high-effort explainer, says "go all out", or the video should be unusually polished.

## Default Tool Patterns

### Voiceover

Prefer the bundled Kokoro helper when Kokoro is available. It accepts `src/segments.json` or a plain text file, writes one WAV per segment, combines `audio/voice_raw.wav`, normalizes `audio/voice.wav` with ffmpeg loudnorm, and records segment starts/durations in `audio/timings.json`.

```bash
# Optional portable wiring; set only what the environment needs.
export KOKORO_PYTHON=/path/to/python-with-kokoro
export KOKORO_TTS_DIR=/path/to/kokoro/repo
export KOKORO_VOICE=af_heart

python {baseDir}/scripts/synth_kokoro.py src/segments.json --out audio
```

Use `python {baseDir}/scripts/synth_kokoro.py --check` to validate Kokoro + ffmpeg availability. If unavailable, fall back to another reliable TTS stack, but preserve the same artifacts: per-segment WAVs, `audio/voice_raw.wav`, normalized `audio/voice.wav`, and `audio/timings.json`.

### Manim environment

Use a per-job or temp venv if Manim is not globally installed:

```bash
uv venv .venv
source .venv/bin/activate
uv pip install 'manim>=0.19,<0.20'
manim -qm --fps 30 src/video.py SceneName
```

Use `-ql` for draft checks, `-qm` for fast delivery, and higher quality only when needed.

### Paper asset extraction

```bash
pdftotext -layout paper.pdf paper.txt
pdftoppm -jpeg -r 200 paper.pdf assets/page
```

Crop figures/tables with PIL. Aggressively simplify dense tables into charts instead of showing tiny unreadable screenshots.

### Final mux

```bash
ffmpeg -y -i render.mp4 -i audio/voice.wav \
  -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p \
  -c:a aac -b:a 160k -shortest exports/final.mp4
```

Verify:

```bash
ffprobe -v error -show_entries format=duration,size -of default=nw=1 exports/final.mp4
ffprobe -v error -select_streams a:0 -show_entries stream=codec_name,duration -of default=nw=1 exports/final.mp4
```

### Optional private hosting fallback

If Tailscale is available:

```bash
python {baseDir}/scripts/host_video.py exports/final.mp4 --port 8791 --slug my-video
```

Then run the printed server command in the background, verify with `curl -I`, and send the URL. Host only the intended video file.

## Delivery Standards

- Final reply should be short and include the attachment/link.
- Mention duration and what is included only if useful.
- Do not leave unarchived finished videos in `/tmp` only.
- Do not claim success until render, audio stream, QC frames, and backup are verified.
