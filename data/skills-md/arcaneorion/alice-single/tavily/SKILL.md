---
name: tavily
description: 使用 Tavily API 进行互联网搜索。当需要获取实时新闻、技术研究、深度资料或限制特定域名搜索时使用该技能。
---

# Tavily 搜索技能

此技能允许 Alice 使用 Tavily API 获取高质量的搜索结果，支持多种搜索模式。

## 核心功能

- **基础搜索 (basic)**: 快速获取摘要和结果。
- **深度研究 (research)**: 使用高级搜索深度，返回更全面的 JSON 数据。
- **新闻模式 (news)**: 获取指定天数内的最新新闻。

## 使用方法

在终端运行以下命令：

```bash
# 基础搜索 (默认返回 Alice 可直接阅读的文本)
python skills/tavily/tavily_search.py --query "搜索关键词"

# 深度研究模式 (返回详细 JSON)
python skills/tavily/tavily_search.py --query "研究课题" --mode research --max-results 10

# 新闻模式
python skills/tavily/tavily_search.py --query "热点" --mode news --days 3

# 限制域名搜索
python skills/tavily/tavily_search.py --query "气候变化" --include-domains nature.com science.org
```

## 依赖要求

1. 安装 Python 包: `pip install tavily-python`
2. 环境变量: 需要在项目根目录 `.env` 中配置 `TAVILY_API_KEY`。

## 参数说明

- `--query`, `-q`: 搜索关键词（必填）。
- `--mode`, `-m`: 模式选择，可选 `basic`, `research`, `news`。
- `--max-results`, `-n`: 返回结果数量 (1-20)。
- `--days`, `-d`: 新闻搜索的时间范围。
- `--json`: 在 basic 模式下强制输出 JSON。
- `--include-domains`: 限制搜索的域名列表（空格隔开）。
- `--exclude-domains`: 排除的域名列表。

## 注意事项

Alice 应优先使用默认的 `basic` 模式进行日常问答，仅在需要进行深入研究或处理复杂数据时使用 `research` 模式。
