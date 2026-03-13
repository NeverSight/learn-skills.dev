---
name: youtube-music-openclaw
description: Control YouTube Music with natural language - search, play, pause, skip, volume, shuffle
user-invocable: true
metadata: {"openclaw":{"emoji":"🎵","os":["darwin"],"requires":{"bins":["osascript","yt-dlp","jq"]},"install":[{"id":"yt-dlp","kind":"brew","formula":"yt-dlp","bins":["yt-dlp"],"label":"Install yt-dlp"},{"id":"jq","kind":"brew","formula":"jq","bins":["jq"],"label":"Install jq"}]}}
---

# YouTube Music Control (Kaset)

## Playback Commands

```bash
osascript -e 'tell application "Kaset" to <command>'
```

| Command | Description |
|---------|-------------|
| `play` | Play/resume |
| `pause` | Pause |
| `next track` | Next song |
| `previous track` | Previous song |
| `set volume N` | Volume 0-100 |
| `toggle mute` | Mute on/off |
| `toggle shuffle` | Shuffle on/off |
| `like track` | Like current |
| `get player info` | Get state as JSON |

## Search and Play

```bash
# 1. Search (returns JSON array with id, title)
{baseDir}/bin/youtube-search "artist or song name"

# 2. Play by ID
{baseDir}/bin/play-video VIDEO_ID
```

When user wants to play something, search first, pick a random result, then play it.
