---
name: juejin-article-trends
description: 掘金技术文章排行榜查询工具。支持按分类查询热门和最新文章，涵盖前端、后端、AI、移动开发等技术领域。
---

# 掘金热门文章排行榜

## 功能概述

此技能用于获取掘金(juejin.cn)网站的技术文章排行榜数据，包括：
- 文章分类列表（前端、后端、AI、移动开发等）
- 各分类的热门/最新文章排行榜
- 文章详细信息（标题、作者、阅读量、点赞数等）

## 输出格式

### Markdown 输出（默认）

以 Markdown 格式输出文章列表，每篇文章包含以下信息：

```markdown
## 序号. 文章标题
- **作者**: 作者名
- **热度**: 热度值
- **阅读**: 阅读数 | **点赞**: 点赞数 | **收藏**: 收藏数 | **评论**: 评论数
- **摘要**: 文章内容概要
- **链接**: [查看详情](<https://juejin.cn/post/文章ID>)
```

**Markdown 输出特点**：
- 使用 Markdown 格式，可直接在支持 Markdown 的环境中渲染
- 每篇文章之间有空行分隔，便于阅读
- 链接使用 `[查看详情](<链接>)` 格式，可正确处理特殊字符
- 文章按热度或发布时间排序（根据 type 参数）

### JSON 输出（使用 `json` 参数）

```bash
node scripts/juejin.js articles <category_id> [type] [limit] json
```

返回 JSON 格式数据：

```json
{
  "category_id": "6809637769959178254",
  "type": "hot",
  "total": 10,
  "articles": [
    {
      "title": "文章标题",
      "brief": "文章摘要",
      "author": "作者名",
      "authorId": "作者ID",
      "articleId": "文章ID",
      "popularity": 1000,
      "viewCount": 2000,
      "likeCount": 50,
      "collectCount": 30,
      "commentCount": 10,
      "interactCount": 60,
      "url": "https://juejin.cn/post/文章ID",
      "publishTime": 1699123456,
      "tags": ["标签1", "标签2"]
    }
  ]
}
```

**JSON 字段说明**：
- `title`：文章标题
- `brief`：文章摘要
- `author`：作者名称
- `authorId`：作者ID
- `articleId`：文章ID
- `popularity`：热度值
- `viewCount`：阅读数
- `likeCount`：点赞数
- `collectCount`：收藏数
- `commentCount`：评论数
- `interactCount`：互动数
- `url`：文章链接
- `publishTime`：发布时间戳
- `tags`：文章标签数组

## 工作流程

### 1. 获取分类列表

当用户需要了解掘金文章分类时：

```bash
node scripts/juejin.js categories
```

返回示例：
```json
[
  { "id": "6809637769959178254", "name": "前端" },
  { "id": "6809637769959178255", "name": "后端" },
  { "id": "6809637769959178256", "name": "Android" },
  { "id": "6809637769959178257", "name": "iOS" },
  { "id": "6809637769959178258", "name": "人工智能" },
  { "id": "6809637769959178260", "name": "开发工具" },
  { "id": "6809637769959178261", "name": "代码人生" },
  { "id": "6809637769959178262", "name": "阅读" }
]
```

### 2. 获取热门文章

当用户需要获取特定分类的热门文章时：

```bash
node scripts/juejin.js articles <category_id> [type] [limit] [json]
```

参数：
- `category_id`: 分类ID（从分类列表获取）
- `type`: 排序类型，可选 `hot`(热门) 或 `new`(最新)，默认 `hot`
- `limit`: 返回文章数量，默认20
- `json`: 输出JSON格式数据（可选）

**注意**：`type=new` 参数可能因掘金 API 限制而不可用，如遇到 HTTP 500 错误请使用 `type=hot`。

常用分类ID：
- `6809637769959178254` - 后端
- `6809637767543259144` - 前端
- `6809635626879549454` - Android
- `6809635626661445640` - iOS
- `6809637773935378440` - 人工智能

## 使用示例

### 查看所有分类
```bash
node scripts/juejin.js categories
```

### 获取后端热门文章（Markdown 格式）
```bash
node scripts/juejin.js articles 6809637769959178254 hot 10
```

### 获取后端最新文章（JSON 格式）
```bash
node scripts/juejin.js articles 6809637769959178254 new 10 json
```

### 获取人工智能分类的热门文章（JSON 格式）
```bash
node scripts/juejin.js articles 6809637773935378440 hot 20 json
```

## 作者介绍

- 爱海贼的无处不在
- 我的微信公众号：无处不在的技术