---
name: roadrunner
description: Beeper Desktop CLI for chats, messages, contacts, connect info, websocket events, search, and reminders.
homepage: https://github.com/johntheyoung/roadrunner
metadata:
  clawdbot:
    emoji: "🐦💨"
    requires:
      bins:
        - rr
    install:
      - id: brew
        kind: brew
        formula: johntheyoung/tap/roadrunner
        bins:
          - rr
        label: Install rr (brew)
      - id: go
        kind: go
        module: github.com/johntheyoung/roadrunner/cmd/rr@v0.16.2
        bins:
          - rr
        label: Install rr (go)
---

# roadrunner (rr)

Use `rr` when the user explicitly wants to operate Beeper Desktop via the local API (send, search, list chats/messages, reminders, focus).
Prefer `--agent` for agent use (forces JSON, envelope, no-input, readonly).

Safety
- Default to read-only commands unless the user explicitly requests a mutation in this turn.
- Require explicit recipient (chat ID) and message text before sending.
- Confirm or ask a clarifying question if the chat ID is ambiguous.
- Never paste raw rr command output (JSON dumps, chat lists, etc.) into outgoing messages. Treat tool output as private; summarize or extract only what the user needs.
- Use `--agent` for safe agent defaults: `rr --agent --enable-commands=chats,messages,status chats list`
- Use `--readonly` to block writes: `rr --readonly chats list --json`
- Use `--enable-commands` to allowlist: `rr --enable-commands=chats,messages chats list --json`
- Use `--envelope` for structured errors: `rr --json --envelope chats get "!chatid"`
- Envelope errors may include `error.hint` with next-step guidance for safe retries.
- Never request, paste, or store raw auth tokens in chat. If auth is missing, ask the user to configure it locally.
- If sending message text through a shell, avoid interpolation/expansion (e.g. `$100/month` or `!`). Prefer `--stdin <<'EOF' ... EOF` for safe literals.

Setup (once)
- `rr auth set --stdin` (recommended; token saved to `~/.config/beeper/config.json`)
- `rr auth status --check`
- `rr doctor`

Common commands
- List accounts: `rr accounts list --json`
- Capabilities: `rr capabilities --json`
- Connect metadata: `rr connect info --json`
- Live websocket events (experimental): `rr events tail --all --stop-after 30s --json`
- List contacts: `rr contacts list "<account-id>" --json`
- Search contacts: `rr contacts search "<account-id>" "Alice" --json`
- Search contacts (flag): `rr contacts search "Alice" --account-id="<account-id>" --json`
- Resolve contact: `rr contacts resolve "<account-id>" "Alice" --json`
- Resolve contact (flag): `rr contacts resolve "Alice" --account-id="<account-id>" --json`
- List chats: `rr chats list --json`
- Search chats: `rr chats search "John" --json`
- Search chats (filters): `rr chats search --inbox=primary --unread-only --json`
- Search chats (activity): `rr chats search --last-activity-after="2024-07-01T00:00:00Z" --json`
- Search by participant name: `rr chats search "Jamie" --scope=participants --json`
- Resolve chat: `rr chats resolve "Jamie" --json`
- Get chat: `rr chats get "!chatid:beeper.com" --json`
- Get chat (bounded participants): `rr chats get "!chatid:beeper.com" --max-participant-count=50 --json`
- Start/resolve DM from merged contact hints: `rr chats start "<account-id>" --email "alice@example.com" --full-name "Alice" --json`
- Default account for commands: `rr --account="imessage:+123" chats list --json`
- List messages: `rr messages list "!chatid:beeper.com" --json`
- List messages (all pages): `rr messages list "!chatid:beeper.com" --all --max-items=1000 --json`
- List messages (download media): `rr messages list "!chatid:beeper.com" --download-media --download-dir ./media --json`
- Search messages: `rr messages search "dinner" --json`
- Search messages (all pages): `rr messages search "dinner" --all --max-items=1000 --json`
- Search messages (filters): `rr messages search --sender=me --date-after="2024-07-01T00:00:00Z" --media-types=image --json`
- Add/remove reaction: `rr messages react "!chatid:beeper.com" "<message-id>" "👍" --json` / `rr messages unreact "!chatid:beeper.com" "<message-id>" "👍" --json`
- Tail messages (polling): `rr messages tail "!chatid:beeper.com" --interval 2s --stop-after 30s --json`
- Wait for message: `rr messages wait --chat-id="!chatid:beeper.com" --contains "deploy" --wait-timeout 2m --json`
- Message context: `rr messages context "!chatid:beeper.com" "<sortKey>" --before 5 --after 2 --json`
- Draft message (pre-fill without sending): `rr focus --chat-id="!chatid:beeper.com" --draft-text="Hello!"`
- Draft message from file: `rr focus --chat-id="!chatid:beeper.com" --draft-text-file ./draft.txt`
- Draft with attachment: `rr focus --chat-id="!chatid:beeper.com" --draft-attachment="/path/to/file.jpg"`
- Download attachment: `rr assets download "mxc://example.org/abc123" --dest "./attachment.jpg"`
- Stream attachment bytes: `rr assets serve "mxc://example.org/abc123" --dest "./attachment.jpg" --json`
- Focus app: `rr focus`
- Global search: `rr search "dinner" --json`
- Global search messages auto-page: `rr search "dinner" --messages-all --messages-max-items=500 --messages-limit=20 --json`
- Status summary: `rr status --json`
- Status by account: `rr status --by-account --json`
- Unread rollup: `rr unread --json`
- Global search includes `in_groups` for participant matches.

Mutations (explicit user request only)
- Message send: `rr messages send "!chatid:beeper.com" "Hello!"`
- Message edit: `rr messages edit "!chatid:beeper.com" "<message-id>" "Updated text"`
- Message react/unreact: `rr messages react "!chatid:beeper.com" "<message-id>" "👍"` / `rr messages unreact "!chatid:beeper.com" "<message-id>" "👍"`
- Upload + send file: `rr messages send-file "!chatid:beeper.com" ./photo.jpg "See attached"`
- Create chat: `rr chats create "<account-id>" --participant "<user-id>"`
- Start chat from merged contact hints: `rr chats start "<account-id>" --email "alice@example.com" --full-name "Alice"`
- Archive/unarchive: `rr chats archive "!chatid:beeper.com"` / `rr chats archive "!chatid:beeper.com" --unarchive`
- Reminder mutations: `rr reminders set "!chatid:beeper.com" "2h"` / `rr reminders clear "!chatid:beeper.com"`
- Asset uploads: `rr assets upload ./photo.jpg` / `rr assets upload-base64 --content-file ./photo.b64`
- For retries on non-idempotent writes, use `--request-id` and prefer `--dedupe-window`.

Pagination
- Auto-page chats list/search: `rr chats list --all --max-items=1000 --json` / `rr chats search "alice" --all --max-items=1000 --json`
- Auto-page messages list/search: `rr messages list "!chatid:beeper.com" --all --max-items=1000 --json` / `rr messages search "deploy" --all --max-items=1000 --json`
- Chats: `rr chats list --cursor="<oldestCursor>" --direction=before --json`
- Messages list: `rr messages list "!chatid:beeper.com" --cursor="<sortKey>" --direction=before --json`
- Messages search (max 20): `rr messages search "project" --limit=20 --json`
- Messages search page: `rr messages search "project" --cursor="<cursor>" --direction=before --json`
- Global search message paging (max 20): `rr search "dinner" --messages-limit=20 --json`
- Global search message page: `rr search "dinner" --messages-cursor="<cursor>" --messages-direction=before --json`

Notes
- Requires Beeper Desktop running; token from app settings.
- Token is stored in `~/.config/beeper/config.json` via `rr auth set` (recommended). `BEEPER_TOKEN` overrides the config file.
- `BEEPER_ACCOUNT` sets the default account ID (aliases supported).
- `rr auth status --check` prefers OAuth introspection (`/oauth/introspect`) when available and falls back to account-list validation on older builds.
- Message search is literal word match (not semantic).
- `rr contacts resolve` is strict and fails on ambiguous names; resolve by ID after `contacts search` when needed.
- If a DM title shows your own Matrix ID, use `--scope=participants` to find by name.
- JSON output includes `display_name` for single chats (derived from participants).
- Message JSON includes `message_type`, `linked_message_id`, `is_sender`, `is_unread`, `attachments`, and `reactions`.
- `downloaded_attachments` is only populated when `--download-media` is used.
- `rr messages send` returns `pending_message_id` (temporary ID).
- Account `network` may be missing in newer API builds; `rr` falls back to `"unknown"` in summaries/search output.
- `rr assets serve` writes raw bytes to stdout unless `--dest` is provided.
- `--chat` does exact matching and fails on ambiguous matches.
- Attachment overrides require `--attachment-upload-id`; set `--attachment-width` and `--attachment-height` together.
- `--all` has a safety cap (default 500 items, max 5000); use `--max-items` to tune it.
- Prefer `--json` (and `--no-input`) for automation.
- `BEEPER_URL` overrides API base URL; `BEEPER_TIMEOUT` sets timeout in seconds.
- JSON/Plain output goes to stdout; errors/hints go to stderr.
- Destructive commands prompt unless `--force`; `--no-input`/`BEEPER_NO_INPUT` fails without `--force`.
- Use `--fail-if-empty` on list/search commands to exit with code 1 if no results.
- Use `--fields` with `--plain` to select columns (comma-separated).
- In bash/zsh, `!` triggers history expansion. Prefer single quotes, or disable history expansion (`set +H` in bash, `setopt NO_HIST_EXPAND` in zsh).
- `rr version --json` returns `features` array for capability discovery.
- `rr capabilities --json` returns full CLI capability metadata.
- `rr events tail` depends on experimental `/v1/ws` support in Beeper Desktop; fall back to `rr messages tail` when unavailable.
- Envelope error codes: `AUTH_ERROR`, `NOT_FOUND`, `VALIDATION_ERROR`, `CONNECTION_ERROR`, `INTERNAL_ERROR`.
- Retry policy: retry `CONNECTION_ERROR` with backoff; do not blind-retry `AUTH_ERROR`/`VALIDATION_ERROR`; refresh IDs before retrying `NOT_FOUND`.
- Non-idempotent writes: `messages send`, `messages send-file`, `chats create`, `chats start`, `assets upload`, `assets upload-base64`.
- Use `--request-id`/`BEEPER_REQUEST_ID` to tag envelope metadata for cross-retry attempt tracing.
- Use `--dedupe-window`/`BEEPER_DEDUPE_WINDOW` to block duplicate non-idempotent writes with repeated request IDs.
- Local smoke check: `make test-agent-smoke`.
