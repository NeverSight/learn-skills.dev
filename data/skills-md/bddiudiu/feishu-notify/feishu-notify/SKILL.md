---
name: feishu-notify
description: 飞书机器人 Webhook 通知集成。在关键节点自动推送通知：任务完成、需要用户决策、等待输入时。支持标准化消息格式，包含任务类型、状态、详情等信息。
---

# 飞书通知 Skill

在关键节点通过 Webhook 将 Claude Code 状态推送到飞书机器人。

## 触发场景

| 场景 | 说明 |
|------|------|
| ✅ 任务完成 | 任务执行完成时通知 |
| 🤔 需要决策 | 需要用户授权确认时通知 |
| ⏳ 等待输入 | 等待用户输入超过60秒时通知 |

## 通知格式

```
【任务类型】任务名称
状态：✅成功 / ❌失败 / ⏳进行中 / 🤔待决策 / ⚠️异常
详情：简要说明
时间：YYYY-MM-DD HH:MM:SS
```

## 脚本用法

```bash
~/.claude/skills/feishu-notify/scripts/notify.sh "任务类型" "状态" "任务名称" "详情" "额外信息"
```

参数说明：
- **任务类型**：编译任务/测试任务/部署任务/决策确认/错误通知
- **状态**：running/success/failed/decision/error
- **任务名称**：任务的简短描述
- **详情**：详细说明
- **额外信息**：预计时间等（可选）

## 状态对照

| 状态值 | 显示 | 卡片颜色 |
|--------|------|----------|
| running | ⏳进行中 | 蓝色 |
| success | ✅成功 | 绿色 |
| failed | ❌失败 | 红色 |
| decision | 🤔待决策 | 橙色 |
| error | ⚠️异常 | 洋红 |

## 手动调用示例

```bash
# 编译开始
~/.claude/skills/feishu-notify/scripts/notify.sh '编译任务' 'running' 'Android库编译' '正在使用NDK编译' '**预计时间**：10分钟'

# 编译成功
~/.claude/skills/feishu-notify/scripts/notify.sh '编译任务' 'success' 'Android库编译' '编译完成，生成 libtuyaos.so'

# 编译失败
~/.claude/skills/feishu-notify/scripts/notify.sh '编译任务' 'failed' 'Android库编译' 'NDK路径未配置'

# 需要决策
~/.claude/skills/feishu-notify/scripts/notify.sh '决策确认' 'decision' '架构选择' '请选择使用 REST API 还是 GraphQL'
```

## 自定义

### 修改 Webhook URL
编辑 `scripts/notify.sh` 中的 `WEBHOOK_URL` 变量。

### 添加更多触发点
在 `~/.claude/settings.json` 的 hooks 中添加配置。
