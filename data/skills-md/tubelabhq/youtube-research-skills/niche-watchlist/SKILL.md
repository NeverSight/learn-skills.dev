---
name: niche-watchlist
description: Use when the user wants to monitor YouTube niches on a schedule and get a digest of new or breakout channels. Requires the TubeLab MCP.
license: MIT
metadata:
  author: tubelab
  version: "5.0"
  requires: tubelab-mcp
---

# Niche Watchlist

## Overview

Watch niches on a schedule and report only what changed since the last run. The two files below keep a fixed shape, so each run can be compared with the last one. For each new channel or mover, say what is worth learning from it.

## Workflow

1. Read `watchlist/config.json`. If it is missing, ask for 1 to 5 niches and write it.
2. Read `watchlist/state.json`. If it is missing, this run is a baseline, not a wave of breakouts.
3. Run each saved search once, exactly as saved. Compare only the channels it returns.
4. A new channel is one first seen since the last run. A mover is a known channel whose median views rose more than 50 percent over the stored value.
5. Read each new channel and mover, which is free. Look at its top videos by ratio, the topics it repeats and the title shapes it repeats. Fetch and view its best video's thumbnail, and say so if one fails to load.
6. Write `watchlist/<date>.md` on every run, then refresh the stored values.

`watchlist/config.json` (the saved search can hold other settings, such as a language):

```json
{ "niches": [ { "name": "budget travel", "search": { "query": ["budget travel tips"], "language": ["en"],
  "publishedAtFrom": "month", "sortBy": "foundAt", "sortOrder": "desc", "size": 20 } } ] }
```

`watchlist/state.json`:

```json
{ "lastRun": "<date>", "niches": { "budget travel": { "<channelId>":
  { "handle": "@name", "subscribers": 0, "medianViews": 0, "firstSeen": "<date>" } } } }
```

## Output Format

```markdown
# 📡 Watchlist Digest: {date}

- **Since {last run}:** {n new and n movers, or "No change", or "Baseline"}

## {Niche}

### [{channel}]({url}) · {new or mover} · {subscribers} subs · {median} median views

[![]({best video thumbnail})]({video url})

- **Worth studying:** ✅ {yes, and why in one sentence}
- **Topics working:** {two or three topics}
- **Title formulas:** {template}, for example [{title}]({video url})
- **Best recent video:** [{title}]({video url}) · {views, ratio, date}

- [{channel}]({url}) · {new or mover} · ❌ not worth studying: {why in one sentence}
```

- Length: about 600 words. Up to five channels per niche, strongest first. One line for a niche with no change, and one line for a channel not worth studying.
- Language: plain words and short, complete sentences. Nothing compressed.
- Bullets: one fact each, under 25 words, except quotes and verbatim titles. No extra sections or bullets.
- If it runs long, cut channels, not the summary line or proof.
- Links: link every video, channel, moment, brand and offer you cite, built from IDs, handles and links in the data. Never guess one.
- Thumbnails: use the 320px `mqdefault.jpg` image, on its own line under the heading, linked to the video.

## Common Pitfalls

- Do not save a search without `publishedAtFrom`, or old channels crowd out the new ones.
- Do not change a saved search between runs, or the differences are noise. An edited niche starts a new baseline.
- Do not call a channel new because it dropped out of the sample and came back. Check its first-seen date.
- Do not call a channel a breakout below 1K median views or 5 videos.
