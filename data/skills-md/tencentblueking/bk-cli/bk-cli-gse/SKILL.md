---
name: bk-cli-gse
description: 当需要通过 `bk-cli gse` 查询 GSE Agent 状态或详情时使用。适合批量查询 Agent 运行状态的场景。
---

# bk-cli gse — GSE 管控平台能力使用说明

用于通过 `bk-cli gse` 调用蓝鲸 GSE 管控平台 API 的系统子命令。

CRITICAL — 开始前 MUST 先用 Read 工具读取 `../bk-cli-shared/SKILL.md`。共享 skill 负责认证、context、tenant、stage、dry-run、verbose、header/body 和通用请求规则；本 skill 只补充 `gse` 命令自己的语义与输入约定。

## 当前覆盖范围

当前 skill 覆盖两个高频命令：

- `list_agent_state`
- `list_agent_info`

## 输入约定

- `--agent_id_list` 使用逗号分隔的 CMDB `bk_agent_id` 列表，最多支持 1000 个
- 这里的 Agent ID 需要使用 CMDB 中的 `bk_agent_id` 字段格式，例如 `02000000000000000000000000000001`，不是 `cloud_id:ip` 或 `0:IP` 格式

## Commands

#### `list_agent_state`

```bash
bk-cli gse list_agent_state --agent_id_list 02000000000000000000000000000001,02000000000000000000000000000002
```

- 批量查询 Agent 运行状态
- 调用路径：`POST /api/v2/cluster/list_agent_state`

#### `list_agent_info`

```bash
bk-cli gse list_agent_info --agent_id_list 02000000000000000000000000000001,02000000000000000000000000000002
```

- 批量查询 Agent 详细信息
- 调用路径：`POST /api/v2/cluster/list_agent_info`
