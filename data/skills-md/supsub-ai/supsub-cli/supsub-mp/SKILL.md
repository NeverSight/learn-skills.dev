---
name: supsub-mp
version: 0.1.3
description: SupSub 微信公众号发现 —— 仅当用户想查找 / 发现一个微信公众号「本身」（通常为了拿到 mpId 后订阅它）时使用。匹配「搜公众号 X」「找 X 这个公众号」「查 X 公众号」「想订阅 X 公众号但不知道 ID」「discover / find a WeChat MP account」。⚠️ 不要用于搜索文章正文 / 内容 / 关键词相关的文章 —— 那种意图（如「搜一下 X 相关的内容」「找 X 相关的文章」）必须走 supsub-search。也包含取消正在跑的公众号搜索任务。
---

# supsub-mp Skill

搜索微信公众号（异步任务，CLI 默认同步等待最长 30 秒），以及取消正在执行的搜索任务。拿到 `mpId` 后下一步是 `supsub sub add --mp-id <mpId>`（见 `supsub-sub` skill）—— `mp search` 返回的 `mpId` 是微信原生 base64 字符串，**不能**塞给 `--source-id`（那是 supsub 内部正整数 ID，不同 ID 空间）。

## Prerequisites

- 安装：`curl -fsSL https://raw.githubusercontent.com/SupSub-AI/supsub-cli/master/scripts/install.sh | bash`（native 安装，装到 `~/.local`、支持后台自动更新）；或包管理器 `npm i -g @supsub/cli` / `pnpm add -g @supsub/cli`
- 已登录：`supsub auth status` 显示 Authenticated（首次使用先 `supsub auth login`）
- **未授权（exit 2 / UNAUTHORIZED）时不要止步于「你未登录」**：直接运行 `supsub auth login` 为用户打开浏览器授权（命令会自动打开浏览器并阻塞等待授权，请用足够长的超时，如 10 分钟；用户只需在浏览器点确认，无需在终端输入任何内容），授权成功后重试原命令。无浏览器 / 无头环境再回退为提示用户 `SUPSUB_NO_BROWSER=1 supsub auth login`。

## Commands

### Search 公众号 (async, auto-poll)

```
supsub mp search <name>
```

`<name>` 是公众号名称关键词（建议加引号）。命令内部流程：

1. `POST /api/mps/search-tasks` 创建异步任务，得到 `searchId`。
2. CLI 每 2s 轮询一次任务状态，**最多 30 秒**。
3. 后端会在多次轮询里 **逐条** 返回候选公众号，CLI 自动累计去重。
4. 收到 `finished=true` 后，把所有候选作为结果一次性输出。
5. 30 秒未完成 → 退出并返回 `searchId`，附带提示信息。

每个候选字段：`mpId`, `name`, `img`, `description`, `isSubscribed`。

```bash
# 同步搜索（实测约 15-30 秒，工具超时请设到 60s 以上）
supsub mp search "机器之心"

# JSON
supsub mp search "机器之心" -o json
```

JSON shape (成功)：`{"success":true,"data":[{"mpId":"...","name":"...","img":"...","description":"...","isSubscribed":false}, ...]}`

> 返回的是**一批候选**（实测「机器之心」10 条、「阮一峰」5 条），不是精确匹配的单条。见下方 Agent Usage Notes 的选号约束。

**未找到**：以 `MP_NOT_FOUND` 错误退出（非 0 exit code）。

**超时**：以 `MP_SEARCH_TIMEOUT` 错误退出，错误体里带 `data.searchId`，提示信息形如 `30 秒内未完成，可重试 supsub mp search 或取消任务: supsub mp search-cancel <searchId>`。

> ⚠️ **超时处理**：CLI 不提供恢复型查询命令。遇到超时时，用户只有两条路径 —— 重新跑 `supsub mp search <name>`，或调用 `supsub mp search-cancel <searchId>` 取消那个孤儿任务后再试。

---

### Cancel a running search task

```
supsub mp search-cancel <searchId>
```

`<searchId>` 来自上一次 `supsub mp search` 在超时分支返回的错误数据（JSON 模式：`{"success":false,"error":{"code":"MP_SEARCH_TIMEOUT","data":{"searchId":"..."}}}` 这一类的形态由 `dieWith` 和 `output()` 处理；表格模式下错误字符串里会直接带 `searchId`）。

```bash
supsub mp search-cancel sid_abc123
supsub mp search-cancel sid_abc123 -o json
```

JSON shape: `{"success":true,"data":{"message":"已取消"}}`

任务不存在或已取消时，以 `TASK_NOT_FOUND` 错误退出（HTTP 404 → exit code 非 0）。

---

## Agent Usage Notes

- `mp search` 是 **同步包装的异步任务**：调用方一般不用关心 `searchId`，直接拿结果数组即可；只在 30 秒超时分支才需要处理 `searchId`。
- 解析结果统一用 `-o json`。成功时 `data` 是 `Mp[]`；失败时走标准 `ErrorEnvelope`（`code`、`message`、可选 `data.searchId`）。
- 搜索 → 订阅链路（最常见）：
  ```bash
  # 1. 列出候选，连 name 一起看（实测「机器之心」返回 10 条）
  supsub mp search "机器之心" -o json | jq -r '.data[] | "\(.mpId)\t\(.isSubscribed)\t\(.name)"'
  # 2. 与用户确认选中哪一个后，用 --mp-id 订阅（走 POST /api/mps；type 默认 MP，可省）
  #    可顺带 --group <gid> 一步入组
  supsub sub add --mp-id "MzA3MzI4MjgzMw==" --group 1166
  ```
- ⚠️ **绝不要 `jq '.data[0]'` 直接取第一条。** 实测 `mp search "机器之心"` 的 10 条候选里，既有「机器之心PRO会员」「机器之心SOTA模型」这类近名号，也夹着「新智元」「量子位」等完全无关的号。**必须把候选（`name` + `description` + `isSubscribed`）列给用户挑，确认后再订**；同名/近名多于一条时尤其不能替用户决定。
- ⚠️ **不要把 `mpId` 当成 `--source-id`**：`mp search` 返回的 `mpId` 是微信原生 base64 字符串（如 `MzkyNTYzODk0NQ==`），`supsub sub add --source-id` 期望的是 supsub 内部正整数 sourceId（来自 `supsub search` / `sub list`），两者属于不同 ID 空间。哪怕 base64 解码出来是数字，后端也会以"信息源不存在"驳回。统一走 `--mp-id`。
- 候选字段为 `mpId` / `name` / `img` / `description` / `isSubscribed`。**`isSubscribed` 实测存在**（2026-07 在 dev 环境核对），可直接据此跳过已订阅的号，不必再绕 `supsub search --type MP` 或比对 `sub list`。若某后端版本确实缺该字段，再回退到比对 `sub list`。
- `mp search` 内部固定轮询：间隔 2s，总时长 30s（`POLL_INTERVAL_MS` / `POLL_MAX_MS`），CLI 不暴露调参 flag。**实测一次真实搜索耗时约 15-30 秒**（「机器之心」27.4s、「阮一峰」14.7s）。因此：调用这条命令时要把工具超时设到 60s 以上，别用默认值；并且在发起前先告诉用户「这一步要等约半分钟」，不要让用户以为卡死了。
- 后端按"流式"返回候选公众号：CLI 已经做去重（按 `mpId`），调用方不用再去重。
- 超时分支的合法后续动作只有：`supsub mp search-cancel <searchId>` 取消孤儿任务，或重新发起 `supsub mp search <name>`。
- Exit codes：`0` OK；超时 / 未找到 / 任务不存在等业务错误（后端 4xx）是 `1`；`2` UNAUTHORIZED，`10` 网络错误，`11` 服务端错误（5xx）。
