---
name: code-review:config-manager
description: This skill should be used when the user asks to "manage review skills config", "update review skills", "discover review skills", "manage review presets", "validate review config", or mentions managing code review skills configuration. Use for configuration management tasks.
---

# Code Review 配置管理器

管理 code review skills 和 commands 的配置文件，包括自动发现能力、管理预设配置、验证配置等。

## 能力类型

配置管理器支持两种类型的 review 能力：

- **skill**: SKILL.md 格式的技能文件
- **command**: 插件中的命令（`~/.claude/plugins/cache/*/commands/*.md`）

**自动排除**: 发现过程中会自动排除自身（`code-review:config-manager` 和 `code-review:executor`），避免循环依赖。

## 配置文件位置

配置文件支持三级优先级（级联覆盖）：

- **全局配置**: `~/.config/claude/code-review-skills/config.yaml`
- **用户配置**: `~/.claude/code-review-skills/config.yaml`
- **项目配置**: `.claude/code-review-skills/config.yaml`

优先级：项目 > 用户 > 全局

## 工作流程

### Step 0: 识别用户意图

首先确定用户想要做什么：

- **初始化配置**: 用户说 "初始化 review 配置"、"创建配置文件"
- **发现/更新 skills**: 用户说 "更新 skills"、"发现 skills"、"同步 skills"
- **管理预设**: 用户说 "管理预设"、"编辑预设"、"创建预设"
- **查看配置**: 用户说 "查看配置"、"显示配置"、"配置状态"
- **验证配置**: 用户说 "验证配置"、"检查配置"

根据用户意图，跳转到相应的步骤。

---

### Step 1: 初始化配置（可选）

当用户首次使用或需要创建新配置时执行。

#### 1.1 确定配置层级

询问用户要在哪个层级创建配置：

- 项目配置（推荐用于特定项目）
- 用户配置（推荐用于个人默认配置）
- 全局配置（推荐用于系统级默认）

#### 1.2 创建默认配置

运行 `scripts/init-config.sh` 创建默认配置文件：

```bash
# 项目配置
./scripts/init-config.sh --project

# 用户配置
./scripts/init-config.sh --user

# 全局配置
./scripts/init-config.sh --global
```

#### 1.3 确认创建成功

验证配置文件已创建并显示路径。

**完成初始化后，跳转到 Step 2 发现 skills。**

---

### Step 2: 自动发现并更新 Review 能力

扫描环境中所有可用的 skills 和 commands，识别与 code review 相关的能力。

**首先运行自动发现脚本：**

```bash
./scripts/discover-skills.sh [配置文件路径]
```

如果未指定配置文件路径，脚本会自动按优先级查找（项目 > 用户 > 全局）。

脚本会自动完成以下工作：
- 读取配置文件中的 `skills_directories` 字段确定搜索目录
- 扫描所有 SKILL.md 文件（skills）
- 扫描 `~/.claude/plugins/cache/` 下的所有 commands
- 识别 review 相关的能力（通过关键词过滤）
- 自动排除自身（`code-review:config-manager`, `code-review:executor`）
- 对相同 ID 的 commands 去重（保留最新版本）
- 提取能力元信息（name、description、category、tags、type）
- 更新配置文件的 `available_skills` 部分（保留用户已编辑的 presets）

**如果脚本执行失败或用户需要手动控制，按以下步骤操作：**

#### 2.1 确定 Skills 搜索目录（手动备选）

**首先**，读取配置文件中的 `skills_directories` 字段。

如果配置文件中没有此字段或为空，使用以下默认策略：

**策略 1: 优先搜索项目内的 skills 目录**
```
Glob: skills/**/SKILL.md
Glob: .skills/**/SKILL.md
```

**策略 2: 如果策略 1 未找到，搜索更广泛的范围但排除常见无关目录**
```
Glob: */SKILL.md
Glob: */*/SKILL.md
```

**排除的无关目录**:
- node_modules/
- .git/
- vendor/
- dist/
- build/
- target/
- __pycache__/
- .venv/

**策略 3: 搜索插件 commands**

搜索 `~/.claude/plugins/cache/` 目录下的 commands：
```
Glob: ~/.claude/plugins/cache/*/commands/*.md
Glob: ~/.claude/plugins/cache/*/*/commands/*.md
```

排除 `temp_git*` 和 `.orphaned_at` 目录。

**策略 4: 询问用户 skills 位置**

如果前几种策略都找不到足够的能力，询问用户 skills 目录的路径。

**添加自定义搜索目录:**

如果用户需要搜索其他位置的 skills，编辑配置文件添加 `skills_directories` 字段：

```yaml
skills_directories:
  - "skills"              # 项目内 skills 目录
  - "../my-skills/skills"  # 其他项目的 skills 目录
  - "~/.claude/skills"     # 用户级 skills 目录
```

使用 Glob 工具对每个目录执行 `**/SKILL.md` 搜索（限制在指定目录内）。

#### 2.2 识别 Review 相关能力（手动备选）

对每个 SKILL.md 文件和 command 文件，使用 Read 工具读取 frontmatter（`---` 之间的内容）。

通过关键词判断是否是 review 相关的能力：
- review, auditor, reviewer
- security, audit, threat
- test, testing, coverage
- performance, optimization
- quality, cleanup, lint

同时检查 description 中是否包含这些关键词。

**排除自身**: 跳过 `code-review:config-manager` 和 `code-review:executor`。

#### 2.3 提取能力元信息（手动备选）

对于每个识别出的能力，提取以下信息：

```yaml
id: "plugin:command-name"   # 对于 command: plugin:command
id: "skill:name"            # 对于 skill: 从 SKILL.md 的 name 字段
name: "显示名称"            # 从 name 字段
type: "skill" | "command"   # 能力类型
category: "分类"            # 根据 description 推断
description: "描述"         # 从 description 字段
tags: ["tag1", "tag2"]      # 从 description 推断
recommended_for: ["场景"]   # 基于 category 和 description
```

**分类规则：**
- 包含 "security", "audit", "threat" → "安全审计"
- 包含 "test", "coverage", "tdd" → "测试+清理"
- 包含 "performance", "optimization", "database" → "性能+架构"
- 包含 "code-quality", "lint", "cleanup" → "代码质量"
- 其他 → "代码质量"

#### 2.4 更新配置文件（手动备选）

将提取的能力添加到配置文件的 `available_skills` 部分。

**重要**: 更新时需要保留用户已编辑的 presets。

读取当前配置文件，保留 `presets` 部分，只更新 `available_skills` 和 `metadata.last_updated`。

使用 Edit 工具更新配置文件：

```yaml
metadata:
  version: "0.2.0"
  last_updated: "2025-01-15"  # 当前日期

available_skills:
  - id: "code-review:code-review"
    name: "code-review:code-review"
    type: "command"
    category: "安全审计"
    description: "..."
    tags: ["review", "security"]
    recommended_for: ["所有项目"]
  # ... 更多能力
```

#### 2.5 显示更新结果

向用户报告：
- 发现了多少个 skills
- 发现了多少个 commands
- 按分类分组显示
- 更新的配置文件路径

---

### Step 3: 管理预设配置

允许用户创建、编辑、删除预设配置。

#### 3.1 显示当前预设

使用 Read 工具读取配置文件，提取 `presets` 部分。

向用户展示当前的预设列表：

```
当前预设配置：

1. 快速审查 (2 个 skills)
   - code-review:code-review
   - codebase-cleanup:code-reviewer

2. 全面审查 (5 个 skills)
   - code-review:code-review
   - security-scanning:security-auditor
   ...

3. 安全优先 (3 个 skills)
   ...
```

#### 3.2 询问用户操作

使用 AskUserQuestion 让用户选择操作：

- 创建新预设
- 编辑现有预设
- 删除预设
- 复制预设

#### 3.3 执行相应操作

**创建新预设:**
1. 询问预设名称
2. 询问描述
3. 显示所有可用的 skills（按分类分组）
4. 让用户选择 skills（AskUserQuestion，multiSelect=true）
5. 将新预设添加到配置文件

**编辑预设:**
1. 让用户选择要编辑的预设
2. 显示当前包含的 skills
3. 询问要添加/删除哪些 skills
4. 更新配置文件

**删除预设:**
1. 让用户选择要删除的预设
2. 确认删除操作
3. 从配置文件中移除

**复制预设:**
1. 让用户选择要复制的预设
2. 询问新预设名称
3. 复制并添加到配置文件

#### 3.4 保存并验证

使用 Edit 工具更新配置文件。

运行 `scripts/validate-config.sh` 验证配置是否正确。

---

### Step 4: 查看配置状态

显示当前配置的详细信息。

#### 4.1 显示配置文件路径

按优先级检查三个层级，显示哪些配置文件存在：

```
配置文件状态：

✓ 项目配置: .claude/code-review-skills/config.yaml
✓ 用户配置: ~/.claude/code-review-skills/config.yaml
- 全局配置: 不存在

当前生效的配置将合并上述文件（项目配置优先级最高）
```

#### 4.2 显示可用 Skills

读取配置文件的 `available_skills`，按分类分组显示：

```
可用 skills (共 15 个):

代码质量 (6):
  - code-review:code-review - 基础代码审查
  - codebase-cleanup:code-reviewer - 代码清理审查
  ...

安全审计 (4):
  - security-scanning:security-auditor - 安全审计专家
  - security-scanning:threat-modeling-expert - 威胁建模专家
  ...

性能+架构 (3):
  - application-performance:performance-engineer - 性能工程师
  ...
```

#### 4.3 显示预设配置

显示所有预设及其包含的 skills（同 Step 3.1）。

#### 4.4 显示合并结果（可选）

如果存在多层级配置，运行 `scripts/merge-configs.sh` 显示合并后的完整配置。

---

### Step 5: 验证配置文件

检查配置文件的正确性。

#### 5.1 运行验证脚本

```bash
./scripts/validate-config.sh [配置文件路径]
```

如果未指定路径，脚本会自动查找。

#### 5.2 显示验证结果

脚本会检查：
- YAML 语法正确性
- 必需字段存在（metadata, available_skills, presets）
- presets 结构正确
- skill ID 格式有效

向用户显示验证结果，如果有错误，给出修复建议。

---

## 脚本工具

配置管理器提供以下脚本工具：

### discover-skills.sh
自动发现并更新 code review skills 到配置文件。

```bash
./scripts/discover-skills.sh [配置文件路径]
```

如果未指定配置文件路径，脚本会自动按优先级查找（项目 > 用户 > 全局）。

### init-config.sh
初始化配置文件，创建默认配置。

```bash
./scripts/init-config.sh [--global|--user|--project] [路径]
```

### validate-config.sh
验证配置文件的正确性。

```bash
./scripts/validate-config.sh [配置文件路径]
```

### merge-configs.sh
合并多层级配置文件。

```bash
./scripts/merge-configs.sh [输出路径]
```

---

## 错误处理

### 配置文件不存在
提示用户运行 `init-config.sh` 初始化配置。

### YAML 语法错误
提示用户运行 `validate-config.sh` 检查错误位置。

### Skill 不存在
如果 preset 中引用的 skill 不在 `available_skills` 中，警告用户并建议运行更新。

### 权限问题
如果无法创建配置文件，检查目录权限，提示用户手动创建目录。

---

## 配置文件格式

配置文件使用 YAML 格式：

```yaml
metadata:
  version: "0.2.0"
  last_updated: "2025-01-15"
  auto_sync: true

# Skills 搜索目录配置
# 支持相对路径（相对于配置文件所在目录）和绝对路径
skills_directories:
  - "skills"           # 默认：项目内的 skills 目录
  # - ".skills"          # 可选：隐藏的 skills 目录
  # - "../other-skills"  # 可选：其他项目的 skills 目录
  # - "~/.claude/skills" # 可选：用户级 skills 目录

# 可用的 code review skills 和 commands
# type 字段标识能力类型: skill 或 command
available_skills:
  - id: "code-review:code-review"
    name: "code-review:code-review"
    type: "command"
    category: "安全审计"
    description: "检查代码质量问题"
    tags: ["review", "security"]
    recommended_for: ["所有项目"]

  - id: "pr-review-toolkit:review-pr"
    name: "pr-review-toolkit:review-pr"
    type: "command"
    category: "测试+清理"
    description: "PR 审查工具"
    tags: ["review", "pr"]
    recommended_for: ["所有项目"]

presets:
  - name: "快速审查"
    description: "轻量级快速审查"
    skills:
      - "code-review:code-review"
```

---

## 注意事项

1. **保留用户编辑**: 更新 `available_skills` 时，始终保留用户的 `presets` 配置
2. **配置合并**: 多层级配置时，`available_skills` 取并集，`presets` 按名称覆盖
3. **YAML 格式**: 编辑配置文件时注意 YAML 缩进和格式
4. **skill ID**: skill ID 使用 `skill:name` 格式，确保与实际 skill 名称一致
