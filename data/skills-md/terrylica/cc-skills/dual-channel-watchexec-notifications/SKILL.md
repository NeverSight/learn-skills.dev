---
name: dual-channel-watchexec-notifications
description: Dual-channel notifications on watchexec events. TRIGGERS - watchexec alerts, Telegram+Pushover, file change notifications.
allowed-tools: Read, Write, Edit, Bash
---

# Dual-Channel Watchexec Notifications

Send reliable notifications to both Telegram and Pushover when watchexec detects file changes or process crashes.

## When to Use This Skill

Use this skill when:

- Setting up file change monitoring with notifications
- Implementing process crash alerting via Telegram and Pushover
- Creating watchexec wrappers with dual-channel notification support
- Formatting messages for both HTML (Telegram) and plain text (Pushover)
- Troubleshooting notification delivery or formatting issues

## Core Pattern

**watchexec wrapper script** → **detect event** → **notify-script** → **Telegram + Pushover**

```bash
# wrapper.sh - Monitors process and detects restart reasons
watchexec --restart -- python bot.py

# On event, call:
notify-script.sh <reason> <exit_code> <watchexec_info_file> <crash_context>
```

---

## Critical Rule: Format Differences

**Telegram**: HTML mode ONLY

```bash
MESSAGE="<b>Alert</b>: <code>file.py</code>"
# Escape 3 chars: & → &amp;, < → &lt;, > → &gt;
```

**Pushover**: Plain text ONLY

```bash
/usr/bin/env bash << 'SKILL_SCRIPT_EOF'
# Strip HTML tags before sending
MESSAGE_PLAIN=$(echo "$MESSAGE_HTML" | sed 's/<[^>]*>//g')
SKILL_SCRIPT_EOF
```

**Why HTML for Telegram**:

- Markdown requires escaping 40+ chars (`.`, `-`, `_`, etc.)
- HTML only requires escaping 3 chars (`&`, `<`, `>`)
- Industry best practice

---

## Quick Reference

### Send to Both Channels

```bash
/usr/bin/env bash << 'SKILL_SCRIPT_EOF_2'
# 1. Build HTML message for Telegram
MESSAGE_HTML="<b>File</b>: <code>handler_classes.py</code>"

# 2. Strip HTML for Pushover
MESSAGE_PLAIN=$(echo "$MESSAGE_HTML" | sed 's/<[^>]*>//g')

# 3. Send to Telegram with HTML
curl -s -d "chat_id=$CHAT_ID" \
  -d "text=$MESSAGE_HTML" \
  -d "parse_mode=HTML" \
  https://api.telegram.org/bot$BOT_TOKEN/sendMessage

# 4. Send to Pushover with plain text
curl -s --form-string "message=$MESSAGE_PLAIN" \
  https://api.pushover.net/1/messages.json
SKILL_SCRIPT_EOF_2
```

### Execution Pattern

```bash
# Fire-and-forget background notifications (don't block restarts)
"$NOTIFY_SCRIPT" "crash" "$EXIT_CODE" "$INFO_FILE" "$CONTEXT_FILE" &
```

---

## Validation Checklist

Before deploying:

- [ ] Using HTML parse mode for Telegram (not Markdown)
- [ ] HTML tags stripped for Pushover (plain text only)
- [ ] HTML escaping applied to all dynamic content (`&`, `<`, `>`)
- [ ] Credentials loaded from env vars/Doppler (not hardcoded)
- [ ] Message archiving enabled for debugging
- [ ] File detection uses `stat` (not `find -newermt`)
- [ ] Heredocs use unquoted delimiters for variable expansion
- [ ] Notifications run in background (fire-and-forget)
- [ ] Tested with files containing special chars (`_`, `.`, `-`)
- [ ] Both Telegram and Pushover successfully receiving

---

## Summary

**Key Lessons**:

1. Always use HTML mode for Telegram (simpler escaping)
2. Always strip HTML tags for Pushover (plain text only)
3. Escape only 3 chars in HTML: `&` → `&amp;`, `<` → `&lt;`, `>` → `&gt;`
4. Archive messages before sending for debugging
5. Use `stat` for file detection on macOS (not `find -newermt`)
6. Load credentials from env vars/Doppler (never hardcode)
7. Fire-and-forget background notifications (don't block restarts)

---

## Reference Documentation

For detailed information, see:

- [Telegram HTML](./references/telegram-html.md) - HTML mode formatting and message templates
- [Pushover Integration](./references/pushover-integration.md) - API calls and priority levels
- [Credential Management](./references/credential-management.md) - Doppler, env vars, and keychain patterns
- [Watchexec Patterns](./references/watchexec-patterns.md) - File detection and restart reason detection
- [Common Pitfalls](./references/common-pitfalls.md) - HTML tags in Pushover, escaping issues, macOS compatibility

**Bundled Examples:**

- `examples/notify-restart.sh` - Complete dual-channel notification script
- `examples/bot-wrapper.sh` - watchexec wrapper with restart detection
- `examples/setup-example.sh` - Setup guide and installation steps

---

## Troubleshooting

| Issue                      | Cause                          | Solution                                       |
| -------------------------- | ------------------------------ | ---------------------------------------------- |
| Telegram escaping errors   | Using Markdown instead of HTML | Switch to HTML mode with parse_mode=HTML       |
| Pushover shows HTML tags   | HTML not stripped              | Strip tags with sed before sending to Pushover |
| Notifications not arriving | Credentials missing            | Verify BOT_TOKEN, CHAT_ID, Pushover keys       |
| Special chars broken       | Missing HTML escaping          | Escape &, <, > in dynamic content              |
| find -newermt fails macOS  | macOS incompatibility          | Use stat for file detection instead            |
| Notifications blocking     | Not running in background      | Add & to run notify script fire-and-forget     |
| Duplicate notifications    | Restart loop                   | Add debounce logic or cooldown period          |
| Missing crash context      | Context file not written       | Verify watchexec info file path exists         |
