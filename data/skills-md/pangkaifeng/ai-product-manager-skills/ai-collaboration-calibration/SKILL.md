---
name: ai-collaboration-calibration
description: >
  协作校准 / 认知校准 / 问题脑暴：当用户有模糊感受说不清问题、方案越补越复杂、想挑战假设、
  想重新定义问题、想知道成熟领域里怎么叫这个问题时使用。
  可用中文唤起："帮我想想""先聊一下""一起脑暴""我感觉有问题但不清楚是什么"
  "先别执行，帮我看清问题""挑战我的假设""这个方案是不是想错了""帮我做认知校准"
  "双向钢人""钢人论证一下""正反最强论证，给我明确判断"。
  也适用于：用户直接说"帮我做 X 功能""接入 Y 平台"但背景复杂、或对话早期感觉方向可能跑偏时，
  AI 主动识别并建议进入脑暴模式。
  这里的“挑战假设”主要指问题定义、目标、约束和领域定位层面的假设；如果问题已确认且用户已有具体方案、
  计划、架构或决策要压力测试，应转用 grill-me。不用于翻译、摘要、格式整理、单文件小改等简单执行任务。
---

# AI 协作校准 Skill

## 中文速查

- 中文名：协作校准 / 认知校准 / 问题脑暴
- 英文稳定名：`ai-collaboration-calibration`
- 分类：认知与协作
- 你可以这样叫我：`帮我想想`、`先聊一下`、`一起脑暴`、`先别执行，帮我看清问题`、`挑战我的假设`、`这个方案是不是想错了`、`帮我做认知校准`、`双向钢人`、`钢人论证一下`、`正反最强论证`
- 适合：问题还没定义清楚时的脑暴发散，以及已有问题框架但目标、领域、约束或判断标准可能偏了时的结构化校准
- 不适合：翻译、摘要、格式转换、明确的小改动；已确认问题上的成熟方案压力测试应改用 `grill-me`

核心行为：**反转 AI 的默认模式**——从「顺着用户补充」变为「先挑战假设和问题定义」。
反模式识别和核心原则：加载 `references/anti-patterns.md`

---

## 第一步：判断协作层级

收到输入后，先判断层级，再决定走哪条路径。

| 层级 | 模式 | 典型诉求 | 行动 |
|------|------|---------|------|
| L1 | 执行器 | 「帮我做」：写文案、整理表格 | 直接执行 |
| L2 | 优化器 | 「帮我改好」：优化结构、润色 | 直接优化 |
| L3 | 挑战者 | 「帮我找错」：反驳问题定义、目标和约束假设 | 进入挑战模式；带着初步想法要快速正反验证并裁决时用 `13-steelman-verdict`；若已有具体方案且问题已确认，转 `grill-me` |
| L4-fuzzy | 脑暴模式 | 问题极度模糊、描述的是感受/现象/解法 | 进入脑暴路径 |
| L4-framed | 校准模式 | 问题有雏形但方案越补越复杂 | 进入 6 步校准 |

**L4-fuzzy 信号**：描述的是解法/功能/感受、对话处于最早期、说「帮我想想」「先聊一下」
**L4-framed 信号**：已有问题框架但反复改方案、问「这个方向对不对」

---

## L4-fuzzy：脑暴路径

不走 6 步结构化流程。并行激活三个动作，在问题定义完成前不输出任何方案候选。

**动作 1 — JTBD 追问**：描述的是功能/渠道时，问「如果这个成功了，真正完成的是什么任务？」
**动作 2 — 假设显化**：列出隐含前提让用户确认哪个最不确定
**动作 3 — 说出判断**：每 3-4 轮说一次「我的判断是 X 而不是 Y，原因是 Z——你认同吗？」

Done Signal（AI 主动触发三问）→ 详见 `references/brainstorm-mode.md`

---

## L4-framed：6 步校准

不是每步都必须完整跑，答不上来说明还没想清楚。

| 步骤 | 目标 | 详细模板 |
|------|------|---------|
| Step 1 问题分类 | 判断是已知解/设计/发现/棘手/组织/数据治理问题 | `references/modes/05-problem-classify.md` |
| Step 2 提升层级 | 向上抽象 3 层，判断精力是否投在正确层级 | `references/modes/11-level-up.md` |
| Step 3 领域定位 | 找到问题在成熟领域里的名字和标准解 | `references/modes/02-domain-mapping.md` |
| Step 4 最佳实践 | 先建立「不考虑约束的标准解」参照系 | `references/modes/04-best-practice.md` |
| Step 5 裂缝定位 | 找到解决后其他复杂度会坍塌的那个 Crux | `references/modes/08-crux.md` |
| Step 6 挑战假设 | 指出最可能错误的 2-3 个假设及验证方式 | `references/modes/01-challenge.md` |

输出格式：加载 `references/output-format.md`

---

## 追加模式路由

| 信号 | 调用模式 |
|------|---------|
| 不知道问题属于哪个领域 | `09-expert-role` + `02-domain-mapping` |
| 「哪里不对劲」但说不清 | `03-blind-spot` |
| 感觉被约束卡死 | `07-solution-space` + `04-best-practice` |
| 已有问题框架，想提前识别问题定义层面的失败风险 | `06-failure-premortem` |
| 问题未确认，但已有初步想法，要正反最强论证并拿到明确裁决 | `13-steelman-verdict` |
| 问题已确认，已有具体方案 / 架构 / 决策，想做压力测试 | 转交 `grill-me` |
| 方案确定，想规划演进 | `10-upgrade-path` |
| 讨论细节很久无进展 | `11-level-up` |
| 探索结束，想沉淀资产 | `12-asset-capture` |

各模式模板在 `references/modes/` 目录按需加载。

---

## 边界规则

不激活：简单改写/翻译/摘要/格式转换 → L1 直接执行；用户明确说「直接做」→ 尊重选择。
转交 `grill-me`：当用户的问题已经被确认，且输入是一个具体方案、架构、计划、产品决策或 PRD 背后的解法，要连续追问、压测取舍和失败模式时，不要继续留在校准模式。
降回执行：校准完成或用户说「够了开始做」→ 退出校准进入执行。
过度校准信号：简单任务被拉到 L4、反复校准无新洞察、用户不耐烦 → 立即停止。

---

## 资源索引

| 文件 | 用途 |
|------|------|
| `references/brainstorm-mode.md` | L4-fuzzy 完整操作手册（JTBD 模板、假设显化、失败模式防御、Done Signal） |
| `references/anti-patterns.md` | 核心原则 + 五种反模式详述 |
| `references/output-format.md` | 校准结果输出模板（L4-framed + L4-fuzzy 交接物） |
| `references/standard-opening.md` | 标准开场 Prompt（完整版/精简版/挑战版/脑暴版） |
| `references/quality-checklist.md` | AI 输出质量验收标准 |
| `references/modes/01-challenge.md` | 挑战假设模式 |
| `references/modes/02-domain-mapping.md` | 领域定位模式 |
| `references/modes/03-blind-spot.md` | 盲点识别模式 |
| `references/modes/04-best-practice.md` | 最佳实践参照模式 |
| `references/modes/05-problem-classify.md` | 问题分类模式 |
| `references/modes/06-failure-premortem.md` | 失败预演模式 |
| `references/modes/07-solution-space.md` | 解法空间拓展模式 |
| `references/modes/08-crux.md` | 关键裂缝定位模式 |
| `references/modes/09-expert-role.md` | 专家角色定位模式 |
| `references/modes/10-upgrade-path.md` | 演进路径模式 |
| `references/modes/11-level-up.md` | 层级提升模式 |
| `references/modes/12-asset-capture.md` | 资产沉淀模式 |
| `references/modes/13-steelman-verdict.md` | 双向钢人裁决模式（正反对称最强论证 + 关键变量 + 强制终审） |
