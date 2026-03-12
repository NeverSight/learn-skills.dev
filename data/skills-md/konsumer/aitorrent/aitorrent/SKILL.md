---
name: aitorrent
description: Manage Plex media library, qBittorrent downloads, and TMDB lookups for movie/TV show management using uvx
---

# AITorrent Skill

Use this skill when working with media management tasks involving Plex, qBittorrent, or TMDB. All tools are run via `uvx` which requires no installation.

## Prerequisites

None required - `uvx` handles everything. Configure credentials in these environment-variables:

```
PLEX_URL=http://localhost:32400
PLEX_TOKEN=your_plex_token
TMDB_API_KEY=your_tmdb_api_key
QBT_URL=http://localhost:8080
QBT_USERNAME=admin
QBT_PASSWORD=adminadmin
```

## Available Tools

### Plex CLI

```bash
# List all library names
uvx --from aitorrent aitorrent-plex-cli list

# List all shows in "TV Shows" library
uvx --from aitorrent aitorrent-plex-cli list "TV Shows"

# List all movies in "Movies" library
uvx --from aitorrent aitorrent-plex-cli list "Movies"

# Show what's currently watching
uvx --from aitorrent aitorrent-plex-cli watching
```

### TMDB CLI

```bash
# Search for a TV show
uvx --from aitorrent aitorrent-tmdb-cli search-shows "Star Trek Lower Decks"

# Get show details (use the tmdb_id from search)
uvx --from aitorrent aitorrent-tmdb-cli show-details 85948

# Get season details
uvx --from aitorrent aitorrent-tmdb-cli season-details 85948 1

# Search for a movie
uvx --from aitorrent aitorrent-tmdb-cli search-movies "The Matrix"

# Get movie details
uvx --from aitorrent aitorrent-tmdb-cli movie-details 603
```

### qBittorrent CLI

```bash
# List all torrents
uvx --from aitorrent aitorrent-qbt-cli list

# List downloading torrents only
uvx --from aitorrent aitorrent-qbt-cli list downloading

# Add a torrent
uvx --from aitorrent aitorrent-qbt-cli add "magnet:?xt=urn:btih:..." --path "/downloads" --category "TV Shows"

# List RSS feeds
uvx --from aitorrent aitorrent-qbt-cli rss list-feeds

# Add RSS feed
uvx --from aitorrent aitorrent-qbt-cli rss add-feed "https://example.com/feed.rss" --folder "TV Shows"

# Add RSS rule for a show
uvx --from aitorrent aitorrent-qbt-cli rss add-show "Star Trek Lower Decks" --season 3 --quality "1080p" --category "TV Shows"
```

## Common Workflows

1. **Find a show to add**: Use TMDB CLI to search for a show, get its details to find episode information
2. **Add to qBittorrent**: Use qBittorrent CLI to add torrent or RSS rule
3. **Check Plex**: Use Plex CLI to verify the library and see what's being watched

## Environment Variables

| Variable       | Description                                    |
| -------------- | ---------------------------------------------- |
| `PLEX_URL`     | Plex server URL (e.g., http://localhost:32400) |
| `PLEX_TOKEN`   | Plex authentication token                      |
| `TMDB_API_KEY` | The Movie Database API key                     |
| `QBT_URL`      | qBittorrent Web UI URL                         |
| `QBT_USERNAME` | qBittorrent username                           |
| `QBT_PASSWORD` | qBittorrent password                           |
