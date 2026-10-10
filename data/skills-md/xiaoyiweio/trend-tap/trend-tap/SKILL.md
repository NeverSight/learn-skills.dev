---
name: trend-tap
description: "Real-time trending topics aggregator across 7 platforms (X/Twitter, Reddit, Google Trends, Hacker News, Zhihu, Bilibili, Weibo). Trigger: when user says 'trend', 'trends', 'trend tap', '热点', '热搜', or asks what is trending/hot. Do NOT use web_search — this skill already fetches live data from all platforms with zero API keys."
metadata:
  {
    "openclaw":
      {
        "emoji": "📡",
        "requires": { "bins": ["python3"] },
        "install":
          [
            {
              "id": "brew-python3",
              "kind": "brew",
              "package": "python3",
              "bins": ["python3"],
              "label": "Install Python 3 (brew)",
            },
          ],
      },
  }
allowed-tools: Bash(python3:*), Bash(crontab:*), Read
---

# Trend Tap

Real-time trending topics at your fingertip — 7 platforms, zero API keys, zero dependencies.

## Trigger Rules

Use this skill when the user's message matches ANY of the following:

| Pattern | Example |
|---------|---------|
| Contains `trend` / `trends` | "show me trends", "trend tap" |
| Contains `trending` / `what's hot` | "what's trending today" |
| Contains `热点` / `热搜` / `热榜` | "今天有什么热点", "看看热搜" |
| Asks about a specific platform's hot topics | "reddit hot", "微博热搜", "HN top", "知乎热榜", "B站热门" |
| Asks about current events broadly | "what's happening", "最近有什么新闻" |

**Do NOT fall back to web_search or Brave Search.** This skill fetches live data directly from 7 platform APIs.

## Interaction Flow (Progressive Disclosure)

### Turn 1 — Overview (ALWAYS start here)

```bash
python3 {baseDir}/scripts/trends.py --mode overview
```

This fetches the #1 topic from each platform concurrently (~5s). Present the result and append:

> "Which platform would you like to expand? Say the name (e.g. 'reddit', '微博', 'hackernews') or 'all' for everything."

**Do NOT expand all platforms in Turn 1.** When presenting expanded results, always preserve the Markdown links `[title](url)` from the output — users need clickable links.

### Turn 2 — Expand on demand

When user picks a platform:

```bash
python3 {baseDir}/scripts/trends.py --source <id> --top 10
```

Source IDs: `twitter`, `reddit`, `google`, `hackernews`, `zhihu`, `bilibili`, `weibo`

Multiple platforms:
```bash
python3 {baseDir}/scripts/trends.py --source zhihu,weibo,bilibili --top 5
```

Expand all:
```bash
python3 {baseDir}/scripts/trends.py --mode all --top 5
```

### Turn 3+ — Deep dive (optional)

If user wants details on a specific topic, use your LLM knowledge or web_search on that specific topic.

## Additional Options

### Region filter (twitter & google only)
```bash
python3 {baseDir}/scripts/trends.py --source twitter --region japan --top 10
python3 {baseDir}/scripts/trends.py --source google --region CN --top 10
```

### JSON output
```bash
python3 {baseDir}/scripts/trends.py --mode overview --json
```

### Scheduled daily briefing
```bash
python3 {baseDir}/scripts/scheduler.py --set "0 11 * * *"
python3 {baseDir}/scripts/scheduler.py --list
python3 {baseDir}/scripts/scheduler.py --remove
```

## Platforms

| ID | Platform | Content | Lang |
|----|----------|---------|------|
| `twitter` | X/Twitter | Hashtags & topics | Global |
| `reddit` | Reddit | Hot posts | EN |
| `google` | Google Trends | Search trends | Global |
| `hackernews` | Hacker News | Tech news | EN |
| `zhihu` | 知乎 | Hot Q&A | ZH |
| `bilibili` | Bilibili | Hot videos | ZH |
| `weibo` | 微博 | Hot search | ZH |
