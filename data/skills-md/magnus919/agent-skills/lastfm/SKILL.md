---
name: lastfm
description: >-
  Interact with the Last.fm music data API: lookup user listening history, get
  artist/album/track metadata, discover similar music via collaborative filtering, explore
  global and per-country charts, search by artist/album/track, manage tags, and scrobble
  listening events. Use when the user asks about music data, listening statistics, music
  recommendations, similar artists, charts, or wants to scrobble or love tracks. Do not
  use this skill for unrelated requests; route to the nearest named specialist.
license: MIT
compatibility: Requires a Last.fm API key in the LASTFM_API_KEY env var. For write
  operations (scrobble, love, now-playing), also needs LASTFM_API_SECRET and LASTFM_SESSION_KEY.
  The `lastfm-cli` CLI tool must be on PATH.
metadata:
  tags: music, lastfm, scrobbling, api-client, music-discovery
  source: https://www.last.fm/api
---

# Last.fm

## Setup

```bash
export LASTFM_API_KEY="your_api_key_here"
# For write operations only:
export LASTFM_API_SECRET="your_api_secret"
export LASTFM_SESSION_KEY="your_session_key"
```

Get an API key at https://www.last.fm/api/account/create (free, requires a Last.fm account).

## Essential Commands

### User queries — "what am I listening to"

Configurable via `LASTFM_USERNAME` env var. Defaults to `<username>` if unset.

```bash
lastfm-cli user info <username>                      # Profile + stats
lastfm-cli user recent-tracks <username> --limit 10   # Recent listening
lastfm-cli user top-artists <username> --period 7day  # Weekly top artists
lastfm-cli user top-tracks <username> --period overall # All-time faves
lastfm-cli user loved-tracks <username>               # Loved tracks
lastfm-cli user friends <username>                    # Social graph
lastfm-cli user weekly-charts <username>              # Available chart periods
```

### Music Discovery — "what's similar to X"

```bash
lastfm-cli artist similar <artist> --limit 10         # Taste graph neighbors
lastfm-cli artist info <artist>                       # Bio, stats, tags
lastfm-cli artist top-tracks <artist>                 # Their most popular
lastfm-cli track similar <artist> "<track>"           # Track-level similarity
lastfm-cli album info <artist> "<album>"              # Tracklist, metadata
lastfm-cli tag top-artists <tag>                      # Genre browsing
```

### Charts — "what's popular"

```bash
lastfm-cli chart top-artists --limit 20               # Global
lastfm-cli geo top-artists "Japan" --limit 20         # Per-country
lastfm-cli geo top-tracks "Germany" --limit 20
lastfm-cli tag top-tracks "electronic" --limit 15     # By genre tag
```

### Search — "find that thing"

```bash
lastfm-cli artist search "Radiohead"                  # Find by name
lastfm-cli album search "OK Computer"                 # Find albums
lastfm-cli track search "Karma Police"                # Find tracks
```

### Write operations (require session auth)

```bash
lastfm-cli track scrobble "Artist" "Song" --album "Album"
lastfm-cli track now-playing "Artist" "Song"
lastfm-cli track love "Artist" "Song"
```

### Auth flow (one-time setup)

```bash
# 1. Get a token
lastfm-cli auth get-token

# 2. User visits: https://www.last.fm/api/auth/?api_key=KEY&token=TOKEN

# 3. Exchange for session key
lastfm-cli auth get-session <token>
# → Set export LASTFM_SESSION_KEY=<key>
```

## Reference Files

- `references/auth-flow.md` — Full walkthrough for setting up write operation auth (scrobble, love, now-playing). Read this before attempting write operations.

## Music Discovery Pipeline — "find me new stuff I'll like"

The core flow for turning liked tracks into recommendations:

1. **Get user's top artists/tracks** from Last.fm:
   ```bash
   lastfm-cli user top-artists <username> --period 1month --limit 5 --json
   lastfm-cli user top-tracks <username> --period 1month --limit 10 --json
   lastfm-cli user loved-tracks <username> --json
   ```

2. **For each artist, find similar artists** via Last.fm's collaborative filtering:
   ```bash
   lastfm-cli artist similar "<artist>" --limit 5 --json
   ```

3. **For each track, find similar tracks** for more granular recommendations:
   ```bash
   lastfm-cli track similar "<artist>" "<track>" --limit 5 --json
   ```

4. **Cross-reference** against what they've already scrobbled (recent-tracks) to filter out already-heard material.

5. **Check against the user's own collection** (via Radarr/Sonarr/jellyfin or Spotify library) to see what's already in the library vs genuinely new discovery.

## Using with --json for Machine Processing

```bash
# Pipe to jq for structured queries
lastfm-cli artist similar "Radiohead" --limit 5 --json | jq '.similarartists.artist[] | {name, match}'

# Get a user's all-time top artists with playcounts
lastfm-cli user top-artists <username> --period overall --limit 3 --json | jq '.topartists.artist[] | {name, playcount}'

# Find most popular tracks by a genre
lastfm-cli tag top-tracks "electronic" --limit 10 --json | jq '.tracks.track[] | {name, artist: .artist.name, listeners}'
```

## Known Gotchas

- **API key required for EVERY request.** The key is free — get one at the Last.fm API account page.
- **Rate limit is ~5 req/sec sustained.** The API docs say "be reasonable" — if you're making several calls per second continuously, your account may be suspended. Add small delays in loops.
- **User-Agent header matters.** The CLI sends `lastfm-cli/1.0 (hermes-agent)`. Last.fm's docs explicitly ask for an identifiable User-Agent.
- **XML is the default response format.** The CLI requests `format=json`. Without it, responses come back as XML.
- **Artist names can be misspelled.** Use `--autocorrect` flag on artist commands to let Last.fm correct misspellings.
- **Write operations need auth setup.** scrobble, love, and now-playing require a full auth flow (token → session key). Read-only endpoints don't.
- **The collaborative filtering graph is NOT social.** `artist.getSimilar` returns algorithmic similarity based on aggregate listening patterns, not human-curated recommendations.
- **Timestamps for scrobbles** are UNIX epoch seconds. If omitted, uses current time.
- **`--from` and `--to` on recent-tracks** accept ISO 8601 date strings (e.g., `2026-05-27`).
- **Period values**: `overall`, `7day`, `1month`, `3month`, `6month`, `12month`.

## When to Reach for This Tool

- User asks "what's [person] listening to lately?"
- User wants music discovery: "find me artists similar to..."
- User wants listening statistics: top artists, tracks, albums by period
- User wants geographic music trends: "what's popular in [country]"
- User wants genre exploration via tags
- User wants to scrobble or love tracks programmatically
- Any question about music metadata, artist info, album tracklists

## Available Scripts

| Script | Purpose | Invocation |
|---|---|---|
| `scripts/lastfm-cli` | The CLI tool this skill drives: read-only queries (user info/recent-tracks/top-artists/top-tracks/loved-tracks/friends/weekly-charts), discovery (`artist similar`, `track similar`), charts and geo charts, search, tags, and — with session auth — `scrobble`, `now-playing`, and `love`. Run it for every Last.fm data question above; see Essential Commands for the full command surface. | `scripts/lastfm-cli user top-artists <username> --period 7day --limit 10` |
| `scripts/test-lastfm.sh` | Shell test suite covering the CLI's argument handling and output formatting without network calls. Run it after modifying `scripts/lastfm-cli` or when auditing a change to its behavior; CI runs it via `scripts/check-skill-tests.py`. | `bash scripts/test-lastfm.sh` |

## Prerequisites

- A free Last.fm API key exported as `LASTFM_API_KEY` (create one at https://www.last.fm/api/account/create); every request fails without it.
- For write operations only: `LASTFM_API_SECRET` plus a session key from the one-time auth flow in `references/auth-flow.md`, exported as `LASTFM_SESSION_KEY`.
- Python 3 on PATH — invoke the bundled tool as `python3 scripts/lastfm-cli ...` if it is not executable directly; the SKILL.md examples assume `lastfm-cli` resolves on PATH.
- Optional: `LASTFM_USERNAME` to set the default user for user queries; `jq` when piping `--json` output for structured processing.

## Limitations

- Read-only endpoints need only the API key; scrobble, now-playing, and love require the full token → session-key auth flow and will fail without it.
- Sustained call rates above ~5 req/sec risk account suspension — add small delays in loops.
- Similarity endpoints are algorithmic collaborative filtering over aggregate listening patterns, not social or human-curated recommendations.
- Period values are fixed to `overall`, `7day`, `1month`, `3month`, `6month`, and `12month`; arbitrary date ranges are only available via `--from`/`--to` on recent-tracks.
- Misspelled artist names return empty or wrong results unless `--autocorrect` is used.

## When not to use

Do not use this skill for music playback control (local players, streaming queues), for non-Last.fm catalog data (MusicBrainz, Spotify metadata), or as a lyrics source — the API covers listening history, metadata, charts, tags, similarity, and scrobbling only.
