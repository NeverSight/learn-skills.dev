---
name: youtube-skill
description: >-
  YouTube skill: get a finished video found on YouTube, then upload it. Transcribes it (free
  local faster-whisper, your own Groq or OpenAI key, or an existing SRT/VTT), finds the phrases
  people actually type into YouTube search (free autocomplete, optional free YouTube Data API
  key), writes 10 titles, a description whose first lines work in search, chapters, tags and
  hashtags, checks every field against YouTube's limits, renders thumbnail options from the
  video's own frames and previews them at feed size, writes clean captions, then uploads to
  YouTube with WoopSocial after you say yes, plus a YouTube Studio checklist. Works on Mac, Windows and Linux with ffmpeg and Pillow; no paid API required. Use
  when someone says "upload to youtube," "youtube seo," "youtube title," "youtube description,"
  "youtube tags," "youtube chapters," "youtube thumbnail," "publish my video," or "youtube with
  Claude Code." Never promises what the video doesn't deliver, confirms before anything posts.
  Standalone: needs no other skills.
metadata:
  version: 1.0.0
license: MIT
---

# YouTube Skill

Most videos are found or lost in the first second someone sees them: a thumbnail and a title in
a feed, a line of description in search. Most uploads waste that: a filename for a title, an
empty description, no chapters, a random frame as the thumbnail. This skill does the publishing
work a good channel manager does: it finds what people search, writes and checks every field,
makes thumbnails from the video and shows them at the size viewers see them, uploads after a
yes, and reads the results. Everything it needs is in this folder.

Four commitments:

1. **The package matches the video.** No title, thumbnail or claim the video doesn't deliver.
   Misleading packaging breaks YouTube's spam and deceptive practices policy, and viewers who
   feel tricked leave in seconds, which ranks the video down.
2. **Search words come from searches,** not guesses: autocomplete, the user's own audience, the
   transcript.
3. **Nothing posts without a yes.**
4. **Only the user's own video,** or one they have the rights to.

On Windows use `py` instead of `python3` in every command.

## Step 0: Setup and the questions

Run `python3 scripts/check_setup.py`: it reports ffmpeg, Pillow, transcription routes and OpenCV
with the install command for the user's system. Required: ffmpeg and Pillow.

Ask, in one message, only what you can't see:

1. Which file is the final video, and is it theirs?
2. The channel: what it's about and who watches (one specific viewer).
3. Is the video **made for kids**? A legal setting (COPPA); never guess it.
4. Does it show **realistic AI-made or AI-altered** people, places or events? Then YouTube
   requires the "AI use" label.
5. When to publish (and their timezone), and whether to upload unlisted first.
6. Optional: a phrase they want to be found for, links for the description, the channel name
   for the preview, a free YouTube Data API key for a look at the top results.

## Step 1: Transcribe

```bash
python3 scripts/transcribe.py final.mp4 --out work/ --terms "Names, Product, Jargon"
```

Three routes: `--from captions.srt` (an existing caption file: free, instant), `GROQ_API_KEY` or
`OPENAI_API_KEY` (fast, a few cents per hour), or local faster-whisper (free, private, slower).
For a video that isn't in English, add `--language` with its code (`nl`, `de`, `es`...).
Read `work/transcript.txt` once, all of it. Everything below is written from it.

## Step 2: Find the search phrase

```bash
python3 scripts/suggest.py "topic in 2 to 4 words" --out pack/
```

It lists what people type into YouTube search for the topic and its question forms (how, why,
what is...). `--deep` adds the topic followed by every letter. It reads YouTube's public autocomplete, which
has no official API: run it a few times per video, never in a loop. For another language or
country, add `--lang nl --country nl`. With the user's own
`YOUTUBE_API_KEY`, `--top` lists the 10 videos ranking now with views and views per day.

Pick **one main phrase**: the most specific suggestion the video fully answers. "is saturn
losing its rings in 2025" beats "saturn" (too broad to rank) and beats a phrase the video only
touches. Note 2 to 4 related phrases for the description. If nothing comes back (a new topic,
offline), use the words the speaker uses for it in the transcript.

## Step 3: Write the package

Rules and the reasons behind them: `references/youtube-seo.md`. Write `upload.json` (format at the
top of `scripts/youtube_pack.py`):

- **10 titles,** then pick with the user. The main phrase early (titles are cut at about 40
  characters on phones and 70 elsewhere), a reason to click that the video pays off: a
  question it answers, a number, a result, a tension. Under 70 characters. Sentence case or
  title case, never all caps. Keep the best 2 runners-up: Test & Compare can A/B test up to 3
  titles.
- **Description:** the first two lines (`top`) are what shows under the video and in search:
  what the viewer gets, with the main phrase, in plain words. Then a short paragraph with the
  related phrases where they fit naturally, the chapters, links with what each one is, and 3
  hashtags (YouTube shows up to three above the title).
- **Chapters** (videos over about 3 minutes; the pack reminds you past 4): 3 to 10, from the topic changes in the
  transcript, first at 0:00, each at least 10 seconds, named for what the viewer gets ("Why the
  rings vanish", not "Part 2"). Chapter names are searchable; use the related phrases where
  they're true.
- **Tags:** 5 to 10, specific: the main phrase, its spelling variants, names. YouTube says tags
  matter little; they help mostly with misspellings.
- **Category, made for kids, privacy, schedule,** and `replace` for words the transcriber got
  wrong (names especially).
- **Pinned comment:** a question viewers want to answer, or the link people will ask for.

Then build and check the pack:

```bash
python3 scripts/youtube_pack.py build upload.json --transcript work/transcript.json --out pack/
```

It checks the title (length, capitals, the phrase), the description (5,000-byte limit, the phrase
in the first 150 characters, hashtags), tags (500 characters as YouTube counts them), chapters
(0:00, 3 or more, 10 seconds each; starts snapped to the sentence they fall in), and writes
`description.txt`, `captions.srt`, `post.json`, `manifest.json` and `upload-pack.md`. **Fix every
warning.**

## Step 4: Thumbnails

```bash
python3 scripts/youtube_pack.py frames final.mp4 --out pack/
```

`pack/frames.jpg` shows 12 candidate frames: sharp, well lit, varied, faces scored when OpenCV is
installed. Look at it and choose 2 or 3 frames that show the video's promise: a face with a clear
expression, the object or result the title is about, a before and after. Then write
`thumbs.json` (format at the top of `scripts/thumbnail.py`) and render:

```bash
python3 scripts/thumbnail.py thumbs.json --out pack/
```

- **2 to 5 words** that add to the title instead of repeating it. Title: "Is Saturn Losing Its
  Rings in 2025?"; thumbnail: "Gone by March?".
- Layouts: `side` (big white words on a dark fade), `box` (dark words on coloured bars), `none`
  (picture only; strong when the image says it all). `zoom` and `focus` crop in on the subject.
- Make the options different ideas (a face vs the object, words vs none), not three crops of
  the same frame; that's what makes a Test & Compare result mean something.
- Thumbnails come out at the source's size up to 3840x2160 (YouTube's recommendation) and under
  2 MB, so they upload from a phone as well as a computer. Keep the bottom-right corner clear:
  the duration badge sits there.

**Judge them in `pack/preview.png`**, which shows every option as a home-feed card and as a
small phone-sized card with the title. Reject an option if the words can't be read in the small
card, the subject is unclear at that size, or it promises something the video doesn't show.
Never use a face, logo or image the user has no rights to.

## Step 5: Upload with WoopSocial

How to connect, upload and post: `references/woopsocial.md`. Short version:

1. `social_accounts_list`; not connected: the one connect path for this agent (free plan: 2
   social accounts), then `oauth_create_authorization` for YouTube.
2. Upload the video with an upload session (`media_uploads_create_session` with `bytes` from
   `pack/manifest.json`, `python3 scripts/upload_parts.py session.json final.mp4`,
   `media_uploads_complete_session`).
3. Fill the IDs into `pack/post.json` and run `posts_validate`.
4. Show the user `upload-pack.md` (title, the description's first lines, chapters, tags, made for
   kids, privacy, time with timezone) and `preview.png`. Get a clear yes. Then `posts_create` and
   `posts_get`.

## Step 6: Finish in YouTube Studio

WoopSocial can't set these; `upload-pack.md` ends with the list for the user:

- **Thumbnail:** upload the chosen one (the channel must be verified), or test up to 3
  thumbnails and titles in Test & Compare (desktop Studio, not for made-for-kids videos).
- **Captions:** upload `captions.srt` (Subtitles > Upload file > With timing).
- **AI use** set to Yes when step 0 said yes.
- **End screen, cards and playlist.**
- **Pin the comment.**

Uploaded unlisted? It goes public after these are done.

## Step 7: Read the results

After 2 days and after 7 days: views and likes with `social_account_posts_list` (with the
collection date; missing means "not reported"). Ask the user for impressions, click-through rate
and average view duration from YouTube Studio. Judge against the channel's own recent videos:

| Click-through | Viewers stay | What to do |
|---|---|---|
| Low | Fine | The package undersells the video: test another thumbnail first, then the title |
| Fine | Low | The opening loses them: the next video gets to the point in the first 30 seconds |
| Low | Low | Rethink the topic or angle before the packaging |
| Fine | Fine | Make the next video on a neighbouring search phrase |

Log each video in `videos.md`: date, phrase, title, thumbnail, CTR, average view duration, views
at 7 days. Never estimate a number the user didn't give.

## Shorts

Vertical or square videos up to 3 minutes are Shorts. The pack spots them: no chapters, a short
title with the phrase, no `#shorts` needed. `thumbnail.py` renders 9:16 thumbnails for a
vertical video (a 16:9 one would be replaced by YouTube), with the words in the upper part, clear
of the title and buttons, and previews them as Shorts-shelf cards. A custom Shorts thumbnail is
added in Studio on a computer; Test & Compare doesn't run on Shorts.

## Quality bar

Before showing anything, ask: would a top channel manager in this niche publish it? Reject it if:

- the title or thumbnail promises more than the video delivers;
- the title would fit any video on the topic;
- the thumbnail words repeat the title, or can't be read in the small card;
- the description's first line is "In this video..." or a list of keywords;
- a chapter is named "Part 2" or starts mid-sentence.

## Edge cases

- **No speech** (music, b-roll): skip the transcript; chapters from the user, no captions.
- **Several languages:** write the package in the video's language; translated titles and
  descriptions are added in Studio.
- **Re-uploading a deleted or old video:** new title and thumbnail; identical re-uploads look
  like spam.
- **Many videos at once:** one pack each, written from each video's own transcript; stagger the
  times. YouTube's Spam Policy bans using automated tools "to churn out high volumes of similar
  content with minimal changes"; say no to near-identical uploads.
- **The user wants clickbait:** offer the strongest honest version; explain the drop-off cost.

## References

- `references/youtube-seo.md`: limits, how search and recommendations work, title, description,
  chapter, tag, thumbnail and Shorts rules, with sources and dates.
- `references/woopsocial.md`: connect, upload, post and read results.
