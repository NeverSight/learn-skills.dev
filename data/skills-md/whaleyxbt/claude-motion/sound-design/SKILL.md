---
name: sound-design
description: Procedural sound design with the sfx engine — writing a cue sheet against a video's timeline, which sound goes with which visual event, gain hierarchy, panning, musical key, automatic mastering to -14 LUFS, adding new generators, and verifying sync. Use when adding, changing or checking audio, SFX, music beds or loudness for any video in this repo.
---

# Sound design

Most AI-made motion graphics are silent. Sound is what makes a piece feel produced.

The `sfx/` engine synthesizes every sound in pure Python stdlib: no samples, no licenses, no installs, same output on every run. It reads the same timeline JSON as the picture, so sound can't drift out of sync.

## How it fits together

| File | Role |
|---|---|
| `sfx/synth.py` | generators: each returns mono samples at 48 kHz |
| `sfx/mix.py` | `Mix`: place sounds in time, master to a loudness target, write WAV |
| `sfx/loudness.py` | BS.1770 integrated loudness (matches ffmpeg's ebur128) |
| `sfx/cues/<video>.py` | a cue sheet: one video's sound design |

```bash
python3 -m sfx --list                   # generators with what each is for
python3 -m sfx sfx/cues/<video>.py      # render → mastered WAV
```

## Writing a cue sheet for a new video

Create `sfx/cues/<video>.py`:

```python
from sfx.synth import click, pop, whoosh, chime, riser, impact

TIMELINE = "timeline.json"      # the same file the composition reads
OUT = "public/sfx.wav"
TARGET_LUFS = -14.0             # optional, this is the default

def score(mix, tl):
    s1 = tl["s1"]
    mix.put(s1["title"], whoosh(0.4, 500, 2400, peak=0.45), 0.12)
    for i, t in enumerate(s1["items"]):
        mix.put(t, pop(900 + i * 150, 400), 0.3, pan=-0.4 + i * 0.3)
```

- `mix.put(t, samples, gain, pan)`: `t` always comes from `tl`, never a typed number. Offsets from a beat (`s1["exit"] + 0.05`) are fine.
- `mix.typing(start, end, chars)`: one humanized keystroke per character.
- `mix.put_stereo(t, left, right, gain)`: for stereo sources like `pad()`.
- Mastering is automatic: the engine soft-clips and sets gain to hit `TARGET_LUFS`, raising drive only as far as needed to keep the true peak ≤ −2 dBFS (room for AAC overshoot, so the MP4 stays under −1 dBTP). A mix that's mostly short hits with silence between can't reach −14 without crushing; the engine then comes out quieter and says so. Fix it with sustained sound (a pad, longer tails), not by forcing it.
- Add an `"sfx"` script in `package.json` pointing at the new cue sheet, or run it directly.

`sfx/cues/effort.py` is a complete, real example: 128 sounds plus a pad bed.

## Visual event → sound

| On screen | Generator | Notes |
|---|---|---|
| Typing | `mix.typing()` | jitter ±4–6 ms, random gain |
| Word / line reveal | `whoosh()` + `blip()` on the landing | short, airy |
| Badge, chip, callout pops in | `pop()` | raise pitch across a sequence |
| Control snaps to a step | `click()` + `blip()` in key | |
| Sketch / draw-on | `scratch()` | |
| Build-up | `riser()` | end exactly on the hit; one big riser per video |
| Success / arrival | `chime()` | chord in key |
| Hero transition | `whoosh()` in, `impact()` on the hit | one impact per video |
| Under everything | `pad()` with an `envelope()` | duck it under the hero transition |

Accent, don't narrate: not every motion needs a sound. Continuous motion (drift, grain, rotation) stays silent.

## Levels and space

- Hero hits: gain 0.25–0.35. Supporting sounds: 0.08–0.2. Pad: ~0.03, ducked ~65% under the hero transition.
- Pan follows on-screen position (−1 left … +1 right). Sequences sweep across the stereo field.
- Pick one key and keep every tonal sound in it; pitch rises with progress and resolves on the payoff. (In the effort example the pad and slider notes are D major, but the scene 3 pops and chime are still in C major. Don't copy that.)

## Adding a generator

Write a function in `sfx/synth.py` that returns a list of floats at `SR`. Put what it's for in the first docstring line; `--list` shows it. Use the module-level `random` for noise so renders stay reproducible. Build on `bandnoise()` for anything airy.

## Verify

```bash
npm run sfx                              # or python3 -m sfx sfx/cues/<video>.py
npm run wave                             # out/wave.png + loudness of the WAV
npm run build
node scripts/wave.mjs out/effort.mp4     # loudness of what you'll actually post
```

In `out/wave.png` every coral line is a timeline beat. Each transient should sit on a line or a hair after it. A hit between lines means a hardcoded time or a stale WAV. Pass `--timeline` for a video with its own timeline file.

## Optional: generated audio

For voiceover or sounds you can't synthesize, the ElevenLabs MCP (see `.mcp.json.example`) can generate files into `public/`. Place them with `<Audio src={staticFile(...)} />` inside a `<Sequence from={beat * FPS}>`.
