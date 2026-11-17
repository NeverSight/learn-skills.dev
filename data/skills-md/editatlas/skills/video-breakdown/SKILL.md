---
name: video-breakdown
description: Break down a reference video shot by shot and name what it does, so the person can make one like it. Measures cuts and transitions (dissolve, dip, wipe, shape, iris, push, zoom, flash), camera moves (crash zoom, push in, shake, speed change), text and graphics and their timing (in, hold, out, stagger), text colours, gradients, backgrounds, font size and free lookalike fonts, the look, pacing, the beat and sound hits; you look at the frames, look up each element in EditAtlas and write a report with technique names, sounds and a recipe. Use it when someone shares a video they like and asks what effect, transition or edit is in it, how it was made, or how to remake it; says "video này dùng hiệu ứng gì", "phân tích video mẫu", "làm sao để edit giống video này", "hiệu ứng chuyển cảnh này tên gì", "what transition is this"; or asks why their remake does not look like the reference ("so sánh bản làm lại"). Works on a local file. Not for downloading from TikTok or YouTube, telling filmed from AI footage, or editing.
license: Apache-2.0. LICENSE.txt has the complete terms
compatibility: Requires Python 3.9+ with numpy and Pillow, and FFmpeg with ffprobe. Runs offline; only the optional --check-api step, font lookalikes (downloaded once from Google Fonts) and the EditAtlas MCP use the network. Designed for Claude Code and other agents with a shell that can read images.
metadata:
  author: EditAtlas
  version: "0.5.0"
  status: beta
  library: techniques sfx
  mcp-tools: search_techniques get_technique search_sfx get_workflow
---

# Video breakdown: from a video someone likes to named techniques and a recipe

This is video-breakdown 0.5.0.

The person has a video they like and cannot name what is in it. You give them, shot by shot, the correct name of
each transition, camera move, text style and sound, the EditAtlas technique that makes it, and the steps to make
one like it with their own footage.

Three things are true the whole way through:

- **The numbers are hints, the frames are the evidence.** `analyze.py` measures pixels and samples. It confuses a
  crash zoom with a join, an iris with a dip to black, an old film's flicker with cuts. Every element you name must
  come from frames you opened with the Read tool. Say which ones you only measured.
- **You cannot hear.** Audio numbers say where something sudden happens, how loud, how bright, and the tempo.
  They do not say what the sound is. Never write "a whoosh" for a transient you have not identified; write
  "a short bright hit at 4.9 s, near the zoom".
- **Never invent.** Work only on the file the person gave. Every technique slug and sound id in the report comes
  from an EditAtlas search or get call in this session. If nothing fits, say so.

Scripts are in `scripts/` (Python 3.9+, numpy, Pillow, FFmpeg with ffprobe in PATH). Run them with the skill
folder's path, from a working folder of your own (`work/`); never write into the person's folders.

```
python SKILL/scripts/analyze.py VIDEO --out work/bd                      # breakdown.json + sheets
python SKILL/scripts/frames.py VIDEO --at 6.8 --span 0.6 --step 0.04 --out work/look   # every frame of a join
python SKILL/scripts/frames.py VIDEO --at 7.9 --crop 0,60,100,40 --out work/look      # bottom 40 %, to read text
python SKILL/scripts/text_look.py VIDEO --at 3.6 --crop 12,24,76,11 --text "Caringbah" --fonts sans-heavy --out work/text/title
python SKILL/scripts/elements.py VIDEO --out work/el                    # motion graphics: each element in, hold, out
python SKILL/scripts/background.py VIDEO --at 1.2,4.0 --out work/bg     # flat, gradient or radial background, hex
python SKILL/scripts/compare.py REFERENCE REMAKE --out work/compare      # what a remake does differently
python SKILL/scripts/report.py work/bd/breakdown.json work/bd/notes.json --out result/breakdown.md --check-api
```

## When the inputs are missing

- **No file, only a link** (TikTok, Reels, YouTube): ask the person to download the video and give you the file
  path. This skill does not fetch from platforms. A screen recording of the video also works.
- **No video at all**: ask for it. Do not describe what such a video "usually" has.
- **Very long video** (over 5 minutes): `analyze.py` reads the first 300 s. Ask which part matters, or pass
  `--max-seconds`.

Breakdowns are for learning how a video was edited. The recipe uses the person's own footage; do not suggest
reusing the reference's footage, music or characters.

## 1. Measure

Run `analyze.py`. It prints a summary and writes `breakdown.json` with:

| Part | What it holds |
|---|---|
| `format` | size, shape (9:16, 16:9), fps, duration |
| `pacing` | shots, joins a minute, median / shortest / longest shot, joins in the first 3 s, regularity |
| `joins` | each change of shot: time, length, kind (`cut`, `cross-dissolve`, `dip to black`, `white flash`, `bright flash`, `wipe` with the side it comes from, `shape wipe` (a flat shape grows over the picture) with its outline and side, `push or slide` with the direction, `zoom transition`, `blur transition`, `snap zoom or punch-in`, `jump cut`, `gradual (other)`) |
| `shots` | per shot: measured camera words (push in, fast zoom, pan, shake, hold, speed change), the look (dark, warm, black and white, black bars, dark corners), and for shots that hold still, the timing: how long things take to come in, how long it holds, how they leave |
| `overlays` | `events`: moments one band of the frame changes while the rest holds (text, stickers, graphics coming or going); `persistent`: regions that stay through joins (logo, frame, caption bar) |
| `audio` | loudness, speech-like share, tempo candidates and whether cuts land on the beat, transients (sudden sounds) with the nearest picture event, swells (rises into a moment) |

What each number means and where it goes wrong: `references/reading-the-numbers.md`. Read it before your first
breakdown of a session.

## 2. Look

Open, with the Read tool, in this order:

1. `overview.png`: the whole video in 24 frames or more (every 0.15 s in a short video, one a second or less in a
   long one). Get the story and the style first, and where each piece of text comes in.
2. `shots_NN.png`: first, middle and last frame of every shot. Check each shot is real: a crash zoom, a flash or
   a flicker can split one shot in two; a dissolve inside the source footage can look like a join.
3. `joins_NN.png`: six frames across every join that is not a plain cut. Name the transition from these.
4. `events.png`: before and after each overlay event. This is where captions, stickers and graphics show.

Then use `frames.py` wherever you are not sure: `--step 0.04` (one frame at 25 fps) across a join to see its
shape, `--crop` to read small text or see how a word enters (pop, bounce, slide, typewriter), `--times` for a
few moments side by side. Two or three close looks are normal; a short video with many effects may need more.

Check the format against the picture. A 9:16 video whose shots look cut out of wider footage (a film, a podcast, a
game: faces and objects cropped at the sides, a frame that sits differently in each shot) is a reframe: say so, and
search `reframe to vertical`. Wide footage with black bars is letterboxed or pillarboxed instead.

Write down, for every element, what you see in plain words before you look for a name: "the old picture is
squeezed into a horizontal line while the new one shows behind it", not "a squeeze".

### Text on screen

Text is what people copy first and what a remake gets wrong most: the wrong kind of script, flat colour where the
original has a gradient, text in front of a person where the original puts it behind. For every piece of text that
is not plain subtitles, find these five things:

1. **Layer.** Does a person or object cover part of the letters (hair over the bottom of a word, a hand in front)?
   Then the text is behind the subject: `compositing-text-behind-object`. Look at a crop where they overlap. Check
   every title, not just the first: one video can put several words behind the subject.
2. **Entrance.** `frames.py --at <time it appears> --span 0.6 --step 0.04 --crop ...`: slides in with motion blur
   (from which side), drops from above, pops (scale), fades in, types on, word by word or all at once, and whether
   words move again after they land. Overlay events miss text that comes in while the camera moves; use the
   overview to find those times.
3. **Colour.** Run `text_look.py` on a crop of the text once it is fully in and still. Crop one line with a little
   background on every side. It prints the fill (solid, or a gradient with its direction and stops as hex colours),
   an outline or offset shadow, a glow or dark halo around the letters, and how far the letters lean. Open
   `look.png`: "taken as text" must show the letters and nothing else. If it took a face or left out part of a
   gradient, run again with `--text-clusters` and the cluster numbers that are text (the panel under it shows each
   cluster). Each word can have its own colours: measure each title separately.
4. **Font.** Describe the letters first: sans or serif or script; for scripts, even strokes (brush, marker,
   casual) or thick downstrokes with hairline upstrokes (formal, calligraphic); weight; upright or leaning; upper
   or lower case; wide or condensed. `text_look.py` prints the stroke weight and contrast, which tell a
   calligraphic script (contrast 2.2 or more) from a brush one. Then add `--text "<the words exactly as shown>"
   --fonts <groups>` (`--list-fonts` shows them) for the one or two groups that fit, and compare the letters by
   eye: capitals, the shapes of a, g, t, the joins. The match number helps for sans and serif fonts and is weak for
   scripts. Name one or two free lookalikes and say they are lookalikes, not the creator's font.
5. **Place and size**: where it sits, how long it stays, and the font size. With `--text`, `text_look.py` prints
   the size in each lookalike (the same letters need a different size in each font): give the size in the font
   you name ("Oswald, about 120 px on a 1080x1920 frame"). Remakes usually set text too small.

### Designed motion

For logos, titles, charts and graphic videos, the timing is what makes them look finished, and what a remake
gets wrong. Read each shot's `timing` (`comes in over 0.7 s, fast, then settles; still for 71 % of the shot;
leaves over 0.8 s, slow, then speeds up`) and `format.loops`, check them in the frames, and put the numbers in
the element's `seen` or `note` and in the recipe. On a plain background, a graphic that grows or appears can be
reported as a join (`jump cut`, `snap zoom`, `zoom transition`): if the background stays, it is the element's
entrance. Details: "Designed motion" in `references/reading-the-numbers.md`.

For motion graphics on a flat or gradient background, also run `elements.py` and open `timeline.png`: each
graphic's entrance (slides from which side, scales up, wipes, fades, cuts on), hold and exit, a `stagger` (things
coming in one after another, with the gap) and what is `carried across the cut` (the same shape in the same place
on both sides: a graphic match cut). Shots over footage are skipped. For designed backgrounds,
`background.py --at <a still moment of each shot>` gives the hex colours and the gradient's direction.

## 3. Name it with EditAtlas

For each element, search by the result, not by a guessed name:

- `search_techniques` with the plain description ("circle closes to black then opens", "words bounce in one at
  a time", "sudden fast zoom into subject"). Use `category` to narrow (transition, captions, motion, vfx, color).
  Search terms that work for each analyzer label are in `references/reading-the-numbers.md`.
- `get_technique` on the best one or two, and keep the one whose description matches what you saw. Copy its
  `slug` and `name` exactly. Mark the match `exact`, `close` (same idea, a detail differs) or `partial`.
- Sounds: `search_sfx` by what the moment needs (pop for text appearing, riser into a hit, whoosh on a push). The
  sound in the reference is unknown to you; you are suggesting an EditAtlas sound for the same moment, so say so.
- `get_workflow` with the video type (`short_vertical`, `product_ad`, `food_review`, ...) for the pacing and
  structure EditAtlas recommends; compare it with what you measured.

Without the MCP, the REST API answers the same searches: `https://edit.trysometh.ing/api/v1/techniques?q=...`
and `/api/v1/sfx?q=...`.

A plain cut, a talking stretch or the footage itself needs no technique: give it a `gap` saying so. When nothing
in EditAtlas fits a real effect, write what you searched in `gap`; that tells EditAtlas what is missing.

## 4. Write the notes and the report

Write `notes.json` next to `breakdown.json` (format and an example: `references/notes-format.md`): what is on
screen in every shot, every element with its time, plain description, evidence and EditAtlas technique or sound,
corrections where the measurements were wrong, a recipe, and what you did not check. Set `lang` to the person's
language (`vi` or `en`).

Run `report.py ... --check-api`. It refuses notes that skip a shot, leave an element without a technique or a
reason, or leave out what was not checked, and with `--check-api` it confirms every slug and sound id exists on
EditAtlas and that names match. Fix what it lists and run it again.

## Deliver

**First, a version check.** If the EditAtlas MCP is connected, call `get_skill` without a name. If it lists video-breakdown above 0.5.0, the first line of your reply says a newer version exists and how to update it (in Claude Code: `/plugin`, then Marketplaces, editatlas-skills, Update marketplace; elsewhere `get_skill` with name video-breakdown gives the step). Without the MCP, skip it.

Give the person, in their language:

1. Two or three sentences: what kind of edit this is and what makes it work (pace, the one signature effect).
2. The elements in time order with their names and links: the report's table, or the main rows of it.
3. The recipe: steps with their own footage, technique by technique. Offer to do the edit, which starts with
   `get_workflow`; and for the sounds, the `sound-design` skill (`get_skill`).
4. What is measured, what you looked at, and what is unknown: the creator's actual font (you give free
   lookalikes), the exact easing curves (`timing` gives durations and a shape, not the curve), what each sound
   actually is, whether footage was filmed or generated.
5. The report file (`result/breakdown.md`), written by `report.py --check-api` with nothing left to fix.

After delivery, ask whether the names and techniques were right and send the answer with `send_feedback` when
that tool is available.

## When the person sends their remake

If they ask why theirs does not feel the same, run `compare.py REFERENCE REMAKE --out work/compare` (`--offset 0.4`
if theirs starts 0.4 s later). It prints the differences largest first: how long moves take, cuts, rows of text
(how many, how tall, how far apart they come in), background colour, the look. Check each in `compare.png` before
you report it; a change made on purpose is not a fault, and a pair caught mid-move only shows the timing
difference again. Give each with its time, both numbers and the fix ("your title is 18 % smaller: set it to about
96 px"). No notes or report file is needed for this.

## References

- `references/reading-the-numbers.md`: every measurement, its known errors, and search terms per label. Read before
  the first breakdown of a session.
- `references/notes-format.md`: the notes.json fields with a complete example. Read before writing notes.
