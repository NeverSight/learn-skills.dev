---
name: podcast-downloader
description: 小宇宙播客下载工具。从小宇宙(xiaoyuzhoufm.com)下载播客音频和Show Notes。自动转换为MP3格式（兼容Sanag、小游等骨传导蓝牙耳机、水下游泳时离线播放）。当用户需要下载播客、保存播客音频、提取播客文字内容时使用。支持：(1) 单集下载，(2) 批量下载，(3) 自定义音质，(4) 自动保存Show Notes为Markdown。音频保存到百度云盘同步目录，个人离线收听后删除，不用于传播。
license: MIT. LICENSE.txt has complete terms.
---

# Podcast Downloader

Download podcast audio and show notes from xiaoyuzhoufm.com (小宇宙).

## Quick Start

```bash
# Download single episode
./scripts/download.sh "https://www.xiaoyuzhoufm.com/episode/abc123def456ghi789jklmno"
```

## Output

```
~/Documents/podcast/  # Default output directory
└── PodcastName-EpisodeTitle/
    ├── EpisodeTitle.mp3
    └── EpisodeTitle.md
```

## Workflow

1. **Extract Info** - Parse `__NEXT_DATA__` JSON from episode page
2. **Download m4a** - Get audio file from CDN
3. **Convert to MP3** - Required for Bluetooth headphones compatibility
4. **Delete m4a** - Save disk space
5. **Save Show Notes** - Extract shownotes as markdown

## Requirements

- `curl` - HTTP requests
- `jq` - JSON parsing
- `ffmpeg` - Audio conversion

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PODCAST_DIR` | `~/Documents/podcast/` | Output directory |
| `AUDIO_QUALITY` | `0` | MP3 quality (0=best, 4=normal) |
| `KEEP_M4A` | `false` | Keep original m4a file |

## Quick Reference

| Task | Command |
|------|---------|
| Download single episode | `./scripts/download.sh <URL>` |
| Batch download | See reference.md |
| Custom quality | `AUDIO_QUALITY=2 ./scripts/download.sh <URL>` |
| Keep m4a | `KEEP_M4A=true ./scripts/download.sh <URL>` |

## Files

- `SKILL.md` - This file (quick start)
- `reference.md` - Advanced usage, batch download, troubleshooting
- `scripts/download.sh` - Main download script
- `LICENSE.txt` - MIT License

## Next Steps

- For batch download, see reference.md
- For troubleshooting, see reference.md
