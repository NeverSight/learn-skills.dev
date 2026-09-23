---
name: transistor
description: >-
  Operate Transistor.fm podcast hosting from the terminal: verify API access,
  browse shows and episodes with JSON:API-aware output, run the episode
  publish lifecycle (create draft, attach audio, publish or schedule via the
  dedicated publish endpoint), pull download analytics, and manage private
  podcast subscribers and webhooks. Use when the user mentions Transistor,
  Transistor.fm, podcast hosting, episode publishing, private podcast
  subscribers, or podcast download analytics. Do not use this skill for other
  podcast hosts (Buzzsprout, Libsyn, Megaphone, Spotify for Creators), for
  editing or producing audio, or for feed/RSS parsing — the bundled CLI
  manages a Transistor account through its v1 API and cannot create new
  shows (dashboard-only).
license: MIT
compatibility: Requires TRANSISTOR_API_KEY env var (Account page -> API Access
  at https://dashboard.transistor.fm/account), Python 3.8+, and `requests`.
  Read commands need a working key; `--help` and `--dry-run` never do.
metadata:
  tags: transistor, podcast, podcast-hosting, episodes, analytics, api-client
  sources: https://developers.transistor.fm/, https://support.transistor.fm/
---

# transistor — Transistor.fm podcast hosting from the terminal

Drive a Transistor.fm account over its v1 JSON:API: shows, episodes, the
draft→publish lifecycle, per-day download analytics, private-podcast
subscribers, and webhooks. Responses are JSON:API documents; the bundled CLI
unwraps them (`--json`) while preserving the raw shapes agents need for jq.
Write commands are guarded: episode creation is always a draft, and
publishing goes through its own dedicated endpoint.

## Setup

1. Find your API key on the Transistor dashboard **Account page → API
   Access** (https://dashboard.transistor.fm/account) and export it:

```bash
export TRANSISTOR_API_KEY="<API_KEY>"
```

2. Verify the key (GET /v1 — the authorization probe; there is no
   /v1/user route):

```bash
transistor user          # name and time zone
transistor user --json | jq '{id, name, time_zone}'
```

A key carries the dashboard role of its user (owner / admin / team member)
per podcast. `--help` and `--dry-run` work without credentials. Requests are
rate-limited to 10 per 10 seconds; the CLI dies with a clear 429 message
instead of hammering.

## Essential Commands

### user — authorization probe

```bash
transistor user                # who does this key belong to?
transistor user --json
```

### shows / show — browse podcasts

```bash
transistor shows                          # newest-updated first
transistor shows --private --json         # private podcasts only
transistor show --id <SHOW_ID_OR_SLUG>    # full attributes incl. feed_url
transistor shows --page 1 --per 20 --json
```

Show ids and slugs are interchangeable on most show-scoped routes. Show
resources carry no counts fields — count via `episodes --show ... --json`,
then `meta.totalCount`.

### episodes / episode — browse episodes

```bash
transistor episodes                                    # newest first, all shows
transistor episodes --show <SHOW_ID> --status draft    # drafts for one show
transistor episodes --show <SHOW_ID> --per 50 --page 1 --json
transistor episode --id <EPISODE_ID> --include show    # compound doc + parent show
```

`--include show` adds `included[]` (the JSON:API compound document); every
episode item in `--json` output already carries `show_id` resolved from
relationships. `--limit` works as an alias for `--per` for old scripts.

### episode-create / episode-update — drafts and metadata

```bash
transistor episode-create --show <SHOW_ID> --title "Ep 12: Roasting" \
  --season 2 --number 4 --audio-url "https://uploads.example.com/ep12.mp3"
transistor episode-update --id <EPISODE_ID> --title "New title"
transistor episode-update --id <EPISODE_ID> --audio-url "<AUDIO_URL>"   # attach audio
```

`episode-create` ALWAYS produces a draft (`status: "draft"`,
`published_at: null`) — it never publishes. `episode-update` changes
metadata or attaches audio and never touches publishing state.

### episode-publish — the lifecycle switch

```bash
transistor episode-publish --id <EPISODE_ID>                       # publish now
transistor episode-publish --id <EPISODE_ID> --status scheduled \
  --published-at "2026-09-03 09:00:00"                             # schedule
transistor episode-publish --id <EPISODE_ID> --status draft        # unpublish
```

Hits `PATCH /v1/episodes/<EPISODE_ID>/publish` with
`episode[status]=draft|scheduled|published` — the documented dedicated
endpoint. The CLI refuses to publish an episode whose `media_url` is still
empty (an unplayable item would hit every subscriber's feed); pass
`--force` to override.

### authorize-upload — local audio (max 5GB)

```bash
transistor authorize-upload --filename ep12.mp3                 # plan only
transistor authorize-upload --filename ep12.mp3 --file ./ep12.mp3
```

Returns (and, with `--file`, performs) the signed PUT; the printed
`audio_url` is what you attach with `episode-create`/`episode-update`. The
signed URL expires (~600 s in the docs' example).

### analytics / episode-analytics — downloads per day

```bash
transistor analytics --show <SHOW_ID>                        # last 14 days
transistor analytics --show <SHOW_ID> \
  --start-date 01-08-2026 --end-date 28-08-2026 --json
transistor episode-analytics --id <EPISODE_ID> --json
```

Dates are dd-mm-yyyy and must come in pairs. Analytics attributes are
per-day `downloads[]` arrays, not totals; the CLI sums them into
`downloads_total` and keeps the raw array.

### subscribers — private podcast audience

```bash
transistor subscribers --show <SHOW_ID> --json
transistor subscriber-create --show <SHOW_ID> --email "listener@example.com"
transistor subscriber-batch --show <SHOW_ID> --email "a@example.com" --email "b@example.com"
transistor subscriber-delete --show <SHOW_ID> --email "a@example.com"   # or --id
```

### webhooks — push instead of poll

```bash
transistor webhooks --show <SHOW_ID>
transistor webhook-create --show <SHOW_ID> --event episode_published \
  --url "https://example.com/hooks/transistor"
transistor webhook-delete --id <WEBHOOK_ID>
```

Events: `episode_created`, `episode_published`, `subscriber_created`,
`subscriber_deleted`. Cap: 50 per account. With a 10 req / 10 s limit,
webhooks beat polling for freshness.

## Global flags

```bash
transistor --json shows                        # flags work in any position
transistor --dry-run episodes --show <SHOW_ID> # request plan, zero network
transistor --force episode-publish --id <EPISODE_ID>   # skip the audio guard
transistor --quiet shows                       # suppress non-essential output
transistor --verbose episodes                  # detailed stderr logging
```

`--dry-run` emits `{"dry_run": true, "method", "path", "params"}` (write
commands add the exact `body` that would be sent — bracket keys and all),
so you can verify a plan before touching the API. `--help` and `--dry-run`
never require credentials.

## Pipeline recipes

### Create, attach audio, publish (the core workflow)

```bash
export TRANSISTOR_API_KEY="<API_KEY>"
SHOW=$(transistor shows --json | jq -r '.shows[0].id')          # string id
AUDIO=$(transistor authorize-upload --filename ep12.mp3 --file ./ep12.mp3 --json | jq -r '.audio_url')
EP=$(transistor episode-create --show "$SHOW" --title "Ep 12" \
     --audio-url "$AUDIO" --json | jq -r '.id')                 # draft id
transistor episode-publish --id "$EP"                           # dedicated endpoint
transistor episode --id "$EP" --json | jq '{status, media_url, published_at}'
```

Each stage's output feeds the next: `shows` → string `id`,
`authorize-upload` → string `audio_url`, `episode-create` → string draft
`id`, `episode-publish` → final `status`. Stage 2 is skippable when the
audio already has a public URL (pass it straight to `episode-create`).

### Draft triage: what is not out yet?

```bash
transistor episodes --show <SHOW_ID> --status draft --json \
  | jq -r '.episodes[] | [.id, .title, (if .media_url == "" then "no-audio" else "ready" end)] | @tsv'
# publish the ready ones (rate limit: 10 req / 10 s — add sleep 1 between calls)
```

### Weekly downloads report

```bash
transistor shows --json | jq -r '.shows[].id' | while read -r S; do
  transistor analytics --show "$S" --json \
    | jq -r --arg id "$S" '[$id, (.downloads_total|tostring)] | @tsv'
  sleep 1
done
```

## JSON and jq

`--json` keys are stable snake_case wrappers around the JSON:API document:
`shows`/`episodes`/`subscribers`/`webhooks` (arrays with `meta` attached),
flat objects for single resources, `dry_run`/`method`/`path`/`params`/`body`
for plans. Attributes keep Transistor's own names — `status`, `season`,
`number`, `duration` (seconds), `media_url`, `share_url`, `published_at`,
`feed_url` — so jq selectors transfer directly to raw `curl` against
api.transistor.fm. Collection pagination surfaces as
`meta.currentPage`/`meta.totalPages`/`meta.totalCount`. Example:
`transistor episodes --show <SHOW_ID> --json | jq -r '.episodes[] |
[.id, .title, .status] | @tsv'`. For compound documents the CLI resolves
relationships (`show_id`) and prints `included` show summaries in human
mode; with raw curl, match `included[]` by `type` and
`relationships.show.data.id`.

## Known Gotchas

- **Publishing is a separate endpoint, never a side effect** — POST
  /episodes and PATCH /episodes/:id cannot change `status`. If an episode
  stays draft, the missing step is `PATCH /v1/episodes/<ID>/publish` with
  `episode[status]=published`. (The pre-thickening CLI had no publish path
  at all.)
- **The user probe is `GET /v1`** — `/v1/user` and `/v1/authorization` are
  404s, and the user resource has no email attribute (name and time_zone
  only).
- **Pagination is `pagination[page]` + `pagination[per]`** (defaults 0 and
  10; docs' examples request page 1). `pagination[limit]` and
  `page[number]` are silently ignored — loops using them re-read page 1
  forever. Loop while `meta.currentPage < meta.totalPages`.
- **Show resources carry no counts** — derive episode/subscriber counts
  from filtered listings' `meta.totalCount`.
- **Analytics are per-day arrays, not totals** — sum `attributes.downloads`
  (the CLI provides `downloads_total`); date bounds are dd-mm-yyyy and
  come in pairs; do not parse the row date format (docs' examples are
  inconsistent between sections).
- **Show creation is dashboard-only** — there is no POST /v1/shows;
  `show-update` is the only show write.
- **Rate limit 10 req / 10 s** — a 429 blocks access for 10 seconds. No
  retry headers; back off, batch subscriber imports, cache responses, and
  use webhooks for freshness. Transistor explicitly forbids using the API
  as a website back end (parse the RSS feed for that).
- **`episode[published_at]` uses the show's time zone** (a show attribute),
  not UTC; scheduling and backdating both ride the publish endpoint.
- **Audio processing is asynchronous** — watch `audio_processing` /
  `processing_failure` after attaching audio; publishing an unprocessed or
  failed file pushes silence to subscribers.
- **Signed upload URLs expire** (~600 s in the docs' example): authorize,
  PUT with the returned `content_type`, attach promptly.
- **Error bodies are not formally specified** — the CLI handles JSON:API
  `errors[]` arrays and bare `{"message": ...}` objects, flattening either
  to one stderr line; 401 (bad key), 403 (role), 404 (bad id/route), 429
  (rate limit) have distinct hints.

## When to use

Use this skill for anything that reads or drives a Transistor.fm account
through its API: verifying API access, browsing shows/episodes (including
drafts and compound documents), running the episode lifecycle
(create → attach audio → publish/schedule/unpublish), pulling download
analytics windows, importing or revoking private-podcast subscribers, and
registering webhooks.

## When not to use

Do not use this skill for other podcast hosts (Buzzsprout, Libsyn,
Megaphone, Spotify for Creators — use their own APIs/tooling); for audio
production or editing (ffmpeg and DAW territory); for generic RSS feed
parsing or website rendering (parse the feed XML directly — Transistor says
the API is not a back-end data source); for creating new shows (the API
cannot — the dashboard does); or for platform-level distribution questions
(Apple/Spotify submission is a dashboard and RSS concern).

## Reference Files

| File | Use it for |
| ---- | ---------- |
| [references/auth-and-basics.md](references/auth-and-basics.md) | x-api-key auth, key location and role scoping, the JSON:API envelope (data/attributes/relationships/included[]) with jq patterns, pagination params, error surfaces |
| [references/endpoint-catalog.md](references/endpoint-catalog.md) | Every route's method, path, and parameters (shows, episodes, publish, uploads, analytics, subscribers, webhooks) plus routes that do not exist |
| [references/episode-publish-lifecycle.md](references/episode-publish-lifecycle.md) | The draft/scheduled/published state machine, the exact publish request/response shapes, create→audio→publish recipes in CLI and curl, authorize-upload detour |
| [references/gotchas-and-recipes.md](references/gotchas-and-recipes.md) | Symptom → cause → fix field guide (404 user route, silent pagination, 429 storms...) and multi-step workflows (bulk scheduling, analytics reports, subscriber import, webhooks) |

## Available Scripts and Prerequisites

- `scripts/transistor` — the bundled Python CLI (`--json`, `--dry-run`,
  `--force`, `--quiet`, `--verbose`, `--help` everywhere). Imports only the
  standard library and `requests`; sends write bodies exactly as documented
  (bracket-key form fields).
- `scripts/test_transistor.py` — offline test suite (pytest + unittest
  compatible); all HTTP mocked with canned JSON:API documents, zero network
  egress, no live-call cases (Transistor is a keyed API).
- Requires Python 3.8+, `requests`, and `TRANSISTOR_API_KEY` for live
  commands (Account page → API Access). No service is started by this skill.
