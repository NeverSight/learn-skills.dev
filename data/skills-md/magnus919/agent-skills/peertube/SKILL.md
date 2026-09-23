---
name: peertube
description: Browse PeerTube federated video from the terminal — instance stats, latest
  videos, video detail, comment threads, channels, accounts, instance-local search, and
  OAuth2 login with per-instance token persistence. Set PEERTUBE_SERVER to any instance;
  point it at sepiasearch.org for fediverse-wide search. Use when the user mentions
  PeerTube, federated video, SepiaSearch, or browsing a specific PeerTube instance.
  Do not use this skill for YouTube/Vimeo uploads, video editing, or installing and
  administering a PeerTube server.
license: MIT
compatibility: Requires Python 3.8+ and `requests`. Reads are anonymous; authenticated
  commands (`me`, `my-videos`) need a token from `scripts/peertube login`. Tokens persist
  per-instance to ~/.config/peertube/token.json (owner-only).
metadata:
  tags: peertube, federated-video, activitypub, video-platform, sepiasearch, api-client
  sources: https://docs.joinpeertube.org/api-rest-reference.html, https://sepiasearch.org/
---

# peertube — PeerTube federated video from the terminal

Browse any PeerTube instance — a federated deployment, not a single API — from the
terminal: instance stats, latest videos, full video detail, comment threads, channels,
accounts, and instance-local search. Authenticate with OAuth2 only for your own account
commands. Every command is read-only except `login`/`logout`.

## Setup

1. Choose the instance to talk to. Every command is per-instance; the API shape is
   identical everywhere, but accounts, tokens, rules, and catalogs are not:

```bash
export PEERTUBE_SERVER="https://<INSTANCE_HOST>"   # e.g. https://tilvids.com
```

   To search the whole fediverse instead of one instance, point the same variable at the
   public search index: `PEERTUBE_SERVER=https://sepiasearch.org` (same API shape — see
   [references/search-and-discovery.md](references/search-and-discovery.md)).

2. Nothing else is required to browse: videos, search, channels, comments, and instance
   info are anonymous reads.

3. (Optional) Log in only for your own account commands (`me`, `my-videos`):

```bash
scripts/peertube login --username <NAME> --prompt
```

### How authentication works

PeerTube uses plain OAuth2 with per-instance client credentials: the CLI anonymously
fetches the client pair from `GET /api/v1/oauth-clients/local` (singular `local`), then
exchanges your username/password for a bearer token at `POST /api/v1/users/token`
(`grant_type=password`, form-encoded). The token rides `Authorization: Bearer <token>`,
lives for the instance's configured lifetime (read `expires_in` from the response — do not
assume a fixed number), and is refreshed automatically when it expires. The token file is
written owner-only to `~/.config/peertube/token.json` keyed by server URL.
**Do not commit tokens** — they are account credentials; revoke with `scripts/peertube
logout` (`POST /users/revoke-token`) when done. Current production instances mask
`client_secret` in the API response; the CLI detects this and explains the workaround.
Details and wire-level error signatures:
[references/auth-and-tokens.md](references/auth-and-tokens.md).

## Essential Commands

### server — instance stats and identity (anonymous)

```bash
scripts/peertube server              # name, description, user/video/view counters
scripts/peertube server --json
```

Composes `GET /config/about` + `GET /server/stats` (canonical paths — there is no
`/instance/stats`).

### videos — browse the instance's uploads (anonymous)

```bash
scripts/peertube videos                       # latest 15, offset pagination
scripts/peertube videos --limit 50 --offset 50
scripts/peertube videos --sort -views --json  # popular first
```

Pagination is `start`/`count` offsets (max count 100) — the API has **no `page`
parameter**.

### search — find videos on THIS instance (anonymous)

```bash
scripts/peertube search --query "linux"            # instance-local (searchTarget=local)
scripts/peertube search -q "docker" --limit 20 --json
PEERTUBE_SERVER="https://sepiasearch.org" scripts/peertube search -q "linux"   # fediverse-wide
```

The bundled CLI performs **instance-local** search only (`searchTarget=local`). For
fediverse-wide search, point `PEERTUBE_SERVER` at SepiaSearch — same commands, wider
index. Search results carry `channel.host`/`url`, the origin instance of federated hits.

### video — full detail for one video (anonymous)

```bash
scripts/peertube video --id <UUID>          # numeric id, UUID, or shortUUID all work
scripts/peertube video --id <UUID> --json | jq '{name, description, views, url}'
```

### comments — top-level comment threads (anonymous)

```bash
scripts/peertube comments --id <UUID>                 # GET /videos/{id}/comment-threads
scripts/peertube comments --id <UUID> --limit 30 --json
```

### channels / channel / account — creators (anonymous)

```bash
scripts/peertube channels --limit 20 --json           # instance channel list
scripts/peertube channel --handle framasoft@framatube.org   # name or name@host
scripts/peertube account --name chocobozzz@framatube.org
```

`channel` shows metadata plus the channel's uploads (offset-paginated).

### me / my-videos — your account (requires login)

```bash
scripts/peertube me --json | jq '.role.label'
scripts/peertube my-videos --limit 50 --json
```

### login / logout — OAuth2 session management

```bash
scripts/peertube login --username <NAME> --prompt        # hidden prompt
echo "<PASSWORD>" | scripts/peertube login --username <NAME> --password-stdin
scripts/peertube login --username <NAME> --otp <CODE>    # 2FA-enabled accounts
scripts/peertube logout                                   # revoke server-side + delete file
```

## Global flags

```bash
scripts/peertube --json videos                     # flag before or after the subcommand
scripts/peertube videos --json
scripts/peertube --dry-run search --query test     # request plan, zero network
scripts/peertube --verbose videos --limit 2        # trace requests on stderr
scripts/peertube --server https://tilvids.com server   # per-invocation instance override
```

`--dry-run` emits `{"dry_run": true, "method", "path", "params"}` (login adds
`form_fields` names only, never values) — use it to verify a jq chain before running it
live. `--help` and `--dry-run` never require credentials.

## Pipeline recipes

### Search, then inspect the top hit

```bash
scripts/peertube search --query "linux" --limit 5 --json | jq -r '.videos[0].uuid'
scripts/peertube video --id "$(scripts/peertube search -q linux --limit 1 --json | jq -r '.videos[0].uuid')" --json
```

### Page through a channel's uploads

```bash
scripts/peertube channel --handle framasoft@framatube.org --limit 100 --offset 0 --json | jq -r '.videos[].name'
# loop: advance --offset by the returned count until you reach .total (no page param exists)
```

### Instance report card

```bash
scripts/peertube server --json | jq '{name: .instance.name, videos: .stats.totalLocalVideos, users: .stats.totalUsers, views: .stats.totalLocalVideoViews}'
```

### Log in, check quota, log out

```bash
scripts/peertube login --username <NAME> --prompt
scripts/peertube me --json | jq '{username, role: .role.label, quota_bytes: .videoQuota}'
scripts/peertube logout
```

## JSON and jq

`--json` output keys are stable snake_case wrappers around raw API objects: `videos`
(the API's `{total, data}` list objects), `channels`, `threads` (+ `total_not_deleted`),
`instance` + `stats`, `channel`, `dry_run`/`method`/`path`/`params` for plans. Video
objects keep PeerTube's own field names — `uuid`, `shortUUID`, `name`, `duration`
(seconds), `views`, `publishedAt`, `account{name,displayName,host}`,
`channel{name,displayName,host}` — so jq selectors transfer directly to raw `curl`
against `/api/v1`. Example: `jq -r '.videos[] | [.name, .views, .channel.displayName] | @tsv'`.

## Known Gotchas

- **Instances are independent (federated, not one API)** — accounts, tokens, rules,
  enabled features, and catalogs differ per instance. A token from instance A 401s on
  instance B; the CLI keys the token file by server URL. Content federated *onto* an
  instance still belongs to its origin (`channel.host`, video `url`).
- **Search scope is two different things** — `searchTarget=local` searches the
  instance's own catalog; `search-index` (or SepiaSearch's base URL) searches the
  fediverse via an external index. Omitting `searchTarget` gives the instance's own
  scope on current servers, not the fediverse. The bundled CLI is instance-local unless
  you point it at sepiasearch.org.
- **`page` does not exist** — collections paginate with `start`/`count` (max 100).
  Clients sending `page=` silently re-read the first page forever.
- **The comments route is `/comment-threads`** (hyphenated) — `/comments` and
  `/commentthreads` are not routes (they 400 on current servers).
- **Instance metadata paths are mixed** — stats at `/server/stats` (operation titled
  "instance stats"), about at `/config/about`, config at `/config`. No
  `/instance/*` metadata paths exist.
- **Production masks `client_secret`** — `oauth-clients/local` answers
  `"********************************"` on current production instances; a token request
  with the masked value 400s. The CLI detects it and explains the front-end-asset
  workaround. `response_type=code` appears in old quick-start curls but is not part of
  the current token schema — the CLI omits it.
- **Token lifetimes are instance-configurable** — read `expires_in` per response; the
  CLI persists the absolute `expires_at` and refreshes automatically. Store tokens
  owner-only, never commit them, revoke on logout (deleting the file alone leaves the
  session live).
- **2FA needs an OTP header** — `x-peertube-otp` on the token request; the CLI maps a
  bare 401 to "pass --otp".
- **Rate limits** — default 50 calls/10 s per IP (token endpoint tighter); on 429 read
  `Retry-After` and back off. Errors use RFC7807 `application/problem+json` bodies, and
  unknown routes answer 400 (not 404) — read the body.
- **`duration` is seconds**; ids are triple (`id`, `uuid`, `shortUUID` — all accepted by
  detail endpoints); `role` is an object `{id, label}`; `videoQuota` is bytes.
- **Anonymous vs authed** — browsing/search/comments/instance-info need no token;
  `/users/me*` and mutations always do.

## When to use

Use this skill for read-only interaction with PeerTube instances: browsing and filtering
videos, instance-local or fediverse-wide search (via SepiaSearch), video detail and
comments, channel/account exploration, instance stats, and managing your own account
session with OAuth2 (login, profile, my videos, logout).

## When not to use

Do not use this skill for YouTube, Vimeo, or other platform uploads or any video
editing/transcoding (route to those platforms' own tooling and ffmpeg); for installing,
hosting, or administering a PeerTube server (instance administration is out of scope —
the bundled CLI is read-only plus login/logout); or for generic ActivityPub/Mastodon
federation questions (use a Mastodon or ActivityPub skill).

## Reference Files

| File | Use it for |
| ---- | ---------- |
| [references/auth-and-tokens.md](references/auth-and-tokens.md) | OAuth2 flow (oauth-clients/local, password grant), secret masking, refresh/revocation, token-file hygiene, wire error signatures |
| [references/search-and-discovery.md](references/search-and-discovery.md) | searchTarget local vs search-index, SepiaSearch semantics, search parameters and sorts |
| [references/endpoint-catalog.md](references/endpoint-catalog.md) | Every read endpoint's parameters, response shapes, pagination, rate limits |
| [references/gotchas-field-guide.md](references/gotchas-field-guide.md) | Symptom → cause → fix table for every failure signature and version drift |
| [references/worked-recipes.md](references/worked-recipes.md) | Multi-step CLI/jq workflows, raw curl auth chain, jq processing patterns |

## Available Scripts and Prerequisites

- `scripts/peertube` — the bundled Python CLI (`--json`, `--dry-run`, `--verbose`,
  `--server` override). Imports only the standard library and `requests`.
- `scripts/test_peertube.py` — offline test suite (pytest + unittest compatible); all
  HTTP is mocked, zero network egress.
- Requires Python 3.8+ and `requests`. Any reachable PeerTube instance (or SepiaSearch)
  works; no credentials exist or are required by default. No service is started by this
  skill.
