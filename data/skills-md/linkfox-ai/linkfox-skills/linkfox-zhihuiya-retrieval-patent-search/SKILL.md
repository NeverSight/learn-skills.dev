---
name: linkfox-zhihuiya-retrieval-patent-search
description: 通过 Analytics 检索式（如 TACD： 关键词）在智慧芽专利数据库中检索专利列表，返回专利ID、公开号及命中总数。当用户提到专利检索式检索、专利表达式搜索、Analytics检索式、TACD检索、专利关键词检索、检索式查专利、专利语义检索、patent expression search, patent query syntax, Analytics query, TACD search, PatSnap, 智慧芽专利检索时触发此技能。即使用户未明确提及"检索式"或"智慧芽"，只要用户希望用检索式/表达式语法在专利库中检索专利列表，也应触发此技能。
---

# Zhihuiya Patent Expression Search

This skill searches the Zhihuiya (PatSnap) patent database using an Analytics query expression (e.g. `TACD: virtual reality`), returning a list of matching patents with their patent IDs and publication numbers, plus the total hit count.

## Core Concepts

**Expression-based patent search** uses Zhihuiya's Analytics query syntax to retrieve patents matching a field-scoped boolean expression. Unlike image-based search, this is a text query against the full patent corpus.

**Query expression (`queryText`)** holds an Analytics expression. Common field-scoped syntax:

| Syntax | Scope |
|--------|-------|
| `TACD: <term>` | Title + Abstract + Claims + Description |
| `TAC: <term>` | Title + Abstract + Claims |
| `TA: <term>` | Title + Abstract |
| `AND` / `OR` / `NOT` | Boolean operators (combine terms/fields) |

> This skill returns a **list** of patents (`patentId` + `pn`). To retrieve detailed bibliographic data, full text, legal status, family, or images for a specific patent, feed the returned `patentId`/`pn` into the corresponding `linkfox-zhihuiya-bibliography` / `linkfox-zhihuiya-simple-bibliography` / `linkfox-zhihuiya-legal-status` / `linkfox-zhihuiya-patent-family` skills.

## Data Fields

Each `data[]` item (one matching patent):

| Field | Description |
|-------|-------------|
| patentId | Zhihuiya internal patent ID |
| pn | Publication (announcement) number |
| title | Patent title |
| apdt | Application date (integer, YYYYMMDD) |
| pbdt | Publication date (integer, YYYYMMDD) |
| apno | Application number |
| authority | Patent office / authority (e.g. `US`) |
| inventor | Inventor(s), pipe-separated |
| originalAssignee | Original applicant(s), pipe-separated |
| currentAssignee | Current assignee(s), pipe-separated |

Top-level fields:

| Field | Description |
|-------|-------------|
| data | 专利列表（每项含上表 10 个字段） |
| total | Number of records returned in this response |
| allRecordsCount | Total hits matching the query expression |
| costToken | Token cost for this query |
| columns | Render metadata (display hints, not data records) |
| type | Render style (e.g. `tableListWorkbenches`) |
| errcode | `200` on success |
| errmsg | `ok` on success |

> The top-level `columns` array is render metadata and may be longer than the real `data` list — do not treat it as data.

## 调用方式

- **API 端点**：`POST /zhihuiya/querySearchPatent`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/zhihuiya_query_search_patent.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗算力；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改检索式连续试探；需要继续检索或翻页时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-zhihuiya-retrieval-patent-search-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 解决认证和算力问题
发生以下异常情况时，采用 references/onboarding.md 引导解决问题：

### 异常情况
- **未配置API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY`，也未配置 `LINKFOXAGENT_API_KEY`。
- **响应401或402状态码**
- **响应提示算力或权限不足**：消息含"算力余额不足/计费不足/余额不足/quota exceeded/insufficient balance/No permission/API package quota/套餐到期/需充值/请充值"，或类似含义的内容。

## Parameter Guide

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| queryText | Yes | - | Analytics 检索式，最大 12000 字符 |
| limit | No | 10 | 返回专利个数，1–1000 |
| offset | No | 0 | 偏移量，0–19999；`limit + offset` ≤ 20000 |
| sort | No | - | 排序数组，元素 `{field, order}` |
| stemming | No | 0 | 截词检索：`1` 开启 / `0` 关闭，默认关闭 |
| collapseType | No | ALL | 去重方式：ALL / APNO / DOCDB / INPADOC / EXTEND |
| collapseBy | No | - | 去重排序字段：APD / PBD / AUTHORITY / SCORE |
| collapseOrder | No | - | 去重排序顺序：OLDEST / LATEST |
| collapseOrderAuthority | No | - | 受理局优先级数组（仅 `collapseBy=AUTHORITY` 时有效），按输入顺序保留对应专利 |

### Sort object

| `field` | Meaning |
|---------|---------|
| PBDT_YEARMONTHDAY | Publication date |
| APD_YEARMONTHDAY | Application date |
| ISD | Issue / grant date |
| SCORE | Query relevance |

`order`: `DESC` or `ASC`. Example: `[{"field":"SCORE","order":"DESC"}]`.

### Collapse (deduplication)

| `collapseType` | Description |
|----------------|-------------|
| ALL | No dedup |
| APNO | By application number |
| DOCDB | By simple family |
| INPADOC | By INPADOC family |
| EXTEND | By PatSnap extended family |

`collapseBy` selects which representative record to keep (APD/PBD/AUTHORITY/SCORE); `collapseOrder` picks OLDEST or LATEST.

## Usage Examples

**1. Basic expression search**
```
检索 TACD: virtual reality 的专利，返回 10 条
```
Action: `{"queryText": "TACD: virtual reality", "limit": 10}`

**2. Sort by relevance**
```
用检索式 TACD: drone AND camera 查专利，按相关性排序
```
Action: `{"queryText": "TACD: drone AND camera", "sort": [{"field": "SCORE", "order": "DESC"}]}`

**3. Paginate**
```
翻到第 2 页，每页 10 条
```
Action: `{"queryText": "TACD: virtual reality", "offset": 10, "limit": 10}`

**4. Dedup by DOCDB family**
```
检索 TACD: virtual reality，按简单同族去重，保留最新
```
Action: `{"queryText": "TACD: virtual reality", "collapseType": "DOCDB", "collapseBy": "APD", "collapseOrder": "LATEST"}`

## Display Rules

1. **Present results as a table**: show `pn`, `title`, `apdt`/`pbdt` (format as dates), `inventor`, `currentAssignee`, `authority` per item.
2. **Show totals**: always state `allRecordsCount` (total hits) and the current page range (`offset`–`offset+limit`).
3. **Default sort**: if the user does not specify a sort, actively inject `{"field": "SCORE", "order": "DESC"}` so results are relevance-ordered; respect any sort the user explicitly requests.
4. **Large result sets**: present a summary table first, note the total, and offer to expand specific patents.
5. **Expand via sibling skills**: to get full metadata for a patent, direct the user to `linkfox-zhihuiya-bibliography` / `linkfox-zhihuiya-simple-bibliography`; do not re-query this search skill for details.
6. **No fabrication**: only display fields actually present in the response; never invent titles, dates, or assignees not returned.

## Important Limitations

- **`queryText` is required** and must be a valid Analytics expression. Missing it returns `errcode 400`.
- **Paging ceiling**: `limit + offset` must be ≤ 20000; `limit` max 1000; `offset` max 19999.
- **List-only output**: this skill returns `patentId` + `pn` (and basic fields). Full bibliographic/full-text/legal data must be fetched via dedicated `linkfox-zhihuiya-*` skills.
- **No auto-retry on empty/error**: if the query returns no hits or an error, do not automatically swap keywords or rewrite the expression; confirm with the user first (each call costs credits).
- **Permission/quota**: a `501 "No permission or API package quota"` response means the current key lacks the query-search permission/quota. This is a permission/package issue (not merely low balance) and **cannot be resolved by recharging alone** — do not retry; surface it to the user to open/enable the query-search API package.

## User Expression & Scenario Quick Reference

**Applicable** — Find patents by query expression:

| User Says | Scenario |
|-----------|----------|
| "检索 TACD: virtual reality 的专利" | Basic expression search |
| "用检索式查虚拟现实相关专利" | Expression search |
| "检索式：TAC AND camera" | Boolean expression |
| "按公开日排序检索" | Sorted search |
| "按简单同族去重" | Deduplicated search |
| "翻到第 2 页" | Pagination |

**Not applicable** — Needs beyond expression search:

- Bibliographic detail of a known patent ID/number (use `linkfox-zhihuiya-bibliography`)
- Image-based patent search (use `linkfox-zhihuiya-patent-image-search`)
- Legal status / family / full-text / PDF (use dedicated `linkfox-zhihuiya-*` skills)

**Boundary judgment**: When the user already has a patent ID or publication number and wants its metadata → use the bibliography skill. When the user wants to **discover** patents matching a query expression → this skill.

## 算力消耗规则

按动态规则计费：消耗算力 = 3 × 返回data条数。每条为 1 条检索式检索专利结果

> **重要**：本技能的服务按倍数动态计算，返回条数越多消耗越大，必须提醒用户，由用户决定是否继续。优先用较小的 `limit` 验证检索式命中，确认后再决定是否扩大范围或翻页。

**Feedback:**

Auto-detect and report feedback via the Feedback API when any of the following apply:
1. The functionality or purpose described in this skill does not match actual behavior
2. The skill's results do not match the user's intent
3. The user expresses dissatisfaction or praise about this skill
4. Anything you believe could be improved

Call the feedback API as specified in `references/api.md`. Do not interrupt the user's flow.

---
*For more high-quality, professional cross-border e-commerce skills, visit [LinkFox Skills](https://skill.linkfox.com/).*
