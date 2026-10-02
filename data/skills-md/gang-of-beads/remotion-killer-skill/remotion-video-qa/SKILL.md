---
name: remotion-video-qa
description: Accepting/QA-ing a rendered Remotion video — ffmpeg evidence extraction (metadata, sampled frames, scene changes, audio levels, sync) and a rubric-based visual review pass. Use before delivering any rendered video.
---

# Video QA & Acceptance

Core principle: judge the RENDERED FILE, never the Studio preview. Convert the video into evidence (metadata + frames + audio measurements), inspect, then accept or fix.

## 1. Evidence extraction

```bash
# Metadata: dimensions, fps, codec, duration, size
ffprobe -v error -show_entries format=duration,size:stream=codec_name,width,height,r_frame_rate -of json out.mp4

# Sampled frames (1fps coverage for short videos; 0.5fps or fewer for long)
ffmpeg -y -i out.mp4 -vf fps=1 qa/frames/s%03d.png

# Hard-cut detection (NOTE: does not catch gradual fades/wipes)
ffmpeg -y -i out.mp4 -vf "select='gt(scene,0.3)',showinfo" -vsync vfr qa/frames/cut_%02d.png 2> qa/scenedetect.log

# Loudness quick check (mean/max dB); expect max ≈ -1 to -6 dB, mean ≈ -18 to -30 for narrated video
ffmpeg -i out.mp4 -af volumedetect -f null - 2>&1 | grep -E "mean_volume|max_volume"

# Per-window envelope (for ducking/beat verification)
ffmpeg -i out.mp4 -af astats=metadata=1:reset=<fps/2.5> -f null - 2>&1 | grep -E "RMS level"
```

For deeper analysis (OCR, ASR captions, sudden-volume events, long-video chaptering), use the video-understanding-skill extractor pattern: metadata → sampled + scene-change frames → audio-change events → timeline, then reason over the bundle with timestamps.

## 2. Visual inspection pass (read the frames)

Check, in order:
1. **First frame & last frame**: does the video start settled (not mid-animation) and end on the intended closing composition? First/last frame bugs are the most common delivery failure.
2. **Per-scene spot check**: at least one frame per scene; verify layout, text rendering (fonts actually loaded — look for fallback serif), captions inside safe area.
3. **Transitions**: sample frames INSIDE every transition window; verify both scenes visible and no flash of background/empty frame.
4. **3D scenes**: object visible (no black canvas = GL backend worked), no flicker across consecutive frames (determinism check: same timestamp two renders should match).
5. **Text**: no clipped/overflowing lines, no missing glyphs, captions synced to expected narration moments.

## 3. Audio checks

- Stream exists and is the expected codec.
- Levels: narration max −1 to −6 dB; BGM audibly below VO (compare RMS windows over narration vs music-only spans).
- Sync: sudden-volume events (clicks, beat drops) land on the intended visual moments; extract the audio as mono 16kHz WAV and compare event timestamps against sampled frames.
- No clipping (max ≥ −0.1dB = red flag), no silence gaps where VO should be.

## 4. Determinism / regression check

- Re-render the same range twice; frames should be byte-identical (or near-identical). Differences = nondeterministic value (unseeded random, time, network) — fix before delivery.
- For design changes: `remotion still --frame=N` on key frames is a cheap regression snapshot; diff against saved baselines.

## 5. Acceptance rubric (all must pass)

- [ ] Metadata matches spec (size, fps, duration, codec)
- [ ] Every scene inspected ≥ 1 frame; fonts, captions, layout correct
- [ ] Every transition window inspected; no flashes/empty frames
- [ ] Audio present, levelled, synced; no clipping
- [ ] First/last frame intentional
- [ ] Determinism verified (repeat render matches)
- [ ] Loudness at platform target (−14 LUFS for online)
