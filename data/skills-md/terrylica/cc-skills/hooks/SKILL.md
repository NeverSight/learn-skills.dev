---
name: hooks
description: "Install/uninstall tts-telegram-sync Stop hook to ~/.claude/settings.json. TRIGGERS - tts hooks, install tts hook, tts stop hook."
allowed-tools: Read, Write, Edit, Bash, AskUserQuestion
argument-hint: "[install|uninstall|status]"
model: haiku
disable-model-invocation: true
---

# TTS Telegram Sync Hooks Manager

Manage the Stop hook that sends session-end notifications to Telegram.

## Hook

| Hook                      | Event | Purpose                                   |
| ------------------------- | ----- | ----------------------------------------- |
| `telegram-notify-stop.ts` | Stop  | Send session end notification to Telegram |

The Stop hook runs when a Claude Code session ends, sending a notification to your Telegram bot with session details.

## Actions

| Action      | Description                         |
| ----------- | ----------------------------------- |
| `install`   | Add Stop hook to settings.json      |
| `uninstall` | Remove Stop hook from settings.json |
| `status`    | Show current hook configuration     |

## Workflow

### Skip Logic

- If action provided (`install`, `uninstall`, `status`) → execute directly
- If no arguments → check current status, then use AskUserQuestion flow

### Interactive Flow (No Arguments)

```
Question: "What would you like to do with the tts-telegram-sync Stop hook?"
Options:
  - "Install" → "Add Stop hook for Telegram notifications on session end"
  - "Uninstall" → "Remove the Stop hook from settings.json"
  - "Status" → "Show current hook configuration"
```

### Execution

The hook is registered in the plugin's `hooks/hooks.json`:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bun $CLAUDE_PLUGIN_ROOT/hooks/telegram-notify-stop.ts",
            "timeout": 10000
          }
        ]
      }
    ]
  }
}
```

The plugin system handles hook installation automatically when the plugin is enabled. Manual installation/uninstallation should modify `~/.claude/settings.json` hooks section.

## Post-Action Reminder

**IMPORTANT: Restart Claude Code session for changes to take effect.**

Hooks are loaded at session start.

## Troubleshooting

| Issue                | Cause                  | Solution                        |
| -------------------- | ---------------------- | ------------------------------- |
| Hook not firing      | Session not restarted  | Restart Claude Code session     |
| Notification missing | Bot not running        | Start bot first                 |
| Timeout errors       | Bot slow to respond    | Increase timeout in hooks.json  |
| Bun not found        | PATH issue in hook env | Add Bun to PATH in hook command |
