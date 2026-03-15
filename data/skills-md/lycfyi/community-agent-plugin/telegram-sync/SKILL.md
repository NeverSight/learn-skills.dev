---
name: telegram-sync
description: "Sync Telegram messages to local storage. Use when user asks to sync, pull, fetch, or download Telegram messages."
---

# telegram-sync

Sync Telegram messages to local Markdown storage.

## Trigger Phrases

- "sync Telegram"
- "pull from Telegram"
- "fetch Telegram messages"
- "download Telegram history"
- "telegram sync"
- "sync my Telegram DMs"

## Description

This skill downloads messages from Telegram groups and DMs to local Markdown files. Messages are stored in an LLM-friendly format that can be easily read and analyzed.

**DMs are synced by default.** Use `--no-dms` to sync groups only.

## Usage

### Basic Sync (Groups + DMs)

Sync all (groups + DMs, last 7 days):
```bash
python ${CLAUDE_PLUGIN_ROOT}/tools/telegram_sync.py
```

Sync groups only (exclude DMs):
```bash
python ${CLAUDE_PLUGIN_ROOT}/tools/telegram_sync.py --no-dms
```

### Sync Specific Group

```bash
python ${CLAUDE_PLUGIN_ROOT}/tools/telegram_sync.py --group 1234567890
```

### Sync Specific DM

```bash
python ${CLAUDE_PLUGIN_ROOT}/tools/telegram_sync.py --dm 123456789
```

### Time Range

Sync last 30 days:
```bash
python ${CLAUDE_PLUGIN_ROOT}/tools/telegram_sync.py --days 30
```

Full sync (ignore previous state):
```bash
python ${CLAUDE_PLUGIN_ROOT}/tools/telegram_sync.py --full
```

### Forum Topics

Sync specific topic in a forum group:
```bash
python ${CLAUDE_PLUGIN_ROOT}/tools/telegram_sync.py --group 1234567890 --topic 5
```

### Custom Limits

Sync with custom message limit for groups:
```bash
python ${CLAUDE_PLUGIN_ROOT}/tools/telegram_sync.py --days 30 --limit 5000
```

Sync with custom DM limit (default is 100 for privacy):
```bash
python ${CLAUDE_PLUGIN_ROOT}/tools/telegram_sync.py --dm-limit 500
```

## Message Limits

### Group Limit (`--limit`)
- Default: 2000 (configurable in `config/agents.yaml`)
- Use higher limits for longer lookback periods
- Example: `--days 90 --limit 10000` for 90-day archive

### DM Limit (`--dm-limit`)
- Default: 100 (privacy-conscious default)
- Lower than group limit by design
- Increase manually if needed: `--dm-limit 500`

## Sync Modes

### Incremental Sync (default)
- Only fetches messages newer than the last sync
- Fast and efficient for regular updates
- Uses the `last_message_id` from sync state

### Full Sync (--full)
- Ignores previous sync state
- Downloads all messages within the date range
- Use when you want a fresh start

## Output

### Groups

Group messages are saved to:
```
data/{group_id}-{slug}/messages.md
data/{group_id}-{slug}/sync_state.yaml
data/{group_id}-{slug}/group.yaml
```

For forum groups with topics:
```
data/{group_id}-{slug}/{topic_name}/messages.md
```

### DMs

DM messages are saved to a separate directory:
```
dms/telegram/{user_id}-{name}/messages.md
dms/telegram/{user_id}-{name}/sync_state.yaml
dms/telegram/{user_id}-{name}/user.yaml
dms/telegram/manifest.yaml
```

## Rate Limiting

Telegram has strict rate limits. The sync tool:
- Adds delays between requests (100ms minimum)
- Handles FloodWait errors automatically
- Shows progress during sync

If rate limited, you'll see the wait time and can retry later.

## Message Format

```markdown
## 2026-01-06

### 10:30 AM - @alice (123456)
Hello everyone!

### 10:31 AM - @bob (789012)
↳ replying to @alice:
Hey there!

[photo: vacation.jpg (1.2MB)]

Reactions: heart 5 | thumbsup 3
```

## Exit Codes

- `0` - Success
- `1` - Authentication error
- `2` - Group not found or permission denied
- `3` - Rate limited

## Troubleshooting

### "Could not find the input entity" Error

**Error message:**
```
Could not find the input entity for PeerUser(user_id=...) (PeerUser)
```

**What this means:** Telethon (the Telegram library) doesn't have this group cached locally. It needs to know the group's "access hash" which is typically cached when you interact with the group.

**Solutions (try in order):**

1. **Run telegram-list first** to refresh the entity cache:
   ```bash
   python ${CLAUDE_PLUGIN_ROOT}/tools/telegram_list.py
   ```
   This iterates through all your dialogs and caches the entities.

2. **Use the exact ID from telegram-list output:**
   ```bash
   # First, list groups to get correct IDs
   python ${CLAUDE_PLUGIN_ROOT}/tools/telegram_list.py

   # Then sync using the ID shown
   python ${CLAUDE_PLUGIN_ROOT}/tools/telegram_sync.py --group <ID_FROM_LIST>
   ```

3. **Open the group in Telegram app:**
   - Open the Telegram desktop or mobile app
   - Navigate to the group you want to sync
   - Send a message or just open the chat
   - This forces Telegram to cache the entity
   - Then retry the sync

4. **For supergroups/channels:** Make sure you're using the correct ID format. Supergroup IDs are typically positive integers (not negative).

### "No group specified" Error

**Error message:**
```
No group specified and no default group configured.
```

**Solution:** Either specify a group ID or set a default:

```bash
# Option 1: Specify group directly
python ${CLAUDE_PLUGIN_ROOT}/tools/telegram_sync.py --group 1234567890

# Option 2: Set a default group
python ${CLAUDE_PLUGIN_ROOT}/tools/telegram_init.py --group 1234567890
```

### Permission Denied (Exit Code 2)

**Possible causes:**
- You're not a member of the group
- The group is private
- You've been banned from the group
- Admin permissions are required

**Solution:** Check your membership status in the Telegram app.

### Rate Limited (Exit Code 3)

**Error message:**
```
Rate limited: Wait X seconds.
```

**Solution:** Wait the specified time before retrying. Telegram rate limits are strict and cannot be bypassed.

## Related Skills

- `telegram-init` - Initialize Telegram connection
- `telegram-list` - List groups and topics
- `telegram-read` - Read synced messages
