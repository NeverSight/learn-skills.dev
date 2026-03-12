---
name: claim-ledger
description: 将研究与写作中的主张转成“Claim-Evidence-Boundary”可核验账本。用于在产出前强制补齐证据、反证、边界与可发布性判断，防止无依据断言并提升复用性。
---

# Claim Ledger

## 何时使用

当用户出现以下意图时使用本技能：

- “先做研究框架/证据链，再写内容”
- “判断某观点是否可发、是否站得住”
- “把资料堆整理成可发布结论”
- “让 AI 先出 Ledger 再出线程/长文”

## 核心定义

Claim Ledger 把每条观点拆成三部分：

- `Claim`：要让读者相信的主张
- `Evidence`：支持该主张的证据
- `Boundary`：成立条件与失效条件

目标：让每个结论都可追溯、可反驳、可复核。

## 最小字段（必填 9 项）

每条 Claim 一行，必须包含：

1. `Claim ID`：`C01/C02/...`
2. `Claim`：一句可检验陈述
3. `Type`：`事实/解释/预测/建议`
4. `Confidence`：`高/中/低`
5. `Evidence`：`E01,E02...`（至少 2 条）
6. `Source Grade`：`S/A/B/⚠️`
7. `Counter`：至少 1 条反证/反例；无则写“未找到，风险=高”
8. `Boundary`：成立条件 + 失效条件
9. `Publishability`：`可发/需改写/不可发`

## Evidence Card 规范

每条证据必须是可复核卡片，而非泛化描述。字段：

- `Source`：标题 + 作者/机构 + 日期
- `Link`：URL 或文档定位
- `Quote/Data`：关键原话或数字
- `Supports`：支持 Claim 的哪一部分
- `Reliability`：`S/A/B/⚠️` + 评级理由
- `Freshness`：`是/否`（是否过时）

经验规则：

- 事实型 Claim：至少 1 条 `S` 或 `A`
- 解释型 Claim：至少 2 条跨来源交叉
- 预测/建议型 Claim：必须有历史对比或失败条件，否则降为低置信度

## 六步流程（从资料堆到可发布）

1. 先写 5 条候选 Claim（先定义要证明什么）
2. 给每条 Claim 标注类型（事实/解释/预测/建议）
3. 每条补 2-4 条证据（优先一手源）
4. 强制补反证/反例（没有也要显式记录）
5. 写边界（成立条件与失效条件）
6. 打置信度和可发布性（必要时降调措辞）

## 质量闸门（必须执行）

以下任一不满足，则禁止进入内容生成：

- 任一 Claim 证据少于 2 条
- 任一 Claim 缺少 Counter
- 任一 Claim 缺少 Boundary
- `预测/建议` Claim 无失败条件

处理规则：

- 证据不足：降级为“猜测（低置信度）”
- 语气要求：不得使用确定性措辞

## 与内容生产的映射

### 线程映射（推荐）

- `3 个 Claim × 4 条推 = 12 条线程`
- 每组 4 条顺序：
  1. Claim
  2. Evidence
  3. Boundary
  4. Action

### 长文映射（推荐）

每个 Claim 作为一节：

- 结论 -> 证据 -> 反方风险 -> 边界 -> 小结/清单

## 默认输出格式

1. `Claim Ledger` 表（至少 3 条 Claim）
2. `Evidence Cards`（与 Ledger 的 E# 对齐）
3. `Gate Check`（逐条列出通过/失败项）
4. 若 Gate 全通过，才生成目标内容（线程/长文/脚本）

## 执行指令模板

```text
先输出 Claim Ledger（至少 3 条 Claim，每条 >=2 条证据 + >=1 条反证 + 边界）。
未满足质量闸门前，不允许生成正文。
若证据不足，必须降级为“猜测（低置信度）”，并避免确定性语气。
```

## 参考模板与示例

需要直接套用表格和卡片时，读取：

- `references/templates.md`

需要自动校验 Ledger 质量闸门时，运行：

- `scripts/validate_ledger.py --file <ledger.md>`
