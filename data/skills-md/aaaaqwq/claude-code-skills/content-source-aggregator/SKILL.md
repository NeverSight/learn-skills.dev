---
name: content-source-aggregator
description: "统一信息源热点采集。从 X/Twitter、YouTube、B站、GitHub、Reddit、LinuxDo 六大平台免费获取热门内容，输出标准化热点池供内容创作流水线使用。全部使用免费公开 API，无需付费。"
allowed-tools: Read, Write, Edit, Bash, WebFetch
---

# 信息源热点采集器

从 6 大平台免费采集热门内容，输出标准化 JSON 热点池。

## 支持平台

| 平台 | 方式 | 免费额度 | 状态 |
|------|------|---------|------|
| X/Twitter | syndication API (无需认证) | 无限 | ✅ |
| YouTube | RSS Feed (频道级) + yt-dlp | 无限 | ✅ |
| B站 | 公开 API (ranking/v2) | 无限 | ✅ |
| GitHub | Search API (无认证) | 60次/小时 | ✅ |
| Reddit | PullPush API | 无限 | ✅ |
| 抖音 | 热搜 API (无需认证) | 无限 | ✅ |
| LinuxDo | Discourse JSON API | 无限 | ⏳ 需登录态 |
| 小红书 | Web 端 SSR 解析 | 无限 | ⏳ 需登录态 |
| 微信公众号 | 搜狗微信搜索 | 有限 | ⏳ 需登录态 |
| 微信视频号 | 无公开 API | - | ⏳ 需 Playwright |

## 使用方法

```bash
# 采集所有平台
python3 ~/clawd/skills/content-source-aggregator/scripts/fetch_all.py

# 采集单个平台
python3 ~/clawd/skills/content-source-aggregator/scripts/fetch_all.py --source twitter
python3 ~/clawd/skills/content-source-aggregator/scripts/fetch_all.py --source youtube
python3 ~/clawd/skills/content-source-aggregator/scripts/fetch_all.py --source bilibili
python3 ~/clawd/skills/content-source-aggregator/scripts/fetch_all.py --source github
python3 ~/clawd/skills/content-source-aggregator/scripts/fetch_all.py --source reddit
python3 ~/clawd/skills/content-source-aggregator/scripts/fetch_all.py --source linuxdo
```

## 输出

标准化 JSON 写入 `~/clawd/workspace/content-pipeline/hotpool/YYYY-MM-DD.json`

```json
{
  "date": "2026-02-19",
  "fetched_at": "2026-02-19T10:00:00+08:00",
  "items": [
    {
      "source": "reddit",
      "title": "...",
      "url": "...",
      "summary": "...",
      "heat_score": 85,
      "category": "AI/Tech",
      "engagement": {"upvotes": 1200, "comments": 340},
      "fetched_at": "..."
    }
  ]
}
```

## 各平台 API 详情

### X/Twitter
- 端点: `https://syndication.twitter.com/srv/timeline-profile/screen-name/{username}`
- 方式: 解析返回 HTML 中的推文文本
- 可配置关注的账号列表

### YouTube
- 端点: `https://www.youtube.com/feeds/videos.xml?channel_id={id}`
- 方式: RSS XML 解析
- 可配置关注的频道列表
- 备选: yt-dlp 获取 trending

### B站
- 热门排行: `https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all`
- 热搜: `https://api.bilibili.com/x/web-interface/wbi/search/square?limit=10`
- 需要 Referer: https://www.bilibili.com

### GitHub
- 端点: `https://api.github.com/search/repositories?q=stars:>100+pushed:>{date}&sort=stars`
- 无认证 60 次/小时，够用

### Reddit
- 端点: `https://api.pullpush.io/reddit/search/submission/?subreddit={sub}&sort=score&sort_type=desc&size=10`
- 免费无限制

### LinuxDo
- 端点: `https://linux.do/latest.json?order=default`
- Discourse 标准 API，免费公开

## 配置

编辑 `scripts/config.json` 自定义关注的账号/频道/子版块。

## 与内容流水线集成

本 skill 是内容创作 SOP 的 Phase 1（热点采集），输出供 research agent 做选题评分。
