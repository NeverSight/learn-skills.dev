---
name: team-init
description: |
  This skill should be used when the user asks to "初始化团队", "创建开发团队",
  "team init", "create team", "build team", "组建团队", "启动项目团队",
  "添加扩展角色", "add extension roles". 通过交互式问答收集项目信息，
  创建包含专业角色的 Agent 工程团队。支持 8 种团队类型和 146 个扩展专业角色（跨 12 领域）。
argument-hint: "[项目名称]"
disable-model-invocation: true
version: 0.1.0
---

# 工程团队初始化

通过交互式问答，收集项目信息并创建由 Lead 领导的 Agent 工程团队。

## 路径约定

本 skill 中 `references/` 和 `scripts/` 路径均相对于 SKILL.md 所在目录（skill base directory）。执行时以 base directory 拼接绝对路径。**不要硬编码 `~/.claude/skills/`** — skill 可能安装在项目级 `.claude/skills/` 或全局 `~/.claude/skills/` 下。

## 支持的团队类型

| # | 类型 | 领导角色 | 目录 | 适用场景 |
|---|------|---------|------|---------|
| 1 | 软件开发 | PM | dev | 全新项目开发、功能迭代 |
| 2 | 软件测试 | 测试经理 | testing | 系统测试、质量保障 |
| 3 | 逆向工程 | 逆向负责人 | reverse | 二进制分析、协议逆向、恶意软件分析 |
| 4 | 调试/Bug修复 | 调试负责人 | debug | 故障排查、性能问题定位 |
| 5 | 安全研究 | 安全负责人 | security | 漏洞挖掘、安全评估(需合法授权) |
| 6 | CTF 比赛 | 队长 | ctf | CTF 竞赛、安全挑战 |
| 7 | 运维 | 运维经理 | ops | 部署运维、基础设施管理 |
| 8 | 讨论/研讨 | 主持人 | discuss | 方案设计、技术选型、需求研讨、头脑风暴 |

各类型的详细角色列表见 `references/role-catalog.md`。

## 交互式问答流程

按顺序使用 AskUserQuestion 工具向用户提问。

### 问题 0: 团队类型

```
AskUserQuestion:
  question: "请选择要创建的团队类型"
  header: "团队类型"
  options:
    - label: "软件开发"
      description: "全新项目开发、功能迭代"
    - label: "软件测试"
      description: "系统测试、质量保障"
    - label: "逆向工程"
      description: "二进制分析、协议逆向"
    - label: "调试/Bug修复"
      description: "故障排查、性能定位"
    - label: "安全研究"
      description: "漏洞挖掘、安全评估(需合法授权)"
    - label: "CTF 比赛"
      description: "CTF 竞赛、安全挑战"
    - label: "运维"
      description: "部署运维、基础设施管理"
    - label: "讨论/研讨"
      description: "方案设计、技术选型、需求研讨、头脑风暴"
  multiSelect: false
```

记录用户选择的 `team_type`，映射到对应目录名：
- 软件开发 → dev
- 软件测试 → testing
- 逆向工程 → reverse
- 调试/Bug修复 → debug
- 安全研究 → security
- CTF 比赛 → ctf
- 运维 → ops
- 讨论/研讨 → discuss

### 问题 1: 项目名称

如果 `$ARGUMENTS` 非空，使用其作为项目名称，跳过此问题。

```
AskUserQuestion:
  question: "请输入项目名称（英文，用作 team name，如 my-webapp）"
  header: "项目名称"
  options:
    - label: "my-project"
      description: "使用默认名称"
    - label: "输入自定义名称"
      description: "在「其他」中输入"
  multiSelect: false
```

### 问题 2: 项目描述

```
AskUserQuestion:
  question: "{根据 team_type 调整措辞}"
  header: "项目描述"
  options: {根据 team_type 提供 2-4 个典型场景选项}
  multiSelect: false
```

措辞映射：
- dev: "请简要描述项目目标和范围"
- testing: "请描述被测系统和测试目标"
- reverse: "请描述逆向目标和分析目的"
- debug: "请描述需要调试的问题和症状"
- security: "请描述安全研究的目标和范围"
- ctf: "请描述比赛名称和赛制"
- ops: "请描述运维目标和基础设施概况"
- discuss: "请描述讨论议题和期望产出"

### 问题 3: 技术栈/目标平台

```
AskUserQuestion:
  question: "{根据 team_type 调整措辞}"
  header: "技术栈"
  options: {根据 team_type 提供 2-4 个典型选项}
  multiSelect: true
```

措辞映射：
- dev: "项目使用什么技术栈？"
- testing: "被测系统的技术栈？"
- reverse: "目标平台和架构？（x86/ARM/MIPS, Windows/Linux/Android）"
- debug: "问题所在的技术栈和环境？"
- security: "研究目标的技术栈和平台？"
- ctf: "比赛偏好方向和工具？"
- ops: "基础设施技术栈？（Linux/K8s/AWS/Docker）"
- discuss: "讨论涉及哪些领域？（用于配置专家角色的专业背景）"

### 问题 4: 角色选择

展示当前 team_type 的角色列表。Lead 角色自动包含，无需选择。

```
AskUserQuestion:
  question: "选择需要的角色（{lead_role} 默认包含）。多实例角色可在「其他」中用 'developer x2' 格式指定数量"
  header: "团队角色"
  options:
    - label: "全部角色 (推荐)"
      description: "包含该类型所有角色各 1 个"
    - label: "核心团队"
      description: "{该类型的核心角色子集}"
    - label: "最小团队"
      description: "{lead + 1-2 个核心角色}"
    - label: "自定义"
      description: "在「其他」中指定角色和数量"
  multiSelect: false
```

核心团队映射：
- dev: pm + architect + developer + tester
- testing: test-manager + test-architect + functional-tester + automation-tester
- reverse: re-lead + static-analyst + dynamic-analyst
- debug: debug-lead + root-cause-analyst + fix-engineer
- security: security-lead + vuln-hunter + security-auditor
- ctf: captain + web + pwn + reverse
- ops: ops-manager + sys-engineer + monitor-engineer
- discuss: moderator + domain-expert + critic + synthesizer

最小团队映射：
- dev: pm + developer
- testing: test-manager + functional-tester
- reverse: re-lead + static-analyst
- debug: debug-lead + fix-engineer
- security: security-lead + vuln-hunter
- ctf: captain + web
- ops: ops-manager + sys-engineer
- discuss: moderator + domain-expert

### 问题 4.2: 扩展角色（可选）

```
AskUserQuestion:
  question: "是否从扩展角色库添加专业角色？（146 个跨 12 领域的专家角色）"
  header: "扩展角色"
  options:
    - label: "跳过"
      description: "仅使用核心团队角色"
    - label: "浏览并选择"
      description: "从扩展角色库中挑选专业角色"
  multiSelect: false
```

若选择「跳过」→ 若 team_type 为 discuss 则进入问题 4.5（讨论轮次）；否则进入问题 5（确认）。
若选择「浏览并选择」→ 进入问题 4.3。

### 问题 4.3: 选择扩展领域

读取 `references/extensions/extension-catalog.md` 获取完整领域列表。

```
AskUserQuestion:
  question: "选择要浏览的领域（可多选）"
  header: "扩展角色领域"
  options:
    - label: "engineering"
      description: "22个: 前端、后端、AI、DevOps、安全、嵌入式..."
    - label: "design"
      description: "8个: UI、UX、品牌、视觉叙事..."
    - label: "marketing"
      description: "29个: 小红书、抖音、微信、B站、SEO..."
    - label: "game-development"
      description: "19个: Unity、Unreal、Godot、Roblox..."
    - label: "paid-media"
      description: "7个: PPC、社交广告、程序化采买..."
    - label: "product"
      description: "4个: Sprint排序、趋势研究、反馈分析..."
    - label: "project-management"
      description: "6个: 制片人、项目协调、实验追踪..."
    - label: "sales"
      description: "8个: 赢单策略、售前工程、Pipeline分析..."
    - label: "support"
      description: "8个: 数据分析、法务合规、财务、招聘..."
    - label: "spatial-computing"
      description: "6个: visionOS、WebXR、Metal..."
    - label: "specialized"
      description: "21个: 编排、区块链安全、MCP、合规..."
    - label: "testing"
      description: "8个: 证据收集、无障碍、API测试..."
  multiSelect: true
```

### 问题 4.4: 选择具体角色

对用户选中的每个领域，从 `references/extensions/extension-catalog.md` 读取该领域的角色列表，展示给用户选择：

```
AskUserQuestion:
  question: "选择要添加的 {department} 角色"
  header: "{department} 扩展角色"
  options:
    {从 extension-catalog.md 读取对应领域角色列表，每个角色一个选项}
  multiSelect: true
```

对每个选中领域重复此问题。记录所有选中的扩展角色 `ext_roles[]`，每项包含 `department` 和 `role_code`。

完成所有领域的角色选择后：若 team_type 为 discuss → 进入问题 4.5（讨论轮次）；否则 → 进入问题 5（工作目录）。

### 问题 4.5: 讨论轮次（仅 discuss 类型触发）

```
AskUserQuestion:
  question: "每个议题的最大讨论轮次？"
  header: "讨论轮次"
  options:
    - label: "3 轮（默认）"
    - label: "5 轮"
    - label: "自定义"
  multiSelect: false
```

`max_rounds` 写入配置和 prompt 的 `<project_context>` 中。

### 问题 5: 工作目录

```
AskUserQuestion:
  question: "项目工作目录在哪里？"
  header: "工作目录"
  options:
    - label: "当前目录"
      description: "使用当前工作目录"
    - label: "指定路径"
      description: "在「其他」中输入绝对路径"
  multiSelect: false
```

### 确认步骤

输出汇总信息，然后确认：

```
团队配置汇总
--------------------
团队类型: {team_type_name}
项目名称: {project_name}
项目描述: {description}
技术栈:   {tech_stack}
工作目录: {work_dir}

团队成员:
  - {lead_role} x1 (Lead)
  - {role_name} x{count}
  ...
{若有扩展角色}
扩展角色:
  - {ext_role_name} ({department})
  ...

预计创建 {N} 个 Agent
--------------------
```

```
AskUserQuestion:
  question: "确认以上配置并创建团队？"
  header: "确认"
  options:
    - label: "确认创建"
      description: "开始创建团队"
    - label: "修改配置"
      description: "重新开始问答"
    - label: "取消"
      description: "放弃创建"
  multiSelect: false
```

## 团队创建流程

用户确认后，执行以下步骤。

### 步骤 1: 准备角色定义（写入 .teams/）

将角色定义文件复制到项目工作目录的 `.teams/{project_name}/`，供用户在团队启动前审阅和修改。

**来源路径**（相对于 skill base directory）:
- 角色定义: `references/{type_dir}/roles/{role_code}.md`
- 工作流: `references/{type_dir}/workflow.md`

使用 Read 工具时，将以上相对路径拼接到 skill base directory 构建绝对路径。

**写入目标**:

```
{work_dir}/.teams/{project_name}/
├── team.yaml           # 团队配置摘要
├── workflow.md          # 工作流定义（从 references 复制）
└── roles/
    ├── {lead_role}.md   # Lead 角色定义
    ├── {role_1}.md      # 执行角色定义
    └── ...
```

**操作步骤**:

1. 使用 Bash 创建目录: `mkdir -p "{work_dir}/.teams/{project_name}/roles"`
2. 使用 Read 读取每个核心角色定义文件和 workflow.md
3. 使用 Write 将每个核心角色定义写入 `.teams/{project_name}/roles/{role_code}.md`
4. 若有扩展角色（`ext_roles[]` 非空）:
   - 扩展角色来源路径: `references/extensions/{department}/{role_code}.md`
   - 使用 Read 读取每个扩展角色定义
   - 使用 Write 写入 `.teams/{project_name}/roles/ext-{department}-{role_code}.md`（加 `ext-` 前缀）
5. 使用 Write 将 workflow.md 写入 `.teams/{project_name}/workflow.md`
6. 使用 Write 创建 `.teams/{project_name}/team.yaml`:

```yaml
# 团队配置 - 由 /team-init 准备
# 修改 roles/ 下的 .md 文件可自定义角色行为
# 确认后使用「开始创建」启动团队

team_type: "{type_dir}"
team_type_name: "{team_type_name}"
project_name: "{project_name}"
description: "{description}"
tech_stack: "{tech_stack}"
work_dir: "{work_dir}"

roles:
  - role: "{lead_role_code}"
    count: 1
    is_lead: true
  - role: "{role_code}"
    count: {N}
  # ... 核心角色

  # 扩展角色（如有）
  # - role: "ext-{department}-{role_code}"
  #   count: 1
  #   source: extension
  #   department: "{department}"
```

### 步骤 2: 用户审阅角色定义

输出角色文件路径并提示用户审阅：

```
角色定义已准备就绪
--------------------
目录: {work_dir}/.teams/{project_name}/

文件列表:
  workflow.md          — 工作流定义
  roles/{lead_role}.md — {lead_role_name}（Lead）
  roles/{role_1}.md    — {role_1_name}
  roles/{role_2}.md    — {role_2_name}
  ...

您可以在编辑器中打开并修改这些文件，自定义角色行为。
修改完成后选择「开始创建」启动团队。
--------------------
```

```
AskUserQuestion:
  question: "准备好启动团队了吗？"
  header: "审阅角色定义"
  options:
    - label: "开始创建"
      description: "使用当前角色定义（含您的修改）创建团队"
    - label: "打开目录"
      description: "显示文件完整路径，方便在编辑器中打开"
    - label: "取消"
      description: "放弃创建，保留 .teams/ 目录供后续使用"
  multiSelect: false
```

如果用户选择「打开目录」，输出每个文件的完整绝对路径，然后再次询问是否开始创建。
如果用户选择「取消」，输出提示后结束：

```
团队创建已取消。角色定义保留在:
  {work_dir}/.teams/{project_name}/

后续可手动编辑后，使用 /team-init {project_name} 重新启动
（检测到 .teams/ 目录时将直接使用其中的角色定义）。
```

### 步骤 3: 创建团队

```
TeamCreate:
  team_name: "{project_name}"
  description: "{team_type_name} - {description}"
```

### 步骤 4: 读取角色定义和工作流

**从 `.teams/` 目录读取**（而非直接从 references/ 读取），这样包含了用户的修改。

角色定义路径: `{work_dir}/.teams/{project_name}/roles/{role_code}.md`
工作流路径: `{work_dir}/.teams/{project_name}/workflow.md`

对每个选中的角色，使用 Read 工具读取其角色定义文件。
同时读取 workflow.md。

### 步骤 5: 构建角色 Prompt

为每个成员组合 prompt。**Lead 角色与执行角色使用不同的工作流注入策略**，以控制 prompt 长度。

> **重要**: 角色定义从 `.teams/{project_name}/roles/` 读取（步骤 4），包含用户可能做的修改。

#### Lead 角色的 Prompt

Lead 角色负责管理整个工作流，因此注入**完整的 workflow.md 内容**。

```
你是「{project_name}」项目的{role_name}。

<project_context>
项目名称: {project_name}
团队类型: {team_type_name}
项目描述: {description}
技术栈: {tech_stack}
工作目录: {work_dir}
{若 discuss 类型} 最大讨论轮次: {max_rounds}
</project_context>

<team_members>
{列出所有成员的名称和角色}
</team_members>

<workflow>
{workflow.md 的完整内容}
</workflow>

<your_role>
{对应角色 .md 文件的完整内容}
</your_role>
```

#### 执行角色的 Prompt

执行角色无需完整工作流，仅注入 workflow.md 中的**阶段总览表格**（即 `## 阶段总览` 下的 Markdown 表格，通常 5-10 行），不包含各阶段的详细流程描述。

```
你是「{project_name}」项目的{role_name}。

<project_context>
项目名称: {project_name}
团队类型: {team_type_name}
项目描述: {description}
技术栈: {tech_stack}
工作目录: {work_dir}
{若 discuss 类型} 最大讨论轮次: {max_rounds}
</project_context>

<team_members>
{列出所有成员的名称和角色}
</team_members>

<workflow_overview>
{仅 workflow.md 中「阶段总览」表格，不含各 Phase 详细流程}
</workflow_overview>

<your_role>
{对应角色 .md 文件的完整内容}
</your_role>
```

#### 扩展角色的 Prompt

扩展角色（`ext-` 前缀）使用与执行角色相同的 prompt 结构（`<workflow_overview>` 而非完整 workflow），并额外标注扩展角色来源：

```
你是「{project_name}」项目的{role_name}（扩展角色 — {department}）。

<project_context>
项目名称: {project_name}
团队类型: {team_type_name}
项目描述: {description}
技术栈: {tech_stack}
工作目录: {work_dir}
{若 discuss 类型} 最大讨论轮次: {max_rounds}
</project_context>

<team_members>
{列出所有成员的名称和角色}
</team_members>

<workflow_overview>
{仅 workflow.md 中「阶段总览」表格，不含各 Phase 详细流程}
</workflow_overview>

<your_role>
{扩展角色 .md 文件的完整内容}
</your_role>
```

### 步骤 6: 创建初始任务

使用 TaskCreate 根据 workflow.md 的阶段创建任务骨架。
设置阶段间的 blockedBy 依赖关系。
将第一个任务分配给 Lead 角色。

### 步骤 7: 派生团队成员

**Lead 角色必须第一个创建。** 注意：多实例角色（如 developer x2）的每个实例使用相同的角色定义文件。

```
Agent:
  name: "{member_name}"
  subagent_type: "general-purpose"
  team_name: "{project_name}"
  prompt: "{步骤 5 构建的 prompt}"
  mode: "bypassPermissions"
  description: "Team member: {role_name}"
```

命名规则：
- 单实例角色: 直接使用代号 (pm, architect, captain 等)
- 多实例角色: 代号-序号 (developer-1, web-2 等)
- 扩展角色: 使用完整代号 (ext-marketing-xiaohongshu, ext-design-ui-designer 等)

创建顺序：先创建 Lead，再并行创建其他角色。

### 步骤 8: 保存团队配置到项目目录

将团队配置保存到项目工作目录下的 `.team-profiles/{project_name}.yaml`，以便后续通过 `/team-load` 复用。

使用 Write 工具创建文件：

```yaml
# 团队配置 - 由 /team-init 自动生成
# 使用 /team-load {project_name} 可直接加载此配置创建团队

format: template
team_type: "{type_dir}"           # dev/testing/reverse/debug/security/ctf/ops/discuss
team_type_name: "{team_type_name}" # 中文名称
description: "{description}"
tech_stack: "{tech_stack}"
work_dir: "{work_dir}"

roles:
  # Lead 角色（自动包含）
  - role: "{lead_role_code}"
    count: 1
    is_lead: true
  # 核心角色
  - role: "{role_code}"
    count: {N}
  # ... 列出所有选中的核心角色及数量

  # 扩展角色（如有）
  # - role: "ext-{department}-{role_code}"
  #   count: 1
  #   source: extension
  #   department: "{department}"
```

保存后输出提示：
```
团队配置已保存到: {work_dir}/.team-profiles/{project_name}.yaml
后续可使用 /team-load {project_name} 直接加载此团队配置。
```

### 步骤 9: 通知 Lead 启动

```
SendMessage:
  type: "message"
  recipient: "{lead_name}"
  content: |
    团队已创建完成。
    - 项目: {project_name}
    - 描述: {description}
    - 技术栈: {tech_stack}
    - 工作目录: {work_dir}
    - 团队成员: {member_list}

    请开始第一阶段工作。
    工作流: {work_dir}/.teams/{project_name}/workflow.md
    角色定义: {work_dir}/.teams/{project_name}/roles/
  summary: "团队已创建，启动项目"
```

## 复用已有 .teams/ 目录

如果执行 `/team-init` 时检测到 `{work_dir}/.teams/{project_name}/` 已存在（例如上次取消后保留的），跳过步骤 1 的文件写入，直接进入步骤 2（用户审阅）。

提示用户：

```
检测到已有角色定义: .teams/{project_name}/
将使用其中的角色文件创建团队（包含您之前的修改）。

如需重新生成，请先删除 .teams/{project_name}/ 目录。
```

## 注意事项

- `.teams/` 目录应加入 `.gitignore`（属于本地自定义，不入版本控制）
- 多实例角色（如 developer x3）共用同一个角色定义 MD，修改一次影响所有实例
- 用户修改角色 MD 后，修改内容会被原样注入到 agent 的 `<your_role>` 段

## 参考资源

- **`references/role-catalog.md`** - 各团队类型的完整角色列表
- **`references/{type_dir}/roles/{role}.md`** - 各角色详细定义（原始版本）
- **`references/{type_dir}/workflow.md`** - 各团队类型的工作流定义
- **`references/shared/handoff-protocol.md`** - 跨角色交接协议
- **`references/shared/role-template.md`** - 角色定义标准模板
- **`references/extensions/extension-catalog.md`** - 扩展角色索引（146 个跨 12 领域）
- **`references/extensions/{department}/{role_code}.md`** - 扩展角色定义

## 脚本工具

- **`scripts/lint-roles.sh`** - 角色定义文件格式校验（5板块结构检查）
  - `bash <skill_base>/scripts/lint-roles.sh` — 检查所有核心角色
  - `bash <skill_base>/scripts/lint-roles.sh dev` — 检查 dev 团队
  - `bash <skill_base>/scripts/lint-roles.sh --extensions` — 检查扩展角色
  - 脚本使用 `${BASH_SOURCE[0]}` 自动定位，任何安装位置均可工作
