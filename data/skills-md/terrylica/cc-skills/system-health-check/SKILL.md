---
name: system-health-check
description: Health check for TTS and Telegram bot subsystems. TRIGGERS - health check, bot health, kokoro health, tts health, tts lock, system status, diagnostics.
allowed-tools: Read, Bash, Glob, AskUserQuestion
---

# System Health Check

Run a comprehensive 10-subsystem health check across the TTS engine, Telegram bot, and supporting infrastructure. Produces a pass/fail report table with actionable fix recommendations.

> **Platform**: macOS (Apple Silicon)

## When to Use This Skill

- Diagnose why TTS or Telegram bot is not working
- Verify system readiness after bootstrap or configuration changes
- Routine health check before a demo or presentation
- Investigate intermittent failures in the TTS pipeline
- Check for stale locks, zombie processes, or orphaned temp files

## Requirements

- Bun runtime (for bot process)
- Python 3.13 with Kokoro venv at `~/.local/share/kokoro/.venv`
- Telegram bot token in `~/.claude/.secrets/ccterrybot-telegram`
- mise.toml configured in `~/.claude/automation/claude-telegram-sync/`

## Workflow Phases

### Phase 1: Setup

Load environment variables from mise to ensure `BOT_TOKEN` and other secrets are available:

```bash
cd ~/.claude/automation/claude-telegram-sync && eval "$(mise env)"
```

### Phase 2: Run All 10 Health Checks

Execute each check and collect results. Each check returns `[OK]` or `[FAIL]` with a brief diagnostic message.

#### Check 1: Bot Process

```bash
pgrep -la 'bun.*src/main.ts'
```

Pass if exactly one process is found. Fail if zero or more than one.

#### Check 2: Telegram API

```bash
BOT_TOKEN=$(cat ~/.claude/.secrets/ccterrybot-telegram)
curl -s "https://api.telegram.org/bot${BOT_TOKEN}/getMe" | jq .ok
```

Pass if response is `true`. Fail if `false`, null, or connection error.

#### Check 3: Kokoro venv

```bash
[[ -d ~/.local/share/kokoro/.venv ]]
```

Pass if the directory exists.

#### Check 4: MLX-Audio Import

```bash
~/.local/share/kokoro/.venv/bin/python -c "from mlx_audio.tts.utils import load_model; print('MLX OK')"
```

Pass if import succeeds with exit code 0.

#### Check 5: Apple Silicon

```bash
[[ "$(uname -m)" == "arm64" ]]
```

Pass if architecture is arm64. MLX-Audio requires Apple Silicon (M1+).

#### Check 6: Lock State

```bash
LOCK_FILE="/tmp/kokoro-tts.lock"
if [[ -f "$LOCK_FILE" ]]; then
  LOCK_PID=$(cat "$LOCK_FILE")
  LOCK_AGE=$(( $(date +%s) - $(stat -f %m "$LOCK_FILE") ))
  if kill -0 "$LOCK_PID" 2>/dev/null; then
    if [[ $LOCK_AGE -gt 30 ]]; then
      echo "STALE (PID $LOCK_PID alive but lock age ${LOCK_AGE}s > 30s threshold)"
    else
      echo "ACTIVE (PID $LOCK_PID, age ${LOCK_AGE}s)"
    fi
  else
    echo "ORPHANED (PID $LOCK_PID not running, age ${LOCK_AGE}s)"
  fi
else
  echo "NO LOCK (idle)"
fi
```

Pass if no lock or active lock with age under 30s. Fail if stale or orphaned.

#### Check 7: Audio Processes

```bash
pgrep -x afplay
pgrep -x say
```

Informational check. Reports count of running audio processes. Not a pass/fail -- just reports state.

#### Check 8: Secrets File

```bash
[[ -f ~/.claude/.secrets/ccterrybot-telegram ]]
```

Pass if the file exists and is non-empty.

#### Check 9: Stale WAV Files

```bash
find /tmp -maxdepth 1 -name "kokoro-tts-*.wav" -mmin +5 2>/dev/null
```

Pass if no stale WAV files found (older than 5 minutes). Fail if orphaned WAVs exist.

#### Check 10: Shell Symlinks

```bash
[[ -L ~/.local/bin/tts_kokoro.sh ]] && readlink ~/.local/bin/tts_kokoro.sh
```

Pass if symlink exists and points to a valid target within the plugin.

### Phase 3: Report

Display results as a table:

```
| # | Subsystem        | Status | Detail                          |
|---|------------------|--------|---------------------------------|
| 1 | Bot Process      | [OK]   | PID 12345                       |
| 2 | Telegram API     | [OK]   | Bot @ccterrybot responding      |
| 3 | Kokoro venv      | [OK]   | ~/.local/share/kokoro/.venv     |
| 4 | MLX-Audio Import | [OK]   | mlx_audio module loaded         |
| 5 | Apple Silicon    | [OK]   | arm64 (MLX Metal)               |
| 6 | Lock State       | [OK]   | No lock (idle)                  |
| 7 | Audio Processes  | [OK]   | 0 afplay, 0 say                |
| 8 | Secrets File     | [OK]   | ccterrybot-telegram present     |
| 9 | Stale WAVs       | [OK]   | No orphaned files               |
|10 | Shell Symlinks   | [OK]   | tts_kokoro.sh -> plugin script  |
```

### Phase 4: Summary and Recommendations

- Report total pass/fail counts (e.g., "9/10 checks passed")
- For each failure, recommend the appropriate fix or skill to invoke

## TodoWrite Task Templates

```
1. [Setup] Load environment variables from mise in bot source directory
2. [Run] Execute all 10 health checks and collect results
3. [Report] Display results table with [OK]/[FAIL] status for each subsystem
4. [Summary] Show pass/fail counts (e.g., 9/10 passed)
5. [Recommend] Suggest fixes for any failures, referencing relevant skills
```

## Post-Change Checklist

- [ ] All 10 checks executed (none skipped due to early exit)
- [ ] Results table displayed with consistent formatting
- [ ] Each failure has an actionable recommendation
- [ ] No sensitive values (tokens, secrets) exposed in output

## Troubleshooting

| Issue                             | Cause                               | Solution                                                                |
| --------------------------------- | ----------------------------------- | ----------------------------------------------------------------------- |
| All checks fail                   | Environment not set up              | Run `full-stack-bootstrap` skill first                                  |
| Only Kokoro checks fail (3-4)     | Kokoro venv missing or broken       | Run `kokoro-install.sh --health` for detailed report                    |
| Lock stuck (check 6)              | Stale lock from crashed TTS process | Check lock age and PID; see `diagnostic-issue-resolver` skill           |
| Bot process missing (check 1)     | Bot crashed or was never started    | See `bot-process-control` skill                                         |
| Telegram API fails (check 2)      | Token expired or network issue      | Verify token in `~/.claude/.secrets/ccterrybot-telegram`; check network |
| Not Apple Silicon (check 5)       | Running on Intel Mac or Linux       | MLX-Audio requires Apple Silicon (M1+)                                  |
| Stale WAVs found (check 9)        | TTS process crashed mid-generation  | Clean with `rm /tmp/kokoro-tts-*.wav`; investigate crash cause          |
| Shell symlinks missing (check 10) | Bootstrap incomplete                | Re-run symlink setup from `full-stack-bootstrap` skill                  |

## Reference Documentation

- [Health Checks](./references/health-checks.md) - Detailed description of each check, failure meaning, and remediation
- [Evolution Log](./references/evolution-log.md) - Change history for this skill
