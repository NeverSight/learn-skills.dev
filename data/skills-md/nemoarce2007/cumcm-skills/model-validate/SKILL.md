---
name: model-validate
description: 对已求解的 CUMCM 模型做误差、灵敏度、稳健性三类检验并量化。在代码跑出结果之后、写结论之前使用。用户说「灵敏度」「三大检验」「稳健性」时使用。
license: MIT
metadata:
  author: cumcm-skills
  version: "0.1.0"
  invocation: model
  graph-node: N8
---

# model-validate

细则：[references/three-tests.md](references/three-tests.md)。

## 何时使用

必须使用：`status=solved`；用户要检验。

禁止使用：没有 `results/`；用“模型较为稳定”代替数字。

## 循环

目标：三类检验都有：方法、指标、图或表路径、一句话结论（含数字）。

`max_rounds`: 4

失败：误差显示实现错误 → 回 `compute-impl`。假设被推翻 → 回 `model-build` 或 `assumption-set`。

## 步骤

1. 误差：按题型选指标（预测 RMSE/MAE/MAPE/R²；优化相对规则策略改进率与约束违反量；评价排序一致性）。必须有对照。
2. 灵敏度：对 1–3 个核心参数做至少 ±10%（或题面合理幅度）。报告输出相对变化。有余力再做简易全局（一次一因子以上）。
3. 稳健性：换算法或子样本或极端情景之一，看结论方向是否变。与灵敏度不同：灵敏度动参数，稳健性动结构/样本/情景。
4. 代码放 `scripts/run_validation.py`，图进 `results/figures/`。

## 验收

- [ ] 三类都有可引用数字
- [ ] 结论区分「数据支持」与「可能解释」
- [ ] 未用编造的检验表
- [ ] 若核心结论在合理扰动下翻转，gate_failures 必须记录，不得标 validated

## 输出

`problems[].validation`。全绿则 `status=validated`。

## 下一跳

绿 → `chart-style`。实现红 → `compute-impl`。结构红 → `model-build`。
