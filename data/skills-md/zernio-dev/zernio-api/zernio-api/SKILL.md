---
name: zernio-api
description: Official Zernio API reference for scheduling posts across 15 social media platforms and running paid ads on 7 ad networks. Covers authentication, endpoints, webhooks, ads, and platform-specific features. Use when building with the Zernio Social Media Scheduling API.
---

# Zernio API Reference

Schedule posts across 15 social media platforms and run paid ads on 7 ad networks with a single API.

**Base URL:** `https://zernio.com/api/v1`

**Docs:** [docs.zernio.com](https://docs.zernio.com)

## Quick Start

```bash
# 1. Create profile
curl -X POST https://zernio.com/api/v1/profiles \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"name": "My Brand"}'

# 2. Connect account (opens OAuth)
curl "https://zernio.com/api/v1/connect/twitter?profileId=PROFILE_ID" \
  -H "Authorization: Bearer YOUR_API_KEY"

# 3. Create post
curl -X POST https://zernio.com/api/v1/posts \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"content": "Hello!", "platforms": [{"platform": "twitter", "accountId": "ACC_ID"}], "publishNow": true}'
```

## Rule Files

Read individual rule files for detailed documentation.

**Publishing & core:**

- [rules/authentication.md](rules/authentication.md) - API key format, usage examples, core concepts
- [rules/posts.md](rules/posts.md) - Create, schedule, retry, edit, unpublish, bulk upload
- [rules/platforms.md](rules/platforms.md) - Platform-specific data for all 15 platforms
- [rules/media.md](rules/media.md) - Presigned uploads, direct upload, supported formats, platform limits
- [rules/queue.md](rules/queue.md) - Queue management, slots configuration

**Accounts & connections:**

- [rules/accounts.md](rules/accounts.md) - List accounts, health checks, per-platform helpers (Discord, TikTok creator-info, LinkedIn orgs, etc.)
- [rules/account-groups.md](rules/account-groups.md) - Group accounts for bulk operations
- [rules/connect.md](rules/connect.md) - OAuth flows, headless mode, ads connections, Bluesky/WhatsApp credentials, Telegram bot

**Paid ads:**

- [rules/ads.md](rules/ads.md) - List, boost, create, analytics, audiences, conversions (7 ad networks)

**Messaging & engagement:**

- [rules/inbox.md](rules/inbox.md) - DMs, comments, reviews, private replies, chat config
- [rules/whatsapp.md](rules/whatsapp.md) - Templates, Flows, business profile, phone numbers, group chats
- [rules/contacts.md](rules/contacts.md) - Contacts CRUD, bulk import, custom fields
- [rules/broadcasts.md](rules/broadcasts.md) - Send a single message to many contacts
- [rules/sequences.md](rules/sequences.md) - Drip sequences + comment-to-DM automations
- [rules/twitter-actions.md](rules/twitter-actions.md) - Retweet, bookmark, follow
- [rules/reddit.md](rules/reddit.md) - Reddit search and subreddit feeds

**Analytics & reporting:**

- [rules/analytics.md](rules/analytics.md) - Platform analytics, demographics, best-time, content decay, Google Business performance
- [rules/webhooks.md](rules/webhooks.md) - Configure webhooks, verify signatures, events

**Google Business management:**

- [rules/gmb.md](rules/gmb.md) - Reviews, location details, attributes, services, food menus, photos, action links

**Tools:**

- [rules/tools.md](rules/tools.md) - Media download, hashtag checker, transcripts, validators (post / media / subreddit)

**Admin:**

- [rules/users.md](rules/users.md) - Workspace users + team invite tokens
- [rules/api-keys.md](rules/api-keys.md) - API key lifecycle (create, list, revoke)
- [rules/errors.md](rules/errors.md) - Error codes, rate limits, publishing logs, usage stats
- [rules/sdks.md](rules/sdks.md) - Direct API usage examples

## Supported Platforms

**Posting (15):** Twitter/X, Instagram, Facebook, LinkedIn, TikTok, YouTube, Pinterest, Reddit, Bluesky, Threads, Google Business, Telegram, WhatsApp, Snapchat, Discord

**Ads (7):** Meta (Facebook + Instagram), Google Ads, TikTok Ads, LinkedIn Ads, Pinterest Ads, X/Twitter Ads

---

*[Zernio](https://zernio.com) - Social Media Scheduling API for Developers*
