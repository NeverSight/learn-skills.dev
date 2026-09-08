---
name: cinema-manager
description: Personal media library management — discover content, save to Quark cloud drive, auto-organize for Infuse/Plex. Plugin system for content sources. Use when user wants to find/watch movies, save to cloud drive, or manage media library.
---

# Cinema Manager

Media discovery → Cloud save → Library organization.

## Quick Start

```bash
python3 scripts/cinema.py auto "电影名"     # search + save + organize
python3 scripts/cinema.py search "电影名"   # search only
python3 scripts/cinema.py plugins           # list plugins
```

## Config

`config.json` (not committed, create from `config.example.json`):
- `quark.cookie` — Quark session cookie (login to pan.quark.cn, copy cookie from browser DevTools)
- `plugins` — enable/disable content source plugins
- `save_folder` — Quark folder name (default: "影视资源")

## Adding Content Sources

1. Copy `scripts/plugins/example.py` to `scripts/plugins/your_site.py`
2. Implement `search()` and `extract_link()`
3. Add `"your_site": {"enabled": true}` to config.json

## Library Management

`cinema.py organize <fid> <title> --type movie|tv`

Organizes files into Infuse/Plex-compatible structure:
- Movies: `影视资源/Movie Name (Year)/Movie Name (Year).ext`
- TV: `影视资源/Show Name/Season XX/Show Name - SXXEXX.ext`

## Workflow

1. User says "I want to watch X"
2. `cinema.py search` across all configured sources
3. Score results, pick best quality version
4. `cinema.py save` → quark drive
5. `cinema.py organize` → proper folder structure
6. Infuse/Plex auto-detects and fetches metadata
