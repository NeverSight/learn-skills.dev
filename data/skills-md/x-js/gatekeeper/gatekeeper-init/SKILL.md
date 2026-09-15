---
name: gatekeeper-init
description: Gatekeeper 初始化子 skill（`/gatekeeper-init`）。创建 `项目根/.gatekeeper/${版本编号}/` 并实例化 requirement.md / progress.md（模板取用 `gatekeeper` skill 的 `assets/`），校验占位符。仅人工触发。
version: "0.0.1"
author: X-JS
license: MIT
when-to-use: manual
metadata:
  tags: ["gatekeeper","init"]
---

# 初始化（gatekeeper-init）

> 版本编号 = 当前 Git 分支名（规则见 `gatekeeper` skill）。仅创建 requirement.md / progress.md；design/review/test 由 `gatekeeper-next` 按阶段实例化。

## Procedure

### 1. 创建目录
- `项目根/.gatekeeper/${版本编号}/` 不存在 → 创建。
- 已存在 → 列出文件询问人工（跳过/确认覆盖/补齐），未确认不写入；分支名含目录非法字符 → 中止询问。

### 2. 实例化模板
- 从 `gatekeeper` skill 的 `assets/` 复制：`_template-requirement.md` → requirement.md、`_template-progress.md` → progress.md。
- 将 `${版本编号}` 占位符替换为实际分支名；不做其他内容改动。

### 3. 校验（不通过不启动）
- 两份文件均存在且无 `${` 残留 → 通过。
- 不通过 → 输出失败项，写 `.init-incomplete` 标记，拒绝启动，等人工修复重跑。

### 4. 输出
- 目录路径 + 文件清单，提示人工填写 requirement.md 后进入需求阶段。

## Pitfalls
1. 仅做占位符替换，禁止修改模板业务内容；不得代写 requirement.md / progress.md。
2. 已存在目录禁止无确认覆盖。