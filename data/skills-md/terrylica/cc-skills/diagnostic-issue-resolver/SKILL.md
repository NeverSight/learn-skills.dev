---
name: diagnostic-issue-resolver
description: Diagnose and resolve TTS and Telegram bot issues. TRIGGERS - tts not working, bot not responding, kokoro error, audio not playing, lock stuck, telegram bot troubleshoot, diagnose issue.
allowed-tools: Read, Bash, Glob, Grep, AskUserQuestion
---

# Diagnostic Issue Resolver

Diagnose and fix common TTS + Telegram bot issues through systematic symptom collection, automated diagnostics, and targeted fixes.

> **Platform**: macOS (Apple Silicon)

---

## When to Use This Skill

- TTS audio is not playing or sounds wrong
- Telegram bot is not responding to messages
- Kokoro engine errors or timeouts
- Lock file appears stuck
- Audio plays twice (race condition)
- MLX Metal acceleration is not working
- Queue appears full or backed up

---

## Requirements

- Access to `~/.claude/automation/claude-telegram-sync/` (bot source)
- Access to `~/.local/share/kokoro/` (Kokoro engine)
- Access to `~/.local/share/tts-telegram-sync/logs/` (centralized logs)

---

## Known Issue Table

| Issue                 | Likely Cause             | Diagnostic                                                                | Fix                                                                                    |
| --------------------- | ------------------------ | ------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| No audio output       | Stale TTS lock           | `stat /tmp/kokoro-tts.lock`                                               | `rm -f /tmp/kokoro-tts.lock`                                                           |
| Bot not responding    | Process crashed          | `pgrep -la 'bun.*src/main.ts'`                                            | Restart: `cd ~/.claude/automation/claude-telegram-sync && bun --watch run src/main.ts` |
| Kokoro timeout        | First-run model load     | Check `~/.cache/huggingface/`                                             | Wait for download, or re-run `kokoro-install.sh --install`                             |
| Queue full            | Rapid-fire notifications | Check queue depth in audit log                                            | Increase `TTS_MAX_QUEUE_DEPTH` in mise.toml or drain queue                             |
| Lock stuck forever    | Heartbeat process died   | `stat /tmp/kokoro-tts.lock` + `pgrep -x afplay`                           | If lock stale >30s AND no audio process, rm lock                                       |
| Slow MLX acceleration | Wrong Python or deps     | `python -c "from mlx_audio.tts.utils import load_model; print('MLX OK')"` | Reinstall via `kokoro-install.sh --upgrade`                                            |
| Double audio playback | Lock race condition      | Check for multiple afplay processes                                       | Kill all: `pkill -x afplay`, then restart                                              |

---

## Workflow Phases

### Phase 1: Symptom Collection

Use AskUserQuestion to understand what the user is experiencing. Key questions:

- What happened? (no audio, wrong audio, bot silent, error message)
- When did it start? (after upgrade, suddenly, always)
- What were you doing? (clipboard read, Telegram notification, manual TTS)

### Phase 2: Automated Diagnostics

Based on symptoms, run the relevant subset of these checks:

```bash
# Lock state
ls -la /tmp/kokoro-tts.lock 2>/dev/null && stat -f "%Sm" /tmp/kokoro-tts.lock || echo "No lock file"

# Audio processes
pgrep -la afplay; pgrep -la say

# Bot process
pgrep -la 'bun.*src/main.ts'

# Kokoro health
~/.local/share/kokoro/.venv/bin/python -c "from mlx_audio.tts.utils import load_model; print('MLX-Audio OK')"

# Recent errors in audit log
tail -20 ~/.local/share/tts-telegram-sync/logs/audit/*.ndjson 2>/dev/null | grep -i error

# Recent bot console output
tail -50 /private/tmp/telegram-bot.log 2>/dev/null | grep -i -E '(error|fail|timeout)'
```

### Phase 3: Root Cause Analysis

Map diagnostic output to the Known Issue Table above. Common patterns:

- Lock file exists + mtime > 30s ago + no afplay = **stale lock**
- No bot PID found = **bot crashed**
- `from mlx_audio.tts.utils import load_model` fails = **MLX-Audio broken**
- Multiple afplay PIDs = **race condition**

### Phase 4: Fix Application

Apply the targeted fix from the Known Issue Table. Always use the least disruptive fix first.

### Phase 5: Verification

After applying the fix, verify the issue is resolved:

```bash
# Quick TTS test
~/.local/share/kokoro/.venv/bin/python ~/.local/share/kokoro/tts_generate.py \
  --text "Diagnostic test complete" --voice af_heart --lang en-us --speed 1.0 \
  --output /tmp/kokoro-tts-diag-test.wav && afplay /tmp/kokoro-tts-diag-test.wav && echo "OK"

# Full health check
~/eon/cc-skills/plugins/tts-telegram-sync/scripts/kokoro-install.sh --health
```

---

## TodoWrite Task Templates

```
1. [Symptoms] Collect symptoms via AskUserQuestion
2. [Triage] Map symptoms to likely causes
3. [Lock] Check TTS lock state (mtime, PID, stale detection)
4. [Process] Check bot process and audio processes
5. [Kokoro] Verify Kokoro venv and MLX-Audio availability
6. [Logs] Check recent audit logs for errors
7. [Fix] Apply targeted fix for identified root cause
8. [Verify] Run health check to confirm resolution
```

---

## Post-Change Checklist

- [ ] Root cause identified and documented
- [ ] Fix applied successfully
- [ ] Health check passes
- [ ] Test audio plays correctly
- [ ] No stale locks or orphan processes remain

---

## Troubleshooting

This skill IS the troubleshooting skill. If the standard diagnostics do not identify the issue:

1. Check the full bot console log: `cat /private/tmp/telegram-bot.log`
2. Check all NDJSON audit logs: `ls -lt ~/.local/share/tts-telegram-sync/logs/audit/`
3. Check system audio: `afplay /System/Library/Sounds/Tink.aiff` (if this fails, it is a macOS audio issue, not TTS)
4. Run a manual Kokoro generation outside the bot to isolate the problem
5. If all else fails, do a full teardown and reinstall using `clean-component-removal` then `full-stack-bootstrap`

---

## Reference Documentation

- [Common Issues](./references/common-issues.md) -- Expanded diagnostic procedures for each known issue
- [Lock Debugging](./references/lock-debugging.md) -- Deep dive into the two-layer lock mechanism
- [Evolution Log](./references/evolution-log.md) -- Change history for this skill
