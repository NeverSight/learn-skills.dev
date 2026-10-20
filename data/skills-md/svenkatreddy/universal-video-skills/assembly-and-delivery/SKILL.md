---
name: assembly-and-delivery
description: "Stitch AI clips into a finished video: ffmpeg concat, transitions, title cards, watermarks, subtitles, and platform exports (16:9, 9:16, 1:1). Use when individual clips exist and need to become one video."
---

# Assembly and Delivery

Generated clips are raw material, not a video. Assembly is where it becomes
one: clips joined, paced, titled, subtitled, and exported for wherever it
plays. Do it with ffmpeg and a script, not by hand in an editor. Scripts are
repeatable, and AI video projects re-render constantly.

## The workflow

1. **Verify the clips.** Same codec, resolution, and frame rate before
   joining (`references/stitching.md`). Mismatched clips are the #1 concat
   failure.
2. **Join them.** `scripts/concat.py`: checks, concatenates losslessly, and
   verifies the result. Transitions go between clips that need them, not
   everywhere.
3. **Finish it.** Title cards, watermark, burned-in or sidecar subtitles,
   credits. The small things are what make it look released instead of
   rendered.
4. **Export per platform.** 16:9 master, then 9:16 and 1:1 crops for social
   (`references/exports.md`). Never upscale; crop or pad.

## Rules that don't bend

- **Master first, always.** One full-quality 16:9 master (H.264 or H.265,
  high bitrate). Every platform export derives from the master. Never
  export a platform cut from another platform cut.
- **Check the joins.** Watch 2 seconds on each side of every cut. AI clips
  drift at their tails; the join is where it shows.
- **Transitions are punctuation.** Cuts for energy, dissolves for time
  passing, fades for beginnings and endings. A transition on every cut is
  the video equivalent of typing in all caps.
- **Audio is part of assembly.** Room tone under everything, fades on the
  master head and tail. (Full mix: `../dialogue-and-audio/references/mix.md`.)
- **Keep the project reproducible.** The concat script, the clip list, the
  subtitle file, the export commands. All in the project folder. When clip
  4 gets regenerated next week, re-running the build should take one command.
