---
name: settings-and-tuning
description: Configure TTS voices, speed, timeouts, queue depth, and bot settings. TRIGGERS - configure tts, change voice, tts speed, queue depth, tts timeout, bot config, tune settings, adjust parameters.
allowed-tools: Read, Write, Edit, Bash, Glob, AskUserQuestion
---

# Settings and Tuning

Configure all adjustable parameters for the TTS engine, Telegram bot, and supporting infrastructure. All settings are centralized in the mise.toml SSoT.

> **Platform**: macOS (Apple Silicon)

## When to Use This Skill

- Changing TTS voice (English, Chinese, or macOS `say` voices)
- Adjusting speech speed
- Tuning TTS timeouts or queue depth
- Configuring notification rate limiting or circuit breakers
- Adjusting prompt executor throttling
- Modifying session picker limits
- Changing audit log retention

---

## Requirements

| Component   | Required    | Installation                                      |
| ----------- | ----------- | ------------------------------------------------- |
| mise        | Yes         | `brew install mise` (for env loading)             |
| Bot running | Recommended | Changes to TTS/queue settings require bot restart |

---

## Workflow Phases

### Phase 0: Read Current Configuration

Read the current mise.toml to see all active settings:

```bash
cat ~/.claude/automation/claude-telegram-sync/mise.toml
```

All configurable values live in the `[env]` section. The file is the single source of truth for the entire stack.

### Phase 1: Identify What to Change

Present the config groups to the user via AskUserQuestion. Config groups:

| Group           | Settings                                                               | Description                                     |
| --------------- | ---------------------------------------------------------------------- | ----------------------------------------------- |
| TTS Voice       | `TTS_VOICE_EN`, `TTS_VOICE_ZH`, `TTS_VOICE_SAY_EN`, `TTS_VOICE_SAY_ZH` | Voice selection per language                    |
| TTS Speed       | `TTS_SPEED`                                                            | Speech rate multiplier                          |
| TTS Timeouts    | `TTS_GENERATE_TIMEOUT_MS`, `TTS_SAY_TIMEOUT_MS`                        | Generation and playback timeouts                |
| TTS Queue       | `TTS_MAX_QUEUE_DEPTH`, `TTS_STALE_TTL_MS`, `TTS_MAX_TEXT_LEN`          | Queue limits and staleness                      |
| TTS Signal      | `TTS_SIGNAL_SOUND`                                                     | Signal sound path (empty to disable)            |
| Rate Limiting   | `NOTIFICATION_MIN_INTERVAL_MS`, `SUMMARIZER_*`                         | Notification and summarizer throttling          |
| Prompt Executor | `PROMPT_*`                                                             | Prompt execution throttling and circuit breaker |
| Session Picker  | `SESSION_*`                                                            | Session scanning and display limits             |
| Audit           | `AUDIT_RETENTION_DAYS`                                                 | Log retention period                            |
| Model           | `HAIKU_MODEL`                                                          | Claude model for Agent SDK calls                |

### Phase 2: Edit Configuration

Edit the appropriate line(s) in `~/.claude/automation/claude-telegram-sync/mise.toml`. Use the Edit tool to make precise changes to specific values.

### Phase 3: Validate and Apply

1. Verify the edited value is within the valid range (see [Config Reference](./references/config-reference.md))
2. If TTS, queue, or rate limiting settings changed, restart the bot:

```bash
# Option A: If using mise tasks
cd ~/.claude/automation/claude-telegram-sync && mise run bot:restart

# Option B: Manual restart
pkill -f "bun.*main.ts" && cd ~/.claude/automation/claude-telegram-sync && bun --watch run src/main.ts
```

1. Confirm new settings are active by checking bot logs or testing the affected feature

---

## TodoWrite Task Templates

### Template: Settings Adjustment

```
1. [Read] Read current mise.toml configuration
2. [Identify] Present config groups to user via AskUserQuestion
3. [Select] User selects setting category to modify
4. [Edit] Update mise.toml with new values
5. [Validate] Verify values are in valid range
6. [Apply] Restart bot to apply changes (if TTS or queue settings changed)
7. [Verify] Confirm new settings are active
```

---

## Post-Change Checklist

After modifying this skill:

1. [ ] Verify all config groups in SKILL.md match current mise.toml
2. [ ] Update config-reference.md if new env vars were added
3. [ ] Test that changed settings take effect after bot restart
4. [ ] Update `references/evolution-log.md` with change description

---

## Troubleshooting

| Issue                      | Cause                            | Solution                                               |
| -------------------------- | -------------------------------- | ------------------------------------------------------ |
| Settings not taking effect | Bot not restarted                | Restart bot after changing mise.toml                   |
| mise.toml parse error      | Invalid TOML syntax              | Check for missing quotes or unescaped chars            |
| Voice not found            | Invalid voice name               | Check voice catalog (Kokoro voices are case-sensitive) |
| Speed too fast/slow        | Value out of range               | Use 0.5 to 2.0 range for TTS_SPEED                     |
| Circuit breaker stuck open | Too many failures                | Wait for breaker timeout or restart bot                |
| Timeout too short          | TTS generation slow on first run | Model warmup takes longer; increase timeout            |

---

## Reference Documentation

- [Config Reference](./references/config-reference.md) - Full reference table with all env vars, defaults, valid ranges, and component ownership
- [mise.toml Reference](./references/mise-toml-reference.md) - Hub/spoke mise architecture, secret loading, and task file structure
- [Evolution Log](./references/evolution-log.md) - Change history for this skill
