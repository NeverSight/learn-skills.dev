---
name: openclaw-config-helper
description: "OpenClaw 配置修改助手。修改任何 OpenClaw 配置前必须先查阅官方文档，确保格式正确，避免系统崩溃或功能异常。强制执行：查 schema → 查文档 → 确认 → 修改的流程。"
license: MIT
metadata:
  version: 1.0.0
  domains: [openclaw, config, safety]
  type: automation
  priority: critical
---

# OpenClaw Config Helper - 配置修改安全助手

## ⚠️ 强制规则

**修改任何 OpenClaw 配置前，必须完成以下步骤，否则可能导致系统崩溃或功能异常！**

## 当使用此技能

- 用户要求修改 OpenClaw 配置（openclaw.json、agents 配置、channels 配置等）
- 用户要求添加/修改 Telegram、WhatsApp 等渠道配置
- 用户要求修改 bindings、models、agents.list 等
- 任何涉及 `gateway action=config.patch` 或 `gateway action=config.apply` 的操作

## 触发词

- "修改配置"
- "改一下 openclaw 配置"
- "添加一个 binding"
- "配置 telegram/whatsapp"
- "改 groupPolicy"
- "添加一个 agent"

## 强制流程（必须按顺序执行）

### 步骤 1: 查阅 Schema

```bash
# 获取完整配置 schema
gateway action=config.schema
```

**检查要点**：
- 确认要修改的字段类型（string/number/array/object）
- 确认字段是否必填
- 确认字段的允许值（enum）
- 确认嵌套结构

### 步骤 2: 查阅官方文档（如 schema 不够清晰）

```bash
# 使用 web_fetch 获取官方文档
web_fetch: https://docs.openclaw.ai/channels/telegram
web_fetch: https://docs.openclaw.ai/channels/whatsapp
web_fetch: https://docs.openclaw.ai/gateway/configuration-reference
```

**或者使用搜索**：
```bash
cd ~/clawd/skills/tavily && ./scripts/tavily.sh search "OpenClaw <配置项> 配置"
```

### 步骤 3: 展示修改方案并确认

向用户展示：
1. **当前配置**（如适用）
2. **计划修改**（具体 JSON 片段）
3. **修改原因**
4. **可能影响**

**等待用户确认后才执行修改！**

### 步骤 4: 执行修改

```bash
# 使用 config.patch 进行部分修改（推荐）
gateway action=config.patch raw='{"修改的路径": "值"}'

# 或使用 config.apply 进行完整替换（谨慎使用）
gateway action=config.apply raw='{"完整配置": "..."}'
```

### 步骤 5: 验证修改

```bash
# 检查配置是否生效
gateway action=config.get

# 检查 Gateway 状态
openclaw status
```

## 常见配置错误案例

### 案例 1: Telegram groupAllowFrom 错误 (2026-02-22)

**错误**：把群 ID 放在 `groupAllowFrom` 里
```json
// ❌ 错误
"groupAllowFrom": [-1003531486855, -1003890797239]  // 这是群 ID，不是用户 ID！

// ✅ 正确
"groupAllowFrom": ["8518085684"]  // 用户 ID
"groups": {
  "-1003531486855": {"groupPolicy": "open", "requireMention": true}
}
```

**教训**：`groupAllowFrom` 是发送者白名单（用户 ID），`groups` 是群组白名单（群 ID）

### 案例 2: 缺少 binding 导致 bot 无响应

**错误**：主 bot (default account) 没有绑定到任何 agent
```json
// ❌ 缺少 default → main 的绑定
"bindings": [
  {"agentId": "ops", "match": {"accountId": "xiaoops"}},
  // ... 其他 bot，但没有 default
]

// ✅ 必须添加
"bindings": [
  {"agentId": "main", "match": {"channel": "telegram", "accountId": "default"}},
  // ... 其他
]
```

### 案例 3: pass: 格式的 apiKey 不被支持

**错误**：OpenClaw 不支持 `pass:` 格式的 apiKey 引用
```json
// ❌ 错误
"apiKey": "pass:api/xingsuancode"  // 会被当作字符串直接发送

// ✅ 正确
"apiKey": "sk-f873092ea177b75b..."  // 必须硬编码真实 key
```

## 快速参考

| 配置项 | 类型 | 说明 |
|--------|------|------|
| `allowFrom` | 用户 ID 数组 | DM 白名单（用户 ID） |
| `groupAllowFrom` | 用户 ID 数组 | 群组发送者白名单（用户 ID） |
| `groups` | 对象 | 群组配置（群 ID 作为 key） |
| `bindings` | 数组 | accountId → agentId 映射 |
| `accounts` | 对象 | 多账号配置（key 是 accountId） |

## 检查清单

修改配置前，确认：
- [ ] 已查阅 `config.schema` 确认字段类型
- [ ] 已查阅官方文档确认用法
- [ ] 已向用户展示修改方案并获得确认
- [ ] 使用 `config.patch` 而非 `config.apply`（除非必要）
- [ ] 修改后验证配置生效

## 记住

**永远不要想当然地修改配置！先查文档，再改配置！**
