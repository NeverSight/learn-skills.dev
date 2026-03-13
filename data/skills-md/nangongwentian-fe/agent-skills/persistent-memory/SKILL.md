---
name: persistent-memory
description: 通用跨会话记忆协议（Universal Memory Protocol）。让所有 AI 编程工具共享同一套记忆系统。适用 Claude Code / Cursor / Aider / Cline / Codex / Trae / OpenCode。能力：智能分类 / FSRS 衰减 / 月度压缩 / 多层检索。触发：用户说"记住"；问"之前"；检测到敏感信息；会话结束。
---

# Persistent Memory — 通用记忆协议

## Quick Start

```bash
# 首次初始化（详见 references/setup.md）
mkdir -p ~/.persistent-memory/{memories,journal,archive,.sensitive}
```

## 核心原则

1. **用户说"记住" = 立刻分类写入**
2. **所有写入必须更新 INDEX.md**
3. **自动检测信息类型 → 写入对应分类文件**
4. **敏感信息 → .sensitive/ 目录（不同步）**
5. **定期衰减检查 + 月度压缩归档**

## 文件结构

```
~/.persistent-memory/
├── INDEX.md              # 记忆索引（AI 首先读取）
├── MEMORY.md             # 核心长期记忆（精炼摘要）
├── SOUL.md               # 用户画像/偏好
├── HEARTBEAT.md          # 心跳清单
├── memories/
│   ├── facts.md          # 事实：账号、配置、技术栈
│   ├── decisions.md      # 决策：架构选型、技术方案
│   ├── preferences.md    # 偏好：编码风格、工具习惯
│   └── context.md        # 上下文：项目背景、业务逻辑
├── journal/
│   └── YYYY-MM-DD.md     # 每日日志
├── archive/
│   └── YYYY-MM.md        # 月度压缩归档
└── .sensitive/            # 敏感信息（gitignored）
```

## 记忆分类速查

| 类型 | 文件 | 写入示例 |
|------|------|----------|
| 事实 | memories/facts.md | 账号、配置、技术栈版本、IP 地址 |
| 决策 | memories/decisions.md | 架构选型、技术方案、为什么选 A 不选 B |
| 偏好 | memories/preferences.md | 代码风格、工具习惯、"总是用 pnpm" |
| 上下文 | memories/context.md | 项目背景、业务逻辑、团队信息 |
| 用户画像 | SOUL.md | 性格、沟通风格、称呼、工作方式 |
| 每日 | journal/YYYY-MM-DD.md | 今天完成的事、发现的问题、临时笔记 |

## 会话开始

```bash
# 必须读取
cat ~/.persistent-memory/INDEX.md
cat ~/.persistent-memory/MEMORY.md

# 可选读取
cat ~/.persistent-memory/SOUL.md
cat ~/.persistent-memory/journal/$(date +%Y-%m-%d).md 2>/dev/null
```

读取后告知用户：「已加载你的记忆，共 X 条长期记忆，今日已有 Y 条日志」

## 触发场景

| 触发 | 行为 |
|------|------|
| 用户说"记住xxx" | 判断分类 → 写入 → 更新 INDEX |
| 用户问"之前怎样" | 三层检索（见 retrieval.md） |
| 检测到 API key/账号 | 提示用户是否记录到 .sensitive/ |
| 完成重要任务 | 提示记录到 journal/ |
| 会话结束 | 更新访问计数 → 更新 INDEX → 写 journal |
| 每月首日 | 提示月度压缩（见 intelligence.md） |

## 写入流程（4 步）

1. **判断分类**：根据内容判断属于 facts/decisions/preferences/context/journal
2. **生成条目**：创建条目 ID（格式 `X-YYYYMMDD-NNN`）+ 元数据（日期/重要度/标签）
3. **写入文件**：追加到对应分类文件
4. **更新 INDEX**：重写 INDEX.md（更新统计、最近新增、分类摘要）

### 条目格式

```markdown
### [F-20260228-001] 标题
- **创建**: 2026-02-28
- **最近访问**: 2026-02-28
- **访问次数**: 1
- **重要度**: high|medium|low
- **标签**: tag1, tag2

正文内容...
```

### ID 规则

- `F` = Facts, `D` = Decisions, `P` = Preferences, `C` = Context
- 格式：`[类型]-[YYYYMMDD]-[当日序号]`

## 向后兼容

会话开始时自动检测：
- INDEX.md 存在 → 新版，正常流程
- 仅 MEMORY.md + memory/ 目录 → 旧版，提示迁移（见 migration.md）
- 都没有 → 新用户，引导初始化（见 setup.md）

---

## 更多内容（渐进式披露）

- **首次安装**: [references/setup.md](references/setup.md)
- **日常工作流**: [references/workflow.md](references/workflow.md)
- **记忆智能（分类/衰减/压缩）**: [references/intelligence.md](references/intelligence.md)
- **检索策略**: [references/retrieval.md](references/retrieval.md)
- **命令参考**: [references/commands.md](references/commands.md)
- **多工具适配**: [references/adapters/overview.md](references/adapters/overview.md)
- **数据迁移**: [references/migration.md](references/migration.md)
- **GitHub 云同步**: [references/sync.md](references/sync.md)
