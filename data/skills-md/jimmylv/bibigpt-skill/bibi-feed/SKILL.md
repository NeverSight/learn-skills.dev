---
name: bibi-feed
description: >
  Subscribe to YouTube / Bilibili / podcast channels in BibiGPT, pull the
  latest feed, and mark items seen. Use when the user wants channel
  subscriptions, "what's new in my feed", a daily digest, or to subscribe /
  unsubscribe. Do not use to summarize a new URL (`bibi`), search already
  saved videos (`bibi-library`), or analyze frames / mind maps (`bibi-vision`).
  Triggers: "subscribe to this channel", "what's new in my subscriptions",
  "daily digest", "mark feed seen", "订阅频道", "我的订阅", "有什么更新",
  "取消订阅", "latest feed".
  Same `bibi` CLI binary and same BibiGPT account as the other skills.
agent_created: true
---

# BibiGPT Feed — channels, latest, mark seen

This skill is the subscription half of BibiGPT. **Same CLI (`bibi`), same account**
as `bibi` / `bibi-library` / `bibi-vision`. It does not summarize a fresh URL.

Landing: https://bibigpt.co/mcp · Install: https://bibigpt.co/agent · Quota: see `references/auth.md`

## When to use / when not

| Use this skill | Use a sibling instead |
|----------------|------------------------|
| List / subscribe / unsubscribe channels | New URL summary → `bibi` |
| Latest videos across subscriptions | Search *saved* library → `bibi-library` |
| Mark feed seen | Frames / mind map → `bibi-vision` |
| Preview a channel's videos before subscribing | |

## 1. Detect mode

Run `scripts/bibi-check.sh` if present. Prefer CLI (`command -v bibi`), else `$BIBI_API_TOKEN`, else MCP `https://bibigpt.co/api/mcp`. Details: `references/auth.md`.

## 2. Intent routing

| User intent | Workflow |
|-------------|---------|
| List / subscribe / unsubscribe / channel videos | → `workflows/channels-manage.md` |
| What's new, daily digest, latest feed | → `workflows/feed-latest.md` |

## 3. Minimum commands (CLI)

```bash
bibi channels list --json
bibi channels subscribe --channelUrl "https://www.youtube.com/@..." --json
bibi feed --json
bibi feed-mark-seen --json
```

Full flags: `references/cli.md`. MCP names: `list_channels`, `subscribe_channel`, `unsubscribe_channel`, `get_channel_videos`, `get_latest_feed`, `get_channel_health`, `mark_feed_seen`.
