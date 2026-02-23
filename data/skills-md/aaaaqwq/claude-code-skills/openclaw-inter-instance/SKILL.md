---
name: openclaw-inter-instance
description: "OpenClaw 实例间通信。当需要在多个 OpenClaw 实例之间传递消息、同步数据、远程执行命令时使用此技能。覆盖 agent-to-agent 消息、nodes.run 远程执行、文件级通信等多种方式。"
license: MIT
metadata:
  version: 1.0.0
  domains: [openclaw, multi-agent, communication]
  type: automation
---

# OpenClaw 实例间通信

## 当使用此技能

- 需要给另一个 OpenClaw 实例发消息
- 跨机器远程执行命令
- 多 agent 协作任务
- 同步仓库/文件到远程实例

## 通信方式优先级

按可靠性和实时性排序，依次尝试：

### 1. sessions_send（最优，需配置）

直接 agent-to-agent 消息，实时双向。

**前提**: 双方配置中开启：
```json
// ~/.openclaw/openclaw.json
"tools": { "agentToAgent": { "enabled": true } }
```

**用法**:
```
sessions_send(sessionKey="agent:<target-agent>:main", message="...")
```

**优点**: 实时、双向、最简洁
**缺点**: 默认禁用，需要两端都开启

### 2. nodes.run（远程命令执行）

通过已配对的 node 在远程机器上执行命令。

**前提**: 目标机器已配对为 node 且在线（`nodes status` 检查）

**用法**:
```
nodes(action="run", node="<node-name>", command=["bash", "-c", "<command>"], commandTimeoutMs=30000)
```

**注意事项**:
- 环境变量可能与本地不同（如代理设置）
- 用 `env -u HTTP_PROXY -u HTTPS_PROXY` 绕过不通的代理
- 复杂命令容易超时，拆分为多个小步骤
- gateway 响应慢时会超时（默认 30s），可调大 `commandTimeoutMs`

**典型场景**:
```bash
# 检查文件是否存在
nodes run: ["bash", "-c", "ls ~/target-dir 2>/dev/null && echo EXISTS || echo NOT_FOUND"]

# clone 仓库（注意代理问题）
nodes run: ["bash", "-c", "env -u HTTP_PROXY -u HTTPS_PROXY git clone https://github.com/user/repo.git ~/repo 2>&1"]

# 创建软链接
nodes run: ["bash", "-c", "ln -sfn /source/path /target/path && readlink /target/path"]
```

### 3. openclaw agent CLI（通过 node 调用远程 gateway）

在远程 node 上通过 CLI 向目标实例注入消息。

**用法**:
```bash
openclaw agent --session-id <session-id> -m '<message>' --json
```

**注意**: 需要等 gateway 处理 agent turn，容易超时（60-120s）。适合非紧急通知。

### 4. 文件级通信（兜底方案）

直接写入目标实例的 memory 文件，等待 heartbeat 读取。

**用法**:
```bash
# 通过 nodes.run 写入远程 memory 文件
cat >> <workspace>/memory/YYYY-MM-DD.md << 'EOF'
## 来自小a的通知 (HH:MM)
<消息内容>
EOF
```

**优点**: 一定能送达，不依赖实时连接
**缺点**: 非实时，需要等 heartbeat 或新 session 才能读到

### 5. Telegram/消息渠道（受限）

通过 `message` 工具发送。

**限制**: Telegram bot 之间不能互发消息（403 Forbidden）。仅适用于 bot → 人类 的场景。

## 不可行的方式

| 方式 | 原因 |
|------|------|
| Telegram bot → bot | Telegram API 禁止 |
| curl 调远程 gateway REST API | gateway 不暴露 REST 消息接口 |
| sessions_send 未开启 agentToAgent | 返回 forbidden |

## 实战检查清单

1. `nodes status` — 目标 node 是否在线？
2. 目标机器有无代理/网络限制？
3. SSH key 是否配置？（git clone 用 HTTPS 更稳）
4. 超时设置是否足够？
5. 软链接路径是否正确？

## 推荐架构

```
小a (Linux VPS)                    小m (Mac-Mini)
├── OpenClaw gateway               ├── OpenClaw gateway
├── ~/AGI-Super-Skills (git repo)  ├── ~/AGI-Super-Skills (git clone)
├── ~/clawd/skills/ (workspace)    ├── ~/.openclaw/workspace/skills → ~/AGI-Super-Skills/skills
│                                  │
├── nodes.run ──────────────────── ├── paired node (connected)
└── sessions_send ─────────────── └── agent-to-agent (需开启)
```

## 触发词

- "给小m发消息"
- "通知另一个实例"
- "跨机器执行"
- "同步到远程"
- "agent间通信"
- "实例间通信"
