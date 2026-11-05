---
name: telegram-log-sidecar
description: Create and configure a Telegram log forwarding sidecar container for Docker Compose stacks. Tails logs from sibling services via the Docker socket and forwards filtered lines to a Telegram chat via Bot API. Use when the user wants Telegram alerts/notifications from container logs, a log shipping sidecar, observability via Telegram, or asks to "set up Telegram logs", "telegram sidecar", "forward container logs to Telegram", "log alerts to Telegram".
---

# Telegram Log Sidecar

Sidecar container that tails Docker Compose service logs via the Docker socket and forwards matching lines to a Telegram chat. Pure bash + `docker:cli` + `curl` + `jq` + `perl`. No persistent state. Per-service include/exclude regex filtering.

## When to Use

- Need lightweight log alerts to Telegram without Loki/Grafana/Promtail stack.
- Want errors or specific log patterns from selected services pushed to a chat.
- Adding observability to a Docker Compose deploy where ops watches a Telegram channel.
- Migrating from raw `docker logs` watching to filtered, formatted notifications.

## When NOT to Use

- High-volume logs (Telegram rate-limits ~30 msgs/sec global, 1 msg/sec per chat). Use Loki/ELK instead.
- Kubernetes — sidecar uses Docker socket, not k8s logging primitives. Use Fluent Bit DaemonSet.
- Need log retention/search — sidecar is fire-and-forget, no storage.
- Logs contain secrets and chat is shared — sidecar has no redaction. Add include/exclude regex or build a redaction step first.

## Architecture

```
┌──────────────────────────────────────────────┐
│ Docker host                                   │
│                                              │
│  ┌─────────┐  ┌─────────┐  ┌──────────────┐ │
│  │ backend │  │   db    │  │ telegram-    │ │
│  │         │  │         │  │ log-sidecar  │ │
│  └─────────┘  └─────────┘  └──────┬───────┘ │
│       │           │                │         │
│       └───────────┴───stdout───────┤         │
│                                    │         │
│  /var/run/docker.sock ◄────────────┘ (ro)   │
└────────────────────────────────────┬─────────┘
                                     │
                                     ▼
                          api.telegram.org/bot<TOKEN>
                                     │
                                     ▼
                              [Telegram chat]
```

Sidecar resolves its own Compose project via `com.docker.compose.project` label on `$HOSTNAME`, then `docker logs --follow` each configured service container. Reconnects on container restart.

## Setup Steps

### 1. Create Telegram bot + get chat ID

1. DM `@BotFather` on Telegram → `/newbot` → save the token (`TELEGRAM_BOT_TOKEN`).
2. Create a channel/group OR DM the bot. Add bot as admin if channel.
3. Send any message to it. Then:
   ```bash
   curl "https://api.telegram.org/bot<TOKEN>/getUpdates" | jq '.result[].message.chat'
   ```
4. Copy `id` (negative for groups/channels) → `TELEGRAM_CHAT_ID`.

### 2. Copy sidecar files into the project

Place under `ops/telegram-log-sidecar/`:
- `Dockerfile` — see `templates/Dockerfile`
- `entrypoint.sh` — see `templates/entrypoint.sh` (chmod +x)

### 3. Add service to `docker-compose.prod.yml`

```yaml
  telegram-log-sidecar:
    build:
      context: ./ops/telegram-log-sidecar
      dockerfile: Dockerfile
    image: ${TELEGRAM_LOG_SIDECAR_IMAGE:-myapp-telegram-log-sidecar:latest}
    env_file:
      - .env
    depends_on:
      - backend
      - db
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
    networks:
      - internal
    restart: unless-stopped
```

Critical bits:
- **`/var/run/docker.sock:ro`** — sidecar needs read access to discover sibling containers and stream logs.
- **`env_file: .env`** — reads `TELEGRAM_*` vars from same env file as app.
- **`depends_on`** — list the services you want tailed (so sidecar starts after them).
- **Network** — only needs internet egress to `api.telegram.org`. `internal` bridge fine if it has outbound NAT; otherwise put on the `proxy` network.

### 4. Configure `.env`

Minimum:
```bash
TELEGRAM_LOGS_ENABLED=true
TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
TELEGRAM_CHAT_ID=-1001234567890
TELEGRAM_LOG_SERVICES=backend,db
```

Optional:
```bash
# Global filters (apply to all services unless overridden)
TELEGRAM_LOG_INCLUDE_REGEX=ERROR|FATAL|panic
TELEGRAM_LOG_EXCLUDE_REGEX=healthcheck|/metrics

# Per-service overrides — suffix = service name UPPERCASED, hyphens → underscores
TELEGRAM_LOG_INCLUDE_REGEX_BACKEND=^\[ERROR\]|Unhandled
TELEGRAM_LOG_EXCLUDE_REGEX_DB=checkpoint complete|autovacuum

# Tuning
TELEGRAM_WATCH_INTERVAL_SECONDS=5      # poll interval while waiting for containers
TELEGRAM_MAX_MESSAGE_LENGTH=4000       # Telegram hard limit is 4096; leave headroom
TELEGRAM_API_BASE=https://api.telegram.org  # override for local mock
```

Service-name → env-var-suffix mapping rule: `tr '[:lower:]-' '[:upper:]_'`. E.g. `worker-queue` → `TELEGRAM_LOG_INCLUDE_REGEX_WORKER_QUEUE`.

### 5. Deploy

```bash
docker compose -f docker-compose.prod.yml up -d --build telegram-log-sidecar
docker compose -f docker-compose.prod.yml logs -f telegram-log-sidecar
```

Expected boot log:
```
[telegram-log-sidecar] Resolved Docker Compose project: myapp.
[telegram-log-sidecar] Following logs from service backend (myapp-backend-1).
[telegram-log-sidecar] Following logs from service db (myapp-db-1).
```

## Behavior Details

- **Disabled by default** — if `TELEGRAM_LOGS_ENABLED != "true"`, sidecar runs `tail -f /dev/null` (no-op). Safe to leave in compose file across environments.
- **Filtering pipeline** per line: strip ANSI → trim whitespace → drop if empty → check include regex (global or per-service) → check exclude regex → send.
- **Per-service regex takes precedence over global.** Both empty = forward all non-empty lines.
- **Regex engine = Perl** (`perl -e`). Use PCRE syntax, not POSIX BRE.
- **Long lines** chunked at `TELEGRAM_MAX_MESSAGE_LENGTH - len("[service] ")`.
- **Rate limit handling** — on HTTP 429, respects `parameters.retry_after` once. Subsequent 429s drop the message (logs error). Tune your include regex to reduce volume.
- **Auto-reconnect** — if `docker logs --follow` exits (container restart), sidecar retries every `TELEGRAM_WATCH_INTERVAL_SECONDS`.
- **Tail starts at `--tail 0`** — only NEW lines after sidecar attaches. Historical logs are NOT replayed.
- **No message formatting** — `parse_mode` not set, so Markdown/HTML in logs render as plain text. Add `--data-urlencode "parse_mode=MarkdownV2"` in `send_telegram_request` only if you also escape special chars.

## Common Adjustments

### Add a new service to watch

1. Append name to `TELEGRAM_LOG_SERVICES` (comma-separated).
2. Add to `depends_on` in compose.
3. Optionally set per-service regex.
4. `docker compose up -d telegram-log-sidecar` (no rebuild needed — config is env-only).

### Throttle noisy service

Set `TELEGRAM_LOG_INCLUDE_REGEX_<SERVICE>` to only errors:
```bash
TELEGRAM_LOG_INCLUDE_REGEX_BACKEND=ERROR|FATAL|Unhandled|panic:|Traceback
```

### Multiple chats (e.g. errors → ops, all → debug)

Run two sidecars with different service names + different `TELEGRAM_CHAT_ID`:
```yaml
  telegram-log-errors:
    extends: telegram-log-sidecar
    environment:
      TELEGRAM_CHAT_ID: ${TELEGRAM_ERRORS_CHAT_ID}
      TELEGRAM_LOG_INCLUDE_REGEX: ERROR|FATAL
  telegram-log-debug:
    extends: telegram-log-sidecar
    environment:
      TELEGRAM_CHAT_ID: ${TELEGRAM_DEBUG_CHAT_ID}
```

(Or duplicate the full block — `extends:` is deprecated in compose v2.)

### Format messages (HTML/Markdown)

Edit `send_telegram_request` in `entrypoint.sh`:
```bash
--data-urlencode "parse_mode=HTML"
```
Then escape `<`, `>`, `&` in `send_log_line` before sending. MarkdownV2 requires escaping `_*[]()~\`>#+-=|{}.!` — more painful.

## Security

- **Docker socket mount is privileged-equivalent.** Sidecar can `docker exec` into any container, read all env vars, mount any volume. Treat the image as part of the trust boundary. Only build from sources you control.
- **Bot token in `.env`** — keep `.env` gitignored. Rotate via BotFather if leaked.
- **Logs may contain secrets** (JWTs, API keys in stack traces). Audit your services' log output before pointing this at a shared chat. Use `TELEGRAM_LOG_EXCLUDE_REGEX` for known patterns: `EXCLUDE_REGEX=Authorization:|password=|token=`.
- **Read-only socket** (`:ro`) prevents `docker run`/`exec` from sidecar but it can still read everything.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Waiting for Docker Compose project label on container ...` forever | Sidecar not started by `docker compose` (e.g. `docker run` standalone) | Use `docker compose up`, or set `COMPOSE_PROJECT_NAME` env var explicitly |
| `Waiting for running container of service X...` | Service name typo or not running | Check `docker compose ps`. Name must match the compose service key, not container name |
| `Telegram log forwarding is disabled` | `TELEGRAM_LOGS_ENABLED` unset or not `"true"` | Set to literal string `true` |
| `Failed to send Telegram message (HTTP 401)` | Bad bot token | Re-check `TELEGRAM_BOT_TOKEN` |
| `Failed to send Telegram message (HTTP 400) ... chat not found` | Wrong chat ID, or bot not added to group/channel | Re-run `getUpdates`; add bot to group; for channels, bot needs admin |
| Messages duplicated | Two sidecars watching same service | Check `docker compose ps` for stale containers |
| ANSI escape codes visible | `strip_ansi` regex missed exotic sequence | Extend the sed pattern in `strip_ansi()` |
| Lines truncated | `TELEGRAM_MAX_MESSAGE_LENGTH` too low | Raise toward 4096 (hard Telegram limit) |
| Sidecar CPU spike | Very chatty service with no filter | Add `TELEGRAM_LOG_INCLUDE_REGEX_<SERVICE>` |

## Files in This Skill

- `templates/Dockerfile` — copy to `ops/telegram-log-sidecar/Dockerfile`
- `templates/entrypoint.sh` — copy to `ops/telegram-log-sidecar/entrypoint.sh` (chmod +x)
- `templates/compose-snippet.yml` — paste into `docker-compose.prod.yml` `services:` block
- `templates/.env.example` — append to project `.env`
