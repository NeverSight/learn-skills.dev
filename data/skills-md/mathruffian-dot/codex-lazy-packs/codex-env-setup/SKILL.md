---
name: codex-env-setup
description: Codex 環境建置（Codex Desktop、Node.js LTS、uv；CLI 選用）。說「建置環境」「安裝開發環境」時載入。
---

# Codex 環境建置

先判斷作業系統，再確認 Codex Desktop app 是否已安裝、登入。不要一開始就重裝所有工具。

本 Skill 不檢查 GitHub 帳號、不執行 `gh auth status`，也不安裝 Git 或 GitHub CLI。GitHub 相關設定全部留給 `codex-github`。

## 步驟一：檢查

Windows 使用 PowerShell：

```powershell
node --version
uv --version
```

只有使用者明確要使用 CLI 時才執行：

```powershell
codex --version
```

Node.js 需 18 以上，建議使用目前 LTS。缺少選用的 Codex CLI 不算 Desktop 環境失敗。

## 步驟二：只補裝缺少項目

### Windows

```powershell
winget install --id OpenJS.NodeJS.LTS --exact --accept-source-agreements --accept-package-agreements
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Codex Desktop app 尚未安裝時，可引導使用者到官方下載頁，或使用：

```powershell
winget install Codex -s msstore
```

### macOS

```shell
brew install node
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Linux

Linux 沒有 Codex Desktop app，使用 IDE 擴充或 Codex CLI。Node.js 依 NodeSource LTS 官方指示安裝，uv 使用：

```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
```

安裝後若目前程序仍找不到指令，先重開 PowerShell 或 Codex Desktop app，再重新檢查，不要立刻判定安裝失敗。

## 步驟三：驗收

至少確認：

- Codex Desktop app 能開啟並正常對話，或使用者選用的 IDE／CLI 可運作。
- `node --version` 為 18 以上。
- `uv --version` 有正常版本輸出。
- 只有選用 CLI 時，才要求 `codex --version` 成功。
- 全程沒有要求 GitHub 帳號或 GitHub 登入。

最終回報：已安裝／已補裝清單、版本、Codex 使用介面與登入狀態，以及仍需使用者手動完成的項目。
