---
name: chartmetric
description: Chartmetric music analytics API for streaming data, playlist placements, audience demographics, and competitive analysis. Use when the user needs artist/track/album analytics, playlist tracking, streaming metrics, audience insights, chart positions, similar artists, or any music industry data. Triggers on requests involving Spotify followers, monthly listeners, TikTok trends, Instagram audience, playlist pitching research, or competitive artist analysis.
---

# Chartmetric API

Music industry analytics via Python scripts. Get streaming metrics, playlist placements, audience data, and competitive insights.

## Setup

### With Python (recommended)

```bash
cd .recoup/skills/chartmetric
python3 -m venv .venv && source .venv/bin/activate
pip install requests
export CHARTMETRIC_REFRESH_TOKEN="your_token"
```

### Without Python (curl fallback)

If Python is unavailable, see `references/curl-fallback.md` for curl-only patterns. Only requires `curl` (universal).

## Quick Start

```bash
# 1. Search for an artist
python scripts/search_artist.py "Drake"
# Returns: Chartmetric ID 3380

# 2. Get profile and stats
python scripts/get_artist.py 3380
python scripts/get_artist_metrics.py 3380 --source spotify

# 3. Get where fans listen
python scripts/get_artist_cities.py 3380
```

---

## Critical Gotchas

These are the API traps that cause 401/400 errors. Memorize them:

| Gotcha | Wrong | Correct |
|--------|-------|---------|
| YouTube metrics | `--source youtube` | `--source youtube_channel` or `youtube_artist` |
| Artist playlists | `/artist/:id/playlists` | `/artist/:id/:platform/current/playlists` |
| Similar artists | `/artist/:id/similar` | `/artist/:id/relatedartists` or `similar-artists/by-configurations` |
| TikTok charts | With `country_code` | **No** `country_code` parameter |
| Amazon charts | With `country_code` | **No** `country_code` - use `genre` + `type` |
| Curator search | By name | By **numeric** Chartmetric ID only |

---

## Scripts Reference

### Artist Discovery

```bash
# Find US artists with 100K-500K Spotify monthly listeners
python scripts/discover_artists.py --country US --spotify-listeners 100000 500000

# TikTok-famous but weak on Spotify
python scripts/discover_artists.py --tiktok-followers 1000000 10000000 --spotify-listeners 0 100000

# Emerging artists in a genre, sorted by weekly growth
python scripts/discover_artists.py --genre 86 --spotify-listeners 50000 200000 --sort weekly_diff.sp_monthly_listeners

# Solo female artists in Brazil
python scripts/discover_artists.py --country BR --band false --pronoun she/her

# Festival performers with low Spotify (undervalued)
python scripts/discover_artists.py --festival-id 123 --spotify-followers 0 50000
```

**Available filters:** `--country`, `--genre`, `--band`, `--pronoun`, `--spotify-listeners`, `--spotify-followers`, `--tiktok-followers`, `--instagram-followers`, `--youtube-subscribers`, `--cpp`, `--festival-id`

**Sort columns:** `latest.sp_monthly_listeners`, `weekly_diff.sp_monthly_listeners`, `monthly_diff.tt_followers`, etc.

### Search & Lookup

```bash
python scripts/search_artist.py "Taylor Swift"        # Search artists by name
python scripts/get_artist.py 2762                     # Get profile by CM ID
python scripts/get_artist_by_spotify.py 3TVXtAsR...   # Lookup by Spotify ID/URL
python scripts/get_track.py 128613854                 # Get track metadata
python scripts/get_track_by_spotify.py 0VjIjW4G...    # Lookup track by Spotify
```

### Artist Data

```bash
python scripts/get_artist_albums.py 3380              # All albums
python scripts/get_artist_tracks.py 3380              # All tracks
python scripts/get_artist_cities.py 3380              # Top cities by listeners
python scripts/get_artist_urls.py 3380                # Social/streaming URLs
python scripts/get_artist_insights.py 3380            # AI-generated insights
python scripts/get_artist_career.py 3380              # Career timeline
```

### Platform Metrics

```bash
python scripts/get_artist_metrics.py 3380 --source spotify
python scripts/get_artist_metrics.py 3380 --source instagram
python scripts/get_artist_metrics.py 3380 --source youtube_channel
```

**Valid sources (14 total):** `spotify`, `instagram`, `tiktok`, `twitter`, `facebook`, `youtube_channel`, `youtube_artist`, `soundcloud`, `deezer`, `twitch`, `line`, `melon`, `wikipedia`, `bandsintown`

### Audience Demographics

```bash
python scripts/get_artist_audience.py 3380                        # Instagram (default)
python scripts/get_artist_audience.py 3380 --platform tiktok      # TikTok
python scripts/get_artist_audience.py 3380 --platform youtube     # YouTube
python scripts/get_artist_instagram_posts.py 3380                 # Top IG posts/reels
```

### Playlist Placements

```bash
# Basic - current Spotify playlists
python scripts/get_artist_playlists.py 3380

# Other platforms
python scripts/get_artist_playlists.py 3380 --platform applemusic
python scripts/get_artist_playlists.py 3380 --platform deezer

# Past placements
python scripts/get_artist_playlists.py 3380 --status past

# With filters
python scripts/get_artist_playlists.py 3380 --editorial --newMusicFriday
python scripts/get_artist_playlists.py 3380 --indie --majorCurator

# With date range and sorting
python scripts/get_artist_playlists.py 3380 --since 2025-01-01 --sort followers --limit 100
```

**Platforms:** `spotify`, `applemusic`, `deezer`, `amazon`, `youtube`

**Spotify filters:** `--editorial`, `--personalized`, `--chart`, `--thisIs`, `--newMusicFriday`, `--radio`, `--indie`, `--majorCurator`, `--popularIndie`, `--brand`

### Similar/Related Artists

```bash
# Basic related artists
python scripts/get_similar_artists.py 3380 --limit 10

# Advanced with configuration filters
python scripts/get_similar_artists.py 3380 --by-config --audience high --genre high
python scripts/get_similar_artists.py 3380 --by-config --mood medium --musicality high
```

**Config options:** `--audience`, `--mood`, `--genre`, `--musicality` (values: `high`, `medium`, `low`)

### Playlists & Curators

```bash
python scripts/get_playlist.py spotify 37i9dQZF1DXcBWIGoYBM5M    # Playlist metadata
python scripts/get_curator.py 1                                  # Curator info (numeric ID)
```

### Discovery

```bash
python scripts/list_genres.py                                    # All Chartmetric genres
python scripts/list_festivals.py                                 # Music festivals
```

---

## Workflow Chains

### Research an Artist for Playlist Pitching

```bash
# 1. Find the artist
python scripts/search_artist.py "Phoebe Bridgers"
# ID: 241089

# 2. Get their current playlist placements
python scripts/get_artist_playlists.py 241089 --editorial --limit 50

# 3. Find similar artists who might share playlists
python scripts/get_similar_artists.py 241089 --by-config --genre high --audience high

# 4. Check where their fans are
python scripts/get_artist_cities.py 241089
python scripts/get_artist_audience.py 241089 --platform instagram
```

### Competitive Analysis

```bash
# 1. Get base artist
python scripts/get_artist.py 3380

# 2. Get similar artists with metrics
python scripts/get_similar_artists.py 3380 --by-config --audience high --limit 25

# 3. Compare streaming growth
python scripts/get_artist_metrics.py 3380 --source spotify
python scripts/get_artist_metrics.py <competitor_id> --source spotify

# 4. Compare playlist reach
python scripts/get_artist_playlists.py 3380 --sort followers
python scripts/get_artist_playlists.py <competitor_id> --sort followers
```

### From Spotify URL to Full Profile

```bash
# 1. Convert Spotify URL to Chartmetric ID
python scripts/get_artist_by_spotify.py "https://open.spotify.com/artist/3TVXtAsR1Inumwj472S9r4"
# Returns: cm_artist: 1320

# 2. Get everything
python scripts/get_artist.py 1320
python scripts/get_artist_metrics.py 1320 --source spotify
python scripts/get_artist_cities.py 1320
python scripts/get_artist_playlists.py 1320
python scripts/get_artist_audience.py 1320
```

### More Advanced Workflows

See `references/advanced-workflows.md` for 10 strategic workflow chains including:
- Playlist pitching intelligence
- TikTok-to-Spotify pipeline analysis
- A&R discovery workflow
- Collaboration finder
- Viral song autopsy

---

## References

| File | When to Use |
|------|-------------|
| `references/parameter-guide.md` | Detailed endpoint parameters and gotchas |
| `references/endpoints.md` | All 120 endpoints with status |
| `references/curl-fallback.md` | **When Python unavailable** - curl patterns for all endpoints |
| `references/advanced-workflows.md` | **Strategic insights** - 10 multi-step workflow chains |

---

## Rate Limits

Chartmetric has rate limits. If you get 429 errors, wait 60 seconds before retrying.

---

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| 401 Unauthorized | Token expired or internal endpoint | Refresh token; check if endpoint is public |
| 402 Payment Required | Subscription expired | Check Chartmetric account |
| 404 Not Found | Invalid ID | Verify Chartmetric ID (not Spotify ID) |
| 400 Bad Request | Wrong parameters | Check parameter-guide.md for correct params |
| "Domain does not exist" | Invalid stat source | Use exact source names (e.g., `youtube_channel` not `youtube`) |
