---
name: x-api-reader
description: Read posts, threads, user timelines, and search X (Twitter) using the X API v2. Use when the user asks to read tweets, look up X posts, search X, get a user's timeline, read a thread, or fetch content from X/Twitter.
---

# X API Reader

Read-only access to X (Twitter) via the X API v2. All requests use `curl` against `https://api.x.com`.

## Setup

The bearer token is stored at `~/.config/x-api/.env`:

```
X_BEARER_TOKEN=your_token_here
```

Before making any API call, load it:

```bash
source ~/.config/x-api/.env
```

If the file doesn't exist, help the user set it up:

```bash
mkdir -p ~/.config/x-api && chmod 700 ~/.config/x-api
read -s "token?Enter your X Bearer Token: "
echo "X_BEARER_TOKEN=$token" > ~/.config/x-api/.env
chmod 600 ~/.config/x-api/.env
```

To get a bearer token: https://developer.x.com/en/portal/dashboard — create a Project + App (Free tier gives 100 reads/month), copy the Bearer Token.

## Authentication

All requests use App-Only Bearer Token auth:

```bash
-H "Authorization: Bearer $X_BEARER_TOKEN"
```

## Core Read Endpoints

### Look up a post by ID

```bash
curl -s "https://api.x.com/2/tweets/{id}?tweet.fields=created_at,public_metrics,conversation_id,author_id,article,note_tweet&expansions=author_id&user.fields=username,name" \
  -H "Authorization: Bearer $X_BEARER_TOKEN"
```

If the post is an **X Article**, the response includes `article.plain_text` with the full article body, `article.title`, and `article.preview_text`. Always include `article` in `tweet.fields` to capture long-form content.

### Look up multiple posts by IDs

```bash
curl -s "https://api.x.com/2/tweets?ids={id1},{id2},{id3}&tweet.fields=created_at,public_metrics,author_id&expansions=author_id&user.fields=username,name" \
  -H "Authorization: Bearer $X_BEARER_TOKEN"
```

### Get a user's profile by username

```bash
curl -s "https://api.x.com/2/users/by/username/{username}?user.fields=description,public_metrics,created_at,profile_image_url" \
  -H "Authorization: Bearer $X_BEARER_TOKEN"
```

### Get a user's recent posts (timeline)

Requires the user's numeric ID (get it from the username lookup above).

```bash
curl -s "https://api.x.com/2/users/{user_id}/tweets?max_results=10&tweet.fields=created_at,public_metrics,conversation_id&expansions=author_id&user.fields=username,name" \
  -H "Authorization: Bearer $X_BEARER_TOKEN"
```

Supports `since_id`, `until_id`, `start_time`, `end_time`, `max_results` (5-100), and `pagination_token`.

### Search recent posts (last 7 days)

```bash
curl -s "https://api.x.com/2/tweets/search/recent?query={query}&max_results=10&tweet.fields=created_at,public_metrics,author_id,conversation_id&expansions=author_id&user.fields=username,name" \
  -H "Authorization: Bearer $X_BEARER_TOKEN"
```

The `query` parameter supports operators — see the [search operators docs](https://docs.x.com/x-api/posts/search/integrate/operators.md).

Common query patterns:
- `from:username` — posts from a specific user
- `to:username` — replies to a user
- `conversation_id:123456` — all posts in a thread
- `#hashtag` — posts with a hashtag
- `"exact phrase"` — exact match
- `-is:retweet` — exclude retweets
- `has:links` — posts containing URLs
- Combine with AND (space), OR, grouping with `()`

### Get a user's mentions

```bash
curl -s "https://api.x.com/2/users/{user_id}/mentions?max_results=10&tweet.fields=created_at,public_metrics,author_id&expansions=author_id&user.fields=username,name" \
  -H "Authorization: Bearer $X_BEARER_TOKEN"
```

### Get quote posts for a post

```bash
curl -s "https://api.x.com/2/tweets/{id}/quote_tweets?max_results=10&tweet.fields=created_at,public_metrics,author_id&expansions=author_id&user.fields=username,name" \
  -H "Authorization: Bearer $X_BEARER_TOKEN"
```

## Reading Threads / Conversations

X doesn't have a dedicated "get thread" endpoint. To reconstruct a thread:

1. Get the original post and note its `conversation_id`
2. Search for all posts in that conversation:

```bash
curl -s "https://api.x.com/2/tweets/search/recent?query=conversation_id:{conv_id}&tweet.fields=created_at,public_metrics,author_id,in_reply_to_user_id,referenced_tweets&expansions=author_id,referenced_tweets.id&user.fields=username,name&max_results=100" \
  -H "Authorization: Bearer $X_BEARER_TOKEN"
```

3. To get only the original author's posts in the thread, add `from:username`:
   `query=conversation_id:{conv_id} from:username`

**GOTCHA: `search/recent` only covers the last 7 days.** For older threads, use the user timeline endpoint instead with `start_time` and `end_time` to narrow the window around the tweet date. Then filter results by `conversation_id` to find thread replies:

```bash
curl -s "https://api.x.com/2/users/{user_id}/tweets?max_results=100&tweet.fields=created_at,public_metrics,conversation_id,note_tweet,referenced_tweets&start_time=2025-12-22T00:00:00Z&end_time=2025-12-25T00:00:00Z" \
  -H "Authorization: Bearer $X_BEARER_TOKEN"
```

Then filter the results where `conversation_id` matches the original tweet's ID. This works for any tweet age, unlike search/recent.

## Fields & Expansions Quick Reference

**Always request these tweet.fields for useful output:**
`created_at,public_metrics,author_id,conversation_id,article,note_tweet`

- `article` — returns full article body (`article.plain_text`), title, preview, and cover media for X Articles
- `note_tweet` — returns full text for long posts (>280 chars)

**Common expansions:**
- `author_id` — includes user object for the post author
- `referenced_tweets.id` — includes quoted/replied-to posts
- `attachments.media_keys` — includes media objects

**User fields:** `username,name,description,public_metrics,profile_image_url,created_at`

**Media fields:** `url,preview_image_url,type,alt_text`

For the full data dictionary, see https://docs.x.com/x-api/fundamentals/data-dictionary.md

## Pagination

Paginated endpoints return `meta.next_token`. Pass it as `pagination_token` in the next request:

```bash
curl -s "https://api.x.com/2/tweets/search/recent?query=...&pagination_token={next_token}" \
  -H "Authorization: Bearer $X_BEARER_TOKEN"
```

## Rate Limits

- Post lookup: 300 req/15min (app), 900 req/15min (user)
- User lookup: 300 req/15min (app), 900 req/15min (user)
- Search recent: 60 req/15min (app), 180 req/15min (user)
- User timeline: 1500 req/15min (app), 900 req/15min (user)

Free tier: 100 reads/month total. Check https://docs.x.com/x-api/fundamentals/rate-limits.md for current limits.

## Error Handling

- `401` — bad or expired token
- `403` — not authorized (check API tier)
- `429` — rate limited (check `x-rate-limit-reset` header)
- `404` — post/user not found or deleted

## Output Formatting

When presenting results to the user, format posts readably:

```
@username (Display Name) · 2024-01-15
Post text here...
♻️ 10  💬 5  ❤️ 100  🔁 2
```

## API Documentation

For anything not covered here, consult the official docs:
- Full docs index: https://docs.x.com/llms.txt
- Post lookup: https://docs.x.com/x-api/posts/lookup/introduction.md
- Search: https://docs.x.com/x-api/posts/search/introduction.md
- Timelines: https://docs.x.com/x-api/posts/timelines/introduction.md
- User lookup: https://docs.x.com/x-api/users/lookup/introduction.md
- Fields & expansions: https://docs.x.com/x-api/fundamentals/fields.md
- Search operators: https://docs.x.com/x-api/posts/search/integrate/operators.md

Fetch the relevant `.md` URL when you need endpoint details, query syntax, or parameter specifics.

## Self-Improvement

If you discover new patterns, gotchas, or useful query techniques while using this skill, **update this SKILL.md** with what you learned. Examples:
- A field combination that works especially well
- An undocumented quirk or error pattern
- A better way to reconstruct threads
- Changes to rate limits or API tiers

Keep this file as the living reference for X API reading.
