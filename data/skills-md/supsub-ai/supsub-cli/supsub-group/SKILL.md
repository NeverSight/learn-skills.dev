---
name: supsub-group
version: 0.1.2
description: SupSub 订阅分组管理 —— 创建 / 重命名 / 删除分组，查看分组内订阅源（带未读数），把订阅源加入 / 移出分组。匹配「我的分组」「新建 / 创建一个分组」「把 XX 加到 YY 分组」「把 XX 从分组移出 / 移除」「YY 分组里有哪些订阅」「这个分组还有多少未读」「重命名分组」「删除分组」「整理订阅 / 给订阅分个类」。⚠️ 消歧：**分组（group）**是把已订阅的源收纳起来的"文件夹"，按 sourceId+sourceType 组织；**关注点（focus）**是 AI 按主题聚合的内容流（「我的关注点 / 我关注了哪些」→ supsub-focus）；订阅源本身的订阅 / 退订走 supsub-sub。删除分组不可逆（组内订阅源本身不受影响）。
---

# supsub-group Skill

「分组」（group）是订阅源的**文件夹**：把已订阅的源（公众号 `MP`、网站 `WEBSITE`、推特 `X` 等）收纳到自定义分组里，便于归类浏览。本 skill 负责分组的增删改查与成员管理。

> 与 `supsub-focus` 的区别：`group` 是**人工收纳**订阅源的文件夹（成员是源）；`focus` 是 **AI 按主题聚合**的内容流（成员是文章）。「把量子位放进 AI 分组」→ 本 skill；「我的关注点里有什么」→ supsub-focus。
> 与 `supsub-sub` 的区别：`sub` 管订阅关系本身（订阅/退订/看文章）；本 skill 只管"源放在哪个文件夹"。`sub add --group <gid>` 可在订阅时直接入组（见 supsub-sub）。

## Prerequisites

- 安装：`curl -fsSL https://raw.githubusercontent.com/SupSub-AI/supsub-cli/master/scripts/install.sh | bash`（native 安装，装到 `~/.local`、支持后台自动更新）；或包管理器 `npm i -g @supsub/cli` / `pnpm add -g @supsub/cli`
- 已登录：`supsub auth status` 显示 Authenticated（首次使用先 `supsub auth login`）
- **未授权（exit 2 / UNAUTHORIZED）时不要止步于「你未登录」**：直接运行 `supsub auth login` 为用户打开浏览器授权（命令会自动打开浏览器并阻塞等待授权，请用足够长的超时，如 10 分钟；用户只需在浏览器点确认，无需在终端输入任何内容），授权成功后重试原命令。无浏览器 / 无头环境再回退为提示用户 `SUPSUB_NO_BROWSER=1 supsub auth login`。

## Commands

### List groups（分组列表）

```
supsub group list
```

无参数。每行字段：`id`, `name`。

```bash
supsub group list
supsub group list -o json
```

JSON shape: `{"success":true,"data":[{"id":1063,"name":"AI 周报"}, ...]}`

> `id` 目前是数字，但请当作**不透明标识**原样回传（不要做数学运算/格式假设），后端保留改用字符串 ID 的可能。

---

### Create a group（创建分组）

```
supsub group add <name>
```

位置参数 `<name>` 为分组名称（空白名称报 `INVALID_ARGS`）。

```bash
supsub group add "AI 周报"
supsub group add 财经 -o json
```

JSON shape: `{"success":true,"data":{"id":1182,"name":"AI 周报"}}` —— 返回里直接带新分组 `id`，可立刻接 `add-sub` / `sub add --group` 使用（已实测）。

> ⚠️ **分组名不可重复**：已存在同名分组时报 `ResourceExists`（409 → exit `1`），**不会**返回已有分组的 id。
>
> 因此「把 X 订上并归到『效率』组里」这类请求的正确顺序是：**先 `group list` 找同名分组**，
> 命中就复用它的 `id`，没命中才 `group add`。上来就 `group add` 会在分组已存在时白白失败一次。
> 若 `group list` 没有该分组，直接建即可（建分组是无损操作，不用反问用户）——但**建之前顺带说一句
> 「『效率』组不存在，我新建一个」**，因为用户很可能只是把组名记错了。

---

### Rename a group（重命名分组）

```
supsub group rename --id <gid> --name <newName>
```

| Flag | Required | Description |
|------|----------|-------------|
| `--id` | yes | 分组 ID（来自 `group list`） |
| `--name` | yes | 新分组名称（非空） |

```bash
supsub group rename --id 1063 --name "AI 深度"
```

JSON shape: `{"success":true,"data":{"message":"分组已重命名"}}`

---

### Remove a group（删除分组）

```
supsub group remove --id <gid>
```

```bash
supsub group remove --id 1182
```

JSON shape: `{"success":true,"data":{"message":"已删除分组"}}`

> ⚠️ **破坏性且不可逆**：执行前必须向用户**二次确认**——复述分组名（从 `group list` 取），获得用户明确同意后才执行。组内订阅源本身不会被退订，只是失去这个文件夹。
>
> **CLI 不会再问一次**：`group remove` 没有交互式确认提示，一执行就删掉。确认只发生在你和用户之间。
> 若把命令交给用户自己执行，**不要说「CLI 会让你确认」**——如实说明它一跑就生效。

---

### List sources in a group（查看分组订阅源）

```
supsub group subs --id <gid> [--all] [--type <MP|WEBSITE|X|PODCAST|NEWSLETTER>]
```

| Flag | Default | Description |
|------|---------|-------------|
| `--id` | required | 分组 ID |
| `--all` | — | 显示**所有**订阅源（含未加入本分组的），带 `inGroup` 布尔列；不带时只显示组内成员 |
| `--type` | — (all) | 过滤类型；比 sub 命令多 `PODCAST`（播客）/ `NEWSLETTER`（通讯）两类（网页端可加入） |

字段：`sourceId`, `sourceType`, `name`, `img`, `description`, `inGroup`；**仅默认（组内成员）模式**每行额外带 `unreadCount`。

```bash
# 组内成员（带未读数）—— 回答「这个分组还有多少未读」
supsub group subs --id 1063

# 所有订阅源 + 是否在组（用于挑选要移入的源）
supsub group subs --id 1063 --all -o json

# 只看组内公众号
supsub group subs --id 1063 --type MP
```

JSON shape（默认）: `{"success":true,"data":[{"sourceType":"MP","sourceId":143,"name":"...","img":"...","description":"...","inGroup":true,"unreadCount":4}, ...]}`

> `--all` 模式后端**不返回** `unreadCount`；要未读数就用默认模式。

---

### Add a source to a group（订阅源入组）

```
supsub group add-sub --id <gid> --source-id <sid> --type <MP|WEBSITE|X>
```

| Flag | Required | Description |
|------|----------|-------------|
| `--id` | yes | 分组 ID（来自 `group list`） |
| `--source-id` | yes | 订阅源 ID（正整数，来自 `sub list` / `search`） |
| `--type` | yes | `MP` / `WEBSITE` / `X`（推特）——`PODCAST`/`NEWSLETTER` 不可经 CLI 加入 |

```bash
supsub group add-sub --id 1063 --source-id 25 --type MP
```

JSON shape: `{"success":true,"data":{"message":"已将订阅源加入分组"}}`

> **幂等**：源已在组中时返回 `"该订阅源已在分组中，无需重复添加"` 且 exit 0——这是成功不是错误，如实转告即可。
> **实现是读-改-写全量覆盖**（后端无原子移入/移出端点）：CLI 先读组内成员再整份写回。**不要并发编辑同一分组**（多个命令同时跑或与网页端同时操作会互相覆盖，last-write-wins）。

---

### Remove a source from a group（订阅源出组）

```
supsub group remove-sub --id <gid> --source-id <sid> --type <MP|WEBSITE|X>
```

Flag 同 `add-sub`。出组**不会退订**该源。

```bash
supsub group remove-sub --id 1063 --source-id 25 --type MP
```

JSON shape: `{"success":true,"data":{"message":"已将订阅源移出分组"}}`

> 幂等：源不在组中时返回 `"该订阅源不在分组中，无需移除"` 且 exit 0。并发警告同 `add-sub`。

---

## Agent Usage Notes

- 解析数据时统一用 `-o json`；所有 JSON 响应都是 `{"success":true,"data":<payload>}` 结构。
- `--id`（分组 ID）唯一来源是 `supsub group list`；`--source-id` 唯一来源是 `supsub sub list` / `supsub search`。用户报分组名时先 `group list` 找到对应 id。
- **`group remove` 执行前必须向用户二次确认**（复述分组名 → 明确同意 → 执行）；删除不可逆。
- `add-sub` / `remove-sub` 是**读-改-写全量覆盖**：勿并发操作同一分组；批量移入多个源时请**串行**逐个执行。
- 订阅新源时若已知目标分组，优先用 `sub add --source-id <id> --type <t> --group <gid>` 一步到位（见 supsub-sub），不必先订阅再 `add-sub`。
- 分组成员的 `sourceType` 可能出现 `PODCAST` / `NEWSLETTER`（网页端加入），`group subs --type` 可过滤它们；但 `add-sub` 只接受 `MP|WEBSITE|X`。
- **没有分组级标记已读命令**。用户说「把这个分组全部标记已读」时：先 `group subs` 列出组内源与各自 `unreadCount`，复述范围并获得确认，再逐个 `sub mark-read --source-id <sid> --type <t> --all`（每个源都不可逆）。也没有单篇已读——详见 `supsub-unread`。
- **本 skill 不负责**：订阅/退订源（→ `supsub-sub`）、关注点（→ `supsub-focus`）、未读工作流（→ `supsub-unread`）。
- Exit codes：`0` OK（含幂等提示），**`1` 业务错误（后端 4xx，如分组不存在 404 NotFound）**，`2` UNAUTHORIZED，`64` INVALID_ARGS（`--id` 空 / `--type` 非法 / `--source-id` 非正整数），`10` 网络错误，`11` 服务端错误（5xx）。
  > 按退出码分支时注意：`1` 和 `11` 不是一回事——`分组不存在` 这类业务失败是 `1`，`11` 只在后端 5xx 时出现。
