---
name: spec-context
description: Use when 需要在 sdlc-dev 的 Spec 流程中定位当前 spec pack（FEATURE_DIR）、避免在错误目录读写 requirements/*.md，或出现“看错上下文/写错文件/分支不符合规范”的问题。
---

# Spec 上下文定位（FEATURE_DIR）

## 概览

在任何 Spec 命令/技能里，只要会读写 `requirements/*.md`，就必须先确定 `{FEATURE_DIR}`。本仓库以 **当前 Git 分支名**作为 spec pack 的定位锚点，禁止猜路径。

## 何时使用

- 你将要读/写：`{FEATURE_DIR}/requirements/raw.md | solution.md | prd.md | prototype.md`
- 你不确定当前处于哪个 spec pack（担心读写错目录）
- 你看到“分支名不规范 / 目录结构不完整 / 缺 .aisdlc”之类上下文错误

## 唯一做法（PowerShell）

```powershell
. ".\spec-common.ps1"
$context = Get-SpecContext
$FEATURE_DIR = $context.FEATURE_DIR
Write-Host "FEATURE_DIR=$FEATURE_DIR"
```

## 硬规则（必须遵守）

- **先定位再读写**：任何读/写 `requirements/*.md` 之前，必须先运行上面的脚本并回显 `FEATURE_DIR=...`。
- **失败就停止**：`Get-SpecContext` 报错时，必须立刻停止，不得继续生成/写文件内容（否则几乎必然跑偏上下文）。
- **只用 FEATURE_DIR 拼路径**：后续所有路径都必须以 `$FEATURE_DIR` 为前缀（禁止用当前工作目录做相对路径猜测）。

## 常见错误

- **在非 spec 分支上执行**：分支名不符合 `{num}-{short-name}`，会导致无法定位 spec pack。
- **手写 `.aisdlc/specs/...` 路径**：人会写错，AI 更容易写错；必须以脚本输出为准。
- **继续执行“生成文档”**：只要上下文失败，就停止并先修复分支/目录结构。

