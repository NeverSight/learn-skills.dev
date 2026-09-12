---
name: problem-brief
description: 把 CUMCM 赛题拆成小问表：背景、已知、约束、输出、陷阱。在题目已锁定、尚未分类或用户说「拆题」「读题」时使用。不要在还没读原文时凭记忆拆题。
license: MIT
metadata:
  author: cumcm-skills
  version: "0.1.0"
  invocation: model
  graph-node: N1
---

# problem-brief

## 何时使用

必须使用：`status` 为 `problem_locked`；用户上传新题要结构化。

禁止使用：没有赛题原文；用户只要分类（用 `problem-classify`）。禁止补题面没有的数据。

## 循环

目标：每个小问有 goal、inputs、outputs、constraints、traps。

`max_rounds`: 3

## 步骤

1. 逐段读 `problem/` 原文与附件说明。
2. 建表：背景 | 原理线索（物理/运筹/统计/规则）| 小问。
3. 每问写四要素：输入 → 决策（若无则写「无决策」）→ 目标 → 约束。
4. 标陷阱：单位、是否含边界、坐标系、时间起点、能否用题外数据。
5. 写 `problems[]`。不要生成装饰性脑图文件作为验收条件。

## 验收

- [ ] 小问数量与原文编号一致
- [ ] 每问 `outputs` 能在题面找到依据
- [ ] `traps` 至少检查过单位与数据口径（无陷阱则写「未发现」并指出检查了什么）
- [ ] 未推荐具体算法库

## 输出

`problems[]` 的拆题字段。`status` 仍 `problem_locked`（分类节点才改 classified）。

## 下一跳

`problem-classify`。
