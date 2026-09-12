---
name: model-select
description: 为每个 CUMCM 小问选定基准模型、主模型与对照，并写 why_not。在题型已分类、用户说「选模型」「用不用机器学习」时使用。不要在数据未看且题面依赖附件结构时锁死黑箱模型。
license: MIT
metadata:
  author: cumcm-skills
  version: "0.1.0"
  invocation: model
  graph-node: N3
---

# model-select

目录见 [references/catalog.md](references/catalog.md)。创新定义见 CONTEXT.md。

## 何时使用

必须使用：已 `classified`；用户要选型或要“冲创新”。

禁止使用：未分类；用“深度学习更高级”代替 why_not。

## 循环

目标：每问 `baseline`、`primary`、至少一条 `why_not`；创新若宣称则属于三类之一。

`max_rounds`: 3

## 步骤

1. 按题型打开 catalog 对应节，先定 baseline（该节「稳妥」列）。
2. primary 必须能解释题面约束。数据很少时禁止以深度网络作 primary。
3. 对照模型用于后文表格，不是装饰。
4. 创新可选。没有创新可以拿稳妥方案，但不得假装有创新。
5. 规划类用 catalog 口诀：能小数且线性 → LP；必须整数 → IP；0/1 选择 → 0-1；非线性项 → NLP；多冲突目标 → 多目标；离散排列 → 组合优化。

## 验收

- [ ] 每问有 baseline 与 primary 且名称具体（禁止只写「智能算法」）
- [ ] why_not 至少排除一个同学可能随手用的模型并说明本题不适合的原因
- [ ] 未把评价题的 AHP 无数据场景硬换成需大样本的黑箱

## 输出

`problems[].model`。`status=model_selected`。

## 下一跳

`data-prep`。无数据且不需要外部数据时，data-prep 应快速写「无需预处理」再走假设。
