---
name: film-assembly
description: Cut the final film with ffmpeg - normalise clips to one size/fps, join with cuts or crossfades (optionally snapped to music beats), lay narration over a ducked music bed, and export for 16:9, 9:16, 1:1 or 4:5. Use when all shots and audio are approved.
---

# film-assembly

`python scripts/assemble.py --clips s01.mp4 s02.mp4 ... --narration vo.wav --music bed.wav --aspect 16:9 --xfade 0.3 --out film.mp4 [--beats beats.txt] [--run]`

Without `--run` the script only prints the ffmpeg command. Show the command, then run it when you're ready. It needs `ffmpeg` and `ffprobe` on PATH. Pass `--durations` to skip ffprobe.

## Steps
1. Concatenate one narration line per shot into `vo.wav` (ffmpeg concat), or mix the lines per shot.
2. Scale and crop every clip to the target aspect at a fixed fps (24 by default). Use hard cuts by default and crossfades only for time jumps.
3. **Beat-snapped cuts** (for music-led films): give `--beats` a file of beat times in seconds. Each cut moves to the nearest beat. The idea comes from motionfield's beat-cut recipe (MIT).
4. **Audio:** the music is ducked under the narration with sidechain compression, and the whole mix fades out over the last 1.5 s.
5. **Repurposing:** re-run with `--aspect 9:16`, `1:1` or `4:5`. The crop is centered, so for vertical versions outpaint or reframe the key shots first with `image-edit`. See `references/fuobe-video-repurposer.md`.
6. **Captions:** make an SRT with `subtitles-captions` (`make_srt.py --manifest`), then burn it in or ship it as a sidecar.
7. After export, run `continuity-check` on the cut and do a last listen for audio clipping.

## Web-safe output
Every H.264 encode uses `-pix_fmt yuv420p -profile:v high -movflags +faststart`. ffmpeg keeps 4:4:4 (High 4:4:4 Predictive) when the input is RGB, for example PNG stills or title cards, and browsers, GitHub and Discord cannot play that, and it shows no thumbnail. 4:2:0 High profile plays everywhere, and `+faststart` puts the index at the front so the file starts streaming at once. Keep these flags in any encode you add.
