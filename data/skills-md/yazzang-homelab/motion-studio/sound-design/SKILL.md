---
name: sound-design
description: "Score a film to its beat grid: measure a track (beats.mjs) or synthesize one (score.mjs), cue SFX from the film, add voice, mix to -14 LUFS / -1 dBTP at exact length. Use for 'add music', 'sync to the beat', 'SFX', 'loudness'."
argument-hint: "[track path | synthesize] [style]"
---

# Sound design (course step 09)

Sound is where a code-drawn clip starts to feel like a film. One timeline drives three lanes: downbeats carry scene
changes, beats carry SFX, and measured onset peaks place the accents exactly. Two paths: if the user supplies a track,
measure it and use it unchanged; if not, synthesize original music on the same grid as the picture.

Work in the film project root. Arguments, shown once:

<request>
$ARGUMENTS
</request>

The mixing details live in
`${CLAUDE_SKILL_DIR}/references/mixing.md` ([references/mixing.md](references/mixing.md)).

## 1. Music: measure or synthesize

| Situation | Command | Result |
|---|---|---|
| user supplied a track | `npm run beats -- audio/track.wav` (any format ffmpeg decodes) | `audio/beats.json` with measured `bpm`, `beats`, `downbeats`, `hits` |
| ambiguous tempo (half or double) | `npm run beats -- audio/track.wav --bpm-hint 120` | tempo search biased to the hint (30 to 300). Without a hint the JS engine searches 70 to 180 BPM, so a 60 BPM track reads as 120; with a hint the window widens (hints of 45, 60, 65, 200 and 250 recover the real tempo) |
| no Python / librosa | `npm run beats -- audio/track.wav --engine js` | built-in JS analysis (spectral flux, autocorrelation, beat tracking). `--engine auto` (the default) falls back to it by itself, also when `MOTION_PYTHON` points at a broken interpreter (it logs `MOTION_PYTHON=... is not usable` and continues); `--engine librosa` stops with that message |
| no track: synthesize | `npm run score -- --style pulse --bpm 120 --dur 12` | `audio/music.wav` + an analytic `audio/beats.json` (source `grid`) |

For a supplied track, set `studio.json` `audio.music` to its path (for example `"audio/track.wav"`) and `bpm` to the
measured value. Then never run plain `npm run score`: it writes to `audio.music` (overwriting the track) and replaces
`beats.json` with a synthetic grid. `npm run build` is safe because it calls `score.mjs --if-missing`, which keeps a
supplied or replaced track (its hash does not match `audio/music.meta.json`).
Confirm the user has the right to use the track (license or ownership) and note it in `docs/production.json` notes.

Score options (`node tools/score.mjs`):

| Flag | Values | Notes |
|---|---|---|
| `--style` | `pulse` (kick 4/4, claps, hats, sub bass, pluck arp) · `piano` (felt piano, sparse percussion) · `minimal` (ticks, clicks, soft kick; UI films) · `cinematic` (taiko-like hits, bowed ostinato, downbeat booms) | no static generic pads in any style |
| `--bpm`, `--dur` | numbers | default from `studio.json` |
| `--key`, `--mode` | `A`, `F#`, `Bb` ... (a trailing `m` means minor), `minor` / `major` | minor i-VI-III-VII, major I-V-vi-IV |
| `--drop BAR` | bar index | default about 40% of the length, riser into it |
| `--loop` | flag | seamless loop: no intro or ending, no drop, tails wrap to the start; default from `studio.json` `loop`. Use a duration that is a whole number of bars, or the tool warns that the seam misses a downbeat |
| `--seed N` | integer | same seed, same bytes |
| `--if-missing` | flag | used by `npm run build`: keep an existing WAV that is a supplied track, or a score whose settings still match `audio/music.meta.json`; regenerate (WAV, `beats.json`, sidecar) a score that `score.mjs` made when `duration`, `bpm`, style, key, mode, seed, loop or drop bar changed, and say what changed (`regenerated` in the JSON) |

Every run also writes `audio/music.meta.json` (the resolved settings plus the sha256 of the WAV): that is how
`--if-missing` tells a score it made from a track you supplied or replaced, which it never touches.

Optional `studio.json` `audio` keys fill the same options when the flag is absent (a flag wins): `style` (the template
ships `"pulse"`), `key`, `mode`, `seed`; `voiceId` is the default ElevenLabs voice for `voice.mjs`. Example:
`"audio": { "style": "cinematic", "key": "D", "mode": "minor", "seed": 7 }`.

The four styles are `pulse`, `piano`, `minimal` and `cinematic`. The arrangement opens with a sparse bar, builds,
drops on a downbeat and lands a final hit on the last downbeat that ends at least 0.5 s before the film ends, then a
decay tail; with `--loop` it is a steady groove that folds back onto itself instead. Length is exactly the film
duration.

`beats.json` notes: results are cached by the audio's sha256 in `audio/.cache/`, so re-runs on the same audio are
instant (`--no-cache` to force). Librosa has a cold start: the first run in a fresh Python environment takes about a
minute (numba compiles), later runs are quick. Do not read that minute as a hang; `--engine js` skips Python.
Downbeats are chosen by scoring the four beat phases on low-band onsets, because "every 4th beat" is one beat off when
a song starts with a pickup. Silence gives an empty beat list with a warning; the page then falls back to the BPM grid.

## 2. Picture on the grid

The film receives the grid as `ctx.grid` (factory) and `c.grid` (scene draw). Measured when `audio/beats.json` exists,
otherwise uniform at `studio.json` `bpm`.

| Call | Returns |
|---|---|
| `grid.beat(n)` | time of beat `n` (fractional `n` allowed: `beat(4.5)` is an eighth note later) |
| `grid.bar(n)` | time of downbeat `n` (bar starts) |
| `grid.index(t)` / `grid.nearest(t)` | beat index at `t` / time of the nearest beat |
| `grid.beatsIn(a, b)` / `grid.barsIn(a, b)` | beat or bar times inside `[a, b)` |
| `grid.isOnBeat(t, tol = 0.02)` | whether `t` is within `tol` seconds of a beat |
| `grid.hits` | measured accent peaks in seconds: frozen, sorted, deduplicated, inside `[0, duration)`; `[]` when the track has none |
| `grid.hitsIn(a, b)` | the hits inside `[a, b)`, the same window as `beatsIn` |

Rules: scene changes and state changes on downbeats (`grid.bar(n)`); UI actions, pops and clicks on beats; big accents
on measured hits when a track is supplied. Derive every time from the grid; never type a time the grid can give you,
or the picture drifts when the track or tempo changes. With a measured track `grid.bar(0)` is the first measured
downbeat, which can sit well after 0 s (a pickup or an intro), so spans written as bars move with it.

Measured hits (onset peaks, `hits` in `audio/beats.json`) reach the film as `grid.hits` and `grid.hitsIn(a, b)`, in the
factory (`ctx.grid`) and in every scene draw (`c.grid`). They are available even when the track has no tracked beats.
Do not fetch `audio/beats.json` yourself; the grid already carries it:

```js
// in the factory's cues: measured accents between seconds 8 and 10
cues: (grid) => [...grid.hitsIn(8, 10).map((t) => ({ t, type: 'snap', gain: 0.5 }))],
```

A synthesized score writes only its main accents to `hits` (for example the drop and the final hit).

## 3. Cues come from the film

Declare cues next to the picture they belong to, in the factory's `cues` (an array or a function of the grid):

```js
export default defineFilm((ctx) => ({
  scenes: [/* ... */],
  cues: (grid) => [
    ...[0, 1, 2, 3, 4].map((n) => ({ t: grid.bar(n), type: 'thump' })),       // scene changes on downbeats
    { t: grid.bar(1), type: 'whoosh', gain: 0.6 },                             // transition into scene 2: the peak lands on the cut
    { t: grid.beat(6), type: 'click', pan: 0.2 },                              // cursor press on a beat
    ...[0, 1, 2, 3, 4, 5, 6, 7].map((i) => ({ t: grid.beat(8) + i * 0.06, type: 'pop', gain: 0.5, pitch: 1 + i * 0.03 })),
    { t: grid.bar(4), type: 'riser' },                                         // a riser STARTS on its cue ...
    { t: grid.bar(5), type: 'hit' },                                           // ... and arrives on the next hit/thump/snap
  ],
}));
```

Cue fields: `t` (seconds), `type`, `gain` (1), `pan` (-1 to 1, 0), `pitch` (playback-rate multiplier, 1). Aliases `sfx`
for `type` and `vol` for `gain` are accepted. Cues at negative or non-finite times are dropped. Types (`SFX_TYPES`):
`click tick pop thump whoosh swoosh riser hit chime type glitch snap`.

Anchor semantics: `t` is the moment the sound lands, not where the sample starts. `node tools/sfx.mjs --list` prints
each voice with its length and anchor.

| Type | What lands on `t` | Use |
|---|---|---|
| `click`, `tick`, `pop`, `thump`, `hit`, `chime`, `type`, `snap` | the transient (the sound starts a few milliseconds earlier) | the visual event: a press, an entrance, a lockup |
| `glitch` | its first fragment: it starts on `t` | a digital break, on the frame it appears |
| `whoosh`, `swoosh` | the pass-by peak (0.31 s and 0.20 s into the sound), so the sweep builds before `t` | put it on the cut or the move it carries |
| `riser` | nothing lands: it starts on `t` and swells into the next `hit`, `thump` or `snap` cue 0.4 to 4 s later, so it arrives on that impact; with no such cue in range it lasts 1.6 s | put it a bar or a beat before the impact, never on it |

A riser on the same time as its `hit` finds no landing cue (it needs one more than 0.35 s later) and runs 1.6 s past the
impact instead of into it. Put the riser cue earlier, at `grid.bar(n - 1)` for a hit on `grid.bar(n)`.

Staggered pops like the tile example above are intentional off-beat cues; the sync metric lists them, which is fine
as long as each one sits on its visual event.

## 4. SFX

```
npm run sfx                         # opens the film headless, reads __studio.cues(), writes audio/cues.json + audio/sfx.wav
node tools/sfx.mjs --dump-cues      # only write audio/cues.json (check times before synthesizing)
node tools/sfx.mjs --cues my.json   # synthesize from a hand-edited cue file instead of the film
```

Every voice is synthesized deterministically (per-cue seed from the cue's type, time and its rank among identical cues, plus
`--seed`, so adding, removing or reordering other cues leaves this cue's sound unchanged), panned with equal power,
summed on a float bus, limited to -1 dBFS, and the file is exactly the film duration (empty cues give silence of that
length; in a loop film a tail that runs past the end folds back to the start). To use recorded samples instead, put `audio/samples/<type>.wav` (also `.flac`, `.mp3`, `.ogg`) in the project: it
replaces the synthesized voice for that type (`--samples none` or `--no-samples` ignores the folder for one run). The loudest peak of the file is its anchor, and a sampled riser is
timed so that this peak lands on the arrival. Samples need a commercial-use license: your own recordings, CC0, or a
license you hold for a published film. Attribution-only licenses (CC BY) need the credit in the post;
NonCommercial and "personal use" packs are out. Record the source and license in `docs/production.json` notes.

Each cue lands its anchor (the transient's peak, not its first sample: attack shapes and limiters move the peak) on its
time plus `audio.sfxLagFrames` frames (new projects: 1; `--lag-frames N` for one run). A hit one frame after the picture
reads as in sync, because light reaches the eye before the brain fuses the sound; at 48 kHz and 60 fps that is exactly
800 samples, so a visual event on frame F sounds at sample (F + 1) × 800. Keep the cue `t` on the picture's frame: the
critique's sync check and the preview strip read the cue, not the lagged sound.

## 5. Voice (optional, ElevenLabs)

1. The key goes in `.env` as `ELEVENLABS_API_KEY=...` (never in a prompt, a file you commit, or a screenshot). Refer
   to it by name: "the ElevenLabs key is ELEVENLABS_API_KEY in .env".
2. Write `audio/voice.json`: `[{ "t": 0.5, "text": "Meet Driftnote." }, { "t": 4.0, "text": "Notes that file themselves." }]`
   (optional per-line `voiceId`). Place lines on downbeats and leave the picture room for them.
3. `node tools/voice.mjs --dry-run` prints the plan and character count (no network, no cost). Show it to the user if
   the budget matters. A line with the same text, voice id and model as an earlier one is synthesized and billed once (the
   dry run marks it `repeat`; `billableChars` counts unique characters only).
4. `node tools/voice.mjs --voice-id <id>` synthesizes (cached per line in `audio/.cache/`), places each line at its
   `t` and writes `audio/voice.wav` at the exact film length.
5. Set `studio.json` `audio.voice` to `"audio/voice.wav"` after `voice.mjs` has written the file (`voice.mjs` prints
   the reminder but does not edit `studio.json`). While `audio.voice` is `null` the mix ignores the voice; with it
   set, `mix.mjs` ducks the music under the voice (`duck: true`). `audio.voiceId` is the default voice for lines
   without their own `voiceId`.

## 6. Mix and verify

```
npm run mix                                   # all formats: out/score.wav + out/<fmt>/final.mp4 + out/final.mp4
node tools/critique.mjs --format 9x16 --video out/9x16/final.mp4    # evidence in out/review/9x16/video/
```

`mix` takes 40 to 80 s: start it in the background and poll the log when the film is long or the machine busy (never wait
in the foreground for more than about 2 minutes).

Before it mixes, `mix.mjs` decodes and measures every stem. A music, voice or sfx stem that is shorter than the film by more
than 0.25 s, empty, or silent (peak below -80 dBFS) stops the mix with `refusing to mix: ... stem problem(s) do not fit the
N s film` and writes nothing: a stale `music.wav` from an earlier duration used to mix in as a silent tail. Regenerate the
stem (`npm run score`, `npm run sfx`, `npm run voice`); for a voice-over or jingle that is meant to be short, pass
`--allow-short-stems` (the missing part is silence). A silent sfx stem only warns, because a film without cues renders
silence; a stem longer than the film warns that its end is cut with no fade. The JSON result carries `stemInfo` (decoded
duration and peak per stem).

Targets: integrated -14 LUFS +-0.5, true peak at or below -1 dBTP, audio length equal to video length (never
`-shortest`). `--lufs` (or `audio.lufs`) must be -70 to -5, `--tp` (or `audio.truePeak`) -20 to 0; below -9 dBTP the
limiter path enforces the ceiling, and a peaky mix that cannot reach the loudness at a low ceiling ends in the
`master misses the target` warning instead of a crash. `mix.mjs` uses two-pass loudnorm and keeps its linear result only when the master lands within half the
tolerance of the target (+-0.25 LU by default); otherwise it falls back to gain plus an oversampled limiter that aims
at +-0.1 LU, then re-measures the muxed AAC. When a number is off, the report table in
[references/mixing.md](references/mixing.md) says what to change.

Sync check: `metrics.md` from `critique.mjs` (in both `out/review/<fmt>/` and `video/`) reports the share of cues within 25 ms of a
beat and lists the others.
Every listed cue must be an intentional hit on a visual event; move the rest onto `grid.beat(n)`.

Silence check: loudness cannot see a soundtrack that drops out for seconds (a stem that ends early still measures -14 LUFS after
the mix). `critique.mjs --video` therefore runs ffmpeg `silencedetect` (-50 dB, 1.0 s) on the mix and lists every silent span as a
P1 `audio-gap` (`silence 3.2 s at 00:08.1`), and `npm run deliver` fails the same span as check `silence`. Not a gap: a silent
intro (a span starting in the first 0.3 s), a fade-out that ends in silence (a span starting in the last 1.0 s) and intervals listed in
`studio.json` `critique.allowSilence: [[from, to], ...]` (seconds, `from < to`, each padded by 0.15 s). Fix the stem that ends early (`npm run score`, `sfx`, `voice`) and mix again.

Claude cannot listen. Before delivery, ask the user to play `out/final.mp4` once and log anything they hear in the next
critique round. For deeper work (stems, sync debugging), delegate to the `sound-designer` subagent.

Next: `/motion-studio:critique-loop` (the sound axis), then `/motion-studio:ship-formats`.
