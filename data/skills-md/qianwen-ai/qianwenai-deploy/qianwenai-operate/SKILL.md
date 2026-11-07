---
name: qianwenai-operate
version: "1.0"
description: >-
  诊断由 qianwenai-deploy 部署到阿里云国内站（aliyun.com）的应用为何不可用或明显变慢，并在用户
  明确确认后执行安全恢复并验证结果。读取项目目录下的 .qianwenai-deploy 状态文件识别 ECS（及可选
  RDS MySQL）资源，先做最小只读诊断，再一次只提议一个恢复动作（启动 ECS、重启应用服务、重载
  Nginx），每个动作都先经过说明影响的确认。
  使用场景：用户说应用打不开 / 返回 502 / 连不上数据库，或要求重启并确认应用恢复。
  不使用场景：没有 .qianwenai-deploy 状态文件；目标是阿里云国际站（用 qwencloud-operate）；
  用户只想要状态/成本概览（用 qianwenai-observe）。
prerequisites:
  - 已配置国内站凭证的 aliyun CLI 3.x
  - 项目目录存在 .qianwenai-deploy 状态文件
input: >-
  含 .qianwenai-deploy 的项目目录。描述的症状（打不开 / 502 / 变慢 / 连不上数据库）。
output: >-
  诊断（故障层次、可能原因、证据、建议动作、影响）；确认后执行一个恢复动作，再验证并返回
  已恢复 / 部分恢复 / 未恢复，并附审计记录（时间、目标、动作、确认结果、CLI RequestId、验证结果）。
---

# 千问 AI 运维

对由 `qianwenai-deploy` 部署在阿里云国内站的应用做故障诊断与确认式恢复。诊断只读、无需确认；任何
改变云资源或应用运行状态的动作都必须经过明确确认。

## 交互流程

```text
识别应用和资源
→ 最小诊断（只读）
→ 给出原因、证据、建议动作
→ 展示影响并请求确认
→ 执行一个恢复动作
→ 验证应用、ECS、RDS
→ 返回结果和审计信息
→ 提议经 qianwenai-observe 重新评分（恢复前 → 恢复后）
```

## 交互形态

- **只读信息**（诊断、原因、证据、验证结果）：纯文本，每条判断后附一行证据（指标、状态、RequestId）。
- **改状态动作**（启停 ECS、重启应用、重载 Nginx 等任何写调用）：先用 AskUserQuestion，提问答清
  **做什么** · **影响**（停机/不可逆） · **怎么验证**，确认前不执行；一次只提议一个恢复动作。
- **主动纪律**：恢复后如结果正常则安静收尾；仅在仍有风险或未恢复时主动给下一步，让用户选。

## 范围

| 范围内 | 范围外 |
|--------|--------|
| 由 `qianwenai-deploy` 部署的应用（存在状态文件） | 无 `.qianwenai-deploy` 状态文件的应用 |
| 单 ECS，或 ECS + RDS MySQL 8.0 | 其他拓扑 / 自建服务器 |
| 诊断 + 确认式恢复（启动 ECS、重启应用、重载 Nginx） | 数据破坏性操作、扩缩容、配置重构 |
| 定位到应用层报错（哪一层坏了、报了什么错） | 源码审查、找 bug/漏洞、判断哪行代码写错、改代码 |
| 阿里云国内站 | 国际站 → 用 `qwencloud-operate` |

## 代码问题不在能力范围内

本 skill 处理基础设施与运行时故障，不做源码审查、缺陷定位或代码修改。诊断可定位到「应用层报错、报了
什么错」，帮用户缩小范围，但不判断具体哪行代码有问题，也不改代码。

涉及代码时，明确告知用户：修改代码属于本 skill 能力之外，需由用户自行决定并执行，相应后果由用户
自行承担。不要在恢复动作里夹带任何代码改动。

## 前置条件

> **Aliyun CLI**：`aliyun version`（需 3.x）。所有命令用驼峰原生形态直连 OpenAPI，
> 不依赖插件。凭证仅用 `aliyun configure list` 查看状态。**绝不**读取、回显、打印或索要 AK/SK/Token。
> 无有效配置集 → 停止并请用户在本会话之外配置凭证。见 `references/cli_installation_guide.md`。

## 怎么做

1. **识别应用** — 从 `.qianwenai-deploy` 识别应用。见 [workflow](references/workflow.md)。
2. **诊断**（只读，无需确认）— 找出坏在哪一层、可能的原因、证据，以及该怎么处理。见
   [diagnose](references/diagnose.md)。
3. **一次只恢复一件事，且先确认。** 选中与诊断匹配的动作，向用户展示影响并取得同意，再执行且仅执行
   那一件事：
   - 启动已停止的服务器 → [recover-ecs](references/recover_ecs.md)
   - 重启卡死的服务器 → [recover-reboot](references/recover_reboot.md)
   - 重启应用服务 → [recover-app](references/recover_app.md)
   - `nginx -t` 通过后重载 Nginx → [recover-nginx](references/recover_nginx.md)
   - EIP 解绑后重新绑定 → [recover-eip](references/recover_eip.md)
   - 放行安全组 80 / 443 入方向 → [recover-securitygroup](references/recover_securitygroup.md)
   - 数据库相关问题 → [recover-rds](references/recover_rds.md)
   - 根分区将满 / 清理后仍不足需扩容 → [recover-disk](references/recover_disk.md)
4. **验证**应用是否恢复，再**记录**做了什么。见 [workflow](references/workflow.md)。

## 保证恢复安全的几条规则

- 诊断只读；恢复只用一小组已知安全的命令。
- 任何会改变状态的动作都先与用户确认，取消则不改变任何东西。
- 一次一个动作，验证后再决定下一步——绝不把多个恢复步骤合在一起。
- 恢复动作可安全重复。
- 遇到超时、权限错误或状态意外变化时，在下一次改动前停下。
- 审计记录和对话里绝不出现密码、Token 或完整连接串。

任何改动前，确认信息要告诉用户：操作哪个资源、执行什么动作、是否会短暂中断应用、是否改变版本、是否
产生新费用，以及你将如何验证（失败了怎么办）。

## 所需权限

见 `references/ram_policies.md`。只读：`ecs:DescribeInstances`、`ecs:DescribeInvocations`、
`ecs:DescribeSecurityGroupAttribute`、`ecs:DescribeDisks`、`vpc:DescribeEipAddresses`、
RDS describe/performance/慢日志。写（恢复）：`ecs:StartInstance`、`ecs:RebootInstance`、
`ecs:AuthorizeSecurityGroup`、`ecs:ResizeDisk`、`vpc:AssociateEipAddress`、
`ecs:RunCommand`（仅白名单恢复命令）。

## 更多细节

分步指南已在上面「怎么做」中链接。另有两份配置参考：

- [CLI 配置](references/cli_installation_guide.md) — 安装与凭证检查。
- [CLI 踩坑速查](references/api_gotchas.md) — 参数形态、时间格式、响应解析易错点。
- [RAM 权限](references/ram_policies.md) — 本 skill 所需的权限。
