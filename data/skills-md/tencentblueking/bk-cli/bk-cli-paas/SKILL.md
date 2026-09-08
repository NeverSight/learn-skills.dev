---
name: bk-cli-paas
description: 当需要通过 `bk-cli paas` 查询蓝鲸 PaaS 应用、模块、部署、日志、进程、环境变量、增强服务信息，创建云原生应用或模块，或触发支持多模块的部署动作时使用。
---

# bk-cli paas — 蓝鲸 PaaS 应用部署能力

用于通过 `bk-cli paas` 调用蓝鲸 PaaS 应用、模块、部署、日志、进程、环境变量和增强服务相关 API。

CRITICAL — 开始前 MUST 先用 Read 工具读取 `../bk-cli-shared/SKILL.md`。共享 skill 负责认证、context、tenant、stage、dry-run、verbose、header/body 和通用请求规则；本 skill 只补充 `paas` 命令自己的语义与输入约定。

## 当前覆盖范围

当前 skill 覆盖以下命令：

- `get_minimal_app_list`
- `get_app_info`
- `list_app_modules`
- `get_repo_branches`
- `get_deployments_list`
- `streams_history_events`
- `list_processes`
- `module_env_released_info`
- `module_env_released_state`
- `search_standard_log_with_post`
- `create_module`
- `get_deployment_result`
- `deploy_with_module`
- `create_cloud_native_app`
- `list_config_vars`
- `get_config_var`
- `set_config_var_value`
- `list_module_services`
- `bind_service`
- `get_service_instance_by_module`
- `unbind_service`

## 输入约定

- 这些接口都要求应用认证 + 用户认证 + 接口资源权限。调用前需要确保当前 context 的凭据同时满足应用身份和用户身份，并且对应应用已申请这些 API 的接口权限。
- 应用 ID 使用 PaaS 应用 `app_code`，部分接口按上游原始参数名使用 `code`。
- 模块名使用 PaaS 模块名称；未指定模块时，通常使用默认模块 `default`。相关命令已把 `module` 或 `module_name` 默认值设为 `default`。
- 环境参数使用接口原始参数名：`env` 或 `environment`，常见值为 `stag` 或 `prod`。写操作默认先用 `stag`，除非用户明确要求 `prod`。
- `deploy_with_module`、`create_module`、`create_cloud_native_app`、`set_config_var_value`、`bind_service` 等复杂请求体通过共享 `--body '<json>'` 传入；查看完整结构可运行 `bk-cli paas <action> -h --body-schema`。

## 常用工作流

1. 用 `get_minimal_app_list` 定位应用 ID。
2. 用 `get_app_info` 确认应用类型、语言、模块和最近部署时间。
3. 用 `list_app_modules` 确认模块名；用户未指定时优先使用 `default`。
4. 代码仓库部署前用 `get_repo_branches` 取得 `name` / `type` / `revision`，填入 `deploy_with_module` 的 `--body`。
5. 部署后用 `get_deployments_list` 找部署任务，再用 `streams_history_events` 查看日志流。
6. 需要看运行态时，用 `module_env_released_state`、`list_processes` 或 `search_standard_log_with_post`。
7. 需要管理环境变量时，用 `list_config_vars`、`get_config_var`、`set_config_var_value`。
8. 需要管理增强服务绑定时，用 `list_module_services`、`bind_service`、`get_service_instance_by_module`、`unbind_service`。
9. 需要创建云原生应用或模块时，分别使用 `create_cloud_native_app` 或 `create_module`。

## Commands

#### `get_minimal_app_list`

```bash
bk-cli paas get_minimal_app_list
bk-cli paas get_minimal_app_list --app_status normal --source_origin 1
```

- 获取当前用户有权限的 App 简明信息列表。
- 调用路径：`GET /bkapps/applications/lists/minimal`
- 常看字段：`results[].application.code`、`results[].application.name`。

#### `get_app_info`

```bash
bk-cli paas get_app_info --app_code bk-demo
```

- 查看应用信息。写操作前先调用一次确认 `app_code`，创建模块前确认 `application.type` 为 `cloud_native`。
- 调用路径：`GET /bkapps/applications/{app_code}/`
- 常看字段：`application.type`、`application.language`、`application.modules`、`application.last_deployed_date`。

#### `list_app_modules`

```bash
bk-cli paas list_app_modules --app_code bk-demo
bk-cli paas list_app_modules --app_code bk-demo --source_origin 1
```

- 查看应用下所有模块。
- 调用路径：`GET /bkapps/applications/{app_code}/modules/`
- 多模块应用先确认用 `default` 还是其他模块；`is_default=true` 表示默认模块。

#### `get_repo_branches`

```bash
bk-cli paas get_repo_branches --app_code bk-demo
bk-cli paas get_repo_branches --app_code bk-demo --module default
```

- 获取应用模块的代码仓库分支信息。
- 调用路径：`GET /bkapps/applications/{app_code}/modules/{module}/repo/branches/`
- 返回中 `results[].name` 对应部署 body 的 `version_name`，`results[].type` 对应 `version_type`，`results[].revision` 可填入 `revision`。
- 纯镜像应用没有仓库；遇到仓库相关错误时改走镜像部署路径，不要反复重试该接口。

#### `get_deployments_list`

```bash
bk-cli paas get_deployments_list --app_code bk-demo
bk-cli paas get_deployments_list --app_code bk-demo --environment prod --limit 12 --offset 0
```

- 获取应用模块部署历史，默认模块为 `default`。
- 调用路径：`GET /bkapps/applications/{app_code}/modules/{module}/deployments/lists/`
- 可选 query：`environment`、`operator`、`limit`、`offset`。
- 返回中 `results[].id` 或 `results[].deployment_id` 可作为 `streams_history_events` 的 `channel_id`。

#### `streams_history_events`

```bash
bk-cli paas streams_history_events --channel_id 22d0e9c8-9cfc-45a5-b5a8-718137c515db
bk-cli paas streams_history_events --channel_id 22d0e9c8-9cfc-45a5-b5a8-718137c515db --last_event_id 10
```

- 获取部署日志流，`channel_id` 通常就是部署任务 ID。
- 调用路径：`GET /streams/{channel_id}/history_events`
- 有频控，约每用户 60 秒 10 次；不要 tight loop。

#### `list_processes`

```bash
bk-cli paas list_processes --app_code bk-demo --env stag
bk-cli paas list_processes --app_code bk-demo --module default --env prod --release_id 123
```

- 获取应用环境所有进程与实例信息。
- 调用路径：`GET /bkapps/applications/{app_code}/modules/{module}/envs/{env}/processes/list/`
- 常看字段：replica、实例 `Running` / `ready`、重启次数。

#### `module_env_released_info`

```bash
bk-cli paas module_env_released_info \
  --code bk-demo \
  --environment prod
```

- 查询应用模块环境部署信息，默认模块为 `default`。
- 调用路径：`GET /bkapps/applications/{code}/modules/{module_name}/envs/{environment}/released_info/`

#### `module_env_released_state`

```bash
bk-cli paas module_env_released_state \
  --code bk-demo \
  --environment prod
```

- 查询应用模块环境部署状态，比 `module_env_released_info` 多 `is_offlined`、默认访问入口等信息。
- 调用路径：`GET /bkapps/applications/{code}/modules/{module_name}/envs/{environment}/released_state/`
- 常看字段：`is_offlined`、`exposed_link.url`、`default_access_entrance.url`。从未发布过时上游可能返回 `APP_NOT_RELEASED`。

#### `search_standard_log_with_post`

```bash
bk-cli paas search_standard_log_with_post \
  --app_code bk-demo \
  --body '{"query":{"query_string":"","terms":{"environment":["stag"]}}}'

bk-cli paas search_standard_log_with_post \
  --app_code bk-demo \
  --module default \
  --time_range customized \
  --start_time '2026-08-24 10:00:00' \
  --end_time '2026-08-24 11:00:00' \
  --body '{"query":{"query_string":"error","terms":{"environment":["prod"],"process_id":["web"]}}}'
```

- 查询应用标准输出日志，默认模块为 `default`，默认查询最近 `1h`。
- 调用路径：`POST /bkapps/applications/{app_code}/modules/{module}/log/standard_output/list/`
- 可选 query：`time_range`、`start_time`、`end_time`、`limit`、`scroll_id`。
- 过滤环境和进程时放在 body 的 `query.terms` 中，例如 `environment` 或 `process_id`。

#### `create_module`

```bash
bk-cli paas create_module \
  --app_code bk-demo \
  --body '{"name":"api","source_config":{"source_init_template":"dj2_with_auth","source_origin":2},"bkapp_spec":{"build_config":{"build_method":"buildpack"}}}'
```

- 为云原生应用创建模块。调用前先用 `get_app_info` 确认应用类型为 `cloud_native`。
- 调用路径：`POST /bkapps/applications/{app_code}/modules/`
- 请求体必填字段：`name`、`source_config`、`bkapp_spec`；常见 buildpack 场景还需在 `bkapp_spec.build_config.build_method` 填 `buildpack`。完整结构见 `bk-cli paas create_module -h --body-schema`。

#### `get_deployment_result`

```bash
bk-cli paas get_deployment_result \
  --app_code bk-demo \
  --deployment_id 12345
```

- 查询部署任务结果，默认模块为 `default`。
- 调用路径：`GET /bkapps/applications/{app_code}/modules/{module}/deployments/{deployment_id}/result/`

#### `deploy_with_module`

```bash
bk-cli paas deploy_with_module \
  --app_code bk-demo \
  --env prod \
  --body '{"revision":"{commit_id}","version_type":"branch","version_name":"master"}'
```

- 触发支持多模块的 App 部署，默认模块为 `default`。
- 调用路径：`POST /bkapps/applications/{app_code}/modules/{module}/envs/{env}/deployments/`
- 请求体字段：`revision` 为源码仓库版本号，可选；`version_name` 为 branch 或 tag 名称，必填；`version_type` 为版本类型，必填，svn 支持 `trunk`/`tag`，git 支持 `branch`。

#### `create_cloud_native_app`

```bash
bk-cli paas create_cloud_native_app \
  --body '{"code":"bk-demo","name":"bk-demo","source_config":{"source_origin":1,"source_repo_url":"https://github.com/octocat/helloWorld.git","source_repo_auth_info":{},"source_dir":"","source_init_template":"docker"},"bkapp_spec":{"build_config":{"build_method":"dockerfile","dockerfile_path":"Dockerfile"}}}'
```

- 创建云原生应用。
- 调用路径：`POST /bkapps/cloud-native/`
- 请求体根字段：`code`、`name`、`source_config`、`bkapp_spec` 必填；`app_tenant_mode`、`auth_code`、`is_plugin_app`、`advanced_options` 按需传入。
- `source_config.source_origin` 表示源码来源，常见值：`1` 为已授权代码仓库；`6` 对应上游 `SourceOrigin.CNATIVE_IMAGE`，表示仅托管镜像的云原生应用。
- `bkapp_spec.build_config.build_method` 支持 `buildpack`、`dockerfile`、`custom_image`；`dockerfile` 场景通常需要 `dockerfile_path`，`custom_image` 场景需要 `image_repository` 且通常需要 `processes`。


#### `list_config_vars`

```bash
bk-cli paas list_config_vars --app_code bk-demo
bk-cli paas list_config_vars --app_code bk-demo --module default
```

- 查看应用模块的环境变量列表，默认模块为 `default`。
- 调用路径：`GET /bkapps/applications/{app_code}/modules/{module}/config_vars/`

#### `get_config_var`

```bash
bk-cli paas get_config_var --app_code bk-demo --config_var_key FOO
bk-cli paas get_config_var --app_code bk-demo --module default --config_var_key FOO
```

- 通过 key 查询单个环境变量，默认模块为 `default`。
- 调用路径：`GET /bkapps/applications/{app_code}/modules/{module}/config_vars/{config_var_key}/`

#### `set_config_var_value`

```bash
bk-cli paas set_config_var_value \
  --app_code bk-demo \
  --config_var_key FOO \
  --body '{"environment_name":"stag","value":"bar","description":"demo config","is_sensitive":false}'
```

- 通过 key 创建或更新环境变量，默认模块为 `default`。
- 调用路径：`POST /bkapps/applications/{app_code}/modules/{module}/config_vars/{config_var_key}/`
- 请求体必填字段：`environment_name`；取值常见为 `stag`、`prod` 或 `_global_`。新建变量时同时传 `value`。
- 敏感变量设置 `is_sensitive=true`，查询结果中的值可能由上游掩码。

#### `list_module_services`

```bash
bk-cli paas list_module_services --app_code bk-demo
bk-cli paas list_module_services --app_code bk-demo --module default
```

- 查看应用模块的增强服务，默认模块为 `default`。
- 调用路径：`GET /bkapps/applications/{app_code}/modules/{module}/services/`
- 返回通常会按已绑定、共享和未绑定服务分组；绑定前可从未绑定服务中确认 `service_id`。

#### `bind_service`

```bash
bk-cli paas bind_service \
  --body '{"code":"bk-demo","service_id":"svc-uuid","module_name":"default"}'
```

- 绑定应用模块与增强服务。
- 调用路径：`POST /services/service-attachments/`
- 请求体必填字段：`code`、`service_id`；`module_name` 不传时由上游按默认模块处理，建议显式传 `default`。
- 需要指定服务方案时传 `plan_id`，需要分环境方案时传 `env_plan_id_map`。

#### `get_service_instance_by_module`

```bash
bk-cli paas get_service_instance_by_module \
  --app_code bk-demo \
  --service_id svc-uuid
```

- 查看应用模块与增强服务的绑定关系详情，默认模块为 `default`。
- 调用路径：`GET /bkapps/applications/{app_code}/modules/{module}/services/{service_id}/`

#### `unbind_service`

```bash
bk-cli paas unbind_service \
  --app_code bk-demo \
  --service_id svc-uuid
```

- 解绑应用模块与增强服务，默认模块为 `default`。
- 调用路径：`DELETE /bkapps/applications/{app_code}/modules/{module}/services/{service_id}/`
- 解绑是写操作，真实执行前建议先加 `--dry-run` 确认 app、module 和 service_id。
