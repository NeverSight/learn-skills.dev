---
name: ngrok-preview
description: Generate short-lived, mobile-friendly ngrok preview links for local artifacts and share them in Telegram. Use when OpenClaw produces images/charts/generated files that the user needs to view remotely on phone, and a temporary per-task link is preferred over manual file transfer.
---

# ngrok-preview

Provide a temporary preview window for task outputs. Keep it fast, scoped, and easy: generate link -> send link -> close link.

## One-time setup

1. Install ngrok if missing.
2. Configure auth token once:

```bash
ngrok config add-authtoken "$NGROK_AUTHTOKEN"
ngrok config check
```

If token is not preconfigured, pass `--auth-token` when running the script.

## Per-task workflow

1. Collect only task artifacts (images/charts/files) for this request.
2. Create a session-scoped temporary preview link.
3. Send the link with explicit expiry in Telegram.
4. Stop and delete the preview session after user confirms or task ends.

Use this command from the skill directory:

```bash
python3 scripts/ngrok_preview.py up \
  --title "<task title>" \
  --session-id "<task-id>" \
  --ttl-minutes 120 \
  --source "<artifact-path-1>" \
  --source "<artifact-path-2>"
```

The command returns JSON including:
- `public_url`
- `expires_at`
- `session_id`
- `stop_command`

### Session ID convention (context binding)

Use IDs that map to the current conversation/task:
- `tg-<date>-<topic>`
- `task-<short-request-id>`

This keeps each link tied to one task context.

## Telegram send pattern

After `up` succeeds, send a concise message:

```text
🔗 Temporary preview link (valid for <X> minutes)
<public_url>

Scope: artifacts from this task only
This link will be cleaned up after expiry
```

If not currently in Telegram, still return the same link format in the active channel.

## Safety boundaries

- Publish only task-specific outputs, never broad directories (do not expose workspace root).
- Keep TTL short (default 120 minutes; use shorter when possible).
- Treat link as temporary access, not persistent hosting.
- Stop session when no longer needed:

```bash
python3 scripts/ngrok_preview.py down --session-id "<task-id>" --delete-session-dir
```

- Periodically clear expired sessions:

```bash
python3 scripts/ngrok_preview.py cleanup
```

## Command quick reference

```bash
# List sessions
python3 scripts/ngrok_preview.py status

# Create preview (auto-generate session id)
python3 scripts/ngrok_preview.py up \
  --title "image results" \
  --source ./outputs/result-1.png \
  --source ./outputs/result-2.png

# Stop latest session
python3 scripts/ngrok_preview.py down
```

## Troubleshooting

If link creation fails, check `references/troubleshooting.md` and follow the minimum recovery sequence.
