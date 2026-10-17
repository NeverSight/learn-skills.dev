---
name: content-repurposer
description: >
  Turn one long-form source (blog post, podcast, YouTube video, webinar,
  transcript) into a batch of short-form reel ideas and scripts. Use when the
  user says "repurpose", "turn this into reels", "atomize", "clip this",
  "content from my blog/podcast", or "make videos from this".
user-invokable: true
argument-hint: "[paste the source, transcript, or link summary]"
license: MIT
metadata:
  author: Ootto
  version: "1.0.0"
  category: content
---

# Content Repurposer

Turn one long source into a week of short-form videos — the heart of a content factory.

## When to use
You have a blog post, podcast episode, YouTube video, or webinar and want 5+ reels out of it instead of one.

## What you'll need
The source text or transcript (paste it, or a detailed summary), your audience, and the platform. Optional: brand voice.

## Instructions
Give Claude the source, then run this prompt:

```
You are my content repurposing engine. From the source below, extract the short-form video gold.

Source:
"""
[paste blog post / transcript / detailed summary]
"""

Audience: [who it's for]   Platform: [Reels/TikTok/Shorts]

Do this:
1. Pull the 5 most reel-worthy ideas (a surprising claim, a how-to, a myth, a story, a result). One line each.
2. For each idea: write 1 scroll-stopping hook + a 3-beat outline (hook → value → CTA).
3. Flag which 2 have the highest viral potential and why (emotion, specificity, or contrarian angle).

Keep it concrete and lifted from the source — no generic filler.
```

**Obsidian memory tip:** Keep your long-form library in your Obsidian vault (Filesystem MCP), and Claude can repurpose *across* sources — "find the 5 best reel ideas across everything I published this quarter," not just one post.

**Tip:** One good podcast can become 8-10 reels. Batch the scripts, then film in one sitting.

---

Built by **[Ootto](https://www.ootto.ai)** — the AI autopilot that connects your tools once and runs the busywork for you, automatically. [Book a demo →](https://www.ootto.ai)
