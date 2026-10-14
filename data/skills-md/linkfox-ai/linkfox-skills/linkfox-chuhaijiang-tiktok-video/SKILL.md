---
name: linkfox-chuhaijiang-tiktok-video
description: 使用出海匠（Chuhaijiang）研究 TikTok 公开视频，支持多条件视频搜索、单视频详情、带货商品和评论钻取。用户点名出海匠或 Chuhaijiang 时触发；未指定数据源时，仅在需要视频评论或视频到带货商品的关系钻取时触发。通用 TikTok 带货视频榜单或详情使用 linkfox-kalodata-tiktok-video，视频上传发布使用 linkfox-tiktok-video；点名其他数据源时不触发。
---

# TikTok Video Market Intelligence

Use this skill to research public TikTok videos: discover videos with market filters, inspect one video's performance, identify products promoted by a shoppable video, or read its public comments.

## Core Concepts

- This is a read-only public-market research skill. It does not upload, publish, edit, or delete TikTok videos.
- Search returns `data.items[]` plus `data.total_count`. Reuse an item's `id` for detail, product, or review drill-downs.
- Detail returns the main profile in `data.items[]`; `include=core` additionally returns normalized performance metrics in `data.core.items[]`.
- Related-product and review rows use endpoint-specific prefixed fields. Read `references/api.md` before interpreting them.
- Money-like values can be objects such as `{ "unit": "US", "value": 402056 }`. Preserve the returned unit and value; do not treat them as plain numbers or silently convert currency.
- Always preserve the returned `country_code`. Do not relabel a row solely from the requested marketplace.

## Data Fields

| Field | Meaning |
|---|---|
| `id` | Video, product, or comment identifier for the current endpoint |
| `video_desc` | Video caption or description |
| `share_url` | Public TikTok URL |
| `author_id` / `author_unique_id` | Creator identifiers |
| `video_play_count` / `video_like_count` | Lifetime plays and likes |
| `video_comment_count` / `video_share_count` / `video_collect_count` | Engagement counts |
| `video_engagement_rate` | Returned decimal engagement rate; format as a percentage only when clearly labeled |
| `video_30d_gpm` | 30-day GMV per thousand views; not a percentage |
| `data.core.items[]` | Optional normalized core metrics from detail `include=core` |
| `tiktok_video_detail_product_*` | Product and video-commerce fields from related products |
| `tiktok_video_detail_comment_*` | Comment identity, text, author, likes, replies, and timestamp |

## Endpoints

| User goal | Endpoint | Script |
|---|---|---|
| Search public videos | `/chuhaijiang/videos/search` | `chuhaijiang_video_search.py` |
| Inspect one video | `/chuhaijiang/videos/detail` | `chuhaijiang_video_detail.py` |
| Find products promoted by a video | `/chuhaijiang/videos/related-products` | `chuhaijiang_video_related_products.py` |
| Read video comments | `/chuhaijiang/videos/reviews` | `chuhaijiang_video_reviews.py` |

Call only the endpoint required by the user's current question. A normal video can legitimately return an empty related-product list; do not replace it with another video without user approval.

## Parameter Guide

- `country`: lowercase request context/site code: `br,de,es,fr,gb,id,it,jp,mx,my,ph,sg,th,us,vn`. The row-level `country_code` can differ from the request value, so preserve both.
- `page`: starts at 1. `pageSize` controls the returned page size and must not exceed 10.
- `id`: required for detail, related products, and reviews. Pass it as a JSON string to preserve 19-digit identifiers.
- `include`: detail-only optional string. Use `core` only when normalized core performance metrics are needed.
- Search supports `keyword`, `category`, `isCommercial`, play/like/30-day-GMV/engagement ranges, `accountType` (`0`, `3`, or `4`), and `sort` (`field:asc|desc`, default `views:desc`). Use the camelCase gateway names in `references/api.md`; do not send the upstream snake_case aliases.

## 调用方式

- **API 端点**：`POST /chuhaijiang/videos/search`、`POST /chuhaijiang/videos/detail`、`POST /chuhaijiang/videos/related-products` 或 `POST /chuhaijiang/videos/reviews`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/chuhaijiang_video_<entry>.py '<JSON 参数>' [--inline]`，其中 `<entry>` 为 `search`、`detail`、`related_products` 或 `reviews`
- **成本约束**：业务入口脚本默认只缓存成功响应 24 小时，业务成功的空结果也可缓存；缓存按当前工作目录、调用身份、网关、端点和完整请求参数隔离。相同组合命中时输出 `Cache hit`，不会发起新的付费请求。HTTP 或业务失败不缓存；`--inline` 不绕过缓存；`--no-cache` 会强制真实请求并可能再次消耗算力，仅在用户明确同意额外消耗或调试时使用。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-chuhaijiang-tiktok-video-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、业务总数、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq` 或 `ConvertFrom-Json` 从保存的 JSON 文件按需抽取，避免整份 JSON 进入上下文。

## 解决认证和算力问题

网关返回认证或余额错误时，读取 `references/onboarding.md`，按其中的 auth/billing 分流使用 `scripts/onboarding.py`。不要把 API Key、验证码、支付链接或原始用户消息写入反馈。

## Usage Examples

```bash
python scripts/chuhaijiang_video_search.py '{"country":"us","keyword":"beauty","isCommercial":true,"sort":"views:desc","page":1,"pageSize":3}'
python scripts/chuhaijiang_video_detail.py '{"country":"us","id":"6788833646091504902","include":"core"}'
python scripts/chuhaijiang_video_related_products.py '{"country":"us","id":"7672655263672864013","page":1,"pageSize":3}'
python scripts/chuhaijiang_video_reviews.py '{"country":"us","id":"6788833646091504902","page":1,"pageSize":3}'
```

These examples were production-validated with non-empty semantic results. IDs are volatile public-market examples; use a fresh search result when they stop resolving.

## Display Rules

1. State request context/site code, filters, sort, page, page size, and returned total.
2. For search results, show caption, video ID, creator, country, plays, likes, comments, shares, engagement rate, and product/commerce metrics only when returned.
3. For detail, group identity, creator, timing, engagement, cover/share URL, and optional `core` metrics.
4. For related products, show product ID/name, region, price range, rating, commission rate, video 30-day sales/GMV, and product total sales/GMV when present.
5. For reviews, show comment ID, text, author handle/nickname, likes, replies, and creation time.
6. Keep 19-digit IDs as strings. Preserve raw timestamps and add a readable date only as a derived label.
7. Report empty arrays honestly. Never imply that an ordinary video is shoppable when `data.items` is empty.

## Important Limitations

1. Data reflects the provider's latest indexed public snapshot and can lag TikTok.
2. The request `country` selects provider context but is not a verified strict row-country predicate; returned `country_code` remains authoritative for each row.
3. Related products are available only for videos linked to products in the indexed dataset.
4. Public comments can be partial, deleted, multilingual, or unavailable.
5. Do not infer sales causality from correlation between views, engagement, and GMV.
6. Do not expose internal tool identifiers, credentials, cache files, signed asset URLs, or unrelated response fields.

## User Expression & Scenario Quick Reference

**Use this skill**: “用出海匠搜美国 TikTok 美妆视频”, “看这个视频详情和评论”, “这个视频带了哪些商品”, “Chuhaijiang video analytics”.

**Adjacent**: General public TikTok shoppable-video rankings or detail requests without a named source should use `linkfox-kalodata-tiktok-video`. Product-first research uses `linkfox-chuhaijiang-tiktok-product`; creator-first research uses `linkfox-chuhaijiang-tiktok-creator`. Uploading or publishing videos uses `linkfox-tiktok-video`.

**Not applicable**: video upload/publishing, creator authorization, seller-backend operations, video downloading, moderation, transcription, or media generation/editing.

## 算力消耗规则

按端点分别计费：视频详情 9 算力/次；视频搜索、视频带货商品和视频评论 18 算力/次。

> 用户会因算力消耗而支付费用。高频调用或多端点钻取前，先说明预计调用次数与算力消耗。

---

**Feedback:** Use the Feedback API in `references/api.md` only when the user explicitly asks to submit feedback or authorizes it after an issue is identified. Sanitize the content and never include credentials, signed URLs, phone numbers, or unrelated task context.
