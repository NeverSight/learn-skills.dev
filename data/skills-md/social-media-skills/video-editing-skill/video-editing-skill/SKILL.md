---
name: video-editing-skill
description: >-
  Video editing skill: edit a talking-head video (YouTube video, course lesson, product demo,
  podcast on camera, vlog) the way an editor would. Transcribes with word timestamps (free local
  faster-whisper, your own Groq or OpenAI key, or an existing SRT/VTT), removes silences, "um"s
  and "uh"s, stutters and retakes (keeps the last take), adds jump-cut punch-ins, cleans and
  levels the audio, writes an SRT caption file and YouTube chapters, optionally burns captions
  or makes a vertical version, shows a cut list to approve before rendering, then posts to
  YouTube and other platforms with WoopSocial after you say yes. Works on Mac, Windows and
  Linux with ffmpeg and Pillow; no paid API required. Use when someone says "edit my video,"
  "remove silences," "cut the ums," "remove filler words," "jump cut my video," "clean up this
  recording," "edit this talking head video," or "video editing with Claude Code." Never cuts
  what the user marked to keep, confirms before anything posts. Standalone: needs no other skills.
metadata:
  version: 1.0.0
license: MIT
---

# Video Editing Skill

A raw talking-head recording is usually 20 to 40% dead air: pauses, "um"s, false starts, the
sentence said twice. Cutting that by hand takes longer than recording. This skill does the first
edit: it reads the transcript, plans every cut with a reason, shows the plan, renders the edit
with punch-ins on the jump cuts and clean audio, writes captions and chapters, and posts after a
yes. Everything it needs is in this folder.

Four commitments:

1. **The user's words stay.** Only pauses, fillers, stutters, retakes and ranges the user approves
   go. Meaning is never edited.
2. **Plan before render.** The cut list is shown and approved first.
3. **Nothing posts without a yes.**
4. **Only footage the user may use.** Their own recording, or with permission.

On Windows use `py` instead of `python3` in every command.

## Step 0: Setup and the source

Run `python3 scripts/check_setup.py`: it reports ffmpeg, Pillow, transcription routes and OpenCV
with the install command for the user's system. Required: ffmpeg and Pillow.

Ask, in one message, only what you can't see:

1. Which file, and is it theirs?
2. Where it's going: YouTube (16:9), social (vertical), or both.
3. How tight: **youtube** (the default: pauses over 0.5 s cut, natural beats kept), **tight**
   (0.3 s, fast YouTube and social) or **podcast** (gentle, no punch-ins).
4. Words they use as habits that are safe to cut ("like", "so", "you know", "basically"). These
   carry meaning in other sentences, so they're opt-in.
5. Anything that must stay as it is (a demo, a joke with a pause, a sponsor read).

## Step 1: Transcribe

```bash
python3 scripts/transcribe.py VIDEO --out work/ --terms "Product name, Jargon, Guest name"
```

`--terms` lists names and jargon so they're spelled right; fix whatever is still misheard with
`"replace"` in edit.json before rendering, because captions burned into a posted video can't be
corrected.

The same three routes as always, with the trade-off explained once:

| Route | How | Cost and speed |
|---|---|---|
| Existing transcript | `--from captions.srt` | Free, instant; word timing estimated and most "um"s missing, so filler cutting is weaker |
| Groq or OpenAI | `GROQ_API_KEY` or `OPENAI_API_KEY` | Groq about $0.04 per hour of audio, a minute or two per hour |
| Local | `pip install faster-whisper` | Free and private; roughly half to one times the video length with `--model small` |

The transcriber is prompted to write fillers down; Whisper drops them otherwise. Sounds it still
misses (an "mm" nobody wrote down, a breath) are found in the audio itself by the editor.

## Step 2: Plan the edit

Read `work/transcript.txt` once, all of it. Then write `edit.json` (format at the top of
`scripts/edit_video.py`):

- **Style:** `"style": "youtube"`, `"tight"` or `"podcast"` (thresholds in
  `references/editing-rules.md`). Pauses over the limit shrink to a natural beat: shorter
  mid-sentence, longer after a sentence, longest at a topic change.
- **Fillers:** the default list ("um", "uh", "er", "hmm", "mm") is safe. Add the user's habit
  words to `extra_fillers` only when they asked.
- **Tangents and dead sections:** a tangent, a "can you hear me?", a long set-up before the
  point. Add them to `cut` with a reason, and tell the user.
- **Protect** anything that must stay with `keep`, including silent stretches.
- **Interviews with question cards or a visible interviewer:** keep the questions (about 3
  seconds of each card in `keep`) unless the user says otherwise; without them every answer
  starts with "So..." and no context.
- **Misheard names:** `"replace": {"Cyrus Rex": "OSIRIS-REx"}`.
- **Chapters** (for YouTube): 3 to 10 chapters from the topic changes, first at 0:00, each at
  least 10 seconds, named for what the viewer gets ("Why the camera failed", not "Part 2").
  Times in the original video; the script moves them.

Then make the plan:

```bash
python3 scripts/edit_video.py edit.json --transcript work/transcript.json --out edited/ --plan
```

`edited/edit-plan.md` gives the new length, how much came from inside the talking versus long
gaps and cards, the pace in words per minute, and every removal over a second with its reason
and words. **Read every retake and stutter line**, and the "possible retakes" list: two finished
sentences that start the same way are never cut automatically; decide each one and add it to
`cut` if it's a real retake. Show the user the summary, the retakes, the tangents you chose and
the chapters, and get a yes.

## Step 3: Render

```bash
python3 scripts/edit_video.py edit.json --transcript work/transcript.json --out edited/
```

What it does:

- Cuts pauses over the limit down to a natural beat, plus fillers, stutters, retakes and every
  `cut` range. Removals shorter than the style's minimum (0.4 s in youtube) are left alone: a
  jump cut costs more than it saves.
- Places every cut by listening: word edges move to where the sound actually stops and starts,
  so word endings aren't clipped, and sounds the transcript missed (an unwritten "mm") are found.
- Looks at the picture too: title cards and shot changes are cut cleanly, never leaving a
  few frames of a card.
- Renders in groups of pieces in one pass each, so sound and picture stay in sync however many
  cuts there are.
- **Punch-ins:** switches between the full frame and a 1.1x punch-in where a jump cut needs
  hiding: always at a cut that removed a second or more, otherwise only after 4 seconds on the
  same framing, never at a cut onto a new camera shot. `"punch_in": 0` turns it off.
- **Audio:** gain to a working level, rumble filter, noise reduction set from the measured room
  noise (skipped when the room is already quiet), gentle compression, a peak limiter, and a
  two-pass loudness pass to -14 LUFS.
- **Captions:** always writes `captions.srt` (2 lines of 42 characters at most, 1 to 7 seconds
  each, no line break after a small word or inside a name) for uploading to YouTube.
  `"captions": {"burn": true}` draws them into the video for social, where many people watch
  muted; vertical versions burn them by default. Don't burn captions into a YouTube video that
  also gets the SRT: viewers with captions on would see both.
- **Vertical:** `"format": "vertical"` makes a 1080x1920 version cropped on `focus_x`.

It writes `edited/edited.mp4`, `captions.srt`, `chapters.txt`, `edit-report.md` and
`manifest.json`.

**Check before showing the user:** open `cuts.jpg` (frames just before and after the biggest
cuts: look for flashes of a card, a jump in a different shot, a frozen expression) and read the
warnings in `manifest.json` (sync, pace over 190 words per minute, loudness). Fix and re-render
when a retake kept the wrong take, the pace feels breathless (a gentler style), or a cut lands
badly (`keep` that spot).

## Step 4: Post with WoopSocial

How to connect, upload and post: `references/woopsocial.md`. Short version:

1. `social_accounts_list`; not connected: the one connect path for this agent (free plan: 2
   social accounts), then `oauth_create_authorization` per platform.
2. Upload `edited.mp4` with an upload session (`media_uploads_create_session` with the byte size
   from `manifest.json`, `python3 scripts/upload_parts.py session.json edited/edited.mp4`,
   `media_uploads_complete_session`).
3. **YouTube:** `title` (main search words first, under 70 characters), `privacy`, and a
   description that starts with one line on what the viewer gets, then the chapters from
   `chapters.txt`. Upload `captions.srt` in YouTube Studio afterwards (WoopSocial doesn't send
   caption files).
4. Show the post (file, title, description, account, time with timezone) and get a clear yes.
   Then `posts_create` and `posts_get`.

## Step 5: Read the results

After a week, `social_account_posts_list`: views, likes, comments where reported, with the
collection date; missing means "not reported". Retention and average view duration are in
YouTube Studio; ask the user for them. If viewers drop early, the next edit gets a tighter
opening; if they drop at a chapter, that section was too long.

## Quality bar

Would a professional editor hand this over? Reject it if a word is clipped, a cut lands
mid-breath with a pop, a punch-in changes every few seconds, the pace leaves no room to think, or
meaning changed.

## Edge cases

- **Two people on camera:** keep `format` at source; punch-ins still work on a wide shot.
- **Screen recording with a voice:** set `"punch_in": 0`.
- **Music under the voice:** silence detection sees music as sound; set `"voiced_gaps": false`.
- **Very long recordings (over an hour):** works, but render time is about the video's length;
  plan first, render once.
- **No speech for a stretch on purpose** (a demo): `keep` it.

## References

- `references/editing-rules.md`: thresholds, fillers, retake patterns, punch-ins, audio chain,
  captions and chapters, with sources.
- `references/woopsocial.md`: connect, upload, post and read results.
