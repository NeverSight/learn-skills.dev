---
name: toutiao-news-trends
description: 今日头条热点新闻热榜工具。实时获取热门资讯，涵盖时政、财经、社会、科技、娱乐等多领域，自动格式化输出规范内容。
---

# 今日头条新闻热榜

## 技能概述

此技能用于抓取今日头条 PC 端热榜（hot-board）数据，包括：
- 热点标题
- 热度值（HotValue）
- 详情跳转链接（去除冗余查询参数，便于分享）
- 封面图（如有）
- 标签（如“热门事件”等）

数据来源：今日头条 (www.toutiao.com)

## 获取热榜

**重要说明**：
- ⚠️ **默认输出格式为规范 Markdown 格式**（符合输出格式规范要求）
- 如需原始 JSON 数据，请使用 `json` 命令

获取热榜（默认 10 条，按榜单顺序返回，格式化输出）：

```bash
node scripts/toutiao.js
```

获取热榜前 N 条（格式化输出）：

```bash
node scripts/toutiao.js 10
# 或
node scripts/toutiao.js format 10
```

获取热榜（JSON 格式，默认 50 条）：

```bash
node scripts/toutiao.js json
```

获取热榜前 N 条（JSON 格式）：

```bash
node scripts/toutiao.js json 20
```

## 返回数据字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| rank | number | 榜单排名（从 1 开始） |
| title | string | 热点标题 |
| popularity | number | 热度值（HotValue，已转为数字；解析失败时为 0） |
| link | string | 热点详情链接（已清理 query/hash） |
| cover | string \| null | 封面图 URL（如有） |
| label | string \| null | 标签/标识（如有） |
| clusterId | string | 聚合 ID（字符串化） |
| categories | string[] | 兴趣分类英文（如有） |
| categoriesCN | string[] | 兴趣分类中文（已自动映射） |

### 分类映射说明

英文分类已自动映射为中文，例如：
- `finance` → 财经
- `car` → 汽车
- `technology` → 科技
- `entertainment` → 娱乐
- `sports` → 体育
- `society` → 社会
- `international` → 国际
- 等等...

## 输出格式规范

### 默认输出格式

⚠️ **重要**：此技能默认输出为以下规范格式，无需额外配置。

AI助手在展示今日头条热点新闻时，应遵循以下统一格式：

```
## 今日头条最新热点新闻 Top N

**🔥 热度前十名**

N. **新闻标题**
热度：X万
分类：分类标签
[查看详情](<链接>)
---
...
```

**格式要求**：
- 标题使用加粗（**标题**）
- 热度以"万"为单位显示（如：4651万）
- 分类如有多个用"/"分隔，无分类显示"-"
- 链接使用尖括号包裹 `[查看详情](<链接>)`，避免特殊字符导致 Markdown 解析问题
- 每条新闻之间用 `---` 分隔
- 默认显示前10条热榜

## 注意事项

- 该接口为网页端公开接口，返回结构可能变动；若字段缺失可适当容错
- 访问频繁可能触发风控，脚本内置随机 User-Agent 与超时控制
- 该接口不提供文章摘要/概要信息，只能获取标题、热度、链接等基本信息

## 作者介绍

- 爱海贼的无处不在
- 我的微信公众号：无处不在的技术
