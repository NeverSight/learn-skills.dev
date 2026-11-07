---
name: supsub-deepread
version: 0.1.0
description: SupSub 精读（deep read）—— 对**已经在上下文里出现过的某一篇文章**做 AI 深度拆解，产出「一句话本质 / 干货成色 / 核心要点 / 分节正文 / 编辑批注（背景·立场·来源可信度·最弱一环）」。匹配「精读这篇」「深读一下」「帮我拆解这篇」「这篇讲透了吗」「这篇靠不靠谱 / 有没有干货 / 有没有立场」「值不值得看」「把这几篇都精读了做份简报」，以及「昨天那篇精读好了吗」「我还有哪些精读没看」。命令：`supsub deepread run / get / list / quota / share / drop / show`。⚠️ **精读消耗按月付费额度**，发起前必须先 `deepread quota` 取当次余额并向用户复述「将消耗 N 次 / 本月剩 M 次」取得同意。⚠️ **contentId 必须来自本轮上下文**（sub contents / focus contents / search 的返回），匹配不到或匹配到多篇一律回问用户，绝不猜、绝不手写。⚠️ `deepread share` 生成的是**任何人可访问且无法撤销**的公开链接，生成前必须单独确认。只是浏览文章列表走 supsub-sub / supsub-focus，关键词搜文章走 supsub-search。
---

# supsub-deepread Skill

精读 = 对**单篇**文章做 AI 深度拆解。它不是摘要（`sub contents` 里的 `summary` 才是摘要），
而是一份带批判视角的结构化拆解：值不值得读、干货在哪、作者什么立场、信源可不可信、论证最弱的一环在哪。

## Prerequisites

- 安装：`curl -fsSL https://raw.githubusercontent.com/SupSub-AI/supsub-cli/master/scripts/install.sh | bash`（native 安装，装到 `~/.local`、支持后台自动更新）；或包管理器 `npm i -g @supsub/cli` / `pnpm add -g @supsub/cli`
- 已登录：`supsub auth status` 显示 Authenticated（首次使用先 `supsub auth login`）
- **未授权（exit 2 / UNAUTHORIZED）时不要止步于「你未登录」**：直接运行 `supsub auth login` 为用户打开浏览器授权（命令会自动打开浏览器并阻塞等待授权，请用足够长的超时，如 10 分钟；用户只需在浏览器点确认，无需在终端输入任何内容），授权成功后重试原命令。无浏览器 / 无头环境再回退为提示用户 `SUPSUB_NO_BROWSER=1 supsub auth login`。
- 精读需要付费计划；无权限时后端返回业务错误（exit 1），如实转达并停止，不要重试。

## 两条硬门禁（先读这两条，再看命令）

### ① 花钱门禁：发起精读前必须确认额度

精读**按次扣月度额度**，且没有「撤销/退额度」的操作。额度上限随套餐/后端调整而变，**一律以 `deepread quota` 当次返回的 `limit` / `remaining` 为准，不要凭记忆里的数字向用户复述余额**。所以：

1. 先 `supsub deepread quota -o json` 取 `{limit, used, remaining}`；
2. 向用户复述：**要精读哪几篇（列标题）、将消耗几次、本月还剩几次**；
3. 得到明确肯定答复后才执行 `deepread run`。

批量时逐篇列出标题让用户确认，**不要**因为用户说了句「都精读了」就自行扩大范围。
用户已经明确点名单篇（「精读这篇」+ 上下文只有一篇）时，一次 `quota` + 一句「将消耗 1 次，本月剩 N 次，现在开始？」即可，不必逐层追问。

> 已经精读过的文章**不会**重复扣费：`run` 会先探测状态，命中 `done` 直接返回结果（`quotaSpent: false`）。
> 所以「这篇之前读过没」不用问用户，跑一遍 `deepread get` 就知道。

### ② 取值门禁：contentId 只能来自上下文

`contentId` 是不透明字符串，**必须**来自本轮会话里 `sub contents` / `focus contents` / `search` 的真实返回。

| 用户说法 | 做法 |
|---|---|
| 「精读第 3 篇」 | 指代上文列表第 3 项 → 直接用它的 contentId |
| 「精读那篇讲 XX 的」 | 在上文列表按标题模糊匹配：**恰好命中 1 篇**才执行；命中 0 篇或 ≥2 篇 → **回问用户**，不要取第一个 |
| 上文没有任何文章列表 | 先 `sub contents --brief` / `search` 把候选列出来，**停下来等用户点名**，不要自作主张选最新一篇 |
| 用户直接粘一条文章 URL | CLI **没有** URL → contentId 的接口。如实说明，并改为从订阅/关注点/搜索里定位这篇 |

**绝不**让用户手输 contentId，**绝不**凭记忆构造或猜测。猜错的代价是花掉一次额度读错文章。

## Workflow

### A. 单篇精读（最常见）

```bash
# 1. 定位文章（拿 contentId + sourceType）
supsub sub contents --source-id 25 --type MP --brief -o json

# 2. 查额度 → 向用户确认 → 才执行
supsub deepread quota -o json

# 3. 发起并等待（默认前台等，实测 20~40 秒）
supsub deepread run --type MP --content-id <cid> --title "<标题>" --source-name "<源名>" -o json
```

`--title` / `--source-name` / `--url` 是**给本地缓存用的展示信息**，精读接口本身不返回标题；
带上它们，本地那份 Markdown 才有像样的标题行，事后 `list` 也认得出是哪篇。**总是带上**。

### B. 批量精读 → 综合简报（CLI+agent 最有价值的用法）

网页端只能一篇一篇点，agent 可以一次排队、一次收割，延迟被摊平（5 篇 ≈ 1 篇的时间）：

```bash
# 1. 取候选 → 列标题 + 消耗次数给用户确认（门禁 ①）
# 2. 并发排队，不等
supsub deepread run --type MP --content-id <c1> --title "…" --no-wait -o json
supsub deepread run --type MP --content-id <c2> --title "…" --no-wait -o json
# 3. 一次等完
supsub deepread list --wait -o json
```

然后基于各篇的 `essence` / `quality.grade` / `keyPoints` 做横向比较和综合。
需要某篇的细节时，读它的 `cachePath`（本地 Markdown 全文）——**不要**把所有全文都塞进上下文。

### C. 跨会话找回（收件箱）

用户隔天问「昨天那篇精读好了吗」「我还有哪些精读没看」：

```bash
supsub deepread list -o json
```

- 默认视图 = **进行中** + **跑完但还没跟用户说过的**（`fresh: true`），播报后自动打水位线，不会天天重复念。
- 看全部历史用 `--all`（`--all` 不动水位线）。
- ⚠️ 队列是**本机本地**的：网页端发起的精读这里看不到，CLI 发起的网页端也看不到（后端没有跨端的精读列表接口）。用户问起时如实说明。

### D. 分享（单独确认）

```bash
supsub deepread share --type MP --content-id <cid> -o json
```

**生成前必须单独向用户确认**，复述这三点：

> 这会生成一个 `https://supsub.net/s/<code>` 页面，**任何人拿到链接都能打开（无需登录）**，
> 且当前 API **没有撤销分享的接口**。确认生成吗？

用户只是想「自己看看全文」时**不要**用 share —— 精读结果本身就已经在输出里，全文也在本地 `cachePath`。
share 只用于「发给别人」。同一篇重复 share 会复用已有分享码（`reused: true`），不会产生第二个公开链接。

## Commands

### `deepread run` — 发起精读

```
supsub deepread run --type <MP|WEBSITE|X> --content-id <cid> [--title <t>] [--source-name <n>] [--url <u>] [--no-wait] [--timeout <sec>] [--brief]
```

| Flag | Default | Description |
|------|---------|-------------|
| `--type` | 必填 | `MP` 公众号 / `WEBSITE` 网站 / `X` 推特 |
| `--content-id` | 必填 | 来自 contents / search 的 contentId |
| `--title` / `--source-name` / `--url` | — | 写进本地队列的展示信息，**建议总是带上** |
| `--no-wait` | — | 只发起不等待（批量排队时用） |
| `--timeout <sec>` | 180 | 前台等待上限，1–600 |
| `--brief` | — | 输出省略正文 sections，只留本质/成色/要点/批注 |

行为：先 `GET` 探测状态 → `none`/`failed` 才 `POST` 发起 → 默认轮询到 `done`。
本地已有 `done` 缓存时**零网络请求**直接返回。

**agent 侧注意**：默认前台等待，实测 20~40 秒。用 Bash 工具跑时把超时设到 **120 秒以上**（默认 120s 通常够，长文接近上限时给到 180s 更稳），或改用 `--no-wait` + `deepread list --wait`。

JSON shape:
```json
{"success":true,"data":{
  "sourceType":"MP","contentId":"…","title":"…","status":"done","version":"v1",
  "quotaSpent":true,
  "cachePath":"/Users/…/.supsub/deepread/u101/MP_xxxx.md",
  "content":{"essence":"…","quality":{"grade":"高","comment":"…"},"keyPoints":["…"],
             "body":{"sections":[{"title":"…","markdown":"…"}]},
             "annotations":{"background":"…","stance":"…",
                            "credibility":{"grade":"中","reason":"…"},"weakestLink":"…"}}}}
```

`status` 取值：`none` 未发起 / `pending` 进行中 / `done` 完成 / `failed` 失败。
**超时或仍在 pending 不是错误**，退出码仍是 `0` —— 按 `status` 字段分支，不要看退出码判断有没有跑完。
`failed` 时可以重跑 `deepread run` 重试（是否重新扣费未确认，重试前告知用户）。

---

### `deepread get` — 查看结果（优先本地缓存）

```
supsub deepread get --type <t> --content-id <cid> [--brief] [--refresh] [--wait] [--timeout <sec>] [--out <file>] [--title <t>] [--source-name <n>] [--url <u>]
```

`done` 是终态、结果不可变，所以默认直接用本地缓存（零请求）；`--refresh` 强制回源。
`--out <file>` 把精读全文导出成 Markdown 文件。查从未精读过的内容返回 `status:"none"`，退出码 `0`。

---

### `deepread list` — 本地精读队列（收件箱）

```
supsub deepread list [--all] [--wait] [--timeout <sec>]
```

只回查 `pending` 项（`done` 不再打扰服务端）。`--wait` 等到队列里所有进行中的都落定。
每项含 `essence` / `qualityGrade` / `cachePath` / `fresh`。

---

### `deepread quota` — 本月额度

```
supsub deepread quota
```

JSON shape: `{"success":true,"data":{"limit":100,"used":7,"remaining":93}}`
（数值仅为示例，实际额度以当次返回为准）

---

### `deepread share` / `show` / `drop`

```
supsub deepread share --type <t> --content-id <cid>    # 生成公开链接，先确认（见 Workflow D）
supsub deepread show  --share-code <code> [--brief]    # 读别人分享的，无需登录
supsub deepread drop  --type <t> --content-id <cid>    # 移出本地队列
```

`drop` 只删本地缓存，服务端结果还在，之后 `get` 能重新拉回来且**不扣额度**——所以它不是危险操作，不用二次确认。

## Agent Usage Notes

- 解析数据统一用 `-o json`；响应都是 `{"success":true,"data":<payload>}`。
- **精读 ≠ 全文**。CLI 没有取文章原文的接口。用户要「原文」时给 `url` 让他自己打开，别拿精读结果冒充全文。
- **精读 ≠ 摘要**。只想知道「讲了啥」时，`sub contents` 里现成的 `summary` 就够了，**不要**为此花一次额度。用户明确想要「拆解 / 值不值得读 / 靠不靠谱 / 有没有干货」时才上精读。
- 一份精读结果约 4~6KB，**可以整份进上下文**；批量（>5 篇）时用 `--brief`，需要细节再按 `cachePath` 读单篇。
- 本地缓存目录 `~/.supsub/deepread/<账号>/`，一篇两个文件（`.json` 元数据 + `.md` 全文）。想在历史精读里找东西，直接 grep 这个目录比重新精读快也便宜。
- 本 skill **不负责**：浏览文章列表（→ `supsub-sub` / `supsub-focus`）、关键词搜文章（→ `supsub-search`）、标记已读（→ `supsub-unread`）。
- Exit codes：`0` OK（含 `pending` / `none`），`2` UNAUTHORIZED，`64` INVALID_ARGS（`--type` 非法、`--content-id` 为空、`--timeout` 越界），`10` 网络错误，`1` 业务错误（如无付费计划、额度用尽），`11` 服务端错误。
