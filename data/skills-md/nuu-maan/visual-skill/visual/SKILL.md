---
name: visual
description: Make a hand-painted watercolor or stop-motion (clay and papercraft) animated video (MP4) entirely from code, in the style of the "I'm Upping My P(doom)" music video. p5.js + p5.brush frames rendered in headless Chrome, joined with ffmpeg, optional music track and karaoke lyrics. Use when the user says "/visual", "create a visual video", "make an animated video / music video / stop-motion / claymation video / explainer / short film about X", or gives a topic plus scene ideas and wants a rendered video.
argument-hint: <topic> — <description> — <scene ideas> [audio=path] [len=30s] [bpm=N] [out=dir]
---

# /visual: painted animation from a prompt

The video is a program: every frame is a pure function of time `t`, painted by p5.brush in `studio.html`, rendered by
`render.mjs` in headless Chrome, and encoded by ffmpeg. You write the storyboard and the chapter files; the engine in
`engine/` (next to this file) does the rest. `GUIDE.md` (next to this file) is the full painting API and style bar.
Read it before writing any chapter.

## 1. Read the request

From the arguments and conversation, pull out:
- **topic**, **description** (tone, audience, style notes) and **scene info** (any shots the user wants). Missing scenes are yours to invent; that is the point.
- **audio** path (optional), **len** (default 30 s when there is no audio; otherwise the track length from `ffprobe -v error -show_entries format=duration -of csv=p=0 <file>`), **bpm**, **lyrics/narration lines** with times, **out** dir (default `./videos/<slug>`).

Only ask the user if the topic itself is missing. Everything else has a default.

## 2. Set up the project

```bash
cp -r <this skill dir>/engine <out> && cd <out>
rm -rf node_modules out src/ch/c01_demo.js
mkdir -p assets && cp <audio> assets/     # only with audio
npm install
```
Needs Node 18+, ffmpeg and Chrome or Chromium (`render.mjs` finds it on Linux, macOS and Windows; else `--chrome=<path>`).

Tempo: use the user's bpm. With audio and no bpm, try `aubio tempo -i <file>`; if that isn't installed use 120 and say so.
The offset is the first downbeat (`ffmpeg -i <file> -af silencedetect=n=-40dB:d=0.1 -f null -` gives where sound starts).

With `uv` available, one script gets both the beat grid and word-level lyric timing, which is far better than guessing:
```bash
uv run --with librosa --with faster-whisper python - <<'EOF'
import librosa
from faster_whisper import WhisperModel
f = "<file>"
y, sr = librosa.load(f, sr=22050)
tempo, beats = librosa.beat.beat_track(y=y, sr=sr, units='time')
print("bpm", tempo, "first beats", beats[:4])
for s in WhisperModel("small.en", device="cpu", compute_type="int8").transcribe(f, word_timestamps=True)[0]:
    print(' '.join(f'{w.word.strip()}@{w.start:.2f}' for w in s.words))
EOF
```
Use the transcript only for timing; take the lyric text from the user, and split lines at the matching word start times.

## 3. Storyboard

Write `STORYBOARD.md` in the project. Start with the user's brief verbatim, then:
- **The idea** in two or three sentences: a through-line that makes it one film, not a slideshow.
- **Cast** table. Clawd (`clawd()`) and the Researcher (`researcher()`) are ready-made; use them when they fit, otherwise the chapter that introduces a character writes its rig.
- **Chapters** of roughly 8–20 s, one place each, each with a palette. One table per chapter: time, lyric/beat, shot, how it transitions out.
- Rules that made the P(doom) video work: something *happens* in every shot; shots 1.4–4 s; one clear focal action; text-light (pictures and acting, a few big sound effects, no labels); every cut motivated by action (a zoom through an eye, a fall, a chomp to black, a flash); a colour arc across the film; moods morph, never snap; every shot has camera motion; big hits land on beats.

Then fill `song.js`: `dur`, `bpm`, `offset`, `audio` (`'assets/<file>'` or `null`), `wipes` (chapter-break times), `chapters` (file names, in order), `lyrics` (`[[start, end, text], ...]` or `[]`).

### Stop-motion mode

When the user asks for stop motion, claymation or a papercraft look, add a **Stop-motion look** section to the storyboard and use `src/stopmotion.js`:
- Render and encode at **12 fps** (on twos): pass `--fps=12` to `--frames`, `--encode` and `--clip`. Stepped motion is the point; don't smooth it away.
- Characters are clay puppets: `CAST.boy` / `CAST.her` (beanie kid and bob-haired girl), or new rigs in the same style (flat `wash`, highlight blob, thick ink outline). `CAST.photo`, `CAST.herFace` and `CAST.hand` (the animator's hand, for meta shots) are ready too.
- Sets are paper cutouts with drop shadows (`cutout(pts, o)`); rain, stars and snow hang on visible threads; backdrops are painted cards with visible edges in wide shots.
- Every set piece gets per-frame replacement jitter from `nudge(id)`. The rigs apply it to themselves; pass `still: true` to turn it off.
- A strong bookend is to reveal the tabletop set, lamp and animator's hand at the end.

Write the rig list, the stop-motion rules and `--fps=12` into every chapter agent's prompt.

## 4. Paint the chapters

One file per chapter in `src/ch/`, in the IIFE shape `GUIDE.md` shows, calling `chapter(name, start, end, shots)`.

- **Up to 2 chapters:** paint them yourself.
- **More:** spawn one subagent per chapter in parallel. Each prompt: the project path, "read GUIDE.md (at `<this skill dir>/GUIDE.md`) and STORYBOARD.md", which chapter and time range it owns, that it may only edit its own file, and that it must iterate with contact sheets until every shot reads well, then report its file and the ms/frame numbers.

Non-negotiable in every chapter: no `Math.random()` and no state carried between frames (use `hash(i)` and `jit(a)`), every shot paints the whole frame, and stay under about 2.5 s per frame.

## 5. Check it yourself

```bash
node render.mjs --sheet=<t1>,<t2>,... --cols=4 --w=480 --out=out/check/all.jpg
```
Look at the sheet with Read. Cover the first and last frame of every shot, the chapter boundaries and the wipes. Fix what is weak (clutter, low contrast, stiff poses, tiny characters, anything under the karaoke band) and repeat. The bar: render it, look at it, fix the three weakest things, look again.

Optionally cut a short preview with sound: `node render.mjs --clip=<a>:<b> --out=out/preview.mp4`.

## 6. Render

Estimate the time first: `dur × fps × avg ms/frame ÷ workers` (fps is 24, or 12 in stop-motion mode). If it is over about 15 minutes, tell the user the estimate and ask before starting.

```bash
node render.mjs --frames --workers=4     # out/frames, resumable: rerun to continue; add --fps=12 for stop motion
node render.mjs --encode --out=out/video.mp4   # same --fps as the frames
```
Run the frame render in the background for long videos. Finish by giving the MP4 path, its length, and how to re-render one part (`--frames=<a>:<b>` after deleting those frames).
