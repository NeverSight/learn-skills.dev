---
name: supsub-focus
version: 0.1.4
description: SupSub 关注点（focus）管理 —— 列出我的关注点、查看某个关注点里聚合的内容/文章（按已读/未读筛选，支持翻页）、把整个关注点标记为已读、删除关注点。匹配「我的关注点」「关注点列表」「我关注了哪些」「我关注的内容」「看 X 关注点里有哪些内容/文章」「关注点 X 有哪些未读」「关注点还有多少没读」「这个关注点我看完了 / 把关注点标为已读」「删除关注点 X」。⚠️ 已读只有**整个关注点**一档（`mark-read --all`，不可逆）：文章没有「详情 / 阅读」这一步，故不支持单篇标记已读。⚠️ 也匹配**用主题名指代自己关注点**的浏览句式：「看一下最近 X 的内容」「X 最近有什么」—— 遇到这类请求先 `supsub focus list` 比对 X 是不是已有关注点的标题（包含匹配、忽略大小写），命中就用 `focus contents` 拉该关注点内容；若 X 同时命中订阅源名，把两边都列出来让用户选；两边都没命中则直接改用 supsub-search 执行全站搜索（**不要反问用户要不要搜**），**不要**默认当成全站关键词搜索。关注点是跨多来源（公众号 MP / 网站 WEBSITE / 推特 X）按主题聚合的内容流。⚠️ 动词判别：「关注 / 关注了 / 我关注了哪些 / 关注点」都归本 skill（focus）；只有「订阅 / 订阅了」才走 supsub-sub（订阅源）。不用于订阅源的增删查（走 supsub-sub），也不用于全文关键词搜索（走 supsub-search）。CLI 没有新增关注点的命令，删除不可逆。
---

# supsub-focus Skill

「关注点」（focus）是 SupSub 里按主题聚合的内容流：它跨多个来源（微信公众号 `MP`、网站 `WEBSITE`、推特 `X`）把同一主题的文章汇集到一起。本 skill 负责**查看**关注点列表、**浏览**某个关注点里的内容（区分已读/未读），以及**删除**关注点。

> 与 `supsub-sub` 的区别：`sub` 管理「订阅源」（一个具体的公众号/网站，以及其下文章）；`focus` 管理「主题聚合视图」（跨多个源的内容流）。两者不要混淆。
> 与 `supsub-search` 的区别：`search` 是按关键词做一次性全文检索；`focus` 是浏览既有的、持续更新的主题流。

## Prerequisites

- 安装：`curl -fsSL https://raw.githubusercontent.com/SupSub-AI/supsub-cli/master/scripts/install.sh | bash`（native 安装，装到 `~/.local`、支持后台自动更新）；或包管理器 `npm i -g @supsub/cli` / `pnpm add -g @supsub/cli`
- 已登录：`supsub auth status` 显示 Authenticated（首次使用先 `supsub auth login`）
- **未授权（exit 2 / UNAUTHORIZED）时不要止步于「你未登录」**：直接运行 `supsub auth login` 为用户打开浏览器授权（命令会自动打开浏览器并阻塞等待授权，请用足够长的超时，如 10 分钟；用户只需在浏览器点确认，无需在终端输入任何内容），授权成功后重试原命令。无浏览器 / 无头环境再回退为提示用户 `SUPSUB_NO_BROWSER=1 supsub auth login`。

## Commands

### List focuses（关注点列表）

```
supsub focus list
```

无参数。每行字段：`id`, `icon`(emoji), `title`, `unreadCount`。

```bash
# 列出全部关注点
supsub focus list

# JSON 输出
supsub focus list -o json
```

JSON shape: `{"success":true,"data":[{"id":42,"icon":"🤖","title":"...","unreadCount":3}, ...]}`

> **已读/未读**：每个关注点的 `unreadCount` 就是该关注点当前的未读条目数。用户问「我哪个关注点还有没读的 / 各关注点还剩多少没看」时，直接读这个字段，无需进 contents。

---

### Browse contents in a focus（查看关注点内容）

```
supsub focus contents --id <focusId> [--unread | --all] [--brief] [--page <n>] [--page-size <n>]
```

| Flag | Default | Description |
|------|---------|-------------|
| `--id` | required | 关注点 ID（正整数），来自 `supsub focus list` 的 `id` |
| `--unread` | (default) | 仅返回未读内容 |
| `--all` | — | 返回全部内容（已读 + 未读） |
| `--brief` | — | 精简输出：只留 `contentId` / `title` / `sourceType` / `sourceName` / `publishedAt(+Text)` / `isRead` |
| `--page` | 1 | 页码（正整数） |
| `--page-size` | 20 | 每页条数，1-100 |

> ⚠️ `--unread` 与 `--all` **互斥**：同时指定会抛 `INVALID_ARGS`。不传任何一个时，默认行为等价于 `--unread`。

**⚠️ 「最近」不等于「未读」**：「看一下最近 X 的内容」「X 关注点最近有什么」这类**按时间浏览**的请求用 **`--all`**，
把 `isRead` 当**标注**（「其中 N 条你还没看过」）而不是过滤条件；只有用户明说「未读 / 没看的 / 还剩多少没读」
才用默认。否则该关注点读完后会返回空数组，回复「没有内容」——而用户问的是「最近」，不是「没读的」。

关注点聚合多来源，故每行都带 `sourceType` / `sourceName`，便于看清这条内容来自哪个号/网站/推特。

每行字段：`contentId`, `url`, `title`, `coverImage`, `keywords[]`, `tags[]`, `summary`, `sourceType`, `sourceName`, `publishedAt`, `isRead`。

```bash
# 默认（仅未读）—— 等价于 --unread
supsub focus contents --id 42

# 全部内容（含已读）
supsub focus contents --id 42 --all

# 翻到第 2 页 / 一次多拿一些（上限 100）
supsub focus contents --id 42 --page 2
supsub focus contents --id 42 --page-size 100 -o json

# 全部 + JSON
supsub focus contents --id 42 --all -o json
```

JSON shape: `{"success":true,"data":[{"contentId":"...","url":"...","title":"...","coverImage":"...","keywords":[...],"tags":[...],"summary":"...","sourceType":"MP","sourceName":"...","publishedAt":<timestamp 或字符串>,"isRead":false}, ...]}`

> `publishedAt` 的原始形态随后端版本而异（Unix 秒数字 / `"YYYY-MM-DD HH:mm:ss"` 字符串），
> **不用自己兼容——直接读 CLI 补好的 `publishedAtText`**（恒为 `"YYYY-MM-DD HH:mm"`）。
> `sourceType` 可能是 `MP` / `WEBSITE` / `X`（推特）。
>
> **批量枚举一律加 `--brief`**：完整输出每条都带 `summary` / `keywords` / `tags`，100 条约 90KB，
> 会撑爆工具输出上限被迫落盘；`--brief` 同样 100 条约 14KB。只在需要给用户讲内容时才用完整输出。
>
> 翻页策略：浏览类请求只拉第 1 页并告知总量；「全部 / 统计 / 导出」类请求用 `--page-size 100` 自动循环翻页，不要逐页询问用户。详见 `supsub-unread`。

---

### Mark a focus as read（整个关注点标记已读）

```
supsub focus mark-read --id <focusId> --all
```

| Flag | Required | Description |
|------|----------|-------------|
| `--id` | yes | 关注点 ID（正整数） |
| `--all` | yes | 确认整个关注点全部标为已读（**不可逆**） |

> ⚠️ **只支持整个关注点已读，没有单篇已读。** 文章没有「详情 / 阅读」这一步，产生不了自然的单篇已读事件，所以 CLI 只保留用户明确表达的「这个关注点我看完了」。传 `--content-id` / `--type` / `--source-type` 会抛 `INVALID_ARGS`。用户说「把这篇标为已读」时如实说明不支持。
>
> ⚠️ **`--all` 必填且不可逆**（无 mark-as-unread）。执行前必须向用户**二次确认**：复述关注点标题 + 当前 `unreadCount`，获得明确同意后才执行。
>
> **CLI 不会再问一次**：这条命令（以及 `focus remove`）没有交互式确认提示，一执行就生效。若把命令交给用户自己在终端跑，
> **不要说「执行后 CLI 会提示确认」**——那是不存在的安全网。

```bash
# 整个关注点已读（需用户确认后执行）
supsub focus mark-read --id 42 --all -o json
```

JSON shape: `{"success":true,"data":{"message":"已标记该关注点全部内容为已读（不可逆）"}}`

---

### Remove a focus（删除关注点）

```
supsub focus remove --id <focusId>
```

| Flag | Required | Description |
|------|----------|-------------|
| `--id` | yes | 关注点 ID（正整数） |

```bash
supsub focus remove --id 42
supsub focus remove --id 42 -o json
```

JSON shape: `{"success":true,"data":{"message":"..."}}`

> ⚠️ **破坏性且不可逆**：删除后 CLI **没有任何新增关注点的命令**（无 `focus add`），删掉就建不回来。执行前务必向用户确认。

---

## 已读 / 未读（重点）

已读状态由**服务端维护**，CLI 既能读取也能标记（只能标为已读，**不能标回未读**）：

- `focus list` 每项的 `unreadCount` = 该关注点的未读条目数。这是判断「哪个关注点还有没看的」的最快入口。
- `focus contents` 默认（或显式 `--unread`）只返回未读条目；`--all` 返回全部（已读 + 未读）。
- `focus contents` 每条的 `isRead`（布尔）= 该条目是否已读：表格里渲染为 `read` 列（已读显示 `✓`，未读为空）。
- **标记已读用 `focus mark-read --all`**：只有「整个关注点已读」一档，没有单篇已读。
- **没有取消已读的命令**：标错了无法在 CLI 里恢复。`--all` 级操作不可逆，执行前必须向用户二次确认。
- 跨订阅源 + 关注点的未读概览与「清未读」工作流见 `supsub-unread`（`supsub unread` 一条命令看全）。

## Agent Usage Notes

- 解析数据时统一用 `-o json`；表格输出有截断、列宽限制，不适合做下游处理。
- 所有 JSON 响应都是 `{"success":true,"data":<payload>}` 结构（来自 `src/ui/output.ts`）。
- 拿 `focusId` 的唯一来源是 `supsub focus list` 的 `id`（正整数）；`--id` 非正整数会报 `INVALID_ARGS` (exit 64)，且不会发起请求。
- 用户问「这个关注点里都有哪些内容/文章」通常意味着 `--all`（含已读）；问「还有哪些没看 / 未读」用默认 `--unread`。
- `focus contents` 默认每页 20 条，用 `--page` / `--page-size`（上限 100）翻页取更早的内容。
- `focus mark-read` 只做整个关注点已读（单篇已读不支持：文章没有详情/阅读这一步）；**`--all` 必填且不可逆，执行前必须向用户二次确认**。
- **本 skill 不负责**：订阅源增删查（→ `supsub-sub`）、订阅分组（→ `supsub-group`）、跨源未读概览与清未读工作流（→ `supsub-unread`）、按关键词全文搜索（→ `supsub-search`）、发现新公众号（→ `supsub-mp`）。focus 没有 add。
- Exit codes：`0` OK，`2` UNAUTHORIZED，`64` INVALID_ARGS（`--id` / `--page` / `--page-size` 校验失败、`--all` 与 `--unread` 互斥、mark-read 未给 `--all` 或误传单篇参数），`1` 业务错误（后端 4xx，如关注点不存在），`10` 网络错误，`11` 服务端错误（5xx）。
