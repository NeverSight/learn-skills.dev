---
name: adhx
description: Fetch X/Twitter posts as clean LLM-friendly JSON via the ADHX API. Converts any x.com, twitter.com, or adhx.com link into structured data with full article content, author info, and engagement metrics. Use when a user shares an X/Twitter link and wants to read, analyze, or summarize the post.
triggers:
  - x.com
  - twitter.com
  - adhx.com
  - tweet
  - read this post
  - read this tweet
---

# ADHX - X/Twitter Post Reader

Fetch any X/Twitter post as structured JSON for analysis using the ADHX API.

## How It Works

ADHX provides an API that returns clean JSON for any X post, including full article/long-form content. This is far superior to scraping or browser-based approaches for LLM consumption.

## API Endpoint

```
https://adhx.com/api/share/tweet/{username}/{statusId}
```

## URL Patterns

Extract `username` and `statusId` from any of these URL formats:

| Format | Example |
|--------|---------|
| `x.com/{user}/status/{id}` | `https://x.com/dgt10011/status/2020167690560647464` |
| `twitter.com/{user}/status/{id}` | `https://twitter.com/dgt10011/status/2020167690560647464` |
| `adhx.com/{user}/status/{id}` | `https://adhx.com/dgt10011/status/2020167690560647464` |

## Workflow

When a user shares an X/Twitter link:

1. **Parse the URL** to extract `username` and `statusId` from the path segments
2. **Fetch the JSON** using curl:
   ```bash
   curl -s "https://adhx.com/api/share/tweet/{username}/{statusId}"
   ```
3. **Use the structured response** to answer the user's question (summarize, analyze, extract key points, etc.)

## Response Schema

The API returns JSON with this structure:

```json
{
  "id": "statusId",
  "url": "original x.com URL",
  "text": "short-form tweet text (empty if article post)",
  "author": {
    "name": "Display Name",
    "username": "handle",
    "avatarUrl": "profile image URL"
  },
  "createdAt": "timestamp",
  "engagement": {
    "replies": 0,
    "retweets": 0,
    "likes": 0,
    "views": 0
  },
  "article": {
    "title": "Article title (for long-form posts)",
    "previewText": "First ~200 chars",
    "coverImageUrl": "hero image URL",
    "content": "Full markdown content with images"
  }
}
```

- `text` contains the tweet body for regular tweets
- `article` is present for long-form X articles and contains the full markdown content
- `article.content` includes inline image references as markdown `![](url)`

## Example

User: "Summarize this post https://x.com/dgt10011/status/2020167690560647464"

```bash
curl -s "https://adhx.com/api/share/tweet/dgt10011/2020167690560647464"
```

Then use the returned JSON to provide the summary.

## Notes

- No authentication required
- Works with both short tweets and long-form X articles
- Always prefer this over browser-based scraping for X content
- If the API returns an error or empty response, inform the user the post may not be available
