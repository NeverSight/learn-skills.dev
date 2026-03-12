---
name: social-media-post
description: When the user wants social media content, post variants, threads, captions, hooks, or channel-specific copy for X, LinkedIn, Instagram, TikTok, or YouTube Shorts. Also use when the user wants to turn a topic, campaign idea, product page, article, or transcript into social posts, or asks for platform-specific repurposing instead of one generic draft. Use this whenever research, source extraction, and writing should be routed through DumplingAI-powered capabilities.
---

# Social Media Post

## Overview

Turn a niche, topic, or campaign idea into platform-specific social posts using DumplingAI v2 capabilities.

## Allowed Commands

```bash
dumplingai run capability google_search --input '{"query":"topic"}'
dumplingai run capability scrape_page --input '{"url":"https://example.com"}'
dumplingai run capability get_youtube_transcript --input '{"videoUrl":"https://youtube.com/watch?v=ID"}'
```

## Workflow

1. Identify the niche, audience, goal, and target platforms.
2. Research the topic first with `google_search`, then deepen with `scrape_page`.
3. Use transcripts as optional source material when a video is provided.
4. Draft platform-specific copy instead of reusing one generic post everywhere.

## Output Strategy

```bash
dumplingai run capability google_search --input '{"query":"AI sales assistant pain points for SMB founders"}' > .dumplingai/search.json
dumplingai run capability scrape_page --input '{"url":"https://example.com/product-page"}' > .dumplingai/product.json
dumplingai run capability get_youtube_transcript --input '{"videoUrl":"https://youtube.com/watch?v=ID"}' > .dumplingai/transcript.json
```

Read incrementally:

```bash
head -80 .dumplingai/search.json
rg '"results"|"content"|"transcript"' .dumplingai/product.json
```
