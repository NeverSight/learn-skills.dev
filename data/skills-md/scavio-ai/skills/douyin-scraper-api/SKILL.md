---
name: douyin-scraper-api
description: Pull Douyin videos, user profiles and feeds, comments, hashtags, music, live rooms, the hot-search board, keyword search across videos, users, music and hashtags, and live-room lookup by creator. 27 endpoints, structured JSON.
version: 1.0.0
tags: douyin, douyin-api, china-tiktok, short-video, social-media-data, creator-data, video-data, comments, hashtags, trending, live-stream, china-market, influencer-data, agents, structured-data, json, ai-agents, scraping-api
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    emoji: "\U0001F3B5"
    homepage: https://scavio.dev/docs?utm_source=agent-skills&utm_medium=skill&utm_campaign=douyin-scraper-api
---

# Douyin Scraper API - Videos, Creators, Comments, Search

Pull Douyin (the Chinese TikTok) videos, user profiles and feeds, comments, hashtags, music, live rooms, the hot-search board, run keyword search across videos, users, music and hashtags, and find which creators are live. All endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Pull a Douyin video's full detail or statistics (play, like, share, download counts), or resolve a share link
- Read a user's profile, their posts, their liked videos, followers or following, or their current live stream
- Read a video's comments and comment replies, or videos recommended alongside it
- Look up a hashtag or a sound (music) and the videos under it
- Read the hot-search board, the recommended home feed, or a live room by `web_rid` or `live.douyin.com` URL
- Search Douyin by keyword - general, or scoped to videos, users, music or hashtags
- Find a creator's live room by nickname or Douyin ID, with live status, room id and stream title
- Do China-market social research, creator analysis or trend spotting on Douyin

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=douyin-scraper-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=douyin-scraper-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Endpoints in this skill cost 1 credit each unless the table below says otherwise.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
The smallest purchase is 2,500 credits for $25, and monthly plans work out
cheaper per credit if the usage is steady rather than one-off.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Pricing

Base URL: `https://api.scavio.dev`.

- **Search endpoints (`/api/v1/douyin/search*`) cost 10 credits** each.
- **Every other Douyin endpoint costs 1 credit.**

Check `credits_used` on each response to confirm what a call cost.

## Endpoints

### Video

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/douyin/video` | 1 | Full detail for a single video by id |
| `POST /api/v1/douyin/video/by-share-url` | 1 | Resolve a share link to its video detail |
| `POST /api/v1/douyin/video/statistics` | 1 | Play, like, share and download counts for one or more videos |
| `POST /api/v1/douyin/video/comments` | 1 | Top-level comments on a video |
| `POST /api/v1/douyin/video/comment-replies` | 1 | Replies under a comment |
| `POST /api/v1/douyin/related` | 1 | Videos recommended alongside a given video |

### User

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/douyin/user/profile` | 1 | Profile details for a user |
| `POST /api/v1/douyin/user/posts` | 1 | A user's published videos |
| `POST /api/v1/douyin/user/likes` | 1 | A user's publicly liked videos |
| `POST /api/v1/douyin/user/followers` | 1 | A user's followers |
| `POST /api/v1/douyin/user/following` | 1 | Accounts a user follows |
| `POST /api/v1/douyin/user/live` | 1 | A user's current live stream |

### Hashtag / music / live

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/douyin/hashtag` | 1 | Details for a hashtag |
| `POST /api/v1/douyin/hashtag/videos` | 1 | Videos under a hashtag |
| `POST /api/v1/douyin/music` | 1 | Details for a sound |
| `POST /api/v1/douyin/music/videos` | 1 | Videos using a sound |
| `POST /api/v1/douyin/live/room` | 1 | Live room detail (title, status, viewers, stream URLs, anchor) by `web_rid` or `live_room_url` |

### Trending / feed / resolve

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/douyin/trending` | 1 | The current hot-search board |
| `POST /api/v1/douyin/home-feed` | 1 | The recommended home feed |
| `POST /api/v1/douyin/resolve/video-id` | 1 | Extract a video id from a Douyin URL |
| `POST /api/v1/douyin/resolve/user-id` | 1 | Extract a user `sec_user_id` from a Douyin URL |

### Search (10 credits each)

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/douyin/search` | 10 | General keyword search |
| `POST /api/v1/douyin/search/videos` | 10 | Search videos by keyword |
| `POST /api/v1/douyin/search/users` | 10 | Search users by keyword |
| `POST /api/v1/douyin/search/music` | 10 | Search sounds by keyword |
| `POST /api/v1/douyin/search/live` | 10 | Live rooms by creator nickname or Douyin ID (`is_live`, `room_id`, `title`); pages with `cursor` |
| `POST /api/v1/douyin/search/hashtags` | 10 | Search hashtags by keyword |

## Key identifiers

- **`aweme_id`** - a video id (e.g. `7436613508646702348`). Used by `video`, `video/statistics`, `video/comments`, `video/comment-replies`, `related`.
- **`sec_user_id`** - a user id (the `MS4wLjABAAAA...` string). Used by the user endpoints. Get it from `resolve/user-id` if you only have a profile URL.
- Feed/comment endpoints paginate with `max_cursor` / `cursor` / `max_time` from the previous response, and take an optional `count` (1-50).

## Examples

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# 1. Resolve a share link, then read that video's comments (1 credit each)
video = requests.post(f"{BASE}/api/v1/douyin/video/by-share-url", headers=HEADERS,
    json={"share_url": "https://v.douyin.com/v1zNJi__Teg/"}).json()
aweme_id = video["data"]["aweme_id"]
comments = requests.post(f"{BASE}/api/v1/douyin/video/comments", headers=HEADERS,
    json={"aweme_id": aweme_id, "count": 50}).json()

# 2. Resolve a profile URL to a user id, then read the user's posts (1 credit each)
uid = requests.post(f"{BASE}/api/v1/douyin/resolve/user-id", headers=HEADERS,
    json={"url": "https://www.douyin.com/user/"}).json()["data"]["sec_user_id"]
posts = requests.post(f"{BASE}/api/v1/douyin/user/posts", headers=HEADERS,
    json={"sec_user_id": uid, "count": 20}).json()

# 3. Keyword search - 10 credits
found = requests.post(f"{BASE}/api/v1/douyin/search/videos", headers=HEADERS,
    json={"keyword": "美食"}).json()
```

curl:

```bash
curl -s https://api.scavio.dev/api/v1/douyin/trending \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}'
```

## Response shape

Every response uses the envelope `{ data, response_time, credits_used, credits_remaining }`. `data` carries the video / user / feed payload, with lists under keys like `videos`, `comments`, `users` and cursors for pagination.

## Guardrails

- **Search costs 10 credits per call; everything else costs 1.** Confirm with `credits_used` and avoid running search in tight loops.
- Use `resolve/video-id` and `resolve/user-id` to turn a Douyin URL into the id the other endpoints need.
- Paginate only with the cursor the previous response returned (`max_cursor` / `cursor` / `max_time`); stop when it stops advancing.
- Trending, hot-search and rankings are point-in-time snapshots - re-fetch for a fresh board rather than assuming stability.
- Never fabricate video counts, comment text, follower numbers or user details. Only return what the API returned.
- Comments and profiles are written by real people. Summarise; do not build profiles of individuals.

## Failure handling

- `400` means malformed input (e.g. a bad URL). Fix and retry.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `422` means a required identifier is missing (e.g. no `sec_user_id`). Supply it and retry.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=douyin-scraper-api).
- `502` means the source is temporarily unavailable - wait a few seconds and retry.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.
