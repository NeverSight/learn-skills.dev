---
name: linkfox-chuhaijiang-tiktok-ads
description: 使用出海匠（Chuhaijiang）研究 TikTok 公开广告与创意素材，支持广告搜索、广告详情与关联商品，以及创意搜索、详情、脚本分镜分析和向量数据。用户点名出海匠或 Chuhaijiang 时触发；未指定数据源时，仅在需要广告到商品关系、创意结构拆解、AIGC/赞助/带货素材筛选时触发。通用 TikTok 带货视频榜单或详情使用 linkfox-kalodata-tiktok-video，广告账户与投放管理使用对应的 TikTok Ads 管理工具；点名其他数据源时不触发。
---

# TikTok Ad & Creative Intelligence

Use this skill to discover public TikTok ads and creative assets, inspect one result, connect an ad to promoted products, or analyze a creative's content structure.

## Core Concepts

- This is public-market intelligence, not the user's private TikTok Ads account or campaign manager.
- All five endpoints require a lowercase marketplace code: `br,de,es,fr,gb,id,it,jp,mx,my,ph,sg,th,us,vn`.
- Search and related-product endpoints return at most 10 records per page.
- Use the top-level item `id` returned by ad search with ad detail/related-products, and the `id` returned by creative search with creative detail. Do not substitute `video_id`, `product_id`, or `advertiser_id`.
- Ad detail accepts optional `include=core`. Creative detail accepts `include=analysis`, `include=embedding`, or both as a comma-separated string.
- Monetary metrics are commonly objects such as `{ "unit": "US", "value": 31 }`. Preserve both fields and inspect runtime types before calculating.
- Each endpoint is billed independently. Do not make an unrequested detail or relationship call after search, and do not repeat a failed/empty search with altered filters without user approval.

## Data Fields

| Path or field | Meaning |
|---|---|
| `data.total_count` | Total records matched by the endpoint |
| `data.items` | Primary ad, creative, or related-product records |
| `data.core.items` | Optional ad performance metrics requested with `include=core` |
| `data.analysis.items` | Optional creative hook/formula/angle, transcript, and storyboard analysis |
| `data.embedding.items` | Optional extracted content, matched tags, and embedding vector |
| `id` | Endpoint lookup ID for the matching detail/relationship calls |
| `ad_title`, `advertiser_name`, `ad_url`, `web_url` | Ad identity and public links |
| `video_play_count`, `video_like_count`, `video_engagement_rate` | Creative reach and engagement |
| `total_gmv`, `video_30d_gmv`, `video_total_gmv` | Returned commerce metrics; usually unit/value objects |
| `product_id`, `product_name` / `product_title` | Promoted product identity and title |

Read `references/api.md` before calling. It contains the complete camelCase request fields and production-validated response paths for each endpoint.

## Endpoints

| Intent | Endpoint | Script | Points/call |
|---|---|---|---:|
| Filter and discover ads | `/chuhaijiang/ad-creative/ads/search` | `chuhaijiang_ad_search.py` | 18 |
| Inspect one ad | `/chuhaijiang/ad-creative/ads/detail` | `chuhaijiang_ad_detail.py` | 9 |
| Find products promoted by an ad | `/chuhaijiang/ad-creative/ads/related-products` | `chuhaijiang_ad_related_products.py` | 18 |
| Filter and discover creative assets | `/chuhaijiang/ad-creative/creatives/search` | `chuhaijiang_creative_search.py` | 18 |
| Inspect and analyze one creative | `/chuhaijiang/ad-creative/creatives/detail` | `chuhaijiang_creative_detail.py` | 9 |

Call only the endpoint required by the user's current question. Search first only when the user has not already supplied a valid entity ID.

## Parameter Guide

- `country`: required lowercase marketplace code.
- `page`: optional, starts at 1. `pageSize`: optional, maximum 10 on search and related-products.
- Ad search supports `keyword`, `category`, `adType`, `excludeSparkAds`, view/GMV/day ranges, and `sort` (`field:asc` or `field:desc`).
- Ad detail requires `id`; request `include=core` only when performance metrics are needed.
- Related products requires the ad `id` and supports pagination.
- Creative search supports `keyword`, `category`, `hasProduct`, `isSponsored`, `isAigc`, and `sort`.
- Creative detail requires the creative `id`. Use `analysis` for content-structure fields and `embedding` only when extracted content, tags, or vector data are needed.
- Use camelCase request names shown in `references/api.md`; do not send upstream snake_case names.

## 调用方式

- **API 端点**：5 个 LinkFox 网关能力均使用 POST；完整请求地址、参数、响应和错误码见 `references/api.md`。
- **Python 脚本**：`python scripts/<entry>.py '<JSON 参数>' [--inline]`
- **成本约束**：业务入口脚本默认只缓存成功响应 24 小时，业务成功的空结果也可缓存；缓存按当前工作目录、调用身份、网关、端点和完整请求参数隔离。相同组合命中时输出 `Cache hit`，不会发起新的付费请求。HTTP 或业务失败不缓存；`--inline` 不绕过缓存；`--no-cache` 会强制真实请求并可能再次消耗算力，仅在用户明确同意额外消耗或调试时使用。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-chuhaijiang-tiktok-ads-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数、主业务列表长度和前 3 条样本；优先 `data.items` / 业务 `*.items`，跳过 embedding/vector）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq` 或 `ConvertFrom-Json` 从保存的 JSON 文件按需抽取，避免整份 JSON 进入上下文。

## 解决认证和算力问题

发生以下异常情况时，采用 `references/onboarding.md` 引导解决问题：

- `LINKFOX_AGENT_API_KEY` 与 `LINKFOXAGENT_API_KEY` 均未配置。
- 网关返回 401 或 402。
- 响应提示算力、余额、quota、套餐到期或充值问题。

## Usage Examples

```bash
python scripts/chuhaijiang_ad_search.py '{"country":"us","keyword":"beauty","page":1,"pageSize":3}'
python scripts/chuhaijiang_ad_detail.py '{"country":"us","id":"7658119807128046879","include":"core"}'
python scripts/chuhaijiang_ad_related_products.py '{"country":"us","id":"7658119807128046879","page":1,"pageSize":3}'
python scripts/chuhaijiang_creative_search.py '{"country":"us","hasProduct":true,"page":1,"pageSize":3}'
python scripts/chuhaijiang_creative_detail.py '{"country":"us","id":"7668708053428047118","include":"analysis,embedding"}'
```

The IDs above were valid during release validation but may age. In user workflows, prefer IDs from the current search response.

## Display Rules

1. State the marketplace, filters, current page, and `data.total_count` for searches.
2. For ads, show title, advertiser, public links, duration, active-day count, views/engagement, GMV/ROAS, product title, and the lookup `id` when available.
3. For related products, show product title/images, price range, rating, commission, total and 30-day sales/GMV, status, and product ID.
4. For creatives, show description, author, launch date, duration, views/likes/comments/shares/saves, engagement, product relationship, GMV/GPM, AIGC flag, and lookup `id` when available.
5. When `analysis` is requested, summarize the hook, formula, angle, structured transcript, and storyboards; do not dump a raw embedding vector into chat.
6. Preserve returned units, public URLs, identifiers, booleans, nulls, and unknown fields. Never expose API keys or cache-key fingerprints.

## Important Limitations

1. Data describes public market ads and creative assets; it is not private spend, attribution, audience, pixel, campaign, or account data.
2. This skill cannot create, edit, launch, pause, or optimize ad campaigns and cannot change budgets or bids.
3. `adType` and `category` values are upstream classifications; do not invent enum labels when the user has not supplied a known value.
4. Results and performance metrics change over time. Report the request date and filters with any analysis.
5. Embeddings are machine-oriented vectors. Retrieve them only for an explicit downstream similarity/ML need.

## User Expression & Scenario Quick Reference

**Applicable**:

- **广告发现与商品关系**：“用出海匠找美国 TikTok 美妆广告”，“看看这个广告详情和它关联的商品”。
- **创意筛选**：“筛 TikTok 带货素材”，“找 AIGC 创意”，“看赞助内容素材”。
- **结构拆解**：“用 Chuhaijiang 拆这个创意的 hook、脚本和分镜”，“取素材标签或 embedding 做相似度分析”。

**Adjacent**: TikTok 商品研究 belongs to `linkfox-chuhaijiang-tiktok-product`; public video search/detail without an ad-creative requirement belongs to `linkfox-chuhaijiang-tiktok-video` or `linkfox-kalodata-tiktok-video`; campaign/account operations belong to a TikTok Ads management integration.

**Not applicable**: campaign creation, budget/bid changes, audience targeting, pixel/events setup, private-account reporting, media downloading, or image/video generation.

## 算力消耗规则

按端点分别计费：广告详情和创意详情 9 算力/次；广告搜索、广告关联商品和创意搜索 18 算力/次。

> 用户会因算力消耗而支付费用。高频调用或多端点钻取前，先说明预计调用次数与算力消耗。

**Feedback:** Use the Feedback API in `references/api.md` only when the user explicitly asks to submit feedback or explicitly authorizes submission after an issue is identified. Summarize and sanitize the content; never include API keys, raw user messages, or unrelated task context.

---
*For more high-quality, professional cross-border e-commerce skills, visit [LinkFox Skills](https://skill.linkfox.com/).*
