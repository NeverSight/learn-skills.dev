---
name: music-discovery
description: 音乐发现 — 搜索 iTunes API 查找歌曲/专辑/艺人信息。
triggers:
  intent_patterns:
    - "音乐|music|歌曲|song|album|专辑|artist|听歌"
  context_signals:
    keywords: ["music", "音乐", "歌曲", "song", "album"]
  confidence_threshold: 0.6
priority: 5
requires_tools: [bash]
max_tokens: 200
cooldown: 30
---

# music-discovery

音乐搜索和发现：通过 iTunes Search API 查找歌曲。

## 调用

```bash
python3 skills/music-discovery/run.py search --query '周杰伦 晴天'
```
