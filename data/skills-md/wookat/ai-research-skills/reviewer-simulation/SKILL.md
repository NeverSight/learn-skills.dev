---
name: reviewer-simulation
description: Simulate a full peer-review round on a finished paper draft with multiple reviewer personas (harsh Reviewer 2, domain expert, Area Chair), producing venue-format mock reviews, a weakness list ranked by rejection risk, and a submit/revise recommendation. Use when the user asks to review a draft, predict reviewer reactions, or decide whether a paper is ready for submission. Do not use on ideas without a draft (use idea-critic).
---

# Reviewer Simulation（投稿前模拟评审）

⚠ 本 skill 属 verdict 类评审，必须遵守
`../cross-model-review` 协议：在零上下文新线程、优先跨模型的条件下出具评审，
只读被评对象，禁止在产生/修改该对象的同一上下文里自评（否则会把真实 3/10 刷成虚假 8/10）。
无法换线程/换模型时，按 `shared-references/reviewer-adapter.md` 降级并在结论标注
self-review 可能虚高。

对完整论文草稿做一轮真实格式的模拟评审。输入：论文草稿 + claim-evidence map + 目标会议。

## 评审 persona（各自独立成篇，禁止互相妥协）

1. **Reviewer 2（苛刻型）**：默认拒稿立场。专攻：novelty 不足、baseline 不新/不强、
   实验设定利己、消融缺失、主张超出证据。必须给出 ≥4 条具体 weakness，每条指明章节/表号。
2. **领域专家**：核查与最接近工作的对比是否公平、是否漏了必比的 SOTA、
   评测协议是否符合领域惯例（读取 `domains/<领域>.md` 的评测协议节逐条对照）、
   数字是否可信（提升幅度 vs 方差）。
3. **粗读审稿人**：只看 abstract、图表、贡献列表和结论（模拟真实的 15 分钟审稿）。
   报告第一印象：故事能否只靠图表被理解？Figure 1 是否自明？
4. **Area Chair**：综合三份意见，判断 borderline 争议点，给出 meta-review。

## 每份评审的格式（按目标会议，默认 NeurIPS/ICLR 格式）

```
Summary / Strengths / Weaknesses（按严重度排序，每条含章节定位）
Questions（作者必须在 rebuttal 回答的）
Soundness / Presentation / Contribution: 1-4
Rating: 1-10 + Confidence: 1-5
改分条件：若 rebuttal 提供 <X>，愿意从 <a> 改到 <b>
```

## 参考文件

- `references/paper-review.md` — 五维自审问题清单与 claim-evidence 检查法（用于 persona 2/3 的核查项）
- `references/reviewer-defense.md` — 常见审稿攻击面与预防清单（用于 weakness 分类）

## 汇总输出（mock_reviews.md）

1. 四份评审全文
2. **合并 weakness 清单**：按"拒稿风险 × 修复成本"二维排序，分三类：
   - 投稿前必须修复（高风险低成本：缺消融、措辞超卖、图表问题）
   - 建议修复（高风险高成本：补 baseline、补数据集——给出预估工作量）
   - rebuttal 阶段可辩护（低风险：口味类意见，预写辩护要点）
3. 预测评分分布与录用概率的定性判断
4. 决策卡 #4：投稿 / 修复后再审 / 降级投稿目标，附推荐

## 纪律

- 用真实审稿标准，不因草稿出自本流水线而放水；模拟评审的价值与其严苛度成正比。
- 每条 weakness 必须具体到可执行（"实验不够"不合格；"缺少与 X 在数据集 Y 上的对比，
  因为 X 是该设定下的公认 SOTA"合格）。
- 发现主张-证据不匹配时按最高严重度上报，这是真实评审中最致命的一类问题。

**本整合包契约：**产物写
`research_run/<课题slug>/stage6_review/mock_reviews.md`；脱离
`research-pipeline` 单独调用时，退当前工作目录。
