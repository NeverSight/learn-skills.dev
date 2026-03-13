---
name: translate-mom-tweets
description: Fetch translated video tasks from the translate.mom API and generate hook-driven tweet drafts based on SRT subtitle content. Use when the user asks to "generate tweets", "make tweets for translate.mom", "tweet drafts", "translate mom tweets", "top tasks tweets", "what videos are trending", "create posts for today's translations", or any request involving translate.mom content promotion on Twitter/X.
---

# Translate Mom Tweets

Generate scroll-stopping tweet drafts for translated video content from the translate.mom platform.

## Workflow

### 1. Fetch tasks

Run the fetch script to get the day's top tasks (defaults to today):

```bash
./scripts/fetch_tasks.sh           # today
./scripts/fetch_tasks.sh 2026-02-23  # specific date
```

API: `GET http://plausible.translate.mom:8001/top-tasks?date=YYYY-MM-DD`

Override the base URL with `TRANSLATE_MOM_API` env var if needed.

Response shape:
```json
{
  "tasks": [{
    "id": "...",
    "videoUrl": "...",
    "thumbnailUrl": "...",
    "viewCount": 123,
    "srtFiles": { "en": "https://...srt-url..." },
    "targetLanguage": "en",
    "status": "...",
    "sourceUrl": "..."
  }]
}
```

- Returns up to 20 tasks ordered by `viewCount` descending
- `srtFiles` is a map of `{ languageCode: srtUrl }`
- `sourceUrl` is the original video link (use this in the tweet)

### 2. Fetch SRT content

For each task, download the SRT for the `targetLanguage` to understand the video content:

```bash
./scripts/fetch_srt.sh "https://...srt-url..."
```

This strips timestamps and outputs dialogue text only. Read the dialogue to identify the most dramatic, funny, or shocking moment.

### 3. Generate tweet draft

For each task, write **one tweet** following this structure:

1. **Hook line** — the single most dramatic moment from the subtitles. Use real names if they appear in the subtitles, otherwise fall back to "this man", "this woman", "she", "he". Must trigger curiosity. One emoji max.
2. **Context line** — 1-2 sentences of setup. What happened, why it matters.
3. **CTA line** — mention the target language translation. One emoji. Include `[video link]` placeholder (the user will replace with `sourceUrl` or their preferred link).

**Constraints:**
- Total tweet must be under 280 characters
- No more than 1 emoji per line
- The hook must make someone stop scrolling — if you'd scroll past it, rewrite it
- Always emphasize that the video is **translated to [targetLanguage]**

For detailed examples and style patterns, read `references/tweet_examples.md`.

### 4. Output format

Present results as a numbered list:

```
## Tweets for 2026-02-23 (X tasks found)

### 1. [brief video description]
Views: 12,345 | Language: English

> This man told his boss exactly what he thinks... on camera 😳
>
> A factory worker finally snaps after months of unpaid overtime. The whole shop floor watched.
>
> Fully translated to English 🎬
> [video link]

Source: [sourceUrl]

---
```

If `srtFiles` is empty for a task, skip it and note "No subtitles available" in the output.
