---
name: niche-finder
description: Use when the user wants new YouTube niche ideas, an untapped or faceless channel idea, or to twist or combine niches, ranked by opportunity. Requires the TubeLab MCP.
license: MIT
metadata:
  author: tubelab
  version: "5.0"
  requires: tubelab-mcp
---

# Niche Finder

## Overview

The product is new channel ideas, not a list of channels that already exist. Start from a deep sample of channels that are breaking out or already earning. Then bend what works: twist a format, merge two formats, or carry a format to an audience or topic where it is missing.

## Workflow

1. Clarify scope only if needed. If the user names a topic, add it as `query` to both presets. If the user names a language, use it instead of the preset languages.
2. Run both presets below for 3 to 4 pages each. Page with `from` (0, 20, 40, 60) and keep every other setting the same. Each page is a paid channel search, so a full run is 6 to 8 searches.
3. From the sample, pick high-quality channels and channels with a clear, repeatable format. Read the best ones, which is free. For a channel you did not read, a video's ratio is its views over the channel's average views. Fetch and view their thumbnails, and say so if one fails to load.
4. Turn them into new niches with one of the three moves in the Overview.
5. For each idea, note one way it could earn beyond AdSense, such as sponsors, affiliates, a product or a community. Base it on what the parent channels or their audience already pay for.
6. Rank the best 10 by opportunity, audience value, money and originality. Check the top 3 with one outlier search each, in the idea's language and over the last year. Count how many returned results closely match the idea, because the search total is capped and means nothing. When a checked idea is crowded, rank it lower and check the idea that takes its place, up to five checks in all. Say so for any top-3 idea left unchecked.

Breakout channels, which are new channels doing better than their size:

```json
{ "publishedAtFrom": "semester", "classificationQuality": "neutral",
  "avgViewsToSubscribersRatioFrom": 1, "averageViewsFrom": 10000, "subscribersFrom": 100,
  "language": ["en", "de", "fr"], "sortBy": "foundAt", "size": 20, "from": 0,
  "excludeNiche": ["music", "song", "lofi", "movies", "breastfeeding", "lingerie", "transparent", "transparency", "clean", "haul"] }
```

Cash cows, which are channels that already earn:

```json
{ "publishedAtFrom": "year", "classificationQuality": "neutral",
  "monetizationAdsense": true, "revenueMonthlyEstimationFrom": 800, "subscribersFrom": 1000,
  "language": ["en", "de", "fr"], "sortBy": "foundAt", "size": 20, "from": 0,
  "excludeNiche": ["music", "song", "lofi", "movies", "breastfeeding", "lingerie", "transparent", "transparency", "clean", "haul", "kids", "news", "politic", "india", "pakistan", "arabic", "manufacturing", "nature", "islamic"] }
```

## Output Format

```markdown
# 🧩 Niche Ideas: {topic or "open discovery"}

- **Best idea:** {one sentence}
- **Sample:** {n} channels from {n} pages

## 🏆 Ranking
Scores are judgment calls: High, Medium or Low.

| # | Idea | Opportunity | Audience value | Money | Originality |
|---|---|---|---|---|---|

## 💡 Ideas

### 1. {Idea}

[![]({parent video thumbnail})]({video url})

- **What it is:** {one sentence on the idea and its audience}
- **Bent from:** [{channel}]({url}), {the move, in a few words}
- **Proof:** [{title}]({video url}) · {views, ratio, date}
- **Audience already watches:** [{channel}]({url}) · [{title}]({video url}) · {views, ratio, date}
- **Earns beyond AdSense:** {one sentence; say "AdSense only so far" when the parents show nothing else}
- **Open check:** {top 3 only: how many returned results match the idea, with the closest one linked; leave this bullet out for the rest}
- **Title formula and first video:** {template}, for example "{first title}"
```

- Length: about 1,800 words. Ten ideas, best first.
- Language: plain words and short, complete sentences. Nothing compressed.
- Bullets: one fact each, under 25 words, except quotes and verbatim titles. No extra sections or bullets.
- If it runs long, cut whole items. Never cut proof, and never squeeze sentences.
- Links: link every video, channel, moment, brand and offer you cite, built from IDs, handles and links in the data. Never guess one.
- Thumbnails: use the 320px `mqdefault.jpg` image, on its own line under the heading, linked to the video.

## Common Pitfalls

- Do not drop `classificationQuality: "neutral"` from a preset, or the results fill with low-effort videos.
- Do not trust ratios from channels with almost no subscribers, or huge views with almost no likes, which are usually paid. Do not trust the language tag either: it can call a Hindi or Urdu video English, so check the title and thumbnail.
- Do not trust a parent channel's numbers alone. Many breakout parents are AI-made or tiny, with a few hundred subscribers. Borrow the format and say what the parent is.
- Do not move a format to a new audience on words alone. The audience must already watch the topic.
- Do not suggest reupload, compilation or AI filler niches without warning that YouTube often demonetizes them.
