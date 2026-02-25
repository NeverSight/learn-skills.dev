---
name: code-review:executor
description: This skill should be used when the user asks to "review code", "do a code review", "review my branch", "review MR !1234", "review PR #567", "review feature/auth branch", "review feature/auth vs dev", "check code quality", or wants to execute code review using configured skill presets. Reads review skills configuration and orchestrates parallel code reviews.
---

# Code Review Executor

执行代码审查，读取配置文件中的 skill/command 预设，协调多个 subagents 并行执行审查，生成综合报告。

## Purpose

管理完整的代码审查执行流程：
- 加载并验证配置文件
- 让用户选择审查预设
- 收集代码内容（diffs, commits, branches）
- 协调多个 subagents 并行执行（支持 skills 和 commands）
- 汇总审查结果生成综合报告

## 能力类型

Executor 支持调用两种类型的 review 能力：

- **skill**: SKILL.md 格式的技能，通过 Task 工具的 subagent_type 调用
- **command**: 插件中的命令，通过 Skill 工具调用

配置文件中的 `type` 字段标识能力类型，Executor 需要根据类型选择正确的调用方式。

## When to Use

当用户请求代码审查时触发：
- "Review my code"
- "Review feature/auth branch"
- "Review MR !1234" / "Review PR #567"
- "Review feature/auth vs dev branch"
- "Do a code review"

## Workflow

### Step 0: Debug Mode Detection (Optional)

**配置**: Debug mode 可通过用户输入或交互式确认控制。

**启用 Debug Mode 的方式**:
1. **自动检测**: 用户输入中包含关键词（`debug`, `verbose`, `调试`, `详细`, `--debug`, `-v`）
2. **交互式**: 提示时选择 "启用调试" 启用详细日志

**Debug Mode 记录内容**:
- 所有检查点和决策点
- 用户选择和确认
- Subagent 启动和完成状态
- 时间戳和进度跟踪
- 完整的交互历史

**输出**: 保存到工作目录的 `DEBUG-SESSION.md`

---

### Step 1: 加载并验证配置

从配置文件加载 review skills 配置。

#### 1.1 查找配置文件

按优先级查找配置文件（项目 > 用户 > 全局）：

```bash
# 项目配置
.claude/code-review-skills/config.yaml

# 用户配置
~/.claude/code-review-skills/config.yaml

# 全局配置
~/.config/claude/code-review-skills/config.yaml
```

#### 1.2 检查配置是否存在

**如果配置文件不存在**:
- 提示用户配置文件缺失
- 建议运行 `code-review:config-manager` 初始化配置
- 提供快速初始化选项

**示例提示**:
```
未找到 Code Review 配置文件。

需要先配置 review skills。请：
1. 运行 "code-review:config-manager" 初始化配置
2. 或选择下方快速初始化

[快速初始化] [手动配置] [取消]
```

#### 1.3 合并多层级配置

如果存在多层级配置，运行 `scripts/merge-configs.sh` 合并：

```bash
../config-manager/scripts/merge-configs.sh
```

合并规则：
- `available_skills`: 取并集，去重
- `presets`: 按名称覆盖（项目 > 用户 > 全局）
- `metadata`: 取最高优先级

#### 1.4 验证配置

运行 `scripts/validate-config.sh` 验证配置文件：

```bash
../config-manager/scripts/validate-config.sh [配置文件路径]
```

检查：
- YAML 语法正确性
- 必需字段存在
- Preset 结构有效
- Skill ID 格式正确

**如果验证失败**:
- 显示验证错误
- 建议修复方法
- 提供运行 `code-review:config-manager` 修复配置的选项

---

### Step 2: 确定审查范围

识别要审查的代码范围。

**审查类型**:
- **分支**: 单个分支（如 `feature/auth`）- 审查分支中的所有变更
- **分支对比**: 分支 A vs 分支 B（如 `feature/auth` vs `dev`）- **重要**: 找到 merge base，从 merge base 到分支 A 的 HEAD 进行 diff
- **MR/PR**: 通过编号或 URL 指定 Merge Request (GitLab) 或 Pull Request (GitHub)
- **项目**: Monorepo 包含多个子项目 - 询问要审查哪些
- **全项目**: 多个独立项目或整个代码库 - 收集所有项目路径

**所需信息**:
- 分支名称（如果对比分支）
- MR/PR 编号或 URL
- 项目路径（对于 monorepo 或全项目审查）
- 仓库 URL（如果不是当前目录）

**全项目审查时**:
当用户要求 "review entire project" 或 "review all code" 时：
1. 询问用户要审查哪些项目/目录
2. 检查每个项目是否是 git 仓库
3. 收集项目元数据（技术栈、代码行数、文件数量）
4. 继续前确认

---

### Step 3: 建立工作目录

**重要**: 工作目录名称必须包含日期和序列号以避免冲突。

**目录命名规范**: `{review_name}-{YYYYMMDD}-{sequence}`

**生成唯一工作目录**:
```bash
# 获取当前日期
DATE=$(date +%Y%m%d)

# 基础目录名
BASE_DIR="{review_name}-${DATE}"

# 查找同名的现有目录
EXISTING=$(ls -d reviews/${BASE_DIR}-* 2>/dev/null | wc -l)

# 计算下一个序列号
SEQUENCE=$((EXISTING + 1))

# 最终目录名
WORKING_DIR="${BASE_DIR}-${SEQUENCE}"
```

**示例**:
```
2026-01-30 第一次审查:    mr557-aihub-refactor-20260130-1
同日第二次审查:           mr557-aihub-refactor-20260130-2
次日第一次审查:           mr557-aihub-refactor-20260131-1
```

**完整路径**: `{project_root}/reviews/{review_name}-{YYYYMMDD}-{sequence}`

**目录结构**:
```
reviews/{review_name}-{YYYYMMDD}-{sequence}/
├── code-context.json                     # 审查元数据
├── diff.patch                             # Git diff 输出
├── commits.json                           # 提交历史
├── branch-info.json                       # 分支详情
├── DEBUG-SESSION.md                       # Debug 会话日志（始终大写）
├── {review_name}-{YYYYMMDD}-{sequence}-comprehensive-summary.md # 最终报告
└── reports/                               # 单个 skill 报告
    ├── skill1-report.md
    ├── skill2-report.md
    └── ...
```

**重要文件命名规范**:
1. **工作目录**: `{review_name}-{YYYYMMDD}-{sequence}`（日期 + 序列号保证唯一性）
2. **总结文件**: `{review_name}-{YYYYMMDD}-{sequence}-comprehensive-summary.md`（包含日期+序列号）
3. **Debug 会话文件**: `DEBUG-SESSION.md`（始终大写，固定名称）
4. **独立报告**: `{skill-name}-report.md`（使用 skill 的短名称）
5. **上下文文件**: 小写加连字符（code-context.json, diff.patch 等）

---

### Step 4: 选择审查预设

从配置文件中加载预设配置，让用户选择。

#### 4.1 读取预设配置

使用 Read 工具读取配置文件中的 `presets` 部分。

#### 4.2 显示可用预设

向用户展示所有可用的预设配置：

```
可用预设配置：

1. 快速审查 (2 个 skills)
   描述: 轻量级快速审查，适用于日常开发
   包含: code-review:code-review, codebase-cleanup:code-reviewer

2. 全面审查 (5 个 skills)
   描述: 包含所有维度的深度审查
   包含: code-review:code-review, security-scanning:security-auditor,
         application-performance:performance-engineer, ...

3. 安全优先 (3 个 skills)
   描述: 重点关注安全问题的审查
   包含: security-scanning:security-auditor, ...

4. 性能优化 (3 个 skills)
   描述: 关注性能和架构的审查
   包含: application-performance:performance-engineer, ...
```

#### 4.3 用户选择预设

**如果只有一个预设**: 跳过选择，直接使用该预设。

**如果有多个预设**: 使用 AskUserQuestion 让用户选择：

```python
AskUserQuestion(
    questions=[
        {
            "question": "请选择审查预设配置",
            "header": "选择预设",
            "options": [
                {
                    "label": "快速审查",
                    "description": "2 个 skills - 轻量级快速审查"
                },
                {
                    "label": "全面审查",
                    "description": "5 个 skills - 包含所有维度"
                },
                # ... 更多预设
            ],
            "multiSelect": False
        }
    ]
)
```

**用户指定预设名称时**: 如果用户明确指定了预设名称（如 "使用快速审查"），跳过选择步骤。

#### 4.4 加载选中的预设

从配置文件中提取选中预设的 `skills` 列表。

---

### Step 5: 收集代码内容

收集完整的审查信息并保存到工作目录。

**使用 `scripts/collect-review-data.sh`** 自动化数据收集。

**保存为 `code-context.json`:**
```json
{
  "review_type": "branch_comparison|branch|mr|pr",
  "source_branch": "feature/auth",
  "target_branch": "dev",
  "merge_base": "abc123",
  "mr_number": "!1234",
  "pr_number": "567",
  "repository": "git@gitlab.com:group/project.git",
  "project_path": "/path/to/project",
  "working_directory": "/path/to/reviews/auth-feature-20260130-1",
  "review_date": "2026-01-30",
  "review_sequence": 1,
  "timestamp": "2026-01-30T14:30:22Z"
}
```

**保存为 `diff.patch`:**
- 使用 `git diff merge_base...source_branch` 进行分支对比
- 使用 `git diff dev...feature/auth` 格式（三个点）找到正确的 merge base
- 包含完整上下文用于审查

**保存为 `commits.json`:**
```json
{
  "commits": [
    {
      "hash": "def456",
      "author": "John Doe",
      "date": "2025-01-28T09:00:00Z",
      "message": "Add login form",
      "files_changed": ["src/auth/login.js"]
    }
  ]
}
```

**保存为 `branch-info.json`:**
```json
{
  "source_branch": {
    "name": "feature/auth",
    "head_commit": "def456",
    "is_merged": false
  },
  "target_branch": {
    "name": "dev",
    "head_commit": "abc123"
  }
}
```

**分支对比的关键点**:
对比分支 A vs 分支 B 时：
1. 找到 merge base: `git merge-base A B`
2. 从 merge base 到 A 进行 diff: `git diff merge_base...A`
3. 确保只审查 A 中的独特变更

**向用户确认**:
收集完代码上下文后，使用 AskUserQuestion 工具呈现给用户：

**示例 AskUserQuestion 调用**:
```python
AskUserQuestion(
    questions=[
        {
            "question": "代码审查信息已收集，是否继续？",
            "header": "确认审查",
            "options": [
                {
                    "label": "继续审查",
                    "description": "开始执行代码审查，启动并行子代理"
                },
                {
                    "label": "取消",
                    "description": "取消本次审查，退出技能"
                }
            ],
            "multiSelect": False
        }
    ]
)
```

**问题描述中呈现的信息**:
```
审查类型: 分支对比
源分支: feature/auth
目标分支: dev

变更统计:
- 15 个文件修改
- +350 行, -120 行

工作目录: /path/to/reviews/auth-feature-20260130-1
```

**等待用户确认后继续，不要在没有用户确认的情况下继续到 Step 6。**

---

### Step 6: 并行执行审查

启动多个 subagents 并行执行审查，根据能力类型选择调用方式。

#### 6.1 准备 Subagent 任务

对于选中的预设中的每个能力：
- 从 `available_skills` 获取能力的详细信息
- 检查 `type` 字段确定能力类型（skill 或 command）
- 准备能力专用的 prompt
- 设置输出文件路径

#### 6.2 根据能力类型选择调用方式

**对于 skill 类型**:
使用 Task 工具启动 subagent，设置 `run_in_background=true`

**对于 command 类型**:
使用 Task 工具包装 Skill 调用，实现并行执行

**推荐方式 - 统一使用 Task 包装**:
无论 skill 还是 command 类型，都使用 Task 工具启动 subagent，在 prompt 中指明如何调用。

#### 6.3 启动并行 Subagents

使用 Task 工具启动 subagents，设置 `run_in_background=true`：

**重要**: 在单个消息中启动所有 subagents 以实现真正的并行执行。

**示例 Task 调用**:
```xml
<!-- 第一个 subagent - skill 类型 -->
<Task subagent_type="general-purpose"
      prompt="使用 code-review:code-review skill 审查以下代码..."
      run_in_background="true"
      description="Review code with code-review skill">

<!-- 第二个 subagent - command 类型（使用 Skill 工具调用） -->
<Task subagent_type="general-purpose"
      prompt="使用 Skill 工具调用 pr-review-toolkit:review-pr 命令执行 PR 审查..."
      run_in_background="true"
      description="Review with review-pr command">

<!-- 第三个 subagent -->
<Task subagent_type="general-purpose"
      prompt="使用 security-scanning:security-auditor skill 审查以下代码..."
      run_in_background="true"
      description="Review code with security-auditor skill">
```

**Subagent Prompt 结构**:
```
使用 {ability_id} {type} 审查以下代码变更。

能力类型: {type} (skill/command)
上下文信息:
- 工作目录: {working_directory}
- 审查类型: {review_type}
- Diff 文件: diff.patch
- 提交信息: commits.json
- 分支信息: branch-info.json

请:
1. 使用 {ability_id} 执行审查（如果是 command 类型，使用 Skill 工具调用）
2. 将报告保存到 {working_directory}/reports/{ability-name}-report.md
3. 使用参考文档中定义的报告格式
4. 标注问题发现位置和严重程度
```

#### 6.3 等待 Subagents 完成

收集所有 subagent 的 task ID，使用 TaskOutput 工具等待完成：

```python
task_ids = ["task_id_1", "task_id_2", "task_id_3"]

for task_id in task_ids:
    TaskOutput(task_id=task_id, block=True, timeout=300000)
```

**超时设置**:
- 小型变更 (<500 行): 1 分钟
- 中型变更 (500-2000 行): 3 分钟
- 大型变更 (2000-10000 行): 5 分钟
- 超大型变更 (>10000 行): 10 分钟

#### 6.4 处理失败的任务

如果某个 subagent 失败：
- 记录失败信息到 DEBUG-SESSION.md
- 继续等待其他 subagents
- 在最终报告中标注该 skill 审查失败

---

### Step 7: 汇总审查结果

收集所有 subagent 的报告，生成综合总结。

#### 7.1 读取所有报告

从 `reports/` 目录读取所有生成的报告：
```bash
ls reports/*-report.md
```

#### 7.2 解析报告内容

从每个报告中提取：
- 问题列表（位置、描述、严重程度）
- 发现该问题的 skill(s)

#### 7.3 去重问题

按以下条件对问题进行去重：
- 相同文件路径
- 相同行号或范围
- 相同的问题类型

**去重逻辑**:
```python
issues = []
for report in reports:
    for issue in report.issues:
        key = (issue.file_path, issue.line_range, issue.type)
        if key not in seen_issues:
            seen_issues.add(key)
            issues.append(issue)
```

#### 7.4 按严重程度分类

将问题分为以下等级：
- **Critical**: 必须修复的安全问题或严重 bug
- **High**: 应该修复的重要问题
- **Medium**: 建议修复的一般问题
- **Low**: 可选改进的问题
- **Info**: 信息性建议

#### 7.5 生成综合报告

生成 `{review_name}-{YYYYMMDD}-{sequence}-comprehensive-summary.md`

**报告格式**:
```markdown
# 代码审查综合报告

## 审查信息

- **审查日期**: 2026-01-30
- **审查类型**: 分支对比
- **源分支**: feature/auth
- **目标分支**: dev
- **使用的预设**: 全面审查
- **审查的 skills**: 5 个

## 变更统计

- 文件修改: 15 个
- 新增代码: +350 行
- 删除代码: -120 行

## 问题汇总

### Critical (0 个)

无

### High (3 个)

#### 1. SQL 注入风险在 auth/login.js:45
- **位置**: `src/auth/login.js:45`
- **严重程度**: High
- **描述**: 用户输入未经验证直接拼接到 SQL 查询中
- **建议**: 使用参数化查询
- **发现者**: security-scanning:security-auditor, code-review:code-review

#### 2. ...

### Medium (5 个)

...

### Low (2 个)

...

### Info (3 个)

...

## 详细报告

各 skill 的详细报告：
- [code-review-report.md](reports/code-review-report.md)
- [security-auditor-report.md](reports/security-auditor-report.md)
- ...
```

---

## Debug 输出

当 Debug Mode 启用时，在每个步骤记录详细日志：

```
🔍 DEBUG [Step 1/7]: 加载并验证配置
🔍 DEBUG [Step 2/7]: 确定审查范围 - 分支对比
🔍 DEBUG [Step 3/7]: 建立工作目录 - mr557-20260130-1
🔍 DEBUG [Checkpoint 1]: 收集代码内容完成，等待用户确认
🔍 DEBUG [Step 4/7]: 选择审查预设 - 全面审查 (5 个 skills)
🔍 DEBUG [Step 5/7]: 收集代码内容
🔍 DEBUG [Step 6/7]: 启动 5 个并行 subagents
🔍 DEBUG [Checkpoint 2]: 所有 subagents 完成
🔍 DEBUG [Step 7/7]: 汇总审查结果
```

---

## 错误处理

### 配置文件缺失
- 提示用户运行 `code-review:config-manager` 初始化配置
- 提供快速初始化选项

### 配置验证失败
- 显示验证错误详情
- 建议修复方法
- 提供运行 `code-review:config-manager` 修复配置的选项

### Preset 不存在
- 列出可用的预设
- 让用户重新选择

### Skill/Command 不可用
- 警告用户该能力在当前环境中不可用
- 询问是否跳过该能力或取消审查

### Subagent 执行失败
- 记录失败详情
- 继续执行其他 subagents
- 在最终报告中标注失败的能力

---

## 配置文件依赖

Executor 依赖以下配置文件结构：

```yaml
metadata:
  version: "0.2.0"
  last_updated: "2025-01-15"
  auto_sync: true

# 能力类型说明:
# - skill: SKILL.md 格式的技能
# - command: 插件中的命令
available_skills:
  - id: "code-review:code-review"
    name: "code-review:code-review"
    type: "command"
    category: "安全审计"
    description: "..."
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
    description: "..."
    skills:
      - "code-review:code-review"
      - "pr-review-toolkit:review-pr"
```

---

## 注意事项

1. **配置优先级**: 始终先检查项目级配置，然后用户级，最后全局级
2. **能力类型**: 根据配置中的 `type` 字段选择正确的调用方式（skill 用 Task，command 用 Skill 工具）
3. **并行执行**: 所有 subagents 必须在单个消息中启动以实现真正的并行
4. **用户确认**: 在启动 subagents 前必须获得用户确认
5. **文件命名**: 工作目录和报告文件必须包含日期和序列号
6. **错误恢复**: 如果某个 subagent 失败，继续执行其他 subagents 并在报告中标注
