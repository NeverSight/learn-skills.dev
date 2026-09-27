---
name: scenario-seedance-music-video
description: "Use when turning a song, track, or audio master into a finished music video with Scenario and Seedance: planning shots against beats and sections, transcribing lyrics, generating clips that cut to music, keeping the shots' own sound while the song stays the only score, assembling a delivery over the untouched master soundtrack, or verifying the final cut. Keywords: music video, beat sync, shot list, lyric transcription, reference frames, ffmpeg assembly, Seedance."
license: MIT
---

# Scenario Seedance Music Video

## Overview

Five steps: song, lyrics, story, frames, video. The supplied master is the only score, and no shot writes its own. [scripts/build.py](scripts/build.py) lays the master over the cut once, at the end, and proves the file untouched by hash. [scripts/song.py](scripts/song.py) reads the master so cuts land on its structure. The scripts need ffmpeg and ffprobe on PATH, and numpy for song.py.

Connection and the core generation loop: see the `scenario` skill in this repo. The Seedance parameter contract and conditioning traps: see the `scenario-seedance` skill. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

## The two soundtracks

Music written inside a shot restarts in a new key at every cut, so the score comes from outside the video model: the supplied master. What Seedance makes is the sound bolted to the picture. The choice sets `generateAudio` on every shot, so make it before generating:

- Song alone: `generateAudio: false` everywhere. build.py stream-copies the master whenever MP4 allows, so the delivered soundtrack is the supplied file, bit for bit.
- Song over the shots' own sound: `generateAudio: true`, every prompt naming the sound the scene itself makes (heels on wet asphalt, room tone) and then "diegetic sound only, no music, no score", plus `"sound": 0.2` in the edit file. Name no instrument or genre, however well it fits the track: that invites a score, and one run failed on an output-audio content check for an added "distant guitar". build.py cuts each clip's audio to its slot, mixes it under the master at that gain, and refuses a mix that would clip. The delivery is then one AAC encode, trading the bit-for-bit guarantee for the sound; the master file stays hash-checked.

## Quick reference

| Step      | Call                                              | Notes                                                             |
| --------- | ------------------------------------------------- | ----------------------------------------------------------------- |
| 1. Song   | `python3 scripts/song.py master.mp3 -o song.json` | hash, duration, loudness, tempo, sections, cut candidates         |
| 2. Lyrics | `recommend` for transcription, `model_run`        | supplied lyrics win; sung-vocal transcription is a draft          |
| 3. Story  | one page, shown to the user first                 | the cheapest place to be wrong; name what must not drift          |
| 4. Frames | image model at the delivery aspect ratio          | reference stills, one per look to hold                            |
| 5. Shots  | Seedance `model_run`, audio per the choice above  | `dry_run` first; `wait=false`; `jobs_wait` with `pending_job_ids` |
| 6. Cut    | `python3 scripts/build.py edit.json out.mp4`      | one ffmpeg pass: conform, concatenate, lay the master, verify     |

Ask once before starting: team and project, track clearance, aspect ratio and length, sound under the song or not, what must and must not appear, spend ceiling. With no one to answer, take the song alone, and write the story down rather than waiting to show it. Then run without stopping.

## Worked example: one verse, three shots

1. `python3 scripts/song.py master.mp3 -o song.json`. Sections are shot boundaries, cut candidates are cut points; listen before trusting them.
2. Upload the master: multipart `upload_asset`, then `upload_asset_complete` (see the `scenario` skill). `recommend` a transcription model (the need in the user's own words as `prompt`), `model_schema_get`, `model_run`, `jobs_wait`. The transcript is a text asset among the job's asset ids: `asset_get` returns it whole in `metadata.preview` when `hasFullPreview` is true (at authoring time the Whisper-based tool wrote SRT-style timed blocks), else `asset_download` fetches the file. Instrumental track: say so and move on.
3. Write one page: what happens, where, how it turns across the sections; name the closing image. Show it to the user before spending anything.
4. Generate reference stills with an image model (via `recommend`) at the delivery aspect ratio, one per look. Look at them: they set identity and palette downstream. Holding one character across several: see the `scenario-consistency` skill.
5. Per shot, decide the conditioning: opening state matters, pass a first-frame `image`; only identity and world matter, pass `referenceImages` (see [references/shots.md](references/shots.md)). Generate each shot one or two seconds longer than its slot for a trim handle. To land an action on a beat inside a shot, timecode it from the clip's start: the beat's master time minus the shot's `at`, plus any head trim planned as `in` (an unplanned trim moves every beat). Hold one camera move and one location across the timecodes; timecoded verbs survive generation where mood words do not.
6. Write `edit.json` and run `python3 scripts/build.py edit.json out.mp4`:

```json
{
  "master": "master.mp3",
  "fps": 24,
  "width": 1280,
  "height": 720,
  "sound": 0.2,
  "shots": [
    { "clip": "clips/01.mp4", "at": 0.0 },
    { "clip": "clips/02.mp4", "at": 12.5, "in": 1.0 }
  ]
}
```

Each shot runs until the next starts and the last to the master's end, so gaps are impossible, and every `at` snaps to the nearest frame. `in` is an optional head trim. `sound` is the gain on the clips' own audio: 0.1 to 0.3 under a mastered track, up to 1.0 when the clips run quiet (build.py takes 0 to 4); drop the line for the song alone. The build fails loudly on a clip too short, a mix that would clip, or delivered audio that is not the master.

## Common mistakes

- Letting a shot score itself: its score restarts at every cut.
- Turning `sound` on while the prompts still allow music: exclude it in words, since `generateAudio` is one switch over the whole track.
- Trimming, normalizing, fading, or re-encoding the master yourself: build.py copies it or carries it at unity, and hash-checks the file either way.
- Trusting a requested aspect ratio: stills and clips land near it, not on it, and build.py pads the difference; crop to the delivery ratio first.
- Prompting an opening state in reference mode: it will not appear; pass a first-frame `image`.
- Judging a clip from a sparse contact sheet: a continuous camera move looks like a hard cut; measure first (see [references/shots.md](references/shots.md)).
- Trusting the beat grid: sections and cut candidates are suggestions; check them against what you hear.
- Calling it done without watching the delivery with sound, then muted.
