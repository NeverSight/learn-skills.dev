---
name: fetch-tweet
description: Fetch tweet content directly from fxtwitter API. Use when given a tweet/X URL to extract the tweet text, author, media, and engagement stats without loading x.com.
user-invocable: false
---

# Fetch Tweet

You fetch tweet content using the fxtwitter API, which returns structured JSON without requiring JavaScript rendering or authentication.

## Why fxtwitter

X/Twitter requires JavaScript to render tweets. `WebFetch` on `x.com` returns an empty shell. The fxtwitter API (`api.fxtwitter.com`) serves the same tweet data as plain JSON — no auth, no JS, no rate-limit friction for reasonable use.

## URL Conversion

Given any tweet URL, convert it to the fxtwitter API endpoint:

| Input URL pattern | API URL |
|---|---|
| `https://x.com/<user>/status/<id>` | `https://api.fxtwitter.com/<user>/status/<id>` |
| `https://twitter.com/<user>/status/<id>` | `https://api.fxtwitter.com/<user>/status/<id>` |
| `https://fxtwitter.com/<user>/status/<id>` | `https://api.fxtwitter.com/<user>/status/<id>` |
| `https://vxtwitter.com/<user>/status/<id>` | `https://api.fxtwitter.com/<user>/status/<id>` |

Extract the `<user>` and `<id>` from the input URL, then construct `https://api.fxtwitter.com/<user>/status/<id>`.

## How to Fetch

Use `WebFetch` with the converted API URL:

```
WebFetch(url: "https://api.fxtwitter.com/<user>/status/<id>", prompt: "Extract the tweet JSON. Return: author name, handle, tweet text, date, media URLs (if any), likes, retweets, replies, views.")
```

## Response Structure

The fxtwitter API returns JSON with this structure:

```json
{
  "code": 200,
  "message": "OK",
  "tweet": {
    "url": "https://x.com/user/status/123",
    "text": "The tweet content...",
    "author": {
      "name": "Display Name",
      "screen_name": "handle"
    },
    "created_at": "Thu Jan 30 12:00:00 +0000 2026",
    "likes": 1000,
    "retweets": 500,
    "replies": 200,
    "views": 50000,
    "media": {
      "photos": [...],
      "videos": [...]
    }
  }
}
```

## Usage Pattern

When you receive a tweet URL (x.com, twitter.com, fxtwitter.com, or vxtwitter.com):

1. **Parse** the URL to extract username and tweet ID
2. **Convert** to `https://api.fxtwitter.com/<user>/status/<id>`
3. **Fetch** using `WebFetch` with the API URL
4. **Present** the tweet content in a readable format:

```
**Author Name** (@handle) — Date

"Tweet text here"

Engagement: X views, Y likes, Z retweets, W replies
```

If the tweet contains media (photos/videos), include the URLs.

## Error Handling

- If fxtwitter returns a non-200 status, the tweet may have been deleted or the account suspended
- If the URL doesn't match any known tweet URL pattern, ask the user for a valid tweet link
