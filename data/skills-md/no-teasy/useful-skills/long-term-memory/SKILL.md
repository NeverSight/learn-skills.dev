---
name: long-term-memory
description: Use when users want to maintain persistent memory across sessions, track user preferences, store important decisions, manage tasks and reminders, or provide personalized service with cross-session context.
---

# 长期记忆管理

## Overview

让 AI 助手拥有跨会话的持久化记忆能力，记住用户信息、偏好、历史交互和重要事项，提供个性化、连续性的智能服务。

**核心原则**：
- 第一次对话必须先检查配置状态 → 引导配置 → 加载全部记忆
- 对话中时刻识别可记录信息
- 主动管理记忆（更新、删除、关联、搜索）

## When to Use

**使用此技能当**：
- 用户提到个人信息（职业、地点、家庭情况）
- 用户表达偏好（沟通风格、输出格式）
- 用户做出重要决定或承诺
- 用户提到待办事项或提醒
- 用户分享知识经验或业务规则
- 需要跨会话的上下文连续性

**不使用**：
- 一次性对话，无需后续跟进
- 纯技术性、无个人化需求的问题

## Quick Reference

| 任务 | 命令 |
|------|------|
| **检查配置** | `python scripts/check_config.py` |
| **直接写入配置** | `python scripts/check_config.py --write --api-key sk-xxx [--base-url https://...] [--model text-embedding-3-large]` |
| **首次加载** | `python scripts/load_context.py --mode all` |
| **语义搜索** | `python scripts/load_context.py --mode all --query "关键词"` |
| **添加长期记忆** | `python scripts/manage_memories.py add --file <文件> --title "标题" --content "内容"` |
| **搜索长期记忆** | `python scripts/manage_memories.py search --query "关键词"` |
| **更新长期记忆** | `python scripts/manage_memories.py update --file <文件> --title "标题" --content "新内容"` |
| **删除长期记忆** | `python scripts/manage_memories.py delete --file <文件> --title "标题"` |
| **添加短期记忆** | `python scripts/manage_short_term.py add --content "内容" --agent chat` |
| **查看今天记忆** | `python scripts/manage_short_term.py show` |
| **向量搜索** | `python scripts/vector_store.py query --query "关键词" --top-k 5` |
| **验证安装** | `python scripts/setup_check.py` |

## Core Workflow

### 1. 首次对话 - 检查配置 → 引导配置 → 加载全部记忆（强制性）

**执行流程**：
```
检测用户第一条消息
    ↓
检查配置状态（必须！）
    ├─ 未配置 → 引导用户配置 → 配置完成后加载记忆
    └─ 已配置 → 直接加载全部记忆
```

**第一步：检查配置状态**
```bash
python scripts/check_config.py
```

**配置状态判断**：
- ✅ **存在** `configured.txt` → 配置已完成
- ❌ **不存在** `configured.txt` → 配置未完成，必须引导用户

**第二步：直接写入配置（如未完成）**
```bash
python scripts/check_config.py --write --api-key sk-xxx
```

**可选参数**：
- `--base-url https://api.example.com` - API Base URL（可选）
- `--model text-embedding-3-large` - 嵌入模型（可选，默认：text-embedding-3-small）

**引导时向用户说明**：
> "我发现记忆系统还没配置，请提供您的 OpenAI API Key，我来帮您完成配置。"

**获取 API Key 后直接写入**：
> 用户提供 API Key 后，直接运行写入命令，无需用户交互确认。

**第三步：加载全部记忆（配置完成后）**
```bash
python scripts/load_context.py --mode all
```

**完整加载流程**：
1. 检测用户第一条消息
2. **先检查配置状态**
3. 如未配置→引导配置
4. 运行加载命令
5. 自动归档过期短期记忆（>24 小时）
6. 加载长期记忆 + 当天短期记忆
7. 总结记忆要点
8. 根据记忆调整交互方式
9. 开始回复

**内心独白示例**：
> "用户第一条消息，先检查配置。
> 配置已完成，现在加载记忆。
> 加载完成，共 13 条长期记忆，2 条当天短期记忆。
> 用户是产品经理，在北京工作，喜欢简洁回复。
> 好的，现在可以开始回复了。"

**跳过配置检查是严重错误！不加载记忆就回复是严重错误！**

### 2. 对话中 - 无感记录

**核心原则**：默默记录，不要打断对话流程

**使用场景**：
- **长期记忆**：用户偏好、个人信息、重要决定、知识经验 → 使用 `manage_memories.py`
- **短期记忆**：当天临时信息、待跟进事项、Agent 间消息 → 使用 `manage_short_term.py`

```
用户输入 → 识别可记录信息 → 后台记录 → 继续正常对话
```

**识别模式**：

| 信息类型 | 用户表达示例 | 记录到 | 记忆类型 |
|----------|--------------|--------|----------|
| 个人信息 | "我是产品经理"、"我在北京" | user-profile.md | 长期 |
| 偏好声明 | "我喜欢简洁回复"、"用表格" | user-preferences.md | 长期 |
| 重要决定 | "我决定选 A"、"下周执行" | decisions-context.md | 长期 |
| 待办事项 | "记得提醒我"、"周三前完成" | tasks-reminder.md | 长期 |
| 知识经验 | "这个流程是..."、"注意..." | knowledge-base.md | 长期 |
| 临时信息 | "下周要搬家"、"上午有体检" | 短期记忆文件 | 短期 |
| Agent 消息 | "告诉健康助手用户要体检" | 短期记忆文件 | 短期 |

**正确做法**：
```
用户：我是做产品经理的，平时工作比较忙
      ↓
AI：（后台运行 manage_memories.py add --file user-profile.md ...）
    那您平时喜欢怎么放松呢？
```

**错误做法**：
```
❌ AI：我记一下，您是产品经理对吗？好的已记录...
   （打断对话，破坏体验）
```

**不要询问确认！不要告诉用户你在记录！默默记录，继续对话！**

### 3. 短期记忆到期评估

**时机**：每次加载记忆时，检查昨天的短期记忆（即将归档）

**核心原则**：AI 自主评估，自主决定，无需询问用户

**评估流程**：
```
检查昨天短期记忆 → AI 自主识别有价值内容 → 自动转入长期记忆 → 继续对话
```

**评估标准**（满足任一即应转入长期）：
- ✅ 用户偏好或习惯（如"我喜欢简洁回复"）
- ✅ 重要个人信息（如"准备考 PMP 证书"、"搬到新地址"）
- ✅ 长期待办或承诺（如"每周健身 3 次"）
- ✅ 重要知识或经验（如"工作流中的关键步骤"）
- ❌ 临时性信息（已完成的、一次性的）→ 让其自然归档

**示例**：
```
用户：（昨天说过）我准备考 PMP 证书，已经报名了
      ↓
AI：（后台检查短期记忆，识别为重要个人发展计划）
    （自动运行 manage_memories.py add --file tasks-reminder.md ...）
    （继续正常对话，不提及转移操作）
```

**完全无感！不要询问！不要告诉用户！AI 自主决定，自动转移！**

### 4. 后续对话 - 按需加载

```bash
# 默认模式（长期 + 当天短期 + 检查昨天记忆）
python scripts/load_context.py --mode all

# 语义搜索（附加向量检索）
python scripts/load_context.py --mode all --query "旅行"

# 仅向量搜索
python scripts/load_context.py --mode vector --query "旅行"
```

## Memory System

### 长期记忆 vs 短期记忆

| 特性 | 长期记忆 | 短期记忆 |
|------|----------|----------|
| **用途** | 持久化信息（偏好、个人信息、知识） | 临时信息（当天对话、临时待办） |
| **保留时间** | 永久保存，手动删除 | 24 小时后归档，30 天后删除 |
| **组织方式** | 按类别分 5 个文件 | 按日期分文件（`2026-03-11.md`） |
| **加载方式** | 每次对话全量加载 | 自动加载当天文件 |
| **典型内容** | "我喜欢简洁回复"、"我是产品经理" | "用户说下周要搬家"、"上午有体检" |

### 长期记忆文件（5 个）

```
memories/
├── user-preferences.md      # 用户偏好和习惯
├── user-profile.md          # 用户个人信息和背景
├── decisions-context.md     # 重要决定和上下文
├── tasks-reminder.md        # 待办事项和提醒
└── knowledge-base.md        # 知识和经验积累
```

### 短期记忆文件（按日期）

```
short-term/
├── 2026-03-11.md              # 今天的短期记忆
├── 2026-03-10.md              # 昨天的（待归档）
└── archived/                  # 归档目录（30 天后清理）
```

**自动归档**：每次运行 `load_context.py --mode all` 时自动检查并归档>24 小时的文件。

### 向量记忆（语义搜索）

**用途**：存储短期记忆的向量，支持语义搜索（搜"体检"也能找到"医院检查"）。

**注意**：长期记忆已全量加载到上下文，不需要向量化。

```bash
# 语义搜索
python scripts/load_context.py --mode all --query "旅行"

# 仅向量搜索
python scripts/load_context.py --mode vector --query "旅行"
```

### 记忆条目格式

```markdown
## [记忆标题]

<!-- @meta category: 类别 | tags: 标签 1, 标签 2 | created: YYYY-MM-DD | updated: YYYY-MM-DD -->

记忆内容...

### 相关记忆（可选）
- 参见 [[其他记忆标题]](其他文件.md#其他记忆标题)

<!-- @end -->
```

### 各类记忆示例

**user-preferences.md**：
```markdown
## 沟通风格偏好

<!-- @meta category: preferences | tags: 沟通风格，输出格式 | created: 2026-03-11 -->

- 回复风格：简洁直接，避免冗长解释
- 输出格式：优先使用表格和列表
- 语言风格：专业但友好

<!-- @end -->
```

**user-profile.md**：
```markdown
## 职业背景

<!-- @meta category: profile | tags: 职业，工作 | created: 2026-03-11 -->

- 职业：产品经理
- 行业：互联网/科技
- 工作地点：北京

<!-- @end -->
```

**tasks-reminder.md**：
```markdown
## 孩子疫苗接种提醒

<!-- @meta category: tasks | tags: 提醒，健康 | created: 2026-03-10 -->

**提醒事项**：带孩子接种百白破疫苗第三针
**截止日期**：2026-03-25
**优先级**：高

<!-- @end -->
```

## Common Mistakes

| 错误 | 正确做法 |
|------|----------|
| ❌ 跳过配置检查 | ✅ 第一条消息后先检查配置 |
| ❌ 忘记首次加载记忆 | ✅ 配置完成后立即运行 `--mode all` |
| ❌ 等到对话结束才记录 | ✅ 识别后立即后台记录 |
| ❌ 询问用户确认 | ✅ 默默记录，不打断对话 |
| ❌ 告诉用户"我已记录" | ✅ 继续对话，不提及记录 |
| ❌ 加载所有向量记忆 | ✅ 向量搜索必须指定 `--query` 关键词 |
| ❌ 忽略记忆管理 | ✅ 主动更新、删除、关联、搜索 |
| ❌ 询问用户是否转移 | ✅ AI 自主评估，自动转移 |
| ❌ 告诉用户"我转储记忆" | ✅ 默默转移，不提及操作 |

## Red Flags - STOP

- 准备回复用户但还没检查配置 → **STOP，先检查配置**
- 准备回复用户但还没加载记忆 → **STOP，先加载**
- 想"等会儿再记录" → **STOP，立即记录**
- 想告诉用户"我记一下" → **STOP，默默记录**
- 想询问确认"您是...对吗？" → **STOP，直接记录**
- 想询问"要转入长期记忆吗" → **STOP，自主决定，直接转移**
- 想告诉用户"我已转移记忆" → **STOP，保持沉默**

## Configuration

**检查配置状态**：
```bash
python scripts/check_config.py
```

**配置完成后会创建** `configured.txt` **文件**：
- 存在 → 配置完成，不会再次引导
- 不存在 → 配置未完成，AI 会引导配置

**重新配置**：
```bash
python scripts/check_config.py --reset
python scripts/check_config.py --guide
```

**验证安装**：
```bash
python scripts/setup_check.py
```

## Related Files

**核心文档**：
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - 完整配置向导
- [assets/memory_template.md](assets/memory_template.md) - 记忆条目模板

**脚本文件**：
- `scripts/load_context.py` - 统一记忆加载
- `scripts/manage_memories.py` - 长期记忆管理
- `scripts/manage_short_term.py` - 短期记忆管理
- `scripts/vector_store.py` - 向量存储管理

**参考文档**：
- `references/linking.md` - 记忆间双向链接
- `references/example_memories.md` - 记忆示例

---

*详细使用说明：[references/usage.md](references/usage.md)*
