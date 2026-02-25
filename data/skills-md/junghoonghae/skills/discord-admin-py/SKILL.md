---
name: discord-admin-py
description: Discord server administration via inference.sh - Multi-function app for channel, role, member management, messages, and more. Use for Discord bot operations, server management, channel creation, role assignment, and message handling.
---

# Discord Admin App

Multi-function Discord administration app for inference.sh.

## What It Does

- **Messages**: Send, edit, delete messages
- **Channels**: Create, list, get info
- **Roles**: Create, list, assign, remove roles
- **Members**: Get info, set nickname, ban, unban, kick
- **Guilds**: Get server information
- **Webhooks**: Create webhooks for automation

## How It Works

This is an inference.sh multi-function app. All public methods in the `App` class become callable functions.

### Adding New Functions

1. Create Input class extending `BaseAppInput`
2. Create Output class extending `BaseAppOutput`
3. Add async method to App class
4. Use `self._request(method, endpoint, data)` for API calls

## API Base

Discord API v10: `https://discord.com/api/v10`

## Example

```python
class GetInviteInput(BaseAppInput):
    invite_code: str = Field(description="Invite code")

class GetInviteOutput(BaseAppOutput):
    code: str
    guild_id: str

async def get_invite(self, input_data: GetInviteInput, metadata) -> GetInviteOutput:
    result = await self._request("GET", f"/invites/{input_data.invite_code}")
    return GetInviteOutput(code=result["code"], guild_id=result["guild"]["id"])
```

## Testing

```bash
infsh app dev --function send_message --input '{"channel_id": "123", "content": "Hello"}'
```

## Prerequisites

- inference.sh account
- Discord Bot Token from Developer Portal
- Python >= 3.11

## References

- [Discord API Docs](https://discord.com/developers/docs/reference)
- [inference.sh Multi-Function Apps](https://inference.sh/docs/extend/multi-function-apps)
