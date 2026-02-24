---
name: openclaw-team-bus
description: Multi-agent communication bus for OpenClaw. Use for team coordination, task distribution, and inter-agent messaging via shared filesystem.
metadata: {"clawdbot":{"emoji":"👥","requires":{"bins":["python3"],"dirs":["/root/.openclaw/team-bus"]}}}
---

# OpenClaw Team Bus

Multi-agent communication system with automatic agent ID detection.

## Setup

### 1. 团队信息

```bash
cp examples/team.json.template /root/.openclaw/team-bus/team.json
```

团队成员：

| 代号 | AgentID | 职责 |
|------|---------|------|
| Prism | lead | 协调、汇总、Telegram沟通 |
| Scope | product | 需求、PRD、User Stories |
| Pixel | coder | 代码实现、bug修复、测试 |
| Lens | architect | 架构设计、接口定义、代码审查 |
| Shutter | ops | 部署、CI、集成测试、安全监控 |

### 2. 安装 Skill

```bash
cd <agent-workspace>/skills
git clone https://github.com/louis-cai/openclaw-team-bus-skills.git openclaw-team-bus
```

### 3. 配置 HEARTBEAT

```bash
cp examples/HEARTBEAT.template <workspace>/HEARTBEAT.md
```

## Usage

```bash
python3 bus.py <command> [args]

Commands:
  send <agent> <title> <desc> <chat> --from <agent>   # 发送任务（必传）
  poll                                              # 扫描收件箱（自动获取agent ID）
  reply <agent> <task-id> <msg> [--accountId <id>]   # 回复（accountId 必传）
  broadcast <msg> [--chatId <id>] [--accountId <id>] # 广播（分发到每个 agent 的 inbox）
  list-agents                                       # 列出 agent
  team                                              # 显示团队信息（我是谁）
  complete <task-id> [result]                       # 完成任务
  fail <task-id> <error>                            # 标记失败
```

## Agent ID

Agent ID 自动从环境变量获取：
- `TEAM_BUS_AGENT` (手动配置)
- `CLAW_AGENT_ID` (OpenClaw 自动提供)

无需手动传入，poll/team 等命令自动识别自己的身份。
