---
name: simplify-instructions-for-smart-ai-agents
description: 当用户要求精简某个或某些 skill、AGENTS.md，减少冗余指令或过度约束时使用。
disable-model-invocation: true
---

重构我的 `Agent Skill 文件` 和/或 `AGENTS.md 文件`。保留指令的实际作用，减少冗余和不必要的步骤限制，并使其符合渐进式披露原则。

术语：

- `Agent Skill 文件`：位于 `.agents/skills`、`.claude/skills` 等目录中的 Agent Skill 相关的文件
- `AGENTS.md` 文件：位于项目根目录或递归嵌套子目录中的 `AGENTS.md`、`CLAUDE.md`、`GEMINI.md` 等文件

## 一、确定处理目标

如果某个具体的 skill 或具体的 `AGENTS.md` 已经被指定，那就仅处理那个目标；

否则，将当前目录视作待处理工作区，找出其中的所有 `Agent Skill 文件` 和 `AGENTS.md 文件`，将它们纳入处理目标的范围。

## 二、处理 `AGENTS.md 文件`

按照以下步骤处理 `AGENTS.md 文件`：

1. **找出矛盾之处**：在处理目标中寻找矛盾。对于每处互相冲突的内容，询问我希望保留哪个版本。
2. **确定核心内容**：提取应当写入根目录 `AGENTS.md` 的核心内容，包括：
   - 一句话项目描述
   - 包管理器（如果非标准，例如一个 Node.js 项目使用了 `pnpm` 而非 `npm`）
   - 非标准的构建/类型检查命令
   - 真正与**每个**任务都相关的知识或实际约束
3. **将剩余内容分组**：将剩余的说明整理成逻辑分类（例如，TypeScript 规范、测试模式、API 设计、Git 工作流）。为每个组创建一个单独的 Markdown 文件。
4. **建立目录结构**：输出：
   - 一个最小化的、位于根目录的 `AGENTS.md` 文件，其中包含指向各独立文件的 Markdown 链接
   - 位于 `docs/` 下的单独的 Markdown 文件，如 `docs/ARCHITECTURE.md`、`docs/DEPLOYMENT.md` 等
5. **标记待删除内容**：识别出符合以下情况的内容：
   - 冗余（不用说你也知道应该这么做的指示内容）
   - 过于模糊、无法确定应该怎么做的指示内容
   - 过于显而易见（例如“编写整洁的代码”）
6. **检查修改边界**：权限边界、用户明确的偏好，以及易出错流程的必要要求应当保留。约束用途不明时，先保留或询问，避免擅自放宽。

## 三、处理 `Agent Skill 文件`

按照以下步骤处理 `Agent Skill 文件`，并将结果统一写入 `.agents/skills` 目录：

1. **重写冗长的、吸引力过强的 Skill 描述**：Skill 的 `description` 应该精炼、具体地描述其工作范围，避免 Agent 在用不到它时错误地读取了它：
    - 修改前：“创建和验证 Postgres 数据库结构迁移。处理数据库、查询、模型或持久化时使用。”
    - 修改后：“创建和验证 Postgres 数据库结构迁移。新增或修改迁移，或审查迁移上线方案时使用。”
2. **重写 Skill 中过于精细、具体的指令**：Skill 中不再需要那些措辞严厉、精细具体的步骤或指令
3. **建立目录结构**：如果 Skill 较为复杂，可建立目录结构，将较长的分支说明移入 `references/` 下的独立文件中，并在主文件 `SKILL.md` 中留下指向各独立文件的 Markdown 链接。例如：`涉及服务边界时阅读 [ARCHITECTURE.md](references/ARCHITECTURE.md)，修改数据库结构时阅读 [DATABASE.md](references/DATABASE.md)，准备部署时阅读 [DEPLOYMENT.md](references/DEPLOYMENT.md)。`。简短的 Skill 保持单文件即可。
