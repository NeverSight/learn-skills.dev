---
name: motion-video
description: Produce beat-synced 1080p motion-graphic videos in HyperFrames (HTML + GSAP) with an AI voice-over, Vietnamese karaoke captions, SFX and generated music, in one of two proven styles (glass keynote or Spider-Verse-style comic). Use when the user asks for a launch/release/feature video, motion graphic, animated explainer or promo clip, or a restyle of an existing one.
user-invocable: true
when_to_use: "Use when asked to make or restyle a motion-graphic/launch/changelog/explainer video with voice-over, captions and music synced to the beat, e.g. 'làm video motion graphic giới thiệu release', 'làm thêm bản phong cách comic', 'thêm nhạc nền đúng beat', 'render bản nén để đăng social'. Not for talking-head editing, AI text-to-video clips (Seedance/Veo) or React/Remotion projects."
category: media
keywords: [motion-graphic, video, hyperframes, gsap, launch-video, voice-over, captions, karaoke, beat-sync, elevenlabs, gemini-tts, multix, spider-verse, comic, keynote, social-encode]
metadata:
  author: BestAgentKits
  version: "1.0.0"
license: MIT
---

# Motion video

Make a 1920×1080 30 fps motion-graphic video where the scene cuts land on the
music's beats, reveals land on spoken words, and the audio is broadcast-clean.
The workflow is fully scripted: facts → script → multix audio → forced
alignment → beat grid → bar-spliced music → timeline + mix → HTML composition →
lint/check/snapshot → render → remux → social encode.

Two finished editions show what each style should feel like. Their working
projects are deliberately not bundled here: the generated voice-over, music and
SFX are large and provider-licensed. Study the published demo, then build every
new video from `assets/templates/index-skeleton.html` plus the style reference.

| Style | Style reference | Public demo | Feel |
|---|---|---|---|
| Comic multiverse | `references/style-comic-spiderverse.md` | [Dewee v3.34 comic edition](https://x.com/goon_nguyen/status/2103332658151555231), the 151 s social encode | loud, playful, hand-made |
| Glass keynote | `references/style-glass-keynote.md` | the 144 s edition of the same release | premium, calm, clear |

## Scope

This skill handles:
- New videos in either style, restyles of an existing video as a separate project,
  and partial reworks (new music, re-timed drops, re-mix, re-render, social encode).
- Audio through the `multix` CLI: Gemini TTS voice, ElevenLabs SFX, ElevenLabs
  Music composition plans, ElevenLabs forced alignment.

This skill does NOT handle:
- Generative text-to-video footage (use `multix` Seedance/Veo directly).
- React/Remotion compositions or generic HyperFrames questions (use the
  hyperframes or remotion skills).
- Publishing to social accounts: produce the file and let the user post it.

## How to work

1. Pin the outcome before touching files: topic and sources, style (one of the
   two, or a new one derived from them), duration, voice language (English VO +
   Vietnamese captions by default), ending, signature. Ask only if the style or
   the facts source is unknown.
2. Create `assets/videos/<slug>/` (never overwrite a finished edition) and a plan
   under `plans/` following the repo convention. Copy the templates from
   `assets/templates/` of this skill: `scripts/*.mjs`, `data/*.example.json`
   (rename to `.json`), `hyperframes.json`, `index-skeleton.html` as
   `index.html`, plus `scripts/fit-beat-grid.py`.
3. Follow `references/production-pipeline.md` step by step. Each step writes a
   file the next one reads, so do not reorder them.
4. Get the music right with `references/audio-and-beat-sync.md`: fit the grid,
   splice bars so the drops land where the script needs them, verify the splice,
   and measure the voice/music balance.
5. Build `index.html` with `references/composition-contract.md` and the chosen
   style reference, starting from `assets/templates/index-skeleton.html`. When a
   scene type repeats (stats, diagrams, charts, terminal, graph, outro), follow
   the demo's choreography for that scene instead of inventing a new one.
6. Finish only when every check in "Done when" passes; report measured numbers,
   not impressions.

Keep credentials inside multix's own config. Never print API keys or copy them
into project files, plans or reports.

## Done when

- `hyperframes lint` and `check` pass; snapshots of every scene were reviewed.
- `verify-arrangement.py` reports every segment within ±2 ms and
  `measure-mix-balance.py` shows the music ~4–6 dB under speech.
- ffprobe: 1920×1080, 30 fps, expected duration, AAC 48 kHz stereo;
  ebur128 ≈ −14 LUFS with peak ≤ −1 dBFS; blackdetect finds nothing outside fades.
- `build-timeline` printed no clip/overlap/missing-word warnings.
- On-screen facts trace to the sources collected in step 1.

## Resources

- `references/production-pipeline.md`: every command from scaffold to social
  encode and studio preview, plus the rebuild table.
- `references/audio-and-beat-sync.md`: voice, SFX cues, music plans,
  bar-splice arrangement, anchors, mix numbers and the ducking pitfall.
- `references/composition-contract.md`: TIMING shape, helpers, determinism,
  scene windows, captions, mascot, renderer limits, signature.
- `references/style-glass-keynote.md` / `references/style-comic-spiderverse.md`:
  tokens, fonts, layers, components, transitions and caption look per style.
- `scripts/fit-beat-grid.py <music> [--min-bpm N --max-bpm N]`: BPM, BEAT0 and a
  per-bar kick/energy table.
- `scripts/verify-arrangement.py <project> [--tolerance-ms 2]`: splice lag per
  segment; exits 1 on drift.
- `scripts/measure-mix-balance.py <project>`: music under speech vs in gaps,
  from `build-timeline.mjs --stems`.
- `scripts/tests/`: `python -m unittest discover -s scripts/tests` (needs
  ffmpeg, numpy, scipy).
- `assets/templates/`: project scripts (`generate-audio-assets`,
  `align-voiceover`, `arrange-music`, `build-timeline`), example data files and
  the composition skeleton.
