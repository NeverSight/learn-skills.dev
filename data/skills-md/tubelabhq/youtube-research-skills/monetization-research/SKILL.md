---
name: monetization-research
description: Use when the user wants monetization gaps for a YouTube channel or niche, what to sell, how to raise RPM, or who could sponsor it. Requires the TubeLab MCP.
license: MIT
metadata:
  author: tubelab
  version: "5.0"
  requires: tubelab-mcp
---

# Monetization Research

## Overview

Find the monetization gaps. These are things this audience already pays for elsewhere that the channel does not offer, and open products nobody in the niche sells. It also lists the brands that sponsor channels like this one. The evidence is in video descriptions, offer pages and sponsor reads, which are all free to read.

## Workflow

1. Clarify scope only if needed. With no channel, audit the niche for a new entrant.
2. Read the channel's descriptions to see how it earns and who already pays it.
3. Find peers: competitors you can name, plus channels with the same audience from one or two searches using the audience filters. Drop results with a different audience.
4. Open the peers' actual offers. Note what each one is, who it is for, the price if shown, and the link. If a brand is only mentioned out loud, link the moment in the video. Keep a list of every sponsor and the peers that carry it.

## Output Format

```markdown
# 💰 Monetization Research: {channel or niche}

- **Biggest gap:** {one sentence}
- **Peers:** {n}, from {named, search}

## 🎯 Monetization Method Gaps
❌ not done yet, a gap to test · ✅ already done, with its offer linked · Money potential is an estimate.

| Method | Description | Inspiration | Money potential |
|---|---|---|---|
| ❌ {method} | {what it would be here} | [{offer}]({link}) on [{channel}]({url}), {price} | {High, Medium or Low}, {why} |

## 🤝 Sponsors on Channels Like This
✅ this channel already works with the brand.

- [{brand}]({the link the peer gives}) {✅ if this channel already works with it} · [{channel}]({url}) ([{sponsor read, or link in description}]({video or moment url})), [{channel}]({url}) ([{sponsor read, or link in description}]({video or moment url}))

## 🧪 Open Products to Test
1. **{Specific offer}**
   - **Evidence:** {linked proof}
   - **First test:** {one sentence}
```

- Length: about 800 words. Up to eight sponsors, then three open products.
- Language: plain words and short, complete sentences. Nothing compressed.
- Bullets: one fact each, under 25 words, except quotes and verbatim titles. No extra sections or bullets.
- If it runs long, cut whole items. Never cut proof, and never squeeze sentences.
- Links: link every video, channel, moment, brand and offer you cite, built from IDs, handles and links in the data. Never guess one.
- Rows: cover products, courses, communities, newsletters, services, sponsors, affiliates, merch, events, software, and ads with RPM levers. Put ❌ rows first, highest potential on top, and ✅ rows last.
- Sponsors: list brands seen on peers, starting with the brand on the most peers. Say whether each is a sponsor read or only a link in the description. Leave out a peer's own products and the company that owns its show. Mark ✅ only when the channel's own videos or descriptions show the brand.

## Common Pitfalls

- Do not search without `publishedAtFrom` and `classificationQuality` at `"neutral"` or above, or the results fill with low-effort videos.
- Do not call every mention a sponsor. Some are affiliate links or the creator's own products.
- Do not rank a method high when this channel already runs it well.
- Do not copy a method without the trust behind it. A 2K channel cannot run a 500K channel's course funnel.
