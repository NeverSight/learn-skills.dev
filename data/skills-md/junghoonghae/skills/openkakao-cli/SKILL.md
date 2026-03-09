---
name: openkakao-cli
description: Work with OpenKakao CLI (`openkakao-rs`) for KakaoTalk on macOS. Use whenever the user asks to authenticate, inspect chats, read messages, send messages, watch real-time traffic, automate from chat data, build hooks or webhooks, verify webhook signing, manage tokens, inspect auth recovery state, or operate unattended KakaoTalk workflows from the terminal. This should also trigger when the user mentions `watch`, `hook`, `webhook`, `LOCO`, `chat_id`, `auth-status`, `doctor`, `launchd`, or wants to wire OpenKakao into local scripts, agents, SQLite, cron, or launchd.
---

# OpenKakao CLI

`openkakao-rs` is a KakaoTalk CLI with REST and LOCO support. Prefer LOCO commands for full history, sending, and real-time behavior. Prefer local-first automation unless the user explicitly wants events to leave the machine.

## Quick checks

```bash
openkakao-rs --version
openkakao-rs auth
openkakao-rs auth-status
openkakao-rs doctor
```

If Homebrew install is needed:

```bash
brew tap JungHoonGhae/openkakao
brew install JungHoonGhae/openkakao/openkakao-rs
```

If the user seems to have an older binary than the repo docs or source imply, check:

```bash
which openkakao-rs
openkakao-rs --version
openkakao-rs send --help
openkakao-rs watch --help
```

Persistent operator policy can live in:

```bash
~/.config/openkakao/config.toml
```

Persisted runtime state now also lives in:

```bash
~/.config/openkakao/state.json
```

## REST API Commands (read-only, cached token)

```bash
openkakao-rs login --save          # Extract credentials from KakaoTalk's Cache.db
openkakao-rs auth                  # Verify token validity
openkakao-rs me                    # Show your profile
openkakao-rs friends [-f] [-s q]   # List friends (favorites/search)
openkakao-rs settings              # Show account settings
openkakao-rs chats                 # List chat rooms (Pilsner REST API)
openkakao-rs read <id> [-n N] [--all] # Read messages (Pilsner, limited cache)
openkakao-rs members <id>          # List chat room members
```

## LOCO Protocol Commands (full access, real-time)

```bash
openkakao-rs loco-test                          # Test full LOCO connection
openkakao-rs send <chat_id> <message> [-y]        # Send text message via LOCO WRITE (add -y to skip prompt)
openkakao-rs send-photo <chat_id> <file> [-y]  # Send photo (JPEG/PNG/GIF) via LOCO SHIP+POST
openkakao-rs send-file <chat_id> <file> [-y]   # Send any file (photo/video/doc) via LOCO
openkakao-rs watch [--chat-id ID] [--raw]       # Watch real-time incoming messages
openkakao-rs watch --read-receipt               # Watch + send read receipts (NOTIREAD)
openkakao-rs watch --max-reconnect 10           # Auto-reconnect on disconnect (default 5)
openkakao-rs watch --download-media             # Auto-download media attachments
openkakao-rs download <chat_id> <log_id> [-o D] # Download media from a specific message
openkakao-rs loco-chats [--all]                 # List all chat rooms
openkakao-rs loco-read <chat_id> [-n N] [--all] # Read message history (SYNCMSG)
openkakao-rs loco-read <chat_id> --all --json   # JSON output
openkakao-rs loco-members <chat_id>             # List members
openkakao-rs loco-chatinfo <chat_id>            # Raw chat room info
```

### LOCO vs REST for messages

- **REST** (`read`): Uses Pilsner cache — only returns messages for recently opened chats in the KakaoTalk app. Many chats return empty.
- **LOCO** (`loco-read`): Uses SYNCMSG protocol — returns all server-retained messages. Preferred for full history access.

## Token Management

```bash
openkakao-rs relogin [--fresh-xvc]    # Refresh token via login.json + X-VC
openkakao-rs renew                     # Attempt token renewal via refresh_token
openkakao-rs watch-cache [--interval N] # Poll Cache.db for fresh tokens
openkakao-rs auth-status               # Show persisted auth recovery state and cooldowns
openkakao-rs doctor [--loco]           # Environment, token, recovery, and safety diagnostics
```

LOCO commands automatically refresh tokens via login.json + X-VC when needed, and REST/LOCO now share the same persisted recovery state.

## Workflow (LOCO-first)

1. Quick sanity: `openkakao-rs --version && openkakao-rs loco-test`
2. Get chat IDs: `openkakao-rs loco-chats --all --json` *(note: `--all` can be slower)*
3. Send message: `openkakao-rs send -y <chat_id> "message text"` *(default prefix on; add `--no-prefix` to disable)*
4. Read messages: `openkakao-rs loco-read <chat_id> -n 50` (or `--all`)
5. Only when you need REST-only features: open KakaoTalk app → `openkakao-rs login --save` → `openkakao-rs auth`

## Watch automation workflow

Use this order:

1. Confirm `watch` behavior first: `openkakao-rs watch --help`
2. Start local-only with `--hook-cmd`
3. Add filters:
   - `--hook-chat-id`
   - `--hook-keyword`
   - `--hook-type`
4. Only then move to `--webhook-url` if the user explicitly wants external delivery
5. If using a webhook, prefer `--webhook-signing-secret` and tell the user to verify:
   - `X-OpenKakao-Timestamp`
   - `X-OpenKakao-Signature`

Local-first example:

```bash
openkakao-rs watch \
  --hook-cmd 'jq . > /tmp/openkakao-event.json' \
  --hook-chat-id 382416827148557 \
  --hook-type 1
```

Webhook example:

```bash
openkakao-rs watch \
  --webhook-url https://hooks.example.com/openkakao \
  --webhook-header 'Authorization: Bearer token' \
  --webhook-signing-secret 'super-secret' \
  --hook-keyword urgent
```

## Unattended and policy gates

OpenKakao separates:

- `--unattended`: declare non-interactive operation
- `--allow-non-interactive-send`: allow `send -y`, `send-file -y`, `send-photo -y`
- `--allow-watch-side-effects`: allow `watch --read-receipt`, `--hook-cmd`, `--webhook-url`

Recommended persistent config:

```toml
[mode]
unattended = true

[send]
allow_non_interactive = true
default_prefix = true

[watch]
allow_side_effects = true
default_max_reconnect = 10

[auth]
prefer_relogin = true
auto_renew = true

[safety]
min_unattended_send_interval_secs = 10
min_hook_interval_secs = 2
min_webhook_interval_secs = 2
hook_timeout_secs = 20
webhook_timeout_secs = 10
allow_insecure_webhooks = false
```

Interpretation:

- unattended sends are rate-limited by default
- local hooks are rate-limited and timed out
- webhooks are rate-limited, timed out, and default to HTTPS only unless localhost
- `auth-status` and `doctor` are the first checks before assuming a long-running job is healthy

## Speed tips

- Prefer **LOCO** for send/read/history — REST token expiry + `login --save` can block waiting on Cache.db.
- Cache `chat_id`s you use often; avoid running `loco-chats --all` repeatedly.
- Use `-y/--yes` for non-interactive sends when you're confident the `chat_id` is correct.

## Multiline (줄바꿈) 메시지 보내기

주의: 커맨드라인에서 `\n`을 그냥 쓰면 **줄바꿈이 아니라 문자 그대로** `\n`이 전송될 수 있음. 실제 개행 문자를 만들어서 인자로 넘겨야 함.

예시:

- bash/zsh:
  - `openkakao-rs send -y <chat_id> "$(printf '첫줄\n\n둘째줄')"`
- bash 전용($'' quoting):
  - `openkakao-rs send -y <chat_id> $'첫줄\n\n둘째줄'`
- fish:
  - `openkakao-rs send -y <chat_id> (printf '첫줄\n\n둘째줄')`

## Troubleshooting

### Token invalid or `-950` error

```bash
# Open KakaoTalk app first, then:
openkakao-rs login --save
openkakao-rs auth
openkakao-rs auth-status
```

LOCO commands auto-refresh tokens, so `-950` is usually handled automatically.

If the machine has been running unattended for a while, inspect:

- `openkakao-rs auth-status --json`
- `openkakao-rs doctor --loco`

Look for:

- `last_failure_kind`
- `consecutive_failures`
- `auth_cooldown_remaining_secs`
- `last_recovery_source`

### `login --save` seems to hang

`login --save` may wait until KakaoTalk updates Cache.db.

- Open KakaoTalk → open the chat list once (forces a cache refresh)
- (Optional) `openkakao-rs watch-cache --interval 2` to see when tokens change
- Or skip REST entirely and use LOCO (`loco-test` / `send` / `loco-read`).

### GETMSGS returns `-300`

This is expected on Mac (dtype=2). Use `loco-read` (SYNCMSG) instead of REST `read` (GETMSGS).

### Homebrew formula not found

```bash
brew tap JungHoonGhae/openkakao
brew update
brew install JungHoonGhae/openkakao/openkakao-rs
```

## Guardrails

- **Prefix/traceability**: By default, `openkakao-rs` prepends `🤖 [Sent via openkakao]` to outgoing messages. Use `--no-prefix` to disable it.
  - If you want a custom tag (e.g. `🤖 [openkakao]`), either add it *in the message text* (and keep default prefix), or disable the default prefix and add your own — avoid double-prefixing unless you want it.
- Use `-y/--yes` only when you are sure the `chat_id` is correct.
- Do not assume unattended send can burst freely; the CLI now rate-limits it by default.
- Avoid `--force` unless you know what you're doing (higher ban risk).
- Prefer `watch --hook-cmd` over webhooks when the task can stay on the same machine.
- If using `--webhook-url`, be explicit that chat content leaves the local trust boundary.
- Expect non-HTTPS remote webhooks to be blocked unless the user has explicitly loosened `safety.allow_insecure_webhooks`.
- Treat `watch` hooks/webhooks as best-effort delivery, not a durable queue or exactly-once event bus.
- Treat unattended mode as a policy decision. If the user is building a service, push them toward `config.toml` instead of repeating long flag strings.
- For macOS services, steer users toward `examples/launchd/` in the repo instead of ad-hoc LaunchAgent files.
- Do not expose personal chat content unless the user explicitly asks.
- Prefer summary/aggregation output for logs and reports.
