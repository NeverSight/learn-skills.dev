---
name: bk-cli-nodeman
description: 当需要通过 `bk-cli nodeman` 使用节点管理相关系统子命令时使用。适合安装/管理 Agent 和查询任务详情的场景。
---

# bk-cli nodeman — 节点管理能力使用说明

用于通过 `bk-cli nodeman` 调用蓝鲸节点管理（bk-nodeman）API 的系统子命令。

CRITICAL — 开始前 MUST 先用 Read 工具读取 `../bk-cli-shared/SKILL.md`。共享 skill 负责认证、context、tenant、stage、dry-run、verbose、header/body 和通用请求规则；本 skill 只补充 `nodeman` 命令自己的语义与输入约定。

## 当前覆盖范围

当前 skill 覆盖这些常用命令：

- `install_job`
- `get_job_details`

## Commands

#### `install_job`

```bash
bk-cli nodeman install_job --body '{"job_type":"INSTALL_AGENT","hosts":[{"bk_biz_id":2,"bk_cloud_id":0,"os_type":"LINUX","inner_ip":"10.0.0.1","auth_type":"PASSWORD","account":"root","password":"xxx","port":22}]}'
```

- 创建安装类任务（安装/重装/卸载/升级 Agent/Proxy）
- payload 较复杂，必须通过 `--body` 提供完整 JSON
- 支持的 `job_type`：INSTALL_AGENT、INSTALL_PROXY、REINSTALL_AGENT、REINSTALL_PROXY、REPLACE_PROXY、UNINSTALL_AGENT、UNINSTALL_PROXY、UPGRADE_AGENT、UPGRADE_PROXY、RELOAD_AGENT、RELOAD_PROXY
- 调用路径：`POST /api/job/install/`

#### `get_job_details`

```bash
bk-cli nodeman get_job_details --job_id 123
bk-cli nodeman get_job_details --job_id 123 --page 1 --pagesize 50
```

- 查询任务执行详情
- 默认 `pagesize=-1`（返回全部）
- 调用路径：`POST /api/job/{job_id}/details/`
