---
name: openclaw-ops
description: OpenClaw 运维助手，提供命令参考和故障排查修复流程。当用户需要执行 OpenClaw 命令、诊断服务问题、修复 Gateway 或渠道连接故障、查看日志、管理渠道或 Agent 时使用此技能。触发词包括：openclaw、小龙虾、gateway、渠道连接、消息发送失败、服务不可达等。
---

# OpenClaw Ops

OpenClaw 是一个多渠道 AI Agent 网关，支持 WhatsApp、Telegram、Discord 等消息平台。本技能提供运维所需的命令参考和故障排查能力。

## 标准诊断流程

当用户报告 OpenClaw 问题时，按以下步骤执行：

```bash
# 1. 快速状态检查
openclaw status

# 2. 深度渠道探测
openclaw channels status --probe

# 3. 自动修复
openclaw doctor --repair

# 4. 验证健康状态
openclaw health
```

## 问题分类处理

根据问题类型选择对应处理路径：

**服务无法启动** → `openclaw gateway status` → `openclaw doctor --repair` → `openclaw gateway restart`

**渠道连接失败** → `openclaw channels status --probe` → `openclaw channels login --channel <name>` → 查看渠道日志

**消息发送失败** → `openclaw logs --limit 200` → 检查渠道状态 → 验证目标格式

**性能问题** → `openclaw status --usage` → 查看系统日志 → 检查资源使用

**配置查询** → 查阅 [openclaw_commands.md](references/openclaw_commands.md) 对应章节

## 修复策略

- **首选：** `openclaw doctor --repair` 自动修复
- **Gateway 未运行：** `openclaw gateway restart`
- **修复后仍不健康：** `openclaw doctor --repair --force`
- **更新后修复：** `openclaw update` → `openclaw doctor` → `openclaw health`

## 成功判断标准

- `openclaw health` 返回无错误
- `openclaw channels status --probe` 所有渠道状态正常
- `openclaw status` 显示 gateway 可达

## 最常用命令速查

| 命令 | 用途 |
|------|------|
| `openclaw status` | 查看整体状态 |
| `openclaw health` | 健康检查 |
| `openclaw doctor --repair` | 自动修复 |
| `openclaw gateway restart` | 重启服务 |
| `openclaw channels status --probe` | 检查渠道 |
| `openclaw logs --limit 200` | 查看日志 |

## macOS 注意事项

- Gateway 由 OpenClaw Mac app 管理，不要用 tmux 手动启动
- 检查 launchd 环境变量覆盖：`launchctl getenv OPENCLAW_GATEWAY_TOKEN`
- 系统日志：`/tmp/openclaw/openclaw-YYYY-MM-DD.log`
- 服务日志：`~/.openclaw/logs/gateway.log`
- macOS 错误日志：`./scripts/clawlog.sh -e`

## 详细参考

- 完整命令手册：[openclaw_commands.md](references/openclaw_commands.md)
- 故障排查与修复流程：[openclaw_fix.md](references/openclaw_fix.md)

## 汇报规范

向用户汇报时应包含：发现的问题、执行的操作、当前的状态、后续建议。
