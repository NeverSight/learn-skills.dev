---
name: ohos-req-feature-baseline
description: Use when preparing an OHOS Feature for Phase 0.4 review, especially for 04-feature.md, SIG review readiness, proposal splitting, feature scope, acceptance criteria, or delivery impact. Do NOT use for requirement intake (ohos-req-requirement-intake), feasibility analysis (ohos-req-feasibility-analysis), or review gate (ohos-req-review-gate).
metadata:
  author: openharmony
  scope: common
  stage: requirements
  capability: feature-baseline
  version: 0.3.0
  status: draft
  tags:
    - sdd
    - requirements
---

# OHOS Feature 评审基线

**Announce at start:** "我正在使用 ohos-req-feature-baseline skill 生成 04-feature.md。"

## 定位

04-feature.md 是 OHOS SIG 评审会议和 IR 生成的共同输入。工作量分级约束（PIR #152 P1）按端到端总人月推导：简单(≤5)/标准(≤8)/复杂(≤15)三级，复杂特性须有独立验收边界。模块覆盖完整性校验引用 02-feasibility.md §2.1 代码仓库分析表，缺失模块必须补行或写明排除理由。03-arch-decision-record.md §6 遗留问题闭环校验阻断 Not Ready Gate。

## ⭐ 思维准则

在给出拆分建议前，自问：是否按 R1→R2→R3→R4 顺序逐条评估？是否在首个触发处即停止，还是跳过了某些检查？
- Before checking module coverage, ask yourself: am I cross-checking 02 §2.1 against 04 §4 line-by-line, or eyeballing from memory?
- Before detecting terminology drift, ask yourself: am I comparing every 影响类型 label between 02 and 04, or skipping reusable ones?

## 输入

- `{docs_dir}/01-requirement.md`
- `{docs_dir}/02-feasibility.md`
- `{docs_dir}/03-arch-decision-record.md`

## 流程

## 模板与产物命名

- 模板路径：`reference/feature.md`（模板文件不带 `04-` 阶段编号前缀）
- 产物路径：`{docs_dir}/04-feature.md`

1. 读取 `reference/feature.md` 和全部输入。
2. 从 `01-requirement.md` frontmatter 继承 `rr_id` 到 04-feature.md frontmatter，并在 §1 概述与价值后填写 RR单号表格行。
3. 收敛一句话特性、价值、目标/非目标、优先级范围和 AC。
4. 摘要记录选定方案、未选方案原因及 Phase 2 验证项。
5. 明确仓库、模块、Owner/SIG、交付物、里程碑、依赖和开放项。
6. 补充「需求变更影响性分析」章节（模板外补充章节，不对应模板 §-编号）：对以下五方逐项分析影响类型（正向优化/无影响/需适配）：
   - **北向应用开发者**：关注 API 变更、行为变更、兼容性
   - **南向开发者**：关注底层接口变更、新增能力
   - **分布式设备**：关注跨设备场景影响
   - **系统开发者（跨子系统）**：关注子系统间接口/依赖变更
   - **设备使用者**：关注用户可感知的功能/体验变更
7. **模块覆盖完整性校验**：提取 02-feasibility.md §2.1"关键代码仓库分析"表中所有仓库/模块，与 §4"受影响模块"表对比。02 中出现但 04 中缺失的仓库/模块必须补行或写明排除理由。在 §4 写入 **模块覆盖检查结论**：pass（齐全）或 warn（有排除理由），供 `ohos-req-review-gate` 读取。
   - **降级规则**：若 02-feasibility.md 不含 §2.1 关键代码仓库分析表，则跳过模块覆盖校验并标注 `warn`（"模块覆盖校验未执行：02-feasibility.md 缺少 §2.1"），不 `fail`。
8. **影响类型术语校验**：对比同一模块在 02-feasibility.md §2.1 和 §4中的影响类型标签。漂移（如"可复用"→"需扩展"）必须在 §4 补充变更理由备注，并在 §4 写入 **术语一致性检查结论**：pass（无漂移）或 warn（有漂移已补理由），供 `ohos-req-review-gate` 读取。
9. 判断是否拆分 proposal，并定义每个 proposal 的独立价值、边界、AC、**工作量估算**和依赖。拆分表必须包含每个 proposal 的估算工作量（人月）。**计算端到端总工作量**（= 各 proposal 工作量之和），按总人月推导复杂度（<5 简单 / 5-10 标准 / >10 复杂），填入 §5「端到端总工作量」与「复杂度」字段——此复杂度即 R3 拆分上限（简单≤5 / 标准≤8 / 复杂≤15 人月）的判定依据。
10. **⭐ 拆分结果确认门禁**：向用户展示拆分方案（每个 proposal 的边界、工作量、Owner、依赖），等待用户确认或调整后才允许进入 Step 0.5。AI 不自行定稿拆分方案。
11. 保存到 `{docs_dir}/04-feature.md`。
12. 执行 Review Ready Gate（读取刚保存的 04-feature.md，确保 Gate 判定基于用户已确认的最终版本）。

## 职责边界

方案选型决策(ADR)由 `ohos-req-arch-decision` skill 负责，本 skill 只收敛 Feature 评审基线。

## 遗留问题闭环校验

在生成 04-feature.md 之前，必须校验 03-arch-decision-record.md §6 遗留问题闭环状态：

1. 读取 03-arch-decision-record.md §6 全部遗留项。
2. 对每条遗留项检查：负责人、解决动作、计划关闭时间 三字段是否齐全。
3. 任一遗留项缺少三字段 → Gate 降级为 Not Ready，block_reasons 记录缺失项。
4. §6 为占位（`[待用户评审会议后填写]`）且无实际遗留项 → Gate 降级为 Not Ready，block_reasons 记录"03-arch-decision-record.md §6 遗留问题未由用户评审会议输入"。
5. §6 无遗留项（用户评审会议认定无需遗留）→ 视为通过，无需阻断。

## Review Ready Gate

- `Ready`：所有检查项通过，可生成 IR 并进入正式评审。
- `Conditional Ready`：无失败项，所有条件项都有 Owner、关闭动作和时点，可生成带条件 IR。
- `Not Ready`：存在失败项或无需求导入计划的阻塞项；禁止生成 IR、proposal 或正式需求 PPT。

### AC一致性校验

主 Session 在 Gate 后生成 FR→AC 追溯表，检查编号一致性：每条 FR 必须映射到至少一条 AC，AC 编号在 04-feature.md 内唯一且无遗漏。

## 错误处理

| 场景 | 恢复指导 |
|------|---------|
| Not Ready (04-feature.md 内容不完整) | 告知用户缺失的具体章节，引导回 Step 0.4 对应子步骤补全 |
| Not Ready (01-03 未完成) | 告知用户需先完成上游 Step 0.1-0.3，列出缺失文档 |
| Conditional Ready | 列出条件项，引导用户确认是否接受条件放行或退回修改 |
| 拆分未确认 (Step 10 gate) | 提示用户确认拆分方案，不可自行定稿 |

## 拆分规则

拆分规则详见 [reference/split-rules.md](reference/split-rules.md)。核心：R1仓库隔离→R2子系统隔离→R3工作量约束→R4默认不拆。工作量分级：简单≤5/标准≤8/复杂≤15人月。

## 自检

- [ ] 内容可追溯到 01-03
- [ ] RR单号已从 01-requirement.md 继承（frontmatter `rr_id` + §一表格）
- [ ] 目标、非目标、AC 和范围可评审
- [ ] 影响范围有 Owner/SIG 和交付物
- [ ] Conditional 项有 Owner 和关闭时点
- [ ] 拆分结论包含事实依据
- [ ] 拆分表每个 proposal 有估算工作量（人月，不超过复杂度上限）
- [ ] §5 端到端总工作量字段已填写（= 各 proposal 工作量之和），复杂度与总工作量匹配
- [ ] 拆分结果已经用户确认（非 AI 自行定稿）
- [ ] 03-arch-decision-record.md §6 遗留问题由用户评审会议输入（非 AI 生成）
- [ ] 03-arch-decision-record.md §6 每条遗留项负责人/解决动作/计划关闭时间齐全

## NEVER

- **禁止 AI 自行定稿拆分方案**：拆分结果必须经用户确认后才允许进入 Step 0.5（原因：拆分涉及资源分配和交付优先级，属人类决策）
- **禁止 AI 代行 §6 遗留问题生成**：遗留问题必须由用户评审会议输入，不得从 feasibility 条件项或风险自动推演（原因：AI 推演会引入虚构风险项）
- **禁止 Not Ready 时生成 IR/proposal/PPT**：存在失败项时禁止生成 IR、proposal 或正式需求 PPT（原因：未通过门禁的需求进入下游会导致返工和评审阻塞）
- **禁止复制 01-03 详细论证**：04-feature.md 只收敛结论，不复制详细论证（原因：避免文档冗余和信息不一致）

## 输出

- 路径：`{docs_dir}/04-feature.md`
- 方案摘要章节：改为一句话引用 03-arch-decision-record.md 选定方案，格式为 "选定方案: PATH-XX（参见 03-arch-decision-record.md）"，不重复决策细节
- 回传：路径、RR单号、Gate 结论、评审建议、拆分结论、影响性分析结论和阻塞项
