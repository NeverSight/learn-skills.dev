---
name: linkfox-chuhaijiang-tiktok-product
description: 使用出海匠（Chuhaijiang）研究 TikTok Shop 公开商品市场，支持搜索、详情、关联达人/直播/视频/评论、热推榜/新品榜/销量榜和图片找同款。用户点名出海匠或 Chuhaijiang 时触发；未指定数据源时，仅对关联直播、图片找同款或跨达人/直播/视频/评论的组合钻取触发。通用 TikTok 商品榜单或选品使用 linkfox-kalodata-tiktok-product，按商品 URL/19 位 ID 查询当前公开详情使用 linkfox-tiktok-shop-product-detail，卖家后台商品操作使用 linkfox-tiktok-shop-product；点名其他数据源时不触发。
---

# TikTok Product Market Intelligence

Use this skill to research public TikTok Shop product markets: discover products, inspect one product, trace its creators/lives/videos/reviews, browse three rankings, or find visually similar products.

## Core Concepts

- Monetary fields are usually objects such as `{ "unit": "US", "value": 31 }`, but some ranking fields can be plain numbers. Inspect the runtime type before reading and preserve `unit` when an object is returned.
- Normal product endpoints require a lowercase marketplace code. Image search accepts an uppercase two-letter code and defaults to `US`.
- Search and relationship endpoints return at most 10 records per page; ranking endpoints return at most 20.
- Each endpoint call is billed independently. Do not repeat the same endpoint and parameters unless the user explicitly asks; successful responses use a 24-hour local cache keyed by endpoint, gateway, API Key fingerprint, and parameters.

## Data Fields

| Field | Meaning |
|---|---|
| `data.total_count` | Total matching records |
| `data.items` | Product or relationship records |
| `data.core.items` | Optional product core metrics when detail `include` contains `core` |
| `data.channel.items` | Optional channel-split sales metrics when detail `include` contains `channel` |
| `id` / `product_id` | Product or related-entity identifier |
| `product_name` | Product title |
| `floor_price` / `ceiling_price` | Current price range |
| `product_sold_count*` | Total or windowed sales |
| `product_gmv*` / `interval_gmv` | Total or windowed GMV |
| `product_rating` / `review_count` | Rating and review volume |
| `product_images` | Main and thumbnail images |
| `shop_name` / `seller_id` | Store identity |

Relationship responses use endpoint-specific prefixed fields. Read `references/api.md` for the complete request definitions, response paths, key fields, and production-validated structure. Do not assume one shared schema.

## Endpoints

| Intent | Endpoint | Script | Points/call |
|---|---|---|---:|
| Filter and discover products | `/chuhaijiang/products/search` | `chuhaijiang_product_search.py` | 18 |
| Inspect one product | `/chuhaijiang/products/detail` | `chuhaijiang_product_detail.py` | 9 |
| Find promoting creators | `/chuhaijiang/products/related-creators` | `chuhaijiang_product_related_creators.py` | 18 |
| Find associated livestreams | `/chuhaijiang/products/related-lives` | `chuhaijiang_product_related_lives.py` | 18 |
| Read product reviews | `/chuhaijiang/products/reviews` | `chuhaijiang_product_reviews.py` | 18 |
| Find promoting videos | `/chuhaijiang/products/related-videos` | `chuhaijiang_product_related_videos.py` | 18 |
| Browse most-promoted ranking | `/chuhaijiang/products/rankings/most-promoted` | `chuhaijiang_product_rank_most_promoted.py` | 18 |
| Browse new-arrival ranking | `/chuhaijiang/products/rankings/new-arrivals` | `chuhaijiang_product_rank_new_arrivals.py` | 18 |
| Browse top-selling ranking | `/chuhaijiang/products/rankings/top-selling` | `chuhaijiang_product_rank_top_selling.py` | 18 |
| Search by an uploaded image | `/chuhaijiang/products/image-search` | `chuhaijiang_product_image_search.py` | 30 |
| Upload helper for image search | `/chuhaijiang/upload/presigned-url` | `upload_image.py` | 0 |

Call only the endpoint required by the user's current question. Ask before making additional paid drill-down calls that the user did not request.

## Parameter Guide

- `country`: one of `br,de,es,fr,gb,id,it,jp,mx,my,ph,sg,th,us,vn` for normal endpoints.
- `id`: required for detail and relationship endpoints. Reuse a product `id` from search or ranking results.
- `page`: starts at 1. `pageSize` is optional.
- Search supports `keyword`, `category`, `sellerType`, price/rating/sales ranges, `freeShipping`, and `sort` (`field:asc` or `field:desc`).
- Most-promoted and top-selling rankings require `date` (`YYYYMMDD`) and `granularity` (`daily`, `weekly`, `monthly`, `0`, `1`, or `2`).
- New arrivals optionally supports `listedFrom`, `listedTo`, and `productStatus`.
- Use camelCase request names shown in `references/api.md`; do not send upstream snake_case names.

## 调用方式

- **API 端点**：11 个 LinkFox 网关能力均使用 POST；完整请求地址、参数、响应和错误码见 `references/api.md`。本地图搜还会向预签名返回的 `data.url` 发送一次不携带 LinkFox API Key 的外部 HTTP PUT。
- **Python 脚本**：`python scripts/<entry>.py '<JSON 参数>' [--inline]`
- **成本约束**：10 个商品业务入口脚本默认只缓存成功响应 24 小时，业务成功的空结果也可缓存；缓存按当前工作目录、调用身份、网关、端点和完整请求参数隔离。相同组合命中时输出 `Cache hit`，不会发起新的付费请求。HTTP 或业务失败不缓存；`--inline` 不绕过缓存；`--no-cache` 会强制真实请求并可能再次消耗算力，仅在用户明确同意额外消耗或调试时使用。上传预签名与 PUT 不使用响应缓存。

**输出策略（10 个商品业务脚本）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-chuhaijiang-tiktok-product-<timestamp>.json`；`<cwd>` 为脚本执行时的当前工作目录，当前目录不可写时退出报错，不回退到用户目录或系统临时目录。
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 输出请求参数、顶层状态、`data.total_count`、各业务列表长度和首个非空业务列表的前 3 条样本
- 加 `--inline` 强制全量打印到 stdout（同样落盘）
- `upload_image.py` 是上传辅助脚本：只输出安全元数据，不保存包含 `data.url` 或 `data.signed_url` 的预签名响应。

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 解决认证和算力问题
发生以下异常情况时，采用 references/onboarding.md 引导解决问题：

### 异常情况
- **未配置API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY`，也未配置 `LINKFOXAGENT_API_KEY`。
- **响应401或402状态码**
- **响应提示算力或余额不足**：消息含"算力余额不足/计费不足/余额不足/quota exceeded/insufficient balance/套餐到期/需充值/请充值"，或类似含义的内容。

## Image Search Workflow

For a local JPG, JPEG, or PNG, upload it first:

```bash
python scripts/upload_image.py /path/to/product.jpg
```

The helper calls the accelerated presign endpoint, uploads the bytes with HTTP PUT to the returned `url`, and prints only safe metadata such as `osKey`, `osBucket`, file metadata, upload status, and `requestId`. The returned `signed_url` is a temporary read URL, not an upload fallback, and must not be printed or persisted. Then call:

```bash
python scripts/chuhaijiang_product_image_search.py '{"osKey":"returned-key","country":"US"}'
```

If the user already provides a valid `osKey`, skip the upload step.

## Usage Examples

```bash
python scripts/chuhaijiang_product_search.py '{"country":"us","keyword":"beauty","minRating":4,"freeShipping":true,"pageSize":5}'
python scripts/chuhaijiang_product_detail.py '{"country":"us","id":"1732052189676081387"}'
python scripts/chuhaijiang_product_rank_top_selling.py '{"country":"us","date":"20260824","granularity":"daily","pageSize":10}'
python scripts/chuhaijiang_product_reviews.py '{"country":"us","id":"1732052189676081387","pageSize":10}'
```

## Display Rules

1. State the marketplace, total count, current page, filters, and ranking window used.
2. For product lists, show image, title, price range, sales/GMV window, rating, store, and product ID when available.
3. Keep response currency units; do not silently label `unit: US` as another currency.
4. For reviews, show rating, content, publish time, SKU specification, and media availability.
5. For creators, lives, and videos, display the relationship metrics returned by that endpoint and retain the related entity ID for optional drill-down.
6. Never expose API keys, signed upload URLs, or raw image bytes.

## Important Limitations

1. Data is real-time market intelligence and cannot be treated as the user's private TikTok Shop account data.
2. This skill does not manage orders, inventory, listings, fulfillment, affiliate invitations, or ad campaigns.
3. Do not invent unsupported filters or compensate by repeatedly calling other endpoints.
4. Search and rankings can change over time; report the request date/window with results.
5. Image search requires a valid uploaded object key; local paths cannot be passed directly to the image-search endpoint.

## User Expression & Scenario Quick Reference

**Applicable**:

- **商品发现与详情**：“用出海匠筛选美国 TikTok 美妆商品”，“用 Chuhaijiang 看这个商品详情”。
- **关联数据**：“用出海匠查哪些达人在带这个商品”，“找这个 TikTok 商品的关联直播”，“用出海匠看这个商品的评论”，“用出海匠查推广这个商品的视频”。
- **商品榜单**：“用出海匠看美国 TikTok 商品热推榜”，“用 Chuhaijiang 看美妆新品榜”，“用出海匠查 TikTok 商品销量榜”。
- **图片与组合钻取**：“用这张图找 TikTok 同款”，“同时分析这个商品的达人、直播、视频和评论”。

**Adjacent**: General TikTok product ranking or selection requests without a source should use `linkfox-kalodata-tiktok-product`. A public product URL or 19-digit product ID lookup should use `linkfox-tiktok-shop-product-detail`. Seller-side product operations should use `linkfox-tiktok-shop-product`. If the user asks for FastMoss, EchoTik, Kalodata, or another named source, use that source instead.

**Not applicable**: order handling, stock changes, listing publication, campaign creation, video downloading, or image generation/editing.

## 算力消耗规则

按端点分别计费：上传预签名 0 算力/次；商品详情 9 算力/次；商品搜索、关联达人、关联直播、商品评论、关联视频及商品榜单 18 算力/次；图片搜索 30 算力/次。

> 用户会因算力消耗而支付费用。高频调用或多端点钻取前，先说明预计调用次数与算力消耗。

**Feedback:** Use the Feedback API in `references/api.md` only when the user explicitly asks to submit feedback or explicitly authorizes submission after an issue is identified. Summarize and sanitize the content; never include API keys, signed URLs, phone numbers, raw user messages, or unrelated task context.

---
*For more high-quality, professional cross-border e-commerce skills, visit [LinkFox Skills](https://skill.linkfox.com/).*
