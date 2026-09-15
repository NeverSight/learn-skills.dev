---
name: gatekeeper-next
description: Gatekeeper 阶段推进子 skill（`/gatekeeper-next`）。确认上一环节复核通过后，执行当前阶段职责并实例化所需模板。仅人工触发。
version: "0.0.1"
author: X-JS
license: MIT
when-to-use: manual
metadata:
  tags: ["gatekeeper","next"]
---

# 阶段推进（gatekeeper-next）

> 版本编号 = 当前 Git 分支名；放行/流转/留痕规则见 `gatekeeper` skill（第一、二、六节）。

## Procedure

### 1. 确认放行（不满足不推进）
- 只读 progress.md 定位首个未完成阶段；review/test 无【待整改】/【复核驳回】才推进，否则转 `/gatekeeper-fix`；未过设计评审（或未标跳过）不得编码。

### 2. 实例化模板（按需）
- 阶段2 建 design.md + review.md、阶段7 建 test.md：复制 `gatekeeper` skill 的 `assets/` 对应模板，替换 `${版本编号}`；已存在则跳过。小改动跳过阶段2 时，review.md 须在进入阶段4（dev 测试）前实例化。

### 3. 执行当前阶段职责
- 阶段2 概要设计：产出 design.md（含「变更点清单」+「关联历史迭代回归项」）；小改动提示人工标「跳过」。
- 阶段3 编码+单测：按变更点拆解编码，配套单测。
- 阶段4 dev 测试：后台+前端 dev 验证，回填 review.md 第三部分（每条标「对应验收§」，含回归回测）。
- 阶段5/7：review.md 已就绪直接交人工录入；阶段7 再实例化 test.md；待整改转 `/gatekeeper-fix`。
- 阶段8：提示人工部署 prod / 归档（转 `/gatekeeper-finish`）。

### 4. 输出
- 变更摘要 + 增量，提示人工下一步（评审/复核/提交留痕文件）。

## Pitfalls
1. 未过设计评审（或未标跳过）不得编码；禁止跨阶段工作。
2. 不主动轮询、不自行推进阶段。