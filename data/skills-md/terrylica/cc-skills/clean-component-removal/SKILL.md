---
name: clean-component-removal
description: Remove TTS and Telegram sync components cleanly. TRIGGERS - uninstall tts, remove telegram bot, uninstall kokoro, clean tts, teardown, component removal.
allowed-tools: Read, Bash, Glob, AskUserQuestion
disable-model-invocation: true
---

# Clean Component Removal

Orderly teardown of TTS and Telegram bot components with proper sequencing to avoid orphaned processes and stale state.

> **Platform**: macOS (Apple Silicon)

---

## When to Use This Skill

- User wants to uninstall the Kokoro TTS engine
- User wants to remove the Telegram bot
- User wants to clean up all TTS-related files
- User wants to do a full teardown before reinstallation
- User wants to remove specific components selectively

---

## Requirements

- No special tools needed (removal uses only `rm`, `pkill`, and the install script)
- User confirmation before destructive operations

---

## Removal Order

The removal sequence matters. Components must be torn down in this order to avoid orphaned processes or lock contention.

| Step | Component          | Command                                            | Reversible?          |
| ---- | ------------------ | -------------------------------------------------- | -------------------- |
| 1    | Bot process        | `pkill -f 'bun.*src/main.ts'`                      | Yes (restart bot)    |
| 2    | Kokoro venv        | `kokoro-install.sh --uninstall`                    | Yes (reinstall)      |
| 3    | Shell symlinks     | `rm -f ~/.local/bin/tts_*.sh`                      | Yes (re-symlink)     |
| 4    | Temp files         | `rm -f /tmp/kokoro-tts-*.wav /tmp/kokoro-tts.lock` | N/A                  |
| 5    | Secrets (optional) | `rm -f ~/.claude/.secrets/ccterrybot-telegram`     | Requires re-creation |

---

## What Is NOT Removed (Unless Explicitly Asked)

These are preserved by default to allow easy reinstallation:

| Resource         | Path                                                   | Why Preserved              |
| ---------------- | ------------------------------------------------------ | -------------------------- |
| Model cache      | `~/.cache/huggingface/hub/models--hexgrad--Kokoro-82M` | ~400MB download, reusable  |
| Bot source code  | `~/.claude/automation/claude-telegram-sync/`           | Git-tracked, not ephemeral |
| mise.toml config | `~/.claude/automation/claude-telegram-sync/mise.toml`  | Configuration SSoT         |
| Centralized logs | `~/.local/share/tts-telegram-sync/logs/`               | Audit trail                |

---

## Workflow Phases

### Phase 1: Confirmation

Use AskUserQuestion to confirm which components to remove. Present options:

1. **Full teardown** -- Remove everything (steps 1-4, ask about secrets)
2. **TTS only** -- Remove Kokoro venv + symlinks + temp files (steps 2-4)
3. **Bot only** -- Stop bot process (step 1 only)
4. **Selective** -- Let user pick individual steps

### Phase 2: Stop Bot Process

```bash
# Check if bot is running
pgrep -la 'bun.*src/main.ts'

# Stop it
pkill -f 'bun.*src/main.ts' || echo "Bot was not running"
```

### Phase 3: Remove Kokoro Venv

```bash
# Uses kokoro-install.sh --uninstall (removes venv, keeps model cache)
~/eon/cc-skills/plugins/tts-telegram-sync/scripts/kokoro-install.sh --uninstall
```

### Phase 4: Remove Symlinks

```bash
# List existing symlinks first
ls -la ~/.local/bin/tts_*.sh 2>/dev/null

# Remove them
rm -f ~/.local/bin/tts_*.sh
```

### Phase 5: Clean Temp Files

```bash
rm -f /tmp/kokoro-tts-*.wav
rm -f /tmp/kokoro-tts.lock
```

### Phase 6: Optional Secret Removal

Only with explicit user confirmation:

```bash
# Show what would be removed
ls -la ~/.claude/.secrets/ccterrybot-telegram

# Remove (requires confirmation)
rm -f ~/.claude/.secrets/ccterrybot-telegram
```

---

## TodoWrite Task Templates

```
1. [Confirm] Ask user which components to remove via AskUserQuestion
2. [Stop] Stop bot process
3. [Venv] Run kokoro-install.sh --uninstall
4. [Symlinks] Remove ~/.local/bin/ symlinks
5. [Temp] Clean /tmp/ TTS files
6. [Secrets] Optionally remove secrets (with confirmation)
7. [Verify] Confirm all selected components removed
```

---

## Post-Change Checklist

- [ ] Bot process is not running (`pgrep -la 'bun.*src/main.ts'` returns nothing)
- [ ] Kokoro venv removed (`ls ~/.local/share/kokoro/.venv` returns "No such file")
- [ ] Symlinks removed (`ls ~/.local/bin/tts_*.sh` returns "No such file")
- [ ] No stale lock file (`ls /tmp/kokoro-tts.lock` returns "No such file")
- [ ] No orphan audio processes (`pgrep -x afplay` returns nothing)

---

## Troubleshooting

| Problem                            | Likely Cause                         | Fix                                                           |
| ---------------------------------- | ------------------------------------ | ------------------------------------------------------------- |
| Symlinks still exist after removal | Glob mismatch or permission          | `ls -la ~/.local/bin/tts_*` then `rm -f` each one             |
| Stale lock after removal           | Process died without cleanup         | `rm -f /tmp/kokoro-tts.lock`                                  |
| Model cache taking space           | ~400MB in HuggingFace cache          | `rm -rf ~/.cache/huggingface/hub/models--hexgrad--Kokoro-82M` |
| Bot respawns after kill            | Launched with `--watch` from launchd | Check `launchctl list` for relevant agents                    |
| Audio still playing after teardown | `afplay` process outlives bot        | `pkill -x afplay`                                             |

---

## Reference Documentation

- [Evolution Log](./references/evolution-log.md) -- Change history for this skill
