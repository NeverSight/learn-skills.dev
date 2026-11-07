---
name: visant-video-editor
description: 'Edits vlogs, event videos and video lessons from raw footage: breakdown, silence cuts that never clip a word, loudness and chapters, with a self-test against silent failures. Use on "edit this vlog", "cut the silence", "edit this lesson", "monta um vlog", "decupagem", "edita essa aula", "tira o silêncio do vídeo", /visant-video-editor.'
---

# Visant Video Editor

## Requirements

| Needed for | What | Check |
|---|---|---|
| everything | Windows (Git Bash), macOS or Linux, with bash 3.2+ | `bash --version` |
| everything | ffmpeg + ffprobe on PATH (libx264, aac; `drawtext` for the contact sheet) | `ffmpeg -version` |
| `plan.py`, `transcribe.sh` | Python 3 (`PYTHON=` picks the interpreter) | `python --version` |
| `transcribe.sh` | faster-whisper (`pip install faster-whisper`) | `python -c "import faster_whisper"` |
| silence inside a take (optional) | auto-editor (`pip install auto-editor`) | `auto-editor --version` |
| real photo dates (optional) | exiftool | `exiftool -ver` |

No Node, no GUI app. Everything else is POSIX shell + awk. See
[references/tools.md](references/tools.md) before adding any tool.

## What it does

Assembles a vlog from a raw folder. The material is phone footage: dozens to hundreds of files,
takes of 1 to 120 s, mixed orientation, audio level varying 20 LU between clips.

Two halves that do not replace each other:

1. **Gate** (`scripts/self-test.sh`, deterministic): the pipeline delivers a whole video or
   nothing. Binary grade.
2. **Judgment** (you, reading the breakdown): which take goes in, in what order, for how long. No
   script decides that well.

> **Rule zero: the cut list goes for approval before encoding.** Encoding 25 min of material from
> a cloud drive costs an hour. Proposing the cut list as text costs seconds. Never render a master
> without the user having seen the cut list, unless they explicitly said "just do it".

> **A green gate is not a watched video.** The gate proves no cut vanished and audio hits the
> target. It does not prove the opening is good or the right take went in. Always open a contact
> sheet before saying it is ready.

## Before touching anything

```bash
bash scripts/self-test.sh
```

~2 min, own sandbox with fixtures generated on the spot. **Gate closed = do not edit a client
video**: the failures covered are all silent (exit 0 with a wrong video). If you changed a
pipeline script, run it again.

## Flow

```
1. self-test          gate. Without it, do not start.
2. ingest.sh          reads metadata of everything -> _build/manifest.tsv (sorted by capture)
3. cutlist.sh         proposes the cut under a ceiling -> _build/edl.txt
4. breakdown.sh       cut sheet + chapters + contact sheet
5. >>> APPROVAL <<<   show the breakdown and the total; wait for the ok
6. build.sh           normalizes each cut and concatenates -> _out/vlog.mp4
7. verify             loudness, duration, contact sheet. Only then say ready.
```

All at once, when the user already approved the profile:

```bash
SRC=/path/media PROJ=/path/project PROFILE=youtube bash scripts/all.sh
```

`PROJ` is where `_build/` and `_out/` are born. `SRC` is the media folder: it is **never
written**, and the gate tests that. Old Portuguese names (`tudo.sh`, `roteiro.sh`, `TETO_MIN`,
`PERFIL`, `_build/transcricao/`...) still work; the scripts' headers list them.

## Profiles

| `PROFILE` | Format | Speech take | Use |
|---|---|---|---|
| `youtube` (default) | 16:9 1920x1080 | **whole** | event vlog, long record |
| `reels` | 9:16 1080x1920 | 8 s max | social cut, 1 min ceiling |
| `archive` | 16:9 | whole, nothing trimmed | organized raw archive |

## Decisions that matter

| Decision | Default | Why |
|---|---|---|
| Fill | `FILL=auto` | horizontal clip fills the frame (crop); vertical clip goes in over a blurred background. Cropping vertical to 16:9 **destroys the framing**. The decision reads the display matrix, not pixel width |
| Loudness | `LOUD=2` (two passes) | one pass compresses the dynamics. Numbers in [audio.md](references/audio.md) |
| Transition | hard cut | a good vlog is cuts. Wipe and crossfade on b-roll look like a template |
| Cut length | proportional to the take | a flat ceiling produced 41 identical 5.0 s cuts: conveyor-belt rhythm |
| Order | chronological by `creation_time` | builds the narrative by itself (setup → arrival → event). Valid for video; **not for photos** |
| Cache | content key | md5 of file+in+out+fill+format+audio. Never by position |

## The cut list (`_build/edl.txt`)

One line per cut, TAB-separated. This is where the real editing happens:

```
file.MOV	0	12.5      # in at 0s, out at 12.5s
other.MOV	4	9         # only 4s to 9s
photo.jpg	0	3         # photo = 3s with a slow zoom (Ken Burns)
# a line with # is ignored    <- "deletes" a take without deleting the file
```

Reordering lines reorders the video. Commenting is how you drop a bad take.

`cutlist.sh` classifies by take length and **never sacrifices narrative**: if it busts the
ceiling, it tightens the caps first and only then thins the b-roll by uniform sampling. A long
take (>25 s) is speech and always goes in.

```bash
MAX_MIN=5 bash scripts/cutlist.sh     # 5 min target
MAX_MIN=0 bash scripts/cutlist.sh     # no ceiling
MAX_LONG=0 bash scripts/cutlist.sh    # whole speech take
PHOTOS_PER_DAY=0 bash scripts/cutlist.sh
```

## Breakdown deliverables

`breakdown.sh` produces three things the user actually uses:

- `BREAKDOWN.md`: one line per cut: timeline position, file, day, how much of the raw was used,
  type (speech/medium/b-roll) and framing
- `CHAPTERS.txt`: chapters per day, ready for a YouTube description (the first one **must** be
  `00:00:00`, or YouTube rejects them)
- `_build/contact/sheet-*.jpg`: grid of numbered thumbs. **Open at least one before declaring
  ready.** It is the only way to see the content without watching it all

## Before saying it is ready

```bash
ffprobe -v error -show_entries format=duration,size -of default=nw=1 _out/vlog.mp4
ffmpeg -hide_banner -nostats -i _out/vlog.mp4 -af ebur128 -f null - 2>&1 | tail -12
```

Check: duration matches the EDL sum; `I:` within ±1 of target; `LRA:` between 5 and 12 (below 3 =
over-compressed). Then open the contact sheet and look at the **opening**: does the vlog open on
a strong clip or on a blurred vertical?

## Narrated edit (essay, not log)

When the material has speech with content, the order does not come from the date, it comes from
the argument. The path (run from the project folder, or set `PROJ`):

```bash
bash scripts/transcribe.sh       # sentences with timecode
bash scripts/frames.sh           # entry point of each clip
# cut the speech blocks into _build/speech_audio (audio) and _build/speech_video (video+audio)
python scripts/plan.py           # builds the EDL by argument
bash scripts/build.sh
```

**Narration EDL**: 5 columns, video from one file and voice from another:

```
broll.MOV   in   out   narration.m4a   voice_in
```

**Face moment**: 3 columns pointing to the speech clip itself in `speech_video/`, which has video and
audio cut together. Guaranteed sync, seamless narration.

Field-measured rules (detail in [pitfalls.md](references/pitfalls.md)):
- ambience breath **only** between blocks from different sources
- global pool with no repetition (otherwise the video spins on the same 6 clips)
- long continuous speech block: 40-56 s without interruption is what sounds natural

## Video lesson / course (screencast, running speech)

A different shape from a vlog: usually **one file** (or a few from one recording session), video
and audio **always from the same source** (no separate b-roll for narration), and the problem is
not finding the right take: the recording has minutes of dead silence (screen being watched,
nobody talking) between good sentences, and sometimes one bad audio event (background scream, mic
bump).

Flow (does not use `cutlist.sh`/`frames.sh`/`plan.py`, which separate narration from b-roll;
here video and audio never separate):

```
1. transcribe.sh              sentences with timecode for each raw file
2. read the transcript        decide which sentences GO IN, in order
3. write the EDL by hand      file\tin\tout, one per sentence (not per take)
4. audio anomaly scan         see references/course-lessons.md: peak and drop
5. build.sh                   same trim+concat+loudnorm engine as the vlog
6. check the cut              listen to the splices, especially where an event was removed
```

Hard rule: **never cut in the middle of a word or of a line of reasoning in progress.** Tighten
silence to almost zero, but only at the real boundary between sentences/clauses. See
[references/course-lessons.md](references/course-lessons.md) for finding that boundary in
whisper's timestamps without guessing.

**The end of the lesson is where this breaks most.** The final cut lands on a "to recap…" and the
evaluation that closes the reasoning ("took 7 minutes, had one error, grade 8") gets left out,
almost always because right before it there is a stalled attempt ("in roughly 450 seconds" +
silence). Remove the attempt and keep the resumption; never drop the evaluation with it. Before
closing the breakdown, check every lesson whose next word in the raw comes within 3 s of the cut,
looking at what stayed and what comes next, with pauses marked. The reader decides: sound does not
know where reasoning closes, and whisper barely uses full stops. Record the accepted ending with
the sentence that closes it. It is not a mid-thought cut when what comes next is already the next
lesson, when "cut" was said in the recording, or when the subject turns ("now the next test…").

Unwanted audio event (scream, bump, peak): **literal cut by default**, do not lower the volume.
Ducking is fragile here: the compressor and loudnorm that run afterwards tend to raise what was
lowered, and the result "seems to work" until someone listens closely. Only consider a duck if
cutting the time would destroy a sentence that must stay whole, and even then say it is an
exception. Full detail, with the measured why, in
[references/course-lessons.md](references/course-lessons.md).

## When the material is speech-heavy

`cutlist.sh` picks takes; it does not clean the middle of a take. That is what `auto-editor` is
for: it cuts silence inside the take. Run it **before** ingest, into a separate folder. See
[tools.md](references/tools.md).

## Media on a cloud drive

On a Google Drive for desktop mount the file is virtual until read, and every read forces a
download. Ingesting ~170 files takes minutes; encoding 2.5 GB takes an hour.

**Run in background and tell the user the cost first**, not after. Never call `all.sh` in
foreground thinking it is fast.

## Read when needed

- **[references/pitfalls.md](references/pitfalls.md)**: the silent failures of this pipeline,
  with root cause. **Read before touching any script**, and before diagnosing a bug by symptom
  similarity: one case there is a wrong diagnosis that cost a one-hour rebuild.
- **[references/audio.md](references/audio.md)**: loudness targets, one vs two passes, de-click,
  music bed, desk mic. Read when touching audio or on "the sound is weird".
- **[references/tools.md](references/tools.md)**: what already exists (auto-editor,
  faster-whisper, ffmpeg-normalize, exiftool) and what not to bring in. Read before writing
  anything new.
- **[references/course-lessons.md](references/course-lessons.md)**: sentence-level breakdown of
  screencasts/lessons: safe cut boundaries in whisper timestamps, finding a bad audio event
  without confusing it with speech emphasis, and why a literal cut beats a duck.
- **[references/cases.md](references/cases.md)**: the jobs these rules came from.
