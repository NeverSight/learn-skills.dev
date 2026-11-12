---
name: channel-analysis
description: Use when the user wants to analyze a YouTube channel for its positioning, what works, what holds it back, and what to change first. Requires the TubeLab MCP.
license: MIT
metadata:
  author: tubelab
  version: "5.0"
  requires: tubelab-mcp
---

# Channel Analysis

## Overview

A channel's median views show what a typical video gets. Its last few uploads show how it is doing now. Comparing the two tells you whether the channel is healthy, growing or declining. A format that gets fewer views each time it returns is worn out: keep what makes it work, and change what the title promises. A hit the channel never followed up is its cheapest opportunity.

## Workflow

1. Clarify scope only if needed. Unless told otherwise, the goal is reach, or conversion if the channel sells something.
2. Compare the last 4 to 6 long-form uploads with the median.
3. Fetch and view the thumbnail of every video you feature. If one fails to load, say so.
4. Check what works now for the same audience. Two or three searches are enough.

## Output Format

```markdown
# 📊 Channel Analysis: [{channel}]({url})

- **Diagnosis:** {one sentence, with numbers}
- **Positioning:** {who it serves and what it promises}

## ✅ What Works

### 1. {Finding}

[![]({thumbnail})]({video url})

- [{title}]({video url}) · {views, ratio, date}
- **Why:** {one sentence}

## ⚠️ What Holds It Back
1. **{Problem}**
   - [{title}]({video url}) · {views, ratio, date}
   - **Fix:** {one sentence}

## 🧪 Next 3 Tests
1. **{Title to test}**
   - **Based on:** [{channel}]({url}) · [{title}]({video url})
   - **Pass if:** {views by day 30}
```

- Length: about 600 words. Three items per section.
- Language: plain words and short, complete sentences. Nothing compressed.
- Bullets: one fact each, under 25 words, except quotes and verbatim titles. No extra sections or bullets.
- If it runs long, cut whole items. Never cut proof, and never squeeze sentences.
- Links: link every video, channel, moment, brand and offer you cite, built from IDs, handles and links in the data. Never guess one.
- Thumbnails: use the 320px `mqdefault.jpg` image, on its own line under the heading, linked to the video.

## Common Pitfalls

- Do not search without `publishedAtFrom` and `classificationQuality` at `"neutral"` or above, or the results fill with low-effort videos.
- Do not call fewer views a problem by itself. A healthy channel is a valid result.
- Do not read a ratio of 1.0 as typical. Big hits pull the channel's mean up, so a median video sits below 1.0.
- Do not judge uploads that are still gathering views, and do not mix in Shorts.
- Do not state a cause as fact. Say what the evidence suggests.
