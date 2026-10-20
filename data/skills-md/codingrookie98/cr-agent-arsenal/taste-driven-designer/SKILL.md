---
name: taste-driven-designer
description: Use when the user wants to design or redesign any UI/UX artifact — landing pages, web apps, mobile interfaces, game UIs, or dashboards — and expects distinctive, tasteful results instead of generic AI slop. Also use when asked to give a design a personality or art direction, make it look premium/unique/not AI-generated, critique an existing interface, or give a frontend build direction. Triggers on landing page, hero section, design language, moodboard, art direction, UI polish, taste.
license: MIT
---

# taste-driven-designer 品味驱动设计

## 概述

将 AI 从"统计平庸的默认设计器"升级为"世界级设计师"的三阶段流程技能。理论基准：《How to Turn Your AI into a World-Class Designer》（Anshu Chimala 的 AI 双钻模型，前 Apple AI 原型团队 12 年负责人；仓库归档路径 docs/reference/articles/how-to-turn-your-ai-into-a-world-class-designer.md）。

**黄金公式**：

$$\text{World-Class AI Design} = \text{外部随机种子} + \text{独立 Critic 闭环} + \text{多模态增强} + \text{残酷减法}$$

本文件是**路由层**：只声明触发条件、铁律与阶段指针，阶段细则见 `references/`。

---

## 何时使用 / 何时不用

**使用**（满足任一）：
- 用户要求设计/重设计落地页、Web 应用、移动界面、游戏 UI、仪表盘等界面产物；
- 用户明确要求"有设计感 / 有品味 / 不像 AI 生成的 / 独特一点 / 高级感 / 给出艺术方向"；
- 既有界面需要"设计批评 / 视觉 vibe-check / 打磨"；
- 前端构建需要超出纯功能布局的创意方向。

**不用**：纯功能改动且无视觉诉求、后端/数据逻辑任务、用户明确要求"就按默认模板来"。

---

## 铁律 (Invariants)

1. **随机性必须来自模型外部**：任何设计开工前先跑种子字符串规程（`scripts/generate-seed.py`）；"随机一点 / 独特一点"等口头指令不算数——模型只会预测"听起来随机"的 Token。
2. **Critic 分离纪律**：Critic 每次以**全新上下文** + **固定模板** + **只看产物**介入——默认只收当前产物（截图，无则降级）；**盲比模式另附去标识、随机左右的上一版**。任何模式下都不得携带实现代码、迭代记录与前次批评全文。
3. **三信号收敛门禁**：D2 完成必须同时满足 —— **A 结构清单**（7 AI Tells + 层级/间距/状态/文案审计，逐项可核验）+ **B 盲比改进**（上一版 vs 当前版强制选择：哪个更好 + 胜出维度，**不输出分数**）+ **C 人类签收**。结构清单扩展项见 [critic-loop-protocol.md](references/critic-loop-protocol.md) Gate A；**产物级验收**（响应式与移动端、交互状态矩阵、无障碍键盘路径、浏览器覆盖、性能预算）以 `frontend-qa-gate` 技能为主路径，其验收基线为内联最小副本，来源版本见该技能的 acceptance-matrix（A 方案：Gate A 为验收基线单一来源）。绝对分数（如 x/10）**仅作遥测**，任何时候不得作为通过判据；**门禁未达 ≠ 交付完成**，如实报 blocked 待裁。
4. **预算有上限**：先跑 1~2 轮验证可收敛性；全流程迭代上限 5 轮，超限熔断向用户汇报。
5. **减法优先**：Deliver 阶段先删除后增补——删不掉价值说明的元素（装饰渐变/多余卡片/装饰标签）一律移除；AI Tells 审计必须逐项过清单（`references/ai-tells-audit.md`）。
6. **文案是占位符**：AI 生成的文案一律视为排版 Lorem ipsum，交付前必须重写为具体、克制、口语化的人类语言（黑名单词表见 `references/ai-tells-audit.md`）。
7. **能力门控**：截图/图像/视频能力按宿主实际可用性启用；缺截图则走降级评审，禁止假装看见了截图。
8. **人类是创意总监**：方向选择、品味标杆与取舍裁决归用户；智能体负责提供速度、广度与执行。
9. **参考是锚点不是拷贝**：moodboard/参考图只用于校准质量基线，禁止照抄。
10. **事实即刻落盘**：方向决策与删除清单写入设计简报，避免上下文腐化。

---

## 阶段路由 (Phase Routing)

| 阶段 | 目标 | 核心技法 | 产物 / 指针 |
|:---:|---|---|---|
| **D1 Discover** | 打散统计平庸，发散探索 | 种子字符串注入随机性 + 雄心跨界 Prompt | 设计简报（`templates/design-brief-template.md`）；细则见 [discover-phase.md](references/discover-phase.md) |
| **D2 Define** | 注入品味与个性，逼近世界级执行水准 | 独立 Critic 闭环（盲比 A/B + 参考排序）+ （可选）图像/视频增强 + **每轮内嵌产物自检**（状态矩阵与响应式抽查，分钟级，不派发 Critic） | 评审账本 + 结构清单 + 自检记录；细则见 [critic-loop-protocol.md](references/critic-loop-protocol.md)、[multimodal-enrichment.md](references/multimodal-enrichment.md) |
| **D3 Deliver** | 收敛与减法，剔除 AI 痕迹 | 残酷减法 + AI Tells 审计 + 文案重写 | AI Tells 审计清单 + 删除记录；细则见 [ai-tells-audit.md](references/ai-tells-audit.md) |

**阶段纪律**：D1 未产出多方向简报不得进入 D2；D2 未同时满足「结构清单全过 + 盲比有改进（或判定已收敛）+ 人类签收」不得进入 D3；D3 审计未逐项过清单不得宣称交付。

---

## 快速流程清单 (Quick Checklist)

```text
D1  ┌ generate-seed.py 生成种子 → 提取子模式 → 定义创意方向（配色/布局/字体/质感）
    ├ 多方向并行：产出 2~4 个 Brief（必要时派发子智能体分别执行）
    └ 与用户对齐方向，选定 1 个（兼修时取 2 个）
D2  ┌ 实现初版 → 捕获产物（截图 / 降级文本）→ 附版本 nonce
    ├ 派发 Critic（全新上下文 + 固定模板 + 设计意图与已决原则；必须回执 nonce）
    ├ 盲比：上一版 vs 当前版强制选择（不输出分数）→ 有改进则记账续跑
    ├ 结构清单逐项核验（7 AI Tells + 层级/间距/状态/文案 + 状态矩阵 / 视口抽查 / 无障碍基线 / 证据三态）→ 全过才谈放行
    └ 人类签收 → 进入 D3；分数仅记遥测（可选增强见 multimodal-enrichment.md）
D3  ┌ 逐项过 AI Tells 审计清单（7 反模式 + 减法 + 文案黑名单）
    ├ 删除无价值元素 → 重写全部文案 → 人工复核方向一致
    ├ 交付说明：方向来源、盲比结论与签收、删除了什么，并标注证据三态（已实现 / 已运行验证 / 未验证）
    └ 产物级完整验收（响应式 / 状态 / 无障碍 / 浏览器 / 性能）由 `frontend-qa-gate` 独立执行，本技能不替代该验收
```

---

## 降级与预算 (Fallbacks & Budgets)

| 场景 | 处置 |
|---|---|
| 宿主无截图能力 | 走降级评审：向 Critic 提供结构化产物摘要（语义树 + 视觉参数 + 关键区段），见 [critic-loop-protocol.md](references/critic-loop-protocol.md) §8 |
| 宿主无图像/视频生成 | 跳过增强层，用代码级质感（着色器/CSS 纹理）替代，见 [multimodal-enrichment.md](references/multimodal-enrichment.md) §4 门控矩阵 |
| 盲比连续 2 轮无改进 | 熔断：停止换皮式迭代，向用户展示盲比记录与已尝试修复，请求方向裁决 |
| 鉴别力自检失败（输入实质不同、输出逐字相同） | 判定 Critic 失效：立即停止循环并升级人工，不再消耗轮次 |
| 连续 2 轮评审作废（回执不符 / 空白产物） | 停止循环：排查产物管线（截图与回执链路）并升级人工；作废不计预算，但连续作废即故障信号 |
| Critic 建议与已决原则冲突 | 原则优先 + 记入台账，交人类裁决；禁止静默反转（防乒乓） |
| 评审账本达 5 轮上限 | 熔断：汇报当前最佳状态与差距清单，请用户决定是否继续 |
| 门禁未达（清单未全过 / 无改进 / 未签收） | 如实报 blocked 待裁，**不得宣称交付完成** |
| 产物级验收未通过（`frontend-qa-gate` 存在失败或未验证断言） | 视为交付未完成：按该技能的回流路由分流后再谈交付 |

---

## 辅助脚本（可选）

`scripts/generate-seed.py` 为 Discover 阶段注入外部随机性（String Seed of Thought）：

```bash
SKILL_DIR="<taste-driven-designer 技能实际所在目录>"
python3 "$SKILL_DIR/scripts/generate-seed.py"            # 64 位真随机种子
python3 "$SKILL_DIR/scripts/generate-seed.py" -l 128 -c 3  # 3 条种子并行探索
python3 "$SKILL_DIR/scripts/generate-seed.py" -s team-2026 -l 48  # 团队可复现
```

旧 `bash "$SKILL_DIR/scripts/generate-seed.sh"` 调用仍可用（POSIX 兼容壳；Windows 原生环境用 `python` 调用同目录 `.py`）。

完整施工步骤与灵感提取 Prompt 见 [seed-string-procedure.md](templates/seed-string-procedure.md)。

---

## 参考导航

- [discover-phase.md](references/discover-phase.md) — D1 种子字符串规程与雄心 Prompt 三步入炉法
- [critic-loop-protocol.md](references/critic-loop-protocol.md) — D2 三信号门禁、盲比与排序协议、版本回执、鉴别力自检与评审账本
- [ai-tells-audit.md](references/ai-tells-audit.md) — D3 7 大反模式清单、减法规则与文案黑名单
- [multimodal-enrichment.md](references/multimodal-enrichment.md) — 可选增强层与能力门控矩阵
- 模板套件：`templates/` 下设计简报、Critic 固定提示词、种子施工三步模板
