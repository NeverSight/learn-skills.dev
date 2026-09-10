---
name: video-analyze
description: |
  Download a video from any URL (Instagram, TikTok, YouTube, direct .mp4, etc.)
  and produce a multimodal package for analysis: extracted frames aligned to a
  transcript, with a low-fidelity grid mode that tiles frames to save context.
  Use when: "analyze this video", "what happens in this clip", "transcribe and
  walk through this reel", "break down this TikTok", "watch this video for me".
allowed-tools:
  - Bash
  - Read
  - AskUserQuestion
---

## Setup check

Before doing anything else, run this to verify required tools are installed:

```bash
~/.claude/skills/video-analyze/scripts/setup.sh check
```

If it prints `NEEDS_SETUP`, ask the user:

> "I need to install `yt-dlp` via Homebrew to download videos. OK to run `brew install yt-dlp`?"

If they agree, run:

```bash
brew install yt-dlp
```

Then re-run the setup check before proceeding.

---

## Invocation

```bash
~/.claude/skills/video-analyze/scripts/run.sh <url> [flags]
```

The script prints the path to `manifest.json` on stdout when done. All progress goes to stderr.

### Flags

| Flag | Default | Description |
|---|---|---|
| `--interval <sec>` | auto | Force N seconds between frames |
| `--max-frames <n>` | 20 | Hard cap on total frames extracted |
| `--fidelity high\|low` | high | `high` = one image per frame; `low` = tile 2–4 frames into a single compressed grid |
| `--grid-size 2\|3\|4` | 4 | Frames per grid tile (only for `--fidelity low`) |
| `--skip-transcript` | off | Skip Whisper transcription entirely |
| `--out-dir <path>` | `/tmp/video-analyze/<hash>-<ts>/` | Override output directory |
| `--ig-tt-auth auto\|cookies\|apify` | auto | Auth strategy for Instagram/TikTok |

### Auto frame-interval policy

| Video duration | Default interval | ~Frame count |
|---|---|---|
| < 30 s | every 2 s | ~15 |
| 30–60 s | every 5 s | ~12 |
| > 60 s | ceil(duration / 15) | ~15 |

If the computed frame count would exceed `--max-frames`, the interval is recalculated so the count lands at exactly `--max-frames`.

### When to use low fidelity

Use `--fidelity low` when:
- The video has simple, bold visuals (tutorial slides, product demos, text overlays)
- Context budget is tight (long video with many frames)
- The user asks for a "quick overview" or "summary" rather than detailed analysis

Use `--fidelity high` (default) when:
- The video has fine visual detail (small text, complex UI, subtle motion)
- The user asks for a precise, detailed analysis
- Frame count is small (< 10 frames)

### Auth strategy for Instagram / TikTok

- `auto` (default): tries `yt-dlp --cookies-from-browser <browser>` first; if that fails and `APIFY_API_TOKEN` is set, falls back to Apify.
- `cookies`: force the browser-cookie path only; fail if it doesn't work.
- `apify`: skip yt-dlp; go straight to Apify (requires `APIFY_API_TOKEN` in env).

### Environment variables (optional)

| Variable | Effect |
|---|---|
| `OPENAI_API_KEY` | Enables Whisper transcription. If unset, the transcript is skipped with a warning and the rest of the pipeline still runs. |
| `APIFY_API_TOKEN` | Enables the Apify fallback for Instagram/TikTok. Not needed if browser cookies work. |
| `VIDEO_ANALYZE_BROWSER` | Which browser yt-dlp pulls cookies from. Default `chrome`; also `firefox`, `safari`, `edge`, `brave`, `chromium`. |
| `OPENAI_BASE_URL` | Point transcription at any OpenAI-compatible endpoint (e.g. a local faster-whisper server). Default `https://api.openai.com/v1`. |
| `WHISPER_MODEL` | Transcription model name. Default `whisper-1`. |
| `VIDEO_ANALYZE_TMPDIR` | Base directory for output. Default `/tmp/video-analyze`. |

---

## Reading the output

After the script completes, do the following in order:

### 1. Read the manifest

```bash
cat <manifest_path>
```

Or use the `Read` tool on the printed path. The manifest is JSON with this shape:

```json
{
  "source": {
    "url": "...",
    "platform": "tiktok",
    "duration_sec": 42.5,
    "downloaded_via": "yt-dlp+cookies"
  },
  "extraction": {
    "interval_sec": 3,
    "frame_count": 15,
    "fidelity": "high",
    "grid_size": null
  },
  "frames": [
    {
      "index": 1,
      "t_sec": 0.0,
      "image": "frames/0001.jpg",
      "transcript": "ok so today we are going to",
      "transcript_t": [0.0, 3.2]
    }
  ],
  "grids": [],
  "transcript": {
    "language": "en",
    "text": "Full transcript text...",
    "segments": [{ "start": 0.0, "end": 3.2, "text": "ok so today we are going to" }]
  }
}
```

`grids` is populated only in `low` fidelity mode. `transcript` is null if `--skip-transcript` was used or `OPENAI_API_KEY` is missing.

### 2. Load images

For **high fidelity**: Read each image using the `image_path` field in `manifest.frames[*]` (absolute path, ready to pass to the `Read` tool directly).

For **low fidelity**: Read each image using `manifest.grids[*].image_path`.

Always read images in index order. Use the `Read` tool (not Bash) — it renders JPEG/PNG inline in the conversation.

### 3. Analyze

For each frame/grid, after reading the image:
- Briefly describe what's happening (scene, motion, UI state, text on screen)
- Cross-reference the `transcript` field for what's being said at that moment
- Note transitions or state changes between consecutive frames
- **Flag design references**: if the frame shows a UI, layout, animation example, style reference, product visual, or anything a designer would want to reproduce, write a replication prompt block immediately below:

```
[DESIGN REFERENCE — t=Xs]
Replication prompt:
"<A dense, directive prompt written as if briefing an AI image or UI generator.
Cover every observable detail:
  - Layout: exact positioning, alignment, white space, proportions
  - Typography: font style (serif/sans/mono/display), weight, size hierarchy, letter-spacing, case (ALL CAPS / sentence), color
  - Color palette: background, foreground, accent — use hex-like descriptors (near-white #f5f5f5, charcoal black, warm off-white, etc.)
  - Visual elements: what objects/images/icons appear, their size relative to the frame, opacity, blur, drop shadow
  - Composition: single focal point vs. scattered, centered vs. off-axis, breathing room vs. dense
  - Texture / surface: flat, grainy, glossy, painterly, photographic collage, etc.
  - Motion feel (if applicable): how the elements would move — drift, snap, spiral, fade
  - Aesthetic mood: editorial, brutalist, minimal luxury, techy, organic, etc.
  Avoid vague words like 'clean' or 'modern' — describe the specific visual choices instead.>"
image_path: <absolute path>
```

Synthesize into a coherent description of the video's visual flow + audio narrative, with design-reference blocks inline at the relevant frames.

---

## Example invocations

```bash
# TikTok, default settings
~/.claude/skills/video-analyze/scripts/run.sh https://www.tiktok.com/@user/video/123

# Instagram reel, low fidelity 2x2 grid
~/.claude/skills/video-analyze/scripts/run.sh https://www.instagram.com/reel/ABC/ --fidelity low --grid-size 4

# Direct mp4 URL, no transcript, 10 frames max
~/.claude/skills/video-analyze/scripts/run.sh https://example.com/video.mp4 --skip-transcript --max-frames 10

# Long video, force 8-second interval
~/.claude/skills/video-analyze/scripts/run.sh https://youtu.be/XYZ --interval 8

# Force Apify auth (if Chrome cookies don't work for IG)
~/.claude/skills/video-analyze/scripts/run.sh https://www.instagram.com/reel/ABC/ --ig-tt-auth apify
```
