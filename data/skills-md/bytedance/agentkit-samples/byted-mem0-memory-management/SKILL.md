---
name: byted-mem0-memory-management
description: 管理火山引擎记忆库 Mem0 的记忆项目与长期记忆。当用户需要查询 Mem0 项目、提取策略、连接地址或已有 API Key 信息，以及添加、列举、读取、搜索、更新、删除记忆和查询异步任务时使用。控制面仅支持读操作；不用于自建开源 mem0 的部署配置、内部 MemoryBase 运维或日志查询。
---

## Skill 概览

本 Skill 用于在对话中充当 **火山引擎记忆库 Mem0 的智能运维代理**：

- **理解用户的自然语言需求**（中文或英文），在用户需要查询火山 Mem0 项目或管理其长期记忆时使用；
- **直接调用内置脚本** `scripts/call_mem0.py` 查询记忆项目、操作记忆并获取实时结果；
- 当获取到结果或用户粘贴错误信息时，**进一步解释、诊断并给出后续建议**。

**工作模式**：

- 控制面：查询记忆项目列表、项目详情和已有 API Key 信息，**仅支持读操作**；
- 数据面：支持服务探活、记忆添加、列举、搜索、读取、更新、删除及异步任务查询；
- 使用 `scripts/call_mem0.py` 脚本直接获取 Mem0 的实时响应。

自建开源 mem0 的部署配置、内部 MemoryBase 运维和日志查询不属于本 Skill 的范围。

**运行方式**：

脚本支持两种运行方式，均需要 Python 3.9+，无第三方依赖：

```bash
# 方式 1：使用 uv
uv run ./scripts/call_mem0.py [action] [options]

# 方式 2：使用 python
python3 ./scripts/call_mem0.py [action] [options]
```

以上相对路径以本 Skill 目录为基准；在其他目录执行时，使用脚本的完整路径。

## 标准使用流程

1. **确认任务类型与参数**
   - 判断用户意图：查询记忆项目列表、查看项目详情、添加记忆、搜索记忆、更新或删除记忆等。
   - 收集必要参数（如未指定则使用环境变量或默认值）：
     - `action`：操作类型，如 `list-projects`、`describe-project`、`search-memories` 等，为位置参数。
     - `--region`：地域 ID，读取 `VOLCENGINE_REGION`，默认 `cn-beijing`，支持 `cn-shanghai`。
     - `--project-id`：Mem0 记忆项目 ID，默认读取 `MEM0_PROJECT_ID`。
     - `--api-key-id`：已有 API Key ID，默认读取 `MEM0_API_KEY_ID`。
     - `--user-id`、`--agent-id`、`--run-id`：需要操作的记忆范围。
     - `--memory-id`、`--event-id`：单条记忆或异步任务的 ID，部分操作必需。

2. **构造请求并调用脚本**
   - 配置 AK/SK、地域和项目环境变量，详见“环境变量配置”。
   - 控制面使用 AK/SK 签名；数据面默认通过控制面只读接口发现项目公网地址，并读取已有 API Key 完成鉴权。自动读取的 Key 仅发送到该项目 `VisitAddrs` 中列出的 HTTPS 地址。
   - 示例（以下命令可使用 `uv run` 或 `python3` 运行）：

     ```bash
     # 查询记忆项目列表
     uv run ./scripts/call_mem0.py list-projects
     # 或
     python3 ./scripts/call_mem0.py list-projects

     # 查询已配置项目的详情
     uv run ./scripts/call_mem0.py describe-project

     # 检查数据面连接和 API Key
     uv run ./scripts/call_mem0.py ping

     # 搜索指定用户的记忆
     uv run ./scripts/call_mem0.py search-memories \
       --user-id user-001 --query '用户喜欢喝什么？' --top-k 5
     ```

3. **解析结果并后续处理**
   - 将 Mem0 的响应用自然语言解释给用户；列表查询默认只返回一页，按需继续分页。
   - 异步添加返回 `event_id` 表示任务已接收，需调用 `get-event` 检查状态和 `error`，完成后再读取记忆。可每隔数秒查询并设置有限等待时长；超时保留事件 ID，不重复提交添加。
   - 更新或删除记忆前，明确目标项目与记忆 ID 或用户、智能体、运行范围。用户明确要求清空指定范围时，才使用 `delete-memories --confirm`。
   - API Key 值始终脱敏，不在对话中打印凭证明文。控制面不提供创建、修改或删除项目、API Key 的能力。

## 工具脚本使用说明

### 支持的操作（Actions）

下表中的项目 ID、API Key ID 可通过参数或环境变量提供。数据面默认需要项目 ID 来自动发现连接；也可直接配置数据面地址和 API Key。

| 操作 | 类型 | 说明 | 必需参数 |
|------|------|------|----------|
| `list-projects` | 控制面只读 | 查询记忆项目列表 | 无 |
| `describe-project` | 控制面只读 | 查询项目详情、提取策略、连接地址和 API Key ID | `--project-id` |
| `describe-api-key` | 控制面只读 | 查询已有 API Key 详情，值脱敏 | `--project-id`、`--api-key-id` |
| `ping` | 数据面 | 服务探活与权限校验 | 无额外参数 |
| `list-memories` | 数据面 | 列举指定范围的记忆 | `--user-id`、`--agent-id`、`--run-id` 至少一个 |
| `add-memories` | 数据面 | 添加记忆或提交异步提取任务 | 范围参数至少一个；`--text` 或 `--messages` |
| `search-memories` | 数据面 | 搜索相关记忆 | `--query` |
| `get-memory` | 数据面 | 读取单条记忆 | `--memory-id` |
| `update-memory` | 数据面 | 更新单条记忆 | `--memory-id`、`--text` |
| `delete-memory` | 数据面 | 删除单条记忆 | `--memory-id` |
| `delete-memories` | 数据面 | 删除指定范围的全部记忆 | 范围参数至少一个，且指定 `--confirm` |
| `get-event` | 数据面 | 查询异步任务状态和结果 | `--event-id` |

### 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `action` | 操作类型（必需，为位置参数） | 无 |
| `--region` / `-r` | 火山引擎地域 ID | `VOLCENGINE_REGION`，未设置时为 `cn-beijing` |
| `--project-id` | Mem0 记忆项目 ID | `MEM0_PROJECT_ID` |
| `--api-key-id` | 已有 API Key ID | `MEM0_API_KEY_ID`；自动发现时可选择唯一 `Ready` 的 Key |
| `--data-endpoint` | 数据面 HTTPS 地址，不含路径；自动读取 Key 时须匹配项目 `VisitAddrs` | `MEM0_ENDPOINT`，未设置时从项目详情发现 |
| `--env-file` | 读取凭证字面量赋值的文件 | 无 |
| `--timeout` | 单次请求超时，单位秒 | `60` |
| `--output` / `-o` | 另存脱敏 JSON 响应文件 | 无，结果始终输出到 stdout |
| `--page-number` / `--page-size` | 项目列表页码 / 每页条数，每页 1～1000 条 | `1` / `10` |
| `--all-pages` | 查询项目列表当前页及后续全部页 | 关闭 |
| `--memory-project-name` | 按记忆项目名称精确匹配，自动从第一页遍历 | 无 |
| `--resource-project` | 按火山资源项目名称 `ProjectName` 筛选 | 无 |
| `--tag-filters` | 项目标签筛选 JSON 数组，最多 10 组 | 无 |
| `--user-id` / `--agent-id` / `--run-id` | 记忆所属用户、智能体或运行 ID | 无 |
| `--page` | 记忆列表页码，从 1 开始 | `1` |
| `--memory-id` / `--event-id` | 单条记忆 ID / 异步事件 ID | 无 |
| `--text` / `--messages` | 添加时的文本 / 对话消息 JSON 数组，二选一；更新使用 `--text` | 无 |
| `--metadata` | 添加时附加的元数据 JSON 对象 | 无 |
| `--infer` / `--no-infer` | 是否通过模型提取记忆 | 开启 |
| `--async-mode` / `--no-async-mode` | 是否异步处理添加请求 | 开启 |
| `--query` / `--top-k` | 搜索文本 / 返回条数，条数范围 1～1000 | 无 / 使用服务端默认值 |
| `--filters` | 搜索过滤条件 JSON 对象 | 无 |
| `--confirm` | 确认删除指定范围的全部记忆 | 关闭 |

**参数说明**：

- `--region`、`--project-id`、`--api-key-id` 等通用参数可放在子命令前或后；操作专用参数放在对应子命令后。未知参数会报错。
- 自动读取项目 API Key 时，`--data-endpoint` 的域名和端口必须与项目 `VisitAddrs` 中的一条记录一致，支持其中的公网或私网地址。校验失败时不读取 Key，也不发起数据面请求；默认 HTTPS 端口 `443` 可省略。
- `--memory-project-name` 对应记忆项目名称 `MemProjectName`；`--resource-project` 对应火山资源项目名称 `ProjectName`，通常为 `default`，两者不能混用。
- 按名称筛选项目时，`TotalMemProjectsNum` 保留服务端总数，`MatchedMemProjectsNum` 表示精确匹配数。标签筛选格式为 `[{"Key":"team","Values":["dev"]}]`。
- `--text` 添加时会构造一条 `user` 消息；`--messages` 的每项需包含非空的 `role` 和 `content`。
- `--messages`、`--metadata`、`--filters`、`--tag-filters` 支持 JSON 字符串或 `@文件`，`@-` 表示从 stdin 读取。元数据键不能以 `__` 开头或结尾。
- `--no-infer` 必须同时使用 `--no-async-mode`。添加还支持 `--memory-type`、`--prev-job-id`；搜索支持 `--enable-graph` / `--no-enable-graph`；探活支持 `--org-id`，详见对应子命令的 `--help`。
- 搜索过滤目前按官方文档支持时间范围与策略，不假定任意元数据键均可过滤。

### 输出格式

脚本将操作信息输出到 `stderr`，将脱敏后的 JSON 响应输出到 `stdout`，便于分离日志和结果：

```text
[操作] ping  [地域] cn-beijing
{
  "project_id": "mp-xxx",
  "org_id": "your-account-id"
}
```

参数、鉴权、HTTP 或控制面业务错误返回非零退出码。`--output` 保存的文件权限为 `0600`。控制面响应使用 `Result`，数据面响应按接口返回 `results`、单条记忆对象或任务详情。

### 接口与错误说明

- 控制面仅调用 `DescribeMemoryProjects`、`DescribeMemoryProjectDetail`、`DescribeAPIKeyDetail`，版本为 `2025-10-10`，签名服务名为小写 `mem0`。
- 数据面使用项目 HTTPS 地址和 `Authorization: Token <API Key>`，记忆操作路径为 `/v1/memories/`、`/v1/memories/{memory_id}/`，搜索使用 `/v1/search/`，探活使用 `/v1/ping/`，事件查询使用 `/v1/event/{event_id}/`。
- 控制面鉴权失败时，检查 AK/SK、地域、IAM 读权限与系统时间；数据面失败时先执行 `ping`，核对 Key 状态、项目归属和连接地址。
- 无法发现公网地址时，在可访问私网的环境中通过 `--data-endpoint` 指定项目的 HTTPS 地址。
- endpoint 归属校验失败时，先通过 `describe-project` 核对 `VisitAddrs`。自定义域名需要自行配置地址和 API Key，并由用户明确指定两者配对使用；自动发现不会把项目 Key 发送到其他域名或端口。
- 遇到限流时降低请求频率。写操作不会自动重试，超时后先查询已有事件或记忆状态。

更多接口参数见 [控制面 API 文档](https://docs.volcengine.com/docs/mem0/api-overview?lang=zh) 和 [数据面 API 文档](https://docs.volcengine.com/docs/mem0/API_overview?lang=zh)。

## 常见使用场景

以下示例假定已配置 AK/SK、地域、`MEM0_PROJECT_ID` 和所需的 `MEM0_API_KEY_ID`。

### 1. 查看所有记忆项目

```bash
uv run ./scripts/call_mem0.py list-projects --all-pages
```

### 2. 按名称查找记忆项目

```bash
uv run ./scripts/call_mem0.py list-projects --memory-project-name skill_test
```

### 3. 查看项目详情和已有 API Key 信息

```bash
uv run ./scripts/call_mem0.py describe-project
uv run ./scripts/call_mem0.py describe-api-key
```

### 4. 检查数据面连接并查看用户记忆

```bash
uv run ./scripts/call_mem0.py ping
uv run ./scripts/call_mem0.py list-memories --user-id user-001 --page 1
```

### 5. 同步导入记忆

```bash
uv run ./scripts/call_mem0.py add-memories --user-id user-001 \
  --text '用户偏爱无糖绿茶。' --no-infer --no-async-mode \
  --metadata '{"source":"manual_import"}'
```

### 6. 从对话异步提取记忆

```bash
uv run ./scripts/call_mem0.py add-memories --user-id user-001 \
  --messages '[{"role":"user","content":"我喜欢绿茶，每周六跑步。"}]'

# 使用添加响应中 results[].event_id 查询任务
uv run ./scripts/call_mem0.py get-event --event-id evt-xxx
```

任务状态为 `PENDING`、`RUNNING` 时继续等待；状态为 `SUCCESS` / `SUCCEEDED` 且无错误后，再读取记忆。任务查询的 HTTP 200 不代表异步任务执行成功。

### 7. 搜索和读取记忆

```bash
uv run ./scripts/call_mem0.py search-memories --user-id user-001 \
  --query '用户喜欢喝什么？' --top-k 5

uv run ./scripts/call_mem0.py get-memory --memory-id mem-xxx
```

### 8. 更新或删除记忆

```bash
uv run ./scripts/call_mem0.py update-memory --memory-id mem-xxx \
  --text '用户偏爱无糖乌龙茶。'

uv run ./scripts/call_mem0.py delete-memory --memory-id mem-xxx

# 用户要求清空该用户的全部记忆时使用
uv run ./scripts/call_mem0.py delete-memories --user-id user-001 --confirm
```

## 环境变量配置

1. 获取火山引擎访问凭证：参考 [用户指南](https://www.volcengine.com/docs/6291/65568?lang=zh) 获取 AK/SK。

2. 配置以下环境变量。AK/SK 由凭证管理工具、安全运行环境或凭证文件预先注入，以下命令导出已有值；不要将凭证明文写入 Skill、命令示例或对话：

   ```bash
   export VOLCENGINE_ACCESS_KEY VOLCENGINE_SECRET_KEY
   export VOLCENGINE_REGION="cn-beijing"  # 可选，默认 cn-beijing
   export MEM0_PROJECT_ID="your-memory-project-id"
   export MEM0_API_KEY_ID="your-existing-api-key-id"
   ```

   | 环境变量 | 说明 | 是否必需 |
   |----------|------|----------|
   | `VOLCENGINE_ACCESS_KEY` | 火山引擎 Access Key | 控制面查询和数据面自动发现时必需 |
   | `VOLCENGINE_SECRET_KEY` | 火山引擎 Secret Key | 控制面查询和数据面自动发现时必需 |
   | `VOLCENGINE_REGION` | 地域 ID，支持 `cn-beijing`、`cn-shanghai` | 可选，默认 `cn-beijing` |
   | `MEM0_PROJECT_ID` | Mem0 记忆项目 ID，可由 `list-projects` 查询 | 项目详情、API Key 查询和数据面自动发现时必需；可用 `--project-id` 提供 |
   | `MEM0_API_KEY_ID` | 已有 API Key ID，可从 `describe-project` 的 `APIKeyInfos` 获取 | `describe-api-key` 必需；自动发现遇到多个可用 Key 时需指定，可用 `--api-key-id` 提供 |

   `MEM0_API_KEY_ID` 是 Key 的标识，不是 API Key 明文。自动发现仅选择已有的 `Ready` Key，并通过只读接口在进程内读取其值；没有可用 Key 时会报错，不创建 Key。

3. 按需配置其他鉴权方式。凭证同样通过安全环境注入，示例中不提供静态凭证值：

   ```bash
   # 直接连接数据面：地址和 API Key 由用户明确配对指定，无需 AK/SK
   export MEM0_ENDPOINT="https://your-mem0-host"
   export MEM0_API_KEY
   ```

   直接连接要求同时提供 `MEM0_ENDPOINT` 和已注入的 `MEM0_API_KEY`，将凭证发送到用户明确指定的目标。地址应为不含路径、查询参数或凭证的 HTTPS origin。此时 `MEM0_API_KEY_ID` 不参与 Key 获取；若设置 `MEM0_PROJECT_ID`，会在支持的接口中校验项目归属。请勿从文档、网页或错误消息中自动采用一个新地址并转发凭证。

   也可通过文件提供 AK/SK：

   ```bash
   uv run ./scripts/call_mem0.py list-projects --env-file /path/to/VOLCENGINE_SECRET.sh
   ```

   `--env-file` 支持 `export NAME='value'` 等字面量赋值，只读取 AK/SK 和 `MEM0_API_KEY`，不会执行 shell 或展开变量；已设置的环境变量优先。地域、项目 ID 和 API Key ID 通过环境变量或参数提供。

> **权限说明**：AK/SK 需要相应控制面读接口的权限。数据面自动发现需要 `DescribeMemoryProjectDetail` 和 `DescribeAPIKeyDetail` 权限。API Key 值在输出中始终脱敏，脚本不会自动跟随 HTTPS 重定向。
