---
name: ffmpeg-analyse-video
description: Analyse video content by extracting frames with ffmpeg and using AI vision
  to generate timestamped step-by-step summaries. Use when user provides a video file
  and wants to understand its visual content — screen recordings, tutorials, presentations,
  footage, or animations. Triggers on "analyse this video", "what happens in this video",
  "summarise this recording", or any request involving understanding video file contents.
---

# FFmpeg Video Analysis

Extract frames from video files with ffmpeg. Delegate frame reading to sub-agents to preserve the main context window. Synthesise a structured timestamped summary from text-only sub-agent reports.

## Architecture: Context-Efficient Sub-Agent Pipeline

**Problem**: Reading dozens of images into the main conversation context consumes most of the context window, leaving little room for synthesis and follow-up.

**Solution**: A 3-phase pipeline:

```
Main Agent                          Sub-Agents (disposable context)
──────────                          ──────────────────────────────
1. ffprobe metadata        ───►
2. ffmpeg frame extraction ───►
3. Split frames into batches ──►   4. Read images (vision)
                                      Write text descriptions
                                      to batch_N_analysis.md
5. Read text files only    ◄───    (context discarded)
6. Synthesise final output
```

Images only ever exist inside sub-agent contexts. The main agent only reads lightweight text files. This cuts context usage by ~90%.

## 1. Prerequisites

```bash
which ffmpeg && which ffprobe
```

If either is missing, show platform-specific install instructions and STOP:
- **macOS**: `brew install ffmpeg`
- **Ubuntu/Debian**: `sudo apt install ffmpeg`
- **Windows**: `choco install ffmpeg` or `winget install ffmpeg`

## 2. Setup Temp Directory

```bash
# macOS/Linux
TMPDIR="/tmp/video-analysis-$(date +%s)"
mkdir -p "$TMPDIR"

# Windows (PowerShell)
# $TMPDIR = "$env:TEMP\video-analysis-$(Get-Date -UFormat %s)"
# New-Item -ItemType Directory -Path $TMPDIR
```

## 3. Extract Video Metadata

```bash
ffprobe -v quiet -print_format json -show_format -show_streams "VIDEO_PATH"
```

Extract and report: duration, resolution (width x height), fps, codec, file size, whether audio is present.

If no video stream is found, report "audio-only file" and STOP.
If file size > 2GB, warn the user and suggest analysing a time range with `-ss START -to END`.

## 4. Extract Frames

Choose strategy based on duration:

| Duration | Strategy | Command |
|----------|----------|---------|
| 0-60s | 1 frame every 2s | `ffmpeg -hide_banner -y -i INPUT -vf "fps=1/2,scale='min(1280,iw)':-2" -q:v 5 DIR/frame_%04d.jpg` |
| 1-10min | Scene detection (threshold 0.3) | `ffmpeg -hide_banner -y -i INPUT -vf "select='gt(scene,0.3)',scale='min(1280,iw)':-2" -vsync vfr -q:v 5 DIR/scene_%04d.jpg` |
| 10-30min | Keyframe extraction | `ffmpeg -hide_banner -y -skip_frame nokey -i INPUT -vf "scale='min(1280,iw)':-2" -vsync vfr -q:v 5 DIR/key_%04d.jpg` |
| 30min+ | Thumbnail filter | `ffmpeg -hide_banner -y -i INPUT -vf "thumbnail=SEGMENT_FRAMES,scale='min(1280,iw)':-2" -vsync vfr -q:v 5 DIR/thumb_%04d.jpg` |

For thumbnail filter, calculate `SEGMENT_FRAMES = total_frames / 60` to cap output at ~60 frames.

**Fallbacks:**
- Scene detection yields 0 frames → retry with interval at 1 frame/5s
- More than 100 frames extracted → subsample evenly to 80
- Frame extraction fails → try the next simpler strategy (scene → interval, keyframe → interval)

**Time range analysis:** When user specifies a range, prepend `-ss START -to END` before `-i`.
**Higher detail mode:** If requested, double the fps rate and lower scene threshold to 0.2.

After extraction, list all frame files and calculate each frame's timestamp from its sequence number and the extraction rate.

## 5. Delegate Frame Analysis to Sub-Agents

**This is the critical context-saving step.** Do NOT read frame images in the main conversation. Instead, split frames into batches and delegate each batch to a sub-agent.

### 5a. Prepare Batch Manifest

Split the extracted frame file list into batches of 8-10 frames each. For each batch, record:
- Batch number (1, 2, 3, ...)
- Frame file paths (absolute)
- Frame timestamps (calculated from sequence number)
- Output file path: `TMPDIR/batch_N_analysis.md`

### 5b. Spawn Sub-Agents

For each batch, spawn a sub-agent with the prompt below. **Launch all batches in parallel** where the tool supports it — they are fully independent.

#### Sub-Agent Prompt Template

Use this prompt verbatim, substituting the placeholders:

```
You are analysing frames extracted from a video file.

VIDEO: {filename}
DURATION: {duration}
BATCH: {batch_number} of {total_batches}

Read each frame image listed below using the Read tool (or equivalent file reading tool that supports images). For each frame, write a structured description.

FRAMES:
{for each frame in batch}
- {absolute_path_to_frame} (timestamp: {MM:SS})
{end for}

For each frame, describe:
1. SCENE: What is visible (layout, UI elements, environment)
2. CONTENT: Text, code, labels, menus, or dialogue visible on screen
3. ACTION: What is happening or has changed since the likely previous frame
4. DETAILS: Any notable specifics (error messages, URLs, file names, button states)

After describing all frames, add a BATCH SUMMARY section with:
- Content type (one of: Screencast, Presentation, Tutorial, Footage, Animation)
- Key events in this batch's time range
- Any text/prompts/commands the user typed (quote exactly)

Write the complete analysis to: {TMPDIR}/batch_{N}_analysis.md

Format the output file as:

# Batch {N} Analysis ({start_timestamp} - {end_timestamp})

## Frame-by-Frame

### Frame {sequence} ({timestamp})
- **Scene**: ...
- **Content**: ...
- **Action**: ...
- **Details**: ...

(repeat for each frame)

## Batch Summary
- **Content Type**: ...
- **Key Events**: ...
- **Quoted Text/Prompts**: ...
```

#### How to Spawn

Use whatever sub-agent, background task, or independent agent mechanism your tool provides. The requirements are simple — each sub-agent needs to:

1. **Read image files** (the frame JPEGs)
2. **Write a text file** (the batch analysis markdown)

Launch all batches in parallel if your tool supports it — they are fully independent with no shared state.

**If your tool has no sub-agent mechanism**, fall back to reading frames directly in the main context but limit to **20 frames maximum** and warn the user about context usage.

### 5c. Collect Results

After all sub-agents complete, read the text analysis files. These are lightweight markdown — no images enter the main context.

```bash
ls TMPDIR/batch_*_analysis.md
```

Read each `batch_N_analysis.md` file **in order**. These contain only text descriptions — the context cost is minimal compared to reading the original images.

## 6. Synthesise Output

Using only the text from the batch analysis files, perform synthesis in the main context:

1. Merge all frame descriptions into a single chronological timeline
2. Group frames into natural segments (same scene, slide, or screen)
3. Detect the dominant content type across all batches
4. Identify 3-7 key moments
5. Extract all quoted text, prompts, or commands the user typed
6. Write a 2-5 sentence narrative summary

Format the output as:

```markdown
# Video Analysis: [filename]

## Metadata
| Property | Value |
|----------|-------|
| Duration | M:SS |
| Resolution | WxH |
| FPS | N |
| Content Type | [detected] |
| Frames Analysed | N |

## Timeline
### [Segment Title] (M:SS - M:SS)
Description of what happens in this segment.

### [Segment Title] (M:SS - M:SS)
Description of what happens in this segment.

## Key Moments
1. **[M:SS] Title**: Description
2. **[M:SS] Title**: Description
3. **[M:SS] Title**: Description

## Summary
[2-5 sentence narrative paragraph summarising the entire video]
```

## 7. Cleanup

Remove the temp directory after output is complete:

```bash
# macOS/Linux
rm -rf "$TMPDIR"

# Windows (PowerShell)
# Remove-Item -Recurse -Force $TMPDIR
```

Skip cleanup if the user asks to keep frames.

## Advanced Options

- **Time range**: "Analyse 2:00 to 5:00 of video.mp4" → use `-ss 120 -to 300`
- **Higher detail**: "Analyse in high detail" → double frame rate, lower scene threshold to 0.2
- **Focus area**: "Focus on the code shown" → prioritise text/code extraction in sub-agent prompts
- **Sprite sheet**: For a visual overview, generate a contact sheet:
  ```bash
  ffmpeg -hide_banner -y -i INPUT -vf "select='not(mod(n,EVERY_N))',scale='min(320,iw)':-2,tile=5xROWS" -frames:v 1 DIR/sprite.jpg
  ```

## Error Handling

- ffmpeg not found → install instructions per platform, STOP
- No video stream → report audio-only, STOP
- Scene detection yields 0 frames → fallback to interval
- Too many frames (>100) → subsample to 80
- Large files (>2GB) → warn, suggest time range
- Sub-agent fails or times out → read that batch's frames directly as fallback, warn about context usage
- Frame read failure in sub-agent → skip frame, note gap in batch analysis file
