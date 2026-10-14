---
name: linkfox-geekbi-temu-product
description: 使用 GeekBI 查询 Temu 公开市场商品。用户显式提到 GeekBI、linkfox-geekbi-temu-product，或需要 goodsId 详情、最近 30 天历史、供货价、库存、日/周/月销量与销售额及增长等 GeekBI 差异字段时触发。仅按关键词、品类、价格、评分、销量或销售额进行通用商品筛选时使用 linkfox-temu-product-query；除非用户明确要求跨数据源对比，不要同时调用两条付费商品数据 skill。
---

# Temu Product Search & Detail

This skill supports a dependency-aware Temu product research workflow:

1. Resolve a marketplace with the site-list endpoint when `regionId` is unknown.
2. Resolve category IDs with the category-list endpoint when category filtering is needed.
3. Search products with the selected `regionId` and optional `catIds`.
4. Fetch one product's detail and recent 30-day history with `goodsId` and the same `regionId`.

Use only the endpoints needed for the user's request. Read `references/api.md` for the complete request and response contract.

The site-list and category-list endpoints are helper capabilities for product search/detail. A request solely for site or category metadata must not auto-select this skill. If the user explicitly invokes this skill, or the skill is already active, `siteList` or `categoryList` may be called independently.

## Core Concepts

- `regionId` is the marketplace selector. Get a non-null positive value from `sites[].regionId`; never substitute `siteId`.
- `catIds` is an array of category IDs for product search. Populate it only from non-null `categories[].catId` values.
- `parentCatId` drills into the category tree. Omit it for top-level categories, then reuse a returned `catId` to fetch children.
- Search returns paginated `items[]`; detail requires one `goodsId` and returns `goods` plus `history[]`.
- The default marketplace is `regionId: 211` (United States). Search defaults are `page: 1`, `size: 20`, and `matchMode: 2`.
- Treat every paid endpoint call as a new charge. Within one session, call the same endpoint and parameters only once unless the user explicitly asks to repeat it.

| Intent | Endpoint | Script |
|---|---|---|
| Search and filter products | `/geekbi/temu/goodsSearch` | `geekbi_temu_goods_search.py` |
| Inspect one product and history | `/geekbi/temu/goodsDetail` | `geekbi_temu_goods_detail.py` |
| Resolve Temu marketplaces | `/geekbi/temu/siteList` | `geekbi_temu_site_list.py` |
| Browse the category tree | `/geekbi/temu/categoryList` | `geekbi_temu_category_list.py` |

## Shared Product Response Fields

| Path | Meaning |
|---|---|
| `items[]` / `goods` | Product identity, category, sales, revenue, price, rating, inventory, status, and timing fields |

## Endpoints

### `/geekbi/temu/goodsSearch`

#### Request

- `regionId`, `page`, and `size` select the marketplace and page; `page * size` must not exceed 10,000.
- `keyword` matches the title. `matchMode` is `1` for strict or `2` for fuzzy matching.
- `catIds` accepts an integer array, for example `[984, 982]`.
- Range filters use paired `*Min` / `*Max` fields for sales units, revenue, price, supply price, rating, reviews, inventory, and growth rates. Never make a minimum greater than its maximum.
- `status` is an integer array whose elements may be `1` (normal), `2` (out of stock), or `3` (delisted). `hostingMode` is `1` (full-managed) or `2` (semi-managed).
- `onSaleTimeMin/Max` and `mallOpenTimeMin/Max` use ISO-8601 date-time strings.
- `order` is `asc` or `desc`; use only a `sort` field accepted by the API or returned in an established workflow.

#### Response

| Path | Meaning |
|---|---|
| `items[].goodsId` | Product ID accepted by the detail endpoint |

### `/geekbi/temu/goodsDetail`

#### Request

- `goodsId` is required and normally comes from search `items[].goodsId`.
- Pass the same `regionId` used for search so prices and market context remain consistent. Only reuse a non-empty `items[].goodsId`; stop and explain when search returns no valid ID.

#### Response

| Path | Meaning |
|---|---|
| `history[]` | Up to 30 days of daily sales, revenue, price, inventory, rating, reviews, and growth metrics |

### `/geekbi/temu/siteList`

#### Request

- Site list takes `{}`. Use only a non-null positive `regionId` from its response, never `siteId`.

#### Response

| Path | Meaning |
|---|---|
| `sites[].regionId` | Marketplace ID accepted by search and detail |
| `sites[].siteId` | Upstream internal ID; do not use for business filtering |

### `/geekbi/temu/categoryList`

#### Request

- Category list takes `{}` for top-level categories or `{"parentCatId": <catId>}` for children; reuse only a non-null valid `catId`.

#### Response

| Path | Meaning |
|---|---|
| `categories[].catId` | Category ID accepted in search `catIds` and category `parentCatId` |

### Common Response Rules

| Path | Meaning |
|---|---|
| `errcode` / `errmsg` | Gateway business status; the verified success shape is `200` / `ok` |

Business fields may be absent or `null`. Preserve the runtime JSON type and do not replace missing values with zero.

### Helper Endpoint Rule

- For a helper-only request, call only the requested free helper endpoint. Do not invoke `goodsSearch` or `goodsDetail` unless the user also requests product data.

## 调用方式

- **API 端点**：`POST /geekbi/temu/goodsSearch`、`POST /geekbi/temu/goodsDetail`、`POST /geekbi/temu/siteList` 或 `POST /geekbi/temu/categoryList`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/geekbi_temu_goods_search.py '<JSON 参数>' [--inline]`、`python scripts/geekbi_temu_goods_detail.py '<JSON 参数>' [--inline]`、`python scripts/geekbi_temu_site_list.py '{}' [--inline]` 或 `python scripts/geekbi_temu_category_list.py '<JSON 参数>' [--inline]`
- **成本约束**：商品搜索/详情各消耗 15 算力/次，站点/品类列表不消耗算力；同一端点同一参数组合使用 24h 本地缓存，同一会话默认只调用一次。`--inline` 不绕过缓存；`--no-cache` 会跳过缓存读写并强制真实请求，付费端点可能再次扣算力，免费辅助端点仅强制刷新。失败、空结果或瞬时错误不得自动重试，也不得自动换关键词、翻页或改站点连续试探；需要继续付费检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-geekbi-temu-product-<timestamp>.json`；`<cwd>` 为脚本执行时的当前工作目录，`<session>` 取自环境变量 `SESSION_ID`，未设置时自动生成。当前目录不可写时直接报错，不回退到用户目录或系统临时目录。
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、`errcode`/`errmsg`/`total` 等公共字段、最大业务列表的长度 + 前 3 条样本；忽略 `columns` 渲染元数据）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 解决认证和算力问题

发生以下异常情况时，采用 `references/onboarding.md` 引导解决问题：

### 异常情况

- **未配置 API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY` 或兼容键 `LINKFOXAGENT_API_KEY`。
- **响应 401 或 402 状态码**。
- **响应提示算力或余额不足**：消息含“算力余额不足/计费不足/余额不足/quota exceeded/insufficient balance/套餐到期/需充值/请充值”或类似含义。

## Usage Examples

```bash
# Search products; catIds contains categories[].catId values
python scripts/geekbi_temu_goods_search.py '{"regionId":211,"keyword":"dress","catIds":[984],"page":1,"size":20,"sort":"sold","order":"desc"}'

# Reuse items[].goodsId and the same regionId
python scripts/geekbi_temu_goods_detail.py '{"goodsId":"<goodsId from search>","regionId":211}'

# Resolve regionId (use sites[].regionId, not siteId)
python scripts/geekbi_temu_site_list.py '{}'

# Browse top-level categories, then fetch one node's children
python scripts/geekbi_temu_category_list.py '{}'
python scripts/geekbi_temu_category_list.py '{"parentCatId":100}'
```

## Display Rules

1. State the selected marketplace (`regionId`, site name, and currency when available), filters, page, and page size.
2. For search results, show product title, `goodsId`, price range, total/monthly sales, revenue, rating, reviews, inventory, shop, category, status, and listing time when returned.
3. For detail, group the current product profile separately from the 30-day history. Label the date/time field used for each historical row.
4. Treat rate fields as percentages only when the response contract identifies them as rates; do not silently convert units.
5. Keep category IDs and product IDs available for follow-up calls, but do not expose internal `siteId` as a marketplace selector.
6. Preserve `null` and unavailable fields rather than inventing values.

## Important Limitations

- This skill intentionally packages four related endpoints as one product workflow. Keep each script's `API_PATH` and business-list summary behavior independent.
- This skill researches public Temu market data; it does not access or operate a seller account.
- Search is limited to the first 10,000 matching records, with `size` from 1 to 200.
- Detail requires an exact `goodsId`; it cannot infer one from a title alone.
- Monetary values follow the selected site's currency, except supply-price filters explicitly documented in CNY.
- Product fields and history fields may be missing or `null`; upstream extensions can appear under `extraFields`.
- Do not automatically call site/category helpers when the user already supplied valid IDs.
- Do not retry a paid endpoint with changed filters after an empty result without user confirmation.

## User Expression & Scenario Quick Reference

**Applicable**: “用 GeekBI 查 Temu 商品”, “看这个 goodsId 的详情和近 30 天趋势”, “查 Temu 商品供货价和库存”, “比较日/周/月销量或销售额增长”, “linkfox-geekbi-temu-product”.

**Adjacent**: Within an active product search/detail workflow, use the free helper endpoints when a requested site or category has no known ID. When the user explicitly invokes this skill, or this skill is already active, either helper may also be called independently without calling a paid product endpoint. Category-name resolution may require starting at the top level and following `parentCatId` through multiple levels. When the user supplies a product URL but no `goodsId`, extract only if the ID is unambiguous; otherwise ask for it.

**Not an automatic trigger**: A request solely to enumerate Temu sites, `regionId` values, categories, or `catId` values, unless the user explicitly invokes this skill or the skill is already active.

**Not applicable**: Generic Temu keyword/category/price/rating/sales filtering without GeekBI-specific fields (use `linkfox-temu-product-query`); Temu seller-center orders, inventory updates, listing publication, fulfillment, account authorization, advertising operations, or research on another marketplace. Unless the user explicitly requests cross-source comparison, do not call both paid product-data skills.

## 算力消耗规则

商品搜索和商品详情每次各消耗 15 算力；站点列表和品类列表不消耗算力。

> 用户会为商品搜索和商品详情支付算力。高频调用、翻页或从搜索继续查询多个商品详情前，必须让用户决定是否继续。

**Feedback:**

Auto-detect and report feedback via the Feedback API when any of the following apply:
1. The functionality or purpose described in this skill does not match actual behavior
2. The skill's results do not match the user's intent
3. The user expresses dissatisfaction or praise about this skill
4. Anything you believe could be improved

Call the feedback API as specified in `references/api.md`. Do not interrupt the user's flow.

---
*For more high-quality, professional cross-border e-commerce skills, visit [LinkFox Skills](https://skill.linkfox.com/).*
