---
name: spec-pack-abandon
description: Use when 需要因需求重大问题而废弃/撤销当前 Spec Pack，并且必须删除对应 `.aisdlc/specs/{branch}` 目录与本地/远程分支，同时需要在执行删除前输出删除清单并要求用户二次确认。
---

# spec-pack-abandon（废弃/撤销 Spec Pack：清单 + 二次确认 + 删除分支）

## 概览

当需求出现重大问题需要“废弃当前 spec pack”时，本技能用于**安全地撤销**：先用 `spec-context` 精确定位 `{FEATURE_DIR}`，再生成“将要删除的内容清单”，并在执行任何破坏性操作前要求用户**二次确认**；最后删除本地/远程分支，并清理工作区中残留的 spec pack 目录。

**开始时宣布：**「我正在使用 spec-pack-abandon 技能废弃当前 Spec Pack（输出删除清单并二次确认后删除目录与分支）。」

## 何时使用 / 不使用

- **使用时机**
  - 需求/约束出现重大问题，决定废弃当前 spec pack（不再继续澄清/设计/实现）。
  - 你需要删除：`.aisdlc/specs/{CURRENT_BRANCH}/` 以及该 `{CURRENT_BRANCH}` 分支（本地 + 远程）。
- **不要用在**
  - 你只是想“回退某个提交”或“重做需求文档”：优先用正常 git 回退/新提交，而不是删分支。
  - 当前不在 spec 分支（分支名不符合 `{num}-{short-name}`）：先切到目标 spec 分支再说；否则**停止**。

## 硬规则（必须遵守）

- **REQUIRED SUB-SKILL：先满足 `spec-context` 门禁并在对话中回显 `FEATURE_DIR=...`（允许 `(reuse)`）。**
- **禁止猜路径/猜分支**：只能使用 `Get-SpecContext` 的 `CURRENT_BRANCH` 与 `FEATURE_DIR`。
- **必须输出删除清单**：在任何删除命令前，先输出“将要删除的内容清单”（目录/分支/远程分支存在性/未提交更改概览）。
- **必须二次确认**：
  - 第一次确认：用户确认“删除清单无误”。
  - 第二次确认：用户确认“即将执行的具体删除命令无误”。
  - 两次确认都必须要求用户回复**精确短语**（见下文）。
- **禁止默认丢弃整个工作区**：不得建议/执行 `git clean -fd` 这类“全盘清空”命令来图省事。
- **遇到任何验证失败就停止**：不得继续给出“直接删”的命令。

## 删除清单生成（PowerShell）

> 本段只用于**生成清单与风险提示**，不执行删除。

```powershell
. (Join-Path (git rev-parse --show-toplevel) "skills\spec-context\scripts\spec-common.ps1")
$context = Get-SpecContext
$FEATURE_DIR = $context.FEATURE_DIR
Write-Host ("FEATURE_DIR={0}" -f $FEATURE_DIR)
Write-Host ("CURRENT_BRANCH={0}" -f $context.CURRENT_BRANCH)

$repoRoot = $context.REPO_ROOT
$branch = $context.CURRENT_BRANCH
$featureDir = $context.FEATURE_DIR
$demoDir = Join-Path $repoRoot ("demo\prototypes\{0}" -f $branch)

$hasRemote = $false
git ls-remote --exit-code --heads origin $branch *> $null
if ($LASTEXITCODE -eq 0) { $hasRemote = $true }

$dirty = git status --porcelain
$aheadBehind = git rev-list --left-right --count ("origin/{0}...{0}" -f $branch) 2>$null

Write-Host "=== 删除清单（待确认）==="
Write-Host ("REPO_ROOT: {0}" -f $repoRoot)
Write-Host ("CURRENT_BRANCH（将删除）: {0}" -f $branch)
Write-Host ("FEATURE_DIR（将删除/清理）: {0}" -f $featureDir)
Write-Host ("demo/prototypes（如存在将删除/清理）: {0}" -f $demoDir)
Write-Host ("远程分支 origin/{0} 是否存在: {1}" -f $branch, $hasRemote)
Write-Host ""
Write-Host "=== 工作区风险提示 ==="
if ($dirty) {
  Write-Host "检测到未提交更改（将随分支删除而丢失）。git status --porcelain："
  $dirty | ForEach-Object { Write-Host ("  {0}" -f $_) }
} else {
  Write-Host "未检测到未提交更改。"
}
if ($aheadBehind) {
  Write-Host ("与 origin/{0} 的 ahead/behind 计数（若分支未 push 可能为空/报错）： {1}" -f $branch, $aheadBehind)
}
```

### 第一次确认（必须）

把上面生成的“删除清单”原样展示给用户，然后要求用户回复以下精确短语：

- **第一次确认短语**：`确认删除清单`

若用户未明确回复该短语（或提出任何疑问/修改），**停止**，先修正清单再继续。

## 删除命令准备（只在第一次确认后展示）

> 本段仍然不执行删除；仅把“将要执行的命令”完整列出来作为第二次确认对象。

```powershell
. (Join-Path (git rev-parse --show-toplevel) "skills\spec-context\scripts\spec-common.ps1")
$context = Get-SpecContext
$branch = $context.CURRENT_BRANCH
$featureDir = $context.FEATURE_DIR
$repoRoot = $context.REPO_ROOT
$demoDir = Join-Path $repoRoot ("demo\prototypes\{0}" -f $branch)

$hasRemote = $false
git ls-remote --exit-code --heads origin $branch *> $null
if ($LASTEXITCODE -eq 0) { $hasRemote = $true }

@"
【将要执行的删除命令（待最终确认）】

1) 切到 main（避免在被删分支上删除）
git switch main
git pull

2) 清理本地残留目录（若存在）
if (Test-Path -LiteralPath `"$featureDir`") { Remove-Item -LiteralPath `"$featureDir`" -Recurse -Force }
if (Test-Path -LiteralPath `"$demoDir`") { Remove-Item -LiteralPath `"$demoDir`" -Recurse -Force }

3) 删除本地分支
git branch -D $branch

4) 删除远程分支（若存在）
"@ | Write-Host

if ($hasRemote) {
  Write-Host ("git push origin --delete {0}" -f $branch)
} else {
  Write-Host ("（跳过远程删除：未检测到 origin/{0}）" -f $branch)
}

```

### 第二次确认（必须）

要求用户在看到“将要执行的删除命令”后，回复以下精确短语：

- **第二次确认短语**：`最终确认执行删除`

未收到该短语前，**禁止**执行任何删除动作。

## 执行删除（只在二次确认后）

按“删除命令准备”里展示的命令执行即可。执行后做最小验收：

```powershell
git branch --list $branch
git branch -r | Select-String ("origin/{0}" -f $branch)
Test-Path -LiteralPath $featureDir
```

期望：
- `git branch --list $branch` 无输出
- 远程分支查询无匹配（若你执行了远程删除）
- `Test-Path $featureDir` 为 `False`

## 常见错误（出现即按硬规则停止）

- **跳过 `spec-context`**：用“看目录/看打开文件/猜分支名”的方式拼路径。
- **不出清单就删**：直接给 `git branch -D` / `git push --delete` / `Remove-Item`。
- **只确认一次**：用户说“删吧”不等于完成二次确认门禁。
- **用 `git clean -fd` 清空仓库**：这是全盘删除，极易误伤非 spec pack 文件。
- **删 main / 删错误分支**：任何分支名与 `Get-SpecContext.CURRENT_BRANCH` 不一致都必须停止。

