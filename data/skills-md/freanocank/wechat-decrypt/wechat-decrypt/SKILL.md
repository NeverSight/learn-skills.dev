---
name: wechat-decrypt
description: Read, search, summarize, export, and transcribe a user's own local WeChat 4.x history on macOS or Windows; diagnose setup and re-extract the device key after a WeChat update. Use for WeChat messages, chats, contacts, and local archives. Do not use for remote accounts or devices the user is not authorized to access.
---

# WeChat local history

Operate only on local WeChat data the user is authorized to access. Keep keys, decrypted databases, voice caches, and exports local. Never print a raw key or include one in chat, logs, commands, or reports.

## Resolve the runtime

Use the directory containing this `SKILL.md` as `SKILL_DIR`; never assume a fixed installation path.

- macOS: prefer `$SKILL_DIR/.venv/bin/python`, otherwise `python3`.
- Windows: prefer `$SKILL_DIR\.venv\Scripts\python.exe`, otherwise `python`.

Before reading chat data, run the read-only diagnostic:

```bash
"$SKILL_DIR/.venv/bin/python" "$SKILL_DIR/scripts/common/doctor.py" --json
```

On Windows, use the equivalent venv Python path. Interpret `fail` as blocking and `warn` as optional/degraded:

- `key` or `database` failure: read the matching platform reference below.
- `mcp` warning: use the CLI fallback now; run platform setup only when MCP registration is needed.
- `voice-backend` warning: ordinary export works; install the optional platform voice stack only for transcription.
- `voice-model` warning: ordinary export still works. Do not download the model without user approval.

## Route the request

| Intent | Preferred action |
|---|---|
| List chats or groups | `wechat_list_chats` |
| Read one chat | `wechat_read_chat` |
| Search all chats | `wechat_search_messages` |
| Review recent activity | `wechat_recent_messages` |
| Summarize recent chats and action items | `wechat_chat_summary` |
| Review pats, recalls, group changes, payments, or calls | `wechat_system_events`; filter with a stable code or Chinese label |
| Review shared music, videos, Channels, mini programs, files, or links | Use normal read/search/summary tools; inspect the structured `app` object in CLI JSON when exact metadata matters |
| Statistics, media, or a received document | CLI `stats`, `media`, or `openfile` |
| Export history or transcribe voice | Read [references/export-transcription.md](references/export-transcription.md) |
| Missing chats, a missing shard, or a corrupted database | Read [references/db-repair.md](references/db-repair.md) |
| macOS setup, key failure, or WeChat update | Read [references/macos.md](references/macos.md) |
| Windows setup, key failure, or WeChat update | Read [references/windows.md](references/windows.md) |

MCP is a thin optional facade. If it is unavailable, use the same logic through `scripts/common/query.py` and request JSON:

```bash
"$PYTHON" "$SKILL_DIR/scripts/common/query.py" list --json
"$PYTHON" "$SKILL_DIR/scripts/common/query.py" read CONTACT -d 7 -n 50 --json
"$PYTHON" "$SKILL_DIR/scripts/common/query.py" search KEYWORD -d 30 -n 50 --json
"$PYTHON" "$SKILL_DIR/scripts/common/query.py" recent -d 3 -n 100 --json
"$PYTHON" "$SKILL_DIR/scripts/common/query.py" summary -d 3 --json
"$PYTHON" "$SKILL_DIR/scripts/common/query.py" events -e pat -d 30 -n 100 --json
```

`[我]` means the account owner; `[对方]` means the peer. If contact matching is ambiguous, show the candidates and ask the user to choose; do not guess. Keep time windows and limits proportional to the request, and do not dump full history unless explicitly requested.

## Operational invariants

- Raw keys are 64 hexadecimal characters and are device-specific. macOS and Windows keys for the same account are not interchangeable.
- macOS queries encrypted databases in place through SQLCipher, always read-only.
- Windows first creates a local plaintext mirror under `decrypted/`, then queries it read-only. Treat that mirror as sensitive.
- WeChat updates may invalidate extraction assumptions or require a new key. Run `doctor.py` before repeating extraction.
- Voice transcription is offline after the model is cached. A first large-v3 download is about 3 GB and always requires user approval.
- Type-49 app messages are parsed locally. Preserve their structured `app` metadata when answering questions about titles, creators, sources, URLs, files, mini programs, or Channels; unknown subtypes may still contain useful fields.
- Setup migrates only missing private files from legacy installs. Switching an existing user-skill link requires the explicit platform upgrade flag and leaves a recoverable backup.
- A damaged shard is quarantined into `<name>.db.factory/` and is usually recoverable page by page. Never repair a live database in place: rebuild into a copy, verify it, and back up before restoring anything.
