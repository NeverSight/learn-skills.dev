---
name: thumbnail-concepts
description: Use when the user wants thumbnail concepts or images for a YouTube video, or to see which thumbnails work in a niche. Requires the TubeLab MCP.
license: MIT
metadata:
  author: tubelab
  version: "5.0"
  requires: tubelab-mcp
---

# Thumbnail Concepts

## Overview

Three thumbnail concepts for one video. A strong thumbnail joins what the viewer already cares about with what is new in this video. So look at 50 or more thumbnails across both, keep the few with an idea worth reusing, write down exactly what works in them, and combine one of each into every concept.

## Workflow

1. Clarify scope only if needed. Split the video into two plain lines: its unique angle (what is new or different about it) and the familiar problem (what this audience already cares about). With only a niche and no video, search the niche from two angles instead. If the user wants a title too, follow `title-formulas` first and design for the chosen title, so the thumbnail shows what the title leaves out.
2. Run two outlier searches: one for videos with the unique angle, wherever they are, and one for videos on the familiar problem. Ask each for 40 results, the largest page, which costs the same as 20. Add outliers already found in this conversation, if they meet the quality floor in Common Pitfalls.
3. View every thumbnail, 50 or more in all. Numbered contact sheets are the quickest way. Leave out the user's own video, and say if a thumbnail fails to load.
4. Keep only the thumbnails worth analysing, up to six in each set. A keeper has a clear idea you could reuse: a composition, a prop, a gesture, a word or a visual trick. Drop the plain ones, such as a face beside the title's words, a stock photo or a podcast frame. View each keeper again on its own, at a larger size.
5. Before designing anything, write down what works in each set of keepers. Note compositions (how the frame is arranged, the shot, where people and objects sit) and details that pull the eye. Count how many thumbnails in that set use each pattern.
6. Look at the channel's recent thumbnails and note what to keep.
7. Build each concept from one unique-angle pattern and one familiar-problem pattern. Generate the images if you can, or else write one prompt per concept.

## Output Format

```markdown
# 🖼️ Thumbnail Concepts: "{title}"

- **Lead with:** {concept 1, and why in one sentence}
- **Keep from the channel:** {style, colours, face or no face}

[![]({current thumbnail, if published})]({video url})

- **Unique angle:** {what is new in this video}
- **Familiar problem:** {what the audience already cares about}

## 🔍 Patterns That Work
{n} thumbnails viewed: {n} on the unique angle and {n} on the familiar problem. The {n} below were worth analysing.

**In unique-angle thumbnails**

[![]({thumbnail})]({video url}) [![]({thumbnail})]({video url}) [![]({thumbnail})]({video url})

- **{Composition or detail}:** {what you saw, in one sentence} · {n} of {n} thumbnails use it · [{title}]({video url})

**In familiar-problem thumbnails**

[![]({thumbnail})]({video url}) [![]({thumbnail})]({video url}) [![]({thumbnail})]({video url})

- **{Composition or detail}:** {what you saw, in one sentence} · {n} of {n} thumbnails use it · [{title}]({video url})

### 1. {Name}

[![]({example thumbnail})]({video url})

- **Combines:** {unique-angle pattern} + {familiar-problem pattern}
- **Based on:** [{channel}]({url}) · [{title}]({video url}) · {views, ratio}
- **Image:** {what is in the frame and where the eye goes}
- **Text:** {3 words at most, or none}
- **Prompt:** {ready to paste}

![]({generated image, if made})
```

- Length: about 900 words. Up to six kept thumbnails and about five pattern notes in each group, then three concepts.
- Language: plain words and short, complete sentences. Nothing compressed.
- Bullets: one fact each, under 25 words, except quotes, verbatim titles and prompts. No extra sections or bullets.
- If it runs long, cut text. Never cut an image, and never squeeze sentences.
- Links: link every video, channel, moment, brand and offer you cite, built from IDs, handles and links in the data. Never guess one.
- Thumbnails: use the 320px `mqdefault.jpg` image, on its own line under the heading, linked to the video.

## Common Pitfalls

- Do not search without `publishedAtFrom` and `classificationQuality` at `"positive"`. Viral thumbnails on low-effort channels teach the wrong lesson. Widen the dates, never the floor.
- Do not write generic pattern notes such as "high contrast" or "show emotion". Name the exact prop, gesture, word or framing you saw, and where.
- Do not describe a thumbnail you have not viewed, or cite one without showing it.
- Do not keep a thumbnail because its video did well. Keep it for an idea in the image itself.
- Do not let the thumbnail text repeat the title.
- Do not keep the face by default. If faceless thumbnails win in this niche, say so.
- Do not generate a real person's face. Leave a place in the prompt for a real photo of them.
