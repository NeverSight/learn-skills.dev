---
name: talking-head-cut
description: Cut a raw talking-head recording (one person speaking to camera, a lesson, a vlog, a voice-over take) into a clean video. Takes out false starts, failed and repeated takes, words said to the editor ("take two", "nói lại nhé"), doubled words and um/uh/ờ/ừm. Shortens long pauses to a natural breath and keeps everything the speaker meant to say. You quote the words to remove; the scripts find them, put every cut in silence, render picture and sound in step, then transcribe the cut again to catch leftovers and clipped words. Use it when someone asks to "cut my mistakes out", "clean up this take", "remove the retakes", "tighten the pacing", "rough cut", "cắt video nói chuyện", "cắt chỗ nói hỏng", "bỏ đoạn nói lại", "cắt ờ ừm và khoảng lặng", "dựng video nói cho gọn". Needs the transcribe skill's word-level transcript. Not for a transcript or subtitles alone (transcribe), picking highlights from a long video, multi-camera edits, or adding music, B-roll or captions (do those after the cut).
license: Apache-2.0. LICENSE.txt has the complete terms
compatibility: Requires Python 3.9+ with numpy, FFmpeg with ffprobe, and the EditAtlas transcribe skill (faster-whisper) for the transcript and for verify.py. Runs on the person's machine; nothing is uploaded. Designed for Claude Code and other agents with a shell.
metadata:
  author: EditAtlas
  version: "0.2.0"
  status: beta
  library: techniques
  mcp-tools: search_techniques get_technique get_skill send_feedback
---

# Talking-head cut: from a raw take to a clean cut

This is talking-head-cut 0.2.0.

The result: the person's raw recording cut so it says what they meant, once, with natural breathing room, and
nothing they meant to say lost. They also get a list of every cut with the words it removed, and a transcript of
the cut film for captions.

Two things are true the whole way through:

- **You cannot hear.** The transcript, the measured levels and `verify.py` are your ears. A render that finished is
  not a cut that is right. Say what was measured, and ask the person to listen at the joins the check lists.
- **The transcript is right about words and wrong about times.** Whisper often starts the first word after a pause
  a second early and lets last words run into the silence. So you never type a time: you quote the words, and
  `cut.py` measures where their sound starts and ends and puts every cut in the quiet beside it.

All scripts are in `scripts/` (Python 3.9+, numpy, FFmpeg). Run them with this folder's path, from a working folder
of your own (`work/`); never write into the person's project or this skill folder. `TRANSCRIBE` is the transcribe
skill's folder (next to this one when installed from the EditAtlas plugin).

```
python TRANSCRIBE/scripts/transcribe.py RAW.mp4 --out work/t --verbatim --language en
python SKILL/scripts/takes.py work/t/transcript.json RAW.mp4 --out work/cut
python SKILL/scripts/cut.py work/t/transcript.json RAW.mp4 work/cut/plan.json --out work/cut
python SKILL/scripts/render.py work/cut/edl.json --out work/cut/cut.mp4
python SKILL/scripts/verify.py work/cut/cut.mp4 --cut work/cut
```

## 1. Ask first

You need, and must not invent:

1. **The file.** No file, no cut: ask for it. Several clips: ask for their order, and cut each one.
2. **What kind of cut.** The default is clean-up: mistakes, retakes, notes to the editor, fillers and long pauses go;
   everything the speaker meant stays. Shortening to a length, dropping a section or reordering is a different job:
   do it only when asked, and list each content cut for the person to approve before it is made.
3. **The pace.** `natural` (default: YouTube, lessons, about 0.45 s between sentences) or `tight` (Shorts, Reels,
   TikTok: about 0.3 s). `keep` removes the mistakes and leaves every pause as it was.
4. **What must stay**, if they say so: a joke built on a stumble, a deliberate repetition.

If the transcribe skill is missing, the EditAtlas MCP's `get_skill` with name `transcribe` says how to add it. Run
its `doctor.py` before installing anything, and install only when the person agrees.

## 2. Transcribe, verbatim

```
python TRANSCRIBE/scripts/transcribe.py RAW.mp4 --out work/t --verbatim --language en
```

`--verbatim` keeps fillers, false starts and repeated words that Whisper otherwise tidies away; without it the
mistakes you need to cut are missing from the text. Pass `--language` when you know it. If a name or term you will
quote was misheard, fix it with the transcribe skill's `fix.py ... set` first: quotes match the transcript's words.

## 3. Read the takes

```
python SKILL/scripts/takes.py work/t/transcript.json RAW.mp4 --out work/cut
```

It prints the take as numbered lines (L1, L2, ...), split where the speaker stops, with the measured pause after
each, and marks:

| Mark | Means | Usually |
|---|---|---|
| `NOTE?` | words said to the editor: "sorry, start over", "take two", "cut that", "nói lại nhé", "bỏ câu này" | the note goes, and so does the attempt it replaces |
| `RETAKE?` | a line said again, nearly the same, a little later | keep the later complete one |
| `UNFINISHED` | the line breaks off ("...", "-") and is said again within three lines | a false start: it goes; the complete version stays |
| `BREAKS OFF` | the line breaks off and the next line goes on with the same sentence ("Và tai này thì... / nó đã có...") | a pause in one sentence: keep both lines; the pause is shortened |
| `DOUBLED` | the same words twice in a row ("the best part, the best part is"), with the plan item for it | only the first copy goes: use that item, never the whole line, which holds other words |
| `[um]` | a sure filler | `cut.py` removes these |
| `SOUND?` | voice with no words in the transcript | often a false start Whisper skipped: look at it |
| `LONG WORD?` | a word far longer than this speaker's words: Whisper may have written a repeat once | read the `HEARD` mark |
| `HEARD "..."` | what Whisper hears in a `LONG WORD?` or `SOUND?` line transcribed on its own, when that has more words | the extra words were said: usually a doubled phrase or a false start to remove |

`takes.py` listens again to `LONG WORD?` and `SOUND?` lines by itself (faster-whisper, a few seconds a line). In a
real recording Whisper often writes a phrase said twice ("and that is that, and that is that every...") only once,
with one word stretched over both; the second listen, without the rest of the take around it, usually hears it.
Then the line's words before the long word are usually the first copy, and the long word holds the second: on a test
take, "And that is that every" was the first "And that is that" plus an "every" lasting 1.1 s over "and that is that
every". Quote those words with the line (`{"quote": "and that is that", "line": 13, "nth": 1}`), and let `verify.py`
confirm: MISSING means you took the wrong copy.

Read every line, not only the marked ones: the marks are hints, and a line can be wrong in a way no mark catches.

## 4. Decide what goes

This is the part that needs you. In order:

1. **Notes to the editor first; they outrank your judgment.** "Sorry, start over", "take two", "quay lại từ đầu
   nhé": the note goes, and the attempt it replaces goes with it. That attempt runs back to where the
   speaker started the same idea, which can be one line or several.
2. **Retakes: keep one complete version of each idea.** Usually the later one, because the speaker redid it for a
   reason. Keep the earlier one only for a fault you can show: a missing word, a clipped end measured in the
   levels, a note to the editor. A word Whisper wrote differently ("pay" for "paid") is Whisper, not the take. But keep a lead-in from the earlier attempt if the later one does not repeat it ("Open the settings
   page." before a failed and then a good "Then click Export..."). Never stitch half sentences from two attempts
   into one.
3. **False starts:** an abandoned beginning followed by a complete version: remove only the abandoned part. A
   line that stops and then carries on in the next line is not one: nothing was said again, so nothing goes.
4. **Doubled words:** cut the first copy ("the best part, the best part is" keeps the second).
5. **Fillers:** um, uh, er, ờ, ừm go (`cut.py` does it). Words that are only sometimes fillers stay unless they are
   pure hesitation: "so" meaning "therefore", "like" in a comparison, "vì", "nên", "thì", "kiểu như" in a real
   sentence. If unsure, keep.
6. **Deliberate repetition stays.** "Every take. Every single take." and "thật sự, thật sự cần" are emphasis, not
   retakes.
7. **Pauses are shortened, not removed**, by the pace. A pause in the middle of an idea that the speaker took to
   think stays as a natural breath.
8. **Do not cut content on your own.** An aside, an example or a long intro the speaker meant to say stays in a
   clean-up. If you think it should go, list it in your reply as a suggestion.

When you are unsure about a line, keep it and ask about it in your reply, quoting the words.

## 5. Write the plan and cut

Write `work/cut/plan.json`. Name what to remove by line numbers from `takes.md` or by quoting words; never by time.

```json
{
  "pace": "natural",
  "fillers": true,
  "remove": [
    {"lines": "6-7", "why": "false start, then 'sorry, start over'"},
    {"quote": "the best part", "line": 12, "nth": 1, "why": "doubled words: the first copy goes"},
    {"lines": "20-21", "why": "replaced by the take after 'take two'"}
  ]
}
```

A quote must match the transcript's words (case and punctuation do not matter). When the same words are said more
than once, add `"line"`, `"nth"` or `"near": seconds`; `cut.py` stops and lists where they are said otherwise.
Every field, removing a sound with no words, and keeping a filler: `references/formats.md`.

```
python SKILL/scripts/cut.py work/t/transcript.json RAW.mp4 work/cut/plan.json --out work/cut
```

Read `cuts.md`: each removal with its words, and each join with the pause it keeps. A join marked "cut inside
sound" had no pause to cut in; listen there after rendering, or remove a word more so the cut lands in a pause.

## 6. Render and check

```
python SKILL/scripts/render.py work/cut/edl.json --out work/cut/cut.mp4
python SKILL/scripts/verify.py work/cut/cut.mp4 --cut work/cut
```

`render.py` cuts picture and sound over the same whole frames in one FFmpeg pass, with a 20 ms fade on the sound at each
join, and says whether picture and sound end together. `verify.py` transcribes the cut film again and lines it up
with the words the plan kept:

- **EXTRA** or **DOUBLED**: something you meant to remove is still there, or Whisper's first transcript missed it.
  Find it in `takes.md` around the source time, remove it in the plan, cut and render again.
- **MISSING**: a kept word was not heard. Check the plan did not remove it; if it sits at a join, the cut may have
  clipped it: keep a word more on that side.
- **FILLER**: an um is still in. **JOIN IN SOUND**, **NO BREATH**, **LONG PAUSE**: listen there, or adjust.
- **Heard differently** ("20" for "twenty") is Whisper, not the cut.

Fix every EXTRA, DOUBLED and MISSING before you deliver: change the plan (a `quote` with `line` or `near` reaches a
repeat the first transcript wrote once), cut, render and check again, up to three rounds. One EXTRA is not a fault:
words heard where `takes.md` had `SOUND?` (voice the first transcript wrote nothing for). `cut.py` keeps such voice
instead of cutting it as a pause, so read what was heard: content stays; a repeat or false start goes with
`"from"`/`"to"` around it. What is still listed after that goes in your reply with its time and words.

Then look at `seams.jpg` (the frame before and after every join). A talking head jumps at every join; that is
normal for this style, but a big jump can be covered. Offer it, do not do it unasked: B-roll over the join (the
EditAtlas media-picker skill) or a punch-in (`search_techniques` "jump cut punch in", then `get_technique`).

Repeat until the check is clean or every remaining line is explained. Do not hand over a cut whose check you have
not read.

## 7. Deliver

**First, a version check.** If the EditAtlas MCP is connected, call `get_skill` without a name. If it lists talking-head-cut above 0.2.0, the first line of your reply says a newer version exists and how to update it (in Claude Code: `/plugin`, then Marketplaces, editatlas-skills, Update marketplace; elsewhere `get_skill` with name talking-head-cut gives the step). Without the MCP, skip it.

Give the person, in their language:

1. **The cut film** (`cut.mp4`) and its length before and after.
2. **What was removed**, from `cuts.md`, quoting the words: "the first try at 'Open the settings and...', then
   'sorry, start over'". Never line numbers or word indexes: the person cannot see them.
3. **What you kept on purpose** and **what you were unsure about**, as questions.
4. **The check**: what `verify.py` found and what you did about it; that nobody has listened yet; the joins to
   listen to first. Say the check transcribed the cut again; do not write that you or Whisper listened to it
   ("nghe lại bản cắt"): that reads as if someone heard it.
5. **What comes next**, if they want it: captions from `transcript_cut.json` (its times are the cut film's; the
   transcribe skill's `captions.py` writes the SRT), music or B-roll (media-picker), sound effects (sound-design).
   Do these after the cut, never before: every one of them is timed to the cut.

If you then build more on top of the cut for them, offer an editable copy once: the editable-export skill opens it
in the EditAtlas studio, where they move a join or a caption themselves.

**Last, ask once how it went.** If the EditAtlas MCP is connected, ask the person, in one short message in their
language, about each thing from EditAtlas you used, by name: the techniques, sounds, music, stock clips and this
skill. Send each answer with `send_feedback`, about `this_item`; an answer only about the whole video goes once, as
`whole_edit`. Send only what they said, and nothing if they do not answer. Ask once per edit: if you or another
skill already asked, skip it.

## References

- `references/formats.md`: every field of `plan.json`, `edl.json` and the other files, and what the pace values are.
- `references/how-cuts-are-placed.md`: how `cut.py` measures the sound, places cuts and shortens pauses, and what
  `verify.py` can and cannot catch. Read it when a join sounds wrong or a check line is unclear.
