---
name: title-formulas
description: Use when the user wants titles or title formulas for a YouTube video or topic, or a title rewrite. Requires the TubeLab MCP.
license: MIT
metadata:
  author: tubelab
  version: "5.0"
  requires: tubelab-mcp
---

# Title Formulas

## Overview

Titles the user can publish, each built on a proven formula, followed by the formulas used. A formula is proven when current outliers in the niche, or the channel's own wins, use it. A formula with no results in the niche is untested. If the user has no video in mind, lead with the formulas and treat the titles as examples.

## Workflow

1. Clarify scope only if needed: the topic or draft title, and what the channel can truthfully claim.
2. Collect formulas from three sources. First, the trending formulas that fit the topic. Second, outliers in this niche: work out the formula behind each winning title, meaning its repeated shape with the slots marked. Third, outliers in one or two neighbouring niches whose viewers are the same kind of people, such as NFL fans for a soccer channel.
3. Label each formula. It is proven when an outlier in this niche or one of the channel's own wins uses it. A formula from a neighbouring niche stays untested here until an outlier in this niche uses it. Use about five searches in total, and reuse outliers already found in this conversation before searching again.
4. Write each title in the channel's own voice.
5. If the user wants a thumbnail too, finish the titles first. Then follow `thumbnail-concepts` for the chosen title.

## Output Format

```markdown
# ✍️ Titles: {topic or draft title}

- **Use:** "{best title}" · {why, with numbers}
- **Can claim:** {what the channel can truthfully say}

1. **{Title}**
   - **Formula:** {formula}
   - **Proof:** [{channel}]({url}) · [{title}]({video url}) · {views, ratio, date}, or "🧪 untested here"

| Formula | Source | Videos | Avg ratio | Example (link) | ✅ Proven or 🧪 untested here |
|---|---|---:|---:|---|---|
```

- Length: about 650 words. Eight titles with at most three untested, then five or six formulas.
- Language: plain words and short, complete sentences. Nothing compressed.
- Bullets: one fact each, under 25 words, except quotes and verbatim titles. No extra sections or bullets.
- If it runs long, cut whole items. Never cut proof, and never squeeze sentences.
- Links: link every video, channel, moment, brand and offer you cite, built from IDs, handles and links in the data. Never guess one.
- Own videos: when the proof is the channel's own video, the linked title is enough.

## Common Pitfalls

- Do not search without `publishedAtFrom` and `classificationQuality` at `"neutral"` or above, or the results fill with low-effort videos.
- Do not write a title over 60 characters, or one that claims what the channel cannot back up.
- Do not fill a slot with what the creator is proud of. Fill it with what the viewer wants.
- Do not pass a language to the trending formats search. It rejects one, and its index is English only.
- Do not reword a formula's pattern when you search with it. The match breaks.
- Do not call a formula rising. Its momentum numbers are not returned.
- Do not carry a formula from a niche whose audience is different. A formula that wins with gamers may not win with gardeners.
