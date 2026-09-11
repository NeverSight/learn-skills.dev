---
name: writing-modeling-abstracts
description: Use when drafting, revising, condensing, or auditing a mathematical modeling contest abstract, 摘要, CUMCM 国赛摘要, MCM/ICM Summary Sheet, keywords, or one-page executive summary after model results are available.
---

# 数学建模竞赛摘要写作

## 核心原则

把摘要写成可独立核验的微型论文：覆盖问题、方法、关键结果和适用边界，但不依赖正文。所有数字和比较必须逐项追溯到冻结结果；建模者决定主打结果与贡献表述，AI 只负责证据组织和文字压缩。

开始前完整读取 [references/abstract-writing-guide.md](references/abstract-writing-guide.md)。

## 模式

- **draft**：从已验证工件生成摘要。
- **revise**：保留原意和证据，重组、压缩并校准主张。
- **audit**：不改稿，逐项给出 PASS/WARN/FAIL 和修复建议。

## 输入门禁

1. 读取当年官方规则和所用模板；二者优先于经验字数。
2. 读取全部子问题的 solution package、`frozen_numbers.json`、稳健性报告和决策日志。不得从零散输出或旧稿猜数字。
3. 查找建模者提供的 `key_result_claim` 与 `contribution_claim`。缺失时只生成结构草稿，并原样保留：
   - `[MODELER INPUT NEEDED: which frozen result(s) should lead the abstract, and why?]`
   - `[MODELER INPUT NEEDED: what contribution should the paper claim, in the modeler's own words?]`
4. 最终稿所需工件不全时，列出缺口并停止；不要用常识补齐结果、创新、最优性或推广范围。

## 工作流

1. 建立内部证据矩阵：`子问题 → 转化/目标 → 方法 → 冻结结果 → 基线/稳健性 → 来源`。
2. 按“问题与总体策略 → 各问方法和结果 → 稳健性/边界与价值 → 关键词”成稿。每个子问题至少出现“做什么、怎么做、得到什么”；无结果的目标不得包装成已实现贡献。
3. 只使用冻结文件中已有的数值与舍入。新计算的提升率先回写并重新冻结，不能直接写入摘要。
4. 删除正文交叉引用、引文、过程叙述、主观修饰和无证据的“最优、显著、普适、创新”。公式仅在不可替代且能自包含时保留。
5. 实施摘要强调合同：单段摘要使用 **3-5 组**语义加粗，合计覆盖核心研究方法、关键模型名称、核心量化指标、核心结论数值和末尾关键词。一组可合并紧密相连的“方法+模型”或“指标+数值”，例如 `**熵权-TOPSIS 综合评价模型**`、`**RMSE = 0.128**`。
   - 加粗只包围关键词、模型名、指标或数值，不得包围完整句子。
   - 关键词行只加粗实际关键词词组，不把整行或“关键词：”标签计入语义加粗组。
   - 沿用项目引擎语法：LaTeX 用 `\textbf{...}`，Typst 用 `*...*`，Markdown 用 `**...**`。
6. 按参考指南审计覆盖率、溯源、主张强度、独立性、长度、关键词和加粗范围。

## 输出合同

`draft` / `revise` 生成：

- `paper/sections/abstract.tex`、`.typ` 或 `.md`，沿用项目引擎；
- `paper/audits/abstract_evidence_audit.md`，记录规则来源、逐问覆盖、每个数值的来源，以及加粗组数、五类语义覆盖和是否误加粗完整句子的 PASS/WARN/FAIL。

`audit` 只写或更新 `paper/audits/abstract_evidence_audit.md`，不得改动摘要；在审计报告中给出逐项修复建议。

仅当官方格式已核对、所有子问题已覆盖、所有数字已冻结、两个人工判断已填写、无 sentinel 且摘要可独立阅读时，状态才是 `READY`。审计材料不得进入提交正文。

## 快速检查

| 检查项 | 通过标准 |
|---|---|
| 覆盖 | 每问均有任务、方法、结果 |
| 证据 | 每个数字和比较可定位到冻结来源 |
| 主张 | 强度不超过基线、稳健性和证明支持 |
| 独立 | 无“见图/表/式/附录/正文” |
| 格式 | 当年模板优先，摘要页不溢出 |
| 关键词 | 无官方另行规定时用 3-5 个，覆盖对象、方法与任务/指标 |
| 强调 | 单段 3-5 组语义加粗，覆盖方法、模型、指标、结论数值和末尾关键词；无完整句加粗 |
