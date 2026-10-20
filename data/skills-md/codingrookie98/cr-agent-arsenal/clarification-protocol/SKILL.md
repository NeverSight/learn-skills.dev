---
name: clarification-protocol
description: Use when clarifying requirements with a user before planning or coding — sequencing which questions to ask (dependency strength × implementation impact), aligning terminology before eliciting scope, keeping a decision ledger (decided items / excluded boundaries / default assumptions), running the three-item convergence self-check (goals / boundaries / contradictions), and escalating when the question budget is exhausted. Triggers on ambiguous or macro-level goals, multi-round Q&A, decisions being re-opened under a new phrasing, and the choice between asking the user versus registering an explicit default assumption.
license: MIT
---

# 澄清规程 (Clarification Protocol)

## 概述 (Overview)

需求澄清的失控只有两种形态：**问得太少**——把未确认的假设当结论落地；**问得太多**——用穷尽边界替代收敛，把用户变成问答机器。

本规程把澄清变成一个有**前置项、有分级、有台账、有预算、有出口**的收敛过程。

> **SSOT 边界**：全局提示词只保留一行指针以维持每轮在场；澄清与收敛的完整规程以本技能为准，不在全局层复制细则。

---

## 1. 术语先行 (Terminology First) —— 全局前置项

- 先逐一定义**核心术语、范围与易歧义处**，登记至需求确认文档（RFC）的术语表段落或计划文件，再用统一术语澄清需求与边界。
- 术语问题属**全局前置项**，豁免下面的「依赖强度 × 实现影响」分级——**不得**因判定为局部低影响而转为默认假设。
- 范围以「易产生歧义」为界，**禁止扩张为全量词表**。
- **次序门禁**：术语未对齐，不进入需求与边界澄清。

---

## 2. 提问排序 (Question Sequencing)

- 澄清性提问以「**依赖强度 × 实现影响**」排序。
- **HIGH**（影响实现）进入本轮问题清单。
- **LOW**（仅影响实现细节）直转**默认假设**并登记，不占用用户注意力。
- 需要用户决策时，优先给出 2–3 个具备可行性的方案（优缺点对比 + 推荐理由），引导用户做选择题而非开放式提问。

---

## 3. 决策台账 (Decision Ledger)

已决项、已排除边界与默认假设，**即时**登记于计划文件或检查点，禁止只留在对话里：

| 类别 | 登记内容 | 必须写明 |
|---|---|---|
| 已决项 | 结论本身 | 出处（用户裁决 / 证据） |
| 已排除边界 | 被排除的方案或范围 | **排除依据** |
| 默认假设 | 未提问即采用的取值 | 影响级别与可否决性 |

- **去重纪律**：禁止换一种说法重开已被排除的边界——**重复提问即违规**。
- **提前收敛**时必须登记被判定为低影响而转为默认假设的分支；未登记即视为未收敛。

---

## 4. 提问收敛律与三项收敛自检 (Convergence Rule & Self-Check)

每个里程碑（默认：每轮提问结束）执行一次**不带新问题**的自检，只回答三项：

1. 核心业务目标与流程是否仍有未明确？
2. 关键边界与异常情况是否仍有未确认？
3. 已决项之间是否存在相互矛盾的描述？

- **三项皆否定（无新增信息增量）即收敛**：闭合主干、把剩余边界登记为显式默认假设并输出需求确认文档；**不以穷尽问题为出口**。
- **任一为是则继续**，且下一轮问题必须落在该项上。
- 不得用「没问题了」自证收敛——收敛必须有上表台账作为证据。

---

## 5. 熔断预算与升级 (Circuit Breakers & Escalation)

| 层级 | 预算 | 触顶动作 |
|---|---|---|
| 错误层 | 同一错误连续尝试 3 次 | STOP → RECORD；Heavy Track 经**证据门控**可有限重入（≤2 轮 × ≤2 次），其余通道直接 ASK & ESCALATE |
| 审查层 | Delta Re-Loop ≤ 5 轮 | 停止追加轮次，携既有证据上报，不靠加轮次求安心 |
| 提问层 | 本节 | 预算耗尽仍不收敛 → **升级人类裁决** |

重入门控四条判据（新假设 / 新外部证据 / 非措辞改写 / 预算未耗尽）与成本上限 `min(任务总预算 × 25%, 剩余预算 ÷ 3)` 见 `goal-loop` 技能的 failure-recovery-protocol。

升级时向用户客观陈述四项：现状、已验证信息、当前瓶颈、需要裁决的具体分叉。

---

## 6. 显式化思考 (Explicit Reasoning)

在执行关键架构决策、复杂重构或多步骤任务前，在输出中用思考块梳理推演（约束 → 候选 → 取舍 → 结论），确保逻辑自洽后再落笔。

---

## 何时使用 / 何时不用

**使用**：目标宏观或含糊；存在多种技术路径；多轮问答中；已决项被换一种说法重开；需要在「问用户」与「登记默认假设」之间取舍；澄清轮次有失控迹象。

**不用**：单文件微调、指令明确的直接执行、只读检索类问答——直接干活即可。

---

## 交付物与走查入口 (Surface & Entry Points)

本节是规程正文的机械入口。规程只有本文件一份；下列文件是它的**展开、骨架与校验器**，不引入新政策。

- **展开**：[references/decision-ledger.md](references/decision-ledger.md) 把 §3 的台账纪律细化为三类登记的必填字段、去重判定式与低影响分支转默认假设的判据；[references/convergence-checklist.md](references/convergence-checklist.md) 把 §4 的三项自检细化为逐问判定标准与「不算收敛」的反例对照。
- **骨架**：[templates/decision-ledger-template.md](templates/decision-ledger-template.md) 可直接落进计划文件；[templates/requirement-confirmation-template.md](templates/requirement-confirmation-template.md) 是需求确认文档骨架（术语表 / 已决项 / 已排除边界 / 默认假设 / 收敛结论 / 待裁决分叉）。
- **校验**：[scripts/check-decision-ledger.py](scripts/check-decision-ledger.py) 机械校验台账结构（离线、只读；退出码 0 合规 / 1 不合规 / 2 用法错误；POSIX 下旧 `.sh` 兼容壳仍可用），§4 自检前先跑一次：`python3 scripts/check-decision-ledger.py <台账文件>`。
- **回归**：[tests/test_clarification_protocol_contract.py](tests/test_clarification_protocol_contract.py) 守护上述交付面与硬约束，运行 `python3 -m pytest skills/clarification-protocol/tests -q`。

