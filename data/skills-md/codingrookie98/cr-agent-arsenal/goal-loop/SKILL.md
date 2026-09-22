---
name: goal-loop
description: Use when executing long-horizon engineering goals that span multiple files or modules, are expected to exceed ~10 minutes, or need durable cross-session state and a strict delivery gate. Triggers on multi-module refactors, cross-cutting feature work, long bug hunts, any task where tiered testing (L0–L3), checkpoint persistence, and an adversarial Zero-Blockers review are required, and legacy-system maintenance fixes whose triage needs the lightweight Maintenance-Patch track.
license: MIT
---

# `goal-loop` 目标实现循环

## 概述

面向长程、跨模块研发任务的自愈闭环状态机：以**计划文件为唯一可读真相源**，按需联动 `brainstorming`、`grilling`、`research`、`writing-plans` 与 `dual-round-review`，用分级测试（L0–L3）与对抗式终审守住交付质量。

本文件是**路由层**：只声明触发条件、不变式与阶段指针。阶段细则见 [stage-progression-protocol.md](references/stage-progression-protocol.md)。

---

## 何时使用 / 何时不用

**使用**（满足任一）：
- 涉及 2 个以上文件或模块，或改动公共契约/数据模型；
- 预期耗时超过约 10 分钟；
- 需要跨会话/中断恢复，或步骤繁多易上下文腐化；
- 需要高保真交付与分级测试保护。

**不用**：纯文案微调、单行常量修改、直接的只读问答检索。

---

## 铁律 (Invariants)

1. **计划文件是唯一人类可读真相源**。进度、复选框与检查点写入计划头部；机器状态写入宿主原生 goal 原语，**不建并行状态文件**（`scripts/goal-state-tracker.sh` 只做派生读写）。
2. **先读检查点再动**。进入新阶段或恢复会话时，首选动作是读计划头部的 `Active Checkpoint` 锚点。
3. **未获用户明确认可（User Nod），不写代码、不写落地计划**（P-1 门禁）。
4. **选型裁决未完成，不进 P1 计划**（P0.5 门禁）；优先复用成熟方案，自研必须书面辩护。
5. **P3 开工前向用户确认执行后端**：宿主原生子智能体 / `agy` 无头进程 / 当前会话内联。
6. **按裁定级别测试，先红后绿**：级别以计划中的《测试策略裁定书》为准，Exit Code 0 才允许原子提交。
7. **分支隔离**：在功能分支工作，不在 `main`/`master` 直接写代码。
8. **交付前必须有独立子智能体的 Zero Blockers 裁决**：Heavy Track 走全量双轮对抗审查；Fast-Track 走定向单轮红队审查，触及公共契约或核心链路时升级为全量双轮。
9. **重试有上限**：单错误修复上限 3 次（第 2 次触发微观调研，第 3 次熔断上报）；场景级更小上限（如编译失败 2 次、重构破坏测试 2 次）优先触发其对应动作；Delta Re-Loop 迭代上限 5 次。
10. **事实即刻落盘**：每 2 次只读探查后，把结论写入 `.goal-loop/scratchpad.md` 或检查点锚点。
11. **写入后 Read-Modify-Verify**：用 `git diff`、关键行回读或测试/编译退出码确认变更生效。
12. **不执行破坏性 Git 命令**（`reset`/`rebase`/`revert`/`restore`/`clean -fd`/强制推送）。

> 需要更高置信度的细节时，读 `references/` 下对应文件；不要将细则抄回本文件。

---

## 阶段路由 (Phase Routing)

| 阶段 | 目标 | 外部技能 | 产物 / 指针 |
|:---:|---|---|---|
| **P-1** | 意图对齐 | `brainstorming` | 2~3 个备选方案；门禁见 [stage-progression-protocol.md](references/stage-progression-protocol.md) |
| **P0** | 方案压力测试 | `grilling` | 需求确认文档 = `docs/proposals/RFC-{NNNN}-{slug}.md`（收敛出口，In Review）；台账段落见 RFC 标准模板 §6；存量工程评估可选 [evaluation-report-template.md](templates/evaluation-report-template.md) |
| **P0.5** | 调研与开源选型 | `research` / `find-docs` | [research-spike-template.md](templates/research-spike-template.md) |
| **P1** | 计划与测试定级 | `writing-plans` | [goal-plan-template.md](templates/goal-plan-template.md) + [testing-decision-matrix.md](references/testing-decision-matrix.md) |
| **P2** | 原子任务拆解 | — | [atomic-task-template.md](templates/atomic-task-template.md) |
| **P3** | TDD 循环实现 | 宿主执行后端（开工前询问用户） | [host-adapters.md](references/host-adapters.md) |
| **P3.5** | 集成验证 | 前端产物验收：`frontend-qa-gate`（设计任务另挂 `taste-driven-designer`） | [stage-progression-protocol.md](references/stage-progression-protocol.md) |
| **P4** | 对抗式终审 | `dual-round-review` | [stage-progression-protocol.md](references/stage-progression-protocol.md) |
| **P5** | 文档归档 | `doc-governance`（可选） | [documentation-sync-matrix.md](references/documentation-sync-matrix.md) |

**通道裁剪**：
- **Fast-Track（敏捷轻量）**：豁免 P-1 / P0 / P0.5，直接进入 P1 轻量计划与 P3；
- **Maintenance-Patch（存量维护）**：豁免 P-1 / P0 / P0.5 / P2；保留 P1 极简计划（现象/复现/根因假设/修复范围/回归测试）、P3 定位与回归测试、P3.5 L2 局部回归、P4 定向单轮红队审查。**强制保留 3-Tries 熔断、修复前先复现、修复必带回归测试、Diff 范围锁定**；一旦需改公共契约即升级为 Heavy Track。

判定阈值、通道 C 完整规程与误判降级规则见 [stage-progression-protocol.md](references/stage-progression-protocol.md) 的执行通道分级判定矩阵。

---

## 异常恢复

同一错误连续 3 次未解决即触发熔断（STOP → RECORD → RESEARCH → ESCALATE），生成结构化仲裁报告并暂停等待人类裁决。完整失败矩阵与报告模板见 [failure-recovery-protocol.md](references/failure-recovery-protocol.md)。

---

## 辅助状态脚本（可选）

`scripts/goal-state-tracker.sh` 提供断点看板与阶段切换。技能目录随安装方式而定（源码仓库通常为 `skills/goal-loop`，安装后通常为 `.agents/skills/goal-loop`）：

```bash
SKILL_DIR="<goal-loop 技能实际所在目录>"
bash "$SKILL_DIR/scripts/goal-state-tracker.sh" init "目标名称" "计划文件路径"
bash "$SKILL_DIR/scripts/goal-state-tracker.sh" status
bash "$SKILL_DIR/scripts/goal-state-tracker.sh" set-phase P3
bash "$SKILL_DIR/scripts/goal-state-tracker.sh" complete-task "p3-1"
```

> 计划文件始终是唯一可读真相源，该脚本仅作派生视图。

---

## 参考导航

- [host-adapters.md](references/host-adapters.md) — P3 执行后端的能力契约、用户选择与降级规则
- [stage-progression-protocol.md](references/stage-progression-protocol.md) — P-1 到 P5 执行细则、分流矩阵与门禁
- [testing-decision-matrix.md](references/testing-decision-matrix.md) — 改动特征到 L0~L3 的判定规则
- [context-engineering.md](references/context-engineering.md) — 2-Action Rule、读写决策矩阵与检查点规范
- [failure-recovery-protocol.md](references/failure-recovery-protocol.md) — 失败矩阵与 3-Tries 熔断
- [documentation-sync-matrix.md](references/documentation-sync-matrix.md) — P5 文档联动复核清单
- 模板套件：`templates/` 下的计划、原子任务、调研与评估四份模板
