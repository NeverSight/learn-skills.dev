---
name: bk-cli-job
description: 当需要通过 `bk-cli job` 使用作业平台相关系统子命令时使用。适合快速执行脚本、分发文件、查询作业状态和执行日志的场景。
---

# bk-cli job — 作业平台能力使用说明

用于通过 `bk-cli job` 调用蓝鲸作业平台（BK-JOB）API 的系统子命令。

CRITICAL — 开始前 MUST 先用 Read 工具读取 `../bk-cli-shared/SKILL.md`。共享 skill 负责认证、context、tenant、stage、dry-run、verbose、header/body 和通用请求规则；本 skill 只补充 `job` 命令自己的语义与输入约定。

## 当前覆盖范围

当前 skill 覆盖这些常用命令：

- `get_job_instance_status`
- `get_job_instance_ip_log`
- `fast_transfer_file`
- `push_config_file`
- `fast_execute_script`

## Commands

### 查询类

#### `get_job_instance_status`

```bash
bk-cli job get_job_instance_status --bk_biz_id 2 --job_instance_id 100
bk-cli job get_job_instance_status --bk_biz_id 2 --job_instance_id 100 --return_ip_result
```

- 查询作业实例执行状态
- 调用路径：`GET /api/v3/get_job_instance_status`

#### `get_job_instance_ip_log`

```bash
bk-cli job get_job_instance_ip_log --bk_biz_id 2 --job_instance_id 100 --step_instance_id 200 --bk_cloud_id 0 --ip 10.0.0.1
```

- 查询某台主机的作业执行日志
- 调用路径：`GET /api/v3/get_job_instance_ip_log`

### 执行类

#### `fast_execute_script`

```bash
bk-cli job fast_execute_script --bk_biz_id 2 --script_content "echo hello" --script_language shell --account_alias root --target_server '{"host_id_list":[1]}'
bk-cli job fast_execute_script --bk_biz_id 2 --script_file ./script.sh --script_language shell --account_alias root --target_server '{"host_id_list":[1]}'
bk-cli job fast_execute_script --body '{"bk_biz_id":2,"target_server":{"host_id_list":[1]},"script_language":1,"script_content":"ZWNobyBoZWxsbw=="}'
```

- 快速执行脚本，`script_content` / `script_file` 必须二选一；未显式提供 `--body` 时至少提供其中一个
- 从 `--script_file` 读取到的脚本内容也会和 `script_param` 一样在发送前做 Base64 编码
- `script_language` 支持：shell、bat、perl、python、powershell
- 未显式提供 `--body` 时，`target_server` 必须通过 `--target_server` 传入 JSON 对象
- 显式提供 `--body` 时，需传完整请求体；不会与其他 flag 做局部合并
- 调用路径：`POST /api/v3/fast_execute_script`

#### `fast_transfer_file`

```bash
bk-cli job fast_transfer_file --body '{"bk_scope_type":"biz","bk_scope_id":"2","bk_biz_id":2,...}'
```

- 快速分发文件，payload 较复杂，必须通过 `--body` 提供完整 JSON
- 调用路径：`POST /api/v3/fast_transfer_file`

#### `push_config_file`

```bash
bk-cli job push_config_file --body '{"bk_scope_type":"biz","bk_scope_id":"2","bk_biz_id":2,"file_list":[...],...}'
```

- 分发本地配置文件，`file_list` 中的 `content` 字段须为 Base64 编码
- 调用路径：`POST /api/v3/push_config_file`

## 什么时候退回 `bk-cli api`

- 需要调用的 Job API 不在上述列表中
- 需要完全自定义 body/header
