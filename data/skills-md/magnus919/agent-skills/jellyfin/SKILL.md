---
name: jellyfin
description: Query your Jellyfin media server from the terminal — recently added media,
  search, item details, series navigation, next-up episodes, library browsing, server
  info, and user login. Use when the user asks about Jellyfin, media servers, movies, TV
  shows, next episodes, or their media library. Do not use this skill for server
  installation, library management, playback control, or Emby/Plex servers.
license: MIT
compatibility: Requires Python 3.8+ and `requests`. Authenticate with JELLYFIN_API_KEY
  (Dashboard → API Keys), a user access token from `login`, or Quick Connect; user-scoped
  commands (`recent`, `next-up`, `item`, `seasons`, `episodes`) also need JELLYFIN_USER_ID
  or --user-id.
metadata:
  tags: jellyfin, media-server, movies, tv, episodes, recently-added, library, home-media,
    api-client
  sources: https://api.jellyfin.org/, https://gist.github.com/nielsvanvelzen/ea047d9028f676185832e51ffaf12a6f
---

# jellyfin — Jellyfin Media Server from the Terminal

Query recently added movies and TV episodes, search and inspect media, walk series →
seasons → episodes, browse libraries, see next-up episodes, log in as a user, and check
server stats — all from your Jellyfin server's REST API. Every command is read-only
except `login`.

## Setup

1. Make sure your Jellyfin server is running and accessible (default `http://localhost:8096`).
2. Pick an authentication route:
   - **API key** — Dashboard → **API Keys** → `+`. Administrator-level, no user identity:
     every user-scoped command then needs an explicit user id.
   - **User token** — run `scripts/jellyfin login --username NAME --prompt` once; it
     prints the values to export.
3. Set these environment variables:

```bash
export JELLYFIN_URL="http://your-server:8096"   # include protocol and port
export JELLYFIN_API_KEY="your-api-key-here"     # or JELLYFIN_TOKEN after `login`
export JELLYFIN_USER_ID="your-jellyfin-user-id" # required by recent, next-up, item, seasons, episodes
```

Run the bundled CLI as `scripts/jellyfin`. `--help` and `--dry-run` work without
credentials.

### How authentication works

Jellyfin wants a `MediaBrowser`-scheme `Authorization` header on every call. The login
endpoint requires its `Client=..., Device=..., DeviceId=..., Version=...` quartet **before
any token exists** — the server rejects `POST /Users/AuthenticateByName` with
`400 Error processing request.` otherwise. Afterwards the access token (or API key) rides
the same header as `Token="..."`; the legacy `X-Emby-Token` header means the same thing
and is scheduled for removal from Jellyfin 12.0. The bundled CLI sends the modern form and
puts the token in exactly that one channel per request (never co-sends `X-Emby-Token`).
See [references/auth-and-sessions.md](references/auth-and-sessions.md).

## Essential Commands

### Authentication — get a session

```bash
scripts/jellyfin login --username alice --prompt          # prints JELLYFIN_* exports
echo "pw" | scripts/jellyfin login --username alice --password-stdin
scripts/jellyfin login --username alice --dry-run --json  # preview the pre-token header
```

`login` demonstrates the full researched sequence: complete pre-token MediaBrowser header
→ `POST /Users/AuthenticateByName` → capture `User.Id` + `AccessToken` → print the
post-token header for reuse. It never echoes the password.

### info — Server information

```bash
scripts/jellyfin info              # server name, version, OS, user count
scripts/jellyfin info --json
```

### recent — Recently added media

```bash
scripts/jellyfin recent                     # last 10 items added for JELLYFIN_USER_ID
scripts/jellyfin recent --movies --limit 5  # server-side includeItemTypes filter
scripts/jellyfin recent --episodes --limit 20 --json
scripts/jellyfin recent --user-id USER_ID   # override the env var
```

Hits `/Items/Latest` with `userId`; the response is a **bare JSON array** (no `Items`
wrapper), and `groupItems` merges episodes by series, so treat it as "what's new".

### search — Search your media library

```bash
scripts/jellyfin search --query "dune"                  # everything
scripts/jellyfin search --query "dune" --type Movie     # comma-separated types
scripts/jellyfin search --query "star trek" --type Series,Episode --limit 5 --json
```

Search hits `/Search/Hints`; results carry `id` (with a deprecated `ItemId` twin on old
servers — the CLI already prefers the modern field).

### Navigation — inspect items and walk series

```bash
scripts/jellyfin search --query "dune" --type Movie --json   # find an item ID
scripts/jellyfin item --id ITEM_ID                           # full metadata (needs user)
scripts/jellyfin seasons --series-id SERIES_ID               # list seasons
scripts/jellyfin episodes --series-id SERIES_ID --season-id SEASON_ID
scripts/jellyfin next-up --limit 10                          # next unwatched episodes
scripts/jellyfin next-up --series-id SERIES_ID --user-id USER_ID
```

`item`, `seasons`, `episodes`, and `next-up` are user-scoped: they require
`JELLYFIN_USER_ID` or `--user-id` and fail before any network call without one.

### libraries — browse a collection

```bash
scripts/jellyfin libraries                                   # library IDs and types
scripts/jellyfin browse --library-id LIBRARY_ID --type Movie --limit 50
scripts/jellyfin browse --library-id LIBRARY_ID --start-index 50   # paginate
scripts/jellyfin browse --library-id LIBRARY_ID --user-id USER_ID  # userId sent explicitly
```

`libraries` reads `/Library/MediaFolders`, which is **admin-only** — non-admin tokens get
403 and should use `/UserViews` (see references). `browse` pages `/Items` with
`startIndex`/`limit` and passes `userId` when provided, since servers using non-API-key
auth reject unscoped queries with `400 userId is required`.

### stats — Library statistics

```bash
scripts/jellyfin stats    # movie, series, episode, song counts (/Items/Counts)
```

## Pipeline recipes

### Find a series, then its next unwatched episode

```bash
scripts/jellyfin search --query "breaking bad" --type Series --json | jq -r '.results[0].id'
scripts/jellyfin next-up --series-id "$SERIES_ID" --user-id "$JELLYFIN_USER_ID" --json | jq -r '.items[0].name'
```

### Page through a whole library

```bash
scripts/jellyfin browse --library-id "$LIB_ID" --limit 100 --start-index 0 --json | jq -c '.items'
# loop: advance --start-index by the returned count until .total_record_count is reached
```

### Log in and persist a session

```bash
scripts/jellyfin login --username alice --prompt --json | jq -r '"\(.user_id) \(.access_token)"'
```

## JSON and jq

Put `--json` before or after the subcommand. Output keys are stable snake_case: `items`
(with `id`, `name`, `type`, `year`, `series`, `season_number`, `episode_number`),
`results`, `libraries`, `total_record_count`, `start_index`. `--dry-run` emits a plan
carrying `dry_run`, `path`, and `params` (`login` adds `authorization_header`; `info`
composes a `requests` list), matching what would be sent, so jq can verify a chain before
running it live. Exit codes: `0` success (including dry-run), `1` CLI/API errors, `2`
argument errors. Use `jq -r '.items[] | [.name, .year] | @tsv'` for tabular handoff.

## Known Gotchas

- **JELLYFIN_URL must include protocol and port** — e.g. `http://192.168.1.100:8096`.
- **User-scoped commands require an explicit user** — `recent`, `next-up`, `item`,
  `seasons`, `episodes` refuse to run without `JELLYFIN_USER_ID`/`--user-id`. The CLI
  never picks an administrator for you. A missing userId on user-token requests makes the
  server answer `400 userId is required`.
- **API keys have no user** — `/Users/Me` answers `400 Token is not owned by a user.` to
  API keys by design; per-user queries need an explicit user id (see
  [references/user-scoping-and-errors.md](references/user-scoping-and-errors.md)).
- **The login 400 vs 401 trap** — missing/partial MediaBrowser header → `400` with plain
  text `Error processing request.`; wrong credentials → `401`. Same endpoint, different
  failures.
- **Response shapes differ per endpoint** — `/Items` and `/Shows/*` wrap results in
  `{Items, TotalRecordCount, StartIndex}`; `/Items/Latest` returns a bare array; search
  uses a `SearchHints` key. Generic clients must branch (the CLI already does).
- **Recent type filtering is server-side** — `--movies`/`--episodes` become
  `includeItemTypes` before `limit`; no local filtering.
- **NextUp needs userId on every server version** — omitting it crashed servers ≤10.8 and
  silently scopes to the session user on ≥10.9. The CLI always sends it.
- **`libraries` is admin-only** — `/Library/MediaFolders` requires an administrator token;
  non-admin tokens get 403.
- **Legacy auth is going away** — `X-Emby-Token`, `X-MediaBrowser-Token`, and the
  `api_key` query parameter are deprecated; admins can already disable them (10.11+), and
  removal targets 12.0. Prefer the modern Authorization header the CLI sends.
- **Lazy auth** — `--help` and `--dry-run` work without credentials; dry-run never touches
  the network.

## When to use

Use this skill for read-only interaction with a running Jellyfin server: discovery of
what's new, searching and inspecting items, walking series and seasons, next-up planning,
library inventories, and obtaining a user session via `login` or Quick Connect.

## When not to use

Do not use this skill for server installation or administration (installing Jellyfin or
Emby, editing libraries, managing users) — every bundled command is read-only except
`login`. It does not target Plex or Kodi (different APIs — use their own tools), and it is
not a playback remote: route streaming or remote-control automation to Jellyfin's official
clients.

## Reference Files

| File | Use it for |
| ---- | ---------- |
| [references/auth-and-sessions.md](references/auth-and-sessions.md) | MediaBrowser header scheme, login flow, token channels, legacy deprecation, error signatures |
| [references/endpoint-catalog.md](references/endpoint-catalog.md) | Every read endpoint's parameters, response shapes, image URLs, pagination loop |
| [references/user-scoping-and-errors.md](references/user-scoping-and-errors.md) | The userId requirement matrix, API-key identity quirks, 400-vs-404 diagnosis |
| [references/gotchas-field-guide.md](references/gotchas-field-guide.md) | Wire-level failure signatures, version-drift ledger, mock shapes |
| [references/worked-recipes.md](references/worked-recipes.md) | Multi-step curl/jq and CLI recipes: login → latest, libraries → browse, search → seasons → episodes |
| [references/quick-connect.md](references/quick-connect.md) | Passwordless Quick Connect login flow |

## Available Scripts and Prerequisites

- `scripts/jellyfin` — the bundled Python CLI (`--json`, `--dry-run`, lazy auth).
  Imports only the standard library and `requests`.
- `scripts/test_jellyfin_cli.py` — offline test suite (pytest + unittest compatible);
  all HTTP behavior is mocked, zero network egress.
- Requires Python 3.8+ and `requests`. A running Jellyfin server (10.8+ assumed; tested
  behaviors anchored to the 12.0-era OpenAPI spec). No service is started by this skill.
