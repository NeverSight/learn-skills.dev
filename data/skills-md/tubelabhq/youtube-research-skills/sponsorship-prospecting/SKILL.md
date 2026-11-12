---
name: sponsorship-prospecting
description: Use when the user wants to find YouTube channels to sponsor for a product or business, build a creator prospect list, or match creators to a buyer. Requires the TubeLab MCP.
license: MIT
metadata:
  author: tubelab
  version: "5.0"
  requires: tubelab-mcp
---

# Sponsorship Prospecting

## Overview

A scored list of YouTube channels worth sponsoring for one product. A brand pays for views by the right people, not for subscribers. So judge reach by median views, and fit by how closely the audience's country, age, gender and income match the buyer.

## Workflow

1. Clarify scope only if needed: the product, the buyer, and any budget.
2. Start with outlier searches on the topics the buyer watches; they are cheap and find most prospects. Then run one channel search with the buyer's audience filters; it returns few on-topic hits. Only channel-search hits carry audience estimates; where a prospect has none, write "no estimate" and judge fit from who the channel says it serves. Skip the similar-channels search. Expect three to five searches; reads are free.
3. Keep two pools. Channels that already take sponsors are proven, and their sponsors show what sells to this audience. One tied to a competing product has little room left; say so. Channels with the right audience and no sponsor yet are cheaper and more open.
4. Read each shortlisted channel. Note its median views (the last ten or so long videos, skipping any under a week old), upload rhythm, how steady its views are, sponsor mentions in the descriptions of two or three recent videos, and a public contact path from the channel's description, links or recent video descriptions. Fetch and view the thumbnail of each video you feature, and say so if one fails to load.
5. Score each prospect from 1 to 5 on audience fit (counted double), topic fit, reach, steady views, sponsor room (none yet, some, or crowded), brand safety and contact path. Rank by total. Drop any prospect whose audience is likely outside the buyer's country, whatever its total.
6. Estimate a cost band per sponsored video from median views. Unless the user gives a rate, assume $20 to $40 per 1,000 median views, and note that small channels often set a minimum fee above it. Label it as an estimate, not as the creator's rate.

## Output Format

```markdown
# 🤝 Sponsorship Prospects: {product}

- **Best fit:** {channel, and why in one sentence}
- **Buyer:** {the audience searched for}
- **Budget:** {if given, and how the top picks fit inside it}

## 🏆 Prospects

Median views come from each channel's last {n} long videos. Audience fields are estimates.

| Channel (link) | Subs | Median views | Audience (estimate) | Sponsors now (competitors marked) | Fit (total score) | Contact |
|---|---:|---:|---|---|---:|---|

## ✅ Best Fits

### 1. [{channel}]({url})

[![]({thumbnail of a recent strong video})]({video url})

- **Why it fits:** {one sentence}
- **Proof:** [{title}]({video url}) · {views, ratio, date}
- **Sponsors now:** {linked brands, or "none found"; say if one is a competitor of the product}
- **Outreach angle:** {one sentence the brand could open with, tied to a specific video}
- **Estimated cost:** {band per sponsored video, labelled as an estimate}

## 📋 CSV

~~~csv
channel,url,subscribers,median_views,audience,sponsors_now,fit_score,contact
~~~
```

- Length: about 900 words, not counting the CSV. 10 to 15 prospects in the table, best first, and the top 3 to 5 as blocks.
- Language: plain words and short, complete sentences. Nothing compressed.
- Bullets: one fact each, under 25 words, except quotes and verbatim titles. No extra sections or bullets.
- If it runs long, cut whole items. Never cut proof, and never squeeze sentences.
- Links: link every video, channel, moment, brand and offer you cite, built from IDs, handles and links in the data. Never guess one.
- Thumbnails: use the 320px `mqdefault.jpg` image, on its own line under the heading, linked to the video.

## Common Pitfalls

- Do not search without `publishedAtFrom` and `classificationQuality` at `"neutral"` or above, or the results fill with low-effort videos.
- Do not rank by subscribers. A mismatched big channel is a worse buy than a matched small one.
- Do not present audience fields as facts. They are estimates, so ask the creator for an analytics screenshot before paying.
- Do not trust the language tag for the audience's country. It can call a Hindi or Urdu video English.
- Do not list made-for-kids channels, dormant channels (no upload in about the last month), or channels whose views swing wildly.
- Do not publish private contact details. Use only what the channel shows publicly.
- Do not trust the sponsor flag alone. It misses some sponsors and flags some channels with none visible, so check the descriptions either way.
