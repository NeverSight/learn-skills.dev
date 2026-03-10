---
name: firecrawl
description: 专业网页抓取和数据提取。使用 Firecrawl API 抓取网页、提取结构化数据、批量爬取网站。当用户需要抓取复杂网页、提取结构化数据、批量爬取时使用此技能。
allowed-tools: Bash, Read, Write, Edit
---

# Firecrawl 网页抓取

## 功能说明
此技能使用 Firecrawl API 提供专业网页抓取能力：
- 单页抓取（支持动态内容）
- 结构化数据提取
- 批量网站爬取
- 搜索并抓取

## 使用方式

### 1. 抓取单个网页
```bash
./scripts/firecrawl.sh scrape <url> [format]
```
- format: markdown (默认), html, text, json

### 2. 提取结构化数据
```bash
./scripts/firecrawl.sh extract <url> <schema>
```

### 3. 批量爬取网站
```bash
./scripts/firecrawl.sh crawl <url> [max_pages]
```

### 4. 搜索并抓取
```bash
./scripts/firecrawl.sh search <query> [limit]
```

## API Key
存储在: `pass show api/firecrawl`

## 示例

### 抓取 Polymarket 页面
```bash
./scripts/firecrawl.sh scrape "https://polymarket.com/event/fed-decision-in-march-885"
```

### 提取产品信息
```bash
./scripts/firecrawl.sh extract "https://example.com/product" '{"name": "string", "price": "number"}'
```

### 搜索 AI 新闻
```bash
./scripts/firecrawl.sh search "latest AI news" 5
```

## 注意事项
- Firecrawl 有使用限制（取决于套餐）
- 复杂网页可能需要更长的处理时间
- 某些网站可能有反爬虫机制
