---
name: vox
description: Turns one photo into a cinematic paper-collage animation in the style of Vox explainer documentaries (halftone cut-outs with a white scissor border, torn paper, aged paper grain, stop-motion moves, slow camera push-in). Codex generates the paper layers with the user's ChatGPT plan, the real photo is cut out and printed as halftone by code, an HTML page animates everything and is captured to an MP4 (1080x1920 by default). Use when the user says vox, Vox style, "anime cette photo", "animate this photo", paper collage animation, documentary collage, or sends a photo and an animation idea; also to change an animation already made ("do it with Napoleon", "add a train", "make it night").
argument-hint: "<photo> <animation idea> [9:16|16:9|1:1] [<seconds>s]"
allowed-tools: Bash(codex --version) Bash(codex login status) Bash(ffmpeg *) Bash(ffprobe *) Bash(node *) Bash(ls *) Bash(cp *) Bash(mkdir *)
---

# Vox

One photo and one idea in, a 6 to 15 second paper-collage animation out, in the look of Vox explainer documentaries. Then every change is one more prompt: another person, another place, another object, the same animation.

Talk to them in their language. `<dir>` = `video-agent/vox/<slug>/` in their project (slug: 2 to 4 words of the idea, kebab-case).

```text
video-agent/vox/<slug>/
├── photo.jpg        their photo, untouched
├── layers/          every layer of the collage (PNG with alpha, plates in JPG/PNG)
├── raw/             Codex renders before the chroma cut, and the job logs
├── shots.json       the layers asked to Codex (name, kind, ar, subject)
├── animation.html   the animation: window.setT(t), opens in any browser and plays
├── capture.mjs      frames -> MP4
└── <slug>.mp4
```

## 1. Tools (once)

```bash
codex --version && codex login status
ffmpeg -version | head -1
node --version
```

- Codex missing: `npm i -g @openai/codex` (Node 20+) or `brew install codex`. Not logged in: they run `codex login` themselves ("Sign in with ChatGPT"). Never ask for a key or a password in the chat.
- ffmpeg missing: `brew install ffmpeg` (macOS), `sudo apt install ffmpeg` (Linux), `winget install ffmpeg` (Windows).
- Then in `<dir>`: `npm init -y >/dev/null && npm i puppeteer@24` (headless Chrome for the capture, downloaded once).

## 2. The plan (one message, then their yes)

From the photo and the idea, plan the collage like a page of a magazine, then the moves:

- **The hero**: their photo, always the REAL photo (never redrawn by an AI: faces drift). Cut out (step 3) and printed as halftone by code in the page.
- **A background plate**: one full-frame 9:16 paper scene that sets the place and the time (a sky, a city, a map, a desk, a sheet of aged paper).
- **3 to 6 cut-outs**: the objects of the story (a monument, newspapers, banknotes, a car, a building, clouds, birds). Each one is a separate layer so it can move on its own.
- **The moves** (6 to 15 s): the camera pushes in slowly the whole time, layers enter one by one every 0.5 to 1.5 s (slide in, rise from below, drop from above, a torn-paper wipe), something keeps living (clouds drifting, a bird flapping with two cut-outs, notes falling), one title on a torn paper strip if the idea has one (a place and a year, a name). All on a 12 fps stop-motion clock.

Show the layers as a numbered list (name, plate or cut-out, what it shows) and the beat timeline in 4 to 6 lines. Wait for a yes: each layer is one Codex image on their plan.

## 3. Their photo: cut out, never redrawn

```bash
cp "<their photo>" <dir>/photo.jpg
uvx --from "rembg[cpu,cli]" rembg i <dir>/photo.jpg <dir>/layers/hero.png
```

`uvx` comes with uv (`curl -LsSf https://astral.sh/uv/install.sh | sh`, or `pip install uv`). The first run downloads the model (about a minute). Look at the PNG: a clean silhouette, no chunk of background left. Then:

- **Cut-out bad or no uv**: keep the photo as a rectangular print instead, it is very Vox too: `layers/hero.jpg` placed as a print with a white border and torn edges (see `references/animation.md`, "The photo as a print").
- **A person who never had a photo** (Napoleon, a painting): an engraving or painting from the public domain (Wikimedia Commons), cut out the same way.
- Only photos of people who agreed, or public-domain images. Say it once if they send someone else's photo.

The halftone, the white scissor border and the shadow are added by the page (`references/animation.md`), so the real photo stays the real photo.

## 4. The layers with Codex

Write `<dir>/shots.json` and build every prompt with `references/look.md`: the subject, plus the green-screen sentence for a cut-out, plus the style sentence. Never the word "Vox" in a prompt, never a logo, a wordmark or any readable text in an image (newspapers and notes get illegible type texture only).

Run the jobs with the command of `references/look.md`, 3 at a time in the background, always ending with `< /dev/null`. A job takes 1 to 3 minutes. Then for each cut-out, the chroma cut:

```bash
ffmpeg -v error -y -i <dir>/raw/<name>.png -vf "colorkey=0x00FF00:0.30:0.10,despill=type=green:mix=0.6:expand=0,format=rgba" <dir>/layers/<name>.png
```

Check each layer by eye: put it on red to see any green fringe (`ffmpeg -v error -y -f lavfi -i color=red:s=1024x1536 -i <layer> -filter_complex "[1:v]scale=1024:-1[a];[0:v][a]overlay=0:0" -frames:v 1 <dir>/raw/check-<name>.png`), and no text or letters in it. A bad one: fix the subject and run that one again.

## 5. The animation page

Write `<dir>/animation.html` from the template of `references/animation.md` (the whole page is there, tested) and adapt it to the plan: the layers, their sizes and places, the timeline in `setT`. The rules that make it look like a Vox documentary are in the same file. Keep `setT(t)` a pure function of `t`: the capture calls it frame by frame.

Open it in their browser to preview (it plays on its own): `open <dir>/animation.html` (macOS), `xdg-open` (Linux), `start` (Windows). Fix what looks wrong before the capture.

## 6. The MP4

Write `<dir>/capture.mjs` from `references/animation.md`, then:

```bash
cd <dir> && node capture.mjs animation.html <slug>.mp4
```

About 4 s of work per second of video. Look at 3 frames (start, middle, end) before showing it: `ffmpeg -v error -y -ss <t> -i <slug>.mp4 -frames:v 1 -vf scale=540:-1 raw/frame-<t>.jpg`. Hand over the MP4 path. Music or a voice go on top in their editor, or with `/short-editing`.

## 7. Change it with one more prompt

Same `<dir>`, same page, only what changes:

- **Another person** ("do it with Napoleon"): a new hero (step 3), same layers, same timeline: the page swaps `layers/hero.png` and is captured again.
- **Another object or place**: one new Codex layer (step 4), placed in the page, the rest stays.
- **Another move or timing**: only `setT`. Another format: see "Formats" in `references/animation.md`.

Never regenerate layers that did not change.

## Honest limits

- Codex's image tool decides the details: a layer can come with letters on it or a green fringe. Always look.
- The cut-out of a busy photo can miss hair or fingers: the print version is the safe fallback.
- Each layer counts against their ChatGPT plan's Codex limits.
- The look is inspired by Vox's documentaries: never their name, logo or wordmark on screen.
