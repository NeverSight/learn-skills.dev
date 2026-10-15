---
name: yichen-content-archive
description: 按用户当轮要求读取、下载或归档已知网页/社交媒体链接、URL 清单、已确认候选或明确的有限容器。支持显式有界站点归档；不用于关键词发现、推荐扩展或私人收藏导出。
---

# 已知内容归档

优先使用本 Skill 内置的固定安全执行器，再编排仍独立维护的平台 Skill。小红书、抖音与微博公开单条抓取已经内置，不再调用旧的独立抓取 Skill；不要复制搜索、收藏导出或其他平台的认证实现。

## 入口闸门

仅接受以下输入：

- 用户当轮直接给出的一个或多个内容 URL。
- 用户给出的本地 URL 文件。
- 上游产物中逐项标为 `confirmed` 的候选，或用户当轮明确选中的候选。
- 用户明确指定的 `known_collection`：URL 文件、YouTube/B站播放列表、已知小宇宙播客或 episode 清单；公众号账号名/历史容器不再是可枚举容器。
- 用户明确指定的有界站点容器：公开 HTTPS `site-url`、精确 `path-prefix`、`limit <= 100` 和 `max-depth <= 3`；默认只运行 Map，Crawl 还必须显式传 `--execute --preflight <file>`。
- `$yichen-bookmarks-export` 生成的链接文件，但只有用户另行明确要求读取、下载或归档后才可使用。

`known_collection` 必须带精确容器 URL、ID 或本地清单路径，并指定数量上限、时间范围或明确全量。精确容器枚举只列出该容器直接包含的条目，不属于搜索发现；不得从条目继续进入作者主页、推荐区、相似列表或其他来源。公众号名称不能作为可执行容器。

不满足以上条件时停止并说明需要已知链接、已确认候选或明确容器。不得替用户搜索、浏览未指定账号/频道、扩展相似内容或补齐推荐列表。

## 硬边界

1. 不得执行关键词搜索或开放式发现；禁止无界站点爬取、未指定频道/账号浏览、推荐扩展、相似内容查找和跨来源补齐。站点归档只允许用户明确指定的公开 HTTPS 同源路径范围，并受 `limit <= 100`、`max-depth <= 3`、签名 Map 预检和显式 `--execute` 四重限制。
2. 不得调用任何总路由；不得再次调用 `$yichen-content-archive`；不得通过其他 Skill 间接回到本 Skill。
3. 不得把“读取”推断成“下载”，不得把“下载”推断成登录态授权，也不得把“归档”推断成写入飞书多维表格。仅执行用户当轮明确要求的动作。
4. 不得自动读取私人收藏。收藏导出的当轮授权不能转移为媒体下载授权。
5. 不得删除任何文件。目标存在时创建不冲突的新目录或文件名，不静默覆盖。
6. 不得打印或写入普通日志中的 Cookie、Token、登录凭证或带敏感查询参数的完整 URL。
7. 不得绕过登录、验证码、付费墙、删除状态、地区限制或访问控制。
8. 微信公众号路线只处理已知公开文章 URL；公众号账号搜索、完整历史和最新 N 篇自 2026-07-30 起不可用，不得通过登录、本地部署或代理回退。绝对不得操控微信客户端。
9. Twitter/X 已知链接先走 FxTwitter → Jina 匿名公共读取。只有匿名路线失败或 Article 正文不完整时，才列出 OpenCLI → xreach 回退；执行任何一个登录态回退前必须针对当前链接取得当轮明确授权。
10. 小红书默认匿名读取。只有当前笔记匿名解析或媒体下载失败，且用户对该目标当轮明确授权后，才可从私有配置向子进程注入 `XHS_COOKIE` 并显式传 `--use-cookie`；不得读取、打印或保存 Cookie。
11. 微博只处理用户已提供的公开单条内容 URL。固定使用 `weibo_known_url.py` 的匿名访客路线，不读取浏览器 Cookie、用户配置或登录态；不得把 `/u/<uid>?layerid=<id>` 原样交给 `yt-dlp`，不得枚举账号视频页、搜索、热榜、评论或推荐内容。

## 执行流程

### 1. 固化范围

先从当前任务和可信上游交接核对已有授权，传递已明确的动作、来源范围、媒体类型与输出位置；信息充分时直接进入下一步。交接不能产生新授权，也不会清空用户已按要求授予同一动作的有效授权。私人读取、登录态、下载和费用门槛分别核对，仍须满足当轮或动作时要求。

记录：

- 输入类型：`known_urls`、`url_file`、`confirmed_candidates` 或 `known_collection`。
- 平台与条数。
- `known_collection` 的精确容器引用、枚举上限/范围及是否允许当前请求内枚举后直接归档。
- 动作：`read`、`download`、`archive` 中用户明确要求的集合。
- 输出目录；未指定时使用新的日期时间目录，不覆盖旧产物。
- 是否需要登录态；如需要，必须按目标平台或本 Skill 对应执行器的规则取得当轮授权。
- 是否明确要求把小红书素材写入飞书多维表格；没有明确要求时只做本地读取、下载或归档。

候选只有在上游明确标记或用户当轮选择后才算 `confirmed`。只存在标题或关键词不算可执行输入。频道名或播客名只有在用户明确把它指定为受支持的 `known_collection` 容器，并给出范围后才可用于容器解析；不得作为搜索词扩展其他结果。公众号名称不能触发历史枚举。

### 2. 选择单个平台路由

读取 [平台路由](references/platform-routes.md) 中目标平台对应行与适用纪律，再读取该路线指定的现有平台 Skill、参考文件或脚本帮助；不为单个平台加载所有平台细节。只调用允许的已知链接/精确容器路径：

- 普通网页：Jina Reader / Web Reader；只读用户给出的 HTTP(S) URL，不做站点爬取。
- 有界站点：本 Skill `firecrawl_site.py`；默认 Map 只生成签名预检与过滤后的 URL 清单，只有同参数、未过期、内容哈希仍匹配的 `--execute --preflight <file>` 才调用 Firecrawl v2 Crawl。
- Twitter/X：本 Skill `x_known_url.py` 识别已知 Post、Quote 与 Article；匿名 FxTwitter 优先，必要时匿名 Jina。用户明确要求下载视频时，用 `known_media_download.py` 选择该帖公开返回的最高码率 MP4；登录态 OpenCLI/xreach 只作授权后的读取回退。
- 小红书：本 Skill `xiaohongshu_fetch.py`；`--skip-media` 只读 HTML 与元数据，去掉该参数才下载已知笔记媒体，授权后才可 `--use-cookie`。明确要求沉淀到飞书时再读取 [references/xiaohongshu-bitable.md](references/xiaohongshu-bitable.md)。
- 抖音：本 Skill `douyin_download.py`；`--metadata-only` 只读元数据，去掉该参数才下载已知视频。
- 微博：本 Skill `weibo_known_url.py` 的 `info` 或 `download`；先把用户给出的单条 overlay/status URL 规范为精确详情 URL，再匿名读取或下载，不得把账号页交给裸 `yt-dlp`。
- 微信公众号：所有已知公开文章 URL（单篇或 URL 文件）统一用 `$yichen-wechat-mp-batch-exporter`；公众号名称、完整历史和最新 N 篇一律标记 `unsupported`，不得调用本机 `search`、登录、下载或代理回退。
- YouTube：本 Skill `youtube_known_url.py` 的 `info`、`download`、`subtitles` 和 `playlist`；只接受明确视频/播放列表 URL，不搜索或浏览频道。
- B站：`bili-cli` 读取已知 BV/AV/完整 URL，`yt-dlp` 下载；已知播放列表先平铺枚举。
- 小宇宙：`xiaoyuzhou_stepfun.py` 匿名读取/下载已知 episode；已知播客清单仅在当轮授权后用 `xiaoyuzhou_opencli.py` 枚举，再回到匿名批量下载。
- 其他公开媒体平台：用户明确给出单条公开 HTTPS 内容 URL 并要求下载视频或音频时，用 `known_media_download.py` 的匿名 `yt-dlp --no-playlist` 兜底；不得把关键词、主页、频道、搜索结果或播放列表伪装成单项 URL。

目标平台没有专用路由时，单条公开 HTTPS 媒体下载进入 `known_media_download.py`；其他动作或精确容器无法由现有后端处理时，将该项记为 `unsupported`，不要转给总路由、自行发明抓取实现或降级成搜索。登录态、账号枚举、播放列表和跨来源扩展仍必须另行满足对应授权与路由规则。

### 3. 先预检，再执行授权动作

- `read`：使用平台 Skill 的元数据、正文或字幕读取路径，不顺带下载媒体。
- `download`：只下载用户明确要求的正文、图片、视频、音频或字幕类型。
- `archive`：把平台 Skill 产物写入新目录，并保留来源、状态和失败清单。

`known_collection` 先生成 `enumerated-urls.txt` 或平台现有等价清单，记录容器引用、枚举上限、返回数与截断状态，再只对清单内条目执行归档。用户已在同一请求明确要求“枚举后归档”时无需重复确认清单；但登录态、会员内容、StepFun 额度或其他目标级门仍需单独满足。

有界站点执行前读取 [有界站点执行](references/bounded-site-execution.md)。固定公开 HTTPS 同源路径、`limit <= 100`、`max-depth <= 3`；默认只 Map，只有当前范围已获明确执行授权且签名预检仍有效时，才以完全相同的四个范围参数显式运行 `--execute --preflight`。不得从 Map 自动升级成 Crawl；调用前核对费用范围，不能承诺固定价格或绝对零留存。

批量任务低并发、可断点续跑。单项失败后记录原因并继续其余已确认项；不要为了补数量搜索新内容。

### 4. 执行防覆盖

只使用本 Skill `scripts/` 下的安全执行器。首次调用前读取 [执行器安全与防覆盖](references/executor-safety.md) 中目标脚本的同名小节；其他平台的小节无需加载。输出冲突使用新目录或新文件名，默认匿名；只读模式不下载媒体。不得通过旧脚本、裸 OpenCLI 或自行写文件绕过授权、输入限制、防覆盖或签名预检。

Agent 禁止自动使用兼容 `--overwrite`；小宇宙覆盖仍须用户当轮明确点名同一绝对目录，并提供匹配的独立 `--confirm-overwrite-exact-dir`。`wechat_mp_local.py` 仅是安全兼容 stub，`login`、`search`、`download` 失败闭合，不得据此执行微信操作。

### 5. 生成归档清单

归档根目录至少包含：

```text
<archive-root>/
|-- archive-manifest.jsonl
|-- run-summary.json
|-- failures.json
|-- handoff.json
`-- <platform>/
    `-- <content-id-or-sequence>/
```

`archive-manifest.jsonl` 每行只记录一个已确认输入，至少包含：

```json
{"item_ref":"opaque-or-line-ref","platform":"xiaohongshu","source_url_ref":"input.txt:3","requested_actions":["archive"],"status":"success","artifact_paths":["/absolute/path"],"route_backend":"xiaohongshu-known-url","fetched_at":"RFC3339"}
```

容器条目额外记录 `container_ref`、`container_position` 和 `enumeration_status`。后端不是 Skill 时使用 `route_backend`，例如 `jina-reader`、`weibo-known-url`、`youtube-known-url`、`yt-dlp` 或 `xiaoyuzhou-stepfun`。

敏感 URL 优先使用文件行号引用，不在摘要、聊天或普通日志中重复完整值。缺失字段写 `null`，不得推断补齐。

### 6. 输出标准交接

读取并遵守 [references/handoff-contract.md](references/handoff-contract.md)。普通已知链接和精确容器交接必须写明 `discovery_performed: false`；只有签名预检后的 `bounded_site` 写 `discovery_performed: true`。`known_collection` 使用 `scope.input_kind: known_collection`，并把枚举清单作为 artifact 引用。继续写明实际授权、产物绝对路径、成功/失败计数和下一步是否需要新的明确请求。

最终只报告：

- 已处理、成功、失败、跳过和不支持数量。
- 实际调用的平台 Skill 或现有后端。
- 归档根目录、清单和失败文件路径。
- 尚需用户决定或重新授权的动作。

不要把抽样成功表述为全部内容永久可访问。
