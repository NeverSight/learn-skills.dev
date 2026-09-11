---
name: model-build
description: 按已锁定的主模型写 CUMCM 公式推导、变量对应与局限。在假设与符号锁定后、写求解代码前使用。用户说「建模」「推公式」时使用。不要从模板粘贴与本题无关的公式堆。
license: MIT
metadata:
  author: cumcm-skills
  version: "0.1.0"
  invocation: model
  graph-node: N6
---

# model-build

## 何时使用

必须使用：`assumptions_locked`；用户要推导。

禁止使用：符号未锁；用散文代替公式却声称“已建立模型”。

## 循环

目标：每问主模型有：原理（贴题）、公式链、编号、局限+拟用检验。

`max_rounds`: 4

## 步骤

1. 按小问写。顺序：场景抽象 → 符号引用 → 公式 → 求解思路（算法名即可，代码留给 compute-impl）。
2. 公式必须能指回假设。禁止“由上易得”跨过关键等式。
3. 公式数量服务推导，不凑 10 条。多余定义式删掉。
4. 写清与 baseline 的差异（一句）。
5. 局限必须可被 `model-validate` 设计实验。

产出放 `paper/fragments/q<n>-model.md`，不要直接生成 30 页 Word。

## 验收

- [ ] 每个主模型公式编号连续且符号与状态表一致
- [ ] 决策变量（优化题）或状态方程（机理题）或指标公式（评价题）存在
- [ ] 有局限，且不是“计算机性能有限”这类空句
- [ ] 未引入状态里没有的符号

## 输出

`problems[].model` 可补 `innovation` 说明；不改 type。`status=model_built`。

## 下一跳

`compute-impl`。
