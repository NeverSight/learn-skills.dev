---
name: agent-skill-rules
description: Agent Skills 开放标准与治理规则。用于 skill 的创建、修改、重构、迁移、审计与维护，提供平台无关的结构标准、frontmatter 规范、渐进式披露与质量门禁。
---

# Agent Skill Rules

> 以 Agent Skills 官方 Step 1–4 为主流程，并在每一步中嵌入平台无关的治理增强项。

---

## Instructions（分步说明）

### Step 1：确认目录结构

每个 skill 至少包含 `SKILL.md`，可选 `scripts/`、`references/`、`assets/`。完整格式规范见 [references/specification.md](references/specification.md)（来源：[agentskills.io/specification](https://agentskills.io/specification)）。

```
skill-name/
├── SKILL.md          # Required
├── scripts/          # Optional
├── references/       # Optional
└── assets/           # Optional
```

目录名必须与 frontmatter 中的 `name` 一致（小写、连字符、1–64 字符）。

**规则设计时的命名约定**（创建/修改 skill 时适用）：除必要外，所有文件名与目录名使用小写。

- **默认**：新建或重命名的文件、目录均使用小写。
- **「必要」**：仅当规范/框架**明确要求**某命名时不改为小写（如 `SKILL.md`、`README.md`、`Makefile`）。强制规范 > 本约定。
- **不确定时**：先查该规范文档；未写明则使用小写。

**增强项（不改变主流程）**：

- 在建结构前先识别动作类型：`create / update / refactor / migrate / audit / deprecate`。
- 根据动作决定是否需要最小结构或完整结构（避免一次性过度创建目录）。
- 避免深层引用链：后续文档设计默认单层引用。

### Step 2：编写 frontmatter

必填两项：

- **name**：与目录名一致，仅 `a-z`、`0-9`、`-`，不以 `-` 开头或结尾，无 `--`
- **description**：做什么 + 何时用，含关键词，1–1024 字符，第三人称

**增强项（不改变主流程）**：

- `description` 除"做什么 + 何时用"外，补充触发关键词以提升匹配稳定性。
- 对维护类动作（update/refactor/migrate/audit/deprecate）也保持可触发语义。
- 明确平台无关：不在 frontmatter 写入平台私有字段或平台绑定术语。
- **识别 skill 类型**（详见 [references/skill-type-taxonomy.md](references/skill-type-taxonomy.md)）：判断当前 skill 属于动作型（procedural）还是约束型（declarative），据此调整 `description` 写法：
  - 动作型：「做什么 + 何时触发」
  - 约束型：「约束什么 + 适用范围」
- 可选：通过 `metadata.type` 标注类型（`procedural` / `declarative`），便于分类管理。

### Step 3：编写正文

YAML 之后为 Markdown 正文。**根据 skill 类型选择对应的正文组织方式**（详见 [references/skill-type-taxonomy.md](references/skill-type-taxonomy.md)）：

**动作型 skill（procedural）** — 沿用官方推荐：

- **Instructions**（分步说明）
- **Examples**（输入/输出示例，若适用）
- **Edge cases**（常见边界情况，若适用）

**约束型 skill（declarative）** — 不硬套步骤格式，改用声明式组织：

- **核心原则**（必须遵守的底线规则）
- **行为要求**（在具体场景下的行为规范，推荐用对照表）
- **判断标准**（如何判断是否违反原则）
- **反模式**（必须避免的行为，含具体示例）

**增强项（不改变主流程）**：

- 正文按"核心规则在前、细节下沉 references"组织（渐进式披露）。
- 同一规则只维护一处，避免 `SKILL.md` 与 `references/` 重复。
- 按任务脆弱性选择自由度：高自由度（原则）、中自由度（模式）、低自由度（硬约束）。
- 维护类任务建议加最小动作表（创建/修改/重构/迁移/审计/弃用）以提升执行一致性。
- 混合型 skill：识别主导类型，按主导类型组织正文，将次要类型的内容作为补充段落。

### Step 3.5：无损迁移（migrate 场景强制）

当动作类型为 `migrate` 或 `merge` 时，必须执行无损迁移规则：

- 迁移以“移动/复制 + 引用重组”为主，不以摘要改写替代原文。
- 原始规则文本（尤其 `SKILL.md` 与 `references/*`）必须完整保留。
- 若需要聚合入口，聚合层仅做路由与导航，不覆盖原规则细节。
- 迁移后必须可追溯：能从聚合入口定位到原始文本路径。

### Step 4：自检与验证

- [ ] 目录名 = `name`
- [ ] `description` 含「做什么」「何时用」和关键词
- [ ] 引用文件仅一层深度，用相对路径
- [ ] 若环境支持：`skills-ref validate ./skill-name`

**增强项（不改变主流程）**：

- [ ] 无平台绑定术语污染核心规则（Cloud/IDE/产品私有机制）
- [ ] 维护动作可追踪（变更摘要、影响范围、迁移路径）
- [ ] 无冗余文档堆叠（与执行无关的 README/更新日志等）
- [ ] migrate/merge 场景满足"无损迁移"：原文未被摘要化删改，聚合层仅做导航
- [ ] **类型一致性**：正文组织方式与 skill 类型匹配（动作型用 Instructions，约束型用核心原则/行为要求/判断标准/反模式）
- [ ] 约束型 skill 未硬套步骤格式，动作型 skill 未缺少执行流程

---

## 来源与演进路径

### 来源

- 第一层来源：Agent Skills 官方文档（结构、frontmatter、渐进式披露、校验约束）。
- 第二层来源：社区 skill-creator 文档中的通用方法（内容组织、迭代思路、反模式识别）。

### 吸纳策略

- 官方 Step 1–4 作为主流程骨架。
- 新增内容仅作为“增强项”并入各 Step，不替换主流程。
- 明确剔除 Cloud/IDE/产品私有绑定内容，保留平台无关规则。

---

## 定位与边界

- 本 skill 负责规则标准与治理流程，不绑定特定平台。
- 默认采用静态规则与文档校验，不依赖固定脚本链路。
- 关注可迁移、可维护、可审计的 skill 设计质量。

---

## 反模式（必须避免）

- 将规则绑定到特定 Cloud/IDE/产品私有能力。
- 把平台安装、打包、发布统计写入规则正文。
- 在 skill 中堆放与执行无关的辅助文档（如通用 README、更新日志）。
- 在 `SKILL.md` 与 `references/` 重复维护同一说明。
- 用精简摘要替代原始规则正文，导致迁移失真与细节丢失。
- **将约束型 skill 硬套进 Instructions/Step 1-2-3 格式**，导致内容牵强或丢失"始终生效"的语义。
- **将动作型 skill 写成纯声明式**，导致缺少可执行的步骤流程。

---

## 参考资料

- `references/specification.md` - Agent Skills 基础规范与字段约束
- `references/anthropic-enhancements.md` - 基于 Anthropic skill-creator 的平台无关增强提炼（含来源与剔除策略）
- `references/skill-type-taxonomy.md` - Skill 类型分类学：动作型（procedural）vs 约束型（declarative）的组织方式指导

---
