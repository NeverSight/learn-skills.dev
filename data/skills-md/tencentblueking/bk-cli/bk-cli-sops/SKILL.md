---
name: bk-cli-sops
description: 当需要通过 `bk-cli sops` 使用标准运维相关系统子命令时使用。适合查询流程模板、创建和管理任务的场景。
---

# bk-cli sops — 标准运维能力使用说明

用于通过 `bk-cli sops` 调用蓝鲸标准运维（SOPS）API 的系统子命令。

CRITICAL — 开始前 MUST 先用 Read 工具读取 `../bk-cli-shared/SKILL.md`。共享 skill 负责认证、context、tenant、stage、dry-run、verbose、header/body 和通用请求规则；本 skill 只补充 `sops` 命令自己的语义与输入约定。

## 当前覆盖范围

当前 skill 覆盖这些常用命令：

- `get_template_list`
- `get_task_list`
- `get_task_status`
- `get_task_detail`
- `create_task`
- `start_task`
- `operate_task`

## Commands

### 模板查询

#### `get_template_list`

```bash
bk-cli sops get_template_list --bk_biz_id 2
bk-cli sops get_template_list --bk_biz_id 2 --keyword deploy
```

- 调用路径：`GET /get_template_list/{bk_biz_id}/`

### 任务管理

#### `get_task_list`

```bash
bk-cli sops get_task_list --bk_biz_id 2
bk-cli sops get_task_list --bk_biz_id 2 --keyword deploy --limit 50
```

- 调用路径：`GET /get_task_list/{bk_biz_id}/`

#### `create_task`

```bash
bk-cli sops create_task --bk_biz_id 2 --template_id 100 --name "deploy-v1"
bk-cli sops create_task --bk_biz_id 2 --template_id 100 --name "deploy" --constants '{"${key}":"value"}'
```

- 从模板创建任务
- `--constants` 必须是 JSON 对象，CLI 会以嵌套对象形式写入请求体
- 调用路径：`POST /create_task/{template_id}/{bk_biz_id}/`

#### `start_task`

```bash
bk-cli sops start_task --bk_biz_id 2 --task_id 100
```

- 启动已创建的任务
- 调用路径：`POST /start_task/{task_id}/{bk_biz_id}/`

#### `get_task_status`

```bash
bk-cli sops get_task_status --task_id 100 --bk_biz_id 2
```

- 调用路径：`GET /get_task_status/{task_id}/{bk_biz_id}/`

#### `get_task_detail`

```bash
bk-cli sops get_task_detail --task_id 100 --bk_biz_id 2
```

- 调用路径：`GET /get_task_detail/{task_id}/{bk_biz_id}/`

#### `operate_task`

```bash
bk-cli sops operate_task --bk_biz_id 2 --task_id 100 --action pause
bk-cli sops operate_task --bk_biz_id 2 --task_id 100 --action resume
bk-cli sops operate_task --bk_biz_id 2 --task_id 100 --action revoke
```

- 操作任务：暂停、继续或终止
- `action` 必须是 pause / resume / revoke 之一
- 调用路径：`POST /operate_task/{task_id}/{bk_biz_id}/`
