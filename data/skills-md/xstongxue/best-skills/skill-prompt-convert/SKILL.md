---
name: skill-prompt-convert
description: 在 Skill（SKILL.md）与 Prompt（聊天框指令）两种格式之间相互转换。支持 Skill→Prompt 与 Prompt→Skill 双向转换，保持核心信息零丢失。当用户提到 Skill 转 Prompt、Prompt 转 Skill、格式互转、SKILL.md 转换时使用。
---

# Skill 与 Prompt 互转

## 使用时机

- 用户需要将 Skill 转为可直接复制到聊天框的 Prompt
- 用户需要将 Prompt 转为 SKILL.md 格式的 Skill
- 用户提到 Skill 与 Prompt 互转、格式转换

## Step 1：获取输入并确认方向

从用户消息或粘贴/附件中获取待转换内容，判断方向：

- **A. Skill → Prompt**：输入为 SKILL.md 内容，输出聊天框可用的 Prompt
- **B. Prompt → Skill**：输入为 Prompt 内容（含 ``` 代码块），输出 SKILL.md 格式

## Step 2：执行转换

**Skill → Prompt 时**：将 `name`、`description` 融入 `# Role` 和 `# Task`；将「使用时机」转化为适用场景；将 Step 1/2... 转化为 `# Workflow` 或 `# Constraints`；补充 `# Output Format` 和 `# Input` 占位符；输出用 ``` 包裹。

**Prompt → Skill 时**：从 `# Role`、`# Task` 提炼 `name`（英文小写短横线）和 `description`；从 `# Task` 或 `# Constraints` 提炼「使用时机」；将 `# Workflow`、`# Constraints` 拆解为 Step 1、Step 2...；保留 `# Output Format` 到「注意事项」；输出完整 SKILL.md，**必须符合标准 Skill 格式**。

## Step 3：输出结果

- **Part 1 [转换说明]**：简要说明映射关系（如：Step 1 映射为 Workflow 第一步）
- **Part 2 [转换结果]**：完整的转换后内容（可直接粘贴使用）

## 注意事项

- **信息零丢失**：不得删减核心逻辑、步骤、约束条件
- **格式适配**：Skill 强调「何时触发」「Agent 如何执行」；Prompt 强调「用户输入什么」「输出什么格式」
- **命名规范**：`name` 必须英文、小写、短横线（如 `wechat-article-writer`）；reference 文件名同理（如 `outline-review-science.md`）
- **description 质量**：需包含「什么时候用」「用来干什么」及关键词
- **Skill 正文结构**：标题 → 使用时机 → Step 1/2... → 注意事项/示例；多输入任务需补充「触发时的输入方式」
- **标准 Skill 格式**：YAML 前置元数据必须用 `---` 开头和结尾闭合，使用 `name:` 和 `description:`（严禁 `## name:`），示例：
  ```
  ---
  name: skill-name
  description: 触发场景与功能描述
  ---

  # 标题
  ...
  ```