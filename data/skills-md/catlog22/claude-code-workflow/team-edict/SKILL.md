---
name: team-edict
description: |
  三省六部 multi-agent 协作框架，完整复刻 Edict 架构。
  太子接旨 -> 中书省规划 -> 门下省审议(多CLI并行) -> 尚书省调度 -> 六部并行执行。
  强制看板状态上报（state/flow/progress），支持 Blocked 一等公民状态，全流程可观测。
  Triggers on "team edict", "三省六部", "edict team".
allowed-tools: TeamCreate(*), TeamDelete(*), SendMessage(*), TaskCreate(*), TaskUpdate(*), TaskList(*), TaskGet(*), Agent(*), AskUserQuestion(*), Read(*), Write(*), Edit(*), Bash(*), Glob(*), Grep(*)
---

# Team Edict — 三省六部

受古代三省六部制启发的多 agent 协作框架。核心设计：**严格的级联审批流 + 实时看板可观测性 + 多 CLI 并行分析**。

## Architecture

```
+----------------------------------------------------------+
|  Skill(skill="team-edict")                               |
|  args="任务描述"                                          |
+------------------------+---------------------------------+
                         |
              Coordinator (太子·接旨分拣)
              Phase 0-5 orchestration
                         |
         +---------------+--------------+
         |                              |
    [串行审批链]                   [看板 State Bus]
         |                              |
    中书省(PLAN)                  ← 所有 agent 强制上报
         |                         state/flow/progress
    门下省(REVIEW) ← 多CLI审议
         |
    尚书省(DISPATCH) ← 路由分析
         |
    +----+----+----+----+----+----+
    工部  兵部  户部  礼部  吏部  刑部
   (IMPL)(OPS)(DATA)(DOC)(HR)(QA)
   [team-worker × 6, 按需并行]
```

## Role Router

此 skill 为 **coordinator-only**。所有 worker 直接以 `team-worker` agent 形式 spawn。

### 输入解析

直接解析 `$ARGUMENTS` 作为任务描述，始终路由至 coordinator。

### Role Registry

| 角色 | 别名 | Spec | Task Prefix | Inner Loop | 职责 |
|------|------|------|-------------|------------|------|
| coordinator | 太子 | [roles/coordinator/role.md](roles/coordinator/role.md) | (none) | - | 接旨分拣、驱动流程 |
| zhongshu | 中书省 | [role-specs/zhongshu.md](role-specs/zhongshu.md) | PLAN-* | false | 分析旨意、起草执行方案 |
| menxia | 门下省 | [role-specs/menxia.md](role-specs/menxia.md) | REVIEW-* | false | 多维审议、准奏/封驳 |
| shangshu | 尚书省 | [role-specs/shangshu.md](role-specs/shangshu.md) | DISPATCH-* | false | 分析方案、派发六部 |
| gongbu | 工部 | [role-specs/gongbu.md](role-specs/gongbu.md) | IMPL-* | true | 功能开发、架构设计、代码实现 |
| bingbu | 兵部 | [role-specs/bingbu.md](role-specs/bingbu.md) | OPS-* | true | 基础设施、部署、性能监控 |
| hubu | 户部 | [role-specs/hubu.md](role-specs/hubu.md) | DATA-* | true | 数据分析、统计、资源管理 |
| libu | 礼部 | [role-specs/libu.md](role-specs/libu.md) | DOC-* | true | 文档、规范、UI/UX、对外沟通 |
| libu-hr | 吏部 | [role-specs/libu-hr.md](role-specs/libu-hr.md) | HR-* | false | Agent 管理、培训、考核评估 |
| xingbu | 刑部 | [role-specs/xingbu.md](role-specs/xingbu.md) | QA-* | true | 代码审查、测试验收、合规审计 |

### 门下省 — 多 CLI 审议配置

门下省审议使用**多 CLI 并行分析**，同时从多个维度评估方案：

| 审议维度 | CLI Tool | Focus |
|----------|----------|-------|
| 可行性审查 | gemini | 技术路径、依赖完备性 |
| 完整性审查 | qwen | 子任务覆盖度、遗漏识别 |
| 风险评估 | gemini (second call) | 故障点、回滚方案 |
| 资源评估 | codex | 工作量合理性、部门匹配度 |

### 六部路由规则

尚书省（DISPATCH）根据任务内容将子任务路由至对应部门：

| 关键词信号 | 目标部门 | 说明 |
|-----------|---------|------|
| 功能开发、架构、代码、重构、实现 | 工部 (gongbu) | 工程实现 |
| 部署、CI/CD、基础设施、容器、性能监控 | 兵部 (bingbu) | 运维部署 |
| 数据分析、统计、成本、报表、资源 | 户部 (hubu) | 数据管理 |
| 文档、README、API文档、UI文案、规范 | 礼部 (libu) | 文档规范 |
| 测试、QA、Bug、审查、合规 | 刑部 (xingbu) | 质量保障 |
| Agent管理、培训、技能优化、考核 | 吏部 (libu-hr) | 人事管理 |

### Dispatch

始终路由至 coordinator (太子)。

### Orchestration Mode

用户只提供任务描述。

**调用**: `Skill(skill="team-edict", args="任务描述")`

**生命周期**:
```
用户提供任务描述
  -> coordinator Phase 1-2: 接旨判断 -> 简单问答直接回复 | 正式任务建 PLAN 任务
  -> coordinator Phase 3: TeamCreate -> spawn 中书省 worker (PLAN-001)
  -> 中书省执行 -> 生成执行方案 -> SendMessage callback
  -> coordinator spawn 门下省 worker (REVIEW-001) <- 多CLI并行审议
  -> 门下省审议 -> 准奏/封驳 -> SendMessage callback
    -> 封驳: coordinator 通知中书省修改 (最多3轮)
    -> 准奏: coordinator spawn 尚书省 worker (DISPATCH-001)
  -> 尚书省分析路由 -> 生成六部任务清单 -> SendMessage callback
  -> coordinator 按任务清单 spawn 六部 workers (按依赖并行/串行)
  -> 六部执行 -> 各自 SendMessage callback
  -> coordinator 汇总所有六部产出 -> Phase 5 报告
```

**用户命令** (唤醒暂停的 coordinator):

| 命令 | 动作 |
|------|------|
| `check` / `status` | 输出看板状态图，不推进 |
| `resume` / `continue` | 检查 worker 状态，推进下一步 |
| `revise PLAN-001 <反馈>` | 触发中书省重新起草 (封驳循环) |

## 看板状态协议

所有 worker 必须遵守以下状态上报规范（强制性）：

### 状态机

```
Pending -> Doing -> Done
              |
           Blocked (可随时进入，需上报原因)
```

### 状态上报调用

每个 worker 使用 `team_msg` 进行看板操作（替代 kanban_update.py）：

```javascript
// 接任务时
team_msg(operation="log", session_id=<session_id>, from=<role>,
  type="state_update", data={state: "Doing", current_step: "开始执行[任务]"})

// 进度上报 (每个关键步骤)
team_msg(operation="log", session_id=<session_id>, from=<role>,
  type="impl_progress", data={
    current: "正在执行步骤2：实现API接口",
    plan: "步骤1分析✅|步骤2实现🔄|步骤3测试"
  })

// 任务交接 (flow)
team_msg(operation="log", session_id=<session_id>, from=<role>, to="coordinator",
  type="task_handoff", data={from_role: <role>, to_role: "coordinator", remark: "✅ 完成：[产出摘要]"})

// 阻塞上报
team_msg(operation="log", session_id=<session_id>, from=<role>, to="coordinator",
  type="error", data={state: "Blocked", reason: "[阻塞原因]，请求协助"})
```

## Specs Reference

| 文件 | 内容 | 使用方 |
|------|------|--------|
| [specs/team-config.json](specs/team-config.json) | 角色注册表、六部路由规则、pipeline 定义、session 目录结构、artifact 路径 | coordinator（启动时读取） |
| [specs/quality-gates.md](specs/quality-gates.md) | 各阶段质量门标准、跨阶段一致性检查规则、消息类型对应关系 | coordinator（Phase 8 汇总验收时）、xingbu（QA 验收时） |

## Session Directory

```
.workflow/.team/<session-id>/
├── plan/
│   ├── zhongshu-plan.md       # 中书省起草的执行方案
│   └── dispatch-plan.md       # 尚书省生成的六部任务清单
├── review/
│   └── menxia-review.md       # 门下省审议报告（含多CLI结论）
├── artifacts/
│   ├── gongbu-output.md       # 工部产出
│   ├── xingbu-report.md       # 刑部测试报告
│   └── ...                    # 各部门产出
├── kanban/
│   └── state.json             # 看板状态快照
└── wisdom/
    └── contributions/         # 各 worker 知识沉淀
```

## Spawn Template

Coordinator 使用以下模板 spawn worker：

```javascript
Agent({
  subagent_type: "team-worker",
  name: "<role>",
  team_name: "<team_name>",
  prompt: `role: <role>
role_spec: ~  or <project>/.claude/skills/team-edict/role-specs/<role>.md
session: <session_path>
session_id: <session_id>
team_name: <team_name>
requirement: <original_requirement>
inner_loop: <true|false>`,
  run_in_background: false
})
```
