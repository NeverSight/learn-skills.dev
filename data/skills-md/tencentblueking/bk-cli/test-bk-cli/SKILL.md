---
name: test-bk-cli
description: 交互式测试和探索蓝鲸 CLI（bk-cli）命令。当用户希望测试 bk-cli、探索蓝鲸平台 API、验证 bk-cli 功能，或对蓝鲸各系统（cmdb、gse、job、sops、nodeman、devops 等）执行只读命令时，使用此 skill。触发短语包括"测试 bk-cli"、"test bk-cli"、"探索 bk-cli 命令"、"查看 bk-cli 接口"，或任何涉及 bk-cli 子命令测试的场景。
---

# test-bk-cli Skill

本 skill 指导对 `bk-cli`（蓝鲸平台命令行工具）进行系统性、安全的探索。目标是测试所有可用的只读命令，**绝不修改任何现有配置**，**绝不执行破坏性命令**。

## 前置条件（开始前确认）

执行任何命令前，先与用户确认以下两点：

1. **bk-cli 已安装**：`bk-cli version` 或 `bk-cli -h` 能正常执行。
2. **现有 context 安全**：测试过程中**绝不**切换、覆盖或删除用户已有的 context。

若任一条件不满足，停下来引导用户修复后再继续。

---

## 第一阶段：基础命令

测试 `help`、`version`、`update`、`completion` 这类内置命令，验证 CLI 基本可用性。

```bash
bk-cli -h         # 获取完整子命令列表，作为后续阶段的依据
bk-cli version    # 查看版本信息
bk-cli update -h  # 查看 update 用法（不执行实际更新）
bk-cli completion -h  # 查看 completion 用法（不执行安装）
```

**注意**：`update` 和 `completion` 只查看 `-h`，不实际执行，避免修改本地环境。

---

## 第二阶段：认证与 Context

先分别查看帮助，然后按完整流程测试 context 和 auth 的各项子命令。

### 查看帮助
```bash
bk-cli context -h
bk-cli auth -h
```

### 完整测试流程

本阶段通过创建一个临时 context 来完整测试所有子命令，测试结束后清理干净，**不影响用户原有的 default context**。

执行前先从 default context 获取 `bk_api_url_tmpl`（`bk-cli context list`），新 context 使用相同的 URL。认证参数使用以下固定测试值，无需询问用户：

- context 名称：`test-ctx`
- bk_app_code：`test_bk_app_code`
- bk_app_secret：`test_bk_app_secret`
- bk_token：`test_bk_token`

```bash
# 1. 创建临时 context
bk-cli context create test-ctx --bk_api_url_tmpl="<default 的 url_tmpl>"

# 2. 切换到新 context
bk-cli context use test-ctx

# 3. 在新 context 下登录
bk-cli auth login --bk_app_code="test_bk_app_code" --bk_app_secret="test_bk_app_secret" --bk_token="test_bk_token"

# 4. 查看认证状态（应已认证）
bk-cli auth status

# 5. 登出
bk-cli auth logout

# 6. 再次查看认证状态（应未认证）
bk-cli auth status

# 7. 重新登录（恢复认证）
bk-cli auth login --bk_app_code="test_bk_app_code" --bk_app_secret="test_bk_app_secret" --bk_token="test_bk_token"

# 8. 列出所有 context（确认新 context 存在且 active）
bk-cli context list

# 9. 切回 default context
bk-cli context use default

# 10. 删除临时 context（清理）
bk-cli context delete test-ctx
```

流程结束后验证：`bk-cli context list` 中不再有 `test-ctx`，active 仍为 `default`。

---

## 第三阶段：API 工具命令

测试 `api` 和 `apigateway` 命令，了解可用的网关和接口。

### `bk-cli apigateway`
```bash
bk-cli apigateway -h                            # 查看子命令
bk-cli apigateway list_gateways                 # 列出所有网关
bk-cli apigateway list_gateway_apis --gateway_name <name>   # 列出网关下的所有接口
bk-cli apigateway retrieve_gateway_api_details --gateway_name <name> --api_name <api>  # 查看接口详情
```

### `bk-cli api`

`bk-cli api` 是原始 HTTP 客户端，本阶段结合 `apigateway` 一起测试：通过 `apigateway` 查询某个系统命令对应的真实 API 路径，再用 `bk-cli api` 直接调用验证。

测试流程示例：
```bash
# 1. 查询某网关下某个命令的真实 API 路径
bk-cli apigateway retrieve_gateway_api_details --gateway_name bk-apigateway --api_name v2_open_list_gateways

# 2. 从返回结果中提取 path、method
# 例如得到：GET /api/v2/open/gateways/

# 3. 用 bk-cli api 直接调用，可附加过滤参数
bk-cli api bk-apigateway GET "/api/v2/open/gateways/?name=bk-iam"
```

选取 2～3 个有代表性的只读接口（GET/POST）进行验证即可，不需要穷举所有接口。**`bk-cli api` 仅在本阶段使用，第四阶段测试系统子命令时禁止用它绕过**。

---

## 第四阶段：系统子命令（仅只读）

对每个系统子命令（cmdb、gse、job、sops、nodeman、devops 等）按以下步骤操作：

### 每个系统的测试步骤

1. **执行 `bk-cli <system> -h`** ——获取完整子命令列表。
2. **识别只读命令**：包含 `get_*`、`list_*`、`search_*`、`find_*`、`query_*`、`retrieve_*`。跳过 `create_*`、`delete_*`、`update_*`、`transfer_*`、`operate_*`、`start_*`、`push_*`、`fast_execute_*`、`install_*` 等。
3. **对每个只读命令执行 `bk-cli <system> <command> -h`** ——了解所需参数。
4. **收集必要参数**——优先从本次会话中已执行命令的结果中推导；实在无法推导时再询问用户。
5. **执行 `bk-cli <system> <command>` 并展示原始输出**。若命令失败，如实上报错误，等待用户指示。

### 参数来源策略

尽量从已有命令结果中推导参数，减少对用户的打扰：
- 执行 `search_business` 后，得到 `bk_biz_id`。
- 执行 `list_biz_hosts` 后，得到主机 IP 和 `bk_agent_id`。
- 执行 `search_set` 后，得到 `bk_set_id`，可用于 `search_module`。
- 执行 `get_job_instance_status` 后，得到 `step_instance_id`，可用于日志查询。

只有真正无法推导的参数（如用户自己作业历史中的 `job_instance_id`、devops 的 `project_id`）才询问用户。

---

## 处理 403 错误

**当 API 网关返回 403**（`X-Bkapi-Error-Code: 1640301`，消息：`App has no permission`）：

**立即停止。** 不要尝试其他路径，不要重试。告知用户：
> "遇到了 403 权限不足。需要在 API 网关管理后台给应用 `<bk_app_code>` 授权访问 **`<gateway_name>`** 网关的权限。
> 请前往：API 网关 → 网关管理 → `<gateway_name>` → 权限管理 → 应用权限 → 添加 `<bk_app_code>`。
> 完成授权后告诉我，我会重新执行。"

`bk_app_code` 和 `gateway_name` 可从 403 响应头和错误消息中获取。

**当业务系统返回 403**（如 `bk_error_code: 9900403`，IAM 权限错误）：

**立即停止。** 告知用户：
> "遇到了业务权限不足（IAM 9900403）。需要在权限中心给应用 `<bk_app_code>` 申请 **`<system_name>`** 系统的 **`<action_name>`** 权限。
> 请前往：蓝鲸权限中心 → 申请权限 → 选择系统 `<system_name>` → 操作 `<action_name>`。"

---

## 安全规则（绝对禁止）

以下规则不得违反：

1. **绝不执行**名称中含有以下词的命令：`create`、`delete`、`update`（系统子命令中）、`transfer`、`install`、`start`、`operate`、`push`、`fast_execute`、`revoke`、`retry`。
2. **保护 default context**——第二阶段只在临时 context 上做 auth 测试，最终必须切回 `default` 并删除临时 context；禁止对 `default` context 执行任何修改或删除操作。
3. **第四阶段只能使用 `bk-cli <system> <command>`**——禁止用 `bk-cli api` 绕过系统子命令，无论遇到任何错误都不例外。
4. **绝不凭训练知识猜测 API 路径或参数**——始终通过 `-h` 输出发现可用命令和参数。
5. **遇到 403 立即停止**——不尝试其他端点或替代路径。
6. **不主动使用 `--dry-run`**——除非用户明确要求预览命令。

---

## 输出格式

每个命令测试后展示：
1. 实际执行的命令。
2. 原始 CLI 输出（若 `info`/`data` 数组超过 10 条，截断为前 3 条并注明总数）。
3. 一行结果说明（成功 / 错误类型）。

每个阶段或系统测试结束后，给出汇总表：

| 命令 | 状态 | 备注 |
|------|------|------|
| search_business | ✅ | 返回 1 条业务 |
| list_biz_hosts | ✅ | 共 52 台主机 |
| list_hosts_without_biz | ❌ IAM 403 | 需要 view_resource_pool_host 权限 |

---

## 示例：处理 403

```
收到 403：App has no permission [bk_app_code=bk_apigw_test, gateway=bk-sops]

→ 立即停止，告知用户：
"遇到了 403。请在 API 网关后台给 bk_apigw_test 授权 bk-sops 网关权限后告诉我，我重新执行。"
```
