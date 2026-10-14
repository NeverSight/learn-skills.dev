---
name: linkfox-geekbi-temu-search-by-image
description: 基于商品图片在 Temu 公开市场检索视觉相似或同款商品，返回商品、销量、价格、评价、库存、供货价、店铺与品类数据。当用户明确提出 Temu 以图搜图、Temu 图搜同款、reverse image search on Temu、Temu visual product search，或提供图片/图片 URL 并明确希望在 Temu 查找相似商品时触发。未指定 Temu 的泛化图片找货请求不自动触发。本 skill 不用于跨平台找 1688 货源、图片识别或编辑、商品详情历史查询、关键词商品搜索。
---

# Temu Visual Product Search

Find visually similar or matching products in Temu's public marketplace from one product image. Use the returned product, sales, pricing, review, inventory, shop, and category fields for visual competitor discovery and product research.

## Core Concepts

- The search input is one image URL. The gateway accepts a LinkFox OSS URL, not an arbitrary external image URL.
- Upload local images with `scripts/upload_image.py`. For an external image URL, download it locally first, then upload it through the same helper.
- The endpoint returns a non-paginated `items` list plus rendering metadata in `columns`. Result count depends on the source image: live tests have returned both 100 rows and a successful empty result, so never assume a fixed or non-zero count.
- Rows are live third-party marketplace data. Fields may be absent, null, duplicated by `goodsId`, garbled, or internally inconsistent; preserve the source values and disclose material quality issues.

## Data Fields

| Group | Fields |
|---|---|
| Identity | `goodsId`, `mallId`, `goodsName`, `goodsNameCn`, `goodsNameEn`, `brand`, `thumbnail` |
| Category | `catIds`, `catItems` |
| Demand | `sold`, `mallSold`, `daySold`, `weekSold`, `monthSold`, corresponding `*SoldRate` fields |
| Revenue | `sales`, `daySales`, `weekSales`, `monthSales`, corresponding `*SalesRate` fields |
| Price and supply | `minPrice`, `maxPrice`, `supplyPrice`, `minSupplyPrice`, `medianSupplyPrice`, `maxSupplyPrice` |
| Quality and stock | `goodsScore`, `reviewNum`, `quantity`, `sku` |
| Status and timing | `hostingMode`, `status`, `isAd`, `isCustom`, `isPresale`, `similarNum`, `onSaleTime`, `mallOpenTime`, `createTime`, `updateTime` |

## Parameter Guide

| Parameter | Required | Description |
|---|---:|---|
| `imageUrl` | Yes | LinkFox OSS image URL returned by `scripts/upload_image.py`; maximum 2048 characters; an arbitrary external URL is rejected |
| `contentType` | No | Image MIME type, maximum 100 characters; only `image/jpeg`, `image/png`, `image/gif`, `image/webp`, or `image/bmp`; when supplied, it must match both the OSS response type and the actual image bytes |

Do not add pagination, sorting, filtering, region, Base64, or keyword fields: they are not part of this endpoint's verified request contract.
The downloaded image must be JPEG, PNG, GIF, WebP, or BMP and no larger than 10 MB.

## 调用方式

- **API 端点**：`POST /geekbi/temu/goodsImageSearch`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/geekbi_temu_goods_image_search.py '<JSON 参数>' [--inline]`
- **成本约束**：以图搜索消耗 150 算力/次；同一端点同一参数组合使用 24h 本地缓存，同一会话默认只调用一次。`--inline` 不绕过缓存；`--no-cache` 会跳过缓存读写并强制真实请求，可能再次消耗 150 算力。失败、空结果或瞬时错误不得自动重试，也不得自动换图片连续试探；需要再次付费搜索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-geekbi-temu-search-by-image-<timestamp>.json`；`<cwd>` 为脚本执行时的当前工作目录，`<session>` 取自环境变量 `SESSION_ID`，未设置时自动生成。当前目录不可写时直接报错，不回退到用户目录或系统临时目录。
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层状态字段、常见业务计数、忽略 `columns` 后最大业务列表的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 解决认证和算力问题

发生以下异常情况时，采用 `references/onboarding.md` 引导解决问题：

### 异常情况

- **未配置 API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY` 或兼容键 `LINKFOXAGENT_API_KEY`。
- **响应 401 或 402 状态码**。
- **响应提示算力或余额不足**：消息含“算力余额不足 / 计费不足 / 余额不足 / quota exceeded / insufficient balance / 套餐到期 / 需充值 / 请充值”或类似含义。

## Local Image Upload

This endpoint requires an image hosted on LinkFox OSS. When the user provides a local file or an external image URL, obtain a local image file and run:

```bash
python scripts/upload_image.py /path/to/product.jpg
```

The helper requests a presigned PUT URL from `${LINKFOX_TOOL_GATEWAY}/oss/file/presignedPut`, uploads a JPG/JPEG, PNG, GIF, WebP, or BMP image to that URL, removes the private query string, and prints JSON containing `url` and `contentType`. It uses only the Python standard library. Never print the presigned query string or the API key.

## Usage Examples

```bash
# Upload once and capture the returned LinkFox OSS URL and MIME type
LINKFOX_UPLOAD_RESULT="$(python scripts/upload_image.py ./product.jpg)"
LINKFOX_OSS_URL="$(printf '%s' "${LINKFOX_UPLOAD_RESULT}" | jq -r '.url')"
LINKFOX_CONTENT_TYPE="$(printf '%s' "${LINKFOX_UPLOAD_RESULT}" | jq -r '.contentType')"

# Search Temu with exactly that URL and its MIME type
python scripts/geekbi_temu_goods_image_search.py "{\"imageUrl\":\"${LINKFOX_OSS_URL}\",\"contentType\":\"${LINKFOX_CONTENT_TYPE}\"}"
```

User requests include “用这张图找 Temu 同款”, “找外观相似的 Temu 竞品”, and “search Temu products by this image”.

## Display Rules

1. Present a compact table with image, title, product ID, price, total/monthly sales, rating, reviews, hosting mode, and update time when available.
2. Display `thumbnail` images inline when the client supports images.
3. Treat `minPrice` and `maxPrice` as marketplace-local currency values; do not invent a currency when the response does not identify it. Supply-price fields are CNY only when the API reference explicitly says so.
4. Prefer `goodsNameEn` when Chinese title fields are visibly garbled. Do not invent a repaired translation.
5. Do not silently deduplicate repeated `goodsId` rows or repair contradictory values. Explain the issue, or group rows only when the user asks and state the grouping rule.
6. Keep `columns` as rendering metadata; do not include all column definitions unless the user asks for schema details.

## Important Limitations

1. Only a LinkFox OSS `imageUrl` is accepted. Direct Amazon, CDN, data URI, Base64, or arbitrary public URLs are rejected. The image must be JPEG, PNG, GIF, WebP, or BMP and no larger than 10 MB.
2. The verified endpoint exposes no pagination, sorting, filtering, keyword, or marketplace-region controls.
3. Search results are live public-market data and may contain missing, null, duplicate, stale, garbled, or inconsistent fields.
4. `sku` may be a JSON-encoded string rather than a parsed array; parse it only when needed and handle malformed content safely.
5. This skill does not fetch a separate product-detail/history record. Use `linkfox-geekbi-temu-product` when the user explicitly needs details or history for a returned `goodsId`.
6. Do not automatically retry with another image after failure or an empty result; another search may incur cost.

## User Expression & Scenario Quick Reference

**Applicable** -- visual discovery on Temu:

| User Says | Scenario |
|---|---|
| “用这张图片找 Temu 同款” | Find matching products |
| “看看 Temu 上有没有外观相似竞品” | Visual competitor discovery |
| “不用关键词，按图片选品” | Image-led product research |
| “reverse image search this on Temu” | Visual product search |

**Not applicable** -- route elsewhere:

- Keyword, category, sales, or price-filtered Temu search without an image: use `linkfox-temu-product-query`.
- Temu product detail or 30-day history: use `linkfox-geekbi-temu-product`.
- Finding 1688 suppliers from an image: use `linkfox-1688-search-by-image`.
- Image recognition, prompt extraction, generation, or editing: use the relevant multimodal skill.

**Boundary judgment:** If the user provides an image and wants visually similar products specifically on Temu, use this skill. For text filters use `linkfox-temu-product-query`; for detailed records or history of known product IDs use `linkfox-geekbi-temu-product`.

## 算力消耗规则

以图搜索每次消耗 150 算力。

> 用户会因算力消耗而支付费用。需要重复搜索其他图片时，必须先说明会产生额外消耗并由用户决定是否继续。

**Feedback:**

Auto-detect and report feedback via the Feedback API when any of the following apply:
1. The functionality or purpose described in this skill does not match actual behavior
2. The skill's results do not match the user's intent
3. The user expresses dissatisfaction or praise about this skill
4. Anything you believe could be improved

Call the feedback API as specified in `references/api.md`. Do not interrupt the user's flow.

---
*For more high-quality, professional cross-border e-commerce skills, visit [LinkFox Skills](https://skill.linkfox.com/).*
