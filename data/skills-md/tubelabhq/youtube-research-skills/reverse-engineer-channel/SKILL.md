---
name: reverse-engineer-channel
description: Use when the user wants to reverse engineer a YouTube channel into what works for it, from formats, title and thumbnail formulas, hook formulas and script structure to how it earns, plus what does not work. Requires the TubeLab MCP.
license: MIT
metadata:
  author: tubelab
  version: "6.0"
  requires: tubelab-mcp
---

# Reverse Engineer Channel

## Overview

One channel taken apart into formulas the user can reuse. A formula is a pattern, not a quote: a title with its slots, a thumbnail as its parts, a hook as its order of beats. It counts when it can be reused, even if the channel used it once. Every read is free. Not for the user's own channel (`channel-analysis`).

## Workflow

1. If the user names their own channel or market, aim the learnings at it.
2. Read the channel's long-form list and its Shorts. The list holds the latest 120 videos, newest first, with rough dates. Read a video for its exact date.
3. Find the outliers: videos with at least twice the list's average views, or the three highest. Then split the list into up to ten equal blocks and compare median views. A turning point is where the median jumps or falls, and stays there, after something changed.
4. View every thumbnail, on numbered contact sheets.
5. Group the videos into formats. A format is a video idea that can be remade with a twist, whatever its title or thumbnail, even if used once. Count how many of its videos beat their neighbours, meaning the median of their own block, because older videos had longer to collect views. Rank videos the same way.
6. Find what does not work: the formats, topics and habits of the weakest videos. Leave out last month's uploads and channel updates such as Q&As.
7. Read the first 30 seconds of the five best videos and two weak ones. Name each opening's beats in words that fit any video, such as setup, stakes or twist. A hook formula is an order of beats that two or more strong openings share.
8. Read the full transcripts of three of the best videos, from different formats. Mark each beat and its time, named the same way, and keep the layout they share.
9. Find how the channel earns, from its description, the descriptions of the ten best and five newest videos, and sponsor reads in the transcripts.
10. Write five learnings to copy, best first. Each names the skill that runs it, such as `title-formulas`, `thumbnail-concepts`, `script-breakdown` or `monetization-research`, and a prompt to paste. Add two or three things not to copy, because they need this channel's fame, budget or access.

## Output Format

```markdown
# 🔬 Reverse Engineering: [{channel}]({url})

- **Why it works:** {one sentence, with numbers}
- **Sample:** the latest {n} long videos, from {month year} to {month year} · {n} thumbnails viewed · {n} openings and {n} full scripts read
- **Shorts:** {how they do next to the long videos, or "none posted"}
- **Start with:** {the one learning to act on this week}

## 📈 Outliers

{n} of {n} videos have at least twice the channel's average views.

[![]({thumbnail})]({video url}) [![]({thumbnail})]({video url}) [![]({thumbnail})]({video url})

1. [{title}]({video url}) · {views, ratio} · {its format}

- **Turning point, {month year} · {what changed}:** median views went from {views} to {views} · [{title}]({video url})

## 🧩 Formats That Work

A video beats its neighbours when it has more views than the median of the videos published around it.

### 1. {Format name} · {n} of {n} beat their neighbours

[![]({thumbnail})]({video url}) [![]({thumbnail})]({video url}) [![]({thumbnail})]({video url})

- **Topics:** {the topics it covers, best first}
- **Title formula:** "{the pattern with every slot in square brackets, such as "[Number] Days In [Place]"}" · [{title}]({video url}) · {views, ratio}
- **Thumbnail formula:** {the parts a viewer can point at, each a few words in square brackets, such as "[face, shocked, centre] + [object, oversized, left] + [price in white, top right]"}
- **Length:** {usual length}

## 🚫 What Doesn't Work

### 1. {Format, topic or habit} · {n} of {n} beat their neighbours

[![]({thumbnail})]({video url})

- **What it is:** "{title pattern, slots in square brackets}" · {thumbnail in a few words}
- **Proof:** [{title}]({video url}) · {views, ratio, date}
- **How it differs:** {what the formats that work have and this lacks}

## 🎣 Hook Formulas

### 1. {Formula name} · {n} of {n} strong openings

- **Structure:** {beat} → {beat} → {beat}
- **Runs:** the first {n} seconds
- **Weak videos:** {whether the weak openings read use it too}

<details>
<summary>Example: {title}</summary>

[{title}]({video url}) · {views, ratio}

- **{Beat}:** "{its words}"

</details>

## 🎬 Script Structure

- **Layout:** Hook 0:00 → {beat} {when} → ... → {ending} {when}
- **What repeats:** {the device every script reuses, and how often}
- **How it ends:** {one sentence}

<details>
<summary>Example: {title}</summary>

[{title}]({video url}) · {views, ratio, length}

| Time | Beat | What happens |
|---|---|---|
| [{m:ss}]({link to that moment}) | {type} | {a few words} |

</details>

## 💰 How It Earns

| Method | Offer | Where it shows |
|---|---|---|
| {product, merch, newsletter, course, membership, community, app, sponsor or affiliate: check each} | [{offer or brand}]({url}) | [{title}]({video or moment url}) · {in the description, or said in the video} |

- **Not found:** {the methods looked for and not seen}

## 🧠 Learnings

1. **{What to copy}**
   - **Proof:** [{title}]({video url}) · {views, ratio, date}
   - **Run next:** `{skill}` · "{a prompt the user can paste, with [square brackets] for what they fill in}"

- ❌ **Do not copy {move}:** {why it will not carry over, with proof}
```

- Length: about 1,700 words. Up to six outliers, three turning points, four formats that work, three that do not, three hook formulas, one script example and ten ways it earns.
- Language: plain words and short, complete sentences. Nothing compressed.
- Bullets: one fact each, under 25 words, except quotes, verbatim titles, formulas and prompts. No extra sections or bullets.
- If it runs long, cut whole items. Never cut proof.
- Links: link every video, channel, moment, brand and offer you cite, built from IDs, handles and links in the data. Never guess one.
- Thumbnails: the 320px `mqdefault.jpg` image, linked to its video, on its own line. A format that works shows its three best on one line, and the outliers share one line.
- Quotes: only inside the collapsed examples, word for word, with misspelt names fixed. Never paste a full transcript.

## Common Pitfalls

- One hit can be a format, but not a turning point.
- Do not study only the hits. A trait the worst videos share is not why the best ones won.
- Do not state a cause as fact. The data shows what changed, not why viewers came.
