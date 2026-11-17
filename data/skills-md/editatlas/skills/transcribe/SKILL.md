---
name: transcribe
description: Transcribe the speech in a video or audio file on the person's own machine with Whisper (faster-whisper), with a time for every word, then check it, write SRT/VTT subtitles, and list what an edit could cut (long silences, filler words like um, uh, ờ, ừm, and repeated takes). The checked word-level transcript is what EditAtlas caption techniques, silence and filler removal, retake selection and every template's verified_transcript input need. Use it whenever someone wants a transcript, subtitles, captions or an SRT from a video; asks to "trích lời", "lấy lời thoại", "chuyển giọng nói thành chữ", "làm phụ đề", "làm sub", "cắt khoảng lặng", "bỏ ờ ừm", "speech to text", "Whisper"; or starts an EditAtlas edit that needs word times, even if they never say "transcript". Installs Whisper only after asking. Not for translating, cleaning up audio, separating a voice from music, or making a voice.
license: Apache-2.0. LICENSE.txt has the complete terms
compatibility: Requires Python 3.9+ with faster-whisper (pip, about 300 MB on disk) and FFmpeg with ffprobe. The first run downloads a Whisper model from Hugging Face (0.5 to 1.6 GB); after that it works offline and no audio leaves the machine. Runs on CPU; an NVIDIA GPU is faster. Designed for Claude Code and other agents with a shell.
metadata:
  author: EditAtlas
  version: "0.2.4"
  status: beta
  library: techniques templates
  mcp-tools: get_technique search_techniques get_workflow
---

# Transcribe: word-level transcripts for editing

This is transcribe 0.2.4.

The aim: a transcript the person has checked, with a start and end time for every word, ready for captions and
cuts. Whisper runs on their machine; nothing is uploaded.

Two things are true the whole way through:

- **Whisper writes what it heard, not what was said.** It mishears names, writes numbers its own way ("400ms" for
  "bốn trăm mi li giây"), and can invent whole lines in silence or under music ("Hãy subscribe cho kênh…",
  "Cảm ơn các bạn đã theo dõi", "Thanks for watching"). Never present a transcript as correct until the person has
  seen the review list. Never fill a gap with words you guess.
- **You cannot hear.** Confidence numbers, the audio level and the review list are your ears. Say what was measured
  and what still needs a person.

All scripts are in `scripts/` (Python 3.9+, FFmpeg). Run them with this folder's path, from a working folder of your
own (`work/`); never write into the person's project or this skill folder.

```
python SKILL/scripts/doctor.py                                   # what is installed, which model fits this machine
python SKILL/scripts/transcribe.py FILM.mp4 --out work/t --names "Minh Anh, EditAtlas"
python SKILL/scripts/fix.py work/t/transcript.json show 40-60    # words with numbers and times
python SKILL/scripts/fix.py work/t/transcript.json set 12-13 "EditAtlas"
python SKILL/scripts/captions.py work/t/transcript.json --max-chars 32
python SKILL/scripts/cuts.py work/t/transcript.json --out work/cuts
```

## 1. Ask first

You need, and must not invent:

1. **The file.** No file, no transcript: ask for it. Read nothing from the file name.
2. **The language** if it is not obvious. `transcribe.py` detects it and warns under 70%; then ask.
3. **Names, brands and terms** that must be spelled exactly (people, products, the channel, "EditAtlas"). They are
   not fed to Whisper: in tests that made it drop punctuation and invent a closing line. They are matched against
   what it heard afterwards, and close misspellings are suggested.
4. **What it is for:** subtitles to upload, captions burned in with an EditAtlas technique, cuts, or a template input.
5. **Who speaks**, for an interview or a talk with several people. Whisper does not tell voices apart; if the person
   wants "Interviewer:" / "Guest:" labels, say that you would add them from the sense of the text and that they need
   checking.

Run `doctor.py`; it needs nothing installed, and it exits 1 while faster-whisper is missing (expected). If it is
missing, tell the person what it is (a local copy of OpenAI's Whisper, about 300 MB on disk by pip, plus a 0.5–1.6 GB
model on first use) and install only when they agree: `doctor.py --install`, then `doctor.py --fetch turbo` so the download shows before the work starts. On a fast
line both took under a minute and a half in a fresh Python.

## 2. Transcribe

```
python SKILL/scripts/transcribe.py FILM.mp4 --out work/t [--language vi] [--names "..."] [--model turbo] [--verbatim]
```

- `--model auto` picks `turbo` (large-v3-turbo) on a GPU, and on a CPU for files up to 20 minutes; `small` beyond.
  Measured on a 12-thread CPU, turbo takes about 5–8 minutes for a 10-minute film (it processes 1.2–2.2 seconds of
  audio per second); small is about 3 times quicker but misheard Vietnamese (9–10% word errors against 0% for turbo
  on the same test film; "EditAtlas" became "Edith Atlas"). On real Vietnamese read speech turbo got 9.5% of words
  wrong, mostly foreign names and terms. Details: `references/models.md`.
- `--verbatim` keeps fillers and false starts that Whisper otherwise tidies away. Use it when the person wants fillers
  cut; it can cost a word elsewhere, so not by default.
- Voice activity detection with a 500 ms silence step is always on: without it, a Vietnamese test film ended with an
  invented "Hãy subscribe cho kênh La La School". It can also make Whisper skip a whole sentence, so any stretch the
  detector calls voice but that got no words is transcribed again on its own and listed for review ("second pass").
- With `--language` given, no language is detected and `language_probability` is null; pass it only when the
  person said which language it is.
- Look at the summary it prints: language, words, mean confidence, how many words are unsure, second-pass stretches,
  and the number of review items.

Outputs in `--out`: `transcript.json` (format in `references/formats.md`), `transcript.srt`, `.vtt`, `.txt` and
`review.md`.

## 3. Check it with the person

Open `review.md`. Each line is a word or a run of words, with why it is there:

| Why | What to do |
|---|---|
| looks like the name X | `fix.py ... names` applies every suggestion; look at them first |
| a line Whisper often invents | read the words around it; if nobody would say that there, `fix.py ... delete i-j` |
| unsure (p under 0.7) | check the sense of the sentence; if the right word is clear from context, fix it and say so; if not, ask |
| number | ask how it should be written (45 giây or bốn mươi lăm giây, $2,500) when it will be on screen |
| name? | a capital in mid-sentence: confirm the spelling |
| heard in near silence | likely invented; check the time against the picture |
| the same words repeat | Whisper looping; delete the extra copies |
| missed on the first pass | heard on its own after the first pass skipped it; read it with the sentences around it |
| speech runs to the very end | the file may stop mid-word; ask whether to keep the last word as it is |

A line from the invented list can be real: a YouTuber's own outro often says "subscribe". It is listed so someone
checks it, not so it is deleted on sight.

The list does not hold every wrong word: on real Vietnamese read speech with a reference text it caught about 4 in
10 (the rest were mostly words Whisper was sure of, such as "cãi tay đò" for "cãi tay đôi"). Read the whole
`transcript.txt` once for words that make no sense, and ask about the ones you cannot fix from context.

Fix with `fix.py` only, never by hand-editing times: `set` keeps the times (several heard words can become one, or
one can become several), `delete` removes invented words, and both rewrite the subtitle files and `review.md` and log
the edit. Word numbers start at 0 everywhere; `fix.py ... review` prints the items still open, and
`fix.py ... ok N` closes one that is right as heard. Read words with `fix.py ... show`: a Windows console cannot
print Vietnamese from your own Python unless `PYTHONIOENCODING=utf-8` is set (and `python -I` ignores it). Then show the person
the corrected text (`transcript.txt`) and the remaining review lines. When they confirm, run
`fix.py ... checked`. A template's `verified_transcript` must be a transcript marked checked.

## 4. Subtitles

`transcribe.py` and `fix.py` write subtitles with the EditAtlas Clean Subtitle rules: at most two balanced lines of
38 characters, a break at sentence ends and pauses, each caption held for its phrase plus 150 ms, never overlapping
the next. For 9:16 video use `captions.py ... --max-chars 32`. It flags captions read faster than 17 characters a
second: a fast speaker, not an error, but mention it for burned-in captions (word-by-word styles read better).
Captions break where a phrase starts (punctuation, a breath, words like "là", "và", "nhưng"), so a two-syllable
word is rarely split, but there is no dictionary: read the lines once, and if one splits a word such as
"tiết / kiệm", move the break by hand in the SRT after the last `fix.py` edit (fix.py rewrites the SRT). Vietnamese
talk usually runs past 17 characters a second (a real 6-minute talk: 69 of 96 captions). Do not shorten or reword
what was said to meet the number unless the person asks.

For styled captions burned into the picture, call EditAtlas `search_techniques` (for example "word by word captions")
and `get_technique`; build the ASS file from the words in `transcript.json`, not from the SRT.

## 5. Cuts (only when the edit wants them)

```
python SKILL/scripts/cuts.py work/t/transcript.json --out work/cuts [--min-silence 0.4] [--pad 0.12]
```

It finds silences from the gaps between words, then moves each edge to where the audio is really quiet (Whisper's
word ends can sit 0.1–0.4 s off), keeping `--pad` around every word. Sure fillers (um, uh, ờ, ừm) are cut; words that
are sometimes fillers (like, you know, kiểu, thì là) and earlier takes of a repeated line are listed as "ask". On
test films with known pauses it cut no speech, left no pause over 0.39 s, and kept at least 80 ms beside every word.

When music or noise runs under the voice, a pause is not quiet: the voice detector finds pauses instead, fillers turn
into "ask" (their edges cannot be measured), and every cut also cuts the music. Say so; cutting before the music is
added, or re-laying it after, sounds better.

Show the person `cuts.md` and settle every "ask" line (`--take-maybe`, `--take-retakes`, or leave them). Then render
with the EditAtlas technique `edit-silence-removal` or `edit-filler-removal` (`get_technique`), using the
expressions in `ffmpeg_cut.txt`; picture and sound are cut at the same times. Captions for the cut film come from
`transcript_cut.json`, whose word times are already in the cut film's time (checked by transcribing a cut film again:
10–20 ms median difference). The expressions cut hard; the filler-removal technique adds a 10–30 ms audio fade at
each join, so apply it when rendering (`ffmpeg_cut.txt` lists the joins that came from fillers).

## 6. Deliver

**First, a version check.** If the EditAtlas MCP is connected, call `get_skill` without a name. If it lists transcribe above 0.2.4, the first line of your reply says a newer version exists and how to update it (in Claude Code: `/plugin`, then Marketplaces, editatlas-skills, Update marketplace; elsewhere `get_skill` with name transcribe gives the step). Without the MCP, skip it.

Give the person, in their language:

1. The files: `transcript.txt` to read, `.srt`/`.vtt` to upload, `transcript.json` for the edit; `cuts.md` when cuts
   were asked for.
2. The numbers: model, language, words, unsure words, review items and what was done with each; for cuts, length
   before and after and the cuts by kind.
3. What is still unchecked: names or numbers nobody confirmed, lines kept on the person's word, whether the
   transcript is marked checked.

Never claim the transcript is word-perfect; say it was checked against the review list and by whom.

If you then put the captions on a video for them, offer an editable copy once: the editable-export skill opens it in
the EditAtlas studio, where they fix a word, a timing or the caption size themselves and export the MP4 again.

**Last, ask once how it went.** If the EditAtlas MCP is connected, ask the person, in one short message in their
language, about each thing from EditAtlas you used, by name: the techniques, sounds, music, stock clips and this
skill. Send each answer with `send_feedback`, about `this_item`; an answer only about the whole video goes once, as
`whole_edit`. Send only what they said, and nothing if they do not answer. Ask once per edit: if you or another
skill already asked, skip it.
