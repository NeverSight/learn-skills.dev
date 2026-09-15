---
name: gatekeeper-finish
description: Gatekeeper 完结子 skill（`/gatekeeper-finish`）。归档校验四项齐备后迁移至 `项目根/.gatekeeper/history/${版本编号}/` 并提示收尾。仅人工触发。
version: "0.0.1"
author: X-JS
license: MIT
when-to-use: manual
metadata:
  tags: ["gatekeeper","finish"]
---

# 完结归档（gatekeeper-finish）

> 版本编号 = 当前 Git 分支名；职责见 `gatekeeper` skill 第八节。

## Procedure

### 1. 归档校验四项（不通过不归档）
| # | 校验项 | 判定 |
|---|--------|------|
| ① | progress.md 全部阶段已完成 | 任一未完成 → 不通过 |
| ② | 无待整改 / 复核驳回问题 | review/test 仍有 → 不通过 |
| ③ | 无 `${` / 「待填写」占位符残留 | 存在 → 不通过 |
| ④ | 各阶段状态与留痕结论一致 | 不一致 → 不通过 |

### 2. 迁移并提示收尾
- 任一不通过 → 输出失败项，要求人工复核，不迁移。
- 全部通过 → 整体迁至 `项目根/.gatekeeper/history/${版本编号}/`，输出放行结论 + 收尾提示。

## Pitfalls
1. 校验不通过禁止迁移；仅迁移目录，不改动留痕内容。