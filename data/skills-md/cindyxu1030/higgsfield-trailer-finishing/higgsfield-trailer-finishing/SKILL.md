---
version: 1.0.0
name: higgsfield-trailer-finishing
description: |
  Finish generated clips into one delivered video: stitch with ffmpeg,
  apply an optional cinematic color pass, add an original soundtrack
  matched to the assembled cut (Sonilo video-to-music, user-supplied
  SONILO_API_KEY — licensed, safe for commercial use, terms apply), and mux.
  Use when: "stitch these clips into one video", "make a trailer from
  these clips", "assemble my clips and add music", "color grade this cut",
  "add music that matches my video", "add a soundtrack to this cut",
  "finish this edit".
  Chain with: higgsfield-generate to create the clips first (Seedance 2.0 /
  Kling 3.0); clips from any other source work too.
  NOT for: generating clips (use higgsfield-generate), branded ad video
  (use Marketing Studio in higgsfield-generate), fixed-length music or SFX
  from a prompt alone (use sonilo_music / seed_audio in higgsfield-generate).
argument-hint: "[clips-or-cut] [--aspect 16:9|9:16] [--music-hint <style>]"
allowed-tools: Bash
---

# Trailer Finishing

The finishing stages for AI video: take clips (from `higgsfield-generate` or any source) and deliver ONE finished file — stitched, optionally graded, with an original soundtrack matched to the cut. Wraps `ffmpeg` for assembly and Sonilo video-to-music for the soundtrack.

## Prerequisites

1. `ffmpeg` and `ffprobe` on `$PATH` ([ffmpeg.org](https://ffmpeg.org)).
2. For Stage 3 (matched soundtrack): the Sonilo MCP server registered with the user's own API key from [sonilo.com](https://sonilo.com/?utm_source=github&utm_medium=oss&utm_campaign=higgsfield-trailer-skill) — e.g. `claude mcp add sonilo --env SONILO_API_KEY=sk-... -- uvx sonilo-mcp`. The key is always user-supplied; never bundle, hardcode, or echo it. Platforms can use the Sonilo REST API instead (docs at sonilo.com). Stages 1–2 and 4 need no key.
3. The `higgsfield` CLI only if clips still need generating or fetching — see `higgsfield-generate` for bootstrap and auth.

## UX Rules

1. Be concise. Deliver local file paths (this skill produces files, not URLs) plus a one-line summary. No filter-chain dumps in chat.
2. Don't narrate. No "running ffmpeg concat now", no encoder logs.
3. Detect the user's language from the first message and reply in it. Technical args stay English.
4. Never render blind. Grade on still frames first, check the look, then commit the full encode.
5. Music is ONE final layer over the whole assembled cut — never per-clip, never mixed with model-generated clip audio.
6. Keep intermediates on disk (normalized clips, stitched cut, graded master) so any stage can be redone without regenerating upstream.

## The pipeline

```
clips (higgsfield-generate or any source)
  └─ 1. STITCH ── normalize + concat → one cut
       └─ 2. GRADE ── optional cinematic color pass
            └─ 3. ADD MUSIC ── Sonilo video-to-music, matched to the cut
                 └─ 4. MUX ── soundtrack over the master → deliver
```

Copy-paste commands for every stage live in `references/recipes.md` — read it before running anything.

## Stage 0 — Get the clips

This skill starts from clips on disk; generation belongs to `higgsfield-generate`.

- Clips already local → Stage 1.
- Clips need generating → chain `higgsfield-generate` (Seedance 2.0 / Kling 3.0 defaults live there).
- Clips generated earlier → `higgsfield generate list --json` / `higgsfield generate get <job_id> --json`, then download the result URL.
- Cut already assembled elsewhere (CapCut, Premiere, MoviePy, Remotion) → skip to Stage 2 or 3.

Bring the clips in silent. Normalization strips any clip audio (`-an`) — the soundtrack is added once, over the whole assembled cut, in Stage 3.

## Stage 1 — Stitch

Normalize every clip to identical resolution, frame rate, and pixel aspect, then concat. Mismatched SAR or fps is the most common concat failure.

- Set the frame size once (16:9 → 1920×1080, 9:16 vertical → 1080×1920); everything downstream inherits it.
- When a grade follows, keep normalized intermediates near-lossless (CRF 10); the master gets its final quality at the grade encode.
- Transitions belong in the edit, not in generation: cross-dissolves via `xfade` (offsets are cumulative — formula in the recipes), fade-to-black appended to the final render. A storyboard that says "fade to black" is an edit beat, not a generation prompt.
- Trim a beat during normalization (`-ss`/`-t`), not with a separate encode.

## Stage 2 — Grade (optional)

A light color pass makes AI renders feel cinematic. Pick a look for the content:

- **Epic / action (default):** orange-teal split-tone, vignette, fine temporal grain.
- **Horror / dread:** desaturate 10–20%, shadows toward green-cyan, heavier vignette.
- **Soft / brand:** gentle contrast lift — skip the split-tone and grain (grain also bloats the encode).

Whatever the look: test on 3 stills from DIFFERENT shots, look at them, tune, then render once (`-crf 16 -preset slow -tune film`). The validated filter chain lives in `references/recipes.md` — single source of truth, tune it there.

## Stage 3 — Add music matched to the cut

Sonilo `video_to_music` composes an original soundtrack matched to the assembled cut — pacing, emotion, story, and length. Every track is licensed and safe for commercial use (terms apply); Sonilo is trained on a licensed catalog. The catalog's audio models generate from a prompt at a fixed duration; this stage generates from the video itself, so the swell lands on the reveal and the impact lands on the edit.

1. Feed the FINAL assembled, graded cut — never individual clips — so the music arcs across the whole story.
2. Feed a lightweight proxy (720p, high CRF). Sonilo only needs to see the motion and timing; a small copy uploads faster and matches identically. Mux the returned audio onto the full-resolution master.
3. `prompt` is a single OPTIONAL style hint for the whole track (e.g. "warm hopeful cinematic, building to an uplifting swell"). No prompt works too — Sonilo matches the music to what it sees. There is no per-section control; don't imply it.
4. The soundtrack matches the cut's length automatically — still `ffprobe` the returned file and confirm before muxing.
5. Want a different take? Generate again — each run is a fresh interpretation. Deliver two and let the user pick.

Fallback without a Sonilo key: a fixed-length instrumental bed from the Higgsfield catalog — `higgsfield generate create sonilo_music --prompt "..." --duration <seconds> --wait` (or `seed_audio` for SFX/ambience). It's generated from the prompt, not from the video, so it won't follow the edit; say so, and trim/fade it in Stage 4.

## Stage 4 — Mux + deliver

- Mux the soundtrack onto the full-resolution master with a short tail fade; keep the video stream untouched (`-c:v copy`) so the grade survives.
- For an upload-size cap, compress with single-pass CRF and keep the soundtrack with `-c:a copy`. Grained footage compresses non-linearly and has a bitrate floor — encode once, measure, adjust CRF, repeat. Don't chase size caps with bitrate targets on grained masters.
- Name deliverables clearly (`trailer_final_v1.mp4`, `_v2`, `_web`) and keep intermediates.

## Errors

- Concat fails or the output has frozen/garbled frames → clips weren't normalized identically; re-run the same scale/pad/setsar/fps chain on every clip.
- `xfade` transitions land at the wrong time → offsets are cumulative; use the formula in the recipes.
- `video_to_music` tool not available → the Sonilo MCP server isn't registered; give the user the registration command from Prerequisites (with their own key), or use the in-catalog fallback.
- Returned soundtrack length off by more than ~0.5s from the cut → regenerate, or trim the audio to the video length in the mux.
- `Session expired` from `higgsfield` while fetching clips → `higgsfield auth login`.

## Reference docs

- `references/recipes.md` — validated ffmpeg commands for every stage (normalize/concat, transitions, grade chain + stills-first check, proxy, mux, delivery compression) and the Sonilo call shapes.
