---
name: twitter-to-binance-square
description: |
  Auto-mirror Twitter/X content to Binance Square.
  Monitors specified Twitter accounts or topics, fetches new tweets,
  transforms content, and posts to Binance Square automatically.
  Auto-run on messages like 'mirror twitter to binance square', 'auto post from twitter', 'start twitter mirror'.
user-invocable: true
allowed-tools: Read, Bash, Grep, Glob
---

# Twitter to Binance Square Auto-Mirror Skill

## Overview

Automatically fetch tweets from specified Twitter accounts or keyword searches, transform the content for Binance Square, and post them. Designed for building automation pipelines with configurable polling intervals and deduplication.

- Automation script: [scripts/auto_mirror.py](scripts/auto_mirror.py)
- Config template: [mirror_config.example.json](mirror_config.example.json)
- Usage guide: [README.md](README.md)

---

## Prerequisites

| Item | Description | How to get |
|------|-------------|------------|
| `TWITTER_TOKEN` | 6551 API Bearer token | 访问 https://6551.io/mcp 注册获取 |
| `SQUARE_API_KEY` | Binance Square OpenAPI Key | 登录币安 → 访问 [创作者中心](https://www.binance.com/zh-CN/square/creator-center/home) → 页面右侧「查看 API」申请 |

---

## Core Workflow

```
┌─────────────────────────────────────────────┐
│  1. FETCH: Get tweets from Twitter/X        │
│     - By account: monitor specific users    │
│     - By topic: keyword/hashtag search      │
├─────────────────────────────────────────────┤
│  2. FILTER: Deduplicate & quality check     │
│     - Skip already-posted tweet IDs         │
│     - Skip retweets / replies (optional)    │
│     - Min engagement threshold (optional)   │
├─────────────────────────────────────────────┤
│  3. TRANSFORM: Adapt content for Square     │
│     - Add source attribution                │
│     - Translate if needed                   │
│     - Add relevant #hashtags               │
│     - Trim to Square length limits          │
├─────────────────────────────────────────────┤
│  4. POST: Publish to Binance Square         │
│     - Call Square API                       │
│     - Record posted tweet ID               │
│     - Log post URL                          │
├─────────────────────────────────────────────┤
│  5. WAIT: Sleep for configured interval     │
│     - Default: 300 seconds (5 minutes)      │
│     - Respect daily post limits             │
└─────────────────────────────────────────────┘
```

---

## API Reference

### Step 1: Fetch Tweets

#### Option A: Monitor Specific Account

```bash
curl -s -X POST "https://ai.6551.io/open/twitter_user_tweets" \
  -H "Authorization: Bearer $TWITTER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "TARGET_USERNAME",
    "maxResults": 10,
    "product": "Latest",
    "includeReplies": false,
    "includeRetweets": false
  }'
```

#### Option B: Monitor Topic/Keywords

```bash
curl -s -X POST "https://ai.6551.io/open/twitter_search" \
  -H "Authorization: Bearer $TWITTER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": "TOPIC_KEYWORDS",
    "minLikes": 50,
    "product": "Top",
    "maxResults": 10,
    "lang": "en"
  }'
```

#### Option C: Monitor Hashtag

```bash
curl -s -X POST "https://ai.6551.io/open/twitter_search" \
  -H "Authorization: Bearer $TWITTER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "hashtag": "bitcoin",
    "minLikes": 100,
    "product": "Top",
    "maxResults": 10
  }'
```

### Step 2: Post to Binance Square

```bash
curl -s -X POST "https://www.binance.com/bapi/composite/v1/public/pgc/openApi/content/add" \
  -H "X-Square-OpenAPI-Key: $SQUARE_API_KEY" \
  -H "Content-Type: application/json" \
  -H "clienttype: binanceSkill" \
  -d '{
    "bodyTextOnly": "TRANSFORMED_CONTENT"
  }'
```

---

## Content Transformation Rules

When transforming a tweet for Binance Square, apply the following rules:

### Template Format

```
{transformed_content}

Source: @{username} on X              ← optional (show_source=true)
Publish by using 6551 twitter mirror tool   ← default enabled (show_tool_attribution=true)
{#hashtag1} {#hashtag2} {#hashtag3}
```

### Transformation Steps

1. **Extract core message**: Keep the tweet's main content
2. **Remove Twitter-specific elements**: Remove @mentions (except source attribution), remove t.co links
3. **Tool attribution (default)**: Append `Publish by using 6551 twitter mirror tool` — controlled by `show_tool_attribution` (default: true)
4. **Source attribution (optional)**: Credit the original author with `Source: @username on X` — controlled by `show_source` (default: true)
5. **Preserve hashtags**: Keep original hashtags, add relevant crypto hashtags if missing
6. **Language handling**: If `translate` is enabled, translate to the target language while preserving technical terms
7. **Length check**: Binance Square has content length limits; trim if needed (keep under 2000 chars)

### Example Transformation

**Original Tweet** by @VitalikButerin:
```
Excited about the new EIP-4844 progress. Proto-danksharding will reduce L2 fees by 10-100x.
This is huge for Ethereum scalability. https://t.co/xxx
```

**Transformed for Binance Square** (show_source=true, show_tool_attribution=true):
```
Vitalik Buterin 对 EIP-4844 的最新进展感到兴奋。Proto-danksharding 将把 L2 费用降低 10-100 倍，这对以太坊的可扩展性意义重大。

Source: @VitalikButerin on X
Publish by using 6551 twitter mirror tool
#Ethereum #EIP4844 #L2 #Crypto
```

**Transformed for Binance Square** (show_source=false, show_tool_attribution=true):
```
Vitalik Buterin 对 EIP-4844 的最新进展感到兴奋。Proto-danksharding 将把 L2 费用降低 10-100 倍，这对以太坊的可扩展性意义重大。

Publish by using 6551 twitter mirror tool
#Ethereum #EIP4844 #L2 #Crypto
```

---

## Configuration Schema

The automation script uses a JSON config file (see [mirror_config.example.json](mirror_config.example.json)):

```json
{
  "mode": "account",
  "accounts": ["VitalikButerin", "cabornedefi"],
  "keywords": "",
  "hashtag": "",
  "poll_interval_seconds": 300,
  "min_likes": 0,
  "min_retweets": 0,
  "max_posts_per_run": 5,
  "include_replies": false,
  "include_retweets": false,
  "translate": false,
  "translate_to": "zh",
  "content_template": "{content}\n\n{source_attribution}\n{tool_attribution}\n{hashtags}",
  "show_source": true,
  "show_tool_attribution": true,
  "add_hashtags": ["Crypto", "Web3"],
  "state_file": "mirror_state.json",
  "dry_run": false
}
```

### Config Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `mode` | string | `"account"` | `"account"` = monitor users, `"search"` = keyword search, `"hashtag"` = hashtag search |
| `accounts` | string[] | `[]` | Twitter usernames to monitor (mode=account) |
| `keywords` | string | `""` | Search keywords (mode=search) |
| `hashtag` | string | `""` | Hashtag to monitor (mode=hashtag) |
| `poll_interval_seconds` | int | `300` | Seconds between each polling cycle |
| `min_likes` | int | `0` | Minimum likes to qualify for mirroring |
| `min_retweets` | int | `0` | Minimum retweets to qualify |
| `max_posts_per_run` | int | `5` | Max posts per polling cycle |
| `include_replies` | bool | `false` | Include reply tweets |
| `include_retweets` | bool | `false` | Include retweets |
| `translate` | bool | `false` | Translate content before posting |
| `translate_to` | string | `"zh"` | Target language for translation |
| `content_template` | string | see above | Template for Square post content |
| `show_source` | bool | `true` | Show `Source: @username on X` attribution |
| `show_tool_attribution` | bool | `true` | Show `Publish by using 6551 twitter mirror tool` |
| `add_hashtags` | string[] | `[]` | Extra hashtags to append |
| `state_file` | string | `"mirror_state.json"` | File to track posted tweet IDs |
| `dry_run` | bool | `false` | If true, print content but don't post |

---

## State Management

The script maintains a `mirror_state.json` to track posted tweets:

```json
{
  "posted_tweet_ids": ["1234567890", "1234567891"],
  "last_poll_time": "2026-03-07T10:00:00Z",
  "post_count_today": 5,
  "last_reset_date": "2026-03-07",
  "post_log": [
    {
      "tweet_id": "1234567890",
      "square_post_id": "298177291743282",
      "square_url": "https://www.binance.com/square/post/298177291743282",
      "username": "VitalikButerin",
      "posted_at": "2026-03-07T10:05:00Z"
    }
  ]
}
```

---

## Error Handling

| Scenario | Action |
|----------|--------|
| Twitter API fails | Log error, retry next cycle |
| Square API returns 20002/20022 (sensitive words) | Log & skip this tweet, continue |
| Square API returns 220009 (daily limit, max 100 posts/day) | Stop posting, wait until next day |
| Square API returns 220004 (key expired) | Stop and alert user |
| Tweet already posted (duplicate ID) | Skip silently |
| Network error | Retry with exponential backoff (max 3 retries) |

---

## Agent Behavior

1. **Verify credentials first**: Check both `TWITTER_TOKEN` and `SQUARE_API_KEY` exist before starting
2. **Prompt for missing config**: If mode/accounts/keywords not specified, ask the user
3. **Show preview before first post**: On the first run, show the first transformed tweet and ask for confirmation
4. **Respect rate limits**: Honor poll_interval_seconds and max_posts_per_run
5. **Daily limit awareness**: Track daily post count, stop when approaching Binance Square daily limit
6. **Deduplication**: Never post the same tweet ID twice (persisted in state_file)
7. **Graceful shutdown**: On interrupt, save state before exiting
8. **Logging**: Print each action (fetch, skip, transform, post) with timestamps
9. **Run script via**: `python3 scripts/auto_mirror.py`

---

## Usage Examples

### Example 1: Mirror a specific KOL's tweets

```
User: Mirror VitalikButerin's tweets to my Binance Square
Agent: I'll set up auto-mirroring for @VitalikButerin → Binance Square.

Config:
- Mode: account
- Account: VitalikButerin
- Poll interval: 5 minutes
- Translate: No

Let me fetch the latest tweets first to preview...

[Fetches and shows latest tweet]

Here's how the first post would look on Binance Square:

---
Excited about the new EIP-4844 progress...

Source: @VitalikButerin on X
Publish by using 6551 twitter mirror tool
#Ethereum #Crypto
---

Shall I start the auto-mirror with these settings?
```

### Example 2: Mirror tweets about a trending topic

```
User: Auto-post trending Bitcoin tweets to Binance Square, minimum 500 likes
Agent: I'll monitor Twitter for popular Bitcoin tweets and mirror them to Binance Square.

Config:
- Mode: search
- Keywords: "bitcoin"
- Min likes: 500
- Poll interval: 10 minutes

Starting monitor...
```

### Example 3: Run as automated script

```bash
# Set environment variables
export TWITTER_TOKEN="your_6551_token"
export SQUARE_API_KEY="your_square_key"

# Run with config file
python3 scripts/auto_mirror.py --config mirror_config.json

# Run with CLI args
python3 scripts/auto_mirror.py \
  --mode account \
  --accounts VitalikButerin,elonmusk \
  --interval 300 \
  --translate \
  --translate-to zh
```

---

## Security

- **Never display full API keys**: Show masked as `abc12...xyz9`
- **State file contains no secrets**: Only tweet IDs and post logs
- **Environment variables for secrets**: Never store keys in config files

## Notes

1. Binance Square 每日最多发帖 100 条 — the script tracks and respects this limit
2. Content may be flagged as sensitive by Binance — those tweets are skipped automatically
3. The 6551 API has rate limits — max 100 results per request
4. Always attribute the original author to comply with content policies
