---
name: plinkfx
description: Design, render and measure game sound effects as code with plinkfx. Use when the user wants a sound effect for a game or UI ("a heavy door for a dungeon", "a softer coin", "a laser that sounds like 1985"), wants to tweak an existing plinkfx sound, or needs WAV/OGG files of game sounds. Produces a plinkfx parameter object plus a WAV, checked against loudness and peak limits. Runs locally through the plinkfx CLI; no network, no AI audio models.
---

# plinkfx: sound effects as code

plinkfx sounds are small JSON objects (layers of oscillators or noise with envelopes, pitch sweeps,
filters and a few effects) that a 3.1 kB player renders in the browser, and the `plinkfx` CLI renders
to WAV. You design a sound by writing that object, rendering it, measuring it, and adjusting.

**You cannot hear.** Say so once. Your checks are numbers and spectrograms; the user's ears decide.
Always hand the user the WAV and ask them to listen before calling a sound done.

## 0. Setup (once)

```bash
npx plinkfx --version          # or: npm i -D plinkfx
```

Everything below uses `npx plinkfx`. Inside the plinkfx repo itself use `node dist/cli.js`.

If the plinkfx MCP server is connected (`claude mcp add plinkfx -- npx -y plinkfx mcp`), its tools do the
same work without a shell: `list_sounds`, `show_sound`, `render_sound` (with `png: true` you get the
picture back), `measure_sound` and `check_sound`. They take a catalogue name or the recipe object itself.

## 1. Start from the catalogue

274 sounds in 21 categories already exist and are tuned (four of them seamless loops). Reuse before you invent.

```bash
npx plinkfx list               # all sounds: name, category, description
npx plinkfx list mechanic      # one category: ui pickup jump hit explosion powerup shoot footstep magic alert jingle mechanic world creature nature card vehicle horror farm scifi puzzle
npx plinkfx show door-heavy    # the parameter object
```

If a sound is close, copy its object and change it. Pick the nearest sound as your **reference** for step 3.

## 2. Write the sound

Save it as `sounds/<name>.json` in the user's project (create the folder). Read
[reference.md](reference.md) for every field, the defaults and recipes per category. The essentials:

```json
{
  "verb": [0.6, 0.3],
  "layers": [
    { "wave": "saw", "freq": 30, "to": 45, "vib": [2.5, 3], "bp": 700, "q": 6, "a": 0.1, "h": 0.5, "d": 0.2 },
    { "wave": "brown", "lp": 300, "at": 0.8, "a": 0.001, "d": 0.6, "shape": 2.5, "gain": 1.6, "drive": 1 },
    { "wave": "sine", "freq": 70, "to": 32, "at": 0.8, "a": 0.001, "d": 0.5, "drive": 1.5 }
  ]
}
```

Think in layers, like a sound designer: **transient** (1-30 ms click or noise burst) + **body** (the
pitched or filtered part that says what it is) + **tail** (decay, reverb, echo). Cheap-sounding
sounds are usually one layer with a linear decay.

## 3. Render, measure, compare

```bash
npx plinkfx level sounds/door.json --like door-heavy   # sets "gain": reference loudness, true peak <= -1 dBTP
npx plinkfx measure sounds/door.json --like door-heavy
npx plinkfx check sounds/door.json --cat mechanic        # clicks, cut tail, DC, clipping, padding, loudness
npx plinkfx render sounds/door.json -o door.wav --png door.png
```

`measure` prints duration, loudness (max momentary LUFS), integrated LUFS, peak, true peak, spectral
centroid (brightness) and DC, next to the reference. Before rendering, write down the target in one
line, for example: *"0.9-1.3 s, dark (centroid under 900 Hz), thud at the end, loudness near the
reference"*. Then compare:

| Measured vs. target | Change |
|---|---|
| too long / short | `d`, `h`, `at` of the layers; tail comes from `verb` size and `echo` feedback |
| too bright | lower `lp`/`lpTo`, fewer square/saw/noise layers, less `drive` |
| too dull | raise `lp`, add a `noise` layer with `hp` 3000+, or a square/saw layer |
| no punch | add a 5-30 ms transient layer (`noise` + `hp`, `a: 0.001`), add a sine thump (`freq` 60-150 `to` 35-50) |
| true peak above -1 dBTP, or loudness off | run `npx plinkfx level` again after every change |
| sounds static when repeated | raise `vary` (semitones between takes, default 0.4) |

`check` must print no `fail` lines (it exits 1 if it does). Fix every failure before you deliver. The
hint after each one says what to change. Warnings are for judgement: a 30 ms lead-in on a slow door is fine.

Look at `door.png`: waveform on top (full height = 0 dBFS), log spectrogram below with lines at 100 Hz,
1 kHz and 10 kHz. A click shows as a bright vertical line at the very start. Aliasing shows as mirrored
diagonal lines. A tail that stops dead ends in a straight vertical edge instead of fading. See
[reference.md](reference.md#reading-the-picture) for more.

Iterate at most 5 rounds. Keep a short log of what you changed and why.

## 4. Deliver

Give the user:

1. the file `sounds/<name>.json`,
2. `<name>.wav` (plus `--variant 1..3` takes if they want variety),
3. the last `measure` and `check` output,
4. how to play it:

```js
import { play } from "plinkfx/core";
import door from "./sounds/door.json" with { type: "json" };
play(door);
```

`play()` skips a repeat of the same sound within 30 ms (`cooldown`) and keeps at most 4 copies playing
(`voices`); both are options. It returns a voice (`stop(fade)`, `rate(r)`) or `undefined` when skipped.

5. one sentence: "I can't hear it: please listen and tell me what to change (darker, shorter, more punch...)."

For files for an engine: `npx plinkfx export assets/sfx --format both` writes every catalogue sound as
48 kHz mono WAV and OGG. In Godot, keep the import's Normalize off; in Unity, use Decompress On Load
for short sounds and leave Force To Mono off (the files are mono already; it can re-normalise them).

## Don'ts

- Don't copy presets or samples from other tools or packs unless their licence allows it.
- Don't claim a sound "sounds great". Report the numbers and let the user listen.
- Don't exceed -1 dBTP or ship one-shots longer than about 4 s. Ambience and engines are loops: see
  "Loops" in reference.md.
- Don't deliver a sound that `plinkfx check` fails.
