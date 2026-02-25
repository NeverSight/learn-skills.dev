---
name: spec-init
description: Use when 需要在本仓库的 AI SDLC 流程中初始化新的 Spec Pack（创建三位编号分支与 `.aisdlc/specs/{num}-{short-name}` 目录），或在执行 `spec-init` 时不确定输入解析、短名称规则、UTF-8 BOM 文件路径传参、脚本调用方式与输出物。
---

# spec-init

## 概览

`spec-init` 用于在本仓库里创建一个新的需求级 Spec Pack：自动递增三位编号、创建并切换到 `{num}-{short-name}` 分支、生成 `.aisdlc/specs/{num}-{short-name}/` 目录结构，并把原始需求写入 `requirements/raw.md`（UTF-8 with BOM）。

## 何时使用 / 不使用

- **使用时机**
  - 用户要开始一个“新需求”的 Spec（还没有 `{num}-{short-name}` 分支与 `.aisdlc/specs/...` 目录）。
  - 用户只给了中文需求文本（不方便先手动建文件），担心参数编码导致乱码。
  - 需要确保分支命名、编号来源、目录结构与后续命令（如 `spec-product-clarify`）一致。
- **不要用在**
  - 已经在一个合法的 `{num}-{short-name}` spec 分支上，且 `.aisdlc/specs/{num}-{short-name}/` 已存在并结构完整（这时直接进入后续命令）。

## 快速参考

- **分支命名**：`{num}-{short-name}`（`num` 为三位数字；`short-name` 为 kebab-case，小写字母/数字/连字符）
- **统一输出位置**：`.aisdlc/specs/{num}-{short-name}/`
- **必备子目录**：`requirements/`、`design/`、`implementation/`、`verification/`、`release/`
- **初始文件**：`requirements/raw.md`（内容=原始需求；编码=UTF-8 with BOM）
- **脚本入口**：`spec-create-branch.ps1` 的 `Main`
- **脚本参数**
  - `-ShortName`（必需）
  - `-SourceFilePath`（必需，必须是文件路径）
  - `-Title`（可选）
- **关键副作用**：脚本执行成功后会删除 `SourceFilePath` 指向的源文件（无论是原始文件还是临时文件）。

## 实施步骤（Agent 行为规范）

### 0) 预检（不要跳过）

- 确认当前工作目录在目标 Git 仓库内（`git rev-parse --show-toplevel` 能成功）。
- 确认 PowerShell 版本满足脚本要求（脚本声明 `#Requires -Version 7.0`）。
- 如果用户提供的是“文件路径”，提醒：该文件会被脚本删除；如需保留，先复制一份再传入。

### 1) 解析用户输入 → 一律落到文件路径

**强制规则：始终以文件路径方式传入需求内容**（避免中文内容在参数传递/编码上出问题）。

- **输入是文件路径**：直接用该路径作为 `$sourceFilePath`（但要提示“会被删除”）。
- **输入是文本**：创建临时文件并用 **UTF-8 with BOM** 写入，然后把临时文件路径作为 `$sourceFilePath`。

PowerShell 模板（文本 → BOM 临时文件）：

```powershell
$raw = @"
为现有后台系统新增‘批量导出订单’功能：支持按时间范围/状态筛选、CSV 与 XLSX 两种格式、导出任务异步执行并在导出中心可下载，权限仅管理员可见。
"@

$utf8Bom = [System.Text.UTF8Encoding]::new($true)
$tmp = Join-Path ([System.IO.Path]::GetTempPath()) ("sdlc-raw-{0}.md" -f ([guid]::NewGuid().ToString("N")))
[System.IO.File]::WriteAllText($tmp, $raw, $utf8Bom)
$sourceFilePath = $tmp
```

### 2) 生成 `short-name`（2-4 词，kebab-case）

从原始需求提炼 2-4 个词的短名称，优先“动词-名词”，保留常见技术缩写（如 `oauth2`、`jwt`、`api`）：

- 示例：批量导出订单 + 异步任务 → `export-orders-batch` 或 `add-order-export`
- 若不确定，宁可更通用、更短：`export-orders`

### 3) 调用脚本创建分支与 Spec Pack

**必须用 dot sourcing 加载脚本并调用 `Main`，不要直接运行脚本文件。**

```powershell
$repoRoot = (git rev-parse --show-toplevel)
. (Join-Path $repoRoot "skills\spec-init\spec-create-branch.ps1")

$shortName = "export-orders"
$title = ""

$result = Main -ShortName $shortName -SourceFilePath $sourceFilePath -Title $title
$result
```

### 4) 验收（DoD）

检查以下事实是否同时成立（缺一不可）：

- 当前分支名等于 `$result.branchName`，且符合 `{num}-{short-name}`。
- `.aisdlc/specs/$($result.branchName)/` 存在，且包含 5 个必需子目录。
- `.aisdlc/specs/$($result.branchName)/requirements/raw.md` 存在，内容等于原始需求，且为 UTF-8 with BOM。
- `$sourceFilePath` 指向的源文件已被删除（这不是 bug；若用户需要保留，应在步骤 1 之前自行备份）。

如需对 `raw.md` 的 **BOM** 做显式校验，可用下面片段检查前三个字节是否为 `EF BB BF`：

```powershell
$repoRoot = (git rev-parse --show-toplevel)
$rawPath = (Join-Path $repoRoot ".aisdlc\specs\$($result.branchName)\requirements\raw.md")
$bytes = [System.IO.File]::ReadAllBytes((Resolve-Path $rawPath))
($bytes.Length -ge 3) -and ($bytes[0] -eq 0xEF) -and ($bytes[1] -eq 0xBB) -and ($bytes[2] -eq 0xBF)
```

### 5) 完成后：自动进入 `spec-product-clarify`（R1）

**强制衔接规则**：`spec-init` 的 DoD 通过后，不要停在“提示下一步”，而是**立刻进入 R1**（澄清 + 方案对比 + 推荐决策），直到产出 `requirements/solution.md` 或用户明确停止。

**门禁（必须）**：先得到并回显 `FEATURE_DIR=...`（来自 `spec-context` / `Get-SpecContext`）。拿不到就**立刻停止**；**任何情况下禁止猜路径**（包括“从分支名推导”或手写 `.aisdlc/specs/...`）。

```powershell
$repoRoot = (git rev-parse --show-toplevel)
. (Join-Path $repoRoot "skills\spec-context\spec-common.ps1")
$context = Get-SpecContext
$FEATURE_DIR = $context.FEATURE_DIR
Write-Host "FEATURE_DIR=$FEATURE_DIR"
```

- 若脚本报错/用户禁止跑脚本/无法确认 `FEATURE_DIR`：**停止**；请用户在本机运行以上片段并把输出粘贴回来（不要继续写任何 `requirements/*.md`）。

**从这里开始严格按 `spec-product-clarify` 执行**（R1 的一次一问、回写、`solution.md` 模板与停止条件等细节以该技能为准；此处不重复）。

## 常见错误（以及怎么避免）

- **自创分支/目录结构**：不要用 `spec/<slug>`、`feature/<slug>`、`features/<slug>`；本仓库规范是 `{num}-{short-name}` + `.aisdlc/specs/...`。
- **把中文需求当作命令行参数直接传递**：一律写入 UTF-8 BOM 文件，再传路径。
- **误以为脚本不会删源文件**：它会删除 `SourceFilePath` 指向的文件；对用户的原始文件务必先确认是否需要备份。
- **短名称不规范**：避免大写、下划线、中文；避免前后连字符与连续 `--`；尽量 2-4 词。
