---
name: linkfox-chuhaijiang-tiktok-shop
description: 使用出海匠（Chuhaijiang）研究 TikTok Shop 公开店铺市场，支持店铺搜索、详情、关联达人/商品/视频、热推榜和销量榜。用户点名出海匠或 Chuhaijiang 且意图涉及店铺搜索、详情、店铺关系或店铺榜单时触发；未指定数据源时，仅在需要按店铺评分、7日销量/GMV筛选，或查看店铺关联达人/商品/视频时触发。通用 TikTok 店铺榜单或详情使用 linkfox-kalodata-tiktok-shop，EchoTik 店铺搜索/详情使用相应 EchoTik skills；卖家后台订单、商品、履约等操作使用 TikTok Shop 官方 skills；点名其他数据源时不触发。
---

# TikTok Shop Store Intelligence

Use this skill to research public TikTok Shop stores: discover and filter stores, inspect one store, trace its creators/products/videos, or browse most-promoted and top-selling store rankings.

## Core Concepts

- Normal endpoints require one lowercase marketplace code: `br,de,es,fr,gb,id,it,jp,mx,my,ph,sg,th,us,vn`.
- Search and relationship endpoints return at most 10 records per page; ranking endpoints accept 1–20.
- Store detail may return `data.items`, `data.core.items`, and `data.channel.items`. When `include=core,channel`, read all three branches.
- Monetary fields are usually `{ "unit": "US", "value": 31 }`. Preserve the returned unit and inspect the runtime type before formatting.
- Each endpoint call is billed independently. Call only the endpoint needed for the current question; successful calls use a 24-hour local cache keyed by endpoint, gateway, API Key fingerprint, and parameters.

## Data Fields

| Field | Meaning |
|---|---|
| `data.total_count` | Total matching records |
| `data.items` | Store, creator, product, video, or ranking rows |
| `data.core.items` | Optional store scale and 30-day core metrics |
| `data.channel.items` | Optional 30-day video/live/product-card/creator channel metrics |
| `id` / `seller_id` | Store or related-entity identifier |
| `shop_name` / `region` | Store identity and marketplace |
| `shop_rating` | Store rating |
| `shop_product_count` | Current product count when supplied |
| `shop_total_sold_count` / `shop_total_gmv` | Lifetime sales and GMV when supplied |
| `shop_sold_count_for_last_7_days` / `shop_gmv_for_last_7_days` | Recent store performance |
| `interval_*` | Metrics for the requested ranking window |

Relationship rows use endpoint-specific `tiktok_seller_*` fields. Read `references/api.md` for the exact request definitions, production-validated response paths, and observed field catalog. Do not assume one shared row schema.

## Endpoints

| Intent | Endpoint | Script | Points/call |
|---|---|---|---:|
| Filter and discover stores | `/chuhaijiang/sellers/search` | `chuhaijiang_seller_search.py` | 18 |
| Inspect one store | `/chuhaijiang/sellers/detail` | `chuhaijiang_seller_detail.py` | 9 |
| Find associated creators | `/chuhaijiang/sellers/related-creators` | `chuhaijiang_seller_related_creators.py` | 18 |
| List store products | `/chuhaijiang/sellers/related-products` | `chuhaijiang_seller_related_products.py` | 18 |
| Find associated videos | `/chuhaijiang/sellers/related-videos` | `chuhaijiang_seller_related_videos.py` | 18 |
| Browse most-promoted stores | `/chuhaijiang/sellers/rankings/most-promoted` | `chuhaijiang_seller_rank_most_promoted.py` | 18 |
| Browse top-selling stores | `/chuhaijiang/sellers/rankings/top-selling` | `chuhaijiang_seller_rank_top_selling.py` | 18 |

Route one intent to one endpoint. Use a store `id` from search or ranking results for detail and relationship calls. Ask before making additional paid drill-down calls the user did not request.

## Parameter Guide

- `country`: required lowercase marketplace code.
- `id`: required for detail and relationship endpoints; send it as a string to preserve precision.
- `page`: starts at 1. `pageSize` is optional and must not exceed the endpoint limit.
- Search accepts `keyword`, `category`, `sellerType`, rating/7-day sales/7-day GMV ranges, and `sort` (`field:asc` or `field:desc`).
- Detail accepts `include=core`, `include=channel`, or both values in either comma-separated order (`core,channel` / `channel,core`).
- Both rankings require `date` (`YYYYMMDD`) and `granularity` (`daily`, `weekly`, `monthly`, `0`, `1`, or `2`); optional `shopType` is one of `1,2,3,4`.
- Use the camelCase request names in `references/api.md`; do not send the upstream snake_case aliases.

## 调用方式

- **API 端点**：`POST /chuhaijiang/sellers/search`、`POST /chuhaijiang/sellers/detail`、`POST /chuhaijiang/sellers/related-creators`、`POST /chuhaijiang/sellers/related-products`、`POST /chuhaijiang/sellers/related-videos`、`POST /chuhaijiang/sellers/rankings/most-promoted`、`POST /chuhaijiang/sellers/rankings/top-selling`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：分别使用 `python scripts/chuhaijiang_seller_search.py '<JSON 参数>' [--inline]`、`chuhaijiang_seller_detail.py`、`chuhaijiang_seller_related_creators.py`、`chuhaijiang_seller_related_products.py`、`chuhaijiang_seller_related_videos.py`、`chuhaijiang_seller_rank_most_promoted.py`、`chuhaijiang_seller_rank_top_selling.py`
- **成本约束**：店铺详情 9 算力/次；其余六个端点 18 算力/次。业务入口脚本默认只缓存成功响应 24 小时，业务成功的空结果也可缓存；缓存按当前工作目录、调用身份、网关、端点和完整请求参数隔离。相同组合命中时输出 `Cache hit`，不会发起新的付费请求。HTTP 或业务失败不缓存；`--inline` 不绕过缓存；`--no-cache` 会强制真实请求并可能再次消耗算力，仅在用户明确同意额外消耗或调试时使用。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-chuhaijiang-tiktok-shop-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、业务总数、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

On Windows hosts whose Python stdout still uses GBK, set `PYTHONIOENCODING=utf-8` before printing rows that may contain emoji. This affects console rendering only; the UTF-8 JSON file is already saved first.

## 解决认证和算力问题

发生以下异常情况时，采用 `references/onboarding.md` 引导解决问题：

### 异常情况

- **未配置API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY`，也未配置 `LINKFOXAGENT_API_KEY`。
- **响应401或402状态码**
- **响应提示算力或余额不足**：消息含“算力余额不足/计费不足/余额不足/quota exceeded/insufficient balance/套餐到期/需充值/请充值”，或类似含义的内容。

## Usage Examples

```bash
python scripts/chuhaijiang_seller_search.py '{"country":"us","keyword":"beauty","minRating":4,"page":1,"pageSize":3,"sort":"gmv_7d:desc"}'
python scripts/chuhaijiang_seller_detail.py '{"country":"us","id":"7495205878591949358","include":"core,channel"}'
python scripts/chuhaijiang_seller_related_creators.py '{"country":"us","id":"7495205878591949358","page":1,"pageSize":10}'
python scripts/chuhaijiang_seller_related_products.py '{"country":"us","id":"7495205878591949358","page":1,"pageSize":10}'
python scripts/chuhaijiang_seller_related_videos.py '{"country":"us","id":"7495205878591949358","page":1,"pageSize":10}'
python scripts/chuhaijiang_seller_rank_most_promoted.py '{"country":"us","date":"20260824","granularity":"daily","pageSize":10}'
python scripts/chuhaijiang_seller_rank_top_selling.py '{"country":"us","date":"20260824","granularity":"daily","pageSize":10}'
```

## Display Rules

1. State the marketplace, filters, current page, total count, and ranking date/granularity used.
2. For store lists, show store name, rating, product count, recent or interval sales/GMV, creator reach, region, and store ID when available.
3. For detail, group base profile, core metrics, and channel metrics; do not ignore `data.core.items` or `data.channel.items`.
4. For creators, products, and videos, show the related entity ID plus its returned performance metrics; retain the store ID for context.
5. Preserve currency units and field time windows. Do not relabel `unit: US` or mix lifetime, 7-day, 30-day, and ranking-window values.
6. Never expose API keys. Treat URLs as expiring when the response contains signed query parameters.

## Important Limitations

1. This is public market intelligence, not private seller-center data.
2. It does not manage orders, inventory, listings, fulfillment, affiliates, advertising, or store authorization.
3. Some fields may be absent or `null`; preserve unknown fields and inspect runtime types before rendering.
4. Search and rankings change over time. Report the request date and ranking window with results.
5. `sellerType` belongs to search, while `shopType` belongs to rankings. Do not interchange them.
6. Do not invent unsupported filters or compensate by repeatedly calling other paid endpoints.

## User Expression & Scenario Quick Reference

**Applicable**:

- **店铺发现与详情**：“用出海匠筛选美国 TikTok 美妆店铺”，“用 Chuhaijiang 看这家店详情”。
- **关系钻取**：“查这家 TikTok 店合作的达人”，“看店内商品”，“找这家店的带货视频”。
- **店铺榜单**：“用出海匠看美国 TikTok 店铺热推榜”，“用 Chuhaijiang 查 TikTok 店铺销量榜”。
- **组合分析**：“先筛 7 日 GMV 高的店，再分析其达人、商品和视频”。

**Adjacent**: General TikTok store ranking or detail requests without a source should use `linkfox-kalodata-tiktok-shop`. Use the EchoTik seller skills when the user asks for EchoTik fields or multi-period seller profiles. Use official TikTok Shop skills for the user's authorized seller-center operations.

**Not applicable**: order handling, stock or listing changes, fulfillment, store authorization, ad campaign changes, non-TikTok marketplaces, or a request naming another data provider.

## 算力消耗规则

按端点分别计费：店铺详情 9 算力/次；店铺搜索、关联达人、关联商品、关联视频及两类榜单 18 算力/次。

> 用户会因算力消耗而支付费用。高频调用或多端点钻取前，先说明预计调用次数与算力消耗。

**Feedback:** Use the Feedback API in `references/api.md` only when the user explicitly asks to submit feedback or explicitly authorizes submission after an issue is identified. Summarize and sanitize the content; never include API keys, phone numbers, raw user messages, or unrelated task context.

---
*For more high-quality, professional cross-border e-commerce skills, visit [LinkFox Skills](https://skill.linkfox.com/).*
