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

## 本地 Agent 协调（A2A）

### ⭐ 高管工作模式（核心原则）

**你是高管，不是传话筒。**

1. **派活即走** — `sessions_send` 不带 `timeoutSeconds`（或设为 1-5s），发完指令立刻做下一件事
2. **不转发** — 员工自己在群里发消息，你不替他们转发回复
3. **不傻等** — 9 个员工并行工作，你不需要逐个等结果
4. **并行处理** — 派完活后继续处理 Daniel 的其他需求
5. **只管结果** — 员工汇报到群里，你审核质量即可

```
❌ 错误模式（秘书）:
   派活 → 等回复 → 转发回复 → 再派下一个

✅ 正确模式（高管）:
   批量派活（不等） → 做其他事 → 看群里汇报 → 审核质量
```

### 指令模板
```
sessions_send(
  sessionKey="agent:<agentId>:telegram:group:YOUR_GROUP_CHAT_ID",
  message="【小a工作指令】<具体任务>。直接在群里发结果，不要回复我。",
  timeoutSeconds=5  // 最多等5秒，超时也没关系，后台会继续
)
```

### sessions_send vs message 的区别

| 方式 | 作用 | 正确用途 |
|------|------|----------|
| `message(accountId=xxx, target=群ID)` | **以该 bot 身份发消息** | 公告、通知、以员工名义发固定文本 |
| `sessions_send(sessionKey=..., message=...)` | **给 agent 发指令，agent 自行处理并回复** | 分配任务、触发 agent 行为 |

### sessionKey 格式（本地 agent）
```
agent:<agentId>:telegram:group:<chatId>
```

### ⚠️ 注意：delivery 回显问题
`sessions_send` 默认 `delivery: "announce"` 会把 agent 回复回显到调用者的会话，导致主 bot 在群里重复发 agent 的回复。agent 自己已经通过 message tool 发了消息，所以回显是多余的。

**解决**: agent 本身发消息到群，主 bot 不需要再转发。看到 agent 的 status=ok/timeout 就够了。

### 完整员工列表

| 员工 | agentId | accountId | 模型 |
|------|---------|-----------|------|
| 小ops | ops | xiaoops | xsc-opus46 |
| 小code | code | xiaocode | xsc-opus46 |
| 小quant | quant | xiaoq | xsc-opus46 |
| 小content | content | xiaocontent | glm5 |
| 小data | data | xiaodata | glm5 |
| 小finance | finance | xiaofinance | glm5 |
| 小research | research | xiaoresearch | glm5 |
| 小market | market | xiaomarket | glm5 |
| 小pm | pm | xiaopm | glm5 |

注意：quant 的 accountId 是 `xiaoq`（不是 xiaoquant）。

### GLM-5 身份覆盖问题
GLM-5 有内置 "Kiro" 人设，会覆盖 SOUL.md 身份。解决方案：在 AGENTS.md 顶部加 `CRITICAL IDENTITY` 强制声明。

### 批量调度
```python
for agent_id in ["ops", "code", "quant", "content", "data", "finance", "research", "market", "pm"]:
    sessions_send(
        sessionKey=f"agent:{agent_id}:telegram:group:YOUR_GROUP_CHAT_ID",
        message="你的任务指令"
    )
```

## 触发词

- "给小m发消息"
- "通知另一个实例"
- "跨机器执行"
- "同步到远程"
- "agent间通信"
- "实例间通信"
