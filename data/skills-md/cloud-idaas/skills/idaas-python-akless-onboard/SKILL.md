---
name: idaas-python-akless-onboard
description: Automates refactoring of Python Alibaba Cloud workloads (OSS V1/V2, SLS, generic OpenAPI) from long-term AccessKey/SecretKey to IDaaS AK-less short-term STS credentials. Use when a developer asks to onboard/integrate IDaaS 无AK, remove hardcoded AK/SK, or convert Python cloud code to IDaaS PAM credential providers.
version: 1.1.3
---

# IDaaS Python 无 AK 接入改造

将 Python 业务代码中的**长期 AK/SK**改造为 IDaaS 无 AK 短期凭证。完成依赖检查、AK/SK 使用点扫描、代码改写、敏感信息清理和验收。

## 前置输入

1. 平台下发的 `client-config.json`（默认 `~/.cloud_idaas/client-config.json`，或 `CLOUD_IDAAS_CONFIG_PATH`）。
2. 目标 RAM `role_arn`，优先通过 `ALIBABA_CLOUD_ROLE_ARN` 注入。
3. 代码仓库根目录与 Python 3.9+。

## 执行流程与分支

1. **环境闸门**
   - 检查 Python 版本不低于 3.9、仓库根目录、`role_arn` 或 `ALIBABA_CLOUD_ROLE_ARN`。
   - 未提供角色 ARN：提示用户提供或由部署环境注入，**停止**；不得写入或臆造 ARN。
2. **配置闸门**
   - 执行 `python3 scripts/render_config.py --config <path>`；未传路径时使用 `CLOUD_IDAAS_CONFIG_PATH`，否则使用默认路径。
   - 输出 `ok=false` 或 `next_action=stop_and_resolve_configuration` 时：立即向用户报告 `problems`，说明“配置校验失败，停止改造”；**不得继续扫描、安装依赖或修改代码**。
   - `CLIENT_SECRET_BASIC`、`CLIENT_SECRET_POST`、`CLIENT_SECRET_JWT`：检查 `clientSecretEnvVarName` 指向的环境变量非空。缺失时只报告变量名，要求部署环境安全注入；绝不读取、输出或生成 Secret。
   - `PKCS7`：要求 ECS 部署标识；`OIDC`：要求 Kubernetes 部署标识；两者均不检查 Client Secret。
   - `--render` 仅生成并校验配置结构，不检查运行时 Secret。
3. **扫描与范围确认**
   - 配置闸门通过后，执行 `python3 scripts/scan_ak_usage.py --repo <root>`。
   - 逐项汇报静态认证、AK/SK 字面量、环境变量读取、手动 STS、SDK 类型和已接入文件；等待用户确认待改造文件。
   - 自动跳过常见依赖与构建目录（包括 `skill-build/`）；其他构建产物、Skill 源码或第三方目录命中时，标为非业务误报；在用户确认排除前不得改动这些文件。
   - 没有命中时报告“无需改造”，执行静态校验后结束。
4. **按 SDK 类型改写**
   - OSS V1：`oss2.Auth(...)` 改为 `get_oss_v1_credential_provider(...)` 与 `oss2.ProviderAuthV4(provider)`。
   - OSS V2、SLS、通用 OpenAPI：严格按 `references/templates.md` 使用对应 provider；不得缓存短期凭证。
   - 角色 ARN 优先从 `ALIBABA_CLOUD_ROLE_ARN` 读取；删除旧 AK/SK、手动 AssumeRole 与手动刷新逻辑。
5. **验证与冒烟分支**
   - 执行 `python3 scripts/verify_akless.py --repo <root>`；失败时报告 violations 并停止交付。
   - 编译或单元测试失败时报告失败原因并停止。
   - 仅在运行时认证资料已注入且用户授权外部访问时，执行最小只读冒烟；写入操作必须单独取得用户确认。
   - 冒烟出现 403 时，提示核对 PAM 功能权限与目标角色数据权限；不得改回长期 AK/SK。

## 安全约束

- 不输出、写入、生成或提交 Client Secret。
- 不缓存 `provider.get_credentials()` 的返回值。
- 换票 403 时优先核对平台的 PAM 功能权限与目标角色数据权限。

## 验收

- 获批资源访问成功，未获批资源返回 403。
- 进程运行超过 StsToken 有效期后自动续期正常。
- 见 `references/checklist.md`。
