---
name: video-to-shorts-skill
description: >-
  Video to shorts skill: turn a long video (podcast, interview, talk, webinar, stream, YouTube
  video) into vertical short clips for TikTok, Instagram Reels and YouTube Shorts, then post them
  to one or many accounts with WoopSocial. Transcribes with word timestamps (free local
  faster-whisper, your own Groq or OpenAI key, or an existing SRT/VTT), scores every candidate
  moment with a clip rubric (hook, standalone, payoff), cuts 1080x1920 clips with ffmpeg,
  removes pauses, keeps the speaker in frame, burns word-by-word captions and a hook line,
  normalises the audio, and writes titles and captions. Works on Mac, Windows and Linux with
  ffmpeg and Pillow; no paid API required. Use when someone says "video to shorts," "clip my
  podcast," "turn this video into shorts," "make reels from my video," "podcast clips," "long
  video to short clips," or "repurpose my YouTube video." Clips only what the user owns or has
  permission to use, confirms before anything posts. Standalone: needs no other skills.
metadata:
  version: 1.0.0
license: MIT
---

# Video to Shorts Skill

One long video holds a week of short clips, if you pick the right moments. Most clips fail for the
same reasons: they open on "so, like I was saying", they need the rest of the episode to make
sense, they end before the point lands, the captions sit under TikTok's buttons, or the speaker
is cut out of the frame.

This skill does the whole job: transcribe, find and score the moments, cut them vertical with
captions, show the user, post through WoopSocial after a yes, and read the results back.
Everything it needs is in this folder.

Four commitments:

1. **Only footage the user may use.** Their own video, or someone else's with permission. Ask.
2. **Moments that stand alone.** A stranger must understand the clip with no context.
3. **Nothing posts without a yes.** Show the clips, titles, captions, accounts and times first.
4. **No invented claims.** Titles and captions say what the clip says; no made-up quotes or numbers.

## Step 0: Setup and the source

Run `python3 scripts/check_setup.py` (on Windows use `py` instead of `python3` in every command). It reports ffmpeg, Pillow, transcription routes and
OpenCV, with the install command for the user's system. Required: ffmpeg and Pillow.

Then ask, in one message, only what you can't see:

1. Which video (a file path; for a YouTube video they own, the file from YouTube Studio).
2. **Is it theirs, or do they have permission?** Clips of someone else's content need the owner's
   OK or a clipping program's brief, plus a credit line. No permission: stop.
3. Who it's for and which accounts post (TikTok, Instagram, YouTube, how many each).
4. Do they have a transcript (an .srt or .vtt from YouTube Studio or their podcast host)?
5. Brand colour for the highlighted caption word, and anything that must not be clipped.

## Step 1: Transcribe

```bash
python3 scripts/transcribe.py VIDEO --out work/
```

Routes, best first. Explain the trade-off once and use what the user has:

| Route | How | Cost and speed |
|---|---|---|
| Existing transcript | `--from captions.srt` | Free, instant; word timing is estimated, so captions are a little less tight |
| Groq | `GROQ_API_KEY` set | About $0.04 per hour of audio, a minute or two per hour; audio goes to Groq |
| OpenAI | `OPENAI_API_KEY` set | whisper-1, which OpenAI plans to retire in February 2027 |
| Local | `pip install faster-whisper` | Free and private; on a laptop roughly half to one times the video length with `--model small`, faster with `--model base` |

It writes `work/transcript.txt` (one timestamped line per sentence) and `work/transcript.json`
(every word with timings).

## Step 2: Find and score the moments

Read the whole `transcript.txt`. List 8 to 12 candidates and score each with the rubric in
`references/clip-rubric.md`. In short:

- **Hard gates** (fail one and it's out): the first sentence makes sense with no context; one
  complete idea; no intro, outro, sponsor read or crosstalk; no music that isn't theirs.
- **Score out of 100:** hook in the first 3 seconds (25), stands alone (20), payoff or turn (20),
  emotion or energy (15), specifics like numbers, names, a story (10), strong last line (10).
- **Ship 70 and up**, review 55 to 69, drop the rest.
- **Length:** 25 to 45 seconds by default, 60 at most; up to 90 only for a story scoring 85+.
  Keep clips with any third-party audio or footage at 60 seconds or less (YouTube blocks longer
  Shorts with a Content ID claim).
- **Spread:** no overlaps, clips from across the video, one per sub-topic.

Every clip starts on the first word of a sentence or of a clause that stands alone, and ends on
the last word of a sentence. Skip the warm-up ("I think one of the things..."); end before the
trailing "so yeah". Read the words just before your start and just after your end in
`transcript.json`. The script fixes small slips and warns about the rest; when a clip starts on a
clause on purpose ("if folks have seen Groundhog Day..."), set `"snap": false`. Inside a clip, list
rambles and fillers like "kind of" in `"cut": [[start, end], ...]`.

Default 25 to 45 seconds. Over 45 needs a score of 85+ and a turn around 15 and 30 seconds; name
those lines. Show the user a table (start, end, length, hook line, score, why) and let them pick,
usually 3 to 5.

For each pick write:

- **hook:** 3 to 8 words on screen for the first 3.5 seconds, the clip's promise in plain words.
  It must not repeat words the speaker says in the first 10 seconds.
- **title:** for YouTube Shorts, under 70 characters, main search words first.
- **caption:** for TikTok and Reels: the search phrase first, one line of context, a question or
  reason to follow, 3 to 5 specific hashtags. Credit the speaker if it isn't the user.

## Step 3: Check the framing, then render

Write `clips.json` (format at the top of `scripts/make_shorts.py`, example in
`examples/nasa-interview/clips.json`), then preview the crop:

```bash
python3 scripts/make_shorts.py clips.json --transcript work/transcript.json --out shorts/ --preview
```

**Open every `preview-XX.jpg`.** Each shows three frames with the planned vertical crop. If the
box misses the speaker, set `focus_x` (0 = left edge, 1 = right edge) on that clip; for two
people far apart, a screen share or a wide shot, set `"reframe": "fit"` (whole frame on a blurred
background). With OpenCV installed the script finds one speaker on its own, but still look.

Then render:

```bash
python3 scripts/make_shorts.py clips.json --transcript work/transcript.json --out shorts/
```

Each clip comes out 1080x1920 H.264 with AAC at -14 LUFS; pauses over 0.45 seconds removed,
including silences the transcriber hides inside long words; stutters, "um", "uh" and "you know,"
cut; a slight punch-in at every cut so jump cuts look intended; word-by-word captions inside the
area no platform covers; and the hook on a white box for the first 3.5 seconds.
Rendering takes about as long as the clips themselves; `--best` is slower and slightly smaller.
Details: `references/shorts-specs.md`.

**Watch the first 5 seconds of every clip and open `contact-sheet.jpg`.** Fix and re-render
(`--only 02`) when: the clip opens mid-thought, a caption hides the face, the hook and the first
words say the same thing, or the end trails off. Read the first caption group aloud: if a stranger
wouldn't understand it, the start is wrong. Resolve every warning in `manifest.json`.

## Step 4: Post with WoopSocial

How to connect, upload and post: `references/woopsocial.md`. Short version:

1. **Check the connection** with `social_accounts_list`. Not connected: give the one connect
   path for the agent you're running in (free plan: 2 social accounts), then
   `oauth_create_authorization` per platform.
2. **Upload each clip** with an upload session (`media_uploads_create_session` with the byte size
   from `shorts/manifest.json`, `python3 scripts/upload_parts.py session.json shorts/clip-01.mp4`,
   `media_uploads_complete_session`). Clips over 10 MB upload in several parts; the script
   handles that.
3. **One post per clip per platform:** TikTok `postType: VIDEO`, Instagram `postType: REEL`,
   YouTube with `title` and `privacy`, Facebook `postType: REEL`. Run `posts_validate`.
4. **Show the plan** as one table (clip, platform, account, title or caption, time with timezone)
   and get a clear yes. Then `posts_create` and confirm each with `posts_get`.

Several accounts: never the same clip at the same time everywhere. Give each account its own clips
or at least its own hook and caption, and stagger the times with `SCHEDULE_FOR_LATER`.

## Step 5: Read the results

After 3 to 7 days, read `social_account_posts_list` (views, likes, comments, shares, saves where
the platform reports them, with the collection date; missing means "not reported", not zero).
Keep `clips-log.md`: source video, timestamps, hook, length, platform, numbers. Then:

- Clips that beat the account's usual numbers: clip more from the same part of the video, same
  kind of moment.
- Views but no follows: stronger last line or a reason to follow in the caption.
- Weak first 3 seconds (fast drop): start later, on the punchline, with a sharper hook.

Never estimate numbers the platform didn't report.

## Quality bar

Before showing anything: would a top clipping editor post this? Reject a clip that needs context,
opens on a warm-up, cuts off the speaker, hides the face behind text, or ends mid-thought.

## Edge cases

- **No speech in a part** (music, b-roll): the transcript has gaps; don't clip across them.
- **Two speakers far apart:** `fit`, or two separate clips each on one speaker.
- **720p or smaller source:** a face crop gets soft. Prefer `fit`, or warn the user.
- **Not English:** transcription detects the language; write hooks and captions in that language.
- **No permission for the footage:** stop and say why.
- **Over 3 minutes:** YouTube Shorts and TikTok's API cap is 3 minutes; split it.

## References

- `references/clip-rubric.md`: gates, scoring, lengths, opening and ending rules, examples.
- `references/shorts-specs.md`: frame, caption and audio specs, safe areas, encode settings,
  platform rules for reused content.
- `references/woopsocial.md`: connect, upload, post and read results.
