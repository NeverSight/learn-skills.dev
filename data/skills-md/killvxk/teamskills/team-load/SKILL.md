---
name: team-load
description: |
  This skill should be used when the user asks to "加载团队", "team load",
  "恢复团队", "载入团队配置". 从 .team-profiles/ 读取 YAML 配置，
  跳过交互问答直接创建团队。支持 template 和 snapshot 两种格式。
argument-hint: "[配置名称]"
disable-model-invocation: true
version: 0.1.0
---

# 团队配置加载

从项目目录的 `.team-profiles/` 加载已保存的团队配置，跳过交互问答，直接创建团队。

## 支持的配置格式

| 格式 | 来源 | 识别方式 | 加载行为 |
|------|------|----------|----------|
| template | `/team-init` 自动保存 | `format: template` 或有 `team_type` + `roles` 字段 | 读取角色定义文件构建 prompt |
| snapshot | `/team-save` 手动保存 | `format: snapshot` 或有 `members` 含 `prompt` 字段 | 直接使用保存的 prompt |

## 加载流程

### 步骤 1: 定位配置文件

配置文件路径: `{当前工作目录}/.team-profiles/{name}.yaml`

- 如果 `$ARGUMENTS` 非空，直接使用 `$ARGUMENTS` 作为配置名称
- 如果 `$ARGUMENTS` 为空，扫描 `.team-profiles/` 目录下所有 `.yaml` 文件，列出供用户选择

当目录下有多个配置时：

```
AskUserQuestion:
  question: "选择要加载的团队配置"
  header: "团队配置"
  options:
    - label: "{name1}"
      description: "[{format}] {description 前30字}"
    - label: "{name2}"
      description: "[{format}] {description 前30字}"
    # ... 最多列出 4 个，更多在「其他」中输入
  multiSelect: false
```

如果 `.team-profiles/` 目录不存在或为空，提示用户：
```
未找到团队配置。
- 使用 /team-init 创建新团队（会自动保存模板配置）
- 使用 /team-save 保存当前运行中的团队（保存快照配置）
```

### 步骤 2: 读取并识别格式

使用 Read 工具读取 `.team-profiles/{name}.yaml`。

**格式判断**：
- 有 `format: snapshot` 或有 `members[].prompt` → snapshot 格式，跳到「快照加载流程」
- 有 `format: template` 或有 `team_type` + `roles` → template 格式，跳到「模板加载流程」
- 都不匹配 → 报错提示格式不正确

### 步骤 2.5: 检测团队冲突

扫描 `~/.claude/teams/` 目录，检查是否存在与即将创建的团队同名的目录。

如果存在同名团队目录，在步骤 3 的确认摘要中增加警告：

```
⚠ 检测到同名团队「{project_name}」正在运行。
加载将创建新团队，旧团队的 agent 不会自动关闭。
建议先关闭旧团队，或使用不同的项目名称。
```

这只是警告，不阻止加载。

### 步骤 3: 确认并允许覆盖

展示配置摘要（两种格式通用）：

```
团队配置: {name} [{format}]
--------------------
描述: {description}
工作目录: {work_dir 或 cwd}

团队成员:
  - {member/role 列表}

预计创建 {N} 个 Agent

任务进度（仅 snapshot 且有 tasks 时显示）:
  {completed}✓ 已完成  {in_progress}⚡ 进行中  {pending}○ 待处理
--------------------
```

```
AskUserQuestion:
  question: "确认加载此团队配置？"
  header: "确认"
  options:
    - label: "直接加载"
      description: "使用保存的配置创建团队"
    - label: "修改项目名称"
      description: "使用相同配置但换一个 team name"
    - label: "修改工作目录"
      description: "使用相同配置但换工作目录"
    - label: "修改名称和目录"
      description: "同时修改项目名称和工作目录"
  multiSelect: false
```

如果用户选择修改项目名称或工作目录，用 AskUserQuestion 收集新值。
如果用户选择"修改名称和目录"，依次用两个 AskUserQuestion 收集新的项目名称和新的工作目录。
用户可以在「其他」中输入取消。

---

## 模板加载流程（format: template）

配置中包含 `team_type`、`roles` 等字段，需要读取角色定义文件构建 prompt。

### T-1: 解析配置

提取：
- `team_type`: 团队类型目录名 (dev/testing/reverse/debug/security/ctf/ops/discuss)
- `team_type_name`: 中文名称
- `description`: 项目描述
- `tech_stack`: 技术栈
- `work_dir`: 工作目录（"." 替换为当前工作目录）
- `roles[]`: 角色列表，每项有 `role`（代号）、`count`（数量）、`is_lead`（是否 Lead）

### T-2: 创建团队

```
TeamCreate:
  team_name: "{project_name}"
  description: "{team_type_name} - {description}"
```

### T-3: 读取角色定义和工作流

角色定义路径: `~/.claude/skills/team-init/references/{team_type}/roles/{role_code}.md`
工作流路径: `~/.claude/skills/team-init/references/{team_type}/workflow.md`

> **注意**: 以上路径以 skill 实际安装目录为准。

### T-4: 构建角色 Prompt

```
你是「{project_name}」项目的{role_name}。

<project_context>
项目名称: {project_name}
团队类型: {team_type_name}
项目描述: {description}
技术栈: {tech_stack}
工作目录: {work_dir}
</project_context>

<team_members>
{列出所有成员的名称和角色}
</team_members>

<workflow>
{workflow.md 的内容}
</workflow>

<your_role>
{对应角色 .md 文件的完整内容}
</your_role>
```

### T-5: 创建初始任务

使用 TaskCreate 根据 workflow.md 的阶段创建任务骨架。
设置阶段间的 blockedBy 依赖关系。
将第一个任务分配给 Lead 角色。

### T-6: 派生团队成员

先创建 Lead，再并行创建其他角色。

```
Agent:
  name: "{member_name}"
  subagent_type: "general-purpose"
  team_name: "{project_name}"
  prompt: "{T-4 构建的 prompt}"
  mode: "bypassPermissions"
  description: "Team member: {role_name}"
```

命名规则：
- 单实例角色: 直接使用代号
- 多实例角色: 代号-序号

### T-7: 通知 Lead 启动

```
SendMessage:
  type: "message"
  recipient: "{lead_name}"
  content: |
    团队已从模板配置加载完成。
    - 项目: {project_name}
    - 描述: {description}
    - 技术栈: {tech_stack}
    - 工作目录: {work_dir}
    - 团队成员: {member_list}
    - 配置来源: .team-profiles/{name}.yaml

    请开始第一阶段工作。
    工作流: ~/.claude/skills/team-init/references/{team_type}/workflow.md
  summary: "团队已从模板加载，启动项目"
```

---

## 快照加载流程（format: snapshot）

配置中包含每个成员的完整 `prompt`，直接使用，不需要读取角色定义文件。

### S-1: 解析配置

提取：
- `name`: 团队名称
- `description`: 团队描述
- `team_type`: 团队类型目录名（可选，用于 S-2 description 和 S-4 lead 识别）
- `team_type_name`: 团队类型中文名（可选，用于 S-2 description）
- `members[]`: 成员列表，每项有：
  - `name`: 成员名称
  - `agent_type`: agent 类型
  - `prompt`: 完整 prompt
  - `model`: 模型（可选，默认继承当前模型）
  - `mode`: 权限模式（可选，默认 "bypassPermissions"，可选 "plan" / "default"）
  - `cwd`: 工作目录
  - `color`: 颜色（可选）
- `tasks[]`: 任务列表（可选），每项有：
  - `original_id`: 原始任务 ID
  - `subject`: 任务标题
  - `description`: 详细描述
  - `active_form`: 进行时描述
  - `status`: 状态
  - `owner`: 负责人名称
  - `blocked_by`: 依赖的 original_id 列表

### S-2: 创建团队

```
TeamCreate:
  team_name: "{project_name}"
  description: "{team_type_name} - {description}"   # 如果 team_type_name 为空则只用 {description}
```

### S-3: 恢复任务进度

如果配置中有 `tasks` 段且非空，按顺序恢复任务：

1. 维护一个 ID 映射表: `old_id → new_id`
2. 按 original_id 顺序遍历每个任务：
   a. 使用 TaskCreate 创建任务（subject, description, activeForm）
   b. 记录 `old_id → new_id` 映射
3. 创建完所有任务后，设置依赖关系：
   - 遍历每个有 `blocked_by` 的任务
   - 将 blocked_by 中的 old_id 通过映射表转换为 new_id
   - 使用 TaskUpdate 设置 addBlockedBy
4. 恢复任务状态：
   - 对 status 为 `completed` 的任务：TaskUpdate status → completed
   - 对 status 为 `in_progress` 的任务：TaskUpdate status → pending，设置 owner（重置为待处理，保留负责人，让 lead 重新评估）
   - 对有 owner 的 `pending` 任务：TaskUpdate 设置 owner

### S-4: 派生团队成员

**确定优先创建的成员（Lead 识别）**：

如果配置中有 `team_type`，根据以下映射找到 lead 角色代号：
- dev → pm
- testing → test-manager
- reverse → re-lead
- debug → debug-lead
- security → security-lead
- ctf → captain
- ops → ops-manager
- discuss → moderator

在 members 列表中查找 name 匹配 lead 代号的成员，优先创建它。
如果 `team_type` 为空或找不到匹配的 lead 成员，则全部并行创建。

对每个成员：

```
Agent:
  name: "{member.name}"
  subagent_type: "general-purpose"
  team_name: "{project_name}"
  prompt: "{member.prompt}"
  mode: "{member.mode 或默认 bypassPermissions}"
  description: "Team member: {member.name}"
```

**注意**：`color` 字段仅作记录保留，Task tool 不支持设置颜色，加载时不生效。

**Prompt 替换规则**：
- 如果用户修改了工作目录，将每个成员 prompt 中该成员自己的 `member.cwd` 值替换为新路径（注意：不同成员可能有不同的 cwd，按各自的值替换）
- 如果用户修改了项目名称，将每个成员 prompt 中的配置原始 `name` 替换为新 `project_name`（包括 `<project_context>` 块中的 `项目名称:` 和 prompt 开头的 `「{old_name}」`）

### S-5: 通知 Lead 成员启动

通知 S-4 中识别出的 lead 成员。如果未识别出 lead（全部并行创建），则通知 members 列表中的第一个成员。

```
SendMessage:
  type: "message"
  recipient: "{lead_member_name 或 first_member_name}"
  content: |
    团队已从快照配置加载完成。
    - 项目: {project_name}
    - 描述: {description}
    - 工作目录: {work_dir}
    - 团队成员: {member_list}
    - 任务恢复: {M} 个任务（{completed} 已完成, {was_in_progress} 个原进行中已重置为待处理, {pending} 待处理）
    - 配置来源: .team-profiles/{name}.yaml (snapshot)

    {如果 was_in_progress > 0: "注意：原来进行中的任务已重置为待处理状态，因为新 agent 没有之前的工作上下文，请重新评估这些任务。"}

    请查看 TaskList 了解当前进度，从未完成的任务继续工作。
  summary: "团队已从快照加载，启动项目"
```
