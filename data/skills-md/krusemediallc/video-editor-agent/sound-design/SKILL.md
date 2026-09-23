---
name: sound-design
description: >
  Generate and mix the full audio pass for a video edit with ElevenLabs — an SFX kit
  (whooshes, pops, impacts, count-ups, sub-drops, risers) generated, audited for the
  ~1/3 near-silent duds, and peak-normalized to −3dB; a music bed prompted by style
  descriptors (optionally style-matched to a reference track via spectrogram + BPM
  estimation); and the proven mix levels + ffmpeg verification recipe to sit it all
  under a spoken voiceover. Use when the user asks for "sound design", "SFX", "sound
  effects on this edit", "a music bed", "background music under the VO", "add
  whooshes/impacts", "a sub drop opener", "make the music feel like this track", or
  "mix/verify the audio" — and as the sound pass inside larger edit skills
  (branded-ad-edit, cinematic edits). Produces audited audio files + mix numbers;
  voiceover generation and clip placement live in the edit skills.
---

# Sound Design

SFX + music beds for video edits, via the ElevenLabs API. The hierarchy never
changes: **the voiceover is dominant, SFX punctuate, the bed is felt, not heard.**
Every number below came from shipped edits that survived client review — treat them
as defaults, not suggestions.

## Requirements

- `ELEVENLABS_API_KEY` — export it, or put `ELEVENLABS_API_KEY=…` in a `.env` at the
  repo root. Both scripts read the environment first, then walk up from cwd looking
  for a `.env`. They error clearly if neither is set. Never hardcode the key.
- `ffmpeg` + `ffprobe` on PATH (or `FFMPEG_PATH` / `FFPROBE_PATH` env vars).
- Node >= 20 (the scripts use global `fetch`).
- `python3` (stdlib only) for the optional BPM estimator in
  [references/style-matching.md](references/style-matching.md).

## 1. SFX kit — `scripts/gen-sfx.mjs`

Endpoint: `POST https://api.elevenlabs.io/v1/sound-generation` with body
`{"text": prompt, "duration_seconds": d, "prompt_influence": 0.6}` and header
`xi-api-key`. **`duration_seconds` minimum is 0.5** — the API 400s below it (the
script clamps).

**The one non-negotiable: audit every file.** Roughly **1/3 of generations come back
near-silent or quiet.** A kit that skips the audit ships hits nobody hears. The
script automates the whole loop:

```bash
node .claude/skills/sound-design/scripts/gen-sfx.mjs kit.json sfx/
```

`kit.json` is a list of `{name, duration, prompt}` (see
[assets/kit.example.json](assets/kit.example.json) for a proven starter kit):

```json
{
  "normalize_db": -3,
  "min_peak_db": -12,
  "effects": [
    { "name": "stamp-slam", "duration": 0.8,
      "prompt": "loud heavy thud slam impact, stamp hitting a desk, punchy bass" }
  ]
}
```

Per effect it: generates → measures the peak with `ffmpeg volumedetect` → any file
peaking below `min_peak_db` is a dud, regenerated once with **"loud, punchy: "**
prepended → then the **whole kit is peak-normalized to −3dB** (quiet survivors get
auto-boosted, hot ones trimmed) so composition volume values mean the same thing for
every file. It also flags files whose first sound starts later than ~0.15s (late
onsets land off-beat — regenerate those with "sharp attack" in the prompt or trim the
head) and writes `durations.json` for the composition builder.

Prompt-writing tips that held up:

- Name the physical source + character: "stamp hitting a desk, punchy bass", not
  "impact sound". Add "single" for one-shots, "dry, no music" to stop the model
  inventing a score behind the effect.
- **Whooshes are a taste risk.** A reviewer on a shipped edit killed every
  whoosh/swoosh as "cheesy". Default transitions to silence or a soft pop; reserve
  whooshes for section cuts (see mixing rules below).
- Match sound semantics to on-screen motion: a counter draining to zero gets a
  power-down / falling pitch, never a rising tick. A rising sound on a "losing" beat
  gets flagged in review.

## 2. Music bed — `scripts/gen-music.mjs`

Endpoint: `POST https://api.elevenlabs.io/v1/music` with body
`{"prompt": "...", "music_length_ms": N}`.

```bash
node .claude/skills/sound-design/scripts/gen-music.mjs \
  --prompt "..." --seconds 32 --out music/bed.mp3
```

The script pre-checks the prompt, requests a couple of padded seconds by default,
trims to length with a fade-out, and reports duration + peak.

**ToS trap — artist names in prompts → HTTP 400** (film and brand names are likely
filtered the same way). "In the style of <famous composer>" fails; the 400 body
often includes a usable `prompt_suggestion`, which the script surfaces. Describe the
STYLE in words instead. A bed prompt should cover, in one sentence each:

- **genre** ("dark cinematic electronic underscore")
- **bpm** ("around 120 bpm")
- **drum character** ("tight punchy kick, quiet ticking hi-hats")
- **bass** ("deep sustained sub bass")
- **melody policy** ("minimal melodic content, no lead melody")
- **energy arc** ("steady energy with a gentle build in the final third")
- **mix intent** — always include verbatim: **"mixed quiet and dry to sit under a
  spoken voiceover"**
- **"no vocals"**
- **"seamless loop feel"**

To match a reference track the user hands you ("make it feel like this"), do NOT try
to name or describe the song — profile it and prompt by descriptors only. Full
workflow, including the spectrogram read and a ~30-line BPM estimator, in
[references/style-matching.md](references/style-matching.md).

Generated tracks often open with a 2–4s low-energy warm-up. If the bed must slap
from frame one (paired with a sub-drop open), scan per-second `volumedetect` means
over the first ~10s, find where energy plateaus, and cut the bed with `-ss <onset>`
plus a 0.25s fade-in.

## 3. Sub-drops / risers as openers

The single highest-impact opener: a short sub-drop under the first frame. Generate it
through the SFX endpoint (add it to `kit.json`):

```json
{ "name": "sub-drop", "duration": 1.2,
  "prompt": "massive cinematic sub bass drop, falling pitch, punchy, no music" }
```

**Verify the sub is actually there** — laptop speakers can't hear it, and the model
sometimes returns a mid-range "boom" with no real low end:

```bash
# low-band energy: max here should be within ~6dB of the file's full-band max.
# 20dB+ down = no real sub — regenerate.
ffmpeg -i sfx/sub-drop.mp3 -af "lowpass=f=120,volumedetect" -f null -

# 0–800Hz spectrogram: a real drop is a dense low block with a falling-pitch trail;
# a dud is empty below ~120Hz. Compare against a known-good drop side by side.
ffmpeg -i sfx/sub-drop.mp3 -lavfi "showspectrumpic=s=1024x400:stop=800" drop-spec.png
```

After the final render, re-check the opener window the same way
(`-ss 0 -t 1.4` + `lowpass=f=120,volumedetect` on the master).

## 4. Mixing into the composition

Order of operations matters — every ratio below assumes step 1 happened first.

1. **Loudness-normalize the VO first**, before setting any bed or SFX level:

   ```bash
   ffmpeg -i vo.wav -af loudnorm=I=-14:TP=-1.2:LRA=11 -ar 48000 vo-norm.wav
   ```

   Mixing against an un-normalized VO makes every number below wrong.

2. **Music bed: track volume ~0.13–0.18** (0–1 linear gain — HyperFrames
   `data-volume`, or the track-volume slider in any NLE). Against a loudnorm'd VO and
   a bed peaking near 0dB that puts the bed **~19–20dB under VO peaks**. Start at
   0.15; offer 0.18 as the "louder" option. In a word gap the bed should raise the
   gap's mean level by a few dB versus a no-music render — present, not competing.

3. **SFX: per-hit base volume × one kit master gain, capped.** Keep per-hit taste
   values in the ~0.28–0.5 range by type, then scale the whole kit with a single
   master gain (**~1.95** proved right for a −3dB-normalized kit against a loudnorm'd
   VO), capping the product at **0.8** so slams never bury the voice:

   | Hit type | base | × 1.95, cap 0.8 |
   |---|---|---|
   | soft whoosh | 0.28–0.35 | 0.55–0.68 |
   | pop / tick | 0.32 | 0.62 |
   | count-up / cha-ching | 0.40–0.45 | 0.78–0.80 |
   | stamp / impact / sub-drop | 0.50 | 0.80 (capped) |

   The one-number kit gain is the point: "everything a touch louder/quieter" becomes
   a single edit instead of forty.

4. **Placement rules** (each of these was learned in review):
   - Land every hit **on the exact word** ("fire" SFX on the word *fire*), not at the
     sentence start.
   - **Whooshes on section cuts only** — a whoosh on every card reads cheesy.
   - **One biggest swell per video** (usually the opener sub-drop or the final
     reveal). If everything is big, nothing is.

## 5. Verify the mix — in dB, never by ear alone

Every audio bug ever caught in this pipeline was found by measuring, not listening.

```bash
# window around a hit (hit at t=12.4, file 0.8s): start ~0.05s early
ffmpeg -ss 12.35 -t 0.9 -i final.mp4 -af volumedetect -f null -

# a quiet window — a word gap with no hits and no big VO peak
ffmpeg -ss 8.0 -t 0.8 -i final.mp4 -af volumedetect -f null -

# integrated loudness of the master
ffmpeg -i final.mp4 -af ebur128 -f null -    # read the final "I:" line
```

Expectations:

- A hit window whose peak **matches the VO's peaks** is *audible-subtle*; **+3–5dB
  over** is *punchy*. A hit window that measures the same as the quiet window means
  the hit is missing or buried — fix placement or volume.
- The quiet window should sit a few dB above the same window in a no-music render
  (the bed is present) but far below VO peaks (the bed isn't competing).
- **Integrated loudness target: ~−14 to −13 LUFS.** Much below −14, the whole mix is
  quiet for social feeds; above ~−12, the limiter is doing the mixing for you.

## Files

- [scripts/gen-sfx.mjs](scripts/gen-sfx.mjs) — kit generate → audit → retry duds → normalize → `durations.json`
- [scripts/gen-music.mjs](scripts/gen-music.mjs) — prompt check → generate → trim/fade → report
- [references/style-matching.md](references/style-matching.md) — profile a reference track (spectrogram + BPM autocorrelation) and re-prompt its style
- [assets/kit.example.json](assets/kit.example.json) — proven starter kit (12 effects incl. sub-drop)
