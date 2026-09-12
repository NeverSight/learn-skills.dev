---
name: award-review
description: 以 CUMCM 评委四轴和 2026 格式硬规则检查论文，列出致命项与回跳节点。在全文初稿之后、打包之前使用。用户说「自查」「能拿奖吗」「评委视角」时使用。不要用查重百分比代替本检查。
license: MIT
metadata:
  author: cumcm-skills
  version: "0.1.0"
  invocation: model
  graph-node: N12
---

# award-review

检查表：[references/checklist.md](references/checklist.md)。

## 何时使用

必须使用：`voice_checked` 或用户丢来完整稿要审。

禁止使用：只有半页提纲；预测「国一」当娱乐而无检查表。获奖预测若要写，必须附致命项；有致命项则只能写「未达送审合格线」，禁止报奖级。

## 循环

目标：每条检查有 合格 / 问题 / 无法核实 + 位置 + 回跳 skill。

`max_rounds`: 2（第二轮只复核声称已改的红项）

## 步骤

1. 先跑致命项（checklist 第一节）。一项红则 `status` 不得标 reviewed 为完成态——保持 `voice_checked` 并写 failures。
2. 再跑四轴。
3. 输出表：维度 | 结果 | 位置 | 回跳。
4. 不要生成花哨 HTML 作为必须交付；Markdown 表即可。

## 验收

- [ ] 致命项全部判定
- [ ] 每个小问是否作答已勾
- [ ] 摘要数字抽查 ≥3 个
- [ ] 未在有致命项时把 status 写成 reviewed

## 输出

`gate_failures`。全绿：`status=reviewed`。

## 下一跳

表述/结构红 → `paper-write` 或 `academic-voice`。结果/检验红 → `model-validate`。格式/AI 声明红 → `compliance-ai`。全绿 → `compliance-ai`。
