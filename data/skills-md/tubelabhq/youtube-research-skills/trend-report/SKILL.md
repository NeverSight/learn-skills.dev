---
name: trend-report
description: Use when the user wants to know what works now in a YouTube niche, why a video blew up, which hooks to copy, or a trend report. Requires the TubeLab MCP.
license: MIT
metadata:
  author: tubelab
  version: "5.0"
  requires: tubelab-mcp
---

# Trend Report

## Overview

A dated report on what is winning in a niche right now. Rank winners by ratio, because a video that beats its own channel's average says more than a big view count. A pattern needs three winners from different channels. To explain why one video blew up, compare it with its channel's normal videos.

## Workflow

1. Clarify scope only if needed. Default to the last month. If given a channel, use its own videos as the baseline for the top finding, not as winners.
2. Search for outliers. Keep at most 2 winners per channel. Two or three searches are enough.
3. Quote each top winner's opening from its transcript, word for word. If there is no transcript, give no hook. Fetch and view each winner's thumbnail, and say so if one fails to load.
4. Work out the winning patterns: the topics, the title formulas written with bracketed slots, how the hooks open, and the emotional triggers, each with what shows it.
5. If given a channel, say in one or two sentences what it should lean into and what to add, citing a winner. Then write about six video ideas, each with one line on what it does and a suggested opening line.

## Output Format

```markdown
# 📈 Trend Report: {niche or [channel](url)} · {date}

- **Top finding:** {one sentence, with numbers}
- **Sample:** {n} winners from {window}

## 🔥 Trending Videos

### 1. [{title}]({video url})

[![]({thumbnail})]({video url})

- [{channel}]({url}) · {date}
- **Views:** {views} | {ratio}X Outlier
- **Hook:** `{first sentence or two, word for word}`
- **Why it worked:** *{one short line}*

## 🔍 Winning Patterns
- **Topics:** {the winning topics, in one line}
- **Titles:**
  - `{formula with [SLOTS]}`
- **Hooks:** {how the hooks open, with the key moves in bold and short quoted phrases}
- **Triggers:** {trigger} ({what shows it}), {trigger} ({what shows it})
- **For your channel:** {what to lean into, citing a winner and its ratio, and what to add}

## 💡 Video Ideas Based on Research
1. **{Title}**
   - {what the video does, in one line}
   - Opening line: `{suggested first line}`
```

- Length: about 700 words. Five trending videos, three to five title formulas, about six ideas.
- Language: plain words and short, complete sentences. Nothing compressed.
- Bullets: one fact each, under 25 words, except quotes, verbatim titles and formulas. No extra sections or bullets.
- If it runs long, cut whole items. Never cut proof, and never squeeze sentences.
- Links: link every video, channel, moment, brand and offer you cite, built from IDs, handles and links in the data. Never guess one.
- Thumbnails: use the 320px `mqdefault.jpg` image, on its own line under the heading, linked to the video.

## Common Pitfalls

- Do not search without `publishedAtFrom` and `classificationQuality` at `"neutral"` or above, or the results fill with low-effort videos.
- Do not promise the user a small channel's multiple. It proves a format, not an expected result.
- Do not count videos for another audience or language, the user's sister channels, or paid placements (huge views, almost no likes) as winners. The language tag can call a Hindi or Urdu video English, so check the title and thumbnail.
- Do not copy a winner's title. Keep what made it work and change the topic.
