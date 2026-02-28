---
name: git-commit
description: "创建高质量的 git 提交：审查/暂存预期的变更，拆分为逻辑提交，并编写清晰的提交信息（遵循 Conventional Commits 规范，支持 Emoji）。当用户要求提交代码、编写提交信息、暂存变更或将工作拆分为多个提交时使用此技能。当用户提及【破坏性变更】关键词时，必须按照本技能的 BREAKING CHANGE 规范使用感叹号格式编写提交信息。优先针对 git 暂存区（staged）中的文件进行提交，只有当暂存区为空时才考虑整个工作树。当用户提及【分门别类】关键词时，必须按照本技能的多提交拆分规范，从文件类型、业务模块、修改类型、修改范围四个维度认真拆分多个提交。"
user-invocable: true
metadata:
  version: "0.2.0"
---

# Git Commit

## 来源说明

该技能本质上是参考 [agent-toolkit/skills/commit-work](https://github.com/softaworks/agent-toolkit/blob/main/skills/commit-work/SKILL.md) 文档的纯中文翻译版本，并进行了特定改写以适应当前环境。

## 目标

制作易于审查且安全发布的提交：

- 仅包含预期的变更
- 提交具有逻辑范围（必要时进行拆分）
- 提交信息描述了变更内容和原因

## 需要询问的输入（如果缺失）

- **单个提交还是多个提交？**（如果不确定：当存在不相关的变更时，默认为多个小提交。）
- **提交风格**：必须使用 Conventional Commits，并包含 Emoji。
- **任何规则**：最大标题长度，必需的作用域。

## 工作流程（清单）

1. **检查暂存区与工作树状态（优先暂存区）**
   - `git status`
   - **首先检查暂存区是否有内容**：`git diff --cached --stat`
     - ✅ **暂存区有文件**：本次提交只针对暂存区，不要自行 `git add` 额外文件。直接跳到步骤 4 审查暂存内容。
     - 📭 **暂存区为空**：才需要从工作树中选取文件进行暂存，继续步骤 2-3。
   - 如果需要查看工作树的变更：`git diff` 或 `git diff --stat`
2. **决定提交边界（必要时拆分）** [见「分门别类拆分规范」]
   - **先分析上下文**：认真阅读对话中用户描述的改动内容，理解本次修改的业务意图。
   - **四维拆分依据**：
     1. **文件类型**：配置文件 vs 源码 vs 文档 vs 测试文件
     2. **业务功能模块**：不同业务模块的改动独立提交（如 `auth` vs `payment`）
     3. **修改类型**：新增功能 vs 修复 Bug vs 重构 vs 格式化（不同 type 的改动分开）
     4. **修改范围**：前端 vs 后端，依赖升级 vs 行为变更，生产代码 vs 测试代码
   - 如果变更混合在一个文件中，计划使用补丁暂存 (`patch staging`)。
3. **仅暂存属于下一个提交的内容**（暂存区为空时才执行此步）
   - 对于混合变更首选补丁暂存：`git add -p`
   - 取消暂存块/文件：`git restore --staged -p` 或 `git restore --staged <path>`
4. **审查实际将要提交的内容**
   - `git diff --cached`
   - **合规性检查**：
     - 无密钥或令牌
     - 无意外的调试日志
     - 无不相关的格式化变动
5. **用 1-2 句话描述暂存的变更（在编写信息之前）**
   - "变更了什么？" + "为什么？"
   - 如果你无法清晰地描述它，那么提交可能太大或混合了；返回第 2 步。
6. **编写提交信息**
   - **必须**使用中文编写提交信息。
   - 使用 **Conventional Commits**（必需）：
     - 普通提交：`<emoji> type(scope): summary`
     - 破坏性变更：`<emoji> type(scope)!: summary`（感叹号紧跟在 `)` 之后，冒号之前）
     - (空行)
     - body (内容/原因，而非实现流水账)
     - footer：破坏性变更时必须包含 `BREAKING CHANGE: <说明>` 行
   - **Emoji 和 Type 规范**：必须查阅并遵循 [commit-types.ts](https://raw.githubusercontent.com/ruan-cat/monorepo/dev/configs-package/commitlint-config/src/commit-types.ts) 中的定义。
     - **主动查阅**：使用 `Read` 或 `WebFetch` 工具主动读取上述文件以获取最新的 Emoji 和 Type 列表。
   - **推荐使用文件方式提交**（解决 Windows/PowerShell 中文乱码问题）：
     - 由于 Cursor IDE 的 Shell 工具在通过 `-m` 参数传递中文时存在编码问题，推荐使用 `-F` 文件方式提交
     - 创建临时提交信息文件（如 `commit-message.txt`）
     - 使用 `git commit -F commit-message.txt` 提交
     - 提交完成后删除临时文件
   - 参考 `references/commit-message-template.md` 获取完整的模板和 Emoji 列表。
7. **运行最小的相关验证**
   - 在继续之前运行仓库中最快且有意义的检查（单元测试、lint 或构建）。
8. **重复下一个提交，直到工作树干净**

## 优先处理暂存区 [CRITICAL]

**在开始任何提交流程之前，首先检查 git 暂存区（staging area / index）是否已有文件。**

这是基于尊重用户意图的原则：如果用户已经手动 `git add` 了某些文件，说明他们明确知道要提交什么，此时不应画蛇添足地扩大提交范围。

| 暂存区状态     | 处理方式                                                    |
| :------------- | :---------------------------------------------------------- |
| **有暂存文件** | 直接对暂存区内容进行提交，**不自行 `git add` 任何额外文件** |
| **暂存区为空** | 从工作树分析所有变更，按拆分规范选取文件并暂存后再提交      |

**检查命令**：

```bash
# 检查暂存区是否有内容
git diff --cached --stat

# 有输出 → 暂存区有文件，直接进入审查流程
# 无输出 → 暂存区为空，需要从工作树选取文件
```

## 分门别类拆分提交规范 [CRITICAL]

当用户提及**「分门别类」**，或工作树中存在较多文件变更时，**必须**认真分析上下文，将变更拆分为若干个逻辑独立的小提交，而不是粗暴地一次性 `git add .` 全量提交。

### 为什么要拆分

- 每个提交都有清晰的单一职责，方便 code review 和问题追溯
- 出现问题时可以精准 `git revert` 单个提交而不影响其他变更
- 符合 Conventional Commits 语义：一个 `type` 对应一类变更

### 四个拆分维度

在分析本次变更时，请从以下四个维度逐一评估，发现可拆分点就独立成一个提交：

#### 1. 按文件类型拆分

不同类型的文件通常对应不同关注点：

- 配置文件（`*.json`, `*.yaml`, `*.toml`, `nitro.config.ts` 等）→ `config` 类型
- 文档文件（`*.md`, `CHANGELOG`, `README`）→ `docs` 类型
- 测试文件（`*.test.ts`, `*.spec.ts`）→ `test` 类型
- 依赖文件（`package.json`, `pnpm-lock.yaml`）→ `deps` 类型
- 核心源码文件 → `feat` / `fix` / `refactor` 类型

#### 2. 按业务功能模块拆分

不同业务模块的改动应独立提交，即使它们都是同一类型（如 `feat`）：

- `feat(auth): ...` 和 `feat(payment): ...` 应分开
- `fix(users): ...` 和 `fix(orders): ...` 应分开

#### 3. 按修改类型拆分

不同 `type` 的变更必须分开提交，不能混在一起：

- 新增功能（`feat`）和修复 Bug（`fix`）→ 分开
- 功能代码（`feat`/`fix`）和格式化（`style`）→ 分开
- 业务逻辑和重构（`refactor`）→ 分开

#### 4. 按修改范围拆分

- 前端代码 vs 后端代码
- 生产代码 vs 测试代码
- 应用代码 vs 基础设施/工具链代码

### 拆分决策流程

```plain
分析变更文件列表
    ↓
有没有不同 type 的混合变更？ → 是 → 按类型拆分
    ↓ 否
有没有跨越多个业务模块的变更？ → 是 → 按模块拆分
    ↓ 否
有没有配置/文档/测试等文件混在一起？ → 是 → 按文件类型拆分
    ↓ 否
变更范围是否横跨前后端或基础设施？ → 是 → 按范围拆分
    ↓ 否
所有变更都聚焦于同一职责 → 可以合并为一个提交
```

### 示例：工作树有 8 个文件的拆分方案

```plain
变更文件：
  M  src/api/users.ts          # 后端业务逻辑：新增用户查询
  M  src/api/orders.ts         # 后端业务逻辑：修复订单Bug
  M  src/components/UserList.vue # 前端组件
  M  nitro.config.ts            # 配置文件
  M  package.json               # 依赖升级
  M  pnpm-lock.yaml             # 依赖锁定文件
  M  tests/users.test.ts        # 测试文件
  M  CHANGELOG.md               # 文档

推荐拆分为 5 个提交：
  提交1: ✨ feat(users): 新增用户查询接口       ← src/api/users.ts
  提交2: 🐞 fix(orders): 修复订单数量计算错误   ← src/api/orders.ts
  提交3: ✨ feat(ui): 新增用户列表组件          ← src/components/UserList.vue
  提交4: 🧪 test(users): 补充用户查询单测       ← tests/users.test.ts
  提交5: 📦 deps: 升级依赖并更新配置            ← package.json + pnpm-lock.yaml + nitro.config.ts
  (CHANGELOG.md 通常随其他提交一起或单独 docs 提交)
```

## 破坏性变更规范 [CRITICAL]

当用户提及**「破坏性变更」**关键词，或本次变更确实存在不向下兼容的 API/行为改动时，**必须**按以下规范编写提交信息。

### 感叹号位置（唯一正确格式）

```text
<emoji> type(scope)!: summary
```

- `!` 紧跟在 `)` 之后，冒号 `:` 之前
- `!` 与 `)` 之间**不留空格**
- `!` 与 `:` 之间**不留空格**

### 错误示例 vs 正确示例

| 写法                                | 状态 | 问题说明                                   |
| :---------------------------------- | :--: | :----------------------------------------- |
| `🦄 refactor!(scope): summary`      |  ❌  | 感叹号在 type 之后、scope 之前，不符合规范 |
| `🦄 refactor(scope) !: summary`     |  ❌  | 感叹号与 `)` 之间有空格                    |
| `🦄 refactor(scope)! : summary`     |  ❌  | 感叹号与 `:` 之间有空格                    |
| `🦄 refactor(scope)!: summary`      |  ✅  | 正确——`!` 紧跟在 `)` 之后，无空格          |
| `🦄 refactor!: summary`（无 scope） |  ✅  | 无 scope 时 `!` 紧跟在 type 之后           |

### 完整破坏性变更提交模板

```text
<emoji> type(scope)!: 简短描述破坏性变更

BREAKING CHANGE: 详细说明破坏性变更的内容、原因，以及用户需要如何迁移。

- 变更点 1
- 变更点 2
```

### 示例

```text
🦄 refactor(nitro-api-development)!: 从 11comm 项目提取技能并重构为通用版本

BREAKING CHANGE: 删除了 reference.md 和 templates.md，替换为 references/ 和 templates/ 子目录结构。

- 移除 reference.md
- 移除 templates.md
- 新增 references/ 子目录（含 7 个专项文档）
- 新增 templates/ 子目录（含 2 个可复用 TypeScript 文件）
```

## 交付物

提供：

- 最终的提交信息（包含 Emoji，中文编写）
- 每个提交的简短摘要（内容/原因）
- 用于暂存/审查的命令（至少：`git diff --cached`，加上运行的任何测试）
