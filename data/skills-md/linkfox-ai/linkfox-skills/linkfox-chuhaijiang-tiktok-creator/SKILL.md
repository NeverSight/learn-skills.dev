---
name: linkfox-chuhaijiang-tiktok-creator
description: 使用出海匠（Chuhaijiang）研究 TikTok 公开达人市场，支持达人搜索、详情、关联直播/商品/视频、机构榜、带货达人榜和涨粉榜。用户点名出海匠或 Chuhaijiang 时触发；未指定数据源时，仅对达人关联直播、机构榜或跨商品/视频的组合钻取触发。通用 TikTok 达人榜单、搜索和详情使用 linkfox-kalodata-tiktok-creator；商品到达人发现使用 linkfox-chuhaijiang-tiktok-product；点名其他数据源时不触发。
---

# TikTok Creator Market Intelligence

Use this skill to research public TikTok creator markets: discover creators, inspect one creator, trace their livestreams, products, and videos, or compare agency, commerce, and follower-growth rankings.

## Core Concepts

- Normal endpoints require a lowercase marketplace code.
- Search and relationship endpoints return at most 10 records per page; ranking endpoints return at most 20.
- Creator detail can request `channel`, `core`, or `portrait` expansions with a comma-separated `include` value.
- Each endpoint call is billed independently. Reuse the 24-hour cache for identical requests; cache identity includes the gateway, API-key fingerprint, endpoint, and parameters.
- Relationship ownership follows the starting entity: product-to-creator discovery belongs to the product skill; this skill owns creator-to-product, creator-to-live, and creator-to-video drill-downs.

## Data Fields

| Field | Meaning |
|---|---|
| `data.total_count` | Total matching records when returned |
| `data.items` | Creator, relationship, or ranking records |
| `id` / `uid` / `creator_oecuid` | Creator identifiers; retain the identifier required by the next endpoint |
| `nickname` / `unique_id` | Creator display identity |
| `follower_count` | Audience size when returned |
| `author_avg_engagement_rate` | Average engagement metric in creator search |
| `total_video_live_30d_gmv` | Combined 30-day video and live GMV in creator search |
| `video_30d_gmv` / `live_30d_gmv` | Channel-specific 30-day commerce performance |

Response fields vary by endpoint and optional detail expansion. Read `references/api.md` before parsing nested fields and preserve the runtime types returned by the API.

## Endpoints

| Intent | Endpoint | Script | Points/call |
|---|---|---|---:|
| Filter and discover creators | `/chuhaijiang/creators/search` | `chuhaijiang_creator_search.py` | 18 |
| Inspect one creator | `/chuhaijiang/creators/detail` | `chuhaijiang_creator_detail.py` | 9 |
| Find a creator's livestreams | `/chuhaijiang/creators/related-lives` | `chuhaijiang_creator_related_lives.py` | 18 |
| Find a creator's promoted products | `/chuhaijiang/creators/related-products` | `chuhaijiang_creator_related_products.py` | 18 |
| Find a creator's videos | `/chuhaijiang/creators/related-videos` | `chuhaijiang_creator_related_videos.py` | 18 |
| Browse creator-agency ranking | `/chuhaijiang/creators/rankings/agencies` | `chuhaijiang_creator_rank_agencies.py` | 18 |
| Browse commerce-creator ranking | `/chuhaijiang/creators/rankings/commercial` | `chuhaijiang_creator_rank_commercial.py` | 18 |
| Browse follower-growth ranking | `/chuhaijiang/creators/rankings/growth` | `chuhaijiang_creator_rank_growth.py` | 18 |

Call only the endpoint required by the user's current question. Ask before making additional paid drill-down calls that the user did not request.

## Parameter Guide

- `country`: one of `br,de,es,fr,gb,id,it,jp,mx,my,ph,sg,th,us,vn` in lowercase.
- `id`: required for detail and relationship endpoints. Reuse the creator identifier returned by search or ranking results.
- `page`: starts at 1. `pageSize` is optional; use no more than 10 for search/relationships and no more than 20 for rankings.
- Search supports `keyword`, `category`, follower, 30-day GMV, average-view and engagement ranges, `hasContact`, and `sort`.
- Commerce and growth rankings require `date` (`YYYYMMDD`) and `granularity` (`daily`, `weekly`, `monthly`, `0`, `1`, or `2`).
- Use camelCase request names shown in `references/api.md`; do not send upstream snake_case names.

## 调用方式

- **API 端点**：8 个 LinkFox 网关能力均使用 POST；完整请求地址、参数、响应和错误码见 `references/api.md`。
- **Python 脚本**：`python scripts/<entry>.py '<JSON 参数>' [--inline]`
- **成本约束**：业务入口脚本默认只缓存成功响应 24 小时，业务成功的空结果也可缓存；缓存按当前工作目录、调用身份、网关、端点和完整请求参数隔离。相同组合命中时输出 `Cache hit`，不会发起新的付费请求。HTTP 或业务失败不缓存；`--inline` 不绕过缓存；`--no-cache` 会强制真实请求并可能再次消耗算力，仅在用户明确同意额外消耗或调试时使用。

**输出策略（8 个达人业务脚本）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-chuhaijiang-tiktok-creator-<timestamp>.json`；`<cwd>` 为脚本执行时的当前工作目录，当前目录不可写时退出报错，不回退到用户目录或系统临时目录。
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 输出请求参数、顶层状态、`data.total_count`、各业务列表长度和首个非空业务列表的前 3 条样本
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 解决认证和算力问题

发生以下异常情况时，采用 references/onboarding.md 引导解决问题：

### 异常情况

- **未配置API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY`，也未配置 `LINKFOXAGENT_API_KEY`。
- **响应401或402状态码**
- **响应提示算力或余额不足**：消息含“算力余额不足/计费不足/余额不足/quota exceeded/insufficient balance/套餐到期/需充值/请充值”，或类似含义的内容。

## Usage Examples

```bash
python scripts/chuhaijiang_creator_search.py '{"country":"us","keyword":"beauty","pageSize":5}'
python scripts/chuhaijiang_creator_detail.py '{"country":"us","id":"7302162228386776110","include":"channel,core,portrait"}'
python scripts/chuhaijiang_creator_related_products.py '{"country":"us","id":"7302162228386776110","pageSize":5}'
python scripts/chuhaijiang_creator_rank_growth.py '{"country":"us","date":"20260828","granularity":"daily","pageSize":5}'
```

## Display Rules

1. State the marketplace, filters, ranking window, total count, and current page when available.
2. For creator lists, show identity, audience size, engagement, content volume, commerce metrics, category, and creator ID when returned.
3. For relationship results, show the endpoint-specific live, product, or video metrics and retain the related entity ID for optional drill-down.
4. Keep currency units and time windows exactly as returned; do not infer a currency or normalize ratios silently.
5. Separate observed API data from recommendations or interpretations.
6. Never expose API keys, private contact details, or raw authentication headers.

## Important Limitations

1. Data is public market intelligence and cannot be treated as the user's private TikTok account or CRM data.
2. This skill does not contact creators, send affiliate invitations, log into accounts, or create campaigns.
3. Do not invent unsupported filters or compensate for an empty result by repeatedly calling paid endpoints.
4. Rankings and creator metrics can change over time; report the request date and ranking window.
5. Contact availability is a search filter, not permission to expose or misuse personal information.

## User Expression & Scenario Quick Reference

**Applicable**:

- **达人发现与详情**：“用出海匠找美国 TikTok 美妆达人”，“用 Chuhaijiang 看这个达人详情”。
- **关联数据**：“查这个达人的关联直播”，“看这个达人的带货商品和视频”。
- **达人榜单**：“用 Chuhaijiang 看达人涨粉榜”，“分析出海匠达人机构榜”，“查看带货达人榜”。

**Adjacent**: General TikTok creator searches without a named source should use the existing dedicated creator skills. Product-to-creator discovery starts from a product ID and belongs to the product skill. Requests naming Kalodata, FastMoss, EchoTik, or another provider should use that provider's skill.

**Not applicable**: private outreach, affiliate invitations, account login, campaign creation, creator impersonation, or extracting unsupported personal data.

## 算力消耗规则

按端点分别计费：达人详情 9 算力/次；达人搜索、关联直播、关联商品、关联视频、达人机构榜、带货达人榜和达人涨粉榜 18 算力/次。

> 用户会因算力消耗而支付费用。高频调用或多端点钻取前，先说明预计调用次数与算力消耗。

**Feedback:** Use the Feedback API in `references/api.md` only when the user explicitly asks to submit feedback or explicitly authorizes submission after an issue is identified. Summarize and sanitize the content; never include API keys, creator contact details, raw user messages, or unrelated task context.

---
*For more high-quality, professional cross-border e-commerce skills, visit [LinkFox Skills](https://skill.linkfox.com/).*
