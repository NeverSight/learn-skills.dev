---
name: article-drafts
description: 批量提交或获取 mixdao 文章初稿（文件路径入参、列表）。需 MIXDAO_API_KEY。触发：更新初稿、获取初稿列表、article-drafts。
---

# Article Drafts（文章初稿）

通过 mixdao API 获取或更新文章初稿。**仅支持批量提交**，以「文件路径」为入参：每条从路径读文件，**文件名（不含扩展名）** 作为标题，正文为文件内容，slug 由 title+content 自动计算。

## 脚本

| 脚本 | 作用 |
|------|------|
| `scripts/patch-draft.js` | 批量创建/更新初稿：入参为多个文件路径，从路径读正文、用文件名作 title 并提交。 |
| `scripts/list-drafts.js` | 获取初稿列表：GET /api/article-drafts（无参数为最新日期）；可传日期参数获取指定日期列表。 |

## 环境变量

| 变量 | 说明 |
|------|------|
| **MIXDAO_API_KEY** | 必填。mixdao API 的 Bearer token。 |

## 批量创建/更新初稿

```bash
node scripts/patch-draft.js [--date 2026-02-15] path/to/article1.md path/to/article2.md
```

- `--date`：可选，格式 YYYY-MM-DD；不传则当天（Asia/Shanghai）。
- 其余参数为文件路径。

## 获取初稿列表

**最新日期的初稿列表：**

```bash
node scripts/list-drafts.js
```

**指定日期的初稿列表：**

```bash
node scripts/list-drafts.js 2026-02-15
```

输出为 JSON，便于后续处理。
