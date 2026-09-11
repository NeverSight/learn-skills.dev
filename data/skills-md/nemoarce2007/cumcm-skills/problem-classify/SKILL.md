---
name: problem-classify
description: 给每个 CUMCM 小问唯一题型 id（optimize/evaluate/predict/mechanism/stat/network/hybrid）。在拆题完成后、选型之前使用。用户说「这是什么题」「评价还是优化」时使用。
license: MIT
metadata:
  author: cumcm-skills
  version: "0.1.0"
  invocation: model
  graph-node: N2
---

# problem-classify

判定规则只认 [CONTEXT.md](../../CONTEXT.md) 题型表。

## 何时使用

必须使用：`problems[]` 已有 goal/outputs；用户问类型。

禁止使用：尚未拆题；为了用某个模型而反向贴类型。

## 循环

目标：每问一个 type + 一句判定依据（引用题面词语）。

`max_rounds`: 2

## 步骤

1. 按 CONTEXT 表从上到下匹配。先看有没有决策变量与最优词。
2. hybrid 仅当同一小问必须串联两类；写下拆解顺序。
3. 不要因为往年“A 题是机理”就标 mechanism。

## 验收

- [ ] 每问恰好一个 type
- [ ] 依据中含题面原词
- [ ] hybrid 带拆解，否则不得使用 hybrid

## 输出

`problems[].type`。`status=classified`。

## 下一跳

`model-select`。
