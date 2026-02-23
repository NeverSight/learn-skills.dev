---
name: omni-x402
description: AI Agent native API provider — no API keys, no signups, no subscriptions. Just pay with USDC per request via x402 to instantly access Twitter, Instagram, and more.
user-invocable: true
disable-model-invocation: false
allowed-tools:
  - "Bash(npx awal@latest *)"
  - "Bash(curl *)"
---

# omni-x402 — AI Agent Native API Provider

omni-x402 is an API provider built for the agentic era. No API keys, no signups, no monthly subscriptions. Just pay with USDC per request via the x402 protocol and instantly access Twitter, Instagram, and more.

**Traditional API providers**: Sign up → Generate API key → Subscribe to a plan → Manage rate limits → Rotate keys

**omni-x402**: Have a wallet → Call the endpoint → Pay per request. Done.

AI Agents can autonomously discover available endpoints, pay the exact cost per call, and get results — all without human intervention or pre-provisioned credentials.

## Available Endpoints

| Path | Method | Price | Description |
|------|--------|-------|-------------|
| `/user` | GET | $0.001 | Get Twitter user profile by username |
| `/user-tweets` | GET | $0.001 | Get tweets from a Twitter user by ID |
| `/get-users-v2` | GET | $0.001 | Get multiple Twitter users by IDs (comma-separated) |
| `/followings` | GET | $0.001 | Get users that a Twitter user is following |
| `/followers` | GET | $0.001 | Get followers of a Twitter user |
| `/instagram/posts` | POST | $0.001 | Get Instagram posts by username |
| `/instagram/profile` | POST | $0.001 | Get Instagram profile by username |

**Server URL**: `https://omniapi-production-7de2.up.railway.app`

## Prerequisites & Setup

### 1. awal CLI Authentication

The awal CLI (`npx awal@latest`) handles wallet operations and x402 payments. You must authenticate before making paid API calls.

**Check status**:

```bash
npx awal@latest status
```

If not authenticated, use the email OTP flow:

```bash
# Step 1: Send OTP to your email
npx awal@latest auth login user@example.com
# Output: flowId: abc123...

# Step 2: Verify with the 6-digit code from email
npx awal@latest auth verify abc123 123456

# Confirm authentication
npx awal@latest status
```

See the `authenticate-wallet` skill for details.

### 2. Fund the Wallet

Check your USDC balance:

```bash
npx awal@latest balance
```

If insufficient, fund via Coinbase Onramp:

```bash
npx awal@latest show
```

This opens the wallet companion UI where you can fund with Apple Pay, debit card, bank transfer, or Coinbase account. Alternatively, send USDC on Base directly to your wallet address:

```bash
npx awal@latest address
```

See the `fund` skill for details.

### Summary

| Requirement | Check | Skill |
|---|---|---|
| Wallet authenticated | `npx awal@latest status` | `authenticate-wallet` |
| USDC balance | `npx awal@latest balance` | `fund` |

## Usage

All requests are made via `npx awal@latest x402 pay`, which handles USDC payment automatically.

### Twitter — Get User Profile

```bash
npx awal@latest x402 pay "https://omniapi-production-7de2.up.railway.app/user?username=elonmusk"
```

### Twitter — Get User Tweets

```bash
npx awal@latest x402 pay "https://omniapi-production-7de2.up.railway.app/user-tweets?user=44196397&count=20"
```

The `user` parameter is the Twitter user ID (numeric). Use the `/user` endpoint first to get the ID from a username.

### Twitter — Get Multiple Users

```bash
npx awal@latest x402 pay "https://omniapi-production-7de2.up.railway.app/get-users-v2?users=44196397,50393960"
```

Accepts comma-separated user IDs.

### Twitter — Get Followings

```bash
npx awal@latest x402 pay "https://omniapi-production-7de2.up.railway.app/followings?user=44196397&count=20"
```

### Twitter — Get Followers

```bash
npx awal@latest x402 pay "https://omniapi-production-7de2.up.railway.app/followers?user=44196397&count=20"
```

### Instagram — Get Posts

```bash
npx awal@latest x402 pay "https://omniapi-production-7de2.up.railway.app/instagram/posts" -X POST -d '{"username": "instagram"}'
```

### Instagram — Get Profile

```bash
npx awal@latest x402 pay "https://omniapi-production-7de2.up.railway.app/instagram/profile" -X POST -d '{"username": "instagram"}'
```

**Note**: Instagram endpoints use POST with a JSON body. Use `-X POST -d '{...}'` to send the request body.

## Response Examples

### Twitter User Profile (`/user`)

```json
{
  "result": {
    "id": "44196397",
    "name": "Elon Musk",
    "screen_name": "elonmusk",
    "description": "...",
    "followers_count": 200000000,
    "friends_count": 800,
    "statuses_count": 50000,
    "profile_image_url_https": "https://pbs.twimg.com/..."
  }
}
```

### Twitter User Tweets (`/user-tweets`)

```json
{
  "result": {
    "timeline": {
      "instructions": [
        {
          "entries": [
            {
              "content": {
                "tweet_results": {
                  "result": {
                    "legacy": {
                      "full_text": "...",
                      "created_at": "...",
                      "favorite_count": 100,
                      "retweet_count": 50
                    }
                  }
                }
              }
            }
          ]
        }
      ]
    }
  }
}
```

### Instagram Profile (`/instagram/profile`)

```json
{
  "result": {
    "username": "instagram",
    "full_name": "Instagram",
    "biography": "...",
    "follower_count": 500000000,
    "following_count": 500,
    "media_count": 7000,
    "profile_pic_url": "https://..."
  }
}
```

### Instagram Posts (`/instagram/posts`)

```json
{
  "result": {
    "items": [
      {
        "caption": { "text": "..." },
        "like_count": 1000000,
        "comment_count": 50000,
        "image_versions": { "items": [{ "url": "https://..." }] },
        "taken_at": 1700000000
      }
    ]
  }
}
```

## Service Catalog

Retrieve the full list of available endpoints and their prices:

```bash
curl https://omniapi-production-7de2.up.railway.app/catalog
```

Returns:

```json
[
  { "path": "/user", "method": "GET", "price": "$0.001", "description": "Get Twitter user profile by username" },
  { "path": "/user-tweets", "method": "GET", "price": "$0.001", "description": "Get tweets from a Twitter user by ID" },
  { "path": "/get-users-v2", "method": "GET", "price": "$0.001", "description": "Get multiple Twitter users by IDs (comma-separated)" },
  { "path": "/followings", "method": "GET", "price": "$0.001", "description": "Get users that a Twitter user is following" },
  { "path": "/followers", "method": "GET", "price": "$0.001", "description": "Get followers of a Twitter user" },
  { "path": "/instagram/posts", "method": "POST", "price": "$0.001", "description": "Get Instagram posts by username" },
  { "path": "/instagram/profile", "method": "POST", "price": "$0.001", "description": "Get Instagram profile by username" }
]
```

## Health Check

```bash
curl https://omniapi-production-7de2.up.railway.app/health
```

Returns: `{"status": "ok"}`

## Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| HTTP 402 | Payment required | Use `npx awal@latest x402 pay` instead of plain `curl` to make the request |
| HTTP 502 | Upstream API error | The backend service may be temporarily unavailable. Retry after a few seconds |
| `"not signed in"` | Wallet not authenticated | Run `npx awal@latest auth login <email>` to authenticate. See `authenticate-wallet` skill |
| `"insufficient balance"` | Not enough USDC | Run `npx awal@latest show` to fund the wallet. See `fund` skill |
| Empty response | Invalid parameters | Check query parameters — e.g. `/user` requires `?username=`, `/user-tweets` requires `?user=` (numeric ID) |
| Instagram 400 | Missing request body | Instagram endpoints require POST with JSON body: `-X POST -d '{"username": "..."}'` |
