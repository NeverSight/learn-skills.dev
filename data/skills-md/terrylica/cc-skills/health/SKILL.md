---
name: health
description: "Health check for TTS and Telegram bot subsystems. TRIGGERS - tts health, kokoro status, telegram bot check, tts diagnostics."
allowed-tools: Read, Bash, Glob
model: haiku
---

# TTS Telegram Sync Health Check

Run 10 subsystem health checks to verify the full TTS + bot stack.

## Checks

| #   | Check            | Command                                                                                  |
| --- | ---------------- | ---------------------------------------------------------------------------------------- |
| 1   | Bot process      | `pgrep -la 'bun.*src/main.ts'`                                                           |
| 2   | Telegram API     | `curl -s "https://api.telegram.org/bot${BOT_TOKEN}/getMe" \| jq .ok`                     |
| 3   | Kokoro venv      | `[[ -d ~/.local/share/kokoro/.venv ]]`                                                   |
| 4   | MLX-Audio import | `~/.local/share/kokoro/.venv/bin/python -c "from mlx_audio.tts.utils import load_model"` |
| 5   | Apple Silicon    | `[[ "$(uname -m)" == "arm64" ]]`                                                         |
| 6   | Lock state       | Check `/tmp/kokoro-tts.lock` mtime and PID                                               |
| 7   | Audio processes  | `pgrep -x afplay` / `pgrep -x say`                                                       |
| 8   | Secrets file     | `[[ -f ~/.claude/.secrets/ccterrybot-telegram ]]`                                        |
| 9   | Stale WAVs       | `find /tmp -name "kokoro-tts-*.wav" -mmin +5`                                            |
| 10  | Shell symlinks   | `[[ -L ~/.local/bin/tts_kokoro.sh ]]`                                                    |

## Execution

### Quick Health Check

```bash
PLUGIN_DIR="${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/plugins/marketplaces/cc-skills/plugins/tts-telegram-sync}"
bash "$PLUGIN_DIR/scripts/kokoro-install.sh" --health
```

### Full Stack Check

Run all 10 checks and display results as `[OK]`/`[FAIL]` table. For each failure, suggest the appropriate skill to fix it:

| Failure         | Recommended Skill         |
| --------------- | ------------------------- |
| Bot not running | bot-process-control       |
| Kokoro issues   | full-stack-bootstrap      |
| Lock stuck      | diagnostic-issue-resolver |
| Secrets missing | full-stack-bootstrap      |
| Symlinks broken | full-stack-bootstrap      |

## Troubleshooting

| Issue             | Cause          | Solution                                         |
| ----------------- | -------------- | ------------------------------------------------ |
| All checks fail   | Not set up yet | Run `/tts-telegram-sync:setup` first             |
| Only Kokoro fails | Venv corrupted | `kokoro-install.sh --uninstall` then `--install` |
| Lock stuck        | Heartbeat died | See diagnostic-issue-resolver skill              |
