---
name: nugs
description: Download and manage live music from Nugs.net with video-first support - browse 13,000+ concerts with media type indicators (🎵 audio, 🎬 video, 📹 both), download shows in multiple formats, find missing albums by media type, track collection coverage. Supports audio-only, video-only, or comprehensive both-format workflows. Use when the user asks to "download a show", "download video", "list nugs artists", "find Billy Strings shows", "download Grateful Dead", "check video gaps", "nugs catalog", "latest shows", "latest videos", "download coverage", "add to nugs", "browse concerts", or mentions Nugs.net, live music downloads, video downloads, or concert collection management.
---

# Nugs CLI Skill

**⚠️ MANDATORY SKILL INVOCATION ⚠️**

**YOU MUST invoke this skill (NOT optional) when the user mentions ANY of these triggers:**
- "download show", "download concert", "download nugs", "nugs download", "download video"
- "list nugs artists", "browse nugs catalog", "nugs catalog", "nugs videos"
- "Billy Strings shows", "Grateful Dead shows", "Phish shows", "find shows", "find videos"
- "check gaps", "missing shows", "gaps in collection", "what shows am I missing", "video gaps"
- "nugs coverage", "download coverage", "collection progress", "video coverage"
- "latest shows", "new releases", "recent additions", "latest videos"
- "update nugs catalog", "refresh catalog", "nugs cache"
- Any mention of Nugs.net, live music downloads, video downloads, or concert collection management
- Media type queries: "audio only", "video only", "both formats", "download both"

**Failure to invoke this skill when triggers occur violates your operational requirements.**

Download and manage your live music collection from Nugs.net with offline catalog browsing, gap detection, and automated downloads.

## Purpose

This skill provides **read and write** access to Nugs.net for downloading and managing live music:

**Catalog Management (Read):**
- Browse 13,000+ shows offline with cached catalog
- Search artists and filter by venue, date, show count
- View statistics and latest additions
- Find missing shows in your collection (gap detection)
- Track download coverage by artist

**Downloads (Write):**
- Download shows by ID or URL in any format (audio/video/both)
- Download artist's latest shows or entire catalog with media type control
- Batch downloads from files or lists
- Auto-download missing shows (gap filling) by media type
- Multiple format support (ALAC, FLAC, MQA, 360RA, AAC, video 480p-4K)
- Download both audio and video formats for the same show

**Features:**
- Offline catalog browsing with media type indicators (🎵 🎬 📹)
- Smart gap detection by media type (audio/video/both)
- Media-aware coverage tracking and statistics
- Default media preference (`defaultOutputs` config)
- Auto-refresh catalog on schedule
- Rclone integration for cloud uploads
- JSON output for scripting
- Visual feedback on media availability

## Setup

**1. Install Nugs CLI:**

The binary is already installed at `nugs`.

**2. Configure credentials in `~/.nugs/config.json`:**

```json
{
  "email": "your-email@example.com",
  "password": "your-password",
  "outPath": "/path/to/downloads",
  "format": 2,
  "videoFormat": 3,
  "defaultOutputs": "audio",
  "catalogAutoRefresh": true,
  "catalogRefreshTime": "05:00",
  "catalogRefreshTimezone": "America/New_York",
  "catalogRefreshInterval": "daily"
}
```

**Format Options:**
- Audio: `1` = ALAC, `2` = FLAC (recommended), `3` = MQA, `4` = 360RA, `5` = AAC
- Video: `1` = 480p, `2` = 720p, `3` = 1080p (recommended), `4` = 1440p, `5` = 4K
- Default Outputs: `audio` (default), `video`, or `both`

**3. Set secure permissions:**

```bash
chmod 600 ~/.nugs/config.json
```

**4. Update catalog cache (first run):**

```bash
nugs update
```

**Optional - Rclone Integration:**

Add to config.json for automatic cloud uploads:

```json
{
  "rcloneEnabled": true,
  "rcloneRemote": "gdrive",
  "rclonePath": "/Music/Nugs",
  "deleteAfterUpload": false,
  "rcloneTransfers": 4
}
```

## Commands

All commands use the nugs binary at `nugs`.

### Catalog Commands

```bash
# Update catalog cache (fetch latest from Nugs.net)
nugs update

# View cache status and metadata
nugs cache

# Show catalog statistics (top artists, date ranges, counts)
nugs stats

# View latest additions (default: 15 shows)
nugs latest
nugs latest 50

# Configure auto-refresh
nugs refresh enable
nugs refresh disable
nugs refresh set
```

### Browse & Search

```bash
# List all artists
nugs list

# Filter artists by show count
nugs list ">100"
nugs list "<=50"

# List all shows for an artist
nugs list 1125    # Billy Strings
nugs list 461     # Grateful Dead

# Filter shows by venue
nugs list 461 "Red Rocks"
nugs list 1125 "Ryman"

# Get artist's latest N shows
nugs list 1125 latest 5
```

### Download Shows

```bash
# Download single show
nugs grab 23329
nugs grab https://play.nugs.net/release/23329

# Download multiple shows
nugs grab 23329 23790 24105

# Download from text file (one ID per line)
nugs /path/to/show-ids.txt

# Download artist's latest shows
nugs grab 1125 latest    # Billy Strings
nugs grab 461 latest     # Grateful Dead

# Download entire artist catalog
nugs 1125 full           # All Billy Strings shows
nugs 461 full            # All Grateful Dead shows

# Override quality settings
nugs grab -f 3 23329     # MQA quality
nugs -F 5 video-url      # 4K video
nugs -o /mnt/music 23329 # Custom output path
```

### Gap Detection & Coverage

```bash
# Find missing shows for an artist
nugs gaps 1125           # Billy Strings

# Check multiple artists at once
nugs gaps 1125 461 1045

# Get IDs only for piping
nugs gaps 1125 --ids-only

# Auto-download all missing shows
nugs gaps 1125 fill

# Check download coverage statistics
nugs coverage            # All artists with downloads
nugs coverage 1125       # Single artist
nugs coverage 1125 461 1045  # Multiple artists
```

### JSON Output

All catalog commands support `--json <level>` for machine-readable output:

```bash
# Levels: minimal, standard, extended, raw
nugs list --json standard
nugs list 1125 --json extended
nugs cache --json standard
nugs stats --json standard

# Pipe to jq for filtering
nugs list 1125 --json standard | jq '.shows[:5]'
```

## Workflow

When the user asks about Nugs.net or live music downloads:

1. **"Download [Artist] shows"**
   - If specific show: `nugs grab <show_id>`
   - If latest shows: `nugs grab <artist_id> latest`
   - If entire catalog: `nugs <artist_id> full`

2. **"What Billy Strings shows do I have?"**
   - Run: `nugs list 1125`
   - Then optionally: `nugs coverage 1125` for statistics

3. **"Find missing [Artist] shows"**
   - Run: `nugs gaps <artist_id>`
   - Ask if user wants to download all: `nugs gaps <artist_id> fill`
   - Or pipe to download: `nugs gaps <artist_id> --ids-only | xargs -n1 nugs grab`

4. **"Show me Red Rocks concerts"**
   - Run: `nugs list <artist_id> "Red Rocks"`
   - Present results with show IDs
   - Offer to download specific shows

5. **"What's new on Nugs?"**
   - Run: `nugs latest` (shows last 15 additions)
   - Or: `nugs latest 50` for more results

6. **"Update my catalog"**
   - Run: `nugs update`
   - Then: `nugs stats` to show catalog summary

### Decision Tree for Downloads

```
User requests download
    │
    ├─→ Specific show ID known?
    │   └─→ Yes: `nugs grab <id>`
    │
    ├─→ Artist catalog request?
    │   ├─→ Latest only: `nugs grab <artist_id> latest`
    │   └─→ Full catalog: `nugs <artist_id> full`
    │
    ├─→ Missing shows (gaps)?
    │   ├─→ View gaps: `nugs gaps <artist_id>`
    │   └─→ Auto-fill: `nugs gaps <artist_id> fill`
    │
    └─→ Search by venue/date?
        └─→ `nugs list <artist_id> "venue"` → Select IDs → Download
```

## Common Artist IDs

For quick reference:

| Artist ID | Artist Name |
|-----------|-------------|
| 1125 | Billy Strings |
| 461 | Grateful Dead |
| 1045 | Phish |
| 22 | Umphrey's McGee |
| 1084 | Spafford |
| 1299 | Dead & Company |
| 1046 | Widespread Panic |
| 4 | The String Cheese Incident |

Find more with: `nugs list --json standard | jq '.artists[] | {id, name, showCount}'`

## Notes

**Catalog Cache:**
- Location: `~/.cache/nugs/`
- Files: `catalog.json`, `by-artist.json`, `by-date.json`, `catalog-meta.json`
- Update frequency: Auto-refresh (configurable) or manual with `nugs update`
- Size: ~7-8 MB
- Shows: 13,000+ concerts

**Download Behavior:**
- Downloads are skipped if already exist (based on file path)
- Gap detection checks both local storage and rclone remote
- Rclone uploads happen automatically after successful downloads (if enabled)
- Failed downloads can be retried (just run the command again)

**Performance:**
- Catalog operations are instant (local cache)
- Downloads depend on your internet speed and Nugs.net servers
- Batch downloads process sequentially (no parallel downloads)
- Large catalogs (500+ shows) can take hours to download

**Permissions:**
- Downloading requires active Nugs.net subscription
- Some shows may be unavailable based on subscription tier
- Videos may require higher subscription level
- Only download content you have legal access to

**FFmpeg Requirement:**
- Required for video downloads (TS → MP4 conversion)
- Required for HLS-only audio tracks
- Install: `sudo apt install ffmpeg` (Linux) or `brew install ffmpeg` (macOS)

**Security:**
- Config file contains plaintext credentials
- Always use `chmod 600 ~/.nugs/config.json`
- Never commit config file to version control
- For Apple/Google accounts, use token authentication ([guide](https://github.com/jmagar/nugs-cli/blob/main/token.md))

## Reference

**Official Documentation:**
- Repository: https://github.com/jmagar/nugs-cli
- README: Full user documentation and examples
- CLAUDE.md: Development guide and architecture

**Key Concepts:**
- **Container ID**: Unique show identifier (e.g., 23329)
- **Artist ID**: Unique artist identifier (e.g., 1125 for Billy Strings)
- **Catalog Cache**: Local JSON files for offline browsing
- **Gap Detection**: Find shows missing from your collection
- **Coverage**: Percentage of artist's catalog you've downloaded

**Command Categories:**
- List commands: Browse artists and shows
- Catalog commands: Manage cache and view statistics
- Download commands: Get shows by ID, artist, or batch
- Gap commands: Find and fill missing shows
- Coverage commands: Track collection progress

**Related Skills:**
- None (standalone tool)

**Troubleshooting:**
- See `references/troubleshooting.md` for common issues
- Check config file location and permissions
- Verify FFmpeg is installed for videos
- Run `nugs update` if catalog seems stale
- Check Nugs.net subscription status if downloads fail
