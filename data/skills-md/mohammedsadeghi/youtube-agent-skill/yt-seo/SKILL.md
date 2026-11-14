---
name: yt-seo
description: >-
  Write the description, tags and search-facing text for a YouTube video,
  aimed at the query a real person types. Use for "write my description",
  "tags", "SEO", "help this video get found", "nobody is finding this".
---

# yt-seo

Search is a smaller lever than packaging and a bigger one than people think for evergreen videos.
For a video aimed at the subscriber feed, say so and spend the effort on `yt-package` instead.

## Before you write

1. Look for `youtube-voice.md` in the current project, then
   `~/.youtube-agent-skill/voice.md`. If neither is readable, ask for a sample or voice
   preferences. Do not create or update a profile unless the user asks.
2. Never invent a number, a result or a source. If a figure would strengthen it and you do not have
   one, ask for it or write the line without it.

## The description

- **The first two lines are the only ones anyone reads.** They show above "...more" and they are
  the search snippet. Say what the video gives them, in the words they would have typed.
- Then the link or the resource, if there is one, so it is above the fold.
- Then chapters. Use `yt-chapters` if it is installed and a transcript is available.
- Then the long version: what is covered, who it is for, what it assumes.

## Tags, honestly

YouTube says tags are mainly useful for common misspellings and otherwise play a minimal role in
discovery. Use relevant spellings or alternate names when they help. Do not add tags to the
description or use unrelated tags. See [YouTube's tags guidance](https://support.google.com/youtube/answer/146402?hl=en).

## The query test

Before handing anything over, write the three search queries this video should win, and check the
title and first two description lines contain the words in those queries. If they do not, the
problem is the title, not the description.

## The gate

Nothing here publishes. This skill writes and you publish. Every output ends in a block the user
copies, and the last line of every run is the question: **ship it, or change it?**
