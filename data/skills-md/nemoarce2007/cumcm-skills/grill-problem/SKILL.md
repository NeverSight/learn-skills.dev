---
name: grill-problem
description: 追问直到 CUMCM 赛题理解无歧义：题号、附件、小问目标、不能改的数据口径。在选题后、正式拆题前，或发现队内对题意打架时使用。不要在用户只要改措辞时使用。
license: MIT
metadata:
  author: cumcm-skills
  version: "0.1.0"
  invocation: user
  graph-node: G0
disable-model-invocation: true
---

# grill-problem

只问赛题事实，不问“想拿什么奖”。

## 何时使用

必须使用：尚未锁定题号；附件路径不明；用户对「要输出什么」意见不一。

禁止使用：题目已锁定且用户要建模；把本技能当成论文大纲生成器。

## 循环

目标：下列问题都有书面答案，写入状态后用户回复「锁定」。

`max_rounds`: 8（每轮最多 5 个未决问题，先问阻塞项）

未决清单（有一项空就不能锁定）：

1. 年份与题号
2. 赛题原文路径
3. 附件清单（或确认无附件）
4. 小问个数与各问要交的东西（数/表/方案/图）
5. 竞赛结束时间（用于后面排期，可粗）

## 步骤

1. 先读 `problem/`。能从原文确定的不要问。
2. 只问原文不能确定的。一次一类。
3. 用户说「锁定」后写 `contest.*`，`status=problem_locked`。

## 验收

- [ ] 未决清单全填
- [ ] 没有开始选模型
- [ ] 用户明确锁定，或 `max_rounds` 到了并列出仍缺项（此时不得写 `problem_locked`）

## 输出

`contest.*`；`status=problem_locked`（仅全绿时）。

## 下一跳

`problem-brief`。
