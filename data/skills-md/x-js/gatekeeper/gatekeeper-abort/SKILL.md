---
name: gatekeeper-abort
description: Gatekeeper 中止子 skill（`/gatekeeper-abort`）。核对留痕后将迭代目录标记「已中止」并迁移至 `项目根/.gatekeeper/history/${版本编号}/`。仅人工触发。
version: "0.0.1"
author: X-JS
license: MIT
when-to-use: manual
metadata:
  tags: ["gatekeeper","abort"]
---

# 中止归档（gatekeeper-abort）

> 版本编号 = 当前 Git 分支名；历史归档规则见 `gatekeeper` skill 第一节。

## Procedure

### 1. 核对留痕
- 只读 `项目根/.gatekeeper/${版本编号}/` 下 progress/review/test，确认当前阶段与留痕结论一致。

### 2. 标记并迁移
- 写独立标记文件（注明「已中止」+ 原因/日期，不动 progress.md）；整体迁至 `项目根/.gatekeeper/history/${版本编号}/`。

### 3. 输出
- 中止阶段、迁移路径、遗留未完成项清单。

## Pitfalls
1. 迁移前必须核对留痕一致，不遗留脏数据；不改动留痕文件内容。