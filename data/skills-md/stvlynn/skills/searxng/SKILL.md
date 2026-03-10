---
name: searxng
description: Privacy-respecting web search powered by a local SearXNG instance. Use when searching the web, looking up information, researching topics, or needing quick answers. Supports multiple categories including general, images, videos, news, and more. Aggregates results from 70+ search engines without tracking.
---

# SearXNG Search Skill

Privacy-respecting web search powered by a local [SearXNG](https://github.com/searxng/searxng) metasearch engine.

## Overview

This skill provides fast, private web search by running a local SearXNG instance. It aggregates results from 70+ search engines without tracking or profiling.

- **Private**: No tracking, no profiling, no data collection
- **Fast**: Local instance for quick responses
- **Comprehensive**: Aggregates results from 70+ search engines
- **Precise**: Category-based filtering (general, images, videos, news, files, etc.)
- **Multi-language**: Supports English, Chinese, Japanese, and more

---

## First-time Deployment

> If you already have SearXNG running, skip to [Configuration](#configuration).

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose installed
- A directory for SearXNG data (this guide uses `~/service/searxng`)

### 1. Create project directory

```bash
mkdir -p ~/service/searxng/config ~/service/searxng/data
cd ~/service/searxng
```

### 2. Create `docker-compose.yml`

```yaml
version: '3.8'
services:
  searxng:
    image: docker.io/searxng/searxng:latest
    container_name: searxng
    restart: unless-stopped
    ports:
      - "8888:8080"
    volumes:
      - "./config:/etc/searxng:rw"
      - "./data:/var/cache/searxng:rw"
    environment:
      - SEARXNG_BASE_URL=http://localhost:8888/
    cap_drop:
      - ALL
    cap_add:
      - CHOWN
      - SETGID
      - SETUID
```

### 3. Create `config/settings.yml`

```yaml
use_default_settings: true

server:
  secret_key: "CHANGE_ME_TO_A_RANDOM_STRING"   # ← 必须修改！
  limiter: false        # 本地使用可关闭限流
  image_proxy: true
  port: 8080
  bind_address: "0.0.0.0"

search:
  safe_search: 0
  autocomplete: "google"
  default_lang: "en"
  formats:
    - html
    - json              # ← 必须启用 JSON，脚本依赖此格式

ui:
  default_theme: simple
  theme_args:
    simple_style: auto
```

> **重要**: `secret_key` 必须替换为一个随机字符串。可以用以下命令生成：
> ```bash
> openssl rand -hex 32
> ```

### 4. Start the service

```bash
cd ~/service/searxng
docker compose up -d
```

### 5. Verify

```bash
# 检查容器运行状态
docker compose ps

# 测试 Web 界面
curl -s http://localhost:8888/ | grep -o "searxng" && echo "OK"

# 测试 JSON API（脚本依赖此接口）
curl -s -X POST http://localhost:8888/search \
  -d 'q=test&format=json&categories=general' \
  -H 'Content-Type: application/x-www-form-urlencoded' | python3 -m json.tool | head -5
```

### Troubleshooting

| 问题 | 解决方法 |
|------|----------|
| 端口 8888 被占用 | 修改 `docker-compose.yml` 中的端口映射，如 `"9999:8080"` |
| JSON API 返回 HTML | 确认 `settings.yml` 的 `search.formats` 包含 `json` |
| 容器启动后立即退出 | `docker compose logs` 查看错误，通常是 `secret_key` 未设置 |
| 搜索无结果 | 部分引擎有区域限制，检查网络环境或换用其他引擎 |

### Optional: Enable rate limiting (公网部署时)

如果将 SearXNG 暴露到公网，建议启用 limiter + Valkey：

```yaml
# docker-compose.yml 追加
  valkey:
    image: docker.io/valkey/valkey:8-alpine
    container_name: valkey
    restart: unless-stopped
    command: valkey-server --save 30 1 --loglevel warning
    volumes:
      - "./valkey-data:/data"

# settings.yml 修改
server:
  limiter: true

valkey:
  url: valkey://valkey:6379/0
```

---

## Configuration

### Default Settings
- **Base URL**: `http://localhost:8888`
- **Timeout**: 10 seconds
- **Max Results**: 10 per query
- **Default Category**: General web search

### Environment Variables
```bash
SEARXNG_URL=http://localhost:8888  # SearXNG instance URL
SEARXNG_TIMEOUT=10                  # Request timeout in seconds
SEARXNG_MAX_RESULTS=10              # Maximum results to return
```

## Usage

### Basic Search
```bash
python3 scripts/search.py -q "your search query"
```

### Category Search
```bash
# Image search
python3 scripts/search.py -q "cute cats" -c images

# Video search
python3 scripts/search.py -q "tutorial" -c videos

# News search
python3 scripts/search.py -q "AI news" -c news

# Files (PDF, docs, etc.)
python3 scripts/search.py -q "research paper" -c files
```

### Advanced Options
```bash
# Limit results
python3 scripts/search.py -q "python" -l 5

# Specific language
python3 scripts/search.py -q "中文" --language zh

# Safe search level (0-2)
python3 scripts/search.py -q "family" --safe-search 1

# JSON output
python3 scripts/search.py -q "AI" --json

# Quiet mode (just URLs)
python3 scripts/search.py -q "news" --quiet
```

## Available Categories

| Category | Description |
|----------|-------------|
| `general` (default) | General web search |
| `images` | Image search |
| `videos` | Video search |
| `news` | News articles |
| `files` | Documents (PDF, etc.) |
| `map` | Map results |
| `music` | Music/Audio |
| `social_media` | Social media |
| `it` | IT/Computing |
| `science` | Scientific papers |
| `shopping` | Products |
| `economic` | Business/Finance |
| `entertainment` | Entertainment |
| `repositories` | Code repositories |

## When to Use

**Use when:**
- Searching the web, looking up information, researching topics
- Finding news, articles, or current events
- Looking for images, videos, or media
- Comparing information from multiple sources

**Don't use when:**
- User wants a specific search engine (Google, Bing, etc.) directly
- Searching local files (use file system tools)
- Querying specific APIs (GitHub, npm, etc.) directly

## Output Format

### Text Output (default)
```
🔍 Search: "your query"
📂 Category: general
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Title
   🌐 https://example.com
   📝 Description...
   ⚙️  Source: engine-name
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Found 5 results in 0.32s
```

### JSON Output
```json
{
  "query": "search term",
  "category": "general",
  "results": [
    {
      "title": "Result Title",
      "url": "https://example.com",
      "description": "Result description",
      "engine": "google"
    }
  ],
  "count": 5,
  "time_seconds": 0.32
}
```

## Service Management

```bash
# Check status
bash manage.sh status

# Start / Stop / Restart
bash manage.sh start
bash manage.sh stop
bash manage.sh restart

# View logs
bash manage.sh logs
```

## See Also

- [SearXNG Documentation](https://docs.searxng.org/)
- [SearXNG GitHub](https://github.com/searxng/searxng)
- [Public Instances](https://searx.space)
