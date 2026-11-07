---
name: edit
description: >
  Edit talking-head and short-form video end to end: cut dead space, ums and retakes, add
  word-timed captions, dynamic visuals and stop motion, then finish the audio at -14 LUFS and
  export for Reels, TikTok and Shorts. Combines the HyperFrames, Remotion and video-use editing
  skills with local ffmpeg tools. Use whenever someone wants to edit, cut, tighten or caption a
  video, or says "cut the dead space", "remove the silences", "cut the ums", "jump cuts", "add
  captions" or "subtitles", "make this a reel", "add b-roll" or "motion graphics", "make a stop
  motion", "fix my audio", or drops raw footage that needs to become postable.
---

# Edit

You are the editor. This skill is an opinionated workflow plus small local tools (Python 3
standard library + ffmpeg). The tools do the measurable work: dead-space cuts, caption files,
stop-motion timing, probing. You do the judgement: what to cut, what to show, when. For motion
graphics you route to HyperFrames (default), Remotion, or video-use.

You cannot watch or listen. Measure, extract stills, read the transcript, and say plainly what
you checked and what you could not.

Tools live in `tools/` next to this file. Below, `T` means that folder:
`python3 "$T/deadspace.py" --help` works for every tool. All tools exit 0 on success, 1 on an
ffmpeg/runtime failure, 2 on bad input, 3 when a program or feature is missing.

| Tool | Does | Writes |
|---|---|---|
| `probe.py` | media facts (rotation, VFR, HDR, audio layout, loudness); `--doctor` checks the machine | stdout / JSON |
| `deadspace.py` | cuts silences, plus fillers and retakes with a transcript; frame-accurate, crossfaded joins | `<name>.cut.mp4`, `.edl.json`, `.words.json` |
| `captions.py` | transcribes (faster-whisper, optional) or reads word timings; 1-3 word phrases | `.srt`, `.ass`, `.cues.json`, `.words.json`, `.phrases.txt` |
| `stopmotion.py` | frames folder or live clip to stop motion: 8/10/12 drawings/s, holds, seeded jitter | `.mp4` |

## 0. Setup check (once per session)

```bash
python3 "$T/probe.py" --doctor
```
It reports: ffmpeg filters (is `ass`/`subtitles` there for burned-in captions?), encoders,
faster-whisper, and Node (HyperFrames needs Node 22+). Do not install anything without asking.
Put every output in `<footage folder>/edit/`, never inside this skill's folder.

## 1. Brief, then a plan the user approves

Infer what you can, ask only what changes the edit: platform (default Reels/TikTok/Shorts,
1080x1920), target length, pace (`tight` for shorts, `normal`, `loose` for talks), caption style,
how much motion. Then state the plan in 3 to 6 lines (what gets cut, caption style, which beats
get visuals, the engine) and wait for an OK before rendering, unless the user said "just do it".

## 2. Probe

```bash
python3 "$T/probe.py" take.mov --loudness
```
Note the display size after rotation, fps and VFR, HDR, channels and loudness. The tools handle
rotation (ffmpeg autorotates), VFR (deadspace renders constant frame rate), mono/stereo (kept as
recorded) and HDR (kept as 10-bit HEVC with its tags). If there is no audio stream, dead-space
cutting is impossible: say so and cut by hand from stills.

## 3. Transcribe once, read the take

```bash
python3 "$T/captions.py" take.mov --words-only --verbatim -o edit/
```
- Writes `edit/take.words.json` (cached: reruns reuse it unless the file changed) and
  `edit/take.phrases.txt`, one timed line per phrase. Read phrases.txt; it is your view of the
  take at a fraction of the tokens.
- `--verbatim` nudges Whisper to keep "um/uh" so they can be cut. Whisper still drops some, so
  never promise every filler is caught.
- `--model small` is the default; use `--model medium` or `large-v3` when words matter (finals,
  accents). `--prompt "Claude, HyperFrames, Remotion"` helps with names and brands.
- No faster-whisper? Exit 3 with install steps. Any word-level JSON works instead via `--words`
  (ElevenLabs Scribe, Whisper, whisper.cpp, Deepgram, AssemblyAI, HyperFrames transcript.json),
  and SRT/VTT works with approximate word times.
- Proofread names and brands in words.json by hand (keep the timings). A wrong word on screen is
  worse than no caption.

## 4. Cut the dead space (dry run, review, render)

```bash
python3 "$T/deadspace.py" take.mov -o edit/take.cut.mp4 --transcript edit/take.words.json --dry-run
# read the printed cuts and edit/take.cut.edl.json, then:
python3 "$T/deadspace.py" take.mov -o edit/take.cut.mp4 --from-edl edit/take.cut.edl.json
```
How it decides:
- A 10 ms envelope with an adaptive gate: the noise floor is the 10th percentile, speech the loud
  frames, and the gate sits 30 dB under speech but never within 8 dB of the floor. It works on
  quiet phone takes and noisy rooms. If speech is under 12 dB above the floor it cuts nothing by
  level and tells you to pass a transcript or `--threshold`.
- Pace presets (pause cut when longer than / air kept before speech / after speech):
  `tight` 0.25 / 0.06 / 0.10 s, `normal` 0.35 / 0.08 / 0.14 s, `loose` 0.60 / 0.12 / 0.22 s.
  A cut pause leaves about 0.2 s of air at normal: tight, never breathless.
- With a transcript: fillers are cut with their gap, and repeated lines are cut so the last take
  wins (`--retakes exact` for stutters and false starts only, `fuzzy` (default) also catches a
  re-said sentence with small changes, `off`). Silence cuts never pass through a transcribed word
  that has real energy.
- Joins: keep ranges snap to the frame grid, audio gets 30 ms equal-power crossfades (no clicks),
  and A/V stays in sync (the summary prints the drift, normally under 1 ms).

Review before rendering. The tool is mechanical: you read phrases.txt and also cut semantic
retakes it missed (a line said twice with different words, a restart after "wait, let me redo
that"). The EDL's `cuts[]` is the source of truth: set `"apply": false` to veto a cut, append
`{"start": s, "end": e, "reason": "manual"}` to add one, then render with `--from-edl`. Keep
the speaker's best delivery, keep laughs and reactions after punchlines.

After rendering, `edit/take.cut.words.json` holds the words on the cut timeline. Use it for
captions and visuals; never re-transcribe the cut.

## 5. Pace and structure

- Hook: the first 1 to 2 s land a concrete payoff (a number, money made or saved, the result).
  Keep the face on screen during the hook (split screen or cutout), no slow push-in.
- Cut, don't hold: in a short, no shot runs past about 1.5 s; aim for a median shot of 1 s or
  less. A beat longer than that gets 2 or 3 genuinely different shots (a reframe of the same
  take counts, two moments of a locked camera do not).
- Plan with a beat table keyed to the words: time, the noun being said, the visual. Measure the
  finished cut: `ffmpeg -i final.mp4 -vf "select='gt(scene,0.25)',showinfo" -f null - 2>&1 | grep -o "pts_time:[0-9.]*"`
  lists cut times; compute the median gap.

## 6. Captions

```bash
python3 "$T/captions.py" edit/take.cut.mp4 --words edit/take.cut.words.json -o edit/
```
- 1 to 3 word phrases. They break after `. ! ?`, after commas once a phrase has 2 words, on
  pauses of 0.3 s or more, and at 18 characters. A phrase never ends on a weak opener ("the",
  "to", "a"), and a phrase too quick to read grows by a word.
- Default look: UPPERCASE bold, white with a black outline, the spoken word in an accent colour
  (`--accent`), fillers hidden. The text bottom sits at y 1440 of 1920 (chest or collar) with
  140 px side margins, so it stays inside the safe zone. `--position seam --y 960` centres the
  captions on a split-screen seam, and `--position top` puts them under the header.
- Never over the face. Extract a still to check:
  `ffmpeg -ss 3 -i edit/take.cut.mp4 -frames:v 1 edit/check.png`. If the chin sits low, move the
  captions with `--y`.
- Burn in: `--burn edit/captioned.mp4` works only when ffmpeg has libass. Without it, the tool
  exits 3 with the routes. HyperFrames route: render the captions in HyperFrames
  (`/embedded-captions`). Copy `take.cut.words.json` into that project as `transcript.json`; it
  uses the same `{text, language_code, words[{text, start, end}]}` shape, so the proofread words
  are reused instead of re-transcribed. For custom kinetic captions in any engine, feed
  `take.cut.cues.json` (phrases, per-word times, size, safe area). On macOS, an ffmpeg with
  libass comes from the homebrew-ffmpeg tap: `brew uninstall ffmpeg`, `brew trust homebrew-ffmpeg/ffmpeg`,
  `brew tap homebrew-ffmpeg/ffmpeg`, `brew install homebrew-ffmpeg/ffmpeg/ffmpeg`.

## 7. Dynamic visuals (route to an engine)

| Situation | Engine | Install (verified from each repo's README) |
|---|---|---|
| Default: overlays, kinetic type, b-roll cards, zooms, captions on footage | HyperFrames (HTML to video, deterministic render) | `claude plugin marketplace add heygen-com/hyperframes` then `claude plugin install hyperframes@hyperframes`, or standalone `npx skills add heygen-com/hyperframes` (agents: `npx hyperframes skills update`). Needs Node.js 22+ and FFmpeg. |
| The user already has a Remotion project or React brand components | Remotion agent skills | `npx skills add remotion-dev/skills` |
| Many takes, transcript-driven selection, a self-checking render loop | video-use | `git clone https://github.com/browser-use/video-use ~/Developer/video-use`, `ln -sfn ~/Developer/video-use ~/.claude/skills/video-use`, then in that folder `uv sync` (or `pip install -e .`). Needs an ElevenLabs API key in `.env` (`cp .env.example .env`). |

In HyperFrames, start at `/hyperframes`. It routes designed overlays on footage to
`/talking-head-recut`, plain captions to `/embedded-captions`, short motion graphics to
`/motion-graphics`, and re-cuts or reframes to `/general-video`. Hand every engine the same data:
the cut video, `*.cut.words.json` (output timeline), `*.cues.json`, the EDL.

House rules for visuals:
- Show the noun on the word: the visual lands on the frame the word is said, and shows the
  literal thing named (sales means a cart and money, a schedule means something landing on a
  calendar). If no honest asset exists, stay on the face and reframe.
- Real UI at real proportions: capture the real page or app and zoom uniformly. Never invent a
  condensed card with inflated type, never slice text with a card edge.
- No scanner effects: no light sweeps, sheens, glows, halos, pulse rings. Crisp motion is a fast
  entrance (4 to 8 frames, strong ease out, 2 to 4 frame stagger), then a clean hold.
- Safe zone on 1080x1920: keep text and key UI inside x 90 to 950, y 240 to 1470. The header
  covers the top, the caption block the bottom, and the button rail covers x > 950 below y 1000.
  Text under about 30 px is texture, not information.
- Every beat gets a different object, not one template repeated. Keep the main element on screen
  from frame 1 of its beat. A face shown between two graphics needs at least 0.8 s.
- Several animations: brief one sub-agent per animation in parallel, each writing its own file.

## 8. Stop motion

```bash
python3 "$T/stopmotion.py" frames/ -o edit/stop.mp4                  # 12 drawings/s on twos, 24 fps
python3 "$T/stopmotion.py" frames/ -o edit/loop.mp4 --fps 8 --hold 3 --pingpong --loop 2
python3 "$T/stopmotion.py" --from-video edit/take.cut.mp4 -o edit/take.stop.mp4 --fps 12
```
- `--fps` sets drawings per second (8 for chunky, 10, 12 for smooth). `--hold` sets frames per
  drawing (2 means "on twos"). Output fps = fps x hold.
- The hand-made feel comes from per-drawing jitter (`--jitter` px, default 0.5% of the short
  side) and rotation (`--rotate` deg, default 0.5). It is seeded: the same `--seed` gives an
  identical render, and each loop pass wobbles differently. `--flicker 0.01` adds exposure drift;
  it is off by default. `--end-hold 1` holds the last pose.
- Mixed sizes and formats are fitted to the canvas (`--size 1080x1920 --fit cover|contain`).
  Transparent PNGs go on `--bg`. From-video mode keeps the original audio in sync.

Making the frames, any style:
- One subject, locked: write a model sheet first (shape, palette as hex, materials, camera
  height and lens, light direction). Every frame prompt or drawing reuses it word for word, and
  only the pose or position changes. Keep the camera locked; movement belongs to the subject.
- With the user's image tool: generate a hero frame, then each next frame from the previous one
  as a reference with one small change (2 to 5% motion). Use 8 to 24 frames for a 1 to 2 s move.
  Styles: clay (fingerprints, soft key light, matte), paper cut-out (flat layers, drop shadows,
  visible paper grain), bricks (studs, plastic sheen, snapped positions), sticky notes (one note
  per frame on a wall, marker text), pixel (fixed grid, limited palette, no anti-aliasing).
- Drawing it yourself: write each frame as SVG with the character as reusable `<g>` groups and
  move only transforms between frames. Add 1 to 2 px random offsets to path points for line
  boil. Rasterize with what exists (`rsvg-convert`, ImageMagick, headless Chrome screenshots) or
  build it as a HyperFrames composition with stepped timing. Then run `stopmotion.py` on the PNGs.

## 9. Audio finishing (one fixed gain, -14 LUFS, limiter)

Rules: never compress, gate or AGC the voice (it lifts room echo between words and chops word
tails). Never use single-pass `loudnorm`, which is dynamic and acts as an AGC. Apply one fixed
gain to -14 LUFS integrated, then a look-ahead limiter at -1.5 dBTP oversampled for true peak.
A music bed sits about 15 dB under the voice at a fixed level.

```bash
# 1) measure (same pre-filter as the master)
ffmpeg -hide_banner -nostats -i edit/final.mp4 -map 0:a:0 -af "highpass=f=75,ebur128=peak=true:framelog=verbose" -f null - 2>&1 | grep -E "^\s+(I|Peak):"
# 2) G = -14 - I   (example: I = -21.3 gives G = 7.3)
ffmpeg -i edit/final.mp4 -map 0:v -map 0:a -c:v copy \
  -af "highpass=f=75,volume=7.3dB,aresample=192000,alimiter=limit=0.841:attack=5:release=50:level=false:latency=true,aresample=48000" \
  -c:a aac -b:a 256k -movflags +faststart edit/final.master.mp4
# 3) measure again: I within 0.5 LU of -14, Peak at or under -1.5 (AAC can add a few tenths)
```
- `level=false` matters: the limiter's default auto-level raises everything. `latency=true`
  removes its 5 ms delay. Older ffmpeg builds lack it: check `probe.py --doctor`.
- Music bed: measure the voice (I_v) and the music (I_m), then gain the music by
  `I_v - 15 - I_m` dB and mix with `amix=inputs=2:duration=first:normalize=0`, then master the
  mix as above. Fade the bed out about 1 s before the end. Use a bed at least as long as the
  video; a looped file with a faded ending dips every loop.
- `-ac 1` sums stereo without scaling (+6 dB). Downmix with `pan=mono|c0=0.5*c0+0.5*c1`.
- If peaks would be limited by more than about 6 dB, say so and offer -16 LUFS instead.
- You cannot hear the result. Report the numbers, and when a change is a judgement by ear, give
  the user a short A/B of the same excerpt.

## 10. Export and self-check before showing anything

Reels / TikTok / Shorts: 1080x1920 (9:16), H.264 High `yuv420p`, 30 fps (or the source rate up
to 60), AAC 48 kHz, `-movflags +faststart`, -14 LUFS, -1.5 dBTP. Platform limits change, so
check length limits when they matter.
- Reframe 16:9 to 9:16 without bars: `-vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"`.
  With bars: `-vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2"`.
- Encode: `-c:v libx264 -crf 18 -preset slow -profile:v high -pix_fmt yuv420p -r 30`.

Before you show the user, check:
1. `probe.py final.mp4`: right size, fps and duration, audio present, video and audio durations
   within a frame.
2. Loudness measured (step 9), numbers reported.
3. Stills at the first frame, each join, and 3 caption moments: nothing over the face, all text
   inside the safe zone, no frozen hold over 1.5 s, and the first frame works as a cover.
4. Captions read the words actually said (spot-check against words.json).
5. Fix and re-check at most 3 times, then hand over with the open issues listed.

## Failure handling

- `probe.py --doctor` says ffmpeg is missing: give the install command and stop.
- No audio: no dead-space cut; offer a manual cut list from stills.
- "Unreliable" gate (noisy room or music under the voice): use `--transcript`, or set
  `--threshold` from the printed levels.
- Too much cut (clipped words): use `--pace loose` or larger `--pad-before/--pad-after`. Too
  little: use `--pace tight`.
- VFR phone footage: fine, it is rendered at constant frame rate. HDR: kept 10-bit; convert to
  SDR once before an engine that renders SDR.
- No libass: use the HyperFrames route (step 6). No faster-whisper: use `--words` or the venv
  install it prints. Node under 22: HyperFrames will not run; use Remotion if installed, or ship
  captions + cuts without overlays and say so.

## Limits (honest)

- The tools never watch or listen. Cuts come from levels and word timings, so review the EDL.
  Retake detection is a heuristic and the last take wins.
- Transcripts are only as good as the model. Whisper drops some fillers and misspells names.
- No generative video or images are made here. Stop-motion frames come from your image tool or
  from SVG you draw.
- Nothing logs into or posts to any account.

Credits and licenses for the merged upstream skills: [CREDITS.md](CREDITS.md).
