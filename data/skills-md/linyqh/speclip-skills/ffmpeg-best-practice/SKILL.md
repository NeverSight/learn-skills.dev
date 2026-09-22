---
name: ffmpeg-best-practice
description: >
  Lean FFmpeg playbook for reliable video compression, WeChat-compatible MP4
  export, clip stitching, audio mixing, subtitle handling, and quick fallback
  decisions. Use for requests like “压缩视频”, “微信上传”, “体积太大”,
  “导出更小但别糊”, “多段素材拼接”, “字幕烧录”, and “ffmpeg 报错”.
---

# FFmpeg Best Practice

Use this skill when the task requires direct FFmpeg work and the answer should be stable, compatible, and easy to adapt.

## Scope

- Compression for smaller files without obvious quality loss
- WeChat/mobile/web-safe MP4 output
- Concat, trim, normalize, subtitle burn-in or muxing
- Audio mixing and missing-audio handling
- Hardware encode with software fallback

## Core Workflow

1. Probe input files with `ffprobe` before writing commands.
2. Check encoder availability once per machine/session.
3. Decide whether the job is stream-copy or re-encode.
4. For compression, default to `MP4 + H.264 + AAC + yuv420p + +faststart`.
5. Prefer capped CRF first; use 2-pass only for a hard file-size target.
6. Use `-map 0:a?` for optional audio and do not write `[0:a?]` inside `filter_complex`.
7. If hardware encode fails or produces oversized output, fall back to `libx264`.
8. For subtitle burn-in, first collect subtitle style/settings parameters, then convert subtitles to `.ass`, and only then run burn-in.
9. Return the command, output path, chosen profile, and key flag rationale.

## Probe First

Run for each input:

```bash
ffprobe -v error -hide_banner -show_streams -show_format -of json "INPUT"
```

Check once per machine/session:

```bash
ffmpeg -hide_banner -encoders
ffmpeg -hide_banner -hwaccels
```

Minimum checks:

- Video/audio presence
- Resolution, fps, duration, rotation
- Whether target is compatibility-first or strict-size-first
- Available H.264 hardware encoders on this machine

## Compression Rules

When the goal is “尽量小，但别太糊”:

1. Do **not** copy streams. Re-encode.
2. Keep `MP4 + H.264 + AAC + yuv420p + +faststart` as the default delivery target.
3. Prefer `CRF + maxrate + bufsize` over pure fixed bitrate.
4. Downscale before crushing bitrate.
5. Clamp fps to `24/25/30` unless higher fps is genuinely needed.
6. Use `AAC 64k~96k` for speech-heavy output, `96k~128k` for general content.
7. Never upscale just to match a target profile.

## WeChat-Compatible Core Method

Treat “微信压缩” as a compatibility-first export target, not a claim of exact parity with WeChat’s private pipeline.

- Container: `mp4`
- Video: `H.264`, `yuv420p`
- Audio: `AAC-LC`, stereo, `44.1kHz` or `48kHz`
- Delivery: `-movflags +faststart`
- Frame rate: `24`, `25`, or `30`
- Avoid 10-bit, unusual pixel formats, and fragile containers

Use this ladder as the default starting point:

```text
540p:  CRF 23, maxrate 1000k, bufsize 2000k, AAC 64k~96k
720p:  CRF 22, maxrate 1800k, bufsize 3600k, AAC 96k
1080p: CRF 21, maxrate 2800k, bufsize 5600k, AAC 96k~128k
```

Selection:

- Short side `<= 540`: keep at most `540p`
- Short side `<= 720`: keep at most `720p`
- Short side `> 720`: default to `720p`; keep `1080p` only if detail matters
- Hard upload limit: switch to 2-pass bitrate budgeting

## Command Patterns

Replace placeholders like `IN`, `OUT`, `W`, `H`, `FPS`, `CRF`, and bitrate values before running.

### 1) Fast remux, no compression

```bash
ffmpeg -y -i "IN" -map 0:v:0 -map 0:a? -c copy -movflags +faststart "OUT"
```

### 2) Web-safe baseline export

```bash
ffmpeg -y -i "IN" \
  -c:v libx264 -preset medium -crf 21 -pix_fmt yuv420p \
  -c:a aac -b:a 128k -ar 48000 -ac 2 \
  -map 0:v:0 -map 0:a? -movflags +faststart "OUT"
```

### 3) Recommended WeChat-style compression

Default to `720p / 25fps / CRF 22 / maxrate 1800k / bufsize 3600k / AAC 96k` unless the source or budget says otherwise.

```bash
ffmpeg -y -i "IN" \
  -vf "scale='min(W,iw)':'min(H,ih)':force_original_aspect_ratio=decrease:force_divisible_by=2,pad=W:H:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=FPS" \
  -c:v libx264 -preset slow -crf CRF -maxrate VMAXRATE -bufsize VBUFSIZE \
  -pix_fmt yuv420p -c:a aac -b:a ABITRATE -ar 48000 -ac 2 \
  -map 0:v:0 -map 0:a? -movflags +faststart "OUT"
```

### 4) Hard file-size target with 2-pass H.264

```text
target_total_kbps = TARGET_MB * 8192 / DURATION
target_video_kbps = target_total_kbps - audio_kbps - 32
```

```bash
ffmpeg -y -i "IN" \
  -vf "scale='min(W,iw)':'min(H,ih)':force_original_aspect_ratio=decrease:force_divisible_by=2,pad=W:H:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=FPS" \
  -c:v libx264 -preset slow -b:v VBITRATE -maxrate VMAXRATE -bufsize VBUFSIZE \
  -pix_fmt yuv420p -pass 1 -an -f mp4 /dev/null && \
ffmpeg -y -i "IN" \
  -vf "scale='min(W,iw)':'min(H,ih)':force_original_aspect_ratio=decrease:force_divisible_by=2,pad=W:H:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=FPS" \
  -c:v libx264 -preset slow -b:v VBITRATE -maxrate VMAXRATE -bufsize VBUFSIZE \
  -pix_fmt yuv420p -pass 2 -c:a aac -b:a ABITRATE -ar 48000 -ac 2 \
  -map 0:v:0 -map 0:a? -movflags +faststart "OUT"
```

On Windows, replace `/dev/null` with `NUL`.

### 5) Concat and normalize mixed clips

- Matching streams: use concat demuxer + `-c copy`
- Mixed sources: re-encode with concat filter after normalizing resolution/fps/audio
- If any clip lacks audio, generate silence first

```bash
ffmpeg -y -i "IN" -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=48000 \
  -shortest -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 128k "OUT"
```

### 6) Subtitle handling

Burn in (required order: get subtitle settings -> convert to ASS -> burn in):

Before any burn-in command, you must first obtain subtitle settings parameters such as:

- font family
- font size
- primary color
- outline/border color and width
- shadow
- alignment/position
- margins / safe area

If subtitle masking is enabled in the current workspace, you must also obtain:

- the exact subtitle mask filter snippet
- the intended visual style of the mask (translucent glass-like blur, not a black rectangle)

Do **not** burn subtitles directly from raw `.srt` or other plain subtitle sources.
Always convert to `.ass` first so style and layout are explicit and reproducible.

#### Required mask-aware burn-in workflow

When the workspace enables subtitle masking, the only correct workflow is:

1. Call `subtitle_settings` with `video_path`
2. Read the returned `subtitleMaskFilter`
3. Convert subtitles to `.ass`
4. Apply the returned mask filter **before** the `.ass` subtitle filter

Rules:

- Use the `subtitle_settings` mask filter snippet **verbatim**
- Do **not** replace it with `drawbox`, a black rectangle, or a custom gray overlay
- The expected look is a **translucent glass-like blur** that keeps the background visible while making the source subtitle unreadable
- If the user mentions the preview mask style, treat that preview style as the target appearance
- If the burn-in result visually diverges from the preview, revise the FFmpeg parameters instead of falling back to a dark overlay

Step 1: convert subtitle source to ASS:

```bash
ffmpeg -y -i "SUB_INPUT" "SUB.ass"
```

Step 2: burn in from the generated ASS file:

```bash
ffmpeg -y -i "IN" -vf "subtitles='SUB.ass'" \
  -c:v libx264 -preset medium -crf 19 \
  -c:a aac -b:a 128k -map 0:v:0 -map 0:a? -movflags +faststart "OUT"
```

Mask-aware burn in (preferred when masking is enabled):

```bash
ffmpeg -y -i "IN" \
  -filter_complex "SUBTITLE_MASK_FILTER;[masked]subtitles=filename='SUB.ass'[v]" \
  -map "[v]" -map 0:a? \
  -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p \
  -c:a copy -movflags +faststart "OUT"
```

Notes:

- Replace `SUBTITLE_MASK_FILTER` with the exact filter string returned by `subtitle_settings(video_path=...)`
- Do not hand-rewrite that filter unless the user is explicitly debugging the mask effect
- Keep the mask filter and subtitle filter in a single `-filter_complex` pipeline
- If audio exists and no audio edit is requested, prefer `-c:a copy`

Soft subtitle mux:

```bash
ffmpeg -y -i "IN" -i "SUB.srt" \
  -map 0:v:0 -map 0:a? -map 1:0 \
  -c:v copy -c:a copy -c:s mov_text -movflags +faststart "OUT"
```

## Quick Fallbacks

- `matches no streams`: replace `-map 0:a` with `-map 0:a?`
- Audio labels fail in `filter_complex`: do not use optional audio labels; pre-create silence
- `concat` parameter mismatch: pre-normalize clips to the same resolution/fps/audio layout
- Hardware encoder unavailable or output too large: fall back to `libx264`
- Output still too large: reduce to `720p` before increasing `CRF`
- VFR sync drift: normalize to CFR before audio mixing or concat

## Encoder Defaults

- macOS: `h264_videotoolbox`, fallback `libx264`
- Windows: `h264_nvenc`, then `h264_qsv`, then `h264_amf`, then `libx264`
- Best compression efficiency: `libx264 -preset slow`
- Best compatibility: `-pix_fmt yuv420p -movflags +faststart`

## Output Contract

Always return:

1. Exact command used
2. Output path
3. Chosen profile (`copy`, `web`, `540p`, `720p`, `1080p`, or `2-pass`)
4. Why key flags were chosen
5. Any fallback applied

## Safety

- Never overwrite source media in place
- Prefer absolute output paths
- Probe first when stream topology is uncertain
- Do not claim “exactly WeChat internal compression”; call it compatibility-aligned
