---
name: dby-api
description: >-
  都爆鸭（doubaoya/本鸭）新媒体取数包：DOUBAOYA_API_KEY取在架数据，做联网事实核查。只给数据：写正文归 dby-write、查违禁词归 dby-banned-words、排版存草稿归 dby-publish，不确定问 dby。要成品图（出图/改图/配图/主视觉）归 dby-image，本包只给封面与标题的**参考数据**。触发词：小红书：搜索/爬取/作品/创作/选题/标题/封面/排行/榜单/热榜/日榜/周榜/周排行/TOP/热门笔记/爆款笔记/笔记查询、公众号：取数/爬虫/标题/封面/排行/榜单/爆文/黑马/对标、抖音：搜索/取数/评论/实时搜索/综合搜索、视频号：AI/日报/爆款/选题、爆款：文章/标题/封面/结构/仿写/复盘/排行/选题/笔记发现、选题：拆解/灵感/素材/角度/信号、封面：灵感/参考/套路/设计/选题、标题：灵感/优化/套路/生成、账号画像/账号体检/账号健康度/账号发文列表、对标：分析/作品/推荐/矩阵/账号/后再写、竞品：账号/诊断/跟踪/发文复盘、出海：选题/爆款/日报/流量风口、笔记：对标/拆解/生成/选题、内容：创作/灵感/出海、跨平台：选题/分析/热搜、热点：扫描/榜、今日热点/综合热点/追热点/蹭热点/借势选题/找选题/中线选题/短视频选题/全网热搜/热搜关键词/全网热榜/聚合热榜/热榜TOP10/每日榜/今日爆款/一周爆款/近期爆款/全平台爆款/低粉爆款/素人爆款/搜抖音爆款、低粉高赞/黑马笔记/黑马账号/头部账号/热门账号/相似账号/标杆账号/小号打法/冷启动对标/起号参考/公众号诊断/批量诊断/被限流/阅读量掉了/周度趋势/近30天作品/最新发布/最多点赞/持续走高/增长榜/阅读增长/增长率排行/流量风向/热度指数/追流量/追更/话题研究/看赛道热门内容、高点击标题/起标题、查出处/引用来源/联网搜索/联网查证/豆包搜索/社媒舆情/舆情监测/用户需求/评论分析/评论风向/看评论/扒评论区、解析链接/链接解析/作品详情/扒文章/扒抖音作品/照着写小红书/找对标笔记/热门文章/批量爬公众号/盯公众号/订阅公众号/某公众号发了什么、AI视频号/小红书抖音公众号/文旅/短剧/赛道日报/每天在推什么/实时取数
version: 4.3.0
changelog: 共享请求层补上 AI 生成内容的法定标识转达：信封顶层的 aigc 此前在 withEnvelope 分支被丢掉，全仓 grep 命中 0 次——服务端挂了标识、agent 侧没人读，等于还是只有网页有。现与 notice 同样统一 warn 到 stderr，并进 withEnvelope 返回
compatibility: >-
  需要环境变量 DOUBAOYA_API_KEY（形如 dyh_…，在 doubaoya.com 密钥中心生成）；需要能对 https://doubaoya.com 发 HTTPS 请求。
  发现类端点（能力清单 / 详情）免鉴权也免费，调用类端点必须带 Bearer 且计费。
  正文里的 curl 示例只要 curl；可选的零依赖封装脚本 scripts/doubaoya.mjs 需要
  Node ≥ 18（用全局 fetch），不装任何 npm 包。
---
# 都爆鸭 · doubaoya

新媒体取数能力包：一条 `DOUBAOYA_API_KEY` 通到平台全部在架数据。
你（agent）的活是**听懂用户想干嘛 → 选对能力 → 调 → 把结果讲成人话**。

调用走 **`scripts/dby.mjs`**，别自己拼路径（硬拼必 404；`api describe` 先拉详情拿 `execution.target` 再打）。

---

## 怎么调

`$SKILL_DIR` = 本包目录（宿主加载本 SKILL.md 时给出的目录），统一走 CLI：`node "$SKILL_DIR/scripts/dby.mjs" <组> <命令> [参数] [flags]`。非 TTY stdout 是单个 `{ok,data|error}` JSON；退出码 0 成功 / 1 一般错误 / 2 用法错 / 3 业务态 / 4 鉴权 / 5 网络超时（**计费请求绝不自动重试**）/ 6 需确认（`--confirm` 放行，回执给的确认命令可原样重放）。参数看 `node "$SKILL_DIR/scripts/dby.mjs" <组> <命令> --help`。

按组命令名（本文件是全量参考；各包 SKILL.md 只列自己用到的那几条）：

- api：list search describe invoke validate recommend
- write：prep topics review articles
- charter：profiles get put
- draft：create get version review-packet precheck submit comment list versions decide merge comments star link
- article：list get
- profile：list get create update delete wechat-history sample-add sample-list sample-rm
- doc：list get patch put revisions revision restore
- material：list get add rm
- insp：list add
- wechat：status render writing-spec topics review publish media-upload theme-list theme-get theme-add theme-update theme-rm
- task：list
- usage：summary balance logs log log-rm analytics
- banned：check
- 单命令：doctor retro upload whoami routes

🔴 先 `dby api describe` 再 `dby api invoke`——入参一律现拉，`requestSchema`/`inputSchema` 是示例值不是 JSON Schema，照键名和值的形状填；上游对错入参一律静默返空或给误导性报错，拿不到数据先回 `describe` 核一遍别急着判「接口挂了」。

→ 要把命令串成自己的流程时读 `references/compose.md`；要照抄骨架写自己的 SKILL.md 时读 `references/user-skill-template.md`。

---

## 0.5 用户该用哪个能力？（按"我想做什么"选）

用户未指明平台时默认公众号。

**本包的地盘**：公开数据、**互动指标**（阅读 / 点赞 / 在看 / 评论）、选题与账号分析——
都爆鸭云端能力覆盖的这一片。写正文、排版、查违禁词、出成品图都不在这里，各有专包。

别人写文章时会来本包取的几样素材（**给数据，不代替他写**）：
`api.gzh.hotArticle` 同主题爆文样本、`api.gzh.cozeData` 同赛道爆款标题与封面套路。
这些都是数据与参考，不会生成成品图。

🔴 **路由由 `dby` 负责；本包只回答「哪条能力给这个数」。**
不要在这里替用户决定下一站去哪个包、也不要自行接续写作交付链——那是 `dby` 的活。
它的路由判据本包**不读、不抄、不复述**，连文件名都不必知道。
按号查发文：先 `api.gzh.searchUser` 拿账号 ID，再 `api.gzh.workList`（上游只认 ID 不认中文昵称）。

**「我自己的东西」例外 —— ⛔ 该能力已下架**：请求指向用户**自己**的内容（帮我记一下 / 我的笔记 /
我是个什么样的人）时过去走 `mera` 第二大脑，**现在调不通且无替代**——**如实告诉用户**，
**别拿公开搜索顶替**（公开搜索看不见他自己的笔记）。详见 `references/retired.md`。

---

→ **查路由（该调哪一条 / 它走哪条路由）时读**
[`references/capability-table.md`](references/capability-table.md)，已经知道调哪条就别读。
入参一律走 `describe` 现拉，那份表一个字段名都不抄。
全量索引与选路的坑在 `dby-gateway/references/capability-index.md` 与 `routing-pitfalls.md`（可选）。

🔴 **合规 / 违禁词：入口请求一律走 `dby-banned-words`**（专职包，三平台一次比对并出全平台安全改写）。
`tool.contentSafety.checkWords`（多平台口径，详情端点 `/api/skills/content-safety-check`）与
`skill.wechat.prohibitedWord`（公众号口径，`/api/skills/wechat-prohibited-word`）在这里只是
**endpoint 索引**，供 gateway 层直调，不作为本入口的路由目标。

🖼 **要成品图去 `dby-image`**（2026-09 随服务端生图能力恢复而重建）。本包给的是封面**数据**——同赛道爆款的封面图 URL、标题与点击量，供你自己提炼套路，不出图。

> ❌ **选题铁律：不要拿用户的账号名 / IP 名当关键词去搜。**
> 用户的公众号/账号名（如「菜籽油」）是**他是谁**（领域/人设/受众），不是搜索词——搜它只会搜到字面同名内容。
> **综合热点用无关键词的 `api.trend.hotSpotKeyword` 直取，IP 名字只用于匹配筛选。**
> 「不带关键词」说的是**关键词**——**时间窗口照样要收窄**（见 Gotchas 第一条）。
> 跨平台趋势雷达（`skill.trend.radar`）**按关键词搜三平台的文章、不是榜**，keyword 必填：
> **手里已经有话题**时用它，看这个词在抖音 / 小红书 / 公众号分别被谁怎么写；
> **没有话题、要它给你想选题**时别用——那种需求走上面的 `api.trend.hotSpotKeyword`。

---

## 失败了怎么办

报错码逐条怎么处置（`noResult` 不是失败、哪些可重试哪些绝不能重试、404 该去另一个集合找）
见 `dby-gateway/references/protocol.md` 第 6 条。
照做仍绕不过去、或想吐槽 → 可提一句用 `dby-feedback` 当场写成反馈（可忽略，不再重复提）。

---

## Gotchas

→ 选定能力之后、真正打请求之前读 [`references/gotchas.md`](references/gotchas.md)；
拿不到数据、或结果明显不对时回来读。最贵的两条先记住：
**热点直取（`api.trend.hotSpotKeyword`）必须收窄时间窗口**，不收窄拿到的是上上周的热榜；
而 **`api.trend.hotKeywords` 恰恰相反，带时间区间必返 0 条**——两条能力的时间语义是反的。

---

## 交付回执（每次交付都随手带一份）

回执随交付写，不事后补。

动手前先说清这一次交到哪一档，**目标停在哪一档就在哪一档收手**。本包交完数据就结束，
**不自行走到下一站**——要不要往下走由 `dby` 判。尤其不要因为「顺手」就去跑 `dby-publish`
（它会写进用户自己的公众号后台，是真实副作用）。拿不准就问一句。

交付末尾附上，四行，别合并：

```
查阅：<读了哪份路由 / 参考了哪张表>
执行：<真正调了哪些能力>
质检：<跑了哪些检查>
跳过：<发现了但没跑的> —— 原因：<为什么不该跑>
```

- **「执行」只写真跑过的**；跑了但失败的写在这里并注明失败，不许挪进「跳过」粉饰。
- **「跳过」只列「发现了、但判断不该跑」的**，压根没发现的不必列。带副作用的尤其不能省。
- 🔴 **只许写能证明的量。** 括号里的结论必须回指这一次真实返回里确实有的东西。
  （违禁词检测回的是风险**类别**数组，所以「命中 N 类」可证；它**不回**等级 / 评分 / 命中词清单，
  所以「0 高危」「低风险」就是编的。）拿不准就回 `describe` 看一眼出参示例。

---

## 硬规则

1. **绝不回显 / 打印 / 记录 key 的任何一部分**——前缀也是。
2. **只通过 `https://doubaoya.com` 的公开接口取数**；不向用户描述、猜测或暴露上游数据来源 / 内部服务。
   对用户而言，能力来自「都爆鸭」。
3. **入参现拉、路径现拉**（用 `describe` / 让脚本去拿），别照记忆或本文档拼。
4. **写脚本以真实数据为素材**，把热点 / 爆款的真实角度落进去，别脱离数据空写。
5. **交付带回执**，四行，「执行」只写真跑过的。

---

## 下一步

| 拿到数据之后 | 去哪 |
|---|---|
| 要出图 / 配图 / 改图 | `dby-image`（文生图 / 图生图 / 改图，出图后落成本地文件）|
| 要把稿子排版、存进公众号草稿箱 | `dby-publish` |
| 要把爆款改写成自己的文案（不调接口、不要 key） | `dby-rewrite` |
| 要立人设 / 取品牌事实 | `dby-charter` |
| 逐跳导航（做完这一步该走哪一步） | `dby` |
| 协议层卡住了（路由 / 信封 / 错误码的完整说明） | `dby-gateway` |
