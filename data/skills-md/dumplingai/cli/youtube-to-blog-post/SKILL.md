---
name: youtube-to-blog-post
description: When the user wants to turn a YouTube video into a blog post, article, outline, newsletter draft, or transcript-based written summary. Also use when the user mentions repurposing a video, extracting a transcript, rewriting a YouTube talk into a post, or expanding a creator video into long-form content. Use this whenever the workflow should start with transcript extraction and optional source verification through DumplingAI capabilities.
---

# YouTube to Blog Post

## Overview

Turn a YouTube video into a structured blog post using DumplingAI v2 capabilities.

## Allowed Commands

```bash
dumplingai run capability get_youtube_transcript --input '{"videoUrl":"https://youtube.com/watch?v=ID"}'
dumplingai run capability google_search --input '{"query":"topic from the video"}'
dumplingai run capability scrape_page --input '{"url":"https://example.com/reference"}'
```

## Workflow

1. Fetch the transcript first and save it to `.dumplingai/transcript.json`.
2. Extract the main argument, audience, examples, and action items.
3. Verify outside claims with `google_search` and `scrape_page` when needed.
4. Draft a blog post that stays faithful to the transcript and cited sources.

## Output Strategy

```bash
dumplingai run capability get_youtube_transcript --input '{"videoUrl":"https://youtube.com/watch?v=ID"}' > .dumplingai/transcript.json
dumplingai run capability google_search --input '{"query":"company or concept from the video"}' > .dumplingai/search.json
dumplingai run capability scrape_page --input '{"url":"https://example.com/reference"}' > .dumplingai/reference.json
```

Read incrementally:

```bash
head -80 .dumplingai/transcript.json
rg '"transcript"|"text"|"results"' .dumplingai/transcript.json
```
