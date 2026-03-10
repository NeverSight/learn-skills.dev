---
name: web-content-fetcher
description: >
  网页正文内容提取。支持 Jina Reader / Scrapling+html2text / web_fetch 三级降级策略，
  自动返回干净的 Markdown 格式正文，保留标题、链接、图片 URL、列表结构。
  能读取微信公众号文章（Jina 做不到的场景）。
  触发条件：用户要抓取某个 URL 的正文内容、读取某篇文章、提取网页内容等。
---

# Web Content Fetcher — 网页正文提取

## 能力说明

给一个 URL，返回干净的 Markdown 格式正文，保留：
- 标题层级（# ## ###）
- 超链接（[文字](url)）
- 图片（![alt](url)）
- 列表、代码块、引用块

## 提取策略（三级降级）

```
URL
 ↓
1. Jina Reader（首选）
   web_fetch("https://r.jina.ai/<url>", maxChars=30000)
   优点：快（~1.5s），格式干净
   限制：200次/天免费配额
   失败场景：微信公众号（403）、部分国内平台
 ↓
2. Scrapling + html2text（Jina 超限或失败时）
   exec: python3 scripts/fetch.py <url> 30000
   优点：无限制，效果和 Jina 相当，能读微信公众号
   适合：mp.weixin.qq.com、Substack、Medium 等反爬平台
 ↓
3. web_fetch 直接抓（静态页面兜底）
   web_fetch(url, maxChars=30000)
   适合：GitHub README、普通静态博客、技术文档
```

## 域名快捷路由

直接跳过 Jina，节省配额：
- `mp.weixin.qq.com` → 直接用 Scrapling
- `zhuanlan.zhihu.com`、`juejin.cn`、`csdn.net` → 优先 Scrapling

## 使用方式

### 自动模式（推荐）

直接告诉我要读取的 URL，我会自动选择合适的方案：

> 帮我读取这篇文章：https://example.com/article

### 手动指定方案

> 用 Scrapling 读取：https://mp.weixin.qq.com/s/xxx

## 安装依赖

```bash
pip install scrapling html2text --break-system-packages
```

## 脚本路径

`scripts/fetch.py` — Scrapling + html2text 提取脚本

调用方式：
```bash
python3 ~/.openclaw/workspace/skills/web-content-fetcher/scripts/fetch.py <url> [max_chars]
```

## 防死循环规则

同一个 URL 累计失败 2 次就放弃，记录为"无法提取"，不重复重试。
