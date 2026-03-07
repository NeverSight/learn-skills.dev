---
name: setup
description: "One-time bootstrap for Kokoro TTS, Telegram bot, and BotFather setup. TRIGGERS - tts setup, kokoro install, telegram bot setup, tts bootstrap, voice synthesis setup."
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, TodoWrite, TodoRead, AskUserQuestion
argument-hint: "[--check|--install]"
disable-model-invocation: true
---

# TTS Telegram Sync Setup

Full-stack bootstrap: Kokoro TTS engine, Telegram bot, BotFather token, secrets, symlinks.

## Prerequisites

| Component   | Required | Check                                   |
| ----------- | -------- | --------------------------------------- |
| Bun         | Yes      | `bun --version`                         |
| mise        | Yes      | `mise --version`                        |
| uv          | Yes      | `uv --version`                          |
| Python 3.13 | Yes      | `uv run --python 3.13 python --version` |
| Homebrew    | Yes      | `brew --version`                        |

## Workflow

### Step 1: Preflight

```bash
/usr/bin/env bash << 'PREFLIGHT_EOF'
echo "=== TTS Telegram Sync Preflight ==="
for cmd in bun mise uv brew; do
    if command -v "$cmd" &>/dev/null; then
        echo "  [OK] $cmd: $($cmd --version 2>&1 | head -1)"
    else
        echo "  [FAIL] $cmd not found"
    fi
done
PREFLIGHT_EOF
```

### Step 2: Kokoro Install

Run the Kokoro TTS engine installer:

```bash
PLUGIN_DIR="${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/plugins/marketplaces/cc-skills/plugins/tts-telegram-sync}"
bash "$PLUGIN_DIR/scripts/kokoro-install.sh" --install
```

This creates a Python 3.13 venv at `~/.local/share/kokoro/`, installs MLX-Audio deps, downloads the Kokoro-82M-bf16 MLX model, and verifies MLX Metal acceleration.

### Step 3: BotFather Token

Guide the user through Telegram BotFather setup:

1. Open Telegram, search for @BotFather
2. Send `/newbot` (or verify existing bot with `/mybots`)
3. Copy the bot token
4. Store in secrets file:

```bash
mkdir -p ~/.claude/.secrets
echo "BOT_TOKEN=<token>" > ~/.claude/.secrets/ccterrybot-telegram
echo "CHAT_ID=<chat_id>" >> ~/.claude/.secrets/ccterrybot-telegram
chmod 600 ~/.claude/.secrets/ccterrybot-telegram
```

Use AskUserQuestion to ask if user has an existing bot token or needs to create one.

### Step 4: Symlinks

Create symlinks in `~/.local/bin/` for all TTS shell scripts:

```bash
PLUGIN_DIR="${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/plugins/marketplaces/cc-skills/plugins/tts-telegram-sync}"
mkdir -p ~/.local/bin
for script in tts_kokoro.sh tts_kokoro_audition.sh tts_read_clipboard.sh tts_read_clipboard_wrapper.sh tts_speed_up.sh tts_speed_down.sh tts_speed_reset.sh; do
    ln -sf "$PLUGIN_DIR/scripts/$script" ~/.local/bin/"$script"
done
```

### Step 5: Verify

```bash
# Test Kokoro health
PLUGIN_DIR="${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/plugins/marketplaces/cc-skills/plugins/tts-telegram-sync}"
bash "$PLUGIN_DIR/scripts/kokoro-install.sh" --health

# Test bot connectivity
source ~/.claude/.secrets/ccterrybot-telegram
curl -s "https://api.telegram.org/bot${BOT_TOKEN}/getMe" | jq .ok
```

## Troubleshooting

| Issue               | Cause                | Solution                              |
| ------------------- | -------------------- | ------------------------------------- |
| uv not found        | Not installed        | `brew install uv`                     |
| Not Apple Silicon   | Intel Mac or Linux   | Requires M1+ Mac (MLX Metal)          |
| Model download slow | Large first download | ~400MB, wait for completion           |
| Token invalid       | Typo or expired      | Re-verify with `/mybots` in BotFather |
| Symlinks broken     | Plugin path changed  | Re-run symlink creation step          |
