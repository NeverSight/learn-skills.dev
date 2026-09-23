---
name: reel-recut
description: >-
  Recut a raw vertical talking-head reel into a finished short-form edit: a
  persistent title banner, word-synced karaoke captions, callout boxes for
  asides and comment-keyword CTAs, and tight silence-cut "talking over myself"
  pacing — all described in ONE JSON spec and rendered deterministically.
  Use when the user supplies a talking-head video and wants it edited,
  styled, or "made to match my other videos / this reference reel" — including
  "add my captions", "put the banner on it", "tighten the cuts / make it
  punchier", "cut the dead air", "add a callout when I say X", or "fix the part
  where I trip over my words". Also use to revise a reel-recut edit
  (change banner text, add/move a callout, remove a stumble, re-time captions),
  and for a graphics-free raw cut (pacing only) on brand-deal footage a
  client's editor will finish. Not for plain subtitles on untouched footage
  (embedded-captions), overlay graphic cards with the clip untouched
  (talking-head-recut), or a fully branded motion-graphics ad (branded-ad-edit).
---

# reel-recut — spec-driven short-form talking-head edit

Turns a raw (or lightly-edited) vertical talking-head reel into a finished
short-form look. The four signature elements:

1. **Persistent title banner** (top, rounded accent-color box, heavy weight, UPPERCASE, 1-2 lines)
2. **Karaoke captions** (bottom third, bold white + thick black stroke, short cleaned phrases, ~2s each)
3. **Callout boxes** for an aside or the comment-keyword CTA (mid-screen, same box style)
4. **Tight "talking over myself" pacing** — inter-phrase pauses silence-cut out so phrases butt together

The existing music/B-roll/audio are kept. The whole edit is described in ONE JSON
"spec" and rendered by `scripts/build_reel.py` in a single pass.

**The styling is spec-driven, not hardcoded.** The spec's `style` block sets the
accent color, font, weights, sizes, and positions (see `references/spec.md`). The
defaults — purple `#8030F8` boxes + Montserrat Black/ExtraBold — are **one example
creator's brand**, reverse-engineered from their reels and kept so the script runs out
of the box. Replace them with the user's brand, or capture the values off whatever
reference reel you're asked to match (sample the box color from a frame, identify the
font, note positions as fractions of frame height). `assets/spec.example.json` labels
the example values explicitly.

**Raw-cut mode (no graphics).** Omit `banner`, `captions` and `callouts` entirely and the
script skips the whole overlay pass — you get element 4 (the pacing) on its own. That is the
right shape for a first-round cut on a brand deal, where the brand's own editor finishes the
video and any overlay you add is wasted work. Pair it with `"fps": "source"` so a 60fps
master is not silently downsampled to 30 on the way to their editor.

## Environment constraints (read `references/environment.md`)

- All text is rendered with **PIL into transparent PNGs** and composited with ffmpeg
  `overlay`. This exists because some ffmpeg builds lack libass/libfreetype (`drawtext`
  and `subtitles` simply don't exist there), and it is kept because it is fully portable —
  don't rewrite it around `drawtext`.
- Graphics are pre-composed into **one overlay video** so the final render has 2 inputs.
  Do not hand-build a 30-input filtergraph — it can OOM a 16 GB machine. The script handles this.
- If an agent sandbox kills ffmpeg (SIGURG / odd exit codes), re-run with the sandbox disabled.
- ffmpeg/ffprobe come from PATH (override with `FFMPEG`/`FFPROBE` env vars). Local
  transcription uses whisper-cli + a ggml model; cloud Whisper needs `OPENAI_API_KEY`
  in a `.env` at the repo root.

## Workflow

**Source from a URL?** If the user gives a link instead of a local file (an IG reel,
TikTok, YouTube — their own or a reference to match), download it first (e.g. `yt-dlp
"<url>"`), then feed that local path in as the target/reference clip below.

The script does the deterministic rendering. Your job is the judgment: watch the
videos, write good captions, and choose the cuts. Follow `references/workflow.md`
step by step. In short:

1. **Probe + watch.** `ffprobe` both clips. Use the `claude-video-vision` plugin if
   available (`video_analyze` for scene/silence/loudness, `video_watch` for frames), or
   plain frame extraction. If matching a NEW reference, capture banner/caption/callout
   styling from it into the spec's `style` block.
2. **Transcribe.** Get the target's speech with timestamps (whisper-cli `-ojf` locally,
   or OpenAI Whisper `verbose_json` with `timestamp_granularities=["word"]` — word-level
   timing is needed for stumble removal and CTA placement).
3. **Write the spec** (copy `assets/spec.example.json`). This is where the craft is:
   - `banner`: 1-2 SHORT uppercase lines, parallel to the reference's hook.
   - `captions`: split the transcript into ~2s phrases of <= ~6 words. **Clean them**:
     drop filler ("like", "um"), fix transcription errors (whisper reliably mangles
     product/brand names — learn the user's recurring ones), and apply the user's house
     copy rules (the example brand bans em dashes in on-screen copy — use
     periods/commas). Captions are paraphrase-clean, not verbatim.
   - `callouts`: add one when the user flags an aside or a CTA ("add a callout when I
     say comment X"). Set `suppress_captions` to the caption indices that overlap, so
     the same words don't show twice.
   - `silence_cut.enabled: true` for the tight feel. FIRST confirm there's no loud
     music bed (see workflow.md) — if pauses don't drop below the noise floor, cutting
     glitches the music; lower `noise_db` or disable.
   - **Noisy source (car, cafe, fan, handheld outdoors)? `silence_cut` will silently do
     almost nothing.** It wraps ffmpeg `silencedetect`, a flat energy gate, so a source
     whose floor sits near the threshold reports a handful of pauses and misses the
     rest. Check first: if `silencedetect=noise=-30dB:d=0.15` returns only a few spans,
     or none in the back half, switch to VAD-driven `manual_cuts` planned with
     `scripts/plan_cuts.py` (see workflow.md step 2b — it targets a fixed residual gap
     per join, which is what makes the pacing read as one continuous take).
   - `manual_cuts`: `[[start,end]]` ranges (original timeline) to remove a stumble or
     a bad take. Get exact word times from the transcript.
4. **Render.** `python3 scripts/build_reel.py spec.json`. It prints the new duration +
   counts and dumps `<spec>.qa-manifest.json` next to the spec (regenerate anytime with
   `--qa-manifest-only`) — a machine-readable manifest of every cut, caption, and
   callout with source + output times.
5. **QA every seam** (workflow.md step 5b): run `scripts/verify_cuts.py` on the planned
   cuts (cut-vs-uncut transcription of the same window), spot-check seams from the
   manifest, re-transcribe the OUTPUT and read it end to end as prose, and scan for
   doubled words. Fix by editing the spec (nudge a cut ≤500ms, retime a caption),
   re-render, re-verify; stop after 3 rounds and surface what's left to the user.
6. **Deliver a phone-viewable link** (review page or file host — see environment.md),
   never just a bare path. Big masters want a 720p proxy for the player; keep the
   master on disk. Keep the original raw untouched.

Iterate by editing the spec and re-running — it's fast (a 60-75s reel renders in well
under a minute). Spec fields are documented in `references/spec.md`.

## On a PAID brand deliverable, the script is approved copy

Only remove what the script itself marks as an alternate (Hook 1 / Hook 2, alt takes) and
genuine stumbles. **Never trim approved lines to hit a runtime target** or to match a
reference ad's duration — propose the trim with timecodes and let the user decide, since
they own the client relationship. Verify every cut with a *different* transcription pass
than the one that made it, and read the surviving transcript end to end as prose.

## Style quick-reference

- The example brand (defaults): accent `#8030F8`, Montserrat (Black banner, ExtraBold
  captions/callouts, auto-downloaded from Google OFL on first run), vertical 1080x1920,
  30fps, no em dashes in on-screen copy. **Treat every one of these as replaceable** —
  set the user's own values in the spec's `style` block.
- Don't restyle the speaker or their footage; this skill edits pacing and adds graphics,
  nothing else.

## Long takes: three traps (learned on a 258 s source with 140 cuts)

1. **Long cuts use the bundled frame/sample-grid assembler.** The old select/aselect
   expression failed at ~120 keeps. `build_reel.py` now calls `scripts/cut_timeline.py`:
   keep windows snap inward to the selected CFR grid, bounded 16-span batches encode
   losslessly with PCM audio and short seam fades, then the joined video gets one AAC
   encode. It verifies actual frames, PCM samples, audio presentation duration and decode.
   Fractional FPS uses cumulative sample rounding. One-frame spans need timestamps rebuilt
   after concat, otherwise coincident timestamps collapse frames. Do not restore the long
   expression or per-span AAC approach. Existing output/work versions are protected; use a
   fresh output filename after a failed attempt. The standalone helper accepts `--keeps`
   containing `[[start,end], ...]` for raw cuts without Pillow.
2. **The manifest's remapped `words` are not a word map.** They silently drop words that sit
   near a cut edge. Derive the cut-timeline word map from a fresh transcription of the
   RENDERED cut and anchor graphics on that.
3. **Manual-cut edges from the full-file transcript are wrong by 0.1-1.0 s.** whisper pads
   sentence-final words and drifts on long files; cuts landed on "job", ate "them have not",
   and left "…chat and TikTok" hanging. Derive each edge from an isolated 10-16 s slice of
   the source around the cut (`ffmpeg -ss A -t D` then transcribe): those times were exact.
   Then re-transcribe the render and read every seam as prose; a residue that a fresh pass
   hears as a complete word ("test **and** another thing") is a clean join — accept it; a
   residue heard as a fragment is not.
   A censor bleep cannot be placed from ANY transcript. The full-file pass put the swear
   350 ms early (the tone muted the word before it); isolated slices, large-v3, put it
   100–150 ms early three times out of three and fused it with its neighbour ("fuck-ton").
   Both rounds failed the reviewer. Place it from the waveform: a 5 ms band-energy map
   (total, <1 k, 1–3 k, 3–6 k, 6–8 k Hz) shows a vowel as loud low-band frames, a stop
   closure as a fall to the floor, and a /t/ or /k/ release as a high-band burst — a
   leading /f/ can be nearly silent. Mute from the end of the previous vowel to the next
   word's burst (8 ms edges, concat of sample-exact trims, not amix), then prove it on the
   render: only the tone inside the window, the next burst intact after it.

## Seams click: declick every join, and cut both streams from the same numbers

Hard butt-joins are audible. On a 180 s cut with 116 seams the sample-to-sample jump at the
join measured **0.037 full-scale at the median, 0.27 at the worst, 47 of 116 above 0.05** — a pop
roughly every 1.5 s that the reviewer described as "the entire video is super glitchy" and that a
whisper pass (which only checks words) never sees. Measure it: dump the render to PCM and take
`max(|diff(samples)|)` in ±10 ms around each seam.

The production repair that worked: build the AUDIO in **one ffmpeg filter graph** — one `atrim` + `afade in` +
`afade out` (10 ms) per keep span, all into a single `concat=v=0:a=1` — then mux onto the video.
Result on the same 116 seams: **median 0.002, 2 above 0.05.** A graph of ~120 filter chains is
fine; it is the `select` EXPRESSION parser that has the ~120-term limit, not the graph.

The bundled assembler now implements this principle with lossless PCM batches and 3 ms
edge fades; inspect the joins and use a longer source-safe fade when the recording needs it.
The batches bound decoder/memory usage without adding per-segment AAC padding.

Two ways this goes wrong:

- **Do not encode each segment to its own file and stream-copy-concat them.** Every AAC segment
  carries encoder priming/padding, so the joined file gained ~50 ms per seam (+6.3 s over 117) —
  a stall at every cut, worse than the click it was meant to fix.
- **Do not cut video and audio with different rounding.** The concat demuxer rounds each span to
  whole frames (and drops a frame at some boundaries); sample-accurate `atrim` does not. Built
  separately, the two streams drifted 367-412 ms apart over 180 s. Use the assembler's shared
  selected CFR grid for both streams. `fps: "source"` retains the nominal source rate;
  VFR input is normalized onto that selected grid. Its inward rounding can shorten a keep
  by up to one frame on each edge, so listen at speech boundaries. Verify the per-render
  receipt and measured joins instead of treating a successful encode as proof of pacing.
