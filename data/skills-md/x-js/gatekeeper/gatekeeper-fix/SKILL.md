---
name: gatekeeper-fix
description: Gatekeeper 整改子 skill（`/gatekeeper-fix`）。读取 review.md / test.md 中【状态=待整改】问题行针对性修复并回填，等待人工复核。仅人工触发。
version: "0.0.1"
author: X-JS
license: MIT
when-to-use: manual
metadata:
  tags: ["gatekeeper","fix"]
---

# 整改执行（gatekeeper-fix）

> 版本编号 = 当前 Git 分支名；留痕/归属/权限规则见 `gatekeeper` skill（第二、三节）。

## Procedure

### 1. 定位待整改问题
- 只读 `项目根/.gatekeeper/${版本编号}/review.md` / `test.md` 中【状态=待整改】行与最新轮次；无 → 提示可进 `/gatekeeper-next`，停止。

### 2. staging 先判归属
- 处理 test.md 问题前，先 read requirement.md 原文引用对应条目，判「需求已有 → 修复 / 需求未覆盖 → 不修，待人工补需求」。

### 3. 针对性修复
- 只改待整改项，不新增功能、不超范围、无依据不整改；误报置「无需整改」附理由。

### 4. 回填留痕（仅两列）
- 只改【状态】（待整改→已整改待复核 / 无需整改）与【整改结果】两列；接口契约变化须声明 apidoc 已同步。

### 5. 输出修复清单，提示人工复核
- 输出问题序号 + 处理结果 + 是否 apidoc 同步；不自行判定完成、不推进阶段。

## Pitfalls
1. 禁止无依据/超范围整改、私自清空问题记录。
2. 只回填两列，不碰 review/test 其他列或 requirement/progress。