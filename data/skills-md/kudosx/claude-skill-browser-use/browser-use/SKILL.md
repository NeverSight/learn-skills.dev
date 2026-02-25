---
name: browser-use
description: Web scraping, screenshots, form filling, file downloads/uploads, Google/DuckDuckGo image search, YouTube video downloading, and TikTok video downloading.
allowed-tools: Bash, Read, Write, Edit
---

# Browser Use Skill

## Overview
This skill enables browsing websites and interacting with web pages using Playwright.

## Quick Start - Use Scripts

**Important:** All `uv run` commands must be executed from the scripts folder (not the project root):

```bash
cd .claude/skills/browser-use/scripts

# === MANUAL BROWSING (opens browser for user interaction) ===
# Open browser for manual use (waits for user to close)
uv run browser.py open https://example.com --wait 60
uv run browser.py open https://example.com --account myaccount --wait 120

# === AUTOMATION (headless, returns content) ===
# Navigate to a URL and get content
uv run browser.py auto https://example.com
uv run browser.py auto https://example.com --account myaccount

# Take a screenshot
uv run browser.py screenshot https://example.com -o screenshot.png

# Extract text from a page
uv run browser.py text https://example.com --selector "h1"

# Get all links from a page
uv run browser.py links https://example.com

# Save page as PDF
uv run browser.py pdf https://example.com -o page.pdf

# Download a file by clicking a download link
uv run browser.py download https://example.com/downloads "a.download-btn" -o ~/Downloads

# Upload file(s) to a page
uv run browser.py upload https://example.com/upload "input[type=file]" myfile.pdf
uv run browser.py upload https://example.com/upload "input[type=file]" file1.txt file2.txt --submit "button[type=submit]"

# Upload via file chooser dialog (for dynamic inputs)
uv run browser.py upload-chooser https://example.com/upload "button.upload-trigger" myfile.pdf

# Click an element
uv run browser.py click https://example.com "button.submit"

# Fill an input field and press Enter
uv run browser.py fill https://google.com "input[name=q]" "search term" --press Enter

# Extract attribute from elements
uv run browser.py extract https://example.com "img" --attr src --all
```

## Image Download Commands

Download images from websites with optimized performance:

```bash
cd .claude/skills/browser-use/scripts

# Download images directly from src attribute
uv run browser.py download-images https://example.com "img.gallery" -n 10 -o ./images

# Download from Google Images (19x faster with regex extraction)
uv run browser.py download-from-gallery \
  "https://www.google.com/search?q=keyword&tbm=isch&tbs=isz:l" \
  "div[data-id] img" \
  "img[jsname='kn3ccd']" \
  -n 100 \
  -o ~/Downloads \
  -a myaccount

# Search Google Images with size filter
uv run browser.py google-image "landscape wallpaper" -n 50 -o ~/Downloads -s Large

# Download 4K images (3840px+ minimum)
uv run browser.py google-image "wallpaper" -n 20 -o ~/Downloads -s 4k

# Download FullHD images (1920px+ minimum)
uv run browser.py google-image "wallpaper" -n 50 -o ~/Downloads -s fullhd
```

### Google Images Size Filters
CLI size options (filters by minimum dimension):
- `-s 4k` - 3840px minimum (4K resolution)
- `-s fullhd` - 1920px minimum (Full HD)
- `-s Large` - 1000px minimum
- `-s Medium` - 400px minimum
- `-s Icon` - No minimum

Google URL params (used internally):
- `tbs=isz:l` - Large images
- `tbs=isz:m` - Medium images
- `tbs=isz:i` - Icon size

## YouTube Commands

Search and download YouTube videos with duration and date filtering:

```bash
cd .claude/skills/browser-use/scripts

# Search YouTube and get video URLs (returns JSON)
uv run browser.py youtube-search "python tutorial" -n 10
uv run browser.py youtube-search "lofi music" -n 5 -o results.json -s screenshot.png

# Search with duration filter (4-20 minutes)
uv run browser.py youtube-search "lofi music" -n 5 -min 4 -max 20

# Search videos from the last week
uv run browser.py youtube-search "news" -n 10 -t week

# Search with custom date range (YYYYMMDD format)
uv run browser.py youtube-search "tutorial" -n 10 -df 20240101 -dt 20241231

# Download a single video by URL
uv run browser.py youtube-download "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -o ~/Downloads

# Download with quality options
uv run browser.py youtube-download "https://youtube.com/watch?v=..." -q 720p -o ~/Downloads
uv run browser.py youtube-download "https://youtube.com/watch?v=..." -q 1080p -o ~/Downloads

# Download audio only (mp3)
uv run browser.py youtube-download "https://youtube.com/watch?v=..." -a -o ./music

# Search and download in one command
uv run browser.py youtube-download "lofi hip hop" --search -o ~/Downloads
uv run browser.py youtube-download "python tutorial" --search -n 3 -o ~/Downloads

# Search and download with duration filter (4-20 min videos only)
uv run browser.py youtube-download "lofi music" --search -n 5 -min 4 -max 20 -o ~/Downloads

# Search and download videos from a date range
uv run browser.py youtube-download "tutorial" --search -n 5 -df 20240101 -dt 20241231 -o ~/Downloads
```

### YouTube Duration Filters
- `-min N` - Minimum duration in minutes
- `-max N` - Maximum duration in minutes
- Filters use YouTube URL parameters for speed, with Python-side validation as backup

### YouTube Date Filters
- `-t, --upload-date` - Filter by upload date: `hour`, `today`, `week`, `month`, `year`
- `-df, --date-from` - Custom date range start (YYYYMMDD format, e.g., 20240101)
- `-dt, --date-to` - Custom date range end (YYYYMMDD format, e.g., 20241231)

### YouTube Quality Options
- `best` - Best available quality (default)
- `1080p` - 1080p or lower
- `720p` - 720p or lower
- `480p` - 480p or lower
- `360p` - 360p or lower
- `audio` - Best audio only

### YouTube Search Output Format
```json
[
  {
    "url": "https://www.youtube.com/watch?v=...",
    "title": "Video Title",
    "channel": "Channel Name",
    "duration": "10:30",
    "views": "1.2M views",
    "date": "2024-12-01"
  }
]
```

## TikTok Commands

**IMPORTANT:** TikTok blocks headless browsers. Use `--no-headless` for search operations.

```bash
cd .claude/skills/browser-use/scripts

# Login and save session for authenticated operations
uv run browser.py tiktok-login -a mytiktok
uv run browser.py tiktok-login -a mytiktok -w 180  # Extended wait for 2FA

# Search videos (--no-headless required for TikTok)
uv run browser.py tiktok-search "keyword" -n 10 --no-headless
uv run browser.py tiktok-search "#dance" -n 5 --no-headless  # By hashtag
uv run browser.py tiktok-search "cooking" -n 10 -a mytiktok --no-headless  # With account

# Download single video
uv run browser.py tiktok-download "https://tiktok.com/@user/video/123" -o ~/Downloads

# Search and download
uv run browser.py tiktok-download "funny cats" --search -n 5 -o ~/Downloads --no-headless
uv run browser.py tiktok-download "#cooking" --search -n 10 -o ~/Downloads -p 3 --no-headless
```

### TikTok Search Output Format
```json
[
  {
    "url": "https://www.tiktok.com/@user/video/123456789",
    "title": "Video description...",
    "author": "username",
    "views": "1.2M",
    "likes": "50K",
    "date": "2d ago"
  }
]
```

## Authentication

Save and reuse login sessions across browser commands. Uses Chrome with stealth mode to bypass automation detection (works with Google, etc.):

```bash
# Run from scripts folder
cd .claude/skills/browser-use/scripts

# Step 1: Create a login session (opens Chrome for manual login)
# Browser will open maximized - login manually then CLOSE THE BROWSER when done
uv run browser.py create-login https://gemini.google.com/app --account myaccount

# Options:
#   --wait, -w    Seconds to wait for login (default: 120)
#   --channel, -c Browser: chrome, msedge, chromium (default: chrome)

# Step 2: List saved accounts
uv run browser.py accounts

# Step 3: Use saved account with commands
# Manual browsing (opens browser for user interaction)
uv run browser.py open https://gemini.google.com/app --account myaccount

# Automation (headless, returns content)
uv run browser.py auto https://gemini.google.com/app --account myaccount
uv run browser.py screenshot https://gemini.google.com/app -o gemini.png --account myaccount
```

### Storage Location

Authentication is stored in user's home directory `~/.auth/`:
```
~/.auth/
├── account-name.json          # Storage state (cookies, localStorage)
└── profiles/
    └── account-name/          # Persistent browser profile
```

This location is shared across all projects and not committed to git.


### Best Practices
- Use `headless=True` for automation tasks
- Use `headless=False` when debugging or when visual confirmation is needed
- Always close the browser after use
- Use specific selectors (id, data-testid) over generic ones when possible
- Add appropriate waits for dynamic content
- Handle timeouts gracefully with try/except blocks

### Common Selectors
- By ID: `#element-id`
- By class: `.class-name`
- By text: `text=Button Text`
- By role: `role=button[name="Submit"]`
- By CSS: `div.container > p.content`
- By XPath: `xpath=//div[@class='item']`
