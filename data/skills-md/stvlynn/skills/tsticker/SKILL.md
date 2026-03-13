---
name: tsticker
description: Manage Telegram sticker packs via tsticker CLI. Init, push, sync, download, and trace sticker packs. Use when user wants to create/update Telegram sticker packs, push stickers to Telegram, sync packs, or manage sticker collections. Integrates with create-sticker for end-to-end sticker generation → publish workflow.
---

# tsticker — Telegram Sticker Pack Manager

## Prerequisites

- `tsticker` installed via `pipx install tsticker --python python3.13 --pip-args="--ignore-requires-python"`
- `ffmpeg` and `ImageMagick` installed (for animated sticker conversion)
- Telegram Bot Token (from @BotFather) + owner user ID

## Auth

```bash
tsticker login -t <BOT_TOKEN> -u <USER_ID>
```

Credentials stored via system keyring.

## Commands

| Command | Description |
|---------|-------------|
| `tsticker init -s regular -n 'pack_name' -t 'Pack Title'` | Create new sticker pack |
| `tsticker push` | Push local stickers → overwrite cloud pack |
| `tsticker sync` | Pull cloud pack → overwrite local files |
| `tsticker download -l <sticker_link>` | Download any pack (read-only) |
| `tsticker trace -l <sticker_link>` | Import pack (editable, must be your bot's pack) |
| `tsticker show` | Show local pack info |

## Sticker Pack Directory Structure

```
<pack_dir>/
├── index.json          # Pack metadata (only `title` is editable)
└── stickers/           # Put images here
    ├── 😄hello.png     # Emoji in filename = explicit emoji
    ├── coffee.png       # No emoji = auto-detected
    └── animation.gif    # Auto-converted to webm
```

## Workflow: Generate → Publish

### 1. Create pack (first time only)

```bash
cd ~/Pictures/lynn-stickers
tsticker init -s regular -n 'lynn_stickers_by_<bot_name>' -t 'Lynn Stickers'
```

### 2. Generate stickers (create-sticker skill)

```bash
python3 /path/to/skills/skills/create-sticker/scripts/create_sticker.py "drinking bubble tea happily"
```

### 3. Copy approved stickers into pack

```bash
cp ~/stickers/drinking_bubble_tea.png ~/Pictures/lynn-stickers/stickers/🧋drinking_tea.png
```

Emoji prefix in filename sets the sticker's emoji. Without prefix, tsticker auto-selects.

### 4. Push to Telegram

```bash
cd ~/Pictures/lynn-stickers
tsticker push
```

⚠️ `push` **overwrites** the entire cloud pack with local files. Always `sync` first if cloud has changes you want to keep.

## Notes

- Rate limited: ~2s per sticker operation
- Don't push too many stickers at once — errors break the flow, recover with `tsticker sync`
- Sticker types: `regular` (static/animated), `mask`, `custom_emoji`
- Supported formats: png, jpg, gif, webm, mov (auto-converted)
- Bot can only manage packs it created — losing the bot means manual management only
