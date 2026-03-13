---
name: iopho-searching-videos
description: Search videos across YouTube, Bilibili, and other platforms without downloading
allowed-tools: Bash(yt-dlp *), Bash(python3 *)
user-invocable: true
argument-hint: <query> [--platform youtube|bilibili|all] [--limit N] [--json]
---

# iopho-searching-videos — Cross-Platform Video Search

Search for videos across multiple platforms and return structured metadata — without downloading anything.

## Prerequisites

Check what's available:

!`which yt-dlp 2>/dev/null && echo "yt-dlp: ✓" || echo "yt-dlp: ✗ — install via: pip install yt-dlp or brew install yt-dlp"`

!`python3 -c "from duckduckgo_search import DDGS; print('duckduckgo-search: ✓')" 2>/dev/null || echo "duckduckgo-search: ✗ (optional) — install via: pip install duckduckgo-search"`

**Minimum requirement**: `yt-dlp` (covers 19+ platforms with native search).
**Optional**: `duckduckgo-search` for cross-platform web video search aggregation.

## Platform Search Matrix

| Platform | Search Prefix | Example |
|----------|---------------|---------|
| YouTube | `ytsearch` | `ytsearch10:SaaS demo` |
| YouTube (by date) | `ytsearchdate` | `ytsearchdate5:product video 2026` |
| Bilibili | `BiliBiliSearch` | `BiliBiliSearch:产品介绍` |
| SoundCloud | `scsearch` | `scsearch:ambient music` |
| Niconico | `nicosearch` | `nicosearch:ボカロ` |
| All video (web) | DuckDuckGo | Cross-platform aggregation |

## Quick Reference

**Basic search** (YouTube, top 5):
```bash
yt-dlp --flat-playlist --dump-json "ytsearch5:$QUERY" 2>/dev/null | python3 -c "
import sys, json
for line in sys.stdin:
    v = json.loads(line)
    dur = f\"{v.get('duration',0)//60}:{v.get('duration',0)%60:02d}\" if v.get('duration') else '?'
    print(f\"  {v.get('title','?')}\")
    print(f\"    Duration: {dur} | Views: {v.get('view_count','?')} | URL: https://youtube.com/watch?v={v['id']}\")
    print()
"
```

**Bilibili search**:
```bash
yt-dlp --flat-playlist --dump-json "BiliBiliSearch:$QUERY" 2>/dev/null | python3 -c "
import sys, json
for line in sys.stdin:
    v = json.loads(line)
    dur = f\"{v.get('duration',0)//60}:{v.get('duration',0)%60:02d}\" if v.get('duration') else '?'
    print(f\"  {v.get('title','?')}\")
    print(f\"    Duration: {dur} | URL: {v.get('url', v.get('webpage_url', '?'))}\")
    print()
"
```

**Filter by duration** (e.g., under 30 seconds):
```bash
yt-dlp --flat-playlist --dump-json --match-filter "duration<30" "ytsearch20:$QUERY"
```

**Full JSON metadata** (for programmatic use):
```bash
yt-dlp --flat-playlist --dump-json "ytsearch5:$QUERY" 2>/dev/null
```

**Web-wide video search** (via DuckDuckGo, no API key needed):
```bash
python3 -c "
from duckduckgo_search import DDGS
results = DDGS().videos('$QUERY', max_results=5)
for v in results:
    print(f\"  {v.get('title','?')}\")
    print(f\"    Duration: {v.get('duration','?')} | Source: {v.get('publisher','?')} | URL: {v.get('content', '?')}\")
    print()
"
```

## Execute

Parse the user's arguments and run the appropriate search:

```bash
# Parse arguments from: $ARGUMENTS
# Expected format: <query> [--platform youtube|bilibili|all] [--limit N] [--json]
#
# Default: --platform youtube --limit 5
#
# The agent should:
# 1. Extract the query, platform, limit, and json flag from $ARGUMENTS
# 2. Choose the right search prefix based on platform
# 3. Run yt-dlp with --flat-playlist --dump-json
# 4. Format output as a readable table (or raw JSON if --json)
# 5. If --platform all, also try DuckDuckGo if available
```

## Advanced Usage

**Search with date sorting** (YouTube only):
```bash
yt-dlp --flat-playlist --dump-json "ytsearchdate10:query"
```

**Search and preview metadata** of a specific video:
```bash
yt-dlp --dump-json "https://youtube.com/watch?v=VIDEO_ID" 2>/dev/null | python3 -c "
import sys, json
v = json.loads(sys.stdin.read())
print(f\"Title: {v['title']}\")
print(f\"Duration: {v['duration']}s | Views: {v.get('view_count','?')}\")
print(f\"Channel: {v.get('channel','?')} | Upload: {v.get('upload_date','?')}\")
print(f\"Description: {v.get('description','')[:200]}...\")
print(f\"Tags: {', '.join(v.get('tags',[])) if v.get('tags') else 'none'}\")
"
```

**Combine with iopho-getting-videos**: After finding videos, use `/iopho-getting-videos <url>` to download.

## Supported yt-dlp Search Extractors

Full list of platforms with built-in search support:
YouTube, SoundCloud, Bilibili, Niconico, Dailymotion, Google Video, Yahoo, GameJolt, Mail.ru, Rokfin, and more.

Run `yt-dlp --list-extractors | grep -i search` to see all available search extractors.

## Tips

- Use `--match-filter "duration<60"` to find short videos (< 1 minute)
- Use `--match-filter "view_count>10000"` to find popular videos
- Combine filters: `--match-filter "duration<30 & view_count>1000"`
- For B站, search queries work best in Chinese
- DuckDuckGo search covers platforms that yt-dlp doesn't have native search for (Vimeo, TikTok, Twitter/X, etc.)
