---
name: find-news
description: |
  多引擎搜索 API 工具，支持通用网页搜索和新闻搜索。
  使用场景：
  - 用户要求搜索网页、新闻、社交媒体内容
  - 需要从 Google/Baidu/Bing/Yahoo/DuckDuckGo 搜索
  - 需要搜索微信公众号、YouTube、GitHub、Reddit、Bilibili
  - 需要获取搜索结果的完整内容（crawl_results > 0）
  - 需要最新新闻和热点追踪
---

# Find News 技能

## 概述

这个技能提供多引擎搜索能力，通过调用官方 API 实现快速搜索。**开箱即用，跨平台支持（Windows/Mac/Linux）**。

## API 接口

### 搜索接口

**端点**: `POST http://36.151.144.35:3001/api/v1/search`

**认证**: `Bearer sk_test_a6f84bf78896f10b2d28aebd7857744c`

**请求参数**:

- `query` (string, 必需): 搜索关键词
- `search_service` (string, 必需): 搜索服务名称
  - `baidu`: 百度搜索
  - `google`: Google 搜索
  - `bing`: Bing 搜索
  - `duckduckgo`: DuckDuckGo
  - `yahoo`: Yahoo 搜索
  - `wechat`: 微信公众号
  - `youtube`: YouTube
  - `github`: GitHub
  - `reddit`: Reddit
  - `bilibili`: 哔哩哔哩
- `max_results` (number, 可选): 返回结果数量 (1-20, 默认 3)
- `crawl_results` (number, 可选): 爬取完整内容的结果数 (0-10, 默认 0)
  - `0`: 只返回搜索摘要（快速）
  - `1-10`: 爬取完整页面内容（慢，成本高）

**请求示例**:

```json
{
  "query": "人工智能",
  "search_service": "baidu",
  "max_results": 5,
  "crawl_results": 0
}
```

**响应示例**:

```json
{
  "results": [
    {
      "title": "搜索结果标题",
      "url": "https://example.com",
      "snippet": "搜索结果摘要...",
      "content": "完整内容（仅当 crawl_results > 0 时）"
    }
  ],
  "total": 5,
  "cached": false
}
```

### 新闻接口

**端点**: `POST http://36.151.144.35:3001/api/v1/news`

**认证**: `Bearer sk_test_a6f84bf78896f10b2d28aebd7857744c`

**请求参数**:

- `query` (string, 必需): 搜索关键词
- `search_service` (string, 可选): 新闻服务名称
  - `google` (默认): Google News
  - `bing`: Bing News
  - `duckduckgo`: DuckDuckGo News
  - `yahoo`: Yahoo News
- `max_results` (number, 可选): 返回结果数量 (1-20, 默认 3)
- `crawl_results` (number, 可选): 爬取完整内容的结果数 (0-10, 默认 0)

**请求示例**:

```json
{
  "query": "科技新闻",
  "search_service": "google",
  "max_results": 10,
  "crawl_results": 0
}
```

## 使用场景

### 场景 1: 快速获取搜索摘要（默认，推荐）

**用户**: "帮我搜索一下最新的 AI 新闻"

**Agent 操作**: 发送 POST 请求到新闻接口

```json
{
  "query": "AI",
  "search_service": "google",
  "max_results": 5,
  "crawl_results": 0
}
```

→ 返回 5 条新闻标题和摘要（**快速，0.5秒，每条 10 积分**）

### 场景 2: 深度内容抓取（仅在必要时使用）

**用户**: "我需要这篇文章的完整内容"

**Agent 操作**: 发送 POST 请求到搜索接口

```json
{
  "query": "文章标题",
  "search_service": "baidu",
  "max_results": 1,
  "crawl_results": 1
}
```

→ 返回完整页面内容（**慢，10-30秒，成本 10 积分**）

### 场景 3: 多平台搜索

**用户**: "在微信公众号和 B 站搜索'Python 教程'"

**Agent 操作**: 发送两个 POST 请求

请求 1 - 微信公众号:
```json
{
  "query": "Python教程",
  "search_service": "wechat",
  "max_results": 5,
  "crawl_results": 0
}
```

请求 2 - 哔哩哔哩:
```json
{
  "query": "Python教程",
  "search_service": "bilibili",
  "max_results": 5,
  "crawl_results": 0
}
```

### 场景 4: GitHub 代码搜索

**用户**: "搜索 GitHub 上的 react hooks 相关项目"

**Agent 操作**: 发送 POST 请求

```json
{
  "query": "react hooks",
  "search_service": "github",
  "max_results": 10,
  "crawl_results": 0
}
```

### 场景 5: YouTube 视频搜索

**用户**: "在 YouTube 上搜索编程教程"

**Agent 操作**: 发送 POST 请求

```json
{
  "query": "programming tutorial",
  "search_service": "youtube",
  "max_results": 5,
  "crawl_results": 0
}
```

## 定价

- 每个搜索结果：10 积分
- 缓存命中：免费（30 分钟内相同查询）
- 相同查询 30 分钟内第二次调用免费

## ⚠️ 重要提示

### 性能

- `crawl_results=0`（默认）：0.5-2 秒
- `crawl_results=1-10`：每个结果增加 10-30 秒

### 成本

- 每个搜索结果：10 积分
- 缓存命中：免费（30 分钟内相同查询）
- **建议**：优先使用摘要，只在必要时抓取完整内容

### 最佳实践

1. **默认使用** `max_results: 3, crawl_results: 0`（快速获取摘要）
2. **只有用户明确要求"完整内容"时** 才设置 `crawl_results > 0`
3. **搜索前** 先检查是否有缓存（相同查询 30 分钟内免费）
4. **合理控制数量** `max_results` 不要设置过大，避免不必要的成本

## 注意事项

1. 默认使用 `crawl_results: 0` 以获得快速响应
2. 设置 `crawl_results > 0` 会显著增加延迟（10-30秒/页）
3. 注意控制请求频率，避免超出限流
4. 相同查询 30 分钟内会使用缓存，免费且更快
5. 所有请求必须在 Header 中包含 `Authorization: Bearer sk_test_a6f84bf78896f10b2d28aebd7857744c`
6. Content-Type 必须设置为 `application/json`

## 错误处理

常见错误码：

- `400`: 请求参数错误
- `401`: 认证失败（API Key 无效）
- `429`: 请求频率超限
- `500`: 服务器内部错误

建议在请求失败时进行重试，最多重试 3 次。
