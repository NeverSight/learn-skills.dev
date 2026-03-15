---
name: content-factory
description: "Automated content production pipeline: hot topic aggregation from 10+ platforms (Bilibili, GitHub, Reddit, YouTube, Weibo, Zhihu, etc.), AI-powered topic scoring, multi-platform content generation (Xiaohongshu, WeChat, Twitter), draft review, and auto-publishing. Use when: user wants daily content pipeline, hot topic collection, content generation, article publishing, or content factory automation."
homepage: https://github.com/aAAaqwq/AGI-Super-Skills
metadata: { "openclaw": { "emoji": "📰", "requires": { "bins": ["python3", "curl"], "python": ["httpx", "beautifulsoup4"] } } }
---

# Content Factory — 内容自动生产分发工厂

从热点采集到内容生成到多平台发布的全流程自动化。Daniel 每天只需 2 分钟挑选主题。

## 核心流程

```
热点采集(10+平台) → AI选题评分 → 推送Top10给用户
                                    ↓
                          用户选择主题(或自定义)
                                    ↓
                          多平台内容生成(LLM)
                                    ↓
                          草稿审核 → 确认发布
                                    ↓
                          自动发布 → 数据追踪
```

## 使用场景

✅ **USE when:**
- "今日热点有什么" / "采集今天的热门话题"
- "帮我生成内容" / "写篇小红书文章"
- "选题评分" / "推荐今天该写什么"
- "发布到小红书/微信/Twitter"
- "运行内容工厂流水线" / "跑一遍完整流程"
- "看看今天的草稿" / "审核内容"

❌ **DON'T use when:**
- GEO优化（AI搜索排名）→ 用 geo-agent
- 纯SEO关键词优化 → 用 SEO 技能
- 单次写作（无流水线需求）→ 用 content-creator

## 数据目录

```
data/
├── hotpool/          # 每日热点池 (YYYY-MM-DD.json)
├── topics/           # 评分选题 (YYYY-MM-DD.json)
├── drafts/           # 生成草稿 (YYYY-MM-DD/)
├── reviewed/         # 审核通过
├── published/        # 已发布记录
├── config/           # 运行配置
│   └── sources.json  # 采集源配置
├── templates/        # 平台模板
│   ├── xiaohongshu.md
│   ├── wechat.md
│   └── twitter.md
└── assets/           # 图片等素材
```

## 脚本说明

| 脚本 | 功能 | 依赖 |
|------|------|------|
| `scripts/aggregator/fetch_all.py` | 10+平台热点采集 | curl, python3 |
| `scripts/topic_scorer.py` | AI选题评分(Top10) | LLM API (DeepSeek/GLM) |
| `scripts/content_generator.py` | 多平台内容生成 | LLM API |
| `scripts/draft_reviewer.py` | 草稿审核推送 | Telegram API |
| `scripts/auto_publisher.py` | 自动发布 | playwright (optional) |
| `scripts/topic_presenter.py` | 选题卡片推送 | Telegram API |
| `scripts/run_daily.sh` | 全流程串联 | bash |
| `scripts/paths.py` | 路径配置(可移植) | - |

## 采集源 (10+)

| 平台 | 方式 | 内容类型 |
|------|------|---------|
| B站热榜 | API | 视频/动态 |
| GitHub Trending | API | 开源项目 |
| Reddit | API | 讨论/新闻 |
| YouTube | API | 视频 |
| 微博热搜 | API | 社交热点 |
| 知乎热榜 | API | 深度讨论 |
| 头条 | API | 新闻资讯 |
| 抖音 | API | 短视频 |
| Twitter/X | Syndication | KOL动态 |
| LinuxDo | API | 技术社区 |

## 安装依赖

```bash
cd ~/clawd/skills/content-factory
pip install -r requirements.txt
```

## 完整流水线

```bash
# 手动执行全流程
bash scripts/run_portable.sh

# 或分步执行
python3 scripts/aggregator/fetch_all.py          # Step 1: 热点采集
python3 scripts/topic_scorer.py       # Step 2: AI评分
python3 scripts/topic_presenter.py    # Step 3: 推送选题
python3 scripts/content_generator.py --top 3  # Step 4: 内容生成
python3 scripts/draft_reviewer.py --all       # Step 5: 草稿审核
# python3 scripts/auto_publisher.py   # Step 6: 发布(需确认)
```

## 与 Ralph CEO Loop 配合

内容工厂可以通过 Ralph CEO Loop 进行持续迭代：
- 小data: 热点采集 + 数据清洗
- 小research: 话题深度调研
- 小content: 内容生成 + 文案优化
- 小pm: 流程协调 + 质量验收
- 小market: 发布策略 + 渠道优化

## 配置

### 采集源配置 (`data/config/sources.json`)
可启用/禁用各平台，配置关注的账号、频道等。

### LLM 配置
评分和生成使用 OpenAI-compatible API：
- 默认: DeepSeek (评分) + GLM-5 (生成)
- 通过环境变量 `LLM_API_KEY` / `LLM_BASE_URL` 覆盖
