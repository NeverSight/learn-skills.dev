---
name: prod-by-claude
description: >
  Use when an agent needs to make a HyperFrames video of a Strudel live-coding track, where the code itself is the
  picture and every token lights up on the note it plays. Trigger on: "strudel video", "live coding video", "show
  my code playing", "make a video of this track with the code", "prod by claude". Covers composing the track,
  recording it offline from pinned Strudel, and building the 1080x1080 video (typed opener, parts powering on,
  real Strudel theme switches, graffiti ASCII drops, typed sign-off).
---

# prod-by-claude

Turn a Strudel track into a live-coding video. The music is rendered offline from the code, and
the video is driven by Strudel's own note events, so every highlight lands on its note.

## When to use

- The user wants a video of Strudel code playing: "make a video of this Strudel track", "show the
  code lighting up", "live-coding video", or a track the agent composed for them.
- Not for other audio or DAW projects, talking-head videos, or visualizers of an existing audio
  file with no Strudel code (use the HyperFrames music workflow for those).

## Inputs

- A Strudel track (`.strudel.js`), or a brief to compose one. Compose with
  [references/composing.md](references/composing.md). With no track, start from
  [assets/example/track.strudel.js](assets/example/track.strudel.js) (synth-only, no samples).
- The arrangement: length in bars, and which bars are builds and drops.

## Tools and dependencies

- Node 22 or newer, npm, and the HyperFrames CLI pinned to `hyperframes@0.8.70` (run through `npx --yes`).
- `tools/package.json` pins everything else: `@strudel/web` 1.3.0 (AGPL-3.0, installed from npm,
  not bundled here), `puppeteer-core` 25.12.0, `@puppeteer/browsers` 3.2.3, and the OFL fonts
  `@fontsource/jetbrains-mono` 5.3.0 and `@fontsource/rubik-mono-one` 5.3.0.
- Chrome for Testing 149.0.7827.22 for recording, or any Chrome given as `CHROME=<path>`.
- No credentials.

## Workflow

1. Create the project (plain file copies):
   `node <skill>/scripts/new-project.mjs <project-dir> [track.strudel.js]`
2. Edit `<project-dir>/video.json`: `bars`, `builds`, `drops`, `themes`, `storm` parts, `signoff`
   ([references/video.md](references/video.md), [references/themes.md](references/themes.md)).
   The template already matches the example track, so skip this step when using it.
3. From `<project-dir>/tools`, install the pinned tools: `npm install`
4. From `<project-dir>/tools`, if `CHROME` is not set, fetch Chrome for Testing:
   `npx --yes @puppeteer/browsers@3.2.3 install chrome@149.0.7827.22 --path .chrome`
5. From `<project-dir>/tools`, record: `node record.mjs ..` It takes about 5-7 minutes for 32
   bars (give it a 10 minute timeout), prints levels per 4 bars and warns on clipping. Fix the
   track and record again until the drops peak at or below -2 dBFS with no clipped samples.
6. From `<project-dir>/tools`, build the video data: `node build-data.mjs ..` It prints the
   snapshot command for step 7.
7. From `<project-dir>`, run `npx --yes hyperframes@0.8.70 check .`, then the printed snapshot
   command, and look at every frame (what to look for: [references/video.md](references/video.md)).
8. From `<project-dir>`, render locally when the user asks for the video:
   `npx --yes hyperframes@0.8.70 render . -o renders/video.mp4`
   HyperFrames cloud render (`npx --yes hyperframes@0.8.70 cloud render .`) spends credits on the
   user's account: use it only after the user explicitly agrees.

If the track changes, repeat steps 5-7. If `video.json` changes, repeat steps 6-7.

## Outputs

- `assets/bgm.wav` (the mix), `assets/stem-<part>.wav` (the scope part), `data/events.json`
  (every note with its code locations), `data/events.js` (what the composition reads).
- `renders/video.mp4`, 1080×1080, 30 fps, about `pre + bars × 240 / bpm + 4.6` seconds with a
  sign-off.

## Side effects

- Files: writes only inside `<project-dir>`. `build-data.mjs` rewrites the `data-duration` and
  audio `data-start` attributes in `index.html`.
- Network: `npm install` (npm registry), the Chrome for Testing download (about 150 MB from
  Google's storage), and GSAP from cdn.jsdelivr.net when the composition loads. `snapshot`
  uploads frames to a hosted captioning model unless given `--describe false`, so always pass it. Recording runs on
  127.0.0.1 only and fetches nothing unless the track itself loads samples (then from the sample
  URLs the track names).
- Audio: recording is headless and muted; nothing plays out loud.
- Cost: none, unless the user approves a cloud render.

## Verify

- `record.mjs` exits 0, lists every part, and reports no clipping.
- `check` passes with 0 errors. `canvas_overflow` info notes for code lines below the frame are
  expected.
- In the snapshots: line 1 typing at 0.6 s, the first part blooming and highlighted after `pre`,
  graffiti in each drop, the decode after each drop, the sign-off at the end.
- In the render: the first sound lands at `pre` seconds, and the video ends in black.

## Rights

The music written in Strudel belongs to its author; Strudel's AGPL covers the software, not the
tracks. Built-in synths need no clearance. Samples loaded by a track are other people's
recordings: use only sounds the user owns or has cleared.
