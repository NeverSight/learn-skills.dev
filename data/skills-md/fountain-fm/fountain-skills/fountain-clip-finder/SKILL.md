---
name: fountain-clip-finder
description: Find the strongest clip moments in a show, write the post copy, and open a draft post for each channel.
---

## Overview

This skill searches a show's transcripts for the moments that could become a strong clip.
Four modules process the moments in order.
Module **discovery** scores the moments.
Module **media** resolves the file that each moment is cut from.
Module **boundaries** sets the span, and module **copy** writes the words around it.
For a video that Fountain does not hold, module **external-source** replaces the search.
Each clip becomes a draft post, so the user decides which clips are posted.

## Input

One of these:

- A topic, or the terms to search for.
- A kind of moment, for example funny, angry, or surprising.
- An episode, with an optional quote or approximate time.
- A person, to find the moments of one guest or host.
- One or more videos that the show never published as an episode, each a URL or a file on this
  machine, with an optional topic or quote.

Optional:

- `clip_count` - the maximum number of clips to return.
  The show's archive may hold fewer.
- `min_duration_seconds` and `max_duration_seconds` - the length range of a clip.
- A link that every post MUST contain, for example the landing page of a campaign.
- Trend context with its sources, when the clip must answer a news story.
  This skill does not search the news, so the caller gives the sources.

## Output

One draft `SocialPost` for each clip on each connected `SocialChannel`.
The posts are ranked by the clip score of module **boundaries**.

A post targets one channel, and the platform of that channel sets the style of the text.
Thus one clip on two channels gives two posts, each with its own text.

This skill MUST write `source` when `media` is a URL.
A later renderer cuts the clip from `source`.
Module **copy** writes `meta.label`, `content.title`, `content.text`, and `context`.
Module **media** and module **boundaries** build `source` between them.

A Fountain episode source names its episode and show in `ids`.
A YouTube match for that episode adds its YouTube video id.
A standalone YouTube source names only its YouTube video id.
Another external URL uses empty `ids`.
Module **external-source** builds the last two forms.
A raw local path is not a URL, so its post holds no `source`.
Thus the render MUST happen in the same session.

The posts with `source` then wait in the Social API.
This skill does not start the next stage.
Skill **fountain-clip-producer** works from `source` and attaches the video to the post.
Skill **fountain-clip-producer** receives a raw local source directly in the same session.

## Housekeeping

You MUST read HOUSEKEEPING.md if you haven't already.

## Requirements

- Fountain API.
- A web search tool, for episodes that have no video on Fountain.
- Python 3.11 or later, yt-dlp for a video URL, and ffmpeg with whisper for a local video that has no
  subtitle file.
  Module **external-source** needs all three.
  A machine without them can run every other input.
- Skill **fountain-onboarding**.

## Process

Make the calls that do not need each other's answers at the same time.
A run loses time between its actions, and not inside them.

1. Resolve the show, and list the connected `SocialChannel` with the Social API.
   Run skill **fountain-onboarding** when the show has no channel.
   A clip becomes a draft post on a channel, and there is no other place to keep the work.
   Continue only when the user asks for the clips without a channel.
2. Run module **discovery** to search the transcripts, score each moment, and drop the weak ones.
   For a video that is not an episode, run module **external-source** first.
   Give its segments to module **discovery** as the passages to score.
3. Run module **media** to resolve the file that each moment is cut from, and the clock of that file.
   Drop a moment when its episode has no video to cut from.
   Skip this module for a video that is not an episode, because module **external-source** already named
   the file.
4. Run module **boundaries** to make each moment into a clip, and to drop the clips that fail a gate.
5. Run module **copy** to write `meta.label`, `content.title`, `content.text`, and `context`.
6. Create one draft `SocialPost` for each clip on each channel with the Social API.
   Give it the copy, and the complete `SocialPostMediaSource` when `media` is a URL.
   The clips do not depend on each other, so create them in batches of 4 to 6 at the same time.
7. Present each clip as one clip card of `assets/clip-card.md`, in rank order.
   End with the drafts link of the card.
   The card shows the score, the reason, and each flag, so do not put them in a summary above the cards.
   Give each raw local source to the renderer in this session.
   Say that these posts cannot be rendered from a later session.

## Additional notes

Each module removes work from the next one, so you MUST run them in the order above.
Inside a module, the order is less strict.
Where a step repeats one API call for many items, the items do not depend on each other.
Ask for them together, and not one at a time.

A clip from a video that is not an episode is about something that the audience cannot find on the feed.
Thus the words contain the link that the request gives, and the user approves the words and the link together.
An episode that is not published yet is the other case.
The clip is posted before the episode is published.
Thus the words MUST NOT say that the audience can hear the rest of the episode today.

`ts_start` and `ts_end` are always in the clock of the transcript.
A YouTube cut of an episode runs to its own clock, and skill **fountain-clip-producer** translates the
span into it at render time.
A video that is not an episode is its own transcript.
Thus the two clocks are the same, and nothing translates the span.

This skill never makes a video file.
It finds the moment, sets the span, and writes the words, and `source` holds all of that.

Give a few strong clips, and not many weak clips.
Say clearly when the show holds no strong clip.
