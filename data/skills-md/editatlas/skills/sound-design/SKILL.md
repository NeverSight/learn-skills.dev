---
name: sound-design
description: Sound-design a finished video with real sound effects from the EditAtlas library (2,278 described sounds, public, downloadable from GitHub with SHA-256 checks). Finds the moments in the picture, lets you look at them as frame sheets, picks sounds by description and measured numbers, places each on its exact frame at a level set by its role, keeps or replaces the film's own music and voice, renders a new MP4 plus a separate SFX WAV, and checks the result in numbers (sync, pace, holes, loudness, mono) before you show it. Use it whenever someone asks to add sound effects, SFX, whooshes, pops, clicks, hits, UI sounds or "sound design" to a video, reel, short, promo, motion graphic, product demo or talking-head edit; says a video "feels silent", "needs sound", "thêm hiệu ứng âm thanh", "lồng SFX", "thêm tiếng động"; or wants EditAtlas sounds placed on a video rather than just found. Not for composing music or generating sound.
license: Apache-2.0. LICENSE.txt has the complete terms
compatibility: Requires Python 3.9+ with numpy and Pillow, FFmpeg with ffprobe, and network access to raw.githubusercontent.com (or a local clone of EditAtlas/sfx). Designed for Claude Code and other agents with a shell.
metadata:
  author: EditAtlas
  version: "0.4.2"
  status: beta
  library: sfx
  mcp-tools: search_sfx get_sfx
---

# Sound design: real sounds on a finished video

This is sound-design 0.4.2.

The aim: the film sounds as if an editor with a good library cut it. Every sound is a real file from EditAtlas,
placed on a frame you have looked at, at a level you can justify in numbers.

Two things are true the whole way through, so plan around them:

- **You cannot hear.** You choose sounds from their descriptions and measured numbers (`sounds.py info`), check
  placement and levels with `check.py`, and hand the person a short list of moments to listen to. Never say a
  sound "sounds good"; say what was measured and what still needs ears.
- **You must not invent.** Work only on the video the person gave you. If there is no video, ask for it. If a
  moment needs a sound the library does not have, leave it quiet and say so in the report.

All scripts are in `scripts/` (Python 3.9+, numpy, Pillow for the frame sheets, FFmpeg with ffprobe in PATH). Run
them with the skill folder's path, from a working folder of your own (`work/`, `result/`); never write into the
person's project or this skill folder.

```
python SKILL/scripts/moments.py FILM.mp4 --out work/moments             # moments.json, sheet.png, overview.png
python SKILL/scripts/moments.py FILM.mp4 --at 10.4 --out work/at        # frames every 0.1 s around one time
python SKILL/scripts/sounds.py search "glass clink" --max-dur 2         # ids from the public index
python SKILL/scripts/sounds.py info sfx-ID sfx-ID                       # download once, SHA-256, measured numbers
python SKILL/scripts/sounds.py sheet sfx-ID sfx-ID --out work/c.png     # waveform + spectrogram of candidates
python SKILL/scripts/mix.py work/cues.json --out result/FILM_sfx.mp4    # MP4 + _track.wav + _resolved.json
python SKILL/scripts/check.py result/FILM_sfx_resolved.json --moments work/moments/moments.json --listen-out result/listen.wav
python SKILL/scripts/beat_grid.py MUSIC.mp3 --fps 30 --out work/beats.json  # tempo, first beat, every beat, bar starts, frames
```

When the film has music with a beat, or you are cutting a new edit to a track, run `beat_grid.py` on the music before
placing anything: put accents and cuts on `beats` (or `beat_frames`), and big moments on `bar_starts`. It prints
`weak` when the music has no steady beat (piano, lullabies, speech); then place by the picture and say so. Bar
starts are a guess from the kick: listen to the first two bars, or ask the person, before cutting a montage on them.
Measured on generated tracks at 92, 120 and 160.25 BPM: tempo within 0.3 %, every beat within 16 ms (half a frame
at 30 fps), bar starts right. On five real music clips nobody checked the tempo by ear.

Sounds come from `https://raw.githubusercontent.com/EditAtlas/sfx/main/` and are cached in
`~/.cache/editatlas-sfx` (`EDITATLAS_SFX_CACHE` moves it). With a local clone of EditAtlas/sfx, pass
`--mirror PATH` (before the subcommand for `sounds.py`) and nothing is downloaded.

## 1. Look at the film and its sound

Run `moments.py`. It reports the existing audio (`has_audio`, LUFS, how much of it is silent) and finds three kinds
of moment from pixel differences: `cut` (scene change), `move` (motion starts or peaks), `land` (motion stops:
something settles). Then **open `overview.png` and `sheet.png` with the Read tool**: the numbers miss soft
animation (a badge scaling up over a still face makes no cut) and over-report camera shake. Where it matters, draw
the frames around a time with `--at T` and find the exact frame where the thing appears, lands or turns.

Decide what the film's own audio is:

| What you hear in the numbers and see | Cue sheet |
|---|---|
| No audio, or `silent_share` near 1 | `"keep_audio": false`: the sounds carry the film; it is brought to about -16 LUFS |
| Music only | `"keep_audio": true`: sounds sit about 3 LU under it; put accents on the beat when you can |
| Someone talking (captions, a face, a lavalier) | `"keep_audio": true, "under_voice": true`: about 8 LU under the voice; fewer, lighter sounds |
| Synthesized beeps already baked into the mix | ask: replacing them needs the stems; layering real sounds on top doubles them |

Ask the person when it is not clear whether to keep the film's audio.

## 2. Write the event list from what you saw

One line per moment that deserves sound: time, what happens, what kind of sound. Think like an editor:

- A thing that **appears** (badge, chip, button, caption card): a short pop, tick or soft ding, `anchor: start`.
- A thing that **moves across** or a transition: a whoosh whose loudest point lands on the arrival, `anchor: peak`.
- A thing that **lands** with weight (logo, product, stamp): a hit or thud on the frame it stops, `anchor: peak`.
- A **real object** on screen (glass, ice, paper, keys, a drink): the matching foley, not a UI sound.
- **Success / error** states: a ding for yes, a short buzzer or alert for no. One family of interface sounds per film.
- Something building up: a riser whose end lands on the payoff, `anchor: end`.

Not every move needs a sound. Pace and taste rules with numbers are in `references/taste.md`; read it before the
first cue sheet of a session.

## 3. Choose sounds: read, measure, compare

1. Search. If the EditAtlas MCP is connected, `search_sfx` ranks better (it also understands Vietnamese); otherwise
   `sounds.py search`. Titles avoid the words of their source files on purpose ("camera shutter" is "Lens Aperture
   Tick"), so search by what the sound is and try synonyms and the category filter.
2. `sounds.py info` on 2–4 candidates. Read: `audible_s` (how long it is really heard; the file can be longer),
   `attack_s` (0.0x = snaps in, 0.3+ = swells), `peak_t_s`, `centroid_hz` (under ~1500 dark, over ~6000 bright),
   `mono_loss_db` (below -6 the channels cancel on a phone; `mix.py` then plays the louder channel).
3. `sounds.py sheet` when two candidates read the same: a sharp vertical line is a click, a smear is a whoosh,
   energy at the bottom is weight.
4. Pick by what moves and what it touches, then by length: a 0.3 s chip pop must not be a 1.8 s cartoon pop. Use
   `max_len` to cut a long file down, with a fade.
5. Repeated moments of one kind (three chips) want different takes of one family (Tiny Plop 05, 06, Empty Plop 06),
   not the same file three times.

The library is thin in some places (measured 2026-11-07): no liquid pour or fizz, no room tone, no stamp, few
water drops and thuds. Pick the nearest honest sound and name the gap in the report rather than forcing a wrong one.

## 4. Write the cue sheet and render

```json
{
  "video": "work/film.mp4",
  "keep_audio": false,
  "under_voice": false,
  "cues": [
    {"t": 0.30, "id": "sfx-988dafbd36", "role": "whoosh", "label": "title lands"},
    {"t": 0.62, "id": "sfx-mi630472",  "role": "foley", "anchor": "start", "max_len": 0.9, "gain_db": -2, "label": "ice into glass"},
    {"t": 8.30, "id": "sfx-fs339114",  "role": "hit", "label": "bottle lands"},
    {"t": 0.00, "id": "sfx-c7d271e90f", "role": "ambience", "bed": true}
  ]
}
```

- `t` is the frame of the moment in seconds. `role` sets the level and the default anchor (`references/taste.md`).
- `anchor`: `start` puts the audible start on `t`, `peak` the loudest point, `end` the audible end.
- Per cue: `gain_db` (relative to the role level), `max_len`, `fade_in`, `fade_out`, `offset_in`, `pan` (-1..1).
- `"bed": true`: one long, steady ambience under the whole film at -54 dBFS (barely heard). Only for films whose
  sound is SFX alone; never under voice or music. It crossfades into itself if the film is longer.

Run `mix.py`. It prints every sound with its landing time and peak level, and notes when a moment was so early
that the sound had to start inside its file.

## 5. Check, fix, check again

Run `check.py` after every render; exit code 1 means it flagged something. It reads the WAV tracks that
`mix.py` wrote next to `_resolved.json`, so keep those files together when you copy results. It finds every sound in the rendered
track by its own waveform, so `sync` is real: anything off by more than one frame is a bug in the sheet. It also
measures gestures per 10 s, the longest hole, heavy hits, repeats, digital silence, master loudness and true
peak, mono fold-down, and how many strong picture moments got a sound.

For each flag either fix it (add a sound to the hole, swap a repeat, move a cue) or decide it is right and say why
in the report ("the 7.8 s hole is a talking stretch, the voice carries it"). Notes about slow attacks are hints:
if the moment is the sound's peak, switch that cue to `anchor: peak`. Two or three rounds are normal.

## 6. Deliver

**First, a version check.** If the EditAtlas MCP is connected, call `get_skill` without a name. If it lists sound-design above 0.4.2, the first line of your reply says a newer version exists and how to update it (in Claude Code: `/plugin`, then Marketplaces, editatlas-skills, Update marketplace; elsewhere `get_skill` with name sound-design gives the step). Without the MCP, skip it.

Give the person:

1. `FILM_sfx.mp4` and `FILM_sfx_track.wav` (sounds alone, full length, to lay under their own edit).
2. A short table: time, moment, sound title and id, why that sound.
3. The numbers from `check.py` (pace, longest hole, LUFS, true peak) and what each remaining flag means.
4. The listen list (`listen.wav` cuts those moments into one file): "listen on headphones and once on a phone".
5. The gaps: moments left quiet and sounds the library lacked.
6. If they may want to move a sound by a few frames or change a level themselves, offer an editable copy once:
   the editable-export skill opens the video and its sounds in the EditAtlas studio, where they fix it and export
   the MP4 again in their browser. Build it only if they want it.

Write the report in the person's language. Do not claim you listened.

**Last, ask once how it went.** If the EditAtlas MCP is connected, ask the person, in one short message in their
language, about each thing from EditAtlas you used, by name: the techniques, sounds, music, stock clips and this
skill. Send each answer with `send_feedback`, about `this_item`; an answer only about the whole video goes once, as
`whole_edit`. Send only what they said, and nothing if they do not answer. Ask once per edit: if you or another
skill already asked, skip it.

## Optional: the real-sfx engine

Clipwing's `real-sfx` skill (MIT scripts, by Alexander Korbanov) does the same job with a heavier engine: typed cue
lists, synth-layer removal, beat grids, a 9-axis critique. It can use the whole EditAtlas library as its main pack.
See `references/real-sfx.md` for the adapter and what was verified.
