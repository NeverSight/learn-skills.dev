---
name: remotion-rendering
description: Rendering Remotion videos — CLI flags, codecs, multi-resolution strategy (scaling compositions vs separate roots), stills, fps interpolation, and platform presets. Use when setting up or running renders.
---

# Rendering & Multi-Resolution

## Resolution strategy

- Design once, relative to `useVideoConfig()` — sizes as fractions or a scale factor `s = width / 1920`. Then:
  - Render different sizes from ONE composition with `npx remotion render --scale 0.5` (half-res) — no duplicate compositions.
  - Aspect changes (16:9 → 9:16) DO need separate compositions or a responsive layout component keyed on aspect ratio.
- Alternative used in production codebases: parallel roots (`Root.tsx` 1080p, `Root-4k.tsx` 2160p) sharing scene components but swapping constants — pick this only when the 4K build needs different assets/quality levels.
- All-or-nothing rule: any hardcoded px that bypasses the scale factor is a bug that appears only in the other resolution — grep for `fontSize: \d` and `width: \d` before rendering a second size.

## CLI essentials

```
npx remotion render <entry> <comp-id> out.mp4 [flags]
```
- `--codec`: h264 (default, universal), h265 (smaller, compatibility risk), vp9/webm, prores (editing masters), gif.
- `--crf`: h264 0–51, default 18. 14–18 archival/marketing, 18–22 normal, >24 artifacts on gradients.
- `--prores-profile=4444` for alpha channel (overlays for editors).
- `--jpeg-quality` affects frame capture quality (default 80; raise for grain-heavy or dark scenes).
- `--frames=0-90` for fast iteration; `--scale` for resolution; `--concurrency` (default = half cores; drop to 2–4 for WebGL comps).
- `--gl=angle` (macOS/Windows 3D) / `--gl=swiftshader` (CI Linux) — required for @remotion/three.
- `npx remotion still <entry> <comp> out.png --frame=N` for single-frame design checks (cheap QA during development).

## Performance budgeting

- Per-frame cost × frame count = render time. The expensive trio: CSS blur radius, large shadows, 3D postprocessing. Test-render a 5s range before full renders.
- Offthread video (`OffthreadVideo`) for embedded footage; cache-size flag `--offthreadvideo-cache-size-in-bytes` for many/large clips.
- Long videos: render in ranges and concat with ffmpeg, or use Lambda/Cloud Run rendering for parallelism.

## fps interpolation

- 30fps master is standard. For 120fps delivery: render ProRes then `ffmpeg -i in.mov -vf "minterpolate=fps=120:mi_mode=mci" out.mov` (slow; acceptable for shorts). Note synthetic frames can smear thin text — check a sample.
- Changing fps in Remotion changes all frame math (springs auto-adapt via `fps`), so retiming = re-render, not manual conversion.
- **Temporal supersampling for smooth slow motion**: write animations fps-independently (`time = frame / fps`), render at N x target fps (`--fps=120`), then average N subframes per output frame: `ffmpeg -i 120fps.mp4 -vf "tblend=average,framestep=2,tblend=average,framestep=2" -r 30 out.mp4`. Each output frame is the temporal average of continuous motion — kills judder on sub-pixel/slow moves and adds free motion blur. Render cost xN; mux original audio after. (`minterpolate` with `mi_mode=blend` is an alternative one-liner, and Remotion's `<CameraMotionBlur>` is a cheaper in-render approximation, not true subframe integration.)

## Platform presets

| Target | Size | fps | Codec | Notes |
| --- | --- | --- | --- | --- |
| YouTube/web 16:9 | 1920x1080 | 30 | h264 crf 18 | -14 LUFS audio |
| 4K master | 3840x2160 | 30 | prores or h264 crf 14 | archive; derive others via --scale |
| Shorts/Reels 9:16 | 1080x1920 | 30 | h264 crf 18 | 8–10% safe margins, captions bottom-third |
| Square feed 1:1 | 1080x1080 | 30 | h264 crf 18 | center-weighted layout |
| Editing overlay | any | match edit | prores 4444 | alpha for NLE compositing |

## Gotchas

- Render output path must not be inside `public/` (server serves it, weird caching).
- h264 output audio defaults to AAC; check the audio stream exists in ffprobe before delivering.
- Deterministic-looking but random outputs across machines usually mean an unseeded `random()`/`Math.random()` or time-based value slipped in — QA two renders byte-comparing frames if suspicious.
