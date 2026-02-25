---
name: spotify
description: |
  Control Spotify playback via CLI. Requires Spotify Premium for playback control.
  USE FOR: play song, play music, play [song name], play [artist], play [album], play [playlist], pause, stop music, resume, skip, next song, previous song, what's playing, now playing, current song, volume up, volume down, set volume, shuffle on, shuffle off, repeat, queue, add to queue, list devices, transfer playback, play on [device].
  DO NOT USE FOR: downloading music, editing playlists, creating playlists.
---

# Spotify Control

## Quick Start

```bash
# Play a song (handles search, device wake, everything)
./scripts/spotify-play.sh "l'amour toujours"

# Play a playlist
./scripts/spotify-play.sh "today's top hits" --type playlist

# Pause/resume/skip
./scripts/spotify-ctl.sh pause
./scripts/spotify-ctl.sh play
./scripts/spotify-ctl.sh next
```

## Setup

### Spotify Developer Account (one-time)

1. Go to https://developer.spotify.com/dashboard
2. Log in with your Spotify account
3. Click **Create App** → name it anything → select "Web API"
4. Add redirect URI: `http://127.0.0.1:17823/callback`
5. Copy your **Client ID** and **Client Secret**

**Note**: Requires Spotify Premium for playback control. Free accounts can only search.

### First Run

First run prompts for credentials interactively:
```bash
./scripts/spotify-auth.sh login
```

Credentials loaded from: env vars → `~/.spotify/credentials.json` → interactive prompt

## Helper Scripts

| Script | Purpose |
|--------|---------|
| `spotify-play.sh <query>` | Search and play (handles device wake) |
| `spotify-ctl.sh <cmd>` | Playback control (pause, play, next, prev, volume, shuffle, repeat) |
| `spotify-auth.sh login` | OAuth setup |
| `spotify-auth.sh token` | Get valid token (auto-refreshes) |

### spotify-play.sh

```bash
# Play track (default)
./scripts/spotify-play.sh "bohemian rhapsody"

# Play playlist
./scripts/spotify-play.sh "workout" --type playlist

# Play album  
./scripts/spotify-play.sh "thriller" --type album

# Play artist
./scripts/spotify-play.sh "queen" --type artist

# Play on specific device
./scripts/spotify-play.sh "song" --device "Kitchen Echo"

# Set default device
./scripts/spotify-play.sh --set-device "Kitchen Echo"
```

### spotify-ctl.sh

```bash
./scripts/spotify-ctl.sh pause
./scripts/spotify-ctl.sh play
./scripts/spotify-ctl.sh next
./scripts/spotify-ctl.sh prev
./scripts/spotify-ctl.sh volume 50
./scripts/spotify-ctl.sh shuffle on|off
./scripts/spotify-ctl.sh repeat track|context|off
./scripts/spotify-ctl.sh devices        # list devices
./scripts/spotify-ctl.sh transfer Echo  # move playback to device
./scripts/spotify-ctl.sh now            # what's playing
./scripts/spotify-ctl.sh queue          # show queue
./scripts/spotify-ctl.sh add-queue <uri> # add to queue
```

## Direct API Access

For advanced use, get token and call API directly:

```bash
TOKEN=$(./scripts/spotify-auth.sh token)

# Search
curl -s "https://api.spotify.com/v1/search?q=despacito&type=track&limit=5" \
  -H "Authorization: Bearer $TOKEN" | jq '.tracks.items[] | {name, uri}'

# Play URI
curl -s -X PUT "https://api.spotify.com/v1/me/player/play" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"uris": ["spotify:track:xxx"]}'
```

## Common Patterns

### Search and play first result
```bash
./scripts/spotify-play.sh "song name"
```

### Play on specific device
```bash
./scripts/spotify-play.sh "song" --device "Echo"
```

### Control playback
```bash
./scripts/spotify-ctl.sh pause
./scripts/spotify-ctl.sh volume 30
./scripts/spotify-ctl.sh shuffle on
```

## Error Handling

| Error | Solution |
|-------|----------|
| No token | Run `./scripts/spotify-auth.sh login` |
| No active device | Script auto-wakes default device, or use `--device` |
| 403 Premium required | Playback needs Spotify Premium |
| 401 Unauthorized | Token auto-refreshes; if persists, re-run login |

## Files

```
~/.config/spotify/          # or $XDG_CONFIG_HOME/spotify/
├── credentials.json        # Client ID/Secret (chmod 600)
├── tokens.json             # Access/refresh tokens (chmod 600)  
└── config.json             # Default device, preferences
```

## API Limits (Feb 2026)

- Search: max 10 results per request
- Batch endpoints removed (fetch individually)
- Normalize playlist URIs: `playlist_v2` → `playlist`
