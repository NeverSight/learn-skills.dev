---
name: team-save
description: |
  This skill should be used when the user asks to "保存团队", "team save",
  "保存团队配置", "导出团队". 从运行中的团队读取配置并保存为快照文件
  到 .team-profiles/ 目录，供 /team-load 复用。
argument-hint: "[团队名称] [保存名称]"
disable-model-invocation: true
version: 0.1.0
---

# 团队配置保存

将当前运行中的团队配置保存为快照，写入项目目录的 `.team-profiles/`，供 `/team-load` 复用。

## 与 team-init 自动保存的区别

| | team-init 自动保存 | team-save 快照 |
|---|---|---|
| 格式 | 模板格式（team_type + role 代号） | 快照格式（完整 prompt） |
| 内容 | 初始配置，引用角色定义文件 | 当前实际状态，自包含 |
| 用途 | 从角色模板重建团队 | 精确还原修改过的团队 |
| 标识 | `format: template` | `format: snapshot` |

## 保存流程

### 步骤 1: 确定要保存的团队

如果 `$ARGUMENTS` 的第一个参数非空，使用它作为团队名称。
否则，扫描 `~/.claude/teams/` 目录，列出现有团队供用户选择。

**如果目录不存在或为空**，输出友好提示后结束：

```
当前没有运行中的团队。
- 使用 /team-init 创建新团队
```

**如果有团队**，列出供用户选择：

```
AskUserQuestion:
  question: "选择要保存的团队"
  header: "选择团队"
  options:
    - label: "{team_name_1}"
      description: "{description_1}"
    - label: "{team_name_2}"
      description: "{description_2}"
    # ... 最多 4 个
  multiSelect: false
```

### 步骤 2: 读取团队配置

读取 `~/.claude/teams/{team_name}/config.json`，提取：
- `name`: 团队名称
- `description`: 团队描述
- `members[]`: 成员列表，每个成员提取：
  - `name`: 成员名称
  - `agentType`: agent 类型
  - `prompt`: 完整 prompt（如果有）
  - `model`: 模型
  - `planModeRequired`: 如果为 true 则 mode 为 "plan"，否则为 "bypassPermissions"
  - `cwd`: 工作目录
  - `color`: 颜色标识

**提取 team_type**：

尝试从以下来源推断团队类型（按优先级）：
1. 检查项目目录 `.team-profiles/` 下是否有同名的 template 格式配置文件，如果有则读取其 `team_type`
2. 从成员 prompt 中的 `<project_context>` 块提取 `团队类型:` 字段
3. 从 description 中匹配关键词（"软件开发"→dev, "测试"→testing, "逆向"→reverse, "调试"→debug, "安全"→security, "CTF"→ctf, "运维"→ops, "讨论"→discuss）
4. 以上都无法确定则设为空字符串

**过滤规则**：
- 跳过 `agentType: "team-lead"` 的成员（team-lead 由系统自动创建，不需要保存 prompt）
- 只保存有 `prompt` 字段的成员

### 步骤 2.5: 采集任务进度

使用 TaskList 工具获取当前团队的所有任务。对每个任务使用 TaskGet 获取完整信息。

提取每个任务的：
- `id`: 任务 ID（仅用于记录依赖关系，加载时会重新分配）
- `subject`: 任务标题
- `description`: 详细描述
- `activeForm`: 进行时描述
- `status`: 状态（pending / in_progress / completed）
- `owner`: 负责人名称（对应成员的 name）
- `blockedBy`: 依赖的任务 ID 列表

**注意**：如果 TaskList 返回为空（没有任务），则 `tasks` 段为空数组，这是正常的。

### 步骤 3: 确定保存名称

如果 `$ARGUMENTS` 的第二个参数非空，使用它作为保存名称。
否则默认使用团队名称。

```
AskUserQuestion:
  question: "保存配置的名称？（将保存到 .team-profiles/{name}.yaml）"
  header: "保存名称"
  options:
    - label: "{team_name}"
      description: "使用团队名称"
    - label: "自定义名称"
      description: "在「其他」中输入"
  multiSelect: false
```

### 步骤 4: 展示摘要并确认

```
团队快照摘要
--------------------
团队名称: {team_name}
团队类型: {team_type_name}（如果有）
团队描述: {description}
工作目录: {cwd}

成员列表 ({N} 个):
  - {member_name} ({agentType}) [{model}]
  - ...

任务进度 ({M} 个):
  - [completed] #{id} {subject} → {owner}
  - [in_progress] #{id} {subject} → {owner}
  - [pending] #{id} {subject} → {owner 或 "未分配"}
  ...

保存到: .team-profiles/{save_name}.yaml
--------------------
```

```
AskUserQuestion:
  question: "确认保存？"
  header: "确认"
  options:
    - label: "保存"
      description: "保存团队快照"
    - label: "取消"
      description: "放弃保存"
  multiSelect: false
```

### 步骤 5: 写入配置文件

**确保目录存在**：

使用 Bash 工具执行：
```bash
mkdir -p "{当前工作目录}/.team-profiles"
```

**覆盖保护**：如果 `.team-profiles/{save_name}.yaml` 已存在：
1. 读取旧文件，提取成员数和任务数
2. 在确认步骤中显示差异摘要：
   ```
   ⚠ 文件已存在，将覆盖:
     旧配置: {old_member_count} 个成员, {old_task_count} 个任务
     新配置: {new_member_count} 个成员, {new_task_count} 个任务
   旧文件将备份为: .team-profiles/{save_name}.yaml.bak
   ```
3. 写入前将旧文件重命名为 `.team-profiles/{save_name}.yaml.bak`（使用 Bash: `mv` 命令）
4. 如果 `.bak` 文件也已存在，直接覆盖 `.bak`

使用 Write 工具创建 `.team-profiles/{save_name}.yaml`：

```yaml
# 团队快照 - 由 /team-save 保存
# 使用 /team-load {save_name} 可直接加载此配置创建团队
# 保存时间: {ISO 8601 时间戳}

format: snapshot
name: "{team_name}"
description: "{description}"
team_type: "{team_type}"           # 如果能从成员 prompt 中提取到则填写，否则为空字符串
team_type_name: "{team_type_name}" # 同上

members:
  - name: "{member_name}"
    agent_type: "{agentType}"
    model: "{model}"
    mode: "{mode}"              # bypassPermissions / plan / default，默认 bypassPermissions
    cwd: "{cwd}"
    color: "{color}"
    prompt: |
      {完整的 prompt 内容，使用 YAML 多行字符串}

  - name: "{member_name_2}"
    agent_type: "{agentType}"
    model: "{model}"
    mode: "{mode}"
    cwd: "{cwd}"
    color: "{color}"
    prompt: |
      {完整的 prompt 内容}

  # ... 所有非 team-lead 成员

tasks:
  - original_id: "{原始任务 ID，仅用于依赖关系映射}"
    subject: "{任务标题}"
    description: |
      {任务详细描述}
    active_form: "{进行时描述}"
    status: "{pending / in_progress / completed}"
    owner: "{负责人名称，对应 members 中的 name，空字符串表示未分配}"
    blocked_by: ["{依赖的 original_id}", ...]  # 空数组表示无依赖

  - original_id: "2"
    subject: "..."
    description: |
      ...
    active_form: "..."
    status: "pending"
    owner: ""
    blocked_by: ["1"]

  # ... 所有任务（包括已完成的，用于记录完整历史）
```

### 步骤 6: 输出结果

```
团队快照已保存到: .team-profiles/{save_name}.yaml
包含 {N} 个成员配置（不含 team-lead）、{M} 个任务记录。

使用 /team-load {save_name} 可直接加载此团队。
```

## 注意事项

- prompt 可能很长（几百行），使用 YAML `|` 多行字符串格式保存
- **大文件写入策略**：snapshot 文件可能超过 150 行（Write 工具单次上限）。应先用 Write 写入文件头部和前几个成员（约 100-120 行），再用 Edit 工具追加剩余成员和 tasks 段
- 如果目标文件已存在，自动备份为 `.bak` 后再覆盖，并在确认步骤中显示差异摘要
- team-lead 不保存 prompt，因为加载时由系统自动创建
- cwd 路径保存绝对路径，加载时可由用户覆盖
- **color 字段**：仅作记录保留，Task tool 不支持设置颜色，加载时不生效
- 任务的 original_id 仅用于保存时记录依赖关系，加载时会重新分配新 ID 并映射依赖
- 已完成的任务也会保存，加载时直接标记为 completed，让团队知道哪些工作已经做过
- mode 检测局限：config.json 中只有 `planModeRequired` 布尔值，`false` 统一映射为 "bypassPermissions"，无法区分原始创建时使用的是 "default" 还是 "bypassPermissions"。如需精确保留 "default" 模式，需在加载后手动编辑 snapshot 文件
