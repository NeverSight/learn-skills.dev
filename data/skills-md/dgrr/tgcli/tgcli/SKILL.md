---
name: tgcli
description: Telegram CLI for syncing, searching, sending messages, and managing chats. Pure Rust implementation with no TDLib dependency. Supports multi-account setups, local FTS5 search, media download, scheduled messages, and real-time daemon mode. Use for interacting with Telegram from the command line or in scripts.
---

# tgcli – Telegram CLI

Pure Rust Telegram client. No TDLib. Fast. Cross-platform.

## Quick Start

```bash
tgcli auth                     # Authenticate (first time)
tgcli sync                     # Incremental sync
tgcli chats list --output markdown      # List chats (markdown recommended)
tgcli messages list --chat 987654321 --output markdown  # List messages from chat
tgcli send --to 123456789 --message "Hello there!"  # Send message
```

## Core Commands

### Sync

Fetch updates from Telegram servers. Always incremental (skips duplicates).

```bash
tgcli sync                     # Default (shows summary)
tgcli sync -q                  # Quiet (no output)
tgcli sync --full              # Full sync (all messages)
tgcli sync --download-media    # Save media files
tgcli sync --stream            # JSONL streaming (for pipelines)
```

### Chats

Manage chats: list, search, archive, pin, mute, create groups, join, leave.

```bash
tgcli chats list --output markdown           # List (markdown recommended)
tgcli chats list --limit 50                  # Limit results
tgcli chats search "DevTeam"                 # Search by name
tgcli chats archive 987654321                # Archive specific chat
tgcli chats pin 987654321                    # Pin chat
tgcli chats mute 987654321                   # Mute notifications
tgcli chats create --group "Project Alpha" --user 111222333  # Create group
tgcli chats join https://t.me/joinchat/...   # Join via invite link
tgcli chats leave 987654321                  # Leave chat
```

### Messages

List, search, show, download, delete messages. Supports forum topics.

```bash
tgcli messages list --chat 987654321 --output markdown  # List messages (markdown)
tgcli messages list --chat 987654321 --limit 100        # Limit to 100 messages
tgcli messages list --chat 987654321 --topic 42         # Forum topic messages
tgcli messages search "project deadline" --output markdown  # Local search (markdown)
tgcli messages search --global "urgent task"               # Telegram API search
tgcli messages show --chat 987654321 --message 4567       # Show specific message
tgcli messages context --chat 987654321 --message 4567    # Show with context
tgcli messages download --chat 987654321 --message 4567   # Download media
tgcli messages delete --chat 987654321 --message 4567     # Delete message
```

### Send

Send messages, files, voice/video notes, scheduled messages, replies.

```bash
tgcli send --to 123456789 --message "Hello from tgcli"      # Text message
tgcli send --to 123456789 --file report.pdf                  # Send file
tgcli send --to 123456789 --voice note.ogg                   # Voice message
tgcli send --to 123456789 --video video.mp4                  # Video note
tgcli send --to 123456789 --message "Meeting tomorrow" --schedule "tomorrow 9am"  # Scheduled
tgcli send --to 123456789 --message "Agreed" --reply-to 5678 # Reply to message
```

### Contacts

List and search contacts.

```bash
tgcli contacts list --output markdown   # List contacts (markdown)
tgcli contacts search "Alice"           # Search by name
```

### Users

Show user info, block/unblock.

```bash
tgcli users show 123456789      # Show user profile
tgcli users block 123456789     # Block user
tgcli users unblock 123456789   # Unblock user
```

### Stickers

List, search, and send stickers.

```bash
tgcli stickers list --output markdown   # List sticker packs (markdown)
tgcli stickers search "cat"             # Search sticker sets
tgcli stickers send --to 123456789 --sticker CAT_ABC123  # Send sticker
```

### Folders

Create and manage chat folders.

```bash
tgcli folders list --output markdown   # List folders (markdown)
tgcli folders create "Work Chats"      # Create new folder
tgcli folders delete 5                 # Delete folder by ID
```

### Admin (Groups/Channels)

Ban, kick, promote, demote members.

```bash
tgcli admin ban --chat 111222333 --user 999888777       # Ban user
tgcli admin kick --chat 111222333 --user 999888777      # Kick user
tgcli admin unban --chat 111222333 --user 999888777     # Unban user
tgcli admin promote --chat 111222333 --user 999888777   # Promote to admin
tgcli admin demote --chat 111222333 --user 999888777    # Demote admin
```

### Daemon (Real-Time)

Listen for real-time updates from Telegram servers. Optional — use `sync` for most workflows.

```bash
tgcli daemon                    # Listen for updates
tgcli daemon --stream           # JSONL output
tgcli daemon --no-backfill      # Skip background sync
tgcli daemon --ignore 987654321 # Ignore specific chat
tgcli daemon --ignore-channels  # Skip all channels
```

### Other

```bash
tgcli read --chat 987654321              # Mark chat as read
tgcli typing --chat 987654321            # Send typing indicator
tgcli profile show                       # Show your profile
tgcli profile set --first-name "Alex"    # Update your name
tgcli completions bash                   # Shell completions
tgcli wipe                               # Reset database (keeps auth)
```

## Multi-Account

Use `--store` to manage multiple Telegram accounts:

```bash
tgcli --store ~/.tgcli-personal sync
tgcli --store ~/.tgcli-work chats list --output markdown
tgcli --store ~/.tgcli-bot messages list --chat 987654321
```

## Output Formats

Always use **markdown** when available (recommended for LLMs and piping):

```bash
tgcli chats list                    # Human-readable table (default)
tgcli chats list --output markdown  # Markdown (recommended for LLMs/pipes)
tgcli chats list --output json      # JSON for parsing
```

**Markdown advantages:**
- Readable structure (headers, bullet points, dividers)
- Pipe to ripgrep/grep for filtering
- Feed to LLMs for processing
- Consistent across commands

## Storage

Data stored in `--store` directory (default `~/.tgcli/`):

```
~/.tgcli/session.db    # Telegram session & authentication
~/.tgcli/tgcli.db      # Messages, chats, contacts (FTS5-indexed)
~/.tgcli/media/        # Downloaded media files
```

## Tips & Tricks

**Search messages with ripgrep:**

```bash
tgcli messages list --chat 987654321 --output markdown | rg "keyword"
```

**Export to markdown file:**

```bash
tgcli messages list --chat 987654321 --output markdown > exported.md
```

**Sync multiple accounts in parallel:**

```bash
for account in personal work bot; do
  tgcli --store ~/.tgcli-$account sync -q &
done
wait
```

## Links

- GitHub: https://github.com/dgrr/tgcli
- Crates.io: https://crates.io/crates/tgcli
