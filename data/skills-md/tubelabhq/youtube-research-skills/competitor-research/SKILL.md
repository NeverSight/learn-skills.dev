---
name: competitor-research
description: Use when the user wants to find a YouTube channel's real competitors, see how it compares, and find the gaps to win. Requires the TubeLab MCP.
license: MIT
metadata:
  author: tubelab
  version: "5.0"
  requires: tubelab-mcp
---

# Competitor Research

## Overview

Find the channels competing for the same viewers. A similar channel is not always a competitor. A competitor serves the same audience with an overlapping promise. The value is the gap: what competitors win with that this channel does not cover. Not for how they earn (`monetization-research`).

## Workflow

1. Clarify scope only if needed.
2. Build a set of 12 to 15 channels: direct competitors of similar size, a few larger leaders, and a few smaller channels growing fast. Start with the ones the user names and the ones you know.
3. Use searches to go further. Channels behind recent outliers in the niche are good, cheap candidates. For a large channel, skip the similar-channels search; outliers in the niche are the source.
4. Verify every channel with a free read, one at a time: topic, audience, language and size. Use medians over the last 90 days.
5. Fetch and view the thumbnail of each gap video. If one fails to load, say so.

## Output Format

```markdown
# ⚔️ Competitor Research: [{channel}]({url})

- **Biggest gap:** {one sentence, with numbers}

Medians cover the last 90 days. This channel's row is in bold.

| Channel (link) | Subs | Median views | Median per sub | Uploads, 90 days | Topics |
|---|---:|---:|---:|---:|---|

## 🎯 Gaps to Win

### 1. {Gap}

[![]({thumbnail})]({video url})

- [{channel}]({url}) · [{title}]({video url}) · {views, ratio, date}
- [{channel}]({url}) · [{title}]({video url}) · {views, ratio, date} (a second win, if found)
- **Why it fits:** {one sentence}

## 🧭 Moves
- **Copy:** {one sentence}
- **Avoid:** {one sentence}
- **Positioning:** {one sentence}
```

- Length: about 800 words. Every verified channel in the table, sorted by median per subscriber, with this channel's row in bold. About five gaps, each with up to two proofs.
- Language: plain words and short, complete sentences. Nothing compressed.
- Bullets: one fact each, under 25 words, except quotes and verbatim titles. No extra sections or bullets.
- If it runs long, cut whole items. Never cut proof, and never squeeze sentences.
- Links: link every video, channel, moment, brand and offer you cite, built from IDs, handles and links in the data. Never guess one.
- Thumbnails: use the 320px `mqdefault.jpg` image, on its own line under the heading, linked to the video.

## Common Pitfalls

- Do not search without `publishedAtFrom` and `classificationQuality` at `"neutral"` or above, or the results fill with low-effort videos.
- Do not keep a channel because a search returned it. Lookalikes are often tiny or off-topic, especially for large channels.
- Do not compare raw medians across channel sizes. Median per subscriber is fairer.
- Do not mix in Shorts.
- Do not build a gap on one lucky video. It should win more than once.
