---
name: web-search
description: 网络搜索与网页内容获取。当用户需要搜索互联网信息、获取网页内容、查找实时数据、进行 websearch 时使用此技能。支持多种搜索工具：WebFetch、Firecrawl skill、Tavily skill。
allowed-tools: WebFetch, Bash
---

# 网络搜索与网页内容获取

## 功能说明
此技能提供全面的网络搜索和网页内容获取能力。

## 可用工具

### 1. WebFetch (OpenClaw 内置)
- **功能**: 获取网页内容
- **使用场景**: 获取特定网页的内容

### 2. Tavily Skill (AI 优化搜索)
- **位置**: `~/clawd/skills/tavily/`
- **功能**: AI 优化的网络搜索
- **命令**: `~/clawd/skills/tavily/scripts/tavily.sh`

#### Tavily 用法
```bash
# 基础搜索
~/clawd/skills/tavily/scripts/tavily.sh search <query> [max_results]

# 深度搜索
~/clawd/skills/tavily/scripts/tavily.sh search <query> --deep

# 搜索并提取
~/clawd/skills/tavily/scripts/tavily.sh extract <query> [max_results]
```

### 3. Firecrawl Skill (专业抓取)
- **位置**: `~/clawd/skills/firecrawl/`
- **功能**: 专业网页抓取和数据提取
- **命令**: `~/clawd/skills/firecrawl/scripts/firecrawl.sh`

#### Firecrawl 用法
```bash
# 抓取单个网页
~/clawd/skills/firecrawl/scripts/firecrawl.sh scrape <url> [format]

# 搜索并抓取
~/clawd/skills/firecrawl/scripts/firecrawl.sh search <query> [limit]

# 批量爬取
~/clawd/skills/firecrawl/scripts/firecrawl.sh crawl <url> [max_pages]
```

## 使用场景

### 何时使用 Tavily
- 搜索互联网信息
- 获取实时数据
- 需要 AI 优化的搜索结果

### 何时使用 WebFetch
- 简单获取网页内容
- 快速查看页面信息

### 何时使用 Firecrawl
- 复杂网页抓取
- 结构化数据提取
- 批量网站爬取

## 示例

### 搜索 Polymarket 信息 (Tavily)
```bash
~/clawd/skills/tavily/scripts/tavily.sh search "Polymarket Fed decision March 2026" 5
```

### 抓取特定页面 (Firecrawl)
```bash
~/clawd/skills/firecrawl/scripts/firecrawl.sh scrape "https://polymarket.com/event/fed-decision-in-march-885"
```

# 网络搜索与网页内容获取

## 功能说明
此技能提供全面的网络搜索和网页内容获取能力，包括：
- 互联网搜索（新闻、信息、数据）
- 网页内容抓取和解析
- 实时数据查询
- 多源搜索结果整合

## 可用工具

### 1. OpenClaw 内置 WebSearch
- **功能**: 互联网搜索
- **使用场景**: 搜索新闻、信息、实时数据
- **触发**: 用户问需要实时信息的问题时

### 2. OpenClaw 内置 WebFetch
- **功能**: 获取网页内容
- **使用场景**: 获取特定网页的内容
- **触发**: 用户提供 URL 并要求获取内容时

### 3. Firecrawl MCP
- **功能**: 专业网页抓取和数据提取
- **工具**: mcp__firecrawl__scrape, mcp__firecrawl__crawl, mcp__firecrawl__search
- **使用场景**: 复杂网页抓取、结构化数据提取、批量爬取
- **优势**: 支持复杂网页、动态内容、结构化输出

## 使用场景

### 何时使用 WebSearch
- "搜索最新的 AI 新闻"
- "查找 Polymarket 最新赔率"
- "今天的天气怎么样"
- "某公司的最新股价"

### 何时使用 WebFetch
- "获取这个网页的内容"
- "读取这个 URL 的内容"
- "这个页面说了什么"

### 何时使用 Firecrawl MCP
- "抓取这个网站的所有产品信息"
- "从这个网页提取结构化数据"
- "爬取这个网站的多个页面"

## 工作流程

1. **分析需求**: 确定需要搜索还是抓取
2. **选择工具**:
   - 简单搜索 → WebSearch
   - 单页抓取 → WebFetch 或 mcp__firecrawl__scrape
   - 复杂抓取 → mcp__firecrawl__crawl
3. **执行操作**: 调用相应工具
4. **整合结果**: 将搜索结果整合到回答中

## 示例

### 搜索信息
```
用户: "搜索一下最新的 AI 新闻"
操作: 使用 WebSearch 搜索 "AI news latest"
```

### 获取网页内容
```
用户: "获取 https://example.com 的内容"
操作: 使用 WebFetch 或 mcp__firecrawl__scrape
```

### 结构化数据提取
```
用户: "从这个网页提取所有产品价格"
操作: 使用 mcp__firecrawl__scrape 并指定提取格式
```

## 注意事项

- 搜索结果可能包含过时或不准确的信息，需要验证
- 网页抓取需要遵守网站的 robots.txt 和使用条款
- 对于付费内容或需要登录的页面，可能无法直接获取
- 大量抓取可能触发反爬虫机制
