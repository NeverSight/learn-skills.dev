---
name: comment-mining
description: Use when the user wants to know what a YouTube audience asks, wants or complains about in the comments, in their own words. Requires the TubeLab MCP.
license: MIT
metadata:
  author: tubelab
  version: "5.0"
  requires: tubelab-mcp
---

# Comment Mining

## Overview

What the audience asks, objects to and wants next, in their own words. Likes are votes: a question with 900 likes is 900 people asking. Quotes stay word for word, and your reading of them goes on its own line.

## Workflow

1. Clarify scope only if needed. Default to 10 to 15 videos: the ones given, or else the channel's latest (its best if asked), or else a topic's top outliers. Finding videos by topic costs one search.
2. Fetch comments one video at a time, because parallel fetches overwrite each other. Remove spam, repeated rows and the creator's own replies.
3. Group the rest into questions, objections and requests, weighted by likes.

## Output Format

```markdown
# 🗣️ Voice of Audience: {channel, topic or videos}

- **Biggest ask:** {one sentence, with likes and number of videos}
- **Sample:** {n} videos, {n} comments

## 🧵 Themes
1. **{Theme}**
   - {n} videos · {total likes} likes
   - "{best quote}" · [{video}]({video url})
   - **What it means:** {one sentence}

| Comment (verbatim) | Type | Likes | Video (link) |
|---|---|---:|---|

## 💬 Their Words
- "{phrase}" · {n} times

## 💡 Video Ideas
1. **{Title}** · {the theme it answers}
```

- Length: about 700 words. Five themes, eight comments, three ideas.
- Language: plain words and short, complete sentences. Nothing compressed.
- Bullets: one fact each, under 25 words, except quotes and verbatim titles. No extra sections or bullets.
- If it runs long, cut whole items. Never cut quotes, and never squeeze sentences.
- Links: link every video, channel, moment, brand and offer you cite, built from IDs, handles and links in the data. Never guess one.

## Common Pitfalls

- Do not search without `publishedAtFrom` and `classificationQuality` at `"neutral"` or above, or the results fill with low-effort videos.
- Do not present a paraphrase as a quote.
- Do not call something a theme unless it appears under 3 or more videos. Under one video, it is a reaction to that video.
- Do not rank spam. Book promos and bots often collect many likes.
- Do not read a quiet comment section as a happy one. Top comments skew positive.
- Do not treat disabled comments as a finding. Say "no data".
