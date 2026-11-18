---
name: animation-export-presets
description: Renders a finished Remotion animation to delivery files for every target - LinkedIn feed (4:5, 1:1, 9:16, 16:9), PowerPoint embed, GIF loop, a custom size or 4K at any fps - with sourced H.264 and GIF presets, ffmpeg post-steps, an ffprobe file checker. Use when the user asks to render, export, encode or resize the video for LinkedIn, PowerPoint, GIF, a screen or resolution. Not for animating.
license: MIT
---

# animation-export-presets

Turns a rendered Remotion composition into files that play where they are going.
It fixes the failures that show up after "the render worked": yuv444p or odd-sized
MP4s LinkedIn rejects, untagged colour that shifts on some players, moov-at-the-end
files that stall, PowerPoint clips that scrub badly or show a seam, GIFs posted to
LinkedIn as a static image, and 4K rooms fed a soft 1080p upscale. Every preset
carries its source URL and date in `assets/presets.json`.

## When to use / when NOT to use

Use when the animation is done and someone needs the MP4/GIF for a platform, a
different size or fps, a fix for a file a platform or PowerPoint refused, or a check
that a delivered file matches a preset.

Do NOT use for: animating (`smooth-motion-choreography`), judging the look of frames
(`animation-frame-qa`), storyboards or layout, compressing screen recordings, deck
conversion, uploading or writing the post, or installing ffmpeg.

## Workflow

1. **Preconditions**: `animation.config.json` has `remotion_license_basis` (the
   renderer refuses otherwise), every target in it has a composition (`Root.tsx`),
   `npx remotion compositions src/index.ts` lists them, ffmpeg and ffprobe are on PATH.
2. **Pick presets** from `assets/presets.json`: `linkedin-4x5` (default feed),
   `linkedin-1x1`, `linkedin-9x16`, `linkedin-16x9`, `pptx-16x9`, `pptx-4k`, `gif-loop`,
   `custom` (composition `custom` from the storyboard's `custom_size`). Why each is
   what it is: `references/delivery-specs.md`.
3. **Render** from the project root (the script runs Remotion inside `--project`):
   ```bash
   python3 "${CLAUDE_SKILL_DIR}/scripts/render.py" --project . --preset linkedin-4x5 --preset pptx-16x9
   ```
   One master per composition (CRF 10, PNG frames, BT.709, with a sidecar recording
   the storyboard and flags it came from), then one ffmpeg pass per deliverable. Each
   deliverable is checked before it replaces `out/<preset>.mp4|gif`; a failed check
   leaves the previous file untouched. `--reuse-masters` reuses a master whose
   sidecar matches; `--input file.mp4` re-encodes an existing file (the repair path
   for "PowerPoint won't play it"); `--dry-run` prints the commands.
4. **Check any file** against its preset (the renderer already did this for what it
   published; run it on files from elsewhere or after edits):
   ```bash
   python3 "${CLAUDE_SKILL_DIR}/scripts/check_output.py" out/linkedin-4x5.mp4 --preset linkedin-4x5 --project .
   ```
   Expected size and fps come from the preset and the project's `storyboard.json`
   (`custom_size` for the custom preset). Checks: container, codec, profile, pixel
   format, even dimensions, exact fps and platform fps range, duration bounds, byte
   floor and cap, bitrate range, BT.709 tags, faststart atom order, no audio, GIF
   infinite-loop extension, full decode. Fix the source of a failure (usually the
   composition or the storyboard), never the checker.
5. **Hand off**: file paths per preset, the checker's summary, and the platform notes
   below. Next: `animation-frame-qa` looks at the frames before delivery.

## Output spec

- `out/<preset>.mp4` or `.gif` per requested preset, plus `out/masters/*.mp4`.
- `check_output.py` exits 0 for every deliverable.
- The reply states, per file, where it is meant to go and any handling note
  (PowerPoint: insert, Start Automatically, Loop until Stopped for loops, do not run
  Compress Media; LinkedIn: upload the MP4, add the credit line from `ATTRIBUTION.md`
  to the post text if one exists; GIF: README/email/desktop decks only).

## Gotchas

- LinkedIn's video platform does not accommodate animated GIFs, and PowerPoint for
  the web cannot play them. GIF is for README, email and desktop decks.
- PowerPoint on Windows and Mac plays H.264/AAC MP4; HEVC, VP9 and ProRes are not in
  Microsoft's supported list, WebM needs an extension, and alpha video is not a
  documented insert format: bake the slide background colour into the render.
- Compress Media (Windows only) re-encodes to 1080p/720p/480p and drops embedded
  subtitles; tell the presenter to leave it off.
- Remotion tags only the colour matrix; primaries and transfer are tagged in the
  ffmpeg pass (`h264_metadata` bitstream filter). Untagged video reads as BT.601 in
  some players and brand colours shift.
- LinkedIn re-encodes: CRF 18 is this skill's policy for the upload; thin saturated
  strokes and long gradients are what break in the re-encode, not bitrate. The checker
  also enforces LinkedIn's 75 KB and 192 Kbps floors that sparse vector clips can miss.
- 4K for PowerPoint is `--scale 2` on the 1080p composition, not a bigger design;
  everything scales because tokens are fractions of the frame.
- Rendering at 60 fps doubles time and no target requires it; keep the storyboard's fps.
- Remotion's free license covers individuals, companies of up to 3 people and
  non-profits; the renderer stops without a recorded basis (remotion.pro/license).

## Pointers

- `assets/presets.json` — the presets with source URLs, dates and the reason for each value.
- `scripts/render.py` — masters + checked deliverables; `--input`, `--dry-run`, `--reuse-masters`, `--self-test`.
- `scripts/check_output.py` — per-preset checks against the project's storyboard; `--self-test`.
- `references/delivery-specs.md` — LinkedIn, PowerPoint, GIF and encoding facts with sources.
