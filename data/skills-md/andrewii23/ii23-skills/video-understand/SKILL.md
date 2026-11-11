---
name: video-understand
description: Watch and fully understand any video — local file or URL, a 10-second clip or a full-length film, with or without speech — by indexing every shot (motion, light, sound hits, silences, on-screen text), packing one timestamp-labelled frame per shot into grid images, and pairing them with a timestamped transcript. Use this whenever the user wants a video watched, summarized, explained, spoiled, recapped, searched, or asked about — "what happens in this video", "summarize this clip", "สปอยคลิปนี้", "สปอยหนังเรื่องนี้", "ดูวิดีโอนี้ให้หน่อย", "recap this episode", "what did they say at 3:20", "find the part where X happens", "อธิบายคลิปนี้", "เลือกซีนเด็ดให้หน่อย" — or pastes a video path/URL and asks anything about its contents. Also use for silent videos (sight gags, room tours, b-roll), choosing the best clips from many ("คัดฟุตเทจ", "which clips are usable"), and screening clips for burned-in subtitles ("คลิปไหนไม่มีตัวหนังสือ"). Do NOT use for editing, cutting, rendering, or generating video.
---

# Video Understand

Read a video the way a person does: see every shot, hear the words, notice what
moves and what goes quiet, tie it all to the clock. Three scripts produce that;
you do the understanding.

- `scripts/index.py` — one cheap pass: every shot (with its motion, light and
  sharpest moment), loudness hits, silences, and with `--ocr` the on-screen
  text over time. Text you can read and grep.
- `scripts/frames.py` — one frame per shot (never skips a shot), extra frames
  through long takes, packed into timestamp-labelled grid images.
- `scripts/transcript.py` — a timestamped transcript (ElevenLabs by default).

**The transcript is required whenever there is speech.** A grid shows what is on
screen and never what was said. On a 24-minute episode the grid alone gives the
arc (someone is accused, a gadget appears, a shadow chases them) while every
fact that matters — what was stolen, the gadget's name and rule, how it
resolves — lives entirely in the audio. Skipping the transcript produces
confident, plausible, wrong summaries. Skip it only when the video has no
speech, or the user explicitly asks for visuals only. When there is no speech,
`index.py --ocr` is what carries the words instead: captions, signs, title cards.

## Resolve `SKILL_DIR` first

Every command below runs a script under `SKILL_DIR/scripts/`. Set `SKILL_DIR` to
the absolute path of the directory holding THIS SKILL.md (your harness reported
it when you read this file). Scripts are always a direct sibling of this file.
On Windows substitute `python` for `python3`.

For a URL, download it first (`yt-dlp -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best' -o video.mp4 "<url>"`)
and pass the local file.

## Pick the recipe by the job

| Job | Run |
| --- | --- |
| Short clip (under ~5 min): what happens, explain it | transcript (background) + `index.py --ocr` + `frames.py --index` |
| Film with burned-in subtitles | `index.py --ocr --ocr-lang <lang>` IS the transcript; skip the paid one |
| Silent / no-speech: sight gags, room tours, b-roll | `index.py --ocr` + `frames.py --index`; transcript only if there is speech |
| Long video / film: recap, spoiler, pick scenes | transcript (background) + `index.py` + `frames.py --index`, read every grid; then zoom |
| One moment ("what happens at 1:02:10") | `frames.py --start --end --cells 16` over that window |
| Choosing footage from many clips | `cull.py --text` — one ranked table + one contact sheet |
| Which clips have burned-in text | `text_check.py` |

## Step 1 — index

```bash
python3 "$SKILL_DIR/scripts/index.py" "<video>" --out-dir <work-dir> [--ocr]
```

Prints `INDEX: <path to index.md>`. Read `index.md` WHOLE. One line per shot:
`#n start-end (dur) | motion, light, sound; sound hit 00:12.3`. Bands are
relative to this video ("high motion" = the busiest quarter of its shots). Below
the shots: on-screen text spans (with `--ocr`) and silences.

What the index gives that frames cannot:

- **Where the cuts are.** Rapid short shots = action, argument, a montage; one
  long shot = a walkthrough, a take, a speech.
- **Sound without words.** A `sound hit` is a sudden loudness jump — a slam, a
  laugh, a music sting. In a silent comedy the hits are the punchlines; check
  the frames right before each one.
- **Silence.** A silence after a line is often the joke landing, or a beat
  meant to be felt. Look at the frames inside it.
- **Words on screen** (`--ocr`). Burned-in captions ARE the transcript of a
  muted clip; signs and title cards name places and chapters.

**Name the language of the on-screen text** with `--ocr-lang` (default
`zh,en`): `th` for Thai subtitles, `ja`, `ko`, ... OCR reads only the scripts
it is told to — on a Thai film with burned-in subtitles the default returned
zero Thai lines; `--ocr-lang th` returned the dialogue verbatim. A film with
burned-in subtitles in a language you can read needs no paid transcript at
all: the OCR track is the dialogue.

Measured cost: a 2h05m 720p film indexed in 69s (1,727 shots); with
`--ocr --ocr-lang th` it took 356s and returned 1,278 Thai subtitle lines
spanning 0:06 to 2:04:45. A 2:45 phone clip with `--ocr` took 7s. `--ocr` needs macOS + `swiftc` or `tesseract`.

## Step 2 — frames

```bash
python3 "$SKILL_DIR/scripts/frames.py" "<video>" --out-dir <work-dir> --index <work-dir>/index.json
```

Prints `MANIFEST: <path>`. Passing `--index` reuses the shot list instead of
decoding the video again (without it, frames.py finds the shots itself).

Every shot gets one frame — its sharpest moment — and that frame is never
deduplicated away. Whatever budget is left goes to extra frames spread through
long takes (up to 4/s on clips under a minute, 2/s under five, 1/s beyond). The
default budget rises to the shot count (capped at 2048), so a film with 1,727
shots yields 1,727+ frames. Measured on a 2h05m film: the old fixed 512-frame
budget put a frame in 29% of shots and skipped shots up to 28s long; the shot
engine covers 100% of them, in 27 grids.

Every cell carries its timestamp burned into the top-left corner, so you can
cite a moment straight off the picture. The manifest still holds the exact
`t_ms` and, for shot anchors, the `shot` number from the index.

Pick `--cells` by the QUESTION, not the video length — the real limit is how
many pixels each cell survives at after downscaling:

| `--cells` | px per cell | Use for |
| --- | --- | --- |
| 16 | ~392 | small on-screen text: UI labels, timestamps, subtitles |
| 36 | ~261 | facial expression, fine action, motion beats |
| **64** | ~196 | **plot, scene inventory, recaps, spoilers (default)** |
| 100 | ~157 | rough skim of very long footage; small text is lost |

(px per cell is for landscape video. Portrait phone video gets a grid with more
columns so the whole image stays near-square.)

Text legibility, measured on 720p: big burned-in captions and full-screen title
cards (including dense Japanese) read fine at **196 px/cell**. Player-UI text —
`0:01 / 20:56`, a chapter label — needs **392 px/cell**. So reach for `--cells
16` only for genuinely small text; 64 already handles anything title-sized.

Useful flags: `--start`/`--end` (`SS`, `MM:SS`, `HH:MM:SS`) to focus a section —
always prefer this over a sparse scan when the user asks about one moment;
`--budget N` to cap total frames (thinned evenly, never truncated at the tail);
`--max-grids N`; `--no-labels`; `--force keyframe|uniform` for the old
extractors.

**Zoom, don't re-read.** For a long video: read the index and transcript, read
every grid once, then zoom into the scenes the question hinges on with
`--start`/`--end` and `--cells 16` or `36`. Do not re-extract single frames to
"look closer" — cropping one still costs an image Read for content a zoomed
grid gives you better.

**Cue frames.** After reading the transcript, if the speaker points at something
("look here", "notice this", "ตรงนี้") and the grid's sampling missed that
moment, grab exactly those instants instead of re-scanning a range:

```bash
python3 "$SKILL_DIR/scripts/frames.py" "<video>" --out-dir <work-dir>/cues --at 4:32,7:10 --cells 16
```

One frame per cue, no dedup, same manifest format (`engine: "cues"`).

## Step 3 — transcript

**Start this FIRST, in the background, then do Steps 1–2 while it runs.** The
transcript dominates wall-clock and the steps share nothing, so running them
concurrently makes the whole job cost about as much as the transcript alone.
Launch it with `run_in_background: true`, build the grids, then poll for the
output file every few seconds.

Measured on a 24-minute 720p episode: grids 5s, transcript ~65s. Run in
sequence that is ~70s; overlapped it is ~65s, and the grids are free.

```bash
python3 "$SKILL_DIR/scripts/transcript.py" "<video>" --out <work-dir>/transcript.json --lang th
```

Do not try to speed this up by splitting the audio into chunks and transcribing
them in parallel — measured, that is 2.2x SLOWER (142s vs 65s), because the API
rate-limits per key so concurrent uploads queue against each other. Shrinking the
upload does not help either: a 2.7x smaller Opus file took 3x longer for a
byte-equivalent transcript. One whole-file call is the fast path.

Prints `TRANSCRIPT: <path>`. Sources tried in order (override with `--source`):

1. **elevenlabs** — Scribe v2, word-level timing. Default and best for Thai.
   Needs `ELEVENLABS_API_KEY` (shell env or a `.env` above the working dir).
2. **captions** — native subtitles via yt-dlp. Free and instant, URLs only.
3. **whisper** — local faster-whisper. Free, offline, weaker on Thai.

Omit `--lang` to auto-detect. If every source fails the script exits non-zero —
say so plainly and continue with frames only, rather than inventing dialogue.

## Step 4 — read everything

Read `index.md` whole, then `Read` every `grids[].path` from the manifest **in
one message** (parallel tool calls) so you see them together, then read
`transcript.json`. For a film that is ~27 grids — read them all; that is the
point of one-frame-per-shot. Skim nothing you will be asked about.

**Read the transcript WHOLE, with `Read`.** Do not sample it — no script that
prints "the interesting windows", no grepping a few timestamps, no reading the
first N segments and inferring the rest. Sampling means YOU choose which lines
matter before knowing what the video is about, and that choice is made from the
pictures, which is exactly the guess the transcript exists to prevent. If the
file is large, read it in sequential chunks until you reach the end; a 24-minute
episode is ~170 segments and costs a few thousand tokens — far cheaper than the
grids you already read.

Each grid is cells laid left-to-right, top-to-bottom, in `grids[g].cols` ×
`grids[g].rows` (the last grid may be smaller so it carries no blank cells).
Cell *i* of grid *g* is `grids[g].cells[i]`, carrying `t_ms` and a human
`t_label`.

**Every cell is stamped with its time** (top-left, `MM:SS.d`). Cells are NOT
evenly spaced — one per shot plus fill — so never infer a time from a cell's
position; read the stamp, or the manifest's `t_ms` when you need the exact
millisecond. Align to the transcript and the index by time.

## Step 5 — answer

Combine the streams: frames say what is shown, the transcript says what is said,
the index says where the cuts, the motion, the sound hits and the on-screen
words are. Time ties them together. Cite timestamps.

For **scene selection** (a spoiler cut, a highlight reel, b-roll pulls) answer
with a list the user can cut from: `start–end | what happens | why it matters`,
taking start/end from the index's shot boundaries, not from a single cell.

If the user asked something specific, answer it directly. Otherwise summarize
what happens — structure, key beats, notable visuals, and what is actually said.
Never paste the raw transcript back; synthesize it.

**The failure mode to watch for.** Pictures let you assemble a story that hangs
together and is wrong, and it will not feel like guessing — it feels like
understanding. A real case from this skill's own testing: the grids showed a
gadget, then a boy turning into a black shadow, a fox appearing, a monkey
falling. The obvious read — "a gadget with side effects, haunted by shadow
creatures" — was confident, coherent, and false. One transcript line at 14:00
explained it: the gadget makes *figures of speech literal*. The shadow was "life
is gloomy", the fox was an idiom about confusion, the octopus on the ear was
"ears growing calluses" (bored of hearing it). No amount of visual detail
contains that link; it is language-only.

So: when the frames suggest a causal story, treat it as a hypothesis and go find
the line that confirms it. If no line confirms it, say what you saw and that the
reason is not stated — never ship the plausible version.

Clean up the work dir with `rm -rf` when the user is unlikely to follow up.

## Culling: choosing the best clips from many

```bash
python3 "$SKILL_DIR/scripts/cull.py" <clip> [<clip> ...] --out-dir <work-dir> --text
```

Prints `CULL: <path to cull.md>`: a ranked table (sharpness, jitter, exposure,
burned-in text, length) plus a contact sheet — each clip's sharpest frame,
labelled with its rank. Read the table and the sheet; that is the whole batch in
one image. Sharpness and jitter are ranked WITHIN the batch (absolute values do
not transfer between cameras); treat the score as an ordering, then look.
Measured: 20 b-roll clips (8s–8min) in 48s. Near-black and low-contrast frames
are excluded from sharpness — they have no edges and would otherwise read as
the sharpest footage in the batch.

## Screening footage for burned-in text

When the job is picking reusable footage out of many downloads — b-roll,
reference clips, "the ones without subtitles" — do NOT build grids for every
file. Screen them first:

```bash
python3 "$SKILL_DIR/scripts/text_check.py" <video> [<video> ...] --out <work-dir>/text_check.json
```

It OCRs 6 full-resolution frames per video (macOS Vision, or `tesseract` on
other systems) and marks each `clean` or `TEXT`. Measured on 54 RedNote clips:
~2s per clip, noise on clean footage ≤4 chars, the smallest real overlay 18
chars, so the default `--max-chars 8` sits in that gap. It only checks 6
moments: a subtitle that shows for one second between samples can slip
through, so run `frames.py` on the `clean` survivors and look before
promising "no text anywhere". Exit 2 means no OCR backend — say so.

## What this cannot do

Say so plainly rather than guessing:

- **Continuous motion** — easing, velocity, bounce, overshoot. Grids give
  positions, not the curve between them; a 250 ms ease is one frame at 4 fps.
  Discrete, staged motion (text animating in, items appearing one by one,
  arrows drawing) does read fine.
- **Frame-exact timing.** Timestamps are as precise as the sampled frame, not
  the cut.
- **Anything inaudible and off-screen.** If neither stream carries it, it is not
  in the answer.

## Cost

Measured: 64 frames read individually ≈ 12.5k tokens; the same 64 as one grid
≈ 1.9k — about 7x cheaper. Past a 1568 px long edge every grid costs the same
~1.9k regardless of cell count, so extra cells are free in tokens and paid for
in per-cell resolution. A 2h05m film with 1,727 shots is 27 grids at
`--cells 64` — every shot seen once. If that is more than the question needs,
cap it with `--budget` and zoom instead.

## Requirements

`ffmpeg` + `ffprobe` on PATH. Python 3.9+, stdlib only. `text_check.py`,
`index.py --ocr` and `cull.py --text` also need macOS with `swiftc` (Xcode
command-line tools) or `tesseract`. Optional: `yt-dlp`
(URLs, native captions), `faster-whisper` (offline transcripts),
`ELEVENLABS_API_KEY` (best transcripts, especially Thai).
