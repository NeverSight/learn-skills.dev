---
name: bk-cli-cmdb
description: 当需要通过 `bk-cli cmdb` 使用 CMDB 相关系统子命令，或在 `cmdb` 子命令与 `bk-cli api bk-cmdb ...` 之间做选择时使用。尤其适合查询业务、拓扑、主机关系、主机转移，或排查 CMDB open API 请求构造是否正确的场景。
---

# bk-cli cmdb — CMDB 能力使用说明

用于通过 `bk-cli cmdb` 调用 CMDB open API 的高频系统子命令。

CRITICAL — 开始前 MUST 先用 Read 工具读取 `../bk-cli-shared/SKILL.md`。共享 skill 负责认证、context、tenant、stage、dry-run、verbose、header/body 和通用请求规则；本 skill 只补充 `cmdb` 命令自己的语义与输入约定。

## 当前覆盖范围

当前 skill 覆盖这些高频 `cmdb` 命令：

- `get_biz_internal_module`
- `search_business`
- `search_set`
- `create_set`
- `search_module`
- `create_module`
- `list_biz_hosts_all`
- `list_biz_hosts`
- `list_hosts_without_biz`
- `find_host_biz_relations`
- `list_biz_hosts_topo`
- `transfer_host_module`
- `transfer_host_across_biz`
- `transfer_host_to_idle_module`
- `transfer_host_to_fault_module`
- `transfer_host_to_recycle_module`
- `transfer_host_to_resource_pool`
- `list_resource_pool_hosts`
- `delete_host`

后续如果新增更多 `cmdb` 子命令，应继续追加到本 skill 的 `## Commands` 章节，而不是拆成新的单命令 skill。

## 推荐工作流

1. 先确认目标是否已经有现成 `cmdb` 子命令。
2. 如果已有现成子命令，优先使用该命令，而不是直接退回原始 `bk-cli api`。
3. 首次调用或排障时，优先先加 `--dry-run` 看最终 URL、headers 和 body。
4. 如果现成子命令还不能覆盖你的目标接口，再退回 `bk-cli api bk-cmdb ...`。

## 输入约定

### 通用规则

- 大多数 `cmdb` 命令都支持 `--stage`、`--header`、`--body`；`list_biz_hosts_all` 例外，不暴露 `--body`。
- 当显式传入 `--body '<json>'` 时，请求会以该 JSON 为准，不再使用命令自带的默认请求内容。
- 这些 `cmdb` 命令通常要求可满足 app+user 的凭据；若当前 context 使用 `access_token`，也可满足非空认证要求。

### CSV 列表参数

当前 `cmdb` 的列表型输入统一优先使用 CSV 风格 flags：

- `--bk_biz_ids 1,2,3`
- `--bk_host_ids 100,200`
- `--bk_module_ids 20,30`
- `--fields bk_host_id,bk_host_innerip`

### `--host_ips` 规则

- 形态一：`10.0.0.1`
- 形态二：`27:10.0.0.2`
- 含义：`cloud_id:ip`；未写前缀时默认 `cloud_id=0`
- 只要有一个非法项，命令会直接报错，不会静默跳过

## Commands

### 业务与拓扑

#### `search_business`

```bash
bk-cli cmdb search_business [--bk_biz_id <id> | --bk_biz_ids <id,id,...>] [flags]
```

- 未显式传 `--body` 时，必须二选一提供 `--bk_biz_id` 或 `--bk_biz_ids`
- 默认 `--fields bk_biz_id,bk_biz_name,bk_biz_maintainer,bk_biz_productor`
- 默认 `--limit 500`
- 默认 `--supplier_account 0`
- 调用路径：`POST /api/v3/open/biz/search/{supplier_account}/`

#### `get_biz_internal_module`

```bash
bk-cli cmdb get_biz_internal_module --bk_biz_id <id> [--supplier_account 0]
```

- 获取业务内置模块（空闲机 / 故障机 / 待回收）
- 调用路径：`GET /api/v3/open/topo/internal/{supplier_account}/{bk_biz_id}`

### 集群与模块

#### `search_set`

```bash
bk-cli cmdb search_set --bk_biz_id <id> [flags]
```

- 默认 `--fields bk_set_id,bk_set_name`
- 默认 `--limit 500`
- 可选过滤：`--bk_set_name`、`--bk_set_id`
- 调用路径：`POST /api/v3/open/set/search/{supplier_account}/{bk_biz_id}`

#### `create_set`

```bash
bk-cli cmdb create_set --bk_biz_id <id> --bk_set_name <name> [flags]
```

- 默认 `bk_parent_id = bk_biz_id`
- 默认 `set_template_id = 0`
- 固定发送 `default = 0`
- 可选字段：`--bk_set_env`、`--bk_service_status`、`--bk_set_desc`、`--bk_capacity`
- 调用路径：`POST /api/v3/open/set/{bk_biz_id}`

#### `search_module`

```bash
bk-cli cmdb search_module --bk_biz_id <id> --bk_set_id <id> [flags]
```

- 默认 `--fields bk_module_id,bk_module_name`
- 默认 `--limit 500`
- 可选过滤：`--bk_module_name`、`--bk_module_id`
- 调用路径：`POST /api/v3/open/module/search/{supplier_account}/{bk_biz_id}/{bk_set_id}`

#### `create_module`

```bash
bk-cli cmdb create_module --bk_biz_id <id> --bk_set_id <id> --bk_module_name <name> [flags]
```

- 默认 `bk_parent_id = bk_set_id`
- 可选字段：`--bk_module_type`、`--operator`、`--bk_bak_operator`、`--service_template_id`、`--service_category_id`
- 调用路径：`POST /api/v3/open/module/{bk_biz_id}/{bk_set_id}`

### 主机查询

#### `list_biz_hosts_all`

```bash
bk-cli cmdb list_biz_hosts_all --bk_biz_id <id> [--bk_set_id <id>] [--bk_module_id <id>] [--page_limit 500]
```

- 命令会自动循环拉取所有分页结果并聚合返回
- 不暴露 `--body`
- dry-run 只预览第一页请求，并在 `data.pagination` 里补充分页元数据
- 调用路径：`POST /api/v3/open/hosts/app/{bk_biz_id}/list_hosts`

#### `list_biz_hosts`

```bash
bk-cli cmdb list_biz_hosts --bk_biz_id <id> [--host_ips 10.0.0.1,27:10.0.0.2]
```

- 固定字段：`bk_host_id,bk_host_innerip,bk_cloud_id,bk_host_name`
- `--host_ips` 用于按 IP 过滤主机
- 调用路径：`POST /api/v3/open/hosts/app/{bk_biz_id}/list_hosts`

#### `list_hosts_without_biz`

```bash
bk-cli cmdb list_hosts_without_biz [--host_ips 10.0.0.1,27:10.0.0.2]
```

- 查询所有业务范围内的主机
- 固定字段：`bk_host_id,bk_host_innerip,bk_cloud_id,bk_host_name,operator,bk_bak_operator`
- 调用路径：`POST /api/v3/open/hosts/list_hosts_without_app`

#### `find_host_biz_relations`

```bash
bk-cli cmdb find_host_biz_relations --bk_host_ids 1,2,3
```

- 查询主机与业务 / 集群 / 模块关系
- 调用路径：`POST /api/v3/open/hosts/modules/read`
- 如果上游 `data` 不是 list，CLI 会规范化输出为空数组 `[]`

#### `list_biz_hosts_topo`

```bash
bk-cli cmdb list_biz_hosts_topo --bk_biz_id <id> [--host_ips 10.0.0.1]
```

- 查询业务主机及拓扑信息
- 固定字段：`bk_host_id,bk_host_innerip,bk_cloud_id`
- 调用路径：`POST /api/v3/open/hosts/app/{bk_biz_id}/list_hosts_topo`

#### `list_resource_pool_hosts`

```bash
bk-cli cmdb list_resource_pool_hosts [flags]
```

- 可选：`--host_ips`、`--fields`、`--start`、`--limit`
- 固定分页排序：`page.sort = bk_host_id`
- 调用路径：`POST /api/v3/open/hosts/list_resource_pool_hosts`

### 主机转移与删除

#### `transfer_host_module`

```bash
bk-cli cmdb transfer_host_module --bk_biz_id <id> --bk_host_ids 1,2 --bk_module_ids 20,30 [--is_increment]
```

- 业务内主机转模块
- 调用路径：`POST /api/v3/open/hosts/modules`

#### `transfer_host_across_biz`

```bash
bk-cli cmdb transfer_host_across_biz --src_bk_biz_id <id> --dst_bk_biz_id <id> --bk_host_ids 1,2 --bk_module_id 20
```

- 跨业务转主机
- 调用路径：`POST /api/v3/open/hosts/modules/across/biz`

#### `transfer_host_to_idle_module`

```bash
bk-cli cmdb transfer_host_to_idle_module --bk_biz_id <id> --bk_host_ids 1,2
```

- 调用路径：`POST /api/v3/open/hosts/modules/idle`

#### `transfer_host_to_fault_module`

```bash
bk-cli cmdb transfer_host_to_fault_module --bk_biz_id <id> --bk_host_ids 1,2
```

- 调用路径：`POST /api/v3/open/hosts/modules/fault`

#### `transfer_host_to_recycle_module`

```bash
bk-cli cmdb transfer_host_to_recycle_module --bk_biz_id <id> --bk_host_ids 1,2
```

- 调用路径：`POST /api/v3/open/hosts/modules/recycle`

#### `transfer_host_to_resource_pool`

```bash
bk-cli cmdb transfer_host_to_resource_pool --bk_biz_id <id> --bk_host_ids 1,2 [--bk_module_id 50]
```

- 上交主机到资源池
- 调用路径：`POST /api/v3/open/hosts/modules/resource`

#### `delete_host`

```bash
bk-cli cmdb delete_host --bk_host_ids 100,200
```

- 删除资源池中的主机
- 调用路径：`DELETE /api/v3/open/hosts/batch`
- 请求会按接口要求发送 `bk_host_id` 的逗号分隔字符串，例如 `100,200`

## 例子

```bash
# 先看 dry-run
bk-cli cmdb search_set --bk_biz_id 2 --bk_set_name web --dry-run

# 聚合业务下所有主机
bk-cli cmdb list_biz_hosts_all --bk_biz_id 2 --page_limit 200

# 只查指定云区域和 IP 的主机
bk-cli cmdb list_biz_hosts --bk_biz_id 2 --host_ips 0:10.0.0.1,27:10.0.0.2

# 把主机批量转到指定模块
bk-cli cmdb transfer_host_module \
  --bk_biz_id 2 \
  --bk_host_ids 1,2 \
  --bk_module_ids 20,30
```

## 什么时候退回 `bk-cli api`

下面这些情况更适合直接用原始 API：

- 目标接口还没有对应 `cmdb` 子命令
- 需要完全自定义 query/body，而不想受现成 flags 语义约束
- 需要先验证完整 method/path/body/header，再逐步收敛成高层命令

示例：

```bash
bk-cli api bk-cmdb POST /api/v3/open/hosts/modules \
  --body '{"bk_biz_id":2,"bk_host_id":[1,2],"bk_module_id":[20],"is_increment":false}' \
  --dry-run
```

## 常见错误

| 错误表现 | 常见原因 | 建议 |
|---------|---------|------|
| `one of bk_biz_id or bk_biz_ids is required when --body is not provided` | `search_business` 未传 `--body`，同时也没传 `--bk_biz_id` / `--bk_biz_ids` | 补一个业务过滤条件，或改为显式传 `--body` |
| `host_ips contains an invalid host entry` | `--host_ips` 里有非法 token | 改成 `10.0.0.1,27:10.0.0.2` 这种格式 |
| `bk_host_ids must be a comma-separated list of integers` | `--bk_host_ids` 含空值、非数字或负数 | 改成 `1,2,3` 这种格式 |
| `supplier_account cannot be empty` | `--supplier_account` 为空字符串 | 使用 `0` 或明确的 supplier account |
| 鉴权失败 / forbidden | 凭据不满足 open API 认证要求，或应用缺少权限 | 先看 shared skill 的认证规则，再核对当前 context 的凭据和权限 |
