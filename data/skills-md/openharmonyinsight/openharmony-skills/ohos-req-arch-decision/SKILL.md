---
name: ohos-req-arch-decision
description: Use when selecting an OHOS solution direction in Phase 0.3, especially for 03-arch-decision-record.md, candidate options comparison, or when the main session needs structured ADR output with user-provided decision. Do NOT use for feasibility analysis (ohos-req-feasibility-analysis), feature baseline (ohos-req-feature-baseline), or review gate (ohos-req-review-gate).
metadata:
  author: openharmony
  scope: common
  stage: requirements
  capability: arch-decision
  version: 0.3.0
  status: draft
  tags:
    - sdd
    - requirements
---

# OHOS 方案选型决策分析

**Announce at start:** "我正在使用 ohos-req-arch-decision skill 生成 03-arch-decision-record.md。"

## 定位

`03-arch-decision-record.md` 记录候选方案对比和用户决策结论，为 SIG 初审提供选型依据。OHOS SIG 采用集体评审制度，方案选型权归属 SIG 评审会议（由 SIG Maintainer + 领域 Owner 组成），AI 仅提供候选方案对比和推荐倾向参考，不代行决策权——决策结论必须由用户（代表 SIG 评审结论）提供。

## 核心原则 ⭐

**决策结论必须由用户提供，AI 不替代用户做决策。**

两阶段执行：
- **阶段 A（候选方案分析）**：生成候选方案对比表和 AI 推荐倾向，输出草稿供用户决策参考。
- **阶段 B（决策定稿）**：用户提供决策结论后，填入 §5-§6，输出定稿。

**⚠️ 阶段 A 完成后必须暂停，主 Session 向用户展示候选方案并等待用户决策。不允许跳过用户决策直接推进到阶段 B 或后续 Step。**

## 输入

- `{docs_dir}/01-requirement.md`
- `{docs_dir}/02-feasibility.md`
- 阶段 B 额外输入：用户决策结论（选定方案、理由、决策者）+ 用户评审会议认定的遗留问题清单

## 自省提示（Mindset Prompts）

在执行关键步骤前，自问以下问题。这些问题把 SIG 评审会议的真实约束传递给 AI——方案选型权归属评审会议，AI 只负责候选对比与推荐倾向参考，任何一步替用户决策都会让未评审的方案进入下游。

- **Before writing §1 (背景与问题), ask yourself:** am I reading constraints from 01-requirement.md，还是在自行推断硬约束？硬约束应一行简述，不展开为表格。
- **Before constructing §3 (候选方案对比表), ask yourself:** 候选方案是 feasibility 给出的客观路径，还是我在自行扩充/裁剪？每个方案是否都有一句话描述 + 工作量 + 优势 + 劣势 + 风险 + AI 推荐倾向？对比表是否中立呈现，未夹带选型结论？
- **Before writing §5 (决策结论), ask yourself:** 这份结论来自用户（代表 SIG 评审），还是我在替用户拍板？§5 是否仍为占位？
- **Before writing §6 (遗留问题), ask yourself:** 这份清单是评审会议提供的，还是我在从 feasibility 条件项/风险自动推演？AI 推演会引入虚构风险项。
- **Before pausing after 阶段 A, ask yourself:** 我是否真的暂停等待用户决策了，还是直接推进到了阶段 B？status 是否保持 `PendingDecision`？
- **Before triggering 单方案快速路径, ask yourself:** feasibility §6 是否明确标注其他路径 ❌不可行 且有证据支撑？还是只有一个方案被标 ✅ 而其余未排除？触发条件不满足时必须回到标准两阶段流程。
- **Before writing §6 占位 in 阶段 B（用户未提供遗留问题）, ask yourself:** 我是否保留了 `[待用户评审会议后填写]` 并保持 status=`PendingDecision`，而不是自行补全 §6 凑闭环？

## 阶段 A：候选方案分析（subagent 执行）

1. 读取 `reference/arch-decision-record.md` 和输入文件。模板文件不带 `03-` 阶段编号前缀；`03-arch-decision-record.md` 仅作为 `{docs_dir}` 下的产物文件名。模板只定义产物结构（6个章节），流程规则（两阶段写入、AI不代行决策等）全部由本 skill 控制，不在模板中呈现。
2. 定义决策问题和硬约束 → 写入 §1 背景与问题（约束条件写为一行简述，不展开为表格）。
3. 从 feasibility 候选路径中提取方案，生成候选方案对比表（一句话描述 + 工作量 + 主要优势 + 主要劣势 + 主要风险 + AI 推荐倾向）→ 写入 §3 候选方案对比。
4. §5 决策结论、§6 遗留问题 **留空占位**（标注 `[待用户评审会议决策后填写]`）。注意：§5和§6均由用户提供，AI不代行。§5来自用户方案选型决策，§6来自用户评审会议认定的遗留问题清单。模板中 §5/§6 无阶段提示注释，这些流程规则由本 skill 控制。
5. 输出到 `{docs_dir}/03-arch-decision-record.md`，frontmatter 添加 `status: PendingDecision`（模板 frontmatter 不含 status 字段，由 skill 注入）。

### 阶段 A 回传

≤15 行：路径 + 候选方案 A/B/C 一句话 + AI 推荐倾向 + 关键风险 + 阻塞条件。

## 阶段 B：决策定稿（subagent 执行）

**前置条件：** 用户已在 Step 0.3.2 明确提供决策结论。

1. 读取 `{docs_dir}/03-arch-decision-record.md`（阶段 A 草稿）。
2. 读取用户决策结论（由主 Session 注入 task 描述）：
   - **选定方案**：方案 A / B / C（或自定义）
   - **决策理由**：用户给出的选择理由
   - **决策者**：拍板人姓名/角色
3. 将用户结论写入 §5 决策结论（选定方案 + 理由 + 决策者）。
4. 读取用户评审会议认定的遗留问题清单（由主 Session 注入 task 描述），写入 §6 决策后遗留问题。表格列结构：`| 遗留项 | 描述 | 负责人 | 解决动作 | 计划关闭时间 | 状态 |`（与模板 arch-decision-record.md §6 一致）。每条遗留项必须包含：描述、负责人、解决动作、计划关闭时间。
   - **⚠️ §6遗留问题必须由用户提供，AI 不代行生成。** AI不得从feasibility条件项或风险自动推演遗留问题。如用户未提供遗留问题清单，§6保留占位标注 `[待用户评审会议后填写]`，status 保持 `PendingDecision`，不允许推进到后续 Step。
5. 更新 frontmatter `status: Accepted`（由 skill 注入，模板不含 status 字段）。
6. 输出到 `{docs_dir}/03-arch-decision-record.md`。

### 阶段 B 回传

≤15 行：路径 + 选定方案 + 决策理由一句话 + 遗留问题数 + status(Accepted)。

## 阶段判定规则

| 阶段 | 触发条件 | status 值 | 产出 |
|------|----------|-----------|------|
| A | Step 0.3.1（requirement+feasibility 就绪） | `PendingDecision` | §1-§3 填充，§5-§6 占位 |
| B | Step 0.3.3（用户提供决策结论 + 遗留问题清单） | `Accepted` | §5 填充（用户决策），§6 填充（用户遗留问题），全文定稿 |

**不允许在阶段 A 直接输出 `status: Accepted` 或自行填写 §5 决策结论。**
**不允许在阶段 B 用户未提供遗留问题清单时输出 `status: Accepted` 或自行填充 §6。**

## 强制规则

- **遗留问题闭环门禁**：§6 每条遗留项必须有负责人、解决动作、计划关闭时间。任一遗留项缺少这三字段 → 阻断 Phase 0→1-9 交接。
- **AI 推荐倾向仅为参考**：§3候选方案对比表的"AI 推荐倾向"列仅供用户决策参考，不是最终结论。

## 单方案例外

只有一个客观可行方案时允许不构造虚假备选，但必须写明其他路径不可行的证据。

**单方案快速路径（简化两阶段为一阶段）**：

当 feasibility 阶段已明确排除其他方案（客观上只有一条可行路径）时，可跳过候选方案对比表，采用简化流程：

1. **阶段 A 简化**：直接呈现唯一方案分析（方案描述 + 工作量 + 优势 + 不可行证据），**不生成候选方案对比表**（§3 标注"单方案场景，无可行备选"）
2. **单次确认**：向用户一次性呈现唯一方案 + 其他路径不可行证据，用户一次确认采纳即可，**无需两阶段暂停**
3. 用户确认采纳后直接定稿 §5（选定方案 + 理由："唯一可行方案，无备选" + 决策者），status 直接设为 `Accepted`

**触发条件**：feasibility.md §6 结论中仅有一个方案标记为 ✅可行 或 ⚠️有条件可行，其余方案均标记为 ❌不可行，且不可行有证据支撑。

**不满足触发条件时**（≥2 个可行方案），仍执行标准两阶段流程。

## 职责边界

本 skill 只产出方案选型决策，不产出 Feature 评审基线（目标/非目标/AC/交付影响），这些由 `ohos-req-feature-baseline` skill 负责。

## NEVER

- **禁止 AI 代行决策**：§5 选定方案、决策理由和决策者由用户提供，AI 不代行（原因：方案选型权归属 SIG 评审会议，AI 推荐倾向仅为参考）
- **禁止 AI 生成遗留问题**：§6 遗留问题由用户评审会议输入，不得从 feasibility 条件项或风险自动推演（原因：遗留问题反映用户认定的开放风险，AI 推演会引入虚构风险项）
- **禁止阶段 A 直接定稿**：不允许在阶段 A 输出 `status: Accepted` 或自行填写 §5（原因：跳过用户决策会导致未评审的方案进入下游）
- **禁止用户未提供遗留问题时填充 §6**：阶段 B 时如用户未提供，§6 保留占位，status 保持 `PendingDecision`（原因：遗留问题未经评审会议认定则不构成闭环）

## 自检

- [ ] status 字段由 skill 注入（PendingDecision→Accepted），非模板填写
- [ ] §5 方案比较来自用户提供，非 AI 推断
- [ ] §6 遗留问题来自评审会议，非 AI 推演
- [ ] 阶段A完成后已暂停等待用户决策
- [ ] 单方案例外仍执行了两阶段流程
- [ ] 每条遗留问题含负责人/解决动作/计划关闭时间

## 错误处理

| 场景 | 行为 |
|------|------|
| 01-02 未就绪 | 提示用户先完成上游 Step 0.1-0.2，列出缺失文档 |
| 用户未提供候选方案 | 追问用户："请提供至少 2 个候选方案用于比较" |
| 用户未做决策（阶段A后） | 保持 status: PendingDecision，追问："请提供评审会议决策结论" |
| 遗留问题未提供 | §6 保留占位符 [待用户评审会议后填写]，不自行填充 |

## 输出

- 路径：`{docs_dir}/03-arch-decision-record.md`
- 阶段 A 回传：路径、候选方案概要、AI 推荐倾向、关键风险、阻塞条件
- 阶段 B 回传：路径、选定方案、决策理由、遗留问题数、status
