---
name: linkfox-damai-mercado-market-intelligence
description: 大麦数据 Mercado Libre（美客多）市场洞察与选品查询，通过 LinkFox 网关查询类目、行业规模、商品与属性聚合、商品销量趋势、相似图片商品和评论，覆盖墨西哥、巴西、阿根廷、智利、哥伦比亚站点。当用户提到大麦数据、大麦 MCP、美客多选品、Mercado Libre 市场调研、类目分析、竞品销量、商品搜索、图搜商品或评论分析时触发此技能。
---

# Damai Mercado Libre Market Intelligence

This skill researches Mercado Libre markets through one LinkFox gateway endpoint. It selects the appropriate operation, validates snake_case arguments, and presents category, industry, product, trend, image-search, or review data.

## Core Concepts

- Call only `${LINKFOX_TOOL_GATEWAY}/damai/call`. Never call the upstream data provider directly or ask the user for an upstream `X-API-Key`.
- Send `{"toolName":"...","arguments":{...}}`; preserve documented snake_case field names exactly.
- Treat `search_categories` and `get_my_quota_status` as free operations. Each successful call to one of the other five operations costs 12 LinkFox points (￥0.12) and consumes one upstream plan request when an active plan exists, or one upstream point when the account is in points billing mode. Plan expiry or exhaustion does not automatically fall back to points; inspect quota status instead of guessing the billing mode.
- Read `data` first. Use `contentText` only when `data` is textual or ambiguous; do not show `rawResponse` unless diagnostics are requested.
- Read `references/api.md` before constructing uncommon filters or interpreting provider-specific fields.

## Data Fields

| Operation | Main output |
|---|---|
| Category search | Category IDs, localized paths, level, 30-day orders/GMV, price, merchant and listing counts |
| Industry overview | Monthly order/price/GMV trends and category summary metrics |
| Product search | Products, prices, 30/60/90-day and lifetime sales, seller/category data, fulfillment, inventory, attribute aggregation |
| Sales trend | Monthly and ISO-week order series with coverage metadata |
| Image search | Similar Mercado Libre product IDs and provider status |
| Review search | Review text, rating, date, product and buyer fields |

## Parameter Guide

- Markets: `MLM` Mexico, `MLB` Brazil, `MLA` Argentina, `MLC` Chile, `MCO` Colombia. Default is `MLM` when omitted.
- Category keywords and product keywords must use the selected market's local language.
- Resolve a category name with free `search_categories` before using paid category analysis.
- `search_product_snapshots` requires at least one of `keyword`, `category_id`, `sku_id`, `shop_id`, `shop_query`, or `product_url`.
- `image_search_products` requires `image_url` or `image_base64`. For a local image, run `python scripts/upload_image.py <path>` and use the returned public URL.
- `product_sales_trend.days` accepts 1-731. `review_search.limit` and product-search `limit` accept at most 100.
- Product listing dates accept `YYYYMMDD` or `YYYY-MM-DD`. Product sort fields are `sales_30d`, `historical_total_sales`, `price`, `listing_date`, `rating`, `review_count`, or `title`.
- `product_status` accepts a string such as `active`/`paused` or an upstream integer status value.
- Do not pass `uId`, `uid`, `memberId`, undocumented camelCase aliases, or unknown fields.

## 调用方式

- **API 端点**：`POST /damai/call`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/damai_mercado_market_intelligence.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗算力；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-damai-mercado-market-intelligence-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 解决认证和算力问题
发生以下异常情况时，采用 references/onboarding.md 引导解决问题：

### 异常情况
- **未配置API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY`，也未配置 `LINKFOXAGENT_API_KEY`。
- **响应401或402状态码**
- **响应提示算力或余额不足**：消息含"算力余额不足/计费不足/余额不足/quota exceeded/insufficient balance/套餐到期/需充值/请充值"，或类似含义的内容。

## Local Image Upload

`image_search_products` requires a public image URL or Base64 content. When the user provides a local image, run `python scripts/upload_image.py <path>` first. The helper requests `${LINKFOX_TOOL_GATEWAY}/oss/file/presignedPut`, uploads the file with the returned presigned PUT URL, and prints a public URL valid for 24 hours. Pass that URL as `arguments.image_url`; never place the presigned query string or image Base64 in user-visible output.

## Usage Examples

```bash
# Free category lookup
python scripts/damai_mercado_market_intelligence.py '{"toolName":"search_categories","arguments":{"market_code":"MLM","query":"celulares","limit":10}}'

# Product opportunity search
python scripts/damai_mercado_market_intelligence.py '{"toolName":"search_product_snapshots","arguments":{"market_code":"MLM","category_id":"MLM1055","sort_by":"sales_30d","sort_order":"desc","page":1,"limit":20}}'

# Product sales trend
python scripts/damai_mercado_market_intelligence.py '{"toolName":"product_sales_trend","arguments":{"market_code":"MLM","sku_id":"MLM1602785195","days":90}}'
```

## Display Rules

1. Present only fields supported by the response; do not invent demand, profit, or competition conclusions.
2. State the market, filters, time coverage, record count, currency, and pagination when available.
3. For category results, show the full localized path and whether the category is terminal.
4. For product results, prioritize product ID/title, price, 30-day orders, lifetime orders, rating/reviews, seller, category, listing date, fulfillment, and inventory.
5. For trends, distinguish requested days from covered days and surface incomplete-coverage notices.
6. Image search returns product IDs; explain that fetching full product records requires another potentially paid operation.
7. Preserve review language and label translations only when the upstream response provides them.

## Important Limitations

- Provider data can be delayed or incomplete; `data_available=false`, empty records, and coverage notices are valid business results.
- Product-search `product_status`, image-search `token`, and some fulfillment values are provider-defined; do not invent undocumented enums.
- A successful paid operation may consume upstream quota even when no matching business records are found.
- Do not retry paid operations automatically after timeout, 5xx, or an ambiguous connection failure.
- Do not expose LinkFox keys, upstream credentials, full Base64 images, or provider account identifiers.

## 错误处理

| 场景 | 处理 |
|---|---|
| 参数错误或 `errcode=1002` | 按 `references/api.md` 修正；如需改变用户筛选意图，先询问用户 |
| HTTP 401/402 或 LinkFox 算力不足 | 使用 `references/onboarding.md` 引导并停止调用 |
| HTTP 403 或 `errcode=1005` | 提示联系后端检查路由和托管密钥；不得要求用户提供上游密钥 |
| 大麦上游套餐、算力或额度异常 | 最多调用一次免费的 `get_my_quota_status` 辅助说明，然后停止收费调用 |
| HTTP 429/5xx、`errcode=1003` 或超时 | 不自动重试；说明结果不确定，用户明确同意后再调用 |
| 成功但无数据 | 如实展示空结果和筛选条件，不自动换词、翻页或换市场 |
| 本地图片上传失败 | 不调用收费图搜，先修正图片输入或上传问题 |

判断结果时同时检查 HTTP 状态、`code` / `errcode`、`error` / `errmsg` 和业务 `data`；不要只依赖脚本退出码，也不要自动重试收费操作。

## User Expression & Scenario Quick Reference

**Applicable** -- Mercado Libre category, market, product, trend, image-similarity, and review research:

| User says | Action |
|---|---|
| "找墨西哥手机类目" / "美客多类目 ID" | Use `search_categories` |
| "这个类目市场规模和趋势" | Resolve category, then use `industry_overview` |
| "筛选月销高的美客多商品" / "查这个 SKU" | Use `search_product_snapshots` |
| "这个商品最近销量走势" | Use `product_sales_trend` |
| "用这张图找美客多同款" | Use `image_search_products` |
| "分析这个商品的评论" | Use `review_search` |

**Not applicable** -- Store authorization, listing publication, inventory updates, order fulfillment, refunds, advertising operations, or other Mercado Libre official seller APIs.

**Boundary judgment:** Use this skill when the user needs market or product intelligence from the documented data operations. Do not use it for seller-account mutations, official commerce workflows, or unsupported predictive conclusions.

## 算力消耗规则

- `search_categories`、`get_my_quota_status` 免费，不扣 LinkFox 算力。
- `industry_overview`、`search_product_snapshots`、`product_sales_trend`、`image_search_products`、`review_search` 每次成功调用收取 **12 LinkFox 算力（￥0.12）**。

> 用户会因收费操作支付算力。需要连续调用多个收费操作、高频查询或翻页时，先说明预计调用次数与算力消耗，由用户决定是否继续。

## Feedback

Auto-detect and report feedback through the Feedback API in `references/api.md` when the skill behavior, documentation, or result presentation mismatches the user's intent, or when the user expresses praise or dissatisfaction. Never include credentials, private data, Base64 images, or complete large responses.

---
*For more high-quality, professional cross-border e-commerce skills, visit [LinkFox Skills](https://skill.linkfox.com/).*
