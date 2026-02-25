---
name: discord
description: |
  Send Discord messages via direct API. Use when:
  (1) Cross-channel messaging (Telegram→Discord, Slack→Discord)
  (2) OpenClaw native gives "Cross-context messaging denied"
  Uses $DISCORD_BOT_TOKEN - no Composio needed.
---

# Discord Direct API

Native OpenClaw Discord is session-bound. For cross-channel, use direct API.

## Send Message

```bash
curl -X POST "https://discord.com/api/v10/channels/$CHANNEL_ID/messages" \
  -H "Authorization: Bot $DISCORD_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content": "<@USER_ID> message"}'
```

## Get Channel ID

```bash
curl "https://discord.com/api/v10/guilds/$GUILD_ID/channels" \
  -H "Authorization: Bot $DISCORD_BOT_TOKEN" | jq '.[] | {id, name}'
```

## Get User ID

```bash
curl "https://discord.com/api/v10/guilds/$GUILD_ID/members?limit=100" \
  -H "Authorization: Bot $DISCORD_BOT_TOKEN" | jq '.[] | {id: .user.id, name: .user.username}'
```

## Mentions

`<@USER_ID>` = notified. `@Name` = ignored.
