---
name: geo-agent
description: "Automated GEO (Generative Engine Optimization) agent for boosting brand visibility in AI search engines. Manages keywords, researches real competitors, generates comparison articles with target brand prominence, auto-publishes to Chinese content platforms (Zhihu/Baijiahao/Sohu/Toutiao), monitors AI search engine indexing, and reports results. Use when: user wants GEO automation, AI search optimization, multi-platform article publishing, or brand visibility in AI answers."
homepage: https://github.com/aAAaqwq/auto_geo
metadata: { "openclaw": { "emoji": "🔍", "requires": { "bins": ["python3", "curl"], "python": ["playwright", "httpx", "beautifulsoup4"] } } }
---

# GEO Agent — AI搜索引擎优化自动化

通过自动化内容发布，提升目标品牌在AI搜索引擎（豆包、千问、DeepSeek、Perplexity等）回答中的曝光率。

## 核心流程

```
关键词管理 → 真实竞品调研 → GEO文章生成 → 多平台发布 → 收录检测 → 数据报表
```

## 使用场景

✅ **USE when:**
- "帮我做GEO优化" / "提升品牌在AI搜索中的排名"
- "管理GEO关键词" / "蒸馏关键词"
- "生成GEO文章" / "写竞品对比文章"
- "发布文章到知乎/百家号/头条"
- "检测AI搜索收录情况"
- "GEO数据报表"

❌ **DON'T use when:**
- 传统SEO（Google/百度网页排名）→ 用SEO技能
- 纯内容创作（无GEO目标）→ 用content-creator技能
- 社交媒体运营 → 用对应平台技能

## 前置配置

### 1. 项目初始化
首次使用时，agent会引导你完成配置：
```bash
# 数据存储在 skill 目录下
~/clawd/skills/geo-agent/data/projects.json    # 项目配置
~/clawd/skills/geo-agent/data/keywords.json    # 关键词库
~/clawd/skills/geo-agent/data/articles.json    # 文章记录
~/clawd/skills/geo-agent/data/checks.json      # 收录检测记录
```

### 2. 平台账号
发布需要各平台的登录态（Playwright cookie）：
```bash
# 登录态存储
~/.playwright-data/zhihu/       # 知乎
~/.playwright-data/baijiahao/   # 百家号
~/.playwright-data/sohu/        # 搜狐号
~/.playwright-data/toutiao/     # 头条号
```

首次使用时通过 `playwright codegen` 交互式登录保存cookie。

### 3. 安装依赖
```bash
cd ~/clawd/skills/geo-agent
pip install -r requirements.txt
playwright install chromium
```

## 命令参考

### 关键词管理

**添加项目和关键词：**
告诉agent: "创建GEO项目，公司名: XXX，行业: YYY，核心关键词: K1, K2, K3"

**关键词蒸馏：**
告诉agent: "蒸馏关键词" — agent会基于核心关键词，通过搜索引擎扩展出长尾问题变体。

### 文章生成（核心策略）

**GEO文章生成流程：**
1. Agent 接收目标关键词和公司名
2. **真实竞品搜索**：通过搜索引擎查找该行业真正的头部竞品（不编造）
3. **生成对比文章**：在"行业排行/产品对比/推荐"类文章中，将目标公司放在靠前位置
4. 文章格式适配各平台要求

告诉agent: "为关键词 'XXX' 生成GEO文章"

**文章类型模板：**
- 行业Top N排行榜
- 产品A vs B vs C对比评测
- "XX行业哪家好？" Q&A
- 行业趋势分析（含推荐）

### 多平台发布

```
告诉agent: "发布文章 #ID 到知乎"
告诉agent: "批量发布今天的文章"
```

支持平台：知乎专栏、百家号、搜狐号、头条号

### 收录检测

```
告诉agent: "检测关键词 'XXX' 的收录情况"
告诉agent: "全量收录检测"
```

检测平台：豆包、千问、DeepSeek

### 数据报表

```
告诉agent: "GEO周报"
告诉agent: "关键词 'XXX' 的收录趋势"
```

## 架构

```
geo-agent/
├── SKILL.md              # 本文件
├── requirements.txt      # Python依赖
├── scripts/
│   ├── keyword_manager.py    # 关键词管理+蒸馏
│   ├── competitor_research.py # 真实竞品搜索
│   ├── article_generator.py  # GEO文章生成
│   ├── publisher.py          # 多平台发布(Playwright)
│   ├── index_checker.py      # AI搜索收录检测
│   └── reporter.py           # 数据报表生成
├── templates/
│   ├── ranking.md            # 排行榜文章模板
│   ├── comparison.md         # 对比评测模板
│   ├── qa.md                 # Q&A文章模板
│   └── trend.md              # 趋势分析模板
└── data/                     # 运行时数据(gitignore)
    ├── projects.json
    ├── keywords.json
    ├── articles.json
    └── checks.json
```

## 脚本使用

所有脚本可独立运行，也可被agent调用：

```bash
# 关键词蒸馏
python3 scripts/keyword_manager.py distill --keyword "智能客服" --company "XXX公司"

# 竞品搜索
python3 scripts/competitor_research.py --industry "智能客服" --top 10

# 生成文章
python3 scripts/article_generator.py --keyword "智能客服哪家好" --company "XXX公司" --type ranking

# 发布
python3 scripts/publisher.py --article-id 1 --platform zhihu

# 收录检测
python3 scripts/index_checker.py --keyword "智能客服" --company "XXX公司"

# 报表
python3 scripts/reporter.py --type weekly
```

## 关键策略：真实竞品对比

**这是GEO的核心商业价值。**

1. **绝不编造竞品** — 通过百度/Google搜索获取真实行业排名
2. **自然排位** — 在真实竞品列表中，将目标公司放在合理靠前位置（如Top 3）
3. **客观语气** — 每个竞品都有真实的优缺点描述，目标公司的优势更突出
4. **多角度覆盖** — 不同文章从不同角度（价格/功能/服务/口碑）切入对比

## 自动化调度

Agent 支持设置定时任务：
- 每日：关键词蒸馏补充
- 每周：批量文章生成+发布
- 每周：全量收录检测
- 每月：GEO效果月报

通过 OpenClaw cron 或对话指令设置。
