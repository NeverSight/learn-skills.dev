---
name: scenario-kinetic-film
description: "Use when making a launch film, game teaser, trailer, product promo or brand film from a brief in kinetic typography: huge type on every beat, whip pans, 3D letters, key art cut in, beat sync to generated music and sound effects, a 1080p or 4K render with motion blur. Not for a song the user already has (scenario-kinetic-music-video)."
license: MIT
---

# Kinetic Launch Film

## Overview

A film here is a spec: scene blocks placed on the beat grid of its music, plus a palette, a caption
track and a logo. The engine turns it into one web page where every frame is a pure function of
time, so a renderer can seek anywhere and average sub-frames into real motion blur. Nothing in the
motion is generated: every word is the word you wrote, and one palette change rebrands the whole
film.

- **Code** makes all the motion, from 14 blocks: kinetic type, a 3D title, key-art cut-ins, an end
  card.
- **Scenario** makes what code cannot: a music bed at the exact tempo the grid needs, a kit of
  one-shot sound effects, and any key art, product shot or character the Picture block cuts in.
- **finish.py** passes a film only with 40% still frames or less, no still stretch over 0.6 s, and a
  median motion of 2.5 px/frame or more before the end card. A film that parks fails.

Needs: Node 20+, ffmpeg and ffprobe, uv (or Python 3.12+), Google Chrome or Playwright's Chromium.
[new_film.sh](scripts/new_film.sh) puts the locked Playwright
([package.json](assets/npm/package.json), [package-lock.json](assets/npm/package-lock.json)), the
pinned Python packages ([requirements.txt](assets/requirements.txt)) and the fonts
([get_fonts.sh](scripts/get_fonts.sh)) in the film folder.

Connection and the generation loop (`recommend`, `model_schema_get`, `dry_run`, `jobs_wait`): the
`scenario` skill. A song the user brings, with lyrics on its sung onsets:
`scenario-kinetic-music-video`. If a sibling skill named here is missing from your available skills,
load it with `skill_get` (Scenario MCP) or ask the user to install it
(https://github.com/scenario-labs/skills#install); unattended, proceed from tool schemas and flag
the gap.

## Quick reference

`$K` is this skill's folder. Run everything from the film folder.

```bash
bash $K/scripts/new_film.sh my-film --example starter   # or kaiju-postal, tour; --force finishes or refreshes a folder
cd my-film && python3 -m http.server 5671                # preview: space plays, arrows step one beat
node $K/scripts/snap.mjs stills 0.5 b4 b12 b20           # half-size stills at beats (or seconds), from a second shell
.venv/bin/python $K/scripts/beat_grid.py audio/music.mp3 --bpm 172 --window 40
.venv/bin/python $K/scripts/mix.py .                     # out/mix.wav from the film's own cue list
.venv/bin/python $K/scripts/render.py . --res 1080       # out/video_1080.mp4, workers sized to memory
.venv/bin/python $K/scripts/finish.py . --video out/video_1080.mp4 --audio out/mix.wav
```

Then render and finish again at `--res 4k` with `--video out/video_4k.mp4`. Outputs are replaced, so
the check run and the master share `out/final`.

Rules:

- Everything is in beats: blocks, shots, captions, cues. `B(k)` is k beats in seconds.
- One idea per beat or half beat: one or two words, filling the frame width.
- No still stretch over 0.6 s before the end card.
- Transitions are moves (`whipIn`/`whipOut`, a zoom through a letter, a collapse to a point), never
  fades.
- Flip the ground (`bg`, `accent`, `paper`) on phrase changes. Palette colors are 6-digit hex or
  `rgb()`.
- A pure function of `t`: no `Math.random`, `Date` or state kept between frames, since motion blur
  renders sub-frames out of order.
- On-screen numbers come from the film (`{lines}`, `{frames}`, `{seconds}`, the HUD's frame count
  and timecode) or the user, never invented.
- 4K masters stay at H.264 Level 5.2 or lower and under 1 GB.

| Asset                | Capability           | Inputs to look for in `model_schema_get` |
| -------------------- | -------------------- | ---------------------------------------- |
| Music bed            | `txt2audio`          | tempo, instrumental switch, duration     |
| Sound kit            | `txt2audio`          | duration, negative prompt                |
| Key art and products | `txt2img`, `img2img` | reference images, 16:9, 2K or more       |

The steps, each with its reference:

1. Scaffold the film folder with `new_film.sh` (the first command above). Every later step runs in
   it, and the downloads go in its `audio/` and `art/`.
2. Brief to beat sheet: [method.md](references/method.md).
3. Music, sound kit and pictures on Scenario: [sound.md](references/sound.md).
4. spec.js: [blocks.md](references/blocks.md), with the motion rules in
   [craft.md](references/craft.md).
5. Preview and stills: scrub, snap the beats, fix, repeat.
6. A 1080p check render until `finish.py` prints `ALL CHECKS PASS`, then the 4K master:
   [render.md](references/render.md).

## Worked example: a 24-second game teaser

Kaiju Postal ([spec.js](assets/examples/kaiju-postal/spec.js)) is a teaser for a fictional game
about a courier delivering mail in a city of giant monsters. Kinetic type runs on a 172 BPM drum and
bass track, two key arts cut in on the drop, a door-knock gag rides the beat cuts, and the title
lands on the last hit.

1. **Scope and folder.** The `scenario` skill connects and picks the team and project.
   `new_film.sh kaiju-postal` scaffolds the film folder from the starter; every later command runs
   in it.
2. **Beat sheet (free).** 68 beats at 172 BPM (23.7 s):
   - 0-8 type: a charge, then THE CITY / HAS NEW / VERY BIG NEIGHBORS. / THEY STOMP.;
   - 8-16 key art 1 on the drop; 16-24 type ending in a zoom through the D of DELIVER.;
   - 24-32 key art 2; 32-43 a fly-through (DODGE THE BIG FEET.); 43-51 the 3D title YOU ARE THE
     POST.;
   - 51-57 the knock gag; 57-68 the title card.
3. **Music at an exact tempo.** `recommend`:

   ```json
   { "capability": "txt2audio", "prompt": "Instrumental drum and bass for a playful video game trailer at a fixed 172 BPM, a tense intro, then a huge drop, punchy kick on every downbeat, no vocals", "duration": 40, "limit": 4 }
   ```

   Pick a model whose schema has a tempo input and an instrumental switch, read the input names off
   `model_schema_get`, and price two takes:

   ```json
   { "model_id": "<id from recommend>", "dry_run": true, "parameters": { "prompt": "<the prompt pattern in sound.md>", "instrumental": true, "duration": 40, "bpm": 172, "numOutputs": 2 } }
   ```

   After the user's go (unattended, every step: run only inside a budget the task states, else
   report the prices and stop): run, `jobs_wait`, `asset_download`, `curl -L -o`.
   `beat_grid.py --bpm 172` on each take; keep the clearest grid and the strongest drop. Take B held
   172.0 BPM with a drop at 10.74 s, so the film starts 8 beats earlier
   (`music: { offset: 7.95, stopBeat: 58 }`): the drop lands on the first key art and the music
   stops dead on the title.

4. **The sound kit.** The 12 core sounds of sound.md (14 runs with the `_1`/`_2` variants), plus the
   film's own jokes (`stomp`, `roar`, `bell`, `knock`): a dry run each and one total. After the
   user's go: one run each, `"wait": false`, one `jobs_wait`.
5. **Key art.** Two pictures, each priced before the user's go, the second only once the first
   exists: it passes the first's asset id as a reference so the courier and the city match. The
   scooter came back with a maker's logo, painted out before use.
6. **spec.js**, an excerpt:

   ```js
   bpm: 172, beats: 68,
   palette: { bg: '#0B1020', paper: '#F3EEE3', accent: '#FFC21A', hot: '#FF8A1F', ink: '#14120E' },
   music: { file: 'audio/music.mp3', offset: 7.95, stopBeat: 58, gain: -7 },
   sounds: { stomp: -1, roar: -5, bell: -7, knock: -1, hit: 1 },
   cues: [[5.5, 'stomp'], [8.25, 'roar', .9], [24.6, 'bell']],
   scenes: [
     [Words, 0, 8, { charge: true, shots: [
       { at: 1, style: 'punch3d', text: 'THE CITY', fx: 'punch' },
       { at: 2, style: 'slam', text: 'HAS NEW', ground: 'accent' },
       { at: 3, style: 'stack', text: ['VERY BIG', 'NEIGHBORS.'], ground: 'paper', in: 'whipX', fx: 'none' },
       { at: 5, style: 'split', text: ['THEY', 'STOMP.'], in: 'whipY', fx: 'punch', big: true } ] }],
     [Picture, 8, 16, { src: 'art/key1.png', weather: 'rain', words: [[1, 'MONSTERS'], [3, 'NEXT DOOR.', 'accent']], cutIns: [[5, 1.65, [.62, .2], 'stomp']] }],
     ...
   ```

7. **Mix and check render.** `mix.py` lists any hit quieter than the music: raise it in
   `spec.sounds`. The first `finish.py` failed on two pictures that held 1.5 s and 1.2 s; the
   Picture block now pushes, pans, punches in and cuts in on the beat. Its `rain` carries each
   picture between words; under `snow`, `dust` or no weather, give every beat a word or a cut-in.
   The teaser passed with 24% still frames, no hold over 0.6 s and 12.5 cuts per 10 s.
8. **Master.** `render.py . --res 4k` and `finish.py`: a 4K master under 1 GB, a 1080p version and a
   9:16 version (the film centered on black), each checked.

## Common mistakes

- **Parking between hits.** A film can land every cut on the beat and still read as slides: a word
  or a picture that sits still for a beat is a hold. Keep something moving every frame.
- **Picture prompts that backfire.** "A calm darker band for the title" came back as a gray band:
  describe the composition and darken with `tint`. "No watermark" beside a reference image was
  blocked: say "no text, no logos". Vehicles and clothes come back with makers' logos: inspect at
  100%.
- **Trusting a generated track's tempo.** Fit the stretch the film uses (`--window`) and give the
  intended tempo (`--bpm`): without it a 172 BPM track reads as 86.
- **Measuring in custom code.** Measure once, while visible (a hidden element measures 0), and use
  `relPos`, not `offsetLeft`, inside a transformed parent.
- **A nested film sharing state.** The Rewind block builds a second film from the same spec: never
  store per-film state on shared objects.
- **Editing the engine in the film folder.** `new_film.sh --force` replaces it. Custom blocks go in
  spec.js or a `custom.js` it imports.
- **Changing render.mjs, browser.mjs or post.py without render.md.** Its trap list is why they look
  the way they do.
- **More 4K workers than `render.py` plans.** Six filled 36 GB and stalled the machine.

## Files

- Scripts: [new_film.sh](scripts/new_film.sh), [get_fonts.sh](scripts/get_fonts.sh),
  [beat_grid.py](scripts/beat_grid.py), [mix.py](scripts/mix.py), [render.py](scripts/render.py),
  [post.py](scripts/post.py), [render.mjs](scripts/render.mjs), [browser.mjs](scripts/browser.mjs),
  [info.mjs](scripts/info.mjs), [snap.mjs](scripts/snap.mjs),
  [filmserver.py](scripts/filmserver.py), [finish.py](scripts/finish.py), [dyn.py](scripts/dyn.py),
  [holds.py](scripts/holds.py), [audit.py](scripts/audit.py), [montage.py](scripts/montage.py),
  [rectify.py](scripts/rectify.py).
- Engine, copied into each film: [index.html](assets/engine/index.html),
  [main.js](assets/engine/main.js), [core.js](assets/engine/core.js),
  [compositor.js](assets/engine/compositor.js), [blocks.js](assets/engine/blocks.js),
  [sanitize.js](assets/engine/sanitize.js), [validate.js](assets/engine/validate.js).
- Examples: [starter](assets/examples/starter/spec.js) (13 s, a shape to fill that passes the
  gates), [kaiju-postal](assets/examples/kaiju-postal/spec.js) (24 s),
  [tour](assets/examples/tour/spec.js) (52 s, 13 blocks) with its placeholder
  [logo.svg](assets/examples/tour/logo.svg).
