---
name: openclaw-troubleshooter
description: |
  OpenClaw故障排除技能。当用户遇到以下问题时使用：
  1. Gateway无法启动、无法连接、无响应
  2. 渠道连接问题（WhatsApp、Telegram、Discord等）
  3. 模型配置问题（API Key、模型切换失败）
  4. Dashboard/Control UI打不开、连接失败
  5. 会话问题（会话丢失、无法创建新会话）
  6. 配置错误（配置文件错误）
  7. 节点问题（配对失败、工具调用失败）
  8. 浏览器工具问题
  9. Cron/心跳任务不执行
  10. 安装/更新问题
  
  触发关键词：Gateway、启动、连接、报错、问题、故障、无法、失败、错误、Dashboard、UI、渠道、模型、会话、节点、浏览器、Cron、心跳、安装、更新
  
  通过按需查阅官方文档来寻找解决方案，提供小白也能看懂的步骤操作。
---

# OpenClaw 故障排除技能

> 适用于0代码基础用户跟着操作解决问题

---

## 🎯 触发条件

当用户遇到以下关键词时，自动触发此技能：

| 类别 | 触发关键词 |
|------|------------|
| Gateway | 无法启动、启动失败、连接失败、无响应 |
| Dashboard | 打不开、连接失败、空白、报错 |
| 渠道 | WhatsApp连不上、Telegram报错、Discord失败 |
| 模型 | API Key、模型切换、模型错误 |
| 会话 | 会话丢失、无法创建新会话 |
| 配置 | 配置文件错误、配置无效 |
| 节点 | 配对失败、工具调用失败 |
| 浏览器 | 浏览器工具失败、Chrome报错 |
| 自动化 | Cron不执行、心跳没反应 |
| 安装 | 安装失败、更新失败、升级失败 |

---

## 🚀 快速诊断流程（60秒）

### 第一步：运行诊断命令

打开终端（Windows用PowerShell/Mac用终端），依次执行：

```bash
# 1. 查看基本状态
openclaw status

# 2. 查看完整状态
openclaw status --all

# 3. 检查Gateway状态
openclaw gateway status

# 4. 运行诊断
openclaw doctor
```

### 第二步：根据问题选择具体检查

| 问题类型 | 检查命令 |
|----------|----------|
| 渠道问题 | `openclaw channels status --probe` |
| 模型问题 | `openclaw models status` |
| 日志查看 | `openclaw logs --follow` |
| 节点问题 | `openclaw nodes status` |
| Cron问题 | `openclaw cron status` |

---

## 🔍 决策树

根据您的实际问题，选择对应路径：

```
我的问题是：
├─ 1️⃣ Gateway无法启动/无响应
│  └─ → 见"问题1：Gateway无法启动"
│
├─ 2️⃣ Dashboard/Control UI打不开
│  └─ → 见"问题2：Dashboard无法连接"
│
├─ 3️⃣ 渠道消息发不出去/收不到
│  └─ → 见"问题3：渠道消息不流动"
│
├─ 4️⃣ 模型相关问题
│  └─ → 见"问题4：模型问题"
│
├─ 5️⃣ 会话相关问题
│  └─ → 见"问题5：会话问题"
│
├─ 6️⃣ 安装/更新问题
│  └─ → 见"问题6：安装更新问题"
│
├─ 7️⃣ 节点/配对问题
│  └─ → 见"问题7：节点问题"
│
└─ 8️⃣ 其他问题
   └─ → 运行基础诊断命令后查看日志
```

---

## 📋 问题解决方案

### 问题1：Gateway无法启动

**症状**：运行`openclaw gateway`报错、闪退、无响应

**解决步骤**：

```bash
# 步骤1：检查端口占用
netstat -ano | findstr 18789

# 步骤2：停止现有进程（如果有）
openclaw gateway stop

# 步骤3：重新启动
openclaw gateway restart

# 步骤4：如果还是不行，运行诊断
openclaw doctor
openclaw doctor --fix
```

**常见错误和解决方法**：

| 错误信息 | 解决方法 |
|----------|----------|
| `EADDRINUSE` 端口被占用 | 运行 `openclaw gateway stop` 然后重启 |
| `gateway.mode=local` 被阻止 | 修改配置 `gateway.mode="local"` |
| 缺少认证 | 运行 `openclaw configure` 重新配置 |

---

### 问题2：Dashboard无法连接

**症状**：浏览器打开 http://127.0.0.1:18789 失败

**解决步骤**：

```bash
# 步骤1：检查Gateway是否运行
openclaw gateway status

# 步骤2：如果没运行，启动它
openclaw gateway start

# 步骤3：检查认证
openclaw config get gateway.auth.token

# 步骤4：如果没有token，生成一个
openclaw doctor --generate-gateway-token
```

**常见错误和解决方法**：

| 错误信息 | 解决方法 |
|----------|----------|
| `unauthorized`  unauthorized | 检查token是否正确 |
| `device identity required` | 需要安全上下文，用localhost访问 |
| 连接被拒绝 | Gateway没运行，先启动 |

---

### 问题3：渠道消息不流动

**症状**：渠道显示已连接，但发消息没有回复

**解决步骤**：

```bash
# 步骤1：检查渠道状态
openclaw channels status --probe

# 步骤2：检查配对列表
openclaw pairing list whatsapp   # 替换为对应渠道

# 步骤3：检查日志
openclaw logs --follow
```

**常见错误和解决方法**：

| 错误信息 | 解决方法 |
|----------|----------|
| `pairing request` | 运行配对批准 |
| `mention required` | 群聊需要@机器人 |
| `allowlist`  blocked | 发送者在白名单吗 |

---

### 问题4：模型问题

**症状**：模型无法切换、API报错

**解决步骤**：

```bash
# 步骤1：查看模型状态
openclaw models status

# 步骤2：查看配置的模型
openclaw config get agents.defaults.model.primary

# 步骤3：切换模型
openclaw models set anthropic/claude-sonnet-4-5
```

**常见错误和解决方法**：

| 错误信息 | 解决方法 |
|----------|----------|
| `Model is not allowed` | 模型不在允许列表，修改配置 |
| `API Key invalid` | 检查API Key是否正确 |
| `rate limit` | 等待后重试 |

---

### 问题5：会话问题

**症状**：会话丢失、无法创建新会话

**解决步骤**：

```bash
# 步骤1：查看会话列表
openclaw sessions list

# 步骤2：创建新会话（发送消息时用 /new）
```

**常见错误和解决方法**：

| 错误信息 | 解决方法 |
|----------|----------|
| 会话自动重置 | 检查 session.reset 配置 |
| 上下文太长 | 运行 `/new` 开始新会话 |

---

### 问题6：安装更新问题

**症状**：安装失败、无法更新

**解决步骤**：

```bash
# 方式1：重新运行安装脚本（推荐）
curl -fsSL https://openclaw.ai/install.sh | bash

# 方式2：npm更新
npm install -g openclaw@latest

# 方式3：pnpm更新
pnpm add -g openclaw@latest

# 更新后运行诊断
openclaw doctor
openclaw gateway restart
```

---

### 问题7：节点问题

**症状**：节点配对失败、工具调用失败

**解决步骤**：

```bash
# 步骤1：查看节点状态
openclaw nodes status

# 步骤2：查看配对请求
openclaw pairing list

# 步骤3：批准配对
openclaw pairing approve <channel> <code>
```

---

## ⚠️ 重要：避免让AI自己"瘫痪"

### 问题
当AI执行 `openclaw gateway stop` 时：
- Gateway停止 → WebSocket断开 → AI无法响应 → **瘫痪**

### 解决方案

#### 1. 永远不要让AI自己执行 `gateway stop`
- 提供命令 → **让用户手动执行**
- 使用 `gateway restart` 时也要警告用户

#### 2. 使用热重载（推荐）
大多数配置更改不需要重启Gateway：

```bash
# 查看热重载配置
openclaw config get gateway.config.hotReload
```

设置热重载模式：
```bash
openclaw config set gateway.config.hotReload "hybrid"
```

| 模式 | 行为 |
|------|------|
| `hybrid` (默认) | 即时应用安全更改，自动重启关键更改 |
| `hot` | 仅热应用安全更改 |
| `restart` | 任何更改都重启 |
| `off` | 禁用文件监视 |

#### 3. 修改配置的安全流程
1. 先说明要改什么
2. 给出修改命令
3. **建议用户手动执行**
4. 或让用户确认后再执行

#### 4. 如果必须重启
1. 警告用户："即将重启Gateway，我会暂时断开连接"
2. 执行 `openclaw gateway restart`
3. 提醒用户："Gateway已重启，请刷新页面或重新发送消息"

---

## 📖 查阅官方文档

当以上解决方案无法解决问题时，按需查阅官方文档：

### 常用文档链接

| 问题类型 | 文档链接 |
|----------|----------|
| 故障排除总览 | https://docs.openclaw.ai/help/troubleshooting.md |
| Gateway问题 | https://docs.openclaw.ai/gateway/troubleshooting.md |
| 渠道问题 | https://docs.openclaw.ai/channels/troubleshooting.md |
| 配置问题 | https://docs.openclaw.ai/gateway/configuration.md |
| 模型问题 | https://docs.openclaw.ai/providers/models.md |
| 安装更新 | https://docs.openclaw.ai/install/updating.md |

### 使用web_fetch获取文档

```python
web_fetch(url="https://docs.openclaw.ai/xxx/xxx.md", maxChars=10000)
```

---

## 📝 输出响应模板

找到解决方案后，按以下格式输出：

```markdown
## 🔧 问题诊断

**您的问题**：{描述问题现象}

**可能原因**：{分析可能的原因}

---

## ✅ 解决步骤

请按顺序执行以下命令：

### 步骤1：{命令1}
```bash
{具体命令}
```

### 步骤2：{命令2}
```bash
{具体命令}
```

### 步骤3：{命令3}
```bash
{具体命令}
```

---

## 🔍 验证结果

执行以下命令验证问题是否解决：

```bash
{验证命令}
```

预期输出：{描述预期输出}

---

## 📖 相关文档

如需了解更多，参考：
- {官方文档链接1}
- {官方文档链接2}

---

## ❓ 如果还是不行

1. 运行 `openclaw doctor --fix` 自动修复
2. 运行 `openclaw logs --follow` 查看详细日志
3. 将日志复制到 Discord 社区寻求帮助：https://discord.gg/clawd
```

---

## 🆘 紧急情况处理

### Gateway完全无响应

```bash
# 强制停止
openclaw gateway stop

# 清理并重启
openclaw doctor --fix
openclaw gateway start
```

### 配置文件损坏

```bash
# 备份旧配置
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.backup

# 重置配置
openclaw reset --scope config

# 重新配置
openclaw configure
```

---

## 📚 参考资料

- 完整文档：https://docs.openclaw.ai/
- 故障排除：https://docs.openclaw.ai/help/troubleshooting.md
- CLI命令：https://docs.openclaw.ai/cli/index.md
- 配置参考：https://docs.openclaw.ai/gateway/configuration-reference.md
- Discord社区：https://discord.gg/clawd
```
