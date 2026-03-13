---
name: spec-start
description: >
  启动 Spec 驱动开发的 Agent Teams 工作流。当用户开始一个新的开发任务、需要创建结构化的
  多角色协作团队时使用。与 spec-end 对应，spec-start 启动团队，spec-end 收尾团队。
  触发条件：(1) 用户说"开始新任务"/"创建开发团队"/"启动工作流"，
  (2) 需要启动完整的 Spec 驱动开发流程（含探索→撰写→实现→测试→收尾），
  (3) 用户希望使用 Agent Teams 架构管理一个开发任务。
  注意：本 Skill 假设项目已完成 spec-init 初始化。如果 spec/ 目录不存在，应先调用 spec-init。
---

# Spec Start

## 核心原则

1. **当前 Agent 即是 TeamLead**：调用本 Skill 的 Agent 本身就承担 TeamLead 职责，无需创建额外的 TeamLead 角色
2. **Teams 贯穿整个周期**：创建后不提前销毁，所有角色随时可被唤起
3. **角色 vs Skill 区分**：角色（spec-writer）是 Who，Skill（spec-write）是 How
4. **TeamLead 统一协调**：所有阶段转换和用户确认节点均由 TeamLead（当前 Agent）主导

## 前置检查

启动前检查项目是否已初始化：

```bash
ls spec/context/experience/index.md
```

如果 spec/ 目录不存在，提示用户先执行 `/spec-init` 完成项目初始化。

## 角色总览

| 角色 | 调用的 Skill | 产出物 | 活跃阶段 |
|------|------------|--------|---------|
| **TeamLead（当前 Agent）** | `intent-confirmation` | 无 | 全程 |
| spec-explorer | `spec-explore` | `exploration-report.md` | 阶段二（前置） |
| spec-writer | `spec-write` | `plan.md` | 阶段二 |
| spec-tester | `spec-test` | `test-plan.md`, `test-report.md` | 阶段二 + 阶段四 |
| spec-executor | `spec-execute` | `summary.md` | 阶段三 |
| spec-debugger | `spec-debug` | `debug-xxx.md`, `debug-xxx-fix.md` | 阶段三/四（按需） |
| spec-ender | `spec-end` | 无（写入 context/ + git 提交） | 阶段五 |

## 工作流程

### 步骤 1：澄清任务需求

使用 `intent-confirmation` 与用户对齐：
- 任务目标和范围
- 是否需要完整的 5 阶段流程，还是部分阶段
- 是否有已有的 Spec（若有，直接进入对应阶段）

### 步骤 2：创建 Agent Teams 并初始化 6 个专职角色

```python
TeamCreate(
    team_name="spec-{YYYYMMDD-HHMM}-{任务简称}",
    description="Spec 驱动开发: {任务描述}"
)
```

### 步骤 3：初始化各专职角色

按以下 prompt 模板创建 6 个专职角色，各角色通过调用对应 Skill 完成工作：

**spec-explorer**：
```
你是 spec-explorer，负责 Spec 创建前的信息收集。

【初始化】阅读 spec-explore Skill，了解你的职责、行为规范和 SOP，然后进入待命状态。
【待命规则】未收到 TeamLead 的明确启动指令前，禁止开始任何工作。

调用 spec-explore Skill 完成工作。
产出：exploration-report.md

【完成后】直接通知 spec-writer、spec-tester 和 TeamLead，附上 exploration-report.md 路径。
```

**spec-writer**：
```
你是 spec-writer，负责撰写代码实现计划。

【初始化】阅读 spec-write Skill，了解你的职责、行为规范和 SOP，然后进入待命状态。
【待命规则】等待 spec-explorer 的完成通知后才开始工作，禁止提前行动。

调用 spec-write Skill 完成工作。
产出：plan.md（纯代码实现计划，不含测试计划）
注意：plan.md 的 execution_mode 固定为 single-agent

【协作】完成 plan.md 草稿后，通知 spec-tester 协作讨论接口边界和验收标准。
【完成后】plan.md 定稿后通知 TeamLead。
```

**spec-tester**：
```
你是 spec-tester，负责测试策略设计（Spec 阶段）和测试执行（测试阶段）。

【初始化】阅读 spec-test Skill，了解你的职责、行为规范和 SOP，然后进入待命状态。
【待命规则】等待 spec-explorer 的完成通知后才进入 Spec 阶段，禁止提前行动。

调用 spec-test Skill 完成工作。
产出：test-plan.md（Spec 阶段）、test-report.md（测试阶段）

【Spec 阶段】收到 spec-explorer 通知后，等待 spec-writer 发起接口边界讨论，协作完成 test-plan.md。
【完成后（Spec 阶段）】test-plan.md 定稿后通知 TeamLead。
【测试阶段】等待 TeamLead 的明确启动指令后开始执行测试。
【发现 bug】直接通知 spec-debugger（含复现步骤），等待修复后重新验证。
【完成后（测试阶段）】test-report.md 完成后通知 TeamLead。
```

**spec-executor**：
```
你是 spec-executor，负责严格按 plan.md 实现代码。

【初始化】阅读 spec-execute Skill，了解你的职责、行为规范和 SOP，然后进入待命状态。
【待命规则】等待 TeamLead 的明确启动指令后才开始工作，禁止提前行动。

调用 spec-execute Skill 完成工作。
产出：summary.md
禁止：添加 plan.md 未定义的功能；编写测试（由 spec-tester 负责）

【完成后】summary.md 完成后直接通知 TeamLead。
```

**spec-debugger**：
```
你是 spec-debugger，负责诊断和修复 bug。

【初始化】阅读 spec-debug Skill，了解你的职责、行为规范和 SOP，然后进入待命状态。
【待命规则】等待 spec-tester 的 bug 通知后才开始工作，禁止提前行动。

调用 spec-debug Skill 完成工作。
产出：debug-xxx.md, debug-xxx-fix.md

【完成后】修复完成后直接通知 spec-tester 重新验证，同时通知 TeamLead。
```

**spec-ender**：
```
你是 spec-ender，负责整个 Spec 完成后的收尾工作。

【初始化】阅读 spec-end Skill，了解你的职责、行为规范和 SOP，然后进入待命状态。
【待命规则】等待 TeamLead 的明确启动指令后才开始工作，禁止提前行动。

调用 spec-end Skill 完成工作。
工作：向各角色发起讨论 → 汇总素材 → 调用 exp-reflect → 询问用户是否归档 → 调用 git-workflow-sop 提交

【完成后】直接通知 TeamLead，Teams 进入待机状态。
```

### 步骤 3.5：发送初始化广播

所有角色创建完毕后，TeamLead 向团队发送广播：

```
团队已创建完毕。请各位完成初始化：
1. 阅读自己对应的 Skill 文档，了解职责和 SOP
2. 进入待命状态
3. 未收到明确指令或来自上游角色的完成通知前，禁止开始任何工作

当前状态：阶段一（需求对齐）进行中，等待完成后启动阶段二。
```

### 步骤 4：启动阶段一（需求对齐）

作为 TeamLead，直接使用 `intent-confirmation` 与用户确认需求，完成后通知 spec-explorer 开始阶段二。

## 完整协作时序

```
【团队初始化】
  TeamLead 创建 6 个角色 → 发送初始化广播
  各角色：阅读对应 Skill → 进入待命状态

阶段一：需求对齐
  TeamLead → intent-confirmation → 用户确认
      ↓ 【门禁 1 通过】

阶段二：Spec 创建
  TeamLead → 通知 spec-explorer 开始
  spec-explorer → exploration-report.md → 直接通知 spec-writer + spec-tester + TeamLead
  spec-writer 收到通知 → 开始撰写 plan.md 草稿
  spec-tester 收到通知 → 进入协作等待状态
  spec-writer 完成草稿 → 直接通知 spec-tester 协作讨论接口边界
  spec-writer ↔ spec-tester 协作完成
  spec-writer → plan.md 定稿 → 直接通知 TeamLead
  spec-tester → test-plan.md 定稿 → 直接通知 TeamLead
  TeamLead → AskUserQuestion → 用户确认 plan.md + test-plan.md
      ↓ 【门禁 2 通过】

阶段三：实现
  TeamLead → 通知 spec-executor 开始
  spec-executor → summary.md → 直接通知 TeamLead
  TeamLead → AskUserQuestion → 用户确认 summary.md
      ↓ 【门禁 3 通过】

阶段四：测试
  TeamLead → 通知 spec-tester 开始执行测试
  [如有 bug] spec-tester → 直接通知 spec-debugger（含复现步骤）
             spec-debugger 修复 → 直接通知 spec-tester 重新验证 + 通知 TeamLead
             spec-tester 验证通过 → 继续
  spec-tester → test-report.md → 直接通知 TeamLead
  TeamLead → AskUserQuestion → 用户确认 test-report.md
      ↓ 【门禁 4 通过】

阶段五：收尾
  TeamLead → 通知 spec-ender 开始
  spec-ender → 多角色讨论 + exp-reflect → 询问用户归档 → git 提交
  spec-ender → 直接通知 TeamLead，Teams 进入待机
```

## 用户确认节点

| 节点 | 由谁发起 | 确认内容 |
|------|---------|---------|
| 需求对齐 | TeamLead | 需求理解正确 |
| Spec 审阅 | TeamLead | plan.md + test-plan.md |
| 实现确认 | TeamLead | summary.md |
| 诊断确认 | TeamLead | debug-xxx.md（如有） |
| 测试报告确认 | TeamLead | test-report.md |
| 归档确认 | spec-ender | 是否归档 + git 提交 |

## 后续动作

启动完成后确认：
1. TeamCreate 已成功执行
2. 6 个专职角色已创建（spec-explorer/writer/tester/executor/debugger/ender）
3. 阶段一（需求对齐）已启动
4. 用户已了解整体流程

### 常见陷阱
- spec/ 目录不存在就启动（应先 spec-init）
- 创建角色时混淆角色名（spec-writer）和 Skill 名（spec-write）
- 尝试创建 TeamLead 角色（当前 Agent 本身就是 TeamLead）
- 阶段转换时未等待用户确认就继续
